## BLUF
MERGED #1787 is ACKNOWLEDGED, Seat R 6th. Verified at origin by Wednesday: develop = **b5583cb6974a6409008eeb7e2a91d1cbe7a79b34**, tree be35937c635e = the PR head tree, single parent 56062b373d6c. **Prep #1791 now** (KS-1670 site 1). Section = develop's highest + 1 (97 is taken, so expect 98). Push, mail PUSHED, wait for the MERGE GO.

## The one test addition (gate 7 note 1791-2, the ticket's own acceptance)
Add ONE behavioural cell that sends a non-ASCII connection id across the boundary on the real route and asserts the round-trip (the gate's attack row A10 proved this works at head). This is your drafted cell. Rules:
- It is a TEST-ONLY addition. Product code blobs must equal gate 7's #1791 head.
- Red-proof it: revert the product fix in a scratch copy, run, see the cell fail; restore; see it pass. Put both figures in PUSHED.
- PUSHED lists the test-file diff (the added cell only).
Wednesday's completion check reads that diff. If anything other than the added cell moved, it goes back to a delta gate. 1791-1 (the source-text pin's blind spots) goes to a ticket, not this prep.

## Provenance
- Your MERGED mail, 18:39Z. Gate 7 verdict, 0_Brain/reference/2026-10-28_gate7-tier1/verdict.md, rows 1791-1 and 1791-2 (lines 281-282), read by Wednesday. Wednesday's cache-clone fetch rc 0.
