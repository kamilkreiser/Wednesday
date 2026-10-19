VERDICT: GO WITH NOTE at head ddb8a5395268... (tier 1, round 1 of 2; landing tree ac490c9430c0 on develop 46e4343a5312; 0 blockers, 5 notes)

model: claude-opus-5-5 -- G1 (tier 1, unauthenticated m365 crash fix) -- P1-P4 no -- gauge 49%

## BLUF

- The fix works on the real process.
  - On develop, each of the author's three inputs kills m365: socket dropped, /health refused, exit code 1.
  - On the landing tree, each one gets a bounded 302 and /health answers 200.
- Fuzz: 4174 qs shapes against every parameter the route reads, and 9 it does not.
  - Landing tree: 0 process deaths, and 0 answers off the expected 302 shape.
  - Develop, same driver as positive control: 162 deaths.
- All 5 of the author's mutants match the author's table.
  - The `code` read has no cell in the PR. I pinned it with a test-only seam in my clone: 2 new cells, both red on the code-raw mutant.
- No `process.on` net was added.
- No other m365 route can throw outside a `try` because of the shape of a query, params or body value.
- N1: develop MOVED during the gate, so the predicted tree a46ecb67 is void. The live landing tree is ac490c94.
  - The develop delta is 26 `.md` files only.
  - The m365, shared, api-gateway and lockfile subtrees are byte-identical, so every measurement here carries over.
- Nothing blocks.

## Findings

No blockers.

N1. **Develop moved during the gate.**
- At the start, ls-remote gave develop 4a065fb75350, which matches the brief. Before this verdict it gave **46e4343a5312**: KS-1668, docs only, 5 commits.
- `git merge-tree --write-tree` on LIVE develop = **ac490c9430c0038c9dd85c1d64945fa61548c234**, rc 0. It is NOT the predicted a46ecb67, which is void.
- a46ecb67 → ac490c94 is 26 paths, all `*.md`.
  - Non-`.md` count: 0. Control: the `Blockchain/Dev/docs` subtree id differs, 01e81904 → 1af5e12b.
  - These subtree and blob ids are identical in both trees: `services/m365-integration` 07da7027a37d, `packages/shared` cc79305dc919, `services/api-gateway` 98fc4aba1fad, `package-lock.json` e53534de57d6, `package.json` 3d91ab763727.
  - So the suite, fuzz, type-check and mutants, all run on a46ecb67, apply to ac490c94 unchanged.
- The PR head is unchanged at ddb8a5395268, with 1 commit.
- Three-dot on live develop = the PR's 2 files, +124/-1.

N2. **A behaviour change the PR does not name: a non-string `error` beside a valid `code` and `state` now reaches the token exchange.**
- Before, it aborted to the error redirect.
- Measured with gate cell G4 (`code=plain&state=<real pending id>&error[x]=y`):
  - develop → 302 `message=[object Object]`;
  - landing → 302 with the MSAL "not configured" exchange error, so the exchange path ran.
- A string `error` (G5) still aborts on both trees (`message=e`).
- I judge this safe:
  - Whoever builds that URL could already get the same exchange by leaving `error` out.
  - Microsoft never sends `error` together with `code`.
- Recording it because the PR's "treated as absent" applies to `error` in this combination too.

N3. **The `code` residue is closable without a product change.**
- The author is right on every point:
  - Mutant M5 (`code` read raw) is 7/7 green in the PR's cells.
  - An object `code` is caught inside the `try`. On develop it flips the pending connection to `error` and reflects `Cannot convert object to primitive value`. I saw that in the server log line "token exchange failed" under the mutant.
- In my clone I built a seam with no product change:
  - The mocked `../db` `initDb` calls its `onReady`, which is `loadFromDb`. The mocked `query` returns one pending row for `SELECT * FROM svc_m365_connections`. `listen` is mocked to call its callback, so `startup()` runs.
  - G1 (object `code`) and G2 (array `code`) are red on M5, red on M1 (stringParam unfiltered) and red on develop. Both are green on the landing tree.
  - G3, a plain code that must reach the exchange and not `connection_not_found`, is green throughout. That shows the seam really reaches the line after the lookup.
- The author can adopt this if wanted. Not a blocker.
- File, clone only: `/private/tmp/wed_gate_ap1/wt/Blockchain/Dev/services/m365-integration/src/__tests__/gate-ap1-code-seam.test.ts`.

N4. **Residue on this route from earlier gates. Outside this PR, and not a query-shape issue.**
- :586 is inside the `catch`. It calls bare `encodeURIComponent(err?.message)`, and `dbSaveConnection` is awaited there too.
  - This is AN1 N5, still open. It needs a valid server-issued state plus a lone surrogate in MSAL error text.
  - `dbSaveConnection` swallows its own errors (read at :168-190), so the await cannot reject.
- :579, the success redirect, interpolates `connectionId` without encoding. It equals a key already in `memConnections` (server-issued `conn_<uuid>`), so a request cannot choose it.

N5. **Out of scope, authenticated, not investigated further.**
- `GET /api/onedrive/files` (:1090) template-interpolates the raw `folderId` into the Graph path.
  - It is inside a `try` that goes to `next`, so it cannot crash.
  - A non-string value or path text reaches graph.microsoft.com with the connection's token.
- The connection is looked up by `connectionId` alone (:1087). I did not check whether the caller's org is enforced somewhere.
- It belongs with a census ticket if Wednesday wants one.

## Questions

**Q1. The crash and the fix on the real process.**
- How each run worked:
  - Driver: `/private/tmp/wed_gate_ap1/tools/live.mjs`.
  - Each run is `tsx src/index.ts` under Node v24.7.0, spawned `detached` as its own process group, with NODE_ENV=development, FRONTEND_URL=http://frontend.test and PORT in the range 55470-55479.
  - Requests go over a raw socket, so the bytes are exact.
  - After each run the whole group gets SIGKILL and lsof checks the port.
  - Versions: express 4.22.3, qs 6.16.0. `express/lib/utils.js:289-292` reads `allowPrototypes: true, arrayLimit: 1000`.
- Results, one fresh process and port per input:

| input | develop (index.ts sha256 a504a66b…) | landing (a8f8a46e…) |
|---|---|---|
| `error[toString]=x` | no response, /health ECONNREFUSED, **exit 1**, 1 TypeError at index.ts:474:21 | 302 `missing_code_or_state`, /health 200, alive |
| `error=a&error_description[toString]=x` | no response, refused, **exit 1**, TypeError at :474:21 | 302 `a`, /health 200, alive |
| `code=x&state[toString]=y` | no response, refused, **exit 1**, TypeError at :521:24 | 302 `missing_code_or_state`, /health 200, alive |
| control `error=access_denied&error_description=plain` | 302 `plain`, alive | 302 `plain`, alive |

- Port free after all 8 runs.
- Fuzz: 4174 cases, generated by `/private/tmp/wed_gate_ap1/tools/gen.mjs`.
  - Parameters: the 4 the route reads (`code`, `state`, `error`, `error_description`), plus `connectionId`, `foo`, `hasOwnProperty`, `toString`, `valueOf`, `__proto__`, `constructor`, `prototype` and `length`.
  - 40 shapes each:
    - `[toString]`, `[valueOf]`, both together, `[__proto__]`, `[__proto__][toString]`, `[constructor]`, `[constructor][prototype][toString]`, `[prototype]`, `[hasOwnProperty]`, `[length]`, `[toJSON]`, `[toString][toString]`;
    - `[]` arrays, repeated keys, string mixed with object in both orders, `[0]`, `[999]`, `[1001]` (over arrayLimit), `[0][toString]`;
    - depth 10, `[toString]`×8, depth 500;
    - values of 8000 chars, 1000 emoji;
    - empty, bare key, encoded brackets, dot notation;
    - 300 repeats, 300 sub-keys.
  - Each shape in 9 contexts, the other parameters set before or after. Plus 18 top-level oddities, including `__proto__[error]`, 1200 parameters and 15000-char values. The longest query is 15026 bytes, under Node's 16 KB header limit, so 0 pre-handler 431/400 rejections.
  - After EVERY request the driver checked /health and child liveness.
  - Every answer was judged: 302, host `frontend.test`, path `/admin/integrations`, keys exactly `m365,message`, `m365=error`, empty hash.
  - The 9 extra parameters are names the route does not read. Their shapes reach the route only through Express's own query parsing.
- Landing: **0 deaths, 0 off-shape**, longest Location 2459, 0 TypeError lines in the server log.
  - Messages: `missing_code_or_state` 1830, `a` 1000, `connection_not_found` 885, `d` 442, 200 code points 9, 400 chars 7, NUL 1.
  - The 400 is AN1's 200-code-point cap on emoji, not a breach.
  - The NUL is `error=%00` reflected as `%00`. That predates this PR and the body-only NUL guard does not cover it. Harmless in a Location.
- Positive controls:
  - The same driver on develop: **162 deaths** (for example `code=x&state[toString]=x`, and `error=a&error[toString]=x`, which gives an array holding an object). Develop also reflected `[object Object]` 123 times and `a,b` 14 times.
  - Shape judge: 6 known inputs (success redirect, foreign host, extra key, other path, 500) were each classified correctly.
- What qs actually builds, checked directly:
  - `error[toString]=x` → `{toString:"x"}`, and String() throws.
  - `error[__proto__][toString]=x` → `{}`.
  - `__proto__[error]=x` → `{}`.
  - `error[1001]=a` → `{1001:"a"}`.
  - Depth is capped at 5.

**Q2. Completeness on /api/callback**, read on landing :525-588.
- The only `req.query` reads are the 4 at :526-529, all through `stringParam`.
- Before the `try`, the route does these:
  - `capCodePoints(oauthError)` and `error_description`, at :531-535;
  - `encodeReflectedText(capCodePoints(...))`;
  - `String(state)` at :543;
  - `capCodePoints(connectionId)` at :547.
- All of these now see `string | undefined`, and `undefined` is guarded at :533.
- `String(code)` at :553 is inside the `try`, as the author says. Confirmed by the seam (N3): under M5, an object code gives a 302 carrying the TypeError text and a logged "token exchange failed", and the process lives.
- Middleware before the route:
  - helmet, cors, express.json;
  - `rejectNulBytes` → `rejectControlBytes`, which walks `req.body` only (shared middleware :608-627);
  - requestLogger, which reads `req.path` only.
  - None of them reads `req.query`.

**Q3. m365 census.**
- `git grep -E "req(uest)?\.(query|params|body)"` over m365 `src` (tests excluded) gave 27 hits, all in index.ts.
- Positive control: the same grep on develop finds the old raw destructure at :507.
- Unauthenticated routes are the ones above `app.use('/api', jwtAuthenticate(...))` at :606: `/health`, `/api/health`, `/api` and `/api/callback`. Plus `POST /api/outlook/verify-hash`, which is in publicOps.
  - Gateway, `proxy.ts:936-939`: `router.use('/api/m365/callback', proxy(...))` with no `authenticateToken`, any method.
  - Gateway, `proxy.ts:945-947`: `router.post('/api/m365/outlook/verify-hash', proxy(...))` with no auth.
  - Everything else under `/api/m365`, `/api/onedrive` and `/api/teams` gets `authenticateToken(true)`.
- verify-hash (unauthenticated): `z.object({hash: z.string()}).parse(req.body)` runs inside the `try`, so a non-string is a ZodError and gives 400.
- Authenticated, async, NO `try`:
  - `GET` / `DELETE /api/connections/:id`, `POST /api/connections/:id/refresh` (before its try), `DELETE /api/sites/:id`.
  - They read `req.params.id` only. Express 4 params are always strings, and a bad `%` is a sync 400 from Express.
  - Their awaited helpers `dbGetConnection`, `dbSaveConnection` and `dbSaveSite` each catch internally (read at :168-212, :214-230).
  - Not throwable from request shape.
- Authenticated SYNC handlers with raw `req.query`: `GET /api/sites` (:891) and `GET /api/documents` (:1013).
  - They compare with `===` only. A sync throw would be caught by Express anyway.
- Authenticated async handlers WITH `try`/`next`:
  - `GET /api/onedrive/files` (:1084): `String(connectionId)` and the `folderId` template are inside the try (N5).
  - `POST /api/onedrive/files/:id/sync` (:1123): `String(connectionId)` is inside the try.
  - Every `schema.parse(req.body)` route, the teams routes and exchange-token.
- **No route outside /api/callback can throw outside a try because of the request's shape.**
- Not measured through the gateway.

**Q4. Cells can fail.**
- PR file, verbose reporter, run in wt2 (landing). Every run counted 7 tests.

| mutant | red |
|---|---|
| head | none, 7/7 |
| M1 `stringParam` returns the value unfiltered | Q1 Q2 Q3 Q4 Q5 |
| M2 `error` raw | Q1 Q4 |
| M3 `error_description` raw | Q2 Q5 |
| M4 `state` raw | Q3 |
| M5 `code` raw | none, 7/7 (the author's disclosed residue; see N3 for the gate seam) |
| gate G6 `error_description` always undefined | C1 |
| gate G7 `state` always undefined | C2 |
| gate G8 filter only drops non-array objects | Q4 |

- index.ts was restored by checkout after each mutant: sha a8f8a46e, 0 status lines.
- Red-first: develop's index.ts with the PR file gives 5 failed and 2 passed (C1 and C2 green), with 3 TypeErrors in the output. This matches the author.
- Q4 and Q5 behaviour change, read against the code and the protocol:
  - The route's authorize URL asks for `response_mode: 'query'` (:1066-1073). Microsoft's identity platform returns `code`, `state`, `session_state`, or `error`, `error_description` and `error_uri`, each as a single string value. This is from my knowledge of the documented protocol; I did not fetch the docs in this gate.
  - Arrays and bracket objects only come from a hand-built URL.
  - The change only affects what such a URL reflects: an error redirect still results, with `missing_code_or_state` or the string `error` in place of `a,b` or `[object Object]`.
  - Safe for a real provider. See N2 for the one combination that changes path.

**Q5. No process-wide net.**
- The landing m365 tree has 0 matches for `process.(on|once|addListener|prependListener)(`, `uncaughtException`, `unhandledRejection` or `setUncaughtExceptionCaptureCallback`.
- In the PR diff, 3 lines mention `process.on` or "unhandled", all in comments. 0 added lines contain `process.on(`.
- Positive control: the same regex finds handlers in the anchoring, api-gateway, auth, billing and demo-service index.ts.
- I did not re-read KS-1427.

**Q6. Landing.**
- Merge-tree on LIVE develop 46e4343a5 = ac490c94 (N1). The predicted a46ecb67 equals merge-tree on the brief's develop 4a065fb7 (measured), but that develop is gone.
- Three-dot = the PR's 2 files, +124/-1.
- Full m365 suite on the landing tree: **81/81 in 11 files, rc 0**.
  - develop index.ts without the PR file: 74/74 in 10, rc 0.
- Type-check including the test file:
  - Config: `/private/tmp/wed_gate_ap1/tools/tsconfig.gate.json`, extending the service tsconfig without its `src/__tests__` exclude.
  - Result: rc 0, 0 errors. `--listFilesOnly` counts the ks1671 file 1 time and 11 test files in all.
  - Planted error (`const gatePlanted: number = "not a number"` appended to the ks1671 file): rc 2, TS2322 at (102,7).
  - The service's own tsconfig gives rc 0 even with the planted error, because it excludes tests. That is why the gate config was needed.

## How (environment)

- Clone: `git clone --shared` of Wednesday's cache clone into `/private/tmp/wed_gate_ap1/repo`, using the cache clone's core.sshCommand.
- Fetched `refs/pull/1627/head` and develop.
- Local landing commit f77f5cbf (`commit-tree` of a46ecb67, never pushed), checked out as worktrees `wt` (live runs and seam) and `wt2` (suite, mutants, tsc).
- In each worktree: `npm ci --prefix <wt>/Blockchain/Dev -w services/m365-integration -w packages/shared --include-workspace-root --ignore-scripts`, then `packages/shared` built (rc 0).
- No cd, no rm, no Docker, no stderr discarded.
- Processes:
  - Every service run was killed by process group.
  - `pgrep -f wed_gate_ap1` → rc 1 (none) after each phase and at the end. Positive control: a decoy node process listening on 55470 was matched by pgrep (rc 0) and by lsof.
  - All of 55470-55479 are free at the end: lsof rc 1 on each.
  - One mid-gate pgrep hit was my own concurrent vitest in wt2, not a leaked service.

## NOT RUN

- No request through api-gateway, and no deployed image or built `dist`.
- No Docker, DB, Redis or MSAL. The exchange path was exercised only to the "MSAL not configured" error.
- I did not re-measure the author's "merge-tree == real --no-ff merge" claim, or the PR body byte-identity.
- The suite, tsc and fuzz were not re-run on ac490c94 itself. Its m365, shared, gateway and lockfile subtrees are identical to a46ecb67 (N1).
- Preflight legs, the four platform suites and other services' suites were not run.
- Linear (KS-1671, KS-1427) was not read, and the GitHub PR page was not read.
- I did not check how the onedrive connection lookup is authorised (N5).
- I did not check which Microsoft OAuth parameters are documented (Q4 relies on my own knowledge).
- WEDNESDAY `git status --short` at the end shows these paths that are not this verdict and not dashboard data: `?? 2_Project_Files/local-model/night/briefs/ks_1660_p1.md`, `?? 2_Project_Files/local-model/night/briefs/ks_1660_p1/`, `?? 2_Project_Files/local-model/night/briefs/ks_1660_p1b/`, `?? 2_Project_Files/local-model/night/briefs/ks_1660_p1c/` (the last appeared between two of my status reads). This seat did not write them.
- Dashboard data: 12 files under `0_Brain/dashboard/data/` modified by other processes.
sha256 bfb74893f1ad376d53d4e4d51e3c3d1e44c7d35f72832009405bcb33c03cf652
