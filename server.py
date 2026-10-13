"""Stepstone pilot server. Python standard library; no paid service or AI required."""
from __future__ import annotations
import preview_checks
import device_work
import ai_support
import projects
from check_sampling import sample_check
import mentor_messages
import gift_cards
import mentor_accounts
import argparse
import base64
import hashlib
import json
import math
import os
import random
import re
import secrets
import socket
import sqlite3
import threading
import time
import webbrowser
from contextlib import contextmanager
from http import cookies
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing_evidence import validate as validate_typing
from pathlib import Path
from urllib.parse import urlparse
from placement import evaluate as evaluate_starting_point
from placement import normalize as normalize_starting_point
from placement import plain_number, numeric as placement_numeric
import pip_rewards
import course_access
import daily_tasks
import laptop_finder
from text_filter import acceptable
from human_text import valid_payload,display_safe,MESSAGE as LANGUAGE_MESSAGE
from tutorial import evaluate as evaluate_tutorial
from voice import VoiceEngine, VoiceError
from host_runtime import HostRuntime, shared_address
from foundation import validate as validate_foundation, assigned_progress
from reward_program import RewardProgram, RewardError, MILESTONES

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
CATALOG = json.loads((PUBLIC / 'catalog.json').read_text(encoding='utf-8'))
UNITS = {u['id']:u for u in CATALOG['units'] if u['ready']}
BANK = json.loads((ROOT / 'content/checkpoints.json').read_text(encoding='utf-8'))
STARTING_POINT = json.loads((PUBLIC / 'starting-point.json').read_text(encoding='utf-8'))
TUTORIAL = json.loads((PUBLIC / 'tutorial.json').read_text(encoding='utf-8'))
PROFILE_OPTIONS = json.loads((PUBLIC / 'profile-options.json').read_text(encoding='utf-8'))
FOUNDATION = validate_foundation(json.loads((PUBLIC / 'foundation.json').read_text(encoding='utf-8')), UNITS)
# The sandboxed useful-app preview runs this exact file inline (see project-runtime.js).
PREVIEW_SCRIPT = "'sha256-"+base64.b64encode(hashlib.sha256((PUBLIC/'project-preview-runtime.js').read_text(encoding='utf-8').lstrip('\ufeff').replace('\r\n','\n').encode('utf-8')).digest()).decode()+"'"
MAX_BODY = 180_000
WEEK = 7 * 86400

class Problem(Exception):
    def __init__(self, status, message): self.status, self.message = status, message

def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def pack(value): return json.dumps(value, ensure_ascii=False, separators=(',',':'))
def uid(): return secrets.token_urlsafe(18)
def public_question(q): return {k:v for k,v in q.items() if k not in ('answer','explanation','hint')}
def suitable(value, message):
    # Names and item names stay PG-16. Written work is private; support uses fixed choices.
    if not acceptable(value): raise Problem(400, message)
    return value

def text_field(data, key, lo=0, hi=2000):
    value=data.get(key,'')
    if not isinstance(value,str) or not lo<=len(value.strip())<=hi: raise Problem(400,f'Please check {key.replace("_"," ")} ({lo}–{hi} characters).')
    return value.strip()

def numeric(value):
    value=plain_number(str(value))
    if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:\s*/\s*[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+))?',value): return None
    try:
        bits=[float(x) for x in value.split('/')]
        result=bits[0] if len(bits)==1 else bits[0]/bits[1]
        return result if math.isfinite(result) else None
    except (ValueError,ZeroDivisionError): return None

def correct(q, answer):
    if q['kind']=='choice': return isinstance(answer,str) and answer==q['answer']
    got=numeric(answer)
    return got is not None and abs(got-q['answer'])<=max(1e-9,abs(q['answer'])*1e-6)

def valid_ink(raw):
    if not isinstance(raw,list) or len(raw)>100: raise Problem(400,'The drawing is too large. Please simplify it.')
    count=0
    for stroke in raw:
        if not isinstance(stroke,list): raise Problem(400,'Invalid drawing.')
        count+=len(stroke)
        if count>6000: raise Problem(400,'The drawing is too large. Please simplify it.')
        for p in stroke:
            if not isinstance(p,list) or len(p)!=2 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=1 for v in p): raise Problem(400,'Invalid drawing points.')
    return raw

class Store:
    def __init__(self, directory):
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.path=self.directory/'stepstone.sqlite3';self.lock=threading.RLock()
        self.funded=RewardProgram(FOUNDATION, laptop_units=course_access.required_units(CATALOG))
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, role TEXT NOT NULL, owner TEXT NOT NULL, expires REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS invites (hash TEXT PRIMARY KEY, created REAL NOT NULL, expires REAL NOT NULL, used INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS learners (id TEXT PRIMARY KEY, alias TEXT NOT NULL, recovery TEXT UNIQUE NOT NULL, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS progress (learner TEXT NOT NULL, unit TEXT NOT NULL, stage INTEGER NOT NULL, updated REAL NOT NULL, PRIMARY KEY(learner,unit));
            CREATE TABLE IF NOT EXISTS attempts (id TEXT PRIMARY KEY, learner TEXT NOT NULL, unit TEXT NOT NULL, questions TEXT NOT NULL, started REAL NOT NULL, finished REAL, report TEXT, reviewed REAL, note TEXT NOT NULL DEFAULT '');
            CREATE TABLE IF NOT EXISTS ledger (id TEXT PRIMARY KEY, learner TEXT NOT NULL, delta INTEGER NOT NULL, label TEXT NOT NULL, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS rewards (id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL, cost INTEGER NOT NULL, kind TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1);
            CREATE TABLE IF NOT EXISTS claims (id TEXT PRIMARY KEY, learner TEXT NOT NULL, reward TEXT NOT NULL, status TEXT NOT NULL, cost INTEGER NOT NULL, created REAL NOT NULL, note TEXT NOT NULL DEFAULT '', UNIQUE(learner,reward));
            CREATE TABLE IF NOT EXISTS profiles (learner TEXT PRIMARY KEY, avatar TEXT NOT NULL DEFAULT 'orbit');
            CREATE TABLE IF NOT EXISTS drafts (learner TEXT NOT NULL, unit TEXT NOT NULL, revision INTEGER NOT NULL, content TEXT NOT NULL, updated REAL NOT NULL, PRIMARY KEY(learner,unit));
            CREATE TABLE IF NOT EXISTS activities (id TEXT NOT NULL, learner TEXT NOT NULL, game TEXT NOT NULL, report TEXT NOT NULL, finished REAL NOT NULL, PRIMARY KEY(learner,id));
            CREATE TABLE IF NOT EXISTS starting_points (learner TEXT PRIMARY KEY, revision INTEGER NOT NULL, content TEXT NOT NULL, result TEXT NOT NULL, updated REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS reward_goals (learner TEXT PRIMARY KEY, reward TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS tutorials (learner TEXT PRIMARY KEY, revision INTEGER NOT NULL, content TEXT NOT NULL, updated REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS device_work (learner TEXT NOT NULL, unit TEXT NOT NULL, revision INTEGER NOT NULL, status TEXT NOT NULL, note TEXT NOT NULL, review_note TEXT NOT NULL, updated REAL NOT NULL, PRIMARY KEY(learner,unit));
            CREATE TABLE IF NOT EXISTS device_work_history (id INTEGER PRIMARY KEY AUTOINCREMENT, learner TEXT NOT NULL, unit TEXT NOT NULL, revision INTEGER NOT NULL, actor TEXT NOT NULL, status TEXT NOT NULL, note TEXT NOT NULL, created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS foundation_paths (learner TEXT PRIMARY KEY, content TEXT NOT NULL);
            ''')
            # Additive migration preserves existing rewards and all learner records.
            reward_columns={r[1] for r in db.execute('PRAGMA table_info(rewards)')}
            for column,definition in (
                ('category',"TEXT NOT NULL DEFAULT 'experience'"),
                ('stock','INTEGER'),
                ('minimum_modules','INTEGER NOT NULL DEFAULT 0'),
                ('required_modules',"TEXT NOT NULL DEFAULT '[]'"),
            ):
                if column not in reward_columns: db.execute(f'ALTER TABLE rewards ADD COLUMN {column} {definition}')
            if 'demonstrated' not in {r[1] for r in db.execute('PRAGMA table_info(claims)')}:
                db.execute('ALTER TABLE claims ADD COLUMN demonstrated INTEGER NOT NULL DEFAULT 0')
            if 'details' not in {r[1] for r in db.execute('PRAGMA table_info(profiles)')}:
                db.execute("ALTER TABLE profiles ADD COLUMN details TEXT NOT NULL DEFAULT '{}'")
            for rid,title,description,cost,kind in [('theme-ocean','Ocean colours','Unlock a blue colour theme.',30,'theme'),('theme-sunset','Sunset colours','Unlock a warm colour theme.',60,'theme')]:
                db.execute('INSERT OR IGNORE INTO rewards(id,title,description,cost,kind) VALUES(?,?,?,?,?)',(rid,title,description,cost,kind))
            mentor_accounts.install(db)
            mentor_messages.install(db)
            ai_support.install(db)
            self.funded.install(db)
            gift_cards.install(db)
            pip_rewards.install(db,PROFILE_OPTIONS)
            daily_tasks.install(db)
    @contextmanager
    def db(self):
        with self.lock:
            conn=sqlite3.connect(self.path,timeout=15);conn.row_factory=sqlite3.Row
            try:
                conn.execute('BEGIN IMMEDIATE')
                yield conn
                conn.commit()
            except Exception:
                conn.rollback();raise
            finally: conn.close()
    def access_code(self):
        return 'w'+getattr(self,'identity','root')+'.'+uid()+uid()
    def session(self, db, role, owner):
        token=self.access_code();duration=43200 if role=='mentor' else 30*86400
        db.execute('INSERT INTO sessions VALUES(?,?,?,?)',(digest(token),role,owner,time.time()+duration))
        db.execute('DELETE FROM sessions WHERE expires<?',(time.time(),))
        return token,duration
    def owner(self, db, token, role):
        row=db.execute('SELECT owner FROM sessions WHERE token=? AND role=? AND expires>?',(digest(token),role,time.time())).fetchone()
        if not row: raise Problem(401,'Please sign in again.')
        return row['owner']
    def points(self,db,learner): return db.execute('SELECT COALESCE(SUM(delta),0) FROM ledger WHERE learner=?',(learner,)).fetchone()[0]
    def welcome_awards(self,db,learner):
        return {step:bool(db.execute('SELECT 1 FROM ledger WHERE id=?',('welcome-'+step+'-'+learner,)).fetchone()) for step in ('starting','tutorial')}
    def award_welcome(self,db,learner,step):
        label='Starting questions completed' if step=='starting' else 'Guided setup completed'
        db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)',('welcome-'+step+'-'+learner,learner,5,label,time.time()))
    def rewards(self,db,personal=False,mentor=False,learner=None):
        items=[]
        for r in db.execute("SELECT * FROM rewards WHERE (?=1 OR active=1) AND (?=0 OR kind='theme') ORDER BY cost,title",(int(mentor),int(personal))):
            item=dict(r);item['required_modules']=json.loads(r['required_modules'])
            committed=db.execute("SELECT COUNT(*) FROM claims WHERE reward=? AND status IN ('pending','approved','given')",(r['id'],)).fetchone()[0]
            item['available']=None if r['stock'] is None else max(0,r['stock']-committed)
            if mentor:item['committed']=committed
            items.append(item)
        if not personal: items=self.funded.rewards(db,learner)+items
        return items
    def module_wins(self,db,learner):
        return pip_rewards.wins(db,learner,PROFILE_OPTIONS)

    def learner(self,db,learner):
        row=db.execute('SELECT id,alias FROM learners WHERE id=?',(learner,)).fetchone()
        if not row: raise Problem(401,'Please sign in again.')
        attempts=[]
        for a in db.execute('SELECT id,unit,finished,report,reviewed,note FROM attempts WHERE learner=? AND finished IS NOT NULL ORDER BY finished DESC LIMIT 200',(learner,)):
            attempts.append(dict(a)|{'report':json.loads(a['report'])})
        progress={p['unit']:p['stage'] for p in db.execute('SELECT unit,stage FROM progress WHERE learner=?',(learner,))}
        claims=[dict(x) for x in db.execute('SELECT c.*,r.title,r.kind FROM claims c JOIN rewards r ON c.reward=r.id WHERE c.learner=?',(learner,))]
        claims=gift_cards.claims(db,learner)+self.funded.claims(db,learner)+claims
        mastered=[r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1",(learner,))]
        earned=db.execute("SELECT COALESCE(SUM(delta),0) FROM ledger WHERE learner=? AND delta>0 AND id NOT LIKE 'refund-%'",(learner,)).fetchone()[0]
        total=db.execute('SELECT COUNT(*) FROM attempts WHERE learner=? AND finished IS NOT NULL',(learner,)).fetchone()[0]
        profile=db.execute('SELECT avatar,details FROM profiles WHERE learner=?',(learner,)).fetchone()
        profile_value={'avatar':profile['avatar'],**json.loads(profile['details'])} if profile else {'avatar':'orbit'}
        own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
        personal=bool(own and own['value']==learner)
        start=db.execute('SELECT * FROM starting_points WHERE learner=?',(learner,)).fetchone()
        starting=dict(revision=start['revision'],data=json.loads(start['content']),result=json.loads(start['result']),updated=start['updated']) if start else None
        goal=db.execute('SELECT reward FROM reward_goals WHERE learner=?',(learner,)).fetchone()
        if starting and starting['result'].get('complete'):
            pip_rewards.sync_grants(db,learner,PROFILE_OPTIONS)
            pip_rewards.sync_starting_items(db,learner,PROFILE_OPTIONS,CATALOG,starting['result'])
        return dict(row)|dict(messagesUnread=mentor_messages.unread(db,learner),personal=personal,courseReadiness=course_access.readiness(CATALOG,mastered),dailyTasks=daily_tasks.snapshot(db,learner),project=projects.get(db,learner),aiSupport=ai_support.record(db,learner,self.funded),deviceWork=device_work.records(db,learner),foundation=assigned_progress(db,learner,FOUNDATION,mastered),startingPoint=starting,tutorial=self.tutorial(db,learner),welcomeAwards=self.welcome_awards(db,learner),goal=goal['reward'] if goal else None,points=self.points(db,learner),earned=earned,mastered=mastered,moduleWins=self.module_wins(db,learner),pipInventory=sorted(pip_rewards.inventory(db,learner)),pipFood=pip_rewards.food(db,learner),totalChecks=total,profile=profile_value,progress=progress,attempts=attempts,claims=claims,cardExchange=None if personal else gift_cards.snapshot(db,learner,self.funded),rewards=self.rewards(db,personal,learner=learner))
    def tutorial(self,db,learner):
        row=db.execute('SELECT * FROM tutorials WHERE learner=?',(learner,)).fetchone()
        if not row:return None
        content,result=evaluate_tutorial(TUTORIAL,json.loads(row['content']))
        if db.execute('SELECT 1 FROM settings WHERE key=?',('tutorial-skip-'+learner,)).fetchone():result={**result,'complete':True,'skipped':True}
        return dict(revision=row['revision'],data=content,result=result,updated=row['updated'])
    def require_tutorial(self,db,learner):
        record=self.tutorial(db,learner)
        if not record or not record['result']['complete']:
            raise Problem(409,'Finish the quick tour first. Your existing work is still saved.')

class Handler(SimpleHTTPRequestHandler):
    server_version='Stepstone/1'
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(PUBLIC),**kwargs)
    @property
    def store(self): return getattr(self,'_store',self.server.store)
    def log_message(self,fmt,*args):
        # No tokens, request bodies, aliases, or query strings in access logs.
        if getattr(self,'path','').startswith('/api/'): return
        # Request fragments never arrive here; discard query strings as well.
        super().log_message('%s %s', self.command, urlparse(getattr(self,'path','')).path)
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Permissions-Policy','camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy',f"default-src 'self'; script-src 'self' {PREVIEW_SCRIPT}; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        if self.path.startswith('/api/'): self.send_header('Cache-Control','no-store')
        else: self.send_header('Cache-Control','no-cache')
        super().end_headers()
    def boundary(self,mutation=False):
        host=self.headers.get('Host','').lower()
        # A hosting health check may use another verified domain. Health returns no private records.
        health=not mutation and urlparse(self.path).path=='/api/health'
        if host not in self.server.allowed_hosts and not health: raise Problem(403,'This host is not configured for this pilot.')
        origin=self.headers.get('Origin')
        if origin and origin not in ('http://'+host,'https://'+host): raise Problem(403,'Request origin does not match this app.')
        if mutation and self.headers.get('Content-Type','').split(';')[0]!='application/json': raise Problem(415,'Use JSON for this request.')
    def token(self,role):
        jar=cookies.SimpleCookie()
        try: jar.load(self.headers.get('Cookie',''))
        except cookies.CookieError: return ''
        value=jar.get('stepstone_'+role)
        return value.value if value else ''
    def local_host(self):
        return self.client_address[0] in ('127.0.0.1','::1') and self.headers.get('Host','').lower() in self.server.local_hosts
    def local_owner_request(self):
        forwarded=any(name.lower()=='forwarded' or name.lower().startswith('x-forwarded-') for name in self.headers)
        return self.local_host() and not forwarded and self.headers.get('Sec-Fetch-Site','')!='cross-site'
    def mentor_owner(self,db):
        return self.server.accounts.owner(self,db)
    def manager_settings(self):
        runtime=self.server.runtime
        return dict(desktop=runtime.desktop,canManageHost=self.local_owner_request() and runtime.desktop and bool(self.store.account and self.store.account.get('hostOwner')),
                    access='account',
                    keepRunning=runtime.keep_running if runtime.desktop else True,idleSeconds=runtime.idle_seconds,
                    sharedAddress=self.server.public_url,sharingReady=bool(self.server.public_url),
                    localAddress=f'http://localhost:{self.server.server_address[1]}',
                    recovery=self.store.backups.status())
    def learner_link(self,kind,code):
        base=self.server.public_url or ('https://' if self.server.secure_cookies else 'http://')+self.headers['Host']
        return base+'/#'+kind+'/'+code
    def cookie(self,role,token,duration):
        secure='; Secure' if self.server.secure_cookies else ''
        return f'stepstone_{role}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={duration}{secure}'
    def respond(self,value,status=200,cookie=None):
        # Keep the original draft editable; never expose legacy language in shared reports.
        if status<400 and urlparse(self.path).path!='/api/drafts':value=display_safe(value)
        body=pack(value).encode('utf-8');self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)))
        if cookie:
            for item in cookie if isinstance(cookie,list) else [cookie]: self.send_header('Set-Cookie',item)
        self.end_headers();self.wfile.write(body)
    def do_GET(self):
        try:
            self.boundary()
            path=urlparse(self.path).path
            if path.startswith('/api/'):
                self._store=self.server.store if path=='/api/health' else self.server.accounts.choose(self,path)
                with self.store.db() as db: result=self.get_api(db,path)
                return self.respond(result)
            # Only the public directory is served. Do not expose symlinks or listings.
            resolved=Path(self.translate_path(path)).resolve()
            if not resolved.is_relative_to(PUBLIC.resolve()) or (resolved.is_dir() and path!='/'): raise Problem(404,'Not found.')
            return super().do_GET()
        except (Problem,RewardError) as e: self.respond({'error':e.message},e.status)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError): pass
    def do_HEAD(self):
        try:
            self.boundary()
            path=urlparse(self.path).path
            resolved=Path(self.translate_path(path)).resolve()
            if path.startswith('/api/') or not resolved.is_relative_to(PUBLIC.resolve()) or (resolved.is_dir() and path!='/'):
                raise Problem(404,'Not found.')
            return super().do_HEAD()
        except (Problem,RewardError) as e:
            self.send_response(e.status);self.send_header('Content-Length','0');self.end_headers()
    def do_POST(self):
        try:
            try: length=int(self.headers.get('Content-Length','0'))
            except ValueError: raise Problem(400,'Invalid request length.')
            if not 0<length<=MAX_BODY: raise Problem(413,'Request is too large or empty.')
            raw=self.rfile.read(length)
            self.boundary(True)
            try: data=json.loads(raw)
            except (ValueError,UnicodeDecodeError): raise Problem(400,'Invalid JSON.')
            if not isinstance(data,dict): raise Problem(400,'Expected an object.')
            path=urlparse(self.path).path
            if not valid_payload(data):raise Problem(400,LANGUAGE_MESSAGE)
            if path=='/api/mentor/setup':
                result,cookie=self.server.accounts.setup(self,data)
                return self.respond(result,cookie=cookie)
            self._store=self.server.accounts.choose(self,path,data)
            if path=='/api/mentor/laptops':
                with self.store.db() as db:
                    self.mentor_owner(db)
                # Read retailer pages outside the account transaction. No learner
                # identifiers or shopping credentials are sent to any retailer.
                return self.respond(laptop_finder.cached_compare())
            if path=='/api/read-aloud':
                try: audio=self.server.voice.speak(data.get('text'))
                except ValueError as e: raise Problem(400,str(e))
                except VoiceError as e: raise Problem(503,str(e))
                self.send_response(200)
                self.send_header('Content-Type','audio/wav')
                self.send_header('Content-Length',str(len(audio)))
                self.end_headers();self.wfile.write(audio)
                return
            if urlparse(self.path).path=='/api/mentor/backup':
                with self.store.db() as db:
                    self.mentor_owner(db)
                try:
                    self.store.backups.create()
                except ValueError as e:
                    raise Problem(409,str(e))
                except (OSError,sqlite3.Error):
                    raise Problem(503,'The recovery copy did not finish. Check host storage and try again.')
                return self.respond(self.manager_settings())
            with self.store.db() as db: result,cookie=self.post_api(db,urlparse(self.path).path,data)
            self.respond(result,cookie=cookie)
        except (Problem,RewardError) as e: self.respond({'error':e.message},e.status)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError): pass
        except Exception:
            import traceback;traceback.print_exc()
            self.respond({'error':'The save did not finish. Your browser will keep the pending check. Please try again.'},500)
    def get_api(self,db,path):
        if path=='/api/health':
            return dict(app='stepstone',version=41,desktop=self.server.runtime.desktop,softVoice=self.server.voice.available,mentorAccess='account',localClaim=self.local_owner_request() and not self.server.store.account,previousPassphrase=bool(db.execute("SELECT 1 FROM settings WHERE key='mentor'").fetchone()))
        if path=='/api/me':
            learner=self.store.owner(db,self.token('learner'),'learner')
            daily_tasks.mark(db,learner,'visit')
            return self.store.learner(db,learner)
        if path=='/api/drafts':
            learner=self.store.owner(db,self.token('learner'),'learner')
            return {r['unit']:dict(revision=r['revision'],data=json.loads(r['content'])) for r in db.execute('SELECT * FROM drafts WHERE learner=?',(learner,))}
        if path=='/api/mentor':
            self.mentor_owner(db)
            own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
            personal=own['value'] if own else ''
            learners=[]
            for l in db.execute('SELECT id,alias,created FROM learners WHERE id!=? ORDER BY created DESC',(personal,)):
                info=self.store.learner(db,l['id']);learners.append(dict(l)|dict(profile=dict(avatar=info['profile'].get('avatar','fox')),points=info['points'],passed=len(info['mastered']),deviceWork=info['deviceWork'],project=info['project'],aiSupport=info['aiSupport'],foundation=info['foundation'],startingPoint=info['startingPoint'],tutorial=info['tutorial'],goal=info['goal']))
            reports=[dict(r)|{'report':json.loads(r['report'])} for r in db.execute('SELECT a.*,l.alias FROM attempts a JOIN learners l ON a.learner=l.id WHERE a.finished IS NOT NULL AND a.learner!=? ORDER BY a.finished DESC LIMIT 300',(personal,))]
            for r in reports: r.pop('questions',None)
            claims=gift_cards.claims(db)+self.store.funded.claims(db)+[dict(c) for c in db.execute('SELECT c.*,l.alias,r.title,r.kind,r.category FROM claims c JOIN learners l ON c.learner=l.id JOIN rewards r ON c.reward=r.id WHERE c.learner!=? ORDER BY c.created DESC',(personal,))]
            return dict(**self.server.accounts.overview(self,db),settings=self.manager_settings(),messages=mentor_messages.inbox(db),learners=learners,reports=reports,personalReady=bool(own),funding=self.store.funded.summary(db),aiMonths=ai_support.history(db),rewards=self.store.rewards(db,mentor=True),claims=claims,giftCardProviders=gift_cards.PROVIDERS,cardBudgets=gift_cards.budgets(db),cardCap=gift_cards.CAP_CENTS)
        raise Problem(404,'Not found.')
    def client_key(self):
        # Behind the hosting proxy every request comes from the proxy, whose load balancer
        # appends the connecting address. Only that last entry is trusted, and only when hosted.
        if self.server.trust_forwarded:
            forwarded=[part.strip() for part in self.headers.get('X-Forwarded-For','').split(',') if part.strip()]
            if forwarded: return forwarded[-1]
        return self.client_address[0]
    def throttle(self,key):
        # Only failed attempts count, so a busy shared address is not locked out by normal sign-ins.
        now=time.time();attempts=self.server.logins.setdefault(key,[])
        attempts[:]=[t for t in attempts if now-t<900]
        if len(attempts)>=12: raise Problem(429,'Too many sign-in attempts. Please wait 15 minutes.')
    def count_attempt(self,key):
        self.server.logins.setdefault(key,[]).append(time.time())
    def post_api(self,db,path,data):
        if path in ('/api/preview-check','/api/preview-result'):
            return preview_checks.handle(path,data,UNITS,BANK,public_question,correct,Problem),None
        if path=='/api/presence':
            self.server.runtime.touch()
            return dict(ok=True),None
        account_result=self.server.accounts.post(self,db,path,data)
        if account_result is not None:return account_result
        if path=='/api/join':
            key=(self.client_key(),'join');self.throttle(key)
            code=text_field(data,'code',8,100);alias=suitable(text_field(data,'alias',1,16),'Choose a different nickname. Names in Stepstone need to suit everyone.')
            invite=db.execute('SELECT * FROM invites WHERE hash=?',(digest(code),)).fetchone()
            if not invite or invite['used'] or invite['expires']<time.time():
                self.count_attempt(key);raise Problem(400,'This invite is used or expired. Ask your mentor for a new one.')
            if data.get('share') is not True: raise Problem(400,'Please acknowledge what is shared before joining.')
            learner=uid();recovery=self.store.access_code()
            db.execute('UPDATE invites SET used=1 WHERE hash=?',(digest(code),))
            db.execute('INSERT INTO learners VALUES(?,?,?,?)',(learner,alias,digest(recovery),time.time()))
            avatar=data.get('avatar','orbit')
            if avatar not in ['orbit','bolt','pixel','leaf','comet','wave',*PROFILE_OPTIONS['companions']]: raise Problem(400,'Choose an available avatar.')
            db.execute('INSERT INTO profiles(learner,avatar) VALUES(?,?)',(learner,avatar))
            token,duration=self.store.session(db,'learner',learner)
            self.server.logins.pop(key,None)
            db.execute('DELETE FROM sessions WHERE token=? AND role=\'mentor\'',(digest(self.token('mentor')),))
            daily_tasks.mark(db,learner,'visit')
            return self.store.learner(db,learner)|dict(recovery=recovery),[self.cookie('learner',token,duration),self.cookie('mentor','',0)]
        if path=='/api/login':
            key=(self.client_key(),'learner');self.throttle(key)
            code=text_field(data,'code',10,100)
            row=db.execute('SELECT id FROM learners WHERE recovery=?',(digest(code),)).fetchone()
            if not row: self.count_attempt(key);raise Problem(401,'That sign-in code did not match.')
            if data.get('expectedLearner',row['id'])!=row['id']: raise Problem(409,'There is unsent work for another learner on this device. Use that learner’s return link first to save it.')
            token,duration=self.store.session(db,'learner',row['id'])
            self.server.logins.pop(key,None)
            db.execute('DELETE FROM sessions WHERE token=? AND role=\'mentor\'',(digest(self.token('mentor')),))
            daily_tasks.mark(db,row['id'],'visit')
            return self.store.learner(db,row['id']),[self.cookie('learner',token,duration),self.cookie('mentor','',0)]
        if path=='/api/logout':
            role=data.get('role')
            if role not in ('learner','mentor'): raise Problem(400,'Unknown account type.')
            if role=='mentor':db.execute('DELETE FROM mentor_devices WHERE token=?',(digest(self.token(role)),))
            db.execute('DELETE FROM sessions WHERE token=?',(digest(self.token(role)),))
            return dict(ok=True),[self.cookie(role,'',0),self.cookie('learner','',0),self.cookie('mentor_pending','',0)] if role=='mentor' else self.cookie(role,'',0)
        if path.startswith('/api/mentor/'):
            self.mentor_owner(db)
            if path.startswith('/api/mentor/cards/'):
                action=path.rsplit('/',1)[1]
                if action in ('reserve','deliver') or (action=='decision' and data.get('status')=='approved'):self.reward_recovery_boundary(db)
                fn={'reserve':gift_cards.reserve,'release':gift_cards.release,'decision':gift_cards.decision,'deliver':gift_cards.deliver}.get(action)
                if not fn:raise Problem(404,'Not found.')
                return fn(db,data,self.store.funded),None
            if path in ('/api/mentor/messages/thread','/api/mentor/messages/send'):
                target=text_field(data,'learner',1,100)
                result=mentor_messages.thread(db,target,'mentor',data,Problem) if path.endswith('/thread') else mentor_messages.send(db,target,'mentor',data,Problem)
                return result,None
            if path=='/api/mentor/recovery-reconciled':
                if data.get('confirmed') is not True:
                    raise Problem(400,'Confirm that later real-world rewards have been reconciled.')
                note=text_field(data,'note',10,1000)
                hold=db.execute("SELECT value FROM settings WHERE key='recoveryHold'").fetchone()
                if hold:
                    self.store.funded.audit(db,'mentor','recovery-reconciled',dict(restore=json.loads(hold['value']),note=note))
                    db.execute("DELETE FROM settings WHERE key='recoveryHold'")
                return dict(ok=True),None
            if (path in ('/api/mentor/ai/reserve','/api/mentor/ai/approve','/api/mentor/ai/activate') or
                    (path in ('/api/mentor/claim','/api/mentor/funded/claim') and data.get('status')=='approved')):
                self.reward_recovery_boundary(db)
            if path=='/api/mentor/device-work':
                target=text_field(data,'learner',1,100)
                if not db.execute('SELECT 1 FROM learners WHERE id=?',(target,)).fetchone():raise Problem(404,'Learner not found.')
                return dict(deviceWork=device_work.save(db,data,target,UNITS,Problem,mentor=True)),None
            if path=='/api/mentor/settings':
                if not self.local_owner_request() or not self.server.runtime.desktop or not self.store.account.get('hostOwner'):
                    raise Problem(403,'Change laptop background settings from Mentor space on the host laptop.')
                enabled=data.get('keepRunning')
                if type(enabled) is not bool: raise Problem(400,'Choose on or off for background running.')
                db.execute("INSERT INTO settings(key,value) VALUES('keepRunning',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(pack(enabled),))
                self.server.runtime.set_background(enabled)
                return self.manager_settings(),None
            if path=='/api/mentor/tutorial-control':
                own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
                if not own or data.get('learner')!=own['value']:raise Problem(403,'Tutorial controls apply only to your own My learning account.')
                learner=own['value'];prior=self.store.tutorial(db,learner)
                revision=prior['revision'] if prior else 0
                if type(data.get('revision')) is not int or data['revision']!=revision:raise Problem(409,'Your setup changed. Reopen the tutorial controls.')
                action=data.get('action')
                if action not in ('restart','skip'):raise Problem(400,'Choose restart or skip.')
                events=[]
                start=db.execute('SELECT result FROM starting_points WHERE learner=?',(learner,)).fetchone()
                if action=='restart' and start and json.loads(start['result'])['complete']:
                    events=[dict(action=a) for a in TUTORIAL['setupActions'][:4]]
                    self.store.award_welcome(db,learner,'starting')
                content=dict(version=2,events=events,count=4,answer='',bagChecked=False,answerChecked=False,hint=False)
                db.execute('INSERT INTO tutorials VALUES(?,?,?,?) ON CONFLICT(learner) DO UPDATE SET revision=excluded.revision,content=excluded.content,updated=excluded.updated',(learner,revision+1,pack(content),time.time()))
                if action=='skip':db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',('tutorial-skip-'+learner,'true'))
                else:db.execute('DELETE FROM settings WHERE key=?',('tutorial-skip-'+learner,))
                return self.store.learner(db,learner),None
            if path=='/api/mentor/reset-learning':
                own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
                if not own or data.get('learner')!=own['value']: raise Problem(409,'Open your own My learning account before resetting it.')
                if data.get('confirmation')!='RESET MY LEARNING': raise Problem(400,'Confirm that only your own learning record should be reset.')
                previous=own['value']
                db.execute('DELETE FROM settings WHERE key=?',('tutorial-skip-'+previous,))
                # A new identity prevents an old offline tab from restoring deleted
                # drafts or submitting an old attempt into the fresh record.
                for table in ('progress','attempts','ledger','claims','profiles','mentor_messages','drafts','activities','starting_points','reward_goals','tutorials','foundation_paths','device_work','device_work_history','ai_plans','learner_projects','pip_grants','pip_food','pip_feeds','pip_review_grants','pip_starting_items','daily_tasks'):
                    db.execute(f'DELETE FROM {table} WHERE learner=?',(previous,))
                db.execute("DELETE FROM sessions WHERE role='learner' AND owner=?",(previous,))
                db.execute('DELETE FROM learners WHERE id=?',(previous,))
                learner=uid()
                db.execute('INSERT INTO learners VALUES(?,?,?,?)',(learner,'My learning',digest(uid()+uid()),time.time()))
                db.execute("UPDATE settings SET value=? WHERE key='mentorLearner'",(learner,))
                token,duration=self.store.session(db,'learner',learner)
                return self.store.learner(db,learner),self.cookie('learner',token,duration)
            if path=='/api/mentor/learn':
                own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
                if own: learner=own['value']
                else:
                    learner=uid()
                    db.execute('INSERT INTO learners VALUES(?,?,?,?)',(learner,'My learning',digest(uid()+uid()),time.time()))
                    db.execute("INSERT INTO settings VALUES('mentorLearner',?)",(learner,))
                token,duration=self.store.session(db,'learner',learner)
                return self.store.learner(db,learner),self.cookie('learner',token,duration)
            if path=='/api/mentor/invite':
                code=self.store.access_code();now=time.time();db.execute('INSERT INTO invites(hash,created,expires) VALUES(?,?,?)',(digest(code),now,now+WEEK))
                return dict(code=code,expires=now+WEEK,url=self.learner_link('join',code),sharingReady=bool(self.server.public_url)),None
            if path=='/api/mentor/review':
                attempt=text_field(data,'id',1,100);note=text_field(data,'note',0,2000)
                if not db.execute('SELECT 1 FROM attempts WHERE id=? AND finished IS NOT NULL',(attempt,)).fetchone(): raise Problem(404,'Report not found.')
                db.execute('UPDATE attempts SET reviewed=?,note=? WHERE id=?',(time.time(),note,attempt))
                return dict(ok=True),None
            if path=='/api/mentor/reward':
                title=text_field(data,'title',2,80);description=text_field(data,'description',1,500);cost=data.get('cost')
                suitable(title+'\n'+description,'Use different words for this reward. Names and items in Stepstone need to suit everyone.')
                if type(cost) is not int or not 10<=cost<=10000: raise Problem(400,'Choose a whole-number cost from 10 to 10000 points.')
                category=data.get('category','experience');stock=data.get('stock')
                minimum=data.get('minimum_modules',0);required=data.get('required_modules',[])
                if category not in ('experience','giftcard','laptop'): raise Problem(400,'Choose an available reward type.')
                if (category!='experience' and stock is None) or (stock is not None and (type(stock) is not int or not 0<=stock<=10000)): raise Problem(400,'Record a whole number of secured rewards. Use zero while waiting for funding.')
                if type(minimum) is not int or not 0<=minimum<=len(UNITS): raise Problem(400,'Choose a valid completed-module target.')
                if type(required) is not list or len(required)>len(UNITS) or any(type(x) is not str or x not in UNITS for x in required) or len(set(required))!=len(required): raise Problem(400,'Choose valid required modules.')
                if category!='experience': raise Problem(409,'Use Funded milestones for new gift cards and laptops. Earlier agreements stay available with their original terms.')
                rid=uid();db.execute('INSERT INTO rewards(id,title,description,cost,kind,category,stock,minimum_modules,required_modules) VALUES(?,?,?,?,?,?,?,?,?)',(rid,title,description,cost,'mentor',category,stock,minimum,pack(required)))
                return dict(ok=True,id=rid),None
            if path=='/api/mentor/reward-stock':
                rid=text_field(data,'id',1,100);stock=data.get('stock')
                reward=db.execute("SELECT * FROM rewards WHERE id=? AND kind='mentor'",(rid,)).fetchone()
                if not reward: raise Problem(404,'Agreed reward not found.')
                if 'expectedStock' not in data or data['expectedStock']!=reward['stock']: raise Problem(409,'This reward changed. Refresh before updating its secured quantity.')
                if type(stock) is not int or not 0<=stock<=10000: raise Problem(400,'Use a whole number of secured rewards.')
                committed=db.execute("SELECT COUNT(*) FROM claims WHERE reward=? AND status IN ('pending','approved','given')",(rid,)).fetchone()[0]
                if stock<committed: raise Problem(409,'The total cannot be below rewards already reserved or given.')
                db.execute('UPDATE rewards SET stock=? WHERE id=?',(stock,rid))
                return dict(ok=True),None
            if path=='/api/mentor/claim':
                if db.execute('SELECT 1 FROM funded_claims WHERE id=?',(text_field(data,'id',1,100),)).fetchone():
                    return self.store.funded.mentor(db,'claim',data),None
                claim=db.execute('SELECT * FROM claims WHERE id=?',(text_field(data,'id',1,100),)).fetchone()
                state=data.get('status');note=text_field(data,'note',0,500)
                if not claim: raise Problem(404,'Reward request not found.')
                if 'expectedStatus' in data and data['expectedStatus']!=claim['status'] and state!=claim['status']: raise Problem(409,'This request changed. Reopen it before deciding.')
                allowed={'pending':('approved','declined'),'approved':('given','declined'),'given':(),'declined':()}
                if state==claim['status']: return dict(ok=True),None
                if state not in allowed[claim['status']]: raise Problem(409,'That reward request has already moved to another step.')
                reward=db.execute('SELECT category FROM rewards WHERE id=?',(claim['reward'],)).fetchone()
                if state=='approved' and reward['category']=='laptop':
                    if data.get('demonstrated') is not True: raise Problem(400,'Confirm the learner has demonstrated and explained their project before approving the laptop.')
                    db.execute('UPDATE claims SET demonstrated=1 WHERE id=?',(claim['id'],))
                db.execute('UPDATE claims SET status=?,note=? WHERE id=?',(state,note,claim['id']))
                if state=='declined': db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)',('refund-'+claim['id'],claim['learner'],claim['cost'],'Reward points returned',time.time()))
                return dict(ok=True),None
            if path=='/api/mentor/project-review':
                return projects.review(db,data),None
            if path.startswith('/api/mentor/ai/'):
                return ai_support.mentor_action(db,path.rsplit('/',1)[1],data,self.store),None
            if path.startswith('/api/mentor/funded/'):
                return self.store.funded.mentor(db,path.rsplit('/',1)[1],data),None
            if path=='/api/mentor/recovery':
                learner=text_field(data,'id',1,100)
                if not db.execute('SELECT 1 FROM learners WHERE id=?',(learner,)).fetchone(): raise Problem(404,'Learner not found.')
                code=self.store.access_code();db.execute('UPDATE learners SET recovery=? WHERE id=?',(digest(code),learner))
                db.execute("DELETE FROM sessions WHERE role='learner' AND owner=?",(learner,))
                return dict(code=code,url=self.learner_link('resume',code),sharingReady=bool(self.server.public_url)),None
            raise Problem(404,'Not found.')
        learner=self.store.owner(db,self.token('learner'),'learner')
        if data.get('learner',learner)!=learner: raise Problem(409,'The signed-in learner changed. Sign in with the original code to save this work.')
        if path in ('/api/reward','/api/cards/request','/api/ai/request'):self.reward_recovery_boundary(db)
        if path=='/api/cards/request':
            result=gift_cards.request(db,learner,data,self.store)
            return result|dict(me=self.store.learner(db,learner)),None
        if path=='/api/cards/reveal':return gift_cards.reveal(db,learner,data),None
        if path in ('/api/messages/thread','/api/messages/send'):
            result=mentor_messages.thread(db,learner,'learner',data,Problem) if path.endswith('/thread') else mentor_messages.send(db,learner,'learner',data,Problem)
            return result,None
        if path=='/api/tutorial':
            revision=data.get('revision')
            if type(revision) is not int or revision<0:raise Problem(400,'Invalid tour revision.')
            try:content,result=evaluate_tutorial(TUTORIAL,data.get('data'))
            except ValueError as error:raise Problem(400,str(error))
            prior=self.store.tutorial(db,learner)
            if content['version']==2:
                actions=[event['action'] for event in content['events']]
                start=db.execute('SELECT result FROM starting_points WHERE learner=?',(learner,)).fetchone()
                if 'questions' in actions and (not start or not json.loads(start['result'])['complete']):raise Problem(409,'Finish the starting questions first. You can choose I do not know yet.')
                if 'profile' in actions:
                    p=db.execute('SELECT details FROM profiles WHERE learner=?',(learner,)).fetchone()
                    if not p or not json.loads(p['details']).get('ready'):raise Problem(409,'Save your profile before continuing.')
            if prior and prior['data']==content:return prior,None
            upgrading=prior and prior['data']['version']==1 and content['version']==2 and not prior['result']['complete']
            if (prior['revision'] if prior else 0)!=revision or (prior and not upgrading and (content['version']!=prior['data']['version'] or content['events'][:len(prior['data']['events'])]!=prior['data']['events'])):
                raise Problem(409,'This tour changed on another device. Load the saved tour to continue.')
            updated=time.time()
            db.execute('INSERT INTO tutorials VALUES(?,?,?,?) ON CONFLICT(learner) DO UPDATE SET revision=excluded.revision,content=excluded.content,updated=excluded.updated',
                       (learner,revision+1,pack(content),updated))
            if content['version']==2 and result['complete'] and not db.execute('SELECT 1 FROM settings WHERE key=?',('tutorial-skip-'+learner,)).fetchone():
                self.store.award_welcome(db,learner,'starting')
                self.store.award_welcome(db,learner,'tutorial')
            return dict(revision=revision+1,data=content,result=result,updated=updated),None
        if path=='/api/starting-point':
            content,revision=data.get('data'),data.get('revision')
            if type(revision) is not int or revision<0: raise Problem(400,'Invalid starting-check revision.')
            try: result=evaluate_starting_point(STARTING_POINT,content)
            except ValueError as error: raise Problem(400,str(error))
            content=normalize_starting_point(content)
            prior=db.execute('SELECT * FROM starting_points WHERE learner=?',(learner,)).fetchone()
            if prior and json.loads(prior['content'])==content:
                if result['complete']:self.store.award_welcome(db,learner,'starting')
                return self.store.learner(db,learner)['startingPoint'],None
            if (prior['revision'] if prior else 0)!=revision:
                raise Problem(409,'This starting check changed on another device. Load the saved check to continue.')
            updated=time.time()
            db.execute('INSERT INTO starting_points VALUES(?,?,?,?,?) ON CONFLICT(learner) DO UPDATE SET revision=excluded.revision,content=excluded.content,result=excluded.result,updated=excluded.updated',
                       (learner,revision+1,pack(content),pack(result),updated))
            if result['complete']:
                self.store.award_welcome(db,learner,'starting')
                pip_rewards.sync_grants(db,learner,PROFILE_OPTIONS)
                pip_rewards.sync_starting_items(db,learner,PROFILE_OPTIONS,CATALOG,result)
            return dict(revision=revision+1,data=content,result=result,updated=updated),None
        if path=='/api/reward-goal':
            rid=text_field(data,'id',1,100)
            reward={'id':rid} if rid in (*MILESTONES,'card-exchange') else db.execute("SELECT id FROM rewards WHERE id=? AND active=1 AND kind='mentor'",(rid,)).fetchone()
            if not reward: raise Problem(404,'Choose an available agreed reward.')
            own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
            if own and own['value']==learner: raise Problem(400,'Agreed learner rewards belong to the learners you support.')
            db.execute('INSERT INTO reward_goals VALUES(?,?) ON CONFLICT(learner) DO UPDATE SET reward=excluded.reward',(learner,reward['id']))
            return self.store.learner(db,learner),None
        if path.startswith('/api/project/'):
            projects.action(db,path.rsplit('/',1)[1],data,learner,self.store)
            return self.store.learner(db,learner),None
        if path.startswith('/api/ai/'):
            ai_support.learner_action(db,path.rsplit('/',1)[1],data,learner,self.store)
            return self.store.learner(db,learner),None
        if path=='/api/device-work':
            device_work.save(db,data,learner,UNITS,Problem)
            return self.store.learner(db,learner),None
        if path=='/api/daily/play':
            if pip_rewards.food(db,learner)['remaining']<=0:
                raise Problem(409,'Feed Pip before playing.')
            daily_tasks.mark(db,learner,'play')
            return self.store.learner(db,learner),None
        if path=='/api/pip/feed':
            request_id=text_field(data,'requestId',8,100)
            pip_rewards.sync_grants(db,learner,PROFILE_OPTIONS)
            pip_rewards.feed(db,learner,request_id,Problem)
            return self.store.learner(db,learner),None
        if path=='/api/profile':
            name=data.get('avatar')
            if name not in ['orbit','bolt','pixel','leaf','comet','wave',*PROFILE_OPTIONS['companions']]: raise Problem(400,'Choose an available companion.')
            if 'alias' in data:
                alias=suitable(text_field(data,'alias',1,32),'Choose a different Pip name. Names in Stepstone need to suit everyone.')
                existing=db.execute('SELECT alias FROM learners WHERE id=?',(learner,)).fetchone()['alias']
                if len(alias)>12 and alias!=existing:raise Problem(400,'Pip name: 12 characters maximum.')
                db.execute('UPDATE learners SET alias=? WHERE id=?',(alias,learner))
            old=db.execute('SELECT details FROM profiles WHERE learner=?',(learner,)).fetchone()
            details=json.loads(old['details']) if old else {}
            completed=db.execute("SELECT COUNT(DISTINCT unit) FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1",(learner,)).fetchone()[0]
            pip_rewards.sync_grants(db,learner,PROFILE_OPTIONS)
            owned=pip_rewards.inventory(db,learner)
            for field,choice in (('accent','accents'),('motivation','motivations'),('accessory','accessories'),('badge','badges')):
                if field in data:
                    if data[field] not in [item['id'] for item in PROFILE_OPTIONS[choice]]:raise Problem(400,'Choose an available profile option.')
                    option=next(item for item in PROFILE_OPTIONS[choice] if item['id']==data[field])
                    if field=='accessory' and option.get('modules',0)>completed and field+':'+data[field] not in owned and data[field]!=details.get(field):raise Problem(409,'Pass '+str(option['modules'])+' different modules to unlock this item.')
                    details[field]=data[field]
            if 'home' in data:
                home=data['home']
                if not isinstance(home,dict) or set(home)-set(PROFILE_OPTIONS['home']):raise Problem(400,'Choose available home decorations.')
                previous=details.get('home',{})
                room={}
                for field,choices in PROFILE_OPTIONS['home'].items():
                    selected=home.get(field,previous.get(field,choices[0]['id']))
                    option=next((item for item in choices if item['id']==selected),None)
                    if not option:raise Problem(400,'Choose an available decoration.')
                    if option['modules']>completed and 'home.'+field+':'+selected not in owned and selected!=previous.get(field):raise Problem(409,'Pass '+str(option['modules'])+' different modules to unlock this item.')
                    room[field]=selected
                details['home']=room
            if 'homePositions' in data:
                positions=data['homePositions']
                if not isinstance(positions,dict) or set(positions)-{'rug','furniture','decor','painting','shelf'}:raise Problem(400,'Choose valid item positions.')
                for field,point in positions.items():
                    if not isinstance(point,dict) or set(point)!={'x','y'} or any(type(n) not in (int,float) or not math.isfinite(n) or not 0<=n<=1 for n in point.values()):raise Problem(400,'Choose valid item positions.')
                details['homePositions']=positions
            if 'interests' in data:
                interests=data['interests']
                if not isinstance(interests,list) or len(interests)>3 or any(not isinstance(item,str) or item not in [option['id'] for option in PROFILE_OPTIONS['interests']] for item in interests) or len(set(interests))!=len(interests):raise Problem(400,'Choose up to three different interests.')
                details['interests']=interests
            if 'nextWin' in data:details['nextWin']=suitable(text_field(data,'nextWin',0,96),'Reword your next win. Words in Stepstone need to suit everyone.')
            if 'companionName' in data:
                companion_name=suitable(text_field(data,'companionName',1,24),'Choose a different companion name. Names in Stepstone need to suit everyone.')
                if len(companion_name)>12 and companion_name!=details.get('companionName'):raise Problem(400,'Pip name: 12 characters maximum.')
                details['companionName']=companion_name
            if 'introReady' in data:
                if data['introReady'] is not True:raise Problem(400,'Save your profile to continue.')
                details['introReady']=True
            if all(field in details for field in ('accent','motivation','interests','nextWin')):details['ready']=True
            db.execute('INSERT INTO profiles(learner,avatar,details) VALUES(?,?,?) ON CONFLICT(learner) DO UPDATE SET avatar=excluded.avatar,details=excluded.details',(learner,name,pack(details)))
            return self.store.learner(db,learner),None
        if path=='/api/draft':
            unit=data.get('unit');revision=data.get('revision');content=data.get('data')
            if unit not in UNITS or type(revision) is not int or revision<0 or not isinstance(content,dict): raise Problem(400,'Invalid lesson draft.')
            if type(content.get('phase',0)) is not int or not 0<=content.get('phase',0)<=7 or len(pack(content).encode())>160_000: raise Problem(400,'This lesson draft is too large or invalid.')
            valid_ink(content.get('ink',[]))
            old=db.execute('SELECT revision FROM drafts WHERE learner=? AND unit=?',(learner,unit)).fetchone()
            if revision!=(old['revision'] if old else 0): raise Problem(409,'This lesson changed on another device. Choose which draft to keep before saving.')
            revision+=1
            db.execute('INSERT INTO drafts VALUES(?,?,?,?,?) ON CONFLICT(learner,unit) DO UPDATE SET revision=excluded.revision,content=excluded.content,updated=excluded.updated',(learner,unit,revision,pack(content),time.time()))
            return dict(revision=revision),None
        if path=='/api/progress':
            unit=data.get('unit');stage=data.get('stage')
            if unit not in UNITS or type(stage) is not int or not 0<=stage<=5: raise Problem(400,'Unknown lesson step.')
            # This is a resume location, not a passed checkpoint or a source of points.
            db.execute('INSERT INTO progress VALUES(?,?,?,?) ON CONFLICT(learner,unit) DO UPDATE SET stage=excluded.stage,updated=excluded.updated',(learner,unit,stage,time.time()))
            return dict(ok=True),None
        if path=='/api/attempt':
            unit=data.get('unit')
            if unit not in BANK: raise Problem(400,'This module is not ready yet.')
            course_access.require_course(db,learner,UNITS[unit],CATALOG,Problem)
            opened=db.execute('SELECT * FROM attempts WHERE learner=? AND unit=? AND finished IS NULL ORDER BY started DESC LIMIT 1',(learner,unit)).fetchone()
            if opened: return dict(id=opened['id'],unit=unit,questions=[public_question(q) for q in json.loads(opened['questions'])]),None
            self.store.require_tutorial(db,learner)
            rng=random.SystemRandom()
            questions=sample_check(BANK[unit],UNITS[unit].get('checkSkills',('calculate','apply','reason')),rng)
            for q in questions:
                if q['kind']=='choice':
                    # Label options by shuffled position; authored ids would reveal the answer order.
                    shuffled=rng.sample(q['options'],len(q['options']))
                    q['answer']=str(next(i for i,o in enumerate(shuffled) if o['id']==q['answer']))
                    q['options']=[dict(o,id=str(i)) for i,o in enumerate(shuffled)]
            rng.shuffle(questions);attempt=uid()
            db.execute('INSERT INTO attempts(id,learner,unit,questions,started) VALUES(?,?,?,?,?)',(attempt,learner,unit,pack(questions),time.time()))
            return dict(id=attempt,unit=unit,questions=[public_question(q) for q in questions]),None
        if path=='/api/submit':
            attempt=db.execute('SELECT * FROM attempts WHERE id=? AND learner=?',(text_field(data,'id',1,100),learner)).fetchone()
            if not attempt: raise Problem(404,'This check does not belong to this account.')
            if attempt['finished']: return dict(report=json.loads(attempt['report']),me=self.store.learner(db,learner)),None
            course_access.require_course(db,learner,UNITS[attempt['unit']],CATALOG,Problem)
            if attempt['unit']=='app-build' and not projects.ready(projects.get(db,learner)):
                raise Problem(400,'Save a working app, complete its four guided tests and explain it before finishing this check.')
            typing_practice=validate_typing(data.get('typingPractice'),UNITS[attempt['unit']],Problem)
            answers=data.get('answers');questions=json.loads(attempt['questions'])
            if not isinstance(answers,dict) or set(answers)!={q['id'] for q in questions}: raise Problem(400,'Please answer all six questions.')
            for q in questions:
                answer=answers[q['id']]
                if not isinstance(answer,str) or not 0<len(answer.strip())<=120: raise Problem(400,'Please answer all six questions.')
                if q['kind']=='choice' and answer not in [o['id'] for o in q['options']]: raise Problem(400,'Choose an available answer.')
                if q['kind']=='number' and numeric(answer) is None: raise Problem(400,'Enter a number or a fraction for each number question.')
            reflection=text_field(data,'reflection',1,2000);support=data.get('support')
            if support not in ('myself','person','tool','mixed'): raise Problem(400,'Please choose what support you used.')
            ink=valid_ink(data.get('ink',[]));now=time.time()
            details=[public_question(q)|dict(answer=answers[q['id']],expected=q['answer'],correct=correct(q,answers[q['id']]),explanation=q['explanation']) for q in questions]
            score=sum(q['correct'] for q in details);passed=score>=5
            prior=[json.loads(x[0]) for x in db.execute('SELECT report FROM attempts WHERE learner=? AND unit=? AND finished IS NOT NULL',(learner,attempt['unit']))]
            earned=0
            def award(key,amount,label):
                nonlocal earned
                cursor=db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)',(key,learner,amount,label,now))
                if cursor.rowcount: earned+=amount
            award('first-check-'+learner+'-'+attempt['unit'],5,'First completed check')
            if passed: award('first-pass-'+learner+'-'+attempt['unit'],15,'Skill checkpoint passed')
            previous_passes=[r['at'] for r in prior if r['passed']]
            review=passed and bool(previous_passes) and now-max(previous_passes)>=WEEK
            if review: award('review-'+attempt['id'],5,'Remembered after a week')
            food_award=pip_rewards.award_review(db,learner,attempt['id'],attempt['unit'],
                UNITS[attempt['unit']].get('foodReplay',False),bool(previous_passes),passed,now)
            report=dict(typingPractice=typing_practice,unit=attempt['unit'],title=UNITS[attempt['unit']]['title'],score=score,total=6,passed=passed,questions=details,reflection=reflection,support=support,ink=ink,at=now,points=earned,review=review,tryNumber=len(prior)+1,practiceRetries=min(999,max(0,data.get('practiceRetries',0))) if type(data.get('practiceRetries',0)) is int else 0)
            report.update(food_award)
            db.execute('UPDATE attempts SET finished=?,report=? WHERE id=?',(now,pack(report),attempt['id']))
            if passed:daily_tasks.mark(db,learner,'module',now)
            return dict(report=report,me=self.store.learner(db,learner)),None
        if path=='/api/reward':
            # Per-account request limit: siblings sharing a device/network are
            # not penalized. The transaction makes retries and reservations safe.
            now=time.time();key=('rewards',learner)
            visits=self.server.logins.setdefault(key,[])
            visits[:]=[at for at in visits if now-at<60]
            if len(visits)>=30: raise Problem(429,'Several reward requests arrived together. Wait a minute, then refresh. Your points and work are saved.')
            visits.append(now)
            if text_field(data,'id',1,100) in MILESTONES:
                result=self.store.funded.request(db,learner,data,self.store)
                return result|dict(me=self.store.learner(db,learner)),None
            reward=db.execute('SELECT * FROM rewards WHERE id=? AND active=1',(text_field(data,'id',1,100),)).fetchone()
            if not reward: raise Problem(404,'Reward not found.')
            own=db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
            if own and own['value']==learner and reward['kind']=='mentor': raise Problem(400,'Agreed learner rewards belong to the learners you support.')
            existing=db.execute('SELECT * FROM claims WHERE learner=? AND reward=?',(learner,reward['id'])).fetchone()
            if existing: return dict(me=self.store.learner(db,learner)),None
            if reward['kind']!='theme':self.store.require_tutorial(db,learner)
            if reward['stock'] is not None:
                committed=db.execute("SELECT COUNT(*) FROM claims WHERE reward=? AND status IN ('pending','approved','given')",(reward['id'],)).fetchone()[0]
                if committed>=reward['stock']: raise Problem(409,'No secured rewards are available right now. Your points are unchanged.')
            mastered={r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND json_extract(report,'$.passed')=1",(learner,))}
            required=json.loads(reward['required_modules'])
            if len(mastered)<reward['minimum_modules'] or any(u not in mastered for u in required): raise Problem(409,'Complete the agreed modules before requesting this reward.')
            if self.store.points(db,learner)<reward['cost']: raise Problem(409,'You need a few more points for this reward.')
            claim=uid();state='given' if reward['kind']=='theme' else 'pending';now=time.time()
            db.execute('INSERT INTO claims(id,learner,reward,status,cost,created) VALUES(?,?,?,?,?,?)',(claim,learner,reward['id'],state,reward['cost'],now))
            db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',('claim-'+claim,learner,-reward['cost'],'Reward: '+reward['title'],now))
            return dict(me=self.store.learner(db,learner)),None
        raise Problem(404,'Not found.')

    def reward_recovery_boundary(self,db):
        if db.execute("SELECT 1 FROM settings WHERE key='recoveryHold'").fetchone():
            raise Problem(409,'Reward requests are paused while your mentor checks restored records. Your learning still works.')

class StepstoneServer(ThreadingHTTPServer):
    def service_actions(self):
        for store in tuple(self.accounts.stores):
            try:store.backups.tick()
            except Exception:store.backups.error='Automatic recovery copies stopped. Check host storage.'
        if self.runtime.due():
            self.runtime.stopping=True
            threading.Thread(target=self.shutdown,daemon=True).start()
    def server_close(self):
        if hasattr(self,'voice'): self.voice.close()
        if hasattr(self,'accounts'):
            for store in self.accounts.stores:store.backups.close()
        super().server_close()
    # Windows SO_REUSEADDR can allow two listeners to take the same port. An
    # exclusive listener makes an accidental second launch fail clearly.
    allow_reuse_address=os.name!='nt'
    def server_bind(self):
        if os.name=='nt': self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
        super().server_bind()

def create_server(host='127.0.0.1',port=8090,data=None,allowed_host=None,secure=False,desktop=False,public_url='',trust_forwarded=False):
    public_url=shared_address(public_url,secure)
    server=StepstoneServer((host,port),Handler)
    actual=server.server_address[1]
    server.store=Store(data or ROOT/'data');server.secure_cookies=secure;server.logins={};server.voice=VoiceEngine()
    server.trust_forwarded=trust_forwarded
    server.accounts=mentor_accounts.Accounts(server.store,Store,Problem,automatic_backups=desktop or bool(public_url))
    server.backups=server.store.backups
    with server.store.db() as db:
        saved=db.execute("SELECT value FROM settings WHERE key='keepRunning'").fetchone()
    server.runtime=HostRuntime(desktop=desktop,keep_running=not saved or saved['value']!='false')
    server.public_url=public_url
    server.local_hosts={f'localhost:{actual}',f'127.0.0.1:{actual}'}
    server.allowed_hosts=set(server.local_hosts)
    if allowed_host: server.allowed_hosts.update(h.lower() for h in allowed_host)
    if public_url: server.allowed_hosts.add(urlparse(public_url).netloc)
    return server

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',default='127.0.0.1');parser.add_argument('--port',type=int,default=8090)
    parser.add_argument('--data');parser.add_argument('--allow-host',action='append',default=[])
    parser.add_argument('--secure-cookies',action='store_true');parser.add_argument('--open',action='store_true')
    parser.add_argument('--desktop',action='store_true',help='Allow local mentor background controls')
    parser.add_argument('--public-url',default='',help='Already deployed HTTPS address, with --secure-cookies')
    args=parser.parse_args()
    app=create_server(args.host,args.port,args.data,args.allow_host,args.secure_cookies,args.desktop,args.public_url)
    url=f'http://localhost:{app.server_address[1]}'
    print('Stepstone ready: '+url,flush=True)
    if args.open: webbrowser.open(url)
    try: app.serve_forever()
    except KeyboardInterrupt: pass
    finally: app.server_close()
