"""Disposable account fixtures, not learner completion evidence."""
import uuid
import unittest
import test_server as fixtures
from test_server import Client


class MentorMessagesTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner

    def message(self,choice='stuck',**extra):
        return dict(choice=choice,clientId=uuid.uuid4().hex,**extra)

    def test_connected_profile_options_and_reload(self):
        child,me=self.learner(tutorial=False)
        value=dict(alias='North',avatar='axolotl',companionName='Pip',accessory='none',badge='aurora',accent='mint',motivation='work',interests=['digital'],nextWin='',introReady=True)
        response=child.request('/api/profile',value)
        self.assertEqual(response[0],200,response[1])
        current=child.request('/api/me')[1]
        self.assertEqual(current['profile']['avatar'],'axolotl')
        self.assertTrue(current['profile']['introReady']);self.assertEqual(current['profile']['accessory'],'none')
        self.assertEqual(current['points'],0);self.assertEqual(current['totalChecks'],0)
        self.assertEqual(child.request('/api/profile',{**value,'accessory':'scarf'})[0],409)
        self.assertEqual(child.request('/api/profile',{**value,'accessory':'unknown'})[0],400)
        self.assertEqual(Client(self.url).request('/api/profile',value)[0],401)

    def test_inbox_read_reply_and_no_rewards(self):
        child,me=self.learner(tutorial=False)
        payload=self.message('stuck')
        self.assertEqual(child.request('/api/messages/send',payload)[0],200)
        item=self.mentor.request('/api/mentor')[1]['messages'][0]
        self.assertEqual((item['id'],item['unread']),(me['id'],1))
        data=self.mentor.request('/api/mentor/messages/thread',{'learner':me['id']})[1]
        self.assertEqual(data['messages'][0]['body'],'I’m stuck.')
        self.assertEqual(len(data['options']),6)
        self.assertEqual(self.mentor.request('/api/mentor')[1]['messages'][0]['unread'],0)
        self.assertEqual(self.mentor.request('/api/mentor/messages/send',self.message('reviewing',learner=me['id']))[0],200)
        self.assertEqual(child.request('/api/me')[1]['messagesUnread'],1)
        self.assertEqual(len(child.request('/api/messages/thread',{})[1]['messages']),2)
        info=child.request('/api/me')[1]
        self.assertEqual(info['messagesUnread'],0);self.assertEqual(info['points'],0)

    def test_private_boundaries_and_plain_text_limits(self):
        first,one=self.learner(tutorial=False);second,two=self.learner('Second',tutorial=False)
        self.assertEqual(first.request('/api/messages/send',self.message())[0],200)
        self.assertEqual(second.request('/api/messages/thread',{'learner':one['id']})[0],409)
        self.assertEqual(second.request('/api/messages/send',self.message(learner=one['id']))[0],409)
        self.assertEqual(second.request('/api/messages/thread',{})[1]['messages'],[])
        self.assertEqual(first.request('/api/mentor/messages/thread',{'learner':one['id']})[0],401)
        self.assertEqual(Client(self.url).request('/api/messages/send',self.message())[0],401)
        for choice in ('','  ','x'*1501,'x\x00y',{'id':'stuck'},'feedback-ready'):
            self.assertEqual(first.request('/api/messages/send',self.message(choice))[0],400)
        for body in ('Arbitrary text','<b>A question</b>\nhttps://example.org'):
            self.assertEqual(first.request('/api/messages/send',self.message(text=body))[0],400)
        self.assertEqual(first.request('/api/messages/send',dict(text='I’m stuck.',clientId=uuid.uuid4().hex))[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/messages/send',self.message('stuck',learner=one['id']))[0],400)
        self.assertEqual(first.request('/api/messages/send',self.message(attachment='fake.png'))[0],400)
        self.assertEqual(first.request('/api/messages/send',self.message(sender='mentor'))[0],400)
        self.assertEqual(first.request('/api/messages/thread',{'before':['invalid']})[0],400)
        self.assertEqual(first.request('/api/messages/send',self.message(),headers={'Origin':'https://wrong.example'})[0],403)

    def test_retry_sends_once_and_rate_limit_preserves_inbox(self):
        child,me=self.learner(tutorial=False);payload=self.message()
        first=child.request('/api/messages/send',payload)
        self.assertEqual(child.request('/api/messages/send',payload)[1],first[1])
        self.assertEqual(child.request('/api/messages/send',{**payload,'choice':'review'})[0],409)
        for _ in range(4):self.assertEqual(child.request('/api/messages/send',self.message())[0],200)
        self.assertEqual(child.request('/api/messages/send',self.message())[0],429)
        self.assertEqual(len(child.request('/api/messages/thread',{})[1]['messages']),5)

    def test_old_pages_stay_private_and_personal_reset_does_not_erase_children(self):
        child,me=self.learner(tutorial=False);other,other_me=self.learner('Other',tutorial=False)
        # Pagination fixture is deliberately labelled; no browser completion claimed.
        with self.app.store.db() as db:
            for i in range(64):db.execute('INSERT INTO mentor_messages VALUES(?,?,?,?,?,NULL,?)',(str(i),me['id'],'learner',f'Message {i}',100+i,f'fixture-{i}'))
        page=child.request('/api/messages/thread',{})[1]
        self.assertEqual(len(page['messages']),60);self.assertTrue(page['hasOlder'])
        self.assertTrue(all(m.get('legacy') for m in page['messages']))
        self.assertTrue(all('Message 6' not in m['body'] for m in page['messages']))
        older=child.request('/api/messages/thread',{'before':page['messages'][0]['id']})[1]
        self.assertEqual(len(older['messages']),4);self.assertFalse(older['hasOlder'])
        self.assertEqual(other.request('/api/messages/thread',{'before':page['messages'][0]['id']})[0],404)
        own=self.mentor.request('/api/mentor/learn',{})[1]
        self.assertEqual(self.mentor.request('/api/messages/send',self.message())[0],403)
        self.assertEqual(self.mentor.request('/api/mentor/reset-learning',{'learner':own['id'],'confirmation':'RESET MY LEARNING'})[0],200)
        self.assertEqual(len(child.request('/api/messages/thread',{})[1]['messages']),60)


if __name__=='__main__':unittest.main()
