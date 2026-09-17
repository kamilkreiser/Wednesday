Wednesday -> Seat A 8th successor (Secuura/Blockchain)

## BLUF
**#1032 KS-1194 round 2 @430672697: the gate returned GO WITH FINDINGS (15:57:36Z). The MERGE WAITS FOR KAM'S TAP.** A card is on his panel (`secuura-ks1194-1032-round2-merge-tap`). Do NOT merge #1032 on this mail. If Kam says merge, a separate signed `GO: #1032` quoting his tap will reach you.
**Finish the #1035 GO steps first.** Then, as tickets independent of #1032's merge, file the items below.

## Recommendation (after #1035's MERGED receipt and the KS-1101 push, or during a wait)
1. **KS-1194 comment (N-1, Minor, TICKET-ON-KS-1194):** "residual (ii), raise NOT landed: two consecutive pool acquisition faults (the pre-auth lookup or the UPDATE, then the re-read) leave the request APPROVED over an unraised level with a 503 'could not be confirmed'. The reviewer's retry and reject answer 400 'Request already APPROVED'; only the subject's resubmit recovers. Deterministic for a plaintext-PII row under a production-like NODE_ENV and for a destroyed subject DEK. Round 1 reached the same stored state under the same two faults. Fail-safe: no level is granted. The 'if you already succeeded' wording plus the 400 steer a reviewer to a false belief." Also note residual (i) (fail → ok → fail, same end state) and the F-3 gaps (no cell fails the pre-auth lookup with the re-read; the seat's two files are red 3/17 under NODE_ENV=production).
2. **FILE E-1, a new ticket** (search first by `tenantManager.getPool` / `query(`; Backlog; our account; related KS-1194): "tenant-pool statements carry no tenant GUC: with MULTI_TENANCY_ENABLED and fail-closed RLS, every approve's level UPDATE matches 0 rows (develop answers a false 200 APPROVED at basic)". Evidence class: MEASURED on the real db.ts + TenantPoolManager with pg faked and RLS MODELLED; the RLS premise is unverified; latent per the bicep read (multi-tenancy unset). Severity: Major while that configuration runs.
3. **FILE N-2, a new ticket** (search first; Minor; related KS-1194): "approving a stale PENDING ENHANCED request after the user's level rose to HIGH answers 200 and stores ENHANCED: a downgrade", on head, round 1 and develop. PROBED; its cause (concurrency or ordering) is unmeasured.
4. Mail the three ids with your next STATUS or the MERGED receipt.

## Detail
- Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1194-1032-430672697-tier1-r2/report.md` (§4 and §14 hold N-1's measurements).
- Merge addendum for Kam's tap, whenever it comes: squash `430672697` onto develop `3961c2add` (merged tree `522fc6606`); KS-1194 `contributes` only; KS-1194 stays In Progress (§5f); equality targets users.ts `3bfa47dcd` / ks1194 test `703c80dca` / round-2 test `b79cddd65`; auth 66/779.
