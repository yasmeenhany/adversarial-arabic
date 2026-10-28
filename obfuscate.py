"""Apply stacked obfuscation transforms to an Arabic text file.

Examples:
    python3 obfuscate.py data/original_text.txt --mode dotless --seed 1 --html
    python3 obfuscate.py data/original_text.txt --mode dotless,disconnect --seed 1 --html
    python3 obfuscate.py data/original_text.txt --mode dotless,shuffle,kashida --kashida-rate 0.5
    python3 obfuscate.py data/akkad.txt --mode root,pattern,order --order-style swap --seed 1
    python3 obfuscate.py data/akkad.txt --mode 3,18,6 --seed 1   # same modes, by number
"""

import argparse
import html
from pathlib import Path

from arabic_obfuscator import (
    CHOICES,
    DEFAULTS,
    DOTTED,
    LOSSY,
    MODES,
    NUMBERS,
    TARGETS,
    normalize,
    obfuscate,
    parse_modes,
    strip_marks,
)


EXPERIMENTS = Path("experiments")
ORIGINAL_TITLE = "\u0627\u0644\u0623\u0635\u0644 (original)"  # الأصل
OBFUSCATED_TITLE = "\u0627\u0644\u0645\u0645\u0648\u0647 (obfuscated)"  # المموه


def write_preview(path, original, obfuscated):
    def block(title, text):
        paras = "".join(f"<p>{html.escape(p)}</p>" for p in text.split("\n\n"))
        return f"<section><h2>{title}</h2>{paras}</section>"

    path.write_text(
        f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Preview</title>
<style>
  body {{ font-family: "Geeza Pro", "Noto Naskh Arabic", "Amiri", serif;
         font-size: 22px; line-height: 1.9; display: flex; gap: 2em; margin: 2em; }}
  section {{ flex: 1; }}
  h2 {{ font-family: sans-serif; font-size: 16px; color: #666; }}
  p {{ white-space: pre-wrap; }}
</style></head><body>
{block(ORIGINAL_TITLE, original)}
{block(OBFUSCATED_TITLE, obfuscated)}
</body></html>
""",
        encoding="utf-8",
    )


# Two separate prompts per method, sent as separate requests, so restoring the
# text cannot help the model answer the questions.
PROMPT = """Read the Arabic text below and answer the questions that follow it.
Base your answers only on the text. Answer each question briefly, numbered to
match the question.

Text:
-----
{text}
-----

Questions:
{questions}
"""

RESTORE_PROMPT = """The Arabic text below may have been distorted: its letters, characters,
spelling, words or word order may have been altered. Restore it: rewrite it as
the clean, original Arabic text the author most likely wrote. Reply with the
restored text only.

Text:
-----
{text}
-----
"""


def write_prompts(out, text, questions_file):
    """<name>.prompt.txt (the questions, if there are any) and
    <name>.restore-prompt.txt (restore the text) next to `out`."""
    written = []
    if questions_file.exists():
        questions = questions_file.read_text(encoding="utf-8").strip()
        path = out.with_suffix(".prompt.txt")
        path.write_text(PROMPT.format(text=text.strip(), questions=questions), encoding="utf-8")
        written.append(path)
    else:
        print(f"no question prompt written ({questions_file} not found)")
    path = out.with_suffix(".restore-prompt.txt")
    path.write_text(RESTORE_PROMPT.format(text=text.strip()), encoding="utf-8")
    written.append(path)
    return written


def output_name(modes, options):
    """e.g. "10-dotless-0.5+disconnect": each mode with its method number, and
    only non-default settings."""

    def suffix(mode):
        return "".join(
            f"-{value:g}" if isinstance(value, float) else f"-{value}"
            for key, value in options.items()
            if key.startswith(mode + "_") and value != DEFAULTS[key]
        )

    return "+".join((f"{NUMBERS[m]}-" if m in NUMBERS else "") + m + suffix(m) for m in modes)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument(
        "--mode",
        default="both",
        help="comma-separated modes, by name or number: "
        + ", ".join(f"{NUMBERS[m]}={m}" if m in NUMBERS else m for m in sorted(MODES, key=lambda m: NUMBERS.get(m, 99)))
        + ", or 'both' (homoglyph+presentation)",
    )
    parser.add_argument("--rate", type=float, default=1.0, help="fraction of words to alter")
    parser.add_argument(
        "--target",
        choices=TARGETS,
        default="all",
        help="words the word-level methods may alter: all, content (nouns, verbs, adjectives, names, "
        "numbers), function (the rest), or random (as many as content, chosen at random)",
    )
    parser.add_argument("--seed", type=int)
    parser.add_argument("--html", action="store_true", help="also write a side-by-side preview")
    group = parser.add_argument_group("per-transform settings")
    for key, default in DEFAULTS.items():
        flag = "--" + key.replace("_", "-")
        if key in CHOICES:
            group.add_argument(flag, choices=CHOICES[key], default=default)
        else:
            group.add_argument(flag, type=float, default=default, metavar="RATE")
    args = parser.parse_args()

    original = args.input.read_text(encoding="utf-8")
    modes = parse_modes(args.mode)
    options = {key: getattr(args, key) for key in DEFAULTS}
    result = obfuscate(original, mode=args.mode, rate=args.rate, seed=args.seed, target=args.target, **options)

    # One folder per text, and inside it one per method (combination), holding
    # everything for that method: text, prompt, preview, replies and scores.
    label = output_name(modes, options) + (f"-on-{args.target}" if args.target != "all" else "")
    out = args.output or EXPERIMENTS / args.input.stem / label / f"{args.input.stem}.{label}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    print(f"wrote {out}")

    letters = [ch for ch in result if ch.isalpha() and ch != "\u0640"]
    print(f"characters: {len(original)} -> {len(result)}")
    if {"homoglyph", "presentation"} & set(modes):
        spoofed = sum(ch in "\u06A9\u06CC" or "\uFB50" <= ch <= "\uFEFF" for ch in letters)
        print(f"spoofed codepoints: {spoofed}/{len(letters)} letters ({spoofed / len(letters):.0%})")
    if "dotless" in modes:
        undotted = sum(ch in DOTTED for ch in original) - sum(ch in DOTTED for ch in result)
        print(f"letters undotted: {undotted}")
    if "tashkeel" in modes:
        marks = len(result) - len(strip_marks(result))
        print(f"diacritics added: {marks} ({marks / len(letters):.1f} per letter)")

    lossy = LOSSY & set(modes)
    if lossy:
        print(f"round-trip check skipped ({', '.join(sorted(lossy))} is lossy)")
    else:
        remove = bool({"tashkeel", "overlap"} & set(modes))
        same = normalize(result, remove_marks=remove) == (strip_marks(original) if remove else original)
        print(f"round-trip normalize == original: {same}")

    for prompt in write_prompts(out, result, args.input.with_suffix(".questions.txt")):
        print(f"wrote {prompt}")

    if args.html:
        preview = out.with_suffix(".html")
        write_preview(preview, original, result)
        print(f"wrote {preview}")


if __name__ == "__main__":
    main()
