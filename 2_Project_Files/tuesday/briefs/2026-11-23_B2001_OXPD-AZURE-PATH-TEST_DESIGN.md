# B2001 DESIGN: Datasec / OXPd_2, the one Azure test resource for the site-to-Azure path (spike S14, N-5), designed and priced. NOTHING IS CREATED until Kam answers the card in section 6.

Design drafter B2001 for Tuesday (s317), 2026-11-23, written after `date` printed `Mon 23 Nov 2026 19:17:03 AEDT`. READ-ONLY: no `az` command was run; the only network calls were GETs to the public Azure Retail Prices API (raw answers kept in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d2001/*.json`). No secret was opened; `4_Credentials/` and `3_Access_Keys/` of OXPd_2 were LISTED only.

**Authority:** card `datasec-oxpd-site-to-azure-path-1123`, ruled `a` at 2026-11-23T18:30:02+11:00: "Create one small resource in the agent-controllable Datasec environment to measure the path from a printer; cost and tenant on a card first." This file is the "cost and tenant" half. The `az` commands in section 2 and 4 are drafts for a later brief. Nobody runs them until Kam answers the card.

## BLUF

- **One Linux VM, `Standard_B2ats_v2` (2 vCPU, 1 GiB), australiaeast**, with a static public IP and a 32 GiB standard HDD. It lives for **one test window of at most 8 hours**, then the whole resource group is deleted. A VM can't exist without its OS disk, and the public IP is needed because the printer calls in, so "one resource" means **three meters (compute, disk, IP) in one resource group, removed by one delete**.
- **Where:** tenant `d500ebad-cf53-4f2a-a501-f831289e67fc` (environment #5), subscription **`Azure subscription 1` (`0c57ab37-349c-47ae-a10f-e284a380bbb9`)**, new resource group **`oxpd2-s14-path-test-rg`**. `datasec-sales-portal-rg` is never named in any command and is outside the identity's reach.
- **Identity: none exists for OXPd yet.** `OXPd_2/4_Credentials/.azure/` is an empty folder, and the project's `CLAUDE.md` says `.env` holds the Jira login. Kam must create one service principal, `oxpd2-claude-deploy`, with Contributor on the new resource group only. The pasteable steps are in section 2.3.
- **Cost (MEASURED, Retail Prices API, AUD):** VM `0.0169`/hour, public IP `0.0071`/hour, disk `3.4926`/month (about `0.0048`/hour). **Total about AUD 0.029/hour, so AUD 0.23 for the 8-hour window.** Egress is about AUD 0 (the first 100 GB a month is a 0.0 tier). If the VM is forgotten it costs AUD 21.01 a month; with the auto-shutdown included in the design that drops to AUD 8.68 a month.
- **Shape measured:** a **site relay with no inbound port at the site**. Kam's Mac opens an outbound SSH tunnel to the VM, so the server reaches the printer on port 7627 (same number at both ends, no port remap). The printer calls the server directly over the internet by its Azure DNS name (HTTPS, dev-CA certificate). **The admin password never leaves the home network.** The Azure side uses only the Test service's echo calls, which HP's spec says take a **guest** credential.

## 0. What was read (and what was not)

| Source | What it gave |
|---|---|
| `decision_queue.sh show datasec-oxpd-site-to-azure-path-1123` (whole) | The ruling `a` and its detail, quoted above |
| `<OXPd_2>/1_Project_Definition/Design/02_architecture.md` lines 14, 248, 585, 786, 847, 900, R34 (976), N-5 (1264) | Two-way traffic; fixed port 7627; "no NAT remap"; Phase 1 in the client's Azure (W5); the path is open (N-5) |
| `03_plan-of-attack-and-build.md:67` (S14) | Pass condition: "443 and 7627 from the server to the printer, the server's HTTPS port from the printer; OXPd 1.x first" |
| `B1996_OXPD-DESIGN-REVIEW.md` F5 (46), F7 (54), F16 (129), F18 (135), F19 | A name, not an IP (CN must match the host); admin password exposure; route rate limit; undo list |
| `Analysis/C1_oxpd1-platform-specs-sdk.md:79, 93, 283, 315`; `C2_...:7, 108, 154, 201` | 7627 not configurable; "NAT port remapping not supported"; "not a cloud-based SDK"; device calls out from ephemeral ports; registration needs the device IP reachable from the server |
| NAS library `OXPd1-NET-Java/Docs/oxpd-test-service-specification.md` lines 15 to 100 | Test service is off by default and must be enabled after every reboot. `SyncEchoString` and `AsyncEchoString` "may be used in a customer environment for triage". The 403 row: "This method requires either guest (username=guest, password={anything}) or admin" credentials. AsyncEcho failure causes: "firewall", "web proxy", "NAT blocking the callback" |
| `B1968_PRINTER-NEEDS.md` (first-run list 2a, premises) | Mac `192.168.20.220`, gateway `192.168.20.1`. Printer on the same subnet. Step 2 turns on the Test service; step 3 uploads the dev CA. Lockout after five wrong admin passwords |
| `B1997_SEAT-X56_oxpd2-l5.md` header | The lab command `oxpd1` has two verbs, `read` and `lab-cert`. `lab-cert` keeps no CA key (D6). Run folders inside git are refused (D7) |
| `<OXPd_2>/CLAUDE.md` (whole); `4_Credentials/` and `3_Access_Keys/` LISTINGS | No Azure identity. `.azure/` is empty; files present: `.env`, `.gh-config/`, `github_deploy_rw(.pub)` |
| Vault `daily/2026-08-12.md:83` (HPSM precedent) | Same pattern used before: Kam present for a device-code login into the project's `4_Credentials/.azure`, then an RG plus SP "Contributor scoped to the RG only", secret to `4_Credentials/.env`. The boundary was proven by an SP login: "AuthorizationFailed on datasec-sales-portal-rg". Gotcha: "fresh SP needs ~30s AAD propagation" |

**Not read, and why:** live Azure state (no `az` allowed; Tuesday reads it at the card). That includes: whether `Microsoft.Compute` is registered in `0c57ab37` (the workspace `CLAUDE.md` records "zero VMs anywhere in #5" on 2026-08-06), the Basv2 vCPU quota in australiaeast, Azure Policy on the subscription, and whether `oxpd2-s14-path-test-rg` already exists. Also not read: the `.env` values, and the HP test-automation methods' credential requirement (spec lines past 100).

## 1. The resource

| Item | Choice | Why |
|---|---|---|
| Type | One Linux VM (Ubuntu 24.04 LTS, `Canonical:ubuntu-24_04-lts:server:latest`) | Needs a listener on a chosen port, an SSH endpoint for the relay, and the lab tool run as a self-contained linux-x64 build. A container instance (ACI) was considered and rejected: it offers no SSH endpoint for the relay without building an image, and it gives no control over the tunnel. |
| Size | `Standard_B2ats_v2` (2 vCPU, 1 GiB, burstable). Fallback: `Standard_B1ls` (0.5 GiB, AUD 0.0094/hour), if the Basv2 quota is 0 | Smallest current-generation size that runs a .NET self-contained tool and `sshd` with headroom |
| Region | `australiaeast` | Per the commission; it is also the closest to Kam's printer (latency is one of the measurements) |
| OS disk | Standard HDD LRS, 30 GiB (bills as S4, 32 GiB) | Cheapest disk that fits the Ubuntu image. No data disk. |
| Network | New VNet `oxpd2-s14-vnet` 10.214.0.0/24 with one subnet. One NIC. One **Standard static** public IP with DNS label `oxpd2-s14-<4 random chars>` → FQDN `oxpd2-s14-xxxx.australiaeast.cloudapp.azure.com` (the printer needs a NAME: CN must match host, no IPs, C1:93 and F7) | VNet, NIC and NSG have no meter (the API returned no NSG, NIC or VNet row for `Virtual Network` in australiaeast, `vnet_all_aud.json`) |
| Open ports (NSG inbound) | **TCP 22** (SSH, key only, no password auth) and **TCP 8443** (the echo callback listener), **both only from Kam's home public IP /32**. Everything else is denied by default. **Nothing is opened at Kam's home router.** | 8443 instead of 443 so the listener needs no root |
| Life | One window, at most 8 hours, same day. Tags: `project=OXPd_2 purpose=S14-path-test owner=kam expires=<date>`. VM auto-shutdown at 23:00 AEDT (12:00 UTC) as a backstop: it deallocates the VM but does not delete anything. | |
| Teardown | `az group delete -n oxpd2-s14-path-test-rg --yes`. Verified by `az group exists` → `false` and, from the next day, a Cost Management check showing the three meters stopped | One delete removes VM, disk, IP, NIC, NSG and VNet together |

**More than one billable resource?** The design has three meters but no second resource *you would choose*. A site-to-site VPN shape would need an Azure VPN Gateway: a second billable resource at AUD 0.27/hour for VpnGw1 or AUD 0.0512/hour for Basic, plus a VPN-capable router at Kam's home. It is **deliberately not in this test**; see section 5.

## 2. Tenant, subscription, resource group, identity

### 2.1 Placement
- Environment #5, tenant `d500ebad-cf53-4f2a-a501-f831289e67fc` (controller `kreiser.org@me.com`).
- **Subscription: `Azure subscription 1` (`0c57ab37-349c-47ae-a10f-e284a380bbb9`).** It is the general-purpose subscription of #5 (Vision, NexusAI dev, myPKI, backups), and the HPSM precedent put its RG-scoped SP there (inferred from that SP being refused on `datasec-sales-portal-rg`). Alternative: `CypherKey` (`29b5c7de-bbdd-409f-a4a2-30fc9e1ae4a6`). It keeps the VM out of the subscription that holds production, but files OXPd's cost under another product's name. Tuesday may offer it on the card if Kam prefers separation.
- **Resource group: `oxpd2-s14-path-test-rg`** (new, australiaeast). `datasec-sales-portal-rg` (PRODUCTION) appears in no command, and the identity below has no rights on it.

### 2.2 Identity: none exists, so one must be created
OXPd_2 has no Azure identity. `4_Credentials/.azure/` is empty (listed). The project `CLAUDE.md` says `.env` holds "the Jira login", and its rules say "any Azure resource (no `az` command without a brief that quotes his word for it)". Per workspace rule 4, OXPd needs its own service principal confined to its own resource group.

### 2.3 What Kam (the tenant controller) runs, once, after the card is answered
Run in a shell launched from `OXPd_2/Launch_Claude.command`, so `AZURE_CONFIG_DIR` is the project's own folder. Use single quotes around paths: the `!` in `!CODING` triggers history expansion inside double quotes in interactive zsh.

```zsh
# 0. Prove the shell is isolated to OXPd's own az state (must print .../OXPd_2/4_Credentials/.azure)
echo "$AZURE_CONFIG_DIR"
# 1. Log in to environment #5 (device code; Kam completes it)
az login --tenant d500ebad-cf53-4f2a-a501-f831289e67fc --use-device-code
az account set --subscription 0c57ab37-349c-47ae-a10f-e284a380bbb9
az account show --query '{tenant:tenantId, sub:id, user:user.name}' -o table
# 2. Only if Tuesday's card read found Microsoft.Compute NotRegistered (an SP scoped to an RG cannot register it):
#    az provider register --namespace Microsoft.Compute --wait
# 3. The resource group (empty; no cost)
az group create -n oxpd2-s14-path-test-rg -l australiaeast \
  --tags project=OXPd_2 purpose=S14-path-test owner=kam
# 4. The service principal: Contributor on THIS group only. The secret goes straight to a 600 file, never to the screen
umask 077
az ad sp create-for-rbac --name oxpd2-claude-deploy --role Contributor \
  --scopes /subscriptions/0c57ab37-349c-47ae-a10f-e284a380bbb9/resourceGroups/oxpd2-s14-path-test-rg \
  > '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json'
# 5. Check without printing the secret: must list exactly one assignment, Contributor, on the RG
az role assignment list --all --assignee "$(python3 -c 'import json;print(json.load(open("/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/oxpd2-claude-deploy.sp.json"))["appId"])')" \
  --query '[].{role:roleDefinitionName, scope:scope}' -o table
```
The project's agent then logs in as the SP (wait about 30 s for propagation, per the HPSM gotcha) and **proves the boundary before anything else**: `az group show -n oxpd2-s14-path-test-rg` succeeds, and `az group show -n datasec-sales-portal-rg` fails with AuthorizationFailed. That failure is the boundary working; it is reported and never worked around.

## 3. Cost: MEASURED from the Azure Retail Prices API (GET, no key, 2026-11-23 about 19:15 AEDT)

Query base: `https://prices.azure.com/api/retail/prices?currencyCode=AUD&$filter=...`. Raw JSON: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d2001/`.

| Meter | `$filter` | productName | meterName | retailPrice | unitOfMeasure | currencyCode | type |
|---|---|---|---|---|---|---|---|
| VM compute (Linux) | `serviceName eq 'Virtual Machines' and armRegionName eq 'australiaeast' and armSkuName eq 'Standard_B2ats_v2' and priceType eq 'Consumption'` | Virtual Machines Basv2 Series | **B2ats v2** | **0.0169** | 1 Hour | AUD | Consumption |
| (same, in USD, for reference) | same, `currencyCode=USD` | Virtual Machines Basv2 Series | B2ats v2 | 0.0119 | 1 Hour | USD | Consumption |
| Public IP | `serviceName eq 'Virtual Network' and armRegionName eq 'australiaeast' and productName eq 'IP Addresses'` | IP Addresses | **Standard IPv4 Static Public IP** | **0.0071** | 1 Hour | AUD | Consumption |
| OS disk | `armRegionName eq 'australiaeast' and productName eq 'Standard HDD Managed Disks' and skuName eq 'S4 LRS'` | Standard HDD Managed Disks | **S4 LRS Disk** | **3.4926** | 1/Month | AUD | Consumption |
| Disk operations | same | Standard HDD Managed Disks | S4 LRS Disk Operations | 0.0007 | 10K | AUD | Consumption |
| Egress to internet, first tier | `serviceName eq 'Bandwidth' and armRegionName eq 'australiaeast'` | Bandwidth - Routing Preference: Internet | Standard Data Transfer Out (tierMinimumUnits 0) | **0.0** | 1 GB | AUD | Consumption |
| Egress beyond 100 GB/month | same | Bandwidth - Routing Preference: Internet | Standard Data Transfer Out (tierMinimumUnits 100) | 0.1563 | 1 GB | AUD | Consumption |
| Egress, Microsoft routing (default for a Standard IP), beyond 100 GB | same | Rtn Preference: MGN | Standard Data Transfer Out (tierMinimumUnits 100) | 0.1705 | 1 GB | AUD | Consumption |
| Fallback size | `... armSkuName eq 'Standard_B1ls' ...` | Virtual Machines BS Series | B1ls | 0.0094 | 1 Hour | AUD | Consumption |
| Not used (context for section 5) | `serviceName eq 'VPN Gateway' and armRegionName eq 'australiaeast'` | VPN Gateway | VpnGw1 / Basic Gateway | 0.27 / 0.0512 | 1 Hour | AUD | Consumption |

**Arithmetic (AUD):** hourly = 0.0169 + 0.0071 + 3.4926/730 = **0.0288 per hour**.

| Life | Running | Deallocated (auto-shutdown hit: IP + disk only) |
|---|---|---|
| 4 h | 0.12 | 0.05 |
| **8 h (planned)** | **0.23** | 0.10 |
| 24 h | 0.69 | 0.29 |
| 7 days (forgotten) | 4.84 | 2.00 |
| 30 days (forgotten) | 21.01 | 8.68 |

- **Egress:** the test moves kilobytes (echo strings, a discovery XML), and the run folder is copied back once. Well under 0.1 GB. At the 0.0 tier that is AUD 0. Worst case, if other workloads already used the account's 100 GB this month: under AUD 0.02. **Disk operations:** about AUD 0.
- **Not proven here:** that a managed disk is billed pro rata by the hour (the API row is per month). If it is billed as a whole month, the disk line is AUD 3.49 and the test's worst case is **AUD 3.72**. No meter exists in the API answer for the NSG, NIC, VNet or the auto-shutdown schedule. **Planned cost: AUD 0.23; ceiling for the 8-hour test: AUD 3.72.**

## 4. The test procedure

### 4.1 Before any Azure resource (no cost; these are gates)
- **G1. The Monday first-run must have worked on the M577.** That means `oxpd1 read` (lane L5) over the LAN, the printer's certificate sha256 recorded and pinned, and the Test service enable step (first-run list 2a step 2) proven.
- **G2. An echo verb in the lab tool.** `oxpd1` has only `read` and `lab-cert` (B1997). The test needs a lane that adds `oxpd1 echo`. It would run `SyncEchoString` (server → printer, `https://<host>:7627/...TestService`) and `AsyncEchoString` with a callback URL, plus a TLS callback listener that records each callback's arrival time and source address. It runs with a **guest** credential (`guest` / any password, per HP's spec) and **refuses a credentials file that holds the admin password name**. The verb is built and gated like every lane. UNMEASURED: the exact SOAP shape of the Test service calls.
- **G3. LAN rehearsal (free).** Run `oxpd1 echo` Mac → printer on 192.168.20.x with the callback on the Mac. A pass here proves the tool, so a later Azure failure is a path failure, not a tool fault.

### 4.2 What Kam must do at home
- **Nothing at the router.** No port forward, no DMZ, no VPN box. This test opens no inbound port at the site, by design.
- Keep the Mac awake and wired (192.168.20.220) for the window. It is the site relay.
- Printer settings (all from the LAN, all already on the first-run list):
  - the Test service enabled (admin call from the Mac on the LAN);
  - a **second dev CA** uploaded to the printer's OXPd CA store, issued for the VM's FQDN (`lab-cert` keeps no CA key, so the FQDN needs a new CA);
  - "Enable HP home screen if OXPd app fails to load" stays ON.
- No button and no agent is registered, so the panel cannot lock. Kam is needed at the panel only if the CA upload is done through the web page.
- UNMEASURED: whether the M577 has a DNS server and a default gateway configured, so it can resolve the FQDN and route to the internet. Check this in its web page before the window.

### 4.3 Steps in the window (run by the OXPd agent as `oxpd2-claude-deploy`, under a brief quoting Kam's card answer)
1. **Home IP:** on the Mac, read the home public IP (`curl -s https://api.ipify.org`). This becomes the NSG source `/32`.
2. **SSH key:** `ssh-keygen -t ed25519 -N '' -f '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/3_Access_Keys/oxpd2_s14_vm'` (gitignored folder).
3. **Create** (draft commands; DO NOT RUN before the card):
   ```zsh
   az vm create -g oxpd2-s14-path-test-rg -n oxpd2-s14-vm -l australiaeast \
     --image Canonical:ubuntu-24_04-lts:server:latest --size Standard_B2ats_v2 \
     --admin-username azureuser --authentication-type ssh \
     --ssh-key-values '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/3_Access_Keys/oxpd2_s14_vm.pub' \
     --storage-sku Standard_LRS --os-disk-size-gb 30 \
     --public-ip-sku Standard --public-ip-address-allocation static \
     --public-ip-address-dns-name oxpd2-s14-<4 random> \
     --vnet-name oxpd2-s14-vnet --vnet-address-prefix 10.214.0.0/24 --subnet-address-prefix 10.214.0.0/26 \
     --nsg oxpd2-s14-nsg --nsg-rule NONE \
     --tags project=OXPd_2 purpose=S14-path-test owner=kam expires=<YYYY-MM-DD>
   az network nsg rule create -g oxpd2-s14-path-test-rg --nsg-name oxpd2-s14-nsg -n allow-home-ssh \
     --priority 100 --direction Inbound --access Allow --protocol Tcp --destination-port-ranges 22 \
     --source-address-prefixes <home-ip>/32
   az network nsg rule create -g oxpd2-s14-path-test-rg --nsg-name oxpd2-s14-nsg -n allow-home-callback \
     --priority 110 --direction Inbound --access Allow --protocol Tcp --destination-port-ranges 8443 \
     --source-address-prefixes <home-ip>/32
   az vm auto-shutdown -g oxpd2-s14-path-test-rg -n oxpd2-s14-vm --time 1200
   ```
   Measure from the API at create time: confirm the VM's size and the IP's SKU match section 3.
4. **Certificate:** `oxpd1 lab-cert` for the FQDN on the Mac, then upload the CA to the printer from the LAN. Copy the server certificate and key, plus the self-contained `oxpd1` build, to the VM with `scp`. **The VM's credentials file holds only the guest line.** Before any run, check it by count, never by value: `grep -c OXPD_TEST_PRINTER_ADMIN_PASSWORD` must be `0`.
5. **Relay up (Mac):**
   ```zsh
   ssh -i <key> -N -o ExitOnForwardFailure=yes \
     -R 127.0.0.1:7627:<printer-ip>:7627 -R 127.0.0.1:10443:<printer-ip>:443 azureuser@<fqdn>
   ```
   The server then reaches the printer at `127.0.0.1:7627`, the same port number end to end. No inbound port opens anywhere at home.
6. **Server → printer (VM):**
   - (a) discovery tree `GET` through `127.0.0.1:10443`, no password;
   - (b) TLS handshake on 7627, printer certificate sha256 compared with the LAN pin from G1 (same sha = same printer, end to end);
   - (c) `SyncEchoString` ×20 with guest, recording each round trip.
7. **Printer → server and the full round trip (VM):** `AsyncEchoString` ×20 with callback `https://<fqdn>:8443/echo`. The printer calls Azure **directly over the internet** through the home router's ordinary outbound NAT. Record: callback received (yes/no), delay, and the source address seen (expected: the home public IP).
8. **Negative controls:**
   - (i) drop the relay and repeat 6c: it must fail (proves the path was the relay);
   - (ii) from the VM, try `<home-ip>:7627` directly: it must fail (proves no site port is open);
   - (iii) from a network other than home (phone hotspot), `8443` and `22` on the FQDN must time out (proves the NSG source limit).
9. **Collect** the run folder to the Mac, outside git (the D7 refusal), then run the undo list.

**Pass (S14, OXPd 1.x leg):**
- 6a, 6b and 6c succeed through the relay;
- 7 delivers the callbacks over the internet;
- 8 (i) to (iii) fail as expected;
- latencies are recorded.

Anything else is a recorded failure. Under no-skip-on-failure, its cause goes into the result, not into a retry loop.

### 4.4 Undo list (each one checked, not assumed)
| # | Undo | Check |
|---|---|---|
| U1 | Stop the SSH relay | `pgrep -f oxpd2_s14_vm` empty |
| U2 | Test service off (`DisableService` from the LAN, or a reboot) | `IsServiceEnabled` = False |
| U3 | Delete the S14 dev CA from the printer's OXPd CA store | CA list read back without it |
| U4 | `az group delete -n oxpd2-s14-path-test-rg --yes` | `az group exists` = false. Next day, Cost Management shows no running meter for the RG |
| U5 | Remove the SP's now-dangling role assignment. Kam decides whether `oxpd2-claude-deploy` stays for OXPd's later Azure work | `az role assignment list --assignee <appId>` |
| U6 | SSH key pair moved to `3_Access_Keys/_quarantine/<date>/` (never deleted) | listing |
| U7 | Run folder outside git; nothing from it committed | `git status` clean of it |

## 5. What this proves, what it does not, and the risks

**Proves (if it passes):**
- **P1.** A FutureSmart 5 printer behind an ordinary home router (outbound NAT only) can call a server in australiaeast by its Azure DNS name over HTTPS, with a certificate whose CN is that name. This is the printer → server half of N-5.
- **P2.** A server in Azure can reach the printer's 7627 SOAP services and 443 discovery through a **site relay that the site opens outbound**, with no inbound port at the site and the port number unchanged. This is the server → printer half, for the relay shape.
- **P3.** The full asynchronous round trip (server calls the printer; the printer calls back to Azure) works across those two legs, with measured latency. That latency is the number timeouts and the sign-in flow will be judged against.

**Does NOT prove:**
- That HP supports it: HP calls OXPd 1.x "not a cloud-based SDK" (C2:154). A pass is a measurement, not support.
- The **admin-class path**: registration of buttons and agents, card-reader traffic, and `login` across the link. These need the admin password, and C2:154 says registration "needs the device IP reachable from the server". Whether the device writes its own address into records the server must reach back is not exercised here.
- A **site-to-site VPN** (customer firewall ↔ Azure VPN Gateway, the design's rejected D1 option c). Not tested: it needs a second billable resource (VpnGw1 AUD 0.27/hour) and enterprise kit.
- A **port forward on the site router**. Deliberately not tested: it would expose the printer's admin SOAP to the internet.
- Customer networks: proxies, egress filtering, split DNS, many printers per relay, relay failover. OXPd 2 printers. IPP and Print-URI. Scan upload sizes.
- That a relay at every site is acceptable to Kam or customers. That is a product decision N-5 still owns.

**Risks and how the design holds them:**
- **Open ports on a public IP:** only TCP 22 (key-only SSH) and 8443, each limited to the home /32. The VM lives for hours, not days. Residual: a home IP that changes mid-window breaks the test, which is fail-safe.
- **The admin password crossing the internet (F16): it does not happen in this test.** Admin calls (enable the Test service, upload the CA) are made from the Mac on the LAN. The VM's credentials file holds only `guest`, checked by count before the run. The echo verb refuses a file carrying the admin-password name. Only guest echo calls travel, inside SSH plus TLS. A wrong guest password cannot lock the admin account (guest takes any password). UNMEASURED on the device.
- **The relay exposes the printer's guest-level services to the VM's loopback** for the window. HP's Test service also has automation methods (`ExecuteJavaScript`, `PressKey`, `GetScreenCapture`); their credential requirement was not read. Mitigation: the relay is up only for steps 6 to 8, nothing else runs on the VM, and U1 and U2 close it.
- **F18 (no rate limit on printer-facing routes):** the echo listener is a lab tool, not the product server, and the NSG limits callers to the home IP. F18 still stands for the first non-lab deployment.
- **Cost overrun** if forgotten: AUD 21.01 a month running, AUD 8.68 after the auto-shutdown. The `expires` tag plus U4's next-day check close it.
- **Production next door:** subscription `0c57ab37` holds `datasec-sales-portal-rg`. The SP's role is scoped to `oxpd2-s14-path-test-rg` only, and the boundary is proven by the AuthorizationFailed check in 2.3 before any create.
- **Unknowns Tuesday reads at the card** (no `az` here): Compute provider registration, Basv2 quota in australiaeast, any policy denying public IPs, and the RG name being free.

## 6. Card draft for Kam

**Title:** OXPd: create the one Azure test VM to measure how a site's older printer reaches Azure? About AUD 0.23, deleted the same day.

**BLUF (6 lines):**
1. Datasec/OXPd. You chose "one Azure test resource". This card is its tenant, resource and cost; nothing exists yet.
2. Where: the agent-controllable Datasec environment (tenant d500ebad), "Azure subscription 1", a new group oxpd2-s14-path-test-rg in Australia East. The production sales-portal group is untouched.
3. What: one small Linux VM with a public IP and a small disk, for one test of at most 8 hours, then the whole group is deleted. Measured price: about AUD 0.03 an hour, AUD 0.23 for the test; AUD 21 a month if forgotten.
4. How: your Mac opens an outbound tunnel to it, so nothing is opened on your router. The printer calls the VM by name. Only harmless echo calls go over the internet; the admin password stays at home.
5. First you create OXPd's own Azure login, limited to that one group (five pasteable lines; about 5 minutes with Tuesday).
6. It runs only after Monday's printer read has worked and the same test has passed on your home network.

**Options (recommended: a):**
- **[a] Create it as designed.** Detail: "One VM in Azure subscription 1, group oxpd2-s14-path-test-rg; you create OXPd's login limited to that group; at most 8 hours, about AUD 0.23; deleted the same day."
- **[b] Not yet: rehearse at home first.** Detail: "The same test on your home network costs nothing and proves the tool; the Azure VM comes back on a card after that."
- **[c] Stop.** Detail: "No Azure test; the path question goes to the kick-off."

**Default (no answer):** nothing is created in Azure and no identity is made. G2 (the echo verb) and G3 (the home-network rehearsal) touch no Azure and cost nothing. They are Tuesday's to brief inside the existing first-run approval; that approval is not widened by this card.
