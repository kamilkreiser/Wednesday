## BLUF

**KAM RULED (panel 14:53:38 AEST) on card `secuura-ks386-nothing-to-dispose`: CLOSE — "Record it and finish stop-storing."** This lands in your queue as a Kam-ruled category-1 item; it does not pre-empt the door merges or the gates. The disposal question is CLOSED as moot: `svc_kyc_images` holds 0 rows on local and 0 on demo (s127's measurement, superuser, RLS confirmed off, `users` 25/30 as the non-zero control).

## WHAT TO DO ON KS-386 (board writes now; code at its place in the queue)
1. **Comment on KS-386 now:** the zero-row measurement (both environments, method, control, time), and "disposal closed as moot on Kam's ruling 2026-09-05 14:53".
2. **Correct the ticket's description** to the stop-storing ruling (Kam 2026-08-14: design + stop-storing; the "encrypt under the subject DEK" sentence contradicts it — replace it, do not append a contradiction).
3. **Finish the stop-storing write-path half** on the parked branch `kamilkreiser/ks-386-stop-storing-kyc-images` @ `e1d91c23b` (migration 045 makes the column nullable — nullable, not `''`, s127's reasoning stands): the write path stops persisting the image bytes; a test that proves an upload no longer lands in `svc_kyc_images`; a red-proof predicted before the tamper. Ends at READY FOR QA on its own PR, Peter requested with the one-line reason. **Place in the queue: after KS-800 and KS-802, before the rest of category-1** — unless the door gates return findings, which pre-empt everything.

## HOLDS — unchanged
Nothing deletes anything: the table is empty and stays as it is; no `DROP`, no data migration. Demo untouched. Every round ends at READY FOR QA.

PROVENANCE:
- Kam's ruling `close` on `secuura-ks386-nothing-to-dispose` | `0_Brain/dashboard/data/chat_log.json` 2026-09-05T14:53:38+10:00 and the ruled card — Wednesday's project, not yours | read 2026-09-05 14:54
- The zero-row measurement, the parked branch and SHA, the stale description | s127's wrap 2026-09-05T04:43:34Z — s127's reads | read 2026-09-05 14:54
- KS-386 Backlog P2, assigned Kam, last comment 2026-08-12T11:29Z | Linear GraphQL, read-only, 14:5x | read 2026-09-05 14:54

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 14:54
(checked: "finish stop-storing" against "nothing deletes" — the write path stops storing, the empty table is untouched; "after KS-800/802" against "Kam-ruled" — his ruling closes the disposal question and authorises the work, it does not set its priority above the security items; stated.)
