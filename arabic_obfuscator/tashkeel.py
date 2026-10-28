"""Diacritic flooding: add tashkeel to every letter to fragment tokenization."""

from .shaping import PASSTHROUGH, base, clusters, is_mark

FATHA, DAMMA, KASRA = "\u064E", "\u064F", "\u0650"
FATHATAN, DAMMATAN, KASRATAN = "\u064B", "\u064C", "\u064D"
SUKUN, SHADDA = "\u0652", "\u0651"

HARAKAT = [FATHA, DAMMA, KASRA]
TANWEEN = [FATHATAN, DAMMATAN, KASRATAN]
ALL_MARKS = HARAKAT + TANWEEN + [SUKUN, SHADDA]

# Long-vowel alefs never carry a haraka in normal writing.
NO_MARK = {"\u0627", "\u0622", "\u0649"}  # ا آ ى

STYLES = ("random", "stacked")


def _random_marks(k, n, rng):
    """Plausible-looking (but not grammatical) vowelling for letter k of n."""
    if k == 0:  # words never start with sukun or shadda
        return rng.choice(HARAKAT)
    if k == n - 1:  # tanween only at the end of a word
        return rng.choice(HARAKAT + TANWEEN)
    mark = rng.choice(HARAKAT + [SUKUN])
    if mark != SUKUN and rng.random() < 0.1:
        mark = SHADDA + mark
    return mark


def _stacked_marks(rng):
    return "".join(rng.sample(ALL_MARKS, rng.randint(2, 3)))


def tashkeel_word(word, rng, style="random"):
    chars = [ch for ch in word if not is_mark(ch)]  # drop any existing marks
    # ZWNJ and tatweel (from disconnect/kashida) are not letters: a mark on a
    # ZWNJ renders as a dotted circle.
    n = sum(ch not in PASSTHROUGH for ch in chars)
    out = []
    k = 0
    for ch in chars:
        out.append(ch)
        if ch in PASSTHROUGH:
            continue
        if ch not in NO_MARK:
            if style == "stacked":
                out.append(_stacked_marks(rng))
            else:
                out.append(_random_marks(k, n, rng))
        k += 1
    return "".join(out)


CASE_MARKS = HARAKAT + TANWEEN + [SUKUN]
CASE_STYLES = ("suffix", "stack")
TEH_MARBUTA, TEH, ALEF = "\u0629", "\u062A", "\u0627"
WEAK_ENDINGS = {"\u0627", "\u0649", "\u064A", "\u0648", "\u0622"}  # ا ى ي و آ
NOMINATIVE = {DAMMA, DAMMATAN}
OTHER_CASES = {FATHA, KASRA, FATHATAN, KASRATAN}


def case_word(word, rng, rate=1.0, style="suffix"):
    """Ambiguous case endings, invented by combining existing ones.

    suffix — give a noun the plural case suffix of the other case:
             nominative → ـين, accusative/genitive → ـون (العَقْلُ → العَقْلِينَ,
             المَنْطِقِ → المَنْطِقُونَ, الأُمُورَ → الأُمُورُونَ); ة becomes ت
             (المَعْرِفَتُونَ). Plurals and duals that already end in ـون/ـين/ـان
             get the other case's ending instead (المُسْلِمِينَ → المُسْلِمُونَ).
    stack  — give the word's last vowelled letter two clashing case marks
             (e.g. damma + kasra)
    """
    if style == "stack":
        return _stack(word, rng, rate)
    number = _noun_number(word)
    if not number or rng.random() >= rate:
        return word
    cs = clusters(word)
    plain = "".join(base(c) for c in cs)
    if number in ("p", "d") and plain.endswith(("ون", "ين", "ان")) and len(cs) > 3:
        # ـونَ ↔ ـينَ, ـانِ → ـينِ: keep the stem, swap the case ending.
        vowelled = any(is_mark(ch) for ch in word)
        stem = cs[:-2]
        nominative = plain.endswith(("ون", "ان"))
        new = "ين" if nominative else "ون"
        if vowelled:
            stem[-1] = base(stem[-1]) + (SHADDA if SHADDA in stem[-1] else "") + (KASRA if new == "ين" else DAMMA)
        return "".join(stem) + new + (cs[-1][1:] if vowelled else "")
    if len(cs) > 2 and base(cs[-1]) == ALEF and FATHATAN in cs[-2]:  # حَكَمًا → حَكَم-
        cs = cs[:-1]
    last = cs[-1]
    if base(last) in WEAK_ENDINGS or base(last) in PASSTHROUGH:
        return word
    marks = set(last[1:])
    if marks & NOMINATIVE:
        suffix = "ين"
    elif marks & OTHER_CASES:
        suffix = "ون"
    else:  # case not written: pick one
        suffix = rng.choice(["ين", "ون"])
    vowelled = any(is_mark(ch) for ch in word)
    letter = TEH if base(last) == TEH_MARBUTA else base(last)
    if vowelled:
        letter += (SHADDA if SHADDA in last else "") + (KASRA if suffix == "ين" else DAMMA)
    return "".join(cs[:-1]) + letter + suffix + (FATHA if vowelled else "")


def _noun_number(word):
    """"s"/"d"/"p" for a common noun (per the analyser), else False. Without
    camel-tools, any word with the definite article (after an optional
    و/ف/ب/ل/ك clitic) counts as a singular noun."""
    from .morphology import noun_number

    try:
        found = noun_number(word)
    except RuntimeError:
        found = None
    if found is not None:
        return found
    plain = "".join(ch for ch in word if not is_mark(ch))
    return "s" if len(plain) >= 4 and plain.lstrip("وفبلك").startswith("ال") else False


def _stack(word, rng, rate):
    """Give the word's last voweled letter two clashing case marks (e.g.
    damma + kasra), an ending that does not exist in Arabic. Marks elsewhere
    in the word are kept."""
    if rng.random() >= rate:
        return word
    cs = clusters(word)
    k = len(cs) - 1
    if base(cs[k]) in NO_MARK and k > 0:  # e.g. the alef after tanween fath: أمينًا
        k -= 1
    if base(cs[k]) in NO_MARK or base(cs[k]) in PASSTHROUGH:
        return word
    shadda = SHADDA if SHADDA in cs[k] else ""
    cs[k] = base(cs[k]) + shadda + "".join(rng.sample(CASE_MARKS, 2))
    return "".join(cs)
