# QA Gate 82 verdict: Secuura/Distributed_Secuura PR 1897 (KS-1901 + KS-1893, services/mcp-server), tier 2

## BLUF
**GO WITH NOTES.** Every client-visible path in the touched catches now answers a constant; the author's numbers all re-measured. Red at base by assertion (31 failed = 28 new + the 3 edited cells), 36/36 new cells at head, suite 47/47 (9 files) to 83/83 (11 files), tsc over tests 0 errors, eslint 0, merge-tree clean, fragments check OK with a planted defect caught. The batch-500 defect is real at base and fixed at head. The one substantive note: **a thrown string is logged by VALUE**, which contradicts the PR's "non-Error logged by type and field names only, never values" claim (G82-F1); no cell pins it, and 2 of my 20 mutants (exactly that branch) survive. Three same-class sites outside the PR are ticket-worthy (G82-F2, F3, F4).

## Heads
- START (logs/head_start.log, 2026-11-01T12:50Z): PR head `07a4cc5be5e6c8637fdd553cfe67b4b5f9df2bee` (matches expected), develop `d7691f35312ea158f043e87a3227e477cccb183d`, head's single parent = develop tip.
- END (logs/head_end.log, 12:58Z): local `refs/gate/pr1897`, worktree HEAD and `ls-remote origin refs/pull/1897/head` all `07a4cc5b...`; develop `d7691f35...`. Unchanged.
- Diffstat (logs/diffstat.log, logs/namestatus.log): 9 files, +533/-16 as claimed (2 product M, 3 tests M, 2 tests A, 2 fragments A).

## FINDINGS
- **G82-F1 (MEDIUM, claim not met + test gap)** A thrown **string** is logged verbatim. `http-server.ts` describeThrown: `if (typeof err === 'string') return err;`; `tools/hash.ts` has the same line inline (`else if (typeof err === 'string') logged = err;`). Probe (logs/probe_hash_head.log, logs/probe_http_head.log): thrown `'S3CR3T-VALUE'` -> log `...item failed: S3CR3T-VALUE` on both batch routes and the hash tool. The PR text (flow fragment, code comments, test header) says a non-Error is logged by type and field names only, never values (KS 1346 ruling). A string is a non-Error value. The wire is safe (constant); this is the log only. No cell asserts the log for a string: A4 (string) asserts the response only, A4b/B4 assert the log only for an object. Mutants M3 (http) and M18 (hash) replace the string branch with `'non-Error string thrown'` and SURVIVE (53/53 pass, logs/mut_M3_*.log, logs/mut_M18_*.log). Fix is one line per site plus one log assertion each; or amend the wording to "strings are logged as is".
- **G82-F2 (MEDIUM, out of scope, same class, ticket)** `POST /hash` (`http-server.ts:75-77`) still answers 500 with `message: message`: the identical `ENOENT: no such file or directory, open '<path>'` text KS-1893 removes from the MCP tool, reachable over HTTP through client-supplied `filePath`. Pinned untouched by KS 1410 C2. Author listed it.
- **G82-F3 (MEDIUM, out of scope, same class, ticket)** `tools/register.ts:64,121-122`, `tools/verify.ts:45,87,139-141`, `tools/info.ts:58,108,166` still return thrown text (logs/candidates_other_tools.log). `register.ts:122` and `verify.ts:141` are the MCP-tool twins of KS-1901's batch per-item results (`results.push({ success:false, filePath, error: message })` shape). Same defect class, same fix.
- **G82-F4 (LOW, out of scope, read from source, not run)** The route-level catches (`http-server.ts:76,91,128,153,191,205,216,227,238,292`) still read `err instanceof Error ? err.message : String(err)` unguarded. An unreadable thrown value reaching one of them makes the catch itself throw. Express 4 does not catch async-handler rejections, so that is an unhandled rejection (process-fatal on Node >= 15). Not exercised by me; reachability needs a revoked Proxy or throwing getter coming out of the api client, unlikely. Same KS-1868 class; one ticket can cover F3 and F4.
- **G82-F5 (INFO)** hash.ts returns a second constant, `unreadable thrown value`, in the client result for an unreadable throw (KS-1868 convention, the task says constant only). It is a fixed string, leaks nothing, but is distinguishable from `An unexpected error occurred`.
- **G82-F6 (INFO)** `describeThrown` and the hash.ts inline copy agree branch for branch (Error, string, object, null/other, catch). Probe results over 21 hostile values are identical apart from the log prefix. Two copies can drift; M15/M5 style mutants on each are killed, so drift would be caught.
- **G82-F7 (INFO, client-visible change)** MCP clients can no longer tell ENOENT from EACCES from the tool or the batch items; stated by the author as a deliberate cost. No consumer in the repo reads it (section 5).
- **G82-F8 (INFO)** ks1410 C3 cells are source-text pins (`SRC.toContain(...)`), the pre-existing style. The edit makes them stricter, see section 1.

No HIGH. Nothing in this PR returns thrown text, errno, a `code` or the message to a client.

## 1. Pinned cells exactness (logs/exactness_hunks.log, logs/product_and_edited_diff.log)
- Pre-existing test files touched: exactly three (`git diff --name-status`): ks1410 part A, part B, ks1868. Hunk headers: part A `@@ -77,3 +77,6`, part B `@@ -77,3 +77,6` (each one hunk, inside C3 only), ks1868 `@@ -39 +39,3` and `@@ -43 +45` (both inside C1, lines 39-45). Every other line byte-equal: `git diff -U0` shows no other hunk.
- Intent kept, not loosened. C3 (A and B): was `toContain('results.push({ success: false, title: doc.title, error: message });')` and the verify twin; now `toContain(...error: '<CONSTANT>' })` for both pushes PLUS a new `expect(SRC).not.toMatch(/results\.push\(\{[^}]*error: message \}\)/)`. Three assertions where there were two, now pinning the opposite value: stricter. ks1868 C1: still `isError === true` and an exact `toEqual({ success:false, error: ... })`, only the expected value changed from `'disk gone'` to the constant. R1/R2 untouched. The new C3/C1 cells FAIL at base product (logs/base_red_all_headtests.log: the two C3 fail with `expected '#!/usr/bin/env node...' to contain 'results.push({ success: false, title:...'`, C1 fails with `error: 'disk gone'` vs the constant), so they discriminate.

## 2. Constant only: every response the touched catches produce
- `/register-batch` item catch: `{ success:false, title: doc.title, error:'An unexpected error occurred' }`. `/verify-batch` item catch: `{ verified:false, error:'An unexpected error occurred' }`. `doc.title` is the request's own title, not thrown text. Hash tool catch: `JSON.stringify({ success:false, error })` where `error` is only ever one of two literals (the constant, or `unreadable thrown value`); `logged` goes only to `console.error`.
- Measured: 21 hostile values through the hash tool and 21 x 2 routes through the handlers (42 cells): 42/42 status 200, 0 throws, the secret never in the wire body (logs/probe_http_head.log, logs/probe_hash_head.log, both `Tests` all passed). No errno, no `code`, no message in any answer. The hash result carries no `filePath` on failure.

## 3. Kam's ks1346 logging rule (logs/probe_*_head.log)
Hostile set (scripts/hostile.ts): revoked Proxy; Error with throwing `message` getter; plain objects with throwing getters on `message`, `name`, `constructor`; null-prototype object; Symbol; BigInt; objects whose `toString` / `Symbol.toPrimitive` throw; Proxy whose `ownKeys` throws; array; function; boolean; `{}`; an Error subclass with a secret message; an Error with a secret in a non-message field; a thrown string.
- No crash and no value of any non-Error OBJECT or primitive in any log line. Objects log as `non-Error object thrown (fields: a, b)` (names only, including `toString` / `toJSON` as names, and `0, 1` for the array), Symbol/BigInt/function/boolean as `non-Error <typeof> thrown`, unreadables as `unreadable thrown value`. No log argument is a non-string (the cells and my probe both assert no `<<object>>` placeholder).
- An Error's own `message` is logged (allowed). An Error's extra fields (`token`) are not logged.
- **The exception is G82-F1: a thrown string is logged as its value.**
- Line-for-line: describeThrown (`http-server.ts:41-50`) and hash.ts (`:41-46`) have the same four branches in the same order with the same strings; only the failure branch differs (hash.ts also sets `error`). Agree (G82-F6).

## 4. The batch-500 fix (logs/probe_http_base.log vs logs/probe_http_head.log, logs/base_red_all_headtests.log)
- Base (develop product, my probe): revoked Proxy, Error with throwing message getter, and null-prototype object thrown for one item each give **HTTP 500 for the whole batch** on both routes (`{"success":false,"error":{"code":"INTERNAL_ERROR",...}}`, the outer catch logs a TypeError text), so the other items' results are lost. The author's A5 cells fail at base with `AssertionError: expected 500 to be 200`.
- Head: same inputs give HTTP 200, `total` intact, the failing item `{...,error:'An unexpected error occurred'}`, neighbours unaffected (A3 and A5 pass; A5 asserts `[ok, failed, failed, ok]`). Bonus the author did not claim: at base a thrown Symbol/BigInt/string/Error subclass was copied into the 200 body (`"error":"Symbol(S3CR3T-VALUE)"`, `"123456789"`, `"S3CR3T-VALUE"`); at head all constant.
- Other route-level catches hiding something they used to surface? The outer catches (`:127`, `:190`) are not edited and already answered a constant before this PR. The only thing newly hidden is the per-item text, which is the point. The per-item failure now only goes to the log: an operator loses it from the response only (still in the log).

## 5. Callers (logs/callers_files.log, logs/callers_detail.log, logs/callers_openapi.log; grep over the whole head tree excluding node_modules)
- Hits for `register-batch|verify-batch|secuura_hash_document|registerHashTools|@secuura/mcp-server|services/mcp-server`: product callers are only `index.ts` (tool registration), `http-server.ts`, and `tools/*`. No other service imports mcp-server code; the api-gateway hits are `/api/verification/verify-batch`, a different layer. Docs and `MCP Deployment` mention the routes by name only; `openapi.yaml` and `mcp-server.openapi.ts` type the item error as an optional string, which a constant satisfies. No string match on `ENOENT` / `no such file` anywhere in mcp-server non-test source. The only tests reading old text are the 3 edited cells. Out-of-repo clients: not checkable.

## 6. Author's numbers re-measured
- Whole suite, mcp-server (`scripts/vt.sh`, vitest 4.1.12, Node v26.8.1): base (logs/base_whole.log) `Test Files 9 passed (9)`, `Tests 47 passed (47)`; head (logs/head_whole.log) `11 passed (11)`, `83 passed (83)`. Matches.
- Red at base by assertion (logs/base_red_all_headtests.log): head's 5 test files on develop product: 31 failed | 22 passed (53). 31 = 28 new + 3 edited. Per file (also logs/spark_gate.log facts): ks1901 20 of 26 red, ks1893 8 of 10 red, +1 each in the 3 edited files. All failures are `AssertionError` (list in the log: deep-equal, `expected 500 to be 200`, `to contain ...`), no import or compile errors. Matches "28 red / 8 green" and "20 of 26, 8 of 10". Base test files restored (logs/base_restored_status.log, clean).
- tsc: my config extends the package tsconfig minus the `__tests__` exclude, noEmit (scripts/tsconfig.gate82.json.head): 0 errors, rc=0, 11 files under `__tests__` in the program (logs/tsc_head_tests.log). Matches. (I did not run a planted type error on tsc.)
- eslint: ESLint 10.7.0 via Node API with cwd = Dev (the root config's globs are cwd-relative; CLI could not be used without a cd): 7 files, 0 errors, 0 warnings (logs/eslint_head.log). Positive control: a planted file raised `no-var` and `no-debugger`, rc=1 (logs/eslint_planted.log).
- Docs fragments: `docs-fragments.mjs check` on the head, rc 0, `flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes html_docs_check`, 2 ADVISORY (committed pages lag the render, by design, the same as gates 78 and 81) (logs/frag_check_clean.log). Planted `<div>` appended to the flow fragment: rc 1, `tags are not balanced: <div> opened 1, closed 0`, FAIL; restored by sha256 (logs/frag_check_planted_flow_div.log, `RESTORE_OK`).
- Fragment claims vs measured: 36 cells, 28 of 36, 20/26 and 8/10, 47 to 83, 9 to 11 files, 11 files under __tests__ in tsc: all confirmed. The fragment's "18 of 18 mutants" is the author's; mine are below.

### Mutants (mine; scripts/mutants.py, product files mutated in place and restored, sha256 equal after every run; per-run logs/mut_*.log, table logs/mutants_summary.log). 5 test files per run.
| Mutant | Result |
|---|---|
| M1 describeThrown object branch `String(err)` | KILLED (2 failed) |
| M2 describeThrown `Object.values` instead of keys | KILLED (2) |
| **M3 describeThrown string branch logs a kind, not the value** | **SURVIVED (53/53)** |
| M4 describeThrown catch rethrows | KILLED (2) |
| M5 describeThrown unreadable text changed | KILLED (2) |
| M6 register item catch rethrows | KILLED (9) |
| M7 verify item catch rethrows | KILLED (9) |
| M8 register constant replaced by `err.message` | KILLED (11) |
| M9 verify constant replaced by `String(err)` | KILLED (11) |
| M10 register log call removed | KILLED (4) |
| M11 verify log `console.error` to `console.log` | KILLED (4) |
| M12 register logs the raw `err` | KILLED (4) |
| M13 hash.ts `console.error` to `console.log` | KILLED (8) |
| M14 hash.ts returns `logged` instead of the constant | KILLED (8) |
| M15 hash.ts object branch `String(err)` | KILLED (1) |
| M16 hash.ts unreadable keeps its own constant dropped | KILLED (3) |
| M17 hash.ts inner catch rethrows | KILLED (3) |
| **M18 hash.ts string branch logs a kind, not the value** | **SURVIVED (53/53)** |
| M19 hash.ts `error` initialised from `err.message` | KILLED (7) |
| M20 hash.ts `isError: true` dropped | KILLED (11) |
Tally: 20 mutants, 18 killed, 2 survived (both G82-F1). The rethrow mutants (M4, M6, M7, M17) are killed because the handler call rejects in the cell, plus assertions; these are assertion/exception failures at run time, no compile error.

## 7. merge-tree
`git merge-tree --write-tree refs/gate/develop refs/gate/pr1897` (develop `d7691f35`, head `07a4cc5b`): **rc 0**, tree `2a3ecc32cf9e9d4be32a50e403720e02a535d8a4` (logs/merge_tree.log). Clean; head's parent is develop's tip.

## Out-of-scope CANDIDATES the author listed
POST /hash (`:60-77`, echoes the fs message with a path): same class, ticket (G82-F2). `tools/register.ts`, `verify.ts`, `info.ts`: same class, two of them the per-item batch results, ticket (G82-F3). The nine KS 1410 log lines with the unguarded read: same KS-1868 class, LOW (G82-F4). `tools/register.ts` and `verify.ts` lines were found by grep; I did not run them.

## Spark shadow calibration (evidence/spark_shadow/, logs/spark_gate.log, logs/spark_review.log)
- Tooling worked: `spark_gate.sh` rc 0 (head 53/53 passed; base product 22 passed / 31 failed, same as my run), `spark_review.py` rc 0, tunnel up. facts.json and review.json copied to evidence/spark_shadow/.
- Spark verdict **GO WITH NOTES: matches mine.**
- Its 7 findings (3 distinct claims, several repeated) are all `Note`: (a) 18/18 mutants, tsc and eslint, 47 to 83 are "unmeasured" because facts.json has only the targeted runs: true of the facts, not a defect of the PR; I measured all of them. (b) "28 red / 8 green does not match 22 passed / 31 failed": **false positive**, 31 = 28 new red + 3 edited cells that also fail at base; it did not reconcile the numbers. (c) "no test pins the 500 escape": **false**, cells A5 pin it and fail at base with `expected 500 to be 200`.
- Recall of my findings: **0 of F1-F4** (the string-value log, the `/hash` echo, the sibling tool echoes, the unguarded outer reads). It had no view of mutants or probes, and it did not catch the verified-wrong-claim in the PR text (G82-F1). Precision: 0 of its 3 distinct claims is a real defect. Verdict agreement is right for the wrong reasons. Calibration: useful as a deterministic facts run (its `targeted_base` 22/31 count is exactly the base red figure); its review cannot yet catch a claim-versus-code mismatch.

## NOT TESTED
A booted server or MCP client (handlers are called in process with mocked express/api client/hasher, same as the author). Clients outside the repo. The real api-client rejecting with exotic values. `docs[i] = null` in a batch (`doc.title` in the catch would throw; pre-existing, base and head identical by reading, not run). F4 reachability. tsc planted-error control. Node LTS (host Node is v26).

## Notes for the PR body (paste-ready)
- `describeThrown` and the hash.ts inline copy log a thrown **string** as its value (`if (typeof err === 'string') return err;` / `logged = err`). Either log it as `non-Error string thrown` (the KS 1346 rule) and add one log assertion per site, or reword "never values" to "never the values of an object". Mutants replacing that branch survive today.
- Verified at head 07a4cc5b: new cells red at base by assertion (28 of 36 plus the 3 edited cells = 31 failures), 36/36 at head, mcp-server suite 47 to 83, tsc over tests 0, eslint 0, merge-tree clean.
- Follow-up ticket (same class, not this PR): `POST /hash` echo, `tools/register.ts`, `tools/verify.ts` (incl. per-item batch results), `tools/info.ts`, and the unguarded read in the route-level catches.
