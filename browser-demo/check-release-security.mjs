import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {publicDemoRequest,demoPracticeScope} from './dist/public-demo.js';
import {dailyDay} from './dist/daily-tasks.js';
import {createReader,voiceOptions} from './dist/read-aloud.js';

const html=await fs.readFile('dist/index.html','utf8');
assert.equal(demoPracticeScope(''),'public-demo');
assert.equal(demoPracticeScope('?practice=release-check-120'),'public-demo-test-release-check-120');
for(const value of ['../other','x'.repeat(65),'','<script>'])assert.equal(demoPracticeScope('?practice='+encodeURIComponent(value)),'public-demo');
const headers=await fs.readFile('dist/_headers','utf8');
for(const directive of ["script-src 'self'", "connect-src 'self'", "object-src 'none'", "worker-src 'none'", "form-action 'none'"]){
  assert(html.includes(directive),directive);
  assert(headers.includes(directive),directive);
}
assert(!/script-src[^;]*unsafe-inline/.test(html));
assert(!/script-src[^;]*unsafe-eval/.test(html));
assert(headers.includes("frame-ancestors 'none'"));
assert(!html.includes('header-install'));
for(const path of ['/api/me','/api/mentor','/api/join','/api/login','/api/mentor/invite','/api/mentor/review','/api/reward']){
  await assert.rejects(publicDemoRequest(path,{code:'fictional',note:'fictional'}));
}
const dates=[['2026-01-07T05:59:59Z','2026-01-06'],['2026-10-31T04:59:59Z','2026-10-30'],['2026-10-31T05:00:00Z','2026-10-31'],['2026-12-07T04:59:59Z','2026-12-06'],['2026-12-07T05:00:00Z','2026-12-07']];
for(const [at,day] of dates)assert.equal(dailyDay(Date.parse(at)),day);

// Exercise the privacy boundary: a selected remote voice must never receive text.
let voices=[], spoken=[], networkCalls=0;
const voiceAPI={getVoices:()=>voices,cancel:()=>{},speak:speech=>spoken.push(speech)};
globalThis.window={speechSynthesis:voiceAPI};
globalThis.speechSynthesis=voiceAPI;
globalThis.SpeechSynthesisUtterance=class{constructor(text){this.text=text;}};
globalThis.fetch=()=>{networkCalls++;throw Error('Unexpected speech request');};
const span={textContent:''}, button={addEventListener(){}};
globalThis.document={body:{append(){}},createElement:()=>({hidden:true,className:'',innerHTML:'',querySelector:selector=>selector==='span'?span:button}),addEventListener(){},getElementById:()=>null};
window.addEventListener=()=>{};
const remote={voiceURI:'remote-test',name:'Remote test voice',lang:'en-CA',localService:false};
const local={voiceURI:'local-test',name:'Local test voice',lang:'en-CA',localService:true};
const messages=[];
const reader=createReader({settings:()=>({voice:'device:remote-test'}),toast:message=>messages.push(message),softVoice:()=>false,localOnly:true});
voices=[remote];
assert(!voiceOptions('soft',false,true).includes('remote-test'));
await reader.read('Fictional practice text.');
assert.equal(spoken.length,0);
assert(messages.some(message=>message.includes('No local English voice')));
voices=[remote,local];
await reader.read('Fictional practice text.');
assert.equal(spoken.length,1);
assert.equal(spoken[0].voice,local);
assert.equal(networkCalls,0);

const result={accountRoutesBlocked:7,sameOriginConnectionsOnly:true,inlineScriptsAndEvalBlocked:true,remoteVoicesBlocked:true,missingLocalVoiceHandled:true,late2026DatesConsistent:true};
console.log(JSON.stringify(result));
