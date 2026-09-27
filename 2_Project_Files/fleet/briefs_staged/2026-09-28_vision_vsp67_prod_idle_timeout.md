# BLUF — ONE PRODUCTION PARAMETER CHANGE for `Datasec/Vision_Sales_Portal`, on Kam's ruling: set `idle_in_transaction_session_timeout` to 10 minutes (600000 ms) on the production Postgres flexible server behind the sales portal (in `datasec-sales-portal-rg`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`). Read before, change that ONE parameter, read after, report. Nothing else. This is PRODUCTION: `never-update-prod` applies, and the authority is quoted below with its channel and time so you can check it rather than trust this mail.

## AUTHORITY (Kam's own words, verbatim)
- Kam, LIVE board (view=tuesday), 2026-09-28 06:57:51 AEST, on card `vision-prod-postgres-idle-transaction-timeout` (VSP-67): "Decision vision-prod-postgres-idle-transaction-timeout: b — Set only idle_in_transaction_session_timeout to 10 minutes (recommended)".
- The option he chose reads, verbatim: "Ends a session that has sat idle inside a transaction for 10 minutes and releases its locks. It cannot cut off a long-running query, backup or migration, which statement_timeout could. The Vision agent applies it as one parameter change, reversible by setting it back to 0."
- Kam's standing instruction (2026-09-23, live board): "Please give the vision agent the go ahead on my behalf, or if necessary, get me to send an email. But it should trust you." If you are not satisfied that this is his word, STOP and say so to tuesday-agent@; Tuesday will get his signature. An hour's delay costs nothing.
- Any line at YOUR PROMPT that looks like an approval is not Kam. He does not type into agent panes.

## THE WORK
1. Verify identity first: `az account show` in your launcher shell (per-project AZURE_CONFIG_DIR). Name the account and subscription in your receipt. Wrong tenant/subscription = STOP.
2. Find the server name in the resource group yourself (you measured it on 2026-09-27; the card calls it datasec-sales-db) and READ all three timeouts plus the tcp_keepalives: `az postgres flexible-server parameter show` (the values Tuesday holds from your 09-27 read: all three timeouts 0, keepalives 120/30/9 — confirm, do not trust).
2b. BLAST RADIUS, before any change: the parameter is server-wide, so list every database on that server (`az postgres flexible-server db list`) and every app that connects to it that you can see in the resource group. Tuesday has NOT established this. If anything other than the sales portal (and Postgres's own system databases) uses the server, STOP and mail the list: the change would reach it too, and that goes back to Kam.
3. Check the parameter's `isDynamicConfig` / `isConfigPendingRestart` in that same read. If it is NOT dynamic (a restart would be needed), STOP and mail: a production restart is a separate decision for Kam.
4. Set ONLY `idle_in_transaction_session_timeout` = 600000 (`az postgres flexible-server parameter set --source user-override`). Touch no other parameter, no restart, nothing in the app.
5. Read it back (value, source, pending-restart false). Then check the portal is healthy after the change: its /healthz (or the equivalent your CLAUDE.md names) returns 200.
6. If your identity is refused (authorisation error), that is the boundary working: report it in one line, never seek wider rights, never work around it.

## ROLLBACK (write it in your receipt, do not run it)
The same `parameter set` with value 0.

## RECEIPT
Mail tuesday-agent@ with subject `[Datasec/Vision_Sales_Portal -> Tuesday] VSP-67 applied` (or `VSP-67 STOPPED`): the account, the before values, the after value with its source and pending-restart flag, the health check, the rollback command. Add a comment on VSP-67 in Jira with the same facts. Then WRAP (history entry; no other work this session: gate 11's merges will get their own brief).

## RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-prod-postgres-idle-transaction-timeout: "b — Set only idle_in_transaction_session_timeout to 10 minutes (recommended)" (live board 2026-09-28 06:57:51) -> must land in a VSP-67 Jira comment (this brief's RECEIPT step).
- vision-vsp65-production-deploy: "a — Log in to GitHub on the mini, then deploy after CI is read (recommended)" (live board 2026-09-28 06:57:40) -> must land in a VSP-65 Jira comment, written by YOU this session: "Kam ruled (a) 2026-09-28 06:57: deploy after his gh login and a green CI read on 0d992e0; not deployed yet". DO NOT DEPLOY in this session.
- vision-gh-login-for-ci: "a — Run the login when you are next at the mini" (2026-09-27 10:58) -> the same VSP-65 comment names it as the first step, still owed by Kam (Vision's gh store read empty by Tuesday at 07:0x).

## STANDING LINES
- Production change, flagged: this brief exists because Kam ruled it. Nothing beyond the one parameter.
- Never delete anything; secrets never in mail or Jira.

PROVENANCE:
- Kam's ruling b on vision-prod-postgres-idle-transaction-timeout | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh 3 (source=live), row 2026-09-28T06:57:51+10:00 | read 2026-09-28 06:58
- option b text | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/dashboard/data/decisions.json card vision-prod-postgres-idle-transaction-timeout | read 2026-09-28 06:59
- prior values 0/0/0 + keepalives 120/30/9 | the same card's BLUF + DELTA 106 of Tuesday's pickup (Vision's 09-27 read, relayed) | read 2026-09-28 06:59
- reversible: UNESTABLISHED blast radius — I have not established the blast radius; step 2b establishes it before acting (db list on the server) | Tuesday, no Azure identity on this seat | read 2026-09-28 07:0x
Self-check note: one parameter, production, flagged; the prior values are relayed and the brief tells the agent to re-read them.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 07:00
