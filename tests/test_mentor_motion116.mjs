import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {COMPANIONS,companionSprite} from '../public/companion.js';
import {pipGait,pipTravelFrames} from '../public/pip-room.js';
import {pipProfileArtwork} from '../public/pip-profile-art.js';
import {pipDance} from '../public/pip-moves.js';
import {configureProfile,profilePreview} from '../public/profile.js';
import {learnerSpace,managerNavigation} from '../public/manager.js';

for(const {id} of COMPANIONS)for(const duration of [1300,7500,14000]){
 const gait=pipGait(id,{duration});
 assert.ok(Number.isInteger(gait.cycles)&&gait.cycles>0);
 assert.ok(Math.abs(gait.beat*gait.cycles-duration)<.001,'Each trip finishes its final stride.');
 for(const part of ['body','front','back']){
  if(id==='rock'&&part!=='body')continue;
  assert.equal(gait[part][0].transform,'none');
  assert.equal(gait[part].at(-1).transform,'none');
  assert.ok(gait[part].every(f=>!f.transform.includes('NaN')));
 }
 if(id!=='rock')assert.notDeepEqual(gait.front,gait.back,id+' has alternating footfalls.');
 const drawing='<g class="sprite-body">'+pipProfileArtwork(id)+'</g>',targets=new Set();
 for(const track of gait.parts){
  const group=[...drawing.matchAll(/<g\b[^>]*class="([^"]*)"[^>]*>/g)].find(m=>m[1].split(/\s+/).includes(track.selector.slice(1)));
  assert.ok(group,id+' walks using an existing '+track.selector);
  assert.ok(!targets.has(group.index),id+' must not apply competing gait animations to the same SVG group');targets.add(group.index);
  assert.equal(track.frames[0].transform,'none');assert.equal(track.frames.at(-1).transform,'none');
  assert.ok(track.frames.some(f=>f.transform!=='none'));
 }
 if(id==='rock'){
  assert.deepEqual(gait.parts.map(p=>p.selector),['.sprite-body']);
  assert.doesNotMatch(JSON.stringify(gait.parts),/scale|skew/,'The rock stays rigid while travelling.');
  for(const dance of [1,2,3])assert.doesNotMatch(pipDance(id,dance).body.join(' '),/scale|skew/,'Dancing cannot squash a rock.');
 }else assert.ok(gait.parts.length>=3,id+' moves individual parts as well as its body.');
 if(['bunny','frog','dog','squirrel'].includes(id))for(const paw of ['front','back'])assert.ok(gait.parts.some(p=>p.selector==='.sprite-foot-'+paw),'Hops and bounds fold and extend both legs.');
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
console.log('PASS: 28 gait profiles with existing non-competing articulated parts, folding hops, rigid rock dances/travel, planted stride endpoints, gentle travel, centred default carpet and preserved moved items.');
