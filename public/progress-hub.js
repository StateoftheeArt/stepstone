import {escapeHTML as esc} from './engine.js?build=123';

export function canonicalHubHash(hash){
  const section=/^#rewards-(cards|goals|ai)$/.exec(hash);
  if(section)return section[1]==='ai'?'#progress/rewards':'#progress/rewards/'+section[1];
  if(hash==='#rewards')return '#progress';
  const current=/^#rewards\//.test(hash)?hash.replace(/^#rewards/,'#progress/rewards'):hash;
  return current==='#progress/rewards/ai'?'#progress/rewards':current;
}
export function hubSectionForHash(hash){
  const canonical=canonicalHubHash(hash);
  if(canonical==='#progress/rewards')return 'learning-rewards';
  const section=canonical.split('/')[2];
  return {cards:'rewards-cards',goals:'rewards-goals',ai:'learning-rewards'}[section]||null;
}
export function learningHubMarkup({points=0,modules=0,checks=0,preview=false,wins='',rewards='',rewardsOnly=false,guide=false}){
  const count=value=>esc(Number.isFinite(Number(value))?Math.max(0,Number(value)):0);
  return `<div class="learning-hub">
    <div class="hub-header"><h1>Rewards</h1>
    <div class="learning-hub-summary" aria-label="Learning summary">
      <div class="hub-points"><strong class="points-value">${count(points)}</strong><span>${Number(points)===1?'Step':'Steps'}${preview?' · welcome':' available'}</span></div>
    </div></div>
    ${rewardsOnly?'':`<section class="hub-wins" aria-labelledby="wins-title">
      <div class="hub-section-head"><h2 id="wins-title">My wins</h2>${guide?'<a class="btn small secondary rewards-jump" href="#progress/rewards">View rewards ↓</a>':''}</div>
      ${wins}
    </section>`}
    <section class="hub-rewards" id="learning-rewards" ${rewardsOnly?'aria-label="Reward goals"':'aria-labelledby="rewards-title"'}>
      ${rewardsOnly?'':'<h2 id="rewards-title">My rewards</h2>'}
      ${rewards}
    </section>
  </div>`;
}
