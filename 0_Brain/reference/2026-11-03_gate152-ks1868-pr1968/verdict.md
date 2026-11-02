# QA Gate 152 verdict: Secuura/Distributed_Secuura PR 1968 (KS-1868, vc-issuer db.ts pool listener + ready hook, credentialRepo.ts three read catches), TIER 2, round 1

## BLUF
**GO WITH NOTES.** The code change does what it says and every figure re-measures (vc-issuer 714 -> 732, red 11/18 by assertion, tsc 0/0, eslint, docs, merge-tree clean). For an unreadable value, head's after-state equals an ordinary Error's at all five sites. **One FIX-BEFORE-MERGE, wording only (PR body / ticket comment, no code): the claim "the credential verifies false in all three cases at base AND head / fails closed both ways" is REFUTED by a run** (G152-F2). Separately a **HIGH, pre-existing finding (G152-F1)**: when the DB read fails with an ORDINARY Error and this process's memory copy is stale-unrevoked (credential revoked in the DB by another process), `getById` returns the memory copy and a revoked credential VERIFIES TRUE, at base and at head. This is not introduced by the PR; the PR makes hostile values behave like ordinary Errors (and so join it). Needs its own ticket. Node v26.8.1 throughout, not measured on Node 24.

## Heads
START (logs/head_start.log via setup.log, 21:45Z): PR head `6e58db5676fb88d821ff9513c32ae874ea307450` (equals the READY mail), develop `b85b7b6786fa6329b6f781cebf2475147738004e`. Develop MOVED during the gate to `ddd770cab4aa922f5a49376b8bbe5232a94939f7` (one commit, "demo-service Redis listener and presenter catch", none of this PR's paths); merge-tree redone on it (section 6). END (logs/head_end.log): PR head unchanged `6e58db56...`. PR parent / merge-base = `2f9f7db313b3` ("base" below). PR body not read (no gh login); the READY mail is in evidence/.

## 1. Diffstat (logs/hunks.diff, git diff --stat)
6 files, +338/-5 as declared: db.ts +18/-?(1 net hunk pair each), credentialRepo.ts +27/-3 incl. context, two new tests (119 + 151 lines), two docs fragments (17 + 11). Nothing outside the declared paths (merge-tree path list equals the PR path list, 6).

## 2. The hunks
Each of five sites: `{ error: err.message }` / `{ error: err?.message }` -> `let reason: string|null|undefined; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; } ... { error: reason }`. Sites: db.ts pool 'error' listener (was unguarded `err.message`, so null/undefined emitted values also threw), db.ts runDbReadyHook catch, credentialRepo.ts getById / getRecordById / getByHash catches. Unchanged: log text, level, other keys, which store is consulted after the catch (memory), return values, flags, SQL.

## 3. Behaviour (RUN)
### 3a. db.ts, the REAL db.ts at base (2f9f7db3) and head in a child process, only pg's Pool replaced (EventEmitter stand-in), real winston logger (NODE_ENV=production, stdout captured), cwd = logs/cwd (the vc-issuer logger has only a Console transport; no file landed anywhere: logs/cwd is empty, no logs/ dir in the service). 72 runs (3 sites x base/head x 12 values), all rc 0, stderr empty (logs/probe_matrix.jsonl, logs/probe_table.log, scripts/probe_child.ts).
| value | pool listener base | head | boot hook base | head | retry-timer hook base | head |
|---|---|---|---|---|---|---|
| ordinary Error | 1 line "boom" | same | initDb true, 1 line | same | 1 line | same |
| revoked Proxy | **uncaughtException** TypeError, no line | 1 line "unreadable thrown value" | **initDb REJECTS** TypeError, no line | true, 1 line | **unhandledRejection** | 1 line |
| message getter throws | **uncaughtException** | 1 line constant | **REJECTS** | true, 1 line | **unhandledRejection** | 1 line |
| null / undefined thrown | **uncaughtException** (pool only) | 1 line, no error key | SAME (hook was already readable) | | SAME | |
| message 42 / Symbol / toString objects | `42` number / key absent / `{}` | `"42"` / `"Symbol(s)"` / constant or text (type change, no throw) | same shape | | same shape | |
isDbAvailable(): equal at base and head in every cell. **Class bar (Q1) at db.ts: PASS** (unreadable-value after-state = ordinary-Error after-state: one logged line, process lives, initDb resolves, flag unchanged). Caller read, not run: index.ts:170 `await initDb(runDbBootTasks)` inside `start()`, `start().catch(err => ... err.message; process.exit(1))`: at base a hostile hook failure made start() reject and (the rejection value there is the TypeError raised in the catch, readable) the service exited 1 at boot; at head it boots like for an ordinary Error. No process.on('uncaughtException'|'unhandledRejection') exists in vc-issuer src (grep: only SIGTERM/SIGINT index.ts:208-209), so the pool-listener throw at base ends the process by Node default.

### 3b. credentialRepo.ts class bar at the three read catches (RUN: the real module, ../db replaced; also logs/red_base_new_repo.log)
For ordinary Error, revoked Proxy and getter-throws, head returns the memory-store answer (undefined for an id not in memory) and logs one warn, `error` = text; base: ordinary Error identical, hostile values REJECT out of the repo call. **PASS** at all three. The repo cells only use a missing id, so "what falls back" is covered by Q2 below.

### 3c. Q2: WHAT falls back, and can a revoked credential verify? (RUN: scripts/runq2.sh + gate_tests/gate152-q2.test.ts, real credentialRepo + real revocationResolvers + real verifier + real routes POST /, /:id/revoke, /verify; only ../db (an in-memory fake DB table that can fail its SELECT / UPDATE) and the logger replaced. logs/q2_base.log, logs/q2_head.log.)
What falls back: all three read catches fall back to `memoryStore` (process-local Map filled by store(), revoke() and ONLY at boot by loadFromDb; never refreshed from the DB afterwards, read credentialRepo.ts 56-62, 453-470). getById has one non-test caller, revocationResolvers.ts:55 (services/, not src/ root as the READY mail's path implied) -> verifier checkStatus ARM 1 (verifier.ts 487-505, read AND run): found+revoked -> error; not found -> "no issuer record" (fail closed, KS 1375); rejection -> "Failed to check credential status". The stale comment at revocationResolvers.ts 46-52 ("ABSTAINS") is confirmed stale (the verifier fails closed); G152-F5.
| scenario (3 values each: ordinary Error, revoked Proxy, getter-throws) | base verified | head verified |
|---|---|---|
| A: revoke succeeded in this process (memory+DB revoked), then DB READ fails | false (ordinary: "Credential has been revoked"; hostile: "Failed to check credential status") | false, "Credential has been revoked: test" for all three |
| D: id unknown to memory, DB read fails | false (ordinary "no issuer record"; hostile "Failed to check...") | false "no issuer record" for all three |
| **B: this process's memory copy is stale-unrevoked; DB row revoked elsewhere (another replica / out-of-band SQL); DB read FAILS** | **ordinary Error: verified TRUE (errors [])  <- pre-existing fail-open**; revoked Proxy / getter: false ("Failed to check credential status") | **TRUE for all three (errors [])** |
| B control: same stale memory, DB healthy | false (DB row wins) | false |
| C: revoke's DB UPDATE fails (ordinary Error): route answers 200 "revoked successfully", DB row stays UNrevoked | memory revoked, DB not | same; hostile values: revoke 500 (sibling unguarded catch, F4) with memory already revoked |
**Q2 answer: YES, a revoked credential verifies true when the DB read fails and memory is consulted, in scenario B, for an ORDINARY Error at BASE already (HIGH, pre-existing) and, after this PR, for the hostile values too.** "Fails closed both ways" holds only when memory is current (scenarios A, D). Preconditions for B: a second writer to the DB (multi-replica ACA, admin SQL, a revoke handled by another instance) plus a DB read failure on the verifying instance. Scenario C is the same class one step earlier: a revoke whose DB write fails is reported 200 and, after a restart, loadFromDb reloads the unrevoked row (read, not run past restart).

## 3d. Q3: the first-cell 5000 ms load timeout
Reproduced once in my own runs: the db mutant run M0 (logs/mut_src_db.ts0__M0_revert.log) failed control C1 on "Test timed out in 5000ms" (23063 ms; vitest reported transform 51 ms, import 90 ms, tests 23.07 s, at load ~12 with 2 workers). It did NOT reproduce in the whole-suite default-workers run (732/732, load 12.9) nor alone (9/9, C1 162 ms). Likely cause (measured part: `require('@secuura/shared')` costs 702 ms cold at load ~12, scripts/reqtime.js; read part: db.ts:186 does that require at module scope, and C1 is the first cell that imports the real db): the first freshDb() pays the shared-package load. Not proven to explain 23 s. Not a product defect; flake risk in CI under load (G152-F6).

## 4. Re-measure
- Red first (product at base 2f9f7db3, new file only; logs/red_base_new_repo.log, red_base_new_db.log): repo **6 failed / 3 passed (9)**, db **5 failed / 4 passed (9)** = 11 red, 7 controls, every red an AssertionError (6 and 5), 0 timeouts. Head: 18/18.
- Whole vc-issuer suite (--maxWorkers=2): base **23 files / 714**, head **25 / 732**; base product + new tests: 11 failed / 721 passed (only the R cells). Default workers at head: 25 / 732 rc 0 (logs/q3_whole_defaultworkers.log).
- tsc including tests (ad hoc tsconfig.gate.json, src/**/*, moved out): **0 at base, 0 at head**; own tsconfig 0. eslint on the 4 changed files: rc 0; planted file (unused var + debugger): rc 1.
- docs-fragments check (node scripts/docs-fragments.mjs check --root <clone>): rc 0 "lint clean, render passes", with the same pre-existing cheat ADVISORY at line 6235 as gates 139/141/150. Planted defects, each restored by sha: flow unclosed div rc 1; flow `<!--n-->.` removed rc 1; cheat unclosed div rc 1; cheat `</table>` corrupted rc 1; after restore rc 0.
- npm ci succeeded for me on the PR branch lockfile (no fallback needed); shared built rc 0.

## 5. Mutants (scripts/mutants.py; one site per run in the product only, tests untouched, sha256 restored after every run: all True; logs/mutants_table.log)
55 runs (11 mutants x 5 sites): **36 killed, 19 survived**, every kill by AssertionError (M0 at db listener also a C1 timeout, see 3d).
| mutant | db.ts listener | db.ts hook | credentialRepo getById | getRecordById | getByHash |
|---|---|---|---|---|---|
| M0 revert, M1 inner try dropped, M2 constant text, M8 always constant, M9 catch rethrows, M10 log drops error | killed | killed | killed | killed | killed |
| M3 no String() | killed | killed | **SURVIVED** | **SURVIVED** | **SURVIVED** |
| M5 String for all / M7 undefined -> text | killed | killed | **SURVIVED** | **SURVIVED** | **SURVIVED** |
| M4 `err?.message` -> `err.message` | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** |
| M6 null message -> text | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** | **SURVIVED** |
The guard itself (M0 to M2, M8 to M10) is pinned at all 5 sites. Surviving = branches no cell reaches (null/undefined thrown value, null message, non-string readable message, and for the repo no non-string-message cell at all). Same family as G139-F1/G141-F1/G150-F1. M4 at the db listener is the one with behaviour weight: a revert to `err.message` regresses a null/undefined emitted value from "logged line" back to an uncaught exception (probe: pool nullValue/undefinedValue, base uncaught) and no cell would fail.

## 6. merge-tree
Onto b85b7b67 (logs/merge_tree_b85b7b67.log): rc 0, clean, paths equal the PR's 6. Onto current develop ddd770ca (logs/merge_tree.log): rc 0, tree f520da70..., clean; merged tree differs from develop in exactly the PR's 6 paths (logs/merged_vs_develop.log equals logs/pr_paths.log). Suites/fragments not re-run on the merged tree.

## 7. ks1346 logging rule
No new log line; the `error` field now carries a string or a constant type statement, never a value of the thrown object beyond a readable `message`. Compliant (info).

## 8. Notes for the PR body
- **G152-F1 (HIGH, pre-existing, NOT introduced by this PR, measured; separate ticket)** Scenario B: stale-unrevoked memory copy + DB read failure -> `getById` -> `revocationVerifierConfig` says found, not revoked -> verifier returns true for a credential whose DB row is revoked. Base: ordinary Error already fails open; hostile values failed closed by accident (the throw inside the catch made the resolver reject). This PR moves hostile values onto the ordinary-Error path, i.e. the class bar is met, but the accident-protection is gone for hostile values. Fix class: in getById (verify path only), when the DB is available and the read THROWS, do not answer from memory (rethrow or return a marker so the resolver reports "Failed to check credential status"); or refresh memory on revoke from the DB. Needs Kam's ruling (availability vs fail-closed: today a DB blip is survived by memory). Related one step earlier (G152-F3).
- **G152-F2 (FIX-BEFORE-MERGE, wording only)** The PR body / READY mail / ticket comment says the credential "verifies false in all three cases at base AND head" and "fails closed both ways". Refuted for scenario B above. Replace with: "fails closed when the process's memory copy is current (revoked in this process, or unknown id); if another writer revoked the DB row and this DB read fails, memory is consulted and the stale copy verifies true, for an ordinary Error already at base (G152-F1)". No code change.
- **G152-F3 (recommended, pre-existing, measured)** revoke(): a DB UPDATE failure is swallowed ("kept in memory"), the route answers 200 "revoked successfully", the DB row stays unrevoked; after a restart loadFromDb loads it unrevoked and it verifies true. Same fail-open family; ticket with F1.
- **G152-F4 (recommended follow-up, read from source)** Four sibling catches in credentialRepo.ts still read `err?.message` unguarded: store (line 98), getReadableByHash (324, the by-hash ROUTE's path), selectList (413, the list route), revoke (502, measured: revoke answers 500 for a hostile value after memory is already revoked). Also db.ts probeDb (`error: err?.message`) unguarded (read). KS-1868 site list.
- **G152-F5 (INFO / recommended)** revocationResolvers.ts 46-52 comment says the verifier ABSTAINS on found:false; it fails closed (KS 1375). Stale comment, confirmed by run (D rows).
- **G152-F6 (recommended, flake)** db test control C1 hit a 5000 ms timeout once in my runs (23 s) and once in the author's; first cell pays the db.ts module-scope `require('@secuura/shared')`. Fix: a warm-up `await import('../db')` in beforeAll or a per-test timeout on C1.
- **G152-F7 (recommended, test gap)** 19 surviving mutants (section 5). One cell per site closes the family: a null/undefined emitted value at the pool listener (kills db M4) and a readable non-string / null message at each repo catch.
- **G152-F8 (INFO)** Behaviour change beyond the unreadable class, as in PRs 1956/1957/1966: a readable non-string message (42, Symbol, custom toString) is now logged as a string (`"42"`, `"Symbol(s)"`, text) where base logged a number, dropped it, or logged `{}`.
- **G152-F9 (INFO)** The READY mail names `revocationResolvers.ts` at src/ root; it is `src/services/revocationResolvers.ts`. The PR is one commit on 2f9f7db3; develop moved twice during the wait; merge clean.
- **G152-F10 (INFO)** At base a hostile ready-hook failure made `start()` reject and the service exit 1 at boot (and from the retry timer an unhandledRejection); head boots like for an ordinary Error.

## 9. NOT TESTED
The live PR body; a real Postgres or pg pool (stand-ins; a real idle-client 'error' emission read, not run); a booted service, Node's actual process exit on uncaughtException/unhandledRejection (read, absence of handlers grepped; the probe captures the events); a real second replica for scenario B (simulated by editing the fake DB row, the mechanism is the same: memory not refreshed); a restart for scenario C (loadFromDb read, not run); the verify route over HTTP and the signature path beyond the route dispatch used by the sibling ks1375 suite; the other three read-path callers (listReadable etc.); CI, the pre-push hook legs, the four platform suites; Node 24; BigInt/cyclic messages; Spark shadow review.

## Processes and files
Every background run I started (npm ci, shared build, suites.sh, probe_matrix.sh, mutants.py) has finished; `ps` shows none with this workdir. Clone `git status` empty at the end (gate tsconfig, planted eslint file, db_base.ts, Q2 test moved to logs/_quarantine). No log file landed outside logs/: logs/cwd is empty and vc-issuer/logs does not exist.
