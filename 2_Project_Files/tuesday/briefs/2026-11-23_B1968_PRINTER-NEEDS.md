# B1968: what we need from you to reach and drive your printer (OXPd, phase 0)

Datasec / OXPd_2. Agent B1968 (Opus, in-session, read-only) for Tuesday (s315), 2026-11-23. Commission: `2026-11-23_B1968_OXPD-PRINTER-NEEDS-LIST_COMMISSION.md`. Nothing here was sent to anyone. No device was contacted. Scratch, outside git: `2_Project_Files/fleet/state/s315/d1968/`.

---

## 1. BLUF (to read aloud, about one minute)

**Decide this first: use your M577 as it is, for the older-printer tests. Do not wipe it.** HP's own firmware notes for the M577 stop at FutureSmart 5 (the newest is 5.10.0.7, dated 28 August 2026). HP says the newer platform runs only on FutureSmart 6, so your M577 is an older-generation (OXPd 1.x) printer. Older-generation tests don't use developer mode, so the wipe you allowed isn't needed and wouldn't help.

What we need from you, in order:
1. **Its address.** Its IP address, from the panel. It must be on the same wired network as this Mac (192.168.20.x).
2. **Its admin password,** typed by you into the project's credentials file, never into the board.
3. **Two settings in its web page:** confirm "Enable HP home screen if OXPd app fails to load" is on, and confirm TLS 1.2 is enabled.
4. **Your OK for the first-run list** in section 2a. It starts read-only and every step after that can be undone.
5. **Your HP downloads:** the newer-printer simulator image and its guide. Fix two things on your Windows PC: switch Virtual Machine Platform off, and sort out the VMware licence.
6. **A FutureSmart 6 printer** from your colleague's lab or HP's Experience Centre, if you want the newer-printer tests on real hardware. Your M577 can't run them.

**Coordinator's recommendation:** our agents drive the M577 over the network from this Mac (route A). You stay at the panel only for what has to be done there: card taps, the phone sign-in, power cycles.

---

## 2. "I need you to do X" (one step per block)

**Step 1: read three values off the printer panel.**
- IP address:
  `<printer IP>`
- Firmware bundle version (for example 5.9.2.3 or 5.10.0.7):
  `<FutureSmart bundle version>`
- Whether any Workpath apps are installed: yes or no.
Unlocks: the first connection (WP0.1) and the generation question (section 4). Without it, nothing connects and every printer test waits.

**Step 2: make sure the printer and this Mac are on the same network.** This Mac is wired at `192.168.20.220`, gateway `192.168.20.1`. The printer should have an address of the form:
  `192.168.20.x`
Unlocks: two-way traffic. OXPd 1.x forbids address translation, and the printer calls back to the server. If it isn't on that network, we have to find a routed path, which costs time.

**Step 3: put the printer's admin password where only the tool reads it.** Add one line yourself to `!CODING/Datasec/OXPd_2/4_Credentials/.env`:
  `OXPD_TEST_PRINTER_ADMIN_PASSWORD=<the password>`
If the printer has no admin password, set one in its web page first. OXPd admin calls fail with a blank one. The variable name is the coordinator's proposal; the tool reads the value by name and never prints it.
Unlocks: every admin call (S2, S3 older-printer half, S6 older-printer half), and remote panel capture. Without it, route A can only read; you would do every step by hand (route B).

**Step 4: in the printer's web page (`https://<printer IP>`), check two settings and change nothing else.**
- "Enable HP home screen if OXPd app fails to load": **ON**. This can only be set in the web page. With it off, a failed solution can lock the panel.
- Networking > Secure Communication: TLS 1.2 enabled.
Unlocks: a safe first registration. If it's left off, a server outage during a test can lock the panel, and only a partial clean recovers it.

**Step 5: tap OK on the first-run list (2a below).** Unlocks: the first connection. Until then nothing touches the printer.

**Step 6 (Windows PC, for the simulators): three changes on your PC. They are yours to make; we won't make them.**
- Turn **Virtual Machine Platform** off in Windows Features (it is on). The simulator needs Hyper-V's hypervisor off. Turning it off affects WSL 2 and container tools on that PC.
- Get VMware Workstation running without the "evaluation period has ended" banner (Broadcom's free download).
- Download, with your HP developer login, the simulator image `HPExtSim_6.38.0.793.ova` and the "HP Extensibility Simulator Guide" (refused to your account earlier, with an HTTP 403 error).
Unlocks: the newer-printer simulator (WP0.1, E0.1), which is the only way to test the newer platform before a FutureSmart 6 printer arrives. If you don't, every newer-printer test stays blocked.

**Step 7 (optional, only for the newer-printer tests): borrow one FutureSmart 6 printer** from your colleague's lab or the HP Experience Centre. It should not be a pilot unit, because developer mode wipes it. That printer needs your LDB Service Key from the HP developer site, and you at its panel to switch developer mode on.
Unlocks: S1, S3 (newer half), S4 on the real Chromium panel, S6 (newer half), S8. Without it, those wait for the simulator, and S4's on-printer result waits entirely.

### 2a. What we run first (for your OK before any connection)

Each step reads first. Every write can be undone, and none touches firmware, disk or settings outside OXPd.

| # | What the agent runs | Reads or writes | How it is undone |
|---|---|---|---|
| 0 | `GET https://<IP>/DevMgmt/DiscoveryTree.xml` (the printer's list of services) | read, no password | nothing to undo |
| 1 | DeviceInfo over OXPd (port 7627) with the admin password: model, firmware, OXPd version | read | nothing |
| 2 | Turn on the OXPd Test service and take one panel screenshot | write; the service turns itself off at every reboot | reboot, or one disable call |
| 3 | Upload our development CA certificate to the printer's OXPd certificate store | write | delete that certificate |
| 4 | Register one top-level test button pointing at this Mac | write | unregister the button |
| 5 | Register a test sign-in agent (S2a), then remove it | write | unregister, which restores the built-in sign-in |
| 6 | One IPP test print of a one-page PDF from this Mac (S6) | prints a page | nothing |

Stops and guards: five wrong admin passwords lock the account (FutureSmart 4 and later), so the tool stops after one authentication failure. We never set an authorisation configuration on the first day, because it overrides the printer's own access control. We never change firmware, and never run a partial clean or disk initialisation.

---

## 3. Two routes, compared

| | A: our agents drive it from this Mac mini | B: you drive it, we step you through |
|---|---|---|
| Reach | Mac → printer: 443 (web page, discovery), 7627 (OXPd SOAP over TLS), 631 or 443 (IPP). Printer → Mac: one HTTPS port we choose for the agents and buttons; the macOS firewall must allow it. Same subnet, no address translation | Nothing from the Mac to the printer, but the printer still has to call a server for any OXPd test, so step 2 is still needed |
| Credentials | Admin password in the project credentials file (step 3) | You type it in the web page |
| Certificates | We make a development CA, upload it (step 3 of 2a), and pin the printer's own certificate | You upload it in the web page (Networking > certificates) |
| What we build | A small CLI in the OXPd repository (`datasecau/OXPd_2`, through a pull request and review): discovery, DeviceInfo, Test-service panel capture and key press, registration and unregistration, IPP print, a log of every call with secrets redacted. It runs on .NET on the Mac. Results on the Mac don't count for the two shipped packagings (Linux, Windows); those are re-run on those hosts | Nothing new; our steps go to you as a checklist |
| What still needs a person | Card taps, phone sign-in, watching the panel, power cycles | Everything |
| Risk | Account lockout from a bad password (guarded); a stuck panel (guarded by step 4) | Slow; you become the bottleneck for every repeat |

**Recommendation (the coordinator's):** route A, with route B as the fallback if step 3 can't be done. Route A turns each test into something the agents can repeat, and the panel capture lets them check the screen without you.

---

## 4. The model question: what the M577 can and cannot test

- **It is an older-generation printer.** HP's M577 firmware readme: newest revision 2510156_069175, datecode 20260828, "FutureSmart Bundle Version 5.10.0.7". The 21 bundle-version lines in that readme all start with 5, and none with 6. The same readme lists fixes to OXPd calls (GetDefaultCopyOptions), so it carries OXPd 1.x. A web search for an M577 FutureSmart 6 firmware returned none. HP: OXPd 2 runs "on only the newest devices running FutureSmart 6 and later", and the OXPd 2 SDK "only support FutureSmart 6 and newer firmware".
- **Can test:** S2 (our .NET agents called from a real printer, both halves), S3 on the older half (if a reader is plugged in), S6 on the older half (IPP print and priority print), and S4 as the **WebKit** panel (open question N-1: whether the on-panel Microsoft step also applies to the older printers). It also covers the supported-floor intent of C-22 (FutureSmart 4.7 and up). The older-printer simulator runs only on Windows with IIS.
- **Cannot test:** anything on OXPd 2. That means S1 (install in developer mode), S3 newer half, S4 on Chromium 87 (the test planned for today), S6 newer half and S8. The plan names exactly these as blocked without a newer device or the simulator.
- **What unblocks them:** the newer-printer simulator on your Windows PC (step 6, which needs the image, the guide and the Hyper-V fix), or one FutureSmart 6 printer (step 7). S4's real-panel result needs the printer; the simulator only gives an indication.
- **Not established:** your firmware level (step 1 settles it), and whether HP offers a FutureSmart 6 for the M577 through any channel that isn't public. A downgrade on an M577 needs someone at the printer (search summary, REPORTED-UNVERIFIED). A firmware change is not covered by the grant either way.

---

## 5. Documents

**Held** (library backup on the NAS, names listed only, plus the analysis reports):
- OXPd 1.x: SDKs 1.8.2.1, 1.8.4, 1.8.4.1 and 1.7.3.2 Pro; the OXPd 1.x simulator 1.3 and the Jedi Simulator SDK1; 32 docs including the service specifications (authentication, authorization, accessories, certificate management, device info, IPP extensions) and `oxpd-simulator-user-guide.md`; tools (Button Manager 1.1.0, OXPdUI 1.4, OXPm 1.7, Jedi Resource Analysis 1.2.1, OXPdProServices 1.0.20); support-forum threads, two of them naming the M577 by title (Quota service configuration; a 49.DE.05 error).
- OXPd 2: SDK Beta 10 and Beta 9; the portal pages (how-it-works, compatible devices, platform versions, download, publish); the SDK documentation including the EWS guide and the debug-bridge (LDB) guide, as cited by report B1.
- General: FutureSmart firmware notes (4.7.1 solution release notes, interim builds), the PJL and PCL references, the logs and traces guide, and the failed-device recovery steps (bootloader menu).
- Public, fetched today: HP's M577 FutureSmart 5 firmware readme (a local copy in scratch).

**Still needed (each with why):**
1. **HP Extensibility Simulator Guide.** Its troubleshooting answers point to it, and the download was refused (403). Nothing found since says that changed: zero mentions in the clarifications record.
2. **The OXPd 2 simulator image `HPExtSim_6.38.0.793.ova`.** The library folder for it is empty (0 entries).
3. **The M577 user and admin (EWS) guide** for its firmware level, to write route B's click paths accurately. Public on HP; not in the library.
4. **The LDB Service Key** (only for a FutureSmart 6 printer). It's a personal secret you hold; never sent to us.
5. **FutureSmart 6 pilot firmware and how Datasec gets it,** from HP. Needed only for a newer printer.
6. **(Optional) the OXPd 1.x licence terms** for the reverse-engineering clause point (R32). They bear on WP0.4, not on the first connection.

---

## 6. Premise table

| # | Load-bearing sentence | Source | Status |
|---|---|---|---|
| 1 | M577 newest firmware is FutureSmart 5.10.0.7, revision 2510156_069175, datecode 20260828 | ftp.hp.com/pub/softlib/software13/printers/CLJM577/readme_cljM577_fs5.pdf, extracted text lines 11-14 | READ |
| 2 | That readme has 21 "FutureSmart Bundle Version 5" lines and 0 "…Version 6" lines | same, by `grep -o -i -c` (the positive control is the 5 count) | READ |
| 3 | That readme fixes OXPd calls, so the firmware carries OXPd 1.x | same, text lines 154-158 | READ |
| 4 | No public M577 FutureSmart 6 firmware turned up | two web searches, hp.com and open web, 2026-11-23 | READ (an absence in search, not proof) |
| 5 | OXPd 2 only on FutureSmart 6+, and those devices don't support OXPd 1 | B1:489 (`P/how-it-works.md:28`); C2:7, C2:178, C2:186 | READ (report lines) |
| 6 | An M577 appears in partner field cases on FS 5.3.0.1 (OXPd timeouts) and with IPP_PRINTER_BUSY | C2:126, C2:140 | READ |
| 7 | OXPd 1.x installs nothing on the device; registrations by admin SOAP on 7627; disk init wipes them | C1:9, C1:79 | READ |
| 8 | Test service: off by default, enabled by an admin call after each reboot; remote panel capture and key press; must not be on in production | C1:104, C1:326, C1:553 | READ |
| 9 | "Enable HP home screen if OXPd app fails to load" is web-page only; with it off the panel can lock | C2:71, C2:225 item 12 | READ |
| 10 | FutureSmart 4 admin lockout (5 attempts), and a blank admin password fails OXPd | C2:155, C1:430 | READ |
| 11 | Setting an authorization configuration overrides built-in access control | C1:172 | READ |
| 12 | LDB: panel only, service key, internet, admin; toggling wipes all solutions | B1:205-208; B3:347; plan 03:38 | READ |
| 13 | Without an OXPd 2 device or simulator, S1, S3-half, S4, S6-half and S8 are blocked | 03:264 | READ |
| 14 | The simulator needs a Windows x86-64 PC, VMware, nested virtualisation, Hyper-V off, WSL 1, a wired adapter | 03:36; B3:348, B3:351; C1:340 | READ |
| 15 | His PC: Virtual Machine Platform ticked, VMware evaluation ended, IIS off | CL C-53 (CLARIFICATIONS.md:360-362) | READ (Tuesday's reading of his photos) |
| 16 | Simulator Guide was refused (403); 0 mentions since in CLARIFICATIONS (positive control: 2 in 03) | B3:402; 03:37; count by program | READ |
| 17 | The printer may be changed, wiped or configured | CL C-47 (CLARIFICATIONS.md:308-316) | READ |
| 18 | Firmware is "irrelevant as we will need to wipe" (his P2) | CLARIFICATIONS.md:466; 05:245 | READ; this file's point is that the premise behind it (developer mode) does not apply to an FS5 printer |
| 19 | Today's test 1 (S4) needs Chromium/FS6; on an OXPd 1.x printer it tests WebKit | 05:220; 03:57 | READ |
| 20 | A colleague's lab and the HP Experience Centre hold FS6-class devices | CLARIFICATIONS.md:464; 05:228 | REPORTED-UNVERIFIED (his words; which models is not stated) |
| 21 | OXPD2-2 lists the M577 against the FutureSmart 5 item | Jira OXPD2-2 description (GET, 2026-11-23) | READ |
| 22 | This Mac: wired en0 192.168.20.220/24, default gateway 192.168.20.1 | `ipconfig getifaddr en0`, `netstat -rn`, `networksetup -listallhardwareports` | READ (the arp table printed 0 lines; no scan made) |
| 23 | Library: OXPd2/Simulator has 0 entries; the OXPd 1.x simulator 1.3 and SDK 1.8.4.1 are present | `ls` of the NAS library | READ (names only) |
| 24 | An M577 downgrade needs someone at the printer | web search summary of an HP page | REPORTED-UNVERIFIED |
| 25 | OXPd 1.x forbids address translation and fixes port 7627 | C2:7; 03:67 | READ |
| 26 | The old build's register tools switch certificate checks off and are not used (OP-17 default) | 05:182 | READ |

---

## 7. Not covered by the grant (each becomes its own card)

- **Any firmware change on the M577,** including updating it to 5.10.0.7 or any downgrade. It's irreversible on the device.
- **Developer mode (LDB) on any FutureSmart 6 printer.** It wipes installed solutions, which is irreversible: one card, naming the device.
- **Partial clean, disk initialisation or factory reset** of any printer.
- **Anything on HP's portal by an agent** (C-50: your downloads only, done by you); **any message to HP, Microsoft or a person,** including asking the lab or the Experience Centre for a device.
- **Azure or tenant actions:** the test tenant (item 11), and S14 (a printer reaching a server in Azure).
- **Spend,** for example a VMware licence if the free route fails.
- **Changes to your Windows PC** (step 6): yours, not ours.
- Covered and gated: the CLI in the OXPd repository goes in as a pull request with review, and its first run waits for your OK on 2a.

Who decided: the order of steps, the variable name, the first-run list and the route A recommendation are the coordinator's. None of them is a ruling of the product owner's.
