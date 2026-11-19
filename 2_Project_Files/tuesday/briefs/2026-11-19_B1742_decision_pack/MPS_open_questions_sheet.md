# MPS open questions sheet: Q-03, Q-09, Q-10, Q-13, Q-14, Q-16, Q-17 and the four design-rule tickets (M3 of SWEEP-1630)

Drafted for Tuesday's reading, 2026-11-19, read-only, nothing posted. Each question is word for word from its source.
"Answered" means a ruling or record that I read at source; the quote and where are given. A recommendation appears only
where the source material gives one. Non-ASCII marks are shown as ASCII.

## BLUF

- Of the 11 items the sweep bundles as M3, **2 are already answered** (MPSCALC-110 by C-104 on 2026-11-11 and two
  cards of 2026-11-12; MPSCALC-288 by C-69 on 2026-10-25), **1 is half answered** (Q-10: D-10 a settled "warnings, not
  blocks" but C-45 itself says Q-10 "stays open as the policy question"), and **8 are open** (Q-03, Q-09, Q-13, Q-14,
  Q-16, Q-17, and the two design-rule tickets 314 and 360, which the tickets themselves say are the coordinator's call,
  not a card for the product owner).
- So the product owner's real list is **7 questions, 6 of them untouched since 2026-10-01** (Q-03, Q-09, Q-13, Q-14,
  Q-16, Q-17) plus the policy half of Q-10. Not one of the seven has an option list in its own source; the register
  rows are open questions with no choices. Any options would have to be written, which this drafter did not do.
- The sweep's reading "D-10 may answer Q-10" is checked and does **not** hold: the C-45 row for D-10 says "none (Q-10,
  MPSCALC-76, stays open as the policy question)".
- The register of 2026-11-11 (card `mpscalc-waiting-register-1111`, "54 tickets, grouped into 35 decisions; 29 of the
  decisions are a quick yes or no") is a PDF outside the repository and was not available. 29 of its 35 decisions were
  ruled (C-102 to C-130); the other 6 are not identified in any text I could read, so some of the seven below may
  already have been in the register's "other 6" and the answer or the non-answer sits there. Reported, unverified.
- Q-15 (MPSCALC-81, export formats and draft wording) is in the register but not in the sweep's list; the delivery line
  of card `mpscalc-decisions-pack-1012` names Jira MPSCALC-81 among the keys it moved. Not examined further.

## Index

| # | Item | Jira | State | Frees |
|---|---|---|---|---|
| Q-03 | Brand and ownership | MPSCALC-69 | OPEN | 69 |
| Q-09 | Pricing Owner, Pricing SME, approvers, golden cases | MPSCALC-75 | OPEN | 75 |
| Q-10 | Approval thresholds and exception policy | MPSCALC-76 | HALF ANSWERED (D-10 a) | 76 |
| Q-13 | Service costs and service levels | MPSCALC-79 | OPEN | 79 |
| Q-14 | Device recommendation rules and capability data | MPSCALC-80 | OPEN | 80 |
| Q-16 | Retention and audit periods | MPSCALC-82 | OPEN (a default is built) | 82 |
| Q-17 | Fleet size and concurrency | MPSCALC-83 | OPEN | 83 |
| rule | One-pager fit | MPSCALC-110 | ANSWERED (C-104, 2026-11-11) | 110 on the product owner's side |
| rule | Reject rule beside the approvals list | MPSCALC-288 | ANSWERED (C-69, 2026-10-25) | 288 on the product owner's side |
| rule | Autosave writes an event per pause | MPSCALC-314 | OPEN, coordinator's call | 314 |
| rule | usageOnly reading | MPSCALC-360 | OPEN, coordinator's call | 360 |

Common facts: all seven questions were seeded 2026-09-30 / 2026-10-01 by the first build seat as tasks under epic
MPSCALC-15 (label `question-for-<owner>`), status Backlog in Jira on 2026-11-19; MPSCALC-69 and 79 have one comment each,
the other five none (checked today, control: 69 returns its comment). The register is
the questions register in `1_Project_Definition/Questions_and_Answers/`. Searched for answers: CLARIFICATIONS.md (3,509
lines) for each key and each Q label; control: "Q-03" has 2 hits, "MPSCALC-69" has 5. Q-09, Q-13, Q-14, Q-17 and
MPSCALC-75, 80, 82, 83 have 0 hits in CLARIFICATIONS.md; Q-16 has 1 (MPS-9, below); MPSCALC-79 has 1 (a records note on MPSCALC-266: "the care service-level filter is absent while no governed level
data exists; MPSCALC-79 holds service levels", which confirms the question is still open, not an answer).

## Q-03 Brand and ownership (MPSCALC-69), OPEN

Question, word for word (register row and Jira): "The spec and guide are branded "HP Solutions Centre" with owner "HP
Solutions Centre / Datasec Solutions". Is HPSC a Datasec brand, and is HP branding approved for this product (spec
section 30 brand assets, section 38)?" Blocks (source): "UI design system, exports, IP (E03, E10, E13)". Source: spec
document table, section 30, 38, 40.

Already answered? No. Register state: "OPEN". Nearest rulings, quoted:
- C-45 D-14 c (2026-10-20): the question "Trading name on documents: [reviewer]'s files say "HP Solutions Centre"; the hosted
  site carries Datasec's logo (Q-03 open)." was answered by c "a setting per quote, with today's Datasec default: it
  answers both without choosing for [product owner]"; the row's own words: "Does not: choose a brand for the product owner."
  (CLARIFICATIONS.md:682; the plan row 254.) Kept-rulings column: "none (Q-03, MPSCALC-69, brand still open)".
- Records pass B1076 (CLARIFICATIONS.md:2055): "no ruling answers MPSCALC-69, and CLARIFICATIONS.md:1716 leaves a
  ticket whose work is a ruling with no merged change as it stands".
- Ticket comment 39311 (2026-10-10): "placeholder used, decision open. The proposal uses a self-made 'LOGO' placeholder
  and an 'IMAGE' placeholder; no HP logo, HP photo or HP Forma font (Arial stands in)."
Options the source offers: none for the question (a two-part yes/no). The related build row offered a) Datasec as today,
b) HP Solutions Centre, c) a setting per quote; c was chosen for the build.
Frees: MPSCALC-69. Not blocked by it: MPSCALC-281 and 287 (D-14 c lets them use "today's wording" until it is answered).
Recommendation: none supported by the source. The sweep's "11 tickets" count credits this question with one key.

## Q-09 Pricing Owner, Pricing SME and approvers (MPSCALC-75), OPEN

Question, word for word: "Who fills the spec's Pricing Owner / Pricing SME / Approver roles, and who will produce the
golden-case expected values in Excel?" Blocks: "Golden tests and approvals (E02, E09)". Source: "Spec section 35 RACI,
section 37, App B".

Already answered? No ruling found. Partial neighbours, not answers: the 2026-10-16 roles ruling, "All roles + owner
self-approval, audited" (card `mps-<reviewer>-review-roles-k01-k18-1016`, ruled a 2026-10-16 13:08; as recorded in
MPSCALC-136's comments), settles who may approve in the product, not who fills the spec's RACI roles. Nothing on
who produces golden-case values: CLARIFICATIONS.md has 2 hits for "golden", both in a records pass line about tests
(2069, 2081), not a ruling.
Options the source offers: none. Frees: MPSCALC-75. Recommendation: none supported.

## Q-10 Approval thresholds and exception policy (MPSCALC-76), HALF ANSWERED

Question, word for word: "What margin thresholds route a quote for approval, who approves, and which warnings may be
exceptioned? The workbook only flags MARGIN REVIEW below the target GP." Blocks: "Approval workflow (E09)". Source:
"Spec section 30, section 38; register R-25".

Already answered, in part. C-45 D-10 (2026-10-20, ruled a): question "Approval thresholds: v13 blocks below 12% upfront
GP, 10% contract GP, or above a 10% discount." Ruled: "a) Review warnings at those values", plan reason "Q-10 is open;
warnings change no price and can be tightened". Effect column: "Lets: T-V11-1 settings and T-V3-2 threshold checks as Review
warnings. Does not: any approval block at those values." Kept earlier rulings column: "none (Q-10, MPSCALC-76, stays open
as the policy question)" (CLARIFICATIONS.md:678). Gap analysis, section on data we do not have: "the prototype's 12 / 10 /
10 % are prototype defaults, not a ruled policy". MPSCALC-286's ticket repeats: "Q-10 stays open as the policy question".
Still open therefore: whether 12 / 10 / 10 are the real values, who approves a breach, which warnings may be
exceptioned. Check of the sweep's claim "D-10 may answer Q-10": it answers "block or warn" only.
Options the source offers: the D-10 choices a) warnings, b) blocks, c) other values / none; a was taken.
Frees: MPSCALC-76 (MPSCALC-286 is ruled buildable on D-10 a and does not wait on it).
Recommendation: none beyond what D-10 recorded.

## Q-13 Service costs and service levels (MPSCALC-79), OPEN

Question, word for word: "The workbook template has fixed service, per-click service reserve and install/freight all
at 0 (the spec says to confirm them). What are the real values, who sets them, and are service levels (SLA) priced
anywhere?" Blocks: "Base charge and CPP (E02, E03)". Source: "Spec section 19.1; register section 3.2".
New input on the ticket (comment 38721, 2026-10-01): "The Synnex book contains two care-pack BIDs (A4 Platinum Carepack,
248 rows; A3 Carepack, 111 rows) and a care-pack/service block in its Price List (rows 518-947). The workbook uses none
of them, and its service costs default to 0. Are care packs the intended source of 'fixed service / device / month', or
are service costs set some other way?" (register finding P-02).

Already answered? No ruling on the values or on SLA pricing. Built since, which does not answer it: the managed-service
cost and sell per device per month per purchase section (MPS #135, MPSCALC-255 Done; CLARIFICATIONS.md:1892: "0
C-entries: no product-owner ruling was given on this ticket since the 2026-10-20 card"), care-pack rows (MPS #78). The
gap analysis lists care-pack eligibility and terms as data the calculator does not have.
Options the source offers: the two readings in comment 38721 (care packs are the source; or some other way).
Frees: MPSCALC-79. Recommendation: none supported.

## Q-14 Device recommendation rules and capability data (MPSCALC-80), OPEN

Question, word for word: "The spec asks for rule-based recommendations by format, colour, volume and authentication
needs but gives no thresholds, and the workbook's device data has no speed, duty cycle or volume range. Who supplies
the rules and device capability data?" Blocks: "Recommendations (E04)". Source: "Spec section 20; register section 6".
Already answered? No ruling (0 hits for MPSCALC-80 and Q-14 in CLARIFICATIONS.md). The review register
(`Registers/2026-10-16_<reviewer>-review-items.md`:304) says the review "touches ... Q-14 (device capability: per-device pages
T15)"; and the gap analysis lists "HP-verified compatibility" among data not held. Not an answer.
Options the source offers: none. Frees: MPSCALC-80. Recommendation: none supported.

## Q-16 Retention and audit periods (MPSCALC-82), OPEN, a default is built

Question, word for word: "How long are quotes, source versions, exports and audit events kept?" Blocks: "Data model
and ops (E12, E14)". Source: "Spec section 30, NFR-PRIV-001".
Already answered? Not for quotes, versions, exports or audit. Two neighbours, quoted:
- MPS-9 (C-23, 2026-10-12, CLARIFICATIONS.md:336), feedback only: "The new in-app feedback stores every message forever,
  and could also raise Jira tickets from the hosted site ... How long to keep feedback, and switch Jira on?" Ruled: "(a)
  Keep everything; no hosted Jira for now." The row's source map "also names Q-16".
- The shipped default for source versions, docs/API.md as quoted in gate B42: "Kept for the life of the store; nothing is
  pruned or deleted (default pending Q-16, MPSCALC-82)." (`Briefs/2026-10-12_B42_STATUS.md`:479; the text is from
  2026-10-12 and was not re-read at main today.)
Options the source offers: none beyond that default (keep everything). Frees: MPSCALC-82.
Recommendation: none supported; what would change on an answer is only whether the "keep forever" default is confirmed
or replaced by a period.

## Q-17 Fleet size and concurrency (MPSCALC-83), OPEN

Question, word for word: "The workbook caps a quote at 20 fleet lines, 80 hardware and 40 software lines; the spec
assumes ~100 lines typical. What maximum fleet size and how many concurrent users?" Blocks: "Performance targets (E14)".
Source: "Spec section 30, NFR-SCALE-001; register section 2".
Already answered? No ruling. The built product limits were not read today (not compared with the workbook caps).
Options the source offers: none. Frees: MPSCALC-83. Recommendation: none supported.

## MPSCALC-110 One-pager fit (design rule owed), ANSWERED

Ticket question (BLUF, word for word): "a design rule is owed, not a defect in the build. The short-form proposal stays on
one A4 page because of count caps alone. Longer detail or summary text, a 7th usage rate on the overflow-as-draft data, or
a single-paragraph lead of 598-600 characters prints 2 pages." Fix shape in the ticket: "the product owner's rule for long
text (e.g. a line clamp on detail cells, or caps by height), then a print test per worst case."
Answered, with quotes:
- C-104 (2026-11-11 14:34, card `mpscalc-waiting-register-1111`, "Accept all 29 quick recommendations"): question "One-page
  proposal: it stays on one page only because of count limits. Tighten the limits so it always fits, or let long text spill
  to a second page?" Options "(a) Tighter limits, always one page; (b) Allow a second page." Recommendation accepted,
  verbatim: "Tighter limits, always one page. A 'one-pager' that prints two pages misleads the customer." (CLARIFICATIONS.md:2671-2678.)
- Card `mpscalc-110-one-page-which-form-1111`, ruled a 2026-11-12 07:31: "Rental short proposal only: cap it so it always
  fits one page (recommended)"; the purchase short proposal stays as the 2026-10-16 cover-sheet layout.
- Card `mpscalc-110-options-still-spill-1112`, ruled a 2026-11-12 10:56: "Cap the option tables too (recommended)".
- Built: MPS #186 and #189 (comments 41188 and 41183), rental short proposal "shows at most three device lines ... and at
  most two rows in each of the hardware-options table and the software table"; the pointer words were approved (card
  `mpscalc-hosted-deploy-words-1112`, 2026-11-12 17:00).
What remains (comment 41183): "the ticket's own subject, longer text: the review printed 2 pages (about 260 mm) for about
75-character device names with about 70-character option text". That residue is the ticket's original long-text rule,
which is not ruled; the product owner's "always one page" ruling covers it in intent. Options the source offers: the
ticket's "line clamp on detail cells, or caps by height".
Frees: nothing is waiting on a new question from him; whether a long-text rule is needed is Tuesday's reading.

## MPSCALC-288 [B318-1] callerCan.approve and reject (design rule), ANSWERED

Ticket question: "Either give reject its own member (callerCan.reject, the old rule) and keep approve on the new rule, or
keep approve on the old rule and let only POST approve refuse. ... Decide whether the canApprove queue should still list
such a quote (it needs a reject)."
Answered, C-69 (2026-10-25 09:56, card `mps-approval-queue-blocking-quote-1025`, option a):
- the card's question, verbatim: "should the approvals-waiting list still show a submitted quote whose calculation has a
  blocking issue, so the approver can reject it? Yes or no."
- option a, verbatim: "Yes: keep listing such a quote for the approver"; detail: "A builder gives reject its own rule
  (callerCan.reject or equivalent) and points the list and the awaiting group at it. New contract member and new words;
  the exact text comes to you on a follow-up card before anything ships." The card's recommendation was option b; the
  product owner chose a. (CLARIFICATIONS.md:1358-1361; Jira comment 40127.)
So the sweep's "288 was ruled 2026-10-25" holds. Owed and not drafted: the reject member (name) and its words, on a
follow-up card; Tuesday's records pass of 2026-10-25 (B655) records "nothing is built". Frees: 288's question; the build
remains.

## MPSCALC-314 [B348-2] Autosave writes a history event per typing pause, OPEN (coordinator's call)

Ticket text, word for word: "The choice is open and has not been ruled (the options the gate named: a longer interval, a
minimum gap between saves, or coalescing the draft-updated events on the server). This ticket does not pick one; it carries
no needs-ruling label because the choice is the coordinator's decision, not a card."
Facts: "Every changed autosave writes a draft-updated history event and a revision. On the real API, 60 s of typing in bursts
with 2500 ms pauses (22 bursts) wrote 22 PATCH requests, 22 draft-updated events and 22 revisions; 60 s with pauses under
1900 ms wrote 1 of each; 30 s of silence on a clean screen wrote 0." "The 2000 ms value itself was ruled and is not the
finding" (`AUTOSAVE_QUIET_MS = 2000`, autosave.ts:9). Same cost is why the debounced recalculation of MPSCALC-34 was not
built (both tickets Backlog today).
Answered? No. CLARIFICATIONS.md lists it as "Open, not ruled" in at least seven entries (:742, :776, :811, :856, ...). Pack of
2026-10-24 (Tuesday's `projects_index`): "T. ... Options: longer interval, minimum gap between saves, or coalesce on the server."
Options the source offers: those three. Frees: MPSCALC-314 (and the recalculation half of MPSCALC-34).
Recommendation: none in the source ("This ticket does not pick one"). Not the product owner's by the ticket's own text.

## MPSCALC-360 [B1075-F3] usageOnly reading, OPEN (coordinator's call)

Ticket text, word for word: "usageOnly (a component that carries volume and no hardware charge) is the last rule the plan
names. Its reading is not confirmed: under the single deal-level calculation (ruling D-06 a) usage-only lines carry volume
only. Tier 1 (number-affecting). The reading needs the coordinator's confirmation before any build." Recommendation (gate
B1075, quoted by the ticket): "confirm the reading with the coordinator first; then add the member so that usage-only
lines carry volume only, into the one deal-level calculation, with a register row and a red-first test."
Answered? The ruling it rests on is answered: C-45 D-06 a, "keep one deal-level calculation (K-09) fed by group volumes,
keep book-derived costs, no unassigned pool". The reading itself is not confirmed in any record read. CLARIFICATIONS.md:2432
(a records entry): "MPSCALC-360 (usageOnly): HELD, not touched ...; the coordinator's reading is ordered after MPSCALC-361 and
MPSCALC-359; 361 has landed and 359 has not." State today (Jira GET): MPSCALC-361 Done; MPSCALC-359 Backlog with its engine
half landed as MPS #155 on 2026-11-03 (comment 40731: "the engine half only is landed"; the Api request, the note screen and
the editor remain). So the ordering condition is partly met.
Options the source offers: confirm the reading and build, or hold. Frees: MPSCALC-360.
Recommendation: the one the gate gave (confirm, then build); it is Tuesday's confirmation to give, not the product owner's.

## Not read

Other projects and boards (not touched). The decision register PDF of 2026-11-11 (outside the repository). Spec sections 19, 20, 30, 35, 37,
38 and the workbook themselves (the questions are quoted from the register and the Jira tickets). The built product's
current caps, defaults and retention at main (Q-16, Q-17; not read). The reviewer's transcript.
