BLUF. **Kam has given GO on the live gate fix b-tight.** Apply it now, following the procedure in HANDOVER-S43 S1 ("LIVE DEMO BLOCKER") and S43's READY-TO-APPLY (09:37:59Z).

## Kam's words (typed into Tuesday's terminal, 2026-09-13 20:4x AEST, verbatim)
> "You have my go-ahead on the live side fix and make sure that you include the credentials in the testing document harness."
- "live side fix" is dictation for **live site fix**: the gate fix b-tight Kam was asked about on his panel at 19:24:59 and 19:39:17. He was told it keeps Basic on everything except the app's own `/api` calls, which keep their bearer check.
- The second half of his sentence is about the QA harness documents. **It is Tuesday's to handle, not yours.** Do nothing with credentials beyond what the procedure below already uses.

## The procedure (HANDOVER-S43 S1, unchanged)
1. **Head mail to Tuesday first:** the apply is starting, there is no SHA change, and the rollback target is the backed-up Caddyfile. Tuesday warns Kam. Start **without** waiting 5 minutes: this is a graceful reload taking seconds, and Kam asked for it.
2. **Identity check.** No `az` is needed for this change. Never touch `datasec-sales-portal-rg`.
3. `bash <S43 scratchpad>/gate/apply-azure-gate.sh <S43 scratchpad>/gate/Caddyfile.b-tight`. It backs up to `/opt/hpsm/Caddyfile.pre-s43-<UTC>`, validates inside `hpsm-caddy`, writes in place (same inode) and runs a graceful `caddy reload`.
   - **If the S43 scratchpad copies are missing** (`/private/tmp`), use the committed copies at analysis `a8651e8`, `qa-s43/gate-blocker/`. Say which you used.
4. **At once, through the PUBLIC URL (never a tunnel):**
   - `browser-gate-check.mjs`, which **must PASS**: sign in, S1, open one engagement;
   - the curl set: `/`, `/api/healthz`, `/api/openapi.json`, `/idp/users`, `POST /idp/token` and the traversal set all answer 401 Basic; `/api/dashboard` without a bearer answers 401 Bearer;
   - `azure/smoke.sh`.
5. **Any failure: ROLL BACK FIRST** with `rollback-azure-gate.sh Caddyfile.pre-s43-<UTC>`, then report.
6. **REPORT mail:** each check with its result, the backup file name, and what Kam can now do through the public URL (which engagement to open: Azure A `3bb6fcb2…`, B `a9101d3f…`).

## Sequencing against your merges
- **The gate apply goes FIRST.** If step 6 (the upgrade) comes due while the apply is in progress, the upgrade waits.
- It touches nothing in the repo and no stack except the Azure VM's Caddy. pc-lane-a has no Caddy.
- No engagement or tenant is created or changed. Kam is testing.

## After your REPORT
Tuesday tells Kam he can use the site, and commissions the re-run of the LIVE half of the acceptance gate. Nothing is owed from you for that.
