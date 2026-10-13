import {escapeHTML as esc} from './engine.js?build=121';
import {avatar} from './home.js?build=121';

export function canMessageMentor(account){return !!account?.id&&!account.personal;}

export function messageInbox(items=[],learners=[]){
  const unread=items.reduce((sum,item)=>sum+item.unread,0);
  return `<section class="manager-list" id="manager-messages" tabindex="-1"><div class="section-title"><span class="pill">${unread} unread</span></div><p class="legend">Fixed support requests and replies with your connected learners. Free-text chat, attachments and AI replies are unavailable.</p>${items.length?items.map(item=>`<div class="message-inbox-row"><div><div class="signal-identity">${avatar(learners.find(l=>l.id===item.id)?.profile?.avatar||'fox',44)}<h3>${esc(item.alias)}</h3></div><p class="small ${item.unread?'message-unread':''}">${item.unread?item.unread+' unread':'Up to date'} · ${item.total} ${item.total===1?'signal':'signals'}</p></div><button class="btn secondary" data-action="message-thread" data-id="${esc(item.id)}">Open requests</button></div>`).join(''):'<p class="empty">A learner’s preset requests will appear here.</p>'}</section>`;
}

export function createSignalDrafts({storage=()=>sessionStorage,uuid=()=>crypto.randomUUID()}={}){
  const prefix='stepstone-support-selection-v1:',cache=new Map();
  const validChoice=value=>typeof value==='string'&&/^[a-z][a-z-]{0,30}$/.test(value);
  function get(key){
    if(cache.has(key))return cache.get(key);
    let saved;try{saved=JSON.parse(storage().getItem(prefix+key)||'null');}catch{}
    const p=saved?.pending;
    const draft={choice:validChoice(saved?.choice)?saved.choice:'',pending:p&&validChoice(p.choice)&&/^[A-Za-z0-9_-]{12,80}$/.test(p.clientId)?{choice:p.choice,clientId:p.clientId}:null,saved:true};
    cache.set(key,draft);return draft;
  }
  function persist(key){
    const draft=get(key);
    try{if(draft.choice||draft.pending)storage().setItem(prefix+key,JSON.stringify({choice:draft.choice,pending:draft.pending}));else storage().removeItem(prefix+key);draft.saved=true;}catch{draft.saved=false;}
    return draft;
  }
  return {
    get,
    select(key,choice){if(!validChoice(choice))throw Error('Choose a preset option.');get(key).choice=choice;return persist(key);},
    begin(key){const draft=get(key);if(!draft.pending){if(!draft.choice)throw Error('Choose a preset option first.');draft.pending={choice:draft.choice,clientId:uuid()};persist(key);}return {...draft.pending};},
    acknowledge(key,id){const draft=get(key);if(draft.pending?.clientId===id){if(draft.choice===draft.pending.choice)draft.choice='';draft.pending=null;persist(key);}return draft;},
    reject(key,id){const draft=get(key);if(draft.pending?.clientId===id){draft.pending=null;persist(key);}return draft;},
    clear(forget=false){cache.clear();if(forget)try{const s=storage(),keys=[];for(let i=0;i<s.length;i++){const k=s.key(i);if(k?.startsWith(prefix)||k?.startsWith('stepstone-message-draft-v1:'))keys.push(k);}for(const k of keys)s.removeItem(k);}catch{}}
  };
}

export function createInbox({api,me,mentor,identity=()=>null,modal,dialog,toast,refresh}){
  let context=null;const drafts=createSignalDrafts();
  const key=c=>(c.manager?'mentor:':'learner:')+c.id;
  const valid=c=>context===c&&(c.manager?mentor():me()?.id===c.id&&!me()?.personal);
  const path=(c,action)=>(c.manager?'/api/mentor/messages/':'/api/messages/')+action;
  async function open(id){
    if(id?!mentor():!canMessageMentor(me()))return;
    const c={manager:!!id,id:id||me().id};context=c;
    modal('Opening support requests…','<p data-message-loading>Your support requests are loading.</p>');
    const loading=dialog.querySelector('[data-message-loading]');
    try{const data=await api(path(c,'thread'),{learner:c.id});if(valid(c)&&dialog.open&&loading.isConnected)show(c,data);}
    catch(error){if(valid(c)&&dialog.open&&loading.isConnected)modal('Requests could not open','<p>'+esc(error.message)+'</p><button class="btn" data-action="'+(c.manager?'message-thread':'messages')+'" data-id="'+esc(c.id)+'">Try again</button>');}
  }
  function show(c,data){
    if(!valid(c))return;
    const draft=drafts.get(key(c)),options=Array.isArray(data.options)?data.options:[],pip=identity(c.id);
    modal(c.manager?'Support for '+data.alias:'Support from my mentor',`<div class="signal-identity">${avatar(pip?.profile?.avatar||'fox',44)}<strong>${esc(data.alias)}</strong></div><p class="legend">Choose a fixed ${c.manager?'reply':'request'}. Only ${c.manager?'this learner':'your assigned mentor'} can receive it.</p><div class="buttons">${data.hasOlder?'<button class="btn secondary small" data-message-older>Earlier requests</button>':''}<button class="btn secondary small" data-message-latest>Refresh latest</button></div><div class="message-thread-list" aria-label="Support history">${data.messages.length?data.messages.map(m=>`<article class="text-message ${m.sender==='mentor'?'mentor-message':''}"><small>${m.sender==='mentor'?'Mentor':esc(data.alias)} · ${esc(new Date(m.created*1000).toLocaleString())}</small><p>${esc(m.body)}</p></article>`).join(''):'<p>No requests yet.</p>'}</div>${options.length?`<form class="support-composer"><fieldset><legend>${c.manager?'Choose your reply':'What do you need?'}</legend><div class="support-choices">${options.map(o=>`<label class="support-choice"><input type="radio" name="choice" value="${esc(o.id)}" ${draft.choice===o.id?'checked':''}><span>${esc(o.label)}</span></label>`).join('')}</div></fieldset><p class="small" data-message-draft></p><p class="notice" data-message-pending ${draft.pending?'':'hidden'}>Your last send is not confirmed. Retry checks the same send.</p><p class="error-text" data-message-error role="alert"></p><button class="btn" type="submit">${draft.pending?'Retry send':'Send '+(c.manager?'reply':'request')}</button><p class="small" data-message-status role="status"></p></form>`:'<p class="notice">Preset requests need the updated Stepstone server. Free-text chat is unavailable.</p>'}`);
    const form=dialog.querySelector('.support-composer'),submit=form?.querySelector('[type=submit]');
    function showSelection(){
      form.querySelector('[data-message-draft]').textContent=draft.choice||draft.pending?(draft.saved?'Your selection is saved in this tab.':'Your selection could not be saved. Keep this window open.'):'Choose one option. Nothing sends until you press Send.';
      form.querySelector('[data-message-pending]').hidden=!draft.pending;
      submit.textContent=draft.pending?'Retry send':'Send '+(c.manager?'reply':'request');
      submit.disabled=!draft.choice&&!draft.pending;
      form.querySelectorAll('input').forEach(input=>input.disabled=!!draft.pending);
    }
    if(form){
      showSelection();
      form.addEventListener('change',event=>{if(event.target.name==='choice'){drafts.select(key(c),event.target.value);showSelection();}});
      form.addEventListener('submit',async event=>{
        event.preventDefault();if(submit.disabled||!valid(c))return;
        const request=drafts.begin(key(c));submit.disabled=true;form.querySelector('[data-message-error]').textContent='';form.querySelector('[data-message-status]').textContent='Sending…';
        let sent=false;
        try{
          await api(path(c,'send'),{learner:c.id,...request});
          sent=true;drafts.acknowledge(key(c),request.clientId);if(!valid(c))return;
          form.querySelectorAll('input').forEach(input=>input.checked=input.value===draft.choice);showSelection();
          form.querySelector('[data-message-status]').textContent='Saved. Refresh latest to see it.';
          const result=await api(path(c,'thread'),{learner:c.id});
          if(valid(c)&&dialog.open&&form.isConnected){show(c,result);dialog.querySelector('[data-message-status]').textContent='Sent. It is saved in your support history.';}
          refresh();
        }catch(error){if(valid(c)&&form.isConnected){if(!sent&&[400,401,403,409,413,429].includes(error.status))drafts.reject(key(c),request.clientId);showSelection();form.querySelector('[data-message-error]').textContent=error.message;if(!sent)form.querySelector('[data-message-status]').textContent=draft.pending?'Not confirmed. Retry checks the same send without adding a second copy.':'Not sent. Your selection stays here.';}}
        finally{if(submit.isConnected)submit.disabled=!draft.choice&&!draft.pending;}
      });
    }
    async function page(before){
      if(!valid(c))return;
      const control=dialog.querySelector(before?'[data-message-older]':'[data-message-latest]');control.disabled=true;
      try{const result=await api(path(c,'thread'),{learner:c.id,...(before?{before}:{})});if(valid(c)&&dialog.open&&control.isConnected)show(c,result);refresh();}
      catch(error){toast(error.message);}finally{if(control.isConnected)control.disabled=false;}
    }
    dialog.querySelector('[data-message-older]')?.addEventListener('click',()=>page(data.messages[0].id));
    dialog.querySelector('[data-message-latest]').addEventListener('click',()=>page());refresh();
  }
  return {open,clear(forget=false){context=null;drafts.clear(forget);}};
}
