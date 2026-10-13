"""Real API requests with disposable synthetic learner data; no browser coverage."""
import json
import unittest
import test_server as fixtures
import server

ADDED = ('dog','badger','rat','squirrel','bat','goblin','rock','hedgehog','otter','moth','snail','mushroom')

class PipExpansionTests(unittest.TestCase):
    setUp = fixtures.PilotTests.setUp
    tearDown = fixtures.PilotTests.tearDown
    learner = fixtures.PilotTests.learner

    def test_new_companions_and_starter_home_choices_save_and_restore(self):
        child, me = self.learner(alias='Pip',tutorial=False)
        positions = dict(painting=dict(x=.44,y=.28),shelf=dict(x=.8,y=.2))
        room = dict(painting='moon',shelf='empty',bowl='ceramic',curtains='sage')
        for species in ADDED:
            status, saved, _ = child.request('/api/profile',dict(avatar=species,home=room,homePositions=positions))
            self.assertEqual(status,200,saved)
            self.assertEqual(saved['profile']['avatar'],species)
            self.assertEqual(saved['profile']['homePositions'],positions)
            for field,value in room.items():self.assertEqual(saved['profile']['home'][field],value)
        returning=fixtures.Client(self.url)
        status,restored,_=returning.request('/api/login',dict(code=me['recovery']))
        self.assertEqual(status,200,restored)
        self.assertEqual(restored['profile']['avatar'],'mushroom')
        self.assertEqual(restored['profile']['homePositions'],positions)
        self.assertEqual(restored['points'],0)

    def test_earned_accessory_and_home_boundaries_still_apply(self):
        child,me=self.learner(alias='Pip',tutorial=False)
        status,_,_=child.request('/api/profile',dict(avatar='dog',accessory='bandana'))
        self.assertEqual(status,409)
        status,_,_=child.request('/api/profile',dict(avatar='dog',home=dict(painting='abstract')))
        self.assertEqual(status,409)
        with self.app.store.db() as db:
            for n,unit in enumerate(list(server.UNITS)[:12],1):
                report=dict(passed=True,score=6,total=6,title=server.UNITS[unit]['title'],unit=unit,points=0)
                db.execute('INSERT INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',('expansion-'+str(n),me['id'],unit,'[]',n,n,json.dumps(report)))
        status,saved,_=child.request('/api/profile',dict(avatar='dog',accessory='bandana',home=dict(painting='abstract',bowl='steel')))
        self.assertEqual(status,200,saved)
        self.assertEqual(saved['profile']['accessory'],'bandana')
        self.assertEqual(saved['profile']['home']['painting'],'abstract')
        self.assertEqual(saved['profile']['home']['bowl'],'steel')
        self.assertEqual(saved['points'],0,'Cosmetic unlocks do not mint Steps.')
        self.assertEqual(saved['pipFood']['bank'],12)
        for field in ['wall','bowl','curtains','unknown']:
            self.assertEqual(child.request('/api/profile',dict(avatar='dog',homePositions={field:dict(x=.5,y=.5)}))[0],400)
        self.assertEqual(child.request('/api/profile',dict(avatar='dog',homePositions=dict(painting=dict(x=1.2,y=.2))))[0],400)
        self.assertEqual(child.request('/api/profile',dict(avatar='unknown'))[0],400)

if __name__ == '__main__':unittest.main()
