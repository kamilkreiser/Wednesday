#1569 (KS-1509, head 1f5d868b69bab7e67389098984a5fc6a604bbbc6): GO WITH NOTE
#1571 (KS-1619 part 3, head fe69faba83a034b5ec4df905be8c9c8daa3e0355): GO WITH NOTE
sha256/16: 737405c903c0df50

## Security-shaped findings
None. Neither PR touches auth, tenancy, secrets, SQL or a trust boundary. #1571 narrows what a log line can carry (field names, never values). No tier-1 hand-off requested.

## FOUND
- No blocking finding on either PR. Both heads reproduced: #1569 1f5d868b69bab7e67389098984a5fc6a604bbbc6, #1571 fe69faba83a034b5ec4df905be8c9c8daa3e0355. Live develop re-read: 833984fc94acf6bc00ff8e5d6642fa768dd44e09.
- LOW (coverage gap, #1569): mutant `prior?.blockHeight || null` SURVIVES (14/14). A real prior height of 0 would be collapsed to null by the `||` form and no test notices; F3 only uses 4242. Product line services/originate/src/services/anchorStateSync.ts:193 is correct as written (`??`), so this is a test-strength note only. Suggest one cell: prior blockHeight 0 stays 0.
- LOW (coverage gap, #1571): mutant hard-coding the constructor name to 'Object' SURVIVES (9/9). No cell throws an instance of a non-Object class, so the `Object.getPrototypeOf(err)?.constructor?.name` arm is untested. Product line services/api-gateway/src/routes/verification.ts:1580 matches fail500.
- INFO (#1571): the header comment of __tests__/ks1543-document-types-catch-logs-the-error.test.ts (lines 1-6) still says the catch uses `String(err)`; stale after this PR. Author's "red-first 3/6" does not match the file: it has 9 cells and exactly the 3 new D1-D3 cells go red (3 failed / 6 passed / 9 total). Same three cells, count phrased differently.
- INFO (#1569, behaviour change to name): an anchor_failed document whose prior height was unknown now persists and echoes blockHeight null where it used to say 0 (api-gateway GET verify tier-1 `blockchain.blockHeight`, verification.ts:670/713/819; originate GET /documents blob). Every reader found tolerates this (see HOW 3).
- INFO (not this PR): fail500 and the new catch both log a thrown string and an Error.message verbatim, and a Proxy whose ownKeys traps would throw inside the describer (same in fail500, byte-identical). Pre-existing, ruled by Kam 2026-09-27 (KS-1346); not introduced here.
- ENV note: in my clone the shared package dist was the project's stale build, so tsc exits non-zero on develop tip for reasons unrelated to either PR (`@secuura/shared` lacks isProvisioningCapable / decideProvisionerRegistration), and 9 originate suites / 3 gateway files fail on develop tip itself. Before and after sets are IDENTICAL. I did not get a clean tsc 0 or the author's full-suite 1375 / 1170 totals; see NOT tested.

## TESTED (all at live develop 833984fc9)
1. Hunks: #1569 changes exactly anchorStateSync.ts (+3/-2 product lines in the markDocumentAnchorFailed blob; one comment rewrite) and the ks1333 test file; #1571 changes exactly routes/verification.ts (one comment line added, one log line replaced) and the ks1543 test file. Nothing else in either diff. Single commit each on 1197ab38a.
2. Red-first at live tip (PR test file overlaid on develop tip product): #1569 ks1333 = 2 failed (F1, F2) / 12 passed of 14. #1571 ks1543 = 3 failed (D1, D2, D3) / 6 passed of 9. Green on develop+PR merge: 14/14 and 9/9; also green on both PRs merged.
3. Readers of blockHeight (originate + consumers), what each does with null:
   - api-gateway/src/routes/verification.ts:670 `persistedBlockHeight = blob.blockHeight ?? null`: null stays null.
   - :704-707 `persistedBlockHeightIsHeight` = typeof number && integer && > 0: null and old 0 both false, so confidence/anchored/verified are unchanged. No arithmetic.
   - :713 `liveBlockHeight || persistedBlockHeight`: falsy-chain, null ok; :819 echoes it into the response (null, was 0).
   - originate/src/routes/verification.ts:446 and verificationV2.ts:150 `toBlockHeight(chain.blockNumber) ?? blob.blockHeight ?? 0`: null falls to 0, null-safe; and the heal helpers early-return the blob untouched for status anchor_failed (verification.ts:409, V2:133, V2:397), so the new null is never fed into them.
   - originate/src/services/anchorStateSync.ts:267/304/386/423 are writers using toBlockHeight (null-preserving, KS-1333); no reader of the blob height in this file.
   - originate/src/routes/documents.ts:923/955/988/1442/1464 are writers on other paths (the other KS-1509 sites, deliberately not in this PR); documentRepo.ts:65 types the field `number | null`.
   - Frontends: verifier ResultPage.tsx:497 `(blockHeight || blockNumber || 0).toLocaleString()` safe; issuer DocumentDetail.tsx:120 `|| ... || 0` safe; frontend/shared verify.ts:62 schema is already `nullable().optional()`. CredentialCard/CredentialDetailModal/vc types read the VC cardanoAnchor, a different source, not this blob.
   - No SQL or JSON-path read of blockchain.blockHeight anywhere in Blockchain/Dev; remaining hits outside Dev are docs only. No reader does arithmetic or comparison that breaks on null.
4. Describer string-compare: the expression after `error: ` in verification.ts is byte-identical to fail500's in routes/batch.ts:24-29 (262 chars each, equal sha256). Behavioural parity over 15 thrown values (null, undefined, number, string, bool, symbol, bigint, function, plain object, array, class instance, null-prototype, Error, TypeError, throwing getter): all same. Secret planted in a thrown object `{code, detail:'SECRET-VALUE-ks1619'}`: log carries only `thrown Object with fields [code, detail]`; D1 asserts the value is absent from every log call. N2/N5 (value-leaking mutants) are killed.
5. Mutants (owning suite): #1569 `?? 0` killed (2 red), `?? undefined` killed, `?? -1` killed, `= null` always killed (1 red, F3), `?? ""` killed (ts compile error), `|| null` SURVIVED, comment-only control passes 14/14. #1571 `String(err)` killed (3), JSON.stringify values killed, drop null guard killed, drop typeof suffix killed (2), Object.values killed, drop string branch killed, drop Error branch killed (2), constant constructor name SURVIVED, comment-only control passes 9/9.
6. Full suites + tsc before (develop tip) vs after (both PRs merged): originate jest 1274 passed / 19 failed (9 suites) -> 1278 passed / 19 failed (same 9 suites); api-gateway vitest 1157 passed / 9 failed (3 files) -> 1161 passed / 9 failed (same 3 files); tsc error lines identical before and after (originate 1, gateway 2, none in touched files). Net delta is +4 and +4 passing, zero new failures.
7. Merge prediction on live develop: develop moved 7 files since base 1197ab38a; none overlap either PR. #1569 alone merges clean, #1571 alone merges clean, #1569 then #1571 clean, #1571 then #1569 clean, and both orders produce the identical tree (6201edbd8). The two PRs share no file. Planted control (develop-side edit of the same blockHeight line, then merge #1569) conflicts in anchorStateSync.ts as expected, so the detector works.

## HOW
Own shared clone at /private/tmp/claude-501/e2-sonnet/repo (origin Secuura/Distributed_Secuura, fetched with the project's deploy-key sshCommand, PR heads via pull/N/head); node_modules and shared dist symlinked read-only from the project checkout. All loops in script files. Scripts and raw outputs in /private/tmp/claude-501/e2-sonnet/ (merges.sh, red.sh, red2.sh, mut.py, cmp.js, full.sh, out/). No git write in !CODING, no push, no GitHub/Linear writes, no Docker.

## NOT tested
- Clean-build tsc exit 0 and the author's totals (originate 1375, gateway 1170/1170): my environment reuses the project's stale shared dist, so 9 originate suites and 3 gateway files fail identically before and after. Only the delta (+4/+4, nothing new) is established.
- The other six KS-1509 sites (documents.ts and the verification heal paths) are out of this PR's scope and were not assessed.
- No live DB, no running gateway/originate stack, no end-to-end anchor failure against Cardano; behaviour is unit-level plus reader audit by reading.
- Pre-existing logging of verbatim thrown strings / Error.message not assessed as a finding.

## Severities
- #1569: no blocker. LOW anchorStateSync.ts:193 area test gap (0-height not pinned, `|| null` survives). INFO null-vs-0 response change (verification.ts:670/713/819).
- #1571: no blocker. LOW verification.ts:1580 constructor-name arm unpinned. INFO stale header comment ks1543 test lines 1-6.
WALL-CLOCK: 6
