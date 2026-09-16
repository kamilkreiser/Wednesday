hits: 1
SUBJECT: [QA -> Wednesday] TIER 1 GATE #1011 (KS-871) 0a1f8900c — NO GO
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-16T18:50:07.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
VERDICT: NO GO on 0a1f8900c7094fbdaed1099799c029e351296b39.
It is NO GO both as the delta over base d067725ff and on the merged tree merged2. merged2 is a local merge f2b6d1d99 of 0a1f8900c with develop 1125607e9 (#1010's squash; develop moved mid-gate). It was never pushed and its audit rows match head.
Gate ran 2026-09-17 04:21:54-04:49 AEST (clocks from date).
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-0a1f8900c-tier1-r1/report.md
(evidence/ holds the scripts and raw outputs; NOT-TESTED.written-first.md was written at 04:22, before any run.)
No rendered surface, so the real-browser half of tier 1 does not apply.

BLUF
1. Under NODE_ENV=production the fix does not land (MEASURED, real app, both trees, replicated). docker-compose.production.yml:81 sets that mode (READ).
   - Production 307s every unversioned /api/* to /api/v1/* above the audit mount.
   - After the 307, head audits every refused POST /api/gdpr/erasures as v1.erasures / v1 at /api/v1/gdpr/erasures, never gdpr.create. Base audits them as unknown.create at /.
   - The no-credential class, which base already got right in production (gdpr.create), regresses to v1.erasures.
   - Major, PR.
2. "Admitted requests unchanged" is FALSE. The census: 1115 requests over 119 routes enumerated from source by the TS parser (planted-mount control +2 found, 2 commented plants absent), matched by User-Agent, 0 orphan inserts. Each row was classed against D3 (entry-time canonical req.path, index.ts:566-569's declared intent):
   - NODE_ENV=test: FIX 100 / REGRESSION 328 (132 admitted, 196 refused) / changed-both-wrong 51 / same 531 / pre-existing 105. The regressions are every /api/v1/ spelling (v1.*), every // spelling (raw details.path), every #frag and every absolute-form target.
   - NODE_ENV=production: FIX 5 / REGRESSION 522 (63 admitted, 459 refused) / both-wrong 128 / same 19 / pre-existing 441. Even the CONTROL POST /api/logs goes logs.create -> v1.create.
   - Major, PR.
3. The request target sets the audit action / resource_type.
   - POST http://qa-anything.invalid/api/v1/gdpr/erasures -> action qa-anything.invalid.v1 on head (production too).
   - /api/logs#qa -> logs#qa.create.
   - Major, PR.
4. PRE-EXISTING SECURITY, NOT THIS PR (base == head): an absolute-form request target bypasses the KS-843 erasure door's scope/role gate. Escalation candidate.
   - Setup: connector without subjects:erase, ENFORCED.
   - POST http://<any host>/api/gdpr/erasures -> 200 and originate received the POST. The origin-form control is 403 with no upstream hit.
   - The GET status read is bypassed the same way, and the user role too.
   - In production only the /api/v1/ absolute form gets through (200, originate hit); the unversioned form is 307'd and refused.
   - A credential is still required: none -> 401, invalid -> 401.
   - Replicated 2x on each of base/head x test/production (evidence/bypass_run.out).
   - Suspected mechanism (READ only): the proxy.ts:734-745 wrapper collapses // across the whole req.url, so http://h becomes http:/h and the /erasures door mount never matches.
   - Severity Blocker-class for the TICKET (KS-843/KS-858), conditional on two NOT TESTED facts: the edge forwards absolute-form targets, and originate does not re-check scope.
5. Test quality (Minor, PR, SHIPS-WITH the fix): the suite pins no non-gdpr row, no /api/v1 row and no production-mode row. G-NONGDPR 0, G-V1 0, G-D3 0 and TE 0 reds all compile, all 406/406.

ITEMS
1. Parity, per route class:
   - Test env: canonical single-slash non-v1 requests are unchanged for admitted rows, except fixes on HPM-proxied mounts (stake.create /api/stake -> staking.create). Refused rows inside use-mounts are FIXED (27 no-auth, 15 user/admin, 15 query, 15 trailing).
   - /api/v1/*, //, #, absolute-form: REGRESSED for admitted AND refused.
   - Production: almost every audited write is regressed to v1.* (522).
   - Head vs merged (identical trees): 1115/1115 identical rows. merged2 == head and base2 == base on all 1115 rows in both envs, so the develop move is audit-neutral.
2. Refusal classes (POST /api/gdpr/erasures), test env:
   - Already right on base: no credential (spec gate index.ts:1044), connector GRACE admitted, originate 400/422, and 405 PUT/DELETE/PATCH.
   - Wrong on base, right on head: invalid token 401, scope 403, role 403 (ENFORCED and GRACE), trailing slash, //erasures (head writes the RAW path), ?x=1, /api/gdpr/ERASURES.
   - Still wrong on head: /api/v1/gdpr/erasures (v1.erasures), #x (path includes #x), absolute-form (127.0.0.1.gdpr, and the door is bypassed), /api/GDPR/erasures (GDPR.create; D3 too).
   - Not audited at all on either tree: /API/GDPR/ERASURES.
   - No rate limiter is mounted on the route.
   - Production: no refusal class is right on head (all v1.erasures), and no credential regresses.
3. Timing (MEASURED, shape fixture plus the REAL createProxyRoutes door):
   - Express trims req.url/path on entry to each use-mount (/erasures inside the wrapper, / inside the gate) and restores it only inside next(). A responding gate stays / at finish, finish+setImmediate and finish+50ms.
   - An admitted request answered inside a use-mount is also still trimmed at finish.
   - C2's mechanism is right. The READY's "trimmed after the response is sent" is wrong.
   - D3 (entry-time canonical req.path for both fields) carries the fix in both envs without the item-1 regressions (the whole suite is 406/406 on it). The timing is the fix; the originalUrl SOURCE breaks parity.
   - Nested-mount Record: under app.use('/gw', ...) head writes api.x and api.create for the admitted row too; base unknown.create /x; D3 correct. The only production mount is index.ts:570 (root).
4. GET clause: AUDITED_METHODS has no GET. A refused GET /api/gdpr/erasures/abc writes no row on any tree, in either env. That clause of KS-871's acceptance is unmeetable through the audit log (Record for KS-871; TG reds exactly the GET cell).
5. The other three req.path reads (:256, :283, :328) are unchanged by the diff.
   - An origin-form proxied login has the full path on base (auth.login).
   - A login-limiter 429 IS trimmed on base (unknown.create /); head writes auth.login in test and v1.login in production.
   - /api/v1/auth/login is v1.login on both trees, and in production every login is v1.login on both (pre-existing).
   - H29 attemptedEmail is NEVER written for any proxied login spelling (pre-existing, TICKET).
6. READY accounting (TS scanner): head's product code tokens equal A0+B0 exactly; all other changed lines are comments (declared). B0's context lacks base's "// Trim trailing slashes" line, which confirms the hand apply. The test files vs A1/B1 (applied with --recount) show only the declared edits (typed Mock/makeQuery, flag restore in finally, the GET cell); 0 undeclared. The header de-indent is RELAYED.
7. Failure paths: isDbAvailable false -> no row on either tree. Sink throws or hangs -> response unchanged (status and body, 0-3 ms) on both trees; the row is attempted on both. isDbAvailable liveness cannot be measured in-process.
8. Tampers (whole suite, 49/406 asserted every row, project tsc rc 0 every row, restore sha-identical, 0 pending/skipped): T0 0 | TA 1 | TB 2 | TAB 3 | TG 1 | TE 0 | TI 0 | G-CTRL 1 | G-NONGDPR 0 | G-ADMITTED-ONLY 1 | G-D3 0 | G-V1 (QA) 0 | T0-after 0. All as predicted. The ones the suite cannot see: TE, G-NONGDPR, G-D3, G-V1.
9. Suites: base 47/400, head 49/406, merged 49/406, base2 (1125607e9) 47/408, merged2 49/414, all pass. Project tsc rc 0 on all (its program has 0 __tests__). Including tsc:
   - Program: tsconfig.qa-including.json {"extends":"./tsconfig.json","include":["src/**/*"],"exclude":["node_modules","dist"]}, run from services/api-gateway; --listFilesOnly shows all 3 PR files; the planted control gives +1 TS2322.
   - Errors: 35 lines / 11 files on base, head and merged; 30/10 on base2 and merged2; 0 in the PR files; NEW 0.
   - The seat's 54 lines with TS2741 come from a program rooted at Blockchain/Dev (two @types/node copies). That is a Record.
   - eslint: 0/0 on the 3 files.
10. Linear (re-read 04:48:59): attachmentsForURL(pull/1011) = KS-871 [In Progress] contributes, only. KS-843 and KS-858 have no #1011 attachment. 0 closing phrases in title, body, commit and comments (regex controls Fixes KS-871 / closes #12 fired). KS-858 is 0x in the body (only in the linear[bot] comment), so the READY is imprecise (Record). KS-871 must NOT go Done on merge.
11. Disjointness: 21 open PRs, 0 overlap with the 3 files, 0 touch audit.ts / index.ts / proxy.ts / versioning.ts / normalisePath.ts / db.ts / auth.ts. #1010 is merged as 1125607e9 (verification.ts + ks1087 test), which is file-disjoint and audit-neutral.
12. Schemathesis/Akto: NOT APPLICABLE. Every hop's status, non-volatile headers and FULL body were compared, base vs head and base2 vs merged2, test and production, with head vs merged as the noise pair: 0 status diffs and 0 product-caused diffs. Two flagged production diffs were timestamp-only and are retracted. The PR changes only the persisted audit row.

SEAT CLAIMS
C1 refuted as stated (test-env origin-form only; fails in production and for /api/v1; "admitted unchanged" false) | C2 confirmed, incomplete (source) | C3 confirmed | C4 unchanged confirmed; 429 trimmed on base; email never written | C5 confirmed | C6 confirmed | C7 confirmed at d067725ff, re-measured 49/414 on the new develop; tsc program-root Record | C8 no response change confirmed; S/A N/A | C9 links confirmed; KS-858-in-body refuted.

MERGE ADDENDUM (for a fixed head; this head is NO GO)
"squash 0a1f8900c onto develop 1125607e9 (then-current; d067725ff at PR time; file-disjoint from #1010, merged); #1011 attaches to KS-871 only, linkKind contributes — KS-871 stays In Progress on merge (§5f: runtime behaviour); equality targets audit.ts f5a83ba2c / ks871 Part A 8d66dfaf7 / Part B 3171d1eff; api-gateway 47/400 -> 49/406 at d067725ff, re-measured 47/408 -> 49/414 on 1125607e9; Records: R-1 nested mount mis-derives (root mount only), R-2 GET clause unmeetable via the audit log (KS-871), R-3 H29 attemptedEmail never written + login-limiter 429 trimmed on base (TICKET), R-4 /API/... not audited + case-split action namespace, R-5 production audit trail already v1.* on base for mounted/proxied routes (TICKET), R-6 seat including-tsc program root, R-7 KS-858 not in body, R-8 READY comment mechanism false, R-9 stale denominators."
Test-quality finding for the owner: F-1011-5, target PR, SHIPS-WITH the fix. Add real-app cells for a canonical non-gdpr row, a /api/v1 row, and a refused erasure under the production 307.
Measured counterfactual D3 (entry-time canonical req.path into both fields): fixes every gdpr refusal class in both envs. It also moves the pre-existing production v1.* base rows toward canonical. The fix itself is the owner's; not commissioned.
ESCALATION CANDIDATE: F-1011-4, the absolute-form erasure-door bypass. It is a TICKET, not #1011; routing and priority are yours and Kam's.

NOT TESTED (same prominence)
- The §5f live sweep on a rebuilt stack (Sunday).
- A real Postgres audit_logs write (RLS, UUID columns).
- Any deployed environment's NODE_ENV, and whether its clients call /api/v1.
- nginx / Container Apps request-target rewriting. This decides F-3 and F-4 severity.
- Whether originate re-checks subjects:erase (decides F-4).
- Out-of-repo audit consumers (SIEM, dashboards, the security-service reader).
- Playwright / k6 (no UI; not commissioned).
- Schemathesis / Akto runs (ruled N/A).
- Preflight legs 3/4/8.
- The packages/shared suite (identical tree).
- The audit.ts:328 warning-log content.

docker info ran once:
docker_info_rc=0

HARNESS SELF-AUDIT
- Run 1's JWTs lacked verificationLevel, so originate proxies 500'd. Diagnosed, quarantined, re-run.
- The production boot failed twice: CSRF_SECRET missing, then my runner popped DATABASE_URL/REDIS_URL after setting them. Quarantined, fixed.
- Three item-2 cells first drafted from run-1 data were corrected in the open in the report.
- Checkout bounds (start 04:22:56 / mid 04:39:58 / close 04:45:23): porcelain 0/0/0; refs 897/898/899; .git/worktrees 110 x3 (worktree list 111); refs/pull/1011/head 0a1f8900c x3; develop d067725ff -> 1125607e9 at mid.
- .git/config sha256 bb55e140 -> d7e7298b between start and mid, not by this gate (read verbs only; another session).
- 0 checkout .vite entries are newer than my setup (control: 12 older ones). No container, no push, no write to GitHub or Linear.

