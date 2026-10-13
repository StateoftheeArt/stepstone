"""Sample six distinct cases while preserving skill and lesson coverage."""

def case(question):
    return question.get('caseId',question['prompt'])

def sample_check(bank,skills,rng):
    chosen=[];used=set()
    quota=6//len(skills)
    for skill in skills:
        pool=list({case(q):q for q in bank if q['skill']==skill and case(q) not in used}.values())
        rng.shuffle(pool)
        first=[q for q in pool if q.get('lesson')==1]
        second=[q for q in pool if q.get('lesson')==2]
        pair=[first[0],second[0]] if first and second else pool[:quota]
        for question in pool:
            if len(pair)>=quota:break
            if case(question) not in {case(p) for p in pair}:pair.append(question)
        chosen.extend(pair);used.update(case(q) for q in pair)
    if len(chosen)<6:
        pool=list({case(q):q for q in bank if case(q) not in used}.values())
        rng.shuffle(pool);chosen.extend(pool[:6-len(chosen)])
    available={q.get('lesson') for q in bank}
    for lesson in (1,2):
        if lesson not in available or any(q.get('lesson')==lesson for q in chosen):continue
        # Sparse older banks may distribute lessons unevenly across skill labels.
        used={case(q) for q in chosen};replacement=False
        candidates=[q for q in bank if q.get('lesson')==lesson and case(q) not in used]
        rng.shuffle(candidates)
        for candidate in candidates:
            other=3-lesson
            other_count=sum(q.get('lesson')==other for q in chosen)
            index=next((i for i,q in enumerate(chosen) if q['skill']==candidate['skill'] and (q.get('lesson')!=other or other_count>1)),None)
            if index is not None:
                chosen[index]=candidate;replacement=True;break
        if not replacement:raise ValueError('Question bank cannot cover both lessons with its skill quotas.')
    if len(chosen)!=6 or len({case(q) for q in chosen})!=6:raise ValueError('Question bank needs six distinct cases.')
    return [dict(q) for q in chosen]
