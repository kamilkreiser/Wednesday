# MPS Calculator: Kam's decision cards, DRAFT for Tuesday to file
Drafted 2026-10-17 08:18 AEDT (from `date`) by a Tuesday drafter. Nothing filed, mailed, posted or tapped. Datasec / MPS Calculator only.
Main read at draft time: `git ls-remote origin refs/heads/main` = `12f8e566398bc83ea5c2be4d662f64ee9fbdbbfe` (#73, committed 08:13:07 +1100). Hosted, per the last deploy record: `0f8ad97` (B156, 16 Oct). Live site NOT re-read (no HTTP allowed to this drafter).

Cards: A (hosted deploy) · B1-B6 (K1-K6 from records seat B164) · B7 (E877 supply costs, Tuesday's addition) · C1 (MPSCALC-144 data step, Tuesday's addition) · DROPPED list · Notes for Tuesday at the end.

---

## CARD A
- **id:** `mpscalc-hosted-deploy-12f8e56-1017`
- **client_project:** `Datasec/MPS Calculator`
- **title:** Put 31 merged calculator changes on the hosted site, and approve their new words?

**BLUF (read aloud):**
Tap a to deploy main to the hosted calculator. It carries 31 merged changes since the 16 October deploy. Users will notice: a new short-form proposal layout with a credit box; Deals won and Deals lost tiles on Home; Save and Calculate buttons at the top and bottom of a quote; adding several catalogue items at once; small (i) help hints; the labels Customisation and Supplies; a button that fixes repeated line numbers; negative numbers refused with a message; an empty quote no longer calculates; a warning when a software licence term differs from the quote term; and anyone holding all four roles, you and the reviewer included, no longer sees the Acting as switch. The security fix from 16 October now really reaches the hosted site. Not included: owner self-approval, screens for deal-level usage, the target-click what-if change, the deploy-check fix. Tapping a also approves the new words in list W below.

**Options:**
- **(a) Deploy main 12f8e56 as is, and approve list W.** One MPS seat deploys from the CI package. It keeps today's version as the way back, then checks the site and a quote, and Tuesday tells you the result.
- **(b) Deploy, but hold back the newest change (#73, deal-level usage and target click).** The seat deploys the commit just before it (798fe98), so you get 30 of the 31. Deal usage and the new supplies messages wait for the next deploy. You approve list W without its part 4.
- **(c) Not yet.** Nothing is deployed and the hosted site stays on the 16 October version.

**Recommended:** a. #73 passed its gate's round 2 once its two missing tests were added, and no web screen can set deal usage yet, so users cannot reach it.
**Default (if no answer):** c. Nothing is deployed. Tuesday raises it again on Monday morning.

**Before you tap, know this (one sentence each):**
1. **The Acting as switch goes.** Your sign-in, and any other that holds all four roles (the reviewer's guest account was given 4 of 4), loses the switch at this deploy and sees every screen at once. No Entra change is needed for that.
2. **You still cannot approve your own quote.** You ruled self-approval on 16 October, but it is not built yet (MPSCALC-137). Until it is, a quote still needs the second approver account.
3. **The Entra group step is yours, and comes after the deploy.** To give everyone all four roles you run the app-registration script once with both flags (`--all-roles-group` and `--approver-only-user`), and then add people to the group. Every later run needs both flags too, or the script stops. The group needs an Entra ID P1 licence, which nobody has checked. Nothing in Entra changes unless you run it.
4. **Each deploy leaves a copy on the deploying machine.** The deploy now saves a copy of the hosted manual-items file there and never deletes it. Today the hosted site has no manual items, so the copy is only a short "not found" note. Once manual items exist, each copy holds their costs (card B4).
5. **The package is now 50 files, not 48.** The two extra files are the patched security component, so the deploy seat expects 50 and checks them.
6. **The deploy now reads the hosted manual-items file first, and stops if it finds entries the new version would refuse.** Today that file does not exist, so the check passes. It still misses some bad shapes (MPSCALC-202), and that has to be fixed before the first manual item is added (card C1).
7. **Any hosted draft that holds a negative quantity, page count or click price cannot be saved, copied or saved as a new version until the value is fixed.** Reading it and recalculating it work as before. Nobody has counted how many hosted drafts hold one.

**Words that need your yes (list W, verbatim; `{…}` is filled in by the app):**
*Part 1: customer proposal, the short form (#50).*
1. "01 Proposed Solution" · "02 Commercial Schedule" · "03 Delivery, Service & Next Steps"
2. "The proposition"
3. "Proposed fleet and package price"
4. "TOTAL UPFRONT ACQUISITION"
5. "Pricing basis"
6. "{edition} pricing. Upfront customer purchase, not a financed monthly rental. Support for the {n}-month term and any software listed are included in the package values; variable usage is additional." (a pricing-policy claim)
7. "The proposed devices, coordinated through one service model."
8. "Device stream" · "Solution and quoted inclusions" · "{CLASS} · {n} DEVICE(S)"
9. "{edition} price basis • {currency} excluding GST"
10. "Variable usage charges"
11. "No monthly total is stated because usage volumes are not yet confirmed."
12. "Software bundle and credit" · "Software element" · "{n}-month value · ex GST"
13. "Separate customer Microsoft 365 / Universal Print subscriptions, extended analytics and bespoke integrations are not priced in the package unless expressly documented in the final agreement."
14. "Commercial conditions" · "Item" · "Proposal treatment"
15. "Pricing validity": "{n}-day {edition} pricing; commencement date to be confirmed" (or "To be confirmed")
16. "Invoicing / financing": "Upfront purchase; separately metered usage charges. Finance terms and recurring fixed base charges are not quoted."
17. "Standard exclusions": "Paper, large-format roll media, specialty consumables, cabling/building works, customer Microsoft subscriptions and custom integrations unless added by agreement."
18. "A practical transition from technical discovery to operational handover."
19. "{n}-month service approach" · "Service area" · "Proposed treatment"
20. "Hardware support": "{n}-month hardware support for the devices in this proposal, under final OEM and site coverage conditions."
21. "Consumables": "Managed office toner and maintenance supply through metered page charging." (with large format: "…; large-format ink, printhead and maintenance-cartridge supply billed under the agreed separate model.")
22. "Operations & reporting": "Remote triage where available, meter collection, incident coordination, service reviews and approved moves, adds and changes."
23. "Implementation sequence" · "Stage" · "Joint activity / key outcome"
24. "1. Validate": "Confirm the {n}-device BOM, site allocation, workflows, users and volumes."
25. "2. Design & stage": "Approve network and security prerequisites, configuration, reader mapping, consumables and installation schedule."
26. "3. Pilot & deploy": "Test print, scan and authentication workflows; deploy in agreed waves and provide training."
27. "4. Accept & operate": "Complete user acceptance, document support channels and commence meter-based service processes."
28. Cover sub-line "{packages} | {n}-month managed support" (the edition is removed)
29. "Credit included in this proposal"
30. "Each credit is already taken off the package price shown, ex GST."
Removed from the customer document (ruled under K-15): the pricing-interpretation callout on purchase, "not yet specified", recommended next steps, the acknowledgement note and the proposal basis. The editor drops "Proposal basis", "Still to be confirmed (one per line)" and "Next steps (one per line)", but stored values are kept.

*Part 2: screens.*
31. Home: "Deals won" / "Deals lost" (replace "Deals closed"); "Quotes marked Lost in {Month YYYY}." / "Quotes marked Lost since 1 July {YYYY}."; group name "{Deals won|Deals lost} period"
32. BOM: "Package name, e.g. Devices and supplies" (placeholder); "Type a package name before saving."; "{n} sections · {m} lines"; screen-reader endings " (end of page)" and " (end of BOM)"
33. Picker: "Tick several items and set a quantity for each, then add them together." · "Choose the device" · "Choose the device for every ticked option." · "Each quantity is a whole number from 1." · "{n} selected" · "Add 1 item" / "Add {n} items" · "Select" / "Select {sku}" · "Qty" · "Quantity of {sku}" · "Device for {sku}" · "For {device}"
34. Hint button "About {topic}"
35. Hint "Quote type": "Finance (monthly): the customer pays one monthly charge over the term, covering the devices with finance, software and printing. Outright purchase: the customer buys the items on the BOM up front, and printing is charged per page at the usage rates."
36. Hint "Optional": "An extra the customer may choose, such as a stapler or finisher. It is priced per unit and never added to a total."
37. Hint "Included": "Supplied at no charge to the customer. Its sell price is 0, but its cost still counts against the margin."
38. Hint "Credit": "A deduction, such as a trade-in or a bundle credit. Its sell price and its cost count as negative amounts."
39. Hint "Section markup" (internal): "The markup on cost for lines in this section that have no sell price, sell override or catalogue default markup of their own. After you save, each line shows the markup that will apply."
40. Hint "Section rebate" (internal): "A percentage of this section's total that is deducted from the margin. It does not change the customer's price."
41. Hint "Mono click": "The charge to the customer for each mono (black) page, in dollars ex GST. It is a price per page, not a number of pages. Leave it empty to have it calculated from supplies, or for no mono charge." It ends with "Typical: {rate} a page (an A3 colour MFP fleet quoted at standard pricing, October 2026)." The rate is the review quote's real customer mono rate, and it is written into the code.
42. Hint "Colour click": the same as 41 for colour, also with the review quote's real colour rate.
43. Hint "Ink rate": "For large-format devices: the charge to the customer for each unit of ink, in dollars ex GST. Set the unit beside it. Leave it empty for no ink charge."
44. Hint "Ink unit": "The unit the ink rate is charged per, for example ml."
45. Hint "Calculate click rates from supplies" (internal): "Works the click rates out from the consumables' cost and yield, the mono and colour margins and the pages per device. A click rate typed above is used instead of the calculated one."
46. Repeated line numbers: "Line number {n} is used by more than one line. Each line needs its own number before the quote can be saved." (plural "Line numbers {1, 2 and 3} are used by more than one line. …") · button "Give each line its own number"
47. Negative input: "{field} is below 0; enter 0 or more." It shows under the existing headline "The draft has values beyond the technical limits." with the raw code and field path on screen (to fix the headline, see card B3).
48. Licence term warning: "Line {n} ({sku}) is a {term}-month licence on a {quote term}-month quote. An outright purchase pays the software for the whole term upfront: choose the {quote term}-month licence."
49. "Supplies" (was "Supply") wherever an item class shows.

*Part 3: what a quote shows when it is calculated (#73). Option b leaves these out.*
50. "This quote has usage rates per section and deal-level usage or page estimates. Use one: the deal's usage replaces the section rates."
51. "Mono pages per device per month must be a non-negative whole number." · "Colour pages per device per month must not be negative."
52. "Line {n} ({sku}) is not a device; page estimates belong on device lines." · "{model} is mono; colour pages are not allowed."
53. "A target click must be above 0." · "The target mono click is below the cost per page: the margin it needs is negative." (also colour)
54. Internal users: "Consumable {n} in the supplies list has a yield of 0; its cost per page is taken as 0." · "Consumable {n} in the supplies list has a negative cost or yield."
55. Everyone else: "A consumable in the supplies list has a yield of 0; its cost per page is taken as 0." · "A consumable in the supplies list has a negative cost or yield."
56. API-only refusals (no screen sends these yet): "usage.supplies is an internal input; setting it needs the Seller role and the internal-metrics permission (I-2)." · "usage: fixed rates are prices; setting or changing them needs the Seller role and the internal-metrics permission (I-2)." · "{path} is required (send [] for none)." · "{path}[{j}] must not be null." · "usage.inkUnit is 0 to 20 characters." · "sections, bomLines, manualItems, clickRates and usage need quoteMode 'purchase'." The .NET deserializer messages that name types (words 25-27 in gate B163) are a known Note, MPSCALC-195.

*For your information only, no yes needed (operator and deploy-log lines no browser shows):* the 9 server-start and source-store lines in gate B157 Check 11, the 11 deploy-check (PRE-1) lines in gate B161 Check 11, and the Entra script's 7 lines in gate B159 Check 10. Already ruled, so not asked again: "Finance (monthly)" / "Outright purchase" (K-20), "Customisation" (K-06) and "Add at least one device." (MPS-6).

**Trailer (sources):** PR list = `git log --oneline 0f8ad97..12f8e566` (31 commits, #43-#73, squashes); hosted = `B156_STATUS.md` :8, :243; package 50 + host load = `B161_STATUS.md` :7-8, :285 (B161-9), :323; PRE-1 in deploy + gaps = `B161` :213, :277 (B161-1), :324; overlay copy = `B161` :194, :280 (B161-4); negatives = `B161` :219-231, :290 (B161-14), words :259, :286 (B161-10); 136 consequences = `B159_STATUS.md` :294-298, :354 (B159-12), :388; Entra step + P1 = `B108_STATUS.md` :158-175; reviewer guest 4/4 roles = decision_queue `mpscalc-paul-invite-email-1012` delivery line (B66: roles 4/4); #73 = `B163_STATUS.md` :1-2, :321 + `B103_STATUS.md` last READY line (`e52debe`, test-only) + the #73 commit; no web screen for deal usage = `B163` :64, `B158_STATUS.md` :5; words part 1 = `git show 12f8e566:web/src/proposal/template/concise.ts` + `MPS-TIER2-REVIEW.md` :145-171; part 2 = `MPS-TIER2-REVIEW.md` :191-195, :236-256, `infoHintWords.ts` @12f8e566 :26-82, `B159` :322-323, `B161` :259, `B158` Check 8 #12; part 3 = `B158` Check 8 #1-16, `B163` Check 11 #17-27; K-20 fixed on main = `git grep` @12f8e566 (no "Rental (monthly)" outside a comment); K7/K8 folded here from `B164_STATUS.md` :310-311.
Card ids in this file name no person; "reviewer" is used in card text.

---

## CARD B1 (K1)
- **id:** `mpscalc-deal-usage-proposal-rates-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Deal-level usage quotes: show the usage rates on the customer proposal
- **BLUF:** A purchase quote that uses deal-level usage prints a proposal with no usage charge at all, because the proposal reads only the per-section rates. This is a customer document. Tap a to have the proposal print the deal's mono and colour rates the way it already does for section rates. Nobody can reach this on the hosted site until the deal-usage screens are built.
- **Options:** (a) Print the deal's mono and colour rates on the proposal: one build, then gate, then deploy. (b) Leave the proposal as it is until the deal-usage screens are built.
- **Recommended:** a. **Default:** a. A lane builds it, Tuesday gates it, and the words come back to you before any deploy.
- **Trailer:** `B164_STATUS.md` :304 (K1, C24, B158-11); `B158_STATUS.md` :5 (UI half = lane A, not built).

## CARD B2 (K2)
- **id:** `mpscalc-feedback-401-words-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Feedback box: the words when only the feedback could not be sent
- **BLUF:** If only the feedback send is refused while the person is still signed in, the box says "Your session has ended. Sign in again." That is not true, and the sentence stays on screen even after a later send works. A ticket (MPSCALC-194) fixes the behaviour, and it needs your words. Tap a to show a sentence that says only that the feedback was not sent.
- **Options:** (a) A new sentence, draft: "Your feedback could not be sent. Try again." (b) Keep today's sentence, shown only when the session really has ended. When it has not ended, the box shows the server's own error.
- **Recommended:** a. **Default:** b. The lane builds b. Tuesday re-raises the sentence at the next words gate.
- **Trailer:** `B164_STATUS.md` :305 (K2, C05, B157-5); `B157_STATUS.md` :17, :344 (B157-5); the sentence in option a was written by this drafter, not taken from a source.

## CARD B3 (K3)
- **id:** `mpscalc-negative-input-headline-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Negative numbers: fix the error headline users see
- **BLUF:** Since this round, a negative quantity, page count or click price is refused. On screen, though, the headline says the values are "beyond the technical limits", and it shows a raw code and a field path such as fleet[1].monoClickOverride. Tap a for a plain headline and the column names users know.
- **Options:** (a) The headline becomes "Some values are below 0.", and the error box shows column names instead of field paths. (b) Keep today's headline and paths.
- **Recommended:** a. **Default:** a. A lane builds it, and the words come to you at the gate.
- **Trailer:** `B164_STATUS.md` :306 (K3, C55, B161-10); `B161_STATUS.md` :233, :286, :303; headline at `QuoteEndpoints.cs:1160` @12f8e566 (`git grep`).

## CARD B4 (K4)
- **id:** `mpscalc-deploy-overlay-copy-retention-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Deploy safety copy of manual items: keep it, or delete it?
- **BLUF:** Before each deploy, the deploy now saves a copy of the hosted manual-items file on the deploying machine and never deletes it. Once manual items exist, that copy holds their costs. Tap b to keep a copy only when the deploy stops, which is when someone needs it to look into the cause.
- **Options:** (a) Keep every copy, as today. (b) Keep it only when the deploy stops, and delete it after a clean check. (c) Never keep it.
- **Recommended:** b. **Default:** b. The lane builds it under MPSCALC-203.
- **Trailer:** `B164_STATUS.md` :307 (K4, C49, B161-4); `B161_STATUS.md` :194, :280, :300; `MPS-TIER2-REVIEW.md` :92.

## CARD B5 (K5, the customer-caption half only)
- **id:** `mpscalc-rental-caption-customisation-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Rental proposal caption: keep "Configured options", or say "Customisation"?
- **BLUF:** You ruled that "Option" becomes "Customisation" as a label. The rental proposal the customer reads still says "Configured options (included in the base charge)". Tap a to keep the customer wording. Tap b to change it to match.
- **Options:** (a) Keep "Configured options (included in the base charge)" on the customer document. (b) Change it to "Customisation (included in the base charge)".
- **Recommended:** a. Customers know "options", and "Customisation" is an internal label. This is Tuesday's view; the records seat gave no recommendation for the caption. **Default:** a. Nothing changes.
- **Trailer:** `B164_STATUS.md` :308 (K5, C70, B162-8); main @12f8e566 `rental.ts:199`, `ProposalPage.tsx:124` (`git grep`). The class-label half is dropped as already ruled (see DROPPED).

## CARD B6 (K6)
- **id:** `mpscalc-panel-options-rental-and-tier-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Colour-panel items: confirm how they are offered and costed
- **BLUF:** As built, colour-panel items also appear as options on rental quotes, priced by the pool tier. On purchase quotes, panels are costed at the device's pool tier. Tap a to confirm that. Tap b to keep panels off rental quotes.
- **Options:** (a) Confirm as built. (b) Purchase quotes only: a lane removes them from the rental option picker.
- **Recommended:** a. **Default:** a. Nothing changes.
- **Trailer:** `B164_STATUS.md` :309 (K6, C35, C74; B159-7, B162 REPORT (g)); `B159_STATUS.md` :349 (B159-7).

## CARD B7 (Tuesday's addition: E877 supply costs)
- **id:** `mpscalc-e877-supply-cost-source-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** E877 supplies: keep the price book's costs, or use the review spreadsheet's?
- **BLUF:** The 16 October review spreadsheet lists 17 supply costs for the E877. All 17 page yields match the price book, but none of the 17 costs do, and the gaps are not a constant ratio. Using the spreadsheet would change the E877 cost per page, and so its prices. Tap a to keep the book until the distributor sends the next one.
- **Options:** (a) The book stays the source. You ruled on 1 October that it is current until a newer one replaces it. (b) Use the spreadsheet's costs for the E877. This is a pricing change, so it needs a workbook register row, a failing test first, and a gate.
- **Recommended:** a. **Default:** a. Nothing changes.
- **Trailer:** `B104_STATUS.md` :133-136, :139-140, :278-279; `B104_ADDENDUM-3` item 1; earlier ruling = decision_queue `mpscalc-pricebook-validity` (c, delivered C-07). No figures on this card.

## CARD C1 (Tuesday's addition: MPSCALC-144 data step)
- **id:** `mpscalc-large-format-manual-items-1017` · **client_project:** `Datasec/MPS Calculator`
- **title:** Add the three large-format items to the hosted catalogue by hand
- **BLUF:** The review quote's three large-format lines are in neither price book: a DesignJet multifunction printer, its 5-year care pack, and an install and network setup. No code is needed. An Administrator adds them as manual items on the hosted inventory, with costs taken from the review spreadsheet (lane E has written the step). These would be the hosted site's first manual items, so the deploy check that reads them should be fixed first.
- **Options:** (a) Add them after this deploy. (b) Add them after the deploy-check fix (MPSCALC-202) and the safety-copy rule (card B4) are live. (c) Not now.
- **Recommended:** b. Gate B161 asked for that fix before the first manual item. **Default:** c. Nothing is added. Tuesday re-raises this with the deploy card that carries MPSCALC-202.
- **Who acts:** you, or someone you name who holds Administrator and internal-metrics, on the hosted inventory. The ink rate is not a catalogue row: it is set on the quote.
- **Trailer:** `B104_STATUS.md` :280-293 (the step, figures by spreadsheet cell only); `B104_ADDENDUM-3` item 1; `B161_STATUS.md` :213, :324 ("fix B161-1 (and -4) before a hosted overlay.json exists"); MPSCALC-144 comment #39550. No price figures on this card.

---

## DROPPED (already ruled, or folded into card A)
- **K5, the class-label half** ("Customisation" wherever a class label shows): already ruled. Card `mps-paul-review-catalogue-k05-k06-k07-k10-k13-k16-1016`, a, 2026-10-16 13:09: *"show 'Option' as 'Customisation' and move panel and colour kits into it (K-06…)"*. Only the customer caption is asked (B5).
- **K-20 quote-type names** (B164 lists none, but card A's words carry them): `mps-paul-review-words-k02-k03-k14-k20-1016`, a, 2026-10-16 13:10: *"quote types renamed to 'Finance (monthly)' and 'Outright purchase' (K-20)"*. Main @12f8e566 uses them everywhere outside one code comment.
- **"Add at least one device."** (#54): ruled MPS-6 under `mpscalc-decisions-pack-1012`, a, 2026-10-12 (C-23).
- **Owner self-approval itself** (asked as K8's background): `mps-paul-review-roles-k01-k18-1016`, a, 2026-10-16 13:08: *"All roles + owner self-approval, audited; accept cost-plus visibility"*. Card A says only that it is not built yet.
- **Hosted deploy as a practice** (card-per-deploy): the last one was `mpscalc-hosted-deploy-0f8ad97-1016`, a. It does not cover this deploy, so card A asks again.
- **K7** (the Entra script needs both flags on every later run): folded into card A, consequence 3. The B164 default (MPSCALC-201 makes the script refuse early, in words, plus a runbook line) is engineering, not a product choice.
- **K8** (the Acting as switch goes; self-approval stays 403): folded into card A, consequences 1-2, as B164's recommendation asked (*"say it on the deploy card"*).

---

## Notes for Tuesday (not for the board)
1. **Risky item for card A option b = #73** (lane D stack). It is the newest change, it is engine work, and its round-2 gate was NO GO until the test-only follow-up `e52debe`. I did not read whether the tier-2 confirm on `mutA`/`mutB` (DELTA 200) finished before the 08:13 merge. Check that before you file. If the confirm never ran, drop option b and keep a.
2. **Option b needs a CI package for `798fe98`.** I did not check that one exists (no `gh` used). The deploy seat's `fetch` would show it.
3. **Hint words 41-42 carry the review quote's real customer rates, written into the code** (`infoHintWords.ts:61,67` @12f8e566). The tier-2 review flagged this as TIER-1-SUSPECT (153), and they are on main now. I left the figures off the card. If no ruling covers them, they need one.
4. **First name in code comments.** Main @12f8e566 carries the reviewer's first name in code comments through card ids (`infoHintWords.ts`, `QuoteScreen.tsx:41`). This was flagged in the tier-2 review :259. It is not a card item.
5. **The hosted state is from the 16 October record, not re-read.** Before filing, re-read the served bundle or ask the deploy seat. That confirms nothing was deployed since `0f8ad97` and that the hosted site still has no manual-items file, which consequence 4 and the 404 path depend on.
6. **Card B2's sentence in option a is mine.** Edit it if lane H has a draft.
