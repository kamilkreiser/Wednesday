From Tuesday (the Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.

# BRIEF B1490 | SEAT-D60 (deploy-class, ONE irreversible action): DELETE THE UAT BACKUP COPY DATABASE `hpsmpoc-b1466-pre` ON THE PRODUCT OWNER'S WORD. NOTHING ELSE.

**Level: Opus** (`model-routing.md`, the deploy row used for D59: a hosted, irreversible write is not delegated to a lighter model). Pane `Datasec/HPSM-POC-D60`. No port, no server.

## AUTHORITY (verbatim; the only reason this runs)
- Card `hpsmpoc-uat-backup-copy-delete-1111`, ruled on the live board 2026-11-11 09:20:15 AEDT, option a, verbatim: **"Delete it once I say UAT looks right (I will look today)"**.
- The product owner, typed into the coordinator's terminal on 2026-11-11, read at about 10:51 AEDT, verbatim: **"UAT looks right, delete the backup copy"**.
- Context (RELAYED from `1_Project_Definition/Briefs/2026-11-10_B1466_STATUS.md`, read its lines 16, 175, 198 and 216 to 232 whole): the copy was made 2026-11-10 11:03:33Z to 11:05:43Z by `az sql db copy -n hpsmpoc --dest-name hpsmpoc-b1466-pre ...` on server `sql-hpsmpoc-uat-25onzn` in resource group `hpsm-poc-uat-rg`, as the way back for that deploy; the deploy finished cleanly (audit rows 95 = 95 = 95). It is billed while it exists. The platform's own point-in-time restore of `hpsmpoc` remains (restore point T0 2026-11-10T11:03Z).

## THE ONE WRITE
`az sql db delete --resource-group hpsm-poc-uat-rg --server sql-hpsmpoc-uat-25onzn --name hpsmpoc-b1466-pre --yes`, exactly once, after every REFUSE below reads clear. **The name `hpsmpoc` (the LIVE UAT database) never appears as the `--name` of any write**; a command line holding `--name hpsmpoc ` or `-n hpsmpoc ` (with the space, i.e. the live name exactly) is a STOP before it runs (check it by program on the exact string you will run; control: the delete line above passes; a planted `--name hpsmpoc --yes` is caught).

## IDENTITY AND READS (first, before anything)
- Run every `az` with `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure'` exported (the project's own identity, as D59 did). Never open `4_Credentials/.azure-sp` or any other credential file; print no token or key.
- **Identity pass** (as D59's `identity_pass1466.sh`; you may `cp` and adapt it from `.tools/b1466/` into `.tools/b1490/`, never edit the original): `az account show` must read subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, name `Azure subscription 1`; control: the same with `AZURE_CONFIG_DIR=/nonexistent` fails. Print the user only as its domain part.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, nothing written)
1. Identity pass fails, or any `az` read errors in a way you cannot name.
2. `az sql server list -g hpsm-poc-uat-rg --query '[].name'` is not exactly `["sql-hpsmpoc-uat-25onzn"]`.
3. `az sql db list -g hpsm-poc-uat-rg -s sql-hpsmpoc-uat-25onzn --query '[].name'` is not exactly the set {`hpsmpoc`, `hpsmpoc-b1466-pre`, `master`} (RELAYED from B1466 STATUS line 198).
4. `az sql db show ... -n hpsmpoc-b1466-pre --query '{created:creationDate,status:status}'` does not show a creation time between 2026-11-10T11:03Z and 11:06Z, or its status is not `Online` or `Paused`.
5. The live database `hpsmpoc` is not `Online` (`az sql db show ... -n hpsmpoc --query status`), or a UAT health GET fails BEFORE the delete: API `/health/ready` and web `/api/health` must each read HTTP 200 (hosts: read them from B1466 STATUS or `az webapp list -g hpsm-poc-uat-rg --query '[].defaultHostName'`; GETs only; never print a host into any record a client reads).
6. Another pane runs a kit that writes Azure in `hpsm-poc-uat-rg` (read each live `Datasec/HPSM-POC-*` pane's kit line 1).
7. The time is past 13:00 AEDT 2026-11-11 (HARD STOP for starting the delete; reads may finish).

## AFTER THE DELETE (reads only)
- `az sql db list ...` reads exactly {`hpsmpoc`, `master`} (control: the before-list printed above held the copy).
- `az sql db show ... -n hpsmpoc --query status` reads `Online`.
- UAT health GETs again: API `/health/ready` 200, web `/api/health` 200.
- The activity log for the resource group since your Step 0 (`az monitor activity-log list -g hpsm-poc-uat-rg --start-time <your Step-0 UTC>`): exactly the one `Microsoft.Sql/servers/databases/delete` on `hpsmpoc-b1466-pre` from your identity, and no other write. Print the operation names and resources (no tokens).
- Whether the deleted database is listed as restorable (`az sql db list-deleted -g hpsm-poc-uat-rg -s sql-hpsmpoc-uat-25onzn --query '[].name'`): record what it reads, as information only.

## HOLDS
No other write of any kind: no deploy, no app setting, no firewall rule, no restart, no SQL connection to any database, no Jira, no GitHub write, no mail, no message to any human. Never `cd`; absolute single-quoted paths (`!CODING` holds a `!`). `/usr/bin/grep -i` with a positive control for every count. Never print a credential.

## STATUS AND LAST LINE
`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-11_B1490_STATUS.md`: BLUF, AUTHORITY (copied), Step 0 (`date`, pane, model, this file's sha256 after a `cp -n` into Briefs and `cmp`), identity pass, REFUSE table with every print, the exact delete command as run with its rc and output, the after-reads, the activity log, NOT TESTED, Corrections, FOR TUESDAY (one line for the records pass: what to record in the next HPSM C-entry). **Last line exactly one of:** `DONE: B1490 hpsmpoc-b1466-pre deleted <UTC time>; databases now hpsmpoc, master; UAT health 200/200` | `STOPPED: NEEDS TUESDAY <one question>`.

## Stamp
- STAMP: written whole by Tuesday s265, completed 10:51:50 AEDT 2026-11-11 (`date`); facts relayed from B1466 STATUS lines 16, 90, 163, 175, 198 (read at 10:51 by grep); the two authorities quoted verbatim from the live board (reconciled RULED a at 09:20) and Kam's terminal line.

READ-WHOLE-BY-TUESDAY: DONE 10:51 by Tuesday s265 (written and read by Tuesday)
