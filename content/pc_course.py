"""Phone-beside-PC course. Original simulations; no host OS actions or secrets."""
from digital import lesson, q
from life_services import attach_guides, evidence

CHECKED = '2026-09-25'
SOURCES = {
 'settings': ('Microsoft — Windows settings and accessibility', 'https://support.microsoft.com/en-us/accessibility/windows/understand-and-explore-windows-settings'),
 'files': ('Microsoft — File Explorer', 'https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows'),
 'backup': ('Microsoft — Windows Backup and its limits', 'https://support.microsoft.com/en-us/windows/experience/backup-recovery/back-up-and-restore-with-windows-backup'),
 'remove': ('Microsoft — uninstall an app', 'https://support.microsoft.com/en-us/windows/uninstall-or-remove-apps-and-programs-in-windows-4b55f974-2cc6-2d2b-d092-5905080eaf98'),
 'docs': ('LibreOffice — official download', 'https://www.libreoffice.org/download/'),
 'code': ('Visual Studio Code — Windows setup', 'https://code.visualstudio.com/docs/setup/windows'),
 'safe': ('Get Cyber Safe — accounts and devices', 'https://www.getcybersafe.gc.ca/en'),
}

def screen(title, body, right, wrong, feedback, *, scene='desktop', input=None):
    return dict(title=title,body=body,scene=scene,input=input,actions=[dict(label=right,correct=True),dict(label=wrong,correct=False,feedback=feedback)])

def sim(ident, title, prompt, screens, why):
    return dict(id=ident,title=title,prompt=prompt,kind='pc',screens=screens,hint='Read the small goal above the practice screen. Nothing here changes your device. Try the control that does that job.',why=why)

def checks(rows):
    # Each set contains independently authored situations, not duplicate shuffles.
    return [q(*row) for row in rows]

START = dict(id='pc-start',title='Get comfortable with your computer',minutes=30,
 goal='Open your tools, move between them, and make the screen comfortable.',
 why='You do not have to remember every button. Learn a few ways to find your place and return to your work.',
 objectives=['Find your tools','Make it comfortable','Show your next step'],needs=['digital-1'],sources=['settings'],help='settings',
 nextSteps=['Use Windows 11 for the real-device steps. If the device has a different system, ask your mentor to adapt them first.',
  'With your mentor, connect to a known network. Keep the Wi-Fi password out of this app. Open two familiar apps and switch between them.',
  'Try a comfortable text size in Settings, then lock the screen and sign back in privately. Save work before restarting.'],
 deviceTask=dict(title='Show how you get around',steps=['Open two apps and switch back to the first.','Choose a comfortable text or pointer size.','Lock the screen and return privately.'],prompt='Which tool helped you find your place? Give a made-up example; do not enter a login or Wi-Fi password.'),
 lessons=[lesson('An app does a job. A file keeps your work.',
  'The keyboard and screen are parts you can touch. An app is a tool you open. A file is saved work. You can close a window without deleting its file.',
  'These are different layers. A notes app can open several note files. A browser can show several tabs. The taskbar helps you return to an open app; Start helps you find one. Scroll to see more of a page. Single-click selects many items; double-click opens many files. A right-click, or touch-and-hold, often opens an item menu. Moving or resizing a window changes your view, not the saved file.',
  'Keep a shopping note open while checking a calendar.',
  ['Open Start and choose Notes in this practice screen.','Open Calendar too. Use its taskbar button to switch, then return to Notes.','Make Notes smaller so you can see both tools. Its saved note stays the same.'],
  'Minimise hides a window. Close ends that window. Neither is the same as deleting a saved file.'),
  lesson('Set the computer up for you',
  'Make text and the pointer easy to see. Turn sound down if needed. Lock your screen when you step away. Save your work before a restart.',
  'Comfort settings help you spend attention on the task. There is no best text size for everyone. Lock protects an open session. Sleep saves power for a break; restart closes and reloads the system; shutdown turns it off. Save first because unsaved work may be lost when apps close.',
  'Ari cannot read a small note and needs a short break.',
  ['Open Settings, then Accessibility. Try larger text and check the preview.','Apply a size that fits. Keyboard, captions, pointer and volume settings can also help.','Save the note. Lock the screen for the break. Sign in privately when returning.'],
  'The simulation cannot change Windows settings. A larger preview here is only rehearsal.')],
 labs=[[
  sim('pc-open','Open a tool and come back','Use the taskbar to return to Notes.',[
   screen('Desktop','Goal: open Start.','Start','Delete files','You only need to find an app.'),
   screen('Start','Goal: open Notes.','Notes','Power off','Power off would end the session.',scene='menu'),
   screen('Notes · shopping.txt','Goal: keep Notes open and open Calendar.','Open Calendar','Delete shopping.txt','Deleting the file is not switching apps.',scene='window'),
   screen('Calendar','Goal: return to the open Notes window.','Notes on taskbar','Close everything','The taskbar lets you switch without closing.',scene='window'),
   screen('Notes · shopping.txt','Goal: make this window smaller.','Restore window size','Delete note','Window size changes the view, not the file.',scene='window'),
   dict(screen('Arrange your tools','Drag the Notes title bar or use the move buttons. Goal: make room beside Calendar.','Keep this arrangement','Close everything','Move the practice window instead of closing your tools.',scene='window'),move=True)], 'You opened, switched, resized and moved the practice window without throwing away work.'),
  evidence('pc-parts','Name the saved work','Which two are files, rather than hardware or an app?', ['shopping.txt','A keyboard','trip-photo.jpg','A notes app'],[0,2],'The named text document and photo are saved files.')],
 [sim('pc-comfort','Make the view easier','Try a comfortable setting and protect your break.',[
   screen('Desktop','Goal: open the system settings.','Settings','An advert promising faster eyesight','Use your device settings, not an advert.'),
   screen('Settings','Goal: find text and pointer settings.','Accessibility','Uninstall all apps','Removing apps cannot make text readable.',scene='settings'),
   screen('Text size preview','Goal: try larger text.','Increase text size','Erase the document','This changes how large text looks.',scene='text'),
   screen('Larger text preview','Goal: keep the readable size.','Apply size','Buy a new font','No purchase is needed for this practice setting.',scene='large-text'),
   screen('Ready for a break','The note is saved. Goal: protect the session.','Lock screen','Share the sign-in code','Keep sign-in information private.',scene='window')], 'You tried a readable size and locked the practice screen.'),
  evidence('pc-power','Choose a restart plan','An update asks to restart. Select the two useful preparations.', ['Save open work.','Plan a time when the restart will not interrupt a task.','Assume every app saved itself.'],[0,1],'Save and choose a suitable moment. A restart is not just hiding a window.')]],
 practice=checks([
 ('Which is hardware?','The keyboard.','A saved note.','A browser tab.','Hardware is the physical part.'),
 ('A letter is open in an editor. Where is the saved writing?','In the letter file.','Only in the mouse.','In the app icon itself.','An app works with files; it is not the contents of every file.'),
 ('You hid Calendar. How can you return?','Choose its taskbar button.','Delete all notes.','Buy Calendar again.','Minimised windows can be restored.'),
 ('The pointer is hard to see. What should you try?','Pointer options in Accessibility.','Remove the keyboard driver.','Disable sign-in.','Change the setting related to the difficulty.'),
 ('You leave your shared space for a minute. What protects the open session?','Lock the screen.','Post the password nearby.','Turn sound up.','Locking requires private sign-in to return.'),
 ('Before a restart, what comes first?','Save open work.','Assume all changes are saved.','Delete the app.','Closing apps can lose unsaved work.')]),
 check=checks([
 ('Jo takes a photo, then opens it in Photos. Which is the file?','The saved photo.','The Photos app.','The touchpad.','Photos is the tool; the image is the saved work.'),
 ('Two apps are open. How can Jo change which is in front?','Select the other app on the taskbar.','Uninstall one app.','Rename the keyboard.','Switching windows keeps both tools available.'),
 ('A window covers the whole screen. Jo wants to see another beside it. What helps?','Restore and resize the window.','Delete its saved document.','Remove the app.','The size of a window is a view setting.'),
 ('An app closed but its file was saved. What is a useful next step?','Open the file again in an appropriate app.','Assume the file was deleted.','Replace the laptop.','A saved file remains after its app closes.'),
 ('Which action opens an app you cannot see on the taskbar?','Find it in Start or search by its name.','Delete Downloads.','Disable updates.','Find the tool by its name and check the result.'),
 ('A browser has two tabs. What does closing one normally close?','That tab, not every file on the computer.','Every app on the device.','The physical screen.','Tabs, windows and saved files are different things.'),
 ('Lee finds text uncomfortable. Which result matters?','A size Lee can read without hiding needed controls.','The smallest setting possible.','The setting another person says looks impressive.','Comfort is personal; check the result in the real task.'),
 ('The practice screen says locked. Is the real laptop locked?','No. This is a simulation.','Yes, on every device.','Only if the quiz score is high.','Stepstone does not control the operating system.'),
 ('A computer needs a restart. A draft is unsaved. What should happen?','Save the draft before restarting.','Unplug immediately.','Pretend the draft is already saved.','Save work before apps and the system restart.'),
 ('Mo needs a short break but will keep the same session. Which protects access?','Lock the screen.','Tell everyone the sign-in code.','Leave the unlocked session open.','A lock protects access to the current session.'),
 ('Which statement about sleep fits?','It is a power-saving state for a break, not a backup.','It creates an independent backup of every file.','It deletes every installed app.','Save work and keep backups separately.'),
 ('The phone guide differs from the laptop screen. What should Mo do?','Check the operating system and ask for matching steps.','Click unknown controls until something happens.','Enter passwords into the practice answer.','Version differences need adapted instructions, not guesses.')]),
 reflection='Explain the difference between a tool, its open window and a saved file. Give one way you can return to your work.')

FILES = dict(id='pc-files',title='Save, find and recover your work',minutes=30,
 goal='Save a small note, reopen it, and recover a separate copy.',why='Finding your own work saves frustration. A checked backup gives you a way back when a file changes or disappears.',
 objectives=['Save with a name','Make a separate copy','Recover your work'],needs=['pc-start'],sources=['files','backup'],help='files',
 nextSteps=['Create a folder called Stepstone practice. Save a fictional shopping note there. Close and reopen it to check the location.',
  'With your mentor, make a backup on an approved separate drive or backup service. Check what is included. Cloud sync can copy deletions too.',
  'Practise recovery using a disposable copy. Open the restored file and read it. Do not delete your only real copy as a test.'],
 deviceTask=dict(title='Show a file coming back',steps=['Save a fictional note with a clear name and reopen it.','Keep a separate backup and identify where it is.','Restore a disposable practice copy and check its contents.'],prompt='Describe the folder and the recovery check, using made-up file names. Do not paste personal documents.'),
 lessons=[lesson('A useful name and a known place',
  'Save chooses a file name and a place. A folder groups files. Downloads is often where new downloads arrive. A shortcut points to something; it is not a second copy.',
  'Imagine a shelf, a labelled box and a page inside it. A location tells you where to look; the name tells you which work to open. Check both. Saving beside an old file may replace it, so pause when an app asks about replacement. A file extension describes its format, not whether it is safe.',
  'Save shopping.txt in Stepstone practice.', ['Write a short invented list.','Choose the practice folder and the name shopping.txt. Save.','Close the note. Open the folder, select the saved file and read it again.'],
  'Seeing a filename is not enough. Reopen it to check the contents you meant to save.'),
 lesson('A backup needs a way back',
  'A backup is a copy you can recover. Keep it apart from the original. Check the restored contents. A shortcut is not a backup, and syncing can copy mistakes too.',
  'One copy can fail. A separate copy protects against some failures, depending on where it lives and what it includes. A second folder on the same drive will not protect against that drive failing. Cloud services have their own space, version and recovery limits. Test a disposable file before depending on the plan.',
  'Recover an earlier shopping note after a practice change.', ['Copy the saved note to the simulated backup drive.','Change the practice original. Notice that the separate backup still holds the earlier text.','Restore from the backup and reopen the recovered file. Compare its contents with what you expected.'],
  'Windows Backup has account and coverage limits. Check the actual files and restore route; do not assume every folder or app is included.')],
 labs=[[
 sim('pc-save','Keep a useful note','Type a made-up item, save the note and find it again.',[
  screen('Notes · new note','Goal: write one made-up shopping item.','Save as','Close without saving','Write and save before closing.',scene='editor',input='Practice note'),
  screen('Save as · choose a folder','Goal: keep course work together.','Stepstone practice','A shortcut only','A shortcut points to a file; choose a folder.',scene='files'),
  screen('Stepstone practice · shopping.txt','Goal: save this note here.','Save shopping.txt','Replace an unrelated file','Use the chosen practice file, not unrelated work.',scene='files'),
  screen('Notes · saved','Goal: close and test the save.','Close note','Erase original','Closing is different from deleting.',scene='editor'),
  screen('Stepstone practice','Goal: reopen the saved file.','Open shopping.txt','Open a blank note','Open the file you saved.',scene='files')], 'The text in the reopened practice note matches your saved note.'),
 evidence('pc-location','Keep the useful details','Which two details help you reopen the right work?', ['Folder: Stepstone practice','File: shopping.txt','Mouse colour: blue'],[0,1],'Location and filename guide you back.')],
 [sim('pc-backup','Make a recovery copy','Use the fake backup drive; your real files are never touched.',[
  screen('Stepstone practice · shopping.txt','Goal: keep a separate copy.','Copy to Backup drive','Make a shortcut','A shortcut is a pointer, not saved contents.',scene='files'),
  screen('Backup drive · shopping.txt','Goal: check the copy.','Open backup copy','Assume it copied','Opening checks the contents, not just the label.',scene='backup'),
  screen('Practice original changed','The original now has a wrong item. Goal: recover the earlier version.','Restore backup to Recovered folder','Copy the changed file over the backup','Overwriting the backup would lose this earlier copy.',scene='backup'),
  screen('Recovered · shopping.txt','Goal: verify recovery.','Open and compare restored note','Delete all backups','Check the result before relying on it.',scene='files')], 'You restored and checked a disposable copy; no real backup has been created.')]],
 practice=checks([
 ('Where would you first look for a newly downloaded document?','Downloads, unless you chose another location.','Inside the keyboard.','Only in the Recycle Bin.','Check the browser download location.'),
 ('What does a shortcut keep?','A link to a location or item.','An independent copy of all file contents.','A new physical drive.','A shortcut can fail if its target disappears.'),
 ('How can you check a save?','Close and reopen the intended file.','Look only at its colour.','Delete the folder.','Check the actual saved contents.'),
 ('A backup on the same failing drive protects against that drive failing?','No; the backup can be lost with it.','Always.','Only when it is renamed.','Location matters for the failure you want to cover.'),
 ('Cloud sync removes a file on two devices. What lesson follows?','Sync alone may copy deletions; check recovery options.','Every backup is useless.','The second device is guaranteed safe.','Sync and independent recovery are different jobs.'),
 ('Which is a safe first recovery test?','Restore a disposable practice copy.','Delete the only family photo folder.','Erase the computer.','Test without risking valuable originals.')]),
 check=checks([
 ('Ari saved a list but cannot find it. Which details help most?','Its folder and filename.','The brightness setting.','The colour of the app icon.','A location and name narrow the search.'),
 ('A file named plan-final.txt contains old work. What did the name prove?','Only its label; the contents still need checking.','That all edits were saved.','That it is a backup drive.','Open the file and inspect the contents.'),
 ('Save asks to replace a different existing file. What is sensible?','Check the name and choose a new one if replacement is unintended.','Always accept.','Disable all warnings.','Replacement may overwrite work you need.'),
 ('Which name gives a useful clue?','bus-plan-september.txt','new-new-final-final.txt','untitled-97.txt','A descriptive name helps your future self.'),
 ('A shortcut remains after its original was deleted. What may happen?','It cannot open the missing original.','It recreates all contents automatically.','It becomes an independent backup.','The shortcut points elsewhere; it is not the data.'),
 ('You saved a document, closed its app and reopened the document. What did this check?','That the saved location contains readable work.','That every file is backed up.','That the laptop can never fail.','A save check has a useful but limited scope.'),
 ('A drive fails, including both folders on it. What would better cover that failure?','A tested copy on a separate device or suitable backup service.','A shortcut on that same drive.','Renaming one folder Backup.','A separate location reduces shared failure.'),
 ('Which recovery test shows more than a filename?','Open the restored file and compare its contents.','Count icons only.','Delete it without reading.','Check the result against what should have been recovered.'),
 ('A synced deletion reaches the laptop. What should you inspect?','The service’s version or deleted-file recovery options.','Only the wallpaper.','A promise that sync never removes files.','Recovery depends on the actual service and its limits.'),
 ('A backup service says only selected folders are included. What does that mean?','Other folders need checking or a separate plan.','Every file on every drive is protected.','No file is ever copied.','Coverage must be checked, not assumed.'),
 ('Your only important file is open. You want to practise deletion recovery. Use…','A disposable copy with a checked backup.','The sole important original.','A stranger’s files.','Practise safely with work you can afford to change.'),
 ('The lesson reports simulation complete. Is a real backup proven?','No; demonstrate a real recovery separately.','Yes on every linked device.','Yes if the learner used a phone.','The simulation teaches actions; it cannot inspect real storage.')]),
 reflection='Explain where a saved practice file lives, where its separate backup lives, and how you would check a restore.')

SAFE = dict(id='pc-safe',title='Protect your sign-in and updates',minutes=25,
 goal='Find a safe recovery route and distinguish real update settings from a scare message.',why='A calm plan keeps a small sign-in problem from turning into a lost account or a scam.',
 objectives=['Protect your access','Check the update route','Explain a safe plan'],needs=['pc-start','digital-2'],sources=['settings','safe'],help='safe',
 nextSteps=['Privately check which account you are using and how its official recovery route works. Use the appropriate supervised route when needed; never share a login here.',
  'Open Windows Settings yourself and find Windows Update. Read the status; save work before a requested restart.',
  'If support has ended, the device is managed, or instructions are unfamiliar, ask the mentor for an appropriate supported plan. Do not bypass an organization lock.'],
 deviceTask=dict(title='Show a safe route without showing secrets',steps=['Explain where official account recovery starts, without revealing any secret.','Open real update settings and explain the status.','Name what you would do with a scary browser pop-up.'],prompt='Describe the routes and one action you would pause. No passwords, codes, email addresses or screenshots of private settings.'),
 lessons=[lesson('Recovery is a plan, not a shared password',
  'A password lets you sign in. A recovery method helps when sign-in fails. Keep both private. Start recovery from the service you know, not an unexpected message.',
  'Someone offering help does not need to know every secret. A mentor can sit beside you while you follow official steps privately. A second sign-in factor adds another check; recovery codes can also unlock access and need protection. A plan names a trusted route and safe storage, without writing the secrets into schoolwork.',
  'Jo receives a message asking for a sign-in code.', ['Do not reply with the code. Stop using the message link.','Open the service through a known address or app and check the account there.','If locked out, use its official recovery route. Keep private details off the shared screen.'],
  'A familiar logo, friendly name or urgent tone does not prove who is asking.'),
 lesson('Updates come through a route you can check',
  'A browser advert saying you have viruses is not your system update screen. Open Settings yourself. Read the status. Save work and plan a restart if needed.',
  'A message can imitate a trusted brand. Opening the real settings independently avoids trusting its link or phone number. Updates change software and may need time or power. A failed update calls for its actual error and official help, not a random cleaner. A successful simulation does not prove the computer is supported or updated.',
  'A web page flashes a warning and asks for payment.', ['Leave the warning alone. Do not call its number or install its tool.','Open Settings from Start, then Windows Update.','Read the real status and choose a supported next step. Ask for help when it is unclear.'],
  'Never disable protection just to satisfy an installer, an advert or an unexplained AI instruction.')],
 labs=[[
 sim('pc-recovery','Find the safe sign-in route','A fake message asks for a code. Practise keeping control.',[
  screen('Inbox · urgent sign-in message','Goal: keep the private code private.','Leave this message','Reply with a code','A sign-in code can grant access. Do not share it.',scene='message'),
  screen('Known account app','Goal: check the account independently.','Open account security','Trust the message logo','The independently opened app is a better starting route.',scene='settings'),
  screen('Sign-in unavailable','Goal: find legitimate recovery.','Use official recovery help','Borrow an adult account','Recovery must follow the right account and provider rules.',scene='settings')], 'You chose an independent recovery route without exposing a secret.'),
 evidence('pc-secrets','Write only the plan','Which two belong in a Stepstone answer?', ['I would use the official recovery page.','My real recovery code is…','I would keep a private backup method.'],[0,2],'Describe the method; keep the secret elsewhere.')],
 [sim('pc-update','Check a scary message','Find the real update status instead of following an advert.',[
  screen('Browser warning','This page demands payment to remove a virus. Goal: avoid its trap.','Close the warning tab','Pay this page','Do not use a warning page as payment or support proof.',scene='warning'),
  screen('Desktop','Goal: open your own system settings.','Start → Settings','Call the advert’s number','Use a known route independently.'),
  screen('Settings','Goal: inspect updates.','Windows Update','Turn protection off','Protection does not need to be disabled for this check.',scene='settings'),
  screen('Windows Update · restart needed','Your practice note is unsaved. Goal: prepare safely.','Save work, then plan restart','Restart and hope','Save first; schedule around your task.',scene='update')], 'You read the simulated status through a known route.')]],
 practice=checks([
 ('Who should receive your sign-in code in a lesson?','No one; keep it private.','Any helpful-sounding account.','A public chat.','Codes can grant account access.'),
 ('A sign-in message looks official. What strengthens verification?','Open the known service independently.','Trust its colours.','Reply with a password to test it.','Check through a route you already trust.'),
 ('What belongs in a recovery plan?','Where official help starts and how you keep recovery private.','All recovery codes in Stepstone.','A borrowed login.','The plan can be explained without secrets.'),
 ('Where should a Windows update check begin?','Settings opened yourself.','A random browser advert.','A stranger’s payment page.','An independent system route is checkable.'),
 ('An update asks for a restart. First…','Save work and plan the interruption.','Delete personal files.','Pay a warning page.','Protect unsaved work.'),
 ('The device is still managed by its previous organization. What next?','Ask the legitimate owner to resolve it.','Bypass the management lock.','Share someone else’s code.','Ownership restrictions need legitimate resolution.')]),
 check=checks([
 ('A helper requests a recovery code to be friendly. What is the safer response?','Keep it private and use official recovery yourself.','Send all codes.','Post the code publicly.','A recovery code may unlock your account.'),
 ('You lost access. A search advert promises instant recovery for payment. What is a better start?','The provider’s known official recovery route.','The first paid advert.','A borrowed identity.','Use the actual account service.'),
 ('Which practice note is appropriate?','I checked where recovery starts, without recording the code.','Here is my password.','Here is someone else’s ID photo.','Describe the process, not private information.'),
 ('A second factor adds what?','Another sign-in check, not permission to share passwords.','A guarantee no scam can work.','A public recovery code.','Keep every factor private and verify requests.'),
 ('A minor needs an account. What must be checked?','The provider’s age and supervised-account rules.','How to enter a false birth date.','Whose adult login to borrow.','Use a permitted account route.'),
 ('An account message is unexpected. Which is evidence beyond its logo?','The account status reached through the known app.','Its urgent punctuation.','A copied brand colour.','Independent checking gives stronger evidence.'),
 ('A web warning tells you to disable security. What should you do?','Stop and verify through real settings or trusted help.','Disable it immediately.','Give the page remote access.','A warning page cannot establish authority.'),
 ('The real update page requests a restart while work is unsaved. Which plan fits?','Save work, then restart at a suitable time.','Unplug without saving.','Buy a registry cleaner.','Use a controlled restart.'),
 ('The update fails with an error. What helps someone assist?','The task, non-sensitive error text and steps tried.','Your password.','Every private document.','Useful context can exclude secrets.'),
 ('The system is no longer supported. What should be checked?','An appropriate supported-device or update plan with the mentor.','How to ignore warnings forever.','Whether a quiz pass renews support.','A course result does not change vendor support.'),
 ('A practice screen shows updated. What can you claim?','Only the simulation step is complete.','The real PC has all updates.','The phone updated the laptop remotely.','The practice screen is not a device inspection.'),
 ('A popup asks you to call an unfamiliar support number. What should you use instead?','A separately verified official contact route.','That number because it is large.','A reply containing private codes.','Find help without relying on the suspicious message.')]),
 reflection='Explain how you would check a worrying sign-in or update message without exposing secrets or trusting its links.')

SOFTWARE = dict(id='pc-software',title='Choose useful apps and remove clutter safely',minutes=30,
 goal='Choose a tool for a real job and make a careful Keep, Remove or Ask decision.',why='A clean computer needs useful tools, not a huge install list or a risky cleanup script.',
 objectives=['Choose a useful tool','Keep, remove or ask','Check your change'],needs=['pc-safe'],sources=['remove','docs','code'],help='remove',
 nextSteps=['Try an existing updated browser and document editor first. If a tool is missing, use the verified publisher or an appropriate official store listing.',
  'Read the publisher, requested permissions and optional extras. Cancel if something unexpected appears. Install with your mentor only when it serves your task.',
  'For a known unwanted Windows app, use Settings → Apps → Installed apps → the app menu → Uninstall. Remove one at a time and check the result. Ask first about drivers, security, accessibility or unknown components. Removing nothing is valid.'],
 deviceTask=dict(title='Explain one software decision',steps=['Name one task and a suitable existing or official tool.','Explain an unexpected permission you would pause.','Choose Keep, Remove or Ask for an app; check the result if anything changed.'],prompt='Explain a decision using an app category. No installation is required if the computer already has what you need.'),
 lessons=[lesson('Install for a job, not for a collection',
  'Name the job first. Try a tool already installed. If you need another, check the real publisher and download route. Read the installer. Cancel any unexpected extra.',
  'An app needs a reason to be on the computer. A document editor helps write and open files; a code editor can wait until a project needs it. Search adverts, familiar icons and filenames can imitate a real publisher. Check the source independently and understand requests for access before accepting them.',
  'Sam needs to edit a short document.', ['Try the installed editor and check it saves a useful format.','If none fits, inspect an official option, such as LibreOffice. A code editor is a different tool.','If setup adds an unrelated cleaner or asks for unexplained access, cancel and verify before continuing.'],
  'The course never requires a paid cleaner, package manager or AI agent just to write a document.'),
 lesson('Keep, remove, or ask first',
  'Keep tools you need. Remove a known unwanted app through normal settings. Ask before touching something unfamiliar. Drivers help hardware work; protection and access tools have important jobs.',
  'Bloat is not a precise technical category. A preinstalled trial may be optional while a plain-looking driver is essential. A reversible, one-at-a-time choice lets you check what changed. Blanket removal scripts hide many decisions in one click. Record the reason and do not remove an app merely because you dislike its name.',
  'Sam sees a game trial, a display driver and a screen reader.', ['Keep the screen reader if it supports the learner. Put the unfamiliar display driver in Ask first.','The known unused game trial may be removed through the normal app settings after checking saved content.','Remove only that app, then check that the computer and useful tools still work.'],
  'A clean device may need no removals. Never disable security, use registry cleaners or run unexplained debloat commands.')],
 labs=[[
 sim('pc-install','Choose the tool you need','Practise cancelling an unwanted extra. Nothing is downloaded.',[
  screen('Your task: write a letter','Goal: try what you already have.','Open existing document editor','Install ten random tools','A short task needs a suitable tool, not a collection.',scene='menu'),
  screen('No suitable editor in this practice case','Goal: check a publisher route.','Open verified LibreOffice download page','Use a look-alike advert','Check the publisher independently.',scene='browser'),
  screen('Practice installer · extra cleaner included','This unexpected add-on is not needed. Goal: keep control.','Cancel and verify','Accept everything','Pause when the request differs from the plan.',scene='warning')], 'You cancelled an unexpected extra. No real installer ran.'),
 evidence('pc-useful','Keep the starter kit short','Choose the two useful starting needs.', ['An updated browser and a document tool','A tested backup method','Five paid registry cleaners'],[0,1],'Use what helps the task and protects work.')],
 [sim('pc-clutter','Sort before removing','Make one careful decision at a time.',[
  screen('Installed apps · screen reader in use','Goal: preserve needed access.','Keep screen reader','Remove because you do not use it','It supports this learner, even if someone else does not need it.',scene='apps'),
  screen('Installed apps · unfamiliar display driver','Goal: avoid breaking hardware.','Ask first about driver','Remove every unfamiliar name','Drivers may be needed for the screen to work.',scene='apps'),
  screen('Installed apps · known unused game trial','The owner confirmed no saved work is needed. Goal: remove just this trial.','Uninstall this trial','Run a bulk cleanup script','Choose only the known unwanted app.',scene='apps'),
  screen('Trial removed','Goal: check the result.','Open the useful tools and check them','Remove security next','A check catches problems before more changes.',scene='desktop')], 'You kept access, asked about a driver and removed one known trial in the simulation.')]],
 practice=checks([
 ('You need to write a letter. Start by…','Trying a suitable installed editor.','Installing every suggested app.','Disabling security.','Use a tool that serves the task.'),
 ('What is stronger evidence of a download source?','The independently verified publisher route.','A familiar logo alone.','The biggest download button.','Imitation pages can copy branding.'),
 ('An installer adds an unexplained cleaner. What fits?','Cancel and inspect before proceeding.','Accept all extras.','Give it every permission.','You control the scope of the change.'),
 ('An unfamiliar item says audio driver. Choose…','Ask first.','Remove all drivers.','Buy a cleaner.','Drivers support hardware.'),
 ('A needed screen reader should be…','Kept.','Removed to look tidy.','Replaced with no access tool.','Accessibility tools serve a practical need.'),
 ('The computer is already tidy and useful. What can be correct?','Remove nothing.','Delete something to earn Steps.','Disable updates.','The goal is a usable computer, not a removal count.')]),
 check=checks([
 ('Ari wants to calculate a small budget. Which choice starts with the job?','Try a suitable existing spreadsheet tool.','Install an unrelated game launcher.','Remove all apps first.','Choose a tool for the task.'),
 ('A download page imitates a known icon. What still needs checking?','The actual publisher and source address.','Only the icon colour.','Whether the button animates.','Branding is easy to copy.'),
 ('A beginner letter task needs a code package manager?','No; use a document tool that fits.','Always.','Only if it has an impressive name.','Avoid unnecessary complexity.'),
 ('An app asks for access unrelated to its job. What is sensible?','Pause, inspect the reason and cancel if unclear.','Approve because access is always harmless.','Share passwords to test it.','Permissions should match the intended job.'),
 ('A trusted editor is already working. What is a reasonable plan?','Keep using it if it fits the task and remains supported.','Install duplicates for every lesson.','Delete saved documents first.','Reusing a working tool avoids needless setup.'),
 ('An install unexpectedly adds a browser extension. What next?','Stop and verify that extra before agreeing.','Accept without reading.','Assume every extra is required.','Unexpected scope deserves a pause.'),
 ('Jo finds an unfamiliar firmware utility. Which category fits first?','Ask.','Remove automatically.','Ignore its purpose and delete it.','Firmware and hardware support need careful identification.'),
 ('A known unused trial has no needed saved content. How can it be removed?','Use the supported app uninstall route and check afterwards.','Delete random system folders.','Run an unexplained bulk script.','Use the normal uninstall process.'),
 ('Why change one app at a time?','You can relate a problem to the change and check its effect.','It guarantees all problems are impossible.','It removes the need to read.','Small changes are easier to inspect and recover from.'),
 ('A learner needs captions and a screen reader. Cleanup should…','Preserve their useful access tools.','Remove them as unnecessary.','Require the smallest text.','Needed accessibility features are part of a usable setup.'),
 ('Someone recommends disabling protection to speed up a laptop. What should you do?','Keep protection and ask about safe performance options.','Disable everything immediately.','Post recovery codes online.','Do not trade away protection on an unexplained claim.'),
 ('No app needs removal. Can this lesson still be completed?','Yes; explain why keeping the setup fits.','No; delete any app.','Only after buying a cleaner.','A justified no-change decision can be correct.')]),
 reflection='Choose a made-up example for Keep, Remove and Ask. Explain why each choice fits and how you would check a change.')

RECOVER = dict(id='pc-recover',title='Fix a small mistake and ask useful help',minutes=25,
 goal='Undo a practice mistake, recover a file, and explain a problem clearly.',why='A mistake does not mean you broke everything. Small checks and a useful help message give you a way forward.',
 objectives=['Undo and recover','Describe what happened','Show your setup'],needs=['pc-files','pc-safe','pc-software'],sources=['files','settings','safe'],help='settings',
 nextSteps=['In a disposable practice note, change a word and use Undo. Check that the expected word returns.',
  'Recover a disposable file using the route you practised. If that route does not apply, pause and ask instead of resetting the computer.',
  'Show your mentor your PC tasks. Describe the goal, what happened and what you tried. Do not include passwords, identity numbers or private family information.'],
 deviceTask=dict(title='Demonstrate a small recovery',steps=['Undo a change in a disposable practice note.','Explain a safe next step if the file cannot be recovered.','Give a useful help message without private information.'],prompt='Describe a practice mistake, the correction and how you checked it. A mentor will separately confirm the demonstration.'),
 lessons=[lesson('Stop. Undo. Check.',
  'If a small edit goes wrong, stop adding changes. Try Undo in that app. Read the result. If a file is missing, check its location and the recovery route you prepared.',
  'Each extra change can make the original problem harder to trace. Undo reverses a supported recent action in an app; it is not a universal recovery button. Deleted files, overwritten versions and failed drives need different routes. A factory reset is a large change with possible data loss, not the first response to a missing note.',
  'A practice note says Tuesday but should say Thursday.', ['Notice the wrong word before changing anything else.','Use Undo to restore the previous wording in this practice app.','Read the corrected line. If it is still wrong, use the known backup or ask for help with the specific problem.'],
  'Undo history can be limited or disappear after closing an app. Keep a separate backup for important work.'),
 lesson('Make your help message useful',
  'Say what you were trying to do, what happened and what you tried. Include only needed, safe details. Tell the helper if their instructions do not match your screen.',
  'A useful report separates observation from a guess. “The file is not in the folder I checked” is more precise than “the computer deleted everything.” A helper can then test a small next step. Private screenshots may show account names or messages; a fictional example or carefully limited description is often enough.',
  'Mo cannot find a saved practice note.', ['Goal: reopen shopping.txt from Stepstone practice.','Observed: the folder is empty. Tried: checking Downloads and the backup folder.','Ask: can you help me check the save location? Do not send passwords or unrelated documents.'],
  'A request for passwords, money or unexplained remote access is a reason to pause and verify the helper.')],
 labs=[[
 sim('pc-undo','Bring the right word back','Recover the practice note without a drastic reset.',[
   dict(screen('Notes · Meet on Tuesday','The previous line said Thursday. Open the note’s edit menu, then undo the last edit. Right-click the note, press Shift+F10 on its menu button, or tap Open edit menu.','Undo last edit','Factory reset computer','A single edit does not justify erasing a computer.',scene='editor'),contextMenu=True),
  screen('Notes · Meet on Thursday','Goal: check the correction.','Read and save the corrected line','Keep clicking Undo blindly','Check the result before making another change.',scene='editor'),
  screen('Practice file moved from its folder','Goal: look for this file.','Check known folders and recovery copy','Erase the drive','Find the file or a recoverable copy first.',scene='files')], 'You corrected a small edit and chose a proportionate recovery route.'),
 evidence('pc-observe','Separate fact from a guess','Choose the two observations a helper can work with.', ['The practice folder is empty.','I checked Downloads.','The computer hates me.'],[0,1],'State what you saw and tried, not an invented cause.')],
 [sim('pc-help','Build a useful help message','Choose the details a helper needs.',[
  screen('Help draft · goal missing','Goal: explain the task.','I am trying to reopen shopping.txt.','Everything is terrible.','Name the task you want help with.',scene='message'),
  screen('Help draft · observation missing','Goal: say what happened.','The practice folder looks empty.','You must fix everything now.','A concrete observation is easier to check.',scene='message'),
  screen('Help draft · next step','Goal: include attempts and a useful question.','I checked Downloads. Can we check the save location?','Here is my password.','Ask a useful question without giving away access.',scene='message')], 'The simulated message has a goal, an observation and a safe next question.')]],
 practice=checks([
 ('A recent text edit was wrong. A useful first try is…','Undo, then read the result.','Erase the drive.','Install a random cleaner.','Use a small correction for a small mistake.'),
 ('Undo is best described as…','An app feature for supported recent actions.','A guaranteed backup of every file.','A replacement for all recovery plans.','Its coverage and history have limits.'),
 ('A practice file is missing. Start with…','Its likely location and known recovery copies.','A factory reset.','Random system-file deletion.','Choose a relevant, low-risk check.'),
 ('A useful help message includes…','The goal, what happened and what you tried.','Only insults.','Your password and private codes.','Useful context does not require secrets.'),
 ('Which is an observation?','The folder I checked is empty.','The computer destroyed every file.','Every helper is lying.','An observation sticks to what was actually seen.'),
 ('A helper’s steps differ from your screen. What can you say?','My screen shows a different heading; can we check the version?','I will click randomly.','Here are all my credentials.','Clarifying the mismatch improves the next step.')]),
 check=checks([
 ('Lee accidentally replaces a word in an open practice note. Start with…','Undo and inspect the result.','Reset the whole computer.','Delete every folder.','A small edit calls for a small reversible correction.'),
 ('Undo brings back the expected word. What completes the check?','Read the corrected line and save when it is right.','Assume every other file changed too.','Continue undoing without looking.','Observe the result before taking another action.'),
 ('Undo is unavailable after closing an app. What should you consider?','The prepared version or backup recovery route.','A guarantee that Undo always works.','A random password request.','Recovery may require a saved copy or version.'),
 ('A document is absent from one folder. What can you conclude?','It was not found in that folder yet.','The drive was definitely erased.','The app deleted every document.','Do not turn one observation into an unsupported cause.'),
 ('A file problem appears after several changes. What helps next?','Stop and describe the changes before trying more.','Make ten more changes without notes.','Erase the only backup.','A clear sequence makes diagnosis easier.'),
 ('Which first recovery experiment is appropriate?','A disposable practice file with a checked backup.','Only-copy personal records.','Someone else’s private files.','Practise without risking valuable originals.'),
 ('What should a useful help request name first?','The task the learner is trying to complete.','The learner’s recovery codes.','An invented diagnosis of the computer.','A goal gives the helper a direction.'),
 ('Which message is most useful?','I saved a practice note, but cannot find it in Documents. I checked Downloads too.','Broken.','Fix everything, here is my password.','This names the goal, observation and attempted check.'),
 ('A screenshot would expose someone’s private messages. What is better?','Use a limited description or safe fictional example.','Send it anyway.','Post it publicly.','Share only what is necessary and appropriate.'),
 ('A stranger says remote access is required before explaining the problem. What fits?','Pause and verify the helper and need for access.','Grant access immediately.','Disable all protection.','Access requests need inspection, not blind trust.'),
 ('Passing this PC check proves which result?','The learner answered this check; real setup still needs a demonstration.','The operating system was inspected remotely.','Every backup on the device works.','Quiz evidence and device verification have different scopes.'),
 ('Your mentor asks you to demonstrate recovery with an accessible input method. What matters?','Showing the steps and explaining the result.','Meeting a universal typing-speed target.','Never using help or accessibility tools.','Useful understanding does not require a speed contest.')]),
 reflection='Write a short fictional help message with your goal, what happened, what you tried and a safe next question.')

MODULES = [START, FILES, SAFE, SOFTWARE, RECOVER]

def attach(units, bank):
    for m in MODULES:
        m['practiceNotice']='Practice computer only. These controls do not change your phone or PC. Real-device work is separate.'
        m['checkSkills']=['interpret','apply','reason']
        for name in ('practice','check'):
            for i,item in enumerate(m[name]): item['skill']=m['checkSkills'][i%3]
    attach_guides(units,bank,MODULES,SOURCES,CHECKED)
    for m in MODULES:
        u=next(u for u in units if u['id']==m['id'])
        u['course']='pc';u['deviceTask']=m['deviceTask'];u['guide']['region']='Windows 11 · phone beside PC'
        u['mission']['label']='PC basics';u['mission']['artLabel']='TRY / CHECK / RECOVER'
        u['mission']['brief']=[m['goal'],m['practiceNotice'],'Use a phone now. Show the real-device tasks to your mentor when you have a computer.']
