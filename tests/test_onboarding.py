"""API fixtures for setup persistence and reward boundaries; not UI completion evidence."""
import copy
import json
import subprocess
import unittest
from pathlib import Path
import test_server as fixtures
from test_server import Client
import server
from placement import evaluate as placement
from tutorial import evaluate


def starting_answers():
    data=dict(version=3,age=16,seed=48,answers=[])
    while not (result:=placement(server.STARTING_POINT,data))['complete']:
        data['answers'].append(dict(id=result['next'],answer=None,heard=False))
    return data


def tour(count=20):
    values=dict(pack=7,answer='3',mentor='connected',goal='core-laptop')
    return dict(version=2,events=[dict(action=a,**({'value':values[a]} if a in values else {})) for a in server.TUTORIAL['setupActions'][:count]])


PROFILE=dict(alias='Setup tester',avatar='wave',accent='violet',motivation='create',interests=['digital','reading'],nextWin='Make a useful checklist')


class OnboardingTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner

    def start(self,client):
        response=client.request('/api/starting-point',dict(revision=0,data=starting_answers()))
        self.assertEqual(response[0],200,response[1])
        return response[1]

    def test_two_milestones_are_exactly_five_each_and_replay_safe(self):
        child,me=self.learner(tutorial=False)
        data=starting_answers();self.assertEqual(len(data['answers']),24)
        saved=self.start(child)
        for _ in range(2):
            self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[1],saved)
        state=child.request('/api/me')[1]
        self.assertEqual(state['points'],5);self.assertEqual(state['mastered'],[])
        self.assertEqual(child.request('/api/profile',PROFILE)[0],200)
        payload=dict(revision=0,data=tour())
        self.assertEqual(child.request('/api/tutorial',payload)[0],200)
        self.assertEqual(child.request('/api/tutorial',payload)[0],200)
        state=child.request('/api/me')[1]
        self.assertEqual(state['points'],10);self.assertEqual(state['totalChecks'],0)
        self.assertEqual(state['welcomeAwards'],dict(starting=True,tutorial=True))
        data['seed']=49;data['answers']=[]
        while not (r:=placement(server.STARTING_POINT,data))['complete']:
            data['answers'].append(dict(id=r['next'],answer=None,heard=False))
        self.assertEqual(child.request('/api/starting-point',dict(revision=1,data=data))[0],200)
        self.assertEqual(child.request('/api/me')[1]['points'],10)

    def test_tour_requires_answers_profile_and_order(self):
        child,_=self.learner(tutorial=False)
        self.assertEqual(child.request('/api/tutorial',dict(revision=0,data=tour()))[0],409)
        self.start(child)
        self.assertEqual(child.request('/api/tutorial',dict(revision=0,data=tour()))[0],409)
        self.assertEqual(child.request('/api/profile',PROFILE)[0],200)
        self.assertEqual(child.request('/api/tutorial',dict(revision=0,data=tour(4)))[0],200)
        self.assertEqual(child.request('/api/tutorial',dict(revision=0,data=tour(5)))[0],409)
        self.assertEqual(child.request('/api/tutorial',dict(revision=1,data=tour(3)))[0],409)
        malformed=tour();malformed['events'][17]['value']='bypass'
        self.assertEqual(child.request('/api/tutorial',dict(revision=1,data=malformed))[0],400)
        self.assertEqual(child.request('/api/me')[1]['points'],5)

    def test_gift_card_goal_can_finish_setup_without_lesson_credit(self):
        child,me=self.learner(tutorial=False)
        self.start(child)
        self.assertEqual(child.request('/api/profile',PROFILE|dict(avatar='dragon'))[0],200)
        status,selected,_=child.request('/api/reward-goal',dict(id='card-exchange'))
        self.assertEqual(status,200);self.assertEqual(selected['goal'],'card-exchange')
        data=tour()
        next(event for event in data['events'] if event['action']=='goal')['value']='card-exchange'
        status,completed,_=child.request('/api/tutorial',dict(revision=0,data=data))
        self.assertEqual(status,200);self.assertTrue(completed['result']['complete'])
        returning=Client(self.url)
        restored=returning.request('/api/login',dict(code=me['recovery']))[1]
        self.assertEqual(restored['goal'],'card-exchange')
        self.assertEqual(restored['profile']['avatar'],'dragon')
        self.assertEqual((restored['points'],restored['totalChecks'],restored['mastered']),(10,0,[]))

    def test_mentor_controls_only_own_account_and_keep_points_and_work(self):
        child,child_me=self.learner(tutorial=False)
        self.assertEqual(child.request('/api/mentor')[0],401)
        self.assertEqual(child.request('/api/mentor/tutorial-control',{})[0],401)
        own=self.mentor.request('/api/mentor/learn',{})[1]
        self.start(self.mentor);self.mentor.request('/api/profile',PROFILE)
        self.mentor.request('/api/tutorial',dict(revision=0,data=tour()))
        self.mentor.request('/api/draft',dict(unit='math-1',revision=0,data=dict(phase=1,ink=[])))
        payload=dict(learner=own['id'],revision=1,action='restart')
        self.assertEqual(self.mentor.request('/api/mentor/tutorial-control',{**payload,'learner':child_me['id']})[0],403)
        restarted=self.mentor.request('/api/mentor/tutorial-control',payload)
        self.assertEqual(restarted[0],200,restarted[1])
        self.assertEqual(restarted[1]['tutorial']['result']['step'],4)
        self.assertEqual(restarted[1]['points'],10)
        self.assertEqual(self.mentor.request('/api/mentor/tutorial-control',payload)[0],409)
        self.assertEqual(self.mentor.request('/api/tutorial',dict(revision=2,data=tour()))[0],200)
        self.assertEqual(self.mentor.request('/api/me')[1]['points'],10)
        self.assertEqual(self.mentor.request('/api/drafts')[1]['math-1']['data']['phase'],1)
        self.assertEqual(child.request('/api/me')[1]['points'],0)

    def test_skip_does_not_award_points_and_restart_removes_override(self):
        own=self.mentor.request('/api/mentor/learn',{})[1]
        result=self.mentor.request('/api/mentor/tutorial-control',dict(learner=own['id'],revision=0,action='skip'))[1]
        self.assertTrue(result['tutorial']['result']['skipped']);self.assertEqual(result['points'],0)
        result=self.mentor.request('/api/mentor/tutorial-control',dict(learner=own['id'],revision=1,action='restart'))[1]
        self.assertFalse(result['tutorial']['result']['complete']);self.assertNotIn('skipped',result['tutorial']['result'])

    def test_profile_roundtrip_and_invalid_fields_do_not_overwrite(self):
        child,_=self.learner(tutorial=False)
        saved=child.request('/api/profile',PROFILE)[1]
        self.assertTrue(saved['profile']['ready'])
        for field,value in [('accent','red'),('avatar','nope'),('motivation','invalid'),('interests',['math','math']),('interests',['math','reading','science','writing']),('nextWin','a'*97)]:
            self.assertEqual(child.request('/api/profile',{**PROFILE,field:value,'alias':'Must not save'})[0],400)
            self.assertEqual(child.request('/api/me')[1]['alias'],PROFILE['alias'])
        self.assertEqual(child.request('/api/me')[1]['profile']['nextWin'],PROFILE['nextWin'])

    def test_v2_browser_server_validation_parity(self):
        cases=[tour(n) for n in range(21)]
        invalid=copy.deepcopy(tour());invalid['events'][18]['value']='cash-now';cases.append(invalid)
        expected=[]
        for data in cases:
            try:
                clean,result=evaluate(server.TUTORIAL,data);expected.append(dict(data=clean,result=result))
            except ValueError:expected.append(None)
        script="import fs from 'node:fs';import {evaluateTour} from './public/tutorial-state.js';const {config,cases}=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(cases.map(data=>{try{return evaluateTour(config,data)}catch{return null}})));"
        run=subprocess.run(['node','--input-type=module','-e',script],input=json.dumps(dict(config=server.TUTORIAL,cases=cases)),capture_output=True,text=True,cwd=Path(__file__).resolve().parents[1],check=True)
        self.assertEqual(json.loads(run.stdout),expected)


if __name__=='__main__':unittest.main()
