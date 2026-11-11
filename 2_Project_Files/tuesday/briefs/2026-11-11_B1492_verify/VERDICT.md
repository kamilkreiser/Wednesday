GATE B1492: GO WITH FINDINGS @ e290417 on main 0ab365b

Branch `b1492/nexusai-rd407-r2-counted-not-timed`, head `e290417a1861c8806b6d44864a67ecc54963aa55` (origin, `ls-remote` 13:55 and 14:23), one commit, parent = main `0ab365b1db62c2b60cb63de9deb1ceccb0b1c4c9`. Main did not move during the gate (`ls-remote` 13:55, fetch at 14:02 inside the verify batch, `ls-remote` 14:23), so the head IS the branch merged with main and no merge-check was needed. Test-only rewrite of cells M2, R1, R3 in `__tests__/rd407-r2-missing-mid-swap.test.js`.

BLUF: 0 Blockers, 0 Majors, 2 Minors. Diff is the one test file; titles and the counts file are unchanged; every `toEqual` value is unchanged. On my own clone and trees: new cells 12/12 plain and 10/10 under an in-realm 3x slow-sleep shim; old cells 3/3 red on exactly M2, R1, R3 under the same shim (and 3/3 green plain this afternoon, so the shim alone is what turns them red). P1, P3 and P2b turn the new cells red as the kit requires. Full plain verify of the head: `VERDICT: PASS - 5536/5536 tests passed across 331 suites`, EADDRINUSE 0. One narrow lost sensitivity, measured (F1).

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref and parent | origin head `e290417a...`, its only parent `0ab365b1` = origin main; `rev-list --count main..head` = 1 | `git ls-remote`, `rev-parse head^@`; control: `refs/heads/main` prints a sha |
| 2 | Scope | `git diff --name-only main head` = the one test file only; no product file; `.github` diff 0 lines | git; control: `main~3..main` lists 12 files |
| 3 | Titles / counts | 17 `test(` + 5 `describe(` lines at both sides, the 22 title lines `cmp` EQUAL; counts file blob `1eae9cc5` at main and head; `git diff --quiet` on it rc 0 | one extraction program; controls: a one-byte change to the title list makes `cmp` rc 1; `diff --quiet` on the test file rc 1 |
| 4 | Assertions line by line | 17 `expect(` lines both sides; the 17 `.toEqual(...)` payloads are textually identical old vs new. Changes: `forMs: PAST_BUDGET_MS` -> `forMs: Infinity` in M2, R1, R3 (the name stays missing longer: never easier to pass); M2 `spentTheBudget: elapsed >= BUDGET` -> `requestedMs >= BUDGET`, where `requestedMs` sums `args[3]` of a pass-through `jest.spyOn(Atomics, 'wait')` restored in `finally` (same pattern as M3/M4); `PAST_BUDGET_MS` removed (4 uses at main, 0 at head); comments. No skip/only/todo/each/timers added | diff read whole; `grep -c` with a planted `x.skip(1)` control = 1 |
| 5 | Shim in the test realm | `slowsleep3x.cjs` (mine, sha256 `6eec594c64b9...`) loaded only by `--setupFiles` after `home-containment.js`, every jest run `env -u NODE_OPTIONS`. In-realm probe (one-cell jest file timing `Atomics.wait(...,200)` inside the test): before the runs 660.0 ms with the shim / 244.0 ms without; after them 670.7 / 231.4 ms; the shim's call counter read 1 / 0 inside the realm | jest JSON + probe JSON; the no-shim run is the control |
| 6 | NEW cells plain | 12 of 12 runs 17/17 (M2 760-967 ms, R1 829-990, R3 837-1059) | `gnew` at head, jest JSON per run, 17 cells and the test file name checked by program each run |
| 7 | NEW cells under the 3x shim | 10 of 10 runs 17/17; M2/R1/R3 1856-2166 ms each (all above the kit's 1500 ms bar: the full loop ran slowed) | same |
| 8 | OLD cells, control | under the same shim 3 of 3 runs: exactly M2, R1, R3 FAILED, 14 passed (M2 received `outcome: resolved`, changed live/current/prev...; R1/R3 `answer: true, gate: require-session`, i.e. the last retry read the real store). Plain, same acquisition: 3 of 3 runs 17/17 (M2 812-890 ms) | `gold` at main; the plain runs are the control that the shim, not the tree, turns them red |
| 9 | P0 / P1 / P3 / P2b on the NEW cells | P0 17/17. P1 (both `missing:true` returns -> `absent:true`, 2 matches asserted) M2, R1, R3 RED 2 of 2 (R1/R3 `answer: false, gate: allow-open-mode`; M2 `resolved`). P3 (first retry loop `.slice(0, 2)`, first of 2 matches) M2 RED on `spentTheBudget: true -> false` only, plus R2 (`answer: null`). P2b (snapshot catch `unreadable` -> `absent` at `authEnforcement.js:86` AND `getSetting('authEnforced', { strict: true })` -> non-strict at `:677`, 1+1 matches) R1 and R3 RED | `gmut` at head; each plant reverted by saved copy, `git hash-object` = HEAD blob (`bba3742b6d46`, `ca764a4b2c1f`) after each; porcelain 0 in all three trees at the end |
| 10 | Full plain verify of the head | `VERDICT: PASS - 5536/5536 tests passed across 331 suites (jest exit 0)`, rc 0, 1265 s; jest JSON: 5536 total, 0 failed, 331 suites, rd407-r2 17/17; EADDRINUSE 0; band 29600-30239 (slot 15) 0 listeners before and after; tree `c02d5811` = head tree, porcelain 0 before and after | `npm run verify -- --maxWorkers=2` under the jest lock; a PASS is equality with the committed pair (`verify-suite.sh` fails below or above); grep control: the same grep finds the 1 VERDICT line |
| 11 | Scans | names 0 over 6 message lines + 19 added lines (planted `_by_<name>_` fires for all 9 names; `kamera`/`kamikaze` 0); non-ASCII 0 and bidi/zero-width 0 (planted U+202E 1 each); gitleaks over `git log -p main..head` no leaks (planted AKIA-shaped line: `leaks found: 1`) | scan.py, gitleaks 8 stdin |
| 12 | Identity | `%ae | %ce` = `88359143+kamilDatasec@users.noreply.github.com` both; equals the repo-local `user.email` of the seat's clone (copied from the b1484 clone's repo-local config, no override); same identity as 14 of the last 40 non-merge commits on main | `git log -1`, `git config --show-origin` |
| 13 | Deploy demo | `__tests__/` not in `paths-ignore` (`**.md`, `docs/**`, `tests/**`): STARTS A RUN; workflow unchanged; jobs gated on `vars.CI_DEPLOY_ENABLED == 'true'` (:53, :91): expected skipped | workflow text at main |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Minor (test fidelity, measured) | M2 now counts the waits the product REQUESTED, so it no longer notices a wait that returns without sleeping. Plant P4 (`Atomics.wait(SLEEP_CELL, 0, 0, ms)` -> `(SLEEP_CELL, 0, 1, ms)`, which returns `not-equal` at once): OLD M2 RED 2 of 2 (`spentTheBudget: false`, M2 67 ms), NEW M2 green (17/17, M2 65 ms). No other cell in the file catches it. Fail-closed is unaffected (outcomes still STORE_UNREADABLE/deny-unknown); the cost of such a regression would be spurious refusals during a real rename storm. The product itself defines its budget as requested time (`waitedMs` sums requested delays, `jsonStorage.js:2993`), and the kit's design accepted this trade. Suggested follow-up (cheap, still timing-free): in M2 also assert `waitSpy.mock.results.every(r => r.value === 'timed-out')`. Not a blocker. |
| F2 | Minor (process, not the branch) | The project checkout `2_Project_Files/.git/config` has a repo-local `user.email` that is the owner's personal address, not the Datasec GitHub identity. The branch is NOT affected (the seat's clone carried the Datasec noreply identity), but a future clone that copies identity from the project checkout would commit under the personal address. Worth a look by whoever owns that config. |

## Builder STATUS claims
| Claim | Grade |
|---|---|
| one file, 19+/11-, counts unchanged 5536/331 | true (rows 2, 3) |
| titles cmp equal, 17 tests / 5 describes | true (row 3) |
| new-plain 20/20, new-slow 20/20 | consistent: my independent 12/12 and 10/10 on my own trees |
| old-slow 3/3 M2/R1/R3 red | true (row 8) |
| P1 all three red, P3 M2 red on spentTheBudget only (+R2), P2 masked, P2b R1+R3 red | true for P1, P3, P2b (row 9); P2 alone not re-run by me |
| full verify PASS 5536/331, EADDRINUSE 0 | true (row 10) |
| shim must load via --setupFiles, NODE_OPTIONS does not reach the realm | --setupFiles route confirmed live in-realm (row 5); the NODE_OPTIONS negative was not re-tested by me |

## NOT RUN
- Hosted Build, CodeQL, CI on Linux, npm-audit, arm-ttk, `CI_DEPLOY_ENABLED` read, Jira (fences).
- P2 alone and the old-vs-new P2 comparison (the builder's; spot-checked only via P2b as asked).
- The `NODE_OPTIONS` negative (that such a shim does not reach jest's realm): not re-run; no run of mine used NODE_OPTIONS.
- Merge-check against a newer main: not needed, main unchanged at `0ab365b1` through 14:23 AEDT.
