ANSWER-4 from Tuesday (s128, 2026-10-20 22:37 AEDT) to B330 (Datasec/Security-Composer-W15). Answers your READY FOR QA of 22:33:39 and its FOR TUESDAY 1-8. SUPERSEDES the brief's "not yours" fence for the 8 renderer test files, the renderer sources the two non-pin failures need, and `apps/api/src/content.test.ts`, as below. Everything else in the brief, the addendum and ANSWER-1/2/3 stands. The K6 FENCE stands: build and test on the branch, cut nothing.

Tuesday's checks of your READY (measured 22:3x, Composer's own gh identity, GETs only): ref `b330/sm316-content-catalogue` = 40b332cf; main 308b7aa6 unchanged; compare ahead 4, behind 0, 38 files, all under your declared paths. Tuesday opened DRAFT PR #85 ("HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)").

WHY THE FENCE MOVES: the held files were B323's, and B323's lane has LANDED (PR #84 = main 308b7aa6). No other Composer seat is live now (Tuesday's `tmux list-panes`, 22:37: %0=tuesday %150=Datasec/MPS-G26 %146=Datasec/Security-Composer-W15 %145=Datasec/NexusAI-W18 %1=fleet-monitor). A tier-1 gate on a branch with 18 known red tests would spend a round proving what you already wrote down, so the pins are fixed BEFORE the gate (Kam's 2026-09-18 rule: minimise gate duplication).

ROUND 2 (on the same branch; new commits on top of 40b332cf, plain push, never a force push, never `--no-verify`):
1. **Count/digest pins (16 of the 18):** pin-only edits in each file's own "re-pinned for … → …" comment style, as you did in the engine tests. Each new number is the one the new release produces, read from a run, never typed.
2. **The output secret-scan false positive** (`render.test.ts`, `policy-document.test.ts`: the Identity Certificate label run "Username Server Password DigiCert"). Do NOT change SM's label and do NOT disable the scan or exempt a whole file. First MEASURE which rule fires and on which exact text. Then make the NARROWEST change to the scanner (for example: the `username <x> password <y>` shape requires value-like tokens, or known label words are not values), and prove BOTH arms: (a) a real credential shape such as `username admin password hunter2` (and the scanner's own existing positive fixtures) STILL fires; (b) the new label run passes. If no narrow change exists, STOP and say what the options are, with their cost: this is a guard, and the tier-1 gate will read the change line by line.
3. **The PDF mid-word break** ("Communicatio | n (NFC)", `s43-fx-r-documents.test.ts`): fix in the RENDERER (column width, a no-break rule inside words, or the wrap function), never by changing the label. Evidence: `pdftotext` of the affected page before and after, and a test that is red on the break.
4. Full node route on the new tip (lint, format, typecheck, build, test) and both DB suites: 0 failed except the pre-existing skip. Load rule unchanged (`waitload.sh`, below 8).
5. Re-run your Q-03/Q-04 gate, the client-name / card-id scans and gitleaks over the new commits; same patterns; 0 hits with controls firing.

RULINGS ON FOR TUESDAY:
1. Demo scope: ACCEPTED as built (release-demo keeps the 55 Preview items with their SM ids, no SM-only rows). The SM rows reach the demo only with L2's values; not in this lane.
2. Held pins: round 2 above.
3. Duplicate names: ACCEPTED (non-Cloud id for all 13, Cloud ids unmapped). The records seat carries it as a question for the next review round.
4. `SM-<id>` controls: ACCEPTED.
5. Unresolved/unmapped items: ACCEPTED as recorded; they go to the records seat (BACKLOG rows) and to the review-round questions.
6. Typing the 55 existing items' fields: out of this lane; a BACKLOG row (needs the setting → choice-set link).
7. #272/#252 sequencing with one combined release: NOT decided now. It is decided at release-cut time, after Kam's open word and deploy cards. Touch neither.
8. Commit grouping: no re-split. Composer lands by squash, so only the tip has to build.

Your process disclosures (tests after code, the two `/dev/null` rm no-ops, the probe mountpoint quarantined) are received and go in the gate brief as stated.

When done: a new READY FOR QA last line naming the new tip and "round 2: 18 held fixed". Then STOP: do not open, mark or comment on the PR, and do not wrap until Tuesday says so (the gate may have questions for you).
