# Review of DECISION-DOCUMENT.md (D-001 to D-085)

Independent check, 10 November 2026. Read-only on every source; the only writes are this folder and the session scratchpad.

**Sources read at source**

- HTML: `fleet/state/kam_attachments_1109/f-84472617d43a_HP_Cyber_Security_Services_Playbook_v2_1_Layout_Alignment.html` (cited below as `HTML:n`, a line of that file; quotes matched after HTML-entity and tag normalisation by a scratch script, so a quote split by a `<span>` still matches).
- Alignment document: `fleet/state/kam_attachments_1110/recommendations.txt` (cited `REC:n`).
- Site code: HPSM-POC main `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb`, fetched as a tarball by `gh api -X GET repos/datasecau/HPSM-POC/tarball/6b0c5f2c…` into the scratchpad (the project's `2_Project_Files` was not touched). Paths below are relative to the repo root; `RS` = `web/src/content/rulesets/snapshot-policy-aligned.v0.1.2.json`, `PK` = `web/src/content/packages/playbook-placeholder.v0.7.0.json`.
- v2.1 UAT tracker (xlsx) and plan (docx) from `kam_attachments_1109`, read with openpyxl / python-docx for D-034 and D-084.
- `UAT-SCENARIOS.md` for D-083 and D-084 (verdicts recounted by script).

## Tally

36 items checked: 12 P0 items, the 7 named items, every THIS PHASE item (24, overlapping the first two groups), and a random sample of 10 others.

| Verdict | Count | Items |
|---|---|---|
| CONFIRMED | 25 | D-001, D-002, D-004, D-006, D-007, D-013, D-014, D-016, D-017, D-018, D-019, D-066, D-067, D-068, D-081, D-083, D-038, D-049, D-055, D-060, D-061, D-064, D-065, D-074, D-075 |
| WRONG | 6 | D-003, D-010, D-028, D-031, D-034, D-082 |
| OVERSTATED | 5 | D-005, D-009, D-022, D-084, D-085 |
| UNCHECKABLE (whole item) | 0 | none |

Sub-claims that cannot be checked from the HTML, the alignment document or the code (they rest on the board, Jira or earlier rulings) are left as written and listed at the end. No recommendation was changed.

**How the sample was drawn.** The 26 items already in scope were removed from D-001..D-085, leaving 59. Ten were drawn with Python `random.seed(20261110); random.sample(rest, 10)`: D-028, D-038, D-049, D-055, D-060, D-061, D-064, D-065, D-074, D-075.

## Fixes made in `DECISION-DOCUMENT.corrected.md`

1. **D-003 (WRONG).** "9 topics exist today, 4 are new, 3 site questions have no place" does not add up to 16. Mapped at source, 12 of the 16 revised topics have a site counterpart (REC:86-133 against RS questions Q-CS-01..16): 01 to Q-CS-13, 02 to 01, 03 to 02, 04 to 04, 05 to 06, 06 to 05, 07 to 07, 08 to 08, 12 to 09, 13 to 15, 15 to 03 (and partly 16), 16 partly to 14. Changed to "12 topics have a counterpart among the site's questions (several reworded, and some only partly matching)".
2. **D-010 (WRONG), in the item BLUF and in the top-five list.** "Rated Critical by the reseller reviewer": "Critical" is the alignment document's *disposition* of the reviewer's feedback (REC:40-43 column headers Feedback / Decision / Design response; REC:65-67 "Customer-statement provenance / Critical"), not the reviewer's own rating. Changed to "The alignment document rates this Critical".
3. **D-028 (WRONG, minor).** "five inputs": the HTML model has five number fields plus a time-horizon chooser (HTML:736 `[['base',…],['attach',…],['assess',…],['implement',…],['managed',…]]` then "Time horizon"). Changed to "five figures and a time horizon". The facts line already listed six.
4. **D-031 (WRONG).** "Site: fixed group headings on a coloured column": the site's column is already white: `web/src/styles/tokens.css:73` `--ds-nav-bg: #ffffff; /* the column */`; `web/src/components/shell/Sidebar.tsx:2` "The left sidebar, a white column". (The gap list's G-039, "coloured column per UAT feedback", is stale at 6b0c5f2c.) Collapsible groups are genuinely absent (`web/src/components/shell/GlobalNav.tsx:18-24` static labels; `:120` a plain `<p>` per group; the whole rail collapses to icons, `Sidebar.tsx:4-5`). Title and BLUF changed to "Collapsible menu groups (the menu column is already white)"; size S and THIS PHASE unchanged, because the remaining half is the same small, data-free change.
5. **D-034 (WRONG, summary table).** Document priority "P0": the alignment document's P0 rows are firmware correction, schema and provenance, and narrative/report approval (REC:259-267); a Customer sign-in is not among them. The P0 comes from the v2.1 UAT tracker (Functional Cases, UAT-275 "Customer role cannot enter Partner workspace", priority P0; UAT-281 P0). Priority changed to "none" and the alignment line now says so. This moves the P0 count from 12 to 11 (BLUF.md, which is not part of this deliverable, still says 12).
6. **D-082 (WRONG).** "and seven more capabilities marked implemented": REC:221-253 lists, after "Revised 16-question set — Implemented", six more marked implemented (six statuses, findings categorisation, narrative revision, report contents, three modes, opportunity register); integrations are "NOT connected" and export is a stand-in. Changed to "six more".
7. **D-005 (OVERSTATED), BLUF, facts and recommendation.** "Every finding carries the same action" / "all 16 findings": 13 of the 16 rules carry "Apply the HP Security Manager settings listed…"; R-004, R-012 and R-013 carry "The recommended action is being finalised." (RS findingRules `remediation.action`, counted by script: 13 / 3). Changed to "13 of the 16". The firmware findings R-001, R-002, R-003 and R-016 all carry the sentence, so the point and the recommendation stand.
8. **D-009 (OVERSTATED).** (a) "raises the same high-severity finding": the rule fires on `["no","unsure"]` at the question's own severity, high for 6 questions and medium for 10 (RS R-001..R-016, `severityOverrides: []`). Changed to "the same finding, at the same severity and with the same fix". (b) "HTML: findings from Unsure show 'Requires review'": in the HTML partner view *every* unaccepted finding, No or Unsure, shows "Requires review" (HTML:684 `findings` filters `['No','Unsure']`; HTML:715 `f.approved?…'Reviewed / accepted':…'Requires review'`), and the partner score counts Unsure as unresolved (HTML:714). Only the customer view separates them (HTML:801). Reworded to say so.
9. **D-022 (OVERSTATED).** "each activity is tagged … and the phases read 'Partner earns: discovery revenue + roadmap ownership'": 11 of 14 activities carry `touchpoint: true` and only phase 1 earns "discovery revenue + roadmap ownership"; phases 2 and 3 read "project revenue + solution attach" and "retainer or per-device managed services revenue" (`web/src/components/home/phase-flow.ts:22-23, 33-62`; rendered `PhaseFlow.tsx:22-26, 65`). Changed to "11 of the 14 phase activities are starred … and the first phase reads …".
10. **D-084 (OVERSTATED, minor).** "60 not met (the page does not exist)": the scenarios file itself says "usually" (UAT-SCENARIOS.md, limit 3). Changed to "mostly because the page does not exist on the site".
11. **D-085 (OVERSTATED).** "Four of the seven gates need an HP SME": REC:364-387 gives HP print hardware SME, HPSM + firmware technical SME, HP WXP product / commercial team (three HP-held), "Datasec / HP security reviewer" (shared), and Datasec product owner, channel lead with partners, QA (not HP). Changed to "Three … held by HP specialists or an HP product team, and a fourth is shared between Datasec and HP".

Two non-factual edits, needed for the deliverable:

- **Plain words.** The "How to use" line named `GAP-LIST.md` and `UAT-SCENARIOS.md` in code style; changed to "the accompanying gap list" and "the accompanying UAT scenarios file". The per-item "Evidence: G-nnn" lines are kept: they are cross-references into the gap list, not code ids, and they sit below each decision line, outside the decision text.
- **Suggested order for the sitting.** It was in BLUF.md, not in the decision document; the brief asks for it in the Word document, so it is copied in before the summary table (item names restored to their capitals: "HTML", "UAT"; "C to G" made "C to H", so that D-085, the one item of section H not in the first five, is not left out).

## Item by item

Format: claim checked · verdict · evidence.

### P0 items

**D-001** · Three 16-question sets; reviewer's numbers match the site's on-screen order · **CONFIRMED**. HTML Q01 "Are printer administration functions restricted to authorised administrators only?" (HTML:642). Site first question RS:893 "Can your printers check that their firmware is trusted…". Document third set REC:83-133, quote REC:82 "The source v2.1 demo uses a different question bank from the version [the reviewer] reviewed" (the document names the reviewer; the decision document correctly does not). On-screen order derived from PK snapshot sections S1..S5 and question `order`: 1 Q-CS-01 trusted startup, 2 Q-CS-02 firmware updates, 4 Q-CS-04 change sequence, 5 Q-CS-06 held release (output controls), 9 Q-CS-13 inventory, 11 Q-CS-05 sign-in, 12 Q-CS-07 roles, 13 Q-CS-15 certificates: matches REC:44-64 exactly. "Unblocks six other items" not counted (judgement).

**D-003** · Revised topics add four, drop three · **WRONG** (count only, fix 1). The four HTML questions are verbatim at HTML:651, 646, 647, 655. Dropped site questions Q-CS-10 encrypted storage, Q-CS-11 secure erase, Q-CS-12 data-protection risk confirmed against REC:86-133. "material data-integrity risk" REC:82.

**D-004** · Site question 2 and RFU recommendation; HTML wording; document wording · **CONFIRMED**. RS:943 "Is your printers' firmware kept current through regular or automated updates?"; RS recommendation HPR-007 "Remote Firmware Upgrade (RFU)" = "Enable with signatures verified" (tier good). HTML:643 question and action verbatim. REC:47-49 "Must change … Replace 'automatic updates required' with approved risk-based firmware governance". P0 REC:259-261.

**D-005** · Generic HPSM action; document guardrail · **OVERSTATED** (fix 7). Quotes REC:180-181 verbatim; HTML:643 "HP Security Manager — firmware assessment (mapping pending)".

**D-006** · Trusted-startup recommendations Enable, 30-day; document guardrail · **CONFIRMED**. RS HPR-001 Secure Boot Presence, HPR-002 Whitelisting Presence, HPR-004 Intrusion Detection Presence, all "Enable"; R-001 severity high, bucket 30-day. REC:179 quote verbatim. HTML:644 question and action verbatim. HP print hardware SME gate REC:337-338, 371-372.

**D-007** · Severity sets the date; Immediate and Ongoing never used · **CONFIRMED**. RS findingRules: every high rule bucket "30-day", every medium "60-90-day"; no rule uses "immediate" or "ongoing" although the type allows four (`web/src/lib/types.ts:5`). HTML per-question `when` (HTML:642-657) and "timings are indicative priority buckets, not a committed project plan" (HTML:718). REC:24, 74-76, 261.

**D-009** · Unsure scored and reported as failed · **OVERSTATED** (fix 8). RS answer options: `unsure` score 0 on all 16 questions; every rule `in ["no","unsure"]`; R-002 title "Regular firmware updates not confirmed". HTML:801 "Unknown responses", "Unsure + unanswered; not scored as failed", "Yes ÷ definitive Yes/No answers"; HTML:811 "Verification required". REC:148-149 quote verbatim; P0 gate REC:263-264.

**D-010** · Typed answers fixed as "stated by the customer" · **WRONG** (attribution only, fix 2); the facts are confirmed. `web/src/components/snapshot/useSnapshot.ts:70` basis is "asserted" unless the answer came from an import; `web/src/lib/plain-words.ts:10` and `api/src/HpsmPoc.Modules.Reporting/Report/ReportModelBuilder.cs:370, 413` "stated by the customer"; live card `web/src/components/snapshot/QuestionCard.tsx:86, 200-208` answer plus note only; field `api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs` `ResponseRecord.EvidenceBasis`; scripted sample's five choices `web/src/components/screens/QuestionBlock.tsx:15-21`. HTML:811 quote verbatim; HTML:713 "Add a note". REC:67, 151 quotes verbatim.

**D-016** · Approved narrative cannot be edited again unless findings change · **CONFIRMED**. `web/src/components/customer/ApiNarrative.tsx:110-111` (`reviewable` only while status is "generated" and not stale), :169-171 "Audit note: why this change" / "Save edit and approve", :190-193 Approve and Edit only when reviewable, :196-204 new draft only when stale. HTML:720 "Regenerate from reviewed findings", "Approve summary". REC:25, 186 quotes verbatim.

**D-017** · Changed finding withdraws approval; no reopen · **CONFIRMED**. ApiNarrative.tsx:198-201 "The findings changed since this was approved: generate again." and "…the executive report uses standard wording until a new summary is approved."; answers locked on completion `web/src/components/snapshot/ReviewPanel.tsx:56`; no reopen endpoint in `api/src` (case-insensitive search: the only hits are "AzureOpenAi"). REC:186, 188 quotes verbatim.

**D-019** · Report section 8 of 9 is "Next engagement", no price · **CONFIRMED**. `api/src/HpsmPoc.Modules.Reporting/Report/ReportModel.cs:16-27` nine sections, Next Engagement eighth; ReportModelBuilder.cs:338 "Indicative only: no price is shown."; :284 "no prices or revenue". HTML:821 "excludes internal partner pricing and sales notes". REC:201 "Never included in security report by default"; REC:267.

**D-034** · Five-role chooser in HTML; site four roles, no Customer role · **WRONG** (priority column, fix 5); facts confirmed. HTML:699 roles Partner, Consultant, Admin, Demo; HTML:854 adds "Customer" and sets aria-label "Review role (demonstration only)"; HTML:856 "The Customer role cannot access partner commercial content." `web/src/lib/session.ts:8` four roles; `web/src/components/security/WorkspaceSwitch.tsx:2-3` "there is no Customer role".

### Named items

**D-081** · Which HTML sections are "most accurate" · **CONFIRMED** as a fair summary of the item-level findings checked here (firmware checklist D-068, impact caveat D-067, unknowns D-009 ahead in the HTML; module text, narrative, report, metrics, calculator ahead on the site). REC:347 "prioritise content accuracy before adding commercial automation" verbatim. The "for some sections" instruction is the product owner's, not in the three sources.

**D-082** · v2.2 demo not supplied · **WRONG** (count, fix 6); the main claim is confirmed: neither attachment folder holds a v2.2 HTML (1109: v2.0 HTML, v2.1 HTML, tracker xlsx, plan docx; 1110: the v2.2 recommendations docx, its text, one screenshot). REC:227-228 "Revised 16-question set / Implemented; new schema and isolated local storage".

**D-083** · 20 scenarios: 4 met, 10 partly, 2 not met, 3 needs content, 1 change request · **CONFIRMED**. Recount of UAT-SCENARIOS.md section 1 gives exactly 4 / 10 / 2 / 3 / 1 = 20; REC:284-326 lists 20. Spot-checked verdicts against code: UAT-03 partly (rules fire on unsure; titles say "not confirmed"), UAT-12 partly (one edit at approval), UAT-14 partly (bookmarks `PdfPigReportRenderer.cs:69`, no contents page): all consistent.

**D-084** · Pack sizes, its reference application, verdict counts · **OVERSTATED** (minor, fix 10). Tracker sheets: Functional Cases UAT-001..UAT-285 (285), Nonfunctional NF-001..038 (38), Production Gates PRD-001..032 (32), End-to-End Scenarios E2E-01..12 (12). Plan docx: "Reference application: HP_Cyber_Security_Services_Playbook_v2_1_Layout_Alignment.html", "Testing boundary: offline fictional-data HTML demonstration". Recount of UAT-SCENARIOS.md section 2: 109 / 26 / 60 / 6 / 84 = 285.

### Remaining THIS PHASE items

**D-002** · Inventory 9th, release 5th, sign-in and roles 11 and 12, split across groups; HTML has no inventory question · **CONFIRMED**. PK order as under D-001 (release in "Printer & fleet administration", sign-in and roles in "Identity & access"). HTML Q01..Q16 (HTML:642-657): no fleet-inventory question (Q02 is about firmware inventory). REC:57-61 "Adopt"; REC:271-273 P1.

**D-013** · Every finding's explanation and action "being finalised" · **CONFIRMED**. All 16 RS rationales are the identical sentence "The answer did not confirm this. The explanation of why it matters for this customer is being finalised."; all 16 actions contain "being finalised". HTML:643, 646 finding and action quotes verbatim.

**D-014** · 54 exact settings, e.g. 12-character password every 90 days; HTML hedges · **CONFIRMED**. RS `recommendations` = 54 (good 14, better 25, best 15); HPR-025 "Enable, min 12 chars · Rotate 90 days"; ruleset status "draft". HTML "mapping pending" (HTML:642-650), "verify with HP" (644), "outside HPSM" (652-654), HTML:717 "HP must vet control terminology, support by model and settings before customer use." REC:17.

**D-018** · Nine sections, bookmarks, no contents or return links; HTML has none either · **CONFIRMED**. ReportModel.cs:16-27; PdfPigReportRenderer.cs:7-8, 69 (outline); no "contents" in the HTML report lines (HTML:721, 821-822). REC:71-73, 272-273.

**D-022** · Consulting touchpoints and fees as the standard motion · **OVERSTATED** (fix 9). Walkthrough `web/src/content/walkthrough/steps.ts:144` "Discovery fees → implementation and attach → reviews and managed services." verbatim. REC:77-79, 20.

**D-031** · White column, collapsible groups · **WRONG** (fix 4). HTML group buttons `groupButton` (HTML:699, 841, 848).

**D-066** · Site rule sentence; HTML wording · **CONFIRMED** at source: `web/src/components/screens/RoadmapScreen.tsx:84-86` "Verified complete needs an evidence reference. The reference is not checked independently."; HTML:816 "Consultant action register", "Marking an action complete requires an evidence reference, but this local demo does not independently verify it." The "approved this morning" ruling is outside the sources (see end).

**D-067** · "Business impact — Not written yet"; HTML caveat · **CONFIRMED**. `web/src/components/customer/FindingDetail.tsx:138`; HTML:716 "Potential business impact" with pill "Draft / to be validated" and the sentence verbatim.

**D-068** · Site checklist is four old-deck partner statements, one repeating "regular or automated updates"; HTML four steps and guidance · **CONFIRMED**. `web/src/components/customer/FirmwareTask.tsx:31, 36-37` items from `deckReadinessSet()` (`web/src/content/registry.ts:151-153`, package 0.3.0), section firmware-protection: "We ensure customer printers can verify trusted firmware at boot and block unauthorized code." … "We keep customer printer firmware current through regular or automated updates." HTML:725 four steps and guidance verbatim.

**D-085** · Seven gates, none with a named holder · **OVERSTATED** (fix 11). REC:364-387, seven rows, every status box unticked; REC:17 "Internal working document; not customer-approved HP product guidance."

### Random sample

**D-028** · **WRONG** (minor, fix 3). HTML:736 "Revenue opportunity model", "Sample scratchpad only." Site: `web/src/components/partner/RevenueCalculator.tsx:2, 27-58` four input steps plus a Results step (five steps); `RevenueResults.tsx:2-3` saved-scenario comparison and CSV export.

**D-038** · **CONFIRMED**. All eight HTML group names and the six renamed entries found (HTML:767-1087). Site `GlobalNav.tsx:18-24` four groups; MAIN_NAV 13 entries of which Assessments retires, so 12 shown at most. The HTML entry count (23) comes from the analyst's rendering, not re-rendered here.

**D-049** · **CONFIRMED**. HTML:1073 "My action queue — Prioritise customer follow-ups, service delivery actions, due dates and review evidence"; HTML:1083 share toggle and "Never share internal pricing, margins, commercial notes or account details."; tasks carry `opportunityId` (HTML:941, 945, 1001…).

**D-055** · **CONFIRMED**. HTML:964 "Delivery and assessment queue" and its sentence verbatim; no such page in the site's menu (`GlobalNav.tsx:39-55`).

**D-060** · **CONFIRMED**. HTML:741 "Local design-review settings and feedback", "Content-package administration", "Future phase". Site `web/src/app/(app)/admin/page.tsx:14-19, 24` "Admin", feedback links, four connection rows.

**D-061** · **CONFIRMED**. HTML:1027-1036 eight requirements (sign-in, isolation, storage, audit, integrations, security testing, accessibility, usability acceptance); HTML:1082 "Operational readiness & release gates", "Production integrations configured".

**D-064** · **CONFIRMED**. HTML:709 "EIGHT-STEP JOURNEY", ninth button shown as "⋯"; HTML:712 "1. Customer profile", HTML:723 "8. Next engagement", HTML:724 "Customer automation metrics". Site `web/src/lib/journey.ts:10-21` Overview plus nine steps ending "Metrics".

**D-065** · **CONFIRMED**. HTML:713 "Show questions for", "Create follow-up draft"; site `web/src/components/snapshot/SnapshotRunner.tsx:253` "Skip for now".

**D-074** · **CONFIRMED**. HTML:811 "Assessment overview", "Question responses by domain", "Declared in place", "Not answered"; site `web/src/components/security/SecurityAssessments.tsx:2, 37`.

**D-075** · **CONFIRMED**. HTML:812 "Reviewed risks & gap analysis", "Recorded response", "Traceable to", "Evidence to verify", "an ISO/NIST mapping does not establish standards compliance"; HTML:769 "A.5.15 / A.8.2", "Admin-role listing and permission review". Site `web/src/components/security/SecurityFindings.tsx:43` "Gaps and findings".

## Whole-document checks

- **Counts.** Summary table 85 rows; 85 item blocks; every row's title, recommendation and size equals its block. THIS PHASE 16 S / 8 M / 0 L = 24; NEXT PHASE 18 / 21 / 16 = 55; DROP 6 / 0 / 0 = 6; columns 40 / 29 / 16 = 85. Section headings' stated counts (A 15, B 6, C 8, D 13, E 19, F 9, G 10, H 5) equal the blocks under them. "Needs HP SME" 10 and "product owner" 11 equal the column; the 5 change-request items (P2 or P3) are D-024, D-025, D-026, D-029, D-043. All unchanged by the fixes (re-run on the corrected copy).
- **Decision boxes.** Every one of the 85 blocks has BLUF, HTML-against-site, alignment line, size, risk, recommendation, the decision line "[ ] This phase  [ ] Next phase  [ ] Drop" and "Notes:".
- **Names.** Underscore-aware scan (a name bounded by any non-letter, so `_Kam_`, `Kam's`, `PAUL` all fire) for Marco, Paul, Kam, Kamil, Kreiser, Anupam, Baidya, Philip, Cuff, Tuesday, Wednesday, Jarvis, Moira. Firing controls: a control line fired 3 of 3; `recommendations.txt` fired 9 (Marco). DECISION-DOCUMENT.md 0, corrected copy 0. A manual read of every capitalised word in the document found no other person's name; people appear only as "the product owner", "the deputy", "the reseller reviewer" and named roles (HP SME).
- **Invented security content.** None found presented as fact. Every security statement is quoted from, or attributed to, the HTML, the alignment document or the site; where wording is missing the item says "needs HP SME content".
- **Plain words.** No file paths, line numbers, code identifiers or ticket keys in the main text (scan for backticks, `.tsx`, `.cs`, `.json`, `name:digits`, `Q-CS`, ticket and brief keys). The only hits were the two file names in "How to use", fixed above.

## Left as written: claims outside the three sources

These rest on the board, Jira, the UAT feedback list or earlier rulings, which this check did not read. Each is plausible and is not a fact about the HTML, the document or the code:

- D-031: the collapsible groups were asked for in the product owner's UAT feedback.
- D-066: the product owner approved the rule sentence this morning.
- D-013: drafts of finding wording are being prepared under the product owner's ruling of 10 November.
- D-028: the site's calculator "was already accepted".
- D-027, D-037, D-045, D-047: earlier rulings (menu entry removed, one banner per page, readiness changed yesterday, open board questions).
- D-001: "unblocks six other items" is the analyst's count.

## Part 2: the deliverable, as checked

- `HPSM_Phase_Decision_Document_2026-11-10.docx`: built with python-docx from `DECISION-DOCUMENT.corrected.md`. A4, title page (title, 10 November 2026, "Internal, draft for decision"), BLUF and counts table, suggested order, 85-row summary table (header row repeats), then sections A to H with one block per item: BLUF, facts, alignment line, size, risk, a shaded recommendation box, three Word checkbox controls (This phase / Next phase / Drop: clickable in Word 2010 and later), and two ruled notes lines. Footer: status and page number. Re-read with python-docx: 85 item headings, D-001 to D-085 in order, 255 checkbox controls (85 x 3), 85 decision lines, 85 recommendation lines (24 / 55 / 6), summary table 85 rows. Page count not measured: neither Word nor LibreOffice is on this machine; a Quick Look preview of page 1 was checked by eye.
- `HPSM_Phase_Decision_Document_2026-11-10.pdf`: LibreOffice is not installed, so the same content was rendered from HTML by headless Google Chrome 157 (`--print-to-pdf`), A5 page for phone reading, 81 pages. Its tick boxes are printed boxes, not form fields. pdftotext: 85 distinct item headings D-001 to D-085, 85 decision lines. Pages 1, 5 and 11 were rendered to images and checked by eye.
- Name scan, same scanner and control as above, over the docx text, the docx's raw `word/document.xml` and the PDF text: 0, 0 and 0; control fired 3 of 3. Document metadata author: "Datasec".
