"""Text-level transforms: inverting word order and breaking the line layout.

These run after the word transforms, on whole sentences or lines.
"""

import re

LRO, PDF = "\u202D", "\u202C"  # left-to-right override … pop directional formatting

# A clause: a run of text up to the next punctuation mark or line break.
CLAUSE_RE = re.compile(r"[^.!?؟؛،\n]+")

ORDER_STYLES = ("reverse", "swap", "shuffle")
LAYOUT_STYLES = ("lines", "mirror")


def order_text(text, rng, style="reverse"):
    """Invert the word order of each clause (reverse), swap random pairs of
    neighbouring words (swap), or put each clause's words in a random order
    (shuffle). Punctuation stays where it was."""

    def repl(m):
        clause = m.group()
        words = clause.split()
        if len(words) < 2:
            return clause
        if style == "reverse":
            words.reverse()
        elif style == "shuffle":
            original = words[:]
            while words == original and len(set(words)) > 1:
                rng.shuffle(words)
        else:
            i = 0
            while i < len(words) - 1:
                if rng.random() < 0.5:
                    words[i], words[i + 1] = words[i + 1], words[i]
                    i += 2
                else:
                    i += 1
        lead = clause[: len(clause) - len(clause.lstrip())]
        trail = clause[len(clause.rstrip()) :]
        return lead + " ".join(words) + trail

    return CLAUSE_RE.sub(repl, text)


def layout_text(text, rng, style="lines"):
    """lines  — hard line breaks after every 1–4 words, ignoring sentences.
    mirror — force each line left-to-right with a bidi override, so it is
             displayed back to front (codepoint order is unchanged)."""
    if style == "mirror":
        return "\n".join(LRO + line + PDF if line.strip() else line for line in text.split("\n"))
    paras = []
    for para in text.split("\n\n"):
        words = para.split()
        lines = []
        i = 0
        while i < len(words):
            n = rng.randint(1, 4)
            lines.append(" ".join(words[i : i + n]))
            i += n
        paras.append("\n".join(lines))
    return "\n\n".join(paras)
