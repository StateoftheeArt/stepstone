import assert from 'node:assert/strict';
import fs from 'node:fs';
import {configureProfile,profileForm,profilePreview,validateProfile} from '../public/profile.js';
import {COMPANIONS,companionSprite} from '../public/companion.js';
import {PIP_ACTIONS} from '../public/pip-moves.js';
import {pipItemIcon} from '../public/pip-items.js';
import {lessonWords} from '../public/lesson-words.js';
import {activeUnits,suggestedStart} from '../public/curriculum.js';
const options=JSON.parse(fs.readFileSync(new URL('../public/profile-options.json',import.meta.url))),catalog=JSON.parse(fs.readFileSync(new URL('../public/catalog.json',import.meta.url))),bank=JSON.parse(fs.readFileSync(new URL('../public/starting-point.json',import.meta.url)));
configureProfile(options);
assert.equal(options.accessories.length,26);assert.equal(Object.values(options.home).flat().length,56);
for(const c of COMPANIONS){assert.ok(PIP_ACTIONS[c.id]);for(const a of options.accessories){const art=companionSprite(c.id,64,a.id);assert.ok(!art.includes('undefined'));if(a.id!=='none')assert.ok(art.includes('sprite-accessory'),c.id+':'+a.id+' needs accessory art');}}
assert.equal(new Set(Object.values(PIP_ACTIONS).map(a=>a.frames.join('|'))).size,28);
for(const [kind,items] of Object.entries(options.home))for(const item of items)if(item.id!=='none')assert.match(pipItemIcon('home.'+kind+':'+item.id),/pip-item-art/);
const form=profileForm({editor:true,profile:{alias:'Mochi',avatar:'octopus',accessory:'sprout'},completed:2});
assert.match(form,/pip-shelf-scroll/);assert.match(form,/pip-shelf-group/);assert.doesNotMatch(form,/Say hello|>Dance<|One portion lasts/);assert.match(form,/data-species="octopus"/);
assert.match(profilePreview({avatar:'cat',home:{wall:'night'}},null),/data-pose="resting"/);
const profile={alias:'Mochi',avatar:'cat',accessory:'none',badge:'plain',accent:'mint',motivation:'confidence',interests:[],nextWin:''};
assert.throws(()=>validateProfile({...profile,accessory:'crown'},true,profile,75),/76/);assert.equal(validateProfile({...profile,accessory:'crown'},true,profile,76).accessory,'crown');
assert.deepEqual(catalog.subjects.map(s=>s.id),['math','reading','science','life','digital','work']);
for(const subject of catalog.subjects){assert.equal(activeUnits(catalog,subject.id).length,24);const id=bank.extended.suggestions[subject.id][3];assert.equal(suggestedStart(catalog,subject.id,{version:4,complete:true,suggestions:{[subject.id]:id}}).id,id);}
for(const unit of activeUnits(catalog)){assert.equal(unit.languageStage,unit.sequence<=8?'foundation':unit.sequence<=16?'apply':'extend');if(unit.terms?.length)assert.match(lessonWords(unit),/Words in this lesson/);}
assert.doesNotMatch(JSON.stringify(catalog.units.find(u=>u.id==='math-12')),/derivative|instantaneous|integral/);
assert.ok(!catalog.units.find(u=>u.id==='math-11').terms.some(t=>t.term==='SIN'),'Mathematical sine must not be defined as a Social Insurance Number.');
assert.match(catalog.units.find(u=>u.id==='life-boundaries').terms.find(t=>t.term==='pressure').meaning,/persuade/);
assert.match(catalog.units.find(u=>u.id==='work-stock').terms.find(t=>t.term==='folder').meaning,/papers/);
assert.equal(catalog.units.find(u=>u.id==='writing-2').terms.length,0,'Common words in a scenario should not create irrelevant early glossary clutter.');
const worker=fs.readFileSync(new URL('../public/sw.js',import.meta.url),'utf8');
const shell=fs.readFileSync(new URL('../public/index.html',import.meta.url),'utf8');
const release=shell.match(/app\.js\?build=(\d+)/)?.[1];
assert.ok(release,'The app shell must identify its asset release.');
for(const name of ['pip-items.js','pip-moves.js','lesson-words.js','starting-replay.js','refinements.css'])assert.ok(worker.includes('./'+name+'?build='+release),name+' must be available offline for the app shell release.');
console.log('PASS: six ordered courses, staged language, useful word help, 26 accessory options, all 28 actions and locked-item rules.');
