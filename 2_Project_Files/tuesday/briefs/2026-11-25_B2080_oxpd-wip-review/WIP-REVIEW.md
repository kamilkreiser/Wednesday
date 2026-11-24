# OXPd: what is useful in the WIP folder (review for Kam)

Commission B2080, 25 November 2026, 10:37 to 10:50 AEDT (clocks from `date`). Kam's request, live board 10:35: "please find oxpd 1.9 and other OSPd relevant files. review to see what is useful /Volumes/DEV-Working/Datasec/WIP".

The folder was read in place and nothing in it was changed. Nothing was run or installed from it, nothing was sent to anyone, and nothing was copied into the OXPd project. Every claim below is traced to a file and line in `REVIEW.md`.

## BLUF

**Most of the folder is already in our library, byte for byte: 2,630 of its 2,652 files, plus the 424 MB simulator zip, which matches a file inside a library zip.** The new material is small, but two finds change the plan for the older printers, and two documents cannot be read until you open them.

1. **OXPd 1.9 has been released, and your M577 already runs it.** HP's release notes in the folder read "Released Version 1.9", dated 9 February 2026, marked HP Confidential. They add two services: an **Action service**, which replaces Callback Operation and "supports filtering and polling to enable remote execution of OXPd services in public cloud and zero trust environments", and a **Security service**, which signs traffic between printer and server. The M577's own service list, saved at its first run on 24 November, already offers `OXPd:Action` and `OXPd:Security` (both revision 2025/01/29). Our design says the opposite: 02 says 1.9 is "soon" and to "treat as absent", and 03 says to build on 1.8.4.1. **What it unblocks:** H7 can now ask HP for the 1.9 SDK itself rather than whether 1.9 exists. The polling service may also bear on N-5 (how printers at a site reach a server in Azure), and 02 currently says a cloud-only server "is not viable without a site relay". **The catch:** the folder does NOT contain the 1.9 SDK. Its "OXpd1.9" demos are the same Demos 1.9 package we already hold, built on OXPdLib 1.8.4, and our 1.8.4.1 library has no client for either new service.
2. **HP's own way to measure panel memory, which C-76 needs.** HP's resource-analysis kit (already in the library, never used) includes `GetMemCounters.exe`, which reads a FutureSmart printer's memory counters over the network. It reports the "Extensibility" figure that OXPd browser pages draw from, with HP's budget of "OXPd Browser Apps: 3MB + Noise Factor + SDK Contribution". That gives the C-76 panel test ("measured for memory") a figure that HP itself defines. It is a Windows program, it needs the admin password, and by default it asks the printer to free memory, so running it is a step beyond C-72's first-run list and needs your word.
3. **HP's troubleshooting guide for printer-to-server connections (new to us).** It covers the M577 test's other measure, certificate trust. It decodes the panel errors step by step: 45.00.1C timeout, 45.00.06 name not resolved, 45.00.33 certificate not OK, 45.00.23 TLS connect error. 02 already cites a partner who failed on 45.00.33. The guide is written for FutureSmart 3 and 4. The M577 runs FutureSmart 5, so whether it applies there is unmeasured.
4. **HP Solution Test Bench 4.17.2.0 (May 2019; new to us).** This is HP's automated test rig for ACT certification: duration reliability, resource profiling, memory leak and performance, plus "Badge Box" automated card swipes (that needs HP hardware). It is the candidate tool for the soak and memory gates in 03: E2.5, the 500-cycle panel soak against the 2 MB budget, and the 1,000-tap card soak. It is Windows only, with SQL Express, and the guide says FutureSmart 3 and 4. Use later.
5. **Two documents cannot be read, by any agent:** "Steves Readme Notes.docx" (probably the guide to the rest) and "Understanding the HP OXPd 1.9SDK.docx". Both carry Datasec's own Microsoft Purview label "Internal Use Only", which encrypts the file to the Datasec corporate tenant. Word opens them for you. Nine other files in the folder (eight PDFs and one Word file) got the same label when they were copied (stamped 2026-11-24 23:27:57 UTC), but each of those has an unlabelled original in the library or a readable twin (the `.odt`), so nothing else is lost.

What changes for you: **one question to you** (open those two documents and save unprotected copies, or paste their text), **one word from you** (whether the C-76 memory reading may use HP's tool), and **H7 rewritten** before it goes to HP (ask for the 1.9 SDK package).

## The items at a glance

| # | Item (WIP path) | What it is | Already held? | Useful for | Verdict |
|---|---|---|---|---|---|
| 1 | `OXpd1.9/` (607 files) | HP OXPd 1.9 release notes (9 Feb 2026, HP Confidential); the "Understanding the HP OXPd 1.9SDK" document (encrypted); HP Demos 1.9 (built 2024-05-01 on OXPdLib 1.8.4) | Demos: yes, 603 of 605 files identical, and the other 2 are the same files after labelling. Release notes and the "Understanding" document: **new** | H7; 02 §4 maturity row; 03 OQ-12 / line 466; N-5; S2; WP2.x adapter | **USE NOW** (release notes): they contradict 02 and 03 and rewrite H7. Demos: reference only (held, used by C1) |
| 2 | `OXPd2-SDK-Beta-10-20260416/` (1,514) | HP OXPd 2 SDK Beta 10, build 20260416.1 | **Yes, every file** (1,514 of 1,514 identical to `2026-11-20_from-product-owner/`), and already analysed in report B4 from this same path | S1, S4, S8, WP1.2 (all via B1 to B4) | **REFERENCE ONLY**: nothing new. Beta 10 matches what 02 assumes |
| 3 | `oxpd-javascript-2/` (74) | HP OXPd JavaScript library 2.6.0 (print, scan, discovery, device info) | **Yes, every file** (74 of 74) | None. C2 says the project does not need it; the 1.9 notes add that 2.6 "does not support the 1.9 release" | **NOT USEFUL** |
| 4 | `OXPD Button/` (5) | HP OXPd Button Manager 1.1.0.0 (© HP 2016, built on OXPdLib 1.7.2) plus a how-to guide for diagnosing printer-to-server connectivity (June 2025), and a note from Steve | Tool: the library holds a **newer** build of 1.1.0 (2025-09-17, on OXPdLib 1.8.4). Guide and note: **new** | C-76 certificate trust; first-run row 4 (test button); S2 TLS and CN match; 02 line 419 (45.00.33) | Guide: **USE NOW** as the error-code key for the C-76 test. Tool: **NOT USEFUL** (superseded; our lab registers its own test button) |
| 5 | `Jedi_Simulator_SDK1/` (7) | HP "Jedi" FutureSmart simulator SDK (inner zip of 2021-06-03: `JediSimulator.msi` plus the IRIS OCR engine), with 5 PDF guides | **Yes**: the inner zip is identical to the one inside the library's `Jedi_Simulator_SDK1.zip`. The 5 PDFs are labelled copies of the library's unlabelled originals | R4 (no simulator yet); WP0.1 lab; kit item 2 | **REFERENCE ONLY**: needs Windows 7 x64 SP1 with IE 8 on VMware, firewall off. It cannot stand in for the M577 in C-76 or S2 (see detail) |
| 6 | `Jedi_ResourceAnalysis_1.2.1/` (442) | HP Jedi Resource Analysis SDK 1.2.0/1.2.1 (2014): memory profiler, `GetMemCounters.exe`, the "dirtying" utilities | **Yes**, 439 identical. 2 are labelled copies of library originals. 1 is **new**: a certificate file (`hpservercertificate.pfx`), see the credentials section | C-76 memory measure; 03 E2.5 (2 MB panel budget); WP6.3 soak | **USE NOW** (method and memory budget for C-76); running the tool needs your word |
| 7 | `STBInstall-Base-files4/` (2) | HP Solution Test Bench 4.17.2.0 (2019-05-07): client and server installers plus 4 guides (ACT certification tests, install and admin, user guide, Badge Box) | **New** (no trace in the library or the project record) | WP6.3 load and soak; WP6.4 certification; E2.5; R10; the 1,000-tap card soak (03 line 362) | **USE LATER** |
| 8 | `Steves Readme Notes.docx` | Steve's notes, encrypted with the Datasec "Internal Use Only" label | **New** | Unknown until read | **Cannot judge**: needs you to open it |

Held means byte-identical by sha256 to a file in `OXPd_2/1_Project_Definition/Source_Documents/`. Every one of the 2,652 files was checked by name and size against the library's 35,223 files, and every candidate match was confirmed by sha256 (all files, not a sample).

<div style="page-break-after: always"></div>

## Detail

### 1. `OXpd1.9/`: HP OXPd 1.9

**What it is.** Three things:
- `1.9.0 Release Notes.txt`. HP header "Released Version 1.9", "HP Confidential", dated "February 9, 2026". Changes: .NET Framework and .NET libraries renamed; "JavaScript ... version is 2.6., which does not support the 1.9 release"; the **Action Service** and the **Security Service** added; "The first fleet release to support the full OXPd 1.9 feature set is FutureSmart 4.7"; "No known issues".
- `Understanding the HP OXPd 1.9SDK.docx`: encrypted with the Datasec label, so it cannot be read here (item 8 has the same problem).
- `hp-ext-oxpd-demos-1.9/`: the same Demos 1.9 package the library holds (revision `6350435c`, built 2024-05-01, ships `OXPdLib-1.8.4.dll`). 603 of its 605 files are identical. The other two (`TestPDFFile.pdf` and a Visio drawing) differ only because the copy was labelled or re-saved.

**What it is not.** It is not the 1.9 SDK. The release notes point to `\OXPdLib\DotNet\Help\OXPdLib-1.9.chm` and the Java docs, and neither is in the folder. The library's newest OXPdLib (1.8.4.1) has proxies for 12 OXPd services plus IPP, and none for Action, Security or CallbackOperation.

**It contradicts the design.**
- 02 line 266 (§4 table, maturity row): "Mature, frozen; OXPd 1.9 "soon" since 2017, treat as absent [C2 §6]". The release notes say: "Released Version 1.9 ... February 9, 2026".
- 03 line 466: "**OXPd 1.9**: build on 1.8.4.1 [C1 §7 Q8] ... HP called 1.9 "soon to be released" in March 2026". The 1.9 notes are dated a month **before** that forum reply, so either the forum reply lagged or the notes were a partner pre-release. **Not established.**
- C1 line 515: "No 1.9 SDK in the library ... Treat 1.8.4.1 as the latest 1.x". The library still holds no 1.9 SDK, so this part stays true.
- Not a contradiction, but it sharpens 03 line 93 (your tap "b: 1.9 means our 1.x line | note: but I will request whether there is anything more recent"). There is something more recent, and the folder holds its notes.

**It ties to a measurement we already hold.** The M577's discovery tree, saved by the first run on 24 November (`OXPd_2/.tools/b2044/ews/m1/m07__DevMgmt_DiscoveryTree.xml.html`), lists `OXPd:Action` (`.../service/action/2025/01/29`) and `OXPd:Security` (`.../service/security/2025/01/29`) beside `OXPd:CallbackOperation` (2019/11/11). So the M577 on FutureSmart 5 already offers both 1.9 services. Brief B2044 line 95 listed `OXPd:Action` among the measured services, but no record links it to 1.9.

**Useful for:**
- **H7**: rewrite it to ask for the full `hp-ext-XX-oxpd-1.9` SDK (OXPdLib 1.9 with the Action and Security clients and their WSDLs), citing the notes of 9 February 2026.
- **N-5 and the 02 network row** ("a cloud-only server is not viable without a site relay"): HP describes the Action service as built for "public cloud and zero trust environments" with "filtering and polling". Whether polling lets a printer work with a server in Azure without inbound traffic to the site is **UNMEASURED** and needs the SDK.
- **S2 and the OXPd 1.x adapter (WP2.x)**: which services the agent uses on a 1.9 printer.
- **C-76 certificate trust**: the Security service is about signed device-to-agent traffic. How it relates to the panel's certificate check is **not established**.

**Verdict: USE NOW** (the release notes). Demos 1.9: REFERENCE ONLY (held; C1 §4.18 already uses AuthnAuthz and PullPrint as skeletons, rewritten without HP's accept-all certificate callback).

### 2. `OXPd2-SDK-Beta-10-20260416/`: HP OXPd 2 SDK Beta 10

All 1,514 files are identical to the copy in `Source_Documents/2026-11-20_from-product-owner/`. Report B4 analysed this same path on 2026-11-20: its licence file lists open-source notices only and holds no HP terms; the folder contains no printer simulator; and B4 lists six points the SDK settles without a printer. **Version against 02:** 02 says "Beta 10 (1 Jun 2026)". B4 line 61 reads the library README as release date 1 June 2026, build `20260416.1`, minimum firmware `6.38.0.793`. The folder name carries the same build. **Consistent, no contradiction.** No passkey, WebAuthn, FIDO or Bluetooth text appears in its specifications, examples or demos, so it does not answer the passkey questions. **Verdict: REFERENCE ONLY.**

### 3. `oxpd-javascript-2/`: OXPd JavaScript 2.6.0

All 74 files are identical to the library's `oxpd-javascript-2.6.0`. C2 line 11: the project does not need it (no sign-in, card reader or statistics services). The 1.9 notes add that 2.6 "does not support the 1.9 release". **Verdict: NOT USEFUL.**

### 4. `OXPD Button/`: HP Button Manager and the connectivity guide

- `ButtonManager.exe` (identical to the one inside `HP Button Manager (GUI).zip`): HP's "OXPd ButtonManager" 1.1.0.0, © HP 2016, built on OXPdLib 1.7.2, zipped 2017. The library already holds a later build of the same version (`HP_OXPd1_ButtonManager-1.1.0`, built 2025-09-17 on OXPdLib 1.8.4). Our lab tool already registers and removes a test button (first-run step 4, contracts in pull request 43). **Not run, and not needed.**
- `steves Readme.txt` (Steve's note): the tool lets you "re-program your OXPD Console App Launch button to point to a new URL ... read the current Button URL etc.. and then create a Test Button with a new URL".
- `How to use the HP Button Manager to identify device connectivity and OXPd issues` (`.odt` readable, LibreOffice, 2025-06-12; the `.pdf` is the labelled copy). A step-by-step device-to-server test: plain HTTP to the IP, then the FQDN (DNS), then HTTPS (TLS). Each step has the panel error and its causes: 45.00.1C timeout (firewall, server down), 45.00.06 name not resolved (DNS suffixes), 45.00.33 "SSL certificate ... not OK" (wrong or missing certificate, IP in the subject on FutureSmart 3, DNS reaching the wrong server), 45.00.23 SSL connect error (no HTTPS binding). Prerequisite: "TCP port 7627 must not be blocked". Stated scope: "All FutureSmart versions 3 and 4".
- **Useful for C-76** (certificate trust): this is the decode table for what the M577 panel shows, and the same HTTP, then DNS, then TLS order is a good shape for the test page's preflight. 02 line 419 already records a partner failing "on memory and CA trust (45.00.33, 45.00.CB)". The guide explains 45.00.33 but not 45.00.CB. Whether it holds on FutureSmart 5 is **UNMEASURED**.

**Verdict:** guide **USE NOW**; tool **NOT USEFUL**.

### 5. `Jedi_Simulator_SDK1/`: the Jedi (FutureSmart) simulator

The inner `Sdk_20210603_2502226_009029_jedi-simulator-sdk.zip` has the same sha256 as the member inside the library's `Jedi_Simulator_SDK1.zip`, and its MD5 matches the `.MD5` file beside it. It holds `JediSimulator.msi` (HP, built 2021-06-03; its launch script says "product=Cordoba") and the IRIS OCR engine 12.3.4 installer (2010). The five PDFs are labelled copies of the library's originals (same creation dates). The originals were read.

**Could it replace a real printer for spikes? No, by its own guide:**
- It needs a Windows 7 Enterprise x64 SP1 PC or VM (tested under VMware), **IE 8 only** ("Newer versions are not supported"), .NET Compact Framework 2.0 and 3.5, .NET 3.5.1 and 4.0, SQL Server Compact 3.5, WSE 2.0, the OCR engine, UAC at its lowest, and the **Windows Firewall disabled**. The panel and the EWS (`http://localhost:4242`) are simulated.
- Which FutureSmart or OXPd revision it simulates is **UNMEASURED**: the guide is from 2014 (v1.5.x), the MSI is from 2021, and neither names one.
- C1 line 116 records HP's note that "Jedi Simulator 1.9 and earlier fail with the .NET example clients unless the line enabling TLS 1.2 is removed". That makes it unfit for the certificate-trust half of C-76.
- C-76 is defined on the M577's real panel, and S2 asks whether "a FutureSmart device" calls our agent. A simulator answers neither. HP's separate OXPd Simulator 1.3 (held) already serves contract tests, with its own warning that its Chromium panel is not the device's WebKit (02 R4).
- One real use: installing it puts HP's `GetMemCounters.exe` in `C:\jedi-simulator\System`. The resource kit (item 6) already contains that tool.

**Verdict: REFERENCE ONLY.** Building an unpatched Windows 7 VM with its firewall off on the lab network is a cost you would have to choose, for little gain over the M577.

### 6. `Jedi_ResourceAnalysis_1.2.1/`: HP's memory-measurement kit

All held except one file (the certificate, below). C1 line 418 judged it "not needed for the port's design". **For C-76 it is the most relevant thing in the folder:**
- `GetMemCounters.exe` reads, over the network from a FutureSmart printer, the counter `JediMem_Extensibility: HighWater`. The kit explains: "Solutions that interact with the browser using the OXPd API will allocate memory out of this quota". It also gives the solution's figure as one high-water reading minus another, taken before and after use.
- HP's limit table: "OXPd Browser Apps: 3MB + Noise Factor + SDK Contribution", with an SDK contribution of "4.955MB (Includes use of SDK UI Widgets)". This matches the 2 to 3 MB budget in 02 (lines 257 and 370) and gate E2.5 in 03 line 221.
- Limits: the memory tool guide warns "At this time, this tool works on CE-based devices". 02 line 257 says FutureSmart 5 is CE-based on some models and Linux-based on others, and **which one the M577 is, is UNMEASURED**. The kit's tested printers stop at 2014 models (the M577 is not listed), though it claims "all released versions of device FW starting with FutureSmart 22.1". It needs the admin password, the OXPd Test service on after each reboot, and Windows. `-memleak` defaults to `true`, which makes the printer run its memory release. The full profiler (`RunMemoryProfileTest.bat`) also "dirties" the printer with print, scan and EWS activity.

**Verdict: USE NOW** as the method and the budget for C-76's memory half. Running any part of it on the M577 goes beyond C-72's first-run list and needs your word (question 6).

### 7. `STBInstall-Base-files4/`: HP Solution Test Bench 4.17.2.0

New to the project. A client and server tool (Windows, SQL Express) that runs "virtual workers" through workflows on real printers, for hours or days. From 4.12.1.0 it automates ACT certification checks: duration reliability, resource profiling, memory leak, performance. "Badge Box (requires proprietary HP HW)" gives automated card swipes. For a solution like ours, the extra capabilities apply only if the partner "writes the appropriate STB Plugins". Without plugins, only the memory-leak snapshot and the "dirtying" part of resource profiling run. Supported: FutureSmart 3 and 4; "Pro" and "Oz" not supported; FutureSmart 5 and 6 are not named (the guides date from 2017 to 2019). The plugin SDK is "provided separately" and "may not be available".

**Useful for:** WP6.3 (load, soak), WP6.4 (certification) and E2.5 (500-cycle panel soak), the 1,000-tap card soak (03 line 362), and R10. **Does it answer an open question?** No. It raises one (question 7): 03 records no HP approval step for OXPd 1.x, so whether ACT applies to us at all is HP's to say. **Verdict: USE LATER.** Installers stay zipped. Only the guides were extracted, into scratch.

### 8. `Steves Readme Notes.docx`

An Office file encrypted by Microsoft Purview: label "Internal Use Only", Datasec corporate tenant `ae7a1e46-…` (your Corporate environment). It is not a password file and no agent can read it. Its name suggests it is the guide to the rest of the folder. **Cannot judge until you open it.**

### Credentials and certificates (location only; no value opened, printed or copied)

| Location (inside WIP) | What | Note |
|---|---|---|
| `Jedi_ResourceAnalysis_1.2.1/MemoryProfiler09-25-2014/DirtyUtilities/Configuration/hpservercertificate.pfx` | a certificate store (1,803 bytes), probably with a private key | **NOT in the library copy** (Friday's library has the same folder without it). HP's test-harness certificate. Not opened. Never import it into any lab machine |
| `OXPd2-SDK-Beta-10-20260416/tools/certificates/ExtSDKRootCA.key` (and `.pem`) | private key of HP's development root CA | Already flagged by B4 §7; held in the library |
| `Jedi_ResourceAnalysis_1.2.1/MemoryProfiler09-25-2014/*.xml`, `DirtyUtilities/DeviceUnderTest.xml`, `TestRunConfig.xml`, `EwsIntegrated/*.xml`, `SNMP/SNMP.xml` | `<Password>` elements for the printer admin, network share and FTP | Placeholders by HP's guide (`adminpw`, `{userpw}`); to be filled per run, never committed |
| `OXpd1.9/hp-ext-oxpd-demos-1.9/Demos/AuthnAuthz/AuthenticationAgent/users.xml` | HP demo users' passwords in plain text | Already flagged by C1 line 536 |
| `OXPd2-SDK-Beta-10-20260416/demos/*/dotnet/*/appsettings.json`, `tools/postman/CDM.postman_collection.json` | password fields of demo settings | Held; B3 §8 and B4 §7 cover the demos |

<div style="page-break-after: always"></div>

## Questions this raises (one per item)

1. **[HP]** (item 1, replaces H7's points 1 and 2) We hold HP's OXPd 1.9 release notes of 9 February 2026, and our FutureSmart 5 printer already offers the Action and Security services. Please send the full OXPd 1.9 SDK package (OXPdLib 1.9 with the Action and Security service clients, their WSDLs and the 1.9 guides), or tell us how to get it.
2. **[HP]** (item 2) No new question: H5 point 2 (the OXPd 2 simulator OVA and its guide) stands, because this SDK folder holds neither.
3. **[HP]** (item 3) Is there an OXPd JavaScript library that supports 1.9, or is it now frozen at 2.6? (Low priority: the design does not use it. Could be folded into H7.)
4. **[HP]** (item 4) Do the device-to-server error codes in the Button Manager connectivity guide (45.00.33 and 45.00.23 in particular) mean the same on FutureSmart 5 as on FutureSmart 3 and 4, and what is 45.00.CB?
5. **[Kam]** (item 5) Do we drop the Jedi simulator (it needs a Windows 7 VM with IE 8 and the firewall off) and keep the M577 plus HP's OXPd Simulator 1.3 as the older-printer lab?
6. **[Kam]** (item 6) May the C-76 panel test take the M577's memory reading with HP's `GetMemCounters.exe` from the Windows lab PC (admin password; it asks the printer to release memory first), a step beyond the C-72 first-run list?
7. **[HP]** (item 7) Do any ACT certification requirements apply to an OXPd 1.x authentication solution, and if they do, is Solution Test Bench (we hold 4.17.2.0 of May 2019) still the tool for FutureSmart 5 and 6?
8. **[Kam]** (items 8 and 1) Will you open "Steves Readme Notes.docx" and "Understanding the HP OXPd 1.9SDK.docx" in Word with your Datasec account and save unlabelled copies (or paste the text) where agents can read them? Both are encrypted with Datasec's "Internal Use Only" label.

## What could not be established

- The contents of the two encrypted documents (BLUF 5).
- Whether 1.9's polling Action service removes the need for inbound traffic to the site (N-5): this needs the SDK.
- Whether the M577 is a CE-based or a Linux-based FutureSmart 5 printer. This decides whether `GetMemCounters.exe` works on it.
- Which firmware the Jedi simulator models.
- Why HP's forum said "soon" in March 2026 about a release whose notes are dated February 2026.

## Sources

The line-by-line source table is in `REVIEW.md` beside this file. Scratch, manifests and hash tables: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/b2080/` (`inventory.tsv`, `library_inventory.tsv`, `compare.tsv`, `text/`, `unpack_stb/` (guides only), `unpack_jedisim/` (MSIs, unopened), `quarantine/`).
