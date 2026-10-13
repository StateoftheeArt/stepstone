"""Authored mission copy and tasks; progress and scoring use the existing engine."""

ORDER_MISSION = dict(
    kind='order', label='Everyday numbers', tagline='Read the order. Pack it. Check it.',
    objectives=['Pack an order', 'Fix a mix-up', 'Run it yourself'],
    brief=['Put two groups together.', 'Fix a bag with too few or too many.', 'Try six fresh questions.'],
    startLabel='Take the order', artLabel='COUNT / PACK / CHECK',
    labLabel='Pack a practice order', backLabel='Back to the bag',
    practiceLabel='One order at a time.', recapLabel='Orders you worked out')

READING_PARTS = (
    'Find the words you need',
    'Read the whole message. Then ask: Where? When? What should I bring? Go back and find the words that tell you.',
    'Make a plan from a message, so you know where to go and what to bring.',
    'Meet Jo at the library at 4 pm. Bring a form.',
    ['Where? “At the library” names the place.', 'When? “At 4 pm” gives the time.',
     'What should I bring? “Bring a form” tells me.'],
    'Check before you go',
    'Plans can change. Read the new message. Keep the details that still apply. If something is missing, ask for it.',
    'New message: Meet at 5 pm instead. Same place. Bring the form.',
    ['“Instead” means use the new time: 5 pm.', '“Same place” means the library. I still need the form.',
     'If the message gives no time, ask: “What time should I come?”'], 'message')

def task(prompt, messages, options, answer, hint, why):
    return dict(prompt=prompt, messages=[dict(label=label, text=text) for label, text in messages],
                options=options, answer=answer, hint=hint, why=why)

_plan = [('From Jo', 'Meet Jo at the library at 4 pm. Bring a form.')]
_update = [('First plan', 'Meet Jo at the library at 4 pm. Bring a form.'),
           ('New message', 'Meet at 5 pm instead. Same place. Bring the form.')]

READING_MISSION = dict(
    kind='message', label='Everyday reading', tagline='Find the details. Check the plan.',
    objectives=['Find the details', 'Handle a change', 'Read it yourself'],
    brief=['Find the place, time, and thing to bring.', 'Check a change and ask for a missing detail.',
           'Try six fresh questions.'],
    startLabel='Open the message', artLabel='READ / CHECK / REPLY',
    labLabel='Read a practice message', backLabel='Back to the message',
    practiceLabel='One message at a time.', recapLabel='Messages you worked out',
    labs=[[
        task('Where will you meet Jo?', _plan,
             ['“at 4 pm”', '“at the library”', '“Bring a form”'], 1,
             'Where asks for a place. Find the place in the message.',
             '“At the library” tells you where to go.'),
        task('When will you meet?', _plan,
             ['“Bring a form”', '“at the library”', '“at 4 pm”'], 2,
             'When asks for a time. Find the time in the message.',
             '“At 4 pm” tells you when to meet.'),
        task('What should you bring?', _plan,
             ['“Bring a form”', '“Meet Jo”', '“at 4 pm”'], 0,
             'Find “Bring”. Read what comes after it.',
             '“Bring a form” names the thing you need. Now you have the full plan.')
    ], [
        task('Which time should you use now?', _update,
             ['4 pm', '5 pm', 'The new message gives no time.'], 1,
             'Read the new message. “Instead” replaces the old time.',
             'Use 5 pm. The new message changes the time from 4 pm to 5 pm.'),
        task('Which reply keeps the new plan?', _update,
             ['I will meet you at the library at 4 pm and bring the form.',
              'I will meet you at the shop at 5 pm and bring the form.',
              'I will meet you at the library at 5 pm and bring the form.'], 2,
             'Check three things: the place, the new time, and the form.',
             'The time changes to 5 pm. The library and the form stay in the plan.'),
        task('Another day, Jo sends this. What should you ask?',
             [('From Jo', 'Come to the library tomorrow. Bring the form.')],
             ['What time should I come?', 'Where should I go?', 'What should I bring?'], 0,
             'You know the place and what to bring. Which detail is missing?',
             'Ask for the time. “Tomorrow” gives a day, but it does not say what time to arrive.')
    ]])

_scenes = [
    ('Alex', 'the shop', 'a bag', 2, 3), ('Sam', 'the park gate', 'water', 3, 4),
    ('Lee', 'the sports centre', 'a towel', 5, 6), ('Ari', 'the bus stop', 'a pass', 2, 4),
    ('Kim', 'the hall', 'a notebook', 3, 5), ('Rae', 'the front desk', 'a form', 4, 6),
    ('Mo', 'the pool entrance', 'a towel', 1, 2), ('Max', 'the cafe', 'a bag', 2, 5),
    ('Ash', 'the main door', 'a key', 3, 6), ('Drew', 'the library', 'a book', 1, 4),
    ('Kai', 'the office', 'a pen', 2, 6), ('Pat', 'the community centre', 'water', 4, 5)
]

def reading_questions(index):
    name, place, item, old, new = _scenes[index % len(_scenes)]
    message = f'Meet {name} at {place} at {old} pm. Bring {item}.'
    field = index % 3
    prompts = ['Where should you go?', 'When should you meet?', 'What should you bring?']
    answers = [place, f'{old} pm', item]
    detail_hint = ['Where asks for a place.', 'When asks for a time.', 'Read the words after “Bring”.'][field]

    def question(prompt, passage, options, answer, why, hint, skill, lesson, case):
        return dict(kind='choice', prompt=prompt, passage=passage,
                    options=[dict(id=str(i), text=text) for i, text in enumerate(options)],
                    answer=str(answer), explanation=why, hint=hint, skill=skill,
                    lesson=lesson, caseId=f'message-{index}-{case}')

    return [
        question(prompts[field], message, answers, field,
                 f'The message gives the answer: {answers[field]}. {detail_hint}', detail_hint,
                 'calculate', 1, 'details'),
        question('Which plan matches the message?', message,
                 [f'Go to {place} at {old} pm and bring {item}.',
                  f'Go to {place} at {new} pm and bring {item}.',
                  f'Go to {place} at {old} pm. You do not need to bring anything.'], 0,
                 f'Keep all three details: {place}, {old} pm, and {item}.',
                 'Check the place, the time, and the thing to bring.', 'apply', 1, 'details'),
        question('Which plan follows the new message?',
                 f'First plan: {message}\nNew message: Meet at {new} pm instead. Same place. Bring {item}.',
                 [f'Meet at {old} pm at {place}. Bring {item}.',
                  f'Meet at {new} pm at {place}. Bring {item}.',
                  f'Meet at {new} pm at {place}. Bring nothing.'], 1,
                 f'“Instead” changes the time to {new} pm. The place and the thing to bring stay the same.',
                 'Read the new time. Then check which details stay the same.', 'apply', 2, 'change'),
        question('Which question asks for the missing detail?',
                 f'Meet {name} at {old} pm tomorrow. Bring {item}.' if field == 0 else
                 f'Meet {name} at {place} tomorrow. Bring {item}.' if field == 1 else
                 f'Meet {name} at {place} at {old} pm tomorrow. Bring what you need for the task.',
                 ['Where should I meet you?', 'What time should I come?', 'What should I bring?'], field,
                 ['The time and item are given. Ask where to meet.',
                  'The place and item are given. Ask what time to meet.',
                  'The place and time are given. Ask which things you need to bring.'][field],
                 'Check what the message tells you. Ask for the detail it leaves out.', 'reason', 2, 'gap')
    ]
