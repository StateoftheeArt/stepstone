import {courseReadiness} from './foundation.js?build=123';
import {activeUnits,suggestedStart} from './curriculum.js?build=123';
import {displayUserText} from './language.js?build=123';
import {COMPANIONS,companionSprite} from './companion.js?build=123';
import {escapeHTML as esc} from './engine.js?build=123';
import {carton,orderGoal} from './mission.js?build=123';

export function hasStartedLearning({local={},me=null}={}){
  return Object.values(local).some(d=>d?.startedFromPlan===true||(d?.phase??0)>0)
    ||!!me?.attempts?.length||!!me?.mastered?.length;
}

export function startingPlanMarkup({catalog,result,next,action='start-plan',locked=false,guide=false,guideStep=null,readButton=()=>''}){
  if(!result?.complete||!next)return '';
  const subject=catalog.subjects.find(s=>s.id===next.subject);
  const control=action==='finish'||action==='sync'?`data-tour="${action}"`:`data-action="start-plan" data-unit="${esc(next.id)}"`;
  return `<div class="mission-layout"><section class="card starting-plan-card" id="starting-plan" aria-labelledby="starting-plan-title">
    <p class="eyebrow">${guideStep?'STEP '+guideStep.number+' OF '+guideStep.total:guide?'FINAL GUIDE STEP':'YOUR FIRST STEP'}</p><h1 id="starting-plan-title">Your starting plan</h1>
    <p>Your starting questions suggest a place to begin. Complete the first four courses before Digital skills and Work & jobs.</p>${readButton('starting-plan','Read my plan aloud')}
    <div class="starting-plan-next"><span class="pill">${esc(subject?.name||next.subject)}</span><div><h2>${esc(next.title)}</h2><p>${esc(next.goal)}</p></div></div>
    ${locked?'<p class="legend">Finish the guided tour, then start from this plan.</p>':''}
    <button class="btn starting-plan-start${guide?' tour-target':''}" ${control} ${locked?'disabled':''}>${action==='sync'?'Save setup & start from my plan':'Start from my plan'} <span aria-hidden="true">→</span></button>
    ${!guide&&!locked?`<details class="starting-plan-subjects"><summary>Suggestions for other subjects</summary><div class="starting-subjects">${catalog.subjects.map(s=>{const first=suggestedStart(catalog,s.id,result);return first&&!['digital','work'].includes(s.id)?`<a href="#lesson/${esc(first.id)}" data-action="start-plan" data-unit="${esc(first.id)}"><strong>${esc(s.name)}</strong><span>${esc(first.title)}</span></a>`:'';}).join('')}</div></details>`:''}
  </section></div>`;
}

export const AVATARS = ['orbit','bolt','pixel','leaf','comet','wave',...COMPANIONS.map(c=>c.id)];
export function avatar(name='orbit',size=60){
  if(COMPANIONS.some(c=>c.id===name))return companionSprite(name,size);
  const n=AVATARS.indexOf(name),colors=['#beb4ff','#dbf66d','#ffb4cf','#9de5d6','#ffb78b','#a3d8ff'];
  const marks=['<circle cx="36" cy="36" r="22" fill="none" stroke="#fff" stroke-width="3"/><ellipse cx="36" cy="36" rx="31" ry="10" transform="rotate(-30 36 36)" fill="none" stroke="#262142" stroke-width="3"/>','<path d="m40 8-23 33h17l-3 23 25-35H38z" fill="#262142"/>','<path d="M17 20h38v32H17zM12 28h8v16h-8m40-16h8v16h-8" fill="#262142"/><path d="M26 32h5v5h-5m15-5h5v5h-5M28 44h16" stroke="white" stroke-width="3"/>','<path d="M16 51Q12 14 57 13Q62 54 22 57M20 56l28-30" fill="#225647" stroke="#225647" stroke-width="3"/><path d="m25 48 21-21" stroke="white" stroke-width="3"/>','<path d="m17 17 20 20M13 29l19 19M29 12l17 17" stroke="#fff" stroke-width="5"/><circle cx="44" cy="44" r="16" fill="#262142"/><circle cx="40" cy="40" r="4" fill="white"/>','<path d="M8 28q14-20 28 0t28 0M8 43q14-20 28 0t28 0M8 57q14-20 28 0t28 0" fill="none" stroke="#26394f" stroke-width="6"/>'];
  return `<svg class="avatar" width="${size}" height="${size}" viewBox="0 0 72 72" aria-hidden="true"><rect width="72" height="72" rx="23" fill="${colors[Math.max(0,n)]}"/>${marks[Math.max(0,n)]}</svg>`;
}
function lessonScene(task,draft,phase,html,next){
  if(next.mission.kind==='order'&&[1,3].includes(phase)&&draft?.examplePhase!==phase){
    const {start,target}=orderGoal(phase),state=draft?.orderLab?.[phase]||{};
    const count=Number.isInteger(state.count)&&state.count>=0&&state.count<=12?state.count:start;
    const status=state.checked&&count===target?'Order checked. Continue to the next step.':count===target?'The quantity matches. Continue the lesson to check your order.':count<target?`${target-count} more to pack.`:`${count-target} extra to take out.`;
    return `<div class="preview-scene" aria-label="Saved packing activity"><strong>Your bag · ${count} of ${target} cartons</strong><div class="preview-pieces" aria-hidden="true">${Array.from({length:Math.max(count,target)},(_,i)=>`<span class="preview-carton ${i<count?'packed':''} ${i>=target?'extra':''}">${i<count?carton:''}</span>`).join('')}</div><small>${status}</small></div>`;
  }
  const game=task?.game,work=draft?.scenarioLab?.[phase]?.tasks?.[task?.id]?.game||{};
  if(game){
    const selected=work.selected||[];
    return `<div class="preview-scene" aria-label="Lesson activity preview"><strong>${esc(game.title)}</strong>${game.facts?`<div class="preview-facts">${game.facts.map(([k,v])=>`<span>${esc(k)}<b>${esc(v)}</b></span>`).join('')}</div>`:''}<div class="preview-pieces">${game.kind==='cash'?game.coins.map(c=>`<span class="preview-piece coin">${c>=100?c/100+(c===100?' dollar':' dollars'):c+' cents'}</span>`).join(''):game.parts.map((p,i)=>`<span class="preview-piece ${selected.includes(i)?'selected':''}"><span aria-hidden="true">${selected.includes(i)?'✓':'○'}</span><strong>${esc(p.label)}</strong><small>${esc(p.detail||'')}</small></span>`).join('')}</div><small>Open the lesson to use this activity.</small></div>`;
  }
  if(task?.messages)return `<div class="preview-scene">${task.messages.map(m=>`<div class="preview-message"><small>${esc(m.label)}</small><p>${html(m.text)}</p></div>`).join('')}</div>`;
  if(task?.table)return `<div class="preview-scene"><div class="table-wrap"><table>${(task.table.rows||[]).map(row=>`<tr>${row.map(x=>`<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</table></div></div>`;
  const lesson=next.lessons[phase>=3?1:0];
  return `<div class="preview-scene"><strong>${esc(lesson.title)}</strong><p>${html(lesson.example?.steps?.[0]||lesson.body)}</p></div>`;
}
export function homeMarkup({me,catalog,next,draft,html,done,guestAvatar,guestName,profile:personalProfile={},startingPlan='',dailyTasks=''}){
  const continued=!!draft,phase=draft?.phase||0;
  const tasks=next?.mission?.labs?.[phase===3?1:0],task=tasks?.[draft?.scenarioLab?.[phase]?.cursor??draft?.messageLab?.[phase]?.cursor??0];
  const example=[1,3].includes(phase)&&draft?.examplePhase===phase;
  const step=example?'Worked example':phase===0?'Your task':phase===1||phase===3?'Guided practice':phase===2||phase===4?'Your turn':phase===5?'Review your work':phase===6?'Your checkpoint':'Module complete';
  const preview=example?next.lessons[phase===1?0:1].body:[1,3].includes(phase)&&next?.mission.kind==='order'?`Pack ${orderGoal(phase).target} drink cartons. Continue with your saved bag below.`:(phase===1||phase===3)&&task?task.prompt:phase===2||phase===4?draft?.rounds?.[phase]?.questions?.[draft?.rounds?.[phase]?.cursor||0]?.prompt:phase===6?'Your answers are saved. Continue your six-question checkpoint.':next?.goal;
  const scene=next&&(!continued||!example&&[1,3].includes(phase))?lessonScene(task,draft,phase,html,next):'';
  const subject=catalog.subjects.find(s=>s.id===next?.subject);
  const profile={avatar:guestAvatar,...personalProfile,...me?.profile};
  const note=(me?.attempts||[]).filter(a=>a.note?.trim()&&a.reviewed).sort((a,b)=>b.reviewed-a.reviewed)[0];
  return `
  ${startingPlan||(next?`<div class="mission-layout"><section class="mission-hero resume-card">
    <div class="resume-heading"><span class="mission-label">${continued?'Pick up where you left off':'Your next lesson'}</span><span class="pill">${esc(subject.name)}</span></div>
    <div class="resume-body"><div class="resume-summary"><h1>${esc(next.title)}</h1>
    <div class="resume-task"><h2>${esc(step)}</h2><p>${html(preview||next.goal)}</p>${scene?`<div class="lesson-preview">${scene}</div>`:''}</div>
    <ol class="resume-objectives" aria-label="Module sections">${next.mission.objectives.map((label,i)=>`<li><span aria-hidden="true">${i+1}</span>${esc(label)}</li>`).join('')}</ol>
    <div class="resume-actions"><a class="btn light resume-button" href="#lesson/${next.id}">${continued?'Continue where I left off':'Start module'} <span aria-hidden="true">→</span></a></div></div>
    </div>
  </section></div>`:`<section class="mission-hero resume-card"><h1>You’ve completed every module.</h1><p>Keep your skills fresh with a food review, or revisit a module in Learn.</p><a class="btn light" href="#path">Choose a module to review →</a></section>`)}
  ${dailyTasks}
  ${note?`<section class="mentor-note"><span class="note-mark" aria-hidden="true">↳</span><div><p class="eyebrow">A NOTE FROM YOUR MENTOR</p><blockquote>${esc(displayUserText(note.note))}</blockquote><p class="legend">About ${esc(note.report.title)}</p><a class="text-link" href="#progress">See my feedback →</a></div></section>`:''}
  <div class="section-title course-section-title"><div><h2>Your courses</h2><p class="course-order-label">Suggested learning order</p></div><a class="text-link all-modules-link" href="#path"><span>All modules</span><span aria-hidden="true">→</span></a></div><section class="world-grid" aria-label="Subjects">${catalog.subjects.map((s,i)=>{const units=activeUnits(catalog,s.id),count=units.filter(u=>done.has(u.id)).length,locked=['digital','work'].includes(s.id)&&!courseReadiness(catalog,done).complete;return `<a class="world-card world-${s.id} ${locked?'course-locked':''}" href="#path/${s.id}"><span class="subject-symbol" aria-hidden="true">${{math:'+',reading:'Aa',science:'⌁',life:'♡',digital:'⌘',work:'▣'}[s.id]||'•'}</span><h3><span class="course-order" aria-label="Course ${i+1}">${i+1}</span>${esc(s.name)}</h3><p>${esc(s.short)}</p><span>${locked?'Locked · finish courses 1–4':count?`${count} of ${units.length} completed`:`${units.length} modules to explore`} <b aria-hidden="true">→</b></span></a>`;}).join('')}</section>
  `;
}
