# gate48a COMMISSION — ONE Secuura PR: #1354 KS-470 (T2), ROUND 1 of its own PR; author and merger Seat B 47th, round 48a

Filled by fill_gate48a.py at 2026-09-29T22:26:13Z from pins_gate48a.json (measured 2026-09-29T21:56:28Z). Wednesday's commission to the drafter, 2026-09-30, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 24 keywords (each as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |
|---|---|---|---|---|---|---|---|---|
| #1354 | KS-470 | T2 | `4370be410bbf37b839b1030f3e28f95d11c454fe` | `37205947ddd2` | `37205947ddd2` | 1 / 0 | 2 (7 0 Blockchain/Dev/scripts/audit/audit-baseline.json; 3 3 systemTest/performance/package-lock.json) | 81 -> 89 |

- develop `37205947ddd2775a72a417beb5b7ac8e3240fbf3` (tree `6930599560c93f3a6cd929cc634b537a2eeb2eaf`) = #1350's squash (gate47's GO). #1354's parent IS develop (0 behind, 1 ahead); alone over develop it is clean and its squash gives END_TREE `bcac9e18943fa6aa97b394a7c8b4424124af6ea9` == the head's own tree (pins (E)-(G)).
- Recorded modes (pin (H), `git ls-tree`): #1354 audit-baseline.json 100644; #1354 package-lock.json 100644; CONTROL pre-push 100755 (not a PR path: the instrument reads a second value in the same run) — all 3 OK at head / alone / END (the control at develop / head / END).
- THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT (pin (I), (K)): pre-push 100755 ffc25ebc37d4 (IDENTICAL at develop, head and END); preflight.sh 100644 270b8913c009 (IDENTICAL at develop, head and END); lockfile-cleanroom.sh 100644 518bffeeaf4a (IDENTICAL at develop, head and END); baseline-contract.mjs 100644 2504d9a28dc0 (IDENTICAL at develop, head and END).
- Author and merger Seat B 47th (tmux %77). Pane `QA/Secuura-batch1354`. Report dir `2026-09-30-batch1354-g48a`.

## The rulings
- Wednesday's leg-7 ruling (2026-09-30 07:31 AEST, under Kam's 2026-09-09 advisory-baseline grant): **FIX** js-yaml GHSA-r3ph (lock-only, MOVED=1 as the outcome test) and **ONE baseline row** for undici GHSA-r53p, ticket KS-470. Its item 2 ("no `expires`") is **SUPERSEDED** by the ROUTE B ruling (07:39 AEST): `expires 2026-10-09`, the contract edit reverted byte-equal, TWO files; the seat's two deviations (the verb `npm update js-yaml`; the parent-dir mount) ACCEPTED.
- **TIER 2** (Wednesday's; the gate grades it). **ROUND 1 of its own PR; a round-1 NO GO goes back to the author for round 2.**
- **The grant's exception is the ruling that decides the verdict**: "A package appearing in BOTH a test lock and a shipped tree stops for Kam, regardless of severity." If it fires: NO GO, first, for Kam.

## What the gate must check (by name)
1. **The lock**: exactly one entry moves (js-yaml 5.2.3 -> 5.4.2), integrity/resolved == the registry, lockfileVersion and the `secuura-observability` link byte-identical; the seat's regen re-run in a scratch copy gives the same bytes; both deviations reproduced; the changed lock clean-room installs (no preflight leg covers `systemTest/`); 5.4.2 outside GHSA-r3ph's range READ FROM THE ADVISORY. (LOCK-DIFF-ONE-ENTRY, JSYAML-OUT-OF-RANGE)
2. **The row**: its fields, `expires` exactly 2026-10-09, ticket KS-470, a pure insert (no other row, no `$comment` byte changed), `baseline-contract.mjs` byte-equal to the base, GRANDFATHERED == the no-expiry rows; the number of rows expiring 2026-10-09 at END. (BASELINE-ROW-FIELDS, CONTRACT-BYTE-EQUAL, FUSE-COUNT)
3. **The audit gates** `audit:contract` / `audit:gate` (leg 6) / `audit:locks` (leg 7) at base (leg 6/7 FAIL expected), head and END (rc 0 each), each rc on its own line, counts and ids printed. (AUDIT-GATES-HEAD-END)
4. **Clause 2 re-measured and the exception checked**: the issuer image built (build only) and its served files searched with positive controls; every lock pinning undici / js-yaml at a vulnerable version, and whether its directory builds a shipped tree; the four clauses as rows. (CLAUSE2-REMEASURE, EXCEPTION-CHECKED, GRANT-CLAUSES)
5. **The row's `reason`**, sentence by sentence, TRUE of the tree / the image — a published record. (REASON-TEXT-TRUE)
6. **The two drafted tickets** (the undici override follow-up; the cleanroom remediation defect), line by line: POST AS-IS / POST AMENDED (in full) / DO NOT POST. (DRAFTED-TICKETS-CHECKED)
7. **The merge**: clean over develop, END_TREE `bcac9e18943fa6aa97b394a7c8b4424124af6ea9`, modes 100644 x2 with a 100755 control, the census of other open PRs (2 paths; KS-470 / KS-1374 / KS-1054 titles; Peter's #1351-#1353 REPORTED, never sequenced by the gate). (CLEAN-MERGE, END-TREE, MODES, OUT-OF-KIT-CENSUS)
8. **Subject and body**: key KS-470 only, landed <= 92, TRUE of the diff, `Refs KS-470`, no closing keyword; the PR body's factual lines. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
9. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**: the report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail, whose body carries the report's sha256.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 47th): merge 1354 on gate48a` — Seat B 47th merges #1354. Verdict mail subject: `[QA -> Wednesday] GATE48A #1354 (Seat B47 author and merger, round 48a; T2: KS-470 js-yaml 5.4.2 fixed, undici GHSA-r53p accepted to 2026-10-09)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate48a.py -> pin_1.out: clean alone; END_TREE `bcac9e18943fa6aa97b394a7c8b4424124af6ea9` == the head tree; the contract byte-equal.
- lockdiff_gate48a.py -> lockdiff_1.out: LOCKDIFF PASS: 0 FAIL | base 37205947ddd2 head 4370be410bbf | sha256 lock base a45e600e82f9ca7e head 8e0883c939d48fdd
- baseline_gate48a.py -> baseline_1.out: BASELINE PASS: 0 FAIL | FUSE-COUNT 5 row(s) expire 2026-10-09 at the head (base 4) | GRANDFATHERED 17 == no-expiry 17
- lockcensus_gate48a.py -> lockcensus_1.out: CENSUS DONE: 45 lock(s), 17 undici/js-yaml entr(y/ies), 3 vulnerable; VULNERABLE entries: 3 in 3 lock(s): ['Blockchain/Dev/frontend/issuer/package-lock.json undici 5.29.0 (PRODUCTION entry)', 'Blockchain/Dev/mobile/secuura-app/package-lock.json undici 6.28.0 (PRODUCTION entry)', 'Blockchain/Dev/package-lock.json undici 5.29.0 (PRODUCTION entry)']
- keyscan_gate48a.py -> keyscan_1.out: KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate48a.py -> gh_read_1.out: CENSUS 23 other open PR(s) read | 0 touch a kit path or carry a census key ['KS-1054', 'KS-1374', 'KS-470'] | client-human PRs named: ['1351', '1352', '1353'] (at 2026-09-29T21:59:52Z; the launch action re-reads it, rc 15 on any hit)
- capture_mail_gate48a.py -> capture_1.out: ELEVEN mails read by id, verbatim, with TEXT_SHA256 (the READY, the leg-7 thread both ways, ROUTE B, the committed status, the handover) plus Wednesday's three clause-4 chat entries to Kam (READY as captured == the seat's record /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-47th/mail/READY-gate48a.txt (stripped): True | CLAUSE-4 Kam flag entries found: 3 of 3 (2026-09-30T07:31:59, 2026-09-30T07:32:16, 2026-09-30T07:39:56); CAPTURE OK: 11 mails, 6 check(s), 0 problem(s) -> mail_gate48a_ready.md).
- drafts_gate48a.py -> drafts_1.out: both texts VERBATIM with SHA256, read from the seat's record folder `ks470/` because the READY names them but does not carry them (override TICKET-DRAFT-override.md: 2308 chars, sha256 c8404eafca2790f6 | header True | READY names file True | READY carries text False | cleanroom TICKET-DRAFT-cleanroom.md: 2126 chars, sha256 9441b243a0270097 | header True | READY names file True | READY carries text False; DRAFTS OK: 2 text(s) -> drafted_texts_gate48a.md | the READY carries the texts verbatim: NO (it names the files)).
