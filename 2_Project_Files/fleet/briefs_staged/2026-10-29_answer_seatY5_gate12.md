## BLUF
Gate 12 (tier 1, round 1) on #1801 head 5c158f42adba: **GO WITH NOTES, nothing fix-before-merge.** It does exactly Kam's option b, measured through the real gateway router in front of the real handler at the 3 s bounds: always 201; `keyPending: true` plus the message on all 11 undelivered shapes; `false` with no message on the 3 delivered ones; writes unchanged, 0 DELETE, no 503, no rollback. Your figures reproduced (12/12 x5, 9 failed / 3 passed vs unchanged code, 47/47, check:openapi rc 0).

**Prep #1801 only AFTER Seat R 6th's #1791 is MERGED** (R is prepping it now; one docs renumber at a time). Wednesday mails "your turn" for #1801. Until then, nothing to do.

## Apply at prep
1. **1801-3 (wording):** the commit message's and both html docs' red-proof figure "10 failed / 2 passed" becomes **"9 failed / 3 passed"** (KPC2 also passes on base). Docs only; the commit message cannot be amended on a pushed commit, so say it in the PR body.
2. **1801-1 (one cell, recommended):** pin a key-service answer that has NO `success` field: today it sets the flag, and mutant N3 (`success !== false`) survives all 12 cells. Add ONE cell. Red-proof it: apply N3 in a scratch copy, the cell fails; restore, it passes. Put both figures in PUSHED. The product blobs must equal 5c158f42adba's.
Docs section at prep = develop's highest h2 + 1 (PROVISIONAL 96 is void).

## Not yours (tickets, Wednesday files them)
1801-2 (`keyPending:false` does not guarantee a recorded hash; derive it from `!keyHash`), 1801-4 (the gateway's undeclared `data` field), 1801-5 (no CI runs check:openapi), 1801-6, 1801-7 (rollout note: keyPending is now required in the spec), 1801-8 (KS-1789).

## Your context
If your band arrives before your turn, write the HANDOVER with these two prep items and wrap. A Y 6th runs them.

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate12/verdict.md (BLUF + findings read by Wednesday; probes not re-run).
