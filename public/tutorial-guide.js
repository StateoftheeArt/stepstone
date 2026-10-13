// A single pointer follows the next real control. It never intercepts that
// control, changes a learner's answer, or advances the saved tutorial.
export function createTourGuide({root,dialog,guidePet=()=>{},readButton=()=>''}){
  let target,layer,bubble,arrow,slot,anchor,frame=0,request,lastKey='',description;
  const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
  function clearTarget(){
    if(!target)return;
    target.classList.remove('tour-target');
    if(description===null)target.removeAttribute('aria-describedby');
    else if(description!==undefined)target.setAttribute('aria-describedby',description);
    target=null;description=undefined;
  }
  function hide(){
    guidePet(null);cancelAnimationFrame(frame);frame=0;clearTarget();layer?.remove();slot?.remove();layer=bubble=arrow=slot=anchor=null;lastKey='';request=null;
    window.removeEventListener('scroll',queue,true);window.removeEventListener('resize',queue);
    window.visualViewport?.removeEventListener('resize',queue);window.visualViewport?.removeEventListener('scroll',queue);
    observer.disconnect();
  }
  function prepare(){
    cancelAnimationFrame(frame);frame=0;request=null;clearTarget();lastKey='';
    if(slot){layer.append(bubble);slot.remove();slot=null;}anchor=null;
    if(layer)layer.hidden=true;
  }
  function queue(){if(!frame&&request)frame=requestAnimationFrame(()=>{frame=0;place();});}
  const observer=new ResizeObserver(queue);
  function mount(){
    layer=document.createElement('div');layer.className='tour-pointer';
    layer.innerHTML='<div class="tour-callout" id="tour-control-hint" role="note"><svg class="tour-arrow" aria-hidden="true"><path class="tour-arrow-line"/><path class="tour-arrow-head"/></svg><div class="tour-dialogue"><div class="tour-pet-seat" data-guide-pet aria-hidden="true"></div><div class="tour-dialogue-copy"><span class="tour-callout-label"></span><h2 class="tour-dialogue-title"></h2><p class="tour-dialogue-detail"></p>'+readButton('tour-control-hint','Read guide aloud')+'<button type="button" class="btn secondary small" data-tour="locate" hidden>Show me where ↓</button></div></div></div>';
    bubble=layer.querySelector('.tour-callout');arrow=layer.querySelector('svg');
    document.body.append(layer);
    window.addEventListener('scroll',queue,true);window.addEventListener('resize',queue);
    window.visualViewport?.addEventListener('resize',queue);window.visualViewport?.addEventListener('scroll',queue);
    observer.observe(bubble);observer.observe(root);
  }
  function useTarget(next){
    if(next===target)return;
    clearTarget();target=next;
    if(target){description=target.getAttribute('aria-describedby');target.setAttribute('aria-describedby',[description,'tour-control-hint'].filter(Boolean).join(' '));target.classList.add('tour-target');}
  }
  function attach(){
    const floating=!!target.closest('#app-header');
    const nextAnchor=floating?null:target.closest('.packing-board,.buttons,.activity-tools,.field')||target;
    if(nextAnchor!==anchor||floating&&slot){
      if(slot){layer.append(bubble);slot.remove();slot=null;}
      anchor=nextAnchor;
      if(anchor){slot=document.createElement('div');slot.className='tour-guide-slot';anchor.before(slot);slot.append(bubble);}
    }
    layer.classList.toggle('tour-floating',floating);bubble.classList.toggle('tour-inline',!floating);
    bubble.dataset.tone=request.tone||'action';
    return floating;
  }
  function place(){
    if(!request||!layer)return;
    const modal=dialog.open;
    const next=modal?(request.breakStep?dialog.querySelector('.pause-card [data-action="close"]'):null):document.querySelector(request.selector);
    if(!next||next.disabled||!next.getClientRects().length){layer.hidden=true;guidePet(null);if(slot)slot.hidden=true;clearTarget();if(modal)lastKey='';return;}
    useTarget(next);
    // A modal is in the browser's top layer; keep its pointer there too.
    const host=modal?dialog:document.body;if(layer.parentElement!==host)host.append(layer);
    layer.hidden=false;const floating=attach();if(slot)slot.hidden=false;
    const view=window.visualViewport,top=(view?.offsetTop||0)+12,left=(view?.offsetLeft||0)+12;
    const right=left+(view?.width||innerWidth)-24;
    const bottom=(view?.offsetTop||0)+(view?.height||innerHeight)-12;
    bubble.style.width=floating?Math.min(440,right-left)+'px':'';
    if(!floating)bubble.querySelector('[data-tour=locate]').hidden=true;
    const r=target.getBoundingClientRect();
    if(!floating){
      bubble.style.width='';bubble.style.left='';bubble.style.top='';bubble.querySelector('[data-tour=locate]').hidden=true;
      const bounds=slot.getBoundingClientRect();
      const end=r.left+r.width/2;
      bubble.style.marginLeft=clamp(end-bounds.left-bubble.offsetWidth/2,0,Math.max(0,bounds.width-bubble.offsetWidth))+'px';
      const b=bubble.getBoundingClientRect();
      // The dialogue reserves space in the page. Its attached arrow stays in
      // that gap, centered on the real control, and moves with the dialogue.
      const x=clamp(end,b.left+18,b.right-18);
      draw(x,b.bottom+1,end,r.top-7);
      arrow.toggleAttribute('hidden',b.bottom<top||r.top>bottom||r.top<b.bottom);
      guidePet(bubble.querySelector('[data-guide-pet]'),request.key);return;
    }
    bubble.style.marginLeft='';arrow.removeAttribute('hidden');
    const offscreen=r.bottom<top+12||r.top>bottom-12;
    const find=bubble.querySelector('[data-tour=locate]');find.hidden=!offscreen;
    const b=bubble.getBoundingClientRect(),gap=26,headerBottom=Math.max(r.bottom,document.querySelector('#app-header')?.getBoundingClientRect().bottom||r.bottom,root.querySelector('.tour-tools')?.getBoundingClientRect().bottom||0);
    let x=clamp(r.left+r.width/2-b.width/2,left,right-b.width),y,side;
    if(offscreen){side=r.top>bottom?'down':'up';y=side==='down'?bottom-b.height:top;}
    else if(r.top-gap-b.height>=top){side='down';y=r.top-gap-b.height;}
    else if(headerBottom+gap+b.height<=bottom){side='up';y=headerBottom+gap;}
    else if(r.right+gap+b.width<=right){side='left';x=r.right+gap;y=clamp(r.top,top,bottom-b.height);}
    else if(r.left-gap-b.width>=left){side='right';x=r.left-gap-b.width;y=clamp(r.top,top,bottom-b.height);}
    else {
      // A tall target may fill a small screen. A compact cue goes just above
      // it, and the learner can scroll normally; it must not cover the target.
      layer.hidden=true;guidePet(null);return;
    }
    bubble.style.left=x+'px';bubble.style.top=y+'px';bubble.dataset.side=side;
    let sx,sy,ex,ey;
    if(side==='down'||side==='up'){
      sx=ex=clamp(r.left+r.width/2,x+22,x+b.width-22);
      sy=side==='down'?y+b.height:y;ey=offscreen?(side==='down'?bottom+7:top-7):(side==='down'?r.top-7:r.bottom+7);
    }else{sy=ey=clamp(r.top+r.height/2,y+18,y+b.height-18);sx=side==='left'?x:x+b.width;ex=side==='left'?r.right+7:r.left-7;}
    draw(sx,sy,ex,ey);guidePet(bubble.querySelector('[data-guide-pet]'),request.key);
  }
  function draw(sx,sy,ex,ey){
    const bounds=bubble.getBoundingClientRect(),left=Math.min(sx,ex)-12,top=Math.min(sy,ey)-12;
    arrow.style.left=left-bounds.left-bubble.clientLeft+'px';
    arrow.style.top=top-bounds.top-bubble.clientTop+'px';
    arrow.setAttribute('width',Math.abs(ex-sx)+24);arrow.setAttribute('height',Math.abs(ey-sy)+24);
    sx-=left;ex-=left;sy-=top;ey-=top;
    const angle=Math.atan2(ey-sy,ex-sx),a=8;
    arrow.querySelector('.tour-arrow-line').setAttribute('d',`M${sx},${sy}L${ex},${ey}`);
    arrow.querySelector('.tour-arrow-head').setAttribute('d',`M${ex-a*Math.cos(angle-.65)},${ey-a*Math.sin(angle-.65)}L${ex},${ey}L${ex-a*Math.cos(angle+.65)},${ey-a*Math.sin(angle+.65)}`);
  }
  function show(next){
    request=next;if(!layer)mount();
    bubble.querySelector('.tour-callout-label').textContent='STEP '+next.number+' OF '+next.total;
    bubble.querySelector('.tour-dialogue-title').textContent=next.title;
    bubble.querySelector('.tour-dialogue-detail').textContent=next.text||next.detail||'';
    layer.dataset.tone=next.tone||'action';
    const key=next.key+':'+next.selector;
    if(key!==lastKey){lastKey=key;
      // Wait until the route's normal scroll reset and the activity's paint
      // have finished. Never jump past the worked example to its last button.
      requestAnimationFrame(()=>{if(request!==next)return;place();const el=target;
        // Settle the next control immediately so a click cannot chase a moving target.
        if(next.reveal!==false&&el?.getClientRects().length&&!el.closest('#navigation')){const r=el.getBoundingClientRect(),b=(slot||el).getBoundingClientRect(),height=window.visualViewport?.height||innerHeight;if(b.top<20||r.bottom>height-100)(slot||el).scrollIntoView({block:'nearest',behavior:'instant'});}
        queue();});
    }
    queue();
  }
  return {show,hide,prepare,refresh:queue};
}
