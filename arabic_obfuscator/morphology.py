"""Root-and-pattern transforms backed by the CAMeL Tools morphological analyser
and its CALIMA-star MSA database:

  root    — swap the word's root, keeping its pattern, clitics and inflection:
            replace  a different root that has a real lexeme in the same
                     pattern, e.g. بِمِقْيَاسِ → بِمِعْيارِ
            permute  the same root letters reordered, kept only if that makes
                     a real stem, e.g. التَّفْكِيرَ → التَّكْفِيرَ
  pattern — keep the root, move it to another of its lexemes,
            e.g. التَّفْكِيرَ (تَفْعِيل) → التَّفَكُّرَ (تَفَعُّل)

Each word is analysed in context-free mode; when the text is vowelled, the
analysis whose diacritics agree with the word's is used. Every rewritten word
is run back through the analyser and kept only if it is a valid MSA word.

Needs Python 3.11+ and camel-tools (installed without its torch/transformers
dependencies, which only the neural models use):

    python3.12 -m venv .venv
    .venv/bin/pip install --no-deps camel-tools
    .venv/bin/pip install cachetools dill pyrsistent six future editdistance \\
        emoji regex tqdm requests muddler docopt tabulate
    .venv/bin/camel_data -i morphology-db-msa-r13
"""

import functools
import itertools
from difflib import SequenceMatcher

from .linguistic import _CONJ, DIALECT, FUNCTION_WORDS, GENDER, NUMBER, norm
from .shaping import base, clusters, is_mark, strip_marks

SHADDA = "ّ"
ALEF, ALEF_WASLA = "ا", "ٱ"
SUN = set("تثدذرزسشصضطظلن")
# Only content words: function words and proper nouns are left alone.
CONTENT_POS = {"noun", "adj", "verb", "adv", "noun_quant", "adj_comp"}
# The analyser tags some of these as nouns (بين، قبل), but swapping them reads
# as a different kind of attack.
STOPWORDS = (
    FUNCTION_WORDS
    | set(DIALECT)
    | set(_CONJ)
    | set(GENDER)
    | set(NUMBER)
    | {norm(w) for w in ["بين", "غير", "بعد", "قبل", "عند", "مع", "كان", "منذ", "لدى", "نحو", "حيث", "خلال", "عبر", "ضد", "كل"]}
)
ROOT_STYLES = ("replace", "permute")
MAX_TRIES = 25  # candidate rewrites to validate per word


@functools.lru_cache(maxsize=None)
def _camel():
    """Load the analyser and index the database stems (about 3 s, once)."""
    try:
        from camel_tools.morphology.analyzer import Analyzer
        from camel_tools.morphology.database import MorphologyDB
    except ImportError as e:
        raise RuntimeError(
            "the root and pattern modes need camel-tools (Python 3.11+); "
            "run with .venv/bin/python — see arabic_obfuscator/morphology.py"
        ) from e
    db = MorphologyDB.builtin_db("calima-msa-r13")
    by_pattern = {}  # (stem category, stem pattern) → [(stem, root)]
    by_root = {}  # root → [(stem, stem category, stem pattern, pos)]
    stems = {}  # (undiacritised stem, root) → {stem categories}
    for key, entries in db.stem_hash.items():
        for cat, f in entries:
            stem, root, pattern, pos = f.get("diac"), f.get("root"), f.get("pattern"), f.get("pos")
            if not (stem and root and pattern) or pos not in CONTENT_POS:
                continue
            by_pattern.setdefault((cat, pattern), []).append((stem, root))
            by_root.setdefault(root, []).append((stem, cat, pattern, pos))
            stems.setdefault((key, root), set()).add(cat)
    # A lexeme can be listed under several keys; keep each candidate once.
    by_pattern = {k: sorted(set(v)) for k, v in by_pattern.items()}
    by_root = {k: sorted(set(v)) for k, v in by_root.items()}
    return Analyzer(db), by_pattern, by_root, stems


def _vowels(cluster):
    return {m for m in cluster[1:] if m != SHADDA}


def _mismatch(word, diac):
    """How badly an analysis' diacritised form disagrees with `word`, or None
    if the letters themselves differ."""
    a, b = clusters(word), clusters(diac)
    if len(a) != len(b) or any(norm(base(x)) != norm(base(y)) for x, y in zip(a, b)):
        return None
    score = 0.0
    for x, y in zip(a, b):
        vx, vy = _vowels(x), _vowels(y)
        if vx and vy and vx != vy:
            score += 1
        elif vx and not vy:
            score += 0.5  # e.g. the analysis without a case ending
    return score


@functools.lru_cache(maxsize=None)
def _analyses(word):
    analyzer = _camel()[0]
    return analyzer.analyze(strip_marks(word)) if not any(is_mark(ch) for ch in word) else analyzer.analyze(word)


def _best(word):
    """The analysis that fits `word` best, or None."""
    scored = []
    for a in _analyses(word):
        s = _mismatch(word, a.get("diac", ""))
        if s is not None:
            scored.append((s, -float(a.get("pos_lex_logprob") or 0), a))
    if not scored:
        return None
    return min(scored, key=lambda t: t[:2])[2]


def _split(word):
    """(analysis, prefix, stem, suffix) for a content word, else None."""
    plain = norm(word)
    if plain in STOPWORDS or plain[1:] in STOPWORDS:
        return None
    a = _best(word)
    if a is None or a.get("pos") not in CONTENT_POS:
        return None
    diac, stem = a.get("diac", ""), a.get("stem", "")
    if not stem or "." not in a.get("root", "") or diac.count(stem) != 1:
        return None
    i = diac.index(stem)
    return a, diac[:i], stem, diac[i + len(stem) :]


def _assemble(word, prefix, stem, suffix):
    prefix, stem, suffix = (x.replace(ALEF_WASLA, ALEF) for x in (prefix, stem, suffix))
    if not any(is_mark(ch) for ch in word):
        return strip_marks(prefix + stem + suffix)
    # The analyser omits the shadda the definite article gives a sun letter.
    if strip_marks(prefix).endswith("ال") and stem[0] in SUN and stem[1:2] != SHADDA:
        stem = stem[0] + SHADDA + stem[1:]
    new = prefix + stem + suffix
    # It also leaves most verbs without their mood ending: keep the word's.
    end = "".join(sorted(_vowels(clusters(word)[-1])))
    if end and not _vowels(clusters(new)[-1]):
        new += end
    return new


def _valid(candidate, root):
    return any(a.get("root") == root for a in _analyses(candidate))


def _first_valid(word, rng, prefix, suffix, options):
    """Try (stem, root) options in random order; return the first rewrite that
    analyses as a real word with that root."""
    options = list(options)
    rng.shuffle(options)
    for stem, root in options[:MAX_TRIES]:
        candidate = _assemble(word, prefix, stem, suffix)
        if _valid(strip_marks(candidate), root):
            return candidate
    return word


def _render(pattern, root):
    letters = root.split(".")
    return "".join(letters[int(ch) - 1] if ch.isdigit() else ch for ch in pattern)


def root_word(word, rng, rate=0.5, style="replace"):
    """Swap the root, keeping the pattern and inflection."""
    if rng.random() >= rate:
        return word
    found = _split(word)
    if not found:
        return word
    a, prefix, stem, suffix = found
    _, by_pattern, _, stems = _camel()
    root, cat = a["root"], a.get("stemcat")
    pattern = next((p for s, c, p, _ in _camel()[2].get(root, []) if s == stem and c == cat), None)
    if pattern is None:
        return word
    if style == "replace":
        options = [(s, r) for s, r in by_pattern.get((cat, pattern), []) if r != root]
    else:
        letters = root.split(".")
        slots = [i for i, ch in enumerate(letters) if ch != "#"]
        options = []
        for perm in sorted(set(itertools.permutations([letters[i] for i in slots]))):
            new = letters[:]
            for i, ch in zip(slots, perm):
                new[i] = ch
            new_root = ".".join(new)
            new_stem = _render(pattern, new_root)
            if new_root != root and cat in stems.get((strip_marks(new_stem), new_root), ()):
                options.append((new_stem, new_root))
    return _first_valid(word, rng, prefix, suffix, options)


def pattern_word(word, rng, rate=0.5):
    """Keep the root, but use a different lexeme (pattern) built on it."""
    if rng.random() >= rate:
        return word
    found = _split(word)
    if not found:
        return word
    a, prefix, stem, suffix = found
    root, pos = a["root"], a["pos"]
    entries = _camel()[2].get(root, [])
    current = next((p for s, c, p, _ in entries if s == stem), None)
    options = sorted({(s, root) for s, c, p, q in entries if q == pos and p != current and s != stem})
    return _first_valid(word, rng, prefix, suffix, options)


# --- Flipping gender or number (breaking agreement) ---------------------------

# Features passed to the generator: the word's own, with only gender or number
# changed.
GEN_FEATS = ["pos", "asp", "per", "gen", "num", "vox", "mod", "stt", "cas", "prc0", "prc1", "prc2", "prc3", "enc0"]
AGREEING_POS = {"verb", "adj"}  # words that agree with a noun; nouns keep their gender


@functools.lru_cache(maxsize=None)
def _generator():
    _camel()  # same import check and error message
    from camel_tools.morphology.database import MorphologyDB
    from camel_tools.morphology.generator import Generator

    return Generator(MorphologyDB.builtin_db("calima-msa-r13", "g"))


def _agreeing_analysis(word, feat):
    """The analysis of `word` if it is a verb or adjective, else None. Only
    readings that fit the word's diacritics as well as any reading do count
    (so رُخْصَةَ stays a noun); among those a third-person verb wins: تطلب is
    "she seeks" here, not "you seek"."""
    scored = [(_mismatch(word, a.get("diac", "")), a) for a in _analyses(word)]
    scored = [(s, a) for s, a in scored if s is not None]
    if not scored:
        return None
    best = min(s for s, _ in scored)
    fits = [
        (a.get("per") not in ("3", "na"), -float(a.get("pos_lex_logprob") or 0), a)
        for s, a in scored
        if s == best
    ]
    a = min(fits, key=lambda t: t[:2])[2]
    return a if a.get("pos") in AGREEING_POS and a.get(feat) in FLIPS[feat] else None


# feature → {value: value it is flipped to}. Duals become singular.
MOODS = {"ُ": "i", "َ": "s", "ْ": "j"}  # final vowel → indicative, subjunctive, jussive
FLIPS = {"gen": {"m": "f", "f": "m"}, "num": {"s": "p", "p": "s", "d": "s"}}


def gender_flip(word):
    """`word` with its gender flipped (المُنْصِفِ → المُنْصِفَةِ), or None."""
    return _flip(word, "gen")


def number_flip(word):
    """`word` singular ↔ plural (يُمَيِّزُ → يُمَيِّزُونَ), or None."""
    return _flip(word, "num")


def _flip(word, feat):
    """`word` with one feature flipped by the morphological generator, or None
    if it is not a verb or adjective, or has no form with the other value."""
    plain = norm(word)
    if plain in STOPWORDS or plain[1:] in STOPWORDS:
        return None
    a = _agreeing_analysis(word, feat)
    if a is None:
        return None
    feats = {k: a[k] for k in GEN_FEATS if a.get(k) not in (None, "na")}
    feats[feat] = FLIPS[feat][a[feat]]
    # The analyses rarely know an imperfect verb's mood, so it is read off the
    # final vowel: يُمَيِّزُ → يُمَيِّزُونَ, يُخْلَقْ → يُخْلَقُوا. With an attached
    # pronoun (يَتَلَقَّاهَا) that vowel is the pronoun's; assume indicative.
    tries = [feats]
    if a.get("asp") == "i":
        mood = "i" if a.get("enc0") not in (None, "0") else MOODS.get(next(iter(_vowels(clusters(word)[-1])), None))
        if mood:
            tries = [{**feats, "mod": mood}, feats]  # without the mood if that gives nothing
    forms = set()
    for f in tries:
        try:
            forms = {g["diac"] for g in _generator().generate(a["lex"], f)}
        except Exception:  # feature combinations the generator rejects
            forms = set()
        forms.discard(a.get("diac"))
        if forms:
            break
    if not forms:
        return None
    # The form closest to the original, diacritics included, keeps its
    # spelling and voice (كُرِّمَ → كُرِّمَتْ, not the active كَرَّمَتْ).
    new = max(sorted(forms), key=lambda f: SequenceMatcher(None, f, word).ratio()).replace(ALEF_WASLA, ALEF)
    if not any(is_mark(ch) for ch in word):
        return strip_marks(new)
    # The generator leaves most verbs without their mood ending; restore it
    # when the word still ends in the same letter (not after a new ـت).
    old_end, new_end = clusters(word)[-1], clusters(new)[-1]
    if base(old_end) == base(new_end) and _vowels(old_end) and not _vowels(new_end):
        new += "".join(sorted(_vowels(old_end)))
    return new


def has_conjunction(word):
    """True if the analyser reads `word` as starting with the conjunction و/ف
    (وَشَجَاعَةً), False if not (فَرِيضَةٌ), None if it cannot analyse it."""
    a = _best(word)
    if a is None:
        return None
    return str(a.get("prc2", "0")).startswith(("wa_", "fa_"))


def noun_number(word):
    """"s", "d" or "p" if the analyser reads `word` as a common noun without a
    pronoun suffix (العَقْلُ, الأُمُورَ), False if not, None if it cannot tell."""
    plain = norm(word)
    if plain in STOPWORDS or plain[1:] in STOPWORDS:
        return False
    a = _best(word)
    if a is None:
        return None
    if a.get("pos") != "noun" or a.get("enc0") not in ("0", None):
        return False
    return a.get("num") if a.get("num") in ("s", "d", "p") else "s"


# Parts of speech that carry content: what any question about a text is answered with.
TARGET_POS = CONTENT_POS | {"noun_prop", "noun_num"}


def content_word(word):
    """True if the analyser reads `word` as a content word (noun, verb,
    adjective, adverb, name or number), False for function words."""
    plain = norm(word)
    if plain in STOPWORDS or plain[1:] in STOPWORDS:
        return False
    a = _best(word)
    return a is not None and a.get("pos") in TARGET_POS
