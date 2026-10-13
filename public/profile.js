import {pipRoomScene,foodBowlArtwork,curtainArtwork} from './pip-items.js?build=120';
import {escapeHTML as esc} from './engine.js?build=120';
import {COMPANIONS,companionSprite} from './companion.js?build=120';
import {AVATARS} from './home.js?build=120';
import {pictureDropdown,homeShelf,pipFoodControls} from './pip-editor.js?build=120';
import {canPipPlay} from './pip-food.js?build=120';
import {itemIcon} from './wins.js?build=120';

let options={accents:[],motivations:[],interests:[],accessories:[],badges:[],home:{}},acceptable=()=>true;
export const profileAccent=value=>options.accents.some(a=>a.id===value)?value:'mint';
export function configureProfile(value,filter){options={...value,home:value.home||{}};if(filter)acceptable=filter;}
export function profileUnlocks(){
  return [['accessory',options.accessories],...Object.entries(options.home).map(([field,choices])=>['home.'+field,choices])].flatMap(([kind,choices])=>choices.filter(c=>c.modules>0).map(c=>({...c,kind,key:kind+':'+c.id})));
}
export function profileValues(form,previous={}){
  const f=new FormData(form);let homePositions=previous.homePositions||{};
  try{homePositions=JSON.parse(f.get('homePositions')||'{}');}catch{}
  return {alias:String(f.get('alias')||'').trim(),avatar:f.get('avatar'),accessory:f.get('accessory')||'none',badge:f.get('badge')||'plain',home:Object.fromEntries(Object.entries(options.home).map(([key,choices])=>[key,f.get('home_'+key)||previous.home?.[key]||choices[0].id])),homePositions,introReady:true,accent:f.get('accent'),motivation:previous.motivation||'confidence',interests:previous.interests||[],nextWin:previous.nextWin||''};
}
export function profileNameError(name,previous=''){
  if(typeof name!=='string'||!name.trim())return 'Give your Pip a name.';
  if(name.length>32||name.length>12&&name!==previous)return 'Pip name: 12 characters maximum.';
  return acceptable(name)?'':'Choose a different Pip name.';
}
export function availableProfileExtras(value,previous={},completed=0,owned=[]){
  const available=(choices,id,old,kind)=>choices.some(c=>c.id===id&&(c.modules<=completed||!c.modules||id===old||owned.includes(kind+':'+id)));
  const next={...value};
  if(!available(options.accessories,next.accessory,previous.accessory,'accessory'))next.accessory=previous.accessory||'none';
  if(next.home)next.home=Object.fromEntries(Object.entries(options.home).map(([field,choices])=>[field,available(choices,next.home[field],previous.home?.[field],'home.'+field)?next.home[field]:previous.home?.[field]||choices[0].id]));
  return next;
}
export function validateProfile(value,connected=true,previous={},completed=0,owned=[]){
  const invalid=(field,message)=>{throw Object.assign(new Error(message),{field});};
  const nameError=profileNameError(value.alias,previous.alias);if(nameError)invalid('alias',nameError);
  if(!AVATARS.includes(value.avatar))invalid('avatar','Choose your Pip.');
  if(value.companionName!==undefined&&(!value.companionName||value.companionName.length>24||value.companionName.length>12&&value.companionName!==previous.companionName))invalid('companionName','Pip name: 12 characters maximum.');
  if(value.companionName!==undefined&&!acceptable(value.companionName))invalid('companionName','Choose a different companion name.');
  if(value.badge!==undefined&&!options.badges.some(item=>item.id===value.badge))invalid('badge','Choose an available profile option.');
  for(const [field,list] of [['accessory','accessories']]){if(value[field]===undefined)continue;const choice=options[list].find(item=>item.id===value[field]);if(!choice||choice.connected&&!connected)invalid(field,'Connect to your mentor to use that extra.');if((choice.modules||0)>completed&&value[field]!==previous[field]&&!owned.includes(field+':'+value[field]))invalid(field,'Pass '+choice.modules+' different modules to unlock this item.');}
  if(value.home){for(const [field,choices] of Object.entries(options.home)){if(value.home[field]===undefined)continue;const choice=choices.find(c=>c.id===value.home[field]);if(!choice)invalid('home_'+field,'Choose an available decoration.');if(choice.modules>completed&&choice.id!==previous.home?.[field]&&!owned.includes('home.'+field+':'+choice.id))invalid('home_'+field,'Pass '+choice.modules+' different modules to unlock this item.');}}
  if(value.homePositions){for(const [key,point] of Object.entries(value.homePositions)){if(!['rug','furniture','decor','painting','shelf'].includes(key)||!point||Object.keys(point).sort().join(',')!=='x,y'||Object.values(point).some(n=>!Number.isFinite(n)||n<0||n>1))invalid('homePositions','Choose valid item positions.');}}
  for(const [field,list] of [['accent','accents'],['motivation','motivations']])if(!options[list].some(item=>item.id===value[field]))invalid(field,'Choose one of the profile options.');
  if(value.interests.length>3||value.interests.some(id=>!options.interests.some(item=>item.id===id)))invalid('interests','Choose up to three interests.');
  if(value.nextWin.length>96)invalid('nextWin','Keep your next win to 96 characters.');
  if(!acceptable(value.nextWin))invalid('nextWin','Reword your next win.');
  return value;
}

export function profilePreview(value={},food=null){
  const accent=profileAccent(value.accent),name=value.alias&&acceptable(value.alias)?value.alias:'Your Pip';
  const room={wall:'teal',rug:'round',furniture:'cushion',decor:'plant',painting:'landscape',shelf:'books',bowl:'gold',curtains:'linen',...value.home};
  // Centre the rug on the visible floor (which starts at 215/310), preserving moved items.
  const positions={rug:{x:.5,y:.845},furniture:{x:.2,y:.68},decor:{x:.83,y:.57},painting:{x:.51,y:.27},shelf:{x:.78,y:.16},...value.homePositions};
  const placed=Object.entries(room).filter(([field,id])=>['rug','furniture','decor','painting','shelf'].includes(field)&&id!=='none').map(([field,id])=>{
    const label=options.home[field]?.find(item=>item.id===id)?.label||id,p=positions[field],icon=itemIcon({key:'home.'+field+':'+id});
    const drawing=field==='rug'?icon.replace('<svg ','<svg preserveAspectRatio="none" '):icon;
    return `<div class="pip-placed-item" data-placed-kind="${field}" data-placed-id="${id}" style="--item-x:${p.x*100}%;--item-y:${p.y*100}%"><button type="button" class="pip-room-piece" data-placed-item="${field}" data-placed-value="${id}" aria-label="Move ${esc(label)}. Drag to the bin or press Delete to put it back.">${drawing}</button></div>`;
  }).join('');
  const curtainName=options.home.curtains?.find(item=>item.id===room.curtains)?.label||'Curtains';
  const curtains=room.curtains==='none'?'':`<div class="pip-placed-item" data-placed-kind="curtains" data-placed-id="${esc(room.curtains)}"><button type="button" class="pip-room-piece" data-placed-item="curtains" data-placed-value="${esc(room.curtains)}" aria-label="Move ${esc(curtainName)}. Drag to the bin or press Delete to put it back."><svg class="pip-room-curtains" data-curtain-style="${esc(room.curtains)}" viewBox="17 37 152 112" preserveAspectRatio="none" aria-hidden="true">${curtainArtwork(room.curtains)}</svg></button></div>`;
  return `<div class="identity-card pip-home pip-home-large${canPipPlay(food)?'':' pip-resting'}" data-profile-accent="${accent}" data-room-wall="${esc(room.wall)}" data-room-rug="${esc(room.rug)}" data-room-furniture="${esc(room.furniture)}" data-home-room data-species="${esc(value.avatar||'fox')}" data-pose="${canPipPlay(food)?'idle':'resting'}" aria-label="${esc(name)}’s home">${pipRoomScene(room.wall,{...room,curtains:'none'})}${placed}${curtains}<button class="pip-trash" type="button" data-home-trash aria-label="Put the selected home item back on the shelf" title="Drag an item here to put it back"><svg viewBox="0 0 56 64" aria-hidden="true"><path d="M14 22h28l-3 33H17Z" fill="#718b91" stroke="#3f5c66" stroke-width="2"/><path d="M21 28v20m7-20v20m7-20v20" stroke="#abc2bc" stroke-width="2"/><g class="pip-trash-lid"><path d="M11 18h34v6H11Z" fill="#a5b9b3" stroke="#47636c" stroke-width="2"/><path d="M23 18v-5h10v5" fill="none" stroke="#a5b9b3" stroke-width="3"/></g><path d="M16 57h24" stroke="#123843" stroke-width="3" opacity=".3"/></svg></button><div class="pip-home-stage"><button type="button" class="pip-home-pet" data-pip-greet aria-label="Dance with ${esc(name)}. Tap to try three dances">${companionSprite(value.avatar||'fox',112,value.accessory,{walkingViews:true})}</button></div><div class="pip-food-bowl" aria-hidden="true"><span data-bowl-food></span><svg viewBox="0 0 80 36" data-bowl-style="${esc(room.bowl)}">${foodBowlArtwork(room.bowl)}</svg></div></div>`;
}

export function profileForm({name='',symbol='fox',profile={},connected=false,setup=false,intro=false,editor=false,readingControls='',panel='pip',theme='',completed=0,owned=[],food=null}={}){
  const v={alias:name,avatar:symbol,companionName:'Pip',accessory:'none',badge:'plain',accent:'mint',motivation:'confidence',interests:[],nextWin:'',...profile};
  if(!COMPANIONS.some(c=>c.id===v.avatar))v.avatar='fox';
  const prefix=editor?'profile-editor':'profile-setup',nameError=v.alias?profileNameError(v.alias,v.alias):'';
  const tabs=`<div class="profile-tabs" role="tablist" aria-label="Profile sections">${[['pip','Pip'],['colour','Colour'],...(readingControls?[['reading','Reading']]:[])].map(([id,label])=>`<button type="button" role="tab" data-profile-tab="${id}" aria-controls="${id==='reading'?'profile-comfort':prefix+'-'+id}" aria-selected="${panel===id}" tabindex="${panel===id?'0':'-1'}">${label}</button>`).join('')}</div>`;
  return `<form data-form="profile" data-completed="${completed}" data-panel="${panel}" ${editor?'id="profile-editor" ':''}${intro?'data-intro="true"':setup?'data-setup="true"':''} class="profile-form pip-studio-form">${tabs}<div class="pip-home-editor" data-profile-panel="pip"><section class="pip-studio" aria-label="Pip’s home"><label class="field profile-name"><span>Pip name <small data-name-count>${v.alias.length>12?v.alias.length+' characters':v.alias.length+'/12'}</small></span><input name="alias" data-original-name="${esc(v.alias)}" value="${esc(v.alias)}" maxlength="12" required autocomplete="off" placeholder="Name your Pip" aria-invalid="${!!nameError}" aria-describedby="${prefix}-name-error"><small id="${prefix}-name-error" class="error-text" data-name-error role="alert">${esc(nameError)}</small></label><div data-profile-preview>${profilePreview(v,food)}</div>${pipFoodControls(food,{species:v.avatar,name:v.alias||'Pip'})}</section><div class="pip-editor-rail"><fieldset class="profile-symbols" id="${prefix}-pip" data-profile-panel="pip"><legend>Your Pip</legend>${pictureDropdown({id:prefix+'-species',label:'Choose your Pip',name:'avatar',items:COMPANIONS,selected:v.avatar})}${pictureDropdown({id:prefix+'-accessory',label:'Pip accessory',name:'accessory',items:options.accessories,selected:v.accessory,avatar:v.avatar,completed,owned})}</fieldset>${homeShelf(options.home,v,completed,owned)}</div></div><fieldset class="profile-colours" id="${prefix}-colour" data-profile-panel="colour"><legend>Colour</legend><div class="profile-choice-grid">${options.accents.map(a=>`<label class="profile-choice" data-profile-accent="${a.id}"><input type="radio" name="accent" value="${a.id}" ${v.accent===a.id?'checked':''}><span class="colour-dot" aria-hidden="true"></span><span>${a.label}</span></label>`).join('')}</div></fieldset>${readingControls}<input type="hidden" name="badge" value="${esc(v.badge)}"><p class="error-text" id="profile-error" role="alert"></p>${editor?'':`<button class="btn" type="submit">${intro||setup?'Continue →':'Save profile'}</button>`}</form>`;
}
export function openingMarkup(){
  return `<section class="launch-sequence" aria-label="Opening Stepstone">
    <div class="launch-content">
      <svg class="launch-stones" viewBox="0 0 480 300" aria-hidden="true" focusable="false">
        <defs>
          <linearGradient id="launch-stone-face" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#cefff3"/><stop offset="1" stop-color="#5ad9c5"/></linearGradient>
          <linearGradient id="launch-stone-edge" x2="0" y2="1"><stop stop-color="#40978c"/><stop offset="1" stop-color="#1f5c60"/></linearGradient>
        </defs>
        <ellipse class="launch-ground" cx="241" cy="264" rx="155" ry="17" fill="#081f29"/>
        <path class="launch-guide" d="M60 264h82v-78h64v-58h64V72h70v176H142" fill="none" stroke="#9dc1b7" stroke-width="1.5"/>
        <g class="launch-stone launch-stone-one">
          <path d="M142 186h64v62h-64z" fill="url(#launch-stone-face)"/>
          <path d="M142 234h64v14h-64z" fill="url(#launch-stone-edge)"/>
          <path class="launch-stone-top" d="M143 187h62"/>
          <path class="launch-stone-grain" d="M153 201h20m12 15h11m-43 8h9"/>
        </g>
        <g class="launch-stone launch-stone-two">
          <path d="M206 128h64v120h-64z" fill="url(#launch-stone-face)"/>
          <path d="M206 234h64v14h-64z" fill="url(#launch-stone-edge)"/>
          <path class="launch-stone-top" d="M207 129h62"/>
          <path class="launch-stone-grain" d="M217 145h18m10 33h13m-41 42h12"/>
        </g>
        <g class="launch-stone launch-stone-three">
          <path d="M270 72h70v176h-70z" fill="url(#launch-stone-face)"/>
          <path d="M270 234h70v14h-70z" fill="url(#launch-stone-edge)"/>
          <path class="launch-stone-top" d="M271 73h68"/>
          <path class="launch-stone-grain" d="M282 92h19m15 31h12m-46 45h14m18 46h14"/>
        </g>
        <path class="launch-step-light" d="M60 264h82v-78h64v-58h64V72h70" pathLength="1" fill="none" stroke="#c9fff0" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div class="launch-copy"><strong class="launch-wordmark"><span>Step</span><span>Stone</span></strong><p class="launch-tagline">Your next step.</p></div>
    </div>
    <p class="launch-status" role="status">Opening Stepstone…</p>
  </section>`;
}
