"""Practical missions that retain the existing worked mathematics and check banks."""
from math_missions import task, spec

def num(ident, title, prompt, answer, hint, why, visual=None):
    return task(ident,title,prompt,'number',hint,why,answer=answer,**({'visual':visual} if visual else {}))

def pick(ident, title, prompt, options, answer, hint, why):
    return task(ident,title,prompt,'choice',hint,why,options=options,answer=answer)

MISSIONS={
'math-cash':dict(title='Count cash and check change',goal='Count money by value and rebuild the payment to check change.',needs=['math-5'],
 objectives=['Count the value','Check the change','Catch a mistake'],
 bodies=['Count what each coin is worth, not just how many coins you have. Group coins with the same value. Add dollars and cents carefully.',
 'Change is the payment minus the final total. Count up from the total or subtract. Then add the total and change to check you get the payment back.'],labs=[[
 num('cash-value','Count the coins','You have 2 one-dollar coins and 3 quarters. How many dollars is that?',2.75,'A quarter is 25 cents. Three quarters are 75 cents.','$2+3(0.25)=2.75$ dollars.','money'),
 pick('cash-count','Coins and value differ','Which amount is larger?',['Four quarters.','Two one-dollar coins.','They match because both are coins.'],1,'Four quarters make one dollar.','The value of each coin matters. Two dollar coins total 2 dollars.')],[
 num('cash-change','Check the counter','The final total is 12.75 dollars. You pay 20 dollars. What change should you get?',7.25,'Count 25 cents to 13 dollars, then 7 dollars to 20.','$20-12.75=7.25$. Check: $12.75+7.25=20$.'),
 pick('cash-repair','Question a short amount','You receive 6.25 dollars instead. What is a useful next step?',['Ignore the receipt because there are lots of coins.','Ask to check the total, payment and change together.','Assume the total was 20 dollars.'],1,'Use the receipt and the amounts, without guessing intent.','The amounts are 1 dollar short of rebuilding the payment. Check them together.')]],
 reflection='Show how to check change from 20 dollars for a final total of 12.75 dollars. Describe a calm way to ask about a mismatch.'),
'math-prices':dict(title='Compare two packs',goal='Compare equal items using a unit price and your actual need.',needs=['math-3','math-6'],
 objectives=['Find the price of one','Compare equal amounts','Choose what fits'],
 bodies=['Unit price means the price of one item, or one agreed amount. Divide the pack price by the number of equal items. Compare the same units.',
 'A lower unit price is useful, but you still pay the whole pack price. Check the amount you need, the total you can spend, and whether extra items would be wasted.'],labs=[[
 num('price-one','Read pack A','Pack A has 6 equal items for 12 dollars. What is the price per item?',2,'Divide 12 dollars by 6 items.','$12\\div6=2$ dollars per item.','prices'),
 num('price-other','Read pack B','Pack B has 3 of the same items for 9 dollars. What is the price per item?',3,'Use dollars per item for both packs.','$9\\div3=3$ dollars per item. A smaller total is not always a lower unit price.')],[
 pick('price-budget','Use the actual limit','You need 3 items today and can spend 10 dollars. A costs 12 dollars for 6; B costs 9 dollars for 3. Which fits both limits?',['Pack A','Pack B','Neither pack has 3 items.'],1,'Check how much you must pay today as well as the unit price.','B meets the need within 10 dollars. A has a lower unit price but costs more than the available money.'),
 num('price-size','Compare matching units','A 500 g bag costs 4 dollars. What is its price per 100 g, in dollars?',.8,'There are five 100 g portions in 500 g.','$4\\div5=0.80$ dollars per 100 g. Compare the other bag using that same unit.')]],
 reflection='Explain why the lowest unit price may not be the right purchase today. Show one unit-price calculation with its units.'),
'math-budget':dict(title='Make the money fit',goal='Plan with available money and revise when a cost changes.',needs=['math-5','math-cash'],
 objectives=['Count what is available','Leave room for a change','Revise the plan'],
 bodies=['A budget is a plan for money you actually have. Start with the amount available. Subtract essential costs and any amount you choose to set aside.',
 'When a cost changes, update the plan. A shortfall is a number to solve, not a verdict about you. Change an optional cost or seek support; do not hide the missing money.'],labs=[[
 num('budget-left','Plan the week','You have 80 dollars. Essentials cost 45 dollars. You set aside 10 dollars. How much is left?',25,'Subtract each planned amount once.','$80-45-10=25$ dollars left.','budget'),
 pick('budget-limit','Choose within the amount','There are 25 dollars left. An optional item costs 30 dollars. What keeps the plan realistic?',['Pretend the item costs 25.','Wait or choose an option costing at most 25.','Count the set-aside amount twice.'],1,'The full price must fit money that is available.','Waiting or choosing a cheaper option keeps the numbers honest.')],[
 num('budget-new','Handle a changed cost','Essentials rise from 45 to 53 dollars. You still have 80 and set aside 10. How much is left now?',17,'Update the essential cost; do not subtract the old cost as well.','$80-53-10=17$ dollars.','budget'),
 num('budget-gap','Measure the gap','After that change, a 20-dollar optional plan is too much. By how many dollars?',3,'Compare the 20-dollar plan with the 17 available.','$20-17=3$. Change the plan before treating it as affordable.')]],
 reflection='Write the original 80-dollar plan and the changed plan. Explain one realistic choice if an essential cost leaves too little for everything.'),
'math-pay':dict(title='Read hours and pay',goal='Separate time worked, gross pay and take-home pay.',needs=['math-3','math-5'],
 objectives=['Count paid hours','Read the deductions','Check the statement'],
 bodies=['Gross pay is pay before deductions. For a simple hourly example, multiply paid hours by the hourly rate. Count time carefully; half an hour is 0.5 hours.',
 'Net pay is what remains after the deductions shown on a pay statement. Real rules can add other items. Here, use only the made-up amounts supplied.'],labs=[[
 num('pay-gross','Work out gross pay','In this example, 4 paid hours at 15 dollars per hour gives how many dollars gross?',60,'Multiply hours by dollars per hour.','$4\\times15=60$ dollars before deductions.','timeline'),
 num('pay-time','Count part of an hour','You work from 9:00 to 12:30 with no unpaid break. How many hours is that?',3.5,'There are 3 full hours plus half an hour.','30 minutes is $30/60=0.5$ hours. Total: 3.5 hours, not 3.30.')],[
 num('pay-net','Read a fictional statement','Gross pay: 240 dollars. Total deductions shown: 35 dollars. What is net pay?',205,'Subtract the listed deductions from gross pay.','$240-35=205$ dollars. These made-up deductions are not a tax estimate.'),
 pick('pay-check','Check a difference','Your own time record says 8 hours; the statement says 6. What is a useful next step?',['Ask the payroll contact to compare the dates, paid hours and your record.','Assume gross and net mean the same thing.','Delete the time record.'],0,'Check the same pay period and keep your notes.','A clear record helps identify an entry, break or pay-period difference without guessing what caused it.')]],
 reflection='Show a gross-pay calculation and a net-pay calculation using made-up amounts. Explain why 30 minutes is half an hour, not 0.30 hours.'),
'math-10':dict(title='Cover a square space',goal='Tell area, side length and perimeter apart.',needs=['math-3','math-8'],
 objectives=['Count square units','Work back to a side','Check a bigger space'],
 bodies=['Area measures how much surface is covered. A square has equal sides. Multiply its side by itself to count the small square units inside.',
 'A square root works backwards from area to side length. Doubling the side makes twice as many rows and twice as many columns. The area becomes four times as large.'],labs=[[
 num('square-area','Cover the floor','A square display is 4 metres on each side. What is its area in square metres?',16,'Count 4 rows with 4 square metres in each.','$A=4\\times4=16\\ \\mathrm{m^2}$.','square'),
 pick('square-units','Choose the right measure','Which quantity tells you how much border tape goes around the square?',['Area in square metres.','Perimeter in metres.','Side squared again.'],1,'Tape follows the outside edge.','Perimeter adds the four sides. Area counts the surface inside.')],[
 num('square-root','Find a side from area','A square mat covers 49 square metres. How many metres long is each side?',7,'Find the positive number which gives 49 when multiplied by itself.','$\\sqrt{49}=7$. A physical side length is positive.','square'),
 num('square-scale','Double the side','A square side grows from 3 m to 6 m. How many times larger is its area?',4,'Compare $3^2=9$ with $6^2=36$.','$36\\div9=4$. Both dimensions doubled, so area grew by $2\\times2$.')]],
 reflection='Draw or describe a square with side 3 m and another with side 6 m. Label each area and perimeter. Explain why the area does not just double.'),
'math-11':dict(title='Find a diagonal',goal='Use a right triangle and name the sides correctly.',needs=['math-4','math-10'],
 objectives=['Find the longest side','Choose a side ratio','Check the triangle'],
 bodies=['A right triangle has one 90-degree corner. The side opposite that corner is the hypotenuse. It is the longest side. For the other two sides, $a^2+b^2=c^2$.',
 'Choose an angle before naming its opposite and adjacent sides. Sine compares opposite with hypotenuse. Cosine compares adjacent with hypotenuse. Tangent compares opposite with adjacent.'],labs=[[
 num('triangle-diagonal','Measure across a rectangle','A rectangular sign is 6 units high and 8 units wide. How long is its diagonal?',10,'The diagonal is the hypotenuse: $c=\\sqrt{6^2+8^2}$.','$\\sqrt{36+64}=\\sqrt{100}=10$.','triangle'),
 pick('triangle-condition','Check the condition','When can you use $a^2+b^2=c^2$ for these three side lengths?',['For every triangle.','When the angle between $a$ and $b$ is 90 degrees.','Only when all sides match.'],1,'The right angle is required.','The hypotenuse $c$ sits opposite the right angle. The rule is not for every triangle.')],[
 num('triangle-ratio','Use the named angle','For one chosen angle, the opposite side is 6 and the hypotenuse is 10. What is the sine ratio?',.6,'Divide opposite by hypotenuse. You may enter 6/10.','$\\sin\\theta=\\frac{6}{10}=0.6$. This is a ratio, not the angle in degrees.','triangle'),
 pick('triangle-swap','Choose the other angle','You choose the other acute angle in the same triangle. What happens?',['The hypotenuse becomes a short side.','The opposite and adjacent legs swap names.','All side lengths change.'],1,'The side names depend on which angle you face.','The hypotenuse stays opposite the right angle. The two legs swap their roles.')]],
 reflection='Sketch a right triangle. Label the right angle, hypotenuse, and one chosen angle. Show a diagonal calculation and one trigonometric ratio.'),
'math-12':dict(title='Track a changing rate',goal='Tell a value, an average rate and a local rate apart.',needs=['math-8','math-9'],
 objectives=['Compare two moments','Shrink the interval','Explain the rate'],
 bodies=['A graph shows a value at each time. Its slope shows how fast that value changes. An average rate uses two times: change in value divided by time passed.',
 'For $s(t)=t^2$, shrinking the interval near $t=2$ makes the average rate approach 4. This limiting rate is a derivative. The graph height there is also 4, by coincidence.'],labs=[[
 num('rate-average','Compare two times','For $s(t)=t^2$, $s(2)=4$ and $s(3)=9$. What is the average rate from 2 to 3?',5,'Divide the change in value by the change in time.','$\\frac{9-4}{3-2}=5$. The units are output units per time unit.','curve'),
 pick('rate-height','Read a graph carefully','What does a graph height tell you?',['The value of the quantity at that time.','Always the speed of change.','The number of seconds between two points.'],0,'Height is a value. Slope is a rate.','A large value can be changing slowly; a small value can be changing quickly.')],[
 num('rate-near','Use a shorter interval','For $s(t)=t^2$, find the average rate from $t=2$ to $t=2.5$.',4.5,'$s(2.5)=6.25$. Divide $6.25-4$ by $0.5$.','$\\frac{6.25-4}{0.5}=4.5$, closer to 4 than the previous average of 5.','curve'),
 num('rate-transfer','Separate value from local rate','For this rule, the derivative is $s^{\\prime}(t)=2t$. What is the local rate at $t=3$?',6,'Use the derivative rule, not the original height rule.','$s^{\\prime}(3)=2(3)=6$. The height is $s(3)=9$. These answer different questions.')]],
 reflection='For $s(t)=t^2$ near $t=2$, show one average rate and explain what happens as the time interval shrinks. Explain why dividing by zero is not the method.'),
'math-6':dict(title='Keep the mix the same',goal='Scale a mix and compare a price per pack.',needs=['math-3','math-4'],
 objectives=['Scale both parts','Find the price of one','Check a new mix'],
 bodies=['A drink mix uses 1 cup of concentrate for every 3 cups of water. To make more of the same mix, multiply both amounts by the same number.',
 'A total price can hide the price of one item. Divide the total by the number of equal items. Keep the unit: dollars per item.'],labs=[[
 num('mix-water','Make a bigger batch','Use 4 cups of concentrate. The mix needs 3 cups of water per cup of concentrate. How many cups of water?',12,'Each cup needs 3 cups of water. Find $4\\times3$.','$4\\times3=12$. Both amounts are four times the original mix.','ratio'),
 pick('mix-error','Catch the changed mix','Someone changes a 1:3 mix to 2:4. What went wrong?',['They added 1 to both amounts instead of multiplying both by 2.','Nothing: adding always keeps a ratio.','A ratio cannot get bigger.'],0,'Compare the water for each one cup of concentrate.','The new mix has 2 cups of water per cup of concentrate. The original had 3.')],[
 num('mix-price','Find a price you can compare','Four equal packs cost 12 dollars. What is the price of one pack, in dollars?',3,'Split the total into four equal prices.','$12\\div4=3$ dollars per pack.'),
 num('mix-transfer','Use the same rate','The price stays 3 dollars per pack. How much do 7 packs cost, in dollars?',21,'Multiply the price per pack by the number of packs.','$3\\times7=21$. The total changed; the price of one pack stayed the same.')]],
 reflection='Explain why changing a 1:3 mix to 2:4 changes its strength. Then show a matching mix with 5 cups of concentrate.'),
'math-7':dict(title='Check the sale price',goal='Tell the discount apart from the amount you pay.',needs=['math-4','math-5'],
 objectives=['Find a share of 100','Take off the discount','Check the price'],
 bodies=['Percent means out of 100. A discount of 25% removes one quarter of the price. The amount taken off and the amount you pay are different.',
 'The full price is 100%. If 25% comes off, 75% remains. You can subtract the discount or find 75% of the original price. Both should agree.'],labs=[[
 num('sale-part','Work out the saving','An item is 80 dollars. The discount is 25%. How many dollars come off?',20,'25% is one quarter. Divide 80 by 4.','$80\\times0.25=20$ dollars saved.','percent'),
 pick('sale-whole','Name the whole','What does 100% mean in this sale?',['The original 80-dollar price.','The 20-dollar saving.','The final price after the discount.'],0,'Ask: a percent of which starting amount?','The original price is the whole. The saving is 25% of that whole.')],[
 num('sale-pay','Pay the remaining part','Original price: 80 dollars. Discount: 20 dollars. What is the new price?',60,'Take the saving away from the original price.','$80-20=60$. Also $80\\times0.75=60$.'),
 pick('sale-check','Spot the mix-up','A friend says a 10% discount on 50 dollars means paying 5 dollars. What should they pay?',['5 dollars','45 dollars','40 dollars'],1,'5 dollars is the saving. Find the part left from 50.','$50\\times0.10=5$ saved; $50-5=45$ paid. These practice prices have no extra charges.')]],
 reflection='Show two ways to find the price after 25% comes off 80 dollars. Label the saving and the final price.'),
'math-8':dict(title='Find the missing amount',goal='Use a balanced equation to work backwards from a total.',needs=['math-3','math-5'],
 objectives=['Keep both sides equal','Undo a cost rule','Check your value'],
 bodies=['An equation says two amounts are equal. A letter stands for a number you do not know yet. Do the same operation to both sides to keep them equal.',
 'A made-up ride has a fixed fee plus a cost per kilometre. Take off the fixed fee first. Then divide by the cost per kilometre to find the distance.'],labs=[[
 num('equation-balance','Balance the equation','Find $x$ so that $3x+2=14$.',4,'Subtract 2 from both sides. Then divide both sides by 3.','$3(4)+2=14$. Substitute the answer to check.','balance'),
 pick('equation-reason','Choose a fair move','Which move keeps $3x+2=14$ balanced?',['Subtract 2 from both sides.','Remove 2 only from the left.','Change the right side to 12 without changing the left.'],0,'The two sides must remain equal.','$3x+2-2=14-2$, so $3x=12$.')],[
 num('equation-ride','Work backwards from the bill','A practice ride costs 5 dollars plus 2 dollars per kilometre. The total is 17 dollars. How many kilometres?',6,'Let $x$ be kilometres. Solve $5+2x=17$.','After the 5-dollar fee, 12 dollars pays for distance. $12\\div2=6$ km.'),
 pick('equation-check','Check the unit and total','Which checks a distance of 6 km in that ride?',['$5+2(6)=17$ dollars.','$17+5=22$ kilometres.','$5+2+6=13$ dollars.'],0,'The distance is multiplied by the price per kilometre.','Substitution checks the original rule and keeps the units clear.')]],
 reflection='Write the equation for the ride. Show each operation on both sides and check the distance in the original cost rule.'),
'math-9':dict(title='Read a changing cost',goal='Connect a rule, a table and a straight-line graph.',needs=['math-8'],
 objectives=['Start and step','Compare two points','Use the rule'],
 bodies=['In $y=2x+3$, start at 3 when $x=0$. Each extra step in $x$ adds 2 to $y$. A table and a graph show the same rule.',
 'A slope tells you the change in output for each one-unit change in input. Divide the rise by the run. The starting value is a different number.'],labs=[[
 num('line-value','Find one output','Use $y=2x+3$. What is $y$ when $x=4$?',11,'Replace $x$ with 4. Multiply before adding.','$y=2(4)+3=11$.','line'),
 pick('line-start','Read the starting value','What does the 3 in $y=2x+3$ tell you?',['The output when $x=0$.','The output rises 3 for every input step.','Every output is 3.'],0,'Put 0 in place of $x$.','$2(0)+3=3$. The slope is 2; the starting output is 3.')],[
 num('line-slope','Find the rate from two points','A cost is 3 dollars at 0 km and 11 dollars at 4 km. How many dollars does it rise per km?',2,'Change in cost divided by change in distance.','$\\frac{11-3}{4-0}=2$ dollars per km.','line'),
 num('line-transfer','Use a new starting fee','A new cost rule is $y=2x+5$. What is the cost at $x=4$?',13,'The rate stayed 2. The fixed fee changed to 5.','$2(4)+5=13$. Every cost is 2 higher than under the old rule.')]],
 reflection='For $y=2x+3$, make a small table for $x=0,1,2$. Explain how the starting value differs from the slope.'),
}

GAME_TASKS = {
 'pay-gross': dict(answerLabel='Gross pay in dollars', answerHelp='Enter the money earned before deductions.', mistakes={'4':'4 is the number of hours. This question asks for dollars. Each of those 4 hours earns 15 dollars.'}, game=dict(kind='earn',title='Build the pay, one hour at a time', instruction='Tap each paid hour. Each block adds 15 dollars.', unit='dollars',rate=15, facts=[['Paid time','4 hours'],['Pay for each hour','15 dollars']],parts=[dict(label=f'Hour {i+1}',detail='15 dollars',value=15) for i in range(4)],answerCue='Count all four hours, then enter the total pay below.')),
 'pay-time': dict(answerLabel='Time worked in hours',answerHelp='Use a decimal or a fraction: half an hour is 0.5 or 1/2.',mistakes={'3.3':'30 minutes is half of 60 minutes: 0.5 hours. It is not 0.30 hours.'},game=dict(kind='clock',title='Walk through the shift',instruction='Tap each part of the shift to count its time.',unit='hours',facts=[['Start','9:00 am'],['Finish','12:30 pm'],['Unpaid break','None']],parts=[dict(label='9:00 → 10:00',detail='1 full hour',value=1),dict(label='10:00 → 11:00',detail='1 full hour',value=1),dict(label='11:00 → 12:00',detail='1 full hour',value=1),dict(label='12:00 → 12:30',detail='Half an hour · 0.5',value=.5)],answerCue='Enter the total time in hours below.')),
 'pay-net':dict(answerLabel='Net pay in dollars',answerHelp='Net pay is the money remaining after the listed deductions.',game=dict(kind='budget',title='Read the pay statement',instruction='Tap the listed deduction to take it away once.',unit='dollars',total=240,facts=[['Gross pay','240 dollars'],['Total deductions','35 dollars']],parts=[dict(label='Deductions',detail='Take away 35 dollars',value=35)],answerCue='Enter the money left: net pay in dollars.')),
 'cash-value':dict(answerLabel='Total value in dollars',answerHelp='Include cents as a decimal, for example 1.25.',game=dict(kind='count',title='Count these coins',instruction='Tap each coin once to add its value. A tick means it is counted.',unit='dollars',parts=[dict(label='1 dollar',detail='100 cents',value=1) for _ in range(2)]+[dict(label='Quarter',detail='25 cents',value=.25) for _ in range(3)],answerCue='Enter the value of all five coins in dollars.')),
 'cash-change':dict(answerLabel='Change in dollars',answerHelp='Enter the money returned after the cost is paid.',game=dict(kind='cash',title='Make the change',instruction='Tap or drag money onto the counter. Use Undo if you add too much.',unit='dollars',coins=[500,200,100,25],facts=[['Final cost','12.75 dollars'],['Paid','20.00 dollars']],answerCue='Check that cost plus change makes 20 dollars. Enter your change below.')),
 'sale-part':dict(answerLabel='Saving in dollars',answerHelp='Enter the amount taken off the price.',mistakes={'60':'60 dollars is the price left to pay. This question asks how many dollars you save.'},game=dict(kind='discount',title='Take a quarter off',instruction='The 80-dollar price has four equal parts. Tap one part to take off 25%.',unit='dollars',total=80,parts=[dict(label=f'Part {i+1} · 25%',detail='One quarter of 80 dollars',value=20) for i in range(4)],answerCue='Enter the saving below, not the price left to pay.')),
}
for ident,essentials in [('budget-left',45),('budget-new',53)]:
 GAME_TASKS[ident]=dict(answerLabel='Money left in dollars',answerHelp='Take each planned cost away once.',game=dict(kind='budget',title='Settle the plan',instruction='Tap both planned amounts to take them out of the 80 dollars.',unit='dollars',total=80,facts=[['Available','80 dollars']],parts=[dict(label='Essentials',detail=f'{essentials} dollars',value=essentials),dict(label='Set aside',detail='10 dollars',value=10)],answerCue='Enter the money left after both planned amounts.'))

def attach(units):
    for u in units:
        data=MISSIONS.get(u['id'])
        if not data: continue
        for l,body in zip(u['lessons'],data['bodies']): l['body']=body
        if u['id']=='math-pay':
            u['lessons'][1].update(title='Read take-home pay',example='A fictional statement: gross pay 180 dollars, deductions 25 dollars',steps=[
                'Gross pay is the amount before deductions: 180 dollars.',
                'Subtract the deductions shown: $180-25=155$ dollars net pay.',
                'Check by adding back: $155+25=180$. Net pay plus deductions rebuilds gross pay.'],
                whyItWorks='Gross pay and net pay answer different questions. Gross describes pay before deductions; net is what remains after the deductions shown. Compare the same pay period and keep your own hours record. These made-up deductions teach subtraction, not a tax calculation.')
        u.update(spec(data['title'],data['goal'],u['why'],data['objectives'],u['lessons'],data['labs'],u['review'],data['reflection'],data['needs']))
        for t in u['mission']['labs'][0]+u['mission']['labs'][1]:
            if t['id'] in GAME_TASKS:
                t.pop('visual',None)
                t.update(GAME_TASKS[t['id']])
        u['workshop']={'kind':'scenario'}
        for i,q in enumerate(u['practice']):q['lesson']=2 if q['skill']=='apply' else 1 if q['skill']=='calculate' else 1+i%2
    for u in units:
        if u['id'] in MISSIONS:u['mission']['preparation']=[{'id':i,'title':next(v['title'] for v in units if v['id']==i)} for i in u['mission']['needs']]
