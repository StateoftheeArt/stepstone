import {PIP_PERSONALITIES} from './pip-personalities.js?build=120';
import {playPipAction,stopPipAction,pipView} from './pip-moves.js?build=120';

// Pace, gait and favourite places keep each companion recognisable in the room.
const characters={
 fox:['tiptoe',36,520,['decor','shelf'],'sniffs around'],
 cat:['prowl',30,650,['rug','furniture'],'pads over to'],
 frog:['hop',39,700,['rug','bowl'],'hops over to'],
 axolotl:['waddle',25,800,['bowl','rug'],'paddles over to'],
 owl:['flutter',30,680,['painting','shelf'],'flutters over to'],
 bunny:['hop',44,570,['furniture','decor'],'bounds over to'],
 robot:['march',32,560,['shelf','painting'],'checks'],
 cloud:['float',22,1600,['curtains','painting'],'drifts over to'],
 duck:['waddle',33,610,['bowl','rug'],'waddles over to'],
 penguin:['waddle',28,750,['rug','curtains'],'shuffles over to'],
 turtle:['crawl',19,1150,['rug','furniture'],'takes a careful look at'],
 dragon:['stomp',37,670,['shelf','decor'],'stomps over to'],
 hamster:['scurry',48,360,['decor','furniture'],'scampers over to'],
 raccoon:['tiptoe',34,580,['shelf','decor'],'takes a curious look at'],
 bee:['flutter',42,320,['curtains','decor'],'buzzes over to'],
 octopus:['sway',24,930,['rug','bowl'],'sways over to'],
 dog:['bound',45,460,['furniture','bowl'],'trots over to'],
 badger:['trundle',27,880,['furniture','decor'],'ambles over to'],
 rat:['scurry',43,400,['shelf','decor'],'scurries over to'],
 squirrel:['bound',50,390,['shelf','decor'],'skips over to'],
 bat:['flutter',36,490,['curtains','painting'],'swoops over to'],
 goblin:['jig',34,600,['shelf','furniture'],'tiptoes over to'],
 rock:['roll',16,1400,['rug','decor'],'rocks over to'],
 hedgehog:['shuffle',23,960,['furniture','decor'],'shuffles up to'],
 otter:['sway',31,710,['bowl','rug'],'scoots over to'],
 moth:['flutter',24,790,['curtains','decor'],'floats over to'],
 snail:['glide',13,1800,['rug','decor'],'glides over to'],
 mushroom:['sway',17,1300,['curtains','rug'],'bobs over to']
};
export const PIP_ROOM_PERSONALITIES=Object.fromEntries(Object.entries(characters).map(([id,[gait,speed,beat,favourites,verb]])=>[id,{gait,speed,beat,favourites,verb}]));
const gaits={
 tiptoe:['none','translateY(-1px) rotate(-2deg)','none','translateY(-1px) rotate(2deg)','none'],
 prowl:['none','scale(1.025,.985) rotate(-1deg)','none','scale(.985,1.015) rotate(1deg)','none'],
 hop:['none','scale(1.04,.92)','translateY(-6px)','scale(.98,1.03)','none'],
 waddle:['none','rotate(-4deg) translateY(-1px)','none','rotate(4deg) translateY(-1px)','none'],
 flutter:['none','translateY(-3px) rotate(-2deg)','translateY(-1px)','translateY(-4px) rotate(2deg)','none'],
 march:['none','translateY(-2px) rotate(-2deg)','none','translateY(-2px) rotate(2deg)','none'],
 float:['none','translateY(-3px) rotate(-1deg)','translateY(-5px)','translateY(-2px) rotate(1deg)','none'],
 crawl:['none','scale(1.015,.99)','translateY(-.5px)','scale(.99,1.01)','none'],
 stomp:['none','translateY(-3px) rotate(-2deg)','scale(1.03,.96)','translateY(-3px) rotate(2deg)','none'],
 scurry:['none','translateY(-1.5px) rotate(-2deg)','none','translateY(-1.5px) rotate(2deg)','none'],
 sway:['none','translateY(-1px) rotate(-3deg)','scale(1.015,.985)','translateY(-1px) rotate(3deg)','none'],
 bound:['none','scale(1.03,.94)','translateY(-4px) rotate(-2deg)','translateY(-1px) rotate(2deg)','none'],
 trundle:['none','translateY(-.7px) rotate(-1deg)','none','translateY(-.7px) rotate(1deg)','none'],
 jig:['none','rotate(-3deg) translateY(-2px)','scale(1.02,.98)','rotate(3deg) translateY(-2px)','none'],
 roll:['none','rotate(-6deg) translateY(-.5px)','none','rotate(6deg) translateY(-.5px)','none'],
 shuffle:['none','rotate(-1.5deg) scale(1.01,.99)','none','rotate(1.5deg) scale(.99,1.01)','none'],
 glide:['none','scale(1.015,.99)','none','scale(.99,1.01)','none']
};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,Number.isFinite(n)?n:(a+b)/2));
const draw=random=>clamp(random(),0,.999999);
export function pipGait(species,{duration=3000,scale=1.375,speed}={}){
 const p=PIP_ROOM_PERSONALITIES[species]||PIP_ROOM_PERSONALITIES.fox;
 // Complete whole strides so stopping never drops a raised paw onto the floor.
 const cycles=Math.max(1,Math.round(duration/p.beat)),beat=duration/cycles;
 const stride=clamp((speed??p.speed)*beat/1000/(4*scale),1.3,5),lift=p.gait==='crawl'||p.gait==='sway'?1:2;
 const frames=(xs,ys)=>xs.map((x,i)=>({transform:i===0||i===xs.length-1?'none':`translate(${x.toFixed(2)}px,${ys[i].toFixed(2)}px)`}));
 return {beat,cycles,body:gaits[p.gait].map(transform=>({transform})),
  front:frames([0,-stride/2,-stride,-stride/2,0,stride/2,stride,stride/2,0],[0,0,0,-lift/2,-lift,-lift/2,0,0,0]),
  back:frames([0,stride/2,stride,stride/2,0,-stride/2,-stride,-stride/2,0],[0,-lift,0,0,0,0,0,-lift,0])};
}
export function pipTravelFrames(from,to,duration){
 const ramp=Math.min(.12,180/duration);
 const percent=n=>Number((n*100).toFixed(6))+'%';
 return [[0,0,'cubic-bezier(.42,0,1,1)'],[ramp,ramp/2,'linear'],[1-ramp,1-ramp/2,'cubic-bezier(0,0,.58,1)'],[1,1,'linear']].map(([offset,t,easing])=>({
  offset,easing,left:percent(from.x+(to.x-from.x)*t),bottom:percent(1-from.y-(to.y-from.y)*t)
 }));
}
export function roomFloor({width=500,height=310,petWidth=112,petHeight=125}={}){
 const margin=clamp((petWidth/2+9)/Math.max(1,width),.14,.34);
 return {left:margin,right:Math.min(.84,1-margin),back:Math.min(.87,Math.max(.74,(petHeight+8)/Math.max(1,height))),front:.93};
}
export function roomPoint(point,floor=roomFloor()){
 return {x:clamp(point?.x,floor.left,floor.right),y:clamp(point?.y,floor.back,floor.front)};
}
export function nextRoomActivity({species='fox',items=[],position={x:.5,y:.87},previous='',random=Math.random,floor=roomFloor()}={}){
 const p=PIP_ROOM_PERSONALITIES[species]||PIP_ROOM_PERSONALITIES.fox;
 const choices=items.filter(item=>['rug','furniture','decor','painting','shelf','curtains','bowl'].includes(item.kind)&&item.id!=='none'&&item.key!==previous&&Number.isFinite(item.x)&&Number.isFinite(item.y));
 let item;
 if(choices.length&&draw(random)<.82){
  const weighted=choices.flatMap(value=>Array(p.favourites.includes(value.kind)?3:1).fill(value));
  item=weighted[Math.floor(draw(random)*weighted.length)];
 }
 let point=item?{x:item.x+(['painting','shelf','curtains','rug'].includes(item.kind)?0:item.kind==='bowl'?-.12:position.x<item.x?-.08:.08),y:['painting','shelf','curtains'].includes(item.kind)?floor.back+.025:item.y+.06}:{x:floor.left+draw(random)*(floor.right-floor.left),y:floor.back+draw(random)*(floor.front-floor.back)};
 point=roomPoint(point,floor);
 if(!item&&Math.hypot(point.x-position.x,point.y-position.y)<.08)point=roomPoint({x:position.x>(floor.left+floor.right)/2?floor.left+.025:floor.right-.025,y:point.y},floor);
 return {point,item,gait:p.gait,verb:p.verb};
}

export function createPipRoomLife({root=document,motion=()=>true,fed=()=>false,name=()=> 'Pip',random=Math.random}={}){
 const sessions=new Map();let disposed=false;
 const visible=room=>!disposed&&!root.hidden&&motion()&&room.isConnected===true&&room.getClientRects().length>0&&(!room.closest('dialog')||room.closest('dialog').open);
 function geometry(s){const r=s.room.getBoundingClientRect(),pet=s.stage.getBoundingClientRect();return {width:r.width,height:r.height,petWidth:pet.width,petHeight:pet.height};}
 function position(s){
  const r=s.room.getBoundingClientRect(),style=globalThis.getComputedStyle(s.stage);
  return roomPoint({x:parseFloat(style.left)/r.width,y:1-parseFloat(style.bottom)/r.height},roomFloor(geometry(s)));
 }
 function place(s,point){s.point=roomPoint(point,roomFloor(geometry(s)));s.stage.style.left=s.point.x*100+'%';s.stage.style.bottom=(1-s.point.y)*100+'%';}
 function cancel(s,{freeze=true,faceFront=true}={}){
  clearTimeout(s.timer);s.timer=null;
  if(freeze&&s.moving)place(s,position(s));
  s.animations.forEach(a=>a.cancel());s.animations=[];s.moving=false;
  if(faceFront)delete s.stage.dataset.pipFacing;delete s.room.dataset.pipMoving;
 }
 function stop(s){cancel(s);stopPipAction(s.room);delete s.room.dataset.pipRoomState;delete s.room.dataset.pipRoomTarget;sessions.delete(s.room);}
 function later(s,delay,action=()=>step(s)){clearTimeout(s.timer);s.timer=setTimeout(action,delay);}
 function animate(s,el,frames,options){if(el?.animate)s.animations.push(el.animate(frames,options));}
 function items(s){
  const box=s.room.getBoundingClientRect(),out=[...s.room.querySelectorAll('[data-placed-kind]')].map(el=>{
   const r=el.getBoundingClientRect(),button=el.querySelector('[data-placed-item]');
   return {kind:el.dataset.placedKind,id:el.dataset.placedId,key:el.dataset.placedKind+':'+el.dataset.placedId,label:button?.getAttribute('aria-label')?.split('. Drag')[0].replace(/^Move /,'')||el.dataset.placedId,x:(r.left+r.width/2-box.left)/box.width,y:(r.top+r.height/2-box.top)/box.height,element:button};
  });
  const curtains=s.room.querySelector('.pip-room-curtains');if(curtains&&!out.some(item=>item.kind==='curtains'))out.push({kind:'curtains',id:curtains.dataset.curtainStyle,key:'curtains',label:'curtains',x:.23,y:.4,element:curtains});
  const bowl=s.room.querySelector('.pip-food-bowl');if(bowl){const r=bowl.getBoundingClientRect();out.push({kind:'bowl',id:'bowl',key:'bowl',label:'food bowl',x:(r.left+r.width/2-box.left)/box.width,y:(r.top+r.height/2-box.top)/box.height,element:bowl.querySelector('svg')});}
  return out;
 }
 function inspect(s,item){
  if(!visible(s.room)){stop(s);return;}
  s.room.dataset.pipRoomState=item?'interacting':'idle';
  if(item?.element?.isConnected){
   s.previous=item.key;s.room.dataset.pipRoomTarget=item.key;
   playPipAction(s.room,s.species,{interaction:'inspect',itemKind:item.kind,motion:true,name:name(s.room),announce:false,statusText:name(s.room)+' '+(item.kind==='bowl'&&!fed(s.room)?'sniffs around':(PIP_ROOM_PERSONALITIES[s.species]||PIP_ROOM_PERSONALITIES.fox).verb)+' the '+item.label.toLowerCase()+'.'});
   if(['painting','shelf'].includes(item.kind))animate(s,item.element,[{transform:'none'},{transform:'rotate(-1.5deg)'},{transform:'rotate(1.5deg)'},{transform:'none'}],{duration:2100,easing:'ease-in-out'});
   else if(item.kind==='curtains')animate(s,item.element,[{transform:'none'},{transform:'translateX(1.5px) skewX(1deg)'},{transform:'translateX(-1px) skewX(-.7deg)'},{transform:'none'}],{duration:2100,easing:'ease-in-out'});
   else animate(s,item.element,[{transform:'none'},{transform:item.kind==='rug'||item.kind==='furniture'?'scale(1.035,.96)':'rotate(-4deg)'},{transform:item.kind==='rug'||item.kind==='furniture'?'scale(.99,1.01)':'rotate(3deg)'},{transform:'none'}],{duration:2100,easing:'ease-in-out'});
  }
  later(s,(item?2400:900)+(fed(s.room)?1100:2200)+draw(random)*1800);
 }
 function step(s){
  if(sessions.get(s.room)!==s)return;
  if(!visible(s.room)){stop(s);return;}
  if(s.held||s.room.classList.contains('pip-room-dragging')||s.room.dataset.pipInteracting){later(s,650);return;}
  cancel(s);const p=PIP_ROOM_PERSONALITIES[s.species]||PIP_ROOM_PERSONALITIES.fox,g=geometry(s),floor=roomFloor(g);
  const plan=nextRoomActivity({species:s.species,items:items(s),position:s.point,previous:s.previous,random,floor});
  const distance=Math.hypot((plan.point.x-s.point.x)*g.width,(plan.point.y-s.point.y)*g.height);
  if(distance<3){inspect(s,plan.item);return;}
  const duration=clamp(distance/(p.speed*(fed(s.room)?1:.8))*1000,1300,['snail','rock','mushroom','turtle'].includes(s.species)?14000:7500);
  s.room.dataset.pipRoomState='walking';s.room.dataset.pipMoving='true';s.moving=true;s.stage.dataset.pipFacing=plan.point.x<s.point.x?'left':'right';
  animate(s,s.stage,pipTravelFrames(s.point,plan.point,duration),{duration,easing:'linear',fill:'forwards'});
  const view=pipView(s.room),body=view.querySelector('.sprite-body');
  if(body?.style){body.style.transformBox='view-box';body.style.transformOrigin='32px 60px';}
  const gait=pipGait(s.species,{duration,scale:g.petWidth/64,speed:distance/duration*1000}),timing={duration:gait.beat,iterations:gait.cycles,easing:'ease-in-out'};
  animate(s,body,gait.body,timing);
  if(!['hop','bound','flutter','float','glide','roll'].includes(plan.gait)){
   for(const [selector,frames] of [['.sprite-foot-front',gait.front],['.sprite-foot-back',gait.back]]){
    const foot=view.querySelector(selector);
    if(foot?.style){foot.style.transformBox='view-box';foot.style.transformOrigin=foot.dataset.pipOrigin||'32px 54px';}
    animate(s,foot,frames,timing);
   }
  }
  const signature=PIP_PERSONALITIES[s.species]||PIP_PERSONALITIES.fox,part=view.querySelector(signature.part);
  if(part?.style){part.style.transformBox='view-box';part.style.transformOrigin=part.dataset?.pipOrigin||signature.origin;}
  if(signature.part!=='.sprite-feet')animate(s,part,signature.greetFrames.map(transform=>({transform})),{duration:duration/Math.max(1,Math.round(gait.cycles/2)),iterations:Math.max(1,Math.round(gait.cycles/2)),easing:'ease-in-out'});
  later(s,duration,()=>{
   if(sessions.get(s.room)!==s)return;
   place(s,plan.point);cancel(s,{freeze:false,faceFront:false});
   if(!visible(s.room)){stop(s);return;}
   s.room.dataset.pipRoomState='settling';
   animate(s,body,[{transform:'none'},{transform:'translateY(.6px) scale(1.008,.99)'},{transform:'none'}],{duration:220,easing:'ease-out'});
   later(s,220,()=>{if(sessions.get(s.room)!==s)return;cancel(s,{freeze:false,faceFront:false});inspect(s,plan.item);});
  });
 }
 function sync(){
  for(const s of [...sessions.values()])if(!visible(s.room))stop(s);
  if(disposed||root.hidden||!motion())return;
  for(const room of root.querySelectorAll('form[data-form="profile"] [data-home-room]')){
   if(sessions.has(room)||!visible(room))continue;
   const stage=room.querySelector('.pip-home-stage');if(!stage?.animate)continue;
   const s={room,stage,species:room.dataset.species,point:null,timer:null,moving:false,held:false,animations:[],previous:''};
   sessions.set(room,s);place(s,position(s));room.dataset.pipRoomState='idle';later(s,900+draw(random)*800);
  }
 }
 function pause(room,delay){const s=sessions.get(room);if(!s)return;cancel(s);stopPipAction(room);room.dataset.pipRoomState='paused';s.held=delay===undefined;if(!s.held)later(s,delay);}
 function resume(room,delay=700){const s=sessions.get(room);if(s){s.held=false;later(s,delay);}else sync();}
 const observe=typeof MutationObserver==='function'?new MutationObserver(sync):null;
 if(observe&&root.documentElement)observe.observe(root.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['open','data-panel','class']});
 root.addEventListener('visibilitychange',sync);root.addEventListener('close',sync,true);
 const resize=()=>{for(const s of sessions.values()){pause(s.room,900);place(s,s.point);}sync();};
 const pagehide=()=>{for(const s of [...sessions.values()])stop(s);};
 globalThis.addEventListener?.('resize',resize);globalThis.addEventListener?.('pagehide',pagehide);globalThis.addEventListener?.('pageshow',sync);
 sync();
 return {sync,pause,resume,dispose(){disposed=true;pagehide();observe?.disconnect();root.removeEventListener('visibilitychange',sync);root.removeEventListener('close',sync,true);globalThis.removeEventListener?.('resize',resize);globalThis.removeEventListener?.('pagehide',pagehide);globalThis.removeEventListener?.('pageshow',sync);}};
}
