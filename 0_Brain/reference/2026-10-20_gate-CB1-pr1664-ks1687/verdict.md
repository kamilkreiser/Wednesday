VERDICT: GO WITH NOTE at head 64a1c1e26f0c... (tier 1, round 1 of 2; landing tree 77613767396979e18840f10289c649067c143604 on develop 7e3b9362e08b1b5b2c418f43e05c9bd0616f896e; 0 blockers, 5 notes)

## BLUF

The product change is what the claim says: 2 files, the product change is only in `token-manager.ts` (+37/-5), there is one `toTokenResult` call site, and the service's only direct read of msal's cache is the `serialize()` line. I reproduced the suite at develop and at the landing (231 -> 240 cells, 0 vanished, 9 new), the author's E1-E5 against the installed msal, K3/K4/K5, the log hygiene on every branch, and 4 of the author's arms plus 2 of my own. Everything was killed by assertion.

**The isolation condition holds for every real-shaped id, but it breaks on near-miss ids, and the cause is inside msal, so the selector cannot see it (N1).** `buildAccountToCache` (msal-common 15.17.0 `ResponseHandler.mjs:326-333`) reuses ANY cached account whose key `startsWith(homeAccountId)`. When one cached account's id has the refreshing account's id as a prefix, or when the refreshing id is empty, msal returns the OTHER account in `result.account`. KS-1682's exact selector then keys on that account and returns the other account's refresh token. I measured this as a new exposure on the refresh path: develop returns '' in the same cells. The sign-in path already has the same hole on develop.

Why this is a NOTE and not a blocker: in Entra ID, `homeAccountId` is `<oid GUID>.<tid GUID>` from `client_info`, which is a fixed 73 characters. One such id cannot be a strict prefix of another, and it is never empty. Control GC8 passes: two GUID-shaped ids that differ only in their last character each get their own token. That reachability argument is INFERENCE about Microsoft's id shapes, not a measurement. **If Wednesday does not accept that inference, N1 is a blocker.** The author's before/after snapshot guard closes N1 as well as the open item (prototype measured, see Q5). That makes the guard worth more than the author's claim gives it credit for.

## Findings

- **N1 (cross-account through msal's own account lookup; measured; reachability is inference).** These are cells in a scratch file, `gatecb1.test.ts`, run against the head with the author's fake transport.
  - GC2b: account x `uida.tidax` refreshed, then account a `uida.tida` refreshed with rotation. The service returns `RT-X-2`, x's token. The cache holds a's own `RT-a-2` under a's id (control), but msal handed back `result.account.homeAccountId = uida.tidax` (GC2 raw msal read).
  - GC2: same, but the refresh of a does not rotate. It also returns `RT-X-2`.
  - GC3: an id differing only by a trailing space in tid (`uida.tida `) leaks the same way. Both refreshes of a return `RT-W-2`.
  - GC4: a response with no `client_info` and an empty `sub` gives `homeAccountId ''`. `startsWith('')` matches the first cached account, so the service returns `RT-A-2`, account A's token, for it. This is "first entry wins" re-entering through msal.
  - On develop all of these return '' (gcdev run: the refresh path never read the cache there).
  - GC7: the same prefix case on `exchangeAuthCode` returns x's token on BOTH trees. This is a pre-existing KS-1682 gap, not something this PR introduced.
  - Case-only ids (GC1) do not leak. msal lower-cases the cache KEY (`msal-node dist/cache/CacheHelpers.mjs:29`) but not `home_account_id`, so a case twin overwrites the entry and the exact selector fails closed with "found 0".
  - What the selector keys on: `result.account.homeAccountId` (`token-manager.ts:274`), compared with `===` to each entry's `home_account_id` (`:290`), with no normalisation. msal sets that field from `client_info` `uid.utid` (`AccountEntity.mjs:179-197`, falling back to `sub`). It does not normalise the value. It only lower-cases cache keys.
- **N2 (author's open item; ruling requested, not a blocker).** Assessment under Q5.
- **N3 (comment overclaims).** The code comment at `token-manager.ts:135-137` says "Nothing else reads that cache". msal's own On-Behalf-Of path (`index.ts:1586`, `acquireTokenOnBehalfOf`) reads the same shared cache. From source it cannot return a forceCache-written token: `OnBehalfOfClient.mjs:125-134` filters by `userAssertionHash`, `CacheManager.mjs:314-315,886-888` require the entity to carry an equal hash, and refresh-flow entries are written with no hash (`RefreshTokenClient.mjs:49` passes `undefined`). So the claim is true for the service's own code but not for msal. This is from source only; no OBO cell was run.
- **N4 (cell coverage gap that hid N1).** K5 seeds its nine neighbours as `RefreshToken` entries only, with no `Account` entities. msal's prefix lookup runs over account keys, so K5 cannot see N1. K3 uses ids that are not prefixes of each other. A cell like GC2b, or the snapshot guard, would pin it.
- **N5 (minor, from source and measured).** The skip at `ResponseHandler.mjs:127-129` applies only when `cacheRecord.account` exists. A response with no id token therefore caches its refresh token even WITHOUT `forceCache` (measured E5b: `rts:["RT-A-2"]`). The service still fails closed in that case (K8, GC5: "no account").

## Answers to the brief

1. **Scope.**
   - `git diff --name-only gdev...pr1664`: `.../__tests__/ks1687-a-rotated-refresh-token-is-persisted.test.ts` and `.../src/auth/token-manager.ts`, +340/-5. One commit, whose parent is develop `7e3b9362e08b`. I read the whole product diff.
   - `git grep -nw` over non-test m365 source:
     - `toTokenResult`: 1 call site (`:144`), plus 2 comment mentions (`:129`, `:237`) and the definition (`:302`).
     - `refreshTokenForAccount`: called at `:99` and `:316`, mentioned in a comment at `:136`.
     - `getTokenCache`: 1 line (`:282`) on both trees.
   - Cache-read surface beyond that: `getMsalClient` (`index.ts:1573`) feeds OBO, see N3.
2. **Isolation.**
   - K3, K4 and K5 pass at the head.
   - GC5 (my interleaved A,B,A, where B's refresh has no id token and A's second refresh does not rotate): A gets `RT-A-2` both times, never B's. B gets '' with the "no account" warning.
   - GC1, GC2, GC3, GC4 and GC8 are covered under N1. Duplicate ids fail closed (K4 measured `found 2`).
3. **forceCache, from the installed source** (msal-node 3.8.10, nested msal-common 15.17.0):
   - `ClientApplication.mjs:100-113` -> `RefreshTokenClient.mjs:49` passes `request.forceCache` as `forceCacheRefreshTokenResponse` -> `ResponseHandler.mjs:127-140`. Without the flag, msal looks up the account (`getAllAccounts` by homeAccountId and environment). If there is none, it warns "refreshed tokens will not be stored in the cache" and returns without calling `saveCacheRecord`. With the flag it falls through to `saveCacheRecord` (`:142`).
   - That is the ONLY thing the flag changes. It does not make msal cache a response for an account the caller did not ask about: the record is built from this response alone (`generateCacheRecord`, `:160-233`). The RT is keyed on `this.homeAccountIdentifier` from this response's `client_info` (`:104`, `:216`), and the id token comes from this response's `id_token` (`:169-170`).
   - The exception is the account ENTITY. Through `buildAccountToCache` it can be merged into another cached account that matches the prefix (N1). The flag widens that exposure: on develop, a refresh into a cache without the account never got this far. The id token's `homeAccountId` is this response's identifier, not the other account's.
   - E1-E5 (GE cell, calling msal directly, no service code, 0 GETs, fake transport only): E1 `[RT-A-2]`, E2 `[]`, E2 with `forceCache:false` `[]`, E3 `[RT-A-2]`, E4 `[RT-A-1]`, E5 `account:null`. `'refreshToken' in result` is false in all 7 runs. This matches the author's table.
4. **Secrets in logs.**
   - Captured through a `winston-transport` instance added to the service `logger` with `logger.add` (GC0 positive control: a direct `logger.warn('control RT-X for uidA.tidA')` is captured and flagged by the detector).
   - Branches covered (GC6): 1 match, 0, >1, no account, and a malformed cache (`serialize` mocked to return invalid JSON that contains `RT-A-2 uidA.tidA`).
   - Result: exactly the 4 expected warnings, in order, and 0 records containing `RT-` or the account id (case-insensitive). The malformed branch does not echo the JSON parse error.
   - GC1, GC2, GC4 and GC5 records: also 0 leaks.
5. **Open item (N2), for a ruling.**
   - Route, measured by reading `index.ts:840-849`: `if (tokenResult.refreshToken) connection.refreshToken = ...`, with no comparison against the stored value, then `dbSaveConnection`.
   - Mechanism, measured at unit level in GC9: a cache that holds `RT-A-OLD` from a sign-in, a refresh that sends `RT-A-NEW` (control: the POST carried `RT-A-NEW`), and a response with no rotation. The service returns `RT-A-OLD`, which the route would persist over the newer token.
   - Likelihood:
     - `services.bicep:1651-1652` gives m365 `minReplicas: 1`, `maxReplicas: 20` (measured from config). Revision rollovers also overlap replicas. The live replica count is unmeasured.
     - A non-rotating response needs Entra to omit `refresh_token`. msal sends `offline_access` by default and Entra normally rotates on every refresh-token grant (INFERENCE, unmeasured).
     - The overwritten token is older but usually still valid (inference). The worst case is a later `invalid_grant`, which surfaces as the existing error status and needs a re-sign-in: visible and recoverable.
   - Ranking:
     - **(1) Per-call isolated token cache.** Either a fresh cache or client per refresh (static authority metadata avoids discovery calls), or remove this account from the shared cache once its token is read. This closes N1, N2 and the accumulation together. Inference; not prototyped.
     - **(2) The author's before/after snapshot.** I measured a prototype (a patched copy, restored by sha256) that only considers entries whose (key, secret) changed during this call.
       - It makes GC2, GC2b, GC3 and GC4 (N1) and GC9 (N2) fail closed to '' with "found 0".
       - K4 now returns the rotated token instead of ''.
       - Non-rotating refreshes return '' (K7, GC5 and GC8 change expectation). That is arguably correct, because the database already holds the token that was sent.
       - The before-read must sit inside the same fail-closed `catch`. My prototype did not, and GC6's malformed-cache case threw a `SyntaxError`.
       - Residual risk (inference): a concurrent rotation of a prefix-colliding account inside the call window.
     - **(3) Return '' when the cached token equals the input token.** Weakest: it does not catch the stale case, because `RT-A-OLD` differs from `RT-A-NEW`.
   - Recommendation: not a blocker for this PR. If any guard is wanted, it should be (2) or (1), because one change closes both N1 and N2.
6. **Red-proof.** Each arm: anchor present exactly once, `tsc -p tsconfig.json --noEmit` rc 0 on the mutant, then the ks1687 file and the 3 ks1682 files (33 cells) run, then restore asserted by sha256 `9ba73cbf...0644` with the anchor count back to 1.
   - Remove `forceCache` -> K1 K2 K3 K4 K5.
   - `forceCache: false` -> K1 K2 K3 K4 K5.
   - First-entry-wins -> K3 K4 K5 plus 16 KS-1682 cells.
   - Case-insensitive near-miss selector -> K5 plus W2.
   - Own O1, first MATCHING entry wins (the >1 refusal removed) -> K4 plus T5.
   - Own O2, empty/non-string secret filter dropped -> W10, W11, L3 (KS-1682 cells; no ks1687 cell covers that clause, which is acceptable because it is KS-1682's).
   - All killed by assertion.
   - Suite by cell NAME (key = file + full describe/title path, as a multiset): develop 24 files / 231 cells / 231 passed -> landing 25 / 240 / 240. 0 vanished; 9 new, all in the ks1687 file. Full-path keys gave 231 distinct names at develop, so there was no undercount.
   - New test file type-checked in its own program (`files: [that file]`, `include: []`, `exclude: []`, extending the service tsconfig): rc 0. Positive control: the same file with an appended `const x: number = "…"` gives rc 2 with TS2322. Service `tsc --noEmit`: rc 0.
   - `merge-tree --write-tree` on live develop gives `77613767396979e18840f10289c649067c143604`, which equals the head tree, at start and at end.

## FOUND / TESTED / HOW

- Clone: `git clone --shared` of the spark cache into the scratchpad `gate_cb1/src`. `refs/pull/1664/head` and `develop` were fetched there with the Blockchain project's deploy key (fetch only, no push).
- Installs:
  - `npm ci --prefix` m365: clean.
  - `packages/shared`: `npm ci --ignore-scripts`, then `npm run build` (tsc rc 0), then symlinked as `m365/node_modules/@secuura/shared`.
- **pglite:** `@electric-sql/pglite@0.5.10` was installed `--ignore-scripts` into a separate scratchpad prefix (`gate_cb1/pglite`) and symlinked into `m365/node_modules/@electric-sql/pglite`. It is not declared in m365.
- Vitest: `npm exec --prefix <m365> -- vitest run --root <m365>`, with `--reporter=json` for the suite and the arms.
- My cells live in an untracked scratch file in the clone (`gatecb1.test.ts`, 12 cells, all green at the head; 8 of them red at develop because the refresh path returns '' there). The arm and prototype scripts are in the scratchpad.
- Heads (ls-remote): #1664 `64a1c1e26f0c7f8b2711b4f377143cc069a4a9fd` and develop `7e3b9362e08b1b5b2c418f43e05c9bd0616f896e`, at 02:15:37Z and 02:25:16Z. Unchanged.

## NOT RUN

- No real Microsoft: whether Entra returns `refresh_token`/`id_token` on refresh, and whether it ever issues non-GUID or empty `homeAccountId`s (N1's reachability is inference).
- No route-level end-to-end run of `POST /api/connections/:id/refresh`.
- No OBO cell (N3 is from source only).
- msal's own logger output, which the service does not configure.
- The four platform suites, the author's preflight, and Docker.
- Option (1) of Q5 was not prototyped.
- Wednesday tree check: `git status --short` lists no untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/. Nothing was written here except this file.

## Wall-clock

02:15Z -> 02:28Z (about 13 min).
sha256 of `sed '1d;$d' verdict.md | shasum -a 256` = 31b631a3cc6f9adccd95489f0f382f60a394a8e3540c4b169bbca9db08868e8b
