VERDICT: GO WITH NOTE at head efd79bc87b36... (tier 1, round 2 of 2; landing tree 53062901f1fb4ca6f3ad50a48f313f697b62d786 on develop f01ba49da56d3d55204caa02ab3348f94d63b9c0; 0 blockers, 4 notes)

## BLUF

The snapshot guard does what the claim says, and it closes both of my round-1 findings.
- **Round-1 findings closed.** All five of my CB1 cells (GC2, GC2b, GC3, GC4, GC9) now fail closed to `''` on the new head. Each one first checks its premise, which holds: msal still hands back the other account. When I remove the guard, all five go red again with the other account's token, or with the stale token for GC9.
- **Scope.** The product change is 2 files. The sign-in path is unchanged. `toTokenResult` has 1 call site (`:177`). msal's cache is read by serialisation at exactly the 2 code lines the author names (`:317`, `:335`).
- **Suite.** At develop: 24 files / 231 cells. At the head: 25 files / 248 cells, all passed, 0 vanished, 17 new, all in the KS-1687 file.
- **Merge-tree.** On live develop it gives `53062901f1fb`, which is the head tree. Heads were unchanged at the start and at the end.
- **Arms.** I re-ran 7 of the author's arms and 6 selector arms, plus 2 of my own. Every one compiled before it counted, and every restore matched by sha256. All results agree with the claim, with one correction: the author's "equivalent" arm is not strictly equivalent (N4).

**What remains, all notes:**
- **N1, measured.** The concurrency residue that the author stated is real. I measured it with the fake transport: P is handed X's freshly rotated token, and nothing warns. It needs a prefix-colliding id, which is still inference: Entra issues fixed-length GUID ids.
- **N2.** A snapshot that parses but has the wrong shape is read as an empty cache, so it is not null. msal's source never produces one.
- **N3.** Test-file comments still credit K5 and K3 with killing the selector mutants. They no longer kill them.
- **N4.** The equivalent-mutant reasoning is slightly off, but the difference is benign.

## Findings

- **N1 (Q3b, MEASURED: the stated residue reproduces).** `GC10`, async fake transport:
  - X (`uida.tidax`) is cached. P (`uida.tida`) starts a refresh. Its snapshot is taken and its POST is held in flight (control asserted).
  - X then refreshes to completion and rotates to `RT-X-3`. After that, P's response is released, rotating to `RT-P-2`.
  - Premise: msal's raw result for P carries `homeAccountId = uida.tidax`.
  - Result: P's `refreshAccessToken` returns **`RT-X-3`, with 0 warnings**. The route would store X's live token on P's connection.
  - Control `GC10c`: the same interleaving with a non-colliding account B gives P its own `RT-P-2`.
  - Mechanism: the guard admits X's entry, because it changed inside P's window, and the exact selector keys on msal's wrong `result.account`.
  - This is exactly the residue in the code comment (`:166-169`) and in the claim's "Not claimed" list. It is now measured rather than inferred.
  - Why it is still a NOTE: it needs both a prefix-colliding id and a concurrent rotation inside the window. Whether Entra ever issues a non-fixed-length or empty `homeAccountId` is inference (CB1 GC8: GUID.GUID ids do not collide).
  - Option 1 from CB1 (a per-call isolated cache) is the only remedy that also closes this. That is follow-up material, not a blocker for this round.
- **N2 (Q3a, measured; reachability from source).** `snapshotRefreshTokens` returns null only when `serialize()` throws or `JSON.parse` throws. Then there is no selection, and the warning goes out with the error dropped (K14, K14b, and my GC11 "throws" and "unparseable" cases, `reads: 1`).
  - A cache that PARSES but has the wrong shape gives an EMPTY Map, not null. I measured three such values from the before-read: `null`, `42`, and `{"RefreshToken":null}`. Every entry then counts as "changed", so selection runs unguarded. With a prefix collision armed, GC11 returns `RT-X-2` in all three cases.
  - Not reachable from msal: `TokenCache.serialize` returns `JSON.stringify(Serializer.serializeAllCache(...))`, and that always builds `RefreshToken` as an object (msal-node 3.8.10 `TokenCache.mjs:44-56`, `Serializer.mjs:134-141`). The service never calls `deserialize`.
  - The doc line "or null if the cache cannot be read" is literally true. It is weaker than "a malformed cache means no selection".
- **N3 (Q6, comments that are now false, test file only).**
  - **K5's title** (`:315`) says "the BR1/BW1 mutants must still red at this size". **Its inline comment** (`:338-339`) says "Any selector that also matches ONE neighbour makes the count 2 and this '' -- red by assertion. The old `Object.values(...)[0]` would return RT-NB-UID-ONLY -- red as well".
  - **The file header** (`:38-39`) says "K3 and K5 prove it at the larger size".
  - Measured: K5's nine neighbours are seeded BEFORE the call, so the guard filters them out. None of S1-S5 and not first-entry-wins (R7) reds K5 or K3, measured across the full suite.
  - The author's READY claim and PR are honest about this ("no longer killed by ANY KS-1687 cell"). Only the test file's own text still claims the old coverage.
  - Product file, cosmetic: the new `RtSnapshot` type and `snapshotRefreshTokens` were inserted between the long KS-1682 JSDoc (`:268-305`) and `refreshTokenForAccount` (`:326`). That doc now attaches to `type RtSnapshot`.
- **N4 (Q4, the "equivalent" arm is benign-equivalent, not equivalent).** Arm R6 is "changed = the secret appears in no earlier entry, ignoring the key".
  - It survives all 260 cells of the suite plus my file, which reproduces the author's result.
  - My cell `GC14` kills it. A sign-in caches `RT-S` for `uidA.tidA`. A refresh then gets a response for `uidA.tidA2` that echoes `RT-S`, so msal writes the same secret under a NEW key (control: two keys, same secret). The head returns `RT-S`; the mutant returns `''`.
  - So the distinguishing input exists. The server, not msal, decides it, and "msal does not" is the wrong reason. In both outcomes the result is the token already sent, or nothing, so it is benign.
  - My own O2, dropping the `!before.has(key) ||` clause, survives everything. It IS equivalent: a new key gives `before.get(key) === undefined`, and that differs from any string secret. The only case it changes, an undefined secret, is then dropped by the `typeof e.secret === 'string'` filter. The clause is redundant but harmless.

## Answers to the brief

1. **Scope and product diff.**
   - `git diff --name-only gdev pr1664` lists 2 files: the KS-1687 test (+500) and `token-manager.ts` (+104/-9 against develop). I read the whole product diff.
   - The head is merge `efd79bc87` with parents `72e47d849` (round 2) and `f01ba49da` (develop). Develop is an ancestor (rc 0). The develop side brings 4 unrelated files.
   - `exchangeAuthCode` (`:79-108`) is byte-identical to develop; the only sign-in change is a doc line.
   - `refreshTokenForAccount(result)` on the sign-in path passes no `before`, so it takes the unfiltered branch (`:339`).
   - `toTokenResult`: 1 call site (`:177`), plus the definition (`:359`) and 3 comment mentions.
   - Reads of `getTokenCache()`/`serialize()` in non-test m365 src: code lines `:317` and `:335`; `:138` is a comment.
   - Persistence plugin: 0 hits in service src. Positive control: the same grep finds `DistributedCachePlugin.mjs` in msal-node.
2. **N1/N2 on the new head (`gatecg1.test.ts`, my CB1 cells copied into my own clone; the harness responder was made awaitable):**
   - **GC2** (prefix, non-rotating): premise raw account `uida.tidax`; returns `''` with `found 0`; 0 leaked records.
   - **GC2b** (prefix, rotating): premise holds; the cache holds a's own `RT-a-2` (control); returns `''`.
   - **GC3** (trailing space): both refreshes have premise `uida.tida `; both return `''`.
   - **GC4** (empty id): premise `uidA.tidA`; the `''`-id entry is stored (control); returns `''`.
   - **GC9** (replica): `RT-A-NEW` was sent and the cache holds `RT-A-OLD` (controls); returns `''`.
   - None returns another account's token. Under arm R1 (guard removed), all five return the other or stale token again.
3. **The guard.**
   - (a) The before-read is inside its own `catch` (`:316-323`). In `toTokenResult`, a null snapshot skips selection entirely (`:374`).
     - K14 and K14b pass.
     - GC11 "throws" and "unparseable" give `''`, an access token, `reads: 1`, exactly the catch warning, and no leak.
     - Arms R3 (before-read outside the catch) and R5 (null still selects) are each killed by K14 and K14b (plus GC11).
     - The wrong-shape case is N2.
   - (b) Measured as N1, with the GC10c control.
   - Also measured, GC10d: two concurrent refreshes of the SAME account. The one whose response lands second gets `RT-A-3`. The first-sent call, released last, gets `RT-A-2`, and the cache ends at `RT-A-2`. Each call returns a token msal really wrote for that account, so no cross-account leak. Which one the database keeps depends on the order of the saves. That is a general rotation race, not one this guard creates.
   - (c) GC12: a non-rotating echo, with the same secret under the same key, returns `''` with `found 0`. After a restart, the same echo returns `RT-A-1`, a new key whose value equals what was sent, which is harmless.
     - The route (`index.ts:840-849`): `if (tokenResult.refreshToken)` skips on `''` and `dbSaveConnection` still runs.
     - Measured at route level by `gatecg1route.test.ts`, a real router over 127.0.0.1 with `../db`, `tokenCrypto`, `refreshAccessToken`, `authenticate` and `listen` mocked, following the ks1673 seam.
     - **GR1:** `''` gives 200, and the INSERT's `refresh_token` param is the PREVIOUS `RT-DB-c_empty`. A second refresh sends that same DB token.
     - **GR2 control:** a returned token is persisted as `ENC(RT-ROTATED)`.
4. **Coverage honesty (full m365 suite, 25 + my 2 scratch files).**
   - S1 case-insensitive: killed only by KS-1682 W2.
   - S2 includes: killed by W3, W4, W7, W8, L2, L4, L5.
   - S3 accept-no-id: killed by W5.
   - S4 startsWith: killed by W7.
   - S5 endsWith: killed by W8.
   - **0 KS-1687 cells and 0 of my gate cells red for S1-S5.** The claim is confirmed. Note that S1, S3, S4 and S5 each rest on a single KS-1682 cell.
   - S6 reverse-startsWith: killed by K9, K11, K12, W1, W9 and my GC2b, GC3, GC4, as claimed.
   - Equivalent arm: see N4.
5. **Red-proof.** Each arm: anchor present exactly once, service `tsc --noEmit` rc 0 on the mutant, then the full suite as JSON, then restore asserted by sha256 `840dd7db…d1cf` with the anchor count back to 1. All 15 arms (R1-R7, S1-S6, O1, O2) and the R6 re-run restored OK. The author's arms re-run:
   - **R1 guard removed:** K4, K7, K9, K10, K11, K12, K13, matching the claim, plus 6 of my cells.
   - **R2 snapshot AFTER the call:** K0, K1, K3, K4, K4b, K5, K9 (7 KS-1687 cells), plus 7 of mine.
   - **R3 before-read outside the catch:** K14 (throws), K14b (SyntaxError), GC11.
   - **R4 remove forceCache:** 10 KS-1687 cells (K1-K5, K4b, K9-K12), plus 9 of mine.
   - **R5 unreadable snapshot still selects:** K14, K14b, GC11.
   - **R6 equivalent:** 0 of 260; GC14 kills it.
   - **R7 first-entry-wins:** K4b, K9, K11, K12, 16 KS-1682 cells, and 4 of mine.

   My own arms:
   - **O1, the snapshot stores the entry object instead of the secret** (this silently disables the guard): 13 red, including K4, K7, K9-K13.
   - **O2:** survives, and is equivalent (N4).

   Two first attempts (R1 `before && false`, R6 with an unused `key`) were tsc rc 2. They were not counted and were rewritten to compile.

   Suite and type-check:
   - **Suite by cell NAME** (key = file + describe/title path, as a multiset): develop 24/231/231 passed, then head 25/248/248 passed. 0 vanished, 17 new, all in `ks1687-…test.ts`.
   - Positive control for the vanished count: dropping one develop key from the head set gives vanished 1.
   - The test file type-checked in its own program (`files: [that file]`, `include: []`, `exclude: []`, extending the service tsconfig; `--listFilesOnly` confirms the file is in the program): rc 0.
   - Positive control: an appended `export const x: number = "…"` gives rc 2 with TS2322. The file was restored with sha256 `adb03354…9ccb` matched. Service `tsc --noEmit`: rc 0.
6. **Comments are claims.** Checked against the code and msal 15.17.0 / msal-node 3.8.10 source:
   - `ResponseHandler.mjs:127-139` (the drop without forceCache) holds.
   - `:295-312` (no `refreshToken` key in the result literal) holds.
   - `:326-333` (`accountKeys.find(k => k.startsWith(homeAccountId))` at 326-329) holds.
   - `RefreshTokenClient.mjs:49` passes `undefined` as `userAssertionHash`, per the `handleServerTokenResponse` signature at `:82`. Holds.
   - `CacheManager.mjs:314-315` and `:886-888` (an equal hash is required) hold. The corrected N3 comment is accurate, and it says it is a source reading.
   - "A non-rotating refresh then returns '' … the route only persists a non-empty value": measured (K7, GC12, GR1).
   - "two serialisations of the cache per refresh": true against develop, which had 0.
   - The residue paragraph is accurate, and now measured (N1).
   - The READY claim's numbers reproduce: 248/248, 0 vanished, 17 new, landing `53062901f1fb`, the K-cells killed by R1, and the selector-mutant consequence.
   - The exceptions are the stale test-file comments in N3.

## FOUND / TESTED / HOW

- **Heads (ls-remote):** #1664 `efd79bc87b36f7d570c29785ce8b0ceb06f8c10e` and develop `f01ba49da56d3d55204caa02ab3348f94d63b9c0`, at 02:54:41Z and 03:06:33Z. Both unchanged and equal to the claim.
- **Clone and fetch:** `git clone --shared` of the spark cache into `scratchpad/gate_cg1/src`. `refs/pull/1664/head` and `develop` were fetched there with the Blockchain project's deploy key via `GIT_SSH_COMMAND`. Fetch only, no push.
- **merge-tree:** `merge-tree --write-tree` on develop and the head gives `53062901f1fb4ca6f3ad50a48f313f697b62d786`, which equals `efd79bc87^{tree}`. Develop's tree is `38200e78045e`.
- **Installs:**
  - `packages/shared`: `npm ci --prefix … --ignore-scripts`, then `npm run build --prefix …`, then symlinked as `m365/node_modules/@secuura/shared`.
  - m365: `npm ci --prefix`.
- **pglite:** it is undeclared in m365. I symlinked CB1's scratchpad install (`gate_cb1/pglite`, `@electric-sql/pglite` ^0.5.10, installed `--ignore-scripts`; used read-only) into `m365/node_modules/@electric-sql/pglite`.
- **Vitest:** `npm exec --prefix <m365> -- vitest run --root <m365>`, with `--reporter=json` for the suite and the arms.
- **Scratch cells (untracked, in the scratch clone only):**
  - `gatecg1.test.ts`, 13 cells, all green at the head: GC0 transport control, GC2, GC2b, GC3, GC4, GC9, GC10, GC10c, GC10d, GC11, GC12, GC13 positive, GC14.
  - `gatecg1route.test.ts`, 2 cells.
- **Arms:** run by `scratchpad/gate_cg1/arms.py`.
- **msal versions:** msal-node 3.8.10, nested msal-common 15.17.0.

## NOT RUN

- No real Microsoft. Whether Entra ever issues prefix-colliding or empty ids (N1 reachability) and whether it rotates or echoes refresh tokens are both inference.
- No OBO cell: the N3 comment is checked against source only.
- No real database: the route cell mocks `../db` and `tokenCrypto`.
- Not every one of the author's 20 arms was re-run: 7 of theirs plus the 6 selector arms. "new key only", "drop-the-id-match" and "count>=1" were not re-run.
- The four platform suites, the author's preflight, and Docker.
- The GC7 sign-in hole is out of scope; it is unchanged and pre-existing.
- **Wednesday tree check:** `git -C /Volumes/DevMASTER/WEDNESDAY status --short` lists untracked paths only under `0_Brain/`, `2_Project_Files/local-model/` and `2_Project_Files/fleet/briefs_staged/`. None is outside the allowed set. This gate wrote only this file.

## Wall-clock

02:54Z -> 03:09Z (about 15 min).
sha256 of `sed '1d;$d' verdict.md | shasum -a 256` = 73cf8991712f7b13496dc171ae301486560c24669d73edd01d931f5c15264669
