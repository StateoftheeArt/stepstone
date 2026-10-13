import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {startingPoint,startingQuestion} from '../public/engine.js';
import {suggestedStart} from '../public/curriculum.js';
import {moduleAccess} from '../public/foundation.js';
import {startingItemUnits,previewStartingItems} from '../public/starting-items.js';
import {preservePreviewCompletions} from '../public/wins.js';

const bank=JSON.parse(readFileSync(new URL('../public/starting-point.json',import.meta.url)));
const catalog=JSON.parse(readFileSync(new URL('../public/catalog.json',import.meta.url)));
const options=JSON.parse(readFileSync(new URL('../public/profile-options.json',import.meta.url)));
const unlocks=[['accessory',options.accessories],...Object.entries(options.home).map(([field,choices])=>['home.'+field,choices])].flatMap(([kind,choices])=>choices.filter(c=>c.modules>0).map(c=>({...c,key:kind+':'+c.id})));
const data={version:5,age:16,seed:37,answers:[]};
let result;
while((result=startingPoint(bank,data)).next){
  const q=startingQuestion(bank,data,result.next);
  data.answers.push({id:q.id,answer:q.kind==='number'?String(q.answer):q.answer,heard:true});
}
assert.equal(data.answers.length,24);
assert.deepEqual(startingItemUnits(catalog,result),[],'An unfinished writing choice cannot grant cosmetic milestones.');
data.writing={status:'skipped',text:''};result=startingPoint(bank,data);
const units=startingItemUnits(catalog,result);
assert.equal(units.length,28);
for(const subject of ['math','reading','science','life']){
  const next=suggestedStart(catalog,subject,result);
  assert.equal(moduleAccess({catalog,unit:next,starting:result}).allowed,true);
}
for(const subject of ['digital','work']){
  const next=suggestedStart(catalog,subject,result);
  assert.equal(moduleAccess({catalog,unit:next,starting:result}).reason,'core-courses');
}
const records=new Map();const storage={getItem:k=>records.get(k),setItem:(k,v)=>records.set(k,v)};
const args={storage,key:'synthetic-owner',catalog,result,unlocks};
const inventory=previewStartingItems(args);
assert.deepEqual(new Set(inventory),new Set(unlocks.filter(c=>c.modules<=28).map(c=>c.key)));
assert.deepEqual(previewStartingItems({...args,result:{complete:false}}),inventory,'A retake keeps previously owned items.');
assert.deepEqual(previewStartingItems({...args,key:'different-owner',result:null}),[],'Preview owners have separate inventories.');
const local={'math-1':{result:{passed:true,score:6,at:1}}};
preservePreviewCompletions(local,unlocks,units);
assert.deepEqual(local['math-1'].firstPass.pipItems,[],'Revisiting an assessed skill does not duplicate cosmetics.');
local['math-prices']={result:{passed:true,score:6,at:2}};
local['math-budget']={result:{passed:true,score:6,at:3}};
preservePreviewCompletions(local,unlocks,units);
assert.ok(local['math-budget'].firstPass.pipItems.length,'The next real milestone earns its new item.');
const snapshot=JSON.stringify(local);preservePreviewCompletions(local,unlocks,units);assert.equal(JSON.stringify(local),snapshot);
console.log('Starting questions route the first four courses, preserve unfinished checks and owned items, and count each cosmetic milestone once.');
