import assert from 'node:assert/strict';
import {canMessageMentor,createInbox,createSignalDrafts} from '../public/mentor-messages.js';

for(const account of [null,{alias:'Preview'},{id:'own',personal:true}])assert.equal(canMessageMentor(account),false);
assert.equal(canMessageMentor({id:'connected'}),true);
for(const account of [null,{id:'own',personal:true}]){
 let calls=0,windows=0;const inbox=createInbox({api:()=>calls++,me:()=>account,mentor:()=>false,modal:()=>windows++,dialog:{},toast(){},refresh(){}});
 await inbox.open();await inbox.open('other');assert.equal(calls,0);assert.equal(windows,0);
}
function storage(){const data=new Map();return {get length(){return data.size;},key:i=>[...data.keys()][i],getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k)};}
const tab=storage();let sequence=0;const fresh=()=>createSignalDrafts({storage:()=>tab,uuid:()=>`test-send-id-${++sequence}`});
let drafts=fresh();drafts.select('learner:one','stuck');
drafts=fresh();assert.equal(drafts.get('learner:one').choice,'stuck');assert.equal(drafts.get('learner:two').choice,'');assert.equal(drafts.get('mentor:one').choice,'');
const pending=drafts.begin('learner:one');drafts=fresh();assert.deepEqual(drafts.begin('learner:one'),pending);
drafts.select('learner:one','review');assert.deepEqual(drafts.begin('learner:one'),pending);
drafts.acknowledge('learner:one',pending.clientId);assert.equal(drafts.get('learner:one').choice,'review');
const next=drafts.begin('learner:one');assert.notEqual(next.clientId,pending.clientId);drafts.acknowledge('learner:one',pending.clientId);assert.deepEqual(drafts.get('learner:one').pending,next);
drafts.acknowledge('learner:one',next.clientId);assert.equal(drafts.get('learner:one').choice,'');assert.equal(tab.length,0);
drafts.select('learner:one','feedback');const rejected=drafts.begin('learner:one');drafts.reject('learner:one',rejected.clientId);assert.equal(drafts.get('learner:one').choice,'feedback');assert.notEqual(drafts.begin('learner:one').clientId,rejected.clientId);
drafts.select('mentor:one','reviewing');tab.setItem('stepstone-message-draft-v1:learner:old','old text');tab.setItem('unrelated','keep');drafts.clear(true);assert.equal(tab.length,1);assert.equal(tab.getItem('unrelated'),'keep');
assert.throws(()=>fresh().select('learner:one','arbitrary text!'),/preset/);assert.throws(()=>fresh().begin('learner:empty'),/Choose/);
tab.setItem('stepstone-support-selection-v1:learner:one',JSON.stringify({choice:'<script>',pending:{choice:'stuck',clientId:'bad'}}));assert.equal(fresh().get('learner:one').choice,'');assert.equal(fresh().get('learner:one').pending,null);
const denied=createSignalDrafts({storage:()=>{throw Error('Denied');},uuid:()=>`test-send-id-${++sequence}`});assert.equal(denied.select('learner:one','stuck').saved,false);assert.equal(denied.begin('learner:one').choice,'stuck');
for(const rejects of [false,true]){
 let settle,panels=0;const loading={isConnected:true},dialog={open:true,querySelector:()=>loading};
 const inbox=createInbox({api:()=>new Promise((resolve,reject)=>{settle=rejects?reject:resolve;}),me:()=>({id:'one'}),mentor:()=>false,modal:()=>panels++,dialog,toast(){},refresh(){}});
 const opening=inbox.open();loading.isConnected=false;settle(rejects?Error('Offline'):{messages:[],options:[]});await opening;assert.equal(panels,1);
}
console.log('PASS: connected-only signals, selection reload, separate owners, stable uncertain retries, stale responses, rejection, old-draft cleanup, denied storage and late-dialog protection.');
