auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA agent -> Wednesday · TIER 1 GATE ROUND 1 of 2 · Secuura/Blockchain PR #1032 (KS-1194) · closed 2026-09-17 23:36:06 AEST

VERDICT: NO GO on `70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039` as the delta over develop `0a2b1603f`, AND on the merged tree `0296c11d879fd9a814839ac12b3c63d8f0be63d2` (then-current develop `732c13459d76f5b05ade94bb91de7e47585b0e7d`). Cause: F-1 (D2) Major, reachable on the approve path #1032 changed (your pre-launch ruling). Round 1 of 2: back to Seat A for one fix round. A GO would not have authorised a merge either; the merge waits for Kam's tap.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/report.md (NOT-TESTED.written-first.md at 23:16:30, before any run; evidence/ + evidence/scripts/)
Real-browser half of tier 1: does not apply (only services/auth users.ts + one vitest file; no rendered surface).
0 Blocker · 1 Major (F-1) · 3 Minor (F-2, F-3, F-5 = D1) · 1 Polish (F-4) · 6 Records · 1 QA self-correction (SC-1).

LEAD
- Item 1: every THROWING save answers 503 (infra: ECONNREFUSED and the pg-pool `timeout exceeded when trying to connect`) or 500 (22001), never 200, on submit, approve and reject, at head = merged. No row is written and nothing is kept in memory. develop answers 200 on all of them and its approve raises the level over PENDING (#1015 F5 reproduced). 59 probe rows × develop/head/merged; the real userRoutes + userRepo + errorHandler + isInfrastructureDbError over a db stub; 30/30 rows shared with the drafter identical.
- D2 = F-1 MAJOR, MEASURED reachable. The level UPDATE lands, then updateUser's read-back fails (pool timeout / ECONNREFUSED / 22001 / empty) -> head 503, row restored PENDING (reviewed_by/at null), level ENHANCED (merged same).
  Admin's next move: a REJECT answers 200 and stores REJECTED over ENHANCED (a permanent contradiction); a re-approve heals it (200 APPROVED). The subject reads ENHANCED with PENDING and a new submit gets 400 "already pending".
  What the read-back needs (READ): db.ts `query()` takes a fresh pooled connection and its own transaction per statement, with a 2 s acquisition timeout (KS-254). KS-253 measured that acquisition failure on 42/266 storm logins. develop reached the same end state on the throwing shapes; #1032 widens it on the empty read-back.
- D3 = F-2 MINOR. The residual line (`error, requestId, userId`) is FALSE when the level was raised: A-DOUBLE-READBACK stores APPROVED + ENHANCED and the line says "the level was not raised ... at an unchanged level". The single-failure line "raising the verification level failed" is also false on every read-back row (NEW). The null path (A-UPD-ZERO) has no error line naming the request (warn with userId only). No line carries the target level.
- D1 = F-5 MINOR, TICKET-ON-KS-1194 (per your ruling). develop = head = merged: M-UPD-ZERO answers 200 APPROVED "upgraded to STANDARD" with the level still basic; M-UPD-INFRA/OTHER 500; M-READBACK-* 503 with the level raised. #1032 did not make it worse.

ITEMS
1. Census: see LEAD. Paths re-derived: saveVerificationRequest at 4 call sites (:1296 submit, :1366 approve, :1378 restore, :1394 reject); level writes at :1277 MFA (untouched), :1372 approve (changed), and :797 admin PATCH / :1079 / :1114 MFA enable-disable (untouched, READ only). FAIL criterion (200 over a THROWN store, or 200 approve with the level raised and the row not APPROVED, on a changed path): 0 rows -> no Blocker. D5 0-row rows (S-ZERO, A-SAVE-ZERO 200 with row PENDING + level raised, R-SAVE-ZERO) are stub-only.
2. Ordering: INSERT:APPROVED before PREAUTH/UPDATE (C2 holds). The restore clears reviewed_by AND reviewed_at and answers 503 on a throw or null (holds), but it also fires after a LANDED update (F-1). The residual line is present but not sufficient for an operator (F-2).
3. House helper: a COPY, not updateUserOrThrow (no platform-scope variant). The response is the generic infra 503 (no forbidden cause). The LOG asserts the forbidden cause (F-2). Q-503-HELPER-WORDING (the helper's "could not be confirmed" wording) reds 0 cells.
4. Tampers: 24 rows on the whole auth suite at 60 s, 24/24 as predicted, 0 VOID. Each row: tsc 0, (65, 773, 0) asserted, 0 reds outside, all AssertionError, sha-restored + diff --quiet 0.
   Seat (parsed from ROWS, never executed): T0 0 · RP-DEV 9 · REORDER 4 · SWALLOW 5 · MEMFIRST 1 · NORESTORE 3 · NOLOG 1 · TI 0 = C6.
   Drafter 8 exact (6 zero-red with consequences re-measured; X-SAVE-INFRA-AS-500 3; X-RESTORE-REJECTED 2).
   QA: Q-RAISED-INIT-TRUE 1 · Q-NULL-AS-OK 3 · Q-MEM-IN-CATCH 1 · Q-OTHER-AS-503 1 · Q-503-HELPER-WORDING 0 · Q-RAISE-LOG-NOT-RAISED 0 (logs "NOT raised" with the level ENHANCED) · Q-ROWCOUNT-CHECK 0 (the hardening closes D5 on the stub, breaks 0/773) · Q-REJECT-INPLACE 0 (no consequence found).
   Structural gap (F-3): the ks1194 cells mock userRepo wholesale and their `throw` means "not raised", so no cell can express F-1.
5. Merge-in: 29d9f90fa -> c896e5492, c82f5edd5 -> 691d29189, 70ee7b6c0 -> 1111602c4, all EQUAL, 0 conflicts, brought = develop delta 7/19/2. 0a2b1603f..head = users.ts +67 -31 + the test +219. patch-id c1264e780015 both ways; the test is byte-identical fix = head; auth subtree f822c95f8 (c82f5edd5 = head); shared dbd72dea0 everywhere.
   develop moved to 732c13459 (bb848b828 #1030, 27e53ec3a #1029, 732c13459 #1031): 47 files, 0 GUARDED hits, auth src unchanged -> merged tree 0296c11d8 (drafter beee976dd superseded).
6. Checks (load 13.9-18.7): develop 64/762, head 65/773, merged 65/773, 0 failed at DEFAULT and at 60 s; ks949 alone 30/30 both trees (the READY's 771/773 = load). Project tsc rc 0 x3; ks1194 not in that program (597 files).
   Test-including program (scratch config OUTSIDE services/auth): 39 error lines in 23 test files on develop AND head, an identical per-file map, 0 in ks1194 (listed), plant +1. Pre-existing baseline; the drafter's 37/21 came from an in-root config (R-5, instrument).
   eslint 0/0 users.ts both trees, 0/0 the test; the control fires 3 no-unused-vars at WARN, rc 0 (a 0-error rc proves only that no error-level rule fired).
7. Callers: none in repo depends on 200 from a failed save (only systemTest schemathesis test_user_admin_isolation.py, a role gate). OpenAPI: 0 of 309 paths contain verification (control /api/users/me: 1) -> undeclared 503/500 = R-2 contract gap. generate-openapi --check: CHECK PASS.
8. Linear/GitHub at 23:25 and again at 23:33 (immediately before this mail): attachmentsForURL(pull/1032) = KS-1194 contributes only (controls pull/1018 -> KS-1050, pull/99999 -> 0). 0 closing phrases in title, body and 4 commits (controls 1/1/0). Body has `Refs KS-1194` and `## Test Evidence`. KS-1194 In Progress, and stays In Progress on merge (§5f).
9. Schemathesis/Akto: NOT REQUIRED. Both routes are outside the published spec (0/309) and the defects need a store fault between two statements that no generator can inject; the deterministic in-process probe is the right instrument (a real-Postgres drill is the next level, NOT COMMISSIONED).
10. See the table below.

CLOSED / STILL OPEN / NEW
- KS-1194 = #1015 F5, a throwing save answered 200: CLOSED (submit, approve, reject), head + merged.
- F5's state clause via the read-back = F-1 Major: STILL OPEN (widened on -EMPTY) -> NOT SHIPS-WITH, NO GO, fix round 1.
- D3 = F-2 Minor: STILL OPEN + NEW (the single-failure line, the null path) -> fix with F-1.
- D6 = F-3 Minor: STILL OPEN + NEW (the mock gap; 2 QA rows) -> SHIPS-WITH the fix round (a real-updateUser cell for F-1 required).
- F-4 Polish NEW: a non-infra level-update error answers 503 (develop 500) -> Record/optional.
- D1 = F-5 Minor: STILL OPEN, pre-existing -> TICKET-ON-KS-1194.
- D5 = R-1: STILL OPEN, READ-unreachable (upsert with no WHERE; the table is in no RLS array and has no policy/trigger/rule) -> Record.
- D8 = R-2: STILL OPEN -> Record. D7 = R-3: load, not the PR -> Record. R-4: other level writes untouched -> Record.
- KS-1018 item 3 (memory-only path) = R-6: STILL OPEN (NODB approve/reject 200) -> TICKET (KS-1018).
- SC-1 QA self-correction: v1 probe shared the plan's insert array by reference; the 4 A-DOUBLE-READBACK follow-ups were wrong in v1; fixed (v2), all 59 rows re-run; only those rows changed.

FIX-SHAPE for Seat A (prose; QA writes no code): either (a) one transaction for the level UPDATE + the request upsert (a repo function on one client inside transaction() with the subject-tenant GUC), or (b) no blind restore: on a throw/null, re-read the level under platform scope; restore PENDING only when the level is confirmed unchanged, keep APPROVED when it reads the target, and when unreadable keep APPROVED and answer the helper's "could not be confirmed" 503 with {requestId, userId, targetLevel}. Regression cell over the REAL updateUser (ks1050 pattern): UPDATE rowCount 1 then the read-back throws `timeout exceeded when trying to connect` -> NOT (row PENDING AND level raised), and a following reject cannot yield REJECTED over a raised level.

PREDICTION SLIPS: drafter D2 Minor / GO WITH FINDINGS -> measured Major / NO GO; drafter D3 missed the single-failure line; drafter tsc 37/21 vs 39/23 (instrument). READY C2/C3 incomplete, C7 load-dependent. QA: SC-1.

NOT TESTED (equal prominence): a real Postgres (F-1 reachability is READ + a stub fault of the documented shape; -EMPTY and every 0-row row are stub-only); a fix cell (prose only); multi-replica memory; api-gateway passthrough and out-of-repo callers; concurrent reviews; admin PATCH / MFA enable-disable level writes (READ); a DEK failure on the read-back; vitest 4.1.11; tampers on the merged tree (not required: 0 guarded hits); Schemathesis/Akto/Playwright/k6/stack/browser (NOT COMMISSIONED); the seat's tamper JSONs byte-for-byte.

BOUNDS (Secuura checkout, read verbs only):
- START 23:17:18: porcelain 0 · config f9ef2cb7e4b9fa5a · refs 942 · worktrees 112 · branch feature/ks-597-b-caller-scoped-externalref · auth .vite [vitest] · develop 732c13459 · pull/1032 70ee7b6c0
- MID 23:27:06: 0 · same · 943 · 112 · same · same · 732c13459 · 70ee7b6c0
- CLOSE 23:33:40: 0 · same · 944 · 112 · same · same · 732c13459 · 70ee7b6c0
Refs moved by another session (nothing attributed). Listeners: START 19 LISTEN / 0 login_stub (1 node listener = another gate's drafter1034); CLOSE 17 LISTEN / 0 login_stub / 0 node listeners; my probe servers bound 127.0.0.1:0 and closed in afterAll; nothing needed a SIGTERM. docker info rc 0 (not used, no container).

MERGE ADDENDUM — HELD (NO GO), recorded for the fix round: "on Kam's tap only: squash `70ee7b6c0` onto develop `732c13459d76f5b05ade94bb91de7e47585b0e7d` (merged tree `0296c11d879fd9a814839ac12b3c63d8f0be63d2`; drafter `beee976dd`) — NOT AT THIS HEAD: NO GO, fix round 1 of 2; #1032 attaches to KS-1194 only, linkKind `contributes`, no closes; KS-1194 stays In Progress on merge (§5f: live sweep owed); equality targets after the squash: users.ts `8299a2558` / ks1194 test `bc8f924c3` (will change with the fix); auth vitest 64/762 at develop -> 65/773 at head -> 65/773 merged (measured on 0296c11d8); dispositions: F-1 Major NOT SHIPS-WITH (fix round), F-2 Minor fix with F-1, F-3 Minor SHIPS-WITH the fix round, F-4 Polish Record, F-5 (D1) Minor TICKET-ON-KS-1194, R-1..R-6 Records; NEW: F-1 reachability via the pool-acquisition timeout on the read-back + reject -> REJECTED over a raised level, F-2 single-failure line, F-3 mock gap, F-4; Records for KS-1194's facts comment at merge: the stated residual holds only when the level update did not land and its line is false when it did (F-2), level raised with the row PENDING via an unconfirmed read-back is reachable and blocks this head (F-1), the MFA auto-approve answers 200 APPROVED over a 0-row UPDATE (F-5, TICKET-ON-KS-1194), the 0-row upsert is READ-unreachable (R-1), the undeclared 503/500 (R-2), non-infra level-update errors answered 503 (F-4)."

Escalation candidates for Wednesday (QA does not act on them): none needs a push. The fix round goes to Seat A; D1's part-2 PR sits on KS-1194.
Findings-only: nothing fixed, pushed, commented, filed or merged; nothing to Peter or Stuart.
