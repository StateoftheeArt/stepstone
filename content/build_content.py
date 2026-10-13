"""Build the public starter library and the server-only checkpoint bank.

This is a general foundation map, not a complete or accredited curriculum.
All examples are original. Rebuild with: python content/build_content.py
"""
import json
import math
from expanded import populate
from depth import enrich
from workshops import attach as attach_workshops
from digital import attach as attach_digital
from ai_course import attach as attach_ai_course
from project_course import attach as attach_project_course
from missions import ORDER_MISSION, READING_MISSION, READING_PARTS, reading_questions as message_questions
from math_missions import attach as attach_math_missions
from math_extension import attach as attach_math_extension
from practical_missions import attach as attach_practical_missions
from science_missions import attach as attach_science_missions
from life_services import attach as attach_life_services
from life_money import attach as attach_life_money
from life_work import attach as attach_life_work
from life_transport import attach as attach_life_transport
from life_home import attach as attach_life_home
from life_support import attach as attach_life_support
from pc_course import attach as attach_pc_course
from typing_course import attach as attach_typing_course
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBJECTS = [
    dict(id="math", name="Math", short="Make numbers make sense", icon="numbers", color="mint"),
    dict(id="reading", name="Reading", short="Understand messages and ideas.", icon="words", color="purple"),
    dict(id="writing", name="Writing", short="Put your ideas into words.", icon="pencil", color="pink"),
    dict(id="science", name="Science", short="Ask questions. Test ideas.", icon="spark", color="orange"),
    dict(id="social", name="Communication & work", short="Ask clearly. Work with others.", icon="compass", color="blue"),
]
TOPICS = {
 "math": ["Pack the order", "Tens and ones", "Equal groups", "Parts of a whole", "Decimals and money", "Ratios that stay fair", "Percent in real life", "Keep equations balanced", "Lines and change", "Square patterns", "Right-triangle tools", "Instantaneous change"],
 "reading": ["Read the plan", "Build a clear sentence", "Put ideas in order", "Find the main point", "Choose precise words", "Explain with evidence", "Read between the lines", "Check a claim", "Compare two accounts", "Build an argument", "Research and reference", "Compare viewpoints"],
 "writing": ["Write a useful message", "Build a sentence", "Put steps in order", "Write a clear paragraph", "Describe precisely", "Ask clearly in writing", "Explain a process", "Use evidence", "Revise for a reader", "Write for work", "Develop an argument", "Write a project proposal"],
 "science": ["Observe and describe", "Materials around us", "Living things and habitats", "Forces and motion", "Make a fair test", "Matter and change", "Energy transfers", "Cells and systems", "Read scientific evidence", "Chemical reactions", "Waves and electricity", "Evaluate a model"],
 "social": ["Ask for help", "Take turns in a task", "Check an instruction", "Explain a problem", "Work in a small team", "Ask for a useful adjustment", "Plan a work task", "Clarify a disagreement", "Messages at work", "Practise a job conversation", "Give and receive feedback", "Solve a workplace problem"],
}

def number(prompt, answer, explanation, skill="calculate", hint="Write down what you know. Then decide which operation connects the numbers."):
    return dict(kind="number", prompt=prompt, answer=answer, explanation=explanation, hint=hint, skill=skill)

def choice(prompt, options, answer, explanation, skill="reason"):
    return dict(kind="choice", prompt=prompt, options=[dict(id=str(i), text=t) for i,t in enumerate(options)], answer=str(answer), explanation=explanation, hint="Compare each choice with the information in the question.", skill=skill)

def math_questions(g, i):
    a, b = 3+i, 2+i%5
    if g == 1:
        a, b = 2+i%7, 1+i%5
        questions = [
            number(f"You pack {a} drink cartons, then {b} more. How many drink cartons are in the bag?", a+b, f"Start at {a}. Count up {b} more: ${a}+{b}={a+b}$ drink cartons.", hint="Count the drink cartons already packed. Count on once for each new drink."),
            choice(f"You pack {a} drink cartons, then {b} more. Which line shows how many you packed?", [f"${a}+{b}={a+b}$", f"${a}-{b}={a-b}$", f"${a}+{b}={a+b+1}$"], 0, f"The plus sign means add more. ${a}+{b}={a+b}$ means both sides count the same number of drink cartons."),
            number(f"The order needs {a+b} drink cartons. You packed {a}. How many more do you need?", b, f"Count from {a} up to {a+b}. That takes {b} more drink carton{'s'*(b!=1)}. Check: ${a}+{b}={a+b}$.", "apply", "Start at the number packed. Count up to the number on the order."),
            number(f"The bag has {a+b} drink cartons. The order needs {a}. How many drink cartons should you take out?", b, f"Take out {b} drink carton{'s'*(b!=1)}: ${a+b}-{b}={a}$. Now the bag matches the order.", "apply", "Count how many extra drink cartons are in the bag."),
            choice(f"The order needs {a+b} drink cartons. You packed {a}. Why would adding {a+b} more be a mistake?", ["It counts the drink cartons already packed twice.", "You must always take drink cartons out.", "The number on the order does not matter."], 0, f"The order asks for {a+b} in all. The {a} already packed count towards that. You only need {b} more."),
        ]
        for j,q in enumerate(questions):
            q['lesson']=1 if j<2 else 2
            q['caseId']=f"order-{i}-{('pack','pack','missing','extra','missing')[j]}"
        return questions
    if g == 2:
        a, b = 2+i%7, 1+i%8
        return [number(f"A number has {a} tens and {b} one{'s'*(b!=1)}. What is it?",10*a+b,f"Each ten is ten ones: ${a}\\times10+{b}={10*a+b}$.",hint="Multiply the number of tens by ten, then add the ones."),number(f"You trade 1 ten from {10*a+b} for 10 ones. How many ones are there now?",10+b,f"The value stays the same: {a-1} ten{'s'*(a!=2)} and {10+b} ones.","apply"),choice(f"Which has the same value as {10*a+b}?",[f"{a} tens + {b} one{'s'*(b!=1)}",f"{b} ten{'s'*(b!=1)} + {a} ones",f"{a} ones + {b} one{'s'*(b!=1)}"],0,"A digit's place gives its value. Trading units changes the grouping, not the total.")]
    if g == 3:
        return [number(f"There are {a} boxes with {b} markers in each. How many markers?",a*b,f"Equal groups multiply: ${a}\\times{b}={a*b}$.",hint="Number of groups times the size of each group gives the total."),number(f"Share {a*b} markers equally among {a} people. How many each?",b,f"Division undoes multiplication: ${a*b}\\div{a}={b}$.","apply"),choice(f"Which story matches ${a}\\times{b}$?",[f"{a} groups of {b}",f"{a} items with {b} removed",f"{a} items with {b} more"],0,"Multiplication counts equal groups. Addition alone does not describe a repeated group unless you repeat it.")]
    if g == 4:
        d, n = [4,5,8,10][i%4], 1+i%3
        return [number(f"A bar has {d} equal parts. {n} {'is' if n==1 else 'are'} shaded. Write the shaded fraction, such as 1/4.",n/d,f"The denominator counts all {d} equal parts. The numerator counts the {n} shaded part{'s'*(n!=1)}: $\\frac{{{n}}}{{{d}}}$.",hint="Shaded parts go above the line. Total equal parts go below it."),number(f"There are {d*3} items. Find $\\frac{{{n}}}{{{d}}}$ of them.",n*3,f"One part is ${d*3}\\div{d}=3$. Take {n} parts: $3\\times{n}={n*3}$.","apply"),choice(f"A friend says $\\frac{{{n}}}{{{d}}}=\\frac{{{n*2}}}{{{d*2}}}$. Why?",["Both part counts are scaled by the same factor.","Only the top number matters.","Every fraction is one half."],0,"Doubling the number of equal pieces and the selected pieces leaves the same share of the whole.")]
    if g == 5:
        cents, count = 125+25*i, 2+i%3
        return [number(f"One item costs ${cents/100:.2f}. What do {count} items cost, in dollars?", cents*count/100,f"Work in cents: ${cents}\\times{count}={cents*count}$ cents, or {cents*count/100:.2f} dollars.",hint="Multiply in cents, then divide by 100 to return to dollars."),number(f"You pay 20 dollars for an item costing {cents/100:.2f} dollars. What is the change?",20-cents/100,f"Align decimal places: $20.00-{cents/100:.2f}={20-cents/100:.2f}$ dollars.","apply"),choice(f"Which is equal to {cents/100:.2f} dollars?",[f"{cents} cents",f"{cents*10} cents",f"{cents/10:g} cents"],0,"One dollar contains 100 cents. A decimal point marks place value; it is not decoration.")]
    if g == 6:
        return [number(f"A mix uses {b} cups of water for 1 cup of concentrate. How much water for {a} cups of concentrate?",a*b,f"Scale both quantities by {a}: ${b}\\times{a}={a*b}$ cups of water.",hint="Keep the amount of water per one cup of concentrate unchanged."),number(f"{b} identical packs cost {a*b} dollars. What is the price per pack?",a,f"Divide the total cost by the number of packs: ${a*b}\\div{b}={a}$ dollars per pack.","apply"),choice(f"A ratio is $1:{b}$. Which keeps the same mix?",[f"$2:{b*2}$",f"$2:{b+1}$",f"$1:{b*2}$"],0,"Multiply both sides by the same number. Adding the same number usually changes the ratio.")]
    if g == 7:
        total, p = (i+3)*20, [10,25,50,75][i%4]
        return [number(f"Find {p}% of {total}.",total*p/100,f"Percent means per hundred: $\\frac{{{p}}}{{100}}\\times{total}={total*p/100:g}$.",hint="Change the percent into a fraction out of 100, then multiply."),number(f"A {total}-dollar item is discounted by {p}%. What is the new price?",total*(100-p)/100,f"The discount is {total*p/100:g}. Subtract it: ${total}-{total*p/100:g}={total*(100-p)/100:g}$.","apply"),choice(f"A price is reduced by {p}%. What share do you still pay?",[f"{100-p}%",f"{p if p!=50 else 25}%","100%"],0,"The original whole is 100%. Subtract the discount percentage to find the part you still pay.")]
    if g == 8:
        solution=2+i%7
        total=b*solution+a
        return [number(f"Solve for $x$: ${b}x+{a}={total}$.",solution,f"Subtract {a} from both sides: ${b}x={b*solution}$. Divide both sides by {b}: $x={solution}$.",hint="Undo addition on both sides first. Then undo multiplication on both sides."),number(f"A ride costs {a} dollars plus {b} dollars per kilometre. The total is {a+b*(i+2)} dollars. How many kilometres?",i+2,f"Let $x$ be kilometres. ${a}+{b}x={a+b*(i+2)}$, so $x=({a+b*(i+2)}-{a})/{b}={i+2}$.","apply"),choice(f"In ${b}x+{a}={total}$, which first step keeps the balance?",[f"Subtract {a} from both sides.",f"Subtract {a} only on the left.",f"Divide only the left by {b}."],0,"An equation says two amounts are equal. Applying the same operation to each side preserves that equality.")]
    if g == 9:
        return [number(f"For $y={b}x+{a}$, find $y$ when $x=3$.",b*3+a,f"Substitute for x, then multiply before adding: $y={b}(3)+{a}={b*3+a}$.",hint="Replace x with 3. The coefficient multiplies x."),number(f"A line goes through $(0,{a})$ and $(4,{a+4*b})$. What is its slope?",b,f"Slope is change in y divided by change in x: $m=\\frac{{{a+4*b}-{a}}}{{4-0}}={b}$.","apply"),choice(f"In $y={b}x+{a}$, what does {a} represent?",["The y value when x is zero.","The change in y for each step in x.","The largest possible y value."],0,"Set x to zero: the multiplication term becomes zero, leaving the starting value (the y-intercept).")]
    if g == 10:
        n = i+2
        return [number(f"A square has side length {n}. What is its area?",n*n,f"Square area is side times side: $A={n}^2={n*n}$ square units.",hint="A square grows in two directions. Multiply its side length by itself."),number(f"Find the positive solution of $x^2={n*n}$.",n,f"Take the square root: $x={n}$. The word positive excludes the other solution, $-{n}$.","apply"),choice(f"A square's side doubles from {n} to {n*2}. What happens to its area?",["It becomes four times as large.","It becomes twice as large.","It stays the same."],0,"Both dimensions double: $(2x)^2=4x^2$. This is quadratic, rather than constant-rate linear, growth.")]
    if g == 11:
        k = i+1
        return [number(f"A right triangle has legs {3*k} and {4*k}. Find its hypotenuse.",5*k,f"$c=\\sqrt{{({3*k})^2+({4*k})^2}}={5*k}$.",hint="For a right triangle, square both shorter sides, add them, then take a square root."),number(f"Relative to angle A, the opposite side is {3*k} and the hypotenuse is {5*k}. Find $\\sin A$.",.6,f"Sine compares opposite to hypotenuse: $\\sin A=\\frac{{{3*k}}}{{{5*k}}}=0.6$.","apply"),choice("Which side is always the hypotenuse?",["The side opposite the right angle.","The side at the bottom of the drawing.","The shortest side."],0,"Triangle orientation does not change side roles. Find the right angle first; the side across from it is the hypotenuse.")]
    t = i+2
    return [number(f"A position is $s(t)=t^2$. Find the average rate from $t={t}$ to $t={t+1}$.",2*t+1,f"$\\frac{{s({t+1})-s({t})}}{{({t+1})-{t}}}=\\frac{{{(t+1)**2}-{t*t}}}{{1}}={2*t+1}$.",hint="Average rate is output change divided by input change over an interval."),number(f"For $s(t)=t^2$, the instantaneous rate is $s'(t)=2t$. Find the rate at $t={t}$.",2*t,f"Substitute time into the derivative: $s'({t})=2({t})={2*t}$.","apply"),choice("How does a derivative differ from an average rate over a long interval?",["It gives the local rate as the interval shrinks toward zero.","It is always the largest value of the function.","It is the total area below the curve."],0,"A derivative describes local change. A function value is a height; an integral accumulates quantities. They answer different questions.")]

MATH = [
 ("Put the drink cartons together", "You are packing an order. You put 5 drink cartons in the bag, then add 3 more. How many are in the bag now?", "Pack the right amount. Use this when shopping, sharing food, or getting an order ready at work.", "5 drink cartons, then 3 more", ["Start with 5 drink cartons.","Add one at a time. Count 6, 7, 8.","Write $5+3=8$. There are 8 drink cartons in all."], "Take out the extras", "The order asks for 4 drink cartons. There are 6 in the bag. Take out enough to leave 4.", "The order needs 4. You packed 6.", ["Start at 6. Take out one carton: 5 are left.","Take out one more: 4 are left. You took out 2. $6-2=4$.","Check: the 4 packed and the 2 taken out make the 6 you started with. $4+2=6$."], "order"),
 ("A place gives a digit its value", "In 34, the 3 means three tens, or 30. The 4 means four ones. A digit has a different value when it moves to a different place.", "Place value helps you read prices, count supplies, and subtract with confidence.", "Build 34",["Make 3 groups of ten: $3\\times10=30$.","Add 4 single ones.","Combine: $30+4=34$."],"Trade without changing the total","One ten can be traded for ten ones. This is what regrouping means. You have changed the groups, not the amount.","Regroup 34",["Start with 3 tens and 4 ones.","Trade one ten for 10 ones.","Now you have 2 tens and 14 ones: $20+14=34$."],"place"),
 ("Count equal groups", "Multiplication counts equal-sized groups. Three groups of four is four added three times. The multiplication sign is a shorter way to record the same idea.","Use equal groups for packaging, recipes, teams, and shared supplies.","3 trays, 4 items in each",["Each tray has the same amount: 4.","Add the groups: $4+4+4=12$.","Shorter form: $3\\times4=12$."],"Share a total equally","Division asks how many are in each group, or how many groups you can make. Check a division by multiplying back.","Share 12 among 3",["Split into 3 equal groups.","$12\\div3=4$ in each group.","Check: $3\\times4=12$."],"groups"),
 ("Name a part of a whole","A fraction describes equal parts. In three quarters, the 4 says the whole has four equal parts. The 3 says you selected three of them. Unequal pieces cannot be counted this way.","Fractions describe food portions, materials, distance, and time.","Three quarters of a bar",["Split one whole into 4 equal parts.","Select 3 of those parts.","Write $\\frac{3}{4}$. It is less than one whole."],"Find a fraction of an amount","First divide by the denominator to find one part. Then multiply by the numerator to take the number of parts you need.","Three quarters of 20",["One quarter: $20\\div4=5$.","Three quarters: $5\\times3=15$.","Check: 15 is less than 20 and more than half of 20."],"fraction"),
 ("Keep decimal places lined up","A decimal continues place value to the right of the ones. One tenth is ten hundredths. With money, dollars and cents give a useful model: 100 cents make one dollar.","Use decimals to compare prices, measure lengths, and check change.","3 items at 1.25 dollars each",["1.25 dollars is 125 cents.","$125\\times3=375$ cents.","375 cents is 3.75 dollars."],"Check your change","Subtract the cost from the amount paid. Keep equal places under each other. An estimate tells you whether the exact answer makes sense.","Pay 10 dollars for a 3.75-dollar item",["Estimate: about $10-4=6$ dollars back.","Exact change: $10.00-3.75=6.25$.","Check: $6.25+3.75=10.00$."],"place"),
 ("Keep the relationship","A ratio compares quantities. One cup of concentrate to three cups of water means the water is always three times the concentrate. Scaling both amounts keeps the same mix.","Ratios help with recipes, maps, unit prices, and mixing materials.","Double a 1 to 3 mix",["Start with 1 cup concentrate and 3 cups water.","Multiply both amounts by 2.","The new mix is 2 cups concentrate and 6 cups water."],"Find the amount per one","A unit rate compares an amount with one unit. Divide first. Then multiply if you need a different number of units.","4 packs cost 12 dollars",["Per pack: $12\\div4=3$ dollars.","For 7 packs: $3\\times7=21$ dollars.","Check the unit: dollars per pack times packs gives dollars."],"ratio"),
 ("Percent means per hundred","A percentage describes a share of a whole. Twenty-five percent means twenty-five out of one hundred, which is one quarter. Always identify the whole before calculating.","Use percentages for discounts, progress, survey results, and comparisons.","25 percent of 80",["Change the percent into a fraction: $25\\%=\\frac{25}{100}$.","Multiply by the whole: $0.25\\times80=20$.","A quarter of 80 is 20, so the answer fits."],"Separate a discount from a new price","A discount is the amount removed. The sale price is the amount left. They are different numbers.","80-dollar price with 25 percent off",["Find the discount: $0.25\\times80=20$ dollars.","Subtract it: $80-20=60$ dollars.","Shortcut: pay 75 percent, so $0.75\\times80=60$."],"fraction"),
 ("An equation is a balance","An equation says two expressions have equal value. An unknown, such as x, represents a number you do not know yet. Keep equality true by doing the same operation to both sides.","Equations help you find a missing cost, distance, quantity, or measurement.","Solve $3x+2=14$",["Subtract 2 from both sides: $3x=12$.","Divide both sides by 3: $x=4$.","Check in the original: $3(4)+2=14$."],"Build the equation from a story","Name the unknown and its unit. Separate the starting amount from the amount that repeats. Then solve and check against the story.","A ride costs 2 dollars plus 3 per kilometre. Total: 14 dollars.",["Let x be the distance in kilometres.","Write the cost relationship: $2+3x=14$.","Solve: $x=4$. A 4 km ride costs $2+3(4)=14$."],"balance"),
 ("A line has a starting value and a rate","In the equation y equals m times x plus b, m is the change in y for one step in x. The value b is where y starts when x is zero. A constant rate makes a straight line.","Model a starting fee plus a repeated cost, distance at constant speed, or a filling tank.","$y=2x+3$ at $x=4$",["Replace x with 4: $y=2(4)+3$.","Multiply first: $y=8+3$.","Add: $y=11$."],"Find a rate from two points","Slope compares the output change with the input change. Keep both changes in the same direction. A negative slope means the output falls as the input rises.","From (0, 3) to (4, 11)",["Output change: $11-3=8$.","Input change: $4-0=4$.","Slope: $m=8/4=2$."],"line"),
 ("Two changing dimensions make a square pattern","For a square, area is side times side. If the side doubles, both dimensions double. Area becomes four times as large. This is an example of quadratic growth.","Use square patterns for area, material planning, and understanding curved graphs.","A square grows from side 3 to side 6",["Original area: $3^2=9$.","New area: $6^2=36$.","Compare: $36/9=4$. The area quadrupled."],"Undo a square with a square root","A square root asks which nonnegative number, multiplied by itself, produces the given value. An equation with x squared can have a positive and a negative solution. Context decides which is useful.","$x^2=25$ for a physical side length",["Both $5^2=25$ and $(-5)^2=25$.","A length is nonnegative.","So the physical side length is 5 units."],"square"),
 ("Find the right angle first","The hypotenuse is opposite the right angle. The other two sides are the legs. In a right triangle, the squares on the two legs add to the square on the hypotenuse.","Right triangles connect horizontal distance, height, and diagonal length.","Legs 3 and 4",["Use $a^2+b^2=c^2$.","$3^2+4^2=9+16=25$.","$c=\\sqrt{25}=5$."],"Compare sides using an angle","The opposite side lies across from your chosen angle. Sine is opposite divided by hypotenuse. This ratio stays the same when a triangle grows without changing its angles.","Opposite 3, hypotenuse 5",["Label sides relative to the chosen angle.","$\\sin A=\\frac{\\text{opposite}}{\\text{hypotenuse}}=\\frac35=0.6$.","The ratio 0.6 is not an angle measured in degrees."],"triangle"),
 ("Compare average and local change","Average rate compares two points. A curve can change at different rates along its length. To understand the rate near one point, look at a smaller and smaller interval around it.","Rates of change describe speed, growth, cooling, and changing costs.","$s(t)=t^2$ between $t=2$ and $t=3$",["Find positions: $s(2)=4$ and $s(3)=9$.","Position change is 5; time change is 1.","Average rate is $5/1=5$."],"Shrink the interval","For a square function, the slope between t and t plus h is two t plus h. As h gets closer to zero, this approaches two t. That local rate is the derivative.","Find the rate of $s(t)=t^2$ at $t=2$",["$\\frac{(t+h)^2-t^2}{h}=2t+h$ for nonzero h.","As h approaches zero, the rate approaches $2t$.","At $t=2$, the instantaneous rate is $s'(2)=4$."],"curve"),
]

def reading_questions(g, i):
    names=["Alex","Sam","Jo","Lee","Ari","Kim","Rae","Mo","Max","Ash","Drew","Kai"]
    name=names[i%len(names)]
    hour=2+i%5
    if g==1:
        return message_questions(i)
    if g==4:
        return [choice(f"Read: {name} started a small garden. They planted beans, watered them, and moved the pots into sunlight. What is the main point?",[f"{name} is growing a garden.","The pots are all red.","Beans never need water."],0,"The main point covers all the important details without adding a new claim.","calculate"),choice(f"Read: {name} walks to the library every Saturday to borrow books. They like adventure stories best. Which detail tells you when?",["Every Saturday","The library","Adventure stories"],0,"When asks about time. Where asks about place.","apply"),choice(f"Read: {name} checks the weather before a trip and packs a jacket because rain is expected. Which summary fits?",[f"{name} prepares for a rainy trip.",f"{name} dislikes every trip.","It always rains in summer."],0,"A summary keeps the important idea and leaves out unsupported guesses.")]
    if g==8:
        n=10+i
        return [choice(f'A post says: "This method helps everyone. I asked {n} friends and {n-1} liked it." Which part is the broad claim?', ["This method helps everyone.",f"The writer asked {n} friends.",f"{n-1} friends liked it."],0,"The claim is the conclusion the writer wants you to accept. The survey is offered as support.","calculate"),choice(f"{name} says one small survey proves a product works for all people. What is the strongest concern?",["The small group may not represent all people.","All numbers are automatically false.","A confident tone proves the conclusion."],0,"A small or selected sample limits the claim. It does not automatically make every observation false.","apply"),choice(f"Two pages disagree about an event. What should {name} do next?",["Check dates, original sources, and evidence on both pages.","Pick the page with the larger title.","Share the more exciting claim immediately."],0,"Trace a claim to evidence. Popularity and presentation are not substitutes for support.")]
    return [choice(f"{name} reads two views on a later library closing time. View A cites evening visitor counts. View B cites staffing costs. How can both matter?",["They measure different benefits and costs of the same choice.","Only one can contain any true fact.","Neither offers information."],0,"Different evidence can illuminate different parts of a decision. Compare what each source actually supports.","calculate"),choice(f"A writer concludes that a later closing time always benefits every visitor. Which revision is better supported by one month's visitor counts?",["The counts suggest some visitors used the later hours that month.","Every visitor will always benefit.","Counts can never support any claim."],0,"Match the strength and scope of the claim to the limits of the evidence.","apply"),choice("Which response synthesizes two viewpoints rather than merely listing them?",["Later hours could improve access, but staffing costs should be compared with the additional visits.","The first view exists. The second view also exists.","I like one writer's name better."],0,"Synthesis connects the evidence and the tradeoff to develop a reasoned position.")]

def science_questions(i):
    n=2+i
    return [choice(f"You test whether light affects plant growth. All plants get {n} cups of water weekly. What should you change between groups?",["Light exposure","Light, soil, and water all at once","The ruler after each measurement"],0,"Change the factor being tested. Keep other relevant conditions similar.","calculate"),choice(f"One group grows {n} cm and another {n+2} cm. What can you report directly?",[f"The second group grew 2 cm more in this test.","Light always makes every plant grow exactly 2 cm more.","The first plants did not grow."],0,"Report the measurement before extending it into a broader claim. One test has limits.","apply"),choice("Why repeat the test with more plants?",["To see whether the pattern is consistent and reduce the influence of unusual cases.","To guarantee the result you want.","To avoid recording measurements."],0,"Repeated measurements help you judge reliability. They do not guarantee a particular outcome.")]

def life_questions(i):
    income,essential,save=50+10*i,20+5*i,10
    remain=income-essential-save
    return [number(f"A practice budget has {income} dollars available, {essential} for essentials, and {save} set aside. How much is left?",remain,f"Subtract both planned amounts: ${income}-{essential}-{save}={remain}$.",hint="Start with the amount available. Subtract each planned amount once."),choice(f"Your practice plan has {remain} dollars left. An optional item costs {remain+5}. What keeps the plan within its limit?",["Wait, choose a cheaper option, or change the plan explicitly.","Ignore part of the item's cost.","Assume the missing 5 dollars is already available."],0,"A workable plan accounts for the full cost and actual available resources.","apply"),choice("An unexpected cost changes a plan. What is a useful next step?",["Update the numbers and identify a realistic next choice.","Hide the cost from the calculation.","Treat one change as proof you can never plan."],0,"A budget is a changing plan, not a judgement of your worth. Use the new information to revise it.")]

EXTRA = [
 ("reading",1,*READING_PARTS,reading_questions),
 ("reading",4,"Find the idea that holds the details together","A main point tells what a passage is mostly about. Details explain, support, or illustrate that point. A detail can be true without being the main point.","Understand a paragraph without getting lost in every detail.","Sam repairs a bike: they pump the tyres, adjust the seat, and test the brakes.",["Notice the repeated purpose: making the bike ready.","The tyre, seat, and brake details all support it.","Main point: Sam is getting a bike ready to ride."],"Write a fair summary","Keep the important meaning in fewer words. Do not add an opinion or a detail that was never stated.","Rain is forecast, so Jo packs a jacket and covers the bag.",["Cause: rain is forecast.","Actions: protect themselves and the bag.","Summary: Jo prepares for rain."],"message",reading_questions),
 ("reading",8,"Separate a claim from its support","A claim is something a person asks you to believe. Evidence is the information offered to support it. A strong feeling or confident voice is not, by itself, evidence.","Read online posts, adverts, and arguments with more independence.","Everyone likes this game. Nine of my ten friends liked it.",["Claim: everyone likes it.","Evidence: nine of ten friends liked it.","Limit: ten selected friends do not represent everyone."],"Check how far the evidence reaches","Ask who collected the information, when, and how. A source can be useful while still having limits. Match your conclusion to what was actually observed.","A survey of one class suggests a later lunch time is popular.",["Find the original survey, not just a screenshot.","Check who was asked and which question was used.","Say one class preferred it. Do not claim every school agrees."],"evidence",reading_questions),
 ("reading",12,"Compare reasons, not just conclusions","Two sources may disagree because they ask different questions or value different outcomes. Identify each claim, its evidence, and what it leaves out.","Build a reasoned position in study, work, and community decisions.","Should a library stay open later?",["View A: evening visits suggest a need for access.","View B: staffing records show a higher operating cost.","Both can be true. The decision involves a tradeoff."],"Connect evidence into a position","Synthesis means using the relationship between sources to develop a conclusion. Explain the tradeoff and qualify claims where the evidence is limited.","Write a supported recommendation.",["Start with a position: trial later opening on one evening.","Give the reason: test demand while limiting extra cost.","State what to measure: additional visits and staffing costs."],"evidence",reading_questions),
 ("science",5,"Change one factor","A fair comparison changes the factor you want to test while keeping other relevant conditions similar. Record what you change and what you measure before starting.","Test an idea instead of relying only on a guess.","Does light affect plant growth?",["Change: hours of light.","Measure: growth in centimetres over the same time.","Keep similar: plant type, water, soil, and starting size."],"Report what you observed","An observation describes what happened in your test. A conclusion explains what the result suggests. Repetition and more examples help test whether the pattern holds.","One group grows 3 cm; the other grows 5 cm.",["Observation: one group grew 2 cm more.","Possible conclusion: the light conditions may affect growth.","Next check: repeat with more plants and the same method."],"experiment",lambda g,i:science_questions(i)),
]

def writing_questions(g,i):
    task=["bring the folder","check the stock","move the boxes","label the shelves"][i%4]
    if g==1:
        return [choice(f'Which message clearly asks someone to {task}?',[f"Please {task}.","Thing stuff later.","Yes maybe."],0,"A useful message names an action and the thing involved.","calculate"),choice("Which sentence gives a time and a place?",["Meet me at the library at 3.","Meet me somewhere.","See you."],0,"A reader should not have to guess information you already know.","apply"),choice("You reread your message and notice a missing word. What is a useful next step?",["Add the word and reread the message.","Assume the reader can see your thoughts.","Delete the whole conversation."],0,"Writing is a process. Revising a message makes it easier for someone else to use.")]
    if g==6:
        return [choice(f'You were asked to {task}, but the deadline is unclear. Which request is specific?', [f"What time should I finish when I {task}?","I do not understand anything.","Never mind."],0,"Name the missing information. A specific question is easier to answer.","calculate"),choice("Which request makes written instructions easy to provide?",["Could you write the steps in order so I can check them as I work?","You should know what I need.","I will guess every step."],0,"You can explain the support that helps without disclosing a diagnosis.","apply"),choice("A message has three unrelated questions in one long sentence. How can you make it easier to answer?",["Put each question on its own line.","Remove every full stop.","Write it all in capitals."],0,"Structure helps the reader see and answer each part. Clear layout matters as well as wording.")]
    return [choice(f'Which subject line helps a supervisor find a message about how to {task}?',[f"Question about the steps to {task}","Hi","IMPORTANT EVERYTHING"],0,"A specific subject line names the purpose without exaggeration.","calculate"),choice("You need clarification before starting a task. Which message is useful?",["I have the list. Should I finish section A or section B first?","Your instructions are useless.","I will do neither and say nothing."],0,"State what you know, then ask about the decision that is missing.","apply"),choice("Before sending a work message, what should you check?",["The recipient, purpose, important details, and tone.","Whether it is the longest message possible.","Whether it contains impressive words you cannot explain."],0,"The goal is to help the reader understand and act. Plain, accurate wording is effective.")]

def social_questions(g,i):
    item=["boxes","folders","tools","labels"][i%4]
    if g==3:
        return [choice(f'Someone says, "Put the {item} over there." You are not sure where. What could you say?',[f"Which shelf should the {item} go on?","I will choose any place and say it is done.","I cannot ever do this task."],0,"Pointing out the missing detail helps you do the task correctly. It is okay to ask.","calculate"),choice("Which response checks an instruction?",["So first I sort them, then I label them. Is that right?","I heard a few words, so I will guess.","I will change every step."],0,"Restating the steps gives the other person a chance to clarify before you begin.","apply"),choice("You understand a task best when you can see it. What is a reasonable request?",["Could you show me one example?","I must pretend I understand.","No one may ever explain it differently."],0,"An example, a written list, or another explanation may help. There is more than one valid way to learn.")]
    if g==6:
        return [choice("A noisy workspace makes instructions hard to follow. What is a clear request?",["Could we go through the steps somewhere quieter, or write them down?","I should hide the problem and guess.","I must force myself to make eye contact."],0,"Ask for a practical change that helps you do the task. Eye contact is not a measure of understanding.","calculate"),choice("Which information do you need to share to ask for written steps?",["The support you need; you can choose whether to share personal medical details.","Your entire medical history every time.","Your family situation."],0,"A request can focus on how you work best. The lesson does not require disclosure of private information.","apply"),choice("You need time to process a question. Which response communicates that?",["Give me a moment to think, please.","I have to answer immediately even if I do not understand.","I should agree to everything."],0,"Taking time, asking for a repeat, or responding in writing are useful options. Quick replies are not the only good replies.")]
    return [choice("In a practice job conversation, you are asked about a strength. Which answer gives useful evidence?",["I keep supplies organised. Last week I sorted and labelled our shared tools.","I am perfect at every task.","I cannot name any examples because only paid work counts."],0,"An example from home, volunteering, or school can show a skill. It does not have to come from paid work.","calculate"),choice("You do not understand a question in a job conversation. What could you do?",["Ask them to repeat it, explain it, or give you a moment.","Invent an answer to a different question.","Assume the conversation is over."],0,"Clarifying the question supports an accurate answer. A different processing pace is not a lack of ability.","apply"),choice("What is the purpose of practising a job conversation?",["To communicate your skills and ask about the work in a way that works for you.","To copy one exact personality and body language.","To hide every support need at all costs."],0,"There are many effective communication styles. This practice focuses on meaning, examples, and useful questions.")]

EXTRA += [
 ("writing",1,"Name an action and a detail","A useful message gives the reader something clear to understand or do. Start with a short sentence. Name the action and the important detail.","Write messages people can use.","Please bring my blue folder.",["Action: bring.","Thing: my folder.","Helpful detail: the blue one."],"Read it as the other person","You know what you mean, but the reader cannot see your thoughts. Reread for missing words, times, or places. You can listen to the message as a check.","Meet me later.",["Missing: a time and place.","Add the details: Meet me at the library at 3.","Now the reader can act without guessing."],"message",writing_questions),
 ("writing",6,"Ask for the missing piece","A specific question names what you already understand and what you still need. You do not need fancy words or a long explanation.","Get useful answers in class, at work, or when organising a task.","I have the boxes. Which shelf should I use?",["Known: the boxes are ready.","Missing: the correct shelf.","Ask one clear question about the missing detail."],"Make a request easy to follow","Break several questions into separate lines. If written steps help you, ask for them directly. You can describe a need without sharing a diagnosis.","Could you write down the steps?",["Name the support: a written list.","Explain its use if helpful: so I can check each step.","Confirm: I will sort first, then label. Is that right?"],"message",writing_questions),
 ("writing",10,"Give a work message a clear purpose","A work message usually needs a useful subject, a short explanation, and a clear question or next step. Keep the tone respectful and the facts accurate.","Write to a supervisor, coworker, or organiser with confidence.","Subject: Question about Friday's stock check",["State the context: I have Friday's list.","Ask the question: Which section should I check first?", "Close simply: Thanks, Jo."],"Revise before sending","Check the recipient and the important details. Read the message from the reader's point of view. Short does not mean rude; clear wording can be respectful.","I need more information.",["Name the missing information.","Revise: What time should the stock check be finished?", "Check that the person receiving it can answer."],"message",writing_questions),
 ("social",3,"Check before you guess","Instructions sometimes leave out details. Ask about the missing part, or restate the steps to check your understanding. This is a useful work skill.","Follow tasks accurately and avoid preventable mistakes.","Put those boxes over there.",["Notice the unclear detail: where?", "Ask: Which shelf do you mean?", "Check: This shelf, with the labels facing out. Is that right?"],"Ask for an example","People learn in different ways. You can ask to see one example, have the steps written down, or hear the instruction again.","I understand the goal but not the first step.",["Say what you know: I need to sort these.", "Name the gap: I am not sure which category to use.", "Ask: Could you show me one example?"],"conversation",social_questions),
 ("social",6,"Describe the support that helps","You can ask for a useful change: written instructions, a demonstration, a quieter explanation, or time to think. You do not have to force eye contact to show you understand.","Communicate how you can do your best work.","It is hard to hear the steps in this room.",["Name the problem without blaming yourself.","Offer an option: Could you write the steps or explain them somewhere quieter?", "Check what can be arranged before starting."],"Give yourself processing time","A pause is allowed. A clear response matters more than a fast one. You can ask for a repeat, a simpler explanation, or time to respond.","A question comes too quickly.",["Say: Give me a moment to think, please.", "If needed: Could you ask that another way?", "Answer when you understand what is being asked."],"conversation",social_questions),
 ("social",10,"Use a real example","In a job conversation, describe a skill and give an example. School, everyday tasks, volunteering, and hobbies can all provide examples. There is no required personality to copy.","Talk about what you can do and learn about a job.","Tell me about a strength.",["Name the skill: I keep things organised.", "Give an example: I labelled and sorted our shared tools.", "Say the result: People could find what they needed."],"Ask questions too","A job conversation also helps you learn about the work. Ask about tasks, training, schedules, and useful supports. It is okay to ask someone to explain a question.","What would my first week involve?",["Ask about the actual tasks.", "Ask how training is given.", "If helpful, ask whether written steps or demonstrations are available."],"conversation",social_questions),
]

def money_questions(kind,i):
    if kind=='cash':
        dollars,quarters=2+i%4,1+i%3
        total=dollars+quarters*.25
        quarter_word="quarter" if quarters==1 else "quarters"
        return [number(f"You have {dollars} one-dollar coins and {quarters} {quarter_word}. What is the total in dollars?",total,f"Each quarter is 0.25 dollars. Total: ${dollars}+{quarters}(0.25)={total:.2f}$.",hint="Group coins by value, then add the groups."),number(f"A purchase costs {total:.2f} dollars. You pay 10 dollars. How much change?",10-total,f"$10.00-{total:.2f}={10-total:.2f}$ dollars. Add the cost and change to check.","apply"),choice("What is a useful way to check change?",["Add the purchase cost and the change; the total should equal the amount paid.","Count only the number of coins.","Assume more coins always mean more money."],0,"Coin values matter, not only the count. Addition reverses the subtraction used to calculate change.")]
    if kind=='prices':
        a,b=2+i,3+i
        return [number(f"A pack of {a} identical items costs {a*2} dollars. What is the unit price?",2,f"${a*2}\\div{a}=2$ dollars per item.",hint="Divide the total price by the number of equal items."),number(f"You need {b} items at 2 dollars each. What is the cost?",b*2,f"${b}\\times2={b*2}$ dollars.","apply"),choice(f"Pack A: {a} items for {a*2} dollars. Pack B: {a} items for {a*3} dollars. Same items. Which has the lower unit price?",["Pack A","Pack B","They are equal"],0,"For equal quantities, the lower total has the lower unit price. More generally, divide each price by its quantity.")]
    if kind=='pay':
        hours,rate=3+i%6,12+i
        gross,deductions=rate*hours,10+i
        return [
            number(f"A practice job pays {rate} dollars per hour. What is gross pay for {hours} hours?",gross,f"Gross pay before deductions: ${rate}\\times{hours}={gross}$ dollars.",hint="Hourly rate times hours gives pay before deductions."),
            number(f"A shift runs from 9:00 to {9+hours}:30 with no unpaid break. How many hours is that?",hours+.5,f"There are {hours} full hours and half an hour. Total: ${hours}+0.5={hours+.5}$ hours.",hint="30 minutes is half an hour, written as 0.5 hours."),
            number(f"A fictional statement shows {gross} dollars gross pay and {deductions} dollars in total deductions. What is net pay in dollars?",gross-deductions,f"Net pay: ${gross}-{deductions}={gross-deductions}$ dollars. Use the supplied deductions; these are not a tax estimate.","apply",hint="Subtract the listed deductions from gross pay."),
            choice("Why might a pay deposit be less than gross pay?",["Deductions can reduce the amount paid out.","An hour always has 100 minutes.","Gross pay already means the deposit after deductions."],0,"Gross means before deductions; net means after. Use the actual listed amounts, not an assumed deduction.")]
    return life_questions(i)

MONEY = [
 ('cash',3,'Count cash & check change',('Group money by value','A coin count is not the same as a money total. Group coins with the same value. Count dollars and cents, then combine them. One dollar is 100 cents.','Handle everyday cash and check a payment.','2 dollars and 3 quarters',["Three quarters: $3\\times25=75$ cents.","Two dollars: 200 cents.","Total: $200+75=275$ cents, or 2.75 dollars."],'Check a payment in both directions','Change is the amount paid minus the cost. Check by adding the cost and change back together. These practice examples use dollar amounts, with no taxes or cash-rounding rules added.','Pay 10 dollars for a 2.75-dollar item',["Subtract: $10.00-2.75=7.25$.","Check: $2.75+7.25=10.00$.","Count the change by value, not just the number of coins."],'budget')),
 ('prices',5,'Compare unit prices',('Compare the same amount','A bigger package is not automatically better value. Divide the price by the quantity to compare the cost for one equal unit.','Compare prices using numbers instead of packaging.','6 identical items cost 12 dollars',["Price per item: $12/6=2$ dollars.","Another pack: 5 identical items for 15 dollars, or $15/5=3$ each.","The first pack costs less per item."],'Match the purchase to the need','Unit price tells you about cost per unit. You still need to check quality, how much you need, and whether you can use the whole pack.','You need 3 items at 2 dollars each',["Multiply quantity by price per item.","$3\\times2=6$ dollars.","Check the total against the amount available."],'budget')),
 ('budget',7,'Build a realistic budget',('Give each amount a job','A budget is a plan for limited resources. Start with what is actually available. Include essentials and amounts to set aside before optional choices. These are invented practice numbers.','Practise a plan that fits the available resources.','80 available, 45 for essentials, 10 set aside',["Start with 80.","$80-45-10=25$.","There are 25 left for other choices."],'Update the plan without blame','Unexpected costs happen. A changed plan is not a judgement of your worth. Recalculate using the new information, then choose a realistic next step.','An extra cost of 8 appears',["Previous amount left: 25.","Update: $25-8=17$.","Compare optional choices with the new limit of 17."],'budget')),
 ('pay',8,'Time, hours & pay',('Multiply hours by an hourly rate','An hourly rate is money earned for each hour. Multiply the rate by the hours worked to find gross pay before deductions. An hour contains 60 minutes.','Read a simple work schedule and understand a pay calculation.','4 hours at 15 dollars per hour',["Identify units: dollars per hour and hours.","Multiply: $15\\times4=60$.","Gross pay is 60 dollars before deductions."],'Separate elapsed time and take-home pay','Find the elapsed hours before calculating pay. Net pay is the amount after deductions. This starter uses simple shifts with no unpaid breaks; real payslips may have more details.','Work from 9:00 to 13:00',["13:00 means 1 pm.","Elapsed time: $13-9=4$ hours.","At 15 dollars per hour, gross pay is $4\\times15=60$."],'timeline')),
]

def build():
    units=[]; bank={}
    for subject in SUBJECTS:
        for g,title in enumerate(TOPICS[subject["id"]],1):
            units.append(dict(id=f'{subject["id"]}-{g}',subject=subject["id"],grade=g,title=title,ready=False))
    def add(subject,g,parts,questions,unit_id=None):
        unit=next(u for u in units if u['id']==(unit_id or f'{subject}-{g}'))
        t1,body1,why,example1,steps1,t2,body2,example2,steps2,visual=parts
        unit.update(ready=True,minutes=12,goal=t1,why=why,visual=visual,lessons=[dict(title=t1,body=body1,example=example1,steps=steps1),dict(title=t2,body=body2,example=example2,steps=steps2)],review=[body1,body2],reflection="Explain one step in your own words. What made it work?",practice=[])
        if unit['id']=='math-1':
            unit['mission']=ORDER_MISSION
            unit['goal']='Get the right number of drink cartons in the bag.'
            unit['reflection']='The order needs 7 drink cartons. You packed 4. How do you know how many more to add?'
        if unit['id']=='reading-1':
            unit['mission']=READING_MISSION
            unit['goal']='Make a plan you can follow.'
            unit['reflection']='Read: Meet Jo at the library at 5 pm. Bring a form. Write the plan in your own words. Keep the place, time, and thing to bring.'
        private=[]
        for i in range(12):
            for j,q in enumerate(questions(g,i)):
                version=2 if unit['id'] in ('math-1','reading-1') else 1
                q['id']=f'{unit["id"]}-v{version}-{i}-{j}'
                (unit['practice'] if i<3 else private).append(q)
        bank[unit['id']]=private
    for g,parts in enumerate(MATH,1): add('math',g,parts,math_questions)
    for subject,g,*rest in EXTRA:
        add(subject,g,rest[:-1],rest[-1])
    for kind,g,title,parts in MONEY:
        unit_id=f'math-{kind}'
        units.append(dict(id=unit_id,subject='math',grade=g,title=title,ready=False,practical=True))
        add('math',g,parts,lambda g,i,k=kind:money_questions(k,i),unit_id)
    # Extra transfer questions give the reading and communication checks several
    # distinct situations, rather than treating shuffled duplicate prompts as variety.
    extra={
      'reading-4': [
        ('A passage describes planting seeds, watering them, and seeing shoots grow. Which title fits?', ['Growing a plant','Fixing a bicycle','A history of cars'],0,'The title should connect the main details.'),
        ('Read: "The bus was delayed, so Jo arrived late." Why was Jo late?', ['The bus was delayed.','Jo forgot the date.','The bus arrived early.'],0,'The word so connects the cause with the result.'),
        ('Which summary adds a claim that was not given: "Lee practised a song each day"?', ['Lee is the best musician in the city.','Lee practised regularly.','Lee worked on a song.'],0,'Daily practice does not establish who is the best musician.'),
        ('A passage lists several ways to save water. What is probably its main topic?', ['Using less water','Choosing a television','The shape of a mountain'],0,'Look for the idea shared by the important details.'),
        ('Read: "Ari packed a lunch because the trip would take all day." Which detail gives a reason?', ['The trip would take all day.','Ari is a name.','A lunch was packed.'],0,'Because introduces the reason for the action.'),
        ('What should a short summary preserve?', ['The main meaning and important connections.','Every small word in the original.','Any opinion that sounds exciting.'],0,'A summary shortens the text without changing its meaning.')],
      'reading-8': [
        ('Which statement is a checkable observation?', ['18 people attended the meeting.','It was the best meeting ever.','Everyone must love meetings.'],0,'An attendance count can be checked against a record.'),
        ('An old article is shared as if it describes today. What should you inspect?', ['The publication date and event date.','Only the colour of the page.','Only how often it was shared.'],0,'Dates help establish whether the information matches the current claim.'),
        ('A large follower count means a claim is…', ['Popular, but still in need of evidence.','Automatically accurate.','Always false.'],0,'Popularity does not establish accuracy either way.'),
        ('A claim cites a study. What would give you better evidence than its headline?', ['The original study and what it measured.','A stranger repeating the headline.','The largest photograph.'],0,'The original source helps you inspect the method and limits.'),
        ("One person's experience differs from a survey result. What follows?", ['Individual experiences and group patterns can differ.','All survey participants lied.','The individual experience is impossible.'],0,'A group pattern is not a promise about every individual.'),
        ('Which wording acknowledges limited evidence?', ['This small sample suggests a pattern.','This proves the same result for everyone forever.','Evidence is unnecessary.'],0,'Careful wording matches the scope of the information.')],
      'reading-12': [
        ('Two sources use different definitions of "success". What should a comparison identify?', ['What each source means by success.','Which source has the longer name.','Only which one agrees with you.'],0,'Different definitions can explain an apparent disagreement.'),
        ('One report measures short-term cost; another measures long-term benefit. What should you do?', ['Compare the timeframes before drawing a conclusion.','Assume the measures are identical.','Discard all cost information.'],0,'The timeframe changes what each result can support.'),
        ('What makes a counterargument useful?', ['It tests a position against a relevant alternative or limitation.','It insults the other writer.','It changes the topic entirely.'],0,'Engage with reasons and evidence rather than the person.'),
        ('A recommendation depends on a trial succeeding. Which sentence makes that condition clear?', ['Expand the programme if the trial shows improved access within the budget.','Expand it because conditions never matter.','Every programme always succeeds.'],0,'A conditional recommendation names the evidence required for the next step.'),
        ('Two sources report similar results using independent data. What can that add?', ['Corroboration, while remaining open to limitations.','A guarantee that no errors exist.','Proof of every possible future result.'],0,'Independent agreement can strengthen support without removing all uncertainty.'),
        ('A fair comparison should represent an opposing view…', ['Accurately, before evaluating its reasons.','As weakly as possible.','Only through an insult.'],0,'You cannot evaluate a view fairly if you change what it claims.')],
      'writing-1': [
        ('Which message names a place?', ['I am at the library.','I am somewhere.','Over there maybe.'],0,'Library identifies the place.'),
        ('Add the missing action: "Please ___ the door."', ['close','blue','yesterday'],0,'Close names an action that fits the sentence.'),
        ('Why reread a message before sending?', ['To check that another person can understand it.','To make it as long as possible.','To remove every useful detail.'],0,'A message succeeds when its meaning reaches the reader.'),
        ('Which message gives a clear time?', ['Please arrive at 2 pm.','Please arrive eventually.','Please arrive at a thing.'],0,'2 pm is a specific time.'),
        ('Which edit makes "Bring it" clearer?', ['Please bring the blue folder.','Please bring something somehow.','It.'],0,'Name the object instead of relying on an unclear pronoun.'),
        ('Your first draft needs a change. What does that mean?', ['You can revise it to make it clearer.','You are not allowed to write.','Every word must be perfect on the first try.'],0,'Drafting and revising are normal parts of writing.')],
      'writing-6': [
        ('Which question asks about priority?', ['Which task should I finish first?','Where is the blue shelf?','How many boxes are there?'],0,'Priority is the order of importance or the task to start with.'),
        ('You know where the task is but not when it is due. What should you ask?', ['What time should it be finished?','Where is it again?','What colour do you like?'],0,'Ask about the missing information rather than repeating what you know.'),
        ('Why put multiple questions on separate lines?', ['The reader can see and answer each question.','It guarantees the answer you want.','It hides the number of questions.'],0,'Good structure makes the message easier to use.'),
        ('Which question asks about quantity?', ['How many labels do we need?','When do we start?','Which room do we use?'],0,'How many asks for a number.'),
        ('Which request explains a useful support?', ['Could you send a written list so I can check each step?','Read my mind.','I must never ask anything.'],0,'Name the support and, if helpful, how you will use it.'),
        ('A reader asks you to clarify a sentence. What is a useful response?', ['Restate it more specifically or give an example.','Assume they are being difficult.','Repeat it louder without changing anything.'],0,'Clarification is a shared effort to make meaning clear.')],
      'writing-10': [
        ('Which opening gives useful context?', ['I am checking the delivery scheduled for Tuesday.','Things are things.','Read this immediately forever.'],0,'The opening names what the message concerns.'),
        ('You cannot meet an agreed deadline. Which message helps planning?', ['I can finish by Thursday. Is that workable, or should we change the priority?','Say nothing until next month.','Promise a time you know is impossible.'],0,'Clear, realistic information lets the other person plan with you.'),
        ('Why check the recipient before sending?', ['To avoid sending information to the wrong person.','To make the message longer.','To avoid asking any questions.'],0,'The intended reader is part of a useful message.'),
        ('Which closing includes a clear next step?', ['Please confirm which section I should do first.','Anyway, everything exists.','You should know what I mean.'],0,'Tell the reader what response or action is needed.'),
        ('Which edit makes a work message more precise?', ['Replace "later" with "by 3 pm today" when that is the intended time.','Replace every fact with a vague word.','Use all capitals for the entire message.'],0,'Specific details reduce unnecessary guessing.'),
        ('Does a professional message need complicated vocabulary?', ['No. Clear, accurate, respectful wording works.','Yes, even if the writer does not understand it.','Only long messages are respectful.'],0,'The reader needs meaning, not impressive-looking complexity.')],
      'science-5': [
        ('You test two paper towel brands. What should be kept equal?', ['The amount of water and testing method.','Only the labels while changing everything else.','Nothing.'],0,'A fair comparison keeps relevant conditions similar.'),
        ('A ruler uses centimetres. How should you record a measured length of 8?', ['8 cm','8 with no unit anywhere','8 hours'],0,'A number and its unit make the measurement interpretable.'),
        ('Why record an unexpected result?', ['It is evidence, even if it differs from your prediction.','Only expected results count.','It must be hidden.'],0,'A fair investigation does not select only the results it likes.'),
        ('Which is a prediction rather than an observation?', ['I think more light will lead to more growth.','This plant grew 4 cm during the test.','The recorded temperature was 20 degrees.'],0,'A prediction describes what you expect before observing the result.'),
        ('One measurement looks unusual. What is useful?', ['Check the method and repeat the measurement where possible.','Change it to the number you wanted.','Delete every other measurement.'],0,'Checking a possible measurement error is different from forcing a preferred result.'),
        ('What does a fair test help you judge?', ['Whether the factor being changed may explain the observed difference.','Whether you are a good person.','Whether one test proves every future result.'],0,'The design helps connect a tested factor with outcomes, within its limits.')],
      'social-3': [
        ('Which phrase asks someone to repeat an instruction?', ['Could you say that step again, please?','I will pretend I heard it.','Every task is finished.'],0,'You can ask for a repeat when information is missing.'),
        ('You are told to label boxes but do not know which labels. What could you ask?', ['Which labels should I use?','Why are all boxes bad?','Should I throw out the labels?'],0,'Ask about the exact part needed to continue.'),
        ('Does asking a useful question mean you cannot learn a task?', ['No. It can help you learn it accurately.','Yes. You must always guess.','Only fast guesses count.'],0,'Clarifying a step is part of learning and working accurately.'),
        ('Which phrase checks the order of a task?', ['First sort, then label. Is that the right order?','I will do all steps at random.','I will change the goal.'],0,'Restating the sequence makes misunderstandings easier to spot.'),
        ('Someone shows you one example. What could you do next?', ['Try a similar example and check the result.','Assume every future task is identical.','Discard the example without looking.'],0,'Using an example helps you apply the method rather than only watch it.'),
        ('Which matters most when checking an instruction?', ['Whether you understand the meaning and next action.','Whether you make continuous eye contact.','Whether you copy another person’s posture.'],0,'Understanding can be shown in different ways. Eye contact is not a required proof.')],
      'social-6': [
        ('Which request names a practical adjustment?', ['Could I use a written checklist for this task?','Everyone must know my thoughts.','I am never allowed to ask for anything.'],0,'A checklist is a specific support someone can discuss with you.'),
        ('You missed part of a spoken instruction. What could you do?', ['Ask for the missed step again or in writing.','Agree while planning to guess.','Assume it can never be explained.'],0,'Different formats can help you receive the information.'),
        ('Is one communication style right for everyone?', ['No. People can communicate clearly in different ways.','Yes. Everyone must speak at the same speed.','Yes. Everyone must use the same body language.'],0,'Focus on shared meaning, not forcing identical behaviour.'),
        ('Which phrase asks for processing time?', ['I need a moment before I answer.','I have already understood everything.','I must say yes immediately.'],0,'Naming the need can make the pause understandable to another person.'),
        ('A requested support is unavailable. What could you ask next?', ['Is there another way to get the instructions clearly?','Assume no alternative can exist.','Pretend the original problem disappeared.'],0,'You can discuss alternatives without treating your need as a personal failure.'),
        ('What can a support request focus on?', ['The task and what helps you do it.','Proving you are exactly like everyone else.','Disclosing every private detail.'],0,'A useful request can be specific without including a diagnosis or family history.')],
      'social-10': [
        ('Which example could show reliability?', ['I arrived at the agreed time for our weekly volunteer task.','I claim I have never made a mistake.','I cannot use volunteer experience.'],0,'A concrete example supports a skill claim. Unpaid experiences can still be relevant.'),
        ('What could you ask to understand a new role?', ['What tasks would I do in a typical shift?','Can I avoid learning anything about it?','Should I guess every responsibility?'],0,'Ask about the actual work so you can judge what it involves.'),
        ('Must an interview answer use one exact script?', ['No. It should communicate a relevant, truthful example.','Yes. Every person must use identical words.','Yes. Only memorised wording shows ability.'],0,'Practice can help you organise your ideas without replacing your own voice.'),
        ('Which example could show problem solving?', ['I noticed labels were hard to find and arranged them by task.','I say I am perfect at everything.','I refuse to name any situation.'],0,'Describe a situation, your action, and the useful result.'),
        ('You want to know how training works. What could you ask?', ['Will someone demonstrate the task or provide written steps?','What is every employee’s personal history?','Why is learning unnecessary?'],0,'The question helps you understand what support and training the job provides.'),
        ('A question is unclear. Which choice supports an accurate answer?', ['Ask for clarification before answering.','Invent experience you do not have.','Say yes to a question you did not understand.'],0,'Clarification helps you respond honestly to the actual question.')],
    }
    for unit_id,questions in extra.items():
        for i,(prompt,options,answer,explanation) in enumerate(questions):
            q=choice(prompt,options,answer,explanation,('calculate','apply','reason')[i%3]);q['id']=f'{unit_id}-transfer-{i}'
            bank[unit_id].append(q)
            if i<3: next(u for u in units if u['id']==unit_id)['practice'].append(q)
    # Add a second distinct reasoning prompt for each mathematical method.
    reasons=[
      ('The order needs 8 drink cartons. You packed 5, then added 3. How can you check the bag?', ['Count all the drink cartons. There should be 8.','Count only the 3 you just added.','Add 8 more drink cartons.'],0,'$5+3=8$. Count the full bag and compare it with the order.'),
      ('Trading one ten for ten ones changes…', ['The grouping, but not the total value.','The total value by ten.','The number into a fraction.'],0,'Equivalent groups can represent the same value.'),
      ('What must be true for equal-group multiplication to fit a story?', ['Each group has the same size.','Every group is a different size.','There are no groups.'],0,'A single group size can be multiplied only when it is the same for each group.'),
      ('In a fraction model, why do the pieces need equal size?', ['Counting pieces must also compare equal shares.','Their colours must be identical.','The numerator must always be one.'],0,'A quarter is one of four equal parts, not just any one piece.'),
      ('Why align decimal places when subtracting money?', ['So units of equal value are subtracted together.','So every answer ends in zero.','So cents can be ignored.'],0,'Hundredths align with hundredths, tenths with tenths, and ones with ones.'),
      ('What does a unit rate describe?', ['An amount for one unit of another quantity.','Any two unrelated numbers.','A total without a quantity.'],0,'A unit rate makes comparisons on an equal basis.'),
      ('Before finding a percentage, what must you identify?', ['The whole amount the percentage refers to.','Only the colour of the label.','A random number to divide.'],0,'The same percent of different wholes gives different amounts.'),
      ('How do you check a proposed equation solution?', ['Substitute it into the original equation and compare both sides.','Look only at how short the answer is.','Change one side until it looks right.'],0,'A solution makes the original equality true.'),
      ('A line has a constant slope of 3. What happens when x increases by 2?', ['y increases by 6.','y always becomes 3.','y must decrease by 2.'],0,'Rate times input change gives output change: $3\\times2=6$.'),
      ('Why does doubling a square side quadruple area?', ['Both dimensions double.','Only one dimension doubles.','Area is the same as perimeter.'],0,'Two factors of two give a factor of four.'),
      ('What does the sine ratio compare?', ['Opposite side with hypotenuse, relative to a chosen angle.','The two longest words in the problem.','An angle with a number of hours.'],0,'Side names depend on the chosen angle; the hypotenuse stays opposite the right angle.'),
      ('Which quantity is a derivative describing?', ['A local rate of change.','The largest output ever reached.','The number of terms in every sum.'],0,'A derivative answers how quickly a quantity changes near a particular input.'),
    ]
    for g,args in enumerate(reasons,1):
        q=choice(*args);q['id']=f'math-{g}-reason-extra';bank[f'math-{g}'].append(q)
    for kind,g,title,parts in MONEY:
        q=choice(f'In the worked example ({parts[3]}), which step helps you solve the task?', [parts[4][0], 'A total can be correct even if you ignore every unit.', 'Always use the number of coins as the dollar value.'],0,parts[4][-1]);q['id']=f'math-{kind}-reason-extra';bank[f'math-{kind}'].append(q)
    for u in units:
        if u['id'] in ('math-5','math-cash'):u['visual']='money'
        if u['id']=='math-prices':u['visual']='prices'
        if u['id']=='math-7':u['visual']='percent'
    populate(units,bank)
    enrich(units)
    attach_workshops(units)
    subjects=[dict(s) for s in SUBJECTS]
    attach_digital(units,bank,subjects)
    attach_math_missions(units)
    attach_math_extension(units)
    attach_practical_missions(units)
    attach_science_missions(units)
    attach_life_services(units,bank)
    attach_life_money(units,bank)
    attach_life_work(units,bank)
    attach_life_transport(units,bank)
    attach_life_home(units,bank)
    attach_life_support(units,bank)
    attach_pc_course(units,bank)
    attach_typing_course(units,bank)
    attach_ai_course(units,bank)
    attach_project_course(units,bank)
    from distinct_questions import refine
    refine(units,bank)
    thin=hold_out_checks(units,bank)
    count=sum(u['ready'] for u in units)
    catalog=dict(version=3,name="Stepstone",description=f"A practical foundation library with {count} modules. This pilot is not a complete curriculum or a qualification.",subjects=subjects,units=units)
    (ROOT/'public').mkdir(parents=True,exist_ok=True)
    (ROOT/'public/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'content/checkpoints.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    from starting import build as build_starting
    build_starting()
    print(f"Built {sum(u['ready'] for u in units)} ready modules, {len(units)} mapped modules, {sum(map(len,bank.values()))} checkpoint questions.")
    if thin: print(f"{len(thin)} modules still reuse published practice in checks until more check cases are written: {', '.join(thin)}")

def hold_out_checks(units,bank):
    """Keep published questions out of each check bank when enough unseen cases remain.

    Anything in catalog.json is public, answers included. Returns the modules whose
    unseen cases cannot yet build a balanced six-question check; they keep their old bank.
    """
    import random,sys
    sys.path.insert(0,str(ROOT))
    from check_sampling import sample_check
    thin=[]
    for unit in units:
        if not unit['ready']:continue
        published=set()
        def walk(value):
            if isinstance(value,dict):
                if isinstance(value.get('prompt'),str):published.add((value.get('passage',''),value['prompt']))
                for item in value.values():walk(item)
            elif isinstance(value,list):
                for item in value:walk(item)
        walk(unit)
        unseen=[q for q in bank[unit['id']] if (q.get('passage',''),q['prompt']) not in published]
        if len(unseen)==len(bank[unit['id']]):continue
        try:
            for seed in range(200):sample_check(unseen,unit.get('checkSkills',('calculate','apply','reason')),random.Random(seed))
        except ValueError:
            thin.append(unit['id']);continue
        bank[unit['id']]=unseen
    return thin

if __name__=='__main__': build()
