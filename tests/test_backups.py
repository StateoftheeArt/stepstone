"""Recovery correctness and access checks; uses only disposable synthetic records."""
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from unittest.mock import patch
import test_server as base
import backups


class BackupTests(unittest.TestCase):
    setUp=base.PilotTests.setUp
    tearDown=base.PilotTests.tearDown
    learner=base.PilotTests.learner
    check=base.PilotTests.check

    def test_consistent_copy_restore_and_expired_access(self):
        learner, person = self.learner()
        self.check(learner)
        unused = self.mentor.request('/api/mentor/invite',{})[1]
        record = self.app.backups.create()
        snapshot = self.app.backups.directory / record['file']
        self.assertEqual(backups.verify(snapshot)['tables']['attempts'],1)
        target = Path(self.tmp.name)/'restored'
        receipt = backups.restore_snapshot(snapshot,target)
        self.assertTrue(receipt['sessionsRevoked'])
        db=sqlite3.connect(target/'stepstone.sqlite3')
        try:
            self.assertEqual(db.execute('select count(*) from sessions').fetchone()[0],0)
            self.assertEqual(db.execute('select sum(delta) from ledger').fetchone()[0],20)
            self.assertEqual(db.execute('select count(*) from attempts where finished is not null').fetchone()[0],1)
            self.assertEqual(db.execute('select max(expires) from invites where used=0').fetchone()[0],0)
        finally: db.close()
        with self.assertRaises(ValueError): backups.restore_snapshot(snapshot,target)
        self.assertEqual(learner.request('/api/me')[1]['id'],person['id'])
        self.assertEqual(backups.verify(snapshot),record)

    def test_only_mentor_can_create_and_snapshots_are_private(self):
        learner,_=self.learner()
        self.assertEqual(base.Client(self.url).request('/api/mentor/backup',{})[0],401)
        self.assertEqual(learner.request('/api/mentor/backup',{})[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/backup',{},headers={'Origin':'https://other.invalid'})[0],403)
        status,settings,_=self.mentor.request('/api/mentor/backup',{})
        self.assertEqual(status,200)
        self.assertEqual(settings['recovery']['count'],1)
        for prefix in ('/recovery/','/data/recovery/'):
            self.assertEqual(base.Client(self.url).request(prefix+settings['recovery']['file'])[0],404)
        self.assertNotIn('sha256',json.dumps(settings))

    def test_restore_cannot_revive_a_replaced_return_code(self):
        _,person=self.learner()
        record=self.app.backups.create()
        replacement=self.mentor.request('/api/mentor/recovery',{'id':person['id']})[1]['code']
        staged=Path(self.tmp.name)/'restored-access'
        receipt=backups.restore_snapshot(self.app.backups.directory/record['file'],staged)
        self.assertTrue(receipt['returnCodesRevoked']);self.assertTrue(receipt['mentorAccessReset'])
        saved=json.loads((staged/'restore-receipt.json').read_text(encoding='utf-8'))
        self.assertNotIn('recoveryKey',saved)
        restored=base.server.create_server(port=0,data=staged)
        thread=threading.Thread(target=restored.serve_forever,daemon=True);thread.start()
        client=base.Client(f'http://127.0.0.1:{restored.server_address[1]}')
        try:
            for code in (person['recovery'],replacement):
                self.assertEqual(client.request('/api/login',{'code':code})[0],401)
            # The copy's old passphrase and recovery key stop working; the one-time key from the restore works.
            self.assertEqual(client.request('/api/mentor/login',dict(username='test-mentor',passphrase='test-only-mentor-passphrase',device='Restored test browser'))[0],401)
            self.assertEqual(client.request('/api/mentor/recover',dict(username='test-mentor',recovery=self.account_setup['recovery'],passphrase='a-new-test-passphrase',device='Restored test browser'))[0],401)
            self.assertEqual(client.request('/api/mentor/recover',dict(username='test-mentor',recovery=receipt['recoveryKey'],passphrase='a-new-test-passphrase',device='Restored test browser'))[0],200)
            fresh=client.request('/api/mentor/recovery',{'id':person['id']})[1]['code']
            status,resumed,_=client.request('/api/login',{'code':fresh})
            self.assertEqual(status,200)
            self.assertEqual(resumed['id'],person['id'])
        finally:
            restored.shutdown();restored.server_close();thread.join()

    def test_corrupt_or_wrong_snapshot_and_existing_folder_are_rejected(self):
        record=self.app.backups.create();path=self.app.backups.directory/record['file']
        with path.open('ab') as f:f.write(b'corrupt')
        with self.assertRaises(ValueError):backups.verify(path)
        with self.assertRaises(ValueError):backups.restore_snapshot(path,Path(self.tmp.name)/'bad')
        self.assertFalse((Path(self.tmp.name)/'bad').exists())

    def test_restore_hold_blocks_claims_until_mentor_records_reconciliation(self):
        learner,_=self.learner()
        with self.app.store.db() as db:
            db.execute("INSERT INTO settings VALUES('recoveryHold',?)",(json.dumps({'snapshot':'synthetic-protocol-fixture'}),))
        self.assertEqual(learner.request('/api/reward',{'id':'core-card-1'})[0],409)
        self.assertEqual(learner.request('/api/ai/request',{})[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/ai/activate',{})[0],409)
        self.assertEqual(self.mentor.request('/api/mentor/funded/claim',{'status':'approved'})[0],409)
        self.assertEqual(learner.request('/api/mentor/recovery-reconciled',{'confirmed':True,'note':'Synthetic check only.'})[0],401)
        self.assertEqual(self.mentor.request('/api/mentor/recovery-reconciled',{'confirmed':'yes','note':'Synthetic check only.'})[0],400)
        self.assertEqual(self.mentor.request('/api/mentor/recovery-reconciled',{'confirmed':True,'note':'Synthetic fixture; no actual deliveries occurred.'})[0],200)
        self.assertFalse(self.mentor.request('/api/mentor')[1]['settings']['recovery']['rewardsOnHold'])
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reward_audit WHERE action='recovery-reconciled'").fetchone()[0],1)
        self.assertEqual(self.mentor.request('/api/mentor/recovery-reconciled',{'confirmed':True,'note':'Duplicate retry.'})[0],200)
        with self.app.store.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM reward_audit WHERE action='recovery-reconciled'").fetchone()[0],1)

    def test_automatic_retention_and_failure_visible(self):
        manager=self.app.backups
        manager.retained=2
        unrelated=manager.directory/'keep-owner-notes.txt'
        manager.directory.mkdir();unrelated.write_text('Keep me',encoding='utf-8')
        for _ in range(3):manager.create()
        self.assertEqual(manager.status()['count'],2)
        self.assertTrue(unrelated.exists())
        manager.enabled=True;manager.last_try=0
        with patch('backups.time.time',return_value=10**12):
            manager.tick();manager.close()
        self.assertEqual(manager.status()['count'],2)
        with patch('backups.create_snapshot',side_effect=OSError('test disk full')):
            with self.assertRaises(OSError):manager.create()
        self.assertIn('did not finish',manager.status()['error'])
        self.assertEqual(manager.status()['count'],2)

    def test_timer_problem_never_stops_the_server(self):
        manager=self.app.backups
        manager.enabled=True;manager.last_try=0
        with patch.object(backups.BackupManager,'records',side_effect=OSError('test storage problem')):
            manager.tick()
        self.assertIn('could not be checked',manager.error)
        manager.last_try=0
        with patch.object(backups.BackupManager,'tick',side_effect=RuntimeError('test fault')):
            self.app.service_actions()
        self.assertIn('stopped',manager.error)
        self.assertEqual(base.Client(self.url).request('/api/health')[0],200)


if __name__=='__main__':unittest.main()
