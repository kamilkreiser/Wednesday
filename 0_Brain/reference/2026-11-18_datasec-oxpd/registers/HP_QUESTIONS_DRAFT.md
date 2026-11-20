# Datasec OXPd 2: the questions to HP (DRAFT, nothing sent)

Datasec / OXPd 2, 2026-11-20. Work package WP0.5, the draft only (`03_plan-of-attack-and-build.md:141`; `05_readiness-to-build.md:213`). For the product owner. **This is a draft. Nothing in it has been sent to HP or to any person, and nothing in it has been agreed by HP.** Sending is the product owner's (`05_readiness-to-build.md:213`; C-42, `CLARIFICATIONS.md:274`).

How to read it: each ask below is one block that can be sent by itself. The text inside the fenced box is the copy-ready message, written in the first person. Square brackets mark what only the product owner can fill in. The note under each box is for the product owner only and is not part of the message.

Pointer forms: `02:n`, `03:n`, `05:n` are line n of `02_architecture.md`, `03_plan-of-attack-and-build.md`, `05_readiness-to-build.md`; `CL:n` is `CLARIFICATIONS.md`; `B1:n`, `B2:n`, `B3:n`, `C1:n`, `C2:n`, `A10:n` are line n of that analysis report. All in `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`. Line numbers are of the copies as they stood on 2026-11-20 at about 13:25 AEDT.

## BLUF

1. **Eight asks.** H1 the written confirmation; H2 App Center and validation enrolment, and the named contact; H3 the four dates; H4 a first signing round with fewer than seven tested printer groups; H5 lab access (developer key, simulator, its guide, pilot firmware); H6 the licence terms; H7 anything newer than OXPd 1.8.4.1; H8 six technical points HP's guides leave open.
2. **The others wait on H2.** The plan routes the dates (H3) and the first-round answer (H4) "through that contact" (`03:47`), and H6 and H8 need the same named person or channel. H1 can go at once to whoever gave you the confirmation. H5 can go to the developer portal's support in parallel. H7 is independent.
3. **Three have a date pressure:**
   - **H5 (lab access): costs time now.** Phase 0 has started (`05:7`). No test on a newer printer can run until the printer is in developer mode, and that needs the HP developer key and firmware 6.38.0.793 or later (`05:181-183`; `B1:207`). The simulator image is not downloaded and its guide was refused for your account (`05:180`; `B3:401-402`).
   - **H6 (licence terms): costs rework if the answer is no.** The clients for the newer printers are being written now from HP's published specifications (WP0.4, `05:212`). That rests on your answer "As assumed" (C-11, `CL:64-68`), not on anything HP has said: the SDK package holds no terms at all (`B3:326`).
   - **H2 and H4: cost time from the end of phase 1.** The first submission to HP is planned for when the first slice works, and the plan's exit point E1.9 needs HP's written answer on the first round by then (`03:89`). Phase 0 supplies one printer of the seven groups HP asks for (`05:203`).
4. **H3 has no deadline of its own but one consequence:** no customer date for the newer printers can be given to anyone until HP dates its four items (`05:18`; `02:899`).
5. **What I could not support from the documents is written as a question, not a statement.** In particular: HP's written confirmation is not in the library; the only evidence for it is your answer (C-30, `CL:178-182`; `05:230`). H1 therefore has two bracketed places only you can fill.
6. **The Jira read worked** (issue `OXPD2-1`, description and both comments, one request). Its group "To raise with HP" has two items; they map to H1 to H5. H6, H7 and H8 come from the documents, not from that group.
7. Twelve further questions are already answered by HP's published documents and are not asks (section ANSWERED BY THE DOCUMENTS). 37 items on the master list are yours, your team's or another team's, not HP's (section NOT FOR HP).

---

## H1. Written confirmation that a server-side Microsoft 365 integration is acceptable on OXPd

```
Subject: Datasec: written confirmation of our OXPd approach (server-side Microsoft 365 integration)

Hello [name],

Datasec is building an OXPd version of our HP Authentication Manager suite
(sign-in with Microsoft Entra, plus our Mailflow, Teams, OneDrive, SharePoint
and Universal Print applications). It is a server on the customer's own
network. The printer never talks to Microsoft: our server does, and the panel
only shows pages our server serves.

[When and how HP told us: for example "When we spoke on <date>" or "In your
e-mail of <date>"], my understanding was that HP is comfortable with this
approach for OXPd. Could you confirm that in writing? Specifically:

1. Is an OXPd solution whose server calls Microsoft 365 (Entra sign-in,
   Microsoft Graph, Universal Print) acceptable to HP on OXPd 2 and on
   OXPd 1.x?
2. Is such a solution eligible for HP validation and signing on OXPd 2, on the
   same terms as any other OXPd 2 solution?
3. We are aware of a 2023 statement on the developer forum that OXPd does not
   support direct integration with public cloud services and that Workpath is
   the route for that. Is our reading correct that this concerned the printer
   connecting to the cloud service itself, and does not apply to a design
   where only the solution's server does?

A short reply by e-mail is all we need. We would like to keep it on file and
refer to it when we submit for validation.

Thank you,
[name]
```

**What Datasec needs back:** one written reply, yes or no to each of the three points. **When it starts to cost time:** it is an exit condition of phase 0 ("HP's written confirmation filed", `03:71`), and it is wanted before the first submission to HP so that a different HP reviewer does not reopen the 2023 statement (`02:912`).

**Note for the product owner only.**
- Why it is asked: the whole newer-printer track was unblocked by your answer "Yes, HP confirmed" (C-30, `CL:178-182`; decision D33, `02:899`). The confirmation itself is not in the library (`05:230`). The 2023 forum statement is at `B3:22` and `B3:370`. What your answer covers (HP's position only, or also a signing route and a date) is still your open question 1 (`05:48-51`): this message asks HP for the position only, and H3 asks for the dates separately.
- The bracketed opening is yours to make true. I do not know when, how or from whom the confirmation came, so the message does not say. If the confirmation was spoken, say so; if nothing was said about signing, point 2 is a new question to HP and not a confirmation.
- Tuesday's default if HP does not answer: the design carries on as now, on your answer C-30, with the risk recorded (R2 in `02:912`), and the gap is put to you again before the first submission to HP.
- Who at HP: the documents name no person. They say "the HP contact behind C-30's confirmation" (`02:928`), which only you know.

---

## H2. Enrolment for HP App Center and validation, and a named contact

```
Subject: Datasec: HP App Center enrolment and a contact for OXPd 2 validation and signing

Hello [name],

Datasec intends to submit an OXPd 2 solution for HP validation and signing.
Before we do, could you help us with the following?

1. Is Datasec already enrolled in HP App Center for OXPd 2 solutions? If not,
   what are the steps, who at Datasec has to hold the master administrator
   account, and how long does enrolment usually take?
2. Who is our contact at HP for validation and signing questions, and what is
   the right channel for them (the developer forum, a support ticket, or a
   named person)?
3. What is the submission route today: what we upload, what HP checks, and
   what comes back to us?
4. What does HP want to see with a submission besides the bundle itself (for
   example a user guide, a statement of the data the solution handles, the
   list of printers we tested on)?
5. Is there anything Datasec has to sign or accept before a first submission
   (an agreement, programme terms, a fee)?

We would like to start this early, in parallel with development, so that the
process is not new to us on the day the solution is ready.

Thank you,
[name]
```

**What Datasec needs back:** whether the enrolment exists; a named contact or channel; the steps and the paperwork. **When it starts to cost time:** the plan starts the submission track in phase 0 and submits an early bundle as soon as the first slice works, not at the end (`02:911`); every other ask in this draft except H1, H5 and H7 is meant to go through the contact this one produces (`03:47`).

**Note for the product owner only.**
- Why it is asked: a production bundle for newer printers must be validated and signed by HP through the App Center, which needs a company enrolment and a master administrator account (`B1:134`). Whether Datasec holds one is not in the documents: the reports asked and nobody answered it as a fact (`B1:624`; `B3:498`; `C2:266`). It is item 14 of the phase-0 kit (`05:191`) and part of work package WP0.5 (`03:141`). HP's signing process is on the release-1 critical path (R1, `02:911`).
- Points 3 and 4 are partly answered by HP's own publishing page as the library holds it (upload of the bundle, declared languages, self-certified printers, an app guide, the data collected: `B1:150`). They are asked anyway in one line each because that page also marks every platform version "Not Supported" for validation (`B1:487`; `B1:601`), so what the page describes may not be what happens today. Strike them if you prefer a shorter message.
- An optional sixth line, left out of the box: "What is the HP Token Proxy that the App Center issues client credentials for, and does an on-premises solution need it?" HP's page mentions it once and no guide explains it (`B1:153`). The design ignores it (`03:350`). Add it only if you are curious; nothing waits on it.
- Tuesday's default if HP does not answer: development continues on the simulator and on a printer in developer mode only; nothing reaches a customer's newer printer (`B3:498`; `B3:414`).
- Who at HP: not named anywhere. The plan says "Kam or HP partner manager" (`03:288`); one report speaks of an "HP PSM/alliance manager" (`C2:266`). Never an address or a name in the documents.

---

## H3. Dates for the four things a customer installation on FutureSmart 6 depends on

```
Subject: Datasec: OXPd 2 production dates (firmware, platform version, signing)

Hello [name],

We are planning the release of an OXPd 2 solution and need to know what we
can tell our customers about timing. As far as we can see from the developer
portal, four things have to be in place before an OXPd 2 solution can be
installed on a customer's printer, and we have not found a date for any of
them. Could you give us HP's current dates, or best estimates, in writing?

1. Production FutureSmart 6 firmware that customers may run with OXPd 2
   solutions. (The firmware we can see is marked as beta, for internal testing
   only and not for distribution to customers.)
2. An OXPd 2 platform version that HP validation accepts. (The platform
   versions table on the portal lists every version as pre-release and "Not
   Supported" for validation, and does not yet list Beta 10.)
3. A signing service whose signed bundle installs on a printer that is not in
   developer mode. (A thread on the developer forum in November 2026 describes
   a bundle signed through the App Center that the Beta 10 firmware and the
   simulator still rejected. Has that been resolved?)
4. HP's turnaround for validation and signing once a bundle is submitted, for
   a first submission and for a later update.

Two related questions:

5. When will the list of printer models that support OXPd 2 be published?
6. Is there a date for a production (non-beta) OXPd 2 SDK?

If a date is not known, the dependency would help us as much: what has to
happen first, and who decides.

Thank you,
[name]
```

**What Datasec needs back:** a date or an estimate for each of the four, in writing; for 5 and 6 a date or "not known". **When it starts to cost time:** not before the release gate, with one exception: no date for the newer printers should be given to any customer or partner until these are in (`05:18`). If any of the four is late at the release gate, release 1 waits or the older printers ship first, and that choice is yours at that point (`03:267`; `02:899`).

**Note for the product owner only.**
- Why it is asked: these are "the four items, none dated" of decision D33 (`02:899`), named in both documents' BLUF (`02:20`; `03:11`) and in `05:18`. WP0.5 is the package that asks for them (`03:141`; `02:911`).
- Each bracketed fact in the message has its source: beta firmware "may not be distributed to customers" (`02:899`, citing HP's download page; `B1:493`); the platform table (`B1:487`); the rejected signed bundle and HP's last word of 17 November 2026, still waiting on its signing team (`B3:18`; `B3:344`); the model list "will be defined prior to production release" (`B1:491`; `B3:379`); no production date anywhere, and a direct forum question of February 2024 that has no reply (`B3:378`).
- The forum thread in point 3 is another partner's. The message names no partner, no solution and no person; keep it that way (`B3:522` lists what in that thread is third-party business data).
- Question 6 (the production SDK) is not one of the four: the design keeps it off the critical path by not shipping HP's library (`02:899`; `02:926`). It is asked because the answer to H6 depends on it.
- Tuesday's default if HP does not answer: no date is planned or promised for the newer printers; both printer generations are still built for the same release; the plan carries sizes, not dates (`03:13`).
- Who at HP: through the contact H2 produces (`03:47`). One HP forum reply says FutureSmart 6 availability goes "via the PSM" (`C2:178`); the documents do not say who that is for Datasec.

---

## H4. A first signing round with fewer than seven tested printer groups

```
Subject: Datasec: first OXPd 2 validation round with fewer than seven tested printer groups

Hello [name],

HP's publishing guidance for OXPd 2 asks for a solution to be tested on at
least one printer from each of five multifunction groups (A to E), and, for a
solution that handles sign-in, also on one from each of two printer groups
(F and G), on the latest firmware at the time of submission.

Our solution handles sign-in, so that is seven groups. Today we have access
to [number and models: for example "one FutureSmart 6 multifunction printer"]
and the simulator. We will not declare a group as tested when it was not.

1. Can a first validation and signing round go ahead with fewer than the
   seven groups tested, for example for a pilot limited to the models we did
   test, with the remaining groups added in a later round?
2. If all seven are required for any signing at all, can HP help with access
   to printers from the groups we lack (loan units, a partner lab, remote
   access)?
3. Does a test on the simulator count for any group?
4. Does "latest firmware at the time of submission" mean pilot firmware today?

We would like to submit early so that problems in the process show up while
there is still time to fix them.

Thank you,
[name]
```

**What Datasec needs back:** yes or no to a reduced first round, and if no, what HP can offer for the missing groups. **When it starts to cost time:** at the end of phase 1. The exit point E1.9 needs HP's written answer on this by then; if HP requires all seven, the first submission moves to when the printers are borrowed, and that date comes to you (`03:89`).

**Note for the product owner only.**
- Why it is asked: HP's rule is one tested printer from each of groups A to E, and F and G as well for a solution with sign-in (`B1:136`, with the group table at `B1:138-146`; `03:89`). Phase 0 supplies one (`05:203`). The design's rule is that no group is self-certified untested (`02:781`; R10 in `02:920`). The ask is the last clause of the WP0.5 row (`03:141`) and of kit item 14 (`05:191`).
- The bracket is yours: what printers you actually hold is not established. You named an HP MFP M577 (C-39, `CL:244-250`); its firmware and its OXPd generation are not known (`05:198`), and the documents show an M577 only in older-printer field reports (see ANSWERED BY THE DOCUMENTS, row 12). Do not write that you hold a FutureSmart 6 printer unless you do.
- Questions 3 and 4 are not in the plan's wording of the ask. They are added because HP's page does not say either way and both change how many printers must be borrowed. Strike them if you want the ask exactly as the plan words it.
- Tuesday's default if HP does not answer: the first signing round waits for the printers; nothing is submitted with an untested group declared (`02:920`; `03:89`).
- Who at HP: the contact from H2.

---

## H5. Lab access: developer key, simulator, its guide, pilot firmware

```
Subject: Datasec: OXPd 2 developer access (debug bridge key, simulator, simulator guide, pilot firmware)

Hello [name],

We are setting up our OXPd 2 lab and are missing four things. Could you help
us get them, or tell us whom to ask?

1. LaserJet Debug Bridge service key. We understand it is requested from the
   developer portal and tied to a developer account. Is our account
   [account e-mail] enabled for it, and is one key enough for a small team or
   does each developer need their own?
2. The OXPd 2 simulator image for the current beta (the file we expect is
   HPExtSim_6.38.0.793.ova). Is that still the current image, and where do we
   download it?
3. The HP Extensibility Simulator Guide. The download was refused for our
   account (HTTP 403). Could access be granted, or the document be sent?
   The portal also has a section marked limited access that our account
   cannot open: what is in it, and do we need it for a solution that does
   sign-in, scanning and printing?
4. FutureSmart 6 pilot firmware at or above 6.38.0.793 for a physical printer.
   How does a partner obtain it, for which models, and under what conditions?
   [Optional: We have an HP <model>. Can it run this firmware?]

We understand that switching developer mode on or off removes every solution
from the printer, and that it needs someone at the control panel and outbound
internet access from the printer to HP. If there is anything else we should
know before we do it to a printer, please say.

Thank you,
[name]
```

**What Datasec needs back:** the key (or confirmation the account can create one), a download location, the guide, and the route to pilot firmware. **When it starts to cost time:** now. These are items 3, 5 and 6 of the phase-0 kit (`05:180`, `05:182`, `05:183`); without the key the lab printer cannot be put into developer mode (`05:182`), and the tests that need a newer printer or the simulator (S1, S4, S8 and half of S6: `03:54`, `03:57`, `03:59`, `03:61`) cannot start.

**Note for the product owner only.**
- Why it is asked: the second item of the master list's group "To raise with HP" (Jira `OXPD2-1`, read 2026-11-20). Sources for each point: the key and what enabling needs (`B1:207`; `B3:347`); the wipe on toggling (`B1:208`); the simulator image is not in the library (`B3:401`; `05:180`); the guide returned 403 for your account (`B3:402`; `03:37`); the "limited access" portal section your account cannot open (`B3:383`; `B3:490`); the pilot firmware and how Datasec obtains it are unknown (`B3:404`; `03:39`), and in the field the firmware files are named "FS6-Pilot" (`B3:378`).
- Points 1 and 2 may need no HP person at all: `05:182` lists the key as yours "from HP's developer site", and the image is a portal download. Try the portal first; send the message for whatever the portal refuses.
- The optional line in point 4 is there because which printer you hold is not established (`05:198`). The documents cannot answer whether an M577 runs FutureSmart 6: HP's list of OXPd 2 models is "to be defined" (`B1:491`).
- Two known field problems you may want to mention if they happen to you, not before: a partner could not re-enable developer mode after disabling it once (`B3:346`, no HP reply at 13 November 2026), and developer-mode sign-in failed after a firmware move until proxy settings were checked (`B3:345`).
- Tuesday's default if HP does not answer: the work that needs no hardware carries on (`05:205-225`); the tests on newer printers wait; the simulator and a developer-mode printer stay "to be confirmed" on the kit list.
- Who at HP: the developer portal and its support forum for points 1 to 3 (`B1:207`). For firmware, "via the PSM" is HP's own phrase (`C2:178`); the documents do not say who that is for Datasec.

---

## H6. Licence terms: what Datasec may ship

```
Subject: Datasec: licence terms for the OXPd 2 SDK and the OXPd 1.8.4.1 libraries in a shipped product

Hello [name],

We want to be sure that what we ship is within HP's terms. The OXPd 2 SDK
package we downloaded contains third-party notices but no statement from HP
on what a partner may do with the SDK. Could you point us to the governing
terms, and confirm the following?

OXPd 2
1. Which agreement governs a partner's use of the OXPd 2 SDK during the beta
   and after it, and where can we read it?
2. Our plan is NOT to ship HP's OXPd 2 client library. Our server would use
   our own client code, written from the interface specifications HP
   publishes with the SDK. Is that acceptable to HP for a production
   solution, and does it change anything for validation and signing?
3. Once a production SDK exists, may the HP client library be shipped
   unchanged inside a partner's product?
4. Are there confidentiality terms for the beta that limit what we may tell
   our customers about OXPd 2 before production release?

OXPd 1.x
5. The SDK user guide says licensed users may distribute the pre-built
   libraries unchanged as part of a solution. Does that hold for the
   1.8.4.1 release, for both the .NET and the Java library, and for the
   panel user-interface kit?
6. Our server hosts the service endpoints the printer calls (sign-in agent,
   card reader events, statistics, scan notifications). For those we build
   our own endpoints from the service descriptions delivered inside the HP
   library. Is that within the terms?

A pointer to the documents is enough if these are already written down.

Thank you,
[name]
```

**What Datasec needs back:** the name and location of the governing terms; yes or no to points 2, 3, 5 and 6. **When it starts to cost time:** now for point 2. The newer-printer clients are being written from HP's specifications in the work that has started (WP0.4, `05:212`; `03:140`). A "no" would send the newer-printer adapter back to HP's library and to waiting for HP's production SDK.

**Note for the product owner only.**
- Why it is asked: your answer on HP code rights was "As assumed" (C-11, `CL:64-68`), and the assumption is the plan's, not HP's: reimplement the logic, ship HP's older library unchanged, ship HP's newer library only after a production SDK (`03:325`). The documents record that the SDK package holds no partner terms at all (`B3:326`), that the terms must be in a portal or partner agreement nobody has read (`B3:326`; `B3:406`), and that redistribution of HP's newer library inside an installer is unconfirmed (`B3:425`). Risk R16 (`02:926`).
- Point 2 is the one the design rests on. The shipped adapter uses Datasec's own clients, and a release that contains HP's beta library fails the build (`02:926`; `03:72`). HP has said it "tests and commits to supporting the signed libraries" and has no position on generated clients (`B3:295`; `03:140`). So the message asks; it does not claim HP agreed.
- Point 5 is mostly answered by HP's guide already (ANSWERED BY THE DOCUMENTS, row 5): it is asked only because the 1.8.4.1 Java library carries no licence text and two different files share one name (`02:49`; `A10:186-190`). Strike it if you are content with the guide.
- **Point 6 deserves your eye before it is sent.** HP's older SDK guide forbids using the library source "or any other means of reverse engineering" on the protocol between library and printer (`C1:316`). The plan builds test stubs from the service descriptions inside HP's library (`03:140`) and hosts the printer-facing endpoints on a framework HP does not demonstrate (`02` component C3, line 332). I did not find a place in 02, 03 or 05 that weighs that clause (search for "reverse engineer" in the folder: one file, report C1; positive control "LDB": 11 files). Whether to raise it with HP, or to have the clause read by someone qualified first, is yours. Leaving point 6 out is a legitimate choice; I list it so that the choice is made knowingly.
- Tuesday's default if HP does not answer: as today. Own clients for newer printers; HP's older library shipped unchanged and identified by checksum; HP's newer library in the lab only (`02:926`; `05:212`).
- Who at HP: not stated. The contact from H2, or whoever manages Datasec's partner agreement with HP.

---

## H7. OXPd 1.x: is there anything newer than 1.8.4.1?

```
Subject: Datasec: OXPd 1.9 availability

Hello [name],

We are building on the OXPd 1.8.4.1 SDK for FutureSmart 4.7 to 5 printers.
An HP reply on the developer forum in March 2026 mentioned a "soon to be
released OXPd 1.9".

1. Is OXPd 1.9 available to partners, as a release or a preview? If so, how
   do we get it?
2. If it is not out yet, is there a date, and what does it change for a
   solution that does sign-in with card readers, scanning and printing?
3. Would 1.9 change the lowest firmware a printer needs, or the rule that an
   OXPd 1.x solution needs no HP approval before it is deployed?
4. Is there a stated support period for OXPd 1.x on FutureSmart 4 and 5?

If the answer to the first question is no, we carry on with 1.8.4.1.

Thank you,
[name]
```

**What Datasec needs back:** yes or no to 1.9, and a download if yes. **When it starts to cost time:** only if the answer is yes, and then at the start of phase 2, the older-printer adapter (`05:131`).

**Note for the product owner only.**
- Why it is asked: your open question 12 (`05:127-131`), whose recommendation is "ask your HP contact". Your brief says "OXPD 1, whatever the latest version is" (C-1, `CL:9`); the library's newest is 1.8.4.1, and HP called 1.9 "soon to be released" in March 2026 (`C1:405`; `C1:422`; `C1:515`). The same roadmap item has been "soon" since 2017 (`C2:248`), which is why the default is to treat 1.9 as absent.
- If you already know from HP that nothing newer exists, this is not an ask: answer question 12 yourself and drop the block.
- Point 4 is an addition of mine: HP said in 2019 that there is "no specified product lifecycle policy for OXPd libraries" (`C1:429`), and nothing newer was found. Strike it if unwanted.
- Tuesday's default if HP does not answer: build on 1.8.4.1 (`05:130`; `03:340`).
- Who at HP: not stated. Any HP developer-support channel; the March 2026 statement was a forum reply (`C1:405`).

---

## H8. Six technical points HP's OXPd 2 guides leave open

```
Subject: Datasec: six OXPd 2 behaviour questions (Beta 10)

Hello [name],

While designing against the Beta 10 SDK we found six points where the guides
are silent or disagree with each other. We will test each on a printer, but a
word from engineering would save time and tell us what is intended.

1. Tokens after a reboot. Does the solution's token (and its refresh token)
   survive a printer reboot, a power loss and a firmware update? If it can be
   lost, can the solution request a new install code with its own token, or
   does that always need the printer administrator's credentials?
2. Upgrading an installed solution. If we install a bundle with the same
   solution id over an installed one, is it replaced in place, refused, or
   something else? Is uninstall then install the intended upgrade route?
3. Printing while the user is at the panel. The IPP extensions guide says
   that submitting a job to a printer in priority print mode is currently not
   supported, by value and by reference; the pull print demo appears to do
   it. Which is right on current firmware?
4. Browser session data between users. When one walk-up user signs out and
   the next signs in, are cookies and cached data of the embedded browser
   cleared? Is that guaranteed, or still under development?
5. Certificate trust in the embedded browser. For pages on third-party sites
   listed as trusted sites, does the browser use the solution's own
   certificate authority store only, or also a public root store?
6. Card reader registration record. The Beta 10 release note deprecates one
   USB accessories record type in favour of another, while the guide says the
   newer one is not supported. Which one should a Beta 10 bundle carry?

Thank you,
[name]
```

**What Datasec needs back:** one line per point. **When it starts to cost time:** it does not, by itself: each point has a test in phase 0 that settles it on a real printer. An early answer shortens those tests and tells us whether what we measure is intended behaviour or an accident of one beta.

**Note for the product owner only.**
- Why it is asked: each point changes a design decision, and each has its phase-0 test:
  1. Tokens after reboot: the guides say the token "may need to be reissued" (`B1:536`; `B1:614`); it decides whether a newer printer's admin password must be kept (your open question 2, `05:53-57`); test S1 (`03:54`).
  2. Same-id upgrade is undocumented (`B1:195`); the design plans "install new, verify, remove old" until HP confirms (`02:803`); test S8 (`03:61`).
  3. Priority print: the guide and the demo disagree (`B1:531`; `B1:611`); it decides how Universal Print release behaves; test S6 (`03:59`).
  4. Cookies between users are "under development" (`B1:580`; `B1:519`); it decides whether Microsoft's page may ever be shown on the panel; test S4 (`03:57`).
  5. Which certificate store the browser uses for third-party sites is not stated (`B1:609`); same decision as point 4.
  6. The record type: release note against guide (`B3:337`; `B1:521`); component C19 records the disagreement (`02` line 348); test S1 (`03:54`).
- The original report question asked for "an HP contact who can answer four platform questions" (`B1:634`); points 2 and 6 were added from the later documents.
- This is the least urgent block and the most technical. It can be posted on the developer forum by the team instead of being sent by you; a forum post is still a message to HP, so it is still yours to release.
- Tuesday's default if HP does not answer: the phase-0 tests decide, as planned (`03:50-66`).
- Who at HP: the OXPd 2 developer forum or a partner engineer (`B1:634`). The reports note that replies take days to weeks and that several threads closed without a fix (`B3:421`).

---

## How the master list's HP group maps to the blocks

The group "To raise with HP" of Jira `OXPD2-1` (read 2026-11-20, updated stamp 2026-11-20T12:25:10+1100) has two items:

| Master list item | Blocks |
|---|---|
| "From HP, in writing: the confirmation reported; App Center and validation access and the contact behind it; dates for production firmware, the accepted platform version, the signing service and its turnaround; whether a first signing round is possible with fewer than seven tested printer groups." | H1, H2, H3, H4 |
| "HP developer account with an LDB Service Key (needed to put a FutureSmart 6 printer into developer mode), the newer-printer simulator image and the HP Extensibility Simulator Guide." | H5 |

Not in that group and added from the documents: H6 (licence terms: `03:325`, `02:926`, `B3:326`), H7 (the master list keeps it under "Open, proceeding on a default" as "OXPd 1.x version"; `05:130` recommends asking HP), H8 (`B1:634` and the tests of `03:54-61`). If the product owner agrees they are asks, they belong in the HP group of the master list; adding them there is Tuesday's, not this draft's.

## ANSWERED BY THE DOCUMENTS

Questions that look like questions for HP and are already answered by HP's published documents as the reports cite them. They are not asks. Twelve rows.

| # | Question | Answer | Pointer |
|---|---|---|---|
| 1 | Do FutureSmart 6 printers still run OXPd 1.x solutions? | No. OXPd 2 is on FutureSmart 6 and later only, and "those devices will not support OXPd1" | `B1:489` (HP portal `how-it-works.md:28`); dropped as a question at `03:359` |
| 2 | Does an OXPd 1.x solution need HP approval or signing before a customer deployment? | No, for 1.8 and the announced 1.9. Caveat: an HP forum reply of March 2026, not marked official | `C1:405`; `03:364` |
| 3 | What is the lowest firmware with the full OXPd 1.8 feature set? | FutureSmart 4.7 (HP release notes of 2024 and 2025) | `C1:423` |
| 4 | What firmware does OXPd 2 Beta 10 need? | 6.38.0.793 or later | `B3:16`; `02:765` |
| 5 | May HP's OXPd 1.x library be shipped inside a product? | Yes, unchanged; not its source, not a modified library. The panel kit likewise, unchanged. Residual doubt only for the 1.8.4.1 Java file, asked in H6 point 5 | `C1:316`; `C1:485`; `02:49` |
| 6 | How is developer mode switched on, and what does it need? | At the panel, with an HP developer account and a service key from the developer portal, admin access, and outbound internet from the printer; switching it on or off removes every solution and reboots | `B1:207-208`; `B3:347` |
| 7 | May developer mode be used at a customer? | No: HP says it is for development and demos only | `B3:18`; `B3:345` |
| 8 | By which route is an OXPd 2 bundle installed, and does HP offer a fleet tool for it? | Only the installer service on the printer; the cloud, USB and web-page routes are not supported; no HP fleet tool is documented | `B1:166-173`; `B1:202` |
| 9 | Which printer groups must be tested for signing, and which models are in each? | Groups A to E for any solution, F and G as well for one with sign-in; the models are tabled | `B1:136-146` |
| 10 | What do the two simulators need? | Newer printers: an x86-64 host, VMware, nested virtualisation, Hyper-V off, a wired network, WSL 1 if the packaging tool shares the machine. Older printers: Windows, .NET Framework 4.6 to 4.7, IIS; that simulator is already in the library | `B3:348`; `B3:351`; `C1:339-341`; `03:36` |
| 11 | Can a printer fail over between two servers by itself? | No. HP firmware has never offered it; the manifest field for it is "not supported in this release" | `B3:371`; `B1:116` |
| 12 | Which OXPd generation is an HP MFP M577? (partly answered) | The documents show an M577 only in older-printer (OXPd 1.x) field reports, one of them on FutureSmart 5.3.0.1. That points to OXPd 1.x and does not establish it for the unit in hand: its firmware version is read from its own panel, not asked of HP | `C2:126`; `C2:140`; `05:198` |

**Where I looked before listing an ask** (step 3 of the commission). Two searches. (1) The subjects of H1 to H5 and H7 (signing, App Center, validation, the four items, turnaround, the seven groups, licence terms, the developer key, pilot firmware, the simulator guide, OXPd 1.9) were searched in `02_architecture.md` by term and in `03_plan-of-attack-and-build.md` by every line containing "HP"; 05 and CLARIFICATIONS were read whole. (2) 23 further subjects (among them the M577, reverse engineering, the HP Token Proxy, interim firmware, the limited-access portal section, the model list, HP's IPP sample code, user policy, Workpath targets, beta confidentiality) were searched in every `.md` file under the reference folder (`02`, `03`, `05`, `CLARIFICATIONS.md`, `analysis/`, `review/`) with `/usr/bin/grep -r -l -i`, with a positive control in the same run: the term "LDB", known to be present, returned 11 files. I then read the matching lines in 02, 03, 05, B1, B2, B3, C1 and C2. The product owner's 25 answers were read in the plan's own table (`03:304-330`) and in `CLARIFICATIONS.md` (C-6 to C-30). Subjects for which the search returned no answer, only the open question: HP's written confirmation (only C-30 and `05:230`), App Center enrolment, the four dates, the first-round rule, the pilot-firmware route, the SDK's partner terms, OXPd 1.9. Subjects searched and found to be settled by the design, so not asks: per-user device permissions (`03:336`), kiosk mode (`03:335`), Workpath target variants on newer printers (`03:339`), Web Jetadmin (`03:341`), HP's IPP sample code (not used: `03:325`).

## NOT FOR HP

Items on the master list (Jira `OXPD2-1`, description and comment 41406) that are the product owner's own, his team's or another party's. 37 items. None is turned into an ask.

**The product owner's or his team's, "needs an answer first" (6):** the card key (question 8, `05:94-98`); the printer on hand, its firmware and whether it may be wiped (`05:198`); the Windows machine for the simulators (`CL:216-226`); `cc-api` (OP-11); the empty repository `OXPD1` (OP-18); the start of building, which the list still shows as waiting although the word was given on 2026-11-20 (C-42, `CL:268-274`).

**The product owner's, "open, proceeding on a default" (12 of the 13 in that group):** what "Yes, HP confirmed" covers (question 1; H1 gathers HP's side of it, the reading of his own answer stays his); the admin password on newer printers (2); the meaning of "full match" (3); OneDrive personal (4); the HP Advance and LRS VPSX sign-in role (5); the design choices that differ from Workpath (6); the Universal Print registration (9); QR sign-in without MFA (10); one central server for several sites (11); sites with no internet (13); the pilot's success threshold (14); "intra-environments" (15). All at `05:48-147`. The thirteenth, the OXPd 1.x version (question 12), is H7.

**The product owner's or his team's, added on 2026-11-20 (18):** OP-1 to OP-18 (`05:149-172`). Two of them name HP products and are still not questions for HP: OP-10 (the source of the HP Secure Authentication phone app is asked of the team that holds it, default a capture in the test tenant) and OP-17.

**Another team's (1):** the access keys in a committed state file of the older back end's repository (Jira comment 41405; C-44, `CL:284-290`). Flagged by the product owner to the team that owns it; location only is recorded there and no value appears here.

Two questions the reports raised that touch HP and are deliberately not asks: whether a customer's other vendor solutions coexist (ruled: C-19, `CL:112-116`), and whether HP can supply interim firmware for older printers (`C2:267`; the design tests against public firmware and the product owner's answer on test devices was "As assumed", C-6, `CL:34-38`). If either should go to HP, say so and a block is added.

## WHAT I DID NOT READ

- **`02_architecture.md` and `03_plan-of-attack-and-build.md` were not read whole.** In 02 (1,067 lines) I read every line a search for HP's dependencies returned (signing, App Center, validation, the four items, turnaround, the seven groups, licence and redistribution, the developer key, pilot firmware, the simulator guide, OXPd 1.9, C-30, C-11, WP0.5) and lines 20, 22, 49, 231-234, 332, 348, 765, 781, 803, 899, 911-928, 1065-1067. In 03 (506 lines) I read every line containing "HP" (80 lines), and lines 30-69 and 294-387 in full. A dependency on HP that neither document words with "HP" or one of those terms would have been missed.
- `05_readiness-to-build.md` and `CLARIFICATIONS.md` were read whole.
- **Reports B1, B2, B3, C1, C2 were read in the parts a question rests on, not whole:** B1 lines 10-20, 112-209, 473-651; B2 lines 356-378; B3 lines 14-22, 270-527; C1 lines 307-344, 389-531; C2 lines 163-268. Not read: B1 sections 4.1 to 4.3 and 4.7 to 4.16; nearly all of B2; B3 sections 2 to 4.6; C1 sections 2 to 4.13; C2 sections 2 to 4.7.
- **Reports A1 to A10 and the review files R1 to R4 and the three APPLIED files were not read.** The two A10 lines cited (`A10:186-190`) are taken from the citation in `02:49`, not from A10 itself.
- **No HP document was opened.** Every statement about what HP's guides, portal pages, release notes or forum say is the report's reading of it, cited by report line. Nothing in the source library on the NAS was opened, and no positive control of the library mapping was needed or made.
- **HP's written confirmation was not seen.** It is not in the library (`05:230`). H1 is written without knowing when, how or by whom it was given.
- **The agreements Datasec has with HP were not seen** (partner agreement, developer-portal terms). H6 asks where they are.
- **The full option text of the 25 answers** (the board's data file) was not read; the labels in `CLARIFICATIONS.md` and the plan's table were.
- **Jira:** one request, `GET /rest/api/3/issue/OXPD2-1` with the fields summary, status, description, updated and comment; it returned the description and both comments (2 of 2). The kit checklist `OXPD2-2` was not read (outside the one permitted request). Nothing was written to Jira.
- **Nothing was verified with HP or on the web.** No network call other than that one Jira request. Whether any fact in the reports has changed since they were written (a new beta, a forum reply after 17 November 2026, a published model list) is not known; the copy-ready texts word the time-sensitive ones as questions for that reason.
- **Secrets:** no secret value was displayed by any command in this work, and none is in this file. The Jira credentials were read by name inside one process and never printed. No new secret location was found; the locations the reports already list (for example `B3:509-525`) were not opened.
