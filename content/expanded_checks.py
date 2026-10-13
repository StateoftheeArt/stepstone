"""Server-only check cases for expanded modules. They are never published as practice.

Each case: (prompt, answer, wrong 1, wrong 2, why, wrong reason 1, wrong reason 2).
Cases 0-2 follow the first lesson and 3-5 the second. The reason version states the
answer and asks which reason explains it, so it tests the reason rather than the wording.
"""
CHECKS = {
 'reading-3': [
  ('Fill the kettle, then switch it on. Which step comes second?','Switching it on','Filling the kettle','Neither step has an order',
   '“Then” moves the plan forward, so switching on comes after filling.','The step written first is always the step done last.','“Then” means you can do the steps in either order.'),
  ('Before you leave, turn off the lights. Which action comes first?','Turning off the lights','Leaving','Locking the door',
   '“Before” puts turning off the lights ahead of leaving, even though leaving is written first.','The first action written is always the first action done.','Locking the door is part of every “before you leave” instruction.'),
  ('Steps: 1. Get a clean cup. 2. Pour the juice. 3. Wipe the counter. What do you need before you pour?','A clean cup','A wiped counter','Nothing',
   'Getting a clean cup is step 1, so it comes before pouring in step 2.','Wiping is the last step, so it has to happen before pouring.','Numbered steps can be done in any order.'),
  ('If the bus is late, text your friend. The bus is on time. Do you need to text?','No — the bus is on time','Yes — always text','Yes — text before the bus comes',
   'The text is only needed when the bus is late, and this time it is not.','An instruction that starts with “if” applies every time.','On time and late mean the same thing for buses.'),
  ('Wear gloves unless the box is empty. The box is full. What should you do?','Wear gloves','Skip the gloves','Empty the box first',
   '“Unless” only makes an exception for an empty box, and this box is full.','“Unless” means you never need gloves.','You must empty the box before any rule applies.'),
  ('A sign says: “Staff only after 6 pm.” It is 4 pm and you are not staff. Can you go in?','Yes — the limit starts at 6 pm','No — only staff can ever go in','Only after 6 pm',
   'The staff-only rule applies after 6 pm; at 4 pm it has not started.','“Staff only” means the room is always closed to everyone else.','“After 6 pm” is when people who are not staff are allowed in.'),
 ],
 'writing-2': [
  ('Which is a complete sentence?','The dog barked at the mail carrier.','Barking at the mail carrier.','The dog at the mail carrier.',
   'It names who (the dog) and what it did (barked), and it ends with a period.','Any group of words that ends with a period is complete.','A sentence only needs to name a person or animal.'),
  ('Which sentence tells who did the action?','Priya fixed the chair.','The chair was fixed.','Fixed the chair yesterday.',
   'Priya is named as the person who did the fixing.','The chair is the actor because it is named first.','A sentence names the actor whenever it says when something happened.'),
  ('Which sentence uses capitals and an end mark correctly?','We meet on Monday.','we meet on monday','We meet on monday',
   'It starts with a capital, capitalizes the day, and ends with a period.','Days of the week never need a capital letter.','Short sentences do not need an end mark.'),
  ('Sam and Leo carried the table. He dropped it. What makes the second sentence unclear?','“He” could mean Sam or Leo','It is too short','It needs a question mark',
   'Two people were named, so the reader cannot tell who “he” is.','Every short sentence is unclear.','A sentence about a mistake should end with a question mark.'),
  ('Which sentence has a subject and verb that agree?','The keys are on the hook.','The keys is on the hook.','The keys be on the hook.',
   '“Keys” means more than one, so it pairs with “are”.','“Is” always follows the word “the”.','The verb should match “hook”, which is one thing.'),
  ('A note will be read by someone who was not there. Which version is clearest?','Put the blue folder on Ana’s desk.','Put it over there.','Put that thing on the desk.',
   'It names the object and the exact place, so the reader does not have to guess.','The shortest note is always the clearest.','Words like “there” and “that” tell a reader the exact place.'),
 ],
 'social-1': [
  ('You cannot find where to write your address on a form. Which request names what you need?','Where on this form does my address go?','This form is too hard.','Can you help me with stuff?',
   'It names the exact part of the form you need help with.','Saying a task is hard tells the helper exactly what to explain.','A general request is clearer because it covers everything.'),
  ('It is too loud to talk. How could you still ask for help with one step?','Point to the step or show a written note','Wait until someone guesses','Skip the step without telling anyone',
   'A request can be shown or written; it does not have to be spoken.','A helper should know what you need without being asked.','Skipping a step is the same as asking for help with it.'),
  ('You finished steps one and two of a recipe, but step three is unclear. What is the most useful thing to say?','“I did one and two. What does step three mean?”','“I just don’t get cooking.”','“Can you do the rest for me?”',
   'It shows what you already did and names the step that is unclear.','A general feeling tells the helper which step to explain.','Asking someone to finish the task helps you learn the step.'),
  ('Someone showed you how to change a password. How can you check you understood?','Say the steps back, then try one','Nod and leave right away','Ask them to change it every time',
   'Repeating or trying a step lets the helper catch a mistake early.','Nodding shows the helper you understood every step.','Checking your understanding means never doing it yourself.'),
  ('After an explanation, the part about saving is still unclear. What is a helpful next request?','“Could you show the saving part another way?”','“Never mind, forget it.”','“You explained it wrong.”',
   'It names what is still unclear and asks for a different way to see it.','Stopping as soon as something is unclear saves everyone time.','Blaming the helper makes the next explanation clearer.'),
  ('The helper used a word you do not know. What could you ask?','“What does that word mean? Can you give an example?”','“Use harder words next time.”','“I’ll stay quiet and guess.”',
   'Asking about the word and for an example makes the explanation usable.','Not knowing a word means you are not ready to learn this.','Guessing quietly is the fastest way to learn a new word.'),
 ],
}
