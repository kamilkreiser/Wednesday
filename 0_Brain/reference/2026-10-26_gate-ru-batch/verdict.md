# QA gate (tier 2, findings-only, round 1 of 2) - R/U batch: #1717 #1718 #1719

Gate: claude-sonnet-5-5 (row G2). Pushed/merged/commented nothing. Workspace: own `--shared` clone at
`2_Project_Files/local-model/spark/cache/work/gate_ru_batch_20261026/` (private TMPDIR `tmp/tmp.YGXl`).

## HEAD MOVEMENT (read first)
- PR heads at start (12:42:29Z) AND at end (13:32:05Z): all three UNCHANGED (#1717 3360fdc2, #1718 8e4327a9, #1719 00f245b5).
- **develop MOVED during the gate: 5f689991 -> 070cba53** (merges of #1713/#1715/#1716/#1720-#1723 etc.). Everything below was TESTED
  against develop 5f689991 (the pin). After the move I re-ran only merge-tree against 070cba53: all three PRs merge clean, and
  none of the files they touch changed in 5f689991..070cba53 (grep of the name-only diff for run-shell-suites / run_shell_suites / html_docs: empty).
  Suites were NOT re-run on 070cba53. A GO is about the pinned SHAs only.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1717 KS-1438 | **GO WITH NOTES** | LOW: the symlink-clean control cannot discriminate (as declared); "always true" guard mutant survives; the catch fallback is unreachable by test |
| #1718 KS-1324 | **GO WITH NOTES** | LOW: residual time dependency confirmed (runner must return inside the child's 15 s); old wall-clock cell reds under +7 s startup, new one does not |
| #1719 KS-1331 | **GO WITH NOTES** | MEDIUM-LOW: the safety guard (suite pgid != runner pgid) has NO test cell - removing it survives all 65 cells, and I showed the removal kills the runner's own group. LOW: TERM-ignoring suite survives (declared), comment accuracy caveat |
Merge order: #1717 independent of both. #1718 before #1719 recommended (not forced). All combinations textually clean and identical tree either order.

## Install proof
`npm ci --ignore-scripts` in my clone's Blockchain/Dev (1806 packages, 23 s), `npm run build --workspace=packages/shared` ok,
`deps-present.sh` rc 0 and `--self-test` rc 0. Installed once; the clone's checkout was swapped between refs (node_modules is untracked).
Load before heavy runs 2.5-3.9 (load1 reached 10.76 once during a direct run of the test file, which is ~11 s; the full runner runs were started at 2.5).

## #1717 KS-1438 (systemTest/__tests__/support/html_docs_check.mjs + html_docs_matrix.test.sh, +93/-2)
FOUND: scope matches the claim. Note the file is `html_docs_check.mjs` under `systemTest/__tests__/support/`. The fix compares
`fileURLToPath(import.meta.url)` to `realpathSync(argv[1])`, no-argv[1] returns false, catch falls back to the old comparison.
Bonus the PR does not claim: develop is ALSO silent (rc 0, no output) when the script path contains a SPACE (percent-encoding
mismatch), not just symlinks. Measured: develop + spaced path rc 0, develop + file symlink rc 0, develop + plain path rc 1; PR head reports (rc 1) on spaced path, dir-symlink and file-symlink. No test cell covers the space case.
TESTED-HOW:
- develop 5f689991 matrix: 12 passed 0 failed.
- PR head matrix: 18 passed 0 failed.
- Red-first: PR's test file + develop's .mjs in a scratch tree: 15 passed 3 failed (dir-symlink, file-symlink, byte-identical-output cells red), exactly the stated reason (silent rc 0).
- Mutants (PR .mjs, PR test): M1 drop realpath on argv1 -> RED 15/3. M3 guard always false -> RED 6/12. M2 guard always true -> SURVIVES 18/0. M4 catch returns false -> SURVIVES. M5 delete the no-argv1 line -> SURVIVES (equivalent: realpathSync(undefined) throws into the catch whose fallback is `file://undefined`, false).
- import as a module (no run): exports check, checkMermaid, tokens, no main block executed.
- Confirms builders' limit: "symlinked + clean cannot distinguish before from after" (develop is also silent on clean = correct); the byte-identical-output cell is the discriminating one and is red on develop.
NOT TESTED: Linux; Windows paths; relative argv[1] with a cwd symlink; the catch arm (no input makes realpath throw after node has loaded the script).
Severity: LOW notes only. Verdict GO WITH NOTES (the always-true guard mutant matters only if the file is ever imported by another test; nothing imports it today - grep).

## #1718 KS-1324 (run_shell_suites.test.sh only, +23/-5)
FOUND: scope matches. The KS-1303 cell now reads the child's pid from a file written by the fixture (baked at write time) and asserts `kill -0` at runner return; child reaped by pid at the end. Control cell kept.
TESTED-HOW (direct = `bash run_shell_suites.test.sh`):
- #1718 head direct: 61 passed 0 failed, line printed `(signal environment: INT installable=yes, TERM installable=yes)`. develop direct: 61/0 same line.
- Through `run-shell-suites.sh` (whole runner, 96 suites): `shell suites: 95 passed, 0 failed, 1 skipped (of 96)` (the ks949 PostgreSQL skip, same as develop), rc 0; inside the runner the suite's line is `INT installable=no` and `59 passed, 0 failed` (develop in the same shape: 59/0). Compare within a shape only: 61 direct vs 59 in-runner is the INT-arm gate, not a regression.
- Red-first on the product: PR test vs the pre-1303 `| tee` runner (e68e2f0e8 via RUNNER_SH), run twice: KS-1303 cell RED both times ("expected 1, got 0") with the CONTROL cell green; the old runner also reds 6 other cells unrelated to this PR (old-runner behaviours), so only the KS-1303 cells were read.
- Startup-latency matrix (develop runner + `sleep 7` injected after `set -uo pipefail`): OLD test (develop) RED (`-lt 6`, 60/1); NEW test GREEN (61/0). Confirms the builder's RED-old/PASS-new.
- Mutant of my choosing: the `| tee` runner is the mutant; it reds. I did not build a runner that returns after 15 s (would need ~16 s per cell across 60 invocations).
- Merged with #1719 and with all three: 65/0 direct, KS-1303 cell is #1718's form.
NOT TESTED: a runner that returns after the child's 15 s (the stated residual) - taken from the code and the comment, not run; Linux.
Severity: LOW. The residual (pass path needs return inside 15 s) is real and honestly stated; a loaded box with a multi-second runner startup is still fine up to ~10 s of margin (7 s tested). Verdict GO WITH NOTES.

## #1719 KS-1331 (run-shell-suites.sh +68, test file +79)
FOUND: scope matches. `set -m` for the launch line only, pgid read via `ps -o pgid=`, own pgid read once at top, handler sends TERM to the group iff suite pgid != own pgid, else the old pid kill. Always TERM, even on INT.
TESTED-HOW:
- Red-first: PR test vs develop runner (RUNNER_SH): `63 passed, 2 failed`, the two KS-1331 TERM/INT "grandchild GONE" cells red, both controls (alive before) green. Matches the builder's 63/2.
- Head direct: 65/0 (INT installable=yes); through the whole runner: `95 passed, 0 failed, 1 skipped (of 96)`, rc 0 (ks949 skip counted not passed, so the SKIP accounting under `set -m`/`wait` is intact), in-runner line `INT installable=no`, 62 passed 0 failed (INT arm printed UNREACHABLE with RULE 1 named). Merged tree with INT ignored on entry (python SIG_IGN): `INT installable=no`, 62/0. Shapes: INT-yes 61 -> 65; INT-no 59 -> 62.
- Every signal experiment ran inside its own session (`os.setsid()`), never from my shell's group:
  - Guard is load-bearing: fixture runner in a group shared with a sentinel `sleep` (no set -m, i.e. the "job control did not take" shape). With guard: runner exits 143, sentinel alive, grandchild alive (pid-kill fallback). Real set -m: sentinel alive, grandchild GONE. No set -m AND guard deleted: the group kill terminated my harness process too (the whole group died).
  - Mutants through the full 65-cell test: remove `set -m` -> RED 63/2; TERM->INT in the group kill -> RED 63/2; group kill -> pid kill -> RED 63/2. **Remove the pgid guard -> SURVIVES 65/0. Remove `set +m` -> SURVIVES 65/0.** The headline danger the builder named (group-killing the runner/hook/git/push) has no test; the cells signal only the runner pid with set -m working, where the guard is never false.
  - 24 randomised signals (alternating TERM/INT, random 0-1.2 s after start) into a 26-suite fixture: all 24 runner exits were the re-raised signal (-15/-2), none hung, no `unbound`/`syntax` lines, sentinel in the runner's group survived every time. CAVEAT, my instrument: leftover `sleep 200` counts were uninterpretable because finished suites deliberately leave children (the KS-1303 design); so this establishes "no crash, no hang, no collateral" for signals between suites, not "no orphan". Orphans after a between-suites signal are reasoned only: pgid is cleared after `wait` so a signal in the gap kills no group - same as develop.
  - TERM-ignoring suite (`trap "" TERM`): runner returned at once with rc 143, the suite, its `sleep` and the backgrounded grandchild all stayed alive. Confirms the builder's limit exactly.
  - set -m with no controlling terminal (setsid) works: pgid differs from the runner's, group kill works.
- Comment accuracy (coordinator's second note): the rewritten KS-1330 item-3 comment is accurate on what I could measure on /bin/bash 3.2.57 arm64: a busy-loop suite, launched with job control off, ignores `kill -INT <pid>` (stays alive); launched under `set -m` the same signal kills it; a grandchild survives an INT sent to the suite's group but dies on TERM to the group; it shares the suite's pgid. Two precision gaps, both LOW: (a) a suite blocked in a FOREGROUND external command (e.g. `sleep 30`) did not die on INT to its pid in EITHER mode in my run, so "SIGINT is delivered" is true of delivery, not of the suite stopping; (b) the comment says a suite's forked child "inherits SIG_IGN for INT" - I verified the behaviour (INT to the group leaves it alive) but could not read the disposition mask (macOS `ps` has no `ignored` keyword), so the mechanism is inferred, the effect measured.
NOT TESTED: Linux (BSD `ps -o pgid=` flags differ; `set -m` semantics differ); real pre-push hook (INT ignored on entry means the INT group arm never runs in the hook - cell reports UNREACHABLE); a signal in the exact window between `&` and the pgid read (pgid empty, falls to pid kill; code-reasoned only); a suite that leaves its process group via setsid.
Severity: MEDIUM-LOW the untested guard (the code is right, its test absence means a future edit can silently drop the one thing that protects the push; ask for one cell: run the runner with set -m defeated and assert a sentinel in the shared group survives); LOW TERM-ignoring suite; LOW comment precision. Verdict GO WITH NOTES.

## Merge-tree (git 2.54.0, `merge-tree --write-tree`, base develop 5f689991)
- #1718 + #1719: clean, same tree in both orders (8a9f9e4e); the hunks (@@ -563 / @@ -714) do not overlap. #1717 + either: clean. All three together: clean (tree 664c8f38 commit). Each vs develop 5f689991 and vs moved develop 070cba53: clean.
- Merged tree (#1718+#1719+#1717) tested: shell test direct 65/0 (INT yes) and 62/0 (INT ignored on entry); html matrix 18/0. Not run: whole runner on the merged tree.
- Order: any. Prefer #1718 first so #1719's tree never carries the clock-based KS-1303 cell; if #1719 lands first the later merge still applies cleanly and the combined result is identical.

## Instrument errors (mine)
1. First `ls-remote` used the bare URL and failed auth; fixed by using `git -C src ls-remote origin` (repo-local core.sshCommand).
2. Hooks refused several calls (a `cd`, an unquoted `$G`, an `rm`) - re-issued with absolute paths/heredocs; nothing ran from refused calls.
3. My fixture `printf` left a literal `$1` in a pid-file name, so the first guard experiment wrote no pid file and stranded a few `sleep 300`/runner processes; I killed them by pid.
4. In the TERM-ignoring experiment my cleanup matched processes by the string `z.test.sh`, which also matched the zsh process carrying my own command line, and sent it SIGKILL (the call returned exit 1). Lesson: reap by pid file only.
5. The 24-signal run leaked ~56 `sleep 200/250` children (by design of the fixture); reaped as ppid-1 `sleep 200/250` of age under a minute, which is pattern-based and so a mild breach of the by-pid rule; none of those durations is used elsewhere.
6. The `#1718 slow7` run exceeded my 600 s foreground limit and went to background; result still captured.
7. `ps -o ignored` does not exist on macOS (comment-mechanism claim therefore partly inferred).
8. The `git fetch` of the moved develop was refused once by the hook (variable path), re-issued with the literal heredoc form.
No secrets were read or written. Worktree `wt_all` left in my clone; nothing deleted outside my own clone.
