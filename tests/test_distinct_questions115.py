"""Distinct pools and stateless previews in disposable test databases."""
import copy
import json
from pathlib import Path
import random
import sys
import tempfile
import threading
import unittest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP/'content'))
import server
from distinct_questions import refine,question_key
from check_sampling import sample_check,case
from test_server import Client,right_answers

def published(units):
    found={}
    def walk(value,uid):
        if isinstance(value,dict):
            if isinstance(value.get('prompt'),str):found.setdefault(question_key(value),set()).add(uid)
            for item in value.values():walk(item,uid)
        elif isinstance(value,list):
            for item in value:walk(item,uid)
    for unit in units:
        if unit['ready']:walk(unit,unit['id'])
    return found

class DistinctQuestionTests(unittest.TestCase):
    def test_all_modules_have_unique_practice_and_private_checks(self):
        public=published(server.CATALOG['units'])
        self.assertTrue(all(len(uids)==1 for uids in public.values()))
        practice=[question_key(q) for u in server.UNITS.values() for q in u['practice']]
        private=[question_key(q) for bank in server.BANK.values() for q in bank]
        self.assertEqual(len(practice),len(set(practice)))
        self.assertEqual(len(private),len(set(private)))
        self.assertFalse(set(private)&set(public))
        for uid,unit in server.UNITS.items():
            self.assertGreaterEqual(len(unit['practice']),6,uid)
            for seed in range(20):
                chosen=sample_check(server.BANK[uid],unit.get('checkSkills',('calculate','apply','reason')),random.Random(seed))
                self.assertEqual(len({case(q) for q in chosen}),6,uid)

    def test_refinement_is_idempotent_and_keeps_existing_ids(self):
        catalog=copy.deepcopy(server.CATALOG);bank=copy.deepcopy(server.BANK)
        before=json.dumps([catalog,bank],sort_keys=True)
        refine(catalog['units'],bank)
        self.assertEqual(json.dumps([catalog,bank],sort_keys=True),before)
        recovery=next(u for u in catalog['units'] if u['id']=='pc-recover')
        self.assertFalse({question_key(q) for q in recovery['practice']} &
                         {question_key(q) for labs in recovery['mission']['labs'] for q in labs},
                         'Recovery practice must transfer the skill to fresh situations.')

class PreviewCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='stepstone115-preview-test-')
        self.app=server.create_server(port=0,data=self.tmp.name)
        self.thread=threading.Thread(target=self.app.serve_forever,daemon=True);self.thread.start()
        self.client=Client(f'http://127.0.0.1:{self.app.server_port}')
    def tearDown(self):
        self.app.shutdown();self.app.server_close();self.thread.join();self.tmp.cleanup()
    def records(self):
        with self.app.store.db() as db:
            tables=[row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
            return {table:[tuple(row) for row in db.execute('SELECT * FROM "'+table+'" ORDER BY rowid')] for table in tables}

    def test_new_preview_uses_unseen_cases_grades_and_writes_no_records(self):
        before=self.records();bank_before=json.dumps(server.BANK,sort_keys=True)
        public=set(published(server.CATALOG['units']))
        for uid in ['math-cash','writing-6','writing-10','social-2','social-9','science-weather','pc-recover']:
            status,attempt,headers=self.client.request('/api/preview-check',dict(unit=uid))
            self.assertEqual(status,200,attempt);self.assertEqual(headers['Cache-Control'],'no-store')
            self.assertTrue(attempt['remotePreview']);self.assertEqual(len(attempt['questions']),6)
            for question in attempt['questions']:
                self.assertFalse({'answer','explanation','hint'}&set(question))
                self.assertNotIn(question_key(question),public)
            answers=right_answers(uid,attempt)
            payload=dict(unit=uid,questions=[q['id'] for q in attempt['questions']],answers=answers)
            status,result,_=self.client.request('/api/preview-result',payload)
            self.assertEqual(status,200,result);self.assertEqual(result['score'],6)
            self.assertTrue(result['passed']);self.assertEqual(result['points'],0)
            for q in attempt['questions'][:2]:answers[q['id']]='not an answer'
            status,result,_=self.client.request('/api/preview-result',payload)
            self.assertEqual(status,200);self.assertFalse(result['passed']);self.assertEqual(result['score'],4)
        self.assertEqual(self.records(),before,'Preview must not create learning, account or reward records')
        self.assertEqual(json.dumps(server.BANK,sort_keys=True),bank_before,'Shuffling a preview must not mutate the source bank')

    def test_invalid_and_older_checks_preserve_records_and_return_errors(self):
        before=self.records()
        self.assertEqual(self.client.request('/api/preview-check',{'unit':'missing'})[0],400)
        self.assertEqual(self.client.request('/api/preview-check',{'unit':'math-cash'},headers={'Origin':'https://unrelated.example'})[0],403)
        attempt=self.client.request('/api/preview-check',{'unit':'math-cash'})[1]
        ids=[q['id'] for q in attempt['questions']];answers=right_answers('math-cash',attempt)
        self.assertEqual(self.client.request('/api/preview-result',dict(unit='math-cash',questions=ids,answers={}))[0],400)
        self.assertEqual(self.client.request('/api/preview-result',dict(unit='math-cash',questions=ids[:5]+[ids[0]],answers=answers))[0],400)
        status,error,_=self.client.request('/api/preview-result',dict(unit='math-cash',questions=['old-check']+ids[1:],answers=answers))
        self.assertEqual(status,409);self.assertIn('still saved',error['error'])
        self.assertEqual(self.records(),before)

if __name__=='__main__':unittest.main()
