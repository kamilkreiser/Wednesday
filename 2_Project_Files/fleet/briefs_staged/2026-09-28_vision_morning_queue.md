# BLUF — MORNING QUEUE for `Datasec/Vision_Sales_Portal`: seven agent-actionable VSP tickets, worked one at a time to READY FOR QA, most severe first. Nothing merges or deploys on your own word; each READY goes to a QA gate, then Tuesday's GO. Portal main at origin = `0d992e0` (VSP-65 merged 2026-09-28, NOT deployed; the deploy is Kam's card).

## AUTHORITY
Kam's standing morning-sweep grant (2026-08-12): a project with agent-actionable tickets gets its agent launched and briefed without a per-morning ask. The v1.3 signature classes still pause (production, money, external comms, anything irreversible).

## THE QUEUE (board read by Tuesday at this brief: 9 open, `board_count.sh`, a real count; VSP-65 and VSP-67 are NOT yours)
1. **VSP-66 (gate 9 VSP65-O1, Major, pre-existing):** a link death while a `pool.connect()` caller holds its client raises an uncaughtException. `server/db.js` + the six `pool.connect()` callers (gate 9 listed them). Tier 1 (every DB call goes through db.js).
2. **VSP-71 (gate 10 R2-O1, Low):** the guarded `CREATE INDEX` in `server/schema.sql` can fail a boot when `IDX_session_expire` is missing. The gate's fix shape: index creation must not be able to fail the boot (catch insufficient_privilege / lock timeout and warn, or a separate statement with .catch(warn)); regression cells named in the gate 10 report.
3. **VSP-70:** dbRestore's ROLLBACK can replace the first error.
4. **VSP-68:** "DB Backup OK" when a whole table is missing from the dump.
5. **VSP-73:** the backup-db SQL dump cannot be replayed into a fresh database (42P01) and carries `session` without its index. (Related to VSP-71's reachable route; say how they interact.)
6. **VSP-69:** the reminder dispatcher is at-least-once (a client reminder can be sent twice). Tuesday has NOT established who is affected: establish what a client receives today and after the fix before building; if the fix changes what a client receives, stop and mail.
7. **VSP-72:** two first boots on an empty database race (23505). Pre-existing at main; ask whether it is worth fixing before building.
Batching: send READYs as they land; Tuesday gates them in batches of disjoint files (Kam's 2026-09-18 minimise-duplication rule). Tell Tuesday which files each ticket touches in its READY.

## STANDING LINES
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything; every READY carries a PRIOR WORK section.
- Red-first with a control that can fail; the gate 9/10 instruments are the reference for DB stalls (`Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/evidence/tools/`), read, never written into.
- READY FOR QA to tuesday-agent@: branch + head sha off current main, ticket, sets not counts, files touched, PRIOR WORK, NOT TESTED, tier.
- Local Postgres on 127.0.0.1:5433, your own databases only; never the live portal, never `datasec-sales-portal-rg` beyond reads you already hold.
- Do not write to the T9 vault clone (Tuesday 2026-09-27); if your launcher does it at boot, say so and do nothing more there.
- No merge, deploy, production change, money, or mail to any human. Client-facing text goes on the ticket only. Datasec seats are retired BY HAND: wrap to tuesday-agent@.

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` and start VSP-66 without waiting.

RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp65-production-deploy: on his board, unruled (default hold). Not yours.
- vision-prod-postgres-idle-transaction-timeout (VSP-67): on his board, unruled (default no change). Not yours.
- vision-gh-login-for-ci = (a): his hands; CI stays UNMEASURED until then.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-27: no writes to the T9 vault clone.
- 2026-09-28: VSP-65 merged by fast-forward; the deploy waits for Kam.

PROVENANCE:
- open tickets VSP-65..VSP-73 (9, Backlog) | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/board_count.sh jira (Vision's own .env) + a Jira search read | read 2026-09-28 06:00
- portal main 0d992e0 | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files | read 2026-09-28 06:00
- VSP-71 fix shape | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md FINDINGS INDEX | read 2026-09-28 02:4x
Self-check note: seven tickets, none Kam-class except the stop on VSP-69's client effect; VSP-65/67 excluded by name.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 06:01
