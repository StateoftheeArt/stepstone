import assert from 'node:assert/strict';
import fs from 'node:fs';
import {accuracy,typingComplete,typingSummary,typingReport} from '../public/typing-lab.js';
assert.equal(accuracy('Milk\nbread','Milk\nbread'),100);
assert.equal(accuracy('cat','cart'),75);
assert.equal(accuracy('abcdef','abdef'),83);
assert.equal(accuracy('hello',''),0);
assert.equal(accuracy('4:30','4:03'),50);
assert.equal(accuracy('😀a','😀b'),50);
const task={id:'a',kind:'typing',target:'abcdefghijklmnopqrst'},work={typing:{text:'abcdefghijklmnopqrsx',method:'phone',target:95}};
assert.equal(typingComplete(task,work),true);
assert.equal(typingComplete({...task,exact:true},work),false);
work.typing.target=0;assert.equal(typingComplete(task,work),true);assert.equal(work.typing.target,95);
work.typing.text='';assert.equal(typingComplete(task,work),false);
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const modules=catalog.units.filter(u=>u.course==='typing');assert.equal(modules.length,3);
for(const u of modules){const draft={scenarioLab:{}};for(const [i,tasks] of u.mission.labs.entries()){
 const phase=draft.scenarioLab[i?3:1]={tasks:{}};
 for(const t of tasks.filter(t=>t.kind==='typing')){assert.ok(t.target.length&&t.target.length<400);const w={checked:true,typing:{text:t.target,method:'assistive',target:95,paused:true}};assert.equal(typingComplete(t,w),true);phase.tasks[t.id]=w;}}
 const summary=typingSummary(u,draft);assert.equal(summary.length,u.mission.labs.flat().filter(t=>t.kind==='typing').length);assert.ok(summary.every(r=>r.accuracy===100&&r.assisted));assert.ok(summary.every(r=>!('text' in r)));assert.match(typingReport(summary),/not unaided typing speed/);
}
console.log('Typing: insertion/deletion/replacement, Unicode, empty input, exact details, access targets, saved summaries and 3 integrated modules passed.');
