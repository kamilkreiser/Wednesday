# QA Gate 74 verdict: Secuura/Distributed_Secuura PR 1889 (KS-1868, analytics O40-P1 + O40-P2), tier 2

## BLUF
**GO WITH NOTES.** Both product hunks are correct and minimal (+7/-1 each). The WARN text, key and value for any readable thrown value are unchanged; the only behaviour change is that an unreadable thrown value now logs the constant `unreadable thrown value` instead of the catch throwing. Red-first confirmed by assertion (4 of 6 fail at base product, 6 of 6 pass with it). Analytics suite 44/44 at base, 50/50 at head, no red. merge-tree rc 0. File-disjoint from PR 1867. Notes are test-coverage gaps only (G74-F1) and two informational items; none blocks merge.

## Heads
- START (ls-remote origin, 14:3x AEDT window): PR head `039cba4a69072539935927f9d19d5a1409401e5d`, develop `b1fb543640e7a439a9344d1d96d5a62862edfcf5` (logs/head_start.log; fetch into refs/gate/pr1889, refs/gate/develop matched).
- END: PR head `039cba4a69072539935927f9d19d5a1409401e5d`, develop `b1fb543640e7a439a9344d1d96d5a62862edfcf5` (logs/head_end.log). Did not move. One commit on base `a71479b49bf3` (merge-base verified through diff against it).

## FINDINGS
- **G74-F1 (LOW, test gap)** `exportService.ts:296-300` and `scheduledJobs.ts:150-154`: no cell exercises the readable non-Error branch (`String(err)` for a string or plain-object throw) nor a throw where `String(err)` itself throws (e.g. `Object.create(null)`). Mutant M6 (non-Error branch replaced by constant `'x'`) and M7 (`(err as any)?.message ?? String(err)`) SURVIVE in both files. Not a product defect; the new branch is covered, the old one is not, and it is unchanged by this PR.
- **G74-F2 (INFO, behaviour not tested)** The loaders are awaited in `Promise.all` inside `loadStoresFromDb` (`index.ts:104-112`, passed to `initDb` as onReady). Before: an unreadable thrown value made the catch throw, the loader rejected, `Promise.all` rejected and the "All in-memory stores loaded" log was skipped. After: the loader resolves, the WARN is logged and the "All ... loaded" info line prints, exactly as for an ordinary Error today. This is the intended outcome (the fragment says so) but it is a startup-path change that no test and no real service start covers (author lists "real service start" as NOT done; confirmed).
- **G74-F3 (INFO)** `docs-fragments.mjs check` on the clean head prints two ADVISORY lines (committed flow/cheat pages differ from the render, a by-design lag per the script header) and still ends `OK`, rc 0. Not attributable to this PR; not compared against the base.

No HIGH or MEDIUM findings.

## 2. Product hunks (read at source)
Both edits are identical in shape. Before: `logger.warn(msg, { error: err instanceof Error ? err.message : String(err) })`. After: `let reason: string; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; } logger.warn(msg, { error: reason })`.
- **Does NOT change:** WARN message strings (`ExportService.loadFromDb failed — starting with empty store`, `loadScheduledJobsFromDb failed — starting with defaults only`), the `error` key, the logged value for any readable thrown value, the return (`Promise<void>`, resolves; neither catch returns or rethrows), the stores left empty/default.
- **Changes:** only the unreadable case: previously the read threw inside the catch (WARN lost, promise rejected); now logs the constant and resolves.
- **Revoked Proxy:** `instanceof` on a revoked proxy throws TypeError; it is inside the inner try, so it is caught. Verified by test R1 and by mutant M2b (instanceof hoisted outside the try is KILLED in both files).
- **Throwing message getter:** `.message` is inside the inner try, caught. Verified by R2; M1/M4/M5 killed.
- **Client-returning?** Neither catch is. They are boot-time hydration loaders that only log. `exportService.ts:160` (`exportResult.error = error instanceof Error ? error.message : 'Unknown error'`, the client-visible record) is UNTOUCHED: the diff has hunks only at 296 and 303 of that file (`git diff -U0`); line 160 on the head reads identically to base.
- Side note: a throw from `String(err)` (null-prototype object) is also caught, which is better than base. The inner catch is unconditional (no `catch (e)` binding), so nothing about the secondary error leaks.

## 3. Red-first and mutants
- Base product + new tests (logs/red_base_new_tests.log): `Tests 4 failed | 2 passed (6)`, rc=1. The 4 failures are R1 and R2 in each file, all `AssertionError: expected [] to have a length of 1 but got +0` (assertion, not import/compile error). Controls C1 pass. Whole suite at base product with new tests (logs/base_product_whole.log): `Test Files 2 failed | 9 passed (11); Tests 4 failed | 46 passed (50)`.
- Head product (logs/after_whole.log): all 6 pass.
- Mutants (scripts/mutants.py, logs/mutants.log, logs/mutants_M2b.log; mutated the two product files in place, never under src/__tests__, sha256 verified restored after each, final tree equals head):

| Mutant | export | scheduled |
|---|---|---|
| M1 fallback string changed | KILLED | KILLED |
| M2b instanceof hoisted outside inner try | KILLED | KILLED |
| M3 message replaced by String(err) | KILLED | KILLED |
| M4 inner catch rethrows | KILLED | KILLED |
| M5 unguarded `(err as any)?.message` in the fallback | KILLED | KILLED |
| M6 non-Error branch -> constant 'x' | SURVIVED | SURVIVED |
| M7 `(err as any)?.message ?? String(err)` | SURVIVED | SURVIVED |
| M8 WARN key renamed | KILLED | KILLED |

My first M2 (instanceof hoisted via an IIFE) was an equivalent mutant (still inside the try) and was replaced by M2b; both are in the logs. Tally: 16 valid runs (8 mutants x 2 files, M2 replaced by M2b); 12 killed, 4 survived (M6 and M7 in both files, G74-F1). The discarded equivalent M2 is excluded.

## 4. Analytics whole suite
- Base product, new tests excluded (logs/base_whole_excl_new.log): `Test Files 9 passed (9); Tests 44 passed (44)`, rc=0.
- Head (logs/after_whole.log): `Test Files 11 passed (11); Tests 50 passed (50)`, rc=0. Matches the author's 44/44 -> 50/50. No red.
- Setup: `npm ci --ignore-scripts` rc=0 (logs/npm_ci.log, 1795 packages); `@secuura/shared` build rc=0 (logs/shared_build.log); then vitest 4.1.12, Node v26.8.1, nice 10, maxWorkers=2.

## 5. merge-tree
`git merge-tree --write-tree b1fb543640e7 039cba4a6907`: **rc 0**, tree `21fb8c2eab05815d878e2979839334e501cdc529` (logs/merge_tree.log). Clean. Nothing in a71479b49bf3..develop touches any of the 6 PR paths.

## 6. File-disjointness from PR 1867
PR 1867 = commit 033a26e8 (ancestor of base). Its 6 files (analyticsService.ts, metricsCollector.ts, two tests, two KS-1868-analytics-unreadable-thrown-value fragments; logs/pr1867_files.log) vs this PR's 6 files (exportService.ts, scheduledJobs.ts, two tests, two ...export-jobs... fragments; logs/pr1889_files.log): `comm -12` intersection empty. Confirmed disjoint.

## 7. Fragment pair
`docs-fragments.mjs check --root <repo>` on the head: rc 0, "lint clean, render passes html_docs_check", OK (logs/frag_check_clean.log), with the two advisory lines of G74-F3. Planted defect (an unclosed `<div>` appended): flow fragment -> rc 1, `tags are not balanced: <div> opened 1, closed 0`, FAIL; cheat fragment -> rc 1, `<div> opened 3, closed 2`, FAIL (logs/frag_check_planted_flow.log, _cheat.log). Each fragment restored by sha256 compare. Fragment content claims (6 cells, 44->50, line 160 untouched) match what I measured.

## NOT TESTED
- Real service start against a failing database (G74-F2).
- The other KS-1868 sites, `exportService.ts:160`, `dbSave*` catches (KS-1922).
- tsc-with-tests and eslint (author's claims of 1 pre-existing TS2835, eslint 0/0 not re-run).
- The four platform suites, the push-hook preflight (13/16 legs, 3 skipped per the author), any LTS Node (host v26.8.1), any deploy.
- Fragment advisory lag at base.

## HOW
Clone: `git clone --shared --no-checkout` from gate65 repo into `.../gate74-ks1868-analytics-1889/repo`; `origin` set to the Secuura URL with push disabled (`no_push_qa_gate`) and the Secuura deploy key via repo-local core.sshCommand (the shared-clone default had none, first fetch failed publickey); fetched PR head and develop into refs/gate/*. `git rev-parse --show-toplevel` asserted before the write verbs. Runner: scripts/vt.sh (nice 10, waits while load1 > 8, stderr kept in logs). Mutants: scripts/mutants.py (sha256 restore). No writes to GitHub, Linear, mail or !CODING. Final `git status --short` in the clone: clean; HEAD = 039cba4a.
Logs: `.../gate74-ks1868-analytics-1889/logs/`.
