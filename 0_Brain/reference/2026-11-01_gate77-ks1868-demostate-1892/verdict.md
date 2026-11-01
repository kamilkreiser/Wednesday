# QA Gate 77 verdict: Secuura/Distributed_Secuura PR 1892 (KS-1868, demo-service GET /state O41-P2), tier 2

Logs are in `<workdir>/logs/` (workdir = `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892/`). Scripts are in `<workdir>/scripts/`.

## BLUF
GO WITH NOTES

The product hunk does what it says: an unreadable thrown value now logs the constant `unreadable thrown value` and answers the in-memory state. The error message never reaches the HTTP response, before or after. The new test goes red at base, green at head, and kills 11 of 14 mutants. Whole-suite and tsc numbers match the author's. The merge is clean and the fragment gate works. The notes are two weak spots in the test (G77-F1, G77-F2) and one understated consequence in the docs (G77-F3). None blocks the merge.

## Heads
- Start (`logs/head_start.log`): PR head `b17ef4400111f55ca5c06e2610252a105eb23032` (as expected), develop `85c56a3d1eb92c8399dcfd3d6ee2a717cf356428`.
- End (`logs/head_end.log`): PR head, local HEAD and `ls-remote refs/pull/1892/head` are all `b17ef440…`. `ls-remote` develop is `85c56a3d…`. Nothing moved.
- The PR is one commit, a direct child of develop's tip (`git merge-base` = `85c56a3d`).
- Diff is 4 files, +147/-1 (`git diff --stat`): `state.ts`, the test (+104), and one cheat and one flow fragment.

## FINDINGS
- **G77-F1 (LOW, test gap):** the status code of the fallback answer is not asserted. Mutant M9 changes line 88 to `res.status(500).json(inMemoryState)` and SURVIVES (3/3 pass; `logs/mut_M9.log`). The test's `res.status()` stand-in records `out.status` (test lines 42-46) but no cell reads it. A future change that turned this answer into a 500 would go unnoticed by this test. `state.ts:88`.
- **G77-F2 (LOW, test gap, pre-existing branch):** the `'Unknown error'` branch (a readable non-Error value) is not exercised. Mutant M6 (constant changed to `'Other'`) SURVIVES (`logs/mut_M6.log`). Mutant M14 (drop `instanceof`, use `(err as Error).message`) also SURVIVES (`logs/mut_M14.log`), because the revoked Proxy and the getter cell both throw either way. The PR claims this branch is unchanged, and that is true (see §1). It is simply unguarded by the new test. `state.ts:83`.
- **G77-F3 (INFO, docs accuracy):** the fragments say the unguarded read made "the handler reject instead of answering". That is true, but it understates the effect. In the emulation (§1), base with a revoked Proxy or a throwing getter gives no HTTP response and the process exits with code 1 (an unhandled rejection under Node's default). demo-service installs no handler (`logs/grep_unhandled.log` is empty), so the change closes a process-exit path, not just a missed response. This is a documentation understatement, not a defect. Evidence is `logs/live_emul.log`, which is an emulation and not the real router.
- **G77-F4 (INFO, author's line reference):** the author's "~:110" other catch is actually `state.ts:114-118` (POST /presenter-mode). It is untouched, and it is a generic 500 that does not leak the message.
- **G77-F5 (INFO, advisory, not caused by this PR):** `docs-fragments.mjs check` prints two ADVISORY lines at head (committed flow page drifts from the render at line 6249, cheat at line 6235) and still exits 0 (`logs/frag_head.log`). The PR touches neither committed page. I did not run it at base, so I cannot say the drift is pre-existing.

No blocking finding.

## 1. The product hunk
Diff of `state.ts` (`git diff develop..head`, +6/-1):
```
-    const message = err instanceof Error ? err.message : 'Unknown error';
+    let message: string;
+    try { message = err instanceof Error ? err.message : 'Unknown error'; }
+    catch { message = 'unreadable thrown value'; }
```
**What changes:** only the read of the thrown value, in `state.ts:81-86`. It is wrapped in an inner try, with the constant fallback `'unreadable thrown value'` (lines 84-85).

**What does NOT change, checked in the head file (`state.ts:79-89`):**
- The `'Unknown error'` non-Error branch is byte-identical (line 83). In the emulation the head, given a plain string, logs `Unknown error` (`logs/live_emul.log`, "head plainstr").
- The `logger.error('Failed to read demo state', { error: message })` text and shape are unchanged (line 87). Mutants M7 and M8 change them and are killed.
- `return res.json(inMemoryState)` is unchanged (line 88).
- Everything above the catch (Redis read, success return, in-memory return at line 79) is untouched.

**KEY QUESTION: does the error message reach the HTTP response? No, before or after.**
- The message goes only to `logger.error` (line 87). The response is `res.json(inMemoryState)`, a fixed object with `currentPersona`, `presenterMode` and `scenarioStep` (lines 24-28). Mutant M12 adds the message to the body and is killed, so the test would catch a leak.
- The error middleware `src/middleware/errorHandler.ts`, mounted at `app.ts:89`, is never reached from this handler. The handler is `async` and never calls `next(err)`. It is also built so a 5xx never carries the thrown message (`errorHandler.ts:87`).
- The other response (`state.ts:72-76`) is built from Redis values only.

**Behaviour BEFORE the change for the unreadable values.** From the code, then confirmed by `scripts/live_emul.js` (real Express 4.22.3 from the repo's `node_modules`, Node v26.8.1, the exact base and head catch code, logged in `logs/live_emul.log`):
- Revoked Proxy: `instanceof` throws `TypeError: Cannot perform 'getPrototypeOf' on a proxy that has been revoked`, inside the catch.
- Throwing `message` getter: `.message` throws inside the catch.
- In both cases the async handler rejects. Express 4 does not catch a rejected promise from an `async` handler, so the error middleware is NOT reached ("ERROR MIDDLEWARE REACHED" never printed) and Express's default handler is not reached either.
- Result at base: no HTTP response, nothing logged, and the process exited with code 1 (`process exit code 1`). In Node (15+) the default is to throw on an unhandled rejection.
- demo-service installs no `unhandledRejection` or `uncaughtException` handler (`logs/grep_unhandled.log` empty). It does not call the shared `setupGracefulShutdown`: `index.ts` defines its own `gracefulShutdown` for SIGTERM and SIGINT (`index.ts:60-82`). `docker-compose.yml:435-440` says only the gateway runs `survive`, and every other service keeps `exit`.
- Real demo-service is therefore expected to crash at base, and I did not exercise it. The emulation covers the catch code, not the real router.
- At head, the same four inputs (`proxy`, `getter`, `plainstr`, `error`) all give HTTP 200 with the in-memory state. The log is `unreadable thrown value` for the first two, `Unknown error` for the string and `redis boom` for the Error. Exit code is 0.

**Other catches in state.ts:** the POST catch at `state.ts:114-118` is unchanged. It still reads `err instanceof Error ? err.message : 'Unknown error'` unguarded and returns a generic 500. `git diff --stat` shows the hunk is the only change in the file. `getRedis` (`:49`, an empty catch) is untouched.

## 2. Red-first and mutation
Scripts: `scripts/redmut.py`, `scripts/redmut2.py` (summaries `logs/redmut_summary.log`, `logs/redmut2_summary.log`).
- **Red at base:** the base `state.ts` (sha256 `c8c3e278…`) with the new test gives rc 1, `Tests 2 failed | 1 passed (3)` (`logs/red_base.log`). Both failures are `AssertionError: expected true to be false` (the handler threw). The control C1 passes.
- **Green at head:** `Tests 3 passed (3)`, rc 0 (`logs/head_newtest.log`).
- The head `state.ts` was restored by sha256 each time (`68bc8787…`). The summaries assert this.

| Mutant | Result | Log |
|---|---|---|
| M1 fallback string changed | KILLED (2 failed) | `mut_M1.log` |
| M2 inner try removed (read hoisted) | KILLED | `mut_M2.log` |
| M3 inner catch rethrows | KILLED | `mut_M3.log` |
| M4 inner catch leaves message undefined | KILLED | `mut_M4.log` |
| M5 `Error.message` dropped (`String(err)`) | KILLED (1 failed) | `mut_M5.log` |
| M6 `'Unknown error'` constant changed | SURVIVED (see G77-F2) | `mut_M6.log` |
| M7 logger text changed | KILLED | `mut_M7.log` |
| M8 logger key renamed | KILLED | `mut_M8.log` |
| M9 final response made `.status(500)` | SURVIVED (see G77-F1) | `mut_M9.log` |
| M10 final body emptied | KILLED | `mut_M10.log` |
| M11 log call skipped | KILLED | `mut_M11.log` |
| M12 message leaked into the response body | KILLED | `mut_M12.log` |
| M13 fallback set to empty string | KILLED | `mut_M13.log` |
| M14 `instanceof` dropped (`(err as Error).message`) | SURVIVED (see G77-F2) | `mut_M14.log` |

14 mutants were run in total: 11 killed, 3 survived. The first pass had M5, M6 and M8 refuse their patterns (two matches, because the POST handler has the same line). I redid them with unique context in `redmut2.py`. The M5, M6, M8 results in the table come from that second run, and M14 was added there. M14 survives because both unreadable cells throw on either read. That is a limit of the cells, not a hole in the hunk.

## 3. Whole suite and tsc
Setup: `npm ci --ignore-scripts` rc 0, 1795 packages (`logs/npm_ci.log`). `packages/shared` built with tsc, rc 0 (`logs/build_shared.log`). vitest ran with `nice 10 --maxWorkers=2`. Node v26.8.1.
- **Base `85c56a3d`:** 11 files, 91 of 91 passed (`logs/suite_base.log`). The new test file does not exist at base.
- **Head `b17ef440`:** 12 files, 94 of 94 passed (`logs/suite_head.log`). This matches the author's figures.
- **tsc with tests** (`scripts/tsconfig.gate.json`, `src/**/*` including `__tests__`, noEmit): 25 errors at head (`logs/tsc_head.log`), 25 at base (`logs/tsc_base.log`). The sorted `error TS` lines are identical (`logs/tsc_diff.log` is empty, diff rc 0). Zero mention `routes/state` or `ks1868-state`. Both runs exit with rc 2, from the errors.

## 4. Merge
`git merge-tree --write-tree refs/gate/develop refs/gate/pr1892`: rc 0, tree `f5a0c860889f30a3ed0f0a9d84a7e2ac76ccc295` (`logs/merge_tree.log`). That is equal to the head's own tree (`rev-parse head^{tree}`), as expected for a one-commit child of develop's tip. No conflicts.

## 5. Fragment pair
`node Blockchain/Dev/scripts/docs-fragments.mjs check` on the head: rc 0 (`logs/frag_head.log`), "flow 117 legacy + 46 new, cheat 112 legacy + 46 new; lint clean, render passes html_docs_check". It also printed the two ADVISORY drift lines (G77-F5). Planted defects (`scripts/frag.py`), each restored by sha256, with a final check at rc 0 (`logs/frag_end.log`):

| Plant | rc | Message | Log |
|---|---|---|---|
| cheat: first `</table>` dropped | 1 | tags not balanced: `<table>` opened 3, closed 2 | `frag_cheat_P1.log` |
| cheat: second `<h2>` added | 1 | must hold exactly one entry (one `<h2>`) | `frag_cheat_P2.log` |
| flow: literal `7.` replaces `<!--n-->` | 1 | the `<h2>` must start with `<!--n-->.`, and the heading carries a literal section number (2 findings) | `frag_flow_P1.log` |
| flow: `</pre>` dropped | 1 | tags not balanced: `<pre>` opened 1, closed 0 | `frag_flow_P2.log` |

## 6. End heads
See `logs/head_end.log` and the Heads section. They are unchanged.

## NOT TESTED
- A real Redis failure against a booted demo-service, and the real router under Express. The §1 base crash is from an emulation of the catch code, not the actual service.
- A Docker or Node 24 run. The Dockerfile uses `node:24-alpine` and I ran Node v26.8.1.
- eslint (the author reports 0 errors) was not re-run.
- The four platform suites and any deploy. PR 1892 touches demo-service, which is part of the demo stack, so a later deploy needs its own gate and Kam's word.
- The `docs-fragments.mjs` check at base, so I cannot say whether the F5 advisory drift is pre-existing.
- Other KS-1868 sites, including `routes/persona.ts`.
