"""Cosmetic unlock and persistence boundaries in disposable learner accounts."""
import json
import unittest
import test_server as fixtures
from test_server import Client


def expanded_room(room):
    # Legacy four-field saves retain those choices and receive the new defaults.
    return dict(painting='landscape',shelf='books',bowl='gold',curtains='linen',**room)


class PipHomeTests(unittest.TestCase):
    setUp=fixtures.PilotTests.setUp
    tearDown=fixtures.PilotTests.tearDown
    learner=fixtures.PilotTests.learner
    check=fixtures.PilotTests.check

    def save(self,child,**changes):
        return child.request('/api/profile',dict(avatar=child.request('/api/me')[1]['profile']['avatar'],**changes))

    def test_starter_room_and_rejected_changes_are_atomic(self):
        child,me=self.learner()
        room=dict(wall='sand',rug='round',furniture='cushion',decor='plant')
        status,saved,_=child.request('/api/profile',dict(alias='North',avatar='frog',home=room))
        self.assertEqual(status,200,saved)
        before=child.request('/api/me')[1]
        for change in (dict(home={**room,'furniture':'chair'}),dict(accessory='sprout'),dict(home={'wall':'unknown'}),dict(home=[]),dict(home={'extra':'plant'})):
            status,_,_=child.request('/api/profile',dict(alias='Changed',avatar='cat',**change))
            self.assertIn(status,(400,409))
            after=child.request('/api/me')[1]
            self.assertEqual((after['alias'],after['profile'],after['points']),(before['alias'],before['profile'],before['points']))
        self.assertEqual(self.save(child,accent='violet')[1]['profile']['home'],expanded_room(room))
        self.assertEqual(Client(self.url).request('/api/profile',dict(home=room))[0],401)

    def test_first_pass_unlocks_and_repeats_do_not_unlock_future_items(self):
        child,me=self.learner()
        self.check(child,'math-1')
        self.check(child,'math-2')
        self.check(child,'math-3')
        self.check(child,'math-4')
        self.check(child,'math-5')
        self.check(child,'math-6')
        before=child.request('/api/me')[1]
        room=dict(wall='lavender',rug='woven',furniture='cushion',decor='lamp')
        saved=self.save(child,home=room,accessory='sprout')
        self.assertEqual(saved[0],200,saved[1])
        self.assertEqual(saved[1]['points'],before['points'],'Cosmetics do not spend or award points.')
        self.check(child,'math-1')
        self.assertEqual(self.save(child,home={**room,'furniture':'chair'})[0],409)
        other,_=self.learner('Other')
        self.assertEqual(self.save(other,home=room)[0],409)
        self.assertEqual(self.save(other,home=room,learner=me['id'])[0],409)
        returning=Client(self.url)
        loaded=returning.request('/api/login',dict(code=me['recovery']))[1]
        self.assertEqual(loaded['profile']['home'],expanded_room(room))
        self.assertEqual(loaded['profile']['accessory'],'sprout')

    def test_distinct_passes_unlock_furniture_and_accessories(self):
        child,_=self.learner()
        # Synthetic reward-boundary records, separate from actual graded checks.
        learner_id=child.request('/api/me')[1]['id']
        units=[u['id'] for u in fixtures.server.UNITS.values() if u.get('active')][:48]
        for n,unit in enumerate(units,1):
            with self.app.store.db() as db:
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',('milestone-'+str(n),learner_id,unit,'[]',n,n,json.dumps(dict(passed=True,score=6,total=6))))
            if n==8:self.assertEqual(self.save(child,home={'wall':'night'})[0],200)
            if n==12:self.assertEqual(self.save(child,home={'furniture':'chair'})[0],200)
            if n==24:self.assertEqual(self.save(child,accessory='scarf',home={'rug':'star','decor':'books'})[0],200)
            if n==30:self.assertEqual(self.save(child,home={'furniture':'desk'})[0],200)
        before=child.request('/api/me')[1]
        saved=self.save(child,accessory='headphones',home={'decor':'stars'})[1]
        self.assertEqual(saved['profile']['home'],expanded_room(dict(wall='night',rug='star',furniture='desk',decor='stars')))
        self.assertEqual(saved['points'],before['points'])

    def test_legacy_owned_items_are_retained(self):
        child,me=self.learner()
        room=dict(wall='night',rug='star',furniture='desk',decor='stars')
        # Migration fixture, not learning completion evidence.
        with self.app.store.db() as db:
            db.execute('INSERT OR REPLACE INTO profiles(learner,details) VALUES(?,?)',(me['id'],json.dumps(dict(avatar='fox',accessory='headphones',home=room))))
        saved=self.save(child,alias='North',accessory='headphones',home=room)
        self.assertEqual(saved[0],200,saved[1])
        self.assertEqual(saved[1]['profile']['home'],expanded_room(room))
        self.assertEqual(saved[1]['totalChecks'],0)


if __name__=='__main__':unittest.main()
