"""Codepoint spoofing with Persian/Urdu homoglyphs, and alternative glyph
forms: regional letter variants that look different but read the same."""

from .shaping import FINA, INIT, ISOL, MEDI, positional_forms

KAF, KEHEH = "\u0643", "\u06A9"  # ك → ک
YEH, FARSI_YEH = "\u064A", "\u06CC"  # ي → ی
ALEF_MAQSURA = "\u0649"  # ى

# Substitutions are only made in positions where the glyphs look the same:
#   ک matches ك when initial/medial (final ك carries a mark ک lacks)
#   ی matches ي when initial/medial (final ی is dotless)
#   ی matches ى when final/isolated
HOMOGLYPHS = {
    (KAF, INIT): KEHEH,
    (KAF, MEDI): KEHEH,
    (YEH, INIT): FARSI_YEH,
    (YEH, MEDI): FARSI_YEH,
    (ALEF_MAQSURA, FINA): FARSI_YEH,
    (ALEF_MAQSURA, ISOL): FARSI_YEH,
}


def homoglyph_word(word):
    forms = positional_forms(word)
    return "".join(HOMOGLYPHS.get((ch, f), ch) for ch, f in zip(word, forms))


HEH, HEH_DOACHASHMEE = "\u0647", "\u06BE"  # ه → ھ
TEH_MARBUTA, TEH_MARBUTA_GOAL = "\u0629", "\u06C3"  # ة → ۃ
ALEF_HAMZA_ABOVE, ALEF_WAVY_HAMZA_ABOVE = "\u0623", "\u0672"  # أ → ٲ
ALEF_HAMZA_BELOW, ALEF_WAVY_HAMZA_BELOW = "\u0625", "\u0673"  # إ → ٳ

# Unlike HOMOGLYPHS, these change the visible shape: final ک has no inner
# mark, final ی has no dots (it looks like ى, as in Egyptian spelling), ھ is
# the knotted Urdu heh.
ALT_ANY = {
    HEH: HEH_DOACHASHMEE,
    TEH_MARBUTA: TEH_MARBUTA_GOAL,
    ALEF_HAMZA_ABOVE: ALEF_WAVY_HAMZA_ABOVE,
    ALEF_HAMZA_BELOW: ALEF_WAVY_HAMZA_BELOW,
}
ALT_END = {KAF: KEHEH, YEH: FARSI_YEH}  # final / isolated only


def altglyph_word(word, rng, rate=1.0):
    """Swap a random `rate` fraction of eligible letters for a variant glyph."""
    out = []
    for ch, f in zip(word, positional_forms(word)):
        alt = ALT_ANY.get(ch) or (ALT_END.get(ch) if f in (FINA, ISOL) else None)
        out.append(alt if alt and rng.random() < rate else ch)
    return "".join(out)
