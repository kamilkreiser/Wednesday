# QA Gate 75 verdict: Secuura/Distributed_Secuura PR 1890 (KS-1868, demo-service boot gate O34-P1), tier 2

## BLUF
**GO WITH NOTES.** The product hunk (index.ts +6/-1) only changes how the thrown value is turned into text. The log string, key and exit code for a readable value are unchanged, and the gate still logs FATAL and exits 1 on every path I tried, including the unreadable ones. The new test is red at base by AssertionError and green with the change. The whole suite is green at base and head. Merge-tree is clean and the PR is disjoint from develop and from PR 1870. The notes are test-strength gaps (3 mutants survived, 1 of them probably equivalent); none is a product defect.

## Heads
- Start (logs/head_start.log): PR head `b4378a3012d38646661f36a0b96dcf53d1d3dea4` (matches the brief), develop `b1fb543640e7a439a9344d1d96d5a62862edfcf5`.
- End (logs/head_end.log): identical to start (diff of the two logs: UNCHANGED).
- Merge base of develop and PR: `a71479b49bf319a6349eb1450c13ef6a9f235a77` (git merge-base, in the Q4 session; stated by the author as a71479b49bf3).

## FINDINGS
- **G75-F1 LOW** `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts:44-55` (hunk at `src/index.ts:40-45`): mutant M12 (process.exit(1) moved BEFORE logger.error) survived, because the test mocks process.exit as a no-op, so call order is not asserted. A change that exits before logging would pass. Evidence: logs/mut_M12.log, logs/mutants_summary.log.
- **G75-F2 LOW** same test file: mutant M11 (non-Error branch replaced by constant 'x') survived. No test throws a non-Error readable value (string, number, null), so `String(err)` for those is unpinned. My ad-hoc probe shows the product handles them correctly. Evidence: logs/mut_M11.log, logs/probe_out.log.
- **G75-F3 INFO** `src/index.ts:42`: M9 (dropping the outer `String()`) survived; it is behaviourally equivalent for the template-literal use except when an Error's `message` is a non-string, so I treat it as a probable equivalent mutant. Evidence: logs/mut_M9.log.
- **G75-F4 INFO** Test coverage of the unreadable class: the committed test pins only the revoked-Proxy case. The other two cases named in the brief (throwing `.message` getter on an Error, null-prototype object) plus a throwing `toString` work in my uncommitted probe (not part of the PR) but are not in the PR's test. Evidence: logs/probe_out.log, logs/probe_variants.log.
- **G75-F5 INFO** Wording in the fragment (`flow` fragment, "What this changes"): says that on an unreadable value "process.exit(1) never runs". True of that line, but the base process does not proceed: the uncaught TypeError terminates node with rc 1 (emulation of the base catch shape: logs/base_emul.log). So the base already failed closed by crashing; the change adds the FATAL log line and a controlled exit. It is an improvement in diagnosability, not a closing of an open gate. Not a defect.
- **G75-F6 INFO** `docs-fragments.mjs check` on the head prints two ADVISORY lines (committed flow and cheat pages differ from the render, lines 6249 and 6235). The PR touches neither page; by the script's own header the committed pages lag the fragments by design. I did not run the check at base, so I cannot say whether these advisories pre-exist. Evidence: logs/frag_check.log.

## 1. Product hunk at source
Diff (`git diff HEAD~1 HEAD` on index.ts, read at b4378a30): the single changed statement in the catch of `assertDemoServiceEnabled()`:
- before: `const message = err instanceof Error ? err.message : String(err);`
- after: `let message: string; try { message = String(err instanceof Error ? err.message : err); } catch { message = 'unreadable thrown value'; }`

Unchanged (read at source, index.ts lines 37-48): the log call `logger.error(\`FATAL: ${message}\`)`, the process.exit(1) call and its code, the gate placement before `createApp()` (line 50) and `app.listen`. There is no key or metadata in that log call. The catch is log-and-exit only; it does not touch a response, so it is not client-returning.

Behaviour (logs/probe_out.log, uncommitted probe test, 8 of 8 pass, logs/probe_variants.log; each case recorded the logged line and an exit call of 1):
- throwing `.message` getter on an Error: "FATAL: unreadable thrown value", exit [[1]]
- null-prototype object: "FATAL: unreadable thrown value", exit [[1]]
- object with throwing toString: "FATAL: unreadable thrown value", exit [[1]]
- readable values: string, undefined, null, number, Symbol log their String() form, exit [[1]]
- revoked Proxy: pinned by the PR's own test R1 (green, logs/green_head_new.log: 2 passed).

Fail closed, real process: tsx boot of the real src/index.ts at the head: NODE_ENV=production gives the production-refusal FATAL line and rc=1 (logs/realboot_prod.log); NODE_ENV=development with no opt-in gives the DEMO_SERVICE_ENABLED FATAL line and rc=1 (logs/realboot_noopt.log). In neither case did the process reach listen. Verdict: the change cannot turn the gate into a pass. Mutant M4 (exit removed) and M5 (exit 0) are both killed (2 of 2 cells fail), so the test does guard the exit. Not tested: a real boot with an unreadable thrown value (the real gate only throws Errors); that path is covered via the mocked test only.

## 2. Red-first and mutants
Red at base: base index.ts restored over the head file (sha restored after), whole suite run with the new test present (logs/red_base.log): "1 failed | 90 passed (91)", the failure is R1, `AssertionError: expected "vi.fn()" to be called with arguments: [ 'FATAL: unreadable thrown value' ]`. No import or compile error. Control C1 passes at base. With the product: new test file alone 2 passed (logs/green_head_new.log).

Mutants on the hunk (tests = the new file, 2 cells; head index.ts sha256 d7812b57...a6351 verified identical after every mutant, and at the end: logs/mutants_summary.log):

| id | mutation | result |
|---|---|---|
| M1 | fallback string changed | KILLED (1 failed) |
| M2 | read hoisted outside inner try | KILLED (1 failed) |
| M3 | inner catch rethrows | KILLED (1 failed) |
| M4 | gate proceeds (exit removed) | KILLED (2 failed) |
| M5 | exit code 0 | KILLED (2 failed) |
| M6 | inner catch leaves message unset | KILLED (1 failed) |
| M7 | Error.message dropped, String(err) | KILLED (1 failed) |
| M8 | FATAL prefix changed | KILLED (2 failed) |
| M9 | outer String() dropped | SURVIVED (probable equivalent, F3) |
| M10 | instanceof check dropped | KILLED (1 failed) |
| M11 | non-Error branch to constant | SURVIVED (F2) |
| M12 | exit before log | SURVIVED (F1) |

9 of 12 killed, 3 survived. Logs: logs/mut_M1.log ... logs/mut_M12.log.

## 3. Whole demo-service suite
Setup: `npm ci --ignore-scripts` rc 0, 1795 packages (logs/npm_ci.log); packages/shared built first with tsc rc 0 (logs/build_shared.log); vitest nice 10, maxWorkers=2, node v26.8.1.
- Base product, new test excluded: 10 files / 89 of 89 passed, rc 0 (logs/suite_base.log).
- Head: 11 files / 91 of 91 passed, rc 0 (logs/suite_head.log).
Both match the author's counts. (The probe test file I added in my clone was excluded from both runs.) The author's 37 s vs 2 s timing was not reproduced as a comparison: mine were 2.19 s base and 1.56 s head, both after install.

## 4. Merge-tree and develop overlap
`git merge-tree --write-tree refs/gate/develop refs/gate/pr1890`: rc 0, tree f7b7f48b64903d28657e05fab9254d6dff8a9346, no conflict lines (logs/merge_tree.log). base..develop changes 59 files (logs/base_develop_files.log); intersection with the PR's 4 paths is empty (logs/overlap_develop.log, grep rc 1); 0 commits on develop since base touch services/demo-service (logs/develop_demo_commits.log).

## 5. Disjointness from PR 1870
PR 1870 head `7388d629ea88851ad82c282c4b217d2b2c727b55`. Its files (logs/pr1870_files.log): scenario.ts, ks1868-scenario-context-unreadable-throw.test.ts, and fragment pair `KS-1868-demo-service-unreadable-thrown-value.html` (cheat and flow). PR 1890's files (logs/pr_files.log) differ in all four; overlap is empty (logs/overlap_1870.log, rc 1). Merge-tree of the two heads: rc 0 (logs/merge_tree_1870_1890.log). Fragment names differ, so no fragment collision.

## 6. Fragment pair
`node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>` on the head: rc 0, "flow 117 legacy + 40 new, cheat 112 legacy + 40 new; lint clean, render passes html_docs_check", with two ADVISORY lines (F6) (logs/frag_check.log). Planted defect (an unclosed div/span appended) per fragment: flow rc 1 "FAIL - 1 finding(s)" (logs/frag_planted_flow.log), cheat rc 1 "FAIL - 1 finding(s)" (logs/frag_planted_cheat.log). Each restored by sha256 (flow 012de16c...f7d72, cheat 89bf1388...6096); check after restore rc 0 (logs/frag_check_after.log).

## 7. End heads
logs/head_end.log equals logs/head_start.log. Neither the PR head nor develop moved.

## NOT TESTED
- The other ~252 sites of KS-1868, and anything outside services/demo-service.
- A real boot where the gate throws an unreadable value (not reachable with the real gate).
- eslint and tsc results claimed by the author (not re-run).
- The four platform suites, any LTS Node (host is v26.8.1), any deploy, the author's preflight/hook claims, Linear/GitHub state.
- Whether the docs-fragments ADVISORY lines pre-exist at base.
- Probe test and base-catch emulation are mine, uncommitted, kept only in the work dir (repo/.../g75-probe.test.ts, scripts/base_catch_emul.js); the PR is unmodified (index.ts sha256 restored; the only untracked file in the clone is the probe).
