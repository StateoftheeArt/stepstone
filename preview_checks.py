"""Unseen device-preview checks; no account, database writes or Steps awards.

The browser retains its answers. The server returns only public questions when
starting a check and grades the submitted values against the private source bank.
"""
import random
import time
from copy import deepcopy
from check_sampling import sample_check,case

def handle(path,data,units,bank,public_question,correct,Problem):
    unit=data.get('unit')
    if not isinstance(unit,str) or unit not in units or unit not in bank:
        raise Problem(400,'This module is not ready yet.')
    if path=='/api/preview-check':
        questions=deepcopy(sample_check(bank[unit],units[unit].get('checkSkills',('calculate','apply','reason')),random.SystemRandom()))
        for question in questions:
            if question.get('options'):random.SystemRandom().shuffle(question['options'])
        random.SystemRandom().shuffle(questions)
        return dict(id='preview-'+str(time.time_ns()),remotePreview=True,unit=unit,questions=[public_question(q) for q in questions])
    ids=data.get('questions');answers=data.get('answers')
    if not isinstance(ids,list) or len(ids)!=6 or any(not isinstance(q,str) for q in ids) or len(set(ids))!=6:
        raise Problem(400,'Please reopen your six-question preview check.')
    by_id={q['id']:q for q in bank[unit]}
    if any(q not in by_id for q in ids):
        raise Problem(409,'This preview check uses an earlier lesson version. Your answers are still saved on this device.')
    questions=[by_id[q] for q in ids]
    if len({case(q) for q in questions})!=6:
        raise Problem(400,'Please use six different question cases.')
    if not isinstance(answers,dict) or set(answers)!=set(ids) or any(not isinstance(a,str) or not 0<len(a.strip())<=120 for a in answers.values()):
        raise Problem(400,'Please answer all six questions.')
    details=[public_question(q)|dict(answer=answers[q['id']],expected=q['answer'],correct=correct(q,answers[q['id']]),explanation=q['explanation']) for q in questions]
    score=sum(q['correct'] for q in details)
    return dict(score=score,total=6,passed=score>=5,points=0,at=time.time(),questions=details)
