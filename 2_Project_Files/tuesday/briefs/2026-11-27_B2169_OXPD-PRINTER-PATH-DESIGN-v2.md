# B2169 lane D | OXPd: the printer path and the Azure mock client, design v2 (B2165 revised per review B2167)

Drafter B2169 lane D for Tuesday s334. READ-ONLY: nothing was created in Azure, the OXPd project, Jira, GitHub, cards or mail; no device contact. Clocks by `date`: started Fri 27 Nov 2026 18:26:32 AEDT; retail price reads 18:26:57 to 18:29:00; Microsoft Learn pages opened between 18:27:23 and 18:28:44; cards printed 18:28:47; written from 18:29:42. Scratch: `TUESDAY/2_Project_Files/fleet/state/s334/d2169-D/` (`prices2.py`..`prices4.py` + `.txt`, `cost.py` + `cost.txt`, `card_*.txt`). Marks: **MEASURED** (I ran or opened it), **RELAYED** (from a record), **UNMEASURED**, **ESTIMATE**. `B2165:n` = line n of the design this revises; `B2167` = the review; `[Fn]` marks a change made for review finding n; a line without a mark is carried from B2165 unchanged in substance. `02:n`, `C1`, `C2`, `CL`, `B2163`, `B2154` as in B2165.

**The two cards, now ruled (RELAYED from Tuesday's message to this drafter, Kam on the live board at 18:30; at my own print, `decision_queue.sh show` 18:28:47, both still read open with `choice=None`, so the rulings below are Tuesday's relay, not my read):**
- `datasec-oxpd-printer-path-design-1127` = **a** "Connector, VPN as an equal option" (free printer test first, the four security fixes, then the lab build; spend comes as a card with cost).
- `datasec-oxpd-p4-confirm-1127` = **a** "Yes, that is right": Phase 1, the server runs in the client's Azure, installed from the Marketplace, reaching office printers through the Site Connector; a server in the office is a later optional form; this supersedes q05's "on each site's network" for Phase 1.
This document is written on those rulings [F3]: P-4 is **settled** (no longer pending); the connector is the default transport and the VPN an equal option chosen at install. Spend still waits for its own card (§8), as the ruling says.

## What changed against B2165 (one line per finding)

| Finding | Severity | Fixed where in v2 | In one line |
|---|---|---|---|
| F1 | HIGH | §2.3, §2.6 pt 3, §4.2 | The connector's reach ceiling (printer addresses and ports) is set ON SITE by the client and cannot be widened from Azure; the server's list only narrows inside it |
| F2 | HIGH | §2.4, §2.6 pts 1, 4 | Relay namespace locked down: Entra RBAC per hybrid connection, no SAS keys, private endpoint for the server side, namespace IP firewall limited to the office's egress |
| F5 | HIGH | §3 | CA: root key offline outside Azure; issuing key non-exportable in its own RBAC vault in a group the agent login has no role in; the server may only ask that vault to sign |
| F10 (console) | HIGH per commission | §2.5 | Admin console on its own port and its own hybrid connection, never on the printer callback path; off on site unless the client names admin addresses |
| F4 | HIGH | §2.2, §2.6 pts 10-11, §7 Q-D3 | Section 2c's rejection of the pass-through marked superseded; HP's wording stated precisely (port remap); caller-address header; the 1.x callback credential made a prerequisite; the free test gates everything |
| F3 | HIGH | header, §1, §7 Q-D1 | The question F3 asked was put to Kam (card `datasec-oxpd-p4-confirm-1127`) and ruled **a** at 18:30 (RELAYED): server in the client's Azure for Phase 1, connector on site, q05 superseded for Phase 1. v2 records P-4 from his ruling, not from a default |
| F6 | MEDIUM | §5.2 | Traffic cost model: per-GB line, ~153 GB/month break-even (review), ~133 GB with v2's extra pieces; three listeners for two connectors |
| F7 | MEDIUM | §2.7, §4.2 | Client work stated honestly; full outbound list; enrolment designed; Windows connector on day one |
| F8 | MEDIUM | §4.1 | The lab says plainly it runs a stand-in tool (azbridge), lists what it does and does not prove, and its four lab risks |
| F9 | MEDIUM | §6 lane AZ-T | The A$0 forwarder test on the lab network (lane T, seat X88) runs first and decides connector vs VPN before any spend |
| F10 (rest) | LOW | §1, §2.8, §6 | Stale VPN text removed or rewritten; HP precedent wording corrected; provider registration is Kam's own click; Windows packaging deviation line |
| F2 (sub) | MEDIUM | §1 row Outbound | No-public-IP option (NAT gateway) still unpriced: retail API returned 0 rows again (MEASURED 18:27:16) |

## BLUF (for Tuesday, then Kam)

1. **Design unchanged in shape, hardened in four places.** Each client office runs an OXPd Site Connector that only dials OUT on 443 to an Azure Relay namespace in the client's own Azure; the server's sidecar does the same; printer traffic passes both ways with TLS end to end. B2167 agreed with the pattern and found four security holes; v2 closes each in the design, not as a note: [F1] the office sets which printers the connector may reach; [F2] the Relay meeting point accepts only Entra identities, only from the office's address and from the server's private endpoint; [F5] the CA root key never enters Azure and the issuing key cannot be exported or granted to the agent login; [F10] the admin console is not on the path the printers use.
2. **The VPN is now an equal first-class transport [F6, B2167 Q4],** chosen at install: (a) connector, the default for sites without a private link to Azure and under ~133 to 153 GB a month of print and scan traffic; (b) the client's existing hub VPN or ExpressRoute, or a new site-to-site VPN, for clients who already have one or for large sites. Same server, same template; a parameter picks the transport.
3. **Kam ruled the connector with the VPN as an equal option, free printer test first (18:30, RELAYED) [F9].** Lane T (seat X88) puts a plain TCP forwarder on this Mac between the lab tool and the M577 at 192.168.8.157, at A$0, no Azure: does the printer accept OXPd 1.x calls from a forwarder's address and call back through it, TLS end to end? Pass: the connector lab, then the spend card. Fail: the ruled equal option, the VPN transport, carries the lab, then the spend card. [F4]
4. **P-4 is settled [F3]:** Kam ruled `datasec-oxpd-p4-confirm-1127` **a** at 18:30 (RELAYED): in Phase 1 the server runs in the client's Azure from the Marketplace and reaches office printers through the Site Connector; a server in the office is a later, optional form; q05 "on each site's network" is superseded for Phase 1. The design record (02) may now add the Site Connector component and record P-4 this way (Q-D1).
5. **Lab cost moves from ~A$105 to ~A$116 a month always on** (private endpoint A$10.37 + its DNS zone A$0.71 + a second vault), **~A$78 with the server off out of hours, ~A$58 with the connector and sidecar off too** (MEASURED meters, `cost.txt`). Over A$50: a card (§8).

## 1. The target: what a client has after a Marketplace install

Packaging reasoning unchanged (B2165:37: Azure Application solution template → VM running the ruled Linux container set). **Changed [F10]:** the transport to the site is a template parameter, `transport = connector | existingLink | siteToSiteVpn`, not "with the VPN to the site". **Deviation-register line [F10]:** the Marketplace VM route mirrors the Linux packaging only; q14 c "both equally" also binds a Windows server packaging, which has no Azure mirror in this design.

| Element | Mock client design (in `oxpd2-dev-rg` unless stated) | Source |
|---|---|---|
| Server | Ubuntu LTS VM, B2s for one printer; system-assigned managed identity; **no inbound rule at all** (the connector path needs none; the VPN path adds §2.9's rule); Docker + compose set from the signed OCI image; Bicep written as the future `mainTemplate`, size parameter default 4 vCPU / 8 GB | B2165:41 |
| Database | bundled PostgreSQL container, E6 data disk | B2165:42 |
| Secrets [F5] | **Two vaults, both Azure RBAC (no access policies).** `oxpd2-mock-kv` (in `oxpd2-dev-rg`): server TLS certificate + key, Entra app credential, DB password, escrowed secret-store key; the VM identity holds Key Vault Secrets User **scoped to the named secrets it needs**, nothing vault-wide. `oxpd2-ca-kv` (in a new group `oxpd2-ca-rg`, §3): the issuing CA key only, non-exportable. **The root key is in neither** (§3). The VM still copies its secrets at boot into the local C15 store (no Key Vault provider in the built store: K-4, 02:1298) | B2167 F5; Microsoft rbac-access-policy (opened 18:2x) |
| Network [F10, F2] | VNet `oxpd2-mock-vnet` 10.232.0.0/24: `snet-server` 10.232.0.0/26; `snet-pe` 10.232.0.64/28 (Relay private endpoint, §2.4); `GatewaySubnet` 10.232.0.224/27 **reserved, empty** unless the VPN transport is built (§2.9). NSG on `snet-server`: **deny all inbound** (connector transport); outbound 443 to the private endpoint and to Microsoft; **outbound 9400-9599 to the private endpoint** (Microsoft: "If you use the relay listener over a private link, open ports 9400-9599 for outgoing communication", MEASURED, private-link-service page) | B2165:44 rewritten |
| Outbound to Microsoft [F2 sub] | Standard public IP on the VM NIC, all inbound denied (A$5.18). A client reviewer will ask for no public IP: NAT gateway is the answer and its price is **UNMEASURED** (retail API, 0 rows at 18:27:16, MEASURED; same as B2165 and B2167) | B2165:45 |
| DNS name | `printsuite.<mock-client domain>`; dedicated domain default (Q3 of B2165) | B2165:46 |
| How the printer resolves it [F10, F8] | Connector transport: `printsuite.<domain>` → **the connector's LAN address** (lab: the Mac, 192.168.20.220, RELAYED B2165:104). Default: a record in the public zone. **Risk [F8]:** a home router's DNS-rebinding protection may drop a public answer pointing at a private address (UNMEASURED for Kam's router); fallback: dnsmasq on the Mac as "the client's internal DNS" and the M577's DNS setting pointed at it, which the board grant now covers (Kam 17:54:13, RELAYED via the commission: "this printer is yours for the project ... provision what you need"; with a printed undo) | B2165:47 rewritten |
| Customer internal CA [F5] | §3 | B2165:48 rewritten |
| CA chain to the printer | `CertificateManagement.ImportCertificate` of the **root certificate** (public part only) into the M577's store (row 3, PR 52); private-root acceptance owed 103; exact CN match, URI host = FQDN | B2165:49 |
| Log Analytics | workspace + DCR; F63 streams; Monitoring Metrics Publisher on the DCR for the app SP (card) | B2165:50 |
| Backups | nightly pg_dump + key escrow to immutable blob + weekly snapshot | B2165:51 |
| Admin console [F10] | §2.5: own port, own hybrid connection, Entra sign-in; never reachable on the printer callback path. Agents administer the VM by `az vm run-command` (no SSH from the Internet, no Bastion) | B2165:52 rewritten |
| Managed identity [F5, F2] | system-assigned on the VM; **all data-plane access by Azure RBAC role assignments** (Relay per hybrid connection, Key Vault per secret / per key). B2165's Q9 default (access policies, "no card") is **withdrawn**: under access policies "users with the Contributor ... role ... can grant themselves data plane access" (MEASURED, rbac-access-policy). Role assignments need Owner or User Access Administrator, which the agent login lacks: one card (§8 K-RBAC) | B2165:53 replaced |
| Entra pieces | as B2165:54; plus the per-site connector identity (§2.7) | B2165:54 |
| Customer's existing Azure pieces | as B2165:55 (after the working copy) | B2165:55 |

## 2. The production design: server in the client's Azure, printers in the client's office

### 2.1 The printer's two-way needs
Unchanged (B2165:60-66): server → printer 443 (OXPd 2 REST, 1.x discovery), **7627** (1.x services, fixed on the device), 631/443 (IPPS); printer → server: callbacks, panel pages, scan upload, Print-URI fetch to the FQDN on the server's HTTPS port; server → Microsoft 443.

### 2.2 What the M577 must accept, stated precisely [F4]
- **HP's wording (RELAYED from B2167, which MEASURED C2:154):** "all OXPd .NET/Java services listen on device port 7627, not configurable; NAT **port** remapping not supported". That forbids changing the **port**, not the **caller's address**. Calls into the device are HTTP Basic admin over TLS to `https://{device}:7627` (C1:79, RELAYED). No HP statement found that the device checks the caller's address.
- **Superseded [F4]:** B2165 §2(c) (B2165:129, "Rejected: ... breaks the no-NAT rule") and the reason given for excluding point-to-site VPN at B2165:133 ("printer traffic would need translation") were written on the reading "translation of the caller = forbidden". Under the precise wording that reading is the weaker one. Both rejections are **withdrawn as reasons**; point-to-site stays excluded for a different reason (it gives the Azure side an address in a client pool, a routing design no client would run for a fleet). The "no NAT" rule in 02:249 / 02:794 is read in v2 as **no port remap, and the URL host and port the printer sees are its own**, which the connector keeps.
- **Still UNMEASURED and decisive:** does the M577 accept 1.x calls from an address that is not the server's, and do its callbacks work through a pass-through, with TLS end to end and within its timeouts? That is lane AZ-T (§6), A$0, before anything else [F9].
- **Second-order loss, now designed [F4]:** through a byte-passing connector the server no longer sees the printer's address on callbacks. The connector prepends a **PROXY protocol v2 header** carrying the original caller address and port to every printer → server stream; the server's sidecar accepts the header **only on its loopback hand-off** and passes the address to the server for audit, lockout and device binding (C1:383, C1:496 warn that address-based identity "breaks behind NAT or a proxy", RELAYED). A stream without a valid header is refused.
- **Prerequisite made explicit [F4]:** OXPd 2 callbacks carry a per-device credential; for OXPd 1.x none is built (02:613 item 2, RELAYED). Because the connector's LAN port accepts any machine in the office, the **1.x callback credential is a prerequisite for the product connector** (lane AZ-1X, §6). The lab may run before it, recorded as a deviation.

### 2.3 The reach ceiling, set on site [F1]
- **Property:** no instruction that originates in Azure (server, sidecar, Relay, the template, a pushed config) can make the connector open a connection to an address or port outside the ceiling the client's IT set on site.
- **How:**
  1. At install the client's IT writes the ceiling into a local file on the connector host: printer subnets or exact addresses (IPv4, RFC1918 only) and the port set, which is at most {443, 7627, 631}. Lab: `192.168.8.157/32`, ports 443, 7627, 631.
  2. The file sits **outside the image**, mounted read-only into the container (container form), or in a protected folder writable only by local Administrators (Windows form). It is **never** part of anything the connector receives over Relay or the update channel. Changing it needs a person with local admin on the connector host.
  3. The server pushes its enrolled-printer list after onboarding; the connector uses **the intersection** of the pushed list and the ceiling. A pushed target outside the ceiling is refused, logged locally and to the client's Log Analytics as `CeilingViolation`, and raises an alert rule shipped with the template.
  4. Hard denies regardless of the file: non-RFC1918 targets, the connector host's own addresses, link-local and loopback, the default gateway, and port 57627 (the device debug port, B2167 F10).
  5. The connector prints its effective ceiling at start and on every change, and the server's console shows it read-only (the server sees it; it cannot set it).
- **Residual risk, stated:** a malicious **signed** connector image from Datasec's own supply chain could ignore the file. Controls: signature verification on site against a pinned Datasec publisher key (cosign or Authenticode by form), the client chooses the update policy (automatic or manual approval), SBOM per release (§2.6 pt 6). This is the same trust a client gives any on-site agent; it is not a control Azure can override.
- **Comparison with the VPN, reworded [F1]:** both transports can be scoped. A site-to-site VPN is scoped by the client's own firewall rules to the printer subnets and ports, a control their security team already knows; the connector is scoped by the on-site ceiling in our code. B2165's "a VPN would give the Azure network reach into the whole office" (B2165:12, :76) is withdrawn.

### 2.4 The Relay namespace, locked down [F2]
- **Authentication: Entra only, per hybrid connection.** Microsoft: role assignment can be scoped to "a specific Relay entity like a hybrid connection" with built-in roles Azure Relay Listener ("listen and entity read") and Azure Relay Sender ("send and entity read") (MEASURED, authenticate-application). Per site:

| Hybrid connection | Listener (role: Azure Relay Listener, scope = this HC) | Sender (role: Azure Relay Sender, scope = this HC) | Carries |
|---|---|---|---|
| `<site>-to-site` | connector identity (each connector of the site) | server VM managed identity | server → printer (443/7627/631) |
| `<site>-to-server` | server VM managed identity | connector identity | printer → server callbacks, port fixed to the callback port |
| `<site>-admin` (optional, §2.5) | server VM managed identity | connector identity | admin console, port fixed to the console port |

  No identity holds a role at namespace, group or subscription scope on Relay data. The server side holds **no key at all** (managed identity). The connector's identity is §2.7.
- **No shared keys.** The template creates **no** SAS authorization rule on any hybrid connection. Whether a namespace can switch SAS off entirely (a `disableLocalAuth`-style property) is **UNMEASURED** (not on the four pages opened); whether `RootManageSharedAccessKey` is created implicitly by ARM is **UNMEASURED** (Microsoft's own sample template declares it explicitly). Lane AZ-2R reads both from the live namespace and the resource schema before anything connects, and records: rule present or absent, keys regenerated if present, an Azure Policy audit of SAS use if available. **SAS fallback** only for a site that refuses Entra: per site, per direction, Listen-only or Send-only, held only on the connector host, rotated by a written job; the server side still uses its managed identity.
- **Private endpoint for the server side.** A private endpoint in `snet-pe` (group id `namespace`) with the `privatelink.servicebus.windows.net` private DNS zone linked to the VNet, so the server's sidecar reaches Relay over its private address (Microsoft: "Traffic between your virtual network and the service traverses over the Microsoft backbone network", MEASURED, private-link-service). NSG rules do not apply to private endpoints (same page, Limitations).
- **Namespace IP firewall limited to the office's egress.** `networkRuleSets/default`: `publicNetworkAccess = Enabled` (the office has no private link), `defaultAction = Deny`, `ipRules` = the office's public egress address(es) only, `trustedServiceAccessEnabled = false`. Microsoft: "Any connection attempt from an IP address that doesn't match an allowed IP rule on the namespace is rejected as unauthorized" (MEASURED, ip-firewall-virtual-networks). Rules are namespace-wide, so one namespace per client lists every site's egress; a namespace per site isolates them (§2.8). For the lab: Kam's WAN address, which may be dynamic (UNMEASURED); if it changes, the connector cannot connect until the rule is updated, a visible failure (fail closed). Microsoft's note that ARM templates default `defaultAction` to `Allow` (MEASURED) becomes an AZ-2R check: the deployed rule set reads `Deny`.
- **Proof steps (security review):** a Send attempt with a valid Entra token from an address outside the rule is refused; a Send attempt on `<site>-to-site` by the connector identity is refused (wrong role); the server reaches Relay with `nslookup <ns>.servicebus.windows.net` resolving to 10.232.0.64/28.

### 2.5 The admin console off the printer path [F10]
- **Property:** a machine on the office LAN that can reach the connector's printer callback port cannot reach the admin console.
- **How:** (1) the server serves the console on a **separate port** from the printer callback port (port numbers: the built server's settings, UNMEASURED against code; the design fixes only that they differ); (2) the sidecar maps `<site>-to-server` streams to the callback port only and `<site>-admin` streams to the console port only, a fixed mapping in the server's own config, so a stream on the callback path cannot be steered to the console; (3) the connector's **admin listener is off by default**; the client turns it on in the same on-site ceiling file by naming admin source addresses (CIDRs); connections from any other source are dropped before Relay; (4) the console requires Entra sign-in (roles Site Admin / Operator / Auditor, C16), and the client's Conditional Access applies; (5) the `<site>-admin` listener on the server runs only while enabled (it bills listener hours only while connected).
- **Lab:** admin listener on, admin source = the Mac only; Kam reaches the console at `https://printsuite.<domain>:<console port>` from the Mac. Agents keep `az vm run-command`.

### 2.6 Security review points (B2165:90-101 revised)
1. [F2] No inbound port on the office or the Azure server (external scan of both) **and** the Relay namespace refuses: an address outside the IP rule; a principal without the role on that hybrid connection; any SAS token (if SAS is absent). An external port scan alone is not proof.
2. TLS end to end printer ↔ server: the connector holds no private key; a capture on the connector shows TLS only. **[F10]** The 7627 leg is HTTPS (C1:79, RELAYED), so B2165's plain-HTTP worry applies only to the debug port 57627, which is hard-denied (§2.3 pt 4). The outer Relay TLS ends at Microsoft, as it must.
3. [F1] Ceiling: refuses a pushed target outside the on-site file, any port outside it, any non-RFC1918 target, and the hard-deny set; each with a forged target test; refusals appear in Log Analytics and fire the alert.
4. [F2] Least privilege: per-HC Entra roles (table §2.4); no namespace-wide role; no SAS rules (or SAS per site per direction with rotation, fallback only).
5. Audit: connector stream log + Relay diagnostic logs + server logs joined by a stream id; **[F4] the PROXY-header caller address is in each record**; deny-list of fields (02:575) applies to the connector.
6. Supply chain: signed image, SBOM, pinned base, non-root, read-only filesystem; **[F1]** on-site signature verification against a pinned key; client-chosen update policy.
7. Data residency: scan and print data transit Relay inside TLS in the client's region; security whitepaper line.
8. Availability: HP home screen fallback (02:571); two connectors per site; Relay SLA UNMEASURED.
9. Latency: one extra hop; measured in AZ-T (LAN forwarder, no Relay) and again in AZ-8 (through Relay) against the 10-second panel limit.
10. [F4] Source address: the printer sees the connector's address; EWS IP access lists must include it (install-guide line); 1.x acceptance is gated by AZ-T.
11. `azbridge` "is not covered by Azure product support": lab only (B2165:101; B2167 F8 confirms latest release v0.16.1, 13 Nov 2025, RELAYED).
12. [F4] The 1.x callback credential exists and is required before the product connector ships (AZ-1X).
13. [F5] The CA root key is not in Azure; the issuing key is non-exportable; the agent login holds no role in `oxpd2-ca-rg` and cannot create one (§3 proof steps).
14. [F10] The console is not reachable through the callback path or from a non-admin source (§2.5 proof).

### 2.7 What the client does, and enrolment [F7]
- **Honest baseline [F7]:** today's Workpath customer does no on-site network or server work (B2163 §3, RELAYED). The connector adds an always-on host per site that the client runs, patches and monitors. It is still far less than a VPN (no firewall change control, no address-plan clash). B2165:11's "three ordinary things" is replaced by this list:
  1. Run the connector on a host that can see the printers: container, the appliance image, or the **Windows service on an existing Windows print server** (day one, §4.2).
  2. Write the on-site ceiling file (§2.3): printer subnets or addresses; optionally admin sources (§2.5).
  3. Allow outbound 443 from that host to: **the client's own Relay namespace by name** (`<ns>.servicebus.windows.net`; Microsoft allows naming one namespace instead of the wildcard, "you'll also need to allowlist the gateways", Relay FAQ, RELAYED from B2167); `login.microsoftonline.com` (Entra token for the connector identity); the image registry (pulls and updates); the client's Log Analytics ingestion endpoint (connector logs). **If Arc is used**, Microsoft's Arc list in addition (about a dozen endpoints including `*.his.arc.azure.com`, `*.guestconfiguration.azure.com`, `management.azure.com`, RELAYED from B2167, network-requirements page). Through their proxy if they have one (Relay runs on WebSockets over 443).
  4. Add one internal DNS record: `printsuite.<domain>` → the connector's address(es) (same work as the ruled design, 02:795).
  5. Give the office's public egress address(es) to the install wizard (§2.4 IP rule).
  6. Enrol the connector (below).
- **Enrolment, designed [F7]:**
  1. The Marketplace install (by the client's Azure Owner) creates the namespace, hybrid connections, private endpoint and the server's role assignments; the createUiDefinition asks for site name(s) and egress address(es).
  2. In the admin console a Site Admin chooses **Add site connector**; the console shows a one-time **enrolment code** (single use, 15-minute life) that carries only non-secret data plus a pairing nonce: tenant id, namespace, hybrid connection names, the server's TLS chain fingerprint.
  3. On the connector host, the client's IT runs `oxpd-connector enrol <code>`. The connector generates its own key pair locally (non-exportable where the OS allows: Windows CNG / TPM; Linux: a file readable only by the service user); the private key never leaves the host.
  4. **Identity, default (no Arc):** the enrol command asks the client admin to sign in interactively (device code) with **their own** Entra rights, creates (or reuses) a per-site app registration `OXPd Site Connector <site>` with the connector's **public certificate** as its credential, and assigns Azure Relay Listener on `<site>-to-site` and Azure Relay Sender on `<site>-to-server` (and `<site>-admin` if enabled). The rights come from the client admin's own sign-in, never from the server: the Azure server cannot mint connector identities. **Option:** the host is Arc-enabled (Windows or Linux host) and the connector uses the Arc managed identity; the role assignments are the same.
  5. The connector opens `<site>-to-server` and presents the pairing nonce to the server inside the TLS session whose chain matches the fingerprint; the server marks the connector enrolled and shows its effective ceiling (read-only).
  6. Rotation: the connector renews its certificate credential before expiry using its current one (Graph `addKey`-style proof of possession, UNMEASURED which API the client tenant permits) or by re-running `enrol` with a new code.

### 2.8 Sizing [F6]
- Listener hours bill per connected listener, and "Adding listeners to an open relay results in additional relay hours" (Relay FAQ, RELAYED from B2167). A site with two connectors and the server's sidecar holds **three listeners** (two on `to-site`, one on `to-server`): A$41.61/month, not A$27.74 (MEASURED meter A$0.019/h, 18:27:16).
- Limits (RELAYED, B2167 F6): 25 listeners per hybrid connection; **5,000 concurrent relay connections per namespace**. Template default: one namespace per client; a namespace per site above a printer-count parameter (default 500) or when the client wants per-site IP rules isolated. Namespaces themselves carry no meter in the retail rows read (only listener hours and data, MEASURED).

### 2.9 The VPN transport, an equal first-class option [F6, F10, B2167 Q4]
- **When chosen (install-time parameter):** the client already runs a hub VPN or ExpressRoute into Azure (`existingLink`: the template peers or attaches the server VNet to their hub and adds nothing on site), or a site over roughly 133 to 153 GB a month of print and scan traffic (§5.2), or a security team that will not vet new tunnel software (`siteToSiteVpn`).
- **What it is:** B2165 §2(a), (b) and (d) carried as written (VPN Gateway VpnGw1AZ, route-based IKEv2, untranslated inner traffic; strongSwan box or the client's firewall; NVA variant), now as **option B of the product**, not "the fallback". NSG for this transport: allow the server's callback port from the printer subnets only; deny all else. GatewaySubnet populated. Admin console reached over the tunnel from admin subnets the client names (same property as §2.5).
- **Not deleted:** B2165 §2's SKU research (B2165:115-134) and the router questions (B2165:119) stand and are referenced, not copied. B2165 §2(c)'s rejection text is superseded (§2.2).

### 2.10 Text withdrawn from B2165 [F10]
- B2165:12 "It is the pattern HP uses for its own cloud fleet service" → **"an on-site outbound component has precedent (HP's Print Fleet Proxy for fleet management, not OXPd, B2163:65-66; one vendor sentence on a 'secondary gateway', B2163:61). Microsoft Universal Print's on-site connector is the closer precedent (B2167, from the reviewer's knowledge, UNMEASURED here)."** HP's cloud does not open connections to printers.
- B2165:15 "or a card for us to do it under his login" (the `Microsoft.Relay` provider registration) → **Kam's own click** as Owner. Kam's sign-in and the agent login share one config folder (B2165:25): no agent runs under his sign-in.
- B2165:37 "with the VPN to the site"; :44 NSG and GatewaySubnet as the design; :47 DNS → 10.232.0.4 "reached over the VPN"; :52 console "only over the VPN"; :193 AZ-8 "the printer sees 10.232.0.4 (no NAT)"; :200 "depends on the tunnel": each rewritten in §1, §4 and §6.
- B2165:76 and :12 blast-radius comparison: rewritten in §2.3.

## 3. The CA [F5]

- **Property:** (a) the root private key never exists in Azure; (b) the issuing private key can sign but cannot be read or exported by anyone, including the server; (c) the agent login cannot obtain any right on the issuing key, now or later, without Kam.
- **Root (offline, outside Azure):** RSA 4096, 10 years. Generated by the CA-ceremony seat on this Mac **inside an encrypted APFS disk image** (AES-256, passphrase typed by Kam, never stored by an agent) held under the OXPd project's `3_Access_Keys/mock-ca-root/` (gitignored, never committed). Used for exactly: signing the issuing CA certificate once; signing the root CRL (yearly). Then the image is detached. A copy on Kam's removable media is the second copy. It is never uploaded to any vault, blob or repo. (A client's own AD CS offline root plays this part in production; the product never holds a root.)
- **Issuing CA (in its own vault, non-exportable):** RSA 3072, 2 years, created **inside** `oxpd2-ca-kv` as a Key Vault **key** with `exportable = false` (Standard vault, software-protected RSA; meters: Advanced Key Operations A$0.2132 per 10K, MEASURED 18:26:59). Ceremony: Key Vault creates the key and a CSR (certificate with issuer "Unknown"); the CSR is carried to the Mac; the root signs it inside the encrypted image; the signed certificate is merged back. The issuing private key never exists outside Key Vault.
- **Where the vault lives:** a separate resource group **`oxpd2-ca-rg`**, created by Kam (subscription scope; free). The agent login `oxpd2-claude-deploy` holds **no role** there. The vault uses Azure RBAC, and granting data-plane access under RBAC needs Owner or User Access Administrator ("RBAC restricts permission management to only the 'Owner' and 'User Access Administrator' roles", MEASURED, rbac-access-policy); the agent login is Contributor on `oxpd2-dev-rg` only (RELAYED B2165:26), so it can neither assign itself a role on the key nor change the vault's permission model (no right in that group at all; whether switching an RBAC vault back to access policies itself requires `roleAssignments/write` is UNMEASURED, which is why the vault is placed outside the agent's group rather than relying on that).
- **What the server may do with it (least privilege, per the commission):** the VM's managed identity gets a custom role **"OXPd CA Signer"** with data actions `Microsoft.KeyVault/vaults/keys/read` and `.../keys/sign/action` only, **scoped to the one issuing key** (key-level RBAC scope: Microsoft rbac-guide, not opened today: UNMEASURED here). It can ask Key Vault to sign a hash; it cannot read, export, delete, rotate or grant. It uses this to issue or renew its own TLS certificate (a .NET `CertificateRequest` with an `X509SignatureGenerator` that calls Key Vault `sign`; design level, not measured in code). If the server does not need to issue certificates in release 1, the role is not assigned and renewal is a ceremony-seat job instead (§7 Q-D4). **Deviation from B2167 F5's wording**, stated: F5 asked for a vault "the VM cannot read"; the commission asks for one "the server reads with least privilege"; sign-only on one non-exportable key satisfies both readings (the key material is unreadable).
- **Ceremony identity:** the ceremony needs Key Vault Certificates Officer on `oxpd2-ca-kv` for about an hour. Kam assigns it to a dedicated ceremony principal (not `oxpd2-claude-deploy`) for the window and removes it after; both actions are printed in the ceremony record. Certificates Officer cannot export a non-exportable key.
- **Server certificate:** RSA 2048+, CN and SAN = `printsuite.<domain>`, full chain, 30-day renewal alert; stored in `oxpd2-mock-kv`; the VM reads only that secret (§1).
- **Proof steps:** (1) `az keyvault key show` reports `exportable: false`; a backup/export attempt by the server identity is refused; (2) a role-assignment list on `oxpd2-ca-rg` shows no entry for the agent login; an attempt by it to read the vault is refused (403, the boundary working, per the workspace rule: report, never work around); (3) the root private key is absent from every vault, blob and repo (search by its public-key hash); (4) the M577 receives only the root **certificate**.

## 4. The lab, and the product connector

### 4.1 Lab build on Kam's M577 network (what it proves and what it does not) [F8, F9]
- **Order:** (1) AZ-T, the A$0 forwarder test (lane T, seat X88): no Azure, decides connector vs VPN. (2) Only after AZ-T passes and Kam rules the spend card: the Azure pieces and the azbridge lab. (3) The product connector replaces azbridge after the working copy or with a second builder.
- **Said plainly to Kam [F8]:** for the 23 Dec working copy the lab runs **Microsoft's open-source `azbridge` as a stand-in** for the product connector, which does not exist yet (5 to 6 lock-days, B2165:108). K11b "full mimic of target environment now" is therefore met for the server, the Relay namespace, its lockdown and the CA, and **not** met for the connector software. Recorded as a deviation.
- **What azbridge does mirror (RELAYED, B2167 MEASURED the repo):** TCP tunnels over the same Relay service, both directions, bytes forwarded end to end, Entra or SAS auth, Docker and macOS. **And [F1] in the lab, its fixed `-T` forwarders to 192.168.8.157:443/7627/631, written in the Mac's own config, ARE an on-site ceiling**: nothing in Azure can add a target.
- **What it does not mirror:** pushed allow-list narrowing, the audit log, the CONNECT sidecar, the PROXY header, enrolment, the admin listener's source filter.
- **Lab risks [F8]:** (1) the server runs in a container; a loopback alias of the printer's address on the VM host reaches the container only if azbridge binds beyond loopback (`-g`), UNMEASURED; (2) Docker on the Mac hides the printer's address from the forwarder and needs the callback port published on the Mac; (3) DNS rebinding protection may drop `printsuite` → 192.168.20.220 (dnsmasq fallback, §1); (4) both routes depend on the printer ↔ Mac path (owed 118, K4/C-84), which AZ-T exercises first; (5) [F2] Kam's WAN address on the namespace IP rule may change (fail closed, update the rule); (6) whether azbridge authenticates with a managed identity on the VM is UNMEASURED (fallback: the VM uses a certificate-credential principal for azbridge only, lab deviation, still no SAS).
- **Kam's hands for the lab:** no router change (K4/C-84 route only, already ruled); the card (§8): spend, `Microsoft.Relay` registration by his own click, `oxpd2-ca-rg` creation, the role assignments, the CA passphrase, the domain, licences.

### 4.2 The product connector (lane AZ-CX) [F1, F4, F7, F10]
- One .NET codebase (the supported Relay SDK, Microsoft.Azure.Relay, by supervised fetch C-61/C-62), shipped **on day one in three forms [F7]**: signed Linux container, the appliance image, and a **Windows service** (MSI, runs on an existing Windows print server). Rationale: q14 c "both equally" (02:793: an appliance "for customers without container skills", and a Windows installer); B2165's Q19 default ("Windows only if a client asks") is withdrawn.
- Functions: on-site ceiling + pushed narrowing (§2.3); `to-site` listener opening TCP to (ceiling ∩ pushed) targets; callback listener on the LAN passing TLS unchanged with a PROXY v2 header [F4]; optional admin listener with source filter (§2.5); enrolment (§2.7); stream audit to Log Analytics; heartbeat to the console; signature-verified updates.
- Server side (sidecar): CONNECT proxy upstream to `to-site` (the device clients keep the printer's real URL); listeners on `to-server` → callback port and `<site>-admin` → console port, fixed mapping [F10]; PROXY header accepted only on the loopback hand-off [F4]. **UNMEASURED [F8]:** ".NET HttpClient takes a CONNECT proxy with no core change" against the built code; the certificate pin lives in four copies (02:613 item 1), each needing the proxy setting.

## 5. Cost (Azure Retail Prices API, AUD, australiaeast, pay-as-you-go, 730 h/month)

Meters MEASURED 18:26:57 to 18:27:23 (`prices2.txt`..`prices4.txt`) where marked *; others RELAYED from B2165 `prices.txt` (B2167 re-checked them). Arithmetic by `cost.py` (MEASURED, `cost.txt`).

### 5.1 Lab (one site, one connector on the Mac)
| Resource | Meter (AUD) | Per month | Stoppable |
|---|---|---|---|
| Server VM B2s | 0.075/h | 54.75 | yes (deallocate) |
| OS disk E4 | 4.6387/month | 4.64 | no |
| Data disk E6 | 9.2773/month | 9.28 | no |
| VM public IP Standard | 0.0071/h | 5.18 | no |
| Public DNS zone | 0.7106/zone/month | 0.71 | no |
| Backups (snapshot + blob) | ESTIMATE | 2.88 | n/a |
| Relay listeners × 2 (connector on `to-site`, sidecar on `to-server`) * | 0.019/h each | 27.74 | yes (stop connector and sidecar) |
| Relay data * | 0-5 GB A$0, then 1.4212/GB | 0 (lab under 5 GB, ESTIMATE) | n/a |
| [F2] Private endpoint (Relay, server side) * | 0.0142/h + 0.0142/GB in and out | 10.37 | no |
| [F2] Private DNS zone `privatelink.servicebus.windows.net` * | 0.7106/zone/month | 0.71 | no |
| [F5] Key Vault × 2 (Standard; issuing key ops) * | 0.0426 / 0.2132 per 10K ops | ~0.02 | n/a |
| [F10] `<site>-admin` listener, on demand * | 0.019/h while on | ~4.12 at 217 h (not in total) | yes |
| Log Analytics | 0-5 GB A$0 | 0 | n/a |
| **Total always on** | | **A$116.28 (A$3.82/day)** | |
| Server VM deallocated outside ~217 h | | **A$77.80** | |
| Server VM and connector/sidecar off outside ~217 h | | **A$58.31** | |

Not in the Azure API: the mock-client domain (yearly, UNMEASURED); Microsoft 365 licences (tenant holds 0 SKUs, RELAYED B2165; price UNMEASURED). NAT gateway (no public IP option): UNMEASURED, 0 rows.

### 5.2 Product traffic model, per client site [F6]
- **Fixed:** three listeners (two connectors + sidecar) A$41.61; plus per client, the private endpoint A$10.37 and its DNS zone A$0.71: **A$52.69/month for a one-site client**.
- **Variable:** every scan upload, print job and Print-URI fetch crosses Relay: **A$1.4212/GB after the first 5 GB** (whether the 5 GB is per namespace or per subscription: UNMEASURED) + A$0.0284/GB private endpoint processing.
- **Break-even against a new site-to-site VPN (A$238.56: VpnGw1AZ 217.83 + connection 15.55 + IP 5.18):** **~153 GB/month** on the review's basis (two listeners, no private endpoint: (238.56 − 27.74) / 1.4212 + 5, MEASURED by `cost.py`); **~133 GB/month** on v2's basis (three listeners + private endpoint: (238.56 − 52.69) / (1.4212 + 0.0284) + 5).
- **Examples (ESTIMATE volumes from B2167 F6; prices MEASURED):** 20-printer office ~22 GB → connector ~A$77/month vs VPN A$239; ~153 GB → A$267 vs A$239; 500-printer site ~550 GB → ~A$843 vs A$239.
- **Rule for the install wizard and Kam's card:** connector for sites without a private link and under ~133 GB/month; the client's existing link or a VPN above it or where a hub already exists. For `existingLink`, the transport's marginal Azure cost to the client is ~A$0.

## 6. Build lanes (every Azure write by `oxpd2-claude-deploy`, Contributor on `oxpd2-dev-rg`, never Kam's sign-in; IaC in the OXPd repo `deploy/azure/**`)

| # | Lane (who) | Scope | Undo | Needs |
|---|---|---|---|---|
| **AZ-T** [F9] | Lane T, seat X88 (device-run, A$0) | plain TCP forwarder on the Mac between the lab tool and 192.168.8.157, both directions; 1.x call from the forwarder's address; callback through it; TLS end to end; timings | stop the forwarder by pid; printed undo for each device write | the printer ↔ Mac path (owed 118); board grant 17:54:13 |
| **AZ-0** | Cards (Tuesday → Kam) | §8 spend card; K-RBAC role assignments; `Microsoft.Relay` registration (Kam's click); `oxpd2-ca-rg`; domain; licences | n/a | AZ-T result (P-4 and the transport card already ruled a, 18:30) |
| **AZ-1** | Drafter + builder (repo) | `deploy/azure/**` Bicep: server, two RBAC vaults, VNet with `snet-pe`, Relay namespace + HCs + `networkRuleSets` (Deny + IP rules, trusted services off), private endpoint + private DNS zone, role-assignment module (deployed by an Owner), `transport` parameter with the VPN module [F6]; what-if only | revert PR | none |
| **AZ-2R** [F2] | Agent under the SP (+ Kam for roles) | namespace, `lab-to-site`, `lab-to-server`, `lab-admin`; no SAS rules; read and record SAS/`disableLocalAuth` state; IP rule = Kam's WAN; private endpoint; proofs of §2.4 | remove the hybrid connections and namespace per B2165 Q11 | AZ-0, AZ-1, AZ-4 VNet |
| **AZ-CA** [F5] | Ceremony seat + Kam (passphrase, role window) | root in encrypted image on the Mac; issuing key non-exportable in `oxpd2-ca-kv`; CSR signed offline, merged; root CRL; proofs of §3 | disable key version; detach image | AZ-0 (`oxpd2-ca-rg`, role window) |
| **AZ-3R** | Agent on the Mac + device-run seat | azbridge on the Mac (fixed `-T` targets = lab ceiling [F1]) and on the VM, Entra auth; then S14b through Relay: 1.x call, callback, CA import, timings | stop containers; remove alias | AZ-T pass, AZ-2R, AZ-4, AZ-5 |
| **AZ-4** | Agent under the SP | VM B2s (identity), E6, public IP inbound-denied, NSG deny-inbound + 9400-9599 to the PE, `oxpd2-mock-kv` (RBAC), Log Analytics + DCR + DCE, storage (immutable), cloud-init | deallocate; per Q11 | AZ-1; K-RBAC for data access |
| **AZ-5** | Agent | DNS zone + `printsuite` → connector address (lab 192.168.20.220) [F10]; server cert signed by the issuing key; into `oxpd2-mock-kv` | remove record; disable cert version | AZ-CA, AZ-4 |
| **AZ-6** | Agent | backups and a timed restore drill | disable timer | AZ-4 |
| **AZ-7** | Card / Kam's Graph rights | app redirect URI, certificate credential, licences, Teams/SharePoint, TAP/TOTP | remove; unassign | AZ-0, AZ-5 |
| **AZ-8** [F10] | Device-run seat | M577 ↔ Azure server end to end through Relay: callback to `https://printsuite.<domain>`, row 3 CA import (mock root certificate), 7627 call; **packet check: the printer sees the connector's address (192.168.20.220) as caller; the server's log shows the sidecar hand-off with the original 192.168.8.157 (PROXY header once AZ-CX lands; azbridge cannot carry it, lab deviation)** | row 3's printed undo | AZ-3R, AZ-5 |
| **AZ-1X** [F4] | Builder (repo, server) | the OXPd 1.x callback credential (02:613 item 2): prerequisite for AZ-CX | revert PR | design pass |
| **AZ-CX** [F1, F4, F7, F10] | Builder (repo) | product connector (container + appliance + Windows service, day one), sidecar, ceiling, PROXY header, admin listener, enrolment, audit, security review pts 1-14 as tests | revert PR | AZ-T pass, AZ-1X, package card |
| **AZ-V** [F6] | Builder (repo) + optional lab | VPN transport module and install docs (B2165 §2 a/b/d); lab build only if Kam rules it or AZ-T fails | delete per Q11 | AZ-1 |
| AZ-9 | Later | ARM-TTK and createUiDefinition sandbox | n/a | AZ-1 |

**Order:** AZ-T now (A$0; transport card ruled a: free test first) → AZ-1 (no spend) in parallel → Kam rules the spend card → AZ-0 Kam's clicks → AZ-4 + AZ-2R + AZ-CA → AZ-5 → AZ-3R/AZ-8. If AZ-T fails: AZ-V lab instead of AZ-2R/AZ-3R, with the VPN lines of §8. Dates are not re-estimated here (B2165's M-a "about Wed 2 Dec" assumed the card on Mon 30 Nov and no AZ-CA ceremony; the ceremony adds about half a day, ESTIMATE).

**Edits owed to B2154 / B2156 (from B2165 §4, revised):** item 1 reads "reaching the M577 through the Site Connector (or the VPN transport, chosen by AZ-T) (K11b c; P-4 ruled: server in the client's Azure, the product owner's 27 Nov ruling)" [F3, F9]; item 3: L9 replaced by AZ-T (store-only, LAN) then AZ-8; item 5: device-run lanes gain "needs AZ-3R/AZ-8 up" (or AZ-V); others as B2165.

## 7. Questions for Tuesday (each with a default)

- **Q-D1 [F3] P-4 into the design record:** Kam ruled `datasec-oxpd-p4-confirm-1127` a (18:30, RELAYED). Record P-4 in 02 / CLARIFICATIONS as "Phase 1: server in the client's Azure (Marketplace) + Site Connector on site; on-site server a later optional form; supersedes q05 a for Phase 1", citing the product owner's 27 Nov ruling (no card id in project text). *Default: yes, by a records seat Tuesday commissions after printing the ruling herself.*
- **Q-D2 [F2] SAS:** if AZ-2R finds `RootManageSharedAccessKey` present and not removable, regenerate both keys, hold neither, and audit. *Default: yes; recorded as a deviation.*
- **Q-D3 [F4] 1.x callback credential:** prerequisite for AZ-CX, not for the lab. *Default: yes; Tuesday commissions the design pass that adds it and the Site Connector component (B2165 Q20, now on Kam's P-4 ruling rather than a default).*
- **Q-D4 [F5] Server signing right:** assign "OXPd CA Signer" (sign-only, one key) to the VM identity. *Default: yes, per the commission's "server reads with least privilege"; if the server needs no issuance in release 1, leave it unassigned and renew by ceremony.*
- **Q-D5 [F5] Root key copies:** encrypted image under the OXPd `3_Access_Keys/` plus Kam's removable media. *Default: yes; destroying the root after signing is the alternative (no CRL renewal then, issuing CA re-done at expiry).*
- **Q-D6 [F7] Windows connector on day one:** *Default: yes (q14 c); if Tuesday reads C-17 as binding the server only, it goes to Kam as a card, not a default.*
- **Q-D7 [F6] Namespace per client vs per site:** *Default: per client, per site above 500 printers or on request.*
- **Q-D8 [F2 sub] No public IP on the VM (NAT gateway):** *Default: keep the inbound-denied public IP for the mock; price NAT gateway by a portal quote in AZ-1 (API returns no rows).*
- B2165 Q1-Q8, Q10-Q17 stand; **Q9 withdrawn [F5]**; **Q18** answered by Kam's ruling a on the transport card (18:30, RELAYED); **Q19 replaced by Q-D6 [F7]**; **Q20 replaced by Q-D3 [F3]**.

## 8. Spend card draft (for Tuesday to file; nothing is spent before Kam rules it)

**Title:** OXPd: monthly cost of the pretend customer in Azure, with the security fixes (over A$50)
**BLUF (plain words for Kam):** After the free printer test passes, we build the pretend customer in your Azure group: one small server, its database and backups, two locked safes (one only for the certificate signing key, which agents cannot open), a log store, and the private meeting point that carries your printer's traffic, locked so only your office and the server can use it. **About A$116 a month left on, A$78 with the server switched off out of hours, A$58 with the printer link off too.** Each line is below. It is over the A$50 a month line, so it needs your yes. If the printer test fails, the VPN lines replace the Relay lines (about A$316 a month, B2165).

| Resource | AUD per month (always on) | Off out of hours (~217 h) |
|---|---|---|
| Server VM B2s | 54.75 | 16.28 |
| OS disk E4 | 4.64 | 4.64 |
| Data disk E6 | 9.28 | 9.28 |
| Server public IP (inbound denied) | 5.18 | 5.18 |
| Public DNS zone | 0.71 | 0.71 |
| Backups (ESTIMATE) | 2.88 | 2.88 |
| Relay listeners × 2 | 27.74 | 8.25 |
| Relay private endpoint | 10.37 | 10.37 |
| Private DNS zone for Relay | 0.71 | 0.71 |
| Key Vault × 2 | ~0.02 | ~0.02 |
| Log Analytics (under 5 GB) | 0 | 0 |
| Relay data (under 5 GB) | 0 | 0 |
| **Total** | **116.28** | **58.31** |
| Admin link, on demand | up to 13.87 | ~4.12 |
| **The A$50/month line** | **over: card** | **over: card** |

Not in the totals (separate asks): the mock-client domain (yearly, price UNMEASURED); Microsoft 365 licences for the test user (UNMEASURED); NAT gateway if a no-public-IP server is wanted (UNMEASURED).
**Kam's own clicks on the same card:** register `Microsoft.Relay` on the subscription; create `oxpd2-ca-rg`; make the role assignments K-RBAC (VM identity: Relay Listener on `lab-to-server` and `lab-admin`, Relay Sender on `lab-to-site`, Key Vault Secrets User on its named secrets, OXPd CA Signer on the issuing key; lab connector identity: Relay Listener on `lab-to-site`, Sender on `lab-to-server` and `lab-admin`; app SP: Monitoring Metrics Publisher on the DCR; ceremony principal: Key Vault Certificates Officer on `oxpd2-ca-kv` for the ceremony window only); type the CA passphrase at the ceremony.
**Options:** [a] Yes, build it with the stop/start rule (recommended); [b] Yes, always on; [c] Not yet. **Default:** c (nothing is spent).

## Sources
- Commission B2169 (whole); `DRAFTER_RULES.md` (whole); B2165 (whole, 244 lines); B2167 (whole, 92 lines).
- Cards printed by `decision_queue.sh show` into scratch, 18:28:47: `datasec-oxpd-p4-confirm-1127`, `datasec-oxpd-printer-path-design-1127`.
- Microsoft Learn, opened 18:27-18:28: azure-relay/network-security; azure-relay/authenticate-application; azure-relay/private-link-service; azure-relay/ip-firewall-virtual-networks; key-vault/general/rbac-access-policy.
- Azure Retail Prices API (AUD): Hybrid Connections (3 rows), Private Link (Standard Private Endpoint 0.0142/h; data processed 0.0142/GB), Key Vault (17 rows), Azure DNS private zone 0.7106, NAT Gateway 0 rows; 18:26:57-18:27:23. `cost.py` 18:29:00.
- Not done: no Azure, device, OXPd repo, Jira or GitHub read or write; the Relay FAQ, Arc network-requirements and Key Vault rbac-guide pages not re-opened (their facts are RELAYED from B2167 or marked UNMEASURED); Relay SLA and throughput still have no documented figure.
