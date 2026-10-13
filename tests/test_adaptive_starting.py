"""Adaptive replay, private writing, compatibility and cross-language parity."""
import copy
import json
import random
import subprocess
import unittest
import test_server as fixtures
from test_server import Client
import server
from placement import evaluate

BANK=server.STARTING_POINT
QUESTIONS={q['id']:q for q in BANK['questions']}


def response(q,right=True,heard=False):
    return dict(id=q['id'],answer=(str(q['answer']) if q['kind']=='number' else q['answer']) if right else None,heard=heard)


def complete(pattern=lambda q,i:True,seed=0,age=14,writing=True):
    data=dict(version=2,age=age,seed=seed,answers=[])
    counts={s:0 for s in BANK['subjects']}
    while (result:=evaluate(BANK,data))['next']:
        q=QUESTIONS[result['next']]
        data['answers'].append(response(q,pattern(q,counts[q['subject']])))
        counts[q['subject']]+=1
    if writing:
        data['writing']=dict(text='Jo, I am running late. I will arrive at 4:15 pm.',status='submitted',support='myself',heard=False)
    return data


class AdaptiveTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_routes_need_repeated_evidence_and_are_independent(self):
        for ceiling,start in [(-1,1),(0,1),(1,4),(2,7),(3,10)]:
            data=complete(lambda q,i:q['band']<=ceiling)
            result=evaluate(BANK,data)
            self.assertTrue(result['complete']);self.assertNotIn('average',result)
            self.assertEqual(result['levels']['math'],start)
            self.assertEqual(result['levels']['digital'],[1,3,5,7][max(0,ceiling)])
            self.assertTrue(all(4<=a['answered']<=6 for a in result['areas'].values()))
            self.assertEqual(len(set(a['id'] for a in result['evidence'])),len(data['answers']))
        data=complete(lambda q,i:q['subject']!='reading')
        result=evaluate(BANK,data)
        self.assertEqual(result['levels'],dict(math=10,reading=1,writing=10,science=10,social=10,digital=7))
        data['age']=5;self.assertEqual(evaluate(BANK,data),result)
        data['age']=99;self.assertEqual(evaluate(BANK,data),result)
        data['answers']=[dict(a,heard=True) for a in data['answers']]
        self.assertEqual(evaluate(BANK,data)['levels'],result['levels'])

    def test_mixed_answers_are_conservative_and_bounded(self):
        # Two out of three at each band confirms it; six answers cannot confirm a third band.
        result=evaluate(BANK,complete(lambda q,i:i%3!=1))
        self.assertEqual(result['levels']['math'],7)
        self.assertTrue(all(a['basis']=='check-in' and a['answered']==6 for a in result['areas'].values()))
        data=dict(version=2,age=14,seed=0,answers=[])
        q=QUESTIONS[evaluate(BANK,data)['next']];data['answers'].append(response(q))
        self.assertEqual(QUESTIONS[evaluate(BANK,data)['next']]['band'],1,'one lucky answer cannot raise difficulty')
        q=QUESTIONS[evaluate(BANK,data)['next']];data['answers'].append(response(q,False))
        self.assertEqual(QUESTIONS[evaluate(BANK,data)['next']]['band'],1,'mixed evidence needs a third question')

    def test_writing_has_no_automatic_grade_and_can_be_deferred(self):
        data=complete(writing=False)
        self.assertFalse(evaluate(BANK,data)['complete']);self.assertTrue(evaluate(BANK,data)['questionsDone'])
        data['writing']=dict(text='anything',status='draft',support='tool',heard=True)
        self.assertFalse(evaluate(BANK,data)['complete'])
        data['writing']['status']='submitted';result=evaluate(BANK,data)
        self.assertTrue(result['complete']);self.assertNotIn('writingScore',result)
        data['writing']=dict(text='',status='skipped',support='myself')
        self.assertEqual(evaluate(BANK,data)['levels'],result['levels'])
        self.assertTrue(evaluate(BANK,data)['complete'])

    def test_drafts_private_resume_and_client_results_ignored(self):
        child,me=self.learner()
        data=dict(version=2,age=14,seed=0,answers=[])
        q=QUESTIONS[evaluate(BANK,data)['next']]
        data['draft']=dict(id=q['id'],answer='3/',heard=True)
        data['result']=dict(complete=True,levels=dict(math=12))
        status,saved,_=child.request('/api/starting-point',dict(revision=0,data=data))
        self.assertEqual(status,200);self.assertFalse(saved['result']['complete'])
        self.assertNotIn('result',saved['data']);self.assertEqual(saved['data']['draft']['answer'],'3/')
        other=Client(self.url);other.request('/api/login',dict(code=me['recovery']))
        self.assertEqual(other.request('/api/me')[1]['startingPoint'],saved)
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[1],saved,'identical retry is idempotent')
        data=complete();data['writing']['text']='<script>not executable</script> My own words.'
        data['writing']['support']='person'
        status,saved,_=other.request('/api/starting-point',dict(revision=1,data=data))
        self.assertEqual(status,200)
        self.assertEqual(self.mentor.request('/api/mentor')[1]['learners'][0]['startingPoint'],saved)
        self.assertEqual(child.request('/api/starting-point',dict(revision=1,data=dict(data,age=15)))[0],409)
        stranger,another=self.learner('Sibling')
        self.assertIsNone(stranger.request('/api/me')[1]['startingPoint'])
        self.assertEqual(stranger.request('/api/starting-point',dict(learner=me['id'],revision=2,data=data))[0],409)
        self.assertEqual(Client(self.url).request('/api/starting-point',dict(revision=0,data=data))[0],401)
        state=child.request('/api/me')[1]
        for field,empty in [('points',5),('mastered',[]),('progress',{}),('attempts',[])]:self.assertEqual(state[field],empty)

    def test_bad_inputs_do_not_change_saved_data(self):
        child,_=self.learner()
        base=dict(version=2,age=14,seed=0,answers=[])
        q=QUESTIONS[evaluate(BANK,base)['next']]
        self.assertEqual(q['kind'],'number')
        bad=[]
        for version in (True,0,6,'2',None):bad.append(dict(base,version=version))
        for answer in (True,3,'','1/0','NaN','1e3','7 feet','0'*81):bad.append(dict(base,answers=[dict(id=q['id'],answer=answer)]))
        bad.append(dict(base,answers=[dict(id='wrong-question',answer='9')]))
        bad.append(dict(base,answers=[dict(id=q['id'],answer='9',heard=None)]))
        bad.append(dict(base,draft=dict(id='wrong-question',answer='1')))
        bad.append(dict(base,writing=dict(text='too early',status='submitted')))
        finished=complete()
        for writing in (None,dict(text='',status='submitted'),dict(text='a'*1001,status='submitted'),dict(text='x',status='done'),dict(text='x',status='submitted',support='guessed')):
            bad.append(dict(finished,writing=writing))
        bad.append(dict(finished,answers=finished['answers']+[response(q)]))
        for data in bad:self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=data))[0],400,str(data)[:180])
        self.assertIsNone(child.request('/api/me')[1]['startingPoint'])
        # Equivalent decimal/fraction answers are interpreted as numbers, never evaluated as code.
        valid=dict(base,answers=[dict(id=q['id'],answer='18/2')])
        self.assertTrue(evaluate(BANK,valid)['evidence'][0]['correct'])

    def test_retake_keeps_mastery_and_personal_work_separate(self):
        child,_=self.learner();checked,_=self.check(child)
        child.request('/api/draft',dict(unit='reading-1',revision=0,data=dict(phase=1,ink=[])))
        child.request('/api/starting-point',dict(revision=0,data=complete()))
        child.request('/api/starting-point',dict(revision=1,data=complete(lambda q,i:False)))
        state=child.request('/api/me')[1]
        self.assertEqual(state['mastered'],checked['me']['mastered']);self.assertEqual(state['points'],checked['me']['points']+5)
        self.assertEqual(child.request('/api/drafts')[1]['reading-1']['data']['phase'],1)
        self.mentor.request('/api/mentor/learn',{})
        self.assertIsNone(self.mentor.request('/api/me')[1]['startingPoint'])
        self.mentor.request('/api/starting-point',dict(revision=0,data=complete(age=31)))
        self.assertEqual(len(self.mentor.request('/api/mentor')[1]['learners']),1)

    def test_browser_and_server_replay_agree(self):
        vectors=[]
        for seed in (0,1,37,65535):
            rng=random.Random(seed)
            for pattern in (lambda q,i:True,lambda q,i:False,lambda q,i:i%3!=1,lambda q,i:rng.random()>.5):
                data=dict(version=2,age=14,seed=seed,answers=[])
                while (result:=evaluate(BANK,data))['next']:
                    vectors.append(copy.deepcopy(data))
                    q=QUESTIONS[result['next']];data['answers'].append(response(q,pattern(q,len(data['answers']))))
                vectors.append(copy.deepcopy(data))
                data['writing']=dict(text='Jo, I will arrive at 4:15 pm.',status='submitted',support='myself')
                vectors.append(data)
        code="""import fs from 'node:fs';import {startingPoint} from './public/engine.js';
const {bank,vectors}=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(vectors.map(d=>startingPoint(bank,d))));"""
        run=subprocess.run(['node','--input-type=module','-e',code],input=json.dumps(dict(bank=BANK,vectors=vectors)),text=True,capture_output=True,cwd=server.ROOT,check=True,encoding='utf-8')
        self.assertEqual(json.loads(run.stdout),[evaluate(BANK,d) for d in vectors])


if __name__=='__main__':unittest.main()
