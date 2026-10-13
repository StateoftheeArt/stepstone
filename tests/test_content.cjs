const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),catalog=JSON.parse(fs.readFileSync(path.join(root,'public/catalog.json'))),bank=JSON.parse(fs.readFileSync(path.join(root,'content/checkpoints.json'))),katex=require(path.join(root,'public/vendor/katex/katex.min.js'));
assert.deepEqual(catalog.subjects.map(s=>s.id),['math','reading','science','life','digital','work']);
for(const subject of catalog.subjects){const pathUnits=catalog.units.filter(u=>u.subject===subject.id&&u.active!==false).sort((a,b)=>a.sequence-b.sequence);assert.equal(pathUnits.length,24,subject.name);assert.deepEqual(pathUnits.map(u=>u.sequence),Array.from({length:24},(_,i)=>i+1));}
assert.equal(catalog.units.filter(u=>u.active!==false).length,144);assert.equal(catalog.units.filter(u=>u.legacy).length,9);
assert.equal(catalog.units.filter(u=>u.ready).length,153);assert.equal(new Set(catalog.units.map(u=>u.id)).size,catalog.units.length);
const guides=catalog.units.filter(u=>u.guide&&!u.course&&u.guide.checked==='2026-09-24');
const workGuides=['life-job-apply','life-first-shift','life-work-problem'];
const transportGuides=['life-bus-trip','life-trip-change','life-driver-plan','life-road-signs'];
const homeGuides=['life-rental-costs','life-home-bills','life-meal-plan','life-home-care','life-repair-request'];
const supportGuides=['life-appointment','life-find-support','life-boundaries','life-adjustments'];
const communicationGuides=[...workGuides,'life-boundaries','life-adjustments'];
assert.deepEqual(guides.map(u=>u.id).sort(),['life-health-card','life-photo-id','life-sin','life-bank-account','life-tax-prep','life-tax-result',...workGuides,...transportGuides,...homeGuides,...supportGuides].sort());
for(const u of guides){
 assert.equal(u.domain,communicationGuides.includes(u.id)?'social':'digital');assert.equal(u.guide.region,'Manitoba, Canada');assert.equal(u.guide.checked,'2026-09-24');
 assert.ok(u.practical&&u.guide.steps.length>=3&&u.resources.some(r=>r.help));
 assert.ok(u.resources.every(r=>r.checked===u.guide.checked&&new URL(r.url).protocol==='https:'&&['www.gov.mb.ca','www.mpi.mb.ca','apps.mpi.mb.ca','www.canada.ca','www.jobbank.gc.ca','www.manitoba.ca','www.winnipeg.ca','www.winnipegtransit.com','info.winnipegtransit.com','www.hydro.mb.ca','ised-isde.canada.ca','www.harvestmanitoba.ca','mb.211.ca','kidshelpphone.ca','www.manitobahumanrights.ca'].includes(new URL(r.url).hostname)));
 assert.ok(bank[u.id].every(q=>!u.practice.some(p=>p.caseId===q.caseId)),'service checks must use different cases from practice');
 for(const lesson of [1,2])assert.equal(bank[u.id].filter(q=>q.lesson===lesson).length,6);
}
// Every possible guide check covers its intended skills and both lesson ideas.
for(const id of ['life-bank-account','life-tax-prep','life-tax-result',...workGuides,...transportGuides,...homeGuides,...supportGuides]){
 const u=catalog.units.find(u=>u.id===id),skills=u.checkSkills||['calculate','apply','reason'];
 assert.equal(skills.length,3);assert.equal(new Set(skills).size,3);
 assert.ok(skills.every(s=>['calculate','interpret','apply','reason'].includes(s)));
 assert.ok(bank[id].every(q=>skills.includes(q.skill)));
 const pools=skills.map(skill=>bank[id].filter(q=>q.skill===skill));
 const pairs=pools.map(pool=>{assert.ok(pool.length>=3);return pool.flatMap((a,i)=>pool.slice(i+1).map(b=>[a,b]));});
 if(skills[0]==='calculate')assert.ok(pools[0].every(q=>q.kind==='number'||q.prompt.includes('which costs less')));
 for(const a of pairs[0])for(const b of pairs[1])for(const c of pairs[2])assert.equal(new Set([...a,...b,...c].map(q=>q.lesson)).size,2,id+' needs both lessons in every check');
}
for(const id of supportGuides){const u=catalog.units.find(u=>u.id===id);assert.ok(u.mission.labs.every(tasks=>tasks.length===3));assert.ok(u.mission.labs[1].some(t=>t.revise));}
const mission=catalog.units.find(u=>u.id==='math-1');
assert.equal(mission.title,'Pack the order');assert.equal(mission.workshop.kind,'order');
assert.equal(mission.mission.objectives.length,3);
for(const lesson of mission.lessons)assert.ok(lesson.body.split(/\s+/).length<=35,'early mission text should stay short');
for(const lesson of [1,2])assert.ok(new Set(mission.practice.filter(q=>q.lesson===lesson).map(q=>q.caseId)).size>=3,'each mission idea needs three distinct practice cases');
for(const skill of ['calculate','apply','reason'])assert.ok(bank['math-1'].filter(q=>q.skill===skill).length>=2,'six-question check must cover calculation, application and reasoning');
const reading=catalog.units.find(u=>u.id==='reading-1');
assert.equal(reading.title,'Read the plan');assert.equal(reading.workshop.kind,'message');
for(const u of [mission,reading]){
 assert.equal(u.mission.objectives.length,3);assert.equal(u.mission.brief.length,3);
 for(const field of ['tagline','startLabel','labLabel','backLabel','practiceLabel','recapLabel'])assert.ok(u.mission[field]);
 for(const lesson of u.lessons)assert.ok(lesson.body.split(/\s+/).length<=35,'early mission copy stays short');
 for(const lesson of [1,2])assert.ok(new Set(u.practice.filter(q=>q.lesson===lesson).map(q=>q.caseId)).size>=3);
}
for(const tasks of reading.mission.labs){
 assert.equal(tasks.length,3);
 for(const task of tasks){assert.ok(task.options[task.answer]);assert.ok(task.hint&&task.why&&task.messages.length);}
}
for(const q of [...reading.practice,...bank['reading-1']])assert.ok(q.passage&&q.caseId&&q.lesson,'reading needs a source message, distinct scenario and matched lesson');
assert.ok(bank['reading-1'].every(q=>!reading.practice.some(p=>p.caseId===q.caseId)),'independent checks use fresh scenarios');
const equations=bank['math-8'].filter(q=>q.prompt.startsWith('Solve for'));
assert.ok(new Set(equations.map(q=>q.answer)).size>=4,'equation checks must not all have the same memorisable answer');
for(const q of equations){const [,a,b,total]=q.prompt.match(/\$(\d+)x\+(\d+)=(\d+)\$/);assert.equal(Number(a)*q.answer+Number(b),Number(total),'the answer must balance the stated equation');}
let texCount=0,questions=0;
function scan(value){if(typeof value==='string'){for(const [,tex]of value.matchAll(/\$([^$]+)\$/g)){katex.renderToString(tex,{throwOnError:true,strict:'error'});texCount++;}}else if(Array.isArray(value))value.forEach(scan);else if(value&&typeof value==='object')Object.values(value).forEach(scan);}
for(const u of catalog.units.filter(u=>u.ready)){
 assert.ok(['order','message','scenario'].includes(u.mission?.kind),u.id+' must use the shared mission flow');
 for(const lesson of [1,2])assert.ok(new Set(u.practice.filter(q=>q.lesson===lesson).map(q=>q.caseId||q.prompt)).size>=3,u.id+' must have three distinct practice situations for each lesson');
 if(u.mission.kind==='scenario'){
  const ids=new Set();assert.equal(u.mission.labs.length,2);
  for(const tasks of u.mission.labs){assert.ok(tasks.length);for(const t of tasks){
   assert.ok(!ids.has(t.id)&&t.title&&t.prompt&&t.hint&&t.why,u.id+' incomplete or repeated task');ids.add(t.id);
   assert.ok(['number','choice','stock','groups','fraction','money','evidence','draft','conversation','pc','typing'].includes(t.kind),t.id);
   if(t.kind==='number')assert.ok(Number.isFinite(t.answer),t.id);
   if(t.kind==='choice')assert.ok(t.options[t.answer],t.id);
   if(t.kind==='evidence')assert.ok(t.answer.length&&new Set(t.answer).size===t.answer.length&&t.answer.every(i=>t.lines[i]),t.id);
   if(['draft','conversation'].includes(t.kind))assert.equal(t.checks.length,3,t.id+' needs a clear human-review checklist');
   if(t.table){assert.ok(t.table.caption&&t.table.columns.length>=2&&t.table.rows.length);assert.ok(t.table.rows.every(row=>row.length===t.table.columns.length&&row.every(cell=>typeof cell==='string'&&cell.trim())),t.id+' table needs labelled complete rows');}
   if(t.sign)assert.ok(['stop','yield'].includes(t.sign),t.id+' needs a supported sign with text alternative');
  }}
  for(const ref of u.mission.preparation)assert.equal(ref.title,catalog.units.find(v=>v.id===ref.id)?.title,u.id+' prerequisite is stale');
 }
 assert.equal(u.lessons.length,2);assert.ok(u.lessons.every(l=>l.whyItWorks?.length>=(u.visual?32:121)&&l.watchFor?.length>25),u.id+' missing substantive explanations');assert.ok(u.workshop,u.id+' missing interactive workshop');assert.ok(u.lessons.every(l=>l.body.trim().length>0&&l.steps.length>=3),u.id+' missing explanation or worked steps');
 assert.ok(new Set(u.practice.map(q=>JSON.stringify([q.passage||'',q.prompt]))).size>=6,`${u.id}: preview needs six distinct questions`);
 // Six unseen cases make one check; published practice stays out of the bank where the build can hold it out.
 assert.ok(new Set(bank[u.id].map(q=>q.caseId||q.prompt)).size>=6,u.id+' needs six distinct check cases');
 for(const q of [...u.practice,...bank[u.id]]){questions++;assert.ok(q.id&&q.explanation&&q.prompt);if(q.kind==='choice'){assert.ok(q.options.some(o=>o.id===q.answer));assert.equal(new Set(q.options.map(o=>o.text)).size,q.options.length,`${q.id} ambiguous options`);}else assert.ok(Number.isFinite(q.answer));}
}
scan(catalog);scan(bank);
const starting=JSON.parse(fs.readFileSync(path.join(root,'public/starting-point.json')));
assert.equal(starting.version,2);assert.equal(starting.questions.length,72);assert.equal(new Set(starting.questions.map(q=>q.id)).size,72);
assert.deepEqual(starting.subjects,['math','reading','writing','science','social','digital'],'The original assessment skill domains remain stable for saved placement results.');
for(const subject of starting.subjects){
 for(const band of [0,1,2,3])assert.equal(starting.questions.filter(q=>q.subject===subject&&q.band===band).length,3);
 for(const level of starting.starts[subject])assert.ok(catalog.units.find(u=>u.id===subject+'-'+level)?.ready);
}
for(const q of starting.questions){if(q.kind==='choice'){assert.equal(new Set(q.options).size,3);assert.ok(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<3);}else assert.ok(Number.isFinite(q.answer));}
assert.equal(starting.legacy.questions.length,30);
for(const q of starting.legacy.questions){assert.equal(new Set(q.options).size,4);assert.ok(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<4);}
scan(starting);
(async()=>{const {correct,numberValue,mergeStages,reviewDue,readable}=await import('../public/engine.js');assert.equal(numberValue('3/4'),.75);assert.equal(numberValue('1/0'),null);assert.equal(numberValue(''),null);assert.equal(correct({kind:'number',answer:.01},'0'),false);assert.equal(mergeStages({'math-1':{phase:1}},{'math-1':5})['math-1'].phase,1);assert.equal(reviewDue([{unit:'math-1',finished:100,report:{passed:false}}],101).length,1);assert.match(readable('$\\frac{3}{4}$'),/3 divided by 4/);for(const [text,value] of [['$10',10],['10 CAD',10],['CAD 6,000',6000],['10,000',10000],['10 000',10000],['25%',25],['10 dollars',10],['-$5',-5],['$2.75',2.75],['3/4',.75],['1,5',null],['12,3456',null],['three',null],['$',null],['',null]])assert.equal(numberValue(text),value,text);console.log(`Validated 6 paths, ${catalog.units.length} practical modules, ${questions} questions, ${texCount} LaTeX fragments, and resume/scoring helpers.`);})().catch(e=>{console.error(e);process.exit(1)});
