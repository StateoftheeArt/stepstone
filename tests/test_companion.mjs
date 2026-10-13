import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {COMPANIONS,companionSprite,createCompanion,safePetPosition} from '../public/companion.js';
import {configureProfile,validateProfile,profileForm,profileAccent} from '../public/profile.js';
import {messageInbox} from '../public/mentor-messages.js';

const options=JSON.parse(readFileSync(new URL('../public/profile-options.json',import.meta.url)));
configureProfile(options);
for(const a of options.accents)assert.equal(profileAccent(a.id),a.id);
assert.equal(profileAccent('unknown'),'mint');
assert.ok(!profileForm({connected:true}).includes('profile-locked'));
assert.ok(!profileForm({connected:true}).includes('Companion accessory'));
assert.ok(!profileForm({connected:true}).includes('Companion dock'));
assert.deepEqual(COMPANIONS.map(c=>c.id),options.companions);
const value={alias:'North',avatar:'axolotl',companionName:'Mochi',accessory:'none',badge:'plain',accent:'mint',motivation:'confidence',interests:[],nextWin:''};
assert.equal(validateProfile(value,false),value);
assert.throws(()=>validateProfile({...value,accessory:'scarf'},false),/Pass 16/);
assert.equal(validateProfile({...value,badge:'aurora'},false).badge,'aurora');
for(const accent of options.accents)assert.equal(validateProfile({...value,accent:accent.id},false,{},0).accent,accent.id,'Every interface colour is available before any modules.');
assert.ok(!profileForm({connected:false,completed:0}).includes('profile-theme-choices'));
assert.equal(options.accents.length,16,'All sixteen interface colours are freely selectable.');
assert.equal(validateProfile({...value,accessory:'headphones',badge:'sunset'},true,{},48).accessory,'headphones');
assert.throws(()=>validateProfile({...value,alias:'x'.repeat(13)}),/12/);
assert.throws(()=>validateProfile({...value,companionName:'x'.repeat(13)}),/12/);
assert.equal(validateProfile({...value,alias:'x'.repeat(12),companionName:'x'.repeat(12)}).alias.length,12);
const legacy={...value,alias:'Alexandria Macintosh',companionName:'Pip the explorer'};
assert.equal(validateProfile({...legacy,accent:'violet'},true,legacy).companionName,legacy.companionName);
assert.throws(()=>validateProfile({...legacy,alias:legacy.alias+'!'},true,legacy),/12/);
assert.throws(()=>validateProfile({...legacy,companionName:legacy.companionName+'!'},true,legacy),/12/);
assert.match(profileForm(),/name="alias"[^>]+maxlength="12"/);
assert.ok(!profileForm().includes('name="companionName"'));
assert.throws(()=>validateProfile({...value,avatar:'unknown'}),error=>error.field==='avatar');
assert.match(profileForm({intro:true,profile:{...value,alias:'<img src=x>',companionName:'" onfocus="bad'}}),/&lt;img src=x&gt;/);
assert.ok(!profileForm({intro:true,profile:{...value,alias:'<img src=x>'}}).includes('<img src=x>'));
assert.match(messageInbox([{id:'test',alias:'<img src=x>',unread:1,total:1}]),/&lt;img src=x&gt;/);
assert.ok(!companionSprite('" onload="bad').includes('onload'));
assert.ok(!companionSprite('fox','" onload="bad').includes('onload'));
assert.deepEqual(safePetPosition({x:-100,y:1000},{width:320,height:600}),{x:8,y:528});
const buttonBounds={left:80,top:80,right:200,bottom:180};
const clear=safePetPosition({x:90,y:90},{width:320,height:600},[buttonBounds]);
assert.ok(clear.x+72<=buttonBounds.left||clear.x>=buttonBounds.right+8||clear.y+72<=buttonBounds.top||clear.y>=buttonBounds.bottom+8);
assert.equal(safePetPosition({x:20,y:20},{width:50,height:50}),null);
assert.equal(safePetPosition({x:20,y:20},{width:320,height:600},[{left:0,top:0,right:320,bottom:600}]),null);
assert.equal(safePetPosition({x:NaN,y:20},{width:320,height:600}),null);
const css=readFileSync(new URL('../public/companion.css',import.meta.url),'utf8');
for(const c of COMPANIONS)for(const dance of [1,2,3])assert.ok(css.includes(`data-species=${c.id}][data-dance="${dance}"]`),`${c.label} dance ${dance} is present`);

let now=10000,nextId=0,animated=true,visible=true;
const timers=new Map(),events=new Map(),nodes={};
function el(){const classes=new Set();return {dataset:{},listeners:{},hidden:false,textContent:'',style:{removeProperty(k){delete this[k];}},classList:{add(...keys){keys.forEach(k=>classes.add(k));},remove(...keys){keys.forEach(k=>classes.delete(k));},contains:k=>classes.has(k)},getBoundingClientRect(){const left=parseFloat(this.style.left)||20,top=parseFloat(this.style.top)||20;return {left,top,right:left+64,bottom:top+64,width:64,height:64};},setAttribute(){},toggleAttribute(){},addEventListener(type,fn){this.listeners[type]=fn;},setPointerCapture(){},offsetWidth:1};}
const host=el();
host.querySelector=selector=>nodes[selector];
Object.defineProperty(host,'innerHTML',{set(value){host.markup=value;for(const s of ['.companion-pet','.companion-magnet','.companion-profile','[data-pip-note]'])nodes[s]=el();}});
let parent='profile';const profileSlot={append(){parent='profile';}};
globalThis.document={body:{append(){parent='body';}},querySelector:()=>profileSlot,querySelectorAll:()=>[],documentElement:{classList:{toggle(){}}},createElement:()=>host,addEventListener:(type,fn)=>events.set(type,fn),hidden:false};
globalThis.innerWidth=800;globalThis.innerHeight=600;globalThis.requestAnimationFrame=fn=>{fn();return 0;};
const positions=new Map(),positionStore={getItem:k=>positions.get(k)||null,setItem:(k,v)=>positions.set(k,v),removeItem:k=>positions.delete(k)};
const realSet=globalThis.setTimeout,realClear=globalThis.clearTimeout,realNow=Date.now;
globalThis.setTimeout=(fn,delay)=>{timers.set(++nextId,{at:now+delay,fn});return nextId;};
globalThis.clearTimeout=id=>timers.delete(id);Date.now=()=>now;
function advance(ms){const until=now+ms;for(;;){const task=[...timers].sort((a,b)=>a[1].at-b[1].at)[0];if(!task||task[1].at>until)break;timers.delete(task[0]);now=task[1].at;task[1].fn();}now=until;}
function click(){nodes['.companion-pet'].listeners.click();}
function pointer(type,x=100,y=100){nodes['.companion-pet'].listeners[type]({button:0,pointerId:1,clientX:x,clientY:y});}
try{
  let edits=0,identity='one',fed=true,loggedPlays=0;const companion=createCompanion({canPlay:()=>fed,onPlay:()=>loggedPlays++,profile:()=>value,ready:()=>visible,motion:()=>animated,edit:()=>edits++,owner:()=>identity,storage:()=>positionStore});companion.update();
  assert.equal(host.hidden,false);assert.match(host.markup,/North/);assert.ok(!host.markup.includes('Mochi'));
  for(let i=1;i<=12;i++){click();assert.equal(host.dataset.pose,'dance');assert.equal(host.dataset.dance,String((i-1)%3+1));advance(100);}
  companion.celebrate();assert.equal(host.dataset.pose,'dance');advance(1600);assert.equal(host.dataset.pose,'idle');
  click();assert.equal(host.dataset.pose,'inflate','Only the thirteenth tap starts inflation.');
  advance(1200);assert.equal(host.dataset.pose,'pop');advance(420);assert.equal(host.dataset.pose,'annoyed');advance(2200);assert.equal(host.dataset.pose,'idle');
  for(let i=0;i<13;i++)click();assert.equal(host.dataset.pose,'inflate','Another thirteen taps work immediately after recovery.');advance(3820);
  pointer('pointerdown');advance(3000);assert.equal(host.dataset.pose,'idle','Holding does not explode the companion.');pointer('pointerup');
  animated=false;companion.quiet();companion.celebrate();assert.equal(host.dataset.pose,'happy');advance(1600);for(let i=0;i<12;i++){click();assert.equal(host.dataset.pose,'happy');}
  click();assert.equal(host.dataset.pose,'still');advance(700);assert.equal(host.dataset.pose,'still');advance(420);assert.equal(host.dataset.pose,'annoyed');
  companion.quiet();assert.equal(host.dataset.pose,'idle');assert.equal(timers.size,0);
  animated=true;pointer('pointerdown');document.hidden=true;events.get('visibilitychange')();advance(4000);assert.equal(host.dataset.pose,'idle');assert.equal(timers.size,0);
  assert.ok(!host.markup.includes('companion-help'));nodes['.companion-profile'].listeners.click();assert.equal(edits,1);
  companion.dockIn({open:true,append(node){assert.equal(node,host);parent='dialog';}});assert.equal(parent,'dialog');
  companion.dockIn(null);assert.equal(parent,'profile');
  document.hidden=false;pointer('pointerdown');pointer('pointermove',260,180);pointer('pointerup');click();
  assert.equal(host.dataset.pose,'idle','Dragging must not count as a dance tap.');
  assert.ok(nodes['.companion-pet'].classList.contains('is-floating'));assert.ok(positions.has('stepstone-pip-position-v1-one'));
  const stored=JSON.parse(positions.get('stepstone-pip-position-v1-one'));assert.ok(stored.x>0&&stored.x<1);
  pointer('pointerdown');pointer('pointermove',300,200);pointer('pointercancel');assert.deepEqual(JSON.parse(positions.get('stepstone-pip-position-v1-one')),stored);
  identity='two';companion.update();assert.ok(!nodes['.companion-pet'].classList.contains('is-floating'),'Another learner does not inherit a pet position.');
  identity='one';companion.update();assert.ok(nodes['.companion-pet'].classList.contains('is-floating'));
  const previousPosition=positions.get('stepstone-pip-position-v1-one');
  let guideX=500;const guideSeat={isConnected:true,getClientRects:()=>[{}],getBoundingClientRect:()=>({left:guideX,top:220,width:64,height:64,bottom:284})};
  companion.followGuide(guideSeat,'first');assert.ok(nodes['.companion-pet'].classList.contains('is-guiding'));assert.equal(nodes['.companion-pet'].style.left,'500px');
  guideX=440;companion.followGuide(guideSeat,'first');assert.equal(nodes['.companion-pet'].style.left,'440px');assert.equal(positions.get('stepstone-pip-position-v1-one'),previousPosition,'Following guidance does not overwrite a saved position.');
  pointer('pointerdown',470,240);pointer('pointermove',400,340);pointer('pointercancel');assert.ok(nodes['.companion-pet'].classList.contains('is-guiding'),'Cancelling a guide drag restores its dialogue position.');assert.equal(positions.get('stepstone-pip-position-v1-one'),previousPosition);
  companion.followGuide(null);assert.ok(nodes['.companion-pet'].classList.contains('is-floating'));
  companion.followGuide(guideSeat,'first');nodes['.companion-magnet'].listeners.click();assert.equal(positions.has('stepstone-pip-position-v1-one'),false);assert.ok(!nodes['.companion-pet'].classList.contains('is-guiding'));
  companion.followGuide(guideSeat,'first');assert.ok(!nodes['.companion-pet'].classList.contains('is-guiding'),'Parking remains respected for the current guide step.');
  companion.followGuide(guideSeat,'second');assert.ok(nodes['.companion-pet'].classList.contains('is-guiding'));companion.followGuide(null);
  pointer('pointerdown');pointer('pointermove',260,180);pointer('pointerup');click();assert.equal(nodes['.companion-magnet'].hidden,false);
  pointer('pointerdown',280,200);pointer('pointermove',40,40);pointer('pointerup');click();assert.equal(positions.has('stepstone-pip-position-v1-one'),false,'Dropping onto the magnet parks the pet.');assert.equal(nodes['.companion-magnet'].hidden,true);
  nodes['.companion-pet'].listeners.keydown({key:'Home',preventDefault(){}});assert.ok(!nodes['.companion-pet'].classList.contains('is-floating'));
  fed=false;companion.update();assert.equal(host.dataset.pose,'resting');const playCount=loggedPlays;let blocked=false;nodes['.companion-pet'].listeners.keydown({key:'Enter',preventDefault(){blocked=true;}});assert.equal(blocked,false,'Enter remains available for a free greeting.');click();assert.equal(host.dataset.pose,'action');assert.equal(loggedPlays,playCount,'Resting greetings never count as daily active play.');companion.celebrate();pointer('pointerdown');pointer('pointermove',400,400);pointer('pointerup');assert.equal(host.dataset.pose,'resting','Empty bowl blocks playing, dragging and checkpoint dancing.');assert.equal(timers.size,0);fed=true;companion.update();click();assert.equal(host.dataset.pose,'dance','Feeding restores play.');companion.quiet();
  visible=false;companion.update();assert.equal(host.hidden,true);
}finally{globalThis.setTimeout=realSet;globalThis.clearTimeout=realClear;Date.now=realNow;delete globalThis.document;delete globalThis.innerWidth;delete globalThis.innerHeight;delete globalThis.requestAnimationFrame;}
console.log(`PASS: ${COMPANIONS.length} Pips with three dances, ${options.accents.length} colours, legacy profile validation, thirteen-tap pop, quiet motion, drag/cancel, magnet return and separate owners.`);
