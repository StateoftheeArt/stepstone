"""Authored practical tasks, embedded in the existing lesson demonstrations."""

def evidence(prompt, lines, answer, why):
    return dict(prompt=prompt,lines=lines,answer=answer,why=why)

READING={
2:[
 evidence('Which sentence makes it clear who packed the bag?', ['Alex gave Sam the bag.','Sam packed it with notebooks.','They left later.'],[1],'Sam performs the packing. It refers to the bag; the earlier sentence alone only says who handed it over.'),
 evidence('Which wording leaves the owner of the notebook unclear?', ['Sam put Sam’s notebook in the bag.','Alex labelled the bag.','Sam gave Alex their notebook.'],[2],'Their could refer to Sam or Alex in this sentence. Ask whose notebook is meant rather than guessing.')],
3:[
 evidence('Select the instruction that must happen before the file is closed.', ['Save the file before closing it.','Collect the printout after it is printed.','If the printer is unavailable, wait for help.'],[0],'Before establishes a dependency: save first, close second. The order is encoded in the sentence, not guessed from a familiar routine.'),
 evidence('The printer is unavailable. Which instruction applies to that condition?', ['Collect the printout after it is printed.','If the printer is unavailable, wait for help.','The room has two windows.'],[1],'The condition is true, so this branch applies. It does not tell you to keep sending copies to an unavailable printer.')],
4:[
 evidence('Select the details that support “Jo is preparing for a trip.”', ['Jo checked the route and departure time.','Jo packed water and a jacket.','Jo’s bag is green.'],[0,1],'Checking the route and packing useful items both support preparation. Bag colour does not explain the main activity.'),
 evidence('Which sentence adds a claim that the source never established?', ['Jo checked the route.','Jo packed a jacket.','Jo is the most prepared traveller in the country.'],[2],'The source supports specific actions, not a comparison with every traveller. A summary must not introduce that claim.')],
5:[
 evidence('Select the context that tells you what “charge” means here.', ['The repair desk is beside the door.','The receipt lists a five-dollar delivery charge.','The receipt was folded.'],[1],'A receipt, a dollar amount, and delivery point to a fee. A battery meaning would not fit this context.'),
 evidence('Select the clue that helps interpret “the queue crawled forward.”', ['People waited a long time and advanced only a few steps.','The floor tiles were grey.','The desk had a sign.'],[0],'Slow progress supports a figurative meaning. The sentence does not establish that people moved on hands and knees.')],
6:[
 evidence('Select the details supporting the claim that the café was busy.', ['All twelve tables were occupied.','The queue extended to the entrance.','A clock hung above the counter.'],[0,1],'Occupied tables and a queue relate directly to demand. The clock may be accurately described without supporting this claim.'),
 evidence('Which sentence limits a claim about how busy the café always is?', ['The observations were made during one fifteen-minute visit.','The café serves drinks.','The door has a handle.'],[0],'One short visit does not establish a pattern across every day or hour. Keep the conclusion within the observation’s scope.')],
7:[
 evidence('Select the clues that make recent rain a reasonable possibility.', ['The pavement is wet.','Several people are folding wet umbrellas.','The shop closes at six.'],[0,1],'The two observations together support rain as a possibility. They do not prove exactly when it rained or rule out every alternative.'),
 evidence('Which new detail should make you revise the rain explanation for this wet floor?', ['The floor was dry ten minutes ago.','A cleaner has just washed it and placed a wet-floor sign.','The room has a clock.'],[1],'This directly explains the wet floor. Updating an inference when evidence changes is careful reasoning.')],
8:[
 evidence('Select the details that limit “everyone prefers this app.”', ['Nine of ten people surveyed preferred the app.','All ten were friends of its creator.','The logo is green.'],[0,1],'Both the small number and the selected group limit the claim. The result describes these respondents, not everyone.'),
 evidence('Which detail matters when an article is shared as news from today?', ['The headline is in bold.','The page has many shares.','The reported event happened three years ago.'],[2],'The event date tells you whether the claim is current. Shares and headline style do not make an old event new.')],
9:[
 evidence('Select both details that explain why these accounts could be compatible.', ['At 8 am, the bus had no empty seats.','At 10 am, the same bus had many empty seats.','Both accounts use black text.'],[0,1],'They describe different times. Both can be true without either author being dishonest.'),
 evidence('Select both counting definitions that need to be reconciled.', ['Report A counts 20 entries through the door.','Report B counts 15 different people; some entered twice.','The door was recently painted.'],[0,1],'Entries and unique people are different units. Repeated visits can account for the numerical difference.')],
10:[
 evidence('Select the evidence offered for keeping the library open later.', ['The proposal is to extend the opening hours.','The evening trial recorded 60 additional visits per week.','The writer feels strongly about libraries.'],[1],'The visit count is evidence about demand. The proposal is the claim, and strong feeling alone is not evidence of use.'),
 evidence('Select the relevant counterargument that still needs an answer.', ['Extra evening staffing would need a budget.','The proposal has four paragraphs.','The writer uses a blue pen.'],[0],'Staffing cost affects feasibility. Answering that concern would improve the plan rather than attack its author.')],
11:[
 evidence('Which source most directly answers when this event is scheduled?', ['A dated schedule from the organizer, updated this morning.','A repost that does not name its source.','A comment remembering last year’s event.'],[0],'The organizer’s current schedule directly addresses the question. You would still check for later change notices.'),
 evidence('Which detail shows that three pages are not three independent confirmations?', ['The pages use different colours.','All three link back to the same original announcement.','The titles have different lengths.'],[1],'Repeating one source does not add independent observations. Trace the origin before counting confirmations.')],
12:[
 evidence('Select the statements showing a shared goal but different priorities.', ['Ari wants a route with the lowest fare.','Jo wants a route with fewer transfers because transfers are difficult for them.','Both want to reach the same appointment on time.'],[0,1,2],'All three are needed to compare this decision fairly: the goal is shared, while cost and transfer burden receive different weight.'),
 evidence('Which next step would help compare the options fairly?', ['Assume the cheaper route is always better for everyone.','Compare fares, travel times, and transfer requirements for the actual trip.','Choose whichever person speaks fastest.'],[1],'A common comparison frame makes the tradeoff visible. It does not erase the people’s different needs.')],
}

# The learner writes into the existing reflection field, then improves that same
# draft in the second lesson. Model answers are examples, never automatic grades.
WRITING={
1:('Arrange a meeting','Write a message arranging to meet someone. Include the place, time, and anything they need to bring.',['The reader knows the action.','The time and place are specific.','The message does not assume a missing detail.'],'Meet me at the library’s west entrance at 3 pm. Please bring the form. Let me know if that time does not work.','The time changes to 4 pm. Revise your message so the current plan is unmistakable.'),
2:('Make the sentence clear','Write two sentences about someone helping another person with a task.',['Each sentence contains a complete thought.','The reader can tell who does each action.','Any pronoun has a clear reference.'],'Sam carried the box to Alex. Alex put it on the labelled shelf.','Combine the sentences if useful, then check that the person doing each action is still clear.'),
3:('Write usable instructions','Write three steps for saving and sharing a file with someone.',['The steps are in the order the reader needs.','Each step starts with a clear action.','The reader can tell when the task is complete.'],'1. Save the file with a clear name. 2. Attach that saved file to the message. 3. Check the recipient and attachment before sending.','Add what the reader should do if the attachment is missing. Keep the main sequence easy to follow.'),
4:('Build one useful paragraph','Write a paragraph explaining why a shared workspace needs labelled storage.',['The paragraph has one main point.','Details support that point.','The connection between the details and point is explained.'],'Labelled storage helps people find the right supplies. A label can identify both the item and its usual location. This reduces searching and makes it easier to return supplies after a task.','Remove an unrelated detail if there is one, then strengthen the link between your example and main point.'),
5:('Describe so someone can act','Describe a damaged container to someone who cannot see it. Invent harmless practice details.',['I name the object and its location.','I describe an observable feature precisely.','I separate what I saw from a guess about its cause.'],'The clear storage box on the lower shelf has a crack about two centimetres long beside the handle. I do not know what caused it.','Revise one vague description into a quantity, location, or feature that another person could check.'),
6:('Ask for the missing information','You have ten boxes to label but no list of names. Write the request you would send.',['I state what I already know.','I identify the particular missing information.','I ask for an action the receiver can take.'],'I have the ten boxes ready to label. Could you send the list of names and confirm which name goes on each box?','You need the list before starting at 2 pm. Add that constraint without pretending the other person has already agreed.'),
7:('Explain a process','Explain how someone can check whether change from a purchase is correct.',['The steps are in a useful order.','I explain why a step works.','I include a way to check the final result.'],'Subtract the price from the amount paid to find the change. Then add the price and change. If the total matches the payment, the two parts rebuild the amount paid.','Add a different numerical example and explain why the same method still works.'),
8:('Support a claim','A survey of 20 club members found that 14 preferred Saturday meetings. Write a supported recommendation.',['I report the actual evidence.','I connect the evidence to my recommendation.','I keep the sample’s limits visible.'],'Saturday may be a useful meeting day for this club: 14 of the 20 surveyed members preferred it. We should still check whether the remaining members would be excluded by that time.','Revise your recommendation to address a member who can never attend on Saturday.'),
9:('Revise for the receiver','Rewrite: “It’s not working. Sort it out soon.” Use a harmless made-up file-sharing problem.',['I identify the particular problem.','I say what action or help is needed.','I replace vague timing with useful information.'],'I cannot open the planning document because the link says access denied. Could you check my access before our 2 pm meeting?','Check your revision for an unsupported assumption or unnecessary detail and improve it.'),
10:('Send a clear work update','Write a short update saying what is finished, what is blocked, and what you need next.',['The main point appears early.','Finished and unfinished work are distinguishable.','The next action and responsible person are clear.'],'The first eight information packs are finished. The last two need a missing page. Could you send that page so I can complete them before collection?','Add a realistic alternative if the missing page cannot arrive in time.'),
11:('Make a reasoned proposal','Argue for keeping a quiet working area in a shared room. Include a relevant objection.',['I state a clear proposal.','I give a reason and explain it.','I answer a fair objection without attacking anyone.'],'A designated quiet area would give people somewhere to concentrate. The room still needs space for discussion, so we could keep one table quiet and use the other side for group work. A short trial would show whether this division helps.','Add a way to evaluate the trial rather than claiming everyone will benefit automatically.'),
12:('Plan a small project','Propose a small shared activity. Include its purpose, actions, people, resources, and a way to check the result.',['The scope and next action are feasible.','The resources and responsibilities are explicit.','I distinguish confirmed resources from requested support.'],'I propose a one-hour shared repair-planning session. Two volunteers would help list faults and needed parts. We already have paper and pens; any tools or purchases need separate agreement. We would finish with a safe next-step list for each item.','The available budget is smaller than expected. Revise the scope and state what can still be achieved without promising unfunded purchases.'),
}

SOCIAL={
1:('You have been asked to label boxes, but you have not seen the labelling method.',[
 ('Could you show me one example, then watch me try the next one?','The other person may demonstrate the first box. You can then check your understanding by doing one yourself.'),
 ('Could you write the steps down?','A written list may give you something to refer back to. You can ask about any step that remains unclear.'),
 ('I will say I understand and guess.','The boxes may need redoing because the missing method has not been clarified. You can still pause and ask before continuing.')],'Write the specific question you would ask if the example still leaves something unclear.'),
2:('Two people need the same tablet to finish separate parts of a shared task.',[
 ('Can we agree which part comes first and how we will hand it over?','An explicit order can make the handoff predictable. Check whether either task has a real deadline.'),
 ('I need five more minutes. Will that leave you enough time?','You give a concrete estimate and invite a check of the other person’s needs. The estimate may need adjusting.'),
 ('I will keep it until they stop asking.','The other person still cannot plan their part. A clear agreement would provide more useful information.')],'Write a short handoff agreement that both people could check.'),
3:('One instruction says to sort boxes by size. Another says to sort them by destination.',[
 ('I have two different sorting instructions. Which one takes priority?','The responsible person can clarify the intended result before you spend time sorting.'),
 ('I can label destinations while we confirm the order, if that helps.','This may be useful only if labelling is already agreed and safe. Check before treating a proposed workaround as an instruction.'),
 ('I will choose one and say the instructions agreed.','The conflict remains hidden, which can cause rework. Stating the conflict keeps the decision accurate.')],'Restate the confirmed instruction in your own words, including one detail you would verify.'),
4:('Three pages are missing from a set of information packs you are assembling.',[
 ('Three packs are missing page two. Could we print three replacement pages?','The report identifies the gap and proposes a concrete next step.'),
 ('I have finished the complete packs and set the incomplete ones aside.','This communicates useful progress. You still need to say which missing material or decision is needed.'),
 ('Someone has ruined the whole job.','The statement assigns blame and hides the scale of the problem. Naming the three missing pages would help solve it.')],'Write a factual problem report with one practical next step.'),
5:('A group has a deadline, but two tasks still have no named owner.',[
 ('Can we list the remaining tasks and agree who is doing each?','A visible allocation can reveal gaps and prevent duplicated work.'),
 ('I can take the checklist if someone else can finish the labels.','You offer a bounded contribution and identify the connected task that still needs agreement.'),
 ('I will assume somebody else has them.','The tasks may remain undone because no one has accepted responsibility.')],'Write a two-person plan with a check-in point and a clear handoff.'),
6:('A spoken explanation contains several steps, and you are losing track of the order.',[
 ('Could I have the steps in writing so I can check them as I go?','A written sequence may reduce the memory load. You can test whether it helps with the next step.'),
 ('Could we do the first step together, then I will try one?','A demonstration may make the process clearer. You can still request a written reminder afterward.'),
 ('I will hide that I missed the order.','The missing information is likely to remain. A specific support request gives the other person something useful to respond to.')],'Write an adjustment request that names the practical need without requiring personal disclosure.'),
7:('You must assemble ten packs by 2 pm, and the printer has stopped halfway through.',[
 ('The printer stopped after five packs. Should I finish those or ask for printing help first?','You report progress and ask the person responsible to clarify the priority.'),
 ('I can assemble the printed pages while we arrange the rest.','This may keep part of the work moving. Confirm that this approach fits the needed order and deadline.'),
 ('I will promise all ten will still be ready without checking.','The promise does not resolve the printing delay. A realistic update would allow a revised plan.')],'Describe a revised plan with one dependency, a time estimate, and a backup option.'),
8:('A teammate wants to move your materials, but you need the current arrangement to finish your task.',[
 ('I need this setup until I finish the labels. What space do you need right now?','This states a boundary and asks about the other person’s practical need.'),
 ('Could we keep this section in place and clear the other side?','A specific compromise might help if it meets both tasks’ needs. It still requires agreement.'),
 ('You always mess everything up.','A personal accusation may escalate the disagreement without identifying the space or timing problem.')],'Write a boundary and a practical question that could help clarify the disagreement.'),
9:('A message asks whether your task is ready. Most is finished, but one required detail is missing.',[
 ('Eight packs are ready. The last two need the updated page; could you send it?','The reply separates completed work from the blocker and requests a specific action.'),
 ('I can send the completed part now, if that is useful.','This offers a concrete option while leaving the receiver a chance to confirm what they need.'),
 ('Yes, all done.','The receiver may make a plan based on inaccurate information. A partial-progress update would be more useful.')],'Write the update you would send, with no unnecessary personal information.'),
10:('In a job conversation, you are asked for an example of learning a new task.',[
 ('Could I use an example from a project rather than paid work?','Relevant examples can come from several settings. You can describe what you did and learned honestly.'),
 ('Give me a moment to choose a specific example.','A brief pause can help you answer the actual question instead of rushing into a vague response.'),
 ('I will invent a job I have never had.','An invented example does not demonstrate your real experience and may create problems in follow-up questions.')],'Write a short answer with a situation, your action, and a result or lesson learned.'),
11:('Someone says your written instructions were hard to follow.',[
 ('Which step was unclear? Could you show me where you got stuck?','A specific example can turn a general comment into an actionable revision.'),
 ('I will read them from the start and check the order with you.','Testing the instructions together may reveal a missing step or assumption.'),
 ('That means I am bad at everything.','The comment concerns this piece of work. It does not establish a verdict about all of your abilities.')],'Write one specific revision you would try and how you would check whether it helped.'),
12:('People keep taking the wrong supplies from a shared shelf.',[
 ('Could we check the labels and observe where the confusion happens?','Gathering specific evidence can identify whether labels, layout, or missing information contribute.'),
 ('We could test clearer labels on one section and review what happens.','A small agreed trial can provide evidence before changing the whole system.'),
 ('I will move every item without telling anyone.','An unannounced change may create new confusion. Agreeing ownership and a trial would make the change easier to evaluate.')],'Propose a small agreed trial, name who should decide, and describe a result you could observe.'),
}

def attach(units):
    for u in units:
        sid,g=u['subject'],u['grade']
        if u.get('mission'):
            u['workshop']=dict(kind=u['mission']['kind'])
        elif sid=='reading':u['workshop']=dict(kind='evidence',scenes=READING[g])
        elif sid=='writing':
            title,task,checks,example,rework=WRITING[g]
            u['workshop']=dict(kind='writing',title=title,task=task,checks=checks,example=example,rework=rework)
            u['reflection']=task+' Explain one choice you made, then improve one detail.'
        elif sid=='social':
            scene,replies,task=SOCIAL[g]
            u['workshop']=dict(kind='conversation',scene=scene,replies=[dict(text=a,outcome=b) for a,b in replies],task=task)
            u['reflection']=task
        elif sid=='science':u['workshop']=dict(kind='science',model=g)
        else:u['workshop']=dict(kind='math')
    assert all(u.get('workshop') for u in units)
