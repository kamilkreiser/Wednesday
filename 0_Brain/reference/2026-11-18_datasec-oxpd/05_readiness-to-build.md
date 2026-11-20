# Datasec OXPd: are we ready to build?

Datasec / OXPd, 2026-11-20. For the product owner. Written after the independent review of the architecture (`02_architecture.md`) and the plan (`03_plan-of-attack-and-build.md`) was applied to both. No secret value appears here. **Updated on 2026-11-20, afternoon (B1765)**, after your answers of that day (C-38 to C-44) and after the two reports on what you sent (A9: the sign-in gateway and the Azure offers; A10: the earlier OXPd 1 work). Where your reading matter changed, the earlier text is kept below the new text and marked. Report lines are cited as "report A9 line n". **Updated again on 2026-11-20, evening (B1773)**, after the OneDrive app's code was read (report A11) and that reading was checked by a second reader (`review/B1769_A11_SECOND-READ.md`, cited as "the second read"). Additions are marked "B1773"; nothing of the earlier text was removed.

## BLUF

1. **Phase 0 has started, on the work that needs no hardware.** You gave the word on 2026-11-20 (C-42). The project folder is `OXPd_2` and the repository is `datasecau/OXPd_2`. Agents are starting the work packages that need no printer, no tenant and no answer (list below). The limits are the ones on the card you tapped: nothing goes to HP or to any person, no Azure, no spend.
2. **What still waits is unchanged:**
   - **The kit set-up.** You said all the kit is in hand and not configured. Setting it up runs alongside the build: by Tuesday where a seat can reach it, by step-by-step guidance to you where it needs your hands. Which of the 17 items you hold is being asked item by item.
   - **The thirteen tests on real printers and a real tenant.** Nothing has been run on a printer, a simulator or a tenant yet.
   - **HP's four undated items** for the newer printers (item 6 below).
3. **What you sent today, and what it showed:**
   - **The sign-in gateway's code is in and read.** It is small (three functions). The server can join it as designed. Two things are different from what the documents assumed: the gateway does not check who sends an unlock message (question 10 now has its fact; the decision is still yours), and adding the phone-link relay to it is a new version of the Azure offer for each customer, not one added endpoint.
   - **The earlier OXPd 1 repository is the same tree we had already analysed, byte for byte**, and the repository `OXPD1` is empty. Nothing new arrived for the older printers.
   - **A deployable licence server already exists** as a second Azure offer. The design still uses Datasec's own licence service; who is meant to deploy that offer is a new point for you.
4. **Your rulings of today, applied:** sensitivity labels are left out, as today (C-38). Deployment uses Datasec's existing HPK Deployment Utility, amended, and no new installer is built (C-43): the utility is the operator's tool, and the server does the work on each printer because it must keep what that work produces. Of fifteen deployment steps the utility carries two as it is and two more in part, six need new code in it, four it cannot carry (installing the server itself, the server's first-run set-up, the repair loop, registering Universal Print printers), and one is split between the two. Detail: `02_architecture.md` section 8.7.
5. **Where the lists live** (C-41): every question and point to clarify is on one master list, Jira `OXPD2-1`; the kit checklist is Jira `OXPD2-2`. Eighteen points were added today (OP-1 to OP-18, after question 15 below), each on a default.
6. **One thing to know before you commit a date to anyone** (unchanged): the newer printers (OXPd 2) cannot reach a customer until HP delivers four things, and HP has given a date for none of them: production firmware, a platform version its validation accepts, a signing service whose output installs, and its turnaround. The older printers (OXPd 1.x) have no such dependency on HP.
7. **Added 2026-11-20, evening (B1773): the OneDrive app's code has been read, and the reading checked by a second reader.**
   - **The OneDrive app is bigger than the documents said.** It has four places, not one: My Drive, Recent, Shared with me, and Shared libraries (SharePoint sites and libraries reached from the OneDrive tile). The documents described My Drive only, because they rested on the manual. Under your "full match of everything" answer (C-16) the rebuild carries all four. That is your ruling applied, not a new question to you. It makes the OneDrive work package larger; it has not been re-sized yet.
   - **Mailflow quick messages are switched off in the code and in the compiled app** (the same switch as SharePoint quick access). The design leaves them out, as question 3's default gives; say if you want a look on a printer first.
   - **Three points were added** (OP-19 to OP-21 below), each on a default. Two of the three need a printer or a test tenant, not a decision.
   - **One licence point about HP's older SDK is recorded as not settled.** It is point 6 of the draft message H6 to HP (`registers/HP_QUESTIONS_DRAFT.md`), which is yours to send or not. The design is unchanged meanwhile.
   - Nothing in this update changes what waits (item 2) or the caution about dates (item 6).

### The BLUF as it stood before your answers of 2026-11-20 (kept for the record; superseded by the six items above)

1. **Not yet, and the gap is short and known.** The design and the plan have now been reviewed line by line against the source code, HP's documents and your 25 answers. 92 corrections were raised and every one is dealt with. None overturns the approach: one server on the customer's network, serving both printer generations, beside Workpath.
2. **Three things stand between here and a start:**
   - **Your word to start building.** Everything so far was analysis and design. Building is a new ask.
   - **The phase-0 kit** (list below): printers, a Windows PC, card readers, a test Microsoft tenant, HP developer access, and two pieces of source code that are not in the library.
   - **Two answers that the first weeks depend on:** whether the card key found in the library is the one live printers use today (question 8), and where the SharePoint app's source is (question 7). The other thirteen questions block nothing in phase 0, and each has a default the design uses meanwhile.
   - **Update, later on 2026-11-20:** you sent the SharePoint source and it has been read (question 7 below). That answer is in. The source of the sign-in gateway, asked for in the same message, is still needed: you asked what was meant, and the question has been put to you again. Of the "two pieces of source code" in the kit line above, one is now in hand.
3. **The first step is not product code.** It is phase 0: a lab, and thirteen short tests on real printers and a real tenant that prove the assumptions the design rests on. Some unit-level work needs no hardware and can start the day you say go (list below).
4. **One thing to know before you commit a date to anyone:** the newer printers (OXPd 2) cannot reach a customer until HP delivers four things, and HP has given a date for none of them: production firmware, a platform version its validation accepts, a signing service whose output installs, and its turnaround. The older printers (OXPd 1.x) have no such dependency on HP.

## What the review changed (ten lines)

1. The newer-printer adapter no longer ships HP's beta library; it uses our own clients built from HP's published specifications, as your answer on HP code rights requires.
2. Three of your answers had been applied more widely than the option you tapped (stored admin passwords on newer printers, one central server for several sites, all six card readers). The documents now follow the option text, and the wider reading is an open question.
3. The parity list was incomplete: 18 of the 90 documented behaviours were cited nowhere, and features that only the code shows (Teams quick access, Mailflow filters, print preview, finishing options and others) had no requirement. 22 requirement rows were added, each with a work package and a test.
4. "OneDrive personal" is not a shipped product as far as the library shows, and the SharePoint app's source is not in the library. Both are now open questions instead of assumptions.
5. The phase order was wrong in places: some tests depended on parts built later. Fixed, and a small admin interface moves into phase 1.
6. The install steps for newer printers were in an order that cannot work with a customer's own certificate authority. Reordered.
7. The parity gate could not be passed as written. It now names exactly which differences from Workpath are allowed and under which of your answers.
8. The two-server (high availability) option contradicted the key storage design and had no build work. Both fixed; it must be proven by a test.
9. Security: the card key is also the phone-app QR key; a session reference would have leaked into job records on newer printers (removed); several protections are now marked "unproven until tested" instead of asserted.
10. Phase 0 grew from eight tests to thirteen, and its shopping list gained the HP items the first draft missed.

## OPEN QUESTIONS FOR THE PRODUCT OWNER

Fifteen. Each is one decision. "Default" is what the design does until you answer. "Blocks" is the first phase that cannot finish without the answer. **Update 2026-11-20:** question 7 is now answered in full, so fourteen are open; you accepted their defaults for now (C-32). Questions 10 and 13 have new facts. Eighteen further points (OP-1 to OP-18) were added today and follow question 15. All of them are kept on the master list, Jira `OXPD2-1`.

**1. What does "Yes, HP confirmed" cover?**
Options: (a) HP's position only: the approach is acceptable; (b) also a signing route and a date.
Recommendation: (a) unless you hold something from HP in writing that says more. Default: (a).
Blocks: nothing in phase 0. It decides how much weight to put on a release date for the newer printers.

**2. May the server keep a stored, encrypted copy of a newer printer's admin password?**
Your answer said "Store it encrypted", and the option's own text said older printers keep it and "newer ones discard it".
Options: (a) never stored on newer printers; (b) stored as a per-site choice, off by default.
Recommendation: wait for the phase-0 test. If a newer printer loses its access token on reboot, (a) means a person must re-enter the password at the server for each printer after each reboot, and (b) becomes the practical choice. Default: (a).
Blocks: nothing until that test reports; then phase 5 (fleet onboarding and repair).

**3. Does "Full match of everything" mean everything Workpath ships today, and no more?**
Options: (a) yes; (b) it also includes things Workpath could do but does not ship.
Recommendation: (a). Default: (a).
Blocks: the phase 3 exit (the parity gate). Questions 4, 5 and 6 are the cases where it bites.
**Added 2026-11-20 (B1773), one more named case:** Mailflow quick messages. The code offers them only behind a switch that returns "off" in the source and in the compiled library the app is built with, and nothing can turn it on (second read, section 2). Under default (a) they are left out. The evidence is the code and the compiled file, not a printer: if you want a look on a Workpath printer before they are dropped, say so.

**4. Is OneDrive personal (consumer accounts) in release 1?**
The code has a build flavour for it, but the release pipeline builds the business app only and the consumer sign-in is switched off in the code.
Options: (a) out: it is not a shipped product; (b) in: it is sold or wanted.
Recommendation: (a). Default: (a).
Blocks: phase 3 (one work package). It also sets the tile list frozen into the HP-signed bundle, so answer before the first submission to HP.
**Added 2026-11-20 (B1773):** the read of the OneDrive code adds evidence and no new question: the personal variant differs from the business one in two places of the code only, has no way to sign in, and is not packaged (report A11 rows 64 to 66; second read, section 7). Recommendation and default unchanged.

**5. Is HP Authentication Manager's role as the sign-in for HP Advance and LRS VPSX in release 1?**
The product documents it today. Your answers pull two ways: "full match" would include it; "ours only, no other vendor's print solution on the printer" would exclude it.
Options: (a) out; (b) in, which is new design and build work.
Recommendation: (a), unless a customer you intend to sell to uses it. Default: (a).
Blocks: the phase 3 exit and the release gate.

**6. Do you approve the design choices that differ from Workpath and that neither your answers nor the platform force?**
Today: card emulation and app settings move from the printer panel to the server console; job counts are reported to Universal Print for all three printer types (Workpath does Secure only); the server may write a refreshed sign-in token back to the directory in No-MFA mode; the help link on error screens may be shown rather than opened.
Options: approve the list; or strike items, which then follow Workpath exactly.
Recommendation: approve, except the token write-back, which should wait for its phase-0 test. Default: as designed, pending your approval.
Blocks: the phase 3 exit.

**7. Where is the source code that builds the SharePoint app?**
**Answered in part on 2026-11-20.** **Answered in full later the same day (C-40): the gateway source arrived and has been read.**
- **Answered:** you supplied the SharePoint source (the repository `CypherSharePoint-main`, version 4.4.6) and a newer copy of the shared library. Both have been read. SharePoint is a separate app with its own code, not a variant of OneDrive. The design and the plan now follow the code: seven requirement rows were added, and two points where the manual and the code disagree were corrected (the code has no limit of four metadata fields at scan, and the app ships in eight languages, not six). Detail: `analysis/A8_sharepoint-app-and-common-library.md` and `review/B1760_APPLIED.md`.
- **Still open:** the source of the sign-in gateway (the Function App in the customer's Azure that the phone app talks to). You asked what was meant by "gateway"; the question has been asked again and is not answered. Nothing you sent is the gateway. **Update, later on 2026-11-20 (this replaces the "Still open" point): received on 2026-11-20 (C-40) and read (report A9).** The gateway is the repository `hpam-api`, a three-function relay in front of Azure SignalR, deployed by the `hpam-marketplace` offer (report A9 lines 11, 234).
- **Found in the SharePoint code and yours to decide, not yet asked as a numbered question:** sensitivity labels (choose a label when scanning, block printing of a "Do Not Print" label) are written and switched off. The design leaves them out unless you say they ship. **Ruled on 2026-11-20 (C-38): "Leave it out, as today".** Sensitivity labels are not in the rebuild; the feature is listed as a possible later addition.

What the question said before the answer, kept for the record:
The suite ships SharePoint as its own app. Nothing in the library builds it.
Options: (a) supply the repository or branch; (b) confirm it is built from the OneDrive code at another revision, and which.
Recommendation: ask the Workpath team this week. Default: SharePoint is built from the manual alone, and its match with Workpath is unverified at source.
Blocks: part of phase 0 (the source read), then phase 3. (No longer blocks either: the source is in and read. The gateway source blocks the phone sign-in work of phase 3, as question 10 says.) (Update, later on 2026-11-20: the gateway source is in and read; what still gates the phone sign-in work is your answer to question 10 and a capture of the phone app's message.)

**8. Is the card key in the library the one fielded printers and phone apps use today?**
You said the keys in the library are old and rotated. That sentence was general. This key is compiled into the 4.4.1 source the shipped apps are built from, every stored card and every installed phone app depends on it, and it cannot be rotated without re-enrolling cards and releasing the phone app. Location: `HPAuthenticationManager-main`, files `util/CardValidator.kt` line 10 and `util/Encryptor.kt` line 12 (the same value in both).
Options: (a) yes, it is live; (b) no, production builds get a different key, and here is how.
Recommendation: answer first. If (a), a live key sits in the library, in its backup copy and in every app package, and that is recorded as an accepted weakness carried over by your "full sharing" answer. Default: treated as live; never copied or printed.
Blocks: phase 0 (the key must reach the lab through a secure channel) and phase 1 (shared card sign-in).

**9. May the server register printers under Datasec's own Universal Print app registration?**
The design assumed yes and had marked it as ruled. Your Universal Print answer does not cover it.
Options: (a) yes, Datasec's registration; (b) each customer registers their own.
Recommendation: (a) if Datasec owns that registration and can add what the server needs; the team can check without a customer. Default: assumed (a); nothing is built on it before you answer.
Blocks: phase 4 (Universal Print) and one phase-0 test.

**10. The customer's sign-in gateway does not check who sends an unlock message. Is QR sign-in without MFA offered on OXPd printers?**
**Updated 2026-11-20: the gateway's code has been read (report A9).** It does not check who sends an unlock message or whose e-mail the message names, and whoever may send may also listen: every message goes to every connection (report A9 lines 240, 241). In No-MFA mode a QR message is a full credential. The gateway is the one Workpath printers and the phone app use today (report A9 line 23): the weakness is in the existing gateway, not something the OXPd server adds.
How bad it is, with its limits: two links between that fact and a real attack are inferred and have NOT been tested. (1) That an ordinary user of the customer's tenant can obtain the token the gateway asks for. (2) That the per-user secret in the message is the same from one sign-in to the next. If both hold, a user of the tenant could listen, collect other users' e-mail and secret pairs, and replay one at a printer, which without MFA is a sign-in as that user. With MFA, the second step you already ruled (phone code or phone link, C-29) bounds it (report A9 line 261). Both links are tested in the test tenant in phase 0.
Options (unchanged): (a) offer it as Workpath does, risk recorded; (b) switch it off on OXPd until the gateway is fixed, which your "may change" answer permits.
Recommendation: (b). The condition the earlier recommendation named is met, as far as reading the code can show. If the two tests show that an ordinary user cannot get the token, the case for (b) weakens and this comes back to you with the result.
Default until you rule: (a), as Workpath, with the risk recorded. That is the default, not a decision: it is what your "full match" and "as is, off by default" answers give until you say otherwise, and nothing of QR sign-in is built before phase 3.
Blocks: phase 3 (QR sign-in). It no longer needs the gateway source.

What the question said before the gateway was read, kept for the record:
If the customer's sign-in gateway does not check who sends an unlock message, is QR sign-in without MFA offered on OXPd printers?
Nobody has read the gateway's code (it is not in the library). In No-MFA mode a QR message is a full credential.
Options: (a) offer it as Workpath does, risk recorded; (b) switch it off on OXPd until the gateway is fixed, which your "may change" answer permits.
Recommendation: decide once the gateway source has been read; if it does not check the sender, (b). Default: (a), as Workpath.
Blocks: phase 3 (QR sign-in). Needs the gateway source first.

**11. Is one central server for several sites to be offered?**
You chose "one server per site". The option you did not choose was one per company account.
Options: (a) no; (b) yes, where the network between sites is flat.
Recommendation: (a) for release 1. Default: (a).
Blocks: nothing.

**12. Has HP given Datasec anything newer than OXPd 1.8.4.1?**
Your brief said "whatever the latest version is". The library's latest is 1.8.4.1; HP called 1.9 "soon to be released" in March 2026.
Options: (a) no, build on 1.8.4.1; (b) yes, and here it is.
Recommendation: ask your HP contact. Default: (a).
Blocks: nothing unless the answer is (b), then the phase 2 start.

**13. Must a site with no internet at all be supported?**
The licence check needs Datasec's licence service. Without it a server runs for 20 days. **Update 2026-11-20:** a deployable licence server already exists as a second Azure Marketplace offer (report A9 line 246), so option (b) would not be new build work from nothing. How much work it would be is not measured (that server's source was not sent), and who is meant to deploy the offer is a new point for you (OP-7 below). The recommendation and the default are unchanged.
Options: (a) no; (b) yes, which means a customer-hosted licence service.
Recommendation: (a) for release 1. Default: (a).
Blocks: nothing before phase 5.

**14. What defect level ends the four-week pilot successfully?**
The plan said "the agreed threshold". None is agreed.
Recommendation: set it when the pilot site is chosen. Default: none.
Blocks: phase 6 (the pilot).

**15. Your brief says "integration into intra-environments". Is that "Entra environments"?**
Options: (a) yes; (b) it meant the customer's intranet as well.
Recommendation: (a). The one intranet item that reading would add, an outbound web proxy, is now in the design either way. Default: (a).
Blocks: nothing.

## OPEN POINTS ADDED ON 2026-11-20 (OP-1 to OP-18)

Found while applying your answers of today and the two reports. Each is yours to decide or to say; none was decided for you. "Default" is what the design does meanwhile. They are on the master list, Jira `OXPD2-1`. The first six come from your ruling on the deployment utility (C-43).

| # | Point | Default | Blocks |
|---|---|---|---|
| OP-1 | Is the amended HPK Deployment Utility the operator's tool that starts and follows jobs the server carries out, or must the utility do the work on each printer itself, without the server? | The first. The server must keep each printer's token, records and repair loop, which a desktop tool that is closed after the job cannot | The utility's amendment (phase 5) |
| OP-2 | Does "use the deployment utility" also cover installing the server itself? | No. The server keeps its two packagings (your "both equally" answer); the utility has no code that installs software on a machine | Phase 5 |
| OP-3 | The utility runs on Windows only. Is a Windows PC for it acceptable at a site that takes the Linux packaging of the server? | Yes, as for Workpath roll-outs today | Phase 5 |
| OP-4 | Does the server's console also keep its own onboarding pages, or is the utility the only place a batch is started? | The utility only; the console shows status and repairs one printer | Phase 5 |
| OP-5 | Where does the amended utility live, and how is it released? Today a push to its main branch publishes a release | On a branch of its own repository; nothing reaches its main branch without your word | The utility's amendment |
| OP-6 | May the amendment also change how the utility stores and passes the printer password for existing Workpath jobs, or is only the OXPd path to be done properly? | OXPd path only; Workpath jobs behave exactly as today | The utility's amendment |
| OP-7 | Who is meant to deploy the licence-server Azure offer: Datasec only, or partners and customers too? | Datasec only | Nothing before phase 5; bears on question 13 |
| OP-8 | How many customers deployed the Azure side by the script, and how many by the Marketplace offer? | Both exist: every gateway change ships both ways | Phase 3 (the relay) |
| OP-9 | Is `v1.3.0` the gateway package live in the Marketplace today? | Yes | Phase 3 (the relay) |
| OP-10 | Can the source of the phone app (HP Secure Authentication) be supplied, or may one sign-in message be captured in the test tenant? | Capture it in the test tenant | Phase 3 (QR sign-in) |
| OP-11 | Is `cc-api`, which was not among the repositories, the API of the older Keycloak back end, and so not needed? | Yes: not needed, not asked for again | Nothing |
| OP-12 | The phone-link relay needs one address on each customer's gateway that accepts a request without a token, and a second update route for customers who deployed by script. Go ahead on that basis? | Yes, under your "may change" answer, with the test described in the plan | Phase 3 (the relay) |
| OP-13 | Is there more of the earlier OXPd 1 work than what you sent: another branch, a later working copy, the repository's history? | No: what you sent is the last state | Nothing |
| OP-14 | That tree's README gives a printer administrator password as the "default", beside a lab address. Is it a live password of a lab printer? | Treated as live: never copied; whoever owns that printer should change it | Nothing |
| OP-15 | Was that code ever run against a physical printer, and what was the "emulator" its author names? | Emulator only; nothing is treated as proven on hardware | Nothing |
| OP-16 | Where did the two card keys written into that earlier build come from? They are not today's Workpath card key | Made up or outdated; never carried into the product | Nothing |
| OP-17 | May that earlier build's register and unregister tools be used once as a lab probe against the test printer? They switch certificate checks off | No: the phase-0 tests are written fresh | Nothing |
| OP-18 | The repository `OXPD1` is empty. Is it meant to receive anything? | Ignored: new work goes to `datasecau/OXPd_2` | Nothing |
| OP-19 | **Added 2026-11-20, evening (B1773).** A SharePoint library can be opened from two tiles: SharePoint, and OneDrive's "Shared libraries". Today the two apps behave differently when you scan into the same library: the SharePoint app asks for the library's fields at scan, the OneDrive app does not. Does each tile keep its own behaviour of today? | Yes: each tile matches its own Workpath app exactly, as "full match" gives | Phase 3 (the OneDrive work package) |
| OP-20 | **Added (B1773). A test, not a decision.** Do the Microsoft permissions a customer has granted cover OneDrive's "Shared with me", where files sit in other users' drives? The code names no permission for it | The permission list is unchanged and nothing is removed from it; the consent text is not changed; a test on the test tenant decides | Phase 3 (Shared with me); needs the test tenant (kit item 11) |
| OP-21 | **Added (B1773).** Do the OneDrive and SharePoint apps on a printer today show their seven translations, or English only? The code holds eight languages, but one line of the build may strip all but English from the shipped app; it was not tested | Build all eight languages as the code has them; confirm on a Workpath printer when one is at hand | Nothing before the language work finishes; needs a Workpath printer (kit item 9) |

## PHASE 0 NEEDS

| # | Item | Who supplies it |
|---|---|---|
| 1 | Your word to start building, and with it a project folder, a repository under Datasec's GitHub organisation and a build pipeline. **Given on 2026-11-20 (C-42), for the no-hardware work:** folder `OXPd_2`, repository `datasecau/OXPd_2`; the build pipeline is work package WP0.3, part of the work now started | You |
| 2 | A Windows x86-64 PC on a wired network, with VMware, nested virtualisation on, Hyper-V off and WSL 1. It must be Windows: the older-printer simulator needs Windows and IIS. HP suggests a second machine (or a Linux build server) for the bundle-packaging tool | You or the team |
| 3 | The newer-printer simulator image (`HPExtSim_6.38.0.793.ova`, not yet downloaded) and the HP Extensibility Simulator Guide (the download was refused for your account) | HP portal, through your HP contact |
| 4 | One newer printer: FutureSmart 6, firmware 6.38.0.793 or later, that may be put into developer mode. Not a pilot unit: switching that mode wipes it. It needs admin access, outbound internet to HP, and a person at its panel | You or the team |
| 5 | An HP developer account with an "LDB Service Key" (without it the printer in item 4 cannot be put into developer mode) | You, from HP's developer site |
| 6 | The FutureSmart 6 pilot firmware, and the route by which Datasec gets it | HP |
| 7 | One FutureSmart 5 printer without Workpath apps (5.8 or later preferred) | You or the team |
| 8 | One FutureSmart 4.7 printer. Without it the lowest supported firmware ships as "expected, untested" | You or the team |
| 9 | One Workpath printer with the current suite, in the test tenant | The team |
| 10 | Card readers: one of each of the eight products in the product's reader table. The six USB ids are not six readers: four products share one id | You or the team |
| 11 | A test Microsoft tenant with: Custom Security Attributes licensed; the HP Authentication Manager registration set up as customers have it; Universal Print licences; the "Onboarding Azure Services" deployment; a Printer Administrator test account with MFA; a test user whose mail address differs from the sign-in name; Conditional Access policies to test against; a tenant admin available for those tests | The team |
| 12 | The source code of the customer gateway (the Function App). It is in none of the library's repositories. **Still needed** (asked again on 2026-11-20). **Update: received 2026-11-20** (`hpam-api`, with `hpam-marketplace`; C-40) and read (report A9). Still wanted: the phone app's source, or leave to capture one sign-in message in the test tenant (OP-10) | The Workpath team |
| 13 | The source code that builds the SharePoint app (question 7). **Received 2026-11-20 and read** | Done |
| 14 | From HP, in writing: the confirmation you reported; App Center / validation access and the contact behind it; dates for the four items in the BLUF; and whether a first signing round is possible with fewer than seven tested printer groups | You and HP |
| 15 | The card key the fielded product uses, and the licence installation credentials, through a secure channel (after question 8) | You |
| 16 | Two Linux and two Windows server hosts (virtual machines will do) for the two-server test and the packaging tests | The team |
| 17 | A person with the printers: taps cards, signs in on a phone that has the HP Secure Authentication app, watches the panel, power-cycles | The team |

**State of the kit on 2026-11-20, as you stated it and no further** (the checklist itself is Jira `OXPD2-2`):
- **Item 1:** given (C-42), within its limits.
- **Printers (items 4, 7, 8):** you hold an HP MFP M577 (C-39; your note was read as "MFP M577", and its trailing letter is not understood). Its firmware version is not known. Whether it may be wiped for developer mode is not known. Which generation of OXPd an M577 runs has NOT been established: no source was opened for it. Until the firmware version is known, one printer of each generation is still to be confirmed.
- **All items:** you said all the kit is in hand and not configured (C-42). Which of the 17 items that covers is not in your note; it is being asked item by item on the master list, and nothing is assumed.
- **Items 12 and 13 (source code):** both received and read.
- **Not applied by this update:** your notes on a card reader, an old Windows PC, a Windows emulator and the Windows environment used by HPSM (C-35, C-36) bear on item 2; they are recorded in the numbered answers and were outside this pass.

Not phase 0, but it decides when the first submission to HP can happen: HP requires a test on at least one printer from each of seven groups for a product that signs users in. Phase 0 has one. No group will be declared tested when it was not.

## WHAT CAN START WITHOUT ANY OF THE ABOVE

These need no printer, no tenant and no answer. They still need item 1, your word. **Update 2026-11-20: you gave it (C-42), and this work is starting.** Rows marked "added" are new today. They are unit-level: their final tests need devices later.

| Work package | What can be done now |
|---|---|
| WP0.3 | Repository layout, Linux and Windows build legs, secret scanning, the check that fails a release containing HP's beta library. Added 2026-11-20 (C-43): the server's admin interface is kept as its own project, so the deployment utility can be built against it, and no installer screen for printers is built into the server |
| WP0.4 | Our own newer-printer clients and test stubs generated from HP's specifications; older-printer stubs from HP's published service descriptions. Added 2026-11-20: HP's older-printer library is taken from SDK 1.8.4.1 and identified by its checksum, because two different files carry the same name (report A10 lines 185-187); and a stand-in for the sign-in gateway, now that its three routes are known (report A9 lines 45-47). Added 2026-11-20, evening (B1773), a point that is not settled: HP's older SDK guide says licensed users may not use the library source "or any other means of reverse engineering" on the protocol between HP's library and a printer (report C1 line 316, which gives the guide's terms). This package builds the older-printer stubs from the service descriptions inside HP's library, and the product hosts the printer-facing endpoints on a framework HP does not demonstrate. Whether the two conflict has not been settled by anyone: it is a question for HP (point 6 of the draft message H6, yours to send or not) and possibly for someone qualified to read the licence. Until then the package is unchanged. This note does not say the plan is permitted or that it is not |
| WP0.5 | Drafting the questions to HP (sending them is yours) |
| WP0.6 | Reading the OneDrive source that is in the library (the SharePoint half was done on 2026-11-20, once item 13 arrived). **Done on 2026-11-20, evening (B1773):** the OneDrive code is read (report A11) and the reading was checked by a second reader. What is left of this package needs a real printer or a tenant, and nothing else. On a Workpath printer: the manual's "4 custom fields" in SharePoint 4.4.6; whether the OneDrive and SharePoint apps show their translations or English only (OP-21); the sign-out confirmation screen in OneDrive, which the code has and nobody has seen on a printer; and, only if you ask for it, a look for Mailflow quick messages. On the test tenant: whether the granted permissions cover "Shared with me" (OP-20), and how long the address of a file's thumbnail image stays valid. The printer look for SharePoint quick access and "remember me" is no longer needed: the compiled library the SharePoint app is built with has the switch off (second read, section 2) |
| WP1.1 | Device registry, database for both packagings, local secret store |
| WP1.3 | Card decoders written from the Workpath decoding code (the comparison with real readers waits for the lab) |
| WP1.4, WP1.5 | Sign-in state machine and token broker against a simulated Microsoft service |
| WP1.10 | Logging with the deny-list and its planted-marker test |
| WP3.8 | The shared Microsoft Graph layer with simulated throttling |
| WP3.12 | The six languages, seeded from the Workpath text resources. Added 2026-11-20 (B1773): eight for the OneDrive and SharePoint pages, as their code has them (OP-21) |
| WP4.1, WP4.2 (part) | The Universal Print protocol encoder, ported from the Workpath logic, with unit tests |
| WP6.7 | The deviation register: the list behind question 6, drafted for your approval |
| WP0.7 (added: the reading half) | Done on 2026-11-20 by report A9. Its other half needs the test tenant: a capture of the phone app's message and the two tests behind question 10 |
| WP0.8 (added: part) | Drafting the report-field map against the 17 and 3 columns the Azure offer accepts (report A9 line 244). The export from a real tenant waits for the tenant |
| WP0.10 (added, new: C-43) | The design note for amending the HPK Deployment Utility, and a check that the utility builds as it stands. It is not one of the twelve rows above that your word covered: say if it should wait |

## WHAT WAS NOT VERIFIED

- **Nothing has been run on a printer, a simulator or a tenant.** Every statement about how a printer behaves comes from HP's documents, the source code or forum history. That is what the thirteen phase-0 tests are for.
- **HP's written confirmation is not in the library.** The only evidence for it is your answer.
- **Sources that are not in the library**, so nothing about them could be checked: the customer gateway (Function App); the phone app; the SharePoint app (received and read on 2026-11-20: see the next point); the customer's Log Analytics rule that decides which report columns are accepted; the job-record field names (inside a compiled HP library); HP's simulator guide; Microsoft's documentation on deleting a cloud printer. **Update 2026-11-20:** two of these are now in hand and read, both in what you sent that day (report A9): the customer gateway (Function App), and the Log Analytics rule that decides which report columns are accepted (a given customer's live rule could still differ from the template: report A9 line 245). The phone app stays on this list. Also not sent: `cc-api`, and the source of the licence server. The repository `OXPd1_solution` sent on 2026-11-20 is the earlier OXPd 1 attempt already analysed (report A7), byte for byte, and the repository `OXPD1` is empty, so neither adds source (report A10 lines 29-31; C-40).
- **The SharePoint source was read, not run.** About 55 of its 220 source files were read; nothing was built and nothing was checked on a printer. The shared library the app is built with is a compiled file one to three versions older than the library source that was read. Three features in the code look switched off (quick access, "remember me", sensitivity labels); a look at a printer running SharePoint 4.4.6 would confirm it. **Update 2026-11-20, evening (B1773):** for quick access and "remember me" the compiled library the SharePoint app is built with was read as bytes, and the switch returns "off" there too (second read, section 2), so those two no longer rest on the source alone. Sensitivity labels are left out by your ruling (C-38).
- **The OneDrive source has not been read in full.** The original analysis never wrote that half; it is a phase-0 work package. **Update 2026-11-20, evening (B1773; this replaces the two sentences before):** the OneDrive code has been read (report A11) and the reading checked by a second reader. It was read, not run. Report A11 read about 40 of the app's source files whole or nearly and the three largest by parts (report A11 section 13); the second read counts 173 source files in the app (its section 3) and itself checked 25 of A11's 74 behaviour rows and 22 of the 28 Microsoft calls A11 lists in full (the second read counts 29 calls, one more than A11: 23 live and 6 dead or unreferenced). Nothing was built, nothing was checked on a printer, on a tenant or against Microsoft's documentation, so every statement about Microsoft permissions is unchecked. The settings inside each scan and print option (which resolutions, sizes and formats) were read by neither reader.
- **Claims resting on a report line only.** The reviewers traced most claims to the line of an analysis report and opened the library itself for a minority (about 15 of 63 on the printer platforms, about 30 of 144 on security). The corrections applied in this pass were each opened at the cited line; unchanged text was not re-traced.
- **The option text of your 25 answers** was read from the board's data file, not from the board export. The numbered record of your answers holds only the label you tapped; copying the full option text into that record is still to be done.
- **That the card key and the QR key are one value** was established by comparing the two without displaying them; this pass did not open those files again.
- **One piece of general knowledge, not from the library:** that a sign-in token obtained by the server may not work at a Workpath printer. A phase-0 test settles it.
- **Sizes of the new work packages and the scores of the nine new risks** are estimates made in this pass, not measured.
- **The library copy that was read** is the backup copy; it was not compared file by file with the original on the laptop drive. For the earlier OXPd 1 attempt the comparison has now been made against what you sent from the repository: identical, 73 files (report A10 lines 28-31).

- **Added 2026-11-20. The gateway and the Azure offers were read, not run.** Every statement about how they behave at run time (what the sign-in check in front of the gateway admits, how a message is addressed, how long a token lives) is a reading of code and configuration (report A9 line 344). The two links behind question 10 are inferred, not tested. The message the phone app sends is not in what you sent.
- **Added 2026-11-20. The HPK Deployment Utility was read in part and not built or run.** Report A5 read 21 of its files; this update read 16 small files and 460 of the 1,070 lines of its worker; the desktop screens (6,179 lines in 26 files) were not read. Whether it builds as it stands is not established. What HP's HPKTool can do to an OXPd printer is not established: its guide was not opened.
- **Added 2026-11-20. Nothing is established about the M577** beyond the model name you gave.
- **Added 2026-11-20. The repository `datasecau/OXPd_2` was not looked at by this update** (no network call was made); its state is as recorded in your numbered answers (C-37).
- **Added 2026-11-20, evening (B1773). Teams quick access is probably switched off too, and that is not proven.** The compiled library the Teams app is built with has the same switch off; whether every way into Teams quick access passes that switch was traced at 7 of 16 places (second read, section 2). The two Teams rows stay in the plan until the rest is read.
- **Added 2026-11-20, evening (B1773). Whether HP's reverse-engineering clause bears on the older-printer work is not settled** (WP0.4 above). HP's guide itself was not opened for this update; the clause is as report C1 gives it. The agreements Datasec has with HP were not seen.
- **Added 2026-11-20, evening (B1773). The new OneDrive rows are unsized.** The OneDrive work package was sized on the manual, for My Drive only; nobody has estimated the three further places.

Details of the update of 2026-11-20, evening (B1773): `review/B1773_APPLIED.md`, `analysis/A11_onedrive-business-app-source.md`, `review/B1769_A11_SECOND-READ.md`; the four places in `02_architecture.md` section 3.9; the plan's side in `03_plan-of-attack-and-build.md`, rows WP0.6 and WP3.10 and section 8.4.

Details of the update of 2026-11-20, afternoon: `review/B1765_APPLIED.md`, `analysis/A9_hpam-backend-gateway-and-infra.md`, `analysis/A10_oxpd1-solution-earlier-work.md`; the deployment utility in `02_architecture.md` section 8.7; the open points also in `03_plan-of-attack-and-build.md` section 8.4.

Details of the SharePoint update of 2026-11-20: `review/B1760_APPLIED.md` and `analysis/A8_sharepoint-app-and-common-library.md`.

Details: one row per review finding in `review/B1757_APPLIED.md`; the changes themselves in the change logs at the end of `02_architecture.md` and `03_plan-of-attack-and-build.md`.
