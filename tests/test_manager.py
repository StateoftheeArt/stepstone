"""Manager boundaries and desktop lifetime; all accounts use temporary databases."""
import json
import threading
import unittest
from host_runtime import HostRuntime, shared_address
import test_server as base


class ManagerTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner

    def test_host_setting_requires_local_mentor_and_desktop_mode(self):
        guest=base.Client(self.url)
        self.assertEqual(guest.request('/api/mentor/settings',{'keepRunning':False})[0],401)
        learner,_=self.learner()
        self.assertEqual(learner.request('/api/mentor/settings',{'keepRunning':False})[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':False})[0],403)
        self.app.runtime.desktop=True
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':'false'})[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':False},headers={'Origin':'https://outside.invalid'})[0],403)
        port=self.app.server_address[1]
        self.app.allowed_hosts.add(f'stepstone.invalid:{port}')
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':False},headers={'Host':f'stepstone.invalid:{port}'})[0],403)
        self.assertTrue(self.app.runtime.keep_running)

    def test_setting_survives_restart_and_keeps_learning_records(self):
        self.app.runtime.desktop=True
        learner,person=self.learner()
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':False})[0],200)
        self.assertFalse(self.mentor.request('/api/mentor')[1]['settings']['keepRunning'])
        other=base.server.create_server(port=0,data=self.tmp.name,desktop=True)
        try:self.assertFalse(other.runtime.keep_running)
        finally:other.server_close()
        self.assertEqual(learner.request('/api/me')[1]['id'],person['id'])
        self.assertEqual(self.mentor.request('/api/mentor/settings',{'keepRunning':True})[0],200)
        self.assertTrue(self.app.runtime.keep_running)

    def test_invite_link_is_one_use_and_lands_in_existing_account_flow(self):
        self.app.public_url='https://learning.example'
        invite=self.mentor.request('/api/mentor/invite',{})[1]
        self.assertEqual(invite['url'],'https://learning.example/#join/'+invite['code'])
        self.assertTrue(invite['sharingReady'])
        learner=base.Client(self.url)
        self.assertEqual(learner.request('/api/join',dict(code=invite['code'],alias='Link test',share=True))[0],200)
        self.assertEqual(base.Client(self.url).request('/api/join',dict(code=invite['code'],alias='Duplicate',share=True))[0],400)

    def test_presence_does_not_grant_access(self):
        self.app.runtime=HostRuntime(desktop=True,clock=lambda:20)
        self.app.runtime.last_seen=0
        guest=base.Client(self.url)
        self.assertEqual(guest.request('/api/presence',{})[0],200)
        self.assertEqual(self.app.runtime.last_seen,20)
        self.assertEqual(guest.request('/api/mentor')[0],401)

    def test_desktop_server_exits_after_idle_opt_out(self):
        self.app.runtime=HostRuntime(desktop=True,keep_running=False,clock=lambda:500)
        self.app.runtime.last_seen=0
        self.thread.join(timeout=2)
        self.assertFalse(self.thread.is_alive())


class LifetimeTests(unittest.TestCase):
    def test_idle_requires_opt_out_and_resets_when_a_page_checks_in(self):
        now=[0];runtime=HostRuntime(desktop=True,clock=lambda:now[0])
        now[0]=1000;self.assertFalse(runtime.due())
        runtime.set_background(False);self.assertFalse(runtime.due())
        now[0]+=179;self.assertFalse(runtime.due())
        runtime.touch();now[0]+=179;self.assertFalse(runtime.due())
        now[0]+=1;self.assertTrue(runtime.due())
        runtime.desktop=False;self.assertFalse(runtime.due())

    def test_shared_address_cannot_turn_http_preview_into_public_hosting(self):
        for url in ('http://example.com','https://localhost','https://user:secret@example.com','https://example.com/#join/test','https://example.com/app','https://example.com:bad'):
            with self.assertRaises(ValueError):shared_address(url,True)
        with self.assertRaises(ValueError):shared_address('https://example.com',False)
        self.assertEqual(shared_address('https://EXAMPLE.com/',True),'https://example.com')


if __name__=='__main__':unittest.main()
