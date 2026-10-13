import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const app=fs.readFileSync(new URL('../public/app.js',import.meta.url),'utf8');
const source=app.slice(app.indexOf('function revisitLesson('),app.indexOf('\nfunction ',app.indexOf('function revisitLesson(')+1));
let saved=0,destination='';
const previous={phase:7,rounds:{2:{answers:{old:'saved'},checks:{old:true}}},result:{passed:true,score:6,points:20},reflection:'My explanation',ink:[{x:1}],support:'person'};
const sibling={phase:2,rounds:{2:{answers:{q:'keep'}}}};
const sandbox={local:{one:structuredClone(previous),two:structuredClone(sibling)},pending:[],unit:id=>({id,ready:true}),passed:()=>new Set(['one']),draft(id){return this.local[id]??={};},resetMissionLabs(u,d){d.messageLab={};},saveLocal(){saved++;},navigate(hash){destination=hash;}};
// Bind draft to the disposable state rather than relying on a VM function's `this`.
sandbox.draft=id=>sandbox.local[id]??={};
vm.createContext(sandbox);vm.runInContext(source,sandbox);
sandbox.revisitLesson('one');
assert.equal(sandbox.local.one.phase,1);
assert.equal(Object.keys(sandbox.local.one.rounds).length,0);
for(const key of ['result','reflection','ink','support'])assert.deepEqual(sandbox.local.one[key],previous[key]);
assert.deepEqual(sandbox.local.two,sibling);
assert.equal(destination,'#lesson/one');assert.equal(saved,1);

for(const phase of [1,2,3,4,5,6]){
  sandbox.local.one={...structuredClone(previous),phase};const before=JSON.stringify(sandbox.local.one);
  sandbox.revisitLesson('one');assert.equal(JSON.stringify(sandbox.local.one),before,'An active retake must remain intact.');
}
sandbox.local.one=structuredClone(previous);sandbox.pending=[{unit:'one',id:'queued'}];
const before=JSON.stringify(sandbox.local.one);sandbox.revisitLesson('one');
assert.equal(JSON.stringify(sandbox.local.one),before,'Queued work must remain intact.');
assert.equal(saved,1);
console.log('PASS: completed lessons reopen practice; saved explanations, prior results, other modules, active retakes and queued reports remain intact.');
