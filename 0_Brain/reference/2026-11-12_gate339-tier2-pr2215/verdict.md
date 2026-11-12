PR 2215: GO WITH NOTES (at head ba847c2ef9f9; tier 2; round 1)

Gate 339, tier 2 (Sonnet), one session, 2026-11-12 about 20:27 to 20:40 AEDT. Findings only: nothing pushed, commented, mailed, merged or written to Linear. The project checkout was touched only by `GIT_OPTIONAL_LOCKS=0 git ls-remote`. All write verbs, installs and runs were in `scratch/` of this folder (`scratch/repo` blobless clone, push URL DISABLED; worktrees `wt-head` = PR head, `wt-parent` = fa2d60ca8cee, `wt-plant` = planted merge controls; `npm ci --ignore-scripts` in the first two, then `tsc` build of packages/shared only; every npm/vitest call named an absolute directory). GitHub: reads only (`gh pr view`) with the Blockchain project's gh config. Node v26.8.1 (NOT the LTS line), no Docker stack.

**Pins.** Start (20:27) and end (20:38), identical: develop eab5ac6bff8ddb3f5e63264083ada73eb8405a4b; refs/pull/2215/head ba847c2ef9f9e649ba9369cae33501698703dc31; refs/pull/2052/head b61674e7b7635a50d51f837849cb9caf1259235d. NONE MOVED. PR: open, not draft, MERGEABLE, base develop, 1 commit (parent fa2d60ca8cee), `closingIssuesReferences` empty, +17 -5, 3 files.

**Verdict in one paragraph.** Every number I could re-take reproduced. The change is exactly the three files claimed, no assertion touched (56 `expect(` before and after), exactly five cells carry the constant (checked by pairing each `it(` opener with its closer), the --testTimeout control reproduces (5 of 31 time out at the parent with the literal text "Test timed out in 40ms", 0 at head), the whole services/auth suite is 1850/1850 at head, the develop move touches no path of the PR and the PR merges cleanly onto eab5ac6bff8d, and the 2052 overlap merges rc 0 in both orders with the planted and twin controls reading as they must. Remaining items are disclosed or process notes; nothing blocks.

## Answers

**Q1. Scope: exactly as claimed.**
- `git diff --numstat fa2d60ca8cee ba847c2ef9f9`: test file 10/5; cheat fragment 3/0; flow fragment 4/0; name-status M, A, A. No product, config, lock or workflow file.
- Hunks (-U0): one added block (4 lines: 3-line comment + `const KS1053_WALK_BUDGET_MS = 20000;`) at old line 28 and five one-line changes `});` -> `}, KS1053_WALK_BUDGET_MS);` at old lines 148, 347, 362, 547, 564. Nothing else.
- `expect(` count in the file: 56 at the parent, 56 at head.
- Which cells: awk pairing every top-level `it(` opener with its closer over the head file: the five BUDGET closers close the cells opening at head lines 146 ("is NOT seeded when DEMO_SECUURA_PASSWORD is unset"), 323 ("the enumeration actually finds seed sites, including the one the gate planted in"), 354 ("no executable seed site anywhere in the tree names the real address"), 545 ("the walk finds .env.example files at all"), 554 ("none of them assigns a non-empty value to an admin password variable"). The other 26 cells have plain closers (the awk listing shows each as "plain"); a second grep for any other `}, <ident>);` closer, `testTimeout`, `setTimeout` or `hookTimeout` found only the five (positive control: the five themselves; 6 `KS1053_WALK_BUDGET_MS` occurrences = 1 definition + 5 uses). The file has 31 `it(` cells (matches "31 of 31").

**Q2. Shape and cost.**
- No config-level timeout exists: grep for "timeout" (case-insensitive) over `services/auth/vitest.config.ts`, `vitest.setup.ts` and `package.json` returns nothing (control: `setupFiles` is found in the same config; I read the config whole: no `testTimeout`). So the body's premise is true.
- Per-cell vs config: per-cell is the narrower, reviewable choice and matches Wednesday's ruling; a config budget would loosen all 1850 tests, a `beforeAll` hoist changes test structure. Both shapes are named and not taken in the body. The per-cell argument is shown to win over the command-line value (the control in Q3).
- Cost, stated not ruled: a hang in one of these five cells is now silent for 20 s instead of 5 s. I planted it: a copy of the file with a 22 s sleep at the top of the ".env.example walk" cell fails with "Test timed out in 20000ms" (file takes 20.43 s, 1 failed, 30 passed). So the budget is real and bounded, not infinite. Five cells x 20 s is at most 100 s of added worst-case wall time in the pathological case; on a healthy run they take 44 to 190 ms. Whether a 20 s stall is acceptable in CI is for the seat; the PR states it.

**Q3. Controls and suites (Node v26.8.1; load1 between 3.6 and 7.9 at every start, always under 8).**
- ks949 file alone: head 2 runs 31/31 rc 0; parent 2 runs 31/31 rc 0.
- `--testTimeout=40`: parent rc 1, 5 of 31 failed, all five are exactly the five cells (141 ms, 40 ms x4), default-reporter log shows 5x "Test timed out in 40ms"; head rc 0, 31/31, 0 timeouts. `--testTimeout=150`: parent rc 1, 1 failed (the "is NOT seeded" runSeed cell, 152.6 ms); head rc 0, 31/31. Both match the seat's claim exactly. (My first JSON-reporter attempt could not show the failure text, vitest reports STACK_TRACE_ERROR there; I re-ran with the default reporter. Logs `tt40def_*.log`, `tt*_wt-*.json`.)
- Whole services/auth suite at head via the package script (`npm run test --prefix .../services/auth -- run`): 150 files, 1850/1850 passed, rc 0, 41 s. The flake FINDING 1 did not appear. I did not run the whole suite at the parent (the seat reports 1850/1850 there; I did not reproduce it).
- Method note, see G339-2215-4: my first whole-suite run launched with vitest `--root` from the WEDNESDAY working directory gave 1837 tests, 2 failed files, both artefacts of cwd; the correct launch (cwd = package dir) is the 1850/1850 above.

**Q4. Develop move: confirmed.** `git diff --name-only fa2d60ca8cee eab5ac6bff8d` = 6 paths (root package.json and package-lock.json, tests/connectors jest.config.cjs and vitest.config.ts, the two KS-2182 fragments); `comm -12` with the PR's 3 paths = 0 (positive control: the same diff lists the root lock, so the diff is non-empty and path-readable). No services/auth path. `git merge-tree --write-tree eab5ac6bff8d ba847c2ef9f9` rc 0, no conflict lines.

**Q5. Overlap with PR 2052: reproduced.**
- Merge base of the two heads cfb6c1573ba9. 2052 changes the test file in two hunks (@@ -532,3 +532,4 and @@ -572,4 +573,5: the `.env.example` walk line and the `env.example` read; +5 -3 in that file; 2052 is 29 files in all).
- `merge-tree --write-tree` pr2215 pr2052: rc 0; pr2052 pr2215: rc 0; the SAME tree d07da01bdec6 in both orders, equal to the seat's tree id. Merged file vs parent: +15 -8 = 10/5 + 5/3.
- Survival control: in the merged file `KS1053_WALK_BUDGET_MS` x6, `KS-1081` x2 and the new `env.example` match present, the old `resolve(here, '../../../../.env.example')` line absent (0). Both sides survive.
- Planted control (PR head + one edit on the exact line 2052's hunk 1 removes): rc 1 in both orders (conflict in the ks949 file). Twin control (one comment line added at the file's top): rc 0 in both orders. Positive and negative controls both fire.

**Q6. Body: yes.** First block after the title is the "TIER 2: test-only ..." statement. Ticket keys: `Refs KS-1053` in title and heading; KS-1081 and KS-966 appear only inside code spans (lines read); regexp for fix/close/resolve forms over the whole body: none; `closingIssuesReferences` empty. Flow and cheat fragments both present (pair, the ruled exception), with the 1053 key and the right file; I did not re-run the docs-fragments check.

## Findings

**G339-2215-1 (Note): no natural red-first; the fix is unproven against the flake itself.** A timeout is not an assertion; the PR proves the mechanism (per-cell argument beats a 40 ms and 150 ms default) and the planted 22 s hang proves the new bound, but neither this host nor the seat's reproduced the 5.0 to 7.8 s durations. The PR says so in its "Not claimed". If the flake recurs above 20 s the ticket reopens. No action.

**G339-2215-2 (Note): worst-case silent time per cell is now 20 s.** Reproduced (planted hang, fails at 20000 ms). Stated in the body's "Cost". Four of five cells walk the repository tree, so a growing repo makes the walk slower and eats the headroom; a future `walk` speed-up (the shape not taken) would fix the cause. Not a defect.

**G339-2215-3 (Info): the `runSeed` cell is the only non-walk cell budgeted, and at 150 ms it is the one that failed at the parent.** Its inclusion is justified by the ticket's own measurement; other unbudgeted `runSeed`-style cells exist (26 plain cells all passed at `--testTimeout=40` and at 150, so none is near the old 5 s limit on this host).

**G339-2215-4 (Info, gate method): two auth tests are cwd-sensitive.** `ks1009-wallet-status...` and `ks1467-...` (not touched by this PR) locate files from `process.cwd()` and fail (2 files, 1837 tests) if vitest is launched with `--root` from a different directory; they pass 1850/1850 when launched in the package directory. Not this PR's concern; worth knowing for gate scripts (use `npm --prefix`, not `vitest --root`, for the whole auth suite).

**G339-2215-5 (Info): corrected note.** An earlier draft of this verdict mis-stated a tree-id difference; it was my error (ad14b694be28 was the tree of the planted-control merge, which conflicts). The real pr2215/pr2052 tree is d07da01bdec6 in both orders, identical to the seat's. No discrepancy.

**G339-2215-6 (Info): hook text.** "PREFLIGHT INCOMPLETE - 13/16 legs, 3 SKIPPED" is correctly quoted and not presented as a pass in the body. I did not run the hook.

No Major or Minor finding.

## NOT TESTED

- Flake reproduction (the 5.0 to 7.8 s durations) and any loaded whole-suite run; whether 20 s is enough under fleet load.
- Node 24 (only v26.8.1 here), the Docker stack, the four platform suites, eslint, check:test-types, tsc with tests, audit:gate, docs-fragments check, the pre-push hook legs.
- Whole services/auth suite at the PARENT (seat claim 1850/1850 not reproduced; I ran only the ks949 file at the parent).
- Whole suite or ks949 file on the merged tree of 2215 + 2052 (merge-tree contact only), and on eab5ac6bff8d (merge-tree only; no install/run on the new root lock; the PR touches none of those paths).
- Every other open PR's contact with the test file or fragments (I read only 2052; the seat's census of 102 PRs and the claim that no other PR touches the file were not re-run).
- Linear (KS-1053 comment, attachment, ticket thread's durations), the body's claims about the 2026-10-30 measurement, the `CLAUDE.md` Node-24 statement.
- A vitest `vitest.setup.ts` read in full (I grepped it for "timeout" with a same-config control but did not read the file whole).
- The Spark shadow review (not requested by this commission).
