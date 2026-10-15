import {stockExampleFrames} from './stock-visual.js?build=123';
import {lessonDiagram} from './lesson-diagrams.js?build=123';
import {escapeHTML as esc} from './engine.js?build=123';

export function exampleFrames(unit,mode=unit.exampleMode||'stock'){
  if(unit.id==='math-2')return stockExampleFrames(unit,mode);
  const lesson=unit.lessons?.[0];
  return (lesson?.steps||[]).map((text,index)=>({text,index}));
}

const tile={math:0,reading:1,writing:2,science:3,social:4,digital:5};
const carton='<svg viewBox="0 0 40 52" aria-hidden="true"><path d="M11 3h18l6 10v34H5V13Z" fill="currentColor"/><path d="M11 3v10H5m6 0h24M29 3v10" fill="none" stroke="#183843" stroke-width="2"/><path d="M13 22h14v16H13Z" fill="#183843"/><circle cx="20" cy="30" r="4" fill="currentColor"/></svg>';

function highlight(text,part){
  const at=text.indexOf(part);
  if(at<0||!part)return esc(text);
  return esc(text.slice(0,at))+'<mark>'+esc(part)+'</mark>'+esc(text.slice(at+part.length));
}

function stage(unit,index,html,mode=unit.exampleMode||'stock'){
  const l=unit.lessons[0];
  const diagram=lessonDiagram(unit.id==='math-2'?{...unit,exampleMode:mode}:unit,index);if(diagram)return diagram;
  const context=l.example===l.title?l.body:l.example;
  if(unit.visual?.kind==='task-sequence'){
    const pictures=['<path d="M8 3h18l7 7v29H8Z M26 3v8h7 M14 18h13 M14 24h13 M14 30h8"/>','<path d="M8 10h26v21H8Z M15 17h12 M15 23h9 M25 26l3 12 3-5 5-2Z"/>','<path d="M9 7h24v30H9Z M15 22l5 5 10-12"/>'];
    return `<div class="task-example-flow" aria-label="Three task steps">${unit.visual.labels.map((label,i)=>`<div class="task-example-step ${i<=index?'active':''}"><svg viewBox="0 0 42 42" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${pictures[i]}</svg><span>${esc(label)}</span></div>`).join('')}</div><p class="task-example-scene">${html(context)}</p>`;
  }
  if(unit.id==='math-1'){
    const count=index===0?5:8;
    return `<div class="example-cartons" aria-label="${count} drink cartons">${Array.from({length:count},(_,i)=>`<span class="${i>=5?'example-added':''}">${carton}</span>`).join('')}</div><div class="example-equation">${html(index===0?'$5$':index===1?'$5+3$':'$5+3=8$')}</div>`;
  }
  if(unit.id==='math-8')return `<div class="example-balance">${index===0?'<span>'+html('$3x+2=14$')+'</span><span class="example-detail-tag">−2 from each side</span><span>'+html('$3x=12$')+'</span>':index===1?'<span>'+html('$3x=12$')+'</span><span class="example-detail-tag">÷3 on each side</span><span>'+html('$x=4$')+'</span>':'<span>'+html('$3(4)+2=14$')+'</span><span class="example-detail-tag">The amounts match ✓</span>'}<span class="example-balance-bar" aria-hidden="true"></span></div>`;
  if(unit.id==='writing-1')return `<div class="example-paper"><span class="example-paper-label">Meeting message</span><p>${highlight('Meet Jo on Tuesday at 3 pm by the library entrance.',['Meet Jo','Tuesday at 3 pm','library entrance'][index])}</p><span class="example-detail-tag">${['Who and action','Day and time','Place'][index]}</span></div>`;
  if(unit.id==='writing-2')return `<div class="example-paper"><span class="example-paper-label">Complete sentence</span><p>${highlight('We cleaned the room after the meeting.',['We','cleaned the room','after the meeting.'][index])}</p><span class="example-detail-tag">${['Who','What happened','When'][index]}</span></div>`;
  if(unit.id==='reading-1')return `<div class="example-message"><span class="example-paper-label">From Jo</span><p>${highlight(l.example,['at the library','at 4 pm','Bring a form'][index])}</p><span class="example-detail-tag">${['Place','Time','Bring'][index]}</span></div>`;
  if(unit.id==='digital-1')return `<div class="example-files"><span class="example-folder">▣ Practice</span><div class="example-file ${index<2?'example-file-active':''}">▤ Weekend-plan-v1.txt</div>${index===2?'<div class="example-file example-file-active">▤ Weekend-plan-v2.txt</div>':''}${index===1?'<span class="example-detail-tag">Reopened and checked ✓</span>':''}</div>`;
  if(unit.id==='pc-start')return `<div class="example-desktop"><div class="example-window ${index===1?'example-window-behind':''}"><span>Notes · shopping.txt</span><p>Milk<br>bread</p></div>${index>0?'<div class="example-calendar"><span>Calendar</span><div class="example-calendar-grid">'+Array.from({length:14},(_,i)=>'<i>'+((i%7)+1)+'</i>').join('')+'</div></div>':''}<div class="example-taskbar"><span class="${index!==1?'selected':''}">Notes</span>${index>0?'<span class="'+(index===1?'selected':'')+'">Calendar</span>':''}</div></div>`;
  if(unit.id==='typing-keys')return `<div class="example-paper"><span class="example-paper-label">shopping.txt</span><p class="example-typed">${index===0?'Milk':index===1?'Milk<br>breadd':'Milk<br>bread'}<span class="example-cursor" aria-hidden="true"></span></p>${index===2?'<span class="example-detail-tag">Backspace removed the extra d</span>':''}</div>`;
  if(['writing','reading','social'].includes(unit.domain||unit.subject))return `<div class="example-${(unit.domain||unit.subject)==='writing'?'paper':'message'}"><span class="example-paper-label">${(unit.domain||unit.subject)==='writing'?'Writing example':unit.subject==='reading'?'Read this example':'Situation'}</span><p>${html(context)}</p></div>`;
  if(unit.subject==='science')return `<div class="example-evidence"><p>${html(context)}</p><div class="example-evidence-track" aria-hidden="true">${exampleFrames(unit).map((_,i)=>`<i class="${i<=index?'active':''}"></i>`).join('')}</div></div>`;
  return `<div class="example-model"><p>${html(context)}</p><div class="example-evidence-track" aria-hidden="true">${exampleFrames(unit).map((_,i)=>`<i class="${i<=index?'active':''}"></i>`).join('')}</div></div>`;
}

export function lessonVisualMarkup(unit,html=esc){
  const frames=exampleFrames(unit);
  if(!frames.length)return '';
  return `<figure class="lesson-visual world-${esc(unit.subject)}" data-lesson-visual data-unit="${esc(unit.id)}" aria-label="Worked example"><div class="lesson-visual-art" data-art-tile="${tile[unit.domain||unit.subject]??3}" aria-hidden="true"></div><div class="lesson-visual-work">${unit.id==='math-2'?`<div class="example-modes" role="group" aria-label="Choose a worked example">${[['stock','Stock bundles'],['money','Canadian money'],['trade','Open a bundle']].map(([id,label])=>`<button type="button" class="btn secondary" data-example-mode="${id}" aria-pressed="${id===(unit.exampleMode||'stock')}">${label}</button>`).join('')}</div>`:''}<div class="example-stage" data-example-stage>${stage(unit,0,html)}</div><figcaption class="example-step" data-example-caption aria-live="polite"><span class="example-step-number" aria-hidden="true">1</span><span>${html(frames[0].text)}</span></figcaption><div class="example-controls"><button class="btn secondary" type="button" data-example-action="play" aria-pressed="false">▷ Watch example</button><div class="example-step-controls"><button class="text-link" type="button" data-example-action="previous" aria-label="Previous example step" disabled>←</button><output data-example-count aria-label="Example step">1 / ${frames.length}</output><button class="text-link" type="button" data-example-action="next" aria-label="Next example step" ${frames.length<2?'disabled':''}>→</button></div></div></div></figure>`;
}

export function createExamplePlayer({count,paint,motion=()=>true,setTimer=setTimeout,clearTimer=clearTimeout}){
  let index=0,playing=false,timer=null,disposed=false;
  const clear=()=>{if(timer!==null)clearTimer(timer);timer=null;};
  const draw=()=>paint({index,playing});
  function stop(){clear();playing=false;if(!disposed)draw();}
  function tick(){timer=null;if(disposed||!motion()){stop();return;}index++;if(index>=count-1){index=count-1;playing=false;draw();return;}draw();timer=setTimer(tick,2800);}
  return {step(delta){if(disposed)return;clear();playing=false;index=Math.max(0,Math.min(count-1,index+delta));draw();},play(){if(disposed)return;if(playing){stop();return;}if(!motion()){this.step(1);return;}index=0;playing=count>1;draw();if(playing)timer=setTimer(tick,2800);},stop,dispose(){clear();playing=false;disposed=true;},get state(){return {index,playing};}};
}

export function mountLessonVisual(host,unit,html,motion){
  if(!host)return {stop(){},dispose(){}};
  let mode=unit.exampleMode||'stock';
  const makePlayer=()=>createExamplePlayer({count:exampleFrames(unit,mode).length,motion,paint:({index,playing})=>{
    const frames=exampleFrames(unit,mode);
    host.dataset.playing=String(playing);
    host.querySelector('[data-example-stage]').innerHTML=stage(unit,index,html,mode);
    host.querySelector('[data-example-caption]').innerHTML=`<span class="example-step-number" aria-hidden="true">${index+1}</span><span>${html(frames[index].text)}</span>`;
    host.querySelector('[data-example-count]').textContent=`${index+1} / ${frames.length}`;
    host.querySelector('[data-example-action=previous]').disabled=index===0;
    host.querySelector('[data-example-action=next]').disabled=index===frames.length-1;
    const play=host.querySelector('[data-example-action=play]');play.textContent=playing?'Ⅱ Pause':index===frames.length-1?'↻ Replay example':'▷ Watch example';play.setAttribute('aria-pressed',String(playing));
    host.querySelectorAll?.('[data-example-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.exampleMode===mode)));
  }});
  let player=makePlayer();
  host.addEventListener('click',event=>{
    const selected=event.target.closest('[data-example-mode]')?.dataset.exampleMode;
    if(unit.id==='math-2'&&['stock','money','trade'].includes(selected)){player.dispose();mode=selected;player=makePlayer();player.step(0);return;}
    const action=event.target.closest('[data-example-action]')?.dataset.exampleAction;
    if(action==='play')player.play();else if(action==='previous')player.step(-1);else if(action==='next')player.step(1);
  });
  const hidden=()=>{if(document.hidden)player.stop();};document.addEventListener('visibilitychange',hidden);
  return {stop:()=>player.stop(),dispose(){player.dispose();document.removeEventListener('visibilitychange',hidden);}};
}
