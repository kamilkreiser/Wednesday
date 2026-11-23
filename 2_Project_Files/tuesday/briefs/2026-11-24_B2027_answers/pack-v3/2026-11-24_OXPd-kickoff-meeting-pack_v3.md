# OXPd 2 kick-off: the meeting pack

Datasec, Tuesday 2026-11-24, for the team kick-off this evening. For Kam to drive the meeting: Part 1 is what needs a decision, Part 2 is what we need from the Workpath team. Every answer box can be typed into in Word.

### Version 3: your answers of this morning, and what is still open for the room

- **Answered this morning.** Your file "OXPd Project Answers" (live board, 2026-11-24 09:55) gives words for 63 of the pack's 112 items. Kick-off basics: 6 of 6 (S1 to S6). Part 1: 10 of 53 (Q1 to Q3, Q12 to Q14, Q22, Q32, Q34, Q39). Part 2: 47 of 53 (W1 to W13, W15 to W24, W26 to W40, W44 to W51, W53). Counted by program from your file and this pack. Your words stand verbatim under each of these items, in place of its answer box; nothing else in the pack is re-worded. Since then your tap of 10:19 answers Q6; it is shown under Q6, verbatim.
- **Sent to Jira.** 28 Part 2 items carry your words "create a Jira ticket (with the question) and assign to Steve M - 2 week time request": W1 to W4, W6, W9 to W11, W16, W19, W21 to W24, W26 and W27, W30 to W40, W48. That is 25 tickets, plus one for the swim-lane diagrams you asked Steve M to give to Artur M (W8): 26 drafts, none created yet. They are not for the room unless you want them there.
- **Still open for the room.** Sent to the meeting by your own words: Q32, W9, W29 ("left for kickoff", "needs discussion", "discussion shoudl be had"). Part 1 with no answer yet: Q4 and Q5, Q7 to Q11, Q15 to Q21, Q23 to Q31, Q33, Q35 to Q38, Q40 and Q41 (30 items, answer boxes kept). Part 2 with no answer yet: W14, W25, W41 to W43, W52 (6 items, boxes kept). Seven items with your words are still open (Q1, Q12, Q13, Q32, W9, W15, W29): each keeps a box under your words. For you alone after the meeting, unchanged: Q42 to Q53 (12 items).
- **Tonight's two lists.** Of the ten to decide, 10 have your words. Six are settled by them: Q2, Q3, Q14, Q22, Q34, Q39. Four still need a pick tonight: Q32 (your words send it to the kick-off), and Q1, Q12 and Q13, where your words name none of the question's options (Q1: a, b or c; Q12: i, ii or iii; Q13: a, b or c). Of the eight to give an owner, 8 have your words: W7 and W12 answered; W8 answered in part (see "Settle these tonight", 6); W1, W2, W3, W4, W16 sent to Jira. By Tuesday's reading of your W7 the build makes its own test set-up, so the BLUF's "W7 asks the team for the tenant" no longer holds; and Q6, under "If time remains" below, is now answered by your tap (see 2).

### Settle these tonight

Each is a place where your words differ from an earlier ruling or the design, or leave a question without a pick. None is resolved in this pack, and the default runs until you say.

1. **Azure.** Your Q12 and W7 name HPSM-POC's subscription and kamil@datasec-rd.com; your tap of 23 November named "the agent-controllable Datasec environment". Which one, and may more than the one test VM be created? Default: the one test VM only.
2. **Dates and Q6: settled by your tap.** Your tap at 10:19 (verbatim): "a — OXPd 1.x ships first: re-plan to the dates". Q6 (do older printers ship alone if HP is late) is answered by it and shows the tap. The dated re-plan to 20 December and 12 January is in the plan of attack: see 03 section 0.5. Still open with it: Q5 (the defect level that ends the pilot).
3. **"OXPd 1.9": settled by your tap.** Your tap at 10:27 (verbatim): "b — 1.9 means our 1.x line". The build stays on HP's SDK 1.8.4.1 (we hold it and the Demos 1.9, and no SDK 1.9).
4. **OXPd 2 by 12 January.** Four HP items have no date, HP wants a test on seven printer groups, and there is a four-week pilot with no customer. Default: no OXPd 2 date is promised.
5. **Q1, Q12, Q13.** Pick an option (see "Tonight's two lists" above).
6. **W8.** We hold captions of the videos and no video file.
7. **W15.** Your words say where reports go, not whether Universal Print counts are for Secure printers only.
8. **Your line "reporting - ..." has no item number.** Are W41 to W43 yours or Steve M's?

OXPd 2 in one line: the rebuild of Datasec's HP printer apps (HP Authentication Manager sign-in and the OneDrive, SharePoint, Teams, Mailflow and Universal Print apps that ship today on HP Workpath) for printers that run HP OXPd, older printers on OXPd 1.x and newer printers on OXPd 2, from one server beside Workpath (project CLAUDE.md, "What this project is").

## BLUF: where OXPd stands today

- **Built and landed.** All 44 pull requests are merged; main is b0b26b60 (pull request 44, landed 2026-11-24 00:45 AEDT). Its CI run passed: 2,093 tests, 0 failed (2,089 ran on Linux and 2,072 on Windows; the rest are skipped on that system), and 0 open code-scanning alerts. What is built needs no printer: build checks, the OXPd 2 contracts and adapter, the server host v0, sign-in and token handling, the card store, the secret store and the database, the Universal Print and job services, the OXPd 1.x read and write clients, and the lab tool. Nothing has been run on a printer, a simulator or a tenant. Nothing is deployed.
- **In preparation today.** The records pass for pull requests 43 and 44, and the second fix round of the lab write command ("W2 round 2"): both are commissioned, and neither has landed. The updated architecture (02) and plan of attack (03). This pack.
- **Held.** Tuesday has put a hold on writes to printers: no "oxpd1 write --execute" against any device, the M577 included. It lifts when W2 round 2 fixes two findings from review B2016. FOUND 1: the undo check prints "nothing is owed" when it read no undo list. FOUND 2: the read-before-register check lets the register go ahead when the printer gives an answer the check does not recognise.
- **Waiting on you (not for the meeting).** The M577's admin password (C-77). The OXPd Azure sign-in steps for the one test VM (C-78; the VM is made only after the home rehearsal passes). A test tenant user with Authenticator, for the first panel sign-in test (C-76; W7 asks the team for the tenant). The videos of the sign-in paths: we hold the captions of 11 Lightning Talks and no video file, so no screen has been seen. You offered to re-share them (your note P3: "If you do not have these, tell me and I will re-share.").
- **Next.** The records pass, then W2 round 2 (this lifts the hold), then the M577's first run and the first sign-in test on its panel (both wait on you: the password and a test tenant user), then the write lanes for first-run steps 2 to 4, the "oxpd1 echo" command and the Azure test, and the phase-0 hardware and tenant list. What tonight decides changes this order.

### What this meeting is for

To kick off OXPd with the team. The build has gone as far as it can without a printer, a tenant or a decision. Tonight it needs two things. First, decisions on the questions that block the most work (Part 1). Second, an owner and a date for each piece of information that only the Workpath team holds (Part 2).

By Tuesday's own reading, your word of 2026-11-23 to move OXPd forward (C-71) is re-read with you after this meeting; C-71 itself names no end. Your word to build what needs no printer (C-42) stands. Q1 asks what else the build may do from tomorrow.

### How to use this pack

- Start with the TONIGHT list on this page. Everything else keeps its default; the team fills in the rest in the Word file afterwards.

- Each question is one question. Its block says why it matters, the options, what we recommend and what the build does meanwhile. If a question gets no answer tonight, the build keeps that default.

- Type into the box under each question (in Word, click the grey text). A short answer is enough: "b", "yes", "Steve M, by Friday".

- Send the filled-in file back to Tuesday. The answers then go into CLARIFICATIONS.md as your words, and onto the master list (Jira OXPD2-1).

- Part 2 items are for the Workpath team. In the meeting, give each one an owner and a date. The team can fill in its own boxes afterwards.

- Ids are new in this version (round 2). Items that need only you, not the team, are at the end of Part 1.

### TONIGHT: decide these ten

| Id | Subject | Why tonight |
|---|---|---|
| Q12 | The phase-1 hosting shape in Azure | Sets the network design, the packaging and the one Azure test; every older printer needs two-way traffic on a fixed port. |
| Q13 | Which packagings ship in release 1 | Decided with the hosting shape; it sets the whole of phase 5 and whether both build legs are kept. |
| Q32 | HP's OXPdLib or Datasec's own client for older printers | The product adapter for older printers cannot start until this is chosen (C-74 left it for the kick-off). |
| Q34 | How an OXPd 2 printer or simulator reaches the lab | Every OXPd 2 component is tested on stand-ins only; without one there is no date for any OXPd 2 proof. |
| Q39 | Which HP asks go out now (H3, H5 first) | HP's answers have the longest lead time in the project, and nothing has been sent. |
| Q2 | When the product is handed to the Workpath team | Decides who owns the pilot, the HP submission and the deployment tool; the team is in the room. |
| Q3 | Who prepares the HP signing submission | Follows Q2; the seven-group printer test needs an owner early. |
| Q14 | Which deployment tool carries OXPd | The deployment design note is written against one tool; a wrong pick is rework (answer with W16). |
| Q22 | Datasec's Universal Print registration or each customer's | All of phase 4 waits on it (answer with W12). |
| Q1 | What the build may do from tomorrow | The printer and lab work beyond the M577 first-run list needs a scope. |

### TONIGHT: give these eight an owner and a date

| Id | Subject | Why tonight |
|---|---|---|
| W1 | Is the card key in the 4.4.1 source the live key | Card sign-in in phase 1 and the lab's key handling wait on it; first item on the master list. |
| W2 | Which card-decoding family produced customers' stored cards | The wrong family means stored cards read as unknown on every OXPd printer; the decoders are already built one way. |
| W3 | Model and firmware of each printer in the product owner's lab | Fills four phase-0 kit items in one table. |
| W4 | Access to a FutureSmart 6 printer in developer mode | The only route to an OXPd 2 proof besides HP's simulator (Q34). |
| W7 | A test tenant set up as customers have it, with a test user | The first panel sign-in test on the M577 (C-76) cannot run without the test user. |
| W8 | A walkthrough of every sign-in path, or the videos | You called it critical; the design rests on transcripts only. |
| W12 | Who owns Datasec's Universal Print registration | Needed to answer Q22. |
| W16 | Which deployment tool customers get today | Needed to answer Q14. |

If time remains: Q6; Q8 with W25; Q31; Q38 with W27; W41.

### Settle first: the kick-off basics

Settle these first: what a team lead asks before the lists.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **S1** | **Who on the Workpath team is the one contact for the build's questions?** C-45 says the build "will leverage the work path team"; the pack never says through whom. <sub>Source: C-45; B2023 F5</sub> | A name. **We recommend: Name one person tonight. Meanwhile: Questions go to you.** | **Your answer, 2026-11-24 morning (verbatim):** s1 - Steve M |
| **S2** | **How fast can the build expect an answer from that contact?** The build waits on Part 2 items; a lane cannot plan around an unknown wait. <sub>Source: B2023 F5</sub> | Same day, two days, a week. **We recommend: Two working days. Meanwhile: None set.** | **Your answer, 2026-11-24 morning (verbatim):** s2 - 1 - 2 days |
| **S3** | **After tonight, how do questions reach the team: the master list (Jira OXPD2-1), or another channel?** Your rule is one master list (C-41); the team may not watch Jira. <sub>Source: C-41; B2023 F5</sub> | (a) Jira OXPD2-1. (b) Another channel you name. **We recommend: (a), with a weekly digest to the contact. Meanwhile: Jira OXPD2-1 (C-41).** | **Your answer, 2026-11-24 morning (verbatim):** s3 - jira.  All dev work assigned to us.  Work path items all assigned to Steve and delegated by him |
| **S4** | **Is there a target date that sets the pace?** Nothing in the records names one. OXPd 2 also waits on four undated HP items (05:20). <sub>Source: 05:20; B2023 F5</sub> | A date, or none yet. **We recommend: Name one for OXPd 1.x; OXPd 2 waits on HP. Meanwhile: No date.** | **Your answer, 2026-11-24 morning (verbatim):** s4 - OXPd 1.9 by 20 Dec OXPd 2 by 12 Jan |
| **S5** | **Is there a first customer in view?** A first customer sets the pilot site, its printers and its tenant (Q4, Q5). <sub>Source: B2023 F5</sub> | A customer, or none yet. **We recommend: Name one if there is one. Meanwhile: None named.** | **Your answer, 2026-11-24 morning (verbatim):** s5 - no |
| **S6** | **How much of the team's time may the build ask for each week?** Part 2 asks the team for documents, walkthroughs, a lab printer and a tenant. <sub>Source: C-45; B2023 F5</sub> | Hours per week, or per request. **We recommend: A fixed weekly slot. Meanwhile: Ask item by item.** | **Your answer, 2026-11-24 morning (verbatim):** s6 - as many as required to met deadlines |

### The questions at a glance

| Theme | Items | Numbers |
|---|---|---|
| Kick-off basics | 6 | S1 to S6 |
| Part 1: Scope and phasing (sets the work from tomorrow) | 11 | Q1 to Q11 |
| Part 1: Hosting and deployment | 10 | Q12 to Q21 |
| Part 1: Sign-in and identity | 10 | Q22 to Q31 |
| Part 1: Licensing and HP code | 2 | Q32 to Q33 |
| Part 1: Printers and lab | 5 | Q34 to Q38 |
| Part 1: Commercial and HP | 3 | Q39 to Q41 |
| Part 1: For Kam alone, after the meeting (defaults stand until then) | 12 | Q42 to Q53 |
| Part 2: Keys, lab and tenant (these block phase 0) | 7 | W1 to W7 |
| Part 2: How today's product signs users in | 4 | W8 to W11 |
| Part 2: Universal Print, licensing and deployment | 13 | W12 to W24 |
| Part 2: Scope, pilot and operations | 5 | W25 to W29 |
| Part 2: What the apps do on a printer today (parity details) | 11 | W30 to W40 |
| Part 2: Reporting | 3 | W41 to W43 |
| Part 2: HP accounts and earlier work | 10 | W44 to W53 |
| Only HP can answer (not for the meeting) | 8 | H1 to H8 |
| Appendix A: answered and dropped | 32 |  |

## Part 1: questions that need discussion or a decision

Questions for the team or for you to decide. Each is still open in the records. Any question you have already answered is dropped and listed in Appendix A, with the C-number that answered it. The themes are in the order of how much work they block. "Meanwhile" is what the build does until the question is answered.

### Scope and phasing (sets the work from tomorrow)

**Q1. From tomorrow, beyond the no-hardware work, what printer and lab work may the build do without asking you each time?**

**Why it matters: **The no-hardware lanes continue under C-42. What needs your word is the printer work beyond the M577 first-run list (C-72), and the OXPd 2 lab work.  
**Options: **(a) The M577 first-run list (C-72) and its panel sign-in test (C-76), each step gated, and no more. (b) (a), plus any read-only work on lab printers the team lends. (c) (b), plus OXPd 2 lab work once a FutureSmart 6 printer or the simulator is here.  
**We recommend:** (c). **Meanwhile the build:** No-hardware lanes, and the M577 runs you approved.  
<sub>Source: C-42; C-60 message 7; C-68; C-71; C-72; C-76; Tuesday EXPIRING-GRANTS (its reading of C-71)</sub>


| Answer Q1 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q1 - Steve M has multiple printers and a full test lab.  He will be in charge of testing. <br>**Still open; decision tonight:** &nbsp; |

**Q2. At what point is the product handed to the Workpath team?**

**Why it matters: **You said the build "will leverage the work path team but hand it over for them to manage commercial deployment once ready" (C-45). When that happens decides who owns the pilot, the HP submission and the deployment tool.  
**Options: **(a) At the end of the pilot. (b) At the release gate, before the HP submission. (c) Earlier, at the end of phase 3, when the apps match Workpath.  
**We recommend:** (b), at the release gate: the build team keeps the product through the pilot's fixes. **Meanwhile the build:** The build team keeps everything up to MVP (C-45).  
<sub>Source: QUESTIONS_BY_OWNER v2 P4-2; C-45; C-48 (the hand-over half of P4 is not answered)</sub>


| Answer Q2 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q2 - after fully tested, documented and listed in the Azure marketplace.  Target date 12 January.  Handed to Steve Molnar as product owner of Workpath apps |

**Q3. Who prepares and sends the submission to HP for signing: the build team or the Workpath team?**

**Why it matters: **HP signs OXPd 2 bundles. A product that signs users in must be tested on at least one printer from each of seven groups (05:250).  
**Options: **(a) The build team. (b) The Workpath team, which already deals with HP for the Workpath apps.  
**We recommend:** (b): the Workpath team already holds the HP route (W44). **Meanwhile the build:** The plan prepares a production bundle once the vertical slice works (03 section 1). Nothing goes to HP without your word.  
<sub>Source: QUESTIONS_BY_OWNER v2 P4-4; 03 section 1; 05:250</sub>


| Answer Q3 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** Q3 - Steve M (who will be part of the dev) |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q4** | **Who runs the pilot: the build team or the Workpath team?** The pilot needs a customer site, a person at the printers and a defect threshold (Q5). Its owner sets all three. <sub>Source: QUESTIONS_BY_OWNER v2 P4-3; 03 phase 6</sub> | (a) The build team. (b) The Workpath team. (c) Jointly: Workpath owns the customer, the build team owns the fixes. **We recommend: (c). Meanwhile: None. Phase 6 (the pilot) is not started.** | &nbsp; |
| **Q5** | **What defect level ends the four-week pilot successfully?** Your answer A24 sets the aim ("as close to commercial ready as possible") but not a number. Phase 6 cannot exit without one. <sub>Source: 05:150 (question 14); 05:213 (N-13); C-58 paragraph 32 (A24)</sub> | A number of open defects by severity, for example: 0 critical, 0 high, up to N medium. The Workpath team can say what it accepts for a Workpath pilot today (W26). **We recommend: Use the Workpath team's own pilot threshold (W26). Meanwhile: None set. It must be set before the pilot starts.** | &nbsp; |
| **Q6** | **If HP's signed OXPd 2 bundle is late at the release gate, do the older printers (OXPd 1.x) ship alone?** OXPd 2 cannot reach a customer until HP delivers four things, and none has a date: production firmware, a platform version validation accepts, a signing service whose output installs, and the turnaround. OXPd 1.x has no such dependency on HP (05:20). <sub>Source: 03 section 1; 05:20; 02 D33</sub> | (a) Yes, OXPd 1.x ships first. (b) No, both ship together. **We recommend: (a). It earns revenue from the older fleet while HP is pending. Meanwhile: Both generations are built to the same release. The plan leaves this to you at the gate (03 section 1).** | **Your tap on the board, 2026-11-24 10:19 (the card on your two dates; verbatim):** a — OXPd 1.x ships first: re-plan to the dates |
| **Q7** | **Is OneDrive personal (consumer accounts) in release 1?** The code has a build variant for it, but the release pipeline does not build it and consumer sign-in is switched off. The test is your C-48 words: is it live in Workpath deployments today? <sub>Source: 05:74 (question 4); 03 section 8.3 (OQ-4)</sub> | (a) Out: it is not a shipped product. (b) In: it is sold or wanted. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q8** | **Is HP Authentication Manager's role as the sign-in for HP Advance and LRS VPSX in release 1?** The product documents this role today. The test is your C-48 words: is it live in Workpath deployments today? "Ours only" (C-19, no other vendor's print solution) would exclude it. Whether any customer uses it is W25. <sub>Source: 05:81 (question 5); 03 section 8.3 (OQ-5)</sub> | (a) Out. (b) In, which is new design and build work. **We recommend: (a), unless a customer you intend to sell to uses it (W25). Meanwhile: (a).** | &nbsp; |
| **Q9** | **When scanning into a SharePoint library, does each tile keep its own behaviour of today?** A library opens from two tiles: SharePoint and OneDrive's "Shared libraries". Today the SharePoint app asks for the library's fields at scan and the OneDrive app does not. <sub>Source: 05:184 (OP-19)</sub> | (a) Yes, each matches its own Workpath app. (b) Make them the same. **We recommend: (a): each tile matches what is live today (C-48). Meanwhile: (a).** | &nbsp; |
| **Q10** | **Should the OneDrive work package be re-sized before it is scheduled?** Reading the code showed four places, not one: My Drive, Recent, Shared with me and Shared libraries. Under C-16 all four are rebuilt. The package was sized from the manual, for My Drive only. <sub>Source: QUESTIONS_BY_OWNER v2 B12; 05:22; 05:294</sub> | (a) Re-size now. (b) Re-size when phase 3 is planned. **We recommend: (b). Meanwhile: Unsized.** | &nbsp; |
| **Q11** | **In your brief, does "integration into intra-environments" mean "Entra environments"?** It is a one-word check on the brief of 2026-11-18. The one intranet item the other reading would add, an outbound web proxy, is designed in either way. <sub>Source: 05:155 (question 15); 03 section 8.3 (OQ-15)</sub> | (a) Entra. (b) The customer's intranet as well. **We recommend, and meanwhile: (a).** | &nbsp; |

### Hosting and deployment

**Q12. In phase 1, what shape is "hosted through Azure"?**

**Why it matters: **Every older printer (OXPd 1.x) needs two-way traffic with the server, cannot work through address translation and uses fixed port 7627. The answer decides the network design, the packaging and test 2 (the one Azure test VM of C-78).  
**Options: **(i) A server in the client's Azure for each site, joined to that site's network. (ii) A machine at each site, deployed and governed through the client's Azure. (iii) Servers in Azure in phase 1, and the on-site server in phase 2.  
**We recommend:** Expect (i); test 2 confirms or refutes it (C-75, C-78). **Meanwhile the build:** The code stays hosting-neutral. Test 2 is written but has not been run.  
<sub>Source: 05:199 (P-4, N-5); 03 section 8.5; C-26; C-60 messages 3 to 5; C-75; C-78</sub>


| Answer Q12 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q12 - clients will deploy the solution through the Azure marketplace using services and components automatically deployed by the configuration scripts we create and submit.  During development, we will mirror this structure as closely as possible so the deployment is tested through dev.  Use the same subscription as HPSM-Poc.  Tied to kamil@datasec-rd.com <br>**Still open; decision tonight:** &nbsp; |

**Q13. Which packagings ship in release 1, now that phase 1 is hosted in Azure?**

**Why it matters: **C-17 ("Both equally") meant container, appliance and Windows, all at release. Your words "different hosting options for the client" (C-60) add an Azure route. Your note A7 ("Azure marketplace") was about how customers deploy today's Azure side, and may point the same way.  
**Options: **(a) All three, as C-17 says. (b) An Azure deployment (template or Marketplace offer) first, the others later. (c) Azure plus one on-site packaging.  
**We recommend:** (b): Azure first, since phase 1 is hosted in Azure. **Meanwhile the build:** The C-17 wording stands. Both build legs are kept and nothing Azure-specific is built.  
<sub>Source: 05:200 (P-5, N-6); 03 section 8.5</sub>


| Answer Q13 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q13 - phase 1 needs to be a fully operational build. <br>**Still open; decision tonight:** &nbsp; |

**Q14. Which deployment tool carries OXPd: HP AuthSuite Manager, or the HPK Deployment Utility?**

**Why it matters: **You asked for the newer tool (C-60 message 2). By file dates that is the AuthSuite Manager. By version number it is the Utility (3.0.0 against 1.1.0). Your note A15 makes the OXPd part a separate app until after the MVP.  
**Options: **(a) HP AuthSuite Manager, with OXPd as a separate app (the current default). (b) The HPK Deployment Utility, amended (C-43). (c) A new separate app that neither tool includes until after the MVP.  
**We recommend:** (a). Confirm which tool the Workpath team actually ships today (W16). **Meanwhile the build:** The design note (WP0.10) is written against the Manager, with OXPd as a separate app. Nothing is pushed to either tool's repository.  
<sub>Source: 05:201 (P-6, N-9); 03 section 8.5; WP0.10:80; C-43; C-60 message 2; C-58 paragraph 23 (A15)</sub>


| Answer Q14 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q14 - option a as reccomended |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q15** | **Does the deployment tool only start and follow jobs, with the server doing the work on each printer?** The server has to keep each printer's token, records and repair loop. A desktop tool that is closed after the job cannot do that. <sub>Source: 05:166 (OP-1); 03 section 8.4; WP0.10:73</sub> | (a) Yes: the tool is the operator's front end and the server does the work. (b) The tool does the device steps itself. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q16** | **Does the deployment tool also install the OXPd server itself?** Neither Datasec tool has code that installs software on a machine (report D2 section 3.3). If the server is deployed into Azure (Q13), the tool may not need to. <sub>Source: 05:167 (OP-2); 03 section 8.4</sub> | (a) No: the server has its own packaging. (b) Yes: the tool is amended to install it. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q17** | **Is a batch of printers started from the deployment tool only, with the server console showing status and repairing one printer?** This decides whether the server console needs its own onboarding pages. <sub>Source: 05:169 (OP-4); 03 section 8.4; WP0.10:82</sub> | (a) Tool only. (b) The console also gets onboarding pages. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q18** | **Does the deployment-tool work (WP0.10) join the first build list now?** It was not one of the twelve no-hardware packages your word to build covered (C-42). Its design note is a draft. <sub>Source: 05:272 (WP0.10 row); WP0.10:79; 03 section 4, Phase 0</sub> | (a) Yes, start it now. (b) Wait until Q14 to Q17 are settled. **We recommend: (b). Meanwhile: Only the draft note exists. No build work has started.** | &nbsp; |
| **Q19** | **Where do the two-server and packaging test hosts run: lab machines, or Azure in a subscription you name?** Kit item 16 needs two Linux and two Windows hosts (virtual machines will do). With phase 1 in Azure, they could run there. <sub>Source: 05:212 (N-18); 05:240 (kit item 16)</sub> | (a) Lab machines. (b) Azure, in a subscription you name, with the cost on a card first. **We recommend: (a) until Q12 is settled. Meanwhile: Nothing is created in Azure without your word.** | &nbsp; |
| **Q20** | **For a two-server setup in the client's Azure, which availability method do we use?** The on-site design pairs two servers behind a virtual IP. Azure has its own load-balancing services that could do this instead. <sub>Source: 02 N-7 (03 section 8.5)</sub> | (a) The virtual-IP pair, as designed. (b) Azure's own load balancing. **We recommend: (b) if Q12 puts servers in Azure. Meanwhile: Unchanged. This is phase-5 work and has not started.** | &nbsp; |
| **Q21** | **When the server runs in the client's Azure, does Azure Key Vault become its default secret store?** Only the local encrypted store is built (pull requests 5, 11, 24). Key Vault would be a second provider. <sub>Source: 02 change log, B1817 open questions (N-8)</sub> | (a) Yes, Key Vault by default in Azure. (b) The local store everywhere. **We recommend: (a) for Azure hosting, once Q12 is settled. Meanwhile: The local store stays the only one built.** | &nbsp; |

### Sign-in and identity

**Q22. Does each customer register their own Universal Print app, or does the server use Datasec's registration?**

**Why it matters: **Your answer A4 put "everything" in the client's tenant. The design had assumed Datasec's own registration. Who owns that registration today is W12.  
**Options: **(a) Datasec's registration. (b) Each customer registers their own.  
**We recommend:** (b) if "everything in their tenant" covers it. Otherwise (a), if W12 shows Datasec can add what the server needs. **Meanwhile the build:** Nothing is built on Datasec's registration before the answer.  
<sub>Source: 05:111 (question 9); 05:214 (N-14); 03 section 8.3; C-58 paragraph 15 (A4)</sub>


| Answer Q22 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q22 - Datasec guides (through doc and paid work) on setup by everything about work path and OXPd is done by the client in their own app / tenant |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q23** | **If Microsoft's sign-in page cannot run safely on a printer panel, what do we do instead?** You ruled that the Microsoft number step stays on the panel, as Entra sets it (C-60 message 1). The first panel test may show that users share cookies, that the page does not render, or that it needs a pop-up. Another HP partner's on-panel Microsoft sign-in failed on OXPd 1.x because of memory and certificate trust (05:196). <sub>Source: 05:210 (N-3); 03 section 8.5; C-60 message 1; C-76</sub> | (a) The phone-link route (M2), which needs the relay on each customer's gateway (Q29). (b) No Microsoft step on that printer generation, so card or QR sign-in only. (c) Decide when the test result is in. **We recommend: (c). The result comes to you with options. Meanwhile: The panel route only. The phone routes and the relay stay unbuilt.** | &nbsp; |
| **Q24** | **Must older (OXPd 1.x) and newer (OXPd 2) printers use the same sign-in step?** You chose to test the panel on the M577 first (C-76). That decides how the test is run, not what the target is. The older panel browser is old and small. The design's sign-in table (02 section 5.5) still offers phone methods for 1.x, against D10 and N-1 (B2019). <sub>Source: 05:196 (P-1, N-1); 03 section 8.5; C-76</sub> | (a) Same target on both: the Microsoft step on the panel. (b) Older printers may use a different route if their panel test fails. **We recommend: (a), and come back to this with the M577 result. Meanwhile: Same target on both. Nothing of a phone route is built for 1.x before the panel test reports.** | &nbsp; |
| **Q25** | **Does "we cannot interfere with ... the token management done by microsoft" stop the server from holding and refreshing users' tokens?** The design's server obtains, holds, refreshes and uses each user's Microsoft tokens so that scan and print can act as that user. No-MFA mode (C-7) redeems a stored token with no user present. <sub>Source: 05:198 (P-3, N-4); 03 section 8.5; C-60 message 1; C-7</sub> | (a) No: the server uses Microsoft's own library and the tokens Microsoft issues, encrypted, and never sent to a printer. That counts as using Microsoft's token management, not interfering with it. (b) Yes: redesign so the server keeps no user tokens. **We recommend: (a). Meanwhile: (a). Nothing new is designed.** | &nbsp; |
| **Q26** | **Is QR sign-in without MFA offered on OXPd printers?** The customer's existing sign-in gateway does not check who sends an unlock message. In No-MFA mode a QR message is a full sign-in (report A9, 05:118). This weakness is in today's gateway, not something OXPd adds. <sub>Source: 05:117 (question 10); 05:215 (N-15); 03 section 8.3</sub> | (a) Offer it as Workpath does, with the risk recorded. (b) Switch it off on OXPd until the gateway is fixed. Your "may change" answer (C-27) allows this. **We recommend: (b). Meanwhile: (a), as Workpath. Nothing of QR sign-in is built before phase 3.** | &nbsp; |
| **Q27** | **If the panel refuses to show Microsoft's page inside a frame, is a full-page sign-in acceptable?** Your words were "display 2 digit in iframe". Whether Microsoft's page can be framed is not measured. Test 1 tries the frame first. <sub>Source: 05:197 (P-2, N-2); 03 section 8.5; C-60 message 1</sub> | (a) Yes, a full page is acceptable. (b) No, it must be a frame. **We recommend: (a). Meanwhile: The panel page is written for either.** | &nbsp; |
| **Q28** | **May the server keep an encrypted copy of a newer printer's admin password?** Your tap C-24 said "Store it encrypted". The option's own text said newer printers discard it. If a newer printer loses its access token on reboot (asked of HP in H8), someone would have to re-enter the password for each printer after each reboot. <sub>Source: 05:62 (question 2); 03 section 8.3 (OQ-2); WP0.10:81; C-24</sub> | (a) Never stored on newer printers. (b) Stored as a per-site choice, off by default. **We recommend: Wait for the phase-0 test of what a reboot does, then (b) if tokens are lost. Meanwhile: (a).** | &nbsp; |
| **Q29** | **May each customer's gateway get one address that accepts a request without a token, for the phone-link relay?** The phone-link route needs it. Customers who deployed by script need a second update route. Since the Microsoft step went back to the panel (C-60), the relay is only needed if Q23 picks the phone route. <sub>Source: 05:177 (OP-12); 05:210 (N-3)</sub> | (a) Yes, under "may change" (C-27), with the test the plan describes. (b) No. **We recommend: Wait for test 1 (Q23). Meanwhile: Not before test 1 reports.** | &nbsp; |
| **Q30** | **Does OXPd offer today's unattended Universal Print registration from a stored account?** Today a fleet can be registered without a person present, from a stored account (how it works today is W14). The design registers interactively. <sub>Source: 02 change log, B1817 open questions (N-12)</sub> | (a) Interactive only. (b) Unattended as well. **We recommend: (a) for release 1. Meanwhile: (a).** | &nbsp; |
| **Q31** | **Do you approve the six design differences from Workpath in the deviation register (DEV-14 to DEV-19)?** They are not forced by the platform or by your answers. Phase 3 cannot exit until they are approved or struck. You approved DEV-22 and DEV-23 on 2026-11-23 (C-70). The six are: DEV-14, pull release matches the user exactly, not by substring; DEV-15, card emulation moves to the server admin console; DEV-16, app settings move to the server console; DEV-17, Universal Print counts are reported for all three printer types, not Secure only; DEV-18, in No-MFA mode a refreshed token is written back, only if spike S5 passes; DEV-19, error screens show the help address as text and QR. <sub>Source: DEVIATION-REGISTER_DRAFT.md:32-37 and :50; 05:87 (question 6); 03 section 8.3 (OQ-6)</sub> | Approve all six, strike any by number (a struck row then follows Workpath exactly), or approve all but DEV-18 until its test. **We recommend: Approve all except DEV-18, which waits for its phase-0 test. Meanwhile: As designed, pending approval before phase 3 exits.** | &nbsp; |

### Licensing and HP code

**Q32. For older printers, does the shipped product use HP's own OXPdLib library or Datasec's own client?**

**Why it matters: **Your note settled the licence question: "our license / commercial agreement allows us to use HP code as part of our code" (C-74). Which client ships is still open, and C-74 leaves it as a design choice for the kick-off. Of lane A's five, this is the real kick-off choice (K-1). The client on main (pull requests 37, 41) is Datasec's own; its service files were taken from HP's OXPdLib jar (B2024 F4).  
**Options: **(a) HP's OXPdLib (.NET), shipped unchanged as the design first said. (b) Datasec's own client, the one the lab uses now.  
**We recommend:** (b): it is built, reviewed and tested, and it is the code the M577 run will prove. **Meanwhile the build:** Datasec's own client, for the lab only. The product adapter waits for this answer.  
<sub>Source: C-74; 02 change log B2019 (K-1); history.md 2026-11-23 20:47; B1996 design review 5 question 3 and amendments A9, A10, A15; 02 C3 and R16</sub>


| Answer Q32 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q32 - left for kickoff  <br>**Still open; decision tonight:** &nbsp; |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q33** | **Is a Datasec-hosted licence server an allowed exception to "everything is deployed in the client's tenant"?** A6 gives two licence-server options, through Azure or through Datasec (C-58 paragraph 17). A4 puts everything in the client's tenant (paragraph 15). The Datasec-hosted option is not in the client's tenant. <sub>Source: 05:202 (P-7); C-58 paragraphs 15 and 17</sub> | (a) Yes, the licence server is the one exception. (b) No, it is always deployed in the client's tenant. **We recommend: (a), since the licence service is Datasec's own control point. Meanwhile: Datasec's own licence service, as designed. Nothing new is built.** | &nbsp; |

### Printers and lab

**Q34. How do we get an OXPd 2 printer or HP's simulator into the lab?**

**Why it matters: **By HP's firmware notes the M577 is OXPd 1.x (FutureSmart 5; not yet read from the device), so the newer-printer panel test (S4, Chromium) cannot run on it. No OXPd 2 printer or simulator is in hand, so every OXPd 2 component is tested on stand-ins only.  
**Options: **(a) A FutureSmart 6 printer from the Workpath product owner's lab (W4). (b) HP's simulator: you download the image, and HP must release the guide (the download was refused; H5). It runs on the Windows PC (Q52). (c) Buy or borrow a FutureSmart 6 printer, with the cost on a card first.  
**We recommend:** (a) and (b) together. Name an owner and a date tonight. **Meanwhile the build:** OXPd 2 work continues on stand-ins. No OXPd 2 claim is made.  
<sub>Source: 03 phase 0 (spike S4) and its B2020 progress section; 05:227-228 (kit items 3, 4); B1996 design review BLUF 5</sub>


| Answer Q34 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q34 - we have multiple printers ready.  Versions prior to OXPd 2 can be tested now.  We will chase HP for OXPD 2 tools, packages, firmware.  Please list this as an action on Kamil |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q35** | **Confirm: the plan's working order changes so the older-printer slice leads on the M577, and OXPd 2 work stays on stand-ins.** By HP's firmware notes the M577 runs FutureSmart 5 only, so it is an OXPd 1.x printer (one reader's finding; its firmware has not been read from the device). That differs from your note P2, which expected to wipe it for developer mode. Please confirm tonight. You already approved the M577 runs (C-72, C-76). <sub>Source: B1996 design review BLUF 5 and question 4; BACKLOG.md owed item 92; C-72</sub> | (a) Confirm. (b) Keep the plan's order. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q36** | **By what date can it be there, and who owns getting it?** Without a date there is no date for any OXPd 2 proof. <sub>Source: 03 phase 0 (spike S4) and its B2020 progress section; 05:227-228 (kit items 3, 4); B1996 design review BLUF 5</sub> | A date and a name. **We recommend: A date and an owner named tonight. Meanwhile: No date.** | &nbsp; |
| **Q37** | **Which certificate authority does the lab use for the M577: our own development CA, or one you name?** HP warns that self-signed certificates are "not recommended/supported" in a printer's OXPd CA store (report B2012 section 4, relayed). The first-run step that imports a CA waits on this. <sub>Source: 03 section 0, row 5 (B2020); report B2012 section 4</sub> | (a) Our development CA, removed after the test. (b) A CA you name. **We recommend, and meanwhile: (a), on the M577 only.** | &nbsp; |
| **Q38** | **How do we stay current with HP firmware updates?** Your own question, with your ruling to accept unknown values (C-61): "how do we stay up to date with updates". HP controls what reaches the printer, and a new firmware can change what a printer sends. <sub>Source: C-61 (his note, recorded as not answered)</sub> | (a) The Workpath team's existing watch on HP releases also covers OXPd (W27 asks how they do it today). (b) The build team re-runs the lab tests on each new firmware. **We recommend: (a), with (b) for each firmware the lab printers take. Meanwhile: Unknown values are read as unknown and never count as success (C-61).** | &nbsp; |

### Commercial and HP

**Q39. Which of the eight drafted HP asks (H1 to H8, listed at the end of Part 2) do you send now?**

**Why it matters: **Nothing has been sent to HP. You send anything to HP yourself, through the portal or by escalation (C-58 paragraph 7). H3 asks for the four dates that gate OXPd 2. H5 asks for lab access: the debug-bridge key, the simulator and its guide.  
**Options: **Send all eight, send some (by number), or hold them all.  
**We recommend:** Send H3 and H5 now. H6 can drop its licence points, which C-74 answers. **Meanwhile the build:** Nothing is sent.  
<sub>Source: HP_QUESTIONS_DRAFT.md; QUESTIONS_BY_OWNER v2 H1-0 to H8-0; C-74</sub>


| Answer Q39 |
|---|
| **Your answer, 2026-11-24 morning (verbatim):** q39 - everything goes out now.  Add as a task for Kamil. |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q40** | **Did HP's confirmation (C-30, "Yes, HP confirmed") cover signing, meaning a route and a date, or only HP's position on the approach?** This decides how much weight to put on a release date for the newer printers. <sub>Source: 05:57 (question 1); 03 section 8.3 (OQ-1); QUESTIONS_BY_OWNER v2 P1-1 to P1-5</sub> | (a) Only HP's position on the approach. (b) Also a signing route and a date. **We recommend: (a), unless you hold something in writing from HP that says more. Meanwhile: (a).** | &nbsp; |
| **Q41** | **Is HP's confirmation written down anywhere we can file?** The only evidence for it is your answer (05:118, "HP's written confirmation is not in the library"). <sub>Source: 05 "What was not verified"; QUESTIONS_BY_OWNER v2 P1-3</sub> | (a) Yes, here it is. (b) No, it was verbal. **We recommend: If verbal, ask HP for it in writing (H1). Meanwhile: Nothing is filed.** | &nbsp; |

### For Kam alone, after the meeting (defaults stand until then)

Engineering defaults and points about your own PC or files. None needs the team. K-3, K-4 and K-5 are gaps not yet built, not choices made against the design.

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q42** | **Is the adapter-to-core event and command interface built before more printer work, or after the M577 first run?** The device model and registry are built (pull requests 12, 25, 30). The interface through which both printer adapters talk to the core (02 section 5.4, D2) is not, and the server host references only the OXPd 2 adapter; the lab tool references the 1.x adapter. A gap not yet built (K-3). <sub>Source: 02 section 5.4 and D2; 02 change log B2019 (K-3)</sub> | (a) Next, before the step 2-4 write lanes. (b) After the M577 first run, so both generations shape it. **We recommend: (b). Meanwhile: Not built.** | &nbsp; |
| **Q43** | **On a Linux server, what makes the secret store's key file "sealed" to the machine?** The design says "sealed" and no more (C15, D28). Built today: a key file only its owner can read, which nothing binds to the machine, and no TPM or Key Vault provider. A gap not yet built (K-4). <sub>Source: Jira OXPD2-1 comment 41450 (RP-2); 02 change log B2019 (K-4); WP1.1</sub> | (a) The owner-only file, as built, on an encrypted disk. (b) A key bound to the machine (TPM). (c) Azure Key Vault where the server runs in Azure (Q21). These options are this pack's, not the review's. **We recommend: (c) in Azure and (b) on site, settled with the packaging (Q13). Meanwhile: The owner-only key file.** | &nbsp; |
| **Q44** | **Which DPAPI-NG protection descriptor does a stand-alone Windows server get?** The design names a domain group for the pair only. The library call with no descriptor was refused on the hosted Windows build, so that test skips itself. <sub>Source: Jira OXPD2-1 comment 41450 (RP-3); WP1.1; WP5.1</sub> | (a) The machine itself. (b) A domain group. **We recommend: (a), settled in packaging (WP5.1). Meanwhile: No descriptor; the Windows test is skipped.** | &nbsp; |
| **Q45** | **Which descriptor does a two-server Windows pair get?** As the item above. <sub>Source: Jira OXPD2-1 comment 41450 (RP-3); WP1.1; WP5.1</sub> | (a) A domain group, as the design names. (b) Another you name. **We recommend: (a). Meanwhile: Not built.** | &nbsp; |
| **Q46** | **Is the logging filter's cost acceptable? On 230 sample events holding no secret, 108 lost at least one harmless value.** The filter strips anything that could be a secret from the logs. It also strips harmless values (223 of 1,210), which makes support harder. <sub>Source: Jira OXPD2-1 comment 41450 (RP-5); WP1.10</sub> | (a) Accept: privacy first. (b) Tune the filter so fewer harmless values go, with a new review. **We recommend: (a) now; tune once real printer logs exist. Meanwhile: The filter as built.** | &nbsp; |
| **Q47** | **Should the print-job stream have a ceiling on fetches, or on time, per document?** There is none. An answer that gives one byte and then fails resets the retry count, so one document can be fetched without end. <sub>Source: Jira OXPD2-1 comment 41450 (RP-7); WP4.2; BACKLOG.md owed item 40</sub> | (a) Yes, a ceiling. (b) No ceiling. **We recommend: (a). Meanwhile: No ceiling.** | &nbsp; |
| **Q48** | **Confirm only: Do your words "we can store them where we want" also cover HP's older-printer (OXPd 1.x) service files, now in the repository?** C-56 named HP's OXPd 2 specification files. Pull requests 37 and 43 added HP's OXPd 1.x description files on the coordinator's reading of C-56, with leave for you to correct it (owed item 86). <sub>Source: C-56; history.md 2026-11-23 20:47 (pull request 37); BACKLOG.md owed item 86; B1996 design review 5 question 5</sub> | (a) Yes, they stay. (b) No, they move out of the repository. **We recommend: (a). Meanwhile: (a), as the coordinator read it.** | &nbsp; |
| **Q49** | **For older printers, does the client default to WS-Addressing 1.0 (as built, from HP's service files) or to the 2004 version (as the design says)?** Two HP sources disagree: HP's prose specification says the 2004 version, HP's service files use 1.0. The built client sends 1.0 by default with a 2004 switch (pull requests 37, 40). Neither is measured (K-2). <sub>Source: 02 section 4 (K-2); 02 change log B2019; B1996 amendment A11</sub> | (a) Keep 1.0 as the default, and let the M577 first run decide. (b) Change the default to 2004. **We recommend: (a). Meanwhile: 1.0, with the 2004 switch.** | &nbsp; |
| **Q50** | **Should the older-printer client judge the model and firmware it reads (for example refuse below FutureSmart 4.7) before the write lanes?** The built read returns the model and firmware, but nothing judges them; the discovery tree is fetched but not interpreted. A gap not yet built (K-5). <sub>Source: 02 change log B2019 (K-5)</sub> | (a) Yes, before the write lanes. (b) Later. **We recommend: (a). Meanwhile: Read, not judged.** | &nbsp; |
| **Q51** | **Your ruling to revisit strict reading after the printer test (C-63): does that revisit move to the first OXPd 2 printer or simulator run?** C-63 concerns OXPd 2 printer answers. The M577 is OXPd 1.x, so Monday's test cannot meet the revisit point. <sub>Source: C-63; B1996 amendment A16; BACKLOG.md owed item 92</sub> | (a) Yes, revisit at the first OXPd 2 run. (b) Revisit now, without traffic. **We recommend: (a). Meanwhile: Strict, as ruled.** | &nbsp; |
| **Q52** | **May Virtual Machine Platform be switched off on the Windows PC used for HP's simulators?** The older-printer simulator needs Windows with VMware. Virtual Machine Platform was ticked, and the VMware evaluation had ended (C-53). The change was asked and not answered (C-54). <sub>Source: C-49; C-52; C-53; C-54; 05:226 (kit item 2)</sub> | (a) Yes. (b) No, use another machine. **We recommend: (a). Meanwhile: Nothing is changed on the PC.** | &nbsp; |
| **Q53** | **May VMware on that PC move from the evaluation to the free licence?** As the item above. <sub>Source: C-49; C-52; C-53; C-54; 05:226 (kit item 2)</sub> | (a) Yes. (b) No, use another machine. **We recommend: (a). Meanwhile: Nothing is changed on the PC.** | &nbsp; |

## Part 2: information we need from the Workpath team

What only the Workpath team (Datasec's own team behind the HP Workpath apps and HPAM; C-45) can give us. Each row is a place where the design states how today's product behaves from a video, the manual or a reading of code, rather than from the product's own people, configuration or a printer. In the meeting give each row an owner and a date; the team can fill the boxes in afterwards. Format: A = an answer in words, D = a document or file, C = a configuration or sample data, T = a test account or device, S = a walkthrough session.

### Keys, lab and tenant (these block phase 0)

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W1** | Is the store build of HPAM and of the phone app made from the 4.4.1 source unchanged, so that the card key compiled into that source is the live key? | The first item on the master list since C-41. You said the keys in the library are old and rotated (C-3). This one is compiled into the shipped source and cannot be rotated without re-enrolling cards, so we ask the team to confirm. Card sign-in in phase 1 waits on it. <sub>Source: 05:105-109 (question 8); 03 section 8.3; C-41</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w1 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W2** | Which family of card-decoding routines produced the card strings today's customers have stored: the older one (firmware before Android 12) or the newer one (Android 12 firmware)? | The two give different strings from the same card in 7 of 13 compared inputs. Cards enrolled under the other family would read as not known on every OXPd printer, though nobody would be signed in as someone else. Built today: the older routines. <sub>Source: Jira OXPD2-1 comment 41450 (RP-1); WP1.3</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w2 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W3** | For each printer in the Workpath product owner's lab: model and firmware version. | Fills phase-0 kit items 4, 7, 8 and 9: one FutureSmart 6, one FutureSmart 5 without Workpath, one FutureSmart 4.7 and one Workpath printer with the current suite. <sub>Source: C-58 paragraph 8; QUESTIONS_BY_OWNER v2 A23-7; FQ-16; 05:228-233</sub> | D (a table) | **Your answer, 2026-11-24 morning (verbatim):** w3 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W4** | When and where can the build use a FutureSmart 6 printer that may be put into developer mode? | Every OXPd 2 claim is untested until one exists (by HP's firmware notes the M577 is OXPd 1.x). Kit items 4 and 17. <sub>Source: 05:228 (kit item 4); 05:241 (kit item 17); B1996 design review 5 point 10</sub> | T + A | **Your answer, 2026-11-24 morning (verbatim):** w4 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W5** | Who is at that printer's panel during the tests? | As the item above. <sub>Source: 05:228 (kit item 4); 05:241 (kit item 17); B1996 design review 5 point 10</sub> | T + A | **Your answer, 2026-11-24 morning (verbatim):** w5 - Steve M |
| **W6** | Which card readers can the lab lend: one of each of the eight products in the reader table? | The card decoders (pull request 3) are checked against golden values only. Real readers settle them (spike S3, exit test E1.3). <sub>Source: 05:234 (kit item 10); BACKLOG.md owed item 41</sub> | T | **Your answer, 2026-11-24 morning (verbatim):** w6 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W7** | A test Microsoft tenant set up as customers have it: the HPAM registration, Universal Print licences, the "Onboarding Azure Services" deployment, Conditional Access policies, and a test user with Authenticator. | The M577 panel sign-in test needs a test tenant user (C-76). Tests of the gateway, permissions and reporting need the rest (kit item 11). <sub>Source: 05:235 (kit item 11); C-76; C-58 paragraph 31 (A23)</sub> | T | **Your answer, 2026-11-24 morning (verbatim):** w7 - we build against kamil@datasec-rd.com.  full environment simulated.  Using my printer so we control.  Final testing will be done against Datasec testing lab |

### How today's product signs users in

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W8** | A walkthrough of every sign-in path on a V4.4 Workpath printer: MFA and No-MFA, card, QR, BLE, security key and first-use self-registration, under each setup option. | You called this critical (P3: "It is critical you understand and document these"). The design holds 11 Lightning Talk transcripts and the manuals, with no video file and no screen seen (B1812 records). It unblocks Q23 to Q27 and test 1. <sub>Source: C-58 paragraph 12; 02 section 1; 02 change log, B1817 open questions; Review/B1812_Q_FOR-RECORDS:198-212</sub> | S (recorded) or the videos by Will | **Your answer, 2026-11-24 morning (verbatim):** w8 - you have videos and documentation on this.  If more information is necessary list the action on me and I will arrange.  You will need to specify what format is best.  If its a technical doc (swim lane diagrams) create a Jira ticket and assign to Steve M but for him to assign to Artur M. Utilisation of the work path team should go through Steve first |
| **W9** | Do customers on V4.4 see the Passkey button, and which sign-in method does it use? | No document shows the button. Requirement F12 is kept but not built until this is known. <sub>Source: 02 change log, B1817 open questions (N-11)</sub> | A + screenshot | **Your answer, 2026-11-24 morning (verbatim):** w9 - no but discussion shoudl be had.  create a Jira ticket (with the question) and assign to Steve M - 2 week time request <br>**Still open; decision tonight:** &nbsp; |
| **W10** | The Conditional Access policy templates customers use, and the "Passwordless MFA" fix as customers are given it. | Today a policy for Android or iOS catches the printer. Whether an OXPd printer matches the same platform is UNMEASURED (spike S7). <sub>Source: 02 section 7.1</sub> | D | **Your answer, 2026-11-24 morning (verbatim):** w10 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W11** | The Microsoft Graph permissions a customer tenant has actually consented to, from a customer tenant or the deployment guide. | The permission names are inferred, not read from code. This sets the first-run scope check and OneDrive's "Shared with me" (OP-20). <sub>Source: 02 section 7.2; 05:185 (OP-20)</sub> | C | **Your answer, 2026-11-24 morning (verbatim):** w11 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |

### Universal Print, licensing and deployment

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W12** | Who owns and administers Datasec's Universal Print app registration? | Needed for Q22 (Datasec's registration or each customer's). Phase 4 (Universal Print) waits on it. <sub>Source: 05:111-115 (question 9); QUESTIONS_BY_OWNER v2 A4-2 to A4-4</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w12 - Steve M.  But we will create our own as per w7 during dev |
| **W13** | Can Datasec add a permission or a redirect address to it without asking each customer? | As the item above. <sub>Source: 05:111-115 (question 9); QUESTIONS_BY_OWNER v2 A4-2 to A4-4</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w13 - I don’t think its relevant any more |
| **W14** | How does today's unattended Universal Print registration from a stored account work? | Needed for Q30. <sub>Source: 02 change log, B1817 open questions (N-12)</sub> | S or D | &nbsp; |
| **W15** | Are Universal Print job status and page counts reported for Secure printers only today, or for Direct and Standard as well? | This rests on an assumption in an analysis report. It decides whether DEV-17 (Q31) is a deviation at all. <sub>Source: 02 section 3.4; DEVIATION-REGISTER_DRAFT.md:35</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w15 - all reporting is done through microsoft log analytics.  Clients can use Nexus for added clarity and reports but they have choice <br>**Still open; decision tonight:** &nbsp; |
| **W16** | Which deployment tool do customers get today: HP AuthSuite Manager or the HPK Deployment Utility? | Needed for Q14. "Newer" points to the Manager by file date and to the Utility by version number. <sub>Source: 05:201 (P-6, N-9); 02 section 8.7</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w16 - be very specific with the ask.  create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W17** | Who owns and releases that tool? | The Utility's workflow installs .NET SDK 8 for a .NET 10 project, and whether it builds is not established. The Manager was not built. <sub>Source: QUESTIONS_BY_OWNER v2 A15-2 to A15-5; 02 section 8.7; WP0.10:69-70</sub> | A + build result | **Your answer, 2026-11-24 morning (verbatim):** w17 - Steve M |
| **W18** | Does it build today on a clean Windows machine? | As the item above. <sub>Source: QUESTIONS_BY_OWNER v2 A15-2 to A15-5; 02 section 8.7; WP0.10:69-70</sub> | A + build result | **Your answer, 2026-11-24 morning (verbatim):** w 18 - yes |
| **W19** | A walkthrough of the Manager by its authors, four points, one line each in the box: (1) does it import existing .cfg files; (2) how could a package kind beside the six fixed Workpath ids be added; (3) its job database; (4) its password and TLS handling. | Sizes the OXPd amendment (WP0.10, WP5.8). Whether the Manager reads .cfg files is UNMEASURED. <sub>Source: 02 section 3.5, 02 section 8.7; WP0.10:42-50, 87-91</sub> | S | **Your answer, 2026-11-24 morning (verbatim):** w19 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W20** | How many customers deployed the Azure side through the Marketplace offer, and how many through the script? | Every gateway change ships both ways until this is known. <sub>Source: 05:173 (OP-8); 05:211 (N-17)</sub> | A (two numbers) | **Your answer, 2026-11-24 morning (verbatim):** w20 - not many through marketplace but its the path we want to push |
| **W21** | Does any customer run their own licence server today? | This bears on Q33 and on the two licence-server options (A6). <sub>Source: QUESTIONS_BY_OWNER v2 A6-2; FQ-11</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w21, w22, w23 & W24 - ask Steve M how it works. create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W22** | The licence portal's source code. | Not sent. Nothing shows how a printer app checks a licence, so the server's licence check is designed from the old back end. <sub>Source: 02 section 7.5; QUESTIONS_BY_OWNER v2 A6-3</sub> | D (repository access) | **Your answer, 2026-11-24 morning (verbatim):** w21, w22, w23 & W24 - ask Steve M how it works. create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W23** | How does a printer app check its licence against the portal? | As the item above. <sub>Source: 02 section 7.5; QUESTIONS_BY_OWNER v2 A6-3</sub> | D (repository access) | **Your answer, 2026-11-24 morning (verbatim):** w21, w22, w23 & W24 - ask Steve M how it works. create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W24** | What does a Workpath printer do when its licence expires? | Fielded printers appear to fall back to a 20-day temporary state [A5]. The same behaviour is planned for OXPd (C-20). <sub>Source: 02 section 7.5</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w21, w22, w23 & W24 - ask Steve M how it works. create a Jira ticket (with the question) and assign to Steve M - 2 week time request |

### Scope, pilot and operations

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W25** | Three points, one line each in the box: (1) does any customer use HPAM as the sign-in for HP Advance or LRS VPSX; (2) if so, how many; (3) for which of the two. | Needed for Q8. <sub>Source: 05:81; QUESTIONS_BY_OWNER v2 A3-1 to A3-3</sub> | A | &nbsp; |
| **W26** | What defect level does the team accept before calling a Workpath pilot a success? | Needed for Q5. Your answer A24 gives the aim and no number; the questions document put the number to the team because they hold today's practice. <sub>Source: QUESTIONS_BY_OWNER v2 A24; FQ-15</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w26 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W27** | How does the team track new HP firmware today and re-test the Workpath apps on it? | Needed for Q38. <sub>Source: C-61</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w27 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W28** | Real fleet sizes, sign-ins per hour and peak load at today's largest customers. | The server sizing (4 vCPU, 8 GB) is inferred. Load test E6.3 assumes 500 devices and 20 sign-ins a minute. <sub>Source: 02 section 5.8; 02 section 8.1</sub> | C | **Your answer, 2026-11-24 morning (verbatim):** w28 - not relevant as client environment |
| **W29** | Datasec's runbook for moving a customer from one sign-in solution to another (Workpath to OXPd). | The design assumes the advice today is "a format", plus removing the printer's cloud record in Command Centre. <sub>Source: 02 section 8.5</sub> | D | **Your answer, 2026-11-24 morning (verbatim):** w29 - needs discussion.  action on Kamil <br>**Still open; decision tonight:** &nbsp; |

### What the apps do on a printer today (parity details)

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W30** | Is OneDrive's "Shared with me" in the shipped OneDrive 4.4? The release notes say it was removed. | It is in the rebuild on the strength of the source alone (C-16). <sub>Source: 02 change log, B1817 open questions (N-10)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W31** | On a panel set to a language other than English, do the OneDrive and SharePoint apps show their own screens in that language? | English is the phase-1 language (A18). The answer decides whether that is less than a full match. <sub>Source: FQ-1 (a follow-up question on the master list, Jira OXPD2-1); 05:186 (OP-21); C-58 paragraph 26 (A18)</sub> | A + photo | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W32** | Has any shipped Mailflow version shown "quick messages" on the panel? | They are switched off in the code and left out (05 question 3). You said you would ask the team (A19). <sub>Source: FQ-2, FQ-3; C-58 paragraph 27 (A19)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W33** | If yes, which version (a photo is enough)? | As the item above. <sub>Source: FQ-2, FQ-3; C-58 paragraph 27 (A19)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W34** | In SharePoint 4.4.6, how many of a library's custom fields can be filled in at the panel when scanning? The manual says four; the code has no limit. | Sets the SharePoint scan screen. You asked for this follow-up (A20). <sub>Source: FQ-4; C-58 paragraph 28 (A20)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W35** | In OneDrive, does pressing Back at the list of sites show a sign-out confirmation screen on a printer? | The code has the screen; nobody has seen it on a printer (A20). <sub>Source: FQ-5; C-58 paragraph 28 (A20)</sub> | A + photo | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W36** | A walkthrough of the panel's admin menu as customers use it for card emulation and app settings. | DEV-15 and DEV-16 (Q31) move both to the server console. The team knows how often customers use them at the panel. <sub>Source: 02 section 3.2, 02 section 3.3; DEVIATION-REGISTER_DRAFT.md:33-34</sub> | S | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W37** | Do the HID OMNIKEY 076B:5428 and Inepro 1DA6:0110 readers decode on a Workpath printer today? | They are kept in the reader table only if Workpath decodes them today. <sub>Source: 02 section 3.2</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W38** | The current meanings of error codes AI01 to AI09 and the help article they point to. | The help texts come from the old back end. Requirement F21. <sub>Source: 02 section 3.2</sub> | D | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W39** | A review of eight "as coded" behaviours of today's Universal Print release code, plus one UUID-parsing question. Which are intended and which are bugs? | The rebuild copies them unless told otherwise. Examples: Acknowledge-Job carries no printer-uri, and a failed open is never retried. <sub>Source: Briefs/2026-11-20_B1788_STATUS.md:274-284; Briefs/2026-11-20_B1810_STATUS.md:317</sub> | A (per item) | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W40** | Does the Universal Print service ever answer with an attribute group other than operation, job, printer or unsupported? | The reader now tolerates other groups. The answer says whether that path is ever used. The team's logs may show it. <sub>Source: Jira OXPD2-1 comment 41450 (RP-6); Briefs/2026-11-20_B1788_STATUS.md:285-287</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |

### Reporting

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W41** | The field list of the job record the apps send to Log Analytics (StatisticsJobData and Supply), or real exported rows from a test or customer workspace. | The list exists only inside a compiled HP SDK, so the OXPd report map (WP0.8) is UNMEASURED in 47 places. <sub>Source: WP0.8:12, 21-35, 45, 61-64</sub> | C | &nbsp; |
| **W42** | Has any customer changed the data-collection rule or tables from the template? | A customer's live rule may differ from the template, and the report rows have to match what those queries read. <sub>Source: WP0.8:51-57, 70</sub> | C | &nbsp; |
| **W43** | Which queries do the customer reports and workbooks run? | As the item above. <sub>Source: WP0.8:51-57, 70</sub> | C | &nbsp; |

Your line with no item number, shown here because it sits between W40 and W44 in your file (verbatim): "reporting - managed by Kamil.  all actions / questions directed to Kamil on fleet activity". Whether it answers W41 to W43 is not certain, so their boxes are kept.

### HP accounts and earlier work

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W44** | Does Datasec have an HP App Center enrolment? | This is the route the OXPd 2 submission will take (Q3, H2). You hold an HP developer account (C-50). App Center was not answered. <sub>Source: QUESTIONS_BY_OWNER v2 A21-2, A21-3; 02 section 4; HP_QUESTIONS_DRAFT H2.1</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w44 - yes |
| **W45** | Who holds its master administrator account? | As the item above. <sub>Source: QUESTIONS_BY_OWNER v2 A21-2, A21-3; 02 section 4; HP_QUESTIONS_DRAFT H2.1</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w45 - Steve M |
| **W46** | How are Workpath bundles validated and signed today? | As the item above. <sub>Source: QUESTIONS_BY_OWNER v2 A21-2, A21-3; 02 section 4; HP_QUESTIONS_DRAFT H2.1</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w46 - submitted to HP validation team for testing and approval. then listed in app distribution catalogue |
| **W47** | Is the Intune edition of the phone app needed, and if so where is its source? | Only the standard edition's source is in hand (report A12 section 7.2). <sub>Source: 05:278</sub> | A or D | **Your answer, 2026-11-24 morning (verbatim):** W47 - no |
| **W48** | Is the printer admin password in the earlier OXPd 1 repository's README the live password of a lab printer? | Treated as live and never copied. Whoever owns that printer should change it. <sub>Source: 05:179 (OP-14)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w48 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request |
| **W49** | Where did the two card keys written into the earlier OXPd 1 build come from? | They are not today's Workpath card key. They are treated as made up or outdated. <sub>Source: 05:181 (OP-16)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w49 - this would have been part of testing.  ignore |
| **W50** | (Your own check, A12.) Was the earlier OXPd 1 code ever run on a physical printer? | You said "I do not believe so but I will check" (A12). Nothing in that code is treated as proven on hardware. <sub>Source: 05:180 (OP-15); C-58 paragraph 22 (A12)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w50 - no |
| **W51** | Which "emulator" did its author use? | As the item above. <sub>Source: 05:180 (OP-15); C-58 paragraph 22 (A12)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w51 - prior work did not go far.  ignore it |
| **W52** | Is the empty repository OXPD1 meant to receive anything? | Ignored meanwhile; new work goes to datasecau/OXPd_2. <sub>Source: 05:183 (OP-18)</sub> | A | &nbsp; |
| **W53** | Has the team received from HP any OXPd 1.x SDK newer than 1.8.4.1? | Question 12 of 05; the older-printer contracts are built from 1.8.4.1. H7 stays for HP's own roadmap. <sub>Source: 05:138 (question 12)</sub> | A | **Your answer, 2026-11-24 morning (verbatim):** w53 - the project files should have included 1.9 |

### Only HP can answer these (not for this meeting to send)

These stay in Registers/HP_QUESTIONS_DRAFT.md. Nothing has been sent; you send anything to HP yourself (Q39). Listed so the meeting can see what waits on HP.

| Id | What only HP can answer | Where it is kept |
|---|---|---|
| H1 | Written confirmation that a server (not the printer) calling Microsoft 365 is eligible for OXPd 2 validation and signing. | HP_QUESTIONS_DRAFT H1 |
| H2 | App Center coverage of OXPd 2, a validation contact, the submission route, and what must be signed first. Datasec's own enrolment is W44. | H2 |
| H3 | Dates for production FutureSmart 6 firmware, an accepted platform version, a working signing service, the turnaround, the model list and a production SDK. | H3 |
| H4 | A first signing round with fewer than the seven printer groups; loan printers; whether the simulator counts. | H4 |
| H5 | Lab access: the LaserJet Debug Bridge service key, the simulator image and its guide (download refused, HTTP 403), pilot firmware. | H5 |
| H6 | The OXPd 2 SDK terms, own client code, shipping HP's library, and beta confidentiality. C-74 settles using HP code in Datasec's code. | H6 |
| H7 | OXPd 1.9: available, when, what it changes, and the support period for OXPd 1.x. This is also question 12 of 05: anything newer than 1.8.4.1. | H7; 05:138 |
| H8 | Technical points: whether the token survives a reboot, the same-id upgrade, priority print, browser cookies between users, the trusted-site CA store, and the USB record type. | H8 |

## Appendix A: questions already answered, and dropped

Each subject below was an open question in the design documents or the questions document. Each was checked against CLARIFICATIONS.md and your notes of 2026-11-20 21:04, and has been answered. It is not asked again. Your words are quoted short. The full text is the C-entry.

| Subject | Answered by | His words (short) |
|---|---|---|
| The 25 first questions of 2026-11-18 (Q1 to Q25 of that list). Five are asked again in part, where your later words opened them: C-17 (Q13), C-24 (Q28), C-26 (Q12), C-29 (Q23, Q24), C-30 (Q40). | C-6 to C-30 | his taps, e.g. C-16 "Full match of everything"; C-20 "Same seat, any platform" |
| Sensitivity labels in the rebuild | C-38 | "Leave it out, as today" |
| Where the SharePoint app's source and the sign-in gateway's source are (OQ-7) | C-33, C-40 | "here are the Sharepoint repo"; "here are the repos" |
| Deployment uses Datasec's existing tool, not a new installer | C-43 | "Datasec has a deployment utility so you should use this or amend it" |
| What the MVP contains (first half of P4) | C-48, C-58 par. 13 | "product equivalent version of what is currently live with work path deployments" |
| Printer firmware version and whether it may be wiped (P2) | C-47, C-58 par. 9 | "anything about my printer can be changed, wiped or configured" |
| Who holds HP developer access, and how HP is reached (A21, first parts) | C-50, C-58 par. 6-7 | "I and each member of the workpath team have access"; "through their portal" |
| Where the lab is (kit items 4, 7 to 10) | C-58 par. 8 | "Steve M has every device, reader that we will need" |
| Datasec's commercial right to rework and distribute | C-58 par. 10 | "we have the commercial right to distribute and make profit" |
| A user acts with their own token and access (A2) | C-58 par. 14 | "it is their token and therefore their access to their apps" |
| Where the server runs: the client's tenant and Azure subscription (A4, P6, FQ-7) | C-58 par. 15; C-60 msgs 3-5 | "OXPd runs in the clients azure subscription" |
| A site with no internet (OQ-13) | C-58 par. 16 | "Phase 2 we will have a local server that allows for no internet.  For now, internet is essential." |
| Who deploys the licence-server offer (OP-7, A6) | C-58 par. 17 | "license server through Azure or Datasec.  2 deployment optiuons" |
| Is gateway package v1.3.0 live (OP-9, A8) | C-58 par. 19 | "yes" |
| The phone app's source (OP-10, A9); cc-api (OP-11) | C-58 par. 20 and its attachments | "Attached should be the one for HPAM" |
| More of the earlier OXPd 1 work (OP-13, A11) | C-58 par. 21 | "not much more than what has been provided" (answered in substance) |
| Where the amended tool lives (OP-5, A15) | C-58 par. 23 | "separate app but with the intention of integration after MVP" |
| May the amendment improve password handling for Workpath jobs (OP-6, A16) | C-58 par. 24 | "any improvement that is worth while is a good idea and will be done" |
| A Windows PC for the tool at a Linux-packaged site (OP-3, A17) | C-58 par. 25 | "yes for now" |
| Languages in phase 1 (the decision half of A18; the fact half is W31) | C-58 par. 26 | "assume English for phase 1" |
| The Microsoft step on the panel, not the phone | C-60 msg 1 | "if my ruling moved it to the phone that is a mistake" |
| One central server for several sites (OQ-11) | C-60 msg 4 | "one server per site on the customer's network is not inconsistent with them deploying through azure" |
| Keeping HP's OXPd 2 specification files in the repository | C-56 | "Keep HP's files in the repository" |
| Fetching the database packages; keeping the SQL Server sign-in packages | C-61, C-62 | "Fetch them once"; "Keep them (standard driver)" |
| Unknown values in printer callbacks; strict reading of printer answers | C-61, C-63 | "Accept unknown values"; "Keep both strict for now" |
| Deviation rows DEV-22 and DEV-23 (card store fails safe) | C-70 | "Approve both rows" |
| Agents drive the M577 for the older-printer tests | C-72 | "Agents drive it" |
| May HP code be used in Datasec's code (licence half of H6, N-16) | C-74 | "our license / commercial agreement allows us to use HP code as part of our code" |
| One Azure test resource to measure the printer path | C-75, C-78 | "One Azure test resource now"; "Create it as designed" |
| How the older-printer sign-in is first tried | C-76 | "Test the panel on the M577 first" |
| Old register and unregister tools as a lab probe (OP-17). Overtaken by the build, not answered by you | pull requests 34, 40, 41, 44 | the lab tool is our own; the old tools are not used |
| Does "full match" mean what ships today, and no more (question 3 of 05, OQ-3) | C-48; C-58 par. 13 | "currently live with work path deployments"; "same functionality as currently in the market" |

## Appendix B: sources read

- OXPd_2: CLAUDE.md; CLARIFICATIONS.md C-1 to C-78 (whole); your notes of 2026-11-20 21:04; Design 05 (lines 1 to 300), 02 and 03 (open-question sections, 8.7, change logs; their before-copies .pre-1124), WP0.8, WP0.10; Registers (deviation register, HP questions, questions v2 model: 157 questions, 26 answered, 8 in part); Review B1812 and B1817; BACKLOG.md (97 owed items, 67 open); history.md; Briefs B1788 and B1810 STATUS.

- Also: GitHub pull requests 1 to 44 and main b0b26b60 (GET); Jira OXPD2-1 (GET); Tuesday NEXT-PICKUP DELTA 1381 to 1389; gate verdict B2016; design review B1996; lane A’s B2019 contradictions K-1 to K-5 (relayed by Tuesday).

## Appendix C: what this pack could not establish

- Nothing here was checked on a printer, a simulator or a tenant; how today's product behaves comes from documents, transcripts or code, which is why Part 2 exists.

- The test count (2,093, 0 failed) is relayed from Tuesday's landing read of b0b26b60; history.md stops at pull request 42 (2,054). The M577's generation is one reader's finding from HP's firmware readme (B1996), not read from the device.

- BACKLOG.md holds further engineering points "decided by nobody" (owed items 34, 40, 41, 44, 46, 49, 57, 72, 73 among them), left to the coordinator. Jira OXPD2-1 was read by GET only; RP-4 (the log scanner and a named pipe) is left to the coordinator.

- The Word file was not opened in Word or Pages (neither is installed here); it was checked by program: every part well-formed, each answer box an unlocked content control with a unique id. The PDF is a reading copy (headless Chrome), without form fields.

- Citations of 02 and 03 are by section, mapped from their before-copies (.pre-1124), since today's updates moved the lines. K-1 to K-5 follow lane A’s 02 as worded after review B2024: K-1 is a kick-off choice; K-3, K-4 and K-5 are gaps not yet built; K-2 is two HP sources that disagree, neither measured.

- The recommendations, and the TONIGHT cut (from review B2023), are proposals for Tuesday and for you, not findings of fact.

