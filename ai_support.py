"""A human-reviewed, once-per-person AI month. No provider or payment API.

Called inside Store's write transaction. A reservation holds existing cash;
recording actual activation spends only the checked total and releases the rest.
"""
import datetime as dt
import json
import time
import projects
from reward_program import text, integer, fail, uid, packed

PC_UNITS = ('pc-start','pc-files','pc-safe','pc-software','pc-recover')
PROVIDERS = ('chatgpt','claude','gemini')
CAP = 5000

def install(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS ai_plans (
      learner TEXT PRIMARY KEY, revision INTEGER NOT NULL, content TEXT NOT NULL, updated REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS ai_months (
      id TEXT PRIMARY KEY, person TEXT NOT NULL, learner TEXT NOT NULL, status TEXT NOT NULL,
      reserve_cents INTEGER NOT NULL, revision INTEGER NOT NULL DEFAULT 0,
      details TEXT NOT NULL DEFAULT '{}', created REAL NOT NULL);
    CREATE UNIQUE INDEX IF NOT EXISTS ai_once_per_person ON ai_months(person) WHERE status!='released';
    CREATE TABLE IF NOT EXISTS learner_projects (
      learner TEXT PRIMARY KEY, revision INTEGER NOT NULL, content TEXT NOT NULL, updated REAL NOT NULL);
    ''')

def held(db):
    return db.execute("SELECT COALESCE(SUM(reserve_cents),0) FROM ai_months WHERE status IN ('allocated','pending','approved')").fetchone()[0]

def readiness(db,learner):
    passed={r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1",(learner,))}
    device={r[0] for r in db.execute("SELECT unit FROM device_work WHERE learner=? AND status='confirmed'",(learner,))}
    starter=projects.starter(projects.get(db,learner))
    gates=[dict(id=u,label=u,done=u in passed and u in device) for u in PC_UNITS]
    gates += [dict(id=u,label=u,done=u in passed) for u in ('digital-5','digital-6')]
    gates.append(dict(id='project-starter',label='Choose a project and save its first working version',done=starter))
    return dict(ready=all(g['done'] for g in gates),gates=gates)

def record(db,learner,funded):
    plan=db.execute('SELECT * FROM ai_plans WHERE learner=?',(learner,)).fetchone()
    person=funded.person(db,learner)
    row=db.execute("SELECT * FROM ai_months WHERE person=? AND status!='released'",(person['id'],)).fetchone() if person else None
    return dict(plan=dict(revision=plan['revision'],**json.loads(plan['content'])) if plan else None,
      month=dict(row)|dict(details=json.loads(row['details'])) if row else None,
      primary=bool(person and person['primary_learner']==learner),**readiness(db,learner))

def history(db):
    return [dict(r)|dict(details=json.loads(r['details'])) for r in db.execute('SELECT a.*,l.alias FROM ai_months a JOIN learners l ON a.learner=l.id ORDER BY created DESC,id')]

def learner_action(db,action,data,learner,store):
    store.require_tutorial(db,learner)
    if action=='plan':
        revision=integer(data,'revision',0,10000000)
        old=db.execute('SELECT * FROM ai_plans WHERE learner=?',(learner,)).fetchone()
        if revision!=(old['revision'] if old else 0):fail('Your AI notes changed on another screen. Refresh before saving.')
        provider=data.get('provider');mode=data.get('mode')
        if provider not in (*PROVIDERS,'unsure','none') or mode not in ('prepared','own-service'):fail('Choose how you compared the examples and your preference.',400)
        result=dict(provider=provider,mode=mode,explain=text(data,'explain',3,600),email=text(data,'email',3,600),change=text(data,'change',3,600),reason=text(data,'reason',3,600))
        if mode=='own-service' and data.get('permitted') is not True:fail('Only use your own permitted service account. Prepared examples work too.',400)
        db.execute('INSERT INTO ai_plans VALUES(?,?,?,?) ON CONFLICT(learner) DO UPDATE SET revision=excluded.revision,content=excluded.content,updated=excluded.updated',(learner,revision+1,packed(result),time.time()))
        # Changing a preference must not silently change an approved purchase.
        for row in db.execute("SELECT * FROM ai_months WHERE learner=? AND status IN ('pending','approved')",(learner,)).fetchall():
            db.execute("UPDATE ai_months SET status='allocated',revision=revision+1,details='{}' WHERE id=?",(row['id'],))
            store.funded.audit(db,learner,'ai-plan-changed',dict(id=row['id'],from_state=row['status'],to_state='allocated',reason='Learner changed their comparison notes. Review again.'))
        return dict(ok=True)
    if action=='request':
        info=record(db,learner,store.funded);row=info['month']
        if not info['primary'] or not row:fail('Your mentor needs to confirm your main account and set aside funding first.')
        if row['status'] in ('pending','approved','active','closed'):return dict(ok=True,id=row['id'])
        if not info['ready']:fail('Finish the named skills, show the PC tasks, and save your project starter first.')
        if not info['plan'] or info['plan']['provider'] not in PROVIDERS:fail('Save a service preference first, or keep using the free project route.')
        db.execute("UPDATE ai_months SET status='pending',revision=revision+1 WHERE id=?",(row['id'],))
        store.funded.audit(db,learner,'ai-request',dict(id=row['id'],from_state='allocated',to_state='pending',points=0))
        return dict(ok=True,id=row['id'])
    fail('AI learning action not found.',404)

def date(data,key):
    value=text(data,key,10,10)
    try:return dt.date.fromisoformat(value)
    except ValueError:fail('Use a real date for '+key.replace('_',' ')+'.',400)

def eligibility(data,provider):
    age=data.get('age_band')
    if age not in ('under13','13-17','18plus'):fail('Confirm the learner’s age band, without storing their birthday.',400)
    if age=='under13' or provider=='claude' and age!='18plus':fail('This funded plan does not fit that age band. Keep the free learning route and choose a permitted option.',400)
    for key in ('terms_checked','own_account','monthly_only','no_addons','demonstrated'):
        if data.get(key) is not True:fail('Confirm the current eligibility, own account, monthly cost controls and skill demonstration.',400)
    if age=='13-17' and data.get('guardian_permission') is not True:fail('This pilot needs the appropriate parent/legal guardian’s permission for an under-18 paid account. A mentor cannot substitute for them.',400)
    checked=date(data,'checked_on')
    if not 0<=(dt.date.today()-checked).days<=7:fail('Recheck the service and plan rules within seven days before approval.',400)
    return dict(age_band=age,guardian_permission=data.get('guardian_permission') is True,checked_on=str(checked),
      terms_checked=True,own_account=True,monthly_only=True,no_addons=True,demonstrated=True)

def mentor_action(db,action,data,store):
    funded=store.funded
    return funded.command(db,'ai-'+action,data,lambda:_mentor(db,action,data,store))

def _mentor(db,action,data,store):
    funded=store.funded
    if action=='reserve':
        learner=text(data,'learner');funded.require_learner(db,learner)
        person=funded.person(db,learner)
        if not person or person['primary_learner']!=learner:fail('Confirm the learner’s main reward account first.')
        existing=db.execute("SELECT id FROM ai_months WHERE person=? AND status!='released'",(person['id'],)).fetchone()
        if existing:return dict(ok=True,id=existing['id'])
        cents=integer(data,'cents',1,CAP)
        if funded.cash(db)<cents:fail('Record money actually received first. These funds cannot also pay for another reward.')
        note=text(data,'note',3,500);ident=uid()
        db.execute('INSERT INTO ai_months(id,person,learner,status,reserve_cents,created) VALUES(?,?,?,?,?,?)',(ident,person['id'],learner,'allocated',cents,time.time()))
        funded.audit(db,'mentor','ai-reserve',dict(id=ident,person=person['id'],cents=cents,reason=note,to_state='allocated'))
        return dict(ok=True,id=ident)
    row=db.execute('SELECT * FROM ai_months WHERE id=?',(text(data,'id'),)).fetchone()
    if not row:fail('AI month record not found.',404)
    if integer(data,'revision',0,10000000)!=row['revision']:fail('This AI month changed. Reopen it before saving.')
    old=row['status'];details=json.loads(row['details']);note=text(data,'note',3,500)
    state=old
    if action=='release':
        if old not in ('allocated','pending','approved'):fail('An activated month cannot be released or funded again.')
        state='released'
    elif action=='approve':
        if old!='pending':fail('Review the learner’s request before approving a purchase.')
        info=record(db,row['learner'],funded)
        if not info['ready']:fail('The learning, observed PC work and project starter must still be ready.')
        provider=info['plan']['provider'] if info['plan'] else None
        if provider not in PROVIDERS:fail('The learner needs an eligible service preference.')
        checks=eligibility(data,provider)
        cents=integer(data,'cents',1,row['reserve_cents'])
        details=dict(provider=provider,plan=text(data,'plan',2,100),approved_cents=cents,
          comparison_revision=info['plan']['revision'],eligibility=checks,approved_on=str(dt.date.today()))
        state='approved'
    elif action=='activate':
        if old!='approved':fail('Approve this exact monthly plan first. Each person has one funded month.')
        info=record(db,row['learner'],funded)
        if not info['ready'] or info['plan']['revision']!=details['comparison_revision']:fail('The readiness or preference changed. Review it again.')
        if (dt.date.today()-dt.date.fromisoformat(details['eligibility']['checked_on'])).days>7:fail('The eligibility check is old. Release the unused reservation and review a current request.')
        cents=integer(data,'cents',1,details['approved_cents'])
        start=date(data,'activated_on');end=date(data,'paid_through')
        if start>dt.date.today() or (dt.date.today()-start).days>31 or not 27<=(end-start).days<=32:fail('Record the actual recent activation and one monthly period (28–33 calendar days inclusive).',400)
        if data.get('paid_confirmed') is not True:fail('Only record a purchase that actually happened outside Stepstone.',400)
        renewal=data.get('renewal')
        if renewal not in ('off','cancel-scheduled'):fail('Record renewal off or a verified cancellation plan.',400)
        cancel_by=date(data,'cancel_by') if renewal=='cancel-scheduled' else None
        if cancel_by and not dt.date.today()<=cancel_by<end:fail('Choose a cancellation date before the paid period ends.',400)
        cancellation=text(data,'cancellation',3,400)
        details.update(actual_cents=cents,activated_on=str(start),paid_through=str(end),renewal=renewal,
          cancel_by=str(cancel_by) if cancel_by else '',cancellation=cancellation)
        state='active'
        db.execute('INSERT INTO reward_funding VALUES(?,?,?,?,?,?,?)',('ai-payment-'+row['id'],'ai-month',-cents,None,0,'AI month record: '+details['provider']+' / '+note,time.time()))
    elif action=='renewal':
        if old not in ('active','closed'):fail('No activated month to update.')
        if data.get('renewal')!='off' or data.get('verified') is not True:fail('Confirm renewal is off in the provider account first.',400)
        details.update(renewal='off',cancel_by='',cancellation=text(data,'cancellation',3,400))
    elif action=='close':
        if old!='active' or details.get('renewal')!='off':fail('Confirm renewal is off before closing this record.')
        if dt.date.today()<=dt.date.fromisoformat(details['paid_through']):fail('Keep the active record until its paid-through date has passed.')
        state='closed'
    else:fail('AI month action not found.',404)
    db.execute('UPDATE ai_months SET status=?,details=?,revision=revision+1 WHERE id=?',(state,packed(details),row['id']))
    funded.audit(db,'mentor','ai-'+action,dict(id=row['id'],person=row['person'],from_state=old,to_state=state,reason=note,details=details))
    return dict(ok=True,id=row['id'])
