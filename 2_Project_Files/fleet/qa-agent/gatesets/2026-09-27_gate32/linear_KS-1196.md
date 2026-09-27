KS-1196 admin POST /api/admin/document-types ids are dt-${Date.now()}: two creates in one millisecond collide and the second silently overwrites the first
state In Progress

## BLUF

Admin `POST /api/admin/document-types` builds the new type's id as `dt-${Date.now()}` (`services/api-gateway/src/routes/admin.ts:682`). Two creates in the same millisecond get the **same id**: both answer 201, and the second **silently overwrites** the first in the Redis catalogue. Measured four times.

## Recommendation

Not built. The fix shape is a collision-free id (e.g. `crypto.randomUUID()`), or a refusal when the key already exists. It matters mostly for scripted bulk creation, and for KS-1190's open question of what the catalogue actually holds.

## Detail

* **Source:** tier-1 QA gate on PR #1014 (KS-1176), finding F-3 (Minor). Report `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014-616c766a5-tier1-r1/report.md`.
* **Evidence:** two census runs each lost one synthetic type (`QA_V_ABSENT` on base, `QA_V_BASIC` on head). An explicit probe produced the same id with 1 type added on two trees, and distinct ids with 2 types on the third (a different millisecond).
* Line re-read at develop `eb1051fd39fe3edab4e0b1d1967515b758d4ba3f`.
* **Related:** KS-1190 (who creates document types, and what the catalogue holds).

### Dedupe before filing

Searched with the board's `searchIssues` (includeArchived, includeComments), keeping only literal, case-insensitive matches:

* `enforceClientRateLimit`: 2 fuzzy, 2 literal (KS-164, KS-170; both archived).
* `rateLimit`: 24 / 24 (none about the mount order of the per-key limiter; nearest KS-947, a different limiter's gate cell).
* `dt-${Date.now()}`: 123 / 0.
* `document-types`: 121 / 14 (KS-1190, KS-1176, and archived catalogue / Akto tickets).
* `verificationLevel`: 25 / 21 (nearest KS-744, a missing claim, not a non-string one).
* `connector-token`: 91 / 1 (KS-695, an incidental mention).
* `connectorMeta`: 1 / 1 (KS-164, archived).

None covers this finding. Related: KS-1176.
