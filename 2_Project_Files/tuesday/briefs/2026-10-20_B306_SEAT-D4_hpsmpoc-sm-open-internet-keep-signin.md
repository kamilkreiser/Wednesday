From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel** (no mail key in this project). A question is a `STOPPED: NEEDS TUESDAY` last line with ONE question.
# BRIEF B306 (final form) · SEAT-D4: open HP Security Manager's web console on Azure to the internet so Paul can use it from anywhere, KEEPING Security Manager's own sign-in. One Azure rule, a VM start, and checks. Model Opus.
**This supersedes `2026-10-20_B306_SEAT-D4_hpsmpoc-sm-access-paul-ip-allowlist.md` (never launched).**

**AUTHORITY (check first, or STOP):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show hpsmpoc-sm-open-without-ip-1020` reads `status: ruled`, choice `a`. Kam, live board 2026-10-20, verbatim, in order: 09:15:20 *"as a priority, can you please provide me access that I can forward to Paul for Security Manager on Azure.  Ideally, remove any logon requirement"* · 10:05:45 *"can you relax the security requirements?  no IP"* · 10:07:02 card `hpsmpoc-sm-open-without-ip-1020` = **a**, *"No IP limit, keep Security Manager's sign-in (recommended)"*. It narrows the 09:38 card (c "no logon"): **Security Manager's sign-in STAYS ON. Change no Security Manager setting.**

## REFUSE AT ONCE
- The authority check does not read ruled `a`.
- `az account show` (under `AZURE_CONFIG_DIR=<project>/4_Credentials/.azure`, exported by `brief_seat.sh`) is not user `kamil@datasec-rd.com`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, subscription "Azure subscription 1" (MEASURED by Tuesday 09:2x: all three). Never `az login`, never another tenant.
- Resource group `hpsm-poc-sm-rg` does not hold VM `vm-hpsm-sm` (MEASURED: deallocated, Standard_D4as_v5, public IP 52.187.238.167) and the NSG filtering its NIC.
- The NSG already has an inbound rule for 7637 or 3389 (MEASURED 09:2x: no custom inbound rules). Someone changed it: STOP and list it.

## THE WORK
1. **Before:** evidence of the NSG's full rule list, which NSG filters the NIC (NIC-level or subnet-level), the VM power state, the auto-shutdown time.
2. **Start the VM** (`az vm start -g hpsm-poc-sm-rg -n vm-hpsm-sm`); wait for `VM running`; record the time. Auto-shutdown at 20:00 stays unchanged.
3. **ONE inbound rule** on the NSG that filters the NIC: name `allow-sm-7637-internet-1020`, the lowest free priority above 100, Inbound, Allow, Tcp, source `Internet`, destination port **7637 only**. Nothing else: never 3389, no other port, no change to an existing rule, no new public IP, no DNS, no Bastion change.
4. **After:** the rule list again; exactly one rule added; every other rule byte-equal (assert by program).
5. **Checks:** (a) from this machine, an HTTPS request to `https://52.187.238.167:7637/` gets an answer: record the status code, the page TITLE and whether the certificate is self-signed (no body beyond the title); (b) the page that answers is Security Manager's SIGN-IN page (the title or login form proves it), i.e. the console is NOT reachable without credentials: say how you know; (c) a TCP connect to `52.187.238.167:3389` FAILS (RDP stays closed); (d) on the VM via `az vm run-command invoke` (RunPowerShellScript): SM's services running, 7637 listening.
6. **Paul's sign-in:** confirm the SM user `HPSM_SM_USER_PAUL` (read the value in-process, never print the password; Tuesday read 09:4x: username `hpsm-sm\paul.waite`, password present) exists in SM, without signing in as him. If it does not exist in SM, STOP: creating it is a separate step.
7. **WHAT KAM FORWARDS** (in STATUS, nothing secret): the address, the username, "password: in the HPSM-POC credentials file, sent separately", the certificate warning Paul will see (if self-signed, say what to click), available daily until 20:00 AEDT when the server stops (and how Kam asks for it to be started).
8. **UNDO:** the one command that removes the rule (written, not run).

## HOLDS
- Datasec / HPSM-POC only. No change to Security Manager's settings or users. No message to Paul, HP or any human (Kam forwards). No guest invite, no licence purchase. Never print or write a password or key value.
- 🔴 STANDING HOLD: no HP Restricted document to any AI tool; never open `HP Reporting and Docs/`, the SOW, `2_Project_Files/HP Docs/`, `.local/`, `1_Project_Definition/Source_Documents/`.
- Deletes nothing. Never `cd`; absolute paths; secrets only in-process.

## STATUS (`/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-20_B306_STATUS.md`)
Step 0 (copy of this brief, `cmp`, sha256) · authority read · identity · before/after rule lists and the one-rule diff · VM start time · checks (a)-(d) · Paul's SM user present · WHAT KAM FORWARDS · UNDO · NOT TESTED (Paul's own sign-in: only he can do it).
**Last line:** `DONE: B306 SM sign-in page reachable at https://52.187.238.167:7637/ from the internet · rule allow-sm-7637-internet-1020 · RDP closed · VM running until 20:00` or `STOPPED: NEEDS TUESDAY` + ONE question.
