# QA gate: Secuura Platform K PR #1508 (KS-1328, tier 2 test-only)

- Head: `09c2646e77de2d299abb2da9d0831342fbc5ce71`. Bundle sha256/16 `4193de964d7d953c` = builder's figure.
- Base: develop `88c348375bd3083e0d9bef191f610ca9289c59ab`. Real tip now (`git ls-remote origin refs/heads/develop`): `88c348375bd3083e0d9bef191f610ca9289c59ab` (unchanged, so head = base + 1 commit, no merge needed; `git merge-tree --write-tree 88c348375 09c2646e7` = tree `1559de51`, rc 0).
- How I got the tree: scratch clone `scratchpad/g1508/repo` (local clone of an earlier gate's scratch clone), `git fetch <bundle> 09c2646e...`, read-only fetch of develop, detached worktree `g1508/head`. Nothing written under `!CODING` except: node_modules in the worktree are SYMLINKS to the project's installed `2_Project_Files/Blockchain/Dev/node_modules` (and per-service ones), as earlier gates did; `packages/shared` rebuilt in the worktree (`tsc` rc 0). Tools can write caches through those symlinks (vite cache); I did not measure that. Node as installed on the host.
- Tier: Sonnet-tier independent gate. All scripts in `scratchpad/g1508/tools/`.

## VERDICT: GO WITH NOTE

Everything claimed reproduces: 16/16 files green on head, 48/48 vitest mutants and 15/15 governance mutants killed or classified, budget demonstrably bites (vitest and jest), lint and ratchets clean, no service code touched. 
The note: governance's source-text pin has real holes (five variants pass the pin with the budget not in effect), and the comment text says "5 s default" where staking/transfer run a 10 s config default; neither blocks a test-only PR.

## By my runs

**1. Bundle / head / diff / merge.**
- `shasum -a 256 <bundle> | cut -c1-16` = `4193de964d7d953c`. `git bundle verify`: "The bundle requires this ref: 88c348375bd3083e0d9bef191f610ca9289c59ab"; `git bundle list-heads` = `09c2646e77de2d299abb2da9d0831342fbc5ce71 HEAD`; worktree `git rev-parse HEAD` = same.
- `git merge-base 88c348375 09c2646e7` = `88c348375`; `git log --oneline 88c348375..09c2646e7` = one commit ("KS-1328: give the other 16 services' db.retry.test.ts a 60 s budget").
- `git diff --stat`: 16 files changed, 218 insertions(+), 15 deletions(-). `git diff --name-only | grep -v -E '\.test\.ts$'` prints nothing (grep rc 1); control: `grep -c -E 'db\.retry\.test\.ts$'` on the same list = 16. Non-test files touched: none (no service code, no config, no CLAUDE.md).
- Overlap with other PRs in flight: `git diff --name-only cc2939bb 767a75dc` (#1506) = baseline-api-gateway.txt, baseline-auth.txt, check.cjs, the auth ks1000 test, CLAUDE.md; #1507 (`cc2939bb..54bc137c`) = preflight_test_types_ratchet_leg.test.sh, test-types-ratchet.sh, CLAUDE.md. Zero overlap with the 16 db.retry files.

**2. Completeness.**
- `git ls-files | grep -i retry`: 17 `services/*/src/__tests__/db.retry.test.ts` (analytics anchoring api-gateway auth billing governance kyc m365-integration nft-certificate prism referral security staking timestamping transfer vc-issuer wallet-connector) + 2 unrelated `systemTest/performance/*authRetry*`. Content search `git grep -il "availability retry" -- '*.ts'` = 17 files (second method agrees). 17 = 16 changed + kyc (already budgeted at base, #1430). Unbudgeted copy left: none.
- Runners: 16 import from `vitest`; governance has `jest.config.js`, no vitest config, 33 `jest` mentions, no vitest import. So exactly 15 vitest changed (+ kyc, vitest) and 1 jest. Confirmed.
- Services with a `db.ts` and no db.retry test: `originate`, `tokenisation`. `grep -c 'KS-377\|isDbAvailable'`: originate 0, tokenisation 0, kyc 5 (positive control). They do not have the retry logic, so no test is missing.

**3. Per-file budget (static).** All 16 + kyc: one `describe`, no nested describe; `grep -nEi` for per-cell `}, <ms>)`, `{ timeout`, `retry:`, `.skip`, `.only`, `.each`, `.concurrent`, `vi.setConfig`, `jest.setTimeout` outside the budget lines finds only the budget line and the pin's own assertion line (control: the same pattern finds 16 describe budget lines + the governance call). Every vitest file: `describe('db availability retry (KS-377)', { timeout: 60_000 }, () => {`. Pinned cell count equals the real `it(` count (pin cell included) in all 16: analytics 8/8, anchoring 6/6, api-gateway 8/8, auth 7/7, billing 8/8, kyc 6/6, m365 8/8, nft 8/8, prism 8/8, referral 8/8, security 8/8, staking 8/8, timestamping 6/6, transfer 8/8, vc-issuer 8/8, wallet-connector 8/8. Fake-timer cells: every file calls `vi.useFakeTimers()` once in `beforeEach` and `useRealTimers` in `afterEach`; unchanged by the diff. Governance: `jest.setTimeout(60_000);` at file top level, column 0, before the describe.

**4. Runs.**
- Head, each file alone (`npx vitest run src/__tests__/db.retry.test.ts` in the service; jest for governance): all 16 green: analytics 8, anchoring 6, api-gateway 8, auth 7, billing 8, kyc 6, m365 8, nft 8, prism 8, referral 8, security 8, staking 8, timestamping 6, transfer 8, vc-issuer 8, wallet-connector 8 passed; governance `Tests: 8 passed, 8 total`.
- Vitest mutants, all 16 vitest files x 3 (option removed, lowered to 30_000, lowered to 5_000) = 48 mutants, each alone, file restored from backup. Every one: `Tests  1 failed | N passed` and the single failure is the `KS-1328: every cell in this file carries the 60 s budget` cell, nothing else red (counted: 48 mutated lines, 0 NOCHANGE controls, 48 `restored identical` sha256/16, 0 MISMATCH; e.g. api-gateway `833b561715ad0157` before = after). This also covers "budget line reverted = pin red and nothing else". Kyc is included (its pre-existing pin killed 3/3).
- Governance, builder's six (B1 call deleted, B2 30_000, B3 `//` commented, B4 inside an indented block, B5 semicolon dropped, B6 10_000): each `1 failed, 7 passed, 8 total`, failing cell = the KS-1328 pin; 6/6 killed. File sha256/16 `e76da8c13dfa601a` before = after, and restored identical after each mutant.

**5. Budget bites (measured).**
- Vitest, api-gateway: added a throwaway real-timer 5.6 s cell inside the describe (copy file `db.retry.bite.test.ts`, removed after). With budget: BITE cell passed (the only red was the pin cell, because I added a ninth cell; I did not print its name, so that attribution is by count). With the option removed: `× BITE: real 5.6 s cell 5003ms ... Test timed out in 5000ms`.
- Jest, governance: added a top-level real-timer 11 s cell (over the 10 s config default, under 60 s). Head: `Tests: 9 passed, 9 total`. B1 (call deleted): `2 failed` (BITE + pin) with `Exceeded timeout of 10000 ms`. So `jest.setTimeout(60_000)` takes effect per file; file removed (`bite file removed: True`).

**6. Governance pin holes (my variants, each run alone, file restored, sha before = after).** The pin reads `__filename`, drops lines starting with `*`, `/*`, `//`, then requires `^jest\.setTimeout\(60_000\);$` (multiline) in the rest.
- H1 call on its own line (column 0) inside a multi-line `/* ... */` block comment: pin PASSES (`8 passed`). With the 11 s cell: BITE fails at 10000 ms. Hole confirmed.
- H2 call at column 0 inside a template literal: pin passes; BITE fails at 10000 ms. H4 call at column 0 inside `afterAll`: pin passes; BITE fails. H5 call at column 0 in a never-called function: pin passes; BITE fails. H6 call at column 0 inside `if (false)`: pin passes (8 passed); BITE fails. (The first run of H2 and H5 gave `Tests: 0 total` because of unused-variable compile errors in my mutant, not a pin result; I re-ran them with `void` usage in the bite run, where the pin cell was not among the failures.)
- Legit variants that are rejected although they work: `jest.setTimeout( 60_000 );` and `jest.setTimeout(60000);` fail the pin (safe direction). H3 call at column 0 inside `beforeAll` passes the pin and is effective in jest (not separately bitten; unmeasured). H9 call after the describe at top level passes the pin; it takes effect in jest-circus (not separately bitten; unmeasured).
- Conclusion: the pin stops the six honest regressions but not a comment-block, string, dead-branch or late-hook placement. These need a deliberate or careless multi-line edit, so Minor.

**7. Lint / ratchets.** From `Blockchain/Dev`: `npx eslint` on the 17 db.retry files (16 + kyc) rc 0. Control: planted `debugger;` at the end of the auth file: `183:1 error Unexpected 'debugger' statement no-debugger`, rc 1; file restored identical. `node scripts/typecheck-tests/check.cjs services/auth` (on this tree, head = base + commit): `tsc examined 144 files, 93 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale`, rc 0. api-gateway: `149 files, 114 under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale`, rc 0. (Develop's count-keyed checker, as the tree has it.)

**8. Ceiling too broad?**
- Measured: api-gateway with a cell `await new Promise(() => {})` (a retry loop whose timer is never advanced). Head: `× HANG ... 60003ms`, `Test timed out in 60000ms`, wall 61.1 s. Option removed: `5003ms`, wall 5.9 s. So a real hang now costs 60 s per cell instead of 5 s.
- All the cells in these files are fake-timer or mock cells that finish in single-digit ms when healthy (CI timing from the builder: 179-675 ms alone). The only failure mode the budget slows is the hang one; a file of 8 hanging cells would take up to 8 min, ~4 min x services in a run if the same regression hit all 15 identically (computed, not run). No cell in these files is meant to prove a bounded failure within seconds via real time (they use fake timers and advance them explicitly); the retry tests assert behaviour, not wall time. I judge the breadth acceptable for a describe whose cells all use fake timers, with the cost stated in the PR by the builder.

## Findings

**Major**: none.

**Minor**
1. `services/governance/src/__tests__/db.retry.test.ts` (pin cell, `BUDGET`/`code` filter at ~lines 174-190): the pin passes when the call is inside a multi-line block comment (line not starting with `*`), a template literal, `afterAll`, a never-called function or `if (false)`, while the budget is NOT in effect (measured: an 11 s cell fails at 10000 ms in each variant while the pin cell is green). Evidence in section 6. Fix direction (not mine): add the real-effect check (a cell that waits just over 10 s is too slow), or parse the file with a TS/AST pass for a top-level expression statement, or assert `jest.setTimeout` via a `testTimeout` set in `jest.config.js`/`setupFilesAfterEach` instead of source text.
2. Comment inaccuracy in 15 vitest files (same text): "instead of vitest's 5 s default" and "every other suite in this service keeps the 5 s default". `services/staking/vitest.config.ts:8` and `services/transfer/vitest.config.ts:8` set `testTimeout: 10000`, so for those two the budget moves 10 s to 60 s and the other suites keep 10 s. Wording only; the pin cell and budget are right.

**Note**
3. The pin's `task.suite?.tasks` counts direct children only and the count is exact per file; a new cell needs a bump (PR states it). A nested describe or a cell with its own lower timeout would be caught only if it is a direct child; I did not run a per-cell-override or nested-describe mutant (unmeasured).
4. A real hang in these fake-timer cells now takes 60 s per cell to surface (measured 60003 ms vs 5003 ms); stated by the builder as a known limit.
5. `originate` and `tokenisation` have `db.ts` without the KS-377 retry code and without a db.retry test (checked, section 2); no gap today, and nothing guards a future new copy (builder states this).
6. Bite-run attribution: for the vitest head-with-budget bite run I counted the one failure as the pin cell (nine cells vs pinned 8) without printing its name.

## Not measured

- The full suites of the 16 services, the platform suites, or any run under real fleet load (the cold-import 9650/11498 ms figures are the builder's, not reproduced).
- Per-cell lower-timeout override and nested-describe mutants (section 3 note); H3 (`beforeAll`) and H9 (late top-level call) bites.
- The PR body and mergeability on GitHub; the pre-push preflight legs; eslint/typecheck other than the commands listed; CI.
- Whether vite wrote cache files through the node_modules symlinks into the project install (not checked).
- Anything on Windows/Linux, or Node versions other than the host's.
