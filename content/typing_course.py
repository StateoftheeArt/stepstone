"""Practical keyboard and editing lessons, using the shared mission engine."""
from digital import lesson,q
from life_services import attach_guides

CHECKED='2026-09-25'
SOURCES={'keys':('Microsoft — keyboard shortcuts','https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec')}
def drill(ident,title,prompt,target,initial='',exact=False):
    return dict(id=ident,kind='typing',title=title,prompt=prompt,target=target,initial=initial,edit=bool(initial),exact=exact,
        hint=('Match every detail in this short task. Compare spaces, letters and punctuation. Use the cue and any comfortable input method.' if exact else 'Compare one small part at a time. Check letters, spaces, capitals and punctuation. Use any comfortable input method. You can lower the practice target for a warm-up.'),
        why='You checked the text after editing. A useful message matters more than speed. This practice does not prove unaided typing.')
def questions(rows):return [q(*r) for r in rows]
def draft(ident,title,prompt,checks,why,example):
    return dict(id=ident,kind='draft',title=title,prompt=prompt,checks=checks,why=why,example=example,hint='Give one useful detail and one clear question. Read your message and check the meaning.')

KEYS=dict(id='typing-keys',title='Find your keys and make space',minutes=15,
 goal='Type a short note, fix a slip, and find a comfortable way to enter text.',
 why='A few useful keys let you write without starting over every time you make a mistake.',needs=['pc-start'],sources=['keys'],help='keys',
 objectives=['Try the useful keys','Find a comfortable rhythm','Explain a correction'],
 nextSteps=['Use a practice note with made-up details. Try Space, Enter and Backspace.','On many physical keyboards F and J have small bumps. Use them if helpful; check your own layout.','Choose a comfortable input method and take a break. There is no speed requirement.'],
 lessons=[lesson('Letters, gaps and new lines',
  'Letters make words. Space puts a gap between words. Enter starts a new line here. Backspace removes the character to the left of the cursor. Shift helps make a capital.',
  'The cursor is the small mark showing where your next character goes. A gap is a character too. If you type two spaces, the words may look farther apart. Move the cursor beside a slip and erase just that character. In a chat, Enter may send a message instead: check the button labels before using it.',
  'Make a two-line shopping note.', ['Type Milk. Hold Shift for M if using a physical keyboard.','Press Enter once. Type bread on the next line.','If you type breadd, press Backspace once. Read both lines.'],
  'Backspace erases left of the cursor. Delete usually erases right. Check which part will change.'),
  lesson('Find a comfortable starting place',
  'On many keyboards, F and J have small bumps. They help your hands find a starting place. Looking down is fine. Use a method that works for you.',
  'A familiar starting place can make keys easier to find. You can try resting your left fingers near A S D F and right fingers near J K L ;, then reach for a key and come back. This is a suggestion, not a required body position. One-hand input, larger keys, speech or another layout can also produce useful writing. Short relaxed practice is more useful than forcing a painful session.',
  'Try a few keys, then a useful phrase.', ['Choose Physical keyboard, Phone or tablet, or supported input.','Try f j f j slowly. Then type a few short words.','Compare the finished text. Correct one slip, then pause if you want.'],
  'Do not compare phone speed with a physical keyboard. No speed score or reward depends on it.')],
 labs=[[drill('keys-lines','Make a two-line note','Use Enter to put bread on its own line.','Milk\nbread'),drill('keys-backspace','Remove one extra letter','The practice note has one extra d. Put the cursor after it and erase it.','Milk bread','Milk breadd',True)],
       [drill('keys-landmarks','Try the two landmarks','Use a comfortable method. If using a physical keyboard, try finding F and J.','f j f j'),drill('keys-phrase','Build a small phrase','Type the words with one space between them.','ask for help')]],
 practice=questions([
 ('You type redbag but need two words. What is missing?','A space between red and bag.','A new app.','Three extra letters.','Space separates words.'),
 ('The cursor is just after the extra x in boxx. Which key removes that last x?','Backspace.','Space.','Shift by itself.','Backspace removes the character immediately left of the cursor.'),
 ('What makes a new line in this practice box?','Enter.','Holding Space for a long time.','Closing the browser.','Here Enter starts a line. Other apps may send on Enter.'),
 ('What can F and J bumps help with on many physical keyboards?','Finding a starting place by touch.','Saving every file automatically.','Proving typing speed.','They are landmarks, not a test or a requirement.'),
 ('Your hands are uncomfortable during practice. What fits?','Pause and adjust your setup or input method.','Force yourself to finish faster.','Turn off every access tool.','A comfortable method is part of useful practice.'),
 ('You use speech to write and then correct a word. How should it be described?','Supported input with editing.','Unaided physical-keyboard speed.','A failed attempt automatically.','Name the method honestly; useful editing still counts.')]),
 check=questions([
 ('A note says bluehat. You want blue hat. What change helps?','Insert one space between the words.','Delete both words and uninstall the editor.','Add an exclamation mark inside blue.','A word gap is made with Space.'),
 ('The cursor is after bookk. You need book. What does one Backspace do?','Removes the last k.','Removes the first b.','Adds a capital K.','Backspace works just left of the cursor.'),
 ('You want two items on separate lines in this exercise. What should you use?','Enter between the items.','A long row of dots.','A second account.','A line break makes separate lines.'),
 ('You need a capital T on a common physical keyboard. Which method fits?','Hold Shift while pressing T.','Press Space twice.','Delete the previous paragraph.','Shift changes the letter case while held.'),
 ('A chat says Enter sends. What is the useful check before pressing it?','Whether you intend to send or need the app’s new-line shortcut.','Whether your Steps balance is high enough.','Whether every app uses identical controls.','Keys can have different jobs in different apps.'),
 ('A cursor is between a and t in cat. What does Backspace normally remove?','The a.','The final t to its right.','The whole app.','The character immediately left of the cursor is removed.'),
 ('A keyboard has small bumps on F and J. What are they useful for?','Finding a familiar starting place without looking.','Showing that all learners must type identically.','Turning speech input off.','Landmarks can help orientation.'),
 ('A learner types with one hand. Which goal is useful?','Readable writing with a comfortable method.','Copying another person’s exact hand position.','Passing a universal speed test first.','Functional writing can use different methods.'),
 ('A phone predicts a whole word. What can the practice report claim?','The final text matched, using that input method.','Every letter was typed without support.','The same speed as a physical keyboard.','Prediction changes how text was entered.'),
 ('You keep missing a nearby key. What is a useful next step?','Slow down, look at the key and try a short phrase.','Keep speeding up without checking.','Assume one slip means you cannot learn.','Focused, comfortable repetition helps you notice the movement.'),
 ('Someone stops mid-exercise and returns later. What should happen?','Resume saved text without a speed penalty.','Lose their laptop reward.','Erase every earlier check.','Breaks and saved progress support practice.'),
 ('A practice percentage is high after several corrections. What does that show?','The final text is close to the target after editing.','There were no mistakes while entering it.','A physical keyboard was definitely used.','Final accuracy is different from first-try keystroke accuracy.')]),
 reflection='Name one useful key. Explain what changed when you corrected a slip, and which input method helped you.')

WORDS=dict(id='typing-words',title='Type words people can use',minutes=15,
 goal='Make a clear time, price and fictional contact line.',why='Small details can change a message. A space, digit or full stop can matter more than speed.',needs=['typing-keys'],sources=['keys'],help='keys',
 objectives=['Build accurate words','Check important details','Explain what matters'],
 nextSteps=['Type a short made-up message. Compare each word and space.','Check times, prices and contact details character by character.','Keep useful examples in a harmless practice note and revisit them later.'],
 lessons=[lesson('Work in small chunks',
  'Read a few words. Type them. Compare them. Fix one slip at a time. Keep spaces between words. You can switch the next-letter cue on or off.',
  'A long sentence can feel crowded. Breaking it into small chunks leaves fewer details to hold in mind. Read “Please save” before “my note.” After typing, read the result rather than assuming the keys produced what you meant. The percentage compares your final text with the example using the fewest character edits needed. It does not count every mistake you made and fixed.',
  'Type Please save my note.', ['Read Please save, then type it.','Add one space and my note. Include the full stop.','Compare the finished line. Find any missing, extra or changed characters.'],
  'Correcting text is part of the job. A lower starting target is fine for practice; important details still need a careful check.'),
  lesson('Capitals, numbers and punctuation',
  'A meeting time, price or email address needs a careful check. Read the finished details. An extra digit or missing symbol can change the job.',
  'Shift often gives a capital or the top symbol on a key. Phone keyboards may have a numbers or symbols page. Layouts differ, so look at your keys. In an email address, @ separates the name from the domain. The reserved example.com address here is fictional practice. Do not type your password or somebody’s private contact details.',
  'Read a fictional meeting message.', ['Type Meet at 4:30. Check both digits and the colon.','Type Cost: 8.50 CAD. Check the decimal point and currency.','Copy the fictional address carefully. Look for @ and the dot.'],
  'A near-match percentage cannot tell whether a changed time or email would be usable. Check the meaning and exact details.')],
 labs=[[drill('words-note','Build a useful sentence','Try a few words at a time.','Please save my note.'),drill('words-rows','Reach for new letters','Check each short word.','check the next step')],
       [drill('words-time','Make the time clear','Copy this fictional message exactly.','Meet at 4:30. Cost: 8.50 CAD.',exact=True),drill('words-contact','Check a fictional address','This practice address must match exactly.','ari.study@example.com',exact=True)]],
 practice=questions([
 ('Why type a few words at a time?','It leaves fewer details to remember at once.','It means spaces no longer matter.','It automatically saves every file.','Small chunks make comparison manageable.'),
 ('Your text has two spaces where the example has one. What should you check?','The extra gap.','The cost of a new keyboard.','The learner’s age.','Spaces are part of the text.'),
 ('The cue points to position 5. What does that mean?','Compare that part with the example.','You have failed five courses.','Type five random characters.','The cue points to a character that needs attention.'),
 ('A message should say 4:30, but says 4:03. What matters?','The digits change the meeting time.','It has the same number of characters, so it is fine.','A high average makes any time correct.','Same length does not mean same meaning.'),
 ('What separates the name from the domain in a typical email address?','The @ symbol.','Any blank space.','A gift-card code.','Check @, the name and the domain.'),
 ('A phone hides punctuation. What can you try?','Its numbers or symbols keyboard.','Posting a real password to ask for help.','Skipping important symbols.','Layouts vary; inspect the available keyboard controls.')]),
 check=questions([
 ('A long line feels hard to follow. What is a useful method?','Read and type a short chunk, then compare it.','Guess the whole sentence without checking.','Remove every space.','Small chunks reduce the amount to remember at once.'),
 ('The example says next step. Your text says nextstep. What differs?','One missing space.','The font alone.','The number of accounts.','A gap separates the two words.'),
 ('A learner turns off the next-letter cue. What stays available?','The example and their own text to compare.','A hidden timer that removes points.','Automatic proof of expertise.','The cue is optional support.'),
 ('Your final sentence matches after three fixes. What should the app report?','The final-text match after corrections.','Zero original mistakes for certain.','A universal typing speed.','The measure describes the finished text.'),
 ('A long message is accurate but hard to read. What can improve it?','Useful punctuation and separate lines.','More random capitals.','Removing all word gaps.','Organisation helps the reader follow meaning.'),
 ('A task is unfinished when you need a break. Which plan fits?','Pause and come back to the saved text.','Type nonsense to finish fast.','Give another person your sign-in code.','A pause does not remove learning progress.'),
 ('The intended time is 6:15. The message says 6:51. What should you do?','Correct the digits before using the message.','Ignore it because most characters match.','Change the font only.','The time has a different meaning.'),
 ('The price is 12.50 CAD. The text says 1250 CAD. Which detail is missing?','The decimal point.','The word CAD.','An app subscription.','The decimal changes the amount.'),
 ('Which fictional contact line follows the taught email pattern?','sam.learn@example.com','sam learn example com','sam@ with no domain','A typical address has a name, @ and a domain.'),
 ('A keyboard’s symbols differ from the example. What is useful?','Check the actual layout or open its symbols page.','Assume the device is broken.','Install an unknown keyboard tool immediately.','Input layouts can differ.'),
 ('Why use fictional contact details for practice?','To practise the structure without exposing private information.','Because real addresses never use @.','Because fictional data removes the need to check spelling.','Useful practice does not need private records.'),
 ('A contact address has one wrong letter but a high match score. Is it ready to use?','No. Check and correct the address exactly.','Yes. Every near-match reaches the same person.','Only the colour of the text matters.','A small address error can change the destination.')]),
 reflection='Explain why a high match percentage is not enough for a time, price or contact address. Describe one detail you checked.')

EDIT=dict(id='typing-edit',title='Fix and reuse your writing',minutes=20,
 goal='Edit a message without throwing away the whole thing.',why='Selecting, copying and undoing let you improve useful work with less effort.',needs=['typing-words'],sources=['keys'],help='keys',
 objectives=['Select and repair','Write something useful','Explain your edit'],
 nextSteps=['In a disposable note, select a word, replace it and check what changed.','Copy and paste a harmless line, then use Undo if the change is wrong.','Write a short request with a clear next step. Read it before sending anywhere.'],
 lessons=[lesson('Change the part you mean',
  'Select the text you want to change. Typing replaces the selected part. Copy keeps the original. Paste inserts a copy. Undo can reverse a recent edit.',
  'The cursor position and selection decide what changes. First look for the highlight. Ctrl+A selects all on Windows; Ctrl+C copies and Ctrl+V pastes. Ctrl+Z usually undoes. Mac commonly uses Command for these shortcuts. Phone selection handles and menus do similar jobs. This exercise also offers simple editing buttons. Its clipboard stays inside the exercise. Real device clipboards may store or sync copied information, so keep secrets out.',
  'Fix a meeting day without deleting the whole message.', ['Select Tuesday and replace it with Thursday.','Read the whole sentence: the day changed but the useful time stayed.','If the wrong part changed, use Undo and check the restored text.'],
  'Undo is useful, but not an independent backup. Some apps or later sessions cannot undo an earlier change.'),
  lesson('Write for the person reading',
  'Say what you need. Give the useful detail. Ask for one next step. Read it again. Change anything unclear. A clear message can be short.',
  'There is more than one good sentence. Unlike the fixed typing examples, your own message is not graded by exact wording. You check whether it includes the needed meaning; your mentor reviews that meaning. Accessibility tools and AI examples can support writing. You still need to understand and check what you send.',
  'Ask about a fictional practice session.', ['Write: I can come on Thursday after 4.','Ask: Which room should I use?','Read both parts. Check day, time and the question. Change a word if it helps.'],
  'Do not put private family details, account codes or somebody else’s contact details into a practice message.')],
 labs=[[drill('edit-day','Repair one detail','Change Tuesday to Thursday and keep the time. Try selection and Undo.','Meet Thursday at 4.','Meet Tuesday at 4.',True),drill('edit-line','Copy without losing the original','Use Select all, Copy selection, move to the end, Enter and Paste in this exercise. Make two matching lines.','Bring a notebook.\nBring a notebook.','Bring a notebook.',True)],
       [drill('edit-label','Make an app button clearer','Replace Go with Save my list. This is a practice app label.','Save my list','Go',True),
        draft('edit-message','Write your own useful message','Ask about a fictional session. Give a day or time and ask one useful question. This is saved, never sent outside Stepstone.',['I gave the useful day or time.','I asked one clear question.','I read and corrected my message.'],'A useful message gives enough context and one next step. A mentor reviews its meaning.',example='I can come Thursday after 4. Which room should I use?')]],
 practice=questions([
 ('What happens when you type over selected text?','The selected part is replaced.','Every saved file is deleted.','Nothing can change.','Check the highlight before replacing text.'),
 ('What does Copy normally do to the original text?','Keeps it and puts a copy on the clipboard.','Deletes it permanently.','Sends it to your mentor automatically.','Copy and Cut are different actions.'),
 ('You replaced the wrong word. What can help right away?','Undo, then inspect the restored text.','Keep making random edits.','Factory reset the computer.','Undo can reverse a recent edit in many apps.'),
 ('Which message gives a useful next step?','I can come Friday at 5. Which room should I use?','Hey.','You already know everything.','Context and a specific question help the reader answer.'),
 ('You use speech to draft a question. What should happen before sharing it?','Read and correct the result.','Assume speech never mishears.','Send private codes with it.','Check meaning regardless of input method.'),
 ('Is a saved practice message automatically sent to the fictional person?','No. It stays in Stepstone for learning.','Yes, every name is contacted.','Only if it contains a capital.','Practice writing is not an external message service.')]),
 check=questions([
 ('Only the meeting day is wrong in a sentence. What is efficient?','Select that day and replace it, then reread.','Erase every document on the computer.','Change the keyboard language at random.','Edit the part that needs changing.'),
 ('You press Ctrl+C on selected text in Windows. What normally happens?','A copy goes to the clipboard; the original stays.','It is sent to every contact.','The app is uninstalled.','Copy reuses text without removing the original.'),
 ('You want the copied text after the last sentence. What matters before Paste?','Place the cursor where the copy should go.','Turn off updates.','Delete the original source.','The cursor marks the insertion point.'),
 ('Selected text is highlighted. You type one letter. What is likely?','The selection is replaced by that letter.','The letter goes to an unrelated app.','The selection is always protected.','Check the highlight to avoid replacing more than intended.'),
 ('Undo brought back the earlier phrase. What comes next?','Read it and confirm it is the version you wanted.','Keep pressing Undo without checking.','Assume every file is backed up now.','Recovery needs a check of the result.'),
 ('A real clipboard tool may keep copied text. Which practice habit helps?','Use harmless fictional text instead of passwords or codes.','Copy all private records for convenience.','Assume every clipboard is temporary everywhere.','Clipboard behaviour varies; keep secrets out of practice.'),
 ('Which request is easiest to act on?','I can visit Monday at 3. Is the front door the right entrance?','Do the thing.','Everything is wrong always.','A concrete detail and question create a useful next step.'),
 ('Two learners write different clear sentences with the same meaning. What fits?','Both can be useful; a mentor checks meaning.','Only the exact example can be correct.','The longer message always wins.','Communication is not just copying a model sentence.'),
 ('An app button says Go but saves a list. Which label is clearer?','Save my list.','Maybe.','Button 7.','Name the action the button performs.'),
 ('An AI tool helped write a message. What remains your job?','Understand the message and check its details before use.','Assume the tool has taken responsibility.','Paste a private account code into the draft.','Support does not remove the need to check meaning.'),
 ('A learner uses a screen keyboard and corrects a message. What should count?','The useful edit, with the input method described honestly.','Only a minimum physical-keyboard speed.','Whether the learner used no support.','Functional editing can use accessible methods.'),
 ('You finished a draft and want another opinion. Which is a useful request?','Does the day, time and question make sense?','Tell me I am right without reading it.','Guess every private detail.','Ask for feedback on the meaning that matters.')]),
 reflection='Use a fictional message. Explain one change you made, why it helped the reader, and how you could undo a wrong edit.')

MODULES=[KEYS,WORDS,EDIT]
def attach(units,bank):
    for m in MODULES:
        m['practiceNotice']='Phone, keyboard and supported input are all welcome. Final-text accuracy is practice; no speed target controls rewards.'
        m['checkSkills']=['interpret','apply','reason']
        for name in ('practice','check'):
            for i,item in enumerate(m[name]):item['skill']=m['checkSkills'][i%3]
    attach_guides(units,bank,MODULES,SOURCES,CHECKED)
    for m in MODULES:
        u=next(u for u in units if u['id']==m['id']);u['course']='typing';u['guide']['region']='Keyboard and editing practice'
        u['mission']['label']='Typing & editing';u['mission']['artLabel']='TYPE / EDIT / CHECK'
        u['mission']['startLabel']='Try the keys';u['mission']['brief']=[m['goal'],m['practiceNotice'],'Try a short task, read the example, then check your understanding.']
