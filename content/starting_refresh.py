"""Add a versioned, practical introduction while preserving saved v1-v4 checks."""
import json
from pathlib import Path
from starting import choice, number

ROOT = Path(__file__).resolve().parents[1]

def tagged(skill, *tasks):
    return [dict(task, skill=skill) for task in tasks]

BANK = {
 'math': [
  tagged('quantity',
   number('How many cartons still need to go in the bag?', 3, 'An order needs 8 cartons. There are 5 in the bag.', 'Cartons to add'),
   number('How many boxes should come out?', 2, 'A shelf has 9 boxes. The label says to keep 7.', 'Boxes to remove'),
   number('How many cups are there altogether?', 9, 'There are 6 cups on the table and 3 on the tray.', 'Number of cups')) +
  tagged('groups',
   number('How many pencils are packed?', 12, 'There are 3 packs, with 4 pencils in each pack.', 'Number of pencils'),
   number('How many notebooks are there?', 24, 'Two sealed packs each hold 10 notebooks. There are also 4 loose notebooks.', 'Number of notebooks'),
   number('How many markers go in each tray?', 4, 'Share 12 markers equally between 3 trays.', 'Markers per tray')),
  tagged('money',
   number('How much change should you receive?', 3.5, 'The total is $6.50 CAD. You hand over $10.', 'Change in dollars'),
   number('What is the total price?', 7.25, 'A sandwich costs $4.50 and a drink costs $2.75. These prices include everything.', 'Total in dollars'),
   number('How much money is left?', 5.75, 'You have $9. You spend $3.25.', 'Dollars left')) +
  tagged('fractions',
   number('How many slices are in one equal share?', 4, 'Share 12 slices equally among 3 people.', 'Slices per share'),
   number('How many labels are used?', 10, 'Use half of a sheet with 20 labels.', 'Number of labels'),
   number('How many cups of water are needed?', 1, 'A recipe needs half a cup of water for one batch. Make two batches.', 'Cups of water')),
  tagged('compare',
   choice('Which pack costs less per notebook?', ['Pack A', 'Pack B', 'They cost the same per notebook'], 1, 'Pack A: 2 notebooks for $6. Pack B: 4 notebooks for $8.'),
   choice('Which option fits within the $15 budget?', ['Two $8 kits', 'Three $4 kits', 'Four $4 kits'], 1, 'You need at least 3 kits. The prices shown include everything.'),
   number('How much will the ride cost?', 11, 'A ride costs $3 to start, plus $2 for each kilometre. You travel 4 kilometres.', 'Cost in dollars')) +
  tagged('time',
   choice('When should the timer finish?', ['2:05 pm', '2:45 pm', '3:15 pm'], 1, 'Start a 30-minute timer at 2:15 pm.'),
   number('How many minutes are available?', 35, 'It is 9:10 am. Your appointment starts at 9:45 am.', 'Minutes available'),
   number('How many hours are worked, after the break?', 3.5, 'A shift runs from 10 am to 2 pm. There is a half-hour unpaid break.', 'Hours worked'))
 ],
 'reading': [
  tagged('reading',
   choice('Where will Jo meet you?', ['The library entrance', 'The park gate', 'The bus stop'], 1, 'Meet Jo at the park gate at 4 pm. Bring your blue folder.'),
   choice('Which entrance should you use today?', ['Main entrance', 'Side entrance', 'Either entrance'], 1, 'The main entrance is closed today. Please use the side entrance.'),
   choice('What should Lee bring?', ['A notebook', 'A bag of books', 'A lunch box'], 0, 'Lee, please bring a notebook to the meeting tomorrow. Lunch will be provided.')) +
  tagged('writing',
   choice('Which message includes both the place and time?', ['See you tomorrow.', 'Meet me at the library at 2 pm tomorrow.', 'The library is nice.'], 1, 'You are arranging a meeting at the library tomorrow at 2 pm.'),
   choice('Which message makes a clear request?', ['Blue folder.', 'Please bring my blue folder.', 'Wherever it is.'], 1, 'You need someone to bring your blue folder.'),
   choice('What detail should you ask for?', ['The meeting place', 'The meeting day', 'The meeting time'], 2, 'The message says, “Meet me at the park gate on Friday.”')),
  tagged('reading',
   choice('Who should label the boxes?', ['Ari', 'Kim', 'Both people'], 1, 'Ari will pack the boxes. Kim will label them after Ari finishes.'),
   choice('What should happen before the lid is closed?', ['Put the note inside', 'Write on the closed lid', 'Move the box outside'], 0, 'Pack the items. Put the note inside. Then close the lid.'),
   choice('Which appointment should you go to?', ['Tuesday at 10 am', 'Wednesday at 11 am', 'Both appointments'], 1, 'Update: your Tuesday 10 am appointment has moved to Wednesday at 11 am. The place is unchanged.')) +
  tagged('writing',
   choice('Which sentence makes clear who will do the task?', ['They will take it.', 'Ari will take the parcel to the post office.', 'That will happen soon.'], 1, 'Ari has agreed to take a parcel to the post office.'),
   choice('Which order is easiest to follow?', ['Close the lid; open the lid; put the items inside.', 'Open the lid; put the items inside; close the lid.', 'Put the items inside; close the lid; open the lid.'], 1, 'Write instructions for packing an empty box whose lid is closed.'),
   choice('Which question asks for the missing detail?', ['What do you mean?', 'Which shelf should I use for these boxes?', 'Are boxes useful?'], 1, 'You have been asked to put boxes on a shelf, but the message does not say which shelf.')),
  tagged('reading',
   choice('What is the main point?', ['Sam is preparing for tomorrow’s shift.', 'Sam is changing jobs.', 'Sam is buying a new phone.'], 0, 'Sam checks the bus time, packs a lunch and puts tomorrow’s work shirt by the door.'),
   choice('What does “charge” mean in this message?', ['Fill a battery', 'A fee', 'Run forward'], 1, 'The receipt includes a delivery charge of five dollars.'),
   choice('Which detail supports the idea that Ari planned ahead?', ['Ari wore a green coat.', 'Ari checked tomorrow’s bus route tonight.', 'Ari walked past a shop.'], 1, 'Ari checked tomorrow’s bus route tonight, then put a green coat by the door.')) +
  tagged('writing',
   choice('Which message explains the problem clearly?', ['It is doing that again.', 'Water is leaking from the pipe under the kitchen sink.', 'The kitchen is bad.'], 1, 'You need to report a leaking pipe under the kitchen sink.'),
   choice('Which subject line will help the reader find your message?', ['Hi!!!', 'Question about my Friday shift', 'Some things'], 1, 'Your email asks which time your Friday shift starts.'),
   choice('Which detail gives evidence for the request?', ['Everyone always needs chairs.', 'Four people had no chair at our last meeting.', 'Chairs are the best.'], 1, 'You are asking for more chairs in a meeting room.'))
 ],
 'science': [
  tagged('observe',
   choice('Which note records an observation?', ['The cup is the best cup.', 'The cup feels cold.', 'The cup wants water.'], 1, 'You are making a note about a cup in front of you.'),
   choice('Which record makes the amount clear?', ['The container holds a lot.', 'The container holds 250 mL.', 'The container looks nice.'], 1, 'You measured water in a marked container.'),
   choice('What do these measurements show?', ['The water became cooler.', 'The water became hotter.', 'The temperature stayed the same.'], 0, 'Water measured 30°C at the start and 24°C ten minutes later.')) +
  tagged('compare',
   choice('Which comparison is fair?', ['Same-size sheets, same amount of water', 'Different-size sheets, different amounts of water', 'One sheet tested; the other not tested'], 0, 'Compare how much water two kinds of paper towel absorb.'),
   choice('What should be kept the same?', ['The material being tested', 'The size of each sample and amount of water', 'Nothing needs to stay the same'], 1, 'Test which of two materials keeps water out better.'),
   choice('What makes the results easier to compare?', ['Measure both trials in the same units', 'Change units halfway through', 'Use no labels on the results'], 0, 'Two people are measuring how far toy carts travel.')),
  tagged('materials',
   choice('Which material is suitable for a rain cover?', ['A waterproof sheet', 'An absorbent paper towel', 'A sheet with many holes'], 0, 'The cover needs to keep rain away from a bag.'),
   choice('Which item will absorb a small spill?', ['A glass lid', 'A paper towel', 'A metal spoon'], 1, 'Choose a material that soaks water into itself.'),
   choice('Which property matters for this task?', ['Whether the label is colourful', 'Whether the material keeps water out', 'Whether the material has a long name'], 1, 'You are choosing a cover for something that must stay dry.')) +
  tagged('changes',
   choice('What happens to the ice?', ['It becomes liquid water.', 'It stops being matter.', 'It becomes a different element.'], 0, 'Ice melts in a closed jar.'),
   choice('What happens to the total mass?', ['It stays the same.', 'It disappears.', 'It doubles.'], 0, 'Ice melts in a closed container. Nothing enters or leaves.'),
   choice('Which result is a change of state?', ['Ice becoming water', 'A cup moving across a table', 'A stone being placed in a box'], 0, 'You are comparing changes you can see in a kitchen.')),
  tagged('separate',
   choice('What would separate these solids?', ['A sieve whose holes pass sand but hold the pebbles', 'A closed lid', 'Adding more pebbles'], 0, 'A dry mixture contains fine sand and larger pebbles.'),
   choice('What should you compare when choosing a sieve?', ['Hole size and particle size', 'The colour of the handle only', 'How long the product name is'], 0, 'You want small grains to pass through and larger pieces to stay behind.'),
   choice('Which result shows separation?', ['The larger pieces remain while smaller grains pass through.', 'All pieces are mixed together again.', 'The total mixture is simply moved to another bowl.'], 0, 'You pour a mixture through a sieve.')) +
  tagged('magnet',
   choice('Which method could separate the steel paper clips?', ['Use a magnet', 'Use a lamp', 'Use a ruler to measure them'], 0, 'A tray contains steel paper clips and plastic beads.'),
   choice('What does this result support?', ['This steel clip is attracted to the magnet.', 'Every metal is attracted to every magnet.', 'Every object in the room is magnetic.'], 0, 'A magnet pulls a steel paper clip toward it.'),
   choice('How could you check whether the magnet attracts this object?', ['Bring the magnet near it and observe what happens.', 'Guess from the object’s colour.', 'Assume every shiny object will move.'], 0, 'You have an unfamiliar object and a magnet.'))
 ],
 'life': [
  tagged('routine',
   choice('Which plan is easiest to check?', ['Keep a short list of the morning tasks', 'Remember every task without a reminder', 'Start a new task each time you forget'], 0, 'You sometimes miss a step while getting ready.'),
   choice('Where would a reminder be useful?', ['Near the place where you do the task', 'Inside a box you never open', 'Only on a device you do not use'], 0, 'You want to remember a regular part of your routine.'),
   choice('What is a useful next step?', ['Put the needed items together before starting', 'Search for each item only after you need it', 'Avoid preparing anything'], 0, 'You are getting ready for a familiar morning task.')) +
  tagged('instructions',
   choice('What should you check before using the cleaner?', ['The product’s directions and warnings', 'Only the bottle’s colour', 'The size of the shop’s sign'], 0, 'You have not used this cleaning product before.'),
   choice('What should you do with an unclear instruction?', ['Ask someone to explain the unclear part', 'Guess and continue', 'Ignore all of the instructions'], 0, 'A care label has a symbol you do not recognise.'),
   choice('Which note would make the task easier to repeat?', ['A short list in the order you do the steps', 'A list of unrelated items', 'No record of what worked'], 0, 'You worked out a routine that is useful to you.')),
  tagged('plan',
   choice('What should you check first?', ['What food you already have', 'Only the most colourful packaging', 'Buy every item on last week’s list again'], 0, 'You are making a grocery list for a few meals.'),
   choice('Which plan fits?', ['A 45-minute recipe', 'A 15-minute recipe', 'Two recipes that each take an hour'], 1, 'You have 20 minutes available to prepare a meal.'),
   choice('What would help avoid buying the same item twice?', ['Check your cupboards against the shopping list', 'Use two separate lists without comparing them', 'Leave the list at home'], 0, 'You have written a grocery list.')) +
  tagged('prepare',
   choice('What should you check before you begin?', ['The ingredients, equipment and steps', 'Only the picture of the finished meal', 'Only the last instruction'], 0, 'You want to follow a recipe you have not used before.'),
   choice('What should you do if the first step is unclear?', ['Ask for an explanation before continuing', 'Skip it without checking', 'Make up an unrelated step'], 0, 'You are following instructions for a new household task.'),
   choice('What makes the plan easier to follow?', ['Group the needed items and read the steps first', 'Start with whichever step looks shortest', 'Change every instruction at once'], 0, 'You have the ingredients for a simple meal.')),
  tagged('care',
   choice('What should you check before washing the shirt?', ['The shirt’s care label', 'Only its colour in a photo', 'The price of an unrelated shirt'], 0, 'This shirt is made from a fabric you have not washed before.'),
   choice('Which approach makes a large cleaning task manageable?', ['Choose one small area and finish it first', 'Begin every area at the same time', 'Keep moving the same items between rooms'], 0, 'A room needs tidying and the full task feels large.'),
   choice('What would make the task safer to start?', ['Clear the walkway before carrying the basket', 'Carry the basket over scattered objects', 'Leave the doorway blocked'], 0, 'You need to carry a laundry basket through a cluttered room.')) +
  tagged('boundaries',
   choice('Which reply makes your available time clear?', ['I can help until 4 pm, then I need to leave.', 'I can stay forever.', 'Maybe sometime.'], 0, 'You can help today but have another commitment at 4 pm.'),
   choice('Which request explains the support you need?', ['Could you write down the steps so I can check them?', 'Nobody should give instructions.', 'I will pretend I understood.'], 0, 'You find spoken instructions difficult to follow in a noisy room.'),
   choice('What is a useful next step?', ['Ask what information is needed and why', 'Give every private detail immediately', 'Publish the information for everyone to see'], 0, 'Someone asks for private information that seems unrelated to the task.'))
 ]
}

def build():
    path = ROOT/'public/starting-point.json'
    bank = json.loads(path.read_text(encoding='utf-8'))
    questions = [dict(task, id=f's5-{subject}-{band}-{i}', subject=subject, band=band)
                 for subject, bands in BANK.items() for band, tasks in enumerate(bands)
                 for i, task in enumerate(tasks)]
    bank['foundation'] = dict(version=5, subjects=list(BANK), stepsPerArea=6,
        questions=questions, starts={s:[1,4,7] for s in BANK}, suggestions={
        'math':['math-1','math-4','math-prices'],
        'reading':['reading-1','reading-3','reading-4'],
        'science':['science-1','science-6','science-light'],
        'life':['life-hands','life-meal-plan','life-home-care']})
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    build()
