## BLUF
Kam ruled option **b** at 22:40:59 AEDT on card secuura-ks1240-key-fail-answer-measured-1028: an explicit 'key pending' flag. Tenant creation keeps answering 201. The published response gains a pending flag and a message, and the server writes a log line when the key service fails or answers not-ok. Wednesday had recommended a (log line only). Kam chose b. This is a change to the public API contract, so it is TIER 1.

## How to build it (sequencing is Wednesday's call under v1.3)
1. **#1782 does not change.** It keeps its place in the merge chain (docs section 93) with the fix round you committed locally, exactly as it was gated. Do not fold b into it. Folding b in would re-open a gated head.
2. **Build b as ONE new PR on KS-1240**, stacked on your #1782 fix-round head in your own worktree. Commit locally now if you have room. Open the PR only after #1782 is MERGED and verified at origin. Then base it on develop.
3. **What b contains, and nothing else:**
   - The pending flag and a human-readable message in the 201 body, on the key-service-failed and not-ok paths only. The success path's body is unchanged apart from the new field's success value. Choose the field name and the value on success yourself, and say what you chose in the READY.
   - The server log line on the same paths.
   - The published contract and docs updated to match. Find every surface that publishes the tenant-create response shape, with the search quoted, and name each one.
   - Red-proofs: a cell that fails without the flag on the key-fail path, and a cell that proves the success path's existing fields are byte-identical.
4. **Not in scope (stated so it does not creep in):** a rollback of the key row the key service writes after the caller gives up, and any 503. Kam did not choose c. Your measurement that the orphaned key row is left behind stays a filing item. Search the board before you file it, and quote the search.
5. **The silent success:false path** from your part-4 READY is covered by b's log line. Say so on the KS-1240 ticket in the same comment that records Kam's ruling. Post that comment yourself, BLUF-first, quoting the card id and the choice. That comment is how the ruling reaches an artefact.
6. End the round at READY FOR GATE (tier 1, round 1). No merge without Wednesday's head-pinned GO.

## If you are out of room
If your context or the push queue will not fit this round, say so in a STATUS. Wednesday will put it in the next lane brief for a fresh seat, and #1782 still goes ahead unchanged.

## Provenance
- Kam's ruling: live board message 2026-10-28T22:40:59 AEDT ("Decision secuura-ks1240-key-fail-answer-measured-1028: b — Explicit 'key pending' flag"). Wednesday read it with kam_msgs.sh and recorded it in the decision store with `decision_queue.sh rule` (rc 0, posted to Secuura HTTP 200).
- The card's option text for b ("Keep 201 and add a pending flag and message to the published response plus the log line") was read from `decision_queue.sh show` in this action.
- #1782's chain position (93) and its locally committed fix round come from Wednesday's pickup and your STATUS (10:43Z). Your ks1240_vault_key_trace.md findings are your measurements. Wednesday has not re-run them.
