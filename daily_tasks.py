"""Small daily checklist. Server-derived completion never awards points or food."""
from datetime import datetime
import time
from zoneinfo import ZoneInfo

ZONE = ZoneInfo('America/Winnipeg')
TASKS = ('visit', 'module', 'play')


def day_at(at=None):
    return datetime.fromtimestamp(time.time() if at is None else at, ZONE).date().isoformat()


def install(db):
    db.execute('CREATE TABLE IF NOT EXISTS daily_tasks (learner TEXT NOT NULL, day TEXT NOT NULL, task TEXT NOT NULL, at REAL NOT NULL, PRIMARY KEY(learner,day,task))')


def mark(db, learner, task, at=None):
    if task not in TASKS:
        raise ValueError('Unknown daily task')
    now = time.time() if at is None else at
    db.execute('INSERT OR IGNORE INTO daily_tasks VALUES(?,?,?,?)', (learner, day_at(now), task, now))


def snapshot(db, learner, at=None):
    today = day_at(at)
    done = {r[0] for r in db.execute('SELECT task FROM daily_tasks WHERE learner=? AND day=?', (learner, today))}
    # Existing passed checks count on their actual day, including checks made
    # before this checklist was introduced. Mentor viewing does not mark a visit.
    for r in db.execute("SELECT finished FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1", (learner,)):
        if day_at(r[0]) == today:
            done.add('module')
            break
    return dict(day=today, zone='America/Winnipeg', completed=sorted(done), total=3)
