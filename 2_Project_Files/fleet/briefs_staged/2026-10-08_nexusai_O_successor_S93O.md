# BLUF — SUCCESSOR SEAT Datasec/NexusAI-O (lane 3): your predecessor S87O wrapped cleanly at 13:55Z on Tuesday's ask (window near full). Nothing of yours is running. Your queued work is MERGES on Tuesday's word: (1) RD-801 + RD-822 @ 6613113 when gate 19 RELEASES them; (2) RD-737, then RD-708, RD-690, RD-675 in the turn order; RD-802 @ a103c8e lands only after RD-801 and after gate 20. Meanwhile, PROPOSE one disjoint item (RD-828 or another). Send a PLAN CONFIRMATION to Tuesday before any product edit or lock ticket.

**Addressed to the cockpit seat `Datasec/NexusAI-O` ONLY.** `Datasec/NexusAI-M`, `-N`, `-P` and `-R` are live and share this inbox (datasec-nexusai@). A mail addressed to another seat is not yours. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`), your launcher and your process tree, never from which thread looks familiar. Number your session from the highest HANDOVER-S* on disk (S91P on disk at 00:5x AEDT; S92R is live as seat R): you are **S93O** unless a newer one appears.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S87O.md` WHOLE. Its top block "CURRENT STATE AT WRAP" supersedes the older successor block below it. It names your landing recipe (session-tools/s87o/ scripts) and every head.
2. Tuesday's mails on this inbox naming `Datasec/NexusAI-O` since 2026-10-07T13:00Z (the 13:53:49Z "wrap now" ANSWER and the 11:00Z RD-709 TURN), read WHOLE.
3. `1_Project_Definition/CLARIFICATIONS.md` by C-number: C-141 + addenda (the jest queue; ADDENDUM 7: only a merge ticket's tag contains the word "merge"), C-185 (CI known-failing set), C-186 (merge turns), C-190 (CodeQL ruleset, BOTH thresholds), C-199 (stacking; applies to RD-802 on RD-801).

## MEASURED BY TUESDAY (2026-10-08 ~00:5x AEDT)
- main = 0f128cbba2c0 (git ls-remote origin). Seat N holds the merge turn now (RD-791; jest lock owner tag s87n-merge-rd791, read at session-tools/locks/nexusai-jest.lock/owner).
- Heads at origin (ls-remote): rd-801-feedback-log-injection-s87o = 661311351166; rd-802-provisioning-log-injection-s87o = a103c8e8c8a9.
- Gate 19 (pane QA/NexusAI-batch19) is RUNNING; RD-801 + RD-822 and RD-821 r2 are its members. Gate 20 (RD-802 a member) is being drafted; not launched.
- Seat O's predecessor pane was closed by Tuesday with pane_close.sh ("closed %7; listeners 11 -> 11").

## AUTHORITY
- The open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27), on Tuesday's GO after a QA gate verdict at the head. Nothing of yours merges until Tuesday sends a RELEASE or TURN mail naming it.
- No CodeQL alert is ever dismissed (dismissal is Kam's alone; the Datasec rule is fix in code).

## WORK, in order
1. Plan confirmation (below). Re-arm your own inbox watcher (your predecessor's died with its pane).
2. Propose ONE disjoint item for the wait (RD-828, lane O's gate-14 findings ticket, is the natural one): files it touches, why disjoint from every live seat (your own branch census), tier. Nothing starts before Tuesday answers.
3. On gate 19's RELEASE: land RD-801/RD-822 by your predecessor's recipe (forward merge onto the then-main, OWN install per RD-827, merge hold, land3.sh with the state=fixed control on refs/pull/58/head = #256-#259). Then RD-737 etc. on TURN mails.

## RULED BY KAM, NOT YET IN AN ARTEFACT (decision_queue.sh list ruled --undelivered, filtered to NexusAI, read 00:5x AEDT)
- `rd104-gh-identity-acceptance-false-premise` (ruled `youcheck`) and `t9-nas-leg-direction` (ruled `a`): neither is lane O's; no action.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- RD-827: any tree at or after 90b2556 gets its OWN install before any hold (print the resolved proxy-addr path + version).
- RD-802 is stacked on RD-801 (C-199): lands only after RD-801, never in the same push; on any RD-801 fix round, forward-merge and re-run rd802's cells.
- C-186: merge turns are given by Tuesday's TURN or RELEASE mail only.
- Alert reads at landing: refs/pull/58/head has 0 OPEN alerts now, so the working control is state=fixed on refs/pull/58/head = exactly #256-#259.

## STANDING LINES
- PRIOR-WORK CHECK: before rebuilding, replacing, removing or redesigning anything, look first (git log -S/--follow/blame, CLARIFICATIONS, history, handovers, tickets), write down what existed and why with its source; every READY FOR QA carries a PRIOR WORK section (or "nothing replaced").
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss an alert.
- Never delete: quarantine/move. Never edit a script while a copy of it runs. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- Context: write the handover when your pane first shows less than 10% before auto-compact, not at 1%.

PROVENANCE:
- main 0f128cb; rd-801 6613113; rd-802 a103c8e | git ls-remote origin on your own 2_Project_Files | read 2026-10-08
- lane O state, recipe, turns | your own HANDOVER-S87O.md (project root) CURRENT STATE AT WRAP block (mtime 2026-10-08 00:54) | read 2026-10-08
- jest lock holder s87n-merge-rd791 | your own session-tools/locks/nexusai-jest.lock/owner | read 2026-10-08
- highest HANDOVER is S91P | ls of your own project root HANDOVER-S* | read 2026-10-08
- undelivered NexusAI cards | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered | read 2026-10-08
- pane closed | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/pane_close.sh output | read 2026-10-08

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-08 00:57

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-O -> Tuesday] QUESTION: plan confirmation` with your seat identity facts (pane id, cockpit name, claude pid), what you read, your proposed disjoint item, and any launcher preflight warnings VERBATIM. Then wait; your wake is Tuesday's mail plus a tap.
-- Tuesday
