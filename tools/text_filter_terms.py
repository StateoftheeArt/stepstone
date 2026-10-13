"""View, check or change the name and item filter list (public/text-filter.json).

The list is stored encoded so learners who open app files do not see it as plain text.

    python -B tools/text_filter_terms.py show
    python -B tools/text_filter_terms.py check "Some nickname"
    python -B tools/text_filter_terms.py add exact someword
    python -B tools/text_filter_terms.py remove exact someword

Kinds: exact (a whole word), phrases (words joined without spaces, such as "sieghail"),
prefix (a word starting with it), contains (anywhere, only for words with no innocent
uses), allow (innocent words that would otherwise match). Use lowercase a-z only.
After a change, run tools/build_assets.py and the tests.
"""
import argparse
import base64
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
KINDS = ('exact', 'phrases', 'prefix', 'contains', 'allow')
NOTE = 'Encoded list for the name and item filter. View or change it with tools/text_filter_terms.py.'


def read(path):
    record = json.loads(Path(path).read_text(encoding='utf-8'))
    return json.loads(base64.b64decode(record['terms']).decode('utf-8'))


def write(path, terms):
    clean = {k: sorted(set(terms[k])) for k in KINDS}
    for kind, values in clean.items():
        bad = [v for v in values if not re.fullmatch(r'[a-z]{2,40}', v)]
        if bad:
            raise SystemExit(f'Use lowercase a-z only in {kind}: {bad}')
    blob = base64.b64encode(json.dumps(clean, separators=(',', ':')).encode('utf-8')).decode('ascii')
    Path(path).write_text(json.dumps(dict(version=1, note=NOTE, terms=blob), indent=1) + '\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', choices=('show', 'check', 'add', 'remove'))
    parser.add_argument('values', nargs='*')
    parser.add_argument('--file', default=str(ROOT / 'public/text-filter.json'))
    args = parser.parse_args()
    if args.action == 'check':
        from text_filter import acceptable, decode
        terms = decode(json.loads(Path(args.file).read_text(encoding='utf-8')))
        for value in args.values:
            print(('passes   ' if acceptable(value, terms) else 'blocked  ') + value)
        return
    terms = read(args.file)
    if args.action == 'show':
        for kind in KINDS:
            print(f'{kind} ({len(terms[kind])}): ' + ', '.join(terms[kind]))
        return
    if len(args.values) < 2 or args.values[0] not in KINDS:
        raise SystemExit('Name a kind (' + ', '.join(KINDS) + ') and at least one word.')
    kind, words = args.values[0], [w.lower() for w in args.values[1:]]
    terms[kind] = sorted(set(terms[kind]) | set(words)) if args.action == 'add' else [w for w in terms[kind] if w not in words]
    write(args.file, terms)
    print(f'{args.action}: {kind} now has {len(terms[kind])} entries.')


if __name__ == '__main__':
    main()
