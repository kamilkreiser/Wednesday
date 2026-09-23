# Gateset 2026-09-23_gate20T2_seatB — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE TIER-2 batch gate over Seat B 21st's FOUR tier-2 PRs of round 20 — seat PRs 1, 2, 4, 5: **#1202 KS-965 ADMINPWDOC** (doc_patch), **#1203 KS-1019
LEAVEUNTYPED** (comment_patch — proof = token equivalence, a NEW kind), **#1205 KS-1081 NEITHERTEMPLATE** (test_only on a bash suite + script tamper, a
NEW kind), **#1206 KS-1139 ERREXITBEHAVIOUR** (test_only on a bash suite, two tampers flipped separately). Seat PR 3 (#1204 KS-851) is TIER 1 by your
05:12:13Z ANSWER and belongs to the tier-1 gate with PRs 6-10. 4 paths / 4 rows (all M), +30/-2; the TIER-2 SUB-TREE over develop 2bc5ccf63 =
`d13a26e19c8d1b2faf25f9e41cc087fbcd51ec47` — re-derived by REAL merge-tree chains in three orders in a scratch clone FROM ORIGIN (never `--shared` from
the checkout), first PREDICTED with PR 5 built from its canonical before it landed, then MEASURED on the four real heads; == the seat's READY 5 value.
Produced in the shape of `gatesets/2026-09-22_gate19B_seatB/`, re-keyed; round 19's pair / amendment guards replaced by this batch's two new kinds.

**PR 5 status: LANDED during drafting** (READY 5 06:39:32Z, #1206 head `bfbaf4366897a97ec20c2f88e67448597739ce46` == the seat's committed head in
raise/commits.tsv read before the push finished == origin). The set is FULL: the launcher carries four pinned rows. It still refuses to start
without PR 5 — see section 2.

## 0. THE DEVELOP PIN (unmoved; the launcher refuses if it moves)
Origin develop = `2bc5ccf63b8c40911afb568b03cace066238ffcf` (tree b4f2a8beaecd) at every READY (05:53Z … 06:39Z) and at every drafter read
(lsremote_1.out 06:34:46Z; predict fetches 06:39:35Z / 06:42:11Z; fill 06:50:46Z / 06:53:28Z; generator 06:53:13Z / 06:53:34Z; --check 06:53:40Z).
Every head's parent IS 2bc5ccf63 (compare merge_base 2bc5ccf63 / ahead 1 / behind 0 / files 1 ×4 — the launcher asserts exactly that, exit 10).
**The tier-1 batch (seat PRs 3, 6-10; same base, separate gate, separate GO) is the likely mover.** It is path-disjoint (the brief's 12 paths;
#1204 at origin measured disjoint, T2-then-#1204 == #1204-then-T2). If develop moves before the launch: `bash take_pr5_gate20T2.sh <scratchpad>` (the
whole re-pin chain; it refuses at the first nonzero step) — after updating round20T2.py's DEV / DEV_TREE / SEAT_T2SUB deliberately from the
re-prediction (the generator and fill refuse while round20T2.DEV != origin).

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_secuura-batch1202-t2.prompt.txt` — fill run 2
  (`fill_prompt_2.out`: 236 lines, 38386 B, sha256 `61415c59641b975d47136503973b21eca72173e24a591e89049bc44b02a16772`; run 1 kept beside as
  `.pre-065328`); first line `ultrathink`; names the brief `fleet/briefs_staged/2026-09-23_raise_seatB_21.md` and the capture `mail_gate20T2_ready.md`;
  the four `PR #N is KS-x.` sentences; TWELVE by-name items (round 19's re-keyed); the KS-1019 TOKEN INSTRUMENT (a planted-token control that FIRES + a
  planted-comment control; the three counts 17679 / 17731 / 18377 on record); the bash-kind rule (each tamper ONE AT A TIME; the two tampers' DIFFERENT
  subsets; the zero-parsed-cells STOP); the MERGE ADDENDUM (1/1/1/1); leads (a)-(j); NOT-PINNED; CARRY-FORWARD (gate19C's CANONENV-NEITHER and
  ERREXIT-ZEROCOUNT); the GO the seat expects VERBATIM: `GO: merge #1202, #1203, #1205, #1206 batch`.
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1202-t2.sh` (generator run 2,
  `gen_launcher.run2.out`: 305 lines, mode 755, sha256 `6230b5f9c1c5674b366eeec92431651791e516c9bf9bd40139f01d73bc033c7f`).
- This directory's `COMMISSION.md`. The drafter's report is its final message to Wednesday (the harness refuses report files from subagents).

## 2. What the launcher asserts at EVERY run (`--check` and launch alike)
Re-reads, in the same run: each of the FOUR heads at origin by branch AND `refs/pull/N/head` (exit 6), origin develop (`ls-remote`), and the GitHub
compare develop...head per PR (merge_base == the pin, ahead 1, behind 0, files 1 — exit 10); a develop != the pin is judged by CONTENT over the 4
targets via the contents API (LANDED 19 / CHANGED 18 / disjoint 17). **Without PR 5 it refuses: fewer than FOUR rows, a row whose head is not
40-hex, or a PENDING-PR- token in the prompt -> exit 34**; #1206 absent / moved at origin -> exit 6. Then the grep ladder over the READY capture and
the prompt: tier lines (7), thinking directive + brief + capture (8), heads in full (20), ticket per PR (32), 62 BOTH tokens (30), 65 by-name keywords
(33), the token instrument (35), the bash-kind rule (36), merge authority (26), MERGE ADDENDUM rules (25), verdict subject / sender / four lines (23),
sub-tree + develop in full (31). Overrides `QAB1202_*` refuse at launch (16); non-TTY launch refuses (21). `--check` is headless (~40 s).
The repin script adds, before any network read, its own FOUR-pinned-rows check (rc 8), then the PULLS API as a second instrument (state `open` ×4, rc 11).

## 3. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1202-t2.sh --check
  Drafter's run: `launcher_check_1.out` rc 0 (06:53:40Z-06:54:22Z). The controls: `launcher_controls_gate20T2.sh` -> `launcher_check_controls.out`
  (read its "controls end" line): C wrong #1206 head -> 6 · D develop at round 19's 3bad652d1 -> 17/18/19 · E develop at #1202's head -> 19 · S PARTIAL
  prompt -> 34 · **P5a PR-5 row PENDING -> 34 · P5b PR-5 row removed -> 34** · G no thinking directive -> 8 · O RULE WHETHER IT BLOCKS reworded -> 30 ·
  L by-name reworded -> 33 · I #1203 re-graded T1 -> 7 · U `planted-comment control` reworded -> 35 · W `DIFFERENT subsets` reworded -> 36 · T a BOTH
  token altered -> 30 · N non-TTY launch -> 21 · POSITIVE -> 0. `pending_control_1.out`: fill and the generator refuse rc 8 on a pipeline copy without
  READY 5 (no launcher written).

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1202|coagent@agentmail.to|yes
  `repin_and_launch_gate20T2.sh` step 0 asserts it (rc 1 if absent; control: the batch1182 line's count = 1). Drafter's read (`repin_dryread_1.out`
  06:55:35Z): batch1202 ABSENT (0), batch1182 present (1).

## 5. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T2_seatB/repin_and_launch_gate20T2.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1202-t2.sh
  Reads its pins FROM THE LAUNCHER (`repin_dryread_1.out` prints develop 2bc5ccf63, the sub-tree, the four `n:head:branch` rows, NROWS 4, PR-5 row
  pinned 1): (0b) four pinned rows incl. KS-1139 (rc 8); (0) routing line (rc 1); (1) ls-remote develop + every pull head + branch; (2) the PULLS
  API; (3) rc 10 if develop is not the pin, rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12 — this lane's 90%
  cut is lifted by Kam's 14:24:05 word; the gate is part of the lane per the commission); (5) the launcher's own `--check` (rc 13); (6) `cockpit.sh add
  QA/Secuura-batch1202 <launcher>` (rc 14) + a pane census. `bash -n` rc 0; NOT RUN by the drafter.

## 6. What is in this directory
  COMMISSION.md · round20T2.py (+ round20T2_selfcheck.out / _2.out: PR5_PENDING True then False; parse_ready controls 3/3 on READYs 1/2/4) ·
  capture_ready_mail_gate20T2.py / capture_ready_mail_1.out (READY 5 NOT YET ARRIVED) / _2.out (READY 5 written) — mail_seatB21_ready01/02/04/05_*.md,
  mail_seatB21_status_0521/0536.md, mail_seatB21_question_*_0511.md, mail_wed_*.md ×4 (the brief 04:52Z, ANSWERs 05:12Z / 05:41Z / 05:58Z); the combined
  mail_gate20T2_ready.md (the launcher greps it) · checkout_counts.sh + checkout_counts_before.txt / _after.txt · lsremote_1.out · loose_objects_1.out ·
  predict_batch_scratch_gate20T2.py / predict_batch_scratch_1.out (PR 5 PREDICTED) / _2.out (MEASURED) / newdev_tree.txt (+ .pre-*-predicted) ·
  c4tokens_gate20T2.js / c4tokens_1.json · gh_pr_reads_gate20T2.py / gh_pr_reads_1.out · linear_reads_gate20T2.py / linear_reads_1.out / _2.out ·
  prompt_gate20T2.DRAFT.txt + fill_prompt_gate20T2.py / fill_prompt_1..2.out · launcher_template_gate20T2.sh.txt + gen_launcher_gate20T2.py /
  gen_launcher.run1..2.out · launcher_check_1.out · launcher_controls_gate20T2.sh / launcher_check_controls.out · pending_control_1.out ·
  repin_and_launch_gate20T2.sh (NOT run) / repin_dryread_1.out / repin_pr5_control_1.out · take_pr5_gate20T2.sh (the re-finish chain) · README.md.
  Every `.out` has its `.rc` beside where the step had one.

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no inbox seen-marking (the capture is a direct API GET), no write into the Secuura checkout (ls-remote /
  status / for-each-ref / count-objects / config --get / ls of .git/worktrees / find over .git/objects / a READ-ONLY `require` of its
  node_modules/typescript by absolute path), every write verb in a scratch clone FROM ORIGIN under the scratchpad guard; no `inbox_routing.conf`
  write; no key printed; no Datasec mail opened or listed (the capture filters on the from-address AND the Blockchain-B subject prefix).

## 8. Re-finishing from disk after any change (a cold successor)
  `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T2_seatB/take_pr5_gate20T2.sh <this session's scratchpad>`
  (capture -> round self-check (PR5_PENDING must be False) -> predict (MEASURED) -> gh / linear -> fill -> generator -> --check; stops at the first
  nonzero rc), then `bash …/launcher_controls_gate20T2.sh <launcher> <prompt> <scratchpad>` (0 MISMATCH), then read the prompt WHOLE, then sections 4-5.

## Wednesday edit 2026-09-23 17:03
Removed `--model opus` from the launcher exec line (backup `launch_qa_secuura_batch1202-t2.sh.pre-0923-1702-configdefault`): Kam 2026-09-23 09:33 (applied by Tuesday e402c5bc7) — launchers follow the CONFIGURED DEFAULT; `opus` would resolve to Opus 5. The recorded launcher sha256 above is the PRE-edit value; `--check` re-run rc 0 after the edit.
