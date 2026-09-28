# BLUF — `Datasec/Vision_Sales_Portal`: GATE 12 is back. (1) MERGE VSP-69 @ `e79682a` to portal main now. (2) VSP-74 is NO-GO (round 1 of 2): fix ONLY the closure's identifier/schema hole (VSP74-G12-F1) as ROUND 2 — a NO-GO in round 2 goes to Kam, so keep the round tight. (3) Merge that fix forward into VSP-75 and send both READYs for a re-gate. VSP-75 is GO on its own scope but carries VSP-74, so it merges only after the re-gate. No deploy, no production, no Azure.

Verdict: QA/Vision-gate12, 00:55Z, report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets/report.md` (Tuesday read VERDICTS, N1.10, FINDINGS INDEX and THE QUEUE whole). Read those four sections yourself before starting.

## 1. MERGE VSP-69
`fix/vsp-69-dispatch-per-reminder-2026-09-28` @ `e79682a` onto main `609e967` (re-read ls-remote first). Merge commit; `BACKLOG.md` conflict = keep all blocks (the gate measured BACKLOG as the only conflict). `npm test` + `test:db` as SETS vs main, 0 names lost; push; ls-remote; MERGED mail. CI UNMEASURED.

## 2. VSP-74 ROUND 2 — VSP74-G12-F1 ONLY
The closure builds `live` from `pg_tables … schemaname = 'public'` (bare names) and FK edges from `conrelid::regclass::text` (QUOTED for mixed-case names, schema-QUALIFIED outside the search path), so the two never match: a `"QA_Outside"` table with a CASCADE key to leads is announced "leaving QA_Outside as it is" and emptied 2→0; SET NULL rewrites its lead_id; a table in another schema with a CASCADE key to public.leads is emptied with no refusal.
Fix (the gate's shape): compare by OID (or pg_class names), and consider tables in EVERY schema whose FKs reach a restored table: refuse by default, and with --allow-incomplete keep them with their parents.
Red-first cells (the gate's): (i) a capitalised outside table with rows and ON DELETE CASCADE to leads: with the flag it AND leads are kept, rows unchanged; (ii) the same with SET NULL: lead_id unchanged; (iii) a table in another schema with a CASCADE key to leads: the restore refuses. Keep every a1794ad cell green; mutants for each.
**Out of scope for this round (ticket them, do NOT build):** VSP74-G12-F2 (plan/clear window), F3 (child rows dropped by 23503 while the restore says "complete"), P1.

## 3. FORWARD INTO VSP-75, THEN READY x2
Merge the new VSP-74 head forward into VSP-75 (never rebase). Re-run VSP-75's own cells, the §N4 required cell and the §N2.9 deploy-time arms. READY FOR QA for VSP-74 (round 2 of 2, tier 1) and for VSP-75 (new head, tier 1), with suite sets vs main (after VSP-69's merge) and local coverage.

## 4. TICKETS (Jira, BLUF-first; the report's FINDINGS INDEX has fix shapes)
- VSP74-G12-F2 + F3 (+ P1) — one ticket if one test pass proves them.
- VSP69-G12-F1 (Minor): the millisecond JS cutoff defers "due now" reminders one tick; fix shape = keep the cutoff in SQL.
- VSP75-G12-O1: old (pre-VSP-75) backups made east of UTC restore DATEs one day early; O5: backup peak memory ~20x the DB in the web process; O3/O4 test gaps.
- G12-O7 (pre-existing): after a restore, a stale session of a deleted user still authenticates and its id is reused.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp65-production-deploy: "a — Log in to GitHub on the mini, then deploy after CI is read (recommended)" -> on VSP-65 (38520). Not yours: no deploy.
- vision-prod-postgres-idle-transaction-timeout: "b — Set only idle_in_transaction_session_timeout to 10 minutes (recommended)" -> on VSP-67 (38519); waits for his typed line. Not yours.
- vision-gh-login-for-ci: "a — Run the login when you are next at the mini" -> Kam's hands.

## HOLDS
No deploy, no production, no az. Local Postgres 5433, own databases only. PRIOR-WORK CHECK. Never delete; quarantine. The vault clone is Kam's.

PROVENANCE:
- gate-12 verdicts, F1 mechanism, fix shape, findings, merge order | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets/report.md (VERDICTS, N1.10, FINDINGS INDEX, THE QUEUE) | read 2026-09-28 11:0x
- heads e79682a / a1794ad / 41c4a66, main 609e967 | the gate's three ls-remote readings, relayed; re-read yours | read 2026-09-28 11:0x
Self-check note: VSP-69 merges; VSP-74 round 2 is F1 only; VSP-75 waits for the re-gate; the rest is tickets.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 10:57
