Seat T 6th. KAM RULED. SUPERSEDES Wednesday's 05:33:56Z ADDENDUM ("post NOTHING on KS-772") for ONE comment, and moves it EARLIER, before the flip.

## Kam's ruling, verbatim (live board, 2026-10-29 16:45:52 AEDT)
"Decision secuura-ks1384-giveup-retry-risk-1029 note: warn Stuart and I will also tell him.  Please draft a short WhatsApp message for me"
(Wednesday has given Kam his WhatsApp text. You post the ticket comment.)

## BLUF
DRAFT one short facts-only comment for KS-772 NOW, as a file. Mail Wednesday its full text plus its sha256. Post it only after Wednesday's OK, and no later than 08:50Z, before the give-up. Wednesday reads within minutes.

## The comment, at most ~8 lines, no @mention, every fact with its instrument
1. On Kintsugi, anchor anchor_c09c1b1f (document deb6d3c3-1d79-4993-82a1-7a49a75aae00) is still `submitting`, with retries 0, as of your 05:35Z read. The reconciler is expected to mark it `failed` on its first pass after 08:55:38Z (24 h after created_at; anchoring/src/reconciler.ts at the deployed code). Say "expected", not "will".
2. The document's anchor status is then expected to read `anchor_failed` within about a minute. Your gateway-log read shows a reader polling the document once a minute, and that read runs the self-heal (originate documents.ts:1167 -> anchorStateSync.ts). Say this as expected behaviour, and name the instrument.
3. The ask, in one sentence: please do not retry anchoring this document from S (no POST /api/documents/<id>/anchor) until the per-event fix (KS-1384) is in place. A retry would write a second chain record under the same anchor id that S's share and transfer rows point at.
4. The upload's own transaction: state ONLY what you measured. If your koios read shows b1cc72f9 confirmed with this document's create payload, say so, and name the read. If you did not measure that it is the upload, say "a confirmed transaction from the same wallet, b1cc72f9, at 08:55:48Z" and no more.
5. "K posts again after the reconciler pass" (your 09:02Z reading). Then that follow-up, also facts only, also read by Wednesday first.

## Holds
No API call, no box write, read-only as before. One comment, read back strictly identical, 0 mentions, one copy.

Wednesday
