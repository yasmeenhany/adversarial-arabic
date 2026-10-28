"""Arabic joining analysis and presentation-form lookup tables.

Presentation forms (U+FB50–U+FDFF, U+FE70–U+FEFF) are fixed glyphs: a renderer
will not join them contextually with their neighbours. To stay legible, a word
must therefore be converted as a whole, with each letter mapped to the
positional form (isolated / initial / medial / final) it would take naturally.
"""

import re
import unicodedata

ISOL, INIT, MEDI, FINA = "isol", "init", "medi", "fina"

_TAGS = {"<isolated>": ISOL, "<initial>": INIT, "<medial>": MEDI, "<final>": FINA}
# FE70 block first so standard letters prefer it over the FB50 block.
_RANGES = [(0xFE70, 0xFEFF), (0xFB50, 0xFDFF)]

LAM = "\u0644"
# Non-letters that transforms may leave inside a word (zero-width non-joiner,
# tatweel, an injected space, a blanked letter). They need no presentation
# form of their own.
PASSTHROUGH = {"\u200C", "\u0640", " ", "_", "-"}

ALEFS = {"\u0627", "\u0622", "\u0623", "\u0625"}  # ا آ أ إ

# A "word" is a run of Arabic letters and combining marks. Punctuation such as
# ، ؟ ؛ is excluded because it is non-joining and has no presentation form.
WORD_RE = re.compile("[\u0621-\u065F\u0670-\u06D3\u06D5]+")


def _build_tables():
    forms = {}  # base letter -> {form: presentation char}
    lam_alef = {}  # (lam, alef) -> {form: presentation char}
    for start, end in _RANGES:
        for cp in range(start, end + 1):
            ch = chr(cp)
            decomp = unicodedata.decomposition(ch).split()
            if len(decomp) < 2 or decomp[0] not in _TAGS:
                continue
            form = _TAGS[decomp[0]]
            base = "".join(chr(int(h, 16)) for h in decomp[1:])
            if len(base) == 1:
                forms.setdefault(base, {}).setdefault(form, ch)
            elif len(base) == 2 and base[0] == LAM and base[1] in ALEFS:
                lam_alef.setdefault(base, {}).setdefault(form, ch)
    return forms, lam_alef


FORMS, LAM_ALEF = _build_tables()


def is_mark(ch):
    return unicodedata.category(ch) == "Mn"


def clusters(word):
    """Split a word into letters, each with its attached marks (vowels, shadda)."""
    out = []
    for ch in word:
        if out and is_mark(ch):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def base(cluster):
    """The letter of a cluster, without its marks."""
    return cluster[0]


def strip_marks(text):
    return "".join(ch for ch in text if not is_mark(ch))


def joins_next(ch):
    """Dual-joining letters connect to the following letter."""
    return ch == "\u0640" or INIT in FORMS.get(ch, {})


def joins_prev(ch):
    return ch == "\u0640" or FINA in FORMS.get(ch, {})


def positional_forms(word):
    """Return the contextual form of each character in `word` (None for marks)."""
    forms = [None] * len(word)
    letters = [i for i, ch in enumerate(word) if not is_mark(ch)]
    for k, i in enumerate(letters):
        ch = word[i]
        prev = word[letters[k - 1]] if k > 0 else None
        nxt = word[letters[k + 1]] if k + 1 < len(letters) else None
        p = prev is not None and joins_next(prev) and joins_prev(ch)
        n = nxt is not None and joins_next(ch) and joins_prev(nxt)
        forms[i] = MEDI if p and n else FINA if p else INIT if n else ISOL
    return forms


def to_presentation(word):
    """Convert a whole word to presentation forms, or return None if any
    character has no suitable form (the word is then left untouched)."""
    forms = positional_forms(word)
    out = []
    i = 0
    while i < len(word):
        ch = word[i]
        if is_mark(ch) or ch in PASSTHROUGH:
            out.append(ch)
            i += 1
            continue
        if ch == LAM:
            # Look past any marks on the lam for a following alef.
            j = i + 1
            while j < len(word) and is_mark(word[j]):
                j += 1
            pair = ch + word[j] if j < len(word) else ""
            if pair in LAM_ALEF:
                # The lam-alef ligature only ever joins to the right.
                form = FINA if forms[i] in (MEDI, FINA) else ISOL
                glyph = LAM_ALEF[pair].get(form)
                if glyph is None:
                    return None
                out.append(glyph + word[i + 1 : j])  # ligature, then lam's marks
                i = j + 1
                continue
        glyph = FORMS.get(ch, {}).get(forms[i])
        if glyph is None:
            return None
        out.append(glyph)
        i += 1
    return "".join(out)
