"""Noise injection: invisible characters, blanked letters, stray spaces,
spurious letters or conjunctions added to the start of words, and small letters
overlapping the real ones."""

from .shaping import PASSTHROUGH, base, clusters, is_mark
from .structural import TATWEEL, insert_after, join_gaps

ZWJ = "‍"  # zero-width joiner: only safe where the letters already join
ZWSP = "​"  # zero-width space
WORD_JOINER = "⁠"
CGJ = "͏"  # combining grapheme joiner
INVISIBLE = [ZWSP, WORD_JOINER, CGJ]

FATHA, KASRA, SUKUN = "َ", "ِ", "ْ"
HURUF = {"و": FATHA, "ف": FATHA, "ك": FATHA, "ب": KASRA, "ل": KASRA}  # attached particles
LETTERS = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"  # ا–ي

BLANK_STYLES = {"kashida": TATWEEL, "underscore": "_", "dash": "-", "space": " ", "mix": None}  # mix: any of them


def zwc_word(word, rng, rate=1.0):
    """Insert invisible characters between a random `rate` fraction of letters.
    ZWJ is only used between letters that join anyway, where it changes nothing."""
    cs = clusters(word)
    joined = set(join_gaps(cs))
    fillers = {}
    for k in range(len(cs) - 1):
        if rng.random() < rate:
            fillers[k] = rng.choice(INVISIBLE + [ZWJ] if k in joined else INVISIBLE)
    return insert_after(cs, fillers)


def blank_word(word, rng, rate=0.2, style="kashida"):
    """Replace a random `rate` fraction of interior letters with a filler the
    reader has to fill in. At most half of a word's letters are blanked."""
    cs = clusters(word)
    interior = [k for k in range(1, len(cs) - 1) if rng.random() < rate]
    fillers = [f for f in BLANK_STYLES.values() if f]
    for k in interior[: len(cs) // 2]:
        cs[k] = BLANK_STYLES[style] or rng.choice(fillers)
    return "".join(cs)


def space_word(word, rng, rate=0.3):
    """With probability `rate`, split the word with a space at a random point."""
    cs = clusters(word)
    if len(cs) < 4 or rng.random() >= rate:
        return word
    return insert_after(cs, {rng.randrange(1, len(cs) - 2): " "})


def _vowelled(word):
    return any(is_mark(ch) for ch in word)


HURUF_STYLES = ("single", "stack")


def huruf_word(word, rng, rate=0.2, style="single"):
    """With probability `rate`, prefix spurious attached particles (و ف ك ب ل)
    with their usual vowels in vowelled text: one (single), or 1–3 piled up,
    repeats allowed (stack: وَوَالعَقْلُ, فَبِلِـ…)."""
    if rng.random() >= rate:
        return word
    vowelled = _vowelled(word)
    count = rng.randint(1, 3) if style == "stack" else 1
    out = ""
    for _ in range(count):
        harf = rng.choice(sorted(HURUF))
        if style == "single" and base(word) == harf:
            return word
        out += harf + (HURUF[harf] if vowelled else "")
    return out + word


def silent_word(word, rng, rate=0.2):
    """With probability `rate`, prefix a random letter. In vowelled text it gets
    a sukun, which no Arabic word can start with, hinting that it is silent."""
    if rng.random() >= rate:
        return word
    return rng.choice(LETTERS) + (SUKUN if _vowelled(word) else "") + word


# Small Arabic letters (Quranic annotation marks) that render on top of or
# under the letter they follow, so two letter shapes overlap.
OVERLAYS = [
    "\u0615",  # small high tah
    "\u0617",  # small high zain
    "\u06DC",  # small high seen
    "\u06E2",  # small high meem
    "\u06E3",  # small low seen
    "\u06E7",  # small high yeh
    "\u06E8",  # small high noon
    "\u06ED",  # small low meem
    "\u0670",  # superscript alef
]
assert all(is_mark(ch) for ch in OVERLAYS)


def overlap_word(word, rng, rate=0.2):
    """Stack a small letter on a random `rate` fraction of the letters."""
    return "".join(
        c + rng.choice(OVERLAYS) if base(c) not in PASSTHROUGH and rng.random() < rate else c
        for c in clusters(word)
    )
