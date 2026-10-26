STARTABLE: YES

# B728 drafter report (SEAT-G140, NexusAI PR #118 flake-fix gate, tier 2 Sonnet)

Drafted 2026-10-26 10:42-10:5x AEDT (clock from `date`: 10:42:09 at first read). Kit: `2026-10-26_B728_SEAT-G140_nexusai-118-flake-gate-tier2.md` (80 lines, shape of B714). Launch needs your stamps in the 8 slots (S1-S7 and the last line; control: `grep -c` of four underscores reads 8); nothing else blocks it.

## BLUF
- Gate for PR #118 at head `610a8759` (1 commit, 1 path, +30 -1) on main `61154bba`; round 1 of 2, new class "a test-only fix whose stated mechanism or effect its evidence does not discriminate".
- The heart is Check 2: the gate builds its OWN plant: a separate-process squatter on the stand's port (IPv4 wildcard answering, IPv4 wildcard closing, and a 127.0.0.1-only boundary) plus a `net.Server.prototype.listen` preload that rewrites the stand's `listen(0)` to a planted port and never touches the host argument, so the REAL base and head blobs run under the same plant. Controls: log-only preload green, unheld ports green, base must be red (otherwise the property is NOT TESTED, not "fixed").
- Check 6 reads each header sentence. Two look wrong against the builder's own STATUS (see UNMEASURED/Findings below).
- CI and CodeQL are read once at the verdict (as commissioned); at 10:4x `build` and all three `Analyze` runs were in progress, so GO WITH FINDINGS is the likely ceiling unless they finish before the gate does (Q-3).

## Facts re-measured (instrument, control)
- Refs, `git ls-remote origin` 10:42:09: main `61154bba`, branch = `refs/pull/118/head` = `610a8759`, merge ref `cc4bc12f` (`git/commits`: parents `61154bba` then `610a8759`, tree `ff95b216`; head parent `8ae0a87f`, head tree `474ae4be`). `pulls/118`: open, not draft, mergeable true, state blocked, commits 1, files 1, +30 -1; `pulls/118/files`: the one path, blob `be8307ad` equal to the builder's. Control: the compare `8ae0a87f...61154bba` lists the 5 PR #117 paths (a different pair that does change paths); none is the PR's path.
- Diff read whole from `compare`: 26-line header paragraph + 3 comment lines + one code line (`app.listen(0, () =>` -> `app.listen(0, '127.0.0.1', () =>`). The contents GET at the head greps 2 occurrences of `listen(0` (one in the comment, one the code line).
- Open PRs: #118 only. CI at the head: success `scan`, `audit-production-deps` x2, `npm-audit`, `PR #118`; `CodeQL` check-run completed neutral; in progress `build` (run 40245881901), `Analyze` x3; analyses on the PR ref: 1 (actions). Ruleset: `code_scanning` errors / high_or_higher, required checks empty.
- Deploy demo: last four runs push / completed / skipped (newest 40243398353 at `61154bba`).
- Ports: `lsof -nP -iTCP:9880-9899 -sTCP:LISTEN` empty (rc 1). Word-boundary scan of non-`.pre-` SEAT kits of 10-25 and 10-26 for `988[0-9]`: only finished 10-25 HPSM-POC kits (B638, B639, B693); no 10-26 hit. Control: `982[0-9]` hits live MPS gates B715 and B722, so the scan fires. 9800-9879 are all named by kits (B713 9800s, B714 9810s, and so on), which is why this kit moved to 9880-9889.
- Panes (`tmux list-panes -a -F '#{@cockpit_name}'`): tuesday, HPSM-POC H31 H32 H33 G137, Composer J20, MPS M29 G135, fleet-monitor. No NexusAI seat is live; M14 and G134 are gone. The B727 records seat (R47, stamped 10:28) may launch beside the gate; its kit says records only and ports 9720-9729. `worktrees/b714-merge`, `b714-mut` and `session-tools/b714` exist and are not the new gate's.
- Lock tool sha256 `cf01bafb...` equal to B714's; `queue-jest/` empty; load1 14.68 at 10:42 (high). Model: `claude-sonnet-5-5` (`checked_at_local` 2026-10-26 10:23:06); G2 at `model-routing.md:109` (read). node on this machine v26.8.1.

## D-decisions
- D1: copy B714's shape but shrink the work to a one-line change: no 53-row attribution table; the heart is a plant matrix (P0-P6) and three small mutants (host `0.0.0.0`, `::1`, identity).
- D2: the plant is a preload that rewrites only the PORT of `listen(0)` calls. Reason: the stand picks its own ephemeral port, so a squatter cannot be aimed at it otherwise; keeping the host argument untouched means the base and head files run exactly as written. Each stand gets a distinct planted port (no port reuse in a process), avoiding the builder's other amplifier (a stale pooled socket on a re-used fixed port, its P2a row).
- D3: foreign process = a separate node process with its pid recorded and its `lsof` line (ADDENDUM-1's proof standard); jest's own pid never counts.
- D4: a 127.0.0.1-only holder (P6) is a boundary row, graded Note: it bounds the header sentence "the request reaches it even when the port is held elsewhere" (a specific-address holder should make the head's bind itself fail).
- D5: no local full verify (22-23 min over the 20-minute bound); the PR's `Build` run on the merge ref is the instrument. The builder's "verify PASS 5102/306" was on the BASE tree; the merged tree should read 5155/306 (main's counts file), so the kit writes 5155/306 as the predicate and calls out the PR body's wording.
- D6: CI and CodeQL read once at Step 0 (pin) and once at the verdict, no polling loop, per the commission; pending = GO WITH FINDINGS at most.
- D7: round count: new PR, zero earlier NO GO rounds; B714's round 1 is a different PR and class, so it is not carried (stated in the kit).
- D8: class name chosen as above; Tuesday may rename.

## Q-questions for Tuesday (each with a default)
- Q-1: class wording for round counting. Default: "a test-only fix whose stated mechanism or effect its evidence does not discriminate".
- Q-2: local full verify? Default: not run; Build run 40245881901 on the merge ref is the instrument; if Build is not complete at the verdict read, GO WITH FINDINGS at most.
- Q-3: wait for `build` and the Analyze runs, or read once? Default: read once at the verdict (as commissioned); the kit's hard stop is 2h30 after Step 0, and Tuesday can re-read CI at landing time (a pending read caps the verdict at GO WITH FINDINGS, the head-pinned landing then waits for CodeQL anyway).
- Q-4: the gate opens a squatter on 0.0.0.0 in 9880-9889 and a preload on jest; a macOS firewall prompt may appear. Default: YES to the probes (loopback ports in the block only); the kit says do not click a dialog and STOP if one blocks.
- Q-5: port block 9880-9889. Default: use it; move it if another brief took it first.
- Q-6: Jira GET of RD-867 (Check 6 sentence 1) through the project's own read helper. Default: YES if a helper is found in five minutes, else NOT TESTED (low value).

## Findings from reading the builder (for Tuesday; the gate re-measures)
- The header says the foreign port "failed twice, in two separate processes"; the builder STATUS (Step 5) says the same port 59869 failed three times in three separate jest processes, plus three more on it in the interleaved arm. Kit grades it a Minor/Note (a count in a comment).
- The header and commit say "168 collisions in 220000 wildcard stands"; the STATUS rows read 160 collisions in 100000 wildcard stands (first probe) and loopback 0 of 220000. The 168 figure is not in the STATUS. Kit marks it UNMEASURED (Note).
- The PR body "Full verify at the head ... 5102 ... equal to the counts file" is true on the base tree only; main's counts file now reads 5155/306.
- The header's "even when the port is held elsewhere" is measured only for a wildcard holder in the STATUS; P6 tests the other holder.
- Boundary of the whole claim: the mechanism is Mac-shaped (builder's FINDINGS 1: Logitech helper daemons); Linux CI is UNMEASURED.

## UNMEASURED
- Whether the gate's plant bites base on this machine (that is Check 2, with P2 as the control); the builder's 4-in-18000 and 7-in-38400 figures; the 168-in-220000 figure; the keep-alive and CPU rows; Linux/node 24; the Build and Analyze results (in progress at 10:4x); `blob c00b8d8a` of main's file (RELAYED, not hashed by me); the `Deploy demo` paths-ignore text (RELAYED from B714; the kit tells the gate to read it at main).

## Outside-the-fences disclosure
- None. Read-only: `ls-remote`, `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (pulls, files, compare, check-runs, actions runs, analyses, rules, git/commits, contents raw piped to grep, deploy-demo runs), `lsof`, `tmux list-panes`, `shasum`, `node --version`, file reads, local greps. One shell command listed the NexusAI `worktrees/` directory (read, to check `b728*` absent; it printed far more than needed). I read B713's STATUS, Tuesday's ADDENDUM-1, the B714 kit/report/STATUS first line and last line, and the R47 kit's first lines for ports/panes. No clone, fetch, npm, jest, Jira, az, ssh, docker, hosted host; never ran `decision_queue.sh`; never read the forbidden stores. Two advisory hook notes about case-sensitive grep appeared (not blocked; my counts that mattered were paired with controls or re-run with `-i`). Only the two named files were written.
