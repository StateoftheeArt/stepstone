import {escapeHTML as esc} from './engine.js?build=119';
export function lessonWords(unit){
  if(!unit.terms?.length)return '';
  return `<details class="lesson-words" ${unit.languageStage==='foundation'?'open':''}><summary>Words in this lesson</summary><dl>${unit.terms.map(word=>`<dt>${esc(word.term)}</dt><dd>${esc(word.meaning)}</dd>`).join('')}</dl></details>`;
}
