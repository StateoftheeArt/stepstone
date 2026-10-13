"""Food replay receipts, cooldown boundaries and course dependencies."""
import json,math,re,unittest
from pathlib import Path
import pip_rewards
import test_server as fixtures
from check_sampling import sample_check
import random
ROOT=Path(__file__).resolve().parents[1]

class ReplayFoodTests(unittest.TestCase):
 setUp=fixtures.PilotTests.setUp
 tearDown=fixtures.PilotTests.tearDown
 learner=fixtures.PilotTests.learner
 check=fixtures.PilotTests.check

 def test_passed_replay_earns_food_without_duplicate_items_points_or_receipts(self):
  child,me=self.learner()
  first,_=self.check(child,'math-chart')
  original=first['me']['moduleWins']
  self.assertEqual(first['report']['pipFoodReason'],'first')
  redo,payload=self.check(child,'math-chart')
  self.assertEqual(redo['report']['pipFoodEarned'],1)
  self.assertEqual(redo['report']['pipFoodReason'],'review')
  self.assertEqual(redo['me']['pipFood']['bank'],2)
  self.assertEqual(redo['report']['points'],0)
  self.assertEqual(redo['me']['moduleWins'],original)
  self.assertEqual(child.request('/api/submit',payload)[1]['me']['pipFood']['bank'],2)
  again,_=self.check(child,'math-chart')
  self.assertEqual(again['report']['pipFoodReason'],'cooldown')
  self.assertEqual(again['report']['pipFoodEarned'],0)
  self.assertEqual(again['me']['pipFood']['bank'],2)
  self.assertEqual(again['me']['moduleWins'],original)
  other,_=self.learner('Another learner')
  self.assertEqual(other.request('/api/submit',payload)[0],404)

 def test_failed_replay_early_module_and_client_flag_do_not_earn_replay_food(self):
  child,_=self.learner()
  self.check(child,'math-chart')
  failed,_=self.check(child,'math-chart',wrong=2)
  self.assertEqual(failed['report']['pipFoodEarned'],0)
  self.assertEqual(failed['me']['pipFood']['bank'],1)
  self.check(child,'math-1')
  early,payload=self.check(child,'math-1')
  self.assertEqual(early['report']['pipFoodEarned'],0)
  forged=child.request('/api/submit',dict(payload,foodReplay=True,pipFoodEarned=99))
  self.assertEqual(forged[1]['me']['pipFood']['bank'],2)

 def test_cooldown_exact_boundary_clock_rollback_and_account_isolation(self):
  _,me=self.learner();_,other=self.learner('Second learner')
  with self.app.store.db() as db:
   def grant(learner,id,unit,now,passed=True,eligible=True):
    return pip_rewards.award_review(db,learner,id,unit,eligible,True,passed,now)
   self.assertEqual(grant(me['id'],'a','math-chart',1000)['pipFoodEarned'],1)
   self.assertEqual(grant(me['id'],'a','math-chart',2000)['pipFoodEarned'],1)
   self.assertEqual(pip_rewards.food(db,me['id'],2000)['bank'],1,'Receipt retry is inert.')
   for now in (900,87399):
    self.assertEqual(grant(me['id'],'blocked-'+str(now),'math-chart',now)['pipFoodEarned'],0)
   self.assertEqual(grant(me['id'],'b','math-chart',87400)['pipFoodEarned'],1)
   self.assertEqual(grant(me['id'],'different','math-9',87400)['pipFoodEarned'],1)
   self.assertEqual(grant(other['id'],'a','math-chart',1001)['pipFoodEarned'],1)
   self.assertEqual(grant(me['id'],'failed','math-12',87400,passed=False)['pipFoodEarned'],0)
   self.assertEqual(grant(me['id'],'early','math-1',87400,eligible=False)['pipFoodEarned'],0)
   self.assertEqual(pip_rewards.food(db,me['id'],87400)['bank'],3)
   pip_rewards.install(db,fixtures.server.PROFILE_OPTIONS)
   self.assertEqual(pip_rewards.food(db,me['id'],87400)['bank'],3,'Restart cannot backfill or duplicate replay grants.')

 def test_concurrent_passed_replays_share_the_cooldown(self):
  import concurrent.futures
  child,me=self.learner();self.check(child,'math-chart')
  attempts=[child.request('/api/attempt',{'unit':'math-chart'})[1] for _ in range(2)]
  # The API resumes one open attempt. Seed a second in this disposable account
  # to exercise two independent submissions racing for the review allowance.
  with self.app.store.db() as db:
   row=db.execute('SELECT * FROM attempts WHERE id=?',(attempts[0]['id'],)).fetchone()
   db.execute('INSERT INTO attempts(id,learner,unit,questions,started) VALUES(?,?,?,?,?)',
              ('concurrent-review-second',me['id'],'math-chart',row['questions'],row['started']))
  attempts[1]={**attempts[0],'id':'concurrent-review-second'}
  def submit(attempt):
   return child.request('/api/submit',dict(id=attempt['id'],answers=fixtures.right_answers('math-chart',attempt),reflection='I checked the labelled totals.',support='myself'))[1]['report']['pipFoodEarned']
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   self.assertEqual(sorted(pool.map(submit,attempts)),[0,1])
  self.assertEqual(child.request('/api/me')[1]['pipFood']['bank'],2)

class CourseFlowTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))
  cls.bank=json.loads((ROOT/'content/checkpoints.json').read_text(encoding='utf-8'))
  cls.units={u['id']:u for u in cls.catalog['units']}
 def test_every_course_has_forward_dependencies_and_matched_starting_suggestions(self):
  starting=json.loads((ROOT/'public/starting-point.json').read_text(encoding='utf-8'))
  eligible=[]
  for subject in self.catalog['subjects']:
   chain=sorted((u for u in self.catalog['units'] if u['subject']==subject['id'] and u.get('active') is not False),key=lambda u:u['sequence'])
   self.assertEqual([u['sequence'] for u in chain],list(range(1,25)))
   self.assertEqual(starting['extended']['suggestions'][subject['id']],[chain[p-1]['id'] for p in (1,4,7,10)])
   self.assertEqual([u['sequence'] for u in chain if u['foodReplay']],[18,21,24])
   eligible.extend(u for u in chain if u['foodReplay'])
   for unit in chain:
    for id in unit['prerequisites']:
     prior=self.units[id]
     self.assertEqual(prior['subject'],unit['subject'])
     self.assertLess(prior['sequence'],unit['sequence'],unit['id']+' must not require a later concept.')
    self.assertEqual(unit['mission']['needs'],unit['prerequisites'])
    self.assertEqual([p['id'] for p in unit['mission']['preparation']],unit['prerequisites'])
  self.assertEqual(len(eligible),18)
 def test_foundations_precede_the_tasks_that_use_them(self):
  for before,after in [
   ('math-remainders','math-4'),('math-estimate','math-budget'),('math-time','math-pay'),
   ('math-10','math-11'),('science-5','science-magnets'),('science-6','science-water'),
   ('life-prep','life-cook'),('life-cook','life-leftovers'),('pc-safe','digital-2'),
   ('digital-4','digital-forms'),('work-resume','life-job-apply'),
   ('work-safety','life-first-shift'),('work-instructions','life-first-shift')]:
   self.assertLess(self.units[before]['sequence'],self.units[after]['sequence'])
 def test_new_diagonal_answers_match_independent_geometry(self):
  unit=self.units['math-11']
  self.assertNotRegex(json.dumps(unit),r'\\sin|trigonom')
  for question in unit['practice']+self.bank[unit['id']]:
   if question['skill']=='calculate':
    match=re.search(r'is (\d+) cm high and (\d+) cm wide',question['prompt'])
    self.assertAlmostEqual(question['answer'],math.hypot(*map(int,match.groups())))
   elif question['skill']=='apply':
    match=re.search(r'is (\d+) cm\. What is the square',question['prompt'])
    self.assertEqual(question['answer'],int(match[1])**2)
 def test_all_active_checks_cover_both_lessons_with_distinct_cases(self):
  for unit in self.catalog['units']:
   if unit.get('active') is False:continue
   for seed in range(100):
    pack=sample_check(self.bank[unit['id']],unit.get('checkSkills',['calculate','apply','reason']),random.Random(seed))
    self.assertEqual(len(pack),6)
    self.assertEqual({q['lesson'] for q in pack},{1,2},unit['id'])
    self.assertEqual(len({q.get('caseId',q['prompt']) for q in pack}),6)
    skills=unit['checkSkills']
    self.assertEqual(sorted(sum(q['skill']==s for q in pack) for s in skills),[6//len(skills)]*len(skills),unit['id'])
if __name__=='__main__':unittest.main()
