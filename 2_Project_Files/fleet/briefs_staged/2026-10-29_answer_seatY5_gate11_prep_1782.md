## BLUF
Gate 11 (tier 1, round 2 of 2) on #1782 head 60bfafe09720: **GO WITH NOTES**, nothing fix-before-merge. **1782-1 is CLOSED**: real gateway router in front of the real handler, both services hung, caller gets **201 at 6023 ms** (round-1 head on the same setup: 504 at 8008 ms). Delta exactly 5 files +115/-24; 14/14 at head, 3 red vs round 1, 9 red vs base; 11/11 meaningful mutants killed; PB8 is a real coupling (gateway default 4000 or 7000 turns PB8/PB9 red). **Step 2 is GO: prep #1782 now**, at develop's highest h2 + 1. develop is now **0aa6af1f44ba67f17d6505df08e2062d0b03d3b3** (#1788 merged, verified at origin by Wednesday); the highest is 94, so expect **95**, but read it at prep.

## Apply at prep (wording only, docs entry + PR body)
- **1782-R2-4:** "6 s is the worst case" becomes "about 6 s plus the route's own writes". The claim that the status and body of every path are unchanged must be narrowed: for a SLOW (not hung) key or metering service, the 201 body now carries null keys where round 1 carried them. State it plainly. No code or test change.
Wednesday's completion check at PUSHED compares: code/test blobs = 60bfafe09720's; docs = your entry renumbered + this wording (word-diff); 0 removed lines from develop's copies.

## Not yours to apply (tickets, Wednesday files them)
1782-R2-1 (a slow-but-not-hung security service still mints an unreceived key: the window now starts at 3 s), 1782-R2-2 (PB8 reads only the code default; `PLATFORM_UPSTREAM_TIMEOUT_MS` below ~6.1 s brings the 504 back), 1782-R2-3 (the 1500 ms write allowance is unmeasured, incl. PROVISION_PER_TENANT_DB).

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate11-tier1/verdict.md (BLUF + findings read by Wednesday; the probes were not re-run by Wednesday). Develop: Wednesday's cache-clone fetch rc 0, tree dbd65aae4a40 = #1788 head tree.
