# gate47 COMMISSION — TWO Secuura PRs: #1349 KS-1374 (T2) then #1350 KS-1054 (T1), each ROUND 1 of its own PR; author and merger Seat B 46th, round 47

Filled by fill_gate47.py at 2026-09-29T14:50:26Z from pins_gate47.json (measured 2026-09-29T14:11:18Z). Wednesday's commission to the drafter, 2026-09-30, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 51 keywords (each as a token).

## The PRs
| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |
|---|---|---|---|---|---|---|---|---|
| #1349 | KS-1374 | T2 | `daab8ff3bff564ee89d4e03cb36a9af04d9b4c9e` | `8c810023f9c9` | `8c810023f9c9` | 1 / 1 | 2 | 71 -> 79 |
| #1350 | KS-1054 | T1 | `8f4f0ef1496304cc853532b686e92bb886fa027d` | `a72149a1a803` | `a72149a1a803` | 1 / 0 | 4 | 72 -> 80 |

- develop `a72149a1a803d802430568254e7fa9afa7029321` (tree `72b5d2e84e9972988dfa00cb623a85770b434310`) = #1348's squash (gate46's GO). #1349 sits on `8c810023f9c9ac060a7aff24f0933ae3b8734479` (**1 commit behind**; the move touches none of its two paths, pin (C)); #1350 sits on develop itself. The two path sets are disjoint (pin (D)); each merges cleanly alone (pin (E)); the chain 1349 -> 1350 and its reverse both give END_TREE `6930599560c93f3a6cd929cc634b537a2eeb2eaf` (pins (F), (G)).
- Recorded modes (pin (H), `git ls-tree`, at head / alone / chain step / END): #1349 aktoRateLimit.ts 100644; #1349 ks1374-n1347-11-scan-target-override.test.ts 100644; #1350 check-startup-migrations.sh 100755; #1350 deploy-all.sh 100755; #1350 deploy.sh 100755; #1350 ks1054_deploy_scripts_read_startup_migrations.test.sh 100644 — all 6 OK.
- THE HOOK (pin (I), (J)): pre-push 100755 ffc25ebc37d4 (IDENTICAL at develop, both heads and END); preflight.sh 100644 270b8913c009 (IDENTICAL at develop, both heads and END); check-package-format.sh 100644 a2a0783d4969 (IDENTICAL at develop, both heads and END). Path class: #1349 0 of 2 path(s) under Blockchain/Dev/ (the preflight FAST-SKIPS, formatting gate only); #1350 4 of 4 path(s) under Blockchain/Dev/ (the preflight TRIGGERS).
- Author and merger Seat B 46th (tmux %74). Pane `QA/Secuura-batch1349`. Report dir `2026-09-30-batch1349-g47`.

## The rulings and the rounds
- #1349 KS-1374 (gate45 N-1347-11, ticketed as a KS-1374 checklist item by gate45's GO) — Kam 16:17:55 / 16:18:57: raise the pacing limit on LOCAL stacks only. One product line: `isLocalScanTarget()` keys on `OVERRIDE_APP_URL || SECUURA_API_URL`, the precedence `scanOptions.ts:98` uses. **TIER 2** (a follow-up whose mechanism gate45 measured; #1347 was T2 in gates 44-45).
- #1350 KS-1054 (gate44 N-1346-2/-3/-4 + gate46 N-1348-6/-7) — Kam option (a), card `secuura-ks1054-f9282-migration-failure-visibility`. A third predicate exit code (rc 2 = PASS-WITH-SKIP), both callers in the same commit, python3 absent FAILS CLOSED (Wednesday 13:07Z), the EMPTY / non-JSON divergence KEPT for Kam. **TIER 1** (a deploy-path RUNTIME change; KS-1054 was T1 in gates 44-46).
- **Each is ROUND 1 of its own PR. The tiering rule governs a NO GO: a round-1 NO GO goes back to the author for round 2; a second NO GO ships the closed instances and tickets the residue.** Whether #1349 / #1350 are "the residue re-opened as its own commission" or a third round on their classes (which would need Kam's word) is carried to the gate as CLASS-ROUND-1349.

## What the gate must check (by name)
1. **#1349's skipped preflight**: the hook read AT THE HEAD, its 15 legs enumerated, every leg runnable offline run at the head and END, each MEASURED / NOT MEASURED with the reason; the formatting gate; `audit:gate` + `audit:locks` re-run. (HOOK-SKIPPED-LEGS-1349, FORMAT-GATE-1349, AUDIT-LEGS-1349, AUDIT-BASELINE-CLEANUP-NOTE)
2. **#1349's akto suite** at develop / head / END (seat: 93/1654 -> 94/1663), red-first 4 failed / 5 passed, the tamper arm with a unique anchor (`const raw = ` occurs twice), lint + prettier with failing controls; the 7500 / 1500 numbers COMPUTED BY RUNNING THE CODE. (SUITE-1349, RED-FIRST-1349, TAMPER-1349, NUMBERS-FROM-CODE-1349, NOT-COVERED-1349)
3. **#1350's KS-1054 suite on macOS bash 3.2 AND python:3.12-slim** (`docker run --rm --network none`, source READ-ONLY, versions printed in the same run), develop / head / END; the whole shell runner (seat 61/0/0); NOT MEASURED said plainly. (SUITE-1350-MACOS, SUITE-1350-GNU, RED-FIRST-1350, RED-AT-BASE, GREEN-AT-HEAD, WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, SUITES-AT-END)
4. **The caller cells**: re-create "predicate returns rc 2, callers untouched" and prove R1 red AND the real deploy.sh failing a deploy over ABSENT there; the hardened E1 both ways; R8 EXECUTES deploy-all.sh's call site (the skip-call tamper reds it); python3 absent fails closed rc 1 in both scripts. (CALLER-CELLS-1350, ABSENT-STILL-PASSES-1350, N-1348-6-BOTH-WAYS, R8-EXECUTES, PYTHON3-ABSENT-FAILS-CLOSED, N-1348-7-COMMENT-FIXED, OTHER-CALLERS-1350)
5. **The eight tamper arms**, each red on its named cell, anchors unique (`return 1` twice in deploy.sh), files restored byte-equal. (TAMPER-ARMS-1350, TAMPER-UNIQUE-ANCHOR, TAMPER-RIGHT-REASON, RESTORE-SHA256)
6. **The deploy path, stubs only**, per body shape per script per tree, beside the PR body's own table; the kept EMPTY / non-JSON divergence and N-1346-9 carried for ruling, not required. (DEPLOY-PATH-TABLE-1350, EMPTY-NONJSON-DIVERGENCE, N-1346-9-OUT-OF-SCOPE)
7. **The merge**: #1349 over develop (1 behind), then #1350 over that; END_TREE `6930599560c93f3a6cd929cc634b537a2eeb2eaf`; disjoint paths; recorded modes 100755 x3 / 100644 at head and END; the census of other open PRs. (CLEAN-MERGE, END-TREE, OVERLAP-MEASURED, MODES)
8. **Both drafted ticket texts** checked claim by claim as ROWS with evidence and returned POST AS-IS / POST AMENDED (with the text) / DO NOT POST; when each may be posted. Nothing is posted by anyone until the gate has read it. (DRAFTED-COMMENTS-CHECKED, DRAFT-POST-TIMING)
9. **Every test that references a changed file**: the drafter's census 0 file(s), re-derived and run. (CENSUS-TESTS-RUN, CENSUS-LISTED)
10. **Subjects** key-scanned (own key only, no `(#n)`), landed <= 92, **TRUE of the diff**; bodies `Refs KS-xxxx`, no closing keyword; the PR bodies' factual lines. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS, HOOK-LINE-CITE)
11. **The tiering and the class round** (TIERING, CLASS-ROUND-1349), DISK-ENOSPC, and **REPORT-HASH-LAST**: the report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail, whose body carries the report's sha256.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 46th): merge 1349 1350 on gate47` — Seat B 46th merges #1349 then #1350. If only one PR may merge, the gate writes the one-PR form. Verdict mail subject: `[QA -> Wednesday] GATE47 #1349 #1350 (Seat B46 author and merger, round 47; T2: KS-1374 pace keyed on the scan target; T1: KS-1054 a skipped migration check stops reading as a pass)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate47.py -> pin_1.out: both PRs clean alone and chained, either order; END_TREE `6930599560c93f3a6cd929cc634b537a2eeb2eaf`.
- testrefs_gate47.py -> testrefs_1.out: 0 test file(s) — 
- keyscan_gate47.py -> keyscan_1.out: KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- linear_read_gate47.py -> linear_read_1.out: LINEAR READ OK: KS-1374 In Progress, 5 comment(s), N-1347-11 checklist line(s) 1 (unticked 1), dc9212b5 dc9212b5-aaec-42fc-9733-ba57737d5ae0, 0 created AFTER gate46 | KS-1054 In Progress, 6 comment(s), raise comment b82bebb3-2c62-435e-b39c-24dc7a246ca4, 0 created AFTER gate46 -> linear_gate47.md
- drafts_gate47.py -> drafts_1.out: both texts VERBATIM with TEXT_SHA256 (the KS-1374 checklist tick for #1349 and the KS-1054 facts comment for N-1348-9 + #1350), extracted from the captured READY by drafts_gate47.py (KS-1374 #1349: 555 chars, sha256 fe7ba98c45550129 | KS-1054 #1350: 595 chars, sha256 3a5227e14526fad8; DRAFTS OK: 2 text(s) -> drafted_texts_gate47.md | READY == seat file: True).
