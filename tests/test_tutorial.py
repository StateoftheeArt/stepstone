"""Guided setup is account-owned and ungraded; existing work survives migration."""
import copy
import json
from pathlib import Path
import subprocess
import unittest
import test_server as fixtures
from test_server import Client
import server
from tutorial import evaluate


def tour(steps=10, **changes):
    value=dict(version=1,events=[dict(action=a,**({'value':7} if a=='pack' else {'value':'3'} if a=='answer' else {})) for a in server.TUTORIAL['actions'][:steps]])
    return value | changes


class TutorialTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_gate_new_work_but_keep_recovery_and_drafts_available(self):
        learner,me=self.learner(tutorial=False)
        self.assertIsNone(learner.request('/api/me')[1]['tutorial'])
        for path,data in [('/api/attempt',dict(unit='math-1'))]:
            code,result,_=learner.request(path,data)
            self.assertEqual(code,409);self.assertIn('quick tour',result['error'])
        self.assertEqual(learner.request('/api/reward',dict(id='theme-ocean'))[0],200)
        self.assertEqual(learner.request('/api/progress',dict(unit='math-1',stage=2))[0],200)
        other=Client(self.url)
        self.assertEqual(other.request('/api/login',dict(code=me['recovery']))[0],200)
        self.assertEqual(learner.request('/api/me')[1]['points'],0)

    def test_walk_resume_receipt_and_no_achievement_awards(self):
        learner,me=self.learner(tutorial=False)
        revision=0
        for step in range(11):
            code,record,_=learner.request('/api/tutorial',dict(revision=revision,data=tour(step)))
            self.assertEqual(code,200);revision=record['revision']
            self.assertEqual(record['result'],dict(step=step,total=10,complete=step==10))
        current=learner.request('/api/me')[1]
        self.assertEqual(current['tutorial'],record)
        self.assertEqual((current['points'],current['totalChecks'],current['mastered']),(0,0,[]))
        self.assertEqual(current['progress'],{})
        mentor=self.mentor.request('/api/mentor')[1]
        self.assertEqual(mentor['learners'][0]['tutorial'],record)
        self.assertEqual(mentor['reports'],[])
        self.assertEqual(learner.request('/api/attempt',dict(unit='math-1'))[0],200)

    def test_retries_conflicts_and_no_regression(self):
        learner,me=self.learner(tutorial=False)
        payload=dict(revision=0,data=tour(3,count=6))
        first=learner.request('/api/tutorial',payload)[1]
        self.assertEqual(learner.request('/api/tutorial',payload)[1],first)
        other=Client(self.url);other.request('/api/login',dict(code=me['recovery']))
        self.assertEqual(other.request('/api/me')[1]['tutorial']['data']['count'],6)
        self.assertEqual(other.request('/api/tutorial',dict(revision=0,data=tour(4)))[0],409)
        self.assertEqual(other.request('/api/tutorial',dict(revision=1,data=tour(2)))[0],409)
        self.assertEqual(other.request('/api/tutorial',dict(revision=1,data=tour(4)))[0],200)
        self.assertEqual(learner.request('/api/tutorial',dict(revision=1,data=tour(3,count=7)))[0],409)

    def test_invalid_actions_and_claimed_completion_do_not_unlock(self):
        learner,_=self.learner(tutorial=False)
        bad=[tour(1,events=[dict(action='finish')]),tour(5,events=tour(5)['events'][:-1]+[dict(action='pack',value=8)]),tour(6,events=tour(6)['events'][:-1]+[dict(action='answer',value='2')]),tour(0,version=True),tour(0,count=True),tour(0,answerChecked='yes')]
        for data in bad:
            self.assertEqual(learner.request('/api/tutorial',dict(revision=0,data=data))[0],400)
        record=learner.request('/api/tutorial',dict(revision=0,data=tour(0,complete=True,result={'complete':True})))[1]
        self.assertFalse(record['result']['complete']);self.assertNotIn('complete',record['data'])
        self.assertEqual(learner.request('/api/attempt',dict(unit='math-1'))[0],409)

    def test_learner_isolation_and_owner_reset(self):
        learner,me=self.learner(tutorial=False)
        other,_=self.learner('Another learner',tutorial=False)
        payload=dict(revision=0,data=tour(4,count=6))
        saved=learner.request('/api/tutorial',payload)[1]
        self.assertEqual(other.request('/api/tutorial',payload|dict(learner=me['id']))[0],409)
        self.assertIsNone(other.request('/api/me')[1]['tutorial'])
        own=self.mentor.request('/api/mentor/learn',{})[1]
        fixtures.complete_tutorial(self.mentor)
        fresh=self.mentor.request('/api/mentor/reset-learning',dict(learner=own['id'],confirmation='RESET MY LEARNING'))[1]
        self.assertNotEqual(own['id'],fresh['id']);self.assertIsNone(fresh['tutorial'])
        self.assertEqual(learner.request('/api/me')[1]['tutorial'],saved)

    def test_existing_unfinished_check_and_reports_survive_new_gate(self):
        learner,me=self.learner()
        old,_=self.check(learner)
        attempt=learner.request('/api/attempt',dict(unit='math-1'))[1]
        with self.app.store.db() as db:
            db.execute('DELETE FROM tutorials WHERE learner=?',(me['id'],))
        legacy=learner.request('/api/me')[1]
        self.assertEqual(legacy['points'],old['me']['points']);self.assertEqual(legacy['mastered'],old['me']['mastered'])
        self.assertEqual(learner.request('/api/attempt',dict(unit='math-1'))[1]['id'],attempt['id'])
        answers=fixtures.right_answers('math-1',attempt)
        self.assertEqual(learner.request('/api/submit',dict(id=attempt['id'],answers=answers,reflection='I counted each part.',support='myself',ink=[]))[0],200)
        self.assertEqual(learner.request('/api/attempt',dict(unit='reading-1'))[0],409)
        fixtures.complete_tutorial(learner)
        current=learner.request('/api/me')[1]
        self.assertEqual(current['totalChecks'],2);self.assertEqual(current['points'],40)

    def test_browser_and_server_state_validation_agree(self):
        cases=[tour(n) for n in range(11)]+[tour(4,count=7,bagChecked=True),tour(5,answer='6/2',answerChecked=True),tour(5,answer='4',answerChecked=True),tour(5,answer='3'+' '*81,answerChecked=True),tour(0,count=None),tour(0,answer=None),tour(0,version=True),tour(0,hint=1),tour(0,events=[{'action':'finish'}])]
        expected=[]
        for data in cases:
            try:
                clean,result=evaluate(server.TUTORIAL,copy.deepcopy(data));expected.append(dict(data=clean,result=result))
            except ValueError:expected.append(None)
        script="""import fs from 'node:fs';import {evaluateTour} from './public/tutorial-state.js';const {config,cases}=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(cases.map(data=>{try{return evaluateTour(config,data)}catch{return null}})));"""
        run=subprocess.run(['node','--input-type=module','-e',script],input=json.dumps(dict(config=server.TUTORIAL,cases=cases)),text=True,capture_output=True,cwd=Path(__file__).resolve().parents[1],check=True)
        self.assertEqual(json.loads(run.stdout),expected)


if __name__=='__main__':unittest.main()
