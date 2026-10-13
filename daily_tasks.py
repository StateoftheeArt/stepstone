"""Small daily checklist. Server-derived completion never awards points or food."""
from datetime import datetime, timedelta, timezone
import time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    ZONE = ZoneInfo('America/Winnipeg')
except ZoneInfoNotFoundError:
    ZONE = None  # Stock Windows Python may have no IANA timezone database.
# S.M. 2023, c. 4, proclaimed for 31 October 2026: Manitoba uses UTC-5.
# Apply the same boundary in public/daily-tasks.js, including on older browsers.
FIXED_TIME_FROM = datetime(2026, 10, 31, 5, tzinfo=timezone.utc).timestamp()
MANITOBA_TIME = timezone(timedelta(hours=-5))
TASKS = ('visit', 'module', 'play')


def day_at(at=None):
    stamp = time.time() if at is None else at
    if stamp >= FIXED_TIME_FROM:
        return datetime.fromtimestamp(stamp, MANITOBA_TIME).date().isoformat()
    if ZONE is not None:
        return datetime.fromtimestamp(stamp, ZONE).date().isoformat()
    # The pilot's pre-change records use the North American rules in effect
    # since 2007. This fallback avoids adding an installation dependency.
    utc = datetime.fromtimestamp(stamp, timezone.utc)
    march = datetime(utc.year, 3, 1, 8, tzinfo=timezone.utc)
    start = march + timedelta(days=(6-march.weekday()) % 7 + 7)
    november = datetime(utc.year, 11, 1, 7, tzinfo=timezone.utc)
    end = november + timedelta(days=(6-november.weekday()) % 7)
    offset = -5 if start <= utc < end else -6
    return (utc + timedelta(hours=offset)).date().isoformat()


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
