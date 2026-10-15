import {escapeHTML as esc} from './engine.js?build=123';

export const ANSWER_PAUSE_MS=8000;

export function successMarkup(ready,text='Continue when you’re ready.'){
  return `<div class="mission-success" data-mission-success ${ready?'':'hidden'}><span class="success-symbol" aria-hidden="true">✓</span><div><strong role="status">Correct!</strong><p class="legend" data-next-note>${esc(text)}</p><div class="next-countdown" data-next-countdown hidden><progress max="8" value="8" aria-label="Time before the next part"></progress><span data-next-seconds aria-hidden="true">8s</span></div></div></div>`;
}

export function createLessonAdvance({now=()=>performance.now(),setTimer=setTimeout,clearTimer=clearTimeout}={}){
  let timer,generation=0,surface=null;
  function showStop(show){
    const button=surface?.parentElement?.querySelector('[data-action="mission-hold"]');
    if(button)button.hidden=!show;
  }
  function paint(remaining){
    if(!surface)return;
    const seconds=Math.ceil(remaining/1000);
    const bar=surface.querySelector('progress');
    bar.value=remaining/1000;
    bar.setAttribute('aria-valuetext',`${seconds} seconds until the next part`);
    surface.querySelector('[data-next-seconds]').textContent=`${seconds}s`;
  }
  function cancel(){
    clearTimer(timer);timer=undefined;generation++;
    if(surface){
      showStop(false);
      surface.classList.remove('celebrate');
      surface.querySelector('[data-next-countdown]').hidden=true;
      surface.querySelector('[data-next-note]').textContent='Auto-next stopped. Choose Next when you’re ready.';
    }
    surface=null;
  }
  function schedule(valid,next,element=null,motion=true){
    cancel();surface=element;
    const token=generation,deadline=now()+ANSWER_PAUSE_MS;
    if(surface){
      showStop(true);
      surface.classList.toggle('celebrate',motion);
      surface.querySelector('[data-next-countdown]').hidden=false;
      surface.querySelector('[data-next-note]').textContent='Next part in 8 seconds. Press Stop to stay and read.';
      paint(ANSWER_PAUSE_MS);
    }
    function tick(){
      if(token!==generation)return;
      if(!valid()){cancel();return;}
      const remaining=Math.max(0,deadline-now());paint(remaining);
      if(!remaining){timer=undefined;showStop(false);surface=null;next();return;}
      timer=setTimer(tick,Math.min(100,remaining));
    }
    timer=setTimer(tick,100);
  }
  return {cancel,schedule};
}
