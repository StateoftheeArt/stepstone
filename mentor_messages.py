"""Fixed support requests and replies inside the existing private accounts."""
import re
import time
import uuid

SIGNALS = {
    'learner': (
        ('stuck', 'I’m stuck.'),
        ('example', 'Can I get another example?'),
        ('review', 'Please review my work.'),
        ('feedback', 'Please explain my feedback.'),
        ('break', 'I’m taking a break.'),
        ('ready', 'I’m ready for my next step.'),
    ),
    'mentor': (
        ('seen', 'I’ve seen your request.'),
        ('example', 'Try the worked example first.'),
        ('one-step', 'Take one step at a time.'),
        ('reviewing', 'I’ll review your work.'),
        ('feedback-ready', 'Your feedback is in My wins.'),
        ('break', 'Take a break. Your place is saved.'),
    ),
}

def options(sender):
    return [dict(id=key,label=label) for key,label in SIGNALS[sender]]


def install(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS mentor_messages (
      id TEXT PRIMARY KEY, learner TEXT NOT NULL, sender TEXT NOT NULL,
      body TEXT NOT NULL, created REAL NOT NULL, read_at REAL,
      client_key TEXT NOT NULL, UNIQUE(learner,sender,client_key)
    );
    CREATE INDEX IF NOT EXISTS message_thread ON mentor_messages(learner,created,id);
    ''')


def check_learner(db,learner,Problem):
    if not isinstance(learner,str) or not db.execute('SELECT 1 FROM learners WHERE id=?',(learner,)).fetchone():
        raise Problem(404,'Learner not found.')
    own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
    if own and own[0]==learner:
        raise Problem(403,'My learning is your private test space. Messages are for connected learners.')


def unread(db,learner):
    return db.execute("SELECT COUNT(*) FROM mentor_messages WHERE learner=? AND sender='mentor' AND read_at IS NULL",(learner,)).fetchone()[0]


def inbox(db):
    rows=db.execute('''SELECT l.id,l.alias,MAX(m.created) AS latest,
        SUM(CASE WHEN m.sender='learner' AND m.read_at IS NULL THEN 1 ELSE 0 END) AS unread,
        COUNT(*) AS total FROM mentor_messages m JOIN learners l ON l.id=m.learner
        GROUP BY l.id ORDER BY latest DESC,l.id''').fetchall()
    return [dict(r) for r in rows]


def thread(db,learner,viewer,data,Problem):
    check_learner(db,learner,Problem)
    before=data.get('before')
    if before is not None and (not isinstance(before,str) or not 1<=len(before)<=80):
        raise Problem(400,'Choose an earlier message from this conversation.')
    condition='';params=[learner]
    if before:
        row=db.execute('SELECT created,id FROM mentor_messages WHERE id=? AND learner=?',(before,learner)).fetchone()
        if not row:raise Problem(404,'That message is not in this conversation.')
        condition=' AND (created<? OR (created=? AND id<?))';params.extend([row[0],row[0],row[1]])
    rows=db.execute('SELECT id,sender,body,created,read_at FROM mentor_messages WHERE learner=?'+condition+' ORDER BY created DESC,id DESC LIMIT 61',params).fetchall()
    older=len(rows)>60;rows=rows[:60]
    for row in rows:
        if row['sender']!=viewer and row['read_at'] is None:
            db.execute('UPDATE mentor_messages SET read_at=? WHERE id=?',(time.time(),row['id']))
    alias=db.execute('SELECT alias FROM learners WHERE id=?',(learner,)).fetchone()[0]
    messages=[]
    for row in reversed(rows):
        item=dict(row)
        if item['body'] not in dict(SIGNALS.get(item['sender'],())).values():
            item['body']='Earlier text message (saved before preset support requests).'
            item['legacy']=True
        messages.append(item)
    return dict(learner=learner,alias=alias,messages=messages,hasOlder=older,options=options(viewer))


def send(db,learner,sender,data,Problem):
    check_learner(db,learner,Problem)
    if set(data)-{'learner','choice','clientId'}:raise Problem(400,'Choose a preset support request or reply. Free text and attachments are not accepted.')
    choice=data.get('choice');key=data.get('clientId')
    if not isinstance(choice,str) or choice not in dict(SIGNALS.get(sender,())):
        raise Problem(400,'Choose one of the preset support options.')
    body=dict(SIGNALS[sender])[choice]
    if not isinstance(key,str) or not re.fullmatch(r'[a-zA-Z0-9_-]{12,80}',key):raise Problem(400,'Reopen your message and try again.')
    prior=db.execute('SELECT id,body FROM mentor_messages WHERE learner=? AND sender=? AND client_key=?',(learner,sender,key)).fetchone()
    if prior:
        if prior['body']!=body:raise Problem(409,'That send already finished. Reopen the conversation before sending a different message.')
        return dict(id=prior['id'],saved=True)
    now=time.time()
    recent=db.execute('SELECT COUNT(*) FROM mentor_messages WHERE learner=? AND sender=? AND created>?',(learner,sender,now-60)).fetchone()[0]
    today=db.execute('SELECT COUNT(*) FROM mentor_messages WHERE learner=? AND sender=? AND created>?',(learner,sender,now-86400)).fetchone()[0]
    if recent>=5 or today>=60:raise Problem(429,'Give the other person time to read. Your selected request stays here; try again later.')
    mid=uuid.uuid4().hex
    db.execute('INSERT INTO mentor_messages VALUES(?,?,?,?,?,NULL,?)',(mid,learner,sender,body,now,key))
    return dict(id=mid,saved=True)
