# QA Gate 109 verdict (TIER 1): Secuura/Distributed_Secuura PR 1927 (KS-1868, nft-certificate blockchain-verifier.service.ts catches)

## BLUF
**GATE 109 (TIER 1) on PR 1927 at 8a3a24599dad: GO WITH NOTES. Nothing has to be fixed before merge.**

The tier-1 claim holds, and I measured it with the REAL verifier, the REAL `nft.routes` router on a real HTTP server, the REAL `recordClientMint` and the REAL winston logger. Only the Blockfrost client (a counting stand-in) and the db `query` (a stateful upsert recorder) were replaced. Runs were at base and at head, under both logger formats (NODE_ENV test and production).
- **Base, unreadable value** (revoked Proxy, or an Error whose `message` getter throws), at either site: `POST /api/nft/record` answers 500 and **stores nothing** (0 db writes). `/verify/transaction` answers 500.
- **Head, unreadable value:** the outcome equals what an ordinary Error gets at the same site, on every field:
  - `/record` answers 201 with `onChainVerified:false`;
  - `onChainStatus` is `pending` (init site) or `error` (lookup site);
  - exactly one row is inserted, status `pending`, `minted_at` null, with the caller's own tx hash;
  - `/verify/transaction` answers 200 with `verified:false`;
  - chain calls are the same.
- **Never verified.** Across 92 records (23 scenarios x base/head x 2 logger formats), no row is `minted` and no answer says `verified:true` or `onChainVerified:true`, except the positive control where the chain lookup actually resolved.
- **Judge:** mechanical, 114 checks, 0 fails. It fails (rc 1) on two planted tampers.

One residual gap: a hostile NON-string `message` (G108-F1 shape). The real winston logger throws while formatting it, so the outcome is base's (500, nothing stored), identical at base and head. It is not a regression and nothing is newly persisted (G109-F1, recommended follow-up).

## 1. Heads + diffstat (logs/head_start.log, head_end.log, fetch.log)
- PR head `8a3a24599dad7c9b9eb255dbba141ec1c21ff13f` at START (06:05:07Z) and END (06:15:18Z): identical.
- Develop was `829233f1a388` at both reads. PR 1926 ("nft ipfs providers' upload reports a constant reason") had already merged before my start; the brief expected `8f313815`.
- Single commit, parent `968f17070208`, author Kam Kreiser <kamil.kreiser@secuura.ai>, message "Refs KS-1868: ...", with no close words.
- Diff vs its merge-base (968f1707): exactly 4 files, +181/-1, as the READY mail claims. All modes are 100644: one M, three A.
  - `blockchain-verifier.service.ts` 15/1
  - `ks1868-blockchain-verifier-unreadable-throw.test.ts` 126/0
  - the flow fragment 21/0
  - the cheat fragment 19/0
- **Operator equality** (logs/held_vs_pr.log, evidence/o72_p2_held.diff): I applied the held O72-P2 diff (`git apply --cached` on 968f1707 in a temporary index). The service and test blobs it produces equal the PR's blobs: `c906310e` and `a4c2c93c`.
  - So the PR has no hand edit in its code. The fragments are the author's own.
  - Control: a corrupted copy of the diff gives a different test blob (`dbff44f1`).
- PR body NOT read (no Secuura gh auth on this host). I used the READY mail (evidence/r74_ready_for_gate_1927.txt).

## 2. The hunks
- **Site 1, `getClient` init catch (:65):** `error: err instanceof Error ? err.message : String(err)` becomes a `let reason` guard around the same expression, falling back to `'unreadable thrown value'`. The function still returns `null` ("verification disabled"), so `verifyTransaction` answers `{verified:false,status:'pending'}`.
- **Site 2, `verifyTransaction` lookup catch (:107):** insert-only. A probe `try` at the top reads three things:
  - `status_code`
  - `err instanceof Error ? err.message : String(err)`
  - `(err as Error).message`

  If any read throws, it logs `'Error verifying transaction', { error: 'unreadable thrown value' }` and returns `{ verified:false, status:'error', error:'unreadable thrown value' }`. The existing code below the probe is byte-unchanged.
- **Unchanged:** `verifyAsset`, the routes, `recordClientMint` and the route catches. Readable values take exactly the old path (confirmed by the ordinary/str/404 rows being identical base vs head).

## 3. Behaviour: real route, stateful recorder (scripts/g109_probe.test.ts, runprobe.sh, short.py, judge.py; logs/probe_{base,head}_{test,production}.jsonl, short.txt, judge*.log)

HOW:
- vitest 4.1.12 (lockfile version). Real `BlockchainVerifierService` singleton, reset per scenario (`api=null`). Real router on `http.createServer`.
- Real `recordClientMint` → real `dbSaveNFTCertificate`, with the `../db` `query` replaced by an upsert recorder (status = `$13`, minted_at = `$22`, tx hash = `$9`) and `isDbAvailable` returning true.
- REAL winston logger, wrapped call-through so that a throw from the logger propagates.
- Blockfrost `BlockFrostAPI` replaced by a class that counts constructions and `txs()` calls. It throws in the constructor (init site) or rejects `txs()` (lookup site).
- Base product = 968f1707's verifier file, which equals develop 829233f1's (same sha256). The PR touches no other product file.

Results (key cells; full table logs/short.txt; identical under NODE_ENV test and production):

| scenario | base `/record` | base rows | head `/record` | head rows | head `/verify/transaction` | txs calls |
|---|---|---|---|---|---|---|
| none (chain resolves) — positive control | 201 v=true confirmed | minted | same | minted | 200 verified:true | 1 |
| unconfigured key | 201 v=false pending | pending | same | pending | 200 pending | 0 |
| init: ordinary Error | 201 v=false pending | pending | same | pending | 200 pending | 0 |
| init: revoked Proxy | **500** | **none** | 201 v=false pending | pending | 200 pending | 0 |
| init: message getter throws | **500** | **none** | 201 v=false pending | pending | 200 pending | 0 |
| lookup: ordinary Error | 201 v=false error | pending | same | pending | 200 error "upstream 500" | 1 |
| lookup: revoked Proxy | **500** | **none** | 201 v=false error | pending | 200 error "unreadable thrown value" | 1 |
| lookup: message getter throws | **500** | **none** | 201 v=false error | pending | 200 error "unreadable thrown value" | 1 |
| lookup: 404 | 201 v=false not_found | pending | same | pending | 200 not_found | 1 |
| lookup: plain string | 201 v=false error | pending | same | pending | 200 "Unknown error" | 1 |

- **Mechanical judge** (judge.py): 114 checks, 0 fails, rc 0.
  - For each site and logger format, head-revoked == head-getterThrows == head-ordinary == base-ordinary on every field: direct result (minus the error text), `/record` status and body, persisted rows, db op list, chain counters, and `/verify` status and body (the error TEXT is masked).
  - base-unreadable = 500 + 0 rows + 0 db ops + verify 500, confirmed.
  - No record in any of the 92 is minted or verified without a resolved chain lookup.
  - Positive control: the `none` scenario IS minted, so the judge can see a minted row.
- **Planted controls:**
  - a head lookup:revoked row tampered to minted gives rc 1 with 2 fails (equality, and VERIFIED without chain);
  - a head init:getterThrows status tampered to 500 gives rc 1 (logs/judge_tamper_*.log).
- **Extra shapes, measured beyond the committed cells:**
  - a thrown null-prototype object (`String(err)` throws);
  - a non-Error with a throwing `message` getter.

  At base, both are 500 with nothing stored. At head both get the ordinary outcome (init pending, lookup error, one pending row). This coverage comes from probe reads 2 and 3 (see G109-F2).
- **The persisted row's meaning:** for an unreadable value the head now stores a `pending` record carrying a caller-supplied tx hash that was NOT verified on chain. That is exactly what an ordinary Blockfrost error, a 404 or an unconfigured key already store. The route has always been "store even if verification is pending".
- **Logs at head for unreadable values:** only the constant, `warn ... {error="unreadable thrown value"}` and `error 'Error verifying transaction' {error="unreadable thrown value"}`.

## 4. The hostile non-string message (G108-F1 / G105-F1 shape) at head
These are Errors whose `message` getter succeeds but returns a hostile value:
- **revoked Proxy (msgRevoked):**
  - Init: the guard assigns the proxy to `reason` (typed `string`, not coerced). winston then throws `TypeError: Cannot perform 'get' on a proxy that has been revoked` while formatting the meta (both the dev format and the production json format). That throw escapes `getClient`, so verifyTransaction rejects.
  - Lookup: the probe passes (no read throws), and the unchanged `logger.error(... err.message)` below it throws the same way.
  - Result at head = base, identical: `/record` 500, 0 rows; `/verify` 500. **Nothing newly persisted, no regression.**
- **toString throws / Symbol / null-proto object (msgToStrThrows, msgSymbol, msgNullProto):** no throw anywhere. `/record` gives 201 pending, identical at base and head (these already persisted at base). `/verify/transaction` echoes `error: {}`, or omits it for a Symbol, also identical at base.

So the guard does not coerce. The fix is a follow-up, not fix-before-merge (G109-F1).

## 5. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Install:** `npm ci --ignore-scripts` succeeded at head (lockfile vitest 4.1.12), followed by `npm install --no-package-lock`. `packages/shared` was built and symlinked as `@secuura/shared`.
- **Red-first** (logs/red_base.json, green_head.json): with the head test file at base product, C1–C3 pass, and **R1–R4 fail, all by assertion** (`expected { rejected: true } to deeply equal { resolved: ... }`). At head 7/7 pass. This matches the author's 4 of 7.
- **Mutants** (scripts/mutants.py, logs/mutants.log; product only, test untouched, sha256-restored after each, RESTORE_OK `07873121421d`, `git status` clean):

  | mutant | red cells |
  |---|---|
  | site1 undo guard | R1, R2 |
  | site1 constant reason `'x'` | C1, R1, R2 |
  | site1 catch rethrows | R1, R2 |
  | site2 probe removed | R3, R4 |
  | site2 probe answers verified:**true** | R3, R4 |
  | site2 probe answers status pending | R3, R4 |
  | site2 drop both message reads (keep status_code) | R4 |
  | site2 probe rethrows | R3, R4 |

  8/8 killed. Each is local: site-1 mutants touch only init cells, site-2 mutants only lookup cells.
  - **Single-line probe mutants** (logs/mutants_extra.log): deleting any ONE of the three probe reads SURVIVES the committed cells. The two committed shapes each throw on more than one read. See G109-F2.
- **Whole nft-certificate suite** (logs/suite_base.json, suite_head.json; lockfile vitest 4.1.12):
  - base (968f1707 verifier, new test absent): 25 files, 162 tests, 162 pass, 0 fail;
  - head: 26 files, **169 tests, 169 pass, 0 fail**.
  - This matches the author exactly. It also shows that G108-F5's single `db.retry` failure was an artefact of vitest 1.6.1.
- **tsc:**
  - the plain config gives rc 0;
  - with tests (scripts/tsconfig.tests.json, 26 test files in the program including the new one) it gives rc 0 with **0 errors**;
  - a planted test file gives rc 2 with TS2322 and TS6133 (logs/tsc_planted.log).
- **eslint** (scripts/eslint_run.cjs = ESLint API with cwd = Blockchain/Dev, since the flat config is cwd-relative; eslint from gate 107's node_modules via symlink): on the 2 changed .ts files, rc 0 with 0 errors and 1 warning (`'e' is defined but never used`, test :53). A planted file gives rc 1 with `no-debugger` and an unused var (logs/eslint_planted.log).
- **docs-fragments check** (scripts/frag.sh, logs/frag_run.log, frag_check_*.log):
  - Clean run: rc 0, "flow 117 legacy + 78 new, cheat 112 legacy + 78 new; lint clean, render passes".
  - Planted defects all give rc 1: flow unclosed `<div>`; flow `<!--n-->.` removed; cheat unclosed `<div>`; cheat `</table>` corrupted.
  - All restored by sha; rc 0 after.
  - One ADVISORY line (cheat :6235) is develop's own, as in G90-F7 and G108.
- The pre-push hook (13/16 legs, PREFLIGHT INCOMPLETE) and CI are the author's; not re-run.

## 6. merge-tree (logs/mergetree.log, mt_paths.log, pr_paths.log, dev_paths.log)
- Develop re-read at the end: `829233f1a388` (fetched again). `git merge-tree --write-tree 829233f1 pr1927` gives rc 0, tree `308d2595`.
- The result vs develop changes exactly the PR's 4 paths (SAME_PATHS), 4 files +181/-1.
- Paths shared between the PR and develop's 17 paths past the base: **0** (control: develop against itself = 17). The merged verifier file is identical to the PR's.
- Develop's move is ipfs.service.ts plus originate routes plus fragments. None of it touches the verifier, the route or the minting service.
- The probe was not re-run on the merged tree; this is read, not run.

## 7. Kam's ks1346 logging rule
- The two new log calls carry only the constant `'unreadable thrown value'` under the field name `error`. No thrown value reaches a new log line or a response in the unreadable case.
- Pre-existing lines are unchanged and are not this PR's: site 1 for readable values, and site 2 below the probe, still log the readable `message` value, and the route catches do the same.

## 8. FINDINGS
- **G109-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured).** The hostile non-string `message` shape is not coerced.
  - At init, `reason` holds whatever the getter returned (typed `string`).
  - At lookup, the probe reads `.message` but does not stringify it.
  - With a getter that returns a revoked Proxy, the REAL winston logger throws while formatting (dev and production formats). Outcome at head = base: `/record` 500, 0 rows; `/verify` 500.
  - The other hostile shapes (toString throws, Symbol, null-proto) already reach 201 pending at base and at head, identically.
  - Not a regression; nothing newly persisted.
  - Suggested follow-up, PR 1924's form:
    - init: `reason = String(err instanceof Error ? err.message : err)` inside the same try;
    - lookup: add `void String((err as Error).message)` to the probe (this routes that shape to the constant answer — note this WOULD newly persist a pending row for it, the same tier-1 class as this PR);
    - plus a cell for each.
  - The author's recorder stubbed the logger, which is why this shape looked handled there. The fragments do not claim it.
- **G109-F2 (RECOMMENDED; measured).** The committed cells pin only the two shapes that throw on several reads. Each of the three probe reads survives deletion on its own.
  - Reads 2 and 3 are the only coverage for a thrown null-prototype object (`String(err)` throws) and for a non-Error whose `message` getter throws.
  - My probe shows both get the ordinary outcome at head (500 with nothing stored at base).
  - Suggest two more cells (nullProto, plain-object getter) so those reads are pinned.
- **G109-F3 (INFO; measured).** No committed cell asserts the ROUTE answer or the persisted row. The tier-1 change is pinned at function level only (as G90-F2). The gate measured it at route level (Check 3).
- **G109-F4 (INFO, doc accuracy).** The fragments say the routes were not exercised over HTTP ("handlers called directly", "the routes over HTTP" not measured) and that the logger was stubbed.
  - This gate ran the real router over HTTP with the real winston logger, in both formats. It confirms the fragments' tier-1 statements and the 162 -> 169 / 0 failed figures.
  - The fragments' "14 records / 9 checks" is the author's own recorder. Mine is 92 records / 114 checks.
- **G109-F5 (INFO).** eslint warning: unused `e` at test :53 (the `answer` helper's `catch (e)`). Optional: `catch {`.
- **G109-F6 (INFO, pre-existing, unchanged).** For a non-string `message`, `/verify/transaction` echoes `error: {}` or omits `error`. A plain-string throw yields "Unknown error". Same at base.
- **G109-F7 (INFO).** Develop had already moved to `829233f1` (PR 1926 merged) by my start, not `8f313815`. The merge-tree onto it is clean with 0 shared paths.
- **No FIX-BEFORE-MERGE item.**

## 9. UNMEASURED / NOT TESTED
- The live PR body, the Linear ticket, CI, the pre-push legs, and Node 24.
- A real Blockfrost client, a real Postgres (the db `query` was a recorder; SQL was not executed), and a real service boot. The router was mounted on bare express, so app middleware and auth were not exercised.
- The probe on the merge-tree result (read only; 0 shared paths).
- Whether Blockfrost or `new BlockFrostAPI` can ever throw any of these values in reality (all values are synthetic).
- The chain counter's positive control is the `none` scenario (txs=1, resolved=1). The init constructor counter is recorded but not judged.
- The author's own recorder and judge (not in evidence; I built my own).
- Mutant forms beyond the 8 + 3 listed.
