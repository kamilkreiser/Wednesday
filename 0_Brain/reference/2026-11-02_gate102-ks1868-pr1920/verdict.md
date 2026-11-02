# QA Gate 102 verdict: Secuura/Distributed_Secuura PR 1920 (KS-1868, services/analytics scheduledJobs.ts dbSaveAlert catch, O64-P1), TIER 2 confirmed

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the real `dbSaveAlert` (a copy of the product file with one `export` appended) and the real `ScheduledJobs.acknowledgeAlert` path, at base and at head, with only `../db` and `../utils/logger` replaced (logs/probe_base.jsonl, probe_head.jsonl; scripts/probe_template.test.ts, quarantined copies in _quarantine/). For an ORDINARY Error (and a ZodError-like Error, and a thrown string) base and head are identical: one `DB save alert failed` INFO line carrying the message, `dbSaveAlert` resolves, the INSERT was attempted once and failed, nothing persisted. For an UNREADABLE value (revoked Proxy, Error with a throwing `message` getter) base writes NO line and `dbSaveAlert` itself REJECTS (swallowed by the caller's `.catch(() => {})`); head writes the line with `error: 'unreadable thrown value'` and resolves, exactly the shape an ordinary Error already gets. Nothing reaches a response or persisted state: in the `acknowledgeAlert` cells base and head are identical in return value (true), in-memory acknowledgement (set), query count (1) and unhandled rejections (0). The class is not even constructed in production code. Tier 2 stands; operator 64's tier 3 would also be defensible, but the change is a one-line log fix with no data path, so I confirm the author's tier 2 (the higher of the two; nothing here argues for lower).
Every other author figure re-measures exactly. One mutant survives (M5, see G102-F1), a consequence of the swallowing caller, not a defect.

## Heads
- START (logs/head_start.log, 2026-11-02 ~13:05 local): `refs/pull/1920/head` = `e10939d03558864ae38a5f87227fcedcfd5140d6` (matches), develop `92a26320e30ad680459cdb96c5b68b91a5f175a5` (matches). merge-base HEAD..origin/develop = `92a26320...` = develop, so the PR is a fast-forward.
- END (logs/head_end.log): PR head `e10939d0...` unchanged, develop `92a26320...` unchanged, local HEAD `e10939d0...`, product sha256 `d6021182307f0df7...` identical to start, working tree clean.
- Repo layout note: product paths are under `Blockchain/Dev/services/analytics/...` (the PR mail abbreviates them).

## 1. Diffstat (logs/diffstat.log; three-dot against origin/develop)
4 files, +150/-1, exactly as claimed: `scheduledJobs.ts` +7/-1 (diff says 8 lines changed), the new test +102, two fragments +21 and +20 (one pair). Nothing outside those paths. One commit.

## 2. The hunk (only product change)
```
-    logger.info('DB save alert failed', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.info('DB save alert failed', { error: reason });
```
The read moves into its own try; the log call is the same message, level (info) and key. Not changed: the INSERT and its parameters, the early `memActiveAlerts.push` and `isDbAvailable` return, the other two catches in the file (dbSaveAlertRule :63 and loadScheduledJobsFromDb already carry the same guard; the file now holds 3 copies), `acknowledgeAlert`, any other file. Same inline guard as the file's own siblings, so the pattern is consistent.

## 3. The behaviour question (RUN, not only read)
Method: logs/probe_{base,head}.jsonl. `direct/*` calls the real `dbSaveAlert` (exported in a copy); `ack/*` builds a real `ScheduledJobs`, raises a real alert through `evaluateAlerts`, and calls the real `acknowledgeAlert`, with the db stand-in rejecting the INSERT with each value. Logger is a recorder. Process-level `unhandledRejection` listener counts leaks.

| thrown value | direct dbSaveAlert base | direct head | log line base | log line head | ack path: return / in-mem ack / queries / unhandled base = head |
|---|---|---|---|---|---|
| ordinary Error('db down') | resolves | resolves | `DB save alert failed {error:'db down'}` | same | true / set / 1 / 0 |
| ZodError-like Error (name ZodError, issues) | resolves | resolves | `{error:'zod issue'}` | same | same |
| string | resolves | resolves | `{error:'plain string failure'}` | same | same |
| revoked Proxy | **REJECTS** | resolves | **none** | `{error:'unreadable thrown value'}` | same |
| Error with throwing message getter | **REJECTS** | resolves | **none** | `{error:'unreadable thrown value'}` | same |

- **Job continues:** acknowledgeAlert returns true and sets `acknowledgedAt` in memory in every cell, base and head; `logger.info('Alert acknowledged')` is written in all 10 ack cells.
- **Persisted alert row:** the INSERT is attempted once in every cell and fails in every cell, so no row is written at base or head (modelled: the db stand-in rejects; no real DB, see NOT TESTED). The change adds no write, no retry, no second query.
- **Unhandled rejections:** 0 in all 20 cells at both versions. At base the unreadable-value rejection is real (direct cells) but is swallowed by the caller; head removes the rejection altogether. (The listener runs inside vitest, which also traps rejections; the 0 for base is explained by the `.catch`, and the direct cells show the rejection itself.)
- **Zod:** there is no Zod pre-check at this site; the ZodError-like cell is just an ordinary Error with extra properties and is treated like one (message only).
- **Callers (git grep over the whole clone, logs in this section; positive control = the test files match):** `dbSaveAlert` is module-private (:69) with exactly ONE call, `acknowledgeAlert` :492 `dbSaveAlert(alert).catch(() => {})`. `acknowledgeAlert` has no caller outside the definition and tests. `ScheduledJobs` is not instantiated anywhere in production code (`new ScheduledJobs` appears only in the two ks1868 tests; production only imports `loadScheduledJobsFromDb`, index.ts:18/109). So the class's alert-ack path is currently not reachable from a request or a boot. Nothing new reaches a response, and the only persisted state (the alert row) is unchanged. This confirms the author's claim and goes one step further: not just no caller response, but no production instantiation (read from source).
- **Why operator 64's tier 3 was reasonable:** a log-only change in a swallowed, currently unreachable path. I keep tier 2 because the PR does change an observable outcome of the function (reject to resolve) and the author proposed 2; either way no fix is needed.

## 4. Re-measure
- **Red first (logs/red_base_new.log):** base product + new test only: 4 cells, 2 passed (C1, C2), **2 failed by assertion** (R1, R2: `AssertionError: expected [] to have a length of 1 but got +0`). Head: 4/4 (logs/head_new.log).
- **Whole analytics suite (vitest, Node v26.8.1, NOT Node 24):** base without the new file **17 files 104/104** (logs/base_whole_excl_new.log); base + new test 18 files 106 passed, 2 failed (logs/base_whole_incl_new.log); head **18 files 108/108** (logs/head_whole.log, again at the end: logs/head_whole_final.log). Ratio 104 -> 108 = the 4 new cells; nothing else changed. Note: needed `@secuura/shared` linked and built (`npm ci --ignore-scripts` skips the postinstall build; I built it with tsc); without it 5 files fail to import, before and after alike (setup, not a PR matter).
- **tsc:** plain `tsc --noEmit` rc 0 at head. With the tests in the program (scratch tsconfig in scripts/, outside the PR): 1 error at head and the same 1 at base, `src/__tests__/db.retry.test.ts(36,17) TS2835` (pre-existing, not a changed file); sorted lists identical (logs/tsc_diff.log, rc 0). Planted control (`const x: number = "x"` in a scratch test) is reported by file name (TS2322, TS6133).
- **eslint 10.7 (cwd services/analytics, repo eslint.config.mjs):** the two changed files 0 errors 0 warnings, rc 0. Planted file: `no-debugger` error + `no-unused-vars` warning, rc 1. (Eslint and its config packages were installed with `npm install --no-save` unpinned because `npm ci` of the workspace subset skipped root devDependencies; versions may differ slightly from the lockfile.)
- **docs-fragments check:** rc 0, "flow 117 legacy + 72 new, cheat 112 legacy + 72 new; lint clean, render passes", with the same 2 ADVISORY lines the author says are not new (they are about the committed pages' pmatrix at lines 6249/6235 and are not in this PR's files). Planted defect (an unclosed `<div>` appended to the flow fragment): rc 1, names the fragment; restored by sha256 and rc 0 after.

## 5. Mutants (scripts/mutants.py; product only, tests untouched; sha256 restored after each run, all `restore True`; logs/mutants_table.log)
10 mutants at the one site: **9 killed, 1 survived.**

| mutant | result | cells red |
|---|---|---|
| M0 revert to base line | KILLED | R1 R2 |
| M1 drop the inner try | KILLED | R1 R2 |
| M2 constant -> `String(err)` | KILLED | R1 R2 |
| M3 rethrow only when unreadable (`throw err` in the inner catch) | KILLED | R1 R2 |
| M4 constant for every value | KILLED | C1 C2 |
| **M5 rethrow every value after the log** | **SURVIVED** | none (4/4 green) |
| M6 readable non-Error branch -> `'x'` | KILLED | C2 |
| M7 log removed | KILLED | C1 C2 R1 R2 |
| M8 constant text changed to `'unreadable'` | KILLED | R1 R2 |
| M9 also log the thrown value (`value: err`) | KILLED | all 4 (toEqual on the whole object) |

M5 survives because the test goes through `acknowledgeAlert`, whose `.catch(() => {})` hides whether `dbSaveAlert` itself resolves. That is G102-F1. M9 is worth noting: the whole-object `toEqual` makes a value-leaking extra key fail.

## 6. merge-tree (logs/merge_tree.log, merge_result_vs_develop.log)
`git merge-tree --write-tree origin/develop pr1920` onto develop `92a26320` (unchanged at start and end): **rc 0, tree `860270e4dd3cb90f7c538550f909aefb34e640c5`**, clean (same tree id the author reports). Diff of that tree against develop lists exactly the PR's 4 paths. Develop equals the PR base, so there is no overlap to check.

## 7. Kam's ks1346 logging rule (log type and field names, never values)
The only new log write is `logger.info('DB save alert failed', { error: reason })`. On the unreadable path `reason` is the literal constant `'unreadable thrown value'`: no value, no type, no field names, nothing from the thrown object. Verified by M9 (adding the value fails 4 cells) and by the probe (head log for unreadable values is the constant only). The ordinary-Error path is unchanged: it still logs `err.message` (or `String(err)` for a non-Error), which is the pre-existing line, not new, and is a message string rather than an object. Whether a driver message can embed row values (e.g. a unique-violation detail) is not examined here; it is pre-existing and not touched (G102-F3). The log call is also not a new leak channel in volume: one line per failed save, as before for ordinary values.

## FINDINGS
- **G102-F1 (LOW, test gap, measured):** mutant M5 (rethrow every value after logging) survives. No cell can see whether `dbSaveAlert` resolves, because it is module-private and reached only through the swallowing `acknowledgeAlert`; the PR's claim "it resolves" is therefore proven only by this gate's probe, not by a committed cell. Optional: assert `jobs` has no unhandled rejection, or export `dbSaveAlert` for test. Not worth blocking: the behaviour is swallowed in the only caller.
- **G102-F2 (INFO, measured/read):** `ScheduledJobs` is not instantiated in any production code (only `loadScheduledJobsFromDb` is imported by index.ts). The path is test-only today; the fragment and body could say so. Reduces risk further and supports tier 2 or 3.
- **G102-F3 (INFO, pre-existing, not this PR):** the ordinary-Error log still carries `err.message` verbatim; a driver message may embed values. Same as the file's other two catches. Belongs with the ks1346 sweep, not here.
- **G102-F4 (INFO, doc wording):** the fragment says "the INFO line is now written" accurately, but the PR body/fragment can add that `dbSaveAlert` itself no longer rejects for an unreadable value (it did at base; swallowed by `.catch`). Cosmetic.
- **G102-F5 (INFO, left-out candidate, agree with the author):** analytics `exportService.ts :166` sets `exportResult.error` from a thrown value unguarded; different shape (stored export record), correctly left for a decision.
- **G102-F6 (INFO, same note as gates 90/96):** the docs-fragments check prints two ADVISORY lines (committed pages lag the render at lines 6249/6235); they appear without this PR's files too (author reports the scratch control; I did not re-run without the PR files, they concern the pmatrix tables the PR does not touch).

## 8. Notes for the PR body
1. G102-F4: add one line that `dbSaveAlert` rejected for an unreadable value at base (swallowed) and now resolves, with the table in section 3.
2. G102-F2: say that `ScheduledJobs` has no production instantiation (git grep), so the reachable behaviour change today is nil.
3. G102-F1: optional, name the M5 gap as a known limit of testing through a swallowing caller.
None is FIX-BEFORE-MERGE.

## 9. NOT TESTED
- The PR body text itself (no gh login for this account; I used the author's READY and BUILT AND PROVEN mails in evidence/); a real PostgreSQL (the INSERT failure is a stand-in, "no row persisted" is a model); a booted analytics service or HTTP request (none can reach this path); Node 24 (host is v26.8.1, every figure is Node 26); the four platform suites; CI; the pre-push hook legs (quoted from the mail only); eslint at the lockfile's exact version; the docs-fragments check with the PR's files removed.
- Setup side effects inside my clone only: `npm ci` for two workspaces, an unpinned `npm install --no-save` of eslint config packages, a tsc build of `packages/shared`. No file in the clone's tracked tree differs from the PR head (git status clean), no push, no GitHub/Linear/mail writes.
