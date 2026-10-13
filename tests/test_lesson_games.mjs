import assert from 'node:assert/strict';
import fs from 'node:fs';
import {gameTotal} from '../public/lesson-games.js';
import {scenarioCorrect} from '../public/mission-lab.js';
import {homeMarkup} from '../public/home.js';

const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const tasks=catalog.units.flatMap(u=>(u.mission?.labs||[]).flat()).filter(t=>t.game);
assert.equal(tasks.length,8);
for(const task of tasks){
  const g=task.game;
  const state=g.kind==='cash'?{coins:[500,200,25]}:{selected:g.kind==='discount'?[0]:g.parts.map((_,i)=>i)};
  const total=gameTotal(g,state),answer=g.kind==='budget'?g.total-total:total;
  assert.equal(answer,task.answer,task.id);
  assert.ok(task.answerLabel,task.id);
  assert.ok(scenarioCorrect(task,{answer:String(answer)}),task.id);
  assert.equal(scenarioCorrect(task,{answer:String(answer+1)}),false,task.id);
}
const pay=tasks.find(t=>t.id==='pay-gross');
assert.equal(scenarioCorrect(pay,{answer:'4'}),false);
assert.equal(scenarioCorrect(pay,{answer:' 60.00 '}),true);
const clock=tasks.find(t=>t.id==='pay-time');
assert.equal(scenarioCorrect(clock,{answer:'7/2'}),true);
assert.equal(scenarioCorrect(clock,{answer:'3.30'}),false);
assert.equal(scenarioCorrect(clock,{answer:'3/0'}),false);
assert.equal(gameTotal(clock.game,{selected:[0,0,1]}),2);
const next=catalog.units.find(u=>u.id==='math-pay');
const html=homeMarkup({catalog,next,draft:{phase:1,scenarioLab:{1:{cursor:1}}},done:new Set(),html:s=>s});
assert.match(html,/9:00 to 12:30/);
assert.match(html,/Continue where I left off/);
assert.doesNotMatch(html,/#play|Try a short practice|level-card/);
console.log('Eight question-linked games, units, decimal/fraction grading and saved-question preview passed.');

const reading=catalog.units.find(u=>u.id==='reading-1');
const readingHome=homeMarkup({catalog,next:reading,draft:{phase:1,messageLab:{1:{cursor:1}}},done:new Set(),html:s=>s});
assert.ok(readingHome.includes(reading.mission.labs[0][1].prompt));
const exampleHome=homeMarkup({catalog,next,draft:{phase:1,examplePhase:1},done:new Set(),html:s=>s});
assert.ok(exampleHome.includes('Worked example'));
assert.ok(exampleHome.includes(next.lessons[0].body));

const order=catalog.units.find(u=>u.id==='math-1');
for(const [phase,count,checked,expected] of [[1,6,false,'1 more to pack.'],[1,7,true,'Order checked.'],[3,7,false,'2 extra to take out.']]){
 const draft={phase,orderLab:{[phase]:{count,checked}}},saved=JSON.stringify(draft);
 const page=homeMarkup({catalog,next:order,draft,done:new Set(),html:s=>s});
 assert.ok(page.includes(expected));
 assert.match(page,/Saved packing activity/);
 assert.equal((page.match(/class="preview-carton packed/g)||[]).length,count);
 assert.equal(JSON.stringify(draft),saved);
}
const orderExample=homeMarkup({catalog,next:order,draft:{phase:1,examplePhase:1,orderLab:{1:{count:7,checked:true}}},done:new Set(),html:s=>s});
assert.ok(orderExample.includes(order.lessons[0].body));
assert.doesNotMatch(orderExample,/Saved packing activity/);
console.log('Saved packing previews match incomplete, checked and overpacked bags; worked examples remain separate.');

for(const next of catalog.units.filter(u=>u.ready)){for(let phase=0;phase<8;phase++){
 const draft={phase};const saved=JSON.stringify(draft);
 const page=homeMarkup({catalog,next,draft,done:new Set(),html:s=>String(s??'')});
 assert.doesNotMatch(page,/undefined|\[object Object\]/,next.id+' phase '+phase);
 assert.equal(JSON.stringify(draft),saved);
}}
console.log('All 103 Home previews render across eight saved phases without mutating progress.');
