"""Versioned learner paths. Completion comes only from server-graded checks."""
import copy
import json


def validate(plan, units):
    if type(plan.get('version')) is not int or plan['version'] < 1:
        raise ValueError('A foundation path needs a positive integer version.')
    groups = plan.get('groups', [])
    if not groups or not isinstance(plan.get('title'), str):
        raise ValueError('A foundation path needs a title and groups.')
    group_ids, assigned = set(), set()
    for group in groups:
        if not group.get('id') or group['id'] in group_ids or not group.get('title'):
            raise ValueError('Foundation group IDs must be unique and titled.')
        group_ids.add(group['id'])
        if not group.get('units'):
            raise ValueError('A foundation group cannot be empty.')
        for unit in group['units']:
            if unit not in units or unit in assigned:
                raise ValueError('Foundation modules must exist and appear only once.')
            assigned.add(unit)
    return plan


def progress(plan, mastered):
    result = copy.deepcopy(plan)
    done = set(mastered)
    for group in result['groups']:
        group['passed'] = [unit for unit in group['units'] if unit in done]
        group['completed'] = len(group['passed'])
        group['total'] = len(group['units'])
    assigned = [unit for group in result['groups'] for unit in group['units']]
    result['completed'] = sum(group['completed'] for group in result['groups'])
    result['total'] = len(assigned)
    result['complete'] = result['completed'] == result['total']
    result['next'] = next((unit for unit in assigned if unit not in done), None)
    return result


def assigned_progress(db, learner, current, mastered):
    # A release must not silently change a learner's agreed path. Snapshots are
    # server-owned; neither draft data nor client-supplied completion is trusted.
    db.execute('INSERT OR IGNORE INTO foundation_paths(learner,content) VALUES(?,?)',
               (learner, json.dumps(current, ensure_ascii=False)))
    plan = json.loads(db.execute('SELECT content FROM foundation_paths WHERE learner=?',
                                (learner,)).fetchone()[0])
    return progress(plan, mastered)
