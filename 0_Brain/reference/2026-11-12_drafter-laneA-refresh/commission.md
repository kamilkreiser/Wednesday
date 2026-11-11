# Drafter commission: BUILD LANE A refresh (Secuura/Blockchain, originate + batch-1 services into the test-type ratchet)
Commissioned 2026-11-12 ~03:1x AEDT by the 03:0x Wednesday rotation-successor seat (Mac mini). Model: claude-sonnet-5-5 (routing v1.0, drafter row; gauge 27%).

## Why
Lane A was drafted 2026-11-11 and HELD by Wednesday at 16:4x for SEQUENCING only ("its blast radius lands on every open originate PR (14) and 43 held test paths at their next push: sequence it after R 96th's raise wave has pushed, then fix A-1..A-5 and stamp"). R 96th's wave has long pushed. The question now is whether launching lane A TODAY would stall the merge pipeline that is clearing the board (B lane merging PRs one at a time; R lane raising held Spark passes), and if not, a stampable brief.

## Read first, whole
1. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_drafter_common.md (the drafter rules; binding).
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-build-lanes/lane_A.md, review.md (its LANE A FINDINGS A-1..A-5 and "Blast radius of lane A"), lanes.md, commission.md.

## Do
1. Re-pin: develop by `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` (GIT_OPTIONAL_LOCKS=0). Every line number lane_A.md cites is re-read at that pin (git show <pin>:<path> | sed -n); a moved line is corrected with its new number.
2. BLAST RADIUS TODAY, measured: (a) which of the 14 originate-test PRs named in review.md line 39 are still OPEN (GitHub PR API or `ls-remote origin 'refs/pull/*/head'` plus the PR files you can read), and every OTHER open PR whose files include originate or batch-1 (billing, kyc, referral, wallet-connector, guardian, queue) tests or product types; (b) held READY files in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/ (names starting READY_, not .pre) whose diff headers touch those test paths; (c) the B lane's current queue (newest briefs_staged/*seatB14*_merge.md and its ADDENDA/GOs) and R lane's rows (newest *seatR10*_raise.md + ANSWERs) that touch them. Name the instrument beside every count.
3. Apply review.md's required changes A-1..A-5 to a NEW brief (do not edit lane_A.md; copy it), carry its provenance table refreshed, and keep the drafter_common standing lines.
4. RECOMMEND, in notes.md, ONE of: LAUNCH NOW (the measured exposure does not block the B/R lanes' next rows, with the reason), LAUNCH AFTER <named PRs merge> (name them), or HOLD (why). State what is unmeasured.

## Constraints
Read-only everywhere outside this folder. In the Secuura checkout: READ git verbs only (ls-remote, show, log, diff, ls-tree, cat-file, grep, merge-base) with GIT_OPTIONAL_LOCKS=0; never fetch, pull, worktree, checkout, reset. No push, PR, Linear write, mail, rm. Never use cd (absolute paths). zsh shell: no PIPESTATUS. Every zero gets a positive control.

## Output (this folder)
brief_laneA.md (the stampable brief, or absent if you recommend HOLD) and notes.md (under 50 lines: the blast-radius table with instruments, the recommendation, the A-1..A-5 disposition, unmeasured items). If Write is refused, return both texts in full.
