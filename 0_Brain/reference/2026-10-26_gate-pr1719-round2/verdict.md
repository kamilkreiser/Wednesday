# QA delta gate (tier 2, findings-only, ROUND 2 of 2) - PR #1719 (KS-1331)

Model row G2 (claude-sonnet-5-5). Nothing pushed, merged, commented; no ticket, no box touched.

## BLUF
**GO WITH NOTES.** Round-1's MEDIUM-LOW finding is CLOSED: deleting the pgid guard now turns exactly one cell red (GUARD) with the four controls green, 69/1, and I reproduced it independently. The runner is byte-identical to the round-1 head. The `set +m` claim measured true. Merge onto develop is textually clean and the merged tree's suite is 70/0. Two residues, both LOW, to ticket (below). One claim I could NOT verify: the "declared limit" about the empty-pgid branch is not in any text I could read.

Pins: develop `6fc4f2bd4629f1825553c51f7115a9e5b287ebf7`, #1719 head `de47a49d4975b5715da0a1ab7398c8b111b2dc49`, via ls-remote at start (git@github.com:Secuura/Distributed_Secuura.git) and again at 14:43:22Z. Both unchanged.

## Round-1 findings: closed / open
| Finding | State |
|---|---|
| MEDIUM-LOW: pgid guard has no test cell (mutant survived 65/0) | **CLOSED** - GUARD cell reds under the mutant, controls hold |
| `set +m` mutant survives | **CLOSED as documented, not as a cell** - measured not load-bearing; see section 5 |
| LOW: TERM-ignoring suite survives (declared by builder) | OPEN, was already declared, unchanged this round |
| LOW: comment precision (a) foreground external command, (b) SIG_IGN inheritance inferred | OPEN, unchanged (this round touches the test file only) |

## FOUND

1. **Delta.** `git diff --stat 00f245b5..de47a49d`: ONE file, `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh`, 93 insertions, 0 deletions. One commit, `de47a49d4`. Runner `Blockchain/Dev/scripts/run-shell-suites.sh` sha256 at both commits: `3b1ef6581ef3da2ad1ab3a0eb94666d15106f8b2497cfc1109afaaa27dbf2e6b` (identical). R's claim "runner byte-identical" CONFIRMED. The added code is one function `guard_run` and five cells (1 FIXTURE, 3 CONTROL, 1 GUARD), as described.

2. **Suite at head, direct** (own session via `start_new_session`/`setsid`, private `TMPDIR=/tmp/g1719/...`):
   - INT installable line: `(signal environment: INT installable=yes, TERM installable=yes)` -> **70 passed, 0 failed**, rc 0. R's 70/0 CONFIRMED.
   - With SIGINT ignored on entry (the hook's shape): `INT installable=no` -> **67 passed, 0 failed**, rc 0 (INT arms print UNREACHABLE; the new GUARD cell is TERM-based and still runs).
   - **Through `run-shell-suites.sh`** (serial, own session):
     - SIGINT default: in-runner line `INT installable=yes, TERM installable=yes` -> `shell suites: 94 passed, 0 failed, 2 skipped (of 96)`, rc 0.
     - SIGINT ignored on entry: in-runner line `INT installable=no, TERM installable=yes` -> `94 passed, 0 failed, 2 skipped (of 96)`, rc 0.
   - Difference from R's 95/0/1/96: my second skip is `preflight_test_types_ratchet_leg.test.sh`, whose own output says "SKIP - workspace install absent (leg 1 refuses this tree)". My fresh `--shared` clone has no `node_modules`. Environmental, not a PR effect; the first skip (ks949, no PostgreSQL) matches R. Skips are counted and named, rc stays 0, accounting intact.

3. **R's mutant reproduced** (copy of the runner with the guard condition reduced to `[ -n "${rss_suite_pgid:-}" ]`, passed via `RUNNER_SH`, so the committed runner was never edited): **69 passed, 1 failed**, rc 1. The only FAIL line is `KS-1331 GUARD: ... expected 1, got 0`. FIXTURE and all three CONTROL cells `ok`; the pre-existing KS-1331 TERM/INT grandchild cells `ok`. Reproduced twice (direct under INT-installable=no giving 66/1 of 67, and under INT=yes giving 69/1 of 70). R's 69/1 CONFIRMED.

4. **My own mutants on the guard** (each a unique-anchor edit of a COPY, sha256 of the unmutated copy verified equal to head's):

| Mutant | Result | Caught by |
|---|---|---|
| M2 invert comparison `!=` -> `=` | 65 passed, 2 failed | GUARD **and** the existing "SIGTERM to pid - grandchild GONE" cell (so the group kill is also lost under real `set -m`) |
| M5 compare suite pgid to suite PID instead of own pgid | 65 passed, 2 failed | same two cells |
| M3 drop the `-n "$rss_own_pgid"` test | 70/0 (INT=yes), 67/0 (INT=no) | **SURVIVES** |
| M4 drop the `-n "$rss_suite_pgid"` test | 70/0, 67/0 | **SURVIVES** |
| M6 remove `set +m` | 70/0 direct | **SURVIVES** (as R stated) |

   M3/M4 survive because they differ from the real code only when `ps` returns an empty pgid, which no cell makes happen. For M3 the unguarded outcome would be a group kill when our own pgid is unreadable (the dangerous direction); for M4 an empty suite pgid yields `kill -TERM -` against no group (probably a harmless error, but unmeasured). These are the exact branch R says is "reasoned, not exercised".

5. **PR-body `set +m` paragraph vs R's numbers.** I could not read the LIVE PR body (`gh` unauthenticated in my shell; unauthenticated API returns 404 for the private repo). I read R's local drafts `PR-ks1331-body.md` (lines 132-148, mtime 00:51), `comment-ks1331-round1.md` and the commit message of `de47a49d`, which carry the same paragraph. Their numbers (suite 70/0 with and without; full runner 95/0/1 of 96 with and without; five job-control-noise patterns 0 and 0) match R's `nosetplusm_suite.log` (70/0) and `nosetplusm_runner.log` (95/0/1 of 96). My independent measurement: `set +m` removed -> suite 70/0 on the same infrastructure; I did NOT re-run the full-runner or noise-pattern columns for the mutant (only for head). The reasoning given (it bounds job control to one fork; a cell would assert code shape, not behaviour) is sound for what I measured: it is an equivalent mutant on every observable I checked. Residual: the claim is about the 5 noise patterns that R chose; interactive-shell edge cases are not covered by anyone.

6. **Merge-tree.** `git merge-tree --write-tree origin/develop pr1719` (git 2.54.0): clean, rc 0, tree `61077de5155d083238ece414cd68cf431c4a5282`. Merge-base is `5f689991` (develop has since moved by 22 files, one of which is the same test file, +23/-5, textually compatible). Merged-tree scripts directory extracted to `/tmp/g1719/merged` and the suite run in its own session: `INT installable=yes`, **70 passed, 0 failed**, rc 0.

## Residue to ticket (no round 3)
1. LOW. Empty-pgid branch of the guard (failed `ps`) has no cell; mutants M3 and M4 survive. A cheap way to reach it is a PATH-shadowed `ps` stub that prints nothing, run against a fixture runner copy, asserting the sentinel survives (M3) and that no group kill is attempted. Builder already calls it a limit; ticket it so it is tracked.
2. LOW, carried from round 1, unchanged: TERM-ignoring suite not killed by the runner's trap (rc 143 returned, suite left running); two comment-precision gaps on the KS-1330 item-3 comment.
3. LOW, process: the "new declared limit: the empty-pgid branch is reasoned, not exercised" is NOT in the draft PR body, the commit message, or the test file comments that I could read (only the older "signal while no suite runs is reasoned" limit is there). If it was added to the live PR body it is fine; Wednesday should check the live body once, or have R add one line.

## TESTED-HOW
- Own `--shared` clone of `.../spark/cache/src` at `.../spark/cache/work/gate_1719_r2_20261027`; `origin` re-pointed to the GitHub SSH URL and `develop` + `pull/1719/head` fetched there, using the Secuura deploy key via `GIT_SSH_COMMAND` for FETCH ONLY. Detached checkout of `de47a49d`. No write git verb under `/Volumes/DevMASTER/!CODING/`.
- Every test run in its own session (python `start_new_session`/`os.setsid`), private short `TMPDIR` under `/tmp/g1719/`; mutants as copies via `RUNNER_SH`, never edited in the clone. No process killed by name; one cleanup done by PID/pgid (see errors).
- Round-1 verdict and R's evidence read read-only.

## NOT TESTED
- Linux (BSD `ps -o pgid=` and `set -m` semantics).
- The real pre-push hook end-to-end (INT-ignored-on-entry shape was only emulated with SIG_IGN).
- The live PR body text.
- Empty-pgid (failed `ps`) behaviour, in the mutant or the real code: no cell, no stub.
- Full runner with the `set +m` mutant (only the direct suite).
- The TERM-ignoring-suite and comment-precision items (not changed this round).

## Instrument errors (mine)
1. Reflexive `cd` and `$G` variables in `git -C`: the workspace hook refused several calls (it treats `git -C $VAR` as an outside-workspace write verb); re-issued with literal paths. No effect on results.
2. First batch of runs launched with a shell `&` job, which gave INT-ignored-on-entry, so they reported 67 not 70. Re-ran with an explicit `SIGINT` disposition to get both shapes; both are reported above.
3. First parallel full-runner runs (7 concurrent) produced two spurious red suites (bootstrap_login_diagnosis, quarantine_call_sites) from resource contention; discarded, re-run serially (94/0/2 twice). Not a PR finding.
4. A `sed -i` for the SIG_IGN toggle failed on macOS and a mis-configured full-runner run was started; I stopped it by its own PID/pgid (47726 / -47733), nothing else, then fixed the harness with python and re-ran.
5. `==` as an echo separator was refused by the zsh hook; trivial.
6. I used `pgrep -f` to display (not to kill) my own harness PIDs; kills were by PID only.
7. Wrote only to my workspace, `/tmp/g1719/`, and this verdict file.
