"""Fresh private checks and stored-attempt continuity, using disposable records."""
from collections import Counter
import copy
import json
from pathlib import Path
import random
import unittest
from unittest.mock import patch

import test_server as fixtures
from check_sampling import case, sample_check

server=fixtures.server
MANIFEST=json.loads((Path(server.__file__).parent/'content/check-bank111.json').read_text(encoding='utf-8'))
UNITS={entry['unit'] for entry in MANIFEST['units']}


class TransferContentTests(unittest.TestCase):
    def test_private_banks_have_distinct_cases_and_cover_both_lessons(self):
        self.assertEqual(len(UNITS),30)
        for unit in UNITS:
            bank=server.BANK[unit]
            if server.UNITS[unit].get('learningRevision',0)>=117 and len(bank)==6:
                self.assertEqual(len({case(q) for q in bank}),6,unit)
                self.assertEqual(Counter(q['lesson'] for q in bank),{1:3,2:3},unit)
                skills=server.UNITS[unit]['checkSkills']
                self.assertEqual(Counter(q['skill'] for q in bank),{s:2 for s in skills},unit)
                for seed in range(100):
                    drawn=sample_check(bank,skills,random.Random(seed))
                    self.assertEqual(len({case(q) for q in drawn}),6,unit)
                    self.assertEqual(Counter(q['skill'] for q in drawn),{s:2 for s in skills},unit)
                    self.assertEqual({q['lesson'] for q in drawn},{1,2},unit)
                for q in bank:
                    self.assertTrue(q['hint'] and q['explanation'],q['id'])
                    self.assertTrue(server.correct(q,str(q['answer'])),q['id'])
                    self.assertFalse(server.correct(q,'a deliberately invalid answer'),q['id'])
                    self.assertNotIn('answer',server.public_question(q))
                    self.assertNotIn('explanation',server.public_question(q))
                continue
            self.assertEqual(len(bank),12,unit)
            self.assertEqual(Counter(q['skill'] for q in bank),{'apply':6,'reason':6},unit)
            self.assertEqual(Counter(q['lesson'] for q in bank),{1:6,2:6},unit)
            cases={case(q) for q in bank}
            self.assertEqual(len(cases),6,unit)
            self.assertEqual(len({q['passage'] for q in bank}),6,unit)
            for key in cases:
                pair=[q for q in bank if case(q)==key]
                self.assertEqual({q['skill'] for q in pair},{'apply','reason'},key)
                self.assertEqual(len({q['lesson'] for q in pair}),1,key)
            for q in bank:
                self.assertIn('-transfer111-',q['id'])
                self.assertTrue(q['hint'] and q['explanation'],q['id'])
                self.assertTrue(server.correct(q,str(q['answer'])),q['id'])
                self.assertFalse(server.correct(q,'a deliberately invalid answer'),q['id'])
                if q['kind']=='choice':
                    self.assertEqual(len({o['text'] for o in q['options']}),len(q['options']),q['id'])
                    self.assertIn(q['answer'],{o['id'] for o in q['options']},q['id'])
                self.assertNotIn('answer',server.public_question(q))
                self.assertNotIn('hint',server.public_question(q))
                self.assertNotIn('explanation',server.public_question(q))
            for seed in range(100):
                drawn=sample_check(bank,server.UNITS[unit]['checkSkills'],random.Random(seed))
                self.assertEqual(len({case(q) for q in drawn}),6,unit)
                self.assertEqual(Counter(q['skill'] for q in drawn),{'apply':3,'reason':3},unit)
                self.assertEqual({q['lesson'] for q in drawn},{1,2},unit)

    def test_new_questions_are_not_published_practice(self):
        published=set()
        def walk(value):
            if isinstance(value,dict):
                if isinstance(value.get('prompt'),str):
                    published.add((value.get('passage','').strip(),value['prompt'].strip()))
                for item in value.values():walk(item)
            elif isinstance(value,list):
                for item in value:walk(item)
        walk(server.CATALOG)
        for unit in UNITS:
            for q in server.BANK[unit]:
                self.assertNotIn((q.get('passage','').strip(),q['prompt'].strip()),published,q['id'])

    def test_science_quantities_and_lesson_order(self):
        # Independent calculations for the authored changed examples.
        expected={('science-3',1):min(7,4),('science-4',1):12/3,
                  ('science-4',4):15/5,('science-7',1):6*8,
                  ('science-10',3):3*2,('science-11',1):8/4,
                  ('science-11',4):5/1,('science-11',6):1/2,
                  ('science-12',4):min(20,3*9),('science-12',5):4*6-20}
        for (unit,index),answer in expected.items():
            q=next(q for q in server.BANK[unit] if q['id']==f'{unit}-transfer111-{index}-apply')
            self.assertEqual(q['kind'],'number',q['id'])
            self.assertEqual(q['answer'],answer,q['id'])
        circuits=[q for q in server.BANK['science-11'] if q['lesson']==1]
        waves=[q for q in server.BANK['science-11'] if q['lesson']==2]
        self.assertTrue(all('resistor' in q['passage'].lower() or 'circuit' in q['passage'].lower() for q in circuits))
        self.assertTrue(all('wave' in q['passage'].lower() for q in waves))


class TransferApiTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_changed_checks_grade_shuffle_failures_and_retries(self):
        learner,_=self.learner()
        fixtures.complete_core_fixture(self.app,learner)
        for unit in sorted(UNITS):
            with self.subTest(unit=unit):
                passed,payload=self.check(learner,unit)
                self.assertEqual(passed['report']['score'],6)
                self.assertTrue(passed['report']['passed'])
                before=passed['me']['points']
                status,repeated,_=learner.request('/api/submit',payload)
                self.assertEqual(status,200)
                self.assertEqual(repeated['report'],passed['report'])
                self.assertEqual(repeated['me']['points'],before)
                failed,_=self.check(learner,unit,wrong=2)
                self.assertEqual(failed['report']['score'],4)
                self.assertFalse(failed['report']['passed'])
                self.assertEqual(failed['me']['points'],before)
                self.assertEqual(len({case(q) for q in passed['report']['questions']}),6)
                expected_ids={q['id'] for q in server.BANK[unit]}
                self.assertTrue(all(q['id'] in expected_ids for q in passed['report']['questions']))

    def test_in_progress_check_uses_its_saved_questions_after_bank_change(self):
        learner,_=self.learner()
        unit='reading-2'
        status,attempt,_=learner.request('/api/attempt',{'unit':unit})
        self.assertEqual(status,200)
        answers=fixtures.right_answers(unit,attempt)
        replacement=copy.deepcopy(server.BANK[unit])
        for q in replacement:
            q['id']='a-later-release-'+q['id']
            q['passage']='A completely different later case.'
        with patch.dict(server.BANK,{unit:replacement}):
            status,resumed,_=learner.request('/api/attempt',{'unit':unit})
            self.assertEqual(status,200)
            self.assertEqual(resumed,attempt)
            status,result,_=learner.request('/api/submit',dict(id=attempt['id'],answers=answers,
                reflection='I checked who performed each action.',support='myself',ink=[]))
            self.assertEqual(status,200,result)
            self.assertEqual(result['report']['score'],6)
            self.assertEqual([q.get('passage','') for q in result['report']['questions']],
                             [q.get('passage','') for q in attempt['questions']])
            self.assertEqual([q['prompt'] for q in result['report']['questions']],
                             [q['prompt'] for q in attempt['questions']])
        guest=fixtures.Client(self.url)
        self.assertEqual(guest.request('/content/check-bank111.json')[0],404)


if __name__=='__main__':unittest.main()
