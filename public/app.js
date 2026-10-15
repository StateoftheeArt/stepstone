import {practiceRound} from './lesson-questions.js?build=123';
import {lessonSourceFooter} from './canadian-money.js?build=123';
import {commonPitfall} from './lesson-help.js?build=123';
import {canMessageMentor,createInbox,messageInbox} from './mentor-messages.js?build=123';
import {installPipEditor,paintFood} from './pip-editor.js?build=123';
import {canPipPlay,previewFood,feedPreviewFood,awardPreviewReview} from './pip-food.js?build=123';
import {dailyTasksMarkup,previewDaily,dailyDay} from './daily-tasks.js?build=123';
import {laptopFinderMarkup} from './laptop-finder.js?build=123';
import {previewStartingItems,startingItemUnits} from './starting-items.js?build=123';
import {activeUnits,canonicalSubject,suggestedStart} from './curriculum.js?build=123';
import {createCompanion} from './companion.js?build=123';
import {createLessonAdvance} from './lesson-feedback.js?build=123';
import {projectMarkup,mountProject,mentorProject,mountMentorProjects} from './project-workshop.js?build=123';
import {aiPlanForm,aiManager,aiMentorForm} from './ai-support.js?build=123';
import {typingSummary,typingReport} from './typing-lab.js?build=123';
import {devicePanel,deviceForm,mentorDevice,deviceReviewForm} from './device-work.js?build=123';
import {previewFoundation,foundationIds,nextFoundationUnit,mentorFoundation,moduleAccess,nextCourseUnit,courseGateMarkup,courseReadiness,accessMessage} from './foundation.js?build=123';
import {resolveEntryRole,roleEntry,learnerSpace,spaceGuide,managerNavigation,managerSettings,mentorAccess,refreshMentorAccess,mentorDeviceSettings,personalLearningTools,inviteCard,copyPrivateLink,keepHostInformed} from './manager.js?build=123';
import {escapeHTML as esc,correct,sample,mastery,reviewDue,mergeStages,readable,numberValue,startingPoint,startingQuestion,rewardEligibility} from './engine.js?build=123';
import {canonicalHubHash,hubSectionForHash,learningHubMarkup} from './progress-hub.js?build=123';
import {homeMarkup,avatar,AVATARS,hasStartedLearning,startingPlanMarkup} from './home.js?build=123';
import {requirements,stockManagement,fundedManager,personForm,allocationForm,fundingForm,updateFundingForm,stockRemoveForm,releaseForm,fundedClaimForm,exportFunding,cardExchange,cardRequestForm,cardClaimForm,cardKeyView} from './rewards.js?build=123';
import {createTutorial} from './tutorial.js?build=123';
import {profileForm,openingMarkup,configureProfile,profileValues,validateProfile,profilePreview,profileAccent,profileNameError,availableProfileExtras,profileUnlocks} from './profile.js?build=123';
import {firstPasses,previewCompletions,preservePreviewCompletions,winsMarkup} from './wins.js?build=123';
import {createReader,narrationText,voiceOptions} from './read-aloud.js?build=123';
import {createTextFilter} from './text-filter.js?build=123';
import {configureLanguage,installLanguageGuard,assertLanguagePayload,displayPayload} from './language.js?build=123';
installLanguageGuard();
import {mountLessonVisual} from './lesson-visual.js?build=123';
import {reflectionMarkup,reflectionSpec} from './reflection.js?build=123';
import {checkpointCompletion,checkpointMarkup,createCheckpointQueue,celebrateCheckpoint} from './checkpoint.js?build=123';
let lessonExample=null,checkpointStop=()=>{};
const checkpointQueue=createCheckpointQueue();

import {isMission,missionHeader,missionIntro,missionLesson,missionPractice,cursorFor,mountMissionLab,missionLabReady,missionLabAnswer,nextMissionTask,resetMissionLabs,showMissionPane,openPracticeExample,returnFromExample} from './mission.js?build=123';

const $=s=>document.querySelector(s),root=$('#main'),dialog=$('#dialog');
const topbar=$('#app-header');
new ResizeObserver(()=>document.documentElement.style.setProperty('--topbar-height',Math.ceil(topbar.getBoundingClientRect().height)+'px')).observe(topbar);
const missionTransition=createLessonAdvance();
const ICONS={home:'M3 10 12 3l9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z',path:'M5 4h5v5H5zM14 15h5v5h-5zM8 9v7a2 2 0 0 0 2 2h4',progress:'M4 20V10m8 10V4m8 16v-7',rewards:'M5 8h14v13H5zM3 4h18v4H3zM12 4v17M12 4C8-3 1 5 12 4M12 4c4-7 11 1 0 0',numbers:'M5 5h6M8 2v6M15 5h6M4 14l6 6m0-6-6 6M15 15h6m-6 4h6',words:'M3 4h7l2 2 2-2h7v15h-7l-2 2-2-2H3zM12 6v15',pencil:'m4 16 12-12 4 4L8 20H4zM13 7l4 4',spark:'m13 2-9 12h7l-1 8 10-13h-8z',compass:'M5 4h14v12H9l-4 4zM8 8h8M8 12h5'};
const icon=(name,cls='')=>`<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${ICONS[name]||ICONS.spark}"/></svg>`;
let foundationPlan,catalog,me=null,mentor=null,health={},route='home',subject='math',lessonId=null,local={},pending=[],storageOK=true,settings={},recovery=null,online=true,working=false,syncing=false,toastTimer,installPrompt;
let lastInvite=null,guestScope='guest',pendingInvite='',nameFilter=()=>true,entryRole=null;
let startingBank,starting=null,startingFlight=null,startingTimer,appReady=false,lastMotionKey='';
const tutorial=createTutorial({
  root,dialog,me:()=>me,guestOwner:()=>guestScope,route:()=>route,catalog:()=>catalog,
  starting:startResult,hasStartingAnswers:()=>!!starting?.data?.answers.length,
  profile:currentProfile,guidePet:(anchor,key)=>companion.followGuide(anchor,key),api,toast,remember:rememberMe,navigate,render,motion:motionAllowed,
  html,readButton,questionCard,unitCard,wins:progressView,home:homeContent,modal,
  stopReading:()=>reader.stop(),refreshAccount,next:plannedNext,startingPlan:guideStartingPlan,beginPlan:startFromPlan,transition:animateView,
  profileForm:value=>profileForm({name:currentProfile().alias,symbol:currentProfile().avatar,profile:value||currentProfile(),connected:!!me,completed:passed().size,owned:currentInventory(),food:currentFood(),theme:currentTheme(),setup:true,readingControls:readingControls()}),
  mentorStep:mentorSetupMarkup,goalForm:goalSetupMarkup,rewardIntro:rewardTourMarkup
});
try{settings=JSON.parse(localStorage.getItem('stepstone-comfort-v1')||'{}');}catch{}
// Comfort settings are device-wide; a profile belongs to one person. Move an older device-wide guest profile once.
if(settings.profile)try{if(!localStorage.getItem('stepstone-guest-profile-v1-guest'))localStorage.setItem('stepstone-guest-profile-v1-guest',JSON.stringify({...settings.profile,alias:settings.profile.alias||settings.nickname||''}));}catch{}
settings=Object.fromEntries(Object.entries(settings).filter(([key])=>['focus','quiet','voice'].includes(key)));
try{localStorage.setItem('stepstone-comfort-v1',JSON.stringify(settings));}catch{}
const reader=createReader({settings:()=>settings,toast,softVoice:()=>health.softVoice});
const companion=createCompanion({profile:currentProfile,ready:()=>appReady&&!!entryRole&&(route!=='mentor'||entryRole==='learner'),motion:motionAllowed,canPlay:()=>canPipPlay(currentFood()),onPlay:recordPipPlay,edit:profileDialog,owner:()=>me?.id||guestScope});
dialog.addEventListener('close',()=>{document.body.append($('#toast'));applyProfileColour(currentProfile().accent);companion.dockIn(null);managerSection=null;delete dialog.dataset.managerPanel;dialog.classList.remove('manager-overlay','profile-overlay');dialog.querySelector('[data-dialog-footer]')?.remove();});
const inbox=createInbox({api,me:()=>me,mentor:()=>route==='mentor'&&!!mentor,identity:id=>mentor?.learners?.find(l=>l.id===id)||(me?.id===id?me:null),modal,dialog,toast,refresh:()=>{if(me)refreshAccount().catch(()=>{});if(route==='mentor'&&entryRole==='mentor')loadMentor();}});
function html(text=''){return String(text).split(/(\$[^$]+\$)/g).map(part=>part.startsWith('$')&&part.endsWith('$')?`<span data-say="${esc(readable(part))}">${window.katex.renderToString(part.slice(1,-1),{throwOnError:false,strict:'ignore',output:'htmlAndMathml'})}</span>`:esc(part)).join('');}
function formatDate(at){return new Date(at*1000).toLocaleDateString(undefined,{month:'short',day:'numeric'});}
function unit(id){return catalog.units.find(u=>u.id===id);}
function sub(id){return catalog.subjects.find(s=>s.id===canonicalSubject(id))||catalog.subjects[0];}
function key(){return 'stepstone-work-v1-'+(me?.id||guestScope);}
function loadLocal(){try{const saved=JSON.parse(localStorage.getItem(key())||'{}');local=saved.units||{};pending=(saved.pending||[]).filter(item=>item.type!=='activity');}catch{local={};pending=[];}if(me)local=mergeStages(local,me.progress);loadStarting();tutorial.load();}
function persist(){if(route==='lesson'&&lessonId){draft().touchedAt=Date.now();if(me){draft()._dirty=true;queueDraft();}}saveLocal();}
function saveLocal(){try{localStorage.setItem(key(),JSON.stringify({units:local,pending}));storageOK=true;}catch{storageOK=false;toast('This browser could not save your work. Please keep this page open.');}status();}
function draft(id=lessonId){const d=local[id]??={};d.phase??=0;d.rounds??={};d.reflection??='';d.ink??=[];d.support??='myself';return d;}
function rememberMe(){if(!me)return;try{localStorage.setItem('stepstone-session-preview-v1',JSON.stringify({...me,attempts:me.attempts.map(a=>({...a,report:{...a.report,questions:[],ink:[]}}))}));}catch{}}
function toast(message){const notice=$('#toast');(dialog.open?dialog:document.body).append(notice);notice.textContent=message;notice.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>notice.classList.remove('show'),6500);}
function errorText(error){return error?.message||'Something did not finish. Please try again.';}
async function api(path,data){
  if(data)assertLanguagePayload(data);
  if(data&&me&&['/api/progress','/api/attempt','/api/submit','/api/reward','/api/daily/play','/api/pip/feed','/api/profile','/api/draft','/api/starting-point','/api/reward-goal','/api/tutorial'].includes(path))data={learner:me.id,...data};
  let response;try{response=await fetch(path,{method:data===undefined?'GET':'POST',headers:data===undefined?{}:{'Content-Type':'application/json'},body:data===undefined?undefined:JSON.stringify(data),cache:'no-store',credentials:'same-origin'});}catch{online=false;status();throw new Error('You are offline. Your work stays on this device.');}
  online=true;const result=await response.json();if(!response.ok){const message=result.error||'The request did not finish.';const error=new Error(/\/(?:reward|cards|mentor\/(?:cards|claim))/.test(path)?message.replace(/\bpoints\b/gi,'Steps'):message);error.status=response.status;throw error;}if(path==='/api/me'&&me&&result.id!==me.id){localStorage.removeItem('stepstone-session-preview-v1');me=null;local={};pending=[];loadStarting();tutorial.load();if(dialog.open)dialog.close();render();throw new Error('The learner changed in another tab. Reload to open the current account. Your previous work stays saved.');}return path==='/api/drafts'?result:displayPayload(result);
}
function applyProfileColour(accent){
  const preview=$('dialog[open] form[data-form="profile"] input[name="accent"]:checked,main form[data-form="profile"] input[name="accent"]:checked');
  document.documentElement.dataset.accent=profileAccent(accent??preview?.value??currentProfile().accent);
}
function status(){applyProfileColour();const ds=$('#draft-status');if(ds)ds.textContent=!storageOK?'This browser could not save your draft.':me&&Object.values(local).some(d=>d._dirty)?'Draft saved here. Waiting to sync.':'';if(me)rememberMe();}
function currentTheme(){return localStorage.getItem('stepstone-theme-'+(me?.id||'guest'))||'';}
function applySettings(){document.documentElement.classList.remove('focus-mode');document.documentElement.classList.toggle('quiet',settings.quiet===true);stopQuietMotion();document.documentElement.classList.remove('theme-ocean','theme-sunset');}
function nav(){const current=route==='lesson'?'path':route;$('#navigation').innerHTML=[['home','Home','home'],['path','Learn','path'],['progress','Rewards','rewards']].map(([id,title,symbol])=>`<a class="nav-item" href="#${id}" ${current===id?'aria-current="page"':''} ${entryRole==='mentor'&&!me?'data-action="mentor-learning" data-destination="'+id+'"'+(!mentor?' aria-disabled="true"':''):''}>${icon(symbol)}<span>${title}</span></a>`).join('');if(route==='mentor')$('#mentor-control').setAttribute('aria-current','page');else $('#mentor-control').removeAttribute('aria-current');status();tutorial.decorateNav();}
function navigate(hash){if(location.hash===hash)readRoute();else location.hash=hash;}
function focusHubSection(hash){const hubSection=route==='progress'&&!tutorial.visible()?hubSectionForHash(hash):null;if(hubSection)requestAnimationFrame(()=>{if(location.hash===hash){const section=root.querySelector('#'+hubSection);let parent=section?.parentElement;while(parent&&parent!==root){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}section?.scrollIntoView({behavior:motionAllowed()?'smooth':'instant',block:'start'});}});}
function readRoute(){cancelMissionAdvance();lessonExample?.dispose();lessonExample=null;checkpointStop();tutorial.cancel();if(!appReady)return;reader.stop();const entry=/^#(?:join|resume)(?:\/|$)/.test(location.hash);const hash=entry?location.hash:entryRole==='mentor'&&!me?'#mentor':tutorial.canonical(canonicalHubHash(location.hash||'#home'));if(hash!==location.hash)history.replaceState(null,'',location.pathname+location.search+hash);const bits=hash.slice(1).split('/');route=bits[0]||'home';if(!['home','path','progress','lesson','mentor','join','resume'].includes(route)){route='home';history.replaceState(null,'',location.pathname+location.search+'#home');}if(['join','resume'].includes(route)&&bits[1]){keepEntryCode(route,bits[1]);history.replaceState(null,'',location.pathname+location.search+'#'+route);}if(route==='path'&&catalog.subjects.some(s=>s.id===canonicalSubject(bits[1])))subject=canonicalSubject(bits[1]);if(route==='lesson'){lessonId=bits[1];if(!unit(lessonId)?.ready){route='path';lessonId=null;}else if(!tutorial.visible()){const access=moduleAccess({catalog,unit:unit(lessonId),done:passed(),local,starting:startResult(),plan:currentFoundation()});if(!access.allowed){subject=unit(lessonId).subject;route='path';lessonId=null;history.replaceState(null,'',location.pathname+location.search+'#path/'+subject);toast(accessMessage(access));}else persist();}}
  if(route==='mentor'){render();if(entryRole==='mentor')loadMentor();}else {render();if(me&&!tutorial.locked()&&(['progress','path'].includes(route)||route==='home'&&!showWelcome())){const view=route,owner=me.id;api('/api/me').then(result=>{if(me?.id!==owner)return;me=result;status();if(route===view&&location.hash===hash&&!dialog.open&&!working){render();focusHubSection(hash);}}).catch(()=>{});}}root.focus({preventScroll:true});window.scrollTo(0,0);focusHubSection(hash);
}
function render(){if(!appReady)return;companion.update();document.documentElement.dataset.page=route;document.documentElement.dataset.area=route==='lesson'?(unit(lessonId)?.subject||'math'):route==='path'?subject:route;document.documentElement.classList.toggle('profile-entry',route==='home'&&showWelcome());nav();if(['join','resume'].includes(route)){entryView();document.documentElement.dataset.ready='true';return;}if(!entryRole){root.innerHTML=roleEntry();document.documentElement.dataset.ready='true';return;}if(entryRole==='learner'&&route==='mentor'){root.innerHTML=learnerSpace(me,{locked:tutorial.locked()});document.documentElement.dataset.ready='true';return;}if(tutorial.visible()){tutorial.render();document.documentElement.dataset.ready='true';return;}tutorial.leaving();if(route==='home')home();else if(route==='path')pathView();else if(route==='join'||route==='resume')entryView();else if(route==='progress')progressView();else if(route==='mentor')mentorView();else lessonView();document.documentElement.dataset.ready='true';if(route!=='lesson')animateView(route==='home'?`home/${starting?.data?.answers.length||0}`:route==='path'?`path/${subject}`:route);}
const button=(label,action,data='',style='')=>`<button class="btn ${style}" data-action="${action}" ${data}>${label}</button>`;
function startButton(id,label='Start learning',style='',revisit=false){return `<a class="btn ${style}" href="#lesson/${id}"${revisit?` data-action="revisit" data-unit="${esc(id)}"`:''}>${esc(label)} <span class="arrow" aria-hidden="true">↗</span></a>`;}
function revisitLesson(id){
  const u=unit(id),d=local[id];
  if(u?.ready&&passed().has(id)&&!pending.some(p=>p.unit===id)&&!(d?.phase>0&&d.phase<7)){
    const work=draft(id);work.phase=1;work.rounds={};resetMissionLabs(u,work);saveLocal();
  }
  navigate('#lesson/'+id);
}
function passed(){return me?new Set(me.mastered||[...mastery(me.attempts||[])]):new Set(Object.entries(local).filter(([,d])=>d.firstPass?.report?.passed||d.result?.passed).map(([id])=>id));}
function currentFoundation(){return me?.foundation||previewFoundation(foundationPlan);}
function nextUnit(){return nextFoundationUnit({catalog,plan:currentFoundation(),local,done:passed(),starting:startResult()});}
function home(){
  if(showWelcome()){welcomeView();return;}
  homeContent();
}
function plannedNext(){return hasStartedLearning({local,me})?nextUnit():nextFoundationUnit({catalog,plan:currentFoundation(),done:passed(),starting:startResult()});}
function guideStartingPlan(action='finish',guideStep=null){return startingPlanMarkup({catalog,result:startResult(),next:plannedNext(),action,guide:true,guideStep,readButton});}
function startFromPlan(id=plannedNext()?.id){
  if(!unit(id)?.ready)return;
  const d=draft(id);d.startedFromPlan=true;d.touchedAt=Date.now();
  if(me){d._dirty=true;queueDraft();}saveLocal();navigate('#lesson/'+id);
}
function homeContent(){
  const next=nextUnit(),profile=currentProfile(),startingPlan=!hasStartedLearning({local,me})?startingPlanMarkup({catalog,result:startResult(),next:plannedNext(),locked:tutorial.locked(),readButton}):'';
  root.innerHTML=homeMarkup({me,catalog,next,draft:next?local[next.id]:null,html,done:passed(),guestAvatar:profile.avatar,guestName:me?'':profile.alias,profile,startingPlan,dailyTasks:dailyTasksMarkup(currentDaily(),{name:profile.alias,connected:!!me,next})});
}
function dailyKey(){return 'stepstone-daily-v1-'+guestScope;}
function currentDaily(){return me?.dailyTasks||previewDaily(localStorage,dailyKey(),'visit');}
function paintDaily(){
  const panel=root.querySelector('[data-daily-tasks]');if(!panel)return;
  const record=currentDaily(),name=currentProfile().alias,next=nextUnit(),signature=[record.day,...record.completed,name,me?.id||guestScope,next?.id||''].join('|');
  if(panel.dataset.dailySignature===signature)return;
  panel.outerHTML=dailyTasksMarkup(record,{name,connected:!!me,next});
  root.querySelector('[data-daily-tasks]').dataset.dailySignature=signature;
}
let dailyPlayFlight=null;
function recordPipPlay(){
  if(!me){previewDaily(localStorage,dailyKey(),'play');paintDaily();return;}
  if(me.dailyTasks?.day===dailyDay()&&me.dailyTasks.completed.includes('play')||dailyPlayFlight)return;
  const owner=me.id;
  dailyPlayFlight=api('/api/daily/play',{}).then(result=>{if(me?.id===owner){me=result;rememberMe();paintDaily();}}).catch(error=>toast(errorText(error))).finally(()=>{dailyPlayFlight=null;});
}
function foodKey(){return 'stepstone-pip-food-v2-'+guestScope;}
function currentFood(){if(me)return me.pipFood||null;try{return previewFood(localStorage,foodKey(),[...passed()]);}catch{return null;}}
function currentInventory(){
  if(me)return me.pipInventory||[];
  const earned=previewCompletions(local,profileUnlocks()).flatMap(c=>(c.pipItems||[]).map(item=>item.key));
  try{return [...new Set([...earned,...previewStartingItems({storage:localStorage,key:'stepstone-pip-starting-v1-'+guestScope,catalog,result:startResult(),done:[...passed()],unlocks:profileUnlocks()})])];}catch{return earned;}
}
function previewItemUnits(){
  let saved;try{saved=JSON.parse(localStorage.getItem('stepstone-pip-starting-v1-'+guestScope)||'null');}catch{}
  const valid=new Set(activeUnits(catalog).map(u=>u.id));
  return [...new Set([...(Array.isArray(saved?.units)?saved.units:[]).filter(id=>valid.has(id)),...startingItemUnits(catalog,startResult())])];
}
let feedReceipt=null;
async function feedPip(){
  const owner=me?.id||guestScope;
  if(me){
    feedReceipt=feedReceipt?.owner===owner?feedReceipt:{owner,id:crypto.randomUUID()};
    const result=await api('/api/pip/feed',{requestId:feedReceipt.id,learner:owner});
    if(me?.id!==owner)return;
    feedReceipt=null;me=result;rememberMe();
  }else{feedPreviewFood(localStorage,foodKey(),[...passed()]);}
  companion.update();
}
installPipEditor({preview:updateProfilePreview,food:currentFood,feed:feedPip,motion:motionAllowed,toast,onPlay:recordPipPlay});
setInterval(()=>{if(!appReady||document.hidden)return;const form=$('dialog[open] .pip-studio-form,main .pip-studio-form');if(form)paintFood(form,currentFood());if(route==='home')paintDaily();companion.update();},1000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&appReady){paintFood($('dialog[open] .pip-studio-form,main .pip-studio-form'),currentFood());companion.update();}});
function guestProfileKey(){return 'stepstone-guest-profile-v1-'+guestScope;}
function guestProfile(){try{return JSON.parse(localStorage.getItem(guestProfileKey())||'null');}catch{return null;}}
function setEntryRole(value){entryRole=value;try{if(value)localStorage.setItem('stepstone-entry-role-v1',value);else localStorage.removeItem('stepstone-entry-role-v1');}catch{}}
function currentProfile(){const guest=me?null:guestProfile();return {...(me?.profile||guest||{avatar:'orbit'}),alias:me?.alias||guest?.alias||''};}
async function refreshAccount(){if(!me)return null;const owner=me.id,fresh=await api('/api/me');if(me?.id===owner){me=fresh;rememberMe();status();}return fresh;}


function motionAllowed(){return settings.quiet!==true&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches;}
function stopQuietMotion(){companion?.quiet();if(!motionAllowed()){lessonExample?.stop();checkpointStop();document.getAnimations().forEach(a=>a.cancel());}}
window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',stopQuietMotion);
function animateView(key){
  if(!appReady||key===lastMotionKey)return;
  lastMotionKey=key;
  root.getAnimations().forEach(a=>a.cancel());
  const surface=route==='lesson'?$('#lesson-body'):root;
  if(motionAllowed())surface?.animate([{opacity:0,transform:'translateY(6px)'},{opacity:1,transform:'none'}],{duration:360,easing:'cubic-bezier(.22,.65,.3,1)'});
}
async function pauseLearning(){
  reader.stop();
  const inTour=tutorial.visible();
  if(route==='lesson'&&!inTour)persist();
  const saved=inTour?tutorial.pause():route==='home'&&starting?.data?saveStarting():storageOK;
  modal('Pause right here.',`<div class="pause-card"><p>You can take a break without starting over.</p><p class="notice">${saved?'Come back to this step whenever you’re ready.':'This browser could not save your work. Keep this page open so you can return to it.'}</p><div class="buttons">${button('Back to what I was doing','close')}${saved?button('Go home for now','pause-home','','secondary'):''}</div><p class="legend">A break does not take away your progress or Steps.</p>${serviceHelp()}</div>`);
  if(inTour)tutorial.sync();
  else if(me&&route==='lesson')flushDrafts();
  if(me&&starting?._dirty)syncStarting();
}

function startingKey(){return 'stepstone-starting-v1-'+(me?.id||guestScope);}
function loadStarting(){
  clearTimeout(startingTimer);
  try{starting=JSON.parse(localStorage.getItem(startingKey())||'null');if(starting?.data)startingPoint(startingBank,starting.data);}catch{starting=null;}
  if(me?.startingPoint&&!starting?._dirty&&(me.startingPoint.revision>=(starting?.revision||0))){starting={...me.startingPoint,dismissed:starting?.dismissed===true};saveStarting();}
}
function saveStarting(){try{localStorage.setItem(startingKey(),JSON.stringify(starting));return true;}catch{storageOK=false;toast('Keep this page open. The browser could not save your starting check.');return false;}}
function startResult(){return starting?.data?startingPoint(startingBank,starting.data):null;}
function showWelcome(){return tutorial.early()||!!starting?.reviewing&&!startResult()?.complete;}
function welcomeTitle(){const guest=currentProfile().alias;return me?(me.personal?'Your own next step.':`Hey, ${esc(me.alias)}.`):guest?`Hey, ${esc(guest)}.`:'Small steps. Big moves.';}
async function beginStarting(age){
 if(!Number.isInteger(age)||age<5||age>99)throw new Error('Enter your age as a whole number from 5 to 99.');
 await syncStarting();if(starting?._conflict)throw new Error(starting._error);
 const bits=new Uint16Array(1);crypto.getRandomValues(bits);starting={revision:starting?.revision||0,reviewing:tutorial.done(),data:{version:5,age,seed:bits[0],answers:[]},_dirty:!!me};saveStarting();await syncStarting();if(dialog.open)dialog.close();navigate('#home');
}
function ageForm(age=''){
  return `<form data-form="starting-age"><label class="field"><span>How old are you?</span><input name="age" type="number" inputmode="numeric" min="5" max="99" step="1" required autocomplete="off" value="${esc(age)}" aria-describedby="age-help"></label><p class="legend" id="age-help">Age helps your mentor understand your starting point. Your answers choose the lessons, not your age. No birthday needed.</p><button class="btn entry-start" data-action="form-submit">Continue →</button><p class="error-text" id="starting-error" role="alert"></p></form>`;
}
function welcomeView(){
  if(tutorial.early()){
    const step=tutorial.stage();
    if(!starting?.data){
      root.innerHTML='<section class="setup-entry card"><p class="eyebrow">YOUR FIRST STEP</p><h1>How old are you?</h1><p>Just your age. You do not need to give your birthday.</p>'+ageForm()+'<button class="text-link" data-action="account">I already have a sign-in code</button></section>';return;
    }
    if(step==='welcome'&&!currentProfile().introReady){
      root.innerHTML='<section class="setup-entry early-profile card"><h1>Choose your Pip</h1>'+profileForm({name:currentProfile().alias,symbol:currentProfile().avatar,profile:tutorial.export()?.profileDraft||currentProfile(),connected:!!me,completed:passed().size,owned:currentInventory(),food:currentFood(),theme:currentTheme(),intro:true,readingControls:readingControls()})+'</section>';return;
    }
    if(step==='welcome'){
      root.innerHTML='<section class="setup-entry card" id="setup-welcome"><p class="eyebrow">WELCOME TO STEPSTONE</p><h1>You and your companion are ready.</h1><p>Learn things you can use: handling money, reading messages, getting ready for work and using technology.</p><p>'+(starting?.data?.version===1?'First, try 10 starting questions.':starting?.data?.version===2?'First, try up to 6 questions in each of 6 areas.':'First, try '+(starting?.data?.version===3?'4':starting?.data?.version===5?'6':'8')+' questions in each of '+(starting?.data?.version===5?'4':'6')+' areas.')+' This helps us choose where to start.</p><p class="notice">Not sure? Choose “I don’t know yet”. That is OK. You still earn 5 Steps for finishing the starting questions.</p><p>No timer. No grades on your profile. You can stop and come back.</p>'+readButton('setup-welcome')+'<button class="btn setup-main" data-tour="welcome">Let’s try the questions →</button></section>';return;
    }
    if(step==='celebrate'){
      root.innerHTML='<section class="setup-entry setup-celebrate card"><span class="setup-point-mark" aria-hidden="true"><img src="points.svg" alt="">+5</span><p class="eyebrow">STARTING QUESTIONS COMPLETE</p><h1>Awesome. You showed up.</h1><p>You earned 5 Steps for finishing the questions. You did not need to know every answer.</p><p>'+(!me?'Your Steps from the starting questions are saved here. Connect your mentor during setup to save them to your account.':starting?._dirty?'Your answers are saved here. The Steps will reach your account when connected.':'Your Steps are saved to your account.')+'</p><button class="btn setup-main" data-tour="celebrate">How do Steps work? →</button></section>';return;
    }
    if(step==='points'){
      root.innerHTML='<section class="setup-entry card" id="setup-points"><h1>Small steps add up.</h1><ol class="points-explainer"><li><strong>5 Steps for the questions.</strong><span>Honest “I don’t know yet” answers count.</span></li><li><strong>5 more Steps for your guided tour.</strong><span>Learn the controls and make your space yours.</span></li><li><strong>Keep learning towards your goals.</strong><span>Lesson checks earn Steps. Your mentor reviews your work and agrees real rewards.</span></li></ol>'+readButton('setup-points')+'<button class="btn setup-main" data-tour="points">Show me Home →</button></section>';return;
    }
  }
  const result=startResult(),index=starting?.data?.answers.length||0;
  root.innerHTML=`${result?'<div class="page-head starting-head"><div><h1>Your starting check</h1><p>No timer. Take it one step at a time.</p></div></div>':`<div class="page-head"><div><p class="eyebrow">${me?.personal?'MY LEARNING · PRIVATE':'WELCOME TO STEPSTONE'}</p><h1>${welcomeTitle()}</h1><p>Let’s find a comfortable place to begin.</p></div></div>`}<section class="welcome-flow card" id="welcome-flow"></section>`;
  const host=$('#welcome-flow');
  if(!result){
    host.innerHTML=`<div class="welcome-mark" aria-hidden="true">${avatar(currentProfile().avatar,80)}</div><p class="eyebrow">YOUR FIRST STEP</p><h2>A start that works for you.</h2><p>Try a few reading, writing, number and practical tasks to find a useful starting point.</p><ul class="starting-intro"><li>6 questions in each of the first four courses. 24 questions in all, saved as you go.</li><li>No timer. You can listen, take a break, or say “I don’t know yet”.</li><li>Your lessons will help us check these first suggestions.</li></ul>${ageForm()}<p class="legend">${me?(me.personal?'This stays in your own learning record.':'Your mentor can see your age, answers, and suggested modules. Other learners cannot.'):'Try it here without an account. This demo stays on this browser; no report is sent.'}</p>`;
  }else if(result.questionsDone){
    const w=starting.data.writing||{text:'',support:'myself'};
    host.innerHTML=`<p class="eyebrow">ONE LAST THING · YOUR WORDS</p><h2>Write a short message.</h2><p>One or two sentences is enough. Focus on what you mean. Spelling can come later.</p><div id="starting-copy"><p class="starting-scene">${esc(startingBank.writing.prompt)}</p></div><button class="read-button" data-action="starting-read">▷ Read this task aloud</button><label class="field"><span>Your message to Jo</span><textarea name="starting-writing" maxlength="1000" rows="4" aria-describedby="writing-help">${esc(w.text)}</textarea></label><p class="legend" id="writing-help">This is a practice message. It goes in your learning record; it is not sent to Jo. ${me&&!me.personal?'Your mentor can read it.':''} It will not be automatically graded.</p><label class="field"><span>What help did you use?</span><select name="starting-support">${[['myself','I wrote it myself'],['person','A person helped'],['tool','A tool helped, such as dictation or AI'],['mixed','A person and a tool helped']].map(([v,t])=>`<option value="${v}" ${w.support===v?'selected':''}>${t}</option>`).join('')}</select></label><div class="buttons">${button('Save my starting plan →','starting-write')}${button('Not ready to write yet','starting-skip-writing','','secondary')}</div>${startingSaveMarkup()}`;
  }else{
    const q=startingQuestion(startingBank,starting.data,result.next),v2=starting.data.version>=2,d=starting.data.draft;
    document.documentElement.dataset.area=q.subject;
    const order=(q.options||[]).map((_,i)=>(i+starting.data.seed+index)%q.options.length),value=d?.id===q.id?d.answer:null;
    const areas=starting.data.version===5?startingBank.foundation.subjects:starting.data.version===4?startingBank.extended.subjects:startingBank.subjects;
    const progress=v2?`Area ${result.sectionIndex+1} of ${areas.length} · question ${result.questionInSection}${starting.data.version===5?' of 6':starting.data.version===4?' of 8':starting.data.version===3?' of 4':''}`:`${index+1} of 10`;
    const visual=q.visual?.groups?`<div class="starting-count" role="img" aria-label="${esc(q.visual.label)}">${q.visual.groups.map(g=>`<span>${Array.from({length:g},()=>'<i aria-hidden="true"></i>').join('')}</span>`).join('<b aria-hidden="true">+</b>')}</div>`:'';
    host.innerHTML=`<div class="horizontal"><p class="eyebrow">${esc(startingAreaName(q.subject))}</p><span class="pill" data-starting-progress>${progress}</span></div>${v2?`<ol class="starting-areas" aria-label="Starting check areas">${areas.map((s,i)=>`<li ${s===q.subject?'aria-current="step"':''} class="${i<result.sectionIndex?'done':''}"><span class="starting-area-mark" aria-hidden="true">${i<result.sectionIndex?'✓':i+1}</span><span class="starting-area-name">${esc(startingAreaName(s))}</span></li>`).join('')}</ol><p class="legend">${starting.data.version===5?'6':starting.data.version===4?'8':starting.data.version===3?'4':'Up to 6'} questions in this area. ${result.questionInSection-1} answered here.</p>`:`<progress class="starting-progress" max="10" value="${index}" aria-label="Questions answered">${index} of 10</progress>`}<div id="starting-copy">${q.scene?`<p class="starting-scene"><span class="question-kicker">THE SITUATION</span>${html(q.scene)}</p>`:''}${visual}${visual?'<p class="model-key">Each dot is one item.</p>':''}<h2 class="question-focus"><span class="question-kicker">YOUR QUESTION</span>${html(q.prompt)}</h2>${q.kind==='number'?`<label class="field"><span>${esc(q.answerLabel||'Your answer')}</span><input type="text" name="starting-answer" inputmode="decimal" maxlength="80" autocomplete="off" value="${esc(value??'')}" aria-describedby="starting-number-help"></label><p class="legend" id="starting-number-help">A number, decimal or fraction is fine.</p>`:`<p class="legend">Choose the answer that fits best.</p><div class="starting-options">${order.map(i=>`<label class="option"><input type="radio" name="starting-answer" value="${i}" ${value===i?'checked':''}><span>${html(q.options[i])}</span></label>`).join('')}</div>`}</div><button class="read-button" data-action="starting-read">▷ Read this question aloud</button><div class="buttons"><button class="btn" data-action="starting-answer" ${value===null||value===''?'disabled':''}>Next question →</button><button class="btn secondary" data-action="starting-unsure">I don’t know yet</button></div>${startingSaveMarkup()}`;
  }
  updateStartingStatus();
  
}
function startingSaveMarkup(){return '<div data-starting-save></div><p class="error-text" id="starting-error" role="alert"></p>';}
function updateStartingStatus(){
  const el=$('[data-starting-save]');if(!el)return;
  el.innerHTML=starting?._conflict?'<p class="notice">This check changed on another device. Load that copy before answering more.</p><button class="btn secondary" data-action="starting-reload">Load the check saved on my account</button>':starting?._error?'<p class="error-text">'+esc(starting._error)+'</p>':'';
  if(starting?._conflict)$('#welcome-flow')?.querySelectorAll('input,textarea,select,[data-action=starting-answer],[data-action=starting-unsure],[data-action=starting-write],[data-action=starting-skip-writing]').forEach(x=>x.disabled=true);
}
function startingAreaName(id){return starting?.data?.version>=4?sub(id).name:({math:'Math',reading:'Reading',writing:'Writing',science:'Science',social:'Communication',digital:'Digital skills'}[id]||sub(id).name);}
function startingAreaNote(area,subject){return subject==='writing'?'Your writing in lessons needs a human review.':area?.basis==='support'?'Start with a worked example.':area?.basis==='check-in'?'Try this lesson to check the fit.':'Build from what you showed here.';}
function startingSummary(){
  const result=startResult();if(!result?.complete)return '';
  return `<section class="starting-summary"><div><p class="eyebrow">YOUR STARTING POINT IS READY</p><h2>Your starting suggestions</h2><p>${starting.data.version>=2?'Each area has its own suggestion. Your first lessons will help us check the fit.':'These suggestions came from the earlier short check. Digital skills, Life skills and Work & jobs begin with their first module.'} You can review earlier modules. Later modules unlock as you pass each check.</p></div><details><summary>My suggested modules</summary><div class="starting-subjects">${catalog.subjects.map(s=>`<a href="#path/${s.id}"><strong>${esc(s.name)}</strong><span>${esc(suggestedStart(catalog,s.id,result)?.title||s.name)}</span>${result.areas?`<small>${startingAreaNote(result.areas[s.id],s.id)}</small>`:''}</a>`).join('')}</div><p class="legend">This is a starting suggestion, not a test score. Practice, explanations, and mentor feedback help you decide what to try next.</p>${starting._dirty?`<p class="legend">Saved on this device. ${esc(starting._error||'Your mentor will receive it when connected.')}</p>`:''}${starting._conflict?'<button class="text-link" data-action="starting-reload">Load the check saved on my account</button>':''}<button class="text-link" data-action="starting-retry">Check my starting point again</button></details></section>`;
}
async function syncStarting(){
  // A submitted answer may arrive while its unfinished input is still saving.
  // Drain that save, then send the current record before leaving the question.
  if(startingFlight){await startingFlight;return syncStarting();}
  if(!me||!starting?._dirty||starting._conflict)return;
  const owner=me.id,record=starting,content=JSON.stringify(record.data);
  startingFlight=(async()=>{
    try{
      const result=await api('/api/starting-point',{learner:owner,revision:record.revision||0,data:record.data});
      if(me?.id!==owner||starting!==record)return;
      record.revision=result.revision;record.result=result.result;record.updated=result.updated;
      record._dirty=JSON.stringify(record.data)!==content;delete record._error;
      me.startingPoint=result;saveStarting();rememberMe();if(result.result.complete)await refreshAccount();
    }catch(e){if(me?.id===owner&&starting===record){record._error=errorText(e);record._conflict=e.status===409;saveStarting();}}
  })();
  try{await startingFlight;}finally{startingFlight=null;updateStartingStatus();}
}
function queueStarting(){starting._dirty=!!me;saveStarting();clearTimeout(startingTimer);if(me)startingTimer=setTimeout(()=>syncStarting(),650);}
function saveStartingInput(heard=false){
  if(!starting?.data||starting._conflict)return;
  if(starting.data.version<2){if(heard){starting.heard=true;saveStarting();}return;}
  const r=startResult();
  if(r.next){
    const q=startingQuestion(startingBank,starting.data,r.next),input=q.kind==='number'?$('input[name=starting-answer]'):$('input[name=starting-answer]:checked');
    starting.data.draft={id:q.id,answer:input?(q.kind==='number'?input.value:Number(input.value)):null,heard:heard||starting.data.draft?.heard||false};
  }else if(r.questionsDone&&!r.complete){
    starting.data.writing={text:$('[name=starting-writing]')?.value||'',status:'draft',support:$('[name=starting-support]')?.value||'myself',heard:heard||starting.data.writing?.heard||false};
  }
  queueStarting();
}
async function answerStarting(unsure){
  if(starting?._conflict)return;
  const q=startingQuestion(startingBank,starting.data,startResult()?.next);if(!q)return;
  const selected=q.kind==='number'?$('input[name=starting-answer]'):$('input[name=starting-answer]:checked');
  if(!unsure&&(!selected||!selected.value.trim()))return;
  if(!unsure&&q.kind==='number'&&numberValue(selected.value)===null){$('#starting-error').textContent='Try a number, decimal or fraction, or choose “I don’t know yet”.';selected.focus();return;}
  const record=starting;
  starting.data.answers.push({id:q.id,answer:unsure?(starting.data.version>=2?null:-1):q.kind==='number'?selected.value:Number(selected.value),heard:!!(starting.data.draft?.heard||starting.heard)});
  delete starting.data.draft;delete starting.heard;starting._dirty=!!me;saveStarting();
  $('#welcome-flow').querySelectorAll('input,button,textarea,select').forEach(el=>el.disabled=true);
  reader.stop();await syncStarting();
  if(route==='home'&&starting===record){tutorial.questionsComplete();readRoute();animateView('home/'+starting.data.answers.length);root.focus({preventScroll:true});window.scrollTo(0,0);}
}
async function finishStartingWriting(skip){
  if(starting?._conflict)return;
  saveStartingInput();const record=starting,w=record.data.writing;
  if(!skip&&!w.text.trim()){$('#starting-error').textContent='Write a short message, or choose “Not ready to write yet”.';$('[name=starting-writing]').focus();return;}
  w.status=skip?'skipped':'submitted';queueStarting();
  $('#welcome-flow').querySelectorAll('input,button,textarea,select').forEach(el=>el.disabled=true);
  reader.stop();await syncStarting();
  if(route==='home'&&starting===record){tutorial.questionsComplete();readRoute();root.focus({preventScroll:true});window.scrollTo(0,0);}
}
function mentorStarting(l){
  const p=l.startingPoint;if(!p)return '<p class="legend">Starting check not taken yet.</p>';
  const r=p.result,w=p.data.writing,v2=p.data.version>=2;
  return `<details class="mentor-starting" data-mentor-disclosure="starting-${esc(l.id)}"><summary>${r.complete?'Suggested starting modules':'Starting check: '+p.data.answers.length+(v2?' answered':' of 10 answered')}</summary><p class="small">Age ${p.data.age} · ${formatDate(p.updated)} · informal starting suggestions, separate from completed modules.</p>${r.areas?`<div class="starting-subjects">${Object.entries(r.areas).map(([s,a])=>`<div><strong>${esc(p.data.version===4?sub(s).name:({reading:'Reading',writing:'Writing',social:'Communication'}[s]||sub(s).name))}</strong><span>${esc(unit(r.suggestions?.[s]||s+'-'+a.level)?.title||'Begin with the first module')}</span><small>${a.matched} of ${a.answered} matched · ${a.unsure} not sure · ${a.heard} read aloud</small><small>${startingAreaNote(a,s)}</small></div>`).join('')}</div><p class="legend">These are starting suggestions. A short starting check cannot establish independent ability across a whole course. Discuss the first lesson and review the learner’s own work. Listening does not lower a suggestion.</p>`:r.complete?`<p class="small">${catalog.subjects.map(s=>esc(s.name)+': '+esc(suggestedStart(catalog,s.id,r)?.title||s.name)).join(' · ')}</p>`:''}${[2,4].includes(p.data.version)?`<section class="starting-writing-review"><h3>Short message · ${w?.status==='submitted'?'ready for your review':w?.status==='skipped'?'learner chose to try later':w?.text?'draft in progress':'not submitted yet'}</h3><p>${esc(startingBank.writing.prompt)}</p>${w?.text?`<blockquote>${esc(w.text)}</blockquote><p class="small">Help: ${esc({myself:'Wrote it myself',person:'A person',tool:'A tool',mixed:'A person and a tool'}[w.support])}${w.heard?' · Task read aloud':''}</p>`:''}<p class="legend">No automatic writing grade. Discuss the learner’s own writing before choosing a harder writing task.</p><ul>${startingBank.writing.review.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></section>`:''}<details data-mentor-disclosure="starting-answers-${esc(l.id)}"><summary>See the starting answers</summary>${r.evidence.map(a=>{const q=startingQuestion(startingBank,p.data,a.id);return `<p class="small">${q.scene?html(q.scene)+'<br>':''}${html(q.prompt)}<br>Answer: ${a.answer===-1||a.answer===null?'Not sure yet':q.kind==='number'?esc(a.answer):html(q.options[a.answer])} · ${a.correct?'Matched':'Revisit'}${a.heard?' · Read aloud used':''}</p>`;}).join('')}</details></details>`;
}


function suggestedModule(sid){return nextFoundationUnit({catalog,plan:currentFoundation(),local,done:passed(),starting:startResult(),subject:sid});}
function pathView(){
  const s=sub(subject),done=passed(),next=suggestedModule(subject),all=activeUnits(catalog,subject);
  root.innerHTML=`<div class="page-head"><h1>Your modules</h1></div><nav class="filters" aria-label="Choose a subject">${catalog.subjects.map(s=>`<a href="#path/${s.id}" class="filter world-${s.id} ${subject===s.id?'active':''}" ${subject===s.id?'aria-current="page"':''}>${esc(s.name)}</a>`).join('')}</nav><div class="module-heading"><div><h2>${esc(s.name)}</h2><p>${esc(s.short)}</p></div><span class="pill">${all.filter(u=>done.has(u.id)).length} of 24 completed</span></div>${courseGateMarkup(catalog,done,subject)}<div class="path-groups"><div class="path-grid">${all.map(u=>unitCard(u,done,next?.id)).join('')}</div></div>`;
}
function unitCard(u,done,nextId){
  const completed=done.has(u.id),active=local[u.id]?.phase>0&&local[u.id]?.phase<7,access=moduleAccess({catalog,unit:u,done,local,starting:startResult(),plan:currentFoundation()}),suggested=access.allowed&&(active||!completed)&&u.id===nextId;
  const state=!access.allowed?'Locked':active?(completed?'Revisiting':'In progress'):completed?'✓ Completed':suggested?'Suggested next':'';
  return `${u.seriesStart?'<h3 class="path-series-heading">AI skills</h3>':''}<article class="card path-unit world-${u.subject} ${!access.allowed?'locked-module':suggested?'recommended-module':''}"><div class="module-card-heading"><h3>${esc(u.title)}</h3><div class="module-meta">${state?'<span class="pill '+(completed?'ready':'')+'">'+state+'</span>':''}</div></div><div class="module-body"><p>${esc(u.why)}</p>${u.foodReplay?'<p class="food-review-label">Food review · pass again to earn a portion, once every 24 hours.</p>':''}</div><div class="module-controls">${access.allowed?startButton(u.id,active?'Continue':completed?'Revisit':'Start','small '+(suggested?'':'secondary'),completed&&!active):`<p class="module-unlock">${access.reason==='core-courses'?'Finish the first four courses to unlock.':'Pass <strong>'+esc(access.previous?.title||'the previous module')+'</strong> to unlock.'}</p>`}</div></article>`;
}
function readButton(id,label='Read aloud'){return `<button class="read-button" data-action="read" data-target="${id}" aria-label="${esc(label==='Read aloud'?'Read this section aloud':label)}">▷ ${esc(label)}</button>`;}
function lessonView(){reader.stop();lessonExample?.dispose();lessonExample=null;checkpointStop();missionTransition.cancel();const u=unit(lessonId),d=draft(),phase=d.phase||0,s=sub(u.subject);root.innerHTML=`<div class="lesson-top"><a href="#path/${u.subject}">← ${esc(s.name)}</a></div>${missionHeader(u,phase,Boolean(d.result?.passed))}<div id="lesson-body" class="mission-content"></div><p class="draft-status" id="draft-status" role="status"></p>${lessonSourceFooter(u,resources(u))}`;
  const body=$('#lesson-body');if(phase===0){body.innerHTML=missionIntro(u,readButton,html);lessonExample=mountLessonVisual(body.querySelector('[data-lesson-visual]'),u,html,motionAllowed);}
  else if(phase===1||phase===3){body.innerHTML=missionLesson(u,phase,html,readButton,{returnToPractice:d.exampleReturnPhase===phase+1});mountMissionLab({u,host:$('#mission-lab'),phase,draft:d,save:persist,html,readButton,onEdit:cancelMissionAdvance,onCorrect:scheduleMissionAdvance});if(d.examplePhase===phase)showMissionPane(root,true);}
  else if(phase===2||phase===4){const round=practiceRound(u,phase,d);if(!round.questions.length){d.phase=phase+1;persist();lessonView();return;}const solved=round.questions.filter(q=>round.checks[q.id]).length;body.innerHTML=missionPractice(u,round,questionCard,html);persist();}
  else if(phase===5){body.innerHTML=`<section class="card lesson-copy" id="review-copy">${reflectionMarkup(u,d.reflection,html)}${readButton('reflection-task')}<details class="reflection-help"><summary>Review an example if you need help</summary><ul class="review-list" id="review-examples">${u.review.map(p=>`<li>${html(p)}</li>`).join('')}</ul>${readButton('review-examples')}</details><p class="legend">${(u.domain||u.subject)==='writing'?'Use your own words to complete the writing task above. Your mentor reviews meaning and clarity; the quiz checks the lesson ideas separately.':'Use your own words. You can add a drawing to show your thinking; spelling is not graded here.'}</p>${inkPad(d)}<div class="notice">${me?(me.personal?'Your work is saved in My learning, separately from the learners you support.':'Your completed check, explanation, support choice, and drawing are shared with your mentor automatically. Practice retries are labelled as device-reported.'):'You are trying a preview. Join your mentor to save checks across devices, send reports, and earn Steps.'}</div><div class="buttons">${button(me?'Start my six-question check':'Try a preview check','start-check')}</div><p class="error-text" id="lesson-error" role="alert"></p></section>`;setupInk(d);}
  else if(phase===6){const attempt=d.attempt;if(!attempt){d.phase=5;persist();lessonView();return;}body.innerHTML=`<div class="notice">${me?(me.personal?'This check stays in your personal learning record.':'Your mentor will see this check.'):'On this device: no report is sent.'} Take your time. You can use the drawing space and explain any support you used.</div>${attempt.questions.map((q,i)=>questionCard(q,i,attempt,true)).join('')}<section class="card">${reflectionMarkup(u,d.reflection,html)}<label class="field"><span>How did you complete this check?</span><select data-draft="support">${[['myself','I worked on my own'],['person','Someone helped me'],['tool','I used notes, an example or a tool'],['mixed','I used more than one kind of help']].map(([v,t])=>`<option value="${v}" ${d.support===v?'selected':''}>${t}</option>`).join('')}</select></label>${inkPad(d)}<p class="error-text" id="lesson-error" role="alert"></p><div class="buttons">${button(me?(me.personal?'Finish & save my check':'Finish & share with my mentor'):'Check my preview answers','finish')}</div></section>`;setupInk(d);}
  else resultView(u,d,body);
  if(u.deviceTask&&(phase===5||phase===7))body.insertAdjacentHTML('beforeend',devicePanel(u,me));
  if(u.projectWorkshop&&(phase===5||phase===7)){body.insertAdjacentHTML(phase===5?'afterbegin':'beforeend',projectMarkup(me));mountProject($('#project-workshop'),{me,api,updated:fresh=>{if(me?.id===fresh.id){const explanation=fresh.project?.data?.explanation;if(explanation&&(!d.reflection||d.reflection===me.project?.data?.explanation||d.reflection===d.scenarioLab?.[3]?.tasks?.['project-test-note']?.text)){d.reflection=explanation;const input=$('[data-draft=reflection]');if(input)input.value=explanation;persist();}me=fresh;rememberMe();}}});}if(lessonId==='digital-8'&&phase===7)body.insertAdjacentHTML('beforeend','<section class="card"><h2>Make your next useful tool</h2><p>Use a phone or PC to build and keep a small app. A paid AI account is optional.</p><a class="btn" href="#lesson/app-build">Build an app you can use</a></section>');status();animateView(`lesson/${lessonId}/${phase}/${d.rounds?.[phase]?.cursor??d.scenarioLab?.[phase]?.cursor??d.messageLab?.[phase]?.cursor??0}`);}
function questionCard(q,i,round,isTest){const value=round.answers?.[q.id]??'',checked=round.checks?.[q.id],hint=round.hints?.[q.id];return `<section class="question ${checked?'correct':''}" data-question="${esc(q.id)}" id="q-${i}"><div class="q-label"><span class="eyebrow">QUESTION ${i+1}</span>${readButton('q-'+i)}</div>${q.passage?`<blockquote class="question-passage">${html(q.passage)}</blockquote>`:''}<p class="prompt question-focus">${html(q.prompt)}</p>${q.kind==='choice'?`<div role="group" aria-label="Answer for question ${i+1}">${q.options.map(o=>`<label class="option"><input type="radio" name="q-${esc(q.id)}" value="${esc(o.id)}" data-answer="${esc(q.id)}" ${value===o.id?'checked':''}><span>${html(o.text)}</span></label>`).join('')}</div>`:`<label class="field"><span>Your answer</span><input type="text" inputmode="${unit(lessonId)?.mission?.kind==='order'?'numeric':'text'}" autocomplete="off" data-answer="${esc(q.id)}" value="${esc(value)}" maxlength="120" aria-label="Answer for question ${i+1}"></label>`}${!isTest?`<div class="buttons">${button('Check my answer','check',`data-q="${q.id}"`,'small')}${button('Show help','hint',`data-q="${q.id}"`,'small secondary')}</div>${hint&&!checked?`<p class="hint"><strong>Common pitfall</strong> ${esc(commonPitfall(unit(lessonId),q))}</p>`:''}<p class="feedback" role="status">${round.last?.[q.id]!==undefined?(checked?(isMission(unit(lessonId))?'':'✓ That fits. ')+html(q.explanation):"That does not fit yet. "+esc(commonPitfall(unit(lessonId),q))):''}</p>`:''}</section>`;}
function resultView(u,d,body){const queued=pending.find(p=>p.unit===u.id);if(queued&&!d.result){const [title,text]=queued.rejected?['This check can no longer be sent.','The app no longer has this check open, for example after records were restored. Start a fresh check. Your lesson work is still here.']:queued.problem?['Your report was not accepted yet.','Your answers are saved on this device. Try again. If the same message returns, show it to your mentor.']:['Your report is waiting to send.','It will send automatically when this app reconnects. Keep your sign-in on this device until you see a receipt.'];body.innerHTML=`<section class="result"><span class="eyebrow">SAVED ON THIS DEVICE</span><h2>${title}</h2><p>${text}</p>${queued.rejected?button('Start a fresh check','restart-check',`data-id="${esc(queued.id)}"`):button('Try sending now','sync')}<div class="buttons"><a class="btn secondary" href="#home">Back home</a></div><p class="error-text" role="alert">${esc(queued.error||'')}</p></section>`;return;}
 const reward=checkpointCompletion({unit:u.id,local,me,unlocks:profileUnlocks()}),celebration=checkpointQueue.peek(me?.id||guestScope,u.id),r=d.result,next=nextCourseUnit({catalog,unit:u,done:passed(),local,starting:startResult(),plan:currentFoundation()})||nextFoundationUnit({catalog,plan:currentFoundation(),local,done:passed(),starting:startResult(),subject:u.subject});if(!r){d.phase=5;lessonView();return;}body.innerHTML=`<section class="result"><span class="eyebrow">${d.preview?'PRACTICE PREVIEW':r.passed?'A STEP FORWARD':'KEEP BUILDING'}</span><div class="score">${r.score}<span class="muted"> / 6</span></div><h2>${r.passed?'Checkpoint passed.':'You have a useful next step.'}</h2><p>${r.passed?'You worked through this module and passed its check. Choose another module when you’re ready, or take a break here.':'You finished the check. It takes 5 of 6 correct to complete this module. Use the explanations below to pick one thing to practise, then try again.'}</p><p>${d.preview?'This preview stays on this device. Join your mentor to keep a shared record.':`${me?.personal?'✓ Saved to your own learning record.':'✓ Report received by your mentor’s inbox.'} <strong class="points-value">${r.points} Steps earned.</strong>`}</p>${r.passed?checkpointMarkup({completion:reward,profile:currentProfile(),fresh:!!celebration?.newCompletion,food:currentFood(),award:r}):''}<div class="buttons">${r.passed?'':button('Go over the lesson','again','','secondary')}${r.passed?(next?`<a class="btn" href="#lesson/${next.id}">Next module: ${esc(next.title)} →</a>`:'<a class="btn" href="#progress">View my wins →</a>'):button('Try a new check','start-check')}<a class="text-link" href="#home">Done for now</a></div></section><section class="card" style="margin-top:20px"><h2>See why each answer works</h2>${r.questions.map((q,i)=>`<details class="result-details"><summary>${q.correct?'✓':'↻'} Question ${i+1} · ${q.correct?'Understood':'Worth another look'}</summary>${q.passage?`<blockquote class="question-passage">${html(q.passage)}</blockquote>`:''}<p>${html(q.prompt)}</p><p>${html(q.explanation)}</p></details>`).join('')}</section>`;const event=checkpointQueue.take(me?.id||guestScope,u.id);if(event){companion.celebrate();checkpointStop=celebrateCheckpoint(body.querySelector('[data-checkpoint-reward]'),motionAllowed,()=>canPipPlay(currentFood()));}}
function sourceDate(value){return value?new Date(value+'T12:00:00Z').toLocaleDateString('en-CA',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}):'Check the current page';}
function sourceLink(r){return `<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.title)} ↗</a><small>${esc(new URL(r.url).hostname)} · checked ${esc(sourceDate(r.checked))}</small>`;}
function resources(u){
 const links=(u.resources||[]).filter(r=>r.url.startsWith('https://'));if(!links.length)return '';
 if(u.guide?.learningOnly)return `<details class="lesson-resources"><summary>Official guidance</summary><ul>${links.map(r=>`<li>${sourceLink(r)}</li>`).join('')}</ul></details>`;
 return `<details class="lesson-resources" ${u.guide?'open':''}><summary>${u.guide?'Use this in real life':'Helpful official websites'}</summary>${u.guide?`<p class="legend">${esc(u.guide.region)} · guide checked ${esc(sourceDate(u.guide.checked))}. Current official instructions take priority.</p><ol>${u.guide.steps.map(step=>`<li>${esc(step)}</li>`).join('')}</ol><p class="legend">No quiz pass is needed to use these links. ${u.deviceTask?'The lesson does not change your device.':u.course==='typing'?'Use a disposable practice note for the real keyboard steps.':'Stepstone does not submit an application.'}</p>`:''}<p class="legend">Opens another website in a new tab; internet needed. No outside account is needed for this practice lesson.</p><ul>${links.map(r=>`<li>${sourceLink(r)}</li>`).join('')}</ul></details>`;
}
function serviceHelp(){
 const guides=catalog?.units.filter(u=>u.guide&&!u.course)||[];if(!guides.length)return '';
 const seen=new Set(),help=guides.map(u=>u.resources.find(r=>r.help)).filter(r=>r&&!seen.has(r.url)&&seen.add(r.url));
 // Urgent help comes first. Checked against 988.ca and kidshelpphone.ca on 2026-09-27.
 const urgent=`<p class="notice"><strong>Urgent help:</strong> if you are in danger, call 9-1-1. For thoughts of suicide or a mental-health crisis, call or text 9-8-8, any time. Young people can also call Kids Help Phone at 1-800-668-6868 or text CONNECT to 686868.</p><ul>${[{title:'9-8-8: Suicide Crisis Helpline',url:'https://988.ca/',checked:'2026-09-27'},{title:'Kids Help Phone',url:'https://kidshelpphone.ca/',checked:'2026-09-27'}].map(r=>`<li>${sourceLink(r)}</li>`).join('')}</ul>`;
 return `<details class="lesson-resources service-help"><summary>Need help with a real service?</summary>${urgent}<p class="legend">These official services and guides are available before any lesson or quiz. They open another website; internet is needed. Keep document numbers out of Stepstone.</p><ul>${help.map(r=>`<li>${sourceLink(r)}</li>`).join('')}</ul></details>`;
}
function inkPad(d){return `<details class="ink-wrap"><summary>Show your working</summary><p class="legend">Use a finger, pen or mouse to show your reasoning. Your drawing is included with the completed check.</p><canvas class="ink" id="ink-pad" width="960" height="440" aria-label="Drawing space for working"></canvas><div class="ink-actions"><button data-action="ink-undo">Undo stroke</button><button data-action="ink-clear">Clear drawing</button></div></details>`;}
function paintInk(canvas,ink){const ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);ctx.strokeStyle='#183c44';ctx.lineWidth=3;ctx.lineCap='round';ctx.lineJoin='round';for(const stroke of ink){if(!stroke.length)continue;ctx.beginPath();ctx.moveTo(stroke[0][0]*canvas.width,stroke[0][1]*canvas.height);for(const p of stroke)ctx.lineTo(p[0]*canvas.width,p[1]*canvas.height);if(stroke.length===1)ctx.lineTo(stroke[0][0]*canvas.width+.2,stroke[0][1]*canvas.height+.2);ctx.stroke();}}
function setupInk(d){const c=$('#ink-pad');if(!c)return;d.ink??=[];paintInk(c,d.ink);let active=null,stroke=null;const pt=e=>{const r=c.getBoundingClientRect();return [Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))].map(v=>Math.round(v*1000)/1000);};c.addEventListener('pointerdown',e=>{if(active!==null||d.ink.length>=100||d.ink.reduce((n,s)=>n+s.length,0)>=5900)return;e.preventDefault();active=e.pointerId;c.setPointerCapture(active);stroke=[pt(e)];d.ink.push(stroke);paintInk(c,d.ink);});c.addEventListener('pointermove',e=>{if(active!==e.pointerId||stroke.length>=300||d.ink.reduce((n,s)=>n+s.length,0)>=6000)return;const p=pt(e),last=stroke.at(-1);if(Math.hypot(p[0]-last[0],p[1]-last[1])>.004){stroke.push(p);paintInk(c,d.ink);}});const end=e=>{if(active===e.pointerId){active=null;persist();}};c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);}
function progressView(){
  const disclosureKey=d=>d.dataset.disclosureKey||d.querySelector('summary')?.textContent.trim().replace(/\d+/g,'#');
  const openSections=new Set([...root.querySelectorAll('.learning-hub details[open]')].map(disclosureKey));
  root.innerHTML=learningHubMarkup({points:me?.points??tutorial.bonus(),preview:!me,guide:tutorial.visible(),
    wins:learningRecordContent(),rewards:rewardsContent()});
  for(const d of root.querySelectorAll('.learning-hub details'))if(openSections.has(disclosureKey(d)))d.open=true;
}
function learningRecordContent(){
  const reports=[...(me?.attempts||Object.entries(local).filter(([,d])=>d.result).map(([unit,d])=>({unit,report:{...d.result,title:catalog.units.find(u=>u.id===unit)?.title||unit,tryNumber:1},finished:d.result.at||d.touchedAt/1000||Date.now()/1000})))].sort((a,b)=>Number(b.finished||0)-Number(a.finished||0)),due=me?reviewDue(reports):[];
  const unlocks=profileUnlocks(),completions=me?(me.moduleWins||firstPasses(reports,unlocks)):previewCompletions(local,unlocks);
  const records=winsMarkup({catalog,reports,completions,unlocks,connected:!!me,personal:!!me?.personal,formatDate,typingReport});
  return `${pending.length?`<div class="notice warning">${pending.length} completed ${pending.length===1?'report is':'reports are'} waiting to send. ${button('Try now','sync','','small secondary')}</div>`:''}${due.length?`<details class="skills-review"><summary>Skills to revisit (${due.length})</summary>${due.slice(0,4).map(a=>`<div class="report-row"><div class="grow"><h3>${esc(unit(a.unit)?.title)}</h3><p>${a.report.passed?'Revisit after a break.':'Review the parts you found difficult, then try another check.'}</p></div>${startButton(a.unit,'Review','small secondary')}</div>`).join('')}</details>`:''}${records}${me?.deviceWork?.length?`<details class="lesson-resources"><summary>My real-device work</summary>${catalog.units.filter(u=>me.deviceWork.some(r=>r.unit===u.id)).map(u=>devicePanel(u,me)).join('')}</details>`:''}`;
}
function rewardCard(r){
 if(r.kind==='theme')return `<article class="card reward-card"><h3>${esc(r.title)}</h3><p>Free. Choose colours that feel good to you.</p>${button('Use these colours','theme',`data-theme="${r.id.replace('theme-','')}"`,'secondary')}</article>`;
 const c=me?.claims.find(c=>r.milestone?c.id===r.claim_id:c.reward===r.id),isGoal=me?.goal===r.id,e=rewardEligibility(r,me);
 const previous=r.milestone&&!r.allocation?me?.claims.find(c=>c.reward===r.id&&c.status==='declined'):null;
 return `<article class="card reward-card ${isGoal?'chosen-goal':''}"><span class="eyebrow">${isGoal?'MY GOAL':r.milestone?'YOUR PATH MILESTONE':'AGREED WITH YOUR MENTOR'}</span><h3>${esc(r.title)}</h3><p>${esc(r.description)}</p><span class="pill ${r.cost?'points-value':''}">${r.cost?r.cost+' Steps':'No Steps to spend'}</span>${c?`<p><strong>${{pending:'Request sent — your mentor will reply',approved:'Approved — arrange with your mentor',given:'Reward given',declined:'Cancelled — Steps returned'}[c.status]}</strong></p>${c.note?`<p class="notice">${esc(c.note)}</p>`:''}`:`${previous?'<p class="notice">Earlier request cancelled. Your Steps returned. '+esc(previous.note)+'</p>':''}${requirements(r,me,catalog)}<p class="legend">${e.remaining?`${e.remaining} more Steps to request it`:e.ready?'You have met the app requirements.':r.cost?'Your Steps are ready. Check the remaining requirements above.':!e.missing.length?'Your skills are ready. Your mentor can confirm your account and arrange the laptop.':'Keep building the skills above. There is no Steps to spend.'}</p><div class="buttons">${!isGoal?button('Make this my goal','reward-goal',`data-id="${r.id}"`,'secondary'):''}${button('Request reward','reward',`data-id="${r.id}" data-allocation="${r.allocation||''}" ${!e.ready?'disabled':''}`)}</div>`}</article>`;
}
function rewardsContent(){
  const rewards=me?.rewards||[],real=rewards.filter(r=>r.kind==='mentor'&&(!r.id.startsWith('core-card-')||me?.claims.some(c=>c.reward===r.id))).sort((a,b)=>Number(b.id===me?.goal)-Number(a.id===me?.goal));
  const cards=cardExchange(me,catalog),cardGoal=me?.goal==='card-exchange',primary=real.find(r=>r.id===me?.goal)||(!cardGoal?real[0]:null),others=real.filter(r=>r!==primary);
  const empty=!cards&&!real.length?`<section class="card reward-empty"><div class="reward-illustration" aria-hidden="true">${icon('rewards')}</div><div class="reward-intro"><h3>${me?.personal?'Plan learner rewards':me?'A goal to work towards':'Choose your next goal'}</h3><p>${me?.personal?'Agree on activities, project supplies or useful items for each learner.':me?'Agree on an activity, project supplies or a useful item with your mentor. Your Steps are already being saved.':'Connect with your mentor to choose a goal and see which rewards are funded.'}</p>${me?.personal?'<a class="btn" href="#mentor">Open my mentor dashboard →</a>':!me?button('Connect with my mentor →','account'):'<a class="btn secondary" href="#mentor">Open mentor space →</a>'}</div></section>`:'';
  const secondary=[cards&&primary?cards:'',...others.map(rewardCard)].filter(Boolean).join('');
  return `<div id="rewards-goals">${primary?rewardCard(primary):cards||empty}</div>${secondary?`<details class="secondary-rewards"><summary>Other reward options</summary>${secondary}</details>`:''}`;
}

let managerSection=null;
function modal(title,body,{footer='',profile=false}={}){
 const back=managerSection;delete dialog.dataset.managerPanel;reader.stop();cancelMissionAdvance();tutorial.cancel();
 dialog.classList.toggle('profile-overlay',profile);dialog.querySelector('[data-dialog-footer]')?.remove();
 $('#dialog-content').innerHTML=`<div class="dialog-head"><h2 id="dialog-title">${esc(title)}</h2><button data-action="close" aria-label="Close window">✕</button></div>${back?`<button class="btn secondary small manager-back" data-action="manager-section" data-section="${back}">← Back to ${esc({personal:'my test space',messages:'support requests',inbox:'progress inbox',learners:'learners',invites:'invitations',rewards:'rewards',settings:'settings'}[back])}</button>`:''}${body}`;
 dialog.setAttribute('aria-labelledby','dialog-title');if(!dialog.open)dialog.showModal();companion.dockIn(profile?null:dialog);
 if(footer){const bar=document.createElement('div');bar.className='dialog-footer';bar.dataset.dialogFooter='';bar.innerHTML=footer;dialog.append(bar);}
 if(profile){$('#dialog-content').scrollTop=0;dialog.scrollTop=0;}
 if(motionAllowed())$('#dialog-content').animate([{opacity:.5,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:180,easing:'ease-out'});
}
function account(){if(me){modal('Your learning account',`<p>Signed in as <strong>${esc(me.alias)}</strong>.</p>${me.personal?'<p class="notice">This is your personal learning record. Your scores, drafts, and Steps are separate from the learners’ records.</p><a class="btn secondary" href="#mentor">Back to my mentor dashboard</a>':''}<p class="notice">${me.personal?'Only your personal record is being updated. Learner reports stay in the mentor dashboard.':'Your mentor sees your finished work and can help with your next step. Other learners cannot see it.'}</p>${recovery?`<p class="field">Keep your private sign-in code. Use it on your phone or tablet to open the same account.</p><div class="invite-code">${esc(recovery)}</div>${button('Copy my sign-in code','copy-recovery','','secondary')}`:`<p class="small muted" style="margin:18px 0">${me.personal?'Open Mentor space, then choose My learning. Sign in with your mentor account on an approved device.':'This device remembers you. If you need another device or get signed out, your mentor can give you a private return link.'}</p>`}<details style="margin-top:18px"><summary>Sign in again with my private code</summary><p class="legend">If your session expired, use the same account’s code to send queued work.</p><form data-form="login"><label class="field"><span>Your private sign-in code</span><input name="code" type="password" required autocomplete="off"></label>${button('Sign in','form-submit','','secondary')}</form></details><div class="buttons">${button('Add app to this device','add-app','','secondary')}${button('Save & switch learner','logout','','secondary')}${button('Check draft sync','draft-resolve','','secondary')}${button('My starting point','starting-retry','','secondary')}</div><p class="legend">Switching saves your lesson drafts to your account first, then locks this device. Keep your private sign-in code to return.</p><p class="error-text" id="account-error" role="alert"></p>`);return;}
 modal('Connect with your mentor',`<p class="small muted">Open the private start link from your mentor. If they gave you a code instead, enter it here.</p><form data-form="join"><label class="field"><span>Pip name</span><input name="alias" value="${esc(currentProfile().alias)}" required maxlength="12" autocomplete="off"></label><label class="field"><span>Invite code from your mentor</span><input name="code" required minlength="8" autocomplete="off"></label><label class="check-label"><input name="share" type="checkbox" required><span>I understand that my completed checks, explanations, drawings, and support choices go to my mentor. Other learners cannot see them.</span></label><div class="buttons">${button('Join my mentor','form-submit','','')}</div></form><hr style="border:0;border-top:1px solid var(--line);margin:23px 0"><details><summary>Already have a private sign-in code?</summary><form data-form="login"><label class="field"><span>Your private sign-in code</span><input name="code" type="password" required autocomplete="off"></label>${button('Sign in','form-submit','','secondary')}</form></details><p class="error-text" id="account-error" role="alert"></p>`);}
function readingControls(){
 return `<fieldset class="profile-reading" id="profile-comfort" data-profile-panel="reading"><legend id="comfort-control">Reading & comfort</legend><label class="toggle-row"><input type="checkbox" data-setting="quiet" ${settings.quiet?'checked':''}><strong>Quiet visuals</strong></label><label class="field"><span>Reading voice</span><select id="voice-choice" data-voice-choice>${voiceOptions(settings.voice||'soft',health.softVoice!==false)}</select></label><div class="buttons"><button class="btn secondary" type="button" data-action="voice-sample">Try voice</button><button class="btn secondary" type="button" data-action="stop-reading">Stop reading</button></div></fieldset>`;
}
async function mentorSignedIn(){setEntryRole('mentor');me=null;lastInvite=null;inbox.clear(true);localStorage.removeItem('stepstone-session-preview-v1');loadLocal();await loadMentor();nav();companion.update();}
async function loadMentor(){
 const refresh=++mentorRefresh;
 let nextHealth=health,nextMentor=null,nextPending=null,refreshError=null,resumedDevice=false;
 try{
   nextHealth=await api('/api/health');
   try{nextMentor=await api('/api/mentor');}catch(error){if(error.status!==401)throw error;const pending=await api('/api/mentor/device-status',{}).catch(()=>null);if(pending?.pending)nextPending=pending;else if(pending?.ok){nextMentor=await api('/api/mentor');resumedDevice=true;}else throw error;}
 }catch(e){refreshError=e;}
 // A sign-in, mode change or newer refresh supersedes this response.
 if(refresh!==mentorRefresh||entryRole!=='mentor')return;
 health=nextHealth;mentor=nextMentor;devicePending=nextPending;
 if(refreshError){lastInvite=null;if(![401,403].includes(refreshError.status))toast(errorText(refreshError));}
 if(mentor&&resumedDevice){me=null;localStorage.removeItem('stepstone-session-preview-v1');}
 if(route!=='mentor'||entryRole!=='mentor')return;
 // Preserve the report being read even if it was opened while a refresh was in flight.
 const open=new Set([...root.querySelectorAll('[data-mentor-disclosure][open]')].map(el=>el.dataset.mentorDisclosure));
 const scrollY=window.scrollY,focused=document.activeElement,focusSection=focused?.closest('[id^=manager-]')?.id,focusAction=focused?.dataset.action;
 mentorView();
 if(dialog.open&&dialog.dataset.managerPanel&&mentor)openManagerSection(dialog.dataset.managerPanel);
 root.querySelectorAll('[data-mentor-disclosure]').forEach(el=>el.open=open.has(el.dataset.mentorDisclosure));
 if(focusAction)(document.getElementById(focusSection)||root).querySelector(`[data-action="${CSS.escape(focusAction)}"]`)?.focus({preventScroll:true});
 else if(focusSection)document.getElementById(focusSection)?.focus({preventScroll:true});
 window.scrollTo({top:scrollY,behavior:'instant'});
}
let mentorAuthMode='login',devicePending=null,mentorRefresh=0;
function mentorView(){status();if(!mentor){if(refreshMentorAccess(root,mentorAuthMode,health,devicePending))return;root.innerHTML=spaceGuide('mentor','I’ll guide you through setting up your account and inviting learners.')+mentorAccess(mentorAuthMode,health,devicePending)+'<div class="buttons hub-footer"><button class="btn secondary" data-action="choose-role" data-role="learner">Use learner space</button></div>';return;}
 root.innerHTML=`<div class="page-head manager-heading"><div><p class="eyebrow">PRIVATE MENTOR SPACE</p><h1>${esc(mentor.account?.name||'Your dashboard')}</h1><p>Manage your learners and their next steps.</p></div><div class="buttons">${button('My learning','personal-learning','','secondary')}${button('Sign out','mentor-logout','','small secondary')}</div></div>${managerNavigation(mentor)}`;
}
function managerPanelContent(section){
  switch(section){
    case 'personal':return personalLearningTools();
    case 'messages':return messageInbox(mentor.messages,mentor.learners);
    case 'inbox':return `<section class="manager-list" id="manager-inbox" tabindex="-1"><div class="section-title">${button('Refresh','mentor-refresh','','small secondary')}</div><p class="legend">Scores are app-checked. Explanations, drawings, and self-reported support give you context. Confirm understanding in a brief conversation; no AI-use judgement is made.</p>${mentor.reports.length?mentor.reports.map(r=>`<div class="report-row"><div class="grow"><h3>${esc(r.alias)} · ${esc(r.report.title)}</h3><p>${formatDate(r.finished)} · ${r.report.score}/6 · Try ${r.report.tryNumber} · ${r.reviewed?'Reviewed':'New report'}</p></div>${button('Review','review-report',`data-id="${r.id}"`,'small secondary')}</div>`).join(''):'<p class="empty">No learner reports yet. Create an invite, let a learner complete a check, and their work will appear here.</p>'}</section>`;
    case 'learners':return `<section class="manager-list" id="manager-learners" tabindex="-1">${mentor.learners.map(l=>`<div class="report-row"><div class="grow"><div class="signal-identity">${avatar(l.profile?.avatar||'fox',44)}<h3>${esc(l.alias)}</h3></div><p>${l.passed} ${l.passed===1?'skill':'skills'} passed · <span class="points-value">${l.points} Steps available</span></p><p class="small">${(mentor.funding?.people||[]).some(p=>p.learner===l.id&&p.primary_learner===l.id)?'Person confirmed · main reward account':(mentor.funding?.people||[]).some(p=>p.learner===l.id)?'Linked extra account · learning kept':'Person confirmation needed before funding'}</p>${tutorial.mentor(l)}${mentorFoundation(l.foundation,l.id)}${mentorDevice(l,catalog)}${mentorProject(l)}${mentorStarting(l)}</div>${button('Person record','funded-person',`data-id="${l.id}"`,'small secondary')}${button('Set aside rewards','funded-allocate',`data-id="${l.id}"`,'small secondary')}${button('Help them sign in','recover',`data-id="${l.id}"`,'small secondary')}</div>`).join('')||'<p class="empty">A learner appears after using an invite.</p>'}</section>`;
    case 'invites':return `<section class="card" id="manager-invites" tabindex="-1"><h2>Give them their own start link</h2><p class="small muted">Create a private link for each learner. They tap it, name and choose their Pip, then try a starting check and a guided tour. Each area gets its own starting suggestion. No password or email needed. The link expires after seven days.</p><div class="buttons">${button('Create learner link','invite')}</div><div id="new-invite" aria-live="polite">${lastInvite?inviteCard(lastInvite,formatDate):''}</div></section>`;
    case 'rewards':return `<section class="card"><h2>Reward requests</h2>${mentor.claims.filter(c=>c.kind!=='theme'&&!c.reward.startsWith('theme-')).length?mentor.claims.filter(c=>!c.reward.startsWith('theme-')).map(c=>`<div class="report-row"><div class="grow"><h3>${esc(c.alias)} · ${esc(c.title)}</h3><p>${c.cost} Steps · ${esc(c.status)}</p></div>${['pending','approved'].includes(c.status)?button('Open request','claim-review',`data-id="${c.id}"`,'small secondary'):''}</div>`).join(''):'<p class="empty">Learners can request rewards you add. You decide whether and when to provide them.</p>'}</section>${fundedManager(mentor)}${aiManager(mentor,catalog)}${stockManagement(mentor.rewards)}`;
    case 'settings':return mentorDeviceSettings(mentor)+managerSettings(mentor.settings);
    default:return '';
  }
}
function openManagerSection(section){
  if(!mentor)return;
  const titles={personal:'My test space',messages:'Support requests',inbox:'Progress inbox',learners:'Learners',invites:'Invitations',rewards:'Rewards & funding',settings:'Account & settings'};
  if(!titles[section])return;
  managerSection=null;modal(titles[section],managerPanelContent(section));managerSection=section;dialog.dataset.managerPanel=section;
  dialog.classList.add('manager-overlay');mountMentorProjects(dialog,mentor,api,loadMentor);
}

function reviewReport(id){const r=mentor.reports.find(r=>r.id===id);if(!r)return;const help={myself:'Worked on their own',person:'A person helped',tool:'Used a tool or example',mixed:'Used more than one kind of help'};modal(`${r.alias} · ${r.report.title}`,`<div class="mentor-details"><span class="pill">${r.report.score}/6 · Try ${r.report.tryNumber} · ${formatDate(r.finished)}</span><p class="small" style="margin:15px 0">Support: ${help[r.report.support]}. Practice retries reported by this device: ${r.report.practiceRetries}. Neither field is independently verified.</p><h3>The learner’s explanation</h3><p class="notice">${esc(r.report.reflection)}</p>${typingReport(r.report.typingPractice)}${r.report.ink.length?'<h3>Their working</h3><canvas id="report-ink" class="ink" width="960" height="440" aria-label="Learner drawing"></canvas>':''}<h3>Answers and explanations</h3>${r.report.questions.map((q,i)=>`<details class="result-details"><summary>${q.correct?'✓':'↻'} Question ${i+1}: ${q.correct?'Correct':'Revisit'}</summary>${q.passage?`<blockquote class="question-passage">${html(q.passage)}</blockquote>`:''}<p>${html(q.prompt)}</p><p class="small">Learner answer: ${html(q.kind==='choice'?q.options.find(o=>o.id===q.answer)?.text:q.answer)}</p><p class="small">${html(q.explanation)}</p></details>`).join('')}<h3>A useful follow-up</h3><p class="small muted">Ask them to explain one step or try a similar example with a new number. Review the skill directly rather than guessing whether AI was used.</p><form data-form="review"><input name="id" type="hidden" value="${r.id}"><label class="field"><span>Encouragement or next step (visible to the learner)</span><textarea name="note" maxlength="2000" placeholder="You explained… well. Next, try…">${esc(r.note)}</textarea></label>${button('Save note & mark reviewed','form-submit')}</form><p class="error-text" id="modal-error" role="alert"></p></div>`);if(r.report.ink.length)paintInk($('#report-ink'),r.report.ink);}
function claimReview(id){const c=mentor.claims.find(c=>c.id===id);if(c.card_exchange){modal('Review gift-card request',cardClaimForm(c,mentor.giftCardProviders)+'<p class="error-text" id="modal-error" role="alert"></p>');return;}if(c.funded){modal('Review reward request',fundedClaimForm(c)+'<p class="error-text" id="modal-error" role="alert"></p>');return;}modal('Review reward request',`<p><strong>${esc(c.alias)}</strong> requested ${esc(c.title)} for ${c.cost} Steps.</p><form data-form="claim"><input type="hidden" name="id" value="${c.id}"><input type="hidden" name="expectedStatus" value="${c.status}"><label class="field"><span>Decision</span><select name="status">${c.status==='pending'?'<option value="approved">Approve — arrange the reward</option>':'<option value="given">Mark as given</option>'}<option value="declined">Not approved — return Steps</option></select></label>${c.category==='laptop'&&c.status==='pending'?'<label class="check-label"><input type="checkbox" name="demonstrated"><span>I have seen the learner explain and adapt their project. Required for approval, not for declining.</span></label>':''}<label class="field"><span>Note for the learner</span><textarea name="note" maxlength="500" placeholder="Explain the next step kindly and clearly."></textarea></label>${button('Save decision','form-submit')}</form><p class="error-text" id="modal-error" role="alert"></p>`);}
async function saveResume(){if(me)try{await api('/api/progress',{unit:lessonId,stage:Math.min(5,draft().phase)});}catch{}}
function cancelMissionAdvance(){missionTransition.cancel();}
function scheduleMissionAdvance(){
  const id=lessonId,owner=key(),d=draft(),phase=d.phase,u=unit(id);
  const round=[2,4].includes(phase)?d.rounds[phase]:null,cursor=round?cursorFor(round):null;
  const answer=round?round.answers[round.questions[cursor].id]:missionLabAnswer(u,phase,d);
  const valid=()=>route==='lesson'&&lessonId===id&&key()===owner&&draft()===d&&d.phase===phase&&!dialog.open&&!document.hidden&&!working&&
    (round?round.cursor===cursor&&round.answers[round.questions[cursor].id]===answer&&!!round.checks[round.questions[cursor].id]:missionLabAnswer(u,phase,d)===answer&&missionLabReady(u,phase,d));
  const success=$('[data-mission-success]');
  missionTransition.schedule(valid,()=>{nextMissionPart().catch(e=>toast(errorText(e)));},success,motionAllowed());
}
async function changeLessonScene(commit,focusSelector='#lesson-body'){
  const id=lessonId,owner=key(),phase=draft().phase,surface=$('#lesson-body');
  reader.stop();surface?.setAttribute('aria-busy','true');
  if(surface&&motionAllowed()){
    surface.inert=true;
    try{await surface.animate([{opacity:1},{opacity:0}],{duration:130,easing:'ease-out'}).finished;}catch{}
  }
  if(route!=='lesson'||lessonId!==id||key()!==owner||draft().phase!==phase){surface?.removeAttribute('aria-busy');if(surface)surface.inert=false;return false;}
  commit();lessonView();
  const focus=$(focusSelector)||$('#lesson-body');focus?.setAttribute('tabindex','-1');focus?.focus({preventScroll:true});
  focus?.scrollIntoView({block:'start',behavior:motionAllowed()?'smooth':'instant'});
  return true;
}
async function nextMissionPart(){
  if(route!=='lesson'||!isMission(unit(lessonId))||working)return;
  cancelMissionAdvance();const d=draft(),phase=d.phase;
  working=true;
  try{
    if(phase===1||phase===3){const u=unit(lessonId);if(!missionLabReady(u,phase,d))return;if(u.mission.kind!=='order'){
      const tasks=u.mission.labs[phase===1?0:1],state=u.mission.kind==='scenario'?d.scenarioLab[phase]:d.messageLab[phase];
      if(state.cursor<tasks.length-1){await changeLessonScene(()=>{nextMissionTask(u,phase,d);persist();},'#mission-lab');return;}
    }}else if(phase===2||phase===4){
      const round=d.rounds[phase],cursor=cursorFor(round);if(!round.checks[round.questions[cursor].id])return;
      const next=round.questions.findIndex((q,i)=>i>cursor&&!round.checks[q.id]),remaining=next<0?round.questions.findIndex(q=>!round.checks[q.id]):next;
      if(remaining>=0){await changeLessonScene(()=>{round.cursor=remaining;persist();},'#practice-questions');return;}
    }else return;
    await advance();
  }finally{working=false;}
}
async function advance(){
  cancelMissionAdvance();const d=draft(),id=lessonId,owner=me?.id;
  if([2,4].includes(d.phase)&&d.rounds[d.phase].questions.some(q=>!d.rounds[d.phase].checks[q.id]))return;
  const changed=await changeLessonScene(()=>{d.phase=Math.min(5,(d.phase||0)+1);persist();});
  if(changed&&owner)api('/api/progress',{learner:owner,unit:id,stage:d.phase}).catch(()=>{});
}

async function startCheck(){const d=draft();if(me&&unit(lessonId).projectWorkshop&&(!me.project?.data?.items?.length||!['normal','empty','boundary','invalid'].every(k=>me.project.data.tests?.[k]?.passed)||(me.project.data.explanation||'').length<20)){d.phase=5;lessonView();$('#lesson-error').textContent='Build your useful app, run its four checks and save your project explanation first.';$('#project-workshop').scrollIntoView({block:'start'});return;}if(!d.reflection?.trim()){d.phase=5;lessonView();$('#lesson-error').textContent=reflectionSpec(unit(lessonId)).empty;$('[data-draft=reflection]').focus();return;}try{if(me){d.attempt=await api('/api/attempt',{unit:lessonId});d.attempt.answers=d.savedAnswers?.[d.attempt.id]||{};d.preview=false;}else{d.attempt={...await api('/api/preview-check',{unit:lessonId}),answers:{}};d.preview=true;}if(d.preview)preservePreviewCompletions(local,profileUnlocks(),previewItemUnits());d.phase=6;d.result=null;persist();lessonView();window.scrollTo(0,0);}catch(e){$('#lesson-error')?$('#lesson-error').textContent=errorText(e):toast(errorText(e));}}
async function finish(){const d=draft(),a=d.attempt,alreadyPassed=passed().has(lessonId);const missing=a.questions.find(q=>!String(a.answers[q.id]??'').trim()||(q.kind==='number'&&numberValue(a.answers[q.id])===null));if(missing){$('#lesson-error').textContent='Please answer each question. Number answers can use a fraction such as 3/4.';const input=document.querySelector(`[data-answer="${missing.id}"]`);input.focus();input.scrollIntoView({block:'center'});return;}if(!d.reflection.trim()){$('#lesson-error').textContent=reflectionSpec(unit(lessonId)).empty;$('[data-draft=reflection]').focus();return;}
 if(d.preview){if(a.remotePreview){try{d.result=await api('/api/preview-result',{unit:lessonId,questions:a.questions.map(q=>q.id),answers:a.answers});}catch(error){$('#lesson-error').textContent=errorText(error);persist();return;}}else{const details=a.questions.map(q=>({...q,correct:correct(q,a.answers[q.id]),answer:a.answers[q.id]})),score=details.filter(q=>q.correct).length;d.result={score,passed:score>=5,points:0,at:Date.now()/1000,questions:details};}if(d.result.passed)previewDaily(localStorage,dailyKey(),'module');preservePreviewCompletions(local,profileUnlocks(),previewItemUnits());Object.assign(d.result,awardPreviewReview(localStorage,foodKey(),{unit:lessonId,id:a.id,eligible:unit(lessonId).foodReplay,alreadyPassed,passed:d.result.passed,at:d.result.at},[...passed()]));checkpointQueue.add(guestScope,lessonId,a.id,d.result.passed,alreadyPassed);d.phase=7;persist();lessonView();window.scrollTo(0,0);return;}
 const item={typingPractice:typingSummary(unit(lessonId),d),id:a.id,unit:lessonId,learner:me.id,answers:a.answers,reflection:d.reflection,support:d.support,ink:d.ink||[],practiceRetries:Object.values(d.rounds).reduce((n,r)=>n+Math.max(0,(r.tries||0)-r.questions.length),0)};if(!pending.some(x=>x.id===item.id))pending.push(item);d.phase=7;persist();await syncPending();lessonView();window.scrollTo(0,0);}
async function syncPending(){if(syncing||!me||!pending.length)return;const owner=me.id;syncing=true;try{for(const item of [...pending]){if(me?.id!==owner)break;if(item.learner!==owner)continue;const {error,problem,rejected,...body}=item,alreadyPassed=passed().has(item.unit);try{const result=await api('/api/submit',body);if(me?.id!==owner)break;me=result.me;checkpointQueue.add(owner,item.unit,item.id,result.report.passed,alreadyPassed);{const d=draft(item.unit);d.result=result.report;d.preview=false;d.phase=7;d._dirty=true;queueDraft();}pending=pending.filter(p=>p.id!==item.id);saveLocal();toast(me.personal?'Saved to your own learning record.':'Your report reached your mentor’s inbox.');}catch(e){item.error=errorText(e);item.problem=!!e.status;item.rejected=e.status===404;persist();
  // Offline or signed-out affects every report. One report's own problem must not hold back the others.
  if(!e.status||[401,409,429].includes(e.status))break;}}}finally{syncing=false;status();}}
document.addEventListener('input',e=>{const el=e.target;if(el.name==='starting-answer'&&!starting?._conflict){const next=$('[data-action=starting-answer]');if(next)next.disabled=false;}if(el.dataset.draft&&lessonId){draft()[el.dataset.draft]=el.value;persist();}if(el.dataset.answer&&lessonId){const d=draft(),round=d.phase===6?d.attempt:d.rounds[d.phase];round.answers??={};round.answers[el.dataset.answer]=el.value;if(d.phase===6){d.savedAnswers??={};d.savedAnswers[round.id]=round.answers;}else{round.checks[el.dataset.answer]=false;delete round.last[el.dataset.answer];const card=el.closest('.question');card.classList.remove('correct');card.querySelector('.feedback').textContent='';$('#round-count').textContent=`${round.questions.filter(q=>round.checks[q.id]).length} of ${round.questions.length} worked out`;const next=$('[data-action=advance]')||$('[data-action=mission-next]');if(next)next.disabled=true;if(isMission(unit(lessonId))){cancelMissionAdvance();$('[data-mission-success]').hidden=true;$('[data-action=mission-hold]').hidden=true;}}persist();}});
document.addEventListener('visibilitychange',()=>{if(document.hidden)cancelMissionAdvance();});
document.addEventListener('input',e=>{
  if(!['starting-answer','starting-writing','starting-support'].includes(e.target.name))return;
  saveStartingInput();
  if(e.target.name==='starting-answer'){
    const next=$('[data-action=starting-answer]');if(next)next.disabled=!!(starting?._conflict)||!e.target.value.trim();
  }
  if($('#starting-error'))$('#starting-error').textContent='';
});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches('input[name=starting-answer][type=text]')){e.preventDefault();$('[data-action=starting-answer]')?.click();}});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches('input[data-answer][type=text]')&&route==='lesson'&&isMission(unit(lessonId))&&[2,4].includes(draft().phase)){e.preventDefault();e.target.closest('.question').querySelector('[data-action=check]')?.click();}});
document.addEventListener('change',e=>{if(e.target.matches('[data-voice-choice]')){reader.stop();settings.voice=e.target.value;localStorage.setItem('stepstone-comfort-v1',JSON.stringify(settings));}if(e.target.dataset.setting){settings[e.target.dataset.setting]=e.target.checked;try{localStorage.setItem('stepstone-comfort-v1',JSON.stringify(settings));}catch{}applySettings();}});
document.addEventListener('click',async e=>{if(e.target.closest('[data-close]'))dialog.close();const el=e.target.closest('[data-action]');if(!el||el.disabled)return;const action=el.dataset.action;if(action==='form-submit'){e.preventDefault();el.closest('form')?.requestSubmit();return;}if(working)return;
 try{if(action==='pause'){working=true;await pauseLearning();}else if(action==='starting-answer'||action==='starting-unsure'){working=true;await answerStarting(action==='starting-unsure');}
 else if(action==='starting-write'||action==='starting-skip-writing'){working=true;await finishStartingWriting(action==='starting-skip-writing');}
 else if(action==='start-plan'){e.preventDefault();startFromPlan(el.dataset.unit||plannedNext().id);}
 else if(action==='revisit'){e.preventDefault();revisitLesson(el.dataset.unit);}
 else if(action==='pause-home'){if(route==='home'&&starting?.data&&!startResult()?.complete){starting.dismissed=true;saveStarting();}dialog.close();navigate('#home');}
 
 else if(action==='starting-retry'){modal('Find my starting point',`<p>Take a fresh check. Your saved lessons, passed checks, and Steps stay yours.</p>${ageForm(starting?.data?.age||'')}`);}
 else if(action==='starting-reload'){working=true;const owner=me?.id,result=await api('/api/me');if(me?.id!==owner)return;me=result;starting=result.startingPoint?{...result.startingPoint}:null;saveStarting();home();}

 else if(action==='device-report')modal('Your computer practice',deviceForm(unit(el.dataset.id),me)+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='device-review'){const learner=mentor.learners.find(l=>l.id===el.dataset.learner);modal('Review real-device work',deviceReviewForm(learner,unit(el.dataset.id))+'<p class="error-text" id="modal-error" role="alert"></p>');}
 else if(action==='daily-pip'){profileDialog();toast('Feed '+(currentProfile().alias||'Pip')+', then tap your Pip to play.');}
 else if(action==='laptop-finder')modal('Choose a starter laptop',laptopFinderMarkup());
 else if(action==='laptop-find'){working=true;el.disabled=true;el.textContent='Checking current options…';try{const result=await api('/api/mentor/laptops',{});if(dialog.open&&dialog.querySelector('.laptop-finder'))dialog.querySelector('.laptop-finder').outerHTML=laptopFinderMarkup(result);}finally{el.disabled=false;}}
 else if(action==='funding-record')modal('Record funds or items',fundingForm()+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='ai-plan')modal('Compare your AI help',aiPlanForm(me?.aiSupport,local['digital-6'],unit('digital-6')));
 else if(action==='ai-request'){const owner=me.id;const result=await api('/api/ai/request',{learner:owner});if(me?.id!==owner)return;me=result;rememberMe();render();toast('Your mentor can review your AI month request.');}
 else if(['ai-reserve','ai-approve','ai-activate','ai-release','ai-renewal','ai-close'].includes(action))modal('Manage one AI month',aiMentorForm(action.slice(3),el.dataset.id,mentor));
 else if(action==='funded-person')modal('Confirm the person',personForm(mentor,el.dataset.id)+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='funded-allocate')modal('Set aside rewards',allocationForm(mentor,el.dataset.id)+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='allocation-release')modal('Release an unused place',releaseForm(mentor,el.dataset.id)+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='stock-remove')modal('Correct unassigned stock',stockRemoveForm(mentor,el.dataset.id)+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='funding-export'){const blob=new Blob([exportFunding(mentor)],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='Stepstone-funding-totals.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Anonymous totals exported. No learner names or notes are included.');}
 else if(action==='reward-goal'){working=true;const owner=me.id,result=await api('/api/reward-goal',{id:el.dataset.id,learner:owner});if(me?.id!==owner)return;me=result;if(route==='rewards')rewardsView();status();toast('Your goal is ready on Home.');}
 else if(action==='mentor-learning'){if(!mentor){toast('Sign in to your mentor account first.');return;}working=true;await selectPersonalLearning();navigate('#'+(['home','path','progress','rewards'].includes(el.dataset.destination)?el.dataset.destination:'home'));}else if(action==='choose-role'){if(me&&me.personal){working=true;await personalLearning();}else{setEntryRole(el.dataset.role==='mentor'?'mentor':'learner');navigate(entryRole==='mentor'?'#mentor':'#home');}}else if(action==='mentor-sign-in'){setEntryRole('mentor');navigate('#mentor');}else if(action==='learner-feedback')navigate(tutorial.locked()?'#home':'#progress');else if(action==='learner-rewards')navigate(tutorial.locked()?'#home':'#progress/rewards');else if(action==='begin-invite')await beginInvitation(el.dataset.code);else if(action==='tutorial-restart'||action==='tutorial-skip'){working=true;await controlTutorial(action==='tutorial-skip'?'skip':'restart');}else if(action==='reset-learning'){working=true;await selectPersonalLearning();resetLearningDialog();}else if(action==='messages')await inbox.open();else if(action==='message-thread')await inbox.open(el.dataset.id);else if(action==='profile')profileDialog();else if(action==='pip-home')companion.returnHome();else if(action==='draft-resolve')await resolveDraft();else if(action==='draft-local'||action==='draft-remote')await chooseDraft(action==='draft-local');else if(action==='close')dialog.close();else if(action==='personal-learning'){working=true;await personalLearning();}else if(action==='add-app')installHelp();else if(action==='copy-invite'){await copyPrivateLink(el.dataset.link);toast(mentor?.settings?.sharingReady?'Private link copied. Send it to this learner.':'Local test link copied. Phone invitations need a shared address.');}else if(action==='account'){if(route==='mentor'&&mentor){working=true;await personalLearning();}else account();}else if(action==='stop-reading')reader.stop();else if(action==='voice-sample')reader.read('Welcome to Stepstone. Put the drink cartons in the bag. Take your time. You can see an example whenever you need one.',el);else if(action==='read'||action==='starting-read'){cancelMissionAdvance();if(action==='starting-read')saveStartingInput(true);const target=document.getElementById(action==='starting-read'?'starting-copy':el.dataset.target);if(target)reader.read(narrationText(target),el);}
 else if(action==='mission-example'||action==='mission-try'){reader.stop();cancelMissionAdvance();const d=draft();if(action==='mission-try'&&returnFromExample(d)){persist();saveResume();lessonView();}else{d.examplePhase=action==='mission-example'?d.phase:null;persist();showMissionPane(root,action==='mission-example',motionAllowed());}}else if(action==='mission-hold'){cancelMissionAdvance();el.hidden=true;$('[data-action=mission-next]')?.focus({preventScroll:true});}else if(action==='mission-next'){await nextMissionPart();}else if(action==='advance'){working=true;await advance();}else if(action==='back-lesson'){if(openPracticeExample(draft())){persist();saveResume();lessonView();showMissionPane(root,true,motionAllowed());}}
 else if(action==='hint'){const d=draft(),r=d.rounds[d.phase];r.hints[el.dataset.q]=true;persist();lessonView();}
 else if(action==='check'){const d=draft(),r=d.rounds[d.phase],q=r.questions.find(q=>q.id===el.dataset.q),answer=r.answers[q.id];if(answer===undefined||!String(answer).trim()){el.closest('.question').querySelector('.feedback').textContent='Try an answer first. No attempt counted yet.';return;}if(q.kind==='number'&&numberValue(answer)===null){el.closest('.question').querySelector('.feedback').textContent='Type the answer as a number, such as 12 or 2.50. A fraction such as 3/4 also works. No attempt counted yet.';return;}if(r.last[q.id]!==answer)r.tries++;r.last[q.id]=answer;r.checks[q.id]=correct(q,answer);persist();const top=window.scrollY;lessonView();window.scrollTo(0,top);if(isMission(unit(lessonId))&&r.checks[q.id]){scheduleMissionAdvance();$('[data-action=mission-next]')?.focus({preventScroll:true});}}
 else if(action==='again'){const d=draft();d.phase=1;d.rounds={};resetMissionLabs(unit(lessonId),d);persist();saveResume();lessonView();window.scrollTo(0,0);}else if(action==='start-check'){working=true;await startCheck();}else if(action==='finish'){working=true;el.disabled=true;await finish();}
 else if(action==='ink-undo'||action==='ink-clear'){const d=draft();if(action==='ink-undo')d.ink.pop();else d.ink=[];paintInk($('#ink-pad'),d.ink);persist();}else if(action==='sync'){working=true;await syncPending();render();}else if(action==='restart-check'){pending=pending.filter(p=>p.id!==el.dataset.id);const d=draft();d.attempt=null;d.result=null;d.phase=5;persist();lessonView();window.scrollTo(0,0);}
 else if(action==='theme'){localStorage.setItem('stepstone-theme-'+(me?.id||'guest'),el.dataset.theme);applySettings();document.querySelectorAll('.profile-theme-choices [data-theme]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===el.dataset.theme)));toast('Your colours are ready.');}
 else if(action==='card-request')modal('Choose your gift card',cardRequestForm(me,Number(el.dataset.amount))+'<p class="error-text" id="modal-error" role="alert"></p>');
 else if(action==='card-reveal'){const owner=me.id,card=await api('/api/cards/reveal',{id:el.dataset.id,learner:owner});if(me?.id!==owner)return;modal('Your private card key',cardKeyView(card));}
 else if(action==='copy-card'){const field=document.getElementById(el.dataset.field);await navigator.clipboard.writeText(field.value);toast('Copied. Keep this key private.');}
 else if(action==='reward'){working=true;const owner=me.id,data=await api('/api/reward',{id:el.dataset.id,allocation:el.dataset.allocation||undefined,learner:owner});if(me?.id!==owner)return;me=data.me;if(route==='rewards')rewardsView();status();toast(el.dataset.id.startsWith('theme-')?'Theme unlocked.':'Reward request sent to your mentor.');}
 else if(action==='logout'){await syncPending();if(pending.length){const waiting=unit(pending[0].unit)?.title;$('#account-error').textContent=`A check report${waiting?' for “'+waiting+'”':''} has not been sent yet. Open that lesson to send it, then switch learners.`;return;}await tutorial.sync();if(tutorial.dirty()){$('#account-error').textContent='Connect and save your quick tour before switching learners. If this device has an older copy, close this window and load your saved tour.';return;}await syncStarting();if(starting?._dirty){$('#account-error').textContent=starting._error||'Connect to save your starting check before switching.';return;}await flushDrafts();if(Object.values(local).some(d=>d._dirty)){$('#account-error').innerHTML='Save your drafts before switching learners. <button class="btn secondary small" data-action="draft-resolve">Check draft sync</button>';return;}await api('/api/logout',{role:'learner'});await api('/api/logout',{role:'mentor'});inbox.clear(true);mentor=null;for(const name of ['stepstone-work-v1-','stepstone-starting-v1-','stepstone-tutorial-v1-'])localStorage.removeItem(name+me.id);localStorage.removeItem('stepstone-session-preview-v1');me=null;recovery=null;guestScope='guest';setEntryRole(null);loadLocal();applySettings();dialog.close();navigate('#home');}
 else if(action==='mentor-mode'){mentorRefresh++;mentorAuthMode=el.dataset.mode;devicePending=null;mentorView();}else if(action==='mentor-device-check'){const result=await api('/api/mentor/device-status',{});if(result.pending){devicePending=result;toast('Approval is still pending. Check the matching code on your signed-in mentor device.');}else{devicePending=null;await mentorSignedIn();}}else if(action==='mentor-device-review'||action==='mentor-device-revoke'){await api('/api/mentor/'+(action==='mentor-device-review'?'device-review':'device-revoke'),{id:el.dataset.id,status:el.dataset.status});await loadMentor();toast('Device access updated.');}else if(action==='manager-section')openManagerSection(el.dataset.section);else if(action==='share-invite'){if(navigator.share)try{await navigator.share({title:'Your Stepstone invitation',url:el.dataset.link});}catch(e){if(e.name!=='AbortError')throw e;}}else if(action==='mentor-logout'){await prepareSwitch();lastInvite=null;await api('/api/logout',{role:'mentor'});inbox.clear(true);me=mentor=null;localStorage.removeItem('stepstone-session-preview-v1');loadLocal();navigate('#mentor');}else if(action==='mentor-refresh')await loadMentor();else if(action==='recovery-copy'){working=true;await api('/api/mentor/backup',{});await loadMentor();toast('Recovery copy created and checked on this host.');}else if(action==='invite'){working=true;lastInvite=await api('/api/mentor/invite',{});lastInvite.url??=location.origin+location.pathname+'#join/'+lastInvite.code;$('#new-invite').innerHTML=inviteCard(lastInvite,formatDate);}
 else if(action==='review-report')reviewReport(el.dataset.id);else if(action==='claim-review')claimReview(el.dataset.id);else if(action==='recover'){const l=mentor.learners.find(l=>l.id===el.dataset.id);modal('Replace a sign-in code',`<p>Replace the code for ${esc(l.alias)}? Their old code and existing sessions will stop working. Their completed reports stay saved.</p><div class="buttons">${button('Replace this learner’s code','confirm-recover',`data-id="${l.id}"`,'secondary')}</div>`);}else if(action==='confirm-recover'){const r=await api('/api/mentor/recovery',{id:el.dataset.id});modal('New private sign-in link',`<p>Give this link privately to the learner. One tap and a Start button bring back their account.</p><label class="field"><span>Private return link</span><input readonly value="${esc(r.url||location.origin+location.pathname+'#resume/'+r.code)}"></label>${button('Copy return link','copy-invite',`data-link="${esc(r.url||location.origin+location.pathname+'#resume/'+r.code)}"`,'secondary')}<p class="legend">The old sign-in code no longer works. Their progress stays saved.</p>`);}
 else if(action==='copy-recovery'){try{await navigator.clipboard.writeText(recovery);toast('Private sign-in code copied. Keep it safe.');}catch{toast('Select the code above and copy it.');}}
 else if(action==='export-reports'){const blob=new Blob([JSON.stringify({exportedAt:new Date().toISOString(),reports:mentor.reports,learners:mentor.learners},null,2)],{type:'application/json'});download(blob,'stepstone-mentor-reports.json');}
 else if(action==='install'&&installPrompt){await installPrompt.prompt();installPrompt=null;dialog.close();}
 }catch(error){const dest=dialog.open?$('#modal-error')||$('#account-error'):$('#lesson-error');if(dest)dest.textContent=errorText(error);else toast(errorText(error));}finally{working=false;if(el.isConnected&&action==='finish')el.disabled=false;}});
function download(blob,name){const href=URL.createObjectURL(blob),a=document.createElement('a');a.href=href;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(href),2000);}
function showFormError(form,target,error){
  if(!form.isConnected)return;
  if(!target){target=form.querySelector('[data-form-error]');if(!target){target=document.createElement('p');target.className='error-text';target.dataset.formError='';target.setAttribute('role','alert');form.append(target);}}
  target.id||='form-error-'+form.dataset.form;
  target.textContent=errorText(error);target.tabIndex=-1;
  form.setAttribute('aria-describedby',target.id);
  const field=error.field&&form.querySelector(`[name="${CSS.escape(error.field)}"]`);
  if(field){
    (field.closest('.field,fieldset')||field).insertAdjacentElement('afterend',target);
    field.setAttribute('aria-invalid','true');field.dataset.formInvalid=target.id;
    field.setAttribute('aria-describedby',[...new Set((field.getAttribute('aria-describedby')||'').split(' ').filter(Boolean).concat(target.id))].join(' '));
    field.closest('details')?.setAttribute('open','');field.focus();
  }else target.focus({preventScroll:true});
  target.scrollIntoView({block:'nearest'});
}
document.addEventListener('input',event=>{const field=event.target,id=field.dataset.formInvalid;if(!id)return;field.removeAttribute('aria-invalid');delete field.dataset.formInvalid;const described=(field.getAttribute('aria-describedby')||'').split(' ').filter(value=>value!==id).join(' ');if(described)field.setAttribute('aria-describedby',described);else field.removeAttribute('aria-describedby');const error=document.getElementById(id);if(error)error.textContent='';});
document.addEventListener('submit',async e=>{const form=e.target.closest('form[data-form]');if(!form)return;e.preventDefault();if(working)return;working=true;const values=Object.fromEntries(new FormData(form)),kind=form.dataset.form;const submit=form.querySelector('[type=submit]')||(form.id?dialog.querySelector('[type=submit][form="'+form.id+'"]'):null);if(submit)submit.disabled=true;
 try{if(kind==='starting-age'){await beginStarting(Number(values.age));}
 else if(kind==='profile'){
  const value=validateProfile(profileValues(form,currentProfile()),!!me,currentProfile(),passed().size,currentInventory());
  if(me){const owner=me.id,result=await api('/api/profile',{...value,learner:owner});if(me?.id!==owner)return;me=result;rememberMe();}
  else localStorage.setItem(guestProfileKey(),JSON.stringify(value));
  if(form.dataset.intro){tutorial.clearProfileDraft();render();window.scrollTo(0,0);const heading=root.querySelector('h1,h2');if(heading){heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});}}
  else if(form.dataset.setup){tutorial.profileSaved();readRoute();}
  else{dialog.addEventListener('close',()=>$('#profile-slot .companion-profile')?.focus({preventScroll:true}),{once:true});dialog.close();render();toast('Your profile is saved.');}
 }
 else if(kind==='setup-mentor'){await joinLearner({...values,alias:currentProfile().alias,avatar:currentProfile().avatar,share:values.share==='on'},true);}
 else if(kind==='setup-goal'){
   if(!['core-card-everyday','card-exchange','core-laptop'].includes(values.goal))throw Error('Choose one reward goal.');
   if(me&&!me.personal){me=await api('/api/reward-goal',{id:values.goal});rememberMe();}
   await tutorial.goalSaved(values.goal);
 }
 else if(kind==='join'){if(!nameFilter(values.alias))throw Error('Choose a different Pip name.');await joinLearner({...values,share:values.share==='on'});}
 else if(kind==='login'||kind==='quick-resume'){
   const expectedLearner=hasUnsent()?me.id:undefined;
   const result=await api('/api/login',{...values,expectedLearner});
   if(me?.id!==result.id)inbox.clear(true);
   me=result;setEntryRole(result.personal?'mentor':'learner');mentor=null;lastInvite=null;recovery=result.recovery||null;guestScope='guest';pendingInvite='';localStorage.removeItem('stepstone-pending-invite');forgetEntryCode();
   loadLocal();await hydrateDrafts();applySettings();await syncPending();await flushDrafts();if(dialog.open)dialog.close();navigate('#home');toast('Your saved learning is ready.');
 }
 else if(kind==='mentor-auth'){mentorRefresh++;const mode=form.dataset.mode;if(mode!=='login'&&values.passphrase!==values.confirm)throw new Error('The two passphrases do not match.');await prepareSwitch();const result=await api('/api/mentor/'+mode,{...values,claimExisting:values.claimExisting==='on'});if(result.pending){devicePending=result;mentorView();}else{devicePending=null;await mentorSignedIn();if(result.recovery)modal('Save your private recovery key',`<p>Keep this key somewhere private outside this browser. It lets you recover your account if you lose this device or forget your passphrase.</p><label class="field"><span>Recovery key — shown once</span><input readonly value="${esc(result.recovery)}"></label><p>Anyone with this key can take control of your mentor account. Your learners do not need it.</p>${button('I have saved my key','close')}`);}}


 else if(kind==='device-work'){const owner=me.id;const result=await api('/api/device-work',{...values,learner:owner,revision:Number(values.revision),steps:unit(values.unit).deviceTask.steps.map((_,i)=>values['step-'+i]==='on')});if(me?.id!==owner)return;me=result;dialog.close();render();toast('Device update saved. Your mentor can review it.');}
 else if(kind==='device-review'){await api('/api/mentor/device-work',{...values,revision:Number(values.revision),observed:values.observed==='on'});await loadMentor();dialog.close();toast('Device review saved.');}
 else if(kind==='ai-plan'){const owner=me.id;const result=await api('/api/ai/plan',{...values,learner:owner,revision:Number(values.revision),permitted:values.permitted==='on'});if(me?.id!==owner)return;me=result;rememberMe();dialog.close();render();toast('Your comparison notes are saved.');}
 else if(kind.startsWith('ai-mentor-')){const data={...values};if(data.revision!==undefined)data.revision=Number(data.revision);if(data.amount!==undefined){const match=data.amount.match(/^(\d+)(?:\.(\d{1,2}))?$/);if(!match)throw new Error('Use dollars and cents, such as 35.00.');data.cents=Number(match[1])*100+Number((match[2]||'').padEnd(2,'0'));delete data.amount;}for(const flag of ['terms_checked','own_account','monthly_only','no_addons','demonstrated','guardian_permission','paid_confirmed','verified'])data[flag]=values[flag]==='on';await api('/api/mentor/ai/'+kind.slice(10),data);await loadMentor();dialog.close();toast('AI month record saved. No payment was made by Stepstone.');}
 else if(kind.startsWith('cards-')){const data={...values};for(const n of ['amount_cents','revision','expected_revision'])if(data[n]!==undefined)data[n]=Number(data[n]);if(data.amount!==undefined){if(!/^\d+$/.test(data.amount))throw new Error('Use whole Canadian dollars.');data.cents=Number(data.amount)*100;delete data.amount;}if('demonstrated' in data)data.demonstrated=data.demonstrated==='on';if('confirmed' in data)data.confirmed=data.confirmed==='on';if(kind==='cards-request'){const owner=me.id,result=await api('/api/cards/request',{...data,learner:owner});if(me?.id!==owner)return;me=result.me;rememberMe();dialog.close();render();toast('Card requested. Steps deducted once.');}else{await api('/api/mentor/cards/'+kind.slice(6),data);await loadMentor();dialog.close();toast(kind==='cards-deliver'?'Card key delivered privately.':'Card record saved.');}}
 else if(kind.startsWith('funded-')){const data={...values};for(const name of ['quantity','expected_quantity'])if(data[name]!==undefined)data[name]=Number(data[name]);if(data.amount!==undefined){const match=data.amount.match(/^(\d+)(?:\.(\d{1,2}))?$/);if(!match)throw new Error('Use dollars and cents, such as 20.00.');data.cents=Number(match[1])*100+Number((match[2]||'').padEnd(2,'0'));delete data.amount;}data.confirmed=data.confirmed==='on';await api('/api/mentor/funded/'+kind.slice(7),data);await loadMentor();dialog.close();toast(kind==='funded-allocate'?'Rewards set aside. Existing places were kept.':'Record saved.');}
 else if(kind==='reward-stock'){await api('/api/mentor/reward-stock',{id:values.id,stock:Number(values.stock),expectedStock:values.expectedStock===''?null:Number(values.expectedStock)});await loadMentor();toast('Secured quantity updated.');}
 else if(kind==='reset-learning'){if(values.confirm!=='yes')throw new Error('Confirm that you want to reset only your own learning.');await resetMyLearning();}
 else if(kind==='recovery-reconciled'){await api('/api/mentor/recovery-reconciled',{confirmed:values.confirmed==='on',note:values.note});await loadMentor();toast('Reward requests reopened after your recorded check.');}
 else if(kind==='review'){await api('/api/mentor/review',values);await loadMentor();dialog.close();toast('Review saved. The learner can see your note.');}
 else if(kind==='claim'){const demonstration=Object.fromEntries(Object.keys(values).filter(k=>k.startsWith('demo-')).map(k=>[k.slice(5),values[k]==='on']));await api('/api/mentor/claim',{...values,revision:values.revision===undefined?undefined:Number(values.revision),demonstration,demonstrated:values.demonstrated==='on'});await loadMentor();dialog.close();toast('Reward decision saved.');}}
 catch(error){const target=kind==='profile'?$('#profile-error'):kind==='starting-age'?$('#starting-error'):kind==='mentor-auth'?$('#mentor-error'):kind==='reward'?$('#reward-error'):kind==='reward-stock'?form.querySelector('[data-stock-error]'):kind==='recovery-reconciled'?form.querySelector('[data-recovery-error]'):$('#setup-error')||$('#entry-error')||$('#account-error')||$('#modal-error');showFormError(form,target,error);}finally{working=false;if(submit?.isConnected)submit.disabled=false;}});
window.addEventListener('hashchange',()=>{if(dialog.open)dialog.close();readRoute();});window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;});window.addEventListener('offline',()=>{online=false;status();});window.addEventListener('online',async()=>{online=true;await syncPendingProfile();await flushDrafts();await syncPending();await syncStarting();await tutorial.sync();if(!tutorial.visible()&&(['progress','rewards'].includes(route)||route==='lesson'&&draft().phase===7))render();});
document.addEventListener('change',event=>{if(event.target.matches('[data-funding-kind]'))updateFundingForm(event.target.form);});
setInterval(async()=>{if(document.hidden||working||syncing)return;try{if(me){const owner=me.id;await syncPending();await syncStarting();await tutorial.sync();const result=await api('/api/me');if(me?.id!==owner)return;me=result;status();paintDaily();if(!tutorial.visible()&&!dialog.open&&!document.activeElement?.matches('input,textarea,select')&&['progress','rewards'].includes(route))render();}if(route==='mentor'&&mentor&&!dialog.open&&!document.activeElement?.matches('input,textarea,select,iframe')&&!root.querySelector('[data-project-mentor-preview] iframe')&&![...root.querySelectorAll('form input,form textarea,form select')].some(el=>el.type==='checkbox'||el.type==='radio'?el.checked!==el.defaultChecked:el.tagName==='SELECT'?el.value!==([...el.options].find(o=>o.defaultSelected)||el.options[0])?.value:el.value!==el.defaultValue))await loadMentor();}catch{}},20000);
async function boot(){
  const opened=performance.now();root.innerHTML=openingMarkup();applySettings();
  try{
    let tourConfig,profileConfig,filterConfig;
    [catalog,startingBank,tourConfig,foundationPlan,profileConfig,filterConfig]=await Promise.all(['catalog.json?build=123','starting-point.json?build=123','tutorial.json?build=123','foundation.json?build=123','profile-options.json?build=123','text-filter.json?build=123'].map(async path=>{const response=await fetch(path);if(!response.ok)throw Error('A setup file could not load. Reload to try again.');return response.json();}));
    nameFilter=createTextFilter(filterConfig);configureLanguage(nameFilter);configureProfile(profileConfig,nameFilter);tutorial.configure(tourConfig);
    try{health=await api('/api/health');keepHostInformed(api,health);}catch{}
    try{me=await api('/api/me');rememberMe();}
    catch(e){if(!e.status){try{me=displayPayload(JSON.parse(localStorage.getItem('stepstone-session-preview-v1')||'null'));}catch{}}else if(e.status===401)localStorage.removeItem('stepstone-session-preview-v1');}
    if(!me){
      pendingInvite=location.hash.startsWith('#join/')?decodeURIComponent(location.hash.slice(6)):localStorage.getItem('stepstone-pending-invite')||'';
      if(pendingInvite){pendingInvite=inviteCode(pendingInvite);localStorage.setItem('stepstone-pending-invite',pendingInvite);guestScope='guest-invite-'+pendingInvite;history.replaceState(null,'',location.pathname+location.search+'#home');}
    }
    loadLocal();
    if(!me&&!localStorage.getItem('stepstone-pip-awards-v2-'+guestScope)){
      preservePreviewCompletions(local,profileUnlocks().map(item=>({...item,modules:item.legacyModules??item.modules})));
      saveLocal();localStorage.setItem('stepstone-pip-awards-v2-'+guestScope,'true');
    }
    await hydrateDrafts();await syncPendingProfile();
    let roleChoice;try{roleChoice=localStorage.getItem('stepstone-entry-role-v1');}catch{}
    setEntryRole(resolveEntryRole({account:me,choice:pendingInvite?'learner':roleChoice,hasLearning:!!(starting?.data||guestProfile()?.alias||tutorial.export()?.data?.events?.length)}));
    if(entryRole==='mentor'&&!me&&!/^#(?:join|resume)(?:\/|$)/.test(location.hash))history.replaceState(null,'',location.pathname+location.search+'#mentor');
    if(me&&startResult()?.complete&&!me.welcomeAwards?.starting&&tutorial.early()){starting._dirty=true;await syncStarting();}
    if(tutorial.done()&&!/^#(?:mentor|join|resume|progress)(?:\/|$)/.test(canonicalHubHash(location.hash)))history.replaceState(null,'',location.pathname+location.search+'#home');
    if(motionAllowed()){
      await new Promise(resolve=>setTimeout(resolve,Math.max(0,3800-(performance.now()-opened))));
      root.querySelector('.launch-sequence')?.classList.add('launch-complete');
      await new Promise(resolve=>setTimeout(resolve,220));
    }
    appReady=true;applySettings();document.documentElement.classList.remove('is-opening');readRoute();
    await syncPending();await syncStarting();await tutorial.sync();
    if('serviceWorker'in navigator&&location.protocol!=='file:')navigator.serviceWorker.register('sw.js').catch(()=>{});
  }catch(e){document.documentElement.classList.remove('is-opening');root.innerHTML='<section class="card"><h1>The app could not open.</h1><p>'+esc(errorText(e))+'</p><p>Keep Stepstone running and reload this page.</p></section>';}
}
boot();


// Drafts use an optimistic revision so two devices cannot silently erase each other.
let draftTimer,draftFlight=null,draftConflict=null;
function queueDraft(){clearTimeout(draftTimer);draftTimer=setTimeout(()=>flushDrafts(),1000);}
async function hydrateDrafts(){if(!me)return;const owner=me.id;try{const remote=await api('/api/drafts');if(me?.id!==owner)return;for(const [id,d] of Object.entries(local))if(!remote[id]&&!d._revision)d._dirty=true;for(const [id,saved] of Object.entries(remote)){if(!local[id]?._dirty)local[id]={...saved.data,_revision:saved.revision};}saveLocal();}catch{}}
async function flushDrafts(){if(draftFlight)return draftFlight;if(!me)return;const owner=me.id;draftFlight=(async()=>{for(const [id,d] of Object.entries(local)){if(!d._dirty||me?.id!==owner)continue;const snapshot=JSON.stringify(d),data={...d};delete data._dirty;delete data._revision;try{const saved=await api('/api/draft',{learner:owner,unit:id,revision:d._revision||0,data});if(me?.id!==owner)return;const unchanged=JSON.stringify(local[id])===snapshot;local[id]._revision=saved.revision;if(unchanged)delete local[id]._dirty;else queueDraft();draftConflict=null;saveLocal();}catch(e){if(e.status===409){draftConflict={id,owner};toast('A draft changed on another device. Open your account to choose which one to keep.');}break;}}})().finally(()=>{draftFlight=null;});return draftFlight;}
async function resolveDraft(){await flushDrafts();if(!draftConflict){toast(Object.values(local).some(d=>d._dirty)?'Reconnect or sign in again to save your drafts.':'Your drafts are saved.');return;}const remote=await api('/api/drafts'),{id,owner}=draftConflict;if(me?.id!==owner)return;draftConflict.remote=remote[id];const mine=local[id],other=remote[id]?.data;modal('Choose a lesson draft',`<p>Both versions of “${esc(unit(id).title)}” are preserved until you choose. Check the explanations below.</p><h3>This device</h3><p class="notice">Step ${Math.min(7,(mine.phase||0)+1)} · ${esc(mine.reflection||'No written explanation yet.')}</p><h3>Other device</h3><p class="notice">Step ${Math.min(7,(other?.phase||0)+1)} · ${esc(other?.reflection||'No written explanation yet.')}</p><p class="legend">Completed check reports stay saved whichever draft you choose.</p><div class="buttons"><button class="btn" data-action="draft-local">Keep this device’s draft</button><button class="btn secondary" data-action="draft-remote">Use the other draft</button></div><p class="error-text" id="modal-error"></p>`);}
async function chooseDraft(keepLocal){const c=draftConflict;if(!c||me?.id!==c.owner)return;if(keepLocal){local[c.id]._revision=c.remote?.revision||0;local[c.id]._dirty=true;}else local[c.id]={...c.remote.data,_revision:c.remote.revision};draftConflict=null;saveLocal();await flushDrafts();dialog.close();render();}
function profileDialog(){
 modal('My profile',profileForm({name:currentProfile().alias,symbol:currentProfile().avatar,profile:currentProfile(),connected:!!me,completed:passed().size,owned:currentInventory(),food:currentFood(),theme:currentTheme(),editor:true,readingControls:readingControls(),panel:tutorial.stage()==='comfort'?'reading':'pip'}),{profile:true,footer:(me?'<button class="btn secondary" type="button" data-action="account" aria-label="Account & sign-in">Account</button>':'')+'<button class="btn" type="submit" form="profile-editor">Save profile</button>'});
 const name=$('#profile-editor input[name="alias"]');name.setCustomValidity(profileNameError(name.value,name.dataset.originalName));
}

function mentorSetupMarkup(){
  if(me)return '<section class="card" data-mentor-step><h2>'+(me.personal?'This is your personal learning space.':'Your mentor is connected.')+'</h2><p>'+(me.personal?'Your progress is separate from the people you support.':'Your mentor sees your starting answers, finished checks, explanations and chosen goals. Other learners cannot see them.')+'</p><button class="btn" data-tour="mentor-connected">Got it. Choose my goal →</button></section>';
  return '<section class="card" data-mentor-step><h2>Save with your mentor.</h2><p>Use the invitation your mentor sent you. A link or a code works.</p><form data-form="setup-mentor"><label class="field"><span>Mentor invitation link or code</span><input name="code" value="'+esc(pendingInvite)+'" required minlength="8" autocomplete="off" spellcheck="false"></label><label class="check-label"><input name="share" type="checkbox" required><span>My mentor can see my age, starting answers, profile, finished work and goals. Other learners cannot.</span></label><button class="btn" type="submit">Connect & save my progress →</button><p class="error-text" id="setup-error" role="alert"></p></form><details><summary class="preview-choice">Just trying the app?</summary><p>You can learn on this device for now. Your welcome Steps stay here until you connect. You cannot request real rewards without a mentor.</p><button class="btn secondary" data-tour="mentor-device">Use this device for now →</button></details></section>';
}
function rewardTourMarkup(){
  const content='<section class="card"><p class="eyebrow">REWARDS</p><h2>Something to work towards.</h2><p>Complete useful skills and choose a goal with your mentor.</p><div class="setup-reward-grid"><article><span aria-hidden="true">▰</span><h3>Gift cards</h3><p>Complete practical skills. Your mentor checks your work and confirms which rewards are funded.</p></article><article><span aria-hidden="true">▱</span><h3>A learning laptop</h3><p>Build your everyday skills, then get ready to use a computer safely.</p></article></div><p class="notice">Choosing a goal does not reserve or buy a reward. Your mentor handles funding and delivery.</p></section>';
  return learningHubMarkup({points:tutorial.bonus(),modules:passed().size,checks:me?.totalChecks??0,preview:!me,rewards:content,rewardsOnly:true});
}
function goalSetupMarkup(){
  return '<form class="card setup-goal-form" data-form="setup-goal"><fieldset data-goal-choices><legend>My first reward goal</legend><div class="setup-reward-grid">'+[['card-exchange','Start with gift cards','Develop skills for everyday decisions.'],['core-laptop','Work towards a laptop','Develop practical skills, then prepare to use your own computer.']].map(([id,title,text])=>'<label class="setup-goal"><input type="radio" name="goal" value="'+id+'" required '+(me?.goal===id?'checked':'')+'><strong>'+title+'</strong><span>'+text+'</span></label>').join('')+'</div></fieldset><p>Your mentor confirms the requirements and funding.</p><button class="btn" type="submit">Save my goal & continue →</button><p class="error-text" id="setup-error" role="alert"></p></form>';
}
function inviteCode(value){
  const raw=String(value||'').trim();
  if(raw.includes('://')){
    let url;try{url=new URL(raw);}catch{throw Error('Paste the full invitation link or just its code.');}
    if(url.origin!==location.origin||!url.hash.startsWith('#join/'))throw Error('Use an invitation for this Stepstone app.');
    return decodeURIComponent(url.hash.slice(6));
  }
  if(!/^[A-Za-z0-9_.-]{8,100}$/.test(raw))throw Error('Check the invitation code your mentor sent.');
  return raw;
}
async function syncPendingProfile(){
  if(!me)return;
  const key='stepstone-profile-pending-'+me.id,raw=localStorage.getItem(key);if(!raw)return;
  const owner=me.id,value=validateProfile(JSON.parse(raw),true,currentProfile(),passed().size,currentInventory()),fresh=await api('/api/profile',value);
  if(me?.id!==owner)return;me=fresh;localStorage.removeItem(key);rememberMe();
}
async function beginInvitation(raw){
  const code=inviteCode(raw);await prepareSwitch();forgetEntryCode();
  if(me){await api('/api/logout',{role:'learner'});await api('/api/logout',{role:'mentor'});for(const name of ['stepstone-work-v1-','stepstone-starting-v1-','stepstone-tutorial-v1-'])localStorage.removeItem(name+me.id);}
  me=mentor=null;recovery=null;localStorage.removeItem('stepstone-session-preview-v1');
  setEntryRole('learner');pendingInvite=code;guestScope='guest-invite-'+code;localStorage.setItem('stepstone-pending-invite',code);
  loadLocal();applySettings();navigate('#home');
}
async function joinLearner(values,setup=false){
  const migrate=!me,oldScope=guestScope,oldStart=migrate?structuredClone(starting):null,oldTour=migrate?tutorial.export():null,profile=migrate?currentProfile():null;
  if(me)await prepareSwitch();
  const result=await api('/api/join',{...values,code:inviteCode(values.code)});
  me=result;companion.adoptPosition(oldScope,me.id);setEntryRole('learner');mentor=null;recovery=result.recovery||null;lastInvite=null;
  if(migrate){
    if(oldStart?.data)localStorage.setItem('stepstone-starting-v1-'+me.id,JSON.stringify({...oldStart,revision:0,_dirty:true}));
    if(oldTour)localStorage.setItem('stepstone-tutorial-v1-'+me.id,JSON.stringify({...oldTour,revision:0,_dirty:true}));
    if(profile?.alias)localStorage.setItem('stepstone-profile-pending-'+me.id,JSON.stringify(availableProfileExtras({accent:'mint',motivation:'confidence',interests:[],nextWin:'',...profile},currentProfile(),passed().size,currentInventory())));
    // The guest copy now belongs to this account. The next person on this device starts fresh.
    for(const name of ['stepstone-work-v1-','stepstone-starting-v1-','stepstone-tutorial-v1-','stepstone-guest-profile-v1-'])localStorage.removeItem(name+oldScope);
  }
  guestScope='guest';
  loadLocal();await hydrateDrafts();
  if(migrate){
    await syncPendingProfile();
    if(oldStart?.data){starting={...oldStart,revision:0,_dirty:true};saveStarting();await syncStarting();if(starting._dirty)throw Error(starting._error||'Your account is connected. Reconnect to save your starting answers before continuing.');}
    if(oldTour){tutorial.adopt(oldTour);await tutorial.sync();if(tutorial.dirty())throw Error('Your account is connected. Reconnect to save your setup before continuing.');}
    const wish=oldTour?.data.events.find(e=>e.action==='goal')?.value;
    if(wish){me=await api('/api/reward-goal',{id:wish});rememberMe();}
  }
  pendingInvite='';localStorage.removeItem('stepstone-pending-invite');
  applySettings();if(dialog.open)dialog.close();
  if(setup)await tutorial.action('mentor-connected');
  readRoute();toast('Connected. Your starting answers, profile and welcome Steps are saved.');
}
async function controlTutorial(action){
  await selectPersonalLearning();
  await tutorial.sync();if(tutorial.dirty())throw Error('Save your current setup before changing it.');
  const owner=me.id,fresh=await api('/api/mentor/tutorial-control',{learner:owner,revision:me.tutorial?.revision||0,action});
  if(me?.id!==owner)return;
  me=fresh;tutorial.replace(fresh.tutorial);rememberMe();dialog.close();navigate('#home');
  toast(action==='skip'?'Your setup was skipped. No tutorial bonus was added.':'Your tour is ready to try again. Your learning and Steps are unchanged.');
}
function updateProfilePreview(event){
  const form=event.target.closest('form[data-form="profile"]');if(!form)return;
  const value=profileValues(form,currentProfile());applyProfileColour(value.accent);form.querySelector('[data-profile-preview]').innerHTML=profilePreview(value);paintFood(form,currentFood());
  const input=form.querySelector('input[name="alias"]'),error=profileNameError(value.alias,input.dataset.originalName);
  input.setCustomValidity(error);input.setAttribute('aria-invalid',String(!!error));form.querySelector('[data-name-error]').textContent=error;
  form.querySelector('[data-name-count]').textContent=value.alias.length>12&&value.alias===input.dataset.originalName?value.alias.length+' characters':value.alias.length+'/12';
  if(form.dataset.setup||form.dataset.intro)tutorial.saveProfileDraft(value);
}
document.addEventListener('click',event=>{
 const tab=event.target.closest('button[data-profile-tab]'),page=event.target.closest('button[data-pip-page]'),form=(tab||page)?.closest('.profile-form');if(!form)return;
 if(tab){form.dataset.panel=tab.dataset.profileTab;form.querySelectorAll('[data-profile-tab]').forEach(button=>{const active=button===tab;button.setAttribute('aria-selected',String(active));button.tabIndex=active?0:-1;});}
 if(page){form.dataset.pipPage=page.dataset.pipPage;form.querySelectorAll('.pip-pages button').forEach(button=>button.setAttribute('aria-pressed',String(button===page)));}
});
document.addEventListener('keydown',event=>{
 const tab=event.target.closest('button[data-profile-tab]');if(!tab||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
 event.preventDefault();const tabs=[...tab.parentElement.querySelectorAll('button')],index=tabs.indexOf(tab),next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
 tabs[next].focus();tabs[next].click();
});
document.addEventListener('input',updateProfilePreview);
document.addEventListener('change',updateProfilePreview);


function isLocalAddress(){return ['localhost','127.0.0.1','::1'].includes(location.hostname);}
function hasUnsent(){return !!me&&(pending.length>0||starting?._dirty||tutorial.dirty()||Object.values(local).some(d=>d._dirty));}
async function prepareSwitch(){if(!me){inbox.clear(true);return;}await syncPending();await flushDrafts();await syncStarting();await tutorial.sync();if(hasUnsent())throw new Error('Save the current learner’s work before changing accounts. Reconnect or use Check draft sync in the account menu.');inbox.clear(true);}
async function selectPersonalLearning(){
  await prepareSwitch();const own=await api('/api/mentor/learn',{});
  me=own;setEntryRole('mentor');recovery=null;loadLocal();await hydrateDrafts();applySettings();rememberMe();
}
async function personalLearning(){await selectPersonalLearning();if(dialog.open)dialog.close();navigate('#home');toast('My learning is ready. Your progress stays separate from the learners’.');}
// Invitation and return-link secrets stay in this tab only, never in the address bar or history.
let entrySecret=null;
function keepEntryCode(kind,raw){let code='';try{code=decodeURIComponent(raw);}catch{}entrySecret={route:kind,code};try{sessionStorage.setItem('stepstone-entry-code',JSON.stringify(entrySecret));}catch{}}
function entryCode(kind){if(entrySecret?.route===kind)return entrySecret.code;try{const saved=JSON.parse(sessionStorage.getItem('stepstone-entry-code')||'null');return saved?.route===kind?saved.code:'';}catch{return '';}}
function forgetEntryCode(){entrySecret=null;try{sessionStorage.removeItem('stepstone-entry-code');}catch{}}
function entryView(){
  const code=entryCode(route);
  if(!code){root.innerHTML='<section class="entry-card card"><h1>This link is incomplete.</h1><p>Ask your mentor for a new link, or use your private sign-in code from Account & sign-in.</p><a class="btn" href="#home">Go to Home</a></section>';return;}
  if(route==='join'){
    root.innerHTML='<section class="entry-card card"><h1>A new learner’s invitation.</h1><p>'+ (me?'Your current account will be saved before starting a separate profile.':'Start with your age. Your invitation will be ready when you reach the mentor step.')+'</p><button class="btn" data-action="begin-invite" data-code="'+esc(code)+'">Start with this invitation →</button><a class="btn secondary" href="#home">Return to my current learning</a></section>';return;
  }
  root.innerHTML='<section class="entry-card card"><p class="eyebrow">WELCOME BACK</p><h1>Your progress is waiting.</h1><form data-form="quick-resume"><input type="hidden" name="code" value="'+esc(code)+'"><p>Your mentor’s return link opens your existing account.</p><p class="error-text" id="entry-error" role="alert"></p><button class="btn entry-start" type="submit">Open my learning →</button></form><p>This device remembers you. Use Save & switch learner when sharing a device.</p></section>';
}
function installHelp(){const installed=matchMedia('(display-mode: standalone)').matches||navigator.standalone;modal(installed?'You’re already using the app':'Put Stepstone on your home screen',installed?'<p>You can come back using the Stepstone icon on this device.</p>':`<p>Keep it one tap away. You can also keep using it in this browser.</p>${installPrompt?'<div class="buttons"><button class="btn" data-action="install">Install Stepstone</button></div>':''}<div class="install-steps"><section><h3>iPhone or iPad</h3><ol><li>Open this page in Safari.</li><li>Tap <strong>Share</strong>, then <strong>Add to Home Screen</strong>. It may be under More.</li><li>If offered, keep <strong>Open as Web App</strong> on. Tap <strong>Add</strong>.</li></ol></section><section><h3>Android phone or tablet</h3><ol><li>Open this page in Chrome.</li><li>Tap the <strong>⋮</strong> menu.</li><li>Choose <strong>Add to home screen</strong>, then <strong>Install</strong> if offered.</li></ol></section><section><h3>Windows PC</h3><p>In Edge or Chrome, use the install icon near the address bar if it appears. You can also bookmark this page.</p></section></div>${isLocalAddress()?'<p class="notice">This preview is on this laptop. Your mentor will need a shared secure web address before this works on other devices.</p>':''}<p class="legend">No payment or app-store account is needed to use Stepstone in a browser.</p>`);}

function resetLearningDialog(){
 if(!me?.personal)return;
 modal('Start your learning again?',`<p>This permanently clears <strong>your My learning record</strong>: starting check, quick tour, drafts, checks, practice history, Steps and Pip choices. Your mentor dashboard, learner accounts, reports, and reward offers stay intact.</p><p>Other devices using your old personal record will need to reopen My learning. Reading and comfort settings stay as you chose them.</p><form data-form="reset-learning"><label class="check-label"><input type="checkbox" name="confirm" value="yes" required><span>Erase only my personal learning history and start fresh.</span></label>${button('Reset my learning','form-submit','','secondary')}</form><p id="modal-error" class="error-text" role="alert"></p>`);
}
async function resetMyLearning(){
 if(!me?.personal)throw new Error('Open My learning from your mentor dashboard first.');
 const old=me.id;
 clearTimeout(draftTimer);
 clearTimeout(startingTimer);
 tutorial.stop();
 await Promise.all([draftFlight,startingFlight,tutorial.flight()].filter(Boolean));
 for(let i=0;syncing&&i<40;i++)await new Promise(r=>setTimeout(r,100));
 if(syncing)throw new Error('A report is still sending. Wait for it to finish, then reset.');
 const fresh=await api('/api/mentor/reset-learning',{learner:old,confirmation:'RESET MY LEARNING'});
 for(const name of ['stepstone-work-v1-'+old,'stepstone-starting-v1-'+old,'stepstone-tutorial-v1-'+old,'stepstone-theme-'+old])localStorage.removeItem(name);
 clearTimeout(draftTimer);draftConflict=null;me=fresh;recovery=null;local={};pending=[];starting=null;loadLocal();applySettings();dialog.close();navigate('#home');status();toast('Your fresh start is ready. Learner records were preserved.');
}

window.speechSynthesis?.addEventListener('voiceschanged',()=>{const select=document.querySelector('[data-voice-choice]');if(select)select.innerHTML=voiceOptions(settings.voice||'soft',health.softVoice!==false);});

document.addEventListener('change',async e=>{
 const toggle=e.target.closest('[data-host-background]');if(!toggle)return;
 const next=toggle.checked;toggle.disabled=true;working=true;
 try{const result=await api('/api/mentor/settings',{keepRunning:next});if(mentor)mentor.settings=result;
  const notice=document.querySelector('[data-host-result]');if(notice)notice.textContent=next?'Saved. Stepstone will keep running after the browser closes.':'Saved. Stepstone will stop about 3 minutes after all pages stop checking in.';
 }catch(error){toggle.checked=!next;const notice=document.querySelector('[data-host-result]');if(notice)notice.textContent=errorText(error);else toast(errorText(error));}
 finally{working=false;if(toggle.isConnected)toggle.disabled=!mentor?.settings?.canManageHost;}
});

dialog.addEventListener('close',()=>{if(document.getElementById('delivered-card-code'))$('#dialog-content').replaceChildren();});
