Seat R 67th

## BLUF
Gate 60 (tier 2 batch, Sonnet, in-session; verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-31_gate60-ks1868-batch/verdict.md`) = **GO WITH NOTES on all three**, no fix-before-merge. **GO: merge them ONE AT A TIME, in this order, each pinned:**
1. #1864 at 76ad178e57d51c0f1af414f5083cab672616caf6
2. #1867 at 437a04ba54f71ea51e31a7d6e78a0bafa67fd17b
3. #1870 at 7388d629ea88851ad82c282c4b217d2b2c727b55
against develop as YOU read it immediately before each merge (last read by Wednesday: 86f80c190f3eb12c08af91d1796aa39a1d3d8bed). The gate measured all three merging cleanly on develop, singly and together, so no merge-prep push is needed: squash at the gated head with `--match-head-commit`. Before EACH merge: re-read the head (must equal the pin) and develop; if develop moved by anything that touches one of the PR's files, STOP and mail; otherwise merge and do the five post-merge reads (one parent = the develop you read, exactly the PR's files, blobs equal the head's, message keys, ticket state). One MERGED mail after all three is fine, each PR's reads in it.

## Notes from the gate (do these after the merges; none blocks)
- **G60-F1 (minor, all three):** the inner try guards a read that throws, not one that RETURNS a non-string: an Error whose `message` getter returns an object with a throwing `toJSON` still reaches the logger as an object, and `JSON.stringify` of the logged meta throws. -> FILE one ticket (board account; board-search first and say what you searched).
- **G60-F2 (file-only):** five inline copies, no shared `safeReason` helper (KS-1868 proposes one) -> one COMMENT on KS-1868 naming the five sites.
- **G60-F4 (file-only, #1864):** `ensureTable` keeps `err?.message` -> fold into the F1 ticket.
- **G60-F5 (#1864 body):** "line 475 at the base" is line 469 at the base (475 is the head line) -> correct that one sentence in the live body, read back.
- **G60-F3 (#1870 body):** the live #1870 body lacks the hook-wording correction note your mail described -> add it, read back.
- PR 4 (mcp-server hash.ts) still waits on #1850 (Seat R 68th's queue).

## Authority
Kam 2026-09-11 16:56 (verbatim): "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested".

Wednesday (rotation seat)
