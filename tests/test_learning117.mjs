import assert from 'node:assert/strict';
import fs from 'node:fs';
import {practicePool,practiceRound,questionKey} from '../public/lesson-questions.js';
import {commonPitfall} from '../public/lesson-help.js';
import {lessonVisualMarkup} from '../public/lesson-visual.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const units=catalog.units.filter(u=>u.ready);
for(const unit of units){
  const draft={rounds:{}};
  for(const phase of [2,4]){
    const pool=practicePool(unit,phase,draft);
    assert.ok(new Set(pool.map(q=>q.caseId||q.prompt)).size>=3,`${unit.id}: fresh situations in phase ${phase}`);
    const round=practiceRound(unit,phase,draft);
    assert.equal(round.questions.length,3,unit.id);
    assert.equal(new Set(round.questions.map(q=>q.caseId||q.prompt)).size,3,unit.id);
  }
  assert.equal(new Set(Object.values(draft.rounds).flatMap(r=>r.questions.map(questionKey))).size,6,unit.id);
}
const stock=units.find(u=>u.id==='math-2');
const corrected=stock.practice.find(q=>q.kind==='number'&&q.answer===11&&/2 closed bundles/.test(q.prompt));
assert.ok(corrected,'21-label regrouping situation is retained');
assert.match(corrected.prompt,/1 loose label\. You open ONE bundle/);
assert.match(corrected.prompt,/How many LOOSE labels/);
assert.match(corrected.explanation,/1\+10=11/);
assert.match(corrected.explanation,/total is still 21/);
const old={...corrected,prompt:'You trade 1 ten from 21 for 10 ones. How many ones are there now?',explanation:'old feedback'};
const saved={questions:[old],answers:{[old.id]:'10'},checks:{[old.id]:false},last:{[old.id]:'10'},tries:1,hints:{[old.id]:true}};
const draft={rounds:{4:saved}};
assert.equal(practiceRound(stock,4,draft),saved,'resume retains the round object');
assert.equal(saved.questions[0].prompt,corrected.prompt,'a wording fix reaches a saved round');
assert.deepEqual(saved.answers,{[old.id]:'10'});assert.equal(saved.tries,1);assert.equal(saved.checks[old.id],false);
const changedAnswer={...stock,practice:[{...corrected,answer:12,prompt:'A different problem'}]};
practiceRound(changedAnswer,4,draft);assert.equal(saved.questions[0].prompt,corrected.prompt,'changed answers must not reinterpret a saved attempt');
assert.match(commonPitfall(stock,corrected),/loose-label count.*whole shelf count/);
const receipt=units.find(u=>u.id==='math-5');
assert.match(receipt.title,/receipt/);assert.match(commonPitfall(receipt,receipt.practice[0]),/unit price|price marked each/i);
assert.match(lessonVisualMarkup(units.find(u=>u.id==='writing-1')),/Tuesday at 3 pm/);
assert.doesNotMatch(lessonVisualMarkup(units.find(u=>u.id==='writing-1')),/blue folder/);
console.log(`PASS: ${units.length} modules supply six fresh practice questions; saved regrouping wording refreshes without changing answers or grading; receipt help and meeting example match the lessons.`);
