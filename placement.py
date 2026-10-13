"""Replay informal starting suggestions, not grades or a standardized assessment.

Each v2 area requires repeated evidence before changing difficulty. Age and
read-aloud use never change routing. Writing is saved for human review only.
Keep this deterministic replay in step with public/engine.js. Retain v1 replay
so existing learners can resume their original check without losing answers.
"""
import math
import re


def evaluate(bank, data):
    if not isinstance(data, dict):
        raise ValueError('Please start with your age.')
    age, seed, answers = data.get('age'), data.get('seed'), data.get('answers')
    if type(age) is not int or not 5 <= age <= 99:
        raise ValueError('Enter your age as a whole number from 5 to 99.')
    if type(seed) is not int or not 0 <= seed <= 65535:
        raise ValueError('Please restart the starting check.')
    version = data.get('version', 1)
    if type(version) is not int or version not in (1, 2, 3, 4, 5):
        raise ValueError('Please reopen your saved starting check.')
    if not isinstance(answers, list) or len(answers) > ({1:10, 2:36, 3:24, 4:48,5:24}[version]):
        raise ValueError('There are too many answers in this starting check.')
    if version == 1:
        return legacy(bank.get('legacy', bank), data)
    replay_bank = bank['foundation'] if version==5 else bank['extended'] if version==4 else bank
    result = extended(replay_bank, data, version=version) if version in (4,5) else adaptive(bank, data)
    validate_draft(replay_bank, data, result)
    return result


def legacy(bank, data):
    seed, answers = data['seed'], data['answers']
    levels, details = {}, []
    first_correct = False
    for index in range(11):
        if index == 10:
            return dict(complete=True, levels=levels,
                        average=math.floor(sum(levels.values()) / 5 + .5),
                        evidence=details, next=None)
        subject = bank['subjects'][index // 2]
        grade = 6 if index % 2 == 0 else (9 if first_correct else 3)
        variants = [q for q in bank['questions'] if q['subject'] == subject and q['grade'] == grade]
        question = variants[(seed + index) % len(variants)]
        if index == len(answers):
            return dict(complete=False, levels=levels, average=None, evidence=details, next=question['id'])
        item = answers[index]
        if (not isinstance(item, dict) or item.get('id') != question['id'] or
            type(item.get('answer')) is not int or not -1 <= item['answer'] < len(question['options']) or
            type(item.get('heard', False)) is not bool):
            raise ValueError('That answer does not match the next question. Reload your saved check.')
        right = item['answer'] == question['answer']
        details.append(dict(id=question['id'], subject=subject, grade=grade,
                            answer=item['answer'], correct=right, heard=item.get('heard', False)))
        if index % 2 == 0:
            first_correct = right
        else:
            levels[subject] = (10 if right else 7) if first_correct else (4 if right else 1)


def plain_number(value):
    """Accept everyday formats: $10, 10 CAD, 10 dollars, 25%, 10,000 or 10 000. Matches engine.js plainNumber."""
    value = value.strip().replace('−', '-')
    value = re.sub(r'^([+-]?)\s*(?:CAD|C\$|\$)\s*', r'\1', value, flags=re.I)
    value = re.sub(r'\s*(?:CAD|\$|%|dollars?)$', '', value, flags=re.I)
    if re.fullmatch(r'[+-]?[0-9]{1,3}(?:(?:,[0-9]{3})+|(?:[ \u00a0\u202f][0-9]{3})+)(?:\.[0-9]*)?', value):
        value = re.sub(r'[, \u00a0\u202f]', '', value)
    return value


def numeric(value):
    if not isinstance(value, str) or len(value) > 80:
        return None
    value = plain_number(value)
    part = r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)'
    if not re.fullmatch(part + r'(?:\s*/\s*' + part + r')?', value):
        return None
    parts = [float(p) for p in value.split('/')]
    if len(parts) == 2 and parts[1] == 0:
        return None
    value = parts[0] / parts[1] if len(parts) == 2 else parts[0]
    return value if math.isfinite(value) else None


def adaptive(bank, data):
    levels, areas, evidence = {}, {}, []
    answers, seed, cursor = data['answers'], data['seed'], 0
    fixed = data.get('version') == 3
    limit = 4 if fixed else 6
    for section, subject in enumerate(bank['subjects']):
        band, confirmed = 1, -1
        asked, hits, misses, failed = [0]*4, [0]*4, [0]*4, set()
        details = []
        for step in range(limit):
            variants = [q for q in bank['questions'] if q['subject'] == subject and q['band'] == band]
            question = variants[(seed + section*7 + band + asked[band]) % len(variants)]
            if cursor == len(answers):
                return dict(complete=False, questionsDone=False, levels=levels, areas=areas,
                            evidence=evidence, next=question['id'], section=subject,
                            sectionIndex=section, questionInSection=step+1)
            item = answers[cursor]
            if (not isinstance(item, dict) or item.get('id') != question['id'] or
                'answer' not in item or type(item.get('heard', False)) is not bool):
                raise ValueError('That answer does not match the next question. Reload your saved check.')
            answer, unsure = item['answer'], item['answer'] is None
            if unsure:
                right = False
            elif question['kind'] == 'number':
                value = numeric(answer)
                if value is None:
                    raise ValueError('Enter a number, decimal or fraction, or choose “I don’t know yet”.')
                right = abs(value-question['answer']) <= max(1e-9, abs(question['answer'])*1e-6)
            else:
                if type(answer) is not int or not 0 <= answer < len(question['options']):
                    raise ValueError('Choose one of the answers shown.')
                right = answer == question['answer']
            detail = dict(id=question['id'], subject=subject, band=band, answer=answer,
                          correct=right, unsure=unsure, heard=item.get('heard', False))
            details.append(detail)
            evidence.append(detail)
            cursor += 1
            asked[band] += 1
            hits[band] += int(right)
            misses[band] += int(not right)
            done = False
            if hits[band] >= 2:
                confirmed = max(confirmed, band)
                done = band == 3 or band+1 in failed
                if not done:
                    band += 1
            elif misses[band] >= 2:
                failed.add(band)
                done = confirmed >= 0 or band == 0
                if not done:
                    band -= 1
            if (done and not fixed) or step == limit - 1:
                level = bank['starts'][subject][max(0, confirmed)]
                levels[subject] = level
                areas[subject] = dict(level=level, confirmedBand=confirmed, answered=len(details),
                                      matched=sum(d['correct'] for d in details),
                                      unsure=sum(d['unsure'] for d in details),
                                      heard=sum(d['heard'] for d in details),
                                      basis='support' if confirmed < 0 else 'steady' if done and not fixed else 'check-in')
                break
    if cursor != len(answers):
        raise ValueError('This starting check already has all its answers.')
    writing = data.get('writing', {})
    if not isinstance(writing, dict):
        raise ValueError('Please check your short message.')
    return dict(complete=fixed or writing.get('status') in ('submitted', 'skipped'), questionsDone=True,
                levels=levels, areas=areas, evidence=evidence, next=None,
                section=None, sectionIndex=len(bank['subjects']), questionInSection=0)


def extended(bank, data, version=4):
    """Eight fresh tasks per course, repeated evidence in different skills.

    This is an informal routing rule, not a calibrated ability score. Two
    misses cap an area's difficulty for this check. No age or reading penalty.
    """
    levels, areas, suggestions, evidence = {}, {}, {}, []
    answers, seed, cursor = data['answers'], data['seed'], 0
    bands=3 if version==5 else 4
    steps=6 if version==5 else 8
    for section, subject in enumerate(bank['subjects']):
        band = 0 if version==5 else 1
        hits, misses = [0]*bands, [0]*bands
        hit_skills = [set() for _ in range(bands)]
        failed, used, skill_asked, details = set(), set(), {}, []
        for step in range(steps):
            unused = [q for q in bank['questions'] if q['subject'] == subject and q['id'] not in used]
            variants = [q for q in unused if q['band'] == band]
            if not variants:
                nearest = min(unused, key=lambda q:(abs(q['band']-band), q['band']))['band']
                variants = [q for q in unused if q['band'] == nearest]
            fewest = min(skill_asked.get((q['band'],q['skill']),0) for q in variants)
            variants = [q for q in variants if skill_asked.get((q['band'],q['skill']),0) == fewest]
            question = variants[(seed+section*11+step) % len(variants)]
            band = question['band']
            if cursor == len(answers):
                return dict(version=version, complete=False, questionsDone=False, levels=levels, areas=areas,
                            suggestions=suggestions, evidence=evidence, next=question['id'],
                            section=subject, sectionIndex=section, questionInSection=step+1)
            item = answers[cursor]
            if (not isinstance(item,dict) or item.get('id') != question['id'] or
                'answer' not in item or type(item.get('heard',False)) is not bool):
                raise ValueError('That answer does not match the next question. Reload your saved check.')
            answer, unsure = item['answer'], item['answer'] is None
            if unsure:
                right = False
            elif question['kind'] == 'number':
                value = numeric(answer)
                if value is None:
                    raise ValueError('Enter a number, decimal or fraction, or choose “I don’t know yet”.')
                right = abs(value-question['answer']) <= max(1e-9,abs(question['answer'])*1e-6)
            else:
                if type(answer) is not int or not 0 <= answer < len(question['options']):
                    raise ValueError('Choose one of the answers shown.')
                right = answer == question['answer']
            detail = dict(id=question['id'],subject=subject,band=band,skill=question['skill'],answer=answer,
                          correct=right,unsure=unsure,heard=item.get('heard',False))
            details.append(detail);evidence.append(detail);cursor += 1;used.add(question['id'])
            skill_key=(band,question['skill']);skill_asked[skill_key]=skill_asked.get(skill_key,0)+1
            hits[band] += int(right);misses[band] += int(not right)
            if right:hit_skills[band].add(question['skill'])
            if misses[band] >= 2:
                failed.add(band)
                lower=[i for i in range(band) if i not in failed]
                band=max(lower,default=0)
            elif hits[band] >= 2 and len(hit_skills[band]) >= 2 and hits[band] > misses[band]:
                if band < bands-1 and band+1 not in failed and (version==4 or band not in failed):band += 1
        steady=[i not in failed and hits[i]>=2 and len(hit_skills[i])>=2 and hits[i]>misses[i] for i in range(bands)]
        confirmed=max((i for i in range(bands) if steady[i] and (version==4 or all(steady[:i+1]))),default=-1)
        level=bank['starts'][subject][max(0,confirmed)]
        levels[subject]=level;suggestions[subject]=bank['suggestions'][subject][max(0,confirmed)]
        areas[subject]=dict(level=level,confirmedBand=confirmed,answered=steps,matched=sum(d['correct'] for d in details),
                            unsure=sum(d['unsure'] for d in details),heard=sum(d['heard'] for d in details),
                            basis='support' if confirmed<0 else 'steady',
                            bands=[dict(band=i,matched=hits[i],revisit=misses[i],skills=len(hit_skills[i])) for i in range(bands)])
    if cursor != len(answers):
        raise ValueError('This starting check already has all its answers.')
    writing=data.get('writing',{})
    if not isinstance(writing,dict):raise ValueError('Please check your short message.')
    return dict(version=version,complete=writing.get('status') in ('submitted','skipped'),questionsDone=True,
                levels=levels,areas=areas,suggestions=suggestions,evidence=evidence,next=None,
                section=None,sectionIndex=len(bank['subjects']),questionInSection=0)


def validate_draft(bank, data, result):
    if 'draft' in data:
        draft = data['draft']
        if (not isinstance(draft, dict) or not result['next'] or draft.get('id') != result['next'] or
            'answer' not in draft or type(draft.get('heard', False)) is not bool):
            raise ValueError('That saved answer belongs to a different question.')
        question = next(q for q in bank['questions'] if q['id'] == result['next'])
        value = draft['answer']
        if value is not None:
            valid = (isinstance(value, str) and len(value) <= 80) if question['kind'] == 'number' else (
                type(value) is int and 0 <= value < len(question['options']))
            if not valid:
                raise ValueError('Please check your saved answer.')
    if 'writing' in data:
        writing = data['writing']
        if (not result['questionsDone'] or not isinstance(writing, dict) or
            writing.get('status') not in ('draft', 'submitted', 'skipped') or
            not isinstance(writing.get('text'), str) or len(writing['text']) > 1000 or
            writing.get('support', 'myself') not in ('myself', 'person', 'tool', 'mixed') or
            type(writing.get('heard', False)) is not bool or
            (writing['status'] == 'submitted' and not writing['text'].strip())):
            raise ValueError('Write a short message, or choose “Not ready to write yet”.')


def normalize(data):
    """Call only after evaluate. Store understood inputs, never client results."""
    content = {k:data[k] for k in ('age', 'seed', 'answers')}
    content['answers'] = [dict(id=a['id'], answer=a['answer'], heard=a.get('heard', False)) for a in data['answers']]
    if data.get('version', 1) in (2, 3, 4, 5):
        content['version'] = data['version']
        if 'draft' in data:
            draft = data['draft']
            content['draft'] = dict(id=draft['id'], answer=draft['answer'], heard=draft.get('heard', False))
        if 'writing' in data:
            writing = data['writing']
            content['writing'] = dict(text=writing['text'], status=writing['status'],
                                      support=writing.get('support', 'myself'), heard=writing.get('heard', False))
    return content
