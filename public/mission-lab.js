import {stockModelMarkup,stockTakeMarkup} from './stock-visual.js?build=123';
import {commonPitfall} from './lesson-help.js?build=123';
import {languageAllowed,displayUserText,LANGUAGE_MESSAGE} from './language.js?build=123';
import {successMarkup} from './lesson-feedback.js?build=123';
import {mountLessonGame} from './lesson-games.js?build=123';
import {mountScienceVisual} from './science-model.js?build=123';
import {escapeHTML as esc,numberValue} from './engine.js?build=123';
import {mountMathVisual} from './math-visual.js?build=123';
import {mountPC,pcComplete} from './pc-lab.js?build=123';
import {mountTyping,typingComplete} from './typing-lab.js?build=123';
import {activityDiagram} from './lesson-diagrams.js?build=123';

// Supported mission tasks live inside the existing lesson draft and transitions.
export function scenarioState(u,phase,draft){
  const tasks=u.mission.labs[phase===1?0:1];draft.scenarioLab??={};
  const state=draft.scenarioLab[phase]??={cursor:0,tasks:{}};
  if(!Number.isInteger(state.cursor)||state.cursor<0||state.cursor>=tasks.length)state.cursor=0;
  state.tasks??={};const task=tasks[state.cursor];
  const work=state.tasks[task.id]??={values:{...task.start},selected:[],answer:'',checked:false,hint:false};
  work.values??={...task.start};work.selected??=[];work.answer??='';
  if(['draft','conversation'].includes(task.kind)){work.text??=task.revise?(draft.reflection||''):(task.initial||'');work.baseline??=work.text;}
  return {tasks,state,task,work};
}
export function scenarioCorrect(task,work){
  if(task.kind==='typing')return typingComplete(task,work);
  if(task.kind==='pc')return pcComplete(task,work);
  if(task.kind==='number'){const n=numberValue(work.answer);return n!==null&&Math.abs(n-task.answer)<1e-7;}
  if(task.kind==='choice')return Number.isInteger(work.answer)&&work.answer===task.answer;
  if(task.kind==='fraction')return new Set(work.selected.filter(i=>Number.isInteger(i)&&i>=0&&i<task.parts)).size===task.take;
  if(task.kind==='evidence')return work.selected.length===task.answer.length&&task.answer.every(i=>work.selected.includes(i));
  if(['draft','conversation'].includes(task.kind))return !!work.text?.trim()&&languageAllowed(work.text)&&(!task.revise||work.text.trim()!==work.baseline.trim())&&(task.kind!=='conversation'||Number.isInteger(work.answer)&&!!task.replies[work.answer]);
  return !!task.target&&Object.entries(task.target).every(([name,value])=>work.values[name]===value);
}
export function scenarioReady(u,phase,draft){const {task,work}=scenarioState(u,phase,draft);return !!work.checked&&scenarioCorrect(task,work);}
export function nextScenarioTask(u,phase,draft){const {state,tasks}=scenarioState(u,phase,draft);if(state.cursor<tasks.length-1){state.cursor++;return true;}return false;}

const dots=n=>Array.from({length:n},()=>'<i aria-hidden="true"></i>').join('');
function taskContext(task,html,u){
  const table=task.table;
  const spoken=table?[table.caption,...table.rows.map(row=>row.map((c,i)=>`${table.columns[i]}: ${c}`).join('. '))].join('. ')+'.':'';
  const grid=table?`<table class="mission-table" data-say="${esc(spoken)}"><caption>${esc(table.caption)}</caption><thead><tr>${table.columns.map(c=>`<th scope="col">${esc(c)}</th>`).join('')}</tr></thead><tbody>${table.rows.map(row=>`<tr>${row.map((c,i)=>i===0?`<th scope="row">${html(c)}</th>`:`<td>${html(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>`:'';
  const signs={
    stop:['STOP sign: a red shape with eight sides.', '<polygon points="38,5 90,5 123,38 123,90 90,123 38,123 5,90 5,38" fill="#b82536" stroke="#f3eee3" stroke-width="4"/><text x="64" y="76" text-anchor="middle" fill="#fff" font-size="32" font-family="sans-serif" font-weight="700">STOP</text>'],
    yield:['Yield sign: a red-bordered triangle pointing down.', '<polygon points="8,15 120,15 64,118" fill="#f3eee3" stroke="#bd2838" stroke-width="11" stroke-linejoin="round"/>']
  };
  const sign=signs[task.sign];
  return activityDiagram(u,task)+grid+(sign?`<figure class="mission-sign" data-say="${esc(sign[0])}"><svg viewBox="0 0 128 128" role="img" aria-label="${esc(sign[0])}">${sign[1]}</svg><figcaption>${esc(sign[0])}</figcaption></figure>`:'');
}
function model(m){
  if(!m)return '';
  if(m.type==='stock')return stockModelMarkup(m);
  if(m.type==='groups')return `<div class="group-model" role="img" aria-label="${m.groups} equal packs with ${m.each} items each">${Array.from({length:m.groups},(_,i)=>`<div class="group-row"><span>Pack ${i+1}</span><div>${dots(m.each)}</div></div>`).join('')}</div>`;
  if(m.type==='fraction')return `<div class="fraction-model" role="img" aria-label="${m.take} of ${m.parts} equal parts selected">${Array.from({length:m.parts},(_,i)=>`<span class="fraction-piece ${i<m.take?'selected':''}">${i+1}</span>`).join('')}</div>`;
  if(m.type==='receipt')return `<div class="order-ticket"><span>${m.quantity} items<br>Each: ${m.price.toFixed(2)} dollars</span></div>`;
  return '';
}
const control=(name,label,value,min,max,fixed)=>`<div class="quantity-control"><span>${esc(label)}</span><div><button class="btn secondary" data-adjust="${name}" data-delta="-1" aria-label="Take away one ${esc(label.toLowerCase())}" ${value<=min||fixed?'disabled':''}>−</button><output>${value}</output><button class="btn secondary" data-adjust="${name}" data-delta="1" aria-label="Add one ${esc(label.toLowerCase())}" ${value>=max||fixed?'disabled':''}>+</button></div></div>`;

export function mountScenario({host,u,phase,draft,save,html,readButton,onEdit,onCorrect}){
  const {task,work,state,tasks}=scenarioState(u,phase,draft),ready=()=>!!work.checked&&scenarioCorrect(task,work);
  const written=['draft','conversation'].includes(task.kind);
  function controls(){
    if(task.kind==='typing')return '<div data-typing-lab></div>';
    if(task.kind==='pc')return '<div data-pc-lab></div>';
    const v=work.values;
    if(task.kind==='stock')return `<p class="stock-directions">${task.trade?'Open a bundle to move its ten labels into the loose tray. The total stays the same.':'Use + to add stock and − to return it. A bundle adds ten labels; a loose label adds one.'}</p>`+stockModelMarkup({...v,released:work.stockJustOpened?10:0},{total:true})+`<div class="scenario-controls">${control('tens','Bundle (10 labels)',v.tens,0,9,task.trade)}${control('ones','Loose label (1)',v.ones,0,29,task.trade)}</div><div class="buttons stock-tools">${task.trade?'<button class="btn secondary" data-scenario="trade" '+(v.tens<1||v.ones>19?'disabled':'')+'>Open one bundle</button>':''}<button class="text-link" data-scenario="stock-reset">Reset shelf</button></div>${work.stockJustOpened?'<p class="stock-open-note" role="status">Ten labels moved from one closed bundle into the loose tray. No labels were added or lost.</p>':''}`;
    if(task.kind==='groups')return '<p class="model-key">Each row is a pack. Each small tile is 1 item.</p>'+model({type:'groups',...v})+`<div class="scenario-controls">${control('groups','Packs',v.groups,1,8,task.fixed?.includes('groups'))}${control('each','In each pack',v.each,1,10,task.fixed?.includes('each'))}</div><p class="pack-equation">${html(`$${v.groups}\\times${v.each}=${v.groups*v.each}$`)}</p>${task.total?`<p>${task.total-v.groups*v.each>=0?`${task.total-v.groups*v.each} labels left to pack`:`${v.groups*v.each-task.total} labels too many`}</p>`:''}`;
    if(task.kind==='fraction')return `<p class="legend">Each ${task.per?'row':'piece'} is an equal share.</p><div class="fraction-model ${task.per?'fraction-rows':''}">${Array.from({length:task.parts},(_,i)=>`<button class="fraction-piece ${work.selected.includes(i)?'selected':''}" data-piece="${i}" aria-pressed="${work.selected.includes(i)}" aria-label="Select part ${i+1}">${task.per?dots(task.per):i+1}</button>`).join('')}</div><p class="pack-equation">${html(`$\\frac{${work.selected.length}}{${task.parts}}$`)} selected${task.per?` · ${work.selected.length*task.per} labels`:''}</p>`;
    if(task.kind==='money')return `<div class="money-model"><span>Amount you made</span><output>${(v.cents/100).toFixed(2)} dollars</output><p>${v.cents} cents</p></div><div class="cash-controls">${[[100,'1 dollar'],[25,'25 cents']].map(([amount,label])=>`<div><button class="btn secondary" data-money="${amount}" ${v.cents+amount>2000?'disabled':''}>Add ${label}</button><button class="text-link" data-money="${-amount}" ${v.cents<amount?'disabled':''}>Take away ${label}</button></div>`).join('')}</div>`;
    if(task.kind==='choice')return `<fieldset class="message-choices"><legend>Choose one answer.</legend>${task.options.map((text,i)=>`<label class="option"><input type="radio" name="scenario-answer" value="${i}" ${work.answer===i?'checked':''}><span>${html(text)}</span></label>`).join('')}</fieldset>`;
    if(task.kind==='evidence')return `<p class="legend">Select every line that answers the task. Tap again to undo.</p><div class="evidence-lines">${task.lines.map((line,i)=>`<button type="button" data-evidence="${i}" aria-pressed="${work.selected.includes(i)}">${html(line)}</button>`).join('')}</div>`;
    if(written)return (task.kind==='conversation'?`<div class="evidence-lines">${task.replies.map((r,i)=>`<button type="button" data-reply="${i}" aria-pressed="${work.answer===i}">${html(r.text)}</button>`).join('')}</div><p class="reply-outcome" role="status">${Number.isInteger(work.answer)?html(task.replies[work.answer]?.outcome||''):''}</p><p>${html(task.writePrompt)}</p>`:'')+`${task.example?`<details class="draft-example" ${work.example?'open':''}><summary>See one possible version</summary><p>${html(task.example)}</p></details>`:''}<label class="field"><span>${task.revise?'Improve your earlier draft':'Your working draft'}</span><textarea data-scenario-text maxlength="2000">${esc(work.text)}</textarea></label>`;
    return (task.id==='stock-take'?stockTakeMarkup(task.model,work.stockTaken||[]):task.model?.type==='stock'?stockModelMarkup(task.model):task.game?'<div data-lesson-game></div>':task.visual?'<details class="mission-model"><summary>Optional: explore how this works</summary><div data-math-model></div><p class="legend">Use this model to explore the idea. Then use the numbers in the task above for your answer.</p></details>':model(task.model))+`<label class="field"><span>${esc(task.answerLabel||'Your answer')}</span><input data-scenario-answer value="${esc(work.answer)}" maxlength="80" autocomplete="off" inputmode="text"></label><p class="legend">${esc(task.answerHelp||'A number or a fraction like 3/4 works.')}</p>`;
  }
  function paint(){
    host.innerHTML=`${tasks.length>1?`<div class="message-task-head"><span class="pill">${state.cursor+1} of ${tasks.length}</span></div>`:''}<h2>${esc(task.title)}</h2><p class="scenario-prompt question-focus">${html(task.prompt)}</p><div class="activity-tools"><button class="text-link mission-show-example" data-action="mission-example">Show me how</button>${readButton('mission-lab')}</div><div class="scenario-model">${taskContext(task,html,u)}${task.science?'<details open class="mission-model"><summary>Explore a model</summary><div data-science-model></div><p class="legend">Try changing the model. Answer using the numbers and details in the task above.</p></details>':''}${controls()}</div><p class="hint" ${work.hint?'':'hidden'}><strong>Common pitfall</strong> ${esc(commonPitfall(u,task))}</p><p class="scenario-feedback" role="status">${work.checked?html(ready()?task.why:'That does not fit yet. Check the common pitfall above.'):''}</p>${successMarkup(ready())}<div class="buttons mission-actions"><button class="btn" data-scenario="check" ${ready()?'hidden':''}>Check my work</button><button class="btn" data-action="mission-next" ${ready()?'':'hidden'}>Next →</button><button class="btn secondary" data-action="mission-hold" hidden>Stop</button><button class="btn secondary" data-scenario="hint">Show help</button></div>`;
    if(written){const field=host.querySelector('[data-scenario-text]');field.closest('label').insertAdjacentHTML('afterend',`<div id="draft-readback" class="sr-only">${esc(displayUserText(work.text))}</div>${readButton('draft-readback','Read my draft aloud')}`);host.querySelector('[data-mission-success] strong').textContent='Draft saved';host.querySelector('[data-next-note]').textContent='';host.querySelector('[data-scenario=check]').textContent='Save this draft';if(ready())host.querySelector('.scenario-feedback').textContent='';}
    if(task.science){work.science??={...(draft.labs?.[phase]||{})};mountScienceVisual({host:host.querySelector("[data-science-model]"),model:task.science,phase,state:work.science,html,save:()=>{onEdit();work.checked=false;save();clearFeedback();}});}
    if(task.game&&task.model?.type!=='stock'){work.game??={};mountLessonGame({host:host.querySelector('[data-lesson-game]'),game:task.game,state:work.game,html,save:()=>{onEdit();work.checked=false;save();clearFeedback();}});}
    if(task.visual){work.visual??={value:draft.visualValues?.[phase]};mountMathVisual({host:host.querySelector('[data-math-model]'),kind:task.visual,state:work.visual,html,save:()=>{onEdit();work.checked=false;save();clearFeedback();}});}
    if(task.kind==='typing'){if(!work.typing&&draft.typingPreferences)work.typing={text:task.initial||'',...draft.typingPreferences,cue:true,assisted:false,paused:false};mountTyping(host.querySelector('[data-typing-lab]'),task,work,()=>{draft.typingPreferences={method:work.typing.method,target:work.typing.target};onEdit();save();clearFeedback();});}
    if(task.kind==='pc'){
      const savedNote=draft.scenarioLab?.[1]?.tasks?.['pc-save']?.pc?.saved;
      if(task.id==='pc-backup'&&savedNote&&(!work.pc||work.pc.step===0&&!work.pc.initialisedFromSave))work.pc={step:0,text:savedNote,saved:'',backup:'',message:'',initialisedFromSave:true};
      mountPC(host.querySelector('[data-pc-lab]'),task,work,repaint=>{onEdit();save();if(repaint){paint();host.querySelector('[data-pc-action], [data-scenario=check]')?.focus({preventScroll:true});}else clearFeedback();});
    }
    host.querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.evidence);edit(()=>work.selected=work.selected.includes(i)?work.selected.filter(n=>n!==i):[...work.selected,i],`[data-evidence="${i}"]`);});
    host.querySelectorAll('[data-reply]').forEach(b=>b.onclick=()=>edit(()=>work.answer=Number(b.dataset.reply),`[data-reply="${b.dataset.reply}"]`));
    const writing=host.querySelector('[data-scenario-text]');
    if(writing)writing.oninput=()=>{onEdit();work.text=writing.value;draft.reflection=writing.value;host.querySelector('#draft-readback').textContent=displayUserText(writing.value);work.checked=false;save();clearFeedback();};
    const example=host.querySelector('.draft-example');if(example)example.ontoggle=()=>{if(work.example!==example.open){onEdit();work.example=example.open;save();}};
    host.querySelectorAll('[data-adjust]').forEach(b=>b.onclick=()=>{
      const key=b.dataset.adjust,value=work.values[key]+Number(b.dataset.delta),limits={tens:[0,9],ones:[0,29],groups:[1,8],each:[1,10]};
      if(task.fixed?.includes(key)||task.trade||value<limits[key][0]||value>limits[key][1])return;
      edit(()=>work.values[key]=value,`[data-adjust="${key}"][data-delta="${b.dataset.delta}"]`);
    });
    host.querySelectorAll('[data-money]').forEach(b=>b.onclick=()=>edit(()=>work.values.cents=Math.max(0,Math.min(2000,work.values.cents+Number(b.dataset.money))),`[data-money="${b.dataset.money}"]`));
    host.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.piece);edit(()=>work.selected=work.selected.includes(i)?work.selected.filter(n=>n!==i):[...work.selected,i],`[data-piece="${i}"]`);});
    const input=host.querySelector('[data-scenario-answer]');
    if(input){input.oninput=()=>{onEdit();work.answer=input.value;work.checked=false;save();clearFeedback();};input.onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();check();}};}
    host.querySelectorAll('[name=scenario-answer]').forEach(input=>input.onchange=()=>edit(()=>work.answer=Number(input.value),`[name=scenario-answer][value="${input.value}"]`));
    host.querySelector('[data-scenario=trade]')?.addEventListener('click',()=>{if(work.values.tens>0&&work.values.ones<=19)edit(()=>{work.values.tens--;work.values.ones+=10;work.stockJustOpened=true;},'[data-scenario=trade]');});
    host.querySelector('[data-scenario=stock-reset]')?.addEventListener('click',()=>edit(()=>{work.values={...task.start};work.stockJustOpened=false;},'[data-scenario=stock-reset]'));
    host.querySelectorAll('[data-stock-pick]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.stockPick);edit(()=>{if(!Array.isArray(work.stockTaken))work.stockTaken=[];work.stockTaken=work.stockTaken.includes(i)?work.stockTaken.filter(n=>n!==i):[...work.stockTaken,i];},`[data-stock-pick="${i}"]`);});
    host.querySelector('[data-scenario=check]').onclick=check;
    host.querySelector('[data-scenario=hint]').onclick=()=>{onEdit();work.hint=true;save();host.querySelector('.hint').hidden=false;};
  }
  function clearFeedback(){host.querySelector('[data-mission-success]').hidden=true;host.querySelector('[data-action=mission-next]').hidden=true;host.querySelector('[data-action=mission-hold]').hidden=true;host.querySelector('[data-scenario=check]').hidden=false;host.querySelector('.scenario-feedback').textContent='';}
  function edit(change,focus){onEdit();change();work.checked=false;save();paint();host.querySelector(focus)?.focus({preventScroll:true});}
  function check(){
    if(written&&!languageAllowed(work.text)){host.querySelector('.scenario-feedback').textContent=LANGUAGE_MESSAGE;host.querySelector('[data-scenario-text]')?.focus();return;}
    onEdit();
    if(['number','choice'].includes(task.kind)&&(work.answer===''||work.answer===undefined)){host.querySelector('.scenario-feedback').textContent='Try an answer first. You can use Show help.';host.querySelector('input')?.focus();return;}
    if(task.kind==='number'&&numberValue(work.answer)===null){host.querySelector('.scenario-feedback').textContent='Type the answer as a number, such as 12 or 2.50. A fraction such as 3/4 also works.';host.querySelector('input')?.focus();return;}
    work.checked=true;if(!scenarioCorrect(task,work))work.hint=true;save();paint();
    if(ready()){if(!written)onCorrect();host.querySelector('[data-action=mission-next]').focus({preventScroll:true});}
  }
  paint();
}
