# DRAFTER COMMISSION — brief for Seat AA 8th (Secuura/Blockchain-AA, demo-pk anchor re-submit: READ FIRST, then a QUESTION)

Written by Wednesday 2026-11-25 (morning). You are a DRAFTER: write ONE brief file and nothing else. You do not launch, mail, or touch any project file outside the output path.

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_seatAA8_demo_resubmit.md`

## Templates (read each WHOLE first)
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatAA6_demo_sign_anchor_failed.md`: the earlier seat on THIS anchor (diagnosis brief; its findings and the KS-2196 fix history live in the Secuura project's 5_Project_History for Seat AA 6th and on KS-2196: find and cite them).
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatD69_demo_catchup.md`: how a seat reaches demo-pk (box access, read-only tooling, the demo rules). Copy its ACCESS and SAFETY sections; do not copy its deploy steps.
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-24_seatD87_kintsugi_k45.md`: current seat-discipline shape (STAMP, provenance table, launcher first-action warning, never-cd/never-rm/MOVE, mail tooling, WRAP).

## Authority (quote verbatim in the brief)
- Stuart, KS-772 comment 2026-11-24T06:01:49Z: "Please re-submit `anchor_c3d42601` on demo-pk. ... Please reply here with the time of the re-submit and its transaction hash, and I will check the rows." Also his KS-2196 comment 2026-11-24T06:05:44Z. Full text: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_stuart_comments.txt`.
- Kam, live board 2026-11-25 06:57:19, a NOTE on card `secuura-demo-pk-anchor-resubmit-1125` (card withdrawn quoting him): "keep working.  I will log in with a new account after usage runs out". Wednesday's reading, told to Kam on the panel with a correction offer: proceed now; read the anchor's state and demo-pk's running commit FIRST; re-submit only if both match Stuart's description, else STOP to Kam.

## Hard sequence (the brief must enforce it)
1. PHASE 0, READ-ONLY on demo-pk and in a scratchpad clone: (a) demo-pk's running commit for anchoring (and originate if it carries the anchor path): is it d4ffc8308249 or later, and does it contain the KS-2196 fix commit 918f5e6d3 (Stuart's claim; UNVALIDATED by Wednesday)? (b) the anchor row `anchor_c3d42601-7f06-44db-89d7-a0c61a1814a7`: status, tx hash(es), retry count, updated_at, and whether ANY tx for it ever landed on chain (preview network: check by its tx hash if one exists; a landed tx means a re-submit would pay a SECOND fee and create a duplicate, the 1107 card's hazard). (c) the re-submit MECHANISM the code offers for a terminal FAILED row: an API/admin route, a reconciler that picks up a status reset, or only a DB write. Name each with file:line at demo-pk's running commit.
2. QUESTION to Wednesday with the Phase 0 facts and the proposed method, its writes (row, chain tx, fee, audit rows), and its rollback. NOTHING is written on demo-pk before Wednesday's GO naming the method. A method that needs a direct DB write on demo, or finds a landed tx, comes back as a STOP: Wednesday takes it to Kam.
3. On GO: the re-submit exactly as GO'd; then watch the row to CONFIRMED (or a terminal state) with time-boxed polls; record the submit time (UTC, from the system, never typed) and the tx hash from the row.
4. The KS-772 reply to Stuart is DRAFTED in the seat's STATUS mail, not posted. Wednesday licenses the post by sha256 of the draft; the seat then posts it, reads it back, and reports the comment id. Facts only: submit time, tx hash, current status; no promise about S's rows.
5. Never: production, prune, any other anchor, any other demo change, any deploy, mail to any human.

## Routing
Model: OPUS (newest; routing row C3: anchoring spends from the platform wallet and the method choice is the work). Lane -AA. Seat name exactly `Seat AA 8th`.

## Return
When the file is written, reply with its path, byte count, and every fact in this commission you could not validate against the source (also marked UNVALIDATED in the brief).
