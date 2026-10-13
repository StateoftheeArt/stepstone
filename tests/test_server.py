import concurrent.futures
import http.cookiejar
import json
import math
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server

class Client:
    def __init__(self,url):
        self.url=url;self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def request(self,path,data=None,headers=None):
        req=urllib.request.Request(self.url+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
        try:
            with self.opener.open(req,timeout=20) as r: return r.status,json.loads(r.read()),r.headers
        except urllib.error.HTTPError as r:
            raw=r.read()
            try: value=json.loads(raw)
            except ValueError: value={}
            return r.code,value,r.headers


def right_answers(unit,attempt):
    """Correct answers for an attempt. Choice ids are shuffled positions, so match the authored option text."""
    bank={q['id']:q for q in server.BANK[unit]};answers={}
    for q in attempt['questions']:
        b=bank[q['id']]
        if b['kind']=='choice':
            text=next(o['text'] for o in b['options'] if o['id']==b['answer'])
            answers[q['id']]=next(o['id'] for o in q['options'] if o['text']==text)
        else: answers[q['id']]=str(b['answer'])
    return answers


def complete_tutorial(client):
    # Explicit fixture for tests of unrelated features. UI coverage walks controls.
    data=dict(version=1,events=[dict(action=a,**({'value':7} if a=='pack' else {'value':'3'} if a=='answer' else {})) for a in server.TUTORIAL['actions']])
    status,record,_=client.request('/api/tutorial',dict(revision=0,data=data))
    if status != 200: raise AssertionError(record)
    return record

def complete_core_fixture(app,client):
    """Explicit first-four-course prerequisites for unrelated feature tests.

    These zero-point authored records live only in disposable test databases.
    Dedicated readiness tests use direct requests to exercise the locked state.
    """
    from course_access import required_units
    _,me,_=client.request('/api/me')
    with app.store.db() as db:
        for unit in required_units(server.CATALOG):
            report=dict(passed=True,score=6,total=6,at=1,title=server.UNITS[unit]['title'],unit=unit,
                        questions=[],reflection='Synthetic course prerequisite',support='myself',ink=[],points=0,tryNumber=1,practiceRetries=0)
            db.execute('INSERT OR IGNORE INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                       ('core-fixture-'+me['id']+'-'+unit,me['id'],unit,'[]',1,1,json.dumps(report)))

class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='stepstone-api-')
        self.app=server.create_server(port=0,data=self.tmp.name)
        self.thread=threading.Thread(target=self.app.serve_forever,daemon=True);self.thread.start()
        self.url=f'http://127.0.0.1:{self.app.server_address[1]}'
        self.mentor=Client(self.url)
        status,self.account_setup,_=self.mentor.request('/api/mentor/setup',{'username':'test-mentor','name':'Test mentor','device':'Test device','passphrase':'test-only-mentor-passphrase','claimExisting':True})
        self.assertEqual(status,200,self.account_setup)
    def tearDown(self):
        self.app.shutdown();self.app.server_close();self.thread.join();self.tmp.cleanup()
    def learner(self,alias='Practice learner',tutorial=True):
        code=self.mentor.request('/api/mentor/invite',{})[1]['code']
        client=Client(self.url);status,result,_=client.request('/api/join',dict(code=code,alias=alias,share=True))
        self.assertEqual(status,200)
        if tutorial: complete_tutorial(client)
        return client,result
    def check(self,client,unit='math-cash',wrong=0):
        if server.UNITS[unit]['subject'] in ('digital','work'):complete_core_fixture(self.app,client)
        status,attempt,_=client.request('/api/attempt',{'unit':unit});self.assertEqual(status,200)
        answers=right_answers(unit,attempt)
        for q in attempt['questions'][:wrong]: answers[q['id']]=next(o['id'] for o in q['options'] if o['id']!=answers[q['id']]) if q['kind']=='choice' else '99999'
        payload=dict(id=attempt['id'],answers=answers,reflection='I added the change back to the price to check the total.',support='myself',ink=[[[.1,.2],[.3,.4]]],practiceRetries=2)
        status,result,_=client.request('/api/submit',payload);self.assertEqual(status,200)
        return result,payload
    def test_private_boundaries_and_static_allowlist(self):
        guest=Client(self.url)
        for path in ('/api/mentor','/api/me'): self.assertEqual(guest.request(path)[0],401)
        for path in ('/content/checkpoints.json','/data/stepstone.sqlite3','/server.py','/vendor/'):
            self.assertEqual(guest.request(path)[0],404)
        status,health,headers=guest.request('/api/health');self.assertEqual(health['app'],'stepstone');self.assertEqual(headers['Cache-Control'],'no-store')
    def test_origin_and_host_checks(self):
        self.assertEqual(self.mentor.request('/api/mentor/invite',{},headers={'Origin':'https://unrelated.example'})[0],403)
        self.assertEqual(self.mentor.request('/api/mentor/invite',{},headers={'Host':'unrelated.example'})[0],403)
    def test_setup_only_once_and_password_is_not_plaintext(self):
        self.assertEqual(Client(self.url).request('/api/mentor/setup',{'username':'test-mentor','name':'Test','device':'Test device','passphrase':'another-test-passphrase'})[0],409)
        self.assertEqual(Client(self.url).request('/api/mentor/login',{'username':'test-mentor','device':'Test device','passphrase':'wrong-test-passphrase'})[0],401)
        with self.app.store.db() as db: value=db.execute("SELECT value FROM settings WHERE key='mentor'").fetchone()[0]
        self.assertNotIn('test-only-mentor-passphrase',value);self.assertIn('salt',value)
    def test_invite_is_single_use_and_sharing_is_disclosed(self):
        code=self.mentor.request('/api/mentor/invite',{})[1]['code'];guest=Client(self.url)
        self.assertEqual(guest.request('/api/join',dict(code=code,alias='Test',share=False))[0],400)
        self.assertEqual(guest.request('/api/join',dict(code=code,alias='Test',share=True))[0],200)
        self.assertEqual(Client(self.url).request('/api/join',dict(code=code,alias='Another',share=True))[0],400)
    def test_cross_device_sign_in_and_recovery_rotation(self):
        first,me=self.learner();other=Client(self.url)
        self.assertEqual(other.request('/api/login',{'code':me['recovery']})[1]['id'],me['id'])
        code=self.mentor.request('/api/mentor/recovery',{'id':me['id']})[1]['code']
        self.assertEqual(first.request('/api/me')[0],401);self.assertEqual(other.request('/api/me')[0],401)
        self.assertEqual(other.request('/api/login',{'code':me['recovery']})[0],401)
        self.assertEqual(other.request('/api/login',{'code':code})[0],200)
    def test_server_grades_and_delivers_evidence(self):
        client,me=self.learner();result,payload=self.check(client,wrong=1)
        self.assertEqual(result['report']['score'],5);self.assertTrue(result['report']['passed']);self.assertEqual(result['me']['points'],20)
        record=self.mentor.request('/api/mentor')[1]['reports'][0]
        self.assertEqual(record['report']['reflection'],payload['reflection']);self.assertEqual(record['report']['ink'],payload['ink'])
        self.assertEqual(len(record['report']['questions']),6)
        self.mentor.request('/api/mentor/review',dict(id=record['id'],note='Good check. Try changing the price next.'))
        self.assertEqual(client.request('/api/me')[1]['attempts'][0]['note'],'Good check. Try changing the price next.')
    def test_failed_test_then_pass_does_not_double_award(self):
        client,_=self.learner();first,_=self.check(client,wrong=2)
        self.assertFalse(first['report']['passed']);self.assertEqual(first['me']['points'],5)
        second,payload=self.check(client);self.assertEqual(second['report']['points'],15)
        duplicate=client.request('/api/submit',payload)[1];self.assertEqual(duplicate['me']['points'],20)
        third,_=self.check(client);self.assertEqual(third['report']['points'],0);self.assertEqual(third['me']['points'],20)
        self.assertEqual(len(self.mentor.request('/api/mentor')[1]['reports']),3)
    def test_attempt_is_owned_and_resume_does_not_reveal_answer(self):
        first,_=self.learner();second,_=self.learner('Second')
        a=first.request('/api/attempt',dict(unit='math-1'))[1]
        self.assertEqual(first.request('/api/attempt',dict(unit='math-1'))[1]['id'],a['id'])
        self.assertTrue(all('answer' not in q and 'explanation' not in q for q in a['questions']))
        self.assertEqual(second.request('/api/submit',dict(id=a['id']))[0],404)
        self.assertEqual(second.request('/api/mentor/invite',{})[0],401)
    def test_short_answer_and_ink_validation(self):
        client,_=self.learner();a=client.request('/api/attempt',dict(unit='math-1'))[1]
        self.assertEqual(client.request('/api/submit',dict(id=a['id'],answers={}))[0],400)
        with self.assertRaises(server.Problem): server.valid_ink([[[float('nan'),.2]]])
        with self.assertRaises(server.Problem): server.valid_ink([[[2,.2]]])
        self.assertEqual(server.numeric('3/4'),.75);self.assertIsNone(server.numeric('1/0'));self.assertIsNone(server.numeric('1e309'));self.assertIsNone(server.numeric('2+2'))
        self.assertTrue(server.correct(dict(kind='number',answer=6.25),'6.250'))
        # Everyday money, percent and thousands formats; words still get a format hint. Mirrors test_content.cjs.
        for text,value in [('$10',10),('10 CAD',10),('CAD 6,000',6000),('10,000',10000),('10 000',10000),('25%',25),('10 dollars',10),('-$5',-5),('$2.75',2.75),('3/4',.75),('1,5',None),('12,3456',None),('three',None),('$',None),('',None)]:
            self.assertEqual(server.numeric(text),value,text);self.assertEqual(server.placement_numeric(text),value,text)
        self.assertFalse(server.correct(dict(kind='number',answer=.01),'0'))
    def test_practice_location_can_move_back_without_losing_mastery(self):
        client,_=self.learner();self.check(client)
        for stage in (5,1): self.assertEqual(client.request('/api/progress',dict(unit='math-cash',stage=stage))[0],200)
        me=client.request('/api/me')[1];self.assertEqual(me['progress']['math-cash'],1);self.assertTrue(me['attempts'][0]['report']['passed'])
    def test_reward_points_and_refund_are_atomic_and_idempotent(self):
        client,_=self.learner();self.check(client)
        rid=self.mentor.request('/api/mentor/reward',dict(title='Choose an activity',description='Choose a group activity together.',cost=20))[1]['id']
        for _ in range(2): self.assertEqual(client.request('/api/reward',{'id':rid})[0],200)
        me=client.request('/api/me')[1];self.assertEqual(me['points'],0);self.assertEqual(len(me['claims']),1)
        claim=me['claims'][0]['id']
        self.assertEqual(client.request('/api/reward',{'id':'theme-ocean'})[0],200)
        self.assertEqual(client.request('/api/me')[1]['points'],0)  # Colours are free.
        for _ in range(2): self.assertEqual(self.mentor.request('/api/mentor/claim',dict(id=claim,status='declined',note='Let us pick another option.'))[0],200)
        self.assertEqual(client.request('/api/me')[1]['points'],20)
        self.assertEqual(self.mentor.request('/api/mentor/claim',dict(id=claim,status='given',note=''))[0],409)
    def test_reward_approval_then_given(self):
        client,_=self.learner();self.check(client)
        rid=self.mentor.request('/api/mentor/reward',dict(title='A notebook',description='A notebook selected with the mentor.',cost=10))[1]['id']
        claim=client.request('/api/reward',{'id':rid})[1]['me']['claims'][0]['id']
        for status in ('approved','given'): self.assertEqual(self.mentor.request('/api/mentor/claim',dict(id=claim,status=status,note='We will arrange it together.'))[0],200)
        self.assertEqual(client.request('/api/me')[1]['claims'][0]['status'],'given')
    def test_delayed_review_reward_uses_server_history(self):
        client,me=self.learner();first,_=self.check(client)
        with self.app.store.db() as db:
            a=db.execute('SELECT id,report FROM attempts WHERE learner=?',(me['id'],)).fetchone();report=json.loads(a['report']);report['at']-=8*86400
            db.execute('UPDATE attempts SET report=? WHERE id=?',(json.dumps(report),a['id']))
        result,_=self.check(client);self.assertTrue(result['report']['review']);self.assertEqual(result['report']['points'],5)
        result,_=self.check(client);self.assertFalse(result['report']['review']);self.assertEqual(result['report']['points'],0)
    def test_all_modules_offer_six_distinct_questions_and_no_duplicate_options(self):
        client,_=self.learner();complete_core_fixture(self.app,client)
        for uid,questions in server.BANK.items():
            with self.subTest(unit=uid):
                status,attempt,_=client.request('/api/attempt',{'unit':uid});self.assertEqual(status,200)
                self.assertEqual(len(attempt['questions']),6);self.assertEqual(len({(q.get('passage',''),q['prompt']) for q in attempt['questions']}),6)
                for q in questions:
                    if q['kind']=='choice': self.assertEqual(len({o['text'] for o in q['options']}),len(q['options']))
    def test_every_module_accepts_a_submitted_check(self):
        # The browser always sends typingPractice, including modules without typing drills.
        client,_=self.learner();complete_core_fixture(self.app,client)
        for unit in server.BANK:
            with self.subTest(unit=unit):
                status,attempt,_=client.request('/api/attempt',{'unit':unit});self.assertEqual(status,200)
                answers={q['id']:q['options'][0]['id'] if q['kind']=='choice' else '1' for q in attempt['questions']}
                status,result,_=client.request('/api/submit',dict(id=attempt['id'],answers=answers,reflection='I checked each step.',support='myself',typingPractice=[]))
                if unit=='app-build': self.assertEqual(status,400,result)  # A saved working app comes first.
                else: self.assertEqual(status,200,result);self.assertEqual(result['report']['total'],6)
    def test_choice_ids_follow_shuffled_positions(self):
        client,_=self.learner();complete_core_fixture(self.app,client);first=0;total=0
        for unit in server.BANK:
            attempt=client.request('/api/attempt',{'unit':unit})[1]
            with self.app.store.db() as db: stored=json.loads(db.execute('SELECT questions FROM attempts WHERE id=?',(attempt['id'],)).fetchone()[0])
            bank={q['id']:q for q in server.BANK[unit]}
            for q in stored:
                if q['kind']!='choice': continue
                authored=next(o['text'] for o in bank[q['id']]['options'] if o['id']==bank[q['id']]['answer'])
                self.assertEqual([o['id'] for o in q['options']],[str(i) for i in range(len(q['options']))])
                self.assertEqual(q['options'][int(q['answer'])]['text'],authored)
                first+=q['answer']=='0';total+=1
        # Authored banks put the answer first almost every time. Shuffled positions must not.
        self.assertGreater(total,200);self.assertLess(first/total,.6)

if __name__=='__main__': unittest.main()
