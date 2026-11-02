# QA Gate 128 verdict (TIER 2): Secuura/Distributed_Secuura PR 1946 (KS-1868, originate retentionScheduler.ts runEnforcement failure log, held Spark pass O79-B4)

## BLUF
**GATE 128 (TIER 2) on PR 1946 at 612ec3f18cfa: GO WITH NOTES. Nothing has to be fixed before merge.**
(1) Commit 1 (`5bc7b5f5bce4`) equals held pass O79-B4: product and test blobs sha256-equal to the pass applied with patch(1) to base. Commit 2 (`612ec3f18cfa`) changes only `});` to `}, 30000);` on cell C2.
(2) I ran the REAL `retentionScheduler.ts` (jest, and a plain-node run with the REAL winston logger), stubbing only `enforceRetention` and (in jest) the logger recorder, at base and head, for an ordinary Error, a thrown string, a revoked Proxy, a throwing message getter, a getter returning a revoked Proxy, and a getter returning an object with a throwing toJSON. Sweep continuation (enforceRetention calls, the interval timer), what is logged, and anything deleted are IDENTICAL base vs head for the first four kinds. For the last two kinds (message getter RETURNS a hostile non-string) base is WORSE than head: the real logger throws inside the catch, the run's promise rejects, nothing is logged, and with no handler **Node exits rc 1** (measured). At head those two kinds log one constant/string line and the process lives, exactly like an ordinary Error. The unreadable-value after-state at head equals the ordinary Error's after-state. The head is strictly safer than base; only log text differs on the other four kinds (none).
(3) Nothing treats the scheduler's outcome as a verdict or authorisation: `runEnforcement` returns void, its promise is never awaited, `reason` goes to one `logger.error`. TIER 2 stands.
(4) C2 timing measured, spread stated in section 5 (31 to 248 ms at head over 17 cold or concurrent runs at load 11 to 14; 1173 ms in my base red run). The 30000 ms edit is ample.
Not measured on Node 24 (host Node v26.8.1). Mac arm64, 1-minute load 8.7 to 26 during my runs.

## 1. Heads + diffstat (logs/head_start.log, head_end.log)
- START 2026-11-02T12:39:59Z: PR head `612ec3f18cfaf2ca744af3651f64e5fd605ce125` (= Wednesday's, = author's), develop `1584c0f0ff808fddf35245bee41b6b5f9231054c` (= brief). END: both UNCHANGED (logs/head_end.log).
- Merge-base `e2a2426d221d8bd672e97c43c6bbcd6c4027b350`. 2 commits above it, no merge commit (develop not merged in). Numstat: 4 files, **+167/-1** as claimed: test +123, retentionScheduler.ts +1/-1, cheat fragment +21, flow fragment +22. Nothing outside the declared paths.
- PR body not read (no Secuura gh auth here); the READY mail copied to evidence/ready_v17_pr1946.txt is the substitute. Body wording not verified.

## 2. The hunk (the whole product change)
`Blockchain/Dev/services/originate/src/services/retentionScheduler.ts`, catch of `runEnforcement` (one line):
- `-      reason = err instanceof Error ? err.message : String(err);`
- `+      reason = String(err instanceof Error ? err.message : err);`
UNCHANGED: the enclosing `let reason; try {...} catch { reason = 'unreadable thrown value'; }` (already on develop from the earlier guard PR), the log call `logger.error('Scheduled enforcement failed', { error: reason })`, level, message text, the absence of a rethrow, the timers, `startRetentionScheduler`/`stopRetentionScheduler`. Effect: an Error whose `message` getter returns a non-string is coerced to a string before it reaches the logger (or becomes the constant if `String()` throws).

## 3. (1) Held-patch identity (scripts/identity.sh, logs/identity.log)
- Held pass O79-B4: run dir `.../runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker/`; `patch.diff` = `cat section_1.diff section_2.diff` (cmp rc 0). Both sections applied with `patch -p1` to a `git archive` of base `e2a2426d221d`: dry-runs rc 0 and 0, applies rc 0 and 0. Held READY file in `local-model/night`: `READY_KS-1868-KS-1868-O79-B4_...diff.md`.
- sha256 (first 16): product held `1834789629480f53` = commit 1 = PR head (all EQUAL). Test held `7b731330eaed55db` = commit 1; PR head `41478497b8195ca7` (differs by commit 2 only).
- Commit 2 (`git diff 5bc7b5f5bce4 pr1946`): 1 file, +1/-1, `-  });` `+  }, 30000);` on cell C2 (`it('control ks1868 C2 ...`). No assertion, no product line, no other cell.
- The two HTML fragments are not in the held pass's two section diffs (the pass has product + test only); they were not compared to a held source. Their text I read: the claims match what I measured (section 4), see G128-F6.

## 4. (2) Behaviour (scripts/probe.test.ts, nodeprobe.js; logs/probe_base.jsonl, probe_head.jsonl, nodeprobe.log, nohandler_*.log; RUN, not read)
Harness A (jest, real `retentionScheduler.ts`, base file swapped in by sha-checked script, restored): only `enforceRetention` stubbed (rejects with the value on the startup run and on the next interval, then resolves), logger either a recorder or a recorder forwarding to the REAL winston logger with transports silenced. Fake timers advance startup + 2 intervals. 12 cells per version.
Harness B (plain node, no jest): real `retentionScheduler.ts` and real `utils/logger.ts` transpiled and loaded, only `enforceRetention` stubbed, real timers (startup 10 ms, interval 60 ms); run with and without an `unhandledRejection` handler.

| thrown value | enforceRetention calls, interval timer base / head | logged line base / head | real logger throws in catch base / head | process base / head |
|---|---|---|---|---|
| ordinary Error | same, timer alive | own message / same | no / no | alive / alive |
| thrown string | same | the string / same | no / no | alive / alive |
| revoked Proxy | same | `unreadable thrown value` / same | no / no | alive / alive |
| throwing message getter | same | `unreadable thrown value` / same | no / no | alive / alive |
| getter returns revoked Proxy | same (3 calls in harness A) | base: object handed to logger, **real logger throws** TypeError (revoked proxy), nothing logged; head: `unreadable thrown value` | **yes** (2 of 2 runs) / no | **base: exit rc 1 (no handler)**; head alive |
| getter returns throwing-toJSON object | same | base: object handed to logger, real logger throws (`tojson`); head: `[object Object]` | **yes** / no | **base: unhandled rejection**; head alive |

- Positive control: in harness A the base failures surface as 2 jest cell failures (`realLogger getterRevokedProxy`, `getterThrowingToJSON`) and `realThrew` is non-empty at base only; harness B prints UNHANDLED_REJECTION twice per cell at base, none at head. My jest `unhandledRejection` counter read 0 because jest intercepts it; the count in harness B is the real one.
- Continuation: in all 12 cells x 2 versions the scheduler ran the third (resolving) sweep and logged `Enforcement complete`; timer count 1 at the end in all. Nothing is deleted or skipped differently: the catch contains no deletion, and the sweep is `enforceRetention` itself (read-only here).
- The 4 readable-or-guarded kinds are identical base vs head in every recorded field. The 2 hostile-return kinds improve to match the ordinary Error's after-state (one `logger.error` line with a string, run completes, interval keeps firing).
- Limits: `enforceRetention` is a stub (the real sweep in gdprService.ts is not exercised); nobody who acts on the system chooses what `enforceRetention` rejects with, so the hostile kinds are synthetic.

## 5. (4) Re-measure
- **Red-first** (logs/red_base.log, red_base.json): new file against the BASE product: **2 failed, 2 passed** of 4: R1, R2 failed by assertion (`Expected - 1 / Received + 1`), C1, C2 passed. Matches the author. C2 took **1173 ms** in that run.
- **Green at head:** 4 of 4 in 8 sequential cold runs plus 3 `--no-cache` runs plus 2 rounds of 3 concurrent runs (17 runs, logs/green_*, nocache_*, par_*).
- **C2 timing (key question 4), ms:** sequential 8 runs (1-minute load 14.1 to 12.9): 50 54 36 60 36 77 35 31; `--no-cache` x3 (load 11.3): 248 59 92; 3 concurrent x2 rounds (load 11.3): 43 42 41 44 43 37; base red run 1173. Head min 31, median ~43, max 248 (17 runs). I did NOT reproduce the author's 4456 to 7826 ms; my maximum at head is 248 ms and the 1173 ms came with the product at base. The other cells run 0 to 3 ms. The 30000 ms is 120 times my head maximum and 3.8 times the author's worst. The cause stays unmeasured (cold winston load is the candidate; `--no-cache` raised it 3 to 6 times).
- **Originate suite** (logs/suite_head.json, suite_base.json; whole service, `--silent --maxWorkers=2`, `packages/shared` built and linked as gate 125 did): base product without the new file **180 suites, 2163/2163**; head **181 suites, 2167/2167**. +4 tests, +1 suite, 0 failures, as claimed. (A first base run that dropped the default integration-ignore pattern ran 208 suites with 326 failures: my mistake, harness only, discarded; rerun with the default ignore restored is the figure above.)
- **tsc** (scratch config tsconfig.g128.json with src/__tests__ and jest types, as gate 125): `tsconfig.json --noEmit` rc 0; with tests included **0 errors at head and 0 with the base product**; planted type error rc 2, 1 error.
- **eslint** (Dev's own `eslint.config.mjs`, eslint installed in a workdir tools folder, cwd Dev, `node_modules` symlinked): new test and retentionScheduler.ts **0 problems**; planted test file: 1 error (`no-debugger`) and 1 warning. (My first attempt with the config path elsewhere returned rc 0 on the planted file too, so it was a blind control; redone as above and discarded.)
- **docs-fragments** (`docs-fragments.mjs check --root`): rc 0, "flow 117 legacy + 84 new, cheat 112 legacy + 84 new; lint clean, render passes", with the cheat ADVISORY at line 6235 already seen in gate 125 and not caused by this PR. Four planted defects, all rc 1 and each restored by sha (4 restore OK, rc 0 after): flow unclosed div, flow `<!--n-->.` removed, cheat unclosed div, cheat `</table>` corrupted.
- **merge-tree** (`git merge-tree --write-tree pr1946 origin/develop`): rc 0, tree `6a88df5e2dbf`, result differs from develop in exactly the PR's 4 paths. 74 files moved on develop since the base, **0 shared** with the PR's 4 paths.

## 6. Mutants (scripts/mutants.py, logs/mutants_table.log; product file only, tests untouched, sha256 restored after every run, all `restore=True`)
13 mutants on the new test file: 12 killed, 1 survivor.
| mutant | killed by |
|---|---|
| M0 revert to base | R1 R2 |
| M1 drop `String()` | R1 R2 |
| M2 constant for all | C1 C2 R2 |
| M3 `String(err)` only | C1 C2 R2 |
| **M4 non-Error branch to `'x'`** | **survives the new file** (killed by the sibling file's C2 `ks1868-retention-scheduler-run-enforcement-p3-unreadable-throw.test.ts`, run separately: C2 red) |
| M5 Error message to `'x'` | C1 C2 R1 R2 |
| M6 fallback text changed | R1 |
| M7 drop inner try | R1 |
| M8 log removed | C1 C2 R1 R2 |
| M9 wrong message text | C1 C2 R1 R2 |
| M10 level error to warn | C1 C2 R1 R2 |
| M11 rethrow `throw err` | suite crash at load (revoked-Proxy TypeError in source-map-support), no assertion cell named; killed as a failed run |
| **M12 stop the scheduler after a failure** | **survives BOTH the new file and the sibling file** |
All kills are by assertion except M11 (suite-level crash). M12 means no test in the repo pins "a failed sweep leaves the timer running"; my harness A measured it directly for the unmutated product (timer 1, third sweep ran). Not a defect of this PR; a gap (G128-F4).

## 7. (3) Tier
`startRetentionScheduler` is called once at `index.ts:519`, `stopRetentionScheduler` at `:345` (logs/callers.log; no other non-test importer). `runEnforcement` is module-private, returns `Promise<void>`, and is invoked by `setTimeout`/`setInterval` without await. `reason` is used only as the field of one `logger.error`. No caller maps a throw or the log to a decision, a verdict or an authorisation, and no persisted state comes from this catch. **TIER 2 stands. Not tier 1.**

## 8. Kam's ks1346 logging rule (type and field NAMES of a thrown object, never values)
- Test as the brief states it: does any changed line print thrown-value text it did not print before? **No new value text.** Ordinary Error: its message, as before. Non-Error: `String(err)`, as before. Hostile-return kinds: base passed the raw object to the logger (the real logger then threw); head logs the constant or `[object Object]`, which prints no field content. No new log line was added.
- The line still logs a thrown Error's message text rather than names only (pre-existing, identical to every KS-1868 sibling; belongs to the KS-1346 card). G128-F5 (info).

## 9. FINDINGS
- **G128-F1 (INFO, measured)** Held-patch identity holds; commit 2 is `}, 30000);` on C2 only.
- **G128-F2 (INFO, measured, positive)** The change is a real fix, stronger than the fragment's wording: at base a message getter returning a hostile non-string makes the real logger throw inside the catch; with no unhandled-rejection handler the Node process exits rc 1 (harness B, logs/nohandler_base.log). Head: no crash, one line logged. Sweep continuation, timers and deletions are the same for every kind. Optional: say in the PR body that the base outcome is a process exit under Node's default `--unhandled-rejections=throw`, not only "an unhandled rejection". (Production whether index.ts installs a handler was not read; see NOT TESTED.)
- **G128-F3 (INFO, measured)** C2 timing at head: 31 to 248 ms over 17 runs at load 11 to 14, and 1173 ms in the base red run; the author's 4456 to 7826 ms not reproduced. 30000 ms is ample.
- **G128-F4 (INFO, recommended-later)** Mutant M12 (stop the scheduler after a failed sweep) survives every test in the repo for this file; no cell pins the "failure does not stop future sweeps" property this PR's whole claim rests on. Out of scope for this PR; a follow-up cell would close it.
- **G128-F5 (INFO, pre-existing, ks1346-adjacent)** The log line carries an Error's message text, not only names; not new, not worse.
- **G128-F6 (INFO, wording)** The fragment says the new test's C2 "took 38 to 345 ms in most runs": mine are 31 to 248 ms; consistent. It also says the timers "neither await nor catch it, so it is an unhandled rejection": confirmed (harness B). The fragment's mutant-run sentence (C2 timed out at 5000 ms before the edit) is the author's measurement; not reproduced, not contradicted.
- **G128-F7 (INFO)** Develop at START and END `1584c0f0ff80`, 0 shared paths, merge-tree clean.
- **No FIX-BEFORE-MERGE item.**

## 10. Notes for the PR body
1. (F2) Optionally add that the base failure for the two hostile-return kinds is a process exit by Node default, not only an unhandled rejection.
2. (F3) Optionally add that a second host measured C2 at 31 to 248 ms (17 runs) and 1173 ms once; cause still unmeasured.
3. (F4) Optionally name the unpinned "timer survives a failed sweep" property as follow-up.

## 11. NOT TESTED
- The live PR body, Linear, CI, the author's pre-push hook (13 of 16 legs, quoted from the READY mail), Node 24.
- Real PostgreSQL, the real `enforceRetention` sweep in gdprService.ts, a real service boot, whether `index.ts` or the production process installs an `unhandledRejection` handler, production logger configuration (I used the repo's logger with silenced transports), the four platform suites.
- tsc and eslint ran with my own scratch config and a workdir-local eslint install, not the repo's `npm ci`; `npm ci` at the root failed on develop's lock file being out of sync with package.json (checked out the PR head instead, where it succeeds); `packages/shared` was built and symlinked by hand for the whole-suite run.
- The fragments were not compared to any held-pass source (the pass sections carry only product and test).
- The seat's own mutant claims (R1 and R2 red) were not re-run as written; I ran my own 13 (and the sibling file for M4, M12).
- Cleanup: no process of mine is left (the end.sh ps read showed only the gate's own shell). Scratch kept in the workdir: repo/ (clean except the gitignored `Blockchain/Dev/node_modules` symlink to eslint_tools), scratch_base/, scratch_base_retentionScheduler.ts, eslint_tools/, tsconfig.g128.json, logs/_quarantine/ (probe and planted files).
