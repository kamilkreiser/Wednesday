# B2027 KAMIL-ACTIONS: the actions Kam put on himself in his answers of 2026-11-24 (card drafts)

Written by the B2027 seat (Opus) for Tuesday, 2026-11-24. These are drafts only: nothing was posted to his board or sent to anyone.

**Who Kamil is.** By Tuesday's reading, "Kamil" in his file is Kam himself. The OXPD2 project's lead in Jira is "Kamil Kreiser", and his Azure sign-in is kamil@datasec-rd.com (C-36).

**His rule in the file** (verbatim, no item id): "reporting - managed by Kamil.  all actions / questions directed to Kamil on fleet activity". Tuesday's reading (ANSWERS-MAP U1, reading (b)): actions and questions about the agents' work come to him, on the board as today. Work for the Workpath team goes through Steve M (w8: "Utilisation of the work path team should go through Steve first"; s3).

**What the cards hold.** KA-1 to KA-5 are the actions his own words put on him. KD-1 to KD-3 come after them and are marked as Tuesday's: they follow from his words but were not named by him as actions. Each card gives the BLUF, the one thing needed from him, our recommendation, and the default that runs until he acts.

---

## KA-1. Chase HP for the OXPd 2 tools, packages and firmware (q34)

**His words (verbatim):** "q34 - we have multiple printers ready.  Versions prior to OXPd 2 can be tested now.  We will chase HP for OXPD 2 tools, packages, firmware.  Please list this as an action on Kamil"

**BLUF:** No OXPd 2 component can be proven until an OXPd 2 printer or HP's simulator is in the lab. Today every OXPd 2 part is tested against stand-ins only. Your 12 January target for OXPd 2 (s4, q2) rests on this chase.

**The one thing needed from you:** ask HP, through the portal, for four items:
- the LaserJet Debug Bridge service key;
- the OXPd 2 simulator image and its guide (our download was refused, HTTP 403);
- pilot FutureSmart 6 firmware;
- the dates in H3: production firmware, an accepted platform version, the signing service and the turnaround.
These are HP asks H5 and H3 in `Registers/HP_QUESTIONS_DRAFT.md`.

**We recommend:** send H5 and H3 first, today, as part of KA-2. If HP has not answered within a week, escalate through Steve Inch, who you said "is a lev 2 manager with enough authority to force aciton" (C-58 paragraph 7). Steve M's ticket T-04 (W4, a FutureSmart 6 printer in developer mode) runs alongside it as the other route. The key is a secret: it never goes on the board, in a ticket or in a document (C-50).

**Default until then:** OXPd 2 work continues on stand-ins, no OXPd 2 claim is made, and no date for any OXPd 2 proof is given (Q36 stays open).

---

## KA-2. Send all eight HP asks now (q39)

**His words (verbatim):** "q39 - everything goes out now.  Add as a task for Kamil."

**BLUF:** Nothing has gone to HP yet. HP's answers have the longest lead time in the project, and by your words all eight go now. Only you send to HP (C-58 paragraph 7; project rule).

**The one thing needed from you:** send H1 to H8, as drafted in `Registers/HP_QUESTIONS_DRAFT.md`, through HP's portal.

**We recommend:** send all eight, and make three edits first:
- Strike H6's licence points. C-74 settled them ("our license / commercial agreement allows us to use HP code as part of our code"), so asking HP again invites an answer that could cut across your own ruling. This is ANSWERS-MAP X13: say "keep" and H6 goes whole.
- In H2, cut item 1 ("Is Datasec already enrolled in HP App Center ... who at Datasec has to hold the master administrator account") down to the enrolment's scope for OXPd 2. You answered the rest this morning (w44 "yes"; w45 "Steve M").
- Add to H7 a request for the OXPd 1.9 files, since your target names 1.9 (KD-2).
Tuesday prepares the edited text for you to paste. Nothing goes out in your name from any agent.

**Default until then:** nothing is sent. The drafts stay as they are.

---

## KA-3. The migration runbook, Workpath to OXPd: needs a discussion (w29)

**His words (verbatim):** "w29 - needs discussion.  action on Kamil"

**BLUF:** W29 asks for Datasec's runbook for moving a customer from one sign-in solution to another, Workpath to OXPd. The design assumes today's advice is "a format", plus removing the printer's cloud record in Command Centre (02 section 8.5). The uninstall and switch-over steps of phase 5 are written against that assumption.

**The one thing needed from you:** 15 minutes, tonight or with Steve M, to say:
- whether a runbook exists;
- if it does not, whether "format, then remove the cloud record" is what customers are told today.

**We recommend:** take it in tonight's meeting, since it is already on the "still open for the room" list in pack v3. If a runbook exists, it goes to the build as a document through Steve M.

**Default until then:** the design keeps its assumption, marked as an assumption (02 section 8.5). No migration step is built before phase 5.

---

## KA-4. The sign-in paths: re-share the videos, in a named format (w8)

**His words (verbatim):** "w8 - you have videos and documentation on this.  If more information is necessary list the action on me and I will arrange.  You will need to specify what format is best.  If its a technical doc (swim lane diagrams) create a Jira ticket and assign to Steve M but for him to assign to Artur M. Utilisation of the work path team should go through Steve first"

**BLUF:** The build holds the captions of 11 Lightning Talks and no video file, so no screen of any sign-in path has been seen (pack BLUF; B1812). You called understanding these paths "critical" (C-58 P3). The design of the panel sign-in, and the first panel test, rest on transcripts only. The technical half (swim-lane diagrams by Artur M) is drafted as ticket T-26.

**The one thing needed from you:** the video files of Will's sign-in path videos.

**The format that is best for us:**
- the original video files (MP4 or MOV), one per path, unedited, so that screens can be read frame by frame;
- placed in a folder you name, or attached on the board;
- if they no longer exist, a phone screen recording of each path on a Workpath printer: MFA and No-MFA, card, QR, BLE, security key and first-use self-registration.
Subtitles are not needed; we have them.

**We recommend:** share the files you have today. Ask for the recordings only if the files are gone.

**Default until then:** the sign-in design keeps resting on transcripts, marked so (02 section 5.5). The M577 panel test (C-76) is still the first real measure.

---

## KA-5. Reporting, W41 to W43: confirm who holds them (the line with no id)

**His words (verbatim):** "reporting - managed by Kamil.  all actions / questions directed to Kamil on fleet activity"

**BLUF:** The line has no item id. It sits where Part 2's Reporting items are (W41 to W43):
- W41: the Log Analytics job record's fields, or real rows;
- W42: whether any customer changed the data-collection rule;
- W43: the queries the customer reports run.
Without them the OXPd report map (WP0.8) is UNMEASURED in 47 places. Your w15 says all reporting goes through Microsoft Log Analytics.

**The one thing needed from you:** one word on whether W41 to W43 are yours to provide ("managed by Kamil"), or Steve M's (a ticket like the others).

**We recommend:** yours. The cheapest source is an export of real rows from a test or customer Log Analytics workspace, which you can reach. If you prefer, they become three tickets for Steve M.

**Default until then:** W41 to W43 keep their answer boxes in pack v3 and stay open for the room. WP0.8 stays a draft.

---

## Following from his words, not named by him as actions (Tuesday's)

### KD-1. Azure for development: confirm the subscription and the tenant, and what may be created (q12, w7)

**His words (verbatim):** "q12 - ... Use the same subscription as HPSM-Poc.  Tied to kamil@datasec-rd.com" and "w7 - we build against kamil@datasec-rd.com.  full environment simulated.  Using my printer so we control.  Final testing will be done against Datasec testing lab"

**BLUF:** Your words put OXPd development in HPSM-POC's subscription. Tuesday's v2 login steps already point there (subscription `a6b8fe11`, directory `ec01829b`, where you are a guest). But your C-75 tap named "the agent-controllable Datasec environment" (ANSWERS-MAP X1). "Full environment simulated" means a test customer set-up: Entra changes, Conditional Access, Universal Print licences and the "Onboarding Azure Services" deployment. That goes beyond the one test VM you approved.

**The one thing needed from you:** run the v2 login steps (already with you). Say on the board that HPSM-POC's subscription replaces "the agent-controllable environment" of C-75.

**We recommend:** keep OXPd's agent login confined to its own resource group in that subscription, as the v2 steps do. Put the simulated customer environment to you on one card, with its parts, its cost and its directory, before anything is created.

**Default until then:** only the one test VM (C-78), after your login and the home rehearsal. Nothing else in Azure, and nothing of HPSM-POC is touched (its hold stands).

### KD-2. OXPd 1.9: the files (w53, s4)

**His words (verbatim):** "w53 - the project files should have included 1.9" and "s4 - OXPd 1.9 by 20 Dec OXPd 2 by 12 Jan"

**BLUF:** The library copy holds HP's OXPd 1.x Demos 1.9 and SDK 1.8.4 and 1.8.4.1, and no SDK 1.9 (directory read, ANSWERS-MAP X3). The design treats 1.9 as absent (02 section 4). Your 20 December target names 1.9.

**The one thing needed from you:** the OXPd 1.9 SDK (or the folder where it is), or a word that "1.9" means the OXPd 1.x product line and not HP's SDK version.

**We recommend:** check the NAS copy you named for the SDK (C-59). If the SDK 1.9 is not held, add it to H7 (KA-2).

**Default until then:** the build continues on SDK 1.8.4.1.

### KD-3. The two dates against one release (s4, q2)

**BLUF:** 20 December for OXPd 1.x and 12 January for OXPd 2 mean two releases. The design (D33) says one release for both, and no date (ANSWERS-MAP X2, X4, and its deadlines paragraph). Q6 (do older printers ship alone if HP is late?) and Q5 (the pilot's exit) are not answered.

**The one thing needed from you:** tonight, Q6, with the dates beside it.

**We recommend:** Q6 (a): OXPd 1.x ships first. Then Tuesday puts a dated re-plan of 03 to you, showing what the four-week pilot and the seven-group certification do to 20 December.

**Default until then:** D33 and 03's order stand. Your dates are recorded as targets.

---

Already open and on you from before this file (not re-carded here): the M577's admin password (C-77), and a test tenant user with Authenticator for the first panel sign-in test (C-76; by w7 the build now builds the test tenant itself, which is KD-1).
