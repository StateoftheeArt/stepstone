"""Synthetic protocol checks; browser walkthrough evidence is recorded separately."""
import unittest
import test_server as base

class PCCourseTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner
    check=base.PilotTests.check

    def test_identity_confirmation_and_revision_boundaries(self):
        first,me=self.learner();second,other=self.learner('Other learner')
        report=dict(unit='pc-start',revision=0,status='practised',note='Synthetic practice report.',steps=[True]*3)
        self.assertEqual(first.request('/api/device-work',dict(report,status='confirmed'))[0],400)
        self.assertEqual(first.request('/api/device-work',dict(report,steps=[True,False,True]))[0],400)
        self.assertEqual(first.request('/api/device-work',dict(report,steps=[1,1,1]))[0],400)
        self.assertEqual(first.request('/api/device-work',dict(report,unit={}))[0],400)
        self.assertEqual(second.request('/api/device-work',dict(report,learner=me['id']))[0],409)
        self.assertEqual(first.request('/api/device-work',report)[0],200)
        self.assertEqual(first.request('/api/device-work',report)[0],409)
        self.assertEqual(second.request('/api/me')[1]['deviceWork'],[])
        review=dict(unit='pc-start',learner=me['id'],revision=1,status='confirmed',note='Synthetic observed fixture.',observed=True)
        self.assertEqual(first.request('/api/mentor/device-work',review)[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/device-work',review)[0],400)
        self.check(first,'pc-start')
        self.assertEqual(self.mentor.request('/api/mentor/device-work',dict(review,observed=False))[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/device-work',review)[0],200)
        self.assertEqual(self.mentor.request('/api/mentor/device-work',review)[0],409)
        record=first.request('/api/me')[1]['deviceWork'][0]
        self.assertEqual(record['status'],'confirmed')
        self.assertEqual(record['revision'],2)
        self.assertEqual(first.request('/api/device-work',dict(report,revision=2,status='help',note='Changed setup; please review.'))[0],200)
        record=first.request('/api/me')[1]['deviceWork'][0]
        self.assertEqual(record['status'],'help')
        self.assertEqual(record['review_note'],'')
        with self.app.store.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM device_work_history WHERE learner=?',(me['id'],)).fetchone()[0],3)

    def test_pc_checks_do_not_fill_foundation_or_give_rewards(self):
        client,me=self.learner();base.complete_core_fixture(self.app,client)
        before=client.request('/api/me')[1]['foundation']['completed']
        for unit in ('pc-start','pc-files','pc-safe','pc-software','pc-recover'):
            result,_=self.check(client,unit)
            self.assertTrue(result['report']['passed'])
        state=client.request('/api/me')[1]
        self.assertEqual(state['foundation']['completed']-before,2)
        self.assertEqual(state['deviceWork'],[])
        self.assertFalse(any(r.get('available') for r in state['rewards'] if r.get('milestone')))

    def test_waiting_and_help_do_not_require_a_computer_or_pass(self):
        client,me=self.learner()
        for revision,status in enumerate(('waiting','help','waiting')):
            self.assertEqual(client.request('/api/device-work',dict(unit='pc-files',revision=revision,status=status,note='Need access to a computer.'))[0],200)
        self.assertEqual(client.request('/api/device-work',dict(unit='math-1',revision=0,status='waiting',note='Wrong type.'))[0],400)
        self.assertEqual(client.request('/api/me')[1]['deviceWork'][0]['status'],'waiting')
        self.assertEqual(self.mentor.request('/api/mentor')[1]['learners'][0]['deviceWork'][0]['revision'],3)

if __name__=='__main__':unittest.main()
