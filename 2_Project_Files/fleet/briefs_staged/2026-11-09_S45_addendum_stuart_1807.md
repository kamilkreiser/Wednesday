Seat S 45th

ADDENDUM: Stuart's KS-1807 message, relayed by Kam. NEW QUEUE ITEM, ahead of batch 7 filler; merge filings still take priority on a waiter wake.

SOURCE: Kam, live board 2026-11-09 16:17:16 (view=wednesday), relaying Stuart verbatim: "Agreed, KS-1807 closes KS-604. One ask before it does: please open a ticket for the anchoring pages now that KS-1384 stage 1 is on both boxes. They should record your 6 Nov answer: one anchor row per document, and a new paid transaction for every share and lifecycle event until stage 2. It's the part of S<->K that systemTest most needs written down. On the UNDECIDED lines, S has never used the connector revoke route, so my ruling is no on revoke with onBehalfOf. S's answers on documents:revoke, anchors:read and the provisioning-key mint will go on KS-1807." and "I've added this to KS-1807".

ITEM A. File ONE ticket: the platform-k anchoring documentation pages record the CURRENT behaviour after KS-1384 stage 1. Board search first (anchoring docs, "one anchor row", KS-1384, KS-1807's children): a hit that already covers it is a comment, not a ticket. Content (BLUF, facts only, no at-sign):
- What the pages must state: one anchor row per document (per document and network); and, until KS-1384 stage 2, every admitted share and lifecycle event pays its own Cardano transaction on that same row, which then names only the latest transaction.
- The authority, quoted: Kam's card secuura-ks1384-share-pays-second-tx-before-stage2-1106 ruled a (2026-11-06 21:04:52): "Leave it until stage 2 ... Admitted events keep paying one fee each. Nothing is built for this. Stage 2 gives each event its own row." The measurement behind it: KS-1384's 2026-11-06 08:36Z and 08:40Z comments (read them whole).
- Stuart's reason: it is the part of S<->K that systemTest most needs written down.
- Relations: related to KS-1807 and KS-1384. Board account, priority High (2) (Stuart asks for it before KS-1807 closes, and KS-1807 is Urgent). Backlog -> Todo by your state tool. It is a DOCS build item: a build seat writes the pages; you do not.
ITEM B. Read KS-1807's newest comment (2026-11-09T05:09:49Z, Stuart's, "Platform S's answers on the four S-facing UNDECIDED (KS-1807) lines") WHOLE. Do not edit it. Then list, for Wednesday, each UNDECIDED line it answers, with (1) Stuart's answer, (2) the docs file and line that still says UNDECIDED at develop 204e62acdc35 (read by `gh_lines` at that sha), (3) whether any CODE today allows what Stuart said no to (the connector revoke route with onBehalfOf: search the route at develop; say "reachable" or "not reachable" with the line). Send it as ONE file in REC with a one-line STATUS. It becomes a docs build item (and a code item only if (3) finds the route live): Wednesday routes it.
ITEM C. KS-604 is already Done and archived (S 44th, 2026-11-09 03:31Z, on Kam's 'Sent'). Stuart's "KS-1807 closes KS-604" needs no state change on either. Do NOT close or move KS-1807 (Stuart's "before it does": KS-1807 stays open until the anchoring-pages ticket exists and its docs land).

RULED BY KAM, NOT YET IN AN ARTEFACT
- Card secuura-ks1384-share-pays-second-tx-before-stage2-1106 = a (2026-11-06 21:04:52), as quoted above; Item A puts it into the docs ticket.
- Kam 2026-11-06 21:03:31 (live board): "Keep going through the tickets and close and archive as many as you can".

PROVENANCE:
- KS-1807 'Please bring the platform-k docs up to date with current behaviour, so systemTest can be written to the docs': In Progress, priority 1 (Urgent), board account, updatedAt 2026-11-09T05:09:49Z, 15 comments, newest 2026-11-09T05:09:49Z by Stuart | Linear GraphQL, team KS number 1807, read-only, key from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env in-process, comments first:50 sorted newest-first | read 2026-11-09; scope: "Please bring the platform-k docs up to date with current behaviour, so systemTest can be written to the docs"
- KS-604 'BM-5: System-details document for Peter & Stuart': Done, archived 2026-11-09T03:31:50Z | same Linear read | read 2026-11-09; scope: header fields only
- KS-1384 'One anchor row per (document_id, network): a repeat POST /api/anchors resets the existing row to pending': In Progress, priority 2, updatedAt 2026-11-09T05:09:49Z, 28 comments | same Linear read | read 2026-11-09; scope: header fields and the two newest comments' first 400 characters
- Card secuura-ks1384-share-pays-second-tx-before-stage2-1106 (ruled a, 2026-11-06T21:04:52) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show (Wednesday's store, read-only) | read 2026-11-09
- Kam's relay of Stuart | Wednesday's live board read, kam_msgs.sh, 16:17:16 | read 2026-11-09

Wednesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-09 16:18 (Wednesday read this addendum whole; items A-C, the holds and the provenance agree; KS-1807 stays open by Stuart's own words)
