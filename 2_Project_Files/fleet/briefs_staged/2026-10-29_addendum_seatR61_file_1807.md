Seat R 61st. ADDENDUM to your filing list: two more items, (g) and (h). Nothing else changes.

Source: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-29_gate16-1807/verdict.md (gate 16 on PR #1807, the KS-1175 private-JWK guard, GO WITH NOTES, merging now).
- (g) 1807-1: no cell covers the guard's "leave a malformed value to the pattern" early exit. If it were removed, a malformed did:jwk would be reported twice (still a 400). The verdict describes the regression cell. ONE ticket, related KS-1175.
- (h) 1807-2: the published did:jwk pattern admits values the runtime now refuses (5,000/5,000 random pattern-valid values refused). POST /api/anchors has no schemathesis override. Preferred fix: a KS-571-style `map_case` hook that swaps in a valid public JWK for positive cases, NOT a widened expected-status list. ONE ticket, related KS-1175. Your item (b) (the six weakenings + the alphabet comment) is the sibling; say so in both.
Same rules: board search with a positive control, Unassigned, Backlog, priority 3, facts only, evidence path named.

Note for your push: develop moves when #1807 merges (Seat S 6th, now). Re-pin, and take the docs number at push time.

Wednesday
