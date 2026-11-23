# B1996 DESIGN REVIEW: Datasec / OXPd_2, the architecture, plan and readiness documents against what was built and against the M577 finding

Reviewer B1996 (Fable 5.2, in-session, read-only) for Tuesday (s317), 2026-11-23, written 17:26 to 17:50 AEDT. Commission: `2026-11-23_B1996_OXPD-DESIGN-REVIEW_COMMISSION.md`. Nothing in the project, on GitHub or on any device was changed; no printer was contacted. Everything here is a proposal: the coordinator and the product owner decide.

Short names used below: `02`, `03`, `05` are the three design documents under `<project>/1_Project_Definition/Design/`; `CL` is `CLARIFICATIONS.md`; `C1`, `C2` are analysis reports; `main` is the code at `d804de5e` (read from a GitHub snapshot unpacked in scratch, `2_Project_Files/fleet/state/s317/d1996/src/`, cited as `src/...:line`); `B19nn` is a gate verdict.

## BLUF

1. The design is still right in its shape: one server, two printer adapters, both generations in release 1. The product owner's card q09 already put the older printers (FutureSmart 4.7 to 5, OXPd 1.x) in the target fleet, so the M577 is inside the design, not outside it.
2. What is wrong is the ORDER and the EVIDENCE. Every document, and almost all the code, leads with the newer printers (OXPd 2). The only printer in hand is an older one. Nothing built so far can be proven on a real device except the small older-printer read client landed today.
3. Three decisions should be taken before more product build on the older track: where Microsoft's sign-in step happens on older printers (N-1), how a site printer reaches a server in Azure (N-5), and whether the older-printer adapter uses HP's own library or our hand-written one (not recorded anywhere in the design; it touches HP's licence clause).
4. The next wave has no lane for the work the M577 needs. The product owner approved a first-run list today (read, panel capture, certificate, test button, test sign-in agent). Only the first two reads have code; nothing writes to an older printer, and the lab tool cannot call the older-printer client at all.
5. Recommended: make the older-printer slice the lead slice on real hardware, run the long-postponed test S2 (can our server host the older printers' call-backs) on the M577 this week, and keep the newer-printer work on stubs until a FutureSmart 6 printer or the simulator arrives.
6. 19 findings; 3 need a decision before more build on the older track. None stops the lab tooling.

---

## 1. The printer generation

**What is established (re-read at source).** HP's M577 firmware readme, `fleet/state/s315/d1968/dl/readme_cljM577_fs5.txt`: lines 12 to 14 give revision 2510156_069175, datecode 20260828, "FutureSmart Bundle Version 5.10.0.7"; `grep -o -i -c` counts 21 "FutureSmart Bundle Version 5" lines and 0 "Version 6" lines, 7 mentions of OXPd. The printer's own firmware level is UNMEASURED (no connection yet). Card q09 (`decision_queue.sh show datasec-oxpd-q09-printer-generations-1118`), ruled option a, DETAIL: "Older track on 4.7 to 5, newer track on 6." So the target fleet is both generations, and the device in hand is on the older track.

**Still right, no change needed:**
- The two-adapter shape (`02:15`, `02:274`, decision D2 at `02:901`), the per-device platform probe (`02:246`), the device scope D32, and release 1 on both generations (D33). They match q09.
- The OXPd 2 parts already built (generated clients, token client, call-back host). They are in the fleet's scope. They are unproven on any device and will stay so until a FutureSmart 6 printer or the simulator exists (`03:264`).
- Plan line `03:264` already says "phase 2 can start alone" when no OXPd 2 device exists. The plan foresaw today's position; it was just never made the working order.

**F1. The sign-in design for older printers contradicts itself, and the first printer test has changed under it. NEEDS THE PRODUCT OWNER'S WORD (N-1).**
- FOUND: `02:414` and decision D10 (`02:909`) put Microsoft's step on the panel (his words W1, `CL` C-60 message 1). The method table in the same section still gives older printers the phone methods: `02:429` "| OXPd 1.x | M1 or M2 | M5 | M1 or M2 | M3 (+ M1/M2) | M1 |". Open question N-1 (`03:443`) asks whether the on-panel step applies to older printers; its default is "built on the OXPd 2 page first; nothing of the phone route built for 1.x before the 1.x panel test reports". The first printer test, S4 (`03:57`), is written for Chromium 87 on a newer printer and cannot run on the M577. `02:414` itself records that a partner's on-panel Microsoft sign-in failed on older printers (memory and certificate trust), and the page budget there is 2 to 3 MB.
- So: on the only device in hand, the first test is now the older-panel test, the one the design itself expects to be hardest. If it fails, what follows is N-3, which nobody has decided. The whole older track could be left with no agreed sign-in for MFA users.
- TESTED: the three places were read at source; `CL` was searched for N-1 (1 hit, in C-58's list of things left open, not a ruling; control C-63 found) and today's rulings (`kam_rulings_today.sh`, 9 rows) name neither. NOT tested: any panel. HOW: read, grep with a positive control.

**F2. Three documents still say the M577's generation is unknown and that it will be wiped for developer mode. NEEDS A TEXT UPDATE.**
- FOUND: `05:245` ("Which OXPd generation an M577 belongs to is still not established"), `05:290` ("Nothing is established about the M577"), `05:220` (Test 1 "Needs: the printer wiped into developer mode"), `03:42` ("which OXPd generation an M577 covers is not established"). Developer mode exists only on FutureSmart 6 (`02:262`); it does not apply to this printer, and card `datasec-oxpd-printer-route-1123` (ruled a, 11:08) already told him "it needs no wipe and no developer mode".
- `CL` has 1 mention of M577 (C-39) and 0 of "FutureSmart 5" (control: C-63 found 1). The finding is recorded in briefs and a card, not yet in the project's own records.
- TESTED: grep counts on the untruncated files. HOW: `/usr/bin/grep -o -c`.

**F3. The phase order leads with the generation nobody can test. NEEDS A 1.x-FIRST WORKING ORDER (coordinator's call; tell the product owner).**
- FOUND: Phase 1 is "thin vertical slice on OXPd 2" (`03:75`); Phase 2 is "the same slice on OXPd 1.x" (`03:92`), defined only by reference to Phase 1's criteria. Every exit test of Phase 1 needs a FutureSmart 6 device in developer mode or the simulator; neither exists (B1968 section 4; the simulator image folder is empty, B1968 premise 23).
- The older-printer slice can be proven on the M577 now. The newer-printer slice can only be built against stubs.
- TESTED: the plan lines read at source. NOT tested: sizes.

**F4. The test that decides how the older-printer adapter is built (S2) has never been run, and it can run now. NEEDS A 1.x PATH, MOVED UP.**
- FOUND: the adapter's design is "CoreWCF for the agent side (inferred ... no HP source shows agents hosted on CoreWCF)" with a Java fallback (`02:363`, D3 at `02:902`). Spike S2 (`03:55`) is what proves or replaces it: a real FutureSmart device calling our server's SOAP end over HTTPS. It also records what the older panel's browser sends on a page request (risk R23, `02:603` "design intent, not yet proven"). The M577 is the first device that can answer it. No lane in waves 1 to 3 of B1969 builds an older-printer call-back host.
- NOT tested: anything on a device.

**F5. Phase 1's hosting (the client's Azure) has no answered network path for older printers. NEEDS THE PRODUCT OWNER'S WORD (N-5).**
- FOUND: `02:248` states older printers need two-way traffic on fixed port 7627 with no address translation, and concludes "Server on the customer LAN; a cloud-only server is not viable without a site relay". `02:14` and D1 (`02:900`) put Phase 1 in the client's Azure subscription (his words, `CL` C-60 messages 3 to 5). The trust diagram still labels the server "(customer LAN)" (`02:585`). The proposed test S14 (`03:67`) says "OXPd 1.x first" and waits for his word because it needs an Azure resource (C-42). `CL` has 0 hits for N-5 (control C-63: 1).
- With the older track now the lead track, this is the first hosting question, not the second. The lab (Mac and printer on one network, B1968 step 2) does not answer it.
- NOT tested: any network path.

**F6. The M577 covers one firmware level and one of two older panel browsers; which is not yet known. STILL RIGHT, with a note.**
- FOUND: the design names two older browser engines (WebKit 534 and 605, `02:256`) and a 4.7 floor that ships "expected, untested" without a 4.7 device (`03:40`, D32). Firmware faults differ by level (TLS 1.3 scan uploads fault on 5.5 to 5.7, `02:629`). The M577's level is unread until first contact. One printer cannot stand for the older track.

**F7. Older printers refuse a server named by IP address; the first-run list has no step for a name. NEEDS A 1.x PATH ITEM.**
- FOUND: `C1:93`: the device "requires the certificate Subject CN to match the URI host exactly ... this precludes IP addresses"; `02:627` repeats it. B1968's needs list has 0 mentions of DNS, FQDN or host name (control "certificate": 4). Steps 4 and 5 of the approved first-run list register a button and a sign-in agent "pointing at this Mac". Without a name the printer can resolve, and a certificate issued for that name, those steps will fail for a reason that looks like a product fault.
- TESTED: grep counts with control. NOT tested: whether the M577 resolves local names (mDNS or the router's DNS): UNMEASURED.

**F8. A recorded revisit point will not get the evidence it was waiting for.**
- FOUND: C-63 (`CL:610` onward): the strict reading of a printer's answers is to be revisited "after Monday's printer test shows real traffic". That decision concerns the OXPd 2 contract reader (pull request 14). Monday's printer is an older one; its traffic is SOAP, not the OXPd 2 answers. The revisit should be re-pointed at the first OXPd 2 device or simulator run, and said so to him, since he asked that the decision be noted as changeable.

---

## 2. The design against what is built (main `d804de5e`, 17 projects)

Evidence base: the snapshot's project files and sources; the gate verdicts B1979 to B1987 and B1990 were read as evidence. Sizes by `wc -l` over non-generated `.cs` files.

**F9. There is no core and no shared device model yet. A decision nobody recorded; the risk is where the wiring lands next.**
- FOUND: the architecture's centre is one internal device model that both adapters translate into (`02:381` to `02:409`: ten events up, nine commands down; "the core never sees SOAP or REST", `02:249`). On main, `Datasec.Suite.Core` is 8 lines (`src/Datasec.Suite.Core/AssemblyMarker.cs:4`: "The core holds no logic yet"). Each library defines its own narrow seam (`ISignInDevice`, three methods, `src/Datasec.Suite.SignIn/ISignInDevice.cs:7`; `IOxpd2CallbackSink`). The host references the OXPd 2 adapter directly and its routes are `/oxpd2/devices/...` (`src/Datasec.Suite.Server/ServerHost.cs:19`, `:50`, `:51`). The older-printer adapter is referenced by nothing.
- Whose fault: nobody's; the libraries were built bottom-up and are generation-neutral where it counts (Sessions and Sign-in carry the platform: Sessions README:17, Sign-in README:13; Devices has both platforms, `DeviceVocabulary.cs:6-7`). But the plan's guard, E2.4 ("the core assembly references neither adapter", `03:96`), is true today only because the core is empty. The next lanes (B1969 wave 3: the identity-to-sign-in adapter in `Server/Composition/`, then "sign-in actor wiring") will put the real joining code in the host, beside OXPd 2 routes.
- Proposal: before that wiring, land the device-model contract of `02` section 5.4 as a small assembly that both adapters implement, and write E2.4 against it. Otherwise the host becomes the place where "if OXPd 2 ... else ..." lives.
- TESTED: the reference graph, by reading every `.csproj` (17). NOT tested: a build.

**F10. The older-printer client is hand-written; the design says HP's library. A decision recorded only in a build kit. NEEDS RECORDING, and it sharpens the licence question.**
- FOUND: `02:363` (component C3): "SOAP client to device services on 7627 (OXPdLib .NET 8 build, client side)"; `03:169` (WP2.1): "SOAP client wrapper (no password in `ToString`)"; risk R16 (`02:958`): "OXPdLib 1.x redistributed unchanged". On main the client is "written by hand: SOAP 1.2 over `HttpClient` and `XmlWriter`, no package" (`src/Datasec.Suite.Adapters.Oxpd1/README.md:3-4`). The kit that chose this says every choice in it is "the coordinator's, none the product owner's" (`Briefs/2026-11-23_B1976_SEAT-X49_oxpd2-x1.md:29`). The deviation register has 0 hits for OXPdLib, hand-written or CoreWCF (control "DEV-": 34); `CL` has 0.
- Two consequences. (a) HP's specification says solutions "shall not interpret the DiscoveryTree XML file directly, but shall instead use the OXPdDiscoveryTree class" (quoted in the kit, line 36); the design's onboarding step 1 is "Discover and probe the DiscoveryTree; record service revisions; refuse Pro and below FS 4.7" (`02:819`). Without HP's library the client fetches the tree and does not read it (adapter README:67-69), so the design's platform probe has no built means on older printers. (b) HP's licence clause (risk R32, `02:974`; `C1:316`) forbids "any other means of reverse engineering" on the protocol HP's libraries use. A client built from HP's published service descriptions may well be fine; a hand-written one is further from "HP's library, unchanged" than the design intended. R32 is unsettled and the question to HP (H6) is unsent.
- Fine for a lab read tool. Not yet a decision anyone should assume for the shipped adapter.
- TESTED: grep counts with controls; the quoted lines read. NOT tested: HP's guide itself (read through C1 and the kit).

**F11. The document says the older printers use the 2004 addressing standard; HP's own service files use the 2005 one. Document unverified; the device decides.**
- FOUND: `02:249`: "SOAP 1.2 + WS-Addressing 2004, both directions" (from `C1:78`, HP's prose specification). Gate B1980 finding 3 measured the 14 committed HP files: the 2004 prefix is declared in 8 files and used 0 times; the four bindings use the 2005/08 namespace. The client was changed to 2005/08 (B1987 line 24; adapter README:16). Which one a printer accepts is UNMEASURED (adapter README:56-60). If the device wants 2004, all five reads fault on first contact. The same question governs the call-back host of F4.
- Proposal: the first connection tries one read; keep the other namespace one switch away; amend `02:249` after the result.

**F12. The call-back credential code is bearer-only and lives inside the OXPd 2 adapter. Code structure; cheap to fix now.**
- FOUND: the design gives both generations a per-device call-back secret: "OXPd 2 target `authorization`, OXPd 1.x registration network credentials" (`02:603`), that is, HTTP Basic on older printers (`02:588`). `CallbackCredentials` accepts exactly "Bearer" (`src/Datasec.Suite.Adapters.Oxpd2/Callbacks/CallbackCredentials.cs:10`, `:18`) and sits in the OXPd 2 assembly with its vault interface (`Device/IDeviceSecretVault.cs`). The older adapter cannot use it without referencing the OXPd 2 adapter or copying it.
- Proposal: move issue, hash, constant-time check and vault binding to a shared assembly with the scheme as a parameter, before the older-printer host is written.

**F13. Four separate copies of the "trust this printer's certificate" rule; the printer's fingerprint is stored nowhere. A cross-lane gap no single gate could see.**
- FOUND: the pin check is written four times, in four assemblies that share no code: `src/Datasec.Suite.Lab/Device/DeviceChannel.cs:59`, `src/Datasec.Suite.Jobs.Transport/HttpIppTransport.cs:44`, `src/Datasec.Suite.Adapters.Oxpd1/Oxpd1Client.cs:50`, `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/DeviceTokenClient.cs:75`. Each was reviewed by its own gate. Gate B1979 finding 2 found that one copy does not switch off certificate downloads during chain building (a printer, or someone in between, could make the server fetch a URL before the pin refuses; proven absent on macOS only, Linux and Windows UNMEASURED). Whether the other three copies have the same gap was nobody's question.
- The design says the device certificate is "pinned at onboarding (trust on first use, recorded, admin-confirmed)" and watched for change (`02:605`, `02:630`). The device record holds no fingerprint: 0 hits for pin, fingerprint or thumbprint under `src/Datasec.Suite.Devices` and `src/Datasec.Suite.Data` (control "serial": 39).
- Proposal: one device-trust component (the check, the chain policy, the stored fingerprint, the change alert), used by all four; one gate reads it once.
- TESTED: grep with control; the four call sites printed. NOT tested: the three other copies' chain policy (not read line by line): UNMEASURED.

**F14. HP's older-printer service files are in the repository on the coordinator's reading of his words, not on a recorded ruling.**
- FOUND: `contracts/oxpd1/hp/` holds 14 HP files. C-56 records the exception as "exactly the files" of the OXPd 2 list (`CL:414`). The kit says that his words cover the older files "is the COORDINATOR'S reading, stated to him on the live board with leave to correct ... it is not his ruling" (kit line 27). The repository's own rule R5 still exempts only the OXPd 2 list (adapter README:79-81). Not a fault; a records gap. One line from him closes it.

**F15 is in section 3** (the lab tool cannot reach the older printer; no write tooling).

**The server's role, as built:** a host with a health route, five OXPd 2 call-back routes and a notification route; no database start, no admin interface, no sign-in (`src/Datasec.Suite.Server/README.md:4`, `:58`). That is honest and matches WP1.11's first part. Whether a printer sends the call-back credential to its notification target at all is UNMEASURED (Server README:63-64); the install-code step of onboarding depends on it.

---

## 3. The plan's order

**F15. The next wave does not build what the approved first run needs. MOVE UP.**
- FOUND: his ruling of 11:08 today approves "the first-run list from the PDF (section 2a)": 0 discovery read; 1 device information over OXPd with the admin password; 2 switch on the Test service and take a panel screenshot; 3 upload our development CA; 4 register a test button; 5 register a test sign-in agent, then remove it; 6 one test print (B1968 section 2a).
- On main: step 0 has the lab `probe`. Step 1 has the read client, but the lab tool cannot call it: 0 mentions of Oxpd1 under `src/Datasec.Suite.Lab` (control Oxpd2: 2) and no project reference. Steps 2 to 5 are writes; the client is read-only by design ("No write", adapter README:24). Step 6 is lane L4, being drafted.
- Wave 2 as drafted is L4, FK, O1. L2 and L3 (panel driver and install sequencer) are rightly held: both are OXPd 2 in developer mode. Nothing replaces them for the older printer.

**What I would move UP (in this order):**
1. **Lab read for older printers**: a lab command over the landed client (first-run step 1), with the stop-after-one-failed-password guard B1968 names (five wrong passwords lock the admin account).
2. **A lab server name and certificate** the printer accepts (F7): a development CA, a certificate for a real host name, and a note of how the printer resolves it.
3. **The older-printer write client, one undoable call at a time**: Test service on and panel capture (the older-printer equivalent of L2, and what lets agents see the panel without him); certificate import and delete; register and unregister a button; register and unregister a sign-in agent. Each ships with its undo and a dry-run default, as L3 was designed.
4. **Spike S2: the call-back host for older printers** (F4), behind the shared credential of F12. Decide first whether it is CoreWCF (a package fetch, so a card under C-61) or hand-written to match the client; the M577 result picks the product design.
5. **The older-panel test of Microsoft's page** (F1): one plain page in the older template that starts Microsoft's sign-in, measured for memory and certificate trust. It needs a test tenant user, which is his to supply.
6. **The device-model contract** (F9) and **the shared trust component** (F13), before any sign-in wiring in the host.

**Keep:** L4 (the print command works on either generation and gives S6 on the M577). FK (contract follow-ups) is sound hygiene and blocks nothing.

**Move DOWN:** O1 (OneDrive against a fake Graph). It is honest no-hardware work, but it reduces none of the unknowns above, and its panel side depends on the sign-in answer. Run it only on a spare seat. Further OXPd 2 host work (sign-in wiring on `/oxpd2/` routes) should wait for F9.

**Keep OUT for now:** anything Azure-specific (N-5, C-42); the phone sign-in routes for older printers (N-1's default says build nothing before the panel test reports); L2 and L3 until a FutureSmart 6 device or the simulator exists.

**One caution on pace.** Today's wave landed five lanes with 8 gate rounds. Every one of them carries "UNMEASURED on a device". The stock of unproven code is now large relative to the proven stock (zero). The first connection will likely overturn some of it (the endpoint path prefix is "in no committed file", adapter README:61; the addressing version, F11). Favour lanes that convert unknowns into measurements over lanes that add more code against stubs.

---

## 4. Security and design risks no single lane gate could raise

**F16. On older printers the admin password is an everyday working credential, and the older track is now the lead track.**
- `02:251`: "HTTP Basic `admin` on every admin-class call, including run-time calls"; stored "for the server's life" (C-24; `02:614`). A compromised server is administrator of every older printer at the site. A server fault that repeats a wrong password locks the admin account (five attempts on FutureSmart 4 and later, B1968 premise 10), fleet-wide. And if Phase 1 runs in Azure (F5), that password crosses the site-to-cloud link on every run-time call. The design names "lockout-aware retry" (`02:614`); no built component owns it. It belongs in the shared device-trust component of F13, with one attempt counter per printer across every caller.

**F17. Credential rotation is per process; the design's two-server pair would disagree with itself.**
- Gate B1981 item 3: the call-back credential cache is per instance, so "a rotation by ANOTHER process after the host cached the old hash leaves the host on the old one until restart". The design's availability model is an active/passive pair on one database (`02` section 5.8). After a switch-over, the second server's cache and the secret store's locality (a local key file per machine, `ServerHost.cs:31-36`) both need a rule. No lane owns it; it is cheap now and expensive after sign-in is wired.

**F18. A printer-facing route does work before it knows the caller.**
- Gate B1981 item 5: any request with a well-formed serial "reads the secret store before it is refused ... the host adds no rate limit". On a site network that is modest. In Azure (F5) the listener's exposure is whatever N-5 turns out to be. Add a limit per source and per serial before the first non-lab deployment; decide it with N-5.

**F19. The first run is on the product owner's own home printer and network.**
- The approved list switches on HP's Test service (HP: never on in production; it switches itself off at reboot, B1968 premise 8), adds a development CA to the printer's trust store, opens a port on the Mac for the printer's call-backs, and keeps the admin password in a plain credentials file. Each is reasonable for a lab. Together they need an explicit end-of-session undo list (CA deleted, button and agent unregistered, Test service off, firewall rule closed) and a check that the run folders, which hold the printer's answers, stay out of git. B1968 gives the undo per step; nobody yet owns "confirm all undone".

**Also for the record (not new findings):** the licence clause R32 now sits under the project's only testable path (F10); the panel-page binding R23 is unproven and S2 is where it is measured (F4); C-63's revisit trigger needs re-pointing (F8).

---

## 5. For the kick-off

**Ten points for the team (plain words):**
1. We are building one server that makes HP printers without Workpath behave like the Workpath suite: card sign-in, scan and print to Microsoft 365, Universal Print. Printers show pages from the server; the server does the work.
2. There are two kinds of target printer. Newer ones (FutureSmart 6) speak a new HP interface. Older ones (FutureSmart 4.7 to 5) speak an older one. We agreed to support both.
3. The test printer we have, an M577, is an older one. HP's firmware notes for it stop at FutureSmart 5. It cannot run the newer interface, and it needs no wipe.
4. So the first real proof will be on the older interface. That is a change of order, not of design.
5. In four days agents have built and reviewed the server's building blocks: 37 merged changes, about 1,800 automated tests. None of it has touched a real printer yet. Expect corrections when it does.
6. The first connection to the M577 is approved and starts read-only. Every later step can be undone. Agents drive it from the Mac; a person is needed only for card taps, the phone, and power.
7. The biggest open risk on older printers is the Microsoft sign-in screen. Their panel browser is old and small. Another HP partner failed to show Microsoft's page on it. We test this first.
8. The newer printers need something from us and something from HP: a FutureSmart 6 printer or HP's simulator to test on, and four things from HP (production firmware, an accepted platform version, working signing, a turnaround time), none of which has a date.
9. The server is planned to run in each customer's own Azure. Older printers must be reachable from the server on a fixed port with no address translation. How a site connects to Azure for that is not yet decided.
10. What we need from the team: a FutureSmart 6 printer from the lab, card readers, a test Microsoft tenant with a test user, and someone who can answer HP licence questions.

**Five questions for the product owner, each with a default:**

| # | Question | Default if not answered |
|---|---|---|
| 1 | On older printers, must Microsoft's number step also be on the printer panel? (N-1) | We test it on the M577 first and bring you the result with options. Nothing of a phone route is built meanwhile. |
| 2 | How will a printer at a site reach the server in the client's Azure, and may we create one small Azure test resource to measure it? (N-5, S14) | No Azure resource is created. The lab stays on one local network. The code stays neutral about hosting. |
| 3 | For older printers, do we use HP's own library to talk to the printer, or our own code written from HP's published service files? And will you send HP the licence question (H6)? | Our own code, for lab reads only. Nothing ships on it. The product adapter waits for your answer or HP's. |
| 4 | Do you agree the older-printer slice leads on real hardware, with the newer-printer work continuing on stand-ins until a FutureSmart 6 printer or the simulator is here? Who brings that printer, and when? | Yes: older-printer first. Newer-printer work continues unproven; no date is given for it. |
| 5 | Do your words "hp files have been provided to us. we can store them where we want" also cover HP's older-printer service files now in the repository? | Yes, as the coordinator read it and told you. Say if not, and they move out. |

Checked before listing as undecided: `CL` searched for N-5 (0), "FutureSmart 5" (0), OXPdLibCore / CoreWCF / hand-written (0), N-1 (1, listed as open), "reverse" (6, all recording the clause as unsettled or his notes on HP access); today's rulings (9 rows) hold the 11:08 route ruling and nothing on these five. Positive controls: C-63 (1), OQ-6 (3).

---

## UNMEASURED

- Anything on a printer, a simulator or a tenant. Every behaviour statement comes from HP's documents, the analysis reports or the code.
- The M577's actual firmware level, its panel browser engine, whether it resolves local host names, and which certificate it presents on each port.
- Which addressing version and which endpoint path an older printer accepts (F11; adapter README:56-63).
- Whether the three other certificate-pin copies share the chain-download gap gate B1979 found in one (F13). I listed the call sites; I did not read each chain policy.
- A build or test run of main. I read the snapshot; I ran nothing. Test and change counts in kick-off point 5 are RELAYED from B1969 (1,809 tests at pull request 32) and the commission (37 pull requests).
- HP's SDK guide and its licence text (read through `C1:316` and the kit's quotation only).
- The analysis reports beyond the lines cited (C1:78, C1:93, C1:316, C1:440, C1:525). Sections of `02` not read in full: 3 (requirements), 5.6, 7, 8.1, 8.2, 8.4 to 8.7, 11. Sections of `03` not read in full: 4 (work-package table, except rows WP0.1, WP0.2, WP0.4, WP2.1 to WP2.4), 5, 8.1 to 8.4. `05`: the open-question lists (lines 53 to 216) were not read line by line; `04` and the two WP0.x drafts were not opened. A point I call undecided could be answered in one of those; the `CL` searches above are the check I ran.
- Gate verdicts: heads and numbered findings of all eight were read; B1981, B1979 and B1980 in the cited parts. Not every line.
- The deviation register was searched, not read whole.
- Sizes, effort and dates: none estimated.

---

## PROPOSED AMENDMENTS (none applied)

| # | Where | Old text | New text | Reason |
|---|---|---|---|---|
| A1 | `05:245`, last sentence | "Which OXPd generation an M577 belongs to is still not established (C-39)." | "The M577 is an older-generation (OXPd 1.x) printer: HP's firmware readme for it lists FutureSmart 5 only, newest 5.10.0.7 (B1968). It needs no wipe and no developer mode. Its own firmware level is read at first contact." | F2 |
| A2 | `05:290` | "Nothing is established about the M577 beyond the model name you gave." | "Established 2026-11-23 (B1968, from HP's firmware readme): the M577 is FutureSmart 5, OXPd 1.x. Not yet read from the device: its firmware level." | F2 |
| A3 | `03:42` | "which OXPd generation an M577 covers is not established: no source was opened for it" | "the M577 is OXPd 1.x / FutureSmart 5 by HP's firmware readme (B1968, 2026-11-23); it fills the FutureSmart 5 item of this list and not the OXPd 2 item" | F2 |
| A4 | `05:220`, from "Needs:" to the end of the item | "Needs: the printer wiped into developer mode (P2, C-47), your HP access for the service key (C-50), a test tenant user with Authenticator. Caveat: ... the Chromium test waits for a FutureSmart 6 printer from the lab (A23)." | "On the M577 (OXPd 1.x) this test runs on the older WebKit panel and answers N-1; it needs no wipe, the printer's admin password and a test tenant user with Authenticator. The Chromium 87 test (S4) waits for a FutureSmart 6 printer or the simulator." | F1, F2 |
| A5 | `02:429` | "| OXPd 1.x | M1 or M2 | M5 | M1 or M2 | M3 (+ M1/M2) | M1 |" | "| OXPd 1.x | open (N-1): M4 if the older-panel test passes; M1 or M2 only if the product owner keeps them (N-3) | M5 | as the first column | M3 (+ the first column's method) | open (N-3) |" | F1: the row contradicts D10 and N-1 |
| A6 | `03:443`, N-1 default | "Same target on both; built on the OXPd 2 page first; nothing of the phone route built for 1.x before the 1.x panel test reports" | "Same target on both; the 1.x panel test runs first, on the M577, because it is the device in hand; nothing of the phone route is built for 1.x before that test reports" | F1, F3 |
| A7 | `03:264`, after "phase 2 can start alone." | (add) | "Since 2026-11-23 this is the working order: the only device in hand is OXPd 1.x, so the phase 2 slice leads on real hardware and spike S2 runs first; phase 1 continues against stubs until an OXPd 2 device or the simulator exists." | F3, F4 |
| A8 | `03:55`, S2 row, pass condition | (add) | "Also needed and recorded: a server host name the device resolves and a certificate whose CN is that name (no IP address, `[C1 §4.2]`); which WS-Addressing version the device accepts in each direction." | F7, F11 |
| A9 | `02:363` (C3) | "SOAP client to device services on 7627 (OXPdLib .NET 8 build, client side)" | "SOAP client to device services on 7627. Two candidates, not yet decided: HP's OXPdLib (.NET 8 build), or Datasec's own client written from HP's service descriptions (the lab read client of 2026-11-23 is the second kind). The choice bears on R32 and on reading the DiscoveryTree, which HP says is done through its library." | F10 |
| A10 | `02:958` (R16) | "OXPdLib 1.x redistributed unchanged" | "OXPdLib 1.x redistributed unchanged if it is used; whether it is used is open (C3)" | F10 |
| A11 | `02:249` | "SOAP 1.2 + WS-Addressing 2004, both directions [C1 §4.1]" | "SOAP 1.2 with WS-Addressing, both directions; HP's prose specification says the August 2004 version [C1 §4.1], HP's service description files use version 1.0 (2005/08); which a device accepts is UNMEASURED until the first connection" | F11 |
| A12 | `02:585` | "B3: Suite Server (customer LAN)" | "B3: Suite Server (client's Azure in Phase 1, path to the site open: N-5; customer LAN in Phase 2)" | F5 |
| A13 | `02:605`, after "never accept-all." | (add) | "One component owns this for every caller (adapters, IPP, lab tool): the check, the chain policy, the fingerprint stored on the device record, the change alert, and the per-device admin-password attempt counter." | F13, F16 |
| A14 | `02:603`, after the first sentence | (add) | "The credential's issue, storage and check are one shared component with the scheme (bearer or Basic) as a setting; neither adapter owns it." | F12 |
| A15 | Deviation register, new row | (none) | "The OXPd 1.x device client is Datasec's own, not HP's OXPdLib (differs from `02` C3 and R16). Class U until decided. Decided by: the coordinator, for the lab read client only (kit B1976)." | F10 |
| A16 | `CL`, a coordinator's note (no word of his changed) | (none) | "C-63's revisit point, 'after Monday's printer test shows real traffic', cannot be met by the M577: it is an OXPd 1.x printer and C-63 concerns OXPd 2 answers. The revisit moves to the first OXPd 2 device or simulator run." | F8 |
