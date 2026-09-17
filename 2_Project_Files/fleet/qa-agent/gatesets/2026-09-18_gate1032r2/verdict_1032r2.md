SUBJECT: [QA -> Wednesday] TIER 1 GATE #1032 ROUND 2 (KS-1194) 430672697 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-17T15:57:36.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
QA agent -> Wednesday · TIER 1 GATE ROUND 2 of 2 (DELTA) · Secuura/Blockchain PR #1032 (KS-1194) · mail built Fri 18 Sep 2026 01:57:34 AEST

VERDICT: GO WITH FINDINGS on `4306726977b55171a7c8c0eb5e42de078587a725` as the delta over round 1 `70ee7b6c0` and over develop `3961c2add`, AND on the merged tree `522fc6606d8fbc7bad760ede926deefa78bb4679` (then-current develop `3961c2add8e1637b32e638f8f0952c328c00833e`, unmoved through 01:54:59; develop is an ancestor, so merged tree = head tree). A GO WITH FINDINGS goes to Kam as a card (https://github.com/Secuura/Distributed_Secuura/pull/1032 @ 430672697). It is NOT a merge authorisation: the merge is Kam's tap.
Round 2 of 2: if you or Kam hold N-1 (below) as Major under the retry-heals clause, the cap applies: the CLOSED instances ship and N-1 is ticketed. The measured case against that premise is in §4 of the report.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1194-1032-430672697-tier1-r2/report.md (NOT-TESTED.written-first.md mtime 01:37:52, before the first run at 01:39:20; evidence/ + evidence/scripts/ + evidence/src/)
Real-browser half of tier 1: does not apply (users.ts + two vitest files; no rendered surface).
On #1032: 0 Blocker · 0 Major · 2 Minor (N-1 NEW, F-3) · F-4 Record · Records. Escalation candidates (pre-existing, independent TICKETs): E-1, N-2. 1 QA self-correction (SC-R2-1).

LEAD (items 1-3)
1. F-1 CLOSED wherever the re-read reads the row the UPDATE wrote. MEASURED on the real route + real userRepo over a db stub, head / r1 / develop x NODE_ENV test and production, 75 rows per tree (234/234 of the drafter's rows identical).
   - Read-back pool timeout / ECONNREFUSED / 22001 / empty, and an UPDATE that commits then loses its connection: head 200 APPROVED · level enhanced · one true warn line. The next reject answers 400 "Request already APPROVED" (r1: 503 PENDING over enhanced, then 200 REJECTED over enhanced).
   - test = production on every ciphertext row.
   - Positional pool-fault census (every single fault, consecutive pair and fail-ok-fail pair over the first 8 statements, 21 plans): fail-OPEN states (level raised under a non-APPROVED request) head 0, r1 2, develop 6 (3 of them 200). Fail-safe states (APPROVED over basic) head 4, r1 2.
   - Still open only on a stale re-read (a per-tenant DB): 503 PENDING over enhanced, then reject gives REJECTED over enhanced, on all three trees. Record (Q3).
2. Both stated residuals are REACHABLE and leave APPROVED over an UNRAISED level. A retry answers 400; the subject's resubmit is the only recovery.
   - (ii) not landed = N-1. Pre-auth lookup (or UPDATE) + re-read both fail to acquire → 503 "Verification approval could not be confirmed. Please retry — if you already succeeded, you may not need to." · APPROVED · basic. Retry 400, reject 400, subject GET BASIC ['APPROVED'], resubmit → 200 PENDING → approve → enhanced.
   - The drafter's "r1: PENDING" row gave r1 ONE fault (r1 never consumes the re-read fault). With the SAME two consecutive faults (POS-3+4, POS-4+5, Q-R1SHAPE) r1 stores the identical APPROVED over basic, 503, retry 400; the round-1 report measured it too (A-UPD-INFRA-RESTORE-INFRA).
   - New at head: (a) deterministic unreadable rows. A plaintext-PII row under NODE_ENV production (SYSTEM_ADMIN review only; ORG_ADMIN 500s before any save on every tree) and a destroyed subject DEK (stub): r1 PENDING, head APPROVED over basic with retry/reject 400. (b) The "already succeeded" wording plus the 400 "already APPROVED" steer the reviewer to a false belief.
   - (ii) landed: consistent (APPROVED · enhanced; retry 400 is true). Record.
   - (i): fail → ok → fail (POS-3+5, POS-4+6, RI-*) → 503 generic · APPROVED · basic, 2 true lines, retry/reject 400, resubmit recovers. r1 reached the same end state by fail-fail. TICKET-ON-KS-1194 (Q2).
   - N-1 GRADE: MINOR. It is fail-safe (no level granted). It needs a correlated double pool failure or an already-broken row. Round 1 reached the same stored state with the same faults. One true error line {requestId, userId, targetLevel, error, readError}. Graded with Q4 (Q1 + Q4).
3. Pool routing. MEASURED on the REAL db.ts + REAL TenantPoolManager, pg faked, RLS MODELLED.
   - S (MULTI_TENANCY unset = the bicep auth container, READ): all on db.ts-pool/secuura. UPDATE and read-back GUC tenant, re-read GUC platform → same row; head 200 on a read-back timeout, reject 400.
   - M1 (enabled, no per-tenant DB): UPDATE and read-back on tm-default/secuura with GUC NONE; re-read on db.ts-pool platform → same database; RLS off → head 200.
   - M2 (distinct tenant DB): 503, request PENDING (default DB), level ENHANCED (tenant DB), reject → REJECTED over enhanced. Pre-existing on all trees. PROVISION_PER_TENANT_DB is set in 0 deployment/compose lines (READ). Record.
   - The live env is unverifiable without az (NOT COMMISSIONED).

ITEMS 4-8
4. F-2 CLOSED: head 39 (test) / 40 (production) approve lines; 0 missing requestId/userId/targetLevel; 0 round-1 strings; 0 silent level-path non-200 rows; 0 untrue for the stored state. Detector positive control fires on the stale rows; r1 control: 33 lines with a round-1 string, 6 silent. Target branch at warn.
   F-3 Minor SHIPS-WITH: (a) no cell fails the pre-auth lookup or the UPDATE with the re-read (N-1 unpinned; the seat's stub answers auth_find_user_by_id unconditionally); (b) no stale re-read; (c) the seat's two files under NODE_ENV production 14/17, 3 red, plaintext seed (Q4's own row); (d) 0-red tampers: other-level 503 wording, levelNow, 200 body.
   F-4 KEPT (O-UPD-OTHER 503; develop 500). The reworded r1 cell pins the residual-(i) line. MFA branch untouched (no hunk).
5. Tampers, WHOLE auth suite at head (27 rows): 0 VOID; all tsc 0; all (66, 779, 0); all restored with diff --quiet 0.
   - Seat 11 parsed with ast from tamper_1194_r2.py (sha256 6cacd81e87f9c6c4, never executed): T0 0 · T0-DEFAULT 0 in ks1194 · RP-PREFIX 6 · BLIND-RESTORE 3 · NO-TARGET-KEEP 2 · UNREADABLE-RESTORE 1 · LOG-NO-CTX 3 · OLD-LOG 1 · SWALLOW 5 · MEMFIRST 1 · TI 0 = 22 reds = C6. T0-DEFAULT also had 2 ks949 reds of 5005/5000 ms: default timeouts at load 28.9, 0 failed at load 24.2 (R-3).
   - Drafter 13/13 at its measured counts; 0-red consequences re-measured on the tampered tree. X2-UNREADABLE-NOTLANDED-RESTORES-WHEN-PREAUTH confirmed INERT.
   - QA: Q2-UNREADABLE-NO-THROW 1 (pred 1) · Q2-TARGET-VS-CURRENT 6 (pred 5, slip) · QC-HEALTHY-APPROVE-503 2 in ks1194 + 2 in ks467 (pred 3 inside, slip; the control fires).
6. Merge-in and checks.
   - 5d55a72bd = merge-tree 70ee7b6c0 x 3961c2add → cdd8b90c6 EQUAL, 0 conflicts. Brought 50 files = develop's delta (set-equal); under auth only package-lock.json.
   - develop..head = the 3 PR files. The fix alone: users.ts +45 -12 (READY "+42/-15" = slip, Record).
   - Auth vitest develop 64/762 and head = merged 66/779: 0 failed at DEFAULT and 60 s, load 23-25. ks949 alone 30/30 both; ks1194 files 17/17.
   - Project tsc rc 0 both (597 files).
   - Test-including program (scratch config outside auth): 734 / 736 files, both ks1194 tests in it and not in the project program; rc 2, 39 errors in 23 files on BOTH, per-file map EQUAL, 0 in ks1194, plant +1.
   - eslint 0/0 on users.ts both trees and both tests; control 2 x no-unused-vars WARN rc 0.
   - vitest 4.1.10 farm: counts equal the READY's 4.1.11; 4.1.11 NOT TESTED.
7. Links, read 01:44 and 01:54:59 (immediately before this mail).
   - attachmentsForURL(pull/1032) = KS-1194 contributes only (controls 1018 → KS-1050, 99999 → 0).
   - 0 closing phrases in title, body and 6 commits (controls 1/1/0). Body: ROUND 2 x1, Refs KS-1194 x1, Test Evidence x2.
   - KS-1194 comments 03c774f0 (accurate; silent on N-1) and 589d437f (accurate) present. KS-1018 53864975 present. KS-1230 exists (Backlog).
   - KS-1194 stays In Progress on merge (§5f).
8. Schemathesis / Akto NOT REQUIRED: 0 of 309 spec paths are verification routes (yaml 122d3a2f8 unchanged), and every finding needs a fault between two pooled statements.

CLOSED / STILL OPEN / NEW
- F-1 same-row (read-back fail after landed UPDATE; landed-throw; S + M1): CLOSED → ships.
- F-1 stale re-read / M2: STILL OPEN, pre-existing → Record.
- F-2: CLOSED → ships.
- F-3: STILL OPEN gaps + NEW (NODE_ENV production 14/17) → Minor SHIPS-WITH.
- F-4: KEPT → Record SHIPS-WITH.
- F-5 = D1 MFA auto-approve: STILL OPEN, untouched → TICKET-ON-KS-1194 (589d437f).
- N-1 residual (ii) NOT landed + deterministic unreadable rows: NEW Minor → SHIPS-WITH Record + TICKET-ON-KS-1194.
- Residual (ii) landed: consistent → Record.
- Residual (i): STILL OPEN, not introduced → TICKET-ON-KS-1194.
- E-1 GUC-less tenant-pool statements (M0/M1/M2 rls=on: every approve's UPDATE 0 rows; develop false 200 APPROVED basic; head 503): pre-existing → escalation TICKET. Major while multi-tenancy + fail-closed RLS runs; latent per bicep READ; the RLS premise is unmeasured.
- N-2 (QA sibling hunt): a stale PENDING ENHANCED request approved after the level rose to HIGH answers 200 and stores enhanced (a downgrade) on head / r1 / develop. Pre-existing, PROBED → escalation TICKET, Minor.
- R-1 (0-row upsert, READ-unreachable), R-2 (contract gap), R-3 (load), R-4, R-5: Records. R-6: TICKET (KS-1018).
- SC-R2-1 (QA self-correction): my round-1 fix-shape recommended "unreadable → keep APPROVED" without sizing the not-landed ordering. N-1's branch descends from it.

PREDICTION SLIPS
- Wednesday Q1 ruling: (a) "it did NOT rule unreadable → keep APPROVED". nogo_1032_fixround.md item 1, third bullet, rules exactly that (READ). (b) "round 1 held as PENDING" holds only under an unequal fault budget (MEASURED).
- Drafter: R2-D4's r1 column (the same budget error); its own inert row and 3 under-counts, as it stated.
- READY: C7 +42/-15 = +45/-12. C2/C9(ii) are silent on the not-landed state and the 400 retry. C4/C8 hold at NODE_ENV test only. C1 is incomplete (no GUC on the tenant-pool branch).
- QA: Q2-TARGET-VS-CURRENT 5→6; QC-HEALTHY-APPROVE-503 3→2 inside + 2 ks467.

NOT TESTED (equal prominence)
- A real Postgres: every stale / empty / zero / landed-throw row, the positional statement mapping and every RLS arm are stub or model; E-1's RLS premise is unverified.
- The live container env (az).
- Whether plaintext-PII rows or erased subjects with PENDING requests exist.
- The real DEK fetch failing (stubbed).
- Concurrency (two admins; submit racing review; N-2's cause).
- Multi-replica memory; the gateway; out-of-repo callers.
- The MFA branch beyond READ; vitest 4.1.11; a multi-line census of query(..., tenantId) callers.
- Schemathesis / Akto / Playwright / k6 / stack / browser (NOT COMMISSIONED).

BOUNDS (Secuura checkout, read verbs only; git writes only in my clone qa1032r2_gate_ob2ddoaz)
- START 01:39:20: porcelain 0 · config 2716d950dd2834b2 · refs 947 · worktrees 112 · branch feature/ks-597-b-caller-scoped-externalref · auth .vite ['vitest'] · develop 3961c2add · pull/1032 430672697
- MID 01:46:28: identical.
- CLOSE 01:51:58: identical. ls-remote again 01:54:59: develop 3961c2add, pull/1032 430672697.
- Listeners: START 01:39:38 17 LISTEN, 0 node, 0 login_stub. CLOSE 01:51:53 19 LISTEN, 0 login_stub, 1 node listener pid 63202 (cwd another Wednesday gate, gate1034r; not mine, untouched). My probe servers bound 127.0.0.1:0 and closed in afterAll; 0 processes reference my clone; nothing needed a SIGTERM.
- docker info rc 0 (not used; no container).
- A credential-looking compose default captured by a READ was redacted in the evidence file before any report or mail.

MERGE ADDENDUM: "on Kam's tap only (a card to Kam; never on this verdict alone): squash `430672697` onto develop `3961c2add8e1637b32e638f8f0952c328c00833e` (merged tree `522fc6606d8fbc7bad760ede926deefa78bb4679`; drafter `522fc6606`); #1032 attaches to KS-1194 only, linkKind `contributes`, no closes; KS-1194 stays In Progress on merge (§5f: live sweep owed; part 2 = F-5 open on comment `589d437f`); equality targets after the squash: users.ts `3bfa47dcd` / ks1194 test `703c80dca` / ks1194 round-2 test `b79cddd65`; auth vitest 64/762 at develop `3961c2add` -> 66/779 at head -> 66/779 merged (measured; merged tree = head tree; default and 60 s, 0 failed); dispositions: F-1 same-row CLOSED (ships), F-1 stale/M2 Record, F-2 CLOSED (ships), F-3 Minor SHIPS-WITH, F-4 Record SHIPS-WITH, F-5 TICKET-ON-KS-1194, residual (i) TICKET-ON-KS-1194, residual (ii) landed Record, R-1..R-5 Records, R-6 TICKET (KS-1018); NEW: N-1 Minor SHIPS-WITH Record + TICKET-ON-KS-1194 (residual (ii) not landed: APPROVED over an unraised level, 503 'could not be confirmed', retry and reject 400; plus plaintext-PII-under-prod and destroyed-DEK rows); escalation candidates E-1 (GUC-less tenant-pool statements, Major while multi-tenancy + fail-closed RLS runs, latent) and N-2 (stale request downgrades the level, Minor), both pre-existing, independent TICKETs; Records for KS-1194's facts comment at merge: F-1 closed on every same-row shape (read-back pool timeout / ECONNREFUSED / 22001 / empty / committed-then-disconnected -> 200 APPROVED, reject 400), open only on a stale re-read (per-tenant DB, unconfigured); residual (i) reachable by fail-ok-fail on the pool -> APPROVED over basic, 503, retry 400, resubmit recovers (same end state as round 1); residual (ii) landed -> consistent, retry 400; not landed -> APPROVED over basic, 503 'could not be confirmed', retry and reject 400, subject resubmit the only recovery (round 1 reached the same state with the same two pool faults; deterministic for a plaintext-PII row under a prod-like NODE_ENV); pool routing S same row / M1 same database, tenant-pool statements carry no GUC (E-1) / M2 different database (Record); F-4 kept (non-infra level-update error -> 503); the MFA auto-approve F-5 TICKET-ON-KS-1194; the seat's cells red 3/17 under NODE_ENV production (F-3); N-2 stale-request downgrade (escalation)."

ESCALATION CANDIDATES for Wednesday (QA acts on none):
- E-1: new ticket.
- N-2: new ticket.
- Confirm or overrule the N-1 Minor grade against your Q1 premise; the measured facts are in report §4 and §14.
Findings-only: nothing fixed, pushed, commented, filed or merged; nothing to Peter or Stuart.

