# QA Gate 150 verdict: Secuura/Distributed_Secuura PR 1966 (KS-1868, pool 'error' listener in prism, timestamping, security db.ts + prism ready-hook catch), TIER 2, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every figure the author claims re-measures. Product change is exactly the pool-listener guard in three db.ts files plus, in prism only, the runDbReadyHook catch; security touches its pool listener ONLY (its probeDb and hook catch were already guarded at base and are untouched). I ran the REAL db.ts of each service, base (4d1ab2cb) and head, in a child process with only pg's Pool replaced by an EventEmitter stand-in (gate 141's harness): 168 runs, all rc 0, stderr empty. For an unreadable value head equals what an ORDINARY Error already gets (one logged line, process lives, initDb resolves, availability flag unchanged); base threw out of the emitter (uncaught exception) or made prism's initDb reject / raised an unhandled rejection. Mutants: 44 runs, 36 killed, 8 survived = the same two branches as G139-F1/G141-F1 (null/undefined VALUE emitted, null MESSAGE) at all 4 sites. Not measured on Node 24 (host Node v26.8.1 throughout).

## Heads
- START (logs/head_start.log, 20:34:51Z): PR head `86986a55593878f21a4bb84c82ae58c256a68592` (matches), develop `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`. END (logs/head_end.log): both unchanged. The PR's parent and merge-base is `4d1ab2cb` (not develop's tip: develop has 4 newer KS-1868 commits, 2f9f7db3 .. 7ad0dcc1). "Base" below = 4d1ab2cb (the PR's parent); the three db.ts are byte-identical at 4d1ab2cb and the current develop for these paths (merge-tree changes exactly the PR paths, section 6).
- PR body not read (no gh login); the author's READY mail is in evidence/w20_pr1966_ready.txt and the two fragments are in the diff.
- Clone HEAD clean at the end (`git status` empty; gate tsconfigs moved to logs/_quarantine; db_base copies likewise; db.ts sha256-restored after every run).

## 1. Diffstat (logs/diffstat.log)
8 files, +424/-4 exactly as declared: prism db.ts 16/2, timestamping 8/1, security 8/1; tests 146 + 108 + 110; flow 11, cheat 17. Nothing outside the declared paths.

## 2. The hunks (logs/hunks.diff)
Listener (all three): `-  dbLog('error','DB pool unexpected error',{ error: err.message });` `+  let reason: string|null|undefined; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } dbLog(... { error: reason });` Note the optional chain: a null/undefined emitted value is now readable too.
Prism ready hook: `err?.message` unguarded read replaced by the same guard (text, level, key unchanged).
Does NOT change: log text/level/other keys, probeDb (prism and timestamping probeDb still `error: err?.message`, unguarded: G150-F3), initDb return, dbAvailable, any query, transaction, route or response. SECURITY: the diff of services/security/src/db.ts is the listener hunk only (+8/-1); the file's hook catch (db.ts ~103-118) and probeDb (~121-135) already carried the guard at base and are not in the diff. No key, credential or tenant path is read or written by the changed lines.

## 3. Behaviour (RUN: logs/probe_matrix.jsonl, logs/probe_table.log (84 comparisons: 48 SAME, 36 DIFF, each DIFF listed), scripts/probe_child.ts)
Values: ordinary Error, revoked Proxy, message getter throws, message 42, message undefined, message null, Symbol, object whose toString throws, object with toString 'custom-string', null, undefined, plain string. Sites: pool listener (3 services), ready hook at boot and via the retry timer (prism, security). Positive control: ordinary and plain-string rows SAME everywhere and show a line (`error:"boom"`). The child chdir'd to logs/cwd (production-mode loggers write logs/ relative to cwd): the dbLog is console.log(JSON), no logger wrote any file; logs/cwd is empty and no `logs/` dir appeared in any service dir.

### Pool listener (prism, timestamping, security: identical)
| emitted value | base | head |
|---|---|---|
| ordinary Error | 1 line `error:"boom"` | same |
| revoked Proxy | **uncaughtException** (TypeError), no line | 1 line `"unreadable thrown value"` |
| message getter throws | **uncaughtException** | 1 line, constant |
| null / undefined value | **uncaughtException** (TypeError reading 'message') | 1 line, `error` absent |
| message 42 | `error: 42` (number) | `"42"` (string) |
| Symbol message | key absent | `"Symbol(s)"` |
| message object, toString throws / returns text | `{}` / `{}` | constant / `"custom-string"` |
| message undefined / null / plain string | unchanged | unchanged |
Availability flag: the listener never touches dbAvailable; isDbAvailable() is equal at base and head in every cell (false in pool cells since no probe ran). Process lifetime: no uncaughtException/unhandledRejection handler exists in prism or security src (git grep `process.on(` non-test: 0 hits; timestamping only SIGTERM/SIGINT, index.ts:904-905), so at base the listener throw ends the process by Node's default; at head it lives.

### Prism ready-hook catch (boot path and retry-timer path both run)
| hook failure | boot base | boot head | retry timer base | retry timer head |
|---|---|---|---|---|
| ordinary Error | initDb true, 1 line | same | 1 line | same |
| revoked Proxy | **initDb REJECTS (TypeError)**, no line | true, 1 line constant | **unhandledRejection** | 1 line, none |
| message getter throws | **REJECTS** | true, 1 line | **unhandledRejection** | 1 line |
| 42 / Symbol / toString objects | true; `42` / absent / `{}` | true; `"42"` / `"Symbol(s)"` / constant or text | same shape | same shape |
| null/undefined thrown, null/undefined message, string | SAME | | SAME | |
isDbAvailable() true in every hook cell at both versions: the hook never changes the flag.
Security hook rows: 24 of 24 SAME (already guarded at base). Timestamping has no hook.

### Prism boot caller, index.ts:891 `initDb(loadFromDb).then((connected) => {...})`, no catch, no process handler
Base, unreadable hook failure: initDb rejects -> unhandled promise rejection -> Node's default (process ends); the `connected=` line and the production `process.exit(1)` check never run, `app.listen` (outside the chain) has already been called, so the process is up briefly then gone. Retry-timer path: the same unhandled rejection from the timer callback. Head: initDb resolves true, the DB line is logged, `.then` runs, process lives = the ordinary-Error outcome. (Run: initDb rejection and the unhandledRejection capture in the probe; Node's actual exit is read, not run.)
Other callers: security index.ts:2237 `initDb(runDbBootTasks).then(...)` (no catch; unaffected, its hook was guarded at base); timestamping index.ts:846 `await initDb()` in startup() inside the listen callback (no hook, flow unchanged; the listener fix only keeps the process up on a pool 'error').

### Q: class bar
For every site and value class, head's after-state (process lifetime, availability flag, logged line, initDb resolution) equals the ordinary-Error after-state. **Raise accepted** at all four sites.

## 4. Re-measure
- Red-first (new file only, product at base 4d1ab2cb; logs/red_base_new_<svc>.log): prism **5 failed / 4 passed (9)**, timestamping **3 / 2 (5)**, security **3 / 2 (5)**: 11 red, 8 controls, every red an AssertionError (5/3/3), 0 timeouts: as claimed.
- Whole suites (--maxWorkers=2; logs/head_whole_*, base_whole_excl_new_*, base_plus_new_whole_*): prism 4 files/30 -> 5/39; timestamping 9/100 -> 10/105; security 48/465 -> 49/470, all rc 0, matches the author. Base product + new test whole: only the 11 R cells red, nothing else.
- tsc with tests (ad hoc tsconfig.gate.json, moved out after): prism 0 / 0, security 0 / 0, timestamping **59 / 59** (identical error lists base vs head, all in ks1404-pki.ts and ks1404-verify-rfc3161.test.ts, none in db.ts or the new test; the author's "59 before and after" reproduces). Own tsconfig (tests excluded) for timestamping: 0.
- eslint on db.ts + new test per service: rc 0 in all three; planted `no-debugger`/unused: rc 1 in all three (logs/eslint_*).
- docs-fragments `check`: rc 0 "lint clean, render passes"; the same cheat ADVISORY at committed line 6235 as in gates 139/141 (pre-existing). Planted: flow unclosed div rc 1, flow `<!--n-->.` removed rc 1, cheat unclosed div rc 1, cheat `</table>` corrupted rc 1; all restored by sha; rc 0 after (logs/frag_*).
- The author's `--maxWorkers=2` caveat is credible: my runs at that setting were clean (one mutant run hit a single 5000 ms C1 timeout under load and was still killed by assertions).

## 5. Mutants (scripts/mutants.py; one site per run in the product only, tests untouched, sha256 restored and verified after every run: all True; logs/mutants_table.log)
44 runs (11 mutants x 4 sites: prism listener, prism hook, timestamping listener, security listener): **36 killed, 8 survived**, every kill by AssertionError.
| mutant | result |
|---|---|
| M0 revert to unguarded; M1 inner try dropped; M2 constant text; M3 no String(); M5 String for all; M7 undefined -> text; M8 always constant; M9 catch rethrows; M10 log drops error | KILLED at all 4 sites |
| **M4 `err?.message` -> `err.message`** | **SURVIVED at all 4** |
| **M6 null message -> text** | **SURVIVED at all 4** |
No committed cell emits a null/undefined VALUE to the listener, a null MESSAGE, or an Error with readable non-string message 42 (see G150-F1).

## 6. merge-tree onto develop `7ad0dcc1` (logs/merge_tree.log)
rc 0, tree `5ac6fddd2610...`, clean. The merged tree differs from develop in exactly the PR's 8 paths (logs/merged_vs_develop.log equals logs/pr_paths.log). Suites/fragments not re-run on the merged tree.

## 7. Kam's ks1346 rule
No new log line: both messages keep text, level and keys; only the value of `error` changes. The constant is a type statement: compliant. A readable message is logged as before; String(m) of a custom-toString message logs its text where base logged `{}`/JSON of the object, so head is no wider. Info only.

## 8. Notes for the PR body
- **G150-F1 (recommended follow-up, test gap, measured)** Mutants M4 (`err?.message` -> `err.message`) and M6 (null message -> text) survive at all 4 sites (same as G139-F1/G141-F1): no cell emits null/undefined to the listener (base threw uncaught, head logs a line without `error`), uses a null message, or a message 42 (`42` -> `"42"` type change is unpinned). One cell per file closes it. Not a merge block; the probe shows the behaviour correct.
- **G150-F2 (INFO, measured)** The prism retry-timer path also ran the hook at base as an unhandled rejection; the fragment mentions it ("on the background retry path, the timer callback rejected"), so this is already disclosed.
- **G150-F3 (INFO, follow-up, read from source)** prism and timestamping `probeDb` still `return { ok:false, error: err?.message }` unguarded (security's is guarded). A revoked-Proxy probe rejection would reject initDb at boot (prism index.ts:891 unhandled; timestamping startup() inside the listen callback) or stop the retry chain. The PR says probeDb is untouched; KS-1868 site-list follow-up.
- **G150-F4 (INFO)** Prism caller consequence: with base, a hostile hook failure in production meant an unhandled rejection at index.ts:891 before the "connected=" check (which would also `process.exit(1)` if the flag were false); head reaches it. Direction is toward the ordinary-Error outcome.
- **G150-F5 (INFO, wording)** The PR is built on 4d1ab2cb, not on current develop (4 newer commits, none touching these paths); merge-tree is clean.
- **G150-F6 (INFO, security)** Hunk is the pool listener only; the availability flag (isDbAvailable, read by adminScope.ts and ~15 index.ts guards) is not written by it and was equal at base and head in every cell. No credential, key or tenant path is touched.
- **G150-F7 (INFO, style)** Guard keeps undefined/null as absent/null, unlike develop admin.ts (`String(err.message)`); intentional, as in PRs 1956/1957.
- **G150-F8 (INFO, tsc)** Timestamping's 59 with-tests tsc errors are pre-existing (ks1404 test helpers, implicit any); no ratchet covers timestamping or prism.

## 9. NOT TESTED
The live PR body; a real Postgres or pg pool (stand-in; a real idle-client 'error' emission is read, not run); a booted service and Node's actual process exit on an uncaught exception / unhandled rejection (read, with the absence of handlers grepped); the tests under CI load or default workers; BigInt and cyclic-object messages; probeDb unguarded reads (read only); suites/fragments on the merged tree; the four platform suites; CI; the pre-push hook legs; Node 24; Spark shadow review (not requested).

## Processes
Every background run I started (npm ci, shared build, probe matrix, suites, mutants) has finished; two aborted suites.sh starts (bash 3.2 associative array) were killed and the clone verified clean before the rerun. `ps` shows no process with this workdir in its command line. No log file landed outside logs/; logs/cwd is empty.
