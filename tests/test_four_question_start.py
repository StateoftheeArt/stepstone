"""A short starting check must stay bounded and preserve older saved journeys."""
import copy
import json
import random
import subprocess
import unittest
import test_adaptive_starting as fixtures
from test_adaptive_starting import BANK, QUESTIONS, response
from placement import evaluate, normalize
import server


class FourQuestionTests(unittest.TestCase):
    def test_four_per_area_and_python_browser_parity(self):
        vectors = []
        for seed in (0, 1, 37, 65535):
            rng = random.Random(seed)
            for pattern in (lambda q: True, lambda q: False, lambda q: rng.random() > .5):
                data = dict(version=3, age=14, seed=seed, answers=[])
                while (result := evaluate(BANK, data))['next']:
                    vectors.append(copy.deepcopy(data))
                    q = QUESTIONS[result['next']]
                    data['answers'].append(response(q, pattern(q)))
                self.assertTrue(result['complete'])
                self.assertEqual(len(data['answers']), 24)
                self.assertEqual(len({a['id'] for a in data['answers']}), 24)
                self.assertTrue(all(a['answered'] == 4 for a in result['areas'].values()))
                self.assertEqual(normalize(data)['version'], 3)
                vectors.append(copy.deepcopy(data))
                with self.assertRaises(ValueError):
                    evaluate(BANK, dict(data, answers=data['answers']+[data['answers'][-1]]))
        code = """import fs from 'node:fs';import {startingPoint} from './public/engine.js';
const {bank,vectors}=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(vectors.map(d=>startingPoint(bank,d))));"""
        run = subprocess.run(['node', '--input-type=module', '-e', code], input=json.dumps(dict(bank=BANK, vectors=vectors)), capture_output=True, text=True, encoding='utf-8', cwd=server.ROOT, check=True)
        self.assertEqual(json.loads(run.stdout), [evaluate(BANK, d) for d in vectors])


class FourQuestionAccounts(unittest.TestCase):
    setUp = fixtures.AdaptiveTests.setUp
    tearDown = fixtures.AdaptiveTests.tearDown
    learner = fixtures.AdaptiveTests.learner

    def test_saved_new_check_and_profile_use_existing_account(self):
        learner, account = self.learner()
        data = dict(version=3, age=14, seed=0, answers=[])
        q = QUESTIONS[evaluate(BANK, data)['next']]
        data['draft'] = dict(id=q['id'], answer='3/', heard=True)
        status, saved, _ = learner.request('/api/starting-point', dict(revision=0, data=data))
        self.assertEqual(status, 200)
        self.assertEqual(saved['data']['draft'], data['draft'])
        status, renamed, _ = learner.request('/api/profile', dict(alias='River', avatar='wave'))
        self.assertEqual(status, 200)
        self.assertEqual(renamed['id'], account['id'])
        self.assertEqual(renamed['alias'], 'River')
        self.assertEqual(renamed['profile']['avatar'], 'wave')
        self.assertEqual(renamed['startingPoint'], saved)
        self.assertEqual(renamed['points'], 0)
        self.assertEqual(learner.request('/api/profile', dict(alias='', avatar='wave'))[0], 400)
        self.assertEqual(learner.request('/api/me')[1]['alias'], 'River')


if __name__ == '__main__':
    unittest.main()
