"""Create, verify or safely stage a private Stepstone recovery copy."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backups import create_snapshot, restore_snapshot, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    create = actions.add_parser('create')
    create.add_argument('--data', type=Path, required=True)
    create.add_argument('--output', type=Path, required=True)
    check = actions.add_parser('verify')
    check.add_argument('snapshot', type=Path)
    restore = actions.add_parser('restore')
    restore.add_argument('snapshot', type=Path)
    restore.add_argument('--to', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == 'create':
            result = create_snapshot(args.data / 'stepstone.sqlite3', args.output)
        elif args.action == 'verify':
            result = verify(args.snapshot)
        else:
            result = restore_snapshot(args.snapshot, args.to)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))


if __name__ == '__main__':
    main()
