# Stepstone operator guide

The private Mentor space is the daily control room. Only the host owner uses the
commands below. Do not put account records, private links, backups or passphrases
in a source repository, chat, funding page or public download.

Current source: interface build 121 / server 41.

This public-source release uses original money-value diagrams, current guides and updated asset versions; it does not rewrite saved records or change the database schema. The build-84 companion
receipt remains historical evidence for that earlier release.

## Daily use

1. Read new reports, including the explanation and support used. A score does not
   prove independent understanding. Ask for a short changed example.
2. Use one private invitation for one learner. Do not post it publicly. Use
   **Help them sign in** to replace a lost return code; the old code and browser
   sessions are revoked. People sharing Wi-Fi or a device remain separate people.
3. Only record funds or items actually received. Assign secured stock to a
   confirmed learner. A request, approval and recorded delivery are different.
   Stepstone does not pay, buy subscriptions or send messages automatically.
4. Check **Mentor space → Account & settings → Recovery copies**. Its timestamp records a copy checked
   when made. A storage failure appears there. **Make a recovery copy now** makes
   another consistent copy without stopping learning.

## Recovery copies and retention

Desktop and configured shared hosts create a copy at startup if none is recent,
then about once every 24 hours while running. The latest 14 managed copies stay
under the data directory's `recovery/` folder. Older managed copy/checksum pairs
rotate only after a new copy passes validation. Other files are left alone.

The free WSGI entry instead checks the visited workspace after each request and
makes a due copy synchronously, without a timer or background thread. An idle
workspace gets its next automatic copy when someone visits it. Manual copies
remain available. Check [FREE_HOSTING.md](FREE_HOSTING.md) for storage and renewal.

Each copy uses SQLite's backup operation, followed by an integrity check, table
counts and SHA-256. It includes private account and reward records. It is never a
public web asset. Report exports are not a substitute for database recovery.

Copy the `.sqlite3` file AND matching `.json` record to a protected off-host
location at least weekly and before a release. Use an encrypted backup service
or encrypted storage under the owner's account. That destination has not been
chosen or connected here. On-host copies cannot recover a lost hosting account
or destroyed disk. Maximum possible work loss depends on the last usable copy.

Manual consistent copy (paths are examples):

```text
python -B tools/backup_records.py create --data /var/data/stepstone --output /private-backups/stepstone
python -B tools/backup_records.py verify /private-backups/stepstone/recovery-TIMESTAMP.sqlite3
```

## Restore without overwriting the working app

1. Keep the failing/current data directory. Do not delete or overwrite it.
2. Verify the selected snapshot and read its timestamp. A restore returns learning
   and reward records to that point; reconcile any later real-world deliveries
   before allowing new rewards. Never pay again because a restored screen says
   an earlier reward is pending.
3. Stage the verified copy in a NEW folder. The tool refuses existing folders:

```text
python -B tools/backup_records.py restore /private-backups/stepstone/recovery-TIMESTAMP.sqlite3 --to /var/data/stepstone/restored-TIMESTAMP
```

   On the prepared Render host, stage inside the persistent disk (`/var/data/stepstone`).
   A folder outside it is lost on restart. The hosted start refuses a data folder
   that does not exist and reports whether it opened existing records.
4. Stop the old app process. Start the reviewed release with `STEPSTONE_DATA_DIR`
   pointing to the restored folder. Preserve the same canonical HTTPS address.
5. The restore tool prints a new one-time recovery key for a claimed workspace.
   The copy's old passphrase and recovery key stop working, so a key replaced
   after the copy was made cannot revive. Give the new key privately to that
   workspace's mentor; it is not saved in the receipt. Use **Mentor space → Lost
   device or forgotten passphrase?** with it. Restore clears approved mentor browsers,
   pending device requests, learner sessions, unused invites and learner return
   codes. Recovery sets a new passphrase and replacement recovery key. Save it.
   Use **Help them sign in** to issue learners fresh private return links.
6. New reward requests and approvals are held after restore. In **Account & settings**,
   reconcile later deliveries and record what was checked before reopening them.
   Compare learner counts, a recent report, project, point balance and reward
   history with the recovery receipt. Verify a new disposable learner separately.
7. Keep the previous folder until recovery and any delivery reconciliation are
   complete. Do not run two servers against the same SQLite directory.

The tool records counts and a restore receipt, not aliases or answers. It does
not change the snapshot. A corrupted copy is rejected. A mentor's passphrase is not recoverable as plaintext. The private recovery key
is required for the app's lost-device/forgotten-passphrase flow; it is rotated
on use. There is no email reset or password bypass based on the local network.

## Name and item filter

Nicknames, companion names, personal goals, useful-app plans and items, reward
names and mentor account names are checked against a PG-16 word list. It catches
common words and disguises; it is not complete moderation. Messages, reflections
and written work are never filtered, so a learner can describe a real situation.
The list is stored encoded in `public/text-filter.json`. To see or change it:

```text
python -B tools/text_filter_terms.py show
python -B tools/text_filter_terms.py check "A nickname to test"
python -B tools/text_filter_terms.py add exact someword
python -B tools/text_filter_terms.py remove exact someword
```

After a change, run `python -B tools/build_assets.py` and the tests, then restart
Stepstone. Existing names are not changed retroactively.

## Sign-in limits

Twelve failed sign-ins within 15 minutes pause further attempts from that
address for 15 minutes; mentor attempts count per address and username.
Successful sign-ins never count. On the prepared shared host, the address is the
last `X-Forwarded-For` entry added by the provider's proxy. After deploying,
confirm that failed attempts on one device do not pause another device.

## Shared-host release checklist

- Use the reviewed app-only archive and its manifest. Keep the parent workspace,
  actual `data/`, test receipts, old snapshots and machine-specific voice files
  outside the upload. The package builder uses an explicit runtime allowlist.
- One persistent app process behind HTTPS. Do not expose the Python port itself.
  Preserve the canonical Host header. Mentors can create separate accounts at the
  configured address; each receives its own private workspace. Claiming pre-existing
  host records is a separate, one-time action restricted to the host computer.
- Use the provider's private shell for initial setup and backup transfers. Owner
  account MFA and the provider's access controls are operator responsibilities.
- Before inviting real learners, test a private invite, recovery, a completed
  check, mentor feedback, host restart, offline/reconnect and installed use on
  actual phone/tablet browsers. Browser emulation is not a physical-device test.
- Review cost and traffic metrics after the first test group. No capacity or
  uptime guarantee follows from the local tests. Soft narration needs a separately
  provisioned voice runtime and a memory/concurrency test on the chosen host.
- During an outage, keep the same learner signed in and its pending work on the
  device. Reopen when connected. Do not clear browser data while work is queued.

## Programme boundaries

This is a small supervised pilot, not a complete K–12 qualification, emergency
service, reliable AI detector or unsupervised mentor. The adult reviews written
work and practical demonstrations. Current guides link official Manitoba/Canada
sources; revisit those sources when a learner takes a real-world action.

Set a retention policy with the mentor and families before a wider programme.
There is no self-service learner account deletion or automated off-host backup
destination yet. Do not collect diagnoses, household details, ID numbers or
passwords in lessons. These are operational limits, not hidden completed features.

## Independent mentor workspaces

The original pilot uses `data/stepstone.sqlite3`. Other mentor groups use
`data/workspaces/<random-workspace-id>/stepstone.sqlite3`. Each includes its own
account metadata, password hash, approved devices, learners, messages, reward
records and recovery keys (hashed). The server builds its account directory from
that metadata at startup. It rejects duplicate names or workspace identities.

A mentor's recovery button backs up only that mentor's database. Automatic
recovery copies cover every loaded workspace on desktop/shared hosts. Include
all workspace directories in a protected off-host backup plan. Restore an
individual workspace into a new location first; do not overwrite running data.
The host owner must preserve the workspace identity and avoid mounting the same
identity twice. A root-workspace restore can run as a separate installation.

Browser approval is a persistent HttpOnly cookie, not a hardware fingerprint.
The browser profile must remain private. Approvals last up to one year; Sign out
revokes the current approval. A passphrase alone cannot approve a new browser.
Lost-device recovery revokes all old approvals and rotates the recovery key.
The installation owner controls host lifetime but does not receive other
mentors' dashboards through the app. An operating-system administrator can
access host files; these are not encrypted from the host administrator.

Gift-card keys: private database and recovery copies contain delivered keys and PINs. Protect these files; the app does not encrypt them. Account snapshots, ordinary exports and audit details exclude keys. Restore reconciliation applies to new card requests, funding reservations, approval and code delivery too. Current rules are in funding/POINTS_AND_REWARDS.md.


Verification and remaining limits: [VERIFICATION.md](VERIFICATION.md).
