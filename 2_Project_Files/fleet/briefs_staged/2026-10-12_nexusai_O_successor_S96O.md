# BLUF — SUCCESSOR SEAT Datasec/NexusAI-O (lane 3), after a cap stop and a reboot. Your predecessor S93O did not wrap: the weekly allowance ran out on 2026-10-08 and the Mac mini rebooted on 2026-10-12 (~11:43 AEDT). Nothing of yours is running. YOUR NEXT TURN IS RD-690 @ b05b6ff (order item 3), right after M's RD-657, which is merging now. You may PREPARE RD-690 now: the forward merge onto the then-main and the own install. File NO lock ticket until Tuesday's TURN mail. Also owed this round: the F-821-1 fix round (gate 19). Send a PLAN CONFIRMATION first.

**Addressed to the cockpit seat `Datasec/NexusAI-O` ONLY.** Seats N (S94N) and M (S95M) are live and share this inbox (datasec-nexusai@). A mail naming another seat is not yours. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`). The highest HANDOVER-S* file is S93O, and S94N and S95M are live, so you are **S96O**.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S93O.md` WHOLE (45 lines; the UPDATE blocks at the top are newest). Then `HANDOVER-S87O.md`'s top block: the recipe (session-tools/s87o/: fwd-merge.sh, own-install.sh, merge-hold-g14.sh, land3.sh).
2. Tuesday's mails on this inbox since 2026-10-08T03:00Z naming O, `M N O` or `Datasec/NexusAI`, read WHOLE. Today these include the gate-19 RELEASE (2026-10-12T00:57Z): your RD-801/822 + RD-802 placement, and the F-821-1 fix round.
3. CLARIFICATIONS: C-57, C-68, C-141 + addenda, C-185, C-186, C-190 + addendum, C-199 (stacking), C-205 (RD-827).

## MEASURED BY TUESDAY (2026-10-12 ~13:0x AEDT)
- main = 9360ae005ed1 (git ls-remote origin; RD-608). Its push Build 38190543781 = success (gh run view, 01:59:42Z). M holds the RD-657 turn now. Main WILL move before your turn, so re-read it at your TURN mail.
- Your heads at origin (ls-remote): rd-690-workspace-prefix-comments-s87o = b05b6ffe15ca · rd-675-ban-wide-windows-scripts-s87o = 12de5116a666 · rd-801-feedback-log-injection-s87o = 661311351166 · rd-802-provisioning-log-injection-s87o = a103c8e8c8a9 · rd-828-gate14-cells-s93o = 2fab7725ab27.
- Known runner artefact: the shared C-57 runner links to worktrees/mkt-rc-selfcontained-s62/node_modules (proxy-addr 2.0.7), so its summary shows rd816 P1 x3 "failed" on A and MERGED. Your own-install hold's VERDICT line is the coverage. RD-837 tickets the runner.

## AUTHORITY
- The open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27). Every merge waits for Tuesday's TURN mail on a gated head.
- No CodeQL alert is ever dismissed.

## YOUR QUEUE (turn order item numbers; each merge opens on a TURN mail)
3 RD-690 (rd385 BY NAME; correct D-F1 in its MERGED) · 5 RD-675 · 11 RD-828+833 (account for the two renamed rd709/rd699 hygiene titles by name) · 18 RD-801+822 · 19 RD-802 (after RD-801, never in the same push).
**Build work while waiting (one item only):** the F-821-1 fix round on the jest-lock tool (gap-0 placement: a merge whose pid sorts below the gate's passes the gate). Evidence: the gate-19 report folder's f3-placement.txt. Tooling, tier 2 through code, round 1 of 2, for gate 21. Never edit the installed session-tools/nexusai-lock.sh while any copy runs: build and arm the fix as a copy, then swap it in only at a moment when the lock has no holder and no queue, and say when. RD-837 (the C-57 runner install) comes after F-821-1. Do not start it.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None for NexusAI (decision_queue.sh list ruled --undelivered, read 2026-10-12).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- RD-827 own install on any tree at or after 90b2556 (print proxy-addr path + version, 2.0.8).
- C-186: turns only by Tuesday's TURN/RELEASE mail. RD-802 is stacked on RD-801 (C-199).
- Alert reads: positive control state=fixed on refs/pull/58/head = #256-#259; the open-alert read BEFORE the main push.
- Ruling (i), the by-hand gate yield, is RETIRED from gate 21 on (gate-19 RELEASE).

## STANDING LINES
- PRIOR-WORK CHECK before rebuilding/replacing/removing anything. Every READY carries PRIOR WORK + NOT TESTED.
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss.
- Never delete (move aside). Never edit a running script. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- Write the handover when your pane first shows less than 10% before auto-compact.

PROVENANCE:
- main 9360ae005ed1 and the five lane-O heads | git ls-remote origin on /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-10-12
- Build 38190543781 success | gh run view, with GH_CONFIG_DIR=/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials/.gh-config | read 2026-10-12
- lane 3 state and queue | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S93O.md | read 2026-10-12
- F-821-1 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/body-0.md §0b | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 13:00

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-O -> Tuesday] QUESTION: plan confirmation` with your seat identity facts (pane id, cockpit name, claude pid), what you read, your RD-690 prep state, your F-821-1 fix design (files, cells red at the installed tool, how you swap it in safely), and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
