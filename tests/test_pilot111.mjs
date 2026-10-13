import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {refreshMentorAccess,mentorAccess,roleEntry,spaceGuide,managerSettings} from '../public/manager.js';
import {mountScienceVisual} from '../public/science-model.js';
import {INTERFACE_BUILD} from '../public/release.js';

// Exercise the actual refresh functions with a minimal DOM, including autofill
// that updates values without dispatching an input event.
const source=fs.readFileSync(new URL('../public/app.js',import.meta.url),'utf8');
const functions=source.slice(source.indexOf('async function loadMentor(){'),source.indexOf('function managerPanelContent('));
const delayed=()=>{let resolve;const promise=new Promise(r=>resolve=r);return {promise,resolve};};
const nextTurn=()=>new Promise(resolve=>setImmediate(resolve));
function setup(mode='login',health={}){
 const fields=Object.fromEntries(['username','passphrase','device','name','confirm','recovery'].map(name=>[name,{value:'',selectionStart:2,selectionEnd:2,dataset:{},closest:()=>null}]));
 const claim={dataset:{mentorClaim:'false:false'},innerHTML:''};
 const form={dataset:{mode},fields,querySelector:s=>s==='[data-mentor-claim]'&&mode==='setup'?claim:null};
 const root={form,assignments:0,querySelector:s=>s==='form[data-form="mentor-auth"]'?root.form:null,querySelectorAll:()=>[]};
 Object.defineProperty(root,'innerHTML',{set(){root.assignments++;root.form=null;}});
 const ctx={root,health,mentor:null,me:{personal:true,id:'personal-learning'},entryRole:'mentor',route:'mentor',lastInvite:null,
  status(){},refreshMentorAccess,mentorAccess,spaceGuide,dialog:{open:false,dataset:{}},
  window:{scrollY:125,scrollTo(){}},document:{activeElement:fields.passphrase},CSS:{escape:s=>s},
  localStorage:{removed:[],removeItem(key){this.removed.push(key);}},toast(){},errorText:e=>e.message,
  esc:s=>s,button:()=>'',managerNavigation:()=>'',openManagerSection(){}};
 vm.createContext(ctx);vm.runInContext(functions,ctx);vm.runInContext(`mentorAuthMode='${mode}';`,ctx);
 return {ctx,root,form,fields,claim,load:()=>vm.runInContext('loadMentor()',ctx)};
}
const unauthorized=()=>Promise.reject({status:401,message:'Sign in'});
for(const mode of ['login','setup','recover']){
 const f=setup(mode),pending=delayed();
 f.ctx.api=path=>path==='/api/health'?Promise.resolve({localClaim:true,previousPassphrase:true}):path==='/api/mentor'?unauthorized():pending.promise;
 const loading=f.load();await nextTurn();
 f.fields.username.value='mentor-example';f.fields.passphrase.value='autofilled-private-example';f.fields.device.value='Personal laptop';
 f.fields.name.value='Example';f.fields.confirm.value='autofilled-private-example';f.fields.recovery.value='recovery-example';
 pending.resolve({ok:false});await loading;
 assert.equal(f.root.form,f.form,mode+' keeps its form nodes');
 assert.equal(f.root.assignments,0);assert.equal(f.fields.passphrase.value,'autofilled-private-example');
 assert.equal(f.fields.username.value,'mentor-example');assert.equal(f.fields.device.value,'Personal laptop');
 assert.equal(f.ctx.document.activeElement,f.fields.passphrase);assert.equal(f.fields.passphrase.selectionStart,2);
 assert.equal(f.ctx.me.id,'personal-learning','A signed-out refresh does not erase personal learning.');
 if(mode==='setup'){
  assert.match(f.claim.innerHTML,/Previous mentor passphrase/);
  f.claim.innerHTML='unchanged host claim values';refreshMentorAccess(f.root,mode,f.ctx.health);
  assert.equal(f.claim.innerHTML,'unchanged host claim values','Identical health leaves host-claim controls intact too.');
 }
 assert.equal(refreshMentorAccess(f.root,mode,{}, {pending:true}),false);
 assert.equal(refreshMentorAccess(f.root,mode==='setup'?'login':'setup'),false);
}
{
 const f=setup(),old=delayed();let calls=0;
 f.ctx.api=path=>path==='/api/health'?Promise.resolve({marker:++calls}):path==='/api/mentor'?unauthorized():calls===1?old.promise:Promise.resolve({ok:false});
 const stale=f.load();await nextTurn();
 await f.load();old.resolve({pending:true,code:'OLD',device:'Old request'});await stale;
 assert.equal(f.ctx.health.marker,2);assert.equal(f.root.assignments,0,'Older refresh cannot restore a pending-device screen.');
}
{
 const f=setup(),pending=delayed();
 f.ctx.api=path=>path==='/api/health'?Promise.resolve({}):path==='/api/mentor'?unauthorized():pending.promise;
 const loading=f.load();await nextTurn();
 vm.runInContext('mentorRefresh++;mentorAuthMode="recover";',f.ctx);
 pending.resolve({pending:true,code:'STALE',device:'Old device'});await loading;
 assert.equal(f.root.assignments,0,'Changing mode invalidates the previous refresh.');
}
{
 const f=setup();f.ctx.api=path=>Promise.resolve(path==='/api/health'?{}:{account:{name:'Mentor'}});
 await f.load();assert.equal(f.ctx.me.id,'personal-learning');assert.equal(f.ctx.localStorage.removed.length,0);
}
{
 const f=setup(),pending=delayed();let mentorCalls=0;
 f.ctx.api=path=>path==='/api/health'?Promise.resolve({}):path==='/api/mentor'?(++mentorCalls===1?unauthorized():Promise.resolve({account:{name:'Mentor'}})):pending.promise;
 const loading=f.load();await nextTurn();pending.resolve({ok:true});await loading;
 assert.equal(f.ctx.me,null,'A resumed approved device enters mentor space.');assert.equal(f.ctx.localStorage.removed.length,1);
}
assert.match(source,/action==='mentor-mode'\)\{mentorRefresh\+\+/);
assert.match(source,/kind==='mentor-auth'\)\{mentorRefresh\+\+/);

// Test native range IDs, their labels, and the real oninput redraw/save handler.
const ids=new Set();let controls=0;
const labels={3:['Food portions','Shelter places'],4:['Force in newtons','Mass in kilograms'],
 7:['Power in watts','Time in seconds'],10:['Reacting pairs (one A₂ and one B₂)'],
 11:['Voltage in volts','Resistance in ohms'],12:['Flow in litres per minute','Minutes']};
for(const [model,phase] of [[3,1],[4,1],[7,1],[10,1],[11,1],[12,1],[11,3]]){
 const nodes=new Map(),inputs=[],outputs=[],state={};let saved=0,markup='';
 const host={classList:{add(){}},querySelector:s=>{if(!nodes.has(s))nodes.set(s,{});return nodes.get(s);},
  querySelectorAll:s=>s==='[data-control]'?inputs:outputs};
 Object.defineProperty(host,'innerHTML',{set(value){markup=value;
  for(const m of value.matchAll(/<label class="field" for="([^"]+)"><span>([^<]+)<output for="([^"]+)" aria-hidden="true" data-out="([^"]+)"><\/output><\/span><input id="([^"]+)" type="range" data-control="([^"]+)" min="([^"]+)" max="([^"]+)" value="([^"]+)"><\/label>/g)){
   assert.equal(m[1],m[3]);assert.equal(m[1],m[5]);assert.equal(ids.has(m[1]),false);ids.add(m[1]);
   inputs.push({id:m[5],label:m[2].replace(/: $/,''),dataset:{control:m[6]},min:Number(m[7]),max:Number(m[8]),value:m[9]});
   outputs.push({dataset:{out:m[4]},textContent:''});
  }
 }});
 mountScienceVisual({host,model,phase,state,save:()=>saved++,html:s=>s});
 const expected=model===11&&phase===3?['Frequency (cycles per second)','Amplitude (illustrative units)']:labels[model];
 assert.deepEqual(inputs.map(i=>i.label),expected);controls+=inputs.length;
 for(const input of inputs){
  input.value=String(input.max);input.oninput();assert.equal(state[input.dataset.control],input.max);
  assert.equal(outputs.find(o=>o.dataset.out===input.dataset.control).textContent,input.max);
 }
 assert.equal(saved,inputs.length);assert.ok(nodes.get('#visual-value').innerHTML);assert.doesNotMatch(markup,/aria-label=""/);
}
assert.equal(controls,13);
const shell=fs.readFileSync(new URL('../public/index.html',import.meta.url),'utf8');
const expectedBuild=Number(shell.match(/app\.js\?build=(\d+)/)[1]);
assert.equal(INTERFACE_BUILD,expectedBuild);assert.ok(managerSettings({}).includes('Interface build '+expectedBuild));
assert.match(roleEntry(),/<\/strong> <span>/);assert.match(roleEntry(),/<\/span> <b>/);
assert.match(spaceGuide('mentor','Example'),/<\/strong> <span>/);
const sw=fs.readFileSync(new URL('../public/sw.js',import.meta.url),'utf8');assert.ok(sw.includes('release.js?build='+expectedBuild));
console.log('PASS: delayed/authofilled mentor forms, host claim updates, stale refresh fencing, personal learning, 13 named native ranges and input updates, text boundaries, generated build and cache. DOM fixtures; no live-browser claim.');
