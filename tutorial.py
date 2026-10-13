"""Replay required setup actions. Bonus awards are handled by the server ledger."""
from placement import numeric


def evaluate(config, data):
    if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] not in (1, 2):
        raise ValueError('Please reopen your saved tour.')
    events = data.get('events')
    actions = config['setupActions'] if data['version'] == 2 else config['actions']
    if not isinstance(events, list) or len(events) > len(actions):
        raise ValueError('Please follow the tour one step at a time.')
    clean_events = []
    for index, event in enumerate(events):
        if not isinstance(event, dict) or event.get('action') != actions[index]:
            raise ValueError('Please follow the tour one step at a time.')
        action = event['action']
        clean = dict(action=action)
        if action == 'pack':
            if type(event.get('value')) is not int or event['value'] != config['target']:
                raise ValueError('Match the bag to the order, then check it.')
            clean['value'] = event['value']
        if action == 'answer':
            if numeric(event.get('value')) != config['question']['answer']:
                raise ValueError('Use the helpful step, then check the practice answer.')
            clean['value'] = event['value']
        if action == 'mentor':
            if event.get('value') not in ('connected', 'device'):
                raise ValueError('Choose how to save your learning.')
            clean['value'] = event['value']
        if action == 'goal':
            if event.get('value') not in ('core-card-everyday', 'card-exchange', 'core-laptop'):
                raise ValueError('Choose your reward goal.')
            clean['value'] = event['value']
        clean_events.append(clean)
    count = data.get('count', 4)
    answer = data.get('answer', '')
    if type(count) is not int or not 0 <= count <= 12:
        raise ValueError('Please check the practice bag.')
    if not isinstance(answer, str) or len(answer) > 120:
        raise ValueError('Please check the practice answer.')
    for flag in ('bagChecked', 'answerChecked', 'hint'):
        if type(data.get(flag, False)) is not bool:
            raise ValueError('Please reopen your saved tour.')
    # A changed input cannot retain a successful check.
    clean = dict(version=data['version'], events=clean_events, count=count, answer=answer,
                 bagChecked=data.get('bagChecked', False) and count == config['target'],
                 answerChecked=data.get('answerChecked', False) and numeric(answer) == config['question']['answer'],
                 hint=data.get('hint', False))
    result = dict(step=len(events), total=len(actions), complete=len(events) == len(actions))
    return clean, result
