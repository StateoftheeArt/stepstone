import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {publicDemoRequest,sampleDemoCheck} from './dist/public-demo.js';
import {correct} from './dist/engine.js';
import {activeUnits} from './dist/curriculum.js';
const catalog=JSON.parse(await fs.readFile('dist/catalog.json','utf8'));
const bank=JSON.parse(await fs.readFile('dist/preview-checks.json','utf8'));
const units=activeUnits(catalog);
assert.equal(units.length,144);
let checks=0, answers=0;
for(const unit of units)for(let round=0;round<5;round++){
  const check=await publicDemoRequest('/api/preview-check',{unit:unit.id},catalog,async()=>bank);
  assert.equal(check.questions.length,6,unit.id);
  assert.equal(new Set(check.questions.map(q=>q.caseId||q.prompt)).size,6,unit.id);
  assert.equal(new Set(check.questions.map(q=>q.id)).size,6,unit.id);
  assert.equal(check.remotePreview,false);
  for(const lesson of [1,2])if(bank[unit.id].some(q=>q.lesson===lesson))assert(check.questions.some(q=>q.lesson===lesson),unit.id);
  const skills=unit.checkSkills||['calculate','apply','reason'];
  for(const skill of skills)assert.equal(check.questions.filter(q=>q.skill===skill).length,6/skills.length,unit.id+':'+skill);
  for(const q of check.questions){assert(correct(q,String(q.answer)),unit.id+':'+q.id);answers++;}
  checks++;
}
await assert.rejects(publicDemoRequest('/api/me',{},catalog),e=>e.status===401);
await assert.rejects(publicDemoRequest('/api/join',{alias:'Test',code:'not-real'},catalog),/connected learner-and-mentor/);
await assert.rejects(publicDemoRequest('/api/preview-check',{unit:'missing'},catalog,async()=>bank),/not ready/);
const health=await publicDemoRequest('/api/health',{},catalog);
assert.equal(health.desktop,false);
assert.equal(health.softVoice,false);
const source='..';
for(const [original,copy] of [['public/catalog.json','dist/catalog.json'],['content/checkpoints.json','dist/preview-checks.json']]){
 const a=await fs.readFile(source+'/'+original), b=await fs.readFile(copy);assert(a.equals(b),copy);
}
const outcome={modules:units.length,sampledChecks:checks,answersVerified:answers,distinctCases:true,skillAndLessonCoverage:true,lessonAndAnswerBytesUnchanged:true,accountRequestsUnavailable:true};
console.log(JSON.stringify(outcome));
