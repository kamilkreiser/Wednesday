# BLUF — SUCCESSOR SEAT Datasec/NexusAI-N (lane 2), after a cap stop and a reboot. Your predecessor S87N did NOT wrap: the weekly allowance ran out on 2026-10-08 and the Mac mini rebooted on 2026-10-12 (~11:43 AEDT). Nothing of yours is running. FIRST WORK: RD-608 (turn 1 of the merge order). Its merge test ran to the end on 10-08 and was never pushed. Read its results, work out whether the 3 failures are the known proxy-addr environment class or something RD-608 caused, and send a PLAN CONFIRMATION to Tuesday before you land anything.

**Addressed to the cockpit seat `Datasec/NexusAI-N` ONLY.** You are the ONLY NexusAI seat live right now. M and O follow you one at a time, and they share this inbox (datasec-nexusai@), so a mail naming another seat is not yours. Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`), never from which thread looks familiar. The highest HANDOVER-S* on disk is S93O, so you are **S94N**.

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S87N.md` WHOLE (158 lines). Its last section (15) is the newest state. It holds your landing recipe, the RD-827 own-install rule, and the RD-747 merge duties.
2. Tuesday's mails on this inbox naming `Datasec/NexusAI-N` or `M N O` since 2026-10-08T03:00Z, read WHOLE. These are the TURN for RD-608, the rebuilt order, and the gate-20 RELEASE.
3. `1_Project_Definition/CLARIFICATIONS.md` by C-number: C-141 + addenda (the jest queue), C-57 (id superset), C-68, C-185 (CI known-failing set), C-186 (merge turns), C-190 (CodeQL, BOTH thresholds), and the RD-827 note.

## MEASURED BY TUESDAY (2026-10-12 ~11:5x AEDT). Your own reads decide.
- main = 53b1ee57c2b6 (git ls-remote origin). Unchanged since RD-708 landed on 10-08, so your forward merge 6e65676 (= 9fd5c9a + 53b1ee5) is still onto the current main.
- Jest lock: no holder; queue-jest empty (ls session-tools/locks/). Your hold's ticket is in released/ as done-jest-s87n-merge-rd608-33899-*. s87n-rd131-proof2 also shows done.
- The hold's results are in `session-tools/c57-s87n-merge-rd608/` (files dated 10-08 17:38 to 18:40). summary.txt: VERDICT OK on the id superset (merged 4409 ⊇ A 4407 ∪ B 4214, missing 0). MERGED.json: 3 failed of 4418, success=false. A.json (main 53b1ee5): 3 failed of 4416. B.json (9fd5c9a): 0 failed of 4223.
- The 3 failures in MERGED, read from MERGED.json by Tuesday, are all `__tests__/rd816-proxy-addr-mapped-subnet.test.js` P1 (IPv6 trust subnet ::ffff:0:0/80 vs IPv4 peers), run in `qa-worktrees/c57-s87n-merge-rd608-MERGED`. Main fails the same 3 in this runner. That fits the RD-827 class (a proxy-addr 2.0.7 resolve in the runner's tree), not RD-608. **UNMEASURED: which proxy-addr version and path that qa-worktree resolved.** Measure it (require.resolve + version) before you call it environment.
- The tmux fleet holds only Tuesday's pane and the monitor. Every 10-08 seat pane is gone, and so is gate 19 (it never wrote a verdict).

## AUTHORITY
- The open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27). Tuesday reads it as still standing (renewal of the same account, no account switch seen). Merges only on Tuesday's TURN or RELEASE mail, after a QA gate verdict at the head. RD-608 was released by gate 12 and given its TURN on 2026-10-08.
- No CodeQL alert is ever dismissed (dismissal is Kam's alone; fix in code).

## WORK, in order
1. Plan confirmation (below). Re-arm your own inbox watcher (your predecessor's died with its pane).
2. RD-608: diagnose the 3 reds as above. Your options: (a) environment (proxy-addr 2.0.7 in the runner tree): fix the runner's install per RD-827 (own install, 2.0.8, never delete: mv aside), re-run ONLY what the C-57 recipe needs under a merge ticket, then land by your predecessor's recipe (alert read BEFORE land2, full 40-char expected main from git rev-parse); (b) anything else: STOP and mail Tuesday with the evidence. Say in the plan confirmation which one you believe, and on what measurement.
3. After RD-608 lands: the MERGED mail, then wait for your next TURN mail (RD-649 is order item 4).
4. RD-131: s87n-rd131-proof2 ran on 10-08 (results dir session-tools/s87n/rd131, out rd131-hold2.out per your handover). Read it. If it is green, send the READY for gate 21 (tier 2 + browser). Nothing new is built meanwhile.

## THE MERGE TURN ORDER (unchanged; main has not moved since 10-08)
1 N RD-608 · 2 M RD-657 · 3 O RD-690 · 4 N RD-649 · 5 O RD-675 · 6 N RD-614 · 7 N RD-629 · 8 N RD-591 · 9 M RD-795 · 10 P RD-823 · 11 O RD-828+833 · 12 P RD-751 · 13 M RD-817 · 14 N RD-747 @968ee14 · 15 P RD-831 · 16 R RD-777+776 · 17 R RD-761 · 18 O RD-802 (only after RD-801, which waits on gate 19). Each turn opens on Tuesday's TURN mail.

## RULED BY KAM, NOT YET IN AN ARTEFACT (decision_queue.sh list ruled --undelivered, read 2026-10-12)
- None for NexusAI (the undelivered list holds Vision/ATTIO/NAS cards only).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- RD-827: any tree at or after 90b2556 gets its OWN install before any hold. Print the resolved proxy-addr path + version.
- C-186: merge turns come by Tuesday's TURN or RELEASE mail only.
- Alert reads at landing: the working positive control is state=fixed on refs/pull/58/head = exactly #256-#259.
- RD-747 merge duties stand as written in your handover section 15 (RD-834 named; the two C-40 survivors onto RD-747's ticket at the merge step).

## STANDING LINES
- PRIOR-WORK CHECK: before rebuilding, replacing, removing or redesigning anything, look first (git log -S/--follow/blame, CLARIFICATIONS, history, handovers, tickets), write down what existed and why with its source. Every READY FOR QA carries a PRIOR WORK section (or "nothing replaced").
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss an alert.
- Never delete: quarantine/move. Never edit a script while a copy of it runs. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- Context: write the handover when your pane first shows less than 10% before auto-compact, not at 1%.

PROVENANCE:
- main 53b1ee57c2b6 | git ls-remote origin refs/heads/main on /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-10-12
- hold results A/B/MERGED counts and the rd816 failing names | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/c57-s87n-merge-rd608/summary.txt and MERGED.json (python json read) | read 2026-10-12
- lock state | ls /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks/ (no jest holder dir, queue-jest empty) | read 2026-10-12
- lane 2 state, recipe, turn order | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S87N.md section 15 (mtime 2026-10-08 16:47) | read 2026-10-12
- highest HANDOVER is S93O | ls /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S* | read 2026-10-12
- undelivered rulings | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered | read 2026-10-12
- fleet panes | tmux list-panes -a on the Mac mini | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 11:55

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-N -> Tuesday] QUESTION: plan confirmation` with your seat identity facts (pane id, cockpit name, claude pid), what you read, your RD-608 diagnosis and the measurement behind it, and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
