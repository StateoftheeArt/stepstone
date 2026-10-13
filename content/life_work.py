"""Work journeys within Communication & work, using the shared guide flow.

People, employers, postings, wages and records are fictional. Primary sources
checked 2026-09-24. Practice does not apply for work, issue a certificate or
decide a person's employment rights. Keep real employment records private.
"""
from digital import lesson, q
from life_services import attach_guides, calculation, evidence, number
from practical_missions import draft_task

CHECKED = '2026-09-24'
SOURCES = {
 'apply': ('Job Bank — prepare and send a job application', 'https://www.jobbank.gc.ca/findajob/resources/apply-for-jobs'),
 'resume': ('Job Bank — write a useful, truthful resume', 'https://www.jobbank.gc.ca/findajob/resources/write-good-resume'),
 'job-safety': ('Job Bank — check job requests and protect your information', 'https://www.jobbank.gc.ca/findajob/resources/safety-tips'),
 'youth': ('Manitoba — young workers, required course and work limits', 'https://www.gov.mb.ca/labour/standards/doc,young-workers,factsheet.html'),
 'breaks': ('Manitoba — hours and breaks', 'https://www.gov.mb.ca/labour/standards/doc,hours-and-breaks,factsheet.html'),
 'standards': ('Manitoba Employment Standards — ask about your situation', 'https://www.gov.mb.ca/labour/standards/contact.html'),
 'pay': ('Manitoba — pay statements and hours records', 'https://www.gov.mb.ca/labour/standards/doc,record-keeping,factsheet.html'),
 'deductions': ('Manitoba — what can be taken from wages', 'https://www.gov.mb.ca/labour/standards/doc,deductions,factsheet.html'),
 'claims': ('Manitoba — unpaid-wage claims, time limits and which office to use', 'https://www.gov.mb.ca/labour/standards/claims.html'),
 'unsafe': ('Manitoba Workplace Safety and Health — report unsafe work', 'https://www.gov.mb.ca/labour/safety/report-unsafe.html'),
 'refuse': ('Manitoba — the process for refusing dangerous work', 'https://www.gov.mb.ca/labour/safety/faq/right-refuse.html'),
 'adjustments': ('Manitoba — disability-related adjustments and human rights help', 'https://www.manitoba.ca/fs/imd/hr.html'),
}

APPLICATION = dict(
 id='life-job-apply',subject='social',title='Apply for a job',minutes=30,
 goal='Use a job posting to write an honest application that fits your time and skills.',
 why='You can explain what you bring even if this would be your first paid job.',
 objectives=['Find what the job needs','Show a real example','Check before sending'],
 needs=['reading-1','writing-4','digital-2','social-10'],
 sources=['apply','resume','job-safety'],help='apply',
 practiceNotice='Use the fictional applicant and posting. Nothing is sent to an employer.',
 nextSteps=['Find a posting through a source you can check. Read the tasks, hours, location, pay and application instructions. Check travel and age requirements before agreeing.',
  'Make a short resume: contact details, relevant skills, learning and honest work or unpaid examples. Use an email address you can reliably check. Ask before naming someone as a reference.',
  'Tailor the message, check the employer and send through the stated application route. Keep a private copy and date. Ask about unclear requests before sharing sensitive information.'],
 lessons=[
  lesson('Turn the posting into a short plan',
   'A posting is a notice for a job. A resume is a short account of your skills and experience. Find the tasks, hours, place and how to apply. Then compare them with what you can actually do.',
   'A useful example says what you did and what happened. Paid work is not the only source of an example: helping at an event can show careful counting or following instructions. Keep it true. Availability means the times you can work, including travel. Do not promise a start time you cannot reach.',
   'Fictional Corner Shop needs a shelf helper, Saturday 10 am to 2 pm. Apply with a short message and resume through its verified website. Ari counted supplies at a community event and can reach the shop by 9:45 am.',
   ['Match the task: counting event supplies is relevant to checking shelf stock. Describe the action without claiming a job Ari never held.',
    'From 10 am to noon is two hours; noon to 2 pm adds two more. The span is $2+2=4$ hours. Arrival at 9:45 am leaves 15 minutes before the start.',
    'Draft a message naming the role, the useful example and the available time. Follow the posting’s instructions for the resume.'],
   'Saying “I can do everything” gives less evidence than one clear, truthful example.'),
  lesson('A changed detail needs a changed reply',
   'Before sending, check the role, time and contact. A reference is someone who can describe your work; ask them first. Keep your Social Insurance Number (SIN) and banking details out of a resume. Check unexpected requests through a separate known contact.',
   'A message can look official and still be fake. A company name or friendly tone is not enough to verify it. Job Bank warns about job requests for money or sensitive information. Hiring and payroll are later steps with a verified employer. You can ask a question, suggest a workable time or decline a mismatch.',
   'New detail: the shop asks about Friday 3 pm to 7 pm instead. Ari finishes class at 3:30 pm and needs 30 minutes to travel. A separate text asks for a deposit to hold the job.',
   ['Ari could reach the shop at 4 pm. That misses the requested start by 60 minutes.',
    'Revise the message: explain the actual available time and ask whether a 4 pm start or Saturday shift is possible. Do not claim the change is agreed.',
    'Pause the deposit request. Check with the shop using its independently verified contact, without paying through the text.'],
   'An application is a request to be considered. It is not a job offer or a guarantee of work.')],
 labs=[[
  evidence('apply-match','Pick an example that fits','Ari is applying for shelf work. Which two details belong in a short application?',
   ['Ari counted event supplies and checked the list for missing items.','Ari can reach the shop before the Saturday 10 am start.','Ari should claim to have managed a shop, although that never happened.'],[0,1],'Connect an honest example and actual availability to the posting.'),
  calculation('apply-time','Check the time margin','The shift starts at 10 am. Ari can arrive at 9:45 am. How many minutes are left before the start?',15,'There are 15 minutes from 9:45 to 10:00. This is travel planning, not a requirement to work unpaid.'),
  draft_task('apply-message',dict(title='Write Ari’s application',task='Write a short message for the fictional shelf-helper role. Include Ari’s supply-counting example and Saturday availability. Mention the resume requested by the posting. Do not invent contact details.',
   example='Hello, I would like to apply for the Saturday shelf-helper role. At a community event I counted supplies and checked for missing items. I can work Saturday from 10 am to 2 pm. My resume will accompany the application through your website. Thank you, Ari.',
   checks=['I named the role and an honest example that fits it.','I gave the available time without adding a false promise.','I followed the posting and kept private details out.']))],
 [calculation('apply-clash','Notice the clash','The shop now asks for a 3 pm start. Ari could arrive at 4 pm after class and travel. How many minutes later is that?',60,'From 3 pm to 4 pm is 60 minutes. The original plan needs changing.'),
  evidence('apply-verify','Two messages arrive','A shift change arrives, followed by an unexpected text asking for a deposit. Which actions make sense?',
   ['Explain the time clash and ask about an alternative.','Verify the deposit request through the shop’s independently found contact.','Pay immediately because the text uses the shop’s name.'],[0,1],'Handle the scheduling question and verify the suspicious request separately.'),
  draft_task('apply-revise',dict(task='Write Ari’s application.',rework='Revise for the Friday request. Ari cannot arrive before 4 pm. Offer a workable option, ask for confirmation and explain how Ari will check the separate deposit text.',
   example='Thank you for the update. On Friday I can arrive at 4 pm after class and travel. Could a 4 pm start or the original Saturday shift work? Please confirm before I make plans. I will verify the separate deposit message through the shop’s known contact before taking any action.',
   checks=['I changed the time to what Ari can actually manage.','I asked instead of treating a new arrangement as agreed.','I explained how to verify the money request separately.']),True)]],
 practice=[
  number('A fictional posting lists 1 pm to 5 pm. How many hours does that time span?',4,'Both times are in the afternoon: $5-1=4$ hours. Check breaks separately when planning paid hours.'),
  q('A first-time applicant helped sort donations. Which line gives useful evidence?','I sorted donations by size and checked each box against the list.','I have held every job in the shop.','I am the best person, with no example needed.','A clear action shows a relevant skill without invented experience.'),
  q('A posting asks for a resume through its website. What should a draft plan include?','The requested resume and the verified application route.','Only an unrelated public comment.','A promise that applying guarantees a shift.','Use the instructions for this role.'),
  q('A new shift conflicts with the applicant’s class. Which reply fits?','State the available time and ask whether an alternative works.','Agree and hope nobody notices the late arrival.','Change the school timetable in the message without permission.','A clear question lets both sides check the fit.'),
  q('An unexpected recruiter asks for a bank password. What is the next step?','Do not share it; verify the request through an independent known contact.','Send it because the recruiter sounds friendly.','Put the password on the resume too.','An official-looking message does not prove a request is legitimate.'),
  q('Someone could be a useful reference. What should the applicant do first?','Ask that person whether they agree to be a reference.','Publish their phone number without asking.','Make up praise and sign their name.','A reference should know about and agree to the request.')],
 check=[
  number('A fictional job notice gives a shift from 4 pm to 7 pm. How many hours does it span?',3,'Both times are in the afternoon: $7-4=3$ hours before considering any break arrangement.'),
  number('A candidate needs 25 minutes to travel and plans 10 extra minutes for delays. How many minutes before the start should they leave?',35,'$25+10=35$ minutes. Plan travel; do not treat arrival time as unpaid work.'),
  q('An applicant has no paid experience but helped check a club’s equipment list. What belongs in the application?','A truthful description of checking that list.','A made-up management role.','A claim that unpaid experience can never be relevant.','The example can show a skill even without a previous wage.'),
  number('A role needs a 2 pm start. The applicant cannot arrive until 2:20 pm. How many minutes is the mismatch?',20,'The applicant would arrive 20 minutes after the requested start.'),
  q('Why name a task you actually performed instead of just writing “hard worker”?','It gives the reader evidence connected to the role.','It proves every required skill without checking.','It removes the need to read the posting.','A specific action supports a claim; a label alone does not.'),
  q('The posting requests a short cover message and resume. Which plan follows it?','Prepare both and use the verified route in the posting.','Send banking details instead.','Assume the employer will write the application.','Match the requested material and route.'),
  q('A proposed shift ends after the applicant’s last available ride. What should the reply do?','Explain the limit and ask whether another arrangement works.','Accept without checking a way home.','Claim a ride is confirmed when it is not.','State a real constraint before making a commitment.'),
  q('A text uses a real employer’s logo and asks for money to reserve a job. Why check elsewhere?','A copied logo does not verify the sender or payment request.','A logo guarantees the offer.','All job applications require a deposit.','Use a separately verified contact to check the request.'),
  q('A potential reference has not agreed yet. Which action fits?','Ask for permission before supplying their details.','Sign their name to a recommendation.','List a stranger with the same name.','A reference is a real person who should agree to the role.'),
  q('Why leave a SIN and bank details out of the initial resume?','They do not show job skills and create unnecessary exposure at this stage.','They are the main proof of experience.','They make an application automatically accepted.','SIN means Social Insurance Number. Verified payroll arrangements are a different stage.'),
  q('Ari has drafted an application in Stepstone. What still needs doing for a real application?','Review it and use the actual employer’s verified application route.','Wait for Stepstone to hire Ari.','Treat the learning score as an offer.','No application was sent by this lesson.'),
  q('Why ask for confirmation after suggesting a different start time?','A suggestion is not yet an agreed shift.','Any written suggestion changes the employer’s schedule automatically.','The original time no longer matters.','Both sides need to know what has actually been agreed.')],
 reflection='Using Ari’s fictional case, explain one useful example, the revised availability and how to check the unexpected request.'
)

FIRST_SHIFT = dict(
 id='life-first-shift',subject='social',title='Get ready for your first shift',minutes=30,
 goal='Plan a shift, check the instructions and ask for the training or support needed.',
 why='Knowing where to go, what to ask and when to stop guessing makes a first day easier.',
 objectives=['Plan the time','Check the instructions','Ask for what you need'],
 needs=['life-job-apply','math-pay','social-3','social-6'],
 sources=['youth','breaks','adjustments','refuse','standards'],help='standards',
 practiceNotice='This is fictional shift practice. It does not replace required training or a work-readiness certificate.',
 nextSteps=['Confirm the date, place, contact person, hours, rate, break plan and tasks. Check the trip there and back. Record hours worked, including required work activities.',
  'For a real job, check the current Manitoba young-worker rules and required course for your age and work. Ask Employment Standards if the required parent or guardian is unavailable; do not invent consent or assume an app mentor can sign instead.',
  'Ask who will train you and how to report a problem. Explain any instruction or access needs. Confirm the arrangement. For dangerous work, use the official reporting and refusal process; app messages are not urgent safety monitoring.'],
 lessons=[
  lesson('Make the day concrete',
   'Write down the day, start time, place and person to meet. Ask about the finish time, breaks and pay. CAD means Canadian dollars. Plan the trip both ways. Leave enough time to find the entrance.',
   'A time span and paid hours are different things. A stated unpaid break must be subtracted from the span. Manitoba generally requires a 30-minute break after five consecutive hours; responsibility-free breaks are usually unpaid. Check the actual arrangement. Keep your own hours record. Travel planning is not an instruction to perform unpaid work.',
   'Fictional schedule: 9 am to 3 pm, with a stated unpaid 30-minute break from noon to 12:30 pm. Travel takes 35 minutes; Jo wants 10 extra minutes to find the entrance.',
   ['Allow $35+10=45$ minutes for travel and finding the place. Leave at 8:15 am for a 9 am start.',
    'The span is six hours. The stated break is half an hour: $6-0.5=5.5$ paid hours.',
    'At the fictional rate of 20 CAD per hour, base pay is $5.5\\times20=110$ CAD before deductions. Other pay rules may also apply.'],
   'Do not subtract a “break” while doing tasks. Ask about that situation instead.'),
  lesson('Ask, confirm, then do the task',
   'You can ask for a demonstration or written steps. Repeat the plan in your own words and check it. If an instruction is unclear or unsafe, stop guessing and tell the person in charge.',
   'For an ordinary Manitoba retail job at ages 13–15, check the approved Young Worker Readiness Certificate Course, parent or guardian signature, direct adult supervision, task limits and permitted hours. The school-week limit is 20 hours, with no work from 11 pm to 6 am. Different rules or exceptions may apply to other work. A support request should explain what helps; it does not need private medical details in this app.',
   'Fictional change: Jo is 15 and already has 18 work hours scheduled in a school week. The shop proposes three more. Jo also wants written steps for the stock task.',
   ['The proposed total is $18+3=21$ hours. That is one hour above the stated 20-hour school-week limit. Jo needs a revised plan, not an automatic yes.',
    'Jo asks the supervisor to check the hours and required youth arrangements. If a required signature is unavailable, Jo can ask Employment Standards about the situation.',
    'Jo asks for the stock steps in writing and a demonstration, then confirms who will check the first attempt. Stepstone cannot issue the required certificate.'],
   'Being confident or having a high quiz score does not replace training, supervision or required permission.')],
 labs=[[
  evidence('shift-details','Find the missing detail','Jo’s message says: “Saturday, 9 am, meet Pat at the side entrance.” Which two details still need checking?',
   ['The finishing time and break arrangement.','The work tasks and who will show Jo how to do them.','Whether the stated start time is 9 am.'],[0,1],'Separate information already given from questions still open.'),
  calculation('shift-paid','Find the paid time','In this made-up schedule, Jo is there from 9 am to 3 pm with a stated unpaid half-hour break. How many paid hours remain?',5.5,'Six hours minus half an hour gives $6-0.5=5.5$ hours.'),
  draft_task('shift-plan',dict(title='Write Jo’s first-day plan',task='Plan Jo’s 9 am shift. Travel takes 35 minutes, plus 10 minutes to find the entrance. Include when to leave, who to meet and a question about the task or training.',
   example='Jo will leave at 8:15 am and meet Pat at the side entrance for the 9 am shift. Jo will confirm the 3 pm finish and the noon half-hour unpaid break. Jo will ask who will demonstrate the stock task before trying it.',
   checks=['I included travel time and the place and person to meet.','I checked the finish and break arrangement.','I asked about the task or training instead of guessing.']))],
 [calculation('shift-limit','Recheck a changed week','Jo’s fictional school-week plan has 18 hours. Three more are proposed. How many hours would the new total be?',21,'$18+3=21$ hours. Compare that total with the rule before agreeing.'),
  evidence('shift-support','Prepare the conversation','Jo is 15. The proposed total is 21 hours in a school week. Which requests fit?',
   ['Ask the supervisor to revise the hours and check the youth-work requirements.','Ask for written stock instructions and a demonstration.','Accept because the extra shift automatically overrides the rules.'],[0,1],'Check the changed schedule and ask for a concrete way to learn the task.'),
  draft_task('shift-revise',dict(task='Write Jo’s first-day plan.',rework='Revise for the proposed 21-hour school week. Include the hours issue, the written-step request and a way to ask for help if a required parent or guardian cannot be reached.',
   example='The proposed total is 21 hours, so Jo needs the school-week plan revised. Jo will ask Pat for written stock steps and a demonstration, then confirm the agreed plan. If a required parent or guardian is unavailable, Jo will ask Employment Standards about the situation rather than inventing a signature.',
   checks=['I used the revised total and asked for the schedule to be checked.','I requested a specific form of instruction and confirmation.','I included an official help route without inventing permission.']),True)]],
 practice=[
  number('A trip takes 30 minutes and the plan adds 15 minutes for finding the entrance. How many minutes should be allowed?',45,'$30+15=45$ minutes before the start.'),
  number('A fictional shift spans 7 hours with a stated unpaid half-hour break. How many paid hours remain?',6.5,'$7-0.5=6.5$ hours. Use the stated arrangement.'),
  q('A message names a place but gives no meeting person. Which reply fills the gap?','Who should I ask for when I arrive?','I will assume every entrance is the same.','I will invent the supervisor’s name.','Ask for the missing detail that affects the first step.'),
  q('Jo’s proposed plan exceeds the school-week limit described in this lesson. What should happen before agreeing?','Ask for the schedule and applicable youth-work requirements to be checked.','Accept because it is only a small difference.','Change the hours record afterward.','A small difference still changes whether the stated plan fits.'),
  q('Someone learns a task better with written steps. Which request is clear?','Could I have the steps in writing and check my first attempt with you?','You must already know what helps me.','I will pretend I understood everything.','Name the support and how you can confirm the task.'),
  q('A machine task has not been demonstrated and looks dangerous. What is a useful immediate response?','Stop guessing and tell the person in charge about the training and safety concern.','Try a random control to look confident.','Wait for an app reward before mentioning it.','Use the workplace safety process; the app is not an urgent-response service.')],
 check=[
  number('A fictional 10 am to 4 pm shift includes a stated unpaid 30-minute break. How many paid hours remain?',5.5,'The span is 6 hours; $6-0.5=5.5$ paid hours.'),
  number('A trip takes 40 minutes. The plan allows 15 more minutes to find the workplace. How many minutes before the shift should the person leave?',55,'$40+15=55$ minutes.'),
  q('A first-day message gives a time but not an address. Which question matters first?','What is the address and which entrance should I use?','What colour is the company logo?','Can I assume the address from another branch?','Check the actual meeting place before planning the trip.'),
  number('Use only this fictional base-pay calculation: 5 paid hours at CAD 22 per hour. What is the base amount before deductions, in CAD?',110,'$5\\times22=110$ CAD. This is not a complete pay-entitlement calculation.'),
  q('Why keep the break arrangement next to the shift times?','It helps distinguish time at the workplace from the stated paid time.','Every break is always unpaid regardless of tasks.','Clock times do not affect hours.','Use the actual arrangement and question a break spent doing work.'),
  q('A first-day task is unfamiliar. What should the worker request?','A demonstration and a way to check the first attempt.','Permission to guess without telling anyone.','A harder task to avoid asking.','Ask for the information needed to do this task.'),
  q('A proposed youth-work plan does not meet the limits described in the lesson. What should the learner do?','Ask for a revised plan and check the current official rules.','Hide some scheduled hours.','Treat an app score as permission.','Apply the rule to the real plan before accepting it.'),
  q('Why does passing this guide not replace the required youth-work course?','They are different courses, and this app does not issue that certificate.','Any quiz score is legally interchangeable.','A practice draft is a guardian’s signature.','Check the approved route in the official young-worker guidance.'),
  q('A required guardian is unavailable. What is a useful route for questions?','Ask Employment Standards about the actual situation.','Have an unrelated app mentor sign as the guardian.','Copy a signature without permission.','Do not invent authority or consent.'),
  q('Why confirm a request for written instructions with the supervisor?','Both people need to know what support and check-in have been agreed.','The request guarantees every detail automatically.','Asking proves the worker cannot learn.','A concrete request helps build a usable plan; it is not a judgement of worth.'),
  q('Which message describes an instruction need without private medical details?','Written steps would help me follow this task. Can we review them together?','Here are my complete medical records in the group chat.','You must guess what I need.','Describe the support needed for the task. Keep sensitive details out of the practice app.'),
  q('A worker sees a serious safety concern. Why should they not wait for a mentor reply in Stepstone?','App messages are not monitored as an urgent safety service.','A quiz unlocks the right to ask for help.','Only an app mentor can speak to a supervisor.','Tell the person in charge and use the official workplace safety route.')],
 reflection='Using Jo’s fictional case, explain the travel calculation, the changed hours and the support Jo will ask for.'
)

WORK_PROBLEM = dict(
 id='life-work-problem',subject='social',title='Handle a work or pay problem',minutes=30,
 goal='Check a pay record, describe the problem and choose the right kind of help.',
 why='A clear record and a specific question make it easier to act when something is wrong.',
 objectives=['Compare the records','Ask a clear question','Choose the help route'],
 needs=['math-pay','writing-5','social-4','life-first-shift'],
 sources=['pay','deductions','standards','claims','unsafe','refuse','adjustments'],help='unsafe',
 practiceNotice='Use fictional pay and workplace details. No message or complaint is sent from this lesson.',
 nextSteps=['Keep hours, pay statements and relevant messages privately. Match the pay-period dates, rate, hours and deductions before comparing totals. Ask about unclear amounts.',
  'For a pay question, ask payroll or the employer to explain or correct the specific item. Contact Employment Standards for help. Its claims page says to file within six months of the last day of work or of the incident, so check the dates promptly. It also directs federally regulated work to a different office. If represented by a union, ask your representative about the relevant process.',
  'For dangerous conditions, tell the person in charge and follow the official refusal/reporting process; contact Workplace Safety and Health if unresolved. For disability-related adjustments or discrimination, use Manitoba’s human rights guidance. Immediate danger needs real-world help, not an app reply.'],
 lessons=[
  lesson('Compare the same dates and labels',
   'CAD means Canadian dollars. A pay period is the set of dates covered by a payment. Gross pay is before deductions; net pay is after them. Match your hours record with that period before comparing the numbers.',
   'Multiplying hours by a rate checks basic pay for those hours. A full statement can also include overtime, vacation pay and other items. Manitoba’s guidance explains pay statements and record keeping. A difference is a reason to check the labels and ask a precise question, not proof by itself of what happened.',
   'Fictional records: Ren lists 18 regular hours at CAD 20 per hour. The statement lists 16 hours and CAD 320 base pay. The pay-period dates still need checking.',
   ['For 18 hours, the base calculation is $18\\times20=360$ CAD.',
    'The difference from the listed base pay is $360-320=40$ CAD. This compares base amounts, not the bank deposit.',
    'Ask which dates the 16 hours cover. Mention the two records and request an explanation or correction. Keep a copy of the reply.'],
   'A bank deposit is usually a net amount. Comparing it directly with basic gross pay can create a false alarm.'),
  lesson('Update the facts and choose who can help',
   'A new fact can change the problem. Correct your calculation if needed, then name the issue that remains. Pay, dangerous work and disability-related support have different help routes. You do not need to solve them alone.',
   'Manitoba’s deductions guidance lists cash shortages among costs an employer cannot take from wages. Employment Standards can explain wage concerns and claim routes. Workplace Safety and Health handles unsafe-work concerns. Disability-related adjustments concern access to doing the job; Manitoba’s human rights guidance explains that process. A practice answer cannot decide an individual case.',
   'New facts: two of Ren’s 18 hours were after this pay period ended, so 16 belong here. But the same statement also shows CAD 40 taken for a cash shortage.',
   ['Revise the base comparison: $16\\times20=320$ CAD. The base-hours difference for this period is zero; check the later two hours on the next statement.',
    'The separate cash-shortage deduction still needs attention. Ask for it to be checked against Manitoba’s deduction rules, and seek Employment Standards help if needed.',
    'For a separate dangerous-machine concern, report to the person in charge and use the safety process. Do not send only a pay query and wait for it to solve a safety issue.'],
   'Checking with the employer is not a requirement to wait indefinitely or give up access to official help.')],
 labs=[[
  calculation('work-base','Check Ren’s base pay','Ren’s fictional notes show 18 regular hours at CAD 20 per hour. What is the base amount in CAD, before deductions and other pay items?',360,'$18\\times20=360$ CAD. Check dates and other items before deciding what a full payment should be.'),
  evidence('work-records','Compare like with like','Which records help explain the difference between Ren’s notes and the statement?',
   ['The daily hours and dates, matched to the pay period.','The listed rate, hours, pay items and deductions.','Only the colour of the bank card.'],[0,1],'Dates and labels let you compare the same work and type of amount.'),
  draft_task('work-query',dict(title='Ask about the difference',task='Write a fictional pay query for Ren. The notes show 18 hours at CAD 20; the statement lists 16 hours and CAD 320 base pay. Ask which dates are included before claiming a final amount is owed.',
   example='Hello, could you help me check this pay period? My notes show 18 regular hours at 20 CAD, which gives 360 CAD before other items. The statement shows 16 hours and 320 CAD base pay. Could we compare the included dates and explain or correct the difference?',
   checks=['I identified the hours, rate and type of amount.','I asked about the pay-period dates and the specific difference.','I used fictional facts without declaring an unverified final amount owed.']))],
 [calculation('work-period','Use the corrected period','Two hours belong to the next pay period. For this period, 16 hours at CAD 20 gives CAD 320, matching the listed base pay. What is the base-pay difference in CAD now?',0,'$16\\times20-320=0$. The separate deduction still needs checking.'),
  evidence('work-route','Keep the two problems separate','A statement shows a cash-shortage deduction. A separate task involves a machine with a missing guard. Which two plans fit?',
   ['Ask about the deduction and use Employment Standards for wage help.','Tell the person in charge about the machine and use the workplace safety process.','Wait for the next app quiz before mentioning either issue.'],[0,1],'A wage question and a dangerous-work concern need different action. The app is not an urgent response channel.'),
  draft_task('work-revise',dict(task='Ask about the difference.',rework='Revise the query: 16 hours belong in this period, so its base pay matches. The separate CAD 40 cash-shortage deduction remains. Ask about that item, say which official help route fits, and note the two hours to check next period.',
   example='Thank you for checking the dates. The 16 hours at 20 CAD match this period’s 320 CAD base pay. I will check the later two hours next period. Could you review the separate 40 CAD cash-shortage deduction against Manitoba’s rules? If I need help, I can contact Employment Standards about the deduction and available steps.',
   checks=['I corrected the base-hours claim when the dates changed.','I kept the remaining deduction issue clear and specific.','I chose wage help and noted the hours to check next period.']),True)]],
 practice=[
  number('Use this fictional basic calculation: 12 regular hours at CAD 20 per hour. What is the base pay before other items, in CAD?',240,'$12\\times20=240$ CAD.'),
  q('A bank deposit is less than the statement’s gross total. What should be checked before calling it missing pay?','The listed deductions and net amount, along with the dates.','Only the biggest number.','Whether the deposit can be treated as gross automatically.','Gross and net measure different stages of the pay calculation.'),
  q('Which message gives payroll something useful to check?','My record lists Tuesday’s four hours, but I cannot find them in this period. Can we compare the dates?','Everything is wrong, with no dates or details.','My app Steps prove the amount I must be paid.','Name the record, period and item that need checking.'),
  q('New dates show two hours belong to the next period. What changes?','Move those hours to the next-period check and recalculate this period.','Keep claiming they belong to both periods.','Delete all hours records.','Revise the calculation when the evidence changes.'),
  q('A worker needs to ask about an unresolved wage deduction. Which official route fits?','Manitoba Employment Standards.','The driver licensing office.','Only the app rewards page.','Use the wage-help route and check any claim time limit.'),
  q('A worker wants help with disability-related adjustments. Which resource fits that question?','Manitoba’s human rights and reasonable-accommodation guidance.','A tax refund calculator.','A promise that every requested change is automatic.','Accommodation means changing how something is done to address an individual protected need; check the process and situation.')],
 check=[
  number('Fictional base-pay check: 14 regular hours at CAD 21 per hour. What is the amount before other items, in CAD?',294,'$14\\times21=294$ CAD.'),
  number('For the same fictional pay period, two regular hours at CAD 22 are missing from a base-pay comparison. What is their base value in CAD?',44,'$2\\times22=44$ CAD before other items. Keep the dates and labels with the calculation.'),
  q('Two pay records use different date ranges. What comes before comparing their totals?','Match the dates and identify which hours each record covers.','Assume both describe the same work.','Add them without reading the labels.','A difference can come from comparing different periods.'),
  number('A fictional statement gives total gross pay CAD 440 and total deductions CAD 35. Using only those supplied amounts, what is net pay in CAD?',405,'$440-35=405$ CAD. This uses supplied totals, not a tax calculation.'),
  q('Why name the particular date and item in a pay query?','The other person can locate the record and check the difference.','A longer accusation guarantees payment.','Specific records remove all need to verify the calculation.','A precise question is easier to investigate and answer.'),
  q('Which pair is a useful pay record to keep privately?','Daily hours and the matching pay statement.','Only an app badge and the company logo.','A public post containing everyone’s banking details.','Keep relevant evidence without publishing private information.'),
  q('The employer explains that three hours fall after the period ended. What should the worker check?','Recalculate this period and look for those hours in the next one.','Count the hours in both periods.','Assume no work after a cutoff can ever be paid.','The date explanation changes the comparison; it does not erase the hours.'),
  q('A serious machine hazard is separate from a wage dispute. Why choose another route for it?','A safety concern needs the workplace safety process, not just a payroll reply.','A payroll calculation repairs machinery.','Nothing can be done until the wage issue is closed.','Report to the person in charge and use the official safety guidance.'),
  q('A person is unsure which wage office covers their job. What should they do?','Use the claims guidance or contact Employment Standards to check the right route.','Assume all Canadian jobs use the same provincial process.','Let an app score decide the jurisdiction.','The official page identifies different routes, including federally regulated work.'),
  q('Why check claim time limits while seeking help?','Waiting can affect the available complaint route.','No work-related process has a deadline.','A saved app draft automatically stops every deadline.','Check current official instructions promptly; a practice draft files nothing.'),
  q('A disability-related instruction need remains unresolved. Which source fits?','Manitoba’s human rights and reasonable-accommodation guidance.','The bank’s card-replacement page.','A rule that everyone must learn the same way.','Use the relevant support process; the app does not determine an individual legal result.'),
  q('Why correct an earlier pay claim when new dates explain part of it?','It separates the resolved calculation from any issue that still needs action.','Changing your mind means all later questions are forbidden.','The first calculation must be kept even if its dates were wrong.','A sound plan follows the evidence and names what remains unresolved.')],
 reflection='Using Ren’s fictional case, explain what the new dates changed, what issue remains and which help route fits it.'
)

MODULES = [APPLICATION, FIRST_SHIFT, WORK_PROBLEM]

# The existing sampler takes two questions per skill. Calculations come from
# lesson 1; at most one reasoning question does, guaranteeing both ideas in
# every draw while retaining several possible checks.
CHECK_SKILLS = ['calculate','calculate','apply','calculate','reason','apply',
                'apply','reason','apply','reason','apply','reason']
for module in MODULES:
    assert len(module['check']) == len(CHECK_SKILLS)
    for question, skill in zip(module['check'],CHECK_SKILLS):
        question['skill'] = skill

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)
