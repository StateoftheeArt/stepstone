// Pointer events support fingers, pens and mice; buttons keep tap/keyboard access.
let active=null;
export function cancelMove(){
  if(!active)return;
  active.ghost?.remove();active.target?.classList.remove('drop-ready');
  active=null;
}
let lifecycleBound=false;

export function wireMoves(host,{source='[data-move]',target='[data-drop]',ghost,onDrop,centerGhost=false}){
  if(!lifecycleBound){document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelMove();});window.addEventListener('hashchange',cancelMove);lifecycleBound=true;}
  let suppressClickUntil=0,suppressClickSource=null;
  host.addEventListener('pointerdown',event=>{
    const el=event.target.closest(source);
    if(!el||!host.contains(el)||el.disabled||event.button>0)return;
    cancelMove();active={host,el,id:event.pointerId,x:event.clientX,y:event.clientY,moved:false};
    el.setPointerCapture(event.pointerId);
  });
  host.addEventListener('pointermove',event=>{
    if(!active||active.host!==host||active.id!==event.pointerId)return;
    if(!active.moved&&Math.hypot(event.clientX-active.x,event.clientY-active.y)<8)return;
    event.preventDefault();active.moved=true;
    if(!active.ghost){active.ghost=document.createElement('div');active.ghost.className='move-ghost';active.ghost.setAttribute('aria-hidden','true');active.ghost.innerHTML=typeof ghost==='function'?ghost(active.el):ghost;document.body.append(active.ghost);}
    const size=centerGhost?active.ghost.getBoundingClientRect():null;
    active.ghost.style.transform=`translate(${event.clientX-(size?size.width/2:24)}px,${event.clientY-(size?size.height/2:30)}px)`;
    active.target?.classList.remove('drop-ready');
    active.target=document.elementFromPoint(event.clientX,event.clientY)?.closest(target);
    if(active.target&&host.contains(active.target)&&active.target!==active.el)active.target.classList.add('drop-ready');
  });
  host.addEventListener('pointerup',event=>{
    if(!active||active.host!==host||active.id!==event.pointerId)return;
    const {el,moved}=active,destination=document.elementFromPoint(event.clientX,event.clientY)?.closest(target);
    cancelMove();
    if(moved){suppressClickUntil=performance.now()+500;suppressClickSource=el;event.preventDefault();if(destination&&host.contains(destination)&&destination!==el)onDrop(el,destination);}
  });
  host.addEventListener('pointercancel',()=>{if(active?.host===host)cancelMove();});
  host.addEventListener('lostpointercapture',()=>{if(active?.host===host)cancelMove();});
  host.addEventListener('click',event=>{if(performance.now()<suppressClickUntil&&event.target.closest(source)===suppressClickSource){suppressClickUntil=0;suppressClickSource=null;event.preventDefault();event.stopImmediatePropagation();}},true);
}
