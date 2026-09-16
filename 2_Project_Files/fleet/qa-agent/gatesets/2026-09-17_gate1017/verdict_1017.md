=====MSG 2026-09-16T23:31:00.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 15830
QA agent -> Wednesday. TIER 1 ROUND 1 gate (round 1 of 2), PR #1017 (KS-1195) @ cbe29597d11e59f2e1a14519e9ba3dbf6de9a756.
Session 09:11:08 -> 09:29:44 AEST 2026-09-17 (clocks from `date`). Findings-only: nothing fixed, merged, pushed, commented or filed.
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/report.md

## BLUF
VERDICT: NO GO on `cbe29597d` (delta over base `7e89318bc`), and on the merged tree `135b07468c0f12279836c43051e16d5ff1053398` (head merged with develop `fa887f382` = #1014's squash; the same OID as the drafter's).

The NO GO rests on F-1 alone:
- F-1 (Major, NEW, made live by #1017; escalation candidate). The "per-key" limiter buckets by connector. Every key whose validate response has no connectorId shares ONE bucket (`connector:api-key`) across ALL tenants.
  - MEASURED on the real app (in-memory, and identical under the fake-Redis substitute): tenant X's key 200, 200; tenant Y's key's FIRST request 429; tenant Z's limit-1000 key Remaining 996; tenant W's key 429. Base never limits.
  - READ (new; not in the brief): the product's own admin mint, `originate/src/routes/adminConfig.ts:932-951` (`POST /api/admin/api-keys`, the path `systemTest/schemathesis/scripts/setup_api_key.py` uses), INSERTs no `connector_id`. It writes `rate_limit = d.rateLimit || 1000` unclamped and window 3600.
  - So every admin-minted key platform-wide shares 1000 requests per hour per replica. One tenant's burst refuses the others for up to an hour. This is the product's documented mint path, not only the pre-KS-869 rows.
  - Oracle: KS-164, "a key configured at N/min lets N through". The PR title claims "a key's ceiling is enforced".
  - The deploy precondition as written names allowances and traffic rates, not the bucket.

Everything else in the delta is clean at the level measured. If you rule F-1 SHIPS-WITH (a named deploy block) or TICKET instead, the rest reads GO WITH FINDINGS. That ruling is yours; the gate's call is NO GO.

## Plain statements, items 1-13
1. The limiter FIRES on the real index.ts app.
   - Census: 326 route rows from SOURCE; every `use` prefix is probed as GET prefix, GET sub-path and POST.
   - Head: 175 rows fire, ALL exactly Remaining [1,0,0] with 429 at N+1 and the refused request not forwarded.
   - Families: proxy 114, index 19, platform 14, verification 11, notifications 9, admin 4, audit-export (the /api/admin/* proxy catch-all) 3, health 1.
   - Upstream hits: 2 on 118 rows, 0 on 56 gateway-answered rows, 6 on POST /api/documents/:id/verify.
   - Positive control on the same instrument: a machine JWT (authMethod api_key) fires on exactly the same 175 rows and on none of the other 151.
   - Non-firing rows:
     - requireAdmin 39 (401 to a key);
     - batch 3 + audit export 1 (401 to every principal; dead by mount order, pre-existing);
     - 405 GET-on-prefix artefacts 22 (their sub-path and POST variants fire);
     - 61 gateway-unauthenticated surfaces (/api/auth*, /api/oauth*, /api/sessions, /api/verification*, /originate/*, /analytics/*, /webhooks/stripe*, /api/m365/*, downloads, health...). READ: no upstream authenticates an sk_ key itself (x-api-key appears only in comments), so no authenticated family stays unlimited.
   - Base: 0 of 326 rows carry X-RateLimit-* for any principal.
   - Merged: 175 fire, identical classes; every stage identical to head. 2 census rows differ only on the per-IP LOGIN limiter (GET /api/auth/password-reset C-leg; no X-RateLimit-*): order-dependent under the census pool, the instrument, not the limiter.
2. COUNTED ONCE.
   - Head: a fresh key at 1000, one request, shows Remaining 999 on all 175 firing rows.
   - KS-870 real erasure routes (POST /api/gdpr/erasures, GET .../:ref) count once, for BOTH a subjects:erase key and a connector grace-role key: [201,201,429,429] and 999.
   - G-ERASE (TG form 2, tsc 0): 8 rows / 7 chains at 998. They are the two erasure routes (proxy.ts:729 then :748), GET /api/documents/:id, and POST /api/documents/:id/{sign, sign/request, anchor, share} (verification.ts:1323 and :1419-1422, then the proxy.ts:565 mount). GET /api/documents/upload is the :id chain.
   - Under G-ERASE the erasure routes give [201,429,429,429]. The whole suite has 1 red (R3, a bare app) = F-2 (Minor).
   - The WeakSet is keyed on the same req object on every real chain (READ).
3. NOT WIDENED.
   - On all 326 rows, 10 non-machine principals (JWT email / wallet / federated / social / jwt / oauth / no authMethod, a connector JWT as Bearer, a test token, a non-sk key plus JWT) carry X-RateLimit-* on 0 rows, and get no 429 from this limiter.
   - Machine controls (JWT api_key and oauth_app, test token api_key and oauth_app) are limited at 100; API_KEY is not.
   - No credential, unknown sk_ key and malformed Bearer carry a header on 0 rows; 0 status or forward diffs base -> head.
   - Optional-auth sites: proxy.ts :573 :859 :942 :1031 :1048 :1097 PLUS admin.ts:1455 and :1483 (the brief's list omits these two).
   - Per-IP limiters: region bytes identical on base, head and develop. At DEFAULT maxima, base = head: verification 429 at request 601 with RateLimit-* standard headers only; global 10,000 then 429.
4. ONE RESPONSE (A1).
   - Sync throw: 500 once, then 429, handler hits 1 (key); JWT 500.
   - Async reject: hang + 1 unhandled rejection, then 429, hits 1 (pre-existing hang class; base hangs twice).
   - Headers-sent in logger, console, unhandledRejection AND uncaughtException: 0 at head. The same capture fired under G-AFTER (control).
   - The next()-throws plant: see F-4 (Record).
5. TENANT (A2). currentTenantId after the continuation, in-memory and fake-Redis:
   - key, JWT, JWT machine and super-admin override correct;
   - the issuer override is ignored;
   - test token null at base AND head (parseTestToken drops tenantId; pre-existing).
   - 24 parallel requests of two keys in two tenants, one being refused: 0 mismatches. TT: 14 mismatches (red).
   - Forwarded x-tenant-id is identical base = head on all 167 forwarded rows.
   - A refused request's audit row carries its own tenant.
6. REDIS (A3).
   - The REAL redis.ts client against a loopback fake: NOT TESTED. None exists in the repo; the search was re-run with controls (net.createServer 0 / control 20; +OK/+PONG 0 / control PONG 11; ioredis-mock etc. 0 / control "ioredis" 17).
   - LABELLED substitute (vi.mock getRedisClient, an in-process async fake):
     - head 2,463 calls, pexpire only at count 1;
     - census 0 row diffs vs in-memory;
     - KS-616 mid-command throw through the new placement: [200,200,429,429], redis-command-failed logged once;
     - base 3 calls (plant only).
   - Degrade: DEGRADED redis-not-ready logged once per run (throttled).
7. ALLOWANCE (A4).
   - Absent / null / 0 -> 100 (window 0 -> 60); 1000/3600 -> 1000; schema min and max as configured.
   - Edges: -1 -> 429 on every request; 'abc' -> never limited (Limit abc, Remaining NaN); window -5 -> never limited; window 'abc' -> Retry-After NaN.
   - Real producers (READ): security clamps 1..10000 / 60..86400. The originate admin mint writes `d.rateLimit || 1000` UNCLAMPED (so -1 is admin-reachable), window 3600, no connectorId. That is a drafter slip: the brief said only hand-edited rows reach the edges.
8. ORDER AND STATE (F-5, Record).
   - A refused POST still writes an audit row (status 429, success false, own tenant).
   - A fresh key's refused POST costs validate 1 + exchange 1, forwarded 0. GET is not audited. Base: all forwarded.
   - G-AFTER: refused requests are forwarded, audit rows written, 3 suite reds, and `process.exit unexpectedly called with "0"` was captured.
9. TAMPERS.
   - Setup: headT worktree; every row 53 files / 432 cells, pending 0; anchor 1, marker 1; sha + HEAD-blob restore; git diff --quiet rc 0.
   - Seat's six: T0 0 · TA 4 · TG 1 · TW 6 · TT 1 · TI 0, exactly.
   - VOID forms: TG-del (guard deleted) and TW-del (`if (!user)`) are tsc rc 2 (TS6133). Their reds equal the compiling forms', but they are VOID.
   - Compiling forms: TG `countedRequests.has(req) && false`; TW `!user || (false && ...)`.
   - Gate rows: G-CTRL exactly 2 · G-OAUTH 0 (probe: oauth limited at 100) · G-KEYSCOPE 6 · G-ERASE 1 · G-AFTER 3.
   - Mine: G-UNKOPT (unknown key counted on optional routes) 0 reds, the probe sees 22 rows gain a header; G-JWTCATCH (JWT continuation awaited in the try) 0 reds, the plant sees hang -> 401.
   - T0 after 0.
   - Controls that cannot see: the suite, for G-OAUTH, G-UNKOPT and G-JWTCATCH (F-3, Minor, TICKET).
10. tsc / eslint / pins.
   - INCLUDING tsc (not -p): 31 lines / 11 files on base, head and merged; NEW 0 on all three pairs; plant +1 (TS2322); ks1195 test in program. Project tsc -p rc 0 on all three.
   - eslint by rule+message: base = head (auth.ts 1, rateLimitEnforce.ts 0, index.ts 2); new test 0; --stdin control fired no-unused-vars, no-debugger, no-var.
   - Pins (KS-953 class): head lines 845/858/891 READ. ks781 solo at head 231/231; head pins over BASE index.ts 229/231 (red, restored by sha); 973eb49ef shared 849/851; head shared 44/851 pass. Merged shares shared tree dbd72dea0, and #1014 does not touch index.ts, so the pins hold.
11. MERGED.
   - develop fa887f382; merged tree 135b07468c0f12279836c43051e16d5ff1053398 (merge-tree in my clone = local merge tree = drafter's).
   - Suites: base 52/424 -> head 53/432 -> merged 54/450, all pass, pending 0, tsc rc 0.
   - Items 1-3 re-run on merged = head.
12. LINEAR (read 09:22:46 and again pre-mail 09:29:27).
   - attachmentsForURL(pull/1017) = exactly [KS-1195, In Progress, contributes]; controls pull/1014 -> KS-1176 contributes, pull/99999 -> 0.
   - KS-1195 stays In Progress on merge (5f).
   - Closing phrases 0 (controls 1/1/0).
   - KS-1187 0 everywhere (positive control 1).
   - Deploy precondition present: PR body 2 lines, and comment 6e25f648 anchors all true.
   - GitHub: head = pin, develop tip fa887f382, 0 exact shared files with 20 other open PRs.
13. SCHEMATHESIS / AKTO: NOT APPLICABLE.
   - The spec blob 122d3a2f8 is unchanged and already declares 429 on 343 operations (control 200: 290), x-ratelimit 100 and Retry-After 342.
   - #1017 changes no status, header or schema, only when a documented 429 is reachable.
   - The real-browser half of tier 1 is NOT APPLICABLE (no rendered surface).
   - Record: setup_api_key.py's key is admin-minted (no connectorId, 1000/3600), so platform-suite runs share F-1's bucket and can refuse, or be refused by, other tenants.

## Other findings (all target TICKET unless you say otherwise)
- F-2 Minor (SHIPS-WITH or TICKET): the guard is load-bearing on 7 real chains, pinned only by a bare-app cell.
- F-3 Minor: no cell sees G-OAUTH (the real 'oauth' signer, auth jwt.ts:205/229), G-UNKOPT or G-JWTCATCH.
- F-4 Record (PROBED; unreachable through Express 4 by READ: 0 manual authenticateToken(...)(...) calls):
  - next() inside the limiter's try: a synchronous throw from the continuation is counted twice and dispatched twice, and logged as redis-command-failed on the Redis path.
  - On the JWT branch the throw now escapes as an unhandled rejection (head hang) where base answered 401. Under production's default UNHANDLED_REJECTION_MODE=exit that calls gracefulShutdown (READ).
- F-5 Record: refused mutations still write audit rows; a refused uncached key still costs validate + exchange.
- R-1 A4 edges: the originate mint is unclamped.
- R-2 Unthrottled "has no rateLimit" warn: 197 lines, all from JWT or test-token machine principals, which no real signer emits.
- R-3 Test token carries no tenant (pre-existing).
- R-4 Unknown sk_ key passes optional auth where none gets 401 (/api/credentials*, /api/referrals/:sub; base = head).
- R-5 The per-IP login limiter makes /api/auth/* census rows order-dependent (instrument).

## Prediction slips
- Drafter: A4 edges and keyless keys are "hand-edited / pre-backfill only". The originate admin mint writes both today.
- Wednesday / drafter: the optional-auth list misses admin.ts:1455 and :1483.
- Seat: TW 1 -> 6 (already self-reported); "KS-870 is the real double-auth chain" -> 7 chains; "TG leaving R1/R2 green shows documents/anchors authenticate once" holds for POST /api/documents and GET /api/anchors only.
- Mine (VOID instruments, kept and superseded): the first spec regex (control 200 = 0), a per-service x-api-key count (git grep rc 128), and an eslint None-ruleId sort crash.

## MERGE ADDENDUM (for the merge seat, ONLY if Wednesday overrules the NO GO)
squash `cbe29597d` onto develop `fa887f382` (then-current; fa887f382 at draft close = #1014's squash) (merged tree `135b07468c0f12279836c43051e16d5ff1053398`; drafter 135b07468; file-disjoint from #1014's squash by content); #1017 attaches to KS-1195 only, linkKind `contributes` (as read at 09:29:27 AEST) — KS-1195 stays In Progress on merge (§5f: a live sweep is owed); the deploy precondition stands: real keys' configured allowances and real connector traffic rates are UNMEASURED and must be measured before any deploy (PR body + KS-1195 comment `6e25f648`) — AND (gate addition) F-1's shared `connector:api-key` bucket must be fixed or explicitly ruled before any deploy, since originate's admin mint writes no connector_id; KS-1187 not named; equality targets after the squash: `auth.ts` blob `8fbe102eb` / `rateLimitEnforce.ts` `f4b66aa1a` / `index.ts` `db127dbfa` / ks1195 test `ade08ac1e` / ks781 test `bc4815c4e`; api-gateway 52/424 at `7e89318bc` -> 53/432 at head -> 54/450 merged (re-measured; drafter 54/450); packages/shared 44/851 at head; Records: F-2 guard pinned only on a bare app (7 real chains), F-3 G-OAUTH/G-UNKOPT/G-JWTCATCH invisible to the suite, F-4 next() inside the limiter try (double count + re-dispatch; JWT-branch unhandled rejection), F-5 refused mutations write audit rows / uncached refusals cost validate + exchange, R-1 originate admin mint rateLimit unclamped, R-2 unthrottled no-rateLimit warn.

## NOT TESTED (equal prominence)
1. Real keys' configured allowances (no DB read).
2. The count of real keys without a connector_id (F-1's population). It needs a read-only per-environment query of svc_api_keys WHERE connector_id IS NULL, by someone authorised.
3. Real connector traffic rates; Platform S's keys toward K.
4. A real Redis and the REAL services/redis.ts client (no loopback fake in the repo). Redis rows are a LABELLED in-process substitute.
5. Multi-replica counting (KS-170).
6. The deployed gateway (nginx / Container Apps, NODE_ENV=production, prod per-IP maxima, UNHANDLED_REJECTION_MODE=exit).
7. systemTest/schemathesis, systemTest/akto, systemTest/playwright, systemTest/performance: NOT COMMISSIONED (40% cap, KS-535 HOLD).
8. Preflight legs 3/4/8 (the seat's SKIPPED legs, not a pass).
9. The auth service suite.
10. Absolute-form request targets (Kam-held; not probed).
11. A real browser (NOT APPLICABLE).
12. The security validate handler and the originate admin mint at runtime (READ ONLY).
13. Real OAuth / connector minting at runtime.
14. Handler reach on gateway-answered routes (inferred from status).
15. docker info rc: 0 (run once; no container created or touched).

## Bounds
- Checkout (read-only), start 09:12:58 / mid 09:25:05 / close 09:29:12, identical:
  - porcelain 0; .git/config sha256 d7e7298b...9f66; refs 911; .git/worktrees 110 (list 111);
  - origin develop fa887f382; refs/pull/1017/head cbe29597d (unmoved); branch feature/ks-597-b-caller-scoped-externalref;
  - .vite results.json 5907 b @ 01:02:02; .vite entries newer than my first file 0 (control 9).
- TCP LISTEN census: 0 node listeners at start, mid and close. All gate listeners bound 127.0.0.1:0 in vitest workers and closed; 0 gate processes remain.
- Clone: scratchpad gate1017_qa_j5ome9s0. Farm per entry, wholesale 0. Nothing pushed.
