import copy
import json
from pathlib import Path
import subprocess
import unittest
import placement
import pip_rewards
import server
import test_server as fixtures

ROOT=Path(__file__).resolve().parents[1]
BANK=server.STARTING_POINT
QUESTIONS={q['id']:q for q in BANK['foundation']['questions']}

def flow(pattern='right',seed=0,age=16,heard=False):
    data=dict(version=5,age=age,seed=seed,answers=[])
    states=[]
    while True:
        result=placement.evaluate(BANK,data)
        states.append((copy.deepcopy(data),result))
        if not result['next']:break
        q=QUESTIONS[result['next']]
        right=pattern=='right' or pattern=='mixed' and len(data['answers'])%3==0
        answer=None if pattern=='unsure' else (str(q['answer']) if q['kind']=='number' else q['answer']) if right else str(q['answer']+20) if q['kind']=='number' else (q['answer']+1)%len(q['options'])
        data['answers'].append(dict(id=q['id'],answer=answer,heard=heard))
    return data,states

class Starting112ReplayTests(unittest.TestCase):
    def test_practical_foundation_questions_and_conservative_routes(self):
        self.assertEqual(BANK['foundation']['subjects'],['math','reading','science','life'])
        for subject in BANK['foundation']['subjects']:
            for band in range(3):
                questions=[q for q in QUESTIONS.values() if q['subject']==subject and q['band']==band]
                self.assertEqual(len(questions),6)
                self.assertEqual(len({q['skill'] for q in questions}),2)
                self.assertTrue(all(q['scene'] for q in questions))
        for pattern in ['right','wrong','mixed','unsure']:
            data,states=flow(pattern,37)
            result=states[-1][1]
            self.assertEqual(len(data['answers']),24)
            self.assertEqual(len({a['id'] for a in data['answers']}),24)
            self.assertTrue(result['questionsDone'])
            self.assertFalse(result['complete'])
            self.assertEqual(set(result['suggestions']),set(BANK['foundation']['subjects']))
            for area in result['areas'].values():
                for band in range(area['confirmedBand']+1):
                    self.assertGreaterEqual(area['bands'][band]['matched'],2)
                    self.assertEqual(area['bands'][band]['skills'],2)
            data['writing']=dict(status='skipped',text='')
            self.assertTrue(placement.evaluate(BANK,data)['complete'])
            if pattern in ('wrong','unsure'):
                self.assertEqual(placement.evaluate(BANK,data)['suggestions'],dict(math='math-1',reading='reading-1',science='science-1',life='life-hands'))

    def test_every_prefix_matches_browser_replay_and_supports_do_not_change_routes(self):
        states=[]
        for seed in [0,1,37,65535]:
            for pattern in ['right','wrong','mixed','unsure']:
                data,parts=flow(pattern,seed,age=5 if seed%2 else 99,heard=bool(seed%2))
                states.extend(parts)
                data['writing']=dict(status='submitted',text='I will arrive at 4:15 pm.',support='tool',heard=True)
                states.append((data,placement.evaluate(BANK,data)))
        code="""import fs from 'node:fs';import {startingPoint} from './public/engine.js';
const bank=JSON.parse(fs.readFileSync('public/starting-point.json','utf8'));
process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(data=>startingPoint(bank,data))));"""
        run=subprocess.run(['node','--input-type=module','-e',code],input=json.dumps([d for d,_ in states]),capture_output=True,text=True,encoding='utf-8',cwd=ROOT,check=True)
        self.assertEqual(json.loads(run.stdout),[r for _,r in states])
        baseline=flow('right',37)[1][-1][1]
        supported=flow('right',37,age=5,heard=True)[1][-1][1]
        self.assertEqual(baseline['suggestions'],supported['suggestions'])

    def test_bad_order_extra_answers_and_early_writing_are_rejected(self):
        data,states=flow()
        for bad in [dict(states[1][0],draft=dict(id='wrong-question',answer=None)),
                    dict(states[1][0],writing=dict(status='skipped',text='')),
                    dict(data,answers=data['answers']+[data['answers'][0]])]:
            with self.assertRaises(ValueError):placement.evaluate(BANK,bad)
        wrong=copy.deepcopy(states[1][0]);wrong['answers'][0]['answer']=True
        with self.assertRaises(ValueError):placement.evaluate(BANK,wrong)
        self.assertEqual(placement.normalize(states[1][0])['version'],5)

class Starting112ApiTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_completed_plan_unlocks_and_retries_preserve_owned_items(self):
        child,_=self.learner()
        other,_=self.learner(alias='Other Pip',tutorial=False)
        data,states=flow('right',37)
        status,saved,_=child.request('/api/starting-point',dict(revision=0,data=states[10][0]))
        self.assertEqual(status,200,saved)
        self.assertEqual(child.request('/api/me')[1]['pipInventory'],[])
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[0],409)
        self.assertEqual(child.request('/api/starting-point',dict(revision=1,data=data))[0],200)
        self.assertEqual(child.request('/api/me')[1]['pipInventory'],[])
        data['writing']=dict(status='skipped',text='',support='myself',heard=False)
        self.assertEqual(child.request('/api/starting-point',dict(revision=2,data=data))[0],200)
        state=child.request('/api/me')[1]
        units=pip_rewards.starting_item_units(server.CATALOG,state['startingPoint']['result'])
        self.assertEqual(len(units),28)
        expected={item['key'] for item in pip_rewards.choices(server.PROFILE_OPTIONS) if item['modules']<=28}
        self.assertEqual(set(state['pipInventory']),expected)
        self.assertEqual(state['points'],5)
        self.assertEqual(state['mastered'],[])
        self.assertEqual(state['moduleWins'],[])
        self.assertEqual(state['pipFood']['bank'],0)
        self.assertFalse(state['courseReadiness']['complete'])
        for unit in ['pc-start','work-strengths']:
            self.assertEqual(child.request('/api/attempt',dict(unit=unit))[0],409)
        self.assertEqual(other.request('/api/me')[1]['pipInventory'],[])
        for _ in range(3):
            self.assertEqual(child.request('/api/starting-point',dict(revision=3,data=data))[0],200)
            self.assertEqual(child.request('/api/me')[1]['pipInventory'],state['pipInventory'])
        lower,_=flow('unsure',1);lower['writing']=dict(status='skipped',text='')
        self.assertEqual(child.request('/api/starting-point',dict(revision=3,data=lower))[0],200)
        self.assertEqual(child.request('/api/me')[1]['pipInventory'],state['pipInventory'])
        result,_=self.check(child,'math-1')
        after=child.request('/api/me')[1]
        self.assertEqual(after['pipFood']['bank'],1)
        self.assertEqual(after['moduleWins'][0]['pipItems'],[])
        self.assertEqual(set(after['pipInventory']),expected)
        self.assertEqual(after['points'],state['points']+result['report']['points'])
        self.assertEqual(after['mastered'],['math-1'])

    def test_future_cosmetic_milestone_and_profile_can_use_starting_items(self):
        child,_=self.learner()
        data,_=flow();data['writing']=dict(status='skipped',text='')
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[0],200)
        state=child.request('/api/me')[1]
        status,profile,_=child.request('/api/profile',dict(alias='Pip',avatar='fox',accessory='glasses'))
        self.assertEqual(status,200,profile)
        self.check(child,'math-prices')
        self.check(child,'math-budget')
        state=child.request('/api/me')[1]
        expected={item['key'] for item in pip_rewards.choices(server.PROFILE_OPTIONS) if item['modules']<=30}
        self.assertEqual(set(state['pipInventory']),expected)
        milestone=next(win for win in state['moduleWins'] if win['unit']=='math-budget')
        self.assertTrue(milestone['pipItems'])
        self.assertEqual(state['pipFood']['bank'],2)

if __name__=='__main__':unittest.main()
