"""Manitoba service navigation: original practice cases, not application forms.

Official sources were read on 2026-09-24. These lessons teach a process; only
the service can confirm eligibility, acceptable documents and an application.
The shared installer also supports later batches without adding a second flow.
"""
from digital import lesson, q
from math_missions import task
from practical_missions import install, evidence_task, draft_task

CHECKED = '2026-09-24'
SOURCES = {
 'health-register': ('Manitoba Health — registration', 'https://www.gov.mb.ca/health/mhsip/registration.html'),
 'health-eligibility': ('Manitoba Health — who may qualify', 'https://www.gov.mb.ca/health/mhsip/eligibility.html'),
 'health-update': ('Manitoba Health — updates and replacements', 'https://www.gov.mb.ca/health/mhsip/updatehealthcard.html'),
 'health-help': ('Manitoba Health — registration help', 'https://www.gov.mb.ca/health/mhsip/contact-info.html'),
 'id-apply': ('MPI — Manitoba Identification Card', 'https://www.mpi.mb.ca/how-to-apply-for-an-identification-card/'),
 'id-documents': ('MPI — identity documents and combinations', 'https://www.mpi.mb.ca/establishing-your-identity/'),
 'id-help': ('MPI — ask about your situation', 'https://www.mpi.mb.ca/contact-us/'),
 'sin-apply': ('Service Canada — choose a SIN application route', 'https://www.canada.ca/en/employment-social-development/services/sin/apply.html'),
 'sin-documents': ('Service Canada — documents for a SIN', 'https://www.canada.ca/en/employment-social-development/services/sin/required-documents.html'),
 'sin-protect': ('Service Canada — when to share your SIN', 'https://www.canada.ca/en/employment-social-development/services/sin/protection.html'),
 'sin-help': ('Service Canada — SIN program help', 'https://www.canada.ca/en/employment-social-development/corporate/contact/sin.html'),
}

def evidence(ident, title, prompt, lines, answer, why):
    return evidence_task(ident,dict(prompt=prompt,lines=lines,answer=answer,why=why),title)

def number(prompt, answer, why):
    return dict(kind='number',prompt=prompt,answer=answer,explanation=why,hint='Use the numbers in this made-up case. Label what you are counting.')

def calculation(ident, title, prompt, answer, why):
    return task(ident,title,prompt,'number','Use only the amounts in the practice case. Write the calculation, then enter the number.',why,answer=answer)

def table(caption, columns, rows):
    return dict(caption=caption,columns=columns,rows=rows)

def with_context(item, *, grid=None, sign=None):
    if grid:item['table']=grid
    if sign:item['sign']=sign
    return item

HEALTH = dict(
 id='life-health-card',title='Sort out a health card',goal='Choose the right health-card route and prepare a question for help.',
 why='A move or lost card is easier to handle when you know which job you are trying to do. Practise with a fictional person first.',
 objectives=['Choose the route','Handle a change','Make a useful plan'],
 needs=['reading-1','writing-6'],sources=['health-register','health-eligibility','health-update','health-help'],help='health-help',
 nextSteps=['Name the job: first registration, a change, or a replacement.',
  'Use the matching Manitoba Health page. Check eligibility and the current document list for that route.',
  'If a requirement is unclear, contact registration staff before submitting. Use the official service for real documents; keep your receipt privately.'],
 lessons=[
  lesson('Name the job first',
   'A health card connects you with health coverage. First registration, changing details and replacing a lost card are different jobs. Read the situation before choosing a form.',
   'A service page may offer several routes. Match the verb to the job: register, update or replace. Eligibility means meeting the service’s conditions. Living in Manitoba is one part of the coverage rules; the official eligibility page covers status and residence conditions too.',
   'Fictional case: Kai moves to Manitoba and has never had Manitoba coverage.',
   ['Kai needs to check first-time registration, not merely replace an existing Manitoba card.',
    'Kai reads the eligibility page and the document requirements linked from registration.',
    'Kai lists any unclear requirement as a question for Manitoba Health. This lesson cannot decide whether Kai qualifies.'],
   'A finished practice lesson is not an application or a decision about coverage.'),
  lesson('Make the next step possible',
   'A missing card, document or internet connection changes the plan. Ask about the missing piece. Manitoba Health lists help and public-computer options. A saved practice answer is not a submitted form.',
   'A checklist separates what you have from what you still need to check. That prevents a guess from becoming a false answer on a form. Manitoba Health asks for relevant changes within 30 days. If you are late or unsure, contact the service rather than assume there is nothing you can do.',
   'Fictional case: Jo moved within Manitoba and cannot find the old card.',
   ['Jo already had Manitoba coverage, so this is not simply a first registration.',
    'Jo asks which update and replacement steps fit both the move and the missing card.',
    'Jo asks how to complete those steps without a home computer. Jo keeps real personal details out of this practice draft.'],
   'A receipt means the service received something. Read what it says before treating the request as approved.')],
 labs=[[
  evidence('health-route','Find the details that matter','Jo needs help after a move. Which details tell you to look at updating an existing record?',
   ['Jo already has a Manitoba Health record.','Jo changed address within Manitoba.','Jo bought a different-coloured bag.'],[0,1],
   'The existing record and changed address explain the job. The bag does not affect this choice.'),
  draft_task('health-plan',dict(title='Write Jo’s first plan',task='Using made-up details, write Jo’s job, the official page to use, and one detail to check before submitting.',
   example='Jo needs to update an existing Manitoba Health record. I would open the Manitoba Health update page and check what it asks for about the address change.',
   checks=['I named the change instead of assuming this is a first application.','I named Manitoba Health as the service.','I used no real card number, address or document photo.']))],
 [evidence('health-change','The old card is missing','Jo cannot find the card and has no computer at home. Which actions make the plan workable?',
   ['Ask Manitoba Health which update and replacement steps are needed.','Ask about available help or public-computer options.','Write a made-up card number on a real form.'],[0,1],
   'Ask about the obstacle directly. Inventing an identifier can cause a new problem.'),
  draft_task('health-revise',dict(task='Write Jo’s plan.',rework='Revise your plan: Jo cannot find the old card and has no home computer. Add a specific question for registration staff and an alternative way to get help.',
   example='Jo needs help with both an address update and a missing card. I would ask registration staff which steps apply and where Jo can get help using a computer.',
   checks=['I included both the move and the missing card.','I asked about a workable way to get help.','I did not claim that this practice submits or approves anything.']),True)]],
 practice=[
  q('Lee already has Manitoba coverage and moved to a new Manitoba address. Which job matches?','Update the existing record.','Register as if Lee never had coverage.','Apply for a driving licence.','Identify the existing record and the changed detail first.'),
  q('A first registration page says to check eligibility. What does that mean?','Check the conditions for who may qualify.','Check your quiz score.','Assume everyone with a local address qualifies.','Eligibility is about the service’s rules, not Stepstone progress.'),
  number('A fictional checklist has 4 items. Rae has confirmed 3. How many items still need checking?',1,'$4-3=1$ item remains. A count helps organise work; it does not decide whether a document is accepted.'),
  q('A card is missing and the correct replacement route is unclear. What is useful?','Ask registration staff about replacement.','Invent the missing card number.','Assume a new health number is needed.','Use the service’s help route for the missing detail.'),
  q('You save your plan in Stepstone. What happened?','Your practice plan was saved.','A government application was sent.','Coverage was approved.','Stepstone records learning; it does not submit to Manitoba Health.'),
  q('You lack a home computer. Which next step could help?','Check the official registration-help and public-computer information.','Assume no application route is possible.','Give an unknown person your document photos.','Ask the service about access options before sharing private documents.')],
 check=[
  q('Morgan has never had Manitoba coverage. What should Morgan check first?','The official eligibility and first-registration instructions.','Only the replacement-card instructions.','Only the rules for renewing a driving licence.','Choose the first-registration route and check its conditions.'),
  q('Pat has a Manitoba Health record and needs to change a name on it. Where should Pat start?','The official update routes.','A new unrelated social-media account.','The original form without reading its purpose.','The task is a change to an existing record.'),
  number('A practice plan has 5 checks. Two are still unconfirmed. How many are confirmed?',3,'$5-2=3$ checks are confirmed. Keep the remaining two visibly unfinished.'),
  q('A friend says a Manitoba address alone proves eligibility. What should you do?','Check the full official eligibility conditions.','Treat the address as the only rule.','Use your friend’s old application as approval.','An address alone does not establish all the coverage conditions.'),
  q('Which record helps distinguish applying from updating?','Whether the person already has Manitoba coverage and what changed.','The colour of their phone case.','The number of practice attempts they made.','The relevant facts identify the job the service must do.'),
  q('An application asks for a document you cannot access. Which question is useful?','Which options apply if I cannot get this required document?','Can I invent its reference number?','Can I leave every required answer blank without checking?','Ask about the exact missing requirement instead of guessing.'),
  q('A message says a request was received and is being reviewed. What does it establish?','It was received; the decision still needs checking.','Every condition was approved.','A new card has already arrived.','Read the message’s actual status, not the outcome you hope for.'),
  number('In this exercise, a change must be reported within 30 days. Ten days have passed. How many days remain in that stated window?',20,'$30-10=20$ days. Contact the service if you are unsure or already late.'),
  q('A registration question is still unclear. Which help route fits?','Manitoba Health’s published registration contact.','A stranger who asks for a card photo in a public comment.','A shop selling unrelated computer parts.','Use the contact route published by the responsible service.'),
  q('Which sentence belongs in a safe practice plan?','I will ask which proof is needed for this made-up case.','Here is my actual health-card number.','I attached my family’s real documents.','Practise the process without putting real identifiers in learning records.'),
  q('Sam needs an address update and a replacement card. What should Sam check?','Which steps cover both needs.','Whether changing an unrelated bank password replaces the card.','Whether a quiz pass automatically updates the address.','Name both changes so the service can direct the next steps.'),
  q('An official instruction changes after this lesson was written. Which should guide the real application?','The current official instruction or clarification from the service.','An older remembered example without checking.','The longest comment below a video.','The checked date helps you know when the lesson’s source information was reviewed.')],
 reflection='Use fictional details. Explain Jo’s revised plan and why you chose those service routes.'
)

IDENTITY = dict(
 id='life-photo-id',title='Prepare for photo ID',goal='Build an ID visit plan and check a missing document.',
 why='Photo ID can help you prove who you are. Reading the document list and planning the visit can save a wasted trip.',
 objectives=['Check the purpose','Find the missing piece','Plan the visit'],needs=['reading-3','math-budget'],
 sources=['id-apply','id-documents','id-help'],help='id-help',
 nextSteps=['Start with MPI’s Identification Card page and confirm this card fits your situation.',
  'Use the identity-document tool and current rules to check your exact combination of originals. Check current fees and any co-signature requirement.',
  'Ask MPI about anything missing before visiting an Autopac agent or MPI Service Centre. Keep real documents out of your practice answer.'],
 lessons=[
  lesson('Match the card to the job',
   'The optional Manitoba Identification Card is for people without a driver’s licence. It proves identity; it does not let you drive. MPI checks eligibility and supporting documents.',
   'Different cards serve different purposes. The card name alone does not tell you all its rules. Under 18, MPI’s application page says a parent must co-sign. If getting documents or a signature is difficult, ask MPI about your situation before planning a visit; do not assume any adult can sign.',
   'Fictional case: Alex wants photo ID, has no driver’s licence, and is 17.',
   ['Alex reads the Identification Card page instead of choosing a driving test.',
    'Alex notes the under-18 co-signature requirement and checks how it applies.',
    'Alex uses MPI’s identity-document information to list what to bring and what still needs confirming.'],
   'A Manitoba Identification Card is not permission to drive and is not a passport.'),
  lesson('Check the combination before the trip',
   'MPI asks for original supporting documents and a specific combination of identity details. The address evidence has date rules. One official-looking document does not automatically cover every requirement.',
   'A document can prove one fact but leave another unproved. MPI’s identity page has combination rules, including special rules when using a new plastic health card. A guarantor declaration may help in some situations, but is not a universal substitute. Check the exact combination with MPI rather than improvising it.',
   'Fictional visit plan: Ari has a checklist with one missing requirement.',
   ['Ari marks the missing item instead of marking the entire checklist complete.',
    'Ari asks which accepted option applies. Ari also checks current cost, location and opening hours.',
    'For this made-up budget only: $24-20=4$ dollars remain from the stated 24-dollar budget after a 20-dollar fee. Real costs must be checked.'],
   'A fee in a practice problem is a supplied number. It is not a promise about your actual cost or a fee waiver.')],
 labs=[[
  evidence('id-purpose','Choose the useful checks','Alex is 17, has no driver’s licence and wants a Manitoba Identification Card. Which belong in the plan?',
   ['Check the card’s eligibility and document requirements.','Check the parent co-signature requirement.','Assume the ID card will allow unsupervised driving.'],[0,1],
   'Read the requirements for this card and this situation. Identification and a driving licence have different purposes.'),
  draft_task('id-plan',dict(title='Build Alex’s visit plan',task='Write a fictional plan: which MPI page to check, which signature question to confirm, and what Alex should organise before visiting.',
   example='Alex will read MPI’s ID-card instructions and check the co-signature requirement. Alex will use the document tool and mark any missing item before planning the visit.',
   checks=['I kept ID separate from permission to drive.','I included the age-related signature check.','I described checks without entering real personal details.']))],
 [evidence('id-combination','One piece is missing','The document plan has a gap. Which are useful next steps?',
   ['Ask MPI which accepted combination fits this case.','Check any restrictions before relying on a guarantor declaration.','Assume two documents are acceptable just because both have an address.'],[0,1],
   'Document type, date and combination matter. Count alone does not establish acceptance.'),
  draft_task('id-revise',dict(task='Write Alex’s visit plan.',rework='Revise the plan: one required item is missing, and Alex is unsure who may co-sign. Add two precise questions for MPI before making the trip.',
   example='Which accepted document combination fits Alex’s missing item? What options apply when Alex cannot obtain the required co-signature? I would confirm these before arranging a visit.',
   checks=['I identified the missing document issue.','I asked who may sign without inventing permission.','I kept approval and fee decisions with MPI.']),True)]],
 practice=[
  q('An ID card and a driver’s licence are…','Different documents with different permissions.','Two names for the same driving permission.','Both permission to cross any border.','Read what a document is for before relying on it.'),
  q('Which plan fits a first ID-card visit?','Check the current list and gather the required originals.','Bring only phone photos without checking.','Choose any two objects with your name on them.','The official list specifies acceptable original supporting documents.'),
  number('A made-up visit costs 20 dollars plus 4 dollars travel. How many dollars are needed altogether?',24,'$20+4=24$ dollars. These are supplied practice costs.'),
  q('A required signature is hard to obtain. What is useful?','Ask MPI which options apply to this situation.','Ask anyone to pretend to be the required signer.','Assume the signature requirement disappears.','Explain the obstacle to the service before making a plan based on a guess.'),
  q('A guarantor declaration appears on a document page. What should you check?','Whether it is accepted for this exact need and document combination.','Whether it can replace every document automatically.','Whether it changes the learner’s birth date.','An alternative can have conditions and combination restrictions.'),
  q('Which statement is accurate after finishing this lesson?','I practised an ID visit plan.','MPI has approved my application.','I can now drive.','Learning progress is separate from government records and permissions.')],
 check=[
  q('Drew wants proof of identity but does not have a driver’s licence. Which page is relevant?','MPI’s Manitoba Identification Card page.','Only a road-test booking page.','Only a passport photo advertisement.','Choose the service for the document being sought.'),
  q('Casey is 16 and sees the under-18 co-signature rule. What should Casey do?','Confirm the required co-signature or ask MPI about a difficulty obtaining it.','Assume a friend’s signature is equivalent.','Ignore it because the form is online.','An age-related requirement must be checked, not replaced by a guess.'),
  number('In a fictional plan, travel costs 6 dollars and the stated fee is 20 dollars. How much is needed?',26,'$6+20=26$ dollars. Include both parts of the planned expense.'),
  q('Two proposed address documents look current. What remains to check?','Accepted document types, dates and combination rules.','Only whether they use the same font.','Nothing: a count of two guarantees approval.','The number of documents is only one part of a valid combination.'),
  q('A practice checklist needs 4 identity details. Three are confirmed. What is the sensible status?','One detail still needs confirming.','The whole application is approved.','The missing detail may be invented.','Keep an unconfirmed item visible until a valid route is established.'),
  q('Which question helps before travelling?','Does this original document combination meet the current requirements?','Can a Stepstone badge replace my documents?','Will any expired card always be accepted?','Ask about the exact combination and its current acceptance.'),
  number('Noon is 12:00. A fictional office closes at 12:00 and you arrive at 12:15. How many minutes after closing is that?',15,'12:15 is 15 minutes after 12:00. Check actual opening hours before a real visit.'),
  q('A budget uses an old quoted fee. What should happen before the visit?','Confirm the current fee and travel cost.','Treat any old amount as guaranteed.','Remove travel from the plan because it is inconvenient.','A usable plan checks both the price and the cost of reaching the service.'),
  q('Why might a photocopy fail to meet the ID instructions?','MPI asks for originals for supporting documents.','All paper documents are forbidden.','Only documents with colourful covers count.','The required format matters as well as the information on it.'),
  q('A new plastic health card is one proposed document. What should be checked?','The special rules for the second document on MPI’s current identity page.','Whether every other address document is automatically accepted.','Whether the card removes the need to prove anything else.','MPI lists combination-specific conditions; consult the current list.'),
  q('Which follow-up note is honest?','I still need MPI to confirm the missing item.','My mentor quiz score guarantees approval.','I can sign someone else’s part for them.','Distinguish what you checked from what the service still needs to confirm.'),
  q('Which item belongs in a fictional learning report?','A made-up visit checklist and a question for MPI.','A photo of a real birth certificate.','Someone else’s actual identification number.','The report demonstrates the planning skill without storing actual identity documents.')],
 reflection='Using made-up details, explain Alex’s revised ID visit plan and what MPI still needs to confirm.'
)

SIN = dict(
 id='life-sin',title='Get ready for a SIN',goal='Find the right SIN route and protect the number.',
 why='A Social Insurance Number is used for work and government programs. Practise preparing for it and spotting requests that do not need it.',
 objectives=['Choose a route','Protect the details','Explain the plan'],needs=['reading-3','digital-4'],
 sources=['sin-apply','sin-documents','sin-protect','sin-help'],help='sin-help',
 nextSteps=['Use Service Canada’s application tool. Select the real applicant situation and a suitable online, in-person or mail route.',
  'Check the current document list and submission format for that route. Ask the SIN program about a missing or mismatched document.',
  'Keep the resulting number private. Use the official protection guide to check when sharing is required. Never put a real SIN in Stepstone.'],
 lessons=[
  lesson('Pick the route for the person',
   'Service Canada handles SINs. Its tool asks who is applying, their status in Canada and how they want to apply. Status means their citizenship or immigration category. Different choices can require different documents.',
   'The application path depends on the person and method, not just the document’s name. From age 12, a person can apply for their own SIN. A parent or legal guardian can apply for a minor. Online, mail and in-person routes have format requirements; the tool helps choose the applicable list.',
   'Fictional case: Mo is 16, a Canadian citizen, and wants to apply in person.',
   ['Mo selects applying for themself, Canadian citizen and in person on the official tool.',
    'Mo checks the listed primary and secondary identity documents. Primary proves status; secondary confirms identity.',
    'Mo checks the required originals and asks Service Canada about any missing item. Mo does not paste document details into this lesson.'],
   'Do not choose a different status merely because its document list looks easier.'),
  lesson('Check the request before sharing',
   'A SIN is private. It is not general photo ID. Service Canada says you do not need to give it for a job application. After hiring, payroll has a different reason to need it.',
   'A request that sounds official still needs checking. Ask why the number is needed and use a known contact route. A missing confirmation letter does not mean you should seek a different number. The official SIN pages explain how to confirm an existing record. Practise with words such as “my number”, never a real number here.',
   'Fictional case: a stranger asks Mo to send a SIN in a public job-application comment.',
   ['Mo does not post the number. An application is not the same stage as hired payroll.',
    'Mo checks the employer through a separate, known contact method.',
    'Mo revises the application plan to ask about the role without including the SIN or document images.'],
   'Do not post or put a real SIN in a practice answer, public comment or unexpected message.')],
 labs=[[
  evidence('sin-route','Read Mo’s situation','Mo is 16, a Canadian citizen and wants to apply in person. Which tool choices match?',
   ['Applying for themself; Canadian citizen.','In-person application.','Select a different status to shorten the checklist.'],[0,1],
   'The choices should describe the actual fictional case. Age 16 is above the minimum age to apply for one’s own SIN.'),
  draft_task('sin-plan',dict(title='Prepare Mo’s checklist',task='Using fictional details, write the route Mo should choose, two kinds of document checks, and one question to ask if something is missing.',
   example='Mo will use Service Canada’s in-person route for a Canadian citizen applying for themself. Mo will check primary and secondary identity documents and ask which accepted option fits any missing item.',
   checks=['I matched Mo’s stated situation and application method.','I checked both kinds of identity evidence rather than inventing a document.','I included no actual SIN or document number.']))],
 [evidence('sin-privacy','A request changes the plan','Before an interview, an unknown account asks Mo to post a SIN in a comment. Which next actions fit?',
   ['Keep the number out of the comment.','Check the employer using contact information found separately.','Post the number because the message says urgent.'],[0,1],
   'A job application does not need a SIN. Check the request and recipient rather than following urgency.'),
  draft_task('sin-revise',dict(task='Prepare Mo’s checklist.',rework='Keep the application plan, then add what Mo should do about the unexpected request before an interview. Explain why a job application differs from hired payroll.',
   example='Mo will keep the number out of the application comment and verify the employer separately. A job application does not require it; hired payroll has a different reporting purpose.',
   checks=['I kept a clear next step for the real Service Canada process.','I explained why Mo should not post the number in this case.','I kept all real identifiers out of the draft.']),True)]],
 practice=[
  q('Which organization handles a SIN application?','Service Canada.','The office that books a road test.','Stepstone’s Steps balance.','Use the responsible service’s official route.'),
  q('In this case, Ali is 15. Can Ali apply for their own SIN?','Yes; Service Canada allows a person aged 12 or older to apply for their own.','No; everyone must be 18.','Yes; without any required documents.','Age 15 meets the own-application age rule; documents still matter.'),
  q('Why choose the application method before making the document plan?','The route has submission-format requirements.','All formats are interchangeable.','The method changes the person’s actual citizenship.','Match the list and format to the route being used.'),
  q('An ordinary job application asks for a SIN. What should you recognise?','The SIN is not needed at this application stage.','A public application is always the safest place to post it.','A quiz score can be sent instead of checking the request.','Service Canada distinguishes job applications from employers’ reporting duties after hiring.'),
  q('A name differs between documents. What is a useful check?','Whether a supporting document is required to link the names.','Whether you can change the scanned document yourself.','Whether spelling never matters.','The SIN document page explains supporting records for name changes.'),
  q('What should appear in this lesson’s practice draft?','The planned steps, using fictional details.','Your actual nine-digit SIN.','Photos of your family’s identity documents.','You can show understanding without exposing identifiers.')],
 check=[
  q('Ari is 13 and is preparing their own SIN application. Which age statement fits?','The own-application route is available from age 12.','Only people aged 18 or older can apply for themselves.','Age 13 removes all document requirements.','The age condition does not replace the document checks.'),
  q('A parent is applying for a 10-year-old. Which tool choice fits the applicant role?','A parent or legal guardian applying on behalf of a minor.','The child applying for themself because they can type.','An unrelated employer choosing any route.','Choose who is actually authorized to apply for this fictional case.'),
  q('Which does a primary SIN identity document establish?','The applicant’s status in Canada.','Their preferred phone brand.','Their Stepstone point total.','Primary evidence and the secondary identity check have different purposes.'),
  q('The online route asks for clear document copies. What should the learner follow?','The online route’s current upload instructions on the official service.','A rule that every route uses the same format.','An instruction to upload real documents to Stepstone.','Application formats belong to the official route; Stepstone is practice only.'),
  number('A fictional checklist has 3 document questions. One is answered. How many still need answers?',2,'$3-1=2$ questions remain. Ask about the missing details before treating the checklist as complete.'),
  q('A document’s printed information appears wrong. What is a useful next step?','Contact the document issuer about correction.','Edit the image to make it look different.','Choose a made-up identity for the application.','Resolve the source document issue through its issuer rather than altering evidence.'),
  q('Which situation differs from an initial job application?','A verified employer needs the SIN after hiring for income reporting.','An unknown account asks for a SIN in a public comment.','A contest asks for a SIN to release a prize.','A legitimate purpose and verified recipient matter; employment reporting is a different stage.'),
  q('Someone says a SIN letter is general photo ID. What is correct?','A SIN confirmation is not an identity document to use that way.','It proves every type of identity requirement.','It replaces a driver’s licence.','Use the right document for the particular identity check.'),
  q('A SIN confirmation is misplaced. What should be checked?','The official route to find or confirm the existing SIN.','How to get a different number just because a letter is missing.','Whether a random nine-digit number can replace it.','A lost confirmation does not itself mean the person needs a new number.'),
  q('An unexpected message threatens urgent action unless you reply with your SIN. Which response fits?','Do not reply with it; verify through a separate official contact route.','Send it quickly to avoid asking questions.','Post it publicly so others can help.','Urgency is not proof of a genuine request.'),
  q('Which question checks a request before sharing?','Why is the SIN required here, and how can I verify who is asking?','Can I send all my documents without knowing the purpose?','Will a more confident message make it safe?','Check purpose and recipient rather than tone or pressure.'),
  q('A learner finishes the practice and gets 6/6. What is true?','They passed this learning check; no SIN application was sent.','Service Canada issued a SIN through the quiz.','The learner can skip required documents.','App progress is separate from government processing and decisions.')],
 reflection='Use fictional details. Explain Mo’s revised application and privacy plan, including one reason behind a step.'
)

MODULES = [HEALTH, IDENTITY, SIN]

def attach(units, bank):
    attach_guides(units, bank, MODULES, SOURCES, CHECKED)

def attach_guides(units, bank, modules, sources, checked):
    for m in modules:
        subject=m.get('subject','digital')
        sequence=1+sum(u['subject']==subject for u in units)
        uid=m['id']
        practice=[]
        private=[]
        for target,items,per_lesson in [(practice,m['practice'],3),(private,m['check'],6)]:
            for n,item in enumerate(items):
                stage=1+n//per_lesson
                group='practice' if target is practice else 'check'
                target.append(dict(item,id=f'{uid}-{group}-{n}',caseId=f'{uid}-{group}-{n}',lesson=stage,skill=item.get('skill',('calculate','apply','reason')[n%3])))
        u=dict(id=uid,subject=subject,grade=min(sequence,12),sequence=sequence,practical=True,ready=True,minutes=m.get('minutes',25),
            title=m['title'],goal=m['goal'],why=m['why'],visual='workshop',lessons=m['lessons'],
            practice=practice,review=[l['watchFor'] for l in m['lessons']]+['State what you know, what you need to check, and who can help.'],reflection=m['reflection'],
            guide=dict(region='Manitoba, Canada',checked=checked,steps=m['nextSteps'],help=m['help']),
            resources=[dict(title=sources[k][0],url=sources[k][1],checked=checked,help=k==m['help']) for k in m['sources']])
        if 'checkSkills' in m:
            u['checkSkills']=list(m['checkSkills'])
        install(u,m['title'],m['goal'],m['objectives'],m['labs'],m['needs'],'Real-life guide')
        u['mission']['brief']=[m['goal'],m.get('practiceNotice','Practise with fictional details. Nothing is submitted to a government service.'),'Make a plan, explain a decision, then try a six-question check.']
        u['mission']['artLabel']='READ / PREPARE / ASK'
        u['mission']['preparation']=[dict(id=i,title=next(v['title'] for v in units if v['id']==i)) for i in m['needs']]
        units.append(u)
        bank[uid]=private
