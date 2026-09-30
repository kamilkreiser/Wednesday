# gate49a COMMISSION — ONE Secuura PR: #1356 KS-1378 (T1, round 1), ITEM A; author and merger Seat B 49th, round 49a

Filled by fill_gate49a.py at 2026-09-30T04:29:44Z from pins_gate49a.json (measured 2026-09-30T04:16:31Z). Wednesday's commission to the drafter, 2026-09-30 (~04:00Z), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 29 keywords (each as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1356 | KS-1378 | T1 | `52dadb07f70d20da8f201b518eba4ebff05c8455` | `3e3a68260d0e` | `3e3a68260d0e` | 1 / 0 | 18 (+90/-90) | 72 -> 80 |

- develop `3e3a68260d0ef541b2410d323849d2639ddd6941` (tree `0693c2b391b6e0086524c18461c22d72f89a84f1`) = #1355's squash. 0 behind. END_TREE `9b61e858210de7dce3a76f7cfa24e7cb99bc231b` (`18 files changed, 90 insertions(+), 90 deletions(-)`).
- MODES (git ls-tree): all 18 PR paths 100644 at head / alone / END; control `.githooks/pre-push` 100755 at develop / head / END.
- IDENTICAL at develop / head / END: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009, `lockfile-cleanroom.sh` 518bffeeaf4a, `baseline-contract.mjs` 16ad64fd42b0, `audit-baseline.json` 6fc1e1c95ca7, `audit-gate.mjs` 8e236ee70ce1, `audit-locks.mjs` aff23b0420ce, `advisory-fetch-stub.mjs` 29c9fc48f328, `gate-exit-codes.test.mjs` 40079f6fb41e, `Dockerfile` 60485f4a67ac, `Dockerfile` e8eb7468d93d.
- Merger Seat B 49th (tmux %81; the author). Pane `QA/Secuura-batch1356`. Report dir `2026-09-30-batch1356-g49a`.

## The ruling
- **Wednesday's ANSWER plan (2026-09-30 13:45 AEST):** ITEM A, an in-range lock refresh measured then raised as ONE PR, `Refs KS-1378`, locks only, no acceptance; T1 (production entries in shipped images). "The 09-09 baseline grant is NOT used." Its STOP conditions (a major; mobile; a baseline row; anything in a shipped tree beyond the named packages) are the gate's to rule NOT fired.
- **The claim** (status itemA measured, 03:56Z): 18 locks, +102/−102, 30 moves, ADDED 0 / REMOVED 0 per lock; `npm update <pkg> --package-lock-only --ignore-scripts` in `node:24-alpine`, npm 11.19.0 (root-mounted for systemTest/akto and performance); a pristine control at the same SHA moved nothing; mobile untouched.

## What the gate must check (by name)
1. **The diff re-derived**: exactly 18 locks; per lock every changed entry (version, resolved, integrity, flags); ADDED/REMOVED 0; every moved version inside every dependant's declared range; integrity == the registry's, with a deliberately wrong one as the control. (LOCK-DELTA-18, DEPENDENT-RANGES, REGISTRY-TRUE)
2. **The refresh reproduced** in a clean container from develop, same npm; `cmp` to the head; the pristine control. (REPRODUCE-REFRESH, PRISTINE-CONTROL)
3. **The audit legs** at develop (6/7 rc 1 with exactly the six) and head (contract/6/7 0/0/0); each id absent per id; each leg still refuses a planted advisory (the offline stub); no baseline row. (AUDIT-LEGS-BASE-HEAD, SIX-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW)
4. **Runtime reach**: mcp-server and nft-certificate built at develop and head under the gate's own compose project names, build only; the served trees' resolved versions; whether the root lock reaches any image. (RUNTIME-REACH, ROOT-LOCK-CONSUMERS)
5. **Suites** for mcp-server and nft-certificate before/after with counts; every test naming a changed path. (SUITES, SHARED-GUARD-TESTS)
6. **`npm ci --ignore-scripts` at the head**: root + the moved standalone locks (or a named representative set). (NPM-CI-HEAD)
7. **The merge, END, modes, and the collision census** of every open PR on the 18 locks — reported, not refused. (CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS)
8. **Title, body, branch, commit**: `Refs KS-1378` only; subject lands ≤ 92; no closing keyword; the body's claims line by line; the squash subject declared WITHOUT `(#n)`. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
9. **Follow-ons, reported**; the fuse count. (FOLLOW-ONS, FUSE-COUNT)
10. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 49th): merge 1356 on gate49a` — Seat B 49th merges #1356. Verdict mail subject: `[QA -> Wednesday] GATE49A #1356 (Seat B49 author and merger, round 49a; T1 KS-1378 in-range lock refresh: brace-expansion, fast-uri, ip-address in 18 locks)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate49a.py -> pin_1.out: END_TREE `9b61e858210de7dce3a76f7cfa24e7cb99bc231b`. The measured numstat is +90/-90 over 18 locks; the seat claimed +102/-102.
- lockdelta_gate49a.py -> lockdelta_1.out: LOCKDELTA PASS: 0 FAIL of 118 checks | base 3e3a68260d0e head 52dadb07f70d | 18 locks, 30 moves (7 PROD), 36 dependant range(s) | numstat +90/-90 | sha256 of the moved-set c6489e4a1e0a6f97
- reach_gate49a.py -> reach_1.out: REACH READ: tree 52dadb07f70d | 11 image Dockerfile(s) copy a moved lock | root-lock copies 0 | 5 test file(s) name a changed path, 5 name the generic lock | controls hold
- overlaps_gate49a.py -> overlaps_1.out: OVERLAPS READ: 10 PR(s) | conflict today 1 | conflict after ITEM A 1 | empty residue (superseded) 0 | touching the moved packages 0
- keyscan_gate49a.py -> keyscan_1.out: KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate49a.py -> gh_read_1.out: CENSUS 23 other open PR(s) read | 10 touch a kit path or carry a census key ['KS-1378'] | client-human PRs named: ['1351', '1352', '1353'] (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
- capture_mail_gate49a.py -> capture_1.out: the thread from the plan confirmation to the READY, read by id from one listing, verbatim, with TEXT_SHA256, and Wednesday's ANSWER files for Seat B 49th (CAPTURE OK: 10 mails by id (1 READY), 0 problem(s) -> mail_gate49a_ready.md).
