From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel** (no mail key in this project). A question is a `STOPPED: NEEDS TUESDAY` last line with ONE question.
# BRIEF B306 · SEAT-D4: give Paul browser access to HP Security Manager on Azure by an IP allow-list (card `hpsmpoc-sm-access-for-paul-1020`, option a). Small, one Azure change, then a check. Model Opus (routing C6: a network change on Azure).

**Written by Tuesday directly.** MEASURED = Tuesday read it 2026-10-20 09:2x AEDT with HPSM-POC's own az identity, read verbs only. RELAYED = from a file (path given). Re-read everything at source before acting.

**AUTHORITY (check first, or STOP):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show hpsmpoc-sm-access-for-paul-1020` reads `status: ruled`, choice `a`. Kam's words that started it (live board 2026-10-20 09:15:20, view=tuesday, verbatim): *"as a priority, can you please provide me access that I can forward to Paul for Security Manager on Azure.  Ideally, remove any logon requirement"*. The standing grant for this setup: Kam 2026-10-03 (`0_Brain/learnings/2026-10-03_hp-security-manager-azure-deploy-grant.md` in Tuesday's tree; criteria in `1_Project_Definition/Briefs/2026-10-03_B106_ADDENDUM-1_access-choice-kam-12-24.md`: named identities, never anonymous, no admin port open to 0.0.0.0/0, an IP allow-list is acceptable).

**PAUL'S IP (Tuesday fills at launch from Kam's board message):** `@SLOT:PAUL_IP@`. It must be ONE public IPv4 address. If it is a private range (10/8, 172.16/12, 192.168/16, 100.64/10), a range wider than /32, or not an IPv4 address: STOP.

## REFUSE AT ONCE
- The authority check above does not read ruled `a`.
- `az account show` (under `AZURE_CONFIG_DIR=<project>/4_Credentials/.azure`, which `brief_seat.sh` exports) is not user `kamil@datasec-rd.com`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, subscription "Azure subscription 1" (MEASURED 09:2x: all three). Never `az login`, never another tenant.
- The resource group `hpsm-poc-sm-rg` does not hold VM `vm-hpsm-sm` and exactly one NSG (MEASURED: VM deallocated, Standard_D4as_v5, public IP 52.187.238.167, NSG with NO custom inbound rule).
- Any existing inbound rule on that NSG that allows 7637 or 3389 from any source (MEASURED: none). Someone changed it: STOP and list it.

## THE WORK
1. **Before:** write to evidence the NSG's full rule list (`az network nsg show ... --query securityRules`), the NIC/subnet association (which NSG actually filters the VM's NIC), the VM power state and the DevTestLab auto-shutdown time.
2. **Start the VM** (`az vm start -g hpsm-poc-sm-rg -n vm-hpsm-sm`). Wait for `VM running`. Record the time. The auto-shutdown at 20:00 stays as it is (do not change it; say in STATUS that Paul's access ends at 20:00 each day unless Kam asks otherwise).
3. **ONE inbound rule** on the NSG that filters the VM's NIC: name `allow-sm-7637-paul-1020`, priority the lowest free number above 100 that no existing rule uses, direction Inbound, access Allow, protocol Tcp, source `<PAUL_IP>/32`, destination port `7637` only. **Nothing else:** no 3389, no other port, no `*` source, no change to any existing rule, no new public IP, no DNS, no Bastion change.
4. **After:** the rule list again (exactly one rule added, every other rule byte-equal: assert by program).
5. **Check it works, safely:** from THIS machine (whose IP is not Paul's) a TCP connect to 52.187.238.167:7637 must FAIL (the control that the allow-list excludes others). On the VM, by `az vm run-command invoke` (RunPowerShellScript), confirm SM's service is running and port 7637 is listening locally (`Get-NetTCPConnection -LocalPort 7637 -State Listen`), and that an HTTPS GET to `https://localhost:7637/` returns a status code (record only the code, never the body). If SM does not start, STOP with what you saw.
6. **Paul's login:** confirm a Security Manager user for Paul exists (the project's `.env` names `HPSM_SM_USER_PAUL`; read the NAME's value in-process only to confirm presence, never print it or the password). If no SM user exists for Paul, STOP: creating one is a separate step.
7. **What Kam forwards (write it in STATUS, exact, nothing secret):** the address `https://52.187.238.167:7637/` (say whether the browser shows a certificate warning, from the GET in step 5: self-signed or not), Paul's SM username (as the variable name, `HPSM_SM_USER_PAUL`, for Kam to read himself), and "the password is in the HPSM-POC credentials file under `HPSM_SM_USER_PAUL_PASSWORD`; send it to Paul separately from the link". Plus: works only from his IP; ends daily at 20:00 AEDT when the server stops; how Kam asks to change the IP.
8. **Undo, written down:** the one command that removes the rule, and that the VM stops at 20:00 by itself.

## HOLDS
- Datasec / HPSM-POC only. No message to Paul, HP or any human (Kam forwards). No guest invite. No licence purchase. No change to SM's own settings or users. No 0.0.0.0/0 or `*` source, ever. Never print or write a password or key value.
- 🔴 STANDING HOLD: no HP Restricted document to any AI tool; never open `HP Reporting and Docs/`, the SOW, `2_Project_Files/HP Docs/`, `.local/`, `1_Project_Definition/Source_Documents/`.
- Never delete anything except nothing: this brief deletes nothing (the undo command is written, not run).
- Never `cd`; absolute paths; secrets only in-process.

## STATUS (`/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-20_B306_STATUS.md`)
Step 0 (copy of this brief, `cmp`, sha256) · authority read · identity · before/after rule lists and the one-rule diff · VM start time · the outside-connect control result · the on-VM listen and status code · Paul's SM user present yes/no · WHAT KAM FORWARDS · UNDO · NOT TESTED (Paul's own connect: only he can test it).
**Last line:** `DONE: B306 SM reachable on 52.187.238.167:7637 from <PAUL_IP>/32 only · rule allow-sm-7637-paul-1020 · VM running until 20:00` or `STOPPED: NEEDS TUESDAY` + ONE question.
