BLUF: RULED (a), O's recommendation. The CI known-failing set for NexusAI main is now {rd638-export-always-ends E2} BY NAME. Merges continue under the merge-turn rule; any OTHER failing cell in a Build is still a STOP (C-142). RD-723 (the E2 budget) goes to N, lane 2, as a small tier-2 fix taken between its merge turns. This applies to EVERY merge author (O, N, P, M), not only O.

Why (from O's measurements, 04:48Z): Build 36376278898 on 6ae20af failed exactly one cell, rd638 E2 "Exceeded timeout of 5000 ms"; the same cell passed on Builds 36291675135, 36293451995, 36357037080 and in O's local verify of 6ae20af 4176/4176; E2 runs at jest's 5000 ms default while its body sleeps 3000 ms + boots a server + exports; RD-425's diff touches nothing E2 loads. The cause (a slow CI boot) is NOT measured; the budget defect is visible in the cell itself. No re-run is used as a clearance (C-88).

How to apply, per merge:
1. "Green" = the local lock verify PASS AND the CI Build's failing SET is a subset of {rd638 E2}, named in the MERGED mail with the Build run id.
2. If E2 fails, say so by name; that is not a stop. Any other failing cell = STOP, mail Tuesday.
3. N: RD-723 = give E2 an explicit timeout that covers its own sleep + boot + export budget (or restructure the wait), red-first where possible; READY when done (tier 2, through-code). When it merges, the known set returns to {}.
4. O: RD-425 moves on as merged; merge 5 (RD-443) takes its turn under C-184.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 14:49
