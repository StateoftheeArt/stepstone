"""Screen-based investigations; models are examples, not real-world instructions."""
from math_extension import num,pick
from practical_missions import install,evidence_task

def ev(ident,title,prompt,lines,answer,why):
    return evidence_task(ident,dict(prompt=prompt,lines=lines,answer=answer,why=why),title)
def model(n,t):return dict(t,science=n)

MISSIONS={
9:dict(title='Read data without overclaiming',goal='Keep units, variation and sample limits visible.',objectives=['Read the sample','Investigate a surprise','Support a careful claim'],needs=['science-5','math-7'],bodies=[
 'Data are recorded observations. Check the units, who or what was measured, and how many cases there were. A result from one chosen group may not describe everyone.',
 'An unusual reading deserves a check, not silent deletion. Keep the original, inspect the method and record any repeat. Averages can hide how much readings differ.'],labs=[[
 ev('data-sample','Keep the sample in view','A survey of 12 friends finds 9 prefer later opening. Which statements are justified?',['9 of these 12 friends preferred later opening.','This small chosen group may not represent all visitors.','Exactly 75% of every town prefers later opening.'],[0,1],'The fraction describes this sample. It does not establish the result for a whole town.')],[
 ev('data-outlier','Investigate an unusual reading','Measurements were 10, 11, 10 and 35 cm. What belongs in a useful record?',['All four readings, with the unusual one flagged.','A note checking the method and recording any repeats.','Only the first three, with 35 quietly deleted.'],[0,1],'Preserve the evidence while checking whether a method, device or real difference explains the reading.')]],
 reflection='Summarise the survey without claiming it represents everyone. Then explain how you would investigate the unusual measurement.'),
10:dict(title='Account for the atoms',goal='Use a symbolic reaction to count matter before and after.',objectives=['Count reacting particles','Check conservation','Explain what changes'],needs=['science-6','math-3'],bodies=[
 'In a chemical reaction, atoms are rearranged into different substances. A balanced model has the same number of each kind of atom before and after. A and B here are pretend atom labels.',
 'Coefficients count whole molecules. Subscripts describe atoms within one molecule. Balance a count by changing coefficients, not the substance. When gas escapes, include it in the total: atoms have moved, not disappeared.'],labs=[[
 model(10,num('reaction-products','Count the products','In $A_2+B_2\\longrightarrow2AB$, three reacting pairs produce how many AB molecules?',6,'Each pair produces two AB molecules.','$3\\times2=6$ AB molecules. This is a symbolic screen model, not chemicals to mix.'))],[
 model(10,pick('reaction-count','Check the atoms','For $2A_2+2B_2\\longrightarrow4AB$, how many A atoms are on each side?',['2 on each side.','4 on each side.','8 on one side and 4 on the other.'],1,'Each $A_2$ has two A atoms; each AB has one.','Left: $2\\times2=4$. Right: $4\\times1=4$. The atoms are conserved.'))]],
 reflection='Draw or count atoms for two reacting pairs. Explain the difference between the 2 before a formula and the 2 inside $A_2$.'),
11:dict(title='Read current and wave patterns',goal='Use an ideal circuit rule and distinguish wave height from frequency.',objectives=['Predict the current','Read the cycles','Explain the difference'],needs=['math-6','math-9','science-7'],bodies=[
 'For an ideal resistor, current equals voltage divided by resistance: $I=V/R$. With voltage fixed, more resistance means less current. This is a screen model, not a wiring task.',
 'Frequency counts complete cycles per second. Amplitude measures the height from the middle to a peak. A wave can get taller without making more cycles.'],labs=[[
 model(11,num('circuit-current','Predict an ideal current','There are 6 volts across an ideal 3-ohm resistor. What is current in amperes?',2,'Use $I=V/R$.','$I=6/3=2\\ \\mathrm{A}$.'))],[
 model(11,num('wave-frequency','Count complete cycles','A wave makes 5 complete cycles in one second. What is its frequency in hertz?',5,'One hertz means one cycle per second.','$f=5\\ \\mathrm{Hz}$. Making peaks taller changes amplitude, not this cycle count.'))]],
 reflection='Show the current calculation and explain which quantity is held fixed. Then describe frequency and amplitude without treating them as the same thing.'),
12:dict(title='Know when a model stops fitting',goal='Use a model within its assumptions and check a physical limit.',objectives=['Calculate a prediction','Apply the capacity','Name an assumption'],needs=['science-9','math-9'],bodies=[
 'A model keeps some features and leaves others out. It can help you predict, but only under its assumptions. Compare its answer with what the situation could actually allow.',
 'An empty tank takes in water at a constant rate, but holds at most 20 litres. After it fills, extra inflow overflows. Water that entered and water still inside are different amounts.'],labs=[[
 model(12,num('tank-first','Predict before it fills','An empty tank takes in 3 litres per minute for 4 minutes, with no outflow. How many litres are inside?',12,'Rate times time gives the volume before the tank is full.','$3\\times4=12\\ \\mathrm{L}$, below the 20 L capacity.'))],[
 model(12,num('tank-capacity','The simple rule meets a limit','At 3 litres per minute, how much remains inside the 20-litre tank after 9 minutes?',20,'27 L entered, but only 20 L fit.','$\\min(20,3\\times9)=20\\ \\mathrm{L}$. The extra 7 L overflowed.'))]],
 reflection='Compare the 4-minute and 9-minute predictions. State the capacity and two assumptions. Explain why the amount that entered differs from the amount inside.'),
5:dict(title='Make a fair comparison',goal='Change one factor and keep a record someone can check.',objectives=['Choose a fair test','Keep the full record','Explain the limit'],needs=['science-1'],bodies=[
 'To test an idea, change the factor you are interested in. Keep other important conditions alike. Decide what to measure before seeing the result.',
 'Record the method and all results, including surprises. Repeating a fair test helps show whether a pattern holds. One result does not prove what always happens.'],labs=[[
 ev('test-controls','Compare paper towels','Which choices make a comparison of two towel brands fair?',['Use equal sheet sizes and equal amounts of water.','Use the same contact time for both brands.','Use two layers for one brand and one for the other.'],[0,1],'If size, water, time or layers differ, the brand is not the only possible cause.')],[
 ev('test-record','Keep a usable record','Which records help someone check a plant-light test?',['Plant type, starting size, water and light conditions.','All growth measurements, including an unexpected result.','Only the picture that looks best.'],[0,1],'The method and complete results help someone assess the comparison. Choosing only a good-looking result hides evidence.')]],
 reflection='Plan a harmless paper-towel comparison on paper. Name what changes, what stays alike, what you measure and one limit. You do not need to carry it out.'),
6:dict(title='Track matter through a change',goal='Explain a state change without making particles disappear.',objectives=['Compare particle models','Check what stayed the same','Distinguish changes'],needs=['science-2'],bodies=[
 'A particle model uses dots to stand for tiny parts of matter. In a solid they stay near fixed positions; in a liquid they move past one another; in a gas they spread out.',
 'Melting changes the state, not which substance it is. A chemical change forms different substances. A colour or temperature change is a clue to investigate, not proof by itself.'],labs=[[
 model(6,pick('matter-liquid','Read the particle model','Which description fits a liquid?',['Particles stay close but can move past one another.','There are no particles.','Every particle is fixed in one position forever.'],0,'Think about pouring a liquid into a different-shaped container.','The liquid changes shape while its particles remain close. The dots are a simplified model.'))],[
 model(6,pick('matter-melt','Explain melting','Ice melts in a closed container without any water escaping. What changes?',['The water disappears.','The arrangement and motion change; it is still water.','The particles turn into empty space.'],1,'Follow the same matter through the change of state.','A state change does not destroy matter or automatically form a new substance.'))]],
 reflection='Compare solid and liquid water using the particle model. Explain what the dots help show and one thing the static picture cannot show.'),
7:dict(title='Connect power and time',goal='Calculate energy and explain where it is transferred.',objectives=['Use power and time','Compare two uses','Trace the energy'],needs=['math-3','science-4'],bodies=[
 'Energy is transferred between things or forms. Power tells how fast energy is transferred. At constant power, energy equals power times time: $E=Pt$.',
 'Double the time at the same power and twice as much energy is transferred. A device can transfer energy usefully and also heat its surroundings. Energy is not simply destroyed.'],labs=[[
 model(7,num('energy-first','Predict an energy transfer','An ideal device uses 5 watts for 4 seconds. How many joules of energy are transferred?',20,'A watt is one joule per second. Multiply power by time.','$E=5\\times4=20\\ \\mathrm{J}$.'))],[
 model(7,num('energy-compare','Same energy, different power','At a steady 10 watts, how many seconds transfer the same 20 joules?',2,'Rearrange $E=Pt$ to $t=E/P$.','$t=20/10=2\\ \\mathrm{s}$. Higher power needs less time for this same energy.'))]],
 reflection='Compare 5 W for 4 s with 10 W for 2 s. Explain why equal energy does not mean equal power. Name a possible transfer to the surroundings.'),
8:dict(title='Connect cell parts to their jobs',goal='Use a cell model and connect parts into a system.',objectives=['Explore a cell','Explain an exchange','Connect parts and whole'],needs=['science-3','science-6'],bodies=[
 'A cell is a basic living unit. Its parts do different jobs. The membrane controls exchange, ribosomes build proteins, and mitochondria help transfer energy into a usable form.',
 'Cells can work together in tissues, organs and systems. A diagram leaves out much of their detail. This model shows a typical animal cell; it does not describe every kind of cell.'],labs=[[
 model(8,pick('cell-boundary','Choose the part for the job','Which part controls exchange between this cell and its surroundings?',['The membrane.','The label on the picture.','Only the empty background.'],0,'Explore the outer boundary of the model.','The membrane is selective: it controls exchange rather than sealing everything out.'))],[
 model(8,pick('cell-limit','Check what the model means','What is a fair conclusion from this picture?',['Every cell has exactly this shape and these visible sizes.','These parts have jobs, but the picture is simplified and not every cell is the same.','Mitochondria create energy from nothing.'],1,'A useful model is not a photograph of every cell.','The model helps connect structure and function. Cells vary; energy is transferred, not created.'))]],
 reflection='Choose two cell parts and explain their jobs. Then explain how cells can work together and why this diagram is not a complete picture.'),
1:dict(title='Record what happened',goal='Separate a measured observation from a guess about its cause.',objectives=['Notice the evidence','Make it repeatable','Explain what is known'],needs=[],bodies=[
 'An observation is something you notice or measure. The cup holds 200 mL is an observation. Someone filled it earlier is a possible explanation. Keep them separate.',
 'A useful measurement has a number and a unit. Add how you measured it so another person can compare. Record what happened, even when it surprised you.'],labs=[[
 ev('observe-cup','Keep the observations','Which lines describe a measurement from this made-up test?',['The cup contains 200 mL of water.','The thermometer reads 22 degrees Celsius.','The cup is warm because someone held it.'],[0,1],'The volume and temperature are recorded observations. The proposed cause needs evidence.')],[
 ev('observe-method','Make the record useful','Which lines help someone repeat the toy-car measurement?',['The toy car was amazingly fast.','It travelled 2 m in 4 s on this surface.','We timed from the first mark to the second mark.'],[1,2],'Distance, time and a clear start and finish describe the measurement. Amazingly fast does not give a quantity.')]],
 reflection='Make up a short measurement record. Include a number, unit and method. Keep a possible cause separate from what was observed.'),
2:dict(title='Choose a rain cover',goal='Match material properties to the job.',objectives=['Compare materials','Check the whole design','Explain a choice'],needs=['science-1'],bodies=[
 'A material is what something is made from. A property is how it behaves, such as bending or soaking up water. Choose properties that fit the job.',
 'Compare materials in the same way. Water-resistant material can still leak through a hole or an open edge. Check the whole design as well as the material.'],labs=[[
 model(2,pick('material-cover','Choose for this job','Which property is especially useful for a rain cover?',['It absorbs rain quickly.','It resists water passing through.','It has the longest name.'],1,'Think about what the cover must keep out.','Water resistance matters for a rain cover. Strength, weight and reuse may matter too.'))],[
 model(2,pick('material-hole','A new problem appears','A plastic cover leaks at a join. What should you investigate?',['Whether the join or a hole lets water through.','Whether all plastic is always useless.','Only the cover’s colour.'],0,'A useful material does not guarantee a sealed design.','The leak could be in the join rather than through an intact sheet. Compare the same conditions.'))]],
 reflection='Choose a material for a rain cover. Name two useful properties and one design detail you would check. This is a plan, not a claim you ran a test.'),
3:dict(title='Find what limits a habitat',goal='Use a simple model to spot a missing resource.',objectives=['Meet the needs','Change one resource','Name the model’s limit'],needs=['science-1','math-3'],bodies=[
 'A habitat is where a living thing lives. It must provide what that living thing needs. In this simple model, each animal needs one food portion and one shelter.',
 'More food may not help if shelter is missing. Food also connects living things: a food chain shows who eats whom. Its arrows follow energy from food to the animal eating it.'],labs=[[
 model(3,num('habitat-limit','Count supported animals','There are 7 food portions and 4 shelters. Each animal needs one of each. How many animals can this model support?',4,'Find the smaller of the two available resources.','Only 4 animals have both a food portion and a shelter.'))],[
 model(3,num('habitat-change','Add a different resource','The food stays at 7 portions. Shelters increase from 4 to 9. How many animals can the model support now?',7,'Now food is the smaller amount.','The limit changes to 7 food portions. Two extra shelters alone do not feed more animals.'))]],
 reflection='Explain which resource limits each example. Name one important feature of a real habitat that this model does not include.'),
4:dict(title='Predict how a cart changes speed',goal='Connect net force, mass and acceleration in an ideal model.',objectives=['Apply the model','Change the mass','Explain its limits'],needs=['math-3','science-1'],bodies=[
 'A net force is the overall push after forces are combined. In this ideal cart model, acceleration equals net force divided by mass. Acceleration means a change in velocity, not velocity itself.',
 'Position tells where something is. Speed tells how fast it moves. Acceleration tells how its velocity changes. With the same net force, a heavier cart has less acceleration; that alone does not tell its present speed.'],labs=[[
 model(4,num('cart-first','Predict the acceleration','The net force is 6 newtons and the mass is 2 kilograms. What is the acceleration in metres per second squared?',3,'Use $a=F/m$.','$a=6/2=3\\ \\mathrm{m/s^2}$.'))],[
 model(4,num('cart-heavy','The cart is heavier','Keep the net force at 6 newtons but change mass to 3 kilograms. What is acceleration now?',2,'Divide the same force by the new mass.','$a=6/3=2\\ \\mathrm{m/s^2}$. The model assumes a known net force and fixed mass.'))]],
 reflection='Compare both cart cases. Explain which quantity stayed fixed and why acceleration differs from speed.'),
}

EARLY_WHY={
1:['An observation tells what you noticed. An explanation tries to say why. Separating them lets another person check the record without accepting your guess first.',
   'Big means different things to different people. A number and unit are clearer. Add the tool and start and finish points so another person knows how you got the number.'],
2:['A rain cover and a cleaning cloth need different properties. One should keep water out; the other may need to soak water up. Choose for the purpose, not the name.',
   'Use the same amount of water, size of sample and time when comparing. Otherwise the difference could come from the test method instead of the material.'],
3:['A shelter alone does not feed an animal, and food alone does not give shelter. Count how many complete sets of needs you can meet in this deliberately simple model.',
   'When the smaller resource increases, another resource can become the limit. Food links add another connection: less grass can affect animals that eat it and animals that eat those animals. Real habitats also depend on water and temperature.']}

# Keep the worked example beside the investigation it actually explains.
WORKED={
3:[{},dict(title='Follow food and resources',example='From grass to grasshopper to bird')],
4:[{},dict(example='A toy car covers 6 metres in 3 seconds',whyItWorks='Average speed uses total distance and total time. It cannot tell whether the car sped up or slowed down along the way. Acceleration needs information about changing velocity. In the cart model, use the combined force and mass: $a=F/m$. Hold one fixed before comparing the other.')],
8:[dict(title='Connect cell parts to their jobs',example='A simplified animal cell',steps=[
    'Find the membrane: it controls exchange with the surroundings.',
    'Find the ribosomes: they build proteins the cell needs.',
    'Find the mitochondria: they help transfer energy into a form the cell can use.']),
   dict(title='Connect cells into a bigger system',example='Muscle cells help an arm move',steps=[
    'Muscle cells can contract. They work together in muscle tissue.',
    'Muscles work with bones, nerves and other parts so the arm can move.',
    'A flat cell diagram helps name parts. It cannot show every shape, size or interaction.'])],
10:[{},dict(title='Count whole molecules and track escaping matter',example='Read the count, then check the boundary',steps=[
    'In $2H_2$, the coefficient 2 counts two molecules. Each contains two hydrogen atoms: $2\\times2=4$ atoms.',
    'Changing $H_2$ to $H_3$ would change the formula. It would not be a valid way to balance this equation.',
    'If a reaction releases gas from an open cup, count the escaped gas as well as what remains. The cup can get lighter without atoms being destroyed.'])],
11:[dict(title='Use voltage and resistance',example='9 volts across an ideal 3-ohm resistor',steps=[
    'Identify voltage $V=9\\ \\mathrm{V}$ and resistance $R=3\\ \\Omega$.',
    'Divide: $I=V/R=9/3=3\\ \\mathrm{A}$.',
    'Keep voltage at 9 V and double resistance to 6 ohms. Current halves: $I=9/6=1.5\\ \\mathrm{A}$.']),
   dict(title='Count cycles and compare height',example='A wave repeats every half second',steps=[
    'The period is the time for one complete cycle: $T=0.5\\ \\mathrm{s}$.',
    'Frequency counts cycles per second: $f=1/T=1/0.5=2\\ \\mathrm{Hz}$.',
    'Doubling the height from the middle to a peak changes amplitude. If each cycle still takes half a second, frequency stays 2 Hz.'])],
}

def attach(units):
    for u in units:
        d=MISSIONS.get(u['grade']) if u['subject']=='science' else None
        if not d:continue
        for l,b in zip(u['lessons'],d['bodies']):l['body']=b
        if u['grade'] in EARLY_WHY:
            for l,w in zip(u['lessons'],EARLY_WHY[u['grade']]):l['whyItWorks']=w
        for l,worked in zip(u['lessons'],WORKED.get(u['grade'],[])):l.update(worked)
        install(u,d['title'],d['goal'],d['objectives'],d['labs'],d['needs'],'Notice / predict / check',reflection=d['reflection'])
    for u in units:
        if u.get('mission',{}).get('kind')=='scenario':u['mission']['preparation']=[{'id':i,'title':next(v['title'] for v in units if v['id']==i)} for i in u['mission'].get('needs',[])]
