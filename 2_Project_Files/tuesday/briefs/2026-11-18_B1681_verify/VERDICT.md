GATE B1681: GO WITH FINDINGS @ 7bc1c5d on main 751285a

Reviewer: independent G2 (tests-only tier), Sonnet, in-session. Target: datasecau/Reporting_Dashboard_Au, branch `b1680/nexusai-lane-nx-t3-test-tail`, head `7bc1c5d201c6f39b78fc2af9e0ca10c1436565c1` over main `751285aa138f366e44d0ef97e1464dc6bf52c436` (merge-base = main, so the branch is 5 commits on current main). Clock `date` 18 Nov 2026 01:51 to 02:19 AEDT. One lock acquisition (`b1681-gate`, acquired after 0 s, released at the end), `env -u NODE_OPTIONS`, `--maxWorkers=2`, own clone `fleet/state/s287/g1681/clone` (jest slot 14, band 28960-29599, `lsof` 0 listeners before the run), `npm ci` done there.

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Advisory (flake risk, not a defect) | H1's new bound is 4500 ms. Measured: real cap 3146 3147 3147 3147 3148 ms (five runs at head, load average about 4.2), flat 5 s cap 5642 5653 5654 ms (three runs) and 5639 ms (base file). Headroom 1.35 s above the real time; 1.14 s below the flat time. The bound sits near the middle of the two (midpoint 4.4 s), which is the right place to detect the flat cap. Judgement below. |
| F2 | Info | The committed comment's numbers (3203 3147 3151 3154 3150 real; 5661 5662 5659 5654 5652 flat) are the builder's, not mine; mine agree within 60 ms. The margin digits are unchanged from the frozen 1500, as the kit's rule allows (B 3203 <= 4000, F 5652 >= 5000). |
| F3 | Info | The ticket text for RD-1002 says counts "stay at 5867/377"; main holds 5868. The commit did not repeat it; the pair moves 5868 to 5870 by two new cells, as intended. |
| F4 | Info | The full verify prints "A worker process has failed to exit gracefully and has been force exited" (jest). I did not measure whether base prints it too; it does not change the verdict (exit 0, `VERDICT: PASS`). |
| F5 | Info | CodeQL is not on PATH here; by-hand rows below. |

No blocking finding.

## Margin judgement (RD-729, F1)

H1's time is the 3 s wall-clock deadline plus about 150 ms (one 250 ms-capped attempt, the 500 ms sleep, failBoot's SIGTERM wait, all of which were already inside the measured 3.15 s). Hosted CI adds scheduling delay on top, but the deadline is a wall clock, so a slow runner mostly delays the tail by its scheduling jitter; 1.35 s of jitter in a path that did 150 ms of work here is roughly 9x. The Linux/Node 24 runner with `--maxWorkers=2` has no heavier load than this laptop at load 4. I judge the 1.5 s margin sufficient, with low but non-zero flake risk. I measured only at load about 4.2, not under heavy load: that is a limit of this measurement. If it ever flakes, widening the margin to 1800 to 2000 ms still fails the flat cap (5.64 s) with 0.65 s or more to spare, so the fix would be a one-digit change.

## Measured rows

1. Diff = exactly the five paths (name-status: five `M`; `__tests__/helpers` diff stat 0 lines; no product, doc, workflow or script file other than `scripts/verify-expected-counts.json`). The counts file changes only `_updated`, `tests` 5868 to 5870, `suites` 377 unchanged.
2. Four test patches vs the kit's frozen diffs, multiset of +/- lines (program `cmp.py`): rd969, rd638, handover-gate-table: kit-only {} and actual-only {} (identical). rd648: kit-only {}, actual-only exactly one line, the measured-numbers comment (`// Measured (five runs each, ms): ...`); the `H1_MARGIN_MS` digits equal the frozen 1500.
3. Added lines: non-ASCII characters 0 (control: a planted U+2014 counts 1); counts of `.skip(` `.only(` `.todo(` `xit(` `xdescribe(` `.each(` `setTimeout` `setInterval` `RegExp(` all 0 (control: `.only(` on a planted string counts 1); `product owner`, `ruling`, `Tuesday`, `Wednesday`, `Kam`, `seat`, `card`, B-number pattern, and the secret-word set all 0. Commit messages (five): the same greps print nothing; the only ticket keys are RD-1002, RD-734, RD-729, RD-730 and, in the added comments, RD-985 and RD-958 (history keys the kit allows).
4. Commit identities: author and committer of all five commits are the project repo's configured `user.email` (equality: yes for all ten fields; the value is the repo-local noreply address, not printed here; my own shell's global email differs, the project's does not).
5. RD-1002: the a-pred program (`apred.py`, the kit's frozen text): base missing `H6 H7 H8` (rc 1); head missing none (rc 0); control (H7 and H8 renamed in a head copy) reports `H7 H8` (rc 1). The diff of the file is comment lines only (the multiset equals the kit patch; every +/- line is a ` * ` header line). Ticket read at source (GET-only): RD-1002 asks exactly that; To Do, no comments.
6. RD-734: `E2_STOP_MS = 20000`; harness `h.stop` is at `__tests__/helpers/rd395-server-harness.js:210-215` with `stopBy = Date.now() + 20000` at `:212` then an immediate SIGKILL, so 20000 is the true bound; the constants 120000 + 3000 + 15000 + 20000 + 10000 = 168000 = `E2_BUDGET_MS`; at base 158000. The `5 s` in the old comment is `BOOT_FAIL_TERM_GRACE_MS` (`:81`, used by failBoot at `:138` and `:141`), as the ticket and the new comment say. I did not run the all-bounds path (a 120 s boot); the kit says so too.
7. RD-730 plants, each run once, each reverted by copying the saved original back, `git hash-object` equal to the HEAD blob after each (yes x3):
   - P0 (head, four files): 22 cells pass: handover-gate-table 7, rd969 11, rd638 2, rd648 2.
   - P1 (old `shaFormatProblems` line `if (!line.startsWith('|')) { if (row >= 0) break; continue; }` put back, match count 1): 7 cells, 1 failed: the blank-line CONTROL cell only.
   - P2 (`return 'archive';` for the ENOENT branch): 1 failed: the git-probe CONTROL cell only.
   - P3 (`catch (e) { return 'no git'; }`): 1 failed: the git-probe CONTROL cell only.
8. RD-729 A-F1 (P4, `Math.min(5000, deadline - Date.now())` term planted flat `5000` in the clone's harness, match count 1): head rd648: H1 RED (5642 ms; again 5653 and 5654 ms in two H1-only runs), K1 green. The same plant with BASE's rd648 file copied in: 2 of 2 GREEN (H1 5639 ms): the old bound could not see it, the new one does. Harness, rd648 and gate-table all back to the HEAD blobs; `git status --porcelain` 0 lines after the plants and after the verify.
9. Full verify at head in my own fresh tree, one lock acquisition, `npm run verify -- --maxWorkers=2`, 1310 s jest time (01:56:55 to 02:18:46): `VERDICT: PASS - 5870/5870 tests passed across 377 suites (jest exit 0)`. Committed counts file at head: tests 5870, suites 377: equal to the received pair. `--update-counts` was never used.
10. CodeQL (by hand, no `codeql` on PATH): added lines contain no `RegExp(`, no `eval(`, no `new Function`, no request value used in a path, no shell string built from input (the one new `execFileSync('git', [...])` is the existing probe with a fixed argument list, only moved). The new test title is ASCII. Hosted CodeQL on the merge commit remains Tuesday's.
11. Tickets: RD-1002, RD-734, RD-729, RD-730 all To Do, no comments, read GET-only. RD-729 stays open after this lands: A-F2 (a helper change), A-F3 and A-F4 are untouched, which the PR body says.

## PR files

`pr-title.txt`, `pr-body.md`, `merge-subject.txt` (placeholder `(#PRNUM)`), `merge-body.txt` are beside this file. The deploy-demo workflow is not path-ignored for `__tests__/**`, so a merge starts a Deploy demo run whose jobs must read `skipped`; that is Tuesday's to confirm after the merge.

Scratch (clone, programs, jest JSONs, logs): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/g1681/`.
