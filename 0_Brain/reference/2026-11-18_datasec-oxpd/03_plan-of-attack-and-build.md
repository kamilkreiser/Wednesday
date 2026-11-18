# Datasec OXPd: plan of attack and build

Datasec / OXPd, 2026-11-18. Author: lead architect agent (Opus), for Kam. Status: DRAFT for the Fable review pass (C-5). Companion to `02_architecture.md` (cited as `[ARCH §n]`). Report citations as `[A1 §4.7]`; library citations as `library:relative/path:line`. No secret value appears here.

---

## 1. BLUF

1. **Build order**: environment and seven risk spikes first; then one thin vertical slice (card sign-in + OneDrive scan and print) end to end on OXPd 2, then the same slice on OXPd 1.x; then the remaining sign-in methods and apps (SharePoint, Teams, Mailflow); then Universal Print (Direct, Pull, Secure); then deployment tooling, admin console, licence and reporting integration; then hardening, HP certification, pilot and release.
2. **OXPd 1.x is likely to reach customers first**: it needs no HP signing [C1 §4.19], while no OXPd 2 bundle from any partner installs on customer firmware yet [B3 §1 item 1]. The plan builds both in parallel behind one core so OXPd 2 ships the day HP's signing works.
3. **What Kam must provide in phase 0**: an x86-64 PC for the OXPd 2 simulator and SPU, one physical OXPd 2 printer (FutureSmart 6, firmware ≥ 6.38.0.793) and one FutureSmart 4.7/5 printer for OXPd 1.x, the certified card readers, a test Entra tenant with Workpath HPAM installed on at least one Workpath printer, the customer-side Azure gateway in that tenant, HP App Center/VNV access and an HP partner contact, and answers to the top questions (Q1 to Q6).
4. **Sizes are relative** (S, M, L, XL) with their drivers; no dates are given because HP's signing timeline, device availability and the answers to Q1-Q6 dominate the schedule.
5. **25 questions** for Kam, ordered by design impact, in §8; Q1 (HP's position and signing route) and Q2 (how the Microsoft sign-in step happens off the panel) move the design most.

---

## 2. Prior-work check (short)

Full table in `[ARCH §2]`. In one line each: the Workpath suite stays untouched and is the behavioural specification; its back-end-side contracts (CSA attribute set, gateway, Log Analytics streams, licence protocol) are reused byte for byte; the licence service is extended additively; the HPK Deployment Utility's job/retry model is reused for onboarding; the earlier Java OXPd 1.x attempt is knowledge only, not code [A7 §5.2]; HP's demos are call-sequence patterns only [B3 §5.3].

---

## 3. Phases, goals and exit criteria

Every exit criterion is a check a tester can run and record (pass/fail, with evidence attached: logs with secrets redacted, screenshots of the panel, Graph results).

### Phase 0: environment, access and spikes

**Goal**: everything needed to build and test exists, and the seven assumptions that could overturn the architecture are tested on real hardware.

What Kam provides (blocking items in bold):
- **x86-64 Windows 11 or Linux PC, wired network**, for the OXPd 2 simulator OVA `HPExtSim_6.38.0.793.ova` (to download into `library:OXPd2/Simulator/`, `library:START-HERE.md:6`) and the SPU (Windows/Linux only [B1 §6 row 8]); the Mac cannot host them [B3 §7 Q3].
- **One physical OXPd 2 printer** on FutureSmart 6 with firmware ≥ 6.38.0.793 that can be put in LDB developer mode (and is not a pilot unit: LDB toggling wipes solutions [B1 §5.2 item 8]).
- **One physical FutureSmart 4.7 or 5.x printer** without Workpath apps for OXPd 1.x (FS 5.8+ preferred [C2 §7 Q1]).
- One Workpath printer with the current Datasec suite, in the same test tenant (mixed-fleet tests).
- The certified readers: Elatec TWN4, RF IDeas, HP X3D03A/35H11B, HID OMNIKEY [A1 §4.11] [C2 §7 Q4].
- **Test Entra tenant** with Custom Security Attributes licensed, the HPAM registration as customers have it, Universal Print licences, the "Onboarding Azure Services" deployment (SignalR, Function App, Log Analytics), and a Printer Administrator test account with MFA.
- **HP App Center / VNV account status and an HP partner contact** (Q1).
- The current production CSA card-blob key and licence installation credentials through a secure channel (not the library copies, C-3).

Spikes (each a throwaway proof with a written result; none of the code is kept unless it passes review):

| Spike | Question it answers | Pass condition |
|---|---|---|
| S1 OXPd 2 install | Can we install an unsigned bundle in LDB on the device and the simulator, exchange the install code, call `login`, and does the solution token survive a device reboot? [B1 §5.3] | Bundle installs; refresh token works after reboot, or the re-issue path is proven |
| S2 OXPd 1.x agents in .NET | Can a FutureSmart device call a CoreWCF SOAP 1.2 agent hosted on .NET 10 on Linux, with TLS and CN match? [C1 §5.1 item 1] | `GetPrePromptResult` and `HidReportEvent` reach the agent over HTTPS from a physical device; else adopt the Java sidecar |
| S3 Reader parity | Do raw reports from each reader on OXPd 2 and OXPd 1.x decode to the same string the Workpath app stores? [A7 §5.3 item 1] | Golden strings equal for every reader × card type × platform |
| S4 On-panel Microsoft page (OXPd 2) | Does Microsoft's sign-in, number match and redirect work in Chromium 87; are cookies isolated between users? [B1 §5.3] | Two users in sequence never share a Microsoft session; page renders; else M4 is dropped |
| S5 Token cross-redemption | Can the server (confidential credential, same client id) redeem a refresh token issued to the Workpath public-client flow? Does device code work with the confidential settings? [ARCH §7.1] | Redemption succeeds, or a documented fallback |
| S6 Print paths | IPP Print-Job and Print-URI from the server to both devices with the device's certificate checks on; priority print on OXPd 1.x; Universal Print IPPS 631 push | A PDF prints on both; failures documented per model |
| S7 Off-panel sign-in | Device code and phone-redirect (server FQDN and Function App relay) in a tenant with Conditional Access policies | Both complete; CA outcomes recorded |
| S8 OXPd 2 life cycle | Same-id bundle upgrade; uninstall leaves nothing | Upgrade path known; uninstall verified by read-back |

**Exit criteria (phase 0)**:
- E0.1 Simulator OVA running and reachable from the dev server; physical OXPd 2 and OXPd 1.x devices reachable both ways with the dev CA installed.
- E0.2 S1-S8 each have a written result in `1_Project_Definition/` of the new project; any failed spike has an architecture change note.
- E0.3 Q1-Q6 answered or explicitly deferred by Kam.
- E0.4 CI builds an empty .NET 10 solution, a test bundle with the SPU, runs secret scanning (no allow-listed paths), CodeQL (Datasec org policy for `datasecau` repositories) and fails on the SDK development CA in a production bundle.

### Phase 1: thin vertical slice on OXPd 2

**Goal**: a user taps a known card at an OXPd 2 printer, is signed in (No-MFA and MFA via device code), opens OneDrive, scans a page into a folder, prints a PDF from OneDrive, signs out; a card enrolled on the Workpath printer works.

Why OneDrive for the slice: it exercises every hard mechanism once (session handle → token broker, scan receiver, Graph upload session, Graph download, conversion, IPP print, capability-limited options) with the simplest UI; Mailflow adds compose complexity and Teams adds channel semantics on the same file APIs (inferred ordering).

**Exit criteria**:
- E1.1 Known card, No-MFA: panel shows the user signed in within the N6 budget at p95 over 50 taps, panel awake.
- E1.2 Known card, MFA: device-code QR shown, phone sign-in completes, sign-in refused if a different user signs in on the phone (binding rule).
- E1.3 Card enrolled on the Workpath printer signs in on OXPd 2 and the reverse (same CSA entry, no duplicate `cardId`).
- E1.4 Second tap signs out; another card switches user; the previous user's tokens are gone from the server (inspected).
- E1.5 Scan two pages to a OneDrive folder; file appears with the right name and page count; spool empty afterwards.
- E1.6 Print a DOCX and a PDF from OneDrive with duplex and copies; only device-supported options offered.
- E1.7 Device inactivity timeout signs out; server session expires even if the notification is blocked (test by dropping it).
- E1.8 No token, card string or file name in any log (automated scan of logs, with a positive control that plants a marker and proves the scan finds it).

### Phase 2: the same slice on OXPd 1.x

**Goal**: E1.1 to E1.8 pass on the FutureSmart 4.7/5 device through the OXPd 1.x adapter with no change in the core.

**Exit criteria**: E2.1 = E1.1-E1.8 on OXPd 1.x; E2.2 wake-from-sleep card tap succeeds in ≥ 95 of 100 attempts (records timings) [C2 §5.3 R2]; E2.3 disk-initialise the device, the drift check restores registrations within 15 minutes and the next tap works; E2.4 the core's diff between phase 1 and phase 2 is limited to the adapter and templates (code review check); E2.5 each panel page set stays under 2 MB and no script runs longer than 2 s on the device (measured).

### Phase 3: complete sign-in hub and the Microsoft 365 apps

**Goal**: functional parity for the sign-in hub (F1-F21) and the apps (F30-F43) on both platforms.

Order and reason:
1. **Sign-in completeness** first, because every app depends on it: QR/phone app via the existing SignalR gateway (F10), enrolment (F9), passkey (F12), phone-redirect mechanism M2 (Q2), launch-after-sign-in (F16), pull-print dialog stub (F17), national clouds (F19), error codes (F21).
2. **SharePoint** (shares the OneDrive module; adds sites, libraries and metadata).
3. **Teams** (same Files APIs; adds channel navigation and the channel-message recipe).
4. **Mailflow** (largest: compose with people search, drafts, attachments via upload sessions, reply threads, HTML rendering and sanitising, print of messages).

**Exit criteria**: E3.1 every row F1-F43 in `[ARCH §3]` has a passing test on both platforms or a recorded, Kam-approved deviation; E3.2 per-user settings set on a Workpath printer appear on an OXPd printer (quick message, pin); E3.3 Graph throttling test (simulated 429 with `Retry-After`) completes without user-visible failure; E3.4 Mailflow send failure after draft creation leaves no draft.

### Phase 4: Universal Print

**Goal**: F50-F57 on both platforms. Order Direct → Pull → Secure, as Workpath's own code structure suggests [A3 §5.2 item 7].

**Exit criteria**: E4.1 register 3 flavours for 10 devices in one admin sign-in, no password stored (inspect C15 and DB); E4.2 Direct job prints within the documented latency with nobody at the panel, PIN job lands in device storage; E4.3 Pull: sign-in shows count, release prints, auto-release honours `UPAR`, exact identity match (a user `a@x` never receives `aa@x` jobs); E4.4 Secure list, preview, option override, release; E4.5 a Workpath `_Pull` printer and an OXPd `_Pull` printer release the same user's pooled job (with Q18's cloud configuration); E4.6 restart the server mid-job: final job state still reported; E4.7 device removal deregisters its cloud printers.

### Phase 5: deployment tooling, admin, licence and reporting

**Goal**: a technician who is not a developer installs the server, onboards 50 devices of both platforms, and sees them in the fleet view with Workpath devices.

**Exit criteria**: E5.1 appliance and Windows installers pass a clean-machine install script; E5.2 onboarding of 50 mixed devices with retry/result report; E5.3 uninstall leaves nothing (read-back proof per device); E5.4 licence: batch validate, grace survives restart, expired licence blocks new sign-ins, seat released on removal; old Workpath devices unaffected (regression run against the existing `/api/validate`); E5.5 Log Analytics rows from OXPd devices have the same columns as Workpath rows and an existing customer KQL query returns both; E5.6 fleet view lists Workpath + OXPd 1 + OXPd 2 devices of one tenant with platform and last seen.

### Phase 6: hardening, certification, pilot, release

**Goal**: secure, sized, certified, piloted.

**Exit criteria**: E6.1 every weakness W1-W27 `[ARCH §6.7]` has a test that would fail if the weakness came back, and each test was seen failing first against a deliberately broken build (red control); E6.2 external penetration test of the server and panel pages with no high findings open; E6.3 load test: 500 devices, 20 sign-ins per minute, 50 concurrent sessions within N5/N6; E6.4 HA switch-over under 2 minutes with active sessions recovered or cleanly ended; E6.5 OXPd 2 self-certification on one device per test group A-G [B1 §1 item 3] and HP VAV/VNV submission accepted; E6.6 pilot at one customer site with both platforms and Workpath for four weeks with defect rate under the agreed threshold; E6.7 release notes, install guide, admin guide, panel user guide, support runbook.

---

## 4. Work packages

Size scale: S (days of one engineer), M (one to two weeks), L (three to six weeks), XL (more than six weeks). Each lists its size drivers. "Independent check" = a review by someone (human or agent) who did not build it.

### Phase 0

| WP | Component | What is built | Tests | Independent check | Definition of done | Size and drivers |
|---|---|---|---|---|---|---|
| WP0.1 | Lab | Simulator host, device network, dev CA, test tenant wiring | connectivity script both directions | Kam's team runs the script | E0.1 | M: hardware lead times, HP portal access |
| WP0.2 | Spikes S1-S8 | throwaway code + result notes | per spike pass condition | second engineer repeats each spike from the note | E0.2 | L: device access, firmware quirks |
| WP0.3 | CI/CD skeleton | repos under Datasec's GitHub org, .NET 10 solution layout, SPU in CI, secret scan, CodeQL | pipeline red/green on planted secret and planted dev CA | reviewer | E0.4 | S |
| WP0.4 | Contract test harness | OpenAPI-generated stubs for 16 OXPd 2 services; WSDL-based stubs from the OXPdLib jar for 1.x [C1 §6 row 3] | contract tests run against simulator responses | reviewer | harness runs in CI | M: beta spec drift [B2 §6 item 7] |
| WP0.5 | HP engagement | App Center/VNV enrolment, written position on M365 integration (Q1) | n/a | Kam | answer recorded | S effort, unknown elapsed |
| WP0.6 | OneDrive/SharePoint source read | the missing half of report A3 [ARCH coverage note] | n/a | second reader | Graph call list and journeys documented | S-M |

### Phase 1 (OXPd 2 slice)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP1.1 | C1 device registry, C17 DB, C15 secret store (local provider) | entities, migrations, encryption | unit; encryption round trip; key rotation | security review | used by slice | M |
| WP1.2 | C2 OXPd 2 adapter (sign-in, USB, notifications) | token management, targets, callback credential check | contract tests; simulator; device | reviewer + contract tests | E1.1, E1.4 | L: beta behaviour, callback formats not in spec [B2 §6 item 4] |
| WP1.3 | C8 decoders | six decoders + generic, sequence reassembly | golden files from S3 for every reader | Workpath engineer compares | E1.3 | S |
| WP1.4 | C5 state machine (card paths) + C7 identity (CSA, refresh, device code) | per-device actor; CSA lookup and enrol; binding rule | unit with fake Graph; integration with test tenant | reviewer | E1.1-E1.3 | L: state machine edge cases |
| WP1.5 | C6 token broker | sessions, handles, refresh, events, expiry | unit; restart test | security review | E1.4, E1.7 | M |
| WP1.6 | C9 panel front end (p2 template) | prompt page, OneDrive pages | browser tests on simulator; screenshots on device | UX review on device | E1.2, E1.5 | M |
| WP1.7 | C11 job service (scan receiver, spool, IPP Print-Job, conversion) | streaming receiver, thumbnails, IPP sender | unit; device tests | reviewer | E1.5, E1.6 | L: IPP library choice, formats per model |
| WP1.8 | C10 OneDrive module (files subset) | browse, scan to folder, print | Graph integration tests | reviewer | E1.5, E1.6 | M |
| WP1.9 | C19 bundle v0 | manifest via SPU, context keys | install on LDB device | reviewer | installs, generic manifest | S |
| WP1.10 | Logging deny-list | structured logging, scanners | planted-marker red control | security review | E1.8 | S |

### Phase 2 (OXPd 1.x slice)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP2.1 | C3 OXPd 1.x adapter | SOAP client wrapper (no password in `ToString`), CoreWCF agents (or Java sidecar), accessory handling, Reserve/Release with retries | WSDL contract tests; simulator; device soak | reviewer | E2.1, E2.2 | L: CoreWCF on device, field defects [C2 §5.3 R2] |
| WP2.2 | C4 onboarding engine v1 (1.x) | probe, CA import, merge trusted sites, register records, manifest, drift repair | device tests incl. disk init | reviewer | E2.3 | M |
| WP2.3 | C9 p1 template | ES5 pages with Omni kit, budget checks | on-device timing | UX review | E2.5 | M: WebKit limits |
| WP2.4 | IPP on 1.x | Print-Job, priority mode from app page | device tests | reviewer | E1.6 on 1.x | S |

### Phase 3 (sign-in completeness and apps)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP3.1 | QR/phone gateway client | one SignalR subscriber per tenant, routing, QR rendering (same format, current key from C15) | with the shipped phone app | Workpath team | F10 | M: gateway contract not in library (Q4) |
| WP3.2 | Phone-redirect sign-in (M2) | authorize URL, relay endpoint (if Q4 allows), redemption | test tenant with CA | security review | F7 via M2 | M |
| WP3.3 | Enrolment, passkey, launch-after-sign-in, national clouds, error codes | | per F row | reviewer | F9, F12, F16, F19, F21 | M |
| WP3.4 | SharePoint | sites, libraries, metadata | Graph tests | reviewer | F39 | M |
| WP3.5 | Teams | channels, files, message recipe, quick access | Graph tests | reviewer | F40 | M |
| WP3.6 | Mailflow | list, search, compose, people, drafts, attachments, reply, print, sanitiser | Graph tests; sanitiser fuzz | security review of sanitiser | F35 | L: largest call list (23 calls) [A2 §6.2] |
| WP3.7 | Per-user settings roaming | CSA properties, approot JSON | mixed-fleet test | reviewer | E3.2 | S |
| WP3.8 | Shared Graph layer hardening | paging, `Retry-After`, upload sessions | 429/503 simulation | reviewer | E3.3 | S |

### Phase 4 (Universal Print)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP4.1 | C12 registration and device tokens | CSR, certificates, key provider, batch admin sign-in | test tenant | security review | E4.1 | M |
| WP4.2 | Direct | polling, Range resume, IPPS push, PIN forwarding, status | device tests | reviewer | E4.2 | M |
| WP4.3 | Pull | sign-in hook, dialog, release, `UPAR` | device tests | reviewer | E4.3, E4.5 | M |
| WP4.4 | Secure | list, preview, override, release | device tests | UX review | E4.4 | M |
| WP4.5 | Persistence and clean-up | job map, deregistration | restart test | reviewer | E4.6, E4.7 | S |

### Phase 5 (deployment, admin, licence, reporting)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP5.1 | Packaging | container images, appliance, Windows installer, upgrade/rollback | clean-machine installs | ops review | E5.1 | M |
| WP5.2 | C4 onboarding v2 (OXPd 2 fleet, both platforms at scale) | batch jobs, reports, OXPm export | 50-device run (simulated + real) | reviewer | E5.2, E5.3 | M |
| WP5.3 | C16 admin console | config, devices, UP registrations, presets, support bundle, roles | UI tests; role tests | security review | console complete | L |
| WP5.4 | C13 licence client + C18 portal extensions | batch endpoint, auth, columns, claims, fleet view | regression against existing validate | licence-service owner | E5.4, E5.6 | M: changes a production service (never-touch-prod discipline; deploy via its own pipeline) |
| WP5.5 | C14 reporting | statistics, supplies, ingestion | KQL parity | reviewer | E5.5 | S |
| WP5.6 | `.cfg` importer | import existing HPAM/app configs | sample files | reviewer | F60 | S |

### Phase 6 (hardening, certification, pilot)

| WP | Component | What is built | Tests | Independent check | DoD | Size and drivers |
|---|---|---|---|---|---|---|
| WP6.1 | Security tests W1-W27 | one red-first test per weakness | as named | external reviewer | E6.1 | M |
| WP6.2 | Pen test | external | | external firm | E6.2 | M (elapsed) |
| WP6.3 | Load, soak and HA | test rigs, simulated devices | as named | reviewer | E6.3, E6.4 | M |
| WP6.4 | HP certification | test evidence for groups A-G, VAV/VNV submission | HP's checklist [B1 §1 item 3] | HP | E6.5 | L-XL: device access, HP turnaround |
| WP6.5 | Pilot | site install, monitoring, defect triage | live | Kam + customer | E6.6 | L (elapsed) |
| WP6.6 | Documentation | guides and runbooks | doc review | support team | E6.7 | M |

---

## 5. Test strategy

| Layer | What | Where | Notes |
|---|---|---|---|
| Unit | state machine transitions (every `AuthPhase` path, stale-session guard), decoders, CSA blob compute, token broker, IPP encoding, licence client | CI | Golden files for decoders and CSA blobs are generated from the Workpath code paths, not hand-written |
| Contract | OXPd 2: requests/responses validated against the 16 OpenAPI files (Beta 10), plus recorded device traffic for the parts the specs omit (post-prompt schema, callback deadlines [B2 §6 items 4, 10]); OXPd 1.x: SOAP envelopes validated against the 100 WSDL/XSD inside `OXPdLib-1.8.4.jar` [C1 §6 row 3] | CI | Re-run on every new OXPd 2 beta; a contract diff fails the build |
| Simulator | OXPd 2 OVA 6.38.0.793; OXPd 1.x Simulator 1.3 (Chromium panel, so UI results do not count for 1.x) [C1 §5.4] | lab | `sdkSupport` simulated HID taps for automated sign-in tests on development firmware only [B2 §5] |
| Real devices | per firmware family: FS6 (OXPd 2), FS5.8+ and FS4.7-5.x (OXPd 1.x); each reader model; panel classes (8-inch, 4.3-inch) | lab | Nightly smoke on real devices; soak runs for card sign-in (1,000 taps, wake-from-sleep included) |
| Mixed fleet | one tenant with a Workpath printer, an OXPd 1.x printer and an OXPd 2 printer: shared enrolment, settings, Pull release across products, reporting rows, licence counts | lab | Required before each release |
| Security | W1-W27 tests; TLS configuration scan; secret scan of logs, DB dumps and support bundles; fuzzing of HID input, scan uploads and mail HTML; authz tests for callback credentials and session handles | CI + lab | Pen test before pilot |
| Performance | N5/N6 targets with simulated devices (adapter-level device simulator built for this) | lab | Graph throttling simulation |
| Red-control discipline | Every automated check (test, scanner, monitor) must first be shown failing against a deliberately broken input or build before its green result is trusted; every "not found" result carries a positive control showing the search can find the thing (inferred to be the discipline Datasec projects use, matching the analysis brief's rule `01_analysis-brief.md` "How to work") | all | A check that has never been seen red is reported as unverified |

---

## 6. Dependencies: what blocks what

```
Kam inputs (hardware, tenant, HP access, Q1-Q6)
   └─> Phase 0 (lab, spikes S1-S8, CI)
         ├─> Phase 1 (OXPd 2 slice) ──┐
         └─> Phase 2 (OXPd 1.x slice) ┴─> Phase 3 (sign-in completeness, SharePoint, Teams, Mailflow)
                                              └─> Phase 4 (Universal Print: Direct → Pull → Secure)
                                                    └─> Phase 5 (packaging, onboarding v2, console, licence, reporting)
                                                          └─> Phase 6 (hardening, HP certification, pilot, release)
HP signing (WP0.5) ───────────────────────────────────────────────────> OXPd 2 customer release only
Licence-service owner (WP5.4) ───────────────────────────────────────> fleet view and batch validation
Customer Azure gateway decision (Q4) ──> WP3.1/WP3.2
```

Specific blockers:
- No OXPd 2 device in LDB or simulator host → phases 1 and S1/S4/S8 blocked; phase 2 can start alone.
- S2 failure (CoreWCF) → Java sidecar for the 1.x adapter (adds a runtime to packaging).
- S5 failure → No-MFA users re-authenticate once on OXPd; Q6 re-opened.
- Q1 negative → OXPd 2 track paused; OXPd 1.x continues.
- Q3 "no interop" → CSA key may be per-tenant from the start (simpler security, no mixed-fleet enrolment).
- Q2 answer decides WP3.2 scope and whether S4's result matters.
- Universal Print Pull across products needs Q18 (cloud-side pooling) before E4.5.
- Phase 6 certification needs devices for test groups A-G (Q25).

Parallel tracks once phase 0 exits: OXPd 2 adapter, OXPd 1.x adapter, core (state machine, broker, identity), job service, app modules (after the broker API is frozen), Universal Print connector (from phase 3, independent of panel UI for Direct).

---

## 7. Team and agent model

| Work | Agents can do it | Needs a human with a device | Needs Kam / HP |
|---|---|---|---|
| Reading specs, generating contract stubs, unit tests, decoders from golden files, Graph modules against a test tenant, DB, secret store, admin console, licence extensions, docs | Yes (with review by a second agent or human; agents never get production credentials) | No | No |
| Spikes S1-S8 | Agents write the code and the test script | Yes: someone at the printer taps cards, signs in on a phone, watches the panel, power-cycles | S7 needs Kam's tenant admin for CA policies |
| Panel UX on real devices (OXPd 1.x WebKit, OXPd 2 Chromium 87) | Agents produce pages and automated simulator checks | Yes: screenshots and timing on devices | No |
| Card reader soak tests, wake-from-sleep | Agents analyse logs | Yes | No |
| Phone app and QR flows | Agents build the server side | Yes: phone with HP Secure Authentication | Q4 (gateway source owner) |
| Universal Print registration and pooling | Agents build | Yes: printer output, portal sharing | Q18 (customer portal config) |
| HP App Center, VAV/VNV, partner questions | Agents draft the submissions and questions | No | Yes: Kam or HP partner manager |
| Licence-service changes (production service) | Agents write and test against a non-production copy | No | Kam approves any production deployment (never-update-prod) |
| Pen test, pilot, customer comms | No | Yes | Kam |

Suggested core team (inferred): one lead engineer who owns the core and reviews agent output; one engineer with lab access who runs device work; agents in parallel lanes per §6; a part-time security reviewer from phase 3.

---

## 8. Question list

How each question was checked against the library before keeping it: the twelve reports' section 7 were merged; for each question I looked for an answer in the reports' findings and, where a report named a likely source, in the library itself (START-HERE, the help portal set per A6, the forum indexes per B3/C2, the source trees per A1-A5). Questions the library answers were dropped (examples at the end). "Kam" = Kam can answer alone; "Team" = needs his team; "HP" = needs HP.

Ordered by how much the answer changes the design.

| Id | Question (one sentence Kam can answer) | Why it matters (decision moved) | Options | Assumed if unanswered | Raised by | Who answers | Library check |
|---|---|---|---|---|---|---|---|
| **Q1** | Has HP confirmed (or can we ask HP to confirm in writing) that an OXPd solution whose server calls Microsoft 365 is acceptable and signable, and does Datasec have HP App Center / VNV access and a partner contact? | Whether the OXPd 2 track can ship at all, and when (R1, R2; D1, D29) | yes / no / not yet asked | Not yet asked; OXPd 1.x first, OXPd 2 gated on HP | [B3 §7 Q1, Q2], [B1 §7 Q1, Q4, Q11], [B2 §7 Q4], [C2 §7 Q7, Q8] | Kam + HP | Forum: 2023 "no public cloud" statement and 17 Nov 2026 signing delay are the latest HP words (`library:OXPd2/Support-Forum/2023-06-15-17607595895827-...md:98-100`, `...2026-11-06-57213300079635-...md:370-378`); nothing newer |
| **Q2** | On OXPd printers, may the interactive Microsoft step happen on the user's phone (device code, or a phone redirect) instead of on the panel, and does a QR sign-in with the HP Secure Authentication app count as the MFA step? | Whole sign-in design (D10, F7, F10) | M1 device code; M2 phone redirect; M4 on-panel (OXPd 2 only); QR app = MFA yes/no | Phone-based M1 + M2; on-panel only after spike S4; QR app still followed by M1/M2 in MFA mode | [A1 §7 Q5], [A7 §7 Q1], [B1 §7 Q5], [B2 §7 Q3], [C2 §7 Q3] | Kam (+ Team for customer expectations) | Library documents only the Workpath WebView flow (`[A6 §4.1]`) and the old build's device code; no ruling |
| **Q3** | Must a card, BLE badge or phone enrolled on a Workpath printer work on an OXPd printer in the same tenant, and the reverse (same CSA format and key, shared No-MFA token, shared user settings)? | CSA contract and key custody (D5), registration choice (D4) | full interop / enrolment only / separate | Full interop | [A1 §7 Q2], [A6 §7 Q1], [A7 §7 Q2], [A2 §8 Q3], [A4 §7 Q6] | Kam | Not stated in docs or code; brief implies mixed fleets (C-1) |
| **Q4** | Is the customer-side Azure back end (SignalR, Function App) and the HP Secure Authentication phone app frozen, and where is the source of the Function App gateway? | QR integration (D11), phone-redirect relay (M2b), whether customers redeploy Azure | frozen / may add one endpoint / may change | Frozen; relay endpoint only if Kam allows | [A6 §7 Q2], [A1 §7 Q4, Q8], [A5 §1 item 5] | Kam + Team | Gateway source absent from all five back-end repos [A5 §1 item 5] and from HPAM [A1 §4.10] |
| **Q5** | Where will the server run for the first customers: on each customer site's LAN, one per Entra tenant or per site, or hosted by Datasec or a partner? | D1, D21, HA, licence (server seats) | per site LAN / per tenant / Datasec-hosted with relay | Customer-hosted, one per site, single tenant | [A6 §7 Q3], [B1 §7 Q2], [B3 §7 Q6], [C2 §7 Q2], [A5 §7 Q2] | Kam | Kam's brief says "localised server" (C-1); no deployment model in the library |
| **Q6** | Should the server reuse each customer's existing "HP Authentication Manager" Entra registration (adding a web redirect and a server credential), or use a new registration? | D4; No-MFA and settings roaming; customer onboarding steps | reuse (Option A) / new (Option B) | Option A | [A1 §7 Q1], [A2 §8 Q5], [A3 §7 UP Q2] | Kam | Code shows single registration per tenant [A1 §4.6]; no ruling for a server |
| **Q7** | May the server store each device's administrator password permanently (required on OXPd 1.x, optional on OXPd 2 for unattended recovery)? | Secret custody (C15), OXPd 1.x feasibility | store encrypted / enter per operation | Store encrypted on the customer's server for OXPd 1.x; OXPd 2 discards after install | [C1 §7 Q2], [B1 §7 Q8], [B2 §7 Q8] | Kam + customers | Required by spec for 1.x run-time calls [C1 §4.2] |
| **Q8** | Which card reader models (USB vendor/product ids) must the first release support, and are any not HID keyboard-type? | OXPd 2 signed manifest content (re-signing per new model), decoders | the six in HPAM's HPK; plus others | The six in `hpk.xml`; OMNIKEY 5427 and the unknown 1DA6:0110 only if they work on Workpath today | [B1 §7 Q6], [B2 §7 Q3], [B3 §7 Q5], [C2 §7 Q4], [A7 §7 Q8] | Kam + Team | HPK lists six pairs [A1 §4.11]; docs list three BLE readers; two have no Workpath decoder |
| **Q9** | Which printer generations and panels are in the target fleets (FutureSmart 6, FutureSmart 4.7-5, older FS3/Oz, Pro, panel sizes 4.3 inch and below)? | Device scope (D32), templates, test matrix | FS4.7+ and FS6 only / include FS3 / include Pro | FS 4.7+ for OXPd 1.x (FS 5.8+ preferred), FS6 for OXPd 2; Pro and Oz out; ≥ 4.3-inch touch | [C1 §7 Q1], [C2 §7 Q1], [A6 §7 Q7], [B1 §7 Q3] | Team | Compatibility guide lists 140 models but not customers' fleets [C1 §4.20] |
| **Q10** | How large are the biggest customer sites (printers, users, sign-ins at peak)? | Sizing (N5), HA need, Universal Print polling design | — | 500 printers, 5,000 users, 20 sign-ins/min per server | new (architecture) | Team | Not in library |
| **Q11** | How should OXPd devices be licensed: one seat per printer whatever the platform under the same tenant licence; is the server itself licensed; how long may a server run without reaching the licence service, and what happens at expiry? | Licence changes (D25, C18), grace logic | same seat / separate platform caps / server seats | One seat per printer any platform; server unlicensed but identified; 20-day grace; stop at confirmed expiry | [A5 §7 Q1, Q2, Q3, Q9], [A1 §7 Q7], [A6 §7 Q10] | Kam | Licence code is platform-agnostic [A5 §1 item 1]; expiry behaviour inconsistent in code [A5 §5.4] |
| **Q12** | Do target customers run other vendors' sign-in, pull-print or accounting solutions on the same printers, and is "one stack per device (Workpath or OXPd)" acceptable? | Reader ownership collisions, singleton roles (D20, D31) | coexist / exclusive | Coexistence needed (no authorization/quota proxy, non-critical stats); one stack per device | [B1 §7 Q7], [C1 §7 Q4], [C2 §7 Q6] | Team | Not in library |
| **Q13** | Are any customers who will buy OXPd still on the legacy Keycloak back end? | Doubles sign-in code (D30) | yes / no | No: Entra CSA only | [A1 §7 Q3], [A5 §7 Q5], [A6 §7 Q5] | Kam | Both back ends in code [A1 §4.1]; customer list not in library |
| **Q14** | How should customers receive the server: Linux container or virtual appliance, Windows service, or both; and may it use the customer's Azure Key Vault for keys? | Packaging (D23), secret store (D28), DB choice | container / appliance / Windows / Key Vault yes-no | Container + appliance primary, Windows secondary; local encrypted store default, Key Vault optional | new (architecture) + [C2 §7 Q2] | Kam + Team | Not in library |
| **Q15** | Which apps and features are in the first OXPd release (all five + hub? OneDrive personal? Teams chats? Mailflow drafts and search? any sixth app)? | Scope and phase 3 size | full parity / core journeys first | All five + hub; OneDrive for Business only; channels only; parity for scan-to and print-from first | [A6 §7 Q4], [A2 §8 Q6, Q7], [A4 §7 Q1] | Kam | Docs name five apps + HPAM (`[A6 §3.1]`); no sixth app found |
| **Q16** | For scanning and printing: is panel scan preview required, may mail attachments be converted on the server instead of through the user's OneDrive, and may "Send to e-mail" use Graph instead of the device's SMTP? | D18, F32, F38 | as assumed / keep today's behaviour | Thumbnail preview with remove/rescan; server-side conversion for mail; Graph send | [A2 §8 Q1, Q2, Q4] | Kam | Code shows preview forced on and OneDrive round trip [A2 §6.1] |
| **Q17** | For Universal Print on OXPd, keep the three printers per device with the same naming, register with an interactive admin sign-in in the server console, and hold "Secure" jobs in the cloud/server rather than on the device? | D15, D16, F50-F54 | as assumed / collapse Secure into Pull | As assumed | [A3 §7 UP Q1, Q4], [C1 §7 Q6], [B2 §7 Q1] | Kam | Code shows today's model [A3 §1]; no ruling for server |
| **Q18** | How do customers share `_Pull` printers in the Universal Print portal (one pool via Print Anywhere?), and is IPPS (TCP 631) from a server to printers allowed on their networks? | Mixed-fleet Pull release, Direct/Pull delivery | — | Print Anywhere pool; 631 open on the print VLAN | [A3 §7 UP Q3, Q5] | Team / customers | Cloud-side rule not in code [A3 §5.2 item 3] |
| **Q19** | How are Workpath fleets deployed and configured today (HP Command Center, the HPK utility, Web Jetadmin; HP signing of HPKs; attestation in production), and do customers have populated `.cfg` configurations to import? | Onboarding tool shape (D26), importer | — | Both HPCC and the utility; importer wanted; WJA optional | [A4 §7 Q2, Q5, Q7], [A5 §7 Q6], [C1 §7 Q7] | Team | Utility code shows the mechanism, not production practice [A5 §6 row 4] |
| **Q20** | What rights does Datasec hold over HP's Workpath sources in the library and over redistributing HP's OXPd 2 libraries (beta) and IPP sample code inside a product? | Reuse vs reimplementation (R16) | — | Reimplement logic; redistribute OXPdLib 1.x unchanged; OXPd2Lib only after production SDK | [A4 §7 Q3], [B3 §7 Q4] | Kam + HP | SDK has no redistribution terms [B3 §4.10]; 1.x SDK permits unchanged library [C1 §5.3] |
| **Q21** | Must job audit be complete (a "critical" statistics agent that can lock printers if the server misses records), and are supplies reports needed for OXPd 1.x printers? | D20, D22 | critical / best effort; supplies yes/no | Best effort, non-critical; no supplies on 1.x in release 1 | [B2 §7 Q2], [C2 §7 Q5], [A2 §8 Q8], [A3 §7 UP Q8] | Kam | — |
| **Q22** | Who issues the server's TLS certificate at customers (internal CA or public) and what DNS name will it have? | Onboarding CA push, installer | internal CA / public CA | Customer internal CA, FQDN in customer DNS | [C1 §7 Q3], [B1 §7 Q9] | Team / customers | — |
| **Q23** | Should the single admin view for mixed fleets live in the extended licence portal, in each server's console, or in the Administration Portal? | D24, WP5.4 | licence portal / server / admin portal | Licence portal (fleet) + server consoles (site) | [A5 §7 Q4] | Kam | Administration Portal does not manage devices [A5 §1 item 4] |
| **Q24** | Is No-MFA mode carried over as it is (users' refresh tokens stored unencrypted in the directory), or should OXPd launch with encrypted storage that also needs a Workpath update? | W2, D5 | as is / encrypt with dual-read / drop No-MFA on OXPd | As is, default off, documented risk; encryption in a later joint release | [A6 §7 Q9], [A1 §6 item 2] | Kam | Docs claim encryption; code stores plain text [A1 §6 item 2] |
| **Q25** | Which test devices can the team get for development and HP self-certification (one per test group A-G), and is there an HP contact for interim firmware? | Phase 0 and 6 schedule (R4, R10) | — | One OXPd 2 MFP + simulator; one FS5 MFP; certification blocked until more are borrowed | [B1 §7 Q3], [B3 §7 Q3], [C2 §7 Q8], [A7 §7 Q3] | Kam (+ HP) | Library has no hardware inventory |

### 8.1 Assumed, minor (folded; no answer needed unless Kam disagrees)

- **Language**: C#/.NET 10 with CoreWCF for OXPd 1.x agents; Java sidecar only if spike S2 fails [A7 §7 Q6] [C1 §7 Q5]. (D3)
- **Kiosk mode** (suite replaces the home screen): not offered; unsupported in Beta 10 [B1 §7 Q10].
- **User policy / per-user device permissions**: not used; Alpha [B1 §7 Q12] [B2 §7 Q6].
- **PIN entry on the panel**: on-page HTML keypad if ever needed [B3 §7 Q8].
- **Stored driver jobs in `copy/storedJobs`**: not relied on [B2 §7 Q5].
- **Workpath target variants on FS6 devices**: not used for the server design [B2 §7 Q7].
- **OXPd 1.9**: build on 1.8.4.1 [C1 §7 Q8].
- **Web Jetadmin**: optional OXPm export only [C1 §7 Q7].
- **EULA**: no per-user panel EULA (both Workpath apps have it switched off); acceptance at install [A2 §8 Q9].
- **Gotenberg conversion service**: treated as retired; its credential location reported [A2 §8 Q4].
- **Per-app legacy Entra registrations (MailFlow, Teams client ids)**: not used [A2 §8 Q5].
- **Universal Print certificate renewal**: treat "gone/unauthorised" as re-register and alert [A3 §7 UP Q7]; **cost of three printers per device**: no effect assumed [A3 §7 UP Q6].
- **HP Advance / LRS VPSX integrations**: out of release 1 [A6 §7 Q8].
- **Rental licence type**: billing only [A5 §7 Q10]; **library copy current**: yes, CI files stale [A5 §7 Q8].
- **Old OXPd 1.x build history / author**: this is the last state [A7 §7 Q7]; **its two hardcoded keys**: treated as sensitive, covered by C-3 [A7 §7 Q4].
- **Server-side custody of user tokens**: accepted with encryption and on-premises hosting [A7 §7 Q5].
- **"Encrypted" vs plain refresh token in docs**: code wins (plain) [A1 §6 item 2].
- **Missing documents** (GCC Universal Print guide, KQL pack, "Set 2 of 2"): schemas taken from code [A6 §7 Q11].

### 8.2 Questions dropped because the library answers them

- "Does OXPd 2 run on the same devices as OXPd 1?" No: FutureSmart 6 devices do not support OXPd 1 (`library:OXPd2/Docs/how-it-works.md:28`) [B3 §7 Q7 answered].
- "Does Universal Print use the Graph print API?" No, IPP INFRA (`library:HPAM - Docs and Notes/Source Code/UniversalPrint-main/app/src/main/java/com/hp/print/mup/agentas/remoteconfig/PrintCloudConfig.kt`) [A3 §1].
- "How do the other apps get Graph permissions?" Tenant-wide consent on the HPAM registration with the documented delegated scope list (`library:START-HERE.md`, key facts) [A1 §7 Q6 answered by A2 §7 item 1].
- "Where are per-user settings stored?" The user's OneDrive app folder (`.../storage/OneDriveUserPropertiesStore.kt:136`) [A2 §8 Q3 mechanism].
- "Which language does HP's OXPd 2 SDK favour?" C# first (`library:OXPd2/SDK/README_Beta_10.txt:112-197`).
- "Do OXPd 1.x solutions need HP approval?" No for 1.8 (forum reply, March 2026) [C1 §4.19].
