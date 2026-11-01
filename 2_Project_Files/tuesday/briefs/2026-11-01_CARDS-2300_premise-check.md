# CARDS-2300 2026-11-01: premise check of the sweep's product-owner questions (drafter C8, read-only)

Measured 22:55 to 23:25 AEDT. Posts nothing. Tuesday reads this and posts.

Instruments used (each is a read): `decision_queue.sh prior` and `show <exact id>` (no `list`, no `add`); `/usr/bin/grep -n -i` over the two CLARIFICATIONS files (MPS local file, HPSM-POC records repo file read through `gh api -X GET` at records main `97cd47f4`); Jira per-key GETs and one `project = MPSCALC AND ( key in (...) )` search through a urllib reader that reads each project's `.env` in-process (no token printed); `gh api -X GET` contents reads at code main (HPSM-POC `d8981b0e`, MPS `3496da33`) under each project's own `GH_CONFIG_DIR`. Controls: MPS `pulls/99999` returned 404; `git/trees` listings were 748 entries (MPS) and 1719 (HPSM-POC) and the files named were found in them; every grep zero below names the positive control that fired beside it.

## Table

| Item | Verdict | Instrument and control |
|---|---|---|
| Q2 MPS roadmap features with new staff-facing words (MPSCALC-237, -246, -267, -272, -273, -274, -275, -276, -278, -281, -286, -287) | **ALREADY RULED.** The product owner chose option a, "Accept all 15 recommendations (recommended)", on 2026-10-20 (store time 10:09:42, panel message 10:09:20), whose detail reads: "Lanes start in waves as soon as you tap. Every new customer-facing word still comes to you as a word pack before it ships, and nothing is deployed without your card." C-45 records it and says every new "customer-facing or screen word" comes as a word pack before it ships. C-79 (2026-11-01, "Done means merged to main, the same as Composer") covers the merge. So build and merge now with words before any deploy is the standing order. NOT covered: MPSCALC-295, which the 2026-10-24 ruling (C-58) holds at "leave the words as they are" (see Surprises). | `decision_queue.sh show mpscalc-v13-gap-15-decisions-1020` (status ruled, choice a, delivered to C-44 and C-45). `grep -n -i 'words gate\|before any deploy\|word pack'` over MPS CLARIFICATIONS fired at lines 569, 660, 688. Jira search for the 13 keys returned 13 rows. All 12 Q2 keys are Backlog and carry a `plan-b308-*` label (12 of 12). Control: MPSCALC-295 returned in the same search with a different label (`plan-b340-b324-5`). `prior` for the proposed id printed 99 matches, of which the only ones on the subject are the cards above and the earlier "approve their wording and put them on the hosted site" cards (2026-10-11, ruled a). |
| Q4 HPSMPOC-405 shell safe area for the Feedback pill | **NOT NEEDED.** A layout defect with no new words and no money. The pill is the product owner's own design (orange, bottom right, 2026-10-03) and a safe area leaves the pill alone and only reserves room. The gate's own recommended fix shape is the safe area. No lane needs his word. The coordinator can build it. | Code read at main: the pill rule is unchanged since 2026-10-03 (`FeedbackPill.module.css` last commit `c2dd4037`) and already carries a footer room rule, `AppShell.tsx` last commit `9659148c` (2026-10-29). The overlap itself was not re-measured (needs a browser, relayed from the ticket). `prior` printed 1 match, a NexusAI card sharing only the word "shell". Positive control for the file reads: the CSS read printed the `.pill` rule. |
| Q5 HPSMPOC-322 B477-7 (reader order of the grouped summary) | **NOT NEEDED now.** B477-5 and B477-6 are real and still on main, so their lane stands. B477-7 is a Note that the ticket says follows the brief's own design choice, and a test already pins that order. Nothing is waiting on it: leaving it IS "kept". Raise it with the next customer-facing words card. The sweep's "branch b467 only" is stale: the code merged (records C-entry for PR #186) and sits on main. A builder is live on B477-5 and -6 only (relayed in the task, not checked). | `Providers.cs` at main: `SharedActions.Partition` and `GroupSizes` present (grep for `SharedActions\|GroupSizes\|group` printed 12 hits), titles joined with "; " at the shared-action sentence (B477-6 premise holds), group sizes global (B477-5 holds). `Hpsmpoc187GroupedSummaryTests.cs` lines 77 to 86 pin group-then-alone order (B477-7 is pinned). `prior` printed 6 matches, none on grouped order (the findings-list order card of 2026-09-26 is about the list sort, not the summary). HPSM-POC CLARIFICATIONS grep for `HPSMPOC-322` hit once (line 2609, the merge record), for `B477` zero hits as a case-insensitive word with control `HPSMPOC-322` firing. |
| Q7 MPSCALC-258 manual tier: permission, reason, audit | **ALREADY RULED (in substance).** 2026-10-20, option a of the 15-point card, row D-03: "keep per pool, add a quote-level manual override on purchase too". 2026-10-10 18:01, option a, "Who may edit prices, margins and manual items": per-quote overrides need a Seller with the pricing-analyst permission, every change audited, "a reason is required". Which ticket owns the Api and web half is the coordinator's records call, not his. The sweep's recommended answer ("the Approver role") contradicts the 2026-10-10 ruling. One reading to flag: the 2026-10-10 ruling says "price overrides", and a tier override is read as one. | `decision_queue.sh show mpscalc-price-edit-permissions-1010` (ruled a, delivered). C-45 row D-03 read at lines 671 and 680 area. Code at main: `PricingPolicy.MaySetQuotePrices` is Seller AND internal-metrics. The Api carries no purchase tier member (`Dtos.cs` has `TierOverride` for rental only, grep printed 1 hit; control `Mapping.cs` tier hits fired). Rental tier changes are audited but "a reason is not required for these this round" (`PriceAudit.cs` line 103). The live-pane facts are not used. |
| Q8 MPSCALC-300 quantity audit for a section with several device lines | **NOT NEEDED.** The ticket says in its own words that it "waits on a coordinator decision, not on a card the product owner has not ruled". The flag is advisory, blocks nothing and changes no price. The coordinator can choose the sweep's reading. | Ticket read (status Backlog, 0 comments). Code at main: `quantityAuditModel.ts` `purchaseAudit` still sums every non-credit, non-optional device line into one count (lines 97 to 110 read, premise holds). `prior` printed 73 matches that share only the word "mpscalc" or "audit". None is on the subject. CLARIFICATIONS grep for `MPSCALC-300`: 0 hits, with the positive control `MPSCALC-258` printing 9 hits in the same file. |
| Q9 MPSCALC-284 software billing default | **NOT NEEDED.** The default of one-off equals today's behaviour (the ticket's own acceptance says a one-off line is unchanged), so building it with that default moves no figure. The real blocker is a list the client must supply (which software is billed monthly), which is a data request and not a decision. The importer has no billing field today, so the feature is unbuilt. | Code at main: 22 importer source files scanned, `billing` printed 0 hits, positive control `software` printed 72 hits. Ticket read (Backlog, 0 comments, "Reading to confirm: until that list exists the column defaults to one-off", "no D card gates this ticket"). CLARIFICATIONS grep for `MPSCALC-284`: 0 hits, control `MPSCALC-258` 9. `prior` 71 matches sharing only project words. |
| Q11 HPSMPOC-406 | **CARD** for item 1 (the four added phrases). Items 2 to 5 of the ticket are layout and hand-off Notes with no words, so they stay with the coordinator. This card also decides whether HPSMPOC-372 can close (see the six keys). Card id `hpsmpoc-partner-home-words-1102`. | Code at main: `PartnerDashboard.tsx` still holds "Open your customers" (line 141), "Customer pipeline table" (line 143), its caption (line 145) and the readiness sentence (line 231); `grep -c -F` printed 1 for each. HPSM-POC CLARIFICATIONS grep for the three phrases: 0 hits each (positive control: the same file printed 264 `### C-` headings and hits for the key HPSMPOC-406 at lines 4832 and 4833). `prior` for the proposed id printed 47 matches, none on this subject. |
| Q11 HPSMPOC-409 | **NOT NEEDED.** The sweep and ticket treat the fix as new words, but the table already has a hidden caption "One customer, sample model, years 1 to 3". The scrolling wrapper can take that same text as its name, so no new word is added. The second item (the page-landmark rule) is a no-words Note. The coordinator can brief it. | `OneCustomerEstimate.tsx` at main: wrapper at line 70 is still `data-scroll-x ... overflow-x-auto` with no name (premise holds), caption at line 72 (positive control for the file read). `prior` for a proposed id printed 0 matches. |
| Q11 HPSMPOC-410 | **ALREADY RULED.** 2026-10-29 20:41, the product owner chose "Keep the sample names (recommended)" on the question whether Demo should see sample customer names on the Service offers pages. The recommendation read that the names are labelled sample data and the alias rule covers the customer frame only, and the question's own text notes that Home already showed Demo one sample name. The 2026-10-11 rulings aliased the frame, headings and the report PDF. The customer-page profile row is not named by either ruling and is covered by reading (flagged). | `decision_queue.sh show hpsmpoc-demo-sample-names-services-1029` (ruled a). C-225 in the records repo records it. `show` of the two 2026-10-11 cards confirmed their text. Timestamp discrepancy: C-225 says 19:51:32, the store says ruled 20:41:18 (see Surprises). |
| Q11 HPSMPOC-420 and -421 (customer page header question count) | **CARD**, one card, because one choice (which count the header shows) decides both. Card id `hpsmpoc-frame-chip-count-1102`. | Code at main: `CustomerShell.tsx` lines 81 to 88 count every applicable question for a customer held in the browser and read a stored figure for a saved one. `AssessmentScreen.tsx` line 45 and 99 count scored applicable questions only. The "0 of 0" reading on the review site is the deployment report's, relayed, not re-measured. `prior` for the proposed id printed 4 matches, none on this subject. CLARIFICATIONS grep for both keys found only landing records (lines 4888 and 4922), no ruling. |
| Q11 HPSMPOC-424 (one old entry empties the saved register) | **NOT NEEDED now.** The ticket says the loss is confined to one browser tab's session storage and to entries an earlier build wrote. No lane waits and a hold is the default. It stays open. | Ticket read. `prior` printed 1 unrelated match (a secrets register). CLARIFICATIONS lines 4967 to 5016 read: "No reachability or choice is ruled". |
| Q11 HPSMPOC-425 (invisible-only evidence for Evidence submitted) | **NOT NEEDED now.** Same reason: three rows pin the unchanged behaviour, nothing waits, and leaving it IS option a. It stays open. | Ticket read, same CLARIFICATIONS lines. |
| HPSMPOC-399 | **NOT NEEDED as a card for the ticket.** Four items: the sideways-scroll test was fixed and merged (confirmed in the ticket's own comment). The last-row menu clip looks ALREADY FIXED on main (see Surprises). The 390 px stress overflow is a no-words defect for the coordinator. The focus ring and corner question is the product owner's and is drafted as the card `hpsmpoc-menu-focus-ring-1102` below, which also decides HPSMPOC-368. | `CustomerManagement.tsx` at main: menu list is `fixed` and flips upward when there is no room (lines 88 to 96), file last committed by the Customers and Engagements restyle (`41922a36`, 2026-10-30 09:40Z), after the ticket's reading point. Not browser-measured. Ring rule `.sidebar-ring:focus-visible { outline-offset: -3px }` in `globals.css` at main, last touched before the gate. `prior` printed 0 matches for the ring subject. |
| HPSMPOC-407 | **NOT NEEDED.** Test-only Notes, no product byte, no words. Building or declining them is the coordinator's. | Ticket read; its own text says "Each is a Note, optional, and test-only". |
| HPSMPOC-408 item 2 (limits' sentences and owner cap) | **NOT NEEDED.** Words, but the gate says it needs scripting or content that does not exist to reach, so no user can meet it. It stays open and costs nothing. | Ticket read (the gate "applied the Minor grade because both instances need DOM scripting or content that does not exist"). |
| HPSMPOC-423 (four code points that draw a box) | **NOT NEEDED.** Leaving them as accepted is the default, a control row already pins it, and the gate itself says the range "may reasonably stay non-blank". Widening needs his word, so no word is needed to leave it. | Ticket and C-entry lines 5006 to 5008 read ("only on his word"). |
| B1055-1 five unseen strings | **NOT NEEDED.** It is a review walk with the right sample data (an action), not a choice. The strings were put to him on the earlier wording list and are "accepted as built" with no veto recorded. | Records BACKLOG B1055-1 and CLARIFICATIONS line 5046 read. Both files fetched by `gh api -X GET`. |
| B1055-6 gate note list (the wake retry trade-offs) | **NOT NEEDED now.** Figures for a future decision about deploying that change. It belongs on that deploy card (approval-class, not mine). | BACKLOG B1055-6 read: "makes no ruling". |
| Records key 357 | **NOT NEEDED.** It waits on a measurement of the customer page at 360 px on the review site, which is a read of a hosted host and is fenced here. No decision is missing. | Ticket and its newest comment (id 40555, 22:57) read. |
| Records key 368 | **CARD** (the focus ring card decides it). | Ticket read: the records comment holds it for the ring and radius questions. |
| Records key 370 | **NOT NEEDED.** Its remaining question (keep or drop the top-bar customer picker) is the open gather ticket HPSMPOC-391, which the ticket text says needs the customer reviewer's input too. Nothing to ask the product owner alone. | HPSMPOC-370 and -391 read (comment 40562). |
| Records key 372 | **CARD** (the Partner Home words card decides it). | Comment 40564 read. |
| Records key 383 | **CARD** (the menu label card decides it). | Comment 40575 read. Label and Home tile checked in code: menu entry reads "Delivery phases" (`GlobalNav.tsx` line 50), Home tile still reads "Service offers" (`PartnerDashboard.tsx`, grep printed 1). Search for "Delivery phases" in the HPSM-POC CLARIFICATIONS file: 0 hits (weak: the second probe string "Service growth" also printed 0, so that file does not echo the design's menu text and the zero is only a hint). The decisive check is the card store, where `prior` printed 7 matches and none is on this subject. |
| Records key 401 | **NOT NEEDED.** Eight measured cells sit 4.5 px right of the reference inside a scroll region and the page is never wider. Recording that as accepted is a no-words layout call for the coordinator. | Ticket and comment 40581 read. |

Counts by table row (24 rows): CARD 5 rows (HPSMPOC-406, -420 and -421, 368, 372, 383), which need **4 cards** because 368 shares the focus ring card (with the ring part of 399), 372 shares the Partner Home words card and 383 shares the menu label card. ALREADY RULED 3 (Q2, Q7, HPSMPOC-410). NOT NEEDED 16 (Q4, Q5, Q8, Q9, 409, 424, 425, 399, 407, 408, 423, B1055-1, B1055-6, 357, 370, 401). CANNOT TELL 0. No card is drafted for MPS: all four MPS questions in scope (Q2, Q7, Q8, Q9) are ruled or the coordinator's.

## Dependence on the live records seat (read only)

The records seat for the design group had already posted a comment on each of the six keys by 22:58 (ids 40555 for 357, 40560 for 368, 40562 for 370, 40564 for 372, 40575 for 383, 40581 for 401), each saying it moves nothing. I read those from Jira. None of the four cards depends on that seat's result. If cards 1, 2 or 4 are ruled, a LATER records pass would move the matching keys. Whether its records branch has landed is UNMEASURED.

## Surprises

1. **MPSCALC-295 is inside the sweep's own lane M2 but the product owner ruled "leave the words as they are" on 2026-10-24 (C-58).** Q2 correctly leaves it out, but lane M2 bundles it with 317. A builder started on M2 would change a sentence he said to leave.
2. **Q7's recommended answer contradicts a ruling.** "Approver role" against the 2026-10-10 ruling's pricing-analyst permission.
3. **HPSMPOC-399's menu clip appears already fixed** by the 2026-10-30 Customers restyle, yet the records comment of 22:03 tonight says the clause is "neither met nor recorded as declined". The comment may be stale. Not browser-measured.
4. **Timestamp mismatch:** C-225 records the product owner's choice at 19:51:32 AEDT on 2026-10-29, while the decision store says ruled 20:41:18. The store time is a write time, so C-225 is probably the better time. Not resolved.
5. **Q2's wording:** the sweep says "staff-facing words". The 2026-10-20 ruling says "customer-facing word" and the C-45 entry widens it to "customer-facing or screen word". Screen words are covered.

## Cards (decision_queue.sh add --json shape)

Each object below was parsed as JSON by a program (see the last line of this section). No card contains a semicolon, a path, a seat name or a build number. `default_action` is nothing built in every case.

### Card 1 of 4: Partner Home words (HPSMPOC-406 item 1, also decides HPSMPOC-372)

```json
{
  "id": "hpsmpoc-partner-home-words-1102",
  "client_project": "Datasec/HPSM-POC",
  "title": "HPSM-POC: approve four new phrases on the partner Home page, or reword them?",
  "bluf": "The new partner Home page is built and merged, but four of its phrases have no approved source. They are the link 'Open your customers' shown when a partner has no customers yet, the screen-reader name 'Customer pipeline table', the table's hidden caption 'Customers with the stage and score of their latest assessment', and the sentence under Practice readiness 'Self-assessment, not certification. The four readiness bands come from the review guide.' The testers noted that no review guide appears in the app, so that last sentence may point at something a user cannot find. I checked the current code and all four are still there, and I checked the earlier rulings and none covers them. Nothing is on the demo. I recommend keeping the first three and trimming the last sentence.",
  "options": [
    {"key": "a", "label": "Approve all four as written", "detail": "The Home page keeps these words exactly. The held Home page ticket can then close. A user with no review guide still reads a sentence that mentions one."},
    {"key": "b", "label": "Approve three and trim the last sentence", "detail": "The sentence becomes just 'Self-assessment, not certification.' A builder makes that one change and it is tested before the demo. Add a note if you want different words."},
    {"key": "c", "label": "Hold all four", "detail": "Nothing changes. The words stay as built and unapproved, and the demo stays held for them."}
  ],
  "recommended": "b",
  "default_action": "Nothing is built. The words stay as built and unapproved, the Home page ticket stays open, and the demo stays held."
}
```

### Card 2 of 4: menu label (HPSMPOC-383 and HPSMPOC-412, also decides the Service offers pages' Done)

```json
{
  "id": "hpsmpoc-services-menu-label-1102",
  "client_project": "Datasec/HPSM-POC",
  "title": "HPSM-POC: is 'Delivery phases' the right name for the old Service offers page?",
  "bluf": "When the new left menu was built, the Service offers page was renamed 'Delivery phases' in the menu, its page title and its breadcrumbs, and it sits under a menu group called 'Service growth'. No ticket or ruling names that label, so you have never approved it. The Home page tile still says 'Service offers' and one Home sentence still says 'service offers', so a user sees two names for one page. I checked the current code for both names and checked the earlier rulings, and found no ruling. I recommend keeping 'Delivery phases' and changing the tile and sentence to match, because that is one name everywhere with the least rework.",
  "options": [
    {"key": "a", "label": "Keep 'Delivery phases' and match the Home tile and sentence", "detail": "The Home tile and the one sentence change to the new name. A builder makes the change and it is tested."},
    {"key": "b", "label": "Use a different name", "detail": "Reply with the name. A builder changes the menu, page title, breadcrumbs, tile and sentence to it, and it is tested."},
    {"key": "c", "label": "Go back to 'Service offers' everywhere", "detail": "The menu, page title and breadcrumbs change back. The Home tile and sentence already match."}
  ],
  "recommended": "a",
  "default_action": "Nothing is built. The menu keeps 'Delivery phases', the Home page keeps its old name, and the two tickets stay open."
}
```

### Card 3 of 4: customer page header question count (HPSMPOC-420 and HPSMPOC-421)

```json
{
  "id": "hpsmpoc-frame-chip-count-1102",
  "client_project": "Datasec/HPSM-POC",
  "title": "HPSM-POC: what should the 'questions answered' count at the top of a customer page show?",
  "bluf": "The header of every customer page shows a count such as '1 of 3 questions answered'. The Assessment page for the same customer says '0 of 2 scored questions answered', and for the first sample customer the header showed '0 of 0' while the security assessments page showed '16 of 16'. I read the current code. The header counts every question that applies, the Assessment page counts only the scored ones, and for a saved customer the header reads a stored figure that came out empty. The '0 of 0' reading comes from the review-site deployment report and I did not re-measure it. No earlier ruling covers this. I recommend one count everywhere, using the scored questions, because the score depends on them and the Assessment page already uses that count.",
  "options": [
    {"key": "a", "label": "Show the scored-question count everywhere", "detail": "The header uses the same figure and the same words as the Assessment page, so the numbers agree on every screen. A builder changes the header and it is tested."},
    {"key": "b", "label": "Show every question that applies, everywhere", "detail": "The Assessment page and the assessments list change to match the header. More screens change and the 'scored' wording goes."},
    {"key": "c", "label": "Leave it as it is", "detail": "The header, the Assessment page and the list keep showing different numbers for the same customer."}
  ],
  "recommended": "a",
  "default_action": "Nothing is built. The numbers keep disagreeing and both tickets stay open."
}
```

### Card 4 of 4: focus outline on the current menu page (HPSMPOC-399 last Note, also decides HPSMPOC-368)

```json
{
  "id": "hpsmpoc-menu-focus-ring-1102",
  "client_project": "Datasec/HPSM-POC",
  "title": "HPSM-POC: make the keyboard focus outline on the current left-menu page easier to see?",
  "bluf": "When someone tabs through the left menu onto the page they are already on, the focus outline overlaps the blue stripe at that item's left edge. On that one edge the outline is white on light blue at 1.91 to 1, while the other three edges read 8.81 to 1. The outline's corners also jump from the item's rounded shape to a squarer shape. The testers measured both and left the choice to you. I read the current code and the outline rule has not changed since they looked, and I found no earlier ruling. Two tickets are waiting on this answer to close. I recommend fixing it, because 1.91 to 1 is below the usual 3 to 1 guideline for focus outlines and the change is small and adds no words.",
  "options": [
    {"key": "a", "label": "Accept it as it is", "detail": "No change. The left edge of the outline stays hard to see on the current page's menu item, and the corner jump stays."},
    {"key": "b", "label": "Make the outline clear on all four edges and keep the corners round", "detail": "A builder moves the outline off the stripe or changes its colour there. It is tested and it affects only keyboard users on the current menu item."}
  ],
  "recommended": "b",
  "default_action": "Nothing is built. The outline stays as it is and both tickets stay open."
}
```

JSON validation line: all four objects above were extracted from this file and parsed with `python3 -I -c 'json.loads'`, with the required keys id, client_project, title, bluf, options, recommended and default_action present, `recommended` equal to one option key, and no ";" in any text field. Checker result (run 23:2x AEDT): 4 blocks, all parsed, every required key present, `recommended` is an option key in each, 0 semicolons, 0 build numbers, 0 paths, 2 or 3 options each, and a planted semicolon is detected by the same test (control true).

## UNMEASURED

- Nothing was rendered in a browser. The Feedback pill overlap (HPSMPOC-405), the menu clip (HPSMPOC-399), the focus ring contrast numbers, the "0 of 0" header reading and every 360 or 390 px reading are the testers' or deploy reports' numbers, relayed.
- `prior` outputs were long. I read the full text only for matches that were not just a shared project word ("mpscalc", "hpsmpoc") and I read the exact cards named. A relevant card whose only shared word was the project name could have been skimmed past.
- Whether the builder on HPSMPOC-322 items 5 and 6 is live (told in the task, not checked), and whether the design-group records branch has landed.
- That a tier override counts as a "price override" under the 2026-10-10 ruling is my reading.
- Q2: I did not read each of the twelve tickets' words list, only status and plan labels.
- The wording "scored" in Card 3 follows the Assessment page's own text. What makes a question scored was not read.
- Hosted state of everything (fenced).

## Read outside these fences

- The MPS project's own `CLAUDE.md` (project file, grep only for "words").
- The HPSM-POC B477 gate report file in that project's Briefs folder (one grep and two lines), a project file named by the ticket.
- Scratch programs and fetched files were written only in the session scratchpad.
- No `list`, no `add`, no kit, no report file, no write to any repo, no HTTP to any hosted host.
