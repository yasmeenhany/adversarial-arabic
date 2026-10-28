"""Dotless (rasm) text: strip the i'jam dots so letters collapse onto shared
skeletons, e.g. ب ت ث ن ي all become ٮ in the middle of a word.

Unlike the other transforms this is lossy: the reader must recover each letter
from context, which is exactly what makes it hard for a model.
"""

from .shaping import FINA, INIT, ISOL, MEDI, positional_forms

DOTLESS_BEH = "\u066E"  # ٮ
DOTLESS_QAF = "\u066F"  # ٯ
DOTLESS_FEH = "\u06A1"  # ڡ
NOON_GHUNNA = "\u06BA"  # ں
ALEF_MAQSURA = "\u0649"  # ى

_BEH_LIKE = "\u0628\u062A\u062B"  # ب ت ث

# Replacements that look right in every position.
_ANY = {
    **{ch: DOTLESS_BEH for ch in _BEH_LIKE},
    "\u062C": "\u062D",  # ج → ح
    "\u062E": "\u062D",  # خ → ح
    "\u0630": "\u062F",  # ذ → د
    "\u0632": "\u0631",  # ز → ر
    "\u0634": "\u0633",  # ش → س
    "\u0636": "\u0635",  # ض → ص
    "\u0638": "\u0637",  # ظ → ط
    "\u063A": "\u0639",  # غ → ع
    "\u0641": DOTLESS_FEH,  # ف → ڡ
    "\u0629": "\u0647",  # ة → ه
}

# Letters whose dotless skeleton depends on position.
_JOINED = {  # initial / medial
    "\u0646": DOTLESS_BEH,  # ن
    "\u064A": DOTLESS_BEH,  # ي
    "\u06CC": DOTLESS_BEH,  # ی (from the homoglyph mode)
    "\u0642": DOTLESS_FEH,  # ق shares the feh skeleton when joined
}
_END = {  # final / isolated
    "\u0646": NOON_GHUNNA,
    "\u064A": ALEF_MAQSURA,
    "\u06CC": ALEF_MAQSURA,
    "\u0642": DOTLESS_QAF,
}

DOTTED = set(_ANY) | set(_JOINED)


def dotless_word(word, rng, rate=1.0):
    """Remove the dots from a random `rate` fraction of the dotted letters."""
    out = []
    for ch, form in zip(word, positional_forms(word)):
        if ch in DOTTED and rng.random() < rate:
            if ch in _ANY:
                ch = _ANY[ch]
            elif form in (INIT, MEDI):
                ch = _JOINED[ch]
            elif form in (FINA, ISOL):
                ch = _END[ch]
        out.append(ch)
    return "".join(out)
