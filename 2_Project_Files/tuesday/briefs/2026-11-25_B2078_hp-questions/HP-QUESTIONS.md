# Questions for HP, as of 25 November 2026

<div style="margin-top:60mm; font-size:13pt; line-height:1.6">
<p><strong>Datasec</strong></p>
<p>Prepared for Kamil Kreiser, CTO</p>
<p>Every question Datasec holds for HP, checked against the project records on 25 November 2026</p>
<p style="margin-top:20mm; font-size:10.5pt; color:#555">Part 1: OXPd (8 asks, copy-ready)<br>Part 2: already answered, changed or struck<br>Appendix: HP Security Manager proof of concept (project on hold; listed for completeness)<br>Sources</p>
<p style="margin-top:10mm; font-size:10pt; color:#555">Nothing in this document has been sent to HP or to anyone.</p>
</div>

<div style="page-break-after: always"></div>

## BLUF

**Yes, the eight OXPd asks (H1 to H8) are current, with one exception: H1's wording should change before you send it.** The project records show none of the eight as sent. Your OXPd 2 lab and dates depend on them, so they are worth sending today.

- **OXPd, 8 asks.** 7 are **current** as worded on 24 November (H2 to H8). 1 is **changed** (H1). 0 are answered by HP. All 8 are **still with you to send**: the records hold no evidence that any of them went out. On 24 November at 10:35 you said you would send H5 and H3 "now". If you did, mark them sent. Only you can confirm it.
- **Changed: H1.** The 24 November text brought back a question that had been struck on 20 November: "is this approach acceptable to HP?". It was struck because it asks HP's permission for Datasec's own design, and HP has no approval step for OXPd 1.x. The corrected H1 below asks only for HP's statement in writing and two questions about HP's validation. Its opening line still needs your words: what HP told you, when, and how.
- **Send first:** **H5** (lab access) and **H3** (dates), as you chose on 24 November. Next **H2**, because its answer gives us the HP contact that H3, H4, H6 and H8 should go through. **H1** goes once you have filled in its opening line. **H4** and **H7** can go any time. **H6** and **H8** are the least urgent.
- **Before you send:** fill in H1's opening line, and put your HP developer account e-mail into H5 point 1.
- **Not yet asked, needs your call (2):** whether HP's certificate store accepts our self-signed development certificate (it bears on the first-run tests on the M577), and an optional question about HP's Token Proxy. Both are in Part 2.
- **HP Security Manager proof of concept (on hold until 10 December):** 20 asks in its register. 13 are still open, 3 were changed in meetings, 3 were answered in full or in part, and 1 was reversed. The register was last updated on 16 October, so check it before the project restarts. Details are in the Appendix.

<div style="page-break-after: always"></div>

## Part 1: OXPd: the eight asks, ready to send

Each block is one message. Copy it as it stands into HP's developer portal, or send it through your escalation contact. The numbering (H1 to H8) is the same as in every earlier version. The asks are listed in the order to send them.

### H5. OXPd 2 developer access

**Why we need it:** No OXPd 2 test can run without the debug bridge key, the simulator and FutureSmart 6 firmware. Your 12 January OXPd 2 date depends on them.

**State:** CURRENT. Not sent, per the records; you said on 24 November that you would send it. **Fill in before sending:** your HP developer account e-mail in point 1.

**Source:** HP-ASKS-TO-SEND.md:18-51; your choice of 24 Nov 10:35 (CLARIFICATIONS.md:970); Jira OXPD2-56 (open).

```
Subject: Datasec: OXPd 2 developer access (debug bridge key, simulator,
simulator guide, pilot firmware)

Hello,

We are setting up our OXPd 2 lab and are missing four things. Could you help
us get them, or tell us whom to ask?

1. LaserJet Debug Bridge service key. We understand it is requested from the
   developer portal and tied to a developer account. Is our account
   [your HP developer account e-mail] enabled for it, and is one key enough
   for a small team or does each developer need their own?
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

We understand that switching developer mode on or off removes every solution
from the printer, and that it needs someone at the control panel and outbound
internet access from the printer to HP. If there is anything else we should
know before we do it to a printer, please say.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H3. OXPd 2 production dates

**Why we need it:** Until HP dates these four things, we cannot give any customer a date for OXPd 2.

**State:** CURRENT. Not sent, per the records; you said on 24 November that you would send it.

**Source:** HP-ASKS-TO-SEND.md:53-90; CLARIFICATIONS.md:970; Jira OXPD2-56 (open).

```
Subject: Datasec: OXPd 2 production dates (firmware, platform version,
signing)

Hello,

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
Kamil Kreiser
CTO, Datasec
```

### H2. App Center enrolment for OXPd 2, and a contact for validation and signing

**Why we need it:** HP must sign an OXPd 2 bundle before it can go to customers. This ask gets us the contact and the submission route.

**State:** CURRENT, with your 24 November edit (point 1 now asks only whether our existing enrolment covers OXPd 2). Not sent, per the records.

**Source:** HP-ASKS-TO-SEND.md:128-158; your edit (CLARIFICATIONS.md:962; KAMIL-ACTIONS.r1.md:42); Jira OXPD2-57 (open).

```
Subject: Datasec: HP App Center for OXPd 2, and a contact for OXPd 2
validation and signing

Hello,

Datasec intends to submit an OXPd 2 solution for HP validation and signing.
Before we do, could you help us with the following?

1. Datasec is already enrolled in HP App Center. Does our enrolment cover
   OXPd 2 solutions, or is something more needed for OXPd 2? If more is
   needed, what are the steps and how long do they usually take?
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
Kamil Kreiser
CTO, Datasec
```

### H1. Written record of HP's position, and OXPd 2 validation

**Why we need it:** The OXPd 2 work rests on what HP told you about our approach, and none of it is in writing. We want it on file before our first submission, so that an HP reviewer cannot reopen HP's 2023 forum statement.

**State:** CHANGED. The 24 November text asked whether the approach "is acceptable to HP" and said "HP is comfortable with this approach". Both were struck on 20 November, after your statement that Datasec owns and controls this build. The wording below is the 20 November rework, with your sign-off. Not sent, per the records.

**Fill in before sending:** the opening line (what HP told you, when, how, and who). Nobody else knows this, and the questions about it are still open.

**Source:** corrected wording QUESTIONS_BY_OWNER.md:511-541 (reasons :16, :500, :889); the 24 Nov text HP-ASKS-TO-SEND.md:92-126; your answer "Yes, HP confirmed" (CLARIFICATIONS.md:182).

```
Subject: Datasec: written record of HP's position on our OXPd solution, and
OXPd 2 validation

Hello,

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
Kamil Kreiser
CTO, Datasec
```

### H4. A first validation round with fewer than seven tested printer groups

**Why we need it:** HP asks for testing on seven printer groups, and we have none of the FutureSmart 6 groups yet. This decides when our first submission can happen.

**State:** CURRENT. The draft's note "[adjust if this has changed]" has been removed: the records still show no FutureSmart 6 printer and no simulator in the lab (the M577 is a FutureSmart 5, OXPd 1.x printer). Not sent, per the records.

**Source:** HP-ASKS-TO-SEND.md:160-192; your answer to q34, "Versions prior to OXPd 2 can be tested now" (Jira OXPD2-56); Jira OXPD2-57 (open).

```
Subject: Datasec: first OXPd 2 validation round with fewer than seven tested
printer groups

Hello,

HP's publishing guidance for OXPd 2 asks for a solution to be tested on at
least one printer from each of five multifunction groups (A to E), and, for a
solution that handles sign-in, also on one from each of two printer groups
(F and G), on the latest firmware at the time of submission.

Our solution handles sign-in, so that is seven groups. Today we do not yet
have a FutureSmart 6 printer or the simulator in our lab. We will not declare
a group as tested when it was not.

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
Kamil Kreiser
CTO, Datasec
```

### H7. OXPd 1.x: anything newer than 1.8.4.1

**Why we need it:** OXPd 1.x ships first (20 December). We want to know whether HP has anything newer than the 1.8.4.1 SDK we are building on.

**State:** CURRENT, with your 24 November edit (it now asks for anything newer than 1.8.4.1, as your note said: "but I will request whether there is anything more recent"). Not sent, per the records.

**Source:** HP-ASKS-TO-SEND.md:213-239; your note of 24 Nov 10:26 (CLARIFICATIONS.md:922); Jira OXPD2-57 (open).

```
Subject: Datasec: OXPd 1.x SDK newer than 1.8.4.1, and OXPd 1.9
availability

Hello,

We are building on the OXPd 1.8.4.1 SDK for FutureSmart 4.7 to 5 printers.
An HP reply on the developer forum in March 2026 mentioned a "soon to be
released OXPd 1.9".

1. Is there any OXPd 1.x SDK newer than 1.8.4.1, released or in preview? If
   so, could we have it, or how do we get it?
2. Is OXPd 1.9 available to partners, as a release or a preview? If so, how
   do we get it?
3. If it is not out yet, is there a date, and what does it change for a
   solution that does sign-in with card readers, scanning and printing?
4. Would 1.9 change the lowest firmware a printer needs, or the rule that an
   OXPd 1.x solution needs no HP approval before it is deployed?
5. Is there a stated support period for OXPd 1.x on FutureSmart 4 and 5?

If nothing newer is available, we carry on with 1.8.4.1.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H6. OXPd 2 beta confidentiality

**Why we need it:** We want to talk to customers about OXPd 2 before its production release, without breaking any beta terms.

**State:** CURRENT, cut down on 24 November to this one question. You struck the licence points because our commercial agreement with HP already covers using HP code in our code (your ruling of 23 November). Not sent, per the records.

**Source:** HP-ASKS-TO-SEND.md:194-211; your ruling (CLARIFICATIONS.md:758); your edit (CLARIFICATIONS.md:962; KAMIL-ACTIONS.r1.md:41).

```
Subject: Datasec: OXPd 2 beta confidentiality

Hello,

We are building an OXPd 2 solution on the Beta 10 SDK and will start talking
to customers about it. Are there confidentiality terms for the beta that limit
what we may tell our customers about OXPd 2 before its production release?
If so, where can we read them?

A pointer to the documents is enough if this is already written down.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H8. Six OXPd 2 behaviour questions

**Why we need it:** Each answer settles a design point early. Each point also has a lab test of its own, so nothing waits on this ask.

**State:** CURRENT. Not sent, per the records. The least urgent of the eight. It could also go on the developer forum.

**Source:** HP-ASKS-TO-SEND.md:241-276; HP_QUESTIONS_DRAFT.md:375-388; Jira OXPD2-57 (open).

```
Subject: Datasec: six OXPd 2 behaviour questions (Beta 10)

Hello,

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
Kamil Kreiser
CTO, Datasec
```

<div style="page-break-after: always"></div>

## Part 2: already answered, changed, struck, or not yet asked

These are kept apart from the open asks above. None of them needs to go to HP as worded below.

**Struck or answered at home (no longer asked of HP)**

| Item | State | What settled it | Source |
|---|---|---|---|
| H1, old point 1: "Is an OXPd solution whose server calls Microsoft 365 acceptable to HP?" and the line "HP is comfortable with this approach" | SUPERSEDED | Struck on 20 November: it asked HP's permission for Datasec's own design, and HP has no approval step for OXPd 1.x | QUESTIONS_BY_OWNER.md:16, :500, :889 |
| H2, old point 1: "Is Datasec already enrolled in HP App Center?" | ANSWERED (by you) | Your answer: "yes" | ANSWERS-MAP.r1.md:176 |
| H2, old point 1: "Who at Datasec has to hold the master administrator account?" | ANSWERED (by you) | You named the Datasec holder | ANSWERS-MAP.r1.md:177 |
| H6, points 1, 2, 3, 5 and 6 (which agreement governs the SDK; our own client code written from HP's specifications; shipping HP's client library; shipping the 1.8.4.1 libraries; building endpoints from HP's service descriptions) | SUPERSEDED | Your ruling of 23 November: "our license / commercial agreement allows us to use HP code as part of our code"; struck by your edit of 24 November | CLARIFICATIONS.md:758, :962; KAMIL-ACTIONS.r1.md:41 |
| H7, old version (asked only about OXPd 1.9) | CHANGED | Widened to "anything newer than 1.8.4.1" by your note of 24 November | CLARIFICATIONS.md:922; HP-ASKS-TO-SEND.md:8 |
| Twelve factual questions (for example: FutureSmart 6 does not run OXPd 1.x; OXPd 1.x needs no HP approval; Beta 10 needs firmware 6.38.0.793; developer mode is not for customer sites) | ANSWERED (by HP's published documents) | HP's own guides and portal | HP_QUESTIONS_DRAFT.md:403-420 |

**Not asked yet: your call**

| Item | State | Why it is not in Part 1 | Source |
|---|---|---|---|
| Does HP's OXPd 1.x certificate store accept our self-signed development certificate? HP's own service description says self-signed certificates there are "not recommended/supported". | UNKNOWN (candidate) | It bears on the certificate step of the M577 first-run tests. The project records say a lab test or a question to HP can settle it, and only you send to HP. Say if you want it drafted as H9. | OXPd BACKLOG.md:756-760 |
| What is the HP Token Proxy, and does an on-premises solution need it? | CURRENT (optional) | An optional line under H2. Nothing waits on it, and the design does not use it. | HP_QUESTIONS_DRAFT.md:105; QUESTIONS_BY_OWNER.md:592 |
| Can HP supply interim firmware for older printers? | Not asked (by choice) | We test on public firmware, as you agreed | QUESTIONS_BY_OWNER.md:873 |

<div style="page-break-after: always"></div>

## Appendix: HP Security Manager proof of concept

**Project on hold (no work until 10 December); listed for completeness.** These asks come from the project's HP requests register. It was last updated on **16 October 2026** and has not been changed for this document. Every "not yet sent to HP" below is the register's wording as of that date. Check it before the project restarts. Recipients are as the register gives them.

| # | What we need from HP | State (register, 16 Oct) |
|---|---|---|
| HP‑1 | Corrected deck v3 slides (duplicates, wrong labels, cross-references, HP's own placeholders) | CURRENT: draft sent to you 27 Sep; not yet sent to HP |
| HP‑2 | Permission to use IDC's quote and logo (deck slide 91) | CURRENT: draft sent to you 27 Sep; not yet sent to HP |
| HP‑3 | The Customer Security Maturity questions | SUPERSEDED: on 29 Sep HP asked Datasec to propose the questions |
| HP‑4 | Security Manager: live access and an integration overview | CHANGED: now "Security Manager first, API/SDK docs" (1 Oct); access is through HP's Bangalore team (29 Sep); in the follow-up list to Steve, not yet sent |
| HP‑5 | Overview of Quick Assess | ANSWERED in part: Quick Assess is the full Security Manager capped at 100 devices (29 Sep) |
| HP‑6 | Control Hub: part of Security Hub? | CHANGED: Control Hub is a small-business tool; the ask is now for access (1 Oct) |
| HP‑7 | Firmware vulnerability tool: access, and how to integrate or upload results | CURRENT: owned by Steve (1 Oct); not yet sent |
| HP‑8 | Fleet Assessment tool: access and information | ANSWERED mostly, by the 1 Oct demo |
| HP‑9 | PO number and approval date | CURRENT: draft sent to you 1 Oct; not yet sent to HP |
| HP‑10 | Reactivate your HP account | CURRENT: draft sent to you 1 Oct; not yet sent to HP |
| HP‑11 | Access pack for you and the team | CURRENT: draft sent to you 1 Oct; not yet sent to HP |
| HP‑12 | FTA video, demo-asset zip, newer demo | CURRENT: draft sent to you 1 Oct; not yet sent to HP |
| HP‑13 | FTA syslog reference spreadsheet | CHANGED: Steve said on 2 Oct he will send it to you directly; no receipt recorded |
| HP‑14 | Running the FTA demo without HP VPN | ANSWERED (2 Oct): no VPN; HP gives an HPSM NFR licence and install docs, and Datasec hosts HPSM itself |
| HP‑15 | Session with Jason O'Keefe's team (remediation content) | CURRENT: not yet sent to HP |
| HP‑16 | HP reviewer for scoring, weights and traffic light | CURRENT: resent to you with the draft weights 1 Oct; not yet sent to HP |
| HP‑17 | Steve's agentic-AI draft; HP's AI-at-the-printer facts | CURRENT: not yet sent to HP |
| HP‑18 | Current generic partner Playbook deck; does it replace v3? | CURRENT: not yet sent to HP |
| HP‑19 | Amplify dates, venue, demo format | CURRENT: not yet sent to HP |
| HP‑20 | Introduction to Alexa; brand guidelines; collateral | CURRENT: not yet sent to HP |

**Counts:** 13 current, 3 changed, 3 answered (one in full, two in part), 1 superseded. There are also two candidates the register says you have not decided on yet: HP's approved policy or configuration examples, and HP logo use and its approval route.

## Sources

- HP-ASKS-TO-SEND.md: the eight asks as you approved them on 24 Nov (the 24 November send pack).
- KAMIL-ACTIONS.r1.md and ANSWERS-MAP.r1.md: same folder.
- QUESTIONS_BY_OWNER.md (20 Nov 16:10) and HP_QUESTIONS_DRAFT.md (20 Nov 13:29): OXPd_2/1_Project_Definition/Registers.
- CLARIFICATIONS.md, BACKLOG.md: OXPd_2 project records (read-only).
- Jira OXPD2-56 and OXPD2-57 (your two actions to send the asks): both open, last updated 24 Nov 12:02; read on 25 Nov.
- HP_REQUESTS_REGISTER.md (HPSM-POC), last updated 16 Oct 2026.
