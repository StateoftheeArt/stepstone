// Matches placement.py extended(). No awards, age weighting or reading penalty.
export function extendedStartingPoint(bank,data,numberValue,version=4){
  const levels={},areas={},suggestions={},evidence=[];let cursor=0;const bands=version===5?3:4,steps=version===5?6:8;
  for(const [section,subject] of bank.subjects.entries()){
    let band=version===5?0:1;const hits=Array(bands).fill(0),misses=Array(bands).fill(0),hitSkills=Array.from({length:bands},()=>new Set()),failed=new Set(),used=new Set(),skillAsked=new Map(),details=[];
    for(let step=0;step<steps;step++){
      const unused=bank.questions.filter(q=>q.subject===subject&&!used.has(q.id));
      let variants=unused.filter(q=>q.band===band);
      if(!variants.length){const nearest=[...unused].sort((a,b)=>Math.abs(a.band-band)-Math.abs(b.band-band)||a.band-b.band)[0].band;variants=unused.filter(q=>q.band===nearest);}
      const fewest=Math.min(...variants.map(q=>skillAsked.get(q.band+':'+q.skill)||0));
      variants=variants.filter(q=>(skillAsked.get(q.band+':'+q.skill)||0)===fewest);
      const question=variants[(data.seed+section*11+step)%variants.length];band=question.band;
      if(cursor===data.answers.length)return{version,complete:false,questionsDone:false,levels,areas,suggestions,evidence,next:question.id,section:subject,sectionIndex:section,questionInSection:step+1};
      const item=data.answers[cursor];
      if(!item||item.id!==question.id||!('answer' in item)||typeof(item.heard??false)!=='boolean')throw new Error('That answer does not match the next question. Reload your saved check.');
      const answer=item.answer,unsure=answer===null;let right=false;
      if(!unsure){if(question.kind==='number'){const value=typeof answer==='string'&&answer.length<=80?numberValue(answer):null;if(value===null)throw new Error('Enter a number, decimal or fraction, or choose “I don’t know yet”.');right=Math.abs(value-question.answer)<=Math.max(1e-9,Math.abs(question.answer)*1e-6);}else{if(!Number.isInteger(answer)||answer<0||answer>=question.options.length)throw new Error('Choose one of the answers shown.');right=answer===question.answer;}}
      const detail={id:question.id,subject,band,skill:question.skill,answer,correct:right,unsure,heard:item.heard??false};
      details.push(detail);evidence.push(detail);cursor++;used.add(question.id);
      const key=band+':'+question.skill;skillAsked.set(key,(skillAsked.get(key)||0)+1);hits[band]+=Number(right);misses[band]+=Number(!right);if(right)hitSkills[band].add(question.skill);
      if(misses[band]>=2){failed.add(band);const lower=Array.from({length:bands},(_,i)=>i).filter(i=>i<band&&!failed.has(i));band=lower.length?Math.max(...lower):0;}
      else if(hits[band]>=2&&hitSkills[band].size>=2&&hits[band]>misses[band]&&band<bands-1&&!failed.has(band+1)&&(version===4||!failed.has(band)))band++;
    }
    const steady=Array.from({length:bands},(_,i)=>!failed.has(i)&&hits[i]>=2&&hitSkills[i].size>=2&&hits[i]>misses[i]);
    const candidates=steady.map((_,i)=>i).filter(i=>steady[i]&&(version===4||steady.slice(0,i+1).every(Boolean))),confirmed=candidates.length?Math.max(...candidates):-1,level=bank.starts[subject][Math.max(0,confirmed)];
    levels[subject]=level;suggestions[subject]=bank.suggestions[subject][Math.max(0,confirmed)];
    areas[subject]={level,confirmedBand:confirmed,answered:steps,matched:details.filter(d=>d.correct).length,unsure:details.filter(d=>d.unsure).length,heard:details.filter(d=>d.heard).length,basis:confirmed<0?'support':'steady',bands:Array.from({length:bands},(_,i)=>i).map(i=>({band:i,matched:hits[i],revisit:misses[i],skills:hitSkills[i].size}))};
  }
  if(cursor!==data.answers.length)throw new Error('This starting check already has all its answers.');
  return{version,complete:['submitted','skipped'].includes(data.writing?.status),questionsDone:true,levels,areas,suggestions,evidence,next:null,section:null,sectionIndex:bank.subjects.length,questionInSection:0};
}
