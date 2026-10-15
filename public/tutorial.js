import {createLessonAdvance} from './lesson-feedback.js?build=122';
import {escapeHTML as esc,numberValue} from './engine.js?build=122';
import {missionIntro,missionLesson,missionPractice,mountOrderLab,showMissionPane} from './mission.js?build=122';
import {freshTour,evaluateTour,tourRoute,continueSavedTour} from './tutorial-state.js?build=122';
import {createTourGuide} from './tutorial-guide.js?build=122';

export function createTutorial(c){
  let config,record,flight,timer,saved=true,shown=false,breakOpen=false,comfortOpen=false,finishing=false,launching=false;
  const transition=createLessonAdvance(),pointer=createTourGuide({root:c.root,dialog:c.dialog,guidePet:c.guidePet,readButton:c.readButton});
  const owner=()=>c.me()?.id||c.guestOwner();
  const key=()=> 'stepstone-tutorial-v1-'+owner();
  const state=()=>config&&record?evaluateTour(config,record.data).result:{step:0,total:20,complete:false};
  const bypassed=()=>!!c.me()?.personal&&!!record?.result?.skipped;
  const done=()=>bypassed()||state().complete;
  const stage=()=>done()?'done':config.setupActions[state().step];
  const dirty=()=>!!c.me()&&!!record?._dirty;
  const locked=()=>!!config&&(!done()||!!c.me()&&!c.me().tutorial?.result.complete);
  const early=()=>locked()&&['welcome','questions','celebrate','points'].includes(stage());
  const visible=()=>!['mentor','join','resume'].includes(c.route())&&((locked()&&!early())||finishing);
  const has=action=>record?.data.events.some(e=>e.action===action);
  const bonus=()=>c.me()?((c.me().welcomeAwards?.starting?5:0)+(c.me().welcomeAwards?.tutorial?5:0)):((record?.awards?.starting?5:0)+(record?.awards?.tutorial?5:0));
  function saveLocal(){
    try{localStorage.setItem(key(),JSON.stringify(record));saved=true;}
    catch{saved=false;c.toast('Keep this page open. This browser could not save your place.');}
    return saved;
  }
  function load(){
    if(!config)return;
    transition.cancel();clearTimeout(timer);breakOpen=comfortOpen=finishing=false;
    try{record=JSON.parse(localStorage.getItem(key())||'null');if(record)evaluateTour(config,record.data);}catch{record=null;}
    const remote=c.me()?.tutorial;
    if(remote&&!record?._dirty&&remote.revision>=(record?.revision||0))record={...structuredClone(remote),awards:record?.awards,profileDraft:record?.profileDraft};
    record??={revision:0,data:freshTour()};
    if(record.data.version===1&&!state().complete){record.data=freshTour();record._dirty=!!c.me();}
    record.awards??={starting:false,tutorial:false};
    const result=c.starting();
    if(record.data.version===2&&result?.complete&&stage()==='welcome'){
      record.data.events=[{action:'welcome'},{action:'questions'}];record.awards.starting=true;record._dirty=!!c.me();
    }else if(record.data.version===2&&result?.complete&&stage()==='questions'){
      record.data.events.push({action:'questions'});record.awards.starting=true;record._dirty=!!c.me();
    }else if(record.data.version===2&&c.hasStartingAnswers()&&stage()==='welcome'){
      record.data.events=[{action:'welcome'}];record._dirty=!!c.me();
    }
    const continued=continueSavedTour(config,record.data);if(continued!==record.data){record.data=continued;record._dirty=!!c.me();}
    saveLocal();
  }
  function persist(){record._dirty=!!c.me();saveLocal();clearTimeout(timer);if(c.me())timer=setTimeout(()=>sync(),400);updateStatus();updateGuide();}
  async function sync(){
    if(flight){await flight;return sync();}
    if(!dirty()||record._conflict)return;
    const who=owner(),current=record,content=JSON.stringify(record.data);
    flight=(async()=>{
      try{
        const remote=await c.api('/api/tutorial',{learner:who,revision:current.revision||0,data:current.data});
        if(owner()!==who||record!==current)return;
        current.revision=remote.revision;current.result=remote.result;current.updated=remote.updated;
        current._dirty=JSON.stringify(current.data)!==content;delete current._error;
        c.me().tutorial=remote;c.remember();saveLocal();
        if(remote.result.complete)await c.refreshAccount();
      }catch(error){if(owner()===who&&record===current){current._error=error.message;current._conflict=error.status===409;saveLocal();}}
    })();
    try{await flight;}finally{flight=null;updateStatus();}
  }
  function add(action,value,paint=true){
    if(record._conflict||stage()!==action)return false;
    record.awards??={starting:false,tutorial:false};
    const event={action};if(value!==undefined)event.value=value;
    const next={...record.data,events:[...record.data.events,event]};
    evaluateTour(config,next);record.data=continueSavedTour(config,next);transition.cancel();
    if(action==='questions')record.awards.starting=true;
    if(action==='finish'){record.newTutorialAward=!(c.me()?.welcomeAwards?.tutorial||record.awards.tutorial);record.awards.tutorial=true;}
    persist();
    if(paint)c.navigate(tourRoute(stage()));
    return true;
  }
  function canonical(hash){
    if(!locked()||/^#(?:mentor|join|resume)(?:\/|$)/.test(hash))return hash;
    return early()?'#home':tourRoute(stage());
  }
  const links={learn:'#path',open:'#lesson/math-1',wins:'#progress',rewards:'#progress/rewards'};
  function decorateNav(){
    const gate=locked()&&!['mentor','join','resume'].includes(c.route());
    document.documentElement.classList.toggle('tour-locked',gate);
    document.querySelectorAll('#navigation a,.rewards-jump,.reward-subnav a').forEach(a=>{
      const available=!gate||a.getAttribute('href')===links[stage()];
      a.toggleAttribute('inert',!available);
      if(!available){a.setAttribute('aria-disabled','true');a.setAttribute('tabindex','-1');a.title='We will visit this during setup';}
      else{a.removeAttribute('aria-disabled');a.removeAttribute('tabindex');a.removeAttribute('title');}
    });
  }
  const guides={
    home:['This is your Home','Home shows your next lesson and saved activity. Explore the controls before you begin.','[data-tour="home"]','Start your guided tour','Follow one step at a time.'],
    learn:['Find your lessons','Learn organises your modules by subject. Select Learn in the menu.','#navigation a[href="#path"]','Tap Learn','This opens your modules.'],
    open:['Open a module','Each module develops a practical skill. Try this training version to explore the controls.','.path-unit a','Open Pack the order','This training copy will not change a lesson score.'],
    start:['Explore the task','First, see what you will do and why it is useful. Then start the activity.','[data-action="advance"]','Tap Take the order','Let’s try the controls.'],
    example:['Ask to see an example','Show me how explains each step. Return to the example whenever you need guidance.','[data-action="mission-example"]','Tap Show me how','See it before trying it.'],
    pack:['Try the activity','The order needs 7 cartons. Move 3 more from the shelf into the bag.','[data-pack="add"]','Add 3 cartons','Tap, or drag a carton into the bag.'],
    answer:['Type an answer','Two cartons and one more make three. Type 3, then check your answer.','input[data-answer]','Type 3 here','A correct answer moves you to the next part.'],
    pause:['Try a break','You can pause. Your place stays saved. Try the break button now.','[data-action="pause"]','Tap Take a break','You will come back to this step.'],
    resume:['Come back','You do not have to start again. Return to the place you saved.','[data-tour="resume"]','Resume your tour','Your work is waiting.'],
    wins:['Find your wins','Rewards starts with your completed learning and feedback. Open Rewards now.','#navigation a[href="#progress"]','Tap Rewards','Your starting questions have earned 5 Steps.'],
    rewards:['Explore your reward goals','Your wins come first. Continue down the page to see your reward goals.','.rewards-jump','View rewards','Both are kept together in Rewards.'],
    comfort:['Reading & comfort','Open My profile, then Reading & comfort.','#profile-slot .companion-profile','Open My profile','Choose your reading tools.'],
    profile:['Choose your Pip','Choose your Pip and the name your mentor will see.','input[name="alias"]','Name your Pip','This name and Pip identify you to your mentor.'],
    mentor:['Connect your mentor','Your mentor can see your finished work and help with rewards. Choose how you want to save.','[data-mentor-step]','Choose your connection','Your age and learning records are shared only with your mentor.'],
    goal:['Choose something to work towards','Pick a first reward goal. You can change it later. A goal does not reserve a reward.','[data-goal-choices]','Choose your goal','Real rewards need mentor approval and funding.'],
    finish:['Start from your plan','Your guide ends here. Start the lesson suggested by your starting questions.','[data-tour="finish"]','Start from my plan','Your first lesson will help you check the fit.']
  };
  function guidance(){
    const action=stage(),base=guides[action]||guides.finish;
    const g={heading:base[0],text:base[1],selector:base[2],title:base[3],detail:base[4],key:state().step,number:Math.max(1,config.setupActions.slice(4,state().step+1).filter(a=>!['pause','resume'].includes(a)).length),total:config.setupActions.slice(4).filter(a=>!['pause','resume'].includes(a)).length,reveal:!['profile','mentor','goal','home'].includes(action),motion:c.motion()};
    if(action==='comfort'&&c.dialog.open)return {...g,selector:'#comfort-control',title:'Reading & comfort',detail:'Close your profile when you are ready.'};
    if(action==='resume'&&breakOpen&&c.dialog.open)return {...g,breakStep:true,title:'Come back to your tour',detail:'Tap Back to what I was doing.'};
    if(action==='pack'){
      if(record.exampleOpen)return {...g,heading:'Watch the example',text:'Read the example, then return to the activity.',selector:'#lesson-copy > [data-action="mission-try"]',title:'Read, then try it',detail:'The button is after the example.',tone:'example',reveal:false};
      if(record.data.bagChecked)return {...g,selector:'[data-action="mission-next"]',title:'Correct! Next is ready',text:'The bag matches the order.',detail:'Choose Next when you are ready to continue.',tone:'success'};
      if(record.data.count===config.target)return {...g,selector:'[data-pack="check"]',title:'Check the bag',text:'You have 7 cartons. Check your work.',detail:'Tap Check the bag.'};
      if(record.data.count>config.target)return {...g,selector:'[data-pack="remove"]',title:'Take out '+(record.data.count-config.target),text:'There are too many. Remove cartons until there are 7.',detail:'Tap the bag to take one out, or drag it back to the shelf.'};
      g.title='Add '+(config.target-record.data.count)+' more';
    }
    if(action==='answer'&&record.data.answerChecked)return {...g,selector:'[data-action="mission-next"]',title:'Correct! Next is ready',text:'You checked the answer. Choose Next when you are ready.',detail:'Choose Next when you are ready to continue.',tone:'success'};
    if(action==='answer'&&record.data.answer.trim())return {...g,selector:'[data-action="check"]',title:'Check your answer'};
    if(action==='profile'&&c.profile().introReady)return {...g,heading:'Your saved profile',text:'You already chose your name and companion. Keep them or edit your profile.',selector:'[data-tour="profile-confirm"]',title:'Keep your profile',detail:'You can change it again later.'};
    if(record?._conflict)return {...g,selector:'[data-tour="reload"]',title:'Load your saved setup',detail:'Another device has a newer copy.'};
    return g;
  }
  function updateGuide(){
    if(!shown)return;
    if(finishing||['finish','done'].includes(stage())){pointer.hide();return;}
    if(stage()==='goal'||stage()==='profile'&&c.root.querySelector('form[data-form=profile]')){pointer.hide();return;}
    const g=guidance();c.root.dataset.tourTone=g.tone||'action';pointer.show(g);
  }
  const guideStatus=()=>'<div data-tour-status role="status"></div>';
  function updateStatus(){
    const target=c.root.querySelector('[data-tour-status]');if(!target)return;
    target.innerHTML=record?._conflict?'<p class="notice">This setup changed on another device.</p><button class="btn" data-tour="reload">Load my saved setup</button>':!saved?'<p class="error-text">Keep this page open. Your place could not be saved.</p>':record?._error?'<p class="error-text">'+esc(record._error)+'</p>':'';
    if(record?._conflict)c.root.querySelectorAll('input,button:not([data-tour="reload"]):not([data-action="read"]):not([data-action="pause"])').forEach(el=>el.disabled=true);
  }
  function render(){
    c.stopReading();pointer.prepare();shown=true;c.root.dataset.tutorial='true';
    if(finishing||stage()==='done'||stage()==='finish'){
      c.root.innerHTML=guideStatus()+c.startingPlan(locked()&&state().complete?'sync':'finish',guidance());
      pointer.hide();
      decorateNav();updateStatus();c.transition?.('guide/final-plan');return;
    }
    const action=stage(),u=c.catalog().units.find(u=>u.id===config.unit);
    if(action==='home'){c.home();const plan=c.root.querySelector('.starting-plan-card');(plan||c.root).insertAdjacentHTML(plan?'beforeend':'afterbegin',guideStatus()+'<div class="tour-start"><button class="btn" data-tour="home">Take the guided tour →</button></div>');}
    else if(action==='rewards'){c.wins();c.root.insertAdjacentHTML('afterbegin',guideStatus());}
    else{
      c.root.innerHTML=guideStatus()+'<div class="tour-surface mission-content"></div>';
      const host=c.root.querySelector('.tour-surface');
      if(action==='learn')host.innerHTML='<section class="card"><h2>Your subjects live in Learn.</h2><p>Math, reading & writing, science, digital & work, and life skills. We’ll find the right place for you in each area.</p></section>';
      else if(action==='open')host.innerHTML='<div class="path-grid tour-training-card">'+c.unitCard(u,new Set(),u.id)+'</div>';
      else if(action==='start')host.innerHTML=missionIntro({...u,mission:{...u.mission,brief:['See an example, then pack 7 cartons.','Try one guided answer. This is not a test.']}},c.readButton);
      else if(['example','pack'].includes(action)){
        host.innerHTML=missionLesson(u,1,c.html,c.readButton);
        const d={orderLab:{1:{count:record.data.count,checked:record.data.bagChecked}}};
        mountOrderLab({host:host.querySelector('#mission-lab'),phase:1,draft:d,html:c.html,save:()=>{record.data.count=d.orderLab[1].count;record.data.bagChecked=d.orderLab[1].checked&&record.data.count===config.target;persist();},onEdit:cancel,onCorrect:()=>schedule()});
        if(action==='example')host.querySelectorAll('[data-pack]').forEach(el=>el.disabled=true);
        if(record.exampleOpen)showMissionPane(c.root,true,false);
      }else if(action==='answer'){
        const q=config.question,d=record.data,round={questions:[q],answers:{[q.id]:d.answer},checks:{[q.id]:d.answerChecked},hints:{[q.id]:d.hint},last:d.answerChecked?{[q.id]:d.answer}:{},tries:0};
        host.innerHTML=missionPractice(u,round,c.questionCard,c.html);
      }else if(action==='resume')host.innerHTML='<section class="card"><h2>Your place is waiting.</h2><button class="btn" data-tour="resume">Resume tour →</button></section>';
      else if(action==='pause'||action==='wins')host.innerHTML='<section class="card"><h2>'+guidance().heading+'</h2><p>'+guidance().text+'</p></section>';
      else if(action==='comfort')host.innerHTML=c.rewardIntro();
      else if(action==='profile')host.innerHTML=c.profile().introReady?'<section class="card"><h2>Your profile is already yours.</h2><p>'+esc(c.profile().alias||'Pip')+'</p><button class="btn" data-tour="profile-confirm">Keep my profile & continue →</button><button class="btn secondary" data-action="profile">Edit my profile</button></section>':c.profileForm(record.profileDraft);
      else if(action==='mentor')host.innerHTML=c.mentorStep();
      else if(action==='goal')host.innerHTML='<div class="tour-form-intro"><p class="eyebrow">STEP '+guidance().number+' OF '+guidance().total+'</p><h1>Choose your first goal</h1><p>Save a goal, then return to Home to begin your starting plan.</p></div>'+c.goalForm();
      else host.innerHTML='<button class="btn" data-tour="finish">Finish setup →</button>';
    }
    decorateNav();updateStatus();updateGuide();c.transition?.('guide/'+state().step);
  }
  function cancel(){transition.cancel();}
  function schedule(){
    const current=record,who=owner(),action=stage(),answer=record.data.answer;
    const valid=()=>visible()&&current===record&&who===owner()&&stage()===action&&!document.hidden&&!c.dialog.open&&!record._conflict&&(action==='pack'?record.data.bagChecked&&record.data.count===config.target:record.data.answerChecked&&record.data.answer===answer);
    const success=c.root.querySelector('[data-mission-success]');
    transition.schedule(valid,next,success,c.motion());
  }
  function next(){cancel();if(stage()==='pack'&&record.data.bagChecked)add('pack',record.data.count);else if(stage()==='answer'&&record.data.answerChecked)add('answer',record.data.answer);}
  async function finishSetup(){
    if(launching||stage()!=='finish'&&!finishing)return;
    const current=record,who=owner();launching=true;
    try{
      if(stage()==='finish')add('finish',undefined,false);
      finishing=true;if(!saved)saveLocal();await sync();
      if(current!==record||who!==owner())return;
      if(locked()||!saved){c.navigate('#home');return;}
      finishing=false;shown=false;pointer.hide();c.beginPlan();
    }finally{launching=false;}
  }
  async function action(name){
    if(name==='reload'){const fresh=await c.refreshAccount();record=structuredClone(fresh.tutorial||{revision:0,data:freshTour()});saveLocal();load();c.navigate(canonical('#home'));return;}
    if(name==='sync'){await finishSetup();return;}
    if(name==='launch'){if(!locked()){finishing=false;shown=false;pointer.hide();c.beginPlan();}return;}
    if(record._conflict)return;
    if(['home','resume','welcome','celebrate','points'].includes(name)){add(name);return;}
    if(name==='profile-confirm'){if(c.profile().introReady)add('profile');return;}
    if(name==='mentor-device'){add('mentor','device');return;}
    if(name==='mentor-connected'){add('mentor','connected');return;}
    if(name==='finish'){await finishSetup();return;}
    if(name==='advance'){add('start');return;}
    if(name==='mission-example'){record.exampleOpen=true;add('example',undefined,false);c.render();return;}
    if(name==='mission-try'){record.exampleOpen=false;saveLocal();showMissionPane(c.root,false,c.motion());updateGuide();return;}
    if(name==='mission-next'){next();return;}
    if(name==='mission-hold'){cancel();c.root.querySelector('[data-action="mission-hold"]')?.setAttribute('hidden','');c.root.querySelector('[data-action="mission-next"]')?.focus({preventScroll:true});return;}
    if(name==='hint'||name==='back-lesson'){cancel();record.data.hint=true;persist();c.render();return;}
    if(name==='locate'){document.querySelector(guidance().selector)?.scrollIntoView({block:'center',behavior:c.motion()?'smooth':'instant'});return;}
    if(name==='check'&&stage()==='answer'){
      cancel();const input=c.root.querySelector('input[data-answer]'),value=input.value;
      if(!value.trim()){c.root.querySelector('.feedback').textContent='Type 3, then check your answer.';input.focus();return;}
      record.data.answer=value;record.data.answerChecked=value.length<=80&&numberValue(value)===config.question.answer;
      if(!record.data.answerChecked)record.data.hint=true;persist();c.render();
      if(record.data.answerChecked)schedule();
      else{c.root.querySelector('.feedback').textContent='Try 3. Two cartons and one more make three.';c.root.querySelector('input[data-answer]').focus();}
    }
  }
  document.addEventListener('click',event=>{
    const button=event.target.closest('button'),link=event.target.closest('a[href]');
    if(button?.dataset.tour&&(visible()||early())){event.preventDefault();event.stopImmediatePropagation();action(button.dataset.tour).catch(e=>c.toast(e.message));return;}
    if(!locked())return;
    if(link&&!c.dialog.contains(link)){
      const hash=link.getAttribute('href');
      if(!hash.startsWith('#')||hash==='#main'||/^#(?:mentor|join|resume)(?:\/|$)/.test(hash))return;
      if(visible()&&hash===links[stage()]&&!record._conflict){event.preventDefault();event.stopImmediatePropagation();add(stage());return;}
      if(!['mentor','join','resume'].includes(c.route())){event.preventDefault();event.stopImmediatePropagation();cancel();c.toast('We will get there. Finish this setup step first.');c.navigate(canonical('#home'));return;}
    }
    if(!button||button.disabled||!visible())return;
    if(c.dialog.contains(button))return;
    const name=button.dataset.action;
    if(['advance','mission-example','mission-try','mission-next','mission-hold','hint','check','back-lesson'].includes(name)){event.preventDefault();event.stopImmediatePropagation();action(name).catch(e=>c.toast(e.message));return;}
    if(name==='comfort'&&stage()==='comfort')comfortOpen=true;
    if(['read','comfort','account','pause','stop-reading','profile','messages'].includes(name))cancel();
    else if(name&&c.root.contains(button)&&button.type!=='submit'){event.preventDefault();event.stopImmediatePropagation();c.toast('Follow the next highlighted step.');}
  },true);
  document.addEventListener('input',event=>{
    if(!visible()||!event.target.matches('input[data-answer]'))return;
    event.stopImmediatePropagation();cancel();record.data.answer=event.target.value;record.data.answerChecked=false;persist();
    c.root.querySelector('[data-mission-success]').hidden=true;c.root.querySelector('[data-action="mission-next"]').disabled=true;c.root.querySelector('[data-action="mission-hold"]').hidden=true;
    c.root.querySelector('.question').classList.remove('correct');c.root.querySelector('.feedback').textContent='';
  },true);
  document.addEventListener('keydown',event=>{
    if(visible()&&event.key==='Enter'&&event.target.matches('input[data-answer]')){event.preventDefault();event.stopImmediatePropagation();action('check').catch(e=>c.toast(e.message));}
  },true);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)cancel();});
  new MutationObserver(()=>{if(shown)updateGuide();}).observe(c.dialog,{attributes:true,attributeFilter:['open']});

  c.dialog.addEventListener('close',()=>{
    if(breakOpen){breakOpen=false;if(stage()==='resume')add('resume');}
    if(comfortOpen||stage()==='comfort'&&c.dialog.querySelector('[data-profile-panel=reading]')){comfortOpen=false;if(stage()==='comfort')add('comfort');}
    if(shown)updateGuide();
  });
  return {
    configure(v){config=v;},load,locked,visible,early,done,stage,dirty,canonical,decorateNav,render,sync,cancel,bonus,action,
    questionsComplete(){if(stage()==='questions'&&c.starting()?.complete)add('questions');},
    profileSaved(){delete record.profileDraft;add('profile');},
    clearProfileDraft(){delete record.profileDraft;saveLocal();},
    saveProfileDraft(value){record.profileDraft=value;saveLocal();},
    async goalSaved(value){const current=record,who=owner();if(!add('goal',value,false))return;await sync();if(record===current&&owner()===who)c.navigate('#home');},
    export(){return structuredClone(record);},
    adopt(value){record={...value,revision:0,_dirty:!!c.me()};saveLocal();},
    replace(remote){record=structuredClone(remote);finishing=false;saveLocal();},
    refreshGuide:updateGuide,
    leaving(){shown=false;pointer.hide();delete c.root.dataset.tutorial;delete c.root.dataset.tourTone;},
    pause(){cancel();if(visible()&&stage()==='pause'){add('pause',undefined,false);breakOpen=true;}return saveLocal();},
    stop(){cancel();clearTimeout(timer);},flight:()=>flight,
    win(){return done()?'<section class="card tour-win"><span class="pill ready">✓ '+(bypassed()?'Mentor setup preview':'Guided setup complete')+'</span><p>'+ (bypassed()?'Tutorial skipped in your personal account. No new tutorial Steps were awarded.':record.data.version===2?bonus()+' welcome Steps saved. Each setup milestone earns 5 Steps once. Lesson scores are separate.':'Your earlier tour is saved. You can keep learning.')+'</p></section>':'';},
    mentor(learner){const t=learner.tutorial;return '<p class="small">Setup: '+(t?.result.complete?'complete':t?t.result.step+' of '+t.result.total+' steps saved':'not started')+'. Setup is not a skill score.</p>';}
  };
}
