"""Funded milestones. All methods run inside the Store's write transaction.

Cash is recorded when received/spent. Physical stock is reserved by person, not
by browser/account. Giving an already purchased item never spends cash twice.
"""
import hashlib
import json
import secrets
import time

from foundation import assigned_progress


class RewardError(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


def fail(message, status=409):
    raise RewardError(status, message)


def uid():
    return secrets.token_urlsafe(18)


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def text(data, key, minimum=1, maximum=500):
    value = data.get(key)
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        fail('Please check ' + key.replace('_', ' ') + '.', 400)
    return value.strip()


def integer(data, key, minimum, maximum):
    value = data.get(key)
    if type(value) is not int or not minimum <= value <= maximum:
        fail('Please check ' + key.replace('_', ' ') + '.', 400)
    return value


PROGRAM = (
    ('core-card-everyday', 'everyday', 'Everyday decisions · CAD5 card'),
    ('core-card-life', 'life', 'Important life tasks · CAD5 card'),
    ('core-card-work-home', 'work-home', 'Work, travel & home · CAD5 card'),
    ('core-card-technology', 'technology', 'Technology · CAD5 card'),
    ('core-laptop', None, 'My own learning laptop'),
)
MILESTONES = {key: (group, title) for key, group, title in PROGRAM}
LAPTOP_DEMO = ('file', 'message', 'budget', 'scam', 'ai')


class RewardProgram:
    def __init__(self, foundation, laptop_units=None):
        self.foundation = foundation
        self.laptop_units = tuple(laptop_units or ())

    def install(self, db):
        db.executescript('''
        CREATE TABLE IF NOT EXISTS reward_people (
          id TEXT PRIMARY KEY, primary_learner TEXT UNIQUE NOT NULL, created REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS reward_accounts (
          learner TEXT PRIMARY KEY, person TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS reward_stock (
          id TEXT PRIMARY KEY, category TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>=0),
          unit_cents INTEGER NOT NULL CHECK(unit_cents>=0), source TEXT NOT NULL,
          note TEXT NOT NULL, created REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS reward_funding (
          id TEXT PRIMARY KEY, kind TEXT NOT NULL, cents INTEGER NOT NULL,
          batch TEXT, quantity INTEGER NOT NULL, note TEXT NOT NULL, created REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS reward_allocations (
          id TEXT PRIMARY KEY, person TEXT NOT NULL, milestone TEXT NOT NULL,
          batch TEXT NOT NULL, state TEXT NOT NULL, created REAL NOT NULL);
        CREATE UNIQUE INDEX IF NOT EXISTS reward_one_entitlement
          ON reward_allocations(person,milestone) WHERE state!='released';
        CREATE TABLE IF NOT EXISTS funded_claims (
          id TEXT PRIMARY KEY, allocation TEXT UNIQUE NOT NULL, learner TEXT NOT NULL,
          reward TEXT NOT NULL, status TEXT NOT NULL, cost INTEGER NOT NULL,
          created REAL NOT NULL, note TEXT NOT NULL DEFAULT '', demonstrated INTEGER NOT NULL DEFAULT 0,
          revision INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS reward_audit (
          id INTEGER PRIMARY KEY AUTOINCREMENT, created REAL NOT NULL,
          actor TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS reward_commands (
          id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, result TEXT NOT NULL);
        ''')
        # Old purchases remain in history; one refund per old theme claim.
        for claim in db.execute("SELECT c.* FROM claims c JOIN rewards r ON c.reward=r.id WHERE r.kind='theme' AND c.status='given' AND c.cost>0").fetchall():
            result = db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)',
                                ('refund-free-colours-' + claim['id'], claim['learner'], claim['cost'],
                                 'Colour choices are now free: original points returned', time.time()))
            if result.rowcount:
                self.audit(db, 'migration', 'free-colours', dict(claim=claim['id'], points=claim['cost']))
        db.execute("UPDATE rewards SET cost=0,minimum_modules=0,required_modules='[]',stock=NULL,description='Free colour choice. Choose it in My profile.' WHERE kind='theme'")

    def audit(self, db, actor, action, details):
        db.execute('INSERT INTO reward_audit(created,actor,action,details) VALUES(?,?,?,?)',
                   (time.time(), actor, action, packed(details)))

    def command(self, db, action, data, run):
        key = text(data, 'key', 8, 100)
        fingerprint = hashlib.sha256(packed(dict(action=action, data=data)).encode()).hexdigest()
        previous = db.execute('SELECT * FROM reward_commands WHERE id=?', (key,)).fetchone()
        if previous:
            if previous['fingerprint'] != fingerprint:
                fail('This save key was already used for a different change. Refresh and try again.')
            return json.loads(previous['result'])
        result = run()
        db.execute('INSERT INTO reward_commands VALUES(?,?,?)', (key, fingerprint, packed(result)))
        return result

    def person(self, db, learner):
        row = db.execute('SELECT p.* FROM reward_accounts a JOIN reward_people p ON a.person=p.id WHERE a.learner=?', (learner,)).fetchone()
        return dict(row) if row else None

    def require_learner(self, db, learner):
        own = db.execute("SELECT value FROM settings WHERE key='mentorLearner'").fetchone()
        if own and own['value'] == learner:
            fail('My learning is separate from funded learner places.', 400)
        if not db.execute('SELECT 1 FROM learners WHERE id=?', (learner,)).fetchone():
            fail('Learner not found.', 404)

    def cash(self, db):
        from ai_support import held
        from gift_cards import held as card_held
        return db.execute('SELECT COALESCE(SUM(cents),0) FROM reward_funding').fetchone()[0] - held(db) - card_held(db)

    def stock(self, db):
        rows = []
        for row in db.execute('SELECT * FROM reward_stock ORDER BY created,id'):
            item = dict(row)
            counts = dict(db.execute('SELECT state,COUNT(*) FROM reward_allocations WHERE batch=? GROUP BY state', (row['id'],)))
            item['given'] = counts.get('given', 0)
            item['reserved'] = sum(counts.get(s, 0) for s in ('allocated', 'pending', 'approved'))
            item['available'] = item['quantity'] - item['given'] - item['reserved']
            rows.append(item)
        return rows

    def claims(self, db, learner=None):
        rows = []
        for row in db.execute('SELECT c.*,l.alias,a.person,a.batch FROM funded_claims c JOIN learners l ON c.learner=l.id JOIN reward_allocations a ON c.allocation=a.id WHERE (? IS NULL OR c.learner=?) ORDER BY c.created DESC', (learner, learner)):
            item = dict(row)
            item.update(title=MILESTONES[row['reward']][1], kind='mentor', category='laptop' if row['reward']=='core-laptop' else 'giftcard', funded=True)
            rows.append(item)
        return rows

    def requirements(self, db, learner, milestone):
        if milestone == 'core-laptop' and self.laptop_units:
            return list(self.laptop_units), 105
        plan = assigned_progress(db, learner, self.foundation, [])
        group = MILESTONES[milestone][0]
        groups = [g for g in plan['groups'] if group is None or g['id'] == group]
        units = [unit for g in groups for unit in g['units']]
        if not units:
            fail('This saved learning path needs a mentor review before a reward can be assigned.')
        return units, plan['version']

    def rewards(self, db, learner=None):
        person = self.person(db, learner) if learner else None
        primary = bool(person and person['primary_learner'] == learner)
        rows = []
        for key, group, title in PROGRAM:
            allocation = db.execute("SELECT * FROM reward_allocations WHERE person=? AND milestone=? AND state!='released'", (person['id'], key)).fetchone() if person else None
            claim = db.execute('SELECT * FROM funded_claims WHERE allocation=?', (allocation['id'],)).fetchone() if allocation else None
            required, version = self.requirements(db, learner, key) if learner else ([], None)
            rows.append(dict(id=key, milestone=key, title=title, kind='mentor', active=1,
                             category='giftcard' if group else 'laptop', cost=60 if group else 0,
                             description='Finish this part of your path, then choose a CAD5 card with your mentor.' if group else 'Finish all 24 modules in each of the first four courses: Money & math, Reading & writing, Science and Life skills. Then ask your mentor for a new starter laptop and charger, when funded. Digital skills and Work & jobs unlock at the same milestone. There is no point cost.',
                             required_modules=required, minimum_modules=0, path_version=version,
                             available=int(primary and allocation is not None and allocation['state']=='allocated'),
                             stock=None, confirmed=primary, linked=bool(person and not primary),
                             allocation=allocation['id'] if primary and allocation else None,
                             allocation_state=allocation['state'] if allocation else None,
                             claim_id=claim['id'] if claim and primary else None))
        return rows

    def summary(self, db):
        stock = self.stock(db)
        allocations = [dict(r) for r in db.execute('SELECT a.*,p.primary_learner,l.alias,s.unit_cents FROM reward_allocations a JOIN reward_people p ON a.person=p.id JOIN learners l ON p.primary_learner=l.id JOIN reward_stock s ON a.batch=s.id ORDER BY a.created DESC')]
        people = [dict(r) for r in db.execute('SELECT a.learner,a.person,p.primary_learner FROM reward_accounts a JOIN reward_people p ON a.person=p.id')]
        funding = [dict(r) for r in db.execute('SELECT * FROM reward_funding ORDER BY created DESC,id')]
        from ai_support import held
        return dict(cash_cents=self.cash(db),ai_held_cents=held(db), stock=stock, allocations=allocations, people=people,
                    entries=funding, audit=[dict(r)|dict(details=json.loads(r['details'])) for r in db.execute('SELECT * FROM reward_audit ORDER BY id DESC LIMIT 150')],
                    totals=dict(received_cents=sum(max(0,e['cents']) for e in funding), spent_cents=-sum(min(0,e['cents']) for e in funding),
                                cards_available=sum(s['available'] for s in stock if s['category']=='giftcard'),
                                laptops_available=sum(s['available'] for s in stock if s['category']=='laptop'),
                                reserved=sum(s['reserved'] for s in stock), given=sum(s['given'] for s in stock)))

    def mentor(self, db, action, data):
        return self.command(db, action, data, lambda: self._mentor(db, action, data))

    def _mentor(self, db, action, data):
        if action == 'person':
            learner = text(data, 'learner')
            self.require_learner(db, learner)
            note = text(data, 'note', 3, 300)
            if data.get('confirmed') is not True:
                fail('Confirm you checked who this learner is and whether they already have an account.', 400)
            person = self.person(db, learner)
            target = text(data, 'same_person_as', 0, 100) if 'same_person_as' in data else ''
            if target == 'separate':
                if not person or person['primary_learner'] == learner:
                    fail('Only a linked extra account can be separated.', 400)
                person = dict(id=uid(), primary_learner=learner)
                db.execute('INSERT INTO reward_people VALUES(?,?,?)', (person['id'], learner, time.time()))
                db.execute('UPDATE reward_accounts SET person=? WHERE learner=?', (person['id'], learner))
                self.audit(db, 'mentor', 'separate-person', dict(learner=learner, person=person['id'], reason=note))
                return dict(ok=True, person=person['id'])
            if target:
                self.require_learner(db, target)
                other = self.person(db, target)
                if not other: fail('Confirm the account you want to keep first.')
                if person and person['id'] != other['id']:
                    from gift_cards import committed
                    if committed(db, person['id']):
                        fail('This account has reserved or delivered gift cards. Release unused funding first. Keep a main account with delivered rewards so its lifetime cap stays attached.')
                    if db.execute("SELECT 1 FROM ai_months WHERE person=? AND status!='released'",(person['id'],)).fetchone():
                        fail('This account has a reserved or used AI month. Keep that main account; release unused funding before linking.')
                    db.execute('UPDATE ai_months SET person=? WHERE person=?',(other['id'],person['id']))
                    if db.execute("SELECT 1 FROM reward_allocations WHERE person=? AND state!='released'", (person['id'],)).fetchone():
                        fail('Release this account’s unused places and cancel any open requests first. If rewards were already given, keep the records and review them before linking.')
                    db.execute('UPDATE reward_allocations SET person=? WHERE person=?', (other['id'], person['id']))
                    db.execute('UPDATE reward_accounts SET person=? WHERE person=?', (other['id'], person['id']))
                    db.execute('DELETE FROM reward_people WHERE id=?', (person['id'],))
                db.execute('INSERT INTO reward_accounts VALUES(?,?) ON CONFLICT(learner) DO UPDATE SET person=excluded.person', (learner, other['id']))
                person = other
            elif not person:
                person = dict(id=uid(), primary_learner=learner)
                db.execute('INSERT INTO reward_people VALUES(?,?,?)', (person['id'], learner, time.time()))
                db.execute('INSERT INTO reward_accounts VALUES(?,?)', (learner, person['id']))
            self.audit(db, 'mentor', 'confirm-person', dict(learner=learner, person=person['id'], primary=person['primary_learner'], reason=note))
            return dict(ok=True, person=person['id'])

        if action == 'funding':
            kind = data.get('kind')
            if kind not in ('received', 'expense', 'buy-cards', 'donate-cards', 'buy-laptop', 'donate-laptop'):
                fail('Choose a funding record type.', 400)
            note = text(data, 'note', 3, 300)
            batch = None
            quantity, cents = 0, 0
            if kind in ('received', 'expense'):
                cents = integer(data, 'cents', 1, 10000000) * (1 if kind=='received' else -1)
            else:
                category = 'giftcard' if kind.endswith('cards') else 'laptop'
                quantity = integer(data, 'quantity', 1, 1000) if category=='giftcard' else 1
                unit_cents = 500 if category=='giftcard' else integer(data, 'cents', 1, 10000000) if kind=='buy-laptop' else 0
                cents = -quantity*unit_cents if kind.startswith('buy-') else 0
                batch = uid()
                db.execute('INSERT INTO reward_stock VALUES(?,?,?,?,?,?,?)', (batch, category, quantity, unit_cents, kind, note, time.time()))
            if self.cash(db) + cents < 0:
                fail('There is not enough recorded cash. Record money actually received before a purchase or expense.')
            fid = uid()
            db.execute('INSERT INTO reward_funding VALUES(?,?,?,?,?,?,?)', (fid, kind, cents, batch, quantity, note, time.time()))
            self.audit(db, 'mentor', kind, dict(entry=fid, batch=batch, cash_cents=cents, quantity=quantity, reason=note))
            return dict(ok=True, id=fid)

        if action == 'stock-remove':
            batch = next((s for s in self.stock(db) if s['id']==data.get('batch')), None)
            if not batch: fail('Stock record not found.', 404)
            quantity = integer(data, 'quantity', 1, 1000)
            if integer(data, 'expected_quantity', 0, 1000000) != batch['quantity']:
                fail('This stock changed. Refresh before changing it.')
            if quantity > batch['available']:
                fail('You cannot remove stock that is reserved or already given.')
            note = text(data, 'note', 3, 300)
            db.execute('UPDATE reward_stock SET quantity=quantity-? WHERE id=?', (quantity,batch['id']))
            db.execute('INSERT INTO reward_funding VALUES(?,?,?,?,?,?,?)', (uid(),'stock-removed',0,batch['id'],-quantity,note,time.time()))
            self.audit(db, 'mentor', action, dict(batch=batch['id'], quantity=-quantity, cash_cents=0, reason=note))
            return dict(ok=True)

        if action == 'allocate':
            learner = text(data, 'learner')
            self.require_learner(db, learner)
            person = self.person(db, learner)
            if not person or person['primary_learner'] != learner:
                fail('Confirm this learner’s main account before setting aside rewards.')
            kind = data.get('kind')
            if kind not in ('cards','laptop'): fail('Choose the four-card place or a laptop.', 400)
            milestones = [p[0] for p in PROGRAM if bool(p[1]) == (kind=='cards')]
            needed = [key for key in milestones if not db.execute("SELECT 1 FROM reward_allocations WHERE person=? AND milestone=? AND state!='released'", (person['id'],key)).fetchone()]
            stock = [s for s in self.stock(db) if s['category']==('giftcard' if kind=='cards' else 'laptop')]
            if sum(s['available'] for s in stock)<len(needed):
                fail('Not enough unassigned stock. A new card place needs all four CAD5 cards secured first.' if kind=='cards' else 'Record a purchased or donated laptop first.')
            for key in needed:
                self.requirements(db, learner, key)
                batch = next(s for s in stock if s['available']>0)
                batch['available'] -= 1
                aid = uid()
                db.execute('INSERT INTO reward_allocations VALUES(?,?,?,?,?,?)', (aid,person['id'],key,batch['id'],'allocated',time.time()))
                self.audit(db,'mentor','allocate',dict(allocation=aid,person=person['id'],learner=learner,milestone=key,batch=batch['id'],cents=batch['unit_cents'],from_state=None,to_state='allocated'))
            return dict(ok=True, allocated=len(needed))

        if action == 'release':
            row = db.execute('SELECT * FROM reward_allocations WHERE id=?', (text(data,'id'),)).fetchone()
            if not row: fail('Allocation not found.',404)
            if row['state']!='allocated': fail('Only an unused place can be released. Review an open request in Reward requests.')
            reason=text(data,'note',3,300)
            db.execute("UPDATE reward_allocations SET state='released' WHERE id=?", (row['id'],))
            self.audit(db,'mentor','release',dict(allocation=row['id'],milestone=row['milestone'],reason=reason,from_state='allocated',to_state='released',points=0))
            return dict(ok=True)

        if action == 'claim':
            claim = db.execute('SELECT * FROM funded_claims WHERE id=?', (text(data,'id'),)).fetchone()
            if not claim: fail('Reward request not found.',404)
            revision=integer(data,'revision',0,1000000)
            if claim['revision']!=revision: fail('This request changed. Reopen it before deciding.')
            state=data.get('status')
            allowed={'pending':('pending','approved','declined'),'approved':('given','declined'),'given':(),'declined':()}
            if state not in allowed[claim['status']]: fail('This request has already moved to another step.')
            note=text(data,'note',3,500)
            demonstration=data.get('demonstration',{})
            if state=='approved':
                keys=LAPTOP_DEMO if claim['reward']=='core-laptop' else ('sample',)
                if not isinstance(demonstration,dict) or any(demonstration.get(k) is not True for k in keys):
                    fail('Confirm the short skill demonstration before approving. Talking, drawing, typing and supports all count.',400)
            db.execute('UPDATE funded_claims SET status=?,note=?,demonstrated=?,revision=revision+1 WHERE id=?',
                       (state,note,int(state=='approved' or claim['demonstrated']),claim['id']))
            allocation_state='released' if state=='declined' else state
            db.execute('UPDATE reward_allocations SET state=? WHERE id=?', (allocation_state,claim['allocation']))
            points=claim['cost'] if state=='declined' else 0
            if state=='declined':
                db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)', ('refund-'+claim['id'],claim['learner'],points,'Reward cancelled: points returned',time.time()))
            self.audit(db,'mentor','decision',dict(claim=claim['id'],allocation=claim['allocation'],milestone=claim['reward'],from_state=claim['status'],to_state=state,points=points,reason=note,demonstration=demonstration if state=='approved' else {}))
            return dict(ok=True)
        fail('Reward action not found.',404)

    def request(self, db, learner, data, store):
        key=data.get('id')
        if key not in MILESTONES: fail('Milestone not found.',404)
        self.require_learner(db,learner)
        person=self.person(db,learner)
        if not person or person['primary_learner']!=learner:
            fail('Your mentor needs to confirm your main account before a reward request.')
        allocation=db.execute('SELECT * FROM reward_allocations WHERE id=? AND person=? AND milestone=?', (text(data,'allocation'),person['id'],key)).fetchone()
        if not allocation: fail('This reward is not set aside for your account. Refresh to check its funding.')
        old=db.execute('SELECT * FROM funded_claims WHERE allocation=?',(allocation['id'],)).fetchone()
        if old: return dict(claim=old['id'])
        if allocation['state']!='allocated': fail('This allocation has changed. Refresh before requesting.')
        if key!='core-laptop':
            from gift_cards import used, CAP_CENTS
            if used(db,person['id'])[0]+500>CAP_CENTS:
                fail('This earlier card would exceed the $250 lifetime gift-card cap. Review the existing agreement with your mentor.')
        store.require_tutorial(db,learner)
        required,version=self.requirements(db,learner,key)
        mastered={r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1",(learner,))}
        if not set(required).issubset(mastered): fail('Finish the named modules in this part of your saved path first.')
        cost=0 if key=='core-laptop' else 60
        if store.points(db,learner)<cost: fail('Keep practising. This card needs 60 points.')
        cid=uid()
        db.execute('INSERT INTO funded_claims(id,allocation,learner,reward,status,cost,created) VALUES(?,?,?,?,?,?,?)',(cid,allocation['id'],learner,key,'pending',cost,time.time()))
        db.execute("UPDATE reward_allocations SET state='pending' WHERE id=?",(allocation['id'],))
        db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)',('claim-'+cid,learner,-cost,'Reward: '+MILESTONES[key][1],time.time()))
        self.audit(db,learner,'request',dict(claim=cid,allocation=allocation['id'],milestone=key,path_version=version,required_modules=required,points=-cost,from_state='allocated',to_state='pending'))
        return dict(claim=cid)
