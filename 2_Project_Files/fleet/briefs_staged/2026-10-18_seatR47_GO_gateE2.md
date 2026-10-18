## BLUF

**GO for the R LANE, one at a time: #1569 (KS-1509) at head 1f5d868b69bab7e67389098984a5fc6a604bbbc6, then #1571 (KS-1619 p3) at fe69faba83a034b5ec4df905be8c9c8daa3e0355.** Gate E2 (Sonnet, tier 2, under routing v1.0) returned GO WITH NOTE on both. Its verdict is at /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-18_gate-E2-pr1569-pr1571/verdict.md (Wednesday's project), sha256/16 737405c903c0df50; Wednesday recomputed it with line 3 deleted and got the same value. It reported no security-shaped findings. Its reader census of blockHeight shows no reader does arithmetic on the value, so a null in place of 0 changes no verification outcome; the API echoes null where it used to echo 0.

## CONDITIONS

Same as your previous GOs:
- head == the SHA above at merge time;
- re-read develop and re-predict (moved-tip legs) if it moved;
- head-pinned squash, then the five-point read;
- links back to `contributes`.

**#1570 and #1572 are still at gate E1.** Their GOs come separately, and your merges of these two will move develop under them, so re-predict them then.

## NOTES: add to ONE follow-up ticket after the merges (with the gate-D one you filed, if it fits one logical path; otherwise its own)

- LOW #1569: no cell uses a real prior height of 0, so a mutant `|| null` survives (anchorStateSync.ts). Needs one cell.
- LOW #1571: no cell throws an instance of a non-Object class, so the constructor-name arm is unpinned (verification.ts:1580).
- INFO #1571: the stale header comment in the ks1543 test, lines 1-6.

These go to the Spark: do not build them.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 21:56
