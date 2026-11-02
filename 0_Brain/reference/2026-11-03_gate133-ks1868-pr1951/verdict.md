# QA Gate 133 verdict: Secuura/Distributed_Secuura PR 1951 (KS-1868, nft-certificate ipfs.service.ts x3 + blockchain-verifier.service.ts x2, held Spark passes O80-G1/G2), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Both behaviour changes the author flagged pass the test the brief set. I ran the real `nft.routes` router, the real minting service, the real IPFS providers, the real verifier and the **real winston logger**, in both `NODE_ENV=production` (json format) and `development` (printf format). Only `../db` (a recording table), `@blockfrost/blockfrost-js`, global `fetch` and `../cardano` were stubbed. 160 cells ran at base and 160 at head (logs/probe_{base,head}.jsonl, logs/probe_outcomes.log).
- **(1) POST /record:** a message getter that returns a revoked Proxy gets **500 with nothing stored at base** and **201 with one `pending` row stored at head**. An **ordinary Error at the same point already gets 201 with the same `pending` row at base and at head**. So head moves the unreadable value onto the ordinary path and adds no new outcome. The stored row has `status='pending'`, `minted_at=null` and `error_message=null`, and no verified column is persisted. Nothing in the repo reads `pending` as verified (§3.3).
- **(2) mintNFT:** an ordinary Error from the upload already gets **503 MINT_DEPENDENCY_UNAVAILABLE at base**. Head changes only the hostile-getter kinds, which went 400 MINT_FAILED -> 503. The ordinary-Error answer is unchanged at every changed site. That 400->503 move is **not reachable from any route**: `POST /mint` passes `documentData: undefined`, so the upload branch never runs. The probe shows 0 IPFS calls from the route.
- Across all 160 cells, every base->head outcome difference is a hostile-getter kind (getter returning a revoked Proxy, a toString that throws, a null-prototype object or a Symbol). The ordinary Error, the thrown string, the thrown revoked Proxy and the throwing getter are byte-identical at base and head on every site, in both envs. Real winston **threw synchronously** at base in 10 cells (getterRevokedProxy x 5 sites x 2 envs) and in 0 cells at head. Unhandled/uncaught = 0 everywhere.
- Held-pass identity: the product hunks and both test files equal O80-G1/G2 line for line (§1). Red-first: 15/22, all by AssertionError. Green: 22/22. Suite: 178/178 (27 files) -> 200/200 (29 files). Merge-tree onto develop `73342c2f` is clean and changes exactly the 6 PR paths. Mutants: 15 of 19 killed. The 4 survivors are 3 sites with no Symbol cell and 1 redundant line (G133-F4).
- Notes: G133-F3 (recommended) covers the verifier lookup, which still reads `err.message` up to 4 times, so a non-idempotent getter can still escape. Head is strictly better than base there. Also G133-F5..F7.

## 1. Heads + diffstat
- START (logs/head_start.log, 2026-11-02T14:14:17Z): `refs/pull/1951/head` = `6db96b6fe07aa64e44d09ac9b8034488fb07063f` (matches the brief and the READY mail). Its parent and merge-base is `1584c0f0ff808fddf35245bee41b6b5f9231054c` (matches). It is one commit. develop = `73342c2f8f490c2af76fb5dfb3cb02c6aed851c2` (matches the brief).
- END (logs/head_end.log, 14:25:33Z): the PR head and develop are unchanged. Local HEAD is `6db96b6f`. Product sha256 is ipfs `27e14964...` and verifier `9b03dead...` (= head blobs), and the working tree is clean.
- Diffstat (logs/diffstat.log): **6 files, +347/-6**, exactly as claimed. ipfs.service.ts +3/-3, blockchain-verifier.service.ts +3/-3, two new tests (+141, +159), two fragments (+19, +22). Nothing else.
- Held passes (logs/held_identity.log, scripts/held_identity.py): O80-G1 = ipfs.service.ts (24 diff lines) + the ipfs test (141), and O80-G2 = blockchain-verifier.service.ts (18) + the verifier test (159). The +/-/context lines are **EQUAL** (sha `d0cf8555`, `77c7569c`, `59df0c16`, `9673013f`, the same on both sides). Hunk line numbers are identical, and the only difference is git's function-context suffix on the `@@` line. The fragments are the author's own and are not in the held passes.
- PR body not read directly (no Secuura gh auth used). I used the commit message (logs/commit_message.log) and the READY mail (evidence/ready_w17_pr1951.txt).
- The develop product files are byte-identical to the base product files (logs/product_sha.log). Since `1584c0f0`, develop changed nft-certificate only in `app.ts` (boundedJson) and the zod `.errors -> .issues` validation-failure branches of `nft.routes.ts` (logs/develop_nft_delta.log). Neither touches a changed catch.

## 2. The hunks (logs/product_diff.log)
- ipfs.service.ts, 3 sites (Pinata :111, Infura :212, Web3.Storage :295): `reason = (error as Error).message;` -> `reason = String((error as Error).message);`, inside the already-existing `try { } catch { reason = 'unreadable thrown value' }`. Unchanged: the return shape `{ success: false, error: '<Provider> upload error: ${reason}' }`, no log line, no rethrow.
- blockchain-verifier.service.ts getClient :70: `reason = err instanceof Error ? err.message : String(err);` -> `reason = String(err instanceof Error ? err.message : err);`. Unchanged: the `logger.warn(... { error: reason })` and `return null` ("verification disabled").
- verifyTransaction lookup :111-112: the probe lines `void (err instanceof Error ? err.message : String(err)); void (err as Error).message;` become `void String(...)` on both. Unchanged: the probe's catch (logs the constant and returns `{verified:false,status:'error',error:'unreadable thrown value'}`), the 404 branch, and the subsequent log line :123 and return :127, **which still read `err.message` raw** (G133-F3).
- What the change does: base already caught a value whose **read** throws. Head also catches a value that reads fine but cannot be **converted to text**. No new branch, log line, status or write path.

## 3. The behaviour question (RUN through the real router + real winston; scripts/probe.test.ts, probe.sh, probe_table2.py)
Every site was driven with 8 kinds: ordinaryError, thrownString, revokedProxy (thrown), throwingGetter, getterRevokedProxy, getterToStringThrows, getterNullProto, getterSymbol. Both envs. Sites: record/init, record/lookup, verifyTx/init, verifyTx/lookup, verifyAsset/init, ipfsUpload x {pinata, infura, web3storage}, mintNFT-direct (Premium + documentData), mintRoute. 160 cells per version, rc 0 both (logs/probe_{base,head}_vitest.log). Product swapped and restored by sha (RESTORE_OK).

### 3.1 Flag (1): POST /record (production shown; development identical)
| point / kind | base | head |
|---|---|---|
| lookup / **ordinaryError** | **201**, onChainVerified false, onChainStatus `error`; 1 row `pending` | same |
| lookup / revokedProxy, throwingGetter, thrownString | 201, `error`; 1 row `pending` | same |
| lookup / **getterRevokedProxy** | **500** "Failed to record NFT mint"; **0 rows**; real winston THREW in `logger.error('Error verifying transaction')` | **201**, `error`; 1 row `pending`; log `error: 'unreadable thrown value'` |
| lookup / getterToStringThrows, getterNullProto, getterSymbol | 201, `error`; 1 row `pending` (winston did not throw) | same outcome; head logs the constant for the first two |
| init / **ordinaryError** | **201**, onChainStatus `pending`; 1 row `pending` | same |
| init / getterRevokedProxy | **500**; 0 rows; winston THREW in `logger.warn('Blockfrost client init failed')` | 201 `pending`; 1 row `pending` |

**Verdict on (1): acceptable.** Head's 201 + stored row is exactly what an ordinary Error gets today at the same point.

### 3.2 Flag (2): mintNFT (direct; Pinata provider; production and development identical)
| kind | base | head |
|---|---|---|
| **ordinaryError** | **503 MINT_DEPENDENCY_UNAVAILABLE** 'IPFS upload failed: Pinata upload error: upstream boom'; row `failed` | same |
| revokedProxy, throwingGetter | 503, '...unreadable thrown value'; row `failed` | same |
| thrownString | 503, '...undefined'; row `failed` | same |
| getterRevokedProxy | 400 MINT_FAILED "Cannot perform 'get' on a proxy that has been revoked"; row `failed` with that text | 503, '...unreadable thrown value'; row `failed` |
| getterToStringThrows | 400 MINT_FAILED **'ts boom'** (the inner throw's text reached the response and the row) | 503 constant |
| getterNullProto / getterSymbol | 400 MINT_FAILED (TypeError text) | 503 (constant / 'Symbol(sym-desc)') |

**Verdict on (2): acceptable.** Ordinary Errors already get 503, and head changes no ordinary-Error answer. The status is computed as `mintFailureHttpStatus(result.errorCode)`, the function the route uses. The function result was run; the route hop was not, because the route cannot reach this branch. **`POST /mint` never reaches the upload**: routes/nft.routes.ts sets `documentData: undefined`, and mintRoute shows `ipfsFetchCalls 0` for every kind at both versions. The only callers are direct `mintNFT` callers with `documentData` (none in this repo's routes).

### 3.3 Other changed-site routes
- `POST /api/nft/ipfs/upload` (all 3 providers): ordinaryError answers 500 `'<Provider> upload error: upstream boom'` at both. For the hostile getter kinds, base answers 500 "Failed to upload to IPFS" (the generic route catch) and head answers 500 `'<Provider> upload error: unreadable thrown value'` (`Symbol(sym-desc)` for a Symbol). That is the same status and the same body shape as an ordinary Error. Nothing is stored at either version.
- `POST /verify/transaction` (public): init/getterRevokedProxy goes from base 500 to head 200 `{verified:false,status:'pending'}`, which equals ordinaryError. lookup/getterRevokedProxy goes from base 500 to head 200 `{verified:false,status:'error',error:'unreadable thrown value'}`. lookup/getterToStringThrows and getterNullProto go from base 200 with `error: {}` to the head constant. ordinaryError answers 200 `error:'upstream boom'` at both.
- `POST /verify/asset`: init/getterRevokedProxy goes from base 500 to head 200 `{exists:false}`, which equals ordinaryError.
- **Stored record (flag 1), field by field** (recordClientMint, minting.service.ts:410-446): new uuid id, `status = 'pending'` (because `onChainVerified` is false), `minted_at = null`, `transaction_hash`/`policy_id`/`asset_name`/`asset_id`/`wallet_address` as the client supplied them, `user_id = 'user-id'` (the legacy placeholder, as for every recorded mint), and `error_message = null`. `onChainVerified`/`onChainStatus` are **not persisted**; they appear only in the 201 body (false / 'error' or 'pending').
- **Does any reader treat `pending` as verified?** Read, not run: `git grep` over Blockchain/Dev (non-test). The `NFTStatus.MINTED` writers are `mintNFT` success and `recordClientMint` with `onChainVerified` true. No code path promotes a `pending` row to `minted`. GET /certificates and /certificates/:id return the status as stored. The issuer frontend's `recordMintOnBackend` (frontend/issuer/src/utils/nftMinting.ts:304-322) is fire-and-forget and ignores the body. No other service reads `svc_nft_certificates` outside the migration/DDL files.
- Nothing newly minted, charged, anchored or claimed verified. In every cell where the hostile value changed the outcome, the head outcome equals the ordinary-Error outcome. Nothing reports `verified: true` on a failure.

## 4. Re-measure
- Head, 2 new files: **22/22** (logs/head_new_tests.log).
- Base product + new files: **15 failed | 7 passed**, rc 1 (logs/red_base_new_tests.log). There are 15 AssertionErrors and no compile or import error. The 7 controls pass at base.
- Whole suite: base without the new files **27 files 178/178** (logs/base_whole_excl_new.log); base + new **200, 185 passed, 15 failed** (logs/base_whole_incl_new.log); head **29 files 200/200** (logs/after_whole.log).
- tsc: `tsconfig.json --noEmit` rc 0 (logs/tsc_plain_head.log). With the tests included (scripts/tsconfig.tests.json, root @types/node), there are **3 errors at base and 3 at head**, all pre-existing TS2322 `Buffer` -> `BlobPart` at ipfs.service.ts:65/182/267, lines this PR does not touch. The new tests add 0 (logs/tsc_tests_{base,head}.log). Planted control: an unused + mistyped const in a new test gives TS6133 + TS2322, rc 2, and the file was restored by sha (logs/tsc_tests_planted.log). Leg 16 does not cover nft-certificate.
- eslint (the ESLint API, cwd `Blockchain/Dev`; scripts/lint.cjs): 4 PR files, **0 errors, 2 warnings** (unused catch `e` in each held test, as the author says) (logs/eslint_pr_files.log). Planted `debugger` gives 1 error, rc 1, and the product was restored by sha (logs/eslint_planted.log).
- docs-fragments: clean rc 0, "flow 117 legacy + 96 new, cheat 112 legacy + 96 new" (logs/frag_check_clean.log). A planted unclosed `<div>` in flow and in cheat gives rc 1 each. Both were restored by sha, and rc 0 after (logs/frag_outer.log). The fragments' blob ids (`6d3926f7`, `ec0a3e82`) match the diff.
- Hook "PREFLIGHT INCOMPLETE 13/16" is quoted from the mail, not re-run.
- Parallelism: vitest `--maxWorkers=2`, `nice 10`, one run at a time. Load1 was 6-12 during the gate. **Node v26.8.1 only; nothing here was measured on Node 24.**

## 5. Mutants (scripts/mutants.py; one site per run, product only, tests untouched, sha256 restored after every run, all `restore=True`; logs/mutants_table.log, logs/mut_*.log)
19 runs: **15 killed, 4 survived.** Every kill was by AssertionError.
| site | M0 revert | M1 constant for all | M2 String(error) | M3 coerce, then pass raw | other |
|---|---|---|---|---|---|
| ipfs Pinata | KILLED R1-R4 | KILLED C1 C4 R4 | KILLED | KILLED R4 (Symbol) | |
| ipfs Infura | KILLED R5 R6 | KILLED C2 | KILLED C2 | **SURVIVED** | |
| ipfs Web3.Storage | KILLED R7 R8 | KILLED C3 | KILLED C3 | **SURVIVED** | |
| verifier init | KILLED R1-R3 | KILLED C1 C2 | n/a | **SURVIVED** | |
| verifier lookup | KILLED R4-R7 (both lines) | | | | M4 revert :111 only **SURVIVED**; M5 revert :112 only KILLED R7; M6 probe always throws KILLED C3 |
- M3 survives where there is no Symbol cell: Symbol is the only value that passes `String()` and then fails a template or logger. M4 is functionally redundant: for an Error, :111 and :112 coerce the same value; for a non-Error, :111's `String(err)` branch is unchanged from base. See G133-F4.

## 6. merge-tree (logs/merge_tree.log)
- Onto develop NOW `73342c2f`: **rc 0, tree `b973fdcef84f2bec31e7f3c16817eec9d62ca018`, clean.** The merged tree differs from develop in exactly the 6 PR paths, and `diff(develop, merged)` is byte-identical to `diff(base, PR head)`. There are 93 files on develop since the base (7 commits) and **0 paths shared** with the PR.

## 7. Kam's ks1346 logging rule
- **This PR adds no log line** (the product diff has no `logger.` +/- line). It changes what two existing lines receive. getClient's `warn` now gets `String(...)`: the constant for unconvertible values, the message text for ordinary ones (as at base), and `'Symbol(desc)'` for a Symbol (at base it got the raw Symbol). The lookup's constant-reason `error` line is pre-existing.
- The existing lines log the message VALUE (`error: reason`, and `error: err.message` at verifier :123), not the type and field names. That is pre-existing non-compliance with ks1346 and is not introduced here (G133-F6). Nothing new is disclosed: the hostile-kind outputs at head are the constant or a Symbol description, and the ordinary-Error text was already logged and already returned in the /ipfs/upload 500 body and the public /verify/transaction `error` field at base.

## 8. Notes for the PR body (G133-F1..)
- **G133-F1 (info, measured)** Flag (1) measured through the real router + real winston by gate 133, both envs. getterRevokedProxy at lookup or init: base 500, 0 rows, winston throws synchronously; head 201, one `pending` row. This equals the ordinary Error at both versions. Stored row: `status pending`, `minted_at null`, `error_message null`, no verified flag persisted. No reader treats `pending` as verified.
- **G133-F2 (info, measured)** Flag (2): for an ordinary Error, mintNFT already answers 503 at base, so no ordinary-Error answer changes at any site. The 400 -> 503 move applies only to hostile-getter kinds and is reachable only by direct `mintNFT` callers with `documentData`, because `POST /mint` never uploads (`documentData: undefined`). Add that sentence. Also: at base, getterToStringThrows put the inner throw's text ('ts boom') into the 400 body and the `failed` row; head replaces it with the constant.
- **G133-F3 (recommended, measured, not a regression)** The verifierTransaction lookup catch still reads `err.message` up to 4 times (probe :111, :112, log :123, return :127). A non-idempotent getter (readable on the first 2 reads, revoked Proxy after) still makes `verifyTransaction` reject at head, so /record answers 500 with nothing stored. Readable for 3 reads, it returns a revoked Proxy as `error`, so /verify/transaction's `res.json` would 500. Base rejects for 0-2 readable reads, so head is strictly better (logs/flip.jsonl, scripts/flip.test.ts). Follow-up fix, not for this PR: read once, `let reason: string; try { reason = String(err instanceof Error ? err.message : err); } catch { ... }`, then log `error: reason` and return `error: reason` (with `'Unknown error'` where base returned it for a non-Error).
- **G133-F4 (recommended, test gap, measured)** Mutant M3 ("coerce, then pass the raw value") survives at Infura, Web3.Storage and getClient, because only Pinata has a Symbol cell. Add a Symbol cell to C/R for those three. M4 (revert :111 only) survives because :111's change is redundant with :112. Either drop the redundant line or say so.
- **G133-F5 (info, correction to fragment/commit wording)** "a Symbol is reported as its text" holds at the 3 upload catches and getClient. At the lookup catch, the raw Symbol still reaches the logger (:123), and the response's `error` field is dropped by JSON. Base = head there.
- **G133-F6 (info, pre-existing, ks1346)** The touched catches log, and in /ipfs/upload and /verify/transaction return, the thrown message VALUE. This is a ks1346 follow-up for the KS-1868/KS-1346 site lists, not this PR.
- **G133-F7 (info, pre-existing, out of scope, observed in the probe)** With `isCardanoNFTReady()` false, `POST /mint` falls back to mock minting and stores a `minted` row with a fabricated tx hash, even under `NODE_ENV=production`. There is no production guard in `mintOnCardano`'s mock branch (minting.service.ts:817-833). The behaviour is the same at base and head and is unrelated to this PR, but worth a card.
- **G133-F8 (info)** tsc with the tests included shows 3 pre-existing TS2322 errors in ipfs.service.ts (:65/182/267) at base and head. nft-certificate is outside leg 16.

## 9. NOT TESTED
- The real PR body (no gh auth); a real Blockfrost, IPFS provider or Postgres; a booted service through `app.ts`. The probe mounts the real router with a test identity middleware and the shared `errorHandler`, so jwt, helmet, cors, boundedJson and rejectControlBytes were not in the path. Also not tested: the merged tree (the route probe ran on the PR head; develop's nft-certificate delta touches only validation-failure branches); Node 24; the four platform suites; CI; the pre-push hook legs (quoted only); a real chain mint (`../cardano` stubbed); the Linear ticket text; the readers' behaviour beyond `git grep` (§3.3 is read, not run).

## Processes
No containers were started. Background: two `npm ci` runs (completed). All vitest runs were foreground and completed. Nothing is left running. Probe and flip test files were copied into the clone for each run and then moved to logs/_quarantine/. The first service-local `npm ci` node_modules was moved to logs/_quarantine/svc_node_modules (not deleted). The clone's push URL is `no_push_qa_gate`.
