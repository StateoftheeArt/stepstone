"""Funded card exchanges. Call only inside Store's transaction and account scope.

Snapshots expose metadata only. Keys are sensitive: the database and backups
need private storage. Format checks cannot prove a card's value or authenticity.
"""
import hashlib
import re
import sqlite3
import time

from reward_program import RewardError, integer, text, uid

TIERS = ((1000, 20), (2000, 36), (5000, 80))
PRICES = dict(TIERS)
CAP_CENTS = 25000
PROVIDERS = (
    dict(id='amazon-ca', label='Amazon.ca',
         pattern=r'(?:[A-Za-z0-9]{14,15}|[A-Za-z0-9]{4}-[A-Za-z0-9]{6}-[A-Za-z0-9]{4,5})',
         maximum=17, pin=False, help='Supported key: 14–15 letters and numbers; printed hyphens are allowed.',
         url='https://www.amazon.ca/gc/redeem'),
    dict(id='walmart-ca', label='Walmart Canada', pattern=r'[0-9]{16}',
         maximum=16, pin=True, help='Card number: 16 digits. PIN: 4 digits.',
         url='https://www.walmart.ca/en/cp/giftcards/6000197915574'),
    dict(id='google-play-ca', label='Google Play Canada', pattern=r'[A-Za-z0-9]{16,20}',
         maximum=20, pin=False, help='Supported key: 16–20 letters and numbers, without spaces or hyphens.',
         url='https://support.google.com/googleplay/answer/15710842?hl=en'),
)
BY_PROVIDER = {p['id']: p for p in PROVIDERS}
BLOCKED_PHRASES = ('CALLME', 'CONTACTME', 'EMAILME', 'HELPME', 'MEETME', 'PAYME',
                   'SENDMONEY', 'TEXTME', 'WHATSAPP', 'TELEGRAM', 'VISITME', 'MESSAGE')


def fail(message, status=409):
    raise RewardError(status, message)


def fields(data, allowed):
    if set(data) - set(allowed):
        fail('Only the fields shown for this action can be sent.', 400)


def install(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS gift_card_budgets (
      person TEXT PRIMARY KEY, reserved_cents INTEGER NOT NULL CHECK(reserved_cents>=0),
      revision INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS gift_card_requests (
      id TEXT PRIMARY KEY, learner TEXT NOT NULL, person TEXT NOT NULL,
      provider TEXT NOT NULL, amount_cents INTEGER NOT NULL, cost INTEGER NOT NULL,
      status TEXT NOT NULL, created REAL NOT NULL, revision INTEGER NOT NULL DEFAULT 0,
      code TEXT, pin TEXT, code_hash TEXT UNIQUE, delivered REAL);
    CREATE UNIQUE INDEX IF NOT EXISTS gift_card_one_open
      ON gift_card_requests(person) WHERE status IN ('pending','approved');
    ''')


def held(db):
    return db.execute('SELECT COALESCE(SUM(reserved_cents),0) FROM gift_card_budgets').fetchone()[0]


def used(db, person):
    new = db.execute("SELECT COALESCE(SUM(amount_cents),0) FROM gift_card_requests WHERE person=? AND status IN ('pending','approved','given')", (person,)).fetchone()[0]
    old = db.execute("SELECT COUNT(*)*500 FROM funded_claims c JOIN reward_allocations a ON c.allocation=a.id WHERE a.person=? AND c.reward!='core-laptop' AND c.status IN ('pending','approved','given')", (person,)).fetchone()[0]
    earlier = db.execute("SELECT COUNT(*) FROM claims c JOIN rewards r ON c.reward=r.id JOIN reward_accounts a ON c.learner=a.learner WHERE a.person=? AND r.category='giftcard' AND c.status IN ('pending','approved','given')", (person,)).fetchone()[0]
    # Earlier custom offers have no saved face value. Require reconciliation;
    # never guess their value or let a new cap bypass those promises.
    return new + old, bool(earlier)


def pending_value(db, person):
    return db.execute("SELECT COALESCE(SUM(amount_cents),0) FROM gift_card_requests WHERE person=? AND status IN ('pending','approved')", (person,)).fetchone()[0]


def committed(db, person):
    budget = db.execute('SELECT reserved_cents FROM gift_card_budgets WHERE person=?', (person,)).fetchone()
    return bool((budget and budget[0]) or db.execute("SELECT 1 FROM gift_card_requests WHERE person=? AND status!='declined'", (person,)).fetchone())


def main_person(db, learner, program):
    program.require_learner(db, learner)
    person = program.person(db, learner)
    if not person or person['primary_learner'] != learner:
        fail('Your mentor must confirm your main learner account first.')
    return person


def requirements(db, learner, program):
    return program.requirements(db, learner, 'core-card-everyday')[0]


def completed(db, learner):
    return {r[0] for r in db.execute("SELECT DISTINCT unit FROM attempts WHERE learner=? AND finished IS NOT NULL AND json_extract(report,'$.passed')=1", (learner,))}


def snapshot(db, learner, program):
    person = program.person(db, learner)
    primary = bool(person and person['primary_learner'] == learner)
    budget = db.execute('SELECT * FROM gift_card_budgets WHERE person=?', (person['id'],)).fetchone() if person else None
    spent, reconcile = used(db, person['id']) if person else (0, False)
    required = requirements(db, learner, program)
    open_value = pending_value(db, person['id']) if person else 0
    remaining = budget['reserved_cents'] if budget else 0
    return dict(tiers=[dict(amount_cents=a, cost=c) for a, c in TIERS], providers=PROVIDERS,
                cap_cents=CAP_CENTS, used_cents=spent, needs_reconciliation=reconcile,
                confirmed=primary, linked=bool(person and not primary),
                funded_cents=max(0, remaining-open_value) if primary else 0,
                required_modules=required, complete=sorted(completed(db, learner) & set(required)),
                open_request=bool(open_value))


def claims(db, learner=None):
    return [dict(r) | dict(reward='card-exchange', title=BY_PROVIDER[r['provider']]['label'] + ' · CAD' + str(r['amount_cents']//100),
                          kind='mentor', category='giftcard', card_exchange=True,
                          code_ready=r['status']=='given', note='Your card key is ready.' if r['status']=='given' else '')
            for r in db.execute('SELECT c.id,c.learner,c.person,c.provider,c.amount_cents,c.cost,c.status,c.created,c.revision,c.delivered,l.alias '
                                'FROM gift_card_requests c JOIN learners l ON c.learner=l.id '
                                'WHERE (? IS NULL OR c.learner=?) ORDER BY c.created DESC', (learner, learner))]


def budgets(db):
    return [dict(r) | dict(pending_cents=pending_value(db, r['person']), used_cents=used(db, r['person'])[0])
            for r in db.execute('SELECT b.*,p.primary_learner,l.alias FROM gift_card_budgets b '
                                'JOIN reward_people p ON b.person=p.id JOIN learners l ON p.primary_learner=l.id')]


def reserve(db, data, program):
    fields(data, ('key', 'learner', 'cents', 'expected_revision'))
    learner = text(data, 'learner', 1, 100)
    person = main_person(db, learner, program)
    amount = integer(data, 'cents', 1000, CAP_CENTS)
    if amount % 1000:
        fail('Set aside whole $10 amounts.', 400)
    expected = integer(data, 'expected_revision', 0, 1000000)

    def save():
        row = db.execute('SELECT * FROM gift_card_budgets WHERE person=?', (person['id'],)).fetchone()
        if expected != (row['revision'] if row else 0):
            fail('This budget changed. Reopen it before adding funds.')
        value = row['reserved_cents'] if row else 0
        spent, reconcile = used(db, person['id'])
        if reconcile:
            fail('This learner has an earlier custom card agreement without a recorded value. Review it before using the new exchange.')
        given = spent - pending_value(db, person['id'])
        if given + value + amount > CAP_CENTS:
            fail('Reserved and delivered card value cannot exceed the $250 lifetime cap.')
        if program.cash(db) < amount:
            fail('Record money actually received first. This budget cannot use unfunded or already reserved cash.')
        db.execute('INSERT INTO gift_card_budgets VALUES(?,?,1) ON CONFLICT(person) DO UPDATE SET reserved_cents=reserved_cents+excluded.reserved_cents,revision=revision+1', (person['id'], amount))
        program.audit(db, 'mentor', 'card-budget-reserved', dict(learner=learner, person=person['id'], cents=amount))
        return dict(ok=True)
    return program.command(db, 'card-budget', data, save)


def release(db, data, program):
    fields(data, ('key', 'learner', 'expected_revision'))
    person = main_person(db, text(data, 'learner', 1, 100), program)
    expected = integer(data, 'expected_revision', 0, 1000000)

    def save():
        row = db.execute('SELECT * FROM gift_card_budgets WHERE person=?', (person['id'],)).fetchone()
        if not row or row['revision'] != expected:
            fail('This budget changed. Reopen it before releasing funds.')
        unused = row['reserved_cents'] - pending_value(db, person['id'])
        if unused <= 0:
            fail('No unused funds can be released. Review any open request first.')
        db.execute('UPDATE gift_card_budgets SET reserved_cents=reserved_cents-?,revision=revision+1 WHERE person=?', (unused, person['id']))
        program.audit(db, 'mentor', 'card-budget-released', dict(person=person['id'], cents=unused))
        return dict(ok=True)
    return program.command(db, 'card-budget-release', data, save)


def request(db, learner, data, store):
    fields(data, ('key', 'learner', 'provider', 'amount_cents'))
    provider = data.get('provider')
    amount = data.get('amount_cents')
    if provider not in BY_PROVIDER or type(amount) is not int or amount not in PRICES:
        fail('Choose a listed provider and a $10, $20 or $50 card.', 400)
    person = main_person(db, learner, store.funded)

    def save():
        store.require_tutorial(db, learner)
        if not set(requirements(db, learner, store.funded)).issubset(completed(db, learner)):
            fail('Finish the Everyday decisions checks before exchanging points. Welcome points alone do not unlock cards.')
        spent, reconcile = used(db, person['id'])
        if reconcile or spent+amount > CAP_CENTS:
            fail('This exchange needs mentor review or would exceed the $250 lifetime card cap.')
        if pending_value(db, person['id']):
            fail('You already have a card request waiting. Your points have not been spent again.')
        budget = db.execute('SELECT reserved_cents FROM gift_card_budgets WHERE person=?', (person['id'],)).fetchone()
        if not budget or budget[0] < amount:
            fail('Your mentor has not funded this amount. Keep your points until funding is ready.')
        cost = PRICES[amount]
        if store.points(db, learner) < cost:
            fail('You need ' + str(cost) + ' points for this card.')
        cid, now = uid(), time.time()
        db.execute('INSERT INTO gift_card_requests(id,learner,person,provider,amount_cents,cost,status,created) VALUES(?,?,?,?,?,?,?,?)', (cid, learner, person['id'], provider, amount, cost, 'pending', now))
        db.execute('INSERT INTO ledger VALUES(?,?,?,?,?)', ('card-'+cid, learner, -cost, 'Gift card requested: CAD'+str(amount//100), now))
        store.funded.audit(db, learner, 'card-requested', dict(claim=cid, person=person['id'], cents=amount, points=-cost))
        return dict(ok=True, claim=cid)
    return store.funded.command(db, 'card-request', dict(data, learner=learner), save)


def decision(db, data, program):
    fields(data, ('key', 'id', 'revision', 'status', 'demonstrated'))
    cid = text(data, 'id', 1, 100)
    revision = integer(data, 'revision', 0, 1000000)
    state = data.get('status')

    def save():
        row = db.execute('SELECT * FROM gift_card_requests WHERE id=?', (cid,)).fetchone()
        if not row:
            fail('Request not found in your mentor account.', 404)
        if row['revision'] != revision or row['status'] not in ('pending', 'approved') or state not in ('approved', 'declined') or (row['status']=='approved' and state=='approved'):
            fail('This request changed. Reopen it before deciding.')
        if state == 'approved':
            person = main_person(db, row['learner'], program)
            if person['id'] != row['person'] or not set(requirements(db, row['learner'], program)).issubset(completed(db, row['learner'])):
                fail('The account or learning prerequisites changed. Cancel and review this request.')
            if data.get('demonstrated') is not True:
                fail('Check a changed example with the learner before approval. Talking, drawing and supports count.', 400)
        db.execute('UPDATE gift_card_requests SET status=?,revision=revision+1 WHERE id=?', (state, cid))
        if state == 'declined':
            db.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?)', ('refund-card-'+cid, row['learner'], row['cost'], 'Card request cancelled: points returned', time.time()))
        program.audit(db, 'mentor', 'card-'+state, dict(claim=cid, person=row['person'], points=row['cost'] if state=='declined' else 0))
        return dict(ok=True)
    return program.command(db, 'card-decision', data, save)


def validate_key(provider, code, pin):
    if not isinstance(code, str) or not re.fullmatch(provider['pattern'], code):
        fail('Enter only the card key. ' + provider['help'], 400)
    normalized = code.replace('-', '').upper()
    if provider['id'] != 'walmart-ca' and (not re.search('[A-Z]', normalized) or not re.search('[0-9]', normalized)):
        fail('Use the actual key containing letters and numbers, not a message.', 400)
    if any(phrase in normalized for phrase in BLOCKED_PHRASES):
        fail('Card keys only. Words or messages cannot be sent here.', 400)
    if not isinstance(pin, str) or (provider['pin'] and not re.fullmatch('[0-9]{4}', pin)) or (not provider['pin'] and pin):
        fail('Enter the 4-digit card PIN.' if provider['pin'] else 'This provider has no separate PIN.', 400)
    return normalized


def deliver(db, data, program):
    fields(data, ('key', 'id', 'revision', 'code', 'pin', 'confirmed'))
    cid = text(data, 'id', 1, 100)
    revision = integer(data, 'revision', 0, 1000000)
    if data.get('confirmed') is not True:
        fail('Confirm that the purchased Canadian card is unused and matches this request’s value.', 400)

    def save():
        row = db.execute('SELECT * FROM gift_card_requests WHERE id=?', (cid,)).fetchone()
        if not row:
            fail('Request not found in your mentor account.', 404)
        if row['status'] != 'approved' or row['revision'] != revision:
            fail('This request changed or already has a code. Reopen it.')
        provider = BY_PROVIDER[row['provider']]
        code, pin = data.get('code'), data.get('pin', '')
        normalized = validate_key(provider, code, pin)
        budget = db.execute('SELECT * FROM gift_card_budgets WHERE person=?', (row['person'],)).fetchone()
        if not budget or budget['reserved_cents'] < row['amount_cents']:
            fail('The reserved funds changed. Reconcile this budget first.')
        now = time.time()
        try:
            db.execute("UPDATE gift_card_requests SET status='given',code=?,pin=?,code_hash=?,delivered=?,revision=revision+1 WHERE id=?", (code, pin, hashlib.sha256(normalized.encode()).hexdigest(), now, cid))
        except sqlite3.IntegrityError:
            fail('This key was already delivered in your account. Use a different purchased card.')
        db.execute('UPDATE gift_card_budgets SET reserved_cents=reserved_cents-?,revision=revision+1 WHERE person=?', (row['amount_cents'], row['person']))
        db.execute('INSERT INTO reward_funding VALUES(?,?,?,?,?,?,?)', ('card-'+cid, 'gift-card-delivery', -row['amount_cents'], None, 1, 'Gift card delivered: CAD'+str(row['amount_cents']//100), now))
        program.audit(db, 'mentor', 'card-delivered', dict(claim=cid, person=row['person'], cents=row['amount_cents']))
        return dict(ok=True)
    return program.command(db, 'card-deliver', data, save)


def reveal(db, learner, data):
    fields(data, ('id', 'learner'))
    cid = text(data, 'id', 1, 100)
    row = db.execute("SELECT provider,amount_cents,code,pin FROM gift_card_requests WHERE id=? AND learner=? AND status='given'", (cid, learner)).fetchone()
    if not row:
        fail('No delivered card is available for this account.', 404)
    return dict(row) | dict(label=BY_PROVIDER[row['provider']]['label'], url=BY_PROVIDER[row['provider']]['url'])
