"""API/storage fixtures, not claimed browser completions or real purchases."""
import concurrent.futures
import datetime as dt
import json
import time
import unittest
import test_server as base
import ai_support

server=base.server

class AIMonthTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner

    def funded(self,action,**data):
        result=self.mentor.request('/api/mentor/funded/'+action,dict(key=server.uid(),**data))
        self.assertEqual(result[0],200,result[1]);return result[1]

    def action(self,action,status=200,**data):
        result=self.mentor.request('/api/mentor/ai/'+action,dict(key=server.uid(),**data))
        self.assertEqual(result[0],status,result[1]);return result[1]

    def info(self,c):return c.request('/api/me')[1]['aiSupport']
    def cash(self):return self.mentor.request('/api/mentor')[1]['funding']['cash_cents']
    def notes(self,c,revision=0,**changes):
        return c.request('/api/ai/plan',dict(revision=revision,provider='chatgpt',mode='prepared',explain='I checked the sum.',email='I kept Saturday.',change='I would test empty text.',reason='I want short checkable explanations.',**changes))
    def confirmed(self):
        c,me=self.learner();self.funded('person',learner=me['id'],confirmed=True,note='Synthetic confirmation.')
        return c,me
    def reserve(self,me):return self.action('reserve',learner=me['id'],cents=5000,note='Synthetic reserve. No real cash.')

    def ready_fixture(self,c,me):
        # Explicit prerequisites for reward tests; actual lessons are walked separately.
        with self.app.store.db() as db:
            for u in (*ai_support.PC_UNITS,'digital-5','digital-6'):
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',(server.uid(),me['id'],u,'[]',time.time(),time.time(),json.dumps(dict(passed=True))))
            for u in ai_support.PC_UNITS:
                db.execute('INSERT OR REPLACE INTO device_work VALUES(?,?,?,?,?,?,?)',(me['id'],u,1,'confirmed','Synthetic practice','Synthetic observation',time.time()))
            db.execute('INSERT OR REPLACE INTO learner_projects VALUES(?,?,?,?)',(me['id'],1,json.dumps(dict(version=1,kind='checklist',title='Practice kit',purpose='Synthetic test project',label='Task',limit=6,goal=5000,accent='teal',items=[dict(id=1,label='Practice task',value=0,done=False)],behaviours=['Add','Check','Save'])),time.time()))
        self.assertEqual(self.notes(c)[0],200)

    def approval(self,row,**changes):
        data=dict(id=row['id'],revision=row['revision'],cents=3500,plan='Synthetic monthly plan',age_band='18plus',checked_on=str(dt.date.today()),
          terms_checked=True,own_account=True,monthly_only=True,no_addons=True,demonstrated=True,note='Synthetic demonstration.')
        data.update(changes);return data

    def activation(self,row,**changes):
        data=dict(id=row['id'],revision=row['revision'],cents=3400,activated_on=str(dt.date.today()),paid_through=str(dt.date.today()+dt.timedelta(days=30)),
          paid_confirmed=True,renewal='off',cancellation='Synthetic non-renewing month.',note='Synthetic receipt, no real purchase.')
        data.update(changes);return data

    def prepared(self):
        c,me=self.confirmed();self.funded('funding',kind='received',cents=6000,note='Synthetic test funds.')
        self.reserve(me);self.ready_fixture(c,me)
        self.assertEqual(c.request('/api/ai/request',{})[0],200)
        return c,me,self.info(c)['month']

    def test_cash_reservation_and_release_are_exact_once(self):
        c,me=self.confirmed();self.action('reserve',status=409,learner=me['id'],cents=5000,note='Not funded.')
        self.funded('funding',kind='received',cents=6000,note='Synthetic funds.')
        self.reserve(me);self.reserve(me);self.assertEqual(self.cash(),1000)
        code,_,_=self.mentor.request('/api/mentor/funded/funding',dict(key=server.uid(),kind='expense',cents=1001,note='Would spend reserved cash.'))
        self.assertEqual(code,409);self.assertEqual(self.cash(),1000)
        row=self.info(c)['month'];data=dict(key=server.uid(),id=row['id'],revision=row['revision'],note='No purchase happened.')
        for _ in range(2):self.assertEqual(self.mentor.request('/api/mentor/ai/release',data)[0],200)
        self.assertEqual(self.cash(),6000)
        self.reserve(me);self.assertEqual(self.cash(),1000)

    def test_readiness_cannot_be_claimed_by_the_browser(self):
        c,me=self.confirmed();self.funded('funding',kind='received',cents=5000,note='Synthetic funds.');self.reserve(me);self.notes(c)
        self.assertEqual(c.request('/api/ai/request',dict(ready=True,score=6,deviceWork='confirmed',project=True))[0],409)
        row=self.info(c)['month'];self.action('approve',status=409,**self.approval(row))
        self.assertEqual(self.cash(),0)

    def test_age_consent_freshness_and_price_are_required(self):
        c,me,row=self.prepared()
        for changes in [dict(age_band='under13'),dict(age_band='13-17'),dict(own_account=False),dict(monthly_only='yes'),dict(demonstrated=False),dict(checked_on='2020-01-01'),dict(cents=5001),dict(cents=True)]:
            self.action('approve',status=400,**self.approval(row,**changes))
        self.action('approve',**self.approval(row,age_band='13-17',guardian_permission=True))
        self.assertEqual(self.info(c)['month']['status'],'approved')
        # Changing notes invalidates the approval and requires a new request.
        changed=dict(revision=1,provider='claude',mode='prepared',explain='Checked math.',email='Checked date.',change='Check empty entry.',reason='Discuss an eligible service.')
        self.assertEqual(c.request('/api/ai/plan',changed)[0],200)
        self.assertEqual(self.info(c)['month']['status'],'allocated')
        self.assertEqual(c.request('/api/ai/request',{})[0],200)
        row=self.info(c)['month'];self.action('approve',status=400,**self.approval(row,age_band='13-17',guardian_permission=True))

    def test_activation_spends_once_and_never_reopens_entitlement(self):
        c,me,row=self.prepared();self.action('approve',**self.approval(row));row=self.info(c)['month']
        self.action('activate',status=400,**self.activation(row,cents=3501))
        self.action('activate',status=400,**self.activation(row,paid_through=str(dt.date.today()+dt.timedelta(days=365))))
        self.action('activate',status=400,**self.activation(row,renewal='unknown'))
        data=dict(key=server.uid(),**self.activation(row))
        # Parallel retries after a lost response must have one financial effect.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:self.mentor.request('/api/mentor/ai/activate',data),range(2)))
        self.assertTrue(all(r[0]==200 for r in results));self.assertEqual(self.cash(),2600)
        active=self.info(c)['month'];self.reserve(me);self.assertEqual(self.info(c)['month']['id'],active['id'])
        self.action('release',status=409,id=active['id'],revision=active['revision'],note='Try to replay funding.')
        self.action('activate',status=409,**self.activation(active))
        self.action('close',status=409,id=active['id'],revision=active['revision'],note='Still within paid month.')
        with self.app.store.db() as db:self.assertEqual(db.execute("SELECT COUNT(*) FROM reward_funding WHERE kind='ai-month'").fetchone()[0],1)

    def test_separate_accounts_and_roles_cannot_take_funding(self):
        c,me,row=self.prepared();other,other_me=self.confirmed()
        self.assertEqual(other.request('/api/mentor/ai/approve',self.approval(row))[0],401)
        self.assertEqual(other.request('/api/ai/request',dict(learner=me['id']))[0],409)
        self.assertIsNone(self.info(other)['plan']);self.assertIsNone(self.info(other)['month'])
        self.funded('person',learner=other_me['id'],same_person_as=me['id'],confirmed=True,note='Synthetic duplicate account.')
        self.assertEqual(other.request('/api/ai/request',{})[0],409)
        self.action('reserve',status=409,learner=other_me['id'],cents=5000,note='Duplicate person.')
        # Merging a used/reserved main account away must not hide its entitlement.
        third,third_me=self.confirmed()
        self.assertEqual(self.mentor.request('/api/mentor/funded/person',dict(key=server.uid(),learner=me['id'],same_person_as=third_me['id'],confirmed=True,note='Try to remove entitlement.'))[0],409)

    def test_stale_notes_and_permissions_do_not_overwrite(self):
        c,me=self.confirmed();self.assertEqual(self.notes(c)[0],200)
        self.assertEqual(self.notes(c)[0],409)
        data=dict(revision=1,provider='gemini',mode='own-service',explain='Checked sum.',email='Checked date.',change='Checked button.',reason='Short steps.')
        self.assertEqual(c.request('/api/ai/plan',data)[0],400)
        self.assertEqual(c.request('/api/ai/plan',dict(data,permitted=True))[0],200)
        self.assertEqual(self.info(c)['plan']['revision'],2)
        self.assertEqual(c.request('/api/me')[1]['points'],0)

    def test_cancellation_record_is_not_cancellation_or_second_payment(self):
        c,me,row=self.prepared();self.action('approve',**self.approval(row));row=self.info(c)['month']
        self.action('activate',status=400,**self.activation(row,renewal='cancel-scheduled',cancel_by=str(dt.date.today()+dt.timedelta(days=31))))
        self.action('activate',**self.activation(row,renewal='cancel-scheduled',cancel_by=str(dt.date.today()+dt.timedelta(days=10))))
        row=self.info(c)['month'];self.action('renewal',status=400,id=row['id'],revision=row['revision'],renewal='off',verified=False,cancellation='Not verified.',note='Test confirmation.')
        self.action('renewal',id=row['id'],revision=row['revision'],renewal='off',verified=True,cancellation='Synthetic provider confirmation.',note='No second payment.')
        self.assertEqual(self.cash(),2600)
        self.assertEqual(self.info(c)['month']['details']['renewal'],'off')

if __name__=='__main__':unittest.main()
