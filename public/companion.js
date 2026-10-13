import {playPipAction,stopPipAction} from './pip-moves.js?build=120';
import {escapeHTML as esc} from './engine.js?build=120';
import {pipArtwork} from './pip-art.js?build=120';
import {pipProfileArtwork,PIP_PROFILE_ANCHORS} from './pip-profile-art.js?build=120';
import {accessoryArtwork} from './pip-items.js?build=120';

export const COMPANIONS=[
  {id:'fox',label:'Fox',colour:'#ce945f',light:'#e8b782'},
  {id:'cat',label:'Cat',colour:'#a4b8c5',light:'#d6dfe0'},
  {id:'frog',label:'Frog',colour:'#88b48c',light:'#c0ddb4'},
  {id:'axolotl',label:'Axolotl',colour:'#e3b7c6',light:'#f3d5de'},
  {id:'owl',label:'Owl',colour:'#b29773',light:'#d9bd92'},
  {id:'bunny',label:'Bunny',colour:'#d0c2aa',light:'#f0e2ca'},
  {id:'robot',label:'Robot',colour:'#9abcc9',light:'#d9e8e9'},
  {id:'cloud',label:'Cloud',colour:'#c2dbe4',light:'#eef4f1'},
  {id:'duck',label:'Duck',colour:'#4f967a',light:'#9bceb0'},
  {id:'penguin',label:'Penguin',colour:'#506c86',light:'#93afc3'},
  {id:'turtle',label:'Turtle',colour:'#afca92',light:'#e0e8bb'},
  {id:'dragon',label:'Dragon',colour:'#8ab8ae',light:'#c1dfcb'},
  {id:'hamster',label:'Hamster',colour:'#d7b181',light:'#efd1a6'},
  {id:'raccoon',label:'Raccoon',colour:'#b1c1cb',light:'#e0e8e8'},
  {id:'bee',label:'Bee',colour:'#dfc27e',light:'#f5dfaa'},
  {id:'octopus',label:'Octopus',colour:'#d6a4af',light:'#efcbd1'},
  {id:'dog',label:'Dog',colour:'#d0ab7d',light:'#edcfaa'},
  {id:'badger',label:'Badger',colour:'#74828b',light:'#a6b2b8'},
  {id:'rat',label:'Rat',colour:'#acb5be',light:'#d6dadb'},
  {id:'squirrel',label:'Squirrel',colour:'#c79b70',light:'#eaca9c'},
  {id:'bat',label:'Bat',colour:'#a29bb6',light:'#cec6d7'},
  {id:'goblin',label:'Goblin',colour:'#a3c197',light:'#d3deb5'},
  {id:'rock',label:'A rock',colour:'#91a4b0',light:'#c3d1d5'},
  {id:'hedgehog',label:'Hedgehog',colour:'#cfb797',light:'#ecd9b7'},
  {id:'otter',label:'Otter',colour:'#b69a79',light:'#dac4a2'},
  {id:'moth',label:'Moth',colour:'#d0c2a9',light:'#f0e4cd'},
  {id:'snail',label:'Snail',colour:'#b0c6aa',light:'#dce3c0'},
  {id:'mushroom',label:'Mushroom',colour:'#b78278',light:'#d9ada0'}
];

export function companionSprite(id='fox',size=64,accessory='none',{walkingViews=false}={}){
  const c=COMPANIONS.find(c=>c.id===id)||COMPANIONS[0],pixels=Number.isFinite(Number(size))?Math.max(16,Math.min(256,Number(size))):64;
  const extra=accessoryArtwork(accessory,c.id);
  const front=pipArtwork(c.id)+extra,side=walkingViews?pipProfileArtwork(c.id)+accessoryArtwork(accessory,c.id,PIP_PROFILE_ANCHORS[c.id]):'';
  const body=art=>`<g class="sprite-body" data-pip-origin="32px 60px">${art}</g>`;
  const drawing=walkingViews?`<g data-pip-view="front">${body(front)}</g><g data-pip-view="right">${body(side)}</g><g data-pip-view="left" transform="translate(64 0) scale(-1 1)">${body(side)}</g>`:body(front);
  return `<svg class="companion-sprite" data-species="${c.id}" width="${pixels}" height="${pixels}" viewBox="0 0 64 64" shape-rendering="crispEdges" aria-hidden="true"><ellipse class="sprite-shadow" cx="32" cy="61" rx="20" ry="2" fill="#061c32" opacity=".3"/>${drawing}<g class="sprite-pop" fill="#f4d595"><path d="M28 0h8v8h-8ZM28 56h8v8h-8ZM0 28h8v8H0ZM56 28h8v8h-8ZM8 8h6v6H8ZM50 8h6v6h-6ZM8 50h6v6H8ZM50 50h6v6h-6Z"/></g></svg>`;
}

export function safePetPosition(point,{width,height,size=64,gap=8},obstacles=[]){
  if(![point?.x,point?.y,width,height,size,gap].every(Number.isFinite))return null;
  const maxX=width-size-gap,maxY=height-size-gap;if(maxX<gap||maxY<gap)return null;
  const clamp=p=>({x:Math.max(gap,Math.min(maxX,p.x)),y:Math.max(gap,Math.min(maxY,p.y))});
  const clear=p=>obstacles.every(r=>p.x+size+gap<=r.left||p.x>=r.right+gap||p.y+size+gap<=r.top||p.y>=r.bottom+gap);
  const desired=clamp(point);if(clear(desired))return desired;
  const candidates=[{x:gap,y:gap},{x:maxX,y:gap},{x:gap,y:maxY},{x:maxX,y:maxY}];
  for(const r of obstacles)for(const x of [r.left-size-gap,r.right+gap])for(const y of [desired.y,r.top-size-gap,r.bottom+gap])candidates.push(clamp({x,y}));
  for(let y=gap;y<=maxY;y+=size/2)for(let x=gap;x<=maxX;x+=size/2)candidates.push({x,y});
  return candidates.filter(clear).sort((a,b)=>(a.x-desired.x)**2+(a.y-desired.y)**2-((b.x-desired.x)**2+(b.y-desired.y)**2))[0]||null;
}

export function createCompanion({profile,ready,motion,canPlay=()=>true,onPlay=()=>{},edit,owner=()=> 'guest',storage=()=>localStorage}){
  const host=document.createElement('aside');host.className='companion-dock';host.hidden=true;host.setAttribute('aria-label','Your profile and pet');document.querySelector('#profile-slot').append(host);
  let look='',timer,burst=false,taps=0,danceIndex=0,gesture=null,suppressClick=false,position=null,currentOwner='',inDialog=false,frame=0,guideAnchor=null,guideKey,parkedGuide;
  const positionKey=id=>'stepstone-pip-position-v1-'+id;
  const pet=()=>host.querySelector('.companion-pet');
  const magnet=()=>host.querySelector('.companion-magnet');
  function syncMagnet(){const m=magnet();if(m)m.hidden=inDialog||!pet()?.classList.contains('is-floating')&&!pet()?.classList.contains('is-guiding');}
  function petLabel(){const p=profile(),name=p.alias||p.companionName||'Pip';pet()?.setAttribute('aria-label',(canPlay()?'Say hi to '+name+'. Tap to dance; tap 13 times for a surprise.':name+' is resting. Tap for a gentle hello; feed for active play.')+(guideAnchor?' I am guiding this step.':' Drag to move; Home returns to profile.'));}
  function setPose(pose,text){host.dataset.pose=pose;const note=host.querySelector('[data-pip-note]');if(note)note.textContent=text;}
  function reset(){stopPipAction(host);clearTimeout(timer);burst=false;taps=0;setPose(canPlay()?'idle':'resting',canPlay()?'Tap to dance.':'Pip is resting. Feed Pip to play.');}
  function pop(){
    stopPipAction(host);
    if(!canPlay()){reset();return;}if(burst)return;
    clearTimeout(timer);burst=true;taps=0;setPose(motion()?'inflate':'still','Getting a little carried away…');
    timer=setTimeout(()=>{setPose(motion()?'pop':'still','Puff!');timer=setTimeout(()=>{setPose('annoyed','Okay, okay. I’m back.');timer=setTimeout(reset,2200);},420);},motion()?1200:700);
  }
  function dance(){
    if(!canPlay()){clearTimeout(timer);const p=profile();host.dataset.pipResting='true';playPipAction(host,p.avatar,{interaction:'greet',name:p.alias||p.companionName||'Pip',motion:motion()});return;}if(burst)return;
    onPlay();
    if(++taps===13){pop();return;}
    clearTimeout(timer);host.dataset.pose='idle';host.dataset.dance=String(danceIndex++%3+1);void host.offsetWidth;
    setPose(motion()?'dance':'happy','Dancing.');const p=profile();host.dataset.pipResting='false';playPipAction(host,p.avatar,{dance:Number(host.dataset.dance),name:p.alias||p.companionName||'Pip',motion:motion(),duration:1520});timer=setTimeout(()=>setPose('idle','Tap to dance. Tap 13 times for a surprise.'),1600);
  }
  function celebrate(){
    if(host.hidden)return;if(!canPlay()){reset();return;}
    stopPipAction(host);clearTimeout(timer);burst=false;
    host.dataset.pose='idle';host.dataset.dance=String(danceIndex++%3+1);void host.offsetWidth;
    const p=profile();host.dataset.pipResting='false';playPipAction(host,p.avatar,{dance:Number(host.dataset.dance),name:p.alias||p.companionName||'Pip',motion:motion(),duration:1520});
    setPose(motion()?'dance':'happy','Checkpoint passed. Pip is cheering you on.');
    timer=setTimeout(()=>setPose('idle','Tap to dance. Tap 13 times for a surprise.'),1600);
  }
  function readPosition(id){try{const p=JSON.parse(storage().getItem(positionKey(id))||'null');if(p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&p.x>=0&&p.x<=1&&p.y>=0&&p.y<=1)return p;}catch{}return null;}
  function savePosition(){try{if(position)storage().setItem(positionKey(currentOwner),JSON.stringify(position));else storage().removeItem(positionKey(currentOwner));}catch{}}
  function clearPlacement(){const p=pet();p?.classList.remove('is-floating','is-guiding','is-dragging');if(p){p.style.removeProperty('left');p.style.removeProperty('top');}syncMagnet();petLabel();}
  function returnHome(){reset();if(guideAnchor)parkedGuide=guideKey;guideAnchor=null;position=null;savePosition();clearPlacement();setPose(canPlay()?'idle':'resting','Your companion is back in your profile.');}
  function obstacles(){return [...document.querySelectorAll('button,a,input,textarea,select,summary,[role="button"],.question-focus,.scenario-prompt,.tour-callout')].filter(e=>e!==pet()&&e.getClientRects().length&&!e.closest('dialog:not([open])')).map(e=>e.getBoundingClientRect());}
  function place(point,avoid=true){
    const p=pet();if(!p||inDialog||guideAnchor)return;
    const size=p.getBoundingClientRect().width,bounds={width:innerWidth,height:innerHeight,size};
    const spot=safePetPosition(point,bounds,avoid?obstacles():[]);if(!spot){clearPlacement();return;}
    p.classList.remove('is-guiding');p.classList.add('is-floating');p.style.left=spot.x+'px';p.style.top=spot.y+'px';position={x:spot.x/Math.max(1,innerWidth-size),y:spot.y/Math.max(1,innerHeight-size)};syncMagnet();
  }
  function placeGuide(){
    const p=pet();if(!p||!guideAnchor?.isConnected||host.hidden)return;
    const r=guideAnchor.getBoundingClientRect();if(!guideAnchor.getClientRects().length||r.bottom<0||r.top>innerHeight){clearPlacement();return;}
    p.classList.remove('is-floating','is-dragging');p.classList.add('is-guiding');p.style.left=(r.left+(r.width-64)/2)+'px';p.style.top=(r.top+(r.height-64)/2)+'px';syncMagnet();petLabel();
  }
  function restorePosition(){if(guideAnchor){placeGuide();return;}if(!position||inDialog||host.hidden||gesture)return;const size=pet()?.getBoundingClientRect().width||64;place({x:position.x*(innerWidth-size),y:position.y*(innerHeight-size)});}
  function schedulePosition(){if(frame||!position&&!guideAnchor)return;frame=requestAnimationFrame(()=>{frame=0;restorePosition();});}
  function followGuide(anchor,key){
    if(anchor&&key!==guideKey){guideKey=key;parkedGuide=undefined;}
    if(anchor&&parkedGuide===key)return;
    guideAnchor=anchor;
    if(anchor)placeGuide();else{clearPlacement();restorePosition();}
  }
  function update(){
    host.hidden=!ready();document.documentElement.classList.toggle('has-companion',!host.hidden);if(host.hidden){reset();return;}
    const nextOwner=owner();if(nextOwner!==currentOwner){currentOwner=nextOwner;position=readPosition(currentOwner);look='';guideAnchor=null;parkedGuide=undefined;danceIndex=0;}
    const p=profile(),id=COMPANIONS.some(c=>c.id===p.avatar)?p.avatar:'fox',name=p.alias||p.companionName||'Pip';
    const key=[id,name,p.alias||'',p.accessory||'none',p.badge||'plain'].join('|');host.dataset.pipResting=String(!canPlay());if(key===look){if(!canPlay()&&!host.dataset.pipInteracting&&host.dataset.pose!=='resting')reset();else if(canPlay()&&host.dataset.pose==='resting')reset();petLabel();pet()?.setAttribute('aria-disabled','false');schedulePosition();return;}
    look=key;reset();host.dataset.badge=p.badge||'plain';host.dataset.species=id;
    host.innerHTML=`<button class="companion-magnet" type="button" aria-label="Bring ${esc(name)} back to my profile" title="Drop your companion here or tap to put them away" hidden><svg viewBox="0 0 32 32" width="30" height="30" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" aria-hidden="true"><path d="M6 5h7v12a3 3 0 0 0 6 0V5h7v12a10 10 0 0 1-20 0Z"/><path d="M6 11h7m6 0h7"/></svg></button><button class="companion-pet" type="button" title="Tap to greet your Pip · feed for active play · drag to move">${companionSprite(id,64,p.accessory)}</button><button class="companion-profile" type="button" aria-label="Edit my profile" title="${esc(name)}"><strong>My profile</strong><span>${esc(name)}</span><span class="companion-edit-label">Edit profile ↗</span></button><span class="sr-only" data-pip-note>Tap to dance. Tap 13 times for a surprise.</span>`;
    const button=pet();petLabel();button.setAttribute('aria-disabled','false');
    button.addEventListener('pointerdown',e=>{if(e.button!==0||!canPlay())return;button.classList.add('pointer-interaction');suppressClick=false;const r=button.getBoundingClientRect();gesture={id:e.pointerId,x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,left:r.left,top:r.top,moved:false,previous:position&&{...position},previousGuide:guideAnchor,previousParked:parkedGuide};button.setPointerCapture(e.pointerId);});
    button.addEventListener('pointermove',e=>{if(!gesture||gesture.id!==e.pointerId)return;const dx=e.clientX-gesture.x,dy=e.clientY-gesture.y;gesture.lastX=e.clientX;gesture.lastY=e.clientY;if(!gesture.moved&&Math.hypot(dx,dy)<8)return;if(!gesture.moved){gesture.moved=true;reset();if(guideAnchor){parkedGuide=guideKey;guideAnchor=null;}button.classList.add('is-dragging');}place({x:gesture.left+dx,y:gesture.top+dy},false);});
    button.addEventListener('pointerup',()=>{if(gesture?.moved){suppressClick=true;const m=magnet()?.getBoundingClientRect(),drop=m&&gesture.lastX>=m.left-8&&gesture.lastX<=m.right+8&&gesture.lastY>=m.top-8&&gesture.lastY<=m.bottom+8;button.classList.remove('is-dragging');gesture=null;if(drop)returnHome();else{restorePosition();savePosition();setPose('idle','Your companion moved clear of the controls.');}}else gesture=null;});
    function cancel(){if(gesture?.moved){position=gesture.previous;guideAnchor=gesture.previousGuide;parkedGuide=gesture.previousParked;button.classList.remove('is-dragging');gesture=null;if(position||guideAnchor)restorePosition();else clearPlacement();suppressClick=true;}gesture=null;}
    button.addEventListener('pointercancel',cancel);button.addEventListener('lostpointercapture',cancel);
    button.addEventListener('contextmenu',e=>e.preventDefault());
    button.addEventListener('click',()=>{if(suppressClick){suppressClick=false;return;}dance();});
    button.addEventListener('keydown',e=>{button.classList.remove('pointer-interaction');if(e.key==='Home'){e.preventDefault();returnHome();return;}const delta={ArrowLeft:[-24,0],ArrowRight:[24,0],ArrowUp:[0,-24],ArrowDown:[0,24]}[e.key];if(delta){e.preventDefault();if(!canPlay()||guideAnchor)return;const r=button.getBoundingClientRect();place({x:r.left+delta[0],y:r.top+delta[1]});savePosition();}});
    button.addEventListener('blur',()=>button.classList.remove('pointer-interaction'));
    magnet().addEventListener('click',returnHome);host.querySelector('.companion-profile').addEventListener('click',edit);schedulePosition();
  }
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&look){gesture=null;reset();pet()?.classList.remove('is-dragging');}});
  globalThis.window?.addEventListener('resize',schedulePosition);globalThis.window?.addEventListener('scroll',schedulePosition,{passive:true});
  return {
    update,returnHome,followGuide,celebrate,
    adoptPosition(oldOwner,newOwner){const p=readPosition(oldOwner);if(p&&!readPosition(newOwner))try{storage().setItem(positionKey(newOwner),JSON.stringify(p));storage().removeItem(positionKey(oldOwner));}catch{}},
    dockIn(dialog){inDialog=!!dialog?.open;guideAnchor=null;host.querySelector('.companion-profile')?.toggleAttribute('hidden',inDialog);clearPlacement();(inDialog?dialog:document.querySelector('#profile-slot')).append(host);if(!inDialog)schedulePosition();},
    quiet(){if(look&&!motion())reset();}
  };
}
