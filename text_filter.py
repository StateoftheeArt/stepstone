"""Keep names and item names suitable for a PG-16 learning space. Mirrors public/text-filter.js.

It checks whole words, common disguises (s h 1 t, f*ck, repeated letters) and a few short
phrases. Adjacent words are checked only against phrases and the strongest words, so
"red skin potatoes" or "Scunthorpe" still pass. It is a first check, not full moderation.
Human-authored text is checked at the form and save boundaries in human_text.py. The list is stored encoded in
public/text-filter.json; view or change it with tools/text_filter_terms.py.
"""
import base64
import itertools
import json
import re
import string
import unicodedata
from pathlib import Path

LIST = Path(__file__).resolve().parent / 'public/text-filter.json'
LEET = str.maketrans({'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', '$': 's', '!': 'i', '|': 'i'})
MARKS = re.compile('[̀-ͯ]')


def decode(record):
    terms = json.loads(base64.b64decode(record['terms']).decode('utf-8'))
    return dict(exact=frozenset(terms['exact']), phrases=frozenset(terms['phrases']), allow=frozenset(terms['allow']),
                prefix=tuple(terms['prefix']), contains=tuple(terms['contains']))


TERMS = decode(json.loads(LIST.read_text(encoding='utf-8')))


def words(text):
    folded = MARKS.sub('', unicodedata.normalize('NFKD', text)).lower().translate(LEET)
    return re.findall(r'[a-z*]+', folded)


def candidates(tokens):
    """(text, whole) pairs. Whole words get every check; joined neighbours only phrases and strong words."""
    found = [(t, True) for t in tokens]
    for n in (2, 3):
        found += [(''.join(tokens[i:i + n]), False) for i in range(len(tokens) - n + 1)]
    run = []
    for t in tokens + ['']:
        if len(t) == 1:
            run.append(t)
        else:
            if len(run) >= 2:
                found.append((''.join(run), True))
            run = []
    if len(tokens) > 3:
        found.append((''.join(tokens), False))
    return found


def acceptable(text, terms=TERMS):
    if not isinstance(text, str):
        return True

    def hit(form, whole):
        if form in terms['allow']:
            return False
        if form in terms['phrases'] or any(c in form for c in terms['contains']):
            return True
        return whole and (form in terms['exact'] or any(form.startswith(p) for p in terms['prefix']))

    stars = 0
    for value, whole in candidates(words(text)):
        for form in dict.fromkeys((value, re.sub(r'(.)\1+', r'\1', value), re.sub(r'(.)\1{2,}', r'\1\1', value))):
            if '*' not in form:
                if hit(form, whole):
                    return False
                continue
            # A star may hide one letter; limited so long text stays quick.
            if not whole or form.count('*') > 2 or len(form) > 12 or stars >= 10:
                continue
            stars += 1
            parts = form.split('*')
            for letters in itertools.product(string.ascii_lowercase, repeat=len(parts) - 1):
                if hit(''.join(p + l for p, l in zip(parts, letters + ('',))), True):
                    return False
    return True
