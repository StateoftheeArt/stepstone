import {escapeHTML as esc} from './engine.js?build=120';

export function dailyDay(at=Date.now()){
  // Manitoba's permanent UTC-5 rule takes effect on 31 October 2026.
  // Use the same boundary as daily_tasks.py even with an older browser TZDB.
  if(at>=Date.UTC(2026,9,31,5))return new Date(at-5*60*60*1000).toISOString().slice(0,10);
  const parts=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Winnipeg',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(at);
  return ['year','month','day'].map(k=>parts.find(p=>p.type===k).value).join('-');
}
export function previewDaily(storage,key,task=null,at=Date.now()){
  const day=dailyDay(at);let saved;
  try{saved=JSON.parse(storage.getItem(key)||'null');}catch{}
  const completed=new Set(saved?.day===day&&Array.isArray(saved.completed)?saved.completed.filter(t=>['visit','module','play'].includes(t)):[]);
  if(['visit','module','play'].includes(task))completed.add(task);
  const record={day,zone:'America/Winnipeg',completed:[...completed],total:3};
  if(task)try{storage.setItem(key,JSON.stringify(record));}catch{}
  return record;
}
export function dailyTasksMarkup(record,{name='Pip',connected=false,next=null}={}){
  const done=new Set(record?.day===dailyDay()?record.completed:[]);
  const tasks=[{id:'visit',title:connected?'Log in':'Open Stepstone',detail:'Come back for today’s practice.'},
    {id:'module',title:'Complete a module',detail:'Pass a new module or a review.',href:next?'#lesson/'+encodeURIComponent(next.id):'#path'},
    {id:'play',title:'Play with '+(name||'Pip'),detail:'Tap your Pip after feeding it.',action:'daily-pip'}];
  return `<section class="daily-tasks" data-daily-tasks aria-labelledby="daily-title"><div class="section-title"><h2 id="daily-title">Today’s tasks</h2><span class="pill">${done.size} of 3 done</span></div><div class="daily-grid">${tasks.map(t=>`<article class="daily-task ${done.has(t.id)?'is-done':''}"><span class="daily-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>${done.has(t.id)?'<path d="m7 12 3 3 7-7"/>':''}</svg></span><div><h3>${esc(t.title)}</h3><p>${esc(t.detail)}</p>${done.has(t.id)?'<span class="daily-state">Done today</span>':t.action?`<button class="text-link" data-action="${t.action}">Open Pip’s home →</button>`:t.href?`<a class="text-link" href="${t.href}">Choose a module →</a>`:''}</div></article>`).join('')}</div></section>`;
}
