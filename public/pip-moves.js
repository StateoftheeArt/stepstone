import {PIP_PERSONALITIES} from './pip-personalities.js?build=119';
export const PIP_ACTIONS=Object.fromEntries(Object.entries(PIP_PERSONALITIES).map(([id,p])=>[id,{label:p.response,frames:p.bodyFrames,part:p.part}]));
export const pipPlayLabel=id=>(PIP_PERSONALITIES[id]||PIP_PERSONALITIES.fox).playLabel;
export function pipDance(species,dance=1){
 const id=species in PIP_PERSONALITIES?species:'fox',p=PIP_PERSONALITIES[id],index=Object.keys(PIP_PERSONALITIES).indexOf(id);
 const gentle=['snail','rock','mushroom','turtle'].includes(id),step=gentle?1.2:2+(index%3)*.5,lift=gentle?1.5:3+(index%3)*.5,turn=gentle?3:4+(index%3);
 const names={snail:['Shell sway','Dewdrop bounce','Antenna twist'],dog:['Tail-wag shuffle','Paw bounce','Happy twist'],rock:['Pebble sway','Rock bob','Boulder shimmy'],goblin:['Pocket shuffle','Goblin bounce','Little jig']};
 const label=(names[id]||['shuffle','bounce','twist'].map(word=>p.toy.charAt(0).toUpperCase()+p.toy.slice(1)+' '+word))[dance-1]||'Little shuffle';
 const body=[
  ['none',`translate(${-step}px,-1px) rotate(${-turn/2}deg)`,`translateY(-${lift/2}px)`,`translate(${step}px,-1px) rotate(${turn/2}deg)`,'none'],
  ['none','scale(1.06,.93)',`translateY(-${lift}px) rotate(2deg)`,'scale(.98,1.02)',`translateY(-${lift*.75}px) rotate(-2deg)`,'none'],
  ['none',`translateX(-2px) rotate(-${turn}deg)`,`translateX(2px) rotate(${turn}deg)`,'scale(1.03,.97)',`rotate(-${turn*.8}deg)`,`rotate(${turn*.8}deg)`,'none']
 ][dance-1]||p.bodyFrames;
 const part=dance===2?['none',p.greetFrames[1]||'none','none',p.playFrames[1]||'none','none']:dance===3?[...p.playFrames].reverse():p.playFrames;
 return {label,body,part};
}
const running=new WeakMap();
const toys={
 firefly:'<ellipse cx="14" cy="15" rx="4" ry="6"/><path d="M10 13Q2 5 7 4L14 10Q22 3 24 7L18 14" fill="#a9d9c9"/><circle cx="14" cy="19" r="3" fill="#ffe7a3"/>',
 yarn:'<circle cx="14" cy="14" r="9"/><path d="M7 10q10 2 13 9M8 19q5-10 12-9M14 23q6 1 10-3" fill="none"/>',
 ripple:'<ellipse cx="14" cy="17" rx="11" ry="5" fill="none"/><ellipse cx="14" cy="17" rx="6" ry="2" fill="none"/>',
 bubble:'<circle cx="14" cy="14" r="9" fill="#9ccfcf55"/><path d="M9 10q2-3 5-3" fill="none"/>',
 feather:'<path d="M7 23Q1 9 14 4Q28 9 18 16L7 23Z"/><path d="M7 23 18 7M10 16l8-1M12 12l5 0" fill="none"/>',
 clover:'<path d="M14 16q-13-1-9-9 7-5 9 5 3-10 10-5 4 8-10 9Z" fill="#a9d4a4"/><path d="M14 15v10" fill="none"/>',
 signal:'<path d="M4 19h4v-8h4v12h4V5h4v14h4" fill="none"/>',
 rainbow:'<path d="M3 23a11 11 0 0 1 22 0" stroke="#efb6b1" fill="none" stroke-width="4"/><path d="M7 23a7 7 0 0 1 14 0" fill="none" stroke="#e4cd8f" stroke-width="3"/>',
 pond:'<ellipse cx="14" cy="20" rx="11" ry="4" fill="#93cacc"/><path d="M8 19q7-5 13 0" fill="none"/>',
 snowflake:'<path d="M14 3v22M4 8l20 12M4 20 24 8M10 6l4 4 4-4M10 22l4-4 4 4" fill="none"/>',
 leaf:'<path d="M5 23Q0 5 24 4Q25 24 5 23Z" fill="#aed1a3"/><path d="M5 23 20 8" fill="none"/>',
 spark:'<path d="m14 2 3 9 9 3-9 3-3 9-3-9-9-3 9-3Z"/>',
 seed:'<ellipse cx="14" cy="14" rx="7" ry="10" transform="rotate(-25 14 14)"/><path d="M11 6q7 8 5 16" fill="none"/>',
 puzzle:'<path d="M4 6h7q-3-6 3-5 5 0 2 5h8v8q-6-3-6 3 0 5 6 2v7H4v-8q6 3 6-2 0-6-6-3Z" fill="#bbafd2"/>',
 flower:'<path d="M14 15v11M14 21l7-4" fill="none"/><circle cx="14" cy="10" r="7" fill="#e8b7bd"/><circle cx="14" cy="10" r="3"/>',
 shell:'<path d="M4 22Q-1 1 14 4Q29 1 24 22Z"/><path d="m14 7 0 15M8 8l6 14M20 8l-6 14" fill="none"/>',
 ball:'<circle cx="14" cy="14" r="10" fill="#9ecac2"/><path d="M5 8q9 6 5 15M22 6q-9 7-1 15" fill="none"/>',
 earth:'<path d="M2 22q12-15 24 0Z" fill="#b3a08b"/><path d="M7 22v-2m7 2v-4m7 4v-2" fill="none"/>',
 ribbon:'<path d="M3 6q24 3 13 12Q7 26 25 22" fill="none" stroke="#ceb5db" stroke-width="5"/>',
 acorn:'<path d="M7 13q0 14 7 13 7 1 7-13Z" fill="#c5a073"/><path d="M5 13q0-11 18 0Z" fill="#b1c29b"/><path d="M14 6V2" fill="none"/>',
 moonbeam:'<path d="M19 3Q3 10 19 25Q-3 23 5 8Q9 2 19 3Z" fill="#ded6b6"/>',
 coin:'<circle cx="14" cy="14" r="10"/><circle cx="14" cy="14" r="6" fill="none"/><path d="m11 17 6-6" fill="none"/>',
 glint:'<path d="m14 1 2 10 10 3-10 2-2 11-3-11-10-2 10-3Z" fill="#c6e6e6"/>',
 autumnleaf:'<path d="m14 2 3 6 6-2-2 7 5 3-10 7h-4L2 16l6-3-3-7 6 2Z" fill="#d6b47e"/><path d="M14 10v17" fill="none"/>',
 pebble:'<path d="M5 21Q-3 7 10 5Q24 2 26 17Q25 26 5 21Z" fill="#b5c5ca"/><path d="M9 10q5-3 10 0" fill="none"/>',
 lantern:'<path d="M9 5h10v4h4v16H5V9h4Z" fill="#b3c6c5"/><path d="M9 13h10v8H9Z" fill="#ffe0a1"/><path d="M11 5V2h6v3" fill="none"/>',
 dewdrop:'<path d="M14 3Q-3 20 14 25Q30 20 14 3Z" fill="#a3d8ce"/><path d="M9 18q-1 3 3 3" fill="none"/>',
 spore:'<circle cx="14" cy="10" r="5" fill="#e0cab9"/><path d="M14 15q-4 3 0 6" fill="none"/>'
};
export const pipToyMarkup=kind=>`<svg class="pip-toy" viewBox="0 0 28 28" fill="#edd59f" stroke="#739798" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${toys[kind]||toys.spark}</svg>`;
export function pipView(room){
 const facing=room.querySelector('.pip-home-stage')?.dataset?.pipFacing||'front';
 return room.querySelector('[data-pip-view="'+facing+'"]')||room;
}
export function stopPipAction(room,{restore=true}={}){
 if(!room)return;const s=running.get(room);if(!s)return;
 clearTimeout(s.timer);s.animations.forEach(a=>a.cancel());s.effect?.remove();running.delete(room);delete room.dataset.pipInteracting;
 if(restore)room.dataset.pose=(room.dataset.pipResting==='true'||room.dataset.pipResting===undefined&&s.resting)?'resting':'idle';
}
export function stopAllPipActions(root=document){root.querySelectorAll?.('.companion-dock,[data-home-room]').forEach(room=>stopPipAction(room));}
export function playPipAction(room,species,{dance=0,snack=false,interaction=snack?'snack':'play',motion=true,name='Pip',duration:fixedDuration,statusText,itemKind,announce=true}={}){
 if(!room)return;const resting=room.dataset.pipResting==='true'||room.dataset.pose==='resting';stopPipAction(room,{restore:false});
 const p=PIP_PERSONALITIES[species]||PIP_PERSONALITIES.fox,duration=fixedDuration||(interaction==='greet'?1350:interaction==='snack'?1500:interaction==='inspect'?2100:p.duration),steps=dance?pipDance(species,dance):null;
 const s={resting,animations:[],timer:null,effect:null};running.set(room,s);
 room.dataset.species=species in PIP_PERSONALITIES?species:'fox';room.dataset.pipInteracting='true';room.dataset.pose=motion?(dance&&interaction==='play'?'dance':'action'):'happy';if(dance)room.dataset.dance=String(dance);
 const note=room.closest?.('.pip-studio')?.querySelector('[data-pip-status]')||room.querySelector('[data-pip-status]')||room.querySelector('[data-pip-note]');if(note){note.setAttribute('aria-live',announce?'polite':'off');note.textContent=statusText||(steps?name+' tries the '+steps.label.toLowerCase()+'.':name+' '+(interaction==='greet'?p.hello:interaction==='snack'?p.snack:p.response));}
 function animate(selector,frames,origin='32px 44px',options={}){
  const part=pipView(room).querySelector(selector);if(!motion||!part?.animate)return;if(part.style){part.style.transformBox='view-box';part.style.transformOrigin=part.dataset?.pipOrigin||origin;}
  s.animations.push(part.animate(frames.map(transform=>({transform})),{duration,easing:species==='robot'?'steps(3,end)':'ease-in-out',...options}));
 }
 if(interaction==='greet'){animate('.sprite-body',species==='rock'?['none','rotate(-3deg)','rotate(3deg)','none']:['none','translateY(1px) scaleY(.99)','none']);animate(p.part,p.greetFrames,p.origin);}
 else if(interaction==='snack'){animate('.sprite-body',['none','translateY(1px) scaleY(.98)','none','translateY(.5px)','none']);animate(p.part,['none',p.greetFrames[1],'none'],p.origin);}
 else if(interaction==='inspect'){
  animate('.sprite-body',['rug','furniture'].includes(itemKind)?['none','translateY(1px) scale(1.025,.97)','translateY(.5px) scale(.99,1.01)','none']:['none','rotate(-2deg)','rotate(2deg)','none']);
  animate(p.part,p.greetFrames,p.origin);
  if(!['rug','furniture'].includes(itemKind)&&p.part!=='.sprite-head')animate('.sprite-head',['none','rotate(-4deg)','rotate(3deg)','none'],'32px 33px');
 }
 else{
  animate('.sprite-body',steps?.body||p.bodyFrames,'32px 60px');animate(p.part,steps?.part||p.playFrames,p.origin);
  if(steps){
   const foot=dance===2?['none','rotate(-4deg)','none','rotate(3deg)','none']:['none','translate(-1px,-1px)','none','translate(1px,0)','none'];
   animate('.sprite-foot-front',foot,'40px 54px');
   animate('.sprite-foot-back',dance===2?foot:foot.map(t=>t.replace('-1px','1px').replace('translate(1px,0)','translate(-1px,0)')),'24px 54px');
  }
  const anchor=room.querySelector('.pip-home-stage')||room.querySelector('.companion-pet');
  if(anchor?.append){const effect=document.createElement('span');effect.className='pip-interaction-toy';effect.setAttribute('aria-hidden','true');effect.innerHTML=pipToyMarkup(p.toy);anchor.append(effect);s.effect=effect;
   if(motion&&effect.animate){const floats=['firefly','bubble','feather','rainbow','signal','snowflake','spark','moonbeam','glint','lantern','spore'].includes(p.toy);s.animations.push(effect.animate(floats?[{transform:'translate(-5px,8px)',opacity:.4},{transform:'translate(5px,-15px)',opacity:1},{transform:'translate(-2px,-22px)',opacity:0}]:[{transform:'translate(-8px,0) rotate(-8deg)',opacity:.5},{transform:'translate(12px,4px) rotate(18deg)',opacity:1},{transform:'translate(-8px,0) rotate(-8deg)',opacity:0}],{duration,easing:'ease-in-out'}));}
  }
 }
 s.timer=setTimeout(()=>{if(running.get(room)===s)stopPipAction(room);},duration+80);return p;
}
