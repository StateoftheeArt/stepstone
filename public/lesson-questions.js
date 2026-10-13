import {sample} from './engine.js?build=119';

export function questionKey(question){
  return `${question.passage||''} ${question.prompt}`.normalize('NFKC').replace(/\s+/g,' ').trim().toLowerCase();
}
export function practicePool(unit,phase,draft={}){
  const used=new Set((unit.mission?.labs||[]).flat().filter(q=>q.prompt).map(questionKey));
  for(const [savedPhase,round] of Object.entries(draft.rounds||{})){
    if(Number(savedPhase)===phase)continue;
    for(const question of round.questions||[])used.add(questionKey(question));
  }
  const lesson=phase===2?1:2,unique=new Map();
  for(const question of unit.practice){
    const key=questionKey(question);
    if((!question.lesson||question.lesson===lesson)&&!used.has(key)&&!unique.has(key))unique.set(key,question);
  }
  return [...unique.values()];
}
export function practiceRound(unit,phase,draft){
  if(draft.rounds[phase]){
    const current=new Map(unit.practice.map(q=>[q.id,q]));
    for(const saved of draft.rounds[phase].questions||[]){
      const revised=current.get(saved.id);
      // Wording fixes can reach a resumed round without changing what its
      // answers mean. Preserve saved ordering, responses and feedback.
      const choices=q=>JSON.stringify((q.options||[]).map(o=>[o.id,o.text]).sort((a,b)=>String(a[0]).localeCompare(String(b[0]))));
      if(revised&&saved.kind===revised.kind&&JSON.stringify(saved.answer)===JSON.stringify(revised.answer)&&choices(saved)===choices(revised)){
        for(const key of ['prompt','passage','hint','explanation']){
          if(key in revised)saved[key]=revised[key];else delete saved[key];
        }
      }
    }
    return draft.rounds[phase];
  }
  const questions=sample(practicePool(unit,phase,draft),3);
  return draft.rounds[phase]={questions,answers:{},checks:{},last:{},tries:0,hints:{}};
}
