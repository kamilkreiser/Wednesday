# gate49b COMMISSION — TWO Secuura PRs, #1357 + #1359 (Seat B 49th, T1 KS-1054), merged by Seat D 1st, + a POST-MERGE AUDIT of #1358 (T2 KS-1380), round 49b

Filled by fill_gate49b.py at 2026-09-30T07:49:13Z from pins_gate49b.json (measured 2026-09-30T07:47:21Z). Wednesday's commission to the drafter, 2026-09-30 (~06:05Z, #1359 added ~06:09Z), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 44 keywords (each as a token).

## The PRs
| PR | ticket | tier | seat | head | parent | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1357 | KS-1054 | T1 | Seat B 49th | `236f9dce38982c17bf5868f3a3ec17c08393d871` | `377989cf3829` | 1 / 13 | 2 (+31/-2) | 71 -> 79 |
| #1359 | KS-1054 | T1 | Seat B 49th | `acac1f5e28ea4c983891dc50d7ed4b08a34d7e39` | `377989cf3829` | 1 / 13 | 4 (+162/-2) | 81 -> 89 |

- develop d8b6c2a7a520ad715417435cde235346c92f7acc (tree eeca25667bb9633e8e7d63c5b8644b4fa98e7b2a). Every PR sits on its merge-base 377989cf3829e46cf47ef957746f01c2f600a370 (#1356's squash; its tree == gate49a's END_TREE) and is 13 behind develop: the move since is 318 path(s), and pin (C) reads it reaching NONE of the 21 kit paths — re-derive that. END_TREE `d485add27eabcbbcfa12242158d14cafd71bb01b` (`6 files changed, 193 insertions(+), 4 deletions(-)`).
- DISJOINT (pin (D)): #1357 x #1359 0 — 0 shared paths; 6 paths, 6 distinct. #1357 and #1359 share two DIRECTORIES (deployment/azure, scripts/__tests__), not a path.
- ORDER-INDEPENDENT (pin (G)/(G2)): the merge order #1357 -> #1359 gives END_TREE `d485add27eab`; the reverse order gives `d485add27eab`; all 2 permutations give the same tree.
- PER-AUTHOR SUBSETS (pin (G2)): Seat B 49th alone (#1357 #1359) -> tree `d485add27eabcbbcfa12242158d14cafd71bb01b`.
- PER-STEP trees in the merge order (pin (F)): #1357 `fc3355d7d6ec68f410b8c3dd9bea0569ad767004` -> #1359 `d485add27eabcbbcfa12242158d14cafd71bb01b` (the last == END_TREE)
- MODES (git ls-tree, at head / alone / chain step / END): check-startup-migrations.sh, deploy.sh, deploy-all.sh 100755; the three suites 100644; all 15 locks 100644; controls `.githooks/pre-push` 100755 and `preflight.sh` 100644 at develop / heads / END — 8 of 8 OK.
- GOLDENS (pin (M)): each golden.diff applied with `git apply --cached` under a temp index to its base 3e3a68260d0e AND to develop gives #1359's 4 blobs byte-for-byte (8 of 8 comparisons BYTE-EQUAL; develop's blob differs from the head for each, the control).
- Pane `QA/Secuura-batch1357`. Report dir `2026-09-30-batch1357-g49b`. ITEM 2 (KS-729) is OUT OF SCOPE (Wednesday, ~06:09Z: handed to Seat B 49th's successor).

## The rulings
- **#1357:** Kam's ruling (a) on `secuura-ks1054-f9282-migration-failure-visibility` ("Keep serving, flag it on /health") quoted verbatim in the PR body (claims C1: verbatim); Wednesday's python3 ruling (absent -> rc 1; present-but-broken -> rc 1; non-JSON -> rc 2).
- **#1359:** Wednesday's ADDENDUM 1 (Seat B 49th): the N-1350-7 rc-1 wording in both callers from the two goldens; message text only.
- **#1358:** Wednesday's ADDENDUM 1 (Seat D 1st): Direction B as one PR after the 1356 merge; READY to gate49b.

## What the gate must check (by name)
1. **The batch shape**: each PR alone clean; the three pairwise DISJOINT; END in the merge order and in the reverse order; each author's subset; the per-step trees; modes and exec bits; the collision census. (CLEAN-MERGE, DISJOINT, END-TREE, ORDER-INDEPENDENT, MODES, EXEC-BITS, COLLISION-CENSUS)
2. **#1357**: the predicate executed on every python3 / body case at develop and head; red-first on macOS + python:3.12-slim (reds exactly P10/P10b, fixtures green); how the callers consume it; the ruling verbatim. (BEHAVIOUR-1357, RED-FIRST-1357, PREDICATE-CONTRACT, CALLERS-READ, RULING-VERBATIM)
3. **#1359**: what each caller prints and counts on rc 0/1/2; bytes == goldens; red-first (M1/N1 red at base, M2/M3/N2/N3 green both sides); no counter / rc change; the message true of every rc-1 path. (BEHAVIOUR-1359, GOLDENS-BYTE-EQUAL, RED-FIRST-1359, NO-COUNTER-CHANGE, MESSAGE-TRUE)
4. **POST-MERGE AUDIT of #1358** (separate, non-merge, T2): the statement verbatim; analytics / billing / governance images BUILD at develop (kyc the previously-green control; the merge's first parent FAILS as the control), the landed 15-lock delta == the PR head, ranges, registry, lock agreement green, legs 6/7/contract rc 0, the four suites (shared built first), tsc NOT a red-proof, the #649 census. (POST-MERGE-AUDIT, MERGED-BEFORE-GATE, IMAGE-BUILDS, LOCK-DELTA-15, LANDED-EQUALS-HEAD, DEPENDENT-RANGES, REGISTRY-TRUE, LOCK-AGREEMENT, AUDIT-LEGS-DEVELOP, SUITES, TSC-NOT-A-RED-PROOF)
5. **The shell runner** at END counts the two new suites (shared built FIRST). (SHELL-RUNNER, SHARED-BUILT-FIRST)
6. **Subjects, bodies, branches, commits**: `Refs <own key>` only; lands <= 92; no closing keyword; bodies line by line. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
7. **The five drafted client comments**, sentence by sentence; one verdict per draft; neither KS-1054 draft repeats or contradicts comment `49aff833`. (DRAFTED-COMMENTS, NO-REPEAT-49AFF833)
8. **Follow-ons**, the fuse count, ITEM 2 out of scope. (FOLLOW-ONS, FUSE-COUNT, OUT-OF-SCOPE)
9. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST, ONE line naming each PR's head, declared subject and per-step tree.

## GO
ONE GO string, the SUBJECT of the GO mail: `GO (Seat D 1st): merge 1357 1359 on gate49b` — Seat D 1st merges #1357 -> #1359 (Wednesday ~07:40Z re-scope). #1358: #1358 was merged by PeterObeden at 07:28:02Z as a merge commit, before any gate. Its audit writes no GO. Per-step trees: PER-STEP trees in the merge order (pin (F)): #1357 `fc3355d7d6ec68f410b8c3dd9bea0569ad767004` -> #1359 `d485add27eabcbbcfa12242158d14cafd71bb01b` (the last == END_TREE). Verdict mail subject: `[QA -> Wednesday] GATE49B #1357 #1359 (Seat D1 merger; T1 KS-1054 broken python3 fails closed + T1 KS-1054 rc-1 wording) + POST-MERGE AUDIT #1358 (T2 KS-1380)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate49b.py -> pin_1.out: END_TREE `d485add27eabcbbcfa12242158d14cafd71bb01b`, 6 of 6 orders agree, 0 shared paths.
- lockdelta_gate49b.py -> lockdelta_1.out: LOCKDELTA PASS: 0 FAIL of 28 checks | 27 moves (1 PROD), 15 locks, base 15 / head 0 disagreeing, nested base 0 / head 0
- overlaps_gate49b.py -> overlaps_1.out: OVERLAPS READ: 11 PR(s) (0 on the kit paths, 11 on the #1358 audit locks) | conflict today 1 | conflict after the batch 1 | empty residue (superseded) 0 | touching @types esc/pg 2 | would re-open a lock disagreement 1
- keyscan_gate49b.py -> keyscan_1.out: KEYSCAN PASS: 12 checks over 2 PR(s), 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- claims_gate49b.py -> claims_1.out: CLAIMS READ: C1 ruling verbatim True | 56 draft sentence(s) (27 NO-INSTRUMENT-WORD) | 6 anchor(s) | 0 problem(s) -> drafts_gate49b.md
- gh_read_gate49b.py -> gh_read_1.out: CENSUS 21 other open PR(s) read | 0 touch a kit path or carry a census key ['KS-1054'] | 0 seat-branch PR(s) disjoint | 0 out-of-scope PR(s) | client-human PRs named: ['1351', '1352', '1353'] | 6 kit paths | 11 AUDIT-OVERLAP PR(s) on #1358's 15 locks (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
- capture_mail_gate49b.py -> capture_1.out: both seats' threads from the plan confirmations to the three READYs, read by id from one listing, verbatim, with TEXT_SHA256; Kam's ruling card verbatim; Wednesday's staged ANSWER / ADDENDUM files for both seats (CAPTURE OK: 49 mails by id (#1357:1/#1359:1/#1358:1 READY), 23 staged file(s), 0 problem(s) -> mail_gate49b_ready.md).
