SUBJECT: [QA -> Wednesday] TIER 1 GATE #1023 (KS-1207) 2f74491eb — GO WITH FINDINGS
TS: 2026-09-17T09:05:07.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA agent -> Wednesday. TIER 1 ROUND 1 gate, Secuura/Blockchain PR #1023 (KS-1207) @ `2f74491ebd6211e722f778838339c55e8add008d`. Session 18:44:17 -> 19:04 AEST (clocks from `date`). Findings-only: nothing fixed, merged, pushed, commented, filed or ticked; no container; nothing to Peter or Stuart.

## BLUF
GO WITH FINDINGS on `2f74491eb`, as the delta over develop `581c9db0d`, AND on the merged tree `985e615cc1f05e4da1e3c052a007c58bdfed8d69`. That is head merged with the then-current develop `81ee4b729` (local --no-ff merge `5f4b3278d`, never pushed; equals the drafter's OID). Over `581c9db0d` the merged tree is `4bdf1b8c7`, the head tree.

- The KS-1207 bypass is CLOSED on the real app on all 8 `authenticateToken(false)` mounts (census from source), `/api` + `/api/v1` in test, `/api/v1` in production, head and merged.
  - 0 of 112 graded rows answer 2xx or reach the upstream: 72 census rows, 16 closed-port rows, 24 non-GET rows.
  - The same grader finds 79 at develop.
- No legitimate caller changes.
  - Head vs develop: 1,255 cells per tree, 222 differ, every one in an intended class (live / store-down / revoked JWT + a key that did not validate).
  - Head vs merged: 0 differ.
- A validation outage is not a silent downgrade to anonymous. It is a principal switch to the JWT user, and it lasts up to 30 s after recovery (Record R-2).
- NEW, not this PR's (identical at develop): N-1, Major severity / Low likelihood, TICKET. A revoked-session JWT plus a VALID key whose connector-token exchange fails is forwarded with the revoked user's Bearer and 0 session checks, on all 10 probed mounts including required ones.

## Plain statements, items 1-10

1. BYPASS, lead Q1.
   - CLOSED. Census READ at head: 8 = proxy.ts `:641` certifications, `:942` credentials, `:1025` referrals, `:1114` governance, `:1131` nft, `:1180` billing; admin.ts `:1455` GET settings/notifications, `:1483` GET privacy/settings. No alias, no router mounted twice.
   - Head / merged: revoked JWT + {junk, validate 500, validate socket destroyed, validate closed port} -> 401 `SESSION_INVALIDATED`, 0 upstream hits, session check ran, on every mount x prefix x mode.
   - Develop: 5 proxy mounts 200 forwarded with the revoked Bearer; 2 local GETs 200; certifications 401 via requireScope.
   - Production unversioned `/api/*` -> 307 on all trees.
   - Oracle trap confirmed: 60 revoked + VALID-key rows per tree are 2xx on all three trees (connector branch), graded separately.

2. LEGITIMATE CALLERS, lead Q2.
   - No Blocker. L1-L7 and L9 are identical head vs develop (valid key alone = connector + key tenant + connector-token Bearer; live JWT alone; live JWT + valid key -> the connector wins on BOTH trees; anonymous; junk alone anonymous; required mounts 401 "Invalid API key" with or without a JWT; `pk_` / `SK_` not a presented key).
   - The connector branch body is byte-identical (2,451 bytes, control fires).
   - L8 intended: live JWT + failed key -> the JWT user + JWT tenant.
   - The 3 unnamed mounts change in the intended direction with no seat cell (R-1): certifications live+junk 401 -> 200 as the user; the admin GETs revoked+junk 200 -> 401. The drafter's "user's own settings" was not measurable (db mocked).

3. LIMITER / TENANT.
   - Intact, head = merged = develop apart from the principal on the intended classes.
   - Junk key alone and beside a live JWT (one key and unique keys): 0 incr, no RateLimit headers.
   - Valid rl3 alone and beside a live JWT: 1 incr per request, 429 on the 4th. Valid rl2 beside a live JWT on certifications: 429 on the 3rd.
   - Fall-through `runWithTenantId` = the JWT tenant `a000...0001` (develop: not called).
   - No optional chain passes authenticateToken twice (READ); 1 incr per request on the most layered optional chain.

4. COULD-NOT-VALIDATE, lead Q3.
   - No silent downgrade. With no Bearer, 500 / destroyed / closed-port rows = develop (anonymous; certifications 401).
   - Live JWT -> the JWT user (develop: anonymous with the Bearer forwarded). Revoked -> 401 (develop: forwarded).
   - `validateApiKey` already returned null for all classes and caches a 5xx 30 s (pre-existing).
   - NEW measurement (flap key): after the security service recovers, the cached 5xx keeps a key + live JWT caller on the human principal for up to 30 s. R-2 is a Record, SHIPS-WITH.
   - Required mounts answer "Invalid API key" during an outage: R-4, pre-existing.
   - Sibling re-measured = N-1 (below), identical at develop, NOT this PR's: NEW, TICKET.

5. TAMPERS on the WHOLE suite at HEAD. Every row: 56/550, pending 0, tsc 0, anchor 1, sha-restored, git diff --quiet; 0 VOID.
   - Seat rows (drafter forms; seat forms not entered): T0 0, TBYPASS 10, TSKIPSESSION 5, TNOBEARER 5, TREQ 1, TI 0.
   - Red-proof: whole suite 10; ks1207 test solo 10 red / 16 green of 26, all AssertionError.
   - TREQ first read 4: 1 tamper red + 3 ks864a/b/c 5 s timeouts at host load avg 45 (the #1022 and #1024 gates were running). Re-run alone: 1 red, 0 non-assertion. Curio C-1.
   - Drafter rows: G-PRECEDENCE 0, G-ERRMETA 1 (auth.test.ts), G-JUNKBUCKET 0, G-TENANTDROP 0, G-PREFIXFREE 0.
   - Mine: N-ERRONLY (the session check skipped only when validation ERRORED) 0 reds: the bypass could return for the unreachable class with the suite green. N-NONOKMETA (5xx -> truthy meta) 1 (auth.test.ts).
   - My probe sees every G/N tamper: 89 / 23 / 115 / 14 / 68 / 63 differing cells.
   - F-1 Minor: no suite cell sees precedence, no-bucket-on-fall-through, the JWT tenant on fall-through, the sk_ prefix rule, or the errored-validation session check.

6. SUITES.
   - api-gateway: head 56/550, develop 55/524, merged 56/550, 0 failed, project tsc 0 each.
   - packages/shared at head: 44/851 (shared tree identical on all three).
   - Test-including tsc program: head 592 / develop 591 / merged 592, the ks1207 test in it (control: the project program, 491 files, excludes it), 31 lines / 11 files each, 0 in touched files, NEW 0, plant +1 restored.
   - eslint auth.ts: 1 `@typescript-eslint/no-unused-vars` "'error' is defined but never used." at head = develop; the test 0; firing controls rc 1.

7. MERGE COMMITS.
   - auth.ts `b8fce678a` and the test `f56bd48b9` are identical at `0f8b699b4` and the head.
   - diff develop..head = exactly those 2 files (control d7e95cd9f..head lists 6: fires).
   - merge-tree in MY clone: head x 81ee4b729 = `985e615cc`; head x 581c9db0d = `4bdf1b8c7` = the head tree.

8. LINEAR / GITHUB at 18:54:36 and 19:02:30, identical.
   - attachmentsForURL(pull/1023) = [KS-1207 contributes]; controls pull/1019 = [KS-843, KS-1187 contributes], pull/99999 = [].
   - 0 closing phrases in title, body (KS ids {KS-1207}) and all 3 commits; planted controls 5/5.
   - KS-1207 In Progress; comment 1c90d0fc says build-after-1019 and stays In Progress. KS-1207 stays In Progress on merge (§5f).
   - compare now ahead 3 / behind 1 (develop moved to 81ee4b729; drift, judged by content: api-gateway and shared trees identical).
   - PR files show no rendered surface: the real-browser half of tier 1 does NOT apply.

9. KS-736 RESIDUAL, NOT this PR's.
   - Junk key alone -> 200 forwarded anonymous on the 5 proxy mounts while no credential -> 401 (`index.ts:1072-1075` counts the header). Identical on all trees. TICKET KS-736.

10. RULINGS.
   - Schemathesis / Akto are NOT REQUIRED for this merge. The decision space (2 headers x validity / session / exchange / signature states) was driven directly: 1,255 cells per tree, 0 unintended diffs. The spec gates are unchanged, and a schema fuzzer cannot construct revoked sessions or failing validations.
   - They ARE required for closing KS-1207 (the edge + the upstreams' authenticate()).
   - Real-browser half: N/A (measured).

## CLOSED / STILL OPEN / NEW
- KS-1207 bypass (gateway): CLOSED. MEASURED AT RUNTIME. PR. SHIPS-WITH. The upstreams and the edge are NOT TESTED.
- #1017 gate R-4 (unknown sk_ key on optional mounts): CLOSED for the revoked-Bearer consequence. The junk-alone forward is STILL OPEN as the KS-736 residual (TICKET).
- N-1: revoked JWT + VALID key + connector-token exchange failure -> revoked Bearer forwarded, 0 session checks, 10/10 mounts incl. required. NEW, pre-existing (= develop). MEASURED + READ. Major severity / Low likelihood. TICKET; escalation candidate. The auth.ts comment says the header is "left unset" on exchange failure; it is left AS SENT. Inducement path READ: auth's own validate refusing a key the gateway still caches valid (60 s), or a 502. Attacker control NOT established. Fix-shape: delete `req.headers.authorization` when `getConnectorBearer` returns null.
- F-1: the suite cannot see precedence / no-bucket / tenant / prefix / errored-validation session check. NEW. MEASURED. Minor. SHIPS-WITH; cells on a ticket.
- R-1: 3 unnamed mounts' behaviour change. Record. SHIPS-WITH.
- R-2: could-not-validate -> Bearer principal (+30 s post-outage). Record. SHIPS-WITH.
- R-3: session store down + junk -> the JWT user (KS-257 fail-open). Record.
- R-4: required mounts say "Invalid API key" during an outage. Record, pre-existing, TICKET-candidate.
- R-5: BADSIG Bearer forwarded anonymous on optional proxy mounts. Record, pre-existing, TICKET-candidate.
- Disagreements 1-5: 1 CONFIRMED (R-1); 2 CONFIRMED (N-1); 3 Record (R-2); 4 F-1 (plus my N-ERRONLY gap); 5 CONFIRMED.
- Open question (not categorised): `/api/batch/*` derives the user via getUserId and is mounted before any authenticateToken. NOT TESTED; flagged.

## MERGE ADDENDUM
"squash 2f74491eb onto develop 81ee4b729 (then-current at 19:02:12; 581c9db0d = the head's second parent) (merged tree 985e615cc1f05e4da1e3c052a007c58bdfed8d69 over 81ee4b729; drafter 4bdf1b8c7 over 581c9db0d = the head tree, and 985e615cc over 81ee4b729, both reproduced in the gate's clone); #1023 attaches to KS-1207 only, linkKind contributes, no closes — KS-1207 stays In Progress on merge (§5f: the upstream services' acceptance and the edge are unmeasured); equality targets after the squash: auth.ts blob b8fce678a / ks1207 test f56bd48b9; api-gateway 55/524 at 581c9db0d -> 56/550 at head -> 56/550 merged; packages/shared 44/851; dispositions: KS-1207 bypass CLOSED SHIPS-WITH; F-1 Minor SHIPS-WITH (cells on a ticket); R-1..R-5 Records SHIPS-WITH; KS-736 residual TICKET (KS-736); NEW: N-1 (Major severity / Low likelihood, pre-existing = develop, NOT this PR's) revoked-session JWT + VALID key whose connector-token exchange fails forwards the revoked Bearer with 0 session checks on all 10 probed mounts incl. required — TICKET, escalation candidate; F-1's N-ERRONLY gap (0 suite reds) — TICKET cells; Records for KS-1207's facts comment at merge: the 3 unnamed optional mounts' behaviour change, could-not-validate -> the Bearer principal (for up to 30 s after recovery via the 5xx negative cache), the KS-736 residual (junk key alone forwarded on bearerAuth ops, index.ts:1072-1075) NOT this PR's, required mounts answer 'Invalid API key' during a validation outage (pre-existing), BADSIG Bearer forwarded anonymous on optional proxy mounts (pre-existing)"

## NOT TESTED (equal prominence)
- The edge (nginx / Caddy / Container Apps ingress).
- The running vc-issuer / referral / governance / nft-certificate / billing / originate services and their authenticate(). Whether they accept a forwarded revoked Bearer is RELAYED, and N-1's real impact depends on it.
- A real security service (/api/keys/validate) and auth (/internal/connector-token, JWKS).
- A real Redis session store and limiter store; a real Postgres (admin GET bodies not compared).
- Preflight legs 3/4/8; demo; any container (docker info rc 0, run once, nothing created).
- Schemathesis / Akto / k6 / Playwright (not commissioned).
- Non-GET operations beyond the 2 the spec method gate lets through.
- Concurrency and cache races; clock-driven cache expiry; x-tenant-override on the fall-through; test tokens; duplicate x-api-key; spoofed inbound x-user-id; /api/batch.
- packages/shared at develop and merged (identical tree).
- Seat A's exact tamper forms (seat worktrees not entered).

## Bounds
- Secuura checkout START 18:45:52 / MID 18:55:39 / CLOSE 19:02:12: porcelain 0, .git/config sha256 d7e7298b02c45f52, for-each-ref 925, .git/worktrees 112, branch feature/ks-597-b-caller-scoped-externalref, origin develop 81ee4b729, refs/pull/1023/head 2f74491eb. Equal at all three.
- Listeners: START 10 pids / CLOSE the same 10 pids, 0 with cwd under my workdir, login_stub.mjs 0 at all three readings. No SIGTERM needed.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/ (report.md, NOT-TESTED.written-first.md, evidence/)

