# QA Gate 84 verdict: Secuura/Distributed_Secuura PR 1899 (KS-1868, nft-certificate minting.service.ts, four catch sites O45), tier 2

## BLUF
**GO WITH NOTES. Tier recommendation: keep tier 2, no Opus re-gate.** The four product hunks are the same guard, byte-for-byte in shape (+7/-1 each, +28/-4 in the file). For any readable thrown value nothing changes. For an unreadable thrown value the PR adds NO new path: I ran the callers at base and at head (logs/probe_base.jsonl, logs/probe_head.jsonl) and at head an unreadable value now behaves exactly as an ordinary `Error('db down')` already does at base, at all four sites and every caller. The mint-path trace the brief asks about (Q1) is confirmed with one correction: at base the failure was worse than "MINT_FAILED although minted", see G84-F3. Red-first 8 of 12 by assertion, green 12 of 12, suite 137 to 149, tsc rc 0. Notes are two test gaps (G84-F1 rethrow-only-unreadable survives at all four sites; G84-F2 readable non-Error branch) and out-of-scope unguarded reads that remain in the same mint path (G84-F4).

## Heads
- START (logs/head_start.log, 2026-11-01T13:25:10Z): PR head `bc05f5bf1f5abccfc4ce16acd3c6f5544baf8af4` (matches expected), develop `ca36945e974081be6abbc15e548f4f8d02767e14` (matches). Merge-base = parent = `d7691f35312ea158f043e87a3227e477cccb183d`.
- END (logs/head_end.log, 13:44:23Z): ls-remote `refs/pull/1899/head` = `bc05f5bf...`, develop = `ca36945e...`, local HEAD `bc05f5bf...`. Nothing moved. Working tree clean. Product sha256 `56e1e777f123...` at start and end (logs/product_sha.log, logs/head_end.log).
- Diffstat (logs/diffstat.log): 7 files, +360/-4: minting.service.ts, four test files (81+71+71+71), two fragments (19 each).
- Product on develop `ca36945e` is byte-identical to the product at the PR's parent `d7691f35` (logs/runs_outer.log line 2), so "base" below is the same for both.

## FINDINGS
- **G84-F1 (LOW, test gap, the author's own flag, now measured)** Mutant M4 "rethrow only for an unreadable value, after logging" SURVIVES at all four sites (12 of 12 pass; logs/mut_*__M4_rethrow_only_unreadable.log). R1/R2 use `await call().catch(() => undefined)`, so a rethrow on the unreadable path is invisible, and C1 only exercises the ordinary-Error path. M3 (rethrow for every value) is KILLED at all four sites, but only by C1. So the "resolves" in every R title is not pinned for the one case the PR is about. Not a product defect: the product does resolve (probe, section 1).
- **G84-F2 (LOW, test gap)** M6 (non-Error branch replaced with constant `'x'`) SURVIVES at all four sites. No cell throws a readable non-Error (string, plain object). The branch is unchanged by the PR. Same gap as G74-F1, G76-F1, G78-F1.
- **G84-F3 (INFO, the behaviour change, measured)** See Q1. Before, an unreadable value at the post-mint save made the client see `MINT_FAILED` (HTTP 400) with an internal engine message and wrote `failed` to the DB for an NFT that was minted. After, the client sees success and the DB keeps the previous status `minting`. The after-state equals the ordinary-Error state at base. Not new.
- **G84-F4 (INFO, out of scope, same file, mint path)** Unguarded `instanceof Error ? ... : String(x)` reads remain (grep, logs/src_excerpts2.log): `minting.service.ts:177` (getCertificationData catch, returns null), `:688` (getWalletNFTCertificates; the author names KS 1843), `:798` (mintOnCardano, "Real minting failed", before `throw err`), and `utils/mintError.ts:36` (`classifyMintError`, called at `:380` inside mintNFT's catch). An unreadable value thrown by the chain step itself would still throw out of `classifyMintError`, so mintNFT would reject and the route would answer 500 (`nft.routes.ts:109-114`). I did not run that. The routes' own catches (`nft.routes.ts` lines for mint, record, list, get) also read the error unguarded. The ticket stays open, which the fragment says.
- **G84-F5 (INFO)** tsc: plain `tsc -p tsconfig.json --noEmit` rc 0 (logs/tsc_plain_head.log). With `__tests__` in the program (my config, scripts/tsconfig.tests.json, which keeps the package's `noUnusedLocals`) rc 2 with 3 errors, all `ipfs.service.ts(65|176|255)` TS2322 Buffer/BlobPart, unrelated to this PR. The same 3 appear with the four new tests excluded (logs/tsc_tests_excl_new_head.log), so the new tests add none and no unused import is left.
- **G84-F6 (INFO)** eslint (`npm run lint`, logs/eslint_pkg.log): 0 errors, 1 warning, `cardano/index.ts:134` preserve-caught-error, a file the PR does not touch. Zero lines name `minting.service` or `ks1868-nft-` (positive control: the output contains the package path twice).
- **G84-F7 (INFO)** docs-fragments `check` prints the same 2 ADVISORY lines (flow, cheat committed page lags render) seen in gates 76 and 78. Not attributable to this PR.
- **G84-F8 (INFO, wording)** Test header comments read "must still log its line and resolves ..." (grammar). The dbSave file's C1 title says "resolves the saved record", but the assertion is on `recordClientMint`'s return, not on `dbSaveNFTCertificate` (which returns void). Harmless.

No HIGH or MEDIUM findings. Every number the author gave that I re-measured matched.

## Q1. Behaviour change on the mint path (in full)
Method: source read at head `bc05f5bf` (logs/callers.log, logs/src_excerpts.log, logs/src_excerpts2.log), then a probe test (scripts/probe.test.ts, copied into my clone for the run and moved out; NOT part of the PR) run against the base product and the head product (logs/probe_base_vitest.log and logs/probe_head_vitest.log, 15 of 15 cells each). The DB stand-in rejects with (a) `new Error('db down')`, (b) a revoked Proxy, (c) an Error with a throwing `message` getter. Positive controls: the probe records the DB statuses saved and the logs, and the "ordinary" rows show the expected "DB save certificate failed {error: db down}" line.

Structure of the helper (head `:40-100`): `dbSaveNFTCertificate` first does `memNftCertificates.set(cert.id, cert)`, returns if the DB is down, then `await query(...)` in a try. The catch only logs. So the in-memory record is always set, whatever the DB does. `nftRecord` in mintNFT is the same object that the map holds, so later mutations are visible through memory.

### Site 1, dbSaveNFTCertificate; callers `git grep -w` (logs/callers.log, head line numbers)
- `:246` initial PENDING save, `:302` after the Premium-tier IPFS step, `:362` the save AFTER `mintOnCardano`/`mintOnEVM` returned (status MINTED), `:388` inside mintNFT's catch (writes FAILED), `:438` `recordClientMint`, `:731` `updateStatus` (PROCESSING, UPLOADING_IPFS, MINTING). All are `await`ed. `:246`, `:302`, `:362`, `:731` are inside mintNFT's try; `:388` is in the catch; `:438` has no catch and `POST /record` (`nft.routes.ts:148`) wraps it in a try that answers 500.
- **Mint post-mint save (`:362`), measured:**

| DB error kind | base: client | base: DB statuses saved | head: client | head: DB statuses saved |
|---|---|---|---|---|
| ordinary Error | success, txHash present | pending, processing, minting | success | pending, processing, minting |
| revoked Proxy | `success:false`, `MINT_FAILED`, error "Cannot perform 'getPrototypeOf' on a proxy that has been revoked" | pending, processing, minting, **failed** | success | pending, processing, minting |
| throwing getter | `success:false`, `MINT_FAILED`, error "getter boom" | pending, processing, minting, **failed** | success | pending, processing, minting |

  Confirmed: before, the helper's catch threw (the read itself throws a fresh TypeError/Error), the throw landed in mintNFT's catch at `:363`, `classifyMintError` produced `MINT_FAILED`, and `:388` then wrote FAILED. The route maps `MINT_FAILED` to HTTP 400 (`mintFailureHttpStatus`, `utils/mintError.ts`). The NFT had already been minted on chain at that point (`:362` runs after the mint returned). **Correction to the brief:** it was not only "the client got MINT_FAILED"; the failure path also overwrote the in-memory record with FAILED (the probe could not read the id back because the failure response carries no `nftCertificateId`), wrote `failed` to the DB when the DB was reachable again, and echoed an internal engine message to the client.
  After: the save logs the constant and resolves; the client gets 201 with the txHash; memory says `minted`; the DB keeps `minting` because the single failed write was the MINTED one. That is a client success with an unsaved final DB state.
- **Is that a new data-integrity risk beyond an ordinary Error at base? No.** The ordinary-Error row at base is identical to the head rows for the unreadable kinds (same client result, same DB statuses, same memory). The PR makes the unreadable case follow the existing path, and in the process removes the worse path (a minted NFT recorded as FAILED, with an engine message shown to the client). The residual (success to the client, DB stale at `minting`) is a pre-existing property of "log and carry on" in this helper (design question, out of scope).
- **Earlier saves (`:246`, `:302`, `updateStatus :731`):** at base an unreadable error there aborted the mint BEFORE the on-chain step (fail closed); at head the mint proceeds. An ordinary Error already proceeds at base (the helper swallows it). I did not probe these three; it follows from the same code (the helper is the only thing that changed). Not a new path for the same reason.
- **`recordClientMint` (`:438`, `POST /record`), measured:** base unreadable: rejects, so the route answers 500 although the client already minted in the browser. Head: resolves with `status: minted`, route 201, DB row not saved. Ordinary Error at base: resolves (same as head).

### Site 2, loadFromDb
Only caller: `server.ts:42`, passed to `initDb(loadFromDb)` as the onReady hook (`db.ts`). `runDbReadyHook` (`db.ts` ~`:81-88`) wraps it in a try/catch that logs `err?.message`, and the retry timer path calls it too. Measured: base unreadable: rejects with a readable TypeError (so `runDbReadyHook` logged "DB ready boot work failed"); head: resolves after logging "Failed to load NFT certificates from DB — starting empty". Ordinary Error at base: resolves. Same end state (empty cache). Not new. Side observation, not a finding: `runDbReadyHook` reads `err?.message` unguarded, but it receives the helper's fresh readable error at base, and at head receives nothing.

### Site 3, getNFTCertificate
Only caller: `GET /certificates/:id` (`nft.routes.ts:276`), 404 on null, 500 on a rejection. Measured: base unreadable: rejects (so 500); head: `null` (so 404, a certificate that may exist in the DB reported "not found"). Ordinary Error at base: `null`, so 404. Same as ordinary; the 404-on-DB-error semantics is pre-existing.

### Site 4, getUserNFTCertificates
Only caller: `GET /certificates` (`nft.routes.ts:242`), and the route then filters with `selectReadableCertificates(fetched, ownerId, ...)` (KS 1836). Measured: base unreadable: rejects (500); head: returns the memory-only list (count grew across cells because my cells share the map). Ordinary Error at base: same memory-only list. The owner filter still applies to what is returned, so no widening of what a caller can read. (`getWalletNFTCertificates`, the neighbour at `:688`, is KS 1843 and untouched.)

### Does the PR add any NEW path? No.
Every changed behaviour is "an unreadable value now takes the path that an ordinary `Error` takes at base". No caller gained a way to proceed that it lacked. **Tier 1 not recommended.** Open limitation of the evidence: the probe stands in for `query`, so a real pg driver is not involved, and a pg driver does not in practice reject with a revoked Proxy; the unreadable value is a defensive hypothetical (the Spark reviewer noted this too).

## Q2. Product hunks (logs/q2_hunks.log, scripts/q2.py)
Exactly four hunks, each 1 line removed and 7 added. For each: the removed line is `logger.<level>('<msg>', { error: <EXPR> });` and the added lines are exactly `let reason: string; try { reason = <EXPR>; } catch { reason = 'unreadable thrown value'; } logger.<level>('<msg>', { error: reason });` (script asserts equality after trim; all 4 `True`). `<EXPR>` is identical in all four (`err instanceof Error ? err.message : String(err)`). Unchanged: log text (`DB save certificate failed`, `Failed to load NFT certificates from DB — starting empty`, `DB get certificate failed`, `DB get user certificates failed`), level (error, warn, error, error), key `error`, return type, nothing rethrown. `git diff --shortstat`: +28/-4. Nothing else touched in the file.

## Q3. Hand edit (logs/handedit.log, scripts/handedit.py)
I rebuilt Spark's original test files from the four READY diffs (`local-model/night/READY_KS-1868-KS-1868-O45-P1..P4`) and diffed them against the PR head. Result: per file exactly one line, the import from `../services/minting.service`: P1 loadFromDb file `{ nftMintingService, loadFromDb }` to `{ loadFromDb }`; the other three `{ nftMintingService, loadFromDb }` to `{ nftMintingService }`. 4 files, +4/-4, nothing else. (My script printed `+8` because of a trailing-newline artefact of my own parser, shown as a blank `+` line per file; the real count is +4/-4.) tsc with `noUnusedLocals` over the tests reports nothing in them (G84-F5).

## Q4. Re-measure
- Head, four new files (logs/head_new_tests.log): `Test Files 4 passed`, `Tests 12 passed`, rc 0.
- Base product (the parent's file, sha256 `b99e9e5a...`) + new tests (logs/red_base_new_tests.log): `Test Files 4 failed`, `Tests 8 failed | 4 passed (12)`, rc 1. All 8 failures are R1 and R2 of each file, `AssertionError: expected [] to have a length of 1 but got +0`, assertion failures, not compile or import errors. The 4 controls pass. Matches 8/12.
- Whole suite: base product with new tests excluded: 18 files, 137 of 137 (logs/base_whole_excl_new.log); head: 22 files, 149 of 149 (logs/after_whole.log). Matches. Restore verified `RESTORE_OK` (logs/runs_outer.log). Setup: `npm ci --ignore-scripts` rc 0, shared build rc 0 (logs/npm_ci.log, logs/shared_build.log). vitest `nice 10`, `--maxWorkers=2`; load was above 8 at times, my gate waited up to 200 s then ran anyway (`load1 at start: 8` or `7` in each log).
- tsc, eslint: G84-F5, G84-F6.
- Fragment pair: `docs-fragments.mjs check --root` on head rc 0, "flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes" (logs/frag_check_clean.log). Planted defects, each restored (all four `restore OK`): unbalanced `<div>` in flow rc 1 ("<div> opened 2, closed 1"), in cheat rc 1 ("opened 4, closed 3"); flow `<!--n-->.` removed rc 1 ("the <h2> must start with <!--n-->."); cheat `</table>` corrupted rc 1 ("<table> opened 3, closed 0"). After restore rc 0 (logs/frag_check_after_restore.log). The fragment text matches what I measured (four sites, +28/-4, line numbers 90/129/504/584 at base, 12 tests, 137 to 149).

## Q5. Mutants (scripts/mutants.py; each applied to ONE site in the product file only, tests untouched; sha256 restored and checked after every run; table in logs/mutants_table.log, per-run logs/mut_<site>__<mutant>.log)
48 runs (12 mutants x 4 sites, the 4 new test files per run): **40 killed, 8 survived**.

| Mutant | dbSave | loadFromDb | getNFT | getUser |
|---|---|---|---|---|
| M1 drop the inner try/catch | KILLED | KILLED | KILLED | KILLED |
| M2 catch fallback `String(err)` instead of the constant | KILLED | KILLED | KILLED | KILLED |
| M3 rethrow after logging, every value | KILLED (C1 only) | KILLED (C1 only) | KILLED (C1 only) | KILLED (C1 only) |
| **M4 rethrow after logging, only when unreadable** | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** |
| M5 log the constant for ALL values | KILLED (C1) | KILLED (C1) | KILLED (C1) | KILLED (C1) |
| **M6 readable non-Error branch to constant `'x'`** | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** |
| M7 message dropped, `String(err)` for all | KILLED | KILLED | KILLED | KILLED |
| M8 constant text changed | KILLED | KILLED | KILLED | KILLED |
| M9 log key renamed | KILLED | KILLED | KILLED | KILLED |
| M10 log call removed | KILLED | KILLED | KILLED | KILLED |
| M11 log level swapped | KILLED | KILLED | KILLED | KILLED |
| M12 unguarded `(err as any).message` in the fallback | KILLED | KILLED | KILLED | KILLED |

Answers to the brief: a rethrow of ALL values is caught (by C1, which has no `.catch`); a rethrow limited to the unreadable path is NOT caught at any site (G84-F1, a test-gap finding); logging the constant for all values IS caught by C1 (it asserts `{ error: 'db down' }`), so losing the readable message is guarded.

## Q6. merge-tree (logs/merge_tree.log, scripts/mt.sh)
`git merge-tree --write-tree refs/gate/develop refs/gate/pr1899` (develop `ca36945e`): **rc 0**, tree `2f3b2b77e396ae839d499fd6c97ae97494fca083`, no conflicts. Since `d7691f35` develop gained 3 commits and 17 changed files (logs/develop_since_d7691f35_log.log: `8126b22b` persona switch handler, `ad78fa10` governance DB read catches, `ca36945e` KS-1885 social sign-in callback), and none of them is a path the PR touches (logs/overlap.log empty, preceded by a populated 17-line file list as positive control). KS 1843 was not among them.

## Spark shadow calibration
Files: evidence/spark_shadow/ (`attempt1_*`, `attempt2/`, `review/`, logs/spark_gate.log, logs/spark_gate2.log, logs/spark_review.log).
- **Attempt 1 failed as data, not as a verdict:** I passed the package-local `services/nft-certificate/node_modules` to `--node-modules`; it holds no vitest (`Cannot find module 'vitest/config'`, 0 passed on head and base, evidence/spark_shadow/attempt1_pkg_node_modules/targeted_head.log). For this workspace layout the argument must be the hoisted `Blockchain/Dev/node_modules`. Worth a line in the spark_gate.sh header. Attempt 2 with that directory worked.
- **Deterministic half (attempt 2):** head 4 files ok, 12 passed 0 failed; base product 4 passed, 8 failed; diff 7 files +360/-4; 31 s. All three agree exactly with my own measurements (12/12, 4/8 of 12, +360/-4).
- **Spark review (`review.json`, SPARK_THINK=0, 1 attempt, 52 s): GO WITH NOTES, 7 Notes, no Major.** Agrees with my verdict. Matches mine: the red cells assert only the log line, so "resolves" is unpinned (my G84-F1, but Spark did not run mutants, so it could not say the rethrow-only mutant survives); the 404-vs-500 claim is read from source (I measured it); the real thrown value is a stand-in (my Q1 limitation). Partial/off: "changes only 4 of 253 sites" (true, in the fragment, not a defect); the two Notes about the logger throwing on hostile values and the production logger path have `evidence_quote_found_in_input: false`, i.e. speculative, I did not verify them. **Missed:** the mint-path behaviour change (the key question, and the worst before-state: minted NFT recorded FAILED), the surviving M4 and M6 mutants, the remaining unguarded reads in the mint path (G84-F4). Takeaway: Spark is reliable on the deterministic numbers and a usable first pass on test-pins-what-it-says; it does not trace callers across files, so Q1-class questions need the human-directed trace.

## Notes for the PR body
- State the real before/after for the mint path: before, an unreadable DB error at the post-mint save made the client see `MINT_FAILED` (400, with an engine message) and recorded FAILED for a minted NFT; after, it logs and the client sees success (201), the DB keeps the last good status, same as an ordinary Error today.
- Say plainly that the R cells do not pin "resolves" (use `await expect(call()).resolves...` in R1/R2, or the titles should say "logs a constant reason"); a rethrow limited to the unreadable path survives all four sites.
- Optionally add a readable non-Error throw (a string) to C1 to kill M6.
- Remaining unguarded reads on the same path (`:177`, `:798`, `classifyMintError`, route catches) are not covered; the ticket stays open as the fragment says.

## NOT TESTED
- A real pg driver or database, a booted service, or a real route request. The probe calls the service methods directly with a stand-in `query`; route statuses (201, 400, 404, 500) are read from `nft.routes.ts`, not requested.
- The earlier saves (`:246`, `:302`, `updateStatus`) with an unreadable error (inferred, not probed).
- An unreadable value thrown by the chain or IPFS step itself (`classifyMintError`, G84-F4), and `logger` itself throwing.
- Premium-tier / IPFS path, EVM chains, Node versions other than the local one, the four platform suites, the pre-push hook legs, CI, any deploy or merge.
- The ticket text (the Spark review ran without Linear text).
