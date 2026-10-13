"""Real-time food, durable migration and API ownership in disposable stores."""
import concurrent.futures
import json
import unittest
import pip_rewards
import test_server as fixtures
from test_server import Client

class PipFoodTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def test_food_is_awarded_once_for_new_passes_and_feed_is_idempotent(self):
        child,me=self.learner()
        self.assertEqual(child.request('/api/pip/feed',dict(requestId='empty-bowl'))[0],409)
        self.check(child,'math-1',wrong=2)
        self.assertEqual(child.request('/api/me')[1]['pipFood']['bank'],0)
        self.check(child,'math-1');self.check(child,'math-1')
        state=child.request('/api/me')[1]
        self.assertEqual(state['pipFood']['bank'],1)
        self.assertEqual(state['moduleWins'][0]['pipFood'],1)
        self.assertEqual(state['moduleWins'][0]['pipItems'],[])
        payload=dict(requestId='food-receipt-one')
        first=child.request('/api/pip/feed',payload)
        repeated=child.request('/api/pip/feed',payload)
        self.assertEqual(first[0],200);self.assertEqual(repeated[0],200)
        self.assertEqual(repeated[1]['pipFood']['bank'],0)
        self.assertLessEqual(repeated[1]['pipFood']['remaining'],1800)
        self.assertGreater(repeated[1]['pipFood']['remaining'],1790)
        self.assertEqual(repeated[1]['points'],state['points'])
        self.assertEqual(Client(self.url).request('/api/pip/feed',payload)[0],401)
        other,_=self.learner('Other')
        self.assertEqual(other.request('/api/pip/feed',dict(**payload,learner=me['id']))[0],409)
        self.assertEqual(child.request('/api/pip/feed',payload,headers={'Origin':'https://unrelated.example'})[0],403)

    def test_elapsed_food_clock_capacity_and_replays(self):
        _,me=self.learner()
        with self.app.store.db() as db:
            db.execute('UPDATE pip_food SET bank=4,last=1000 WHERE learner=?',(me['id'],))
            for i in range(3):pip_rewards.feed(db,me['id'],'fill-'+str(i),fixtures.server.Problem,now=1000)
            self.assertEqual(pip_rewards.food(db,me['id'],now=1000)['remaining'],5400)
            with self.assertRaises(fixtures.server.Problem):pip_rewards.feed(db,me['id'],'overflow',fixtures.server.Problem,now=1000)
            self.assertEqual(pip_rewards.food(db,me['id'],now=1600)['remaining'],4800)
            self.assertEqual(pip_rewards.food(db,me['id'],now=1200)['remaining'],4800)
            state=pip_rewards.food(db,me['id'],now=6400)
            self.assertEqual(state['remaining'],0);self.assertEqual(state['bank'],1)
            self.assertEqual(pip_rewards.feed(db,me['id'],'fill-0',fixtures.server.Problem,now=6400)['remaining'],0,'A replay does not refill an empty bowl.')
            state=pip_rewards.feed(db,me['id'],'new-feed',fixtures.server.Problem,now=6400)
            self.assertEqual(state['remaining'],1800);self.assertEqual(state['bank'],0)

    def test_concurrent_feeds_cannot_spend_the_same_portion_twice(self):
        child,me=self.learner();self.check(child,'math-1')
        def send(index):return child.request('/api/pip/feed',dict(requestId='concurrent-'+str(index)))[0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:statuses=list(pool.map(send,range(2)))
        self.assertEqual(sorted(statuses),[200,409]);self.assertEqual(child.request('/api/me')[1]['pipFood']['bank'],0)

    def test_legacy_migration_preserves_unselected_items_and_original_receipts(self):
        child,me=self.learner()
        with self.app.store.db() as db:
            db.execute("DELETE FROM settings WHERE key='pipRewardSchedule'")
            db.execute('DELETE FROM pip_food WHERE learner=?',(me['id'],))
            for n in range(1,6):
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',('legacy-'+str(n),me['id'],'math-'+str(n),'[]',n,n,json.dumps(dict(passed=True,score=6))))
            pip_rewards.install(db,fixtures.server.PROFILE_OPTIONS)
            owned=pip_rewards.inventory(db,me['id'])
            self.assertEqual(len(owned),11);self.assertIn('accessory:headphones',owned)
            before=pip_rewards.wins(db,me['id'],fixtures.server.PROFILE_OPTIONS)
            self.assertEqual([len(w['pipItems']) for w in before],[3,2,3,1,2])
            pip_rewards.install(db,fixtures.server.PROFILE_OPTIONS)
            self.assertEqual(pip_rewards.food(db,me['id'])['bank'],5)
        saved=child.request('/api/profile',dict(avatar='fox',accessory='headphones',home={'decor':'stars','furniture':'desk'}))
        self.assertEqual(saved[0],200,saved[1])
        self.check(child,'math-6')
        after=child.request('/api/me')[1]
        self.assertEqual(after['moduleWins'][:5],before)
        self.assertEqual([item['key'] for item in after['moduleWins'][5]['pipItems']],['accessory:cap'])
        self.assertEqual(after['moduleWins'][5]['pipItems'][0]['modules'],6)
        self.assertEqual(after['pipFood']['bank'],6)

    def test_positions_and_twelve_character_name_are_atomic(self):
        child,me=self.learner()
        valid={'rug':{'x':.3,'y':.7},'decor':{'x':.8,'y':.6}}
        status,saved,_=child.request('/api/profile',dict(alias='TwelveChar12',avatar='frog',homePositions=valid))
        self.assertEqual(status,200,saved)
        for changes in [dict(alias='x'*13),dict(homePositions={'rug':{'x':float('nan'),'y':.2}}),dict(homePositions={'extra':{'x':.2,'y':.2}}),dict(homePositions={'rug':{'x':True,'y':.2}}),dict(homePositions={'rug':{'x':2,'y':.2}})]:
            self.assertEqual(child.request('/api/profile',dict(avatar='cat',**changes))[0],400)
            current=child.request('/api/me')[1];self.assertEqual(current['alias'],saved['alias']);self.assertEqual(current['profile'],saved['profile'])
        self.assertEqual(child.request('/api/profile',dict(avatar='cat',homePositions={}))[1]['profile']['homePositions'],{})

if __name__=='__main__':unittest.main()
