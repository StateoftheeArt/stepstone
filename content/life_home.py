"""Original home-life practice, integrated with the existing mission system.

Prices, bills, labels and people are fictional. Dated primary sources support
real next steps; no account details, applications or actual household records
are collected. Written plans need a human review.
"""
from digital import lesson, q
from life_services import attach_guides, calculation, evidence, number, table, with_context
from math_missions import task
from practical_missions import draft_task

CHECKED = '2026-09-24'
SOURCES = {
 'rent-basics': ('Manitoba RTB — leases, deposits and responsibilities', 'https://www.gov.mb.ca/cca/rtb/faqsgen.html'),
 'rent-help': ('Manitoba RTB — ask about a rental situation', 'https://www.gov.mb.ca/cca/rtb/detailde.html'),
 'rent-assist': ('Manitoba — Rent Assist information and eligibility', 'https://www.gov.mb.ca/fs/eia/rent_assist.html'),
 'condition': ('Manitoba RTB — condition reports and tenant forms', 'https://www.gov.mb.ca/cca/rtb/tenant/forms.html'),
 'repairs': ('Manitoba RTB — repair requests and official routes', 'https://www.gov.mb.ca/cca/rtb/tenant/repairs.html'),
 'repair-process': ('Manitoba RTB — repair responsibilities and process', 'https://www.gov.mb.ca/cca/rtb/ot/gbook/s4maintenance_llordresponsibleforrepairs3.html'),
 'repair-rent': ('Manitoba RTB — repairs fact sheet (PDF)', 'https://www.gov.mb.ca/cca/rtb/resource_list/repairs.pdf'),
 'billing': ('Manitoba Hydro — billing and payment', 'https://www.hydro.mb.ca/account/billing/'),
 'bill-help': ('Manitoba Hydro — help paying a bill', 'https://www.hydro.mb.ca/account/loans/help/'),
 'hydro-contact': ('Manitoba Hydro — customer support', 'https://www.hydro.mb.ca/support/contact/'),
 'emergency': ('Manitoba Hydro — gas, CO and electrical emergencies', 'https://www.hydro.mb.ca/safety/emergency/'),
 'meal-plan': ('Canada’s food guide — plan meals that fit your day', 'https://www.canada.ca/en/health-canada/services/food-guide/explore/healthy-eating-recommendations/cook-more-often/plan-what-you-eat.html'),
 'food-budget': ('Canada’s food guide — shopping on a budget', 'https://www.canada.ca/en/health-canada/services/food-guide/eating-support/meal-planning-grocery-shopping/healthy-eating-budget.html'),
 'leftovers': ('Health Canada — handle and store leftovers', 'https://www.canada.ca/en/health-canada/services/general-food-safety-tips/food-safety-tips-leftovers.html'),
 'food-help': ('Harvest Manitoba — ask for food support', 'https://www.harvestmanitoba.ca/need-food/'),
 'care-labels': ('Canada — guide to clothing-care symbols', 'https://ised-isde.canada.ca/site/office-consumer-affairs/en/product-safety-recalls-and-labelling/guide-apparel-and-textile-care-symbols'),
 'cleaning': ('Health Canada — use and store household products safely', 'https://www.canada.ca/en/health-canada/services/home-safety/household-chemical-safety.html'),
}

RENTALS = table('Made-up monthly costs in Canadian dollars', ['Cost','Cedar','Birch'],
 [['Rent','760','820'],['Energy estimate','90','Included'],['Travel estimate','70','50']])
MOVE_IN = table('Birch — fictional move-in plan', ['Item','Amount or detail'],
 [['First month’s rent','CAD 820'],['Security deposit','CAD 410'],['Saved for these two items','CAD 1,180'],['Other move-in costs','Still to check']])
RENT_CHANGE = table('Changed Birch estimate — not yet agreed', ['Cost','Monthly amount'],
 [['Rent','CAD 820'],['Energy, now said to be extra','CAD 80 estimate'],['Travel','CAD 50 estimate'],['Money left after other needs','CAD 900']])

RENTAL = dict(
 id='life-rental-costs',title='Compare places to live',minutes=30,
 goal='Compare the whole cost of a place and find what you need to ask before agreeing.',
 why='The lowest rent on an advert may not mean the lowest monthly cost. A few good questions can prevent a costly surprise.',
 objectives=['Compare full costs','Check the agreement','Revise your plan'],
 needs=['math-budget','reading-3','life-bank-account'],
 sources=['rent-basics','condition','rent-assist','rent-help'],help='rent-help',
 practiceNotice='Listings, prices and savings are made up. Use fictional details; this is not a rental application.',
 nextSteps=['For a real place, check the rent, due date, length of the agreement, named tenants and included services. Ask for unclear terms to be explained before agreeing. Check who you are dealing with before sending money.',
  'Plan monthly spending separately from money needed to move in. Confirm deposits, receipts and the condition of the place. RTB can explain which rules apply, including questions about shared housing or renting while under 18.',
  'If the cost does not fit, ask about other housing or support. Rent Assist has conditions to check; a lesson score does not make someone eligible. Keep real agreements, receipts and addresses out of Stepstone.'],
 lessons=[
  lesson('Count more than the advertised rent',
   'Rent pays for the place. Utilities are services such as heat or electricity. Some are included; others cost extra. Add the costs for the same month before comparing.',
   'A fair comparison includes the same items for both choices. An estimate is a best guess, not a promised bill. Keep money for food and other needs separate. A lower total only helps if the place, location and terms also work for the person.',
   'Fictional case: Lee has CAD 900 a month left after other needs. Compare Cedar and Birch in the table.',
   ['Cedar: $760+90+70=920$ dollars a month. That is $920-900=20$ dollars over this practice limit.',
    'Birch: $820+0+50=870$ dollars a month. Included energy adds zero to this estimate, not a second energy bill.',
    'Birch leaves $900-870=30$ dollars. Check the estimate and other costs before choosing; thirty dollars is not a guarantee against surprises.'],
   'Do not compare one place’s rent alone with another place’s total. Keep the time period and included items the same.'),
  lesson('Read what you would be agreeing to',
   'A lease is a rental agreement. Read what it includes. Moving in can also need a deposit and other costs. If a detail changes, stop and update your plan before agreeing.',
   'Monthly costs and move-in money answer different questions. In an ordinary Manitoba tenancy covered by RTB rules, a security deposit is limited to half the first month’s rent; ask RTB about other deposits or situations. A spoken promise about an included service should be clarified in the agreement. Check the terms, not just the total.',
   'Fictional change: Birch’s energy is now said to cost an extra CAD 80 a month. Lee still has CAD 900 available monthly.',
   ['The first rent and stated deposit total $820+410=1230$ dollars. With CAD 1,180 saved, $1230-1180=50$ dollars is still missing, before other moving costs.',
    'The changed monthly total is $820+80+50=950$. That exceeds the monthly limit by $950-900=50$ dollars.',
    'Lee asks which utilities are included and requests clear terms. Lee can compare another place or ask about support, instead of treating an unaffordable plan as settled.'],
   'Do not add the deposit to every month’s rent. Do not assume a lower advertised rent, a possible benefit or a verbal promise solves a shortfall.')],
 labs=[[
  with_context(calculation('rental-total','Build Cedar’s full cost','Using the table, how many dollars is Cedar’s monthly rent, energy and travel total?',920,'$760+90+70=920$ dollars. Count each item once.'),grid=RENTALS),
  with_context(evidence('rental-compare','Compare the whole month','Lee has CAD 900 after other needs. Select the two statements supported by the table.',
   ['Birch’s listed monthly costs total CAD 870.','Cedar’s listed monthly costs exceed CAD 900.','Cedar must cost less overall because its rent is lower.'],[0,1],
   'Cedar totals CAD 920 and Birch CAD 870. The headline rent alone gives the wrong comparison.'),grid=RENTALS),
  with_context(draft_task('rental-plan',dict(title='Make Lee’s first plan',task='Write a fictional plan: compare the monthly totals, name the move-in money still missing, and ask one question about the agreement.',
   example='Birch’s listed costs are CAD 870 a month, compared with Cedar’s CAD 920. Lee is CAD 50 short for the first rent and deposit, before other moving costs. I would ask which utilities the agreement includes.',
   checks=['I compared the same monthly costs.','I kept the move-in shortfall separate.','I asked about a term and used only fictional details.'])),grid=MOVE_IN)],
 [with_context(calculation('rental-change','Energy is now extra','With the changed Birch table, what is the new monthly total in dollars?',950,'$820+80+50=950$ dollars. The new information must replace the old estimate.'),grid=RENT_CHANGE),
  evidence('rental-decision','The plan no longer fits','Which two actions help Lee respond to the new cost?',
   ['Ask for the included services to be clear in the agreement.','Compare another option or ask about available support.','Pay now because the old total was below the limit.'],[0,1],
   'The updated plan is CAD 50 over the monthly limit. Clarify and reconsider before committing.'),
  draft_task('rental-revise',dict(task='Make Lee’s first plan.',rework='Revise the plan for CAD 80 extra energy each month. Include the new total, the monthly gap and a useful next step. Keep the separate move-in gap visible.',
   example='Birch is now estimated at CAD 950 monthly, CAD 50 above Lee’s limit. Lee also remains CAD 50 short of the first rent and deposit. I would clarify utilities in writing and compare another place or ask about support before agreeing.',
   checks=['I used the changed monthly total and limit.','I kept monthly and move-in gaps separate.','I chose a next step without promising support or approval.']),True)]],
 practice=[
  number('A fictional place costs 740 dollars rent, 80 energy and 60 travel each month. What is the monthly total?',880,'$740+80+60=880$ dollars.'),
  q('One advert includes heat; another lists heat as extra. What makes the comparison useful?','Include estimated heat in the second total.','Compare only the larger headline number.','Assume heat is free in both.','Use the same kinds of cost for the same time period.'),
  number('The first rent is 800 dollars and the stated one-time deposit is 400. What is their combined move-in cost?',1200,'$800+400=1200$ dollars before any other moving costs.'),
  number('A monthly estimate was 860 dollars. A newly confirmed extra utility adds 70. What is the new total?',930,'$860+70=930$ dollars. Replace the outdated total.'),
  q('An included-service promise differs from the written agreement. What should happen before agreeing?','Ask for clarification and clear terms.','Assume the cheapest version must apply.','Ignore the written terms.','Resolve the mismatch before relying on it.'),
  q('A renter might qualify for Rent Assist. How should a budget treat that possibility?','Check eligibility and the actual outcome before counting it as confirmed money.','Count any amount they wish for as approved.','Treat a quiz pass as a benefit approval.','Possible support is not a confirmed payment.')],
 check=[
  number('A made-up monthly plan has 710 dollars rent, 95 energy and 65 travel. What is its total?',870,'$710+95+65=870$ dollars.'),
  number('A person has 930 dollars after other needs. Listed housing and travel total 875. How many dollars remain?',55,'$930-875=55$ dollars.'),
  q('Which details belong in a check of a rental agreement?','Amount, due date, length and included services.','Only the size of the title.','Only the colour of the building.','The terms explain what is being agreed to.'),
  number('First rent is 900 dollars and the stated deposit is 450. How much is needed for those two items?',1350,'$900+450=1350$ dollars.'),
  q('Why can a lower advertised rent still lead to a higher monthly total?','Extra utilities or travel can outweigh the rent difference.','Addition stops working for rent.','A cheaper advert includes every cost automatically.','Compare the complete supplied cost list.'),
  q('The move-in plan says “other costs unknown”. What is a useful action?','Find out about those costs before calling the budget complete.','Replace unknown with zero without checking.','Add the deposit to every future month.','Unknown costs need a question, not an invented amount.'),
  q('A new term says the renter pays electricity. What changes first?','The cost estimate and the questions about the agreement.','Only the colour of the plan.','The renter’s age.','A changed responsibility can change the budget.'),
  q('Why keep receipts and a condition record privately?','They preserve evidence about payments and the place’s condition.','They guarantee every future claim will succeed.','They replace reading the agreement.','Records can support a later question; they do not decide every dispute.'),
  q('A deposit rule or shared-housing arrangement is unclear. Which route fits?','Ask Manitoba’s Residential Tenancies Branch which rules apply.','Use any rule from a different province without checking.','Treat the Stepstone mentor as the landlord.','Check the actual jurisdiction and arrangement.'),
  q('Why is an energy estimate different from a fixed agreed charge?','Actual use and conditions may change an estimated bill.','An estimate means the charge is always zero.','Both words guarantee exactly the same price.','Label uncertainty rather than hiding it.'),
  q('Which information belongs in this learning draft?','A made-up comparison and questions to ask.','A photo of the real signed lease.','An actual bank account number.','Practice can show the method without storing private documents.'),
  q('The revised total is above the available money. Why is another planning step needed?','The old plan no longer fits the stated limit.','A correct addition automatically supplies the missing money.','A rental decision cannot be changed before agreement.','A calculation identifies the problem; a workable next action addresses it.')],
 reflection='Explain the revised rental comparison, the separate move-in cost and the question Lee still needs answered.'
)

BILL = table('Fictional energy statement — Canadian dollars', ['Line','Amount'],
 [['Previous unpaid balance','30'],['New charges','90'],['Payment already credited','20'],['Total amount due','100']])
DUE = table('Fictional bill calendar', ['Bill','Due','Amount'],
 [['Energy','15 October','CAD 100'],['Internet','18 October','CAD 45'],['Available for these bills','Now','CAD 130'],['Next pay','20 October','Not available yet']])
ARRANGEMENT = table('Fictional confirmed payment arrangement', ['Item','Agreed date','Amount'],
 [['Energy part 1','15 October','CAD 40'],['Internet, unchanged','18 October','CAD 45'],['Energy part 2','22 October','CAD 60']])

BILLS = dict(
 id='life-home-bills',title='Keep track of home bills',minutes=30,
 goal='Read a bill, plan payment dates and ask early when the money will not cover it.',
 why='A bill has several numbers. Knowing which is the total, and when it is due, helps you make a useful plan.',
 objectives=['Read the amount due','Match money to dates','Handle a shortfall'],
 needs=['math-budget','reading-3','digital-4'],
 sources=['billing','bill-help','hydro-contact'],help='bill-help',
 practiceNotice='All bills, dates, payments and arrangements are fictional. Do not enter account numbers or banking details.',
 nextSteps=['Use the provider’s official account or contact route. Check the period, payments already credited, amount due and due date. Ask about a charge you do not understand; keep real records private.',
  'Set a reminder and use an accepted payment method early enough for it to arrive. A saved reminder or pending transfer is not proof that a bill is paid. Check the receipt and provider balance.',
  'If you cannot pay in full, contact the provider promptly. Manitoba Hydro lists payment arrangements and help programs with conditions. Ask what is agreed, record the dates, and follow up if the plan changes. No lesson can promise a fee waiver or funding.'],
 lessons=[
  lesson('Find the total without counting it twice',
   'A balance is money still owed. New charges add to it. Payments already counted reduce it. The amount due is the result. Find the due date, then check when your money is available.',
   'A statement’s total often already includes the other lines. Adding them again makes a false debt. Also separate a bill’s issue date from its payment deadline. Having enough money next week does not mean it is available for a bill due today. A calendar makes that timing visible.',
   'Fictional energy bill: CAD 30 unpaid, CAD 90 new charges and CAD 20 already credited. Internet adds CAD 45 on a different date.',
   ['Energy: $30+90-20=100$ dollars due. Do not add the CAD 100 total to its own parts.',
    'Both bills need $100+45=145$ dollars. With CAD 130 available, the gap is $145-130=15$ dollars.',
    'Energy is due 15 October and internet on 18 October. The stated pay date, 20 October, comes after both deadlines. Ask about the gap early.'],
   'The bill date is not necessarily the due date. A future pay date or a reminder does not automatically extend a deadline.'),
  lesson('Ask, confirm, then update the calendar',
   'If money is short, contact the provider. Explain the problem and ask about options. A payment plan is only agreed when the provider confirms it. Keep the amount and date for each part.',
   'A partial payment leaves a balance. It does not create an extension by itself. In the fictional example, a provider confirms new dates; that confirmation is the reason the calendar changes. Check future commitments too. An equal-payment plan spreads costs; it does not make energy free or erase an old balance.',
   'Fictional change: energy payments are confirmed as CAD 40 on 15 October and CAD 60 on 22 October. Internet stays CAD 45 on 18 October.',
   ['By 18 October, the plan needs $40+45=85$ dollars. CAD 130 available leaves $130-85=45$ dollars for this plan.',
    'The remaining energy part is CAD 60, so the stated CAD 45 alone is $60-45=15$ dollars short. Confirm money available before 22 October.',
    'Record the provider’s confirmation and both dates. If the later money will not arrive, contact the provider again; do not silently assume another extension.'],
   'Treat an unexpected payment message cautiously. Open the known provider’s site or number yourself, rather than using an urgent message’s link.')],
 labs=[[
  with_context(calculation('bill-total','Check the energy total','What is owed after the payment already credited? Enter dollars.',100,'$30+90-20=100$. The printed total is not an extra charge.'),grid=BILL),
  with_context(evidence('bill-dates','Does the timing fit?','Select the two facts that show why Ari needs to act before the next pay.',
   ['The two bills need CAD 145, but only CAD 130 is available.','Both stated due dates are before 20 October.','The next pay date automatically changes every bill’s due date.'],[0,1],
   'There is a CAD 15 shortfall and a timing gap. Ask before assuming a payment plan.'),grid=DUE),
  draft_task('bill-plan',dict(title='Make Ari’s bill plan',task='Write the two totals and due dates, the shortfall and a question for the provider. Use fictional details.',
   example='Ari owes CAD 100 by 15 October and CAD 45 by 18 October. There is CAD 130 now, leaving a CAD 15 gap before pay on 20 October. Ari will ask the provider whether an arrangement is possible and record its response.',
   checks=['I used the amount due without double-counting.','I matched due dates with available money.','I asked for an option without claiming it is already approved.']))],
 [with_context(calculation('bill-arrangement','Use the confirmed dates','Under this fictional confirmed arrangement, how many dollars must be paid by the end of 18 October?',85,'$40+45=85$ dollars. The other CAD 60 is due later.'),grid=ARRANGEMENT),
  evidence('bill-left','Keep the remaining balance visible','Ari has CAD 45 left after those payments. Which statements fit?',
   ['The CAD 60 later payment still needs a plan.','Ari must check the later money and contact the provider if it will not arrive.','Making the first payment proves the full bill is paid.'],[0,1],
   'A staged plan still has later obligations. CAD 45 is CAD 15 less than the remaining CAD 60.'),
  draft_task('bill-revise',dict(task='Make Ari’s bill plan.',rework='Revise Ari’s plan using the confirmed dates. Include the CAD 85 needed by 18 October and the remaining CAD 60. State what must be checked for 22 October.',
   example='The confirmed plan needs CAD 40 on 15 October, CAD 45 on 18 October and CAD 60 on 22 October. After the first CAD 85, Ari has CAD 45. Ari will check that at least CAD 15 more is available before the last payment and contact the provider if that changes.',
   checks=['I used the confirmed dates and kept internet separate.','I kept the later balance and money gap visible.','I included a confirmation or follow-up step.']),True)]],
 practice=[
  number('A fictional bill has 20 dollars unpaid, 60 new charges and 10 already paid. What is due?',70,'$20+60-10=70$ dollars.'),
  q('A bill was issued on the 4th and is due on the 19th. Which date is the stated payment deadline?','The 19th.','The 4th simply because it is printed first.','Any date chosen without agreement.','Read the label beside each date.'),
  number('Two supplied totals are 80 dollars and 35 dollars. What is their combined amount due?',115,'$80+35=115$ dollars. Use each bill’s total once.'),
  number('A confirmed arrangement splits 100 dollars into 60 and a remaining part. How many dollars are in that remaining part?',40,'$100-60=40$ dollars.'),
  q('Someone has requested an extension but has no reply. What is the accurate status?','Requested; not yet confirmed.','Approved automatically.','Paid in full.','Separate asking, approval and payment.'),
  q('An unexpected text asks for gift cards to settle an energy bill. What is a useful response?','Verify through the provider’s known contact route before paying anything.','Buy cards because the text says urgent.','Send a password to prove identity.','Urgency and a logo do not verify a sender.')],
 check=[
  number('A made-up statement has 35 dollars unpaid, 90 new charges and a credited payment of 25. What is due?',100,'$35+90-25=100$ dollars.'),
  number('There are 140 dollars available for bills totalling 110. How many dollars remain?',30,'$140-110=30$ dollars.'),
  q('A bill is due on the 12th and pay arrives on the 16th. What should be checked?','How to cover or arrange the payment before its deadline.','Whether the later pay date silently replaces the due date.','Whether ignoring the bill removes it.','Timing matters as well as the total.'),
  number('Two bills total 175 dollars. There are 150 dollars available. How many more dollars are needed?',25,'$175-150=25$ dollars.'),
  q('Why not add a printed total to all the lines used to produce it?','That would count the same charges twice.','Printed totals are always meaningless.','Payments never affect totals.','Identify parts and whole before calculating.'),
  q('A statement shows a payment you think is missing. What helps?','Check the payment record and ask the provider to explain.','Pay a stranger to edit the statement.','Assume a screenshot changes the account.','Use the actual record and service to resolve the mismatch.'),
  q('A provider confirms two later payment dates. What belongs in the revised calendar?','Both amounts and both confirmed dates.','Only the first instalment.','Only the original bill issue date.','The whole arrangement matters.'),
  q('Why is a reminder different from a receipt?','A reminder prompts action; a receipt records a payment.','A reminder automatically transfers money.','The words always mean the same thing.','Planning an action is not evidence it happened.'),
  q('Where can a Manitoba Hydro customer ask about trouble paying?','Hydro’s official bill-help or customer-support route.','A random urgent text reply.','Only the app’s points page.','Check current arrangements and program conditions with the provider.'),
  q('Why should a plan keep ordinary bills alongside an overdue balance?','New costs can continue while old amounts are being paid.','An old balance cancels future bills automatically.','Only the smallest amount counts.','A plan needs to fit both ongoing and past commitments.'),
  q('The next pay will arrive later than expected. What is useful?','Recheck the dates and contact the provider before assuming the arrangement still fits.','Silently invent another extension.','Mark every amount paid.','A changed income date can require a changed agreed plan.'),
  q('Why should a possible assistance program stay labelled unconfirmed?','Eligibility and approval still need checking.','A possible grant is already in the bank.','A quiz score guarantees the application.','A plan should distinguish known money from hoped-for help.')],
 reflection='Explain Ari’s revised dates, the money still needed and how to tell a request from a confirmed arrangement.'
)

RECIPE = table('Practice lunch recipe — two lunch packs', ['Ingredient','For two packs'],
 [['Whole wraps, cut into halves','2 wraps = 4 halves'],['Ready-to-eat beans, drained','250 mL'],['Prepared vegetables','250 mL']])
SHOP = table('Fictional shop — final prices, no extra charges in this exercise', ['Item to buy','Price'],
 [['4 wraps','CAD 4'],['250 mL beans','CAD 3'],['250 mL vegetables','CAD 4'],['Money for this purchase','CAD 12']])
FOOD_CHANGE = table('Six lunch packs — changed shopping choices', ['Item to buy','Price'],
 [['6 wraps','CAD 6'],['500 mL beans','CAD 4'],['500 mL prepared vegetables','CAD 4'],['Suitable vegetable alternative, 500 mL','CAD 2']])

MEALS = dict(
 id='life-meal-plan',title='Plan meals and groceries',minutes=30,
 goal='Scale a simple meal, shop for what is missing and make a workable backup.',
 why='Food planning combines counting, reading and choices. Start with the food, time and equipment available.',
 objectives=['Scale the amounts','Build a shopping plan','Adapt without guessing'],
 needs=['math-3','math-4','math-prices'],
 sources=['meal-plan','food-budget','leftovers','food-help'],help='food-help',
 practiceNotice='This is a made-up meal-planning exercise, not a complete diet. Prices are fictional. Use food that suits the person’s needs.',
 nextSteps=['Choose meals and snacks that fit the people, available time, equipment and storage. Check food already on hand, labels and allergies or other food needs. Use a suitable recipe rather than guessing cooking instructions.',
  'Write the missing items and compare amounts and prices. A larger package only helps if it fits the cash available and can be used or stored safely. Recheck substitutions; do not treat a cheaper ingredient as automatically suitable.',
  'Follow current food-safety instructions for preparation and storage. If money or access is the obstacle, Harvest Manitoba can explain food-support options. Asking for food support is a practical step, not a failed lesson.'],
 lessons=[
  lesson('Make the right amount for the people',
   'A recipe amount is for a stated number of portions. To make twice as many, double each ingredient. Then check what you already have. Shop for the missing amount, not the full recipe again.',
   'The same scale factor keeps the ingredient amounts in the same proportion. It does not automatically double cooking time. This cold-wrap example uses ready-to-eat ingredients and clean hands and utensils. Real portions and food choices depend on the people; this model is for practising a method.',
   'Practice recipe: two lunch packs use two wraps, 250 mL beans and 250 mL vegetables. Each wrap is cut into two halves.',
   ['For four packs, $4\\div2=2$: multiply each ingredient amount by two. Use four wraps, 500 mL beans and 500 mL vegetables.',
    'There is one wrap, 250 mL beans and 250 mL vegetables already available. The missing amounts are three wraps, 250 mL beans and 250 mL vegetables.',
    'The fictional shop sells four wraps together. Buying that pack plus the missing beans and vegetables costs $4+3+4=11$ dollars. CAD 12 leaves CAD 1; one bought wrap is spare.'],
   'The amount needed and the package you must buy can differ. Check the package price and what you will do with any extra.'),
  lesson('More people means a new plan',
   'Two more people join. Recount the portions before shopping. Check a suitable cheaper option if the cost rises. Include safe storage in the plan. Food that smells fine can still be unsafe.',
   'Six packs need three times the two-pack recipe: six wraps and 750 mL each of beans and vegetables. With the same pantry amounts, five wraps and 500 mL of each filling are missing. Compare whole purchase costs, not just the cheapest sticker. Store leftovers promptly; cooked food left at room temperature over two hours should be discarded, not judged by smell.',
   'Fictional change: make six packs using the same pantry. The listed prepared vegetables cost CAD 4; a suitable alternative costs CAD 2.',
   ['The first purchase costs $6+4+4=14$ dollars, which is $14-12=2$ dollars over the available money.',
    'The suitable alternative gives $6+4+2=12$ dollars. It supplies the needed amount within this exercise’s limit.',
    'Check the actual food labels and safe handling. Plan refrigeration promptly; use the linked storage guide. If no workable food option exists, ask about help rather than hide the gap.'],
   'Do not scale cooking temperature or cooking time just because portions increase. Do not stretch a budget by relying on food whose storage was unsafe.')],
 labs=[[
  with_context(task('meal-packs','Build four lunch packs','Set four packs with two wrap halves in each. Each dot represents one half-wrap. Keep “In each pack” at 2.','groups',
   'There are four people in this practice case. Make one two-half pack for each person.','$4\\times2=8$ half-wraps, which come from four whole wraps.',
   start=dict(groups=2,each=2),target=dict(groups=4,each=2),fixed=['each']),grid=RECIPE),
  with_context(calculation('meal-beans','Scale the beans','How many mL of beans are needed for four packs in total?',500,'$250\\times2=500$ mL. This is the total recipe amount, before subtracting pantry food.'),grid=RECIPE),
  with_context(draft_task('meal-plan',dict(title='Build the first shopping plan',task='For four packs, there is already one wrap and 250 mL each of beans and vegetables. Write what is missing, which shop packs to buy, and the cost.',
   example='We need three more wraps and 250 mL each of beans and vegetables. Buy the four-wrap pack for CAD 4, beans for CAD 3 and vegetables for CAD 4. That costs CAD 11 and leaves one purchased wrap spare and CAD 1.',
   checks=['I subtracted what is already available.','I used package costs, including any spare food.','I planned food the people can eat and used fictional details.'])),grid=SHOP)],
 [with_context(calculation('meal-cost-change','Two more people join','For six packs, buy the listed wrap pack, beans and the CAD 4 vegetables. What is the total cost in dollars?',14,'$6+4+4=14$ dollars, CAD 2 above the stated CAD 12 budget.'),grid=FOOD_CHANGE),
  with_context(evidence('meal-backup','Choose a workable revision','The CAD 2 vegetable alternative is stated to be suitable and the right amount. Which facts support using it?',
   ['The revised purchase totals CAD 12.','The alternative provides the needed 500 mL.','A cheaper option means labels and storage no longer matter.'],[0,1],
   'The replacement fits both the quantity and the exercise’s budget. Real substitutions still need checking.'),grid=FOOD_CHANGE),
  draft_task('meal-revise',dict(task='Build the first shopping plan.',rework='Revise the plan for six packs. Include the new quantities, the suitable CAD 2 vegetable choice, the purchase total and a storage step.',
   example='Six packs need six wraps and 750 mL of each filling. With the pantry food, buy six wraps and 500 mL each of beans and suitable vegetables. The revised purchase is CAD 12. Keep ingredients safely chilled and refrigerate leftovers promptly using the storage guide.',
   checks=['I scaled all ingredient amounts for six packs.','I used the available pantry food and revised purchase cost.','I included a safe storage step and checked suitability.']),True)]],
 practice=[
  number('A practice recipe uses 200 mL beans for two portions. How many mL for four portions?',400,'$200\\times2=400$ mL.'),
  number('A meal needs 600 mL vegetables. There are 250 mL available. How many mL are missing?',350,'$600-250=350$ mL.'),
  q('You need three wraps but the shop sells packs of four. What belongs in the purchase cost?','The price of the whole pack being bought.','Only three quarters of the price without a part-pack option.','No cost because one wrap will be spare.','The purchase is for the package actually sold.'),
  number('A changed shopping list costs 5, 4 and 3 dollars. What is the total?',12,'$5+4+3=12$ dollars.'),
  q('A cheaper ingredient replaces the original. What still needs checking?','Its amount, suitability and storage instructions.','Only whether the packaging is brighter.','Nothing because cheaper always means equivalent.','A useful substitution must fit the actual meal and people.'),
  q('Cooked food was left on a room-temperature counter for three hours. What fits the linked safety advice?','Discard it; smell is not a reliable safety test.','Eat it if it smells pleasant.','Assume adding fresh food makes it safe.','Three hours is beyond the two-hour room-temperature guidance.')],
 check=[
  number('A practice recipe needs 150 mL filling for two portions. How many mL for six portions?',450,'$6\\div2=3$ and $150\\times3=450$ mL.'),
  number('A plan needs 8 wraps and already has 3. How many more wraps are needed?',5,'$8-3=5$ wraps.'),
  q('What should be read before changing a recipe’s quantities?','The number of portions the original amounts make.','Only the title’s font.','Only the largest printed number.','Scaling needs an original amount and a target.'),
  number('The actual packages on a fictional shopping list cost 6, 3 and 4 dollars. What is the total?',13,'$6+3+4=13$ dollars.'),
  q('Why can a bulk package with a low unit price still be unsuitable?','It may exceed available money or be too much to store and use.','Unit prices have no meaning.','Bulk food never needs storage.','Consider both price per unit and the usable purchase.'),
  q('What is a useful first step before buying food?','Check what is available and safe to use already.','Buy the whole recipe again regardless.','Assume everyone can eat every ingredient.','An inventory prevents unnecessary purchases.'),
  q('Two extra people join a meal. What should be revised?','Portions, missing ingredients and the shopping cost.','Only the meal’s name.','Only the date on the old list.','A changed number of people affects the quantities.'),
  q('Why does doubling a recipe not automatically mean doubling its oven temperature?','Quantity scaling does not determine safe cooking settings.','All ovens need the same maximum setting.','Ingredient arithmetic proves food is cooked.','Use the actual recipe and food-safety instructions.'),
  q('There is no affordable workable option in the stated plan. What is a useful next step?','Ask about food support or another suitable meal plan.','Treat needing help as a personal failure.','Pretend the missing money is already available.','A real barrier calls for a practical support route.'),
  q('Why is a pleasant smell insufficient to prove leftovers safe?','Unsafe contamination may not be detected by smell.','A strong perfume makes any food safe.','Storage history never matters.','Use safe handling and storage information.'),
  q('Someone cannot eat a proposed ingredient. What should happen?','Choose and check a suitable alternative with them.','Hide it in the meal to finish the task.','Assume a lower price removes the concern.','The meal has to fit the person, not just the budget.'),
  q('Why should the revised plan show spare ingredients?','They can be planned for, stored safely or avoided next time.','All spare food must stay on a warm counter.','Spare food has no purchase cost.','Keep the difference between bought and used amounts visible.')],
 reflection='Explain the six-pack shopping plan, why the substitution works and what you would check before preparing or storing the food.'
)

CARE = table('Fictional clothing labels — words supplied for practice', ['Item','Wash','Dry'],
 [['Shirt','Cold, machine wash','Low heat'],['Sweater','Hand wash, cool','Dry flat'],['Towels','Warm, machine wash','Medium heat']])
LAUNDRY = table('Fictional laundry plan', ['Part','Price','Time'],
 [['One wash','CAD 3','30 minutes'],['One dryer cycle','CAD 2','40 minutes'],['Available','CAD 12','90 minutes']])
CLEAN_PLAN = table('Fictional task list', ['Task','What the label or situation says'],
 [['Clean a table','Use a suitable labelled cleaner as directed'],['Bottle by the sink','No label; contents unknown'],['Sweater in the basket','Hand wash; dry flat'],['Time available','One small task is enough to start']])

CARE_MODULE = dict(
 id='life-home-care',title='Care for clothes and your space',minutes=30,
 goal='Read care instructions and choose a manageable laundry or cleaning plan.',
 why='A few label checks can protect your clothes and your space. You do not have to solve the whole house at once.',
 objectives=['Read the instructions','Plan one task','Adjust safely'],
 needs=['reading-3','math-cash','science-1'],
 sources=['care-labels','cleaning'],help='cleaning',
 practiceNotice='Labels, prices and timings are made up for reading practice. Follow the actual item, machine and product instructions at home.',
 nextSteps=['Pick one manageable task. Read the garment’s care label and the machine’s instructions; ask about a symbol you do not recognise. The linked Canadian symbol guide is an explanation resource, not a claim that every item uses the same label.',
  'For cleaning, choose a suitable product and follow its label, including ventilation and protection. Never mix household chemical products. Keep them in their labelled original containers, closed and out of reach of children and pets.',
  'If a label is missing or a task is unclear, pause and get suitable help or another labelled product. If someone may have been harmed by a chemical, use the poison-centre or medical-help route on Health Canada’s page promptly. Do not wait for an app reply.'],
 lessons=[
  lesson('The label decides the method',
   'Read how to wash and how to dry. They are separate instructions. Sort items by compatible care needs. Plan the cost and time. Start with one load you know how to handle.',
   'Two clothes of the same colour can need different care. The practice table supplies words; a real label may use symbols. Check both the item and machine before using them. A laundry budget includes the whole task, and the time estimate needs room for changing machines or waiting.',
   'Fictional plan: a shirt says cold machine wash and low-heat drying. A wash is CAD 3 for 30 minutes; drying is CAD 2 for 40 minutes.',
   ['Choose the cold wash and low-heat dryer setting for this shirt, following the actual machine instructions.',
    'One wash-and-dry task costs $3+2=5$ dollars. Two such tasks would cost $2\\times5=10$ dollars.',
    'The cycles take $30+40=70$ minutes. In a 90-minute plan, $90-70=20$ minutes remain for moving items or waiting; queues can still change the plan.'],
   'Do not assume all items in one basket can share the hottest or fastest setting. A drying instruction matters too.'),
  lesson('A changed label changes the plan',
   'A hand-wash sweater is mixed into the basket. Take it out of the machine load. An unlabelled bottle is nearby. Leave it alone. Choose a known, suitable product for a small cleaning task.',
   'Changing one item can change which method is suitable. Dry flat means lay the item flat to dry; it does not mean use a hot dryer. For cleaning, more product or a mixture is not a shortcut. Read the actual instructions and keep the task small enough to finish without rushing.',
   'Fictional change: the sweater says hand wash and dry flat. The bottle by the sink has no label.',
   ['Separate the sweater and plan its stated hand-wash and flat-dry method. Ask for help if the method is unfamiliar.',
    'Do not use or mix the unknown liquid. For the table, use a suitable labelled cleaner according to its instructions.',
    'The planned shirt load still costs CAD 5. From CAD 12, $12-5=7$ dollars remain. Check any separate sweater cost rather than inventing one.'],
   'Never mix cleaners or transfer them into a drink bottle. A missing label is a reason to stop and check, not guess.')],
 labs=[[
  with_context(evidence('care-shirt','Read both instructions','Select the two instructions that match the shirt.',
   ['Use the stated cold machine wash.','Use the stated low-heat drying.','Use medium heat because the towels allow it.'],[0,1],
   'Read across the shirt’s row. A different item’s instructions do not apply to it.'),grid=CARE),
  with_context(calculation('care-cost','Budget two laundry tasks','How many dollars do two wash-and-dry tasks cost at these made-up prices?',10,'$2\\times(3+2)=10$ dollars.'),grid=LAUNDRY),
  draft_task('care-plan',dict(title='Make one manageable plan',task='Write a plan for one shirt load. Include wash and dry instructions, CAD 5 cost, the 70 minutes of cycles and time to move or wait.',
   example='I will use the shirt’s cold wash and low-heat drying instructions. One task costs CAD 5 and the cycles take 70 minutes. In the 90-minute plan I have 20 minutes for moving clothes or waiting, and I will recheck if there is a queue.',
   checks=['I included both wash and dry instructions.','I counted the whole cost and cycle time.','I chose a manageable task and allowed for waiting.']))],
 [with_context(evidence('care-change','Handle the changed basket','Which two changes fit these instructions?',
   ['Keep the hand-wash sweater out of the shirt’s machine load.','Leave the unknown liquid unused and choose a suitable labelled product.','Mix the unknown liquid with cleaner to make it stronger.'],[0,1],
   'The sweater has different care needs, and the bottle gives no reliable product instructions.'),grid=CLEAN_PLAN),
  calculation('care-left','Keep track of what remains','There is CAD 12 for the task. One shirt wash and dry costs CAD 5. How many dollars remain?',7,'$12-5=7$ dollars. Do not assume a separate task has no cost.'),
  draft_task('care-revise',dict(task='Make one manageable plan.',rework='Revise the shirt plan after finding the hand-wash sweater and unknown bottle. Include what you will separate, how you will dry the sweater and a suitable small cleaning step.',
   example='I will keep the shirt’s cold-wash and low-dry plan. I will separate the sweater, follow its hand-wash directions and dry it flat. I will leave the unlabelled bottle unused, choose a suitable labelled cleaner and follow its instructions for the table.',
   checks=['I responded to the sweater’s different care instructions.','I left the unknown product unused and did not mix cleaners.','I kept the task manageable and included safe labelled use.']),True)]],
 practice=[
  q('A label says hand wash and dry flat. Which plan matches?','Hand wash as directed, then lay flat to dry.','Machine wash hot and tumble dry high.','Use another shirt’s label instead.','Follow the instructions for this item.'),
  number('A fictional wash is 4 dollars and drying is 2 dollars. What is the combined cost?',6,'$4+2=6$ dollars.'),
  number('One cycle takes 25 minutes and the next takes 35. How many minutes of cycle time is that?',60,'$25+35=60$ minutes, before any waiting or transfer time.'),
  q('A bottle has no readable label. What is the useful action?','Leave it unused and get suitable help or a known labelled product.','Identify it by tasting it.','Mix it with a known cleaner.','The product and safe-use instructions must be known.'),
  q('Why keep a cleaner in its original labelled container?','The product and safety instructions remain identifiable.','It becomes safe to drink.','The label replaces closing the cap.','Identification and storage instructions matter.'),
  q('The laundry queue makes the planned finish impossible. What should change?','The timing or choice of task, while keeping care instructions.','The garment’s label.','The safe settings just to force a faster finish.','Adapt the schedule rather than invent a different care rule.')],
 check=[
  number('A fictional wash is 2.50 dollars and drying is 1.50. What is the total in dollars?',4,'$2.50+1.50=4.00$ dollars.'),
  number('Each complete wash-and-dry task costs 4 dollars. What do two such tasks cost?',8,'$2\\times4=8$ dollars.'),
  q('A care label allows cool washing but says dry flat. What should a plan include?','Both the cool-wash and flat-dry instructions.','Only the washing instruction.','Any dryer setting.','Washing and drying are different parts of care.'),
  number('A wash takes 30 minutes and drying takes 40. How many minutes of cycle time should be counted?',70,'$30+40=70$ minutes.'),
  q('Why might two same-coloured garments need separate care?','Their care labels can specify different methods.','Colour guarantees identical fabric and care.','Every garment has the same drying rule.','Check the actual items, not only how they look.'),
  q('The machine instructions are unclear. What is useful?','Ask for help before starting an unfamiliar setting.','Force controls until something starts.','Assume a different machine works identically.','Knowing the item’s care needs is only part of using the machine.'),
  q('An unknown cleaning liquid is found during the task. What fits?','Leave it unused rather than guessing or mixing it.','Try a little in a drink cup.','Combine it with bleach to test it.','Unknown contents do not provide safe-use directions.'),
  q('Why is mixing household cleaners a poor shortcut?','Some combinations can release harmful gases.','A mixture always removes the need for ventilation.','All household products have identical ingredients.','Use a suitable product as labelled.'),
  q('A product label requires ventilation and gloves. What should be planned?','Those conditions before using that product.','Only how quickly the task can end.','Using more product to replace the precautions.','Safe-use instructions are part of the task.'),
  q('Why choose one small cleaning task when the whole room feels too much?','It creates a manageable next action that can be finished.','It proves the whole home is permanently clean.','Every other responsibility disappears.','A small complete action can be a useful start.'),
  q('Where should household chemicals be stored?','As labelled, in closed original containers, out of children’s and pets’ reach.','In an open drink bottle.','Mixed together to save shelf space.','Keep both the contents and their instructions identifiable.'),
  q('Why is a saved cleaning plan not proof a real task was completed safely?','The app records the plan, not the actual product use or result.','Typing a plan changes the room automatically.','A quiz can inspect every household.','Real practice and appropriate help provide different evidence.')],
 reflection='Explain the revised laundry and cleaning plan, including why the sweater and unknown bottle change the next action.'
)

REPAIR_LOG = table('Fictional repair notes', ['When','What was observed or agreed'],
 [['Monday, 6:00 pm','Kitchen cupboard door hangs loose'],['Monday, 6:15 pm','Written request sent to landlord'],['Tuesday','Reply offers Wednesday, 2–4 pm'],['Current condition','No immediate hazard reported in this case']])
REPAIR_CHANGE = table('Fictional changed availability', ['Item','Time'],
 [['New work shift','Wednesday, 2–5 pm'],['Class','Thursday, 10 am–noon'],['Proposed visit A','Thursday, 9–11 am'],['Proposed visit B','Friday, 1–3 pm']])

REPAIR = dict(
 id='life-repair-request',title='Ask for a home repair',minutes=30,
 goal='Describe a problem clearly, keep a useful record and follow up through the right route.',
 why='You do not have to diagnose a fault to explain what you noticed and ask for it to be checked.',
 objectives=['Record useful facts','Ask clearly','Choose the next route'],
 needs=['writing-3','social-5','life-rental-costs'],
 sources=['repairs','repair-process','repair-rent','emergency','rent-help'],help='rent-help',
 practiceNotice='Use the fictional home and dates. No repair request is sent, and no real address or home photo is needed.',
 nextSteps=['For an ordinary rental repair, tell the landlord what needs attention, preferably in writing. State where it is, what you observed and when. Keep a private record of the request and response.',
  'If needed repairs are not addressed, use the Residential Tenancies Branch’s repair information and ask which formal route applies. Follow lawful access arrangements. Do not withhold rent on your own to force a repair.',
  'An urgent danger needs the proper immediate route, not an ordinary app report. For a suspected gas leak or sounding CO alarm, leave the area and call 911 or local emergency services from safety. Use the official emergency guidance; never attempt a repair based on this lesson.'],
 lessons=[
  lesson('Describe what happened, not a guessed cause',
   'A useful repair request says where, what and when. Describe what you noticed. Ask for a next step. Keep a copy. You can be clear without knowing the technical name or blaming anyone.',
   'An observation is something you actually noticed. A diagnosis explains the cause, which may need a qualified person. Keeping those separate makes a request more accurate. A dated record helps follow-up, but a sent message does not prove it was read or the repair completed.',
   'Fictional case: a kitchen cupboard door hangs loose on Monday at 6 pm. The written request is sent at 6:15 pm. A reply proposes Wednesday, 2–4 pm.',
   ['Record the location and observation: “The kitchen cupboard door hangs loose.” Do not invent the cause.',
    'Write when it was noticed and ask when it can be checked. The gap between 6:00 and 6:15 is 15 minutes.',
    'The proposed visit lasts $4-2=2$ hours. Keep the reply and clarify access using the applicable rules; an appointment offer is not a completed repair.'],
   'A repair note is not a reason to try electrical, gas or other unfamiliar repair work. This practice case is an ordinary non-emergency request.'),
  lesson('Follow up when the plan changes',
   'A work shift now overlaps the visit. Ask about another time and get confirmation. Keep the problem and dates clear. If repairs remain unresolved, ask the tenancy service about the next step.',
   'The new availability does not silently cancel an agreed or lawfully notified visit. Communicate and clarify access. For unresolved ordinary repairs, RTB has a formal request route; do not hold back rent on your own. A new immediate danger changes the route entirely: leave danger and use the proper emergency service, rather than waiting for the mentor.',
   'Fictional change: Wednesday work is 2–5 pm. Thursday class is 10 am–noon. The offered alternatives are Thursday 9–11 am and Friday 1–3 pm.',
   ['Wednesday overlaps work. Thursday’s proposed visit overlaps class between 10 and 11 am.',
    'Friday 1–3 pm has no conflict in the stated schedule. Ask to use it and wait for confirmation; it is a proposal until agreed.',
    'Update the record after the visit with what was actually done. If the needed repair is still unresolved, ask RTB about the appropriate next step using the saved facts.'],
   'Do not treat any fixed number of days in a practice calculation as a legal repair deadline. Urgency and circumstances affect the proper response.')],
 labs=[[
  with_context(calculation('repair-time','Read the record','How many minutes passed from noticing the door at 6:00 pm to sending the request at 6:15 pm?',15,'From 6:00 to 6:15 is 15 minutes. This is elapsed time, not a rule about how long anyone must wait.'),grid=REPAIR_LOG),
  with_context(evidence('repair-facts','Choose facts for the request','Which two details belong in the first request?',
   ['The kitchen cupboard door hangs loose.','The problem was noticed on Monday at 6 pm.','A specific internal part definitely failed, though nobody checked it.'],[0,1],
   'Location, observation and time make the request useful without inventing a diagnosis.'),grid=REPAIR_LOG),
  draft_task('repair-plan',dict(title='Write a clear request',task='Write a short fictional message with the location, observation, when it started and a request for the next step. Do not add a real address.',
   example='Hello, the kitchen cupboard door is hanging loose. I noticed it on Monday at 6 pm. Could you arrange to check it and confirm the next step and access arrangements? Thank you.',
   checks=['I stated where and what was observed.','I included the time without guessing the cause.','I asked for a clear next step using fictional details.']))],
 [with_context(calculation('repair-window','Read the proposed alternative','How many hours are in the Friday 1–3 pm visit window?',2,'$3-1=2$ hours. The window still needs confirmation.'),grid=REPAIR_CHANGE),
  with_context(evidence('repair-clash','Choose a workable proposal','Which two statements fit this changed schedule?',
   ['The Thursday option overlaps class.','Friday 1–3 pm has no stated conflict and can be proposed.','A new shift automatically cancels the landlord’s visit without communication.'],[0,1],
   'Check all the time windows, then communicate. A proposal is not yet confirmation.'),grid=REPAIR_CHANGE),
  draft_task('repair-revise',dict(task='Write a clear request.',rework='Write a follow-up about the Wednesday clash. Propose Friday, ask for confirmation and state how you will keep track if the repair remains unresolved.',
   example='My new Wednesday shift overlaps the offered visit. Could we arrange Friday 1–3 pm instead? Please confirm the time and access arrangements. I will keep the request and reply, record what is repaired and ask RTB about the next step if the needed repair remains unresolved.',
   checks=['I explained the changed availability and a fitting alternative.','I requested confirmation instead of assuming cancellation.','I kept a record and chose a proper follow-up route.']),True)]],
 practice=[
  q('Which note describes an observation?','Water appears under the sink when the tap runs.','A hidden valve definitely failed without anyone checking.','The cause must be the neighbour.','Describe what can be observed before assigning a cause.'),
  number('A fictional issue is noticed at 7:10 pm and reported at 7:25 pm. How many minutes pass?',15,'From 7:10 to 7:25 is 15 minutes. This is only a time calculation.'),
  q('A request has been sent. What is known?','The message was sent; receipt and repair still need checking.','The repair is complete automatically.','A legal ruling was issued.','Track sent, acknowledged and completed separately.'),
  number('A proposed visit runs from 9 am to noon. How many hours is that?',3,'Noon is 12:00; $12-9=3$ hours.'),
  q('A work shift conflicts with a proposed repair time. What helps?','Contact the landlord, propose a workable time and clarify access.','Assume silence communicates the change.','Delete the original repair record.','A changed plan needs communication and confirmation.'),
  q('Needed ordinary repairs remain unresolved. What is an appropriate route?','Ask RTB about its repair process, keeping the records.','Withhold rent on your own to force action.','Treat Stepstone Steps as a legal order.','Use the proper tenancy process rather than an invented remedy.')],
 check=[
  number('A fictional message is sent at 8:05 am and acknowledged at 8:20 am. How many minutes pass?',15,'From 8:05 to 8:20 is 15 minutes.'),
  number('A proposed appointment is from 1 pm to 4 pm. How many hours is the window?',3,'$4-1=3$ hours.'),
  q('Which first request gives useful evidence without guessing?','The bedroom window will not close; noticed Tuesday evening.','Every part of the building is definitely broken.','The landlord must already know everything.','Give a location, observation and time.'),
  number('A fictional record starts Monday and is reviewed Friday of the same week. How many days elapsed?',4,'Tuesday is one day later, Wednesday two, Thursday three and Friday four. This is not a legal deadline.'),
  q('Why separate observation from diagnosis?','The cause can need checking even when the symptom is clear.','Only a technical diagnosis permits asking for help.','A guessed cause is always stronger evidence.','Clear observations let the appropriate person investigate.'),
  q('What should be kept after making a repair request?','A private copy of the request and any response.','Only a public post with the home address.','Nothing until an argument starts.','A record supports accurate follow-up.'),
  q('A proposed visit clashes with class. What should the follow-up include?','The clash, a possible alternative and a request for confirmation.','An unexplained refusal with no communication.','A statement that the repair already happened.','Make the changed plan understandable.'),
  q('Why is a proposed new visit different from a confirmed one?','The other party has not yet agreed to the proposal.','Typing a time automatically changes every schedule.','Confirmation is never useful.','Keep pending and agreed arrangements distinct.'),
  q('A CO alarm sounds. Which route fits the official emergency guidance?','Leave the area and call emergency services from safety.','Wait for a reply to a routine repair message.','Remove the alarm and continue the lesson.','An immediate hazard needs immediate appropriate help.'),
  q('Why should a renter not hold back rent on their own over repairs?','RTB has a process; self-directed withholding can create another tenancy problem.','Rent payment guarantees every repair is already complete.','Only a quiz decides the legal remedy.','Ask the tenancy service about the actual situation.'),
  q('A worker visited but the reported problem remains. What is a useful update?','Record what happened and what is still wrong, then use the appropriate follow-up route.','Mark the issue fixed because someone arrived.','Invent a repair detail to close the record.','A visit and a completed repair are different facts.'),
  q('Why is four elapsed days in a question not a universal repair deadline?','Required responses depend on urgency, circumstances and applicable rules.','A made-up exercise changes rental law.','All repair issues have exactly the same urgency.','Separate arithmetic practice from an individual legal decision.')],
 reflection='Explain the revised repair message, what remains unconfirmed and when a different help route would be needed.'
)

MODULES = [RENTAL, BILLS, MEALS, CARE_MODULE, REPAIR]
# The existing server draws two from each skill pool. This assignment includes
# both lesson ideas in every possible six-question selection.
CHECK_SKILLS = ['calculate','calculate','apply','calculate','reason','apply',
                'apply','reason','apply','reason','apply','reason']
for module in MODULES:
    assert len(module['check']) == len(CHECK_SKILLS)
    for question,skill in zip(module['check'],CHECK_SKILLS):
        question['skill']=skill

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)
