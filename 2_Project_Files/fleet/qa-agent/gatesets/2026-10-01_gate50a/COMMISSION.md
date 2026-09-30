# gate50a COMMISSION — ONE Secuura PR: #1363 KS-1378 (T1, round 1), ITEM A; author and merger Seat B 51st, round 50a

Filled by fill_gate50a.py at 2026-09-30T21:36:46Z from pins_gate50a.json (measured 2026-09-30T21:28:38Z). Wednesday's commission to the drafter, 2026-10-01 (~07:25 AEST), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 32 keywords (each as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1363 | KS-1378 | T1 | `9e84e1fabafe1ecc1963953051759c4038f88db2` | `4f18c59a89db` | `4f18c59a89db` | 1 / 0 | 4 (+19/-19) | 75 -> 83 |

- develop `4f18c59a89db16cb8b06b7850aeb64e6f81f95ee` (tree `25e343e8141241ae6f617b92c3b3f612c28a2c8a`) = #1361's merge. 0 behind. END_TREE `2a874956406ca974f3090b24392f6dbfdc8bc4d6` (`4 files changed, 19 insertions(+), 19 deletions(-)`). Three instruments agree on it (end_tree_crosscheck_1.out): merge-tree + commit-tree over develop, the head's own tree (parent == develop), and GitHub's `refs/pull/1363/merge` tree; develop's own tree 25e343e81412 is the control that differs.
- MODES (git ls-tree): all 4 PR paths 100644 at head / alone / END; control `.githooks/pre-push` 100755 at develop / head / END.
- IDENTICAL at develop / head / END: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009, `baseline-contract.mjs` 16ad64fd42b0, `audit-baseline.json` 6fc1e1c95ca7, `audit-gate.mjs` 8e236ee70ce1, `audit-locks.mjs` aff23b0420ce, `lock-discovery.mjs` 3dd903b527f2, `advisory-fetch-stub.mjs` 29c9fc48f328, `kyc/Dockerfile` 8e752ac3f19a, `admin/Dockerfile` 87c05e8512c0, `verifier/Dockerfile` a47940c5107b, `issuer/Dockerfile` 67d5abc68560.
- Merger Seat B 51st (tmux %86; the author). Pane `QA/Secuura-batch1363`. Report dir `2026-10-01-batch1363-g50a`.

## The ruling
- **Wednesday's ANSWER route (a) (2026-09-30T20:54Z):** ITEM A, ONE in-range lock-refresh PR from develop 4f18c59a89db, no manifest change, its OWN gate (gate50a, T1) because it unfreezes every push, Peter's included. Route (b) (baseline the batch) REFUSED. If any advisory survives, STOP and mail. **ANSWER 20:59Z:** the lock set is FOUR; `Refs KS-1378` on the branch; the NEW ticket text is read by gate50a and filed on the GO, before the merge.
- **The claim** (the READY, 21:21:14Z): 4 locks, +19/−19, 5 moves (root 2, admin / verifier / kyc 1 each), ADDED 0 / REMOVED 0; `refresh46.sh` in `node:24-alpine`, npm 11.19.0; a pristine control at the same base; legs 6 / 7 / contract rc 1 / 1 / 0 at develop and 0 / 0 / 0 at head; 13/13 advisories cleared; 26 baselined before and after; kyc suite 33/33 both sides; four images built (build only).
- **The drafter's addition, measured:** each axios entry also moves one range line, `form-data` `^4.0.5` -> `^4.0.6` (axios 1.20.0's own manifest); form-data 4.0.6 is already resolved in all four locks.

## What the gate must rule (by name)
1. **The four lock diffs re-derived and reproduced**: containerised `node:24-alpine` regen against a pristine control at the base, byte-identical to the PR; ONLY axios 1.18.1 -> 1.20.x and dompurify 3.4.13 -> 3.4.16 moved (plus integrity / resolved); MOVED / ADDED / REMOVED per lock; the form-data range line ruled. (LOCK-DELTA-4, OWN-DEPENDENCIES, DEPENDENT-RANGES, REGISTRY-TRUE, REPRODUCE-REFRESH, PRISTINE-CONTROL)
2. **Legs 6 / 7 / audit:contract** at develop (rc 1 / 1 / 0) and head (rc 0 x3), with a refusal control per leg. (AUDIT-LEGS-BASE-HEAD, THIRTEEN-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW)
3. **Each of the 13 advisories mapped** to the lock entry that cleared it, re-derived. (ADVISORY-MAP)
4. **Consumers**: kyc / admin-frontend / verifier-frontend / issuer-frontend built develop vs head (build only); the served axios in the kyc image; the kyc suite; the root lock's workspace consumers (issuer at least); `npm ci` at the head. (RUNTIME-REACH, ROOT-LOCK-CONSUMERS, SUITES, NPM-CI-HEAD)
5. **mobile/secuura-app untouched** (KS 769). (MOBILE-UNTOUCHED)
6. **The merge, END, modes, the census** (Peter's #1360 touches the root and kyc locks: reported). (CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS)
7. **The PR text**: subject, body, the Test Evidence block — every factual line checked against the head. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
8. **The proposed NEW ticket text** (client-visible): POST AS-IS / POST AMENDED (full amended text) / DO NOT POST, sentence by sentence against its sources. (NEW-TICKET-TEXT)
9. **The gatelines VERDICT wording**: which state of gatelines46.py is the clean one — a tooling finding, not for this PR. (GATELINES-VERDICT)
10. FUSE-COUNT, TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST. The change is SMALL: a proportionate pass (usage 76% of the weekly allowance).

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 51st): merge 1363 on gate50a` — Seat B 51st merges #1363. Verdict mail subject: `[QA -> Wednesday] GATE50A #1363 (Seat B51 author and merger, round 50a; T1 in-range lock refresh: axios 1.20.0 in 4 locks, dompurify 3.4.16 in the root lock; the new-ticket text ruled)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate50a.py -> pin_1.out: END_TREE `2a874956406ca974f3090b24392f6dbfdc8bc4d6`. The measured numstat is +19/-19 over 4 locks; the seat claimed +19/-19.
- lockdelta_gate50a.py -> lockdelta_1.out: LOCKDELTA PASS: 0 FAIL of 50 checks | base 4f18c59a89db head 9e84e1fabafe | 4 locks, 5 moves (5 PROD), 9 dependant range(s) | numstat +19/-19 | sha256 of the moved-set 0fbcebd211492cb8
- reach_gate50a.py -> reach_1.out: REACH READ: tree 9e84e1fabafe | 3 image Dockerfile(s) copy a moved lock | root-lock copies 0 | 7 test file(s) name a changed path, 7 name the generic lock | controls hold
- overlaps_gate50a.py -> overlaps_1.out: OVERLAPS READ: 11 PR(s) | conflict today 1 | conflict after ITEM A 1 | empty residue (superseded) 0 | touching the moved packages 0
- keyscan_gate50a.py -> keyscan_1.out: KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate50a.py -> gh_read_1.out: CENSUS 22 other open PR(s) read | 11 touch a kit path or carry a census key ['KS-1378'] | client-human PRs named: ['1351', '1352', '1353'] (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
- capture_mail_gate50a.py -> capture_1.out: the thread from the LAUNCH BRIEF (id + sha256 only) through route (a) and the READY to the latest mail at capture time, read by id from one listing, verbatim, with TEXT_SHA256 (CAPTURE OK: 18 mails by id (1 READY), 0 problem(s) -> mail_gate50a_ready.md).
