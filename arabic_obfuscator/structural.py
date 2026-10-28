"""Transforms that change a word's structure rather than its letters' glyphs:
shuffling middle letters, breaking joins with ZWNJ, and stretching with kashida.

All of them work on clusters (a letter plus its marks) so that vowelled text
keeps each haraka on the letter it belongs to.
"""

from .shaping import base, clusters, joins_next, joins_prev, strip_marks

ZWNJ = "‌"  # zero-width non-joiner: shows the letters either side unjoined
TATWEEL = "ـ"  # ـ
ARTICLE = "ال"  # ال


def shuffle_word(word, rng):
    """Shuffle the interior letters, keeping the first and last letter (and the
    definite article) in place so the word stays recognisable to a reader."""
    cs = clusters(word)
    head = 3 if strip_marks(word).startswith(ARTICLE) else 1
    middle = cs[head:-1]
    if len({base(c) for c in middle}) < 2:
        return word
    original = middle[:]
    while [base(c) for c in middle] == [base(c) for c in original]:
        rng.shuffle(middle)
    return "".join(cs[:head] + middle + cs[-1:])


def join_gaps(cs):
    """Indices k where cluster k joins onto cluster k + 1."""
    return [
        k
        for k in range(len(cs) - 1)
        if joins_next(base(cs[k])) and joins_prev(base(cs[k + 1]))
    ]


def insert_after(cs, fillers):
    """Join clusters, appending fillers[k] (if any) after cluster k."""
    return "".join(c + fillers.get(k, "") for k, c in enumerate(cs))


def disconnect_word(word, rng, rate=1.0):
    """Break a random `rate` fraction of the joins between letters."""
    cs = clusters(word)
    return insert_after(cs, {k: ZWNJ for k in join_gaps(cs) if rng.random() < rate})


def kashida_word(word, rng, rate=0.3):
    """Stretch a random `rate` fraction of the joins with 1–3 tatweels."""
    cs = clusters(word)
    return insert_after(
        cs, {k: TATWEEL * rng.randint(1, 3) for k in join_gaps(cs) if rng.random() < rate}
    )
