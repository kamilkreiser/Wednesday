# QA Gate 91 verdict: Secuura/Distributed_Secuura PR 1909 (KS-1868, nft-certificate minting.service.ts, two catch sites O51-P1 / O51-P2)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge. Tier: 2 (agree with the author).**
I ran the REAL `POST /api/nft/mint` and `GET /api/nft/certificates?walletAddress=` routes (real router, real `NFTMintingService`, real `classifyMintError`, real KS-1836 read gate) on a loopback listener, at base and at head, with only `../db`, `../cardano`, the logger and the originate-URL `fetch` replaced (logs/probe_table.log, scripts/probe_route.test.ts). All three key questions re-measure exactly:
- **Q-A (P1):** an unreadable fetch rejection in production answers **400 MINT_FAILED carrying the TypeError text** at base (revoked Proxy: "Cannot perform 'getPrototypeOf' on a proxy that has been revoked"; throwing getter: "getter boom"). At head it answers **404 CERTIFICATION_NOT_FOUND "Certification not found"**, byte-identical to an ordinary `Error('originate down')` (404, same body, at both base and head) and to a non-ok response. The P1 test restores NODE_ENV (measured, G91 section 4).
- **Q-B (P2):** an unreadable DB rejection answers **500 "Failed to fetch NFT certificates"** at base (route log `Error fetching certificates`); at head **200 with the in-memory match (count 1)**, the same as an ordinary DB error gives at both base and head.
- **Q-C:** nothing on the mint path that moves a chain write or a credit changes. The route probe records zero calls into the cardano module (`isReady`, `mintNFTOnChain`, `getPolicyId`, `wait`: `chain: []` in all 8 mint-cell runs, base and head) and the SQL sequence is the same two upserts (PENDING, then FAILED) in every cell. The service has no credit/charge/ledger code at all (`grep -il credit|debit|ledger|charge` over non-test src: 0 files, positive control `minting.service.ts` hits for `logger`). `getCertificationData` has one caller (`mintNFT` :255), reached before the first status update past PENDING, before IPFS and before any chain call.
The raise is acceptable: in both sites the unreadable-value after-state equals what an ordinary Error already gets, and nobody who acts on the system can produce either value (G91-F2).

## Heads
- START (logs/head_start.log): `refs/pull/1909/head` = `5f30fb1b9411c413f8dc02f9e6cf8a0e1455d3ca` (matches), develop `03977e89a343ad7362760e4fb0270602fb6da5ce`. One commit; its parent is develop; merge-base = develop.
- END (logs/head_end.log): PR head `5f30fb1b...` unchanged, develop `03977e89...` unchanged; local HEAD `5f30fb1b`; product sha256 `8f2839d3...` (head), `56e1e777...` (develop); working tree clean after quarantining my scratch files to logs/_quarantine.
- **PR body not read directly** (no `gh` login for the Secuura account here). I used the author's READY and BUILT AND PROVEN mails (evidence/) and the committed fragments. Wording in the live PR body that I could not see is not verified.

## 1. Diffstat (logs/diffstat.log; three-dot vs 03977e89)
5 files, +230/-2, exactly as claimed, nothing outside its declared paths: minting.service.ts (+14/-2; the stat bar shows 16 changed lines), two new test files (+103 and +71), one fragment pair (flow +22, cheat +20 per stat). All five paths are the five the author names.

## 2. The hunks (logs/product_diff.log)
Two sites, same shape as gate 90's: a 6-line guard (`let reason: string; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }`) inserted before the log, and the one log argument swapped to `error: reason`. P1: the production branch catch of `getCertificationData` (base :174, log :175); P2: the DB catch of `getWalletNFTCertificates` (base :688). Unchanged: message text, level `error`, other keys (`certificationId`), `return null` (P1), the fall-through to `certificates.sort(...)` (P2), no rethrow. The non-production branch (bare `catch {}`) is untouched. The guard text at both sites matches the three guards already merged at :92 :137 :518 :604 (PR 1899).
Left alone, named by the author and confirmed: `mintOnCardano` log (now `minting.service.ts:810` at head; the author says :798, which is the base line) and `utils/mintError.ts:37` `classifyMintError`.

## 3. Behaviour (Q-A, Q-B, Q-C), RUN through the real routes (logs/probe_base.json, probe_head.json, probe_table.log, probe_*.log)
All 7 probe cells ran at each version (rc 0). Unhandled rejections: 0 in every cell.

POST /api/nft/mint, `NODE_ENV=production`, fetch to the originate URL rejects (base / head):
| case | status | errorCode | message | log | SQL | cardano calls |
|---|---|---|---|---|---|---|
| ordinary Error | 404 / 404 | CERTIFICATION_NOT_FOUND / same | "Certification not found" / same | `error: "originate down"` / same | 2 upserts / same | none / none |
| non-ok response (status 404) | 404 / 404 | same | same | `Failed to fetch certification from originate service` / same | same | none |
| revoked Proxy | **400** / **404** | **MINT_FAILED** / **CERTIFICATION_NOT_FOUND** | the TypeError text / "Certification not found" | **none** / `error: "unreadable thrown value"` | 2 upserts / same | none / none |
| Error whose `message` getter throws | **400** / **404** | MINT_FAILED / CERTIFICATION_NOT_FOUND | "getter boom" / "Certification not found" | none / `unreadable thrown value` | same | none |

Persisted state: PENDING upsert then a FAILED upsert in every cell; only the stored `errorMessage` differs for the two unreadable cases (the TypeError text at base, "Certification not found" at head), which is the same message an ordinary failure stores. `GET /api/nft/certificates?walletAddress=` (one seeded in-memory row owned by the caller, DB SELECT rejects):
| case | status | body | log |
|---|---|---|---|
| ordinary Error | 200 / 200 | count 1 / count 1 | `DB get wallet certificates failed`, `error: "originate down"` / same |
| revoked Proxy | **500** "Failed to fetch NFT certificates" / **200**, count 1 | | base: route log `Error fetching certificates` (the service's own line is lost); head: service line, `unreadable thrown value` |
| throwing getter | **500** / **200**, count 1 | | same |

**The existing conflation is unchanged, not widened.** A fetch failure of ANY kind (network down, non-ok, now unreadable) is reported as "Certification not found"/404 at base already for ordinary errors and non-ok responses; head only moves one more input onto it. The 404-for-an-outage honesty question (it arguably should be 503) is pre-existing and is G91-F4.
**Side note on the KS-1836 gate (read, and confirmed by the probe seeding):** every real row carries `userId 'user-id'`, which the read gate treats as nobody, so for a real caller the wallet route lists nothing today whichever way the DB behaves. The 200-with-count-1 above needed me to re-stamp the seeded row's owner. The status change (500 to 200) is real; the body for a production caller is `count 0` either way until KS-1820.

## 4. Re-measure (Node v26.8.1 only; nothing here is measured on Node 24)
- **Red first (logs/red_base.log):** product at develop `56e1e777`, tests as committed: **4 failed, 3 passed, rc 1**, all four by `AssertionError`: fetch R1/R2 `expected 'MINT_FAILED' to be 'CERTIFICATION_NOT_FOUND'`, wallet R1/R2 `expected [] to have a length of 1 but got +0`. Controls C1, C2 (fetch) and C1 (wallet) pass at base. Product restored by sha (`8f2839d3...`) after.
- **Green at head:** 7/7, three runs (logs/head_new_{1,2,3}.log).
- **Whole service suite:** base without the new files **22 files, 149/149** (logs/whole_base.log); head **24 files, 156/156** (logs/whole_head.log). +2 files, +7 tests, ratio 156/149, 0 failed, 0 skipped. vitest from the workspace root binary with `--root`, `--maxWorkers=2`; `@secuura/shared` built first.
- **tsc:** plain `tsconfig.json` rc 0; with tests (scratch config, because the service's own tsconfig excludes `src/__tests__` and it has no test config): head **0 errors** (45 files, both new tests listed), base set (new tests excluded) **0 errors**; planted `const x: number = "gate91"` in a new test is reported (TS2322, rc 2) and the file restored byte-identical (logs/tsc_*.log). I did not run the repo's leg-16 checker; it has no nft baseline file in `scripts/typecheck-tests/` (baselines exist for api-gateway, auth, m365, security, vc-issuer).
- **eslint:** product file + both tests, from the service dir: **0 problems, rc 0**; planted file: `no-debugger` error + unused var warning, rc 1 (logs/eslint_*.log).
- **docs-fragments** (logs/frag_*.log, scripts/frag.sh): `check` rc 0 "flow 117 legacy + 64 new, cheat 112 legacy + 64 new; lint clean, render passes", **2 ADVISORY lines** (the author says the same 2 sit on untouched develop; I did not re-run it at develop). Planted defects, each restored by sha: flow unclosed `<div>` rc 1 (tags not balanced); cheat unclosed `<div>` rc 1; flow and cheat `<p>` prose outside a table rc 1 (html_docs_check); after-restore rc 0. Content of the fragments checked against the measurements: the 400 -> 404 and 500 -> 200 claims, the 149/156 figures, the 3/4 red split and "line 174 / 688 of the base" are all right; one claim is over-stated (G91-F1).
- **NODE_ENV restore (the author's second probe, re-measured by me):** a sentinel cell appended to a copy of the fetch test file passes (the unmutated copy: all 5 cells, logs/sent.log shows the combined run of both copies as 9 passed, 1 failed), and with the `process.env.NODE_ENV = savedEnv;` line removed the sentinel fails (the mutated copy: 1 failed, the sentinel; the combined run was `1 failed | 9 passed`). The committed afterEach restores it. `savedEnv` is `'test'` under vitest; had it been undefined the assignment would store the string "undefined" (cosmetic, G91-F5).

## 5. Mutants (scripts/mutants.py: one mutation at one site in the product file, tests untouched, sha256 restored and checked after every run, all `restore True`; logs/mut_*.log, logs/mutants_table.log)
16 runs (8 mutants x 2 sites, both new test files each run): **13 killed, 3 survived.**
| Mutant | P1 getCertificationData | P2 getWalletNFTCertificates |
|---|---|---|
| M0 drop the guard (revert) | KILLED R1 R2 | KILLED R1 R2 |
| M2 constant -> `String(err)` | KILLED R1 R2 | KILLED R1 R2 |
| M3 rethrow only when unreadable | KILLED R1 R2 (by the rejected promise, not an assertion: `mintNFT` itself rejects because `classifyMintError` throws on the same value) | KILLED R1 R2 |
| M4 constant for every value | KILLED C1 | KILLED C1 |
| M5 rethrow every value after the log | KILLED C1 R1 R2 | KILLED C1 only (R1/R2 swallow the outcome) |
| M6 readable non-Error branch -> `'x'` | **SURVIVED** | **SURVIVED** |
| M7 log removed | KILLED C1 R1 R2 | KILLED C1 R1 R2 |
| M8 P1: `return null` -> `return undefined`; P2: always `return []` (drop the in-memory matches) | **SURVIVED (equivalent: `!certification` is true for both)** | **SURVIVED (real gap, G91-F3)** |
M6 is the known readable-non-Error gap (same as G90-F3, G74-F1 and the earlier gates); not changed by this PR. M3 at P1 is the instructive one: rethrowing the unreadable value does not reach the route as a clean failure, it makes `mintNFT` reject and the route answer 500, because `classifyMintError` has the identical unguarded read. That is why :810 and `classifyMintError` have to go together.

## 6. merge-tree (logs/merge_tree.log, merge_changed.log)
`git merge-tree --write-tree origin/develop pr1909`: **rc 0, clean**, tree `748a99db...`. Develop has not moved (`03977e89` at start, mid and end), so the merged tree is the PR tree; it differs from develop in **exactly the five PR paths**.

## 7. Kam's ks1346 logging rule
Both new lines log either the Error's own `message` (as the base lines did) or the constant `unreadable thrown value`. No thrown object, no field values, no stack, no keys of the thrown value are logged. Compliant. P1 keeps `certificationId` (a uuid already logged at base).

## FINDINGS / NOTES FOR THE PR BODY
- **G91-F1 (recommended, wording; fragment and likely the body)** The flow fragment says the scratch `resolves.toEqual([])` copy "is the 'returns the in-memory matches' claim above". It is not: with an empty in-memory store, `[]` is also what `return []` gives (my mutant M8 survives even that stronger assertion). The in-memory claim is true (the real route returned the seeded row, count 1, at head, probe wallet/proxy and wallet/getter) but no committed or scratch cell pins it. Reword to "resolves instead of rejecting", or add a seed row.
- **G91-F2 (info, reachability)** Neither value is reachable by an actor. P1: the URL is built from a zod-uuid `certificationId` and a fixed env-configured base; the rejection value is whatever Node's `fetch` rejects with (a `TypeError` with a `cause`, always an `Error`). P2: the rejection comes from `pg`, whose errors are `Error` subclasses (a lost socket is an ordinary `Error`). An unreadable one needs a wrapper/monkeypatch around fetch or the pool, or a test double. Defence in depth, like every KS-1868 site. All thrown values in the PR's cells and in my probe are synthetic.
- **G91-F3 (low, test gap, measured)** M8 on P2 (always return `[]`, dropping the in-memory matches) survives: the wallet file seeds no row, and R1/R2 discard the call's outcome (`.catch(() => undefined)`), which the author discloses. Optional: seed one in-memory record and assert `resolves` to it in R1 and R2 (scripts/probe_route.test.ts shows how).
- **G91-F4 (info, pre-existing, unchanged)** Any fetch failure in production, including an unreachable or erroring originate service, is reported as 404 "Certification not found", even though the route's own comment (KS-444/445) says an unavailable dependency is a 503. P1 does not widen this; it moves one unreachable input onto it. A separate card if Kam wants 503 for an originate outage.
- **G91-F5 (info)** `afterEach` restores with `process.env.NODE_ENV = savedEnv`; if `savedEnv` were undefined the string "undefined" would be stored (not the case under vitest: 'test'). Cosmetic.
- **G91-F6 (info, follow-ups, measured by grep at head)** Still unguarded in this service: `minting.service.ts:810` (mintOnCardano 'Real minting failed') and `utils/mintError.ts:37` (`classifyMintError`), which must be fixed in ONE pull request (guarding :810 alone turns today's resolved MINT_FAILED/400 into a `mintNFT` rejection and a route 500; M3 at P1 demonstrates the mechanism); the route catches `nft.routes.ts:116, 175, 215, 260, 291 ...` (13 more in that file), `cardano/index.ts:133`, `blockchain-verifier.service.ts:69, 109`, `ipfs.service.ts:487, 512`. `cardano/provider.ts:68` and the six merged `minting.service.ts` sites are guarded. Note `nft.routes.ts:260` (the GET /certificates route catch) is the route-level twin of P2: an unreadable value reaching it would still lose its log line, but after P2 it is no longer reachable from `getWalletNFTCertificates`.
- **G91-F7 (info)** the author's mail cites mintOnCardano at :798; at head it is :810 (the +12 from the two guards). Not a defect.
- **G91-F8 (info)** docs-fragments prints 2 ADVISORY lines at head; the author reports the same 2 at the untouched base (not re-run by me at develop).

## 8. Tier
Tier 2. The observable statuses move (400 -> 404, 500 -> 200) for inputs nobody can produce, onto the answers an ordinary error already gets; no auth, credential, chain write, credit, or persisted-data path changes (the same two upserts run; only an error string differs). Tier 1 would apply if either site had moved fail-closed to fail-open on a security decision; neither has (gate 90's rotate path did).

## 9. NOT TESTED
The live PR body text (no gh auth); a real PostgreSQL, originate service or `fetch` implementation (the originate fetch and pg are stand-ins; the real route and service code are real); a booted service (`app.ts` auth middleware was replaced by a stub that sets `req.user`); Node 24; the leg-16 typecheck checker (no nft baseline exists); the four platform suites; CI; the pre-push hook legs (quoted only from the mail); the mintOnCardano path with a real chain; the gateway consumers of the nft route (a 400 -> 404 change for the unreadable case could matter only to a caller that special-cases 400; not read); ESM/Windows. Spark shadow calibration was not run.
