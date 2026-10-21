import assert from 'node:assert/strict';
import {demoMentor,mountDemoMentor} from './dist/public-demo.js';

function reviewForm(){
  const listeners={},inputListeners={},attributes=new Map();
  const input={value:'',focused:false,
    addEventListener(name,listener){inputListeners[name]=listener;},
    setAttribute(name,value){attributes.set(name,value);},
    removeAttribute(name){attributes.delete(name);},
    focus(){this.focused=true;}
  };
  const output={innerHTML:''};
  const form={elements:{note:input},querySelector(){return output;},
    addEventListener(name,listener){listeners[name]=listener;}
  };
  mountDemoMentor({querySelector(){return form;}});
  return {input,output,attributes,
    type(value){input.value=value;inputListeners.input?.();},
    submit(){let prevented=false;listeners.submit({preventDefault(){prevented=true;}});assert(prevented);}
  };
}

const blank=reviewForm();
blank.type('   ');blank.submit();
assert.match(blank.output.innerHTML,/Write a short note/,'Whitespace-only notes need an explanation.');
assert.equal(blank.attributes.get('aria-invalid'),'true');
assert(blank.input.focused,'Return keyboard focus to the note that needs attention.');

blank.type('You checked by adding back. Next, try 9 cartons.');
assert(!blank.attributes.has('aria-invalid'),'Editing should clear the stale invalid state.');
blank.submit();
assert.match(blank.output.innerHTML,/The sample learner would see:/);
assert.match(blank.output.innerHTML,/Next, try 9 cartons/);
assert.doesNotMatch(blank.output.innerHTML,/Write a short note/);

blank.type('   ');blank.submit();
assert.doesNotMatch(blank.output.innerHTML,/The sample learner would see:/,'A blank retry must not leave an old preview visible.');

const literal=reviewForm();
literal.type('Use <b>3</b> & check 4 + 3 = 7.');literal.submit();
assert.match(literal.output.innerHTML,/&lt;b&gt;3&lt;\/b&gt; &amp;/,'Notes remain escaped text.');
assert.doesNotMatch(literal.output.innerHTML,/<b>/);

assert.match(demoMentor(),/aria-describedby="demo-feedback-result"/);
assert.match(demoMentor(),/id="demo-feedback-result"[^>]*role="status"/);
assert.doesNotThrow(()=>mountDemoMentor({querySelector(){return null;}}));
console.log(JSON.stringify({mentorFeedbackChecks:5,whitespaceExplained:true,stalePreviewRemoved:true,keyboardFocusReturned:true,noteTextEscaped:true,realRecordsUsed:false}));
