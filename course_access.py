"""Current course readiness is independent of historical reward agreements."""
CORE_SUBJECTS = ('math', 'reading', 'science', 'life')
LATER_SUBJECTS = ('digital', 'work')


def required_units(catalog):
    return [u['id'] for sid in CORE_SUBJECTS for u in sorted(
        (u for u in catalog['units'] if u.get('ready') and u.get('active') is not False and u['subject'] == sid),
        key=lambda u: u.get('sequence', 0))]


def readiness(catalog, mastered):
    done = set(mastered)
    courses = []
    for sid in CORE_SUBJECTS:
        ids = [u['id'] for u in catalog['units'] if u.get('ready') and u.get('active') is not False and u['subject'] == sid]
        courses.append(dict(id=sid, title=next(s['name'] for s in catalog['subjects'] if s['id'] == sid),
                            completed=len(done.intersection(ids)), total=len(ids), complete=bool(ids) and set(ids).issubset(done)))
    return dict(courses=courses, completed=sum(c['completed'] for c in courses),
                total=sum(c['total'] for c in courses), complete=all(c['complete'] for c in courses))


def mastered_units(db, learner):
    return [r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1", (learner,))]


def require_course(db, learner, unit, catalog, problem):
    if unit['subject'] in LATER_SUBJECTS and not readiness(catalog, mastered_units(db, learner))['complete']:
        raise problem(409, 'Finish all 24 modules in Money & math, Reading & writing, Science and Life skills to unlock Digital skills and Work & jobs.')
