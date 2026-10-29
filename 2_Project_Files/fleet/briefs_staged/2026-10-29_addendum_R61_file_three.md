Seat R 61st

## BLUF
ADDENDUM: three more filings before your wrap, same discipline as (a)-(h) (board search first with controls, read back, Backlog, P3, no assignee, no @mention). Source: Seat W 7th's KS-1384 design revision, section 16, at /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatW-7th/KS-1384-per-event-anchor-DESIGN-rev2.md (read 16.4, 16.7 and 16.9 there; W 7th's sub-agents found them; they are W 7th's claims until you read the lines).

1. (i) 16.9, SECURITY-class: POST /api/documents/:id/anchor (routes/documents.ts, the retry route) reportedly has no owner, role or revoked-document check (W 7th's lexical count 0 there against 11 in GET /:id; it did NOT check upstream middleware). READ the route and every middleware mounted in front of it at develop 6d41673e0f79 before filing. If an upstream check covers it, file nothing and tell me with the lines. If the gap is real, file it High, label the surface, and say exactly what you read and what you did not run (no request to any box).
2. (j) 16.4, test fidelity: Kam's 2026-09-14 retry cell (ks726-write-ahead-tx-hash.test.ts:414) uses the short text "All inputs are spent"; the node's real text ("All inputs are spent. Transaction has probably already been included", ks705-submission-idempotency.test.ts:48-50) is never paired with a write-ahead + absent re-poll, so the ALREADY_INCLUDED_REPLY clause that makes the ruled retry unreachable is unpinned. Related KS-726, KS-1384. Do not run the mutant unless it is cheap; say which.
3. (k) 16.7: two comments in reconciler.ts W 7th calls false; read them and file only if they are.

If your context does not allow all three, do (i) first, hand the rest over in your HANDOVER, and say so. Keep your worktrees until gate 17 (#1808 + #1809, running now) reports.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-29 21:37
