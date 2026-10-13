export const activeUnits=(catalog,subject)=>catalog.units.filter(u=>u.ready&&u.active!==false&&(!subject||u.subject===subject)).sort((a,b)=>(a.sequence||a.grade||0)-(b.sequence||b.grade||0));
export const canonicalSubject=id=>({writing:'reading',social:'reading'}[id]||id);
export function suggestedStart(catalog,subject,starting){
  const chain=activeUnits(catalog,canonicalSubject(subject));
  if(!chain.length)return null;
  if(!starting?.complete)return chain[0];
  if([4,5].includes(starting.version))return chain.find(u=>u.id===starting.suggestions?.[canonicalSubject(subject)])||chain[0];
  if(['digital','life','work'].includes(subject))return chain[0];
  const area=canonicalSubject(subject)==='reading'?'reading':subject;
  const level=area==='reading'?Math.min(starting.levels?.reading||1,starting.levels?.writing||1):starting.levels?.[area]||1;
  return chain.find(u=>u.id===area+'-'+level)||chain.find(u=>(u.placementArea||u.domain||u.subject)===area&&!u.practical&&u.grade>=level)||chain[0];
}
