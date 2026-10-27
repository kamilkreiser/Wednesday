# QA gate — tier 1, round 1 of 2 — Secuura/Blockchain #1725, #1732, #1733

- **Tier:** 1 (published API contract + pre-push gate code), round 1 of 2
- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), subagent of Wednesday; not the author of any of this work
- **Window:** 2026-10-26 22:09:46Z → 22:29:35Z (2026-10-27 09:09–09:29 AEDT)
- **Workspace:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-t1-1027/` (clone `repo/`, logs `out/`, TMPDIR `tmp/`)
- **Pushed / merged / commented / edited: nothing.** No git command was run against `!CODING/Secuura/Blockchain/2_Project_Files` or its worktrees. No docker, az, network beyond fetch/ls-remote/`gh pr view`.

## Pins

Start (`out/lsremote_start.txt`) = end (`out/lsremote_end.txt`) = the brief's pins. `diff` empty.

| ref | sha |
|---|---|
| develop | 1b550684fa6284c0b68eef0ffbd90ee62732d97a |
| #1725 head | df47c7983092820ca8efa076d2b4da4fe87a9cef |
| #1732 head | bfe5c3b311b7bc2b3baceb6c4946ef1019d288ce |
| #1733 head | e9871f3ce2356aa98cce5b237321adec96e70551 |

All three PRs are one commit on merge-base `ec3313a80440` (#1733 as well, not only #1725/#1732). develop has 5 commits since then; none touches the yaml, any `*.openapi.ts`, m365-integration, or `preflight.sh`/`preflight_deps.test.sh` (they touch `run-shell-suites.sh`, pre-push-hook suites, typecheck baselines, security vitest config).

## BLUF

| PR | verdict | worst finding |
|---|---|---|
| #1725 KS-1700 | **GO WITH NOTES** | LOW: the "no CHECK constraint" licence cites one DDL (`migrations/002:432`); the table is created by **five** DDLs. I checked all five: none has a CHECK, so the conclusion holds. Nothing pins the new enum to the service's type (author's own NOT-COVERED, honest). |
| #1732 KS-1531 | **GO WITH NOTES** | LOW: the U2 cell's stated rationale ("declaring bearerAuth would silently move authentication to the edge") is false. I mutated the yaml to `bearerAuth` and the 28-cell behaviour matrix did not change, because GET is answered by the health router (index.ts:837) before the edge gate (index.ts:1054) runs. Auth is unchanged. The only behaviour change is non-GET 404 → 405, as claimed. |
| #1733 KS-1643 | **GO WITH NOTES** | LOW: the nit-2 hardening (the comment filter) has no cell. A mutant that removes it stays 68/0. The author says it changes no behaviour today, which is true (census: one `:-` read, live code, pre-push:77). |

No MAJOR in any PR.

## MERGE ORDER

**Any order is safe. Every order gives the same single tree.**

- `git merge-tree --write-tree` (git 2.54.0), develop + each PR: rc 0 for all three, no conflicts.
- Each pair, both orders (pr1725×pr1732, pr1725×pr1733, pr1732×pr1733): rc 0. Each pair gives the same tree in both orders: 7330512…, 3a02893…, 818fde1….
- All **six** sequential orders from develop (built by chaining `merge-tree` + `commit-tree`): all rc 0, and all six give the **same tree `eb3704e52d7269339ac35923d7e0e5db3731f90e`** (`out/seq.txt`).
- #1725 and #1732 both edit `secuura-api.yaml`, but the hunks are ~11k lines apart (components 4835 vs components 1744 + paths 15929). That is why they merge cleanly.
- The generated yaml stays consistent after merging. `check:openapi` passes (rc 0) on the combined tree: the regenerated spec matches the on-disk yaml. So a merge cannot leave a stale yaml, in whichever order.

## #1725 — KS-1700 (M365Connection.status enum)

**FOUND**
- The diff matches the claim: 2 files. The yaml change is +2/−2 = four lines in one schema (`M365Connection.status`: `expired`, `revoked` → `error`, `disconnected`). `m365-integration.openapi.ts` is +3/−1 (enum plus a two-line comment). Nothing else changed.
- My census, at base `ec3313a`:
  - The quoted string `'expired'` appears in m365-integration exactly **once**, on the enum line. The bare word "expired" appears 8 times; the other 7 are prose or comments (SETUP.md, token-manager comments, test names).
  - `'revoked'` appears 6 times. Five are Teams webhook event vocabulary (`index.ts:1264`, `:1448`, two tests, openapi `:248` description); the sixth is the enum line.
  - Positive control: quoted `'connected'` appears 28 times, so the search does find quoted literals.
  - Every assignment to `status` (`index.ts:656` connected, `:679` error, `:730` pending, `:812` disconnected, `:864` error) is inside the new enum. The stored type at `index.ts:94` is `'pending'|'connected'|'error'|'disconnected'`.
  - History: `git log -G"status.*'(expired|revoked)'"` on m365 src finds only the commit that introduced the enum line (2b0c33f07). No version ever assigned `expired` or `revoked`.
- The author's "7 not 5" holds. Base yaml: `- expired` appears as an enum entry **7** times. Head: 6. `- revoked`: 6 → 5.
- Writers of the column: every repo-wide reference to `svc_m365_connections` was enumerated. The **only** INSERT/UPDATE is `index.ts:175` (`INSERT … ON CONFLICT DO UPDATE SET status = EXCLUDED.status`). No other `INSERT`/`UPDATE`/`ALTER` exists. The claim holds.
- **The table is created by five DDLs, not one:**
  - `migrations/002:432`, `deployment/azure/migrate/init.sql:1179`, `docker/init/04-…:260`: `status TEXT NOT NULL DEFAULT 'pending'`.
  - `docker/init/06-m365-tables.sql:9`: `VARCHAR(50) DEFAULT 'pending'`.
  - `api-gateway/src/startup-migrations.ts:376`: `status TEXT DEFAULT 'active'`, with a different column set.
  - None has a CHECK, so the licence holds. The `'active'` default is outside the new enum. It cannot be reached through the only writer, which always supplies `c.status`, and that DDL lacks `tenant_name`, so the writer's INSERT would fail against it anyway. The load path (`index.ts:285`) casts `r.status` without checking it.
- `M365Connection` is used only as a 200 response schema (GET `/api/m365/connections/{id}`, POST `…/refresh`). No request validation is narrowed.

**TESTED-HOW**
- Deps: absent before (fresh clone). `npm ci --ignore-scripts` rc 0 (1806 pkgs). `check:openapi` builds `packages/shared` itself.
- m365-integration at develop+1725 (`m1725` bd6e151): **26/26 files, 261/261**. Same at all-three (`mall` d8cbf5f).
- api-gateway at develop+1725: **122/122 files, 1196/1196**. Matches the claim.
- `check:openapi` at develop+1725: rc **0**. **Independent control (the repo's own checker):** develop plus only the #1725 `.ts`, with the yaml left stale, gives rc **1** (`CHECK FAIL: generated YAML differs`). This reproduces the author's rc=1 → rc=0, and shows the checker would catch an unregenerated yaml.

**NOT TESTED:** no live probe of a stored row's status on any deployment. Whether a deployed DB holds an out-of-enum value (for example `'active'` from the startup-migrations DDL) is unknown.

**SEVERITIES**
- LOW: the "no CHECK" claim cites one DDL of five. The conclusion still holds, as checked above.
- LOW: no test pins `M365ConnectionSchema.status` to the `index.ts:94` type, so the two can drift again silently (author's own NOT-COVERED). Ticket it.
- INFO: `startup-migrations.ts:376` creates `svc_m365_connections` with `DEFAULT 'active'` and a divergent column set. This existed before the PR; it belongs on a schema-hygiene ticket and is not this PR's scope.

## #1732 — KS-1531 (GET /api/connector/info in the contract)

**FOUND**
- The diff matches the claim: 3 files, all additions. Yaml +73/−0 in **two hunks** (`ConnectorInfo` schema at components:1744; the path at paths:15929). `api-gateway.openapi.ts` +77. New test +153. Paths go **311 → 312** (base, develop, head, develop+1732, all-three counted). The same yaml diff on develop+1732 is still +73/−0 with 0 removed lines.
- Security: `security: [{connectorApiKey: []}]`. `connectorApiKey` already exists in `components.securitySchemes` (apiKey, header `x-api-key`) and is now used twice.
- The new path matches no other spec path: no `/api/connector/{…}` sibling, and specRouteMap's regex is `^/api/connector/info/?$`.
- "Three 403s and two 503s" refers to handler code paths (`health.ts`: not-connector, container-malformed, allow-list-not-a-list; Redis-unavailable, read-threw). The yaml carries one 403 and one 503 response object, whose descriptions enumerate those paths. That is accurate.
- **Mount order (index.ts):** `rejectConnectorBearer` :584 → `createHealthRoutes` **:837** → spec edge gate **:1054** → proxies :1107. GET/HEAD are answered by the health router before the edge gate. Only methods the router does not match (POST/PUT/PATCH/DELETE) reach the edge gate, which now 405s them.

**TESTED-HOW**
- api-gateway at develop+1732 (`m1732` dadef67): **123/123 files, 1203/1203**. All-three: the same.
- **Author's red reproduced on the merged tree.** Reverting only the yaml and `api-gateway.openapi.ts` to develop (test file kept) gives **3 failed / 4 passed**: U1, U2, and R1 `expected 404 to be 405`. Restored with `git checkout --`; sha256 of both files equal to head (`out/sha_head_1732.txt`). Green after restore: 7/7.
- **Independent: a behaviour matrix I built** (`out/zzgate-connector-info-matrix.test.ts.txt`, now quarantined at `_quarantine_2026-10-27/`). It boots the real app with the author's harness plus `ENABLE_TEST_TOKENS`, and covers 7 methods × 4 credentials (anon, user test-bearer, admin test-bearer, a junk non-`sk_` key) = 28 cells. Run at develop and at develop+1732, then diffed (`out/matrix_*.txt`):
  - GET, HEAD, OPTIONS: **all 12 cells identical.** GET: anon 401 `Authentication required`, user 403, admin 403, junk key 401. HEAD: 401/403/403/401. OPTIONS: 204 (cors).
  - POST, PUT, PATCH, DELETE: **all 16 cells** change from 404 `NOT_FOUND` to 405 `METHOD_NOT_ALLOWED`, `Allow: GET`, for every credential state.
  - So the 405 is the only behaviour change, and authentication is unchanged.
- **One 403 body driven:** a user or admin bearer gives 403 `FORBIDDEN` "This endpoint is only available for API-key authenticated connectors". The other two 403s and both 503s need a validated `sk_` key (DB-backed `validateApiKey`) and were not driven.
- **Mutation, gate-built:** I changed the route's yaml security to `bearerAuth`. U2 goes red, but R2 still passes, and the whole 28-cell matrix is **byte-identical** to head. Declaring `bearerAuth` would not move authentication to the edge for GET, because the edge gate never sees GET on this path.
- `check:openapi` at develop+1732: rc 0. Stale-yaml control: rc 1.

**NOT TESTED:** the connector-key 200 path, the 403s for a malformed allow-list or non-list allow-list, the 503s. Legs 3/4/8 were not run. From the code I predict: leg 3 (`spec-auth-conformance.mjs`) treats a `connectorApiKey`-only op as authed and expects 401/403 for anon, and the matrix shows 401, so a predicted pass. Leg 4: GET routes (401, not 404), predicted pass. These are predictions, not measurements.

**SEVERITIES**
- LOW: the U2 comment and assertion message, and the PR's framing that declaring `connectorApiKey` "keeps the edge auth gate off", are not load-bearing for GET. The gate is bypassed by mount order whichever scheme is declared. U2 pins the yaml text, not a behaviour. Fix the wording, or add a note that the router at :837 precedes the gate.
- LOW: wording. The 401 description says "A JWT bearer is not accepted here and is answered 401". In the code that is only a *connector* JWT (`rejectConnectorBearer`, auth.ts:268-280). A user or admin JWT gets 403, as the route description itself says. The two descriptions read as contradictory to an integrator.
- LOW: the source comment says `allowedDocumentTypes` "is guaranteed by the handler". The handler checks `Array.isArray` but never checks that the items are strings, so `[1, {}]` stored would be echoed against a declared `string[]`. This sits beside the author's honest `name`/`workflowPolicy` note.
- INFO: R2's "from authenticateToken and not from the edge" cannot be distinguished by its assertions: the edge 401 body is identical and also has no Allow header. The conclusion is still true because of mount order.

## #1733 — KS-1643 (preflight leg 14)

**FOUND**
- The diff matches the claim: 2 files, +91/−12 (`preflight_deps.test.sh` +64/−6, `preflight.sh` +27/−6). Nothing else changed.
- Minor 1: the run, the timer and the `fail=1` now sit inside the `else` of the hook-control guard. The refusal branch still sets `fail=1`.
- Minor 2: the stub prints `STUB-SAW-ALLOW_FORCE=…`, and a `nostrip` fixture mutant (M3) is applied to the fixture copy only.
- Nit 1: the vacuous `SOMETHING_ELSE` check is replaced in place by an exact-line assertion.
- Seven new `expect` cells: 61 + 7 = 68.
- Nit 2 / nit 3 census (mine, at base, develop and all-three): `.githooks/pre-push` has exactly one `${NAME:-` read, `ALLOW_FORCE` at :77, in live code. Non-comment braced alternative ALL-CAPS reads (`${X}`, `${X:?}`, `${X:+}`): **zero**. Bare ALL-CAPS: only `$ZERO`, which the hook assigns itself. Both "measured" comments are true.

**TESTED-HOW** (develop+1733 = `m1733` d9b6d9c, real tree, in place)
- `preflight_deps.test.sh`: **68 passed / 0 failed**. I did not see the author's 3 shared reds: they belong to the copied tree, as the author said.
- **Two-arm red-proof, differing only in `preflight.sh`** (same tree, the new test file kept; develop's `preflight.sh` swapped in): **67 / 1**. The only failure is `KS-1643 Minor 1: the refusal WITHHOLDS the run`. This matches the author's one-cell delta (64/4 vs 65/3). Restored, sha256 equal to head (`out/sha_head_1733.txt`).
- **Gate-built mutant G1** (not the author's M3): leg 14 runs with plain `env` and strips nothing, slot or hook. Result: **67 / 1**, killed by `Minor 2: the suite does NOT see ALLOW_FORCE`. The new oracle discriminates on a mutant the author did not write.
- **Gate-built mutant G2:** remove the nit-2 comment filter. Result: **68 / 0, survives.**
- Full runner `run-shell-suites.sh` on all-three (`mall`): rc 0, **95 passed / 0 failed / 1 skipped of 96** (skip `ks949_main_seed_idempotence`, no PostgreSQL, a skip ruled 2026-09-13). 590 s.

**NOT TESTED:** a real `ALLOW_FORCE=1 git push` through the hook (no push by rule). Legs 3/4/8 were not run.

**SEVERITIES**
- LOW: the nit-2 comment filter is unpinned (G2 survives). It is honest that no behaviour changes today, but a later edit could drop it silently. A cell with a fixture hook that holds `# ${FAKE:-x}` would pin it. Ticket it.
- INFO: under G1 only the new Minor-2 cell went red. No cell observes the *slot* de-slotting from the stripped side. This existed before the PR; ticket it with the same oracle shape.
- INFO: nit 3 (only the `:-` read shape is derived) is recorded and not closed. My census agrees nothing is missed today.

## Authors' NOT-COVERED lists

| item | honest? | when |
|---|---|---|
| U: legs 3/4/8 skipped; leg 3 would check KS-1531's auth | Honest. From the code, leg 3 covers `connectorApiKey`-only ops and the in-process anon GET is 401, so a predicted pass. | after merge, ticketed (run at the next box preflight) |
| U: no live probe | Honest | after |
| U: no Schemathesis | Honest | after |
| U: no cell drives KS-1531's 403/503 bodies | Honest. Now partly closed by the gate: one 403 (not-a-connector) driven. Two 403s and two 503s remain, and they need a stubbed `validateApiKey`. | after, ticketed (MINOR: these are the contract's documented refusals) |
| U: no test pins KS-1700's enum | Honest | after, ticketed |
| U: `name`/`workflowPolicy` not validated | Honest, but **incomplete**: `allowedDocumentTypes` items are not validated either, and the source comment claims they are | after, ticketed with the comment fix |
| U: `mergeStateStatus` UNSTABLE on both | Out of date. `gh pr view` at 22:10Z returns `UNKNOWN` for #1725 and #1732, and `UNSTABLE` for #1733. `statusCheckRollup` was not read (403 for this token, as briefed). | Kam/Wednesday to read the checks before merge |
| S: 3 reds shared by both arms (copied tree) | Honest. In place the suite is 68/0, so the reds belong to the copy. | none |
| S: nit 3 recorded, not closed | Honest (census agrees) | after, its own ticket as stated |
| S: legs 3/4/8 not run | Honest | after |
| S: no Node/Playwright/Schemathesis/Akto/k6 | Honest. The change is shell-only, so these are irrelevant to it. | none |

Nothing on either list must be closed before merge.

## Instrument errors (mine)

1. The first `check:openapi` run failed with EINVAL from tsx's IPC socket: the absolute TMPDIR path is longer than macOS's ~104-byte `sun_path`. I re-ran with relative `TMPDIR=../../../tmp`, which resolves to the same workspace `tmp/` from `Blockchain/Dev`. Vitest runs used the absolute TMPDIR.
2. `run-shell-suites.sh` itself moved TMPDIR to `/tmp/rss.JaKye7` (its KS-1135 rule for a TMPDIR longer than 80 chars). That directory was removed by the runner; checked afterwards. The other `/tmp/rss.*` directories already existed and are not mine.
3. The first fetch failed because the shared clone had no SSH key configured. I set repo-local `core.sshCommand` in **my clone only**, copied from Wednesday's mirror; it was used for fetch only.
4. The first bearerAuth-mutation matrix run failed because I had not set `GATE_OUT` (the test had no output file to write). Re-run with it set; that run is the one reported.
5. Two hooks refused my commands (a literal `cd`, and `$VAR` word-splitting); I re-issued them. A third hook refused `rm` of my gate test file; it is quarantined at `work/gate-t1-1027/_quarantine_2026-10-27/` instead.
6. The api-gateway `test` script is `vitest` (watch mode by default), so I passed `-- run`. The first full m1732 run used bare `vitest`, which completed in non-TTY mode.

## Stray files outside the workspace

None. My clone is clean at the end (`git status --porcelain` empty). The WEDNESDAY repo shows only this verdict file and items that were already untracked before the session.
