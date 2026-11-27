# B2163 | OXPd: how the final build is deployed at a customer, and what the lab must mirror (card K11)

Analyst B2163 for Tuesday s334. READ-ONLY. Clocks by `date`: started Fri 27 Nov 2026 17:55:45 AEDT; Azure listing 17:57:31; prices 17:57:40. Every claim has a source; UNMEASURED where none. `02:` = `OXPd_2/1_Project_Definition/Design/02_architecture.md` line, `03:` = `03_plan-of-attack-and-build.md`, `CL:` = `CLARIFICATIONS.md`, `B2154:` = `TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2154_OXPD-WORKING-COPY-PLAN.md`.

## BLUF (K11 in two sentences)

**Neither option on the K11 card mirrors a client deployment: a router name for the Mac is not a ruled packaging, not a customer-internal-CA name and not in the client's Azure, and the Azure VM alone cannot reach a printer on his LAN without a two-way, no-NAT path (VPN) that nobody has designed or costed.** The faithful mirror is the ruled Linux container (C-17) under a name in the test tenant's own domain (`datasec-rd.com`, C-9/q22) with a certificate from a lab "customer internal CA" pushed to the M577, run first on the lab network (the per-site shape C-26 and HP's on-premises model) and then the same container on a VM in `oxpd2-dev-rg` behind a site-to-site VPN (the W5 "client's Azure subscription" shape, which is N-5 and still open); this costs about **+1.5 lock-days before M-a (1 Dec slips to about 2-3 Dec)** and **+1.5 to 2 days plus about A$3 a day of Azure** for the VPN leg, which fits only if that leg lands after M-d (18 Dec) or replaces S14.

Plainly: **the lane P plan contradicts the client-deployment rule** in four places (section 4), and **the design itself is not settled on where Phase 1's server lives** (P-4 and N-5 are open, 02:1274, 05:199): his W5 says the client's Azure subscription, HP says on the customer's network, and the design's own platform table says "a cloud-only server is not viable without a site relay" (02:249).

## 1. The final-build deployment per the design and his rulings

| Item | What the design / ruling says | Source |
|---|---|---|
| Where the server runs | "in the client's Azure subscription in Phase 1 (W5, B1817), one per site (W4; the path to the printers is N-5)"; "a local server that works with no internet is Phase 2 (A5)" | 02:14, 02:275, 02:910 (D1) |
| His words | W4 "one server per site on the customer's network is not inconsistent with them deploying through azure in their tenant. Phase 1 will be hosted through azure"; W5 "OXPd runs in the clients azure subscription"; A4 "everything including oxpd servers need to be in their tenant"; A5 "Phase 2 we will have a local server that allows for no internet. For now, internet is essential"; A6 "license server through Azure or Datasec. 2 deployment optiuons"; A7 "Azure marketplace" | CL:552, 554, 478-484 (02:1148-1152) |
| q05 ruling | `datasec-oxpd-q05-server-location-1118` choice **a** "On each site's network" (detail "Customer hosts one server per site"), 2026-11-19 03:33 | decision_queue show |
| Conflict | P-4: C-26 (q05 a) against W4/W5/A4/A5, shapes (i) Azure server per site joined to the site network, (ii) a machine at each site governed through Azure, (iii) Azure now, on-site in Phase 2: **open** | 03:557, 05:199 |
| How printers reach it | N-5 "How do printers at a site reach a server in the client's Azure, and the server them?" **open**; "Code hosting-neutral; no Azure resource" | 02:1274, 03:572 |
| Delivery route | q12: "clients will deploy the solution through the Azure marketplace using services and components automatically deployed by the configuration scripts we create and submit. During development, we will mirror this structure as closely as possible so the deployment is tested through dev"; q22: "everything about work path and OXPd is done by the client in their own app / tenant"; w7 "we build against kamil@datasec-rd.com. full environment simulated" | CL:848, 856, 864 (C-80) |
| Dev environment | his note: "create a new resource group under kamil@datase-rd.com. issue new steps so agents have full control to spin up and create services/ vms etc" (C-81) → `oxpd2-dev-rg` | CL:930; project CLAUDE.md:60 |
| Packaging (q14) | `datasec-oxpd-q14-server-packaging-1118` choice **c** "Both equally": Linux container set (server + PostgreSQL, signed OCI image + compose) and virtual appliance (OVA/VHDX), and a Windows Server installer (service + SQL Server) | decision_queue show; 02:793 (8.1 Packaging) |
| Host prerequisites | 4 vCPU, 8 GB, 100 GB per 500 printers (inferred); static IP on a network that reaches every printer | 02:794 |
| Ports | server → printer TCP 443 (OXPd 2 REST, 1.x discovery), 7627 (1.x services), IPPS 631 (Workpath-era firmware) or 443; printer → server on its HTTPS port; outbound 443 to Microsoft, customer SignalR/Function, Log Analytics DCE, Datasec licence, via proxy where required; NTP | 02:794 |
| q18 ruling | `datasec-oxpd-q18-pull-sharing-ipps-1118` **a**: "port 631 open on the printer network" | decision_queue show |
| DNS | "An FQDN in the customer's DNS (for example `printsuite.<customer domain>`) resolving to the server or the HA virtual IP; must be resolvable by printers" | 02:795 |
| Certificate (q22) | `datasec-oxpd-q22-tls-certificate-1118` **a** "Customer internal authority", detail "Name in the customer's DNS"; server cert for the FQDN (CN and SAN, never an IP: OXPd 1.x exact CN match), RSA 2048+, full chain; CA chain uploaded to the installer and pushed to every device (1.x `ImportCertificate`; OXPd 2 `certificateAuthorities/import`) | decision_queue show; 02:796, 02:635-636 (6.3) |
| Network trust | "Server on the customer LAN; a cloud-only server is not viable without a site relay"; OXPd 1.x "Two-way, fixed port 7627 on the device, no NAT remap" | 02:249 (section 4) |
| First run | bootstrap code on console; Entra admin consent (Option A add redirect + credential to the existing HPAM registration, Option B create); Datasec licence installation credential + CSA key package; `.cfg` import; test page | 02:797 |
| Admin console | Entra sign-in, roles Site Admin / Operator / Auditor, no anonymous first run | 02:377 (C16), 02:614 |
| Secrets | C15: local store under DPAPI-NG/TPM (Windows) or sealed key file (Linux), or customer Key Vault; as built: Linux key file owner-only, NOT sealed, no Key Vault provider (K-4) | 02:376 (C15) |
| Backups | DB + secret-store key escrow; restore under 15 minutes | 02:798 |
| Updates | blue/green on the appliance; side-by-side on Windows; out of hours | 02:844 (8.4) |
| Logging | Serilog to file + optional OpenTelemetry, deny-list of fields | 02:575 (5.9) |
| Onboarding | operator starts jobs in the AuthSuite Manager (amended); server's onboarding engine executes | 02:803, 02:859 (8.7) |
| Multi-site | one server (or pair) per site; a central server "not offered in release 1" (OQ-11) | 02:857 (8.6) |
| Approved Azure test | C-75 "One Azure test resource now"; C-78 one small Linux VM for about a day, "about 23 cents", only after the home rehearsal passes; for S14 (the N-5 path test) | CL:772-830; 03:192 |

## 2. How HP documents an OXPd server being deployed

| HP says | Source |
|---|---|
| OXPd "centralizes the 3rd party code (called a Solution) on a Solution Server connected to the same network"; the context holds "the hostname of the customer's Solution Server" | B1 §4.10 (`P/how-it-works.md:13, 32`) |
| OXPd 2 is two-way: device → server (pages, every target) and server → device (token grant, install, login, HID open, every REST call); no device-initiated-only mode; WebSocket/TCP targets "not currently supported" | B1 line 15, §4.10 items 1-3 |
| OXPd 2 device trusts only the CAs in the solution's own store for outbound TLS; a private-CA server needs that CA imported after install | B1 §4.10 item 4 (`G/solutionPackagingUtility.md:162`) |
| OXPd 1.x: "not a cloud-based SDK and is expected to be run from a server in the customer's environment"; port 7627 fixed; NAT remap not supported; device inbound 80/443/7627 | C2 line 154 (SF 360002980048 :33) |
| For cloud workflows HP steers to Workpath, not OXPd; cloud server-side logout "never prioritized ... not even planned" | C2 lines 63, 174 (SF 4620109272339) |
| HP portal "Which SDK": Workpath = cloud (SaaS); OXPd = on-premises | C2 line 179 (`General/Portal-Pages/which-device-sdk-should-i-use.md:9-12`) |
| OXPd 1.x CA store: empty store = no outbound HTTPS; CN must equal the URI host, no IPs | 02:251 (C1 §4.2, §4.19) |
| HP's CertificateManagement description: self-signed certificates in the OXPd CA store "not recommended or supported" (whether that excludes a private root CA: not established) | BACKLOG item 103 |
| No load balancer / failover supported; `hostSets` not supported | 02:567; B1 §4.10 |
| HP's public web pages: see section 2a | WEB |

### 2a. HP public documentation (web)

Fetched by a helper agent at about 18:00 AEDT. **developers.hp.com returned HTTP 403 on every page tried**, so HP's own OXPd pages are search snippets only (marked). Nothing opened gives HP's deployment rule for an OXPd server; nothing opened settles two-way reachability, NAT, or a cloud connector for OXPd.

| Claim | Source | Status |
|---|---|---|
| OXPd2 keeps the Solution on "a Solution Server connected to the same network"; the Solution Context carries "the customer's Solution Server hostname"; one server can serve OXPd 1 and OXPd 2 devices | https://developers.hp.com/node/28706 | search snippet only (403) |
| A vendor (Ricoh): "The first generation of the HP terminal (OXPd) can connect to the cloud only via a secondary gateway"; Workpath Gen 2 "connects directly to the cloud", server needs a domain name, not an IP | https://manual.na.ps.cloudstream.ricoh.com/docs/latest/cloudstream/hp-workpath-gen-2-cloud-terminal | opened (not HP) |
| OXPd 1.6: when the server certificate comes through a CA chain, the root CA is what goes on the printer | https://docshield.tungstenautomation.com/ControlSuite/en_US/help/clients/AutoStore/Source/HPOXPd(1.6)/Dita/OXP16Certificate.html | search snippet only (page not found) |
| HP: Workpath is "a flexible and scalable cloud-based solution", "no additional infrastructure needed" | https://hp.com/us-en/solutions/business-solutions/workpath.html | opened |
| Workpath install: enable Workpath in EWS, claim the printer in HP Command Center, install the app from Command Center | https://docshield.tungstenautomation.com/Printix/en_US/help/admin/Printix_admin/t_how_to_install_hp_workpath_printers_in_hp_command_center.html | opened (not HP) |
| HP's cloud fleet service never opens connections to printers on a customer network; printers poll (443, 631 fallback, UDP 9930) | https://learn.workforceexperience.hp.com/docs/hp-wxp-printer-fleet-management-security-and-privacy | opened (HP) |
| HP's on-site connector for its cloud is the "Print Fleet Proxy" beside Web Jetadmin behind the firewall (fleet management, not OXPd) | https://learn.workforceexperience.hp.com/docs/onboarding-printers-through-a-proxy | opened (HP) |

Read together with section 2: HP's own cloud services avoid inbound connections to printers and put an on-site component behind the firewall when they need local reach; OXPd 1.x/2 require server → printer calls. **No HP source opened or held describes an OXPd server in a public cloud reaching printers**; the only pattern any source offers for it is a site gateway/VPN (Ricoh, C2:214, both not HP).

## 3. How companies deploy the Workpath apps today

| Piece | Where it runs | Source |
|---|---|---|
| The apps (HPAM, OneDrive, SharePoint, Mailflow, Teams, Universal Print) | **on the printer**; no Datasec server in the customer's tenant: "the logic runs on the printers" | D2 §2.4, §6.1 row 5 |
| Installed by | HP Command Centre (default, HP or reseller), HP's local tools (Workpath Essential licence), or Datasec's AuthSuite Manager | D2 §2.4 row 2, §4 step 11 |
| Customer tenant | single-tenant app registration "HP Authentication Manager" + client secret; 13 delegated Graph permissions + admin consent; Attribute Assignment/Definition Administrator on the enterprise app; Universal Print enterprise app consent (Datasec multi-tenant); optional `SignalR.Access` scope | D2 §2.1 (HD:344-768) |
| Customer Azure (optional) | Marketplace offer "HP Authentication Suite Onboarding Azure Services" (publisher DATASEC SOLUTIONS PTY LTD): Function App (3-function SignalR relay), SignalR, Storage, Log Analytics; or PowerShell/Bash scripts; card-only sites need none | D2 §2.1; A9 §1.1-1.2 |
| Licence server | Datasec's in Azure Australia East, OR a second Marketplace offer into the customer's Azure (Linux App Service B1, VNet, NSG inbound 443, SQLite on Azure Files, its own app registration) | D2 §2.2, §0 item 4; A9 §3.3 |
| Network | all printer traffic outbound (HTTPS 443 to Microsoft, Function App/SignalR, Log Analytics, licence; IPP 631 for Universal Print) | A6:341, A6:374-379 |
| Certificates / DNS | "nothing is documented about TLS trust or customer CA certificates for the suite" | A6:382 |
| Values handed over | tenant id, client id, secret, SignalR endpoint, reporting string, "securely" | D2 §4 step 8 |

So "mirror how companies do it" carries over the **route** (customer tenant, the same registration and consents, Marketplace offer, the same handed-over values) but not the **shape**: OXPd needs a server reachable both ways that Workpath never had (D2 §6.1 row 5).

## 4. What the lab must mirror (Kam's M577; this Mac; `oxpd2-dev-rg`, tenant ec01829b)

Measured 17:57:31: `az account show` (project `AZURE_CONFIG_DIR`) = tenant `ec01829b-...`, subscription `a6b8fe11-...` "Azure subscription 1", user `kamil@datasec-rd.com`; `az resource list -g oxpd2-dev-rg` = ONE resource, `oxpd2-boundary-proof-vnet` (australiaeast). No VM, no DNS zone, no Key Vault, no VPN gateway. Prices: Azure Retail Prices API (`https://prices.azure.com/api/retail/prices`, AUD, australiaeast, 17:57:40): VPN Gateway Basic A$0.0512/h, VpnGw1 A$0.27/h, S2S connection A$0.0213/h; Linux B1s A$0.0188/h, B2s A$0.075/h, B2ms A$0.1506/h (730 h/month used for monthly figures).

| Item | Design says | HP says | Workpath customers do | Lab plan (B2154) | Gap | Cost |
|---|---|---|---|---|---|---|
| Server host / OS | ruled packaging: Linux container set or appliance, or Windows service (02:793, C-17) | "external server", any OS (B1 §4.10) | no server | "the server run from a build on the lab Mac"; container "only as CI's build" (B2154:29) | **not a ruled packaging** | run the compose set on Docker (present: `/usr/local/bin/docker`) on the Mac or a Linux box: ~0.5 day (owed 5 status UNMEASURED) |
| Where it runs | client's Azure subscription, one per site (W5/W4); q05 a: site network; P-4 open | on the customer's network (C2:154; B1 §4.10) | n/a | lab network, "no Azure" (B2154:9, K11 default) | W5 shape untested; on-LAN shape matches C-26 and HP | stage 1 A$0; stage 2 VM B2s ≈ A$1.80/day (A$55/month) |
| DNS name | FQDN in customer DNS, e.g. `printsuite.<customer domain>` (02:795, q22) | host name or IP accepted on OXPd 2 (B1 §4.10 item 6); 1.x needs exact CN host (02:251) | n/a | "a name on your router for the lab Mac" (K11); L9 CA named `oxpd-lab-ca-test.local` (X85 brief D2) | a `.local`/router name is not "the customer's DNS" | a `printsuite.lab.datasec-rd.com`-style name on the router's DNS (A$0) or Azure Private DNS (stage 2; price UNMEASURED); who owns the `datasec-rd.com` zone: UNMEASURED |
| Certificate authority / trust | customer internal CA (q22 a, C-9), cert for FQDN, CA pushed to every device, renewal alert (02:796, 6.3) | device trusts only its solution / OXPd CA store; self-signed in store "not recommended or supported" (BACKLOG 103) | nothing documented (A6:382) | a fresh 1-day dev CA for the row-3 store test only; "a later TLS test makes a new CA for the host name ... K11" (X85 D2) | no lab "customer internal CA" exists; whether the M577 accepts a private root is the open owed 103 | +0.5 day: a lab two-tier CA (root offline, issuing CA) standing in for the customer's; if the M577 refuses a private root, a card (public cert on a Kam-owned domain) |
| Entra tenant pieces | app registration (Option A/B), 13 delegated permissions, CSA roles, admin consent, optional SignalR/Log Analytics, licence credential (02:797; 7.1) | n/a | same registration and consents (D2 §2.1) | K2 (tenant user + app registration) by 7 Dec (B2154:11) | matches if K2 is built as the customer guide's steps, in ec01829b | 0 Azure; K2 is Kam's |
| Network printer → server | printer reaches server's HTTPS port; FQDN resolvable (02:794-795) | mandatory (B1 §4.10 item 1) | outbound only | route 192.168.8 → 192.168.20, untested (owed 118; L9) | same as plan for stage 1 | in plan (L9, 0.5) |
| Network server → printer | 443, 7627, 631, no NAT (02:794, 02:249) | mandatory; 1.x no NAT, 7627 fixed (C2:154) | none | same LAN route | **stage 2 (Azure) has no path**: needs routed site-to-site VPN, no NAT; can Kam's router do IPsec: UNMEASURED | VPN Basic A$0.0512/h + S2S A$0.0213/h ≈ A$1.74/day (A$53/month) [Basic SKU's current availability for new gateways: UNMEASURED]; VpnGw1 ≈ A$6.99/day (A$213/month); +1.5-2 days build |
| Can an Azure server reach his LAN printer, and how do customers do it? | open (N-5); design names VPN only as D1's rejected option (c) (02:910) | "not a cloud-based SDK"; cloud → Workpath (C2:154, 174); C2's inference: "an Azure-hosted OXPd 1.x server would need a site connector/VPN per site" (C2:214) | n/a (no inbound path exists today) | not tested; S14 approved but not created (03:192) | no customer pattern documented anywhere we hold | see row above |
| Admin roles / least privilege | console roles Site Admin, Operator, Auditor; device admins cannot change tenant config (02:377, 02:582) | n/a | Global Admin consent; Owner/Contributor for the offer (D2 §2.1) | not in plan before 23 Dec (no admin API: B2154:10) | gap accepted for WC; record it | 0 |
| Consent | admin consent link at first run (02:797) | n/a | admin consent (D2 §4 step 4) | K2 | as K2 | 0 |
| Secrets store | C15; Linux key file NOT sealed as built (K-4); Key Vault optional (02:376) | n/a | secret in Command Centre config | local store on the Mac | as built, not as designed (sealed / Key Vault) | Key Vault: price UNMEASURED; not needed for WC |
| Backups | DB + key escrow, 15-minute restore (02:798) | n/a | n/a | none | not mirrored | defer; 0 |
| Updates | blue/green (02:844) | n/a | Command Centre | none | not mirrored | defer |
| Logging | Serilog + deny-list (02:575); E1.8 log scan | n/a | app data logs | not stated | E1.8 is in E2.1 | in plan |
| Delivery | Marketplace offer + config scripts (q12, A7) | n/a | Marketplace offer (D2 §2.1) | none | no offer or script for the server exists | after WC; UNMEASURED |

## 5. K11's answer and its cost against lane P

**Recommendation: "both, staged", not either option alone.**

- **Stage 1 (lab network; the C-26 / HP on-premises shape; before M-a):** the server as the ruled Linux container set on this Mac's Docker (or a small Linux host on the lab network); name `printsuite.<lab sub-domain of datasec-rd.com>` in the router's DNS; server certificate from a lab two-tier "customer internal CA"; that CA pushed to the M577 by first-run row 3 (L9 then uses this CA, not a throw-away `.local` one). Cost: about +1.5 lock-days (container run 0.5, CA + DNS + host-name TLS 0.5, L9 rerun with the real CA 0.5): **M-a Tue 1 Dec → about Thu 3 Dec**, absorbed by the 18 Dec / 23 Dec slack only if Q2's hygiene lanes stay off the lock (B2154:11, 168). A$0.
- **Stage 2 (W5 shape, the N-5 test; after M-d 18 Dec or as S14):** the same image on a Linux VM in `oxpd2-dev-rg` behind a routed site-to-site VPN to the lab (no NAT, 7627/443/631 both ways), Azure Private DNS for the same name. Cost: +1.5 to 2 days (gateway provisioning alone takes tens of minutes: UNMEASURED here), about **A$3.5 a day** (B2s A$1.80 + VPN Basic A$1.23 + S2S A$0.51) or about A$9/day with VpnGw1; left running a month ≈ A$108-268, which is **over the ~A$50/month line** the coordinator reads into C-81 (B2154:112): a card. Needs a router that terminates IPsec (UNMEASURED) and his word beyond C-78's "one small Linux VM for about a day".
- **The Azure VM alone (K11 option b):** does not work for the M577 without stage 2's VPN (02:249; C2:154). **The router name for the Mac alone (option a):** works for the flow but mirrors neither the packaging (C-17) nor the CA (C-9) nor the Azure ruling (W5).

**Where the plan or a brief contradicts the client-deployment rule** ("This project needs to mirror a client deployment and follow all security, operational and deployment rules", K11 note 17:53:19):
1. B2154:9 "on one packaging, on the lab network, no Azure" and K11 default "a router name for the Mac; no Azure" against W5 "OXPd runs in the clients azure subscription" and q12 "During development, we will mirror this structure as closely as possible so the deployment is tested through dev" (CL:554, 848).
2. B2154:29 "the server run from a build on the lab Mac" is not either ruled packaging (q14 c / C-17, 02:793).
3. X85 (L9) D2: a 1-day CA named `oxpd-lab-ca-test.local` is a store test, not the customer-internal-CA + customer-DNS arrangement (q22 a); the brief itself says the TLS host comes later with K11, so it is a gap, not a breach.
4. B2154 has no step for consent/roles/secrets-as-designed/backups; acceptable for a working copy only if written as a deviation (the design's own words: "follow all security, operational and deployment rules" is now his rule, so each omitted item needs a line in the deviation register, OQ-6 style).
5. The design itself: 02:249 ("a cloud-only server is not viable without a site relay") stands against 02:14 (Phase 1 in the client's Azure) with N-5 and P-4 open: the "final build" shape is **not decided**, so no lab can mirror it fully until he rules P-4 (i), (ii) or (iii).

**One question for Kam that unlocks K11:** P-4 — in Phase 1, is each site's server (i) a VM in the client's Azure joined to the site network by VPN, or (ii) a machine on the site's network deployed and governed through the client's Azure? (ii) is what stage 1 mirrors at no cost; (i) is stage 2.

## Sources (read for this note)

- Commission `2026-11-27_B2163_OXPD-CLIENT-DEPLOYMENT-MIRROR_COMMISSION.md`.
- `OXPd_2/1_Project_Definition/Design/02_architecture.md` lines 11-18, 241-275, 358-382, 561-660, 785-903, 910, 986, 1143-1152, 1274; `03_plan-of-attack-and-build.md` lines 80, 104, 192, 200-222, 557, 572; `05_readiness-to-build.md` line 199.
- Decision cards via `decision_queue.sh show`: q05 (a), q14 (c), q22 (a), q18 (a).
- `CLARIFICATIONS.md` lines 158, 466-484, 550-570, 772-830, 840-870, 926-940, 1098-1104.
- Analysis: `D2_current-solution-deployment-second-review.md` §0, §2, §4, §6; `A6_product-behaviour-spec-from-docs.md` lines 341, 374-382; `A9_hpam-backend-gateway-and-infra.md` §1.1-1.2, §3.3; `B1_oxpd2-platform-guides.md` line 15, §4.10, line 568; `C2_oxpd1-field-experience-js-general.md` lines 7, 63, 154, 174, 179, 214, 239.
- `OXPd_2/BACKLOG.md` items 103, 118; `OXPd_2/CLAUDE.md` line 60.
- `B2154_OXPD-WORKING-COPY-PLAN.md` lines 9-12, 29, 66, 83, 105-112, 123-129, 144; `B2159_SEAT-X85_oxpd2-l9-network-path.md` lines 7, 38, 92-93.
- `az account show`, `az resource list -g oxpd2-dev-rg` (read-only, project `AZURE_CONFIG_DIR`), 17:57:31.
- Azure Retail Prices API, AUD, australiaeast, 17:57:40.
- HP public pages: section 2a.
