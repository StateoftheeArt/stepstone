import {numberValue} from './engine.js?build=123';

export const freshTour=()=>({version:2,events:[],count:4,bagChecked:false,answer:'',answerChecked:false,hint:false});

// Keep the saved event contract while removing the obsolete break exercise.
export function continueSavedTour(config,data){
  evaluateTour(config,data);
  const actions=data.version===2?config.setupActions:config.actions;
  let next=data;
  while(['pause','resume'].includes(actions[next.events.length]))next={...next,events:[...next.events,{action:actions[next.events.length]}]};
  return next;
}

// Mirrored in tutorial.py. A complete flag from a client is never trusted.
export function evaluateTour(config,data){
  if(!data||![1,2].includes(data.version)||!Array.isArray(data.events))throw Error('Please reopen your saved tour.');
  const actions=data.version===2?config.setupActions:config.actions;
  if(data.events.length>actions.length)throw Error('Please follow the tour one step at a time.');
  const events=data.events.map((event,index)=>{
    if(!event||event.action!==actions[index])throw Error('Please follow the tour one step at a time.');
    const clean={action:event.action};
    if(event.action==='pack'){
      if(!Number.isInteger(event.value)||event.value!==config.target)throw Error('Match the bag to the order, then check it.');
      clean.value=event.value;
    }
    if(event.action==='answer'){
      if(typeof event.value!=='string'||event.value.length>80||numberValue(event.value)!==config.question.answer)throw Error('Use the helpful step, then check the practice answer.');
      clean.value=event.value;
    }
    if(event.action==='mentor'){
      if(!['connected','device'].includes(event.value))throw Error('Choose how to save your learning.');
      clean.value=event.value;
    }
    if(event.action==='goal'){
      if(!['core-card-everyday','card-exchange','core-laptop'].includes(event.value))throw Error('Choose your reward goal.');
      clean.value=event.value;
    }
    return clean;
  });
  const count=data.count===undefined?4:data.count,answer=data.answer===undefined?'':data.answer;
  if(!Number.isInteger(count)||count<0||count>12||typeof answer!=='string'||answer.length>120)throw Error('Please check your practice answer.');
  for(const flag of ['bagChecked','answerChecked','hint'])if(data[flag]!==undefined&&typeof data[flag]!=='boolean')throw Error('Please reopen your saved tour.');
  const clean={version:data.version,events,count,answer,bagChecked:!!data.bagChecked&&count===config.target,answerChecked:!!data.answerChecked&&answer.length<=80&&numberValue(answer)===config.question.answer,hint:!!data.hint};
  return {data:clean,result:{step:events.length,total:actions.length,complete:events.length===actions.length}};
}

export function tourRoute(action){return ['open'].includes(action)?'#path/math':['start','example','pack','answer','pause','resume','wins'].includes(action)?'#lesson/math-1':action==='rewards'?'#progress':['comfort','profile','mentor','goal'].includes(action)?'#progress/rewards':'#home';}
