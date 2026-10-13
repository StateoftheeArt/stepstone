"""Private, consistent SQLite recovery snapshots; never served as web assets."""
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import sqlite3
import threading
import time

REQUIRED = {'settings', 'sessions', 'invites', 'learners', 'attempts', 'ledger'}


def readonly(path):
    return sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True, timeout=15)


def fingerprint(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def inspect_database(path):
    with closing(readonly(path)) as db:
        db.execute('PRAGMA trusted_schema=OFF')
        if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
            raise ValueError('The recovery copy failed its database integrity check.')
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not REQUIRED.issubset(tables):
            raise ValueError('This is not a complete Stepstone recovery copy.')
        return {t: db.execute('SELECT COUNT(*) FROM "' + t.replace('"', '""') + '"').fetchone()[0]
                for t in sorted(tables) if not t.startswith('sqlite_')}


def verify(snapshot):
    snapshot = Path(snapshot).resolve(strict=True)
    record = json.loads(snapshot.with_suffix('.json').read_text(encoding='utf-8'))
    if (record.get('format') != 'stepstone-recovery-v1' or
            record.get('file') != snapshot.name or record.get('sha256') != fingerprint(snapshot)):
        raise ValueError('The recovery copy does not match its checksum record.')
    if inspect_database(snapshot) != record.get('tables'):
        raise ValueError('The recovery copy does not match its table record.')
    return record


def create_snapshot(source, destination):
    source = Path(source).resolve(strict=True)
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    stem = datetime.now(timezone.utc).strftime('recovery-%Y%m%dT%H%M%S-') + secrets.token_hex(4)
    target = destination / (stem + '.sqlite3')
    temporary = destination / (stem + '.partial')
    try:
        with closing(readonly(source)) as src, closing(sqlite3.connect(temporary)) as dst:
            src.backup(dst)
        os.chmod(temporary, 0o600)
        tables = inspect_database(temporary)
        record = dict(format='stepstone-recovery-v1', file=target.name, created=time.time(),
                      sha256=fingerprint(temporary), tables=tables)
        os.replace(temporary, target)
        target.with_suffix('.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
        os.chmod(target.with_suffix('.json'), 0o600)
        verify(target)
        return record
    finally:
        temporary.unlink(missing_ok=True)


def restore_snapshot(snapshot, destination):
    """Stage into a NEW directory. Never replace a live or existing database."""
    record = verify(snapshot)
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Choose a new folder. Restore never replaces existing records.')
    destination.mkdir(parents=True)
    target = destination / 'stepstone.sqlite3'
    try:
        with closing(readonly(snapshot)) as src, closing(sqlite3.connect(target)) as dst:
            src.backup(dst)
            # A restore must not reactivate a session, invite or return code that
            # was revoked after the snapshot. The mentor issues fresh links.
            dst.execute('DELETE FROM sessions')
            for table in ('mentor_devices','mentor_device_requests'):
                if dst.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(table,)).fetchone():dst.execute('DELETE FROM '+table)
            dst.execute('UPDATE invites SET expires=0 WHERE used=0')
            for (learner,) in dst.execute('SELECT id FROM learners').fetchall():
                dst.execute('UPDATE learners SET recovery=? WHERE id=?',
                            (hashlib.sha256(secrets.token_bytes(32)).hexdigest(), learner))
            dst.execute("INSERT OR REPLACE INTO settings(key,value) VALUES('recoveryHold',?)",
                        (json.dumps(dict(snapshot=record['file'],restored=time.time())),))
            recovery_key = None
            if dst.execute("SELECT 1 FROM settings WHERE key='mentorAccount'").fetchone():
                # A passphrase or recovery key replaced after this copy must not revive. The old
                # passphrase stops working and a fresh one-time recovery key is shown to the operator.
                recovery_key = secrets.token_urlsafe(32)
                dst.execute("UPDATE settings SET value=? WHERE key='mentor'",
                            (json.dumps(dict(salt=secrets.token_hex(16), hash=secrets.token_hex(64))),))
                dst.execute("INSERT OR REPLACE INTO settings(key,value) VALUES('mentorRecovery',?)",
                            (hashlib.sha256(recovery_key.encode()).hexdigest(),))
            dst.commit()
        os.chmod(target, 0o600)
        tables = inspect_database(target)
        receipt = dict(source=record['file'], restored=time.time(), sessionsRevoked=True,
                       returnCodesRevoked=True, unusedInvitesExpired=True,
                       rewardsOnHold=True, mentorAccessReset=bool(recovery_key), tables=tables)
        (destination / 'restore-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
        if recovery_key:
            # Returned once for the operator; never written into the receipt file.
            return receipt | dict(recoveryKey=recovery_key, recoveryKeyNote=
                'Shown once. Give it privately to this workspace mentor for Lost device or forgotten passphrase.')
        return receipt
    except Exception:
        # Leave the new staging folder for inspection; never touch the source.
        raise


class BackupManager:
    interval = 24 * 3600
    retained = 14

    def __init__(self, database, enabled=False):
        self.database = Path(database)
        self.directory = self.database.parent / 'recovery'
        self.enabled = enabled
        self.lock = threading.Lock()
        self.worker = None
        self.last_try = 0
        self.error = ''

    def records(self):
        result = []
        if self.directory.exists():
            for p in self.directory.glob('recovery-*.json'):
                try:
                    value = json.loads(p.read_text(encoding='utf-8'))
                    if (value.get('format') == 'stepstone-recovery-v1' and
                            isinstance(value.get('created'), (int, float)) and
                            value.get('file') == p.with_suffix('.sqlite3').name and
                            p.with_suffix('.sqlite3').is_file()):
                        result.append(value)
                except (OSError, ValueError):
                    continue
        return sorted(result, key=lambda r: r['created'], reverse=True)

    def status(self):
        records = self.records()
        latest = records[0] if records else None
        with closing(readonly(self.database)) as db:
            hold = db.execute("SELECT value FROM settings WHERE key='recoveryHold'").fetchone()
        return dict(automatic=self.enabled, count=len(records), retained=self.retained,
                    latest=latest['created'] if latest else None,
                    file=latest['file'] if latest else None, error=self.error,
                    busy=self.lock.locked(), rewardsOnHold=bool(hold))

    def create(self):
        if not self.lock.acquire(blocking=False):
            raise ValueError('A recovery copy is already being made. Please check again shortly.')
        try:
            record = create_snapshot(self.database, self.directory)
            self.error = ''
            for old in self.records()[self.retained:]:
                # Only managed complete pairs in this recovery folder rotate.
                path = self.directory / old['file']
                if path.resolve().parent != self.directory.resolve():
                    continue
                path.unlink(missing_ok=True)
                path.with_suffix('.json').unlink(missing_ok=True)
            return record
        except Exception:
            self.error = 'A recovery copy did not finish. Check available storage and try again.'
            raise
        finally:
            self.lock.release()

    def tick(self, *, background=True):
        now = time.time()
        if not self.enabled or now - self.last_try < 300 or self.lock.locked():
            return
        self.last_try = now
        try:
            records = self.records()
        except OSError:
            # A timer problem must never stop the web server. The mentor status shows it.
            self.error = 'Recovery copies could not be checked. Check host storage.'
            return
        latest = records[0]['created'] if records else 0
        if now - latest < self.interval:
            return
        def run():
            try:
                self.create()
            except Exception:
                pass  # The private mentor status reports the failure.
        if background:
            self.worker = threading.Thread(target=run, daemon=True)
            self.worker.start()
        else:
            run()  # A WSGI host may forbid threads; complete the copy in this request.

    def close(self):
        if self.worker:
            self.worker.join(timeout=20)
