import {playPipAction,pipPlayLabel,stopAllPipActions} from './pip-moves.js?build=122';
import {escapeHTML as esc} from './engine.js?build=122';
import {companionSprite} from './companion.js?build=122';
import {itemIcon} from './wins.js?build=122';
import {foodRemaining,canFeedPip,canPipPlay} from './pip-food.js?build=122';
import {createPipRoomLife} from './pip-room.js?build=122';

export function pictureDropdown({id,label,name,items,selected,avatar='fox',completed=0,owned=[]}){
  const choice=items.find(c=>c.id===selected)||items[0];
  const picture=c=>name==='avatar'?companionSprite(c.id,48):companionSprite(avatar,48,c.id);
  return `<details class="pip-card-dropdown" data-choice-name="${name}" id="${id}"><summary aria-controls="${id}-cards"><span>${label}</span><span class="pip-dropdown-value">${picture(choice)}<strong data-choice-label>${esc(choice.label)}</strong><span aria-hidden="true">⌄</span></span></summary><div class="pip-option-cards" id="${id}-cards" role="radiogroup" aria-label="${label}">${items.map(c=>{const locked=(c.modules||0)>completed&&!owned.includes(name+':'+c.id)&&selected!==c.id;return `<label class="pip-option-card ${locked?'is-locked':''}"><input type="radio" name="${name}" value="${c.id}" ${c.id===selected?'checked':''} ${locked?'disabled':''}><span class="pip-card-picture">${picture(c)}</span><span>${esc(c.label)}</span>${locked?`<small>${c.modules} modules</small>`:''}</label>`;}).join('')}</div></details>`;
}

const titles={wall:'Room colours',rug:'Rugs',furniture:'Furniture',decor:'Decorations',painting:'Paintings',shelf:'Shelves',bowl:'Food bowls',curtains:'Curtains'};
export function homeChoiceMarkup(field,value,label){
  const empty={rug:'Choose a rug',furniture:'Choose furniture',decor:'Choose a decoration',painting:'Choose a painting',shelf:'Choose a shelf',curtains:'Choose curtains'};
  return (value==='none'?'<span class="pip-add-item" aria-hidden="true">+</span>':itemIcon({key:'home.'+field+':'+value}))+'<strong>'+esc(value==='none'?(empty[field]||'Choose an item'):label)+'</strong><span aria-hidden="true">⌄</span>';
}
export function homeShelf(options,profile,completed=0,owned=[]){
  return `<section class="pip-item-shelf" aria-label="Home items"><h3>Home items</h3><div class="pip-shelf-scroll" tabindex="0" aria-label="Home item menus">${Object.entries(options).map(([field,items])=>{const value=profile.home?.[field]||items[0].id,choice=items.find(i=>i.id===value)||items[0];return `<details class="pip-shelf-group"><summary><span>${titles[field]}</span><span class="pip-home-choice" data-home-choice="${field}">${homeChoiceMarkup(field,value,choice.label)}</span></summary><div class="pip-shelf-cards">${items.filter(item=>item.id!=='none').map(item=>{const active=item.id===value,key='home.'+field+':'+item.id,locked=item.modules>completed&&!owned.includes(key)&&!active;return `<button type="button" class="pip-shelf-item ${locked?'is-locked':''}" data-home-item="${field}" data-home-value="${item.id}" data-item-label="${esc(item.label)}" aria-pressed="${active}" ${locked?'disabled':''} draggable="false"><span class="pip-shelf-picture" data-item-kind="${field}" data-item-id="${item.id}">${itemIcon({key})||'<span class="pip-empty-item" aria-hidden="true">−</span>'}</span><span>${esc(item.label)}</span>${locked?`<small>${item.modules} modules</small>`:active?'<small>In room</small>':'<small>Place</small>'}</button>`;}).join('')}</div><input type="hidden" name="home_${field}" value="${esc(value)}"></details>`;}).join('')}</div><input type="hidden" name="homePositions" value="${esc(JSON.stringify(profile.homePositions||{}))}"></section>`;
}

export function pipFoodControls(state,{species='fox',name='Pip'}={}){
  const remaining=foodRemaining(state),portion=state?.portionSeconds||1800,bank=state?.bank||0;
  return `<div class="pip-care" data-pip-care><div class="pip-food-label"><span>Food bowl</span><span data-food-time>${remaining>0?Math.ceil(remaining/60)+' min':'Empty'}</span></div><meter min="0" max="${state?.capacity||5400}" value="${remaining}" aria-label="Food remaining in Pip’s bowl" data-food-meter></meter><div class="pip-care-buttons pip-play-buttons"><button class="btn secondary" type="button" data-pip-feed ${canFeedPip(state)?'':'disabled'}>Feed Pip <span data-food-bank>· ${bank} ${bank===1?'portion':'portions'}</span></button><button class="btn secondary" type="button" data-pip-play ${canPipPlay(state)?'':'disabled'}>${esc(pipPlayLabel(species))}</button></div><p class="sr-only" data-pip-status role="status">Tap ${esc(name)} to try three dances. ${remaining>0?'Ready for a little game.':'Feed for games.'}</p></div>`;
}

export function paintFood(form,state){
  if(!form)return;
  const remaining=foodRemaining(state),canPlay=canPipPlay(state),feed=form.querySelector('[data-pip-feed]');
  form.querySelector('[data-food-meter]')?.setAttribute('value',remaining);
  const time=form.querySelector('[data-food-time]');if(time)time.textContent=remaining>0?Math.ceil(remaining/60)+' min':'Empty';
  const bank=form.querySelector('[data-food-bank]');if(bank)bank.textContent='· '+(state?.bank||0)+' '+(state?.bank===1?'portion':'portions');
  if(feed&&!feed.dataset.feeding)feed.disabled=!canFeedPip(state);
  const activity=pipPlayLabel(form.querySelector('[name=avatar]:checked')?.value||'fox'),name=form.querySelector('[name=alias]')?.value||'Pip';
  form.querySelectorAll('[data-pip-play]').forEach(button=>{button.disabled=!canPlay;button.textContent=activity;button.setAttribute('aria-label',canPlay?activity+' with '+name:name+' is resting. Feed for '+activity.toLowerCase()+'.');});
  const room=form.querySelector('.pip-home');room?.classList.toggle('pip-resting',!canPlay);if(room){room.dataset.pipResting=String(!canPlay);if(!room.dataset.pipInteracting)room.dataset.pose=canPlay?'idle':'resting';}
  const food=form.querySelector('[data-bowl-food]');if(food)food.style.transform=`scaleX(${Math.min(1,remaining/(state?.capacity||5400))})`;
  const note=form.querySelector('[data-pip-status]');if(note&&!room?.dataset.pipInteracting){const message='Tap '+(form.querySelector('[name=alias]')?.value||'Pip')+' to try three dances. '+(canPlay?'Ready for a little game.':'Feed for games.');if(note.textContent!==message)note.textContent=message;}
}

export function installPipEditor({preview,food,feed,motion,toast,onPlay=()=>{}}){
  const formOf=el=>el?.closest('form[data-form="profile"]');
  let gesture=null,ignoreClick=false;const interactions=new WeakMap(),selectedItems=new WeakMap();
  const roomLife=createPipRoomLife({motion,fed:()=>canPipPlay(food()),name:room=>formOf(room)?.querySelector('[name=alias]')?.value||'Pip'});
  function choose(form,field,value,point){
    const input=form.querySelector(`[name="home_${field}"]`);if(!input)return;
    input.value=value;
    if(point&&['rug','furniture','decor','painting','shelf'].includes(field)){const positions=form.querySelector('[name="homePositions"]');const data=JSON.parse(positions.value||'{}');data[field]=point;positions.value=JSON.stringify(data);}
    form.querySelectorAll(`[data-home-item="${field}"]`).forEach(button=>{const active=button.dataset.homeValue===value;button.setAttribute('aria-pressed',String(active));const small=button.querySelector('small');if(small&&!button.disabled)small.textContent=active?'In room':'Place';});
    const current=form.querySelector(`[data-home-choice="${field}"]`),chosen=form.querySelector(`[data-home-item="${field}"][data-home-value="${CSS.escape(value)}"]`);
    if(current)current.innerHTML=homeChoiceMarkup(field,value,chosen?.dataset.itemLabel||'');
    preview({target:input});paintFood(form,food());
    const menu=chosen?.closest('details')||current?.closest('details');menu?.removeAttribute('open');
    if(point)form.querySelector(`[data-placed-item="${field}"]`)?.focus({preventScroll:true});else menu?.querySelector('summary')?.focus({preventScroll:true});
  }
  const movable=['rug','furniture','decor','painting','shelf','curtains'];
  const onWall=field=>field==='painting'||field==='shelf';
  function dropPoint(room,x,y,field){const r=room.getBoundingClientRect();return {x:Math.max(.08,Math.min(.92,(x-r.left)/r.width)),y:Math.max(onWall(field)?.08:.25,Math.min(onWall(field)?.64:.87,(y-r.top)/r.height))};}
  function putBack(form,field){
    if(!movable.includes(field)||form.querySelector(`[name="home_${field}"]`)?.value==='none')return;
    choose(form,field,'none');selectedItems.delete(form);
    form.querySelector('[data-home-trash]')?.focus({preventScroll:true});
  }
  document.addEventListener('focusin',e=>{const piece=e.target.closest('[data-placed-item]');if(piece)selectedItems.set(formOf(piece),piece.dataset.placedItem);});

  document.addEventListener('click',async e=>{
    const item=e.target.closest('[data-home-item]'),trash=e.target.closest('[data-home-trash]'),button=e.target.closest('[data-pip-feed]'),play=e.target.closest('[data-pip-play]'),greet=e.target.closest('[data-pip-greet]');
    const form=formOf(item||trash||button||play||greet);if(!form)return;
    if(item){if(ignoreClick){ignoreClick=false;return;}if(!item.disabled)choose(form,item.dataset.homeItem,item.dataset.homeValue);return;}
    if(trash){putBack(form,selectedItems.get(form));return;}
    const pipName=form.querySelector('[name=alias]')?.value||'Pip';
    if(greet){const room=form.querySelector('[data-home-room]'),n=interactions.get(form)||0;interactions.set(form,n+1);roomLife.pause(room,3400);if(canPipPlay(food()))onPlay();playPipAction(room,form.querySelector('[name=avatar]:checked')?.value,{dance:n%3+1,name:pipName,motion:motion()});return;}
    if(button){button.disabled=true;button.dataset.feeding='true';try{await feed();preview({target:button});const room=form.querySelector('[data-home-room]');roomLife.sync();roomLife.pause(room,2100);playPipAction(room,form.querySelector('[name=avatar]:checked')?.value,{snack:true,name:pipName,motion:motion()});}catch(error){toast(error.message);}finally{delete button.dataset.feeding;paintFood(form,food());}return;}
    if(play){const state=food();if(!canPipPlay(state)){paintFood(form,state);toast('Feed Pip to play.');return;}onPlay();const room=form.querySelector('[data-home-room]');roomLife.pause(room,3400);playPipAction(room,form.querySelector('[name=avatar]:checked')?.value,{name:pipName,motion:motion()});}

  });
  document.addEventListener('toggle',e=>{const opened=e.target;if(!opened.matches?.('.pip-card-dropdown')||!opened.open)return;formOf(opened)?.querySelectorAll('.pip-card-dropdown[open]').forEach(other=>{if(other!==opened)other.open=false;});},true);
  document.addEventListener('change',e=>{const drop=e.target.closest('.pip-card-dropdown');if(!drop||!e.target.matches('input[type="radio"]'))return;const form=formOf(drop),label=e.target.closest('label'),summary=drop.querySelector('summary'),species=form.querySelector('[name=avatar]:checked')?.value||'fox';summary.querySelector('[data-choice-label]').textContent=label.querySelector('.pip-card-picture+span').textContent;summary.querySelector('.companion-sprite').outerHTML=companionSprite(species,48,e.target.name==='accessory'?e.target.value:'none');if(e.target.name==='avatar'){const accessories=form.querySelector('[data-choice-name=accessory]');accessories?.querySelectorAll('.pip-option-card').forEach(card=>{const value=card.querySelector('input').value;card.querySelector('.pip-card-picture').innerHTML=companionSprite(species,48,value);});const selected=form.querySelector('[name=accessory]:checked')?.value||'none';const image=accessories?.querySelector('summary .companion-sprite');if(image)image.outerHTML=companionSprite(species,48,selected);}drop.open=false;summary.focus({preventScroll:true});paintFood(form,food());});
  document.addEventListener('keydown',e=>{const drop=e.target.closest('.pip-card-dropdown,.pip-shelf-group');if(e.key==='Escape'&&drop?.open){e.preventDefault();e.stopPropagation();drop.open=false;drop.querySelector('summary').focus();}} ,true);
  document.addEventListener('keydown',e=>{
    const piece=e.target.closest('[data-placed-item]');if(!piece)return;
    const form=formOf(piece),field=piece.dataset.placedItem;
    if(e.key==='Delete'||e.key==='Backspace'){e.preventDefault();putBack(form,field);return;}
    const delta={ArrowLeft:[-.03,0],ArrowRight:[.03,0],ArrowUp:[0,-.03],ArrowDown:[0,.03]}[e.key];if(!delta)return;
    e.preventDefault();const positions=JSON.parse(form.querySelector('[name="homePositions"]').value||'{}'),r=piece.closest('[data-placed-kind]').getBoundingClientRect(),room=form.querySelector('[data-home-room]'),old=positions[field]||dropPoint(room,r.left+r.width/2,r.top+r.height/2,field);
    choose(form,field,piece.dataset.placedValue,{x:Math.max(.08,Math.min(.92,old.x+delta[0])),y:Math.max(onWall(field)?.08:.25,Math.min(onWall(field)?.64:.87,old.y+delta[1]))});
  });
  const contains=(element,x,y)=>{if(!element)return false;const r=element.getBoundingClientRect();return x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;};
  function tidyDrag(g){
    if(!g)return;g.ghost?.remove();g.item.classList.remove('pip-item-dragging');
    g.room?.classList.remove('pip-drop-ready','pip-room-dragging');g.room?.querySelector('[data-home-trash]')?.classList.remove('is-drop-target');
    try{if(g.item.hasPointerCapture?.(g.id))g.item.releasePointerCapture(g.id);}catch{}
  }
  function cancelDrag(){const g=gesture;gesture=null;tidyDrag(g);if(g)roomLife.resume(g.room);}
  function followPointer(g,x,y){
    if(!g.ghost){
      const ghost=document.createElement('div');ghost.className='pip-placed-item pip-drag-preview';ghost.dataset.placedKind=g.field;ghost.dataset.placedId=g.value;ghost.setAttribute('aria-hidden','true');ghost.innerHTML=itemIcon({key:'home.'+g.field+':'+g.value});
      (g.item.closest('dialog')||document.body).append(ghost);g.ghost=ghost;g.item.classList.add('pip-item-dragging');g.room.classList.add('pip-room-dragging');
    }
    g.ghost.style.left=x+'px';g.ghost.style.top=y+'px';
    const bin=g.room.querySelector('[data-home-trash]');bin?.classList.toggle('is-drop-target',contains(bin,x,y));
    g.room.classList.toggle('pip-drop-ready',contains(g.room,x,y)&&!contains(bin,x,y));
  }
  // A single pointer gesture moves a visible preview; only the bin removes an item.
  document.addEventListener('dragstart',e=>{if(e.target.closest('[data-home-item],[data-placed-item]'))e.preventDefault();});
  document.addEventListener('pointerdown',e=>{
    const item=e.target.closest('[data-home-item],[data-placed-item]');if(!item||item.disabled||e.button!==0)return;
    const field=item.dataset.homeItem||item.dataset.placedItem,value=item.dataset.homeValue||item.dataset.placedValue;
    if(!movable.includes(field)||value==='none')return;
    cancelDrag();const form=formOf(item),room=form?.querySelector('[data-home-room]');if(!room)return;
    roomLife.pause(room);
    selectedItems.set(form,field);gesture={id:e.pointerId,item,form,room,field,value,x:e.clientX,y:e.clientY,moved:false,ghost:null};
    try{item.setPointerCapture?.(e.pointerId);}catch{}
  });
  document.addEventListener('pointermove',e=>{
    const g=gesture;if(!g||g.id!==e.pointerId)return;
    if(!g.moved&&Math.hypot(e.clientX-g.x,e.clientY-g.y)<6)return;
    g.moved=true;e.preventDefault();followPointer(g,e.clientX,e.clientY);
  },{passive:false});
  document.addEventListener('pointerup',e=>{
    const g=gesture;if(!g||g.id!==e.pointerId)return;gesture=null;
    try{
      if(!g.moved)return;
      ignoreClick=true;setTimeout(()=>ignoreClick=false,0);
      if(contains(g.room.querySelector('[data-home-trash]'),e.clientX,e.clientY)){
        if(g.value===g.form.querySelector(`[name="home_${g.field}"]`)?.value)putBack(g.form,g.field);
      }
      else if(contains(g.room,e.clientX,e.clientY))choose(g.form,g.field,g.value,dropPoint(g.room,e.clientX,e.clientY,g.field));
    }finally{tidyDrag(g);roomLife.resume(g.room);}
  });
  document.addEventListener('pointercancel',cancelDrag);
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&gesture){e.preventDefault();e.stopPropagation();cancelDrag();}},true);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelDrag();stopAllPipActions();}});
  document.addEventListener('change',()=>queueMicrotask(()=>{if(!motion())stopAllPipActions();roomLife.sync();}));
  globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').addEventListener?.('change',()=>{if(!motion())stopAllPipActions();roomLife.sync();});
  document.addEventListener('pointerdown',e=>{const pip=e.target.closest('[data-pip-greet]');if(pip)roomLife.pause(formOf(pip)?.querySelector('[data-home-room]'),3400);});
  document.addEventListener('pointermove',e=>{const pip=e.target.closest('[data-pip-greet]');if(!pip||!motion())return;const room=formOf(pip)?.querySelector('[data-home-room]'),r=pip.getBoundingClientRect();if(!room||!r.width||!r.height)return;room.style.setProperty('--pip-look-x',Math.round(Math.max(-1,Math.min(1,(e.clientX-r.left-r.width/2)/(r.width/2))))+'px');room.style.setProperty('--pip-look-y',Math.round(Math.max(-1,Math.min(1,(e.clientY-r.top-r.height/2)/(r.height/2))))+'px');},{passive:true});
  return roomLife;
}
