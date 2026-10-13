"""Reviewed non-math batches using one mission shell and the original check IDs."""
from math_missions import spec,task,lesson

READING={
10:('Look behind an argument','Find the proposal, its evidence and a fair objection.', ['Find the proposal','Test its support','Answer an objection'],None),
11:('Trace a source','Find the original record and check what it can tell you.', ['Choose a direct source','Trace repeated claims','Keep a useful reference'],None),
12:('Weigh a real choice','Compare needs and evidence before recommending a plan.', ['Name the shared goal','Compare the tradeoff','Support a decision'],None),
6:('Back up what you read','Point to a detail and explain what it supports.', ['Choose a detail','Limit the claim','Explain the link'],None),
7:('Check your first guess','Use clues without pretending they prove more than they do.', ['Find the clues','Try another explanation','Check a new clue'],None),
8:('Check a bold claim','Tell what a post claims from what its evidence shows.', ['Name the claim','Check its reach','Recheck before sharing'],None),
9:('Compare two accounts','Find out whether two reports really disagree.', ['Match time and place','Check what was counted','Compare fairly'],None),
2:('Who did what?','Follow the person, the action and the thing.', ['Find the action','Clear up a name','Read a new sentence'],[
 lesson('Find the person and the action','Read: Sam packed the bag. Who did it? Sam. What did Sam do? Packed. What did Sam pack? The bag.',
 ['Read the whole sentence.','Find the action: packed.','Ask who packed, and what was packed.'],
 'Word order helps you follow the action. Sam helped Alex and Alex helped Sam use the same names, but name different helpers. Read every word before deciding.',
 'Do not pick a person just because their name comes first in the passage.'),
 lesson('Check what a short word points to','Words like they and it save us repeating names. Go back to check what they mean. If two names fit, ask for a clearer sentence.',
 ['Sam put the bag down. It was heavy.','It means the bag.','Sam gave Alex their notebook is less clear. Ask whose notebook it is.'],
 'A reader needs to know who or what a word points to. Sometimes the message leaves that unclear. Asking for the missing detail is better than a confident guess.',
 'They can mean one person or more than one. Use the sentence, not a guess.')]),
3:('Follow the steps','Use before, after and if to choose the next step.', ['Read the order','Handle a change','Follow a new plan'],[
 lesson('Read before you start','Some steps need another step first. Before and after show the order. Read all the steps so you know what you need.',
 ['Save the file before closing it.','That means save first.','Close the file after saving.'],
 'The word before tells you which action must come first. It does not matter which action was named first in the sentence. Say the order back in your own words.',
 'Do not guess the order only from where a step appears on the page.'),
 lesson('Use an if step when it fits','An if step is for a particular situation. Check whether that situation is happening before you use the step.',
 ['Read: If the printer is busy, wait.','Check: is it busy?','If yes, wait. If no, follow the normal printing step.'],
 'An if step gives you a different route when something changes. It does not replace the normal plan in every situation. Find the condition, then choose the matching action.',
 'Do not follow every branch at once. First check which condition is true.')]),
4:('Find the point','Keep the main idea without adding a guess.', ['Find useful details','Keep the meaning','Summarise a new text'],[
 lesson('Ask what the details are about','Jo checks a route, packs water and finds a jacket. These details share a purpose: getting ready for a trip.',
 ['List the useful actions.','Ask what connects them.','Say the main point in one short sentence.'],
 'A main point covers the important details together. A detail can be true without being the main point. The colour of a bag tells you less about the purpose of the trip.',
 'Do not choose a tiny detail just because you remember it easily.'),
 lesson('Keep a summary fair','A summary says the important meaning in fewer words. Leave out small details. Keep the meaning. Do not add facts the text never gave you.',
 ['Source: Jo checked the route and packed a jacket.','Fair summary: Jo prepared for a trip.','Too far: Jo is the best traveller in the country.'],
 'A short summary still has to be supported by the source. Check each claim against the words you read. If you cannot find support, remove it or clearly mark it as a question.',
 'A summary is not a place to turn a guess into a fact.')]),
5:('Work out a word','Use nearby words to choose a meaning that fits.', ['Read around the word','Test the meaning','Explain your choice'],None),
}

READING_BODIES={
10:['An argument connects a proposal with reasons and evidence. Find what the writer wants to happen. Then ask which facts support that choice.',
    'A fair objection points out a cost, risk or missing detail. Answering it makes the proposal stronger. Attacking the person does not answer their concern.'],
11:['Start with the question you need answered. Find a source close to the event or service. Check who made it, when, and whether it covers your situation.',
    'Several pages can repeat one source. Trace their links before counting them as separate evidence. Keep enough detail for someone else to find the original.'],
12:['People can share a goal and care about different needs. One traveller needs a low fare; another needs fewer transfers. Neither need disappears because the other matters.',
    'Use the same facts to compare the options. Explain what your choice helps, what it costs, and what you still need to check. A small trial can test an uncertain plan.'],
5:['A word can mean different things. Read the words around it. A delivery charge is a price. Charging a tablet adds stored energy. Choose the meaning that fits.',
   'Some phrases do not mean exactly what their words say. The queue crawled means it moved slowly. Ask for a plain version if a phrase is unclear.'],
6:['Evidence is a detail that supports an answer. Pick the detail, then explain the link. A true detail is not useful evidence for every question.',
   'One example tells you about that example. It does not prove always or everyone. Keep your claim within what the text actually shows.'],
7:['An inference is a possible explanation based on clues. Wet pavement and wet umbrellas suggest rain. They do not prove when it rained or rule out another cause.',
   'Use may or suggests when the clues are incomplete. A quiet person might be thinking, tired or not have heard. Ask instead of deciding you know their feelings.'],
8:['A claim asks you to believe something. Evidence is the information offered to support it. A confident voice is not evidence by itself.',
   'Check who was asked, how many, and when. A survey of ten friends tells you about those ten people. It cannot show what everyone thinks.'],
9:['Two reports may describe different times or places. Check what each person actually saw. Different accounts can both be true.',
   'Compare the same kind of count. Twenty visits is not necessarily twenty different people. If reports still disagree, keep that question open and look for better evidence.']}

WRITING={
9:('Rewrite for the reader','Turn a vague complaint into a usable request.', ['Find the missing detail','Revise for the receiver','Check what changed'],[
 'The reader needs enough information to act. Name the problem, the help needed and a useful time. Replace vague words such as it, soon and broken when their meaning is unclear.',
 'Revision changes meaning, order or detail to help the reader. Check facts and the purpose before polishing spelling. Keep only the personal information the task needs.']),
10:('Send a useful work update','Explain progress, a blocker and the next action.', ['Report the progress','Offer a workable option','Check the handoff'],[
 'Put the main point early. Say what is finished, what is not, and what you need. Keep a confirmed fact separate from an estimate.',
 'If the first plan cannot happen, offer a realistic alternative. Name who needs to decide. Do not promise a result that depends on an unconfirmed step.']),
11:('Propose a fair change','Make a reasoned proposal and answer an objection.', ['Explain the proposal','Address another need','Plan a fair trial'],[
 'A useful proposal names a change and explains why it would help. Give evidence or a clear reason. Consider a fair objection instead of attacking the person raising it.',
 'Explain how your plan handles the objection. A limited trial can test an uncertain idea. Say what you would measure and when you would review it.']),
12:('Plan a small project','Write a plan that fits the people, time and resources available.', ['Set a clear scope','Adapt to a constraint','Explain the next step'],[
 'Name the purpose, the actions and who would do them. List resources you actually have separately from support you still need. Explain how you will know the project helped.',
 'A smaller budget or missing resource may require a smaller plan. State what can still be done. Agree changes before promising someone else’s time or money.']),
5:('Describe a problem clearly','Give someone enough detail to picture what you saw.', ['Name the object','Replace vague words','Check the description'],[
 'A useful description helps someone who cannot see the object. Give its name, location and a feature they can check. A size or direction is often more useful than bad or broken.',
 'Separate what you saw from what you think caused it. Replace vague words with measurements or locations when useful. Say what you do not know.']),
6:('Ask for what is missing','Write a request the other person can answer.', ['State what you know','Add the missing need','Check the request'],[
 'Name the task and the information you already have. Ask for the exact missing piece. A clear request gives the reader a useful action to take.',
 'Add a time limit if it matters. Ask whether the person can meet it. A request is not an agreement until the other person confirms it.']),
7:('Explain how it works','Show the steps and the reason behind them.', ['Set out the method','Try a new example','Explain the check'],[
 'A process explanation tells how and why. Put the steps in order. Explain the reason for an important step, rather than only saying do this.',
 'Try the method with a new example. Name the conditions it needs and how to check the result. That helps the reader use it again.']),
8:('Make a supported recommendation','Use evidence while keeping its limits visible.', ['Report the evidence','Answer another need','Revise the recommendation'],[
 'State a recommendation, give evidence, then explain the link. Keep the actual numbers. Say who or what the evidence describes.',
 'A majority preference does not erase other needs. Consider a fair objection. Change your proposal or explain what else must be checked before acting.']),
1:('Arrange a meeting','Write a message someone can act on.', ['Name the plan','Update the time','Send a clear draft'],[
 'Start with what you want the reader to do. Add where and when. Write one useful sentence first. You can add another if a detail is missing.',
 'Read your message as if you did not know the plan. Add a missing time, place or item. If the plan changes, make the new plan clear.']),
2:('Make the sentence clear','Show who does each action.', ['Name the action','Remove a guess','Check your sentences'],[
 'A sentence gives a complete thought. Name who or what it is about, then what happens. Start with a capital letter. Use an ending mark.',
 'Read back each sentence. Can the reader tell who they or it means? If not, use a name. A short, clear sentence is enough.']),
3:('Write steps someone can follow','Give the next action in a useful order.', ['Put first things first','Handle a missing step','Test the instructions'],[
 'Write one action per step. Name what the reader needs. Put the first action first. Words like open, select and check help the reader know what to do.',
 'Add a final check so the reader knows they are done. Use if for a different situation. Say what to do if something needed is missing.']),
4:('Make one clear point','Build a short paragraph with useful support.', ['Say the point','Choose useful detail','Improve the paragraph'],[
 'A paragraph groups sentences about one main point. Say the point, give a useful detail, then explain how the detail helps. Leave out unrelated facts.',
 'Read each sentence against the main point. Keep what helps the reader understand it. Replace a vague detail with an example someone can picture.']),
}

WRITING_WHY={
1:['The reader cannot see the plan in your head. A place and a time turn meet me later into something they can use. Short can still be complete.',
   'Read the message as the other person. If you would have to ask where or when, add that detail. Check the plan first; fix spelling after the meaning is clear.'],
2:['Sam moved the box tells who did what. The heavy red box is only a description; it does not tell what happened. Build the whole thought before adding detail.',
   'A full stop can split two thoughts. Because gives a reason, but shows a difference, and adds another idea. Use a name if a short word leaves the person unclear.'],
3:['Picture yourself doing the task. Put a needed item before the step that uses it. Then name each action in order, so the reader does not have to guess.',
   'Ask someone to tell you the next action after each step. If they must guess, add the missing detail. A final check tells them when the job is done.'],
4:['Keep the sentences working together. The point says what matters; the detail shows it; the explanation joins them. An interesting but unrelated fact can go elsewhere.',
   'Check each sentence against the main point. Remove a detail that changes the topic. Add a link when the reader would otherwise have to guess why your example matters.']}

SOCIAL={
9:('Close the message loop',['Send a clear update','Check what was received','Follow up usefully'],[
 'A work update names the facts, the missing piece and the next action. Use the agreed channel. Keep private information out unless the task actually needs it.',
 'Sent does not mean read, understood or agreed. If a change matters to immediate work, ask for confirmation and use the agreed follow-up route when it does not arrive.'],
 'No reply has arrived and collection is soon. Revise your update to request confirmation and name an appropriate follow-up without inventing agreement.',
 'Eight packs are ready; two still need the updated page. Please confirm whether to send the eight now. If I do not hear before collection, I will check with the task lead.'),
10:('Explain a real job example',['Choose a truthful example','Handle a follow-up','Name what you learned'],[
 'A useful job example can come from a project, volunteering or daily life. Describe the situation, what you did and what happened. Do not invent experience.',
 'Take time to understand a follow-up question. Ask for it again or choose a specific detail. You can say what you learned when a task did not go perfectly.'],
 'The interviewer asks what you would change next time. Add a specific lesson from your invented practice example; do not invent real work history.',
 'In my practice project, the first labels missed a date. I checked one with the organizer and then used that as the pattern. Next time I would confirm one sample before making all of them.'),
11:('Turn feedback into a next step',['Find the specific issue','Revise the right part','Check the result'],[
 'Useful feedback names an action and its effect. It can show what to keep and what to change. A comment about one piece of work is not a verdict about you.',
 'Ask for an example if feedback is vague. Compare it with the task requirements. Make a useful change, or show why a correction may be based on the wrong version.'],
 'The person explains that step two uses a name they do not know. Revise your response with a concrete fix and a way to test it.',
 'I will replace that name with a plain description and add where to find the button. Could you try reading step two again and tell me your next action?'),
12:('Try a small solution',['Define the problem','Agree a limited trial','Review the result'],[
 'Describe the problem with examples. Compare possible causes before choosing an action. Stay within your role and training; some tasks need an appropriate specialist or supervisor.',
 'Agree a small trial, who will do it and what result to look for. If it does not help, use the evidence to change the plan. Do not call a problem solved without checking.'],
 'After a week, clearer labels helped one shelf but not another. Revise the plan using the result, rather than claiming the whole problem is solved.',
 'The first shelf improved, but items on the second are still mixed. Could we check its layout and labels with the people using it? I suggest a small agreed change there and another review next week.'),
5:('Make a team plan',['Name the jobs','Agree a new handoff','Check responsibilities'],[
 'List the jobs and agree who does each one. Name when people will check in and what must be handed over. A clear plan reduces both missed and duplicated work.',
 'A plan needs agreement. Check workload and access needs instead of assuming everyone can work the same way. When something changes, tell the people who depend on that step.'],
 'One person is unavailable for the last half hour. Revise the two-person plan so the remaining work has an agreed owner and handoff.',
 'I can finish the labels before you leave. Could you complete the list first and hand it over at 1:30? Let’s check at 1:15 whether the timing still fits.'),
6:('Ask for support that works',['Name a useful support','Test the adjustment','Revise the request'],[
 'An adjustment is a change that helps you do the task. Name the practical need and a support to try. You do not have to share a diagnosis or private family details in this practice.',
 'Try the support on one step. If it still does not help, explain what remains difficult and suggest a change. There can be more than one workable format.'],
 'The written list helps, but one step is still hard to picture. Revise your request for a brief demonstration of that step.',
 'The written order helps me keep track. Could you show me where the date goes on one label? I can then try the next label and check it with you.'),
7:('Adjust a work plan',['Find the blocker','Choose a realistic option','Confirm the next check'],[
 'A plan connects a goal to the jobs, time and resources it needs. Some jobs depend on earlier steps. Name the dependency so a delay does not stay hidden.',
 'When a resource is unavailable, update the estimate. Offer a workable option and ask the responsible person to confirm the priority. An estimate is not a guarantee.'],
 'The printer will be unavailable for another hour. Revise the plan without promising all ten packs by the old deadline.',
 'Five packs can be finished now. The rest need printing, which is delayed at least an hour. Should we hand over the five first? I can update you when printing is confirmed.'),
8:('Clarify a disagreement',['Name the practical needs','Offer a workable option','Check the agreement'],[
 'Describe the specific issue and ask what the other person needs. A boundary says what you need to keep or protect. You can be clear without guessing their motives.',
 'Look for an option that meets the important needs. Confirm it together. If you cannot agree or the issue is outside your role, ask an appropriate person for help.'],
 'The other person needs half the table immediately. Propose a specific boundary and compromise, and ask whether it works.',
 'I need this labelled section in place for ten more minutes. Could we clear the other half now? If that is not enough space, let’s ask which task takes priority.'),
1:('Ask for the help you need',['Name the missing step','Try another way','Check you can begin'],[
 'Name the task and the part you do not understand. You can ask aloud, write it or point to the step. A clear request does not need a particular facial expression.',
 'Try one step after the explanation. If it is still unclear, say which part and ask for a different example. Asking again can prevent a mistake.'],
 'The spoken example was too fast. Revise your request to ask for a format you can use.',
 'Could you write the label steps down? I understood the name, but I missed where the date goes. Then I can try one for you to check.'),
2:('Agree on a handoff',['Name both tasks','Change the timing','Check the agreement'],[
 'When two people need the same tool, agree who uses it first and how it passes to the next person. Check the real time limit for both tasks.',
 'If the plan stops working, say what changed and agree a new handoff. Do not assume the other person can guess your timing or that silence means agreement.'],
 'Your task needs five extra minutes. Revise the handoff plan and ask whether it still works for the other person.',
 'I need five more minutes to finish the labels. Would handing over the tablet at 2:15 leave enough time for your task? If not, let’s check the priority.'),
3:('Check before you guess',['Spot the missing detail','Confirm the change','Restate the plan'],[
 'Two instructions may conflict or leave something out. Name the exact difference. Ask the person responsible which instruction to use before doing work that may need redoing.',
 'Say the confirmed plan back in your own words. You can ask for an example or written steps. The useful test is whether you know what to do next.'],
 'The responsible person confirms destination first, then size within each destination. Rewrite your reply to check that order.',
 'I will group the boxes by destination first, then by size within each group. Is that the order you want? Could you show me one finished group?'),
4:('Report a problem clearly',['State what happened','Update the next step','Check the report'],[
 'Say what happened and where. Give the size of the problem if you know it. A specific report helps someone act more than blaming a person.',
 'Separate what you know from a possible cause. Say what is already done and which decision or item you need. Update the report if new information changes the task.'],
 'Two replacement pages arrive, but one is still missing. Update your report with what is now complete and what you still need.',
 'Two of the three packs now have page two. One still needs a copy. Could you print one more, or confirm whether to hold that pack?'),
}

DIGITAL={
5:('Check an AI claim',['Separate claim and evidence','Protect private details','Explain your checks'],[
 'AI can produce a convincing answer that is wrong. A real-looking picture, confident sentence or working link is not proof. Find evidence for the claim itself.',
 'You cannot reliably prove who made something from style alone. Check sources, dates and context. Keep passwords, personal documents and other people’s private details out of a practice prompt.']),
6:('Use AI and keep the skill',['Ask for the right help','Verify the result','Explain your correction'],[
 'Choose the job before asking a tool. For learning, ask for one hint or a worked example you can inspect. Do the next step yourself and explain the method.',
 'Check the answer against numbers or trustworthy sources. Revise errors and say what help you used. A polished answer is still your responsibility to understand before you rely on it.']),
7:('Make a plan you can actually use',['Budget time and money','Handle a delay','Keep a backup'],[
 'Work backwards from an appointment time. Include travel, waiting and preparation. Use money you actually have. List what to bring and which details need confirming.',
 'A delay or extra cost changes the plan. Update the numbers and choose a workable backup. Ask for help early when the plan no longer fits; do not hide the missing time or money.']),
8:('Build toward your own laptop',['Name the intended jobs','Show useful skills','Check the actual offer'],[
 'Start with what you want the computer to do. Check the exact model, supported software, battery, charger and ownership locks. An i5 label alone does not show what a laptop can run.',
 'Prepare a small project you can explain: a checked budget, useful email, source note and corrected AI draft. Rewards depend on your mentor’s actual agreed offer and secured stock. Points do not automatically buy a laptop.']),
1:('Save, find and share your work',['Save a usable file','Plan a recovery','Check the sharing'],[
 'An app helps you do a task. A file holds the work. A folder groups files. Save with a name you can find again. A screenshot is not the same as an editable document.',
 'Before sharing, check the file, the person and the permission. Viewer and editor are different roles. A cloud copy needs the right account and a completed sync; plan how you would recover it.']),
2:('Write an email someone can use',['Plan a useful address','Write the message','Revise before sending'],[
 'A professional email address can use a name or initials with a neutral addition. It does not need a paid service. Avoid a full birth date or other private details in the address.',
 'Check the recipient. Use a subject that names the purpose. Add the key detail and a clear question or next step. Check any attachment before sending. This lesson only makes a practice draft.']),
3:('Check where information came from',['Read the source','Check the date and place','Resolve a difference'],[
 'A logo or search title can be copied. Read the website address and find who runs it. Canadian government services often use canada.ca, gc.ca or official provincial domains; .gov is not the only official ending.',
 'Check the date, location and original source. A screenshot may leave those out. Several pages repeating one announcement are still relying on one source. Use the current service page for a current service question.']),
4:('Pause a suspicious message',['Spot the pressure','Verify another way','Plan a recovery'],[
 'A message may use urgency, fear or a reward to rush you. Pause before clicking, paying or sharing a code. A familiar logo or sender name can be copied.',
 'Use a trusted contact method you find separately, not the message’s link. If you entered a password, use the real service to secure the account and ask a trusted person for help. Do not enter real passwords here.']),
}

def draft_task(ident,w,second=False):
    return task(ident,'Improve your draft' if second else w.get('title','Make something useful'),w.get('rework',w['task']) if second else w['task'],'draft',
       'Write your version, then read each self-check. Improve one detail before saving a revised draft.' if second else 'Start with one useful sentence. Use the example if you need a starting point, then write your own version.',
       'Your draft is ready for the next part. Your mentor will review its meaning and clarity.',checks=w['checks'],example=w['example'],revise=second)

def evidence_task(ident,scene,title):
    return task(ident,title,scene['prompt'],'evidence','Read each line. Keep the lines that answer the task, not just lines that are true.',scene['why'],lines=scene['lines'],answer=scene['answer'])

def install(u,title,goal,objectives,labs,needs,label,lessons=None,reflection=None):
    if lessons:u['lessons']=lessons
    u.update(spec(title,goal,u['why'],objectives,u['lessons'],labs,u['review'],reflection or u['reflection'],needs))
    u['mission']['label']=label;u['workshop']={'kind':'scenario'}
    for i,q in enumerate(u['practice']):q.setdefault('lesson',1+i%2)

def attach(units):
    for u in units:
        n=u['grade'];sid=u['subject']
        if sid=='reading' and n in READING:
            title,goal,objectives,lessons=READING[n];w=u['workshop']
            if n in READING_BODIES:
                for l,body in zip(u['lessons'],READING_BODIES[n]):l['body']=body
            labs=[[evidence_task(f'reading-{n}-{i}',s,'Find the detail' if i==0 else 'Check the changed situation')] for i,s in enumerate(w['scenes'])]
            install(u,title,goal,objectives,labs,[f'reading-{n-1}'],'Read / understand / use',lessons)
        elif sid=='writing' and n in WRITING:
            title,goal,objectives,bodies=WRITING[n];w=u['workshop']
            for l,body in zip(u['lessons'],bodies):l['body']=body
            if n in WRITING_WHY:
                for l,why in zip(u['lessons'],WRITING_WHY[n]):l['whyItWorks']=why
            if n==2:w['checks']=['Each sentence gives a whole thought.','The reader knows who does each action.','They and it clearly point to someone or something.']
            if n==3:w['checks']=['The steps are in the right order.','Each step says what to do.','There is a check at the end.']
            install(u,title,goal,objectives,[[draft_task(f'writing-{n}-first',w)],[draft_task(f'writing-{n}-revised',w,True)]],[f'writing-{n-1}'] if n>1 else ['reading-1'],'Write / revise / use')
        elif sid=='social' and n in SOCIAL:
            title,objectives,bodies,change,example=SOCIAL[n];w=u['workshop']
            for l,body in zip(u['lessons'],bodies):l['body']=body
            checks=['I named the task or need clearly.','I made the next action or question clear.','I checked facts instead of guessing someone’s thoughts.']
            first=task(f'social-{n}-reply','Try a response',w['scene'],'conversation','Choose a response to see a possible effect. Then write the words you would use.',
                'You have a response to discuss with your mentor. The app does not grade your personality, eye contact or speaking speed.',replies=w['replies'],writePrompt=w['task'],checks=checks)
            revised=draft_task(f'social-{n}-changed',dict(task=w['task'],rework=change,example=example,checks=checks),True)
            install(u,title,u['goal'],objectives,[[first],[revised]],[f'social-{n-1}'] if n>1 else [],'Ask / agree / follow through',reflection=change+' Explain one choice in your reply.')
        elif sid=='digital' and n in DIGITAL:
            title,objectives,bodies=DIGITAL[n];w=u['workshop']
            for l,body in zip(u['lessons'],bodies):l['body']=body
            labs=[[evidence_task(f'digital-{n}-evidence-{i}',scene,'Check the choice' if i==0 else 'Handle a change'),draft_task(f'digital-{n}-draft-{i}',w,i==1)] for i,scene in enumerate(w['scenes'])]
            install(u,title,u['goal'],objectives,labs,[f'digital-{n-1}'] if n>1 else ['reading-1'],'Use / verify / keep control')
    for u in units:
        if u.get('mission',{}).get('kind')=='scenario':u['mission']['preparation']=[{'id':i,'title':next(v['title'] for v in units if v['id']==i)} for i in u['mission'].get('needs',[])]
