// Keeps names and item names suitable for a PG-16 learning space. Mirrors text_filter.py;
// language.js applies the boundary to human-authored text and narration.
const LEET={'0':'o','1':'i','3':'e','4':'a','5':'s','7':'t','@':'a','$':'s','!':'i','|':'i'};

export function textWords(text){
  const folded=String(text).normalize('NFKD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[013457@$!|]/g,c=>LEET[c]);
  return folded.match(/[a-z*]+/g)||[];
}

function candidates(tokens){
  const found=tokens.map(t=>[t,true]);
  for(const n of [2,3])for(let i=0;i+n<=tokens.length;i++)found.push([tokens.slice(i,i+n).join(''),false]);
  let run=[];
  for(const t of [...tokens,'']){if(t.length===1)run.push(t);else{if(run.length>=2)found.push([run.join(''),true]);run=[];}}
  if(tokens.length>3)found.push([tokens.join(''),false]);
  return found;
}

export function createTextFilter(record){
  const t=JSON.parse(atob(record.terms)),exact=new Set(t.exact),phrases=new Set(t.phrases),allow=new Set(t.allow);
  const hit=(form,whole)=>{
    if(allow.has(form))return false;
    if(phrases.has(form)||t.contains.some(c=>form.includes(c)))return true;
    return whole&&(exact.has(form)||t.prefix.some(p=>form.startsWith(p)));
  };
  return function acceptable(text){
    if(typeof text!=='string')return true;
    let stars=0;
    for(const [value,whole] of candidates(textWords(text))){
      for(const form of new Set([value,value.replace(/(.)\1+/g,'$1'),value.replace(/(.)\1{2,}/g,'$1$1')])){
        if(!form.includes('*')){if(hit(form,whole))return false;continue;}
        // A star may hide one letter; limited so long text stays quick.
        const parts=form.split('*');
        if(!whole||parts.length>3||form.length>12||stars>=10)continue;
        stars++;
        const letters='abcdefghijklmnopqrstuvwxyz';
        for(const a of letters){
          if(parts.length===2){if(hit(parts[0]+a+parts[1],true))return false;continue;}
          for(const b of letters)if(hit(parts[0]+a+parts[1]+b+parts[2],true))return false;
        }
      }
    }
    return true;
  };
}
