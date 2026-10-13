import random
import unittest
from collections import Counter
import server
from check_sampling import sample_check,case

class CheckSamplingTests(unittest.TestCase):
    def test_many_draws_cover_lessons_and_preserve_skill_quotas(self):
        for uid,unit in server.UNITS.items():
            skills=unit.get('checkSkills',('calculate','apply','reason'))
            for seed in range(75):
                chosen=sample_check(server.BANK[uid],skills,random.Random(seed))
                self.assertEqual(len({case(q) for q in chosen}),6,uid)
                if {1,2}.issubset({q.get('lesson') for q in server.BANK[uid]}):
                    self.assertTrue({1,2}.issubset({q.get('lesson') for q in chosen}),uid)
                available=Counter(q['skill'] for q in server.BANK[uid])
                actual=Counter(q['skill'] for q in chosen)
                quota=6//len(skills)
                if all(available[s]>=quota for s in skills):
                    self.assertEqual(actual,Counter({s:quota for s in skills}),uid)
                else:
                    for skill in skills:self.assertGreaterEqual(actual[skill],min(available[skill],2),uid)

    def test_published_practice_stays_out_of_checks(self):
        # Public practice includes answers, so no published case can appear in a check.
        still_reused=set()
        reused=set()
        for uid,unit in server.UNITS.items():
            published=set()
            def walk(value):
                if isinstance(value,dict):
                    if isinstance(value.get('prompt'),str):published.add((value.get('passage',''),value['prompt']))
                    for item in value.values():walk(item)
                elif isinstance(value,list):
                    for item in value:walk(item)
            walk(unit)
            if any((q.get('passage',''),q['prompt']) in published for q in server.BANK[uid]):reused.add(uid)
        self.assertEqual(reused,still_reused)
        # Every module on the saved 32-skill path checks only unseen cases.
        self.assertFalse(reused & {u for g in server.FOUNDATION['groups'] for u in g['units']})

if __name__=='__main__':unittest.main()
