"""Language-level obfuscation: dialect words, swapped conjunctions, and broken
gender / number agreement.

These are rule-based heuristics, not a morphological analyser: they only touch
words whose shape makes their role clear (function words from a lexicon,
imperfect verbs starting with ي, nisba adjectives ending in ـيّ / ـيّة). They
work on plain or vowelled text; vowels are kept where the rule allows it.
"""

import re
import sys

from .shaping import base, clusters, is_mark, strip_marks

FATHA, DAMMA, KASRA = "َ", "ُ", "ِ"
SUKUN, SHADDA = "ْ", "ّ"
ALEF, TEH, WAW, YEH, TEH_MARBUTA = "ا", "ت", "و", "ي", "ة"
NOON = "ن"
CLITICS = "وف"  # و ف


def norm(text):
    """Spelling-insensitive key: no marks, bare alef, ى→ي, ة→ه."""
    text = strip_marks(text)
    for src, dst in (("أ", ALEF), ("إ", ALEF), ("آ", ALEF), ("ى", YEH)):
        text = text.replace(src, dst)
    return text.replace(TEH_MARBUTA, "ه")


def _table(pairs):
    return {norm(k): v for k, v in pairs.items()}


def _vowelled(word):
    return any(is_mark(ch) for ch in word)


def split_clitic(word, table):
    """Find `word` in `table`, allowing a leading و/ف clitic.
    Returns (clitic, core) or None."""
    if norm(word) in table:
        return "", word
    cs = clusters(word)
    if len(cs) > 2 and base(cs[0]) in CLITICS and norm("".join(cs[1:])) in table:
        return cs[0], "".join(cs[1:])
    return None


def _lexical(word, rng, table, rate):
    found = split_clitic(word, table)
    if not found or rng.random() >= rate:
        return word
    clitic, core = found
    choice = table[norm(core)]
    return clitic + (rng.choice(choice) if isinstance(choice, list) else choice)


# --- 15. Dialect substitution (MSA → Egyptian, Levantine, Gulf, Maghrebi) ---

DIALECTS = ("egy", "lev", "gulf", "mag")
DIALECT_STYLES = ("mix",) + DIALECTS  # mix: a random dialect for each word

# MSA word → (Egyptian, Levantine, Gulf, Maghrebi). None: no common
# dialect form, so the word stays MSA in that dialect.
_DIALECT_WORDS = {
    "الذي": ("اللي", "اللي", "اللي", "اللي"),
    "التي": ("اللي", "اللي", "اللي", "اللي"),
    "الذين": ("اللي", "اللي", "اللي", "اللي"),
    "اللاتي": ("اللي", "اللي", "اللي", "اللي"),
    "اللواتي": ("اللي", "اللي", "اللي", "اللي"),
    "هذا": ("ده", "هاد", "هذا", "هادا"),
    "هذه": ("دي", "هاي", "هذي", "هادي"),
    "هؤلاء": ("دول", "هدول", "هذولا", "هادو"),
    "ذلك": ("ده", "هداك", "ذاك", "داك"),
    "تلك": ("دي", "هديك", "ذيك", "ديك"),
    "ماذا": ("إيه", "شو", "شنو", "أش"),
    "لماذا": ("ليه", "ليش", "ليش", "علاش"),
    "كيف": ("إزاي", "كيف", "شلون", "كيفاش"),
    "أين": ("فين", "وين", "وين", "فين"),
    "متى": ("إمتى", "إيمتى", "متى", "فوقاش"),
    "الآن": ("دلوقتي", "هلق", "الحين", "دابا"),
    "ليس": ("مش", "مش", "مو", "ماشي"),
    "ليست": ("مش", "مش", "مو", "ماشي"),
    "لست": ("مش", "مش", "مو", "ماشي"),
    "لم": ("ما", "ما", "ما", "ما"),
    "جدا": ("قوي", "كتير", "وايد", "بزاف"),
    "فقط": ("بس", "بس", "بس", "غير"),
    "أيضا": ("كمان", "كمان", "بعد", "حتى"),
    "لكن": ("بس", "بس", "بس", "ولكن"),
    "نعم": ("أيوه", "إيه", "إي", "إيه"),
    "هناك": ("فيه", "في", "فيه", "كاين"),
    "عندما": ("لما", "لما", "لما", "ملي"),
    "مثل": ("زي", "متل", "مثل", "بحال"),
    "كثيرا": ("كتير", "كتير", "وايد", "بزاف"),
    "قليلا": ("شوية", "شوي", "شوي", "شوية"),
    "شيء": ("حاجة", "شي", "شي", "حاجة"),
    "إذن": ("يبقى", "يعني", "عيل", None),
    "حسنا": ("ماشي", "ماشي", "زين", "واخا"),
    "يغدو": ("يبقى", "بيصير", "يصير", "كيولي"),
    "يصبح": ("يبقى", "بيصير", "يصير", "كيولي"),
    "أصبح": ("بقى", "صار", "صار", "ولى"),
    "يريد": ("عايز", "بدو", "يبي", "بغا"),
    "يرى": ("يشوف", "بيشوف", "يشوف", "كيشوف"),
    "يذهب": ("يروح", "بيروح", "يروح", "كيمشي"),
    "ذهب": ("راح", "راح", "راح", "مشا"),
    "يعطي": ("يدي", "بيعطي", "يعطي", "كيعطي"),
    "المرء": ("الواحد", "الواحد", "الواحد", "الواحد"),
    "الإنسان": ("البني آدم", "البني آدم", "الإنسان", "بنادم"),
    "أمام": ("قدام", "قدام", "جدام", "قدام"),
    "خلف": ("ورا", "ورا", "ورا", "ور"),
    "داخل": ("جوه", "جوا", "داخل", "داخل"),
    "خارج": ("بره", "برا", "برا", "برا"),
    "جميل": ("حلو", "حلو", "حلو", "زوين"),
}
DIALECT_LEVELS = ("basic", "full")

# Level "full" also swaps everyday content words for their dialect ones.
_DIALECT_CONTENT = {
    "الخطأ": ("الغلط", "الغلط", "الغلط", "الغلط"),
    "خطأ": ("غلط", "غلط", "غلط", "غلط"),
    "الصواب": ("الصح", "الصح", "الصح", "الصح"),
    "الأمور": ("الحاجات", "الأشيا", "الأمور", "الحوايج"),
    "الكون": ("الدنيا", "الدنيا", "الدنيا", "الدنيا"),
    "سبيل": ("سكة", "طريق", "طريق", "طريق"),
    "طريق": ("سكة", "طريق", "طريق", "طريق"),
    "الآخرين": ("الناس التانيين", "الناس التانيين", "الباقين", "الناس لخرين"),
    "غيره": ("حد تاني", "حدا تاني", "أحد ثاني", "شي واحد آخر"),
    "يرتكبها": ("بيعملها", "بيعملها", "يسويها", "كيديرها"),
    "يتلقاها": ("بياخدها", "بياخدها", "ياخذها", "كياخدها"),
    "يميز": ("بيفرق", "بيفرق", "يفرق", "كيفرق"),
    "يفقد": ("بيخسر", "بيخسر", "يخسر", "كيخسر"),
    "تطلب": ("عايزة", "بدها", "تبي", "بغات"),
    "عاجزا": ("مش قادر", "مش قادر", "ما يقدر", "ما قادرش"),
    "عاجز": ("مش قادر", "مش قادر", "ما يقدر", "ما قادرش"),
    "النظر": ("البص", "الشوف", "الشوف", "الشوف"),
    "الحياة": ("العيشة", "الحياة", "الحياة", "الحياة"),
    "كثير": ("كتير", "كتير", "وايد", "بزاف"),
    "كثيرة": ("كتيرة", "كتيرة", "وايد", "بزاف"),
    "دائما": ("على طول", "دايما", "دوم", "ديما"),
    "هنا": ("هنا", "هون", "هني", "هنا"),
    "هكذا": ("كده", "هيك", "جذي", "هكا"),
    "يستطيع": ("يقدر", "بيقدر", "يقدر", "يقدر"),
    "يعرف": ("بيعرف", "بيعرف", "يعرف", "كيعرف"),
    "يقول": ("بيقول", "بيقول", "يقول", "كيقول"),
    "يفعل": ("بيعمل", "بيعمل", "يسوي", "كيدير"),
    "فعل": ("عمل", "عمل", "سوى", "دار"),
    "يجب": ("لازم", "لازم", "لازم", "خاصو"),
    "يمكن": ("ممكن", "ممكن", "يمكن", "يمكن"),
    "سيئ": ("وحش", "عاطل", "شين", "خايب"),
    "جيد": ("كويس", "منيح", "زين", "مزيان"),
    "صغير": ("صغير", "زغير", "صغير", "صغير"),
    "رجل": ("راجل", "زلمة", "رجال", "راجل"),
    "امرأة": ("ست", "مرة", "حرمة", "مرا"),
    "الأطفال": ("العيال", "الولاد", "اليهال", "الدراري"),
    "ماء": ("مية", "مي", "ماي", "ما"),
}
DIALECT = _table({k: v[0] for k, v in _DIALECT_WORDS.items()})  # Egyptian (also a stoplist elsewhere)
_DIALECT_TABLE = _table(_DIALECT_WORDS)
_DIALECT_FULL_TABLE = _table({**_DIALECT_WORDS, **_DIALECT_CONTENT})

# Present-tense marker on an indicative verb (يميز → بيميز / كيميز); Gulf
# speech has none, so Gulf leaves the verb alone.
_PRESENT = {"egy": "ب", "lev": "ب", "gulf": "", "mag": "ك"}
# Purpose لِـ before a verb (لِيَكُونَ → عشان يكون).
_PURPOSE = {"egy": "عشان", "lev": "مشان", "gulf": "عشان", "mag": "باش"}
# "قبل أن" / "بعد أن" → "قبل ما"; Gulf says "قبل لا".
_AN_WORD = {"egy": "ما", "lev": "ما", "gulf": "لا", "mag": "ما"}
_PRONOUN_SUFFIXES = ("ها", "هم", "هما", "هن", "ه", "ك", "كم", "ني", "نا")
# Level "full": past passive فُعِلَ → اتفعل; "لا + noun" → "there is no".
_PASSIVE = {"egy": "ات", "lev": "ات", "gulf": "ان", "mag": "ت"}
_THERE_IS_NO = {"egy": "مفيش", "lev": "ما في", "gulf": "ما فيه", "mag": "ما كاين"}
_HIS_O = {"lev", "mag"}  # write the suffix "his" ـه as ـو (عقله → عقلو)


def _pick(rng, style):
    return rng.choice(DIALECTS) if style == "mix" else style


def _verb(word):
    """("present" | "purpose", clitic, verb) if `word` is an imperfect verb
    that takes a dialect marker, else None. In vowelled text an indicative
    verb ends in damma (or a pronoun suffix) and a purpose verb is لِـ + a
    verb ending in fatha; unvowelled text only counts يـ verbs."""
    cs = clusters(word)
    vowelled = _vowelled(word)
    i = 1 if len(cs) > 3 and base(cs[0]) in CLITICS + "ل" else 0
    rest = cs[i:]
    if len(rest) < 3 or base(rest[0]) not in (YEH, TEH) or (not vowelled and base(rest[0]) != YEH):
        return None
    if vowelled and not (set(rest[0][1:]) & {FATHA, DAMMA}):
        return None
    end = rest[-1][1:]
    plain = norm(word)
    if i and base(cs[0]) == "ل":
        if vowelled and FATHA not in end:
            return None
        return "purpose", "", "".join(rest)
    if vowelled and DAMMA not in end and not plain.endswith(_PRONOUN_SUFFIXES):
        return None
    return "present", "".join(cs[:i]), "".join(rest)


def _passive(word):
    """True for a vowelled past passive verb: خُلِقَ, كُرِّمَ."""
    cs = clusters(word)
    return (
        len(cs) == 3
        and DAMMA in cs[0]
        and KASRA in cs[1]
        and FATHA in cs[2]
        and not any(base(c) in (ALEF, WAW, YEH, "ى") for c in cs)
    )


def _his(word):
    """True for a vowelled word ending in the suffix "his" (عَقْلَهُ, نَفْسِهِ).
    Words with the article cannot take it, which rules out الفِقْهِ."""
    cs = clusters(word)
    return (
        len(cs) >= 4
        and base(cs[-1]) == "ه"
        and set(cs[-1][1:]) & {DAMMA, KASRA}
        and _vowelled(cs[-2])
        and not norm(word).lstrip("وفبل").startswith("ال")
    )


def dialect_word(word, rng, rate=1.0, style="mix", level="basic"):
    """MSA → dialect for one word: a dialect word from the table, or a dialect
    marker on a verb; level "full" also uses everyday content words and
    rewrites past passives and the suffix "his". Dialect forms are written
    without diacritics."""
    table = _DIALECT_FULL_TABLE if level == "full" else _DIALECT_TABLE
    found = split_clitic(word, table)
    if found:
        if rng.random() >= rate:
            return word
        clitic, core = found
        dialect = _pick(rng, style)
        new = table[norm(core)][DIALECTS.index(dialect)]
        return strip_marks(clitic) + new if new else word
    if level == "full" and (_passive(word) or _his(word)):
        if rng.random() >= rate:
            return word
        dialect = _pick(rng, style)
        if _passive(word):
            return _PASSIVE[dialect] + strip_marks(word)
        return strip_marks(word)[:-1] + "و" if dialect in _HIS_O else word
    verb = _verb(word)
    if not verb or rng.random() >= rate:
        return word
    kind, clitic, core = verb
    dialect = _pick(rng, style)
    if kind == "purpose":
        return _PURPOSE[dialect] + " " + strip_marks(core)
    if not _PRESENT[dialect]:
        return word
    return strip_marks(clitic) + _PRESENT[dialect] + strip_marks(core)


_MARKS = "[ً-ْ]*"


def _marked(word):
    """Regex for `word` with any vowel marks after each letter."""
    return "".join(re.escape(ch) + _MARKS for ch in word)


_BEFORE_AFTER = _marked("قبل") + "|" + _marked("بعد")
_AN = _marked("أن") + "|" + _marked("ان")
_AN_AFTER = re.compile("((?:" + _BEFORE_AFTER + ")\\s+)(?:" + _AN + ")(?=\\s)")


# "لا رُخْصَةَ" (no exemption): لا before a noun in the accusative (fatha).
_LA_NOUN = re.compile("(?<!\\S)(" + _marked("و") + ")?" + _marked("لا") + "(\\s+)(\\S*?َ)(?=[\\s،.؛]|$)")


def dialect_text(text, rng, word_re, rate=1.0, style="mix", level="basic"):
    """Rewrite MSA words and phrases in dialect: one dialect throughout, or
    (style "mix") a random one for each word, so the text switches between
    MSA and several dialects."""

    def an(m):
        if rng.random() >= rate:
            return m.group(0)
        return strip_marks(m.group(1)) + _AN_WORD[_pick(rng, style)]

    def there_is_no(m):
        if rng.random() >= rate:
            return m.group(0)
        clitic = strip_marks(m.group(1) or "")
        return clitic + _THERE_IS_NO[_pick(rng, style)] + m.group(2) + strip_marks(m.group(3))

    text = _AN_AFTER.sub(an, text)
    if level == "full":
        text = _LA_NOUN.sub(there_is_no, text)
    return word_re.sub(lambda m: dialect_word(m.group(), rng, rate, style, level), text)


# --- 16. Switching conjunctions ---------------------------------------------

CONJUNCTIONS = ["ثم", "أو", "أم", "بل", "لكن", "حتى"]
_CONJ = _table({c: [o for o in CONJUNCTIONS if o != c] for c in CONJUNCTIONS})
# Subordinating conjunctions, swapped among themselves: قبل أن → قبل لو.
SUBORDINATORS = ["أن", "إن", "لأن", "كي", "لكي", "إذا", "لو"]
_SUBORD = _table({c: [o for o in SUBORDINATORS if norm(o) != norm(c)] for c in SUBORDINATORS})
# What an attached و / ف can become: the other one, or a standalone conjunction.
_FOR_ATTACHED = {"و": ["ف", "ثم", "أو", "بل", "لكن"], "ف": ["و", "ثم", "أو", "بل", "لكن"]}
FUNCTION_WORDS = {norm(w) for w in ["لا", "لم", "لن", "ما", "من", "في", "على", "عن", "إن", "أن", "قد", "هو", "هي", "كل"]}


def _preposition_fi(cs):
    """True for في + pronoun (فيه، فيها، فيهم), whose ف is not a clitic."""
    return norm("".join(cs)).startswith("فيه")


def _attached_conjunction(cs):
    """True if the leading و/ف is a conjunction rather than part of the root."""
    if len(cs) < 3 or base(cs[0]) not in CLITICS or _preposition_fi(cs):
        return False
    rest = norm("".join(cs[1:]))
    if rest.startswith("ال") or rest in FUNCTION_WORDS or (rest[0] == YEH and len(rest) >= 3):
        return True
    # Otherwise ask the analyser, which tells وَشَجَاعَةً (و + noun) from
    # فَرِيضَةٌ (ف is a root letter); without camel-tools, no.
    return bool(_morph_conjunction("".join(cs)))


def _morph_conjunction(word):
    from .morphology import has_conjunction

    try:
        return has_conjunction(word)
    except RuntimeError:
        return None


def conjunction_word(word, rng, rate=1.0):
    """Switch conjunctions: standalone ones (ثم، أو، بل…) for one another,
    subordinating ones (أن، لأن، إذا…) for one another, and an attached و/ف
    for the other one or a standalone conjunction (وَالعَقْلُ → ثم العقل)."""
    plain = norm(word)
    if plain in _CONJ:
        return _lexical(word, rng, _CONJ, rate)
    if plain in _SUBORD and SHADDA not in word:  # إنَّ / أنَّ are particles, not conjunctions
        return _lexical(word, rng, _SUBORD, rate)
    cs = clusters(word)
    if _attached_conjunction(cs) and rng.random() < rate:
        new = rng.choice(_FOR_ATTACHED[base(cs[0])])
        if new in CLITICS:
            return new + cs[0][1:] + "".join(cs[1:])  # keeps the fatha
        return new + " " + "".join(cs[1:])
    return word


# --- 4 & 5. Breaking gender and number agreement ----------------------------

GENDER = _table(
    {
        "هو": "هي",
        "هي": "هو",
        "هذا": "هذه",
        "هذه": "هذا",
        "ذلك": "تلك",
        "تلك": "ذلك",
        "الذي": "التي",
        "التي": "الذي",
        "الذين": "اللاتي",
        "هم": "هن",
        "هن": "هم",
    }
)
NUMBER = _table(
    {
        "هو": "هم",
        "هي": "هن",
        "هذا": "هؤلاء",
        "هذه": "هؤلاء",
        "ذلك": "أولئك",
        "تلك": "أولئك",
        "الذي": "الذين",
        "التي": "اللاتي",
    }
)
OBJECT_SUFFIXES = ["ها", "هم", "هما", "ه"]


def _imperfect(cs):
    """Index of the ي prefix if the word looks like an imperfect verb (with an
    optional و/ف/ل clitic), else None."""
    if _preposition_fi(cs):
        return None
    i = 1 if len(cs) > 3 and base(cs[0]) in CLITICS + "ل" else 0
    if len(cs) - i < 3 or base(cs[i]) != YEH:
        return None
    marks = cs[i][1:]
    if marks and FATHA not in marks and DAMMA not in marks:
        return None
    return i


def _nisba(cs):
    """'masc' for البشريّ-type adjectives, 'fem' for الحضاريّة, else None."""
    plain = norm("".join(cs))
    if len(cs) < 5 or not plain.startswith("ال"):
        return None
    if plain.endswith("يه") and base(cs[-1]) == TEH_MARBUTA and base(cs[-2]) == YEH:
        return "fem"
    if base(cs[-1]) == YEH and (SHADDA in cs[-1] or not _vowelled(cs[-1] + cs[-2])):
        return "masc"
    return None


def _case(cluster):
    """The case/mood marks on a cluster (everything except shadda and sukun)."""
    return "".join(m for m in cluster[1:] if m not in (SHADDA, SUKUN))


_warned = []


def _morph_flip(word, feat):
    """Gender ("gen") or number ("num") flip from the morphological generator,
    or None (also when camel-tools is not installed: then only the rules are
    used)."""
    from .morphology import gender_flip, number_flip

    try:
        return (gender_flip if feat == "gen" else number_flip)(word)
    except RuntimeError as e:
        if not _warned:
            print(f"warning: {e}; gender and number fall back to simple rules", file=sys.stderr)
            _warned.append(True)
        return None


def gender_word(word, rng, rate=0.7):
    """Break gender agreement: flip the gender of pronouns, demonstratives and
    relative pronouns (from a word list), and of verbs and adjectives (with the
    morphological generator, e.g. المُنْصِفِ → المُنْصِفَةِ, كُرِّمَ → كُرِّمَتْ).
    Nouns keep their gender, so the words agreeing with them no longer match.
    Words the generator cannot handle fall back to rules: imperfect verbs
    (ي→ت), feminine past verbs (ـَتْ dropped), nisba adjectives (ـيّ ↔ ـيّة)."""
    if split_clitic(word, GENDER):
        return _lexical(word, rng, GENDER, rate)
    if rng.random() >= rate:
        return word
    flipped = _morph_flip(word, "gen")
    if flipped:
        return flipped
    cs = clusters(word)
    v = _vowelled(word)
    i = _imperfect(cs)
    if i is not None:
        cs[i] = TEH + cs[i][1:]
        return "".join(cs)
    if v and len(cs) >= 3 and base(cs[-1]) == TEH and SUKUN in cs[-1]:
        return "".join(cs[:-1])  # قالَتْ → قالَ
    kind = _nisba(cs)
    if kind == "fem":  # الحضاريّةِ → الحضاريِّ
        return "".join(cs[:-2]) + YEH + (SHADDA + _case(cs[-1]) if v else "")
    if kind == "masc":  # البشريُّ → البشريّةُ
        return "".join(cs[:-1]) + YEH + (SHADDA + FATHA if v else "") + TEH_MARBUTA + (_case(cs[-1]) if v else "")
    return word


def number_word(word, rng, rate=0.7):
    """Break number agreement: make pronouns, demonstratives and relative
    pronouns plural (from a word list), and switch verbs and adjectives
    between singular and plural with the morphological generator (يُمَيِّزُ →
    يُمَيِّزُونَ). Nouns keep their number. Words the generator cannot handle
    fall back to rules: imperfect verbs and nisba adjectives made plural."""
    if split_clitic(word, NUMBER):
        return _lexical(word, rng, NUMBER, rate)
    if rng.random() >= rate:
        return word
    flipped = _morph_flip(word, "num")
    if flipped:
        return flipped
    cs = clusters(word)
    v = _vowelled(word)
    plural = WAW + NOON + (FATHA if v else "")  # ـونَ
    if _imperfect(cs) is not None:
        plain = norm(word)
        for suffix in OBJECT_SUFFIXES:  # يرتكبها → يرتكبونها
            if plain.endswith(suffix) and len(plain) - len(suffix) >= 3:
                n = len(suffix)
                stem = cs[:-n]
                stem[-1] = base(stem[-1]) + (DAMMA if v else "")
                return "".join(stem) + plural + "".join(cs[-n:])
        if base(cs[-1]) == WAW:  # يغدو → يغدون
            return word + NOON + (FATHA if v else "")
        if base(cs[-1]) in (ALEF, "ى"):
            return word
        cs[-1] = base(cs[-1]) + (SHADDA if SHADDA in cs[-1] else "") + (DAMMA if v else "")
        return "".join(cs) + plural
    kind = _nisba(cs)
    if kind == "masc":  # البشريُّ → البشريّونَ
        return "".join(cs[:-1]) + YEH + (SHADDA + DAMMA if v else "") + plural
    if kind == "fem":  # الحضاريّةِ → الحضاريّاتِ
        return "".join(cs[:-2]) + YEH + (SHADDA + FATHA if v else "") + ALEF + TEH + (_case(cs[-1]) if v else "")
    return word
