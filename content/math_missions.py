"""Reviewed practical maths missions, attached after the foundation generator.

Keep unit IDs and stored attempts stable. Supported tasks are deliberately public;
only the existing six-question check awards mastery.
"""

def lesson(title, body, steps, why, trap):
    return dict(title=title,body=body,example=title,steps=steps,whyItWorks=why,watchFor=trap)

def task(ident, title, prompt, kind, hint, why, **data):
    return dict(id=ident,title=title,prompt=prompt,kind=kind,hint=hint,why=why,**data)

def spec(title, goal, why, objectives, lessons, labs, review, reflection, needs):
    return dict(title=title,goal=goal,why=why,lessons=lessons,review=review,reflection=reflection,
                mission=dict(kind='scenario',label='Everyday numbers',tagline=goal,objectives=objectives,
                 brief=[goal,'Try a changed situation, with help when you need it.','Explain your method, then try a six-question check.'],
                 startLabel='Start the job',artLabel='TRY / CHECK / EXPLAIN',labLabel='Try the task',backLabel='Back to the task',
                 practiceLabel='Try a fresh situation.',recapLabel='Tasks you worked out',labs=labs,needs=needs))

SPECS={
'math-2':spec('Count the stock','Count bundles and loose items without losing track.','Use groups of ten to count supplies, read bigger numbers, and take items from a pack.',
 ['Build a count','Open a bundle','Check the stock'],[
 lesson('Count bundles and loose labels','A closed bundle holds ten labels. Two bundles hold twenty labels. Four loose labels bring the count to twenty-four. The number of bundles is different from the number of labels. Canadian money uses the same idea: a 10-dollar note is worth ten dollars, and a loonie is worth one.',['Each bundle holds 10 labels. Two bundles hold $2\\times10=20$ labels.', 'Four loose labels add $4$ more labels.', 'Together, $20+4=24$ labels.'],'A bundle is one package, but it contains ten labels. Count the contents of the bundles, then include the loose labels. The Canadian money view shows the same grouping with two 10-dollar notes and four loonies.','Counting a bundle as one label loses nine of its labels from your total.'),
 lesson('Open a bundle; keep the labels','You have 34 labels. You need 8 loose labels. Open one bundle. You still have 34 labels, but now more are loose.',
 ['Start with 3 tens and 4 ones: $30+4=34$.','Open one ten: 2 tens and 14 ones. $20+14=34$.','Take 8 loose labels. $14-8=6$, so $20+6=26$ remain.'],
 'Opening a bundle does not add labels. It changes one ten into ten ones. This is the reason the written method lets you regroup before subtracting.',
 'Trade a ten for ten ones. Do not keep the old ten as well.')],[[
 task('stock-build','Build the shelf count','The order needs 24 labels. Build the shelf count using closed bundles of ten and fewer than ten loose labels.','stock','Use Add a ten twice, then Add a one four times.','$2\\times10+4=24$. You counted the labels inside the bundles too.',start={'tens':0,'ones':0},target={'tens':2,'ones':4}),
 task('stock-read','Read a different shelf','Count every label on this shelf. Include the labels inside the four closed bundles and the two loose labels.','number','Four tens are 40. Add the 2 loose labels.','$40+2=42$. The 4 has moved into the tens place.',answer=42,model={'type':'stock','tens':4,'ones':2})
 ],[
 task('stock-trade','Open one bundle','The shelf holds 34 labels, but only four are loose. Open one closed bundle so an order of eight loose labels can be filled.','stock','Choose Open one ten. Watch where those ten labels go.','$30+4=20+14=34$. The grouping changed; the count did not.',start={'tens':3,'ones':4},target={'tens':2,'ones':14},trade=True),
 task('stock-take','Fill the request','The shelf holds two closed bundles and fourteen loose labels. An order needs eight loose labels. How many labels will remain on the shelf?','number','Take 8 from the 14 loose labels. Then add the 20 in bundles.','$34-8=26$. Check: $26+8=34$.',answer=26,model={'type':'stock','tens':2,'ones':14})
 ]],['A ten holds 10 ones.','$34=30+4=20+14$. Opening a bundle keeps the total.','Check a subtraction by adding back what you took.'],
 'You have 34 labels and take 8. Explain how opening a bundle helps. You can draw bundles and loose labels.', ['math-1']),

'math-3':spec('Pack equal sets','Make equal packs and share a total fairly.','Use this for packing supplies, sharing food, or working out how many items to buy.',
 ['Make equal packs','Share the total','Check the packs'],[
 lesson('The same amount in each pack','Put 4 labels in each of 3 packs. Each pack has the same amount. You can count by fours instead of counting every label again.',
 ['One pack holds 4 labels.','Three packs hold $4+4+4=12$ labels.','Write $3\\times4=12$: packs times labels per pack.'],
 'Multiplication is a short way to count equal groups. An array is the same idea drawn in rows. Count the rows, then count how many are in each.',
 '$3\\times4$ is not $3+4$. The groups must be equal.'),
 lesson('Share every item','There are 18 labels to share between 3 packs. Give each pack the same number. Use all 18 labels.',
 ['Try 6 in each pack.','Check: $6+6+6=18$.','Write $18\\div3=6$. Total divided by packs gives labels per pack.'],
 'Multiplication checks division. If you know the packs and the amount in each, multiply to rebuild the total. More packs means fewer labels per pack when the total stays fixed.',
 'Count what is left over. A leftover item does not disappear.')],[[
 task('groups-build','Make the packs','Build 3 packs with 4 labels in each.','groups','Set Packs to 3 and In each pack to 4.','$3\\times4=12$. The rows show three equal groups.',start={'groups':1,'each':1},target={'groups':3,'each':4}),
 task('groups-count','Count a new order','There are 4 packs with 5 labels in each. How many labels in all?','number','Count $5+5+5+5$, or use $4\\times5$.','$4\\times5=20$. Four packs of five hold twenty labels.',answer=20,model={'type':'groups','groups':4,'each':5})
 ],[
 task('groups-share','Share 18 labels','There are 3 packs. Put the same number in each and use all 18 labels.','groups','Change In each pack. Try 6 in each of the 3 packs.','$18\\div3=6$. Check: $3\\times6=18$.',start={'groups':3,'each':1},target={'groups':3,'each':6},fixed=['groups'],total=18),
 task('groups-change','The number of packs changes','Share the same 18 labels between 6 packs. How many labels go in each?','number','Find the number that makes $6\\times\\square=18$.','$18\\div6=3$. Twice as many packs means half as many labels in each.',answer=3)
 ]],['Count equal packs with multiplication.','Share a total with division.','Multiply back to check: packs times amount in each equals the total.'],
 'Compare sharing 18 labels between 3 packs and 6 packs. Explain what changes and what stays the same.', ['math-1']),

'math-4':spec('Split a fair share','Use equal parts to work out a share.','Use fractions for portions, time, or splitting a set of supplies.',
 ['See equal parts','Find a share','Check the whole'],[
 lesson('Name the selected parts','Split one whole into 4 equal parts. Take 3 parts. That is three quarters. The bottom number counts all the equal parts. The top counts the parts you take.',
 ['The whole has 4 equal parts.','You take 3 of them.','Write $\\frac{3}{4}$. Say: three out of four equal parts.'],
 'Equal size matters. Three small scraps are not automatically three quarters. Always name the whole before naming its fraction.',
 'Half of a small pizza and half of a large pizza are different amounts.'),
 lesson('Find a share of a set','There are 20 labels. You need three quarters of them. Split 20 into 4 equal groups, then take 3 groups.',
 ['Find one quarter: $20\\div4=5$.','Take three groups of five: $3\\times5=15$.','Check: 15 is more than half of 20, but less than all 20.'],
 'The bottom number tells you how many equal groups to make. The top tells you how many groups to take. Splitting first makes the fraction easier to picture.',
 'Do not divide by the top number. The bottom number sets the size of one part.')],[[
 task('fraction-select','Show three quarters','Select 3 of the 4 equal pieces. Tap a piece again to undo it.','fraction','Tap three pieces. Leave one unselected.','$\\frac{3}{4}$ means 3 of 4 equal parts.',parts=4,take=3),
 task('fraction-name','Same share, smaller pieces','This whole has 8 equal pieces. 4 are selected. What fraction is selected?','number','Write 4/8. You can also write 1/2.','$\\frac{4}{8}=\\frac12$. Both name half of this same whole.',answer=.5,model={'type':'fraction','parts':8,'take':4})
 ],[
 task('fraction-set','Find three quarters of 20','The 20 labels are in 4 equal rows. Select 3 rows.','fraction','Each row holds 5. Select three rows of five.','$20\\div4=5$, then $5\\times3=15$ labels.',parts=4,take=3,per=5),
 task('fraction-new','Find a different share','You need one third of 18 labels. How many labels should you take?','number','Split 18 into 3 equal groups. Take one group.','$18\\div3=6$. One third of 18 is 6.',answer=6,model={'type':'groups','groups':3,'each':6})
 ]],['Name the whole. Split it into equal parts.','Bottom: how many equal parts. Top: how many you take.','For a fraction of a set, divide into groups first, then take the groups you need.'],
 'Explain how to find three quarters of 20. Show what the 4 and the 3 each tell you to do.', ['math-3']),

'math-5':spec('Read prices and change','Keep dollars and cents straight.','Work out a simple total and check the change using made-up prices.',
 ['Build a price','Check the change','Read a new receipt'],[
 lesson('One dollar is 100 cents','A price of 1.25 dollars means 1 dollar and 25 cents. For three items at that price, count each price three times.',
 ['Change 1.25 dollars to 125 cents.','Three items cost $125\\times3=375$ cents.','Change back: $375\\div100=3.75$ dollars.'],
 'Cents let you work with whole numbers. Keep the unit with the number: 25 cents is a quarter of a dollar, not 25 dollars. Label your total with cents or dollars.',
 '3.50 dollars and 3.05 dollars are different. The zero holds a place.'),
 lesson('Add the change back to check','The final total is 3.75 dollars. You hand over 10 dollars. Your change is the part of that payment left after the cost.',
 ['Estimate: about $10-4=6$ dollars back.','Subtract: $10.00-3.75=6.25$.','Check: $3.75+6.25=10.00$.'],
 'Cost plus change must equal the payment. This checks both the amount and the decimal places. Write 10.00 to keep dollars under dollars and cents under cents.',
 'These examples use final totals. No extra tax, fees or rounding is needed.')],[[
 task('money-build','Build 1.25 dollars','Use dollar and quarter buttons to make 1.25 dollars.','money','Add 1 dollar, then 25 cents.','$100+25=125$ cents. That is 1.25 dollars.',start={'cents':0},target={'cents':125}),
 task('money-total','Count a purchase','You buy 3 items at 1.25 dollars each. What is the total in dollars?','number','Each item is 125 cents. Find $125\\times3$, then divide by 100.','$125\\times3=375$ cents, or 3.75 dollars.',answer=3.75,model={'type':'receipt','quantity':3,'price':1.25})
 ],[
 task('money-change','Give the change','Final total: 3.75 dollars. Payment: 10 dollars. Build the change.','money','Count up from 3.75 to 4: 25 cents. Then from 4 to 10: 6 dollars.','$3.75+6.25=10.00$. Give back 6.25 dollars.',start={'cents':0},target={'cents':625}),
 task('money-place','Catch a decimal mistake','A receipt says 3.50 dollars. Which amount is the same?','choice','The 50 means 50 cents, not 5 cents.','3.50 dollars means 3 dollars and 50 cents. A trailing zero does not change 3.5 dollars.',options=['3 dollars and 5 cents','3 dollars and 50 cents','35 dollars'],answer=1)
 ]],['100 cents make one dollar.','Use cents for whole-number calculations, then change back to dollars.','Cost plus change should equal the payment.'],
 'For a final total of 3.75 dollars paid with 10 dollars, explain how you find and check the change.', ['math-2','math-3'])
}

def attach(units):
    for u in units:
        if u['id'] in SPECS:
            u.update(SPECS[u['id']])
            # Replaced by the mission model, so do not keep a second workshop.
            u['workshop']=dict(kind='scenario')
            for i,q in enumerate(u['practice']):
                q['lesson']=2 if q['skill']=='apply' else 1 if q['skill']=='calculate' else 1+i%2
    for u in units:
        if u['id'] in SPECS:
            u['mission']['preparation']=[dict(id=ident,title=next(v['title'] for v in units if v['id']==ident)) for ident in u['mission']['needs']]
