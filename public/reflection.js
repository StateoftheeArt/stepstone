import {escapeHTML as esc} from './engine.js?build=121';

export function reflectionSpec(unit){
  const writing=(unit.domain||unit.subject)==='writing';
  const specifics={
    'reading-4':'Jo checks the route, packs water and finds a jacket. Summarize what Jo is doing in one sentence. Explain which details support your summary.',
    'reading-8':'Read: “Everyone likes this game. Nine of my ten friends liked it.” Explain what this evidence shows and what it cannot prove.',
    'reading-12':'A library could stay open later to help evening visitors, but extra staffing would cost more. Describe one benefit, one cost and what else you would check before deciding.'
  };
  const task=specifics[unit.id]||(writing?unit.reflection.replace(/ Explain one choice you made, then improve one detail\.$/,''):unit.reflection);
  const why=unit.id==='writing-1'?'Explain how the day, time and specific place help the reader use your meeting plan.':unit.id==='writing-2'?'Explain how naming each person makes their action clear.':'Explain one change that makes your writing clearer.';
  return {title:writing?'Your writing task':'Show your thinking',task,guidance:writing?why:'Use words or a drawing to show how you worked it out.',label:writing?'Your writing and explanation':'Your explanation',placeholder:writing?'My message: …\nI included … so the reader knows …':'I worked it out by …\nThis works because …',empty:writing?'Write your message, then explain one detail you included.':'Answer the task above and describe how you worked it out.'};
}

export function reflectionMarkup(unit,value,html=esc){
  const s=reflectionSpec(unit);
  return `<div class="reflection-task" id="reflection-task"><h2>${esc(s.title)}</h2><p class="reflection-instruction" id="reflection-prompt">${html(s.task)}</p><p class="reflection-guidance" id="reflection-guidance">${esc(s.guidance)}</p><label class="field"><span>${esc(s.label)}</span><textarea data-draft="reflection" maxlength="2000" aria-describedby="reflection-prompt reflection-guidance" placeholder="${esc(s.placeholder)}">${esc(value||'')}</textarea></label></div>`;
}
