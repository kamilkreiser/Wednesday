# DRAFTER REPORT: Seat F 6th launch brief (KS-808, F-C), 2026-10-08

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatF6_raise_ks808.md` (483 lines, 78,740 B, sha256/16 `f4690591d2a5a273` at 08:49Z). It is staged, NOT sent, NOT launched.

**Placeholders:** there are no placeholder tokens. The SEND AMENDMENT is an empty section that says Wednesday writes it at send. By `grep` for angle-bracket tokens, the only ones left are `<h2>` (literal HTML) and the five inside the verbatim PARALLEL-SEAT block (`:313-318`). That block is `cmp`-identical to `0_Brain/learnings/2026-09-09_parallel-seats-on-one-project-grant.md:86-91`.

**Where I wrote:** nothing under `!CODING/`. Write verbs (`apply --cached`, `read-tree`, `write-tree`) ran only in my own `git clone --shared --no-checkout` at `scratchpad/f6/clone`, with a temp `GIT_INDEX_FILE`. The red/green ran on blobs extracted into `scratchpad/f6/run/`. The lock `find` control was planted in a `mktemp -d` in the scratchpad, never in the shared `worktrees/`. Linear was read-only: the key was sourced transiently from the project `.env` into one shell, never copied, never in argv. No mail, no tap, no launch, no GitHub or Linear write.

## BLUF
1. **The payload is still good.** At develop `0a6177ea5482` (unmoved, read at 08:29Z and 08:39Z) the KS-808 payload (6,445 B, `d47753aa37f9641c`) applies strictly: forward rc 0, reverse rc 1, re-apply control rc 1. The tree is `d9b1a2ab31fe`, as F 5th recorded. Flow `41.` is free at develop and on all seven PR heads (#1383, #1427-#1432).
2. **`STANDING_LINES:109-111` is stale.** It says `run-migrations.sh` exits 0 when migrations fail. At develop, `:190` is `exit 3`, under KS 1031 (#1183, 2026-09-22). F 5th's brief and handover both tell the seat to "name that in the body", which would put a false claim in a client-visible PR body. The brief overrides this (Q-EXIT808). **Your STANDING_LINES needs the correction; I did not edit it.**
3. **F 5th's push logs name the skipped legs.** Both logs print `legs 3 4 8 — local stack not up` on the line straight after `PREFLIGHT INCOMPLETE`. So "3 SKIPPED, unnamed by this push's output" is false. It sits in F 5th's READY and handover, in the #1430 and #1431 bodies as F 5th described them, and in your 07:51:23Z and 07:56:34Z ANSWERs. Whether to correct the two open PR bodies is your call; the brief keeps F 6th out of it.
4. **`commitf5.sh:85` is missing from the handover's first three things.** It still carries the seat gate `*" f5")`, the same gate F 5th listed and then missed. The brief makes the re-key explicit.
5. **The matcher and trap4 need more than the handover lists:**
   - `e 12th`, `r 20th` (gate76's default merge seat) and `g 6th` are ABSENT from `OTHER_SEATS`.
   - trap4 has no arm making F 5th's real ANSWERs read foreign, including the 07:31:21Z push authorisation. The brief lists six real subjects with their timestamps.
6. **A READY exists for this payload** (`b3346ef479655371`). It says "Tier: AT LEAST tier 2", while F 5th's brief said TIER 1 plus your read (Q-TIER808). Its "raise blocked until leg 14 green" line is superseded by F 5th's two clean pushes at this same develop.
7. **Usage gauge is 95%** (bare rc 3; with `WED_USAGE_STOP=100`, rc 0; 08:36:35Z). It went 86% -> 92% -> 95% across today's three drafts. One raise fits only if the gauge holds.

## Open questions for Wednesday (recommendation / default)
- **Q-EXIT808:** what does the body say about the exit code? Rec: state the measured `exit 3` at `:190` and that defect (1) was closed under KS 1031; never write "exits 0". Default: as recommended. Separately, you correct STANDING_LINES `:109-111`.
- **Q-TIER808:** which tier goes in the READY? Rec: TIER 2, with your Q-READ808 read recorded; the gate decides upward. Default: TIER 2.
- **Q-5D808:** SKILL §5d wants a WHY comment on every changed line, and payload lines `:121` and `:146` have none. The #1422 follow-up shows a gate asks for these. Rec: add two comment-only lines, shown in the Q-READ808 diff; this deviates from the held bytes. Default if unruled at the plan ANSWER: raise byte-for-byte, name the gap, and ask in Q-READ808.
- **Q-READ808-SHAPE:** should the Q-READ808 mail double as the pre-push ctx QUESTION, with your ANSWER carrying both? Rec/default: yes.
- **Q-PROSE808:** what happens to the prose that describes the pre-fix summary line? There are 7 sites: the REVIEW's 3 runbook lines, plus repo `CLAUDE.md:21`, SKILL `:351` and `systemTest/CLAUDE.md:232` and `:779`. Rec/default: name them all and edit none; a follow-up is your call.
- **Q-BRANCH-F6:** rec/default `feature/ks-808-run-migrations-counts-skips-apart-f6-1` (53 characters).
- **Q-SUBJ808:** rec/default commit `fix(KS-808): run-migrations.sh no longer counts skipped migrations as applied` (77 characters, under the tool's 84) and PR title `KS 808: …` (72), the shape of #1431.
- **Q-F6TOOLS:** rec/default: copy F 5th's 13 tools, keep the filenames, re-key per ITEM 0.4, and borrow no other lane's kit.
- **Q-LOCK56-F6:** rec/default: leave `.push-lock-56` in the WAIT set. It waits on a lock nobody takes; the seat says so in its plan mail. Reshaping it mid-round is the risk you declined at 07:51Z.
- **Q-OBJ-F6:** rec/default: a recorded no-op, since develop's objects are present (both controls).
- **Correction you owe, outside F 6th's queue:** whether #1430 and #1431's "unnamed" leg sentence is fixed (BLUF 3).
- **Correction you owe, outside F 6th's queue:** STANDING_LINES `:109-111` (BLUF 2).

## What I verified, and how (times UTC, 2026-10-08)
- **Sources, read whole:** the F 5th handover (160 lines, `c3b79f6e2352acff`, equal to the WRAP); the F 5th brief; the G 5th brief (295 lines) and its DRAFTER_REPORT; all ten F 5th mails and all six of your ANSWERs to F 5th; STANDING_LINES (443 lines, `09cef6999b8ae40b`); the KS-808 REVIEW, `checker.out`, red/green outputs, `round.json` and READY; gate76 `RULINGS_wednesday.md:3-24`.
- **Refs:** `env -u GIT_SSH_COMMAND git ls-remote git@github.com:Secuura/Distributed_Secuura.git`, rc 0, at 08:29:22Z (2,147 lines) and 08:39:30Z (2,150 lines).
  - develop is unmoved. #1432 appeared between the two reads (R 19th, KS-1410, `c4e6f50654fa`).
  - Namespace counts with controls: `-ra13-` 2, `-zzNOTREAL-` 0.
  - `ks-808` branches: 0.
- **Shared store, read verbs only:** `rev-parse --all` 1,644 lines, `241bcbfbd21dc49a`, unchanged by my `clone --shared`. `cat-file -e` with positive and negative controls. `core.filemode` reads false. HEAD, local develop and `origin/develop` all read `ddea005553bf`.
- **Floor:** `tmux list-panes -a` at 08:29:34Z and 08:39:36Z shows `%0`, `%1`, `%99` R, `%100` G and `%101` gate76.
  - **`%97` (E 11th) was already gone at 08:29Z**, though your 19:2x read had it wrapping.
  - Locks: `.push-lock-d8` was held by `Secuura/Blockchain-R ra19` from 08:24:09Z and released by 08:39:36Z. The `mktemp -d` control read 1.
  - `df -m`: 386,781 MB available.
- **Payload:** checked with `wc -c` + `shasum`. In my scratch clone with a temp index: strict apply, reverse check, re-apply control, `write-tree`, `ls-tree` modes, both numstats (patch +8/-3, tree +6/-1) and `--summary`.
- **Red/green:** `/bin/bash` 3.2.57 on extracted blobs.
  - New suite: base `3 passed, 2 failed`, rc 1; after `5 passed, 0 failed`, rc 0.
  - KS 1031 sibling: 7/0 on both sides.
  - `sh -n` and `bash -n`: rc 0.
- **Develop reads** (`git show` + `sed -n` / `grep`):
  - `run-migrations.sh`: whole file, 194 lines.
  - `run-shell-suites.sh`: `:48-51`, `:65`, `:99`, `:360`, and no `-x` test.
  - Mode census of `__tests__/`: 38 x 100644 and 15 x 100755.
  - 71 tracked suites, all inside the runner's ROOTS.
  - `run_shell_suites.test.sh`: its cells are fixture-tree cells, so it should not count the new suite.
  - `preflight.sh` legs 9 and 10.
  - Consumers of the summary line, by `git grep`.
  - Spark tip vs develop: 77 commits, and 0 drift on the three migration files.
- **F 5th's two push logs:** the legs line, the SKIP lines and the leg 10/12/14 lines; both `.rc` files read 0.
- **Tools:** 13 of 13 hashes match the handover. Read whole: `commitf5.sh` and `pathgatef3.py`. Read in part: `trap4_f3.py:40-174`, plus the knob regions of `pushf3.sh`, `lockf3.sh`, `twolockf3.sh` and `restraisef5.py`. I swept lane tokens over the non-comment lines of all 13. The matcher was parsed with `ast` (`MINE :139`, 124 entries in `OTHER_SEATS`, `tag` at `:331-403`).
  - **Finding:** the handover's `.pre-*` claim fails for 4 edited tools (`inbox_matchf3.py`, `inbox_watchf3.sh`, `twolockf3.sh`, `restraisef5.py`). Their originals are still at known hashes in F 4th's and E 10th's folders.
- **F 5th's real Wednesday subjects and timestamps:** from its record files `answer_*.json`, `addendum_lock.json` and `inbox_tail.txt`.
- **Overlap:** `diff --name-only` from each head's merge-base, across 7 PR heads. 0 touch F-C's files. The doc paths are the positive control. Newly added suites: 0 on every head except #1383 (1, the positive control).
- **Doc tails:** my newline-tolerant `tails.py`, run at develop and at 6 PR heads plus R 19th's local KS-1410 head (since #1432). Its controls are copied from each document's own last `<h2>`, and both controls read; the same-line reader misses the flow control. Develop reads 30 flow numbers and 19 cheat sections, tail `26` / `KS-1164`.
- **Linear** (read-only GraphQL by id, `comments(first:50)` sorted client-side, KS-99999 control in its own query returns "Entity not found"):
  - KS-808 at 08:34:14Z: In Progress, P3, board account; 4 comments, newest 2026-09-25T07:37; 1 attachment (#1229); last state change 2026-09-25.
  - 17 other keys at 08:34:57Z. KS-1410 shows the new #1432 attachment at 08:32Z.
- **Project MUSTs at develop:** SKILL blob `b59b74a592e9`, equal to the on-disk SKILL (`4f7491fca5d514d5`), §3 traps, §4, §5b-§5f. Repo `CLAUDE.md` `:19-22`, `:167-175`, `:209-212`, `:255-256`, `:285`, `:296`. `systemTest/CLAUDE.md` `:838`, `:909`. `pre-push` `:46-50`. Project `CLAUDE.md:185-187` on disk.
- **Usage:** `usage_gate.sh --check`, bare and with `WED_USAGE_STOP=100`, at 08:36:35Z.

## What I could not measure (and why; the instrument that closes it)
- **Whether any other open PR touches `run-migrations.sh`:** I had no GitHub API token. Closed by the seat's first API read (open PRs, paginated, then each PR's files). I checked 7 heads by `ls-remote` objects only.
- **`mergeable_state`, reviews and Actions on #1427-#1432:** also needs the API. Same instrument.
- **`ks1054_deploy_scripts_read_startup_migrations` at develop:** an extracted blob is not enough of the tree to run it. It is byte-identical to the Spark tip, where the REVIEW read 40/40. Closed by the seat's sibling run.
- **`ks949_main_seed_idempotence`:** needs Postgres and a built shared package. Closed by leg 14 of the seat's push.
- **A real worktree red/green, S-1 and the push gates:** these belong to the seat. Mine are expectations only.
- **The runner under the `migrations` container's own `/bin/sh` against a real database:** the owed live run; nobody in this seat runs it.
- **F 6th's pane id; E 12th's token and launch; R 20th's launch; whether gate76 merges before F 6th's RAISE_BASE:** future events. Closed by your SEND AMENDMENT and the seat's ITEM 0.
- **The exact subjects of your 07:51:23Z, 07:56:34Z and 08:08:03Z ANSWERs:** I have their bodies from staged files, but not their AgentMail timestamps from source. The times come from the F 5th handover. I did not read the inbox API.

## Departures from the predecessor shape, with reasons
- **ITEM 0 opens with the handover's FIRST THREE THINGS as 0.1-0.3**, as commissioned, then TOOL RE-KEYS (0.4), then measurements (0.5).
- **A dedicated Q-READ808 section** sits between QUEUE F and the PR BODY, because it is the round's one hold point.
- **The requested section `RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE`** lists your 15 F-lane rulings by timestamp, then the project-wide carried rulings. One of them is flagged as resting on a false premise (BLUF 3).
- **I did not carry the "RULED BY KAM, NOT YET IN AN ARTEFACT" card list.** You generate it at send with `decision_queue.sh`, as with G 5th.
- **The partition marks each pane id by source:** your 19:2x read or my 08:29Z and 08:39Z reads. E 11th's `%97` disagrees between the two.
