import {activeUnits,suggestedStart,canonicalSubject} from './curriculum.js?build=123';
import {escapeHTML as esc} from './engine.js?build=123';

export function previewFoundation(plan) {
  const groups=plan.groups.map(group=>({...group,passed:[],completed:0,total:group.units.length}));
  return {...plan,groups,completed:0,total:groups.reduce((n,g)=>n+g.total,0),complete:false,next:groups[0].units[0]};
}

export function foundationIds(plan) {return plan.groups.flatMap(group=>group.units);}

const moduleGroup=u=>u.pathVersion===2?'path':u.course|| (u.guide?'guides':u.practical?'practical':'core');

export function courseReadiness(catalog,done=new Set()){
  const courses=['math','reading','science','life'].map(id=>{
    const units=activeUnits(catalog,id),completed=units.filter(u=>done.has(u.id)).length;
    return {id,title:catalog.subjects.find(s=>s.id===id)?.name||id,completed,total:units.length,complete:units.length>0&&completed===units.length};
  });
  return {courses,completed:courses.reduce((n,c)=>n+c.completed,0),total:courses.reduce((n,c)=>n+c.total,0),complete:courses.every(c=>c.complete)};
}
export const accessMessage=access=>access.message||`Pass ${access.previous?.title||'the previous module'} to unlock this module.`;
export function courseGateMarkup(catalog,done,subject){
  if(!['digital','work'].includes(subject))return '';
  const ready=courseReadiness(catalog,done);
  return `<section class="course-gate ${ready.complete?'is-complete':''}" aria-label="Course readiness"><div><h3>${ready.complete?'Your next two courses are open':'Complete your first four courses'}</h3><p>${ready.complete?'Digital skills comes next, followed by Work & jobs. You can now ask your mentor for the learning laptop, when funded.':'Pass all 24 modules in each course below to unlock Digital skills and Work & jobs, and ask for the learning laptop.'}</p></div><ul>${ready.courses.map(c=>`<li><a href="#path/${c.id}">${esc(c.title)}</a><span>${c.completed}/${c.total}${c.complete?' ✓':''}</span></li>`).join('')}</ul>${ready.complete?'<a class="btn small secondary" href="#progress/rewards">My laptop goal →</a>':''}</section>`;
}

export function moduleAccess({catalog,unit,done=new Set(),local={},starting=null,plan=null}){
  if(!unit?.ready)return {allowed:false};
  if(['digital','work'].includes(unit.subject)&&!courseReadiness(catalog,done).complete)return {allowed:false,reason:'core-courses',message:'Finish Money & math, Reading & writing, Science and Life skills to unlock this course.'};
  const started=id=>Boolean(local[id]&&(local[id].startedFromPlan||(local[id].phase??0)>0));
  if(done.has(unit.id)||started(unit.id))return {allowed:true};
  if(unit.legacy)return {allowed:!!plan&&foundationIds(plan).includes(unit.id),previous:activeUnits(catalog,unit.subject)[0]};
  const chain=unit.pathVersion===2?activeUnits(catalog,unit.subject):catalog.units.filter(u=>u.ready&&u.subject===unit.subject&&moduleGroup(u)===moduleGroup(unit));
  const index=chain.findIndex(u=>u.id===unit.id);
  let baseline=unit.pathVersion===2?Math.max(0,chain.findIndex(u=>u.id===suggestedStart(catalog,unit.subject,starting)?.id)):moduleGroup(unit)==='core'&&starting?.complete?Math.max(0,chain.findIndex(u=>u.grade>=(starting.levels[unit.subject]||1))):0;
  const evidence=chain.findIndex(u=>done.has(u.id)||started(u.id));
  if(evidence>=0)baseline=Math.min(baseline,evidence);
  if(index<=baseline)return {allowed:true};
  const previous=chain[index-1];
  return {allowed:done.has(previous.id),previous};
}

export function nextCourseUnit({catalog,unit,done=new Set(),local={},starting=null,plan=null}){
  const chain=activeUnits(catalog,unit.subject);
  const index=chain.findIndex(u=>u.id===unit.id);
  return chain.slice(index+1).find(u=>!done.has(u.id)&&moduleAccess({catalog,unit:u,done,local,starting,plan}).allowed)||null;
}

export function nextFoundationUnit({catalog,plan,local={},done=new Set(),starting=null,subject=null}) {
  const units=catalog.units.filter(u=>u.ready&&(u.active!==false||done.has(u.id)||local[u.id]||foundationIds(plan).includes(u.id))&&(!subject||u.subject===canonicalSubject(subject))&&moduleAccess({catalog,unit:u,done,local,starting,plan}).allowed);
  const active=units.filter(u=>local[u.id]&&(local[u.id].phase??0)<7).sort((a,b)=>(local[b.id].touchedAt||0)-(local[a.id].touchedAt||0))[0];
  if(active)return active;
  // Continue a course before moving to the next subject. Starting questions
  // suggest a place to begin; they never count skipped modules as completed.
  for(const s of catalog.subjects){
    if(subject&&s.id!==canonicalSubject(subject))continue;
    const chain=activeUnits(catalog,s.id),unfinished=chain.filter(u=>!done.has(u.id));
    if(!unfinished.length)continue;
    const available=unfinished.filter(u=>units.some(v=>v.id===u.id));
    if(!available.length)continue;
    const highest=chain.reduce((n,u,i)=>done.has(u.id)?Math.max(n,i):n,-1);
    if(highest<0){const assessed=suggestedStart(catalog,s.id,starting);if(available.some(u=>u.id===assessed?.id))return assessed;}
    return available.find(u=>chain.indexOf(u)>highest)||available[0];
  }
  return null;
}

export function foundationMarkup(plan,catalog,{compact=false,preview=false,offline=false}={}) {
  const byId=new Map(catalog.units.map(u=>[u.id,u]));
  return `<section class="card foundation-path" aria-label="Your everyday path">
    <div class="foundation-heading"><div><h2>${esc(plan.title)}</h2></div><span class="pill">${plan.completed} of ${plan.total} checks passed</span></div>
    ${plan.complete?'<p>Everyday path complete. Review your practical skills with your mentor.</p>':''}
    <div class="foundation-groups ${compact?'foundation-compact':''}">${plan.groups.map((group,index)=>compact?
      `<div class="foundation-group foundation-tone-${index}"><span class="foundation-number" aria-hidden="true">${index+1}</span><div><h3>${esc(group.title)}</h3><span>${group.completed} of ${group.total} passed</span></div></div>`:
      `<details class="foundation-group foundation-tone-${index}"><summary><span class="foundation-number" aria-hidden="true">${index+1}</span><span><strong>${esc(group.title)}</strong><span class="foundation-count">${group.completed} of ${group.total} passed</span></span></summary><p>${esc(group.description)}</p><ul>${group.units.map(id=>`<li><a class="foundation-step" href="#lesson/${encodeURIComponent(id)}"><span>${esc(byId.get(id)?.title||id)}</span><span class="foundation-state">${group.passed.includes(id)?'✓ Passed':'Open →'}</span></a></li>`).join('')}</ul></details>`).join('')}</div>
    ${compact?'<a class="text-link foundation-more" href="#progress">View my full path →</a>':''}
    ${preview||offline?'<p class="source-note">'+(preview?'Preview only. Join your mentor to save check results.':'Last saved results. Checks are waiting to sync.')+'</p>':''}
  </section>`;
}

export function mentorFoundation(plan,learner='') {
  if(!plan)return '';
  return `<details class="mentor-foundation" data-mentor-disclosure="foundation-${esc(learner)}"><summary>Everyday path: ${plan.completed} of ${plan.total} checks passed</summary><ul>${plan.groups.map(g=>`<li>${esc(g.title)}: ${g.completed}/${g.total}</li>`).join('')}</ul><p class="legend">Path version ${plan.version}. App checks are evidence for your review, not proof of independent understanding or a reward approval.</p></details>`;
}
