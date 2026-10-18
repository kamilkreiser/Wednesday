#1586 KS-1627 head b12f56e303ac36a3e7adecfa4aab9fdeda3c384a: GO WITH NOTE (the suite catches the failure H1 named: renaming the real module's isRedisAvailable, with every compiler-forced caller updated and the route's optional member missed, turns R1+R2 red while product tsc stays rc 0; notes are INFO-level test-hygiene only)
sha256/16: e32e02e935734a16

Gate K1, round 1 of 2. Opus QA gate, findings only. Live develop 840ac4182d750d38ace9bea578e7fc6af100fd7b and head b12f56e303ac36a3e7adecfa4aab9fdeda3c384a: both re-read with `git ls-remote` at start and again at end, unchanged. All work ran in a `--shared` clone at scratchpad/k1/repo (origin set to git@github.com:Secuura/Distributed_Secuura.git, fetched with the Blockchain checkout's `core.sshCommand`). Ran `npm ci` (rc 0) and `npm run build -w packages/shared` (rc 0) in Blockchain/Dev before any suite. No write verb in !CODING, no push, no GitHub/Linear writes, no Docker.

## FOUND

| # | Severity | File:line | Finding |
|---|---|---|---|
| F1 | INFO | src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts:55 vs :64 | **Order coupling inside the file.** C2 asserts that the fallback store read resolves to null. R2 writes `platform-settings` into the same module-level `notificationSettingsStore` (services/redis.ts:671) and never clears it. With `--sequence.shuffle`, 3 of 12 seeds (3, 8, 12) ran R2 before C2, and C2 then failed: `expected { integrations: [...] } to be null`. Declaration order is the default and no config in the repo shuffles, so this is not a failure today. It is a latent flake if shuffle is ever turned on. A fix would be an `afterEach`/`beforeEach` that clears the store, or C2 reading a different key. R1 and the RED verdicts stayed correct in every order: all 12 seeds kept R1/R2 green. |
| F2 | INFO | same file :19, :34; interacts with src/__tests__/ks1233-in-redis-mode-platform-settings-expires.test.ts | **Cross-file coupling only under `--no-isolate`.** The file relies on the real module never having been initialised in its process. It does not assert that precondition on its own: C1 checks it, but the RED cells do not depend on C1 passing. With `--no-isolate --no-file-parallelism`: ks1627 first, then ks1233 fails 3/3; ks1233 first, then ks1627 fails 4/4 (C1 sees `true`; R1/R2 get 200 `[]`). The same 6 neighbours without ks1627 pass 29/29 under `--no-isolate`. Nothing in .github or Blockchain/Dev disables isolation (grep for `no-isolate`, `isolate: false`, `singleThread`, `poolOptions`: 0 hits), so CI uses vitest's per-file isolation. Default-mode runs are clean (see TESTED 5). |
| F3 | INFO | same file :39-41 | If the dynamic `import('../services/health')` in `beforeAll` fails, `afterAll` throws a second error (`Cannot read properties of undefined (reading 'close')`), because `server` was never assigned. The run still fails loudly (rc 1). This is only noise in the failure output. |

No finding at LOW or above. The PR does exactly what it claims, and the claim H1 asked for is now pinned.

## TESTED / HOW

1. **Diff at head.** The merge-base equals develop's tip 840ac418. There is one commit (b12f56e30), and `diff --raw` shows exactly one `A` entry: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts`, +68/-0. Nothing else changed: product is untouched, and health.ts/redis.ts/verification.ts blobs at the head equal develop's. The blob is **0886e4639a9af56dda0140fd06a9af2077e0ad29**, equal to the claim. The PR diff is **byte-identical** (`cmp`; sha256 1c57a9e0…eb3b9 for both) to 2_Project_Files/local-model/night/briefs/ks_1627_p1/golden.diff. R's disclosed tamper is absent from the committed tree: health.ts at the head is blob 48aaf4dd…, equal to develop.
2. **Red-first / green.**
   - Untampered: **4/4 passed**, rc 0.
   - Author's tamper (health.ts:53 `isRedisAvailable?.()` changed to `isRedisReachable?.()`): **2 failed | 2 passed**. R1 and R2 are the failures, C1 and C2 pass. R1 received `[200, undefined, undefined, []]`.
   - Restored by an EXIT trap with absolute paths. Post-restore blobs: health.ts 48aaf4dd, redis.ts fbb74be7 and verification.ts e5550504, all EQUAL to develop's. The test file is still 0886e463, and `git status --porcelain` is empty.
3. **The silent case (why this PR exists).**
   - **3a.** `isRedisAvailable` renamed to `isRedisUp` IN services/redis.ts (41 lines: the definition plus 40 internal uses), and routes/verification.ts:1276 updated (the only compiler-forced product caller). health.ts:23/:53 was left alone, and so was the test file. Product `tsc --noEmit -p tsconfig.json` gives **rc 0, 0 errors**: the compiler does not see the inert guard. Suite: **3 failed | 1 passed** (C1, R1, R2 red; C2 green).
   - **3b.** As 3a, plus the PR's own C1 moved to the new name (the edit a renamer would make, since the test-config tsc flags :50/:51). health.ts was still missed. Product tsc rc 0. Suite: **2 failed | 2 passed**, with **R1 and R2 red** (200 `[]`) and C1/C2 green. **This is exactly H1's F1 failure, and the suite catches it through the RED cells, not only through C1.**
   - **3c (opposite control).** The rename was applied everywhere: redis.ts, verification.ts, health.ts (interface and guard) and the test. Suite **4/4 green**, product tsc rc 0. A correct rename stays green. Test-config tsc gains 1 error over its baseline of 35, a pre-existing stale named import in ks1233 test :31. That error is not from this PR.
   - **3d.** The product was renamed everywhere but the test was left stale: **1 failed (C1) | 3 passed**. This fails loudly and points at the stale pin.
   - **Plain statement:** yes, the suite catches the failure H1 named. Before this PR, H1 measured the KS-1540 suite 5/5 green under the same rename. With this PR, the rename-with-missed-guard reds two cells while the product compiler stays green.
4. **Independence of the controls.**
   - C1 shares only the static `realRedis` import with the RED cells. It does not use HTTP, the express server, `authenticateToken`, the api-key/bearer caches, `createHealthRoutes`/health.ts, or the settings store.
   - C2 shares the `realRedis` import and the fallback settings store (see F1). It does not use HTTP, auth, the route or `isRedisAvailable`.
   - Neither control reads the route's guard, so a guard regression cannot turn a control red. That is what 2 and 3b show: controls green, REDs red.
   - **Broken import (redis path wrong):** the file fails to load with `ERR_MODULE_NOT_FOUND`, "Test Files 1 failed, Tests no tests", rc 1. All four fail together and none passes.
   - **Broken health import path:** `beforeAll` throws, "Tests 4 skipped (4)", "Test Files 1 failed", rc 1. All four are reported identically as not passed (vitest reports skipped, not failed), and the run is red.
5. **`authenticateToken(true)` dependencies.**
   - The api-key path reads `apiKeyCache` and `connectorBearerCache` (middleware/auth.ts:223-224, :193-194). The test pre-seeds both with `expiresAt = Date.now() + 600000`, which is relative, so the outbound `fetch` calls (auth.ts:197, :227) are never reached.
   - No secret is involved: the key `sk_ks1627` and token `connector.jwt.token` are literals.
   - No live Redis (the module is never initialised) and no database.
   - Measured 4/4 green under each of these: plain; `SECURITY_SERVICE_URL`/`AUTH_SERVICE_URL`/`DATABASE_URL`/`REDIS_URL` pointed at 127.0.0.1:1; `NODE_ENV=production`; `TZ=Pacific/Kiritimati`; `JWT_PUBLIC_KEY=` (empty, so setup regenerates it).
   - The test sets **no env var**. Only the shared vitest.setup.ts sets `JWT_PUBLIC_KEY` and `__TEST_JWT_PRIVATE_PEM`, as for every suite. Its cache entries and store write are module-level state, which stays per-file under default isolation (F2 for the non-default case).
   - **Full api-gateway suite:** before (head minus this file, the same tree as develop) **1191/1191, 124 files**, rc 0. After (PR head) **1195/1195, 125 files**, rc 0, which matches the author's 1195.
   - **Neighbours in one run** (ks1627, ks1540, ks1532, ks1232, ks1231, ks1233, ks1256), default isolation: **33/33, 7 files**, rc 0.
6. **Merge prediction.** develop is an ancestor of the head, so the merge is a fast-forward. `git merge-tree --write-tree origin/develop origin/pr1586` gives rc 0, **tree b5a2912563e60460ea1c8a7c3d54beed5c10ae47**, equal to the head's tree.
   - **Overlap check.** Without gh auth there is no open/closed flag, so I used a superset: every `refs/pull/N/head` with N ≥ 1400 whose head is not an ancestor of develop. That is 156 PRs, and it includes squash-merged and closed ones, so it covers the 23 open ones.
     - Path overlap with the new file: **0**. The positive control is the same grep on #1586's own diff, which gives 1.
     - Merge outcome against develop compared with against the #1586 head: **identical for all 156** (83 already conflict with develop on their own, and #1586 changes none).
   - **Planted conflicting control:** a commit on develop adding the same path with other content, merged with the #1586 head, gives merge-tree rc 1, `CONFLICT (add/add)` on the test file. The detector fires.

## NOT tested

- Leg 16 `check.cjs` (the author's claim of 35 = 35 baseline). I did not run it. My own `tsc -p tsconfig.test.json` baseline is also 35 errors (csrf.test.ts and others, pre-existing), unchanged by the PR file at head.
- The author's api-gateway "1195/1195" figure is reproduced. Other workspaces' suites were not run (the PR touches none).
- Open/closed status of PRs (no gh auth in this shell). The overlap check used the superset described in 6.
- CI itself (no GitHub reads beyond `ls-remote`/fetch).

WALL-CLOCK: 10
