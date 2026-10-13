import {languageAllowed,LANGUAGE_MESSAGE} from './language.js?build=119';
import {escapeHTML as esc,readable} from './engine.js?build=119';

export function narrationText(target){
  const copy=target.cloneNode(true);
  copy.querySelectorAll('[hidden],details:not([open]) > :not(summary),.speech-player').forEach(el=>el.remove());
  copy.querySelectorAll('[data-say]').forEach(el=>el.replaceWith(document.createTextNode(el.dataset.say)));
  copy.querySelectorAll('[role="img"][aria-label]').forEach(el=>el.replaceWith(document.createTextNode(el.getAttribute('aria-label')+'. ')));
  copy.querySelectorAll('button,input,select,textarea,.katex-html,annotation').forEach(el=>el.remove());
  copy.querySelectorAll('p,h1,h2,h3,h4,li,legend,blockquote,tr,label,output,.pill,.quantity-control>span').forEach(el=>el.append(document.createTextNode('. ')));
  return readable(copy.textContent).replace(/\s*([+=])\s*/g,(_,s)=>s==='+'?' plus ':' equals ').replace(/\.{2,}/g,'.').replace(/\s+/g,' ').trim();
}
export function speechChunks(text){
  const chunks=[];let remaining=text.trim();
  while(remaining.length){
    const limit=chunks.length?360:180;
    if(remaining.length<=limit){chunks.push(remaining);break;}
    const lead=remaining.slice(0,limit),sentence=Math.max(lead.lastIndexOf('. '),lead.lastIndexOf('? '),lead.lastIndexOf('! '));
    const end=sentence>100?sentence+1:Math.max(1,lead.lastIndexOf(' '));
    chunks.push(remaining.slice(0,end).trim());remaining=remaining.slice(end).trimStart();
  }
  return chunks;
}
export function voiceOptions(selected='soft',soft=true){
  return `<option value="soft" ${selected==='soft'?'selected':''}>${soft?'Soft voice':'Soft voice (not set up here; the device voice reads instead)'}</option><option value="device:auto" ${selected==='device:auto'?'selected':''}>Device default</option>`+(window.speechSynthesis?.getVoices()||[]).filter(v=>v.lang.startsWith('en')).map(v=>`<option value="${esc('device:'+v.voiceURI)}" ${selected==='device:'+v.voiceURI?'selected':''}>${esc(v.name)} · ${esc(v.lang)}</option>`).join('');
}

export function createReader({settings,toast,softVoice=()=>undefined}){
  let generation=0,controller,context,source,control;
  const player=document.createElement('div');player.className='speech-player';player.hidden=true;
  player.innerHTML='<span role="status" aria-live="polite"></span><button class="btn secondary" type="button">Stop reading</button>';
  document.body.append(player);player.querySelector('button').addEventListener('click',stop);
  const status=message=>{player.hidden=false;player.querySelector('span').textContent=message;};
  function stop(){
    generation++;controller?.abort();controller=null;
    if(source){try{source.stop();}catch{}source=null;}
    window.speechSynthesis?.cancel();player.hidden=true;
    control?.removeAttribute('aria-pressed');control?.removeAttribute('aria-busy');control=null;
  }
  function speakDevice(text,chosen,token,note='Reading aloud'){
    const speech=new SpeechSynthesisUtterance(text);speech.rate=.98;
    const selected=speechSynthesis.getVoices().find(v=>'device:'+v.voiceURI===chosen);if(selected)speech.voice=selected;
    speech.onend=()=>{if(token===generation)stop();};
    speech.onerror=()=>{if(token===generation){stop();toast('That device voice could not play. Choose another voice in Reading & comfort.');}};
    status(note);speechSynthesis.speak(speech);
  }
  async function read(text,button){
    if(!languageAllowed(text)){stop();toast(LANGUAGE_MESSAGE);return;}
    if(button&&button===control){stop();return;}
    stop();const token=generation;control=button;control?.setAttribute('aria-pressed','true');
    (button?.closest('dialog')||document.body).append(player);
    let chosen=settings().voice||'soft';
    if(!text.trim()){toast('There is no text to read here yet.');stop();return;}
    // The soft voice runs on the Stepstone host. When it is not set up there, read with the device voice.
    if(chosen==='soft'&&softVoice()===false&&window.speechSynthesis)chosen='device:auto';
    if(chosen.startsWith('device:')){
      if(!window.speechSynthesis){stop();toast('This browser has no device voice. Choose Soft voice.');return;}
      speakDevice(text,chosen,token);return;
    }
    const AudioEngine=window.AudioContext||window.webkitAudioContext;
    if(!AudioEngine){stop();toast('Choose a device voice in Reading & comfort.');return;}
    // Unlock audio in the tap handler before waiting for the server.
    context??=new AudioEngine();const resumed=context.resume();
    controller=new AbortController();const signal=controller.signal;
    const chunks=speechChunks(text);let part=0;
    try{
      await resumed;
      // Prepare one following section during playback, without unhandled errors
      // or leaving a late request playing after Stop / route changes.
      const load=async text=>{
        try{
          const response=await fetch('/api/read-aloud',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text}),cache:'no-store',signal});
          if(!response.ok){const error=await response.json();throw new Error(error.error||'The soft voice is unavailable.');}
          return {buffer:await context.decodeAudioData(await response.arrayBuffer())};
        }catch(error){return {error};}
      };
      let pending=load(chunks[0]);
      for(let i=0;i<chunks.length;i++){
        if(token!==generation)return;part=i;
        status(i===0?'Preparing the soft voice…':'Reading the next part…');control?.setAttribute('aria-busy','true');
        const {buffer,error}=await pending;if(error)throw error;
        if(token!==generation)return;
        if(i+1<chunks.length)pending=load(chunks[i+1]);
        status('Reading aloud');control?.removeAttribute('aria-busy');
        const playing=source=context.createBufferSource();playing.buffer=buffer;playing.connect(context.destination);
        await new Promise(resolve=>{playing.onended=resolve;playing.start();});
        if(source===playing)source=null;
      }
      if(token===generation)stop();
    }catch(error){
      if(token!==generation)return;
      if(error.name!=='AbortError'&&window.speechSynthesis){speakDevice(chunks.slice(part).join(' '),'device:auto',token,'The soft voice is unavailable. Reading with the device voice.');return;}
      stop();if(error.name!=='AbortError')toast(error.message||'The voice could not play. Try again.');
    }
  }
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  document.getElementById('dialog')?.addEventListener('close',stop);
  window.addEventListener('pagehide',stop);
  return {read,stop};
}
