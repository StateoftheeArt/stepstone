"""Original useful-app course, integrated with the existing mission/check engine."""
from digital import lesson, q
from math_missions import spec, task
from ai_course import choice, draft

LESSONS=[
 lesson('Give your app one useful job',
  'An app takes something in, follows a rule, and shows a result. Start with a job you understand. A checklist can remember what to pack. An inventory can count supplies. A planner can add practice minutes. A saving tracker can compare saved amounts with a goal.',
  'The input is what you enter. The rule decides what is allowed and what to do. The output is what changes on screen. For a checklist: type “water”, reject an empty name, then show a new item. A condition is an if decision. A limit is also a rule: if six items already exist, do not add a seventh. A label tells someone what to enter; it is not the stored value. Changing the label should not erase the list.',
  'Sketch a shift checklist',
  ['Write the job: help me remember what to take. Leave payments and public sharing out of this first version.',
   'Name three behaviours: add an item, mark it done, keep it after I return. Sketch a title, input box, button and list.',
   'Predict: with two items, adding one makes $2+1=3$. An empty name should leave the count at $2$.'],
  'A plan and a working app are different. In Your useful app, build the version and add a real practice item before calling it working.'),
 lesson('Make one change. Check it. Keep a way back.',
  'Before a change, save a working copy. Say what should happen. Change one small part, then compare the result with your prediction. Try ordinary input, empty input, the edge of a limit, and an invalid value. A nice-looking screen can still have a wrong calculation.',
  'A boundary is the edge of an allowed range. If the maximum is six items, test six and then a seventh. Invalid means the input breaks a rule, such as a word in a quantity box. When a check fails, first compare the observed result with the stated rule. Undo can return to a recent version; a separate backup helps after browser data is cleared. The app HTML and the data backup do different jobs: HTML is the tool, the backup is its saved contents.',
  'Check a small saving tracker',
  ['Use a 25-dollar goal. Enter 10.50 and 4.25: $10.50+4.25=14.75$, so $25-14.75=10.25$ remains.',
   'Predict that “ten” is rejected. If a label change also breaks the total, undo it and inspect the smaller change.',
   'Download the app and a data backup. Reopen the app, restore the backup and compare the items and total. Try keyboard controls and a phone or narrow window; describe which you actually used.'],
  'A paid AI plan is optional. If asking AI, name one change, the existing behaviour to keep, and a test. Read code changes before running them; never add passwords, payment access or unexplained commands.')]

LABS=[[
 choice('project-scope','Keep the first job small','Which first version can you build and test with a short list?',
  ['A shift checklist that adds items and marks them done.','An app that handles every part of life and pays everyone automatically.','A tool that needs access to everyone’s private messages.'],0,'One small job gives you a result you can explain and test.'),
 choice('project-rule','Find the rule','A checklist shows an item after you type its name. Which is the rule?',
  ['The title colour.','Reject an empty name before adding an item.','The letters someone typed.'],1,'The typed name is input. The check is a rule. The new list item is output.'),
 task('project-total','Predict a changed total','A practice planner has 12 minutes and 8 minutes. You add 5. What is the new total?','number','Add all three session lengths.','$12+8+5=25$ minutes.',answer=25),
 draft('project-first-plan','Describe your first useful version','Write one useful job and one feature to leave out for now. Use a fictional example.',
  ['I named one job.','I named something outside the first version.','I can explain a useful result.'],
  'This checklist helps me pack for a practice shift. It will add items and mark them done. It will not send messages or buy supplies.')
 ],[
 choice('project-empty','Predict an empty entry','You press Add item with an empty name. What should a safe checklist do?',
  ['Keep the list unchanged and explain what is missing.','Add a blank item and pretend it worked.','Delete every saved item.'],0,'A rejected input leaves useful saved work in place.'),
 choice('project-boundary','Try the edge','A list limit is 3. It already has 3 items. What should happen when you add one more?',
  ['Add it anyway because limits are decoration.','Keep the 3 items and explain that the list is full.','Delete the oldest item without asking.'],1,'An upper limit includes the allowed maximum and rejects the next value.'),
 choice('project-undo','Respond to a bad edit','A prepared AI suggestion changes your button label but also clears the list. What should you do?',
  ['Keep it because the label looks good.','Delete your backup too.','Undo the change. Ask for only the label edit and test that items stay.'],2,'Check the behaviour you meant to keep, not just the new wording.'),
 draft('project-test-note','Write a checkable change request','Ask for one small app change. State what must stay the same and two cases to test.',
  ['I asked for one change.','I named the behaviour to keep.','I described ordinary and empty-input checks.'],
  'Rename Add to Add item. Keep the saved items and limit. Test a normal name and an empty name; the empty name should not add an item.')
 ]]

PRACTICE=[
 ('A shopping checklist needs one first job. Which fits?','Add a needed item and mark it packed.','Run an online bank.','Send every family message.','Choose a job small enough to test.'),
 ('In a planner, the typed 15 is…','An input value.','The background colour.','A backup file automatically.','Input is what the user gives the app.'),
 ('Two practice sessions are 9 and 6 minutes. What total should the app show?','15 minutes.','96 minutes.','3 minutes.','Add the two session lengths: $9+6=15$.'),
 ('A quantity box expects a whole number. You enter “many”. What should happen?','Explain the error and keep saved data.','Guess a number silently.','Erase the inventory.','Reject invalid input without destroying earlier work.'),
 ('A label change accidentally removes a saved list. Which check finds the problem?','Compare the saved items before and after.','Check only the button colour.','Read only the file name.','Regression checks test behaviour that should stay the same.'),
 ('Which pair lets you keep both the tool and its latest contents?','The app HTML and a separate current data backup.','Only a screenshot of the title.','Only a paid subscription receipt.','The program and its saved data have different roles.')]

CHECKS=[
 ('A hobby inventory starts with which useful job?','Track named supplies and quantities.','Collect everyone’s passwords.','Make every possible app at once.','Start with a clear bounded purpose.'),
 ('An item name appears as a new list row. The row is the…','Output.','Input box before typing.','Permission to spend money.','Output is the visible result of the rule and input.'),
 ('A rule says only whole quantities are allowed. Which entry is valid?','4.','four-ish.','2.5.','The chosen rule permits whole numbers, not words or fractions.'),
 ('An inventory has quantities 7 and 2. Its total should be…','9.','72.','5.','Add quantities from all saved rows.'),
 ('Changing a title should normally affect…','The displayed name, while keeping the saved items.','Every saved quantity without explanation.','The learner’s other accounts.','Keep a small edit inside its intended scope.'),
 ('A first app plan leaves public chat out. Is that a failure?','No; a small working scope can be tested and expanded later.','Yes; every app needs public chat.','Yes; private data must be shared.','Deliberate limits make a useful first version achievable.'),
 ('A list permits at most 5 items and already has 5. Adding another should…','Show the limit and keep all 5.','Silently replace item 1.','Ignore the limit.','A boundary test checks what happens at and beyond the edge.'),
 ('A saving tracker goal is 30 dollars; 8 and 7 are saved. What remains?','15 dollars.','45 dollars.','1 dollar.','Add the saved amounts, then subtract from the goal.'),
 ('An AI edit adds unexplained network code to an offline checklist. What fits?','Pause, inspect the unexpected change and return to the safe copy.','Run it because all generated code is safe.','Add private information to test it.','A change request is not permission for unrelated access.'),
 ('The page survived a reload. What does that alone prove?','This saved copy returned in that browser; a separate backup still needs checking.','Every phone has the data.','No backup is ever needed.','Local persistence and independent recovery are different checks.'),
 ('After restoring a backup, what should you compare?','The expected title, items and totals.','Only whether a button moved.','Nothing; restore always proves correctness.','Verify the restored content, not just the success message.'),
 ('A narrow browser window was tested. How should the evidence describe it?','A narrow-window test; a real-phone check remains separate.','Every physical device is proven.','The learner never used help.','Report exactly what was observed.')]

def attach(units,bank):
    uid='app-build';title='Build an app you can use';goal='Plan, build, test and keep a small app that does one useful job.'
    u=dict(id=uid,subject='digital',grade=12,sequence=40,ready=True,practical=True,minutes=45,course='project',projectWorkshop=True,
      **spec(title,goal,'Make a tool for your own routine. Keep the useful result and learn how to change it.',
       ['Choose a useful job','Test one change','Keep your app'],LESSONS,LABS,[l['watchFor'] for l in LESSONS]+[goal],
       'Explain your app’s input, rule and output. Describe one mistake, a correction and the evidence that it worked.',['digital-6','digital-8']))
    u['mission'].update(label='Your useful app',artLabel='BUILD / TEST / KEEP',preparation=[dict(id=i,title=next(v['title'] for v in units if v['id']==i)) for i in ['digital-6','digital-8']])
    u['resources']=[];u['workshop']={'kind':'scenario'}
    u['practice']=[dict(q(*r),id=f'{uid}-practice-{i}',caseId=f'{uid}-practice-{i}',lesson=1+i//3,skill=('calculate','apply','reason')[i%3]) for i,r in enumerate(PRACTICE)]
    bank[uid]=[dict(q(*r),id=f'{uid}-check-{i}',caseId=f'{uid}-check-{i}',lesson=1+i//6,skill=('calculate','apply','reason')[i%3]) for i,r in enumerate(CHECKS)]
    units.append(u)
