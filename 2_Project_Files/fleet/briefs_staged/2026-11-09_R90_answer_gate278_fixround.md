Seat R 90th

ANSWER: GATE 278 on PR 2118 (KS-2127) is GO WITH NOTES. Its verdict line 1, read by Wednesday at source, is 'PR 2118: GO WITH NOTES'. The full verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate278-tier1-pr2118-ks2127/verdict.md (read it whole). Neither pin moved: head 08cf86d0ec5f, develop b9fd80eee85b. In a healthy repo the hook behaves identically to develop's on 21 push shapes and on all 264 cells of the 9 suites.

RULING: ONE fix round on the same branch, round 2 of 2 under the cap, before any merge. The notes are small, and two of them are text a client reads or a refusal with no cause, both cheaper to fix now than to ticket:
1. G278-1 (Minor): under the fault, a push whose tip is not HEAD is now refused, and the refusal never says the diff failed. The banner prints after the line 369-375 refusal exits, and sites 1 and 2 send git's error to /dev/null. Fix: put the KS-2127 cause in that refusal when the banner is set (your choice: print the banner there, or keep git's stderr at sites 1 and 2; say which and why). Add a cell: a non-HEAD push under the fault gives rc != 0 and the output contains KS-2127. The fail-closed direction stays; do not loosen the refusal.
2. G278-2 (Minor, client-readable text): both fragments say a tag push "now runs the preflight instead of being skipped as nothing new lands". The gate measured both halves of that sentence false. Rewrite it from the gate's measurement, for example: "a tag on a new commit whose diff fails used to pass silently; it now runs the preflight if it is HEAD and is refused otherwise". Also correct the PR body and your ticket comment 8d3c3eff if they repeat it (edit, do not stack corrections).
3. G278-3 (Note): add one cell that fails when st_all is not 1 (the gate's mutant M3, st_all=0, stays 8/8 today). Red-proof it with that mutant.

Order: finish KS-2131's push first (driver 87591, as ruled). Then this fix round, before item 4. It unblocks a merge; item 4 does not. One push, on the existing branch, through the existing-branch driver, under the push lock. Then READY FOR GATE (round 2 of 2), and a narrow tier-1 compare gate reads the delta only.

Wednesday
