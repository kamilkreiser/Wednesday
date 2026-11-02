# QA Gate 108 verdict (TIER 2): Secuura/Distributed_Secuura PR 1926 (KS-1868, nft-certificate ipfs.service.ts upload catches)

## BLUF
**GATE 108 (TIER 2) on PR 1926 at 608b37c5b0b8: GO WITH NOTES. Nothing has to be fixed before merge.**

The three guards do what the PR says, and nothing else changed. With the real `IPFSService`, the real `/api/nft/ipfs/upload` route and the real `NFTMintingService.mintNFT` run at both products, an unreadable value (a revoked Proxy, an Error whose `message` getter throws) now gets exactly what an ordinary provider Error gets, at all three providers:
- `upload()` resolves `{ success: false, error: "<Provider> upload error: unreadable thrown value" }` instead of rejecting.
- The route answers 500 with that string.
- The mint classification moves 400 MINT_FAILED -> 503 MINT_DEPENDENCY_UNAVAILABLE. This is the same class an ordinary Error gets (I ran both values through the real `classifyMintError`).
- The persisted mint record is `failed` in both cases, with the same "IPFS upload failed: ..." form.
- No STOP-class outcome. The provider is called once for every value. The chain-call counter reads 0 for every value.

One residual gap remains, identical to base and so not a regression (G108-F1, recommended follow-up).

TIER 2 is right: for an unreadable value the persisted mint state equals the ordinary-Error state, and no chain call happens on either path (details in Check 4).

## 1. Heads + diffstat (logs/head_start.log, mergetree.log, pr_paths.log)
- PR head `608b37c5b0b84d95fbe2baba95dd0d5c09df69e1` at START (05:44Z) and at END (05:55Z): identical. Develop `8f313815f415` at both times.
- Single commit, parent `968f17070208` (rev-list --parents), author Kam Kreiser <kamil.kreiser@secuura.ai>.
- Three-dot diff vs develop: exactly 4 files, +175/-3, as the mail says:
  - `ipfs.service.ts` 21/3
  - the new test 115/0
  - the flow fragment 20/0
  - the cheat fragment 19/0
- Shared paths between the PR (4) and develop's 13 paths past the base: **0**. `git merge-tree --write-tree 8f313815f415 pr1926` gives rc 0, tree `35eccb28`, and the result changes exactly the PR's 4 paths (SAME_PATHS).
- PR body NOT read (no Secuura gh auth on this host). I used the READY mail (evidence/r74_ready_for_gate_1926.txt).

## 2. The hunks
Each of the three catches has the same change, and it is the guard PR 1915 merged in this file (`fetch()` catch):
```
-  error: `Pinata upload error: ${(error as Error).message}`,
+  let reason: string;
+  try { reason = (error as Error).message; } catch { reason = 'unreadable thrown value'; }
+  error: `Pinata upload error: ${reason}`,
```
- Sites: Pinata :108, Infura :203, Web3.Storage :280 (base lines).
- The returned object and the message text for readable values are unchanged. `pin`, `unpin`, `fetch`, the route and `classifyMintError` are untouched.
- The hand edit: `encrypted: false` appears once, on the REQUEST fixture line of the new test (line 18).
  - It is the same convention as two sibling tests (`ipfs.service.test.ts:25`, `ks1240b...:25`).
  - I removed it in a scratch run and `tsc` gave `TS2345` at the new test (28,44), so the edit is the fix. With it, the new test file has 0 tsc errors.
  - I cannot diff it against the author's canonical bytes (not in evidence). That the edit is exactly one line is read, not measured against the canonical patch.

## 3. Behaviour (scripts/g108_probe.test.ts, runprobe.sh; logs/probe_{base2,head2}_<provider>.jsonl, compare.txt)
HOW: the REAL `IPFSService` singleton (env pinata, infura or web3storage), the REAL `nft.routes` router on a real http server, and the REAL `NFTMintingService.mintNFT` (PREMIUM tier, with documentData), plus the real `classifyMintError`. Only the logger, the provider `fetch` (rejects with the injected value) and a counting wrapper on `../cardano` are replaced. In-memory persistence (no DB). Base product = develop's `ipfs.service.ts` (the PR does not touch other product files), head = PR.

| value | base: upload() | base: route | base: mint | head: upload() | head: route | head: mint | persisted at head |
|---|---|---|---|---|---|---|---|
| ordinary Error | success:false "...connect refused" | 500 same text | 503 | same | 500 same | 503 | failed, "IPFS upload failed: ..." |
| revoked Proxy | REJECTS TypeError | 500 "Failed to upload to IPFS" | **400** MINT_FAILED, message = TypeError text | success:false "...unreadable thrown value" | 500 with that string | **503** | failed, "IPFS upload failed: <P> upload error: unreadable thrown value" |
| message getter throws | REJECTS "getter boom" | 500 generic | **400** | as above | as above | **503** | as above |

- The same table holds for Pinata, Infura and Web3.Storage (24 base cells, 24 head cells). The ordinary-Error rows are byte-identical base vs head.
- Persisted record: status `failed` in every cell at both products. At base the unreadable-value `errorMessage` is the raw TypeError text with no "IPFS upload failed" prefix. At head it equals the ordinary form.
- Side effects: provider fetch called exactly once per value per path, no retry, at both products. (The ordinary mint run shows 2 because the first mint also makes one originate-lookup fetch; the cache removes it afterwards.)
- Chain calls: the counter on `mintNFTOnChain`/`getPolicyId`/`waitForNFTConfirmation` is 0 for every value at both products (no positive control for the counter; it is also true by code order, since the IPFS failure throws before `mintOnCardano`).
- Author's claim "mint classification 400 -> 503, and 503 is what an ordinary Error already gets": **confirmed** (classifyMintError on "IPFS upload failed: ..." -> MINT_DEPENDENCY_UNAVAILABLE, like the ordinary row).
- Author's base correction ("at base an unreadable value does NOT go unanswered; upload's own catch raises a TypeError"): **confirmed**. The route answers 500 and the mint record is FAILED, with HTTP 400 on the mint path.
- Reach (read, grep): the only callers of `mintNFT` are the `/mint` route and tests. The route passes `documentData: undefined` (`nft.routes.ts:81`), so the PREMIUM IPFS branch is not reachable over HTTP today. The 400->503 shift therefore only reaches direct callers. The live reach of this PR is `POST /api/nft/ipfs/upload` (500 either way, different body text). `IPFSService.upload()` itself has no production caller.

## 4. TIER
TIER 2 stands. The mint path is touched, but for an unreadable value:
- the persisted state is `failed`, equal to the ordinary-Error state with the same message form;
- no chain call is made on either path;
- the only differences are the HTTP status class 400 -> 503 and the stored text, both moving to the ordinary values.

## 5. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Red-first:** with the head test file at develop's product (`8f313815f415`): 3 control cells pass, **6 RED cells fail, all by assertion** (`expected { rejected: true } to deeply equal { resolved: { success: false, ... } }`; logs/red_base.json). The author said 6 of 9; matches. At head all 9 pass.
- **Mutants** (product only, test untouched, sha256-restored after each; scripts/mutants.py, logs/mutants.log; three forms x three sites; the run includes the neighbouring ipfs.service and ks1240b tests):

  | form | site 1 Pinata | site 2 Infura | site 3 Web3.Storage |
  |---|---|---|---|
  | undo guard | R1, R2 only | R3, R4 only | R5, R6 only |
  | constant reason | C1, R1, R2 | C2, R3, R4 | C3, R5, R6 |
  | catch rethrows | R1, R2 only | R3, R4 only | R5, R6 only |

  Each mutant turns exactly its own provider's cells red, 0 survivors, RESTORE_OK, `git status` clean afterwards.
- **Whole nft-certificate suite** (vitest 1.6.1, installed with `npm install --no-package-lock` because `npm ci` refuses at base: the lockfile is out of sync with package.json; plus `packages/shared` built for `@secuura/shared`):
  - base `8f313815f415`: 25 files, 162 tests, 161 pass, 1 fail (`db.retry.test.ts`, KS-1328 "every cell carries the 60 s budget", `expected undefined to be 60000`);
  - head: 26 files, **171 tests**, 170 pass, the same 1 fail.
  - 162 -> 171 matches the author. The 1 failure is identical at both products in an unchanged file. It reads `task.timeout`, which vitest 1.6.1 (my unlocked install) does not set, so I read it as an installed-version artefact. The fragment says "0 failed", which I could not reproduce. Not run with the lockfile versions.
- **tsc with tests** (scripts/tsconfig.tests.json, 26 test files in the program): the plain config is rc 0. With tests there are 2 errors (TS2322 in `db.retry.test.ts:55` and `ipfs.service.test.ts:42`, both unchanged files, both vitest-typing), and 0 errors in the PR's test file. Without the hand edit there is 1 more (TS2345, see Check 2). The author's "0 before, 0 after" used its own install; mine is not comparable on the two pre-existing ones.
- **eslint** (ipfs.service.ts + the new test, repo flat config, eslint borrowed from gate 107's node_modules via a symlink): rc 0, 0 errors, 1 warning (`'e' is defined but never used`, test line 29, the `answer` helper's `catch (e)`). A planted file gives rc 1 with `debugger` and unused var (logs/eslint_planted.log).
- **docs-fragments check:** rc 0, "flow 117 legacy + 78 new, cheat 112 legacy + 78 new; lint clean, render passes" (logs/frag_head.log). It carries two ADVISORY lines (flow :6249, cheat :6235, the "adopt cannot absorb" class from G105-F8; the flow one I did not compare against base). A planted unbalanced `<div>` in the PR's cheat fragment gives rc 1 "tags are not balanced: <div> opened 3, closed 2"; the fragment was restored (sha256 `853de8150ff7` before and after).
- The pre-push hook (13/16 legs, PREFLIGHT INCOMPLETE) and CI are the author's; not re-run.

## 6. merge-tree
See Check 1: clean (rc 0), 0 shared paths, the result changes exactly the 4 PR paths.

## 7. Kam's ks1346 logging rule
The diff adds no log line. The only new text is the constant `unreadable thrown value` placed in the returned `error`, which the route echoes. No thrown value reaches a log or a response in the unreadable case.

## 8. FINDINGS
- **G108-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured).** The guard wraps only the READ of `.message`. If the getter succeeds and returns a hostile NON-string (a revoked Proxy, an object whose `toString` throws, a Symbol, a null-prototype object), then `${reason}` throws INSIDE the catch, outside the guard.
  - Result at head, identical to base (no regression): `upload()` rejects, the route answers 500 "Failed to upload to IPFS", the mint answers **400** MINT_FAILED with the raw TypeError/Error text as the record's `errorMessage`. The cells are msgRevoked, msgToStrThrows, msgSymbol and msgNullProto, at all three providers (compare.txt).
  - This is the G105-F1 / G107 shape that PR 1924 closed by coercing inside the try. Suggested follow-up: `reason = String((error as Error).message)` inside the same try, plus a cell. Nothing in the fragments claims this shape is handled ("a thrown value that cannot be read").
- **G108-F2 (INFO, measured).** Body text change on the live route: for an unreadable value `POST /api/nft/ipfs/upload` still answers 500, but the message goes from the generic "Failed to upload to IPFS" to "<Provider> upload error: unreadable thrown value". The fragments disclose this.
- **G108-F3 (INFO, doc accuracy, measured).** The fragments say the mint path was not run end to end ("only classifyMintError was run"). I ran the real `mintNFT` up to the IPFS step. The fragments also do not say that `/mint` passes `documentData: undefined`, so the PREMIUM branch is not reachable over HTTP and the 400 -> 503 shift reaches direct callers only (Check 3, Reach).
- **G108-F4 (INFO, pre-existing, unchanged).** A thrown plain string gives "upload error: undefined" at all three providers (`'str'.message`). Same at base and head, and the mint classifier still says 503. Outside this PR's remit.
- **G108-F5 (INFO).** Suite figures in the fragments say 0 failed. My run (vitest 1.6.1) shows 1 failure in an unchanged file at both base and head (Check 5). `npm ci` is refused at base (lockfile out of sync: vitest, coverage-v8, uuid). Neither is caused by this PR.
- **G108-F6 (INFO).** eslint warning for an unused `e` at test line 29. Optional (`catch {`).
- **G108-F7 (INFO).** The hand edit is exactly one line by read, matches sibling fixtures, and is necessary for tsc (TS2345 without it). I could not diff it against the author's canonical bytes.
- **No FIX-BEFORE-MERGE item.**

## 9. UNMEASURED / NOT TESTED
- The live PR body, the Linear ticket, CI, the pre-push legs, and Node 24.
- A real IPFS provider, a real DB (persistence was in-memory), a real Cardano chain, and a real boot of the service (the router was mounted on a bare express app, so auth and middleware were not exercised).
- The author's canonical (pre-hand-edit) test bytes.
- The lockfile-pinned vitest and the 1 `db.retry` failure under it.
- The chain-call counter has no positive control.
- Whether any hostile thrown value occurs in reality (all values are synthetic).
- The flow-fragment ADVISORY at :6249 was not compared against base.
- Non-"undo" mutants beyond the three forms listed.
