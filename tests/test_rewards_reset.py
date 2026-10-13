import concurrent.futures
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import test_server as base
Client=base.Client
server=base.server

class MilestoneTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner
    check=base.PilotTests.check

    def offer(self,**changes):
        body=dict(title='Synthetic gift card',description='Synthetic offer only; no value issued.',cost=10,category='giftcard',stock=0)
        body.update(changes)
        # Earlier agreements retain their published terms. New funded cards and
        # laptops use the stable program, covered in test_funded_program.py.
        rid=server.uid()
        with self.app.store.db() as db:
            db.execute('INSERT INTO rewards(id,title,description,cost,kind,category,stock,minimum_modules,required_modules) VALUES(?,?,?,?,?,?,?,?,?)',
                       (rid,body['title'],body['description'],body['cost'],'mentor',body['category'],body['stock'],body.get('minimum_modules',0),json.dumps(body.get('required_modules',[]))))
        return rid

    def test_funding_and_module_requirements_are_server_enforced(self):
        person,me=self.learner()
        self.check(person)
        reward=self.offer(minimum_modules=2,required_modules=['digital-4'])
        self.assertEqual(person.request('/api/reward-goal',dict(id=reward))[0],200)
        self.assertEqual(person.request('/api/reward',dict(id=reward,mastered=['digital-4']))[0],409)
        self.assertEqual(person.request('/api/me')[1]['points'],20)
        self.assertEqual(self.mentor.request('/api/mentor/reward-stock',dict(id=reward,stock=1,expectedStock=0))[0],200)
        self.assertEqual(person.request('/api/reward',dict(id=reward))[0],409)
        self.check(person,'digital-4')
        result=person.request('/api/reward',dict(id=reward))
        self.assertEqual(result[0],200);self.assertEqual(result[1]['me']['points'],30)
        self.assertEqual(next(r for r in result[1]['me']['rewards'] if r['id']==reward)['available'],0)

    def test_two_learners_cannot_claim_one_item_and_decline_releases_once(self):
        a,ma=self.learner('A');b,mb=self.learner('B')
        self.check(a);self.check(b);reward=self.offer(stock=1)
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results=list(pool.map(lambda c:c.request('/api/reward',dict(id=reward)),[a,b]))
        self.assertEqual(sorted(x[0] for x in results),[200,409])
        winner,loser=(a,b) if results[0][0]==200 else (b,a)
        win=winner.request('/api/me')[1];claim=next(c for c in win['claims'] if c['reward']==reward)
        self.assertEqual(win['points'],10);self.assertEqual(loser.request('/api/me')[1]['points'],20)
        winner.request('/api/reward',dict(id=reward))
        self.assertEqual(winner.request('/api/me')[1]['points'],10)
        for _ in range(2):self.assertEqual(self.mentor.request('/api/mentor/claim',dict(id=claim['id'],status='declined',note='Synthetic decline.'))[0],200)
        self.assertEqual(winner.request('/api/me')[1]['points'],20)
        self.assertEqual(loser.request('/api/reward',dict(id=reward))[0],200)
        self.assertEqual(self.mentor.request('/api/mentor/reward-stock',dict(id=reward,stock=0,expectedStock=1))[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/reward-stock',dict(id=reward,stock=2,expectedStock=0))[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/reward-stock',dict(id=reward,stock=2,expectedStock=1))[0],200)

    def test_laptop_requires_human_demonstration_and_delivery_does_not_restock(self):
        person,me=self.learner();self.check(person)
        reward=self.offer(category='laptop',stock=1)
        result=person.request('/api/reward',dict(id=reward))[1]['me']
        claim=next(c for c in result['claims'] if c['reward']==reward)
        payload=dict(id=claim['id'],status='approved',note='Synthetic project review.')
        self.assertEqual(self.mentor.request('/api/mentor/claim',payload)[0],400)
        payload['demonstrated']=True
        self.assertEqual(self.mentor.request('/api/mentor/claim',payload)[0],200)
        self.assertEqual(self.mentor.request('/api/mentor/claim',dict(id=claim['id'],status='given',note='Synthetic delivery.'))[0],200)
        info=self.mentor.request('/api/mentor')[1]
        self.assertEqual(next(r for r in info['rewards'] if r['id']==reward)['available'],0)
        self.assertEqual(next(c for c in info['claims'] if c['id']==claim['id'])['demonstrated'],1)

    def test_reward_validation_and_privacy(self):
        guest=Client(self.url);person,me=self.learner()
        self.assertEqual(guest.request('/api/mentor/reward-stock',{})[0],401)
        self.assertEqual(person.request('/api/mentor/reward',{})[0],401)
        offer_data=dict(title='Test offer',description='No real reward.',cost=10,category='giftcard',stock=0)
        for change in ({'stock':None},{'stock':True},{'stock':-1},{'stock':1.5},{'minimum_modules':True},{'required_modules':['missing']},{'required_modules':['digital-1','digital-1']}):
            self.assertEqual(self.mentor.request('/api/mentor/reward',offer_data|change)[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/reward',offer_data|dict(required_modules=['digital-1'],minimum_modules=1))[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/reward',offer_data|dict(category='experience',required_modules=['digital-1'],minimum_modules=1))[0],200)
        base.complete_core_fixture(self.app,person)
        for u in [f'digital-{i}' for i in range(1,9)]:
            result=person.request('/api/attempt',dict(unit=u))
            self.assertEqual(result[0],200);self.assertEqual(len(result[1]['questions']),6)
            self.assertTrue(all('answer' not in q and 'explanation' not in q for q in result[1]['questions']))

    def test_owner_reset_preserves_every_learner_and_rejects_stale_work(self):
        child,child_me=self.learner();self.check(child,'digital-2')
        child.request('/api/draft',dict(unit='digital-2',revision=0,data=dict(phase=1,reflection='Child work must remain.')))
        reward=self.offer(stock=2)
        child_before=child.request('/api/me')[1];inbox_before=self.mentor.request('/api/mentor')[1]
        own=self.mentor.request('/api/mentor/learn',{})[1];base.complete_tutorial(self.mentor);old=own['id']
        self.check(self.mentor,'digital-5')
        replay,_=self.check(self.mentor,'digital-5')
        self.assertEqual(replay['report']['pipFoodReason'],'review')
        self.mentor.request('/api/profile',dict(avatar='pixel'))
        self.mentor.request('/api/starting-point',dict(revision=0,data=dict(age=31,seed=1,answers=[])))
        self.mentor.request('/api/draft',dict(unit='digital-5',revision=0,data=dict(phase=3,reflection='Owner work to clear.')))
        _,attempt,_=self.mentor.request('/api/attempt',dict(unit='math-cash'))
        self.assertEqual(child.request('/api/mentor/reset-learning',dict(learner=old,confirmation='RESET MY LEARNING'))[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/reset-learning',dict(learner=child_me['id'],confirmation='RESET MY LEARNING'))[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/reset-learning',dict(learner=old))[0],400)
        status,fresh,_=self.mentor.request('/api/mentor/reset-learning',dict(learner=old,confirmation='RESET MY LEARNING'))
        self.assertEqual(status,200);self.assertNotEqual(fresh['id'],old);self.assertTrue(fresh['personal'])
        self.assertEqual(fresh['points'],0);self.assertEqual(fresh['attempts'],[]);self.assertEqual(fresh['mastered'],[])
        self.assertIsNone(fresh['startingPoint']);self.assertEqual(fresh['profile']['avatar'],'orbit')
        self.assertEqual(self.mentor.request('/api/drafts')[1],{})
        current=child.request('/api/me')[1]
        current['pipFood'].pop('asOf',None);child_before['pipFood'].pop('asOf',None)
        self.assertEqual(current,child_before)
        inbox_after=self.mentor.request('/api/mentor')[1]
        for key in ('learners','reports','rewards','claims'):self.assertEqual(inbox_after[key],inbox_before[key])
        self.assertEqual(self.mentor.request('/api/draft',dict(learner=old,unit='digital-5',revision=0,data=dict(phase=1)))[0],409)
        self.assertEqual(self.mentor.request('/api/submit',dict(learner=old,id=attempt['id']))[0],409)
        with self.app.store.db() as db:
            self.assertIsNone(db.execute('SELECT * FROM learners WHERE id=?',(old,)).fetchone())
            self.assertEqual(db.execute("SELECT COUNT(*) FROM sessions WHERE role='learner' AND owner=?",(old,)).fetchone()[0],0)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM pip_review_grants WHERE learner=?',(old,)).fetchone()[0],0)
        self.assertEqual(fresh['pipFood']['bank'],0)

    def test_migration_preserves_an_old_reward(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'stepstone.sqlite3'
            with sqlite3.connect(path) as db:
                db.execute('CREATE TABLE rewards (id TEXT PRIMARY KEY,title TEXT,description TEXT,cost INTEGER,kind TEXT,active INTEGER)')
                db.execute("INSERT INTO rewards VALUES('legacy','Existing activity','Keep this.',40,'mentor',1)")
            db.close()
            store=server.Store(tmp)
            with store.db() as db:
                reward=next(r for r in store.rewards(db) if r['id']=='legacy')
                self.assertEqual(reward['title'],'Existing activity');self.assertIsNone(reward['stock'])
                self.assertEqual(reward['required_modules'],[])

if __name__=='__main__':unittest.main()
