# Gate verdict: Secuura Platform K PR #1524 (KS-1521), SONNET tier 3, narrow, tests only

Gated 2026-10-13 by an independent QA session (findings only; no fixes, no pushes, no GitHub/Linear writes, no server contact).

## VERDICT: GO WITH NOTE

Majors: 0. Minors: 3 (none blocks merge). The reason for "NOTE" rather than plain GO: one of the author's numbers ("governance tsc clean") is vacuous for this change, and the jest-upgrade fail-loud claim is proved only for the class of change (state symbol renamed or moved), not against a real jest 30 build, which is not on disk.

## Head under test

- Head `7624c699380d6d152f20220ee34242fc7adad7c5` ASSERTED by `git rev-parse HEAD` in my clone after `checkout --detach` (a `git clone --shared` of a project worktree that holds the objects, in my scratchpad; the bundle `ks1521-7624c699380d.bundle` sha256/16 = `5314c2e2b298423d` matched the brief, but `bundle verify` against the main checkout failed on prerequisites b08ee629 / 69878dc5, so I took the objects from a sibling worktree object store instead. Commit sha equality is the proof; I did not unbundle).
- HEAD^1 = `56bdc391ebd7160940c15c4940b597dab4a30fa3` (the one change commit), HEAD^2 = `69878dc5d1ae4b717834c547c47d8bc036625d2e` (develop). Merge base of the change commit and develop = `b08ee629`.
- `git diff 69878dc5 HEAD --stat`: exactly 3 files, +23/-20, all `db.retry.test.ts` (governance, staking, transfer). No service code. Matches the brief.
- Develop comparison tree: `69878dc5` checked out in a second scratchpad clone. Both clones share `node_modules` read-only via symlink from the project checkout (see NOT tested).

## Scope item 1: the eight shapes (governance), old pin vs new pin

Instrument: `evidence/shapes.py` (python, jest `--json`). For each shape it replaces the single column-0 line `jest.setTimeout(60_000);` (anchor asserted to occur exactly once, replacement asserted to change the file, tamper state asserted by sha before the run), runs ONLY `db.retry.test.ts` under jest 29.7.0, records the failing cell titles, restores the original bytes and asserts the sha256 equal (all 24 restores asserted; "ALL RESTORED OK"). Raw: `evidence/shapes_results.json`.

CONTROLS that could have failed: unmutated file on each tree must be 8/8 green (both were: rc 0, 8 tests), and the mutation must land (asserted). Each "red" was read, not just counted: the new-pin reds all read `Expected: 60000 Received: 10000` (or `30000` for "lowered"), i.e. the assertion fired, not a compile error or load error (`load_errors` empty on every run, 7 of 8 other cells passing every time).

| # | shape | old pin (develop) | new pin (head) |
|---|---|---|---|
| 0 | control, unmutated | green 8/8 | green 8/8 |
| 1 | deleted | RED, pin cell alone | RED, pin cell alone (10000) |
| 2 | lowered to 30_000 | RED, pin cell alone | RED, pin cell alone (30000) |
| 3 | multi-line block comment | green (false green) | RED, pin cell alone (10000) |
| 4 | template literal | green (false green) | RED, pin cell alone |
| 5 | in afterAll | green (false green) | RED, pin cell alone |
| 6 | in beforeAll | green (false green) | RED, pin cell alone |
| 7 | uncalled function | green (false green) | RED, pin cell alone |
| 8 | false condition | green (false green) | RED, pin cell alone |

Result: old pin red on 2 of 8, new pin red on 8 of 8, each red is the pin cell alone (1 failing test of 8). This reproduces the author's claim exactly.

Extra shapes of my own (not in the brief), to try to make the new pin wrong in either direction:
- 9: `jest.setTimeout(60_000)` inside a `beforeEach` (applies at test time, after `run_start` copied the symbol): old pin green (false green), new pin RED (10000). Correct, the runner never applies it.
- 10: the call moved to the END of the file at top level (runs at collection time, before `run_start`, so it genuinely applies): new pin green, old pin green. Correct, no false positive.
- 11: the call inside a bare top-level `{ }` block (runs at collection time): new pin green. Correct.
So no false red found where the budget really is 60 s, and no false green found where it is not.

## Scope item 2: the symbol lookup

FOUND (source read, not memory), installed `node_modules/jest-circus` `package.json` version 29.7.0:
- `build/types.js:19` `const STATE_SYM = Symbol('JEST_STATE_SYMBOL');` an UNREGISTERED symbol (not `Symbol.for`), exported as `STATE_SYM`; `build/state.js` `getState = () => global[STATE_SYM]` and `resetState` writes `global[STATE_SYM] = createState()`.
- `build/state.js:49` default `testTimeout: 5000`; `legacy-code-todo-rewrite/jestAdapterInit.js:38-39` copies `globalConfig.testTimeout` into state; `build/eventHandler.js:230-233` on `run_start`: `global[TEST_TIMEOUT_SYMBOL] && (state.testTimeout = global[TEST_TIMEOUT_SYMBOL])` (`TEST_TIMEOUT_SYMBOL = Symbol.for('TEST_TIMEOUT_SYMBOL')`, types.js:24). `run.js:279` and `:306` read `getState().testTimeout` for hooks and tests. So the PR's code comment ("copies ONCE at run_start", "unregistered Symbol('JEST_STATE_SYMBOL')", "build/types.js") is accurate.
- The lockfiles pin it: `services/governance/package-lock.json:3130-3133` `node_modules/jest-circus` 29.7.0; `Dev/package-lock.json:15584`. `jest-config` Defaults `testRunner: 'jest-circus/runner'` (so circus is the runner for this suite).
- The lookup works on the test environment's global at runtime: the unmutated head passes (`states` length 1, `testTimeout` 60000).

TESTED (`evidence/symbol.py`, `evidence/symbol_results.json`; same restore/sha discipline; control Z0 unmutated green): does "zero or several" fail, and does a moved/renamed state fail loud?
- Z1 zero symbols (the description string in the filter renamed, simulating a jest rename): RED `Expected length: 1 Received length: 0`.
- Z2 two symbols (second also `testTimeout: 60_000`): RED `Expected length: 1 Received length: 2`.
- Z3 two symbols (second `10_000`): RED, same length message.
- Z4 state found but the field is not `testTimeout` (simulating a renamed field): RED `Expected: 60000 Received: undefined`.
So a jest-circus bump in package-lock that renames the symbol, renames the field, or adds a second state fails loud on this cell; it cannot pass silently. A bump that keeps both the symbol description and the field name keeps working and still reads what the runner applies (that is the intended behaviour). A bump that applied the timeout elsewhere and left `state.testTimeout` at 10000 would also go RED, not green.
NOT proved here: that a real jest 30 build behaves as the simulations; only 29.7.0 exists anywhere on this drive (15 copies, all 29.7.0, checked by find) and fetching one would need the network, which is forbidden.

## Scope item 3: staking and transfer claims (10 s)

- `services/staking/vitest.config.ts:8` and `services/transfer/vitest.config.ts:8`: `testTimeout: 10000`. The new comments and titles ("this service's 10 s testTimeout", "vitest.config.ts", "not vitest's 5 s default, which this service overrides") match each file's own config.
- Class hunt (a stale "5 s default" sibling that is really not 5 s): `find services -maxdepth 2 -name 'vitest.config.*' -o -name 'jest.config.*'` returned 23 configs; case-insensitive grep for `testTimeout` hits exactly 3 (governance jest, staking, transfer; the other 20 give 0). Positive control: the 3 hits are the 3 known files. So the other 14 siblings that still say "5 s default" are correct (vitest 4.1.10 default). No stale sibling.
- Both staking and transfer pin cells (`task.suite.tasks[*].timeout === 60_000`) are unchanged apart from the title string. The titles contain `\'` escapes; eslint is clean (below).

## Scope item 4: suites at head vs develop

Instrument: jest 29.7.0 (governance) and vitest 4.1.10 (staking, transfer), run once each per tree, `--no-cache` for jest. Tails in `evidence/*_head.tail.txt`, `evidence/*_dev.tail.txt`.

| suite | head 7624c699 | develop 69878dc5 |
|---|---|---|
| governance (jest) | 4 files, 116/116, rc 0 | 4 files, 116/116, rc 0 |
| staking (vitest) | 4 files, 66/66, rc 0 | 4 files, 66/66, rc 0 |
| transfer (vitest) | 7 files, 92/92, rc 0 | 7 files, 92/92, rc 0 |

Matches the author's 116 / 66 / 92 and equals develop (the PR replaces one cell in place, so counts must not move; a changed count would have been the control failing). Also ran eslint on the three changed files (rc 0, both trees) and `tsc --noEmit -p` in governance (rc 0 on both trees); see Minor 2 on what the tsc number does not prove.

## Scope item 5: the develop merge

Blob ids of `.../src/__tests__/db.retry.test.ts` (read with `git rev-parse <rev>:<path>`):
- governance: head `5ed75206…` = change commit 56bdc391 `5ed75206…`; develop and merge-base-side `20590408…`.
- staking: head `909a84ba…` = 56bdc391 `909a84ba…`; develop `d6c22cec…`.
- transfer: head `a8dd192b…` = 56bdc391 `a8dd192b…`; develop `ed1ea820…`.
All three files at the merge equal the change commit's blobs (the merge brought nothing in). Develop did not touch them since the merge base (`git diff --name-only b08ee629 69878dc5 | grep -c db.retry` = 0). `git diff --name-only 56bdc391 HEAD` = 10 files, all develop's own work (KS-1517/1351/1533), none of the three. The merge is a true no-overlap merge, as its message says.

## Findings

Majors: none.

Minors (all severity-minor; priority is for the humans):

1. `Blockchain/Dev/services/governance/src/__tests__/db.retry.test.ts` lines 13-15: removing `import { readFileSync } from 'fs';` left two consecutive blank lines (after the header comment `*/`, line 14 and 15 empty). Cosmetic only; eslint passes. Reproduce: view lines 10-17. Oracle: Product consistency (the other 16 db.retry files have one blank line there).
2. The author's "governance tsc clean" proves nothing for this change. `services/governance/tsconfig.json` has `"exclude": [..., "src/__tests__"]`, so `tsc --noEmit -p tsconfig.json` never sees the test file. Control (`evidence/tsctl.py`): planting `const TYPEERR: number = 'a';` in the test file leaves `tsc -p` at rc 0, while jest/ts-jest fails the suite with `TS2322`. So the real type check for this edit is ts-jest at run time (which ran green on head; the `Record<symbol, ...>` cast compiled), not the tsc the author cited. Oracle: Explainability/Claims (an instrument that cannot fail was cited as evidence). Not a defect in the code.
3. The new pin measures the EFFECTIVE budget, so it also stays green if the 60 s is supplied by `jest.config.js` `testTimeout: 60000` instead of the file's own `jest.setTimeout`, while the title still says "this file RUNS on its own 60 s budget (jest.setTimeout)". Inferred from `eventHandler.js` / `jestAdapterInit.js` reading above; I did NOT run a config-change mutation (it would mean editing a second file). Impact: none for the stated purpose (a run under 60 s is what KS-1328 needs); only the wording over-promises "its own". Oracle: Purpose vs Image.

Curios (not defects): the pin cell reads runner state at test time, so it is order-independent within the file (no `--randomize` run done); extra shape 9 shows a late `jest.setTimeout` is correctly judged not applied for the first cells, so the pin guards the real first-cell hazard.

## What was NOT tested (Rule 2)

- Real jest 30 or any jest-circus other than 29.7.0. Only simulated renames (Z1-Z4). Unverified from memory only: that a future jest keeps the description `JEST_STATE_SYMBOL`; either way the pin fails loud if it changes.
- CI. I did not run the project's CI workflows, the pre-push hooks, or the "test-file type-check ratchet" referenced in the develop commits (KS-1351/KS-1517); the type check I relied on is ts-jest only.
- Environment fidelity: tests resolved `node_modules` and `@secuura/shared` (`packages/shared/src`) through a read-only symlink into the project checkout at its own HEAD (`40ed3573b`), not from an install of the PR's lockfile. Develop and head used the identical dependency set, so the head-vs-develop comparison is fair, but I did not do a clean `npm ci` (no network). The installed jest-circus (29.7.0) equals the lockfile.
- A single run per suite; no repetition under load, no `--runInBand` vs worker comparison, no `--randomize`, no Windows/CI Node-version matrix. The timeout hazard KS-1328 is about (fleet load) was not reproduced; I tested that the pin reads the right number, not that 60 s is sufficient.
- The 14 sibling vitest services were only grep-checked for their `testTimeout` setting, not run.
- GitHub state (review comments, CI status, PR body vs commit), Linear, and the live `refs/pull/1524/head` (no network; I used the local object store and checked the sha instead).
- The vitest-side pins in staking/transfer were not mutation-tested (out of the brief's scope; the brief only asked for the comment/title claims there).

## Cleanup / state left behind

All mutations were made only inside my scratchpad clones and restored byte-identical (sha256 asserted after every run; `git status` in both clones shows only the untracked `node_modules` symlinks). The project checkout and every other project folder were read only. Evidence: `evidence/` in this folder (scripts, JSON results, run tails).
