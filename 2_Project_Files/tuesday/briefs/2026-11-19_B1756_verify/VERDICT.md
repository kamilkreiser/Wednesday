GATE B1756: GO WITH FINDINGS @ 18c490c on main b0499db

Tier G1 (security: authentication bypass on the Marketplace SaaS webhook). Round 1 of 2. Reviewer: Opus 5.5, in-session, independent of the builder.
Clocks AEDT 2026-11-19: first `date` 20:25:32. Work: own clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s294/g1756/clone` (push URL `invalid://no-push`), with worktrees `head`, `main`, `t445`, `v6` (head, jest slot 8) and `vA` (T445, jest slot 8).

Blocker 0 | Major 0 | Minor 4 | Info 3

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Minor | M-1. The committed cells cannot see a weakened verification. With `jose` mocked, my mutant M10 dropped `audience` from the `jwtVerify` options and stayed 20/20 green. My mutant M9 widened the flag test (trimmed, so ` true ` would be honoured) and also stayed green. This is residual (a), and the texts state it honestly (test docblock :6-7, the T445 message, the STATUS NOT TESTED, the PR body). It is no worse than stated, but it means "same options as flag-unset" is proved here only by this gate's real-library run (section REAL LIBRARY), not by any committed cell. | Follow-up ticket (not this lane): a plain-node or ESM-capable cell that loads the real `jose` against a loopback JWKS. This gate's `progs/sig.js` shows that this works without jest and without network. |
| Minor | M-2. Cell C2 pins source text: `process.env.NODE_ENV` must occur exactly once in `backend/marketplaceJwt.js` (test :189-193). It is one of the 8 red-first cells, so red-first rests partly on a text count. A future harmless refactor that reads NODE_ENV twice reddens it with no behaviour change. | Accept for this lane; replace it later with a behaviour cell. R1-R6 already carry the property. |
| Minor | M-3. The kit's frame figure was off by one. The kit gave 469/387 (`.js` / `.test.js` under `__tests__` and `tests`) at drafting main 9373976e. I measured 468/386 there by `git ls-tree`, 470/388 at BASE and 471/389 at head. The builder's Corrections 4 (470/388, two N-F files named) is TRUE; the gap is in the drafter's figure. No product effect. | None for landing; note it for the drafter form. |
| Minor | M-4. Unshown builder claims. STATUS Step 0 says the B1737 kit was not read whole and the landing rule `CLARIFICATIONS.md:2067` was not printed (the builder relied on the kit's own quote). The B1737 chain log was not read. No product effect. | None for landing. |
| Info | I-1. Residual (b), measured. With the flag `true`/`TRUE`, NODE_ENV `prod`, `staging`, `development`, `test`, empty or unset still skips verification (matrix below). It is not worse than stated: every shipped run path sets `production` exactly (Dockerfile:144, docker-compose.yml:37, docker-compose.dev.yml:12, mainTemplate.json:541, deployment/printer-dashboard.service:11, .env.example:2, package.json:7 `npm start`). Only `npm run dev` (package.json:13) or a bare run with no environment gives a non-production value, and server.js:1045 then fills `development`. No shipped template sets `AZURE_MARKETPLACE=true`, so the router exists only on a hand-configured instance (`.env.example:45` has it commented out). | Keep the wording in the PR and merge body (done). A boot-time refusal (bootPreflight) remains LEFT FOR OTHERS. |
| Info | I-2. Pre-existing, out of lane, not changed. `backend/marketplaceJwt.js:150` logs `e.message`, which for an issuer failure includes the token's `iss` (:96). That claim is only reached after a valid signature, so a caller without a valid key cannot set it. `_jwks` (:39-50) caches the first JWKS URL for the process. `MARKETPLACE_JWKS_URL` / `MARKETPLACE_AUDIENCE` (:82-83) are operator settings that decide what "verified" means. | None for this lane. |
| Info | I-3. Pre-existing, out of lane, UNMEASURED at run time. The router's `/subscriptions/*` and `/subscriptions/usage` routes (marketplace-api.js:87-94) never call the token verifier. `resolve` and `activate` are always-public by design (server.js:2250-2251). The rest sit behind the global `requireAuth` (server.js:2905) and CSRF (only `/api/marketplace/webhooks/` is CSRF-exempt, server.js:1546). The webhook path itself is not in `alwaysPublicPaths` (server.js:2223), while `requireAuth` is mounted before the router (server.js:22491). I did not run whether that refuses Microsoft's webhooks on an auth-enforced instance. | Tuesday: worth a separate read; not a defect of this change. |

No path skips verification in production at head. No Blocker.

## THE BYPASS MATRIX (measured)

How: a fresh `node` process per cell (77 cells per tree; `progs/matrix.py` runs `progs/cell.js`), not jest. It does a real `require` of `backend/marketplaceJwt.js` with the REAL `jose` 6.1.3. The real logger is required, but its warn/error/info methods are swapped for recorders before the module loads. Each process gets a clean environment (`env` holds only PATH, HOME, the two names under test, `MARKETPLACE_AUDIENCE=gate-aud` and `MARKETPLACE_JWKS_URL` pointed at closed loopback port 9). `globalThis.fetch` is wrapped and refuses any host but the loopback address; the hosts seen were the loopback address only. Each cell builds `jwtMiddleware()` (factory time), then sends:

- a self-signed RS256 JWT (throwaway key, made in-process);
- `Bearer not-a-jwt`;
- no header;
- a `Basic` header.

S = skips (next called, payload `skipped`); v = verified (forged and junk both 401 `INVALID_TOKEN`, next 0).

```
HEAD 18c490c
flag \ NODE_ENV production Production " production " PRODUCTION prod production\n staging development test empty unset
true            v          v          v              v          S    v            S       S           S    S     S
TRUE            v          v          v              v          S    v            S       S           S    S     S
1               v          v          v              v          v    v            v       v           v    v     v
yes             v          v          v              v          v    v            v       v           v    v     v
" true "        v          v          v              v          v    v            v       v           v    v     v
empty           v          v          v              v          v    v            v       v           v    v     v
unset           v          v          v              v          v    v            v       v           v    v     v
MAIN b0499db: rows true and TRUE are S in all 11 columns; every other row v.
```

- Head: 12 skip cells, all {true, TRUE} x {prod, staging, development, test, empty, unset}. Main: 22 skip cells.
- The 10 cells that skipped at main and verify at head give answers equal to main's flag-unset production answers (10 of 10).
- In the 55 cells that verify at main, head's answers are equal (55 of 55).
- No header and `Basic` give 401 `INVALID_AUTH_HEADER` in all 77 cells at both trees.
- Head factory log: an error line in 10 cells (flag on, production forms), a warn line in 12 (flag on, non-production), and nothing otherwise. Head per-request error line: 10 cells.

Other ways an operator-believed-production deployment could still skip. Each was enumerated BY PROGRAM at head (`git grep -n -I -i -E 'SKIP_JWT|skipJwt|skip_jwt'` over all tracked files; control: the module's own lines are found):

- Flag occurrences: `backend/marketplaceJwt.js` (:65-66 the only READER; :106, :116, :118, :120, :134, :137, :139 text and calls), `scripts/test-marketplace-webhook.js:7, :31` (the hand-run smoke script; it sets NODE_ENV development itself; not copied into the image: Dockerfile copies `scripts/seed/` only, Dockerfile:52), `HISTORY.md:1104, :1146`, and the new test. There is no second reader and no other skip path.
- Callers: `jwtMiddleware(` is called only at `backend/marketplace-api.js:83` (require :37), inside `getRouter()`. `getRouter()` is mounted once at `server.js:22491`, and the router is built once, under `isAzureMarketplace && !isAzureManagedApp` (server.js:778-779). So there is one module instance and one factory call per process, with no per-request re-creation.
- NODE_ENV at factory time vs request time: both read `process.env` at call time. The only runtime writes to NODE_ENV in `backend/` are `server.js:1045` (fills `development` when unset) and none to the flag. The full scan of `process.env.X =` writes found only logger.js:24 LOGS_DIR, :1045, and OLLAMA/AZURE_OPENAI fills. So the two reads cannot disagree on a production instance. `dotenv` (server.js:81) does not override variables already set.
- Order: the HMAC check runs first (`marketplace-api.js:82`, fails closed with 503 when the secret is unset, :119-123). The JWT check is second (:83), so an anonymous caller never reaches either new log line.
- Test helpers: no `__tests__/**` file is copied into the image (Dockerfile COPY list :23-75 names backend, static, docs, development, scripts/seed and root files).

## WHAT THE VERIFIER DOES WHEN IT RUNS
With the flag refused, the request falls through to the unchanged `try { validateMarketplaceToken(bearer, opts) }` (`marketplaceJwt.js:145-155`): the same function, the same options and the same 401 bodies (`Invalid token` / `INVALID_TOKEN`; `INVALID_AUTH_HEADER` from the unchanged header guard :124-131, which still runs first). Measured equal to main (matrix above and REAL LIBRARY below).

The three new log strings (:118, :120, :137) are fixed ASCII. They name only the two variable names, and the caller controls no part of them. The factory line is written once per `jwtMiddleware()` call (once per process). The request line is written once per webhook request that meets the flag in production, and only after the HMAC check passed, so an unauthenticated flood cannot multiply it. No token, header or error detail is added to any response or new log line.

## THE REAL LIBRARY (the gate's own evidence for residual (a))
How: `progs/sig.js` runs in plain `node` v26.13.0 with the real `jose` 6.1.3 (require of the ESM package works in plain node). A throwaway RSA key A is served as a JWKS by a loopback-only HTTP server on an OS-chosen port. A second key B is never served. `fetch` refuses any host but the loopback address, and nothing reached Microsoft. The run was repeated for head with flag `true` + NODE_ENV `production`, head flag unset + production, head flag `true` + development, and main flag unset + production.

| token | head, flag true, production | head, flag unset, production | main, flag unset, production |
|---|---|---|---|
| A1 signed by the served key, right aud and iss (POSITIVE CONTROL) | accepted, payload sub from token | accepted | accepted |
| A2 signed by another key, same kid | 401 INVALID_TOKEN (signature verification failed) | same | same |
| A3 alg none | 401 (Unsupported alg) | same | same |
| A4 payload changed after signing | 401 (signature verification failed) | same | same |
| A5 wrong audience | 401 (unexpected aud) | same | same |
| A6 issuer not Microsoft (validly signed) | 401 (issuer not allowed) | same | same |
| A7 expired | 401 (exp check failed) | same | same |
| A8 HS256 keyed with the public key | 401 (Unsupported alg) | same | same |
| A9 not a JWT | 401 (Invalid Compact JWS) | same | same |

- `validateMarketplaceToken('')` throws `Empty Bearer token`.
- With the JWKS at a closed port (the matrix), every token is refused 401: it fails closed when the key fetch fails.
- In development with the flag on, all nine tokens pass as `skipped` (the kept bypass), and the JWKS is fetched 0 times.

Established: when the check runs, the real library checks the RSA signature against the served key set and enforces the alg allow-list, audience, expiry and the module's issuer regexes. Production plus flag behaves token for token like flag-unset.

NOT established: behaviour against Microsoft's real JWKS, real Microsoft-issued tokens, key rotation and the cooldown/timeout settings, or Node 24 (the CI version).

## CELLS (measured, under the lock)
- New file at head, run twice in `v6`: 20/20 green both times (suites 1, judged from the jest JSON).
- Red-first: tree `vA` at T445 `da360be15fbb` with main's module copied in (blob d2feb537adac). Received 12 green and 8 RED: R1 R2 R3 R4 R5 R6 B6 C2, equal to the STATUS claim. Reverted by copy (blob 8583d059c9b6), then 20/20 green.
- Mutants (mine; each planted by an asserted single replace, `node --check` rc 0, reverted by copy with the blob proved 8583d059c9b6 each time; `vA` porcelain empty after):

| mutant | RED cells |
|---|---|
| M1 production test inverted (`=== 'production'` to `!==`) | R1 R2 R3 R4 R5 R6 B1 B2 B3 B4 B6 |
| M2 trim removed | R4 |
| M3 case-fold of NODE_ENV removed | R4 |
| M4 request-time refusal log removed | R3 |
| M5 flag honoured again in production (request branch `if (false)`) | R1 R2 R3 R4 R5 |
| M6 factory error log removed | R6 |
| M7 factory warn removed | B6 |
| M8 refusal logged but still bypasses in production | R1 R2 R4 R5 C1 |
| M9 flag test widened with trim (informative) | none (M-1) |
| M10 `audience` dropped from jwtVerify (informative) | none (M-1) |

- Constants: every asserted array is built from values read in that cell (status, body code, next count, payload, mock call counts, source text). No field is written into both expected and received.
- Other tests that pin the old behaviour: `git grep` for the flag and `jwtMiddleware|marketplaceJwt|validateMarketplaceToken` over the test tree finds only `rd385-shipped-root-markdown-identifiers.test.js:755, :844, :856`. These pin the two GUID lines by count and hash; the lines are unmoved, and the test stays green in the full verify. No test runs the middleware with the old answer.

## FULL VERIFY (head)
`npm --prefix v6 run verify -- --maxWorkers=2` at head (tree b94d4fda; `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES -u VERIFY_EXPECTED_FILE`) ran 20:31:54 to 20:53:58, rc=0:
`VERDICT: PASS - 6148/6148 tests passed across 387 suites (jest exit 0)`, equal to the committed pair 6148/387 (6128 + 20, 386 + 1).

- `EADDRINUSE` count in the log: 0.
- Porcelain before and after: empty.
- Band 25120-25759 listeners: 0 before and 0 after (control: all listeners 11).
- Load1 4.23 at start, 4.83 at end.
- One lock acquisition (20:31:48 to the release at 20:53:58).
- The builder's p-plain-K claim (PASS 6148/387) is TRUE.

## SCOPE AND MERGE
- `git ls-remote`: the branch is at 18c490c653fee13346d98779ba63222a77c83f00 and main at b0499db08dafc08313e855faf7c2ce4f7f9f0bcc (ahead 3, behind 0). The parents are linear: A445 1a3d6242 on b0499db, T445 da360be1, K 18c490c6, with no merge commit.
- Exactly three paths:
  - `__tests__/rd445-marketplace-jwt-skip-flag.test.js` +194 (A, blob 43b10b5b752b)
  - `backend/marketplaceJwt.js` +30 -4 (blob d2feb537adac to 8583d059c9b6)
  - `scripts/verify-expected-counts.json` +3 -3 (blob 424f786b1fba to 7bec5916f610)
- `backend/marketplace-api.js` and `backend/server.js`: diff 0 lines.
- Frozen program: kit lines 35-96 extracted by `awk` and run by me on main's file. It wrote 6602 bytes, blob 8583d059c9b6, and `cmp` against the head file gave rc 0 (byte-equal, so every unchanged line is byte-equal).
- `git merge-tree --write-tree main head` = b94d4fdac9a6892622832fa1ef233478206d51f6 = the head tree (clean). Open PRs: 0.

## CODEQL
`pr_codeql_check.sh --base b0499db0... --head 18c490c6... --lang javascript`, scratch clone as `--checkout`, CLI 2.27.4, 20:32:02-20:33:31, rc=0:
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```
- Hosted open alerts on main (read-only `gh api` GET, account check: login contains "datasec", count 1): 22 open, 0 in `backend/marketplaceJwt.js` or `backend/marketplace-api.js` (control: 21 rows name `backend/`). The builder's claim (22, 0 in the file) is TRUE.
- The local run holds one result in those files on both sides, `js/file-access-to-http` at `backend/marketplace-api.js:511`. It is not an open hosted alert, and the change KEEPS it (file untouched). Nothing is claimed closed or moved.
- CodeQL pre-scan of added lines: no `new RegExp(`, `eval`, `new Function`, `child_process`, `innerHTML`, timer or skip/only/each form. No sensitive-word identifier or title.

## TEXT
Program `progs/textscan.py` over the 227 added lines and 3 commit messages (Co-Authored-By lines excluded), each count with a control that fires:

| scan | result |
|---|---|
| names | 0 |
| B-number/seat | 0 |
| card/decision id | 0 |
| product-owner attribution (`product owner`, `ruled`, `approved by`) | 0 |
| non-ASCII | added 3, removed 3, net 0 (the moved log line); messages 0 |
| Cf characters | 0 |
| dotted quads | 0 |
| GUIDs | 0 |
| gitleaks over the diff | no leaks (control: a planted AKIA-shaped string reports 1) |

- Ticket key `RD-445` only.
- Signature claims: the only hits are "not a real signature check" (test :7) and "not a real signature check" (T445 message). Both are negations, and both are honest.
- No committed text says the signature check was tested.

## PROCESS (builder Corrections 1-8, judged by effect on the product)
1. Stale branch name in the copied `lib.sh`: fixed before use. `lib.sh:8` now names the right branch; origin holds only `b1739/nexusai-lane-nj-marketplace-jwt-bypass` (ls-remote of `b1739*`). No effect.
2. Gross-vs-net non-ASCII row: the net rule is right. I measured net 0 (3 and 3). No effect.
3. Sensitive-word row listing existing names (`marketplaceTokenPayload`, already at main): acceptable. My identifier and title scan finds no new sensitive name. No effect.
4. Frame count 470/388 vs 469/387: TRUE as corrected (M-3). No effect.
5. Frozen edit extracted, not retyped: TRUE (my own extraction gives the same blob).
6. Reflog `reset: moving to HEAD`: present at `wt` `HEAD@{3}` at b0499db, right after the worktree's creation entry. This is git's own `worktree add` behaviour; the branch reflog shows created, then three commits. No effect.
7. `node_modules` symlinked: TRUE. I did the same (symlink to the builder clone's `node_modules`, package-lock blob 2d7dbece equal at both). The risk is only to tooling, not the product.
8. Monitor stopped and band clear: not re-measurable now. My band reads 0 before and after.

## FOUND / TESTED / HOW
- FOUND: no production skip path. Residual (a) and (b) are stated honestly and are no worse than stated. The 4 Minors and 3 Infos are above.
- TESTED (by me):
  - refs, scope, frozen-program blob and merge-tree;
  - the 77-cell bypass matrix at head and main (fresh processes, real jose);
  - the real-library signature table with a positive control;
  - the flag, caller and env-write enumerations;
  - 20 cells twice, red-first at T445 on main's module, and 10 mutants;
  - the full verify (below);
  - local CodeQL and hosted alert reads;
  - the RD-445 ticket read whole by GET (To Do; item 2 quoted in the kit is exact; credentials read in-process, nothing printed);
  - text scans;
  - deploy-demo.yml at head (paths-ignore `**.md`, `docs/**`, `tests/**` at :29-32, so backend/** triggers a run; jobs gated on `vars.CI_DEPLOY_ENABLED` at :53 and :91; the last three main runs concluded skipped, newest jobs build=skipped, deploy=skipped).
- NOT TESTED:
  - Microsoft's real JWKS and tokens, and any request to Microsoft or a Marketplace endpoint;
  - a hosted instance and its app settings;
  - Partner Center;
  - Linux and Node 24;
  - the hosted Build and CodeQL on the PR merge ref;
  - whether `requireAuth` admits the webhook on an auth-enforced instance (I-3);
  - the Deploy demo run a landing starts (it must read skipped).
- HOW: everything ran in my own clone and trees under `fleet/state/s294/g1756/`. Jest and the verify ran under ONE acquisition of the NexusAI jest lock (base `session-tools/locks-laptop-1017`, the same as the builder's `lib.sh:13`; tag `b1756-gate`; acquired after 0 s with the queue empty). `NODE_OPTIONS` was unset, `--maxWorkers=2`, slot 8 (band 25120-25759). Slot 8 was chosen because a loose scan of 249 briefs of 18-19 Nov names EVERY slot 0-18 somewhere, so no unnamed slot exists. 8 is outside the commission's taken list and was empty by `lsof` before and after. No push, PR, Jira write, alert action, deploy or `cd`.
