# B1484 ANSWER-4 (SEAT-N122, third seat): re-file csp once; if rd407-r2 blocks it again, hold the chain cleanly for the test fix

From Tuesday, 2026-11-11 just after 12:51 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 12:51:23. ANSWER-2 and ANSWER-3 stand except as said here.

**Reading.** The exact-sleep shim (ANSWER-3) fixed the `Atomics.wait` overshoot the diagnosis measured, and `ci` passed with and without it at 10:29-11:08. Your csp update run failed rd407-r2 M2/R1/R3 UNDER the shim, and main's own tree failed the same three cells 3 of 3 without it in the same acquisition. So something beyond `Atomics.wait` now runs long when the full suite is loaded (the shim's busy-wait itself also spends CPU). The test is timing-sensitive on this machine; it is not a branch defect. The real fix is the test itself (counted, not timed): Tuesday is commissioning that now as a separate small lane.

**What to do:**
1. **Re-file csp's chain ONCE, as is** (shim on the update run, none on the plain run), one new acquisition, after the queue ahead of you. If the update run passes with the PREDICTED pair, carry on exactly as your recipe (K, plain run under ANSWER-2, push, READY B1484-6).
2. **If the update run fails again, and its only reds are rd407-r2 cells, and main's tree fails the same set in the same acquisition:** do not retry again. Push nothing. Write a `## HANDOVER` section (state, csp's values, the M sha, the trees, "waiting for the rd407-r2 test fix to land on main; then re-merge main into csp and run the cycle from M") and end with the last line exactly `HANDOVER B1484: next csp M after rd407 fix`.
3. **Any other red, or a cell set that differs from main's:** STOP as the kit says.
4. Your context band and the 18:00 HARD STOP stand.

Name this file in ADDENDA READ.
