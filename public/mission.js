import {commonPitfall} from './lesson-help.js?build=121';
import {successMarkup} from './lesson-feedback.js?build=121';
import {escapeHTML as esc} from './engine.js?build=121';
import {mountScenario,scenarioReady,nextScenarioTask} from './mission-lab.js?build=121';
import {wireMoves} from './touch-move.js?build=121';
import {lessonVisualMarkup} from './lesson-visual.js?build=121';
import {lessonWords} from './lesson-words.js?build=121';

// Mission presentation uses the existing lesson phases, rounds and saved draft.
// It has no separate scoring, currency, account or progression system.
export const isMission = unit => ['order','message','scenario'].includes(unit?.mission?.kind);

const parcel = `<svg viewBox="0 0 160 160" fill="none" aria-hidden="true"><path d="m80 9 62 36v73l-62 35-62-35V45Z" stroke="currentColor" opacity=".25"/><path d="m80 29 44 25v52l-44 25-44-25V54Z" fill="currentColor" opacity=".12"/><path d="m36 54 44 26 44-26M80 80v51M59 41l44 26v23" stroke="currentColor" stroke-width="3"/><path d="m60 99 12 7m-12 4 12 7" stroke="currentColor" stroke-width="3"/></svg>`;
export const carton = `<svg viewBox="0 0 40 52" aria-hidden="true"><path d="M10 3h19l6 9v35H5V12Z" fill="currentColor" opacity=".85"/><path d="M10 3v9H5m5 0h25M29 3v9M25 0v18" fill="none" stroke="#173a40" stroke-width="2"/><rect x="11" y="21" width="18" height="17" rx="3" fill="#173a40"/><circle cx="20" cy="31" r="5" fill="currentColor"/><path d="M20 25q0-6 6-5-1 5-6 5" fill="currentColor"/></svg>`;
export const orderGoal = phase => phase===1?{start:4,target:7}:{start:7,target:5};
const message = `<svg viewBox="0 0 160 160" fill="none" aria-hidden="true"><path d="m80 9 62 36v73l-62 35-62-35V45Z" stroke="currentColor" opacity=".25"/><path d="M31 43h83l15 15v49H69l-26 21v-21H31Z" fill="currentColor" opacity=".12"/><path d="M31 43h83l15 15v49H69l-26 21v-21H31ZM48 64h61M48 80h39" stroke="currentColor" stroke-width="3"/><path d="m99 88 7 7 14-16" stroke="currentColor" stroke-width="3"/></svg>`;
const emblem = u => u.mission.kind==='message'?message:parcel;

export function missionHeader(u, phase, passed=false) {
  const current = phase===7 && passed ? 3 : phase <= 2 ? 0 : phase <= 4 ? 1 : 2;
  return `<h1 class="sr-only">${esc(u.title)}</h1>
    <ol class="mission-route" aria-label="Module sections">${u.mission.objectives.map((label,i)=>`<li class="${i===current?'active':i<current?'done':''}" ${i===current?'aria-current="step"':''}><span class="mission-node" aria-hidden="true">${i<current?'✓':String(i+1).padStart(2,'0')}</span><span>${esc(label)}</span></li>`).join('')}</ol>`;
}

export function missionIntro(u, readButton, html=esc) {
  return `<section class="mission-brief card" id="intro-copy"><div><h2>${esc(u.goal)}</h2>${lessonVisualMarkup(u,html)}${lessonWords(u)}${u.communication?`<details class="communication-transfer"><summary>Communication example</summary><h3>${esc(u.communication.title)}</h3><blockquote>${html(u.communication.example)}</blockquote><ol>${u.communication.steps.map(step=>`<li>${html(step)}</li>`).join('')}</ol></details>`:''}<div class="mission-intro-actions">${readButton('intro-copy')}<button class="btn" data-action="advance">${esc(u.mission.startLabel)} <span aria-hidden="true">→</span></button></div>${u.mission.preparation?.length?`<details class="mission-preparation"><summary>Related skills</summary>${u.mission.preparation.map(v=>`<a href="#lesson/${esc(v.id)}">${esc(v.title)}</a>`).join('')}</details>`:''}</div></section>`;
}

export function openPracticeExample(draft) {
  if (![2,4].includes(draft.phase)) return false;
  draft.exampleReturnPhase=draft.phase;
  draft.phase-=1;
  draft.examplePhase=draft.phase;
  return true;
}

export function returnFromExample(draft) {
  const returnPhase=draft.exampleReturnPhase;
  delete draft.exampleReturnPhase;
  draft.examplePhase=null;
  if ([2,4].includes(returnPhase)&&draft.phase===returnPhase-1) {
    draft.phase=returnPhase;
    return true;
  }
  return false;
}

export function missionLesson(u, phase, html, readButton, {returnToPractice=false}={}) {
  const l=u.lessons[phase===1?0:1];
  return `<div class="mission-play"><section class="card lesson-copy" id="lesson-copy" tabindex="-1" hidden><div class="activity-tools"><button class="btn secondary" data-action="mission-try">${returnToPractice?'Back to your question ↑':'Back to the activity ↑'}</button>${readButton('lesson-copy')}</div><p class="eyebrow">Worked example</p><h2>${esc(l.title)}</h2><p>${html(l.body)}</p>${l.example&&l.example!==l.title?`<h3 class="mission-example-title">${html(l.example)}</h3>`:''}<ol class="mission-example">${l.steps.map((step,i)=>`<li><span aria-hidden="true">${i+1}</span><div>${html(step)}</div></li>`).join('')}</ol><p class="mission-meaning">${html(l.whyItWorks)}</p><p class="legend">${html(l.watchFor)}</p><button class="btn" data-action="mission-try">${returnToPractice?'Return to your question →':'Return to the activity →'}</button></section><section class="mission-lab card" id="mission-lab" tabindex="-1" aria-label="${esc(u.title)}"></section></div>`;
}
export function showMissionPane(root,example,motion=false){
  const copy=root.querySelector('#lesson-copy'),lab=root.querySelector('#mission-lab');
  if(!copy||!lab)return;
  copy.hidden=!example;lab.hidden=example;
  const target=example?copy:lab;target.focus({preventScroll:true});target.scrollIntoView({block:'start',behavior:motion?'smooth':'instant'});
}

export function cursorFor(round) {
  if (!Number.isInteger(round.cursor) || round.cursor<0 || round.cursor>=round.questions.length) {
    const missing=round.questions.findIndex(q=>!round.checks[q.id]);
    round.cursor=missing<0?round.questions.length-1:missing;
  }
  return round.cursor;
}

export function missionPractice(u, round, questionCard, html) {
  const cursor=cursorFor(round),q=round.questions[cursor],ready=!!round.checks[q.id];
  const done=round.questions.filter(q=>round.checks[q.id]).length;
  return `<div class="practice-head"><span class="sr-only" id="round-count">${done} of ${round.questions.length} answered</span></div>
    <div class="mission-round-track" aria-label="Question ${cursor+1} of ${round.questions.length}">${round.questions.map((item,i)=>`<span class="${i===cursor?'active':round.checks[item.id]?'done':''}" aria-hidden="true">${round.checks[item.id]?'✓':i+1}</span>`).join('')}</div>
    <div id="practice-questions">${questionCard(q,cursor,round,false)}</div>${successMarkup(ready)}
    <div class="buttons mission-actions"><button class="btn" data-action="mission-next" ${ready?'':'disabled'}>Next <span aria-hidden="true">→</span></button><button class="btn secondary" data-action="mission-hold" hidden>Stop</button><button class="text-link" data-action="back-lesson">See the example</button></div>`;
}

function messageState(u, phase, draft) {
  const tasks=u.mission.labs[phase===1?0:1];
  draft.messageLab??={};
  const state=draft.messageLab[phase]??={cursor:0,answers:{},checks:{},hints:{}};
  if(!Number.isInteger(state.cursor)||state.cursor<0||state.cursor>=tasks.length)state.cursor=0;
  return {state, tasks, task:tasks[state.cursor]};
}

export function missionLabReady(u, phase, draft) {
  if(u.mission.kind==='scenario')return scenarioReady(u,phase,draft);
  if(u.mission.kind==='order')return !!draft.orderLab?.[phase]?.checked&&draft.orderLab[phase].count===orderGoal(phase).target;
  const {state,task}=messageState(u,phase,draft);
  return !!state.checks[state.cursor]&&state.answers[state.cursor]===task.answer;
}

export function missionLabAnswer(u, phase, draft) {
  if(u.mission.kind==='scenario')return JSON.stringify(draft.scenarioLab?.[phase]);
  return JSON.stringify(u.mission.kind==='order'?draft.orderLab?.[phase]:draft.messageLab?.[phase]);
}

// Returns true when the same lesson still has another supported task.
export function nextMissionTask(u, phase, draft) {
  if(u.mission.kind==='scenario')return nextScenarioTask(u,phase,draft);
  if(u.mission.kind!=='message')return false;
  const {state,tasks}=messageState(u,phase,draft);
  if(state.cursor<tasks.length-1){state.cursor++;return true;}
  return false;
}

export function resetMissionLabs(u, draft) {
  if(u.mission?.kind==='scenario')delete draft.scenarioLab;
  if(u.mission?.kind==='order')delete draft.orderLab;
  if(u.mission?.kind==='message')delete draft.messageLab;
}

export function mountMissionLab(options) {
  const before=missionLabAnswer(options.u,options.phase,options.draft);
  if(options.u.mission.kind==='scenario')mountScenario(options);
  else if(options.u.mission.kind==='message')mountMessageLab(options);
  else mountOrderLab(options);
  if(before!==missionLabAnswer(options.u,options.phase,options.draft))options.save();
}

function mountMessageLab({u, host, phase, draft, save, readButton, onEdit, onCorrect}) {
  const {state,tasks,task}=messageState(u,phase,draft),cursor=state.cursor;
  const ready=()=>missionLabReady(u,phase,draft);
  host.innerHTML=`<div class="message-task-head"><span class="pill">${cursor+1} of ${tasks.length}</span></div>
    <h2 id="message-prompt" class="question-focus">${esc(task.prompt)}</h2><div class="activity-tools"><button class="text-link mission-show-example" data-action="mission-example">Show me how</button>${readButton('mission-lab')}</div>
    <div class="message-thread">${task.messages.map(m=>`<div class="message-bubble"><span class="eyebrow">${esc(m.label)}</span><p>${esc(m.text)}</p></div>`).join('')}</div>
    <fieldset class="message-choices"><legend>Choose one answer.</legend>${task.options.map((text,i)=>`<label class="option"><input type="radio" name="message-answer" value="${i}" ${state.answers[cursor]===i?'checked':''}><span>${esc(text)}</span></label>`).join('')}</fieldset>
    <p class="message-hint" ${state.hints[cursor]?'':'hidden'}><strong>Common pitfall</strong> ${esc(commonPitfall(u,task))}</p><p class="message-feedback" role="status"></p>${successMarkup(ready())}
    <div class="buttons mission-actions"><button class="btn" data-message="check">Check my answer</button><button class="btn" data-action="mission-next" ${ready()?'':'hidden'}>Next →</button><button class="btn secondary" data-action="mission-hold" hidden>Stop</button><button class="btn secondary" data-message="hint">Show help</button></div>`;
  const feedback=host.querySelector('.message-feedback');
  const paint=()=>{
    host.querySelector('[data-mission-success]').hidden=!ready();
    host.querySelector('[data-action=mission-next]').hidden=!ready();
    host.querySelector('[data-action=mission-hold]').hidden=true;
    host.querySelector('[data-message=check]').hidden=ready();
    host.querySelector('.message-hint').hidden=ready()||!(state.hints[cursor]||state.checks[cursor]===false);
    host.querySelector('[data-message=hint]').hidden=ready();
    feedback.textContent=ready()?task.why:state.checks[cursor]===false?'That does not fit yet. Check the common pitfall above.':'';
  };
  host.querySelectorAll('input[name=message-answer]').forEach(input=>input.addEventListener('change',()=>{
    onEdit();state.answers[cursor]=Number(input.value);delete state.checks[cursor];save();paint();
  }));
  host.querySelector('[data-message=hint]').addEventListener('click',()=>{
    onEdit();state.hints[cursor]=true;save();paint();
  });
  host.querySelector('[data-message=check]').addEventListener('click',()=>{
    onEdit();
    if(state.answers[cursor]===undefined){feedback.textContent='Choose an answer first. You can use Show help.';return;}
    state.checks[cursor]=state.answers[cursor]===task.answer;save();paint();
    if(ready()){onCorrect();host.querySelector('[data-action=mission-next]').focus({preventScroll:true});}
  });
  paint();
}

export function mountOrderLab({u,host,phase,draft,save,html,onEdit,onCorrect}) {
  const first=phase===1,{start,target}=orderGoal(phase);
  draft.orderLab??={};const state=draft.orderLab[phase]??={count:start,checked:false};
  if(!Number.isInteger(state.count)||state.count<0||state.count>12){state.count=start;state.checked=false;}
  const ready=()=>state.checked&&state.count===target;
  host.innerHTML=`<div class="packing-goal"><span class="goal-mark" aria-hidden="true">${carton}</span><div><h2>Pack ${target} drink cartons</h2></div></div>
    <p class="packing-instruction">${first?'Tap Add a carton until your bag holds '+target+'.':'You started with '+start+' cartons. Tap the bag to remove extras until '+target+' remain.'} Then choose Check my bag.</p>
    <div class="activity-tools"><button class="text-link mission-show-example" data-action="mission-example">Show me how</button><button class="read-button" data-action="read" data-target="mission-lab">▷ Read aloud</button></div>
    <div class="packing-board">
      <button class="carton-source" data-pack="add" data-move="shelf" data-drop="shelf" aria-label="Add one carton to the bag">${carton}<strong>Add a carton</strong><span>Tap or drag into the bag →</span></button>
      <button class="order-tray" data-pack="remove" data-move="bag" data-drop="bag" aria-label="Take one carton out of the bag"><span class="bag-handle" aria-hidden="true"></span><span class="packed-label">YOUR BAG <output data-packed-count aria-live="polite"></output></span><span class="packed-slots">${Array.from({length:12},(_,i)=>`<span data-cup="${i}" class="drink-slot">${carton}</span>`).join('')}</span><span class="bag-help">Tap the bag to remove one carton</span></button>
    </div><p class="pack-objective" data-pack-objective aria-live="polite"></p>
    <div class="pack-equation" data-pack-equation></div><p class="equation-key" data-equation-key></p>
    <p class="pack-feedback" role="status"></p>${successMarkup(ready())}
    <div class="buttons mission-actions"><button class="btn" data-pack="check">Check my bag</button><button class="btn" data-action="mission-next" ${ready()?'':'hidden'}>Next →</button><button class="btn secondary" data-action="mission-hold" hidden>Stop</button></div>`;
  function paint(){
    host.querySelector('[data-packed-count]').textContent=`${state.count} / ${target}`;
    host.querySelectorAll('[data-cup]').forEach((el,i)=>{el.hidden=i>=Math.max(target,state.count);el.classList.toggle('packed',i<state.count);el.classList.toggle('extra',i>=target);});
    host.querySelector('[data-pack=remove]').disabled=state.count===0;
    host.querySelector('[data-pack=add]').disabled=state.count===12;
    host.querySelector('[data-pack-objective]').textContent=ready()?'Your order is ready.':state.count===target?'The quantities match. Check your bag.':state.count<target?`Add ${target-state.count} more ${target-state.count===1?'carton':'cartons'}.`:`Remove ${state.count-target} extra ${state.count-target===1?'carton':'cartons'}.`;
    const diff=state.count-start;host.querySelector('[data-pack-equation]').innerHTML=html(`$${start}${diff<0?'-':'+'}${Math.abs(diff)}=${state.count}$`);
    host.querySelector('[data-equation-key]').textContent=`Started with ${start} · ${diff<0?'removed':'added'} ${Math.abs(diff)} · ${state.count} in the bag now`;
    host.querySelector('.order-tray').classList.toggle('quantity-matched',state.count===target);
    host.querySelector('[data-mission-success]').hidden=!ready();host.querySelector('[data-action=mission-next]').hidden=!ready();host.querySelector('[data-action=mission-hold]').hidden=true;host.querySelector('[data-pack=check]').hidden=ready();
  }
  function move(delta){onEdit();const before=state.count;state.count=Math.max(0,Math.min(12,state.count+delta));state.checked=false;save();paint();host.querySelector('.pack-feedback').textContent='';const piece=host.querySelector(`[data-cup="${Math.max(0,state.count-1)}"] svg`);if(state.count>before&&piece&&!document.documentElement.classList.contains('quiet')&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches)piece.animate([{opacity:0,transform:'translateY(-9px) scale(.85)'},{opacity:1,transform:'translateY(0) scale(1)'}],{duration:320,easing:'ease-out'});}
  host.querySelector('[data-pack=add]').addEventListener('click',()=>move(1));
  host.querySelector('[data-pack=remove]').addEventListener('click',()=>move(-1));
  host.querySelector('[data-pack=check]').addEventListener('click',()=>{
    onEdit();state.checked=true;save();paint();
    host.querySelector('.pack-feedback').textContent=ready()?'':commonPitfall(u,{prompt:state.count>target?'remove':'more'});
    if(ready()){onCorrect();host.querySelector('[data-action=mission-next]').focus({preventScroll:true});}
  });
  wireMoves(host,{ghost:carton,onDrop:(from,to)=>{if(from.dataset.move==='shelf'&&to.dataset.drop==='bag')move(1);else if(from.dataset.move==='bag'&&to.dataset.drop==='shelf')move(-1);}});
  paint();
}
