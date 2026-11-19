# MPS words pack for the v13.4.1 lanes: what exists, what is quoted, what is not drafted (M1 of SWEEP-1630)

Drafted for Tuesday's reading, 2026-11-19, read-only, nothing posted. Every word below is quoted from a ticket, a
ruling or a source document, with its source. Where words do not exist, the ticket is listed as "words not drafted"
with the material that would supply them. No customer word was written by this drafter. Non-ASCII marks in sources
(curly quotes, arrows, middle dots, long dashes) are shown as plain ASCII.

## BLUF

- The sweep's M1 asks the product owner to "approve one words pack ... so builders may use it". **No such pack exists
  and none could be approved today: for 31 of the 35 tickets nothing that is owed has been drafted (23 have only the
  reviewer's prototype text, which the plan says must be rewritten to our behaviour; 8 have nothing).** The plan and the ruling both say the words
  come per lane, after the build, as a pack for his card (quotes in section 1).
- 35 tickets covered. Verdict counts: **2** words already approved, nothing owed on words (MPSCALC-129, 139);
  **2** have exact proposed words waiting for his marks (121, 130); **23** have only source material quoted below
  (reviewer's prototype text or the ruling's own words), not drafted for our product; **8** are "words not drafted"
  (154, 156 rental half, 161, 169, 194 second half, 233 refusal half, 368, 402).
- Two tickets read in Jira as still waiting on words that were in fact approved: MPSCALC-139 (the 11 hint texts are
  items 34 to 45 of list W, approved with C-36 on 2026-10-17; ticket comment 41307 of 2026-11-16 still says "clause 5
  stays NOT MET") and MPSCALC-129 (the three fixed sentences were approved on 2026-10-14; the 2026-11-12 review page says
  the app prints them). Both are records fixes for Tuesday, not word questions for him.
- Hosted state is not needed for any of this. At main 317bbb14 (read 2026-11-19 by `gh api -X GET`, file names
  only) none of the lane V5 to V9 screens exist: 0 file names containing Wizard, FieldLabel, GroupEditor,
  ConfigAssistant, ProjectionTable, Enterprise, `screens/help`, `screens/review` (positive controls in the same
  listing: `infoHintWords` 1, `ConsolidatedBom` 6, `Lifecycle` 34). A file-name absence, not a content read.

## 1. Prior work found (do not redo)

1. **C-45, 2026-10-20 10:09** (card `mpscalc-v13-gap-15-decisions-1020`, option a): D-01 to D-15 accepted. Option a's
   detail, verbatim from the store: "Lanes start in waves as soon as you tap. Every new customer-facing word still
   comes to you as a word pack before it ships, and nothing is deployed without your card." (CLARIFICATIONS.md:660.)
   D-09 a: "yes, all three" formats, "with the Enterprise text to [product owner] as words" (plan recommendation, :677; the
   product owner is named in the source; quoted here by role). D-11 a: "checklist yes, score no". D-15 a: field help
   "yes", "all to the words gate".
2. **Tuesday's own pack of 2026-10-24** (`TUESDAY/0_Brain/projects_index/2026-10-24_mps-words-for-<reviewer>-review.md` (the file name carries the reviewer's first name),
   section 2) says of these tickets: "They build as planned. Option a's detail: 'Every new customer-facing word still
   comes to you as a word pack before it ships, and nothing is deployed without your card.' Words arrive per lane,
   not as one rulings list now." It also records that of the 23 V-lane tickets here, 0 had a comment on 2026-10-24
   (checked again today: 0 comments on each of 237, 243, 246, 264 to 268, 270 to 283, 286, 287).
3. **Words packs that were drafted, sent and ruled (all earlier lanes, none for the 23 below):**
   - list W, 56 items, card `mpscalc-hosted-deploy-12f8e56-1017`, ruled a 2026-10-17 09:23 (C-36, :518-531). File:
     `TUESDAY/5_Project_History/2026-10-17_mps-words-list-W-12f8e56.md`.
   - list W2 for e6f92a5 (C-43, :611); card `mpscalc-hosted-deploy-e6f92a5-1017` ruled a 2026-10-18 18:59.
   - the B449 pack, 346 words, card `mps-hosted-deploy-words-f5b6f5a-1022` ruled a 2026-10-22 15:19 ("Approve all as
     built"; C-48, :917-918). Files: `1_Project_Definition/Deliverables/2026-10-22_word-pack-hosted-f5b6f5a/`
     (strings.tsv 365 rows). It covers the wave-1 builders' lists collected in
     `Registers/2026-10-20_v13-wave1-new-words.md`.
   - 55 words and 8 questions, card `mps-words-55-and-8-questions-b444-b445-b446-1022` ruled a 2026-10-22 22:47 (C-46).
   - feedback triage words, C-65 (2026-10-24); register `Registers/2026-10-24_mps-176-feedback-triage-approved-words.md`.
   - one-page rental proposal words, card `mpscalc-hosted-deploy-words-1112` ruled a 2026-11-12 17:00, and 31
     staff-only strings, card `mpscalc-staff-words-31-deploy-1112` ruled a 2026-11-12 18:20 (CLARIFICATIONS.md:3076:
     "left 0 unruled strings"). The 2026-11-12 10:49 line, quoted in that entry: "new wording for mps are good.
     please go. ahead and deploy".
   - roll-forward stop words, card `mpscalc-rollforward-stop-words-1115` ruled a 2026-11-15 13:49 (C-152).
4. **The 2026-11-12 words review page** (`TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_mps-words-review-page.md`):
   9 wording differences between the printed rental proposal and the approved mock, plus one attachment sentence.
   Card `mpscalc-two-words-questions-1111` ruled a 2026-11-12 07:31; the page was sent (`delivered: ... sent to [product owner]
   bf-eebc278b9968 (HTTP 201)`, 2026-11-12 10:26). **No marks from the review have been recorded** in anything read:
   `decision_queue.sh show` has no later delivery line; the 2026-11-12 to 2026-11-18 CLARIFICATIONS entries do not
   mention it; MPSCALC-121 and 130 carry no comment after 2026-11-11. It is the prior work for 121 and 130 below.
5. **The decision register of 2026-11-11** (card `mpscalc-waiting-register-1111`, ruled a 14:35: "Accept all 29 quick
   recommendations"; recorded as C-102 to C-130) is a PDF kept outside the repository; it was not available. Its
   rows that touch these tickets are quoted where they apply (156, 161, 169, 194, 233, 368).
6. **Not found:** any words pack, card or mail for lane V2 to V11 labels, the Enterprise book text, the help topics,
   the checklist, or the field-help catalogue. Searched: CLARIFICATIONS.md (C-45, C-109, C-116, and the strings "word
   pack", "words pack", "word-pack"), `1_Project_Definition/Registers/`, `Deliverables/`, `Questions_and_Answers/`,
   `Briefs/` file names, Tuesday's briefs folder and `0_Brain/projects_index/` by file name, and `decision_queue.sh
   list ruled` (1,477 rows; every MPS row from 2026-10-25 on read). `decision_queue.sh prior --title` returned 0 for every
   query tried, including a control word that certainly exists ("deploy"), so it was not used as evidence.

## 2. Verdict table (35 tickets)

Key: APPROVED = words already approved, nothing owed; PROPOSED = exact words in hand, waiting for marks; SOURCE =
source material quoted below, not drafted for our product; NOT DRAFTED = no words exist; the source listed is where
they would come from.

| Ticket | Lane | Words verdict |
|---|---|---|
| 121 | feedback | PROPOSED (2 sentences, review page) |
| 129 | rental book | APPROVED 2026-10-14 (ticket text out of date) |
| 130 | printed books | PROPOSED (rows 1, 4, 6, 7, 8, 9 of the review page) |
| 139 | hints | APPROVED (list W items 34 to 45) |
| 154 | phase 2 | NOT DRAFTED |
| 156 | credit box | APPROVED for purchase; rental half NOT DRAFTED |
| 161 | archive | NOT DRAFTED |
| 169 | contract field | NOT DRAFTED (name and words owed on a follow-up card) |
| 194 | feedback 401 | APPROVED first half; "will be lost" sentence NOT DRAFTED |
| 233 | V0-2 clone | APPROVED -COPY and docs; clash refusal sentence NOT DRAFTED |
| 237 | V0-7 | SOURCE (status name ruled; API words not drafted) |
| 243 | V1-8 | SOURCE |
| 246 | V2-4 | SOURCE (tab name) |
| 264 | V5-4 | SOURCE |
| 265 | V5-5 | SOURCE |
| 267 | V5-7 | SOURCE |
| 268 | V5-8 | SOURCE |
| 270 | V6-2 | SOURCE |
| 271 | V6-3 | SOURCE |
| 272 | V7-1 | SOURCE |
| 273 | V7-2 | SOURCE (the seven sentences) |
| 274 | V7-3 | SOURCE |
| 275 | V7-4 | SOURCE |
| 276 | V7-5 | SOURCE (two labels only) |
| 277 | V8-1 | SOURCE (format names, Enterprise text) |
| 278 | V8-2 | SOURCE |
| 279 | V8-3 | SOURCE (section list only) |
| 280 | V8-4 | SOURCE (and approved wording of the short-form sequence) |
| 281 | V8-5 | SOURCE (blocked on brand answer for the default line) |
| 282 | V9-1 | SOURCE (the seven topics, full text) |
| 283 | V9-2 | SOURCE (60 field-help entries, listed by name) |
| 286 | V11-1 | SOURCE (three labels and values) |
| 287 | V11-2 | SOURCE (three labels) |
| 368 | V4 | NOT DRAFTED (field name owed) |
| 402 | deploy | NOT DRAFTED (approved pack exists; the four changes are new) |

Counts: APPROVED 2 (129, 139) + first-half-approved tickets counted under NOT DRAFTED (156, 194, 233);
PROPOSED 2; SOURCE 23; NOT DRAFTED 8. 2 + 2 + 23 + 8 = 35.

## 3. Words by lane

### 3.1 Older [reviewer]-review and records tickets (10)

**MPSCALC-121** (feedback form wedges after a file the browser cannot read). Appears in: the feedback dialog, the
attach refusal line. Built: the refusal exists (MPS #178, comment 41137: "a file the browser cannot read ... is
refused with the sentence the form already has"). The sentence shown today, approved 2026-10-13 (C-26): `Only PNG,
JPEG or PDF files can be attached.` Open word question (ticket comment 41137): "the sentence shown ... does not read
true for a PNG the browser cannot read". PROPOSED words, from the 2026-11-12 review page (last section), both marked "new words and are not yet
approved": Suggested: `This file could not be read. Check that you can open it, then attach it again.` Alternative:
`The file could not be read.` Options on the page: Suggested / Alternative / Keep today's sentence / Other. Marks:
not recorded. Missing: his mark.

**MPSCALC-129** (rental proposal, three untrue sentences). Words card `mpscalc-rental-book-words-1014` was ruled a on
2026-10-14 06:58 with "three wording fixes" (C-31 region, :455-470). The review page rows 2, 3 and 5 quote the
approved fixes and say the app prints them (read of main baf0aabe by that page's author; not re-read here):
- Row 2: `The contract value is worked out for the whole {term}-month term, so it can differ by a few cents from the monthly
  charge multiplied by the term.` (mock still reads `The contract value is the total of the monthly charges over the
  {term}-month term.`)
- Row 3 (quote approved before charges were itemised): `The monthly charge covers the fleet, options and software in
  this proposal. This quote was approved before charges were itemised, so no breakdown is shown.`
- Row 5: `The total monthly charge is worked out for the whole fleet. Each line's monthly charge is rounded to the cent, so
  the line charges above may not add up exactly to the total.`
The ticket's description (written 2026-10-14) still quotes the three untrue originals (rental.ts:136, :44, :46).
Missing: nothing for the product owner; Tuesday's records pass should check main and note the ticket. Unverified by
this drafter: that main prints the three approved sentences.

**MPSCALC-130** (printed A4 books: style done, words per page differ from the mock). Style half built (comment 41136).
The open item is which side's words are right. The review page rows, app today versus mock:
- Row 1, cover line: app `{term}-month rental`; mock `{term}-month rental  |  STANDARD PRICING`. "Approved on 14 Oct? No."
- Row 4, section 2 box: app prints nothing; mock `Not yet specified` / `Applicable tenant subscriptions and the
  detailed deployment calendar have not been supplied.` / `These must be captured before a firm service schedule is
  issued.` (removed 2026-10-16, listed removed in C-36).
- Row 6, section 10: app prints nothing; mock heading `Recommended next steps`, numbered list (typical variant's
  five steps start `Sample Customer R confirms its fleet allocation, site locations, volumes and output requirements.`
  and end `The parties complete contracting and agree pilot / rollout dates.`).
- Row 7: app none; mock `Acknowledgement indicates intent to progress final configuration and contracting; it is not
  acceptance of a binding MPS agreement.`
- Row 8: app none; mock `Proposal basis` / `Prepared from quote {reference}, version {n}, in the Datasec MPS
  calculator.`
- Row 9, draft ribbon: app `LOCAL DEMO` on a local run, hosted `SHOWCASE`; mock `SHOWCASE` (existing word, not new).
- Consequence: the large book prints 15 pages, the mock 16 (after rows 4, 6, 7, 8 were removed).
Each row has marks App / Mock / Other. Marks: not recorded. Rows 2, 3 and 5 are the 129 words above.

**MPSCALC-139** (info hints site-wide). APPROVED. List W items 34 to 45 (C-36 "the 56 words of list W as written",
2026-10-17) are the 11 hints and the button label, for example: item 34 `Hint button "About {topic}"`; item 36 `Hint
"Optional": "An extra the customer may choose, such as a stapler or finisher. It is priced per unit and never added
to a total."`; item 37 `Included`: "Supplied at no charge to the customer. Its sell price is 0, but its cost still counts
against the margin."; item 38 `Credit`: "A deduction, such as a trade-in or a bundle credit. Its sell price and its cost count
as negative amounts."; item 43 `Ink rate`: "For large-format devices: the charge to the customer for each unit of ink, in
dollars ex GST. Set the unit beside it. Leave it empty for no ink charge." (full set in the list W file). The ticket's
comments 40364 and 41307 say clause 5 "no approval is recorded"; list W and C-36 are that approval. What does remain
open on the ticket is clause 4 (axe check, a dependency decision, comment 41307), not words. Typical values in
hints 41 and 42 carry a figure from the review quote and are not repeated here.

**MPSCALC-154** (client fleet template spreadsheet). NOT DRAFTED. Source: the ticket's acceptance names "words
approved by the product owner (K-17)"; K-17 appears in no CLARIFICATIONS entry (0 hits; control: K-14 has 1). Source
material: the example client's fleet sheet in the project source documents (confidential copy); the ticket quotes the
product owner (review PR-36, 40:42) "Use the [the example client] spreadsheet as an example, create a templated
spreadsheet that we provide to the client". **Unverified reading:** the ticket also quotes PR-37 at 42:28, same
speaker, "No, let's not do it. Let's force everyone to do it through the tool." The ticket reads it as limiting the
template to the fleet sheet; it could also read as withdrawing the idea. Not decided here.

**MPSCALC-156** (credit box). APPROVED for purchase: list W items 29 and 30, `Credit included in this proposal` and
`Each credit is already taken off the package price shown, ex GST.` (ticket comment 40954 confirms approval under
C-36; the earlier comment 40369 is out of date). Rental half NOT DRAFTED: ruling C-114 (2026-11-11, "Yes. Your 24 Oct
ruling already allows rental credits; the box is the sweetener you asked to call out.") requires a rental credit field
and box; the comment says "any new words go to the product owner first". Source material for the rental words: the two
approved purchase sentences above and RentalDocument.tsx (no credit handling at main per comment 40954).

**MPSCALC-161** (archive a quote). NOT DRAFTED. Ruling C-115 (2026-11-11): "Archive. Quotes and snapshots are audit
records." The ticket's default (K-16): owner may archive a Draft or Rejected quote; Submitted/Approved cannot be
archived; archived quotes leave every list; an Administrator can list and restore them. No label, button or message
word is drafted. Appears in: the quotes list (QuoteList.tsx) and an administrator view.

**MPSCALC-169** (contract field naming the price-book versions). NOT DRAFTED. C-68 (2026-10-25): "Yes in principle: a
builder proposes the field name and the contract words on a follow-up card"; "No contract change is made until you
approve the exact text on that card." C-116 (2026-11-11): "Approve. Your earlier ruling holds every contract change
until you approve the exact name." The only name anywhere is the ticket register's suggestion, "a field like
lineMarkupsSourceVersions" (CLARIFICATIONS.md:1354, a builder suggestion, not proposed on a card). Where it would
appear: Dtos.cs beside lineMarkupsOverlayVersion, openapi.json, docs/API.md:208-210 (developer documents; C-109 b
keeps developer-only docs out of word review, but a contract member name is the product owner's by C-116).

**MPSCALC-194** (feedback dialog after a feedback-only 401). First half APPROVED and live: C-37, "Your feedback could
not be sent. Try again." Second half NOT DRAFTED: ruling C-118 (2026-11-11), "Tell the user. Keeping it means storing
customer text in the browser." comment 41082: the user is told the text will be lost; "the sentence ... goes to the
product owner before it ships". Appears in: the feedback dialog when the session ends (FeedbackDialog.tsx).

**MPSCALC-233** (V0-2 clone). Approved: `-COPY` (the clone reference suffix) and the duplicate descriptions
(strings.tsv rows for #85, openapi.json:350 and :877, docs/API.md:413), inside the 346-word pack ruled 2026-10-22
(C-48; gate finding B318-3 had called `-COPY` customer-visible because quoteRef is printed on the proposal). NOT
DRAFTED: the refusal for a typed reference that already exists. Ruling C-119 (2026-11-11): "Refuse. Two quotes with
one reference break the audit trail." It is an API refusal sentence; Tuesday's answer 1 on SWEEP-1630 treats such an error string as "text a user can see".

### 3.2 Lane V0, V1, V2, V4 (4)

**MPSCALC-237** (V0-7, Won acceptance record and Issued status). The name "Issued" is ruled (C-45 D-12 a: "an Issued
status and a PO / acceptance record on Won are in; the footer stays 'Commercial in confidence'"). API description
words (contract, docs/API.md) NOT DRAFTED; the ticket says "New words go to the product owner's words gate before any
deploy". Source: B309 wave-1 list (`Registers/2026-10-20_v13-wave1-new-words.md`:54-87) holds the event words, among
them item 22, the `QuoteEvent.kind` description that adds the `accepted` sentence "and there is no separate issued
kind"; docs/API.md:384 "`accepted` is now a kind in the contract's event list." and :382 "The *status* 'Issued' ruled by D-12 a is a different thing and is a later change."

**MPSCALC-243** (V1-8 guided wizard). Source words, reviewer's prototype (HTML:25, :491-498, gap row V-04): two modes
"Single-page | Advanced" and "Guided wizard | Sales admin"; five steps "Opportunity", "Device configuration", "MPS
calculations", "Software", "Review & submit"; buttons Previous / Next; a step-1 gate on customer, reference and term.
The ticket: "Mode names and the default mode are words for the gate." Default mode: not drafted. Gap row V-04
marks it "[product owner]: words (mode names, default mode)".

**MPSCALC-246** (V2-4 Issued queue). Source: only the status name "Issued" (D-12 a) and the reviewer's "Sent". Tab
label NOT DRAFTED.

**MPSCALC-368** (V4 purchase projection on the API). NOT DRAFTED. C-110 (2026-11-11): "Hide all six; agent proposes
the name for your approval. It matches how other cost and profit figures are restricted." Owed: the field name and
the openapi projection description and docs/API.md section (comment 40935 clause 6 "NOT MET"). Source: engine
`PurchaseResult.cs:287`, existing names such as `annualRecurringGp` (ticket text). Developer-doc sentences may skip
review per C-109 b; the member name does not.

### 3.3 Lane V5 (4)

**MPSCALC-264** (V5-4 group editor and Duplicate). Source, reviewer's prototype (HTML:467), the confirmation: "Duplicate
this configuration as an ADDITIONAL billable fleet group? Hardware, software, services and page volumes will all be
counted again. Cancel if you only want to increase the existing fleet quantity." Gap row V-43. Group editor labels
(name, fleet quantity, per-device components, volume basis, per-group rates and fee) not drafted. Plan: button
"Duplicate billable group".

**MPSCALC-265** (V5-5 configuration assistant). Source (HTML:41-45): heading "Smart configuration assistant"; categories
"All recommendations", "Accessories / card readers", "HP Care Services", "Hardware licences", "Software"; note "Selections
are never added automatically. An advisor must verify OEM eligibility, regional availability, entitlement and device model
compatibility." Ticket words: `"Add 1 per device"` with a confirm; suggestions "labelled as suggestions"; "no
suggestion is worded as verified". Our wording NOT DRAFTED.

**MPSCALC-267** (V5-7 projection table). Source (gap row V-55): table "monthly / annual (x12) / contract (xterm)": "pages
mono, colour, total; click cost, managed service cost, total recurring cost; click revenue, service revenue, total
recurring revenue; recurring GP". Ticket: "labels match the words list" (no list exists). NOT DRAFTED beyond these.

**MPSCALC-268** (V5-8 site allocation). Source (HTML:29, :548-549): section "Site allocation & deployment"; fields "Customer site"
(placeholder "Melbourne office"), "Configuration", "Number of devices for this site"; button "Allocate devices"; empty
state "No site allocations yet."; warning "<name>: allocated <n> / <qty> devices". Ticket: "the reconcile warning".

### 3.4 Lane V6 (2)

**MPSCALC-270** (V6-2 template library). Source (gap row V-40, HTML:766-795): "+ New template", "Copy active group", saved list,
name, "Save" / "Delete", and the line "Creating or editing a template does not change the current quote." The ticket
names New, Edit, Archive, "Copy active group". Staff API words for the template store are already approved: 13
templates-API errors in the 31 staff strings ruled 2026-11-12 18:20 (card `mpscalc-staff-words-31-deploy-1112`).
Screen labels NOT DRAFTED.

**MPSCALC-271** (V6-3 "Add to quote"). Source (HTML:790): button "Add to active quote"; prompts "Enter a whole number of devices
greater than zero.", "Add at least one SKU to the template.", and the confirm "Add <qty> devices using "<name>" as a
NEW billable group?". Ticket label: "Add to quote". Not drafted for our product.

### 3.5 Lane V7 (5)

**MPSCALC-272** (V7-1 summary tiles, staff-only). Source (gap row V-65, HTML:101): tiles "Customer, Quote, Contract, Upfront
sale, Upfront GP, Annual recurring GP, Total contract value, Contract GP, TCV margin" and a gate line "Automatic
readiness and reconciliation checks passed...". Ticket's own tiles: "upfront sale and GP, annual recurring GP, contract
value, contract GP and contract margin". Heading in the prototype: "Quotation review & approval" / "Verify commercial values
before releasing the customer proposal." Labels for our product NOT DRAFTED.

**MPSCALC-273** (V7-2 pre-issue checklist). The seven sentences, verbatim from the reviewer's file (HTML:503-509); the
ticket says "The seven sentences come to the product owner as a word pack before they ship":
1. `Customer, site, quotation reference and contract term are confirmed`
2. `Device group quantities, standalone BOM quantities and related accessories are reconciled`
3. `Synnex and HP software pricebooks, discounts and licence terms are current and approved`
4. `HP Care eligibility and delivery, installation and staging are confirmed`
5. `MPS volumes are correctly entered as per-device or total fleet, with no duplication`
6. `Hardware/software upfront GP, annual recurring GP, TCV and financing terms are reviewed`
7. `Customer exclusions, GST treatment, software credits and quotation validity are checked`
Heading "Pre-issue checklist"; alert `Complete every review checklist item before approving.` Note: sentence 6 names
"financing terms" while D-02 a defers finance/lease; sentence 3 names Synnex and HP; whether to adopt them as written
is the word question. Gap row V-66: "[product owner]: words (7 sentences)".

**MPSCALC-274** (V7-3 authorisation reference). Source (HTML:101, V-67): labels "Approver's full name" (placeholder
"Authorised HPSC manager") and "Approval notes / authorisation reference" (placeholder "e.g. management approval
reference, special pricing authorisation"); alert "Enter the name of the authorised approver." Our rule: the approver
stays the signed-in identity, so "full name" is not adopted as a typed field. Label NOT DRAFTED.

**MPSCALC-275** (V7-4 acceptance capture). Source (HTML:31, :561): card "Customer acceptance & fulfilment"; labels "Customer
acceptance reference" (placeholder "PO / signed approval reference"), "Acceptance date"; button "Record customer
acceptance"; alerts "Approve an unchanged quote before recording customer acceptance", "Enter customer acceptance
reference and date". The ticket's own: "PO / reference and date". NOT DRAFTED for our product.

**MPSCALC-276** (V7-5 version diff view and export). Source (gap row V-22, V-81): "Save revision", "Export revision history"
(JSON). Diff view labels NOT DRAFTED; related existing words: "What changed since the previous calculation"
(PriceView.tsx:276-285).

### 3.6 Lane V8, customer proposal (5), customer-facing

**MPSCALC-277** (V8-1 proposal formats). Source (HTML:48-53, :680, :694; gap row V-70): buttons "Quick Quote (1-2 pages)",
"Standard MPS Proposal", "Enterprise MPS Proposal"; document titles "QUICK QUOTE", "MANAGED PRINT SERVICES PROPOSAL",
"ENTERPRISE MANAGED PRINT SOLUTION"; the note "All formats exclude internal buy costs and gross profit. The approved
quotation is the source of customer pricing." and "Opens a print-ready document. Use Print -> Save as PDF. Customer
issue is blocked unless the current quote is approved and unchanged." The Enterprise text, verbatim (HTML:694), the
text D-09 sends to the product owner as words:
- Heading `Site rollout and implementation`: "Confirm site-level quantities, access requirements, network prerequisites and
  installation windows. Recommended implementation: discovery and validation -> configuration and staging -> controlled
  deployment and UAT -> operational handover."
- Heading `Identity and print security`: "HP Authentication Manager, Microsoft Universal Print, Conditional Access and
  any Microsoft 365 scan services require tenant-specific technical validation, licensing and security policy
  alignment."
- Heading `Governance and assumptions`: "Supplier price validity, applicable service SKUs, customer approvals,
  acceptance criteria, finance provider terms and scope exclusions must be confirmed in the final statement of work."
Ticket: "Name Quick as today's short form and Standard as today's full book". Not drafted for our product; the text above
is the reviewer's prototype, names HP and Microsoft products, and mentions finance provider terms (see D-02 a).

**MPSCALC-278** (V8-2 priced or unpriced). Source (gap row V-63, HTML:245, :270): options "Show customer unit and extended
prices" and "Show SKUs and quantities only"; the unpriced value shown is `Available on request`. Ticket's own pair:
"unit and extended prices" / "SKUs and quantities only". The label and the placeholder are not drafted for ours.

**MPSCALC-279** (V8-3 fleet schedule, per-group click rates, notes, PO line). Source (gap row V-71, HTML:242-281): cover
stats (devices, term, upfront package); "fleet configuration schedule by group (devices, mono/colour per month)";
"commercial schedule with per-group click rates"; "opportunity notes"; "acceptance block with PO / reference". HTML:696
acceptance lines: "Customer authorised representative: ____", "Purchase order / reference: ____", "Signature and date:
____", "Quotation is not binding until accepted under agreed commercial terms." Our current block: "Authorised
representative / Title / Date" (sections.ts:359). Footer unchanged: "Commercial in confidence" (C-13). NOT DRAFTED.

**MPSCALC-280** (V8-4 implementation sequence). Source (gap row V-71): "01 VALIDATE / 02 PREPARE / 03 DEPLOY / 04 ACCEPT";
HTML:694 sequence "discovery and validation -> configuration and staging -> controlled deployment and UAT ->
operational handover". Approved wording that already exists for the SHORT form (list W items 23 to 27, ruled 2026-10-17):
`Implementation sequence`; `1. Validate`: "Confirm the {n}-device BOM, site allocation, workflows, users and volumes.";
`2. Design & stage`: "Approve network and security prerequisites, configuration, reader mapping, consumables and
installation schedule."; `3. Pilot & deploy`: "Test print, scan and authentication workflows; deploy in agreed
waves and provide training."; `4. Accept & operate`: "Complete user acceptance, document support channels and commence
meter-based service processes." Whether the Standard block reuses these is the open word question; the ticket says
"The wording comes to the product owner as a word pack."

**MPSCALC-281** (V8-5 trading-entity line). C-45 D-14 c: "a setting per quote, with today's Datasec default".
Source: the prototype default "HP Solutions Centre" (HTML:18, :244, :266; gap row V-84 "conflicts"). Whether HP
branding is allowed is open question Q-03 (see the questions sheet); the ticket prints "today's wording" when no
setting exists. Setting label NOT DRAFTED.

### 3.7 Lane V9 and V11 (4)

**MPSCALC-282** (V9-1 help page, seven topics). Source, verbatim (HTML:736; the plan says "several describe a
browser-only prototype and must be rewritten (for example, our quotes are kept on the server)"). Title of the dialog:
"Quote Builder - Help & Guidance"; intro: "Click the blue i icon next to an individual field for specific guidance. The
topics below cover the complete quoting workflow."
1. Getting started: "Complete Opportunity Details first. Then select or build devices, enter MPS volumes, choose
   contract-term software and review the BOM. Both Advanced and Guided modes use the same quote values."
2. Quantities and device baskets: "One printer and one card reader in a basket applied to 12 devices produces 12 of each.
   Duplicating a billable fleet group adds an additional group; saving a template alone should not add anything."
3. Print volumes and recurring GP: "Fleet-wide volumes are not multiplied by device quantity. Per-device volumes are
   multiplied once by devices. Monthly MPS gross profit is monthly customer charges less monthly internal costs."
4. Software term pricing: "A full-term software licence is a one-off purchased entitlement for the contract period. Avoid
   multiplying its price by the number of contract months. Verify software renewal coverage independently."
5. Financial validation and approvals: "Use Quote Readiness & Financial Validation at the BOM stage. Correct critical
   calculation/quantity mismatches before approval. A passed arithmetic check is not evidence of approved supplier terms."
6. Customer proposals: "Generate the chosen customer quote format from the approved quote. Always inspect the resulting
   document before issue; internal costs and GP must remain confidential."
7. Prototype limitations: "Version 13.2 is a standalone HTML prototype. Local data are not shared; role previews do not
   enforce security. Live Entra login, central approval audit, server PDFs and Business Central integration require a
   backend."
Topic 7 is false for our product; topics 1 and 5 name Guided mode and a readiness panel that differ from ours; no
rewrite exists. The ticket says "Start: now as a draft of words (plan section 4)" and has no comment: nobody has started.

**MPSCALC-283** (V9-2 field-help catalogue). Source: the prototype's `HELP` table, 60 entries (HTML:735), each a title
and a sentence, keyed by label: Customer / organisation, Opportunity / quote reference, Account manager, Site / delivery
location, Number of devices, Contract length (months), Acquisition method, Supplier pricing tier, Hardware gross margin
target (%), Finance annual interest (%), Finance deposit ($), Opportunity notes, ... through Quote valid for (days).
Example, verbatim: key "Number of devices" -> "Fleet quantity": "Total number of devices in the opportunity. Device
configuration groups should reconcile to this value; quantities must not be multiplied twice." Existing approved hints
in our product: the 11 of list W items 34 to 45. D-15 a: "adopt ... where they match our behaviour, rewrite the rest, all
to the words gate". None of the 60 has been compared with our behaviour or rewritten. NOT DRAFTED for our product.

**MPSCALC-286** (V11-1 approval thresholds). Source (HTML:26; gap row V-18): labels "Minimum initial gross margin (%)",
"Minimum TCV gross margin (%)", "Maximum unapproved discount (%)", prototype values 12, 10, 10. Gap analysis: these are
"prototype defaults, not a ruled policy"; the ticket: "The values are in the gap analysis (section 1, V-18), not in this
ticket" and D-10 a rules "Review warnings at the reviewer's three values, not blocks". Review issue sentence NOT DRAFTED.
See Q-10 on the questions sheet.

**MPSCALC-287** (V11-2 trading entity and document defaults). Source (HTML:24, gap row V-16): "Trading entity / supplier
(default "HP Solutions Centre")", "Quote valid for (days, default 30)", "Currency AUD". Our default: "today's house
default" (D-14 c). Labels NOT DRAFTED.

### 3.8 Deploy words

**MPSCALC-402** (roll-forward stop words). Approved as written 2026-11-15 (C-152, card `mpscalc-rollforward-stop-words-1115`
ruled a): the main stop line and eight companion lines of the pack (operator messages in the deploy log, not customer
words). Ticket comment 41217: "each of this ticket's four items would change a word or a path of that approved pack, so
the ticket stays open". The four changes (say entries not row(s); token-failure wording; PRE-1 line; the silent return) are
described in the ticket but no replacement sentence is drafted ("Nothing is drafted by this ticket"). One more item,
comment 41217: after MPS #194 the undecided line prints `git answered 128` although git answered 1. Per comment 41217
a change goes back to the product owner first (the coordinator's reading).

## 4. What would make M1 a real decision

Stated, not recommended: the sweep's wording ("approve one words pack") does not match the standing process (C-45
option a detail; Tuesday's 2026-10-24 pack: "Words arrive per lane"). The sources in section 3 are the reviewer's prototype text; adopting them
as ours is a drafting step that nobody has taken. The only exact words ready for his marks today are the two for
MPSCALC-121 and the review page rows for MPSCALC-130 (page already sent 2026-11-12).

## 5. What was not read

Other projects and boards (not touched). The decision register PDF of 2026-11-11. The B100 STATUS words list and the full 346-word
strings.tsv beyond the rows quoted. The full text of the Standard proposal in HTML:242-281. The reviewer's handoff
zips and docx. The Jira comments of tickets outside the 35 (except 359, 361, 253, 34, 27 for the questions sheet).
Hosted site, any app host, any test, any PR diff at main (file names only). 
