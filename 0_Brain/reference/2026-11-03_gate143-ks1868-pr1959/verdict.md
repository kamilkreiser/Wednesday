# QA Gate 143 verdict: Secuura/Distributed_Secuura PR 1959 (KS-1868, auth service events.ts: Redis init catch + 'error' listener), TIER 2, round 1 (RESUMED run)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** One product hunk set (+16/-2 in `events.ts`, two guards of identical text), two new test files (10 cells), two docs fragments. I ran the real `events.ts`, base and head, in a child process with only `ioredis` replaced by an EventEmitter stand-in and the REAL winston logger, in the development and production formats: 14 values x 2 sites x 2 formats x 2 versions = **112 runs**, stderr empty. For an unreadable value, head equals what an ORDINARY Error already gets (one log line, boot continues, `initEventBus` answers false / listener process lives); base threw out of `initEventBus` (boot ends exit 1 via start()'s `.catch`) or raised an uncaughtException from the listener. Mutants: 18 runs, 14 killed, **4 survived** = two branches (drop `?.` on `err?.message`; null message as text) x 2 sites: a test gap (G143-F1, recommended follow-up). Not measured on Node 24 (host Node v26.8.1).
PR 1953 (zod 4): none of the PR's 5 paths is among its changed paths; `events.ts` imports only `ioredis` and the local logger (no zod). Develop moved THREE times during the gate; merge-tree is clean onto the latest (see 6).

## Resume statement (what was accepted, what was re-run)
The first runner died at 05:34 AEDT 2026-11-03. `ps` at resume showed NO process with this workdir, vitest or tsx: nothing to stop. The clone: push URL `no_push_qa_gate` (verified), core.sshCommand set, HEAD = `pr1959` = `a3c6feea...` (matches the pin); one stray untracked file `src/events_base.ts` (the predecessor's base copy, used by its scripts) was moved to logs/_quarantine/ at the end; `git status` clean after, `events.ts` sha256 equals the head blob.
- ACCEPTED on the first runner's logs (each log complete, rc present, restore recorded): clone/fetch/diffstat; npm ci + shared build (rc 0); probe matrix (112 lines, complete, stderr empty); red/green cells (cells_base.log, cells_head.log); mutants (18 results + "restored sha ok"); suites (suite_head_run1/2, suite_base_run1, each with .rc and a full vitest summary; suite_restore.ok, suites.done); q5/q5b (patch independence); first merge-tree onto cc33e702.
- RE-RUN by me: heads at start/end; merge-tree onto the latest develop (the first one was onto cc33e702, develop has since moved to 0bd5e7bf); PR 1953 overlap; tsc with tests (head and base) and own tsconfig; eslint with a planted defect; the test-types ratchet; docs-fragments check with two planted defects; caller re-read at the new line number.
- NOT redone: a second base suite run (the base run failed on the same flaky ks949 cell as head run 1; see 4).

## Heads
- First runner START (logs/head_start.log, 18:26:44Z): PR head `a3c6feeab5e11c16446896718906e13a55c56f4a`, develop `4307ac87` (PR 1956 merged). Merge-base with the PR: `2d3b3bb3d386` (develop at PR creation).
- My RESUME START (logs/head_resume_start.log): PR head `a3c6feea...` (unchanged); develop `0bd5e7bf62ac81e15450dd712e0427c4cede918c` (PR 1957 merged on top of 1953). END (logs/head_resume_end.log): PR head `a3c6feea...`, develop `0bd5e7bf...`: both unchanged across my work. The PR head never moved.
- **PR body not read** (no `gh` login); used the author's READY mail (evidence/w19_pr1959_ready.txt).

## 1. Diffstat (logs/diffstat.log)
5 files, +261/-2, as declared: `events.ts` 16/2; two test files 108/0 each; flow fragment 11; cheat fragment 18. Nothing outside the declared paths (three-dot vs 2d3b3bb3).

## 2. The hunks (logs/events.patch)
One hunk of two sites in `Blockchain/Dev/services/auth/src/events.ts`:
- Redis `'error'` listener: `-  logger.debug('EventBus Redis error (non-fatal)', { error: err.message });` `+` the guard `let reason: string|null|undefined; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; }` then the same `logger.debug(..., { error: reason })`.
- `initEventBus` catch: `-  logger.warn('Failed to initialise EventBus', { error: err?.message });` `+` the same guard, then `logger.warn(..., { error: reason })`; still `return false`.
Does NOT change: log message text, levels, keys; the returned booleans; the publish path, the `redis` config or retry; no other file in the service. Independent reconstruction of head from base + P3 + P1 equals head byte for byte, in either application order (logs/q5b.log); the guard text equals the one in the merged PRs 1956/1957.

## 3. Behaviour (RUN: scripts/probe_child.ts, logs/probe_matrix.jsonl, logs/probe_table.log; 56 comparisons: 32 SAME, 24 DIFF, every DIFF listed)
Values: ordinary Error, revoked Proxy, message getter throws, message 42, message undefined, null, Symbol, object whose toString throws / returns text, thrown null, undefined, string, number, Symbol. The constructor-site run replicates `index.ts` `initEventBus();` (bare call, return ignored) inside an async start() awaited with `.catch -> logger.error + process.exit(1)`.
### Constructor throws (initEventBus catch)
| thrown | base | head |
|---|---|---|
| ordinary Error | false, `warn error:"boom"`, boot continues | same |
| revoked Proxy / getter throws | **throws out of initEventBus; no line; start() rejects -> exit(1)** | false, one warn line `"unreadable thrown value"`, boot continues |
| message 42 / Symbol | `42` (number) / key absent | `"42"` (string) / `"Symbol(s)"` |
| toString throws / returns text | `{}` / `{}` | constant / `"custom-string"` |
| message undefined / null; thrown null/undefined/string/number/Symbol | SAME | SAME |
Head never throws in any of the 28 head ctor runs; `returned` is false in all.
### Listener (`redis.on('error')`)
| emitted | base | head |
|---|---|---|
| ordinary Error | one debug line `"boom"` | same |
| revoked Proxy / getter throws | **uncaughtException** (TypeError / Error), no line | one debug line `"unreadable thrown value"` |
| null / undefined value | **uncaughtException** (TypeError "Cannot read properties of null") | one debug line, no `error` key |
| message 42 / Symbol / toString objects | `42` / absent / `{}` | `"42"` / `"Symbol(s)"` / constant or text |
| message undefined/null, string, number, Symbol value | SAME | SAME |
`publishXadds` equal at base and head in every cell (the listener never touches the publish path). The listener is at `debug`: at the production default level (info) the line is dropped, for an ordinary Error as well (production-format rows show NO LINE for both, as the author states). So in production the user-visible change is: the process no longer dies on an unreadable emitted value, and boot no longer exits 1.
### Caller (read)
One caller: `src/index.ts` `initEventBus();` (author: line 256; on develop `0bd5e7bf` it is line 259 after PR 1953 added 3 lines of imports; the call text is unchanged), bare, return ignored, inside start() whose rejection ends in `process.exit(1)` (per the author, read, not re-opened line by line). So base: an unreadable constructor throw = auth fails to boot; head: boot continues with events off, the same state as no REDIS_URL and the same as for an ordinary Error. Raise accepted: every unreadable-value after-state equals the ordinary-Error after-state.
Persisted state / side effects: none involved (log only; no DB, no session).

## 4. Re-measure
- Red first (the two new files only, product = base `events.ts`): **6 failed | 4 passed (10)**, 6 `AssertionError`, no timeouts; the 6 failures are exactly R1-R3 in each file (logs/cells_base.log). Green at head: 2 files / 10 passed (logs/cells_head.log). 6 red, 4 control, as the file names claim.
- Whole auth suite (vitest, `--root` the clone; logs/suite_*): head run 1 **131 files + 1 failed / 1545 passed + 1 failed (1546)** with the single failure `ks949-platform-admin-seed-identity.test.ts > the enumeration actually finds seed sites` = **5000 ms timeout**; head run 2 **132 files, 1546 passed, rc 0**; base (events.ts reverted, the two new files moved out) **130 files / 1536, the same single ks949 timeout (5004 ms)**. So the same cell times out under load at base and head (flaky, not caused by the PR); ratio: +2 files, +10 cells (1536 -> 1546), nothing else moved. The author's note about this ks949 cell is confirmed; the other two load symptoms the author lists (auth.integration beforeAll, the seedDemoUsers mock) did not occur in my three runs.
- tsc, ad hoc: own `tsconfig.json` (tests excluded) **0 errors**; `tsconfig.test.json` (tests included) **42 errors at head and 42 at base** (same count; logs/tsc_*_test.log); ratchet `test-types-ratchet.sh services/auth`: "tsc examined 184 files, 132 under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale" rc 0 (author: 42 baselined, 0 new, 0 stale: confirmed).
- eslint on `events.ts` + the two new tests: 0 problems rc 0; planted file (`debugger` + unused const) rc 1.
- docs-fragments `check --root`: rc 0, "lint clean, render passes" (107 new each). Same two pre-existing committed-page ADVISORY lines (flow 6249, cheat 6235) as gates 139/141: not from this PR. Planted defects: flow `<!--n-->` token removed rc 1; cheat unclosed `<div>` rc 1; both restored by sha, check rc 0 after.

## 5. Mutants (scripts/mutants.py; one site per run, product only, tests untouched, sha256 restored: "restored sha ok"; logs/mutants.log)
18 runs (9 mutants x 2 sites): **14 killed, 4 survived**, no timeouts.
| mutant | listener | init-catch |
|---|---|---|
| remove guard (revert to the old line) | KILLED (3 red) | KILLED (3 red) |
| wrong constant; always `String(m)`; no coercion; swallow-undefined in catch; undefined-as-text; read outside try | KILLED | KILLED |
| **drop optional chain (`err?.message` -> `err.message`)** | **SURVIVED** | **SURVIVED** |
| **null message as text** | **SURVIVED** | **SURVIVED** |
Why they survive: no cell emits/throws a null or undefined VALUE (at the listener base threw; with the `?.` dropped head would still log, but with `"unreadable thrown value"` instead of no `error` key since the TypeError is caught by the inner try), and no cell uses a null MESSAGE. Same two branches as gates 139/141 (G139-F1, G141-F1).

## 6. merge-tree (logs/mergetree.log first onto `cc33e702`; logs/mergetree2.log onto the latest `0bd5e7bf`)
- Onto cc33e702 (PR 1953, zod 4): rc 0, tree `22350834...`. Onto the latest develop `0bd5e7bf` (adds PR 1957: five db.ts + tests + fragments, none under auth): rc 0 clean, tree `5a53554e...`; the result differs from develop in exactly the PR's 5 paths (path lists equal, logs/mergetree2_paths.log); the merged `events.ts` blob `0c128ebf` = the PR head's. `events.ts` on develop is byte-identical to the PR's base (sha256 789789ee... both): nobody else touched it.
- **PR 1953 overlap:** none of the PR's 5 paths is among PR 1953's 150 changed paths (grep of the two lists, rc 1; logs/pr1953_paths.log). 1953 DID change `services/auth` (`package.json`/lock, `src/index.ts`, `errorHandler.ts`, `routes/*`, one test): `index.ts` holds the caller but 1953's index.ts hunk only adds the first-import `@secuura/shared/zod3-compat`, so the caller line merely moved 256 -> 259.
- **Does the PR's behaviour depend on zod?** No by read: `events.ts` imports `ioredis` and `./utils/logger` (winston) only; the two tests import `../events` only; the guard uses `String()`. Not measured under zod 4: I did not install the merged tree (zod 4.6.7), so the 10 cells, the suite and tsc are measured on the PR's tree (zod 3), not on merged develop; I expect no difference but that is an inference (NOT TESTED).
- Suites/fragments on the merged tree: not re-run.

## 7. Kam's ks1346 rule (log type and field NAMES, never values)
No new log line: both messages keep text, level and keys; only the value of `error` changes. The constant `'unreadable thrown value'` is a type statement: compliant. A readable message is logged as before (the existing sibling KS-1868 practice). `String(m)` on a non-string readable message logs a value; a custom `toString` is logged by its return (`"custom-string"`) where base logged `{}` for the object: narrower or equal in information to base's `JSON.stringify` of own fields, no stack, no whole object, no secret field added. Compliant relative to the existing pattern; info only.

## 8. Notes for the PR body
- **G143-F1 (recommended follow-up, test gap, measured)** 4 mutants survive (drop `?.`, null message as text) at both sites: no cell has a null/undefined thrown/emitted VALUE or a null MESSAGE, or message 42. The listener's new tolerance of a null/undefined emitted value (base: uncaughtException) is correct per the probe but unpinned. One cell per file would close it (same as G139-F1/G141-F1). Not a merge block.
- **G143-F2 (INFO, measured)** The listener is `debug`: at the production default (info) nothing is logged for any value, ordinary or hostile; the fix's production effect is purely that the process no longer dies (uncaught exception) and boot no longer exits 1. The fragment/body should say that rather than imply a visible log line in production (the author's mail already says so).
- **G143-F3 (INFO, measured)** The base failure mode at the constructor is auth failing to boot (start() rejects, `process.exit(1)`); head continues with events off. The author reads this at `index.ts:256`; after PR 1953 it is `:259`. Cite by text, not line.
- **G143-F4 (INFO)** PR 1953 (zod 4) and PR 1957 merged since the PR was created; disjoint, merge-tree clean; the PR need not be rebased. Its tests/suite were measured on the pre-1953 tree (see 9).
- **G143-F5 (INFO, measured)** Under load the same `ks949` cell times out (5000 ms) at base and at head (one of my three runs each way; passes in head run 2): not caused by the PR, a flaky cell the author already documents.
- **G143-F6 (INFO, measured)** Type/lint state unchanged: tsc-with-tests 42 = 42 (all baselined), own tsconfig 0, eslint 0.
- **G143-F7 (INFO, style)** Guard preserves undefined/null as absent/null, unlike the develop admin.ts guard (`String(err.message)`); intentional, as in G139-F6 / G141-F7. The guard is now pasted in a 3rd service pair; a shared helper would be a later cleanup.

## 9. NOT TESTED
The live PR body; a real Redis or ioredis client (stand-in; the 'error' emission from a real client is read, not run); a booted auth service (the caller and `process.exit(1)` path are read, not run to exit); the tests, suite, tsc and probe on the MERGED tree with zod 4.6.7 (not installed; by read the PR does not touch zod); the author's `index.ts:256` boot path re-read line by line (I re-grepped the call site only); BigInt and cyclic-object messages; the author's real-winston recorder evidence (I re-ran the real winston logger myself in the probe, but not their recorder script); a second base suite run; CI; the pre-push hook legs other than the ratchet; the four platform suites; the 56 auth.integration cells (not run separately); Node 24; Spark shadow review (not requested).

## Processes
`ps` at resume: no orphan from this workdir. All runs I started (static.sh: tsc, eslint, ratchet, docs-fragments; mergetree2.sh) finished; no background process left running.
