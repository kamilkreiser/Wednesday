# QA gate: Secuura PR #1518 (ticket KS-1532), tier 2

- Head under test: 7bc83d75708fa226f309cc0881b4f09fddc9792d (matches the fetched refs/pull/1518/head exactly)
- Base: f39104e71688e2c3b071bbc7380f4b259f0f204a (PR #1517 squash)
- Develop now: b2085e99ff1ce3604d592c980c700fe6eccce6c5 (`git ls-remote origin refs/heads/develop`, read myself)
- Tree: scratch clone `--shared` of the main checkout, fetch of refs/pull/1518/head and develop, `git archive` of head and of base into fresh dirs, node_modules as symlink shells to the main checkout (read-only), @secuura links pointing into the scratch tree, packages/shared built with tsc in each. No earlier gate results used. Nothing written under !CODING.
- Gate: Sonnet, tier 2 (small gateway-reader change, client-visible status change)

## VERDICT: GO WITH NOTE

Majors: 0. Minors: 2 (both already declared by the builder, plus one new wording point).

## Findings

Majors: none. No double-send on any path, 503 body byte-equal to the create path, healthy reads byte-identical.

Minor 1 (declared, not in this PR): the fallback half stays open. The create path (routes/verification.ts:1267) answers 503 'Connector allow-list configuration is currently unreadable...' via isRedisAvailable() BEFORE the read, for the mode where the read RESOLVES to null. The info reader (services/health.ts, RedisServiceLike at ~line 20) has no such method, so a sustained Redis outage can still answer 200 with allowedDocumentTypes [] through this route. Pinned by a control cell (ks1532 test, 'resolved null unchanged'). Needs its own ticket; the PR does not claim to close it.

Minor 2 (new wording point, low): MCP agent path. services/mcp-server/src/tools/info.ts:124,148 turns any non-ok result into the note 'Connector info not available (endpoint may not exist yet or no API key set)'. A 503 therefore reads as "no key / no endpoint" rather than "allow-list unreadable". It fails closed (the agent is shown no allowedDocumentTypes at all), so it is a message-quality point only. http-server.ts:199 `/connector` relays status and body untouched, so there the 503 text is visible.

Note (info): neither catch logs the thrown error (KS-1539, declared). Nothing internal is lost to the client, and nothing is available to operators either.

## Topology
- Base = f39104e7 = `pr1518~1`. Diff: 2 files, +240 -6 (health.ts +13 -6 net of the file stat; new test file 227 lines).
- Develop delta since the PR base: 5 files, all under services/originate (ks1293 test, two ks1508 tests, routes/certifications.ts, routes/documents.ts). Zero overlap with health.ts or the new test.
- `git merge-tree --write-tree pr1518 dev`: rc 0, tree c9172e0d8ef38354fdf62bd37fbccd18097091cd (equals the claimed c9172e0d8ef3). Clean.

## Diff read (health.ts)
- `let containerBad = false` hoisted above the try; `let containerBad = !Array.isArray(ints)` became `if (!Array.isArray(ints)) containerBad = true` (equivalent).
- Catch now answers 503 with `{success:false,error:{code:'SERVICE_UNAVAILABLE',message:...}}` and `return`s. No variable from the error is interpolated: nothing thrown can reach the body.
- Container 403 moved after the try as straight-line code; list 403 (KS-1232) untouched; success body unchanged.
- Create-path text at routes/verification.ts:1294 compared to health.ts: status 503, code SERVICE_UNAVAILABLE, message and JSON key order identical (checked by reading both literals; AGREEMENT cell also drives the real create route).
- The catch wraps the whole try (attack point 3): the only code inside beyond the read is pure property access on the parsed value, so an unexpected throw would also refuse (fail-closed direction). Acceptable.

## What I ran, and results
1. New test at head: 6 passed / 6.
2. Red-first: new test file copied into an untouched base tree, run against the base reader: 4 passed / 2 failed (the thrown table and AGREEMENT; the table shows `200 ... allowedDocumentTypes=[]` for all four thrown shapes). Matches the claim.
3. Neighbours at head: ks1232, ks1231 (both files), ks480 (three files), ks1256, ks1204: 8 files, 58 / 58 passed.
4. Full api-gateway suite at head, run twice: 117 files / 1123 tests, 0 failed, both runs.
5. tsc --noEmit -p services/api-gateway/tsconfig.json: no output (clean). (My rc echo was after a pipe, so I rely on empty output, not rc.)
6. eslint on health.ts and the new test file: no output (clean). No positive control run for eslint.
7. `check:test-types` for services/api-gateway: 152 files examined, 35 errors all in baseline, 0 new, 0 stale. (services/auth half of the script not run.)
8. Mutants, in a separate copy of the head tree, control first (6/6), restore verified by sha256 after every one:

| Mutant | Result |
|---|---|
| M1 catch swallows again | 2 failed (table, AGREEMENT) |
| M2 status 500 | 2 failed |
| M3 other code | 2 failed |
| M4 other text | 2 failed |
| M5 catch loses `return` (second send) | 1 failed: only the thrown table (response counter), as claimed |
| M6 container 403 removed | 1 failed (403s control) |
| M7 container check dropped | 1 failed (403s control) |
| M8 null read now throws | 1 failed (resolved-null control) |
| M9 default workflowPolicy changed | 1 failed (healthy byte-identical) |
| M10 catch refuses only Error instances | 2 failed (the string / no-reason / object-like shapes) |
| X1 (mine) status 504 | 2 failed |
| X2 (mine) drop authenticateToken | 5 failed |
| X3 (mine) 503 body appends the thrown error message | 2 failed (leak is caught) |

All 13 killed, all restored byte-identical.

9. Differential harness (mine, in the mutant copy, real express server, real authenticateToken(true), base health.ts vs head health.ts, fetch over HTTP): 18 stored shapes (null, {}, integrations absent / empty / null / non-array string, no matching entry, one / many types, config null / array, list empty / null / string / false, duplicate id, null entry, bad entry after a good one): status, whole body text, and headers (excluding date, etag, content-length, and x-ratelimit-remaining which is a per-call counter) identical base vs head for all 18. content-length compared and equal. 24 / 24 passed.
10. Thrown shapes over HTTP (rejected Error whose message contains `SECRET-internal redis://10.0.0.5:6379`, rejected string, rejection with no reason, synchronous throw, rejected object with a password field): head answers 503 with the fixed body every time; body contains none of the planted text. Base answered 200 with allowedDocumentTypes [] for all five.
11. Single-send counter (wraps res.json, counts second calls) across all 18 healthy / malformed / resolved-null stored shapes and all five thrown shapes: 0 second sends. Positive control: with the catch's `return` removed, the same counter test fails (so the counter can see a double send).

## Per-path table (head)

| Path | Status / decision | Sends | Checked by |
|---|---|---|---|
| Thrown: rejected Error | 503 SERVICE_UNAVAILABLE, fixed text | 1 | PR cell + my HTTP harness |
| Thrown: rejected string | 503, same | 1 | same |
| Thrown: rejection with no reason | 503, same | 1 | same |
| Thrown: synchronous throw | 503, same | 1 | same |
| Thrown: rejected object | 503, same | 1 | my harness only |
| Container malformed (integrations not an array, bad entry, duplicate id, config not an object) | 403 FORBIDDEN container text, unchanged | 1 | PR cell + my harness base vs head |
| List present but not an array | 403 FORBIDDEN list text, unchanged | 1 | same |
| Healthy: absent / null / empty / one / many | 200, body byte-identical to base | 1 | my harness base vs head, PR cell |
| Resolved null | 200 with [] (unchanged; this is the declared gap) | 1 | PR control + my harness |

## Question-by-question
- (6) Leak: the catch takes no parameter and the body is a literal. Planted secrets did not appear. X3 shows the suite would catch a regression.
- (7) Headers and timing: no Retry-After on either route (0 hits in verification.ts; neither sets a header on this path). Response headers match the healthy-path set (content-type, keep-alive, x-powered-by, x-ratelimit-*). Timing: the 503 returns immediately after the failed read, same shape as the create route; no extra awaits were added.
- Attack point 4 (AGREEMENT stubs enforcement helpers): the stubs sit AFTER the allow-list read on the create route and cannot influence the 503; the create route's real authenticateToken is stubbed in that cell, but the info side uses the real one. Fine.
- Attack point 5 (e2e specs): tests/e2e/tests/full-lifecycle-e2e.spec.ts:194 and mcp-server.mcp.spec.ts:84 GET MCP_URL (default http://localhost:6023, the MCP server) /api/connector/info with no API key. The MCP server has no such route (its own relay is `/connector`) and an unauthenticated gateway call would be refused before the reader, so a 503 cannot reach these assertions (`status < 500`). Traced by reading, NOT RUN.

## NOT TESTED
- The two e2e specs (need a live stack and MCP server): reasoned only.
- A live Redis outage, or the real redis service module's getNotificationSettings throwing (SyntaxError from malformed stored JSON, MaxRetriesPerRequestError): shapes were simulated.
- The real production mounting in index.ts (the module is passed as redisService; I did not trace it).
- services/auth half of `check:test-types`; the hook's 16 legs (I did not run the builder's hook); other workspaces' suites; docker / deploy.
- eslint positive control; unauthenticated / non-connector 403 path (unchanged lines, not re-driven in my harness beyond the X2 mutant).
- Actual timing measurement (reasoned only).
