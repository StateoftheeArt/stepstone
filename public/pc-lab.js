import {languageAllowed,displayUserText,LANGUAGE_MESSAGE} from './language.js?build=121';
import {escapeHTML as esc} from './engine.js?build=121';

// A rehearsal inside a lesson draft. It never calls an OS, shell or account API.
export function pcState(task,work){
  work.pc??={step:0,text:'Milk, bread',saved:'',backup:'',message:''};
  const state=work.pc;
  if(!Number.isInteger(state.step)||state.step<0||state.step>task.screens.length)state.step=0;
  return state;
}
export function pcComplete(task,work){return work.pc?.step===task.screens.length;}
export function pcAction(task,work,index){
  const state=pcState(task,work),screen=task.screens[state.step],action=screen?.actions[index];
  if(!action)return false;
  if(!action.correct){state.message=action.feedback;return false;}
  if(!languageAllowed(state.text)){state.message=LANGUAGE_MESSAGE;return false;}
  if(screen.input&&!state.text.trim()){state.message='Type an item first.';return false;}
  if(screen.contextMenu&&!state.menu){state.message='Open the edit menu first.';return false;}
  if(screen.move&&!state.moved){state.message='Move the Notes window first. Drag its title bar or use the move buttons.';return false;}
  if(task.id==='pc-open'&&state.step===4)state.compact=true;
  if(task.id==='pc-save'&&state.step===2)state.saved=state.text;
  if(task.id==='pc-backup'&&state.step===0){state.saved=state.text;state.backup=state.text;}
  if(task.id==='pc-backup'&&state.step===1)state.saved='Wrong practice item';
  if(task.id==='pc-backup'&&state.step===2)state.saved=state.backup;
  state.step++;state.message='';return true;
}
export function mountPC(host,task,work,onChange){
  const state=pcState(task,work),screen=task.screens[state.step],done=!screen;
  const icons={desktop:'▦',menu:'▤',window:'▣',files:'▱',backup:'⇄',settings:'⚙',text:'Aa','large-text':'Aa',editor:'≡',warning:'!',message:'✉',apps:'▦',browser:'⌕',update:'↻'};
  host.innerHTML=`<div class="pc-rehearsal"><div class="pc-label"><strong>Practice computer</strong><span>Simulation · no real device changes</span></div><div class="pc-window"><div class="pc-titlebar"><span aria-hidden="true">${icons[screen?.scene]||'✓'}</span><strong>${esc(screen?.title||'Rehearsal complete')}</strong><span aria-hidden="true">− □ ×</span></div><div class="pc-screen ${screen?.scene==='large-text'?'pc-large':''}">${done?`<p class="pc-complete">✓ ${esc(task.why)}</p>${task.id==='pc-save'||task.id==='pc-backup'?`<div class="pc-note"><strong>Reopened practice note</strong><p>${esc(displayUserText(state.saved||state.text))}</p></div>`:''}`:`<p class="pc-target"><span aria-hidden="true">➜</span> ${esc(screen.body)}</p>${screen.input?`<label class="field">${esc(screen.input)}<textarea data-pc-note maxlength="300">${esc(state.text)}</textarea></label>`:screen.scene==='editor'?`<div class="pc-note"><strong>Practice note</strong><p>${esc(task.id==='pc-undo'?(state.step===0?'Meet on Tuesday':'Meet on Thursday'):displayUserText(state.text))}</p></div>`:screen.scene==='large-text'||screen.scene==='text'?'<p class="pc-preview-text">This is the text preview.</p>':''}<div class="pc-tools">${screen.actions.map((a,i)=>`<button class="btn ${i?'secondary':''}" data-pc-action="${i}">${esc(a.label)}</button>`).join('')}</div>`}<p class="pc-feedback" role="status">${esc(state.message)}</p></div><div class="pc-taskbar"><span aria-hidden="true">▦</span><span>${done?'Ready to explain the steps':`Action ${state.step+1} of ${task.screens.length}`}</span><progress max="${task.screens.length}" value="${state.step}" aria-label="Practice computer steps completed"></progress></div></div><button class="btn secondary small" data-pc-restart>Try this rehearsal again</button></div>`;
  const input=host.querySelector('[data-pc-note]');if(input)input.oninput=()=>{state.text=input.value;state.message='';work.checked=false;onChange(false);};
  host.querySelectorAll('[data-pc-action]').forEach(b=>b.onclick=()=>{pcAction(task,work,Number(b.dataset.pcAction));work.checked=false;onChange(true);});
  host.querySelector('[data-pc-restart]').onclick=()=>{work.pc={step:0,text:'Milk, bread',saved:'',backup:'',message:''};work.checked=false;onChange(true);};
  if(screen?.contextMenu){
    const panel=host.querySelector('.pc-tools');panel.hidden=!state.menu;
    panel.insertAdjacentHTML('beforebegin','<button class="btn secondary" data-edit-menu aria-expanded="'+!!state.menu+'">Open edit menu</button>');
    const opener=host.querySelector('[data-edit-menu]'),openMenu=()=>{state.menu=true;panel.hidden=false;opener.setAttribute('aria-expanded','true');panel.querySelector('button')?.focus();onChange(false);};
    opener.onclick=openMenu;opener.onkeydown=e=>{if(e.key==='F10'&&e.shiftKey){e.preventDefault();openMenu();}};
    host.querySelector('.pc-note').oncontextmenu=e=>{e.preventDefault();openMenu();};
  }
  if(task.id==='pc-open'&&(state.step>=3||done)){
    host.querySelector('.pc-screen').insertAdjacentHTML('afterbegin',`<div class="pc-desk" aria-label="Two practice windows"><div class="pc-calendar"><strong>Calendar</strong><p>Thursday<br>Practice session</p></div><div class="pc-movable ${state.compact?'compact':''}" style="transform:translate(${Number(state.x)||0}px,${Number(state.y)||0}px)"><button class="pc-grip" aria-label="Move Notes window with arrow keys or drag" ${!screen?.move?'disabled':''}>Notes · drag here ↔</button><p>shopping.txt<br>Milk, bread</p></div></div>${screen?.move?'<div class="buttons pc-move-tools"><button class="btn secondary small" data-window-move="left">Move left</button><button class="btn secondary small" data-window-move="right">Move right</button><button class="btn secondary small" data-window-move="down">Move down</button></div>':''}`);
    if(screen?.move){
      const desk=host.querySelector('.pc-desk'),window=host.querySelector('.pc-movable'),grip=host.querySelector('.pc-grip');
      const move=(x,y)=>{const oldX=state.x||0,oldY=state.y||0;state.x=Math.max(0,Math.min(Math.max(0,desk.clientWidth-window.offsetWidth),x));state.y=Math.max(0,Math.min(100,y));if(state.x!==oldX||state.y!==oldY)state.moved=true;state.message='';work.checked=false;window.style.transform=`translate(${state.x}px,${state.y}px)`;onChange(false);};
      let start=null;
      grip.onpointerdown=e=>{if(e.button>0)return;grip.setPointerCapture(e.pointerId);start={id:e.pointerId,x:e.clientX,y:e.clientY,left:Number(state.x)||0,top:Number(state.y)||0};};
      grip.onpointermove=e=>{if(start?.id===e.pointerId&&Math.hypot(e.clientX-start.x,e.clientY-start.y)>3)move(start.left+e.clientX-start.x,start.top+e.clientY-start.y);};
      grip.onpointerup=grip.onpointercancel=grip.onlostpointercapture=()=>{start=null;};
      grip.onkeydown=e=>{const delta={ArrowLeft:[-20,0],ArrowRight:[20,0],ArrowUp:[0,-20],ArrowDown:[0,20]}[e.key];if(delta){e.preventDefault();move((state.x||0)+delta[0],(state.y||0)+delta[1]);}};
      host.querySelectorAll('[data-window-move]').forEach(b=>b.onclick=()=>{const d=b.dataset.windowMove;move((state.x||0)+(d==='left'?-30:d==='right'?30:0),(state.y||0)+(d==='down'?30:0));});
    }
  }
  if(task.id==='pc-backup'&&state.backup){host.querySelector('.pc-screen').insertAdjacentHTML('afterbegin',`<div class="pc-copies"><div><strong>${state.step>=3?'Recovered':'Original'} note</strong><p>${esc(state.saved)}</p></div><div><strong>Separate backup</strong><p>${esc(state.backup)}</p></div></div>`);}
}
