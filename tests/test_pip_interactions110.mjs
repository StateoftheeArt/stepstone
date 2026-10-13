import assert from 'node:assert/strict';
import fs from 'node:fs';
import {COMPANIONS,companionSprite} from '../public/companion.js?build=110';
import {PIP_PERSONALITIES} from '../public/pip-personalities.js?build=110';
import {playPipAction,stopPipAction,stopAllPipActions,pipToyMarkup} from '../public/pip-moves.js?build=110';
import {installPipEditor,pipFoodControls,paintFood} from '../public/pip-editor.js?build=110';

const original={setTimeout,clearTimeout,document:globalThis.document};
const timers=new Map(),events=new Map();let next=0;
globalThis.setTimeout=(fn,delay)=>{timers.set(++next,{fn,delay});return next;};
globalThis.clearTimeout=id=>timers.delete(id);
const flush=()=>{for(const [id,t] of [...timers]){if(timers.has(id)){timers.delete(id);t.fn();}}};
function node(){return {dataset:{},style:{},textContent:'',attributes:{},animations:[],setAttribute(k,v){this.attributes[k]=v;},animate(frames,options){const a={frames,options,cancelled:false,cancel(){this.cancelled=true;}};this.animations.push(a);return a;},remove(){this.removed=true;}};}
function roomFor(species,resting=true){
 const art=companionSprite(species),parts={'.sprite-body':node()},status=node(),stage={children:[],append(n){this.children.push(n);}};
 for(const m of art.matchAll(/class="(sprite-[^"]+)"/g))for(const cls of m[1].split(/\s+/))parts['.'+cls]=node();
 return {dataset:{pose:resting?'resting':'idle',pipResting:String(resting)},style:{},parts,status,stage,classList:{toggle(){}},querySelector(s){return s==='[data-pip-status]'?status:s==='.pip-home-stage'?stage:parts[s]||null;},getAnimations(){throw Error('Must never cancel unrelated CSS animations');}};
}
let rooms=[];
globalThis.document={createElement:()=>node(),querySelectorAll:()=>rooms,addEventListener(type,fn){const all=events.get(type)||[];all.push(fn);events.set(type,all);}};
try{
 assert.deepEqual(Object.keys(PIP_PERSONALITIES),COMPANIONS.map(c=>c.id));
 assert.equal(new Set(Object.values(PIP_PERSONALITIES).map(p=>p.playLabel)).size,28,'Every Pip has an individual activity.');
 assert.equal(new Set(Object.values(PIP_PERSONALITIES).map(p=>p.toy)).size,28,'Each activity has its own prop.');
 for(const {id} of COMPANIONS){
  const p=PIP_PERSONALITIES[id],room=roomFor(id);rooms=[room];
  assert.ok(room.parts[p.part],id+' animates a real part of its approved drawing');
  assert.doesNotMatch(pipToyMarkup(p.toy),/undefined|NaN/);
  playPipAction(room,id,{interaction:'greet',name:'North'});
  assert.equal(room.dataset.pose,'action');assert.match(room.status.textContent,/^North /);
  assert.equal(room.parts[p.part].style.transformBox,'view-box','64px pivot coordinates use the drawing view box.');
  assert.ok(room.parts[p.part].animations.some(a=>a.frames.some(f=>f.transform!=='none')),id+' has a visible greeting');
  assert.equal(room.stage.children.length,0,'A greeting does not start an active game.');
  flush();assert.equal(room.dataset.pose,'resting');assert.equal(room.dataset.pipInteracting,undefined);
  room.dataset.pipResting='false';playPipAction(room,id,{interaction:'play'});
  const prop=room.stage.children.at(-1);assert.ok(prop?.innerHTML.includes('<svg'));
  assert.ok(room.parts['.sprite-body'].animations.at(-1).frames.some(f=>f.transform!=='none'));
  room.dataset.pipResting='true';flush();assert.equal(room.dataset.pose,'resting','Food expiry during play restores the resting state.');assert.equal(prop.removed,true);
  const count=Object.values(room.parts).reduce((n,p)=>n+p.animations.length,0);
  playPipAction(room,id,{motion:false});
  assert.equal(room.dataset.pose,'happy');assert.equal(Object.values(room.parts).reduce((n,p)=>n+p.animations.length,0),count,'Quiet feedback creates no animated frames.');
  stopPipAction(room);assert.equal(room.dataset.pose,'resting');assert.equal(timers.size,0);
 }
 const a=roomFor('dog',false),b=roomFor('snail',true);rooms=[a,b];
 playPipAction(a,'dog');const old=a.parts['.sprite-tail'].animations.at(-1),prop=a.stage.children.at(-1);
 playPipAction(a,'dog',{interaction:'greet'});assert.equal(old.cancelled,true);assert.equal(prop.removed,true);assert.equal(timers.size,1,'Repeating a tap replaces its previous timer.');
 playPipAction(b,'snail',{interaction:'greet'});assert.equal(timers.size,2);a.dataset.pipResting='true';b.dataset.pipResting='false';
 stopAllPipActions();assert.equal(timers.size,0);assert.equal(a.dataset.pose,'resting');assert.equal(b.dataset.pose,'idle');

 // Exercise the real delegated editor controls. Greetings cannot log a daily
 // play, grant food, or unlock active play when the bowl is empty.
 const room=roomFor('snail'),play=node(),feedButton=node(),meter=node(),time=node(),bank=node(),status=room.status;
 let fed=false,plays=0,feeds=0;const notices=[];
 const food=()=>({bank:fed?0:1,remaining:fed?1800:0,asOf:Date.now()/1000,capacity:5400});
 const form={querySelector(s){return ({'[data-home-room]':room,'.pip-home':room,'[name=alias]':{value:'North'},'[name=avatar]:checked':{value:'snail'},'[data-pip-play]':play,'[data-pip-feed]':feedButton,'[data-pip-status]':status,'[data-food-time]':time,'[data-food-meter]':meter,'[data-food-bank]':bank})[s]||null;},querySelectorAll(s){return s==='[data-pip-play]'?[play]:[];}};
 rooms=[room];
 const target=kind=>({...node(),closest(s){return s===kind?this:s==='form[data-form="profile"]'?form:null;}});
 installPipEditor({preview:()=>{},food,feed:async()=>{fed=true;feeds++;},motion:()=>true,toast:s=>notices.push(s),onPlay:()=>plays++});
 const click=async kind=>{for(const fn of events.get('click')||[])await fn({target:target(kind)});};
 await click('[data-pip-greet]');assert.equal(plays,0);assert.equal(feeds,0);assert.equal(room.dataset.dance,'1');assert.match(status.textContent,/North tries the shell sway/);flush();
 await click('[data-pip-greet]');assert.equal(room.dataset.dance,'2');flush();
 await click('[data-pip-greet]');assert.equal(room.dataset.dance,'3');flush();
 assert.equal(plays,0,'An empty-bowl cosmetic dance cannot count as active daily play.');
 await click('[data-pip-play]');assert.equal(plays,0);assert.equal(play.disabled,true);assert.equal(notices.at(-1),'Feed Pip to play.');
 await click('[data-pip-feed]');assert.equal(feeds,1);assert.equal(plays,0);assert.equal(play.disabled,false);flush();
 await click('[data-pip-play]');assert.equal(plays,1);assert.match(status.textContent,/North /);assert.match(play.textContent,/dewdrop/);
 fed=false;paintFood(form,food());assert.equal(room.dataset.pose,'action','Food refresh does not erase a response in progress.');flush();assert.equal(room.dataset.pose,'resting');
 assert.match(pipFoodControls(food(),{species:'snail',name:'<North>'}),/Tap &lt;North&gt;/);
 assert.match(pipFoodControls(food(),{species:'snail'}),/data-pip-play disabled/);
 const css=fs.readFileSync(new URL('../public/pip-life.css',import.meta.url),'utf8');
 assert.match(css,/prefers-reduced-motion:no-preference/);assert.match(css,/html:not\(\.quiet\)/);
 for(const {id} of COMPANIONS)assert.ok(css.includes('data-species='+id+']'),'Idle signature exists for '+id);
 fed=true;await click('[data-pip-play]');document.hidden=true;for(const fn of events.get('visibilitychange')||[])fn();assert.equal(timers.size,0,'Leaving the page cancels active response timers.');
 console.log('PASS: 28 individual greetings, activities and resting parts; owned-animation cleanup, food expiry, independent rooms, quiet motion and real editor food/play boundaries.');
}finally{Object.assign(globalThis,original);}
