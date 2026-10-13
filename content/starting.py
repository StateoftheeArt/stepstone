"""Short, adaptive starting tasks. Original examples, not a standardized test.

The frozen legacy bank is needed to resume/review existing ten-question checks.
Band numbers are private routing metadata, never school grades or mastery.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def choice(prompt, options, answer, scene=''):
    return dict(kind='choice', prompt=prompt, options=options, answer=answer, scene=scene)

def number(prompt, answer, scene='', label='Your answer', visual=None):
    q = dict(kind='number', prompt=prompt, answer=answer, scene=scene, answerLabel=label)
    if visual:
        q['visual'] = visual
    return q

BANK = {
 'math': [
  [number('How many drinks are there in all?', 7, 'You have 4 drinks. You add 3 more.', visual=dict(groups=[4,3], label='4 drinks, then 3 more')),
   number('How many more do you need?', 4, 'The order needs 9 items. You have packed 5.'),
   choice('Which calculation counts all the items?', ['$3\\times4=12$', '$3+4=7$', '$4-3=1$'], 0, 'There are 3 bags. Each bag holds 4 items.')],
  [number('What change should you get?', 3.75, 'You pay 10 dollars for an item costing 6.25 dollars.', 'Change, in dollars'),
   number('What is half of 18?', 9),
   choice('Which amount is the same as $\\frac{3}{4}$?', ['$0.34$', '$0.75$', '$3.4$'], 1)],
  [number('What is $25\\%$ of 40?', 10),
   number('Find $x$: $2x+3=11$.', 4),
   choice('Which expression gives the total cost?', ['$3+2x$', '$3x+2$', '$5x$'], 0, 'A service costs 3 dollars to start, then 2 dollars per hour. You use it for $x$ hours.')],
  [number('If $y=x^2$, what is $y$ when $x=3$?', 9),
   number('How long is the longest side?', 5, 'A right triangle has shorter sides of 3 cm and 4 cm.', 'Length, in centimetres'),
   choice('For $y=x^2$, which calculation gives the slope at $x=2$?', ['$2x=4$', '$x^2=4$', '$x+2=4$'], 0, 'Different methods can give the same number. Choose the method that finds the slope.')]
 ],
 'reading': [
  [choice('Where should you go?', ['The main door', 'The side door', 'The back gate'], 1, 'Please use the side door today.'),
   choice('What should you bring?', ['A pen', 'A book', 'A bag'], 0, 'Meet Lee at the library at 3 pm. Bring a pen.'),
   choice('Which detail is missing?', ['The day', 'The place', 'The time'], 2, 'Meet me at the park gate tomorrow.')],
  [choice('What is the main point?', ['Sam is getting ready for work.', 'Sam is buying new clothes.', 'Sam is changing jobs.'], 0, 'Sam checks the bus time, packs lunch, and puts their work shirt by the door.'),
   choice('Why does Jo cover the bag?', ['To keep the rain out', 'To make it lighter', 'To show what is inside'], 0, 'Rain is forecast, so Jo covers the bag before going outside.'),
   choice('What does “charge” mean here?', ['Fill a battery', 'A fee', 'Run forward'], 1, 'The receipt lists a delivery charge of five dollars.')],
  [choice('Which detail supports the idea that Ari is planning ahead?', ['Ari has a blue coat.', 'Ari checks tomorrow’s route tonight.', 'Ari walks past a shop.'], 1),
   choice('What can this message support?', ['Every bus is always late.', 'This bus was late today.', 'The driver chose to be late.'], 1, 'My bus arrived ten minutes late this morning.'),
   choice('Which detail should you check before treating this as current news?', ['The date of the event', 'The colour of the headline', 'The number of emojis'], 0, 'A post shared today describes a road closure. The linked notice was written three years ago.')],
  [choice('Which conclusion uses both pieces of evidence?', ['Later hours have no cost.', 'Try later hours and compare use with staffing costs.', 'Visitor counts prove all residents want later hours.'], 1, 'A library trial found more evening visitors. Staffing the extra hours also cost more.'),
   choice('Which wording matches the evidence?', ['Everyone benefits from the service.', 'People who replied reported benefits; others may differ.', 'Nobody outside the survey can benefit.'], 1, 'A voluntary survey of service users reports mostly positive experiences.'),
   choice('What extra information would help compare these reports?', ['Whether both measured the same time and group', 'Which writer has the shorter name', 'Whether their headings use the same font'], 0, 'One report says attendance rose. Another says it fell. They do not give their dates or who they counted.')]
 ],
 'writing': [
  [choice('Which message gives a clear action?', ['My blue folder.', 'Please bring my blue folder.', 'Blue, please.'], 1),
   choice('Which version is a complete sentence?', ['At the bus stop.', 'The bus stops here.', 'Because the bus.'], 1),
   choice('Which detail makes the message useful?', ['Meet me sometime.', 'Meet me at the library at 4 pm.', 'Meet me, you know.'], 1)],
  [choice('Which order makes the instructions easy to follow?', ['Open the lid, put the items in, close the lid.', 'Close the lid, put the items in, open the lid.', 'Put the items in, close the lid, open the lid.'], 0, 'Explain how to pack an empty box with a closed lid.'),
   choice('Which sentence belongs in this paragraph?', ['I water them when the soil is dry.', 'My bus has new seats.', 'My phone needs charging.'], 0, 'I grow herbs by the window. They need light and water.'),
   choice('Which question asks for the missing detail clearly?', ['What?', 'Which shelf should I use for these boxes?', 'Why is everything confusing?'], 1, 'Someone asks you to put boxes on a shelf but does not say which shelf.')],
  [choice('Which revision gives the reader enough information?', ['It happened there.', 'Water is leaking under the kitchen sink.', 'The thing is doing that again.'], 1, 'You are reporting a leak so someone can arrange a repair.'),
   choice('Which sentence supports the request with evidence?', ['We need more chairs because I said so.', 'All meetings everywhere lack chairs.', 'At our last meeting, four people had no chair.'], 2, 'You want to explain why this meeting room needs more chairs.'),
   choice('Which subject line helps the reader find your message?', ['Hi', 'Question about my Friday shift', 'IMPORTANT!!!'], 1)],
  [choice('Which revision avoids claiming more than the evidence shows?', ['This trial suggests the new layout may help.', 'The layout will always work for everyone.', 'The trial proves nobody needs help.'], 0, 'In one short trial, people found items faster with a new layout.'),
   choice('Which sentence addresses a reasonable concern?', ['There are no downsides.', 'A trial would let us measure the benefit before paying for a full change.', 'People who disagree do not count.'], 1, 'A proposal may save time, but the new equipment costs money.'),
   choice('What would make the proposal easier to judge?', ['More impressive words', 'A clear goal, steps, costs and a way to check the result', 'Removing every source'], 1)]
 ],
 'science': [
  [choice('Which is something you can observe?', ['The cup feels cold.', 'The cup is the best cup.', 'The cup wants more water.'], 0),
   choice('Which item soaks up a small spill?', ['A metal spoon', 'A paper towel', 'A glass lid'], 1),
   choice('Which place helps an earthworm stay damp?', ['Dry pavement in the sun', 'Moist soil under leaves', 'An empty glass shelf'], 1)],
  [choice('What should you keep the same?', ['Plant type, water and soil', 'The amount of light only', 'Nothing else'], 0, 'You want to test whether more light changes plant growth.'),
   choice('What happens to the total mass?', ['It stays the same.', 'It disappears.', 'It doubles.'], 0, 'Ice melts in a closed jar. Nothing enters or leaves.'),
   choice('Which force pulls a dropped ball toward the ground?', ['Gravity', 'Friction with a table', 'A push from the ceiling'], 0)],
  [choice('Which result would best support the claim?', ['Repeated trials show less cooling with the cover.', 'The covered cup looks nicer.', 'Someone likes the cover.'], 0, 'You are testing whether a cover slows a cup of water cooling.'),
   choice('Where does some of the electrical energy go?', ['Into light and heat', 'It is all destroyed', 'It turns into extra mass in the wire'], 0, 'A lamp lights up and gets warm.'),
   choice('What do cells use a membrane for?', ['Controlling what enters and leaves', 'Making every cell the same shape', 'Stopping all movement forever'], 0)],
  [choice('What should you conclude?', ['The result suggests a link; other factors may matter.', 'The result proves one thing caused the other.', 'Every possible explanation is equally supported.'], 0, 'Two things increase together in a set of observations. No controlled test was done.'),
   choice('Which change raises a wave’s frequency?', ['More cycles in the same time', 'A taller wave with the same timing', 'Moving the drawing upward'], 0),
   choice('What should you do when a model misses some results?', ['Check its assumptions and revise or limit it.', 'Hide the results it misses.', 'Assume the measurements must all be wrong.'], 0)]
 ],
 'social': [
  [choice('Which reply helps you start the right task?', ['Which item do you mean, and where should it go?', 'I will guess.', 'I will move every item.'], 0, 'Someone says, “Put it over there.” You are not sure what they mean.'),
   choice('What could help you finish the task?', ['Skip the missing step.', 'Ask them to repeat or write down step two.', 'Start a different task without saying.'], 1, 'You heard steps one and three, but missed step two.'),
   choice('What could you say?', ['I need a hand with this box. Can someone help?', 'I must lift it without help.', 'I will leave it in the doorway.'], 0, 'A box is too heavy for you to lift comfortably.')],
  [choice('Which request explains what would help?', ['Could you write the steps so I can check them?', 'I will pretend I heard.', 'Nobody should speak again.'], 0, 'A noisy room makes spoken instructions hard to follow.'),
   choice('Which response gives you time to understand?', ['I agree to everything.', 'Could you show one example, then let me try?', 'Please do every task for me.'], 1),
   choice('What should the group agree first?', ['Who will do each part and when to check in', 'That nobody can ask questions', 'That the fastest person makes every decision'], 0, 'Three people are sharing a packing task.')],
  [choice('Which message gives useful information?', ['I will be there sometime.', 'The bus is late. I expect to arrive at 9:15, fifteen minutes late.', 'The bus is annoying.'], 1, 'Your shift starts at 9 am. Your bus is delayed.'),
   choice('What is a useful next step?', ['Check which instruction applies before continuing.', 'Pick one and tell nobody.', 'Assume the other person is trying to cause trouble.'], 0, 'Two people give you different instructions for the same task.'),
   choice('Which reply sets a clear boundary?', ['I can help until 4 pm, then I need to leave.', 'Fine, I will stay as long as anyone wants.', 'You always ask too much.'], 0, 'You can help with a task today, but you have another commitment at 4 pm.')],
  [choice('Which feedback is specific enough to act on?', ['Your report is bad.', 'The report is clear. Adding the delivery date would help us schedule it.', 'Be more professional somehow.'], 1),
   choice('Which reply moves the disagreement toward a solution?', ['Let’s compare the deadlines and decide which task comes first.', 'My idea must win.', 'We should never work together again.'], 0, 'You and a coworker disagree about which task is most urgent.'),
   choice('Which example gives useful evidence of a skill?', ['I am perfect at organising.', 'I labelled our shared supplies so people could find them.', 'Only paid work counts as experience.'], 1, 'You are asked about being organised in a job conversation.')]
 ],
 'digital': [
  [choice('Which name makes the file easier to find?', ['thing-final-new2', 'Friday-shift-notes', 'untitled'], 1, 'You save notes about your Friday shift.'),
   choice('How can you include a saved file in an email?', ['Use the attachment control and select the file.', 'Only type the file name in the message.', 'Rename the email app.'], 0),
   choice('Who should get your sign-in password?', ['Anyone who says they need it', 'Nobody; use the service’s account-sharing or recovery tools', 'Everyone in a group chat'], 1)],
  [choice('What should you check before sending?', ['The recipient, message and attachment', 'Only the colour of the send button', 'Whether the message is very long'], 0, 'You are emailing a completed application.'),
   choice('Where should you start checking a service rule?', ['The service’s official website', 'An unlabelled screenshot', 'The most confident comment'], 0),
   choice('Which address is suitable for job applications?', ['party-anytime@example.com', 'lee.morgan@example.com', 'password123@example.com'], 1, 'These are made-up email addresses. Choose a clear, professional name.')],
  [choice('What is the safest way to check the request?', ['Use the organisation’s known website or contact details.', 'Tap the message link and pay quickly.', 'Send a photo of your ID in reply.'], 0, 'An unexpected text demands an urgent payment through a link.'),
   choice('How can you check whether the claim is reliable?', ['Look for the original source and other independent evidence.', 'Trust it because the picture looks real.', 'Trust it if many people shared it.'], 0, 'A realistic image is being used to support a surprising claim.'),
   choice('What should you do with private information?', ['Remove it before asking a public AI tool for help.', 'Paste all of it because AI always keeps secrets.', 'Post it publicly first.'], 0, 'You want help rewriting a message that contains personal account details.')],
  [choice('What is a sound next step?', ['Run a small test, inspect the result and check the explanation.', 'Submit it without opening it.', 'Assume a long answer must be correct.'], 0, 'An AI tool gives you a spreadsheet formula.'),
   choice('Which workflow keeps you in control?', ['Keep the original, review the changes, then test them.', 'Delete the original before checking.', 'Accept every change at once.'], 0, 'An assistant offers to change several files in your project.'),
   choice('What would best show that you understand the result?', ['Explain it and solve a changed example yourself.', 'Repeat the tool’s answer word for word.', 'Point to how quickly it answered.'], 0)]
 ]
}

def build():
    questions=[]
    for subject,bands in BANK.items():
        for band,variants in enumerate(bands):
            for index,q in enumerate(variants):
                questions.append(dict(q, id=f's2-{subject}-{band}-{index}', subject=subject, band=band))
    bank=dict(version=2,subjects=list(BANK),questions=questions,
              starts={s:([1,3,5,7] if s=='digital' else [1,4,7,10]) for s in BANK},
              writing=dict(prompt='You will be late to meet Jo. You will arrive at 4:15 pm. Write Jo a short message.',
                           review=['Does the message say the writer will be late?', 'Does it give the arrival time?',
                                   'Could Jo understand the plan? Focus on meaning before spelling.']),
              legacy=json.loads((ROOT/'content/starting_legacy.json').read_text(encoding='utf-8')))
    (ROOT/'public/starting-point.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    build()
