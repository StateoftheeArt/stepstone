import assert from 'node:assert/strict';
import fs from 'node:fs';
import {practiceRound,practicePool,questionKey} from '../public/lesson-questions.js';
import {canadianMoneyPiece,lessonSourceFooter} from '../public/canadian-money.js';
import {coinSceneMarkup,gameTotal} from '../public/lesson-games.js';
import {wireMoves,cancelMove} from '../public/touch-move.js';

const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const options=JSON.parse(fs.readFileSync(new URL('../public/profile-options.json',import.meta.url)));
assert.equal(options.accents.length,16);
assert.deepEqual(options.accents.slice(-4).map(a=>a.id),['plum','copper','olive','ice']);
assert.equal(new Set(options.accents.map(a=>a.id)).size,16);

// New rounds do not repeat a guided case or a question in the other practice round.
let questions=0,empty=0;
for(const unit of catalog.units.filter(u=>u.ready)){
  const guided=new Set((unit.mission?.labs||[]).flat().map(questionKey));
  const draft={rounds:{}};
  for(const phase of [2,4]){
    const pool=practicePool(unit,phase,draft),round=practiceRound(unit,phase,draft);
    assert.equal(new Set(pool.map(questionKey)).size,pool.length,unit.id);
    assert.ok(round.questions.length<=3);
    for(const q of round.questions)assert.ok(!guided.has(questionKey(q)),unit.id+' repeats guided question');
    if(!round.questions.length)empty++;
    questions+=round.questions.length;
    const saved=JSON.stringify(round);assert.strictEqual(practiceRound(unit,phase,draft),round);
    assert.equal(JSON.stringify(round),saved,'Reopening a saved round preserves its state');
  }
  const first=new Set(draft.rounds[2].questions.map(questionKey));
  for(const q of draft.rounds[4].questions)assert.ok(!first.has(questionKey(q)),unit.id);
}
assert.equal(empty,0,'Every module should have fresh practice beyond its guided cases.');
assert.equal(questions,catalog.units.filter(u=>u.ready).length*6);
const oldRound={questions:[{id:'old',prompt:'Existing saved case'}],answers:{old:'1'},checks:{old:true},tries:2};
assert.strictEqual(practiceRound({practice:[]},2,{rounds:{2:oldRound}}),oldRound);
assert.equal(questionKey({passage:'A plan.',prompt:'Where?'}),questionKey({prompt:'A plan. Where?'}));

const cashUnit=catalog.units.find(u=>u.id==='math-cash');
const cash=cashUnit.mission.labs.flat().find(t=>t.game?.kind==='cash').game;
for(const cents of cash.coins){
  const markup=canadianMoneyPiece(cents),file=markup.match(/src="\.\/(.*?)"/)[1];
  assert.ok(fs.statSync(new URL('../public/'+file,import.meta.url)).size>200);
  assert.match(markup,/alt="Canadian/);assert.match(markup,/draggable="false"/);
}
assert.throws(()=>canadianMoneyPiece(10),RangeError);
assert.equal(gameTotal(cash,{coins:[500,200,25]}),7.25);
const coinGame=cashUnit.mission.labs.flat().find(t=>t.game?.kind==='count').game;
assert.doesNotMatch(coinSceneMarkup(coinGame),/money-source|Museum/);
assert.match(lessonSourceFooter(cashUnit),/<footer.*Bank of Canada Museum.*<\/footer>/s);
assert.equal(lessonSourceFooter({id:'math-1'}),'');
assert.match(lessonSourceFooter({id:'reading-1'},'<details>Reading source</details>'),/<footer.*Reading source/);

// Exercise the pointer implementation: centred money ghost, one drop, cancellation,
// no drop outside the counter and suppression only of the drag's generated click.
const listeners=new Map(),classes={add(){},remove(){}};
const source={disabled:false,classList:classes,setPointerCapture(){},closest(){return this;}};
const destination={classList:classes,closest(){return this;}};
const host={addEventListener(name,fn){listeners.set(name,fn);},contains(el){return [source,destination].includes(el);}};
let hover=destination,removed=0,lastGhost=null,drops=0;
globalThis.window={addEventListener(){}};
globalThis.document={addEventListener(){},body:{append(){}},elementFromPoint(){return hover;},createElement(){return lastGhost={style:{},setAttribute(){},getBoundingClientRect(){return {width:72,height:72};},remove(){removed++;}};}};
wireMoves(host,{centerGhost:true,ghost:()=>canadianMoneyPiece(200),onDrop(){drops++;}});
const event=(x,y=120)=>({target:source,button:0,pointerId:1,clientX:x,clientY:y,preventDefault(){}});
listeners.get('pointerdown')(event(100));listeners.get('pointermove')(event(200));
assert.equal(lastGhost.style.transform,'translate(164px,84px)');assert.match(lastGhost.innerHTML,/toonie/);
listeners.get('pointerup')(event(200));assert.equal(drops,1);assert.equal(removed,1);
const generated={target:source,blocked:false,preventDefault(){this.blocked=true;},stopImmediatePropagation(){}};
listeners.get('click')(generated);assert.equal(generated.blocked,true);
listeners.get('pointerdown')(event(100));listeners.get('pointermove')(event(140));listeners.get('pointercancel')();
assert.equal(drops,1);assert.equal(removed,2);
listeners.get('pointerdown')(event(100));listeners.get('pointermove')(event(160));hover=null;
listeners.get('pointerup')(event(160));assert.equal(drops,1);assert.equal(removed,3);cancelMove();
console.log(`PASS: 16 colours; ${questions} distinct new practice questions across 153 modules; saved rounds intact; original Canadian-dollar value diagrams; footer sources; centred money drag/drop/cancel.`);
