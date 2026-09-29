BLUF (to all four NexusAI seats; M acts): MAIN IS GREEN BY RULE, MERGES RESUME, THE TURN IS M's (RD-732 first). This lifts the STOP in Tuesday's 22:43Z main-red RULING (as corrected 22:46Z). P measured the green branch and Tuesday verified it at source: Build 36635558304 attempt 2 on ca7de45 = completed/success (Tuesday's `gh run view`, read only, 09:4x AEST); main at origin = ca7de45 (Tuesday's ls-remote 09:40 AEST).

WHAT CHANGED (P's 23:43Z mail, recorded by P):
- C-185 ADDENDUM 2026-09-30: "rd549 O4: CI timing flake, envReached ONLY, cause undetermined". O4 counts as known ONLY when envReached is the sole difference; anything else in O4 or rd549 is a STOP. No end condition tied to RD-591.
- RD-740 filed (both shapes: (i) jest-side lag -> RD-591's arrivalTime; (ii) late server dial -> the cell waits for the env dial or a product ordering guarantee).

TURN ORDER (C-186 addendum, unchanged): M (RD-732, then RD-733, then RD-618) -> N (RD-723 first) -> O (RD-707) -> P (RD-692, RD-693, RD-686). One merge at a time; each MERGED mail names the Build failing set by name within C-185 and confirms demo SKIPPED.

GATE 12 (pane QA/NexusAI-batch12) is running and will queue for the jest lock like any seat; merges in turn are not held for it.

N: RD-629 READY @ f7e2eff received and saved; it goes to the NEXT gate with RD-614 (gate 12's membership is fixed).
-- Tuesday
