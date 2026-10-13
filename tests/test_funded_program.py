"""Synthetic API/storage fixtures. These are not browser-completed grades."""
import concurrent.futures
import copy
import json
import time
import unittest
from unittest.mock import patch

import test_server as base
from reward_program import PROGRAM, LAPTOP_DEMO

server = base.server
Client = base.Client


class FundedProgramTests(unittest.TestCase):
    setUp = base.PilotTests.setUp
    tearDown = base.PilotTests.tearDown
    learner = base.PilotTests.learner
    check = base.PilotTests.check

    def post(self, action, data=None, expected=200):
        data = {'key': server.uid(), **(data or {})}
        result = self.mentor.request('/api/mentor/funded/' + action, data)
        self.assertEqual(result[0], expected, result[1])
        return result[1]

    def confirm(self, me, **kwargs):
        return self.post('person', dict(learner=me['id'],confirmed=True,note='Synthetic person confirmation.',**kwargs))

    def cards(self, count=4):
        return self.post('funding', dict(kind='donate-cards',quantity=count,note='Synthetic donated cards. No real value.'))

    def allocate(self, me, kind='cards', **kwargs):
        return self.post('allocate', dict(learner=me['id'],kind=kind), **kwargs)

    def fixture_passes(self, me, ids=None, points=640):
        ids = ids if ids is not None else [u for g in server.FOUNDATION['groups'] for u in g['units']]
        with self.app.store.db() as db:
            for unit in ids:
                report=dict(passed=True,score=6,total=6,at=time.time(),title=server.UNITS[unit]['title'],unit=unit)
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                           (server.uid(),me['id'],unit,'[]',time.time(),time.time(),json.dumps(report)))
            db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',(server.uid(),me['id'],points,'Synthetic test prerequisites',time.time()))

    def offer(self, client, key='core-card-everyday'):
        return next(r for r in client.request('/api/me')[1]['rewards'] if r['id']==key)

    def request(self, client, key='core-card-everyday', **kwargs):
        r=self.offer(client,key)
        return client.request('/api/reward',dict(id=key,allocation=r['allocation'],**kwargs))

    def claim(self, client):
        return next(c for c in client.request('/api/me')[1]['claims'] if c.get('funded'))

    def decision(self, claim, status, **kwargs):
        return self.mentor.request('/api/mentor/claim',dict(id=claim['id'],revision=claim['revision'],key=server.uid(),status=status,note='Synthetic review decision.',**kwargs))

    def summary(self):
        return self.mentor.request('/api/mentor')[1]['funding']

    def ready(self):
        person,me=self.learner();self.confirm(me);self.cards();self.allocate(me);self.fixture_passes(me)
        return person,me

    def test_unfunded_confirmed_and_named_path_are_distinct_gates(self):
        person,me=self.learner()
        self.assertFalse(self.offer(person)['confirmed'])
        self.assertEqual(self.request(person)[0],409)
        self.cards();self.allocate(me,expected=409);self.confirm(me);self.allocate(me)
        fake=dict(mastered=[u for g in server.FOUNDATION['groups'] for u in g['units']],points=9999,score=6,path_version=999,phase=7)
        self.assertEqual(self.request(person,**fake)[0],409)
        # Irrelevant and unfinished/incorrect checks cannot fill named gates.
        self.check(person,'math-1')
        self.check(person,'math-cash',wrong=3)
        self.assertEqual(self.request(person,**fake)[0],409)
        for unit in server.FOUNDATION['groups'][0]['units']: self.check(person,unit)
        before=person.request('/api/me')[1]['points']
        result=self.request(person,**fake)
        self.assertEqual(result[0],200,result[1]);self.assertEqual(result[1]['me']['points'],before-60)
        self.assertEqual(result[1]['me']['foundation']['groups'][1]['completed'],0)

    def test_cash_purchase_donation_delivery_accounting_and_retry(self):
        payload=dict(key=server.uid(),kind='received',cents=2000,note='Synthetic CAD20 receipt.')
        self.post('funding',payload);self.post('funding',payload)
        self.assertEqual(self.summary()['cash_cents'],2000)
        self.post('funding',payload|dict(cents=2100),expected=409)
        self.post('funding',dict(kind='buy-cards',quantity=4,note='Synthetic CAD20 purchase.'))
        self.assertEqual(self.summary()['cash_cents'],0)
        before=self.summary();self.post('funding',dict(kind='buy-laptop',cents=20000,note='Synthetic overspend.'),expected=409)
        self.assertEqual(self.summary(),before)
        self.cards(4)
        self.assertEqual(self.summary()['totals']['received_cents'],2000)
        self.assertEqual(self.summary()['totals']['cards_available'],8)
        person,me=self.learner();self.confirm(me);self.allocate(me);self.fixture_passes(me)
        self.assertEqual(self.request(person)[0],200)
        self.assertEqual(self.decision(self.claim(person),'approved',demonstration={'sample':True})[0],200)
        self.assertEqual(self.decision(self.claim(person),'given')[0],200)
        after=self.summary()
        self.assertEqual(after['cash_cents'],0);self.assertEqual(after['totals']['spent_cents'],2000)
        self.assertEqual(after['totals']['given'],1);self.assertEqual(after['totals']['reserved'],3)
        self.assertEqual(after['totals']['cards_available'],4)

    def test_one_last_place_concurrent_allocations_and_reserved_ownership(self):
        a,ma=self.learner('A');b,mb=self.learner('B')
        self.confirm(ma);self.confirm(mb);self.cards()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results=list(pool.map(lambda me:self.mentor.request('/api/mentor/funded/allocate',dict(key=server.uid(),learner=me['id'],kind='cards')),[ma,mb]))
        self.assertEqual(sorted(r[0] for r in results),[200,409])
        win,lose=(a,b) if results[0][0]==200 else (b,a)
        win_me=ma if win==a else mb;lose_me=mb if win==a else ma
        self.fixture_passes(win_me);self.fixture_passes(lose_me)
        offer=self.offer(win)
        attack=lose.request('/api/reward',dict(id=offer['id'],allocation=offer['allocation'],points=10000))
        self.assertEqual(attack[0],409);self.assertEqual(lose.request('/api/me')[1]['points'],640)
        self.assertEqual(self.request(win)[0],200)
        self.assertEqual(self.summary()['totals']['cards_available'],0)

    def test_simultaneous_posts_lost_response_and_recreated_offer(self):
        person,me=self.ready();r=self.offer(person);payload=dict(id=r['id'],allocation=r['allocation'])
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results=list(pool.map(lambda _:person.request('/api/reward',payload),range(8)))
        self.assertTrue(all(r[0]==200 for r in results));self.assertEqual(len({r[1]['claim'] for r in results}),1)
        self.assertEqual(person.request('/api/me')[1]['points'],580)
        self.assertEqual(self.allocate(me)['allocated'],0)
        self.assertEqual(self.summary()['totals']['reserved'],4)
        # No new card/laptop offer can mint another entitlement.
        body=dict(title='Recreated card',description='Synthetic duplicate.',cost=60,category='giftcard',stock=1)
        self.assertEqual(self.mentor.request('/api/mentor/reward',body)[0],409)
        with self.app.store.db() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM ledger WHERE id LIKE ? AND learner=?',('claim-%',me['id'])).fetchone()[0],1)

    def test_cancel_refunds_once_reallocation_does_not_replay_old_claim(self):
        person,me=self.ready();old=self.offer(person);self.request(person)
        c=self.claim(person);decision=dict(id=c['id'],revision=c['revision'],key=server.uid(),status='declined',note='Synthetic cancellation.')
        for _ in range(3):self.assertEqual(self.mentor.request('/api/mentor/claim',decision)[0],200)
        self.assertEqual(person.request('/api/me')[1]['points'],640)
        self.assertEqual(self.summary()['totals']['cards_available'],1)
        self.assertEqual(self.decision(self.claim(person),'given')[0],409)
        self.assertEqual(self.allocate(me)['allocated'],1)
        new=self.offer(person);self.assertNotEqual(new['allocation'],old['allocation'])
        for _ in range(2):self.assertEqual(person.request('/api/reward',dict(id=old['id'],allocation=old['allocation']))[0],200)
        self.assertEqual(person.request('/api/me')[1]['points'],640)
        self.assertEqual(self.request(person)[0],200);self.assertEqual(person.request('/api/me')[1]['points'],580)
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ledger WHERE learner=? AND id LIKE 'refund-%'",(me['id'],)).fetchone()[0],1)

    def test_stale_decision_and_accessible_demonstration(self):
        person,me=self.ready();self.request(person);stale=self.claim(person)
        self.assertEqual(self.decision(stale,'approved')[0],400)
        self.assertEqual(self.decision(stale,'pending')[0],200)
        self.assertEqual(self.decision(stale,'approved',demonstration={'sample':True})[0],409)
        c=self.claim(person);self.assertEqual(c['status'],'pending');self.assertEqual(person.request('/api/me')[1]['points'],580)
        self.assertEqual(self.decision(c,'approved',demonstration={'sample':True})[0],200)
        self.assertEqual(self.decision(self.claim(person),'given')[0],200)
        self.assertEqual(self.decision(self.claim(person),'declined')[0],409)
        self.assertEqual(self.allocate(me)['allocated'],0)

    def test_laptop_is_exact_path_zero_points_with_five_demonstrations(self):
        person,me=self.learner();self.confirm(me)
        self.post('funding',dict(kind='donate-laptop',note='Synthetic laptop and charger.'))
        self.allocate(me,'laptop')
        from course_access import required_units
        ids=required_units(server.CATALOG)
        self.assertEqual(len(ids),96)
        self.fixture_passes(me,ids[:-1],points=0)
        self.assertEqual(self.request(person,'core-laptop')[0],409)
        self.fixture_passes(me,[ids[-1]],points=0)
        self.assertEqual(self.request(person,'core-laptop')[0],200)
        self.assertEqual(person.request('/api/me')[1]['points'],0)
        self.assertEqual(self.decision(self.claim(person),'approved',demonstration={'file':True})[0],400)
        self.assertEqual(self.decision(self.claim(person),'approved',demonstration={k:True for k in LAPTOP_DEMO})[0],200)
        self.assertEqual(self.decision(self.claim(person),'given')[0],200)
        self.assertEqual(self.summary()['cash_cents'],0);self.assertEqual(self.summary()['totals']['given'],1)

    def test_duplicate_account_links_without_deleting_learning(self):
        primary,main=self.ready();extra,other=self.learner('Extra account')
        self.check(extra)
        before=extra.request('/api/me')[1]['attempts']
        self.confirm(other,same_person_as=main['id'])
        self.allocate(other,expected=409)
        self.assertTrue(self.offer(extra)['linked']);self.assertEqual(self.request(extra)[0],409)
        self.assertEqual(extra.request('/api/me')[1]['attempts'],before)
        self.assertEqual(self.summary()['totals']['reserved'],4)
        self.assertEqual(self.request(primary)[0],200)

    def test_mistaken_link_can_be_separated_without_touching_the_main_place(self):
        primary,main=self.ready();extra,other=self.learner('Sibling linked')
        self.confirm(other,same_person_as=main['id'])
        self.assertTrue(self.offer(extra)['linked'])
        # Only a linked extra account can be separated; a main account keeps its record.
        self.post('person',dict(learner=main['id'],same_person_as='separate',confirmed=True,note='Synthetic check.'),expected=400)
        self.post('person',dict(learner=other['id'],same_person_as='separate',confirmed=True,note='Synthetic sibling correction.'))
        self.assertFalse(self.offer(extra).get('linked'))
        self.assertEqual(self.summary()['totals']['reserved'],4)
        self.assertEqual(self.request(primary)[0],200)
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reward_audit WHERE action='separate-person'").fetchone()[0],1)

    def test_confirmed_extra_account_can_link_after_releasing_unused_places(self):
        a,ma=self.ready();b,mb=self.learner('Extra confirmed');self.confirm(mb);self.cards();self.allocate(mb)
        self.post('person',dict(learner=mb['id'],same_person_as=ma['id'],confirmed=True,note='Synthetic duplicate review.'),expected=409)
        for allocation in self.summary()['allocations']:
            if allocation['primary_learner']==mb['id']:
                self.post('release',dict(id=allocation['id'],note='Synthetic extra account correction.'))
        self.confirm(mb,same_person_as=ma['id'])
        self.assertTrue(self.offer(b)['linked']);self.assertEqual(self.summary()['totals']['cards_available'],4)

    def test_stock_correction_and_optimistic_update(self):
        self.cards(5);person,me=self.learner();self.confirm(me);self.allocate(me)
        stock=self.summary()['stock'][0]
        body=dict(batch=stock['id'],expected_quantity=5,quantity=2,note='Synthetic stock correction.')
        self.post('stock-remove',body,expected=409)
        self.post('stock-remove',body|dict(quantity=1));self.post('stock-remove',body|dict(quantity=1),expected=409)
        self.assertEqual(self.summary()['stock'][0]['quantity'],4)
        self.assertEqual(self.summary()['totals']['reserved'],4)

    def test_frozen_path_and_identity_recovery_expiry_owner_reset(self):
        person,me=self.ready()
        changed=copy.deepcopy(server.FOUNDATION);changed['version']=999;changed['groups'][0]['units'].append('math-12')
        with patch.object(self.app.store.funded,'foundation',changed):
            self.assertEqual(self.offer(person)['path_version'],server.FOUNDATION['version'])
            self.assertEqual(self.request(person)[0],200)
        recovery=self.mentor.request('/api/mentor/recovery',dict(id=me['id']))[1]
        self.assertEqual(person.request('/api/me')[0],401)
        again=Client(self.url);self.assertEqual(again.request('/api/login',dict(code=recovery['code']))[0],200)
        self.assertEqual(self.request(again)[0],200);self.assertEqual(again.request('/api/me')[1]['points'],580)
        before=self.summary()
        own=self.mentor.request('/api/mentor/learn',{})[1]
        self.post('person',dict(learner=own['id'],confirmed=True,note='Cannot fund owner.'),expected=400)
        self.assertEqual(self.mentor.request('/api/mentor/reset-learning',dict(learner=own['id'],confirmation='RESET MY LEARNING'))[0],200)
        self.assertEqual(self.summary(),before)
        with self.app.store.db() as db:db.execute("UPDATE sessions SET expires=0 WHERE role='learner' AND owner=?",(me['id'],))
        self.assertEqual(again.request('/api/reward',dict(id='core-card-everyday'))[0],401)
        self.assertEqual(self.summary(),before)

    def test_input_auth_ownership_and_per_account_rate(self):
        person,me=self.ready();other,mo=self.learner('Same network')
        self.assertEqual(person.request('/api/mentor/funded/funding',{})[0],401)
        self.assertEqual(Client(self.url).request('/api/reward',dict(id='core-laptop'))[0],401)
        self.assertEqual(self.request(person,learner=mo['id'])[0],409)
        for data in ({'id':[]},{'id':1},{'id':'core-card-everyday','allocation':[]},{'id':'core-card-everyday','allocation':None}):
            self.assertEqual(person.request('/api/reward',data)[0],400)
        for changes in ({'quantity':True},{'quantity':1.5},{'quantity':-1},{'quantity':100000}):
            self.post('funding',dict(kind='donate-cards',note='Synthetic malformed input.',**changes),expected=400)
        for _ in range(30):result=person.request('/api/reward',dict(id='core-card-everyday',allocation='invalid'))
        self.assertEqual(result[0],429)
        self.assertEqual(other.request('/api/reward',dict(id='core-card-everyday'))[0],409)
        self.assertEqual(person.request('/api/me')[1]['points'],640)
        self.assertEqual(self.summary()['totals']['reserved'],4)

    def test_theme_refund_is_one_time_and_not_lifetime_earnings(self):
        person,me=self.learner()
        with self.app.store.db() as db:
            db.execute('INSERT INTO claims(id,learner,reward,status,cost,created) VALUES(?,?,?,?,?,?)',('legacy-colour',me['id'],'theme-ocean','given',30,time.time()))
            db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',('synthetic-earned',me['id'],60,'Synthetic earned',time.time()))
            db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',('claim-legacy-colour',me['id'],-30,'Old colour purchase',time.time()))
        server.Store(self.tmp.name);server.Store(self.tmp.name)
        info=person.request('/api/me')[1]
        self.assertEqual(info['points'],60);self.assertEqual(info['earned'],60)
        self.assertEqual(next(r for r in info['rewards'] if r['id']=='theme-ocean')['cost'],0)
        self.assertEqual(info['claims'][0]['cost'],30)
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ledger WHERE id LIKE 'refund-free-colours-%'").fetchone()[0],1)


if __name__=='__main__':unittest.main()
