# QA Gate 151 verdict: Secuura/Distributed_Secuura PR 1967 (KS-1868, demo-service src/routes/state.ts: Redis 'error' listener + presenter-mode catch), TIER 2, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every figure the author claims re-measures. I ran the REAL routes/state.ts (base and head) behind a real Express 4.22.3 server, the real winston logger in NODE_ENV=production, with only ioredis replaced (a counting stand-in, preload), one child process per cell: 40 runs, all rc 0. For an unreadable value head's after-state equals an ORDINARY Error's after-state at base, at both sites. At base an unreadable value in the listener threw out of the emitter AND left the dead client in use for the life of the process (every later POST /presenter-mode 500s, GET falls back to the in-memory object); a hostile value in the presenter-mode catch left the request unanswered with an unhandled rejection (demo-service has no unhandledRejection handler, so Node's default ends the process: read). Head: no throw, client replaced exactly as for an ordinary Error, 500 body sent. Mutants: 18 run, 14 killed, 4 survived (redis = null removal/relocation, and the 'Unknown error' text at both sites): see G151-F1/F2. Not measured on Node 24 (host Node v26.8.1 throughout). Dependencies installed with `npm install --no-package-lock` (see section 4), not `npm ci`.

## Heads
- START (logs/head_start.log, 21:1xZ / 08:1x AEDT): PR head `118cf6d972e5723284c5270a66cc7337027ef6e0` (matches), develop `b85b7b6786fa6329b6f781cebf2475147738004e`. END (logs/head_end.log, 21:25:40Z): both unchanged.
- Merge-base and PR parent = `2f9f7db3` (develop has since moved: 7ad0dcc1 .. b85b7b678 = PR 1966). "Base" = 2f9f7db3; state.ts is byte-identical at 2f9f7db3 and at current develop (checked: `git show` diff empty).
- PR body not read (no gh login); the READY mail is in evidence/w20_pr1967_ready.txt.
- Clone left clean (`git status` empty); gate scratch (state_base.ts copy, tsconfig.gate.json) moved to logs/_quarantine; state.ts sha256 restored after every swap (59194ccf...).

## 1. Diffstat (logs/diffstat.log, three-dot vs develop)
4 files, +194/-2 exactly as declared: state.ts +13/-2; new test 153; flow fragment 11; cheat fragment 17. Paths: Blockchain/Dev/services/demo-service/src/{routes/state.ts, __tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts}, Projects Documents/fragments/{flow,cheat}/KS-1868-demo-service-state.html. Nothing outside.

## 2. The hunks (logs/hunks.diff)
Listener (getRedis, line 43): `-  logger.warn('Redis unavailable, using in-memory state', { error: err.message }); redis = null;` becomes `let message: string; try { message = err instanceof Error ? err.message : 'Unknown error'; } catch { message = 'unreadable thrown value'; }` then the SAME logger.warn with `{ error: message }`, then `redis = null`.
Presenter-mode catch (line 112): `const message = err instanceof Error ? err.message : 'Unknown error';` becomes the same try/catch; the logger.error call, the 500 status and the JSON body are unchanged lines.
Does NOT change: the log texts and levels, the 500 body, getRedis creation/options (retryStrategy null, maxRetriesPerRequest 1), GET /state (its catch already carried the guard at base, lines 86-95, not in the diff), inMemoryState, any route or response shape.
Two behaviour changes beyond the unreadable class, both disclosed by the author: (a) the listener now uses the `instanceof Error` form, so a non-Error value reaching it (string, number, plain object, null, undefined) logs `Unknown error`: at base a string/number left the field out (undefined), a plain object {message:'x'} logged 'x', null/undefined threw; (b) nothing else. The plain-object-with-message row is NOT in the author's list (G151-F4).

## 3. Behaviour (RUN: scripts/probe_child.ts + stub_ioredis.js + run_cell.js; logs/probe_matrix.jsonl, logs/probe_table.log)
Harness: a bare Express 4.22.3 app mounting the real stateRouter, a real HTTP client (fetch, 1.2 s abort for "no response"), REDIS_URL set, NODE_ENV=production (winston JSON console). The ioredis stand-in counts constructions, shares one key store, marks a client dead after its error is emitted (commands then reject "Connection is closed.", as a client with retryStrategy null does: read, not run against real ioredis) and can make set() reject any value. Child cwd = logs/cwd; winston here is console-only (utils/logger.ts) and no file landed anywhere (logs/cwd empty). Kinds: ordinary Error, revoked Proxy, message getter throws, null, undefined, string, number, plain object {message:'x'}, Error with Symbol message. Mode "listener": N cycles of GET /state, POST /presenter-mode {enabled:true}, then emit the kind to the live client's error listener; mode "catch": N POSTs whose set() rejects the kind (client healthy).

### Q1 (the author's): what does `redis = null` do to the demo state route?
getRedis is called by exactly two routes (git grep: state.ts lines 69 GET /state, 110 POST /presenter-mode). With redis cleared and REDIS_URL set the next request builds a NEW client (`new Redis(url, ...)`), with no REDIS_URL getRedis returns null before the listener can ever exist and the in-memory object answers.

| listener, N=20 (and N=500 for Error/revoked) | clients built | listener threw | uncaught | warn lines | state after |
|---|---|---|---|---|---|
| base, ordinary Error | 21 (N=500: 501) | 0 | 0 | 20 (500) `error:"boom"` | presenterMode true, requests 200 |
| head, ordinary Error | 21 (501) | 0 | 0 | 20 (500) | same |
| base, revoked Proxy / getter / null / undefined | **1** (stays 1 at N=500) | **N of N** (emitter would raise uncaughtException; my child caught it) | n/a | **0** | dead client reused: first POST 200, every later POST **500**, GET falls to in-memory (presenterMode false although Redis holds true); never recovers until restart |
| head, revoked Proxy / getter | 21 (501) | 0 | 0 | 20 (500) `error:"unreadable thrown value"` | identical to the ordinary-Error row: POST 200, GET presenterMode true |
| head, null / undefined / string / number / plain object | 21 | 0 | 0 | 20 `error:"Unknown error"` | identical to the ordinary-Error row |
Client growth: exactly one new client per error cycle (== requests that follow an error), the same at base and head for an ordinary Error; no unbounded growth beyond that, and head for an unreadable value grows exactly like an ordinary Error at base. Nothing in the listener path calls quit()/disconnect() on the replaced client at either version (read): the old client is left to end itself (retryStrategy returns null); an ioredis connection attempt per request while Redis is down is the existing, deliberate fallback behaviour (code comment "Do not retry"), unchanged by this PR. The statement "next request builds a new client" is therefore a behaviour of ordinary errors too; head makes the unreadable class equal to it (and removes the permanent dead-client state at base).
Presenter-mode state: head unreadable == head/base ordinary in every listener row (GET presenterMode true after the POST).

### Q2: the presenter-mode catch (set() rejects the value; client healthy; N=3)
| value | base | head |
|---|---|---|
| ordinary Error | 500 + exact body, 1 log line `error:"boom"` per call | same |
| revoked Proxy, message getter throws | **no response (timeout), unhandledRejection x3**, no log line | 500 + exact body x3, log `error:"unreadable thrown value"`, 0 unhandled |
| null / undefined / string / number / plain object | 500, `Unknown error` | same (unchanged) |
| Symbol message | 500, `error` field absent | same (unchanged) |
Final GET after the POSTs: 200 with presenterMode false in every row (the write never landed in the in-memory object, since a client existed). Confirmed: the HTTP response for the ordinary Error is constant `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"Internal server error"}}` at base and head; the only difference between base and head at this site is for a value whose message read throws (rows 2): response sent vs hung request. Nothing else differs (the diff is the message read; status/body lines are not in it).
Consequence at base is READ: Express 4.22.3 does not forward an async handler's rejection (measured above: no response), demo-service registers no `process.on('unhandledRejection'|'uncaughtException')` (logs/process_handlers.log: only SIGTERM/SIGINT, src/index.ts:84-85), so Node's default ends the process. Not run on a booted service.

### Demo-only status (read)
The code says so: src/middleware/demoGuard.ts header ("demo-service mints REAL platform tokens ..."), `assertDemoServiceEnabled()` is called at boot from src/index.ts:41 and throws on NODE_ENV=production ("demo-service must never run in production") and on an unset NODE_ENV, and requires DEMO_SERVICE_ENABLED=true plus a key of 16+ chars; the header also records that nothing routes /demo-api/ today. So this is not a production path; the PR touches no token, persona, reset or credential code (state.ts holds persona NAME and presenter flag only).

### Class bar
For every value class and both sites, head's after-state (response, client count, process lifetime, presenter-mode state, logged line) equals the ordinary-Error after-state. **Raise accepted.**

## 4. Re-measure
- Install: `npm ci` fails on this develop (lock/package out of sync: @harmoniclabs/crypto 0.2.5 vs 0.3.1, logs/npm_ci.log; pre-existing, not this PR). I used `npm install --no-package-lock --ignore-scripts --workspace=services/demo-service --workspace=packages/shared --include-workspace-root` (logs/npm_install.log), then built packages/shared (rc 0). Resolved versions: vitest 4.1.12, ioredis 5.11.1, express 4.22.3. Tool versions may differ from the lockfile's.
- Red-first (new file only, product at base; logs/red_base_new.log): **4 failed / 2 passed (6)**, every failure an AssertionError (R1/R2 "expected { threw: true } to deeply equal { threw: false }", R3/R4 "expected true to be false"), 0 timeouts; the 2 controls C1/C2 pass. As claimed.
- Green at head: 6 of 6; whole service suite (--maxWorkers=2, --root anchored): head **14 files / 103 cells, rc 0** (logs/head_whole.log); base product + new test: 13 passed / 1 failed file, 99 passed 4 failed of 103 (logs/base_plus_new_whole.log) = the 4 R cells only, so the base suite is 13 files / 97 cells (99 minus the 2 controls) as claimed: 97 -> 103.
- tsc: service tsconfig (tests excluded) rc 0, 0 errors at head (logs/tsc_own_head.log). With tests (ad hoc tsconfig.gate.json, quarantined after): **25 errors at base and 25 at head, the same set** (diff of the sorted error lists empty), none in state.ts or the new test (logs/tsc_tests_*.log). The author's 25/25 reproduces.
- eslint (run with cwd = demo-service so the flat config's file globs apply; scripts/eslint_run.js): state.ts + new test rc 0, no output (logs/eslint_head.log); planted `debugger;` + unused const in state.ts: rc 1 (no-debugger error + no-unused-vars warning), restored by sha (logs/eslint_planted.log).
- docs-fragments check (Blockchain/Dev/scripts/docs-fragments.mjs check --root repo; scripts/frag.sh): clean rc 0 "lint clean, render passes" with the same pre-existing cheat ADVISORY at committed line 6235 as gates 139/141/150. Planted: flow unclosed div rc 1; flow `<!--n-->.` removed rc 1; cheat unclosed div rc 1; cheat `</table>` corrupted rc 1; every restore verified by sha; rc 0 after (logs/frag_*.log, logs/frag_run.log).
- Fragment claims checked against runs: "+13/-2", "4 of 6 red by assertion", "13/97 then 14/103", "25 at both", the dead-client and unhandled-rejection statements, and "a string, a number, null, undefined logs Unknown error where it left the field out or threw" all hold (string/number: absent at base; null/undefined: threw).

## 5. Mutants (scripts/mutants.py; one change per run in state.ts only, tests untouched, sha256 restored and verified after every run: all True; logs/mutants.jsonl)
18 runs: **14 killed (every kill an AssertionError), 4 survived.**
| mutant | result |
|---|---|
| L0 revert listener to unguarded; L1 inner try dropped; L2 constant text; L3 catch rethrows; L6 instanceof inverted; L7 always constant; L9 log line dropped | KILLED (R1/R2, C1) |
| P0 revert catch; P1 try dropped; P2 constant text; P3 catch rethrows; P4 always constant; P5 instanceof inverted; P7 log line dropped | KILLED (R3/R4, C2) |
| **L4 `redis = null` removed** | **SURVIVED** |
| **L5 `redis = null` moved inside the try (skipped when the read throws)** | **SURVIVED** |
| **L8 listener `'Unknown error'` text changed** | **SURVIVED** |
| **P6 catch `'Unknown error'` text changed** | **SURVIVED** |
L4/L5 are the author's gate question itself: the new tests only assert the listener does not throw and what it logs, never that the client is replaced. My probe (client count 1 vs 21) does catch both, the committed tests do not.

## 6. merge-tree onto develop `b85b7b67` (logs/merge_tree.log, scripts/mt.sh)
rc 0, tree `0567b363eaa6...`, clean. The merged tree differs from develop in exactly the PR's 4 paths (logs/merged_vs_develop.log equals logs/pr_paths.log). Suites/fragments not re-run on the merged tree (develop's state.ts equals the PR's base).

## 7. Kam's ks1346 logging rule
No new log line. The listener and catch keep their texts, levels and keys; only the value of `error` changes, and it is either the message of a real Error (as before) or one of two constants ('Unknown error', 'unreadable thrown value') = type statements, never a thrown object's values. Compliant. Head is narrower than base in one case: a plain object's `message` ('x') is no longer logged (G151-F4).

## 8. Notes for the PR body
- **G151-F1 (recommended follow-up, test gap, measured)** Mutants L4 and L5 survive: no committed cell asserts that the Redis client is cleared after the error (i.e. that the next request builds a new client), which is the behaviour the PR exists to restore for the unreadable class. One cell closes it: emit R1's revoked Proxy, call `run('/state', {})` again and assert a second stand-in client was constructed (counter in the existing class stand-in). Not a merge block; the probe shows the behaviour correct (clients 1 -> 21 at N=20, equal to an ordinary Error).
- **G151-F2 (INFO, test gap, measured)** L8/P6 survive: the `'Unknown error'` constant (new in the listener, the stated non-Error behaviour change) is pinned nowhere; a cell emitting a string to the listener and a string rejection to presenter-mode would pin it.
- **G151-F3 (INFO, measured, answer to the author's gate question)** `redis = null` makes the next request build a new client; ordinary Error: +1 client per error cycle at base and head (N=500: 501 clients, no other growth). Before this PR an unreadable value never reached `redis = null`: one dead client stayed in use forever (POST /presenter-mode 500 for every later call, GET silently served the in-memory object while Redis held a different value). Head ends that; the per-request reconnect while Redis is down is the existing retryStrategy-null design, unchanged and equal to the ordinary-Error behaviour.
- **G151-F4 (INFO, disclosure gap)** The listener's non-Error behaviour change also covers a plain object with a `message` field: base logged its message ('x'), head logs `Unknown error`. The PR text lists string/number/null/undefined but not this row (and the Symbol-message row is unchanged: field absent at both). A listener only ever receives what ioredis emits, which is an Error in practice (read, not run), so the practical effect is nil.
- **G151-F5 (INFO, consequence read)** At base the presenter-mode catch throw is an async-handler rejection under Express 4.22.3 with no unhandledRejection handler (src/index.ts registers SIGTERM/SIGINT only): request hangs and Node's default ends the process; measured: no response + 3 rejections; process exit read, not run.
- **G151-F6 (INFO, scope)** demo-service is demo-only by code (demoGuard.ts; boot refuses NODE_ENV=production or unset; index.ts:41). No token, persona, reset or credential path is touched.
- **G151-F7 (INFO, wording)** PR is built on 2f9f7db3, develop has moved to b85b7b678 (PR 1966); state.ts unchanged between them, merge-tree clean.
- **G151-F8 (INFO, tooling)** `npm ci` fails on develop's lockfile (pre-existing, @harmoniclabs/crypto); this gate used `npm install --no-package-lock`. Worth a separate ticket if CI does not hit it.
- **G151-F9 (INFO, follow-up)** The same listener, once the value is readable, still passes `err.message` of a real Error unmodified (a message that is a number or Symbol is passed through as that type; Symbol message drops the field in the JSON logger). Unchanged by this PR and the same as G150's note on type changes.

## 9. NOT TESTED
The live PR body; a real Redis or real ioredis (stand-in; the dead-client behaviour after retryStrategy null is read, not run); a booted demo-service and Node's actual exit on an unhandled rejection (read, with the absence of handlers grepped); the real error-event emission by ioredis for a hostile value (a real client only emits Errors; the hostile row is a synthetic value); a request concurrent with the error emission (client in flight); BigInt/cyclic-object messages; whole suite and fragments on the merged tree; the four platform suites; CI; the pre-push hook legs; Node 24; lockfile-pinned tool versions (see section 4); Spark shadow review (not requested).

## Processes
npm install, shared build, probe cells, suites and mutants all ran in the foreground or finished; the failed first `npm ci`/build chain I backgrounded ended itself (rc 1 in logs). `ps` shows no process with this workdir in its command line. No log file landed outside this workdir (logs/cwd empty; winston here is console-only); the pre-existing /Volumes/DevMASTER/WEDNESDAY/logs files are dated before this gate and were not touched.
