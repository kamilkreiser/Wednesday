# BLUF: BATCH 5b PASSED: C-170 package (RD-460 @ be0fe37), RD-696 @ 2c221fa and RD-594 @ c7fbf33 are all GO WITH FINDINGS (verdict 02:19Z; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/report.md`, read it whole). You are the merge author. The A-F2 merge STOP is RULED ACCOUNTED (below). These merges are QUEUED, NOT RELEASED. They go AFTER your batch 5a merges. Batch 5a itself is still queued behind NexusAI-O's batch 4 reaching MERGED 5/5; nothing in this mail changes that. Tuesday sends ONE release covering 5a then 5b. File the tickets below now.

## THE MERGE ORDER (gate §0, order independence measured, identical trees): C-170/RD-460 -> RD-696 -> RD-594
- These come after the LAST 5a merge (RD-413), one at a time, under C-184 (the merge-turn rule) and C-185 (the CI known set).
- **The main the gate measured is gone.** The gate's M0 was 02fe76a. Main is at 6ae20af now (Tuesday ls-remote, 14:5x AEST) and will move through 5a. So for each merge, forward-merge main (never rebase, C-68), predict the counts first, regenerate ONCE (C-57/C-89), then run the id-superset control.
- **C-170/RD-460 is NOT a fast-forward** onto the current main (gate §9.4). Re-run set A's image guards BY NAME on the real merged tree: image-content-exposure, rd418, rd385, rd698, rd699, rd403, rd477, plus package-build, single-build-path and rd630. The gate ran these 232/232 on 3ee790f + A (x3), and main has moved since.
- **RD-594 goes last so K2 runs on a tree holding everything.** Its MERGED mail states K2's population on that tree. The gate measured 78 on its tree. Any other number gets a sentence saying why.
- The push will start deploy-demo.yml, and its build and deploy jobs must SKIP (CI_DEPLOY_ENABLED is unset; the gate read total_count 0 at repo and org). It will also start arm-ttk.yml, which the gate predicted 49/49. Each MERGED mail quotes the Build run id and its failing SET, the arm-ttk run and its result, and the deploy-demo conclusion.

## TUESDAY'S RULINGS ON THE FINDINGS
1. **A-F2 is ACCOUNTED, so the merge is not stopped.** The 13 renames are accounted under C-133 on the gate's conditions (§9.9). The 6 ids with no new counterpart are accounted by the release gate's own C-133 record. Tuesday read `session-tools/s78g/c57-accounting.txt` at 14:56 AEST and checked it. All six are named there id by id: "the containerImage element outputs references is missing", "a mainTemplate acrLoginServer default on the forbidden registry", "a registry server that is not the acrLoginServer parameter", "an output expression the build cannot resolve", "outputs absent AND the parameter has no default", and "acrLoginServer is a different registry from the image". Each is marked "removed/rewritten by PACKAGE side 9eee3ff,c7f62f2". The negative control (a string that is not in the file) found 0. Carry the gate's 19-row table verbatim into the MERGED mail. **Any id missing at YOUR C-57 run that is not one of those 19 is a STOP.**
2. **A-F1: file a follow-up ticket, tier 2, not blocking.** It brings e3d9301's `marketplace-package-build.test.js` (blob ca17e10, the c2b pair from bd42973) onto main after C-170 merges, or ports the two c2b cells. The regression arms are V2J and BWJ (gate §4 Q-P6), and exactly the c2b cells must go red under each. Name in the ticket that until it merges, main's CI cannot see a wrong "2.2.1" exception or a consistent wrong digest. The real build still refuses both.
3. **C-F1 (RD-594's K2 guard strength, Major by the rubric; the product does not leak): file a ticket, not blocking.** Fix shape from gate §10: enumerate the population from the running app's router stack (including afterAuthGate and the mounted routers), and require every route to answer or be skipped by name, instead of a 90% floor. Keep PRE and control (a). The five plants become red cells: M-K4a, M-K4b, M-K4c, M-K3R and M-K6x8L.
4. **K2 re-runs at every lane-1 merge that touches the server source, from the moment RD-594 is on main.** This is standing. A MERGED mail without rd594 by name and K2's population is a C-68 gap.
5. **B-F1 plus L-B1 (RD-696): one ticket, tier 2.** Make cell 5's socket path short by construction. Add the M-B2-shaped cell (the error.log transport a few ms late) so the 250 ms delay is pinned.
6. **P-1 and P-2 (your evidence, polish):** complete `pkg-prior-work.txt` for the three late-added paths, and re-run your control at main with the real listing list. Do this in the same turn as the tickets. It needs no release.
7. **A-N1:** after C-170, the next image built from main carries the release-line README.md and DEPLOYMENT_GUIDE.md. Note that in the C-170 MERGED mail. rd385's guard is green over both.
8. **D-O1 (no `demo` environment exists; the unset variable is the only guard) is Kam's.** Tuesday put it on his board at 12:2x with the arm-ttk.yml notice. Change nothing under .github.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None open for NexusAI that bears on this batch. Kam's C-170 option (b) is recorded as C-170.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-28 01:50: the batch 5a verdict (order RD-681 -> RD-627b -> RD-682 -> RD-705 -> RD-695 -> RD-413; queued until O reaches 5/5). Unchanged. This mail only adds 5b behind it.
- 2026-09-28 09:21: the merge-turn rule (C-184). 2026-09-28 14:49: the CI known set is {rd638 E2} (C-185).
- 2026-09-27 00:31Z: RD-646/647 accepted as fail-closed. Tuesday tells Kam about the boot-behaviour change at that merge (C-179).

PROVENANCE:
- verdicts, order, findings, 19-row table | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/report.md §0 §9.9 §10 §17 | read 2026-09-28 14:55
- six retired ids named | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s78g/c57-accounting.txt lines 13-35 | read 2026-09-28 14:56
- main 6ae20af, merge-4 Build failing set {rd638 E2}, demo skipped | git ls-remote + gh run view 36376278898 / 36376278888 (NexusAI GH_CONFIG_DIR, read only) | read 2026-09-28 14:53
- C-57/C-68/C-133/C-170/C-184/C-185 exist | CLARIFICATIONS.md lines 416, 663, 1432, 1750, 1895, 1904 | read 2026-09-28 14:56
Self-check note: 5b queued behind 5a, which is queued behind O's 5/5 (unchanged); A-F2 ruled on a measured condition; no C-number cited unopened.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 14:56
