KS-1263 A partly-completed /share or /transfer-custody is now unattributed: the multi-write is not transactional (share rows or the custody event written, no action_provenance row)
state In Progress
comments at ['2026-09-25T06:17:15.334Z', '2026-09-25T11:04:35.327Z']

## BLUF

**When** `/share` **fails at recipient k > 1, or** `/transfer-custody`**'s owner flip throws after the custody event is written, part of the action has happened but no** `action_provenance` **row exists.** Before KS-1228 (#1043) the same case carried a row, because every refused request did. The root is the pre-existing non-transactional multi-write.

## Recommendation

Wrap the per-recipient `createShare` loop in one transaction, and do the same for the custody INSERT plus the owner flip. Alternatively, record the row when `created.length > 0` before returning the error. Regression cell: two recipients, the second refusing, and the share rows and provenance rows must agree.

## Detail

* **Measured by the batch gate** (the #1043 D table). Each cell reads status · share rows · provenance rows:

| case | develop | head (#1043) |
| -- | -- | -- |
| D1 recipient 2 of 2 → SHARE_TARGET_NOT_FOUND | 404 · 1 · 1 | 404 · 1 · **0** |
| D2 recipient 2 of 2 → SQLSTATE 23503 | 400 · 1 · 1 | 400 · 1 · **0** |
| D3 recipient 3 of 3 → SQLSTATE 22007 | 400 · 2 · 1 | 400 · 2 · **0** |
| D4 recipient 2 of 2 → plain Error | 500 · 1 · 1 | 500 · 1 · 0 |
| C7 transfer: the owner flip throws after the custody event | 500 · 1 | 500 · **0** (the custody event row EXISTS) |

* **Reachability (READ):** `shares` has no foreign key on `recipient_user_id` (`migrations/022_shares_polymorphic.sql:28-48`). Every per-recipient field is validated up front. So a refusal at k > 1 needs a race (the document deleted mid-loop) or a transient DB error. The transfer handler's own comment accepts its window (`services/originate/src/routes/documents.ts` near the custody INSERT).
* **Why it is a trade, not a regression:** #1043 stopped a row being written on every refused request, which was common. The cost is no row on a rare partial one. Develop already answered an error for a half-written share.
* The facts line is on KS-1228. Found by the batch gate `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1042-1045-tier1-r1/report.md` (finding N43-2; the drafter's lead D, confirmed).
* Refs KS-1228.
