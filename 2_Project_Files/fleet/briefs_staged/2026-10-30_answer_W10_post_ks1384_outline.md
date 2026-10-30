Seat W 10th

## BLUF
Post ONE comment on KS-1384, the text below VERBATIM, as a reply to Stuart's comment 50294791 (threaded if Linear allows, otherwise top-level), facts only, no @ mention. Read it back by id (body equal, 0 mention nodes, state/priority/assignee unchanged) and mail the comment id. Then carry on with F0.

## Authority
Kam, live board 2026-10-30 12:58:16 AEDT (view=wednesday), verbatim: "Rather than giving him a date, can you please post an outline of our proposed appproach and tell him that we will update him when progress is made". This is Kam's own instruction to communicate to Stuart on the ticket; it sits on his card secuura-ks1384-stuart-asks-a-date-1030. Post nothing else to Stuart or Peter.

## The comment text (verbatim; do not edit the claims; if any sentence is false against your re-cited code or the design rev 4, STOP and mail before posting)
----- begin -----
**Thanks, Stuart. Our approach for KS-1384, in two stages. No date yet: we will update this ticket as each stage makes progress.**

**Stage 1: make today's one-anchor-per-document model safe (in build now).**
- The reconciler stops giving up too early: it judges a row by its last update, not its creation time, and it no longer fails a row because the chain provider was unreachable (KS-1808, KS-1810).
- Anchoring stops a refused or retried event from paying twice or getting stuck: every attempt for one event spends the same wallet coin, so at most one of them can land on chain.
- A sweep ends a stranded row honestly as `failed` instead of leaving it pending, and never mints.
- The retry route checks anchoring's own row first: an attempt still in flight answers 409 and nothing new is posted.
- These parts deploy together on each box, after a wallet check.

**Stage 2: one anchor per lifecycle event (the fix for what you describe above).**
- Each event (upload, version, share, transfer, and so on) gets its own anchor row and its own transaction, so S can name the transaction for each event rather than the document's first one.
- This needs a database migration and a backfill, and it follows stage 1.

**On your verify observation** (verify-by-hash reporting an anchor id as confirmed while that id's own row reads failed with a different transaction): noted, and we are tracking it as its own item.
----- end -----

Wednesday
