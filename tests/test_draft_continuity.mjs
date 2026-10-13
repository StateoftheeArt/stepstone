import assert from 'node:assert/strict';
import {scenarioState} from '../public/mission-lab.js';
import {openPracticeExample,returnFromExample} from '../public/mission.js';
const u={mission:{labs:[[{id:'new',kind:'draft'}],[{id:'revise',kind:'draft',revise:true}]]}};
const draft={reflection:'Earlier unrelated calculation.'};
assert.equal(scenarioState(u,1,draft).work.text,'');
const first=scenarioState(u,1,draft).work;first.text='New message written by the learner.';
assert.equal(scenarioState(u,1,draft).work.text,first.text);
draft.reflection=first.text;
assert.equal(scenarioState(u,3,draft).work.text,first.text);
assert.equal(scenarioState(u,3,draft).work.baseline,first.text);
console.log('Independent drafts start empty; revisions and saved learner text are retained.');

for(const phase of [2,4]){
  const practice={phase,rounds:{[phase]:{cursor:1,questions:[{id:'q1'},{id:'q2'}],answers:{q2:'12'},checks:{q1:true}}}};
  const savedRound=JSON.stringify(practice.rounds);
  assert.equal(openPracticeExample(practice),true);
  assert.equal(practice.phase,phase-1);
  const reopened=JSON.parse(JSON.stringify(practice));
  assert.equal(returnFromExample(reopened),true);
  assert.equal(reopened.phase,phase);
  assert.equal(JSON.stringify(reopened.rounds),savedRound);
  assert.equal(reopened.examplePhase,null);
  assert.equal('exampleReturnPhase' in reopened,false);
}
const guided={phase:1,examplePhase:1};
assert.equal(returnFromExample(guided),false);
assert.equal(guided.phase,1);
const stale={phase:7,exampleReturnPhase:2};
assert.equal(returnFromExample(stale),false);
assert.equal(stale.phase,7);
assert.equal(openPracticeExample(stale),false);
console.log('Returning from a worked example preserves the practice question and answer, including after a reload; stale return markers cannot change a completed stage.');
