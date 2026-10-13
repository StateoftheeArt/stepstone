import {activeUnits} from './curriculum.js?build=120';
import {escapeHTML as esc, shuffle, correct} from './engine.js?build=120';
export const PUBLIC_DEMO = true;
// Keep release checks separate from the visitor's saved practice.
export function demoPracticeScope(search=''){
  const id=new URLSearchParams(search).get('practice')||'';
  return /^[A-Za-z0-9_-]{1,64}$/.test(id)?'public-demo-test-'+id:'public-demo';
}
let bankFlight;
const demoError = (message, status=400) => Object.assign(new Error(message), {status});
const caseKey = question => question.caseId || question.prompt;

export function sampleDemoCheck(bank, skills=['calculate','apply','reason']) {
  const chosen=[], used=new Set(), quota=Math.floor(6/skills.length);
  for (const skill of skills) {
    const cases = new Map(bank.filter(q=>q.skill===skill&&!used.has(caseKey(q))).map(q=>[caseKey(q),q]));
    const pool=shuffle([...cases.values()]);
    const first=pool.find(q=>q.lesson===1), second=pool.find(q=>q.lesson===2);
    const pair=first&&second ? [first,second] : pool.slice(0,quota);
    for(const q of pool) if(pair.length<quota&&!pair.some(p=>caseKey(p)===caseKey(q))) pair.push(q);
    chosen.push(...pair); for(const q of pair) used.add(caseKey(q));
  }
  if(chosen.length<6) {
    const pool=[...new Map(bank.filter(q=>!used.has(caseKey(q))).map(q=>[caseKey(q),q])).values()];
    chosen.push(...shuffle(pool).slice(0,6-chosen.length));
  }
  for(const lesson of [1,2]) {
    if(!bank.some(q=>q.lesson===lesson)||chosen.some(q=>q.lesson===lesson)) continue;
    const usedCases=new Set(chosen.map(caseKey)); let replaced=false;
    for(const q of shuffle(bank.filter(q=>q.lesson===lesson&&!usedCases.has(caseKey(q))))) {
      const other=3-lesson, count=chosen.filter(p=>p.lesson===other).length;
      const index=chosen.findIndex(p=>p.skill===q.skill&&(p.lesson!==other||count>1));
      if(index>=0){chosen[index]=q;replaced=true;break;}
    }
    if(!replaced) throw demoError('This practice check could not cover both examples. Try opening it again.');
  }
  if(chosen.length!==6||new Set(chosen.map(caseKey)).size!==6) throw demoError('This practice check could not open. Try again.');
  return shuffle(chosen).map(q=>({...structuredClone(q),...(q.options?{options:shuffle(q.options.map(o=>({...o})))}:{})}));
}
async function loadBank() {
  bankFlight ??= fetch('preview-checks.json?demo=2').then(response=>{
    if(!response.ok) throw demoError('Practice questions could not load. Please reload.',503);
    return response.json();
  }).catch(error=>{bankFlight=null;throw error;});
  return bankFlight;
}
export async function publicDemoRequest(path, data={}, catalog, getBank=loadBank) {
  if(path==='/api/health') return {ok:true,publicDemo:true,desktop:false,softVoice:false};
  if(path==='/api/me'||path==='/api/mentor') throw demoError('You are trying Stepstone on this browser.',401);
  if(path==='/api/presence'||path==='/api/logout') return {ok:true};
  if(path==='/api/preview-check') {
    const unit=catalog?.units.find(u=>u.id===data.unit&&u.ready), bank=await getBank();
    if(!unit||!Array.isArray(bank[data.unit])) throw demoError('This module is not ready yet.');
    return {id:'demo-'+crypto.randomUUID(),unit:unit.id,remotePreview:false,questions:sampleDemoCheck(bank[unit.id],unit.checkSkills)};
  }
  throw demoError('This feature uses a connected learner-and-mentor installation. You can keep practising in this browser.');
}
const readyUnits = catalog => activeUnits(catalog);
function demoFooter() {
  return `<footer class="demo-footer"><a href="https://www.linkedin.com/feed/update/urn:li:share:7515571522032459776/" target="_blank" rel="noopener">Share feedback</a><a href="https://github.com/StateoftheeArt/stepstone" target="_blank" rel="noopener">Source & setup</a><a href="privacy.html">Privacy &amp; data</a><a href="THIRD_PARTY_NOTICES.md">Asset notices</a><a href="LICENSE">MIT license</a></footer>`;
}
export function demoHome(catalog,local) {
  const units=readyUnits(catalog), inProgress=units.filter(u=>local[u.id]?.phase>0&&local[u.id]?.phase<7).sort((a,b)=>(local[b.id].touchedAt||0)-(local[a.id].touchedAt||0));
  return `<section class="demo-hero"><div><p class="eyebrow">PRACTICAL LEARNING, ONE STEP AT A TIME</p><h1>Try your next step.</h1><p class="demo-lead">Work through a clear example, try it yourself, and see why each answer works. Pip keeps you company along the way.</p><div class="buttons"><a class="btn" href="#lesson/math-1">Try a first lesson →</a><a class="btn secondary" href="#mentor">Explore the mentor workflow</a></div><p class="legend">No sign-in or download. Your practice stays on this browser.</p></div><div class="card demo-first-step"><img src="icon.svg" width="80" height="80" alt=""><p class="eyebrow">A SMALL FIRST STEP</p><h2>Pack the order</h2><p>Count what is in the bag. Add what is missing. Check that the order matches.</p><a class="text-link" href="#lesson/math-1">Start with everyday math →</a></div></section>${inProgress.length?`<section class="card demo-resume"><h2>Pick up where you left off</h2><p>${esc(inProgress[0].title)}</p><a class="btn secondary" href="#lesson/${esc(inProgress[0].id)}">Continue my practice →</a></section>`:''}<section class="demo-courses"><div class="module-heading"><div><h2>What would you like to try?</h2><p>Browse any of the ${units.length} modules. Choose something useful to you.</p></div></div><div class="demo-course-grid">${catalog.subjects.map((s,i)=>`<article class="card demo-course world-${esc(s.id)}"><span class="demo-course-number" aria-hidden="true">0${i+1}</span><h3>${esc(s.name)}</h3><p>${esc(s.short)}</p><a class="btn secondary" href="#path/${esc(s.id)}">Browse ${esc(s.name.toLowerCase())} →</a></article>`).join('')}</div></section><section class="card demo-mentor-intro"><div><p class="eyebrow">LEARNING WITH SUPPORT</p><h2>See how a mentor helps.</h2><p>Explore a sample lesson report and practise writing an encouraging next step.</p></div><a class="btn secondary" href="#mentor">Try a sample review →</a></section>${demoFooter()}`;
}
export function demoPath(catalog,subject,local,passed) {
  const chosen=catalog.subjects.find(s=>s.id===subject)||catalog.subjects[0], units=readyUnits(catalog).filter(u=>u.subject===chosen.id);
  return `<div class="page-head"><h1>Choose a lesson.</h1><p>Every module is open for you to explore in this demo.</p></div><nav class="filters" aria-label="Choose a subject">${catalog.subjects.map(s=>`<a href="#path/${esc(s.id)}" class="filter world-${esc(s.id)} ${s.id===chosen.id?'active':''}" ${s.id===chosen.id?'aria-current="page"':''}>${esc(s.name)}</a>`).join('')}</nav><div class="module-heading"><div><h2>${esc(chosen.name)}</h2><p>${esc(chosen.short)}</p></div><span class="pill">${passed.size} modules practised across all subjects</span></div><div class="path-grid">${units.map(u=>`<article class="card path-unit world-${esc(u.subject)}"><div class="module-card-heading"><h3>${esc(u.title)}</h3>${passed.has(u.id)?'<span class="pill ready">Check passed here</span>':''}</div><div class="module-body"><p>${esc(u.why)}</p></div><div class="module-controls"><a class="btn secondary small" href="#lesson/${esc(u.id)}">${local[u.id]?.phase>0&&local[u.id]?.phase<7?'Continue':'Try this module'} →</a></div></article>`).join('')}</div>${demoFooter()}`;
}
export function demoProgress(catalog,local) {
  const records=readyUnits(catalog).filter(u=>local[u.id]?.result).sort((a,b)=>(local[b.id].result.at||0)-(local[a.id].result.at||0));
  return `<div class="page-head"><h1>My practice.</h1><p>Your checks and drafts stay on this browser. Come back using the same browser to continue.</p></div>${records.length?`<section class="demo-records">${records.map(u=>`<article class="card report-row"><div class="grow"><h2>${esc(u.title)}</h2><p>${local[u.id].result.score} of 6 matched · ${local[u.id].result.passed?'Check passed here':'Worth another look'}</p></div><button class="btn secondary small" data-action="revisit" data-unit="${esc(u.id)}">Try this lesson again →</button></article>`).join('')}</section>`:'<section class="card"><h2>Your first check is waiting.</h2><p>Try an example, practise it, and complete a six-question preview check.</p><a class="btn" href="#lesson/math-1">Try a first lesson →</a></section>'}<p class="notice">A practice score is one part of learning. Try a changed example or talk through your reasoning with someone who can help.</p>${demoFooter()}`;
}
export function demoMentor() {
  return `<div class="page-head"><p class="eyebrow">MENTOR WORKFLOW · SAMPLE</p><h1>A useful next step, together.</h1><p>Mentors invite learners, review their completed work, and give encouragement or a clear next step.</p></div><div class="demo-mentor-steps"><section class="card"><span class="demo-course-number">01</span><h2>Invite a learner</h2><p>In the full app, open <strong>Mentor → Invitations</strong> and create one private start link per learner. An invitation is single use and expires after seven days. Returning learners use their return link.</p></section><section class="card"><span class="demo-course-number">02</span><h2>Review their work</h2><p>Open <strong>Progress inbox</strong>, choose a report, and review the check, learner explanation and any support they used. Discuss the reasoning and try a changed example.</p></section><section class="card"><span class="demo-course-number">03</span><h2>Give feedback</h2><p>Write encouragement or a next step, then choose <strong>Save note & mark reviewed</strong>. The learner sees it in <strong>My feedback</strong>.</p></section></div><section class="card demo-sample-report"><p class="eyebrow">FICTIONAL REPORT · TRY A REVIEW</p><h2>Pack the order</h2><p><strong>Sample learner</strong> · 5 of 6 matched · Worked on their own</p><blockquote>“The order needs 7 cartons. I packed 4. I counted 5, 6, 7, so I need 3 more. I checked that 4 + 3 = 7.”</blockquote><p>A helpful note names something the learner did well and gives one specific next step.</p><form data-demo-feedback><label class="field"><span>Encouragement or next step for this example</span><textarea name="note" rows="3" maxlength="1000" required placeholder="You checked your answer by adding back. Next, try an order with 9 cartons."></textarea></label><button class="btn" type="submit">Preview learner feedback</button><div data-demo-feedback-result role="status" aria-live="polite"></div></form><p class="legend">This is a sample review on your browser. A connected installation keeps real learner records and shares mentor feedback privately.</p></section><section class="card"><h2>Run a learner-and-mentor pilot</h2><p>The full app can run on your own computer. Learners on other devices need a shared HTTPS installation with persistent storage and recovery copies.</p><div class="buttons"><a class="btn secondary" href="https://github.com/StateoftheeArt/stepstone#run-locally" target="_blank" rel="noopener">Full app setup →</a><a class="text-link" href="#home">Back to trying the lessons →</a></div></section>${demoFooter()}`;
}
export function mountDemoMentor(root) {
  const form=root.querySelector('[data-demo-feedback]');
  form?.addEventListener('submit',event=>{
    event.preventDefault(); const note=form.elements.note.value.trim(); if(!note)return;
    const output=form.querySelector('[data-demo-feedback-result]');
    output.innerHTML=`<div class="notice"><strong>The sample learner would see:</strong><p>${esc(note)}</p></div>`;
  });
}
