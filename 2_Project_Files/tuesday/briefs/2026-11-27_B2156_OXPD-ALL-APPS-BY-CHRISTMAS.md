DONE

# B2156 (lane P2): OXPd, what it would take to have ALL apps by Christmas

Read-only analyst for Tuesday (s333). Clock at start `date`: Fri 27 Nov 2026 17:17:46 AEDT; at writing: Fri 27 Nov 2026 17:21:58 AEDT. Kam's question (terminal, 2026-11-27, verbatim): "what would it take to have all apps by chistmas?" Kam's input relayed by Tuesday mid-lane (verbatim): "I know the infrastructure cannot be done in parallel easily but the apps could". The answer below is built in that shape: (1) serial shared infrastructure, (2) per-app lanes that run in parallel.

The rules followed are those of the B2154 commission: read-only. No dotnet job was run, no device was touched, and nothing was read in Source_Documents, 4_Credentials or the key folders. GitHub was read only by `gh api -X GET` under the OXPd gh config. No cd was used and nothing was deleted. Marks: **MEASURED** (I ran the instrument named), **RELAYED** (taken from a record and not re-checked), **ESTIMATE** (my sizing), **UNMEASURED**. `<P>` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2`. `03:n` / `02:n` = line n of the design docs today. "B2154" = `tuesday/briefs/2026-11-27_B2154_OXPD-WORKING-COPY-PLAN.md`.

"The apps" means the five Workpath apps plus the sign-in hub: Mailflow, Teams, OneDrive, SharePoint and Universal Print, plus the hub (HP Authentication Manager). C-16 (card `datasec-oxpd-q15-release-one-scope-1118`, his tap "b — Full match of everything", `<P>/1_Project_Definition/CLARIFICATIONS.md:98`) is the scope ruling.

## BLUF

1. **Full match of every app by Wednesday 23 Dec: NO, under any staffing.** On the M577 alone, ESTIMATE about 75 lock-days of build. Even spread over five parallel lanes, it cannot fit in 18 working days: the device is single, and parity checks need a Workpath printer and Steve M's answers. **Realistic full match on the M577 (OXPd 1.x, one packaging): late January 2027, ESTIMATE about Fri 29 Jan.** The plan's real release 1 (E6.8: both platforms, both packagings, pilot) comes later still and is not dated here.
2. **All apps at core journeys by Christmas: NO on the one wave lock** (about 30 lock-days against 18). **It is POSSIBLE, but not likely, with 4-5 builders in parallel**, and only if all seven conditions in section E hold. The main ones: the heavy-job runner fix (owed 138) and the Server.Tests bound (owed 137) land by Tue 1 Dec. Kam's tenant pieces (user, licences, app registration, CSA set, a Teams team, a SharePoint site, Universal Print) arrive by Mon 7 Dec. Mailflow core leaves out printing mail bodies, and Universal Print core is Direct only. **Most likely Christmas outcome with parallel builders:** the hub (card sign-in) plus OneDrive, SharePoint and Teams at core, and Universal Print Direct. Mailflow core lands in the first week of January.
3. **The one wave lock is a convention, not a machine limit (MEASURED).** It is an `mkdir` of `<P>/.tools/wave1-heavy.lock.d` inside the runner `heavy.py`, behind a load gate of load1 under 7. The machine is an Apple M5 Max with 18 cores and 128 GB, and load1 was 2.14 at 17:18. Lane B2138's 19 heavy jobs held the lock for **12.5 minutes in total** (11:20:44-11:33:16). Its whole-solution test took **58 s** (`duration: 58s 054ms`). Each lane builds in its own `clone/` with its own bin/obj. The tests I read bind port 0. A "lock-day" is a builder seat's day of kit, build, gate and fix. It is not machine time. The real serial resources are four:
   - the one M577 (device runs);
   - Tuesday's gate and merge throughput;
   - usage limits;
   - the few shared files.
4. **Infrastructure stays serial, and the apps fan out.** The infrastructure critical chain is about 11.5 lock-days (agent host, then host composition, then panel shell, then onboarding, then card path, then end-to-end). With 2-3 builders it lands **about Wed 16 Dec**, against B2154's Wed 23 Dec on one lock. **App lanes can start Mon 30 Nov.** Their Graph-side libraries need only what main already has (Graph layer, Sessions, OneDrive, UniversalPrint material) and fakes. Panel pages and device runs join from Thu 10 Dec, when the host and the panel shell are in.
5. **Kam's inputs decide the date more than code does** (section D). The latest dates are: the tenant user, app registration and CSA set by Mon 7 Dec (Wed 2 Dec for B2154's sign-in test); licences, a Teams team, a SharePoint site and the Universal Print pieces by Mon 7 Dec; the reader by Mon 7 Dec; five home-screen buttons (K7 widened) by Thu 10 Dec; the printer switched on for one device window a day from Tue 1 Dec. OXPd 1.x needs **nothing from HP** (02 §4 signing row, RELAYED via B2154).

## A. Per app: built on main, missing, size, external dependencies

Main: `760e1a644ce9a419cf1b9132d0776e9e5eac1cac` (PR 58), merged 2026-11-27T01:04:29Z, 0 open PRs (MEASURED, `gh api -X GET`, 17:19:49). The tree has 679 blobs. The scratch listing was in my session scratchpad (not kept).

Path search over the whole tree: `mail|teams|sharepoint` (case-insensitive) matches **0 paths**. The control `onedrive` matches 12 (MEASURED). **Mailflow, Teams and SharePoint have no code on main.**

Sizes are ESTIMATES in **lock-days**, in B2154's unit: one builder seat's day, including kit, build, gate and one fix round. **Non-lock days** are device or tenant runs, which need no heavy job, and record or text work. "Core" is the smallest journey per app that a user would call working on the M577. "Full" means every F-row for that app in `02 §3` on OXPd 1.x, excluding rows that exit in phases 5 and 6 (console rows F18, F43, F77, F78).

### A0. Shared infrastructure (serial; B2154's critical path, minus OneDrive-specific work)

| Item | On main | Missing | Lock-days | Non-lock |
|---|---|---|---|---|
| Agent host (B2154 L1) | SOAP 1.2 **client** only (PRs 37, 40, 41, 47, 51-54) | the endpoints the M577 calls (pre-prompt, prompt page, post-prompt, HID report), Reserve/HidOpen calls | 3 | 0.5 device (L1d) |
| Microsoft sign-in (L2) | `IGraphTokenSource`, `ITokenRefresher` interfaces only | auth code + PKCE, device code, app token, refresh | 2 | 0.5 tenant (L-C76) |
| Host composition (L3) | `ServerHost` refs Core, Adapters.Oxpd2, Secrets only | wiring of registry, broker, sign-in, Graph, jobs, apps | 2 | - |
| Panel shell (part of L4) | none | ES5 template, prompt page, app menu, sign-out | 1.5 | screens on device |
| 1.x scan (L6) | no HP scan-service description committed | description + client call (shared by **every** scanning app) | 2 | device |
| Network path (L9) | lab CA verbs built (PR 52) | the route and the CA in the M577 store (owed 103, 118) | 0.5 | device |
| Onboarding v1 (L7), card path (L8), end-to-end (L10), scaffold (L0) | lab verbs only | as B2154 | 0.5+1+2+1 | device |
| **Infrastructure total** | | | **about 15.5** (B2154's 16.5, minus L5's 1, which moves to OneDrive) | |

### A1. Per app

| App | Built on main (MEASURED paths and PRs) | Missing for CORE on the M577 | Core lock-days | Missing for FULL match (adds) | Full adds, lock-days | External dependencies (who) |
|---|---|---|---|---|---|---|
| **Hub (sign-in)** | SignIn actor, card paths, binding (PRs 23, 28); card store in CSA against fake Graph (27, 29, 32); token broker (9, 18); 5 decoders (3) | = infrastructure (WC-1: card tap, No-MFA and MFA, Microsoft's page, minimal enrolment) | in A0 | WP3.1 QR/phone gateway (SignalR), WP3.2 phone-redirect relay (customer Function App release), WP3.3 enrolment completeness, passkey, launch-after-sign-in, national clouds, error codes; WP3.7 settings roaming; WP3.13 tiles and panel classes; E2.2 wake-from-sleep 95/100 | about 10 | test user with Authenticator, app registration (Option A, the HPAM one, ruled C-25), CSA attribute set with the two attribute-admin roles, a reader and card (**Kam**: K2, K3); for QR/relay, the customer gateway Function App in a tenant (**Kam**, Azure); E1.3 needs a Workpath printer (**Steve M**) |
| **OneDrive** | `src/Datasec.Suite.OneDrive/`: browse My Drive, list-children only (PR 50; 7 files); Graph chunked upload (PR 10) | upload into a folder, download for print (L5), OneDrive pages (in B2154's L4) | 2 (1 + 1) | WP3.10: Shared libraries (F97, built on SharePoint's site/library code), rename, delete, create folder, search (F99), sort by size, tile/list, swipe and multi-select print, write gating, quota (F98), thumbnails; F38 send-to-email by Graph; the shared option model WP3.11 (counted once below). Plan size: **UNSIZED** (03:312) | about 5 | `Files.ReadWrite.All`, `Sites.ReadWrite.All`, `User.Read` consented (02 §7.2); an OneDrive licence on the test user (**Kam**) |
| **SharePoint** | nothing (0 paths) | sites (all/search) → libraries → folders, scan into a library, print a file (from 18 live Graph calls, A8 §5.2, RELAYED) | 3 (library 1.5, pages 1, tenant run 0.5) | WP3.4 in full: recent sites, column chooser, sort and group by column, edit column values, one input per editable column of five types at scan, create/rename/delete/search, list/grid, write gating, admin read-only | about 4 | **a SharePoint site with a document library with editable columns of the five types** (text, number, currency, yes/no, date), user a member (**Kam**, or agents with his word to create it by Graph); `Sites.ReadWrite.All` consent |
| **Teams** | nothing (0 paths) | teams → channels → channel files folder, browse, scan into the channel folder, print | 2.5 (reuses OneDrive's drive-item calls) | WP3.5: channel message with reference attachment (eTag GUID recipe), quick access and pins (F82, possibly dead behind `isSIOEnabled`, 03:307), folder print (F83, same), columns and group-by, search, several scan destinations; F81 Recent not built (coordinator's decision applying the Recent ruling) | about 3.5 | **a Teams team with at least one channel, with the test user a member, and a Teams licence** (**Kam**); consent to `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `Files.ReadWrite.All`, `ChannelMessage.Send` (02:546) |
| **Mailflow** | nothing (0 paths); the Graph layer's upload sessions exist (PR 10) | inbox list, read a message (sanitised HTML), compose to a typed address with the scanned file as attachment (draft → upload session → send; draft deleted on failure, E3.4) | 5 (sanitiser included) | WP3.6: filters, unread counts, search, People auto-complete, drafts, reply-all (`createReplyAll`), inline images, mark-read; **printing messages and attachments needs the converter (D18, WP0.9 "not started", 03:33)**; E3.5's eleven attachment types; admin max-attachment size; F36 hide on 4.3-inch panels | about 6 (+2 converter, shared) | **an Exchange Online mailbox on the test user** (**Kam**); consent to `Mail.ReadWrite`, `Mail.Send`, `People.Read`; a converter component and its licence (**Kam if paid**); an HTML sanitiser, either hand-written or a package by supervised fetch (C-61/C-62 pattern) |
| **Universal Print** | `src/Datasec.Suite.UniversalPrint/`: registration key pair, CSR, device-token holder; IPP encoder, reader, resumable stream (PRs 4, 17, 22, 58; 29 files). Its README: "Nothing here calls Universal Print ... The registration call, the admin sign-in, the device-token request ..., polling, the job map, the orphan report, the removal flow and the host wiring are later work" (MEASURED, read by GET) | **Direct only:** the admin sign-in of a Printer Administrator through a minimal admin API (part of WP1.11), the registration call, the device-token request, polling Get-Jobs, fetch with Range, IPPS Print-Job to the M577 (uses Jobs.Transport, PR 35). Needs no panel (03:399) | 5 | WP4.3 Pull (sign-in hook, F17 dialog, UPAR, sign-out timeout, Cancel-Job, S9 identity rule), WP4.4 Secure (list, preview, override, release), WP4.5 persistence and clean-up, WP4.6 capability sync and flavour changes, E4.10 GCC, E4.11 1 GB jobs; E4.5 needs a Workpath `_Pull` printer | about 8 | **Universal Print available in the tenant (a qualifying licence on the test users; which licence the tenant holds is UNMEASURED); a user with the Printer Administrator role; a ruling on OQ-9 (use Datasec's own Universal Print registration `CLIENT_ID_UP`, or a new one: "not ruled", 02 §7.1); a print share and a user given access in the UP portal** (all **Kam**); IPPS port (631 or 443, spike S6) reachable from the server to the M577 |

**Shared full-match items** (counted once): the WP3.11 scan and print option model with preview editing (plan size L: about 5 lock-days); the WP0.9 converter (about 2, plus a licence check); WP3.13 tiles, WP3.7 roaming and F30 buttons per app (about 2). WP3.12 is English only for phase 1 (A18, RELAYED, 03:314).

## B. Totals against 18 lock-days (Mon 30 Nov to Wed 23 Dec)

| Scope | Lock-days (ESTIMATE) | On ONE lock | Fits 18? |
|---|---|---|---|
| Infrastructure (hub at WC-1) | 15.5 | 15.5 | yes (B2154: about 1 day slack once OneDrive is included) |
| + OneDrive core | 2 | 17.5 | yes, just (this is B2154's WC-1) |
| + SharePoint, Teams core | 5.5 | 23 | **no** |
| + Mailflow core, UP Direct | 10 | **33** (about 30 if UP's admin piece shares L3) | **no** |
| + full match of all six | about 45.5 more | **about 78** | **no** (more than four times over) |

## C. What it WOULD take: options, cost and risk

### C1. More parallel builders (Kam's shape: serial infrastructure, parallel apps)

**Is the wave lock real? It is a convention (MEASURED).**
- `heavy.py` (newest copy `<P>/.tools/b2138/gate/heavy.py`, 93 lines) takes the lock by `os.mkdir(LOCK)`, with `LOCK = P + '/.tools/wave1-heavy.lock.d'`. It first reads load1 and waits while it is 7 or more.
- Nobody held the lock at reading (`ls`: no such directory).
- Machine (MEASURED, `sysctl`): `hw.ncpu` 18, `hw.memsize` 137438953472 (128 GB), "Apple M5 Max"; `uptime` load averages 2.14 1.96 1.63; disk 842 GiB free.
- Lock time per lane (MEASURED from the quarantined lock folders and `gate.log`):
  - B2138: 19 jobs from 11:20:44 to 11:33:16;
  - B2134: 38 jobs from 03:57:34 to 04:49:26;
  - whole-solution test `duration: 58s 054ms` (B2138 `chain-test.log`);
  - builds `Time Elapsed 00:00:07.48` and `00:00:01.25`.
- Each lane builds in its own `<P>/.tools/b<n>/clone/` with its own bin/obj (MEASURED for B2138).
- The test listeners I read bind port 0: `HostRig.cs:82` `https://127.0.0.1:0`; `HttpIppTransportTests.cs:99, 186, 386`. The fixed ports 7627 and 8443 in tests appear in URI strings, not in listeners I found. A full audit for fixed listeners is UNMEASURED.
- The NuGet cache is shared (`.tools/nuget-packages`). It is safe to read in parallel. It is unsafe only if two lanes restore a NEW package at once, and no lane adds a package by default.

**What really serialises work:**
1. **One M577.** Its panel can hold one session at a time, and Kam switches it on per window (pickup protocol, RELAYED from Tuesday commit fa511bdfd4).
2. **Tuesday's gate and merge throughput.** Each PR needs a reader, a squash pinned to head, and records. The measured merge pace (by UTC day) was 4, 11, 17, 13, 6, 3, 3, 1 PRs per day from 20 to 27 Nov. The peak shows that 10 or more a day has been carried. The recent 3 a day reflects deeper, device-adjacent rounds.
3. **Usage limits.** Kam: "I will sign into as many accounts as necessary", RELAYED.
4. **Owed 137 and 138.**

**What must land first:**
- **138 first:** the runner kills `dotnet test` at its bound but not the test host, which is left orphaned with parent 1 (`BACKLOG.md` item 138). The fix is the coordinator's own file and needs no repo PR: start each job in a new process group and kill the group at the bound. With parallel builders, an orphan otherwise survives into other lanes' load readings.
- **137 next** (B2153, already drafted): a bound on `HostRig.StartAsync`/`StopAsync`. The hang was seen twice and cost 15 and 30 minutes. It blocks any lane that runs `Server.Tests`, which means the host lane (L3) and every whole-solution run.

**Per-project locks (proposal; default for Tuesday):**
- A reader-writer pair.
  - A project job (`dotnet test tests/<X>.Tests` in the lane's own clone) takes `.tools/locks/<X>.lock.d` and waits while `wave1-heavy.lock.d` exists.
  - A whole-solution job (gate only) takes `wave1-heavy.lock.d`, then waits until no project lock exists.
- Keep the load gate. Raise its 1800 s wait only if it proves too short. Four project-scoped builders at about 1-minute jobs should stay under load1 7 on 18 cores. This is UNMEASURED: one trial day, with the lane folders' `gate.log` counting waits, measures it.
- Cross-project breakage is still caught: CI's hosted Linux and Windows legs run the whole solution on every PR. They run on GitHub, not on this machine.
- **2-4 builders are safe** if 138 and 137 have landed, each lane has its own clone, packages are pre-fetched, and the L0 scaffold below is in.

**Per-app lane ownership (disjoint):**

| Lane | Owns (only it writes) | Reads (public API, no edit) |
|---|---|---|
| INFRA (one seat, serial) | `src/Datasec.Suite.Adapters.Oxpd1.Agents/**`, `src/Datasec.Suite.Identity.Entra/**`, `src/Datasec.Suite.Server/**`, `src/Datasec.Suite.Panel/Shell/**`, `src/Datasec.Suite.Onboarding/**`, `contracts/oxpd1/**` + `src/Datasec.Suite.Adapters.Oxpd1/**` (L6 scan), and their `tests/*` | everything |
| ONEDRIVE | `src/Datasec.Suite.OneDrive/**`, `tests/Datasec.Suite.OneDrive.Tests/**`, `src/Datasec.Suite.Panel/Apps/OneDrive/**` | Graph, Sessions, Jobs; SharePoint's site/library API (for F97, after SharePoint publishes it) |
| SHAREPOINT | `src/Datasec.Suite.SharePoint/**` (new), its tests, `src/Datasec.Suite.Panel/Apps/SharePoint/**` | Graph, OneDrive drive-item API |
| TEAMS | `src/Datasec.Suite.Teams/**` (new), its tests, `src/Datasec.Suite.Panel/Apps/Teams/**` | Graph, OneDrive drive-item API |
| MAILFLOW | `src/Datasec.Suite.Mailflow/**` (new), its tests, `src/Datasec.Suite.Panel/Apps/Mailflow/**` | Graph, Jobs |
| UNIVERSALPRINT | `src/Datasec.Suite.UniversalPrint/**`, its tests, `src/Datasec.Suite.AdminApi/UniversalPrint/**` (new, minimal) | Jobs.Transport, Secrets, Devices |

**The shared touches, and how to batch them:**
1. **`Datasec.Suite.slnx` and `Directory.Packages.props`.** The L0 scaffold (INFRA, Mon 30 Nov, 0.5 day) adds **every** new project in one PR: the four infrastructure projects plus SharePoint, Teams, Mailflow, Panel and AdminApi, each with an empty test project and a lock file. After that, no app lane touches the slnx. A new package is a stop and a card.
2. **The host's app registration.** L0 defines `IAppModule` (register services, map routes, declare panel entry and Graph scopes) in Server. The INFRA lane's L3 puts one line per app into `ServerHost` up front, pointing at an empty module in each app project. App lanes then fill their own module and never edit Server. Any later host change goes through INFRA, batched once a week (Fridays).
3. **Panel menus and buttons.** The app list (title, icon, route, panel-class rule F36) is a file in `Panel/Shell/` written once in L4-shell with all five entries, each hidden until its module reports ready. The OXPd 1.x top-level buttons (one per app, F30, `RegisterTopLevelButton`) are one list in Onboarding (L7). Both belong to INFRA.
4. **Graph scope union** (02 §7.2: the server requests the union of enabled apps). Each module declares its own scopes in its `IAppModule`, so there is no shared edit.
5. **OneDrive drive-item code used by Teams, and SharePoint site/library code used by OneDrive F97.**
   - Teams and SharePoint consume OneDrive's public API. If they need a change in OneDrive, the OneDrive lane makes it.
   - SharePoint publishes its site/library API before OneDrive builds Shared libraries. This is an order only, not a shared path.

**Can each app's heavy jobs stay in its own test project?** Yes for the library work (fake Graph, the OneDrive.Tests pattern). Panel page tests sit in `tests/Datasec.Suite.Panel.Tests/Apps/<App>/` folders, which is one shared test assembly. **Either** split per app (`tests/Datasec.Suite.Panel.<App>.Tests`, created in L0; my default) **or** run the Panel assembly under the wave lock. Host integration (an app reachable through `ServerHost`) runs `Server.Tests`, so it needs 137 landed and stays under the wave lock at the gate.

**Cost:**
- 4-5 concurrent build seats. Usage at roughly 4-5 times today's build burn: Kam has offered accounts.
- Tuesday needs extra gate-reader seats (one reader per 2-3 PRs a day) and a records seat full-time.
- One trial day measures the load gate.

**Risk:**
- Merge conflicts if L0 misses a project.
- Device-window contention.
- More PRs mean more review findings, so fix rounds grow.
- 137's cause is UNMEASURED; a bound hides it rather than fixing it.

### C2. Scope: core journeys first, then full match

The commission names this as q15 option a; I did not re-read the card's option text, so this is RELAYED. Kam ruled b (C-16), so core-first is a **sequencing** choice for Christmas, not a scope cut. It is a card for Kam only if he reads "all apps by Christmas" as full match. Full match on the M577 follows in January (section E).

Cost: none in rework, provided each app's core uses the same module the full version extends. Risk: the deviation register (E3.1) must not be used to defer scope (03:233, "A deviation is never used to defer scope (C-16)"), so the core-first label must be called a milestone, not a release.

### C3. Kam-side inputs and their latest dates

| # | Input | Needed for | Latest date | Ruled already? |
|---|---|---|---|---|
| D1 | Test user with Authenticator in `datasec-rd.com` (C-80 w7, RELAYED), app registration (Option A, C-25), CSA attribute set + two attribute-admin roles, admin consent to the delegated union of all five apps | sign-in test, every app's tenant run | **Wed 2 Dec** (sign-in test), Mon 7 Dec at the latest | user asked (OXPD2-61, RELAYED); registration, roles and consent not asked anywhere I found (B2154 K2) |
| D2 | Licences on the test user covering Exchange Online, OneDrive, SharePoint, Teams; **Universal Print** eligibility | Mailflow, Teams, SharePoint, OneDrive, UP runs | **Mon 7 Dec** | none; which licences the tenant holds: UNMEASURED |
| D3 | A Teams team with a channel; a SharePoint site with a library carrying the five column types; a mailbox with some mail and attachments. Kam may make them himself or give agents his word to create them by Graph | Teams, SharePoint, Mailflow core | **Thu 10 Dec** | none |
| D4 | Universal Print: Printer Administrator role on a user; OQ-9 ruling (Datasec's `CLIENT_ID_UP` or a new registration); a print share and an assigned user | UP Direct | **Thu 10 Dec** | OQ-9 "not ruled" (02 §7.1) |
| D5 | Card reader + test card on the M577 (K3) | hub WC-1 | Mon 7 Dec (without it: WC-0, no card) | none |
| D6 | K6 (sign-in agent takeover during test runs) and **K7 widened to five home-screen buttons** (one per app, F30), removed by undo after each run | every app's device run | Thu 10 Dec | C-84 "We ask again before any home-screen app is added": card required |
| D7 | Printer on for one device window a day, Tue 1 Dec to Wed 23 Dec; his availability 21-23 Dec | every device run | from Tue 1 Dec | protocol RELAYED (fa511bdfd4) |
| D8 | Converter component (WP0.9) and its licence, if paid; a sanitiser package fetch if the reviewer refuses hand-written | Mailflow print (full), Mailflow core (sanitiser) | Fri 4 Dec for Mailflow core | none |
| D9 | Parallel builders | all of C1 | Mon 30 Nov | Kam: "dont forget this machine can handle multiple agents" (RELAYED). Per-project locks are Tuesday's rule to change (B2154 Q4) |
| - | Steve M: a Workpath printer for parity comparisons (E1.3, E3.2, E3.5, E4.5) and the W30-W40 parity answers | full match only | January | tickets' status UNMEASURED |

## D. Schedule: infrastructure dates, then N app lanes in parallel

Assumptions: 138 lands Mon 30 Nov morning and 137 by Tue 1 Dec. The inputs D1-D7 arrive by their dates. There is one INFRA seat plus up to two infrastructure helpers on disjoint projects, and four app seats. Weekdays are by `date -j`.

| Dates | INFRA (serial chain) | INFRA helpers (parallel, disjoint) | App lanes (4 in parallel) | Device window (one at a time) |
|---|---|---|---|---|
| Mon 30 Nov | L0 scaffold (all projects, `IAppModule`, panel per-app test projects) | 138 runner fix; B2153 (137) | **start libraries against fakes:** OneDrive L5; SharePoint sites/libraries; Teams channels/files; Mailflow list/read/sanitiser; UP admin sign-in and registration call | - |
| Tue 1 - Fri 4 Dec | L1 agent host (3) | L2 Entra sign-in (2); L6 1.x scan (2) | libraries continue; UP device-token + polling | L9 network path and CA (Tue 1, milestone M-a) |
| Mon 7 - Wed 9 Dec | L3 host composition (2), app module lines in | L-C76 panel sign-in test (needs D1) | Mailflow compose/attachments; UP IPPS push; SharePoint/Teams scan-to-destination calls | L1d (Mon 7); L-C76 (Tue 8) |
| Thu 10 - Fri 11 Dec | L4 panel shell (1.5) | L7 onboarding v1 (1) | **app pages start** on the shell (OneDrive, SharePoint, Teams) | UP Direct first device print (Fri 11, needs D4) |
| Mon 14 - Wed 16 Dec | L8 card path (2), L10 WC-1 (1) | fix rounds | app pages; tenant runs per app | WC-0 Mon 14; OneDrive device run; WC-1 Wed 16 (needs D5) |
| Thu 17 - Wed 23 Dec | infrastructure fixes only (owner of host/panel shared touches) | - | SharePoint, Teams device runs; Mailflow pages; UP Direct evidence | one app per day: SharePoint Thu 17, Teams Fri 18, Mailflow Mon 21-Tue 22, re-runs Wed 23 |

**Resulting dates (ESTIMATE):**
- **Infrastructure (hub WC-1): about Wed 16 Dec** with helpers. On one lock it is Wed 23 Dec (B2154).
- **All apps at core journeys: Wed 23 Dec at the earliest, if every condition holds.** The probable slip is Mailflow core (largest, sanitiser and attachments) into **Mon 4 to Fri 8 Jan 2027**.
- **All apps at full match on the M577: about Fri 29 Jan 2027.** That is about 45 more lock-days over 4-5 lanes, so about 10-12 working days from 4 Jan, plus Workpath-printer parity runs and Steve M's answers. The holidays (25 Dec to 1 Jan) and Australia Day (Tue 26 Jan) are counted as non-working. Team working days over the break are UNMEASURED.
- **For comparison, on one lock with no parallelism:** core for all apps is about early to mid January (33 lock-days from 30 Nov). Full match is about mid March 2027.

## E. Verdict

- **All apps at full match by Christmas: NO.** About 78 lock-days of work against 18 days and one printer. Parity checks need a Workpath printer and Steve M, and neither is booked.
- **All apps at core journeys by Christmas: NO on the single wave lock; YES only under all of these conditions, and even then not likely (most likely Mailflow slips to early January):**
  1. 138 by Mon 30 Nov and 137 by Tue 1 Dec;
  2. per-project locks plus the L0 scaffold, with 4-5 builders from Mon 30 Nov;
  3. Tuesday's gate and merge carry about 5 PRs a day (extra reader seats);
  4. D1 by Wed 2 Dec, and D2-D5 by Mon 7 to Thu 10 Dec;
  5. the M577 on daily for one window, and no device blocker at M-a (Tue 1 Dec: CA and route) or at S2 (Mon 7 Dec: the printer calls our host);
  6. core means: Mailflow without printing mail bodies, and Universal Print Direct only;
  7. Microsoft's page works on the old panel, or the QR device-code fallback (K14) is accepted.
- **Realistic full match on the M577: late January 2027 (about Fri 29 Jan).** Release 1 as the plan defines it (E6.8: OXPd 2 as well, both packagings, pilot) is later and depends on HP and an OXPd 2 device. It is not dated here.

## F. UNMEASURED and disclosures

- Every size and date in sections A-E is my ESTIMATE in B2154's unit. Nothing was built or run. The ratio of lock-days to PRs is not measured.
- How much load 4-5 concurrent project-scoped builders put on this machine, and whether the load gate (load1 < 7) then throttles them: UNMEASURED. One trial day measures it.
- Fixed-port listeners: only `HostRig.cs` and `HttpIppTransportTests.cs` were read. They were read in the B2138 clone at `b3248f8c`, not at main 760e1a64. A full audit of the test tree is UNMEASURED.
- Which Microsoft licences the `datasec-rd.com` tenant holds (Exchange, Teams, SharePoint, Universal Print eligibility): UNMEASURED. My statement that Universal Print needs a qualifying licence is general knowledge, not checked against Microsoft's page in this lane.
- Whether Teams F82/F83 are dead behind `isSIOEnabled` (03:307: "likely and not traced"); if they are, the Teams full size shrinks.
- WP3.10 (OneDrive completion) is UNSIZED in the plan itself (03:312). My about-5 is a guess.
- The q15 option-a wording was not re-read (RELAYED from the commission). Jira was not read (B2154's fence on `4_Credentials/.env` kept).
- Read in part: `02_architecture.md` §3.3, §3.4, §5.6, §7.1-7.3; `03` lines 1-155, 217-256, 255-404 (phases 0-6 work packages, dependencies). `BACKLOG.md` was read only for items 137-139. CLARIFICATIONS was read by search plus C-16 and C-88 to C-92.
