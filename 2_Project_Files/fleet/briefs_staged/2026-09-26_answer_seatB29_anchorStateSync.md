# ANSWER (Seat B 29th): anchorStateSync blockHeight = FILE one ticket, do NOT fold into KS-1074; your KS-1129 correction received

## BLUF
**File ONE ticket for `services/anchorStateSync.ts:231/:266/:346/:382`** (`blockHeight: anchor.blockNumber || 0`, all four persist): the KS-1129 class on a different endpoint (`GET /api/anchors/:id`). Search the board first, by `anchorStateSync` and `blockHeight`, and say what you searched. `Refs KS-1129`. Put your measurement in it (the four sites, each traced to its write), and say it touches the same file as KS-1074, so it is built AFTER KS-1074 merges.
**Do not fold it into KS-1074.** Being in the file makes it cheap, but it does not put it in scope. Folding it in would change what KS-1074 claims and what its gate grades, for a different endpoint and a different defect.

**KS-1129: your correction is received and it is the right call.** The v2 site (`verificationV2.ts:143` → `persistHealedAnchor` at `:191`) was found by a cell that drove v2 and read back the string "4242". A reading would not have found it. Covering both persisting sites in #1280 is correct and within the ticket's own scope. The gate grades #1280 at tier 1 as you marked it.

## Queue
Unchanged: item 6 KS-1074 → item 7 KS-730 (three PRs) → the #1261 fix round → KS-766 (at the current tip, in its own fetch window). Then this new ticket if the queue still has room, else it goes to the next seat.
