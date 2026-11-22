# B1969 OXPd_2 kick-off lanes: the no-hardware work and the printer-ready tooling, split into file-disjoint waves (sweep, READ-ONLY)

Written 2026-11-23, about 10:20 to 11:00 AEDT, by sweep agent B1969 for Tuesday (s315), on the commission `2026-11-23_B1969_OXPD-KICKOFF-LANE-SWEEP_COMMISSION.md`. It uses the form of B1913 (items 1 to 7) plus items 8 and 9. Read-only: nothing was written to the project, Jira or GitHub. Scratch and the programs behind every count are in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1969/`: `tree.json`, `pulls.tsv`, `prfiles.tsv`, `jira.json`, `jobs.tsv`, the three job logs, `spec/` (four of HP's OXPd 2 bundles, read from origin), `src/` (main files read by GET), `rulings_today.txt` and `partition.py`.

**Who decided.** Every lane, wave, split, default and order below is a proposal for the coordinator to decide. None of it is the product owner's word. His words quoted here are the board message of 2026-11-23 10:10 (quoted in the commission), C-42, C-47, C-56 (message 5) and C-63. Nothing I checked touches B1968's needs list, B1970's records or B1967's NexusAI work.

## State read (by GET, with controls)
- **Main** is `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b` (PR 32, 2026-11-22T20:45:50Z), the SHA Tuesday read.
- **Tree:** 726 entries, 553 blobs, `truncated: false`. The control: the rules job of main's push run printed `RULES: clean (553 files)`.
- **Pull requests:** 32 in all, 0 open, every one merged. There are 33 origin branches: `main` plus one per landed lane. The newest, `b1953/...` and `b1961/...`, are the heads of PRs 32 and 31, so no lane is in flight.
- **Main's push run** is 45068273700, `ci`, attempt 1, success:
  - linux: total 1809, failed 0, succeeded 1805, skipped 4.
  - windows: total 1809, failed 0, succeeded 1788, skipped 21.
  - rules: `UNIT-TEST FLOOR: ran 111, floor 111` and `RULES: clean (553 files)`.
  - These are read from the three job logs.
- **Jira OXPD2:** 25 issues, all `Backlog`, the same count as B1913.
- **Every lane B1913 proposed last night has landed:**

  | B1913 lane | Landed as |
  |---|---|
  | X27 | PR 18 |
  | C | PR 19 |
  | T | PR 20 |
  | E | PR 21 |
  | U | PR 22 |
  | A1 | PR 23 |
  | S | PR 24 |
  | D | PR 25 |
  | A2 | PR 27, with follow-ups PR 29 and PR 32 |
  | Follow-up rounds | PRs 26, 28, 30 and 31 |

  So **none of B1913's lanes is proposed again.** What is left of them is in the owed items below.
- **Owed items.** BACKLOG has 76 items. Open and new since B1913: 54 (part), 55 (2 to 7), 56, 57, 65 (part), 67, 72, 73, 74 (closed by PR 32 but not yet ticked; that is B1970's work), 75 and 76.
- **Machine at 10:19:**
  - `hw.ncpu` is 18.
  - Load is 5.79 / 3.70 / 2.54.
  - There is no `.tools/wave1-heavy.lock.d`.
  - `launch_when_cool.sh` (header, line 4) sets LOAD_MAX to "default 4/3 of the CPU count, min 7; 24 on 18 CPUs".
  - `heavy.py` "waits while load1 is 7 or more" (kit B1961, line 94).
- **The product owner's rulings today** (`kam_rulings_today.sh`, five rows; OQ-6 is found as the positive control):
  - 06:59: OQ-6 "Approve both rows". B1970 records it.
  - 10:10: the kick-off message.
  - 10:11: "thank you".
  - Nothing else names OXPd.

## 1. BLUF
- **The no-hardware backlog is now small.** Most of the value left before the kick-off is in tooling that is ready for the printer. Every product library of the twelve packages has landed. What remains is follow-up rounds (S/XS) and packages outside C-42's twelve.
- **Wave 1: ten lanes can start now, and they share no file** (55 pairs, 0 overlaps by `partition.py`; the planted control overlap is found).
- **The four lanes ranked first for the kick-off are new code:**
  1. **L1, the lab device-reach tool, read-only core** (G1, M). It probes a printer's generation (OXPd 2 service discovery, the OXPd 1.x DiscoveryTree and IPP printer attributes) with a pinned TLS certificate and records every exchange. It answers the M577 question on first contact using GET requests only.
  2. **TA, device sign-in for OXPd 2** (G1, S-M): the admin password grant, the install-code exchange and the solution-token refresh endpoint, built against HP's security model as reports B1 and B2 cite it.
  3. **H, the server end the printer talks to** (G1, M): the five OXPd 2 callback routes, the vault binding and a health route in `Datasec.Suite.Server`.
  4. **IP, the IPP-over-HTTPS transport for the landed Print-Job sender** (G1, S). It is the S6 print path for either generation.
- **Also in wave 1, as follow-up rounds:**
  - Six standard follow-ups: FU (Universal Print cells), FS (secret store), FN (sign-in), FI (identity docs, with the B1960 pointer), FD (data) and FE (session test cells).
  - Wave 1b, when a seat is free: FC (rule R6's false refusals).
- **Wave 2 starts after L1 lands.** L1 creates the Lab project and is the first owner of `Datasec.Suite.slnx`.
  - **L2, the panel driver** (sdkSupport screen capture, press and simulated card tap). It assumes OXPd 2 in developer mode.
  - **L3, the S1/S8 install sequencer.** It is dry-run first and needs a bundle to run.
  - **L4, the lab `print` command.** It uses IP's transport and works on either generation.
  - **O1, the OneDrive module v0** against a fake Graph (WP1.8; outside the twelve).
  - **FK, the contract runtime follow-ups** (owed item 36).
  - **X1, the OXPd 1.x read-only SOAP client.** It is conditional on a coordinator reading of C-56, and high value if the M577 is on FutureSmart 5.
- **Seats:** at most **6 concurrent OXPd seats** (builds and gates counted together). The binding limit is `heavy.py`'s load1 < 7 and the one heavy lock, not the launcher's LOAD_MAX of 24.
- **Nothing in any lane connects to a printer.** Every printer-ready lane is proved against a local stub device. The first connection waits for B1968's needs list and the product owner's answer.

## 2. The lanes

The tier rule: G1 is for security, credential, network or parsing surfaces; G2 is for tests, docs and config.

### Lane L1: lab device-reach tool, read-only core (PRINTER-READY; either generation)
- **Work package:** WP0.2 (spikes S1, S6 and S8 tooling) and WP0.1 ("connectivity script both directions", `03:138`). Jira OXPD2-3 (phase-0 epic). No ticket names the tool.
- **What it builds:** a console project `src/Datasec.Suite.Lab/` (plus `tests/Datasec.Suite.Lab.Tests/`), lab-only and never shipped, with these commands:
  - **`probe <host>`**, read-only and generation-agnostic:
    - (a) `GET https://<host>/cdm/servicesDiscovery` (the OXPd 2 fixed point, `B1_oxpd2-platform-guides.md:49`).
    - (b) `GET http(s)://<host>/DevMgmt/DiscoveryTree.xml` (the OXPd 1.x discovery, "common to all devices", `C1_oxpd1-platform-specs-sdk.md:123`).
    - (c) IPP Get-Printer-Attributes on 631 and on 443. It uses the landed IPP writer and reader (`src/Datasec.Suite.UniversalPrint/Ipp/`, PR 4) over a minimal HTTP POST. Which attributes a device answers is UNMEASURED.
    - It prints which of (a), (b) and (c) answered, so the generation is read, never assumed.
  - **`read <host>`**, for OXPd 2 only: device `identity`, `status` and `capabilities` (generated `DeviceClient`) and Solution Manager `GET /installer` and `GET /solutions` (generated `SolutionManagerClient`; the C-19 pre-install list of spike S1, `03:54`). The bearer token comes through an `IDeviceAccessTokenSource` interface that L1 defines. L1's tests use a fake, and TA supplies the real source in wave 2.
  - **TLS trust:** no accept-all. The first contact prints the device certificate's SHA-256 and stops. Later runs need `--pin <sha256>` and refuse any other certificate. Plain HTTP is allowed only for the DiscoveryTree GET (C1:123 names ports 80 and 443).
  - **The recorder:** every request and answer is written under a run folder with credential fields masked. This reuses `Datasec.Suite.Logging` (PR 2) and applies owed item 36 F7 ("the `BearerAuthorization` family ... the logging deny-list ... must cover them"). It is the raw material for E0.2's written results.
- **Files:**
  - Creates `src/Datasec.Suite.Lab/` and `tests/Datasec.Suite.Lab.Tests/`. Both are new; 0 tree paths exist.
  - Adds two lines to `Datasec.Suite.slnx`. **L1 is the first owner of slnx.**
  - L1 should add the project references wave 2 needs now (Adapters.Oxpd2, UniversalPrint, Jobs, Cards, Logging), so wave-2 lanes add folders only.
  - **Commands are one folder each, `src/Datasec.Suite.Lab/Commands/<Name>/`, registered through one table that L1 owns.** Wave-2 lanes add a folder and one registry line, merged in order.
- **Must NOT touch:**
  - Any existing `src/` or `tests/` file.
  - `Directory.Packages.props`. There is no new package: Kestrel comes from the `Microsoft.AspNetCore.App` framework reference, as `Datasec.Suite.Jobs.csproj` already uses it.
  - `ci.yml`, which is fingerprinted.
  - `src/Datasec.Suite.Server/`.
- **Cells it must add:**
  - A stub device: Kestrel on 127.0.0.1:0 with a throwaway self-signed certificate. It serves canned `servicesDiscovery`, `DiscoveryTree.xml`, IPP and OXPd 2 answers built from the committed specifications.
  - A wrong pin is refused.
  - An unpinned first contact connects to nothing beyond the TLS handshake.
  - Plain HTTP is refused for every OXPd 2 call.
  - A planted credential marker in a stub answer never reaches stdout or the run folder (positive control: the same marker unmasked is found).
  - `Datasec.Suite.Server.csproj` does not reference the Lab project (control: it does reference Core).
  - The probe makes only GET or IPP Get-Printer-Attributes calls. The control is a planted write verb in a test registry, which the cell must find.
- **Depends on:** main only.
- **Review tier:** G1 (network, TLS trust, credential handling). **Size:** M.
- **What it needs from the device later:** an address on a network this Mac reaches, and for `read` the admin password (B1968's list). The rest can be proven before.
- **Generation:** `probe` assumes neither generation. `read` assumes OXPd 2 (FutureSmart 6+, `02:246` "FutureSmart 6 and later only").
- **Authorised by:**
  - The product owner's word of 2026-11-23 10:10: "have you connect and drive the printer yourself (even if it requires you to build something that allows for it)".
  - Tuesday's grant reading: "the printer may be driven by our agents and the tooling for it built in the OXPd repo, but the FIRST connection waits for one needs list to him".
  - Plan WP0.1: "connectivity script both directions" (`03:138`).
- **Prior work:** the generated clients of all 16 services are public (`public sealed class SolutionManagerClient`, `Generated/SolutionManager/SolutionManagerClient.cs:10`; PR 6), and so are the IPP reader and writer (PR 4) and the logging deny-list (PR 2). No lab or device-reach code exists on main.

### Lane TA: OXPd 2 device sign-in (admin grant, install-code exchange, solution-token refresh) (PRINTER-READY; OXPd 2)
- **Work package:** WP1.2 part, "token management" (`03:154`), and WP1.11's "scripted single-device onboarding in the order of `[ARCH §8.2]`" (`03:163`), the token half. Jira OXPD2-14 / OXPD2-9 (no dedicated ticket).
- **Scope, from the sources:**
  - **The admin password grant:** `POST <deviceRoot>/cdm/oauth2/v1/token`, form `grant_type=password`, 1 hour, no refresh (`B2_oxpd2-api-contracts.md:72`; `B1:87`, `:103`).
  - **The install-code exchange:** `grant_type=authorization_code`, `client_id=com.hp.cdm.client.hpE2Solution`, `refresh_token_requested=true`, within 5 minutes (`B2:73`).
  - **The refresh**, implemented as the HTTP `ISolutionTokenEndpoint` that the adapter README says is the host's to bind: "No specification in this repository describes that endpoint" (`src/Datasec.Suite.Adapters.Oxpd2/README.md:95-96`).
  - **The path is uncertain.** B2:358 records the conflict: the guide's table says `/cdm/oauth2/v1/token` and its three examples say `/oauth2/v1/token`. So the path is a setting with the table's value as default. Which path a device answers is UNMEASURED.
- **Files:**
  - Creates `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/` and `tests/Datasec.Suite.Adapters.Oxpd2.Tests/DeviceAuthCellTests.cs`.
  - Changes `src/Datasec.Suite.Adapters.Oxpd2/README.md` (its token-endpoint sentence). TA also takes the adapter's two owed text lines: item 45 limit (10), the doc comment on `Device/IDeviceSecretVault.cs`, and item 65's unlisted `finally` limit. TA therefore also changes `Device/IDeviceSecretVault.cs`, doc comment only.
- **Must NOT touch:** `Generated/`, `contracts/`, the adapter csproj (no reference: the adapter's boundary test forbids any project or package reference, BACKLOG item 45), the adapter's lock file and slnx.
- **Cells it must add:**
  - The password grant sends the form and never logs it (planted-marker control).
  - A non-HTTPS root is refused.
  - A wrong-certificate root is refused (the same pin rule as L1).
  - An exchange later than the 5 minutes is refused typed. This is a client-side guard; the device's own answer is UNMEASURED.
  - The refresh binding returns a fresh copy (the item 45(10) rule).
  - A 1-hour admin token is held in memory only. C-24 rules that the OXPd 2 admin password is discarded after install (`02:251`).
- **Kit must check first** (UNMEASURED by me): whether any adapter cell forbids network code inside the adapter. If one does, TA lives in `src/Datasec.Suite.Lab/` instead, after L1.
- **Review tier:** G1 (credentials, device trust). **Size:** S-M.
- **What it needs from the device later:** the admin password, and whether the device answers the table path or the example path. Everything can be proven before against a stub.
- **Authorised by:**
  - The 10:10 word, as quoted for L1.
  - The adapter README's own words that the endpoint binding "is the host's, not this library's" (`README.md:95`).
  - Item 45: "the host binds it ... later".
  - Who decides where the HTTP binding lives: the coordinator.
- **Prior work:** PR 13 (`Device/DeviceTokenHolder.cs`, `ISolutionTokenEndpoint.cs`, `SolutionTokenGrant.cs`) and PR 28 (follow-ups).

### Lane H: host composition v0, the server end the printer talks to (PRINTER-READY for S1 step 5; NO-HARDWARE demo)
- **Work package:** WP1.11 in part (`03:163`, "Minimal admin API and OXPd 2 onboarding v1"). It is **not in C-42's twelve**: B1913 §5 listed host wiring as "the coordinator's call". The new 10:10 word ("move the project forward as much as you can") is the coordinator's to read as covering it. Jira: none.
- **Scope:**
  - `src/Datasec.Suite.Server/Program.cs` maps the five OXPd 2 callback routes to `Oxpd2CallbackHandler`. Its `HandledOperationIds` are `POST_prePromptResult`, `POST_postPromptResult`, `POST_signoutNotification`, `POST_registration` and `POST_operationCallback` (`Callbacks/Oxpd2CallbackHandler.cs:65`).
  - It binds `IDeviceSecretVault` to `ISecretStore`. This closes the adapter lane's recorded departure: "the host binds it to `ISecretStore` later" (item 45).
  - It adds a `/health` route.
  - It adds a notification route for `ntAuthCode`. S1 step 5 needs it: "wait for `ntAuthCode` on the server's notification target" (`02:802`).
  - The server's TLS certificate comes from configuration.
  - **Not in scope:** migrate-at-start, the admin API, the Universal Print wiring and the sign-in actor wiring. Each is a later lane.
- **Files:**
  - Changes `src/Datasec.Suite.Server/` (`Program.cs`, the csproj adding project references to Adapters.Oxpd2, Secrets and Logging, the Server `packages.lock.json`, and new files under it).
  - Creates `tests/Datasec.Suite.Server.Tests/`.
  - **It adds its one slnx line by merging main after L1 lands** (serial on slnx only, the A1/A2 precedent of B1913).
- **Must NOT touch:** any library's source (it consumes only public members), `Directory.Packages.props` (no `Mvc.Testing`: test with Kestrel on port 0 as `tests/Datasec.Suite.Contracts.Tests/GatewayStub.cs` does) and `ci.yml`.
- **Cells it must add:**
  - The host starts and `/health` answers.
  - A callback with the right credential reaches the sink.
  - A wrong or missing credential is refused with nothing reaching the sink.
  - A body over the adapter's bound is refused.
  - `dotnet publish src/Datasec.Suite.Server` (the `ci.yml` legs, lines 48 and 78) still holds no HP `OXPd2Lib` and no Lab assembly. The release guard's own planted control stays.
- **Route paths and the notification route's shape** are decided by nobody: the kit chooses them for the coordinator.
- **Review tier:** G1 (network surface, credentials). **Size:** M.
- **Generation:** OXPd 2 (OXPd 1.x agents are SOAP; that is X1's work).
- **Authorised by:**
  - The 10:10 word.
  - Plan WP1.11 ("Pulled forward because phases 1 to 4 need onboarded OXPd 2 devices", `03:163`).
  - Item 45's departure line.
  - Who decided to widen beyond the twelve: the coordinator.
- **Prior work:** `Program.cs` "maps no route" (Server PR 1). The adapter is PR 13, the secret store PRs 5, 11 and 24, the logging library PR 2.

### Lane IP: an IPP-over-HTTP(S) transport for the landed Print-Job sender (PRINTER-READY for S6; either generation)
- **Work package:** WP1.7 in part (`03:159`, "IPP sender") and spike S6 (`03:59`: "IPP Print-Job and Print-URI from the server to both devices with the device's certificate checks on ... which port accepts IPP over TLS ... (631 or 443)"). Jira: none (WP1.7 has no ticket; OXPD2-18 is Universal Print).
- **Scope:** `PrintJobSender` "writes it and the document after it through an `IIppTransport`" (`src/Datasec.Suite.Jobs/README.md:16`). No implementation of `IIppTransport` exists on main (3 hits in `PrintJobSender.cs`, all the interface use). IP builds `HttpIppTransport`:
  - an HTTP POST of `application/ipp` to `https://<host>:<port>/ipp/print` (the port and path are settings);
  - the pinned certificate rule shared with L1;
  - streaming bodies;
  - the existing bounds of the README (lines 84 to 106).
- **Files:**
  - Creates `src/Datasec.Suite.Jobs/Transport/` and `tests/Datasec.Suite.Jobs.Tests/HttpIppTransportTests.cs`.
  - Changes `src/Datasec.Suite.Jobs/README.md`.
- **Must NOT touch:** the sender, spool and receiver files, `ReceiverTests.cs`, the UniversalPrint project and the Jobs csproj (no new reference).
- **Cells it must add:**
  - A stub IPP printer (Kestrel, self-signed) receives the exact bytes the sender writes.
  - A wrong pin is refused.
  - A response time-out maps to `ResponseTimedOut`.
  - A refused connection maps to `TransportFailed`.
  - `IPP_PRINTER_BUSY` on a second job is surfaced, not retried silently. Partners saw it on an M577 ("partners saw `IPP_PRINTER_BUSY` on the second job on an M577", `C2_oxpd1-field-experience-js-general.md:140`, REPORTED).
- **Review tier:** G1 (network, TLS). **Size:** S.
- **Authorised by:** C-42 (WP1.7 parts already landed as PR 15, a precedent B1913 §5 names) and the 10:10 word.
- **Prior work:** PR 15 (sender, spool, receiver) and PR 20 (W02 cell).

### Lane FU: Universal Print registration test round (owed items 75, 73 for PR 28, 76 for PR 30's registration README, 54's survivors)
- **Scope:**
  - **Item 75:** "a test cell, and the test seam it needs to hold the entry's lock". The under-lock disposed check (`CloudDeviceTokenHolder.cs:318` at 5b66a7b1) is reached by no test.
  - **Item 73:** "the mutant `mNoDisposedRecheck` survives every cell"; "the comment of cell T14 says the clean-up has run when its wait ends, which that wait does not prove (wait on the object's state)".
  - **Item 76:** the registration README's "snapshot reading" wording, and that the under-lock check's lock "is the new state's while the old call's clean-up runs under the old state's lock".
  - **Item 54:** `mCatchNarrow` and `mFixUndone` "stay named survivors on macOS". Add cells that hold on every leg, or name them for good.
- **Files:** `src/Datasec.Suite.UniversalPrint/Registration/` (an internal seam and README only) and `tests/Datasec.Suite.UniversalPrint.Tests/Registration/`.
- **Must NOT touch:** `Ipp/` (L1 and IP consume it), the UP csproj and lock file, and any public member.
- **Review tier:** G1 (key custody). **Size:** S.
- **Authorised by:** each item's own "a later round the coordinator commissions", and C-42 (WP4.1, `BACKLOG.md` work-package table).
- **Prior work:** PRs 17, 22, 28 and 30.

### Lane FS: secret store follow-ups (owed items 42 (3) and (4), 34 N2)
- **Scope:**
  - **Item 42(3):** "type a runtime fault inside `Decode` (`FileNotFoundException`, `FileLoadException`, `TypeInitializationException`) as `StorageFailed`, never as `UnreadableRecord` ...; optionally warm the decoder when the store opens".
  - **Item 42(4):** the README's `DeleteUnreadable` sentence on a file descriptor.
  - **Item 34 N2:** "`RotateKey` can throw after its new key is written".
- **Files:** `src/Datasec.Suite.Secrets/` and `tests/Datasec.Suite.Secrets.Tests/`.
- **Must NOT touch:** any public member (H binds `ISecretStore`; Sessions, UniversalPrint and Data build against it) and anything DPAPI-NG (N1, UNMEASURED on Windows).
- **Review tier:** G1. **Size:** S.
- **Authorised by:** item 42's "each is a later store kit's work", and C-42 (WP1.1).
- **Prior work:** PRs 5, 11, 24 and 26.

### Lane FN: sign-in state machine follow-ups (owed item 67, the PR 23 part)
- **Scope (item 67, verbatim):**
  - "a subject that differs from the object id by case only has no cell: suggested cell B03 in upper case";
  - "format characters (U+202E, U+200B) are kept in display names";
  - "the second reader's choice I-1 (refuse a grant whose access token is already disposed or empty before the printer is told) and its probe file as a start set of cells".
- **The coordinator's defaults** (mine to propose, the coordinator's to set):
  - I-1: refuse, which fails closed.
  - Format characters: a named limit plus a cell pinning today's behaviour, with no stripping. Stripping could differ from Workpath, whose behaviour is UNMEASURED, and full parity is C-16.
- **Files:** `src/Datasec.Suite.SignIn/` and `tests/Datasec.Suite.SignIn.Tests/`.
- **Must NOT touch:** Sessions and any public member signature.
- **Review tier:** G1 (sign-in and identity binding). **Size:** S.
- **Authorised by:** item 67's "test cells, README ... and named limits, each a round ... of its own", and C-42 (WP1.4).
- **Prior work:** PRs 23 and 28.

### Lane FI: identity card store text round (the B1960 pointer, owed item 76 for PR 29, item 72's README points)
- **Scope:**
  - **The B1960 gate, FOR-RECORDS 1:** "`src/Datasec.Suite.Identity/README.md:35` cites `CsaStore.cs:288` and `:305` ...; they are now `:294` and `:311` ... One-line README fix in a later round or the next Identity lane". This is the Minor the commission folds into "the next Identity lane".
  - **Item 76:** the README states the cost of the repeated-name refusal for parts never read, and that "a caller that cancels while the maker throws gets `CodecFailed`" (named, not changed). Also "a spacing slip in a test line (`FindTests.cs:240`, cosmetic)".
  - **Item 72's README points:**
    - "a failed or cancelled write may still have been applied";
    - "two enrolments at once for one user both read `Enrolled`" (already named: re-check only);
    - "a null value inside a user's attribute set fails that user's read".
- **Files:** `src/Datasec.Suite.Identity/README.md` and `tests/Datasec.Suite.Identity.Tests/FindTests.cs`.
- **Must NOT touch:** any `.cs` file under `src/`.
- **Review tier:** G2 (docs, one cosmetic test line). **Size:** XS.
- **Authorised by:** the B1960 record ("the next Identity lane") and each item's "README lines".
- **Prior work:** PRs 27, 29 and 32.

### Lane FD: state database and device registry follow-ups (owed item 43 (3) and (5); item 76's data part)
- **Scope:**
  - **Item 43(3):** "a capability snapshot holding a lone surrogate escapes as `ArgumentException`". Type it.
  - **Item 43(5):** "the clock result's offset is truncated to whole seconds ...; fix `difference.Ticks / TimeSpan.TicksPerSecond` and one README line".
  - **Item 76:** "every later save on that context refuses ... not only the next" (README), and "no mutant guards the synchronous pre-check (`SuiteDbContext.cs:95`)" (one cell).
- **Held back:**
  - Item 43(4) (the model and firmware text rule, "printable ASCII only ... what HP devices report is UNMEASURED") waits for L1's first probe of a real device.
  - Item 73's latch ("an owed design choice").
- **Files:** `src/Datasec.Suite.Data/`, `src/Datasec.Suite.Devices/` and their two test folders.
- **Must NOT touch:** migrations or either SQL snapshot (a schema change is a STOP).
- **Review tier:** G1 (persistence, audit integrity). **Size:** S.
- **Authorised by:** item 43's "a later data kit's work", and C-42 (WP1.1).
- **Prior work:** PRs 12, 25, 26 and 30.

### Lane FE: session test cells (owed item 67, the PR 18 part), test-only
- **Scope (item 67):** "no cell lets the late answer arrive AFTER the second call's answer has been accepted (... a `LateAnswerAfterTimeOut` variant that releases the second call first); the mutant `mCountFirst` stays a named survivor".
- **Files:** `tests/Datasec.Suite.Sessions.Tests/` only.
- **Must NOT touch:** `src/Datasec.Suite.Sessions/`. Owed item 37, wiring the broker to `ListAll`, is NOT this lane (see §5).
- **Review tier:** G2. **Size:** XS.
- **Authorised by:** item 67. **Prior work:** PRs 9 and 18.

### Lane FC: rule R6's false refusals and H8 (owed item 67, the PR 19 part) (wave 1b)
- **Scope (item 67):** "false refusals the kit did not list (`- echo "hi"`, `args: --flag 'x'`, an anchor or a tag before a quoted value, and a comment line holding an expression before its first colon and blank ...); H8, a block indicator after an expression ... refuse it or name it as a limit for good"; "the root README's line 29 names the tag only".
- **Files:** `build/repo_rules.py`, `build/tests/test_repo_rules.py` and the root `README.md` (B1913 gave the root README to no lane; FC owns it now).
- **Must NOT touch:** `ci.yml` (`REVIEWED_WORKFLOW` fingerprint), `build/tests/test_pipeline_controls.py`, `release_guard.py`, `squash_scan.py` and `denylist/`.
- **Review tier:** G1 (build and pipeline files, owed item 25's standing rule). **Size:** S.
- **Authorised by:** C-67 (the two shapes ticketed; this is that rule's follow-up) and C-42 (WP0.3).
- **Prior work:** PRs 8, 16 and 19.

### Wave 2 lanes (after L1 lands; each is a folder of the Lab project or a separately owned path)

#### Lane L2: panel driver (sdkSupport) (PRINTER-READY; OXPd 2 in developer mode)
- **Scope**, from the committed `com.hp.ext.service.sdkSupport` bundle (read from origin, `spec/sdkSupport.json`):
  - `POST /controlPanel/captureScreen` ("Capture the current screen and return the image", local device administrator);
  - `POST /controlPanel/pressScreen` (coordinates);
  - `POST /controlPanel/pressKey`;
  - `GET/POST/DELETE /simulatedHidDevices` and `POST /simulatedHidDevices/{id}/tap` ("Simulate a card tap", available to solution providers and the local administrator).
  - **This is what lets an agent "drive the printer yourself":** see the panel, press it and tap a simulated card. It gives S1's stale-tap measurement and E1.1's tap-to-panel timing (`03:82`) without a person.
- **Out of scope:** `executeBrowserScript` ("Executes an arbitrary script payload") is left out, or limited to script files committed in the repository. That is the coordinator's call; the default is left out.
- **Files:** `src/Datasec.Suite.Lab/Commands/Panel/` and `tests/Datasec.Suite.Lab.Tests/Panel/`, plus one registry line.
- **What it needs from the device later:** the architecture says sdkSupport exists on "development firmware only" (`02:805`). That means developer mode (LDB), which "wipes all solutions when toggled" (`02:262`) and needs HP's LDB Service Key (`03:38`).
  - The product owner has said "anything about my printer can be changed, wiped or configured" (C-47), with his reading open to correction. His word is not leave for HP's developer key, which "is still needed before developer mode (H5)" (C-47).
  - Whether his M577 can run OXPd 2 at all is not established (C-39). Field reports put the M577 on FutureSmart 5.3 with OXPd 1.x calls (`C2:126`, REPORTED), so L2 may have no target on his printer.
- **Review tier:** G1 (device-control surface). **Size:** M.
- **Authorised by:** the 10:10 word ("connect and drive the printer yourself").

#### Lane L3: S1 and S8 install sequencer, dry-run first (PRINTER-READY; OXPd 2; runs only once a bundle exists)
- **Scope:** `02` §8.2 steps 2 to 7 as one scripted sequence (`02:793-806`):
  - the admin grant (TA);
  - `InstallSolutionInstallerAsync` with the context part in the same request (the operation accepts `multipart/mixed`, `application/vnd.hp.solution-bundle` and the context type, `spec/solutionManager.json`);
  - CA import (`ImportSolutionsSolutionCertificateAuthoritiesAsync`);
  - `ReissueInstallCodeSolutionsSolutionAsync`;
  - waiting for `ntAuthCode` on H's route, then the exchange (TA);
  - for S8, `UninstallSolutionInstallerAsync` plus read-back: "uninstall verified by read-back (context, certificate store and agents gone)" (`03:61`).
- **The default is `--dry-run`:** it prints the planned calls. A real run needs `--execute` and a pinned device.
- **Files:** `src/Datasec.Suite.Lab/Commands/Install/` and its tests folder.
- **What it needs later:**
  - a bundle built with HP's SPU (owed item 1, "the tool is HP's, is not in the repository");
  - developer mode for an unsigned bundle (S1: "install an unsigned bundle in LDB");
  - the admin password.
- **What it proves before:** the order, the 5-minute bound and the read-back logic, against the stub.
- **Review tier:** G1. **Size:** M.
- **Depends on:** L1, TA and H (its routes).

#### Lane L4: lab `print` command (PRINTER-READY for S6; either generation)
- **Scope:** wraps IP's transport and `PrintJobSender`. It runs on 631 and on 443 (S6: "which port accepts IPP over TLS"), and generates a synthetic 600-page PDF (S6: "a 600-page PDF by Print-Job").
- **Out of scope:** the Print-URI half (it needs a server-hosted document; wave 3 with H) and the scan half (it needs a bundle's UI context).
- **Files:** `src/Datasec.Suite.Lab/Commands/Print/` and its tests folder.
- **Review tier:** G2 (it wraps G1 code that IP reviewed). **Size:** XS-S.
- **Depends on:** L1 and IP.

#### Lane O1: OneDrive module v0, the files subset, against a fake Graph (NO-HARDWARE; outside the twelve)
- **Scope:** WP1.8 (`03:160`): "browse, scan to folder, print". The Graph calls are the files subset of report A11 §5 (the 22 live calls). It uses Graph's upload session and paging (PR 10) and the Jobs spool (PR 15).
- **Files:** creates `src/Datasec.Suite.OneDrive/` and `tests/Datasec.Suite.OneDrive.Tests/`. Its slnx line merges after L1 and after H, so the slnx order is L1, then H, then O1.
- **Review tier:** G1 (tokens reach Graph). **Size:** M.
- **Authorised by:** WP1.8 is a phase-1 slice package, not one of the twelve. Who decided to widen: the coordinator, under the 10:10 word.

#### Lane FK: contract runtime follow-ups (owed item 36 F1, F2, F3 and F6; item 67, the PR 20 part)
- **Scope:**
  - **Item 36:**
    - "F1 four public lists hand out their arrays";
    - "F2 an overflow at a caller limit of the largest integer";
    - "F3 string length in Unicode scalar values";
    - "F6 an `IOException` from a body stream passes out of a client method".
  - **Item 67:** "the K8 check covers the first optional root property of each model only, and its count (716 client models) is not pinned".
- **Files:** `contracts/oxpd2/generator/`, the regenerated `src/Datasec.Suite.Adapters.Oxpd2/Generated/` (by the regeneration discipline of item 46(1)) and `tests/Datasec.Suite.Contracts.Tests/`.
- **Why wave 2:** F1 may change a public member the Lab project compiles against.
- **Review tier:** G1 (parsing). **Size:** S-M.
- **Authorised by:** item 36's "follow-ups ... none blocking", and C-42 (WP0.4).

#### Lane X1 (CONDITIONAL): OXPd 1.x read-only SOAP client (PRINTER-READY; OXPd 1.x)
- **Scope:** WP0.4's "WSDL-based stubs from the OXPdLib jar for 1.x" (`03:141`). It holds only the reads the pre-install checks need:
  - DiscoveryTree;
  - device info;
  - `GetAuthenticationAgentRecords`, `GetOwnedAccessoryRecords` and `GetSignInMethods` (`02:821`, step 2a; S2's "Recorded" list, `03:55`).
  - These use HTTP Basic `admin` (`02:251`, OXPd 1.x column).
- **Why it may be high value:** field reports put the M577 on FutureSmart 5 with OXPd 1.x (`C2:126`, REPORTED, not established). If B1968 confirms that, this is the lane that lets an agent talk to his printer at all.
- **Two points must be settled before it starts:**
  - **(a) The WSDLs.** C-56's exception covers "exactly the files" of `contracts/oxpd2/inputs.sha256`. Whether the product owner's message 5 ("hp files have been provided to us. we can store them where we want") also covers HP's OXPd 1.x WSDLs is the coordinator's reading to make, or a card.
  - **(b) The licence clause.** The WP0.4 row records that whether WSDL-based stubs conflict with HP's reverse-engineering clause "is NOT settled ... Default until then: this package is unchanged" (`03:141`).
- **No package:** a hand-written SOAP 1.2 envelope over `HttpClient` and `XmlWriter`. A WCF client package would be a supervised fetch: C-61 covered four packages only.
- **Files (proposed):** `contracts/oxpd1/`, `src/Datasec.Suite.Adapters.Oxpd1/` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`, plus slnx after L1, H and O1.
- **Review tier:** G1. **Size:** M.

## 3. Partition table
`partition.py` (scratch) checked every pair of lanes against main's tree.
- **Wave 1** {L1, TA, H, IP, FU, FS, FI, FN, FD, FE, FC}: **55 pairs, 0 overlaps.**
- **Wave 2** {L2, L3, L4, FK, O1}: **10 pairs, 0 overlaps.**
- **Positive control:** a planted lane on `src/Datasec.Suite.Secrets/SecretStore.cs` was found overlapping FS (1 of 66 pairs).
- **New paths:** every path marked new has 0 tree entries on main. Every changed path exists (for example FU's `Registration/` holds 13 source and 10 test blobs).
- **Wave-2 lanes against wave 1:** L2, L3 and L4 sit inside L1's new folder, so they are serial after L1 by design. FK touches the adapter's `Generated/`, and TA touches `DeviceAuth/`, the README and `IDeviceSecretVault.cs`, so the files are disjoint. FK is still held to wave 2 for the public-API reason above.

| | TA | H | IP | FU | FS | FI | FN | FD | FE | FC |
|---|---|---|---|---|---|---|---|---|---|---|
| L1 | none (build dependency: L1 compiles against Adapters.Oxpd2) | none (slnx: H merges after L1) | none (L4 consumes IP later) | none (L1 consumes `Ipp/` read-only) | none | none | none | none | none | none |
| TA | | none (H binds TA's endpoint in a later commit) | none | none | none | none | none | none | none | none |
| H | | | none | none | none (*) | none | none | none | none | none |
| IP | | | | none | none | none | none | none | none | none |
| FU, FS, FI, FN, FD, FE | | | | | none (*) | none | none | none | none | none |

(*) A build dependency, not a shared file: H, Sessions, UniversalPrint and Data compile against the secret store. FS stays parallel only while it changes no public member. The same rule binds TA against L1 and H (the adapter's public surface).

**Shared project files, one owner each:**
| File | Owner |
|---|---|
| `Datasec.Suite.slnx` | **L1** first. Then H, O1 and X1, each by merging main after the one before it lands. |
| `Directory.Packages.props`, `Directory.Build.props`, `NuGet.config`, `global.json` | **No lane.** A package need is a supervised fetch (C-61) and the lane STOPs. |
| `.github/workflows/ci.yml` | **No lane.** It is whole-file fingerprinted. New projects are covered by `dotnet restore/build/test` at the root (`ci.yml:40-45`, `70-75`) with no edit. |
| Root `README.md` | **FC** |
| `src/Datasec.Suite.Server/*` | **H** |
| `src/Datasec.Suite.Adapters.Oxpd2/README.md` | **TA** |
| `packages.lock.json` | Each lane touches only the lock files of projects it creates or whose references it changes: L1 and Lab tests, H (Server, Server.Tests), O1 and X1. |

## 4. Owed items (59 to 76, plus 1 to 58 re-checked) that are agent-actionable now
| Item | Lane | Files | Size |
|---|---|---|---|
| 45 (10) doc line; 65 `finally` limit | TA | adapter README, `Device/IDeviceSecretVault.cs` | XS |
| 54 survivors `mCatchNarrow`, `mFixUndone` | FU | `UniversalPrint.Tests/Registration/` | XS |
| 75 under-lock check cell and seam | FU | `Registration/CloudDeviceTokenHolder.cs` (internal seam), tests | S |
| 73 (PR 28 part) `mNoDisposedRecheck`, T14 comment | FU | tests | XS |
| 76 (PR 30 registration README) | FU | `Registration/README.md` | XS |
| 42 (3), (4); 34 N2 | FS | `src/Datasec.Suite.Secrets/`, tests | S |
| 67 (PR 23 part) | FN | `src/Datasec.Suite.SignIn/`, tests | S |
| B1960 pointer; 76 (PR 29 part); 72 README points | FI | Identity README, `FindTests.cs` | XS |
| 43 (3), (5); 76 (PR 30 data part) | FD | Data, Devices, tests | S |
| 67 (PR 18 part) | FE | `tests/Datasec.Suite.Sessions.Tests/` | XS |
| 67 (PR 19 part) | FC | `build/repo_rules.py`, its test, root README | S |
| 36 F1, F2, F3, F6; 67 (PR 20 part) | FK (wave 2) | generator, `Generated/`, Contracts tests | S-M |
| 72 (4) the adapter from the store's lookup to the sign-in card identity service | **wave 3** after H (it is host composition: `ICardIdentityService` "Nothing in this library implements it", `src/Datasec.Suite.SignIn/ICardIdentityService.cs:5`) | `src/Datasec.Suite.Server/Composition/` | S-M |
| 74 | **closed by PR 32**; the tick is B1970's | | |

**Records-only, not build lanes** (a records seat; B1970 holds PRs 31 and 32 and OQ-6): 33, 35, 38 to 41, 44, 46 (records half), 49, 50, 56, 57, the records halves of 67, 73 and 76, and the move or comment of OXPD2-20 to OXPD2-25 after PRs 16 and 19.

## 5. EXCLUDED, with the reason
- **Needs the device or the simulator** (built for in L1 to L4, run later): WP0.1 itself, the WP0.2 spike runs, WP1.2's USB and notifications on a device, WP1.6 panel pages (the sign-in page is "frame or full page, per S4 and open question N-2", `03:158`), WP1.9 bundle v0, WP2.x, the E-tests of WP4.2 to WP4.6, and item 43(4) (what HP devices report).
- **Needs HP's tool or a document we do not hold:**
  - WP1.9 and L3's real run need the SPU (item 1).
  - The bundle manifest schema is in HP's SDK, not in `contracts/`.
  - The OXPd 2 token endpoint is in no committed specification (adapter README:96). TA builds it from reports B1 and B2, which cite `G/securityModel.md`; the path conflict stays (B2:358).
  - EWS: no specification we hold. No EWS-driving lane is proposed. §8.3 step 8 names one EWS setting only (`02:827`).
- **Needs a tenant, Azure or a person:**
  - S4: Microsoft's page on the panel needs an app registration and test users.
  - S5, S7, S9, S11's export, S13, S14 and WP3.2.
  - Items 55 (2) to (7) and 57.
  - Item 72 (5) and (6): the Entra flows, each "a supervised fetch, C-61", and an integration run.
- **Needs a ruling or a coordinator decision:**
  - X1's two points (above).
  - WP3.12, beyond an English-only framework. Its default is "English for Phase 1" (C-58 paragraph 26). Copying strings needs Q-B (item 38).
  - Item 37: wiring the broker to `ListAll` and `DeleteUnreadable`. Today's fail-closed start is "the coordinator's decision of 2026-11-21", and "who may call `DeleteUnreadable` in the product is open" (item 42(1)).
  - Item 72(2), the refresh-token chunks ("a security question first: stored as plain text by the Workpath app").
  - Item 72(3), the blob maker holding the card key (the card key is treated as LIVE, `CLAUDE.md` line 47).
  - Item 73's latch.
  - Item 34 N1, N4, N6 and N8.
  - Item 55 (2) and (3) (later rules).
- **Waits on another lane:**
  - L2, L3 and L4 wait on L1.
  - L3 also waits on TA and H.
  - L4 waits on IP.
  - O1 and X1 wait on slnx turns.
  - 72(4) waits on H.
  - FK waits on L1 (API).
  - Item 43(4) waits on L1's first real probe.

## 6. PRIOR WORK on main, per lane (do not rebuild)
| Lane | What exists |
|---|---|
| L1 | 16 generated OXPd 2 clients, public, taking an `HttpClient` (PR 6); IPP reader and writer (PR 4); logging deny-list (PR 2). There is no lab or probe code. |
| TA | `DeviceTokenHolder`, `ISolutionTokenEndpoint`, `SolutionTokenGrant` (PR 13); follow-ups (PR 28). There is no HTTP token client. |
| H | `Program.cs` maps no route (PR 1); the callback handler and credentials (PR 13); the secret store (PRs 5, 11, 24, 26). |
| IP | `PrintJobSender` over `IIppTransport` (PR 15). There is no transport implementation. |
| FU, FS, FN, FI, FD, FE, FC, FK | As each lane's prior-work line says: PRs 17/22/28/30; 5/11/24/26; 23/28; 27/29/32; 12/25/26/30; 9/18; 8/16/19; 6/14/20. |
| L2, L3 | Generated `SdkSupportClient` (15 paths, `controlPanel` and `simulatedHidDevices` among them) and `SolutionManagerClient` (28 paths: install, uninstall, CA import, `reissueInstallCode`). |
| O1 | Graph layer with paging, `Retry-After` and upload results (PR 10); job spool (PR 15). |
| X1 | Nothing. Report C1 names the files that carry the 1.x wire behaviour (`C1:25`, `:364`). |

## 7. Machine notes
- **One heavy dotnet job at a time** across all OXPd seats, through each lane's `heavy.py`:
  - it waits while load1 is 7 or more;
  - it takes `mkdir .tools/wave1-heavy.lock.d`;
  - it sets `DOTNET_ROOT`, `PATH` and the project's own package cache, and closes the network (kit B1961, lines 62 and 93 to 94).
- **The launcher's LOAD_MAX of 24 is not the binding limit; the heavy lock and load1 < 7 are.** A NexusAI seat (N165) shares the CPU but not the lock.
- **Main's suite is now 1809 tests in 14 assemblies** (B1913 measured 1578 at PR 17). A full run takes minutes, not seconds. Each seat runs its own project's tests first and the full solution once.
- **The C7 Contracts cell** was the one hosted-Windows flake (B1955, 1 of 63). It was fixed by PR 31. One run since then reads green, which is one run and not a rate.
- **Recommendation:** at most **6 concurrent OXPd seats**, builds and gates counted together. Wave 1 is best started as **L1, TA, H, IP, FU and FS**, with FI, FN, FD, FE and FC filling seats as they free. More would mostly queue on the lock and on the hosted runner's four jobs per push. Whether hosted minutes are billed (item 18) is UNMEASURED.

## 8. WAVES
- **Wave 1, start now; no shared file and no heavy job together beyond the lock:**
  - Kick-off value: L1, TA, H and IP.
  - Hygiene: FU, FS, FN, FI, FD and FE.
  - Wave 1b, when a seat is free: FC.
  - H adds its slnx line only after L1 lands. Its build starts now.
- **Wave 2, after L1 lands** (and the named lanes):
  - L2 (after L1), L3 (after L1, TA and H), L4 (after L1 and IP).
  - FK (after L1).
  - O1 (slnx after H).
  - X1, only if its two points are settled (slnx after O1).
- **Wave 3, after H:** 72(4), the identity-to-sign-in adapter in `Server/Composition/`. Then the sign-in actor wiring (WP1.11's next part), and L4's Print-URI half.
- **Max useful concurrent seats on this machine:** 6, as §7 explains. The 18 CPUs and LOAD_MAX 24 would allow more launches, but the heavy lock serialises the work.

## 9. Drafter-ready scopes (one paragraph each, to paste into a kit commission)

**L1.** Goal: a lab-only console `src/Datasec.Suite.Lab/` with `probe` and `read`, plus `tests/Datasec.Suite.Lab.Tests/` and the two slnx lines (L1 is the first slnx owner). `probe <host>` makes GET calls only: `/cdm/servicesDiscovery` (B1:49), `/DevMgmt/DiscoveryTree.xml` (C1:123), and IPP Get-Printer-Attributes on 631 and 443 through the landed `Ipp/` writer and reader. It reports which answered. `read <host>` (OXPd 2) calls the generated `DeviceClient` (`identity`, `status`, `capabilities`) and `SolutionManagerClient` (`GET /installer`, `GET /solutions`), with the token through an `IDeviceAccessTokenSource` that L1 defines (fake in tests). TLS: the certificate SHA-256 is printed on first contact and the run stops; `--pin` is required afterwards; there is never accept-all. A recorder writes every exchange to a run folder, masked by `Datasec.Suite.Logging`. Commands live in `Commands/<Name>/` with one registry. The project references Adapters.Oxpd2, UniversalPrint, Jobs, Cards and Logging. There is no package, no `ci.yml` edit and no Server reference. Cells:
- a stub device (Kestrel on 127.0.0.1:0, self-signed) with canned answers from the committed specifications;
- a wrong pin is refused;
- an unpinned contact stops after the handshake;
- plain HTTP is refused for OXPd 2;
- a planted credential marker is absent from the output (with an unmasked control);
- Server does not reference Lab (with a Core control);
- the probe makes no write verb (with a planted control).

Gate G1. Authority: the product owner, 2026-11-23 10:10, "have you connect and drive the printer yourself (even if it requires you to build something that allows for it)"; the first connection to a real device waits for the needs list (B1968) and his answer.

**TA.** Goal: an HTTP client for the OXPd 2 device token resource in `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/`, built against `B2_oxpd2-api-contracts.md:72-73` and `B1:87`:
- the admin password grant (`grant_type=password`, 1 h, memory only);
- the install-code exchange (`grant_type=authorization_code`, `client_id=com.hp.cdm.client.hpE2Solution`, `refresh_token_requested=true`, a client-side 5-minute guard);
- an `ISolutionTokenEndpoint` implementation for the refresh.

The token path is a setting: the default is `/cdm/oauth2/v1/token`, and the conflict at B2:358 is named. TA also writes the adapter README's endpoint sentence, item 45(10)'s doc comment on `IDeviceSecretVault.TryGet` and item 65's `finally` limit line. There is no csproj, `Generated/` or lock-file change. The kit first checks for an adapter cell that forbids network code; if one exists, TA moves into the Lab project after L1. Cells: the form is never logged (with a marker control); a non-HTTPS root is refused; a wrong pin is refused; a late exchange is refused typed; a fresh copy is returned from the vault read; the admin token is never persisted. Gate G1. Authority: the 10:10 word; the adapter README:95, "is the host's, not this library's"; the coordinator decides where the binding lives.

**H.** Goal: `src/Datasec.Suite.Server/` hosts:
- the five OXPd 2 callback routes bound to `Oxpd2CallbackHandler` (its `HandledOperationIds`, `Oxpd2CallbackHandler.cs:65`);
- the `IDeviceSecretVault`-to-`ISecretStore` binding (item 45's departure);
- `/health`;
- an `ntAuthCode` notification route (`02:802`);
- a configured TLS certificate.

There is no migrate-at-start, admin API, Universal Print or sign-in wiring. It adds `tests/Datasec.Suite.Server.Tests/` (Kestrel on port 0, no `Mvc.Testing`), and its slnx line goes in after L1 lands. Cells: the host starts and health answers; the right credential reaches the sink; a wrong or missing credential is refused with nothing reaching the sink; an oversize body is refused; the published Server holds no `OXPd2Lib` and no Lab assembly (the guard's planted control stays). Gate G1. Authority: WP1.11, "Pulled forward because phases 1 to 4 need onboarded OXPd 2 devices" (`03:163`); the 10:10 word "move the project forward as much as you can"; outside C-42's twelve, so who decided is the coordinator.

**IP.** Goal: `HttpIppTransport : IIppTransport` in `src/Datasec.Suite.Jobs/Transport/`: an `application/ipp` POST, the port and path as settings, the shared pin rule, streaming, and the README's existing bounds kept. One README section. Cells: a stub IPP printer receives the sender's exact bytes; a wrong pin is refused; a time-out maps to `ResponseTimedOut`; a refused connection maps to `TransportFailed`; `IPP_PRINTER_BUSY` on a second job is surfaced, not retried (C2:140, REPORTED on an M577). There is no change to the sender, spool or receiver, or to the csproj. Gate G1. Authority: S6, "IPP Print-Job and Print-URI from the server to both devices with the device's certificate checks on" (`03:59`); C-42 (WP1.7 parts landed as PR 15).

**FU.** Goal: Universal Print registration test round.
- Item 75: an internal seam to hold the entry's lock, and the cell that reaches the under-lock disposed check.
- Item 73 (PR 28): a cell that reddens `mNoDisposedRecheck`, and T14 waiting on the object's state.
- Item 76: the README's two wording points.
- Item 54: cells that hold `mCatchNarrow` and `mFixUndone` on macOS, or a named limit.

Files: `Registration/` (internal seam and README only) and its tests; no public member, no `Ipp/`, no csproj. Gate G1. Authority: item 75, "a test cell, and the test seam it needs ... of a later round the coordinator commissions".

**FS.** Goal: type runtime faults inside `Decode` as `StorageFailed` and optionally warm the decoder (item 42(3)); the README `DeleteUnreadable` descriptor sentence (42(4)); `RotateKey` must not throw after its new key is written, or a named limit with a cell (34 N2). Files: `src/Datasec.Suite.Secrets/` and its tests; no public member change and no DPAPI-NG. Cells: one per fault type, red first, plus the N2 cell. Gate G1. Authority: item 42, "each is a later store kit's work".

**FN.** Goal: cell B03 (a case-only subject difference); I-1, refusing a grant whose access token is disposed or empty before the printer is told (coordinator's default: refuse); format characters U+202E and U+200B as a named README limit plus a cell pinning today's behaviour (coordinator's default; no stripping, because Workpath parity is UNMEASURED and C-16 applies). Files: `src/Datasec.Suite.SignIn/` and its tests. Gate G1. Authority: item 67, "test cells, README ... and named limits, each a round ... of its own".

**FI.** Goal:
- correct `README.md:35`'s pointers to the two blob-maker catches (B1960 FOR-RECORDS 1);
- add item 76's two README sentences (the cost of the repeated-name refusal in unread parts; a caller who cancels while the maker throws gets `CodecFailed`);
- add item 72's README points;
- fix `FindTests.cs:240`'s spacing.

No product `.cs` file changes. Gate G2. Authority: B1960, "One-line README fix in a later round or the next Identity lane".

**FD.** Goal: type the lone-surrogate snapshot (43(3)); fix the whole-seconds truncation with `Ticks / TicksPerSecond`, plus the README line (43(5)); add item 76's "every later save" README clause and one cell guarding the synchronous pre-check at `SuiteDbContext.cs:95`. No migration and no snapshot change (a STOP if needed). 43(4) waits on L1's first probe. Gate G1. Authority: item 43, "a later data kit's work".

**FE.** Goal: a `LateAnswerAfterTimeOut` variant that releases the second call first, and a cell that reddens `mCountFirst` (or a named survivor). Only files under `tests/Datasec.Suite.Sessions.Tests/` change. Gate G2. Authority: item 67.

**FC.** Goal: remove the false refusals item 67 lists (`- echo "hi"`, `args: --flag 'x'`, an anchor or tag before a quoted value, a comment with an expression before its first colon); decide H8 (refuse, or name it for good: the kit's choice for the coordinator); make root `README.md:29` name the digest. No `ci.yml`, `test_pipeline_controls.py`, `release_guard.py`, `squash_scan.py` or `denylist/` change. Gate G1. Authority: C-67, "the two missed shapes are written down as named limits with a follow-up ticket".

**L2** (wave 2). Goal: `Commands/Panel/` with `screen` (captureScreen to a PNG in the run folder), `press x y`, `key <name>`, and `card add|tap|remove` over `simulatedHidDevices`. `executeBrowserScript` is left out (the coordinator's default). Write verbs need `--execute` and a pinned device. Cells against the stub: the order and shape of each call, refusal without `--execute`, the image saved and never echoed. Gate G1. Authority: the 10:10 word. Real use needs developer mode (`02:805`; C-47 for his printer; HP's developer key per C-47 and H5).

**L3** (wave 2). Goal: `Commands/Install/`, §8.2 steps 2 to 7 and S8's uninstall plus read-back, `--dry-run` by default. Cells: the step order against the stub; the 5-minute exchange bound; the read-back diff. Gate G1. Authority: S1 and S8 (`03:54`, `03:61`); the 10:10 word. A real run waits for a bundle (item 1) and developer mode.

**L4** (wave 2). Goal: `Commands/Print/`, which sends a PDF by IP's transport to 631 or 443 and generates a 600-page synthetic PDF. Cells against IP's stub. Gate G2. Authority: S6 (`03:59`).

**O1** (wave 2). Goal: `src/Datasec.Suite.OneDrive/`: browse, scan to folder (upload session) and print (download to the spool), against a fake Graph, over the files subset of A11 §5. Gate G1. Authority: WP1.8 (`03:160`); outside the twelve, so the coordinator decides.

**FK** (wave 2). Goal: item 36 F1, F2, F3 and F6 in the generator, then regenerate by the item-46(1) discipline (never a hand edit under `Generated/`); pin the 716-model count and cover every optional root property in K8. Gate G1. Authority: item 36.

**X1** (conditional). Goal: a hand-written SOAP 1.2 read client for DiscoveryTree, device info, `GetAuthenticationAgentRecords`, `GetOwnedAccessoryRecords` and `GetSignInMethods`, with no package. It starts only after the coordinator's reading (or a card) on keeping HP's 1.x WSDLs in the repository, and on the WP0.4 licence default. Gate G1. Authority: WP0.4, "WSDL-based stubs from the OXPdLib jar for 1.x" (`03:141`); C-56 message 5, "we can store them where we want", is the product owner's word that the coordinator's reading would rest on.
