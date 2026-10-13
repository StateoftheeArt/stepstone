"""Durable module rewards and elapsed-time Pip food, separate from money points."""
import json
import time

PORTION_SECONDS = 30 * 60
BOWL_PORTIONS = 3
REVIEW_SECONDS = 24 * 60 * 60
SCHEDULE_VERSION = '2'


def choices(options):
    groups = [('accessory', options['accessories'])]
    groups.extend(('home.' + field, items) for field, items in options['home'].items())
    return [dict(item, kind=kind, key=kind + ':' + item['id'])
            for kind, items in groups for item in items if item.get('modules', 0) > 0]


def install(db, options):
    db.executescript('''
        CREATE TABLE IF NOT EXISTS pip_grants (
            learner TEXT NOT NULL, unit TEXT NOT NULL, finished REAL NOT NULL,
            items TEXT NOT NULL, food INTEGER NOT NULL CHECK(food>=0),
            PRIMARY KEY(learner,unit));
        CREATE TABLE IF NOT EXISTS pip_food (
            learner TEXT PRIMARY KEY, bank INTEGER NOT NULL DEFAULT 0 CHECK(bank>=0),
            remaining REAL NOT NULL DEFAULT 0 CHECK(remaining>=0), last REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS pip_feeds (
            learner TEXT NOT NULL, id TEXT NOT NULL, at REAL NOT NULL,
            PRIMARY KEY(learner,id));
        CREATE TABLE IF NOT EXISTS pip_review_grants (
            learner TEXT NOT NULL, attempt TEXT NOT NULL, unit TEXT NOT NULL,
            at REAL NOT NULL, PRIMARY KEY(learner,attempt));
        CREATE INDEX IF NOT EXISTS pip_review_cooldown
            ON pip_review_grants(learner,unit,at);
        CREATE TABLE IF NOT EXISTS pip_starting_items (
            learner TEXT PRIMARY KEY, units TEXT NOT NULL, items TEXT NOT NULL);
    ''')
    if not db.execute("SELECT 1 FROM settings WHERE key='pipRewardSchedule'").fetchone():
        # Freeze build97 awards before changing the thresholds. Unselected items
        # are preserved too, and each old completed module gets its food portion.
        for row in db.execute('SELECT id FROM learners').fetchall():
            sync_grants(db, row['id'], options, legacy=True)
        db.execute("INSERT INTO settings VALUES('pipRewardSchedule',?)", (SCHEDULE_VERSION,))


def first_passes(db, learner):
    return db.execute('''SELECT unit,finished,report FROM (
        SELECT unit,finished,report,rowid AS attempt_order,
               ROW_NUMBER() OVER(PARTITION BY unit ORDER BY finished,rowid) AS occurrence
        FROM attempts WHERE learner=? AND finished IS NOT NULL
             AND json_extract(report,'$.passed')=1)
        WHERE occurrence=1 ORDER BY finished,attempt_order''', (learner,)).fetchall()


def inventory(db, learner):
    owned={item['key'] for row in db.execute('SELECT items FROM pip_grants WHERE learner=?', (learner,))
           for item in json.loads(row['items'])}
    starting=db.execute('SELECT items FROM pip_starting_items WHERE learner=?',(learner,)).fetchone()
    if starting:owned.update(item['key'] for item in json.loads(starting['items']))
    return owned


def starting_item_units(catalog, result):
    """Only a completed server-evaluated suggestion supplies cosmetic milestones."""
    if not result or not result.get('complete'):return set()
    units=set()
    for subject in ('math','reading','science','life'):
        chain=sorted((u for u in catalog['units'] if u.get('ready') and u.get('active') is not False and u['subject']==subject),
                     key=lambda u:u.get('sequence') or u.get('grade',0))
        if result.get('version') in (4,5):
            suggested=result.get('suggestions',{}).get(subject)
        elif subject=='life':
            suggested=chain[0]['id'] if chain else None
        else:
            area='reading' if subject=='reading' else subject
            levels=result.get('levels',{})
            level=min(levels.get('reading',1),levels.get('writing',1)) if area=='reading' else levels.get(area,1)
            suggested=next((u['id'] for u in chain if u['id']==area+'-'+str(level)),None)
            if not suggested:
                suggested=next((u['id'] for u in chain if (u.get('placementArea') or u.get('domain') or u['subject'])==area
                                and not u.get('practical') and u.get('grade',0)>=level),None)
        index=next((i for i,u in enumerate(chain) if u['id']==suggested),0)
        units.update(u['id'] for u in chain[:index])
    return units


def sync_starting_items(db, learner, options, catalog, result):
    if not result or not result.get('complete'):return
    row=db.execute('SELECT units,items FROM pip_starting_items WHERE learner=?',(learner,)).fetchone()
    units=starting_item_units(catalog,result)
    if row:
        previous=set(json.loads(row['units']));units.update(previous)
        if units==previous:return
    count=len(units|{a['unit'] for a in first_passes(db,learner)})
    items={item['key']:item for item in json.loads(row['items'])} if row else {}
    owned=inventory(db,learner)
    for item in choices(options):
        if item['modules']<=count and item['key'] not in owned:items[item['key']]=item
    db.execute('INSERT INTO pip_starting_items VALUES(?,?,?) ON CONFLICT(learner) DO UPDATE SET units=excluded.units,items=excluded.items',
               (learner,json.dumps(sorted(units)),json.dumps(list(items.values()))))


def sync_grants(db, learner, options, legacy=False, now=None):
    now = time.time() if now is None else now
    db.execute('INSERT OR IGNORE INTO pip_food(learner,last) VALUES(?,?)', (learner, now))
    owned = inventory(db, learner)
    unlocks = choices(options)
    starting=db.execute('SELECT units FROM pip_starting_items WHERE learner=?',(learner,)).fetchone()
    seen=set(json.loads(starting['units'])) if starting and not legacy else set()
    for ordinal, row in enumerate(first_passes(db, learner), 1):
        before=len(seen);seen.add(row['unit'])
        if db.execute('SELECT 1 FROM pip_grants WHERE learner=? AND unit=?', (learner, row['unit'])).fetchone():
            continue
        items = [item for item in unlocks
                 if item.get('legacyModules' if legacy else 'modules', item['modules']) == ordinal
                 and item['key'] not in owned]
        if starting and not legacy:
            items=[item for item in unlocks if before<item['modules']<=len(seen) and item['key'] not in owned]
        db.execute('INSERT INTO pip_grants VALUES(?,?,?,?,?)',
                   (learner, row['unit'], row['finished'], json.dumps(items), 1))
        db.execute('UPDATE pip_food SET bank=bank+1 WHERE learner=?', (learner,))
        owned.update(item['key'] for item in items)


def wins(db, learner, options):
    sync_grants(db, learner, options)
    grants = {row['unit']: row for row in db.execute('SELECT * FROM pip_grants WHERE learner=?', (learner,))}
    result = []
    for row in first_passes(db, learner):
        report = json.loads(row['report'])
        summary = {key: report.get(key) for key in ('title', 'score')}
        summary.update(passed=True, total=report.get('total', 6), tryNumber=report.get('tryNumber', 1))
        grant = grants[row['unit']]
        result.append(dict(unit=row['unit'], finished=row['finished'], report=summary,
                           pipItems=json.loads(grant['items']), pipFood=grant['food']))
    return result


def food(db, learner, now=None):
    now = time.time() if now is None else now
    db.execute('INSERT OR IGNORE INTO pip_food(learner,last) VALUES(?,?)', (learner, now))
    row = db.execute('SELECT * FROM pip_food WHERE learner=?', (learner,)).fetchone()
    # Never regain food if the host clock moves backwards.
    observed = max(now, row['last'])
    remaining = max(0.0, row['remaining'] - (observed - row['last']))
    db.execute('UPDATE pip_food SET remaining=?,last=? WHERE learner=?', (remaining, observed, learner))
    return dict(bank=row['bank'], remaining=remaining, asOf=observed,
                portionSeconds=PORTION_SECONDS, capacity=BOWL_PORTIONS * PORTION_SECONDS)


def award_review(db, learner, attempt, unit, eligible, previously_passed, passed, now=None):
    """Called in the attempt's submit transaction. Never backfill old replays."""
    now = time.time() if now is None else now
    if not passed:
        return dict(pipFoodEarned=0, pipFoodReason='none')
    if not previously_passed:
        # The existing first-pass grant is credited by sync_grants after submit.
        return dict(pipFoodEarned=1, pipFoodReason='first')
    if not eligible:
        return dict(pipFoodEarned=0, pipFoodReason='none')
    receipt = db.execute('SELECT at FROM pip_review_grants WHERE learner=? AND attempt=?',
                         (learner, attempt)).fetchone()
    if receipt:
        return dict(pipFoodEarned=1, pipFoodReason='review', pipFoodNextAt=receipt['at'] + REVIEW_SECONDS)
    latest = db.execute('SELECT MAX(at) AS at FROM pip_review_grants WHERE learner=? AND unit=?',
                        (learner, unit)).fetchone()['at']
    if latest is not None and now < latest + REVIEW_SECONDS:
        return dict(pipFoodEarned=0, pipFoodReason='cooldown', pipFoodNextAt=latest + REVIEW_SECONDS)
    db.execute('INSERT OR IGNORE INTO pip_food(learner,last) VALUES(?,?)', (learner, now))
    db.execute('INSERT INTO pip_review_grants VALUES(?,?,?,?)', (learner, attempt, unit, now))
    db.execute('UPDATE pip_food SET bank=bank+1 WHERE learner=?', (learner,))
    return dict(pipFoodEarned=1, pipFoodReason='review', pipFoodNextAt=now + REVIEW_SECONDS)


def feed(db, learner, request_id, problem, now=None):
    now = time.time() if now is None else now
    state = food(db, learner, now)
    if db.execute('SELECT 1 FROM pip_feeds WHERE learner=? AND id=?', (learner, request_id)).fetchone():
        return state
    if state['bank'] < 1:
        raise problem(409, 'Complete a new module or replay a food-review module to earn food for Pip.')
    if state['remaining'] > state['capacity'] - PORTION_SECONDS:
        raise problem(409, 'Pip’s bowl has enough food for now.')
    db.execute('UPDATE pip_food SET bank=bank-1,remaining=remaining+? WHERE learner=?',
               (PORTION_SECONDS, learner))
    db.execute('INSERT INTO pip_feeds VALUES(?,?,?)', (learner, request_id, now))
    return food(db, learner, now)
