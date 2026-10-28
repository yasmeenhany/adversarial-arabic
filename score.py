"""Score an LLM's replies to the prompts made by obfuscate.py: its answers to
the questions (.prompt.txt) and, optionally, its restored text
(.restore-prompt.txt).

Paste the model's answers when asked (finish with Ctrl-D on a new line), or pass
them with --answer. For each question the expected answer, the model's answer
and a suggested score are shown; press Enter to accept the suggestion or type
1, 0.5 or 0. With --restored, the restored text is compared with the original
automatically (character and word similarity); run_llm.py also has it graded
by the judge. The report is saved next to the prompt and a summary row is
added to results.md. Name chat-app runs clearly, e.g. --model gemini-app.

Examples:
    python3 score.py experiments/akkad/2-homoglyph/akkad.2-homoglyph.prompt.txt --model claude-app
    python3 score.py experiments/akkad/10-dotless/akkad.10-dotless.prompt.txt --model chatgpt-app \
        --answer answers.txt --restored restored.txt --auto
"""

import argparse
import datetime
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

RESULTS = Path("results.md")
SCORES = ("1", "0.5", "0")

# A numbered item at the start of a line: "1.", "1)", "**1.**", "- 1:", "### 1 -"
MARKER = re.compile(r"^[\s>*#\-]*\**\s*(\d{1,2})\s*[.):\-]", re.M)
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
STOPWORDS = set(
    """a an and are as at be by for from has have he her his in into is it its
    of on or she that the their them they this to was were what which who whom
    with does do did not no only before after than then there one ones person""".split()
)


def parse_prompt_name(path):
    """akkad.root-permute+pattern.prompt.txt → ("akkad", "root-permute+pattern")."""
    name = path.name.removesuffix(".prompt.txt")
    text, _, mode = name.partition(".")
    return text, mode


def clean_restored(reply):
    """The restored text from a restore reply, without code fences, rules or a
    leading heading such as "Restored text:"."""
    text = re.sub(r"^\s*(```\w*|-{3,})\s*$", "", reply, flags=re.M)
    text = re.sub(r"^[#*\s]*(restored text|النص المستعاد|النص المصحح)[*:\s]*\n", "", text.strip(), flags=re.I)
    return text.strip()


ALEF_FORMS = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه", "ک": "ك", "ی": "ي"})


def plain_arabic(text):
    """Text reduced to bare letters and single spaces: no diacritics, invisible
    characters, tatweel or punctuation, presentation forms folded back, and
    hamza/alef, alef maqsura and ta marbuta spellings unified."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(
        ch for ch in text if not unicodedata.combining(ch) and unicodedata.category(ch) != "Cf" and ch != "ـ"
    )
    text = re.sub(r"[^\w\s]|_", " ", text.translate(ALEF_FORMS))
    return " ".join(text.split())


def similarity(original, restored):
    """(character similarity, share of the original's words recovered in order),
    both 0–1, ignoring diacritics, punctuation and spelling variants."""
    a, b = plain_arabic(original), plain_arabic(restored)
    if not a or not b:
        return 0.0, 0.0
    chars = SequenceMatcher(None, a, b, autojunk=False).ratio()
    wa, wb = a.split(), b.split()
    matched = sum(block.size for block in SequenceMatcher(None, wa, wb, autojunk=False).get_matching_blocks())
    return chars, matched / len(wa)


def split_answers(reply, n):
    """Cut the reply into answers 1..n at its numbered lines."""
    reply = reply.translate(ARABIC_DIGITS)
    starts = []
    for m in MARKER.finditer(reply):
        if int(m.group(1)) == len(starts) + 1:
            starts.append(m)
        if len(starts) == n:
            break
    answers = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(reply)
        answers.append(reply[m.end() : end].replace("**", "").strip())
    return answers + [""] * (n - len(answers))


def tokens(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return [t for t in re.findall(r"\w+", text) if t not in STOPWORDS]


def _matches(term, answer, got):
    """A key term matches a word it starts (English stems such as "obligat"),
    any word containing it (Arabic, where clitics attach), or a phrase."""
    term = " ".join(tokens(term)) if " " in term else term.lower()
    if " " in term:
        return term in " ".join(got)
    if term.isascii():
        return any(t.startswith(term) for t in got)
    return any(term in t for t in got)


def _rating(coverage):
    return "1" if coverage >= 0.75 else "0.5" if coverage >= 0.34 else "0"


def suggest(item, answer):
    """Suggested score. With a "key" (groups of accepted words) in the question
    file: the fraction of groups the answer matches. Otherwise: how many of the
    expected answer's words (not already in the question) appear in the answer,
    with numbers matched exactly."""
    if not answer:
        return "0"
    question, expected = item["q"], item["a"]
    if item.get("key"):
        got = tokens(answer)
        hits = sum(any(_matches(term, answer, got) for term in group) for group in item["key"])
        return _rating(hits / len(item["key"]))
    asked = {t[:5] for t in tokens(question)}
    key = [t for t in tokens(expected) if t.isdigit() or t[:5] not in asked] or tokens(expected)
    got = tokens(answer)
    stems = {t[:5] for t in got}
    hits = sum((t in got) if t.isdigit() else (t[:5] in stems) for t in key)
    return _rating(hits / len(key) if key else 0)


def ask(tty, prompt):
    print(prompt, end="", flush=True)
    return tty.readline().strip()


def cell(text):
    return " ".join(text.split()).replace("|", "\\|") or "—"


def quote(text):
    """Markdown blockquote, one quoted paragraph per paragraph of `text`."""
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text.strip())]
    return "\n>\n".join(f"> {p}" for p in paras if p)


def fmt(x):
    return f"{x:g}"


def add_result_row(row):
    """Insert `row` at the end of the first table in results.md."""
    lines = RESULTS.read_text(encoding="utf-8").split("\n")
    first = next(i for i, l in enumerate(lines) if l.startswith("|"))
    last = first
    while last + 1 < len(lines) and lines[last + 1].startswith("|"):
        last += 1
    lines.insert(last + 1, row)
    RESULTS.write_text("\n".join(lines), encoding="utf-8")


def load_qa(text):
    questions = Path(f"data/{text}.questions.json")
    if not questions.exists():
        sys.exit(f"no answer key for '{text}': {questions} not found")
    return json.loads(questions.read_text(encoding="utf-8"))


def file_label(model):
    """A model name safe for file names: "google/gemini-3.8-flash" → "google-gemini-3.8-flash"."""
    return re.sub(r"[/:\s]+", "-", model)


def run_path(prompt, model, kind, judge=None):
    """<text>.<mode>.<model>[.judge-<judge>].<kind>, in the prompt's folder, e.g.
    experiments/akkad/2-homoglyph/akkad.2-homoglyph.anthropic-claude-sonnet-5.5.judge-openai-gpt-5.6-terra.scores.md"""
    text, mode = parse_prompt_name(prompt)
    judged = f".judge-{file_label(judge)}" if judge else ""
    return prompt.with_name(f"{text}.{mode}.{file_label(model)}{judged}.{kind}")


def interactive_grader(tty):
    """Show each answer with a suggested score and let the user confirm it."""

    def grade(qa, answers):
        out = []
        for i, (item, answer) in enumerate(zip(qa, answers), 1):
            guess = suggest(item, answer)
            print(f"\n[{i}/{len(qa)}] {item['q']}")
            print(f"  expected: {item['a']}")
            print(f"  model:    {cell(answer)}")
            while True:
                typed = ask(tty, f"  score [{guess}]: ")
                typed = "0.5" if typed == ".5" else typed
                if typed in ("",) + SCORES:
                    break
                print("  type 1, 0.5 or 0 (Enter accepts the suggestion)")
            out.append((float(typed or guess), ""))
        return out

    return grade


def keyword_grader(qa, answers):
    """Accept every suggested score."""
    return [(float(suggest(item, answer)), "") for item, answer in zip(qa, answers)]


def score_reply(prompt, model, reply, grader, judge, notes="", record=True, restoration_grader=None, restore_reply=None):
    """Grade the answers in `reply` (to the question prompt) and, if given, the
    `restore_reply` (to the restore prompt); write the report and (if `record`)
    add a summary row to results.md. `judge` names who scored them (a model
    id, "manual" or "keywords"); `restoration_grader(original, restored)`, if
    given, returns (score out of 10, reason, [(original word, restored word)]).
    Returns the total answer score."""
    text, mode = parse_prompt_name(prompt)
    qa = load_qa(text)
    original = Path(f"data/{text}.txt").read_text(encoding="utf-8").strip()
    asked = restore_reply is not None
    restored = clean_restored(restore_reply) if asked else ""
    answers = split_answers(reply, len(qa))
    found = sum(bool(a) for a in answers)
    if found < len(qa):
        print(f"warning: found numbered answers for {found}/{len(qa)} questions")

    if asked and not restored:
        print("warning: the restore reply is empty")
    chars, words = similarity(original, restored)
    restoration = None  # (score, reason, errors)
    if asked and restoration_grader:
        restoration = restoration_grader(original, restored) if restored else (0, "empty restore reply", [])

    graded = grader(qa, answers)
    scores = [s for s, _ in graded]
    reasons = [r for _, r in graded]
    total = sum(scores)
    date = datetime.date.today().isoformat()

    show_reasons = any(reasons)
    head = f"| Q | Question | Expected | {model} | Score |" + (" Judge's reason |" if show_reasons else "")
    rule = "|---|---|---|---|---|" + ("---|" if show_reasons else "")
    rows = "\n".join(
        f"| {i} | {cell(item['q'])} | {cell(item['a'])} | {cell(ans)} | {fmt(s)} |"
        + (f" {cell(r)} |" if show_reasons else "")
        for i, (item, ans, s, r) in enumerate(zip(qa, answers, scores, reasons), 1)
    )
    similar = f"{chars:.0%} characters, {words:.0%} words" if restored else "empty"
    if restoration:
        r_score, r_reason, r_errors = restoration
        r_summary = f"{fmt(r_score)}/10 ({similar})"
        errors = "".join(f"| {cell(o)} | {cell(r)} |\n" for o, r in r_errors)
        r_section = (
            f"Judge: {fmt(r_score)}/10 — {r_reason}  \nSimilarity to the original: {similar}\n\n"
            + (f"| Original | Restored |\n|---|---|\n{errors}\n" if errors else "")
        )
    elif asked:
        r_summary = similar
        r_section = f"Similarity to the original: {similar}\n\n"
    else:
        r_summary = "—"
        r_section = "Not run (no restore reply).\n\n"
    if restored:
        r_section += f"Restored:\n\n{quote(restored)}\n\nOriginal:\n\n{quote(original)}\n\n"

    report = run_path(prompt, model, "scores.md", judge)
    report.write_text(
        f"# {text} — {mode} — {model}\n\n"
        f"Date: {date}  \nAnswers: {fmt(total)}/{len(qa)}  \nRestoration: {r_summary}  \n"
        f"Scored by: {judge}  \nPrompt: `{prompt}`\n\n"
        f"## Answers\n\n{head}\n{rule}\n{rows}\n\n"
        f"## Restoration\n\n{r_section}"
        f"## Answer reply\n\n```\n{reply.strip()}\n```\n"
        + (f"\n## Restore reply\n\n```\n{restore_reply.strip()}\n```\n" if asked else ""),
        encoding="utf-8",
    )
    print(f"answers: {fmt(total)}/{len(qa)}")
    print(f"restoration: {r_summary}")
    print(f"wrote {report}")

    if record:
        add_result_row(
            f"| {date} | {text} | {mode} | {model} | {fmt(total)}/{len(qa)} | {r_summary} | {judge} | "
            f"{cell(notes) if notes else ''} |"
        )
        print(f"added a row to {RESULTS}")
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("prompt", type=Path, help="the .prompt.txt file the model was given")
    parser.add_argument("--model", required=True, help="model name for the results table")
    parser.add_argument("--answer", type=Path, help="file with the model's answers (default: paste them)")
    parser.add_argument("--restored", type=Path, help="file with the model's reply to the restore prompt")
    parser.add_argument("--auto", action="store_true", help="accept every suggested score")
    parser.add_argument("--notes", default="", help="notes for the results table")
    parser.add_argument("--no-record", action="store_true", help="do not add a row to results.md")
    args = parser.parse_args()

    load_qa(parse_prompt_name(args.prompt)[0])  # fail before asking for the reply
    if args.answer:
        reply = args.answer.read_text(encoding="utf-8")
    else:
        print("Paste the model's reply, then press Ctrl-D on a new line:\n")
        reply = sys.stdin.read()
    grader = keyword_grader if args.auto else interactive_grader(open("/dev/tty", encoding="utf-8"))
    judge = "keywords" if args.auto else "manual"
    restore_reply = args.restored.read_text(encoding="utf-8") if args.restored else None
    score_reply(args.prompt, args.model, reply, grader, judge, args.notes, not args.no_record, None, restore_reply)


if __name__ == "__main__":
    main()
