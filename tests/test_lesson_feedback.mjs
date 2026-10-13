import assert from 'node:assert/strict';
import {createLessonAdvance,ANSWER_PAUSE_MS} from '../public/lesson-feedback.js';

function clock(){
  let time=0,id=0;const tasks=new Map();
  return {now:()=>time,setTimer:(fn,delay)=>{tasks.set(++id,{at:time+delay,fn});return id},clearTimer:id=>tasks.delete(id),
    advance(ms){const until=time+ms;while(true){const entry=[...tasks].sort((a,b)=>a[1].at-b[1].at)[0];if(!entry||entry[1].at>until)break;time=entry[1].at;tasks.delete(entry[0]);entry[1].fn();}time=until;},count:()=>tasks.size};
}
assert.equal(ANSWER_PAUSE_MS,8000);
{
  const c=clock(),flow=createLessonAdvance(c);let calls=0;
  flow.schedule(()=>true,()=>calls++);c.advance(7999);assert.equal(calls,0);
  c.advance(1);assert.equal(calls,1);c.advance(8000);assert.equal(calls,1);assert.equal(c.count(),0);
}
{
  const c=clock(),flow=createLessonAdvance(c);let calls=0;
  flow.schedule(()=>true,()=>calls++);c.advance(3000);flow.cancel();c.advance(16000);
  assert.equal(calls,0);assert.equal(c.count(),0);
}
{
  const c=clock(),flow=createLessonAdvance(c);let calls=0,valid=true;
  flow.schedule(()=>valid,()=>calls++);c.advance(3000);valid=false;c.advance(100);
  valid=true;c.advance(10000);assert.equal(calls,0);assert.equal(c.count(),0);
}
{
  const c=clock(),flow=createLessonAdvance(c);let old=0,fresh=0;
  flow.schedule(()=>true,()=>old++);c.advance(5000);flow.schedule(()=>true,()=>fresh++);
  c.advance(7999);assert.equal(old,0);assert.equal(fresh,0);c.advance(1);assert.equal(fresh,1);
}
console.log('PASS: eight-second delay, exactly-once advance, Stop, invalidated answer/page, and replacement countdown.');
