# Current release verification

The current source interface is build 120. The public browser demo is revision 2, based on the same lesson and answer bank. The earlier preparation results below are retained as historical evidence.

- The corrected source passed all 230 backend tests and all 35 JavaScript/content suites. Backend tests use disposable local accounts and include authentication, ownership, invitation/recovery, Host/Origin, cookie, private-file and backup boundaries.
- The browser demo renders all 144 lesson opening screens at desktop and 320-pixel widths. Its five main views were checked at 320, 390, 768, 1100, 1240, 1440 and 1699 pixels, including whether navigation contents fit their buttons.
- Demo security checks reject account actions, restrict scripted connections to the same origin, escape mentor-feedback text, and prevent narration through remote voices. The browser policy blocks inline scripts, eval, embedded objects and service workers.
- Public repository files and reachable history were inspected for credentials, private records and personal paths. The published commit authors use GitHub noreply addresses. The demo contains code, lesson data, practice answers, assets and notices; it contains no learner database or account records.
- Local testing is isolated from the owner's working Stepstone installation. Lesson IDs and grading values are unchanged.
- A complete browser-demo math lesson passed all six checkpoint answers, saved its result across reload, and left the normal visitor practice empty. Release tests use a separate local scope through the `practice` query parameter.
- Daily dates use consistent Manitoba time after the [31 October 2026 proclamation](https://web2.gov.mb.ca/laws/statutes/proclamations/2023c4(2026-10-31).php?lang=en), including on browsers with older timezone data. The source's versioned assets and offline cache are rebuilt for build 120.

The public demo is a trial with local practice and fictional mentor feedback. Shared online learner accounts and private mentor reports are not deployed. Physical phone/tablet acceptance, production account hosting, capacity and independent security assessment remain separate checks. No teaching-effectiveness claim is made.

---

# Verification — interface 119 / server 41

## This candidate's change

The public-source candidate replaces five extracted Museum images with original value diagrams and updates their adapter, descriptions, asset queries and cache. The Python backend and checkpoint bank are unchanged; two singular-label phrases in Count the stock practice are corrected without changing question IDs, numbers, answers or meaning. The installed local build remains separate. The generator and all five SVG assets use MIT; the Museum resource is only an external link.

## Prior build-118 evidence

The reviewed build-118 source candidate passed 229 backend tests on 11 October 2026. The application audit also passed 35 JavaScript/content suites and 55 public JavaScript syntax checks. Its disposable learner completed all 144 active modules with 864/864 final correct answers and 145 matching mentor receipts, including a failed attempt and retake. Its layout sweep covered 1,728 views. Those checks concern the build-118 application and synthetic behaviour, not real learner mastery.

The full curriculum/rendering sweeps preceded the small Revisit route fix. JavaScript/syntax and focused Revisit/offline/account checks ran after that fix. Earlier first-use checks covered the 24-question start, tour, feedback, support replies, browser approval/revocation and learner return. Raw receipts and all disposable records remain outside this source package.

## Build-119 checks

The affected lesson suites verify the $10/loonie/quarter example counts, 24-dollar and 2.75-dollar totals, cash selection/undo and drag/drop contracts, retained drafts, correct image descriptions and source-resource footer. A browser component review loads the actual worked-example and cash-game renderers, uses the new SVGs, and checks arithmetic and controls at 320, 390, 768 and 1440 pixels. It is a component review with fictional in-memory work; it does not create a learner, submit a check or establish a new full learner-to-mentor result.

The final local release receipt records suite/syntax results, all 175 asset responses, source hashes, archive integrity, local documentation links and exclusion of the Museum images and learner data. Optional voice installation is not run as part of this release preparation.

## Limits

No shared public deployment or real learner acceptance is established. Real phone/tablet acceptance, hosted account/report flows, capacity, off-host recovery and physical reward delivery require separate checks. Browser emulation is not a physical-device test. A software score is one part of mentor review; it does not prove independent understanding or validate teaching effectiveness.

## Final preparation results — 12 October 2026

- 35/35 JavaScript/content suites and 55/55 public JavaScript syntax checks passed.
- 3/3 hosting and allowlisted-package tests passed with disposable data.
- All 175 cached public assets returned matching bytes; all five new money assets returned image/svg+xml. The Museum image extracts are absent.
- The browser component review passed at 320, 390, 768 and 1440 pixels, with no broken images, horizontal page overflow or equation errors. Real cash selections produced 7.25 dollars; undo produced 7.00. Example totals were 24 dollars and 2.75 dollars. These are component controls, not a new whole-account audit.
- All 96 Python files and the PowerShell scripts parsed. The runtime Python backend and checkpoint bank match the prior reviewed bytes. Two singular-label wording fixes retain the question IDs, numbers and answers.
- Source hashes matched the existing local application before the staged frontend changes. That installation and its learner records were not modified.
- Font/KaTeX licenses are preserved. The SVG generator and diagrams are original MIT work. Optional voice installation was not executed; its installer now creates its private data folder if absent.

The final source and hosting archives were checked for integrity and SHA-256 manifests. GitHub publication, social posting and shared hosting have not been performed. The command-line GitHub credential requires re-authentication before a CLI upload.
