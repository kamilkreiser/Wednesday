VERDICT: GO WITH NOTE at head f2827e39d5c5... (tier 1, round 1 of 2; landing tree 785b2b7cfff7 on develop cd63883c62a9; 0 blockers, 4 notes)

## BLUF
The product code does what the ruling says (shape 1). No path I could build returns another organisation's refresh token: 118 permutation cells across 2, 3 and 4 accounts, a sequential A-then-B-then-C sign-in on one shared client, same-uid/different-tenant, same homeAccountId in two realms, case, whitespace, prefix and substring variants, and orphan entries all give the signer's own token or ''. All four fail-closed branches (plus two extra unreadable shapes) store '' and log with no token material and no account identifier. The author's M1, M2 and M3 reproduce exactly. Landing tree 785b2b7cfff7 is confirmed on live develop, tsc rc 0, m365 suite 22 files / 212 / 0 failed, 0 cells vanished.
The note that matters (N1): **five of my selector mutants survive the PR's own six cells.** They are case-insensitive, trimmed, substring and uid-only comparison, and accepting an orphan entry. The code is right today, but the suite does not pin exact equality, so a later "tidy" that loosens the comparison would pass CI. Not a blocker, because the ruling's cell list was delivered in full and nothing returns a wrong token at this head. Worth a follow-up cell before or soon after merge.

## Findings
- **N1 (test-strength gap, selector):** the PR's T1–T6 do not kill G3 (compare the uid part only, ignoring the tenant), G4 (case-insensitive), G5 (trimmed), G6 (`includes` substring) or G7 (an entry with no home_account_id accepted). Under G4, G5 and G6 a variant homeAccountId selects the VICTIM's token ('RT-VICTIM' returned). My cells Q1c, Q1e and Q1f/Q1f2 kill all five. Suggested fix: add an exact-match cell (case, whitespace, prefix, substring, orphan) to the KS-1682 file.
- **N2 (downstream of '', report only, Q3):** after a fail-closed exchange the callback (index.ts:651-:675 at the landing) still sets `status='connected'`, stores `refreshToken=''` (encryptToken maps '' to SQL NULL, tokenCrypto.ts:42) and redirects with `m365=success`. Nothing is shown at sign-in. When the access token expires (about 1h), each Graph route passes Graph's 401 through to the caller (for example :1161-:1167, "OneDrive API error"). `GET /api/connections/:id` shows `tokenExpired: true` while status stays `connected` (:794). `POST /api/connections/:id/refresh` answers 400 "No refresh token available" (:835-:837). Nothing refreshes automatically (`refreshAccessToken` has one caller, :840). Result: a silent sign-in, then a visible but unexplained failure about an hour later. Not judged.
- **N3 (existing rows not remediated):** reads from the DB (index.ts:204, :287) return whatever was stored before this fix, including a wrong organisation's RT. The refresh path then keeps it (:844-:845; T6 pins that the guard never fires). The PR does not touch stored rows. The author's dormancy figure (demo 0 rows, kintsugi NOT measured) is the only evidence that no such row exists.
- **N4 (where the warnings go):** the three KS-1682 warnings go to `console.warn` (token-manager.ts:244, :253, :261), not to the service's structured `log()`. The catch at :252 also deliberately drops the error. Good: a Node JSON SyntaxError message can quote part of the input, so dropping it is the safe choice. The cost is that these lines may not reach whatever collects `log()` output. Report only.
- **Q2, every write of `connection.refreshToken` (develop = landing, same lines):** :654 comes from exchangeAuthCode, whose only non-selector source is `(result as any).refreshToken` (token-manager.ts:96). That is msal's own result for this exchange, and the claim that msal never sets it is the author's SOURCE READING, not observed. :812 sets `undefined` (disconnect). :845 is the refresh path via toTokenResult :279, using the connection's own RT. :204 and :287 are DB reads (see N3). No other path makes it non-empty.

## FOUND / TESTED / HOW
- **Heads:** read at start and end with `ls-remote` (via the cache's origin): #1651 = f2827e39d5c518fb532ee183724eb7a8057f2538, develop = cd63883c62a9bb0e66969df8cd3f02db2b9b2217, unchanged across the gate. Merge-base 89956fe92956. `merge-tree --write-tree gh/develop gh/pr1651`: rc 0, **785b2b7cfff7b74c6721c1955f960b77fb19759f**, matching the author. `develop...head` is 2 files, +176/-10. The head's own tree is d45992afa78a.
- **Harness:** a `git clone --shared` of the cache, with the PR and develop fetched into the scratch clone only. Worktrees `dev` (cd63883c62a9) and `land` (a local commit-tree of 785b2b7cfff7, never pushed). `npm ci` per worktree, `@secuura/shared` built and symlinked, `@electric-sql/pglite@0.4.1` (the root lock version) installed `--no-save` because the workspace hoists it.
- **Q6:** `tsc --noEmit` rc 0 with 0 diagnostics at the landing, and also rc 0 at develop.
- **Q5:** the vitest JSON reporter, compared by file+fullName. develop 21 files/206 cells; landing 22 files/212 cells, 212 passed. **Vanished 0, new 6** (exactly the KS-1682 T1–T6). The test files were type-checked in their own program (a child tsconfig with `exclude: []` kept in scratch): rc 0, 0 diagnostics, at both ends. Control: 22 (landing) and 21 (develop) `__tests__` files were in the program, not 0.
- **Q4 red-proof (develop arm):** I ran the author's file on real develop (asserted: `refreshTokenForAccount` absent, `Object.values(refreshTokens)[0]` present). T1, T3, T4 and T5 FAIL by assertion; T2 and T6 pass. That matches the claim.
- **Q4 mutants:** these ran on the landing snapshot via `scratchpad/gate_bl1/mutants.py`. Each anchor was asserted unique, each swap was asserted by sha256 change, and each restore was asserted by sha256 == e679378db536…1a1e. Every arm had tsc rc 0 and none produced a LOADFAIL. Killers per arm:
  - M1 `[0]` restored: T1, T4, T5 (author's row exactly) + Q1a–Q2.
  - M2 null falls back: T3 only among the author's (exactly) + Q2.
  - M3 multiple picks first: T5 only (exactly) + Q1d, Q2.
  - G1 3-char prefix: T1, T4 + Q1a, Q1b, Q1c, Q1f2, Q2.
  - G2 last match: T5 + Q1d, Q2.
  - **G3 uid-only: Q1c, Q1e only. SURVIVES T1–T6.**
  - **G4 case-insensitive: Q1e only. SURVIVES.**
  - **G5 trimmed: Q1e only. SURVIVES.**
  - **G6 substring: Q1e only. SURVIVES.**
  - **G7 orphan accepted: Q1f, Q1f2 only. SURVIVES.**
- **Q1/Q2 adversarial file** (`scratchpad/gate_bl1/zz-gate-bl1-adversarial.test.ts`): it used the PRODUCT's `initMsal`/`exchangeAuthCode`, a real msal-node 3.8.10 ConfidentialClientApplication (msal-common 16.14.1) and a real cache, with only `acquireTokenByCode` stubbed (`serialize` was stubbed only in the cells that say so). Seed reaching the cache was asserted per cell.
  - Landing: 8/8 pass. Develop: 8/8 FAIL by assertion (e.g. "expected 'RT-SECRET-uidA.tidA' to be 'RT-SECRET-uidB.tidB'"), so every cell can fail.
  - Cells:
    - Q1a: 118 order×signer cells over 2, 3 and 4 accounts.
    - Q1b: sequential A→B→C on one client, with a stub that writes each RT into the real cache the way msal would (control: the cache held 3).
    - Q1c: uidX.tidA vs uidX.tidB, both orders.
    - Q1d: the same homeAccountId under two realm keys stores ''.
    - Q1e: case, leading/trailing space, `\n`, `uidB`, `uidB.`, `uidB.tid`, `.tidB` all store '' and never the victim's token.
    - Q1f/Q1f2: orphan alone stores ''; orphan with the signer before or after picks the signer's; null home, '' secret, numeric secret and a null entry are all safe.
    - Q2: null account, '' homeAccountId, zero match, multiple match, unparseable JSON, serialize throws, and `RefreshToken` as a string all store '', with the access token still returned.
- **Log hygiene:** every console line in the file was captured (171 lines; 22 KS-1682 warnings covering all three warning branches: 2 no-account, 2 unreadable, 18 count). None matched `RT-`, `uid?.tid` or the other test ids. Positive controls: the matcher catches a planted secret and a planted id, and the KS-1682 count is greater than 0 (it was 0 at develop).
- **Network:** `fetch`, `http(s).request` and `http(s).get` were replaced with throwing recorders. Zero calls were recorded. Positive control: a planted `fetch` was recorded. Nothing reached Microsoft.

## NOT RUN
- No real msal `acquireTokenByCode` writing the cache. Q1b's cache write is my imitation of msal's, not msal's own. Whether msal ever writes two RT entries for one homeAccountId (Q1d's shape) was not measured.
- No real sign-in, no real refresh, no Graph call, no Docker, no platform suites, no DB (the pglite real-engine suites ran only as part of the m365 suite).
- Concurrency (two interleaved sign-ins on the shared cache) was not measured. I only reasoned that it lands on the >1 or 0 branch.
- B2B guest semantics (the home-tenant RT used for a resource tenant) and the same Microsoft user connecting two Secuura organisations (both store that user's own RT) were not tested; both are outside this PR's change.
- The author's preflight (13/16 legs) and the `.githooks/pre-push` citation were not re-run. Kintsugi was not read. The PR body, ticket comment `a00e1f76…` and the GitHub PR were not read (no GitHub API reads).
- The author's "201 at the merge-base" figure was not checked. I measured develop (206) and the landing (212) only.

## Wall-clock
23:14:53Z → 23:22Z (2026-10-19 UTC; 10:14 → 10:22 AEDT 2026-10-20), about 8 min.
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): c8f821c43cc48880224bc5507be8e6477c132b4c353f82435f7da807ed234cce
