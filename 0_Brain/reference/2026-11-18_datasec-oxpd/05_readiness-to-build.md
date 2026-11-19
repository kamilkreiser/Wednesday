# Datasec OXPd: are we ready to build?

Datasec / OXPd, 2026-11-20. For the product owner. Written after the independent review of the architecture (`02_architecture.md`) and the plan (`03_plan-of-attack-and-build.md`) was applied to both. No secret value appears here.

## BLUF

1. **Not yet, and the gap is short and known.** The design and the plan have now been reviewed line by line against the source code, HP's documents and your 25 answers. 92 corrections were raised and every one is dealt with. None overturns the approach: one server on the customer's network, serving both printer generations, beside Workpath.
2. **Three things stand between here and a start:**
   - **Your word to start building.** Everything so far was analysis and design. Building is a new ask.
   - **The phase-0 kit** (list below): printers, a Windows PC, card readers, a test Microsoft tenant, HP developer access, and two pieces of source code that are not in the library.
   - **Two answers that the first weeks depend on:** whether the card key found in the library is the one live printers use today (question 8), and where the SharePoint app's source is (question 7). The other thirteen questions block nothing in phase 0, and each has a default the design uses meanwhile.
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

Fifteen. Each is one decision. "Default" is what the design does until you answer. "Blocks" is the first phase that cannot finish without the answer.

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

**4. Is OneDrive personal (consumer accounts) in release 1?**
The code has a build flavour for it, but the release pipeline builds the business app only and the consumer sign-in is switched off in the code.
Options: (a) out: it is not a shipped product; (b) in: it is sold or wanted.
Recommendation: (a). Default: (a).
Blocks: phase 3 (one work package). It also sets the tile list frozen into the HP-signed bundle, so answer before the first submission to HP.

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
The suite ships SharePoint as its own app. Nothing in the library builds it.
Options: (a) supply the repository or branch; (b) confirm it is built from the OneDrive code at another revision, and which.
Recommendation: ask the Workpath team this week. Default: SharePoint is built from the manual alone, and its match with Workpath is unverified at source.
Blocks: part of phase 0 (the source read), then phase 3.

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

**10. If the customer's sign-in gateway does not check who sends an unlock message, is QR sign-in without MFA offered on OXPd printers?**
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
The licence check needs Datasec's licence service. Without it a server runs for 20 days.
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

## PHASE 0 NEEDS

| # | Item | Who supplies it |
|---|---|---|
| 1 | Your word to start building, and with it a project folder, a repository under Datasec's GitHub organisation and a build pipeline | You |
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
| 12 | The source code of the customer gateway (the Function App). It is in none of the library's repositories | The Workpath team |
| 13 | The source code that builds the SharePoint app (question 7) | The Workpath team |
| 14 | From HP, in writing: the confirmation you reported; App Center / validation access and the contact behind it; dates for the four items in the BLUF; and whether a first signing round is possible with fewer than seven tested printer groups | You and HP |
| 15 | The card key the fielded product uses, and the licence installation credentials, through a secure channel (after question 8) | You |
| 16 | Two Linux and two Windows server hosts (virtual machines will do) for the two-server test and the packaging tests | The team |
| 17 | A person with the printers: taps cards, signs in on a phone that has the HP Secure Authentication app, watches the panel, power-cycles | The team |

Not phase 0, but it decides when the first submission to HP can happen: HP requires a test on at least one printer from each of seven groups for a product that signs users in. Phase 0 has one. No group will be declared tested when it was not.

## WHAT CAN START WITHOUT ANY OF THE ABOVE

These need no printer, no tenant and no answer. They still need item 1, your word. They are unit-level: their final tests need devices later.

| Work package | What can be done now |
|---|---|
| WP0.3 | Repository layout, Linux and Windows build legs, secret scanning, the check that fails a release containing HP's beta library |
| WP0.4 | Our own newer-printer clients and test stubs generated from HP's specifications; older-printer stubs from HP's published service descriptions |
| WP0.5 | Drafting the questions to HP (sending them is yours) |
| WP0.6 | Reading the OneDrive source that is in the library (the SharePoint half waits for item 13) |
| WP1.1 | Device registry, database for both packagings, local secret store |
| WP1.3 | Card decoders written from the Workpath decoding code (the comparison with real readers waits for the lab) |
| WP1.4, WP1.5 | Sign-in state machine and token broker against a simulated Microsoft service |
| WP1.10 | Logging with the deny-list and its planted-marker test |
| WP3.8 | The shared Microsoft Graph layer with simulated throttling |
| WP3.12 | The six languages, seeded from the Workpath text resources |
| WP4.1, WP4.2 (part) | The Universal Print protocol encoder, ported from the Workpath logic, with unit tests |
| WP6.7 | The deviation register: the list behind question 6, drafted for your approval |

## WHAT WAS NOT VERIFIED

- **Nothing has been run on a printer, a simulator or a tenant.** Every statement about how a printer behaves comes from HP's documents, the source code or forum history. That is what the thirteen phase-0 tests are for.
- **HP's written confirmation is not in the library.** The only evidence for it is your answer.
- **Sources that are not in the library**, so nothing about them could be checked: the customer gateway (Function App); the phone app; the SharePoint app; the customer's Log Analytics rule that decides which report columns are accepted; the job-record field names (inside a compiled HP library); HP's simulator guide; Microsoft's documentation on deleting a cloud printer.
- **The OneDrive source has not been read in full.** The original analysis never wrote that half; it is a phase-0 work package.
- **Claims resting on a report line only.** The reviewers traced most claims to the line of an analysis report and opened the library itself for a minority (about 15 of 63 on the printer platforms, about 30 of 144 on security). The corrections applied in this pass were each opened at the cited line; unchanged text was not re-traced.
- **The option text of your 25 answers** was read from the board's data file, not from the board export. The numbered record of your answers holds only the label you tapped; copying the full option text into that record is still to be done.
- **That the card key and the QR key are one value** was established by comparing the two without displaying them; this pass did not open those files again.
- **One piece of general knowledge, not from the library:** that a sign-in token obtained by the server may not work at a Workpath printer. A phase-0 test settles it.
- **Sizes of the new work packages and the scores of the nine new risks** are estimates made in this pass, not measured.
- **The library copy that was read** is the backup copy; it was not compared file by file with the original on the laptop drive.

Details: one row per review finding in `review/B1757_APPLIED.md`; the changes themselves in the change logs at the end of `02_architecture.md` and `03_plan-of-attack-and-build.md`.
