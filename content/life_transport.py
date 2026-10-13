"""Transport practice: fictional trips, current Manitoba information routes.

No live trip, booking, location collection, licence application or driving
certification. Tables and sign illustrations reuse the shared mission tasks.
"""
from digital import lesson, q
from life_services import attach_guides, calculation, evidence, number, table, with_context
from practical_missions import draft_task

CHECKED = '2026-09-24'
CITY = 'https://www.winnipeg.ca/services-programs/transportation-roads-parking/transit/'
SOURCES = {
 'planner': ('Winnipeg Transit — plan a real trip with Navigo', 'https://www.winnipegtransit.com/navigo'),
 'fares': ('Winnipeg — current fares, youth passes and WINNpass', CITY+'fares'),
 'transfers': ('Winnipeg Transit — peggo payments and transfers', 'https://info.winnipegtransit.com/en/fares/say-hello-to-peggo/changes-to-fares'),
 'transit-help': ('Winnipeg Transit — 311, Telebus and service help', CITY+'contact-winnipeg-transit'),
 'training': ('Winnipeg — free travel training and printed maps', CITY+'riding-transit/travel-training-resources'),
 'licence': ('MPI — Class 5 licence steps and restrictions', 'https://www.mpi.mb.ca/get-a-passenger-vehicle-class-5-licence/'),
 'stages': ('MPI — graduated licensing stages', 'https://www.mpi.mb.ca/graduated-driver-licensing/'),
 'testing': ('MPI — tests, preparation and access options', 'https://www.mpi.mb.ca/testing-for-your-class-5-licence/'),
 'id': ('MPI — accepted identity documents', 'https://www.mpi.mb.ca/establishing-your-identity/'),
 'fees': ('MPI — current licensing and testing fees', 'https://www.mpi.mb.ca/licensing-fees-and-other-charges/'),
 'mpi-help': ('MPI — ask about a missing requirement or support', 'https://www.mpi.mb.ca/contact-us/'),
 'handbook': ('MPI — complete Driver’s Handbook', 'https://apps.mpi.mb.ca/comms/drivershandbook/'),
 'shapes': ('MPI handbook — sign shapes and the 24-hour clock', 'https://apps.mpi.mb.ca/comms/drivershandbook/signs-shapes-colors.html'),
 'rules': ('MPI handbook — regulatory signs and posted conditions', 'https://apps.mpi.mb.ca/comms/drivershandbook/regulatory-signs.html'),
 'crossing': ('MPI handbook — crosswalks and pedestrian signals', 'https://apps.mpi.mb.ca/comms/drivershandbook/crosswalks.html'),
 'quiz': ('MPI — driving practice quizzes', 'https://apps.mpi.mb.ca/DriverQuiz/'),
}

OUTBOUND = table('Fictional weekday buses — east to Library', ['Bus','Leaves','At Library'],
 [['A','8:10 am','8:40 am'],['B','8:25 am','8:55 am'],['C','8:40 am','9:10 am']])
EARLIER = table('Fictional options for the changed appointment', ['Bus','Leaves','At Library'],
 [['Early','7:50 am','8:20 am'],['A','8:10 am','8:40 am']])

BUS = dict(
 id='life-bus-trip',title='Plan a bus trip',minutes=30,
 goal='Choose a bus that gets you to the actual destination on time, with a way home.',
 why='A trip is more than the time spent on the bus. See the walking, waiting and fare together.',
 objectives=['Read the timetable','Count the whole trip','Make a workable plan'],
 needs=['reading-1','math-cash','math-budget'],
 sources=['planner','fares','training','transit-help'],help='training',
 practiceNotice='All stops, buses, times and prices in the tasks are made up. Use the official planner for a real trip.',
 nextSteps=['In Navigo, set your starting place, destination, travel date and arrival target. Check the direction, stop, walking parts, connections and current service changes. Use your own walking needs, not a rushed estimate.',
  'Check the current fare and payment method for your situation. Ask about youth-pass or WINNpass eligibility if useful; do not assume a discount applies. Plan the return trip and what to do if the first plan fails.',
  'Save a private copy of the route and useful contact details. Winnipeg offers free travel training and printed maps. Ask 311 about help if needed. Outside Winnipeg, use the local operator’s planner and rules.'],
 lessons=[
  lesson('Arrive at the door, not just the stop',
   'A timetable lists when buses leave or arrive. Read one row at a time. Check the day and direction. Add the walk from the last stop to the place you need. Leave some spare time.',
   'Leaving later is useful only if the whole trip still fits. Count walking and waiting as well as riding. A route number alone does not tell you the direction. Real schedules can change, so the practice table cannot replace a current trip plan. You can choose more walking time or ask for support.',
   'Fictional plan: Kim needs to reach an office by 9 am. The walk from Library stop takes 8 minutes. Bus A arrives at 8:40; B at 8:55; C at 9:10.',
   ['A reaches the office at 8:48 am after the walk. That leaves 12 minutes before 9 am.',
    'B reaches it at 9:03 am. Reaching the bus stop before 9 does not make the full trip on time.',
    'Choose A from these options. If walking to its departure stop takes 7 minutes and Kim wants 5 minutes spare, allow $7+5=12$ minutes before its 8:10 departure: leave at 7:58 am.'],
   'A scheduled arrival is an estimate, not a promise. Include a margin and check current information.'),
  lesson('Replan when the appointment moves',
   'CAD means Canadian dollars. Budget for getting home too. Check which fare or pass fits you. If the appointment changes, compare the whole trip again. A plan that worked yesterday may not work today.',
   'Use the same destination and walking time when comparing buses. Keep the fare calculation separate from real eligibility: the price in a maths task is not a current fare quote. Winnipeg’s fare page includes youth-pass and lower-income options with conditions. Having a phone does not mean having data or enough battery; keep a usable backup.',
   'Kim’s appointment moves to 8:45 am. A new fictional option reaches Library at 8:20. Kim has CAD 8; the made-up fare is CAD 3 each way, with no pass or valid return transfer in this case.',
   ['The earlier option reaches the office at 8:28 am. Bus A still reaches it at 8:48, three minutes too late.',
    'Two separate fares cost $3+3=6$ CAD. From 8 CAD, $8-6=2$ CAD remains.',
    'Revise the departure time, check a return option and save the route privately. For a real journey, check current fares, access needs and service changes.'],
   'Do not spend the return fare just because the first bus has been paid for.')],
 labs=[[
  with_context(evidence('bus-table','Read the arrival column','Kim must be at the office by 9 am. The walk from Library takes 8 minutes. Which statements fit this table?',
   ['Bus A leaves enough time for the walk.','Bus B reaches the stop before 9 but reaches the office after 9.','Bus C gets Kim to the office by 9.'],[0,1],'Add the walk: A reaches the office at 8:48; B at 9:03; C at 9:18.'),grid=OUTBOUND),
  with_context(calculation('bus-margin','Count the spare minutes','Bus A arrives at Library at 8:40 am. An 8-minute walk reaches the office at 8:48. How many minutes remain before 9 am?',12,'From 8:48 to 9:00 is 12 minutes.'),grid=OUTBOUND),
  draft_task('bus-plan',dict(title='Write Kim’s trip plan',task='Plan Kim’s fictional 9 am appointment using Bus A. Include leaving for the stop, the bus direction, the walk after arrival and one return-trip detail to check.',
   example='Kim can leave at 7:58 am, walk 7 minutes and allow 5 minutes before Bus A at 8:10. Take the eastbound bus to Library, arrive at 8:40 and walk 8 minutes to the office. Check the return timetable and keep enough fare to get home.',
   checks=['I included the right day, direction and bus.','I included walking and spare time, not just the ride.','I included a return-trip question.']))],
 [with_context(evidence('bus-earlier','The appointment moved','The appointment is now 8:45 am. The walk is still 8 minutes. Which details change the choice?',
   ['The Early bus reaches the office at 8:28 am.','Bus A would reach the office three minutes late.','The later deadline means every bus now works.'],[0,1],'The new deadline is earlier. Recalculate door-to-door arrival.'),grid=EARLIER),
  calculation('bus-budget','Keep the fare home','Only for this made-up case: CAD 8 available, CAD 3 out and CAD 3 back. How much remains after both fares, in CAD?',2,'$8-3-3=2$ CAD. Real fare and pass conditions must be checked separately.'),
  draft_task('bus-revise',dict(task='Write Kim’s trip plan.',rework='Update for the 8:45 am appointment and Early bus leaving at 7:50. Allow the same 7-minute walk and 5-minute spare time before boarding. Include the two-fare budget and a backup without mobile data.',
   example='Kim will leave at 7:38 am for the 7:50 Early bus, arrive at Library at 8:20 and reach the office at 8:28. The two fictional fares use 6 of the 8 CAD. Kim will save or write the return plan and contact details before leaving, then check current information if the plan changes.',
   checks=['I changed departure and arrival for the new appointment.','I reserved the return fare using the fictional prices.','I included a usable backup without assuming mobile data.']),True)]],
 practice=[
  number('A bus arrives at 10:20 am. A 10-minute walk reaches the appointment at 10:30. It starts at 10:45. How many spare minutes remain?',15,'From 10:30 to 10:45 is 15 minutes.'),
  q('The timetable is for weekdays, but the trip is on Sunday. What should be checked?','The Sunday service for that route and direction.','Only the colour of the bus.','Nothing: every day has identical service.','Read the date and day as well as the time.'),
  q('An eastbound bus and westbound bus have the same route number. What else matters?','The destination direction and the correct stop.','Only the route number.','Whichever bus is nearest, regardless of direction.','A number alone is not the whole trip.'),
  number('A made-up journey needs two separate fares of CAD 4. The rider has CAD 10. How much remains after both fares?',2,'$10-4-4=2$ CAD.'),
  q('An appointment moves earlier. Which part should be recalculated?','Departure, arrival and walking time for the new deadline.','Only the app nickname.','Nothing if the route number stays the same.','A changed deadline can change which trip fits.'),
  q('A rider needs more support to learn buses. Which Winnipeg service is relevant?','Free travel training, with a request through the official contact route.','A requirement to pass every Stepstone quiz first.','A promise that every person must travel alone.','Training and support can be part of a workable travel plan.')],
 check=[
  number('A fictional bus reaches the stop at 2:35 pm. The final walk takes 10 minutes. The appointment is at 3 pm. How many spare minutes remain?',15,'Arrival at the door is 2:45 pm, leaving 15 minutes.'),
  number('A walk to a stop takes 9 minutes. The plan adds 6 minutes spare. How many minutes before the bus should the person leave?',15,'$9+6=15$ minutes.'),
  q('The trip result is for tomorrow, but the rider needs to go today. What should change?','Set the correct travel date and check the resulting trips.','Keep it because the place is the same.','Assume the day cannot affect service.','The travel date belongs to the route plan.'),
  number('A bus arrives at 11:50 am and the door is 15 minutes away. The appointment is at noon. How many minutes late would arrival be?',5,'Ten minutes reaches noon; five more reaches 12:05 pm.'),
  q('Why count the walk after leaving the bus?','The bus stop may not be the actual destination.','Walking time never affects arrival.','It automatically changes the fare.','Compare arrival at the door with the deadline.'),
  q('Two buses have the same number. Which detail helps choose the right one?','The direction and destination shown, matched to the trip plan.','The first bus seen, without checking.','The driver’s clothing.','Check the trip, stop and direction together.'),
  q('The final walk is longer than expected. What should be revised?','The door-arrival estimate and, if needed, the chosen departure.','Only the bus number on an old screenshot.','The appointment time without telling anyone.','Use the new walking time in the full trip.'),
  q('Why budget the return before leaving?','Getting there uses only one part of the travel money.','Return travel is always free everywhere.','An app score pays the fare.','Check the return route and payment needs as part of the same plan.'),
  q('A rider has limited mobile data. What preparation helps?','Keep a private saved or written route and a way to ask for updates.','Assume an old screenshot becomes live information.','Share their home address publicly.','A saved copy is a backup, and changes still need checking.'),
  q('A fare discount is mentioned online. Why check its conditions?','It may depend on age, school status, income or other requirements.','Every offer applies automatically to everyone.','A low price cannot have conditions.','Use the current operator’s rules for the actual situation.'),
  q('These practice buses are made up. What is needed for a real journey?','The actual operator’s current plan, fares and access information.','Only the table from this lesson.','A printed Stepstone score instead of payment.','The lesson teaches a method, not a live route.'),
  q('Why might someone choose an earlier bus even when two seem to fit?','It may give a useful margin for their walking or connection needs.','Everyone must always choose the earliest bus all day.','Earlier buses are guaranteed never to be delayed.','Compare workable margins without treating any timetable as a guarantee.')],
 reflection='Using Kim’s fictional case, explain the revised bus choice, the whole arrival time and how to keep a way home.'
)

CONNECT = table('Fictional connection — first bus reaches Hub at 9:12 am', ['Next bus','Leaves Hub','At Centre'],
 [['Tight','9:18 am','9:38 am'],['Later','9:30 am','9:50 am']])
DELAY = table('Fictional update — first bus now reaches Hub at 9:26 am', ['Option','Leaves Hub','At Centre'],
 [['Tight','9:18 am','9:38 am'],['Later','9:30 am','9:50 am'],['Next','9:45 am','10:05 am']])

CHANGE = dict(
 id='life-trip-change',title='Handle a missed connection',minutes=30,
 goal='Recheck the time and fare, then send a clear update when a journey changes.',
 why='Missing a bus is a problem to solve, not a reason to panic or take an unsafe shortcut.',
 objectives=['Allow connection time','Recheck the options','Update the plan'],
 needs=['life-bus-trip','writing-1','social-7'],
 sources=['planner','transfers','fares','transit-help','training'],help='transit-help',
 practiceNotice='Use the fictional trip and transfer times. This app does not track buses or contact anyone.',
 nextSteps=['Move to a safe place to read updates. Check the stop, direction and current trip options. Include the time needed to reach a different stop. Do not run into traffic to catch a bus.',
  'Recheck the arrival estimate, return trip and any transfer expiry or extra fare. Ask the operator or official contact if the payment rule is unclear. Winnipeg lists 311 and Telebus as alternatives for information.',
  'Tell the person expecting you what changed, your best current estimate and what you need to confirm. If there is no workable trip, ask about another arrangement. You do not need an app score to get help.'],
 lessons=[
  lesson('A connection needs time between buses',
   'A connection means changing buses. You may need to walk to another stop. Count that walk before counting spare minutes. A short gap can disappear if the first bus is late.',
   'Separate three times: first arrival, reaching the next stop, and the next departure. This prevents counting the same minutes twice. A transfer is also a fare rule, not a promise that the bus will wait. Winnipeg’s current guidance gives transfers a time limit; check the actual expiry and payment method.',
   'Fictional case: Max reaches Hub at 9:12 am and needs 4 minutes to reach the next stop. The Tight bus leaves at 9:18; Later leaves at 9:30. After Centre, Max needs a 5-minute walk for a 10 am appointment.',
   ['Max reaches the next stop at 9:16 am. The Tight bus leaves just 2 minutes later.',
    'Later leaves 14 minutes after Max reaches that stop. It gets to Centre at 9:50; the final walk reaches the appointment at 9:55.',
    'Later offers a larger connection margin and still fits this appointment. Check real conditions before choosing; a margin cannot prevent every delay.'],
   'The gap between bus times is not all waiting time if you must walk between stops.'),
  lesson('Say what changed and what you know',
   'Pause in a safe place. Recheck the trip from where you are now. A saved timetable is useful, but it may be out of date. Keep an estimate separate from a confirmed fact.',
   'If the connection no longer works, compare the next safe option with the appointment and return needs. A clear update says what happened, the new estimated arrival and a question. Transfer expiry may also change the cost. A missed connection does not guarantee a free extra ride; use official information or ask.',
   'The first bus is delayed to 9:26 am. The 4-minute walk now ends at 9:30, exactly when Later is due to leave. Next leaves at 9:45 and gets to Centre at 10:05.',
   ['Do not count a zero-minute margin as a reliable connection or run into traffic. Recheck live information and the next workable option.',
    'Next plus the 5-minute walk gives 10:10 am, an estimated 10 minutes late. Ask whether the appointment can still go ahead.',
    'In this made-up case, the printed transfer ends at 9:40. Boarding at 9:45 would be 5 minutes later. Check the payment needed and keep the return plan workable.'],
   'A saved message in Stepstone has not been sent. Use a real agreed contact method when travelling.')],
 labs=[[
  with_context(calculation('connection-gap','Count the usable gap','The first bus arrives at 9:12 am. Walking to the next stop takes 4 minutes. How many minutes remain before Tight leaves at 9:18?',2,'The walk ends at 9:16, leaving 2 minutes before 9:18.'),grid=CONNECT),
  with_context(evidence('connection-choice','Compare the full options','Max needs a 5-minute walk after Centre for a 10 am appointment. Which statements fit?',
   ['Later gives a larger connection margin than Tight.','Later reaches the appointment at 9:55 am after the walk.','All 6 minutes from 9:12 to 9:18 are free waiting time.'],[0,1],'Subtract the connection walk, then add the destination walk.'),grid=CONNECT),
  draft_task('connection-plan',dict(title='Write the connection plan',task='Write Max’s fictional plan using Later. Include the Hub walk, the departure, arrival at the actual appointment and one detail to recheck if the first bus is late.',
   example='Max expects to reach Hub at 9:12, walk 4 minutes and catch Later at 9:30. It reaches Centre at 9:50, then a 5-minute walk reaches the appointment at 9:55. If the first bus is late, Max will recheck the connection and transfer expiry.',
   checks=['I allowed the walk between stops.','I included the final walk and the actual appointment arrival.','I named a detail to recheck if the trip changes.']))],
 [with_context(calculation('connection-delay','Find the new arrival difference','The updated Next bus reaches Centre at 10:05 am. The final walk is 5 minutes. How many minutes after the 10 am appointment would Max arrive?',10,'The walk ends at 10:10, which is 10 minutes after the appointment.'),grid=DELAY),
  evidence('connection-fare','Check the remaining problems','The next workable bus leaves at 9:45. The fictional transfer ends at 9:40, and the appointment is now likely to be missed. Which actions fit?',
   ['Check whether another fare is needed and keep money or a plan for the return.','Send a clear arrival estimate and ask whether to come or rearrange.','Assume the bus, fare and appointment must all wait.'],[0,1],'A changed trip can affect time, payment and the person expecting you.'),
  draft_task('connection-revise',dict(task='Write the connection plan.',rework='Turn the plan into a short update for the appointment. Include the delay, the estimated 10:10 arrival and a question. Add a separate note about the transfer and a safe next step.',
   example='Hello, my first bus was delayed and I may miss the connection. The next workable trip would get me to you around 10:10. Can I still attend, or should we rearrange? My travel note: check the transfer/payment and return route from a safe place, using current information or official help.',
   checks=['I described the change and labelled the arrival as an estimate.','I asked the person expecting me what should happen next.','I checked fare and return needs without an unsafe shortcut.']),True)]],
 practice=[
  number('A bus reaches Hub at 1:10 pm. The next stop is 5 minutes away on foot. The connection leaves at 1:20. How many spare minutes remain?',5,'Reach the stop at 1:15; there are 5 minutes before departure.'),
  q('A connection has only one spare minute after walking. What does that mean?','A small delay may make it unworkable; compare another option.','The bus is required to wait.','Running across traffic makes it guaranteed.','Use a margin that fits the trip and your needs.'),
  q('What are different meanings of “connection” and “transfer” here?','A connection is the change of bus; the fare transfer has payment conditions.','Both guarantee the next driver will wait.','Both remove all walking time.','The trip timing and fare validity are separate checks.'),
  number('A fictional transfer expires at 2:15 pm. Boarding is at 2:23. How many minutes after expiry is that?',8,'From 2:15 to 2:23 is 8 minutes. Check the payment needed.'),
  q('The earliest workable arrival is after the appointment. Which message helps?','Give the new estimate and ask whether to attend or rearrange.','Claim to be on time when you are not.','Send only an unrelated emoji.','Share the useful change and request a decision.'),
  q('The phone has no data, but can make calls. Which official route can help in Winnipeg?','The listed 311 or Telebus information route.','A promise that old screenshots update themselves.','Only a paid app subscription.','Prepare the contact details before travel; use official information.')],
 check=[
  number('A bus arrives at 3:05 pm. The next stop needs a 6-minute walk. The connection leaves at 3:18. How many spare minutes remain?',7,'Reach it at 3:11; 7 minutes remain.'),
  number('A bus reaches the final stop at 4:20 pm. Walking takes 7 minutes. The appointment is at 4:40. How many spare minutes remain?',13,'Arrival is 4:27, leaving 13 minutes.'),
  q('A transfer ticket is valid, but the connecting bus has already left. What is true?','Fare validity does not make that bus available; replan the journey.','The ticket brings the bus back.','No new timetable check is needed.','Payment and vehicle timing are different issues.'),
  number('The gap between two buses is 12 minutes. Walking between their stops takes 8 minutes. How much spare time remains?',4,'$12-8=4$ minutes.'),
  q('Why allow walking time when choosing a connection?','You cannot use all the gap as waiting time at the next stop.','Stop locations never matter.','The fare automatically pays for more minutes.','Compare departure with the time you can actually reach that stop.'),
  q('Which detail should be checked before boarding a replacement bus?','Its destination and direction in the revised plan.','Only whether other people are boarding.','Whether the old route had the same colour.','A replacement must fit the journey you now need.'),
  q('A delay removes all connection margin. What is a sensible next step?','Recheck current options from a safe place.','Run into the road without checking traffic.','Assume the old plan is guaranteed.','Choose a workable plan rather than forcing an unsafe connection.'),
  q('Why call a revised arrival time an estimate?','Traffic and service changes can still affect it.','It means there is no need to tell anyone.','The appointment automatically moves.','Be clear about what is known and what may change.'),
  q('The next bus would be after the transfer expiry. Which question matters?','What payment is needed for this ride, and can the return still work?','Can a quiz score change the expiry?','Should the expiry label be ignored?','Check the actual operator’s fare conditions.'),
  q('Why keep the return journey in a changed plan?','A new route or extra fare can affect getting home.','Return service always runs all night.','The trip ends as soon as the first destination is reached.','A useful plan includes the way back.'),
  q('There is no workable bus for the appointment. What can the message request?','A later time, another arrangement or help choosing the next step.','A guarantee that an impossible trip will happen.','A false claim that the rider has already arrived.','Ask for a practical change rather than inventing certainty.'),
  q('Why is a saved route only a backup?','It may not include current delays, detours or service changes.','Saving it makes it live forever.','Paper and saved routes cannot ever be useful.','Keep the useful details and know how to check for updates.')],
 reflection='Using Max’s fictional trip, explain the changed arrival, the fare question and the message the other person needs.'
)

STEPS = table('First-licence planning — confirm requirements with MPI', ['Step','What to prepare'],
 [['Register','Accepted ID; applicable age and consent requirements'],['Prepare','Handbook study; current fees and test arrangements'],['Test','Knowledge test; required vision and medical standards'],['Practise','Issued learner licence; qualified supervision and all restrictions']])

LICENCE = dict(
 id='life-driver-plan',title='Plan your driver’s licence',minutes=30,
 goal='Map the first-licence steps and make a realistic plan for study, costs and supervised practice.',
 why='Driving takes more than passing a quiz. Separate the documents, learning, tests and practice.',
 objectives=['Find the correct steps','Prepare time and money','Check a changed plan'],
 needs=['life-photo-id','math-budget','life-bus-trip'],
 sources=['licence','stages','testing','id','fees','handbook','mpi-help'],help='mpi-help',
 practiceNotice='This is a planning guide for a first Manitoba Class 5 licence. It is not the full handbook, driver training or an official test.',
 nextSteps=['Check MPI’s Class 5 route for your situation, age and any required consent. Register with accepted identification before booking. Ask MPI about missing documents, unavailable required support or access needs; do not invent a signature.',
  'Read the full Driver’s Handbook. Use official practice quizzes and ask about test audio or other access options. Check current testing, licence and premium costs, plus travel or lessons. Keep documents and health information out of Stepstone.',
  'After a licence is issued, follow all stage restrictions. Arrange lawful supervised practice in a suitable insured vehicle, then the road test when eligible and ready. Check ongoing stage requirements. If a car or qualified supervisor is unavailable, ask about permitted driving schools and keep another travel plan.'],
 lessons=[
  lesson('Build the plan before booking',
   'MPI means Manitoba Public Insurance. A Class 5 licence is the usual passenger-vehicle licence. CAD means Canadian dollars. Start with the official route, documents and study plan. Passing Stepstone does not give permission to drive.',
   'A first Manitoba licence normally starts at 16; the age-15-and-a-half route needs an eligible Driver Z course in progress. Under-18 applicants need the required consent. Registration, knowledge testing, vision and medical standards, and licence issue are separate steps. MPI offers knowledge-test audio; ask about other access needs before booking. A missing requirement is a question to resolve, not something to fake.',
   'Fictional Noor is 17 and planning the first steps. The savings goal for now is CAD 90, with CAD 68 saved. This is a made-up goal, not a quote for a licence or its total cost.',
   ['Use MPI’s route to list ID, consent and testing questions. Keep real documents private.',
    'The savings gap is $90-68=22$ CAD. Check actual fees and other costs before treating the goal as enough.',
    'Plan short handbook study sessions. Four sessions of 15 minutes give $4\\times15=60$ minutes. Study time helps learning but does not certify readiness.'],
   'The knowledge test, road test, licence and any lessons can have separate costs. Check the current full plan.'),
  lesson('Practice needs the right support',
   'New drivers move through Learner, Intermediate and Full stages. Each has rules. A friend willing to sit beside you is not automatically a qualified supervising driver. Check the whole arrangement before driving.',
   'The Learner stage has a nine-month minimum; passing the road test leads to an Intermediate stage with a fifteen-month minimum. Licence validity and other conditions matter. Learners need a qualified supervisor: a valid minimum Class 5 Full licence held for at least three years, the only front-seat passenger, and compliance with MPI’s alcohol and drug rules. Learner alcohol and drug restrictions also apply. Read the complete current rules.',
   'Noor later has a Learner licence. A cousin offers to supervise but has held a Full licence for only two years. Noor still needs transport to work.',
   ['Check the supervisor requirements. This cousin does not meet the three-year Full-stage requirement, even if Noor feels confident.',
    'Look for a qualified arrangement or ask about permitted driving-school options. Do not drive alone to practise.',
    'Revise the plan: keep studying and use a workable bus or other travel option meanwhile. Completing minimum time does not replace the required test or prove practical skill.'],
   'A practice score does not change licence restrictions or authorize a vehicle, supervisor or road test.')],
 labs=[[
  with_context(evidence('licence-steps','Separate the steps','Noor is 17 and planning a first licence. Which items need checking before treating the plan as ready?',
   ['Accepted ID, required consent and registration arrangements.','Current fees, test access and handbook preparation.','Whether a Stepstone score automatically issues a licence.'],[0,1],'Prepare the real requirements and use the official process.'),grid=STEPS),
  calculation('licence-budget','Find the savings gap','Noor’s made-up savings goal for the first steps is CAD 90. Noor has CAD 68. How much more is needed for that goal, in CAD?',22,'$90-68=22$ CAD. This is only the fictional savings goal; actual costs need checking.'),
  draft_task('licence-plan',dict(title='Make Noor’s preparation plan',task='Write a fictional plan with one document or consent question, a handbook study plan and a cost or test-access question. Keep it separate from permission to drive.',
   example='Noor will ask MPI which ID and consent arrangements are required, plan four 15-minute handbook sessions and check current fees. Noor will ask about audio or other test access if useful. The 90 CAD savings goal is provisional; this plan does not give permission to drive.',
   checks=['I named requirements to confirm through MPI.','I included study and a cost or access question.','I kept private details out and did not claim a licence was issued.']))],
 [evidence('licence-supervisor','Check the offered help','Noor now holds a Learner licence. The willing cousin has had a Full licence for two years. Which statements follow?',
   ['The cousin does not yet meet the stated three-year Full-stage requirement.','Noor should find a qualified arrangement and check the other restrictions.','Confidence makes the supervisor’s licence history irrelevant.'],[0,1],'Willingness and the required qualifications are different checks.'),
  calculation('licence-study','Keep a useful study plan','While arranging qualified support, Noor studies for 15 minutes on each of four days. How many study minutes is that?',60,'$4\\times15=60$ minutes. Minutes studied are not a licence qualification.'),
  draft_task('licence-revise',dict(task='Make Noor’s preparation plan.',rework='Revise for the unqualified cousin. Explain what arrangement still needs finding, what can continue now and how Noor can travel to work in the meantime.',
   example='The cousin has only two Full-stage years, so Noor needs a different qualified supervising arrangement and must check the remaining rules. Noor can keep studying and ask MPI about permitted driving-school options. A checked bus plan can cover work travel meanwhile; Noor must not practise alone.',
   checks=['I identified the supervisor requirement that is not met.','I proposed a lawful next step without claiming a guaranteed arrangement.','I kept study and work travel possible while resolving the gap.']),True)]],
 practice=[
  number('A fictional first-step savings goal is CAD 100. There is CAD 75 saved. What is the gap in CAD?',25,'$100-75=25$ CAD. Check real costs separately.'),
  q('A person needs audio or another test-access option. What is a useful preparation step?','Check MPI’s options and ask before the test appointment.','Assume every device can be used during the real test.','Put medical records into Stepstone.','Use the actual testing service for arrangements.'),
  q('A required consent or identity document is unavailable. What should the applicant do?','Ask MPI about accepted arrangements for the situation.','Invent a signature or alter an image.','Treat app completion as a substitute.','Resolve the requirement through the service.'),
  q('A willing friend does not meet the supervisor requirements. What should change?','Find a qualified arrangement before learner driving.','Treat willingness as enough.','Practise alone until the friend qualifies.','The whole supervised-practice arrangement must fit the rules.'),
  q('A new driver passes the official road test from Learner stage. What should they check next?','The Intermediate-stage restrictions and ongoing requirements.','A claim that every restriction disappears immediately.','Only the app rewards total.','Passing a test changes the stage; it does not erase every rule.'),
  q('A learner cannot currently access a suitable car or supervisor. What can continue?','Handbook study, asking about training options and another travel plan.','Unsupervised road practice.','Pretending a car has been insured.','Keep useful preparation moving without inventing permission.')],
 check=[
  number('A made-up preparation savings goal is CAD 120 with CAD 85 saved. How much remains to reach that goal, in CAD?',35,'$120-85=35$ CAD; the actual cost still needs checking.'),
  number('A study plan has three sessions of 20 minutes. How many minutes are planned?',60,'$3\\times20=60$ minutes of study.'),
  q('Before booking a first knowledge test, which service step matters?','Register with MPI using accepted identification and check applicable requirements.','Submit an app score as a licence.','Assume an appointment verifies every document automatically.','Prepare through the actual service.'),
  number('A fictional preparation budget allows CAD 18 for travel and CAD 12 for learning materials. What is that subtotal in CAD?',30,'$18+12=30$ CAD. It excludes any other costs, including real test and licence fees.'),
  q('Why compare current fees with a personal savings goal?','A made-up goal may not cover the actual required costs.','Any round number is the official price.','A high score removes every fee.','An estimate and the actual cost are different things.'),
  q('What material should form the main knowledge-test study source?','MPI’s complete current Driver’s Handbook.','Only a six-question Stepstone check.','A claim that memorising one sign covers the road rules.','Use the full official material and check preparation options.'),
  q('A proposed supervisor has held a Full licence for two years. Which plan fits this lesson?','Find someone who meets the full supervisor requirements before learner driving.','Treat any Full licence as enough to supervise immediately.','Drive alone while waiting.','The minimum licence-history requirement is one part of qualification.'),
  q('Why does minimum stage time not guarantee readiness for the road test?','Eligibility conditions and actual driving skill still need to be met.','Time alone replaces every test.','Only a Stepstone score matters.','Check the official route and prepare practical skills with qualified support.'),
  q('A person has a Learner licence and feels confident. Which rule still matters?','The required supervising arrangement and all current licence restrictions.','Only the restrictions they personally prefer.','No restrictions once confidence improves.','Confidence does not change licence conditions.'),
  q('Why keep a bus or other travel plan while arranging practice?','Transport needs continue even when driving arrangements are not ready.','Planning another trip cancels a licence application.','A car appears automatically after a quiz.','Separate today’s transport need from the longer learning goal.'),
  q('The learner cannot meet a requirement yet. Which action is useful?','Ask MPI about options and keep the unresolved item visible in the plan.','Claim that an app mentor approved it instead.','Hide the missing requirement.','An accurate plan names what is still unresolved.'),
  q('Why does a Stepstone pass not count as an MPI test pass?','Different assessments serve different purposes; this app issues no licence result.','Every online quiz has the same authority.','Points are equivalent to a driving licence.','Practice supports preparation but does not replace official testing.')],
 reflection='Using Noor’s fictional case, explain the preparation goal, the support gap and a useful plan while it is unresolved.'
)

CLOCK = table('Reading a 24-hour clock', ['Time shown','Everyday time'],
 [['07:00','7 am'],['12:00','Noon'],['13:00','1 pm'],['17:30','5:30 pm']])
RESTRICTION = table('Fictional practice sign — read all three lines', ['Part','What is posted'],
 [['Action','No right turn'],['Days','Monday to Friday'],['Times','07:00–09:00']])

SIGNS = dict(
 id='life-road-signs',title='Read road signs',minutes=25,
 goal='Connect a sign to its meaning, then check the time, conditions and people around it.',
 why='Reading a shape or number is the start. Understanding when the instruction applies is the useful part.',
 objectives=['Read the sign','Use the conditions','Explain the next step'],
 needs=['reading-1','math-3','life-driver-plan'],
 sources=['shapes','rules','crossing','handbook','quiz'],help='quiz',
 practiceNotice='These are a few study examples, not the whole driving course or an MPI test. Use the full handbook and qualified instruction.',
 nextSteps=['Study the full handbook’s signs, signals and road-user chapters. Name what a sign requires before explaining a scenario. Use the official practice quizzes to find topics to revisit.',
  'Read any day, time, direction and exception along with the main sign. Check unfamiliar wording in the handbook. Do not assume a sign outside its time window gives blanket permission.',
  'Practise applying the rules only within a lawful supervised or otherwise permitted driving arrangement. Study in a safe place; never operate this app while driving.'],
 lessons=[
  lesson('Read the shape and the details',
   'A red eight-sided STOP sign requires a complete stop. A downward-pointing yield triangle means give way: slow down and stop if needed. Some signs also use days and times. Read those details as part of the message.',
   'Shape helps recognition, but one feature is not the whole rule. A 24-hour clock numbers the hours from midnight. Before noon the hour matches am time. For 13 through 23, subtract 12 to get the pm hour. Keep the minutes. Noon is 12:00; midnight is 00:00. Connect the sign to the handbook rule, not just a colour.',
   'Study example: compare a STOP sign with a yield sign, then read a separate posted time of 17:30.',
   ['Name the difference: STOP requires stopping; yield requires giving way, with a stop when needed.',
    'For 17:30, $17-12=5$, so the time is 5:30 pm. The 30 minutes stay the same.',
    'Find the full sign or rule in the handbook. A single recognised shape does not mean every driving situation is understood.'],
   'Yield does not mean “keep moving no matter what.” Colour alone is not a complete instruction.'),
  lesson('A condition changes when a rule applies',
   'A condition is a detail that must be true. A sign may name an action, days and times. Read them together. People crossing, traffic signals and other rules still matter even when one posted restriction is not active.',
   'Think through the whole message instead of stopping at one number. A weekday-only time window needs both the correct day and time. Outside that window, only that timed restriction stops applying; other rules can still prevent the action. At a pedestrian signal, an orange hand means do not begin crossing. Watch for turning traffic and use the actual crossing instructions.',
   'Fictional study sign: no right turn, Monday to Friday, 07:00 to 09:00. First case: Tuesday at 8:20 am. Changed case: Saturday at 8:20 am.',
   ['Tuesday is a named day and 8:20 is inside the window, so the posted turn restriction applies.',
    'Saturday is not a named day. That timed restriction is not active, but this alone does not prove a turn is safe or permitted.',
    'Explain what still needs checking: other signs, signals, lane rules and people crossing. Do not use a time calculation as permission to ignore them.'],
   'Reading one sign correctly is not the same as assessing the whole road situation.')],
 labs=[[
  with_context(evidence('sign-stop','Connect the shape to the action','Which two statements correctly describe this sign?',
   ['It is an eight-sided STOP sign.','It requires a complete stop.','It means a slow roll is always enough.'],[0,1],'Name the shape and the required action.'),sign='stop'),
  with_context(calculation('sign-clock','Read the afternoon hour','A separate sign shows 17:30. In everyday time, that is what hour followed by :30 pm? Enter only the hour number.',5,'$17-12=5$, so it is 5:30 pm.'),grid=CLOCK),
  draft_task('sign-explain',dict(title='Explain the difference',task='In your own words, compare STOP with yield. Then explain how 17:30 becomes 5:30 pm. This is a study explanation, not a live driving instruction.',
   example='STOP means a complete stop. Yield means give way, slowing or stopping as needed. For 17:30, subtract 12 from the hour to get 5 and keep the minutes, giving 5:30 pm.',
   checks=['I distinguished stopping from giving way.','I converted the hour while keeping the minutes.','I explained the meaning instead of only naming colours.']))],
 [with_context(evidence('sign-yield','Use the meaning in a situation','In this study case, giving way requires waiting for crossing traffic. Which statements fit this sign?',
   ['The driver must give way.','Stopping may be needed to give way.','The triangle gives permission to go first regardless of traffic.'],[0,1],'Yield describes giving way; it does not promise that continuing is possible.'),sign='yield'),
  with_context(evidence('sign-conditions','Check day and time together','Which conclusions match this fictional sign?',
   ['On Tuesday at 8:20 am, the posted restriction applies.','On Saturday at 8:20 am, this weekday restriction is not active; other rules still matter.','Outside the posted time, every right turn is automatically safe and legal.'],[0,1],'The action, day and time belong together. Keep the wider road context.'),grid=RESTRICTION),
  draft_task('sign-revise',dict(task='Explain the difference.',rework='Improve your explanation with the fictional no-right-turn sign: Monday to Friday, 07:00–09:00. Compare Tuesday and Saturday at 8:20 am. State why the changed day does not settle every other safety or road-rule question.',
   example='On Tuesday at 8:20 am, both the weekday and time conditions match, so the posted restriction applies. On Saturday that particular weekday restriction is not active. Other signs, signals, lane rules and people crossing still need attention; the changed day is not blanket permission.',
   checks=['I used the posted action, day and time.','I changed the conclusion for the changed day.','I kept other rules and road users in the explanation.']),True)]],
 practice=[
  q('Which action matches a STOP sign?','Come to a complete stop.','Always roll through slowly.','Treat the sign as decoration.','STOP requires stopping; use the full handbook for the situation.'),
  number('A posted time is 16:15. It is what hour followed by :15 pm? Enter the hour only.',4,'$16-12=4$, so it is 4:15 pm.'),
  q('A yield sign is ahead. Which statement is correct?','Give way, slowing and stopping when needed.','A stop is never allowed at yield.','The driver automatically has priority.','Giving way is the required outcome.'),
  q('A fictional restriction says Monday to Friday, 4 pm to 6 pm. Is Wednesday at 5 pm within those conditions?','Yes, both the day and time match.','No, because Wednesday is not a weekday.','The time matters but the day never does.','Read both conditions together.'),
  q('The same timed restriction is inactive. What follows?','Other signs, rules and road users still need checking.','Any movement is now allowed.','Traffic signals no longer matter.','An inactive restriction does not remove every other condition.'),
  q('A pedestrian sees an orange hand before starting to cross. Which action fits the handbook?','Do not begin crossing on that signal.','Start because it guarantees enough time.','Ignore all signals if someone is waiting.','Use the crossing signal and check traffic, including turning vehicles.')],
 check=[
  number('A sign shows 18:20. What hour comes before :20 pm in everyday time?',6,'$18-12=6$, so it is 6:20 pm.'),
  number('A fictional restriction runs from 14:00 to 16:00 on the same day. How many hours is that window?',2,'$16-14=2$ hours. These are 2 pm and 4 pm.'),
  q('Which description matches the STOP-sign example?','An eight-sided sign requiring a complete stop.','A sign allowing a slow roll in every case.','A sign that only controls parking.','Connect the sign with its instruction.'),
  number('A posted window ends at 3 pm. It is now 2:40 pm. How many minutes remain before that end?',20,'From 2:40 to 3:00 is 20 minutes; other conditions still need reading.'),
  q('Why keep the minutes when converting 19:45 to everyday time?','Changing the hour format does not change the minutes.','Minutes must always become zero.','Every clock conversion adds an hour.','It is 7:45 pm: the hour changes notation, the minutes do not.'),
  q('Which study statement fits a yield sign?','Give way; a stop may be needed.','Always go ahead of other traffic.','Never slow down.','The sign requires giving way, not maintaining movement.'),
  q('A fictional no-turn sign says weekdays, 07:00–09:00. At Monday 8 am, what is true?','The stated day and time conditions match.','The weekday condition is false.','It only applies on weekends.','Apply the complete posted message.'),
  q('Why does being outside that window not prove a turn is permitted?','Other restrictions and road conditions can still prevent it.','All road rules expire together.','A time check is a full driving assessment.','One inactive condition does not decide the whole situation.'),
  q('A sign has an exception for buses. A car driver is reading it. What should the driver avoid assuming?','That an exception for buses also covers the car.','That the sign contains any words.','That the vehicle type could matter.','Match exceptions to the actual vehicle and complete rule.'),
  q('Why do days printed below a timed restriction matter?','The same clock time can have a different result on a different day.','The days are always decorative.','Weekends must always follow weekday wording.','Read the day and time as separate conditions that work together.'),
  q('An orange pedestrian hand appears before someone starts crossing. Which study response fits?','Wait rather than begin crossing on that signal.','Start because all turning traffic must have disappeared.','Use the app score as permission to cross.','The signal is not an invitation to start; use the actual crossing rules and traffic conditions.'),
  q('Why use the full handbook after finishing these examples?','A few shapes and conditions do not cover all signs, signals and driving situations.','This app automatically certifies every road skill.','The handbook is replaced by six practice answers.','Use these examples as a start, with the full official learning and testing route.')],
 reflection='Explain the fictional sign’s meaning and how the changed day affects it, while keeping other rules and people in view.'
)

MODULES = [BUS, CHANGE, LICENCE, SIGNS]
CHECK_SKILLS = ['calculate','calculate','apply','calculate','reason','apply',
                'apply','reason','apply','reason','apply','reason']
for module in MODULES:
    assert len(module['check']) == len(CHECK_SKILLS)
    for question,skill in zip(module['check'],CHECK_SKILLS):
        question['skill']=skill

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)
