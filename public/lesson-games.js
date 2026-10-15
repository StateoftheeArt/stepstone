import {escapeHTML as esc} from './engine.js?build=123';
import {wireMoves} from './touch-move.js?build=123';
import {canadianCoin,canadianMoneyPiece} from './canadian-money.js?build=123';

export function gameTotal(game,state){
  const selected=new Set(state.selected||[]);
  if(game.kind==='cash')return (state.coins||[]).reduce((a,b)=>a+b,0)/100;
  return game.parts.reduce((sum,part,i)=>sum+(selected.has(i)?part.value:0),0);
}

const moneyLabel=c=>c>=100?`${c/100} ${c===100?'dollar':'dollars'}`:`${c} cents`;

export function coinSceneMarkup(game){
  if(game.kind!=='count'||game.unit!=='dollars'||!game.parts?.length||game.parts.some(p=>![1,.25].includes(p.value)))return '';
  const coins=game.parts,loonies=coins.filter(p=>p.value===1).length,quarters=coins.length-loonies;
  const description=`${loonies} Canadian one-dollar ${loonies===1?'coin':'coins'} and ${quarters} ${quarters===1?'quarter':'quarters'}.`;
  return `<section class="lesson-game canadian-coin-scene" aria-label="${esc(game.title)}"><strong>${esc(game.title)}</strong><figure><svg viewBox="0 0 ${coins.length*94+24} 124" role="img" aria-label="${description}">${coins.map((p,i)=>canadianCoin(p.value,14+i*94+(p.value===1?0:4),p.value===1?18:23,p.value===1?84:76)).join('')}</svg><figcaption>Canadian $1 coins (loonies) and 25¢ coins (quarters)</figcaption></figure><p class="game-next">${esc(game.answerCue)} <span aria-hidden="true">↓</span></p></section>`;
}
export function mountLessonGame({host,game,state,html,save}){
  const coinScene=coinSceneMarkup(game);if(coinScene){host.innerHTML=coinScene;return;}
  state.selected??=[];state.coins??=[];
  const cash=game.kind==='cash';
  const choose=i=>{state.selected=state.selected.includes(i)?state.selected.filter(n=>n!==i):[...state.selected,i];save();paint();host.querySelector(`[data-game-piece="${i}"]`)?.focus({preventScroll:true});};
  const add=value=>{if(state.coins.length>=30)return;state.coins.push(value);save();paint();host.querySelector(`[data-game-coin="${value}"]`)?.focus({preventScroll:true});};
  function paint(){
    const amount=gameTotal(game,state),any=cash?state.coins.length:state.selected.length;
    const format=value=>game.unit==='hours'?String(value):value.toFixed(2);
    let label=game.total===undefined?'Counted so far':game.kind==='discount'?'Saving selected':'Money left';
    let formula='';
    if(game.kind==='earn')formula=`${state.selected.length}\\times${game.rate}=${amount}`;
    if(game.kind==='clock')formula=state.selected.length?game.parts.filter((_,i)=>state.selected.includes(i)).map(p=>p.value).join('+')+'='+amount:'0';
    if(game.kind==='budget')formula=`${game.total}-${amount}=${game.total-amount}`;
    if(game.kind==='discount')formula=`${game.total}-${amount}=${game.total-amount}`;
    const result=game.kind==='budget'?game.total-amount:amount;
    host.innerHTML=`<section class="lesson-game game-${esc(game.kind)}" aria-label="${esc(game.title)}"><div class="game-instruction"><span aria-hidden="true">↘</span><div><strong>${esc(game.title)}</strong><p>${esc(game.instruction)}</p></div></div>
      ${game.facts?`<div class="game-facts">${game.facts.map(([name,value])=>`<div><span>${esc(name)}</span><strong>${esc(value)}</strong></div>`).join('')}</div>`:''}
      ${cash?`<div class="game-counter" data-drop="cash"><span>Your change counter · drop money here</span><output>${format(amount)} dollars</output><div class="game-coins">${state.coins.map(c=>`<span class="counter-money">${canadianMoneyPiece(c)}</span>`).join('')||'<span>Empty counter</span>'}</div></div><div class="game-pieces">${game.coins.map(c=>`<button type="button" class="game-piece coin-piece" data-game-coin="${c}" data-move="cash" ${state.coins.length>=30?'disabled':''}>${canadianMoneyPiece(c)}<strong>${moneyLabel(c)}</strong><small>Tap or drag to add</small></button>`).join('')}</div><button class="btn secondary small" data-game-undo ${any?'':'disabled'}>Undo last amount</button>`:
      `<div class="game-pieces">${game.parts.map((part,i)=>`<button type="button" class="game-piece" data-game-piece="${i}" aria-pressed="${state.selected.includes(i)}"><span class="piece-state" aria-hidden="true">${state.selected.includes(i)?'✓':'＋'}</span><strong>${esc(part.label)}</strong><span>${esc(part.detail)}</span><small>${state.selected.includes(i)?'Tap to undo':'Tap to '+(game.kind==='budget'?'subtract':game.kind==='discount'?'take off':'count')}</small></button>`).join('')}</div><div class="game-tally" aria-live="polite"><span>${label}</span><output>${format(result)} ${esc(game.unit)}</output>${game.kind==='discount'?`<span>Price after your selection: ${format(game.total-amount)} dollars</span>`:''}</div>`}
      ${formula?`<div class="game-equation">${html('$'+formula+'$')}</div>`:''}<p class="game-next">${esc(game.answerCue)} <span aria-hidden="true">↓</span></p></section>`;
    host.querySelectorAll('[data-game-piece]').forEach(b=>b.onclick=()=>choose(Number(b.dataset.gamePiece)));
    host.querySelectorAll('[data-game-coin]').forEach(b=>b.onclick=()=>add(Number(b.dataset.gameCoin)));
    host.querySelector('[data-game-undo]')?.addEventListener('click',()=>{state.coins.pop();save();paint();host.querySelector('[data-game-undo]')?.focus({preventScroll:true});});
    if(cash)wireMoves(host.querySelector('.lesson-game'),{centerGhost:true,ghost:el=>canadianMoneyPiece(Number(el.dataset.gameCoin)),onDrop:from=>add(Number(from.dataset.gameCoin))});
  }
  paint();
}
