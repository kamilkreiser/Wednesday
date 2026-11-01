# QA Gate 92 verdict: Secuura/Distributed_Secuura PR 1910 (KS-1868, mcp-server http-server.ts, nine route catches), TIER 2

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Tier 2 is right (log-only change, no status or body change, the only new outcome is for a value an ordinary Error never is). I ran the REAL Express 4 app over a real loopback socket (only api-client, hashing, package-generator and the shared guard replaced) at base and at head, 7 routes x 5 thrown values. An ordinary Error at base already logs its message and answers the route's constant 500; at head it is identical. An unreadable value (revoked Proxy, Error with a throwing `message` getter) gets NO response and an unhandled rejection at base on all 7 routes, and at head exactly what an ordinary Error gets (constant 500, log `unreadable thrown value`, 0 unhandled rejections). Existing pins ks1410 A/B and ks1901 are green at base and head; the :76 /hash catch is byte-untouched. The bundle that package-generator emits carries http-server.ts byte-equal to the file (and the helper with it). Every figure is Node v26.8.1, NOT Node 24.

## 1. Heads + diffstat (logs/head_start.log, logs/head_end.log, logs/ff.log)
- START and END (21:37Z / 21:48Z): `refs/pull/1910/head` = `9f00640d134b8e7b0602e4fd9840c87d06c8af9b` (equals READY mail), develop = `03977e89a343` (unchanged). Merge-base = develop tip, so the PR is a fast-forward of develop.
- Three-dot diffstat: 6 files, +668/-18, exactly the declared paths: http-server.ts (+9/-18), three new tests (207, 207, 204), a fragment pair (flow 21, cheat 20). Nothing else. PR body not read (no gh login); READY and BUILT AND PROVEN mails used (evidence/).
- Product sha256 at head `372c54a1...`; restored equal after every run (logs/summary.log).

## 2. The hunks (logs/product_diff.log)
Nine identical `-`/`+` pairs: the two lines `const message = err instanceof Error ? err.message : String(err);` + `console.error('[mcp-http] <route> failed:', message);` become `console.error('[mcp-http] <route> failed:', describeThrown(err));`. Sites: /register, /register-batch (outer), /verify, /verify-batch (outer), GET /documents, /workflow/:id, /connector, /policy, /generate-package. NOT changed: the 500 statements, their bodies, `if (!res.headersSent)` at /generate-package, the two batch item catches (already describeThrown, KS-1901), the helper, the :76 /hash catch (still reads `message` into its 500 body; KS-1928's class). The old read remains once in the file (:76), which is Q-D.

## 3. Behaviour (Q-A), run through the real routes (scripts/probe_real.test.ts via scripts/probe.sh; logs/probe_table.log, probe_base.json, probe_head.json)
Real `express` listening, real `fetch`, handlers real; stand-in api-client rejects with the value. 45 cells each side.
| value | base | head |
|---|---|---|
| ordinary Error (7 routes) | constant 500 (/verify `{verified:false,error:...}`), log = message | identical |
| revoked Proxy | NO RESPONSE (1.5 s client timeout), unhandled rejection 1, nothing logged | constant 500, log `unreadable thrown value`, 0 unhandled |
| Error with throwing message getter | as revoked Proxy | as above |
| thrown string `S3CR3T-STR` | 500, log prints the string itself | 500, log `non-Error string thrown` |
| thrown object `{secretField:'S3CR3T-VAL', other:1}` | 500, log `[object Object]` | 500, log `non-Error object thrown (fields: secretField, other)` |
- Q-A holds for all nine: /generate-package answered 500 only because `!res.headersSent` (headers not yet sent in the probe; untouched by the PR). The two batch OUTER catches are not reachable from a real request with this driver (the item catches take every api-client throw), so they are pinned only by the committed cells (req `body` getter throws): killed by every mutant below, but not run through Express (G92-F2).
- Unhandled rejection is counted in-process (vitest); on production Node >= 15 an unhandled rejection is process-fatal by default (read, not run).

## 4. Re-measure
- Head, whole mcp-server suite: **14 files, 131/131** (logs/head_suite.log; first run before `@secuura/shared` was built showed ks1232 failing on import only; after the build 131/131).
- Base product + the new tests: **27 failed, 104 passed**, all 27 `AssertionError` (6x`expected 200 to be 500` listed by the grep dedupe, 9x `to contain 'non-Error string thrown'`; R1/R2 = 18, R3 = 9); the 18 controls pass at base. 104 - 18 = 86 = the author's base suite. Suite 86 -> 131.
- Pins: ks1410 A, ks1410 B, ks1901, ks1868-hash, ks1893, ks1232 = **60/60 green at head**; ks1410 + ks1901 = **42/42 green at base** (Q-C).
- tsc including tests (scratch config scripts/tsc_lint.sh, extends the service config, includes src + tests): **0 errors before (21 files) and after (24 files)**; planted type error rc 2. eslint on http-server.ts + 3 tests: rc 0. (leg 16 does not cover mcp-server.)
- docs-fragments check: rc 0, "flow 117 legacy + 64 new, cheat 112 legacy + 64 new; lint clean, render passes"; the two ADVISORY lines (flow 6249, cheat 6235) are the hand-appended-content lines, same as gate 90 G90-F7, not from this PR. Planted unclosed `<div>` in the flow fragment: rc 1 "tags are not balanced"; restored sha-equal.
- Bundle (scripts/bundle.mts): ran the real `generatePackage` to a buffer, unzipped: `mcp-server/src/http-server.ts` is **byte-equal** to the source and contains `describeThrown` 12 times (definition + 11 calls); the helper is in the same file so it travels.

## 5. Mutants (scripts/mutants.py; product only, tests untouched, sha256 restored, `restore True`)
9 sites x 7 mutants = 63 runs over the 3 new files + ks1410 A/B + ks1901: **63 killed, 0 survived** (logs/mutants_table.log). M0 revert to inline read, M1 `String(err)`, M2 constant `'x'`, M3 log removed, M4 wrong prefix, M5 log raw `err`, M6 `(err as Error)?.message`. M3 is killed by BOTH the new file and the ks1410 pin of that route (the pin does its job). The author's nine one-hunk reverts are reproduced by M0.

## 6. merge-tree
Not run as `git merge-tree` (the fleet hook refuses it as a write verb). Not needed: merge-base equals the current develop tip `03977e89`, so the merge is a fast-forward and the result tree is the PR tree; `git diff --name-status origin/develop pr1910` lists exactly the six PR paths (logs/merge_paths.log).

## 7. Kam's ks1346 rule (Q-B)
Every new log line is `describeThrown(err)` with the existing prefix. For a non-Error it logs the kind (`non-Error string thrown`, `... null/number/... thrown`) or `non-Error object thrown (fields: <names>)`; no value of a field and no string content. Measured: `S3CR3T-STR` and `S3CR3T-VAL` appear in no head log line. This is strictly stricter than base, which printed a thrown string itself. An Error's message is logged unchanged (measured: `ordinary boom 10.0.0.7` at base and head). Loses nothing an operator needs: the route prefix and, for an Error, the message remain; what is lost is the content of a thrown STRING, which is the ruling (G82-F1). api-client and hashing throw only through fetch/fs (Errors); no repo code in this service throws a non-Error.

## FINDINGS / Notes for the PR body
- **G92-F1 (info; correction to the fragment's "not run" wording)** The flow/cheat fragments and the body say a real Express request was not run. Gate 92 ran it (45 cells each side): base no response + unhandled rejection on 7 routes, head constant 500. The PR body may say "confirmed by gate 92 through real Express 4".
- **G92-F2 (low, test gap, measured)** The two batch OUTER catches (/register-batch, /verify-batch) are exercised only through the handler-level cells (a `body` getter that throws). Mutants die on them, but no real-HTTP run reaches them (the item catches absorb api-client throws). Optional.
- **G92-F3 (info)** A thrown string's content is no longer logged (the intent). If an operator ever needs it, the fix belongs at the thrower, not the log.
- **G92-F4 (info, pre-existing, unchanged)** An Error's message is logged verbatim (can carry hosts/IPs). Not changed by this PR; same as base.
- **G92-F5 (info)** Reachability of an unreadable value in production is not shown (the values are test-authored); same as G82-F4/G90 reachability. The same-shape tool-level catches remain KS-1928 and :76 /hash remains a separate class (Q-D confirmed untouched).
- **G92-F6 (info)** Hook leg 14/16 "PREFLIGHT INCOMPLETE 13/16, nothing failed" is the author's quote; not re-run.

## NOT TESTED
Node 24; a booted production process (unhandled-rejection-fatal read from Node semantics, not run); the api-gateway hop to POST /generate-package; the real api-client network failure shapes; the real PR body text; the four platform suites; CI; the push hook legs; git merge-tree (hook-blocked, fast-forward argued instead).

## Method notes
Clone: copied gate 90's `.git` (its core.sshCommand already set, push disabled to `no_push_qa_gate`), fetched `refs/pull/1910/head`; the first direct clone was blocked by a path guard that mistook the read-only deploy-key argument for a write, so no override was used. Scratch moved to `_quarantine_2026-11-02/`. Untracked `tsconfig.gate92.json` is gate scratch in the clone only.
