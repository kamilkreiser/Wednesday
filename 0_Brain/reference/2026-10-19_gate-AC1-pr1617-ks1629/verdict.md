VERDICT: GO WITH NOTE at head f8b3bf0cd313... (tier 1, round 1 of 2; landing tree 83c945a644b8 on develop 8323f2f70cd7; 0 blockers, 3 notes)

# GATE AC1: PR #1617 (KS-1629), independent tier-1 code gate

- Gate: AC1 (Opus), round 1 of 2. Findings only. Nothing written under `!CODING`, no GitHub or Linear writes.
- Instruments ran in my own clone: `scratchpad/ac1/repo`. I fetched `develop` and `refs/pull/1617/head` from origin. The project repo was used read-only (`ls-remote`, `config --get`).
- Heads, read at 08:34:36Z and again at 08:43:26Z with `git ls-remote origin`: develop `8323f2f70cd796219774f240184f777813c28aec` and #1617 `f8b3bf0cd313e1a2505094514262ff8f43387dd2`. Neither moved.
- Merge-base: `80868551e67934cb951d28eec44ce3bdf835944c`.

## Blockers
None.

## Notes
1. **The census claim "0 config / compose / deploy / bicep / env files set it true at all" is false.**
   - `Blockchain/Dev/deployment/azure/services.bicep:790` sets originate's `{ name: 'SIMULATE_ANCHORING', value: environment == 'demo' ? 'false' : 'true' }`. The `param environment` default is `'staging'` (`:21`), so every bicep deploy except demo gets the opt-in.
   - `deployment/azure/env.demo.json:10` sets `"SIMULATE_ANCHORING": "true"`. Its own `_comment` calls it reference only.
   - Neither line matches the author's literal `= 'true'` shape. I found them with a quoted-key `[:,=]` regex and a ternary read, and the control was the same pattern with `false`, which found `orchestration.py:311` and `env.dev.json:10`.
   - This does not change the code verdict. The PR only removes a write, so those environments get safer.
   - It does correct the severity framing. "Live only under an explicit opt-in" should read: the opt-in is the bicep default for any non-demo Container Apps deploy. `systemTest/performance/config/environments.yml:35` says the old `*.azurecontainerapps.io` hosts are dead. I did not verify whether any such environment is live.
2. **"The file's other 9 cells" overstates what pins KS-520.**
   - The 9 are 7 `it` blocks, one of which is an `it.each` × 3. Without the re-pin that leaves 9 executed tests (confirmed by jest: 17 = 7 + 10).
   - Only **2 of the 9** are KS-520 cells: the POST auto-anchor fail-closed cell, and the GET 404 with no write when the flag is unset. The other 7 are KS-1124 cells that share the file.
   - KS-520's property is still pinned, by those 2 plus the re-pinned cell. The claim's wording implies 9.
3. **Pre-existing, now in both modes: `getAnchorByDocumentId` returns null on a DB error (`anchors.ts:90-93`).**
   - A database failure therefore answers 404 "No anchor found", not 500.
   - With the flag unset this was already true at develop. Under the opt-in, develop would have attempted `saveAnchorToDb` and probably answered 500.
   - Not introduced by this PR, and not a blocker. It is the one behaviour on this path a reader might not expect.

## Q1. Is the read path a pure read in every mode? YES
- Instrument: read the whole GET handler at the head (`git show origin/pr1617:…/routes/anchors.ts`, lines 168-238).
- Calls reachable from the handler:
  - `getUserFromRequest`, `validationResult`
  - the `non-existent`/`missing` early 404
  - `getAnchorByDocumentId` (`:85` `$queryRaw` `SELECT * FROM anchor_store … LIMIT 1`, read-only)
  - the `!anchor` → 404 return
  - `isSimulatedAnchor`, `res.json`
- There is no `saveAnchorToDb`, no `$executeRaw`, and no INSERT/UPDATE.
- The handler no longer reads `process.env` at all. True, unset and any other value (`'1'`, `'TRUE'`, `''`) therefore take the identical path. The 404 decision hangs only on whether a row exists.
- `saveAnchorToDb` survives only in POST `/` (`:340`) and POST `/submit` (`:440`), so `crypto` and the helper are still used. tsc with `noUnusedLocals` is rc 0.
- Mock write counts, from my runs at the landing tree:
  - `mockExecuteRaw` calls = 0 on A1, A2, B1, C1 and C2, and on the re-pinned ks520 cell. Each asserts `not.toHaveBeenCalled()` or a delta of 0, and each is green.
  - Positive control: with develop's `anchors.ts` the same counter reads `Received: 1` on A2.

## Q2. Did the change go too far? NO
- **C1:** a real anchor row (`'f'×64`, `simulated:false`) under the opt-in answers 200 with `transactionId` = the hash and `verified:true`. Green at the landing tree.
- **C2:** a stored `tx_sim_…` row with `simulated:true` answers 200 with `[transactionId, simulated, simulatedTxRef, verified]` = `[null, true, SIM_TX, false]`. This is the KS-587/522 shape. Green.
- **My own over-reach mutation:** I changed `if (!anchor)` to `if (!anchor || process.env.AC1_NEVER !== 'set')`, which makes the 404 unconditional. **C1 and C2 both red. A1-B2 stay green.** C1 and C2 therefore discriminate. Head restored, sha256 `2b83513a…` byte-identical before and after.
  - An earlier `if (true || !anchor)` form failed TS compilation (0 tests ran) and was discarded, not counted.
- **Verify routes:**
  - `routes/verification.ts`: `/verify` `:840`, `/verify-file` `:654`, and the `:1177-1186` chain-verify leg.
  - `routes/verificationV2.ts`: `/verify` `:425`, `/verify-file` `:504`.
  - All of them read anchors from the **anchoring service**, through `${ANCHORING_SERVICE_URL || 'http://anchoring:4005'}/api/anchors/verify/<hash>` (`verification.ts:439/706/1184`, `verificationV2.ts:102-103`).
  - None imports from `routes/anchors`. The only importer outside tests is `index.ts:22/43`.
  - `getAnchorByDocumentId` is module-private, and none of these files is in the 3-file diff (`grep -ci verif` over the three-dot list = 0).
  - Unaffected.

## Q3. The re-pinned ks520 assertion: an honest contract change, not a weakening
- **Old expectation (develop `:170`):** `toBe(200)`, `transactionId` null, `simulated` true, `simulatedTxRef` matching `/^tx_sim_/`, `verified` false.
- **New expectation (head `:185`):** `toBe(404)`, `error.code === 'NOT_FOUND'`, no `tx_sim_` anywhere in the body, `mockExecuteRaw` not called.
- This matches ruling (b) exactly. It is a contract change, not a weakening.
  - The old cell pinned honest labelling of a fabricated anchor.
  - The new one pins that no anchor is fabricated and nothing is written.
  - Honest labelling of a stored simulated anchor moved to ks1629 C2, which is green.
  - The cell's comment quotes the old expectation, and header item 2 was updated. Disclosed as required.
- With the product parked at develop, the re-pinned cell **reds** (`Expected: 404 Received: 200`). All 9 others stay green both at develop and at the landing tree. See Note 2 for which of the 9 are actually KS-520.

## Q4. Consumer census (re-run independently): no consumer depends on a synthesized 200
- **Regex:** POSIX `[[:space:]]` only.
  - Feature control: `process\.env\.SIMULATE_ANCHORING[[:space:]]=[[:space:]]'true'` on the ks1629 file returns 6, so the class works.
  - Side observation: the dead `\s` form read 32 here, not 0. git's ERE treats `\s` as a literal `s`, so `s*` matches the no-space spellings only. It is not a zero, but it measures something else.
- **JS/TS files setting `= 'true'`:** 31 at the head. That is 30 at develop plus the new ks1629 file, which matches the author's 30.
  - Of those, the ones that import `routes/anchors` or hit `/api/anchors/` or `/api/anchoring/`: `ks520` and `ks1629` only, which matches the author's 1 at develop.
  - Control: files referencing `routes/anchors` = 6 at develop and 7 at the head, and 49 `.ts` files reference `/api/anchors/`.
  - The author's 8 / 48 differ by method. Immaterial: the narrowing is real.
- **Gateway:** `api-gateway/src/routes/proxy.ts:873-893` proxies **all** of `/api/anchors` and `/api/anchoring` to the **anchoring** service (`config/services.ts:107`), never to originate. Originate's GET is reachable only service-internally (`originate:4000`). This shrinks the blast radius of both the bug and the change.
- **Schemathesis:** `fixtures/orchestration.py:311` sets `"false"` and `:332` sets `""`. These are the only `SIMULATE_ANCHORING` assignments in that file. Neither reaches the old branch.
  - Every other `.py` hit is a comment or docstring.
  - `test_anchor_read_honesty.py:84` does `GET /anchors/{document_id}` through the issuer client (the gateway, so the anchoring service). It does so after waiting for an anchor row to exist, so it takes the stored-row path, not synthesis.
- **e2e:** `tests/e2e/.../recruitment-helpers.ts:276` requires a truthy `transactionId` and `blockNumber > 0`. A synthesized anchor (null / 0 since KS-587) would already fail that, so it does not depend on synthesis. `alternative-paths.spec.ts:250` expects the `non-existent` 404, which is unchanged.
- **OpenAPI:**
  - `docs/openapi/secuura-api.yaml` has no `/api/anchors/{documentId}` path. Its `/api/anchors*` keys are `/api/anchors`, `tx/{txHash}`, `thread-mint`, `thread-state/{documentId}` and `document/{documentId}`, all anchoring-service paths.
  - `originate.openapi.ts` mentions `GET /api/anchors/{id}` only as an anchor-id resolver description.
  - No spec promises a synthesized 200.
- **Frontend:** `frontend/issuer/src/services/api.ts:535/543` uses `/anchoring/status/…` and `/anchoring/submit` only. Control: 365 tracked frontend files were searched.
- **Docs / deploy:** see Note 1. Two deploy files set the flag true. Both are configuration, not consumers of the 200.

## Q5. Red-first and controls are real: CONFIRMED, 4 red / 3 green
- With develop's `anchors.ts` (sha256 `eacfdfd0…`) under the head tests:
  - A1 red: `Expected: 404 Received: 200`.
  - A2 red: `Expected: 0 Received: 1`.
  - A3 red: the body carried `simulatedTxRef: "tx_sim_eb19…"`.
  - B2 red.
  - B1, C1 and C2 green.
- **My own mutation:** I restored the persist under the opt-in while keeping the 404 (`saveAnchorToDb({… tx_sim_ …})` before the return, file sha256 `206fced7…`).
  - **A2 red** (`Expected: 0 Received: 1`). A1 and the re-pinned ks520 cell also red.
  - A3 and B2 stay green, as expected: the response is unchanged.
  - Head restored, `2b83513a…`.

## Q6. Landing
- **merge-tree onto the live develop:** `git merge-tree --write-tree origin/develop origin/pr1617` gives `83c945a644b82d29f0727c38d28f328a80c4b34e`, rc 0. This equals the author's prediction. develop was re-read before the verdict and is unchanged.
- **Subtrees:** the originate subtree is `1086d5aa…` at both develop and the merge-base `80868551e`. It is `cbdc8240…` at both the head and the landing tree. `packages/shared` is identical across all four refs.
- **Build:** `npm run build --workspace=packages/shared` ran tsc clean. `npm run generate --workspace=services/originate` gave "generate: OK".
- **Originate suite on the landing tree (jest, full default config):** **1488 / 1488, 123 suites, 0 failed**, rc 0.
- **Parent** (develop originate, the ks1629 file ignored): **1481 / 1481, 122 suites**, rc 0. Delta +7 / +1, which matches the claim.
  - The integration config (`*.integration.test.ts`, which includes ks1612 and needs a DB) is excluded by `jest.config.js`. I did not run it.
- **tsc:**
  - Pass 1, the production `tsconfig.json`: rc 0, 0 errors. Tests are excluded; `anchors.ts` is in the program and the ks1629 file is not.
  - Pass 2, a scratch `tsconfig.ac1.json` extending it with `exclude: []`: rc 0. `anchors.ts`, ks1629 and ks520 are all in the program.
  - Positive control: a planted `const ac1Probe: number = 'not a number'` in the ks1629 file is reported by pass 2 and not by pass 1. File restored from copy.
- **Three-dot list** (`git diff --name-only origin/develop...origin/pr1617`): exactly 3 files, +239/−43:
  - `…/routes/anchors.ts`
  - `…/__tests__/ks520-anchor-fail-closed.test.ts`
  - `…/__tests__/ks1629-the-anchor-read-path-writes-nothing.test.ts`

## NOT RUN
- ESLint. The flat config ignored absolute paths ("outside of base path") and `cd` is barred, so the author's "1 pre-existing warning, 0 new" is unverified.
- The four platform suites and every schemathesis integration test (no Docker). The read of their fixtures is a reading, not a run.
- The originate DB-backed integration config (`npm run test:integration`; ks1612 / migration 051 through the routes).
- Box readings of `SIMULATE_ANCHORING` on demo and kintsugi (no ssh). Whether any non-demo bicep / Container Apps environment is live.
- The author's preflight hook, the open-PR overlap census (`gh` not used), and the closing-keyword guard claims.
- No deploy and no live check.
- The KS-1629 / KS-1603 comments listed as still owed by the author.

sha256: fd211d3c9d27325278f745ffa0cdd2afeb4de4793f2a860017fdf210448179fc
