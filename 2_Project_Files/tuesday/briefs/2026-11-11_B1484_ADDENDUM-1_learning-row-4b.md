# B1484 ADDENDUM-1 (SEAT-N122): the `learning` row comes back as row 4b, right after `header` lands

From Tuesday, 2026-11-11 (just after 04:24 AEDT).

**What changed.** Gate B1433b finished. The first line of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1433b_verify/VERDICT.md` now reads `GATE B1433b: GO WITH FINDINGS @ 725dcf0 on main 849b808` (0 Blockers, 0 Majors, 5 Minors). You skipped `learning` correctly at 03:22:29, when it read PROVISIONAL.

**The change to THE QUEUE:** insert `learning` (`b1433/nexusai-b-learning-manager-log-lines`, gated head `725dcf0ed76572af8773685769e5e5f1414745b2`, own files 2, delta +8/+1, names +8 rd798-learning-manager-log-lines / 0) as **row 4b**, between `header` (4) and `ci` (5). It shares no path with any queue branch (ORDER.md). So:
- after you SEE `header` land by W's checks, do `learning` next;
- its W is the landing of `header`;
- `ci`'s W is the landing of `learning`.

Run the full cycle for it (G against the line above, O, M, chain, invariants, push, READY), with READY line `READY B1484-4b: COUNTS b1433/nexusai-b-learning-manager-log-lines <K sha40> <t>/<s> ON MAIN <sha8>`. Its PREDICTED pair is the pair of the main of its turn + 8/+1. Every later row's PREDICTED pair moves up by +8/+1 from the kit's skip-run numbers.

**Note from the gate:** its own full head/merge verify was NOT RUN (load stayed 14 to 28). Your update and plain runs on the merged tree are therefore the first full-suite runs of this branch. A red is a STOP with the names, never a skip.

**Nothing else changes:** the scope, holds, handshake and HARD STOP. Read this whole at your next W poll, name it in ADDENDA READ, and say in STATUS that row 3 is now row 4b.
