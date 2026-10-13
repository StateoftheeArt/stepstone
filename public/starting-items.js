import {activeUnits,suggestedStart} from './curriculum.js?build=121';

export function startingItemUnits(catalog,result){
  if(!result?.complete)return [];
  return ['math','reading','science','life'].flatMap(subject=>{
    const chain=activeUnits(catalog,subject),start=suggestedStart(catalog,subject,result);
    const index=chain.findIndex(unit=>unit.id===start?.id);
    return index>0?chain.slice(0,index).map(unit=>unit.id):[];
  });
}

// Cosmetic milestones use unique skills; a later revisit cannot count twice.
export function previewStartingItems({storage,key,catalog,result,done=[],unlocks=[]}){
  let saved;try{saved=JSON.parse(storage.getItem(key)||'null');}catch{}
  const valid=new Set(activeUnits(catalog).map(unit=>unit.id));
  const units=new Set((Array.isArray(saved?.units)?saved.units:[]).filter(id=>valid.has(id)));
  for(const id of startingItemUnits(catalog,result))units.add(id);
  const count=new Set([...units,...done]).size;
  const available=new Set(unlocks.map(item=>item.key));
  const items=new Set((Array.isArray(saved?.items)?saved.items:[]).filter(id=>available.has(id)));
  for(const item of unlocks)if(item.modules<=count)items.add(item.key);
  const next={units:[...units],items:[...items]};
  storage.setItem(key,JSON.stringify(next));return next.items;
}
