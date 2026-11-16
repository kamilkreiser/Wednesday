From Tuesday (the Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.

# BRIEF B1610 | SEAT-D66 (deploy-class, ONE irreversible action): DELETE THE UAT BACKUP COPY DATABASE `hpsmpoc-b1609-pre` ON THE PRODUCT OWNER'S WORD. NOTHING ELSE.

**Level: Opus** (`model-routing.md` row C6, the deploy row: a hosted, irreversible write is not delegated to a lighter model). Pane `Datasec/HPSM-POC-D66`. No port, no server. A clone of B1490 (SEAT-D60, 2026-11-11), which deleted the previous copy cleanly (`DONE: B1490 hpsmpoc-b1466-pre deleted 2026-11-10T23:54:29Z; databases now hpsmpoc, master; UAT health 200/200`).

## AUTHORITY (verbatim; the only reason this runs)
- Card `hpsmpoc-uat-backup-copy-b1609-delete-1116`, tapped on the live board 2026-11-16 14:29 AEDT, option a, verbatim: **"Delete the copy now"** (ruled in the decision store by Tuesday the same minute).
- Context (RELAYED from `1_Project_Definition/Briefs/2026-11-16_B1609_STATUS.md`; read its P2 w3 line and the 'After the way back' and P3 (g) lines whole): the copy was made 2026-11-16 01:02:58Z to 01:05:08Z by `az sql db copy ... --dest-name hpsmpoc-b1609-pre` on server `sql-hpsmpoc-uat-25onzn` in resource group `hpsm-poc-uat-rg`, as the way back for that deploy. Its snapshot equalled S0 byte for byte. The deploy then landed on UAT and was verified at source (B1609 last line `PARTIAL B1609: DEPLOYED, NOT PROVEN, platform status failed ... while the live predicate passed`, read as deployed by Tuesday's ANSWER-1 item 6). The copy is billed while it exists. The platform's own point-in-time restore of `hpsmpoc` remains (restore point T0 2026-11-16T01:02Z).

## THE ONE WRITE
`az sql db delete --resource-group hpsm-poc-uat-rg --server sql-hpsmpoc-uat-25onzn --name hpsmpoc-b1609-pre --yes`, exactly once, after every REFUSE below reads clear. **The name `hpsmpoc` (the LIVE UAT database) never appears as the `--name` of any write.** A command line holding `--name hpsmpoc ` or `-n hpsmpoc ` (with the space, i.e. the live name exactly) is a STOP before it runs. Check it by program on the exact string you will run. Control: the delete line above passes; a planted `--name hpsmpoc --yes` is caught.

## IDENTITY AND READS (first, before anything)
- Run every `az` with `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure'` exported (the project's own identity, as D60 and D65 did). Never open `4_Credentials/.azure-sp` or any other credential file; print no token or key.
- **Identity pass** (as D65's `identity_pass1609.sh`; you may `cp` and adapt it from `.tools/b1609/` into `.tools/b1610/`, never edit the original): `az account show` must read subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, name `Azure subscription 1`. Control: the same with `AZURE_CONFIG_DIR=/nonexistent` fails. Print the user only as its domain part. Which of the five Datasec environments that tenant is stays UNRESOLVED: assert nothing about it.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, nothing written)
1. Identity pass fails, or any `az` read errors in a way you cannot name.
2. `az sql server list -g hpsm-poc-uat-rg --query '[].name'` is not exactly `["sql-hpsmpoc-uat-25onzn"]`.
3. `az sql db list -g hpsm-poc-uat-rg -s sql-hpsmpoc-uat-25onzn --query '[].name'` is not exactly the set {`hpsmpoc`, `hpsmpoc-b1609-pre`, `master`} (RELAYED from B1609 STATUS P3 (g)).
4. `az sql db show ... -n hpsmpoc-b1609-pre --query '{created:creationDate,status:status}'` does not show a creation time between 2026-11-16T01:02Z and 01:06Z (B1609 recorded created 2026-11-16T01:04:37Z), or its status is not `Online` or `Paused` (it auto-pauses after 60 minutes).
5. The live database `hpsmpoc` is not `Online` (`az sql db show ... -n hpsmpoc --query status`), or a UAT health GET fails BEFORE the delete: API `/health/ready` and web `/api/health` must each read HTTP 200. Read the hosts from `az webapp list -g hpsm-poc-uat-rg --query '[].defaultHostName'`. GETs only; never print a host into any record a client reads.
6. Another pane runs a kit that writes Azure in `hpsm-poc-uat-rg` (read each live `Datasec/HPSM-POC-*` pane's kit line 1).
7. The time is past 16:30 AEDT 2026-11-16 (HARD STOP for starting the delete; reads may finish).

## AFTER THE DELETE (reads only)
- `az sql db list ...` reads exactly {`hpsmpoc`, `master`} (control: the before-list printed above held the copy).
- `az sql db show ... -n hpsmpoc --query status` reads `Online`.
- UAT health GETs again: API `/health/ready` 200, web `/api/health` 200.
- The activity log for the resource group since your Step 0 (`az monitor activity-log list -g hpsm-poc-uat-rg --start-time <your Step-0 UTC> --end-time <now UTC>`) shows exactly the one `Microsoft.Sql/servers/databases/delete` on `hpsmpoc-b1609-pre` from your identity, and no other write. Print the operation names and resources (no tokens).
- Whether the deleted database is listed as restorable (`az sql db list-deleted -g hpsm-poc-uat-rg -s sql-hpsmpoc-uat-25onzn --query '[].name'`): record what it reads, as information only.

## HOLDS
No other write of any kind: no deploy, no app setting, no firewall rule, no restart, no SQL connection to any database, no Jira, no GitHub write, no mail, no message to any human. Never `cd`; absolute single-quoted paths (`!CODING` holds a `!`). `/usr/bin/grep -i` with a positive control for every count. Never print a credential. Never `az webapp show` (it fetches the publish profile).

## STATUS AND LAST LINE
`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-16_B1610_STATUS.md` holds:
- BLUF and AUTHORITY (copied);
- Step 0: `date`, pane, model, and this file's sha256 after a `cp -n` into Briefs and a `cmp`;
- the identity pass, and the REFUSE table with every print;
- the exact delete command as run, with its rc and output;
- the after-reads and the activity log;
- NOT TESTED, Corrections, and FOR TUESDAY (one line for the records pass: what to record in the next HPSM C-entry).

**Last line exactly one of:**
- `DONE: B1610 hpsmpoc-b1609-pre deleted <UTC time>; databases now hpsmpoc, master; UAT health 200/200`
- `STOPPED: NEEDS TUESDAY <one question>`

## Stamp
- STAMP: written whole by Tuesday s282 at 14:30:55 AEDT 2026-11-16; facts relayed from B1609 STATUS (the w3 copy line, 'After the way back', P3 (g)); the authority quoted verbatim from the live board (kam_rulings_today.sh, 14:29) and ruled a in the store.

READ-WHOLE-BY-TUESDAY: DONE 14:30:55 by Tuesday s282 (written and read by Tuesday)
