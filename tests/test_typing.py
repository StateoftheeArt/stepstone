import unittest
import server
from typing_evidence import validate
import test_server as fixtures

class TypingTests(unittest.TestCase):
    def test_summary_has_only_bounded_device_reported_fields(self):
        unit=server.UNITS['typing-keys']
        row=dict(task='keys-lines',accuracy=100,target=95,method='phone',assisted=False)
        self.assertEqual(validate([row],unit,server.Problem),[row])
        for change in [dict(accuracy=True),dict(accuracy=101),dict(target=0),dict(method={}),dict(assisted='no'),dict(rawKeys='private')]:
            with self.assertRaises(server.Problem):validate([dict(row,**change)],unit,server.Problem)
        with self.assertRaises(server.Problem):validate([row,row],unit,server.Problem)
        with self.assertRaises(server.Problem):validate([row],server.UNITS['math-1'],server.Problem)
        with self.assertRaises(server.Problem):validate([dict(row,task='keys-backspace')],unit,server.Problem)
        self.assertTrue(validate([dict(row,method='assistive')],unit,server.Problem)[0]['assisted'])

class TypingReceiptTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner

    def test_reported_accuracy_cannot_pass_a_check_or_change_a_receipt(self):
        client,me=self.learner();fixtures.complete_core_fixture(self.app,client)
        before=client.request('/api/me')[1]['foundation']['completed']
        attempt=client.request('/api/attempt',dict(unit='typing-keys'))[1]
        right=fixtures.right_answers('typing-keys',attempt)
        wrong={q['id']:next(o['id'] for o in q['options'] if o['id']!=right[q['id']]) if q['kind']=='choice' else '99999' for q in attempt['questions']}
        payload=dict(id=attempt['id'],answers=wrong,reflection='Synthetic summary test; not a learner walkthrough.',support='tool',ink=[],typingPractice=[dict(task='keys-lines',accuracy=100,target=95,method='phone',assisted=False)])
        status,result,_=client.request('/api/submit',payload)
        self.assertEqual(status,200)
        self.assertFalse(result['report']['passed']);self.assertEqual(result['report']['score'],0)
        self.assertEqual(result['report']['points'],5)
        self.assertEqual(result['me']['foundation']['completed'],before)
        replay=client.request('/api/submit',dict(payload,typingPractice=[]))[1]
        self.assertEqual(replay['report'],result['report'])
        self.assertEqual(self.mentor.request('/api/mentor')[1]['reports'][0]['report']['typingPractice'],payload['typingPractice'])

if __name__=='__main__':unittest.main()
