"""Independent mentor workspaces and explicitly approved browser devices."""
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from backups import BackupManager
from text_filter import acceptable

DEVICE_LIFETIME = 365 * 86400
UNKNOWN = dict(salt='00' * 16, hash='00' * 64)
REQUEST_LIFETIME = 900


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def password_record(password):
    salt = secrets.token_hex(16)
    return dict(salt=salt, hash=hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex())


def matches(password, record):
    got = hashlib.scrypt(password.encode(), salt=bytes.fromhex(record['salt']), n=16384, r=8, p=1).hex()
    return hmac.compare_digest(got, record['hash'])


def install(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS mentor_devices (
      id TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, label TEXT NOT NULL,
      created REAL NOT NULL, expires REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS mentor_device_requests (
      id TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, label TEXT NOT NULL,
      code TEXT NOT NULL, created REAL NOT NULL, expires REAL NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending');
    ''')


class Accounts:
    def __init__(self, root_store, store_class, problem, automatic_backups=False):
        self.root = root_store
        self.Store = store_class
        self.Problem = problem
        self.lock = threading.RLock()
        self.by_name = {}
        self.by_id = {}
        self.stores = [root_store]
        self.automatic_backups = automatic_backups
        folder = root_store.directory / 'workspaces'
        for path in folder.glob('*/stepstone.sqlite3'):
            if re.fullmatch(r'[a-f0-9]{16}', path.parent.name):
                self.stores.append(store_class(path.parent))
        for store in self.stores:
            with store.db() as db:
                row = db.execute("SELECT value FROM settings WHERE key='mentorAccount'").fetchone()
            store.account = json.loads(row['value']) if row else None
            store.identity = store.account['id'] if store.account else 'root'
            store.backups = BackupManager(store.path, enabled=automatic_backups)
            if store.account:
                if store.identity in self.by_id or store.account['username'] in self.by_name:
                    raise ValueError('Duplicate mentor workspace identity. Restore into a separate installation.')
                self.by_id[store.identity] = store
                self.by_name[store.account['username']] = store

    def field(self, data, name, minimum=1, maximum=100, *, moderate=True):
        value = data.get(name, '')
        if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
            raise self.Problem(400, f'Please check {name.replace("_", " ")} ({minimum}–{maximum} characters).')
        # Account, username and device names stay PG-16 like learner names.
        if moderate and name in ('name', 'username', 'device') and not acceptable(value):
            raise self.Problem(400, f'Choose a different {"device name" if name == "device" else name}. Names in Stepstone need to suit everyone.')
        return value.strip()

    def lookup(self, data):
        username = self.field(data, 'username', 3, 32, moderate=False).lower()
        store = self.by_name.get(username)
        if not store:
            # Spend the same passphrase work, so response time does not reveal which usernames exist.
            matches(str(data.get('passphrase', ''))[:200], UNKNOWN)
            raise self.Problem(401, 'The account details did not match.')
        return store

    def from_token(self, token):
        if '.' not in token:
            return self.root
        parts = token.split('.')
        if len(parts) != 2 or not re.fullmatch(r'w(?:root|[a-f0-9]{16})', parts[0]) or not re.fullmatch(r'[A-Za-z0-9_-]{16,80}', parts[1]):
            raise self.Problem(401, 'This access link or sign-in is not valid.')
        store = self.by_id.get(parts[0][1:])
        if not store:
            raise self.Problem(401, 'This account is not available on this installation.')
        return store

    def choose(self, handler, path, data=None):
        data = data or {}
        if path in ('/api/mentor/login', '/api/mentor/recover'):
            # Failures count per address and username, so one person's mistakes cannot lock out other mentors.
            handler.sign_in_key = (handler.client_key(), 'mentor', str(data.get('username', '')).strip().lower()[:32])
            handler.throttle(handler.sign_in_key)
            try:
                return self.lookup(data)
            except self.Problem:
                handler.count_attempt(handler.sign_in_key)
                raise
        if path == '/api/mentor/device-status':
            return self.from_token(handler.token('mentor_pending'))
        if path in ('/api/join', '/api/login'):
            return self.from_token(data.get('code', '') if isinstance(data.get('code'), str) else '')
        role = data.get('role') if path == '/api/logout' else 'mentor' if path.startswith('/api/mentor') else 'learner'
        return self.from_token(handler.token(role))

    def setup(self, handler, data):
        key = (handler.client_key(), 'mentor-register')
        handler.throttle(key)
        handler.count_attempt(key)  # Every registration counts, which limits new workspaces per address.
        name = self.field(data, 'name', 1, 50)
        username = self.field(data, 'username', 3, 32).lower()
        if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{2,31}', username):
            raise self.Problem(400, 'Use 3–32 letters, numbers, dots, underscores or dashes for your username.')
        password = self.field(data, 'passphrase', 12, 200)
        label = self.field(data, 'device', 1, 60)
        claim = data.get('claimExisting') is True
        with self.lock:
            if username in self.by_name:
                raise self.Problem(409, 'That username is already in use. Choose another, or sign in.')
            if claim and (not handler.local_owner_request() or self.root.account):
                raise self.Problem(403, 'Existing records can only be claimed once, from this installation’s host.')
            store = self.root if claim else self.Store(self.root.directory / 'workspaces' / secrets.token_hex(8))
            identity = 'root' if claim else store.directory.name
            account = dict(id=identity, username=username, name=name, hostOwner=claim)
            recovery = secrets.token_urlsafe(32)
            with store.db() as db:
                old = db.execute("SELECT value FROM settings WHERE key='mentor'").fetchone()
                if claim and old and not matches(data.get('previousPassphrase', ''), json.loads(old['value'])):
                    raise self.Problem(401, 'Enter the previous mentor passphrase to keep these existing records.')
                db.execute("INSERT OR REPLACE INTO settings VALUES('mentor',?)", (json.dumps(password_record(password)),))
                db.execute("INSERT INTO settings VALUES('mentorAccount',?)", (json.dumps(account),))
                db.execute("INSERT OR REPLACE INTO settings VALUES('mentorRecovery',?)", (digest(recovery),))
                db.execute("DELETE FROM sessions WHERE role='mentor'")
                store.identity = identity
                token = self.device(store, db, label)
            store.account = account
            self.by_id[identity] = store
            self.by_name[username] = store
            if store not in self.stores:
                store.backups = BackupManager(store.path, enabled=self.automatic_backups)
                self.stores.append(store)
            handler._store = store
        return dict(ok=True, account=account, recovery=recovery), [handler.cookie('mentor',token,DEVICE_LIFETIME),handler.cookie('learner','',0)]

    def device(self, store, db, label):
        token = store.access_code()
        db.execute('INSERT INTO mentor_devices VALUES(?,?,?,?,?)', (secrets.token_hex(12), digest(token), label, time.time(), time.time()+DEVICE_LIFETIME))
        return token

    def owner(self, handler, db):
        row = db.execute('SELECT id FROM mentor_devices WHERE token=? AND expires>?', (digest(handler.token('mentor')), time.time())).fetchone()
        if not row or not handler.store.account:
            raise self.Problem(401, 'Sign in with your mentor account on an approved device.')
        return row['id']

    def overview(self, handler, db):
        current = self.owner(handler, db)
        now = time.time()
        return dict(account=handler.store.account,
                    devices=[dict(r) | dict(current=r['id']==current) for r in db.execute('SELECT id,label,created,expires FROM mentor_devices WHERE expires>? ORDER BY created', (now,))],
                    requests=[dict(r) for r in db.execute("SELECT id,label,code,created,expires FROM mentor_device_requests WHERE status='pending' AND expires>? ORDER BY created DESC", (now,))])

    def post(self, handler, db, path, data):
        store = handler.store
        if path == '/api/mentor/login':
            password = self.field(data, 'passphrase', 12, 200)
            saved = db.execute("SELECT value FROM settings WHERE key='mentor'").fetchone()
            if not saved or not matches(password, json.loads(saved['value'])):
                handler.count_attempt(handler.sign_in_key)
                raise self.Problem(401, 'The account details did not match.')
            handler.server.logins.pop(handler.sign_in_key, None)
            existing = db.execute('SELECT id FROM mentor_devices WHERE token=? AND expires>?', (digest(handler.token('mentor')), time.time())).fetchone()
            if existing:
                return dict(ok=True), handler.cookie('learner','',0)
            label = self.field(data, 'device', 1, 60)
            secret = store.access_code()
            rid = secrets.token_hex(12)
            code = str(secrets.randbelow(900000)+100000)
            db.execute('DELETE FROM mentor_device_requests WHERE expires<?', (time.time(),))
            db.execute('INSERT INTO mentor_device_requests(id,token,label,code,created,expires) VALUES(?,?,?,?,?,?)', (rid,digest(secret),label,code,time.time(),time.time()+REQUEST_LIFETIME))
            return dict(pending=True, code=code, device=label), handler.cookie('mentor_pending', secret, REQUEST_LIFETIME)
        if path == '/api/mentor/device-status':
            request = db.execute('SELECT * FROM mentor_device_requests WHERE token=? AND expires>?', (digest(handler.token('mentor_pending')),time.time())).fetchone()
            if not request:
                raise self.Problem(401, 'This device request expired. Sign in to request approval again.')
            if request['status']=='denied':
                raise self.Problem(403, 'This device request was declined.')
            if request['status']!='approved':
                return dict(pending=True,code=request['code'],device=request['label']),None
            token = self.device(store,db,request['label'])
            db.execute('DELETE FROM mentor_device_requests WHERE id=?',(request['id'],))
            return dict(ok=True),[handler.cookie('mentor',token,DEVICE_LIFETIME),handler.cookie('mentor_pending','',0),handler.cookie('learner','',0)]
        if path == '/api/mentor/recover':
            recovery = self.field(data,'recovery',20,100)
            saved = db.execute("SELECT value FROM settings WHERE key='mentorRecovery'").fetchone()
            if not saved or not hmac.compare_digest(saved['value'],digest(recovery)):
                handler.count_attempt(handler.sign_in_key)
                raise self.Problem(401,'The recovery details did not match.')
            handler.server.logins.pop(handler.sign_in_key, None)
            password = self.field(data,'passphrase',12,200)
            label = self.field(data,'device',1,60)
            db.execute('DELETE FROM mentor_devices')
            db.execute('DELETE FROM mentor_device_requests')
            replacement = secrets.token_urlsafe(32)
            db.execute("UPDATE settings SET value=? WHERE key='mentor'",(json.dumps(password_record(password)),))
            db.execute("UPDATE settings SET value=? WHERE key='mentorRecovery'",(digest(replacement),))
            token = self.device(store,db,label)
            return dict(ok=True,recovery=replacement),[handler.cookie('mentor',token,DEVICE_LIFETIME),handler.cookie('learner','',0)]
        if path in ('/api/mentor/device-review','/api/mentor/device-revoke'):
            current = self.owner(handler,db)
            target = self.field(data,'id',1,100)
            if path.endswith('device-revoke'):
                if target==current:
                    raise self.Problem(400,'Use Sign out to remove access from this browser.')
                db.execute('DELETE FROM mentor_devices WHERE id=?',(target,))
            else:
                status = data.get('status')
                if status not in ('approved','denied'):
                    raise self.Problem(400,'Choose approve or decline.')
                row=db.execute("SELECT id FROM mentor_device_requests WHERE id=? AND expires>? AND status='pending'",(target,time.time())).fetchone()
                if not row:
                    raise self.Problem(409,'That device request has expired or was already handled.')
                db.execute('UPDATE mentor_device_requests SET status=? WHERE id=?',(status,target))
            return dict(ok=True),None
        return None
