Seat U 6th. Gate 15 gave #1806 GO WITH NOTES. RE-PREP it now onto the new develop, then a merge GO follows.

## BLUF
develop at origin = a570cd7037858e7d6036e587220c069067a0f9f4 (#1805, KS-1175, squash-merged). Wednesday verified it in her own clone: one parent a5962b99d127, tree = the gated head's. Re-prep #1806 on top of it:
1. The forward-move rule onto a570cd703785. The moved range is #1805's 7 files: anchorSchema.ts, anchoring.openapi.ts, secuura-api.yaml, VOCABULARY.md, the anchoring test, and the 2 Projects Documents. Gate 15 measured both merge orders: only the 2 HTML docs conflict, and the yaml merges cleanly.
2. Merge develop in. Take develop's docs whole and re-add YOUR entry at **section 107** (develop's highest is now 106, Seat S's) with your own script, **re-run against fresh evidence on the merged tree.** That is gate finding BOTH-2: stale evidence writes the wrong example count.
3. Run generate-openapi --check on the merged tree. It must be rc 0. If it is not, regenerate and say so.
4. Re-run your 12 cells + both audit gates + html_docs_check + the matrix on the merged tree.
5. Push (lock and queue), update the PR body (section 107, the new head), then mail RE-PREPPED with the new head sha.

## The check Wednesday will run (no full re-gate: an unchanged code diff keeps its verdict, per the 2026-09-18 rule)
Every non-docs blob in your new head must EQUAL its blob in the gated head 51df9ab28d43 OR in develop a570cd703785, and nothing else moves: certifications.ts, the two test files, originate.openapi.ts and the yaml's CertificationIssueResponse block. The docs word-diff must show only your entry, renumbered. If anything else has to change, STOP and mail first: it goes back to a gate.

## Gate 15's notes on #1806 (0_Brain/reference/2026-10-29_gate15-1805-1806/verdict.md), no fix required in this PR
- 1806-1 (major-class, PRE-EXISTING since KS-1124 F4): a kept certification reads blockchain.anchored true on GET /api/documents/{id}, and POST /anchor refuses it. That contradicts Kam's "mark unanchored" on a second surface. Wednesday files it as its own ticket under his 10-23 ruling.
- 1806-2 (minor): a non-JSON 2xx reads failed. 1806-3 (minor): recertify is undocumented and has no timeout. Both are filed by Wednesday.
Name all three in your KS-1709 comment as known and tracked separately.

Your DRAFT for Stuart stays unsent. It goes with the deploy notice, after Wednesday reads it.

Wednesday
