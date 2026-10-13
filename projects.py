"""One learner-owned, bounded utility app; no supplied code is executed."""
import copy
import json
import re
import time
from reward_program import fail, integer, packed, text
from text_filter import acceptable

KINDS=('checklist','inventory','planner','savings')
CASES=('normal','empty','boundary','invalid')
ITEM_WORDS='Use different words for this item. Names and items in Stepstone need to suit everyone.'
PLAN_WORDS='Use different words in your app plan. Names and items in Stepstone need to suit everyone.'

def get(db,learner):
    row=db.execute('SELECT * FROM learner_projects WHERE learner=?',(learner,)).fetchone()
    return dict(revision=row['revision'],data=json.loads(row['content']),updated=row['updated']) if row else None

def config(data):
    if not isinstance(data,dict) or data.get('kind') not in KINDS:fail('Choose a project type.',400)
    behaviours=data.get('behaviours')
    if not isinstance(behaviours,list) or len(behaviours)!=3 or any(not isinstance(s,str) or not 3<=len(s.strip())<=180 for s in behaviours):fail('Describe three things your app should do.',400)
    result=dict(version=1,kind=data['kind'],title=text(data,'title',3,60),purpose=text(data,'purpose',8,500),
      behaviours=[s.strip() for s in behaviours],label=text(data,'label',2,32),limit=integer(data,'limit',1,30),
      goal=integer(data,'goal',1,100000000),accent=data.get('accent') if data.get('accent') in ('teal','violet','amber') else 'teal')
    if not all(acceptable(s) for s in (result['title'],result['purpose'],result['label'],*result['behaviours'])):fail(PLAN_WORDS,400)
    return result

def value(kind,raw):
    if kind=='checklist':return 0
    if not isinstance(raw,str):raise ValueError('Enter a number in the value box.')
    raw=raw.strip()
    if kind=='savings':
        if not re.fullmatch(r'\d{1,6}(?:\.\d{1,2})?',raw):raise ValueError('Use dollars and up to two cents digits, such as 2.50.')
        whole,_,fraction=raw.partition('.');v=int(whole)*100+int(fraction.ljust(2,'0') or '0')
        if not 1<=v<=100000000:raise ValueError('Use a positive amount up to 1000000.00.')
    else:
        if not re.fullmatch(r'\d{1,4}',raw):raise ValueError('Use a whole number, such as 3.')
        v=int(raw);lo,hi=(0,9999) if kind=='inventory' else (1,1440)
        if not lo<=v<=hi:raise ValueError(f'Use a value from {lo} to {hi}.')
    return v

def add(data,label,raw):
    if not isinstance(label,str) or not 1<=len(label.strip())<=80:raise ValueError('Write an item name from 1 to 80 characters.')
    if not acceptable(label):raise ValueError(ITEM_WORDS)
    if len(data['items'])>=data['limit']:raise ValueError('Your list is full. Remove an item or increase the limit.')
    n=value(data['kind'],raw)
    data['items'].append(dict(id=max([x['id'] for x in data['items']]+[0])+1,label=label.strip(),value=n,done=False))

def validate_backup(raw):
    if not isinstance(raw,dict) or raw.get('format')!='stepstone-project' or raw.get('version')!=1:fail('Choose a Stepstone project backup, version 1.',400)
    source=raw.get('data');result=config(source)
    items=source.get('items')
    if not isinstance(items,list) or len(items)>result['limit']:fail('This backup has too many items.',400)
    result['items']=[];seen=set()
    for row in items:
        if not isinstance(row,dict):fail('An item in the backup is invalid.',400)
        ident=integer(row,'id',1,100000000);n=integer(row,'value',0,100000000)
        if ident in seen or type(row.get('done')) is not bool:fail('An item in the backup is invalid.',400)
        if result['kind']=='checklist' and n!=0 or result['kind']=='inventory' and n>9999 or result['kind']=='planner' and not 1<=n<=1440 or result['kind']=='savings' and not 1<=n<=100000000:fail('A saved amount is outside this app’s range.',400)
        label=text(row,'label',1,80)
        if not acceptable(label):fail(ITEM_WORDS,400)
        seen.add(ident);result['items'].append(dict(id=ident,label=label,value=n,done=row['done']))
    return result

def starter(record):
    try:return bool(record and validate_backup(dict(format='stepstone-project',version=1,data=record['data']))['items'])
    except Exception:return False

def ready(record):
    d=record['data'] if record else {}
    return starter(record) and all(d.get('tests',{}).get(k,{}).get('passed') is True for k in CASES) and len(d.get('explanation',''))>=20

def test_case(data,case):
    if case not in CASES:fail('Choose an available test.',400)
    trial=copy.deepcopy(data);trial['items']=[]
    label='Practice item';raw='2.50' if data['kind']=='savings' else '2'
    if case=='empty':label=' '
    elif case=='invalid':
        if data['kind']=='checklist':label='x'*81
        else:raw='not a number'
    elif case=='boundary':trial['items']=[dict(id=i+1,label='Full list item',value=1,done=False) for i in range(data['limit'])]
    before=len(trial['items'])
    try:add(trial,label,raw);message='One item was added.'
    except ValueError as e:message=str(e)
    outcome='added' if len(trial['items'])==before+1 else 'unchanged'
    return dict(outcome=outcome,actual=message,before=before,after=len(trial['items']))

def action(db,action,data,learner,store):
    store.require_tutorial(db,learner)
    old=get(db,learner);revision=integer(data,'revision',0,10000000)
    if revision!=(old['revision'] if old else 0):fail('Your project changed on another screen. Reload the saved copy before trying again.')
    d=copy.deepcopy(old['data']) if old else None
    history=d.pop('history',[]) if d else []
    if action in ('save','restore'):
        new=config(data.get('data')) if action=='save' else validate_backup(data.get('backup'))
        if action=='save':new['items']=d.get('items',[]) if d and d.get('kind')==new['kind'] else []
        if len(new['items'])>new['limit']:fail('This limit is below the items already saved. Remove some first.',400)
        if d:history.append(d)
        d=new
    elif not d:fail('Save your first project plan before using its controls.',400)
    elif action in ('add','toggle','remove'):
        prior=copy.deepcopy(d)
        if action=='add':
            try:add(d,data.get('label'),data.get('value',''))
            except ValueError as e:fail(str(e),400)
        else:
            ident=integer(data,'id',1,100000000);item=next((i for i in d['items'] if i['id']==ident),None)
            if not item:fail('That item changed. Reload the saved project.')
            if action=='remove':d['items'].remove(item)
            else:item['done']=not item['done']
        history.append(prior)
        d.pop('tests',None);d.pop('explanation',None)
    elif action=='undo':
        if not history:fail('There is no earlier saved change to undo.')
        d=history.pop();d.pop('tests',None);d.pop('explanation',None)
    elif action=='test':
        result=test_case(d,data.get('case'))
        prediction=data.get('prediction')
        if prediction not in ('added','unchanged'):fail('Predict whether the test adds an item.',400)
        result.update(prediction=prediction,passed=prediction==result['outcome'])
        d.setdefault('tests',{})[data['case']]=result
    elif action=='explain':
        d['explanation']=text(data,'explanation',20,1800)
        d['accessNote']=text(data,'accessNote',3,500)
        d['backupNote']=text(data,'backupNote',3,500)
    else:fail('Project action not found.',404)
    # A changed artifact needs a new human review. Prior review remains labelled.
    if old and old['data'].get('review'):d['review']=old['data']['review']
    d['history']=history[-5:]
    db.execute('INSERT INTO learner_projects VALUES(?,?,?,?) ON CONFLICT(learner) DO UPDATE SET revision=excluded.revision,content=excluded.content,updated=excluded.updated',(learner,revision+1,packed(d),time.time()))
    return get(db,learner)

def review(db,data):
    learner=text(data,'learner');record=get(db,learner)
    if not record or integer(data,'revision',0,10000000)!=record['revision']:fail('This project changed. Inspect the latest saved version before reviewing.')
    if not ready(record):fail('The learner needs a saved item, the four guided checks and their explanation first.')
    if data.get('demonstrated') is not True:fail('Watch the learner explain and change the app using their chosen supports.',400)
    d=record['data'];d['review']=dict(revision=record['revision']+1,note=text(data,'note',3,1000),at=time.time(),observed=True)
    db.execute('UPDATE learner_projects SET revision=revision+1,content=?,updated=? WHERE learner=?',(packed(d),time.time(),learner))
    return dict(ok=True)
