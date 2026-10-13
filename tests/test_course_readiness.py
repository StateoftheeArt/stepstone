import json
import time
import unittest
from unittest.mock import patch
import test_server as test_support
import course_access
import daily_tasks
import server


def pass_fixture(app, learner, ids):
    """Authored passes in a disposable test database; not live learner evidence."""
    with app.store.db() as db:
        for unit in ids:
            now=time.time()
            report=dict(passed=True, score=6, total=6, questions=[], reflection='Test fixture', support='myself',
                        ink=[], at=now, points=0, unit=unit, title=server.UNITS[unit]['title'], tryNumber=1, practiceRetries=0)
            db.execute('INSERT OR IGNORE INTO attempts(id,learner,unit,questions,started,finished,report) VALUES(?,?,?,?,?,?,?)',
                       ('readiness-fixture-'+learner+'-'+unit,learner,unit,'[]',now,now,json.dumps(report)))


class CourseReadinessTests(unittest.TestCase):
    setUp=test_support.PilotTests.setUp;tearDown=test_support.PilotTests.tearDown;learner=test_support.PilotTests.learner;check=test_support.PilotTests.check
    def test_only_all_96_passes_open_both_courses(self):
        client,me=self.learner()
        ids=course_access.required_units(server.CATALOG)
        self.assertEqual(len(ids),96)
        for unit in ('pc-start','digital-5','work-strengths','social-12'):
            self.assertEqual(client.request('/api/attempt',{'unit':unit})[0],409,unit)
        client.request('/api/progress',{'unit':'pc-start','stage':7})
        self.assertEqual(client.request('/api/attempt',{'unit':'pc-start'})[0],409)
        pass_fixture(self.app,me['id'],ids[:-1])
        self.assertFalse(client.request('/api/me')[1]['courseReadiness']['complete'])
        for unit in ('pc-start','work-strengths'):
            self.assertEqual(client.request('/api/attempt',{'unit':unit})[0],409)
        pass_fixture(self.app,me['id'],ids[-1:])
        ready=client.request('/api/me')[1]['courseReadiness']
        self.assertTrue(ready['complete']);self.assertEqual(ready['completed'],96)
        self.assertEqual(client.request('/api/attempt',{'unit':'pc-start'})[0],200)
        self.assertEqual(client.request('/api/attempt',{'unit':'work-strengths'})[0],200)

    def test_old_incomplete_check_cannot_bypass_gate_but_saved_report_remains_readable(self):
        client,me=self.learner()
        with self.app.store.db() as db:
            db.execute('INSERT INTO attempts(id,learner,unit,questions,started) VALUES(?,?,?,?,?)',('old-open',me['id'],'pc-start','[]',time.time()))
        self.assertEqual(client.request('/api/attempt',{'unit':'pc-start'})[0],409)
        self.assertEqual(client.request('/api/submit',{'id':'old-open'})[0],409)
        pass_fixture(self.app,me['id'],['pc-start'])
        before=client.request('/api/me')[1]
        status,result,_=client.request('/api/submit',{'id':'readiness-fixture-'+me['id']+'-pc-start'})
        self.assertEqual(status,200);self.assertTrue(result['report']['passed'])
        self.assertEqual(result['me']['points'],before['points'])
        self.assertFalse(result['me']['courseReadiness']['complete'])

    def test_laptop_requirements_do_not_require_a_laptop_to_learn(self):
        client,me=self.learner()
        laptop=next(r for r in client.request('/api/me')[1]['rewards'] if r['id']=='core-laptop')
        self.assertEqual(laptop['required_modules'],course_access.required_units(server.CATALOG))
        self.assertEqual(laptop['path_version'],105)
        self.assertEqual(laptop['cost'],0)
        self.assertFalse(any(server.UNITS[u]['subject'] in ('digital','work') for u in laptop['required_modules']))
        # Historical card agreements keep their assigned 32-module path.
        self.assertEqual(client.request('/api/me')[1]['foundation']['total'],32)

    def test_daily_play_requires_food_and_is_private_without_extra_rewards(self):
        client,me=self.learner();other,other_me=self.learner('Other Pip')
        self.assertEqual(client.request('/api/daily/play',{})[0],409)
        self.assertEqual(client.request('/api/me')[1]['dailyTasks']['completed'],['visit'])
        result,_=self.check(client,'math-1')
        self.assertEqual(result['me']['dailyTasks']['completed'],['module','visit'])
        self.assertEqual(client.request('/api/pip/feed',{'requestId':'daily-test-feed'})[0],200)
        before=client.request('/api/me')[1]
        for _ in range(2):
            status,played,_=client.request('/api/daily/play',{})
            self.assertEqual(status,200);self.assertEqual(played['dailyTasks']['completed'],['module','play','visit'])
            self.assertEqual(played['points'],before['points']);self.assertEqual(played['pipFood']['bank'],before['pipFood']['bank'])
        self.assertEqual(other.request('/api/me')[1]['dailyTasks']['completed'],['visit'])
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM daily_tasks WHERE learner=? AND task='play'",(me['id'],)).fetchone()[0],1)
            future=time.time()+86400
            self.assertEqual(daily_tasks.snapshot(db,me['id'],future)['completed'],[])

    def test_new_colours_are_validated(self):
        client,_=self.learner()
        for accent in (a['id'] for a in server.PROFILE_OPTIONS['accents']):
            status,result,_=client.request('/api/profile',{'avatar':'fox','accent':accent})
            self.assertEqual(status,200);self.assertEqual(result['profile']['accent'],accent)
        self.assertEqual(client.request('/api/profile',{'avatar':'fox','accent':'unknown'})[0],400)

    def test_old_theme_requirements_are_removed_without_spending_points(self):
        client,me=self.learner(tutorial=False)
        with self.app.store.db() as db:
            db.execute("UPDATE rewards SET cost=40,minimum_modules=24,required_modules='[\"math-cash\"]',stock=0 WHERE kind='theme'")
            self.app.store.funded.install(db)
        before=client.request('/api/me')[1]
        for theme in ('theme-ocean','theme-sunset'):
            self.assertEqual(client.request('/api/reward',{'id':theme})[0],200)
        after=client.request('/api/me')[1]
        self.assertEqual(after['points'],before['points']);self.assertEqual(after['mastered'],[])
        self.assertIsNone(after['tutorial'])
        for theme in (r for r in after['rewards'] if r['kind']=='theme'):
            self.assertEqual(theme['cost'],0);self.assertEqual(theme['minimum_modules'],0)
            self.assertEqual(theme['required_modules'],[]);self.assertIsNone(theme['stock'])

    def test_finder_requires_mentor_authentication(self):
        client,_=self.learner()
        self.assertEqual(client.request('/api/mentor/laptops',{})[0],401)
        with patch('laptop_finder.cached_compare',return_value={'offers':[],'currency':'CAD'}):
            self.assertEqual(self.mentor.request('/api/mentor/laptops',{})[0],200)


class DailyDayTests(unittest.TestCase):
    def test_winnipeg_midnight_and_daylight_saving(self):
        from datetime import datetime,timezone
        at=lambda s:datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp()
        self.assertEqual(daily_tasks.day_at(at('2026-10-07T04:59:59')),'2026-10-06')
        self.assertEqual(daily_tasks.day_at(at('2026-10-07T05:00:00')),'2026-10-07')
        self.assertEqual(daily_tasks.day_at(at('2026-01-07T05:59:59')),'2026-01-06')
        self.assertEqual(daily_tasks.day_at(at('2026-01-07T06:00:00')),'2026-01-07')

    def test_permanent_manitoba_time_and_missing_timezone_data(self):
        from datetime import datetime, timezone
        at=lambda s:datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp()
        cases=[('2026-01-07T05:59:59','2026-01-06'),
               ('2026-10-07T04:59:59','2026-10-06'),
               ('2026-10-31T04:59:59','2026-10-30'),
               ('2026-10-31T05:00:00','2026-10-31'),
               ('2026-12-07T04:59:59','2026-12-06'),
               ('2026-12-07T05:00:00','2026-12-07')]
        for missing in (False, True):
            with patch.object(daily_tasks, 'ZONE', None if missing else daily_tasks.ZONE):
                for timestamp, expected in cases:
                    with self.subTest(missing_timezone_data=missing, timestamp=timestamp):
                        self.assertEqual(daily_tasks.day_at(at(timestamp)), expected)
