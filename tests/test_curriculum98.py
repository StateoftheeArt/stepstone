import json,random,unittest
from pathlib import Path
from check_sampling import sample_check

ROOT=Path(__file__).resolve().parents[1]
class Curriculum98Tests(unittest.TestCase):
    def test_new_banks_cover_six_fresh_cases_and_three_skills(self):
        catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))
        bank=json.loads((ROOT/'content/checkpoints.json').read_text(encoding='utf-8'))
        authored=[u for u in catalog['units'] if isinstance(u.get('visual'),dict)]
        self.assertEqual(len(authored),51)
        for unit in authored:
            practice={q['caseId'] for q in unit['practice']}
            for seed in range(100):
                qs=sample_check(bank[unit['id']],unit.get('checkSkills',['calculate','apply','reason']),random.Random(seed))
                self.assertEqual(len({q['caseId'] for q in qs}),6)
                self.assertFalse(practice.intersection(q['caseId'] for q in qs))
                self.assertEqual({q['lesson'] for q in qs},{1,2})
                self.assertEqual(sorted(sum(q['skill']==skill for q in qs) for skill in unit.get('checkSkills',['calculate','apply','reason'])),[2,2,2])
    def test_all_legacy_lesson_ids_survive_reorganisation(self):
        catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))
        baseline=ROOT.parent/'baseline.json'
        # The retained original lesson domains keep old saved links meaningful.
        for area,amount in [('math',12),('reading',12),('writing',12),('science',12),('social',12),('digital',8)]:
            for n in range(1,amount+1):self.assertTrue(any(u['id']==area+'-'+str(n) and u.get('domain')==area for u in catalog['units']))
        self.assertEqual({u['id'] for u in catalog['units'] if u.get('active') is False and u['id'].startswith('digital-')},{'digital-photos','digital-backup'})
if __name__=='__main__':unittest.main()
