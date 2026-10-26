STARTABLE: YES

# B802 drafter report - NexusAI PR #127 gate kit (tier 2, G169)

Drafted 2026-10-27 09:59-10:05 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B802_SEAT-G169_nexusai-127-odd-limit-rows-gate-tier2.md` (74 lines, 55794 bytes).

## BLUF
Startable now, from the stamp, at load1 below 7 (10:00 read 8.92 8.31 7.60, so launch_when_cool). Shape copied from the B793 kit. Differences from B793 that the kit carries: (1) the merge ref is fresh (made on current main), so the gate makes the REAL merge in its clone and verifies on that tree; (2) the fetch uses three refspecs into `refs/remotes/g169/` (the B793-5 refspec collision) and reads rc plus `cat-file -t` before any repeat; (3) the Build job log `HEAD is now at ... Merge <head> into <main>` is read in Check 7; (4) the mutants are the four per-input ones plus ML (no -5 row), M1 and M4, run on BASE and HEAD files.

## Facts re-measured (instrument, control)
- Refs 09:59:49 (`git ls-remote`): main `b96b1da7`; branch and `refs/pull/127/head` `b952d7ff`; `refs/pull/127/merge` `6baddcef` (parents `b96b1da7`, `b952d7ff`, tree `ee01ea641253`). `refs/heads/b802*`, `b799*`: none (control: `b798*` prints 1 line).
- PR #127 (`gh api -X GET pulls/127`): open, not draft, base `b96b1da7`, 1 commit, +9 -1, 1 file, blob `f76995331268` (main `86262442ca76`), `mergeable_state` blocked. Open PRs: #127 only. Compare main...head: ahead 1, behind 2, diverged, merge base `ce8c33a6`. `ce8c33a6...b96b1da7`: HISTORY.md only (control compare lists 7 files).
- Diff read whole: 4 comment lines + 4 keys + 1 modified toEqual line = +9 -1. Matches the builder.
- Counts blob `9712206a584f` at main and head, 5170 / 307 raw (control: bad sha answers 404). simpleDb.js blob `0d07e81a927b`; build.yml blob `e4e5c095263f`.
- Checks 10:00: Build in_progress; Analyze javascript-typescript in_progress; actions and python success; 2 analyses, 0 results; open alerts 0 (a suspect zero until the third completes).
- Ports 8890-8899: lsof rc 1, python bind control on 8895 listed then freed. Word-boundary scan of 97 non-`.pre-` SEAT kits: 0 hits in 8890-8899; hits 8880/8881/8889 are B800 and B801 (HPSM-POC). Panes: tuesday, HPSM-POC-H43/H44/G168, MPS-G167, fleet-monitor; no NexusAI seat, G169 free (control MPS-G167 counts 1; G166 found in the B793 kit).
- Lock tool sha256 equal to B793's; queue-jest empty. Model `claude-sonnet-5-5` (models_latest.json line 23); G2 at model-routing.md:109, G-cap :111.
- Round count: first lines of the 7 `GATE VERDICT` STATUS files of 10-26/27 contain no NO GO (control: B793 line prints). Three older STATUS files carry NO GO in the first line (B592, B647, B667), classes unread; the kit tells the gate to read them and stop at round 2 if one names this class.
- Unstamped kit: 8 lines with the four-underscore pattern (control: a planted line reads 1), 0 `@X@` tokens, 0 non-ASCII bytes.

## D-decisions
- D1 The gate verifies on the merge tree (`worktrees/b802-merge`), not the head tree: CI checks out the merge, and a fresh merge ref exists this time. The head tree differs from it by HISTORY.md only.
- D2 M1 (`|| 101`) is run as a recorded shared-arm mutant. My prediction: BASE red at 3 keys (the sibling PR's), HEAD red at 6 keys, `limitAt2Point9` stays 2. B793's "BASE green under M1" does NOT carry over to this base.
- D3 MN1 on BASE already throws at the NaN row, so it discriminates nothing about the new rows; the kit says so.
- D4 The test-mutant "delete the four rows under MA-MD" equals the BASE-file runs; kept as a stated equality.
- D5 Fetch includes `refs/pull/127/merge` as a third refspec, so the gate compares its own merge tree to GitHub's.

## Q-questions for Tuesday (default in brackets)
- Q-1 Class name on the verdict line: "a pinned row that does not turn red under the defect it names" (round 1 of 2, NO GO 0 of 2). [accept]
- Q-2 Hard stop / wall clock: kit suggests target 2 h, hard stop 3 h after Step 0. [accept; you set the ceiling]
- Q-3 Build is a 34-48 minute job and may still run at the verdict. [GO WITH FINDINGS with "Build PENDING"; you decide whether to wait before landing]
- Q-4 If main moves again to a non-records path before launch the kit's REFUSE stops. [re-stamp S6]

## UNMEASURED
No clone, fetch, npm, jest, probe, CodeQL, workflow ran. The predicted M1 / ML / M4 matrices are the drafter's arithmetic from the clamp expression and the builder's measured MA-MD figures. The Build job log endpoint's availability while a job runs. B592, B647, B667 classes.

## Outside the fences
None. Only GitHub GETs under the NexusAI `GH_CONFIG_DIR`, `ls-remote`, lsof (one local python bind control on 127.0.0.1:8895, freed), tmux list, shasum, a python scan, file reads. No decision-queue use, no Jira, no ledger/scoreboard/staged-brief reads, no HTTP to any hosted host. One hook advisory (case-sensitive grep of CLARIFICATIONS; hits were found, so no false zero).
