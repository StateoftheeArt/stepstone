# Shared-device pilot handoff

Current source: interface 121 / server 41. This guide describes a prepared deployment contract, not a completed remote pilot.

The application can be run locally. A shared installation requires a configured HTTPS host and persistent storage. Publishing code does not create that service.

## Runtime contract

- Python 3.10+ for core lessons, accounts and reports; no third-party packages for those features. Optional Soft voice uses an isolated local Kokoro runtime: [installation and operating limits](VOICE.md).
- Public assets are read from `public/` only. Keep `content/`, `server.py`, and `data/` outside a reverse proxy's static root.
- Run a **single app process** for the pilot. The standard-library threaded HTTP server is intended for this small pilot, behind a production HTTPS reverse proxy. It is not an internet-scale application server.
- Use `--data` to point at persistent storage outside a deployable source bundle.
- Preserve the external Host header and add that exact host with `--allow-host`. Use `--secure-cookies` for HTTPS deployments. API responses are `no-store` and are excluded from the service worker's cache. `/api/health` answers any Host, because [Render's health checks](https://render.com/docs/health-checks) use a verified custom domain when one exists; it returns no private records.
- Ordinary mentor registration creates a separate empty workspace and can be offered at the shared HTTPS address. Only claiming existing host records requires a loopback client and loopback Host header, plus the previous passphrase when one exists. Preserve the external Host header through the proxy; do not globally block ordinary account creation as though it were the local-claim operation.
- The host must terminate TLS, limit request sizes/rates, supervise the process, and retain an operational backup. Do not expose the Python port directly to the public internet.
- Verify sign-in, a learner check, server persistence across a restart, offline retry, mentor review, and reward approval on the actual phone/tablet browsers before inviting learners.

An example invocation after selecting and configuring a host is:

```text
python -B server.py --host 127.0.0.1 --port 8090 --data /persistent/stepstone --public-url https://your-configured-host.example --secure-cookies
```

The example domain and storage path are placeholders, not configured services. This build has not been deployed to that or any public host.

## Prepared shared-host option (not deployed)

A free full-app route is now prepared: [PythonAnywhere setup](FREE_HOSTING.md).
It preserves learner and mentor records on the free account's filesystem,
requires monthly web-app renewal, and is intended for a small supervised pilot.
The Render option below is optional paid infrastructure; no subscription is
required to use the free route.

`render.yaml` describes one Python web service and a 1 GB persistent disk. Render
supplies HTTPS and its own app address; no purchased domain is required. The
startup wrapper requires durable storage and reads `RENDER_EXTERNAL_URL` (or an
explicit `STEPSTONE_PUBLIC_URL`). Invitations and return links use that canonical
address even when created from the host console. The shared service does not use
the laptop's idle-shutdown policy.

The proposed compute and 1 GB disk are a prepared starting configuration. The earlier cost estimate was checked on 2026-09-25; it is not a current quote. Check [Render pricing](https://render.com/pricing) and the chosen account before authorising provisioning.
[Persistent disks require a paid service](https://render.com/docs/disks). This is
a core-app starting configuration, **not a tested capacity estimate for Kokoro
soft narration**. Voice models and the local Windows voice environment are not
part of this deployment. Choose and test sufficient memory and provision the
voice runtime before promising the same voice experience on the shared host.

Before provisioning: choose the hosting account and cost limit, create a reviewed app
repository containing only this app, and review the upload. Do not upload `data/`,
the parent workspace, personal records, funding drafts, or a voice-runtime path.
The reviewed public repository is [StateoftheeArt/stepstone](https://github.com/StateoftheeArt/stepstone), branch `Main`. Its browser demo is a separate static service. No full account service or paid hosting subscription has been provisioned.

After deploying the reviewed app:

1. Mentors open **Mentor space → Create account** at the shared HTTPS address.
   Each creates their own username, passphrase and named first device, then saves
   their private recovery key. No account belongs to a default mentor.
2. Each mentor invites and manages only their own learners. Another device needs
   approval from their existing device, or their recovery key to replace access.
3. When migrating this existing local pilot, the installation owner first creates
   an account from the host's loopback address and selects **Keep the existing
   records on this host**. A prior mentor passphrase is required if one exists.
   Remote registration always makes a separate empty workspace.
4. Test invitations, messages, checks, reload and host restart using disposable
   accounts before inviting real learners. Back up every workspace, not just the
   original database. Each workspace has its own recovery copies and account
   metadata; none is included in the app-only hosting archive.
5. Use the shared address on learners' devices. A separate local installation
   keeps separate records; Stepstone does not silently merge databases.

Provider schema and environment details: [Blueprint specification](https://render.com/docs/blueprint-spec),
[automatic app URL](https://render.com/docs/environment-variables).

## Pilot limitations to address before wider use

The 144 active modules across six courses have content, explanations and guided workshops; nine older modules are retained for saved records. All 153 ready private check banks are separate from published practice, although later attempts can repeat cases. This is not a complete K–12 programme. Review the examples, difficulty and accessibility with the actual learners and mentor, then deepen the curriculum around their needs. Add operational account-management and retention tools before a larger programme. Separate mentor accounts, browser approvals and recovery keys are implemented. Account deletion/retention policies, abuse operations and capacity testing remain prerequisites for a broad public launch. There is no email delivery, background push notification service or app-store package.

There is no automatic AI-use judgement, reliable proctoring, or independent verification of who answered. Scores alone should not decide high-value rewards. The dashboard provides answer evidence and the learner's explanation for human follow-up.

Private learner records, credentials and machine-specific runtime configuration must stay out of shared source archives.

## Prepared recovery and upload package

[OPERATIONS.md](OPERATIONS.md) gives tested recovery, rotation and release steps.
Mentor space shows on-host recovery status and can create a consistent SQLite
copy. Restore stages into a new directory, revokes browser sessions and learner
return links, expires unused invites and pauses new reward requests/approvals until the mentor records
reconciliation of any later real-world deliveries. It also replaces a claimed workspace's
passphrase and recovery key and prints a one-time recovery key for its mentor.

`python -B tools/package_hosting.py dist/stepstone-host-build-121.zip` creates a
verified app-only archive with a SHA-256 file manifest. It refuses an existing
output. Learner data, test receipts, local voice configuration, course documents
and this parent workspace are outside its allowlist. Saving the archive does
not create a repository, upload it, purchase hosting or make a shared URL live.

The previously checked [Render Blueprint reference](https://render.com/docs/blueprint-spec)
named the small paid compute plan `0.5c-512mb`; the blueprint uses that ID.
The core-app base excludes tax, exchange rates, overages, a separately hosted
backup destination and any larger voice-capable instance. Budget and host account
still require the owner's approval. A cost estimate is not a hard spending cap.

## Deployment prepared on 13 October 2026

The blueprint selects one `0.5c-512mb` service in Ohio, the actual `Main` branch, a 1 GB disk at `/var/data/stepstone`, and manual deployment. `.python-version` selects the latest Python 3.12 patch; local checks use Python 3.12.14. The asset builder needs no external Python packages. Soft voice is outside this starter configuration.

Current [Render pricing](https://render.com/pricing) lists US$7/month for this compute size and US$0.25/month for 1 GB of disk. The Hobby workspace has no workspace subscription charge. The base is **US$7.25/month**, excluding taxes, exchange charges and usage overages. Its [included outbound bandwidth](https://render.com/docs/outbound-bandwidth) is 5 GB per month, shared by the workspace; extra public traffic is US$0.15/GB. Other services in that workspace can consume the allowance. A [build-pipeline spend limit](https://render.com/docs/build-pipeline) only limits extra pipeline minutes; it is not a total hosting or bandwidth cap. Confirm the account's plan and limits before provisioning.

Public access is through the host's HTTPS address. Records are stored in the United States for this proposed region. Use fictional aliases and practice details during acceptance; do not migrate existing records or collect sensitive personal information. A separate private off-host recovery destination still needs selection.

Run `python -B tools/check_release.py` before a release. Repository automation runs these checks on pushes and pull requests without deployment credentials or automatic hosting deployment. A successful workflow is software evidence; it does not complete the live HTTPS, restart, separate-device or real learner acceptance checks.
