import {escapeHTML as esc} from './engine.js?build=119';
import {companionSprite} from './companion.js?build=119';
import {canPipPlay} from './pip-food.js?build=119';
import {firstPasses,previewCompletions,itemIcon} from './wins.js?build=119';

export function checkpointCompletion({unit,local,me,unlocks}){
  const completions=me?(me.moduleWins||firstPasses(me.attempts||[],unlocks)):previewCompletions(local,unlocks);
  return completions.find(item=>item.unit===unit)||null;
}

export function createCheckpointQueue(){
  const seen=new Set(),waiting=new Map();
  const key=(owner,unit)=>JSON.stringify([owner,unit]);
  return {add(owner,unit,receipt,passed,alreadyPassed=false){if(!passed||!receipt)return false;const token=JSON.stringify([owner,unit,receipt]);if(seen.has(token))return false;seen.add(token);waiting.set(key(owner,unit),{newCompletion:!alreadyPassed});return true;},peek(owner,unit){return waiting.get(key(owner,unit));},take(owner,unit){const k=key(owner,unit),item=waiting.get(k);waiting.delete(k);return item;}};
}

export function checkpointMarkup({completion,profile={},fresh=false,food=null,award=null}){
  const items=completion?.pipItems||[],id=profile.avatar||'fox';
  const foodLabel=award?.pipFoodReason==='review'?'+1 food portion · Earned by replay':award?.pipFoodReason==='cooldown'?'Food review ready again: '+new Date(award.pipFoodNextAt*1000).toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}):`${completion?.pipFood===0?'':'+1 food portion · '}${fresh?'Earned with this module':'Earned on first completion'}`;
  return `<section class="checkpoint-pip-reward" data-checkpoint-reward aria-label="Pip checkpoint reward"><div class="checkpoint-pip-stage"><span class="checkpoint-pip" data-checkpoint-pip data-species="${esc(id)}" data-pose="idle" data-dance="1">${companionSprite(id,80,profile.accessory)}</span><div class="checkpoint-confetti" data-checkpoint-confetti aria-hidden="true"></div></div><div class="checkpoint-collection"><h3>${items.length?(fresh?'New for Pip':'Unlocked with this module'):'Food for Pip'}</h3>${items.length?`<ul class="checkpoint-items">${items.map(item=>`<li data-earned-item="${esc(item.key)}">${itemIcon(item)}<span>${esc(item.label)}</span></li>`).join('')}</ul>`:''}<p class="checkpoint-food">${esc(foodLabel)}</p><button type="button" class="text-link" data-action="profile">${canPipPlay(food)?'Decorate Pip’s home':'Feed Pip & decorate its home'} →</button></div></section>`;
}

export function celebrateCheckpoint(host,motion,canPlay=()=>true){
  if(!host||!motion())return ()=>{};
  const pip=host.querySelector('[data-checkpoint-pip]'),layer=host.querySelector('[data-checkpoint-confetti]'),animations=[];
  pip.dataset.pose=canPlay()?'dance':'resting';
  for(let i=0;i<18;i++){
    const piece=document.createElement('i');piece.style.setProperty('--confetti-colour',['#f5ce83','#a5e5d5','#b6acf0','#f4abbd'][i%4]);layer.append(piece);
    const angle=(i/18)*Math.PI*2,dx=Math.cos(angle)*72,dy=-30-Math.abs(Math.sin(angle))*76;
    animations.push(piece.animate([{transform:'translate(0,0) rotate(0deg)',opacity:0},{transform:`translate(${dx*.6}px,${dy}px) rotate(${i*23}deg)`,opacity:1,offset:.3},{transform:`translate(${dx}px,${48+i%4*9}px) rotate(${i*47}deg)`,opacity:0}],{duration:1700+i%3*100,easing:'cubic-bezier(.2,.6,.3,1)',fill:'forwards'}));
  }
  const tidy=()=>{animations.forEach(animation=>animation.cancel());layer.replaceChildren();pip.dataset.pose='idle';};
  const timer=setTimeout(tidy,2100);
  return ()=>{clearTimeout(timer);tidy();};
}
