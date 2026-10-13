import assert from 'node:assert/strict';
import fs from 'node:fs';
import {pcAction,pcState,pcComplete} from '../public/pc-lab.js';
import {nextFoundationUnit} from '../public/foundation.js';
import {devicePanel,mentorDevice} from '../public/device-work.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url))),bank=JSON.parse(fs.readFileSync(new URL('../content/checkpoints.json',import.meta.url)));
const units=catalog.units.filter(u=>u.course==='pc');assert.equal(units.length,5);
for(const u of units){
 assert.equal(u.deviceTask.steps.length,3);assert.equal(u.lessons.length,2);
 const cases=u.id==='pc-recover'?18:12;
 assert.deepEqual(u.checkSkills,['interpret','apply','reason']);assert.equal(bank[u.id].length,cases);
 assert.equal(new Set(bank[u.id].map(q=>q.prompt)).size,cases);
 assert.deepEqual([...new Set(bank[u.id].map(q=>q.lesson))].sort(),[1,2]);
 assert.ok(!bank[u.id].some(q=>u.practice.some(p=>p.prompt===q.prompt)));
 for(const task of u.mission.labs.flat().filter(t=>t.kind==='pc')){
  const work={};pcState(task,work);assert.equal(pcComplete(task,work),false);
  assert.equal(pcAction(task,work,1),false);assert.equal(work.pc.step,0);assert.ok(work.pc.message);
  for(let i=0;i<task.screens.length;i++){if(task.screens[i].move){assert.equal(pcAction(task,work,0),false);work.pc.moved=true;}if(task.screens[i].contextMenu){assert.equal(pcAction(task,work,0),false);work.pc.menu=true;}assert.equal(pcAction(task,work,0),true);const resumed=JSON.parse(JSON.stringify(work));assert.equal(resumed.pc.step,i+1);}
  assert.equal(pcComplete(task,work),true);assert.equal(pcAction(task,work,0),false);
 }
}
const save=units[1].mission.labs[0][0],work={};pcState(save,work);work.pc.text='';assert.equal(pcAction(save,work,0),false);work.pc.text='Fictional oats';
for(let i=0;i<save.screens.length;i++)pcAction(save,work,0);assert.equal(work.pc.saved,'Fictional oats');
const plan=JSON.parse(fs.readFileSync(new URL('../public/foundation.json',import.meta.url))),done=new Set(catalog.units.filter(u=>u.active!==false&&u.pathVersion===2&&['math','reading','science','life'].includes(u.subject)).map(u=>u.id));
assert.equal(nextFoundationUnit({catalog,plan,done}).id,'pc-start');
assert.match(devicePanel(units[0],{deviceWork:[{unit:'pc-start',status:'practised',note:'<script>oops</script>'}]}),/&lt;script&gt;/);
assert.match(mentorDevice({id:'fake',deviceWork:[]},catalog),/0 of 5/);
console.log('PC simulations: all branches, save/reopen, resume, 5-unit content, next action and evidence labels passed.');
