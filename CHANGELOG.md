# Changes

## Interface 122 / server 41 — 15 October 2026

- Pip's initial hint, button description and tooltip now match whether Pip is
  resting and whether quiet visuals or reduced motion are active. Quiet greetings
  no longer announce an unseen dance, including after a reload or celebration.
- Refreshed versioned assets and the offline cache; browser demo revision 4
  includes the same correction. Lesson data, grading and account records are unchanged.

## Free full-app hosting support — 13 October 2026

- Added a socket-free WSGI entry point using the existing learner and mentor
  routes, grading, cookie and ownership rules. Public proxy requests cannot
  claim local records or manage the owner's laptop.
- Added synchronous daily recovery copies for hosts that prohibit background
  threads. Local desktop and standalone hosted servers retain their existing
  background recovery behavior.
- Added a PythonAnywhere configuration template and free-host guide, with
  persistent storage, HTTPS, monthly renewal and free-plan limits.
- The hosting archive includes only reviewed app code and the new entry point;
  no existing account records or browser-demo practice is migrated.

## Interface 119 / server 41 — first public-source candidate, 12 October 2026

- Replaced five Museum image extracts with original MIT-licensed money-value SVG diagrams. The cash lessons link the Museum as a separate real-cash learning resource.
- Updated the artwork adapter, accessible image descriptions, interface asset queries and offline cache. All five new SVGs are included in the 175-asset cache.
- Added the vector generator and public bug/lesson-review templates. Retained the font's SIL OFL and KaTeX's MIT notices.
- Prepared public setup, contribution and mentor instructions. The optional Windows voice installer accepts an installed Python executable.

Lesson IDs, checkpoint questions, answers, grading, account rules, course access and saved learning contracts match the reviewed build 118. Two singular-label phrases in Count the stock practice have been corrected; their numbers and answers are unchanged. This source candidate is separate from the existing local installation. It does not include learner records or activate shared hosting, rewards, a repository or social posts.

See [VERIFICATION.md](VERIFICATION.md) for the scope and limitations of the checks.
