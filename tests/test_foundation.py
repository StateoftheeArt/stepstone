"""API/SQLite fixtures for path integrity, not browser completion evidence."""
import copy
import json
import unittest
from unittest.mock import patch
import test_server as base
from foundation import validate


class FoundationTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner
    check=base.PilotTests.check

    def test_manifest_and_server_saved_pass_reach_both_views(self):
        learner,person=self.learner()
        plan=person['foundation']
        self.assertEqual([g['total'] for g in plan['groups']],[8,8,8,8])
        self.assertEqual((plan['completed'],plan['total'],plan['next']),(0,32,'math-cash'))
        result,payload=self.check(learner)
        self.assertEqual(result['me']['foundation']['completed'],1)
        self.assertEqual(result['me']['foundation']['next'],'math-prices')
        # Retrying a lost response cannot award the same check/path step again.
        again=learner.request('/api/submit',payload)[1]['me']
        self.assertEqual((again['foundation']['completed'],again['points']),(1,20))
        self.check(learner)
        self.assertEqual(learner.request('/api/me')[1]['foundation']['completed'],1)
        other=base.Client(self.url)
        self.assertEqual(other.request('/api/login',dict(code=person['recovery']))[1]['foundation'],again['foundation'])
        mentor=self.mentor.request('/api/mentor')[1]['learners'][0]
        self.assertEqual(mentor['foundation'],again['foundation'])

    def test_opening_drafts_or_forging_client_fields_cannot_fill_path(self):
        learner,_=self.learner()
        self.assertEqual(learner.request('/api/progress',dict(unit='math-cash',stage=5,passed=True))[0],200)
        self.assertEqual(learner.request('/api/draft',dict(unit='math-cash',revision=0,data=dict(phase=7,passed=True,score=6,foundation=dict(completed=32))))[0],200)
        self.assertEqual(learner.request('/api/foundation',dict(completed=32))[0],404)
        self.assertEqual(learner.request('/api/me')[1]['foundation']['completed'],0)
        failed,_=self.check(learner,wrong=2)
        self.assertFalse(failed['report']['passed'])
        self.assertEqual(failed['me']['foundation']['completed'],0)
        self.check(learner,'math-1')
        self.assertEqual(learner.request('/api/me')[1]['foundation']['completed'],0)
        other,_=self.learner('Separate account')
        self.check(learner)
        self.assertEqual(other.request('/api/me')[1]['foundation']['completed'],0)

    def test_existing_passes_count_and_assignment_does_not_change_with_release(self):
        learner,person=self.learner()
        self.check(learner)
        # Model an old account with genuine API-submitted work but no path row.
        with self.app.store.db() as db:
            db.execute('DELETE FROM foundation_paths WHERE learner=?',(person['id'],))
        saved=learner.request('/api/me')[1]['foundation']
        self.assertEqual(saved['completed'],1)
        changed=copy.deepcopy(base.server.FOUNDATION)
        changed['version']=3
        changed['groups'][0]['units'].remove('math-cash')
        with patch.object(base.server,'FOUNDATION',changed):
            self.assertEqual(learner.request('/api/me')[1]['foundation'],saved)
            _,new=self.learner('New version')
            self.assertEqual((new['foundation']['version'],new['foundation']['total']),(3,31))

    def test_final_step_and_history_limit_use_exact_saved_units(self):
        learner,person=self.learner()
        ids=[u for g in base.server.FOUNDATION['groups'] for u in g['units']]
        # Synthetic storage fixtures test aggregation independently of the UI.
        with self.app.store.db() as db:
            for i,unit in enumerate(ids[:-1]):
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                           (f'fixture-pass-{i}',person['id'],unit,'[]',1,2,json.dumps(dict(passed=True))))
            for i in range(205):
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                           (f'fixture-review-{i}',person['id'],'math-cash','[]',3,4,json.dumps(dict(passed=False))))
        plan=learner.request('/api/me')[1]['foundation']
        self.assertEqual((plan['completed'],plan['complete'],plan['next']),(31,False,'digital-8'))
        result,_=self.check(learner,'digital-8')
        plan=result['me']['foundation']
        self.assertEqual((plan['completed'],plan['complete'],plan['next']),(32,True,None))
        self.assertEqual(self.mentor.request('/api/mentor')[1]['learners'][0]['foundation'],plan)

    def test_personal_reset_only_replaces_personal_assignment(self):
        learner,person=self.learner()
        self.check(learner)
        own=self.mentor.request('/api/mentor/learn',{})[1]
        reset=self.mentor.request('/api/mentor/reset-learning',dict(learner=own['id'],confirmation='RESET MY LEARNING'))
        self.assertEqual(reset[0],200)
        self.assertNotEqual(reset[1]['id'],own['id'])
        self.assertEqual(reset[1]['foundation']['completed'],0)
        self.assertEqual(learner.request('/api/me')[1]['foundation']['completed'],1)
        with self.app.store.db() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM foundation_paths WHERE learner=?',(own['id'],)).fetchone()[0],0)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM foundation_paths WHERE learner=?',(person['id'],)).fetchone()[0],1)

    def test_manifest_rejects_duplicates_or_missing_modules(self):
        for bad in ('missing-unit','math-cash'):
            plan=copy.deepcopy(base.server.FOUNDATION)
            plan['groups'][1]['units'][0]=bad
            with self.assertRaises(ValueError):validate(plan,base.server.UNITS)


if __name__=='__main__':unittest.main()
