import {extendedStartingPoint} from './starting-replay.js?build=122';
// Small, dependency-free helpers shared by the learner interface and its tests.
export function newId(){
  const b=crypto.getRandomValues(new Uint8Array(16));b[6]=(b[6]&15)|64;b[8]=(b[8]&63)|128;
  const h=Array.from(b,v=>v.toString(16).padStart(2,'0')).join('');
  return `${h.slice(0,8)}-${h.slice(8,12)}-${h.slice(12,16)}-${h.slice(16,20)}-${h.slice(20)}`;
}
export function escapeHTML(value='') { return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
// Everyday formats: $10, 10 CAD, 10 dollars, 25%, 10,000 or 10 000. Matches placement.py plain_number.
export function plainNumber(value){
  let s=String(value).trim().replaceAll('−','-').replace(/^([+-]?)\s*(?:CAD|C\$|\$)\s*/i,'$1').replace(/\s*(?:CAD|\$|%|dollars?)$/i,'');
  if(/^[+-]?[0-9]{1,3}(?:(?:,[0-9]{3})+|(?:[ \u00a0\u202f][0-9]{3})+)(?:\.[0-9]*)?$/.test(s))s=s.replace(/[, \u00a0\u202f]/g,'');
  return s;
}
export function numberValue(value) {
  const s=plainNumber(value);
  if(!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:\s*\/\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+))?$/.test(s))return null;
  const parts=s.split('/').map(Number),n=parts.length===2?parts[0]/parts[1]:parts[0];return Number.isFinite(n)?n:null;
}
export function correct(question,answer){
  if(question.kind==='choice')return String(answer)===question.answer;
  const value=numberValue(answer);return value!==null&&Math.abs(value-question.answer)<=Math.max(1e-9,Math.abs(question.answer)*1e-6);
}
export function sample(items,count){
  const unique=[...new Map(shuffle(items).map(x=>[x.caseId||JSON.stringify([x.passage||'',x.prompt]),x])).values()];
  for(let i=unique.length-1;i>0;i--){const bits=new Uint32Array(1);crypto.getRandomValues(bits);const j=bits[0]%(i+1);[unique[i],unique[j]]=[unique[j],unique[i]];}
  return unique.slice(0,count).map(q=>q.options?{...q,options:shuffle(q.options)}:q);
}
export function shuffle(items){const out=[...items];for(let i=out.length-1;i>0;i--){const bits=new Uint32Array(1);crypto.getRandomValues(bits);const j=bits[0]%(i+1);[out[i],out[j]]=[out[j],out[i]];}return out;}
export function mastery(attempts=[]){const units=new Set();for(const a of attempts)if(a.report?.passed)units.add(a.unit);return units;}
export function reviewDue(attempts=[],now=Date.now()/1000){
  const latest=new Map();for(const a of attempts){if(!latest.has(a.unit)||a.finished>latest.get(a.unit).finished)latest.set(a.unit,a);}
  return [...latest.values()].filter(a=>!a.report.passed||now-a.finished>=7*86400);
}
export function mergeStages(local={},remote={}){const out={...local};for(const [id,stage] of Object.entries(remote))out[id]={...(out[id]||{}),phase:out[id]?.phase??Math.min(5,stage)};return out;}
export function readable(text){return String(text).replace(/\$([^$]+)\$/g,(_,tex)=>tex.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g,'$1 divided by $2').replace(/\\times/g,' times ').replace(/\\div/g,' divided by ').replace(/\\square/g,'blank').replace(/\\sqrt\{([^{}]+)\}/g,' square root of $1 ').replace(/\\%/g,' percent ').replace(/\^2/g,' squared ').replace(/\\[a-z]+/gi,' ').replace(/[{}]/g,'')).replace(/\s+/g,' ');}

// Replayed by placement.py. Suggestions never award mastery or reward points.
export function startingQuestion(bank,data,id){return ((data?.version||1)===1?(bank.legacy||bank):data?.version===5?bank.foundation:data?.version===4?bank.extended:bank).questions.find(q=>q.id===id);}
export function startingPoint(bank,data){
  if(!data)return null;
  const version=data.version??1;
  if(![1,2,3,4,5].includes(version)||!Number.isInteger(data.age)||data.age<5||data.age>99||!Number.isInteger(data.seed)||data.seed<0||data.seed>65535||!Array.isArray(data.answers)||data.answers.length>({1:10,2:36,3:24,4:48,5:24}[version]))throw new Error('Please reopen your saved starting check.');
  if(version===1)return legacyStartingPoint(bank.legacy||bank,data);
  const result=version>=4?extendedStartingPoint(version===5?bank.foundation:bank.extended,data,numberValue,version):adaptiveStartingPoint(bank,data);
  if('draft' in data){
    const d=data.draft,q=startingQuestion(bank,data,result.next);
    if(!d||!q||d.id!==q.id||!('answer' in d)||typeof(d.heard??false)!=='boolean'||(d.answer!==null&&(q.kind==='number'?typeof d.answer!=='string'||d.answer.length>80:!Number.isInteger(d.answer)||d.answer<0||d.answer>=q.options.length)))throw new Error('That saved answer belongs to a different question.');
  }
  if('writing' in data){
    const w=data.writing;
    if(!result.questionsDone||!w||!['draft','submitted','skipped'].includes(w.status)||typeof w.text!=='string'||w.text.length>1000||!['myself','person','tool','mixed'].includes(w.support??'myself')||typeof(w.heard??false)!=='boolean'||w.status==='submitted'&&!w.text.trim())throw new Error('Write a short message, or choose “Not ready to write yet”.');
  }
  return result;
}
function legacyStartingPoint(bank,data){
  const levels={},evidence=[];
  let firstCorrect=false;
  for(let index=0;index<=10;index++){
    if(index===10)return {complete:true,levels,average:Math.floor(Object.values(levels).reduce((a,b)=>a+b,0)/5+.5),evidence,next:null};
    const subject=bank.subjects[Math.floor(index/2)],grade=index%2===0?6:firstCorrect?9:3;
    const variants=bank.questions.filter(q=>q.subject===subject&&q.grade===grade);
    const question=variants[(data.seed+index)%variants.length];
    if(index===data.answers.length)return {complete:false,levels,average:null,evidence,next:question.id};
    const item=data.answers[index];
    if(!item||item.id!==question.id||!Number.isInteger(item.answer)||item.answer< -1||item.answer>=question.options.length||typeof(item.heard??false)!=='boolean')throw new Error('Please reopen your saved starting check.');
    const right=item.answer===question.answer;
    evidence.push({id:question.id,subject,grade,answer:item.answer,correct:right,heard:item.heard||false});
    if(index%2===0)firstCorrect=right;
    else levels[subject]=firstCorrect?(right?10:7):(right?4:1);
  }
}

function adaptiveStartingPoint(bank,data){
  const levels={},areas={},evidence=[];let cursor=0;
  const fixed=data.version===3,limit=fixed?4:6;
  for(const [section,subject] of bank.subjects.entries()){
    let band=1,confirmed=-1;
    const asked=[0,0,0,0],hits=[0,0,0,0],misses=[0,0,0,0],failed=new Set(),details=[];
    for(let step=0;step<limit;step++){
      const variants=bank.questions.filter(q=>q.subject===subject&&q.band===band);
      const question=variants[(data.seed+section*7+band+asked[band])%variants.length];
      if(cursor===data.answers.length)return{complete:false,questionsDone:false,levels,areas,evidence,next:question.id,section:subject,sectionIndex:section,questionInSection:step+1};
      const item=data.answers[cursor];
      if(!item||item.id!==question.id||!('answer' in item)||typeof(item.heard??false)!=='boolean')throw new Error('That answer does not match the next question. Reload your saved check.');
      const answer=item.answer,unsure=answer===null;let right=false;
      if(!unsure){
        if(question.kind==='number'){
          const value=typeof answer==='string'&&answer.length<=80?numberValue(answer):null;
          if(value===null)throw new Error('Enter a number, decimal or fraction, or choose “I don’t know yet”.');
          right=Math.abs(value-question.answer)<=Math.max(1e-9,Math.abs(question.answer)*1e-6);
        }else{
          if(!Number.isInteger(answer)||answer<0||answer>=question.options.length)throw new Error('Choose one of the answers shown.');
          right=answer===question.answer;
        }
      }
      const detail={id:question.id,subject,band,answer,correct:right,unsure,heard:item.heard??false};
      details.push(detail);evidence.push(detail);cursor++;asked[band]++;hits[band]+=Number(right);misses[band]+=Number(!right);
      let done=false;
      if(hits[band]>=2){confirmed=Math.max(confirmed,band);done=band===3||failed.has(band+1);if(!done)band++;}
      else if(misses[band]>=2){failed.add(band);done=confirmed>=0||band===0;if(!done)band--;}
      if((done&&!fixed)||step===limit-1){
        const level=bank.starts[subject][Math.max(0,confirmed)];levels[subject]=level;
        areas[subject]={level,confirmedBand:confirmed,answered:details.length,matched:details.filter(d=>d.correct).length,unsure:details.filter(d=>d.unsure).length,heard:details.filter(d=>d.heard).length,basis:confirmed<0?'support':done&&!fixed?'steady':'check-in'};
        break;
      }
    }
  }
  if(cursor!==data.answers.length)throw new Error('This starting check already has all its answers.');
  return{complete:fixed||['submitted','skipped'].includes(data.writing?.status),questionsDone:true,levels,areas,evidence,next:null,section:null,sectionIndex:bank.subjects.length,questionInSection:0};
}

export function rewardGoal(me){
  if(!me?.goal)return null;
  const reward=me.rewards?.find(r=>r.id===me.goal&&r.kind==='mentor');
  if(!reward)return null;
  const claim=me.claims?.find(c=>reward.milestone?c.id===reward.claim_id:c.reward===reward.id);
  return {...reward,claim,...rewardEligibility(reward,me)};
}
export function rewardEligibility(reward,me){
  const mastered=new Set(me?.mastered||[]),required=reward.required_modules||[];
  const missing=required.filter(id=>!mastered.has(id));
  const modulesRemaining=Math.max(0,(reward.minimum_modules||0)-mastered.size);
  const remaining=Math.max(0,reward.cost-(me?.points||0)),unavailable=reward.available===0||!!(reward.milestone&&!reward.confirmed);
  return {missing,modulesRemaining,remaining,unavailable,ready:!missing.length&&!modulesRemaining&&!remaining&&!unavailable};
}
