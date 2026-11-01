# QA Gate 97 verdict: Secuura/Distributed_Secuura PR 1915 (KS-1868, nft-certificate ipfs.service.ts, IPFSService.fetch two catches, O59-P1)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge. Tier: 2 (agree with the author; operator 59 said "low", the 500 -> 503 status move on two read routes makes 2 the safer label).**
I ran the REAL routes `GET /api/nft/ipfs/:cid` and `GET /api/nft/ipfs/:cid/encrypted` (real router, real `IPFSService` singleton on the pinata/HTTP-gateway path, real shared `errorHandler`) on a loopback listener at base and at head, with only the gateway `fetch`, `../db`, `../cardano` and the logger replaced (logs/probe_table.log, scripts/probe_route.test.ts):
- **Q1:** an unreadable rejection (revoked Proxy; Error with a throwing `message` getter) at the gateway request OR the body read answers **500 INTERNAL_ERROR "An unexpected error occurred" at base** (no log line at all: the throw happens before the logger call) and **503 SERVICE_UNAVAILABLE "IPFS gateway is temporarily unavailable" at head** with the warn line carrying `error: "unreadable thrown value"`. 8 of 8 unreadable cells (2 routes x 2 stages x 2 values). An ordinary Error is **byte-identical at base and head**: 503, same body, same warn line (`error: "gateway down"`), all 4 cells.
- **Q2:** every success and non-throw path is identical base vs head, status, body, log lines and gateway call count: 200 plain content, 200 encrypted package, gateway 404 -> 404 NOT_FOUND, gateway 502 -> 503 (warn "non-OK"), and the two route-level 500s that come from `fetchEncrypted` (non-encrypted JSON / non-JSON body) which are not in this hunk. Nothing about what is returned, cached or decrypted changes (no cache or decrypt code is in the hunks).
- **Q3:** product hunks vs the held section: **EQUAL** (all 28 content lines, +14/-2; the only textual difference is git's `@@ ... export class IPFSService {` function-context suffix on the two hunk headers).
The raise is acceptable: the unreadable-value after-state equals what an ordinary Error already gets at base, and the 503 is what the method's own doc comment promises.

## Heads
- START (logs/head_start.log, 23:28:16Z): `refs/pull/1915/head` = `8277beec416c64d30fc64bf06f0dd24797524a7d` (matches the READY mail), develop `b887480394cc67764922b0aa123027c344241ed7`. One commit; its parent and merge-base is `03977e89a343` (an ancestor of current develop).
- END (logs/head_end.log, 23:33:36Z): both unchanged; local HEAD `8277beec`; working tree clean; product sha256 `6f3e9111...` (head), `cf181c21...` (base and also current develop: develop has not touched ipfs.service.ts).
- **PR body not read directly** (no gh login for the Secuura account); the author's READY and BUILT AND PROVEN mails (evidence/) were used.

## 1. Diffstat (three-dot vs origin/develop; logs/diffstat.log)
4 files, +170/-2, exactly as claimed: ipfs.service.ts (+14/-2, 2 hunks), `ks1868-ipfs-fetch-unreadable-throw.test.ts` (+115, sha256 `6e7b904b...` same as the author's), one flow fragment (+21) and one cheat fragment (+20). Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
Both catches: a 6-line guard `let reason: string; try { reason = error instanceof Error ? error.message : String(error); } catch { reason = 'unreadable thrown value'; }` inserted before the log, and the one log argument `error: error instanceof Error ? ... : String(error)` swapped to `error: reason`. Catch 1 = gateway request (base :482-490, head :483), catch 2 = body read (base :507-519, head :515). Unchanged: log level `warn`, message strings, `cid` key, `throw new ServiceUnavailableError('IPFS gateway')`, the 404/410/non-ok branches, `Buffer.from(arrayBuffer)`. The guard text is the one already merged in minting.service.ts.

## 3. Behaviour, RUN through the real routes (logs/probe_base.json, probe_head.json, probe_table.log; 23 cells each, rc 0; unhandled rejections 0 in every cell)
| route | stage / value | base | head |
|---|---|---|---|
| plain and /encrypted | request, ordinary Error | 503 SERVICE_UNAVAILABLE; warn "IPFS gateway unreachable" error "gateway down" | identical |
| plain and /encrypted | request, revoked Proxy | **500** INTERNAL_ERROR; no log | **503** SERVICE_UNAVAILABLE; warn error "unreadable thrown value" |
| plain and /encrypted | request, throwing getter | **500**; no log | **503**; warn "unreadable thrown value" |
| plain and /encrypted | body, ordinary Error | 503; warn "body read failed" "gateway down" | identical |
| plain and /encrypted | body, Proxy / getter | **500**; no log | **503**; warn "body read failed" "unreadable thrown value" |
| plain and /encrypted | gateway 404 / 502 | 404 NOT_FOUND / 503 + warn non-OK | identical |
| plain | 200 content | 200, base64 content, size 12 | identical |
| /encrypted | 200 encrypted package | 200, encryptedData, metadata | identical |
| /encrypted | 200 non-encrypted / non-JSON | 500 (JSON.parse / "Data is not encrypted" in fetchEncrypted, not in the PR) | identical |
Persisted state and side effects: none exist on these read routes (no db write, no chain call, no cache); the gateway was called exactly once in every cell at both versions. The only observable moves are the status/body (500 -> 503) and a warn line that did not exist at base for the unreadable cases. The author read the mapping from source; I ran it, so the PR body's "read from source, not requested over HTTP" is now additionally confirmed by a run (with a real errorHandler but a probe app, see NOT TESTED).

## 4. Re-measure (Node v26.8.1 only; none of it measured on Node 24)
- **Red first** (logs/red_base.log): base product, new test as committed: **4 failed, 2 passed**, all four `AssertionError: expected { statusCode: undefined, ... } to deeply equal { statusCode: 503, ... }`; the 2 controls green.
- **Whole service suite** (scripts/vt.sh, vitest from the workspace binary): base (new file moved aside) **22 files / 149 of 149**; head **23 files / 155 of 155**; +1 file, +6 tests, 0 failed, 0 skipped. ipfs.service.test.ts and ks1240b also run green inside the mutant runs.
- **tsc** (logs/tsc_*.log): plain tsconfig rc 0; with tests in the program (scratch tsconfig because the service tsconfig excludes `src/__tests__`): **0 errors, 44 service src files listed** (the new test included); a planted `const x: number = "gate97"` is reported (TS2322 and TS6133, rc 2), file restored byte-identical. The repo's leg-16 checker was not run.
- **eslint** on ipfs.service.ts and the new test: 0 problems, rc 0; a planted file fires `no-debugger` (error) and unused-var (warning), rc 1.
- **docs-fragments** (scripts/frag.sh, logs/frag_*.log): check OK, rc 0, "flow 117 legacy + 64 new, cheat 112 legacy + 64 new; lint clean, render passes", 1 ADVISORY line printed (cheat page differs from render at line 6235; the author counts 2, not compared at develop). Planted defects, each restored by sha: unclosed `<div>` in flow rc 1, in cheat rc 1; `<p>` prose outside a table in flow rc 1, in cheat rc 1; after restore rc 0. Fragment figures (155/23, 149/22, 2/4 red, 43/44 files, lines 482/507 of the base) agree with my measurements; "hunk mutants 2 of 2" is reproduced in section 5.

## 5. Mutants (scripts/mutants.py; one mutation at one catch in the product, tests untouched, sha256 restored and checked after every run, all `restore True`; runs include ipfs.service.test and ks1240b)
18 runs (9 mutants x 2 catches): **16 killed, 2 survived.**
| Mutant | catch 1 (request) | catch 2 (body) |
|---|---|---|
| M0 drop the guard | KILLED R1 R2 (assertion) | KILLED R3 R4 |
| M2 constant -> `String(error)` | KILLED R1 R2 | KILLED R3 R4 |
| M3 rethrow only when unreadable | KILLED R1 R2 | KILLED R3 R4 |
| M4 constant for every value | KILLED C1 | KILLED C2 |
| M5 rethrow `error` instead of the 503 | KILLED C1 R1 R2 + ks1240b cells | KILLED C2 R3 R4 + ks1240b |
| M6 readable non-Error branch -> `'x'` | **SURVIVED** | **SURVIVED** |
| M7 log call removed | KILLED C1 R1 R2 | KILLED C2 R3 R4 |
| M8 throw plain `Error` instead of ServiceUnavailableError | KILLED | KILLED |
| M9 swallow and return an empty Buffer | KILLED | KILLED |
M6 is the known readable-non-Error gap (same as G90-F3, G91 M6): no cell throws a readable non-Error (a string, a number), so the `String(error)` branch is not pinned. Not changed by this PR.

## 6. merge-tree onto current develop (b88748039; logs/merge_tree.log, merge_changed.log, shared_paths.log)
`git merge-tree --write-tree origin/develop pr1915`: **rc 0, clean**, tree `09b43c11...`. The merged tree differs from develop in **exactly the four PR paths**. Develop moved 17 files past the base (5 under nft-certificate, among them PR 1909's minting.service.ts and its tests); shared paths with the PR: **0** (comm of the two path lists, empty). ipfs.service.ts is byte-identical on develop and at the base, so the head's product hunk applies unchanged. I did not re-run the suite on the merged tree (no second install); the two services files are independent (minting.service.ts uses only `uploadEncrypted`, per the author, not re-grepped by me).

## 7. Kam's ks1346 logging rule
Both new/changed log lines log either the Error's own `message` (as base did) or the constant `unreadable thrown value`, plus `cid`. No thrown object, no keys, no stack, no field values. Compliant.

## FINDINGS / NOTES FOR THE PR BODY
- **G97-F1 (info, reachability)** Neither value is produced by an actor: `fetch` rejects with an Error (TypeError with cause), `arrayBuffer()` with a DOMException/Error. An unreadable one needs a wrapper or a test double. Defence in depth, as every KS-1868 site; all thrown values in the PR and in my probe are synthetic.
- **G97-F2 (info, behaviour)** Observable change is the status on two read routes for unreadable inputs only: 500 INTERNAL_ERROR -> 503 SERVICE_UNAVAILABLE, and a new warn line (base logged nothing). No state is written on these routes. Any client that special-cases 500 on these routes for this input is not read (gateway consumers not examined).
- **G97-F3 (recommended, wording; body and fragments)** The PR body, flow fragment (".3 What this does not prove") and cheat page say the routes and `errorHandler` were not run over HTTP. That was true for the author; gate 97 ran them (this probe), so the body may add "confirmed at gate 97: 500 -> 503, ordinary Error unchanged, success paths unchanged". Not a defect; keep the "not run by the author" wording honest.
- **G97-F4 (low, test gap, measured)** M6 survives at both catches: no cell throws a readable non-Error. Optional: one cell that rejects with the string "boom" and asserts `error: 'boom'` in the log.
- **G97-F5 (info, follow-ups, measured by grep)** Same file, not in this PR and not KS-1868 unreadable-value fixes: the three provider upload catches `ipfs.service.ts:108, 203, 280` read `(error as Error).message` unguarded in a returned `{ success: false, error }` string (a throwing getter there would reject `upload`; they sit in provider `upload()` methods, outside `fetch()`). Also `blockchain-verifier.service.ts:69, 109` (operator 59: verdict-changing, deliberately skipped) and the remaining route catches in nft.routes.ts.
- **G97-F6 (info)** ADVISORY count: my docs-fragments run prints 1 ADVISORY line; the author reports 2. Not compared against an untouched develop; harmless.
- **G97-F7 (info)** Author's PREFLIGHT INCOMPLETE (13/16 legs, legs 3, 4, 8 skipped, local stack down; "Nothing failed") is quoted from the mail only; I did not run the pre-push hook or CI.

## 8. Tier
Tier 2. The status moves 500 -> 503 for inputs nobody can produce, onto the answer an ordinary error already gets; no auth, credential, chain write, credit or persisted-data path is touched. Tier 1 would apply only if a security decision moved fail-closed to fail-open; none did.

## 9. NOT TESTED
The live PR body (no gh auth); a real IPFS gateway or provider; a booted service (app.ts `jwtAuthenticate` was not mounted; the probe app mounts the real router and the real shared `errorHandler` only, so the full middleware chain, incl. rejectControlBytes and auth, was not run); the `provider.read` (mock) path (untouched by the hunks); Node 24; the leg-16 typecheck checker; the four platform suites; CI; the pre-push hook legs; the suite on the merged tree; ESM/Windows; Spark shadow calibration.

## Scratch
Scratch files moved to logs/_quarantine (the probe copy, tsconfig.gate97.json, the planted lint file, the aside-moved new test). Repo working tree clean at end. No push, no GitHub/Linear write, no mail.
