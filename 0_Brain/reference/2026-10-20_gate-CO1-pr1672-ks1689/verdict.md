VERDICT: GO WITH NOTE at head e9e88339eecefab2df395c1cc803be4616fb422d (tier 2, round 1 of 2; landing tree 610d1d80e161ebde9dd81b04b4fca23741325a19 on develop 21e0c39149ca22e623835e07691c032dd6550f91; 0 blockers, 3 notes)

## BLUF
PR #1672 is correct and does what Kam's option (d) asked. The product change is two lines in `GET /api/connections/:id` only; `needsReauth` is a boolean derived from `status === 'connected' && !refreshToken`, so no token or part of one reaches the response. I reproduced every number in the claim: red-first 7 failed / 2 passed, then 9/9; the author's three mutants MA 4/4, MB 2/2, MC 7/7; suite 252 -> 261 and 25 -> 26 files with 0 vanished; `tsc` rc 0 on the shipped build and on the landing tree. The author's own survivor MD (`=== undefined`) really survives 9/9, and so does my `typeof !== 'string'` variant, so the `''` shape is genuinely unpinned. That is a test gap, not a defect in the shipped line, and it is less reachable than the claim suggests (N1). Safe to merge on a GO naming this head; re-read develop in the same action, it moved while I worked.

## Heads and landing
- ls-remote at start and at end, identical: `refs/pull/1672/head` = `e9e88339eecefab2df395c1cc803be4616fb422d`, develop = `21e0c39149ca22e623835e07691c032dd6550f91`.
- merge-base `f418cddac51498adda34cfed0bf5486a2d8cca77`. `git merge-tree --write-tree dev pr1672` = `610d1d80e161ebde9dd81b04b4fca23741325a19` (matches Wednesday's figure; the claim's `367043585a77` was on the older `88933d5c7ebb`, superseded). No conflict output.
- Three-dot against live develop: exactly 2 files, +150/-0 (the test file +148, `index.ts` +2). `src/auth/token-manager.ts` is not in the diff.

## Findings
No blockers.

**N1 (note) The `''` shape is unpinned, and it is narrower than the claim says.** Mutants MD (`refreshToken === undefined`) and MG (`typeof refreshToken !== 'string'`) both survive 9/9, so nothing pins the `''` case. The reachability needs one correction to the claim. `GET` reads through `dbGetConnection` (`index.ts:194`), which queries the DB FIRST and falls to `memConnections` only if the DB is unavailable, throws, or returns no row. The fail-closed exchange assigns `''` at `index.ts:654`, but `dbSaveConnection` runs it through `encryptToken` (`tokenCrypto.ts`: `plaintext == null || plaintext === ''` returns null), so the column stores NULL and the next read gives `undefined` via `decryptToken` (`stored == null || stored === ''`). So with a working DB, `''` collapses to the `undefined` shape the cells DO pin. The raw `''` reaches the GET only on the in-memory fallback. The shipped `!connection.refreshToken` is right for all of them. A future rewrite to `=== undefined` would still be caught on the DB path by R2/R3 and be silently wrong only on the memory fallback, so the residue is real but small. Suggest the Known residue say "unpinned, and only reachable when the DB is unavailable".

**N2 (note) leg-16 typecheck gap confirmed.** Only `api-gateway`, `auth` and `vc-issuer` have a `tsconfig.test.json`; `originate` and `m365-integration` have only `tsconfig.json`, which excludes `src/__tests__`. The shipped program lists the new test file 0 times; my purpose-built program lists it once. The claim's "two services, KS 1090" is accurate.

**N3 (note) "No OpenAPI change" holds, but for a weaker reason than "in sync".** `M365ConnectionSchema` (`m365-integration.openapi.ts:105-117`) is `.passthrough()`, so an extra field cannot drift the generated spec. It also does not describe the real response at all (status enum `pending|connected|expired|revoked` against the code's `pending|connected|error|disconnected`; no `data` envelope; no `tokenExpired`). That mismatch is pre-existing and is not this PR's. The new field is therefore undocumented for API consumers; the claim's KS 1700 follow-up is the right home.

### Q1 the diff and the value shapes
The diff is `needsReauth: connection.status === 'connected' && !connection.refreshToken` inside the `res.json({ data })` of `app.get('/api/connections/:id')`, plus a comment. Grep of `needsReauth` over the service: exactly one product site (`index.ts:796`). The POST init response, the health count (`index.ts:482`, a status filter), and every write path are untouched.

Every way `connection.refreshToken` takes a value:
- `undefined`: row NULL or `''` (`decryptToken` first line); an undecryptable `v<N>:` envelope (`catch`, fail-closed); `encryptToken` failure stores NULL (keyring uninitialised); `DELETE` sets `undefined` (`index.ts:814`, status also `disconnected`); a new `pending` connection has none.
- `''`: `exchangeAuthCode` `|| ''` (`token-manager.ts:97`) assigned at `index.ts:654`; reaches GET only on the memory fallback (N1).
- `null`: not produced by the code (type is `string | undefined`; NULL becomes `undefined`).
- non-empty string: a decrypted token, or a legacy plaintext row returned as-is by `decryptToken` (truthy, so not flagged, correct).
`!x` is right for `undefined`, `null` and `''`, and false only for a real token. `token-manager.ts:383` (`refreshAccessToken`) returns `''` too, but `POST /refresh` only overwrites when truthy (`index.ts:846`), so it cannot create the shape.

### Q2 no secret in the response
The field is a boolean expression (`&&` of a boolean and a negation). Nothing else in the `data` literal changed, and no `refreshToken` field is added. C1 pins `status` and `tokenExpired` for both token and no-token connections (200, `connected`, `false`). Mutant MF (swap to `accessToken`) was also caught, so a different token cannot satisfy the cells.

### Q5 scope
Only the 2 claimed files change; `token-manager.ts` untouched (empty in the diff stat). The claim's residue statements (MD survives; leg 16 names no `m365` and neither service has `tsconfig.test.json`) match what I measured, subject to N1's reachability refinement. I could not read the PR body (see NOT RUN), so I checked the claim mail's residue text, not the body.

## FOUND / TESTED / HOW

FOUND: the claim reproduces in full; 0 blockers; N1-N3 above.

TESTED, all in my own clone `.../scratchpad/gate_co1/src`:
- **Red-first.** On develop `21e0c3914` with ONLY the new test file added (product `needsReauth` count 0): 7 failed / 2 passed of 9. The two greens are C0 and C1. The seven failures are assertions (`expected undefined to be false/true`, `['error', undefined]` vs `['error', false]`), not import errors. With the product hunk as well: 9/9.
- **Mutants**, each applied as an anchor-unique single-line replacement (anchor count asserted 1), `tsc --noEmit` rc 0 before it counted, restore asserted by sha256 (`575fa27b...3004` before and after). Control (unmutated shipped line through the same script): 0 failed / 9 passed.
  - MA drop status clause `!connection.refreshToken`: 4 failed (R4, R5, R6, R7) / 5 passed.
  - MB drop token clause `status === 'connected'`: 2 failed (R1, R7) / 7 passed.
  - MC invert: 7 failed / 2 passed.
  - MD `=== undefined`: 0 failed / 9 passed. SURVIVES.
  - ME (mine) `status !== 'disconnected' && !refreshToken`: 2 failed (R5, R6) / 7. Killed.
  - MF (mine) `!connection.accessToken`: 2 failed (R2, R3) / 7. Killed.
  - MG (mine) `typeof refreshToken !== 'string'`: 0 failed / 9. SURVIVES (same hole as MD, confirms the `''` shape is the only unpinned one among the live states).
- **Counts.** Per-test JSON reports on develop: 252 tests / 25 files; on the PR head: 261 / 26, 0 failed. By name: 0 vanished, 9 new, all 9 in the new test file, no duplicate names in either run. On the landing tree (commit built from `610d1d80e` with develop as parent): 261 passed / 26 files, `tsc --noEmit` rc 0.
- **Type-check.** Shipped build `tsc --noEmit -p tsconfig.json` rc 0 (PR head and landing tree). The shipped program lists the test file 0 times (`--listFilesOnly | grep -c ks1689` = 0); a purpose-built child `tsconfig.gate.json` (extends the service config, includes `src/**/*` with tests) lists it 1 time and `tsc` rc 0. Positive control: appending `const gateCtl: number = 'x'` to the test file made the child program fail with TS2322 at line 149; the file was restored (sha256 `04a46b6c...b7cd` both before and after).
- **OpenAPI.** Read `m365-integration.openapi.ts` (N3); did not run the drift leg.
- **Overlap/scope.** Three-dot diff stat is the 2 files; no `src/auth` path in it.

HOW: `git clone --shared` of the Spark cache into `.../gate_co1/src`, repointed origin and fetched `refs/pull/1672/head` and develop there (the deploy-key `core.sshCommand` copied from the cache). `packages/shared`: `npm ci` failed on a native build script (node-gyp), so I ran `npm ci --ignore-scripts --prefix packages/shared` then `npm run build --prefix packages/shared` (ok). `m365-integration`: `npm ci --prefix` the service; `@secuura/shared` is not installed there (it is a root workspace), so I symlinked `node_modules/@secuura/shared` to the clone's `packages/shared`; `@electric-sql/pglite` is undeclared in m365's package.json and two existing test files import it, so I installed it with `--prefix` into a separate scratch dir and symlinked it in. Without these two links 16 and then 2 of the 26 files fail to import (an environment fact, identical for base and head). Vitest ran as `npm test --prefix <service>` (JSON reporter, output in the gate scratch folder) and, for mutants, `npx vitest run` with an explicit cwd inside the clone. No `cd`. Wall-clock: about 6 minutes of work from first command to this file (epoch 1792469627 to 1792469960 at the last check, plus writing).

## NOT RUN
- The PR body: `gh` is not authenticated in this shell (no GH_TOKEN, project config empty), so I did not read the Known residue text as posted on GitHub, only the claim mail.
- The preflight gate legs (OpenAPI drift "OK - spec is in sync", leg 16), lint (the service has no lint script; I did not run `eslint src`), the four platform suites, Docker, any container, `az`, any deploy.
- The OAuth callback / fail-closed exchange path: no cell was run that makes `''` reach GET, so the `''` behaviour is argued from source, not observed.
- Nothing observed on a running box. KS-1689 is not Done by this PR; the flag has never been read from a deployed service by anyone in this gate.
- Wednesday's tree: `git status --short` shows no untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/, 2_Project_Files/fleet/briefs_staged/. One staged modification, `0_Brain/dashboard/data/chat_tuesday.json`, is inside 0_Brain and not from this gate (I did not run anything against it). The only file I added is this verdict.
- Left in my scratch folder (not Wednesday's tree): JSON reports, `mut.py`, the clone on the landing commit (I ran `git stash -u` there before checking out the landing commit, so my untracked `tsconfig.gate.json` sits in that stash).

sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: 27af4bfb595b9d96a38fbb9230973f444c412d89412c525984401925f8a5ee5d
