From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to B306 (SEAT-D4), answering your STOPPED at 10:30:12.

## ANSWER: YES, add the ONE Windows Firewall rule exactly as you wrote it.

**Authority.** Kam's card `hpsmpoc-sm-open-without-ip-1020` = a (live board 2026-10-20 10:07:02, view=tuesday): "No IP limit, keep Security Manager's sign-in (recommended)". The ruling is that the Security Manager console is reachable from the internet on its own port with its own sign-in. Your measurements show the NSG half is done and Azure passes the packet (`test-ip-flow` Allow), while the VM's Windows Firewall (Public profile, default Block, no rule for local port 7637) drops it. A host firewall rule for TCP 7637 only is the host-side half of the same opening: same port, same exposure, nothing wider. Tuesday rules it inside the card. This is Tuesday's reading; it does not widen what Kam ruled.

**Exactly this, nothing more:**
- Via `az vm run-command invoke` (RunPowerShellScript) under the HPSM-POC `AZURE_CONFIG_DIR`, your command verbatim: `New-NetFirewallRule -Name 'B306-allow-sm-7637-in' -DisplayName 'B306 allow SM console 7637 (Kam card hpsmpoc-sm-open-without-ip-1020=a)' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 7637 -Profile Any -RemoteAddress Any`.
- Before and after: list the firewall rules that name local port 7637 and count all enabled inbound rules. Assert by program that exactly one rule was added and none changed or removed.
- No change to Security Manager, IIS, its users, RDP (3389 stays closed from outside), the NSG, or any other firewall rule. Keep the auto-shutdown at 20:00 untouched.
- Then re-run checks (a) (HTTPS from this laptop, expect an answer with the sign-in page, not 000) and (c) (3389 from outside still closed), and the sign-in check (the console asks for credentials; no session without them).
- Record the undo (`Remove-NetFirewallRule -Name 'B306-allow-sm-7637-in'` via run-command) beside the NSG undo. Do not run it.
- Fill WHAT KAM FORWARDS for real (address, username `hpsm-sm\paul.waite`, "password: sent separately", the self-signed certificate warning and what to click, available until 20:00 AEDT daily and how Kam asks for a start).

**Last line as your brief says** (DONE / STOPPED). If check (a) still fails after the rule, STOP with the measurement; do not try anything else.
