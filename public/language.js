// User-authored words use the same boundary in forms, saves and narration.
let acceptable=()=>true;
export const LANGUAGE_MESSAGE='Please reword this without offensive language.';
export function configureLanguage(filter){acceptable=filter;}
export const languageAllowed=text=>acceptable(text);
const TEXT_KEYS=new Set('alias name username device title description purpose label behaviours note text reflection explanation nextWin companionName message content supporter sponsor saved backup review_note accessNote backupNote explain email change reason plan cancellation writing value'.split(' '));
const SKIP=new Set('password passphrase username code recovery token id key questions options prompt hint example baseline'.split(' '));
export function payloadAllowed(value,key=''){
  if(SKIP.has(key))return true;
  if(Array.isArray(value))return value.every(item=>payloadAllowed(item,key));
  if(value&&typeof value==='object')return Object.entries(value).every(([field,item])=>payloadAllowed(item,key==='answers'?'answer':field));
  return typeof value!=='string'||(!TEXT_KEYS.has(key)&&key!=='answer')||languageAllowed(value);
}
export function assertLanguagePayload(value){if(!payloadAllowed(value))throw Error(LANGUAGE_MESSAGE);}
export const displayUserText=value=>languageAllowed(value)?value:'Text needs revision.';
export function displayPayload(value,key=''){
  if(key==='questions'&&Array.isArray(value))return value.map(item=>item&&typeof item==='object'&&'answer' in item?{...item,answer:displayPayload(item.answer,'answer')}:item);
  if(SKIP.has(key))return value;
  if(Array.isArray(value))return value.map(item=>displayPayload(item,key));
  if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([field,item])=>[field,displayPayload(item,key==='answers'?'answer':field)]));
  return typeof value==='string'&&(TEXT_KEYS.has(key)||key==='answer')?displayUserText(value):value;
} 

export function installLanguageGuard(doc=document){
  const editable=field=>field?.matches('textarea,input[type=text],input:not([type]),input[type=search],input[type=email],input[type=tel]')&&!/(?:^|[-_])(password|passphrase|code|recovery|token|url|link)(?:$|[-_])/i.test(field.name||'')&&!(field.name==='username'&&field.closest('form')?.dataset.form==='mentor-auth'&&field.closest('form').dataset.mode!=='setup');
  let nextId=0;
  function validate(field){
    if(!editable(field))return true;
    const ok=languageAllowed(field.value),existing=field.parentElement.querySelector('[data-language-error]');
    if(!ok){
      field.setCustomValidity(LANGUAGE_MESSAGE);field.setAttribute('aria-invalid','true');field.dataset.languageBlocked='';
      if(!existing){const error=doc.createElement('span');error.dataset.languageError='';error.className='language-error';error.id='language-error-'+(++nextId);error.setAttribute('role','alert');error.textContent=LANGUAGE_MESSAGE;field.insertAdjacentElement('afterend',error);field.setAttribute('aria-describedby',((field.getAttribute('aria-describedby')||'')+' '+error.id).trim());}
    }else if(field.dataset.languageBlocked!==undefined){
      if(field.validationMessage===LANGUAGE_MESSAGE)field.setCustomValidity('');
      field.removeAttribute('aria-invalid');delete field.dataset.languageBlocked;
      if(existing){field.setAttribute('aria-describedby',(field.getAttribute('aria-describedby')||'').split(' ').filter(id=>id!==existing.id).join(' '));existing.remove();}
    }
    return ok;
  }
  const fields=root=>[...root.querySelectorAll('input,textarea')].filter(editable);
  const blocked=root=>fields(root).find(field=>!validate(field));
  const rejectEdit=event=>{if(!validate(event.target))event.stopImmediatePropagation();};
  doc.addEventListener('input',rejectEdit,true);
  doc.addEventListener('change',rejectEdit,true);
  doc.addEventListener('keydown',event=>{if(event.key==='Enter'&&event.target.tagName==='INPUT'&&!validate(event.target)){event.preventDefault();event.stopImmediatePropagation();}},true);
  doc.addEventListener('submit',event=>{const field=blocked(event.target);if(field){event.preventDefault();event.stopImmediatePropagation();field.focus();}},true);
  doc.addEventListener('click',event=>{
    const button=event.target.closest('button');if(!button)return;
    const action=button.dataset.action||button.dataset.scenario||button.dataset.pcAction||'';
    if(button.dataset.pcAction===undefined&&!/^(?:form-submit|starting-write|start-check|finish|check|advance|mission-next|save|add|send|read$)/.test(action))return;
    const section=button.closest('form,.mission-lab,.lesson-copy,.card')||doc;
    const field=blocked(section);if(field){event.preventDefault();event.stopImmediatePropagation();field.focus();}
  },true);
  const scan=()=>fields(doc).forEach(validate);
  const observer=new MutationObserver(scan);observer.observe(doc.body,{childList:true,subtree:true});scan();
  return {validate,scan,stop:()=>observer.disconnect()};
}
