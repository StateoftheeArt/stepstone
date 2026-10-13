"""Separate learner self-reports from mentor-observed PC demonstrations."""
import json
import time

def records(db,learner):
    return [dict(row) for row in db.execute('SELECT unit,revision,status,note,review_note,updated FROM device_work WHERE learner=? ORDER BY unit',(learner,))]

def save(db,data,learner,units,problem,*,mentor=False):
    unit=data.get('unit');revision=data.get('revision');status=data.get('status');note=data.get('note')
    if not isinstance(unit,str) or unit not in units or not units[unit].get('deviceTask'):raise problem(400,'Choose a PC task.')
    if type(revision) is not int or revision<0:raise problem(400,'Invalid device-work revision.')
    if not isinstance(note,str) or not 1<=len(note.strip())<=1000:raise problem(400,'Add a short update without private details.')
    old=db.execute('SELECT * FROM device_work WHERE learner=? AND unit=?',(learner,unit)).fetchone()
    if (old['revision'] if old else 0)!=revision:raise problem(409,'This device task changed. Reload to read the latest update before saving.')
    review_note='';learner_note=note.strip()
    if mentor:
        if not old:raise problem(400,'Ask the learner to submit a device update first.')
        if status not in ('help','confirmed'):raise problem(400,'Choose a review decision.')
        if status=='confirmed':
            if old['status'] not in ('practised','confirmed') or data.get('observed') is not True:raise problem(400,'Confirm only after the learner reports practice and you observe the real-device steps.')
            passed=any(json.loads(r['report']).get('passed') for r in db.execute('SELECT report FROM attempts WHERE learner=? AND unit=? AND finished IS NOT NULL',(learner,unit)))
            if not passed:raise problem(400,'This PC module check must be passed before confirming the setup task.')
        review_note=learner_note;learner_note=old['note']
    else:
        if status not in ('waiting','help','practised'):raise problem(400,'Choose waiting, help, or practised. Only your mentor can confirm a demonstration.')
        steps=data.get('steps')
        if status=='practised' and (not isinstance(steps,list) or len(steps)!=len(units[unit]['deviceTask']['steps']) or any(step is not True for step in steps)):raise problem(400,'Check each real-device step you tried, or choose help or waiting.')
    now=time.time()
    db.execute('INSERT INTO device_work VALUES(?,?,?,?,?,?,?) ON CONFLICT(learner,unit) DO UPDATE SET revision=excluded.revision,status=excluded.status,note=excluded.note,review_note=excluded.review_note,updated=excluded.updated',(learner,unit,revision+1,status,learner_note,review_note,now))
    db.execute('INSERT INTO device_work_history(learner,unit,revision,actor,status,note,created) VALUES(?,?,?,?,?,?,?)',(learner,unit,revision+1,'mentor' if mentor else 'learner',status,note.strip(),now))
    return records(db,learner)
