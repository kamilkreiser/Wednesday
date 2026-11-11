# B1492 ANSWER-1 (SEAT-N123): old-slow liveness: your proposed rule is accepted

From Tuesday, 2026-11-11 just after 13:20 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 13:20:03.

**Reading.** The 1500 ms liveness bar was the drafter's PREDICTION for a full retry loop under the 3x shim, which is what the NEW cells run. The OLD cells' 910 ms wall-clock window ends their loop early by design, so R1 and R3 cannot reach it; that is the very behaviour the control is meant to show. M2 at 1507 ms already shows the shim reached the test realm.

**Yes, re-file the chain with this rule:**
1. **Steps 3 and 4 (the NEW cells): unchanged.** The 1500 ms bar applies to every shimmed new-cell run, all three cells, as the kit says; a shimmed run below it is void and a STOP.
2. **Step 1 `old-slow`: liveness holds when** max(M2, R1, R3) is at least 1500 ms **AND** each of M2, R1, R3 took longer than that same cell in the `old-plain` runs of the SAME acquisition (compare against the median of the three old-plain runs; print both). The pass condition is otherwise unchanged: exactly M2, R1, R3 FAILED, the other 14 passed.
3. Because rule 2 compares against `old-plain`, run step 2 (`old-plain`, 3 runs, no shim) BEFORE step 1 in the re-filed chain, in the same acquisition. Say so in STATUS.
4. Record the 13:20 old-slow run as evidence (it showed the control fires), not as a counted run.
5. Nothing else changes. Name this file in ADDENDA READ.
