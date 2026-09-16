SUBJECT: [QA -> Wednesday] TIER 1 GATE #1015 (KS-1018) 77145ce84 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TIMESTAMP: 2026-09-16T21:09:46.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

TIER 1 GATE, ROUND 1: #1015 (KS-1018) at 77145ce84353534ba381688d5bbd16ff9ff27aef
VERDICT: GO WITH FINDINGS, on 77145ce84 as the delta over base 523f283c6, and on the merged tree with develop 523f283c6. develop did not move at START (06:52:48), MID (07:02:56) or END (07:08:11), so merged = head in content.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1018-1015-77145ce84-tier1-r1/report.md
(NOT-TESTED.written-first.md was written before any run; the evidence is in evidence/.)

BLUF
- Every INFRA fault on the three reads answers 503 at head: message form, pg 53300, ECONNREFUSED and 57014. This holds on every route and role that reaches a read, under F-all and F-ver, with the REAL userRepo and with a recording repo.
  Instrument: a stateful stubbed table with an SQL-scoped fault switch, REAL userRoutes at /api/users, REAL errorHandler and REAL rejectNulBytes, on 127.0.0.1:0. 242 rows x 2 shapes x base/head.
  INFRA-NOT-503 = 0. The positive control flags 14-62 rows on tampered trees.
- No other row changed status or body. That covers healthy, not found, 42P01, 42501, 40001, 40P01, 403, the KS-467 foreign-tenant 404, the GET /api/users/me control, L4 and L5. CHANGED = 0.
- Writes at head under an infra fault on a read = 0, so no Major against #1015. The same rows at BASE write:
  S1: a duplicate PENDING row.
  S2: a STANDARD auto-approve (UPDATE users).
  S3: a stale-memory approval (level raised, row REJECTED -> APPROVED, SYSTEM_ADMIN and ORG_ADMIN).
  S3r: a stale-memory reject (APPROVED -> REJECTED).
- No blocker. L1, L2 and L5 are correct.

FINDINGS
F1 Minor, TICKET, MEASURED. The KS-217 message-form pool timeout is unpinned. D-NARROW (rethrow only when err.code is set) passes 751/751 with tsc 0, yet my probe shows 21 real / 29 rec rows go from 503 back to 200/404, and 6 / 9 writes land, including the S3 approval with the level raised. Oracle: History (KS-217) and Product (dbErrors names this message).
F2 Polish, TICKET, MEASURED. The review site has no non-infra control: D-TW-GET is 0/751. Oracle: Product.
F3 Polish, TICKET, MEASURED. The controls cannot tell the memory fall-through from an empty return: D-CTL-NOMEM is 0/751. Oracle: Product.
F4 Minor, TICKET, MEASURED. The non-infra half (42P01, 42501, 40001, 40P01 on a read) still WRITES at head, identically to base: duplicate PENDING, auto-approve, stale-memory approval with the level raised, and an overwrite. It now also logs ERROR. This contradicts dbErrors.ts's KS-253 docstring ("propagate ... as a 500"). Oracle: Product.
  Ruling: not a blocker. The scope is deliberate (ticket item 3), base = head on every row, and the codes are config-class or not expected on a READ COMMITTED SELECT (READ ONLY reasoning).
  FLAG: read literally, "any write that still lands at head under a fault on one of the three reads = Major" covers these rows. I ruled them under Disagreement 4. Your call.
F5 Major, TICKET, pre-existing, not #1015, MEASURED. Save side (the unchanged saveVerificationRequest):
  - An INSERT fault still gets 200 PENDING, and the request is then invisible on a healthy list; a re-POST creates a second request.
  - A review approve whose save faults gets 200 "approved" with the level raised, while the DB row stays PENDING.
  Save-side ruling: TICKET. The fault is on the write, not on the three reads; base = head; the seat's NOT-covered list and the ticket name it. It belongs with the KS-1188 F3 class or a new ticket.

PLAIN STATEMENTS
1. Every calling route, per tree, fault scope and condition.
   - The census found exactly 3 callers (users.ts:1260/:1302/:1319, grep controls 0/1); no fourth.
   - REAL repo, F-all: GET and POST /me/verification are ALREADY 503 at base (getUserById runs first). Only review changes: 404 -> 503 for SYSTEM_ADMIN, ORG_ADMIN same-tenant and foreign-tenant, and 200 -> 503 for the stale reject.
   - F-ver: GET 200 -> 503, POST 200(+write) -> 503, review 404/200(+write) -> 503.
   - Non-infra, healthy and not-found rows are unchanged. The ORG_ADMIN foreign-tenant rows (with or without a memory hit) are 404 healthy and 503 under an infra fault, with no disclosure.
2. Writes under a fault: S1, S2, S3 and S3r all write at base and write 0 at head (infra, F-ver). Save side ruled TICKET (F5).
3. Callers failing open: D-CF-POST, D-CF-LIST, D-CF-REVIEW and my G-CF-REVIEW-404 (selective 503 -> 404) each red 1/751 with tsc 0. errorHandler 503 -> 500 reds 17 (14 + 3).
   The api-gateway proxy (READ at 523f283c6) streams /api/users. onProxyRes counts 500-599 alike. circuitBreakerGate is defined but mounted nowhere (stale comment at :187, pre-existing). Nothing fails open.
4. Log meta: exactly [code, error] on all three new lines, every row, both shapes; no ids.
   Tampers each red 1/751: userId (TK, D-TK-FIND), requestId (G-TK-GET), stack (G-STACK-GET/FIND/LIST), line removed (TL, D-TL-GET, G-TL-FIND).
   Request-controlled text: none echoed by the pg classes reachable here (READ). A path %00 is not rejected by rejectNulBytes (it checks the body only); it reaches the SQL parameter and gets 404 on both trees. At head, real pg would add an ERROR line (22021; READ ONLY).
   Two ERROR lines per infra fault at head: noise, not a leak.
   Leaks: in test, development and production, every 503 carries one fixed body, only the content-type and x-powered-by headers, and no Retry-After.
   VOID: real-shape production GET/POST, because my plaintext rows tripped PII_PLAINTEXT_CUTOFF. The rec shape measured 503 there.
5. READY and casts-only:
   - 139/139 READY + lines are in order at 6e30fe9f5, and 136/139 at head (3 = the casts). Nothing undeclared. Product +14 -4 is equal line for line.
   - git apply --check without --recount: rc 128 "corrupt patch". patch --dry-run: rc 2. A real patch -p1 fails but leaves a 0-line file. --recount succeeds silently, consistent with the seat's 0-byte outputs.
   - Casts-only: the emitted-JS diff is 13 lines = 5 redundant parens + 1 hoisted const calls; the planted control was caught. "No runtime change" HOLDS; "casts only" is not literal.
6. Tampers: 26 rows, whole auth suite, 751 cells run, pending 0, tsc rc 0 on EVERY row. VOID: none.
   T0 0, T1 1, T2 1, T3 1, TL 1, TW 1, TK 1, TI 0.
   INVISIBLE: D-TW-GET, D-NARROW, D-CTL-NOMEM.
   G-CTL-42 (control-aimed classifier over-classification) reds 4.
   Red before green: 6 run / 4 red at base.
   The probe under T2 flips 14/24 rows back; under D-NARROW, 21/29.
   Including tsc (src/**, exclude []): base 37 -> head 37, NEW 0, users.ts 0, ks1018 0, plant 38. `tsc -p services/auth` excludes __tests__, so it is vacuous for the new file. The seat's 8-error claim at 6e30fe9f5 is re-derived: 45 errors, 8 new, all in ks1018. eslint: 0/0 on both files, base and head; the plant counted 1+1.
   KS-1186: CORRECTION to the drafter. Review approve reaches the unawaited return fromRow( at userRepo.ts:512 via updateUserPlatformScope -> updateUser -> getUserByIdPreAuth (currentTenantId() is empty under runWithPlatformScope). PROBED with the auth_find_user_by_id SQL witness, and READ. No #1015 effect; record under KS-1186.
   Suites: auth base 61/745 -> head 62/751, pending 0; merged = head; shared 44/851 at head; project tsc rc 0 on both.
   Linear, read at START 06:56:50-06:57:07 and PRE-MAIL 07:07:32-07:08:06: attachmentsForURL(pull/1015) = exactly 1 node, KS-1018 (In Progress), linkKind contributes. KS-1188, KS-1186 and KS-1050 have 0 attachments; KS-253 -> #236 closes (control). 0 closing phrases (+control 2, Refs KS-1018 0). KS-1018 STAYS OPEN on merge (§5f live sweep owed, ticket item 3 open). Disjoint: 0 shared files with the 20 other open PRs.
   Schemathesis (spec-generated) and Akto: NOT APPLICABLE. The spec has no path for the three routes, and no spec-generated run can fault the DB. The hand-written systemTest/schemathesis/tests/test_user_admin_isolation.py does drive the review route: it is owed in the §5f live sweep and was NOT RUN (stack HOLD). Real-browser half: NOT APPLICABLE (no surface, no in-repo client).
   Checkout at START, MID and END: porcelain 0, config sha d7e7298b02c45f52..., 905 refs, 110 .git/worktrees, pull/1015/head = branch = 77145ce84, both .vite results.json unchanged (auth 6,697 b @ 09-09 08:58:04; api-gateway 5,907 b @ 09-17 01:02:02).

MERGE ADDENDUM
squash 77145ce84 onto develop 523f283c6 (or the then-current develop; file-disjoint from #1014); #1015 attaches to KS-1018 only, linkKind contributes (as read at 07:07:32-07:08:06 AEST) — KS-1018 stays open for the §5f live sweep and ticket item 3; equality targets after the squash: services/auth/src/routes/users.ts blob 8ef9065e2fb24308daeb41820a227a4ee1d6ecc9 / services/auth/src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts blob 6723276d016e4d6cf4ead8cb4f511ce5dad5ce53; auth 61/745 -> 62/751 (re-measured at 06:54:29 / 06:54:35), merged 62/751 (= head, develop unmoved); A16 KS-1050 waits for this merge (same file); Records: F1 msg-form unpinned (D-NARROW invisible, reopens writes); F2 no review non-infra control (D-TW-GET); F3 controls cannot see D-CTL-NOMEM; F4 non-infra half still writes at head (KS-253 docstring); F5 save side acks unpersisted writes incl. a level raise with the row PENDING (TICKET, pre-existing); KS-1186 review approve reaches userRepo.ts:512 (drafter prediction corrected); rejectNulBytes is body-only (path NUL reaches SQL param); circuitBreakerGate unmounted (stale comment); casts-only not literal (runtime-equivalent); READY header over-declared (apply without --recount refuses; patch leaves a 0-line file).

NOT TESTED (same prominence)
docker info rc:
0
1. The §5f live sweep on a rebuilt stack (KS-535 HOLD), including systemTest/schemathesis/tests/test_user_admin_isolation.py.
2. A real Postgres and a real infrastructure failure (pool starvation, connection loss between the reads, real 57014/53300/22021/40001/40P01). Every fault here is a thrown object.
3. Multi-replica divergence (ticket item 3). S3 simulates a second replica with a table edit; no second process.
4. nginx and the api-gateway proxy: READ only, never run.
5. Route clients (admin review screen, issuer portal; none in repo), out-of-repo callers, a real browser.
6. systemTest/schemathesis: spec-generated NOT APPLICABLE; the hand-written test NOT RUN. systemTest/akto, systemTest/playwright, systemTest/performance: NOT COMMISSIONED.
7. Preflight legs 3/4/8 (not a pass); preflight never run.
8. KS-1186: reachability recorded only. Ticket item 3.
9. The real authenticate, JWT and sessions; the real logger transport.
10. Two healthy POSTs racing (no partial-unique index).
11. api-gateway suites (develop did not move).
12. Real-shape production GET/POST 503 (VOID; rec shape only).
13. A DB fault inside getUserByIdPreAuth or updateUser on the approve path (only the INSERT save fault was measured).
No container was created. Loopback only. No push, no comment, no file, no ack.
