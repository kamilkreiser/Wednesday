# QA GATE 72 verdict: Secuura/Distributed_Secuura PR 1887 (KS-1868, packages/shared O38-P1 + O38-P2), tier 2

## BLUF

**GO WITH NOTES.** Both product hunks do what the author says and nothing more. The inner try is correct for a revoked Proxy and for a throwing `message` getter. The tests fail by assertion at base (4 of 6) and all 6 pass with the change. Mutants: 9 of 10 killed. The shared whole suite shows no new red against the base, over 2 runs each. api-gateway passes 1368/1368 on rebuilt shared. The merge with current develop is clean, with no overlap with the PR's files. The notes are low or info only (G72-F1 to F4); none blocks a merge.

## Heads

| | sha | how read |
|---|---|---|
| START | 2d1a2265bbab7bef1b689087e021a412b08fabae (develop b1fb543640e7a439a9344d1d96d5a62862edfcf5) | `ls-remote origin refs/pull/1887/head refs/heads/develop`, before any fetch; fetched into `refs/gate/pr1887` and `refs/gate/develop` |
| END | 2d1a2265bbab7bef1b689087e021a412b08fabae (develop b1fb543640e7a439a9344d1d96d5a62862edfcf5) | same `ls-remote` after all runs; the clone `HEAD` is the same sha |

The head did not move. `git status --short` in the clone is empty at the end.

## FINDINGS

| id | severity | where | finding |
|---|---|---|---|
| G72-F1 | low | `packages/shared/src/utils/gracefulShutdown.ts:52-59` | Mutant M4 (the stack dropped from the readable-Error log text) SURVIVED. No cell asserts that `reason.stack` reaches the log. The change keeps that behaviour (probe.log: the plain Error line contains the stack), but nothing pins it. The test gap is not a defect in the product. |
| G72-F2 | info | `gracefulShutdown.ts:52-59` | The try wraps the whole template, `message` plus `stack`. Probe.log: an Error with a readable `message` and a throwing `stack` getter logs only the constant `unreadable thrown value`, so the readable message is lost. This is the safe direction (the log is never skipped) and the author's fragment says "unreadable thrown value", but it is coarser than a per-property guard. No cell covers it. |
| G72-F3 | info | `packages/shared/src/cache/response-cache.ts:127,135,147,155,333` | Five more identical unguarded `err instanceof Error ? err.message : String(err)` reads sit in the same file: set, delete, deleteByTag, addTag and the write catch. They are not fixed here. The author scopes this as 2 of 253 sites and KS-1868 stays open, so this is consistent with the ticket. The write-catch line 333 sits inside the `res.json` wrapper, not the read path. |
| G72-F4 | info | `Projects Documents/fragments/cheat/KS-1868-...html` | The cheat fragment says `wallet-signature` is "KS-278". The ready mail says KS-1727/KS-1739. KS-278 is only the label inside the failing test's own title (`failnames_*.txt`), so the two are not in conflict. This is a documentation nit, not a defect. |

No finding above low severity. The base reds are not caused by the PR.

## 1. Head assertion

See the Heads table. Fetched from `git@github.com:Secuura/Distributed_Secuura.git`, fetch only. The clone's push url is set to `no_push_qa_gate`. Nothing was written to GitHub, Linear, mail or `!CODING`. The clone is `git clone --shared --no-checkout` from the gate65 repo, under `repo/`, which is gitignored by `.gitignore:257`.

## 2. Product hunks at source

`git diff a71479b49bf3 2d1a2265` touches 6 files: 2 product (+8/-2 and +7/-1), 2 tests, 2 fragments.

**P1, `createUnhandledRejectionHandler` (gracefulShutdown.ts:49-59).** Before, one expression: `reason instanceof Error ? `${reason.message}\n${reason.stack ?? ''}` : String(reason)`. After, the same expression sits in `try { detail = ... } catch { detail = 'unreadable thrown value'; }`.

What changes: only the case where reading the reason throws. That case used to make the listener itself throw before it reached its log or its `shutdown` call. It now sets `detail` to the constant.

What does not change, from source:
- the log text and both templates (`UNHANDLED REJECTION #n ... : ${detail}` in survive mode, `Unhandled rejection: ${detail}` in exit mode);
- the `survived` counter;
- the return type (`void`; survive mode `return`s after the log, exit mode calls `ctx.shutdown('unhandledRejection')`);
- the mode logic.

Nothing is rethrown (mutant M2 proves the cells catch a rethrow).

Survive-mode behaviour, measured against the built `dist` (`scripts/probe.js`, `logs/probe.log`). For every unreadable value (revoked Proxy, throwing `stack` getter, Symbol `message`, throwing `toString`, null-prototype object):
- survive mode logs exactly one line ending `unreadable thrown value`, calls shutdown zero times, and does not throw;
- exit mode logs one line and calls shutdown once with `unhandledRejection`;
- a plain `Error` still logs `ok` plus its stack.

**P2, `responseCache` read catch (response-cache.ts:298-305).** Before, `logger.error('[ResponseCache] Cache read error', { error: error instanceof Error ? error.message : String(error) })`. After, the same expression is in an inner try with the fallback, assigned to `reason`, and logged under the same message and the same `{ error: reason }` key.

What changes: a throwing read used to escape the catch. The middleware threw instead of falling through to the response-capture wrapper and `next()`. It now falls through.

What does not change: the log message string, the key name, the control flow after the catch, and the function's return. Mutant M8 shows the key name is pinned.

**Is the inner try correct?**
- Revoked Proxy: `instanceof` throws a TypeError on a revoked Proxy. That sits inside the try in both hunks. Cells R1 killed M1, M2, M5, M6, M7 and M9.
- Throwing `message` getter: the read is `error.message` (P2) or `${reason.message}...` (P1), both inside the try. Cells R2 cover it.
- Beyond the author's cells, probe.log also shows the `stack` getter, a Symbol `message` (the template literal throws a TypeError, caught), a throwing `toString` and a null-prototype value all handled. P2's Symbol-message case does not throw (no template), so it logs the Symbol as the value; I did not execute that path.

## 3. Red-first and mutants

**At base** (product files `git checkout a71479b49bf3`, the 2 new tests in place, log `logs/base_redfirst.log`): `Test Files 2 failed (2)`, `Tests 4 failed | 2 passed (6)`, rc=1. The 4 failures are R1 and R2 in each file, each `AssertionError: expected true to be false // Object.is equality`. That is assertion, not timeout. The two C1 controls pass.

**At head** (`logs/head_targeted.log`): `Test Files 2 passed (2)`, `Tests 6 passed (6)`, rc=0.

**Mutants** (`scripts/mutants.py`, `logs/mutants_summary.log`, one log per mutant `logs/mutant_M*.log`; each restored by `git checkout 2d1a2265` and status clean after):

| mutant | result |
|---|---|
| M1 listener fallback text changed | KILLED |
| M2 listener catch rethrows | KILLED |
| M3 listener survive branch inverted | KILLED |
| M4 listener stack dropped for a readable Error | **SURVIVED** (6 passed): G72-F1 |
| M5 listener fallback calls `String(reason)` (re-reads the unreadable value) | KILLED |
| M6 cache fallback emptied | KILLED |
| M7 cache catch rethrows | KILLED |
| M8 cache log key renamed | KILLED |
| M9 cache inner try removed | KILLED |
| M10 cache readable path uses `String(error)` for Errors | KILLED |

## 4. Suites before and after

Host: Node v26.8.1, vitest 4.1.12. `npm ci --ignore-scripts` rc=0 (`logs/npm_ci.log`, "added 1795 packages"). `@secuura/shared` build (`tsc`) rc=0 (`logs/shared_build.log`) before any test. Prisma generate rc=0 (`logs/prisma_generate.log`, via `services/originate` `npm run generate`; a bare `prisma generate` failed first with rc=127 and then "Could not resolve @prisma/client", so I used the workspace script).

Method: base is the product reverted and the 2 new tests moved aside. Two runs each (`scripts/suite_ab.sh`, driver `logs/suite_ab_driver.log`). All runs rc=1 because of the one red below.

| run | files | cells | pass | fail | failing names (`logs/failnames_*.txt`) |
|---|---|---|---|---|---|
| base1 | 57 | 1099 | 1096 | 3 | wallet-signature KS-278; threadToken different-seeds (timeout class); ks879 raw-control-bytes walker (timeout class). Duration 66.21s. |
| base2 | 57 | 1099 | 1098 | 1 | wallet-signature KS-278 |
| head1 | 59 | 1105 | 1104 | 1 | wallet-signature KS-278 |
| head2 | 59 | 1105 | 1104 | 1 | wallet-signature KS-278 |

The head failing set is a subset of the base failing set in both runs. No NEW red. The extra reds in base1 are the timeout class (KS-1155) under that run's 66s wall time; base2 and both head runs took 5-7s. The 6 new cells account for the 1099 to 1105 difference. The wallet-signature red is at base in 2 of 2 runs, as the ready mail says (it said 3 of 3).

**api-gateway on rebuilt shared** (`dist` built from the head, confirmed to contain `unreadable`; `scripts/vt_api.sh`, `--maxWorkers=2`): `logs/api_head.log` shows `Test Files 133 passed (133)`, `Tests 1368 passed (1368)`, rc=0, Duration 94.06s. The author saw 1366/1368 under load.

**The two ks1543 eslint-spawning files alone** (`logs/api_ks1543_alone.log`): `Test Files 2 passed (2)`, `Tests 16 passed (16)`, rc=0, Duration 928ms. In the whole run the slowest ks1543 cell (C7, which spawns eslint) took 24.2s (`api_head.json`). It was within budget at this load, which confirms the author's "over budget under load only" reading. I did NOT run api-gateway at base, so the "1368 before" is the author's figure, not mine.

## 5. Merge with develop

`git merge-tree --write-tree b1fb543640e7 2d1a2265bbab`: **rc=0**, tree `f0ddb72b4a8fbb7df5934960ceb33b0aaf7a234b` (`logs/merge_tree.log`). No conflict output. Develop moved 59 files from the PR's base to `b1fb54364`; none is in `packages/shared`, and none is a `KS-1868` file. The only fragment files develop touched are KS-1384, KS-1860 and KS-1861.

## 6. Blast radius (`git grep` at head, `logs/blast_grep.log`)

`createUnhandledRejectionHandler` is imported by:
- `services/api-gateway/src/index.ts:56` (installed at line 1195), the only runtime consumer;
- `packages/shared/src/index.ts:26` (re-export);
- inside `gracefulShutdown.ts:179` (`setupGracefulShutdown` installs it);
- the tests.

`setupGracefulShutdown` is re-exported at `packages/shared/src/utils/index.ts:10`. The comment at `src/index.ts:23` says it has no live consumers, and the grep found no importer of it outside shared.

`response-cache`: grep for `response-cache`, `responseCache` and `setDefaultCacheStore` finds only the file itself and the new test. There is no importer, no `src/index.ts` export (`index.ts:15` exports `./cache/redis` only) and no `exports` entry (`package.json:143` lists only `./cache/redis`). Matches the author's claim.

## 7. Docs fragments

`node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>`:
- Clean head: rc=0, "flow 117 legacy + 40 new, cheat 112 legacy + 40 new; lint clean, render passes html_docs_check" (`logs/fragments_check_clean.log`).
- Planted flow defect (literal `999.` in place of `<!--n-->.`, plus an unclosed `<div>`): rc=1 with 3 findings ("tags are not balanced", "the h2 must start with <!--n-->.", "literal section number") (`logs/fragments_check_planted_flow.log`).
- Planted cheat defect (unclosed `<div>`): rc=1, "tags are not balanced: <div> opened 3, closed 2" (`logs/fragments_check_planted_cheat.log`).
- Restored with `git checkout -- "Projects Documents"`; the clean re-check rc=0 (`logs/fragments_check_clean2.log`).

An ADVISORY line (committed page differs from the render at flow line 6249 and cheat line 6235) appears in the clean head run. It is identical with the PR's two fragments removed (`logs/fragments_check_without_pr.log`, rc=0), so it exists at base and is not caused by this PR.

## NOT TESTED

- A booted api-gateway: the survive-mode effect is read from source and the `dist` probe, not measured in a running process.
- A real `process.on('unhandledRejection')` event inside a live process.
- api-gateway at base ("before"): only the head run and the alone run are mine.
- The four platform suites, a LTS Node (host v26.8.1), and the pre-push hook (not run by me).
- The P2 Symbol-message path in `responseCache` (reasoned, not executed).
- Whether the `eslint` cells go over budget under real load: I observed one run at a lower load.
- `eslint` and `tsc` on the changed files: not re-run by me; the author's claims are unverified here.

## HOW

- Clone: `git clone --shared --no-checkout` from `0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo` to `.../2026-11-01_gate72-ks1868-shared-1887/repo`; origin reset to GitHub (fetch only, push url `no_push_qa_gate`); `refs/gate/pr1887` and `refs/gate/develop`.
- Runners: `scripts/vt.sh` (shared vitest), `scripts/vt_api.sh` (api-gateway vitest), both `nice -n 10` and waiting while load1 > 8. Load stayed at or below 5.1, so no waits are logged.
- Scripts: `scripts/mutants.py`, `scripts/suite_ab.sh`, `scripts/probe.js`.
- Logs: all under `logs/`, named above, stderr kept (`2>&1` into each log).
- No secrets used. The ssh deploy key already configured in the sibling clone was used for fetch only.
