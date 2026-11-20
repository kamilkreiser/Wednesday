# Datasec OXPd 2: the open questions, by who answers them (DRAFT, nothing sent)

Datasec / OXPd 2, 2026-11-20, evening. For the product owner. **This file replaces `registers/HP_QUESTIONS_DRAFT.md` as the working document.** That draft is kept unchanged as a record; nothing in it should be sent as it stands, because three of its blocks are reworded here. **Nothing in this file has been sent to HP, to the Datasec product team or to any person, and nothing in it has been agreed by anyone.** Sending is the product owner's (C-45, `CL:298`; C-42, `CL:274`).

Why it was reworked: the product owner's message of 2026-11-20 15:41 (C-45, `CL:296`), which says, in his words: "this is a Datasec Project. Datasec created and owns HPAM (authentication) and all workflow apps. This OXPd project is also owned by Datasec. HP owns the printers, firmware. Datasec is in control over all aspects of this build on top of OXPd." and asks: "Please rework the questions document so we have a list for the Datasec team (there is currently an entire product team working on the warpath apps), the build team for OXPd up to MVP (we will leverage the work path team but hand it over for them to manage commercial deployment once ready) and HP". "warpath" and "work path" are read as the Workpath apps and their team; that reading is the coordinator's, recorded as such at `CL:298`, and is open to his correction.

How to read it: four parts, then the record. FOR THE PRODUCT OWNER HIMSELF (five items only he can answer); LIST A for the Datasec product team; LIST B for the OXPd build team; LIST C for HP. In lists A and C the text inside a fenced box is copy-ready: plain words, no internal numbers. The note under each box is for the product owner and is not part of the message. Square brackets mark what only the sender can fill in.

Pointer forms: `02:n`, `03:n`, `05:n` are line n of `02_architecture.md`, `03_plan-of-attack-and-build.md`, `05_readiness-to-build.md`; `CL:n` is `CLARIFICATIONS.md`; `B1:n`, `B3:n`, `C1:n`, `C2:n`, `A9:n`, `A10:n` are line n of that analysis report; `J` is the master list, Jira issue OXPD2-1, as read on 2026-11-20 (updated stamp 2026-11-20T14:03:13+1100). All files are in `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`. Line numbers are of the copies as they stood on 2026-11-20 after the evening update (02: 1,126 lines; 03: 529; 05: 266; CLARIFICATIONS: 306). They differ from the old draft's numbers, which were taken before that update.

## BLUF

1. **Counts.** For the product owner himself: **5**. LIST A, the Datasec product team: **24** questions and 2 notices. LIST B, the OXPd build team: **31** (15 decisions on a default, 16 tests). LIST C, HP: **8** asks holding 37 points (the old draft had 8 asks holding 38).
2. **What moved because of your statement (C-45).** The old draft put 37 items in one bucket, "the product owner's or his team's". Of those 37: **21 go to the Datasec product team** (LIST A), **10 to the build team** (LIST B), **4 stay with you**, 1 is answered (your word to start, C-42) and 1 is a notice you are passing on yourself (C-44). The full table is at the end; the counts in it are taken by program.
3. **What your statement changed in the HP asks.** No ask is dropped: each of the eight rests on something HP owns (its validation and signing service, its developer access, its firmware and dates, its licence terms, its platform's behaviour). **One question to HP falls away** and **three blocks are reworded**:
   - H1: the question "is this approach acceptable to HP" is gone. It asked HP's permission for Datasec's own design, and on the older printers HP has no approval step at all (`C1:405`). What is kept is what HP owns: a written record of what HP told you, and whether HP's validation and signing will take the solution.
   - H2: the opening and point 1 no longer ask HP whether Datasec is enrolled as if nobody at Datasec could know. The Datasec product team is asked first (A21); HP is asked only whether that enrolment covers OXPd 2.
   - H6: point 2 no longer asks whether writing Datasec's own client code "is acceptable to HP". It asks what HP's terms for its own published specifications say, and whether HP's validation needs HP's library. Point 6 (the clause in HP's older SDK guide) is **kept as HP's**, worded as a question: your statement of ownership says nothing about HP's licence terms, and this file does not read it as if it did.
   - H3, H4, H5, H7, H8 are unchanged in substance. Five points across H2, H5, H6 and H7 are now asked of the Datasec team first (A21, A22), and the bracket in H4 (which printers Datasec has) is filled from A23.
4. **The few that cost time now:**
   - **A21 (LIST A): who at Datasec holds the HP developer and App Center accounts, and who is Datasec's contact at HP.** Every block of LIST C has a bracket that this answers, and H5 cannot be sent to the right place without it.
   - **H5 (LIST C): lab access.** No test on a newer printer can run without HP's developer key and firmware 6.38.0.793 or later (`05:192-194`; `B1:207`). The simulator image is not downloaded and its guide was refused for your account (`05:191`; `B3:401-402`).
   - **A1 (LIST A): the card key.** It blocks the lab set-up and the first working slice (`05:106`).
   - **P2 (yours): the firmware version on your printer's panel, and whether it may be wiped.** Until then no printer of either generation is confirmed (`05:209`).
   - **H6 point 2 (LIST C): costs rework if HP's terms say no.** The newer-printer clients are being written now from HP's published specifications (`05:223`).
   - **B11 (LIST B): the Windows machine for HP's two simulators.** No simulator work can start without it (`03:36`).
5. **What you personally still have to answer: five things** (next section). P1 what HP told you, when, how and through whom. P2 the printer in your hands. P3 whether QR sign-in without MFA is offered on OXPd printers. P4 what "MVP" contains and where the hand-over to the Workpath team sits: no document defines either. P5 one word of your brief. Everything else has a team that can answer it or a default the build carries.
6. **Besides the five, three things stay yours by their nature and are not questions:** releasing any block of LIST C to HP; releasing LIST A to the team; approving any spend (the Windows machine in B11 may be one).
7. **The Jira read worked** (one request: the master list, its description and all five comments; the old draft saw two comments, three were added after it). Nothing was written to Jira.
8. **Not checked by me:** no HP document, no source tree and no printer was opened; every statement about HP's rules is a report's reading, cited by line. The last section lists what I did not read.

---

## FOR THE PRODUCT OWNER HIMSELF

Five items. Each is here because no team can answer it: it is your own knowledge, your own hands, or a product ruling the documents reserve to you. Each has a default, so none stops the no-hardware work.

**P1. What did HP tell you, when, how, and through whom? Did it cover signing, or only HP's position?**
- Why: your answer was "Yes, HP confirmed" (C-30, `CL:182`). The confirmation itself is not in the library (`05:241`). Whether it covers HP's position only, or also a signing route and a date, is open question 1 (`05:54-57`). The opening of block H1 has two brackets only you can fill. If the confirmation came through someone in the Datasec product team, say so and it becomes theirs (A21).
- Default: position only (`05:56`); no date is promised to anyone for the newer printers (`05:18`).
- Enough as an answer: one line, for example "by phone on [date] with [role at HP]; position only".

**P2. Your printer: what firmware version does its panel show, and may it be wiped?**
- Why: you wrote "I have a printer that can run oxpd" (C-34, `CL:210`) and a note read as "HP MFP M577" (C-39, `CL:248-250`). Its firmware, its OXPd generation and whether it may be put into developer mode (which removes everything installed on it) are not known (`05:209`). The documents show an M577 only in older-printer reports (`C2:140`), which points to the older generation and does not establish it for your unit.
- Default: one printer of each generation stays "to be confirmed" (`05:209`).
- Enough as an answer: a photo of the panel's firmware screen, and yes or no to "may be wiped".

**P3. Is QR sign-in without MFA offered on OXPd printers?**
- Why: the customer's sign-in gateway does not check who sends an unlock message, and without MFA that message is a full credential (`05:114-120`; `A9:240`). The weakness is in the existing gateway that Workpath printers use today, not something the new server adds. Two links between that fact and a real attack are inferred and not yet tested (LIST B, test T7). This is a ruling on how much risk the product carries, which the documents reserve to you (`03:381`). Fixing the gateway itself would be the Datasec product team's work.
- Default: offered as Workpath offers it, risk recorded; nothing of QR sign-in is built before phase 3 (`05:119`). The recommendation in the documents is to switch it off on OXPd until the gateway checks the sender (`05:118`).
- Enough as an answer: "as Workpath" or "off until the gateway is fixed". It can wait for the two test results.

**P4. What does "MVP" contain, and at which point is the product handed to the Workpath team?**
- Why: your message names "the build team for OXPd up to MVP" and a hand-over to the Workpath team "to manage commercial deployment once ready" (C-45, `CL:296`). Neither word is defined anywhere: "MVP" and "hand over" appear 0 times in `02`, `03` and `05` (same search finds "LDB" 4, 6 and 1 times). The plan has one release, release 1, which by your ruling is a full match of everything (C-16, `CL:98`; `03:10`), reached after six phases ending in certification and a pilot (`03:121-125`). So today the plan cannot say what the build team builds before it hands over.
- Default: the plan is unchanged; no phase is named "MVP"; the build team proposes a definition for you to accept or change (LIST B, B15).
- Enough as an answer: one of (a) MVP is the first working slice on both printer generations (the end of phases 1 and 2); (b) MVP is every app working in the lab (the end of phase 4); (c) MVP is release 1 ready for a pilot (into phase 6); or your own line. And: who takes the pilot and the HP submission, the build team or the Workpath team.

**P5. Your brief says "integration into intra-environments". Is that "Entra environments"?**
- Why: the wording is yours (C-1, `CL:9`); open question 15 (`05:152-155`).
- Default: yes, Entra. The one item the other reading would add, an outbound web proxy, is in the design either way (`05:154`).
- Enough as an answer: yes or no. Nothing waits on it.

---

## LIST A. For the Datasec product team (the people who build and run the Workpath apps today)

24 questions and 2 notices. Each box can be sent by itself. They are grouped so that one person can take a group: the keys and the back end (A1, A4 to A10), what is shipped and what customers have (A2, A3, A18 to A20, A24), the earlier OXPd 1 work (A11 to A14), the deployment utility (A15 to A17), HP and the lab (A21 to A23). A covering line you may want on top of whatever you send: "We are building an OXPd version of the suite. The questions below are about how today's apps and back end are built and run. A short answer in the form asked is enough."

### A1. The card key

```
Is the card key that is written into the source of HP Authentication Manager
4.4.1 (the same value in the card validator and in the encryptor) the key
that printers and phone apps in the field use today?

- If yes: please say so. Do not send the key in mail or chat. Tell us by
  which secure channel the lab can receive it, together with one licence
  installation credential for a test server.
- If no: how does a production build get its key (a build secret, a
  pipeline variable, something else)?

Enough as an answer: yes or no, and one line on the channel or on how
production builds get the key.
```

- Why it is asked: every stored card and every installed phone app depends on this key, and it is also the phone app's QR key (`05:102-106`; risk R27, `02:968`). The new server must use the same key for cards to work on both kinds of printer (C-28, `CL:170`). Your general sentence "keys will be old and rotated" (C-3, `CL:21`) does not name this key. The lab needs the key and a licence installation credential through a secure channel (kit item 15, `05:203`; `03:48`).
- Waits on it: the lab set-up (phase 0) and shared card sign-in (phase 1) (`05:106`).
- Default: treated as live; never copied, never printed (`05:105`).
- Old place: the product owner's, "needs an answer first". Moved because the team that builds the shipped apps knows how their builds get the key.

### A2. OneDrive for personal accounts

```
Is a OneDrive app for personal (consumer) Microsoft accounts shipped or sold
to any customer today, or promised to one?

Enough as an answer: yes or no. If yes, which customers.
```

- Why: the code has a build variant for it, but the release pipeline builds the business app only, the consumer sign-in is switched off, and the variant is not packaged (`05:71-76`). It also fixes the list of tiles frozen into the bundle HP signs, so it is wanted before the first submission to HP (`05:75`).
- Waits on it: one work package of phase 3 (`03:185`).
- Default: out; it is not a shipped product as far as the source shows (`05:74`).
- Note: if the team says yes, including it in release 1 follows from your ruling "Full match of everything" (C-16, `CL:98`); if the team says no, the default stands. No new ruling is needed either way.

### A3. HP Authentication Manager as the sign-in for HP Advance and LRS VPSX

```
The product documentation says HP Authentication Manager can be the sign-in
for HP Advance and for LRS VPSX. Does any customer use it that way today?

Enough as an answer: yes or no. If yes, roughly how many customers, and for
which of the two products.
```

- Why: open question 5 (`05:78-82`). Two of your answers pull opposite ways: "Full match of everything" (C-16) would include it, "No, ours only" (C-19, `CL:116`) would exclude it (`03:346`).
- Waits on it: the phase 3 exit and the release gate (`05:82`).
- Default: out (`05:81`). If the team answers yes, whether release 1 carries it comes back to you with that fact; this question only collects the fact.

### A4. The Universal Print app registration

```
For Universal Print the apps register printers under an app registration.
1. Is that registration owned by Datasec (in a Datasec tenant)?
2. Can Datasec change it, for example add a permission or a redirect
   address, without asking each customer?
3. Is there any reason a server on a customer's network should not use the
   same registration that the printer apps use today?

Enough as an answer: yes or no to each, and the name of whoever administers
the registration.
```

- Why: open question 9 (`05:108-112`). The design assumed the server may register printers under Datasec's own registration; your Universal Print answer (C-14, `CL:86`) does not cover it. `05:111` says "the team can check without a customer".
- Waits on it: Universal Print (phase 4) and one phase-0 test (T13, `03:66`).
- Default: assumed yes; nothing is built on it before the answer (`05:111`).

### A5. Sites with no internet

```
Does any customer or prospect need the suite to run at a site that has no
internet connection at all (so the server could never reach Datasec's
licence service)?

Enough as an answer: yes or no. If yes, how many sites.
```

- Why: open question 13 (`05:141-145`). Without the licence service a server runs for 20 days.
- Waits on it: nothing before phase 5 (`05:145`).
- Default: not supported in release 1 (`05:144`).

### A6. The licence-server offer in the Azure Marketplace

```
A second Azure Marketplace offer deploys a licence server into any Azure
subscription. Who is meant to deploy it: Datasec only, or partners and
customers too? Is any customer running their own licence server today?

Enough as an answer: one line, and yes or no to the second question. If its
source code is in a repository we have not been given, the repository name.
```

- Why: OP-7 (`05:169`; `A9:332`). It decides whether an OXPd server must expect a licence server at a host other than Datasec's, and it bears on A5. The licence server's source was not among what was sent (`A9:339`).
- Default: Datasec only (`05:169`).

### A7. How customers deployed the Azure side

```
The customer's Azure services for the suite (SignalR, the Function App, Log
Analytics) can be deployed two ways: by the Marketplace offer, or by the
deployment script. Roughly how many customers used each?

Enough as an answer: two numbers, or "nearly all by the offer" or the like.
```

- Why: OP-8 (`05:170`; `A9:333`). The phone-link sign-in needs a change on each customer's gateway, and a change reaches the two groups by different routes (risk R19, `02:960`).
- Waits on it: the phone-link relay (phase 3, `03:178`).
- Default: both exist; every gateway change ships both ways (`05:170`).

### A8. The gateway version that is live

```
Which version of the sign-in gateway package is live in the Azure
Marketplace today? Is it v1.3.0?

Enough as an answer: the version number.
```

- Why: OP-9 (`05:171`; `A9:334`). The built packages are not in the repository, so the live version is not recorded there (`02:960`).
- Default: yes, v1.3.0 (`05:171`).

### A9. The phone app

```
Can the source code of the HP Secure Authentication phone app be shared with
the OXPd project? If not: may we capture one sign-in message from the phone
app in a test tenant, to learn its format?

Enough as an answer: a repository name, or "capture it".
```

- Why: OP-10 (`05:172`; kit item 12, `05:200`). The gateway forwards the phone's message without reading it, so its format is known only from the printer's side (`A9:330`).
- Waits on it: QR sign-in (phase 3, `03:177`).
- Default: capture it in the test tenant (`05:172`; LIST B, test T15).

### A10. The repository cc-api

```
The repository cc-api is on the organisation's repository list. Is it the
API of the older Keycloak back end?

Enough as an answer: yes or no. If no, one line on what it is.
```

- Why: OP-11 (`05:173`; `A9:331`); also on the master list under "needs an answer first" (`J`). No OXPd customer is on the older back end by your ruling (C-18, `CL:110`).
- Default: yes; not needed, not asked for again (`05:173`).

### A11. The earlier OXPd 1 work: is there more of it?

```
We have the repository OXPd1_solution (its default branch). The repository
OXPD1 ("HP Authentication Suite OXPD V1.8") is empty.
1. Is there more of the earlier OXPd 1 work anywhere: another branch, a
   later working copy on someone's machine, or history we were not sent?
2. Is the empty repository OXPD1 meant to receive anything?

Enough as an answer: yes or no to each, and where the rest is if yes.
```

- Why: OP-13 and OP-18 (`05:175`, `05:180`; `A10:334`, `A10:339`); the master list's "OXPD1 repository" item (`J`). What was sent equals, byte for byte, what had already been analysed (`05:14`).
- Default: no, what was sent is the last state; the empty repository is ignored and new work goes to the project's own repository (`05:175`, `05:180`).

### A12. The earlier OXPd 1 work: was it ever run on a printer?

```
Was the earlier OXPd 1 code ever run against a physical printer? If so,
which model and firmware? Its author's notes name an "emulator": which one
was that, and on what machine did it run?

Enough as an answer: "printer: model and firmware", or "emulator only: its
name".
```

- Why: OP-15 (`05:177`; `A10:335`; `A10:175`).
- Default: emulator only; nothing in that code is treated as proven on hardware (`05:177`).

### A13. The earlier OXPd 1 work: its two card keys

```
The earlier OXPd 1 build has two card keys written into it. They are not
the card key of today's Workpath apps. Where did they come from: an older
version of the apps, or made up for the experiment?

Enough as an answer: one line. Do not send any key.
```

- Why: OP-16 (`05:178`; `A10:337`).
- Default: made up or outdated; never carried into the product (`05:178`).

### A14. The earlier OXPd 1 work: a printer password in its README

```
The README of the earlier OXPd 1 repository gives a printer administrator
password as the "default", next to a lab address. Is that the live password
of a lab printer? If it is, whoever owns that printer should change it.

Enough as an answer: yes or no. Do not send the password.
```

- Why: OP-14 (`05:176`; `A10:336`).
- Default: treated as live; never copied (`05:176`).

### A15. The deployment utility: where the OXPd changes live

```
The HPK Deployment Utility is to be extended so that it can also start and
follow OXPd roll-outs. Today a push to the utility's main branch publishes a
release.
1. Where should the OXPd changes be made: a branch of the utility's own
   repository, or somewhere else?
2. Who releases the utility, and how should an OXPd-capable version be
   released (a new major version, a separate build)?
3. Does the utility build as it stands today on a clean Windows machine?

Enough as an answer: one line each, and the name of the utility's owner.
```

- Why: OP-5 (`05:167`; `03:398`). You ruled that deployment uses the existing utility, amended (C-43, `CL:280`). The utility's owner in the Workpath team is the plan's independent check for this work (`03:146`, `03:213`); whether it builds as it stands is not established (`05:253`).
- Waits on it: the utility's amendment (phase 5), and its design note now (`03:146`).
- Default: a branch of its own repository; nothing reaches its main branch without your word (`05:167`).

### A16. The deployment utility: the printer password in existing Workpath jobs

```
While the utility is being extended for OXPd, may the way it stores and
passes the printer's administrator password for existing Workpath jobs be
changed as well, or must Workpath jobs keep behaving exactly as today?

Enough as an answer: "leave Workpath jobs as they are" or "may change".
```

- Why: OP-6 (`05:168`; `03:399`).
- Default: OXPd path only; Workpath jobs behave exactly as today (`05:168`).

### A17. The deployment utility: a Windows PC at every site

```
The utility runs on Windows only. In Workpath roll-outs today, is a Windows
PC for it always available at the customer's site, including sites that
otherwise run Linux?

Enough as an answer: yes or no, and one line if there have been exceptions.
```

- Why: OP-3 (`05:165`; `03:396`). The server ships for Linux and for Windows equally (C-17, `CL:104`); the deployment tool does not.
- Default: yes, acceptable, as for Workpath roll-outs today (`05:165`).

### A18. Languages shown on a printer

```
On a printer running the current OneDrive and SharePoint apps, with the
panel set to a language other than English (German, for example): do the
apps show their own screens in that language, or in English?

Enough as an answer: one photo of each app's first screen.
```

- Why: OP-21 (`05:183`; `03:414`). The code holds eight languages, but one line of the OneDrive build may strip all but English from the shipped app; nothing was built to test it.
- Waits on it: nothing before the language work finishes (`03:188`).
- Default: build all eight languages as the code has them (`05:183`).

### A19. Mailflow quick messages

```
Has any shipped version of Mailflow shown "quick messages" on the printer
panel? In the current source and in the compiled library the switch for them
is off.

Enough as an answer: yes or no. If yes, which version, or a photo.
```

- Why: the named case under open question 3 (`05:69`; `03:374`). The evidence that they are off is the code and the compiled file, not a printer.
- Default: left out (`05:69`).

### A20. Two looks at a Workpath printer

```
Two things we could read in the code but not see on a printer:
1. SharePoint 4.4.6: when scanning into a library, how many of the
   library's custom fields can be filled in at the panel? The manual says
   four; the code shows no limit.
2. OneDrive: pressing Back at the list of sites shows a sign-out
   confirmation screen in the code. Does it appear on a printer?

Enough as an answer: a photo of each screen.
```

- Why: what is left of the source read needs a Workpath printer and nothing else (`05:225`, items "4 custom fields" and "the sign-out confirmation screen"; `03:142`). New in this file as a question to a team; until now it waited for a printer in the lab.
- Default: follow the code (no limit of four; the confirmation screen is built).

### A21. Datasec's accounts and contact at HP

```
For the OXPd project we need to know what Datasec already has with HP.
1. Who at Datasec holds the HP developer portal account, and does Datasec
   have an HP App Center enrolment with a master administrator account?
   Whose are they?
2. Who is Datasec's contact at HP (a partner manager, a developer-support
   contact)? A name and a role.
3. Is there a signed agreement with HP, or accepted programme terms, that
   covers building and shipping solutions on HP printers? Where is it kept?
4. Has the HP account ever been issued a LaserJet Debug Bridge service key,
   or been used to download the OXPd 2 simulator or its guide?

Enough as an answer: a name for 1 and 2, a location for 3, yes or no for 4.
```

- Why: new in this file, and the direct result of your statement that a whole product team works on the Workpath apps (C-45, `CL:296`). The documents do not say whether Datasec holds an App Center enrolment (`B1:624`; `B3:498`), name no HP contact (the plan says only the product owner or an HP partner manager, `03:288`), and record that the agreements with HP were never seen (`05:257`). The old draft asked HP all of this. Search behind "not said anywhere": "master admin", "partner agreement" and "HP.io" each appear 0 times in `02`, `03`, `05` and `CLARIFICATIONS.md` (the same run finds "App Center" 1, 5 and 1 times in the first three).
- Waits on it: the brackets of H1, H2, H5 and H6 in LIST C. It costs time now.
- Default: nobody at Datasec is assumed to hold any of it; LIST C asks HP as before.

### A22. Anything newer than OXPd 1.8.4.1

```
Has HP given Datasec any OXPd 1.x SDK newer than 1.8.4.1 (a 1.9 release or
preview)?

Enough as an answer: yes or no. If yes, where the files are.
```

- Why: open question 12 (`05:135-139`), whose recommendation was "ask your HP contact". The team is asked first; block H7 in LIST C asks HP the part only HP knows (whether 1.9 exists).
- Waits on it: nothing unless the answer is yes, then the start of the older-printer work (`05:139`).
- Default: build on 1.8.4.1 (`05:137`).

### A23. What the team can lend the lab

```
The OXPd lab needs the following. Which of these does the team have and can
lend or set up? For each printer please give model and firmware version.
1. An HP printer on FutureSmart 6 (firmware 6.38.0.793 or later) that may be
   wiped.
2. An HP printer on FutureSmart 5 without the Workpath apps, and one on
   FutureSmart 4.7.
3. A printer running the current Workpath suite, in a test tenant.
4. Card readers: one of each product in the product's reader table.
5. A test Microsoft tenant set up as a customer's is: the HP Authentication
   Manager registration, Custom Security Attributes, Universal Print
   licences, the Azure services for the suite, an admin account with MFA.
6. Someone who can stand at the printers for tests (tap cards, sign in on a
   phone, power-cycle).

Enough as an answer: have or have not for each line, with model and firmware
for the printers.
```

- Why: kit items 4, 7, 8, 9, 10, 11 and 17, which the kit list assigns to "the team" or to "you or the team" (`05:192`, `05:195-199`, `05:205`). You said all the kit is in hand and not configured (C-42, `CL:272`); which items that covers is not in your note (`05:210`). New in this file as a question to a team. It also fills the bracket in H4 (which printers Datasec has tested on).
- Default: asked of you item by item on the kit checklist, as now.

### A24. When is a pilot good enough

```
When the Workpath apps go to a pilot customer, what defect level does the
team accept before calling the pilot a success (for example "no open
severity-1 defects, at most N severity-2")?

Enough as an answer: the rule the team uses today, or "none is written
down".
```

- Why: open question 14 (`05:147-150`). The plan says the threshold is set before the pilot starts and none is agreed (`03:125`, E6.6).
- Waits on it: the pilot (phase 6).
- Default: none set.
- Placement, said plainly: the plan's wording is that you set the threshold. It is put to the team because your message gives them commercial deployment (C-45) and they hold today's practice; the figure is still yours to accept. Move it back to your own five if you prefer.

### Two notices for the teams that own the code (not questions)

- **N1. Access keys in a committed state file of the older back end's infrastructure repository.** Location and count only are on the master list (`J`, comment 41405); no value is recorded anywhere. You said you will flag it to that team yourself (C-44, `CL:288`). Nothing in OXPd depends on it.
- **N2. The OneDrive app's signing keystore.** The keystore file at the root of the OneDrive source tree has its store password and key password written in clear text in the app's build file, and the file's own name is that same string, so any document that names the file prints the password (`J`, comment 41412). Recommended to the owning team there: change the keystore password and stop keeping it beside the keystore. You were told on the board. This file does not name the keystore file.

---

## LIST B. For the OXPd build team, up to MVP

**Who this team is today, said plainly: it is the coordinator's agents, working under the product owner. No person is on it yet.** The plan suggests one lead engineer and one engineer with lab access (`03:292`); nobody is named. Your message says the build will draw on the Workpath team and hand the product to them once ready (C-45, `CL:296`); until someone from that team joins, every item below is carried by agents on its default, and the tests that need hands wait for a person at a printer (`03:282`).

31 items: 15 decisions the build takes on a default (B1 to B15) and 16 tests (T1 to T16). None needs an answer from you to carry on. Where a decision changes what a customer gets, the note says when it comes back to you. "Needs" says whether the item can be settled with hardware (a printer, a card reader or the simulator machine), a tenant (the test Microsoft tenant), or neither.

### Decisions on a default

| # | Decision | Default the build takes | Settled by | Needs | Pointer and note |
|---|---|---|---|---|---|
| B1 | May the server keep an encrypted copy of a newer printer's administrator password? | Never stored on newer printers | Test T1 (does the printer's access token survive a reboot), then the fleet work of phase 5 | Hardware | Open question 2, `05:59-63`; `02:810`; risk R29, `02:970`. Your tap was "Store it encrypted" (C-24, `CL:146`), and the option's own text discards it on newer printers. If T1 shows the token is lost on reboot, a stored copy as a per-site choice becomes the practical answer and comes back to you with the result |
| B2 | The scope rule: release 1 matches what the Workpath apps ship today, and no more | Yes | The deviation register (WP6.7, `03:223`) and the parity gate (`03:125`, E6.8) | Neither | Open question 3, `05:65-69`. It is a reading of your "Full match of everything" (C-16, `CL:98`), accepted as a default for now (C-32, `CL:194`). The cases where it bites are asked of the team as facts: A2, A3, A19 |
| B3 | The design choices that differ from Workpath and that nothing forces: card emulation and app settings move from the panel to the server console; job counts go to Universal Print for all three printer types; the server may write a refreshed sign-in token back to the directory in No-MFA mode; the help link on error screens is shown, not opened | As designed; the token write-back waits for test T5 | WP6.7, the deviation register (`05:233`) | Neither, except the write-back (tenant and a Workpath printer) | Open question 6, `05:84-88`. Placed with the build team because Datasec controls the build (C-45). Unchanged: the plan still takes the register to you for approval before phase 3 exits (`03:107`); that gate is the plan's, and this file does not remove it |
| B4 | One central server for several sites | Not offered in release 1; one server per site | Nothing to build | Neither | Open question 11, `05:129-133`; `02:846`. Your tap was "On each site's network" (C-26, `CL:158`) |
| B5 | The deployment utility is the operator's tool; the server does the work on each printer | The first: the utility starts and follows jobs, the server carries them out | WP0.10 (design note, `03:146`), then WP5.8 (`03:213`) | Neither | OP-1, `05:163`; `03:394`. The server must keep each printer's token, records and repair loop. Reviewed by the utility's owner (A15) |
| B6 | "Use the deployment utility" does not cover installing the server itself | The server keeps its two packagings | WP5.1 (`03:206`) | Neither | OP-2, `05:164`; C-43, `CL:280`; C-17, `CL:104` |
| B7 | Batch onboarding is started from the utility only; the console shows status and repairs one printer | The utility only | WP5.3 (`03:208`) | Neither | OP-4, `05:166` |
| B8 | The phone-link relay needs one address on each customer's gateway that accepts a request without a token, and a second update route for customers who deployed by script | Go ahead, with the test described in the plan | WP3.2 (`03:178`); test T7 | Tenant | OP-12, `05:174`; `03:405`. You ruled the Azure back end "May change" (C-27, `CL:164`). It changes a product the Workpath team runs: their numbers (A7, A8) and their review are wanted before any gateway release, and customer-side Azure releases stay yours to approve (`03:285`) |
| B9 | May the earlier OXPd 1 build's register and unregister tools be used once as a lab probe? | No: the tests are written fresh | Nothing to build | Neither | OP-17, `05:179`; `A10:338`. They switch certificate checks off |
| B10 | A SharePoint library opened from the OneDrive tile and from the SharePoint tile: does each tile keep its own behaviour of today when scanning into it? | Yes: each tile matches its own Workpath app exactly | WP3.10 (`03:186`) | Neither | OP-19, `05:181`; `03:412`. Follows from C-16; the consequence has not been put to you |
| B11 | The Windows machine for HP's two simulators: a machine in the Azure subscription the HPSM project uses, your old Windows PC, or an emulator on the Mac | None chosen | WP0.1 (`03:137`): measure whether an Azure machine can run VMware inside it, then choose | Hardware | The master list's "Windows machine" item (`J`); your notes C-35 and C-36 (`CL:218`, `CL:224`). **It costs time now:** no simulator work starts without it (`03:36`). An Azure machine is spend: its size and cost go to you before it is created (`CL:226`) |
| B12 | The size of the widened OneDrive work package (four places, not one) | UNSIZED; the earlier size M was for My Drive only | An estimate by the build team before WP3.10 is scheduled (`03:186`) | Neither | `05:20`, `05:258`; `02:217`. New in this file as a build-team item. The four places themselves are not a question: they follow from C-16 |
| B13 | Is Teams quick access switched off in every shipped build, like SharePoint's? | The two Teams rows stay in the plan until the rest of the code is read | A source read at the start of WP3.5 (`03:181`): 9 of 16 places are unread | Neither | `05:256`. New in this file as a build-team item |
| B14 | HP's older SDK guide has a clause on reverse engineering of the protocol between HP's library and the printer. The build makes older-printer test stubs from the service descriptions inside HP's library | The work package is unchanged; nobody has settled whether the clause bears on it | HP's answer to H6 point 6 in LIST C, or a reading by someone qualified. Not by the build team | Neither | Risk R32, `02:973`; `05:223`, `05:257`; `C1:316`. This row does not say the work is permitted and does not say it is not. Your ownership statement (C-45) is about Datasec's products and this build; it is not read here as a statement about HP's licence terms |
| B15 | What "MVP" contains, and the point of hand-over to the Workpath team | The plan is unchanged: one release, release 1, a full match (C-16) | A one-page proposal from the build team, for your ruling (P4) | Neither | C-45, `CL:296`. Neither term is defined in `02`, `03` or `05` (search and its control are under P4). New in this file |

### Tests (phase 0)

Thirteen are the plan's own tests (`03:54-66`; work package WP0.2, `03:138`); three more are checks on the test tenant that came out of the source reads. Agents write the code and the script; each needs a person where "Hardware" is marked (`03:282`). None has been run (`05:240`).

| # | What it settles | Default until it has run | Needs | Pointer |
|---|---|---|---|---|
| T1 | Newer printers: install order, whether the access token survives a reboot, a power loss and a firmware update, which card-reader record type the firmware accepts, what the panel's browser sends | The install order of the design; B1's default | Hardware (a newer printer in developer mode, or the simulator) | S1, `03:54`. Three of HP's six open points (H8 points 1 and 6, and part of 2) are measured here |
| T2 | Older printers: can the printer call the server's endpoints on the chosen framework, on Linux and on Windows | Yes; if either half fails, a Java helper is added | Hardware (an older printer) | S2, `03:55` |
| T3 | Card readers: does each reader give the same card string on both printer generations as on Workpath | Readers a Workpath printer cannot decode are left out | Hardware (readers, a Workpath printer) | S3, `03:56`; C-23, `CL:140` |
| T4 | Microsoft's sign-in page on a newer printer's panel: does it work, and are two users' sessions kept apart | Not offered on the panel; phone code or phone link is the baseline (C-29) | Hardware and tenant | S4, `03:57`. H8 points 4 and 5 |
| T5 | Can the server redeem a sign-in token issued to a Workpath printer, and the reverse | The server does not write tokens back until the reverse passes | Tenant and a Workpath printer | S5, `03:58` |
| T6 | Printing paths on both generations with certificate checks on; printing while a user is at the panel | Failures recorded per model | Hardware | S6, `03:59`. H8 point 3 |
| T7 | Sign-in on the phone under the tenant's access policies; the relay; and the two untested links behind P3 (can an ordinary user get a gateway token; is the per-user secret the same each time) | P3's default | Tenant, a phone, a Workpath printer | S7, `03:60`; `05:116` |
| T8 | Newer printers: upgrading an installed solution; does an uninstall leave nothing | "Install new, verify, remove old" | Hardware | S8, `03:61`; `02:834`. H8 point 2 |
| T9 | Pull printing: which user value returns a user's own jobs | Workpath's rule, exact match | Tenant | S9, `03:62` |
| T10 | Two servers: how long a printer keeps calling the old address after a switch | The 2-minute target; replaced by the measured figure if it fails | Hardware and two hosts | S10, `03:63` |
| T11 | Reporting: can the new printers fill the same record the customer's reports read | The field map drafted from the Azure offer's template | Tenant (the no-hardware half is under way, `05:235`) | S11, `03:64` |
| T12 | Which document converter prints mail attachments as Workpath does, in both packagings | None chosen | A Workpath printer for the comparison | S12, `03:65` |
| T13 | Universal Print: can a lab host get a registration token with Datasec's registration; which call deletes a cloud printer | Removal stays a report of orphaned printers | Tenant; runs only after A4 is answered | S13, `03:66` |
| T14 | Do the Microsoft permissions a customer has granted cover OneDrive's "Shared with me", where files sit in other users' drives | The permission list and the consent text are unchanged | Tenant | OP-20, `05:182`; `03:413`. A test, not a decision |
| T15 | The format of the phone app's sign-in message, by capturing one | A placeholder in the gateway stand-in | Tenant and a phone; not needed if A9 brings the source | `05:234`; `03:143` |
| T16 | How long the address of a file's thumbnail image stays valid | None | Tenant | `05:225`; `03:142` |

---

## LIST C. For HP

Eight asks, each a block that can be sent by itself. Only what HP alone can answer: its validation and signing service, its developer access, its firmware and its dates, its licence terms for its own libraries and documents, and how its platform behaves. Nothing here asks HP's leave for Datasec's own product or design.

**How each was re-judged against your statement (C-45).** The test applied to every sentence: does it ask HP for permission about something Datasec owns (the apps, the authentication product, this project, the design of the build), or does it ask about something HP owns?

| Ask | Verdict | What changed |
|---|---|---|
| H1 | Kept, reworded; one question falls away | Gone: "Is an OXPd solution whose server calls Microsoft 365 ... acceptable to HP on OXPd 2 and on OXPd 1.x?" and the sentence "my understanding was that HP is comfortable with this approach". Both asked HP to approve Datasec's design; on the older printers HP has no approval step at all (`C1:405`). Kept: the written record of what HP said, and the two points that are about HP's own validation |
| H2 | Kept, opening and point 1 reworded | Whether Datasec is enrolled is asked of the Datasec team first (A21). HP is asked what only HP knows: whether that enrolment covers OXPd 2, the contact, the route, the paperwork |
| H3 | Kept, unchanged | HP's firmware, platform versions, signing service and turnaround are HP's |
| H4 | Kept, unchanged | HP's validation rule. The bracket (which printers Datasec has) is now filled from A23 |
| H5 | Kept, unchanged | HP's developer access. The account in point 1 is now named from A21 |
| H6 | Kept; point 2 reworded, point 6 kept as HP's | Gone from point 2: "Is that acceptable to HP for a production solution". Writing its own client code is Datasec's design. Kept, as questions about what HP owns: whether HP's terms for its published specifications put a condition on that use, and whether HP's validation needs HP's library. Point 6 is HP's term about HP's library and stays HP's to answer |
| H7 | Kept, unchanged | Whether a newer HP SDK exists is HP's. Whether Datasec already has it is asked of the team first (A22) |
| H8 | Kept, unchanged | How HP's firmware behaves. Each point also has a test in LIST B |

**Order.** H5 first: it costs time now. H2 next: the plan routes H3 and H4 through the contact it produces (`03:47`), and H6 and H8 need the same person or channel. A21 (LIST A) should come back before any of them goes, because it may supply the contact and the account. H1 goes to whoever gave you the confirmation (P1). H7 is independent.

### H1. A written record of HP's position, and eligibility for OXPd 2 validation

```
Subject: Datasec: written record of HP's position on our OXPd solution, and OXPd 2 validation

Hello [name],

Datasec is building an OXPd version of our HP Authentication Manager suite
(sign-in with Microsoft Entra, plus our Mailflow, Teams, OneDrive, SharePoint
and Universal Print applications). It is a server on the customer's own
network. The printer never talks to Microsoft: our server does, and the panel
only shows pages our server serves.

[When and how HP told us: for example "When we spoke on <date>" or "In your
e-mail of <date>"], HP told us [what was said, in one line]. Could you put
that in writing, so that we can keep it on file and refer to it when we
submit for validation? Two points matter to us, both about HP's own process:

1. Is such a solution eligible for HP validation and signing on OXPd 2, on
   the same terms as any other OXPd 2 solution?
2. We are aware of a 2023 statement on the developer forum that OXPd does not
   support direct integration with public cloud services and that Workpath is
   the route for that. Is our reading correct that this concerned the printer
   connecting to the cloud service itself, and that HP's validation will not
   apply it to a solution where only the solution's server does?

A short reply by e-mail is all we need.

Thank you,
[name]
```

**What Datasec needs back:** one written reply; yes or no to each of the two points. **When it starts to cost time:** it is an exit condition of phase 0 ("HP's written confirmation filed", `03:71`), and it is wanted before the first submission so that a different HP reviewer does not reopen the 2023 statement (risk R2, `02:943`).

**Note for the product owner only.**
- Why it is asked: the newer-printer track was unblocked by your answer "Yes, HP confirmed" (C-30, `CL:182`; decision D33, `02:930`). The confirmation is not in the library (`05:241`). The 2023 statement is at `B3:22`.
- What C-45 changed: the old point 1 is gone (see the table above). The message no longer asks whether the approach is acceptable. It asks for a record of what was said and for two facts about HP's validation, which is HP's service and sits on the release path (risk R1, `02:942`). That dependency is real and is not weakened: a production bundle for newer printers installs only if HP signs it (`B1:134`).
- The brackets are yours (P1). I do not know when, how, from whom or in what words the confirmation came, so the message does not say. If nothing was said about signing, point 1 is a new question to HP and not a confirmation.
- Default if HP does not answer: the design carries on as now, on your answer C-30, with the risk recorded, and the gap is put to you again before the first submission.
- Who at HP: the documents name no person (`02:959` says only "the HP contact behind C-30's confirmation").

### H2. HP App Center and validation for OXPd 2, and a named contact

```
Subject: Datasec: HP App Center, OXPd 2 validation and signing, and a contact

Hello [name],

Datasec intends to submit an OXPd 2 solution for HP validation and signing.
[What Datasec already holds with HP, from our own records: for example "We
hold an HP App Center enrolment under <account>" or "We do not yet have an
App Center enrolment".] Before we submit, could you help us with the
following?

1. Does [that enrolment] cover OXPd 2 solutions? If not, or if we have none,
   what are the steps, who at Datasec has to hold the master administrator
   account, and how long does enrolment usually take?
2. Who is our contact at HP for OXPd 2 validation and signing questions, and
   what is the right channel for them (the developer forum, a support ticket,
   or a named person)?
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

**What Datasec needs back:** whether the enrolment covers OXPd 2; a named contact or channel; the steps and the paperwork. **When it starts to cost time:** the plan starts the submission track in phase 0 and submits an early bundle as soon as the first slice works (risk R1, `02:942`); H3, H4, H6 and H8 are meant to go through the contact this one produces (`03:47`).

**Note for the product owner only.**
- Why it is asked: a production bundle for newer printers must be validated and signed by HP through the App Center, which needs a company enrolment and a master administrator account (`B1:134`). It is kit item 14 (`05:202`) and work package WP0.5 (`03:141`).
- What C-45 changed: the old text asked HP "Is Datasec already enrolled" as its first question. Datasec's own product team may know that (A21); the bracket carries their answer, and HP is asked only what HP decides. If A21 comes back empty, use the second form of the bracket and the block reads as before.
- Points 3 and 4 are partly answered by HP's publishing page as the library holds it (`B1:150`). They are asked because the same page marks every platform version "Not Supported" for validation (`B1:487`), so what it describes may not be what happens today. Strike them for a shorter message.
- An optional sixth line, left out of the box: "What is the HP Token Proxy that the App Center issues client credentials for, and does an on-premises solution need it?" HP's page mentions it once and no guide explains it (`B1:153`); the design ignores it (`03:350`). Nothing waits on it.
- Default if HP does not answer: development continues on the simulator and on a printer in developer mode only; nothing reaches a customer's newer printer (`B3:498`).
- Who at HP: not named anywhere in the documents (`03:288` says only the product owner or an HP partner manager). A21 asks the team for the name.

### H3. Dates for the four things a customer installation on FutureSmart 6 depends on

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

**What Datasec needs back:** a date or an estimate for each of the four, in writing; for 5 and 6 a date or "not known". **When it starts to cost time:** not before the release gate, with one exception: no date for the newer printers should be given to any customer or partner until these are in (`05:18`). If any of the four is late at the release gate, release 1 waits or the older printers ship first, and that choice is yours then (`03:267`; `02:930`).

**Note for the product owner only.**
- Why it is asked: these are the four undated items of decision D33 (`02:930`; `02:20`; `03:11`; `05:18`); WP0.5 asks for them (`03:141`).
- What C-45 changed: nothing. Firmware, platform versions and the signing service are HP's.
- Sources of the facts in the message: beta firmware not for customers (`02:930`); the platform table (`B1:487`); the rejected signed bundle and HP's last word of 17 November 2026 (`B3:18`; `B3:344`); the model list "will be defined prior to production release" (`B1:491`); no production date, and a direct forum question of February 2024 without a reply (`B3:378`).
- The forum thread in point 3 is another partner's. The message names no partner and no person; keep it that way.
- Default if HP does not answer: no date is planned or promised for the newer printers; both generations are still built for the same release; the plan carries sizes, not dates (`03:13`).
- Who at HP: through the contact H2 produces (`03:47`). One HP forum reply says FutureSmart 6 availability goes "via the PSM" (`C2:178`).

### H4. A first signing round with fewer than seven tested printer groups

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

**What Datasec needs back:** yes or no to a reduced first round, and if no, what HP can offer for the missing groups. **When it starts to cost time:** at the end of phase 1. The exit point E1.9 needs HP's written answer by then; if HP requires all seven, the first submission moves to when the printers are borrowed, and that date comes to you (`03:89`).

**Note for the product owner only.**
- Why it is asked: HP's rule is one tested printer from each of groups A to E, and F and G as well for a solution with sign-in (`B1:136`; `03:89`). Phase 0 supplies one (`05:214`). The design's rule is that no group is declared tested when it was not (`02:812`; risk R10, `02:951`).
- What C-45 changed: nothing in the questions. The bracket (which printers Datasec has) is filled from A23 and P2. Do not write that Datasec holds a FutureSmart 6 printer unless it does.
- Questions 3 and 4 are not in the plan's wording of the ask; they are there because HP's page does not say either way and both change how many printers must be borrowed. Strike them for the ask exactly as the plan words it.
- Default if HP does not answer: the first signing round waits for the printers; nothing is submitted with an untested group declared (`02:951`; `03:89`).
- Who at HP: the contact from H2.

### H5. Lab access: developer key, simulator, its guide, pilot firmware

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

**What Datasec needs back:** the key (or confirmation the account can create one), a download location, the guide, and the route to pilot firmware. **When it starts to cost time:** now. These are kit items 3, 5 and 6 (`05:191`, `05:193`, `05:194`); without the key the lab printer cannot be put into developer mode, and tests T1, T4, T8 and the newer-printer halves of T3 and T6 in LIST B cannot start (`03:263`).

**Note for the product owner only.**
- Why it is asked: the second item of the master list's group "To raise with HP" (`J`). Sources: the key and what enabling needs (`B1:207`); the wipe on switching (`B1:208`); the simulator image is not in the library (`B3:401`); the guide returned 403 for your account (`B3:402`; `03:37`); the pilot firmware and how Datasec obtains it are unknown (`B3:404`; `03:39`).
- What C-45 changed: nothing in the questions; these are HP's developer access. One thing before sending: A21 asks the Datasec team whether their HP account already has a key or the simulator. If it does, points 1 and 2 are answered at home and can be struck, and the account in point 1 is theirs to name.
- Points 1 and 2 may need no HP person at all: the kit list has the key as yours "from HP's developer site" (`05:193`), and the image is a portal download. Try the portal first; send the message for whatever the portal refuses.
- The optional line in point 4 is there because which printer you hold is not established (P2).
- Default if HP does not answer: the work that needs no hardware carries on (`05:216-236`); the tests on newer printers wait.
- Who at HP: the developer portal and its support forum for points 1 to 3 (`B1:207`). For firmware, "via the PSM" is HP's own phrase (`C2:178`); who that is for Datasec is asked in A21.

### H6. Licence terms: what HP's terms say about what Datasec ships

```
Subject: Datasec: licence terms for the OXPd 2 SDK and the OXPd 1.8.4.1 libraries in a shipped product

Hello [name],

We want to be sure that what we ship is within HP's terms. The OXPd 2 SDK
package we downloaded contains third-party notices but no statement from HP
on what a partner may do with the SDK. Could you point us to the governing
terms, and answer the following?

OXPd 2
1. Which agreement governs a partner's use of the OXPd 2 SDK during the beta
   and after it, and where can we read it?
2. We do not ship HP's OXPd 2 client library. Our server uses client code
   that Datasec writes itself from the interface specifications HP publishes
   with the SDK.
   a. Do the terms under which HP publishes those specifications place any
      condition on that use?
   b. Does HP validation and signing require, or check for, HP's own client
      library in a solution?
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
   card reader events, statistics, scan notifications). We build those
   endpoints ourselves, from the service descriptions delivered inside the
   HP library. The licence section of the SDK user guide restricts what a
   licensed user may do with the library's source and with the protocol
   between the library and the printer. Does that section apply to building
   endpoints from those service descriptions, and where can we read the
   full terms?

A pointer to the documents is enough if these are already written down.

Thank you,
[name]
```

**What Datasec needs back:** the name and location of the governing terms; an answer to points 2a, 2b, 3, 5 and 6. **When it starts to cost time:** now for point 2. The newer-printer clients are being written from HP's specifications in the work that has started (`05:223`; `03:140`). If HP's terms or its validation require HP's own library, the newer-printer adapter goes back to HP's library and to waiting for HP's production SDK.

**Note for the product owner only.**
- Why it is asked: your answer on HP code rights was "As assumed" (C-11, `CL:68`), and the assumption is the plan's, not HP's: reimplement the logic, ship HP's older library unchanged, ship HP's newer library only after a production SDK (`03:325`). The SDK package holds no partner terms at all (`B3:326`); the terms must be in a portal or partner agreement nobody on the project has read (`B3:406`; `05:257`). Risk R16 (`02:957`). A21 asks the Datasec team where that agreement is: if they have it, point 1 may be answered at home.
- What C-45 changed in point 2: the old text asked "Is that acceptable to HP for a production solution". Whether Datasec writes its own client code is Datasec's design, so that sentence is gone. What is kept is what HP owns: the terms on HP's own specifications (2a) and what HP's validation checks (2b). HP has said it "tests and commits to supporting the signed libraries" and has no position on generated clients (`B3:295`); the message asks and does not claim HP agreed.
- **Point 6 is kept as HP's, and deserves your eye before it is sent.** HP's older SDK guide, as the report gives it, says licensed users may not use the library source "or any other means of reverse engineering" on the protocol between library and printer (`C1:316`). The build makes test stubs from the service descriptions inside HP's library (`03:140`) and hosts the printer-facing endpoints on a framework HP does not demonstrate (`02:363`). Whether the two conflict is not settled by anyone (risk R32, `02:973`). **Your statement that Datasec owns the build does not answer it:** the clause is a term on HP's library, and only HP, or someone qualified to read the licence, can say what it covers. So the point stays a question, and its wording neither says the work is permitted nor that it is not. Leaving point 6 out of the message, or having the clause read by someone qualified first, is a legitimate choice and is yours.
- Point 5 is mostly answered by HP's guide already (`C1:316`); it is asked because the 1.8.4.1 Java library carries no licence text and two different files share one name (`02:49`). Strike it if you are content with the guide.
- Default if HP does not answer: as today. Own clients for newer printers; HP's older library shipped unchanged and identified by checksum; HP's newer library in the lab only (`02:957`; `05:223`).
- Who at HP: not stated. The contact from H2, or whoever manages Datasec's agreement with HP (A21).

### H7. OXPd 1.x: is there anything newer than 1.8.4.1?

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

**What Datasec needs back:** yes or no to 1.9, and a download if yes. **When it starts to cost time:** only if the answer is yes, and then at the start of the older-printer work (`05:139`).

**Note for the product owner only.**
- Why it is asked: open question 12 (`05:135-139`). Your brief says "OXPD 1, whatever the latest version is" (C-1, `CL:9`); the library's newest is 1.8.4.1, and HP called 1.9 "soon to be released" in March 2026 (`C1:405`). The same roadmap item has been "soon" since 2017 (`C2:248`), which is why the default treats 1.9 as absent.
- What C-45 changed: nothing in the questions. Whether Datasec already holds something newer is asked of the team first (A22). If they do, or if you know from HP that nothing newer exists, this block is not needed.
- Point 4 is an addition: HP said in 2019 that there is "no specified product lifecycle policy for OXPd libraries" (`C1:429`). Strike it if unwanted.
- Default if HP does not answer: build on 1.8.4.1 (`05:137`; `03:340`).
- Who at HP: any HP developer-support channel; the March 2026 statement was a forum reply (`C1:405`).

### H8. Six technical points HP's OXPd 2 guides leave open

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

**What Datasec needs back:** one line per point. **When it starts to cost time:** it does not, by itself: each point has a test in LIST B that settles it on a real printer. An early answer shortens those tests and says whether what is measured is intended behaviour or an accident of one beta.

**Note for the product owner only.**
- Why it is asked, and the test that settles each: (1) the guides say the token "may need to be reissued" (`B1:536`); it decides B1; test T1. (2) Same-id upgrade is undocumented (`B1:195`; `02:834`); test T8. (3) The guide and the demo disagree (`B1:531`); test T6. (4) Cookie behaviour between users is undefined (`B1:580`); test T4. (5) Which certificate store the browser uses for third-party sites is not stated (`B1:609`); test T4. (6) Release note against guide (`B3:337`; `02:379`); test T1.
- What C-45 changed: nothing. These are facts about HP's firmware.
- This is the least urgent block and the most technical. It can be posted on the developer forum instead of being sent by you; a forum post is still a message to HP, so it is still yours to release.
- Default if HP does not answer: the tests decide, as planned (`03:54-66`).
- Who at HP: the OXPd 2 developer forum or a partner engineer (`B1:634`).

---

## ANSWERED OR CLOSED: asked of nobody

- **Answered by HP's published documents (12 rows).** The table "ANSWERED BY THE DOCUMENTS" of `registers/HP_QUESTIONS_DRAFT.md` (its lines 403 to 420) stands as it is; its pointers to the reports are unchanged, and its pointers into `02`, `03` and `05` are of the earlier copies. Row 12 (which generation an M577 is) is only partly answered and is also P2.
- **Answered by you on 2026-11-20:** the word to start the no-hardware work (C-42, `CL:272`); the SharePoint source (C-33) and the gateway source (C-40), both received and read (`05:91-93`); sensitivity labels left out (C-38, `CL:240`); deployment by the existing utility, amended (C-43, `CL:280`); the OneDrive source read, done and second-read (`05:225`).
- **Closed by an earlier ruling:** other vendors' solutions beside ours on a printer (C-19, `CL:116`: "No, ours only"); the four places of the OneDrive app, which follow from "Full match of everything" (C-16; `05:20`), with only their size open (B12).
- **Not asked, on a default:** whether HP can supply interim firmware for older printers (`C2:267`). The design tests against public firmware, and your answer on test devices was "As assumed" (C-6, `CL:38`). Say so if it should go to HP and a line is added to H5.

---

## TABLE OF MOVES

Every item of the old draft and of the master list, with its old place and its new one. Built and counted by program from one list of rows: the items in equal the items out in each table. An item that is asked in two places is counted once, under its first place; the second is in brackets. The two tables overlap: most of the master list's items are also in the old draft's section NOT FOR HP.

### Table 1. The old draft (`registers/HP_QUESTIONS_DRAFT.md`): 90 items in, 90 out

Items in: the 38 numbered points of asks H1 to H8, 1 optional line, 12 rows answered by the documents, 37 items not for HP, 2 items that touch HP and were deliberately not asks. **Out: For the product owner himself 4; LIST A 21; LIST B 10; LIST C 38; Answered 13; Closed by a ruling or not asked 2; Notice 1; Fell away (C-45) 1. Sum 90.**

Of the 37 items the old draft held as "the product owner's or his team's": **For the product owner himself 4; LIST A 21; LIST B 10; Answered 1; Notice 1. Sum 37.** Of the 39 lines addressed to HP: **LIST C 38; Fell away (C-45) 1. Sum 39.** 5 of those kept are now asked of the Datasec team first.

| # | Item | Old place | New list | New place | Reason |
|---|---|---|---|---|---|
| 1 | H1 point 1: is the approach acceptable to HP on OXPd 2 and OXPd 1.x | Ask to HP | Fell away (C-45) | none | C-45: it asked HP's leave for Datasec's own design; on older printers HP has no approval step |
| 2 | H1 point 2: eligible for HP validation and signing on OXPd 2 | Ask to HP | LIST C | H1 point 1 | HP's validation service |
| 3 | H1 point 3: the 2023 forum statement | Ask to HP | LIST C | H1 point 2 | HP's own statement; reworded to ask how HP's validation applies it |
| 4 | H2 point 1: is Datasec enrolled in HP App Center | Ask to HP | LIST C | H2 point 1 (team first: A21) | Reworded: Datasec's team is asked what Datasec holds; HP is asked whether it covers OXPd 2 |
| 5 | H2 point 2: the HP contact and channel | Ask to HP | LIST C | H2 point 2 (team first: A21) | Only HP names its validation contact; the team may know Datasec's existing one |
| 6 | H2 point 3: the submission route | Ask to HP | LIST C | H2 point 3 | HP's process |
| 7 | H2 point 4: what HP wants with a submission | Ask to HP | LIST C | H2 point 4 | HP's process |
| 8 | H2 point 5: agreement, terms or fee before a first submission | Ask to HP | LIST C | H2 point 5 | HP's terms |
| 9 | H2 optional line: the HP Token Proxy | Optional line under an ask to HP | LIST C | H2 note (optional, outside the box) | HP's service; nothing waits on it |
| 10 | H3 point 1: production FutureSmart 6 firmware | Ask to HP | LIST C | H3 point 1 | HP's firmware, platform and dates; unchanged |
| 11 | H3 point 2: a platform version validation accepts | Ask to HP | LIST C | H3 point 2 | HP's firmware, platform and dates; unchanged |
| 12 | H3 point 3: a signing service whose output installs | Ask to HP | LIST C | H3 point 3 | HP's firmware, platform and dates; unchanged |
| 13 | H3 point 4: turnaround | Ask to HP | LIST C | H3 point 4 | HP's firmware, platform and dates; unchanged |
| 14 | H3 point 5: the list of supported models | Ask to HP | LIST C | H3 point 5 | HP's firmware, platform and dates; unchanged |
| 15 | H3 point 6: a production SDK date | Ask to HP | LIST C | H3 point 6 | HP's firmware, platform and dates; unchanged |
| 16 | H4 point 1: a first round with fewer than seven groups | Ask to HP | LIST C | H4 point 1 | HP's validation rule; unchanged |
| 17 | H4 point 2: help with printers of the missing groups | Ask to HP | LIST C | H4 point 2 | HP's validation rule; unchanged |
| 18 | H4 point 3: does a simulator test count | Ask to HP | LIST C | H4 point 3 | HP's validation rule; unchanged |
| 19 | H4 point 4: does latest firmware mean pilot firmware | Ask to HP | LIST C | H4 point 4 | HP's validation rule; unchanged |
| 20 | H5 point 1: the debug bridge service key | Ask to HP | LIST C | H5 point 1 (team first: A21) | HP's developer access; the team is asked whether its account has a key |
| 21 | H5 point 2: the simulator image | Ask to HP | LIST C | H5 point 2 | HP's developer access; unchanged |
| 22 | H5 point 3: the simulator guide and the limited-access section | Ask to HP | LIST C | H5 point 3 | HP's developer access; unchanged |
| 23 | H5 point 4: pilot firmware | Ask to HP | LIST C | H5 point 4 | HP's firmware; unchanged |
| 24 | H6 point 1: which agreement governs the OXPd 2 SDK | Ask to HP | LIST C | H6 point 1 (team first: A21) | HP's terms; the team is asked where Datasec's agreement is |
| 25 | H6 point 2: own clients written from HP's specifications | Ask to HP | LIST C | H6 point 2 (a and b) | Reworded by C-45: the permission sentence is gone; HP's terms on its specifications and what validation checks are kept |
| 26 | H6 point 3: shipping HP's library once a production SDK exists | Ask to HP | LIST C | H6 point 3 | HP's library and terms; unchanged |
| 27 | H6 point 4: confidentiality terms of the beta | Ask to HP | LIST C | H6 point 4 | HP's terms; unchanged |
| 28 | H6 point 5: shipping the 1.8.4.1 libraries unchanged | Ask to HP | LIST C | H6 point 5 | HP's library and terms; unchanged |
| 29 | H6 point 6: own endpoints from the service descriptions; the reverse-engineering clause | Ask to HP | LIST C | H6 point 6 (tracked as B14) | Kept as HP's: a term on HP's library; C-45 is not read as a statement about it |
| 30 | H7 point 1: is OXPd 1.9 available | Ask to HP | LIST C | H7 point 1 (team first: A22) | HP's SDK; the team is asked whether Datasec already holds it |
| 31 | H7 point 2: a date and what 1.9 changes | Ask to HP | LIST C | H7 point 2 | HP's SDK and policy; unchanged |
| 32 | H7 point 3: lowest firmware and the no-approval rule | Ask to HP | LIST C | H7 point 3 | HP's SDK and policy; unchanged |
| 33 | H7 point 4: support period of OXPd 1.x | Ask to HP | LIST C | H7 point 4 | HP's SDK and policy; unchanged |
| 34 | H8 point 1: tokens after a reboot | Ask to HP | LIST C | H8 point 1 (test T1 in LIST B) | HP's firmware behaviour; unchanged |
| 35 | H8 point 2: upgrading an installed solution | Ask to HP | LIST C | H8 point 2 (test T8 in LIST B) | HP's firmware behaviour; unchanged |
| 36 | H8 point 3: printing in priority print mode | Ask to HP | LIST C | H8 point 3 (test T6 in LIST B) | HP's firmware behaviour; unchanged |
| 37 | H8 point 4: browser session data between users | Ask to HP | LIST C | H8 point 4 (test T4 in LIST B) | HP's firmware behaviour; unchanged |
| 38 | H8 point 5: certificate trust in the embedded browser | Ask to HP | LIST C | H8 point 5 (test T4 in LIST B) | HP's firmware behaviour; unchanged |
| 39 | H8 point 6: the card reader registration record | Ask to HP | LIST C | H8 point 6 (test T1 in LIST B) | HP's firmware behaviour; unchanged |
| 40 | Answered row 1: do FutureSmart 6 printers run OXPd 1.x solutions | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 41 | Answered row 2: does an OXPd 1.x solution need HP approval | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 42 | Answered row 3: lowest firmware for the full OXPd 1.8 feature set | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 43 | Answered row 4: firmware OXPd 2 Beta 10 needs | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 44 | Answered row 5: may HP's OXPd 1.x library be shipped | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 45 | Answered row 6: how developer mode is switched on | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 46 | Answered row 7: may developer mode be used at a customer | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 47 | Answered row 8: the install route for an OXPd 2 bundle | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 48 | Answered row 9: which printer groups must be tested | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 49 | Answered row 10: what the two simulators need | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 50 | Answered row 11: can a printer fail over between two servers | Answered by the documents | Answered | Answered or closed | HP's published documents answer it |
| 51 | Answered row 12: which OXPd generation an M577 is (partly answered) | Answered by the documents | Answered | Answered or closed (also P2) | HP's published documents answer it; the unit's own firmware is read from its panel |
| 52 | The card key | Not for HP: needs an answer first | LIST A | A1 | The team that builds the shipped apps knows how their builds get the key |
| 53 | The printer on hand, its firmware, may it be wiped | Not for HP: needs an answer first | For the product owner himself | P2 | The printer is in the product owner's hands (C-34, C-39) |
| 54 | The Windows machine for the simulators | Not for HP: needs an answer first | LIST B | B11 | A lab choice the build makes after one measurement; spend goes to the product owner |
| 55 | cc-api | Not for HP: needs an answer first | LIST A | A10 | A fact about the team's own repositories |
| 56 | The empty repository OXPD1 | Not for HP: needs an answer first | LIST A | A11 | A fact about the team's own repositories |
| 57 | The start of building | Not for HP: needs an answer first | Answered | Answered or closed | Given on 2026-11-20 (C-42) |
| 58 | Question 1: what "Yes, HP confirmed" covers | Not for HP: open on a default | For the product owner himself | P1 | Only he knows what HP told him |
| 59 | Question 2: the admin password on newer printers | Not for HP: open on a default | LIST B | B1 | Waits on a test the build runs (T1) |
| 60 | Question 3: the meaning of "full match" | Not for HP: open on a default | LIST B | B2 | The build's scope rule on its default; the cases are facts asked of the team (A2, A3, A19) |
| 61 | Question 4: OneDrive personal | Not for HP: open on a default | LIST A | A2 | Whether it is shipped or sold is a fact the team holds |
| 62 | Question 5: the HP Advance and LRS VPSX sign-in role | Not for HP: open on a default | LIST A | A3 | Whether any customer uses it is a fact the team holds |
| 63 | Question 6: design choices that differ from Workpath | Not for HP: open on a default | LIST B | B3 | C-45: Datasec controls the build; the plan's approval gate before phase 3 exits is kept |
| 64 | Question 9: the Universal Print registration | Not for HP: open on a default | LIST A | A4 | Datasec's own registration; the team can check |
| 65 | Question 10: QR sign-in without MFA | Not for HP: open on a default | For the product owner himself | P3 | A ruling on product risk, reserved to him; its two tests are T7 |
| 66 | Question 11: one central server for several sites | Not for HP: open on a default | LIST B | B4 | A design choice on its default; nothing is built |
| 67 | Question 13: sites with no internet | Not for HP: open on a default | LIST A | A5 | Whether any customer needs it is a fact the team holds |
| 68 | Question 14: the pilot's success threshold | Not for HP: open on a default | LIST A | A24 | The team holds today's practice and takes commercial deployment (C-45); the figure stays his to accept |
| 69 | Question 15: "intra-environments" | Not for HP: open on a default | For the product owner himself | P5 | His own wording |
| 70 | OP-1: the utility as the operator's tool | Not for HP: added 2026-11-20 | LIST B | B5 | A design choice of the build |
| 71 | OP-2: does the utility install the server | Not for HP: added 2026-11-20 | LIST B | B6 | A design choice of the build |
| 72 | OP-3: a Windows PC at a Linux site | Not for HP: added 2026-11-20 | LIST A | A17 | How roll-outs are run today |
| 73 | OP-4: the console's own onboarding pages | Not for HP: added 2026-11-20 | LIST B | B7 | A design choice of the build |
| 74 | OP-5: where the amended utility lives | Not for HP: added 2026-11-20 | LIST A | A15 | The utility is the team's tool; its owner says where changes live |
| 75 | OP-6: the password in existing Workpath jobs | Not for HP: added 2026-11-20 | LIST A | A16 | Behaviour of the team's tool for Workpath jobs |
| 76 | OP-7: who deploys the licence-server offer | Not for HP: added 2026-11-20 | LIST A | A6 | Licensing as run today |
| 77 | OP-8: script or Marketplace: how many customers | Not for HP: added 2026-11-20 | LIST A | A7 | What customers have |
| 78 | OP-9: is v1.3.0 the live gateway package | Not for HP: added 2026-11-20 | LIST A | A8 | What is live today |
| 79 | OP-10: the phone app's source | Not for HP: added 2026-11-20 | LIST A | A9 | The phone app is the team's |
| 80 | OP-11: cc-api | Not for HP: added 2026-11-20 | LIST A | A10 | A fact about the team's own repositories |
| 81 | OP-12: the relay's basis on the customer gateway | Not for HP: added 2026-11-20 | LIST B | B8 | A design choice under C-27; the team reviews before any gateway release |
| 82 | OP-13: more of the earlier OXPd 1 work | Not for HP: added 2026-11-20 | LIST A | A11 | The earlier work is the team's |
| 83 | OP-14: the password in that tree's README | Not for HP: added 2026-11-20 | LIST A | A14 | The earlier work is the team's |
| 84 | OP-15: was that code run on a printer | Not for HP: added 2026-11-20 | LIST A | A12 | The earlier work is the team's |
| 85 | OP-16: the two card keys in that build | Not for HP: added 2026-11-20 | LIST A | A13 | The earlier work is the team's |
| 86 | OP-17: that build's tools as a lab probe | Not for HP: added 2026-11-20 | LIST B | B9 | A lab choice of the build |
| 87 | OP-18: the empty repository OXPD1 | Not for HP: added 2026-11-20 | LIST A | A11 | A fact about the team's own repositories |
| 88 | Access keys in a committed state file of the older back end | Not for HP: another team's | Notice | N1 | He flags it to the owning team himself (C-44) |
| 89 | Do a customer's other vendor solutions coexist | Touches HP, deliberately not an ask | Closed by a ruling or not asked | Answered or closed | Ruled: C-19 |
| 90 | Can HP supply interim firmware for older printers | Touches HP, deliberately not an ask | Closed by a ruling or not asked | Answered or closed | Not asked: public firmware only, on his answer C-6 |

### Table 2. The master list (Jira OXPD2-1, description and five comments): 60 items in, 60 out

Items in: the description's 24 (6, 13, 2 and 3 in its four groups); comment 41405, 1; comment 41406, 5 changed items and 18 new points; comment 41408, 3 asks added and 2 notes; comment 41412, 1; comment 41413, 3 findings and 3 new points. **Out: For the product owner himself 6; LIST A 25; LIST B 12; LIST C 6; Answered 8; Closed by a ruling or not asked 1; Notice 2. Sum 60.**

| # | Item | Old place | New list | New place | Reason |
|---|---|---|---|---|---|
| 1 | Card key | Master list: needs an answer first | LIST A | A1 | as in the first table |
| 2 | Printer on hand (HP MFP M577) | Master list: needs an answer first | For the product owner himself | P2 | as in the first table |
| 3 | Windows machine for the HP simulators | Master list: needs an answer first | LIST B | B11 | as in the first table |
| 4 | cc-api | Master list: needs an answer first | LIST A | A10 | as in the first table |
| 5 | OXPD1 repository | Master list: needs an answer first | LIST A | A11 | as in the first table |
| 6 | Start of building | Master list: needs an answer first | Answered | Answered or closed | C-42 |
| 7 | HP confirmation | Master list: open, proceeding on a default | For the product owner himself | P1 | as in the first table |
| 8 | Admin password on newer printers | Master list: open, proceeding on a default | LIST B | B1 | as in the first table |
| 9 | Meaning of full match | Master list: open, proceeding on a default | LIST B | B2 | as in the first table |
| 10 | OneDrive personal | Master list: open, proceeding on a default | LIST A | A2 | as in the first table |
| 11 | HP Advance and LRS VPSX sign-in role | Master list: open, proceeding on a default | LIST A | A3 | as in the first table |
| 12 | Design choices that differ from Workpath | Master list: open, proceeding on a default | LIST B | B3 | as in the first table |
| 13 | Universal Print registration | Master list: open, proceeding on a default | LIST A | A4 | as in the first table |
| 14 | QR sign-in without MFA | Master list: open, proceeding on a default | For the product owner himself | P3 | as in the first table |
| 15 | One central server for several sites | Master list: open, proceeding on a default | LIST B | B4 | as in the first table |
| 16 | OXPd 1.x version | Master list: open, proceeding on a default | LIST A | A22 (HP's part: H7) | The team is asked first whether Datasec holds anything newer; whether 1.9 exists is HP's |
| 17 | Sites with no internet | Master list: open, proceeding on a default | LIST A | A5 | as in the first table |
| 18 | Pilot success | Master list: open, proceeding on a default | LIST A | A24 | as in the first table |
| 19 | "Intra-environments" in the brief | Master list: open, proceeding on a default | For the product owner himself | P5 | as in the first table |
| 20 | From HP, in writing: the confirmation; App Center and validation access and the contact; the four dates; a first round with fewer than seven groups | Master list: to raise with HP | LIST C | H1, H2, H3, H4 | What HP owns; H1 and H2 reworded |
| 21 | HP developer account with an LDB Service Key, the simulator image, the simulator guide | Master list: to raise with HP | LIST C | H5 | HP's developer access |
| 22 | SharePoint source: received and read | Master list: answered | Answered | Answered or closed | C-33 |
| 23 | Sensitivity labels: left out | Master list: answered | Answered | Answered or closed | C-38 |
| 24 | HPAM back-end repositories and OXPd1_solution: received | Master list: answered | Answered | Answered or closed | C-40; both read since |
| 25 | Access keys in a committed state file (infra_hpam) | Master list: comment 41405 | Notice | N1 | C-44 |
| 26 | Gateway source: answered in full | Master list: comment 41406, items that changed | Answered | Answered or closed | C-40 |
| 27 | Sensitivity labels: answered | Master list: comment 41406, items that changed | Answered | Answered or closed | C-38 |
| 28 | QR sign-in without MFA: the fact is in | Master list: comment 41406, items that changed | For the product owner himself | P3 | An update of that item; follows it |
| 29 | Sites with no internet: a licence-server offer exists | Master list: comment 41406, items that changed | LIST A | A5 (and A6) | An update of that item; follows it |
| 30 | Deployment uses the existing utility, amended | Master list: comment 41406, items that changed | Answered | Answered or closed | Ruled: C-43; what follows from it is B5 to B7 and A15 to A17 |
| 31 | OP-1: the utility as the operator's tool | Master list: comment 41406, new points | LIST B | B5 | as in the first table |
| 32 | OP-2: does the utility install the server | Master list: comment 41406, new points | LIST B | B6 | as in the first table |
| 33 | OP-3: a Windows PC at a Linux site | Master list: comment 41406, new points | LIST A | A17 | as in the first table |
| 34 | OP-4: the console's own onboarding pages | Master list: comment 41406, new points | LIST B | B7 | as in the first table |
| 35 | OP-5: where the amended utility lives | Master list: comment 41406, new points | LIST A | A15 | as in the first table |
| 36 | OP-6: the password in existing Workpath jobs | Master list: comment 41406, new points | LIST A | A16 | as in the first table |
| 37 | OP-7: who deploys the licence-server offer | Master list: comment 41406, new points | LIST A | A6 | as in the first table |
| 38 | OP-8: script or Marketplace: how many customers | Master list: comment 41406, new points | LIST A | A7 | as in the first table |
| 39 | OP-9: is v1.3.0 the live gateway package | Master list: comment 41406, new points | LIST A | A8 | as in the first table |
| 40 | OP-10: the phone app's source | Master list: comment 41406, new points | LIST A | A9 | as in the first table |
| 41 | OP-11: cc-api | Master list: comment 41406, new points | LIST A | A10 | as in the first table |
| 42 | OP-12: the relay's basis on the customer gateway | Master list: comment 41406, new points | LIST B | B8 | as in the first table |
| 43 | OP-13: more of the earlier OXPd 1 work | Master list: comment 41406, new points | LIST A | A11 | as in the first table |
| 44 | OP-14: the password in that tree's README | Master list: comment 41406, new points | LIST A | A14 | as in the first table |
| 45 | OP-15: was that code run on a printer | Master list: comment 41406, new points | LIST A | A12 | as in the first table |
| 46 | OP-16: the two card keys in that build | Master list: comment 41406, new points | LIST A | A13 | as in the first table |
| 47 | OP-17: that build's tools as a lab probe | Master list: comment 41406, new points | LIST B | B9 | as in the first table |
| 48 | OP-18: the empty repository OXPD1 | Master list: comment 41406, new points | LIST A | A11 | as in the first table |
| 49 | H6 added to the HP group: licence terms | Master list: comment 41408 | LIST C | H6 | HP's terms; point 2 reworded, point 6 kept |
| 50 | H7 added to the HP group: anything newer than 1.8.4.1 | Master list: comment 41408 | LIST C | H7 (team first: A22) | HP's SDK |
| 51 | H8 added to the HP group: six technical points | Master list: comment 41408 | LIST C | H8 | HP's firmware behaviour |
| 52 | For the product owner before sending: the opening of H1 | Master list: comment 41408 | For the product owner himself | P1 | Only he knows when and how HP confirmed |
| 53 | For the product owner before sending: point 6 of H6 | Master list: comment 41408 | LIST C | H6 point 6 (tracked as B14) | Kept as HP's; whether it is sent is his |
| 54 | The OneDrive app's signing keystore and its password | Master list: comment 41412 | Notice | N2 | For the team that owns that repository; location only |
| 55 | The OneDrive source read: done and second-read | Master list: comment 41413 | Answered | Answered or closed | Done 2026-11-20 |
| 56 | The OneDrive app has four places | Master list: comment 41413 | Closed by a ruling or not asked | Answered or closed (size: B12) | Follows from C-16; only the size is open |
| 57 | Mailflow quick messages are switched off | Master list: comment 41413 | LIST A | A19 | Whether any shipped build showed them is a fact the team holds |
| 58 | OP-19: each tile keeps its own scan behaviour | Master list: comment 41413 | LIST B | B10 | A design choice of the build, on the default C-16 gives |
| 59 | OP-20: do the permissions cover Shared with me | Master list: comment 41413 | LIST B | T14 | A test on the tenant, not a decision |
| 60 | OP-21: translations or English only | Master list: comment 41413 | LIST A | A18 | The team can look at a printer today |

### New in this file (in neither table)

| Item | Why it is new | Source |
|---|---|---|
| P4 and B15: what MVP contains and where the hand-over sits | The words are in his message of 2026-11-20 and in no document | C-45, `CL:296` |
| A20: two looks at a Workpath printer | Until now they waited for a printer in the lab; the team has one today | `05:225`; `03:142` |
| A21: Datasec's accounts and contact at HP | The old draft asked HP; a Datasec team may already hold them | C-45; `B1:624`; `03:288` |
| A23: what the team can lend the lab | The kit list assigns these items to "the team"; no question had gone to a team | `05:192-205` |
| B12: the size of the widened OneDrive work package | Recorded as unsized, not listed as anyone's item | `05:258`; `03:186` |
| B13: the Teams quick-access read | Recorded as not proven, not listed as anyone's item | `05:256`; `03:181` |
| T1 to T13: the plan's thirteen tests | The plan's own; listed here so the build team's list is whole | `03:54-66` |
| T15 and T16: the phone message capture and the thumbnail address | What is left of two work packages on the tenant | `05:234`; `05:225` |

---

## WHAT I DID NOT READ

- **Read whole:** the commission; `registers/HP_QUESTIONS_DRAFT.md` (450 lines); `05_readiness-to-build.md` (266); `CLARIFICATIONS.md` (306, C-1 to C-46); `review/B1773_APPLIED.md` (180).
- **`03_plan-of-attack-and-build.md` was read in part:** lines 1 to 147 and 245 to 421 in full (the phases, the thirteen tests, the phase-0 work packages, dependencies, the team table, the 25 answers, the open questions and open points). Of lines 148 to 228 (the work packages of phases 1 to 6) I read only each row's name, independent check and the start of its size cell, by program. Lines 229 to 244 (test strategy) and 422 to 529 (change log) were not read.
- **`02_architecture.md` was read in part:** lines 792 to 847 and 926 to 973 in full, and lines 20, 22, 49, 217, 263, 362, 363, 379, 1097 and 1099 (the first 700 characters of each). The rest of its 1,126 lines was not read. A question that only the unread part of `02` raises is not in this file.
- **The analysis reports were not read whole.** I opened 57 single lines to check the pointers this file carries over from the old draft and from `05`: 15 in B1, 13 in B3, 4 in C1, 6 in C2, 12 in A9, 7 in A10 (the first 420 characters of each). Each said what the citing document says it says. Reports A1 to A8, A11 and B2, and the review files other than `B1773_APPLIED.md`, were not opened.
- **The twelve rows "answered by the documents"** were carried over by reference to the old draft and not re-checked row by row; five of their report lines are among the 57 above.
- **No HP document, no source tree, no printer, no tenant.** Every statement about what HP's guides, portal, release notes or forum say is a report's reading, cited by report line. Every statement about what the apps' code does is from `05` or `03` at the line cited.
- **HP's written confirmation and Datasec's agreements with HP were not seen.** Neither is in the library (`05:241`, `05:257`).
- **Nothing is known to me about the Datasec product team** beyond the product owner's sentence in C-45: not its people, not what accounts or printers it holds. LIST A asks; it assumes nothing. Whether a given question should go to one named person is his to decide.
- **Jira:** one request, a GET of issue OXPD2-1 with the fields summary, status, description, updated and comment. It returned the description and 5 of 5 comments (41405, 41406, 41408, 41412, 41413). The kit checklist OXPD2-2 was not read (outside the one permitted request). Nothing was written to Jira. The credentials were read by name inside one process and never printed.
- **Searches behind "defined nowhere" and "not said anywhere"** (counts of the term, case ignored, in `02`, `03`, `05`, `CLARIFICATIONS.md`, in that order): "MVP" 0, 0, 0, 2; "handover" and "hand over" 0, 0, 0, 0; "hand it over" 0, 0, 0, 1; "commercial deployment" 0, 0, 0, 2; "master admin" 0, 0, 0, 0; "partner agreement" 0, 0, 0, 0; "HP.io" 0, 0, 0, 0; "product team" 0, 0, 0, 2. Positive controls in the same run: "LDB" 4, 6, 1, 0; "App Center" 1, 5, 1, 0; "Workpath team" 0, 4, 2, 1. The analysis reports were not part of this search, except that "MVP" was also searched as a whole word in every `.md` file under the folder: it appears in reports A2 and A11 (not opened) and in `CLARIFICATIONS.md`.
- **Judgements that are mine and not a ruling of anyone:** which list each item goes to; that the "acceptable to HP" question falls away; the placing of the pilot threshold with the team (A24) and of the design choices with the build team (B3); the three options offered under P4; the wording of every copy-ready box. C-45 is quoted where it is used, and it rules on no single question (`CL:298`).
- **Not done:** no message to anyone, no Jira write, no git, no Azure, no GitHub call, no network call other than the one Jira request. `registers/HP_QUESTIONS_DRAFT.md` and its PDF were not touched. No PDF of this file was made.
- **Secrets:** no secret value is in this file and none was displayed by any command. The keystore file at the root of the OneDrive tree is referred to only by that description; its name was never read or written by this work. Locations of keys are given as the documents give them, without paths.

