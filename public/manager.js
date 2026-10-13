import {escapeHTML as esc} from './engine.js?build=121';
import {companionSprite} from './companion.js?build=121';
import {INTERFACE_BUILD} from './release.js?build=121';

const hubMarks={
 account:'<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-2 2M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l2-2"/>',
 messages:'<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 9h8M8 12h5"/>',
 'learner-feedback':'<path d="m5 12 4 4L19 6"/>',
 'learner-rewards':'<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M3 9V6h18v3M12 6v14M12 6C7 6 6 3 8 2c2-1 4 2 4 4Zm0 0c5 0 6-3 4-4-2-1-4 2-4 4Z"/>',
 learners:'<circle cx="9" cy="7" r="3"/><path d="M3 20v-3a6 6 0 0 1 12 0v3M17 4a3 3 0 0 1 0 6M18 14a5 5 0 0 1 3 5"/>',
 inbox:'<path d="M4 4h16v16H4V4ZM4 14h5l1 3h4l1-3h5M8 8h8M8 11h8"/>',
 invites:'<circle cx="9" cy="7" r="3"/><path d="M3 20v-3a6 6 0 0 1 12 0v3M19 7v6M16 10h6"/>',
 personal:'<path d="M4 10a8 8 0 1 1 1 8M4 4v6h6"/>',
 settings:'<path d="M4 6h3M11 6h9M4 12h9M17 12h3M4 18h3M11 18h9"/><circle cx="9" cy="6" r="2"/><circle cx="15" cy="12" r="2"/><circle cx="9" cy="18" r="2"/>'
};
function hubMark(kind){return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${hubMarks[kind]||hubMarks['learner-rewards']}</svg>`;}

export function resolveEntryRole({account,choice,hasLearning=false}={}){
  if(account)return account.personal?'mentor':'learner';
  if(['learner','mentor'].includes(choice))return choice;
  return hasLearning?'learner':null;
}

export function spaceGuide(role,text){
  return `<aside class="space-guide" data-guide-role="${role==='mentor'?'mentor':'learner'}">${companionSprite(role==='mentor'?'owl':'fox',64)}<p><strong>${role==='mentor'?'Mentor Pip':'Learner Pip'}</strong> <span>${esc(text)}</span></p></aside>`;
}

export function roleEntry(){
  return `<section class="welcome-box card role-entry"><p class="eyebrow">WELCOME TO STEPSTONE</p><h1>How will you use Stepstone?</h1><div class="role-options"><button class="role-choice" data-action="choose-role" data-role="learner">${companionSprite('fox',88)}<strong>I’m learning</strong> <span>Develop practical skills and work towards your goals.</span> <b>Start learning →</b></button><button class="role-choice" data-action="choose-role" data-role="mentor">${companionSprite('owl',88)}<strong>I’m mentoring</strong> <span>Set up your private dashboard and invite learners.</span> <b>Set up my mentor space →</b></button></div></section>`;
}

export function learnerSpace(account,{locked=false}={}){
  const connected=!!account?.id&&!account.personal,unread=account?.messagesUnread||0;
  const card=(title,detail,count,action,accent)=>`<button class="manager-card" data-action="${action}" style="--card-accent:${accent}" ${action==='messages'&&!connected?'disabled':''}><span class="manager-card-top">${hubMark(action)}<span>${esc(count)}</span></span><strong>${title}</strong><span class="manager-card-detail">${detail}</span><span class="manager-card-open">${action==='messages'&&!connected?'Connect first':'Open →'}</span></button>`;
  return `<section class="learner-mentor-space" aria-labelledby="mentor-space-title"><div class="page-head"><div><h1 id="mentor-space-title">Mentor space</h1></div></div><nav class="manager-nav learner-hub" aria-label="Your mentor hub">${card(connected?'My connection':'Connect with my mentor',connected?'View your sign-in details or switch learners.':'Use your invitation link or code to save with your mentor.',connected?'Connected':'Not connected','account','#8cf0de')}${card('Support requests','Choose a preset request. Your mentor can send a preset reply.',unread?unread+' new '+(unread===1?'reply':'replies'):'Preset messages only','messages','#c9b4fc')}${card('My feedback',locked?'Finish the guided tour, then check your mentor’s feedback.':'See your completed checks and your mentor’s feedback.',locked?'Tour first':'My wins','learner-feedback','#9be5c4')}${card('My reward goals',locked?'Finish the guided tour, then choose and request rewards.':'See your goal, requirements and reward requests.',locked?'Tour first':'Rewards','learner-rewards','#ffd197')}</nav><div class="buttons hub-footer">${locked?'<a class="btn secondary" href="#home">Continue my setup →</a>':'<a class="btn secondary" href="#home">Back to Home</a>'}<button class="btn secondary small" data-action="mentor-sign-in">Use a mentor account</button></div></section>`;
}

export function managerNavigation(mentor={}){
  const unread=(mentor.messages||[]).reduce((n,m)=>n+m.unread,0),reports=(mentor.reports||[]).filter(r=>!r.reviewed).length,claims=[...(mentor.claims||[]),...(mentor.aiMonths||[])].filter(c=>['pending','approved'].includes(c.status)).length;
  const cards=[['learners','Learners','View learning, goals and account access.',mentor.learners?.length||0,'↗'],['messages','Support requests','Read learner requests and choose preset replies.',unread+' unread','✉'],['inbox','Progress inbox','Review completed checks and give feedback.',reports+' to review','✓'],['invites','Invitations','Create a private invitation for a new learner.','One-use links','＋'],['rewards','Rewards & funding','Manage goals, stock, requests and delivery.',claims+' '+(claims===1?'request':'requests'),'◇'],['personal','My test space','Try the app with your own separate progress.','Reset or replay','↺'],['settings','Account & settings','Manage sign-in, your device and recovery.','Private controls','⚙']];
  return `<nav class="manager-nav" aria-label="Manage Stepstone">${cards.map(([id,label,detail,count],i)=>`<button class="manager-card" data-action="manager-section" data-section="${id}" style="--card-accent:${['#94dfff','#c9b4fc','#9be5c4','#8cf0de','#ffd197','#bdc5ff','#a7cded'][i]}"><span class="manager-card-top">${hubMark(id)}<span>${esc(String(count))}</span></span><strong>${label}</strong><span class="manager-card-detail">${detail}</span><span class="manager-card-open">Open <span aria-hidden="true">→</span></span></button>`).join('')}</nav>`;
}

function mentorClaim(health={}){
 return health.localClaim?`<details><summary>Keep the existing records on this host</summary><label class="check-label"><input name="claimExisting" type="checkbox" checked><span>I manage this installation and want these existing records in my account.</span></label>${health.previousPassphrase?'<label class="field"><span>Previous mentor passphrase</span><input name="previousPassphrase" type="password" autocomplete="off"></label>':''}</details>`:'';
}

// Reuse the form nodes, including password-manager autofill and the current selection.
// Only host-claim availability can change during a background health refresh.
export function refreshMentorAccess(root,mode,health={},pending=null){
 if(pending)return false;
 const form=root.querySelector('form[data-form="mentor-auth"]');
 if(!form||form.dataset.mode!==mode)return false;
 const claim=form.querySelector('[data-mentor-claim]');
 if(claim){
  const availability=String(!!health.localClaim)+':'+String(!!health.previousPassphrase);
  if(claim.dataset.mentorClaim!==availability){claim.innerHTML=mentorClaim(health);claim.dataset.mentorClaim=availability;}
 }
 return true;
}

export function mentorAccess(mode='login',health={},pending=null){
  if(pending)return `<section class="auth-box card"><p class="eyebrow">APPROVE THIS DEVICE</p><h1>Check your mentor device</h1><p>On your signed-in device, open Mentor space → Account & settings. Approve the request with this matching code.</p><p class="device-match">${esc(pending.code)}</p><p>${esc(pending.device)}</p><button class="btn" data-action="mentor-device-check">I've approved it — continue</button><p class="error-text" id="mentor-error" role="alert"></p><button class="btn secondary" data-action="mentor-mode" data-mode="recover">I cannot use that device</button></section>`;
  const create=mode==='setup',recover=mode==='recover';
  return `<section class="auth-box card"><p class="eyebrow">MENTOR ACCOUNT</p><h1>${create?'Create your mentor space':recover?'Recover your account':'Sign in to your space'}</h1><p>${create?'Your learners, messages and rewards stay private to your account.':'Use your own mentor account. Learners use an invitation or return link.'}</p><div class="auth-tabs"><button class="btn ${!create&&!recover?'':'secondary'}" data-action="mentor-mode" data-mode="login">Sign in</button><button class="btn ${create?'':'secondary'}" data-action="mentor-mode" data-mode="setup">Create account</button></div><form data-form="mentor-auth" data-mode="${mode}">
  ${create?'<label class="field"><span>Your display name</span><input name="name" maxlength="50" required autocomplete="name"></label>':''}
  <label class="field"><span>Mentor username</span><input name="username" minlength="3" maxlength="32" required autocomplete="username" autocapitalize="none" spellcheck="false"></label>
  ${recover?'<label class="field"><span>Private recovery key</span><input name="recovery" type="password" required autocomplete="off"></label><p class="notice">Recovery signs out all previously approved devices. Your learner records are kept.</p>':''}
  <label class="field"><span>${create||recover?'Choose a passphrase (12+ characters)':'Your passphrase'}</span><input name="passphrase" type="password" minlength="12" maxlength="200" required autocomplete="${create||recover?'new-password':'current-password'}"></label>
  ${create||recover?'<label class="field"><span>Repeat the passphrase</span><input name="confirm" type="password" minlength="12" maxlength="200" required autocomplete="new-password"></label>':''}
  <label class="field"><span>Name this device</span><input name="device" placeholder="For example: My laptop" maxlength="60" required autocomplete="off"></label>
  ${create?`<div data-mentor-claim="${!!health.localClaim}:${!!health.previousPassphrase}">${mentorClaim(health)}</div>`:''}
  <p class="legend">Use a browser profile only you can access. Stepstone remembers this browser for up to a year. Clearing browser data removes that recognition.</p><p class="error-text" id="mentor-error" role="alert"></p><button class="btn" type="submit">${create?'Create my account':recover?'Recover on this device':'Sign in'}</button></form>
  ${!recover?'<button class="btn secondary small auth-recover" data-action="mentor-mode" data-mode="recover">Lost device or forgotten passphrase?</button>':''}</section>`;
}
export function mentorDeviceSettings(info={}){
 return `<section class="card"><h2>Your account & devices</h2><p><strong>${esc(info.account?.name||'')}</strong> · ${esc(info.account?.username||'')}</p><p class="legend">Only approved browsers can open your dashboard. Sharing Wi-Fi does not grant access. Signing out removes this browser's approval.</p><h3>Device requests</h3>${info.requests?.length?info.requests.map(r=>`<div class="device-row"><div><strong>${esc(r.label)}</strong><p>Match this code: <b>${esc(r.code)}</b></p><small>Expires ${new Date(r.expires*1000).toLocaleTimeString()}</small></div><div class="buttons"><button class="btn secondary" data-action="mentor-device-review" data-id="${r.id}" data-status="approved">Approve device</button><button class="btn secondary" data-action="mentor-device-review" data-id="${r.id}" data-status="denied">Decline</button></div></div>`).join(''):'<p class="small">No pending requests.</p>'}<button class="btn secondary small" data-action="mentor-refresh">Refresh device requests</button><h3>Approved devices</h3>${(info.devices||[]).map(d=>`<div class="device-row"><div><strong>${esc(d.label)}</strong><p>${d.current?'This browser':'Approved '+new Date(d.created*1000).toLocaleDateString()}</p></div>${!d.current?`<button class="btn secondary small" data-action="mentor-device-revoke" data-id="${d.id}">Remove access</button>`:''}</div>`).join('')}</section>`;
}

export function personalLearningTools(){
  return `<section class="card manager-personal" id="manager-personal" tabindex="-1"><div><p class="eyebrow">MY TEST SPACE</p><h2>Start again or revisit the guided tour</h2><p>These controls apply to your personal learning record. Your learners’ records remain unchanged.</p></div><div class="personal-tool-grid"><div><h3>Reset your personal learning</h3><p>Clear your own answers, lessons, profile and Steps. You will confirm before anything is erased.</p><button class="btn" data-action="reset-learning">Reset my learning</button></div><div><h3>Replay the guided tour</h3><p>Keep your learning and Steps. Restart the tour, or skip setup to explore.</p><div class="buttons"><button class="btn secondary" data-action="tutorial-restart">Restart my guided tour</button><button class="btn secondary" data-action="tutorial-skip">Skip my setup</button></div></div></div></section>`;
}

export function managerSettings(s={}){
  return `<section class="card manager-settings" id="manager-settings" tabindex="-1"><h2>App settings</h2>
    <p class="small muted">Manage the app here. Your own learning stays separate from learner records.</p>
    <label class="toggle-row"><div><strong>Keep Stepstone running in the background</strong><p>${s.desktop?'On: learners can connect after you close the browser. Off: the app stops about 3 minutes after the last open page stops checking in.':'This server is managed by its host. The desktop launcher enables this control on your laptop.'}</p></div><input type="checkbox" role="switch" data-host-background ${s.keepRunning?'checked':''} ${s.canManageHost?'':'disabled'} aria-describedby="background-help"></label>
    <p class="legend" id="background-help">${s.canManageHost?'Keep the laptop awake and connected. This does not prevent sleep or start the app with Windows. Reopen the desktop icon if the app has stopped.':'Only this installation’s owner can change host background settings, from the host computer.'}</p>
    <p class="small" data-host-result role="status"></p>
    <div class="manager-connection"><strong>${s.sharingReady?'Shared address configured':'Currently on this laptop'}</strong><p class="small">${s.sharingReady?esc(s.sharedAddress):'A localhost invite only works on this laptop. The separate Wi-Fi preview does not share these learner accounts.'}</p>${!s.sharingReady?'<details><summary>How do I invite their phones?</summary><ol><li>Host this Stepstone server at a shared HTTPS address, with its saved account database.</li><li>Configure that address on the host.</li><li>Create a private learner link here and send it to one person.</li></ol><p class="small">Background mode keeps this laptop app alive; it does not publish it to the internet.</p></details>':''}</div>
    ${recoverySettings(s.recovery)}
    <div class="buttons"><button class="btn secondary small" data-action="export-reports">Export report records</button><button class="btn secondary small" data-action="mentor-refresh">Check connection</button></div>
    <p class="source-note">Interface build ${INTERFACE_BUILD} · ${s.desktop?'Desktop host':'Server host'} · No messages or purchases are sent from these settings.</p>
  </section>`;
}

function recoverySettings(r={}){
  return `<div class="manager-connection"><h3>Recovery copies</h3><p>${r.latest?'Last copy created and checked: '+esc(new Date(r.latest*1000).toLocaleString()):'No recovery copy has been made yet.'}</p><p class="small">${r.automatic?'A copy is made about once a day while this host runs.':'Use the button to create a copy on this test server.'} The latest ${r.retained||14} copies stay privately on this host. A separate protected off-host copy is still needed if the whole host fails.</p>${r.error?`<p class="notice warning">${esc(r.error)}</p>`:''}<button class="btn secondary small" data-action="recovery-copy" ${r.busy?'disabled':''}>${r.busy?'Making a recovery copy…':'Make a recovery copy now'}</button>${r.rewardsOnHold?`<form data-form="recovery-reconciled"><h4>Check rewards after this restore</h4><p>New requests and approvals are paused. Compare rewards actually delivered since the snapshot with these restored records so nothing is issued twice. Learning can continue.</p><label class="check-label"><input type="checkbox" name="confirmed" required><span>I checked later deliveries and reconciled the stock and reward records.</span></label><label class="field"><span>What did you check or correct?</span><textarea name="note" minlength="10" maxlength="1000" required></textarea></label><button class="btn secondary" type="submit">Reopen reward requests</button><p class="error-text" data-recovery-error role="alert"></p></form>`:''}<details><summary>How recovery works</summary><p>Copies include account access records, learning and reward history. They are private host files, never public downloads. Keep both the database copy and its matching checksum file.</p><p>Restore is a host-owner task: verify a copy, restore it to a new folder, then start the app with that folder. The restore tool refuses existing folders and signs all browsers out. Unused invites and learner return links expire too. Use Help them sign in to issue fresh private links for existing learners.</p><p>Export report records is useful for reading reports, but it cannot restore accounts. The host guide includes the exact recovery steps.</p></details></div>`;
}

export function inviteCard(result,formatDate){
  const link=result.url;
  return `<div class="created-invite"><p class="small">${result.sharingReady?'One private start link for one learner:':'Local test link — this does not invite a phone yet.'}</p><label class="field"><span>Private learner link</span><input readonly value="${esc(link)}" id="invite-link"></label><div class="buttons"><button class="btn secondary" data-action="copy-invite" data-link="${esc(link)}">Copy learner link</button>${result.sharingReady&&navigator.share?`<button class="btn secondary" data-action="share-invite" data-link="${esc(link)}">Share link…</button>`:''}</div><details><summary>Use a code instead</summary><div class="invite-code">${esc(result.code)}</div></details><p class="legend">One use. Expires ${formatDate(result.expires)}. Keep it private. ${result.sharingReady?'They choose their nickname and companion when they open it.':'See Account & settings for the connection setup.'}</p></div>`;
}

export async function copyPrivateLink(link){
  if(!navigator.clipboard?.writeText)throw new Error('Select the private link and copy it using your device’s Copy command.');
  try{await navigator.clipboard.writeText(link);}
  catch{throw new Error('Copy was blocked. Select the private link and use your device’s Copy command.');}
}

// Presence contains no names, answers or credentials. It only prevents an opted-out
// desktop host from stopping while somebody still has the app open.
export function keepHostInformed(api,health){
  if(!health.desktop)return;
  const ping=()=>api('/api/presence',{}).catch(()=>{});
  ping();setInterval(ping,25000);
  window.addEventListener('pageshow',ping);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)ping();});
}
