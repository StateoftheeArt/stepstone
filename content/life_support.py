"""Support skills using fictional situations and the existing mission flow.

Sources checked 2026-09-24. This is preparation, not counselling, diagnosis,
an accommodation decision or a contact channel to any listed service.
"""
from digital import lesson, q
from math_missions import task
from practical_missions import draft_task
from life_services import attach_guides, evidence, number, calculation, table, with_context

CHECKED = '2026-09-24'
SOURCES = {
 'primary-care': ('Manitoba — finding primary care', 'https://www.gov.mb.ca/health/familydoctorfinder/'),
 'health-advice': ('Manitoba — Health Links and care options', 'https://www.gov.mb.ca/health/primarycare/access/'),
 '211': ('211 Manitoba — find community help', 'https://mb.211.ca/get-help-now/'),
 '211-privacy': ('211 Manitoba — chat and privacy questions', 'https://mb.211.ca/chat-faq/'),
 'trusted-person': ('Kids Help Phone — finding a safe adult', 'https://kidshelpphone.ca/get-info/how-identify-safe-adult'),
 'khp-privacy': ('Kids Help Phone — privacy and confidentiality', 'https://kidshelpphone.ca/privacy-policy/'),
 'adjustments': ('Manitoba — human rights and reasonable accommodation', 'https://www.manitoba.ca/fs/imd/hr.html'),
 'medical-info': ('Manitoba Human Rights Commission — medical information at work', 'https://www.manitobahumanrights.ca/education/pdf/fact-sheets/factsheet_medical_information.pdf'),
 'rights-help': ('Manitoba Human Rights Commission — current contact options', 'https://www.manitobahumanrights.ca/about/contact.html'),
}

VISIT = table('Fictional appointment message', ['Detail','What the message says'], [
 ['Day','Tuesday, in this made-up week'],['Visit starts','10:30 a.m.'],
 ['Check in by','10:15 a.m.'],['Place','Oak Clinic, in person'],
 ['Travel to the door','25 minutes riding, then 5 minutes walking'],
 ['Before leaving','Confirm what to bring with the clinic']])
HELP_CARDS = table('Fictional services — practise comparing', ['Service','Who / cost','How to get help'], [
 ['Form Desk','Ages 16 and over; free','Tuesday 4–6 p.m.; book a place by phone'],
 ['Device Shop','All ages; repair charges apply','Walk in for phone repairs'],
 ['Learning Desk','Ages 10–15; free','Wednesday 4–6 p.m.; ask about form help']])

APPOINTMENT = dict(
 id='life-appointment',title='Plan an appointment',goal='Read the booking details, plan the time and ask a clear question.',
 why='An appointment has several moving parts. A short plan helps you get there, say what you need and know what happens next.',
 objectives=['Read the booking','Plan the time','Handle a change'],needs=['reading-1','writing-6'],
 sources=['primary-care','health-advice'],help='health-advice',
 practiceNotice='Use the fictional visit. Do not enter real health details. This app does not book or contact a service.',
 nextSteps=['Use the provider’s own contact details to confirm the date, time, place or call method, and what to bring.',
  'Allow for travel and the requested check-in time. Prepare a short question and ask for any help you need to take part.',
  'If plans change, contact the provider. Repeat back the agreed next step. Family Doctor Finder is for finding primary care; Health Links offers health advice, not a Stepstone booking.'],
 lessons=[
  lesson('Work back from check-in',
   'Read the day, time and place. Check-in can be earlier than the visit. Work back from check-in to find when to leave. Use the clinic’s message, not a guess.',
   'A start time and an arrival time do different jobs. Work backwards from the requested arrival: subtract the whole journey, including the walk. This gives a latest departure for the stated journey; real delays may need more room. A request for a booking is not yet a confirmed booking.',
   'Fictional visit: Tuesday at 10:30 a.m.; check in at 10:15. Travel takes 25 minutes riding and 5 minutes walking.',
   ['Total travel is $25+5=30$ minutes.',
    'Thirty minutes before 10:15 is 9:45 a.m. That is the latest departure for these stated times.',
    'Confirm the place and what to bring. Add room for delays when planning a real trip.'],
   'The appointment time is not always the time you should reach the door.'),
  lesson('Confirm the change and next step',
   'A changed time or phone visit needs a new plan. Ask what is agreed. Before a visit ends, say the next step back in your own words. Ask again if it is unclear.',
   'Repeating a plan exposes gaps: who will call, at what time, and what should happen if the call is missed? A private place and a working phone may matter. If the new plan will not work, ask about alternatives rather than quietly treating an unconfirmed option as settled.',
   'The clinic offers a phone visit at 11:00 a.m. Kai has class then and cannot speak privately.',
   ['Kai explains the clash without giving health details in a public message.',
    'Kai asks for another time and asks who will call whom. The offered change stays pending until confirmed.',
    'After the visit, Kai asks: What do I do next, by when, and who do I contact if I am unsure?'],
   'A learning plan cannot assess symptoms. Use the appropriate care service; immediate danger needs emergency help.')],
 labs=[[
  with_context(evidence('appointment-details','Read Kai’s message','Which two details set Kai’s latest departure time?',
   ['Check in by 10:15 a.m.','The whole journey takes 30 minutes.','The clinic name contains two words.'],[0,1],
   'Work back from check-in using the whole journey, including the walk.'),grid=VISIT),
  calculation('appointment-travel','Count the whole journey','Kai rides for 25 minutes and walks for 5. How many minutes does the journey take?',30,'$25+5=30$ minutes. Keep the walk in the plan.'),
  draft_task('appointment-plan',dict(title='Write a visit plan',task='For Kai, write the check-in time, latest departure for the stated journey and one question to confirm before leaving.',
   example='Kai checks in Tuesday at 10:15 a.m. The stated trip takes 30 minutes, so 9:45 is the latest departure. Kai should confirm what to bring and allow for delays.',
   checks=['I used check-in rather than the later visit start.','I included riding and walking.','I added a question without real health details.']))],
 [evidence('appointment-change','A phone visit is offered','Kai has class at the offered 11:00 a.m. time and cannot talk privately. Which details need a response?',
   ['The time clashes with class.','The place is not private enough for the call.','The phone case is a different colour.'],[0,1],
   'Say which parts will not work so the provider can discuss another arrangement.'),
  evidence('appointment-confirm','Check the reply','Which lines would show an agreed phone plan rather than a request still waiting for a reply?',
   ['The clinic confirms Thursday at 2:00 p.m.','The clinic says it will call Kai and gives missed-call instructions.','Kai has typed a new time but has not sent it.'],[0,1],
   'Confirmation comes from the provider. A draft or proposal alone does not change the appointment.'),
  draft_task('appointment-revise',dict(task='Plan Kai’s visit.',rework='Revise the plan: the clinic offers an 11:00 a.m. phone visit, but Kai has class and no private place then. Ask for a workable option and explain what still needs confirmation.',
   example='Kai will ask for another time because of class and privacy. Kai will confirm the new time, who calls whom, and what to do if the call is missed before treating the change as agreed.',
   checks=['I included the time and privacy obstacles.','I asked a specific question about the call.','I kept a proposed time separate from a confirmed one.']),True)]],
 practice=[
  number('A made-up trip takes 18 minutes riding and 7 minutes walking. How many minutes altogether?',25,'$18+7=25$ minutes. Include both parts.'),
  q('Check-in is at 2:00 p.m. The whole trip takes 20 minutes. What is the latest departure for these stated times?','1:40 p.m.','2:00 p.m.','2:20 p.m.','Work back 20 minutes from check-in. Allow extra room for real delays.'),
  q('A message says your booking request was received. What is still needed?','Confirmation of the actual booking details.','Assuming the requested time is already agreed.','Turning up without checking the location.','Received and confirmed describe different stages.'),
  q('An offered call clashes with class. What makes the reply useful?','Name the clash and ask for another workable option.','Say the new time is agreed when it is not.','Ignore it and assume the provider knows.','The provider needs to know which part of the plan will not work.'),
  q('You are unsure who calls whom. What should you ask?','Will you call me, or should I call you?','Does the phone colour matter?','Can I assume all providers use the same method?','Ask directly about the missing step.'),
  q('The visit ends with a next step you do not understand. What can help?','Say what you think it means and ask them to check it.','Nod and invent the missing instruction later.','Copy a stranger’s plan instead.','Repeating the next step is a check on the instructions, not a test of politeness.')],
 check=[
  number('A journey takes 22 minutes on a bus and 8 minutes on foot. How many minutes in total?',30,'$22+8=30$ minutes.'),
  number('A visit starts at 3:20 p.m. Check-in is 15 minutes earlier. How many minutes after 3:00 p.m. is check-in?',5,'$20-15=5$: check-in is at 3:05 p.m.'),
  q('Check-in is at 9:10 a.m. Travel takes 35 minutes. Which latest departure matches these stated times?','8:35 a.m.','8:45 a.m.','9:10 a.m.','9:10 minus 35 minutes is 8:35. The calculation crosses the hour.'),
  number('The clinic asks for two forms. One is ready. How many still need checking?',1,'$2-1=1$ form remains; confirm the real requirements with the provider.'),
  q('Why use the check-in time when planning the trip?','The provider needs you there before the visit starts.','The visit start and check-in are always identical.','Travel time disappears if you have an appointment.','Each time has a purpose. Plan for the requested arrival.'),
  q('Which question belongs before an unfamiliar first visit?','What should I bring, and where do I check in?','Can I assume every clinic wants the same things?','Does saving this quiz book the visit?','Check the requirements with this provider.'),
  q('A phone visit is offered during a work shift. What should you do?','Ask for an option that fits and wait for confirmation.','Mark a different time confirmed without asking.','Treat the old visit as cancelled without checking.','Explain the clash and confirm the new arrangement.'),
  q('Why ask what happens if a call is missed?','It gives a clear recovery step if the plan goes wrong.','It guarantees the call cannot be missed.','It changes the appointment into an emergency service.','A recovery plan handles uncertainty; it does not remove it.'),
  q('A provider says, “We will call you at 1:30.” What still may need planning?','A working phone and a suitable place to take the call.','A trip to the clinic without checking.','Sharing health details in a public comment.','The format changes what you need to prepare.'),
  q('Why repeat a next step back before ending a visit?','It lets the provider correct a misunderstanding.','It proves the condition has gone away.','It replaces any follow-up the provider advised.','Check that both people mean the same next action.'),
  q('Someone needs help finding a regular primary-care provider in Manitoba. Which route fits that task?','Family Doctor Finder.','A Stepstone check receipt.','A driving-test booking page.','Family Doctor Finder helps people find primary care; it is not urgent assessment or a confirmed appointment.'),
  q('Why is a saved visit plan not proof that an appointment exists?','The provider still has to confirm the booking.','Writing a date sends it to every clinic.','A quiz score changes the provider’s schedule.','The learning record and the provider’s booking are separate.')],
 reflection='Using Kai’s fictional case, explain the changed plan and one detail you still need the clinic to confirm.'
)

FIND_HELP = dict(
 id='life-find-support',title='Find the right help',goal='Match a need to a service and make a backup plan.',
 why='You do not have to know every service name. Learn to describe the job you need help with and check whether a service fits.',
 objectives=['Name the need','Compare the options','Choose a backup'],needs=['reading-3','writing-6'],
 checkSkills=['interpret','apply','reason'],sources=['211','211-privacy','trusted-person','khp-privacy'],help='211',
 practiceNotice='The service cards are made up. Use fictional details; your practice draft is not sent to a support service.',
 nextSteps=['Describe the help you need in one sentence. 211 Manitoba can help you find community services; its Get help page lists contact options.',
  'Check who the service helps, cost, current hours, access needs and how to book. Ask what is private and when information may be shared.',
  'Confirm the next step with the service. If the route does not fit, ask for an alternative. You can open help without completing this lesson.'],
 lessons=[
  lesson('Match the help to the job',
   'Start with the need: I need help filling in a form. Then check who the service helps, what it costs and how to reach it. A familiar name is not enough.',
   'A service can be real and still be wrong for this job. Compare the need with the service’s purpose, age rules, cost and booking method. A listed opening time is not a promise of a free place. Ask the service about availability and requirements.',
   'Fictional case: Rae is 17 and wants free help with a form after 4:00 p.m.',
   ['Form Desk offers form help for ages 16 and over. Its Tuesday time fits Rae.',
    'Device Shop repairs phones; Learning Desk’s stated age range does not fit Rae.',
    'Rae still needs to phone Form Desk to ask about a place and what to bring.'],
   'A search result or referral is a lead to check, not a guaranteed appointment.'),
  lesson('Make a backup without oversharing',
   'If the first route is full or closed, ask for another. Give the details needed for the next step. Before sharing private information, ask who can see it and why it is needed.',
   'A useful request names the job and the obstacle. “I need form help, but that session is full” gives a helper something specific to work with. Privacy rules differ between services and contact methods, and can have exceptions. Ask rather than assume total secrecy or post documents publicly.',
   'Form Desk has no places this week. Rae can make a phone call but has no mobile data.',
   ['Rae asks whether another session or another service offers the same help.',
    'For a real search in Manitoba, Rae could phone 211 and describe the need and access limit.',
    'Rae records a suggested next step as unconfirmed until the receiving service agrees. No real documents belong in this lesson.'],
   'Not getting a place on the first try is a service-access problem, not a judgement of your worth.')],
 labs=[[
  with_context(evidence('support-match','Compare Rae’s options','Rae is 17, needs free form help and is free after 4:00 p.m. Which details make Form Desk a possible fit?',
   ['It offers the right help to ages 16 and over at no charge.','Its Tuesday 4–6 p.m. session fits the available time.','It has guaranteed Rae a place without a phone booking.'],[0,1],
   'The need, age, cost and time fit the fictional card. A place is still unconfirmed.'),grid=HELP_CARDS),
  evidence('support-missing','Find the missing checks','Before treating the visit as settled, what should Rae confirm?',
   ['Whether a place is available and how to book it.','What to bring and whether the location is accessible.','Whether a quiz pass has booked the service.'],[0,1],
   'Check the practical details with the service; a learning score does not reserve a place.'),
  draft_task('support-plan',dict(title='Write a help request',task='Write Rae’s short phone request: the job, why Form Desk looks suitable and the detail that still needs checking.',
   example='I need help filling in a form. I am 17 and can come after 4. Is there a free place at Tuesday’s Form Desk, and what should I bring?',
   checks=['I named the form-help task.','I included only relevant made-up details.','I asked about a place rather than assuming one.']))],
 [evidence('support-backup','The session is full','Rae has no mobile data but can make a call. Which actions could move the plan forward?',
   ['Ask Form Desk about another session or a referral.','Phone 211 Manitoba to ask about suitable community help.','Assume Rae must solve it alone because the first session is full.'],[0,1],
   'Try a route that fits the available access. Another option still needs checking.'),
  evidence('support-privacy','Ask before sharing','Which questions help Rae understand a service’s privacy rules?',
   ['Who will see this information, and why do you need it?','When might you have to share it with someone else?','Can I upload my real documents into this quiz instead?'],[0,1],
   'A service can explain its own rules and limits. Stepstone is not an application or confidential counselling channel.'),
  draft_task('support-revise',dict(task='Plan Rae’s request.',rework='Revise the request: the first session is full, and Rae has no mobile data but can make a phone call. Add a backup route and a privacy question.',
   example='Rae will phone Form Desk about another session, or ask 211 about free form help that can be arranged by phone. Before sharing documents, Rae will ask who can see them and why they are needed.',
   checks=['I used a route Rae can access.','I kept the new service or time unconfirmed until checked.','I included a privacy question without real personal details.']),True)]],
 practice=[
  q('A card offers free homework help for ages 12–15. Lee is 19 and needs housing advice. What does the card show?','This service does not match the stated age and task.','Free means it handles every need.','A friendly name means the age rule can be ignored.','Read the purpose and eligibility together.'),
  q('A service opens at 4 but requires a booking. What should you check?','Whether a place is available and how to reserve it.','Only the opening time.','Whether arriving early replaces all booking rules.','Opening and availability are different details.'),
  q('A search result lists form help but no cost. Which question fills the gap?','Is there a fee for this help?','Can I assume every listed service is free?','How many Steps is the logo worth?','An unstated cost is unknown, not automatically zero.'),
  q('The first session is full. Which reply helps find another option?','Is there another session or service for this same need?','Then nobody can help anywhere.','I will claim I already have a place.','Keep the need clear while changing the route.'),
  q('A helper asks for private details. What is a useful question?','Why do you need this, who can see it and what are the privacy limits?','Can I assume secrecy has no exceptions?','Should I post it publicly first?','Check the rules for this service and contact method.'),
  q('211 suggests a service. What does that mean?','You have a possible route to confirm with that service.','Every eligibility condition has been approved.','You have automatically attended a visit.','A referral helps navigation; it does not guarantee a place.')],
 check=[
  q('A service card says “18 and over, job search help.” A 16-year-old needs reading support. What can you conclude?','The stated age and purpose do not fit this case.','All support services are identical.','The learner must have no other options.','Use the actual conditions to compare; a poor match does not rule out other help.'),
  q('A listing says “phone to arrange a visit.” What is the next step it states?','Call to ask about arranging the visit.','Assume a visit is already booked.','Send documents to an unrelated social account.','Read the action in the instruction.'),
  q('A free service matches the need but its building cannot be accessed by the learner. What should be asked?','What accessible ways of getting this help are available?','Can the access problem be ignored?','Does free mean everyone can physically enter?','Cost and access are separate checks.'),
  q('A card lists hours but says nothing about fees. What is the fee status?','Unknown until checked.','Definitely zero.','Definitely unaffordable.','Missing information should stay unknown, rather than turn into a guess.'),
  q('Why start with “I need help completing a form” instead of only naming a building?','It lets a helper match the actual task to a suitable service.','It guarantees approval of the form.','It means no other information can ever be needed.','A clear need gives the search a useful purpose.'),
  q('Two services help with forms. One fits the age and budget; the other does not. Which is a sensible lead?','The matching service, while confirming booking and access.','The one with the brighter logo.','Neither, because asking for help means failure.','Relevant conditions matter more than appearance.'),
  q('A website cannot load, but a phone is available. What is a workable next step in Manitoba?','Call 211 to ask about community help and access options.','Assume every service is online-only.','Share a private document with a random caller.','Use an available verified contact route.'),
  q('Why ask about another option after a waiting-list message?','The first route may not meet the current need or timing.','It proves the first service is dishonest.','A waiting list guarantees help today.','Describe the obstacle without guessing motives or availability.'),
  q('A helper suggests Tuesday, but the service has not confirmed. How should you record it?','Suggested Tuesday visit — confirmation needed.','Completed Tuesday visit.','Guaranteed accepted application.','Keep the status as precise as the evidence allows.'),
  q('Why ask about exceptions to confidentiality?','Different services and situations can have limits on privacy.','Every service shares everything publicly.','Asking makes all privacy protections disappear.','Ask the provider about its actual rules; avoid either absolute assumption.'),
  q('You are helping a fictional person and the task asks for a plan. What belongs in the answer?','A made-up need, a suitable route and a question to confirm.','Your household’s real documents.','A real password so the mentor can apply for you.','Practise the process without exposing personal records.'),
  q('Why should help links remain usable before a quiz pass?','Getting support should not depend on earning a learning score.','A quiz can establish every service’s eligibility.','Help is a reward purchased with points.','Support and assessment serve different purposes.')],
 reflection='Explain Rae’s first choice, the backup route and one question that protects privacy. Keep the details fictional.'
)

BOUNDARY_CASE = table('Fictional messages — keep the limit clear', ['Person','Message'], [
 ['Ari','I can help with the form until 6:00. Then I need to leave.'],
 ['Jo','Can you stay until 7:00 instead?'],
 ['Ari’s plan','Leave at 6:00; sharing a password is not part of the offer.']])
ADJUSTMENT_CASE = table('Fictional training task', ['Detail','What is happening'], [
 ['Task','Pack an order using four steps'],
 ['Barrier','All four steps are spoken quickly in a noisy room'],
 ['What already helps','Sam follows one written step at a time'],
 ['Goal','Pack the order accurately and safely']])

BOUNDARIES = dict(
 id='life-boundaries',subject='social',title='Protect your time and privacy',
 goal='State a limit, respect another person’s choice and handle pressure.',
 why='You can care about someone and still have a limit. Practise clear words and a backup step without sharing a personal story.',
 objectives=['Name your limit','Try your words','Respond to pressure'],needs=['social-1','writing-2'],
 checkSkills=['interpret','apply','reason'],sources=['trusted-person','khp-privacy','211'],help='trusted-person',
 practiceNotice='Use Ari and Jo’s fictional messages. Do not describe a real conflict or confront anyone to finish this lesson.',
 nextSteps=['Decide what you are willing and able to do. Use a short, clear statement; a long personal explanation is not required.',
  'Offer another option only if you want to and can follow through. Respect the other person’s right to decline it.',
  'If pressure continues, seek support or leave the exchange when safe. A trusted person can be outside your home. Use the help links for real support; this lesson sends no message to them.'],
 lessons=[
  lesson('Say what you can do',
   'A limit says what you will do or allow. Keep it clear. You can say no. An offer to help for a short time does not promise the whole evening.',
   'A clear boundary describes your own time, belongings or actions. It is different from controlling all of someone else’s choices. “I can stay until six” gives usable information. “You must never ask anyone else” tries to control the other person. A useful limit also leaves room for the other person to decline your offer.',
   'Ari can help Jo with a form until 6:00, but Jo asks Ari to stay until 7:00.',
   ['Ari’s limit is leaving at 6:00. Jo’s request does not change it by itself.',
    'Ari can say: I can help until six. I cannot stay later.',
    'Ari may offer another time if it is wanted and workable. Jo does not have to accept that offer.'],
   'A clear sentence can help, but it cannot guarantee how someone else will respond.'),
  lesson('Keep the limit when the request changes',
   'A new request needs a new choice. You can refuse to share a password even if you agreed to help with a form. If pressure feels unsafe, focus on getting support.',
   'Agreeing to one thing is not permission for everything else. Separate the original offer from the new request. You do not have to keep arguing to make a limit valid. If someone ignores it or the situation feels unsafe, a trusted person or support service can help plan a safer next step; the other person’s behaviour is not your fault.',
   'Jo now asks for Ari’s account password so Jo can keep using the form service later.',
   ['Ari separates helping with the form from giving account access.',
    'Ari can say: I do not share passwords. I can show you where to start your own account.',
    'If Jo keeps pressuring Ari, Ari can stop the exchange when safe and ask a trusted person for help. Ari need not prove the limit by confronting Jo.'],
   'Helping, sharing a device and sharing an account password are different choices.')],
 labs=[[
  with_context(evidence('boundary-limit','Find Ari’s actual offer','Which details describe what Ari has agreed to?',
   ['Help with the form until 6:00.','Leave at 6:00.','Stay until 7:00 because Jo asked.'],[0,1],
   'A request is not an agreement. The offered time ends at six.'),grid=BOUNDARY_CASE),
  evidence('boundary-own-choice','Keep both people’s choices','Which statements respect Ari’s limit and Jo’s ability to choose?',
   ['I can help until six; you can decide whether that works.','If that does not work, you can ask someone else.','You must accept my help and never ask anyone else.'],[0,1],
   'Say what you can offer without taking over the other person’s choices.'),
  task('boundary-words','Try the words','Jo asks Ari to stay until seven. Ari still needs to leave at six. Try a response, then write your own.','conversation',
   'Tap a response to see a possible effect. Then write a short version that keeps Ari’s limit.',
   'Your words are saved for human review. The app does not grade your tone, personality or eye contact.',
   replies=[
    dict(text='I can help until six. I cannot stay later.',outcome='The time limit is clear. Jo may still be disappointed; clarity cannot control the response.'),
    dict(text='Maybe. We will see.',outcome='Jo may think staying later is still an option. If Ari means no, this leaves the plan unclear.'),
    dict(text='You are never allowed to ask anyone else.',outcome='This tries to control Jo’s choices instead of stating Ari’s own limit.')],
   writePrompt='Write Ari’s reply. An alternative is optional; use made-up details.',
   example='I can help until six, but I cannot stay until seven. You can decide if that helps.',
   checks=['I made the time limit clear.','I did not promise an option Ari cannot provide.','I left Jo free to accept or decline.'])],
 [evidence('boundary-change','A password is requested','Which facts still matter after Jo asks for Ari’s password?',
   ['Ari offered help with the form, not account access.','Ari can choose not to share the password.','Earlier help means Jo is now entitled to the account.'],[0,1],
   'Permission is specific. An earlier yes does not cover a different request.'),
  evidence('boundary-pressure','Choose a backup','Jo keeps pushing after a clear refusal. Which are possible next steps for Ari?',
   ['End or pause the exchange when safe.','Ask a trusted person or support service for help.','Keep arguing alone until Jo agrees, regardless of safety.'],[0,1],
   'A boundary does not depend on winning an argument. Prioritise support and safety.'),
  draft_task('boundary-revise',dict(task='Write Ari’s reply.',rework='Revise the reply: Jo now wants Ari’s password and keeps pushing. Keep the password private and add a safe backup step. You do not need to describe any real conflict.',
   example='I do not share passwords. Helping with the form did not include my account. If the pressure continues, Ari can stop the exchange when safe and ask a trusted person for support.',
   checks=['I separated help from account access.','I kept the limit clear without promising a particular reaction.','I added support rather than requiring confrontation.']),True)]],
 practice=[
  q('Lee offers a lift at 5:00. Pat asks for 7:00. What has been agreed so far?','Only the original 5:00 offer; the new request needs a reply.','The lift automatically moved to 7:00.','Lee must now offer every evening.','A new request does not change an existing offer by itself.'),
  q('Which sentence states your own limit?','I can lend the book until Friday.','You cannot read anyone else’s books.','You must agree with everything I say.','A boundary concerns your own offer or participation.'),
  q('You offer a different time. The other person declines. What does that mean?','That alternative does not work for them; it is not an agreement.','They have agreed because you offered it.','You must remove every limit.','An alternative needs both people to agree.'),
  q('You agreed to help with a job search. Now someone asks for your sign-in code. What follows?','You can help without sharing account access.','The first yes gives permission for any later request.','You must disclose the code to be helpful.','Treat the different request as a separate choice.'),
  q('You said no clearly, but the pressure continues. What is an option?','Pause when safe and seek support.','Prove the limit by winning an argument alone.','Assume the pressure is your fault.','You are not responsible for making another person respect a limit.'),
  q('Which statement about a clear boundary is accurate?','It tells the other person your limit, but cannot guarantee their reaction.','It makes everyone agree immediately.','It only counts if you give private details.','Clarity helps communication; it is not control over someone else.')],
 check=[
  q('“I can help today, but I cannot help tomorrow.” What is the limit?','The offer is for today only.','The offer covers the whole week.','The other person cannot ask anybody else.','Read the time and scope of the offer.'),
  q('“I am not lending my phone. I can tell you where the public phone is.” What is being offered?','Information about another option, not the phone.','Full access to the device.','A promise that the public phone is working.','Separate the refused request from the optional alternative.'),
  q('Ari can spare ten minutes and wants to keep the offer clear. Which reply fits?','I can help for ten minutes, then I need to go.','Maybe I can stay as long as you need.','You must stop needing help after ten minutes.','State what Ari can do instead of controlling someone else’s needs.'),
  q('Which sentence tries to control another person rather than state your own limit?','You are not allowed to talk to anyone else.','I will not share my account password.','I need to leave at six.','The first sentence controls another person’s contacts; the others state personal limits.'),
  q('Why is an alternative optional when refusing a favour?','You may not have another workable offer to make.','Every refusal cancels all future friendship.','An invented promise makes the boundary better.','A useful answer can be a clear no without a promise you cannot keep.'),
  q('Pat declines your offered time. Which response respects both choices?','Okay; that time does not work for you, and I cannot do the later one.','You have to accept because I offered.','I will mark the later time agreed even though I cannot attend.','Agreement needs a workable choice for both people.'),
  q('You agreed to explain an app. A friend now wants your account recovery code. Which response fits?','I can explain the app, but I will not share recovery codes.','The earlier yes requires handing over the code.','A recovery code becomes public after one explanation.','Help and account access are separate permissions.'),
  q('Why might someone ask for support instead of repeating a boundary alone?','Pressure or safety concerns can make a different next step needed.','A boundary only exists after a public argument.','Support means they caused the other person’s behaviour.','Seeking help is an option, not a failure to communicate.'),
  q('A conversation starts to feel unsafe. What should guide the next step?','Getting to safety and suitable support, rather than completing an argument.','Finishing the lesson before seeking help.','Staying until the other person admits being wrong.','A practice task should never require unsafe confrontation.'),
  q('Why avoid promising that a perfect script will make someone respect a limit?','You cannot control someone else’s behaviour with a sentence.','Words can never help make a limit clear.','Any upset reaction proves the limit was wrong.','Clear words can help while leaving the outcome uncertain.'),
  q('A learner needs a trusted person but cannot turn to someone at home. What is a possible route?','Seek a suitable trusted person elsewhere or use a support service.','Assume support is only allowed from family.','Post real account details to get attention.','Support can come from outside a household; choose someone who respects safety and boundaries.'),
  q('Why does the app save a written boundary response as a draft?','A person needs to review meaning and fit; a checkbox cannot judge every situation.','The app has contacted the other person.','Every saved sentence is guaranteed to work.','Practice records support human feedback, not automatic judgements about relationships.')],
 reflection='Explain Ari’s revised limit and backup step. Use the fictional case; no personal story is required.'
)

ADJUSTMENTS = dict(
 id='life-adjustments',subject='social',title='Ask for a useful adjustment',
 goal='Describe what gets in the way, request a change and check whether it helps.',
 why='A different way of giving instructions can make a task easier to do. Practise asking clearly without having to disclose a diagnosis here.',
 objectives=['Name the barrier','Ask for a change','Check the result'],needs=['social-1','writing-6'],
 checkSkills=['interpret','apply','reason'],sources=['adjustments','medical-info','rights-help'],help='rights-help',
 practiceNotice='Use Sam’s fictional training task. No diagnosis, medical record or real workplace complaint is needed.',
 nextSteps=['Describe the task, what gets in the way and a change that could help. Ask the teacher, supervisor or responsible service about its process.',
  'Discuss workable options and agree how to review them. An everyday request and a formal accommodation process may involve different steps.',
  'Ask what supporting information is needed and how to share it privately. For a Manitoba human-rights concern, use the Commission’s current contact route. The app cannot decide entitlement or approval.'],
 lessons=[
  lesson('Link the change to the task',
   'Name the job and what gets in the way. Ask for a change that helps with that problem. You can start with a short sentence: Could I have the steps in writing?',
   'A specific request connects the barrier to the task: fast spoken instructions are hard to follow, so written steps may help. An adjustment changes how a person can take part; it does not automatically remove the task’s safety needs. Manitoba’s accommodation guidance describes changes for needs protected by human-rights law. Individual decisions depend on the situation.',
   'Sam must pack an order. Four steps are spoken quickly in a noisy room. Sam follows one written step at a time more easily.',
   ['Name the task: pack the order accurately and safely.',
    'Name the barrier: the spoken steps are too fast to keep track of in this room.',
    'Ask: Could I have a written checklist and a chance to try one order with you?'],
   'A specific request starts a discussion. It does not guarantee that one exact option will be approved.'),
  lesson('Try, review and protect private details',
   'Check whether the change helps with the job. Say what works and what still gets in the way. Ask how any needed private information should be handled. Keep it out of this lesson.',
   'An adjustment can partly help. Compare the result with the goal, then refine the plan. A formal work accommodation request may need relevant supporting information; that is different from handing over a complete medical file. Ask what is needed, why, and who will see it. Human-rights guidance and a responsible person can help with the real process.',
   'Sam gets a checklist, but it uses small print and unexplained short forms. Sam completes the first two steps, then gets stuck.',
   ['The checklist helps Sam keep a place, so keep that useful part.',
    'Ask for readable text, explained words and a demonstration of the unclear step.',
    'Agree to try the revised checklist on one order and review the result. Do not mark the issue solved just because a page was provided.'],
   'You can practise making a request here without stating any diagnosis or proving you deserve support.')],
 labs=[[
  with_context(evidence('adjustment-barrier','Separate the job and barrier','Which two details explain Sam’s request?',
   ['The job is to pack an order accurately and safely.','Fast spoken steps in a noisy room are hard for Sam to follow.','Sam’s favourite colour determines whether support is deserved.'],[0,1],
   'Describe the job and the specific obstacle, without judging the person.'),grid=ADJUSTMENT_CASE),
  evidence('adjustment-fit','Match a change to the barrier','Which requests address the stated difficulty?',
   ['Provide a written checklist for the steps.','Demonstrate one order, with time for questions.','Skip all safety steps to finish faster.'],[0,1],
   'Change how instructions are available while keeping the real task and its safety needs.'),
  task('adjustment-words','Try a request','Sam wants to pack accurately but loses track of the quick spoken steps. Try a request, then write one.','conversation',
   'Tap a response, read its possible effect and connect your request to the barrier.',
   'This is a draft for human review. An app cannot grant an accommodation or grade a person’s support needs.',
   replies=[
    dict(text='Could I have a written checklist and try one order with you?',outcome='This names a concrete change linked to the task. The supervisor may discuss this or another workable option.'),
    dict(text='I need something different.',outcome='This starts a conversation, but the supervisor may need more detail about the barrier and useful change.'),
    dict(text='I will skip the checks from now on.',outcome='This changes the safety of the job without agreement. Ask for a way to follow the checks instead.')],
   writePrompt='Write Sam’s task, barrier and requested change. No real diagnosis is needed.',
   example='I want to pack the order correctly. I lose track of the quick spoken steps. Could I have a written checklist and try one order with you?',
   checks=['I named the task and the barrier.','I asked for a specific change that could help.','I kept safety needs and private information in mind.'])],
 [evidence('adjustment-review','The first change partly helps','Sam can keep a place on the checklist, but small print and unexplained words still cause difficulty. Which facts should the review include?',
   ['The checklist helps Sam keep track of the place.','Text size and unclear words still get in the way.','Receiving any checklist proves the issue is completely solved.'],[0,1],
   'Keep what works and name what still needs changing.'),
  evidence('adjustment-private','Handle a document question','A formal process asks for supporting information. Which are useful next steps?',
   ['Ask what relevant information is needed and why.','Ask for the proper private channel and who will see it.','Upload a complete real medical file into Stepstone.'],[0,1],
   'Relevant supporting information may be needed. Use the responsible service’s process, not a learning draft.'),
  draft_task('adjustment-revise',dict(task='Write Sam’s request.',rework='Revise the request: the checklist helps Sam keep a place, but its small print and unexplained short forms are still a barrier. Ask for a useful change and a way to review it.',
   example='The checklist helps me keep my place. Could we use larger readable text, explain the short forms and walk through the unclear step? I would like to try one order and check how it goes with you.',
   checks=['I kept the part that helps.','I named the remaining barrier and a matching change.','I included a review step without claiming approval.']),True)]],
 practice=[
  q('Instructions are spoken quickly, and a learner loses the order of the steps. Which change fits?','Written steps or one step demonstrated at a time.','A different wall colour with no change to instructions.','Skipping every instruction.','Match the requested change to the actual barrier.'),
  q('What does “barrier” mean in this lesson?','Something that gets in the way of doing the task.','Proof that the person is not trying.','A diagnosis the app has made.','Describe an obstacle rather than label the person.'),
  q('Which request gives useful detail?','Could I have the steps in writing so I can check the order?','Make everything different somehow.','You must know my needs without asking.','A specific change and purpose make the discussion clearer.'),
  q('A checklist helps, but its print is too small. What is a useful review?','Keep the checklist and ask for a readable version.','Call the whole attempt useless without explaining why.','Mark everything solved because paper was provided.','A partial improvement can be refined.'),
  q('Supporting information is requested in a formal process. What can you ask?','What information do you need, why, and how can I provide it privately?','Can I assume all requests for any information are forbidden?','Should I put my complete medical file in a practice answer?','Check the relevant process and protect private records.'),
  q('Someone offers a different change from the one requested. How can it be assessed?','Discuss whether it addresses the barrier and how to review it.','Assume a different option can never help.','Assume any offered option automatically works.','The goal is a workable way to take part, checked against the actual need.')],
 check=[
  q('A learner misses details in a noisy demonstration but follows pictures well. Which detail identifies the barrier?','Important instructions are hard to follow in the noisy setting.','The learner has chosen a nickname.','The learner has not earned enough points.','The obstacle is linked to how instructions are given.'),
  q('A request says, “Could we put the steps on a card so I can check the order?” What change is requested?','A written way to check the sequence.','Permission to ignore every step.','A decision about a diagnosis.','Read the requested format and its purpose.'),
  q('A worker understands a task after seeing it once but not from abbreviations. Which request fits?','Could you demonstrate it and explain these abbreviations?','Could we replace the clock battery instead?','Could I omit the unclear safety step?','Ask for a change linked to the actual difficulty.'),
  q('“I need a different way to get the instructions” is an example of what?','A request to discuss access to the task.','An automatic approval of every possible adjustment.','A medical diagnosis made by the supervisor.','A request begins a conversation; it is not a decision.'),
  q('Why name both the task and the barrier?','It shows what the change needs to help the person do.','It proves one option must always be granted.','It removes the need to listen to a reply.','A task-linked request gives the discussion a concrete purpose.'),
  q('The task includes a safety check. Which approach fits a request for clearer instructions?','Ask for an accessible way to follow the safety check.','Remove the safety check without discussion.','Hide uncertainty and guess the step.','Keep safety needs while changing how the step can be followed.'),
  q('A new checklist helps except for unexplained abbreviations. What is a useful update?','The checklist helps; could we explain these abbreviations and try it again?','Nothing helped in any way.','Everything is solved because a checklist exists.','Report both the improvement and the remaining obstacle.'),
  q('Why agree on a review after trying an adjustment?','You need to see whether it addresses the barrier in practice.','Any written request guarantees success forever.','A review is a test of whether the person deserves help.','Review the fit of the change, not the person’s worth.'),
  q('A formal work process asks for supporting information. What should happen next?','Clarify what relevant information is required and the private way to provide it.','Send the complete medical file to every coworker.','Assume no supporting information can ever be requested.','The process may need relevant information; unrestricted sharing is a different matter.'),
  q('Why should an offer of an alternative be discussed rather than automatically accepted or rejected?','Its usefulness depends on whether it addresses the actual barrier.','An alternative always removes every difficulty.','Only the first wording can ever lead to a helpful change.','Evaluate the proposal against the need and task.'),
  q('Someone is unsure about a Manitoba human-rights accommodation concern. Which route fits?','The Manitoba Human Rights Commission’s current contact information.','A Stepstone score as a legal decision.','An unrelated seller’s support chat.','Use the responsible information service for the real concern.'),
  q('Why does this lesson not ask for a real diagnosis?','The practice is about describing a task, barrier and request using a fictional case.','A person can never need formal supporting information anywhere.','The app already knows everyone’s medical history.','Practice needs fictional reasoning, not private medical records.')],
 reflection='Explain what Sam’s first checklist helped with, what still needs changing and how Sam could review the next version.'
)

MODULES = [APPOINTMENT, FIND_HELP, BOUNDARIES, ADJUSTMENTS]
for module in MODULES:
    first = module.get('checkSkills', ['calculate','apply','reason'])[0]
    # Three first-skill, five application and four reasoning cases. At least
    # one of any two reasoning cases is from lesson two; all first-skill cases
    # are from lesson one, so every six-question draw covers both ideas.
    skills = [first,first,'apply',first,'reason','apply',
              'apply','reason','apply','reason','apply','reason']
    assert len(module['check']) == len(skills)
    for question,skill in zip(module['check'],skills):
        question['skill'] = skill
    if 'checkSkills' in module:
        for question in module['practice']:
            question['skill'] = 'apply'

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)
