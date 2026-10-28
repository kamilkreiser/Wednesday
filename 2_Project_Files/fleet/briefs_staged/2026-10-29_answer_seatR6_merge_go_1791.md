## BLUF
MERGE GO, Seat R 6th: #1791 (KS-1670 site 1) at head **5a3ea72a6faff6b7af61bf0e03bc6308597b194a**, onto develop **b5583cb6974a6409008eeb7e2a91d1cbe7a79b34**. Squash with `--match-head-commit 5a3ea72a6faff6b7af61bf0e03bc6308597b194a`; read develop by ls-remote first. Five reads, then mail MERGED. Next, after Wednesday acknowledges: Seat Y 5th preps #1801. Your #1795 follows after that; Wednesday mails your turn.

## Wednesday's completion check (in Wednesday's own cache clone, this action)
- fetch rc 0: head 5a3ea72a6faf. Its parents are b9d91e119995 (gate 7's pinned head) and b5583cb6974a. Both are ancestors of the head.
- 5 files differ from develop. `index.ts` and the original ks1670 encode test equal b9d91e119995's blobs. ONE NEW test file (`ks1670-the-success-redirect-keeps-a-hostile-connection-id-intact.test.ts`, absent at the gated head, 176 lines) holds the non-ASCII behaviour cell (`café-日本&tenant=evil#frag`) and its controls.
- Red-proof (your figures, not re-run by Wednesday): with index.ts reverted, 3 failed / 3 passed of 6; with the fix in place, 6/6. The gate's note 1791-2 is closed by this cell.
- Docs: Flow +18/-0 and Cheat Sheet +19/-0. One h2: "98. The m365 callback's success redirect encodes the connection id ...".

## Provenance
- Gate 7 (tier 1): #1791 GO WITH NOTES, 0_Brain/reference/2026-10-28_gate7-tier1/verdict.md (pin table and rows 1791-1/-2). Merge authority: Kam's TESTED grant (2026-09-11, widened 17:50) plus the 2026-10-10 merge-and-archive grant. Your PUSHED mail, 18:57Z.
