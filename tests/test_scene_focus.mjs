import assert from 'node:assert/strict';
import fs from 'node:fs';
import {missionIntro,missionHeader,missionLesson} from '../public/mission.js';
import {scenarioCorrect} from '../public/mission-lab.js';
import {createTextFilter} from '../public/text-filter.js';
const release=fs.readFileSync(new URL('../public/index.html',import.meta.url),'utf8').match(/app\.js\?build=(\d+)/)[1];
const {configureLanguage,payloadAllowed,displayPayload,LANGUAGE_MESSAGE}=await import(`../public/language.js?build=${release}`);
import {escapeHTML} from '../public/engine.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const filter=createTextFilter(JSON.parse(fs.readFileSync(new URL('../public/text-filter.json',import.meta.url))));
configureLanguage(filter);
let units=0;
for(const u of catalog.units.filter(u=>u.ready)){
 const intro=missionIntro(u,()=>'<button>Read aloud</button>'),title=escapeHTML(u.goal);
 assert.equal(intro.split(title).length-1,1,u.id);
 assert.doesNotMatch(intro,/Work at your own pace|Useful first|six-question check|Write messages people can use|Try a changed situation/);
 for(let phase=0;phase<8;phase++){
  const header=missionHeader(u,phase);
  assert.doesNotMatch(header,/class="mission-header"|mission-emblem/);
  assert.match(header,/h1 class="sr-only"/);
  assert.match(header,/aria-label="Module sections"/);
 }
 const activity=missionLesson(u,1,s=>s,()=>'',{});
 assert.doesNotMatch(activity,/aria-label="Try the task"/);
 units++;
}
const task=catalog.units.find(u=>u.id==='writing-1').mission.labs[0].find(t=>t.kind==='draft');
const clean='Meet at the library at four. Please bring your notebook.';
assert.equal(scenarioCorrect(task,{text:clean,baseline:''}),true);
assert.equal(scenarioCorrect(task,{text:'  ',baseline:''}),false);
assert.equal(scenarioCorrect({...task,revise:true},{text:clean,baseline:clean}),false);
assert.equal(scenarioCorrect({...task,revise:true},{text:clean+' We will read together.',baseline:clean}),true);
const blocked=Buffer.from('ZnVjaw==','base64').toString();
assert.equal(scenarioCorrect(task,{text:blocked,baseline:''}),false);
for(const field of ['reflection','note','text','explanation','accessNote','backupNote','review_note'])assert.equal(payloadAllowed({data:{[field]:blocked}}),false,field);
assert.equal(payloadAllowed({answers:{q:blocked}}),false);
assert.equal(payloadAllowed({passphrase:blocked,code:blocked}),true);
assert.deepEqual(displayPayload({reflection:blocked,passphrase:blocked}),{reflection:'Text needs revision.',passphrase:blocked});
assert.deepEqual(displayPayload({questions:[{prompt:blocked,answer:blocked}]}),{questions:[{prompt:blocked,answer:'Text needs revision.'}]});
assert.equal(payloadAllowed({reflection:'The class meets in Scunthorpe. Bring a glass.'}),true);
const lab=fs.readFileSync(new URL('../public/mission-lab.js',import.meta.url),'utf8');
assert.doesNotMatch(lab,/selfChecks|data-scenario-selfcheck|Read your draft, then check|Try the task|Use made-up details|Nothing is sent outside/);
assert.ok(LANGUAGE_MESSAGE.length);
console.log(`PASS: ${units} module intros and 824 phase headers; writing saves without checkboxes, revisions and language boundaries.`);
