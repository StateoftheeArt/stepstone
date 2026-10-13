import assert from 'node:assert/strict';
import {INTERFACE_BUILD} from '../public/release.js';
const {COMPANIONS,companionSprite}=await import('../public/companion.js?build='+INTERFACE_BUILD);
const {pipDance,playPipAction,stopAllPipActions}=await import('../public/pip-moves.js?build='+INTERFACE_BUILD);
const {PIP_ROOM_PERSONALITIES,roomFloor,roomPoint,nextRoomActivity,createPipRoomLife}=await import('../public/pip-room.js?build='+INTERFACE_BUILD);

assert.deepEqual(Object.keys(PIP_ROOM_PERSONALITIES),COMPANIONS.map(p=>p.id));
assert.equal(new Set(Object.values(PIP_ROOM_PERSONALITIES).map(p=>[p.gait,p.speed,p.beat].join(':'))).size,28);
for(const {id} of COMPANIONS){
 const dances=[1,2,3].map(n=>pipDance(id,n));
 assert.equal(new Set(dances.map(d=>JSON.stringify(d.body))).size,3,id+' has three genuinely different dance paths');
 assert.equal(new Set(dances.map(d=>d.label)).size,3,id+' has three readable dance names');
}
for(const geometry of [{},{width:300,height:190,petWidth:90,petHeight:100},{width:640,height:310},{width:80,height:80}]){
 const floor=roomFloor(geometry);
 for(const point of [{x:-100,y:10},{x:NaN,y:Infinity},{x:.5,y:.83}]){
  const safe=roomPoint(point,floor);assert.ok(safe.x>=floor.left&&safe.x<=floor.right&&safe.y>=floor.back&&safe.y<=floor.front);
 }
}
const placed=[{kind:'rug',id:'round',key:'rug',x:.5,y:.8},{kind:'decor',id:'plant',key:'decor',x:.8,y:.6},{kind:'furniture',id:'none',key:'absent',x:.2,y:.7}];
for(const {id} of COMPANIONS)for(const value of [0,.2,.5,.81,.9,1,NaN]){
 const plan=nextRoomActivity({species:id,items:placed,previous:'rug',random:()=>value});
 assert.ok(Number.isFinite(plan.point.x)&&Number.isFinite(plan.point.y));
 assert.notEqual(plan.item?.key,'rug');assert.notEqual(plan.item?.id,'none');
}
const empty=nextRoomActivity({items:[],position:{x:.49,y:.87},random:()=>.5});
assert.ok(Math.abs(empty.point.x-.49)>.08,'An empty room still offers a visible wandering destination.');

const originals={setTimeout,clearTimeout,getComputedStyle:globalThis.getComputedStyle,document:globalThis.document,MutationObserver:globalThis.MutationObserver,localStorage:globalThis.localStorage};
let clock=0,nextId=0,animated=true;const timers=new Map(),events=new Map();
globalThis.setTimeout=(fn,ms)=>{timers.set(++nextId,{at:clock+ms,fn});return nextId;};
globalThis.clearTimeout=id=>timers.delete(id);
function advance(ms){const end=clock+ms;for(let guard=0;guard<1000;guard++){const task=[...timers].sort((a,b)=>a[1].at-b[1].at)[0];if(!task||task[1].at>end)break;timers.delete(task[0]);clock=task[1].at;task[1].fn();}clock=end;}
const node=()=>({dataset:{},style:{},isConnected:true,attributes:{},animations:[],setAttribute(k,v){this.attributes[k]=v;},append(){},remove(){this.isConnected=false;},animate(frames,options){const animation={frames,options,started:clock,cancelled:false,cancel(){this.cancelled=true;}};this.animations.push(animation);return animation;}});
function makeRoom(species='snail'){
 const dialog={open:true},stage=node(),status=node();stage.style.left='50%';stage.style.bottom='13%';
 stage.getBoundingClientRect=()=>({width:112,height:125});
 const parts={'.sprite-body':node()};for(const m of companionSprite(species).matchAll(/class="(sprite-[^"]+)"/g))for(const key of m[1].split(/\s+/))parts['.'+key]=node();
 const views=Object.fromEntries(['left','right'].map(direction=>[direction,Object.fromEntries(Object.keys(parts).map(key=>[key,node()]))]));
 const button=node();button.attributes['aria-label']='Move Round rug. Drag to the bin or press Delete to put it back.';button.getAttribute=k=>button.attributes[k];
 const rug={...node(),dataset:{placedKind:'rug',placedId:'round'},getBoundingClientRect:()=>({left:55,top:230,width:140,height:50}),querySelector:()=>button};
 const studio={querySelector:selector=>selector==='[data-pip-status]'?status:null};
 const room={...node(),dataset:{species,pipResting:'true',pose:'resting'},dialog,stage,status,parts,views,button,rug,classList:{contains:()=>false},closest:selector=>selector==='dialog'?dialog:selector==='.pip-studio'?studio:null,getClientRects:()=>dialog.open?[{}]:[],getBoundingClientRect:()=>({left:0,top:0,width:500,height:310}),querySelectorAll:()=>[rug],querySelector(selector){const direction=selector.match(/^\[data-pip-view="(left|right)"\]$/)?.[1];if(direction)return {querySelector:s=>views[direction][s]||null};return selector==='.pip-home-stage'?stage:parts[selector]||null;}};
 return room;
}
let rooms=[];
const document={hidden:false,documentElement:{},querySelectorAll:()=>rooms,createElement:()=>node(),addEventListener(type,fn){const all=events.get(type)||[];all.push(fn);events.set(type,all);},removeEventListener(type,fn){events.set(type,(events.get(type)||[]).filter(f=>f!==fn));}};
globalThis.document=document;
globalThis.localStorage=new Proxy({}, {get(){throw Error('Room life must not touch saved learning or inventory.');}});
globalThis.getComputedStyle=stage=>{
 const active=stage.animations.findLast(a=>!a.cancelled&&'left' in a.frames[0]);
 let x=parseFloat(stage.style.left),bottom=parseFloat(stage.style.bottom);
 if(active){const fraction=Math.min(1,(clock-active.started)/active.options.duration),a=active.frames[0],b=active.frames.at(-1);x=parseFloat(a.left)+(parseFloat(b.left)-parseFloat(a.left))*fraction;bottom=parseFloat(a.bottom)+(parseFloat(b.bottom)-parseFloat(a.bottom))*fraction;}
 return {left:x/100*500+'px',bottom:bottom/100*310+'px'};
};
let observer;globalThis.MutationObserver=class{constructor(fn){this.fn=fn;observer=this;}observe(){}disconnect(){this.disconnected=true;}};
try{
 const a=makeRoom(),b=makeRoom('badger');rooms=[a,b];
 const life=createPipRoomLife({root:document,motion:()=>animated,name:()=> 'North',random:()=>0});
 assert.equal(timers.size,2,'Each visible room owns one scheduling timer.');
 advance(901);assert.equal(a.dataset.pipRoomState,'walking');assert.equal(b.dataset.pipRoomState,'walking');
 assert.equal(a.views[a.stage.dataset.pipFacing]['.sprite-ears'].animations.length,1,'Walking animates the visible snail profile.');
 assert.equal(a.parts['.sprite-ears'].animations.length,0,'Walking leaves the hidden front portrait alone.');
 assert.equal(a.views[a.stage.dataset.pipFacing]['.sprite-body'].animations.length,1,'Weight shifts animate the visible side body.');
 assert.equal(a.parts['.sprite-body'].animations.length,0,'Hidden front bodies do not walk.');
 const visible=b.views[b.stage.dataset.pipFacing],frontPaw=visible['.sprite-foot-front'].animations.at(-1),backPaw=visible['.sprite-foot-back'].animations.at(-1);
 assert.ok(frontPaw&&backPaw,'The Badger takes individual alternating steps.');
 assert.notDeepEqual(frontPaw.frames,backPaw.frames,'Both paws must not slide together.');
 assert.equal(frontPaw.frames.at(-1).transform,'none','A stride finishes with a planted paw.');
 const snailWalk=a.stage.animations.at(-1),badgerWalk=b.stage.animations.at(-1);assert.ok(snailWalk.options.duration>badgerWalk.options.duration,'The snail actually travels slower than the Badger.');
 advance(200);const location=globalThis.getComputedStyle(a.stage).left;
 life.pause(a);assert.equal(snailWalk.cancelled,true);assert.ok(Math.abs(parseFloat(a.stage.style.left)/100*500-parseFloat(location))<.001,'A click or drag stops at the current position without teleporting.');
 assert.equal(a.dataset.pipRoomState,'paused');advance(6000);assert.equal(a.stage.animations.length,1,'A held item drag keeps roaming paused.');
 life.resume(a,50);advance(55);assert.equal(a.dataset.pipRoomState,'walking');
 advance(15000);assert.ok(a.button.animations.length,'A placed item responds to a random visit.');assert.equal(a.status.attributes['aria-live'],'off','Ambient visits do not repeatedly interrupt screen-reader users.');
 life.pause(a,3400);playPipAction(a,'snail',{dance:2,name:'North'});assert.equal(a.dataset.dance,'2');assert.equal(a.status.attributes['aria-live'],'polite');
 const clickTimerCount=timers.size;assert.ok(clickTimerCount>=2);a.dialog.open=false;observer.fn();assert.equal(a.dataset.pipRoomState,undefined);assert.equal(a.dataset.pipInteracting,undefined,'Closing the room cancels a dance too.');
 assert.equal(b.dataset.pipRoomState!==undefined,true,'Closing one room does not stop another.');
 b.isConnected=false;observer.fn();assert.equal(timers.size,0,'Removed previews leave no animation or scheduling timers.');
 a.dialog.open=true;rooms=[a];life.sync();advance(901);animated=false;observer.fn();assert.equal(timers.size,0,'Quiet visuals immediately cancel wandering and item responses.');
 assert.equal(a.dataset.pipRoomState,undefined);animated=true;life.sync();assert.equal(timers.size,1);document.hidden=true;for(const fn of events.get('visibilitychange')||[])fn();assert.equal(timers.size,0,'Hidden pages stop their room timers.');
 document.hidden=false;life.sync();assert.equal(timers.size,1);life.dispose();assert.equal(timers.size,0);assert.equal(observer.disconnected,true);stopAllPipActions();
 console.log('PASS: 28 individual roaming profiles, three distinct dances per Pip, floor bounds, empty rooms, real item reactions, interruption without teleporting, independent rooms, quiet mode and lifecycle cleanup.');
}finally{Object.assign(globalThis,originals);}
