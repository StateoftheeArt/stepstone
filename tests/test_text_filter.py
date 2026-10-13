"""PG-16 name and item filter: blocked disguises, innocent look-alikes, browser parity and API use."""
import base64
import json
import subprocess
import unittest
import test_server as base
import projects
from human_text import MESSAGE
from text_filter import acceptable

# Encoded so this file does not show offensive words as plain text.
BLOCKED = json.loads(base64.b64decode(
    'WyJGdWNrIiwgIkYuVS5DLksiLCAiZiB1IGMgayIsICJmdXV1dWNrIiwgImZ1IGNrIiwgIkYqY2siLCAiZioqayIsICJTaDF0IiwgIiRoaXQiLCAi'
    'YnVsbHNoIXQiLCAiQjF0Y2hlcyIsICJEdW1iZnVjayIsICJjIHUgbiB0IiwgIm1vdGhlcmZ1Y2tlciIsICJLaWxsIHlvdXJzZWxmIiwgImt5cyIs'
    'ICJTaWVnIEhlaWwiLCAiS0tLIiwgIkhpdGxlciIsICJOMWdnYSIsICJuaWcgZ2VyIiwgIkZhZyBnb3QiLCAicmV0YXJkZWQiLCAicGlwZSBib21i'
    'IiwgIlAwcm4iLCAiUG9ybmh1YiIsICJibG93IGpvYiIsICJSYXBpc3QiLCAiUFx1MDBlOWRvIiwgIlx1ZmY0Nlx1ZmY1NVx1ZmY0M1x1ZmY0YiIs'
    'ICJzbHV0dHkiLCAid2hvcmUiLCAiSGVudGFpIiwgIktpbGwgWW91ciBTZWxmIl0='))
# Real names, places and everyday items that contain or sit next to blocked letters.
ALLOWED = ['Scunthorpe','Red skin potatoes','White power bank','Cocktail napkins','Shiitake','Yamashita','Sussex','Therapist',
           'Pedometer','Rapeseed oil','Fire retardant','Dickinson','Cumming','Aryan','Isis','Sambo class','Honky-tonk night',
           'Kaffir lime leaves','Spick and span','Snigger','Niggardly','Bit chess set','Assassin','Class','Glass','Nazir',
           'Hancock','Peacock','Wankel engine','Pip','Nib','Laptop charger','***Star***','Save $20','Rock & roll','Élodie',
           'Chloë','Zoë','Mr. Jones','Mia B.','Ash','Grape','Scrap metal','Drink cartons','Bus pass','Math test','Bat cave']
BLOCKED += json.loads(base64.b64decode('WyJlYXQgYSBkaWNrIiwgImVhdCBhIGQxY2siLCAiZCBpIGMgayIsICJkaWNrcyJd'))


class TextFilterTests(unittest.TestCase):
    setUp = base.PilotTests.setUp
    tearDown = base.PilotTests.tearDown
    learner = base.PilotTests.learner

    def test_blocks_disguises_but_not_innocent_look_alikes(self):
        for text in BLOCKED:
            with self.subTest(blocked=len(text)): self.assertFalse(acceptable(text))
        for text in ALLOWED:
            with self.subTest(allowed=text): self.assertTrue(acceptable(text))
        self.assertTrue(acceptable(''));self.assertTrue(acceptable(None))

    def test_browser_filter_matches_the_server(self):
        script = """import {readFileSync} from 'node:fs';import {createTextFilter} from './public/text-filter.js';
const ok=createTextFilter(JSON.parse(readFileSync('public/text-filter.json','utf8')));let input='';for await(const c of process.stdin)input+=c;
console.log(JSON.stringify(JSON.parse(input).map(t=>ok(t))));"""
        samples = BLOCKED + ALLOWED + ['x' * 60 + '*', 'a*b*c*d', 'f*** off', 'sh*t', 'b * t c h', 'The Big Book of Fun']
        r = subprocess.run(['node', '--input-type=module', '-e', script], input=json.dumps(samples), text=True,
                           capture_output=True, encoding='utf-8', cwd=base.server.ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [acceptable(t) for t in samples])

    def test_refused_profile_name_keeps_identity_and_lesson_draft(self):
        client,me=self.learner('Sprout')
        draft=dict(phase=1,round=2,labStep=0,reflection='Synthetic saved draft',mission={},practiceRetries=0)
        saved=client.request('/api/draft',dict(unit='math-1',revision=0,data=draft))
        self.assertEqual(saved[0],200,saved[1])
        before=client.request('/api/me')[1]
        drafts=client.request('/api/drafts')[1]
        for name in (BLOCKED[-4], 'N'*17):
            status,result,_=client.request('/api/profile',dict(alias=name,avatar='octopus',accent='rose'))
            self.assertEqual(status,400,result)
            after=client.request('/api/me')[1]
            self.assertEqual(after['alias'],before['alias'])
            self.assertEqual(after['profile'],before['profile'])
            self.assertEqual(after['points'],before['points'])
            self.assertEqual(client.request('/api/drafts')[1],drafts)

    def test_names_items_rewards_and_preset_requests_keep_their_boundaries(self):
        bad = BLOCKED[0]
        code = self.mentor.request('/api/mentor/invite', {})[1]['code']
        status, result, _ = base.Client(self.url).request('/api/join', dict(code=code, alias=bad, share=True))
        self.assertEqual(status, 400); self.assertEqual(result['error'],MESSAGE)
        # The refused name did not use up the invitation.
        self.assertEqual(base.Client(self.url).request('/api/join', dict(code=code, alias='Ash', share=True))[0], 200)
        client, me = self.learner()
        for field in ('alias', 'companionName', 'nextWin'):
            self.assertEqual(client.request('/api/profile', {'avatar': 'fox', field: bad})[0], 400, field)
        self.assertEqual(client.request('/api/profile', dict(avatar='fox', alias='Ash', companionName='Pip'))[0], 200)
        plan = dict(kind='checklist', title='Game day kit', purpose='Pack for Saturday practice.', behaviours=['Add', 'Mark', 'Undo'], label='Item', limit=5, goal=1)
        self.assertEqual(client.request('/api/project/save', dict(revision=0, data=dict(plan, title=bad + ' kit')))[0], 400)
        self.assertEqual(client.request('/api/project/save', dict(revision=0, data=plan))[0], 200)
        revision = client.request('/api/me')[1]['project']['revision']
        status, result, _ = client.request('/api/project/add', dict(revision=revision, label=bad, value=''))
        self.assertEqual(status, 400); self.assertEqual(result['error'],MESSAGE)
        self.assertEqual(self.mentor.request('/api/mentor/reward', dict(title=bad, description='A test reward.', cost=20))[0], 400)
        self.assertEqual(base.Client(self.url).request('/api/mentor/setup', dict(username='second-mentor', name=bad, device='Laptop', passphrase='second-mentor-passphrase'))[0], 400)
        self.assertEqual(client.request('/api/messages/send', dict(clientId='filter-test-1', text='Someone called me ' + bad + ' today.'))[0], 400)
        self.assertEqual(client.request('/api/messages/send', dict(clientId='filter-test-2', choice='stuck'))[0], 200)
        # Offensive written work is rejected before a shared report or award is saved.
        attempt=client.request('/api/attempt',dict(unit='math-cash'))[1]
        reflection='Someone called me ' + bad + ' today.'
        result=client.request('/api/submit',dict(id=attempt['id'],answers=base.right_answers('math-cash',attempt),reflection=reflection,support='myself',ink=[]))
        self.assertEqual(result[0],400,result[1])
        self.assertEqual(result[1]['error'],MESSAGE)
        self.assertEqual(self.mentor.request('/api/mentor')[1]['reports'],[])

    def test_project_rules_match_the_browser_for_filtered_items(self):
        data = dict(kind='checklist', title='Game day kit', purpose='Pack for Saturday practice.', behaviours=['Add', 'Mark', 'Undo'], label='Item', limit=5, goal=1, items=[])
        try: projects.add(dict(data, items=[]), BLOCKED[0], ''); error = None
        except ValueError as e: error = str(e)
        script = """import {readFileSync} from 'node:fs';import {createTextFilter} from './public/text-filter.js';import {projectRules} from './public/project-runtime.js';
let input='';for await(const c of process.stdin)input+=c;const v=JSON.parse(input);
const filtered=projectRules(createTextFilter(JSON.parse(readFileSync('public/text-filter.json','utf8'))));
let error=null;try{filtered.add(v.data,v.label,'');}catch(e){error=e.message;}
const plain=projectRules();plain.add(v.data,v.label,'');
console.log(JSON.stringify({error,exported:v.data.items.length}));"""
        r = subprocess.run(['node', '--input-type=module', '-e', script], input=json.dumps(dict(data=data, label=BLOCKED[0])),
                           text=True, capture_output=True, encoding='utf-8', cwd=base.server.ROOT)
        self.assertEqual(r.returncode, 0, r.stderr)
        # Same message as the server; a downloaded copy of the app has no word list.
        self.assertEqual(json.loads(r.stdout), dict(error=error, exported=1))


if __name__ == '__main__': unittest.main()
