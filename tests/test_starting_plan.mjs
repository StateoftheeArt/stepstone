import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {hasStartedLearning,startingPlanMarkup,homeMarkup} from '../public/home.js';
import {createTutorial} from '../public/tutorial.js';
import {freshTour,evaluateTour,tourRoute} from '../public/tutorial-state.js';

const catalog=JSON.parse(readFileSync(new URL('../public/catalog.json',import.meta.url)));
const config=JSON.parse(readFileSync(new URL('../public/tutorial.json',import.meta.url)));
const next=catalog.units.find(u=>u.id==='math-1');
const result={complete:true,levels:Object.fromEntries(catalog.subjects.map(s=>[s.id,1]))};
assert.equal(hasStartedLearning({local:{'math-8':{phase:0}}}),false,'Browsing an introduction does not dismiss the plan.');
for(const local of [{'math-1':{phase:0,startedFromPlan:true}},{'math-1':{phase:2}},{'math-1':{phase:7,result:{passed:true}}}]){
  assert.equal(hasStartedLearning({local:JSON.parse(JSON.stringify(local))}),true,'A saved launch or existing learning hides the first-start card.');
}
assert.equal(hasStartedLearning({me:{attempts:[{unit:'math-1'}]}}),true);
const plan=startingPlanMarkup({catalog,result,next});
const home=homeMarkup({catalog,next,done:new Set(),html:String,startingPlan:plan});
assert.ok(home.indexOf('Your starting plan')<home.indexOf('Subjects'));
assert.ok(!home.includes('resume-card'),'The plan owns the first action, without a competing module-start card.');
assert.match(plan,/data-action="start-plan" data-unit="math-1"/);
assert.equal(startingPlanMarkup({catalog,result:{complete:false},next}),'');
const finalPlan=startingPlanMarkup({catalog,result,next,guide:true,action:'finish'});
assert.match(finalPlan,/data-tour="finish"/);
assert.ok(!finalPlan.includes('Suggestions for other subjects'),'The final handoff has one primary choice.');
assert.equal(tourRoute('finish'),'#home');

globalThis.ResizeObserver=class {observe(){} disconnect(){}};
globalThis.MutationObserver=class {observe(){}};
globalThis.cancelAnimationFrame=()=>{};
globalThis.document={addEventListener(){},hidden:false};
globalThis.window={removeEventListener(){}};
const storage=new Map();
let storageUnavailable=false;
globalThis.localStorage={setItem:(k,v)=>{if(storageUnavailable)throw Error('Synthetic storage failure.');storage.set(k,v);},getItem:k=>storage.get(k)};

function fixture({connected=false,offline=false}={}){
  let unavailable=offline,starts=0;
  const navigations=[];
  const me=connected?{id:'synthetic-plan-owner',welcomeAwards:{starting:true},tutorial:null}:null;
  const tour=createTutorial({root:{querySelector:()=>null},dialog:{addEventListener(){}},
    me:()=>me,guestOwner:()=> 'synthetic-plan-guest',route:()=> 'home',starting:()=>result,
    readButton:()=>'',guidePet(){},remember(){},toast(){},motion:()=>false,
    navigate:hash=>navigations.push(hash),beginPlan:()=>starts++,refreshAccount:async()=>me,
    api:async(_path,{data,revision})=>{
      if(unavailable)throw Error('Synthetic offline test.');
      const clean=evaluateTour(config,data),remote={...clean,revision:revision+1};
      if(clean.result.complete)me.welcomeAwards.tutorial=true;
      return remote;
    }});
  tour.configure(config);
  const events=config.setupActions.slice(0,config.setupActions.indexOf('goal')).map(action=>({action,
    ...(action==='pack'?{value:7}:action==='answer'?{value:'3'}:action==='mentor'?{value:'device'}:{})}));
  tour.adopt({revision:0,data:{...freshTour(),events},awards:{starting:true,tutorial:false}});
  return {tour,navigations,starts:()=>starts,reconnect:()=>{unavailable=false;}};
}

for(const connected of [false,true]){
  const f=fixture({connected});
  await f.tour.goalSaved('card-exchange');
  assert.equal(f.tour.stage(),'finish');
  assert.equal(f.tour.done(),false,'Saving a goal must leave the final plan click to the learner.');
  assert.equal(f.starts(),0);
  assert.equal(f.tour.bonus(),5);
  assert.equal(f.navigations.at(-1),'#home');
  await Promise.all([f.tour.action('finish'),f.tour.action('finish')]);
  assert.equal(f.tour.done(),true);
  assert.equal(f.starts(),1,'Two clicks produce one launch.');
  assert.equal(f.tour.bonus(),10);
  await f.tour.action('finish');
  assert.equal(f.starts(),1);
  f.tour.stop();
}
const offline=fixture({connected:true,offline:true});
await offline.tour.goalSaved('card-exchange');
await offline.tour.action('finish');
assert.equal(offline.starts(),0,'An unsaved connected tour cannot launch a lesson.');
assert.equal(offline.tour.locked(),true);
offline.reconnect();await offline.tour.action('sync');
assert.equal(offline.starts(),1);
assert.equal(offline.tour.locked(),false);
offline.tour.stop();
const localRetry=fixture();
await localRetry.tour.goalSaved('card-exchange');storageUnavailable=true;
await localRetry.tour.action('finish');assert.equal(localRetry.starts(),0);
storageUnavailable=false;await localRetry.tour.action('finish');
assert.equal(localRetry.starts(),1,'A temporary local-save failure can be retried at the final plan.');
assert.equal(localRetry.tour.bonus(),10);
localRetry.tour.stop();
console.log('Home plan visibility, final guide click, exactly-once launch and reconnect recovery passed.');
