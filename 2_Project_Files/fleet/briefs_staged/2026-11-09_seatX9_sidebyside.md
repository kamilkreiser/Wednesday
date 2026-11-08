
# BRIEF: Seat X 9th, Secuura/Blockchain-X. Successor to Seat X 8th. The SIDE-BY-SIDE on ONE real commit, then (only on Wednesday's separate GO) ONE real new-branch push. No tool changes.

## BLUF

Gate 263 (tier 1, round 3) returned GO WITH NOTES on X 8th's pre-run push driver. It covers 14 first-use files by sha256; a change to any one voids it. Kam's card `secuura-prerun-push-third-round-1106` = a: "One narrow third round (recommended)"; detail, verbatim: "One seat fixes the blocker and the Majors only, one tier 1 gate on the changes, then the side-by-side and one real push. A NO GO ends it for good." The original card `secuura-push-queue-prerun-preflight-1106` = a: "Test side by side, then pre-run if it holds (recommended)"; detail: "Two pre-runs in scratch copies must match a normal run. If they do, at most 3-4 run at once and each PR states --no-verify and which checks ran. If they do not, nothing changes and I report back."

**You build nothing and edit no first-use file.** You run the harness the gate called ready, read its output by hand against the gate's list, and report. Each step ends in a mail and WAITS for Wednesday's ANSWER before the next.

**Steps, in order:**
1. Plan confirmation (QUESTION mail, topic `plan confirmation`).
2. The side-by-side RUN of `sidebyside_x8.py` on ONE real commit. NO push of any kind in this step. Report HOLDS / DOES NOT HOLD with every G5 item (section 2).
3. ONLY on Wednesday's separate GO mail: ONE real new-branch push, origin read back by hand, NO ADOPT.
4. The `STANDING_LINES.md:96` amendment text proposed to Wednesday. Proposed, never applied: the file is hers.

A NO GO result from the side-by-side (DOES NOT HOLD) is a result, not a failure to fix: report it, change nothing, stop. Kam's card says "If they do not, nothing changes and I report back."

**Seat number.** Re-run before your first write: `/usr/bin/grep -c -i -E '^## .*Seat X 9'` over `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` gave 0 and the control `'^## .*Seat X 8'` gave 1 on 2026-11-09. If the 9 count is not 0, stop and QUESTION.

**Model.** model: claude-opus-5-5 -- Wednesday's call: this tool decides when a push skips the hook (`--no-verify`), a security-guard surface; the step-3 push is a real `--no-verify`. Your model was set at launch; this brief instructs no change.

## 0. FIRST: read, then measure (before any step)

1. Read X 8th's HANDOVER, FINAL block on top: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatX-8th/HANDOVER.md` (56 lines). Then `drafts/driver_built_x8_body.md` (the 14 first-use files with shas, the OPEN list, NOT TESTED) and `drafts/standing_lines_proposal_x8.md` (step 4's base).
2. Read the gate verdict WHOLE: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate263-tier1-x8-prerun-driver-r3/verdict.md` (180 lines). Where this brief summarises it, the verdict wins.
3. Check and report in the plan confirmation: (a) re-hash the 14 first-use files in X 8th's `tools/` against the shas in the body (exact paths; a flipped-digit control that must fail; X 8th's own `evidence/final_shas.txt` has all 41); (b) your own worktree state: you hold none in the shared repo; the shared checkout `2_Project_Files` status is not yours to clean; (c) origin develop NOW: the drafter read `01b26bc772a713e5e4d6ffc545f7fedeeeb4afe3` at 2026-11-09 ~01:3x, NOT the a65ae7ed that the pins were measured at; (d) does `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/prerun/` exist yet (the drafter found it did NOT); (e) `push_queue.sh list`; (f) any launcher warning VERBATIM.
4. **The hook, cells and legs pins were measured at develop a65ae7ed** (hook 74e8d270, 82 cells plus blob 2c03e3dc, 16 legs). Develop has moved 90+ commits since (B 98th and B 100th/101st merges). If `prerun_x8.py run` REFUSES FAST on a stale pin (that is N5 working), **do not edit a pin**: pin files are first-use files and an edit voids gate 263. Report the refusal line verbatim in a QUESTION; Wednesday decides (a new gate on a pin edit is hers to commission).
5. **The leaked drivers (your standing chore, with a measured surprise).** X 8th left scratch `pushlock_x8_newbranch_v3.sh` drivers running: pids 18293 and 40147 (as commissioned), and a THIRD, pid 42744, world `/private/tmp/x6t/x8/w2d7kz7wu`, that the commission did not name. All three have ppid 1 (drafter's `ps`, 2026-11-09). Commissioned test: `lsof -a -p <pid> -d cwd` must show X 8th's scratch world under `/private/tmp/x6t/x8/`. **The drafter ran it and the cwd of 18293 and 40147 was `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (the project root), NOT the scratch world.** Their argv names scratch paths (`/private/tmp/x6t/x8/wjbebbmre/...`, `.../wp6i2lhqg/...`). Your commission says: if a cwd is anything else, STOP and QUESTION. So: re-run the lsof on all three, record before (ps + lsof), and if a cwd is not under `/private/tmp/x6t/x8/`, **stop the chore and QUESTION** with the lsof lines, the full argv (`ps -o command=`), the world dirs' existence, and whether the argv's worktree and queue paths are all under scratch. Do not stop any pid on argv alone unless Wednesday's ANSWER says so. If every cwd is scratch (the drafter's reading was a snapshot, re-measure), stop each by pid with a plain `kill <pid>` (never by name, never `-9` first), then report after (`ps -p`). Pid 42744 is not commissioned: measure it the same way and QUESTION; do not stop it without an ANSWER naming it.

## 1. STEP 2 DETAIL: the side-by-side run

**What it is.** `sidebyside_x8.py --sha SHA --worktree-a WT_A --worktree-b WT_B --second-worktree WT_C --out OUTDIR` runs `prerun_x8.py run` (the real tool, not stubbed; about 20 minutes each) in WT_A and WT_C at the same time, then the REAL hook once in WT_B directly (no push, no network), and compares. HOLDS only if every row of every pre-run is true. (Source: `tools/sidebyside_x8.py` docstring, lines 1-26.)

**Which commit.** You propose it in the plan; Wednesday confirms. Constraints, all from the harness: the sha must be an UNPUSHED commit on a NAMED local branch that changes `Blockchain/Dev`; a sha already on the remote is refused (`sidebyside_x8.py:122`, `for-each-ref --contains` over `refs/remotes/origin/`), and the hook skips an already-pushed commit so there would be no preflight to compare. Wednesday's reading: take a test-only or docs-only change from an OPEN PR's head and re-create it as a NEW local commit on current develop, in your own scratch clone (a fresh `git clone` under `/private/tmp/x6t/x9/`, or a `git worktree` of one), on a branch name that does not exist on origin. A PR head itself is on the remote, so it cannot be the sha; the new commit has a different sha. If you see a way the constraints and this reading collide, QUESTION it. The three checkouts (WT_A, WT_B, WT_C) are different trees, clean, on that sha and branch.

**Setup facts from the gate (Q6), binding:** run from the `fleet/prerun/` copy, re-hashed after copying so the slot base matches (the copy is Wednesday's job after a GO; if it is absent, QUESTION, do not make it); on the unpushed branch commit; with `TMPDIR=/private/tmp/prt` set for the harness process only. Launch from Python, not a bare `&`; the run ends in a tracked background process that EXITS when done, and you wake on its exit, not by "monitoring". One suite at a time: do not run beside another heavy job (the load gate is bypassed, see G5 below, so YOU judge load: read `uptime` before and after and report both).

**READ-ONLY on everything real:** origin, other worktrees, the queue, the lock. The pre-runs use only the pre-run slot folder beside the tool. NO `git push`, NO `gh pr`, NO queue join, NO driver launch, no ADOPT, no `rehearse_push_x8_nb.sh` (reaches real gates and `gh`; never run).

**Your report (STATUS-with-a-result mail, body = path to a file in your record folder) must show, copied from the real output, ALL of these (gate 263 Q6, verbatim list):**
- `HOLDS` and exit 0.
- `2 pre-run(s)`, run with `--second-worktree`.
- For each pre-run, all eight rows `true`.
- `tree read N times (min 15)` with N >= 15 and the default `--min-tree-reads` (never lowered).
- Moved 0.
- Headers `16 hook 16 of 16`.
- Decide rc 0.
- At most 2 known lines, each read.
- 0 unknown, with any same-text pairs read.
- In `sidebyside.json`, the two pre-runs' `started_utc`/`finished_utc` overlapping.

## 2. G5, BINDING: the harness's limits, each checked BY HAND in your report

Gate 263 G5 says (verbatim): "HOLDS does not check that the two pre-runs overlapped in time, or that `--min-tree-reads` was left at its default. Both are visible in `sidebyside.json` (`started_utc`/`finished_utc`, `min_tree_reads`), so read them there. The hook runs after both pre-runs, not beside them. The pre-runs are launched with `--max-load 1000`, which bypasses the load gate. The VOLATILE normalisation was measured only against fixtures. A real-output token it misses (for example an `HH:MM:SS` time) gives a false DOES NOT HOLD. That is the safe direction, but it costs a real run. Same-text pairing is a multiset match: it ignores line order. That is enough given the rc, legs and verdict rows, but it is order-blind."

Your report has one line per limit, each with the evidence you read:
1. Overlap: the two `started_utc`/`finished_utc` pairs from `sidebyside.json`, and the overlap computed in seconds.
2. `min_tree_reads` from `sidebyside.json` equals 15 (the default).
3. The hook ran after both pre-runs (read the times); say plainly that this means the run did NOT test the hook and a pre-run in the same moment.
4. Load bypassed: `uptime` load1 before, during (at least one mid-run read), after.
5. VOLATILE: if DOES NOT HOLD, list every unknown pair and say for each whether it is a missed volatile token (a time, a pid, a path) or a real difference. A false DOES NOT HOLD from a missed token is REPORTED AS THAT and you do NOT edit the tool and rerun; QUESTION. If HOLDS, say so and note the normalisation was exercised on real output once.
6. Order-blind pairing: list the same-text pairs, if any, and read their order in both outputs.

Also record (do not fix): the other gate notes. **G1** (the REAL hook skips the preflight when `git diff` fails, e.g. a `diff.orderFile` pointing at a missing file; at 35bcfa000 it pushed a RED commit with rc 0; not X 9th's to fix: put it in your record and your wrap; Wednesday routes a High ticket; you write no ticket). **G2** (`hook_changed_set_COPY` is fail-safe only weakly; live if a systemTest package gains `format:check`), **G3** ("clean" means clean to `git status`, on both paths), **G6** (ADOPT reachable as a mode via the launcher's 10th argument; you use no 10th argument), **G7** (`qualify` sets no minimum on `tree_reads`): carry each into the use note you hand Wednesday. **G4** is fine (the gate's own arms cover it).

## 3. STEP 3 (ONLY on Wednesday's separate GO): one real new-branch push

Not before her mail names the branch, the sha and the time. The shape is hers; the brief asks: new branch only; launched by `launch_driver_x8.py` from the `fleet/prerun/` copy; a fresh pre-run record for that exact sha; origin read back BY HAND after (`git ls-remote origin refs/heads/<branch>` equals the pushed sha, run in a separate call from the mail citing it); the PR line states `--no-verify` and which checks ran; no ADOPT. A real push is the signature class of production-adjacent irreversible; Wednesday's GO must say Kam's word covers it (card `secuura-prerun-push-third-round-1106` = a says "one real push"; card `secuura-wednesday-go-counts-as-kams-word-1030` = a). If the pre-run falls back to the hook, that is the tool working: report it, push through the hook as normal.

## 4. STEP 4: STANDING_LINES.md:96 amendment

Base your text on `drafts/standing_lines_proposal_x8.md` in X 8th's record, with the gate number 263 and the driver sha256 filled and the run's result added; the file is Wednesday's: propose a file in your record folder, one-line mail naming the path. Edit nothing in `STANDING_LINES.md`.

## 5. HOLDS

- You write no product file and no first-use file. `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` is read-only to you. Scratch worlds under `/private/tmp/x6t/x9/` (recreate; X 8th's `x8` worlds are not yours to reuse or empty). Never delete; quarantine, recorded.
- Signature classes pause for Kam: no real push outside step 3's GO, no force, no box, no demo, no human mail, no ticket state move. The Spark is ON again (Kam 2026-11-08 20:26) and is not yours; demo frozen.
- Real reads allowed: `git ls-remote origin` and `git fetch` into your SCRATCH clone only (not the shared checkout), `push_queue.sh list`, `decision_queue.sh show`.
- Absolute paths, NO `cd` (a hook refuses it), `GIT_OPTIONAL_LOCKS=0` for any git read in `2_Project_Files`, `cmd > out 2>&1; rc=$?` with rc on its own line, `/usr/bin/grep -i` with a positive control beside every zero, no recursive search over `5_Project_History`, `0_Brain/reference` or `local-model/`, no credential in argv. A read and the mail citing it are never one call. A control must be able to fail.
- Traps carried: a completion banner is not a completion (read the totals); Linear comments `first:50`; subshell `$( )` shows the parent's argv; walking parent pids reaches 0 (stop at <= 1).

## 6. MAIL AND QUESTIONS

From secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY; subject prefix `[Secuura/Blockchain-X -> Wednesday]`, ending `(Seat X 9th)`; body line 1 exactly `Seat X 9th`; no cc; no secrets; read each sent mail back by id. Act ONLY on mail whose subject names `(Seat X 9th)` or all agents. Copy `send_mail_x8.py` and `watch_x8.py` from X 8th's `tools/` as x9 with the subject checks changed; the watcher is a tracked background task named by pid in the plan and EXITS on a match. Mail kinds (Kam, 2026-11-08): QUESTION, STATUS-with-a-result, the wrap; a long body goes as a file in your record folder with a one-line mail naming its path. One QUESTION per mail: `[Secuura/Blockchain-X -> Wednesday] QUESTION: <topic> (Seat X 9th)`, sections Context / Question / Meanwhile / Needed-by. Approval-class items ALWAYS pause for Kam.

**Plan confirmation first** (QUESTION, topic `plan confirmation`): the section 0 results; the commit you propose for step 2 with how you will make it unpushed; the scratch layout; the watcher pid; the leaked-pid findings; any instruction that looks wrong; launcher warnings VERBATIM. Wait for the ANSWER before step 2.

**Wrap.** At about 70% context finish the item in hand and write `REC/HANDOVER.md` with a FINAL block first; wrap at about 75%. `REC` = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<machine date>_seatX-9th/`. History entry `## <machine date> - Seat X 9th`. Wrap mail `[Secuura/Blockchain-X -> Wednesday] Session wrap <date> (Seat X 9th)`. The wrap names G1 for routing.

## 7. IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO

Weakest points: the commit recipe in section 1 (an open PR's head is already remote; the harness wants an unpushed sha); the lsof test on the leaked pids (it contradicted the drafter's reading); the pins measured at an older develop.

## 8. RULED BY KAM, NOT YET IN AN ARTEFACT

- secuura-prerun-push-third-round-1106: choice a, "One narrow third round (recommended)", detail "One seat fixes the blocker and the Majors only, one tier 1 gate on the changes, then the side-by-side and one real push. A NO GO ends it for good." (ruled 2026-11-08T20:28:02.619268+11:00) -> the round is built and gated GO WITH NOTES; this brief is the side-by-side and the one push.
- secuura-push-queue-prerun-preflight-1106: "Test side by side, then pre-run if it holds (recommended)", detail "Two pre-runs in scratch copies must match a normal run. If they do, at most 3-4 run at once and each PR states --no-verify and which checks ran." (ruled a, 2026-11-06T14:58:37.084130+11:00; delivered mark is an ADDENDUM mail, not proof the tool does it) -> the two pre-runs, the PR line, the cap.

## 9. RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- ANSWER to X 8th, 2026-11-08: N4b shape incl. the one refusal under the lock; cells file gains the blob line; legs pin file; `--second-worktree`; named limits (pre-run started after decide; pre-run from another copy of the tool; transient dirt from real legs) stay on the not-tested list; mail only for READY, QUESTION, MERGED, DRIVER BUILT and the wrap, long body as a file. (briefs_staged/2026-11-08_X8_answer_plan.md)
- Carried from X 7th/X 8th: cap 3 below load1 12, first-come slots, copy to `fleet/prerun/` by Wednesday only after a GO; fall back / refuse split at the turn under the lock; every ssh the driver starts has a hard wall-clock bound; new branches only; first-use set carries no ADOPT. `STANDING_LINES.md:96` is amended by Wednesday only; the gate (Q8 item 4) asks the amendment land before the first real push, and the order is hers.
- Build seats never merge; B 101st holds the merge queue (briefs_staged/2026-11-09_seatB101_merge.md). This round has no PR of your own unless step 3 opens one; if it does, it goes to the gate like any other.

PROVENANCE:
- Gate 263 verdict is GO WITH NOTES; covers 14 first-use files, pushlock_x8_newbranch_v3.sh sha256 cc29e44bd3823b22ef98a0d593feb2a734be784dfa39fe3e978735e435df64d6; notes G1 to G7; Q6 list | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate263-tier1-x8-prerun-driver-r3/verdict.md lines 1-180, Read tool | read 2026-11-09
- Card secuura-prerun-push-third-round-1106 ruled a at 2026-11-08T20:28:02.619268+11:00, label and detail as quoted | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-prerun-push-third-round-1106 | read 2026-11-09
- Card secuura-push-queue-prerun-preflight-1106 ruled a at 2026-11-06T14:58:37.084130+11:00, label and detail as quoted | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-push-queue-prerun-preflight-1106 | read 2026-11-09
- X 8th HANDOVER FINAL: DRIVER BUILT sent 14:04Z, wrap 14:05Z, pass 3 clean, 41 shas, nothing pushed, watcher task blilp37x6 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatX-8th/HANDOVER.md lines 1-56, Read tool | read 2026-11-09
- DRIVER BUILT body: 14 first-use shas, pins hook 74e8d270 / cells 82 plus blob 2c03e3dc / legs 16 measured at a65ae7ed, OPEN and NOT TESTED lists | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatX-8th/drafts/driver_built_x8_body.md lines 1-136, Read tool | read 2026-11-09
- sidebyside_x8.py usage, eight rows, unpushed-sha rule, line 122 remote check, VOLATILE list | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatX-8th/tools/sidebyside_x8.py lines 1-30 and grep line 122-123 | read 2026-11-09
- send_mail_x8.py, watch_x8.py, run_all_x8.py exist in X 8th's tools | ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatX-8th/tools | read 2026-11-09
- Seat ordinal: count of '^## .*Seat X 9' is 0, control '^## .*Seat X 8' is 1 | /usr/bin/grep -c -i -E over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-09
- Origin develop is 01b26bc772a713e5e4d6ffc545f7fedeeeb4afe3 (twice) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop | read 2026-11-09
- fleet/prerun/ does not exist | ls /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/prerun (No such file or directory) | read 2026-11-09
- Pids 18293, 40147, 42744 alive, ppid 1, argv pushlock_x8_newbranch_v3.sh under /private/tmp/x6t/x8/{wjbebbmre,wp6i2lhqg,w2d7kz7wu}; those world dirs exist | ps -o pid,ppid,etime,stat,command and ps -axo over /private/tmp/x6t/x8 (the drafter's reads on this machine), and ls -d of those absolute world dirs | read 2026-11-09
- lsof cwd of pids 18293 and 40147 is /Volumes/DevMASTER/!CODING/Secuura/Blockchain (not scratch); pid 42744's cwd not measured | lsof -a -p 18293 -d cwd and lsof -a -p 40147 -d cwd | read 2026-11-09
- STANDING_LINES.md line 96 begins "No --no-verify, no force pushes, no --admin." | sed -n 96p of /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md | read 2026-11-09
- Wednesday's ANSWER to X 8th (N4b, pins, second worktree, mail-kinds line) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_X8_answer_plan.md lines 1-15, Read tool | read 2026-11-09
- Predecessor brief structure, HOLDS, mail protocol, model row carried | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_seatX8_prerun_round3.md lines 1-101, Read tool | read 2026-11-09
- Drafter common part (reboot, B seats, Spark ON per Kam 11-08 20:26 corrected by Wednesday, demo frozen, signature classes, mail format) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-08_drafter_common.md lines 1-21, Read tool | read 2026-11-09

UNMEASURED by the drafter (you measure these): whether the 14 first-use files in X 8th's tools/ still hash to the body's shas today (not re-hashed); whether the hook, cells and legs pins still hold at develop 01b26bc7 (measured only at a65ae7ed by X 8th); the cwd of pid 42744; whether the cwd of 18293 and 40147 is a snapshot artefact or stable; an eligible open-PR test-only/docs commit (no PR was inspected); whether Wednesday has staged the fleet/prerun copy since this read; Agent Mail daily-cap state; launcher preflight warnings at your boot; machine load; evidence/ files of X 8th and gate 263 were not opened beyond the verdict; no Wednesday mail addressed to lane X after 2026-11-08_X8_answer_plan.md was found by listing briefs_staged (not a proof of none).

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-09 01:31
