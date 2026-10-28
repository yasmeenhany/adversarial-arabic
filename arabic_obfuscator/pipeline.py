"""The `obfuscate` pipeline that stacks the individual transforms."""

import random
import unicodedata

from .arabizi import STYLES as ARABIZI_STYLES, arabizi_word
from .dotless import dotless_word
from .homoglyph import ALEF_MAQSURA, FARSI_YEH, KAF, KEHEH, YEH, altglyph_word, homoglyph_word
from .layout import LAYOUT_STYLES, ORDER_STYLES, layout_text, order_text
from .linguistic import DIALECT_LEVELS, DIALECT_STYLES, conjunction_word, dialect_text, gender_word, number_word
from .morphology import ROOT_STYLES, pattern_word, root_word
from .noise import (
    BLANK_STYLES,
    HURUF_STYLES,
    CGJ,
    WORD_JOINER,
    ZWJ,
    ZWSP,
    blank_word,
    huruf_word,
    overlap_word,
    silent_word,
    space_word,
    zwc_word,
)
from .shaping import FINA, ISOL, WORD_RE, is_mark, positional_forms, to_presentation
from .structural import TATWEEL, ZWNJ, disconnect_word, kashida_word, shuffle_word
from .tashkeel import CASE_STYLES, STYLES as TASHKEEL_STYLES, case_word, tashkeel_word

# Transforms are always applied in this order, whatever order they are given in:
#   - dialect works on the whole text (it rewrites "قبل أن" as a phrase);
#   - the language-level swaps need clean words to recognise them;
#   - letters are then added, moved or blanked, which decides each letter's
#     position (and kashida only stretches joins that disconnect left intact);
#   - the position-dependent glyph swaps follow;
#   - tashkeel replaces any existing marks, so case (which clashes the final
#     marks) comes after it, and arabizi after both, to read the vowels;
#   - presentation forms freeze each glyph's shape, so they come last among
#     the visible changes, followed only by the overlaid and invisible marks;
#   - word order and line layout work on whole clauses and lines.
MODES = (
    "dialect",
    "conjunction",
    "gender",
    "number",
    "root",
    "pattern",
    "huruf",
    "silent",
    "shuffle",
    "blank",
    "space",
    "disconnect",
    "kashida",
    "dotless",
    "homoglyph",
    "altglyph",
    "tashkeel",
    "case",
    "arabizi",
    "presentation",
    "overlap",
    "zwc",
    "order",
    "layout",
)
# Each method's number in the project's list of obfuscation methods. It labels
# the output files and can be used in place of the name in a mode spec.
# disconnect is not on the list.
NUMBERS = {
    "zwc": 1,
    "homoglyph": 2,
    "root": 3,
    "gender": 4,
    "number": 5,
    "order": 6,
    "layout": 7,
    "tashkeel": 8,
    "kashida": 9,
    "dotless": 10,
    "shuffle": 11,
    "arabizi": 12,
    "presentation": 13,
    "altglyph": 14,
    "dialect": 15,
    "conjunction": 16,
    "case": 17,
    "pattern": 18,
    "blank": 19,
    "space": 20,
    "huruf": 21,
    "silent": 22,
    "overlap": 23,
}
BY_NUMBER = {str(n): m for m, n in NUMBERS.items()}
TEXT_BEFORE = {"dialect"}
TEXT_AFTER = {"order", "layout"}
ALIASES = {"both": ["homoglyph", "presentation"]}
# Cannot be undone by `normalize`.
LOSSY = set(MODES) - {"disconnect", "kashida", "homoglyph", "tashkeel", "presentation", "overlap", "zwc"}

# Per-transform settings, named "<mode>_<setting>". CHOICES lists the allowed
# values of the string settings.
DEFAULTS = {
    "dialect_rate": 1.0,
    "dialect_style": "mix",
    "dialect_level": "basic",
    "conjunction_rate": 1.0,
    "gender_rate": 0.7,
    "number_rate": 0.7,
    "root_rate": 0.5,
    "root_style": "replace",
    "pattern_rate": 0.5,
    "huruf_rate": 0.2,
    "huruf_style": "single",
    "silent_rate": 0.2,
    "blank_rate": 0.2,
    "blank_style": "kashida",
    "space_rate": 0.3,
    "disconnect_rate": 1.0,
    "kashida_rate": 0.3,
    "dotless_rate": 1.0,
    "altglyph_rate": 1.0,
    "tashkeel_style": "random",
    "case_rate": 1.0,
    "case_style": "suffix",
    "arabizi_rate": 1.0,
    "arabizi_style": "letter",
    "overlap_rate": 0.2,
    "zwc_rate": 1.0,
    "order_style": "reverse",
    "layout_style": "lines",
}
# Which words the word-level transforms may touch (text-level ones ignore it):
#   all      — every word (the default)
#   content  — content words: nouns, verbs, adjectives, names, numbers
#   function — the other words (control)
#   random   — as many words as "content" would pick, chosen at random (control)
TARGETS = ("all", "content", "function", "random")

CHOICES = {
    "dialect_style": DIALECT_STYLES,
    "dialect_level": DIALECT_LEVELS,
    "root_style": ROOT_STYLES,
    "huruf_style": HURUF_STYLES,
    "blank_style": tuple(BLANK_STYLES),
    "tashkeel_style": TASHKEEL_STYLES,
    "case_style": CASE_STYLES,
    "arabizi_style": ARABIZI_STYLES,
    "order_style": ORDER_STYLES,
    "layout_style": LAYOUT_STYLES,
}


def parse_modes(spec):
    """Turn "dotless,disconnect" (or an alias like "both", or method numbers
    like "10,3") into a mode list."""
    names = []
    for name in spec.split(","):
        name = BY_NUMBER.get(name.strip(), name.strip())
        names.extend(ALIASES.get(name, [name]))
    unknown = set(names) - set(MODES)
    if unknown:
        raise ValueError(f"unknown mode(s) {sorted(unknown)}; choose from {MODES}")
    return [m for m in MODES if m in names]


def obfuscate(text, mode="both", rate=1.0, seed=None, target="all", **options):
    """Obfuscate a random `rate` fraction of the Arabic words in `text`,
    limited to the `target` words (see TARGETS).

    `options` override DEFAULTS (per-transform settings such as dotless_rate).
    `rate` and `target` only apply to the word-level transforms.
    """
    if target not in TARGETS:
        raise ValueError(f"unknown target {target!r}; choose from {TARGETS}")
    modes = parse_modes(mode)
    unknown = set(options) - set(DEFAULTS)
    if unknown:
        raise TypeError(f"unknown option(s) {sorted(unknown)}")
    opts = {**DEFAULTS, **options}
    rng = random.Random(seed)

    steps = {
        "conjunction": lambda w: conjunction_word(w, rng, opts["conjunction_rate"]),
        "gender": lambda w: gender_word(w, rng, opts["gender_rate"]),
        "number": lambda w: number_word(w, rng, opts["number_rate"]),
        "root": lambda w: root_word(w, rng, opts["root_rate"], opts["root_style"]),
        "pattern": lambda w: pattern_word(w, rng, opts["pattern_rate"]),
        "huruf": lambda w: huruf_word(w, rng, opts["huruf_rate"], opts["huruf_style"]),
        "silent": lambda w: silent_word(w, rng, opts["silent_rate"]),
        "shuffle": lambda w: shuffle_word(w, rng),
        "blank": lambda w: blank_word(w, rng, opts["blank_rate"], opts["blank_style"]),
        "space": lambda w: space_word(w, rng, opts["space_rate"]),
        "kashida": lambda w: kashida_word(w, rng, opts["kashida_rate"]),
        "disconnect": lambda w: disconnect_word(w, rng, opts["disconnect_rate"]),
        "dotless": lambda w: dotless_word(w, rng, opts["dotless_rate"]),
        "homoglyph": homoglyph_word,
        "altglyph": lambda w: altglyph_word(w, rng, opts["altglyph_rate"]),
        "tashkeel": lambda w: tashkeel_word(w, rng, opts["tashkeel_style"]),
        "case": lambda w: case_word(w, rng, opts["case_rate"], opts["case_style"]),
        "arabizi": lambda w: arabizi_word(w, rng, opts["arabizi_rate"], opts["arabizi_style"]),
        "presentation": lambda w: to_presentation(w) or w,
        "overlap": lambda w: overlap_word(w, rng, opts["overlap_rate"]),
        "zwc": lambda w: zwc_word(w, rng, opts["zwc_rate"]),
    }
    word_modes = [m for m in modes if m in steps]

    if "dialect" in modes:
        text = dialect_text(text, rng, WORD_RE, opts["dialect_rate"], opts["dialect_style"], opts["dialect_level"])

    selected = select_targets(text, target, seed) if word_modes else None
    position = iter(range(10**9))

    def repl(match):
        word = match.group()
        if selected is not None and next(position) not in selected:
            return word
        if rng.random() >= rate:
            return word
        for m in word_modes:
            word = steps[m](word)
        return word

    if word_modes:
        text = WORD_RE.sub(repl, text)
    if "order" in modes:
        text = order_text(text, rng, opts["order_style"])
    if "layout" in modes:
        text = layout_text(text, rng, opts["layout_style"])
    return text


def select_targets(text, target, seed):
    """Indices (in WORD_RE order) of the words `target` allows, or None for all."""
    if target == "all":
        return None
    from .morphology import content_word

    words = [m.group() for m in WORD_RE.finditer(text)]
    content = {i for i, w in enumerate(words) if content_word(w)}
    if target == "content":
        return content
    if target == "function":
        return set(range(len(words))) - content
    # random: same number of words as "content", chosen independently of the
    # transforms' own randomness
    return set(random.Random(f"{seed}-target").sample(range(len(words)), len(content)))


def strip_marks(text):
    return "".join(ch for ch in text if not is_mark(ch))


INVISIBLE = {ZWNJ, TATWEEL, ZWSP, WORD_JOINER, ZWJ, CGJ}


def normalize(text, remove_marks=False):
    """Undo the lossless transforms (used to check the meaning survived intact)."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ch not in INVISIBLE)
    if remove_marks:
        text = strip_marks(text)

    def repl(match):
        word = match.group().replace(KEHEH, KAF)
        forms = positional_forms(word)
        return "".join(
            (ALEF_MAQSURA if f in (FINA, ISOL) else YEH) if ch == FARSI_YEH else ch
            for ch, f in zip(word, forms)
        )

    return WORD_RE.sub(repl, text)
