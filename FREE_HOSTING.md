# Full Stepstone on a free host

This route runs the full Python application: separate mentor accounts, approved
devices, private learner invitations, saved lessons, graded reports, reviews and
feedback. Visitors need no GitHub account. The existing static browser demo is
a separate installation and its browser practice is not imported.

## Cost and limits checked 13 October 2026

[PythonAnywhere's Beginner plan](https://www.pythonanywhere.com/pricing/) is
US$0/month, with a provider subdomain and HTTPS. Its current
[free-account limits](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/)
include 512 MiB of persistent storage, one web app, one web worker and monthly
web-app expiry. Renew it from the host's Web page before its expiry date. Do not
upgrade, add a paid resource or enter a payment method for this setup.

This is a small supervised pilot configuration, not a promise of unlimited users
or uptime. The provider supports SQLite for free accounts but
[recommends a different database for larger production use](https://help.pythonanywhere.com/pages/KindsOfDatabases).
Use one worker and the existing rollback-journal SQLite setup; do not enable WAL
on the provider's network filesystem. Watch storage and response times before
expanding invitations. An external host can change its free offering later.

Local device narration remains available where the device supplies an English
voice. The optional large Soft voice runtime is excluded. Retailer comparisons
may be limited by the free plan's outbound-network allowlist. Stepstone does not
purchase rewards, deliver email or send push notifications automatically.

## Reviewed deployment

1. The installation owner creates a **Beginner** account on the US system,
   `www.pythonanywhere.com`, and keeps its credentials with that provider.
   The app's subdomain includes the chosen account username.
2. Upload the allowlisted Stepstone hosting ZIP, or clone the reviewed public
   repository into `/home/YOUR_USERNAME/stepstone`. Do not upload existing local
   learner records, backups, voice models or this parent workspace. Verify the
   source commit and archive manifest before running it.
3. Create `/home/YOUR_USERNAME/stepstone-records` separately. The WSGI entry
   refuses a missing directory, a relative path or records inside app source.
   These records stay on the provider's persistent filesystem across reloads.
4. On **Web → Add a new web app**, use **Manual configuration** and Python 3.12.
   No extra Python package or virtual environment is needed for core features.
5. Replace the generated sample WSGI configuration with the reviewed
   `tools/pythonanywhere_wsgi.py`. It derives the account's home folder and
   canonical HTTPS address on that host. Preserve a copy of any existing WSGI
   configuration before replacing it; use a new unused app for this pilot.
6. Enable [Force HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS/), then
   reload. Keep **one** web worker. Do not map `/` or a data directory as static
   files; requests must pass through Stepstone's file and security boundaries.
7. Run the disposable acceptance below. Confirm renewal date and private backup
   access before inviting real learners. If storage or capacity reaches its
   limit, stop expanding the pilot; do not silently buy an upgrade.

For the EU provider system, change the configuration's URL suffix to
`.eu.pythonanywhere.com` before deployment. The selected region is a real data
location; explain it to pilot participants. An installation uses only its own
records and does not merge records from another host.

## Recovery without a background service

PythonAnywhere does not support background threads in web apps. On this entry
point, a visited workspace gets its consistent daily recovery copy after its
request's database transaction closes. A workspace with no visits gets its next
copy on a later request. **Make a recovery copy now** also works. The latest 14
managed copies are retained per workspace; include them when checking storage.

Download complete `.sqlite3`/`.json` recovery pairs through the owner's private
hosting account to a protected off-host destination. Never create a public file
route for recovery downloads. Verify a disposable recovery copy before using
real records. [Recovery and restore procedure](OPERATIONS.md).

## Acceptance before real invitations

- Create two fictional mentor accounts, each with its own approved device.
  Confirm that one cannot see or change the other's learner reports.
- Invite one fictional learner, complete the tour and a lesson checkpoint,
  review the actual answer evidence and send a next step. Confirm that the
  learner receives it after reload.
- Test another mentor browser's approval flow and a learner return link.
- Reload the host and confirm that both groups, progress and feedback remain.
- Check HTTPS redirect, secure cookies, Host/Origin boundaries, private-file
  exclusion and actual learner phones/tablets. Verify a private recovery copy.

`python -B tools/check_release.py` includes the socket-free WSGI tests and the
existing backend/content/package checks. These use disposable local records.
A passing suite is separate from a verified PythonAnywhere deployment and a
real learner's outcome. No shared hosted URL is established by this guide alone.
