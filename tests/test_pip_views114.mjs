import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {COMPANIONS,companionSprite} from '../public/companion.js';
import {pipArtwork} from '../public/pip-art.js';
import {pipProfileArtwork,PIP_PROFILE_ANCHORS} from '../public/pip-profile-art.js';
import {PIP_PERSONALITIES} from '../public/pip-personalities.js';
import {configureProfile,profilePreview,validateProfile} from '../public/profile.js';
import {homeShelf,pipFoodControls} from '../public/pip-editor.js';
import {coinSceneMarkup,mountLessonGame} from '../public/lesson-games.js';

const options=JSON.parse(fs.readFileSync(new URL('../public/profile-options.json',import.meta.url)));
configureProfile(options);
const silhouettes=new Set();
for(const c of COMPANIONS){
  const side=pipProfileArtwork(c.id),anchor=PIP_PROFILE_ANCHORS[c.id];
  assert.notEqual(side,pipArtwork(c.id),c.id+' needs a genuine side silhouette.');
  assert.ok(!silhouettes.has(side),c.id+' keeps its own silhouette.');silhouettes.add(side);
  assert.match(side,new RegExp(PIP_PERSONALITIES[c.id].part.slice(1)),c.id+' retains its animated part.');
  assert.ok(Object.values(anchor).every(n=>Number.isFinite(n)&&n>0&&n<64));
  const room=companionSprite(c.id,112,'none',{walkingViews:true});
  assert.equal((room.match(/data-pip-view=/g)||[]).length,3);
  assert.match(room,/data-pip-view="left" transform="translate\(64 0\) scale\(-1 1\)"/);
  assert.doesNotMatch(companionSprite(c.id,48),/data-pip-view/,'Small portraits remain front facing.');
}
assert.equal(silhouettes.size,28);

const empty=Object.fromEntries(Object.entries(options.home).map(([key,list])=>[key,list.find(c=>c.id==='none')?'none':list[0].id]));
const shelf=homeShelf(options.home,{home:empty});
assert.doesNotMatch(shelf,/data-home-value="none"/);
for(const field of ['rug','furniture','decor','painting','shelf','curtains']){
  assert.match(shelf,new RegExp('name="home_'+field+'" value="none"'));
}
assert.match(shelf,/Choose curtains/);
const value={alias:'Pip',avatar:'snail',accessory:'none',badge:'plain',accent:'mint',motivation:'confidence',interests:[],nextWin:'',home:empty};
assert.equal(validateProfile(value,false).home.curtains,'none','Putting curtains back remains a valid saved profile.');
assert.doesNotMatch(profilePreview(value),/data-placed-item="curtains"/);
assert.match(profilePreview({...value,home:{...empty,curtains:'linen'}}),/data-placed-item="curtains"/);
assert.match(pipFoodControls(null),/class="sr-only" data-pip-status role="status"/,'Interaction feedback remains available to screen readers.');

const catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url)));
const coinTask=catalog.units.find(u=>u.id==='math-cash').mission.labs.flat().find(t=>t.game?.kind==='count');
const state={selected:[0],coins:[100],answer:'1.00'},before=JSON.stringify(state),host={};
let saves=0;
mountLessonGame({host,game:coinTask.game,state,html:s=>s,save:()=>saves++});
assert.equal((host.innerHTML.match(/data-cad="1-dollar"/g)||[]).length,2);
assert.equal((host.innerHTML.match(/data-cad="25-cents"/g)||[]).length,3);
assert.match(host.innerHTML,/cad-loonie-value119\.svg/);assert.match(host.innerHTML,/cad-quarter-value119\.svg/);
assert.doesNotMatch(host.innerHTML,/<button|game-tally|2\.75|Tap each/);
assert.equal(JSON.stringify(state),before,'Opening the image preserves existing answer and game drafts.');assert.equal(saves,0);
assert.equal(coinSceneMarkup({kind:'count',unit:'hours',parts:[{value:1}]}),'','Other counting activities keep their interaction.');

// Execute the actual result renderer with disposable completion data.
const app=fs.readFileSync(new URL('../public/app.js',import.meta.url),'utf8');
const renderer=app.slice(app.indexOf('function resultView('),app.indexOf('function sourceDate('));
const sandbox={pending:[],local:{},me:null,catalog:{},guestScope:'preview',profileUnlocks:()=>[],checkpointCompletion:()=>({}),checkpointQueue:{peek:()=>null,take:()=>null},nextCourseUnit:()=>({id:'math-2',title:'Count the stock'}),nextFoundationUnit:()=>null,passed:()=>new Set(),startResult:()=>null,currentFoundation:()=>null,currentProfile:()=>({}),currentFood:()=>null,checkpointMarkup:()=>'',esc:s=>s,html:s=>s,button:(label,action)=>`<button data-action="${action}">${label}</button>`};
vm.createContext(sandbox);vm.runInContext(renderer,sandbox);
const result={};sandbox.resultView({id:'math-1'},{result:{passed:true,score:6,questions:[]},preview:true},result);
assert.doesNotMatch(result.innerHTML,/data-action="again"|More practice/);
assert.match(result.innerHTML,/Next module: Count the stock/);assert.match(result.innerHTML,/Done for now/);
sandbox.resultView({id:'math-1'},{result:{passed:false,score:3,questions:[]},preview:true},result);
assert.match(result.innerHTML,/Go over the lesson/);assert.match(result.innerHTML,/Try a new check/);
console.log('PASS: 28 genuine side views, signature parts, front portraits, empty menu removal, curtain removal state, accessible feedback, Canadian coin image counts, unchanged drafts and safe completion controls.');
