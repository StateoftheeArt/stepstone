import {pipItemIcon} from './pip-items.js?build=119';
import {escapeHTML as esc} from './engine.js?build=119';

const byTime=(a,b)=>Number(a.finished||0)-Number(b.finished||0);
const brief=r=>({title:r.title,score:r.score,total:r.total||6,passed:true,tryNumber:r.tryNumber||1});

export function firstPasses(reports=[],unlocks=[]){
  const seen=new Set(),completed=[];
  for(const a of [...reports].sort(byTime)){
    if(!a.report?.passed||seen.has(a.unit))continue;
    seen.add(a.unit);
    completed.push({...a,report:brief(a.report),pipFood:a.pipFood??1,pipItems:Array.isArray(a.pipItems)?a.pipItems:unlocks.filter(item=>item.modules===completed.length+1)});
  }
  return completed;
}

export function previewCompletions(local={},unlocks=[]){
  return firstPasses(Object.entries(local).flatMap(([unit,d])=>d.firstPass?[{...d.firstPass,unit}]:d.result?.passed?[{unit,finished:d.result.at||d.touchedAt/1000||0,report:d.result}]:[]),unlocks);
}

export function preservePreviewCompletions(local={},unlocks=[],startingUnits=[]){
  const seen=new Set(startingUnits),owned=new Set();
  for(const a of previewCompletions(local,unlocks)){
    const before=seen.size;seen.add(a.unit);
    if(!local[a.unit].firstPass){
      const pipItems=unlocks.filter(item=>before<item.modules&&item.modules<=seen.size&&!owned.has(item.key));
      local[a.unit].firstPass={...a,pipItems};
    }
    for(const item of local[a.unit].firstPass.pipItems||[])owned.add(item.key);
  }
}

export function groupWins({catalog,reports=[],completions=[],unlocks=[]}={}){
  const passed=firstPasses(completions,unlocks),modules=new Map(passed.map(a=>[a.unit,{unit:a.unit,completion:a,checks:[]}])) ;
  for(const a of [...reports].sort((a,b)=>byTime(b,a))){
    if(!modules.has(a.unit))modules.set(a.unit,{unit:a.unit,completion:null,checks:[]});
    modules.get(a.unit).checks.push(a);
  }
  const groups=catalog.subjects.map(s=>({...s,modules:[],completed:0}));
  for(const item of modules.values()){
    const unit=catalog.units.find(u=>u.id===item.unit),sid=unit?.subject||item.unit.split('-')[0];
    let group=groups.find(s=>s.id===sid);
    if(!group){group=groups.find(s=>s.id==='other');if(!group){group={id:'other',name:'Other learning',modules:[],completed:0};groups.push(group);}}
    item.title=unit?.title||item.completion?.report.title||item.checks[0]?.report.title||item.unit;
    group.modules.push(item);if(item.completion)group.completed++;
  }
  for(const group of groups)group.modules.sort((a,b)=>byTime(b.completion||b.checks[0]||{},a.completion||a.checks[0]||{}));
  return groups.filter(s=>s.modules.length);
}

export function itemIcon(item){
  const drawing=pipItemIcon(item.key);if(drawing)return drawing;
  const shapes={
    'home.rug:round':'M2 12a10 5 0 1 0 20 0 10 5 0 1 0-20 0m3 0a7 3 0 1 0 14 0 7 3 0 1 0-14 0',
    'home.furniture:cushion':'M2 12q10-7 20 0v6q-10 6-20 0ZM5 15q7 4 14 0',
    'home.decor:plant':'M8 14h9l-1 8h-7Zm4 0V5m0 6C3 11 3 3 7 4c4 0 5 5 5 7m0-3c8 2 9-7 4-6-3 0-4 3-4 6',
    'accessory:sprout':'M12 21V9m0 5C3 14 2 4 7 5c4 1 5 5 5 9Zm0-3c8 2 10-7 5-7-3 0-5 4-5 7Z',
    'accessory:scarf':'M7 3h10v6H7zM9 9v12h4V9m0 0 5 7-3 3-6-8',
    'accessory:headphones':'M4 14v-3a8 8 0 0 1 16 0v3M4 12h4v8H4zM16 12h4v8h-4z',
    'home.wall:night':'M3 3h18v18H3zM16 6a5 5 0 1 0 2 8 5 5 0 0 1-2-8Z',
    'home.rug:woven':'M3 5h18v14H3zM6 8h12M6 12h12M6 16h12M3 21v-2m6 2v-2m6 2v-2m6 2v-2',
    'home.rug:star':'m12 2 3 6 7 1-5 5 1 8-6-4-6 4 1-8-5-5 7-1Z',
    'home.furniture:chair':'M6 12V6a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v6M3 11h4v6h10v-6h4v8H3zM5 19v3m14-3v3',
    'home.furniture:desk':'M2 9h20v4H2zM5 13v9m14-9v9M10 3h7v6h-7z',
    'home.decor:lamp':'m6 12 3-9h6l3 9ZM12 12v9m-5 0h10',
    'home.decor:books':'M4 2h16v20H4zM4 12h16M8 5v5m4-5v5m3-5 2 5M8 15v4m4-4v4m4-4v4',
    'home.decor:stars':'M6 2v4m12-4v9M6 5l2 3 3 1-2 2 1 4-4-2-4 2 1-4-2-2 3-1ZM18 10l2 3 3 1-2 2 1 4-4-2-4 2 1-4-2-2 3-1Z'
  };
  return `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="${shapes[item.key]||'M4 7h16v14H4zM2 3h20v4H2zM12 3v18'}"/></svg>`;
}

export function winsMarkup({catalog,reports=[],completions=[],unlocks=[],connected=false,personal=false,formatDate=()=>'',typingReport=()=>''}={}){
  const groups=groupWins({catalog,reports,completions,unlocks});
  const storage=!connected?'Practice preview · Saved on this device. You begin earning Steps from lessons when you connect with your mentor.':personal?'Saved to your personal learning record.':'Your mentor can review these checks and leave feedback.';
  if(!groups.length)return `<div class="wins-empty"><p>Your completed modules will appear here, grouped by subject.</p><a class="text-link" href="#path">Choose a module →</a>${!connected?`<p class="legend">${storage}</p>`:''}</div>`;
  const checkRow=a=>`<div class="win-check"><div><p>Check ${esc(a.report.tryNumber||1)} · ${esc(formatDate(a.finished))}${connected&&!personal?' · '+(a.reviewed?'Reviewed by mentor':'Awaiting mentor review'):''}</p>${a.note?`<p class="notice">Mentor note: ${esc(a.note)}</p>`:''}${typingReport(a.report.typingPractice)}</div><span class="pill">${esc(a.report.score)} of ${esc(a.report.total||6)} · ${a.report.passed?'Passed':'Try again'}</span></div>`;
  const moduleCard=m=>{
    const c=m.completion,items=c?.pipItems||[];
    const historyLabel=connected&&!personal?'Checks & mentor feedback':'Check history';
    return `<article class="win-module" data-win-unit="${esc(m.unit)}"><div class="win-module-head"><h3><a class="win-skill-link" href="#lesson/${encodeURIComponent(m.unit)}">${esc(m.title)}</a></h3><span class="pill win-outcome ${c?'passed':'review'}">${c?'Passed':'Keep practicing'}</span></div><p class="win-module-meta">${c?'Completed '+esc(formatDate(c.finished))+' · '+esc(c.report.score)+' of '+esc(c.report.total||6):'Pass this module to add it to your completed skills.'}</p>${c?items.length?`<div class="win-unlocks"><p class="win-unlock-label">Unlocked for Pip</p><ul class="win-item-list">${items.map(item=>`<li data-pip-item="${esc(item.key)}">${itemIcon(item)}<span>${esc(item.label)}</span></li>`).join('')}</ul></div>`:'':''}${c?'<p class="win-food-earned">+1 food portion for Pip</p>':''}${m.checks.length?`<details class="win-check-history" data-disclosure-key="win-checks-${esc(m.unit)}"><summary>${historyLabel} (${m.checks.length})</summary>${m.checks.map(checkRow).join('')}</details>`:''}</article>`;
  };
  return `<div class="wins-subjects">${groups.map(s=>`<details class="wins-subject world-${esc(s.id)}" data-disclosure-key="wins-${esc(s.id)}" data-win-subject="${esc(s.id)}"><summary><span class="wins-subject-name">${esc(s.name)}</span><span class="wins-subject-count">${s.completed} ${s.completed===1?'module':'modules'} completed</span></summary><div class="wins-subject-body">${s.modules.map(moduleCard).join('')}</div></details>`).join('')}</div><p class="legend wins-storage wins-subject-storage">${storage}</p>`;
}
