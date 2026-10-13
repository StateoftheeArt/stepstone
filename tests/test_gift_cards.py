"""Disposable API/storage fixtures, never browser-completed learning or real cards."""
import concurrent.futures
import json
import unittest

import test_server as base
import test_funded_program as funded_base

server = base.server


class GiftCardTests(unittest.TestCase):
    setUp = base.PilotTests.setUp
    tearDown = base.PilotTests.tearDown
    learner = base.PilotTests.learner
    check = base.PilotTests.check
    post = funded_base.FundedProgramTests.post
    confirm = funded_base.FundedProgramTests.confirm
    fixture_passes = funded_base.FundedProgramTests.fixture_passes

    def card(self, action, payload, expected=200):
        result = self.mentor.request('/api/mentor/cards/'+action, {'key':server.uid(), **payload})
        self.assertEqual(result[0], expected, result[1])
        return result[1]

    def cash(self, cents):
        self.post('funding', dict(kind='received', cents=cents, note='Synthetic received cash; no actual funding.'))

    def reserve(self, me, amount=1000, expected=200):
        b=next((b for b in self.mentor.request('/api/mentor')[1]['cardBudgets'] if b['primary_learner']==me['id']),None)
        return self.card('reserve', dict(learner=me['id'], cents=amount, expected_revision=b['revision'] if b else 0), expected)

    def ready(self, cents=5000):
        client, me=self.learner();self.confirm(me);self.cash(cents);self.reserve(me,cents)
        self.fixture_passes(me, points=1000)
        return client, me

    def request(self, client, amount=1000, provider='amazon-ca', key=None):
        return client.request('/api/cards/request',dict(key=key or server.uid(),amount_cents=amount,provider=provider))

    def claim(self, client):
        return next(c for c in client.request('/api/me')[1]['claims'] if c.get('card_exchange'))

    def approve(self, client):
        c=self.claim(client)
        return self.card('decision',dict(id=c['id'],revision=c['revision'],status='approved',demonstrated=True))

    def deliver(self, client, code='A1B2C3D4E5F6G7', pin='', **extra):
        c=self.claim(client)
        return self.mentor.request('/api/mentor/cards/deliver',dict(key=server.uid(),id=c['id'],revision=c['revision'],code=code,pin=pin,confirmed=True)|extra)

    def test_welcome_only_cannot_exchange_or_fake_prerequisites(self):
        c,me=self.learner();self.confirm(me);self.cash(1000);self.reserve(me)
        with self.app.store.db() as db:db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',(server.uid(),me['id'],10,'Synthetic welcome milestone points',0))
        self.assertEqual(c.request('/api/me')[1]['points'],10)
        self.assertEqual(self.request(c)[0],409)
        self.check(c,'math-cash')
        self.assertEqual(self.request(c)[0],409)
        self.assertEqual(c.request('/api/cards/request',dict(key=server.uid(),amount_cents=1000,provider='amazon-ca',mastered=['all']))[0],400)
        self.assertEqual(c.request('/api/me')[1]['claims'],[])

    def test_prices_minimum_and_savings_are_server_owned(self):
        for amount,cost in ((1000,20),(2000,36),(5000,80)):
            c,me=self.ready(amount);before=c.request('/api/me')[1]['points']
            self.assertEqual(self.request(c,amount)[0],200)
            self.assertEqual(c.request('/api/me')[1]['points'],before-cost)
            claim=self.claim(c);self.assertEqual(claim['amount_cents'],amount);self.assertEqual(claim['cost'],cost)
        c,me=self.ready()
        for amount in (500,1500,10000,'1000',True):self.assertEqual(self.request(c,amount)[0],400)
        self.assertEqual(self.request(c,1000,'unknown')[0],400)

    def test_funding_holds_prevent_overspend_and_double_reservation(self):
        c,me=self.learner();self.confirm(me);self.cash(3000);self.reserve(me,2000)
        self.assertEqual(self.mentor.request('/api/mentor')[1]['funding']['cash_cents'],1000)
        self.reserve(me,2000,409)
        self.post('funding',dict(kind='expense',cents=1001,note='Synthetic overspend.'),expected=409)
        self.fixture_passes(me)
        self.assertEqual(self.request(c,5000)[0],409)
        self.assertEqual(self.request(c,1000)[0],200)
        b=self.mentor.request('/api/mentor')[1]['cardBudgets'][0]
        self.card('release',dict(learner=me['id'],expected_revision=b['revision']))
        b=self.mentor.request('/api/mentor')[1]['cardBudgets'][0]
        self.assertEqual(b['reserved_cents'],1000)
        self.assertEqual(self.mentor.request('/api/mentor')[1]['funding']['cash_cents'],2000)

    def test_parallel_request_retry_and_refund_once(self):
        c,me=self.ready();before=c.request('/api/me')[1]['points'];key=server.uid()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results=list(pool.map(lambda _:self.request(c,key=key),range(6)))
        self.assertTrue(all(r[0]==200 for r in results));self.assertEqual(len({r[1]['claim'] for r in results}),1)
        self.assertEqual(c.request('/api/me')[1]['points'],before-20)
        self.assertEqual(self.request(c)[0],409)
        self.assertEqual(self.request(c,2000,key=key)[0],409)
        claim=self.claim(c);data=dict(key=server.uid(),id=claim['id'],revision=claim['revision'],status='declined')
        for _ in range(3):self.card('decision',data)
        self.assertEqual(c.request('/api/me')[1]['points'],before)
        self.card('decision',data|dict(key=server.uid()),409)
        self.assertEqual(self.request(c)[0],200)

    def test_approval_format_phrase_and_payload_rejections(self):
        c,me=self.ready();self.request(c);claim=self.claim(c)
        self.card('decision',dict(id=claim['id'],revision=0,status='approved'),400)
        self.assertEqual(self.deliver(c)[0],409)
        self.approve(c)
        for code in ('https://evil.test','hello there','CALLME123456789','A1B2C3D4E5F6G!', 'Ａ1B2C3D4E5F6G7', 'ABCDEFGHIJKLMN', '12345678901234'):
            self.assertEqual(self.deliver(c,code)[0],400,code)
        self.assertEqual(self.deliver(c,note='extra message')[0],400)
        self.assertEqual(self.deliver(c,pin='1234')[0],400)
        self.assertEqual(self.deliver(c,confirmed=False)[0],400)
        self.assertEqual(self.claim(c)['status'],'approved')

    def test_private_delivery_spends_cash_once_and_hides_keys(self):
        c,me=self.ready(2000);other,_=self.learner('Other learner');self.request(c);self.approve(c)
        claim=self.claim(c);code='A1B2-C3D4E5-F6G7'
        data=dict(key=server.uid(),id=claim['id'],revision=claim['revision'],code=code,confirmed=True)
        for _ in range(3):self.card('deliver',data)
        self.assertEqual(self.claim(c)['status'],'given')
        self.assertEqual(c.request('/api/cards/reveal',dict(id=claim['id']))[1]['code'],code)
        self.assertEqual(other.request('/api/cards/reveal',dict(id=claim['id']))[0],404)
        self.assertEqual(other.request('/api/cards/reveal',dict(id=claim['id'],learner=me['id']))[0],409)
        overview=self.mentor.request('/api/mentor')[1]
        self.assertEqual(overview['funding']['cash_cents'],0)
        self.assertEqual(overview['funding']['totals']['spent_cents'],1000)
        self.assertEqual(overview['cardBudgets'][0]['reserved_cents'],1000)
        for path,client in (('/api/me',c),('/api/mentor',self.mentor)):
            response=client.request(path);self.assertNotIn(code,json.dumps(response[1]));self.assertEqual(response[2]['Cache-Control'],'no-store')
        with self.app.store.db() as db:
            self.assertNotIn(code, json.dumps([tuple(r) for r in db.execute('SELECT * FROM reward_commands')]))
            self.assertNotIn(code, json.dumps([tuple(r) for r in db.execute('SELECT * FROM reward_audit')]))
        self.card('decision',dict(id=claim['id'],revision=self.claim(c)['revision'],status='declined'),409)
        self.request(c);self.approve(c)
        self.assertEqual(self.deliver(c,'A1B2C3D4E5F6G7')[0],409)

    def test_providers_pin_and_lifetime_cap(self):
        c,me=self.ready(25000)
        for i in range(5):
            self.assertEqual(self.request(c,5000,'walmart-ca')[0],200);self.approve(c)
            self.assertEqual(self.deliver(c,str(6000000000000000+i),pin='1234')[0],200)
        x=c.request('/api/me')[1]['cardExchange'];self.assertEqual(x['used_cents'],25000)
        self.cash(1000);self.reserve(me,1000,409);self.assertEqual(self.request(c)[0],409)
        with self.app.store.db() as db:self.assertEqual(db.execute("SELECT COUNT(*) FROM gift_card_requests WHERE status='given'").fetchone()[0],5)

    def test_linked_extra_account_and_mentor_personal_cannot_claim(self):
        c,me=self.ready();extra,other=self.learner('Extra account');self.confirm(other,same_person_as=me['id'])
        self.fixture_passes(other)
        self.assertEqual(self.request(extra)[0],409)
        self.post('person',dict(learner=me['id'],same_person_as=other['id'],confirmed=True,note='Synthetic attempted relink.'),expected=200)
        personal=self.mentor.request('/api/mentor/learn',{})
        self.assertEqual(personal[0],200)
        self.assertIsNone(personal[1]['cardExchange'])
        self.assertEqual(self.request(self.mentor)[0],400)

    def test_recovery_hold_blocks_reward_side_effects(self):
        c,me=self.ready()
        with self.app.store.db() as db:db.execute("INSERT INTO settings VALUES('recoveryHold','{}')")
        self.assertEqual(self.request(c)[0],409)
        self.assertEqual(c.request('/api/me')[1]['claims'],[])

    def test_google_delivery_and_walmart_rejects_wrong_lengths(self):
        c,me=self.ready(2000)
        self.assertEqual(self.request(c,1000,'google-play-ca')[0],200);self.approve(c)
        code='A1B2C3D4E5F6G7H8'
        self.assertEqual(self.deliver(c,code)[0],200)
        self.assertEqual(c.request('/api/cards/reveal',dict(id=self.claim(c)['id']))[1]['code'],code)
        self.assertEqual(self.request(c,1000,'walmart-ca')[0],200);self.approve(c)
        for code in ('123456789012345','12345678901234567','1234567890123456789'):
            self.assertEqual(self.deliver(c,code,pin='1234')[0],400)

    def test_another_mentor_cannot_read_or_mutate_card_request(self):
        c,me=self.ready();self.request(c);claim=self.claim(c)
        other=base.Client(self.url)
        status,_,_=other.request('/api/mentor/setup',dict(username='another-card-mentor',name='Another test mentor',device='Another test device',passphrase='another-card-test-passphrase'))
        self.assertEqual(status,200)
        overview=other.request('/api/mentor')[1]
        self.assertEqual(overview['claims'],[]);self.assertEqual(overview['cardBudgets'],[])
        self.assertEqual(overview['funding']['cash_cents'],0)
        for action,payload in (('reserve',dict(learner=me['id'],cents=1000,expected_revision=0)),('decision',dict(id=claim['id'],revision=0,status='approved',demonstrated=True)),('deliver',dict(id=claim['id'],revision=0,code='A1B2C3D4E5F6G7',confirmed=True))):
            self.assertEqual(other.request('/api/mentor/cards/'+action,dict(key=server.uid(),**payload))[0],404,action)
        self.assertEqual(self.claim(c)['status'],'pending')
