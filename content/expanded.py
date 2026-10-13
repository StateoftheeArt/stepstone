"""Original foundation mini-courses. Each mapped level is one skill, not a school year.

Cases pair an application decision with an explanation. They are deliberately
readable, with close alternatives and explicit limits, rather than trick questions.
"""
from expanded_checks import CHECKS

SPECS=[]
def module(subject,grade,goal,body,example,steps,second,body2,steps2,cases,reflection):
    SPECS.append(dict(subject=subject,grade=grade,goal=goal,body=body,example=example,steps=steps,second=second,body2=body2,steps2=steps2,cases=cases,reflection=reflection))

module('reading',2,'Find who does what in a sentence.',
 'A sentence connects a person or thing with an action or state. Word order helps you tell who did what. In “Maya helped Lee”, Maya is the helper. In “Lee helped Maya”, the same words create a different meaning. Read to the end before deciding.',
 'Maya packed the red bag before lunch.', ['Find who: Maya.','Find the action: packed.','Find the detail: the red bag, before lunch.'],
 'Follow words that stand in for names','Words such as she, he, they, and it can point back to a person or thing. Check the surrounding sentence. If two names could fit, the message may need clarification; readers should not have to guess.',
 ['Read “Maya found the bag. She packed it.”','She refers to Maya; it refers to the bag.','If a sentence has two possible people, ask which person is meant.'],[
 ('Jo carried the box. Who carried something?','Jo','The box','Both Jo and the box','Jo is the person performing the action.'),
 ('The dog followed the cyclist. Who was in front?','The cyclist','The dog','The sentence says neither moved','Following places the dog behind the cyclist in this sentence.'),
 ('Lee found a key. They put it in a drawer. What does “it” mean?','The key','The drawer','Lee','The key is the object mentioned before the pronoun.'),
 ('The red bus passed the blue car. What was blue?','The car','The bus','The road','Blue describes car, not bus.'),
 ('Sam gave Alex their notebook. Whose notebook was it?','The wording is unclear; ask whose','Definitely Sam’s','Definitely Alex’s','Their could refer to either person without more context.'),
 ('Before leaving, Nia locked the door. What happened first?','Nia locked the door','Nia left','Both must happen at exactly the same time','Before sets the order even when the first action is written later.')],
 'Write a sentence about two people. Explain how a reader can tell who does what.')

module('reading',3,'Follow the order of a short set of instructions.',
 'Time words connect events. First starts a sequence; then moves it forward; before and after compare two events. Instructions can depend on earlier steps. Reading every step before starting helps you notice what you need.',
 'Before pouring juice, place the cup on the tray.', ['Name both actions: placing and pouring.','Before means the cup goes on the tray first.','Check the sequence against the complete instruction.'],
 'Notice conditions and exceptions','An instruction beginning with if only applies when its condition is true. Unless introduces an exception. Do not turn a conditional instruction into an instruction for every situation.',
 ['Read “If the door is locked, use the bell.”','Check whether the door is locked.','Use the bell in that situation; the message does not say to ring every time.'],[
 ('Wash the apple, then slice it. Which is first?','Washing','Slicing','Either order is stated','Then places slicing after washing.'),
 ('After you save the file, close the app. What comes last?','Closing the app','Saving the file','Opening a new file','After makes saving a prerequisite for closing.'),
 ('If it rains, meet inside. It is raining. Where is the meeting?','Inside','Outside','Cancelled','The stated condition is true, so the inside plan applies.'),
 ('Bring a towel unless you are only watching. You are only watching. What does the notice require?','No towel for watching','A towel for everyone','Two towels for watching','Unless creates an exception for people who are only watching.'),
 ('First log in. Next select Print. Finally collect the pages. What comes between login and collection?','Selecting Print','Collecting twice','Signing out','Next identifies the middle action.'),
 ('The note says “Put the lid on before carrying the cup.” What should you check before lifting it?','The lid is on','The cup has already been carried','The cup is empty','The lid step must precede carrying.')],
 'Write three instructions for an everyday task. Include before, after, or if, and explain the order.')

module('reading',5,'Use context to choose a precise meaning.',
 'A word can have several meanings. Context is the surrounding information that helps you choose. “Charge the tablet” refers to electrical energy; “a delivery charge” refers to a price. Test your chosen meaning by rereading the whole sentence.',
 'The battery is flat, so the tablet needs charging.', ['Flat can describe a shape or an empty battery.','Battery and charging point to stored energy.','Here flat means the battery has little usable charge.'],
 'Separate literal meaning from figures of speech','A phrase such as “give me a hand” can mean help rather than a body part. If a phrase is unfamiliar, asking for a literal version is a useful reading strategy. Precise words reduce guessing.',
 ['Read “The queue crawled forward.”','People probably moved slowly; the sentence need not mean crawling on hands and knees.','Replace crawled with moved slowly and check whether the idea fits.'],[
 ('“The shop will charge five dollars for delivery.” What does charge mean here?','Ask for payment','Fill a battery','Run towards something','A price and delivery identify the payment meaning.'),
 ('“The weather was mild, so we wore light jackets.” What does mild suggest?','Not very cold or hot','Dangerously cold','Completely dry all day','The clothing clue supports a moderate temperature, not a claim about rain.'),
 ('“Could you give me a hand with this box?” What is being requested?','Help with the box','A measurement of a hand','A new box','Give me a hand is a common expression for help.'),
 ('“The instructions are vague.” Which change would help?','Add specific steps and quantities','Use the same unclear words again','Make the letters smaller','Vague means not specific enough for the reader to act confidently.'),
 ('“The meeting ran over.” In a schedule discussion, what is likely meant?','It lasted beyond its planned end','People ran during the meeting','It ended early','The schedule context points to extra time.'),
 ('A notice says “bring suitable footwear”. What detail may still need checking?','Which footwear is suitable for the activity','Whether bring is an action word','Whether footwear can ever mean shoes','Suitable depends on the situation, so the instruction may need a concrete example.')],
 'Choose a word with two meanings. Write two sentences that make the intended meaning clear.')

module('reading',6,'Support a reading answer with a relevant detail.',
 'An answer is stronger when the text supports it. Start with your claim, identify a detail, and explain the connection. A quote is not automatically evidence for every claim: it must address the actual question.',
 '“The path was icy. Jo shortened their steps and held the rail.” Was Jo moving cautiously?', ['Claim: Jo was being cautious.','Evidence: shorter steps and use of the rail.','Connection: both actions can help Jo move carefully on ice.'],
 'Keep the claim within the evidence','Distinguish what the text states from what you infer. One example may support sometimes, but usually needs more evidence to support always. You can make a reasonable inference while acknowledging what remains unknown.',
 ['The text describes one trip on one icy path.','It supports caution on that trip.','It does not show that Jo is always cautious in every situation.'],[
 ('“Mina checked the route twice and packed a map.” Which claim is supported?','Mina prepared for the journey','Mina never gets lost','Mina dislikes travelling','Checking and packing support preparation, not universal claims.'),
 ('“The queue reached the door, and every table was occupied.” What detail supports a busy café?','Every table was occupied','The café had a door','Someone could count tables','Occupied tables directly relate to how many people are using the café.'),
 ('“I prefer the earlier bus because it gives me time to walk.” What is the stated reason?','Time for the walk','A lower fare','A better driver','The because clause explicitly names the reason.'),
 ('A text describes one successful garden trial. Which claim fits that scope?','This trial succeeded','Every garden method succeeds','The trial proves all plants grow equally','One trial supports a claim about that trial, with limits.'),
 ('A writer says a park is accessible and lists a step-free entrance. Why does the detail matter?','It supports one aspect of access','It proves every visitor has identical needs','It only describes the park’s colour','A step-free entrance supports a specific access feature, not every possible need.'),
 ('“The lights were off, but a voice came from inside.” Can you conclude the building was empty?','No; the voice is evidence against that conclusion','Yes; darkness always means empty','Yes; voices cannot be inside dark rooms','Check all relevant details, including those that challenge the first impression.')],
 'Write a claim about a short text, give one detail, and explain exactly how the detail supports it.')

module('reading',7,'Make an inference and check its limits.',
 'An inference connects clues with a reasonable explanation. It is more than copying a sentence, but it is not permission to invent facts. Say what you infer, name the clues, and consider another explanation.',
 'The pavement is wet. People carry folded umbrellas. Did it rain recently?', ['Wet pavement and umbrellas are clues.','Recent rain is a reasonable possibility.','A sprinkler or other explanation is possible; the clues do not prove the exact time.'],
 'Notice uncertainty in your wording','Words such as may, suggests, and probably can match incomplete evidence. A character being quiet does not prove anger or rudeness. Describe observable actions before assigning intentions or emotions.',
 ['Observe: Jo did not answer immediately.','Possible explanations include thinking, not hearing, or wanting time.','Ask for clarification instead of deciding you know Jo’s intention.'],[
 ('A person enters shaking water from an umbrella. What is a reasonable inference?','They may have been outside in rain','They must dislike the weather','They definitely walked for an hour','The water and umbrella support rain, but not feelings or travel duration.'),
 ('A character rereads the question and pauses. What can you safely infer?','They may be processing or checking it','They are definitely refusing to help','They do not know any answers','Several explanations fit a pause; avoid inventing intent.'),
 ('Boxes are stacked by the door and shelves are empty. What might be happening?','A move or reorganisation','Proof the place is permanently closed','Proof all belongings were stolen','The clues fit a move, but do not establish one specific cause.'),
 ('A bus stop is crowded after a long gap in arrivals. Which extra clue would help?','The service update and timetable','The colour of a passenger’s coat','The number of nearby trees','Information about service directly tests the delay explanation.'),
 ('“Pat glanced at the clock three times.” Which wording fits the evidence?','Pat may be watching the time','Pat certainly hates the meeting','Pat must have missed the bus','The behaviour suggests attention to time without proving a motive.'),
 ('A story later reveals the wet floor came from cleaning. What should happen to a rain inference?','Revise it using the new detail','Keep it because it came first','Ignore the new sentence','An inference should change when stronger evidence explains the clues.')],
 'Describe a clue, give two possible explanations, and name one detail that could distinguish them.')

module('reading',9,'Compare two accounts without flattening their differences.',
 'Two accounts can describe the same event from different positions. Compare the event, the observations, the time, and the purpose. A difference is not automatically a lie; a person may have seen only part of what happened.',
 'One report says the bus was crowded at 8. Another says seats were empty at 10.', ['Check whether the time is the same: it is not.','Crowding can change during a morning.','Both observations could be accurate for their stated times.'],
 'Resolve apparent conflicts with a fair comparison','Look for shared definitions and matching units. When accounts truly conflict about the same thing, keep the disagreement visible and seek evidence. Do not average incompatible claims just to make them agree.',
 ['Compare “twenty arrivals” with “twenty unique visitors”.','The same person might arrive twice.','Define what was counted before deciding the reports disagree.'],[
 ('A pool is busy in one report at 3 and quiet in another at 8. What should you check first?','The different times','Which title uses larger letters','Which writer sounds more confident','Time differences may explain both accounts.'),
 ('One account lists benefits of a new route; another lists costs. How should you compare them?','Consider both the benefits and costs','Discard all cost information','Assume benefits mean there are no costs','The accounts address different aspects of the same decision.'),
 ('Two reports disagree on the same start time. What would help?','The dated official schedule and any change notice','Picking the longer report','Assuming both times are equally usable','Relevant records can help resolve a factual timing conflict.'),
 ('One survey counts households and another counts individuals. What must you notice?','They use different counting units','The larger number must be more accurate','The numbers can be compared as identical measures','The unit affects the meaning of the number.'),
 ('A witness saw only the end of a game. What limits their account?','They cannot directly describe the unseen beginning','They cannot accurately describe anything','They must support the winning side','Scope matters: partial observation can still provide some reliable detail.'),
 ('Both accounts mention a power cut, but only one gives the duration. What is shared?','That a power cut occurred','Its exact duration','Its cause','Separate points of agreement from details found in only one source.')],
 'Compare two brief accounts. State one agreement, one difference, and what could explain it.')

module('reading',10,'Identify a claim, its reasons, and its limits.',
 'An argument asks you to accept a claim for stated reasons. Find the conclusion, the evidence, and the link between them. A strong feeling can explain why someone cares, but it does not by itself establish a factual claim.',
 '“Keep the library open later: evening visits increased during the trial.”', ['Claim: keep later opening hours.','Evidence: evening visits increased during the trial.','Missing detail: how much, over what period, and at what staffing cost?'],
 'Test assumptions and counterarguments','An assumption is an unstated idea needed for an argument to work. A counterargument offers a reason to question the conclusion. Addressing a relevant objection can strengthen a position; dismissing the person does not answer the objection.',
 ['Later visits alone do not tell us whether the added hours are affordable.','Compare additional use with staffing needs.','A limited trial may be a better-supported proposal than a permanent change immediately.'],[
 ('“Add bike racks because existing racks are full each weekday.” What is the claim?','Add bike racks','Existing racks are full','Weekdays exist','The claim is the action the writer wants accepted.'),
 ('A proposal cites three dated counts of full racks. What role do the counts play?','Evidence for demand','A definition of bicycles','Proof the proposal has no costs','Counts provide observations related to the proposed need.'),
 ('“Everyone will use the new room because my friends will.” What assumption is weak?','The friends represent everyone','The friends exist','Rooms can be used','A small group may not represent the wider group.'),
 ('A critic raises maintenance costs. Which reply addresses the point?','Compare likely costs with the available budget','Call the critic boring','Repeat the title of the proposal','Respond to the reason offered, not the person’s character.'),
 ('One short trial went well. Which conclusion is proportionate?','The result supports a longer trial with monitoring','The approach will always work everywhere','No more evidence could ever matter','A limited trial supports a cautious extension, not certainty in all settings.'),
 ('A popular creator endorses a product without evidence. What remains needed?','Relevant evidence for the product claim','More followers alone','A more dramatic slogan','Popularity does not establish whether a particular factual claim is true.')],
 'Write an argument map: claim, evidence, link, one assumption, and one fair objection.')

module('reading',11,'Find, evaluate, and acknowledge a useful source.',
 'Begin research with a question narrow enough to answer. Record who created a source, when, what evidence it uses, and what it can support. A search snippet is a lead, not a substitute for opening and understanding the source.',
 'Question: when does the community centre’s swimming session start this Saturday?', ['Find the centre’s current timetable.','Check the date and any closure or change notice.','Record the page title and address so the information can be checked again.'],
 'Keep source words separate from your explanation','A quotation uses a source’s exact words and needs clear attribution. A paraphrase explains the idea in your own sentence structure and still acknowledges its source. Changing a few words does not turn borrowed work into your own evidence.',
 ['Write a short note of the source’s main idea.','Set the source aside and explain that idea in your own words.','Check accuracy and include the source details required for the task.'],[
 ('You need this weekend’s opening hours. Which source is most directly relevant?','The venue’s current timetable and notices','An undated screenshot from last year','A comment guessing the hours','Current first-party scheduling information directly addresses the question.'),
 ('A search result gives part of a sentence. What should you do before citing it?','Open the source and read its context','Treat the fragment as the whole argument','Assume omitted words cannot change meaning','Context can qualify or change what a snippet appears to claim.'),
 ('You explain a source idea in your own words. What still matters?','Acknowledging the source','Pretending it is your own discovery','Keeping only every second original word','The idea’s origin still needs acknowledgement when paraphrased.'),
 ('A claim depends on a survey. Which detail helps evaluate it?','Who was surveyed and how','The page background colour','Whether the heading rhymes','Sampling affects what the survey can reasonably support.'),
 ('Two articles both repeat one original report. How many independent reports does that establish?','One original report','Two independent studies','Three independent studies','Repetition is not independent confirmation.'),
 ('A link is useful but may change later. What notes help a reader locate it?','Creator, title, date if available, address, and access information as required','Only “the internet”','Only the colour of its logo','Specific source details allow checking and distinguish similar pages.')],
 'Choose a research question. List what you would check in a source and how you would record it.')

module('writing',2,'Write a sentence that tells who does what.',
 'A useful sentence gives the reader a complete thought. A basic pattern is who or what, then an action or state. A capital letter and ending mark help readers find the boundaries. Simple sentences can be precise and effective.',
 'Fragment: “After the meeting.” Complete thought: “We cleaned the room after the meeting.”', ['Name who: we.','Add what happened: cleaned the room.','Keep the time detail and finish with a full stop.'],
 'Check meaning before decoration','More words do not automatically make a sentence better. Check that a pronoun has a clear referent, that your verb fits the subject, and that the reader can identify the action. Read aloud or use text-to-speech to hear missing words.',
 ['Draft: “They put it there.”','Ask who, what, and where if those details are not already clear.','Revise: “Jo put the receipt in the folder.”'],[
 ('Which sentence gives a complete thought?','The team checked the list.','After the team.','Because the list.','A subject and action form a complete thought in the first sentence.'),
 ('Which version makes the object clear?','Put the receipt in the folder.','Put it there, with no other context.','Put something somewhere.','Named objects reduce guessing when context is missing.'),
 ('Which ending fits a direct question?','What time does it start?','What time does it start.','What time does it start,','A question mark signals a direct question.'),
 ('Which version begins a standard written sentence correctly?','Mina opened the shop.','mina opened the shop.','opened the shop Mina','A capital begins the sentence; the standard order clearly names the actor.'),
 ('Which revision adds the missing action to “The two bags”?','The two bags fell.','The two heavy bags.','The two bags near the door.','Fell supplies what happened to the bags.'),
 ('Which sentence keeps a singular subject and verb aligned?','The box is open.','The box are open.','The box be opens.','The singular box pairs with is in this sentence.')],
 'Write two complete sentences about a real task. Point out the subject and action in one.')

module('writing',3,'Write instructions in a usable order.',
 'Instructions guide someone through a task. Give one main action at a time, name the things needed, and put prerequisites first. Use action verbs such as open, select, place, and check. Test whether a new reader could act without guessing.',
 'Save a document into a named folder.', ['Select Save as.','Choose the correct folder and type a useful file name.','Select Save, then check that the file appears in that folder.'],
 'Add checks and conditional steps','A final check catches errors. A conditional step begins with if and explains what to do when something differs from the usual case. Keep alternatives near the step where they are needed.',
 ['Name the expected result: the file is in the folder.','Add “If it is missing, check the selected location.”','Avoid telling someone to repeat every step without checking the problem.'],[
 ('Which instruction is easiest to act on?','Place the blue folder on shelf 2.','Sort that thing out.','Make it look right.','A named object, action, and location make the instruction usable.'),
 ('A cup must be under a tap before water runs. Which order fits?','Place the cup, then open the tap','Open the tap, then look for the cup','Only describe the colour of the cup','A prerequisite should appear before the action that needs it.'),
 ('Which is a useful final check after saving?','Open the folder and confirm the named file is present','Assume every click worked','Rename an unrelated file','The check directly confirms the expected result.'),
 ('Which instruction makes a condition explicit?','If the light is off, check the power switch.','The light might do things.','Always change every setting.','If links the action to the relevant condition.'),
 ('A beginner needs to copy a file. Which extra detail is useful?','The source folder and destination folder','A story about every file ever created','A decorative title with no location','The reader needs to know what to copy and where it should go.'),
 ('Which sequence word signals the last step?','Finally','Before starting','Meanwhile','Finally tells the reader this is the concluding step.')],
 'Write four steps for a safe everyday task. Add a final check and one if condition.')

module('writing',4,'Build a paragraph around one main point.',
 'A paragraph develops a connected idea. State the main point, add relevant details, and explain why they matter. A topic sentence is a guide, not a rule that every paragraph must sound the same. Remove details that lead the reader away from the purpose.',
 'Main point: a written checklist helped our group finish setup.', ['State the point in the first sentence.','Describe how the list made missing items visible.','Explain that checking each item reduced repeated work.'],
 'Link sentences without repeating yourself','Use linking words only when the relationship fits: because gives a reason, however signals a contrast, and for example introduces an illustration. Read the paragraph as a whole to check that each sentence earns its place.',
 ['Claim: the checklist helped.','Example: we noticed two missing chairs before people arrived.','Link: that example shows how the checklist caught omissions.'],[
 ('A paragraph explains why a bus pass is useful. Which detail belongs?','It allows several trips without buying a new ticket each time','My shoes are green','The café has a new sign','The ticket detail directly supports the paragraph’s point.'),
 ('Which sentence introduces a paragraph about a helpful checklist?','The checklist made our setup easier to organise.','Here are several unrelated things.','All objects have names.','A topic sentence guides the reader to the specific main point.'),
 ('Which word introduces a reason?','Because','However','Finally','Because connects a statement with why it happens or is justified.'),
 ('A detail seems interesting but unrelated. What is a useful revision?','Move it elsewhere or remove it','Repeat it three times','Let it replace the main point accidentally','A paragraph should stay focused on its purpose.'),
 ('Which link fits a contrast?','The room was small; however, it had enough seats.','The room was small because it had enough seats.','The room was small, for example enough seats.','However signals a contrast between small size and sufficient seating.'),
 ('What should an example do in a paragraph?','Make the main idea more concrete','Replace every explanation with a new topic','Add length without relevance','A good example demonstrates the idea the writer is developing.')],
 'Write a four-sentence paragraph: main point, detail, example, and why it matters.')

module('writing',5,'Replace vague description with useful detail.',
 'Precision means giving the detail the reader actually needs. Names, locations, quantities, and observable features are often more useful than good, bad, big, or soon. Do not add unnecessary private details just to make writing longer.',
 'Vague: “The thing near there is broken.” Precise: “The left wheel on the blue cart is loose.”', ['Name the object: blue cart.','Locate the issue: left wheel.','Describe what you observed: loose, not a guessed cause.'],
 'Separate observation from judgement','An observation tells what you noticed. A judgement adds your interpretation. Both can have a place, but label uncertainty. “The screen went dark twice” is more useful in a report than “this tablet is terrible”.',
 ['Record the observable behaviour.','Include a time or condition if it helps reproduce the issue.','Avoid stating an untested explanation as a fact.'],[
 ('Which description best locates an item?','The red folder on the second shelf','That stuff over there','The nice-looking thing','Specific colour, object, and shelf help the reader locate it.'),
 ('Which request gives a clear time?','Please send it by 3 pm today','Please send it soon','Please send it at some point','A time and day reduce uncertainty about soon.'),
 ('Which report is an observation?','The screen turned off twice during the video','The tablet wants to annoy me','The maker definitely used bad parts','The first statement describes an observable event without inventing intent or cause.'),
 ('Which detail makes “bring cups” more useful?','Bring six clean cups','Bring some appropriate things','Bring cups, maybe','A quantity and condition help the reader meet the request.'),
 ('A room felt cold to you. Which wording preserves that distinction?','The room felt cold to me; I did not measure the temperature','The room was exactly 10 degrees','Everyone felt equally cold','A personal observation is valid, but it is not a measured temperature.'),
 ('Which description best supports finding a damaged parcel?','Box 14 has a tear on its upper-left corner','A box looks weird','All parcels are probably damaged','A label and location point to a checkable issue.')],
 'Rewrite one vague message using an object, location, and observable detail.')

module('writing',7,'Explain a process and why its steps work.',
 'A process explanation does more than list commands. It connects steps to their purpose, so someone can adapt when conditions change. Start with the goal and needed materials or information. Explain decisions where a beginner might otherwise guess.',
 'Check a shopping total before paying.', ['Add each item price to make a subtotal.','Include any stated extra charges or discounts using the given rules.','Compare the resulting total with the amount available.'],
 'Use a concrete example, then state the pattern','A worked example shows the method on one case. Afterwards, say what stays the same when numbers or materials change. Keep important exceptions visible instead of hiding them in a long paragraph.',
 ['Explain one example in order.','Name the general rule used at each step.','Give one changed situation and explain which step would need adapting.'],[
 ('Which sentence explains why as well as what?','Check the name so the file goes to the intended person','Click something','Do the usual action','The purpose helps the reader understand the check.'),
 ('Where should a required material be mentioned?','Before the step that needs it','Only after the process is finished','Nowhere if the writer already knows','Readers need time to prepare required materials.'),
 ('What makes a worked example useful?','It shows the method applied to a specific case','It adds unrelated facts','It replaces the method with the answer alone','The learner can see how the general method produces a result.'),
 ('A process has two possible paths. What should the explanation state?','The condition for choosing each path','One path with no mention of the other','That any choice gives the same result','Conditional choices need criteria so the reader can choose appropriately.'),
 ('Which link explains a purpose?','Save a copy so the original is preserved','Save a copy although folders exist','Save a copy, meanwhile blue','So connects the step with its intended result.'),
 ('A reader gets stuck between steps two and three. What revision helps?','Explain the missing decision or action between them','Make the heading larger only','Delete both steps','A process explanation must include the transition the reader cannot infer.')],
 'Explain a process in four steps. Add a because or so statement to two steps.')

module('writing',8,'Connect a claim with evidence and explanation.',
 'Evidence helps a reader evaluate a claim. State the point, give a relevant observation or source detail, then explain the connection. Do not let a quote speak for itself when the connection needs explaining. Record where outside evidence came from.',
 'Claim: the new sign helped people find the room.', ['Evidence: fewer visitors asked for directions during the recorded trial.','Link: fewer requests may indicate easier navigation.','Limit: visitor numbers and other changes could also affect the count.'],
 'Revise claims that are too strong','Match your wording to the evidence. Some and during this trial may be more defensible than everyone and always. Include evidence that challenges your view when it is relevant; explain rather than hide it.',
 ['Avoid saying the sign solved every access issue.','State the observed change and the trial dates.','Suggest what else should be measured to check the explanation.'],[
 ('Which evidence fits a claim that a route is quicker?','Travel times measured on comparable trips','The colour of the bus','The writer’s favourite seat','Comparable travel times directly address speed.'),
 ('What should follow a quoted detail in an argument?','An explanation of how it supports the point','An unrelated new topic','A claim that quoting proves everything','The writer needs to connect the evidence to the argument.'),
 ('Ten people answered a survey. Which claim stays within its scope?','Seven of these ten respondents preferred option A','Everyone prefers option A','No one could prefer option B','The result describes the respondents, not the entire population.'),
 ('You paraphrase an external report. What should you include?','Source acknowledgement','A claim that you collected its data','Only a new title','Paraphrasing does not remove the need to acknowledge borrowed evidence.'),
 ('One measurement contradicts your expectation. What should you do?','Record and discuss it honestly','Delete it without explanation','Change the number to match','Unexpected evidence is still evidence and may reveal variation or a problem.'),
 ('Which sentence links evidence to a claim?','The shorter queues suggest the extra desk improved service during the trial','Here is a number, with no explanation','The title is attractive, therefore the claim is true','The first sentence explains a relevant connection while keeping a trial limit.')],
 'Write a claim, one supporting detail, its source or how it was observed, and a limitation.')

module('writing',9,'Revise a message for its reader and purpose.',
 'Revision changes meaning, organisation, and clarity. Proofreading checks details such as spelling and punctuation. First ask what the reader needs to know or do. A friendly group message and a formal request can share facts while using different amounts of explanation.',
 'Draft: “It changed, tell them.”', ['Identify the reader and the action they need to take.','Name what changed: the meeting moved from 2 to 3.','Name who needs the update and ask for confirmation if necessary.'],
 'Use a two-pass check','On the first pass, check information and order. On the second, check wording and mechanics. Reading aloud can reveal missing words, but clear meaning matters more than making every message sound elaborate.',
 ['Content: are the date, time, place, and request correct?','Clarity: can pronouns or vague words confuse the reader?','Proofread the final version after larger changes are made.'],[
 ('A reader cannot tell which meeting changed. What should you revise first?','Name the meeting and its new details','Only replace a comma','Add more adjectives','Missing essential information is a meaning problem, not just punctuation.'),
 ('Which task is proofreading?','Checking a misspelled word','Reordering an entire argument','Deciding the main purpose','Proofreading focuses on surface details after the content is settled.'),
 ('A short text to a teammate omits the deadline. What should you add?','The specific date or time needed','A longer greeting only','Unrelated personal information','A deadline lets the reader plan the requested action.'),
 ('Which revision reduces ambiguous pronouns?','Jo will send the file to Lee','They will send it to them, with no context','It will go there','Specific names and objects help when references are unclear.'),
 ('A reader is unfamiliar with an abbreviation. What helps?','Write the full term first or explain it','Use several more unexplained abbreviations','Assume confusion means they cannot learn','Writers can adapt terminology to their reader’s knowledge.'),
 ('Which order is usually efficient for a practical request?','Purpose, necessary details, next action','Unrelated history, no request','Several endings before the purpose','Readers can act more easily when the point and next step are clear.')],
 'Write a short message, then revise it for someone who lacks your background knowledge. Explain two changes.')

module('writing',11,'Develop a reasoned argument with a fair counterpoint.',
 'A reasoned argument gives a position and supports it. Define the question before gathering evidence. Each paragraph should advance a reason, with relevant support and an explanation. A strong argument can acknowledge uncertainty without giving up its central point.',
 'Proposal: trial a quiet work area in a shared room.', ['Reason: some tasks need fewer interruptions.','Evidence plan: compare usage and feedback during a trial.','Limit: the space must still meet other users’ needs.'],
 'Answer the strongest relevant objection','Represent another view fairly. Then explain whether it changes, limits, or fails to overturn your conclusion. A compromise should follow the evidence and purpose, not merely split every difference.',
 ['Objection: a permanent quiet area could reduce space for group work.','Response: try specified hours and measure demand for both uses.','Conclude with a testable proposal rather than a guarantee about everyone.'],[
 ('What belongs in an argument’s opening?','The question and position being developed','A conclusion unrelated to the question','Only a dictionary entry for every word','The reader needs to understand the issue and proposed position.'),
 ('Which counterargument is relevant to later opening hours?','Extra staffing and operating costs','The writer’s favourite colour','The length of the title','Costs bear directly on whether the proposed change is practical.'),
 ('How should an opposing view be represented?','Accurately enough that its supporter could recognise it','As an obviously absurd version','Without checking what it says','A fair response addresses the real objection.'),
 ('A trial supports a benefit but the sample is small. What conclusion fits?','Extend the trial and collect broader evidence','Guarantee the benefit for every person','Hide the sample size','The limitation suggests a next evidence step rather than false certainty.'),
 ('What makes evidence relevant?','It bears on the reason or claim being considered','It contains any number','It agrees with the writer’s mood','Relevance depends on the connection to the argument, not mere appearance.'),
 ('Which ending follows a balanced argument?','A clear position with its conditions and next step','An unrelated new accusation','A claim that objections no longer exist','A conclusion can state a position while preserving important limits.')],
 'Write a position, two reasons, a fair objection, and your response. State one limit on your conclusion.')

module('writing',12,'Write a practical project proposal.',
 'A proposal helps someone decide whether to support an action. Explain the need, the intended result, the plan, resources, responsibilities, and how success will be checked. Keep facts, estimates, and open questions distinct.',
 'Proposal: organise a shared shelf for borrowed games.', ['Need: people cannot find or return games consistently.','Plan: label spaces and add a checkout sheet.','Check: compare missing items and ease of use before and after a short trial.'],
 'Make the plan reviewable','A reader should be able to tell who does what, by when, with what resources. Identify a realistic risk and a response. Success measures should match the goal; counting posters made does not show whether people can find the shelf.',
 ['List materials and estimated costs with assumptions.','Assign steps and a review date.','Choose an outcome measure and explain what would lead to a revision.'],[
 ('Which proposal element describes the problem to solve?','The need','The decorative cover','The appendix title alone','The need explains why the proposed work is worth considering.'),
 ('A cost is not yet confirmed. How should it be written?','As an estimate with its assumption','As a guaranteed exact price','Omitted from every version','Labelling estimates lets the reviewer judge uncertainty.'),
 ('The goal is easier book finding. Which success measure fits?','Time or effort needed to find selected books','Number of fonts used on labels','Length of the proposal','The measure should reflect the intended outcome.'),
 ('Which plan makes responsibility clear?','Lee labels shelves by Friday; Jo checks the list Saturday','Someone does it soon','Everything happens eventually','Named roles and dates make the plan actionable.'),
 ('A possible delay is identified. What belongs beside it?','A response or alternative plan','A promise delays are impossible','Only a larger heading','A risk is more useful when paired with a practical response.'),
 ('What should a proposal request from its reader?','A specific decision, support, or next discussion','Agreement to unspecified future work','Only praise for writing it','The reader needs to know what action is being sought.')],
 'Draft a small proposal with need, goal, three steps, resources, one risk, and a success check.')

module('science',1,'Describe what you observe without guessing the cause.',
 'An observation is information you notice or measure. You can describe colour, shape, number, sound, or change. An explanation tries to say why it happened. Keeping these separate makes it easier to compare ideas fairly.',
 'There are drops of water on the outside of a cold cup.', ['Observe the drops and where they are.','Do not immediately conclude the cup leaks.','List a question: where did the outside water come from?'],
 'Use tools and repeatable descriptions','A measurement connects a number to a unit and a tool. Different observers can compare “the pencil is 14 centimetres long” more easily than “the pencil is big”. Do not taste unknown materials to investigate them.',
 ['Choose a suitable tool, such as a ruler.','Read from the same starting point.','Record the value and unit, and note if the reading is approximate.'],[
 ('Which statement is an observation?','The leaf has three brown spots','The plant is definitely angry','The soil must be useless','Spots can be observed; feelings or causes are interpretations.'),
 ('Which description is easiest to compare?','The line is 12 centimetres long','The line is huge','The line is the best','A measurement with a unit allows a clearer comparison.'),
 ('A cup has water outside it. What is a question rather than a conclusion?','Where did the water come from?','It definitely leaks','Someone certainly spilled it','A question keeps possible explanations open.'),
 ('Which tool measures length?','A ruler','A clock alone','A colour chart alone','A ruler has marked units for comparing length.'),
 ('What is missing from “the length is 8”?','The unit','The writer’s favourite colour','A louder voice','Eight centimetres and eight metres describe very different lengths.'),
 ('Two observers disagree about an object’s length. What helps?','Use the same units and starting point, then remeasure','Vote without measuring','Choose whichever number is larger','A shared method makes measurements comparable.')],
 'Describe an object with three observations and one measurement. Add a question about it.')

module('science',2,'Choose a material using a relevant property.',
 'Objects are made from materials with properties. A property is something such as flexibility, transparency, hardness, or ability to absorb water. An object’s purpose determines which properties matter. A material is not best for every job.',
 'Choose material for a window that lets you see through it.', ['Need: light and a clear view must pass through.','Relevant property: transparency.','Also consider strength and how the window will be used.'],
 'Test the property you actually need','A comparison should use the same method for each sample. A flexible material can bend; a brittle material can break instead. Waterproof and absorbent describe different behaviours. Avoid using appearance alone as proof.',
 ['Question: which cloth absorbs more water?','Use equal-sized samples and the same starting amount of water.','Compare absorbed amounts, rather than choosing the brightest colour.'],[
 ('Which property helps a towel dry a spill?','Absorbency','Transparency','Electrical brightness','A towel needs to take in water.'),
 ('A cover must keep rain off a bag. Which property matters?','Resistance to water passing through','Ability to soak up as much water as possible','Sweet smell','The purpose is to block water rather than absorb it into the contents.'),
 ('A ruler bends and returns without breaking. Which property is shown?','Flexibility','Complete transparency','High temperature','Bending describes flexibility, not colour or temperature.'),
 ('What makes an absorption comparison fairer?','Equal-sized samples tested with the same method','A huge sample against a tiny one','Different starting water amounts with no record','Size and method affect how much water a sample can take in.'),
 ('A window lets you see clearly through it. What property is useful here?','Transparency','Absorbency','Magnetism','Transparent materials transmit enough light for a clear view.'),
 ('Why might two objects need different materials?','Their jobs require different properties','One material is always best','Colour decides every property','A suitable choice depends on the purpose and constraints.')],
 'Choose an everyday object. Explain two properties its material needs and why.')

module('science',3,'Explain how a habitat meets living things’ needs.',
 'A habitat is the place where an organism lives. Living things need resources and suitable conditions, such as water, food or an energy source, and space. Different organisms need different ranges of temperature, light, and moisture.',
 'A pond supports several kinds of living things.', ['Plants use light and available resources.','Animals obtain food and use suitable parts of the habitat.','Changes to water or shelter can affect more than one organism.'],
 'Trace a food relationship','A food chain represents energy passing between organisms. In a simple chain, an arrow points from the food source to the consumer. It is a model of one pathway; real habitats often have many connected pathways.',
 ['Grass is eaten by a grasshopper.','A bird eats the grasshopper.','Draw arrows grass → grasshopper → bird to show the direction of energy transfer.'],[
 ('Which habitat feature directly meets a bird’s need for water?','An accessible water source','Only the colour of a sign','A name for the park','Water availability is a resource the bird can use.'),
 ('In grass → rabbit → fox, what does the rabbit eat in this model?','Grass','Foxes','The arrow itself','The arrow runs from the food source to the consumer.'),
 ('What can happen when shelter is removed?','Organisms that use it may be affected','Every organism benefits equally','No living thing can notice','Habitat changes can alter access to needed conditions or resources.'),
 ('Why can different plants live in different places?','Their needs and tolerances differ','All plants need identical conditions','Only their names differ','Organisms can have different suitable ranges for light, moisture, and temperature.'),
 ('What is a limitation of one simple food chain?','It leaves out other feeding relationships','It shows every possible interaction','It has to predict exact population sizes','A chain selects one pathway from a more connected food web.'),
 ('A pond loses much of its water. Which question is relevant?','How does the change affect resources and shelter?','What font is on a nearby poster?','Can we assume every species responds the same?','The effects depend on what organisms need from the habitat.')],
 'Name a habitat and two organisms. Explain a resource each needs and one connection between them.')

module('science',4,'Connect a change in motion with unbalanced forces.',
 'A force is a push or pull. Forces can change an object’s speed, direction, or shape. More than one force can act at the same time. Balanced forces mean no change in velocity; they do not necessarily mean the object is stopped.',
 'A rolling toy car slows down on a rough floor.', ['Observe the speed decreasing.','Friction and other resistive forces oppose the motion.','The combined force changes the car’s motion.'],
 'Distinguish position, speed, and acceleration','Position tells where something is. Speed tells how quickly distance is covered. Acceleration is a change in velocity, which includes direction. For a straight journey at constant speed, distance equals speed times time.',
 ['A car covers 6 metres in 3 seconds.','Its average speed is $6\\div3=2$ metres per second.','That average does not tell us whether its speed changed during the journey.'],[
 ('A stationary cart begins moving when pushed. What changed?','Its motion due to an unbalanced force','Its mass must vanish','Its name determines its speed','A net force can change velocity.'),
 ('Forces are balanced on a moving object. What can happen?','It continues at constant velocity','It must instantly stop','It must speed up','Balanced forces mean zero acceleration, not necessarily zero velocity.'),
 ('A ball changes direction while keeping the same speed. Is its velocity changing?','Yes, direction is part of velocity','No, only speed ever matters','Only if the ball changes colour','Velocity includes both speed and direction.'),
 ('Which force helps explain a sliding box slowing on a rough surface?','Friction','The written label on the box','A force guaranteed to push it forward','Friction can oppose sliding motion.'),
 ('A toy travels 8 metres in 4 seconds. What is its average speed?','2 metres per second','4 metres per second','32 metres per second','Average speed is total distance divided by elapsed time.'),
 ('What information does position give?','Where an object is relative to a reference','Always how fast it is moving','Always the force acting on it','Position and rate of motion are different quantities.')],
 'Describe an object changing speed or direction. Explain a force that could contribute, and distinguish speed from position.')

module('science',6,'Distinguish a physical change from evidence of a new substance.',
 'Matter has mass and occupies space. In a physical change, such as melting ice, the substance can remain the same while its arrangement or state changes. A chemical change forms different substances. Visible change alone does not always tell you which kind occurred.',
 'Ice melts into liquid water.', ['The state changes from solid to liquid.','The substance is still water.','Cooling can freeze the water again, showing a physical state change.'],
 'Use evidence without jumping to certainty','Bubbling, colour change, or heating can be clues, but they need context. Boiling water bubbles without forming a new substance. Gas formation during a reaction can also bubble. Compare explanations and use appropriate evidence; do not mix unknown chemicals.',
 ['Notice bubbles in a warm liquid.','Consider boiling and a gas-forming reaction as different possibilities.','Use the material and conditions to decide what further information is needed.'],[
 ('Ice turns to water. What is the clearest classification?','A physical state change','Proof of a new element','A change that removes all matter','The substance remains water while its state changes.'),
 ('Paper is cut into pieces. What changes directly?','Its size and shape','Its identity must become metal','Its total matter disappears','Cutting changes form without by itself creating a new substance.'),
 ('A metal slowly forms rust. What kind of process is involved?','A chemical change forming different substances','Only folding the metal','Only moving the metal','Rusting involves chemical reactions, not merely shape change.'),
 ('Why are bubbles alone inconclusive evidence of a reaction?','Boiling can also make bubbles','Bubbles never contain gas','All bubbles are solids','Different processes can produce the same visible clue.'),
 ('What does a liquid becoming gas demonstrate?','A change of state','Guaranteed formation of a new substance','Matter ceasing to exist','A state change can occur while chemical identity stays the same.'),
 ('How should an uncertain observation be reported?','State the change and the information still needed','State an untested cause as certain','Hide the observation','Separating evidence from interpretation helps evaluate explanations.')],
 'Compare one physical and one chemical change. Explain the evidence and one misleading clue.')

module('science',7,'Trace energy transfers without treating energy as used up.',
 'Energy can be transferred between objects and stored in different ways. A battery-powered lamp transfers energy through an electrical circuit to light and thermal energy in its surroundings. Energy is conserved, but some transfers are less useful for the intended purpose.',
 'A moving bicycle slows when its brakes are used.', ['The bicycle’s motion decreases.','Friction transfers energy into thermal stores in the brakes and surroundings.','Energy is transferred, not destroyed by the brakes.'],
 'Distinguish energy from power','Energy is an amount transferred; power is the rate of transfer. Using the same power for longer transfers more energy. For constant power, $E=Pt$. Keep units consistent: watts times seconds gives joules.',
 ['A device transfers energy at 10 watts.','In 3 seconds, $E=10\\times3=30$ joules.','Doubling the time at that power doubles the energy transferred.'],[
 ('A lamp warms its surroundings while lighting a room. What happened to some energy?','It transferred as thermal energy','It vanished','It all stayed in the battery','Not all transferred energy serves the lighting purpose.'),
 ('Which quantity describes energy transferred each second?','Power','Length','Temperature alone','Power is the rate of energy transfer.'),
 ('At constant power, what happens if operating time doubles?','Twice as much energy is transferred','Power must double','No extra energy is transferred','Energy equals power multiplied by elapsed time.'),
 ('What is the energy transferred by 5 watts over 4 seconds?','20 joules','1.25 joules','9 joules','Use $E=Pt=5\\times4=20$ joules.'),
 ('Why do bicycle brakes get warmer?','Friction transfers energy as motion decreases','The bike creates matter from nothing','Warmth proves all energy disappeared','Energy transferred from motion increases thermal energy in the system and surroundings.'),
 ('Which wording is more accurate than “energy was used up”?','Energy was transferred into less useful stores','Energy stopped existing','Energy became a length','Conservation means tracking transfers instead of disappearance.')],
 'Trace energy through an everyday device. Explain one useful transfer and one less useful transfer.')

module('science',8,'Connect cells, tissues, organs, and systems.',
 'Cells are basic units of living organisms. In many multicellular organisms, specialised cells work in tissues; tissues make up organs; organs interact in systems. The levels help explain how small structures contribute to a larger function.',
 'Muscle cells contribute to the movement of an arm.', ['Muscle cells can contract.','They work together within muscle tissue.','Muscles interact with other structures so the arm can move.'],
 'Relate structure to function without overextending a model','A cell diagram highlights parts and relationships but leaves out motion, scale, and complexity. Plant and animal cells share features, including a cell membrane; typical plant cells also have a cell wall. Not every cell looks like a textbook drawing.',
 ['Identify which feature the diagram represents.','Explain how it contributes to the cell’s function.','State a limitation, such as a flat drawing of a three-dimensional structure.'],[
 ('Which order goes from smaller organisational level to larger?','Cell, tissue, organ, system','System, cell, organ, tissue','Organ, system, tissue, cell','Specialised cells can form tissues, which contribute to organs and systems.'),
 ('What does a specialised cell’s structure help it do?','Carry out a particular function','Perform every function equally well','Stop interacting with all other cells','Specialisation relates features to particular jobs.'),
 ('Which feature is shared by typical plant and animal cells?','A cell membrane','A plant cell wall in every animal cell','An identical shape in every cell','Both have a membrane separating cell contents from their surroundings.'),
 ('What is a limitation of a flat cell diagram?','It cannot show full three-dimensional structure','It proves all cells are flat','It shows every molecule at true scale','A diagram simplifies a more complex physical structure.'),
 ('Several organs work together to move and process materials. Which level describes their interaction?','An organ system','One molecule only','A single diagram label','A system describes coordinated interactions among organs.'),
 ('Why can different cell types look different?','Their structures support different functions','Only one cell type can be living','All diagrams with different shapes are wrong','Variation in structure can reflect specialisation.')],
 'Choose one cell or organ example. Explain its function, a useful structural feature, and a limit of a diagram.')

module('science',9,'Read data with units, variation, and uncertainty.',
 'A graph connects measurements. Read axis labels, units, scale, and what each point represents before describing the pattern. A trend can exist alongside variation. A relationship between two measurements does not by itself prove that one caused the other.',
 'Ice cream sales and swimming visits both rise in warm weather.', ['Notice the association.','Temperature could influence both quantities.','Do not conclude that buying ice cream causes people to swim.'],
 'Check the strength of a conclusion','Consider how data were collected, the size and range of the sample, and whether measurements were repeated. An unusual value deserves investigation, not automatic deletion. Distinguish interpolation within measured values from extrapolation beyond them.',
 ['Read the measured range before predicting.','Check whether a trend is consistent and repeated.','Label predictions beyond that range as less secure.'],[
 ('What should you inspect before reading a graph’s height?','Axis label, units, and scale','Only its colour','Only the largest printed word','A height has meaning only in relation to the axis scale and quantity.'),
 ('Two quantities rise together. What does that alone show?','An association, not proof of causation','Certain direct causation','No possible useful information','A common cause or other factors may explain the association.'),
 ('What should you do with an unexpected measurement?','Record it and investigate possible reasons','Delete it because it differs','Replace it with the expected value','Variation or a measurement problem must be examined honestly.'),
 ('A trend was measured from 10 to 20 degrees. Predicting at 15 is what kind of use?','Interpolation within the range','Extrapolation far beyond the range','Proof at every temperature','Fifteen lies between the measured limits.'),
 ('A graph’s vertical axis starts at 95 instead of zero. What should you consider?','Small changes may look visually large','The data must all be false','The labels no longer matter','Axis choices affect visual impressions; inspect the actual values.'),
 ('Why repeat measurements?','To examine variation and reliability','To guarantee no uncertainty','To keep only the best-looking result','Repeats help reveal the spread of measured results.')],
 'Describe a graph: quantities, units, trend, variation, and one conclusion it cannot establish.')

module('science',10,'Describe reactions using particles and conservation.',
 'In a chemical reaction, atoms are rearranged into different substances. The atoms are conserved in ordinary chemical reactions. A balanced equation counts the same number of each type of atom before and after; coefficients change the number of particles, not their formulas.',
 '$2H_2+O_2\\rightarrow2H_2O$', ['Left: four hydrogen atoms and two oxygen atoms.','Right: two water molecules contain four hydrogen atoms and two oxygen atoms.','The counts match; the atoms have been rearranged.'],
 'Explain apparent mass changes using the system boundary','A system is the part you choose to study. In a closed system, matter cannot enter or leave. An open container may lose a gas, so its measured mass can decrease even while total matter is conserved. Include what crossed the boundary.',
 ['A reaction releases a gas from an open cup.','The cup and remaining contents can have less mass.','Count the escaped gas too when applying conservation of mass.'],[
 ('What happens to atoms in an ordinary chemical reaction?','They are rearranged into different substances','All atoms disappear','Every atom changes into a new element','Chemical reactions rearrange atoms rather than changing their element identities.'),
 ('Why must an equation be balanced?','To show conserved numbers of each atom type','To make every molecule look identical','To force all coefficients to be one','The representation must account for the atoms before and after.'),
 ('How many hydrogen atoms are in $2H_2O$?','4','2','6','Two molecules each contain two hydrogen atoms.'),
 ('Gas leaves an open cup during a reaction. Why may the cup’s measured mass fall?','Matter crossed the chosen boundary','Mass was destroyed everywhere','The scale must always be broken','The escaping gas is part of the total matter but no longer part of the weighed contents.'),
 ('When balancing an equation, what may be changed without changing substance identity?','Coefficients before formulas','Subscripts inside every formula','Element symbols arbitrarily','Coefficients count particles; subscripts define their composition.'),
 ('What does a closed system prevent?','Matter entering or leaving','All possible energy transfer','Every chemical reaction','Closed refers to matter exchange; energy may still transfer.')],
 'Explain the atom counts in the water equation and why an open cup can seem to lose mass.')

module('science',11,'Connect wave patterns and basic circuit quantities.',
 'A repeating wave has amplitude, period, and frequency. Amplitude measures displacement from the middle value. Period is the time for one cycle. Frequency counts cycles per second, in hertz: $f=1/T$. A larger amplitude does not automatically mean a higher frequency.',
 'A wave repeats every 0.5 seconds.', ['Period $T=0.5$ seconds.','Frequency $f=1/0.5=2$ hertz.','Doubling its height changes amplitude, not its cycle count.'],
 'Distinguish voltage, current, and resistance','Voltage is energy transferred per unit charge. Current is the rate of charge flow. Resistance relates voltage and current for the component and conditions. For an ohmic resistor at constant conditions, $V=IR$. Use simulations or teacher-approved low-voltage equipment for circuit practice.',
 ['An ideal 6-volt source is across a 3-ohm resistor.','Current $I=V/R=6/3=2$ amperes.','At the same voltage, doubling resistance halves current in this model.'],[
 ('Which wave quantity counts cycles per second?','Frequency','Amplitude','Period','Frequency is measured in hertz, or cycles per second.'),
 ('A wave’s height doubles but the cycle time stays the same. What changes?','Amplitude','Frequency must double','Period must halve','Height and repetition rate describe different features.'),
 ('A period is 0.25 seconds. What is the frequency?','4 hertz','0.25 hertz','25 hertz','Use $f=1/T=1/0.25=4$ hertz.'),
 ('What does current describe?','Rate of charge flow','Energy per unit charge','Opposition measured in ohms','Current measures how much charge passes per unit time.'),
 ('An ideal 12-volt source is across a 6-ohm resistor. What is the current?','2 amperes','72 amperes','0.5 amperes','Use $I=V/R=12/6=2$ amperes.'),
 ('At fixed voltage, resistance doubles for an ohmic resistor. What happens to current?','It halves','It doubles','It must stay unchanged','Current is inversely proportional to resistance when voltage is held fixed.')],
 'Explain amplitude versus frequency, then use voltage, current, and resistance in a worked example.')

module('science',12,'Use a model and state where it may fail.',
 'A scientific model is a representation used to explain, calculate, or predict. Models may be diagrams, equations, physical objects, or computer simulations. A model selects important features and makes assumptions. Usefulness depends on the question and the conditions.',
 'A constant-speed model predicts distance using $d=vt$.', ['Assumption: speed stays constant over the interval.','At 2 metres per second for 5 seconds, $d=10$ metres.','A stop or acceleration breaks that assumption, so the prediction needs adjustment.'],
 'Compare predictions with observations','A useful test compares the model’s prediction with independent measurements. A mismatch can reflect measurement uncertainty, wrong inputs, or a limitation of the model. Revising a model in response to evidence is part of science.',
 ['Make a prediction before inspecting the outcome.','Measure the relevant quantity and record uncertainty.','Compare, explain discrepancies, and identify a better next test.'],[
 ('What makes a model useful?','It represents relevant features for a particular question','It copies every detail perfectly','It can never be revised','Models simplify; usefulness depends on purpose and evidence.'),
 ('A constant-speed model is used for a trip with a long stop. Which assumption is violated?','Constant speed over the whole interval','That distance has units','That time can be recorded','A stop changes the motion conditions assumed by the model.'),
 ('A prediction differs from a measurement. What should you inspect?','Inputs, uncertainty, and model assumptions','Only whether the model looks attractive','How to hide the difference','Several sources of mismatch need investigation.'),
 ('Why test on new observations rather than only fitted data?','To check predictions beyond the examples used to tune the model','To guarantee every future result','To avoid recording units','Independent observations offer a stronger check of predictive usefulness.'),
 ('A globe represents Earth. Which feature is simplified?','Its scale and many surface details','The existence of any spherical form','The meaning of a model','A globe can capture broad shape while omitting fine detail.'),
 ('When evidence consistently challenges a model, what is appropriate?','Revise or limit the model and test again','Declare evidence irrelevant','Treat the first model as permanent','Models remain accountable to observations.')],
 'Choose a model. State its purpose, two assumptions, one prediction, and how you would test it.')

module('social',1,'Ask for the help you actually need.',
 'A useful help request names the task and the part that is unclear. You can ask aloud, write, point to the step, or show your work. You do not have to perform a particular facial expression to make a clear request.',
 'You understand step one but cannot locate the folder for step two.', ['Name the task: saving the file.','Name the stuck point: finding the correct folder.','Ask: “Could you show me which folder to use?”'],
 'Check that the help answered your question','After an explanation, try one step or repeat the plan in your own words. If it is still unclear, say what remains unclear and request a different example. Asking again is a way to improve accuracy.',
 ['Listen, read, or watch the explanation.','Say or write the next action you will try.','Ask a follow-up if the action still does not match the task.'],[
 ('You are unsure which form to use. Which request is specific?','Could you show me the form for this task?','Everything is impossible','You should know what I mean','The request identifies the missing information.'),
 ('Speaking is difficult right now. How else could you ask?','Write the question or point to the step','Give up all communication','Pretend you understood','A clear request can use different communication methods.'),
 ('An explanation was too fast. What can you ask?','Could we go through one step at a time?','Can you repeat it even faster?','Should I guess the missing steps?','Changing the pace can make the information easier to use.'),
 ('Which follow-up checks understanding?','So I save it in this folder first—is that right?','I will never ask again','Every possible folder is the same','Restating the next action allows correction before proceeding.'),
 ('You know most of a task but one part is unclear. What is useful to show?','The part you tried and the exact stuck point','Only an unrelated finished task','Nothing about the task','The helper can respond more usefully to specific context.'),
 ('The first example did not help. What is a constructive next request?','Could you show a different example?','Can we assume I understand now?','Should the unclear step be skipped automatically?','A different representation may address the point that remains unclear.')],
 'Write or draw a help request for one specific task. Add a follow-up that checks your understanding.')

module('social',2,'Agree on a clear turn-taking plan.',
 'Shared tasks work more smoothly when people know whose turn it is and how turns change. Agree on a visible order, a task boundary, or a time limit that works for the group. People may use different ways to signal that they want a turn.',
 'Two people share one tablet for a practice activity.', ['Agree that each person completes one round.','Use a written order or visible marker.','Save work and switch accounts before handing the tablet over.'],
 'Repair a mix-up directly','If turns get confused, describe the sequence you understood and ask to reset the agreement. A clear system helps more than expecting people to read each other’s minds. Review the plan if it repeatedly excludes someone.',
 ['State what you noticed without labelling the person.','Check the agreed order.','Choose a clear next turn and make the order visible.'],[
 ('Two learners share a tablet. Which plan is clear?','Each completes one round, then saves and switches accounts','Whoever grabs it keeps it','No one mentions turns','An agreed boundary makes turn changes predictable.'),
 ('Someone needs a little longer to finish a step. What can the group do?','Discuss a workable adjustment to the turn plan','Assume they are cheating','Cancel their turn without discussion','A clear plan can be adjusted when needs or task lengths differ.'),
 ('You think your turn was skipped. Which message checks the sequence?','I thought I was next after Jo. Can we check the order?','You always ruin everything','I will hide the equipment','The request describes the issue and asks for clarification.'),
 ('What helps a group remember whose turn follows?','A visible order or marker','An unspoken expectation','Changing the order without telling anyone','External cues reduce the need to guess or remember an invisible agreement.'),
 ('Before passing a shared device, what protects private work?','Save and switch out of the current account','Leave every private report open','Share a private sign-in code with everyone','Account separation keeps one learner’s information from the next.'),
 ('A turn rule repeatedly leaves one person out. What should happen?','Review the rule with the group','Keep it because it was the first rule','Assume the excluded person does not matter','A useful agreement should allow participation and be open to revision.')],
 'Create a turn-taking plan for a shared device or tool. Include how to save and how to handle a delay.')

module('social',4,'Describe a problem with enough detail to get help.',
 'A clear problem report states what you were trying to do, what you observed, what you expected, and what you have already checked. Keep observations separate from blame or guessed causes. Do not include private information that is unnecessary for solving the problem.',
 'A document does not print.', ['Goal: print the named document.','Observation: it remains in the queue and no page appears.','Request: ask the responsible person to help check the printer status.'],
 'Agree on the next step','After reporting, clarify who will act and when to check back. If the issue involves an immediate hazard, use the site’s safety procedure and responsible contact. Do not experiment with unfamiliar equipment simply to appear independent.',
 ['State what you can do safely now.','Confirm who is responsible for the next action.','Record the agreed update or check-back time.'],[
 ('Which report gives useful information?','I selected Print, but the file is still queued and no page appeared','It is bad','Someone definitely broke everything','The first report describes the action and observable result.'),
 ('A cause has not been checked. How should you describe it?','As a possibility, not a confirmed fact','As certain because it sounds likely','As the only possible explanation','Separating a hypothesis from an observation supports accurate troubleshooting.'),
 ('What helps someone avoid repeating your checks?','A brief list of what you already tried','Hiding all previous actions','Listing unrelated tasks','Relevant previous checks give the helper a useful starting point.'),
 ('What should a problem report request?','A specific check, help, or next action','Only someone to blame','A guarantee before any information is shared','The request helps move from description to a practical response.'),
 ('An unfamiliar machine looks unsafe. What is appropriate?','Follow the site procedure and notify the responsible person','Open it without training','Keep using it to avoid asking','Use the established safety process rather than guessing.'),
 ('Help has been requested. Which detail supports follow-through?','Who will act and when an update is expected','Only the colour of the room','An unrelated opinion','Responsibilities and timing make the next step clear.')],
 'Write a problem report: goal, observation, expectation, checks tried, and requested next step.')

module('social',5,'Make teamwork explicit and manageable.',
 'A shared goal needs a shared plan. Break the work into tasks, agree on roles, and make handoffs clear. A role can change after discussion. Clear teamwork does not require everyone to communicate or work in exactly the same way.',
 'A group prepares a small display.', ['List tasks: gather items, arrange them, check labels.','Agree who handles each task and how to ask for help.','Set a check-in before the display is needed.'],
 'Use check-ins to adjust the plan','A check-in is a short update about completed work, obstacles, and next steps. It is an opportunity to change the plan before a deadline is missed. Avoid treating a request for support as proof that someone is not contributing.',
 ['Say what is finished.','Name any blocked task and the help needed.','Agree on a revised next step and responsibility.'],[
 ('Which team plan makes responsibility clear?','Jo gathers items; Lee checks labels; both review at 3','Everyone does something sometime','The loudest person decides silently','Named roles and a check-in time reduce ambiguity.'),
 ('A task depends on another task finishing first. What should be agreed?','The handoff and how completion is signalled','That dependencies do not matter','That both people must guess','A clear handoff connects the tasks in the right order.'),
 ('A teammate prefers written instructions. What supports the shared work?','Provide a usable written task list','Insist all instructions be spoken quickly','Remove their role without discussion','Different communication formats can support the same shared goal.'),
 ('Which update is useful at a check-in?','Labels are done; two names need confirmation','Everything, maybe','A long unrelated story with no task information','Completed work and a specific obstacle support a decision.'),
 ('A person is blocked by missing materials. What should the group consider?','Getting the materials or adjusting tasks','Assuming the person did not try','Waiting silently until the deadline','An obstacle may require a resource or plan change.'),
 ('Why review the final work together?','To check the shared goal and catch missed details','To make every person’s style identical','To find someone to blame first','A joint review compares the result with the agreed purpose.')],
 'Plan a three-person task: goal, roles, a handoff, and a short check-in question.')

module('social',7,'Turn a work task into a realistic plan.',
 'Planning starts with the outcome and deadline. Break the task into actions, identify dependencies, and estimate time with some room for uncertainty. If several requests conflict, ask about priorities before promising everything.',
 'Prepare ten information packs before 2 pm.', ['Check the required contents and materials.','Arrange the steps: print, assemble, then check.','Allow time for missing pages or a printing delay.'],
 'Update a plan when conditions change','A plan is a tool, not a prediction guaranteed to come true. When a delay appears, report the effect early, offer realistic options, and confirm the revised priority. Use an external checklist if holding all steps in memory is difficult.',
 ['Identify which step is delayed.','Estimate the effect on the finish time.','Ask whether to change scope, get help, or move the deadline.'],[
 ('What should you clarify before planning an unfamiliar task?','The expected result and deadline','Only the project nickname','Nothing until it is finished','Outcome and timing determine the plan’s requirements.'),
 ('Assembly needs printed pages first. Which order respects the dependency?','Print, then assemble','Assemble before pages exist','Only count finished packs','A dependent step needs its inputs ready.'),
 ('Two urgent requests conflict. What is useful?','Ask which priority should come first','Promise both without checking time','Choose silently and tell no one','Clarifying priority helps match limited time to expectations.'),
 ('A printer delay will affect the deadline. When should you report it?','When the effect becomes clear, with options','Only after everyone has left','Never if it feels uncomfortable','Early information allows the plan to be adjusted.'),
 ('Why leave some buffer in a time estimate?','Tasks and interruptions can vary','Time estimates should be deliberately meaningless','Every task takes exactly the same time','A buffer acknowledges uncertainty rather than guaranteeing a perfect schedule.'),
 ('What helps track a task with several steps?','A visible checklist with completed steps marked','Relying on guessing each time','Rewriting the entire goal after every action','An external list makes the current and next steps visible.')],
 'Plan a practical task with three steps, a dependency, a time estimate, and a backup option.')

module('social',8,'Clarify a disagreement before trying to solve it.',
 'A disagreement may concern facts, priorities, preferences, or an unclear agreement. Start by describing the specific issue. Ask what the other person means and check your understanding. You can set boundaries and request a pause while still working towards clarity.',
 'Two people thought they had the same turn on a shared tool.', ['State your understanding of the order.','Ask what order the other person understood.','Check the written plan or agree a new visible order.'],
 'Look for a next step, not a personality verdict','Focus on the action or agreement that can change. Offer options and check whether they address the concern. If the issue cannot be resolved or the situation feels unsafe, involve an appropriate trusted person or workplace contact.',
 ['Name the practical concern.','Suggest two workable options.','Confirm the agreement, or ask an appropriate person to help mediate.'],[
 ('Two people remember different deadlines. What should they check first?','The written instruction or source of the deadline','Which person is louder','Who has more unrelated hobbies','A factual difference may be resolved through the original information.'),
 ('Which statement focuses on a specific issue?','I expected the tool after your first round; can we check the plan?','You are always selfish','You never care about anything','The first statement makes the disagreement concrete without a broad personal label.'),
 ('You need time to process the discussion. What can you say?','I need a short pause; can we continue at an agreed time?','I must answer instantly','A pause means I can never return','A clearly communicated pause can support a more useful discussion.'),
 ('Which question checks understanding?','Are you saying the deadline matters more than the format?','Why are you wrong?','Can I ignore what you just said?','Restating a point lets the other person clarify or correct it.'),
 ('A practical disagreement remains unresolved. What is an option?','Ask an appropriate trusted person to help clarify it','Escalate threats','Assume one person’s needs do not count','A suitable third person can help with a stuck agreement or process.'),
 ('Two options both meet the shared goal. What can help choose?','Compare constraints and agree a workable option','Treat every preference as a factual error','Choose an option nobody understands','Constraints and preferences can be discussed without declaring a person wrong.')],
 'Write a disagreement example with your understanding, a clarifying question, and two possible next steps.')

module('social',9,'Send a work message that makes the next action clear.',
 'Useful work messages state the purpose early, include the necessary details, and say whether a reply or action is needed. Match the channel to the task’s urgency and the workplace’s normal process. Keep private information limited to what the recipient needs.',
 'A delivery is delayed and the team needs a new time.', ['State the update: delivery is delayed.','Give the confirmed new time, or say it is not yet confirmed.','Name the next action and who will send another update.'],
 'Confirm changes and close the loop','When a message changes a plan, check that the affected people received and understood it. A sent message is not proof that it was read. Use the agreed escalation process when an urgent issue needs a timely response.',
 ['Send the change using the agreed channel.','Ask for confirmation when it affects immediate work.','Follow up appropriately if the required response does not arrive.'],[
 ('Which update is most useful?','The delivery is now expected at 3; please keep the receiving area available','Things changed','There may be stuff later','The update identifies the change, timing, and requested action.'),
 ('A new time is not confirmed. How should it be described?','As unconfirmed, with a plan for the next update','As guaranteed','As secret from the affected people','Clear uncertainty prevents others treating an estimate as a promise.'),
 ('What does sending a message establish?','That it was sent, not necessarily read or understood','That everyone agrees','That no follow-up can ever be needed','Delivery, reading, understanding, and agreement are separate steps.'),
 ('A message contains private details unrelated to the task. What should you do?','Remove details the recipient does not need','Send it to the widest group','Add more personal background automatically','Share information proportionate to the purpose and appropriate recipient.'),
 ('A work plan changes at short notice. What helps close the loop?','Ask affected people to confirm the change','Assume silence is always agreement','Use an unrelated channel nobody checks','Confirmation can catch missed or misunderstood updates.'),
 ('Which subject line helps a reader act?','Action needed: confirm Friday’s start time','Hello stuff','Everything important ever','A specific purpose and topic help prioritise the message.')],
 'Draft a work update with purpose, facts, any uncertainty, and a clear next action.')

module('social',11,'Give and use feedback about a specific action.',
 'Helpful feedback describes a particular action and its effect. It can recognise what worked and identify a change. Avoid vague praise or criticism that gives no useful next step. A person can receive feedback through speech, writing, or a demonstration.',
 'A teammate’s labels are clear, but one date is missing.', ['Recognise the useful feature: the labels are easy to read.','Identify the specific issue: one label lacks a date.','Ask for the date to be added and checked.'],
 'Turn feedback into a next attempt','When receiving feedback, check the example and ask what a successful revision would look like. You can question inaccurate feedback respectfully. Understanding feedback does not require agreeing with every judgement.',
 ['Ask which part needs changing.','Compare the feedback with the task’s requirements.','Make a relevant revision or explain the evidence for a different view.'],[
 ('Which feedback is actionable?','The title is clear; add the missing date beside it','It is bad','You are hopeless at this','A specific observation and next step support revision.'),
 ('Feedback says “be better”. What can you ask?','Which part should change, and what would a good example look like?','Should I guess every possible meaning?','Does that prove I cannot learn?','Clarifying the target turns a vague judgement into usable information.'),
 ('You think a correction is based on the wrong version. What helps?','Show the current version and check the requirement together','Accept a false detail without checking','Insult the reviewer','Evidence and clarification can resolve an inaccurate judgement.'),
 ('Why name something that worked?','So the learner knows what to keep doing','To avoid ever mentioning changes','To guarantee every part was perfect','Specific positive feedback identifies a repeatable action.'),
 ('A person finds spoken feedback hard to retain. What is an option?','Provide a brief written version or example','Speak faster','Refuse any other format','A suitable format makes the feedback easier to use.'),
 ('What is a useful response after a revision?','Check whether the changed work now meets the requirement','Assume any change is automatically correct','Start a new unrelated argument','Feedback is completed by checking its effect on the task.')],
 'Write feedback on an imaginary task: one specific strength, one change, and how to check the revision.')

module('social',12,'Solve a workplace problem using evidence and follow-through.',
 'A practical problem-solving cycle is define, gather, compare, act, and review. Clarify who is affected and what a satisfactory result would be. Work within your role, training, and authority. Some issues need an appropriate supervisor or specialist rather than solo improvisation.',
 'Items are repeatedly returned to the wrong shelf.', ['Define the problem with examples, rather than blaming a person.','Consider causes: unclear labels, inconsistent locations, or missing instructions.','Try a labelled shelf plan, then check whether misplaced items decrease.'],
 'Choose and evaluate an option','Compare options using relevant criteria such as time, accessibility, cost, and safety. Agree who will act and how the result will be measured. If the first attempt fails, use what you learned to revise the plan.',
 ['List two practical options and their constraints.','Choose a small, reversible trial when appropriate.','Review the outcome against the original problem, then keep or adapt the change.'],[
 ('What should come before choosing a solution?','Define the problem and gather relevant examples','Pick the most dramatic action','Decide who to blame','A clear problem statement helps ensure the solution addresses the actual issue.'),
 ('Which observation helps investigate missing stock labels?','Which labels are missing and when the issue is noticed','An unrelated opinion about the team','Only the nicest-looking shelf','Specific evidence can reveal a pattern or point of failure.'),
 ('A solution requires work outside your training. What should you do?','Involve the appropriate qualified or responsible person','Proceed secretly to prove independence','Assume instructions are unnecessary','Role and training limits determine who can appropriately carry out a task.'),
 ('Two possible solutions exist. How can you compare them?','Use criteria connected to the goal and constraints','Choose only the longer description','Ignore who needs to use them','Relevant criteria make the choice explainable and reviewable.'),
 ('What should an action plan name?','Who acts, by when, and how the result will be checked','Only the problem’s nickname','A promise with no responsibility','Clear ownership, timing, and evaluation support follow-through.'),
 ('A trial did not reduce the problem. What next?','Review the evidence and revise the approach','Declare the problem solved anyway','Keep repeating without checking why','Results should guide whether a solution is kept, changed, or replaced.')],
 'Describe a problem, two options, the chosen action, who should act, and a measurable review.')

def populate(units,bank):
    for spec in SPECS:
        sid=f"{spec['subject']}-{spec['grade']}"
        unit=next(u for u in units if u['id']==sid)
        if unit['ready']: raise ValueError('Refusing to overwrite an existing authored module: '+sid)
        questions=[]
        # Each scenario checks both a decision and the reason behind it. Options
        # are shuffled by the learner UI and server when selecting a checkpoint.
        for i,(prompt,answer,wrong1,wrong2,why) in enumerate(spec['cases']):
            for j in range(2):
                qprompt=prompt if j==0 else f'Explain your reasoning: {prompt}'
                options=[answer,wrong1,wrong2] if j==0 else [why,f'The wording alone guarantees that “{wrong1}” is correct.',f'The information given requires “{wrong2}”, with no need to check.']
                questions.append(dict(id=f'{sid}-case-{i}-{j}',caseId=f'{sid}-case-{i}',lesson=1 if i<3 else 2,kind='choice',prompt=qprompt,options=[dict(id=str(k),text=v) for k,v in enumerate(options)],answer='0',skill='apply' if j==0 else 'reason',hint='Read the situation again. Compare the details with the method from the lesson.',explanation=why))
        unit.update(ready=True,minutes=15,goal=spec['goal'],why=spec['goal'],visual='workshop',
          lessons=[dict(title=spec['goal'],body=spec['body'],example=spec['example'],steps=spec['steps']),dict(title=spec['second'],body=spec['body2'],example='Work through the reasoning',steps=spec['steps2'])],
          review=[spec['body'],spec['body2']],reflection=spec['reflection'],practice=questions)
        # Published practice never doubles as the check once held-out cases are written.
        bank[sid]=check_questions(sid,CHECKS[sid]) if sid in CHECKS else questions
    assert len(SPECS)==37,len(SPECS)
    assert set(CHECKS)<={f"{s['subject']}-{s['grade']}" for s in SPECS} and all(len(c)==6 for c in CHECKS.values())

def check_questions(sid,cases):
    """Server-only checks. The reason version states the answer and asks which reason explains it."""
    questions=[]
    for i,(prompt,answer,wrong1,wrong2,why,wrong_why1,wrong_why2) in enumerate(cases):
        for j,(text,options) in enumerate(((prompt,[answer,wrong1,wrong2]),(f'{prompt} The answer is “{answer}”. Which reason explains it?',[why,wrong_why1,wrong_why2]))):
            questions.append(dict(id=f'{sid}-check-{i}-{j}',caseId=f'{sid}-check-{i}',lesson=1 if i<3 else 2,kind='choice',prompt=text,options=[dict(id=str(k),text=v) for k,v in enumerate(options)],answer='0',skill='apply' if j==0 else 'reason',hint='Read the situation again. Compare the details with the method from the lesson.',explanation=why))
    return questions
