"""Original explanations and transfer tasks for the existing foundation modules.

These enrich the same two lessons and saved working area, without adding another
path or treating a short module as a complete school course.
"""

DEPTH = {
'math-1': (
 'The $+$ sign means add more. The $=$ sign means the amounts match. The 5 cartons and the 3 cartons together are the same amount as 8 cartons.',
 'Subtract means take away. Here, $6-2=4$ starts with 6 cartons, takes out 2, and leaves 4. Count the cartons left to check.',
 'Start counting AFTER 5: 6, 7, 8. Do not count the fifth carton twice.', 'Check by adding back what you took out: $4+2=6$. You get the number you started with.'),
'math-2': (
 'A digit gets its value from its position. In 34, the 3 represents three groups of ten, not three loose objects. The 4 represents four ones. A ten can be exchanged for ten ones without changing the total. Draw bundles and loose items to see why 34 can also be described as two tens and fourteen ones.',
 'Regrouping is an exchange, not a trick that creates or removes value. To subtract 8 from 34, trade one ten for ten ones. Now fourteen ones can lose eight ones, leaving six ones alongside the two tens. This is why the written borrowing method works. Check that the amounts before and after the exchange are equal.',
 'The number of bundles is different from the number of objects inside them.', 'Writing a zero holds a place; removing it can change every digit’s value.'),
'math-3': (
 'Multiplication records equal groups. Four packs containing three items each can be counted as 3 plus 3 plus 3 plus 3. An array shows four rows of three, so you can check the total without guessing. The first number describes how many groups there are; the second describes the size of each group.',
 'Division can ask either how many groups fit or how large each group will be. Twelve items packed three to a bag make four bags. Twelve items shared between four bags put three in each bag. Use the question’s units to distinguish these stories. If groups are unequal, count them separately before deciding whether multiplication fits.',
 'Four groups of three is not four plus three.', 'A remainder still has meaning: it may need another container rather than being discarded.'),
'math-4': (
 'A fraction compares a selected amount with one defined whole. The denominator names how many equal parts make that whole; the numerator counts the selected parts. Three of eight equal sections is three eighths. Three differently sized sections cannot be called three eighths just because there happen to be eight pieces.',
 'Equivalent fractions describe the same amount after changing the size of the parts. Cutting every half into two equal pieces gives fourths: one half becomes two fourths. The numerator and denominator both double because each old piece becomes two new pieces. Before comparing fractions, check that the wholes themselves have the same size.',
 'A bigger denominator makes each part smaller when the whole stays the same.', 'Half of a small item and half of a large item are not equal amounts.'),
'math-5': (
 'Decimal places are units too. In 3.45 dollars, 3 means whole dollars, 4 means tenths of a dollar, and 5 means hundredths. Money is often easier to calculate as whole cents: 3.45 dollars is 345 cents. Keeping the unit visible prevents adding 25 cents as if it were 25 dollars.',
 'When adding or subtracting decimals, align equal place values. Writing 5.00 instead of 5 does not change the amount; it shows the hundredths clearly. Estimate first, calculate, then compare with the estimate. A result near 300 dollars for a purchase of a few dollars is a clue that a decimal or unit moved.',
 '3.5 and 3.50 represent the same value; 3.05 is different.', 'Do not round intermediate money calculations unless the problem tells you to.'),
'math-6': (
 'A ratio links two quantities. A mix with one scoop of concentrate for three scoops of water uses four scoops in total. Doubling both parts preserves the mix. Adding one scoop to both parts does not: two to four is a different relationship from one to three. Keep labels on the two quantities so you do not reverse them.',
 'A unit rate sets one quantity to one. Dividing a total price by the number of identical units tells you the price per unit. This makes different pack sizes comparable. The comparison is fair only when the units and useful quantity match. Price per 100 grams cannot be compared directly with price per kilogram.',
 'A one-to-three ratio is not one third of the complete mixture; it is one quarter.', 'Scaling a ratio multiplies both quantities by the same factor.'),
'math-7': (
 'Percent means per hundred. A percentage is a share of a particular whole, so identify that whole before calculating. Twenty percent of 50 is 10 because twenty hundredths times 50 equals 10. Ten percent can be found by dividing by ten; five percent is half of that. These shortcuts work because the fractions are equivalent.',
 'A discount is the amount removed, not the final price. Find the discount, then subtract it from the original. For a percentage increase, add the increase instead. Successive percentages use successive wholes: a 20 percent increase followed by a 20 percent decrease does not return to the original amount.',
 'The same percentage of two different totals can give different amounts.', 'Twenty percent off is not the same as twenty dollars off.'),
'math-8': (
 'An equation says two expressions have the same value. Think of each side as an entire quantity on a balance. To keep that equality, perform the same operation on both sides. In three groups of x plus 2 equals 14, first remove the added 2 from both sides, then divide the remaining 12 into three equal groups.',
 'Build an equation by naming the unknown and its unit. Separate a one-time amount from an amount that repeats. A starting charge plus a cost for each item becomes starting charge plus rate times quantity. After solving, substitute the answer into the original story. A sensible unit and a matching total are both part of the answer.',
 'The equals sign is a relationship, not an instruction to write the next number.', 'Moving a term changes its sign only because you applied an operation to both sides.'),
'math-9': (
 'A straight-line model has a constant rate of change. The starting value is the output when the input is zero; the slope is the output change for one unit of input. In a cost model, these might be a booking fee and a cost per hour. Label both axes so the graph describes a relationship rather than just a shape.',
 'To calculate slope, divide the change in output by the change in input. Use the same direction for both differences. A line can have a positive starting value and a negative slope, such as water draining from a full tank. A line is a model with limits: a tank cannot keep draining below zero water.',
 'The height of one point is not its slope.', 'A straight line need not pass through zero; a starting amount shifts the whole line.'),
'math-10': (
 'Area counts unit squares that cover a surface. A square with side 3 contains three rows of three squares. Increasing the side changes both the number of rows and the number in each row. Doubling the side therefore multiplies area by four. The perimeter follows a different rule because it counts lengths around the edge.',
 'A square root reverses squaring for a nonnegative amount. If an area is 36 square units, its square side is 6 units. In an algebra equation, both positive and negative 6 square to 36; in a side-length story, only the nonnegative answer fits. Carry the units through the calculation to distinguish length from area.',
 'Doubling a side doubles perimeter but quadruples area.', 'A square root does not mean divide the number by two.'),
'math-11': (
 'The right-angle condition matters. The Pythagorean relationship connects the areas of squares built on the three sides of a right triangle. Identify the hypotenuse before substituting numbers: it is opposite the right angle and is the longest side. If you are finding a leg, subtract the other leg’s square from the hypotenuse’s square.',
 'Trigonometric ratios compare sides relative to a chosen angle. When a right triangle is scaled, its side lengths change together but these ratios remain fixed. This lets you relate an angle to a slope or height without building every possible triangle. A ratio is a number; finding the corresponding angle is a separate inverse-trig step.',
 'Do not use the right-triangle formula on an arbitrary triangle.', 'Opposite and adjacent change with the chosen angle; the hypotenuse does not.'),
'math-12': (
 'Average rate compares two outputs over an interval. For position against time, it measures position change per time change: average velocity. A curved graph can have a different rate at different points, so one long interval can hide changes inside it. Draw the secant line through the two points and compare its slope with the curve nearby.',
 'To estimate a local rate, keep one input fixed and bring the second input closer. For a square function, expanding the squared expression lets a factor of the interval cancel before taking a limit. The limit describes what the rate approaches; it does not require dividing by zero. The answer has output units per input unit.',
 'Position, average speed, and instantaneous speed answer different questions.', 'Substituting a zero interval into the original fraction gives an undefined expression, not the derivative.'),
'math-cash': (
 'Count value rather than objects. Two coins can be worth less than one coin if their denominations differ. Sort by denomination, multiply each value by its count, and add the subtotals. Convert everything to cents if that makes the arithmetic clearer. For example, two dollars and three quarters become 200 plus 75 cents.',
 'Change can be found by subtraction or by counting up from the price to the amount paid. From 2.75 to 3.00 is 0.25, then to 10.00 is 7.00: together that is 7.25. Check by adding price and change. These examples omit taxes and cash-rounding rules so the relationship stays visible.',
 'A coin’s size is not a reliable guide to its value.', 'If the payment is smaller than the price, the customer still owes money; it is not positive change.'),
'math-prices': (
 'A lower package price is not always a lower unit price. Divide each total by its quantity, then compare the resulting prices for one matching unit. Three items for 6 dollars cost 2 dollars each. Five for 9 dollars cost 1.80 each. Write the comparison in a small table to keep totals and rates separate.',
 'The lowest unit price is useful information, not an automatic buying instruction. Consider how much you need, whether you can store it, and whether it fits your available budget. A larger pack can be cheaper per item but still cost more today. An unused or spoiled item does not provide the value its label suggests.',
 'Use equal units: convert kilograms to grams or compare both per kilogram.', 'Do not divide quantity by price if the question asks for dollars per item.'),
'math-budget': (
 'A budget gives each part of a finite amount a job. Start with money actually available, subtract essential commitments, then decide what can be saved or spent optionally. Writing categories prevents counting the same money twice. A negative balance is a signal to change the plan, not a number to hide or turn positive.',
 'Plans need room for uncertainty. If an expense increases, calculate the difference and decide which optional amount can change. Keep a distinction between expected money and received money. A useful budget can be updated after every new fact; it does not need to predict every future expense perfectly.',
 'Available money is different from money you hope will arrive.', 'A discount still costs money when you buy something that was not in the plan.'),
'math-pay': (
 'Hours are measured in units of sixty minutes. Thirty minutes is half an hour, not 0.30 hours. Calculate elapsed time, subtract any unpaid break, then multiply paid hours by the hourly rate. Label the rate as dollars per hour so the hours cancel conceptually and leave a money amount.',
 'Gross pay is the amount before deductions. A pay deposit may differ, so a practice gross-pay calculation is not a promise about take-home pay. For changing shifts, calculate each paid duration first and add the hours. Check a result by estimating: about four hours at about fifteen dollars is around sixty dollars.',
 'An end time is not a duration; subtract the start time.', 'Do not assume breaks, overtime, tax, or payroll rules that the question has not supplied.'),
'reading-1': (
 'Each detail has a job. The place tells you where to go. The time tells you when. “Bring” tells you what to take. Find the words in this message; another message may have a different plan.',
 'A new message can change one part of a plan. Check what changes and what stays the same. If a detail is missing, you cannot find it by guessing. Ask one clear question to get it.',
 'Check this message each time. Do not use an answer from the last one.', '“Tomorrow” gives a day. It does not give a time.'),
'reading-2': (
 'Find the main action, then ask who performs it and what receives it. Swapping two names can reverse a sentence even when every word remains familiar. Describing words narrow the meaning of a noun: the blue bag may be different from the red bag. Track those details when deciding which person or object the writer means.',
 'Pronouns save repetition, but they need a clear reference. Read the sentence before a word such as they, it, or this. Check which noun fits the grammar and the situation. Sometimes more than one reference fits. Recognizing that ambiguity is stronger reading than choosing a person without enough evidence.',
 'The first noun is not always the person doing the action.', 'A pronoun does not reliably mean the closest name if the context supports more than one reading.'),
'reading-3': (
 'Instructions encode an order, even when the sentences are not written in that order. “Before carrying it, close the lid” puts closing first. Write the actions separately and connect them with arrows. Check prerequisites: a step may depend on having materials ready or completing a safety check before the next action starts.',
 'Conditions split a plan into branches. An if instruction applies only when its condition is true. Unless usually identifies the exception. Try two concrete cases: one where the condition holds and one where it does not. This turns an abstract sentence into a plan you can actually follow and reveals when the instructions leave something unspecified.',
 'The first action mentioned is not necessarily the first action to perform.', 'A conditional instruction does not say that its condition always occurs.'),
'reading-4': (
 'The main point connects the important details. A good summary is broad enough to cover them but narrow enough to stay within the text. If a passage explains saving for a bicycle, “money” is too broad and one coin amount is too narrow. Ask what the writer wants you to understand after reading the whole passage.',
 'Separate the main idea from supporting examples. Keep cause-and-effect links when they explain why events happened. To test a summary, compare each part with the source: is anything important missing, and has anything been added? Summarizing is a selection task, not simply copying the first sentence or making the passage shorter at random.',
 'The most memorable detail may not be the main point.', 'A summary must not turn one event into a claim about what always happens.'),
'reading-5': (
 'Context provides clues to meaning, but clues have different strengths. A definition in the text is stronger than a vague association. Substitute your proposed meaning into the sentence and reread the surrounding sentences. If the resulting story no longer fits, try another meaning. This works for familiar words used in an unfamiliar way as well as new words.',
 'Figurative phrases do not always mean exactly what their separate words suggest. Check whether a literal reading fits the situation. If not, explain the phrase in plain language or ask the speaker to do so. Ambiguous wording is a feature of the message, not a reason to blame yourself for needing clarification.',
 'A word’s first dictionary meaning may not fit this use.', 'One surrounding clue can suggest a meaning without proving every detail about the situation.'),
'reading-6': (
 'Evidence has to support the exact claim being made. Start with the question, state an answer, choose a relevant detail, then explain the connection. A detail can be accurate but irrelevant. The colour of a bus may be in the passage, but it does not explain why the passenger arrived late unless the text makes that connection.',
 'Match the strength of your wording to the strength of the evidence. One observed event can support a claim about that event. Claims about everyone, never, or always require much wider support. Look for a detail that challenges your first answer as well as one that supports it. A revised answer can be more accurate than a confident first guess.',
 'Copying a quote is not the same as explaining why it matters.', 'A detail that supports part of a claim may not support the entire claim.'),
'reading-7': (
 'An inference combines an observation with background knowledge. Keep the observation separate from your explanation so you can test the explanation. A wet floor is observable; a leaking pipe is one possible cause. List another possible cause and ask what extra detail would distinguish them. This keeps inference useful without turning it into certainty.',
 'When new information arrives, return to the original clues and update the explanation. Words such as suggests and may communicate that uncertainty honestly. This matters especially when reading people’s actions: a delayed reply can have several explanations. You can describe the delay and ask a question without inventing someone’s intention.',
 'A plausible explanation is not automatically the only explanation.', 'Do not treat silence, expression, or eye contact as proof of another person’s thoughts.'),
'reading-8': (
 'Break a claim into something checkable: who did what, when, and according to which source? Follow a citation to the original information when possible. Check the date of the event as well as the publication date. An accurate old report can be misleading when presented as a current event without that context.',
 'A small sample can provide a clue, but who was included matters. Asking ten friends about a game measures those friends’ responses, not everyone’s opinion. Distinguish popularity, confidence, and evidence. A responsible conclusion describes what the information supports and what you would still need to check before using it for an important decision.',
 'A large follower count or professional appearance does not establish accuracy.', 'A source can be reliable on one topic and outside its expertise on another.'),
'reading-9': (
 'Compare accounts using a shared frame: the same event, time, place, and definition. Two descriptions can differ because they cover different parts of a situation. Put their actual claims side by side before deciding whether they conflict. This is particularly useful for schedules, reviews, and reports that use different counting units.',
 'When two claims really are incompatible, preserve the disagreement and seek relevant evidence. Do not choose the more confident writer automatically or average two different times into a new invented time. State what both accounts agree on, what they disagree on, and which record or observation could help settle the difference.',
 'A difference is not by itself proof that someone lied.', 'Twenty visits and twenty visitors are different measures when a person may visit more than once.'),
'reading-10': (
 'An argument has a claim, reasons, and an implied link between them. Ask whether accepting the evidence would make the conclusion more reasonable. Then identify what else would need to be true. More visitors during a trial might support longer opening hours, but the argument may still need information about costs and whether the pattern continued.',
 'A counterargument targets a relevant weakness, not the person making the argument. Consider whether an objection changes your conclusion or simply limits it. A narrower proposal can be better supported: a longer trial may fit uncertain evidence better than a permanent change. Explain why you accept one option while acknowledging its tradeoffs.',
 'Strong emotion can show importance without proving a factual claim.', 'Repeating the conclusion in different words does not supply evidence.'),
'reading-11': (
 'Research starts with a question specific enough to investigate. Use search terms that name the topic and the fact you need. Record where each useful claim came from while reading, including title, author or organization, and date when available. This prevents a later list of links from becoming disconnected from the claims they are meant to support.',
 'Compare sources that bring independent information. Several pages repeating the same original claim are not several independent confirmations. Separate quotation from paraphrase, and preserve the original meaning when paraphrasing. A reference helps another reader trace your work; it does not make a weak or irrelevant source strong.',
 'A search-result snippet can leave out the condition that changes a claim.', 'Do not cite a source you have not actually checked as if you read it.'),
'reading-12': (
 'A viewpoint is shaped by what a person knows, experiences, and values. Identify the actual claim and reasons before agreeing or disagreeing. A reader can understand a viewpoint accurately without accepting every part of it. Look for the strongest fair version of each position rather than selecting a weak sentence that is easy to dismiss.',
 'Compare perspectives using the same question. Identify shared goals, disputed facts, and different priorities separately. Evidence can resolve some factual disputes; a value tradeoff may still require a decision. State where the evidence leads you and what remains uncertain. Fair comparison does not require treating all claims as equally well supported.',
 'Describing a position fairly is not the same as endorsing it.', 'Two sides of a disagreement need not have equal amounts or quality of evidence.'),
'writing-1': (
 'Write for a person who cannot see what is in your head. Name the action or information they need, then add the specific detail that makes it usable. A short message can be complete. “I’ll meet you at the west entrance at 3 pm” gives a clearer plan than “I’ll be there later,” even though both are brief.',
 'Read the message as its receiver. Could they tell what to do next, where to go, or whether a reply is needed? Replace vague words with concrete information. Check names, times, and amounts before polishing style. Spelling can be revised, but perfect spelling cannot rescue a message that leaves out its purpose.',
 'Longer is not automatically clearer.', 'A reader may not know what “there”, “that”, or “later” refers to.'),
'writing-2': (
 'A complete sentence usually connects a subject with a complete thought. Start with who or what, then add what happens or what is true. Extra description can help, but it should not hide that central connection. Reading the sentence aloud can reveal where you have joined two separate thoughts without a clear boundary.',
 'Punctuation helps readers group meaning. A full stop can separate two complete thoughts; a joining word can explain how they relate. Choose because for a reason, but for a contrast, or and for an addition. Check that a pronoun still has a clear reference after you combine sentences.',
 'A string of descriptive words may still be missing the main action.', 'Adding commas everywhere does not reliably fix a run-on sentence.'),
'writing-3': (
 'Start by doing the task mentally, one action at a time. List materials or prerequisites before the step that needs them. Put actions in the order the reader must perform them, not the order you happened to remember them. Use clear action verbs such as label, compare, save, or check.',
 'Test instructions with a reader who has not done the task. Ask them to tell you their next action after each step. If they must guess, add the missing detail or split a long step. Include how to recognize completion and what to do if a condition changes. A numbered list is useful when order matters.',
 'Do not hide two dependent actions inside a vague word such as prepare.', 'An instruction needs enough detail for this reader, not every possible detail about the topic.'),
'writing-4': (
 'A paragraph develops one main idea. Begin with the point, support it with relevant detail, then show why the detail matters. The reader should be able to explain what the paragraph is doing in a short phrase. A sentence can be interesting and still belong in a different paragraph if it changes the subject.',
 'Revision checks connections. Read only the first and last sentences: do they match? Then check whether each middle sentence supports that purpose. Put evidence near the claim it supports, and use a transition only when it describes a real relationship. Adding more transition words cannot make unrelated ideas fit.',
 'A paragraph is not defined only by reaching a certain number of sentences.', 'Do not add a new major claim in the final sentence without explaining it.'),
'writing-5': (
 'Precise description selects details that help the reader act or understand. Replace “the thing over there” with a name and a location. Add a quantity, direction, or observable feature when it distinguishes the correct item. The goal is not to use impressive adjectives; it is to reduce the reader’s need to guess.',
 'Separate what you observed from how you interpreted it. “The lid has a two-centimetre crack” is more actionable than “the container is terrible.” A comparison or example can explain an unfamiliar term. Test the description by asking whether another person could find or identify the same object using your words.',
 'An opinion about quality is not a substitute for an observable detail.', 'Precision does not mean sharing unnecessary private information.'),
'writing-6': (
 'A useful request names the situation, the missing information, and the action you want from the reader. If you already know part of the answer, say so briefly. This prevents a long reply explaining things you already understand. One clear request is often easier to answer than several questions buried in a paragraph.',
 'Check whether the receiver can act on the request. If you need a reply before a particular task or time, explain that reason and give a realistic deadline. If a support would help, name it directly: written steps, an example, or a moment to process. You can ask for help without writing a personal history.',
 '“I don’t get it” may need a specific follow-up question to get a useful answer.', 'A request should not pretend that an unanswered assumption is already agreed.'),
'writing-7': (
 'A process explanation tells the reader both what happens and why the steps connect. Use sequence for order and cause words for reasons. Define the input, describe the changes, and identify the output. This is different from a list of commands: an explanation helps a reader adapt when the exact example changes.',
 'Check the explanation for missing links. If you say one step causes another, describe the mechanism or condition that connects them. Include a way to check the result. An example with different numbers or materials can test whether you explained a reusable method rather than only the answer to one task.',
 '“Then” shows order; it does not necessarily show cause.', 'A list of results may leave out the process that produced them.'),
'writing-8': (
 'Make a claim that your evidence can actually support. Introduce the source or observation, present the relevant detail, and explain how it connects. Evidence should be specific enough for someone else to inspect. If the source has a limit, such as a small sample or a short time period, keep that limit visible in your wording.',
 'Revise claims that reach beyond their support. Changing “everyone prefers” to “most respondents in this survey preferred” may make a sentence more accurate without weakening its useful point. Keep your interpretation distinguishable from the source’s exact words. A reader needs to know which part is evidence and which part is your reasoning.',
 'A quote dropped into a paragraph does not explain itself.', 'Do not turn a personal example into a universal rule.'),
'writing-9': (
 'Revision begins with purpose and audience. Ask what the reader must understand or do, then change the content and order to support that purpose. Editing spelling is useful, but it comes after deciding whether the right information is present. Read a draft from the receiver’s position, including what they do not already know.',
 'Revise one kind of problem at a time: missing information, unclear references, organization, then sentence details. Compare the before and after versions and name what improved. Keeping both versions makes revision visible and shows that a first draft is material to work with, not a permanent verdict on your ability.',
 'A longer or more formal replacement can be less clear than the original.', 'Do not remove a condition or exception just to make a sentence shorter.'),
'writing-10': (
 'Work messages should make the next action clear. Put the topic and main point early, include the relevant date or task, and state any action requested. Match tone to the situation while staying direct. A useful subject line helps the receiver recognize the message without opening several unrelated conversations.',
 'Before sending, check recipients, attachments, names, dates, and whether the wording commits you to something you can actually do. Describe a problem using facts and a proposed next step. If an instruction is unclear or conflicting, ask for clarification instead of inventing a promise. Keep private information out unless the recipient needs it.',
 'Politeness does not require hiding the actual request.', 'A confident promise is not useful if the deadline or responsibility was never confirmed.'),
'writing-11': (
 'A developed argument links a position with reasons, evidence, and explanation. Write the claim in one sentence before expanding it. Choose reasons that address the actual decision, not just facts related to the topic. A practical argument often needs to consider cost, benefit, alternatives, and who is affected.',
 'Use a fair counterargument to test the proposal. Explain whether it changes the plan, limits the claim, or can be answered with evidence. A good conclusion follows from the argument you actually made. It should not introduce a new dramatic claim merely to sound persuasive.',
 'Repeating a claim more forcefully does not add support.', 'Attacking a person’s character does not answer a relevant objection.'),
'writing-12': (
 'A project proposal connects a problem with a feasible action. Describe who would benefit, what would be done, who would do it, and which resources are needed. A small clear scope is easier to assess than a promise to solve everything. State assumptions as assumptions so the reader can see what still needs confirmation.',
 'Build a budget and a way to evaluate the result. Separate money already available from money requested. Choose observations that would show whether the activity helped, such as completing a practical task with less support. Include a fallback if funding or time is smaller than expected. A proposal is an honest plan, not a guarantee.',
 'An attractive idea still needs ownership, a time frame, and resources.', 'Participant names or personal circumstances are not required to describe a project’s purpose.'),
'science-1': (
 'An observation is something you can describe or measure with a stated method. An inference explains what might cause it. Keep these separate in notes: “the surface feels warm” is different from “the machine is faulty.” Use units and comparable conditions when measuring so someone else can understand what you actually noticed.',
 'Repeated observations help you check whether a pattern is consistent. Instruments have limits, and two measurements may differ slightly without either person being dishonest. Report a useful level of precision and the conditions of the observation. If the evidence does not identify a cause, say which extra measurement would help.',
 'A confident explanation is still an inference unless the evidence establishes it.', 'More decimal places do not automatically mean a more accurate measurement.'),
'science-2': (
 'A material’s properties affect what it is useful for. Stiffness, flexibility, absorbency, and transparency describe different features. Choose a property relevant to the task before comparing materials. A material can work well for one purpose and poorly for another, so “best” needs a context.',
 'Compare samples using the same method and similar size when possible. Change the material while keeping the test conditions consistent. Record what happened rather than only which one you liked. If you change thickness as well as material, you may not know which change caused the difference.',
 'A material’s colour alone does not tell you its strength or absorbency.', 'One successful trial does not prove a material will work in every condition.'),
'science-3': (
 'A habitat provides resources and conditions an organism needs. Consider water, energy sources, space, and shelter together. A change in one resource can affect several organisms through feeding relationships or competition. Trace a specific connection rather than assuming every organism responds to a change in the same way.',
 'A simple model helps you predict a direction of change, but real habitats contain many interacting factors. Compare the prediction with observations and revise it when needed. If a plant grows poorly, do not assume more water must help: the problem might involve light, soil conditions, disease, or too much water.',
 'A resource can be useful in one amount and harmful in another.', 'A food web describes feeding relationships, not a ranking of which living things matter most.'),
'science-4': (
 'A force is a push or pull with direction. Opposing forces combine into a net force. An object can keep moving with zero net force; a net force changes its motion. In an ideal model, the same force changes the motion of a smaller mass more quickly than a larger mass.',
 'Use a force diagram to separate the forces acting on one object. Check direction as well as size. Friction can oppose sliding, while a support force can balance weight. A simple equation is useful only after you identify the system and the assumptions. Our slider model leaves out friction so you can isolate force and mass.',
 'Motion does not by itself prove that the net force is forward.', 'Mass and force are different quantities with different units.'),
'science-5': (
 'A fair comparison changes the factor you want to investigate while controlling other important conditions. Decide what you will measure before starting. “Which plant looks nicer?” is less precise than measuring height change over the same number of days. A clear method helps someone else repeat the comparison.',
 'If two factors change together, the result may not identify which one mattered. Repeat trials where practical, compare the spread of results, and avoid selecting only the trial that supports your expectation. An unexpected result is information that can help improve the question or method.',
 'Keeping every condition literally identical is impossible; identify the important controls.', 'A comparison can show an association without proving the proposed cause.'),
'science-6': (
 'A particle model represents matter as tiny parts. In a change of state, the substance’s particles remain the same kind while their arrangement and motion change. The drawing is a model, not a literal photograph: the spaces, sizes, and colours are chosen to make a relationship understandable.',
 'Distinguish a change in state or shape from the formation of a new substance. Melting ice and cutting paper do not create different substances simply because they look different. Observations such as colour change or gas production may be clues to a reaction, but the interpretation depends on the situation and evidence.',
 'Particles do not become larger just because a substance expands.', 'Disappearing from view does not establish that matter was destroyed.'),
'science-7': (
 'Energy accounting follows transfers into, within, and out of a system. Name the system boundary and the useful output. A lamp transfers energy to light and to warming its surroundings; the thermal transfer is still part of the accounting even when it is not the intended purpose. Conservation concerns the total, not just the useful part.',
 'Power describes how quickly energy is transferred. The same device used twice as long at constant power transfers twice as much energy. A high-power device can transfer less total energy than a lower-power device if it runs for much less time. Compare both power and duration before deciding which used more energy.',
 'Power and energy are not interchangeable words.', 'Energy described as wasted has been transferred; it has not disappeared.'),
'science-8': (
 'A cell model links structures with functions. A boundary controls exchanges, internal structures carry out processes, and genetic information helps direct activity. Different cells can have different structures and roles. A diagram simplifies their shapes and relative sizes; focus first on which function each label represents.',
 'A multicellular organism depends on coordinated parts. Cells form tissues, tissues contribute to organs, and organs work within systems. A change in one part can affect others because materials and information move between them. Avoid treating a single diagram as a complete account of every cell or every organism.',
 'Not every cell has every structure shown in one textbook diagram.', 'A label names a structure; understanding also requires saying what it does.'),
'science-9': (
 'Read the axes, units, sample, and method before interpreting a graph. Separate the measured pattern from a proposed explanation. A rising line describes a relationship in the displayed data; it does not automatically identify a cause. Check whether a different scale makes the same change appear more dramatic.',
 'Look for repeated patterns, variation, and exceptions. An unusual point may be an error, an important event, or ordinary variation; investigate rather than deleting it automatically. The size and selection of a sample affect how widely you can generalize. A useful conclusion states both the result and its limits.',
 'A graph can be accurately drawn yet support a narrower claim than its headline.', 'Correlation alone does not identify the direction or cause of a relationship.'),
'science-10': (
 'Chemical equations account for atoms. In a reaction, bonds can change and atoms are rearranged into different groupings. In a closed system, the number of each kind of atom is conserved. Count each type on both sides of a model before deciding whether the equation represents a possible rearrangement.',
 'Coefficients change the number of complete molecules; subscripts change what a molecule is. To balance an equation, adjust whole-molecule counts rather than quietly changing the substance. Our coloured-particle example is a bookkeeping model, not instructions for mixing real chemicals. Use it to track what stays constant during a change.',
 'A gas leaving an open container can make the measured container mass fall without destroying atoms.', 'Do not change a formula’s subscript to make an equation appear balanced.'),
'science-11': (
 'Current is the rate of charge flow, while potential difference describes energy transferred per unit charge. In a simple resistor model, increasing voltage at fixed resistance increases current. Increasing resistance at fixed voltage reduces current. This relationship is useful for an idealized resistor; not every electrical device behaves as a constant resistor.',
 'A wave’s amplitude and frequency describe different features. Amplitude measures the size of its variation; frequency counts cycles per second. Changing frequency packs more cycles into the same time interval without necessarily making the wave taller. Read the time axis before deciding whether a wave has a higher frequency.',
 'Current does not mean the amount of energy stored in a battery.', 'A taller wave is not automatically a faster oscillation.'),
'science-12': (
 'A scientific model represents selected relationships to answer a question. Identify what it includes, what it leaves out, and where it has been compared with evidence. A straight-line model may work over a short interval while missing limits that appear later. A model’s usefulness depends on its purpose and range.',
 'Compare predictions with observations and inspect the differences. If the model misses systematically, revise its assumptions or restrict its use. A good fit to existing points does not prove every future prediction. Testing a new situation is more informative than repeatedly checking the same example used to build the model.',
 'A model is not a complete copy of reality.', 'A precise numerical prediction can still rely on an unrealistic assumption.'),
'social-1': (
 'Asking for help starts with identifying the next obstacle. Name the task, what you have already tried, and the specific thing you need. A demonstration, a short explanation, or a written step can each solve different problems. You can choose a communication method that works for you without performing a particular facial expression.',
 'Check the answer by restating the next action. If it still does not make sense, ask for a smaller step or a concrete example. The other person may also need time or may not be the right person to ask. That does not make the question wrong; it changes who or what could help next.',
 'Needing help does not mean you have made no progress.', 'Do not agree that you understand when you still need an important detail.'),
'social-2': (
 'Shared tasks need a clear handoff. Agree on who does which part, how long a turn lasts if relevant, and how someone signals they are ready. A turn can involve speaking, using equipment, or making a decision. The useful rule is one everyone can understand and use, not simply who speaks the loudest.',
 'When a handoff breaks down, describe the task and ask to reset the agreement. You can request a written order or a clear signal. If someone needs more processing time, a pause can be part of the plan. Taking turns does not mean accepting an unfair share of work without discussing it.',
 'Silence is not a reliable agreement to a new responsibility.', 'Equal turns and identical time are not always the same as a workable plan.'),
'social-3': (
 'Confirm the result the instruction is meant to produce, then identify the next action and any missing detail. Repeating the words without understanding the task may hide a misunderstanding. A short restatement lets the other person correct the plan before time or materials are used.',
 'When instructions conflict, state the conflict factually and ask which priority applies. If a task could be unsafe, stop and get appropriate guidance instead of experimenting with a guess. Asking for clarification can prevent rework; it is part of doing a task carefully.',
 'Nodding or saying yes does not itself confirm understanding.', 'Do not invent a deadline or safety procedure that was not supplied.'),
'social-4': (
 'Describe the observable problem before assigning a cause or blame. Include the task, what happened, and how it affects the next step. “Three labels are missing, so I cannot match the boxes” gives another person something specific to work with. If you are unsure of the cause, say that clearly.',
 'Offer a reasonable next step or ask who can decide. Separate a temporary workaround from a permanent fix. After action is taken, check whether the original problem is resolved. A clear report can be brief and direct; it does not need exaggerated language to be worth taking seriously.',
 'A guess about someone’s intention is not an observation.', 'Saying everything is broken can hide the one detail needed to fix the problem.'),
'social-5': (
 'Teamwork becomes easier when the outcome, roles, and check-in point are explicit. Different people can contribute in different ways. Agree how work will be handed over and how a person can flag a problem. Written responsibilities reduce the need to remember an entire spoken conversation.',
 'When progress changes, tell the team what is done, what remains, and which help or decision is needed. Do not silently take over every task or wait until the deadline to mention a blocker. Review the plan together when the original division no longer fits.',
 'Being cooperative does not require agreeing to every request.', 'A task assigned to “someone” may have no actual owner.'),
'social-6': (
 'A useful adjustment changes the task or communication so you can participate more effectively. Identify the barrier and a specific support: written instructions, a quieter place, a demonstration, or a predictable check-in. You can describe the practical need without sharing a diagnosis or personal history.',
 'Check whether the adjustment helps with the actual task. If not, explain what still gets in the way and suggest another approach. Different people may need different supports; there is no single correct preference. This practice is about expressing a need clearly, not deciding legal entitlements or medical treatment.',
 'An adjustment request is not a demand to be treated as incapable.', 'A support that helps one person may not help another.'),
'social-7': (
 'A work plan connects the outcome to actions, resources, and time. Identify which steps depend on earlier ones and which can happen independently. Estimate with some room for ordinary delays. A checklist carries information outside your memory, leaving more attention for the task itself.',
 'Update the plan when a condition changes. State the effect on the deadline and offer realistic choices, such as reducing scope or asking for another person’s help. Confirm the revised priority with the person who can decide. Reporting a delay early gives more options than hiding it until the end.',
 'A list of tasks is not yet a schedule unless it accounts for order and time.', 'Promising an impossible deadline does not resolve conflicting priorities.'),
'social-8': (
 'Begin a disagreement by checking what each person means. Two people may share a goal while disagreeing about timing or method. Describe the observable issue and its effect, then ask a specific question. Keep your boundary clear without needing to insult or diagnose the other person.',
 'A workable resolution names the next action, who owns it, and when to review it. If the conversation becomes threatening, prioritize leaving the situation and seeking appropriate support rather than trying to win the argument. No sample script can guarantee another person’s response; the scenarios show possible outcomes to compare.',
 'Understanding another view does not require agreeing with it.', 'You cannot control another person’s reaction by finding one perfect sentence.'),
'social-9': (
 'Choose a channel that fits urgency and privacy. A routine update may work in a written message; an urgent practical blocker may need a direct check with the responsible person. Put the main point and requested action early. Avoid sending personal information to a group when only one person needs it.',
 'Before replying, check the whole message and any stated deadline. Confirm what you can actually do and ask about anything unclear. If you sent a mistaken detail, correct it promptly and specifically. A useful correction names the changed fact instead of sending several vague follow-up messages.',
 'A short reply can be clear without being rude.', 'Being online does not mean someone has read or understood a message.'),
'social-10': (
 'A job conversation is a chance to connect your experience with the task. Use a specific example: describe the situation, what you did, and what happened or what you learned. Examples can come from projects, volunteering, study, or responsibilities outside paid work. Do not invent experience to make the answer sound stronger.',
 'You can ask for a question to be repeated or for a moment to think. You can also ask what the role involves and how instructions are provided. The aim is an accurate exchange about the work, not a performance of a particular personality. Practice a short answer and revise the parts that feel unclear.',
 'Eye contact and fast answers are not the same as understanding or competence.', 'A memorized script needs adapting when the actual question changes.'),
'social-11': (
 'Useful feedback identifies an observable action, its effect, and a possible next step. “The date is missing, so I cannot schedule it” gives more guidance than “this is bad.” Ask what the receiver wants feedback on, and distinguish a requirement from your personal preference.',
 'When receiving feedback, check the specific change being requested. You can ask for an example or explain a relevant constraint. Decide what to try, then compare the result. Feedback is information about a piece of work or an action; it is not a complete description of a person’s worth.',
 'Praise without a specific observation may not tell someone what to repeat.', 'Disagreeing with one suggestion does not require dismissing all feedback.'),
'social-12': (
 'Define the workplace problem in terms of a result that is not being achieved. Gather relevant facts, identify who can decide, and compare more than one possible response. Consider cost, time, safety, and the people affected. Choose an action within your role rather than changing an unfamiliar system without agreement.',
 'A solution needs follow-through. Name the person responsible, the next action, and a way to check whether it helped. If the evidence shows it did not work, revise the approach. Document a useful handoff so the next person does not have to reconstruct the whole situation from scattered messages.',
 'The first possible fix is not automatically the best one.', 'A problem is not solved merely because someone has been told about it.'),
}

def enrich(units):
    assert set(DEPTH)=={u['id'] for u in units}, 'Every module needs authored depth.'
    for u in units:
        a,b,trap_a,trap_b=DEPTH[u['id']]
        for lesson,why,trap in zip(u['lessons'],(a,b),(trap_a,trap_b)):
            lesson['whyItWorks']=why
            lesson['watchFor']=trap
        u['minutes']=25 if u['subject'] in ('writing','science') else 20
        u['review']=u['review']+[trap_a,trap_b]
