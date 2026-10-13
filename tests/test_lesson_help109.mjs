import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PITFALLS,commonPitfall} from '../public/lesson-help.js';
import {missionPractice} from '../public/mission.js';
import {lessonDiagram} from '../public/lesson-diagrams.js';
import {lessonVisualMarkup} from '../public/lesson-visual.js';
import {stockExampleFrames} from '../public/stock-visual.js';
import {canadianCoin,lessonSourceFooter} from '../public/canadian-money.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
for(const unit of catalog.units.filter(u=>u.ready)){
  assert.ok(PITFALLS[unit.id]?.length>30,'Missing specific pitfall: '+unit.id);
  for(const q of unit.practice){
    const tip=commonPitfall(unit,q);
    assert.ok(tip.length<250,unit.id);
    assert.doesNotMatch(tip,/\$|\b(?:answer is|choose option|add a ten twice|try 6|20\+4)\b/i);
  }
  const questions=[{id:'done',prompt:'Previous question',explanation:'PREVIOUS SOLUTION MUST NOT APPEAR'}, {id:'now',prompt:'Current question'}];
  const markup=missionPractice(unit,{questions,checks:{done:true},cursor:1},q=>`<p>${q.prompt}</p>`,s=>s);
  assert.match(markup,/Current question/);
  assert.doesNotMatch(markup,/mission-recap|Previous question|PREVIOUS SOLUTION|worked out/);
}
const order={id:'math-1'};
assert.match(commonPitfall(order,{prompt:'How many drink cartons should you take out?'}),/removed.*left/);
assert.match(commonPitfall(order,{prompt:'How many more drink cartons do you need?'}),/extra.*final total/);
assert.match(commonPitfall({id:'math-2'},{prompt:'Open one ten'}),/counts those items twice/);
assert.match(commonPitfall({id:'reading-1'},{prompt:'When should you meet?'}),/question about time/);
assert.match(commonPitfall({id:'reading-1'},{prompt:'Where should you meet?'}),/question about a place/);
const stock=catalog.units.find(u=>u.id==='math-2');
for(let step=0;step<3;step++){
  const art=lessonDiagram({...stock,exampleMode:'money'},step);
  assert.equal((art.match(/data-cad="10-dollars"/g)||[]).length,2);
  assert.equal((art.match(/data-cad="1-dollar"/g)||[]).length,step===0?0:4);
  assert.match(art,/Two Canadian ten-dollar notes/);
  assert.doesNotMatch(art,/\bNaN\b|undefined/);
}
assert.match(lessonDiagram({...stock,exampleMode:'money'},2),/\$20 \+ \$4 = \$24/);
assert.match(lessonDiagram({...stock,exampleMode:'money'},0),/\$10 \+ \$10 = \$20/);
assert.match(lessonDiagram({...stock,exampleMode:'money'},1),/Four loonies = \$4/);
assert.match(stockExampleFrames(stock,'money')[0].text,/10-dollar notes/);
assert.match(stockExampleFrames(stock,'money')[1].text,/1-dollar loonies/);
assert.doesNotMatch(lessonVisualMarkup({...stock,exampleMode:'money'}),/Source:.*Bank of Canada Museum/s);
assert.match(lessonSourceFooter(stock),/<footer.*Original value diagrams.*Bank of Canada Museum/s);
assert.equal((lessonDiagram({id:'math-cash'},2).match(/data-cad="25-cents"/g)||[]).length,3);
assert.match(lessonDiagram({id:'math-cash'},0),/Three quarters = 75 cents/);
assert.match(lessonDiagram({id:'math-cash'},1),/Two loonies = 200 cents/);
assert.match(lessonDiagram({id:'math-cash'},2),/275 cents = \$2\.75/);
assert.throws(()=>canadianCoin(2,0,0),RangeError);
// Incorrect-answer feedback must not reveal the published solution.
const app=fs.readFileSync(new URL('../public/app.js',import.meta.url),'utf8');
assert.doesNotMatch(app,/html\(q\.hint\)|Show a helpful step/);
assert.match(app,/That does not fit yet\. ".*commonPitfall/);
for(const name of ['mission.js','mission-lab.js']){
  const source=fs.readFileSync(new URL('../public/'+name,import.meta.url),'utf8');
  assert.doesNotMatch(source,/html\(task\.hint\)|esc\(task\.hint\)|mission-recap/);
  assert.match(source,/commonPitfall\(u,task\)/);
}
console.log(`PASS: ${catalog.units.filter(u=>u.ready).length} modules have specific common-pitfall help, no worked-answer recaps; Canadian $10 notes, loonies and quarters match the example steps.`);
