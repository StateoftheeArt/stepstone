"""Read-only row fingerprints, plus an optional SQLite-consistent release backup.

Snapshots contain counts and hashes, never learner content or credentials.
"""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

def snapshot(path):
    with sqlite3.connect(f'{Path(path).resolve().as_uri()}?mode=ro', uri=True) as db:
        tables=[r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        result={}
        for table in tables:
            safe=table.replace('"','""')
            rows=sorted(json.dumps(r,ensure_ascii=False,default=str) for r in db.execute(f'SELECT * FROM "{safe}"'))
            result[table]={'count':len(rows),'sha256':hashlib.sha256(json.dumps(rows).encode()).hexdigest()}
        return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('database');p.add_argument('output');p.add_argument('--backup');p.add_argument('--compare')
    args=p.parse_args();path=Path(args.database)
    if args.backup:
        backup=Path(args.backup)
        if backup.exists():raise SystemExit('Backup already exists; refusing to overwrite.')
        backup.parent.mkdir(parents=True,exist_ok=True)
        source=sqlite3.connect(f'{path.resolve().as_uri()}?mode=ro',uri=True);target=sqlite3.connect(backup)
        try:source.backup(target)
        finally:target.close();source.close()
    current=snapshot(path)
    if args.compare:
        before=json.loads(Path(args.compare).read_text(encoding='utf-8'))
        changed=[t for t in before if current.get(t)!=before[t]]
        result={'before':before,'after':current,'changedExistingTables':changed,'newTables':{t:v for t,v in current.items() if t not in before}}
    else:result=current;changed=[]
    Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f'{len(current)} tables fingerprinted; {len(changed)} existing tables changed.')
    if changed:raise SystemExit(1)
