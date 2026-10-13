import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {COMPANIONS,companionSprite} from '../public/companion.js';
import {pipGait,pipTravelFrames} from '../public/pip-room.js';
import {configureProfile,profilePreview} from '../public/profile.js';
import {learnerSpace,managerNavigation} from '../public/manager.js';

for(const {id} of COMPANIONS)for(const duration of [1300,7500,14000]){
 const gait=pipGait(id,{duration});
 assert.ok(Number.isInteger(gait.cycles)&&gait.cycles>0);
 assert.ok(Math.abs(gait.beat*gait.cycles-duration)<.001,'Each trip finishes its final stride.');
 for(const part of ['body','front','back']){
  assert.equal(gait[part][0].transform,'none');
  assert.equal(gait[part].at(-1).transform,'none');
  assert.ok(gait[part].every(f=>!f.transform.includes('NaN')));
 }
 assert.notDeepEqual(gait.front,gait.back,id+' has alternating footfalls.');
}
for(const [from,to] of [[{x:.2,y:.75},{x:.8,y:.9}],[{x:.8,y:.9},{x:.2,y:.75}]]){
 const frames=pipTravelFrames(from,to,4000);
 assert.equal(frames[0].left,from.x*100+'%');
 assert.equal(frames.at(-1).left,to.x*100+'%');
 assert.equal(frames[0].offset,0);assert.equal(frames.at(-1).offset,1);
 assert.notEqual(frames[0].easing,'linear','The first step accelerates.');
 assert.notEqual(frames.at(-2).easing,'linear','The last step slows down.');
 for(let i=1;i<frames.length;i++)assert.ok(frames[i].offset>frames[i-1].offset);
 for(const frame of frames)assert.ok(parseFloat(frame.left)>=20&&parseFloat(frame.left)<=80);
}
const badger=companionSprite('badger',88,'none',{walkingViews:true});
assert.equal((badger.match(/class="sprite-body"/g)||[]).length,3,'Every facing owns its body motion.');
for(const part of ['front','back'])assert.equal((badger.match(new RegExp('class="sprite-foot-'+part+'"','g'))||[]).length,3);
configureProfile(JSON.parse(readFileSync(new URL('../public/profile-options.json',import.meta.url))));
assert.match(profilePreview(),/--item-x:50%;--item-y:84.5%/);
assert.match(profilePreview({homePositions:{rug:{x:.26,y:.86}}}),/--item-x:26%;--item-y:86%/,'A deliberately moved rug keeps its saved position.');
assert.match(learnerSpace(null),/class="learner-mentor-space" aria-labelledby="mentor-space-title"/);
assert.doesNotMatch(managerNavigation({}),/learner-mentor-space/,'The mentor management dashboard keeps its own layout.');
console.log('PASS: planted alternating footfalls for 28 Pips, complete stride timing, gentle travel endpoints, genuine facing bodies, centred default carpet and preserved moved items.');
