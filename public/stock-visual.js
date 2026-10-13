import {escapeHTML as esc} from './engine.js?build=120';
const amount=(n,max)=>Number.isInteger(n)&&n>=0&&n<=max?n:0;
const chip='<span class="stock-label" aria-hidden="true"></span>';
export function stockModelMarkup({tens=0,ones=0,released=0}={}, {total=false}={}){
 tens=amount(tens,9);ones=amount(ones,29);released=amount(released,29);
 return `<div class="stock-workbench" role="group" aria-label="${tens} bundles of ten labels and ${ones} loose labels"><div class="stock-trays"><section class="stock-tray"><h3>Closed bundles <span>${tens}</span></h3><p>10 labels in every bundle</p><div class="stock-packs">${Array.from({length:tens},(_,i)=>`<div class="stock-pack" aria-label="Bundle ${i+1}: ten labels">${chip.repeat(10)}<strong>10 labels</strong></div>`).join('')||'<span class="stock-empty">No bundles here yet</span>'}</div></section><section class="stock-tray"><h3>Loose labels <span>${ones}</span></h3><p>1 label in every tile</p><div class="stock-loose">${Array.from({length:ones},(_,i)=>`<span class="stock-label${i>=ones-released?' is-released':''}" style="--release:${Math.max(0,i-ones+released)*35}ms" aria-hidden="true"></span>`).join('')||'<span class="stock-empty">No loose labels here yet</span>'}</div></section></div>${total?`<p class="stock-total"><span>Labels on the shelf</span><output>${tens*10+ones}</output><span>${tens} × 10 + ${ones} = ${tens*10+ones}</span></p>`:''}</div>`;
}
export function stockTakeMarkup(model,selected=[]){
 const n=amount(model?.ones,29),chosen=new Set((Array.isArray(selected)?selected:[]).filter(i=>Number.isInteger(i)&&i>=0&&i<n));
 const button=(i,taken)=>`<button type="button" class="stock-pick${taken?' is-taken':''}" data-stock-pick="${i}" aria-pressed="${taken}" aria-label="${taken?'Return':'Take'} loose label ${i+1}">${chip}</button>`;
 return `<div class="stock-take"><p class="stock-directions">Tap a loose label to move it into the order. Tap it there to put it back. Include the labels inside closed bundles when you work out what remains.</p><div class="stock-take-trays"><section class="stock-tray"><h3>Still on the shelf</h3>${stockModelMarkup({tens:model.tens,ones:0}).replace(/<section class="stock-tray"><h3>Loose labels[\s\S]*?<\/section>/,'')}<p class="stock-loose-count">${n-chosen.size} loose labels</p><div class="stock-loose">${Array.from({length:n},(_,i)=>chosen.has(i)?'':button(i,false)).join('')||'<span class="stock-empty">No loose labels remain</span>'}</div></section><section class="stock-tray stock-order"><h3>Moved to the order <span>${chosen.size} of 8</span></h3><div class="stock-loose">${Array.from(chosen).sort((a,b)=>a-b).map(i=>button(i,true)).join('')||'<span class="stock-empty">Your order starts empty</span>'}</div></section></div></div>`;
}
export function stockExampleFrames(unit,mode='stock'){
 if(mode==='money')return [
  {text:'Two Canadian 10-dollar notes: 10 + 10 = 20 dollars.',index:0},
  {text:'Four 1-dollar loonies: 1 + 1 + 1 + 1 = 4 dollars.',index:1},
  {text:'Combine the values: 20 + 4 = 24 dollars.',index:2}
 ];
 if(mode==='trade')return [
  {text:'Start with 3 closed bundles and 4 loose labels: 30 + 4 = 34.',index:0},
  {text:'Open one bundle. Its 10 labels join the 4 loose labels. The shelf still holds 34.',index:1},
  {text:'Move 8 loose labels to the order. The shelf keeps 2 bundles and 6 loose labels: 26.',index:2}
 ];
 return unit.lessons[0].steps.map((text,index)=>({text,index}));
}
const text=(x,y,s,size=16)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="#e0efea" font-size="${size}" font-family="sans-serif">${esc(s)}</text>`;
const label=(x,y,colour='#a9d8c7',opacity=1)=>`<g opacity="${opacity}"><path d="M${x+3} ${y}h14v18H${x}V${y+3}Z" fill="${colour}" stroke="#547f85" stroke-width="1"/><circle cx="${x+4}" cy="${y+4}" r="1" fill="#244b59"/><path d="M${x+4} ${y+10}h9m-9 4h9" stroke="#547f85" stroke-width="1"/></g>`;
const bundle=(x,y)=>`<g data-stock-bundle=""><rect x="${x}" y="${y}" width="96" height="78" rx="9" fill="#244650" stroke="#aad1c4" stroke-width="1.5"/>${Array.from({length:10},(_,i)=>label(x+7+i%5*17,y+8+Math.floor(i/5)*23)).join('')}<path d="M${x+4} ${y+30}h88" stroke="#e4c592" stroke-width="4"/>${text(x+48,y+70,'10 labels',13)}</g>`;
export function stockDiagram(mode='stock',index=0){
 let shapes='',description='';
 if(mode==='trade'){
  const tens=index===0?3:2,ones=[4,14,6][index];
  shapes=Array.from({length:tens},(_,i)=>bundle(10+i*100,18)).join('');
  if(index===0){shapes+=Array.from({length:4},(_,i)=>label(148+i*26,127)).join('')+text(200,170,'3 bundles · 4 loose labels')+text(200,209,'30 + 4 = 34 labels',19);}
  else{shapes+=Array.from({length:ones},(_,i)=>label(245+i%5*23,25+Math.floor(i/5)*25,index===1&&i>=4?'#e5c694':'#a9d8c7')).join('')+text(300,index===1?118:94,ones+' loose labels',14);if(index===2)shapes+=Array.from({length:8},(_,i)=>label(252+i%4*23,128+Math.floor(i/4)*22,'#e5c694',.7)).join('')+text(300,184,'Order: 8 labels',13);shapes+=text(107,121,'2 closed bundles',14)+text(200,209,index===1?'20 + 14 = 34 labels':'20 + 6 = 26 labels',19);}
  description=index===0?'34 labels: three bundles of ten and four loose labels':index===1?'One bundle opened: two bundles and fourteen loose labels still total thirty-four': 'Eight loose labels moved to the order; two bundles and six loose labels remain';
 }else{
  shapes=bundle(15,42)+bundle(121,42)+text(116,146,'2 bundles = 20 labels',15);
  if(index)shapes+=Array.from({length:4},(_,i)=>label(263+i%2*28,63+Math.floor(i/2)*28)).join('')+text(295,144,'4 loose labels',14);
  shapes+=text(200,204,index===2?'20 + 4 = 24 labels':index===1?'Each loose label counts as one':'Every closed bundle counts as ten',18);
  description=index===0?'Two closed bundles, each visibly containing ten labels': 'Two bundles of ten labels and four loose labels make twenty-four labels';
 }
 return `<svg class="lesson-diagram stock-example-diagram" viewBox="0 0 400 220" role="img" aria-label="${esc(description)}">${shapes}</svg>`;
}
