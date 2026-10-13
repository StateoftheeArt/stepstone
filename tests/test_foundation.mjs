// Pure routing/markup checks. No browser automation or claimed learner grades.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {previewFoundation,nextFoundationUnit,foundationMarkup,moduleAccess,nextCourseUnit,courseReadiness} from '../public/foundation.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const plan=previewFoundation(JSON.parse(fs.readFileSync(new URL('../public/foundation.json',import.meta.url))));
const next=extra=>nextFoundationUnit({catalog,plan,...extra})?.id;
assert.equal(next({}),'math-1');
assert.equal(next({done:new Set(['math-cash'])}),'math-5');
assert.equal(next({local:{'reading-1':{phase:2}}}),'reading-1');
assert.equal(next({subject:'digital'}),undefined);
const starting={complete:true,levels:{math:1,reading:1}};
assert.equal(next({starting}),'math-1');
assert.equal(next({starting,done:new Set(['math-1'])}),'math-2');
assert.equal(next({starting,done:new Set(['math-1','reading-1'])}),'math-2');
const allCore=new Set(plan.groups.flatMap(g=>g.units));
assert.ok(next({done:allCore}));
const markup=foundationMarkup(plan,catalog,{preview:true});
assert.equal((markup.match(/class="foundation-step"/g)||[]).length,32);
assert.ok(markup.includes('Preview only.'));
assert.ok(!foundationMarkup(plan,catalog,{compact:true}).includes('class="foundation-step"'));
assert.ok(foundationMarkup(plan,catalog,{offline:true}).includes('Last saved results.'));
console.log('Foundation routing, saved-place ordering and markup passed.');

assert.equal(next({local:{'math-1':{phase:2,touchedAt:100},'reading-1':{phase:1,touchedAt:200}}}),'reading-1');
assert.equal(next({local:{'math-1':{phase:2,touchedAt:100},'reading-1':{phase:0,touchedAt:200}}}),'reading-1');
assert.equal(next({local:{'math-1':{phase:2,touchedAt:100},'reading-1':{phase:7,touchedAt:200}}}),'math-1');

const core=new Set(catalog.units.filter(u=>u.ready&&u.active!==false&&['math','reading','science','life'].includes(u.subject)).map(u=>u.id));
assert.equal(core.size,96);assert.ok(courseReadiness(catalog,core).complete);
const access=(id,extra={})=>moduleAccess({catalog,unit:catalog.units.find(u=>u.id===id),...extra});
assert.equal(access('math-1').allowed,true);
assert.equal(access('math-2').allowed,false);
assert.equal(access('math-2').previous.id,'math-1');
assert.equal(access('math-2',{done:new Set(['math-1'])}).allowed,true);
assert.equal(access('math-3',{done:new Set(['math-1'])}).allowed,false);
assert.equal(access('math-8',{starting:{complete:true,levels:{math:8}}}).allowed,true);
assert.equal(access('math-9',{starting:{complete:true,levels:{math:8}}}).allowed,false);
assert.equal(access('math-2',{local:{'math-2':{phase:0}}}).allowed,false,'Opening an old card alone does not unlock it.');
assert.equal(access('math-9',{local:{'math-9':{phase:2}}}).allowed,true,'Existing work remains resumable.');
assert.equal(access('reading-2',{done:new Set(['math-1'])}).allowed,false,'Another subject cannot unlock the next reading module.');
assert.equal(access('math-prices').allowed,false);
assert.equal(access('math-prices',{done:new Set(['math-cash'])}).allowed,false);
assert.equal(access('math-prices',{done:new Set(['math-5'])}).allowed,false,'Estimating totals comes before comparing prices.');
assert.equal(access('math-prices',{done:new Set(['math-estimate'])}).allowed,true);
assert.equal(access('reading-2',{done:new Set(['reading-1'])}).allowed,false);assert.equal(access('reading-2',{done:new Set(['writing-1'])}).allowed,true);
assert.equal(access('pc-files').allowed,false);
assert.equal(access('pc-files',{done:new Set([...core,'pc-start'])}).allowed,false,'Typing basics now come before managing files.');
assert.equal(access('pc-files',{done:new Set([...core,'typing-edit'])}).allowed,true);
assert.equal(access('pc-files',{local:{'pc-files':{phase:2}}}).allowed,false,'Saved work cannot bypass the first-four-course gate.');
assert.equal(access('typing-edit',{done:new Set([...core,'typing-words'])}).allowed,true);
const baseline=JSON.stringify(catalog);
for(const u of catalog.units){
  const status=access(u.id);
  if(!status.allowed)assert.ok(status.reason==='core-courses'||status.previous?.ready);
}
assert.equal(JSON.stringify(catalog),baseline,'Access checks do not alter curriculum data.');
console.log('Sequential access, starting suggestions, saved work and independent course progression passed.');

assert.equal(access('math-2',{starting:{complete:true,levels:{math:8}},local:{'math-1':{phase:2}}}).allowed,false,'Choosing an earlier starting module keeps subsequent modules sequential.');
assert.equal(access('math-8',{starting:{complete:true,levels:{math:8}},local:{'math-1':{phase:2}}}).allowed,false);
assert.equal(nextCourseUnit({catalog,unit:catalog.units.find(u=>u.id==='math-1'),done:new Set(['math-1']),starting:{complete:true,levels:{math:8}}}).id,'math-2');

const allActive=new Set(catalog.units.filter(u=>u.ready&&u.active!==false).map(u=>u.id));
assert.equal(nextFoundationUnit({catalog,plan,done:allActive}),null,'Completing every active module does not suggest a completed module.');
assert.equal(nextFoundationUnit({catalog,plan,subject:'digital',done:allActive}),null,'A completed course has no unfinished next module.');
const unfinished=new Set(allActive);unfinished.delete('digital-6');
assert.equal(next({subject:'digital',done:unfinished}),'digital-6','An unfinished earlier module remains available after a later review.');
assert.equal(next({done:allActive,local:{'digital-5':{phase:2}}}),'digital-5','An intentional unfinished replay remains resumable.');
