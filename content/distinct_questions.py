"""Remove identical prompts and add original held-out cases to the remaining thin banks.

Question IDs already embedded in saved attempts remain valid. This only changes
the source pools used for new rounds and new checks.
"""
import re
import unicodedata

def question_key(question):
    text=question.get('passage','')+' '+question['prompt']
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip().casefold()

CHECKS={
 'writing-6':[
  ('A task sheet says “submit the count”, but gives no destination. Which question fills that gap?', 'Where should I submit the count?', 'How many items should I count again?', 'Can I start counting later?', 'The missing detail is the destination, not the quantity or start time.'),
  ('You need both a due date and the file format for a poster. Which message makes both easy to answer?', 'When is the poster due? Which file format should I use?', 'Tell me everything about the poster.', 'The poster is confusing. Is that fine?', 'Two specific questions let the reader answer each missing detail.'),
  ('A colleague already answered which room to use. Your next message asks the same thing again. What should you revise?', 'Ask about the remaining unknown detail instead.', 'Add more question marks to the repeated question.', 'Remove all context from the message.', 'Use the answer you have and ask for what is still missing.'),
  ('You will order labels, but do not know how many copies each shelf needs. Which written question fits?', 'How many label copies does each shelf need?', 'What colour is the storage room?', 'Can you describe the whole building?', 'The quantity per shelf is the detail needed to order the labels.'),
  ('The reply gives a quantity but leaves your question about size unanswered. What is a useful follow-up?', 'Thanks. What size should those copies be?', 'Repeat every question without acknowledging the reply.', 'Assume any size will work.', 'Acknowledge the useful answer and name the unanswered part.'),
  ('A request says “Please explain it.” Why might adding the step number help?', 'It identifies the exact part the reader should explain.', 'It guarantees that no follow-up will be needed.', 'It makes the request sound more urgent.', 'A specific reference reduces guessing about the unclear step.'),
 ],
 'writing-10':[
  ('A supplier needs to find your message about order 418. Which subject line is most useful?', 'Order 418: confirm delivery day', 'Hello again', 'Important things to discuss', 'The order number and purpose help the reader identify the message.'),
  ('A shipment arrived with one damaged box. Which first sentence reports the problem clearly?', 'Order 418 arrived today; one of its six boxes is damaged.', 'Your company never does anything right.', 'There is something about an order.', 'The sentence gives a reference, an observation and the affected quantity.'),
  ('You wrote “The replacement will arrive tomorrow” without confirmation. What should you change?', 'Say that you are asking when the replacement can arrive.', 'Add capital letters to make the claim stronger.', 'Remove the order reference.', 'Separate a confirmed fact from a time you still need to ask about.'),
  ('You need approval to use a different material. Which closing asks for a clear next action?', 'Please confirm whether I should use the substitute material.', 'I have mentioned some materials.', 'Everyone can decide later somehow.', 'The reader can see the decision you need before continuing.'),
  ('Your draft promises a report by noon, but you can finish it at 2 pm. Which revision supports planning?', 'I can send the report by 2 pm. Does that timing work?', 'I will send it by noon even though I cannot.', 'Delete every mention of timing.', 'A realistic time gives the reader useful information for planning.'),
  ('A message includes a coworker’s private phone number that the recipient does not need. What should you do before sending?', 'Remove the unnecessary private detail.', 'Leave it because longer messages look thorough.', 'Put it in the subject line instead.', 'Include information needed for the task, rather than unrelated personal details.'),
 ],
 'social-2':[
  ('Two people share one label printer. One job is running and the next person is waiting. Which plan respects the current turn?', 'Finish that print job, then hand over the printer.', 'Cancel the current job without checking.', 'Send both jobs repeatedly until one appears.', 'Finish the agreed turn and make the handover clear.'),
  ('You and Lee need the same measuring tool. Which request helps arrange a turn?', 'Can I use it after you finish this measurement?', 'You should have guessed that I needed it.', 'I will take it while you are measuring.', 'A specific request makes the next turn predictable.'),
  ('Your partner asks for a moment to read a task card before responding. What helps the shared task?', 'Allow the pause, then check the next step together.', 'Answer every question for them immediately.', 'Start a different task without telling them.', 'Time to process information can support an accurate contribution.'),
  ('The agreed roles are sort first, then label. Sorting is complete. What should happen next?', 'Tell the labeler the sorted items are ready.', 'Keep moving the sorted items without explaining.', 'Start labeling a different pile secretly.', 'A clear handover tells the next person when their part can begin.'),
  ('A turn is taking longer than expected and you need the tool soon. Which response helps?', 'Ask how much longer is needed and agree on a plan.', 'Grab the tool without warning.', 'Assume the other person is ignoring you.', 'Discuss timing before changing the shared plan.'),
  ('Why can a written role list help a group with several steps?', 'People can check who does each step and when to hand over.', 'It means nobody ever needs to communicate.', 'It makes every task take the same amount of time.', 'A shared reference supports coordination without replacing communication.'),
 ],
 'social-3':[
  ('An instruction says to seal the blue crates. You see blue and grey crates. What should you confirm before sealing?', 'That the blue crates are the ones intended.', 'That every crate needs the same treatment.', 'That colour never matters in instructions.', 'Check the named objects rather than extending the instruction to other items.'),
  ('You are told to “check the meter”, but there are two meters. Which clarification helps?', 'Which meter should I check?', 'Should I skip both meters?', 'Can I rearrange the room instead?', 'Ask about the ambiguous object before choosing one.'),
  ('You repeated an instruction and your partner corrected the order. What should you do?', 'Use the corrected order and confirm it.', 'Keep the first order because you said it already.', 'Assume that checking was a mistake.', 'The correction is useful information caught before you act.'),
  ('A task requires recording the reading before switching off a device. Which restatement checks the sequence?', 'Record the reading first, then switch it off. Correct?', 'Switch it off and estimate the reading later. Correct?', 'Either step can always go first. Correct?', 'Restate both actions in their required order.'),
  ('You know where an item goes, but not how many to move. Which question targets the remaining gap?', 'How many should I move there?', 'Where does it go again?', 'Why does the room have shelves?', 'Ask for the missing quantity rather than repeating a known location.'),
  ('Why can trying one supervised example help check an instruction?', 'It lets you show your interpretation and catch a misunderstanding.', 'It proves that every later task will be identical.', 'It means there is no need to inspect the result.', 'A small trial gives evidence of understanding before the full task.'),
 ],
 'social-4':[
  ('A printer feeds paper but produces blank pages. Which statement describes the observed problem?', 'Paper moves through, but the pages come out blank.', 'The whole printer is always useless.', 'Printing is a bad idea.', 'Describe what happened rather than making a broad judgement.'),
  ('You want help with a file that will not open. Which detail is useful to include?', 'The message shown when you try to open it.', 'A guess about the helper’s personal life.', 'Every unrelated file on the device.', 'The exact message helps the helper understand the specific failure.'),
  ('You think a cable may be loose, but have not checked. How should you present that idea?', 'As a possible cause, separate from what you observed.', 'As a confirmed fact.', 'As proof that the device must be replaced.', 'A possible explanation is different from an observed result.'),
  ('A label peeled off after the box was moved. Which description gives useful sequence information?', 'The label was attached before the move and loose afterward.', 'Labels never work anywhere.', 'The box is the wrong colour.', 'Before-and-after details help locate when the problem appeared.'),
  ('You tried restarting the program and it still shows the same error. What should you tell the helper?', 'That you restarted it and the same error remains.', 'That you have not tried anything.', 'That the error must be gone because you restarted.', 'Reporting what you tried avoids unnecessary repeated steps.'),
  ('Why name the result you expected when explaining a problem?', 'It helps compare the intended result with what actually happened.', 'It makes your expectation an observed fact.', 'It means the cause is already known.', 'The gap between expected and observed behaviour defines the problem.'),
 ],
 'social-6':[
  ('A fast spoken demonstration is difficult to follow. Which support request fits that task?', 'Could we pause after each step while I try it?', 'Could everyone stop doing all work forever?', 'Should I pretend I followed every step?', 'A pause between steps gives time to try and check the action.'),
  ('A written checklist helps you complete a packing task. What can you say when requesting it?', 'A checklist helps me check each item before sealing the box.', 'I must describe my entire personal history first.', 'You should know why without me naming the task.', 'Explain the practical support and how it helps the work.'),
  ('The requested quiet room is unavailable. Which next step keeps the discussion useful?', 'Ask whether written instructions or a quieter time are available.', 'Assume no other support could help.', 'Agree to instructions you cannot hear.', 'Another format or timing may address the same practical need.'),
  ('Tiny print on a task card is hard to read. Which request names the relevant change?', 'Could I have a larger-print copy of this task card?', 'Could the task be made more complicated?', 'Can you remove every instruction?', 'Ask for a format that makes the actual information accessible.'),
  ('You need a short pause before answering a new question. Which phrase states that need clearly?', 'Please give me a moment to think about this question.', 'I understood everything before you spoke.', 'I have to answer immediately even if I guess.', 'You can name processing time directly.'),
  ('Why check whether an agreed support is helping after trying it?', 'You can keep it or discuss a more useful adjustment.', 'Every first suggestion must work perfectly.', 'Checking a support means the task no longer matters.', 'A support can be reviewed against how it helps the task.'),
 ],
 'social-8':[
  ('Two people disagree about who was meant to lock the room. Which first question helps clarify?', 'What did each person understand the locking plan to be?', 'Which person should be blamed before checking?', 'Why should the room stay open forever?', 'Start by comparing the actual understandings of the shared plan.'),
  ('You heard that a coworker changed a schedule, but have not seen the updated schedule. What helps before responding?', 'Check the current schedule or ask for clarification.', 'Treat the rumour as a confirmed fact.', 'Change another shift in return.', 'Confirm the information before acting on an assumption.'),
  ('Your partner wants the window open; you need less noise. Which proposal addresses both concerns?', 'Try ventilation during a quiet period and check whether that works.', 'Assume only one concern can be real.', 'Refuse to name either concern.', 'A practical trial can account for more than one valid need.'),
  ('A discussion becomes too heated to continue clearly. Which response supports a later resolution?', 'Suggest a pause and agree when to return to the issue.', 'Leave without any plan to continue.', 'Keep repeating the same point faster.', 'A planned pause preserves the chance to discuss the issue calmly.'),
  ('Someone says, “That is not what I meant.” Which reply checks meaning?', 'Can you explain what you meant by that part?', 'I know your meaning better than you do.', 'Then nothing you said matters.', 'Ask about the unclear meaning rather than insisting on your interpretation.'),
  ('Why separate an observation from an assumption during a disagreement?', 'The people can check the facts without treating a guess as established.', 'Assumptions are always more accurate than records.', 'Observations decide every preference automatically.', 'Shared facts and different interpretations can be discussed separately.'),
 ],
 'social-9':[
  ('A coworker covering your shift needs to know which orders remain. Which message is useful?', 'Orders 12 and 15 are unfinished; the others are packed.', 'Some things happened during the shift.', 'Everything is probably fine somehow.', 'Name the remaining work so the next person can act.'),
  ('A meeting has moved from Room A to Room C. Who needs the updated message?', 'The people expected to attend that meeting.', 'Only people who are not attending.', 'Nobody, because the first message was sent.', 'Send the change to the people whose plan is affected.'),
  ('A message gives a task but no deadline. Why might a deadline clarification matter?', 'It helps the recipient plan when the work is needed.', 'It guarantees that the work will take no time.', 'It changes the task into a different subject.', 'Timing is part of coordinating work, especially when priorities compete.'),
  ('You finished the inventory check and found two missing boxes. Which handover message is precise?', 'Inventory checked: two boxes are missing from shelf 4.', 'I did a thing and there was an issue.', 'The entire store has disappeared.', 'A specific result and location make the report usable.'),
  ('You cannot finish a task by the agreed time. Which message gives the team useful information?', 'I need another 30 minutes. Should I finish this or switch priorities?', 'Say nothing until someone notices.', 'Promise it is finished while it is not.', 'State the delay and ask about the next priority while planning is still possible.'),
  ('Why check that a work message was understood when the next step depends on it?', 'A short confirmation can reveal a missing or misunderstood detail.', 'Sending always proves that every recipient understood.', 'It lets you avoid giving any task details.', 'Receipt and understanding are different; clarification supports the handover.'),
 ],
 'social-10':[
  ('A job conversation asks for an example of organising work. Which answer gives evidence?', 'I sorted the stock labels by shelf so the team could find them.', 'I am organised because I say so.', 'I have a favourite colour.', 'A concrete action connected to a useful result supports the claim.'),
  ('A question asks about using a checklist, but you do not understand the word “checklist”. What could you ask?', 'What do you mean by checklist in this task?', 'Can I claim an experience I never had?', 'Should I answer a different question?', 'Clarifying a word helps you answer the actual question honestly.'),
  ('Why prepare several truthful examples before a job conversation?', 'Different questions may call for different relevant examples.', 'Every question requires the same memorised sentence.', 'Prepared examples should include invented achievements.', 'Preparation helps you choose evidence that fits the question.'),
  ('You have no paid work experience but helped organise a school event. How could you use that experience?', 'Describe the relevant task, your action and its result.', 'Say it never counts because it was unpaid.', 'Change it into a paid job you did not have.', 'Relevant skills can be demonstrated in unpaid settings too.'),
  ('You want to learn how new staff are trained. Which question helps?', 'How is a new person shown the tasks during the first shifts?', 'What is every employee’s home address?', 'Can I ignore all training?', 'Ask about the actual support for learning the role.'),
  ('What is a useful purpose of practising an interview answer aloud or in writing?', 'Check whether your example is clear and relevant.', 'Remove every natural variation in your wording.', 'Guarantee that you will receive an offer.', 'Practice can improve clarity without guaranteeing an outcome.'),
 ],
}

PC_RECOVERY=[
 ('A Windows practice note was deleted by mistake. Where can you check before recreating it?', 'Check the Recycle Bin for that note.', 'Empty the Recycle Bin immediately.', 'Delete another note with a similar name.', 'The Recycle Bin may hold a deleted local file until it is emptied.'),
 ('You restore two notes with similar names. What should you inspect to identify your shopping note?', 'Open the restored note and check its contents.', 'Choose whichever icon looks brighter.', 'Assume the first filename is enough.', 'Opening the recovered copy checks that it contains the note you intended.'),
 ('A restored file is back, but the changes from this morning are missing. What does that tell you?', 'You need to check whether another saved version has those changes.', 'Restoring always invents every unsaved change.', 'The missing edits prove every file is damaged.', 'Recovery restores an available saved version, not work that was never saved.'),
]

def make_question(uid,index,args,skill=None):
    prompt,right,wrong1,wrong2,why=args
    return dict(id=f'{uid}-distinct115-{index}',kind='choice',prompt=prompt,
                options=[dict(id=str(i),text=text) for i,text in enumerate((right,wrong1,wrong2))],
                answer='0',explanation=why,hint='Compare the choices with the specific situation.',
                skill=skill or ('calculate','apply','reason')[index%3],lesson=1 if index<3 else 2)

def refine(units,bank):
    by_id={u['id']:u for u in units}
    recovery=by_id['pc-recover']
    if recovery.get('learningRevision',0)<117:
        old=recovery['practice'][:3]
        new=[make_question('pc-recover',i,args,'interpret' if i==0 else 'apply' if i==1 else 'reason') for i,args in enumerate(PC_RECOVERY)]
        replacements={question_key(a):b for a,b in zip(old,new)}
        recovery['practice']=[replacements.get(question_key(q),q) for q in recovery['practice']]
        for task,question in zip(recovery.get('mission',{}).get('labs',[[]])[0],new):
            task.update(id=question['id']+'-lab',prompt=question['prompt'],options=[o['text'] for o in question['options']],answer=0,why=question['explanation'])
            task['messages']=[dict(label='Situation',text=question['prompt'])]
    public=set();practice_seen=set()
    def walk(value):
        if isinstance(value,dict):
            if isinstance(value.get('prompt'),str):public.add(question_key(value))
            for item in value.values():walk(item)
        elif isinstance(value,list):
            for item in value:walk(item)
    for unit in units:
        if not unit['ready']:continue
        unique=[]
        for question in unit['practice']:
            key=question_key(question)
            if key in practice_seen:continue
            practice_seen.add(key);unique.append(question)
        assert len(unique)>=6,unit['id']
        unit['practice']=unique
        walk(unit)
    for uid,args in CHECKS.items():
        if by_id[uid].get('learningRevision',0)<117:bank[uid]+=[make_question(uid,i,q) for i,q in enumerate(args)]
    seen=set()
    for uid,questions in bank.items():
        distinct=[]
        for question in questions:
            key=question_key(question)
            if key in seen or key in public:continue
            seen.add(key);distinct.append(question)
        assert len(distinct)>=6,uid
        bank[uid]=distinct
    return dict(practiceQuestions=len(practice_seen),checkQuestions=len(seen),newCheckCases=sum(map(len,CHECKS.values())))
