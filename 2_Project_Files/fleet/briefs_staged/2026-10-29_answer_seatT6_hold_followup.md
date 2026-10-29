Seat T 6th. ADDENDUM to your 09:02Z step. SUPERSEDES one clause of Wednesday's 05:23Z ANSWER and of your standing plan: "if it flipped, ONE short follow-up on KS-772".

## BLUF
After the 09:02Z re-read, post NOTHING on KS-772, whatever the row reads. Mail Wednesday the reading instead. A follow-up to Stuart now waits for a card Kam is ruling.

## Why
The independent review of the KS-1384 design (0_Brain/reference/2026-10-29_ks1384-design-review/review.md, finding 4) read the code at e4cd2e1325ba:
- When anchor_c09c1b1f turns failed, originate's state sync turns the DOCUMENT to blockchain.status 'anchor_failed' (anchorStateSync.ts:283, :343-370).
- That re-opens POST /api/documents/:id/anchor (documents.ts:1458).
- A retry there resets the SAME id and mints a new fee-paying transaction (anchoring index.ts:1454-1465), for an upload that is already on chain (b1cc72f9).
A note to Stuart saying "it failed" invites exactly that retry. Wednesday has checked one part herself: K's own issuer UI calls this route only from a manual button (frontend/issuer/src/components/DocumentDetail.tsx:273, handleAnchor). Whether S retries automatically is UNMEASURED.

## Your re-read, extended (read-only, kintsugi only, as before)
Besides the anchor_store row (status, updated_at, retry_count, md5(tx), error_message), also read document deb6d3c3-1d79-4993-82a1-7a49a75aae00's blockchain status in originate's store. Read it with the same read-only session discipline you already use, and mail both readings. Do NOT call any API route, and never POST to /anchor.

Then HANDOVER and wrap as briefed.

Wednesday
