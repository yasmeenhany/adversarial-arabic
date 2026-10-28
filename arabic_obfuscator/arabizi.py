"""Arabizi / Franco: embed Latin letters and digits in the Arabic text.

Two styles:
  letter — (default) keep the text Arabic but swap single letters for the
           digits Arabizi writes them with (ء أ إ ؤ ئ→2, ع→3, خ→5, ح→7, ق→8),
           e.g. العقل → ال38ل; `rate` is the fraction of those letters swapped
  word   — transliterate whole words, e.g. العقل → el3a8l (vowels come from the
           tashkeel, so this reads best on vowelled text); `rate` is the
           fraction of words
"""

from .shaping import base, clusters

FATHA, DAMMA, KASRA = "َ", "ُ", "ِ"
KEHEH, FARSI_YEH = "ک", "ی"  # left by the homoglyph / altglyph modes
FATHATAN, DAMMATAN, KASRATAN = "ً", "ٌ", "ٍ"
SHADDA, SUKUN = "ّ", "ْ"
ALEF, LAM, WAW, YEH, TEH_MARBUTA, ALEF_MAQSURA = (
    "ا",
    "ل",
    "و",
    "ي",
    "ة",
    "ى",
)

DIGITS = {
    "ء": "2",  # ء
    "أ": "2",  # أ
    "إ": "2",  # إ
    "ؤ": "2",  # ؤ
    "ئ": "2",  # ئ
    "ع": "3",  # ع
    "خ": "5",  # خ
    "ح": "7",  # ح
    "ق": "8",  # ق
}
CONSONANTS = {
    **DIGITS,
    "آ": "2a",  # آ
    "ب": "b",
    "ت": "t",
    "ث": "th",
    "ج": "g",
    "د": "d",
    "ذ": "z",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "s",
    "ض": "d",
    "ط": "t",
    "ظ": "z",
    "غ": "gh",
    "ف": "f",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    WAW: "w",
    YEH: "y",
}
VOWELS = {FATHA: "a", DAMMA: "o", KASRA: "e", FATHATAN: "an", DAMMATAN: "on", KASRATAN: "en"}

STYLES = ("letter", "word")


def _transliterate(word):
    """Write a (preferably vowelled) word the way Arabizi writers would: with
    the spoken pronunciation, so the article assimilates to sun letters
    (التَّفْكِير → ettafkeer) and the case endings are dropped."""
    cs = clusters(word)
    last = len(cs) - 1
    # Index of the definite article's alef: at the start, or after و/ف/ب.
    article = next(
        (k for k in (0, 1) if k + 2 <= last and base(cs[k]) == ALEF and base(cs[k + 1]) == LAM), None
    )
    sun = article is not None and SHADDA in cs[article + 2]
    out = []
    for k, c in enumerate(cs):
        letter, marks = base(c), c[1:]
        if letter == KEHEH:
            letter = "ك"
        elif letter == FARSI_YEH:
            letter = ALEF_MAQSURA if k == last else YEH
        # The vowel on the last letter is the case ending, which speech drops.
        vowel = "" if k == last else "".join(VOWELS.get(m, "") for m in marks)
        prev = "".join(out)
        if k == article:
            out.append(("e" if sun else "el") if k == 0 else "")  # after و/ف/ب: "wal...", "wat-t..."
        elif article is not None and k == article + 1:
            out.append("" if sun or article == 0 else "l")  # the article's lam
        elif letter in (ALEF, ALEF_MAQSURA):
            # silent after a vowel "a" and after tanween fath (حَكَمًا → 7akaman)
            out.append("" if prev.endswith("a") or FATHATAN in cs[k - 1] else "a")
        elif letter == TEH_MARBUTA:
            out.append("" if prev.endswith("a") else "a")
        elif letter == YEH and k == last and SHADDA in marks:  # nisba ـيّ: البشريّ → elbashari
            out[-1] = out[-1].rstrip("e") if out else ""
            out.append("i")
        elif letter in (WAW, YEH) and k > 0 and not vowel and SHADDA not in marks and SUKUN not in marks:
            long_vowel = "o" if letter == WAW else ("e" if prev.endswith("e") else "i")
            out.append("" if prev.endswith(long_vowel * 2) else long_vowel)
        elif letter in CONSONANTS:
            sound = CONSONANTS[letter]
            out.append(sound * (2 if SHADDA in marks else 1) + vowel)
    return "".join(out)


def arabizi_word(word, rng, rate=1.0, style="letter"):
    """letter: swap each digit-written letter with probability `rate`.
    word: with probability `rate`, rewrite the whole word in Arabizi."""
    if style == "word":
        return _transliterate(word) if rng.random() < rate else word
    # Marks are dropped from swapped letters: on a digit they would render as
    # a dotted circle.
    return "".join(
        DIGITS[base(c)] if base(c) in DIGITS and rng.random() < rate else c for c in clusters(word)
    )
