"""Send each method's two prompts to models on OpenRouter, then score the
replies: the answers to the questions and the restored text.

The question prompt (.prompt.txt) and the restore prompt (.restore-prompt.txt)
are separate requests, so restoring cannot help the model answer. Replies are
saved in the method's folder and reused on later runs unless --rerun is given.
A judge model grades the answers against the expected ones and, in a separate
call, the restored text against the original (out of 10, alongside an
automatic similarity measure); --judge keywords skips the judge. One report
covers both, and a row is added to results.md. File names carry the model
that answered and the judge, e.g.
    experiments/akkad/2-homoglyph/akkad.2-homoglyph.anthropic-claude-sonnet-5.5.answer.reply.txt
    experiments/akkad/2-homoglyph/akkad.2-homoglyph.anthropic-claude-sonnet-5.5.restore.reply.txt
    experiments/akkad/2-homoglyph/akkad.2-homoglyph.anthropic-claude-sonnet-5.5.judge-openai-gpt-5.6-terra.scores.md

Needs an OpenRouter API key in the environment:
    export OPENROUTER_API_KEY="sk-or-..."

Examples:
    python3 run_llm.py experiments/akkad/2-homoglyph/akkad.2-homoglyph.prompt.txt
    python3 run_llm.py experiments/akkad/*/*.prompt.txt --model anthropic/claude-sonnet-5.5,google/gemini-3.8-flash
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from score import cell, keyword_grader, load_qa, parse_prompt_name, run_path, score_reply

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-sonnet-5.5"
DEFAULT_JUDGE = "openai/gpt-5.6-terra"
RETRIES = 3
# Upper bound on each reply. Without one, OpenRouter reserves credit for the
# model's maximum output (often 64k tokens) and may refuse the request. Ten
# short answers need a few hundred tokens; the rest is headroom for models
# that reason before answering.
MAX_TOKENS = 4000
JUDGE_MAX_TOKENS = 2000  # the verdict is a short JSON object


def ssl_context():
    """Certificates for HTTPS. The python.org installers for macOS ship without
    any (until "Install Certificates.command" is run), so fall back to certifi
    or to the bundle macOS itself provides."""
    if ssl.get_default_verify_paths().cafile:
        return ssl.create_default_context()
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    if Path("/etc/ssl/cert.pem").exists():
        return ssl.create_default_context(cafile="/etc/ssl/cert.pem")
    return ssl.create_default_context()


SSL_CONTEXT = ssl_context()

JUDGE_PROMPT = """You are grading answers to reading-comprehension questions about an Arabic text.
For each question, compare the model's answer with the expected answer:
  1   — same meaning as the expected answer (paraphrases and synonyms count)
  0.5 — partly right: an essential part is missing or slightly wrong
  0   — wrong, missing, or contradicts the expected answer
Grade only against the expected answer, not against your own knowledge of the
text. The model's answer may be in Arabic or English.

Reply with JSON only, in this form:
{{"scores": [{{"q": 1, "score": 1, "reason": "short reason"}}, ...]}}

{items}"""


RESTORE_JUDGE_PROMPT = """You are grading how well a model restored a distorted Arabic text to
its original. Compare the restored text with the original word by word.
Ignore diacritics (tashkeel), punctuation, line breaks, and spelling variants
of hamza/alef, ta marbuta (ة/ه) and alef maqsura (ى/ي).

Score from 0 to 10:
  10   — the same words as the original
  8–9  — a few wrong or missing words; the meaning is fully intact
  5–7  — several wrong words, but the main ideas are intact
  2–4  — many wrong words; the meaning is partly lost
  0–1  — not restored, or mostly different from the original

Reply with JSON only, in this form (list at most 10 errors, most important first):
{"score": 8, "reason": "short reason", "errors": [{"original": "word", "restored": "word"}]}

Original:
-----
ORIGINAL
-----

Restored:
-----
RESTORED
-----"""


class CutOff(RuntimeError):
    """The reply hit the token cap; `partial` holds what arrived."""

    def __init__(self, message, partial):
        super().__init__(message)
        self.partial = partial


def chat(model, prompt, key, max_tokens=MAX_TOKENS):
    """One user message to `model`; returns (reply text, cost in USD or None)."""
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": max_tokens,
            "usage": {"include": True},
        }
    ).encode()
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Title": "Adversarial Arabic",
        },
    )
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(request, timeout=300, context=SSL_CONTEXT) as response:
                data = json.load(response)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and attempt + 1 < RETRIES:
                wait = 5 * 2**attempt
                print(f"  {model}: HTTP {e.code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            raise RuntimeError(f"{model}: HTTP {e.code}: {detail}") from None
    if "error" in data:
        raise RuntimeError(f"{model}: {data['error']}")
    choice = data["choices"][0]
    content = choice["message"].get("content") or ""
    if isinstance(content, list):  # some providers return content parts
        content = "".join(part.get("text", "") for part in content)
    if choice.get("finish_reason") == "length":
        raise CutOff(
            f"{model}: reply cut off at {max_tokens} tokens (reasoning models count their "
            "thinking too); rerun with a higher --max-tokens",
            content,
        )
    return content, (data.get("usage") or {}).get("cost")


def parse_judgement(text, n):
    """[(score, reason)] for questions 1..n from the judge's JSON reply."""
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"judge did not return JSON:\n{text}")
    by_q = {}
    for item in json.loads(match.group())["scores"]:
        score = float(item["score"])
        if score not in (0, 0.5, 1):
            raise ValueError(f"judge gave an invalid score {score} for Q{item['q']}")
        by_q[int(item["q"])] = (score, str(item.get("reason", "")))
    missing = [q for q in range(1, n + 1) if q not in by_q]
    if missing:
        raise ValueError(f"judge skipped questions {missing}")
    return [by_q[q] for q in range(1, n + 1)]


def parse_restoration(text):
    """(score 0–10, reason, [(original, restored)]) from the judge's JSON reply."""
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"restoration judge did not return JSON:\n{text}")
    data = json.loads(match.group())
    score = float(data["score"])
    if not 0 <= score <= 10:
        raise ValueError(f"restoration judge gave an invalid score {score}")
    errors = [(str(e.get("original", "")), str(e.get("restored", ""))) for e in data.get("errors", [])][:10]
    return score, str(data.get("reason", "")), errors


def restoration_judge(judge, key, costs, max_tokens):
    def grade(original, restored):
        prompt = RESTORE_JUDGE_PROMPT.replace("ORIGINAL", original).replace("RESTORED", restored)
        text, cost = chat(judge, prompt, key, max_tokens)
        costs.append(cost)
        return parse_restoration(text)

    return grade


def judge_grader(judge, key, costs, max_tokens):
    def grade(qa, answers):
        items = "\n\n".join(
            f"Q{i}: {item['q']}\nExpected: {item['a']}\nModel's answer: {cell(answer)}"
            for i, (item, answer) in enumerate(zip(qa, answers), 1)
        )
        text, cost = chat(judge, JUDGE_PROMPT.format(items=items), key, max_tokens)
        costs.append(cost)
        return parse_judgement(text, len(qa))

    return grade


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "prompts", type=Path, nargs="+", help=".prompt.txt files made by obfuscate.py (the .restore-prompt.txt next to each is sent too)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"OpenRouter model id(s) to test, comma-separated (default {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--judge",
        default=DEFAULT_JUDGE,
        help=f"OpenRouter model that grades the answers (default {DEFAULT_JUDGE}), "
        "or 'keywords' for the keyword suggestions",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=MAX_TOKENS, help=f"cap on each reply's length (default {MAX_TOKENS}; the judge uses at most {JUDGE_MAX_TOKENS})"
    )
    parser.add_argument("--rerun", action="store_true", help="request new replies even if saved ones exist")
    parser.add_argument("--notes", default="", help="notes for the results table")
    parser.add_argument("--no-record", action="store_true", help="do not add rows to results.md")
    args = parser.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit('OPENROUTER_API_KEY is not set: export OPENROUTER_API_KEY="sk-or-..."')
    models = [m.strip() for m in args.model.split(",") if m.strip()]
    for prompt in args.prompts:
        load_qa(parse_prompt_name(prompt)[0])  # fail early on a missing answer key

    if args.judge != "keywords":
        same = [m for m in models if m.split("/")[0] == args.judge.split("/")[0]]
        if same:
            print(f"warning: {args.judge} is judging models from its own provider ({', '.join(same)}); "
                  "consider --judge with another provider's model")

    costs = []
    judge_tokens = min(args.max_tokens, JUDGE_MAX_TOKENS)
    if args.judge == "keywords":
        grader, restorer = keyword_grader, None
    else:
        grader = judge_grader(args.judge, key, costs, judge_tokens)
        restorer = restoration_judge(args.judge, key, costs, judge_tokens)
    judge = args.judge
    def get_reply(prompt_file, model, task):
        """The model's reply to `prompt_file`: reused from an earlier run if
        saved (unless --rerun), otherwise requested and saved."""
        saved = run_path(prompt, model, f"{task}.reply.txt")
        if saved.exists() and not args.rerun:
            print(f"{task}: reusing {saved}")
            return saved.read_text(encoding="utf-8")
        try:
            reply, cost = chat(model, prompt_file.read_text(encoding="utf-8"), key, args.max_tokens)
        except CutOff as e:
            partial = saved.with_name(saved.name.replace(".reply.txt", ".reply.partial.txt"))
            partial.write_text(e.partial, encoding="utf-8")
            sys.exit(f"{e}\nThe cut-off reply is in {partial}")
        costs.append(cost)
        saved.write_text(reply, encoding="utf-8")
        print(f"{task}: wrote {saved}")
        return reply

    for prompt in args.prompts:
        restore_prompt = prompt.with_name(prompt.name.replace(".prompt.txt", ".restore-prompt.txt"))
        for model in models:
            print(f"\n{prompt.parent.name} → {model}")
            reply = get_reply(prompt, model, "answer")
            restore_reply = get_reply(restore_prompt, model, "restore") if restore_prompt.exists() else None
            if restore_reply is None:
                print(f"restore: skipped ({restore_prompt.name} not found)")
            score_reply(prompt, model, reply, grader, judge, args.notes, not args.no_record, restorer, restore_reply)

    known = [c for c in costs if c is not None]
    if known:
        print(f"\nOpenRouter cost: ${sum(known):.4f} ({len(known)}/{len(costs)} calls reported a cost)")


if __name__ == "__main__":
    main()
