SUBJECT: [QA -> Wednesday] TIER 1 GATE #1013 (KS-999) 5fbfb66a9 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TIMESTAMP: 2026-09-16T19:26:44.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

VERDICT: GO WITH FINDINGS on 5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2 — as the delta over base 1125607e9 AND on the merged tree = develop 79432c797 (moved by #1012, api-gateway only, content-disjoint) + 5fbfb66a9, merged in the gate's own clone (never pushed). No Blocker. 3 TICKET findings.

Composed Thu 17 Sep 2026 05:26:42 AEST. Session 05:01:49 AEST onward. Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks999-1013-5fbfb66a9-tier1-r1/report.md (NOT-TESTED.written-first.md written 05:02:05, before any run; evidence/ beside it).

BLUF
- Over HTTP (REAL auth/wallet/mfa/oauth/users routers + REAL userRepo + REAL passwordLoginGate + REAL errorHandler on 127.0.0.1:0; db.query, getDek, shared crypto, authenticate, logger, jwt/session/lockout stubbed with hit witnesses; the DEK fault aimed by READER via the getDek stub's own stack), a DEK-read INFRA failure on the getUserById read turns 500 INTERNAL_ERROR -> 503 SERVICE_UNAVAILABLE on 13 of 13 measured calling routes (message form, pg 53300, ECONNREFUSED), at head AND merged. Every other row is status+body identical base->head; the only other delta is the new 'DB getUserById failed' log line. 230 rows per tree; base->head 74 rows differ (49 (b) flips, 23 log-line-only, 2 cookie-Expires-second artefacts); head->merged 0.

1. CALLING ROUTES per condition and tree (base/head/merged)
- Flip 500->503 under a getUserById-targeted DEK infra fault (all 3 forms): GET /api/users/me, GET /api/auth/me, PATCH /api/users/me, POST /api/users/me/mfa/enable, GET /api/users/me/verification, PATCH /api/users/admin/:id (platform scope), GET /api/auth/mfa/status, POST /api/auth/mfa/setup/start, POST /api/auth/mfa/backup-codes/regenerate, DELETE /api/auth/wallet/unlink, POST /api/auth/login (:587 read-back), POST /api/auth/reset-password, POST /api/auth/verify-email.
- Healthy (a) / non-infra DEK failure (L3, 500) / destroyed DEK (L5, 200) / plaintext cutoff (c, 500) / not found (d: 404, 400, 401, mfa/status 200 mfaEnabled:false) / query() infra (e: 503; reset-password+verify-email 500 pre-existing): UNCHANGED on all three trees. 5 controls (oauth/scopes, mfa/verify 410, social/providers, wallet/status, users/admin/organizations) unchanged everywhere.
- Retry-After: absent on all 690 rows. 503 body verbatim: {"success":false,"error":{"code":"SERVICE_UNAVAILABLE","message":"Authentication service temporarily unavailable, please retry"}}.
- Every route where (b) is NOT 503 at head: none that reaches getUserById. Under an ALL-reads DEK outage, login / reset-password / verify-email stay 500 at head because their FIRST DEK read is a KS-1186 sibling (getUserByEmail / getUserByIdPreAuth) — RECORD R2; the real provider also caches a subject's DEK 5 min (READ).
- /api/oauth/token (refresh grant, measured): does NOT call getUserById (reader getUserByIdPreAuth); all-reads fault 500 base AND head; getUserById-targeted fault 200/200; hard-coded 500 catch. The ticket's "four families" is wrong for /oauth/token; the reach is wider (9 families census in the report).
- NOT MEASURED over HTTP (READ only): register, social callback/link, oauth/authorize (catch hard-codes 500), wallet/link and auth/refresh (refused before any read under my stubs — path not reached).

2. SECURITY
- No leak: 503 body fixed text; headers content-type + x-powered-by only, identical to base; no user id / DEK / pg code / stack in body or headers; the new log line's meta is {error, code} only (all 5 distinct metas enumerated). 'Error occurred' logs stack at base AND head (not new). At head 'Error occurred' carries the classifier message, so for (b) the root cause survives ONLY in the new line.
- No caller branches on 503 vs 500: non-test auth src only errorHandler.ts:290 and requestLogger (>=500 both). Login under the read-back fault: no token, no session, recordFailure 0 on both trees (recordSuccess 1 both — pre-existing order). oauth/token issues nothing on any failing row. api-gateway proxy.ts (READ, blob unchanged): onProxyRes counts any 500-599 as one breaker failure — 503 and 500 identical, pass-through, no retry.

3. DECRYPT-FAILURE LOG LINE
- Under the plaintext cutoff head adds error 'DB getUserById failed' {"error":"[piiCrypto] plaintext email present after PII_PLAINTEXT_CUTOFF (2026-06-01T00:00:00.000Z) — encryption migration incomplete"} beside 'Error occurred' (same message) = a DUPLICATE (2 error lines per request) — operator noise, NOT a leak (no user id, no stack, only the cutoff date). Same for L3 non-infra. The ks949 decrypt CHARACTERISATION cell is byte-identical (AST); Q-DECRYPT-503 reds exactly it (1).

4. SIBLINGS
- KS-1186 real over HTTP: POST /api/auth/mfa/disable (getUserByIdWithPasswordHash) under an all-reads DEK infra fault = raw 500 at base AND head (503 under query() infra).
- FIVE unawaited 'return fromRow(' inside a try at head: :446 :512 :585 :594 :627 (base :442 :508 :581 :590 :623). :1040 listUsersInner has no try: GET /api/users = 500 under both a DEK fault and query() infra, base and head — a separate KS-253 gap (RECORD R4).

5. READY ACCOMMODATIONS + SEAT EDITS
- Per-cell AST diff of ks949 (TypeScript API, with a planted control edit that it catches): 30 -> 30 cells; 28 byte-identical; the renamed cell (CHARACTERISATION: ...UNAWAITED fromRow... -> CONTROL: the same row in a non-prod env resolves...) has a BYTE-IDENTICAL body; the KS-963 infra cell only GAINS the declared log assertion. Undeclared: logCalls.length = 0 in the KS-963 beforeEach — benign (X-NOCLEAR 0 red; X-NOCLEAR+TL still reds the ks949 log assertion).
- Head = READY: product + line present x1; ks999 file = the patch's 97 + lines, 0 diff.
- DISAGREEMENT 6 answered: the READY test patch (@@ -0,0 +1,75 @@ over 97 lines) is accepted with rc 0 by BOTH git apply and patch and silently writes a 75-line file — 3 of 5 cells, cut mid-cell. 0-product.patch is rejected by git apply --check (corrupt at line 11) and accepted by patch. The seat's apply-*.out are 0 bytes. The pushed head blob is correct; the READY patch is not a faithful transport (RECORD R6).

6. TAMPERS (head, whole auth suite, project tsc rc per row; anchors count 1, landing + sha256 restore + porcelain asserted)
T0 0 | TA 2 | TL 2 (failed_suites 4) | TC 3 | TI 0 | Q-SWALLOW 4 | Q-500 4 | Q-CTL-NODEK 7 | Q-DECRYPT-503 1 | Q-LOG-LEAK 0 INVISIBLE | Q-EH-503-AS-500 14 (0 in ks999/ks949) | G-CTL-QUERY (gate CONTROL-aimed) 3 | G-CALLER-FAILOPEN (gate caller tamper: mfa/status maps 503 -> 200 mfaEnabled:false) 0 INVISIBLE | T0-after 0. Every row: tsc rc 0, 745 tests, 745 cells run, pending 0, success as expected. VOID rows: none. All seat + drafter predictions reproduced. Red before green: head ks999 on base = 5 run / 2 red / 3 green.
HTTP probe under tampers: TA -> the 49 (b) rows back to 500; Q-SWALLOW -> login 200 WITH a token, mfa/status fail-open, /users/me 404 under a DEK outage (the suite catches Q-SWALLOW: 4 red); G-CALLER-FAILOPEN -> mfa/status 503 -> 200 on 5 conditions with 0 suite reds.
Instrument self-audit: my first including-tsc run was VOID (wrong -p path, TS5058) — caught by its planted control, quarantined, re-run; my tamper marker assertion aborted twice (too strict), restores verified, outputs quarantined; the final run is clean.

FINDINGS (all TICKET, SHIPS-WITH)
- F1 Minor, MEASURED AT RUNTIME: the route-level HTTP 503 on getUserById callers is unpinned — G-CALLER-FAILOPEN (fail OPEN on 503) reds 0/745 while the probe shows mfa/status 503 -> 200 mfaEnabled:false; Q-EH-503-AS-500 reds 0 in ks999/ks949. Oracle: History (KS-253/KS-963), Purpose. Owner's regression test: one HTTP cell per family head, infra -> 503, non-infra control -> 500.
- F2 Polish, MEASURED AT RUNTIME: the classifier log SHAPE is unpinned — Q-LOG-LEAK (stack + userId in the new line) reds 0/745. Oracle: Statutes & standards (PII in logs). Test: assert the meta key set is exactly {error, code}.
- F3 Minor, MEASURED AT RUNTIME: backup-code sign-in (real argon2 codes) — the burn LANDS (2 -> 1 codes), then the read-back DEK fault answers 503 "please retry" at head (500 at base); the retry with the same code answers 401 and calls recordFailure (lockout +1). Controls: healthy-then-reuse 200 then 401; query() fault BEFORE the burn 503 then 200. Oracle: Product (updateUserOrThrow's own KS-1052 comment reasons 503 for an UNBURNT token), User desires.

INCLUDING TSC (in-tree config extends ./tsconfig.json, include src/**/*.ts, exclude [], noEmit; quoted in the report): --listFilesOnly base 60 / head 61 / merged 61 __tests__ (ks999 + ks949 listed at head and merged); errors base 37 -> head 37 -> merged 37; NEW 0 (line-number-free); userRepo.ts 0; ks999 0; ks949 7 TS1343 shifted +2; 0 TS2741; planted TS2322 -> 38 lines. The seat's 67-line program REPRODUCED on the gate's head tree with its out-of-tree config (rc 2, 70 lines, 67 errors, 29 TS2741 incl. ks1013 (103,5)): out-of-tree, @types/node resolves from Dev + packages/shared node_modules; in-tree from services/auth/node_modules (R4 class). Project tsc rc 0 base/head/merged (excludes __tests__ — vacuous for tests). eslint on the 3 files base 0/0, head 0/0; planted unused const -> 1 warning @typescript-eslint/no-unused-vars on both trees.

LINKKIND (read at run time): START 05:11:28 and PRE-MAIL 05:25:07 — attachmentsForURL(pull/1013) = exactly 1 node, KS-999 'contributes' (In Progress). KS-1186 0 attachments, KS-1168 0, KS-963 3 closes (#970/#913/#907, none 1013 — control), KS-253 1 (#236). Closing phrases 0 over title/body/commit/1 comment (positive control 2, negative 'Part of KS-999' 0). KS-999 must STAY OPEN on merge for the §5f live sweep.

DISJOINTNESS: PR files API #1013 vs 19 other open PRs by exact filename -> 0 shared (incl. #1011, head now 6dc825644, 4 files). Neighbours: dependabot #948/#649 (auth package.json + lockfile), others on the lockfile; #922 on secuura-api.yaml. develop read 05:02:42 / 05:14:28 / 05:25:02 = 79432c797 (moved from 1125607e9 before START; #1012; judged by content; merged tree built and measured: auth tree b788fec96 = head).

SCHEMATHESIS / AKTO: Schemathesis NOT APPLICABLE — 23 of 28 calling route/methods documented, all 23 declare 503 with one shared definition (required success+error, success enum false, error.required code+message) that the measured body satisfies; a spec-generated run cannot induce a DEK-read failure. Absent from the spec (pre-existing): GET/POST /api/users/me/verification, POST /api/users/verification/{requestId}/review, POST /api/auth/verify-email, GET /api/users. Akto NOT APPLICABLE / NOT COMMISSIONED. Neither run.

SUITES: auth base 60/740, head 61/745, merged 61/745 (pending 0, success true); ks949 30/30 base and head; shared 44/851 at head (851 passed, pending 0).

CHECKOUT (read-only) START 05:02:42 / MID 05:14:28 / END 05:25:02: porcelain 0; .git/config sha256 d7e7298b02c45f52...; 899 refs; 110 .git/worktrees; HEAD 355d82c8b; refs/pull/1013/head = branch = 5fbfb66a9 (no move); auth .vite results.json 6,697 b @ 2026-09-09 08:58:04; api-gateway 5,907 b @ 2026-09-17 01:02:02 — identical at all three.

ADDENDUM (merge seat)
squash 5fbfb66a9 onto develop 79432c797 (develop moved from 1125607e9 by #1012 — api-gateway only, content-disjoint; file-disjoint from #1011 / #1012); #1013 attaches to KS-999 only, linkKind contributes (as read at 05:11:28 and 05:25:07) — KS-999 stays open for the §5f live sweep; equality targets after the squash: userRepo.ts 9060b308e / ks949 test 4f03e6f4f / ks999 test 04ce4e156; auth 60/740 -> 61/745 (re-measured), merged 61/745; Records: R1 /oauth/token is not a getUserById caller; R2 under a total DEK outage login/reset-password/verify-email stay 500 (KS-1186 siblings read first); R3 KS-1186 real over HTTP (mfa/disable raw 500), five sites :446/:512/:585/:594/:627; R4 listUsersInner :1040 unclassified query() infra (GET /api/users 500); R5 no Retry-After; R6 READY test patch silently truncates to 75 lines under git apply AND patch (head blob correct); R7 undeclared logCalls.length = 0 benign; R8 seat's 67-line tsc = out-of-tree @types/node resolution; F1-F3 TICKET.

NOT TESTED
docker info rc:
0
(run once; no container created)
- the §5f LIVE sweep on a rebuilt stack (owed at the Sunday QA pass)
- a real Postgres / real DEK store (pii_subject_keys) / real pool starvation; the real provider cache
- the auth service behind nginx and the api-gateway proxy (READ only)
- real OAuth clients; POST /api/oauth/authorize over HTTP (READ only)
- register, social callback/link, wallet/link, auth/refresh over HTTP (not reached / not measured)
- out-of-repo callers; a real browser (not applicable: no rendered surface change)
- systemTest/schemathesis (NOT APPLICABLE, not run); systemTest/akto, systemTest/playwright, systemTest/performance (NOT COMMISSIONED: 40% cap, stack HOLD)
- preflight legs 3/4/8 (not run; the seat's SKIPPED legs are not a pass)
- KS-1186 (Record measurement only); KS-1168
- concurrency on the DEK read; cross-app side effects (stubbed)

Nothing went to Peter or Stuart. No comment, no ticket change, no push, no merge.
