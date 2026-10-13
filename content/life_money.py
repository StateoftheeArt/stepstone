"""Money and tax navigation, using the existing service-guide mission flow.

All people, amounts, fees and extracts below are fictional teaching examples.
Primary sources checked 2026-09-24; no real return, account or benefit claim is
submitted or calculated. Existing pay/budget lessons remain optional preparation.
"""
from digital import lesson, q
from life_services import attach_guides, calculation, evidence, number
from practical_missions import draft_task

CHECKED = '2026-09-24'
SOURCES = {
 'bank-open': ('FCAC — opening an account, ID and help', 'https://www.canada.ca/en/financial-consumer-agency/services/banking/opening-bank-account.html'),
 'bank-fees': ('FCAC — compare chequing-account costs', 'https://www.canada.ca/en/financial-consumer-agency/services/banking/bank-accounts/chequing-accounts.html'),
 'bank-free': ('FCAC — low-cost and no-cost accounts', 'https://www.canada.ca/en/financial-consumer-agency/services/banking/bank-accounts/low-cost-no-cost.html'),
 'tax-ready': ('CRA — prepare documents and check dates', 'https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/get-ready-taxes.html'),
 'tax-terms': ('CRA — tax words explained', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/educational-programs/common-terms.html'),
 'tax-benefits': ('CRA — filing with modest or no income and benefit help', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/segments/modest-income-individuals.html'),
 'tax-file': ('CRA — ways to file a return', 'https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/how-file.html'),
 'tax-t4': ('CRA — understand a T4 slip', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/tax-slips/understand-your-tax-slips/t4-slips/t4-statement-remuneration-paid.html'),
 'tax-missing': ('CRA — get a missing slip', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/tax-slips/a-copy-your-tax-slips.html'),
 'tax-clinic': ('CRA — find a free tax clinic and check eligibility', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program/need-a-hand-complete-your-tax-return.html'),
 'tax-noa': ('CRA — read a notice of assessment', 'https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/after-you-file/noa-nor.html'),
 'tax-after': ('CRA — learn about refunds and balances', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/educational-programs/after-sending-tax-return.html'),
 'tax-change': ('CRA — correct a filed return', 'https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax/after-you-file/change-return.html'),
 'tax-pay': ('CRA — arrange to pay over time', 'https://www.canada.ca/en/revenue-agency/services/payments/payments-cra/payment-arrangements.html'),
 'tax-records': ('CRA — keep tax records', 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/long-should-you-keep-your-income-tax-records.html'),
 'tax-help': ('CRA — contact the right team', 'https://www.canada.ca/en/revenue-agency/corporate/contact-information.html'),
}

BANK = dict(
 id='life-bank-account',title='Choose a bank account',minutes=25,
 goal='Compare real costs and prepare the questions needed to open an account.',
 why='A low monthly fee can still come with extra costs. Learn to spot them before you agree.',
 objectives=['Compare the costs','Check the conditions','Explain your choice'],
 needs=['math-budget','math-prices','life-photo-id'],sources=['bank-fees','bank-free','bank-open'],help='bank-open',
 practiceNotice='Use fictional fees and details. Stepstone does not open an account or move money.',
 nextSteps=['List how you would use an account: paying bills, card purchases, cash and help in person.',
  'Use FCAC’s account pages to compare the monthly fee, included services and extra charges. Ask about no-cost options and their conditions.',
  'Contact the institution through its official website or branch. Check accepted ID and any age or consent requirements before applying. Ask what options exist if a required person or document is unavailable. Keep the agreement privately.'],
 lessons=[
  lesson('Compare the whole cost',
   'CAD means Canadian dollars. A bank account holds money. A chequing account is often used for everyday payments. A transaction is one action, such as a payment. Compare the monthly fee and the extra charges together.',
   'Compare the same month and the same use. A package may include some transactions and charge for more. Access matters too: an account is less useful if you cannot use its cash machines or get the help you need. The cheapest headline price does not settle every choice.',
   'Made-up offers: A costs CAD 5 a month and includes 10 payments. Each extra payment costs CAD 2. B costs CAD 9 and includes 20. Lee makes 15.',
   ['A has $15-10=5$ extra payments. Its cost is $5+5\\times2=15$ CAD.',
    'B includes all 15 payments, so its cost is 9 CAD. B is $15-9=6$ CAD cheaper for this use.',
    'Check that the needed payments and access are included. These are fictional offers, not advertised accounts.'],
   'A low monthly fee does not mean every service is free.'),
  lesson('Check the conditions before agreeing',
   'An offer may depend on age, student status or a minimum balance. Ask what happens when that condition changes. Check the ID and permission requirements with the institution. Do not guess them.',
   'The Financial Consumer Agency of Canada (FCAC) lists low-cost and no-cost options, including eligibility for people aged 18 or younger and students at participating institutions. Extra services can still cost money. A fee waiver means a fee is removed only while its conditions hold. Bank access and youth-account arrangements need separate checking; do not assume a parent is available.',
   'New made-up detail: B costs CAD 9 only while Lee is a student. Later it costs CAD 16. Lee’s student status ends soon.',
   ['For the same 15 payments, A still costs 15 CAD. After the discount ends, B costs 16 CAD.',
    'Now B costs $16-15=1$ CAD more. The earlier choice needs another look.',
    'Lee asks when the change starts, which no-cost options apply, and which ID and consent arrangements are accepted.'],
   'Opening a deposit account is not the same as being approved for a loan or credit card.')],
 labs=[[
  calculation('bank-cost','Count the full fee','Fictional A: CAD 4 monthly, 12 payments included, CAD 1 for each extra payment. Sam makes 18. What is the total cost in CAD?',10,'Six extra payments cost 6 CAD. $4+6=10$ CAD in total.'),
  evidence('bank-evidence','Choose useful comparison details','Which details help compare accounts for Sam’s 18 monthly payments?',
   ['The number and type of included payments, and extra charges.','Whether Sam can use the needed cash machines and support.','The colour of the bank’s logo.'],[0,1],'Cost and access affect whether the account fits the job.'),
  draft_task('bank-plan',dict(title='Explain Sam’s choice',task='Compare fictional A at CAD 10 and B at CAD 7 for this month. Write which costs less, why, and one condition to ask about.',
   example='For 18 included-type payments, B costs 7 CAD while A costs 10 CAD. B is cheaper for this month. Sam should ask whether the price depends on student status.',
   checks=['I compared the same use and included the extra fees.','I named a condition or access need to check.','I used fictional details, without banking numbers or passwords.']))],
 [evidence('bank-change','A discount is ending','Sam’s student status ends soon. What must the revised comparison include?',
   ['The date B changes from CAD 7 to CAD 14.','Whether a different no-cost option fits Sam’s situation.','An assumption that all youth offers last forever.'],[0,1],'A changed condition can change the cost. Check alternatives before deciding.'),
  calculation('bank-difference','Compare after the change','After the discount, B costs CAD 14. A costs CAD 10 for the same use. How much more does B cost, in CAD?',4,'$14-10=4$ CAD more for the same month and use.'),
  draft_task('bank-revise',dict(task='Explain Sam’s choice.',rework='Update your plan for B changing to CAD 14. Sam also cannot bring the person they expected to help. Add a question about accepted ID and age or consent arrangements, without assuming the account cannot be opened.',
   example='After the discount, A costs 10 CAD and B costs 14 CAD for this use. Sam should compare again and ask about no-cost options. Sam can ask the institution which ID and youth-account arrangements apply if the expected helper is unavailable.',
   checks=['I updated the cost comparison after the discount ends.','I asked about the missing support and requirements without inventing a rule.','I explained a choice instead of claiming an account was opened.']),True)]],
 practice=[
  number('Fictional offer: CAD 3 monthly plus two extra payments at CAD 1 each. What is the total cost in CAD?',5,'$3+2\\times1=5$ CAD.'),
  q('One offer costs CAD 6 for all 20 payments. Another costs CAD 4 plus CAD 1 for each payment above 12. For 20 payments, which costs less?','The CAD 6 offer.','The CAD 4 offer because its headline is lower.','Both cost the same.','The second costs $4+(20-12)=12$ CAD. Compare the total for the same use.'),
  q('A lower-cost account has no usable cash machine nearby. What should the comparison include?','The access need and any extra cash-withdrawal costs.','Only the logo.','Only the monthly price, regardless of access.','Cost and practical access both matter.'),
  q('An offer says the monthly fee is waived at a minimum balance. What should you ask?','How the balance condition works and the fee if it is not met.','Whether waived means free forever.','Whether the bank lends that balance automatically.','A waiver has conditions; understand them before relying on it.'),
  q('A 17-year-old wants to explore lower-cost banking. What is a useful next step?','Ask about no-cost options and the institution’s ID and age arrangements.','Assume every service at every bank is free.','Apply for a loan instead of comparing accounts.','No-cost options have terms. Check what applies to this person and institution.'),
  q('The expected adult helper is unavailable. What should the learner ask?','What accepted arrangements or help routes are available for this situation?','How to forge a signature.','Whether app Steps replace identity checks.','A missing helper is a question for the institution, not a reason to invent consent.')],
 check=[
  number('Fictional account: CAD 5 monthly, 10 payments included, CAD 2 for each extra payment. Ren makes 13. Total cost in CAD?',11,'$13-10=3$ extras; $5+3\\times2=11$ CAD.'),
  q('Fictional C costs CAD 9 for 22 payments. D costs CAD 3 plus CAD 1 for each payment above 10. At 22 payments, which costs less?','C, at CAD 9.','D, at CAD 3 total.','They both cost CAD 15.','D costs $3+12=15$ CAD. The relevant comparison is 9 versus 15.'),
  q('Dev needs teller help for bills. An offer lists self-service payments. What must Dev check?','Whether teller help is included and any extra fee.','Whether the card has an attractive pattern.','Whether self-service always means free teller help.','The type of included transaction matters as well as the number.'),
  number('A made-up monthly fee falls from CAD 8 to CAD 5. How much is saved over 12 months, if all other costs stay the same?',36,'$(8-5)\\times12=36$ CAD saved.'),
  q('Which comparison is fair for two offers?','Use the same likely payments and access needs for both.','Use 3 payments for one and 30 for the other without saying so.','Compare only the biggest printed number.','Hold the use constant so the different prices mean something.'),
  q('A fee list says transfers cost extra. What does that change?','The total cost if the person needs those transfers.','Nothing, because there is already a monthly fee.','The person’s date of birth.','Add the costs of the services actually needed.'),
  q('A youth discount ends next month. Which plan uses the new information?','Compare the next-month price and ask about other eligible options.','Treat the discounted price as permanent.','Open a credit card automatically.','Recheck a choice when its price conditions change.'),
  q('Someone has no job. Which statement follows FCAC’s account-opening guidance?','No job alone does not remove the right to open an account; identity and other applicable requirements still matter.','Every bank account requires an employer.','No identification can be required.','Account-opening rights and identity verification are separate questions.'),
  number('A fictional waived fee becomes CAD 9. An alternative costs CAD 4 for the same use. How much more is the first account per month?',5,'$9-4=5$ CAD more per month.'),
  q('A person cannot provide the first document they planned to use. What should they do?','Ask about accepted identification routes using the official guidance.','Create a fake document image.','Assume any screenshot must be accepted.','There are identification routes to check; do not invent or alter evidence.'),
  q('An account offers no monthly fee. Which question still matters?','Which services or extra transactions have charges?','Which fees can safely be ignored?','Which prize is guaranteed for signing up?','No monthly fee and no possible fees are different claims.'),
  q('Jo finishes this account-comparison guide. What can Jo show?','A reasoned practice choice and questions for the institution.','An opened bank account.','Guaranteed credit approval.','A practice result is evidence of learning, not a banking action.')],
 reflection='Use fictional details. Explain the revised choice, one calculation and one question Sam still needs answered.'
)

TAX_PREP = dict(
 id='life-tax-prep',title='Get ready to file taxes',minutes=30,
 goal='Sort the right records and choose a workable way to file a return.',
 why='Taxes feel less mysterious when you separate the papers, the choices and the next small step.',
 objectives=['Read the records','Choose a filing route','Fix a missing piece'],
 needs=['math-pay','digital-1','life-sin'],sources=['tax-ready','tax-t4','tax-terms','tax-missing','tax-file','tax-clinic'],help='tax-clinic',
 nextSteps=['Open CRA’s preparation page. Check the tax year, who should file, and both the filing and payment dates for the person’s situation.',
  'Gather that year’s income records and relevant receipts privately. Compare slips by issuer and year; request missing or corrected records. Use CRA’s missing-slip guidance if time is short.',
  'Choose certified tax software, paper, or suitable help from CRA’s filing page. A free clinic may fit a modest income and simple situation; ask the clinic first. Review the return, send it through that route and keep the confirmation.'],
 lessons=[
  lesson('A tax return puts the year together',
   'A return is the information you send the Canada Revenue Agency (CRA) about a tax year. CAD means Canadian dollars. A refund is money returned after the calculation. A T4 is an employer’s yearly slip. It is different from one payday’s payslip.',
   'Read the labels before doing arithmetic. T4 box 14 reports employment income; box 22 reports income tax already deducted. A deduction reduces income used in the tax calculation. A tax credit reduces tax, under its own rules. Neither word means every expense is refunded. The full return can include other income and claims.',
   'Fictional records for one year: Lee has two different jobs. T4 A box 14: CAD 6,000; box 22: CAD 150. T4 B box 14: CAD 4,000; box 22: CAD 100.',
   ['Match the person, tax year and employer. The two slips cover different jobs, not duplicate copies.',
    'For these records, employment income totals $6000+4000=10000$ CAD. Tax already deducted totals $150+100=250$ CAD.',
    'Keep those labels separate. These two totals alone do not calculate Lee’s refund or final tax.'],
   'Do not count a downloaded copy and a mailed copy of the same slip as two incomes.'),
  lesson('Choose help and handle a missing slip',
   'You can file with certified software, on paper, or with suitable help. A free clinic may help people with modest income and a simple situation. Ask about eligibility, access and what to bring.',
   'Preparing, saving and sending are separate steps. Choose the right tax year and provincial package, then check current filing and payment dates. If a slip is missing, ask its issuer. CRA also explains what to do if it cannot arrive in time. A missing slip is not a reason to hide income or guess a number from memory.',
   'Fictional change: Lee has only a phone and is still missing the second employer’s slip.',
   ['Lee asks that employer for the correct year’s slip and gathers the available pay records.',
    'Lee asks a clinic whether the situation fits and whether phone, in-person or other help is available.',
    'Lee checks the real deadlines and missing-slip instructions. After filing, Lee keeps the confirmation and supporting records privately.'],
   'Saving a draft in software or Stepstone does not mean CRA received a return.')],
 labs=[[
  evidence('tax-labels','Read the slip labels','Fictional T4: box 14 employment income CAD 6,000; box 22 income tax deducted CAD 150. Which statements match?',
   ['CAD 6,000 is the employment-income amount on this slip.','CAD 150 is tax already deducted, not a promised refund.','CAD 6,000 must be the amount deposited on one payday.'],[0,1],'A box label tells you what the number measures.'),
  calculation('tax-total','Combine different jobs','Two different fictional employers report CAD 6,000 and CAD 4,000 of employment income for the same year. What is the combined amount in CAD?',10000,'$6000+4000=10000$ CAD. Combine distinct jobs; do not count duplicate copies.'),
  draft_task('tax-plan',dict(title='Make Lee’s filing plan',task='Write which year and records Lee should check, a possible filing route, and how Lee would know the return was sent. Keep all details fictional.',
   example='Lee will check the same tax year on both employers’ slips and keep the income and deducted-tax labels separate. Lee can ask a free clinic whether the situation fits. After sending the return, Lee should keep the filing confirmation.',
   checks=['I named the year and distinct income records to check.','I named a filing route and a condition to confirm.','I separated preparing from sending and used no real tax details.']))],
 [evidence('tax-missing','The second slip is missing','Lee has only a phone and lacks the second slip. Which steps keep the plan workable?',
   ['Ask the employer for the slip and gather available pay records.','Ask a clinic about access and check CRA’s deadlines and missing-slip guidance.','Leave the second job out because the paper is missing.'],[0,1],'Keep the income in the plan and seek the correct record or official fallback process.'),
  draft_task('tax-revise',dict(task='Make Lee’s filing plan.',rework='Revise your plan for the missing second slip and phone-only access. Include who to ask, what to gather, and what to check if the slip will not arrive before the deadline.',
   example='Lee will contact the second employer and keep the available pay records. Lee will ask a clinic about phone or in-person help, confirm whether the situation fits, and check CRA’s missing-slip instructions and current filing/payment dates.',
   checks=['I kept both jobs in the plan and asked for the missing record.','I included a help route Lee can ask about with only a phone.','I checked current dates and official fallback guidance instead of inventing figures.']),True)]],
 practice=[
  q('A yearly T4 lists employment income and income tax deducted. Which amount is already sent from pay as tax?','The amount labelled income tax deducted.','All employment income.','The balance of the person’s chequing account.','Use the label; earnings and tax already deducted are different amounts.'),
  number('Two different fictional jobs for one year show employment income of CAD 3,000 and CAD 2,000. What is their combined employment income in CAD?',5000,'$3000+2000=5000$ CAD. This is an income total, not a tax calculation.'),
  q('A mailed T4 and a downloaded T4 are identical copies from the same employer and year. How should they be treated?','As one slip with a duplicate copy.','As two jobs to add together.','As evidence that no income needs reporting.','Check issuer and year so a copy is not counted twice.'),
  q('A person cannot afford paid help and has a simple situation. What should they explore?','Whether a free tax clinic can help and what its conditions are.','A guaranteed refund from any social-media account.','A rule that filing is impossible without paid software.','Free-clinic eligibility and availability need checking with the clinic.'),
  q('A slip is missing close to filing time. Which plan fits?','Request it, gather records and use CRA’s missing-slip instructions.','Invent the amount from memory.','Leave that income out automatically.','There is an official missing-slip process. Ask for help applying it to the situation.'),
  q('A software screen says saved draft. What is still unconfirmed?','Whether the return was sent and a filing confirmation received.','Whether the screen was drawn with pixels.','Whether Stepstone Steps were earned.','A saved draft and a filed return are different states.')],
 check=[
  q('Fictional T4: employment income CAD 8,200; income tax deducted CAD 240. What does CAD 240 represent?','Tax already deducted from employment pay.','A guaranteed refund.','Total employment income.','Read the deducted-tax label without turning it into a refund promise.'),
  number('Two distinct employers’ fictional slips for one year show employment income CAD 7,200 and CAD 1,800. Combined income in CAD?',9000,'$7200+1800=9000$ CAD for these two jobs.'),
  number('A fictional folder has 7 slips: 4 for the year being filed and 3 for an earlier year. How many belong in this year’s group?',4,'Use the year labels: $7-3=4$ slips belong in this group. Keep other years separate.'),
  q('Which describes a tax deduction compared with a tax credit?','A deduction reduces income used in calculating tax; a credit reduces tax under its rules.','Both always repay the full price of anything bought.','A credit is the same thing as a bank loan.','The effect depends on the type and rules. A receipt alone does not guarantee a claim.'),
  number('Fictional tax-deducted amounts from two different jobs are CAD 180 and CAD 70. What is their total in CAD?',250,'$180+70=250$ CAD already deducted. The final tax result needs the whole return.'),
  q('A payslip and the employer’s annual T4 cover some of the same pay. What should you avoid?','Adding the annual income and every payslip again as separate employment income.','Using pay records to check the annual slip.','Checking the employer’s name.','Supporting records help check a total; they are not automatically extra income.'),
  q('A learner in Manitoba finds a tax package for another province. What must be checked?','The correct year and provincial package for the person’s tax situation.','Whether the cover is colourful.','Whether any province’s forms are always interchangeable.','Use CRA’s package instructions for the year and relevant residence situation.'),
  q('A clinic offers free help for modest income and simple situations. Is a place guaranteed just by finishing this guide?','No; ask the clinic about eligibility, scope and availability.','Yes; app points make every return eligible.','Yes; the app has booked an appointment.','The clinic, not Stepstone, confirms whether and how it can help.'),
  q('A missing T4 is not yet in a CRA account. Which step still makes sense?','Ask the employer or issuer for a copy.','Assume the income never existed.','Use another person’s slip.','CRA cannot show a slip it has not received; the issuer is another route.'),
  q('Why check filing and payment dates separately?','They can be different for some situations, and both matter.','Only the later date ever matters.','The app chooses both dates.','Use the current CRA dates for the person’s situation; do not assume they match.'),
  q('A tax helper asks for documents through an unfamiliar message. What should you do before sharing?','Verify the helper and the secure submission route independently.','Post the documents in a public comment.','Share the CRA password so anyone can try it.','Prepare privately and confirm the recipient and method before sharing real records.'),
  q('The return was sent through a filing route. What should the person keep?','The confirmation, return copy and supporting records privately.','Only the app’s quiz badge.','Nothing, because sending prevents any later question.','Retained records support follow-up. The app’s check is not a filing receipt.')],
 reflection='Using Lee’s fictional case, explain the revised filing plan and why a missing slip does not mean missing income.'
)

TAX_RESULT = dict(
 id='life-tax-result',title='Understand your tax result',minutes=30,
 goal='Read a fictional tax result and choose a useful next step.',
 why='A tax letter is easier to handle when you know what the labels mean and who can help.',
 objectives=['Read the result','Check what changed','Plan the next step'],
 needs=['life-tax-prep','math-budget','reading-6'],sources=['tax-noa','tax-after','tax-change','tax-pay','tax-records','tax-benefits','tax-help'],help='tax-help',
 nextSteps=['Keep the filing confirmation. When the notice arrives, check the tax year, the account summary and any explanation of changes against your records.',
  'Use CRA’s help page if something is unclear. For missing or incorrect return information, follow the change-return route after assessment. If the amount is unaffordable, ask CRA about payment arrangements.',
  'Keep tax records privately for at least six years, checking any longer-retention rules that apply. Review CRA’s current benefits information and yearly filing requirements; a tax refund does not decide every benefit payment.'],
 lessons=[
  lesson('Refund, owing or zero?',
   'The Canada Revenue Agency (CRA) sends a notice of assessment after processing a return. CAD means Canadian dollars. A refund means money back. A balance owing means money to pay. Nil means zero. Read the words beside the amount, not just the number.',
   'Compare the total payable with total credits. Payable is the calculated amount charged; credits include amounts already paid or deducted and other applicable credits. More credits than payable can give a refund. Fewer can leave a balance owing. We use supplied totals here, not a formula for calculating anyone’s real tax.',
   'Fictional teaching summary: total payable CAD 400; total credits CAD 650. No other balance or adjustment is included in this example.',
   ['Credits exceed payable. The difference is $650-400=250$ CAD back in this example.',
    'If payable were 700 CAD with the same 650 CAD credits, $700-650=50$ CAD would be owing.',
    'If both were 650 CAD, the difference would be zero. Real notices may also show other balances or changes.'],
   'A refund is not your total yearly pay, and tax already deducted is not automatically the final tax bill.'),
  lesson('Read the change and choose an action',
   'Check the year, amount and explanation on the notice. If something is wrong, use the official correction route. If you cannot pay, ask CRA about arrangements. Do not ignore a letter you do not understand.',
   'A question can be specific without exposing documents in this app. Name the line or change and ask what evidence is needed. For a change to your filed information, wait for the notice of assessment and use CRA’s change-return process. Keep records. Benefits have their own conditions and notices; yearly filing can matter even when there is little or no income.',
   'Fictional change: Ren expected CAD 250 back. The notice now says CAD 40 owing and explains that a claimed credit was not allowed.',
   ['Ren compares the explanation with the return and supporting records. A different result is a reason to investigate, not proof that Ren did something dishonest.',
    'Ren asks CRA which evidence or correction route fits. If Ren cannot pay, Ren asks about a payment arrangement; a plan in this app is not an agreement with CRA.',
    'Ren keeps the documents and separately checks benefit information. Ren does not budget a benefit just because a quiz or return is complete.'],
   'A payment arrangement is not automatic debt cancellation. Check current terms and any interest that continues.')],
 labs=[[
  calculation('result-amount','Find the difference','Fictional summary: payable CAD 400, credits CAD 650, no other balances. What is the refund amount in CAD?',250,'Credits are larger: $650-400=250$ CAD back in this example.'),
  evidence('result-label','Read the direction','Which statements describe the fictional CAD 250 refund above?',
   ['Credits exceed payable in the supplied totals.','The example shows money back, not an amount Ren must pay.','Every person who files receives CAD 250.'],[0,1],'The direction comes from these totals. Another person can have a different result.'),
  draft_task('result-plan',dict(title='Explain Ren’s result',task='Explain the fictional CAD 250 refund, the comparison behind it, and what Ren should read when the real notice arrives.',
   example='Credits of 650 CAD exceed payable of 400 CAD by 250 CAD in this practice case. Ren should check the year, account summary and any explanation of changes on the notice.',
   checks=['I explained the direction and difference using the supplied totals.','I named details to check on the notice.','I kept real notices, numbers and identifiers out of my answer.']))],
 [evidence('result-change','The result is different','The fictional notice says CAD 40 owing after a credit was not allowed. Which next steps are useful?',
   ['Compare the explanation with the return and supporting evidence.','Ask CRA about the right correction route or payment help, depending on the issue.','Hide the notice because it differs from the estimate.'],[0,1],'Separate understanding or correcting the result from arranging an affordable way to pay.'),
  draft_task('result-revise',dict(task='Explain Ren’s result.',rework='Revise your plan for CAD 40 owing after a credit was not allowed. Write one question about the evidence or correction, and one about help if Ren cannot pay now. Do not promise a benefit or debt cancellation.',
   example='Ren will read why the credit was not allowed and compare the records. Ren can ask CRA what evidence or correction process applies. If Ren cannot pay now, Ren can ask about a payment arrangement and its terms. Benefit eligibility is a separate check.',
   checks=['I acknowledged the changed result and looked for its explanation.','I separated correcting an error from asking for payment help.','I made no promise of a refund, benefit or cancelled debt.']),True)]],
 practice=[
  number('Fictional summary: payable CAD 300, credits CAD 500, no other balances. What is the refund in CAD?',200,'$500-300=200$ CAD back in this example.'),
  q('A notice says amount due CAD 75. What does due mean here?','The notice shows an amount to pay.','A guaranteed payment coming to you.','The person’s total yearly earnings.','The label gives the direction of the money.'),
  q('Payable and credits are equal in a simplified example. What is their difference?','Zero; neither refund nor amount owing from those totals.','A refund equal to all income.','An automatic benefit payment.','Equal totals cancel in this calculation.'),
  q('A notice differs from the return estimate. Where should you look?','The notice’s explanation of changes and your supporting records.','Only the largest number on the page.','A stranger’s screenshot of a different return.','Compare the reasons and evidence for this person and year.'),
  q('A person cannot pay the full balance now. What can they explore?','CRA’s payment-arrangement route and its terms.','An assumption that silence cancels the balance.','Changing income to make the bill disappear.','Ask about options using accurate information; an arrangement is not automatic forgiveness.'),
  q('Someone had very little income. Why check filing and benefit information anyway?','Yearly filing can be needed for benefits they may qualify for.','Filing guarantees every benefit to everyone.','A quiz score decides the benefit amount.','Benefits have conditions; check the current rules instead of assuming no income means no reason to file.')],
 check=[
  number('Fictional summary: payable CAD 480, credits CAD 700, no other balances. Refund amount in CAD?',220,'$700-480=220$ CAD back in this example.'),
  number('Fictional summary: payable CAD 900, credits CAD 640, no other balances. Amount owing in CAD?',260,'$900-640=260$ CAD owing in this example.'),
  q('A notice’s account summary says balance nil. What does nil mean?','Zero for the balance shown.','A guaranteed refund of all tax deducted.','No return has ever been filed.','Nil is a word for zero; read it with the account summary.'),
  q('Which record shows CRA’s assessment after it processes a return?','A notice of assessment.','A Stepstone practice draft.','A banking advertisement.','The assessment notice is different from the preparation or practice record.'),
  q('Which conclusion can you draw from CAD 500 labelled tax deducted on a T4 alone?','That amount was deducted; the full return is still needed to determine the result.','The final refund must be CAD 500.','No tax return can be required.','One deducted amount does not show the complete tax calculation.'),
  number('In a fictional summary, payable and credits are both CAD 360. What is the difference in CAD?',0,'$360-360=0$ CAD.'),
  q('An already-assessed return left out a slip. What should be checked?','CRA’s process for changing the assessed return.','How to send an unchanged duplicate as a brand-new return.','How to delete the original slip.','Use the correction route for missing information in an assessed return.'),
  q('The estimate said refund, but the notice says owing. What is the strongest first step?','Read the explanation and compare the same year’s records.','Assume the person is dishonest.','Assume a friend’s result overrides this notice.','A changed result needs evidence and explanation, not blame.'),
  q('A proposed repayment plan was written in this app. What is true?','CRA still needs to confirm any actual payment arrangement.','The debt has been cancelled.','A bank transfer has been sent.','An app draft is not an accepted arrangement or a payment.'),
  q('Why keep the return, receipts and notices after filing?','CRA may ask for evidence later; follow its retention guidance.','Keeping them guarantees a refund.','They replace every future return.','Keep records privately for at least six years and check any rules requiring longer.'),
  q('A filed return shows no refund. Does that alone settle every benefit?','No; benefits have separate conditions and information to check.','Yes; zero refund always means zero benefits.','Yes; it guarantees the same benefit for everyone.','Tax result and benefit eligibility are related but different questions.'),
  q('A payment arrangement looks possible. What still needs checking?','The agreed amounts, dates and whether interest continues.','Only the colour of the website.','Whether the app can promise all charges are waived.','Get the actual terms from CRA; do not treat a possibility as an approved agreement.')],
 reflection='Using Ren’s fictional notice, explain what changed, which records to compare and how to ask for the next useful help.'
)

MODULES = [BANK, TAX_PREP, TAX_RESULT]

# Deliberate assessment coverage. The unchanged server draws two from each
# skill. These pools guarantee at least one question from each lesson while
# retaining more than one possible six-question set.
CHECK_SKILLS = {
 'life-bank-account': ['calculate','calculate','apply','calculate','reason','apply','apply','reason','calculate','apply','reason','reason'],
 'life-tax-prep': ['apply','calculate','calculate','reason','calculate','apply','apply','reason','apply','reason','apply','reason'],
 'life-tax-result': ['calculate','calculate','apply','apply','reason','calculate','apply','reason','reason','apply','reason','reason'],
}
for module in MODULES:
    assert len(module['check']) == len(CHECK_SKILLS[module['id']])
    for question, skill in zip(module['check'],CHECK_SKILLS[module['id']]):
        question['skill'] = skill

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)
