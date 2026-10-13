import copy,json,subprocess,unittest
from pathlib import Path
import placement

ROOT=Path(__file__).resolve().parents[1]
BANK=json.loads((ROOT/'public/starting-point.json').read_text(encoding='utf-8'))
EXT=BANK['extended'];QUESTIONS={q['id']:q for q in EXT['questions']}
def run_check(pattern,seed=0,heard=False,age=16):
    data=dict(version=4,age=age,seed=seed,answers=[]);states=[]
    for i in range(49):
        result=placement.evaluate(BANK,data);states.append((copy.deepcopy(data),result))
        if not result['next']:break
        q=QUESTIONS[result['next']];correct=q['answer']
        right=pattern=='right' or pattern=='mixed' and i%4 in (0,1)
        answer=None if pattern=='unsure' else str(correct) if right and q['kind']=='number' else correct if right else str(correct+2) if q['kind']=='number' else (correct+1)%len(q['options'])
        data['answers'].append(dict(id=q['id'],answer=answer,heard=heard))
    return data,states

class Starting103Tests(unittest.TestCase):
    def test_all_six_courses_get_eight_unique_cases(self):
        for seed in [0,1,37,65535]:
            for pattern in ['right','wrong','mixed','unsure']:
                data,states=run_check(pattern,seed)
                result=states[-1][1]
                self.assertEqual(len(data['answers']),48)
                self.assertEqual(len({a['id'] for a in data['answers']}),48)
                self.assertTrue(result['questionsDone']);self.assertFalse(result['complete'])
                self.assertEqual(list(result['levels']),EXT['subjects'])
                self.assertTrue(all(a['answered']==8 for a in result['areas'].values()))
                if pattern in ['wrong','unsure']:self.assertEqual(set(result['levels'].values()),{1})
                if pattern=='right':self.assertEqual(set(result['levels'].values()),{10})
                data['writing']=dict(text='',status='skipped');self.assertTrue(placement.evaluate(BANK,data)['complete'])
    def test_repeated_evidence_and_no_age_or_listening_penalty(self):
        for age in [5,16,99]:
            data,states=run_check('right',37,True,age)
            baseline=run_check('right',37)[1][-1][1]
            self.assertEqual(states[-1][1]['suggestions'],baseline['suggestions'])
            self.assertEqual(states[-1][1]['levels'],baseline['levels'])
            self.assertEqual([r['next'] for _,r in states],[r['next'] for _,r in run_check('right',37)[1]])
        data,states=run_check('right')
        for _,result in states:
            for area in result['areas'].values():
                band=area['confirmedBand'];self.assertGreaterEqual(area['bands'][band]['matched'],2);self.assertGreaterEqual(area['bands'][band]['skills'],2)
    def test_inconsistent_evidence_does_not_skip_to_hardest_material(self):
        data,states=run_check('mixed')
        self.assertTrue(all(a['confirmedBand']<3 for a in states[-1][1]['areas'].values()))
        # One correct answer in a band is not enough to recommend that band.
        short=copy.deepcopy(data);short['answers']=short['answers'][:1]
        self.assertEqual(placement.evaluate(BANK,short)['next'],states[1][1]['next'])
    def test_forged_answers_and_drafts_rejected(self):
        data,states=run_check('right');short=copy.deepcopy(data);short['answers']=short['answers'][:1]
        for mutation in [dict(id='not-the-next-question'),dict(answer=True),dict(heard='yes')]:
            bad=copy.deepcopy(short);bad['answers'][0].update(mutation)
            with self.assertRaises(ValueError):placement.evaluate(BANK,bad)
        bad=copy.deepcopy(short);bad['draft']=dict(id='wrong',answer=None)
        with self.assertRaises(ValueError):placement.evaluate(BANK,bad)
        bad=copy.deepcopy(data);bad['answers'].append(bad['answers'][0])
        with self.assertRaises(ValueError):placement.evaluate(BANK,bad)
        self.assertEqual(placement.normalize(short)['version'],4)
    def test_python_and_browser_replay_match_every_prefix(self):
        states=[]
        for seed in [0,1,37,65535]:
            for pattern in ['right','wrong','mixed','unsure']:
                data,flow=run_check(pattern,seed,seed%2==1);states+=flow
                data['writing']=dict(status='submitted',text='I will be late. I will arrive at 4:15 pm.',support='myself',heard=False)
                states.append((data,placement.evaluate(BANK,data)))
        script="""import fs from 'node:fs';import {startingPoint} from './public/engine.js';
const data=JSON.parse(fs.readFileSync(0,'utf8')),bank=JSON.parse(fs.readFileSync('public/starting-point.json','utf8'));
process.stdout.write(JSON.stringify(data.map(d=>startingPoint(bank,d))));"""
        result=subprocess.run(['node','--input-type=module','-e',script],input=json.dumps([d for d,_ in states]),text=True,encoding='utf-8',capture_output=True,cwd=ROOT,check=True)
        self.assertEqual(json.loads(result.stdout),[r for _,r in states])

class Starting103ApiTests(unittest.TestCase):
    import test_server as fixtures
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    def test_new_check_saves_resumes_and_awards_only_once(self):
        child,_=self.learner(tutorial=False)
        data,states=run_check('right',37)
        for revision,(partial,expected) in enumerate([states[13],states[31],states[-1]]):
            status,saved,_=child.request('/api/starting-point',dict(revision=revision,data=partial))
            self.assertEqual(status,200,saved);self.assertEqual(saved['result'],expected)
            self.assertEqual(child.request('/api/me')[1]['startingPoint']['data'],partial)
        self.assertFalse(child.request('/api/me')[1]['welcomeAwards']['starting'])
        data['writing']=dict(status='skipped',text='',support='myself',heard=False)
        status,saved,_=child.request('/api/starting-point',dict(revision=3,data=data))
        self.assertEqual(status,200,saved);self.assertTrue(saved['result']['complete'])
        before=child.request('/api/me')[1]
        self.assertTrue(before['welcomeAwards']['starting']);self.assertEqual(before['points'],5)
        self.assertEqual(child.request('/api/starting-point',dict(revision=4,data=data))[0],200)
        after=child.request('/api/me')[1]
        self.assertEqual(after['points'],5);self.assertEqual(after['mastered'],[])
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=dict(data,age=17)))[0],409)
        self.assertEqual(child.request('/api/me')[1]['startingPoint']['data'],data)
    def test_forged_new_question_cannot_change_saved_record(self):
        child,_=self.learner(tutorial=False)
        data,states=run_check('unsure')
        short=states[2][0]
        self.assertEqual(child.request('/api/starting-point',dict(revision=0,data=short))[0],200)
        bad=copy.deepcopy(states[3][0]);bad['answers'][-1]['id']='math-1-check'
        self.assertEqual(child.request('/api/starting-point',dict(revision=1,data=bad))[0],400)
        self.assertEqual(child.request('/api/me')[1]['startingPoint']['data'],short)

if __name__=='__main__':unittest.main()
