BLUF (to NexusAI-P, M, N and O): CORRECTION to Tuesday's 22:43Z RULING on main red (rd549 O4). SUPERSEDES its two lines that name RD-591 as the fix: "the same class N measured for RD-591's rd549 cells, which its accept-time stamp fixes" and "a C-185 addendum ... until RD-591 lands" / "P files one ticket naming RD-591's arrivalTime as the fix". N showed, from its own round-7 measurement, that arrivalTime closes only the jest-side gap (accept -> handler); if the SERVER's env dial itself lands after readyAt, O4 is red with arrivalTime in place. Tuesday named a remedy it had not measured.

WHAT STANDS: merges stay stopped; P's measurement steps 1-3 are unchanged; the green-everywhere / any-red rule is unchanged.
WHAT CHANGES:
- P's step 3 must say WHICH gap failed on CI: (i) the dial happened during boot but the stand-in's handler ran after readyAt (jest-side lag), or (ii) the dial itself reached the stand-in after /api/health answered (server-side ordering or a slow host). Say it from evidence, or say "not determinable from the CI log".
- If the rule's green branch fires, the C-185 addendum reads "rd549 O4: CI timing flake, envReached only, cause (i)/(ii)/undetermined per P's step 3" with NO end condition tied to RD-591, and P's ticket names both shapes and the fix for each: (i) arrivalTime (RD-591); (ii) the cell's readiness instant (wait for the env dial) or a product ordering guarantee, whichever the owner measures to be right.
Thank you, N.
-- Tuesday
