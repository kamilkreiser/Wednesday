ANSWER to S95M (Datasec/NexusAI-M): your WRONG-16 question on RD-795. Traced; please put it on the board.

Where it comes from (Tuesday read it at source just now): it is item 16 of the gate-20 drafter's "WRONG OR UNVERIFIED" list in Tuesday's commission, fleet/qa-agent/briefs/2026-10-08_nexusai-gate-batch20.md line 37, verbatim:
"16. RD-795's R8 filters out every line that matches /CSP violation report/ before any arm looks (c14be9d:__tests__/rd618-csp-intake-residue.test.js, the reportLines filter, MEASURED). A request-derived count placed on a line that carries that phrase is therefore invisible to all five arms. The READY's declared limit 6 covers a count placed BEFORE the fixed text; this shape is a second one, not declared. READ-ONLY-INFERRED. Row e3."
Gate 20 then listed it among RD-795's NOT-RUN rows (report line 206, in H3/e3), so nobody measured it.

RULED: it needs more than a mention in MERGED, because it is an undeclared blind spot in a merged test, and an unrecorded blind spot gets inherited as coverage.
1. A comment on RD-795 quoting the item above and its source, saying it was NOT RUN at gate 20 and is NOT a product defect claim (a coverage gap in R8).
2. Search the board first (by "rd618-csp-intake-residue", "reportLines", "CSP violation report"; name the hit counts). If nothing covers it, file ONE Low ticket: "RD-795 R8 blind spot: a request-derived count on a line carrying 'CSP violation report' is filtered before every arm", linked to RD-795, label qa-gate-finding. It is a candidate for a later test-only round, not now.
No code. Then carry on with the Build watch; the turn passes to P on your verdict mail.
-- Tuesday
