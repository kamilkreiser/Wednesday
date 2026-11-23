# B2027 JIRA-DRAFTS: Workpath questions for Steve M (drafts only, nothing written to Jira)

BLUF: 26 ticket drafts. T-01 to T-25 cover the 28 Workpath items Kam marked "create a Jira ticket (with the question) and assign to Steve M - 2 week time request" (W21 to W24 are one ticket, as he grouped them). T-26 is the w8 technical-document ask, "assign to Steve M but for him to assign to Artur M".

**No Jira write of any kind was made by this seat.** A project seat creates these later from this file.

**What was found by read** (GET only, with this seat's helper `fleet/state/s320/b2027/jira_get.py`, which has no other method; the login was read by name from the project's `4_Credentials/.env` and never printed):
- **Project:** key `OXPD2`, id 10655, "OXPd 2 (2026)", lead Kamil Kreiser. The issue type for these is **Task** (id 10030); Epic, Sub-task, Story and Bug also exist. Task's create screen offers `assignee`, `duedate`, `labels`, `issuelinks` and `parent`; `description` is required. The newest issue is OXPD2-25.
- **Steve M:** found. "Steven Molnar", accountId `626881c70f0cc0006f8ee5c9`, active, assignable on OXPD2 (`/rest/api/3/user/assignable/search?project=OXPD2&query=steve`, one result; `/user/search?query=molnar` gives the same account).
- **Artur M:** found. "Artur Menchenko", accountId `6188db6dabad3c0071c2cb75`, active, assignable on OXPD2. He is NOT set as assignee on any draft: Kam routes his work through Steve M (w8).
- **Label `oxpd-workpath-question`:** no OXPD2 issue carries it yet (JQL search, 0 results). It is created on first use.
- **Due date:** 2026-12-08 (Tuesday), from `date -j -v+14d +%Y-%m-%d` and `date -j`.

**How these relate to the master list OXPD2-1 (C-41).** OXPD2-1, "MASTER: questions and points to clarify (OXPd 2)", is the one list his C-41 made. His answers now route each Workpath question to a ticket of its own, assigned to Steve M (s3: "Work path items all assigned to Steve and delegated by him").
Tuesday's reading and recommendation: OXPD2-1 stays the index. Each draft is a Task linked to OXPD2-1 ("relates to"), and one comment on OXPD2-1 lists the 26 new keys against the pack ids, so nothing leaves the master list without a pointer (ANSWERS-MAP, X10).
Not recommended: making them sub-tasks of OXPD2-1. A kanban board usually hides sub-tasks, and Steve M must see them.

**"1 question per question".** His rule of 2026-11-20 (C-58 paragraph 3: "Rephrase questions so its 1 question per question") is read by Tuesday as one ticket per pack item for "w30 - w40". So that range is eleven tickets, T-14 to T-24. The one exception is his own grouping of W21 to W24 into one ask ("ask Steve M how it works"): it is his later and more specific word, so it is one ticket.

**Each description** quotes the question exactly as the round-2 pack asks it, gives the pack's reason and the design text it feeds, and names the format wanted. Formats: A = an answer in words, D = a document or file, C = a configuration or sample data, T = a test account or device, S = a walkthrough session. No draft holds a secret value. T-25 says the password itself must never be written in the ticket.


## T-01 (pack W1)

- **Summary** (93 characters): Workpath question: is the card key in the HPAM 4.4.1 source the live key in the store builds?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.3, WP1.4; F4, F6, F8 (master list OXPD2-1 item 1)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w1 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W1. Is the store build of HPAM and of the phone app made from the 4.4.1 source unchanged, so that the card key compiled into that source is the live key?

Why the build needs it: The first item on the master list since C-41. You said the keys in the library are old and rotated (C-3). This one is compiled into the shipped source and cannot be rotated without re-enrolling cards, so we ask the team to confirm. Card sign-in in phase 1 waits on it. Design text it feeds: 02 section 6.2 and D5 (the card key, OQ-8); 03 section 3, E1.3; 03 WP1.3. Sources in the pack: 05:105-109 (question 8); 03 section 8.3; C-41.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-02 (pack W2)

- **Summary** (106 characters): Workpath question: which card-decoding family (pre-Android 12 or Android 12) made customers' stored cards?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.3, spike S3; F4

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w2 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W2. Which family of card-decoding routines produced the card strings today's customers have stored: the older one (firmware before Android 12) or the newer one (Android 12 firmware)?

Why the build needs it: The two give different strings from the same card in 7 of 13 compared inputs. Cards enrolled under the other family would read as not known on every OXPd printer, though nobody would be signed in as someone else. Built today: the older routines. Design text it feeds: 02 D9; 03 WP1.3, spike S3. Sources in the pack: Jira OXPD2-1 comment 41450 (RP-1); WP1.3.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-03 (pack W3)

- **Summary** (90 characters): Workpath question: model and firmware of each printer in the product owner's lab (a table)
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP0.1 (phase-0 kit items 4, 7, 8, 9); no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w3 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W3. For each printer in the Workpath product owner's lab: model and firmware version.

Why the build needs it: Fills phase-0 kit items 4, 7, 8 and 9: one FutureSmart 6, one FutureSmart 5 without Workpath, one FutureSmart 4.7 and one Workpath printer with the current suite. Design text it feeds: 03 section 3, phase 0 (kit items 4, 7, 8, 9); 03 WP0.1. Sources in the pack: C-58 paragraph 8; QUESTIONS_BY_OWNER v2 A23-7; FQ-16; 05:228-233.

Format wanted: D (a document or file) (a table). Reply in this ticket; a short answer is enough where the format is A.

## T-04 (pack W4)

- **Summary** (94 characters): Workpath question: when and where can the build use a FutureSmart 6 printer in developer mode?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP0.1, WP0.2 (spike S4; kit items 4, 17); no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w4 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W4. When and where can the build use a FutureSmart 6 printer that may be put into developer mode?

Why the build needs it: Every OXPd 2 claim is untested until one exists (by HP's firmware notes the M577 is OXPd 1.x). Kit items 4 and 17. Design text it feeds: 03 section 3, phase 0 (spike S4, kit items 4, 17); 02 section 4. Sources in the pack: 05:228 (kit item 4); 05:241 (kit item 17); B1996 design review 5 point 10.

Format wanted: T (a test account or device) + A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-05 (pack W6)

- **Summary** (102 characters): Workpath question: which card readers can the lab lend (one of each of the eight in the reader table)?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.3, spike S3 (kit item 10); F4, F5

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w6 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W6. Which card readers can the lab lend: one of each of the eight products in the reader table?

Why the build needs it: The card decoders (pull request 3) are checked against golden values only. Real readers settle them (spike S3, exit test E1.3). Design text it feeds: 02 D9 and section 3.2 (the reader table); 03 spike S3, E1.3. Sources in the pack: 05:234 (kit item 10); BACKLOG.md owed item 41.

Format wanted: T (a test account or device). Reply in this ticket; a short answer is enough where the format is A.

## T-06 (pack W9)

- **Summary** (98 characters): Workpath question: do V4.4 customers see the Passkey button, and which sign-in method does it use?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.4; F12 (N-11)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w9 - no but discussion shoudl be had.  create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

Kam's word on this point (2026-11-24, verbatim): "no but discussion shoudl be had". The ticket asks the team to confirm and to say what a discussion should cover.

The question, exactly as the kick-off pack asks it:

> W9. Do customers on V4.4 see the Passkey button, and which sign-in method does it use?

Why the build needs it: No document shows the button. Requirement F12 is kept but not built until this is known. Design text it feeds: 02 section 3.2, F12; 02 change log B1817 / R4-35 (N-11); 03 section 3, phase 3 item 1 (passkey). Ticket T-06. Sources in the pack: 02 change log, B1817 open questions (N-11).

Format wanted: A (an answer in words) + screenshot. Reply in this ticket; a short answer is enough where the format is A.

## T-07 (pack W10)

- **Summary** (106 characters): Workpath question: the Conditional Access templates customers use, and the "Passwordless MFA" fix as given
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP0.2 (spike S7); F7, F20

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w10 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W10. The Conditional Access policy templates customers use, and the "Passwordless MFA" fix as customers are given it.

Why the build needs it: Today a policy for Android or iOS catches the printer. Whether an OXPd printer matches the same platform is UNMEASURED (spike S7). Design text it feeds: 02 section 7.1 (Conditional Access); 03 spike S7. Sources in the pack: 02 section 7.1.

Format wanted: D (a document or file). Reply in this ticket; a short answer is enough where the format is A.

## T-08 (pack W11)

- **Summary** (84 characters): Workpath question: the Graph permissions a customer tenant has actually consented to
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.8 and the app packages; F30 to F41 (OP-20)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w11 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W11. The Microsoft Graph permissions a customer tenant has actually consented to, from a customer tenant or the deployment guide.

Why the build needs it: The permission names are inferred, not read from code. This sets the first-run scope check and OneDrive's "Shared with me" (OP-20). Design text it feeds: 02 section 7.2; 03 section 0.4 (first-run scope check); OneDrive "Shared with me" (OP-20). Sources in the pack: 02 section 7.2; 05:185 (OP-20).

Format wanted: C (a configuration or sample data). Reply in this ticket; a short answer is enough where the format is A.

## T-09 (pack W16)

- **Summary** (110 characters): Workpath question: which deployment tool do customers get today, AuthSuite Manager 1.1.0 or HPK Utility 3.0.0?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP0.10, WP5.8; D26; no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w16 - be very specific with the ask.  create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

Kam asked for this ask to be "very specific". So: name the one tool customers are given today (product name, version number, and where a customer downloads it), say whether the other tool is still given to anyone, and say which one the Workpath team maintains. Our copies: HP AuthSuite Manager 1.1.0 and the HPK Deployment Utility 3.0.0 (from HPK-Deployment-Utility-main, sent 2026-11-20).

The question, exactly as the kick-off pack asks it:

> W16. Which deployment tool do customers get today: HP AuthSuite Manager or the HPK Deployment Utility?

Why the build needs it: Needed for Q14. "Newer" points to the Manager by file date and to the Utility by version number. Design text it feeds: 02 section 8.7, D26; 03 WP0.10. Sources in the pack: 05:201 (P-6, N-9); 02 section 8.7.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-10 (pack W19)

- **Summary** (108 characters): Workpath question: AuthSuite Manager walkthrough, .cfg import, new package kinds, job database, password/TLS
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP0.10, WP5.8; F61

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w19 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W19. A walkthrough of the Manager by its authors, four points, one line each in the box: (1) does it import existing .cfg files; (2) how could a package kind beside the six fixed Workpath ids be added; (3) its job database; (4) its password and TLS handling.

Why the build needs it: Sizes the OXPd amendment (WP0.10, WP5.8). Whether the Manager reads .cfg files is UNMEASURED. Design text it feeds: 02 sections 3.5 and 8.7; 03 WP0.10, WP5.8. Sources in the pack: 02 section 3.5, 02 section 8.7; WP0.10:42-50, 87-91.

Format wanted: S (a walkthrough session). Reply in this ticket; a short answer is enough where the format is A.

## T-11 (pack W21, W22, W23, W24)

- **Summary** (105 characters): Workpath question: how does licensing work today (own licence servers, portal source, app check, expiry)?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** phase 5 licence work; F62 (C-20)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the questions below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w21, w22, w23 & W24 - ask Steve M how it works. create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

Kam grouped these four into one ask: "ask Steve M how it works". The four questions below are the pack's, unchanged; one answer that covers all four is enough.

The questions, exactly as the kick-off pack asks them:

> W21. Does any customer run their own licence server today?
>
> W22. The licence portal's source code.
>
> W23. How does a printer app check its licence against the portal?
>
> W24. What does a Workpath printer do when its licence expires?

Why the build needs it: This bears on Q33 and on the two licence-server options (A6). Not sent. Nothing shows how a printer app checks a licence, so the server's licence check is designed from the old back end. Fielded printers appear to fall back to a 20-day temporary state [A5]. The same behaviour is planned for OXPd (C-20). Design text it feeds: 02 section 7.5 (licence service); 03 section 3, phase 5 (licence). Sources in the pack: QUESTIONS_BY_OWNER v2 A6-2; FQ-11; 02 section 7.5; QUESTIONS_BY_OWNER v2 A6-3.

Format wanted: A (an answer in words); D (a document or file) (repository access). Reply in this ticket; a short answer is enough where the format is A.

## T-12 (pack W26)

- **Summary** (100 characters): Workpath question: what defect level does the team accept before calling a Workpath pilot a success?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP6.x (pilot exit, Q5); no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w26 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W26. What defect level does the team accept before calling a Workpath pilot a success?

Why the build needs it: Needed for Q5. Your answer A24 gives the aim and no number; the questions document put the number to the team because they hold today's practice. Design text it feeds: 03 section 3, phase 6 (pilot exit, Q5). Sources in the pack: QUESTIONS_BY_OWNER v2 A24; FQ-15.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-13 (pack W27)

- **Summary** (95 characters): Workpath question: how does the team track new HP firmware and re-test the Workpath apps on it?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** test strategy (03 section 5), Q38; no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w27 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W27. How does the team track new HP firmware today and re-test the Workpath apps on it?

Why the build needs it: Needed for Q38. Design text it feeds: 02 section 4 (firmware); 03 section 5 (test strategy); Q38. Sources in the pack: C-61.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-14 (pack W30)

- **Summary** (104 characters): Workpath question: is OneDrive "Shared with me" in the shipped OneDrive 4.4 (release notes say removed)?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.8, WP3.x; F37 (N-10)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W30. Is OneDrive's "Shared with me" in the shipped OneDrive 4.4? The release notes say it was removed.

Why the build needs it: It is in the rebuild on the strength of the source alone (C-16). Design text it feeds: 02 section 3.9 (F37) and change log B1817 (N-10). Sources in the pack: 02 change log, B1817 open questions (N-10).

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-15 (pack W31)

- **Summary** (106 characters): Workpath question: on a non-English panel, do OneDrive and SharePoint show their screens in that language?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.12; F42 (A18)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W31. On a panel set to a language other than English, do the OneDrive and SharePoint apps show their own screens in that language?

Why the build needs it: English is the phase-1 language (A18). The answer decides whether that is less than a full match. Design text it feeds: 02 section 3 (A18, English for Phase 1); 03 WP3.12. Sources in the pack: FQ-1 (a follow-up question on the master list, Jira OXPD2-1); 05:186 (OP-21); C-58 paragraph 26 (A18).

Format wanted: A (an answer in words) + photo. Reply in this ticket; a short answer is enough where the format is A.

## T-16 (pack W32)

- **Summary** (88 characters): Workpath question: has any shipped Mailflow version shown "quick messages" on the panel?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.x (Mailflow); F35, F41 (A19)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W32. Has any shipped Mailflow version shown "quick messages" on the panel?

Why the build needs it: They are switched off in the code and left out (05 question 3). You said you would ask the team (A19). Design text it feeds: 02 section 3.3 (Mailflow). Sources in the pack: FQ-2, FQ-3; C-58 paragraph 27 (A19).

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-17 (pack W33)

- **Summary** (93 characters): Workpath question: if Mailflow showed "quick messages", in which version (a photo is enough)?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.x (Mailflow); F35, F41 (A19)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

Asked only if T-16 is answered yes.

The question, exactly as the kick-off pack asks it:

> W33. If yes, which version (a photo is enough)?

Why the build needs it:  Design text it feeds: 02 section 3.3 (Mailflow). Sources in the pack: FQ-2, FQ-3; C-58 paragraph 27 (A19).

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-18 (pack W34)

- **Summary** (101 characters): Workpath question: in SharePoint 4.4.6, how many custom library fields can be filled in at the panel?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.x (SharePoint); F39 (A20)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W34. In SharePoint 4.4.6, how many of a library's custom fields can be filled in at the panel when scanning? The manual says four; the code has no limit.

Why the build needs it: Sets the SharePoint scan screen. You asked for this follow-up (A20). Design text it feeds: 02 section 3.8 (SharePoint). Sources in the pack: FQ-4; C-58 paragraph 28 (A20).

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-19 (pack W35)

- **Summary** (102 characters): Workpath question: in OneDrive, does Back at the sites list show a sign-out confirmation on a printer?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP3.x (OneDrive); F37, F14 (A20)

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W35. In OneDrive, does pressing Back at the list of sites show a sign-out confirmation screen on a printer?

Why the build needs it: The code has the screen; nobody has seen it on a printer (A20). Design text it feeds: 02 section 3.9 (OneDrive). Sources in the pack: FQ-5; C-58 paragraph 28 (A20).

Format wanted: A (an answer in words) + photo. Reply in this ticket; a short answer is enough where the format is A.

## T-20 (pack W36)

- **Summary** (105 characters): Workpath question: walkthrough of the panel admin menu as customers use it (card emulation, app settings)
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP6.7 (DEV-15, DEV-16); F18, F43

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W36. A walkthrough of the panel's admin menu as customers use it for card emulation and app settings.

Why the build needs it: DEV-15 and DEV-16 (Q31) move both to the server console. The team knows how often customers use them at the panel. Design text it feeds: 02 sections 3.2 and 3.3; DEV-15, DEV-16 (Q31). Sources in the pack: 02 section 3.2, 02 section 3.3; DEVIATION-REGISTER_DRAFT.md:33-34.

Format wanted: S (a walkthrough session). Reply in this ticket; a short answer is enough where the format is A.

## T-21 (pack W37)

- **Summary** (98 characters): Workpath question: do HID OMNIKEY 076B:5428 and Inepro 1DA6:0110 readers decode on Workpath today?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.3; F5

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W37. Do the HID OMNIKEY 076B:5428 and Inepro 1DA6:0110 readers decode on a Workpath printer today?

Why the build needs it: They are kept in the reader table only if Workpath decodes them today. Design text it feeds: 02 section 3.2 (reader table). Sources in the pack: 02 section 3.2.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-22 (pack W38)

- **Summary** (98 characters): Workpath question: current meanings of error codes AI01 to AI09 and the help article they point to
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.4; F21

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W38. The current meanings of error codes AI01 to AI09 and the help article they point to.

Why the build needs it: The help texts come from the old back end. Requirement F21. Design text it feeds: 02 section 3.2 (F21). Sources in the pack: 02 section 3.2.

Format wanted: D (a document or file). Reply in this ticket; a short answer is enough where the format is A.

## T-23 (pack W39)

- **Summary** (110 characters): Workpath question: review eight "as coded" Universal Print behaviours and one UUID question: intended or bugs?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP4.x; F50 to F59

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W39. A review of eight "as coded" behaviours of today's Universal Print release code, plus one UUID-parsing question. Which are intended and which are bugs?

Why the build needs it: The rebuild copies them unless told otherwise. Examples: Acknowledge-Job carries no printer-uri, and a failed open is never retried. Design text it feeds: 02 section 3.4; 03 phase 4. Sources in the pack: Briefs/2026-11-20_B1788_STATUS.md:274-284; Briefs/2026-11-20_B1810_STATUS.md:317.

Format wanted: A (an answer in words) (per item). Reply in this ticket; a short answer is enough where the format is A.

## T-24 (pack W40)

- **Summary** (102 characters): Workpath question: does Universal Print ever answer with an IPP attribute group beyond the four known?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP4.2; F52

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w30 - w40 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

The question, exactly as the kick-off pack asks it:

> W40. Does the Universal Print service ever answer with an attribute group other than operation, job, printer or unsupported?

Why the build needs it: The reader now tolerates other groups. The answer says whether that path is ever used. The team's logs may show it. Design text it feeds: 02 section 3.4; 03 WP4.2. Sources in the pack: Jira OXPD2-1 comment 41450 (RP-6); Briefs/2026-11-20_B1788_STATUS.md:285-287.

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-25 (pack W48)

- **Summary** (105 characters): Workpath question: is the admin password in the old OXPd 1 repository README a live lab printer password?
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9` · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** 02 section 6.6 (OP-14); no F row

**Description**

BLUF: Kam asks the Workpath team, through you, to answer the question below within two weeks (by Tuesday 2026-12-08). Today the OXPd 2 design rests on a reading of code, a document or a transcript for this point; your answer replaces that reading.

Kam's instruction for this item (2026-11-24, verbatim): "w48 - create a Jira ticket (with the question) and assign to Steve M - 2 week time request"

Never put the password itself in this ticket or its answers: a yes or no, and who owns that printer, is enough.

The question, exactly as the kick-off pack asks it:

> W48. Is the printer admin password in the earlier OXPd 1 repository's README the live password of a lab printer?

Why the build needs it: Treated as live and never copied. Whoever owns that printer should change it. Design text it feeds: 02 section 6.6 (secret locations); 05 OP-14. Sources in the pack: 05:179 (OP-14).

Format wanted: A (an answer in words). Reply in this ticket; a short answer is enough where the format is A.

## T-26 (pack W8, the technical-document half)

- **Summary**: Workpath ask for Artur M via Steve M: swim-lane diagrams of every V4.4 Workpath sign-in path
- **Project** OXPD2 · **Issue type** Task · **Assignee** Steven Molnar (Steve M), accountId `626881c70f0cc0006f8ee5c9`, for him to assign to Artur M · **Due date** 2026-12-08 (Tuesday) · **Labels** `oxpd-workpath-question` · **Link** relates to OXPD2-1
- **Serves** WP1.4 and phase 3 sign-in completeness; F7 to F12, F20 (02 section 5.5)

**Description**

BLUF: Kam asks for a technical document of every sign-in path of today's product, as swim-lane diagrams, prepared by Artur M; you assign it to him (Kam: "Utilisation of the work path team should go through Steve first").

Kam's instruction (2026-11-24, verbatim): "w8 - you have videos and documentation on this.  If more information is necessary list the action on me and I will arrange.  You will need to specify what format is best.  If its a technical doc (swim lane diagrams) create a Jira ticket and assign to Steve M but for him to assign to Artur M. Utilisation of the work path team should go through Steve first"

What the build needs, as the kick-off pack asks it:

> W8. A walkthrough of every sign-in path on a V4.4 Workpath printer: MFA and No-MFA, card, QR, BLE, security key and first-use self-registration, under each setup option.

Why the build needs it: You called this critical (P3: "It is critical you understand and document these"). The design holds 11 Lightning Talk transcripts and the manuals, with no video file and no screen seen (B1812 records). It unblocks Q23 to Q27 and test 1. Design text it feeds: 02 section 5.5 (sign-in flows) and section 1; 03 section 3, phase 3 item 1; 03 section 8.5 (N-1, N-3). Sources in the pack: C-58 paragraph 12; 02 section 1; 02 change log, B1817 open questions; Review/B1812_Q_FOR-RECORDS:198-212.

Format wanted: one swim-lane diagram per path (lanes: user, printer panel, HPAM app on the printer, Microsoft Entra, the customer's gateway, the phone app where used), for MFA and No-MFA, card, QR, BLE, security key and first-use self-registration, under each setup option; PDF or image files attached here. Where a step differs by setup option, one note on the diagram is enough.

Note for the seat that writes it: Artur M's account was found by read (Artur Menchenko, accountId `6188db6dabad3c0071c2cb75`, assignable on OXPD2) but is NOT set as assignee: Kam's words route it through Steve M.


Counted by program: 26 ticket drafts (T-01 to T-26) covering 28 ticketed pack items plus the W8 technical-document ask; every summary under 120 characters.
