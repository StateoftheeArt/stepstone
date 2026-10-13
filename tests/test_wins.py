"""First-pass cosmetic attribution in disposable learner accounts."""
import json
import unittest
import test_server as fixtures
from test_server import Client


class SubjectWinsTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_items_stay_with_first_module_pass_across_retries_and_devices(self):
        child,account=self.learner()
        self.assertEqual(child.request('/api/me')[1]['moduleWins'],[])
        first,_=self.check(child,'math-1')
        initial=first['me']['moduleWins'][0]
        self.assertEqual({x['key'] for x in initial['pipItems']},set())
        second,_=self.check(child,'reading-1')
        reading=second['me']['moduleWins'][1]
        self.assertEqual({x['key'] for x in reading['pipItems']},{'accessory:sprout'})
        self.check(child,'math-1')
        self.check(child,'math-1',wrong=2)
        current=child.request('/api/me')[1]
        self.assertEqual(current['moduleWins'],[initial,reading])
        balance=current['points']
        self.assertEqual(child.request('/api/me')[1]['points'],balance,'Viewing wins never awards or spends points.')
        returning=Client(self.url)
        loaded=returning.request('/api/login',dict(code=account['recovery']))[1]
        self.assertEqual(loaded['moduleWins'],current['moduleWins'])
        other,_=self.learner('Other learner')
        self.assertEqual(other.request('/api/me')[1]['moduleWins'],[])
        self.assertEqual(Client(self.url).request('/api/me')[0],401)
        self.assertNotIn('questions',initial['report'],'The archive is a lean completion summary.')

    def test_failed_checks_do_not_receive_items(self):
        child,_=self.learner()
        failed,_=self.check(child,'math-1',wrong=2)
        self.assertEqual(failed['me']['moduleWins'],[])
        passed,_=self.check(child,'math-1')
        win=passed['me']['moduleWins'][0]
        self.assertEqual(win['report']['tryNumber'],2)
        self.assertEqual(len(win['pipItems']),0)

    def test_first_pass_archive_survives_recent_history_limit(self):
        child,account=self.learner()
        # Explicit history fixture in the temporary test store, not learning evidence.
        with self.app.store.db() as db:
            for index in range(205):
                unit='reading-1' if index==1 else 'math-1'
                report=dict(title=unit,score=6,passed=True,tryNumber=index+1)
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                    ('history-'+str(index),account['id'],unit,'[]',index+1,index+2,json.dumps(report)))
        current=child.request('/api/me')[1]
        self.assertEqual(len(current['attempts']),200)
        self.assertEqual([x['unit'] for x in current['moduleWins']],['math-1','reading-1'])
        self.assertEqual(current['moduleWins'][0]['finished'],2)
        self.assertEqual(current['moduleWins'][0]['report']['total'],6)
        self.assertEqual({x['key'] for x in current['moduleWins'][1]['pipItems']},{'accessory:sprout'})

    def test_remaining_milestones_do_not_repeat_after_the_collection_is_complete(self):
        child,_=self.learner()
        for index in range(1,7):self.check(child,'math-'+str(index))
        wins=child.request('/api/me')[1]['moduleWins']
        self.assertEqual([{item['key'] for item in win['pipItems']} for win in wins],
                         [set(),{'accessory:sprout'},set(),{'accessory:bandana','home.rug:woven'},set(),
                          {'accessory:cap','home.decor:lamp'}])
        keys=[item['key'] for win in wins for item in win['pipItems']]
        self.assertEqual(len(keys),len(set(keys)))
        self.check(child,'math-6')
        self.assertEqual(child.request('/api/me')[1]['moduleWins'],wins)


if __name__=='__main__':unittest.main()
