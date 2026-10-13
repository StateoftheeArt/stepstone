"""Bounded, explicitly device-reported practice; never a mastery/reward input."""
METHODS={'keyboard','phone','assistive'}
TARGETS={75,85,95,100}

def validate(records,unit,problem):
    if records is None:return []
    if not isinstance(records,list) or len(records)>20:raise problem(400,'Typing practice must be a short list of drill summaries.')
    # Older lab formats (such as reading-1's choice tasks) have no id or kind.
    tasks={t['id']:t for group in unit.get('mission',{}).get('labs',[]) for t in group if isinstance(t,dict) and t.get('kind')=='typing' and 'id' in t}
    result=[];seen=set()
    for r in records:
        if not isinstance(r,dict) or not isinstance(r.get('task'),str) or r['task'] not in tasks or r['task'] in seen:
            raise problem(400,'A typing summary must name a different drill in this module.')
        if set(r)!={'task','accuracy','target','method','assisted'}:raise problem(400,'Send only typing summary fields, not text or key logs.')
        if type(r['accuracy']) is not int or not 0<=r['accuracy']<=100 or type(r['target']) is not int or r['target'] not in TARGETS:
            raise problem(400,'Use a valid final-text percentage and practice target.')
        if not isinstance(r['method'],str) or r['method'] not in METHODS or type(r['assisted']) is not bool:
            raise problem(400,'Choose the input method used for practice.')
        if tasks[r['task']].get('exact') and r['target']!=100:raise problem(400,'This detail-checking exercise uses an exact-text target.')
        seen.add(r['task']);result.append(dict(r,assisted=r['assisted'] or r['method']=='assistive'))
    return result
