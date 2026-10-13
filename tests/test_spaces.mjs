import assert from 'node:assert/strict';
import {resolveEntryRole,roleEntry,learnerSpace,managerNavigation} from '../public/manager.js';

assert.equal(resolveEntryRole(),null);
assert.equal(resolveEntryRole({hasLearning:true}),'learner');
assert.equal(resolveEntryRole({choice:'mentor'}),'mentor');
assert.equal(resolveEntryRole({choice:'invalid'}),null);
assert.equal(resolveEntryRole({account:{id:'learner'},choice:'mentor'}),'learner');
assert.equal(resolveEntryRole({account:{id:'own',personal:true},choice:'learner'}),'mentor');
assert.match(roleEntry(),/data-role="learner"/);
assert.match(roleEntry(),/data-role="mentor"/);
assert.match(learnerSpace(null),/data-action="messages"[^>]+disabled/);
assert.ok(!/data-action="messages"[^>]+disabled/.test(learnerSpace({id:'connected'})));
assert.match(learnerSpace({id:'connected',messagesUnread:2}),/2 new replies/);
assert.match(learnerSpace({id:'connected'},{locked:true}),/Tour first/);
assert.ok(!learnerSpace({id:'connected'}).includes('manager-section'));
assert.ok(!learnerSpace({id:'connected'}).includes('<textarea'));
assert.match(managerNavigation({}),/data-section="messages"/);
console.log('PASS: new-role choice, preserved legacy learning, authenticated-role precedence, gated learner requests and separate manager controls.');
