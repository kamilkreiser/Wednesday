# QA Gate 78 verdict: Secuura/Distributed_Secuura PR 1893 (KS-1868, analytics dbSaveExport + dbSaveAlertRule O42), tier 2

## BLUF
**GO WITH NOTES.** Both hunks are correct and minimal (+7/-1 each). For any readable thrown value the INFO text, the `error` key and the logged value are unchanged. The only behaviour change is that an unreadable thrown value (revoked Proxy, throwing `message` getter) now logs the constant `unreadable thrown value` instead of the catch throwing. Red-first confirmed by assertion (4 of 6 fail at base product, 6 of 6 pass at head). Analytics suite 50/50 at base (new tests excluded) and 56/56 at head. tsc: the same 1 error at base and head. merge-tree rc 0. Fragment check rc 0, planted defects rc 1. Notes are test-coverage gaps (G78-F1, F2) and the caller-behaviour trace (G78-F3), none blocking.

## Heads
- START (logs/head_start.log, 2026-11-01T06:19:38Z): PR head `276564a771713769e86e20928356121fa8c85e84` (matches expected), develop `85c56a3d1eb92c8399dcfd3d6ee2a717cf356428`. Merge-base = parent = develop tip (one commit on develop's tip).
- END (logs/head_end.log, 06:29:23Z): local HEAD, `refs/gate/pr1893` and `ls-remote origin refs/pull/1893/head` all `276564a7...`; develop on origin `85c56a3d...` (logs/lsremote_end.log). Nothing moved. Working tree clean (`git status --short` empty).
- Diffstat (logs/diffstat.log): 6 files, +202/-2: two product files (8 lines changed each: +7/-1), tests +69 and +82, two fragments (+19, +18).

## FINDINGS
- **G78-F1 (LOW, test gap)** `exportService.ts:56-62` and `scheduledJobs.ts:59-65` (head line numbers). Mutants M6 (non-Error branch replaced by constant `'x'`) and M7 (`(err as any)?.message ?? String(err)`) SURVIVE in both files (logs/mutants2.log). No cell exercises the readable non-Error branch (a string or plain-object throw). Same gap gate 74 recorded for the loaders (G74-F1). Not a product defect; the branch is unchanged by this PR.
- **G78-F2 (LOW, test gap, "resolves" contract)** The behaviour the PR sells (the catch now resolves) is only partly pinned. Scheduled file: M9 (log, then rethrow, in every case) SURVIVES (logs/mutants2.log, `sched | M9 ... SURVIVED`) because the only path to `dbSaveAlertRule` is `addAlertRule`, which swallows the rejection (`scheduledJobs.ts:497`); nothing observes it. Export file: M9 is KILLED, but only by control C1, whose `await save()` has no catch. R1 and R2 use `await save().catch(() => undefined)`, so by reading, a rethrow limited to the unreadable path would survive. I did not run that narrower mutant. No product defect.
- **G78-F3 (INFO, behaviour change, read from source, not exercised)** `dbSaveExport` callers all propagate; see section 1. Before: an unreadable value made the catch throw, so `createExport` rejected (route answers 500, `routes/analytics.ts:322-326`) or `processExport` produced an unhandled rejection in a service that registers no handler. Now: it logs and resolves, so the route answers 202 with an export record the DB never saved. This is exactly what an ordinary Error already does at base, so the change only routes the unreadable case into the existing path. Matches the author's claim.
- **G78-F4 (INFO, line-number note)** The `exportResult.error = ...` client-visible assignment is base line 160 and is `exportService.ts:166` at head (+6 shift from the hunk). Untouched. Anyone grepping head for `:160` lands on `exportResult.completedAt`.
- **G78-F5 (INFO)** `docs-fragments.mjs check` on the clean head prints 2 ADVISORY lines (flow and cheat committed pages lag the render, by design per the script header) and ends `OK` rc 0 (logs/frag_check_clean.log). Not attributable to this PR.

No HIGH or MEDIUM findings. All of the author's numbers that I re-measured matched (4 of 6 red, 50 to 56, 11 to 13 files, tsc 1 identical error).

## 1. Product hunks (read at source; logs/product_diff.log)
- **Changes:** `logger.info('DB save export failed', { error: err instanceof Error ? err.message : String(err) })` becomes a `let reason; try { reason = <same expression>; } catch { reason = 'unreadable thrown value'; } logger.info('<same text>', { error: reason })`. Same shape in `scheduledJobs.ts`.
- **Does NOT change:** the INFO text (`DB save export failed`, `DB save alert rule failed`), the log level (`info`), the key (`error`), the value for any readable thrown value, the return type `Promise<void>`, and nothing is returned or rethrown from either catch. The preceding `memExports.set` / `memAlertRules.push` and the `isDbAvailable()` early return are untouched.
- **Client-returning?** Neither message is. Both go only to `logger.info`. `git diff -U0` on exportService.ts has exactly one hunk, `@@ -56 +56,7 @@` (logs/callers.log); the client-visible `exportResult.error = error instanceof Error ? error.message : 'Unknown error'` (head `:166`, base `:160`) is untouched. The route `POST /exports` returns `exportResult` (`routes/analytics.ts:310-313`), whose `.error` comes from that untouched line, not from `dbSaveExport`'s catch.
- The inner catch is unconditional (no binding), so a secondary error (including a throwing `String(err)` on a null-prototype object) is swallowed and never leaks.

### THE KEY QUESTION: callers (logs/callers.log, logs/handlers.log, logs/handlers2.log, logs/route_create.log; head `276564a7`)
- `dbSaveAlertRule` (`scheduledJobs.ts:30`): callers `scheduledJobs.ts:372` (`defaultRules.forEach(... dbSaveAlertRule(rule).catch(() => {}))`) and `:497` (`addAlertRule`: `dbSaveAlertRule(rule).catch(() => {})`). Both swallow, **author's claim confirmed**. Visible change there: the missing log line is now written.
- `dbSaveExport` (`exportService.ts:30`): four callers, none swallow, **author's claim confirmed**: `:81` `await this.dbSaveExport(exportResult)` in `createExport` (no try/catch around it); `:119` inside `processExport`'s try; `:163` inside the same try; `:167` inside `processExport`'s catch block. `createExport` calls `this.processExport(exportId, request)` at `:84` without `await`. The only caller of `createExport` is `routes/analytics.ts:308`, inside a try/catch that returns 500 `INTERNAL_ERROR` (`:314-327`).
- **Behaviour change.** Before (base): unreadable value, so the catch threw, so (a) `createExport` rejected at `:81` and the route answered 500 with no export started; (b) in `processExport`, a throw at `:119` or `:163` went to the catch, which called `dbSaveExport` again at `:167` and rejected again; a throw at `:167` escaped directly. Because `:84` is not awaited, those rejections were unhandled. After (head): it logs and resolves in all four places.
- **Is that still possible?** Not from the unreadable-value path: the helper's catch cannot throw now. Other throw sources are the code before the try (`memExports.set` and `isDbAvailable()`, neither throws by reading) and `logger.info` itself, which I did not test.
- **unhandledRejection handler in analytics?** No. `git grep` for `process.on(`, `gracefulShutdown`, `shutdown`, `SIGTERM`, `rejection` over `services/analytics/src` (non-test) finds no handler (logs/handlers2.log). `setupGracefulShutdown` (shared, `gracefulShutdown.ts:105`) has no caller anywhere under `Blockchain/Dev/services` (empty "who calls it" result in logs/handlers2.log). The shared handler (`gracefulShutdown.ts:44-71`) exists but is not wired into analytics. So at base an unhandled rejection from `processExport` would hit Node's default behaviour; I did not run that, it is stated from Node's documented default since v15 (crash), not measured.
- **Is "logs and resolves" correct for an export record?** `dbSaveExport` sets `memExports` first (`:31`), then tries the DB. After the change `createExport` returns the pending record (route: 202 `{success:true, data}`) for an export that was never persisted to the DB, and processing continues in memory (`getExport`/`listExports` read `memExports`, `:93-106`). At base, an ordinary `Error` from `query` already takes exactly this path: the catch logs `err.message` and returns, so `createExport` succeeds with an unsaved export. The PR makes the unreadable-value case behave the same as the ordinary-Error case. That is the comparison asked for, and it holds. (Whether a silently unsaved export is itself desirable is a pre-existing design question, out of scope.)

## 2. Red-first and mutants
- Head product + new tests (logs/head_new_tests.log): `Test Files 2 passed (2)`, `Tests 6 passed (6)`, rc=0.
- Base product (develop's two files copied in; sha256 `6801cae02f7e...` / `3ac581288...` per logs/runs_outer.log) + new tests (logs/red_base_new_tests.log): `Test Files 2 failed (2)`, `Tests 4 failed | 2 passed (6)`, rc=1. The 4 failures are R1 and R2 in each file, all `AssertionError: expected [] to have a length of 1 but got +0`; both controls C1 pass. Assertion failures, not import or compile errors. Product restored: `RESTORE_OK` (logs/runs_outer.log), head sha256 `0df3da87abf1...` (exportService.ts), `dd285988c54a...` (scheduledJobs.ts), identical at END.
- Mutants (scripts/mutants.py windowed to the new catch only; mutated the two product files in place, never test files; sha256 equal after every run; logs/mutants2.log, logs/mutants_M8.log, per-run logs/mut_*.log). My first pass (logs/mutants.log) matched the identical loader code from PR 1889 in the same files (pattern count 2) and is superseded; it is kept, not used for the table.

| Mutant | export | scheduled |
|---|---|---|
| M1 fallback constant changed | KILLED (2 failed) | KILLED (2 failed) |
| M2b instanceof hoisted outside inner try | KILLED (1 failed) | KILLED (1 failed) |
| M3 message replaced by String(err) | KILLED (1 failed) | KILLED (1 failed) |
| M4 inner catch rethrows | KILLED (2 failed) | KILLED (2 failed) |
| M5 unguarded `(err as any)?.message` in fallback | KILLED (2 failed) | KILLED (2 failed) |
| M6 non-Error branch to constant `'x'` | SURVIVED | SURVIVED |
| M7 `(err as any)?.message ?? String(err)` | SURVIVED | SURVIVED |
| M8 key `error` renamed `err` | KILLED (3 failed) | KILLED (3 failed) |
| M9 log, then rethrow | KILLED (1 failed, C1) | SURVIVED |
| M10 level info to warn | KILLED (3 failed) | KILLED (3 failed) |
| M11 log call removed | KILLED (3 failed) | KILLED (3 failed) |

Tally: 22 runs (11 mutants x 2 files); 18 killed, 4 survived (M6 and M7 in both files, M9 in scheduled). Findings G78-F1, G78-F2.

## 3. Analytics whole suite and tsc
- Setup: `npm ci --ignore-scripts` rc=0, "added 1795 packages" (logs/npm_ci.log); `packages/shared` build rc=0 (logs/shared_build.log). vitest via `scripts/vt.sh`: `nice 10`, `--maxWorkers=2`, load gate.
- Base product, new tests excluded (logs/base_whole_excl_new.log): `Test Files 11 passed (11)`, `Tests 50 passed (50)`, rc=0.
- Head (logs/after_whole.log): `Test Files 13 passed (13)`, `Tests 56 passed (56)`, rc=0. Matches the author's 50 to 56 and 11 to 13 files. No red.
- tsc with tests in the program (my config scripts/tsconfig.tests.json extends the package tsconfig, drops the `__tests__` exclude, `noEmit`; the author's exact method is unknown). Head: 1 error, `db.retry.test.ts(36,17): error TS2835`, rc=2 (logs/tsc_head.log). Base product with new tests excluded (logs/tsc_base_excl_new.log): the same 1 error. Base product with all tests (logs/tsc_base_product_all_tests.log): the same 1 error. **Identical at base and head; none in the changed files.** Author's claim confirmed. (An earlier run of mine with a bad typeRoots override gave 2 unrelated TS2688 errors; I removed the override and reran. Only the reruns above count.)

## 4. merge-tree
`git merge-tree --write-tree refs/gate/develop refs/gate/pr1893` (develop `85c56a3d1eb9`, head `276564a77171`): **rc 0**, tree `061cf3c8445c629da46d7256088e24cb98e05d6c` (logs/merge_tree.log). Clean. The PR's parent is develop's tip, so it is a fast-forward in content.

## 5. Fragment pair
`node Blockchain/Dev/scripts/docs-fragments.mjs check --root <repo>` on the head: **rc 0**, "flow 117 legacy + 46 new, cheat 112 legacy + 46 new; lint clean, render passes html_docs_check", `OK`, with 2 ADVISORY lines (G78-F5) (logs/frag_check_clean.log). After all plants were restored: the same result (logs/frag_check_after_restore.log).
Planted defects, each restored by sha256 compare (all four printed `restore OK`, logs/frag_*.log via scripts/frag.sh):
- Unbalanced `<div>` appended to the flow fragment: rc 1, `<div> opened 2, closed 1`, FAIL (logs/frag_check_planted_flow_div.log).
- Same in the cheat fragment: rc 1, `<div> opened 4, closed 3`, FAIL (logs/frag_check_planted_cheat_div.log).
- Flow `<!--n-->.` token removed from the `<h2>`: rc 1, "the <h2> must start with <!--n-->.", FAIL (logs/frag_check_planted_flow_2.log).
- Cheat `</table>` corrupted to `</tabl>`: rc 1, `<table> opened 3, closed 0`, FAIL (logs/frag_check_planted_cheat_2.log).
Fragment content claims checked against what I measured: 6 cells, 4 of 6 red, 50 to 56, 11 to 13 files, tsc 1 identical error, callers analysis, line 160 untouched. All match. Its "npm ci was not run" is true of the author; I ran it (rc 0). The author's "resolves" wording in the flow fragment is a Promise term and harmless.

## 6. END heads
See Heads (logs/head_end.log). Unchanged from START.

## NOT TESTED
- A real database failure against a booted analytics service; the callers' behaviour (createExport 500 before, 202 after; unhandled rejection before) is read from source, not exercised.
- Node's default unhandled-rejection behaviour in this service (stated from Node's documented default, not run).
- A rethrow limited to the unreadable path in `dbSaveExport` (inferred from reading R1/R2, G78-F2; mutant not run).
- `logger.info` itself throwing inside the catch.
- eslint (author reports 0 errors; I did not run it), the four platform suites, Node 24 or an LTS Node (ran on v26.8.1), any deploy.
- The other KS-1868 sites, the stored message at `exportService.ts:166` (KS-1922) and `dbSaveAlert`, all out of scope per the PR.
