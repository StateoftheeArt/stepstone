"""New feature boundaries, using synthetic records in temporary databases."""
import json
import unittest
import time
import test_server as fixtures
from test_server import Client
import server

class EngagementTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check



    def test_retired_practice_endpoint_cannot_award_points(self):
        client,me=self.learner()
        before=client.request('/api/me')[1]['points']
        status,_,_=client.request('/api/activity',dict(id='retired',game='cash',answers={}))
        self.assertEqual(status,404)
        self.assertEqual(client.request('/api/me')[1]['points'],before)
        self.assertNotIn('activities',client.request('/api/me')[1])
        self.assertNotIn('activities',self.mentor.request('/api/mentor')[1])

    def test_draft_cross_device_conflict_and_ownership(self):
        first,me=self.learner();second=Client(self.url)
        second.request('/api/login',dict(code=me['recovery']))
        draft=dict(learner=me['id'],unit='writing-12',revision=0,data=dict(phase=5,reflection='A shelf project with a review date.',ink=[[[.1,.2],[.4,.6]]]))
        self.assertEqual(first.request('/api/draft',draft)[1]['revision'],1)
        remote=second.request('/api/drafts')[1]['writing-12']
        self.assertEqual(remote['data'],draft['data'])
        draft['data']['reflection']='A stale version'
        self.assertEqual(second.request('/api/draft',draft)[0],409)
        self.assertEqual(first.request('/api/drafts')[1]['writing-12']['data']['reflection'],remote['data']['reflection'])
        draft['revision']=1
        self.assertEqual(second.request('/api/draft',draft)[1]['revision'],2)
        other,_=self.learner('Sibling')
        self.assertEqual(other.request('/api/drafts')[1],{})
        self.assertEqual(other.request('/api/draft',draft)[0],409)
        first.request('/api/logout',dict(role='learner'))
        self.assertEqual(first.request('/api/drafts')[0],401)
        first.request('/api/login',dict(code=me['recovery']))
        self.assertEqual(first.request('/api/drafts')[1]['writing-12']['revision'],2)

    def test_draft_size_ink_and_revision_validation(self):
        client,_=self.learner()
        base=dict(unit='math-cash',revision=0,data={'phase':1})
        for revision in (True,-1,'0'):
            self.assertEqual(client.request('/api/draft',base|dict(revision=revision))[0],400)
        self.assertEqual(client.request('/api/draft',base|dict(data={'phase':8}))[0],400)
        self.assertEqual(client.request('/api/draft',base|dict(data={'phase':1,'ink':[[[2,0]]]}))[0],400)
        # Maximum supported drawing fits inside the actual request-size limit.
        base['data']['ink']=[[[.123,.456]]*300 for _ in range(20)]
        self.assertLess(len(json.dumps(base).encode()),server.MAX_BODY)
        self.assertEqual(client.request('/api/draft',base)[0],200)

    def test_profile_follows_account_and_is_validated(self):
        client,me=self.learner()
        self.assertEqual(client.request('/api/profile',dict(avatar='pixel'))[1]['profile']['avatar'],'pixel')
        other=Client(self.url)
        self.assertEqual(other.request('/api/login',dict(code=me['recovery']))[1]['profile']['avatar'],'pixel')
        self.assertEqual(client.request('/api/profile',dict(avatar='<script>'))[0],400)

    def test_pip_identity_reaches_mentor_and_survives_recovery(self):
        client,me=self.learner()
        before=client.request('/api/me')[1]
        client.request('/api/draft',dict(unit='math-1',revision=0,data=dict(phase=3)))
        saved=client.request('/api/profile',dict(alias='Sprout',avatar='turtle',accent='violet'))
        self.assertEqual(saved[0],200)
        returning=Client(self.url)
        recovered=returning.request('/api/login',dict(code=me['recovery']))[1]
        self.assertEqual((recovered['alias'],recovered['profile']['avatar']),('Sprout','turtle'))
        self.assertEqual(recovered['points'],before['points'])
        self.assertEqual(recovered['progress'],before['progress'])
        self.assertEqual(returning.request('/api/drafts')[1]['math-1']['data']['phase'],3)
        learner=self.mentor.request('/api/mentor')[1]['learners'][0]
        self.assertEqual((learner['alias'],learner['profile']),('Sprout',dict(avatar='turtle')))
        thread=self.mentor.request('/api/mentor/messages/thread',dict(learner=me['id']))
        self.assertEqual(thread[0],200)
        self.assertEqual(thread[1]['alias'],'Sprout')

    def test_profile_name_limits_and_atomic_rejection(self):
        client,me=self.learner()
        status,result,_=client.request('/api/profile',dict(avatar='fox',alias='N'*12,companionName='P'*12))
        self.assertEqual(status,200)
        self.assertEqual(result['alias'],'N'*12)
        self.assertEqual(result['profile']['companionName'],'P'*12)
        self.assertEqual(client.request('/api/profile',dict(avatar='fox',alias='N'*13))[0],400)
        self.assertEqual(client.request('/api/profile',dict(avatar='fox',alias='Changed',companionName='P'*13))[0],400)
        unchanged=client.request('/api/me')[1]
        self.assertEqual(unchanged['alias'],'N'*12)
        self.assertEqual(unchanged['profile']['companionName'],'P'*12)

    def test_join_rejects_long_nickname_without_consuming_invite(self):
        code=self.mentor.request('/api/mentor/invite',{})[1]['code']
        client=Client(self.url)
        self.assertEqual(client.request('/api/join',dict(code=code,alias='N'*17,share=True))[0],400)
        self.assertEqual(client.request('/api/join',dict(code=code,alias='N'*16,share=True))[0],200)

    def test_existing_long_names_survive_profile_changes(self):
        client,me=self.learner()
        alias='Alexandria Macintosh';pip='Pip the explorer'
        with self.app.store.db() as db:
            db.execute('UPDATE learners SET alias=? WHERE id=?',(alias,me['id']))
            db.execute('UPDATE profiles SET details=? WHERE learner=?',(server.pack(dict(companionName=pip)),me['id']))
        status,result,_=client.request('/api/profile',dict(avatar='dragon',alias=alias,companionName=pip,accent='violet'))
        self.assertEqual(status,200)
        self.assertEqual(result['alias'],alias)
        self.assertEqual(result['profile']['companionName'],pip)
        self.assertEqual(result['profile']['accent'],'violet')
        self.assertEqual(client.request('/api/profile',dict(avatar='dragon',alias=alias+'!'))[0],400)
        self.assertEqual(client.request('/api/profile',dict(avatar='dragon',companionName=pip+'!'))[0],400)
        returning=Client(self.url)
        self.assertEqual(returning.request('/api/login',dict(code=me['recovery']))[1]['alias'],alias)

    def test_all_companions_and_colours_save_to_their_owner(self):
        client,me=self.learner()
        other,_=self.learner('Another learner')
        before=other.request('/api/me')[1]['profile']
        for avatar in server.PROFILE_OPTIONS['companions']:
            for accent in server.PROFILE_OPTIONS['accents']:
                status,result,_=client.request('/api/profile',dict(avatar=avatar,accent=accent['id']))
                self.assertEqual(status,200,(avatar,accent['id']))
                self.assertEqual(result['profile']['avatar'],avatar)
                self.assertEqual(result['profile']['accent'],accent['id'])
        returning=Client(self.url)
        self.assertEqual(returning.request('/api/login',dict(code=me['recovery']))[1]['profile'],result['profile'])
        self.assertEqual(other.request('/api/me')[1]['profile'],before)

    def test_old_mastery_is_not_lost_after_200_attempts(self):
        client,me=self.learner();self.check(client,unit='math-1')
        with self.app.store.db() as db:
            for i in range(205):
                report={'passed':False,'unit':'math-2','at':time.time()+i}
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',(f'synthetic-{i}',me['id'],'math-2','[]',1,time.time()+i,server.pack(report)))
        state=client.request('/api/me')[1]
        self.assertEqual(len(state['attempts']),200)
        self.assertEqual(state['totalChecks'],206)
        self.assertEqual(state['mastered'],['math-1'])
        self.assertEqual(self.mentor.request('/api/mentor')[1]['learners'][0]['passed'],1)

    def test_refund_does_not_inflate_lifetime_experience(self):
        client,me=self.learner();self.check(client)
        reward=self.mentor.request('/api/mentor/reward',dict(title='Test reward',description='Synthetic only',cost=20))[1]['id']
        state=client.request('/api/reward',dict(id=reward))[1]['me']
        self.assertEqual(state['points'],0);self.assertEqual(state['earned'],20)
        claim=state['claims'][0]['id']
        self.mentor.request('/api/mentor/claim',dict(id=claim,status='declined',note='Test refund'))
        state=client.request('/api/me')[1]
        self.assertEqual(state['points'],20);self.assertEqual(state['earned'],20)

    def test_proxy_host_cannot_claim_existing_records(self):
        self.app.allowed_hosts.add('school.example')
        health=Client(self.url).request('/api/health',headers={'Host':'school.example'})[1]
        self.assertFalse(health['localClaim'])

    def test_every_module_has_a_valid_six_question_check(self):
        client,_=self.learner()
        fixtures.complete_core_fixture(self.app,client)
        self.assertEqual(len(server.UNITS),153)
        for unit in server.UNITS:
            status,attempt,_=client.request('/api/attempt',dict(unit=unit))
            self.assertEqual(status,200,unit)
            self.assertEqual(len(attempt['questions']),6,unit)
            self.assertEqual(len({(q.get('passage',''),q['prompt']) for q in attempt['questions']}),6,unit)
            self.assertEqual(len({q.get('caseId',q['prompt']) for q in attempt['questions']}),6,unit)
            self.assertTrue(all('answer' not in q and 'explanation' not in q for q in attempt['questions']),unit)
            if 'checkSkills' in server.UNITS[unit]:
                self.assertEqual({q['lesson'] for q in attempt['questions']},{1,2},unit)
                self.assertEqual({skill:sum(q['skill']==skill for q in attempt['questions']) for skill in server.UNITS[unit]['checkSkills']},
                                 {skill:6//len(server.UNITS[unit]['checkSkills']) for skill in server.UNITS[unit]['checkSkills']},unit)

    def test_support_check_resumes_then_retries_with_the_same_skill_coverage(self):
        client,_=self.learner()
        unit='life-boundaries'
        _,first,_=client.request('/api/attempt',dict(unit=unit))
        self.assertEqual(client.request('/api/attempt',dict(unit=unit))[1],first)
        answers=fixtures.right_answers(unit,first)
        status,done,_=client.request('/api/submit',dict(id=first['id'],answers=answers,reflection='Fictional boundary response, for human review.',support='tool',ink=[]))
        self.assertEqual(status,200)
        self.assertEqual(done['report']['score'],6)
        self.assertEqual(done['report']['points'],20)
        _,retry,_=client.request('/api/attempt',dict(unit=unit))
        self.assertNotEqual(retry['id'],first['id'])
        self.assertEqual({skill:sum(q['skill']==skill for q in retry['questions']) for skill in ['interpret','apply','reason']},
                         {'interpret':2,'apply':2,'reason':2})
        self.assertEqual({q['lesson'] for q in retry['questions']},{1,2})
        self.assertTrue(all('answer' not in q and 'explanation' not in q for q in retry['questions']))

    def test_family_can_make_successful_sign_ins_without_rate_lockout(self):
        client,me=self.learner()
        for _ in range(16): self.assertEqual(client.request('/api/login',{'code':me['recovery']})[0],200)
        for _ in range(12): self.assertEqual(client.request('/api/login',{'code':'invalid-secret-code'})[0],401)
        self.assertEqual(client.request('/api/login',{'code':'invalid-secret-code'})[0],429)

    def test_mentor_learning_is_separate_and_resumable(self):
        own=self.mentor.request('/api/mentor/learn',{})[1];fixtures.complete_tutorial(self.mentor)
        self.assertTrue(own['personal']);self.assertEqual(own['alias'],'My learning')
        self.check(self.mentor,unit='math-cash')
        self.assertEqual(self.mentor.request('/api/me')[1]['points'],20)
        child,child_info=self.learner('Separate learner');self.check(child,unit='math-1')
        inbox=self.mentor.request('/api/mentor')[1]
        self.assertEqual([x['id'] for x in inbox['learners']],[child_info['id']])
        self.assertEqual([x['unit'] for x in inbox['reports']],['math-1'])
        self.assertEqual(self.mentor.request('/api/mentor/learn',{})[1]['id'],own['id'])
        self.assertEqual(self.mentor.request('/api/me')[1]['mastered'],['math-cash'])
        self.assertEqual(child.request('/api/me')[1]['mastered'],['math-1'])
        self.assertEqual(child.request('/api/mentor/learn',{})[0],401)

    def test_unsent_account_reauthentication_cannot_switch_owner(self):
        client,one=self.learner();other,two=self.learner('Second')
        client.request('/api/logout',dict(role='learner'))
        self.assertEqual(client.request('/api/login',dict(code=two['recovery'],expectedLearner=one['id']))[0],409)
        self.assertEqual(client.request('/api/login',dict(code=one['recovery'],expectedLearner=one['id']))[1]['id'],one['id'])

    def test_join_on_shared_mentor_browser_locks_mentor_session(self):
        code=self.mentor.request('/api/mentor/invite',{})[1]['code']
        result=self.mentor.request('/api/join',dict(code=code,alias='New learner',avatar='comet',share=True))[1]
        self.assertEqual(result['profile']['avatar'],'comet')
        self.assertEqual(self.mentor.request('/api/mentor')[0],401)

    def test_second_server_cannot_take_an_active_port(self):
        with self.assertRaises(OSError):
            server.create_server(port=self.app.server_address[1],data=self.tmp.name)

if __name__=='__main__':unittest.main()
