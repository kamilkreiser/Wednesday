DONE

# B2154 (lane P): OXPd, the critical path to a WORKING COPY by Thursday 2026-12-24

Read-only analyst for Tuesday (s333), written 2026-11-27 (clock at writing: `date` printed Fri 27 Nov 2026 17:02:16 AEDT). Commission: `tuesday/briefs/2026-11-27_B2154_OXPD-WORKING-COPY-CRITICAL-PATH_COMMISSION.md`, section "B2154 (lane P)". Scratch: `fleet/state/s333/d2154/`. No dotnet job was run (the one-wave-lock rule): every expectation below is PREDICTED. Fact marks: **MEASURED** (I ran the instrument named), **RELAYED** (from a record, not re-checked), **UNMEASURED**. `<P>` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2`. `03:n` / `02:n` = line n of the design docs as the Read tool printed it today.

## BLUF

1. **No reading of "working copy" in the plan's own terms is reachable by 24 Dec except phase 2's slice on the M577.** Phase 1 (the OXPd 2 slice) needs an OXPd 2 printer or the simulator, which nobody holds (03:389); release 1 (E6.8) is full parity on both platforms and both packagings. The reading taken here: **the phase-1 goal flow (03:202), run on the OXPd 1.x M577, as phase 2 defines it (03:219, E2.1 = E1.1-E1.8 on OXPd 1.x), on one packaging, on the lab network, no Azure, no HP.** This is also the core of Tuesday's own unruled 20-December proposal (03:116).
2. **What main has is libraries, not a flow.** 58 pull requests are merged (MEASURED); the server host wires only the OXPd 2 callbacks and the secret store (`src/Datasec.Suite.Server/Datasec.Suite.Server.csproj` references Core, Adapters.Oxpd2, Secrets only; its README: "no database start, no admin API, no Universal Print and no sign-in"). **Missing for the flow, in order of risk:** (i) the OXPd 1.x agent side (server-hosted SOAP endpoints the printer calls: pre-prompt, prompt page, post-prompt, HID reports): no code, no package, spike S2 not run; (ii) Microsoft sign-in from the server (no auth-code, device-code or token-endpoint code anywhere on main); (iii) the panel pages (ES5 template, WP2.3): none; (iv) the host composition; (v) OXPd 1.x scan: no HP scan-service description is committed; (vi) the network path printer-to-server (owed 118) and the dev CA in the M577's store (owed 103), both unrun.
3. **Critical path: eleven lanes, about 16 lock-days of build in 18 working days (Mon 30 Nov to Wed 23 Dec).** It fits only if (a) the OX-A / OX-B / OX-D hygiene lanes and owed 121 give the wave lock to the path until 18 Dec (OX-C's owed 137/138 stays: the hang burns lock time), and (b) Kam supplies the test tenant user and app registration, a card reader, and the router route by **Mon 7 Dec**.
4. **Six things need Kam (cards), none needs HP, Azure is optional.** OXPd 1.x needs no HP signing (02 §4 signing row: "None; no HP approval for 1.8"). The cards: the working-copy scope (K1), the tenant pieces (K2), a reader (K3), the agent that takes over the M577's sign-in (K6), the home-screen button (K7; C-84 requires asking), the server's host name (K11). Two device items are already ruled (K4 route test, K5 CA import: C-84, C-87).
5. **The records disagree with the code in eight places** (section F); the largest: `03 §0` still describes main at 44 PRs (b0b26b60), lists WP1.8 OneDrive as "not started" (PR 50 landed browse), and says first-run rows 2 to 4 are not built (PRs 47, 52, 53 built them).

## A. What "a working copy" can mean, quoted from the plan

| Reading | The plan's words (quoted) | Reachable by 24 Dec? |
|---|---|---|
| R1 Phase 1 exit | Goal 03:202: "a user taps a known card at an OXPd 2 printer, is signed in (No-MFA and MFA via device code) [B1817: (No-MFA, and MFA through Microsoft's page on the panel)], opens OneDrive, scans a page into a folder, prints a PDF from OneDrive, signs out; a card enrolled on the Workpath printer works." Exit E1.1-E1.9 (03:207-215). | **No.** 03:389: "No OXPd 2 device in LDB or simulator host → phase 1 and spikes S1, S3 (OXPd 2 half), S4, S6 (OXPd 2 half) and S8 blocked; phase 2 can start alone." Jira OXPD2-56 (Kam chasing HP for tools, simulator, firmware) open at the 11-26 census (RELAYED). |
| R2 Phase 2 exit | Goal 03:219: "E1.1 to E1.8 pass on the FutureSmart 4.7/5 device through the OXPd 1.x adapter with no change in the core." Exit 03:221: E2.1 = E1.1-E1.8 on OXPd 1.x; E2.2 wake-from-sleep 95/100; E2.3 disk-initialise and drift repair; E2.4 core references neither adapter; E2.5 panel memory within 2 MB, 500-cycle soak. | **Partly.** The M577 is OXPd 1.x, FutureSmart 5, firmware 5.10.0.7 (C-84, read on the device, RELAYED). E1.3 needs a Workpath printer (none in the lab flow); E2.3 needs a disk initialise (C-72 forbids wipe/reset by agents); E2.2/E2.5 are soak work beyond a first copy. |
| R3 Release 1 | 03:135: "Release 1 is everything, on both platforms, in both packagings"; E6.8 parity gate (03:251). | **No** (03:87, 03 §0.5, Tuesday's own estimate of 2026-11-24: neither of his dates holds full parity). |
| R4 His words | C-80 q13: "phase 1 needs to be a fully operational build."; s4: "OXPd 1.9 by 20 Dec OXPd 2 by 12 Jan"; C-81: "OXPd 1.x ships first: re-plan to the dates"; Tuesday terminal 2026-11-27: "a working copy before chistmas" (pickup line 12, RELAYED). | Whether "phase 1" is the plan's phase 1 or his first release is NOT decided (03:95). 03 §0.5.3's eight yes/no questions for him: **no C-entry records an answer** (MEASURED: `grep -i -c '20 December'` on CLARIFICATIONS.md = 2, the only content hit is C-81's re-plan line 978; `pilot` = 1 hit). |

**Reading taken (K1 asks him to confirm):** R2 narrowed to **WC-1**, the phase-1 goal flow on the M577:

- **WC-0 (walking skeleton, no card):** at the M577 panel a user starts sign-in on the server's prompt page, completes Microsoft's sign-in (on the panel per B1817 R1-29, or by device code QR if the C-76 test shows the old panel cannot), sees their OneDrive My Drive, scans one page into a folder, prints a PDF from OneDrive, signs out; the server's session and tokens are gone afterwards.
- **WC-1 (the target):** WC-0 plus a known card tap (No-MFA and MFA) on a reader on the M577, enrolment by Microsoft's page (minimal, WP1.4), second tap signs out.
- Exit checks taken from the plan for WC-1: E1.2, E1.4, E1.5, E1.6 (PDF only; DOCX needs the converter, WP0.9 not started), E1.7, E1.8, each on OXPd 1.x; E1.1 measured and reported but NOT gating (50 taps need a person); E1.3 and E1.9 and E2.2-E2.5 out of the working copy, said so.
- One packaging: the server run from a build on the lab Mac (192.168.20.220, RELAYED from owed 118); the Linux container exists only as CI's build (owed 5).

## B. Built on main, missing, owed

Main: `760e1a644ce9a419cf1b9132d0776e9e5eac1cac` (PR 58), `gh api -X GET repos/datasecau/OXPd_2/commits/main` at 16:59:06 AEDT (MEASURED). PRs: 58 of 58 closed with a merge time, 0 open (MEASURED, `pulls?state=all`). Tree: 679 blobs, 18 src projects, 18 test projects (MEASURED, git trees API; file `scratchpad/tree.txt`). The local checkout is stale (HEAD 6e2629bc): every code read was by GET at 760e1a64.

### B1. Built, by module (PRs from the titles, MEASURED; "device" = has it run on the M577)

| Module (src) | What it does today | PRs | Device |
|---|---|---|---|
| CI, guards (`build/`, `ci.yml`) | Linux+Windows legs, secret scans, release guard, rules R1-R8, squash scan | 1, 8, 16, 19, 49 | n/a |
| Contracts | OXPd 2: 37 HP spec files, generated clients; OXPd 1.x: 23 HP files in 9 service folders (authentication, authorization, accessories, certificatemanagement, deviceinfo, test, uiconfiguration, common, domain security) | 6, 7, 14, 37, 38, 43 | no |
| Adapters.Oxpd2 | token holder, callback credential check, five callback handlers, device token client | 13, 21, 33, 46, 57 | no (no OXPd 2 device) |
| Adapters.Oxpd1 | Datasec's own SOAP 1.2 **client**: discovery + five reads; writer: register/unregister a test sign-in agent, CA import/remove, top-level button register/unregister; Test-service echo with a loopback callback listener | 37, 40, 41, 47, 51-54 | rows 0,1,2,5,6 ran (C-84, C-88, RELAYED); rows 3, 4 not run |
| Lab (`oxpd1`, `print`, `probe`) | drives the M577 over the network; one synthetic page printed by IPP on 2026-11-24 (C-84) | 34, 39, 40, 42, 44, 45, 47, 48, 51-53, 55, 56 | yes, partly |
| Server | `/health`, five OXPd 2 callback routes, a notification route, HTTPS-only | 36 | no |
| Secrets, Data, Devices | encrypted local store with rotation; EF registry, PostgreSQL+SQL Server migrations, clock check | 5, 11, 12, 24-26, 30 | library only, not wired |
| Cards | five decoders, reader table, read assembly | 3 | no |
| SignIn | per-printer actor, card paths, binding rule, stale-tap guard, display names (against fakes) | 23, 28 | no |
| Identity | card store in custom security attributes (find by card, enrol under 15-card limit) against a fake Graph | 27, 29, 32 | no |
| Sessions | token broker: sessions, opaque handles, bounded refresh via `ITokenRefresher` | 9, 18 | no |
| Graph | paging, Retry-After, one refresh on 401, chunked uploads; `IGraphTokenSource` interface | 10, 57 | no tenant |
| OneDrive | browse My Drive (root or one folder), list-children only | 50 | no tenant |
| Jobs, Jobs.Transport | streaming scan receiver, encrypted spool, IPP Print-Job sender; IPP over HTTPS pinned | 15, 20, 35 | the lab print used the transport (RELAYED) |
| Logging | field deny-list and log scanner, not wired | 2 | n/a |
| UniversalPrint | registration material, IPP encoder (not on the WC path) | 4, 17, 22, 58 | no |

### B2. Missing for WC-1 (MEASURED absences, each with its control)

| # | Missing | Evidence (instrument; control) |
|---|---|---|
| M1 | **OXPd 1.x agent side**: server endpoints for `GetPrePromptResult`, the prompt page target, `GetPostPromptResult`, `HidReportEvent`; and the client calls `ReserveAuthenticationContext`, `HidOpen`, `HidStartReading` | tree grep `corewcf|agent|panel|html` -i: 7 hits, none in src beyond `DocumentRange.cs` (word "agent" only in contract paths); `Directory.Packages.props` lists 7 packages, no CoreWCF; `Oxpd1Client.cs`/`Oxpd1Writer.cs`/`Oxpd1Read.cs` grep for `HidOpen|HidStartReading|ReserveAuthenticationContext`: 0; control: same grep finds `RegisterAuthenticationAgent` 6 and `ImportCertificate` 4 in `Oxpd1Writer.cs` |
| M2 | **Microsoft sign-in by the server** (auth code + PKCE for the panel page, device code as fallback; the app's own token for the card store; refresh) | tree grep `msal|devicecode|oauth|entra` -i: 0 in src; control: the same grep finds `UnauthorizedTests.cs`. `IGraphTokenSource` and `ITokenRefresher` are interfaces with fakes only (file list) |
| M3 | **Panel pages** (ES5 template for WebKit 534/605, within 2-3 MB, no pop-ups) | no `.html`, no `wwwroot`, no Panel project in the tree (grep above); WP2.3 and WP1.6 "not started" (03:40, 03:47 rows, RELAYED) |
| M4 | **Host composition**: registry, secret store, broker, sign-in actor, identity, Graph, OneDrive, jobs and the OXPd 1.x agent behind one host | Server csproj: 3 ProjectReferences (MEASURED); Server README "Nothing else is wired yet" |
| M5 | **OXPd 1.x scan**: the scan service's HP description and a client call | `contracts/oxpd1/hp/` holds 9 folders, none a scan service (MEASURED); 02 §4 scan row: "Scan service only with the app's UI context, not the sign-in one" (which HP service and file: UNMEASURED by me) |
| M6 | **OneDrive scan-to-folder and download-for-print** | OneDrive README: "one Graph call", list-children only (MEASURED); the Graph layer has chunked uploads (PR 10) |
| M7 | **Printer-to-server path**: route 192.168.8 → 192.168.20 (owed 118, untested), server certificate whose CN is a host name the M577 resolves ("Subject CN must match the URI host exactly, no IP addresses", 02 §4 trust row, [C1 §4.2]), the CA of that certificate in the M577's OXPd CA store (row 3 built, not run; owed 103: HP's line "self-signed certificates ... not recommended/supported") | BACKLOG items 103, 118 open (program parse) |
| M8 | **Onboarding v1 for one 1.x device** (agent + accessory + button + CA, read-before-write, undo) from the server rather than the lab | lab verbs exist per write kind; no engine (WP2.2 not started, 03:47 RELAYED) |
| M9 | **A reader on the M577 and a tenant with the CSA attribute set, a test user with Authenticator, and an app registration** | OXPD2-61 (test tenant user) open at the 11-26 census (RELAYED, `fleet/state/s328/sweep0446/OXPD2.tsv`); no C-entry after C-76 records a user or a reader |

### B3. Owed

BACKLOG.md: **160 numbered, 89 open, 71 ticked** (MEASURED, python regex `^(\d+)\. - \[( |x)\]` over the file; control: items 1 and 160 parsed). Material to WC-1: **103** (dev CA on the M577), **118** (call back to the Mac), **137** (Server.Tests hang, in B2153), **138** (heavy.py orphan, named in B2153), **140** (1.9 SDK: nothing built on 1.9 before HP's package, C-85), **115** (`remoteItem` tenant test; WC-1 can skip remote items), **1** (SPU: OXPd 2 only, off the WC path), **92** (design facts A1-A4, A16). The other ~81 open items are hygiene and record points (SWEEP-0446 lanes OX-A..D and OX-R, plus kits since): none blocks WC-1.

## C. The dated critical path (lanes)

Working days: Mon 30 Nov - Fri 4 Dec, Mon 7 - Fri 11 Dec, Mon 14 - Fri 18 Dec, Mon 21 - Wed 23 Dec = 18 (weekdays by `date -j`; Thu 24 Dec kept as the hand-over day). Sizes in **lock-days** (days a builder holds the one wave lock, gate and fix round included), my estimate, not measured. "Kam/HP/Azure/device" columns: Y = needs it (card list in C2).

### C1. Lanes

| Lane | What | Files (owned; DISJOINT) | Size | Depends on | Device | HP | Azure | Kam |
|---|---|---|---|---|---|---|---|---|
| **L0 Scaffold** | Empty projects + test projects for L1, L2, L4, L7, their slnx entries, lock files; nothing else | `Datasec.Suite.slnx`; `src/Datasec.Suite.Adapters.Oxpd1.Agents/` (new); `src/Datasec.Suite.Identity.Entra/` (new); `src/Datasec.Suite.Panel/` (new); `src/Datasec.Suite.Onboarding/` (new); matching `tests/*.Tests/` | 0.5 | none | - | - | - | - |
| **L9 Network path** | Run row 3 (dev CA import, then remove) on the M577; `oxpd1 echo` async callback from the M577 to the Mac across the route; record whether HP's store takes the dev root (closes or narrows owed 103 and 118) | no repo file (evidence in `<P>/1_Project_Definition/Briefs/` STATUS and `.tools/b<n>/`) | 0.5 (lab binary build only) | L0 not needed; Kam's router route (K4) | Y | - | - | ruled (K4, K5) |
| **L1 Agent host (S2, code half)** | SOAP 1.2 endpoints the M577 calls: authentication agent (pre-prompt, post-prompt, sign-out notification), prompt-page target, HID report event; `ReserveAuthenticationContext`/`Release` and `HidOpen`/`HidStartReading` client calls; WS-Addressing per the switch of PR 40; contract tests against the committed 1.x descriptions | `src/Datasec.Suite.Adapters.Oxpd1.Agents/**`, `tests/Datasec.Suite.Adapters.Oxpd1.Agents.Tests/**` (calls the existing client by its public API; no edit in `Adapters.Oxpd1/**`) | 3 | L0; K9 (framework) | - (code) | - | - | K9 is Tuesday's |
| **L1d S2 device half** | Register the sign-in agent pointing at the Mac host (undo printed); a panel sign-in reaches `GetPrePromptResult`; answer `Continued` then a stub page; unregister | no repo file | 0.5 | L1, L9 | Y | - | - | **K6** |
| **L5 OneDrive slice 2** | Upload a scanned file into a chosen My Drive folder (upload session); download a file's bytes for print; tests against the fake | `src/Datasec.Suite.OneDrive/**`, `tests/Datasec.Suite.OneDrive.Tests/**` | 1 | none | - | - | - | - |
| **L2 Entra sign-in** | Confidential-client token code: auth code + PKCE (panel page), device code (fallback), app token (card store), refresh behind `ITokenRefresher` and `IGraphTokenSource`; secrets only through the secret store | `src/Datasec.Suite.Identity.Entra/**`, `tests/Datasec.Suite.Identity.Entra.Tests/**` | 2 | L0; K2 for the live check (unit tests need no tenant) | - | - | - | **K2** |
| **L-C76 Panel test** | C-76's test: one plain page on the M577 panel that starts Microsoft's sign-in; memory and certificate trust measured; result and options to Kam | page served by a lab-only route in `src/Datasec.Suite.Panel/**` (L4's project; L4 not yet running) | 0.5 | L1d, L2, K2 | Y | - | - | ruled C-76; result goes to him (K14) |
| **L3 Host composition** | Wire registry, secret store, broker, sign-in actor, identity, Graph, OneDrive, jobs, the 1.x agent host and the panel into `ServerHost`; one config file; host-name TLS | `src/Datasec.Suite.Server/**` (README included), `tests/Datasec.Suite.Server.Tests/**` | 2 | B2153 landed (it owns `HostRig.cs`, owed 137); L1, L2 | - | - | - | - |
| **L6 1.x scan** | Commit the HP scan-service description(s) from the pinned 1.8.4.1 jar (by sha256, as PR 43 did); client call that starts a scan in the app's UI context to the server's receiver | `contracts/oxpd1/**`; `src/Datasec.Suite.Adapters.Oxpd1/**`, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/**` (**OX-A's paths: OX-A must not run beside it**) | 2 | none for code; device run after L3 | Y (run) | - | - | K8 ruled by C-74 reading |
| **L4 Panel pages** | ES5 pages: prompt (Microsoft page start, or QR device code per L-C76), OneDrive browse, scan-to-folder, print, sign-out; page weight budget printed; no script over 2 s | `src/Datasec.Suite.Panel/**`, `tests/Datasec.Suite.Panel.Tests/**` | 2 | L-C76 result; L3 for routes | Y (screens) | - | - | K7 for the button |
| **L7 Onboarding v1 (one device)** | Server-side: CA, agent, accessory, one OneDrive button; read before write; undo list; drift read | `src/Datasec.Suite.Onboarding/**`, `tests/Datasec.Suite.Onboarding.Tests/**` | 1 | L1, L3 | Y | - | - | **K6, K7** |
| **L8 Card path** | HID reports → decoder (PR 3) → card store (PR 27) → sign-in actor (PR 23) wired; enrol by Microsoft page (minimal) | `src/Datasec.Suite.Adapters.Oxpd1.Agents/Accessories/**` (+ its tests folder) — same project as L1, so **after L1**; no edit in Cards/SignIn/Identity unless a defect is found | 2 | L1, L2, L3; K3 reader; K2 CSA attribute set + test card | Y | - | - | **K2, K3** |
| **L10 End-to-end** | Run WC-0 then WC-1 on the M577; evidence per exit check (E1.2, E1.4-E1.8 on 1.x); E1.8 log scan with planted marker; runbook | `<P>/1_Project_Definition/Briefs/` STATUS; fixes go to the owning lane's paths | 1 + fixes | all | Y | - | - | demo |
| **OX-R Records** | as SWEEP-0446; also the docs fact corrections of section F | records files only | 0 lock | landings | - | - | - | - |

Lock-days on the path: L0 0.5 + L9 0.5 + L1 3 + L1d 0.5 + L5 1 + L2 2 + L-C76 0.5 + L3 2 + L6 2 + L4 2 + L7 1 + L8 2 + L10 1 = **18**, minus the device-run halves if Q3 lets them run without the lock (L9, L1d, L-C76 = 1.5) = **16.5**, plus B2153 (1, already commissioned). Available: 18. **Slack is about one day.**

### C2. Cards (Kam's word, a device run, HP or Azure), one sentence each, with a default and what already rules it

`decision_queue.sh prior` (read-only) was run for six titles (file `fleet/state/s333/d2154/prior.txt`): each returned the same 72 OXPd cards on the shared word "oxpd" only, so it discriminates nothing here; the rulings below are from CLARIFICATIONS.

| Card | Question (one sentence) | Default | Already ruled by |
|---|---|---|---|
| **K1** | Is the Christmas working copy the sign-in, OneDrive browse, scan-to-folder and print-a-PDF flow on your M577 (an older printer), on the lab network, with OXPd 2 and every other app after? | yes (WC-1; WC-0 if no reader) | none: 03 §0.5.3 Q1 is unanswered (section A) |
| **K2** | Can you give us, in the `datasec-rd.com` tenant, one test user with Authenticator, an app registration we may use, and the custom security attribute set the card store needs, by Mon 7 Dec? | yes, his w7 tenant | OXPD2-61 asks the user (open, RELAYED); C-76 "Needs a test tenant user from you"; C-80 w7 names the account; the app registration and attribute set are NOT asked anywhere I found |
| **K3** | Can you plug one card reader (and one test card) into the M577 by Mon 7 Dec? | yes; without it the copy is WC-0 | C-80 q34 "we have multiple printers ready" (no reader named); OXPD2-30 asks Workpath to lend readers (open) |
| **K4** | (Device run) Test the printer-to-Mac call back across your two networks. | an agent tests it; if blocked, he opens the route on his router | **C-84** (his tap 14:58 "Route both ways", detail "open a route from 192.168.8 to this Mac (your router); we test the callback"); owed 118 |
| **K5** | (Device run) Import and remove the development CA in the M577's OXPd CA store. | run it | **C-84** 14:06 "please do what you need to set up the printer for the OXPd project", limited by **C-72** (no firmware change, no wipe, no reset); **C-87** names it a later step of the coordinator's |
| **K6** | May an agent register the real sign-in agent on the M577 pointing at the server, so the panel's sign-in goes through our server during test runs, with the undo printed and run at the end of each session? | yes, during his working hours | C-72's first-run list has a TEST sign-in agent (row 5) only; C-84 covers set-up, not a sign-in takeover: card needed |
| **K7** | May an agent add one OneDrive button to the M577's home screen for the test runs, removed by undo after each? | yes | **C-84** detail "We ask again before any home-screen app is added" (C-88: "no button is put on the M577 until he answers"): card REQUIRED |
| **K11** | Which host name does the M577 use for the server: a name on your router for the lab Mac (no cost), or the small Azure machine in `oxpd2-dev-rg`? | a router name for the Mac; no Azure | N-5 open; C-75/C-78 approve one small test VM for the S14 path test only; C-81 allows agents in `oxpd2-dev-rg`, spend over about A$50/month to him (coordinator's reading) |
| **K14** | (After L-C76) If Microsoft's page does not work on the M577's old panel, do we use the QR device code on the panel for the working copy? | yes, QR device code | C-76 says the result goes to him "with options"; N-3 open |
| K8 | (Tuesday's, no card) Commit HP's 1.x scan-service description from the pinned jar. | yes | C-74 ("allows us to use HP code"), C-56 tap "Keep HP's files in the repository", coordinator's reading (owed 86) |
| K9 | (Tuesday's, no card) The 1.x agent host: hand-written SOAP 1.2 endpoints on ASP.NET Core like the PR 37 client, or CoreWCF (a new package, a supervised fetch as C-61/C-62)? | hand-written (no package fetch; design says CoreWCF is "inferred", 02 §1 item 7, and "firm after spike S2") | none |
| K10 | (no card) Build on 1.9? | no: nothing on 1.9 before HP's package (owed 140) | **C-85** |
| K13 | HP | none for the working copy | 02 §4 signing row (OXPd 1.x needs no HP approval) |

**Board order:** K1, K2, K3, K6, K7, K11 together on Mon 30 Nov morning (one card each); K14 after L-C76.

### C3. Dated schedule (one lock; device runs per Q3)

| Dates | Lock holder (in order) | Beside it (no lock) | Milestone |
|---|---|---|---|
| Fri 27 - Sun 29 Nov | B2153 (owed 137) | drafters for L0, L1, L5; records (OX-R) | cards K1-K11 drafted |
| Mon 30 Nov - Fri 4 Dec | L0 (Mon), L5 (Tue), L1 (Wed-Fri) | L9 device run (Mon-Tue; route test); drafters for L2, L3, L6; cards on the board Mon | **M-a Tue 1 Dec:** M577 calls the Mac back over TLS with the CA in its store (or the blocker is known) |
| Mon 7 - Fri 11 Dec | L1 gate/fix (Mon), L2 (Tue-Wed), L3 (Thu-Fri) | L1d (Tue), L-C76 (Wed, needs K2); drafters for L4, L7, L8 | **M-b Tue 8 Dec:** the M577's panel sign-in reaches our `GetPrePromptResult` (spike S2a); **M-c Wed 9 Dec:** C-76 result to Kam |
| Mon 14 - Fri 18 Dec | L6 (Mon-Tue), L4 (Wed-Thu), L7 (Fri) | device runs of L6 and L4 screens | **M-d Fri 18 Dec: WC-0 end to end** |
| Mon 21 - Wed 23 Dec | L8 (Mon-Tue), L10 (Wed) | evidence, runbook | **M-e Wed 23 Dec: WC-1** (or WC-0 if no reader) |
| Thu 24 Dec | none | hand-over note and demo to Kam | |

## D. What can run in parallel under the one-wave-lock rule

- **No lock at all:** drafters (predict, never build); records (OX-R); this kind of analysis; card drafting; docs fact corrections (section F) in the coordinator's tree; Jira text.
- **Device runs need no heavy job** once the lab tool is built: `oxpd1 echo`, row 3, L1d, L-C76 are a few network requests each. **Proposal (Q3):** a device-run seat uses a lab binary published once into its own `.tools/b<n>/` folder and runs beside the builder, under the runbook's load check (two reads 120 s apart, both under 24). Default: yes.
- **Short project-scoped jobs:** L5, L2, L4, L7 each build one new project and its tests (`dotnet test tests/<one>.Tests`): minutes, not the 15-30 minutes of a whole-solution run that hit owed 137. Even so the commission's rule is one OXPd build seat at a time, so the schedule above does NOT assume two builders. **Proposal (Q4, default NO until 137 lands):** after B2153's bound lands, allow a second builder whose jobs are project-scoped only, never a whole-solution run, under the load check; whole-solution runs only at the gate, under the lock.
- **Path disjointness check:** every lane in C1 owns a distinct path set; the shared files are `Datasec.Suite.slnx` and `Directory.Packages.props`, both given to L0 only (no lane adds a package by default: K9 and Q6). L6 is the only lane inside OX-A's paths and L3 the only lane inside OX-C's Server paths: OX-A must not run beside L6, and L3 starts after B2153 lands.
- **What the path displaces:** OX-A, OX-B, OX-D hygiene and owed 121 (cross-lane) hold no lock until 18 Dec unless a day is free (Q2).

## E. Risks to the date

1. **Microsoft's page on the M577's WebKit** (02 §4 panel row: about 2-3 MB for the whole solution, 10 s script limit, cookies unreliable on FS5): may not render or may not complete. Mitigation: device code QR (K14). Known by M-c, 9 Dec.
2. **Tenant pieces (K2) or reader (K3) late:** L2's live check, L-C76 and L8 slip day for day; without a reader by about 14 Dec the copy is WC-0.
3. **The printer cannot reach the server:** route not open (owed 118), no host name the printer resolves (CN rule), or the M577 refuses the dev root (owed 103, HP's "not recommended/supported"). Then a certificate from a CA the M577 already trusts is needed (cost or Kam's domain: a card). Known by M-a, 1 Dec. This is the first device run on purpose.
4. **S2 itself (L1/L1d):** the printer calling a .NET SOAP 1.2 endpoint is unproven (02 §1 item 7: "inferred: no HP source shows agents hosted on it"); WS-Addressing 2004 vs 1.0 is contradicted between HP's sources (02 §4 wire row, K-2). The design's fallback is a Java sidecar (03:391), which does not fit by 24 Dec.
5. **Lock capacity:** about one day of slack; every fix round, every owed-137 hang (15-30 min each, seen twice) and any hygiene lane on the lock eats it.
6. **People over the holidays:** card taps, the phone and the router need Kam's hands; Fri 25 Dec onward is outside the window, but 21-23 Dec availability is not known.
7. **Usage limits and seat rotation:** earlier today a usage card held gates at 7d 99% (pickup DELTA 1525, RELAYED); a hold of that kind for two days removes the slack.
8. **1.x scan service unknown in the repo (M5):** which HP description and whether the 1.8.4.1 jar carries it is UNMEASURED by me; if absent, scan slips out of WC and the copy is sign-in + browse + print.
9. **Scope reading (K1):** if he means OXPd 2, or Marketplace deployment (C-80 q12), nothing here meets it by 24 Dec (03:389; HP's four undated items).

## F. Where the plan or the records disagree with the code

| # | Record says | Code / origin says (MEASURED unless marked) |
|---|---|---|
| F1 | `03 §0` (03:9-58): "44 pull requests ... `main` = b0b26b60" | 58 PRs; main 760e1a64 |
| F2 | 03:42 WP1.8 OneDrive "not started" | PR 50 landed browse My Drive (`src/Datasec.Suite.OneDrive/`) |
| F3 | 03:77 and C-84: first-run rows 2 to 4 "not built" | row 2 built (PR 47) and ran; row 3 built (PR 52), row 4 built (PR 53), neither run (C-87, C-88 record this; 03 not updated) |
| F4 | 03:36 WP1.2 "server host v0" with the OXPd 2 routes; 03:13 "the building blocks of the server exist" | true as libraries, but the host references 3 projects and its README says no database, no admin API, no sign-in: nothing the plan calls a slice is assembled |
| F5 | 02 §1 item 7: the OXPd 1.x agent side "planned on CoreWCF"; 03:46 WP2.1 "part" | no CoreWCF package, no agent code: WP2.1 has the client half only |
| F6 | 02 §4 maturity row: "OXPd 1.9 ... treat as absent"; 03 "build on 1.8.4.1" | C-85 targets 1.9 once HP's package arrives; the M577 lists `OXPd:Action` and `OXPd:Security` 2025 services (C-85, RELAYED). Owed 140 open |
| F7 | `SETUP_RUNBOOK.md`: `.azure` "empty; no Azure is in use"; "Azure ... nothing exists for this project" | CLAUDE.md and C-81: `oxpd2-dev-rg` and the agent login `oxpd2-claude-deploy` exist; a boundary proof left one empty virtual network (CLAUDE.md, RELAYED) |
| F8 | SETUP_RUNBOOK "Test ... `total: 1`" and the launcher "never run" | main's hosted run reads 2431 tests (pickup DELTA 1534, RELAYED); whether the launcher has since been run: UNMEASURED |

## G. Questions for Tuesday (each with a default)

- **Q1** Reading of the working copy: WC-1 on the M577 as in section A, WC-0 the floor. *Default: yes; put K1 to Kam Mon 30 Nov.*
- **Q2** Do OX-A, OX-B, OX-D and owed 121 stay off the wave lock until 18 Dec unless a lock-day is free? *Default: yes; OX-C's 137 (B2153) stays first.*
- **Q3** May a device-run seat (prebuilt lab binary, no build) run beside the builder under the load check? *Default: yes.*
- **Q4** A second builder for project-scoped jobs only, after owed 137's bound lands? *Default: no until 137 lands, then revisit on 4 Dec.*
- **Q5** L0 (scaffold all new projects and the slnx in one small PR) first, so later lanes never share `Datasec.Suite.slnx`? *Default: yes.*
- **Q6** L2 by hand-written token-endpoint calls over the existing Graph HTTP layer (no new package), not MSAL? *Default: hand-written, with the security review the plan names for WP1.4/1.5; MSAL only through a supervised fetch and a card if the reviewer refuses.*
- **Q7** K9: the agent host hand-written SOAP 1.2 on ASP.NET Core? *Default: yes.*

## H. UNMEASURED and disclosures

- **Jira was not read live.** The commission asks for OXPD2 by GET, and also forbids reading `4_Credentials/`; the project's Jira helpers read `4_Credentials/.env`. I kept the stricter fence and used the 11-26 04:53 census (`fleet/state/s328/sweep0446/OXPD2.tsv`, 59 open; OXPD2-56/-57 In Progress, OXPD2-60/-61 Kam actions open). Changes since then: UNMEASURED.
- **Not read whole:** `02_architecture.md` (read §1, §4, §5.5.2; the rest by heading) and `03` beyond line 421 (§8 questions and the change log; §0-§7 read whole). The 20 CLARIFICATIONS entries C-73 to C-92 were read whole; BACKLOG open items by program, items 92, 103, 118, 137, 138, 140 whole; SETUP_RUNBOOK whole (wide lines cut at 700 characters); history by headings and the newest entries' titles.
- Which HP 1.x service carries scan, and whether the pinned jar holds its description: UNMEASURED.
- Whether Kam already has a reader, a tenant user or an app registration since 11-26: UNMEASURED (no C-entry).
- Every size and date in C is my estimate. No dotnet job, no device contact, no write outside this file and `fleet/state/s333/d2154/prior.txt`.
