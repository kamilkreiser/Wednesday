# HP reviewer feedback F1-F14: action plan (Tuesday s278, 2026-11-15)

Read-only plan. Nothing here is built, ticketed, sent or committed.

**The ruling this plan carries out** (live board 2026-11-15 17:16:37, quoted in the commission): "please action the reviewers feedback. keep the 16 questions. and yes, the stated-by-the-customer label does print in the exported report". Tuesday's reading: act on the feedback now, without waiting for the 11-10 phase decision. Keep exactly 16 questions. Reordering, rewording and new answer options are allowed. D-003 ("four added, three dropped") is not adopted.

**What was read.** Code is HPSM-POC origin main `f32b209bfa6f33c3c0268c1daa76753c816b316e` (2026-11-15T05:04:28Z), re-read via `gh api` tarball. RESULT.md had read `8766b253`. Its package lines for Q-CS-01..16 match exactly at `f32b209` (re-measured). The branch `b1577/hpsmpoc-168-industry-choice` head `fda88777` is 1 ahead and 0 behind main, and touches 43 files. Jira HPSMPOC was read, never written: HPSMPOC-241, -181, -476, -87, -35, -168 in full, plus JQL searches. 3 tickets were created today, all unrelated. "compensating" gives 0 hits (control: "firmware" 22). "WXP" gives 1 (HPSMPOC-476). I also read the analysis-repo CLARIFICATIONS at `a4ae33367a`. Its last entry is C-372. "D-002|D-010|D-016|D-018" gives 0 hits (control "C-366": 11). The project's standing line is at CLARIFICATIONS:2676: "This phase builds no integration with HP tools".

Abbreviations, all at main `f32b209`:
- `PK` = `web/src/content/packages/playbook-placeholder.v0.6.1.json`, the package a new snapshot starts on (`web/src/content/registry.ts:80`).
- `PK70` = `.../playbook-placeholder.v0.7.0.json`.
- `RS` = `web/src/content/rulesets/snapshot-policy-aligned.v0.1.2.json`.
- On b1577, `PK71` = `playbook-placeholder.v0.7.1.json` and `RS13` = `snapshot-policy-aligned.v0.1.3.json`.

Tags: **M** = measured at that commit, **DERIVED** = reasoned from measured lines, **RELAYED** = from FEEDBACK.md/RESULT.md or the decision document (DD), not re-checked, **UNMEASURED** = not checked.

---

## 1. BLUF

**6 items become build work now. 5 need words from Kam or content from an HP expert first. 3 are answers or commercial points only.**

| Class | Count | Items |
|---|---|---|
| BUILD-NOW | 6 | F5, F6 (reorder), F7 (the reviewer's own wording; Tuesday's reading that Kam's "action" approves it), F9 (answer-source chooser), F10 (re-edit an approved narrative), F11 (contents page and links in the PDF) |
| WORDS-FOR-KAM | 2 | F1 (a "Partly" answer on Q1), F4 (a "covered another way" answer on secure release). Each comes with exact proposed text and a score. |
| HP-SME | 3 | F2 (firmware-update question, finding action, and the WXP/EWS questions), F3 (Q4: keep or reword), F12 (the timeframe for a hardware-dependent finding) |
| ANSWER-ONLY | 1 | F8 |
| COMMERCIAL | 2 | F13, F14 |

Four things matter most:
1. **The 16 questions stay 16.** Every question change goes into one new content version, `playbook-placeholder@0.7.2` / `snapshot-policy-aligned@0.1.4`, stacked on b1577's 0.7.1 / 0.1.3. That lane (Lane Q) cannot start until b1577 lands, because it rewrites the same files (§3).
2. **Three lanes can start now** while b1577 is unlanded: P (answer source), N (narrative re-edit) and R (PDF contents). They share no file with each other or with b1577 (M, from the compare list).
3. **Kam has two word decisions (F1, F4) and two smaller optional ones** (an interim Q2 text in F2, and the wording of the "stated by the customer" label in F9). If he answers F1 and F4 before b1577 lands, the whole question-set change ships as **one** content version. If he answers later, F5/F6/F7 ship as 0.7.2 and F1/F4 follow as 0.7.3.
4. **A note does not reach the PDF.** The report "deliberately" leaves out consultant notes (`api/src/HpsmPoc.Modules.Reporting/Report/ReportModelBuilder.cs:19`, `:380-381`, M). The reviewer's interim idea for F4, "mark yes + a note", would therefore not show in the exported report. Only an answer option prints, because answer text goes into the per-finding Evidence column (`:208`, M). This is why F4 is an answer option.

---

## 2. Item by item

Ticket text follows the project's form (`JIRA.md`: BLUF · Recommendation · Detail), with no person's name and no card id. Sizes follow the DD: Small is under a day, Medium is one to three days, Large is more than three days.

### F1. Q1 trusted firmware: no "partial" answer for mixed fleets
- **(a) Actioned means:** Q-CS-01 gets a fourth answer for a mixed fleet. It stays one question, so the count stays at 16. The full six-state answer model (D-011, recommended next phase) is **not** built. This is a narrow version on one question, using what the ruleset already supports. The ruleset question type is already `single-choice` with per-option scores (`RS:895`, options `:904-920`, M). Only the package says `yes-no-unsure` (`PK:4283` block, M).
- **(b) Class:** WORDS-FOR-KAM. Proposed text (Tuesday's):
  - New option on Q-CS-01, between Yes and No: **"Partly: some printers can, others cannot"**, option id `partly`.
  - Score **50**. Kam sets it, under the ruleset's standing note "SME/Kam to set; HP to vet" (`RS:1686`, M).
  - Finding R-001 fires on `no`, `unsure` **and** `partly`, with its title unchanged ("Trusted-firmware checks at start-up not confirmed", `RS:1652` block). On a "Partly" answer, the PDF's Evidence column then prints "…— Partly: some printers can, others cannot (how it is known: …)" (`ReportModelBuilder.cs:208`, DERIVED).
  - Kam's other choice: apply the same option to other fleet-coverage questions (Q-CS-02, -03, -10). Default: Q1 only, as the reviewer asked.
- **(c) Ticket (new, after Kam approves the words):**
  - BLUF: The reseller reviewer said Q1 (trusted firmware at start-up) has no answer for a mixed fleet. This adds one answer, "Partly: some printers can, others cannot", scored 50, which still raises the trusted-start-up finding. Still 16 questions. It ships in the same new content version as the question reorder.
  - Recommendation: Add the option to Q-CS-01 in package 0.7.2 and ruleset 0.1.4 (on top of 0.7.1 / 0.1.3). Change only Q-CS-01's answer type, options and R-001's trigger. Count "Unsure" by answer id, not by question type, so the result tile still counts Unsure on Q-CS-01. Assessments already stamped keep their three answers.
  - Detail: Decision document D-011 (six states, next phase) is not built. This is the reviewer's one point. The ruleset already scores single-choice options. The package type and the web result count are the only code that assumes three answers. Words approved by the product owner on [date]. The score is DRAFT for HP to vet.
- **(d) Size and files:** Small on top of Lane Q.
  - The package's Q-CS-01 (`PK:4283`; `PK71:4304`, M): `type` changes to `single-choice`, with `options`.
  - The ruleset's Q-CS-01 options (`RS:904-920`; `RS13:907` block, M) and R-001 `when` (`RS:1652` block).
  - `web/src/components/snapshot/SnapshotResult.tsx:34,37` counts Unsure only when `kind === "yes-no-unsure"` (M).
  - `web/src/content/validate.ts:17` and `api/src/HpsmPoc.Modules.Assessment/Content/ContentModel.cs:124` hold the YNU list (M). Whether either rejects a single-choice snapshot question: UNMEASURED.
  - `QuestionCard.tsx:96-99` already renders single-choice (M), so no card change is needed.
- **(e) Depends on:** Kam's words and score; Lane Q; b1577 landing.

### F2. Q2 firmware updates: automated updates are not best practice; is WXP released; HP SM does not perform updates; no EWS setting?
- **(a) Actioned means:**
  - Q2's wording stops presenting automated updates as the goal.
  - The finding and its recommendations stop implying that HP Security Manager installs firmware (D-004, D-005).
  - The reviewer's two questions go to HP.
- **(b) Class:** HP-SME, with one optional interim wording for Kam.
  - Today: `PK:4309` "Is your printers' firmware kept current through regular or automated updates?" (M). R-002's action is "Apply the HP Security Manager settings listed…" (`RS:1707`, M), and its recommendations include HPR-007 "Remote Firmware Upgrade (RFU) = Enable with signatures verified" (`RS:2366-2373`, M).
  - On screen, the finding reads "Apply the HP/HPSM recommendation: Network Services › Remote Firmware Upgrade (RFU) = Enable with signatures verified" (`web/src/components/customer/FindingDetail.tsx:104`, M). This is most likely the reviewer's "HP SM to the 'configured setting'" (DERIVED).
  - HPSMPOC-476 row K3 holds this question "with D-004 and D-005 (this phase, needs HP SME wording)" (M, Jira).
  - **Optional interim for Kam** (ours, removes only the challenged words): Q-CS-02 text becomes **"Is your printers' firmware kept current through a planned, tested update process?"** R-002's action becomes the sentence the product already uses where no action is set, **"The recommended action is being finalised."** (`RS:1784`, R-004, M). HPR-005..010 stay attached, because they are device settings HP has not yet vetted, not a claim about deployment. Default if Kam does not choose: unchanged until HP answers.
- **(c) Ticket:**
  - Comment on **HPSMPOC-476**: "BLUF: The reseller reviewer (feedback of 2026-11-15) challenges row K3. Automated firmware updates are not a current best practice, and the finding reads as if HP Security Manager performs updates. On 2026-11-15 the product owner ruled to act on the feedback, keeping 16 questions. Recommendation: the question wording and R-002's action wait on HP's answer to the two questions now on HPSMPOC-241. If the product owner approves the interim wording, it ships in content 0.7.2 / ruleset 0.1.4. Detail: question at `playbook-placeholder.v0.6.1.json:4309`; R-002 action at `snapshot-policy-aligned.v0.1.2.json:1707`; HPR-007 at `:2366`; on-screen sentence at `FindingDetail.tsx:104`."
  - The HP questions go on HPSMPOC-241 (§5).
- **(d) Size and files:** Small: Q-CS-02 text (`PK71:4330`, `RS13:957` block) and R-002 (`RS:1690-1707`), in Lane Q.
- **(e) Depends on:** HP's answer, or Kam choosing the interim. Lane Q.

### F3. Q4 "firmware brought up to date before other settings are changed": the reviewer sees no logical relation
- **(a) Actioned means:** HP confirms whether Q4 is kept as it is or reworded. **Dropping it is out**, because Kam's ruling keeps 16. If it is reworded, the new wording rides in Lane Q.
- **(b) Class:** HP-SME. Q-CS-04 is at `PK:4362` (M). R-004 is medium, 60-90-day, action "The recommended action is being finalised." (`RS:1767-1784`, M). Its weight is 1, the lowest in the set (`RS:1041` block, M).
- **(c) Ticket (new):**
  - BLUF: The reseller reviewer questions whether Q4 ("Before other printer security settings are changed, is the firmware brought up to date first?") is a valid control. Hardening is applied up front, then kept configured and audited. The product owner has ruled the set stays at 16 questions, so the choice is keep or reword, not drop.
  - Recommendation: Ask HP to confirm keep or reword (question on HPSMPOC-241). Any rewording ships as a new content version. Until then Q-CS-04 and R-004 stay as they are.
  - Detail: `playbook-placeholder.v0.6.1.json:4362`; `snapshot-policy-aligned.v0.1.2.json:1767`. Not in the decision document. D-003 drops three other questions, not this one, and is not adopted.
- **(d) Size and files:** Small if it is reworded (Q-CS-04 text in `PK71:4383` and `RS13:1058` blocks).
- **(e) Depends on:** HP's answer. Lane Q, or a later version if HP answers after 0.7.2.

### F4. Q5 secure release: no way to record a compensating control such as physical security
- **(a) Actioned means:** the assessor can record "covered another way" as an answer. A note would not do it: notes never print in the report (`ReportModelBuilder.cs:19,380-381`, M). Only the answer text prints (`:208`, M). One option is added to Q-CS-06 and the count stays at 16. The fuller version from D-011 (rationale, risk owner, expiry) stays next phase.
- **(b) Class:** WORDS-FOR-KAM. Proposed text (Tuesday's):
  - New option on Q-CS-06: **"Covered another way (for example, printers in a secured room)"**, id `compensating`.
  - **Kam chooses one of two:**
    - **(i), Tuesday's default:** score 100, and R-006 does not fire. The answer is kept in the record and shown on screen, but it does not appear in the PDF, because the PDF lists answers only under findings (`:208`, DERIVED).
    - **(ii):** R-006 also fires on `compensating`, with severity Low via the rule's existing `severityOverrides` field (`RS:1663` shape, M). The PDF then prints the answer under the finding. The title stays "Held print jobs released at the printer not confirmed", which reads as a gap.
  - Help sentence for Q-CS-06, replacing "Guidance on answering it is being finalised." (`PK:4384` block, M) on this question only: **"If uncollected output is controlled another way, for example printers in a secured room, choose 'Covered another way' and say how in the note."**
- **(c) Ticket (new, after Kam's words):**
  - BLUF: The reseller reviewer said many customers secure printed output another way (for example, physical security) and the assessment cannot record it. This adds one answer to the held-print-release question. Still 16 questions.
  - Recommendation: Add the option in content 0.7.2 / ruleset 0.1.4 with the approved words and scoring choice. Earlier stamped assessments keep their three answers.
  - Detail: Q-CS-06 at `playbook-placeholder.v0.6.1.json:4384`; R-006 at `snapshot-policy-aligned.v0.1.2.json:1833`. Notes are not printed in the report (`ReportModelBuilder.cs:19`), so a note cannot carry this. D-011 (next phase) is not built.
- **(d) Size and files:** Small on top of Lane Q. The same files as F1, for Q-CS-06 (`PK71:4405`, `RS13:1148` blocks; R-006 `RS:1833` block), plus the same `SnapshotResult.tsx:34,37` change.
- **(e) Depends on:** Kam's words and choice (i or ii); Lane Q. Do it together with F1 so `SnapshotResult` is changed once.

### F5. Q9 inventory: make it the first question
- **(a) Actioned means:** Q-CS-13 is shown first. No wording, weight or score changes.
- **(b) Class:** BUILD-NOW. No new words.
- **(c) Ticket (new; also covers F6 and the order part of F12):**
  - BLUF: The reseller reviewer asked for the fleet inventory question first and for sign-in to sit next to secure release. Today inventory is 9th, held release 5th and sign-in 11th. This reorders the existing 16 questions with no change to wording, weights or scoring, as content 0.7.2 / ruleset 0.1.4 on top of 0.7.1 / 0.1.3.
  - Recommendation: New on-screen order:
    1. Q-CS-13 inventory
    2. Q-CS-02 firmware updates
    3. Q-CS-03 outdated firmware
    4. Q-CS-04 firmware first
    5. Q-CS-01 trusted start-up
    6. Q-CS-08 admin settings
    7. Q-CS-10 encrypted storage
    8. Q-CS-11 secure erase
    9. Q-CS-06 held release
    10. Q-CS-05 sign-in
    11. Q-CS-07 roles
    12. Q-CS-15 certificates
    13. Q-CS-09 encrypted communication
    14. Q-CS-12
    15. Q-CS-14
    16. Q-CS-16
  - To get this, the Identity & access section moves from 3rd to 2nd, Network goes to 3rd, and held release becomes the last question of section 1. Question ids, section membership and section weights stay as they are, so scores are unchanged. Stamped assessments keep the order they were answered in.
  - Detail: Decision document D-002 (this phase). Section weights equal the sum of their question weights (S1 26, S3 9), so moving held release into Identity & access instead would change two section weights. Not done. Comments that cite old question numbers refer to the old order.
- **(d) Size and files:** Medium as Lane Q, because it is a new content version.
  - Today: `order` in `PK` sections (`PK:4241` S1, `:4257` S3) and questions (`PK:4283-4689`, M). `RS` sections `:88` S1, `:130` S3, and question `order` fields (`RS:890-1601`, M).
  - On b1577: `PK71` (Q-CS-01 `:4304`, Q-CS-13 `:4519`) and `RS13` (Q-CS-01 `:907`, Q-CS-13 `:1486`), M.
  - Tests that pin the first card: `web/e2e/playbook-content-050-live-api.spec.ts:56` expects Q-CS-01 (M).
  - Within one bucket and severity, the PDF's finding order follows question order, so finding order in S1 changes (key bucket → severity → section weight → section order → question order, HPSMPOC-35 comment, RELAYED; DERIVED).
- **(e) Depends on:** b1577 landing. Starts Lane Q.

### F6. Q11 sign-in: put it next to secure release
- **(a)–(e):** In the same ticket and lane as F5. Held release (Q-CS-06) becomes S1's last question (9th) and sign-in (Q-CS-05) becomes S3's first (10th). The two are then adjacent, and sign-in and roles (Q-CS-07, 11th) stay adjacent, which F7 needs. BUILD-NOW, no words. Files as F5 (Q-CS-06 `PK:4384`, Q-CS-05 `PK:4557`, M).

### F7. Q11/Q12 partly overlap: the reviewer's rewording (Q11 = WHO, Q12 = WHAT)
- **(a) Actioned means:** the reviewer's two questions replace the texts of Q-CS-05 and Q-CS-07, verbatim. Same ids, same weights, same rules.
- **(b) Class:** BUILD-NOW, **on Tuesday's reading** (§4).
- **(c) Ticket (new; same content version as F5):**
  - BLUF: The reseller reviewer found the sign-in and role-based access questions partly overlap (the sign-in text says "role-based sign-in") and supplied replacement wording: Q11 asks who authenticates, Q12 what each role may do. The product owner ruled on 2026-11-15 to act on the feedback. This puts the reviewer's two sentences in, verbatim. Still 16 questions.
  - Recommendation: In content 0.7.2 / ruleset 0.1.4, set Q-CS-05 and Q-CS-07 to the reviewer's text in both the package and the ruleset. Keep ids, weights and findings R-005 and R-007. The reviewer's labels "User Authentication" and "Role-Based Access Control" are not shown, because the product has no per-question title.
  - Detail: Q-CS-05 at `playbook-placeholder.v0.6.1.json:4557`, Q-CS-07 at `:4586`; ruleset `:1083`, `:1178`. The new Q12 text names "administrative settings … device configuration", which overlaps Q-CS-08 ("Are sensitive printer settings restricted to authorised administrators only?"); recorded, not changed.
- **(d) Size and files:** Small on top of Lane Q.
  - Text fields in `PK71:4578`/`:4607` and `RS13:1100`/`:1195` blocks (M; in main's `PK70` `:4561`/`:4590`).
  - Tests pinning the old text: UNMEASURED; content tests match by hash and by text.
- **(e) Depends on:** Lane Q; b1577 landing.

### F8. Q13 certificates: no comment from the reviewer
- **(a)** Nothing is owed to the reviewer. **(b)** ANSWER-ONLY. **(c)** No ticket. D-012 (next phase; ownership, renewal, expiry, licensed-edition check) already holds the topic (DD:350, RELAYED). Line for the product owner's reply, if one is wanted: "Q13 is unchanged for now. Recording ownership, renewal and expiry is planned for the next phase." **(d)** None. **(e)** None.

### F9. "Stated by the customer": the assessor cannot change it, and the partner may answer for the customer
- **(a) Actioned means:** on the live question card, the assessor can set how each answer is known. It is pre-filled with today's default and sits inside the note's disclosure, as the reviewer suggested. Kam confirmed the label prints in the PDF, which matches the measured code: Evidence column `ReportModelBuilder.cs:208`, words `:414`, methodology line `:371` (M).
- **(b) Class:** BUILD-NOW using words the product already has.
  - The five values and their words exist in two vocabularies. The PDF and screens use `web/src/lib/plain-words.ts:6-14` ("verified", "observed", "stated by the customer", "assumed", "not assessed"). The scripted sample's chooser uses `web/src/components/screens/QuestionBlock.tsx:15-21` with the label "How do we know?" (`:64`), M.
  - The API already accepts all five on a live answer (`api/src/HpsmPoc.Modules.Assessment/Endpoints/Requests.cs:103,164`, M).
  - **Optional words sub-item for Kam:** because the partner may be the one answering, the default's words could change from "stated by the customer" to **"stated, not checked"**, in `plain-words.ts:10`, `ReportModelBuilder.cs:414` and `:371`. Default if he does not choose: the words stay, and the chooser alone makes the label correctable.
- **(c) Ticket (new):**
  - BLUF: Every answer typed into the live assessment is stored and printed in the PDF as "stated by the customer", and the assessor cannot change it. The reseller reviewer pointed out the partner often answers for the customer. This adds the existing "How do we know?" chooser to the live question card, inside the note's disclosure, pre-filled with today's default.
  - Recommendation: Reuse the five existing values and words. An imported answer keeps its observed or verified source unless the person changes it. No API change.
  - Detail: Decision document D-010 (this phase). The answer is written as asserted at `useSnapshot.ts:70`; the note's disclosure is at `QuestionCard.tsx:200-212`; the chooser exists on the scripted sample at `QuestionBlock.tsx:15-21,64`; the API accepts all five values at `Requests.cs:103`.
- **(d) Size and files:** Medium.
  - `web/src/components/snapshot/useSnapshot.ts:70`: `toWrite`, where the basis is fixed.
  - `web/src/components/snapshot/QuestionCard.tsx:200-212`: `NotesField`.
  - The `DraftResponse` type: path UNMEASURED.
  - The tests `SnapshotRunner.provenance.test.tsx` and others.
  - Report files only if Kam changes the words.
- **(e) Depends on:** nothing. **Lane P, can start now.** b1577 touches none of these files (M, compare list).

### F10. The narrative cannot be edited once approved
- **(a) Actioned means:** an approved or edited narrative can be edited again. Each revision keeps the earlier text, needs an audit note and re-approval, and a report already issued stays as issued (D-016, D-017).
- **(b) Class:** BUILD-NOW. The product's existing words ("Edit", "Save edit and approve", "Edited by a person", `web/src/components/customer/ApiNarrative.tsx:161,171,193`, M) cover it.
- **(c) Ticket (new):**
  - BLUF: Once a narrative is approved it cannot be edited again unless a finding changes. The reseller reviewer asked for this. This allows a later edit with an audit note, keeps every earlier version, and leaves any report already issued unchanged.
  - Recommendation: Let the review accept an edit when the status is approved or edited, not only generated. Store each revision rather than overwriting the text. Offer the existing Edit button on an approved, current narrative. The next report uses the latest approved revision.
  - Detail: Decision document D-016 (this phase). The review refuses anything not generated at `NarrativeReview.cs:28`, mapped at `ReportingEndpoints.cs:292-293`; the screen offers Edit only before approval at `ApiNarrative.tsx:111,190-195`; the row keeps one original and one edited text (`Entities.cs:222-245`).
- **(d) Size and files:** Medium, with new stored data.
  - `api/src/HpsmPoc.Modules.Reporting/Narrative/NarrativeReview.cs:26-32`.
  - `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs:262-300`.
  - `api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs:222-245` (`NarrativeRow`), plus `AssessmentDbContext.cs` and a migration pair (Sqlite and SqlServer).
  - The selector at `NarrativeReview.cs:64-78`, if it orders by `ReviewAt`.
  - `web/src/components/customer/ApiNarrative.tsx:105-111,190-204`.
- **(e) Depends on:** nothing. **Lane N, can start now.**

### F11. Executive report: a contents page with links, and a link back to it on each page
- **(a) Actioned means:**
  - A contents page after the cover lists the sections, each linked to its page.
  - On every page after the cover, the running header links back to the contents page.
  - The PDF has no HP logo (no image is drawn: `Pdf/Layout.cs:67-93` cover, M), so the link sits on the existing header text.
- **(b) Class:** BUILD-NOW. The heading is **"Table of contents"**, the reviewer's own words. The return link reuses the existing header text, so no new words are added. Tuesday's reading.
- **(c) Ticket (new):**
  - BLUF: The PDF has a bookmarks pane but no contents page and no links. The reseller reviewer asked for a table of contents with links to each section, and a way back to it from every page. This adds both, with no change to the report's content.
  - Recommendation: After the cover, add a "Table of contents" page listing each numbered section and its page, each entry linked to that section. Make the running header on every later page a link to the contents page. Keep the bookmarks. Check printing and a screen reader.
  - Detail: Decision document D-018 (this phase). Section headings and their pages are already collected for the bookmarks (`Layout.cs:101`, `PdfPigReportRenderer.cs:69`). PdfPig 0.1.16 is the renderer (`HpsmPoc.Modules.Reporting.csproj:17`).
- **(d) Size and files:** Medium.
  - `api/src/HpsmPoc.Modules.Reporting/Pdf/Layout.cs:28,46,55,98-104`: bookmark collection and the cover.
  - `Pdf/PdfPigReportRenderer.cs:58-71` (page loop, bookmarks) and `:75` (`DrawChrome`, the header).
  - The page numbers in the contents shift by one page. DERIVED: lay out first, then insert one fixed contents page, because nine sections fit on one page.
  - **Risk, UNMEASURED:** whether PdfPig 0.1.16's writer adds link annotations on a page. If it does not, the build adds the annotation itself. Check this first.
- **(e) Depends on:** nothing. **Lane R, can start now.**

### F12. "Trusted-firmware checks at start-up" gets 30 days but is a hardware purchase; as Q1 it looks the most important
- **(a) Actioned means:**
  - **Order part:** F5's order moves the question from 1st to 5th, behind inventory and the firmware-update questions. That is BUILD-NOW, in Lane Q.
  - **Timeframe part:** R-001 stops carrying a 30-day date for what can be a hardware replacement.
- **(b) Class:** HP-SME, for the timeframe.
  - R-001's bucket is `"30-day"` (`RS:1668`, M), given by the draft rule "30-day for High" (`RS:1686`, M) and shown as "Within 30 days" (`web/src/components/security/SecurityDashboard.tsx:14`, M).
  - The buckets the product already has are immediate, 30-day, 60-90-day and ongoing (`:13-14`, M). Moving R-001 to another bucket needs no new words. Which bucket is a remediation policy choice, so the project rule "do not invent security policy" applies.
  - Moving R-001 out of 30-day also lowers the "target" score, because the target counts remediated immediate and 30-day findings (`RS:21-23` `targetHorizon`, M; DERIVED).
- **(c) Ticket (new, `awaiting-hp`):**
  - BLUF: The trusted start-up finding (R-001) is given "Within 30 days" by the draft rule for High severity. The reseller reviewer points out that meeting it can mean buying new printers. The question's position is handled by the reorder ticket. Its timeframe needs HP.
  - Recommendation: Ask HP which timeframe fits a hardware-dependent finding (question on HPSMPOC-241). Set R-001's bucket in the next content version after the answer. Moving it out of 30 days changes the target score.
  - Detail: `snapshot-policy-aligned.v0.1.2.json:1652,1668,1686`; buckets at `SecurityDashboard.tsx:13-14`. Decision document D-007 and D-006 (this phase, need HP SME). Related HPSMPOC-35.
- **(d) Size and files:** Small: R-001 `bucket` in `RS13` (R-001 at `RS13:1669`, M).
- **(e) Depends on:** HP's answer. It rides in 0.1.4 if the answer arrives in time, otherwise a later version.

### F13. Commercial: partners charge only for HP SM, WXP, hardware and service; no consulting fees
- **(a)** A commercial position for the product owner. **(b)** COMMERCIAL.
  - Product trace: D-022 (this phase, wording the product owner supplies, DD:560, RELAYED).
  - The 11-12 pass softened the Home phase panel (`web/src/components/home/phase-flow.ts:22,41`, RELAYED from RESULT).
  - The deck still says "discovery revenue" (HPSMPOC-476 row C-deck, kept by D-058).
- **(c)** No build ticket. Optional comment on HPSMPOC-474 (operating modes): "BLUF: The reseller reviewer's position (2026-11-15): partners charge for HP Security Manager, WXP, hardware and service only, with no consulting fees for this or other tools. Recommendation: the product owner states the commercial position. D-022's wording follows from it. Detail: no product change until then."
- **(d)** None. **(e)** The product owner.

### F14. Commercial: HP SM is very expensive, WXP pricing is unknown, the price point must be right
- **(a)** A pricing question for HP, raised by the product owner. **(b)** COMMERCIAL. The product carries no price ("No price or revenue is carried", `RS` HPR-001 provenance note, RELAYED).
- **(c)** No build ticket. Optional comment on HPSMPOC-392: "BLUF: The reseller reviewer (2026-11-15) says HP Security Manager is very expensive and WXP pricing is unknown, and the price point must be right. Recommendation: the product owner raises SM and WXP partner pricing with HP. Nothing to build."
- **(d)** None. **(e)** The product owner and HP.

---

## 3. Lanes

The BUILD-NOW items are grouped into lanes that share no file.

| Lane | Items | Files (all at main `f32b209`) | Can start while b1577 is unlanded? | Order |
|---|---|---|---|---|
| **Q: question set, one new content version** | F5 + F6 + F7 (build now); F1 + F4 once Kam's words arrive; F2 interim text if Kam chooses it; F3 rewording and F12 bucket once HP answers | New `web/src/content/packages/playbook-placeholder.v0.7.2.json`, its `client/` copy, `api/src/HpsmPoc.Api/SeedContent/playbook-placeholder.0.7.2.content.json`; new `rulesets/snapshot-policy-aligned.v0.1.4.json`, its `client/` copy and SeedContent copy; `web/src/content/registry.ts` (`:22-30` hashes, `:60`, `:76`, `:80`); `web/src/content/PROVENANCE.md`; `api/.../HostedDemo/HostedDemo.cs`; `api/.../Showcase/ShowcaseSeeder.cs`; `infra/modules/appservice.bicep:141` (`HostedDemo__DraftRuleset`); `web/scripts/client-content.mjs`; the content tests; `web/e2e/playbook-content-050-live-api.spec.ts:56`; F1/F4 also `web/src/components/snapshot/SnapshotResult.tsx:34,37` and possibly `web/src/content/validate.ts:17` and `ContentModel.cs:124` | **No: must wait.** b1577 adds 0.7.1 / 0.1.3 and edits registry.ts, PROVENANCE.md, HostedDemo.cs, ShowcaseSeeder.cs, appservice.bicep, client-content.mjs and the same content tests (M, compare list). 0.7.2 / 0.1.4 must be copied from b1577's 0.7.1 / 0.1.3, not from 0.6.1 / 0.1.2, or the Industry field is lost. | After b1577 lands. Ask Kam the F1/F4 words now, so one version carries everything. If HP's F3/F12 answers arrive later, they go in 0.7.3 / 0.1.5. Size: Medium. b1577 needed 43 files for one field, so the pattern is known (DERIVED). |
| **P: how an answer is known** | F9 | `web/src/components/snapshot/useSnapshot.ts:70`; `web/src/components/snapshot/QuestionCard.tsx:200-212`; the DraftResponse type; `SnapshotRunner.provenance.test.tsx` and others. Only if Kam changes the words: `web/src/lib/plain-words.ts:10`, `ReportModelBuilder.cs:371,414` | **Yes** | Any time. If Kam's word change is taken, P touches `ReportModelBuilder.cs`, which Lane R does not (R works in `Pdf/` only). |
| **N: narrative re-edit** | F10 | `NarrativeReview.cs:26-32,64-78`; `ReportingEndpoints.cs:262-300`; `Entities.cs:222-245`; `AssessmentDbContext.cs`; a new migration pair; `ApiNarrative.tsx:105-111,190-204`; tests | **Yes** | Any time. It is the only lane with a migration. |
| **R: PDF contents and links** | F11 | `Pdf/Layout.cs`; `Pdf/PdfPigReportRenderer.cs`; the PDF tests | **Yes** | Any time. Check PdfPig link support first. |

File overlap check (DERIVED from the paths above): P is in `components/snapshot` and `lib`, N in `Narrative/`, `Endpoints/ReportingEndpoints.cs`, `Persistence/` and `components/customer/ApiNarrative.tsx`, R in `Pdf/`, and Q in `content/`, `SeedContent/`, `HostedDemo`, `Showcase`, `infra` and `SnapshotResult.tsx`. No file is in two lanes. Q and P both sit in `components/snapshot/` but share no file: `QuestionCard.tsx:96-99` already renders single-choice, so Q does not touch it (M).

---

## 4. The F7 rewording

The reviewer's two proposed questions, verbatim. RELAYED from FEEDBACK.md, which is Kam's paste of the reviewer's mail:

- Q11 User Authentication: **"Do users authenticate at the printer (e.g., PIN, badge, or username/password) before accessing secured print, copy, or scan functions?"**
- Q12 Role-Based Access Control: **"Are printer functions and administrative settings restricted based on user roles or assigned permissions (e.g., limiting access to color printing, copying, scanning, or device configuration)?"**

**Does Kam's "action" approve them as words? Tuesday's reading: yes.** The reviewer wrote the exact sentences, and Kam said to act on the feedback while keeping 16 questions. This rewording keeps 16. This is Tuesday's reading, not a quoted ruling. Kam can veto it in one line.

Three things to flag. None of them blocks:
1. "color" is US spelling, while the product uses UK spelling ("authorised", `PK:4283`). Verbatim keeps "color".
2. The new Q12 overlaps Q-CS-08 (admin settings) through "administrative settings … device configuration".
3. The labels "User Authentication" and "Role-Based Access Control" have no place on screen, because the product has no per-question title field. They are dropped.

---

## 5. Questions for HP: one comment for HPSMPOC-241

**Which ticket:**
- **HPSMPOC-241** holds the questions for HP that are not on any other ticket. Its 2026-11-11 records note says the product owner accepted that unsent questions go "in one batch, an agent drafting the e-mail for the product owner" (M, Jira).
- **HPSMPOC-181** tracks HP's own internal access request to its teams, and nothing of ours is asked there (M).

So **241**. Comment text (no names; the product owner sends; nothing goes to HP from a seat):

> BLUF: Four more questions for HP, from a reseller reviewer's feedback on the customer assessment (2026-11-15). They join this ticket's batch. The product owner sends them; nothing goes to HP from any seat.
> Recommendation: Add them to the one batch e-mail already queued for the product owner. Record each answer here.
> Detail:
> RF-1. Is WXP released, and is its firmware-deployment capability available to partners today?
> RF-2. Is there any EWS or HP Security Manager setting for automatic firmware updates? Should the assessment's firmware question ask about a planned, tested update process instead of automated updates? (Customer question Q-CS-02, `playbook-placeholder.v0.6.1.json:4309`; held on HPSMPOC-476 row K3.)
> RF-3. Q-CS-04 asks "Before other printer security settings are changed, is the firmware brought up to date first?". The reviewer sees no link between the order of firmware updates and hardening, which is applied up front and then kept configured and audited. Should the question be kept as it is, or reworded? (The set stays at 16 questions, so it is not dropped.)
> RF-4. The trusted start-up finding (R-001) currently carries "Within 30 days". Where meeting it means replacing printers, which timeframe should it carry: act now, within 30 days, within 60 to 90 days, or ongoing? (`snapshot-policy-aligned.v0.1.2.json:1668`.)
> Related: HPSMPOC-476 (firmware question wording), HPSMPOC-35 (timeframe buckets).

---

## 6. What NOT to do

- **Do not add or drop a question.** The count is 16 before and after (Kam's ruling). D-003's "four added, three dropped" is not adopted. F3's Q4 may be kept or reworded, never dropped. F1 and F4 add answer options, not questions.
- **Do not build any HP-tool integration** (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM). CLARIFICATIONS:2676 forbids it this phase. The F2 and F12 answers are content, not integration.
- **Do not build the full D-011 six-state model** (coverage, risk owner, approver, expiry, residual risk), D-008 action types, D-012 certificate lifecycle fields, or D-020 extra report outputs. They stay next phase; Kam's ruling covers only what the reviewer asked for.
- **Do not edit the existing content files** (0.6.1, 0.7.0, 0.7.1 / 0.1.2, 0.1.3). They are hash-pinned and stamped. Every change is a new version.
- **Do not start Lane Q on 0.6.1 / 0.1.2 or before b1577 lands.**
- **Do not write HP-facing words or send anything to HP or the reviewer from a seat.** The §5 comment and the reply lines in F8, F13 and F14 are drafts for the product owner.
- **Do not change the deck's commercial text** (HPSMPOC-476 row C-deck, D-058) or the pricing pages, on the strength of F13 and F14.

PLAN DONE: 14 items, 4 lanes, 2 word items, 3 HP items
