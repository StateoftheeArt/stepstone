# Security and private data

The public browser demo has no learner accounts, invitations, private mentor reports or account backend. It stores practice in the visitor's browser. Anyone using that same browser profile can see the practice. Use fictional details on a shared device. Its question bank and answers are public practice material, not a protected assessment.

The full Python application is a separate installation. Its learner database, sessions, invitations, recovery copies, mentor credentials and reward records must remain outside public files and Git history. Never publish `data/`, recovery databases, environment files, private links or credentials. Shared hosting requires the HTTPS and storage controls in [HOSTING.md](HOSTING.md).

## Reporting a concern

Do not put learner records, invitation or recovery codes, passwords, private screenshots or account details in public GitHub issues or social comments. Alert the maintainer with a description that contains no private data and ask for a private channel before sending sensitive evidence. If a credential was exposed, removing a file is insufficient: revoke or rotate the credential and review the repository history.

## Verification limits

Automated account, ownership, Host/Origin, cookie and static-file boundary tests use disposable local records. They establish those software contracts; they do not establish production TLS, operational capacity, real-device acceptance or independent security certification. The browser demo's current privacy notice describes its actual data flow.
