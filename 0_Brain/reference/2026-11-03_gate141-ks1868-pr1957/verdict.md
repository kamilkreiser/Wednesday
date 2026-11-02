# QA Gate 141 verdict: Secuura/Distributed_Secuura PR 1957 (KS-1868, pool 'error' listener + ready-hook catch in five db.ts), TIER 2, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every figure the author claims re-measures except one pre-existing-error claim (3 nft-certificate tsc errors, not reproduced: G141-F5). The change is the same 16-line/-2 hunk in five `db.ts` (identical text, sha256 of the +/- lines equal across all five), nothing else in product code. I ran the real `db.ts` of each service, base and head, in a child process with only `pg`'s `Pool` replaced by an EventEmitter stand-in (gate 139's harness): 5 services x 3 sites x 12 values x 2 versions = **360 runs**, all rc 0, stderr empty. For an unreadable value, head equals what an ORDINARY Error already gets (one logged line, process lives, `initDb` resolves); base threw out of the emitter (uncaught exception) or made `initDb` reject / raised an unhandled rejection. **All five services behave identically** (72 cells, zero cross-service disagreement). Mutants: 110 runs, **90 killed, 20 survived** = the same two branches as gate 139 (null/undefined VALUE emitted, null MESSAGE), at all 10 sites: the test gap G139-F1 exists here too (G141-F1, recommended follow-up).
Not measured on Node 24 (host Node v26.8.1 throughout).

## Heads
- START (logs/head_start.log, 17:55:15Z): PR head `af9517f146fc64956c470f07aaaa9ddddc124775` (matches the author's), develop `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (= merge-base, one commit). END (logs/head_end.log, 18:09:34Z): both unchanged; clone HEAD `af9517f1`, `git status` clean (db_base copies, tsconfig.gate.json files moved to logs/_quarantine; product files sha256-restored after every run).
- PR #1956 (gate 139) is queued but had not merged into develop at either check; its four services (analytics, api-gateway, anchoring, kyc) are disjoint from these five, so no conflict is expected, but the merge-tree below is against today's develop only.
- **PR body not read** (no `gh` login); I used the author's READY mail (evidence/w19_pr1957_ready.txt) and the two fragments in the diff.

## 1. Diffstat (logs/diffstat.log)
12 files, +828/-10, exactly as declared: five `db.ts` 16/2 each (80/10), five tests 144/0 each (720), flow 11, cheat 17. Nothing outside the declared paths. The five +/- bodies hash identically (sha256 d9041abb...).

## 2. The hunks
Pool listener: `-  dbLog('error', 'DB pool unexpected error', { error: err.message });` `+  let reason: string | null | undefined; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } dbLog('error', 'DB pool unexpected error', { error: reason });`
Ready-hook catch: the same guard around `err?.message` in `runDbReadyHook` (message text, level, keys unchanged).
Does NOT change: log message text/level/other keys, `probeDb` (its `error: err?.message` is still unguarded: G141-F4), `initDb`'s return, `dbAvailable`, any query, transaction, route or response. The five db.ts files are otherwise textually identical (diff modulo service name and five comment lines).

## 3. Behaviour (Q1), RUN: logs/probe_matrix.jsonl, logs/probe_table.log (180 comparisons: 80 SAME, 100 DIFF, each DIFF listed), scripts/probe_child.ts
Values: ordinary Error, revoked Proxy, message getter throws, message 42, message undefined, message null, Symbol, object whose toString throws, object with toString 'custom-string', null, undefined, plain string. Positive control: ordinary and plain-string rows are SAME at every site and show a line (`error:"boom"`).

### Pool 'error' listener (identical in all five)
| emitted value | base | head |
|---|---|---|
| ordinary Error | 1 line `error:"boom"` | same |
| plain string | 1 line, `error` absent | same |
| revoked Proxy | **uncaughtException** (TypeError), no line | 1 line `"unreadable thrown value"` |
| message getter throws | **uncaughtException** | 1 line `"unreadable thrown value"` |
| null / undefined value | **uncaughtException** (TypeError "Cannot read properties of null") | 1 line, `error` absent |
| message 42 | `error: 42` (number) | `error: "42"` (string) |
| Symbol message | key absent | `"Symbol(s)"` |
| message obj, toString throws / returns text | `{}` / `{}` | constant / `"custom-string"` |
| message undefined / null | absent / `null` | absent / `null` (UNCHANGED) |
Availability flag: the listener never touches `dbAvailable`; `isDbAvailable()` equal at base and head in every cell.
Process outcome in production: **none of the five installs a process handler** (git grep `process.on(` over the five src trees, non-test: 0 hits; positive control: api-gateway/src/index.ts has 2 `uncaughtException` hits). So at base an uncaught listener throw ends the process by Node's default; at head the process lives.

### Ready-hook catch (boot path and retry-timer path both run)
| hook failure | boot base | boot head | retry timer base | retry timer head |
|---|---|---|---|---|
| ordinary Error | `initDb` true, 1 line | same | 1 line | same |
| revoked Proxy | **`initDb` REJECTS (TypeError)**, no line | true, 1 line constant | **unhandledRejection** | 1 line, no rejection |
| message getter throws | **REJECTS** | true, 1 line | **unhandledRejection** | 1 line |
| 42 / Symbol / toString objects | true; `42` / absent / `{}` | true; `"42"` / `"Symbol(s)"` / constant or text | same shape | same shape |
| null/undefined value thrown, null/undefined message, string | SAME | | SAME | |
`isDbAvailable()` is true in every hook cell at both versions (the probe set it before the hook ran): the hook never changes the flag.

### Who calls initDb (git grep, logs/callers.log; getPool has no caller outside db.ts) and what base did on an unreadable hook failure
- **nft-certificate** server.ts:42 `dbOk = await initDb(loadFromDb)` inside try/catch: base rejects, caught, `console.error('[NFT] Failed to initialize DB:', err)`, `dbOk=false`, boot continues and logs "in-memory fallback" although the DB flag was true; head: "connected", one DB line.
- **transfer** index.ts:1074 and **staking** index.ts:161 `initDb(...).then(...)` with NO catch and no process handler: base = unhandled rejection = Node default ends the process at boot (app.listen sits outside, but the process is gone); head logs the DB line and continues.
- **wallet-connector** server.ts:334 `.then(... app.listen ...).catch(...)`: base rejection lands in the catch and starts the app in "in-memory mode" (logs `{ error: err }` whole object, pre-existing); head takes the normal branch.
- **m365-integration** index.ts:1701 `await initDb(loadFromDb)` in `startup()`, which is awaited inside the async `app.listen` callback (index.ts:1759): base rejection = unhandled rejection from the listen callback, process ends by default and the "started" log is never reached; head continues.
- Retry-timer path (all five): base = unhandled rejection inside the timer callback, process ends; head logs. The author's note and fragment describe boot only (G141-F2).
Every head after-state equals the ordinary-Error after-state at every site. **Raise accepted.**

## Q2 transfer / wallet-connector money adjacency
Both services' diffs touch only `src/db.ts` (the two hunks above; diffstat and the hunk hash equal the other three) plus their own new test file. `approvalWorkflowService.ts` and `userErasedSubscriber.ts` are not in the diff (the 12 paths are listed in logs/pr_paths.log). No query text, transaction, persisted state, route or response changes; the only observable change is the log line (above) and that a process that used to die (listener, retry timer, transfer boot) now stays up on the same hostile input, behaving as for an ordinary Error. `isDbAvailable()` unchanged in every cell.

## Q3 null / undefined / non-string messages (measured, section 3 rows)
- message undefined / null: base == head (absent / `null`). Thrown null/undefined at the HOOK: SAME. At the LISTENER a null/undefined emitted value is a fix: base threw (uncaught), head logs a line without `error`.
- message 42: base logs the number `42`, head the string `"42"` (type change in the `error` field, disclosed by the author); Symbol: absent -> `"Symbol(s)"`.
- **TEST GAP: same as gate 139.** The nine cells per file are C1-C4 (ordinary at the listener, plain string, ordinary from the hook, thrown 42 from the hook) and R1-R5 (revoked Proxy + Symbol at the listener; revoked Proxy, getter-throws, Symbol from the hook). No cell emits a null/undefined VALUE to the listener, none uses a null MESSAGE, none uses message 42 (C4 throws the bare number 42, which has no message). Mutants M4 and M6 survive (section 5). Reported, not fix-before-merge: the fragment's claim that "the message itself when it is undefined or null" is kept is true (probe), and the base-throws-on-null listener fix is correct at head; only the pin is missing.

## 4. Re-measure
- Red first (new file only, product at develop `2d3b3bb3`; logs/red_base_new_<svc>.log): **5 failed | 4 passed (9) in each of the five**, every failure an `AssertionError` (5 each), 0 timeouts: 25 red, 20 control, as claimed.
- Green at head, whole suites (logs/head_whole_<svc>.log), each rc 0; base = new file moved out (logs/base_whole_excl_new_<svc>.log): nft-certificate 29 files/200 -> 30/209; transfer 9/120 -> 10/129; wallet-connector 9/61 -> 10/70; m365-integration 29/280 -> 30/289; staking 6/84 -> 7/93. +1 file, +9 cells each, nothing else moved, matches the author. Base product + new tests whole: 5 failed in each (the same five R cells), nothing else red.
- tsc with tests in the program (ad hoc tsconfig.gate.json, removed): head nft-certificate 0, transfer 0, wallet-connector **1**, m365-integration 0, staking 0; base the same (0/0/1/0/0; logs/tsc_{head,base}_<svc>.log). The wallet-connector error is `cardano-cip30.test.ts(8,32) TS6133 'vi' is declared but its value is never read`, present at base: the author's pre-existing claim holds. **The author's 3 nft-certificate `ipfs.service.ts` errors do NOT reproduce here (0 at base and head, shared package built)** (G141-F5). Each service's own tsconfig (tests excluded): 0 errors, all five.
- Ratchet: `test-types-ratchet.sh` default list rc 0 "OK - 5 service(s)" (auth, api-gateway, vc-issuer, security, m365-integration); `check.cjs services/m365-integration`: 0 errors, 0 baseline, 0 new. transfer, nft-certificate, wallet-connector and staking are in no ratchet (G141-F6).
- eslint on db.ts + new test per service: 0 problems rc 0 in all five; planted `no-debugger`/unused file: rc 1 in all five (logs/eslint_*).
- docs-fragments `check`: rc 0, "lint clean, render passes" (107 new). It prints the same cheat ADVISORY at committed line 6235 gate 139 saw (pre-existing, not from this PR). Planted: flow unclosed div rc 1, flow `<!--n-->.` removed rc 1, cheat unclosed div rc 1, cheat `</table>` corrupted rc 1; all restored by sha, rc 0 after.

## 5. Mutants (scripts/mutants.py; one site per run in the product only, tests untouched, sha256-restored and verified after every run: all restore True; logs/mutants_table.log)
110 runs (11 mutants x 5 services x 2 sites): **90 killed, 20 survived**, 0 timeouts, every kill an AssertionError.
| mutant | all 10 sites |
|---|---|
| M0 revert to unguarded read; M1 inner try dropped; M2 constant text; M3 no `String()`; M5 `String` for all (undefined -> "undefined"); M7 undefined -> text; M8 always constant; M9 catch rethrows; M10 log drops `error` | KILLED |
| **M4 `err?.message` -> `err.message`** | **SURVIVED at all 10** |
| **M6 null message -> text** | **SURVIVED at all 10** |

## 6. merge-tree onto develop `2d3b3bb3` (logs/merge_tree.log)
rc 0, tree `3da2cbac...`, clean; develop = merge-base (the PR is one commit on develop's tip), so the merged tree differs from develop in exactly the PR's 12 paths (path lists equal, logs/merged_vs_develop.log). Suites/fragments not re-run on the merged tree (identical to the head tree).

## 7. Kam's ks1346 rule (log type and field NAMES, never values), Q4
No new log line: both existing messages keep text, level and keys; only the value of `error` changes. The constant `'unreadable thrown value'` is a type statement: compliant. A readable message is still logged as before (pre-existing practice, same as sibling KS-1868 sites). `String(m)` on a readable non-string message logs a value; with a custom `toString` head logs its return (`"custom-string"`), where base logged `JSON.stringify` of the object (`{}` here, own fields in full if any), so head is no wider; a throwing `toString` falls to the constant. No stack, whole-object or secret field is introduced. Compliant relative to the existing pattern; info only. (Untouched and pre-existing: wallet-connector's `.catch` logs `{ error: err }` and nft-certificate's `console.error('...', err)` log whole objects; head makes the hook path stop reaching them.)

## 8. Notes for the PR body
- **G141-F1 (recommended follow-up, test gap, measured)** M4 and M6 survive at all 10 sites: no committed cell emits a null/undefined VALUE to the pool listener (base threw; head logs a line without `error`) or a null MESSAGE; no cell has an Error with readable non-string message 42 (the type change `42` -> `"42"` the PR discloses is unpinned). Same as G139-F1. One cell per file would close it. Not a merge block: the probe shows the behaviour correct and the PR makes no claim a cell contradicts.
- **G141-F2 (INFO, measured)** The retry-timer path (scheduleRetry) also ran the hook at base as an unhandled rejection in all five services; the fragment describes boot only. One sentence in the body.
- **G141-F3 (INFO, measured)** The head-vs-ordinary equivalence holds per service including the callers: nft-certificate head says "connected" where base said "in-memory fallback" for a hook failure with the DB up; wallet-connector no longer drops to the catch/"in-memory mode" banner for it; transfer, staking, m365 no longer die at boot. All toward the ordinary-Error outcome.
- **G141-F4 (INFO, follow-up, read from source)** `probeDb`'s `return { ok: false, error: err?.message }` is still an unguarded read in all five (db.ts:~116); a revoked-Proxy probe rejection would reject `initDb` at boot or stop the retry chain with an unhandled rejection. The author names `probeDb` as untouched; a KS-1868 site-list follow-up.
- **G141-F5 (INFO)** The 3 `ipfs.service.ts` tsc errors in nft-certificate are not reproduced in my clone (0 at base and head, `packages/shared` built). Probably an environment difference (stale or unbuilt shared dist on the author's side); no effect on the verdict, but "pre-existing" should be worded as "in the author's tree".
- **G141-F6 (INFO, follow-up)** Of the five services only m365-integration has a `tsconfig.test.json` and a ratchet baseline; no gate leg type-checks the tests of the other four (wallet-connector has the pre-existing 1 error), so the new test files in them are only compiled by vitest.
- **G141-F7 (INFO, style)** The guard preserves undefined/null as absent/null, unlike the develop admin.ts guard (`String(err.message)`), as in PR 1956 (G139-F6); intentional.

## 9. NOT TESTED
The live PR body; a real Postgres or pg pool (stand-in; a real pool 'error' emission path from an idle client is read, not run); a booted service (the callers' `.then`/`.catch`/try and the lack of process handlers are read; Node's default exit on an uncaught exception/unhandled rejection is not run to process exit); the tests' behaviour under CI load; BigInt and cyclic-object messages; `probeDb` unguarded read (read only); suites and fragments on the merged tree; the four platform suites; CI; the pre-push hook legs other than the ratchet leg; Node 24; the interplay with PR 1956 once it merges (disjoint paths, not run); Spark shadow review (not requested).

## Processes
All background runs I started (npm ci, shared build, probe matrix, suites, mutants, tsc, eslint, fragments) have finished; `ps` shows no process with this workdir in its command line.
