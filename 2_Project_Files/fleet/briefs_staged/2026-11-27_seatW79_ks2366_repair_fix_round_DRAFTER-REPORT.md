# DRAFTER-REPORT: Seat W 79th brief (PR 2296 fix round after gate 421), 2026-11-27

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatW79_ks2366_repair_fix_round.md
What I touched: these two files only (each written as a temp file and renamed). No box, no mail, no ticket, no GitHub write. GitHub reads were `gh auth status`, `gh pr view 2296 --json ...`, `gh api .../git/ref/heads/develop` and `gh api .../pulls/2296/files`, as kksecura. Under !CODING I used Read and git read verbs only. (A no-cd hook refused one call of mine that held a `cd`, and another that held `git worktree list` on W 78th's clone; I re-ran both with read verbs only, so nothing was written.) Clock at drafting: `date` 2026-11-27 15:48:08 AEDT.

## COMMISSION FACTS I MEASURED AS WRONG OR OVERSTATED
1. **"Its own new worktree made from the PR head", together with "never edits W 78th's trees", cannot both hold as written.** `s-w78-fix` is a worktree of W 78th's own clone `s-w78-base` (`git rev-parse --git-common-dir` gives `.../s-w78-base/.git`, and its `.git/worktrees` lists `s-w78-a` and `s-w78-fix`). Adding `s-w79-fix` as a worktree there writes into W 78th's `.git`. The brief has the seat make its own clone `s-w79-base`, which needs W 78th's config-write licence again (STAMP W1).
2. **"Quote that method from W 78th's HANDOVER": the HANDOVER does not describe the method.** It says only "Installs were cloned from s-w77-fix (16 of 16 lock blobs equal)" (HANDOVER line 68). The method is in `DECLARED.md` lines 36-41 and `tools/mk_deps_w78.sh` lines 5-6, and the brief quotes those. The tool's donor is hard-coded to `s-w77-fix` (line 8), so the seat's derive has to re-point it to `s-w78-fix`.
3. **"Socket only" contradicts W 78th's kit and licence.** `tools/pg_dev_w78.sh` runs TCP on 127.0.0.1 (lines 3 and 10-14), and its line 12 throws stderr away (`> /dev/null 2>&1`). W 78th's STAMP W4 licensed loopback. Gate 421 was the run that used a socket. The brief has the seat derive the kit to a socket (STAMP W5).
4. **"`manifest.box.db` (and whatever else A4's BEGIN line records)" overstates what the manifest holds.** The manifest's `box` object holds `db`, `user` and `applied_at` (script lines 338-341). The BEGIN line's `now` and `stuck_class` are not in it, and could not be compared anyway. Only `db`, and possibly `user`, can be checked (STAMP W3).
5. **Change 7 misses the script's own header.** The header makes the same false E2 claim as DESIGN.md: "an event that later replaced the payload carries the event's time, outside this window" (script lines 34-36). The brief tells the seat to correct those lines in the script, not only to add the limit sentence.
6. **Change 5 ("block number and network") is narrower than the gate's ask.** The gate asked for `block_number` and `transaction_hash` (verdict line 88; the mock pattern is block 10_500_000 + 47n plus a bare sha256 hash). Your "whatever makes the mock pattern visible" covers this, and the brief names both.
7. **"The gate's 9 surviving mutants" needs one nuance; the names themselves are exact.** 8 of the 9 survived only the builder's suite and were KILLED by the gate's fixtures. Only `blob_network_const` survived both judges (verdict lines 269-270). All nine names match the verdict byte for byte.
8. **"The project's rule file allows a second commit": the rule files say nothing either way.** I read `/Volumes/DevMASTER/!CODING/Secuura/CLAUDE.md` (36 lines) and `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md` (306 lines) whole, plus a grep. They are silent on force pushes, amends, pushing to an existing PR branch and the pre-push hook. "New commit, no amend, no force" is Wednesday's rule, carried from W 78th's brief STOP 5, and the brief says so. The rule that does bind is the merge rule: "TESTED = a QA gate verdict ... at the PR's current head" (Blockchain CLAUDE.md line 237). The new commit therefore needs its own gate, which matches your delta gate.
9. **"W 78th's READY and wrap: `2026-11-27_W78_ready.txt`": that file is the READY only.** No W78 wrap .txt exists in briefs_staged. There are `_W78_answer_wrap.md` and W 78th's HANDOVER/DECLARED, which I read.
10. **W 78th's push kit is for a new branch and does not fit this round.** W 76th recorded that a new-branch pushlock "cannot be inverted by a counted shift" (W 76th HANDOVER line 19). The brief points the seat at W 76th's existing-branch kit (`tools/existing/pushlock_w76_existing.sh`, `launch_driver_w76_existing.py`, `edit_pr_body_w76.py`), with OWN_PR re-keyed 2159 to 2296.

Checked and TRUE:
- head 329fae8c395fc624033def570058bb8b65e6b990, OPEN, 6 files, +964 -0, base develop 4764b2cf (unmoved);
- the 6 files are the "3 paths" (script, suite trio, fragment pair);
- one Major, two Mediums, three Lows (G421-4, -5, -6) and two Notes (G421-7, -8);
- W 78th's 40 mutants;
- the gate's forged-manifest case;
- the literal reverse failing with rc 3;
- the four impossible timestamps;
- G421-4's +6 s fixture;
- the census rows 5a and 5b, plus the missing 8, 9 and 10;
- Kam's card.

## READ BY THE DRAFTER (PROVENANCE in the brief carries each with line numbers)
- PR 2296 state and develop tip: gh as kksecura, `date -u` Fri 27 Nov 2026 04:46:57 UTC.
- Kam's card: `decision_queue.sh show ...-1127`, 04:46:53 UTC. Title; option a "Repair, Kintsugi first" with its detail; `choice='a'  ruled_ts=2026-11-27T13:05:58.078926+11:00`.
- The verdict, read whole; W 78th's brief and its DRAFTER-REPORT; the design ANSWER; READY.
- W 78th's HANDOVER and DECLARED, read whole; DESIGN.md sections 2, 3 and 5.
- The script at the head: header, modes, manifest, reverse.
- mk_deps_w78.sh and pg_dev_w78.sh.
- W 76th's HANDOVER lines on its existing-branch kit.
- Both project rule files.

## NOT MEASURED
- Live seat processes.
- The box container's `sh`.
- Whether s-w78-fix carries the nested `@types/node`.
- The PR body's current text (not read, by rule).
- The hook's current leg list.
- Whether `brief_and_launch.sh` needs a model id line. It holds 0 `model` matches against 13 `brief` matches, so I wrote "set at launch by Wednesday (Opus)" and no id.

## STAMP POINTS (in the brief, W1-W9, with my recommendations)
W1 own clone plus config licence: yes. W2 integrity failure refuses the whole reverse; drift restores the clean rows and exits non-zero. W3 check both db and user. W4 exactly 6 files. W5 socket only, licensed. W6 no local container run, named NOT RUN. W7 merge gated on the PRECONDITION text, not the box proof. W8 dry and apply outputs are box data WHOLE. W9 live seats: Wednesday's to list.
