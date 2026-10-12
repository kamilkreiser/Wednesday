# BLUF — SUCCESSOR SEAT Datasec/NexusAI-R (lane 4), after a cap stop and a reboot. Your predecessor S92R did not wrap (the weekly cap on 2026-10-08, then the Mac mini reboot on 2026-10-12 ~11:43 AEDT). Nothing of yours is running. ONE BUILD ITEM: the RD-807 F-807-1 fix round (test-only), so it joins gate 21 with the other three members already READY. Your merge turns (16 RD-777+776, 17 RD-761, 21 RD-794, 22 RD-819, then RD-807 after its gate) come later, each on a TURN mail. Send a PLAN CONFIRMATION first.

**Addressed to the cockpit seat `Datasec/NexusAI-R` ONLY.** Seats N (S94N), M (S95M) and O (S96O) are live and share this inbox (datasec-nexusai@). A mail naming another seat is not yours. Establish your seat from your own pane's cockpit name. The highest HANDOVER-S* file is S93O, and S94N-S96O are live, so you are **S97R**.

## READ FIRST (all in the NexusAI folder)
1. `HANDOVER-S92R.md` WHOLE (53 lines). It holds the lane-R table, the merge-turn notes and the C-209 landing condition for RD-777/776.
2. Tuesday's gate-19 RELEASE (2026-10-12T00:57Z) WHOLE: RD-794/RD-819 placement and the F-807-1 fix round.
3. Gate 19's finding text: `Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/body-0.md` §0b row F-807-1, and its reproducer `qa-d807race19.js` (in that report's evidence).
4. CLARIFICATIONS: C-57, C-68, C-141 + addenda, C-185, C-186, C-199 + addendum, C-205 (RD-827), C-209.

## MEASURED BY TUESDAY (2026-10-12 ~13:1x AEDT)
- main = 9360ae005ed1 (git ls-remote). M is merging RD-657 now, so main will move.
- Your heads at origin (ls-remote): rd-807 9b15a99bce53 · rd-775 537741ce9d1d · rd-777-776 94b288cc64d6 · rd-761 7f1881eae1e8 · rd-794 cd171f953a4c · rd-819 fdd07af07964.
- RD-775 READY @ 537741c is saved for gate 21 (tier 1). No action needed unless its head must move.
- Known runner artefact: the shared C-57 runner's install is proxy-addr 2.0.7, so its "failed 3" (rd816 P1) is not yours. Your own-install hold's VERDICT line is the coverage (RD-837).

## THE BUILD ITEM: RD-807 F-807-1 (gate 19, MAJOR)
The gate's words: "Its route cell's readProbe() catches only ENOENT; the preload rewrites probe.json non-atomically → a torn read ("") throws in beforeAll and fails 3 cells (MTF union). 20/200,000 torn reads measured; 5/5 green alone. Fix: temp file + rename, or retry on empty."
- Fix the test harness only (probe write atomic via temp + rename, or readProbe retries on empty). The product incidents.js is untouched.
- A cell that goes red on a torn read at 9b15a99 and green after. Use the gate's reproducer shape. A mutant of your fix must bite.
- Tier 2 through code, round 1 of 2 under the cap. Base: the gated head 9b15a99. Own install per RD-827 before any jest run. File a non-merge jest ticket only behind any merge ticket (merge-first).
- READY FOR QA for gate 21 with PRIOR WORK + NOT TESTED.

## AUTHORITY
- The open-ended NexusAI grant "work through the tickets and merge once tested" (Kam, 2026-09-25, re-affirmed 2026-09-27). Merges only on Tuesday's TURN mail. No CodeQL alert is ever dismissed.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None for lane R (decision_queue.sh list ruled --undelivered, read 2026-10-12; RD-774's ruling is already on its ticket, comment 39347).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- RD-827 own install on any tree at or after 90b2556.
- C-186 turns. RD-819 after RD-794, never in the same push (C-199). C-209: #83/#84/#43 must read fixed on main after RD-777/776's push.
- Ruling (i), the by-hand gate yield, is RETIRED from gate 21 on.

## STANDING LINES
- PRIOR-WORK CHECK. Every READY carries PRIOR WORK + NOT TESTED.
- CodeQL: never push an unscanned commit to main; never bypass; never dismiss.
- Never delete (move aside). Never edit a running script. Never kill by pattern (C-174). Any harness that touches the jest queue runs on a scratch NEXUSAI_LOCK_BASE (today's O slip).
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- Write the handover when your pane first shows less than 10% before auto-compact.

PROVENANCE:
- main 9360ae005ed1 and the six lane-R heads | git ls-remote origin on /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-10-12
- lane R state | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S92R.md | read 2026-10-12
- F-807-1 text | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/body-0.md §0b | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 13:13

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-R -> Tuesday] QUESTION: plan confirmation` with your seat identity (pane id, cockpit name, claude pid), what you read, your F-807-1 fix design and cells, and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
