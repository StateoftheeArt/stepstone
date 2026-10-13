# Contributing to Stepstone

Help is welcome with clear lessons, accessibility, mentor workflows and reliable local setup.

For a lesson correction, name the course and module, quote only the relevant short passage, describe the error and give a corrected example with its reasoning. For a bug, include application build, browser, steps, expected result and actual result. Use fictional records. Public issues must not contain learner identities, personal circumstances, private invitation/return links, recovery keys, gift-card details or unredacted learner work.

Change one behaviour at a time and preserve module IDs, saved question meanings, drafts, explanations and reward agreements. Changing a worked example should also prompt review of practice, feedback and check cases. A passing automated check does not establish teaching effectiveness. Have a learner and mentor try the changed explanation.

Use the current catalogue and checkpoint JSON as the released lesson content. Earlier Python builders are retained as source history and helpers; compare generated output before replacing current edited lessons. Rebuild the offline cache with `python -B tools/build_assets.py` after public asset changes. Run relevant Python and JavaScript suites; use disposable data for browser or account checks.

Submit contributions under the repository's MIT license. Add provenance and compatible license notices for new third-party material. The money-value diagrams are generated from original vector code; keep denomination labels and lesson totals correct when editing them.
