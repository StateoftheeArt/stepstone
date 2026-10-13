import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {continueSavedTour,evaluateTour,freshTour} from '../public/tutorial-state.js';
import {profileValues,profileForm,configureProfile,validateProfile,profileNameError,profilePreview,availableProfileExtras} from '../public/profile.js';
import {createTextFilter} from '../public/text-filter.js';
import {messageInbox} from '../public/mentor-messages.js';

const config=JSON.parse(readFileSync(new URL('../public/tutorial.json',import.meta.url)));
function saved(version,step){
  const actions=version===2?config.setupActions:config.actions;
  return {...freshTour(),version,events:actions.slice(0,step).map(action=>({action,...(action==='pack'?{value:7}:action==='answer'?{value:'3'}:action==='questions'?{value:'complete'}:action==='mentor'?{value:'device'}:action==='goal'?{value:'core-card-everyday'}:{})}))};
}
for(const version of [1,2]){
  const actions=version===2?config.setupActions:config.actions;
  const before=actions.indexOf('pause');
  for(const step of [before,before+1]){
    const original=saved(version,step),snapshot=JSON.stringify(original),continued=continueSavedTour(config,original);
    assert.equal(continued.events.length,before+2);
    assert.equal(evaluateTour(config,continued).result.step,before+2);
    assert.equal(JSON.stringify(original),snapshot,'Continuing does not mutate the saved input.');
  }
  for(const step of [0,before-1,before+2,actions.length]){
    const original=saved(version,step);
    assert.equal(continueSavedTour(config,original),original,'Normal steps and completed tours stay untouched.');
  }
}
configureProfile(JSON.parse(readFileSync(new URL('../public/profile-options.json',import.meta.url))),createTextFilter(JSON.parse(readFileSync(new URL('../public/text-filter.json',import.meta.url)))));
const OriginalFormData=globalThis.FormData;
globalThis.FormData=class {constructor(fields){this.fields=fields;}get(key){return this.fields[key]??null;}};
try {
  const previous={alias:'Alexandria Macintosh',companionName:'Pip the explorer',motivation:'confidence',interests:['reading'],nextWin:'Read a timetable'};
  const values=profileValues({alias:previous.alias,avatar:'turtle',accent:'violet'},previous);
  assert.equal(values.alias,previous.alias);
  assert.equal('companionName' in values,false);
  assert.equal(values.nextWin,previous.nextWin);
  assert.deepEqual(values.interests,previous.interests);
  assert.equal(validateProfile(values,true,previous),values,'Existing long names remain valid for unrelated changes.');
} finally {globalThis.FormData=OriginalFormData;}
const form=profileForm({editor:true});
assert.match(form,/id="profile-editor"/);
assert.equal((form.match(/<span>Pip name /g)||[]).length,1);
assert.match(form,/maxlength="12"/);
assert.match(form,/data-name-count>0\/12/);
assert.equal(profileNameError('Dickinson'),'');
assert.equal(profileNameError('N'.repeat(12)),'');
assert.match(profileNameError('N'.repeat(13)),/12 characters/);
const rejected=Buffer.from('ZWF0IGEgZGljaw==','base64').toString();
assert.ok(profileNameError(rejected));
assert.ok(profileNameError(rejected,rejected),'An existing blocked name still needs correction before saving.');
assert.ok(!profilePreview({alias:rejected,avatar:'fox'}).includes(rejected));
assert.match(profilePreview({alias:rejected,avatar:'fox'}),/Your Pip/);
assert.equal(profileNameError('Alexandria Macintosh','Alexandria Macintosh'),'');
for(const name of ['companionName','motivation','interests','nextWin'])assert.ok(!form.includes(`name="${name}"`));
assert.ok(!form.includes('type="submit"'),'The editor submits from the separate footer.');
const inbox=messageInbox([{id:'one',alias:'Sprout',unread:1,total:1}],[{id:'one',profile:{avatar:'turtle'}}]);
assert.match(inbox,/Sprout/);
assert.match(inbox,/data-species="turtle"/);
console.log('Profile identity and saved-tour continuity checks passed.');

const starter=profileForm({completed:0});
assert.ok(starter.includes('class="pip-card-dropdown"'));
assert.equal((starter.match(/type="radio" name="avatar"/g)||[]).length,28);
assert.ok(/data-home-value="lamp"[^>]*disabled/.test(starter));
const earned=profileForm({completed:6});
assert.ok(/data-home-value="lamp"/.test(earned));assert.ok(!/data-home-value="lamp"[^>]*disabled/.test(earned));
assert.ok(/data-home-value="chair"[^>]*disabled/.test(earned));
const room={wall:'sand',rug:'woven',furniture:'cushion',decor:'lamp'};
const identity={alias:'North',avatar:'fox',accent:'mint',accessory:'sprout',badge:'plain',motivation:'confidence',interests:[],nextWin:'',home:room};
assert.equal(validateProfile(identity,false,{},6),identity);
assert.throws(()=>validateProfile({...identity,home:{...room,furniture:'desk'}},false,{},6),/Pass 30/);
assert.match(profilePreview(identity),/data-room-wall="sand"/);
assert.match(profilePreview(identity),/data-room-rug="woven"/);
const connectedStarter=availableProfileExtras(identity,{},0);
assert.equal(connectedStarter.accessory,'none');
const starterHomeExtras={painting:'landscape',shelf:'books',bowl:'gold',curtains:'linen'};
assert.deepEqual(connectedStarter.home,{wall:'sand',rug:'round',furniture:'cushion',decor:'plant',...starterHomeExtras});
assert.equal(validateProfile(connectedStarter,true,{},0),connectedStarter,'Preview cosmetics cannot block joining a new account.');
const expandedIdentity={...identity,home:{...identity.home,...starterHomeExtras}};
assert.deepEqual(availableProfileExtras(identity,{},6),expandedIdentity,'Earned choices survive queued saves, with new starter home fields.');
assert.deepEqual(availableProfileExtras(identity,identity,0),expandedIdentity,'Legacy owned choices remain available, with new starter home fields.');
