# B1744: MPS Calculator v13.4.1, which tickets are buildable now under C-45, in lanes (read-only sweep)

Written 2026-11-19 (clocks by `date`: 17:15 start, 17:26 last GitHub read, AEDT) by a read-only lane analyst for Tuesday.
Nothing was built, ticketed, commented on or decided. Project: `Datasec MPS Commercial Calculator` (Jira MPSCALC; repo
`datasecau/MPS-Commercial-Calculator`). Folder verified by listing `!CODING/Datasec/`. Code read at origin main
**`317bbb14c7258023b1d2855a9bcce1b9b07b93f6`** (the squash of MPS #217; read again at 17:26: unchanged; open pull requests
0, control: `pulls/99999` answers 404), through `gh api -X GET` under the project's own `GH_CONFIG_DIR` (tarball unpacked in
scratch, `.local` and `Source_Documents` excluded at extraction). Jira read by GET only, credentials read by name in-process.
Marks: MEASURED = I printed it myself; RELAYED = I read it in another seat's file or a ticket; UNMEASURED = nobody has.
Non-ASCII marks in quotes are shown as plain ASCII.

## 1. BLUF

- **Under the standard of this commission (a builder may use only words that already exist as source text, and every other
  word must have been drafted by someone): 3 keys are buildable now, in 3 lanes (267, 278, 121), and 7 more are
  buildable once Tuesday gives one reading each (237, 236, 273, 274, 275 in one contract lane; 314; 360). 57 keys were
  judged: the 35 of the sweep and 22 more open v13 lane keys.** The other 47 are not buildable now:
  14 need words nobody drafted, 9 wait on an unbuilt predecessor, 6 wait on a contract name, 12 need a
  ruling, marks, a decision or outside data, 5 need only records or a pack, 1 is in flight.
- **The words are not what blocks most of them. A predecessor is.** Main has the ENGINE halves of the V4 device groups
  (fleet quantity, volume basis, managed-service fee, tier override, sell method, sites: MPS #133 to #140) but the Api has
  none of those members (0 hits for `FleetQuantity` in `src/MpsCalc.Api`; control: 1 hit set in
  `src/MpsCalc.Engine/Input/PurchaseInput.cs:71`), and the tickets that were to carry the Api, DTO, contract and web halves
  were never filed ("no ticket holds them", comment 40504 on 256; "held as separate work", 40482 on 255; "Open: the Api, DTO,
  openapi and web", 40401 on 252 and 40403 on 259). Every V5 and V6 screen, and V8-3, stands on them: 264 265 268 270 271 279
  (6 of the 35) plus 248 and 258. A name card for those members (C-68/C-116 reading, section 2.4) is the single unlock.
- **The rule (section 2).** A lane may be built and its new words come to the product owner as a word pack BEFORE THE HOSTED
  DEPLOY, not before the merge. The sentence: C-45 option a detail, `CLARIFICATIONS.md:660`: "Lanes start in waves as soon
  as you tap. Every new customer-facing word still comes to you as a word pack before it ships, and nothing is deployed
  without your card." Not settled: "ships" is never defined; the practice (7 merged lanes of 2026-10-20, pack ruled
  2026-10-22) reads it as the deploy.
- **Two lanes can run at once** (section 6): the five no-contract lanes touch no common file; the contract lane is serial.
- **Drafter B was right on the main fact and wrong or short on four** (section 7).

## 2. The rule (task 1)

### 2.1 The rulings, word for word (file `1_Project_Definition/CLARIFICATIONS.md`, read whole at the lines named)

**C-44** (heading :641; the product owner's words :645, 2026-10-20 09:44:20): "It's not a replacement, it is additional
screens, change of layout, and additional features to change the flow and everything else. ... Review these documents
extremely carefully and create a gap analysis and map out what needs to be done to get the new version of the calculator
up and running and as close to the following documents as possible. Spin up as many agents as you can to make this happen."
Settles (the records seat's reading, :647): "(1) v13.4.1 is **additive**: the calculator is not rebuilt, and its existing
rulings stand unless Kam reverses one; (2) the work is a gap analysis and a map ... then a build in parallel lanes".

**C-45** (heading :654; card `mpscalc-v13-gap-15-decisions-1020`, option a, 2026-10-20 10:09). Option a, :660, verbatim from
the store: "[a] Accept all 15 recommendations (recommended)"; its detail: "Lanes start in waves as soon as you tap. Every new
customer-facing word still comes to you as a word pack before it ships, and nothing is deployed without your card." The
card's default (:661, not triggered): "If you do not tap, Tuesday starts only the lanes that need none of the 15 decisions,
and holds the rest." :665: "Ruled: **a** on fourteen rows and **c** on D-14". The fifteen rows (:669 to :683; each: the
ruled option, then the cell "What it lets the plan build / does not"):

| Row (line) | Ruled option | Lets / Does not (verbatim) |
|---|---|---|
| D-01 (:669) | "a) yes: screens now, platform later" | Lets: lanes V0-V11 build the screens and flow on the server calculator now. Does not: the master prompt's platform asks (roles, Azure SQL, server PDFs, Business Central, Xero, resellers) stay in the plan's group L (later or blocked). |
| D-02 (:670) | "a) later, once a financier's schedule exists" | Lets: T-V4-9 is filed as a later-phase placeholder so its dependency is visible. Does not: any finance / lease mode, deposit or finance row in the summary rail until a financier's schedule exists. |
| D-03 (:671) | "a) keep per pool, add a quote-level manual override on purchase too" | Lets: T-V4-7 (per-pool tier kept; quote-level manual override on purchase too). Does not: a whole-quote device-count tier. |
| D-04 (:672) | "a) keep markup, allow "margin" per section (the engine has both), still no default" | Lets: T-V4-8 (margin per section beside markup, no default). Does not: one margin on every line, or any default markup or margin. |
| D-05 (:673) | "a) yes: sections become groups (label stays)" | Lets: purchase sections become billable device groups; T-V4-1, -2, -4, -6, T-V5-4 and lane V6 can be built. Does not: groups beside sections as a second structure. |
| D-06 (:674) | "a) keep one deal-level calculation (K-09) fed by group volumes, keep book-derived costs, no unassigned pool" | Lets: T-V4-3 and T-V4-2's usageOnly rule feed one deal-level calculation. Does not: T-V4-10 (unassigned volumes, typed click costs): not filed. |
| D-07 (:675) | "a) keep C-10" | Lets: nothing to build, today's rental software spreading stands. Does not: T-V4-11 (software once upfront on rental): not filed. |
| D-08 (:676) | "a) yes, wave 4" | Lets: T-V1-8, the guided wizard, in wave 4 after the single-page layout lands. Does not: start before T-V1-3. |
| D-09 (:677) | "a) yes, all three" | Lets: T-V8-1, three proposal formats; the Enterprise text comes to the product owner as words. Does not: ship any new customer word without that word pack. |
| D-10 (:678) | "a) Review warnings at those values" | Lets: T-V11-1 settings and T-V3-2 threshold checks as Review warnings. Does not: any approval block at those values. |
| D-11 (:679) | "a) checklist yes, score no" | Lets: T-V7-2, the pre-issue checklist. Does not: T-V3-3's readiness score (no score is built). |
| D-12 (:680) | "a) Issued + PO yes, footer C-13 stays" | Lets: T-V0-7, T-V2-4, T-V7-4 (Issued status, PO / acceptance record); T-V8-3 keeps the footer. Does not: change the footer wording. |
| D-13 (:681) | "a) +/-0.01 (cents, matching C-30)" | Lets: T-V3-1 reconciles to a tolerance of one cent. Does not: a looser tolerance. |
| D-14 (:682) | "c) a setting per quote" | Lets: T-V8-5 and T-V11-2, a trading-name setting per quote with today's house default. Does not: choose a brand for the product owner. |
| D-15 (:683) | "a) yes" | Lets: T-V9-1 and T-V9-2, field help and the help page, all through the words gate. Does not: ship unapproved words. |

:688 (the records seat's reading, not his words): "Settles: the 12 lanes (V0-V11) and the order of the plan's section 2 are
the build plan, and lanes start in waves; **every new customer-facing or screen word still comes to Kam as a word pack
before it ships and nothing is deployed without his card** (option a's detail above, verbatim)". :689 "Not settled: **PR #84
must merge before lane V10 starts** (plan :192); the data the calculator does not have (gap analysis section 4: lender
schedules, HP-verified compatibility, care terms and eligibility, large-format items, Business Central / Xero tenants, the
approval-threshold policy Q-10, monthly-billed software SKUs); the platform asks; the authorisation rule for rental credits
(T-V4-12; no D card)."

**Earlier practice the plan relies on.** Build plan `2026-10-20_v13.4.1_BUILD_PLAN.md:21`: "Every new staff or customer word
goes to Kam at the words gate before any hosted deploy. This is the standing practice: K-02 "approve every sentence at the
gate", C-26, C-36, C-43." C-23 MPS-6 (`CLARIFICATIONS.md:333`, ruled 2026-10-13): "The new message comes to you as wording
before any deploy." Tuesday's own ruling on 2026-10-20 (:706, a coordinator ruling, not his): "The new readiness sentence and
the new Review check are new words and **go to the words gate before any deploy**." The tickets filed from the plan end:
"New words go to the product owner's words gate before any deploy." (e.g. MPSCALC-237, 243, 264, 265, 267; MEASURED in the
descriptions).

**C-79** (:1712, 2026-11-01): the words, :1714: "Done means merged to main, the same as Composer". The records seat's reading,
:1716: "a ticket moves to Done when its change is merged to main AND each Done-when clause of the ticket is MET; a clause
that needs a deploy, a words approval or a further ruling is still not met by a merge".

**C-85** (:2325, 2026-11-02): the words, :2327: "Land it and ticket the gaps" (MPS #145, the template store). The brief
relayed there says it "does not settle a hosted deploy, the seven word-pack sentences, or clause 4 of MPSCALC-269". :2331
"Not settled: ... the seven word-pack sentences (row [B1137-WORDS-1] ...)".

**C-68** (:1348, 2026-10-25), option a detail (:1351): "No contract change is made until you approve the exact text on that
card. The builder also proves the field is set from the same source set the trial run reads, with a test." Settles (:1353):
"No contract change is made until the exact text is approved there."

**C-109** (:2716, 2026-11-11): the recommendation he accepted (:2719): "Leave developer-only docs out of your word review;
approve only the customer-visible sentence. One is developer documentation that customers never see." What it settles
(:2720): "developer-only documentation sentences are corrected from what the code does without the product owner's word
review; only a sentence a customer sees goes to the product owner for approval."

**C-110** (:2725, 2026-11-11, MPSCALC-368): (:2728) "Hide all six; agent proposes the name for your approval. It matches how
other cost and profit figures are restricted." (:2729) "a name for the field is proposed for the product owner's approval
(clause 6 of comment 40935 waits on that approval)."

**C-116** (:2779, 2026-11-11, MPSCALC-169): the recommendation he accepted (:2782): "Approve. Your earlier ruling holds every
contract change until you approve the exact name." What it settles (:2783): "The field is approved as proposed; under entry
C-68 its exact name and words still come to the product owner before any contract change."

**Later cards that widen it.** `decision_queue.sh show mps-412-panel-note-words-1118` (MEASURED, ruled a 2026-11-18 11:22):
option a, "Developer fix, list it after", detail "Corrected from the code with a test; the review reads the words; you see
the sentence after it lands"; delivered: MPS #215 landed, "the final sentence sent to the product owner on the live board
after landing; not deployed". C-95 (:2573, 2026-11-06, relayed): "yes, hold UAT but work on everything else". Kam,
2026-11-19 16:26:43 (the commission): "keep working on other outstanding tickets and the backlog."
**Later kit convention that narrows it:** the builder kit B1594 (`tuesday/briefs/2026-11-15_B1594_...`:69) forbids "no new
customer-facing or operator-facing word, no new setting, no new environment variable, no new npm package"; kit B1741 builds only
a sentence that "is accepted" and states "MPSCALC-195 IS NOT IN THIS KIT (its accepted sentence is not on any record)".

### 2.2 What I conclude (both directions)

1. **May a lane be built before he sees its words? Yes.** :660 "Lanes start in waves as soon as you tap" and every D-row's
   "Lets: ... can be built". No ruling I read requires a word pack before a build starts. D-09's "Does not: ship any new
   customer word without that word pack" and D-15's "Does not: ship unapproved words" both bar SHIPPING, not building.
2. **May it be merged to main before he sees its words? Yes in practice, never ruled in terms.** Seven lanes merged on
   2026-10-20 with their new words unapproved (section 2.3); #145 landed 2026-11-02 with seven word-pack sentences pending
   (C-85 :2331); #174 landed 2026-11-10 with its contract words unapproved (comment 40935, clause 6 unmet). No sentence
   forbids it and no ruling says the merge is the ship. C-79 makes the merge the Done event, and :1716 keeps a words
   approval as a separate clause, so a merged lane with unapproved words stays Backlog: that is the existing mechanism.
3. **Is "ships" the deploy or the merge? The deploy, by the practice and every text that glosses it** (plan :21 "before any hosted
   deploy"; C-23 :333 "before any deploy"; Tuesday's :706 "before any deploy"; the tickets "before any deploy"; the 2026-11-12
   card title "the new words ... before the hosted deploy"). C-45's own sentence uses two verbs, "ships" and "deployed", and
   defines neither. **The rule I conclude:** build and merge may precede his sight of the words; the hosted deploy needs both
   the word pack ruled and his deploy card. The sentence that carries it is :660.
4. **A cost the rule hides.** A deploy takes main (the deploy cards read "Deploy main now", C-48 :916; the deploy seat measures
   "words 0W delta", C-47 and C-48 lines `DEPLOYED:`). Unapproved customer words merged into main therefore stop the next
   deploy of main until their pack is ruled, or force a deploy of an older pinned commit (as C-48 re-pinned to `35887699`).
   Each merged lane with new customer words puts a clock on the next deploy. (My reading of the deploy lines; not a ruling.)
5. **Who drafts the words.** In wave 1 (2026-10-20) the builders drafted their own new words in their STATUS files ("NEW WORDS:
   the four column headings", comment 39795 on 244; 39797 on 245; 39751 on 248), a records seat collected them
   (`Registers/2026-10-20_v13-wave1-new-words.md`) and the pack of 346 words went to the card. Today's builder kits forbid a
   builder to write a new word (B1594:69). The commission's standard ("a ticket whose words nobody has drafted is NOT
   buildable") is the kit convention, not the wave-1 practice. **Under the wave-1 practice most of the 14 "words nobody drafted"
   keys would be buildable; under today's kits none is.** That is Tuesday's choice (question 1, section 8).

### 2.3 What the lanes that ALREADY landed under C-45 did (MEASURED from the merged-PR list, CLARIFICATIONS.md and the decision store)

| Lane | Pull requests (merged) | New words | Pack and when | Deploy |
|---|---|---|---|---|
| Wave 1: V0 contract, V5 starters, V3, V1 phases 1 and 2, V2 Home, follow-ups | #85, #86, #87, #88, #89, #90, #91 (all 2026-10-20; the ones whose time I read ran 03:14Z to 16:19Z) | yes, drafted by the builders (UI and staff words, e.g. the readiness sentences, the four staff column headings, "Export CSV") | the **B449 pack of 346 words** (`Deliverables/2026-10-22_word-pack-hosted-f5b6f5a/`, strings.tsv 365 rows), card `mps-hosted-deploy-words-f5b6f5a-1022`, ruled a 2026-10-22 15:19 "Approve all as built" (C-48 :913-918), two days after the merges | main `35887699` deployed 2026-10-22 (#83 to #94), after the pack |
| Self-approval, rebate default, feedback limit | #95, #96, #97 (2026-10-22) | yes (55 words) | pack C-46, ruled 2026-10-22 22:47 | `e027ebd0` deployed 2026-10-23 (C-47), words checked "55/55 ruled forms" |
| V6 server store | #145 (2026-11-02, on the ruling "Land it and ticket the gaps", after a NO GO at the round cap) | 7 sentences pending at landing | 13 template-API errors approved later in the 31 staff strings (card `mpscalc-staff-words-31-deploy-1112`, ruled 2026-11-12 18:20; RELAYED from B's pack) | hosted 2026-11-12 (C-145) |
| Purchase projection on the Api | #174 (2026-11-10) | contract words unapproved at landing | not yet sent: comment 40935 clause 6 and C-110 | not deployed with those words approved |
| One-page rental proposal | #186, #189 (2026-11-12) | yes, customer words | card `mpscalc-hosted-deploy-words-1112`, ruled a 2026-11-12 17:00, BEFORE the deploy (C-145) | `0bb3ed12` on 2026-11-12 |
| Developer note | #215 (2026-11-18) | one developer sentence | listed to him after landing (card ruled 2026-11-18 11:22) | not deployed |

So: seven pull requests with new words on main and a pack sent after: #85 to #91 (pack B449). The engine halves of V4
(#133 to #140, #150, #155) carried no customer words and no pack.

### 2.4 C-116: which tickets does "every contract change until you approve the exact name" stop?

- **Stopped in terms:** MPSCALC-169 (C-68 and C-116: the name and the words first); MPSCALC-368 (C-110: "agent proposes the
  name for your approval"; the member `projection` is already on main since #174, so what is owed is his approval of that name
  and of the contract sentences, not a build).
- **Stopped if C-116 is read widely** (every NEW contract member needs its name approved before it is merged): 237, 236's
  accepted-event half, 273, 274, 275 (new members on the Won and Approve calls), the Api halves of 252 255 257 258 259 (not
  ticketed), 286 and 287 (a new Settings contract), 288 (`callerCan.reject`), 315 (a result field), 358 (the wire spelling:
  C-95 :2578 "the wire words are the product owner's"). If read widely, it also stops what #85, #150 and #174 did, which
  merged new members before their names were approved.
- **My reading:** C-116's sentence is about 169, because "your earlier ruling" is C-68, and C-68's own wording is "on that
  card" (the 169 follow-up card). Under that reading a lane may merge a new member and send its name in the pack, as #85, #150
  and #174 did. **Not settled by any ruling.** It decides whether lane 4 below may start (question 2).

### 2.5 What is NOT settled

1. Whether "ships" ever means the merge. (No ruling says so; practice says the deploy.)
2. Whether C-116 is about 169 alone or about every new contract member (2.4).
3. Whether a builder may draft words (wave 1 yes; today's kits no).
4. Whether unapproved customer words may sit on main while other fixes wait to deploy (2.2 point 4).
5. The product owner's marks on the 2026-11-12 words review page: I did not find them (see section 7, not re-verified).
6. The brand question Q-03 (D-14 c rules a setting per quote; the default line of 281 and 287 waits on it).

## 3. The build plan, lane by lane (task 2)

Plan: `1_Project_Definition/2026-10-20_v13.4.1_BUILD_PLAN.md` (12 lanes V0 to V11 plus group L; lanes :25-203; order :216-235)
and `2026-10-20_v13.4.1_GAP_ANALYSIS.md` (85 rows V-01 to V-85). Status read from the merged-PR list, the Jira lane labels
(99 keys carry the label mpscalc-b308 or a lane-v label, Done included; 162 MPSCALC keys are open) and main.

| Lane | Planned tickets | Built and landed (pull requests) | Partly built | Not started |
|---|---|---|---|---|
| V0 contract (tier 1) | T-V0-1..7 | 232, 234, 235 Done (#85); 209 | 233 (clone: the clash refusal owed), 236 (accepted event is recorded by nothing) | 237 (T-V0-7) |
| V1 frame (tier 2) | T-V1-1..8 | 238, 239, 240, 241, 242 Done (#88, #90, #91); autosave, toolbar, readiness panel | 314 (autosave pause choice), 297 (smoke leg) | 243 (wizard) |
| V2 Home | T-V2-1..4 | #89 and #91: Ready to Export tab, staff columns, CSV (T-V2-2 has no separate open key) | 244 (annual GP absent by data), 245 | 246 |
| V3 readiness (tier 1) | T-V3-1..5 | 247, 249, 250 Done (#87) | 248 (held checks), 251 (sign-in leg) | none |
| V4 engine (tier 1) | T-V4-1..12 | ENGINE halves only: 252, 253, 254, 255, 256, 257, 259 Done (#133 to #140, #155); Api quantityRule (#150); Api projection (#174) | 258 (engine half only), 358, 359 | Api, DTO, contract and web halves of groups, volume basis, fee, sites, tier, sell method (no ticket); 260 later by D-02; 261, 360, 315 |
| V5 editors (tier 2) | T-V5-1..8 | 262, 263, 266 and 151 Done (#86, #103) | none | 264 265 267 268 |
| V6 templates | T-V6-1..3 | 269 store (#145) | 269 open on a clause | 270 271 |
| V7 review | T-V7-1..6 | T-V7-6 self-approval (#95, 137 and 172) | none | 272 273 274 275 276 |
| V8 proposals | T-V8-1..5 | none | none | 277 278 279 280 281 |
| V9 help | T-V9-1..2 | the 11 hints (139, list W) only | none | 282 283 |
| V10 price book | T-V10-1..3 | T-V10-1 is MPSCALC-51 (existing); #84 merged 2026-10-19 | none | 284 285 |
| V11 controls | T-V11-1..3 | none | none | 286 287 |

## 4. The tickets (task 3)

Every ticket is **Backlog** in Jira (MEASURED, 57 of 57). Classes: B1 buildable now; B2 buildable after one Tuesday reading;
R records only; F in flight; W words nobody drafted; P unbuilt predecessor; N contract name owed; D ruling, marks, decision or
outside data. "On main" is MEASURED at the sha above unless marked RELAYED. Prototype texts (the reviewer's HTML) live in the
project's `Source_Documents`, which I did not read: their quotes are RELAYED from drafter B, except where the gap analysis
row (which I read) quotes the same words, marked "verified".

### 4.1 The 35 of the sweep (counts: B1 3, B2 4, R 2, W 12, P 8, N 2, D 4)

| Key | Lane | Asks | On main | Words (source) | Also needs | Class |
|---|---|---|---|---|---|---|
| 121 | feedback | Unreadable-file refusal should read true | Refusal built (#178); sentence on main is words.ts:20 REFUSED_TYPE | 1 sentence proposed on the 2026-11-12 review page ("Suggested"); marks not recorded | his mark before it ships | B1 |
| 129 | rental book | Three untrue sentences | All 3 approved sentences ARE on main (rental.ts); the old sentence is not | Approved 2026-10-14 | Jira text stale; records fix | R |
| 130 | printed books | Words per page differ from the mock | Style half built (#178); 6 rows differ | Rows 1,4,6,7,8,9 quoted on the review page, "which side is right" unmarked | his marks, row by row | D |
| 139 | hints | (i) hints on fields | 11 hints + button label ARE on main (infoHintWords.ts, InfoHint.tsx) | Approved: list W items 34-45 (C-36) | clause 4 (axe check, a dependency decision) is open, not words | R |
| 154 | phase 2 | Client fleet template spreadsheet | Not on main | Not drafted; K-17 named by the ticket is in no entry; the ticket quotes both "build it" and "let us not do it" | a ruling on which; phase 2 | W |
| 156 | credit box | Credit callout in proposals | Purchase half ON main (sections.ts:403-404, CreditCallout.tsx) | Purchase half approved (list W 29-30); rental half not drafted | rental credit field (C-114) and 261 | W |
| 161 | archive | Archive a quote | Not on main | No label, button or message drafted (C-115 ruled "Archive") | none other | W |
| 169 | contract field | Name the source set of lineMarkups | Not on main | No name, no words | C-68 and C-116: exact name first | N |
| 194 | feedback 401 | Tell the user typed text will be lost | First half live (C-37); second half not | "will be lost" sentence not drafted (C-118) | none other | W |
| 233 | clone | Refuse a clone reference that exists | -COPY on main (#85); the refusal is not | Refusal sentence not drafted (C-119 ruled "Refuse") | none other | W |
| 237 | V0-7 | Acceptance record on Won + Issued status | Not on main (QuoteEvents.cs: accepted is "recorded by nothing yet") | "Issued" is ruled (D-12 a); API description words are developer text (C-109 b) | Tuesday reading of when Approved becomes Issued; member names (C-116 reading) | B2 |
| 243 | V1-8 wizard | Guided wizard over the quote | Not on main (0 hits "wizard") | Step names are in the ticket; default mode and the step-1 gate sentence are not drafted | default-mode decision; touches Shell/QuoteScreen | W |
| 246 | V2-4 | Issued queue on Home | Not on main | Tab label can only be the ruled name "Issued" | 237 unbuilt | P |
| 264 | V5-4 group editor | Edit a group; Duplicate billable group | No group editor; the Api has no group fields (fleetQuantity 0 hits in Api) | Confirm sentence only in the prototype (relayed) | Api half of the V4 group fields unbuilt | P |
| 265 | V5-5 assistant | What fits each group; Add 1 per device | Not on main | Prototype heading and note (relayed); "our wording" not drafted | group fields on the Api | P |
| 267 | V5-7 projection table | Monthly / annual / contract table | Api member projection IS on main (#174, internal-only); web shows none | Labels in gap analysis V-55 (verified), 9 strings | none | B1 |
| 268 | V5-8 sites | Site allocation screen | No sites on the Api (0 hits); no screen | Prototype labels (relayed) | Api half of sites unbuilt | P |
| 270 | V6-2 library | Template library screen | Store + API on main (#145); no screen (no web templates client) | Some labels in prototype; Archive and Edit not; "Copy active group" needs a group | group fields on the Api | P |
| 271 | V6-3 add to quote | Template to one new group | No apply endpoint; no group on the Api | Prototype confirm sentences (relayed) | apply endpoint + group fields | P |
| 272 | V7-1 tiles | Staff summary tiles | Not on main | Tile labels in gap V-65 (verified) | rental has no per-year GP on the quote (315 open) | D |
| 273 | V7-2 checklist | 7 ticks before approve, ticks audited | Not on main | 7 sentences + heading + alert in the prototype (relayed), 9 strings | new contract members for audited ticks | B2 |
| 274 | V7-3 auth ref | Authorisation reference on approve | Not on main (0 hits) | Label from the ticket and prototype (relayed), 2 strings | new contract member on ApproveRequest | B2 |
| 275 | V7-4 acceptance | PO / reference and date on Won | Not on main | Prototype labels and alerts (relayed), 5 strings | after 237 (same lane) | B2 |
| 276 | V7-5 diff view | Version diff view + export | Endpoint on main (#85); web client has 0 diff calls | "Save revision", "Export revision history" only; diff labels not drafted | none other | W |
| 277 | V8-1 formats | Quick / Standard / Enterprise | Two formats ("Short-form proposal (PDF)", "Full proposal (PDF)"); Standard already has identity, governance, assumptions sections | Enterprise text and names in the prototype (relayed) | what Enterprise adds beyond Standard is undecided | D |
| 278 | V8-2 priced/unpriced | Option: unit and extended prices vs SKUs and quantities only | Not on main (fixed constants, settings.ts) | 2 labels, gap V-63 (verified) and the ticket | scope: which documents | B1 |
| 279 | V8-3 schedule | Fleet schedule by group, per-group rates, PO line | Not on main | Not drafted for ours | group fields on the Api; words | P |
| 280 | V8-4 sequence | Implementation sequence block | Standard ALREADY has LIFECYCLE_STEPS (sections.ts:102-106) and implementationPhases (:259); short form has 4 stages (concise.ts:108) | Four different wordings exist; which one is wanted is open | a decision, not a build | D |
| 281 | V8-5 entity line | Trading entity line from a setting | Not on main | Setting label not drafted; brand Q-03 open | 287 unbuilt | P |
| 282 | V9-1 help page | Seven topics rewritten | No help screen | Prototype text, several topics false for our product (plan); no rewrite | a drafting job first | W |
| 283 | V9-2 field help | Catalogue + FieldLabel | Not on main | 60 entries, none compared with our behaviour | a drafting job first | W |
| 286 | V11-1 thresholds | Governed settings, Review warnings | No Settings area in the Api | 3 labels in prototype; Review sentence not drafted; values ruled (D-10 a) | new contract + settings | W |
| 287 | V11-2 entity setting | Governed trading-entity setting | No Settings area | Labels not drafted | Q-03 brand; contract | W |
| 368 | V4 projection | Name and contract words | Member projection IS on main (#174) | Name and sentences await approval (C-110) | approval of the name as built | N |
| 402 | deploy words | Four changes to approved stop words | Approved pack (C-152) is on main | No replacement sentence drafted | back to the product owner first | W |

### 4.2 Twenty-two more open v13 lane keys found (counts: B2 3, R 3, F 1, W 2, P 1, N 4, D 8)

| Key | Lane | Asks | On main | Words | Also needs | Class |
|---|---|---|---|---|---|---|
| 236 | V0-6 | Audit events issued/accepted | Customer/term old-new values built (#85); accepted recorded by nothing | No words (event kinds) | closes with 237 | B2 |
| 244 | V2-1 | Staff GP columns | Built (#89): 3 of 4 columns for purchase, 1 of 4 rental | Words approved (list W) | annual GP absent by data (315) | D |
| 245 | V2-3 | Analytics CSV | Built (#89, #91); the ticket text asked for the Home figures | Approved | records: ticket text vs built | R |
| 248 | V3-2 | Readiness post-pass | Partly built (#87); held checks wait | Staff words in 346 pack | device count needs groups; thresholds need 286; coverage needs 285 | P |
| 251 | V3-5 | Zero-errors e2e | Built (#87), runs in CI (#178) | none | sign-in leg not built | D |
| 258 | V4-7 | Manual tier on purchase | Engine half merged (#134); Api, audit, web not | Reason words exist (PRICE_REASON_REQUIRED) | new contract members | N |
| 260 | V4-9 | Finance / lease | Builds nothing now (D-02 a) | none | a financier schedule | D |
| 261 | V4-12 | Rental credits | Not built; who approves ruled (C-63) | Review-issue words not drafted | none other | W |
| 269 | V6-1 | Template store | Landed (#145) | 7 sentences await the pack | clause 4 test needs 271 | R |
| 284 | V10-2 | Software billing column | Not built | Refusal words not drafted | monthly-SKU list is outside data | D |
| 285 | V10-3 | Care pack term | Not built | Not drafted | care terms from the book owner | D |
| 288 | rule | Own reject rule | Not built | New words | C-69: a new member and a follow-up card | N |
| 297 | V1 | Smoke e2e | Green only on an invented-data API; red on stub | none | not measurable in CI | D |
| 306 | V2 | Staff list overflow | Overflow 0 at 1440; Action button clause open | none | owner question B354-5 | D |
| 310 | V2 | Leak-layer seam test | Not built | none | a product decision on the seam | D |
| 314 | V1 | Autosave writes one event per pause | Not decided | none | Tuesday picks interval, gap or coalesce | B2 |
| 315 | V4 | Per-year GP on the result | Not built | none | number-affecting; new result field | N |
| 316 | V0 | Quote reference sentence | Kit B1741 drafted for the one string | Accepted (C-108, C-64) | in flight | F |
| 358 | V4 | Quantity rule: contract text + editor | Api quantityRule merged (#150) | Wire words are the product owner's | spelling and text | N |
| 359 | V4 | Note under a per-site entry | Engine merged (#155) | Note words not drafted (C-86) | none other | W |
| 360 | V4 | usageOnly rule | Not built | none (engine rule) | Tuesday must confirm the reading in writing | B2 |
| 369 | V0 | Web tests under load | #205 landed; every clause met on a reading | none | records only | R |

**All 57: B1 3, B2 7, R 5, F 1, W 14, P 9, N 6, D 12.**

### 4.3 Notes on the tickets that surprised me

- **280 and 277 (V8).** Main's Standard book is richer than the tickets assume. `sections.ts` already holds `LIFECYCLE_STEPS`
  (Assess, Prepare, Deploy, Operate, :102-106), `implementationPhases` (:259), `identityIntro` and `governanceRows` (:306,
  :315) and an assumptions and exclusions section (:345), and the document renders governance and assumptions sections
  (`ProposalDocument.tsx:472, :483`). Ticket 280 says "The full book has no implementation-sequence block" and 277 says the
  Enterprise book "adds site rollout, identity and print security, and governance and assumptions". Part of that is already in
  Standard. What Enterprise adds is a content decision, not a build.
- **368.** Built (#174: `Projection` with six measures, internal-only, `Dtos.cs:932-946`). Drafter B listed it "NOT DRAFTED (field
  name owed)". The name `projection` exists; the pack item is its approval (C-110).
- **129, 139.** Main has the three approved rental sentences (3 of 3 found in `rental.ts`; the old "total of the monthly charges"
  sentence 0 found; control: the approved ones are found) and the 11 hints. Records fixes, as B said.
- **245, 269, 369.** Built or met on a reading; only comments or a pack are owed.
- **233, 236.** #85 landed the clone's own reference and the old/new audit values; what is left is a refusal sentence (C-119) and
  the accepted event (237).
- **267.** The Api's six measures are `Pages, ClickCost, ManagedServiceCost, ClickRevenue, ServiceRevenue,
  RecurringGrossProfit` (`Dtos.cs:939-946`); the prototype table has nine rows, the two "total recurring cost / revenue" rows
  are sums the Api does not send, so the table would show six rows and no browser arithmetic. The stub (`web/src/api/stub/`)
  sends no `projection` (0 hits), so the lane adds it.

## 5. Lanes (task 4)

Disjoint by file, in dependency order, six at most. Sizes S <= 1 seat-day, M 2-4, L 5+ (plan :18-20). Gate tier is my guess
against `fleet/specs/model-routing.md:108-110` (G1: security surfaces, anything deploying, anything handed to a client tester;
G2: tests-only, docs, CI, tooling); Tuesday rules it. "Words" counts strings the lane would introduce.

### First wave, buildable now (3 lanes, 3 keys)

**Lane 1: MPSCALC-267 (V5-7 projection table).** Size S. Files (MEASURED at main): new
`web/src/screens/bom/ProjectionTable.tsx` and test; `web/src/screens/bom/PurchaseResultView.tsx` (mounts it, 0 hits for
"projection" today); `web/src/api/stub/purchaseQuotes.ts` (stub sends no `projection`). Jira tier 2; gate guess **G1** (it shows
internal money figures, a leak surface; the Api already nulls `Projection` without internal-metrics, so a leak row is the proof).
Words **9**, all source text: six row labels (Pages, Click cost, Managed service cost, Click revenue, Service revenue,
Recurring GP) and three column heads (monthly, annual (x12), contract (xterm)), from gap analysis row V-55
(`GAP_ANALYSIS.md:178`, verified) and the Api member names (`Dtos.cs:939-946`); the prototype lines HTML:173-189 are RELAYED. No
D card gates it. Predecessors: 256 (Done), 368 (merged #174). What would STOP it: the product owner renames `projection` on
the C-110 card (a one-line rework); a need for a sum the Api does not send (no browser arithmetic); a rental quote (the
projection is purchase only).

**Lane 2: MPSCALC-278 (V8-2 priced or unpriced).** Size M. Files: `web/src/screens/ProposalPage.tsx`, `web/src/proposal/**`
(`ProposalDocument.tsx`, `OnePager.tsx`, `RentalDocument.tsx`, `model.ts`, `settings.ts`, `template/*`) and their tests. Jira
tier 2; gate guess **G1** (a customer document; the acceptance is "no price appears anywhere ... (test over the printed text)").
Words **2**: "Show customer unit and extended prices" and "Show SKUs and quantities only" (gap row V-63, `GAP_ANALYSIS.md:196`,
verified; the ticket's own pair is "unit and extended prices" / "SKUs and quantities only"); the existing approved
`PRICE_ON_REQUEST` ('Price on request', `sections.ts:406`) may be reused. No predecessor. What would STOP it: "the choice is
recorded" needing a new contract member (then it joins lane 4's reading, question 2); the builder cannot say which of the
three documents (Standard, short form, rental book) takes the option without a scope answer; a price left in a total.

**Lane 3: MPSCALC-121 (feedback form, unreadable file).** Size XS. Files: `web/src/feedback/words.ts`,
`web/src/feedback/FeedbackDialog.tsx`, `FeedbackDialog.unreadable.test.tsx`. Jira tier 2; gate **G2**. Words **1** (16 words):
"This file could not be read. Check that you can open it, then attach it again." (the "Suggested" line of the 2026-11-12 words
review page, `tuesday/briefs/2026-11-12_mps-words-review-page.md:90`; the page also offers "Alternative", "Keep today's
sentence" and "Other", and its mark line :93 is unticked in the copy I read). What would STOP it: his mark choosing another
option. It is cheaper to read his mark than to build; the lane exists only because the rule lets it.

### Conditional wave (3 more lanes; each needs one Tuesday reading and no product-owner word first)

**Lane 4: V0 and V7 contract-plus-screen lane: MPSCALC-237, 236 (accepted event), 273, 274, 275.** Size L, tier 1; gate **G1**.
Files: `src/MpsCalc.Api/Contracts/Dtos.cs`, `docs/api/openapi.json`, `docs/API.md`, `web/src/api/generated/**`,
`src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, `QuoteStore.cs`, `Mapping.cs`, `QuoteEvents.cs`, `PriceAudit.cs`, `web/src/api/client.ts`,
`web/src/api/stub/stubApi.ts`, `web/src/screens/Lifecycle.tsx`, new `web/src/screens/review/**` (does not exist today). Words
about **17** screen strings, RELAYED from the prototype: 273 heading "Pre-issue checklist", the seven sentences and the alert
"Complete every review checklist item before approving."; 274 the authorisation-reference label and one note label; 275
"Customer acceptance reference", "Acceptance date", "Record customer acceptance" and two alerts; plus the ruled name "Issued"
(D-12 a). The seven sentences are what D-11 a adopts (the checklist words are in the reviewer's file); sentence 3 names Synnex and HP and sentence 6
names "financing terms" while D-02 a defers finance: a builder uses them unchanged and the pack decides. Developer text in
openapi and API.md is out of his review (C-109 b). The `accepted` event description is already in the 346 pack (register item
22, relayed). **Needs, before it starts:** (a) Tuesday's reading of 237's own line "Reading to confirm with the coordinator:
Approved moves to Issued when the "issued" event of T-V0-6 is recorded" (there is no separate issued kind by the 2026-10-20
ruling, comment 39742); (b) the C-116 reading (2.4): if wide, the names go to a card first. 246 (Issued queue, Dashboard.tsx,
QuoteList.tsx, QuoteFigures.cs) follows this lane. What would STOP it: the wide C-116 reading; sentence 3 or 6 struck in the pack
(a one-string rework); a collision with the in-flight kit B1741 on `QuoteEndpoints.cs:1436` (one string, different hunk).

**Lane 5: MPSCALC-314 (autosave writes an event per pause).** Size XS; gate **G2**; no words. Files:
`web/src/screens/quote/autosave.ts` (`AUTOSAVE_QUIET_MS = 2000` at :9 per the ticket) and its test (web-only choice). **Needs:**
Tuesday picks interval, minimum gap or server coalescing (the ticket: "the choice is the coordinator's decision, not a card");
server coalescing would touch the draft save and leave this lane. STOP: the pick is server-side.

**Lane 6: MPSCALC-360 (usageOnly rule).** Size S-M; tier 1; gate **G1** (number-affecting); no words. Files:
`src/MpsCalc.Engine/Input/PurchaseInput.cs`, `Calculation/PurchaseCalculator.cs`, `Reconciliation/PurchaseRecomputation.cs`,
`docs/ENGINE.md` (register rows), `tests/MpsCalc.Engine.Tests/ComponentQuantityRuleTests.cs`. **Needs:** Tuesday confirms the
reading "in writing" (the ticket's acceptance). STOP: the Api mapping must name a fourth rule (that is a contract member and
joins lane 4's files and reading).

### Not in the first wave, and why (counts by class from section 4)

- **Needs words nobody drafted, 14 keys:** 154 156 161 194 233 243 261 276 282 283 286 287 359 402. A drafting seat (no
  code) could write these now; that, not a builder, is what moves them.
- **Unbuilt predecessor, 9:** 246 (237); 264 265 268 270 271 279 (the V4 Api half); 281 (287); 248 (groups, 285, 286).
- **Contract name owed, 6:** 169 368 258 288 315 358.
- **Ruling, marks, decision or outside data, 12:** 130 244 251 260 272 277 280 284 285 297 306 310.
- **Records only, 5:** 129 139 245 269 369. **In flight:** 316.

## 6. Can two lanes run at once?

- **By file: yes.** Lanes 1, 2, 3, 5 and 6 share no file (lane 1: `web/src/screens/bom/`, one stub file; lane 2: `ProposalPage.tsx` and
  `proposal/`; lane 3: `web/src/feedback/`; lane 5: `screens/quote/autosave.ts`; lane 6: engine and tests). **Lane 4 is the only contract
  lane and is serial**: the plan's own rule (:23, :235) is that `Dtos.cs`, `openapi.json` and the generated client are edited by one
  lane, and "after any V0 contract merge, every web lane rebases on the regenerated client before merging". Lanes 1 and 4 both
  touch `web/src/api/stub/` (different files); Tuesday should order them.
- **By machine, from two kits I read (RELAYED, not re-run):** B1594 (web, 2026-11-15) and B1564 (Api, 2026-11-15). Each lane gets
  its own port block (B1594: 9960-9969, listener on 9961; B1564: 9800-9809, none started); each checks "a live `Datasec/MPS-*` code
  pane whose kit GRANTS a path of yours" and refuses if one exists; each takes the heavy checks one slot at a time
  (`.tools/.heavy-lock-1`, `-2`: so at most two heavy runs at once on the machine), takes git fetches under `.tools/.git-lock`
  (atomic `mkdir`), and refuses to start with load1 at 24 or more. So **two lanes at once, yes; a third queues its heavy checks.**
- **A shared counts file: none found.** The kits compare the test count to a baseline the seat measures itself ("file count equal
  to the baseline plus 1", B1594 line 41), so a later lane must re-measure after an earlier one lands. The repo has shared
  generated files (contract copies; `contract.sync.test.ts` compares them), which is the contract-lane serialisation above.
  `CLAUDE.md` of the project is stale (last status 2026-10-01) and says nothing on locks.
- **Landing:** seats push a branch only; Tuesday opens the PR and merges once CodeQL is green (project `CLAUDE.md:50-51` names
  Friday; the kit B1741:`FACT 1` names Tuesday), squash with the head pinned (`--match-head-commit`).

## 7. Drafter B (`2026-11-19_B1742_decision_pack/B_REPORT.md` and `MPS_words_pack_v13-4-1.md`), checked both ways

**Right (MEASURED by me):**
1. No words pack exists for lanes V2 to V11 and the standing process is per-lane packs after the build: confirmed (C-45 :660;
   Tuesday's 2026-10-24 pack line 37, "Words arrive per lane, not as one rulings list now.", found at
   `0_Brain/projects_index/2026-10-24_mps-words-for-<reviewer>-review.md:37`).
2. 129's three sentences and 139's hints are approved and on main (above); the ticket texts are stale. Right.
3. No V5 to V9 screen exists: `web/src/screens/review`, `help`, `templates`, `controls` do not exist; 0 hits for
   `GroupEditor|ConfigAssistant`; `src/MpsCalc.Api/Settings` does not exist (controls: `ProposalPage.tsx` holds "Short-form
   proposal"; `Lifecycle.tsx` holds "Review &amp; approval").
4. The prototype texts it quotes for 267 (V-55), 278 (V-63), the 277 format names (V-70), 272's tile list (V-65), 274's two labels
   (V-67), 243's modes, steps and gate (V-04) and 265's heading (V-47) match the gap analysis rows I read (verified). The
   264 confirm sentence, the 275 labels, the seven checklist sentences and the help topics are in no file I may read (RELAYED).
5. 288 and 110 are not open questions (C-69, C-104). Not re-read by me beyond C-69's existence in the ticket comment 40127.

**Wrong or short:**
1. **"31 of 35 have no owed words drafted" is true but is not "not buildable".** For 267 and 278 the labels are quoted in the gap
   analysis and the ticket; under C-45 the words follow the build. B's verdict "SOURCE: not drafted for our product" blurs the
   two. (A difference of standard, not of fact; section 2.2 point 5.)
2. **B did not find the unbuilt Api half of the V4 groups,** so it left 264 265 268 270 271 279 as word questions. They are blocked
   before words matter.
3. **B did not read main's Standard book** for 277 and 280. It calls the Standard reuse of the four-step wording "the open word
   question"; main already prints a different four-step strip and an implementation table (4.3).
4. **368** is listed "NOT DRAFTED (field name owed)"; the member is on main as `projection` since #174 and what is owed is his
   approval of that name (C-110).
5. **Not verified by me:** "no marks recorded" on the 2026-11-12 review page (I read that the mark line is unticked in the
   copy of the page; the decision store may hold a later reply); B's note that `CLARIFICATIONS.md:1708` may be stale (I
   confirmed only that C-145 and C-166 record the 2026-11-12 and 2026-11-16 deploys).

## 8. Questions only Tuesday or the product owner can answer (queued, one at a time)

1. May a builder draft new words in a lane (wave-1 practice, a records seat collects them, one pack) or only use words already
   on record (today's kits)? It moves 14 keys.
2. Is C-116 about 169 only, or about every new contract member? It moves lane 4 (5 keys), 258, 288, 315, 358.
3. Will a name card for the V4 Api-half members be posted? It is the unlock for 264 265 268 270 271 279.
4. Lane 4's one reading (237: when Approved becomes Issued).

## 9. FOUND / TESTED (and NOT TESTED) / HOW

**FOUND.** 57 keys judged: B1 3, B2 7, R 5, F 1, W 14, P 9, N 6, D 12. First wave 3 keys in 3 lanes (267, 278, 121); conditional 7 keys in 3 lanes (237 236 273 274
275; 314; 360). The rule: build and merge before the words, deploy after the pack and his card (C-45 :660); "ships" undefined.
Seven pull requests landed with unapproved words and a pack followed (#85 to #91, pack B449 of 346 words ruled 2026-10-22).
The V4 Api half is unbuilt and unticketed (blocks 6 of the 35). Standard already has a lifecycle strip, governance and
assumptions (277, 280).

**TESTED (MEASURED, each with a control).** Main sha twice (17:15 tarball, 17:26 ref): equal. Open PRs 0 (control: PR 99999 answers
404). File and symbol absences at main: `FleetQuantity` in the Api 0 (control: 1 file set in the Engine input); `diff` and `templates`
in `client.ts` 0 (control: `duplicate` 2); `Enterprise` 0 and `GroupEditor|ConfigAssistant` 0 (controls: `Short-form proposal` 2 in
ProposalPage); `authorisation reference` 0 (control: the Review and approval heading found); directories `screens/review`, `help`,
`templates`, `controls` and `Api/Settings` absent (control: `screens/quote` lists 17 files). The three approved rental sentences
3 of 3 on main (control: the old sentence 0). Jira: 162 open keys and 99 keys with the b308 or a lane-v label, paged by `nextPageToken` (neither
count equals the page size 100); 57 tickets read with all comments. CLARIFICATIONS lines quoted were printed by line number.

**NOT TESTED / NOT READ.** No build, no test run, no server, no app host, no `az`, no mail. The reviewer's prototype HTML and
every `Source_Documents` file (excluded by the rules): the seven checklist sentences, the help topics and 60 field-help entries
are RELAYED. `.local`, any price book. The 2026-11-11 decision register PDF. PR diffs (file lists only, by title). Whether a live
MPS seat holds any of the paths (no tmux read). The lock scripts themselves (two kits read; the claims in section 6 are theirs).
Merge times are by day from the merged list and by the landing comments. `board_count.sh` was not used: its Jira form takes the
token on its command line, which the rules forbid; the counts above come from in-process paged reads with the controls named.
The words of 273/274/275 beyond what B and the gap rows quote. Other clients and the other Datasec projects were not read or named.

**HOW.** `gh api -X GET` under `4_Credentials/.gh-config` (branch ref, paginated merged-PR list, tarball into scratch);
Jira GET through a scratch script reading `4_Credentials/.env` by name (`fleet/state/s293/d1744/tools/jira_fetch.py`,
`show.py`, `brief.py`); `grep` and `sed` on the extracted tree; `decision_queue.sh show` and `list` only. Scratch:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1744/`. This file was assembled by `tools/build_doc.py`, checked
ASCII, written beside the target and moved with `os.replace`.
