"""Separate mentor groups, browser approval and access recovery on disposable hosts."""
import json
import threading
import unittest
from unittest.mock import patch
import test_server as base


class MentorAccountTests(unittest.TestCase):
    setUp = base.PilotTests.setUp
    tearDown = base.PilotTests.tearDown
    learner = base.PilotTests.learner
    check = base.PilotTests.check

    def second(self):
        client=base.Client(self.url)
        status,result,_=client.request('/api/mentor/setup',dict(username='second-mentor',name='Second mentor',device='Second device',passphrase='second-mentor-test-passphrase'))
        self.assertEqual(status,200,result)
        return client,result

    def test_private_groups_and_cross_group_mutations(self):
        learner,person=self.learner()
        result,_=self.check(learner)
        other,_=self.second()
        invite=other.request('/api/mentor/invite',{})[1]['code']
        other_learner=base.Client(self.url)
        status,other_person,_=other_learner.request('/api/join',dict(code=invite,alias='Other learner',share=True))
        self.assertEqual(status,200)
        own=self.mentor.request('/api/mentor')[1]
        theirs=other.request('/api/mentor')[1]
        self.assertEqual([l['id'] for l in own['learners']],[person['id']])
        self.assertEqual([l['id'] for l in theirs['learners']],[other_person['id']])
        self.assertEqual(theirs['reports'],[])
        report=own['reports'][0]['id']
        for path,data in [('/api/mentor/review',dict(id=report,note='Not my learner')),
                          ('/api/mentor/recovery',dict(id=person['id'])),
                          ('/api/mentor/messages/thread',dict(learner=person['id'])),
                          ('/api/mentor/messages/send',dict(learner=person['id'],choice='seen',clientId='cross-group-test-id')),
                          ('/api/mentor/device-work',dict(learner=person['id']))]:
            self.assertEqual(other.request(path,data)[0],404,(path,data))
        self.assertEqual(learner.request('/api/me')[1]['id'],person['id'])
        self.assertEqual(base.Client(self.url).request('/api/login',dict(code=other_person['recovery']))[1]['id'],other_person['id'])
        self.assertNotEqual(self.app.accounts.root.path,self.app.accounts.by_name['second-mentor'].path)

    def test_devices_require_owner_approval_and_cannot_be_approved_by_another_mentor(self):
        new=base.Client(self.url)
        status,pending,_=new.request('/api/mentor/login',dict(username='test-mentor',passphrase='test-only-mentor-passphrase',device='New test browser'))
        self.assertEqual(status,200)
        self.assertTrue(pending['pending'])
        self.assertEqual(new.request('/api/mentor')[0],401)
        request=self.mentor.request('/api/mentor')[1]['requests'][0]
        self.assertEqual(request['code'],pending['code'])
        other,_=self.second()
        self.assertEqual(other.request('/api/mentor/device-review',dict(id=request['id'],status='approved'))[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/device-review',dict(id=request['id'],status='approved'))[0],200)
        self.assertEqual(new.request('/api/mentor/device-status',{})[1]['ok'],True)
        self.assertEqual(new.request('/api/mentor')[1]['account']['username'],'test-mentor')
        self.assertEqual(new.request('/api/mentor/device-status',{})[0],401)
        device=next(d for d in self.mentor.request('/api/mentor')[1]['devices'] if not d['current'])
        self.assertEqual(self.mentor.request('/api/mentor/device-revoke',dict(id=device['id']))[0],200)
        self.assertEqual(new.request('/api/mentor')[0],401)

    def test_recovery_rotates_key_and_preserves_learners(self):
        other,created=self.second()
        invite=other.request('/api/mentor/invite',{})[1]['code']
        child=base.Client(self.url)
        person=child.request('/api/join',dict(code=invite,alias='Keep my work',share=True))[1]
        fresh=base.Client(self.url)
        data=dict(username='second-mentor',recovery=created['recovery'],passphrase='a-new-test-passphrase',device='Replacement browser')
        status,recovered,_=fresh.request('/api/mentor/recover',data)
        self.assertEqual(status,200,recovered)
        self.assertNotEqual(created['recovery'],recovered['recovery'])
        self.assertEqual(other.request('/api/mentor')[0],401)
        self.assertEqual(fresh.request('/api/mentor')[1]['learners'][0]['id'],person['id'])
        self.assertEqual(child.request('/api/me')[1]['id'],person['id'])
        self.assertEqual(base.Client(self.url).request('/api/mentor/recover',data)[0],401)

    def test_legacy_username_can_sign_in_and_recover_after_filter_upgrade(self):
        credentials=dict(username='sh1t-mentor', name='Legacy mentor', device='Old browser',
                         passphrase='legacy-test-only-passphrase')
        self.assertEqual(base.Client(self.url).request('/api/mentor/setup',credentials)[0],400)
        legacy=base.Client(self.url)
        with patch('mentor_accounts.acceptable',return_value=True):
            status,created,_=legacy.request('/api/mentor/setup',credentials)
        self.assertEqual(status,200,created)
        fresh=base.Client(self.url)
        status,pending,_=fresh.request('/api/mentor/login',credentials)
        self.assertEqual(status,200,pending)
        self.assertTrue(pending['pending'])
        self.assertEqual(fresh.request('/api/mentor')[0],401)
        status,recovered,_=fresh.request('/api/mentor/recover',dict(
            username=credentials['username'], recovery=created['recovery'],
            passphrase='replacement-test-passphrase',device='Replacement browser'))
        self.assertEqual(status,200,recovered)
        self.assertEqual(fresh.request('/api/mentor')[1]['account']['username'],credentials['username'])
        self.assertEqual(legacy.request('/api/mentor')[0],401)

    def test_local_network_and_desktop_do_not_grant_access(self):
        self.app.runtime.desktop=True
        guest=base.Client(self.url)
        self.assertEqual(guest.request('/api/mentor')[0],401)
        self.assertEqual(guest.request('/api/mentor/local',{})[0],401)
        other,_=self.second()
        self.assertFalse(other.request('/api/mentor')[1]['settings']['canManageHost'])
        self.assertEqual(other.request('/api/mentor/settings',dict(keepRunning=False))[0],403)
        self.assertEqual(self.mentor.request('/api/mentor/settings',dict(keepRunning=False),headers={'X-Forwarded-For':'127.0.0.1'})[0],403)
        self.assertTrue(self.mentor.request('/api/mentor')[1]['settings']['canManageHost'])

    def test_restart_recognizes_both_workspaces_and_browser_devices(self):
        other,_=self.second()
        self.app.shutdown();self.app.server_close();self.thread.join()
        port=int(self.url.rsplit(':',1)[1])
        self.app=base.server.create_server(port=port,data=self.tmp.name)
        self.thread=threading.Thread(target=self.app.serve_forever,daemon=True);self.thread.start()
        self.assertEqual(other.request('/api/mentor')[1]['account']['username'],'second-mentor')
        self.assertEqual(self.mentor.request('/api/mentor')[1]['account']['username'],'test-mentor')
        self.assertEqual(other.request('/api/logout',dict(role='mentor'))[0],200)
        self.assertEqual(other.request('/api/mentor')[0],401)
        self.assertEqual(self.mentor.request('/api/mentor')[0],200)

    def test_tokens_cannot_change_workspace_by_changing_prefix(self):
        learner,person=self.learner()
        other,_=self.second()
        otherid=other.request('/api/mentor')[1]['account']['id']
        tampered='w'+otherid+'.'+person['recovery'].split('.')[1]
        self.assertEqual(base.Client(self.url).request('/api/login',dict(code=tampered))[0],401)
        self.assertEqual(base.Client(self.url).request('/api/login',dict(code='w../../data.bad'))[0],401)
        self.assertEqual(learner.request('/api/me')[0],200)

    def test_only_failed_sign_ins_count_and_one_username_cannot_lock_out_another(self):
        _,person=self.learner()
        # Many successful sign-ins from one shared address never trigger a lockout.
        for _ in range(15):self.assertEqual(base.Client(self.url).request('/api/login',dict(code=person['recovery']))[0],200)
        other,_=self.second()
        stranger=base.Client(self.url)
        for _ in range(12):
            self.assertEqual(stranger.request('/api/mentor/login',dict(username='second-mentor',device='Guess',passphrase='not-the-right-passphrase'))[0],401)
        self.assertEqual(stranger.request('/api/mentor/login',dict(username='second-mentor',device='Guess',passphrase='second-mentor-test-passphrase'))[0],429)
        # Another mentor on the same address can still sign in.
        status,result,_=base.Client(self.url).request('/api/mentor/login',dict(username='test-mentor',device='Laptop',passphrase='test-only-mentor-passphrase'))
        self.assertEqual(status,200,result);self.assertTrue(result['pending'])
        for _ in range(12):self.assertEqual(stranger.request('/api/login',dict(code='w'+'x'*40))[0],401)
        self.assertEqual(stranger.request('/api/login',dict(code=person['recovery']))[0],429)

    def test_forwarded_address_is_trusted_only_when_hosted(self):
        bad=dict(code='w'+'x'*40)
        # On a desktop host a forged header is ignored: failures count against the real address.
        for _ in range(12):self.assertEqual(base.Client(self.url).request('/api/login',bad,headers={'X-Forwarded-For':'203.0.113.9'})[0],401)
        self.assertEqual(base.Client(self.url).request('/api/login',bad,headers={'X-Forwarded-For':'198.51.100.7'})[0],429)
        self.app.logins.clear();self.app.trust_forwarded=True
        # Hosted: the proxy appends the connecting address, so only the last entry counts.
        for _ in range(12):self.assertEqual(base.Client(self.url).request('/api/login',bad,headers={'X-Forwarded-For':'198.51.100.7, 203.0.113.9'})[0],401)
        self.assertEqual(base.Client(self.url).request('/api/login',bad,headers={'X-Forwarded-For':'203.0.113.9'})[0],429)
        self.assertEqual(base.Client(self.url).request('/api/login',bad,headers={'X-Forwarded-For':'203.0.113.9, 198.51.100.7'})[0],401)

    def test_health_answers_a_hosting_check_on_another_domain(self):
        status,health,_=base.Client(self.url).request('/api/health',headers={'Host':'custom-domain.example'})
        self.assertEqual(status,200);self.assertFalse(health['localClaim'])
        self.assertEqual(base.Client(self.url).request('/api/me',headers={'Host':'custom-domain.example'})[0],403)
        self.assertEqual(base.Client(self.url).request('/api/presence',{},headers={'Host':'custom-domain.example'})[0],403)


if __name__=='__main__':unittest.main()
