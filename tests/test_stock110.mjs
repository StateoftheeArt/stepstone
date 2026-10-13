import assert from 'node:assert/strict';
import fs from 'node:fs';
import {stockModelMarkup,stockTakeMarkup,stockDiagram} from '../public/stock-visual.js';
import {lessonVisualMarkup,mountLessonVisual} from '../public/lesson-visual.js';
import {mountScenario,scenarioState,scenarioCorrect} from '../public/mission-lab.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url))),unit=catalog.units.find(u=>u.id==='math-2');
const count=(s,pattern)=>(s.match(pattern)||[]).length;
assert.equal(count(stockModelMarkup({tens:4,ones:2}),/class="stock-label"/g),42,'Every label is visible, including ten inside each bundle.');
assert.doesNotMatch(stockModelMarkup({tens:4,ones:2}),/<output>|\b42\b/,'A read question does not print its answer.');
assert.match(stockModelMarkup({tens:2,ones:14,released:10},{total:true}),/<output>34<\/output>/);
assert.equal(count(stockModelMarkup({tens:2,ones:14,released:10}),/is-released/g),10);
for(const bad of [null,'bad',[999,-1,0,0]])assert.doesNotMatch(stockTakeMarkup({tens:2,ones:14},bad),/NaN|undefined/);
const taken=stockTakeMarkup({tens:2,ones:14},[0,1,2,3,4,5,6,7]);
assert.equal(count(taken,/data-stock-pick=/g),14);assert.equal(count(taken,/aria-pressed="true"/g),8);assert.match(taken,/6 loose labels/);assert.doesNotMatch(taken,/<output>|\b26\b/);
for(const mode of ['stock','trade'])for(let i=0;i<3;i++)assert.doesNotMatch(stockDiagram(mode,i),/NaN|undefined/);
assert.equal(count(stockDiagram('trade',0),/data-stock-bundle/g),3);assert.equal(count(stockDiagram('trade',1),/data-stock-bundle/g),2);assert.match(stockDiagram('trade',1),/20 \+ 14 = 34/);assert.match(stockDiagram('trade',2),/Order: 8 labels/);
const markup=lessonVisualMarkup(unit);for(const mode of ['stock','money','trade'])assert.match(markup,new RegExp('data-example-mode="'+mode+'"'));

const original={setTimeout,clearTimeout,document:globalThis.document};const timers=new Map(),listeners=new Map();let next=0,animated=true;
globalThis.setTimeout=fn=>{timers.set(++next,fn);return next;};globalThis.clearTimeout=id=>timers.delete(id);
globalThis.document={hidden:false,addEventListener:(k,f)=>listeners.set(k,f),removeEventListener:(k,f)=>{if(listeners.get(k)===f)listeners.delete(k);}};
function node(){return {dataset:{},value:'',hidden:false,attributes:{},setAttribute(k,v){this.attributes[k]=v;},focus(){this.focused=true;},addEventListener(k,fn){this[k]=fn;}};}
try{
 const fields={},buttons=['stock','money','trade'].map(mode=>({...node(),dataset:{exampleMode:mode}}));
 const host={dataset:{},querySelector:s=>fields[s]??=node(),querySelectorAll:()=>buttons,addEventListener(k,fn){this[k]=fn;}};
 const mounted=mountLessonVisual(host,unit,s=>s,()=>animated);
 const click=(key,value)=>host.click({target:{closest:s=>s==='['+key+']'?{dataset:{[key.replace('data-','').replace(/-([a-z])/g,(_,s)=>s.toUpperCase())]:value}}:null}});
 click('data-example-action','play');assert.equal(timers.size,1);click('data-example-mode','money');assert.equal(timers.size,0,'Switching examples stops the previous player.');assert.match(fields['[data-example-stage]'].innerHTML,/data-cad="10-dollars"/);assert.equal(fields['[data-example-count]'].textContent,'1 / 3');
 click('data-example-action','next');assert.match(fields['[data-example-stage]'].innerHTML,/data-cad="1-dollar"/);
 click('data-example-mode','trade');assert.match(fields['[data-example-stage]'].innerHTML,/3 bundles/);click('data-example-action','next');assert.match(fields['[data-example-stage]'].innerHTML,/20 \+ 14 = 34/);
 click('data-example-action','play');document.hidden=true;listeners.get('visibilitychange')();assert.equal(timers.size,0);document.hidden=false;animated=false;click('data-example-action','play');assert.equal(timers.size,0);mounted.dispose();assert.equal(listeners.size,0);

 // Minimal host fixture invokes the actual mission event handlers and grading.
 function scenarioHost(){
  const h={nodes:[],inner:''};
  Object.defineProperty(h,'innerHTML',{get:()=>h.inner,set(value){h.inner=value;h.nodes=[];for(const match of value.matchAll(/<(button|input)[^>]*>/g)){const n=node();for(const a of match[0].matchAll(/([\w-]+)="([^"]*)"/g)){if(a[1].startsWith('data-'))n.dataset[a[1].slice(5).replace(/-([a-z])/g,(_,s)=>s.toUpperCase())]=a[2];else n.attributes[a[1]]=a[2];}for(const attr of match[0].matchAll(/\s(data-[\w-]+)(?=[\s>])/g))n.dataset[attr[1].slice(5).replace(/-([a-z])/g,(_,s)=>s.toUpperCase())]='';h.nodes.push(n);}for(const cls of ['.hint','.scenario-feedback','[data-mission-success]'])h.nodes.push({...node(),selector:cls});}});
  const match=(n,s)=>n.selector===s||s==='input'&&Object.hasOwn(n.dataset,'scenarioAnswer')||[...s.matchAll(/\[([\w-]+)(?:="?([^\]"]+)"?)?\]/g)].every(a=>{const key=a[1].replace('data-','').replace(/-([a-z])/g,(_,s)=>s.toUpperCase());return Object.hasOwn(n.dataset,key)&&(a[2]===undefined||n.dataset[key]===a[2]);})&&s.startsWith('[');
  h.querySelector=s=>h.nodes.find(n=>match(n,s))||null;h.querySelectorAll=s=>h.nodes.filter(n=>match(n,s));return h;
 }
 let saved=0,correct=0;const draft={};const make=phase=>{const host=scenarioHost();mountScenario({host,u:unit,phase,draft,save:()=>saved++,html:s=>s,readButton:()=>'',onEdit:()=>{},onCorrect:()=>correct++});return host;};
 let h=make(1);
 for(let i=0;i<2;i++)h.querySelector('[data-adjust="tens"][data-delta="1"]').onclick();
 for(let i=0;i<4;i++)h.querySelector('[data-adjust="ones"][data-delta="1"]').onclick();
 h.querySelector('[data-scenario="check"]').onclick();assert.equal(correct,1);assert.equal(scenarioState(unit,1,draft).work.checked,true);
 h.querySelector('[data-scenario="stock-reset"]').click();assert.deepEqual(scenarioState(unit,1,draft).work.values,{tens:0,ones:0});assert.equal(scenarioState(unit,1,draft).work.checked,false);
 draft.scenarioLab[1].cursor=1;h=make(1);assert.match(h.inner,/four closed bundles/);assert.doesNotMatch(h.inner,/<output>42/);
 h=make(2);h.querySelector('[data-scenario="trade"]').click();assert.deepEqual(scenarioState(unit,2,draft).work.values,{tens:2,ones:14});assert.equal(scenarioCorrect(scenarioState(unit,2,draft).task,scenarioState(unit,2,draft).work),true);assert.match(h.inner,/<output>34/);
 h.querySelector('[data-scenario="trade"]').click();assert.equal(scenarioCorrect(scenarioState(unit,2,draft).task,scenarioState(unit,2,draft).work),false);h.querySelector('[data-scenario="stock-reset"]').click();assert.deepEqual(scenarioState(unit,2,draft).work.values,{tens:3,ones:4});
 draft.scenarioLab[2].cursor=1;h=make(2);
 for(let i=0;i<8;i++)h.querySelector('[data-stock-pick="'+i+'"]').onclick();
 assert.equal(scenarioState(unit,2,draft).work.stockTaken.length,8);assert.match(h.inner,/8 of 8/);assert.match(h.inner,/6 loose labels/);assert.equal(scenarioState(unit,2,draft).work.answer,'','The interactive tray never writes the answer.');
 const restored=JSON.parse(JSON.stringify(draft));assert.deepEqual(restored.scenarioLab[2].tasks['stock-take'].stockTaken,[0,1,2,3,4,5,6,7]);
 h.querySelector('[data-stock-pick="0"]').onclick();assert.match(h.inner,/7 of 8/);
 const input=h.querySelector('[data-scenario-answer]');input.value='26';input.oninput();h.querySelector('[data-scenario="check"]').onclick();assert.equal(correct,2,'The established numeric grading remains unchanged.');assert.ok(saved>20);
 console.log('PASS: visible label counts, conserved regrouping, answer-free working tray, reversible controls, saved draft continuity, unchanged grading, and stock/money/trade playback cleanup.');
}finally{Object.assign(globalThis,original);}
