# MPS calculator: new words and consequences for the hosted deploy of main e6f92a5 (list W2)

Card mpscalc-hosted-deploy-e6f92a5-1017. Tapping a on that card approves the NEW words in Part 2. {…} is filled in by the app. Prepared by Tuesday from the merged code, the GitHub API and the QA gates, 2026-10-17 17:20 AEDT. Every figure here is a count, a hash or a synthetic test value.

## BLUF
- The hosted calculator runs main 12f8e566 (deployed this morning, gate B166). MPS main is now **e6f92a5f** (read by `git ls-remote` at 17:18:16-17:18:19 AEDT). That is 9 merged changes, PRs #74 to #82 (GitHub compare: ahead 9, behind 0, 51 files).
- What users will notice: a "Deals won" title on the list behind the Deals won tile; a plain message when only feedback fails to send; a plain "Some values are below 0." headline with line and column names; two new item classes, Care pack and Staging; and, on a deal-usage quote only, the deal's mono and colour rates printed on the customer proposal.
- **The deal-usage quote has no screen yet.** One can only be made through the API, so the proposal change in #82 (and B170-3/-4/-5, OBS-1/-2 below) reaches no one who works only in the browser.
- 3 sets of words are already approved by you today. **5 NEW items** need your yes (Part 2). One is a new pairing on the customer proposal (B170-4).
- **Once anyone adds a Care pack or Staging item, there is no way back to today's version.** From then on you can only roll forward (B167, B168).
- **Main's CI is green:** run 39009325479 on e6f92a5f completed with success (re-read by Tuesday, 17:2x AEDT), so its package exists. The 4 CodeQL analyses, web and python were green at 17:20.

## Part 1: the 9 changes, in plain words
Source: GitHub API `pulls/{n}` (merge sha, merged time) and the PR bodies; `compare/12f8e566...e6f92a5f`.

| PR | Merge sha | Ticket | Gate | What a user sees change |
|---|---|---|---|---|
| #74 | ed726068 | MPSCALC-140 (half) | B165 GO WITH NOTES | Nothing on screen. The calculator accepts the catalogue key that care packs use (`care_`). |
| #76 | 0217044e | MPSCALC-142, -155 | B167 GO WITH NOTES | Two new item classes, **Care pack** and **Staging**, in inventory, the class filter and manual items. Both total under Services. |
| #77 | 422b87b2 | MPSCALC-158 r2 | B167 GO WITH NOTES (round 2) | Setting, changing or clearing a deal's target click no longer asks for a reason and no longer writes a price-audit entry. Real price changes still need a reason. Only the API can do this; there is no screen. |
| #75 | 725b4ef5 | none (Kam card `mpscalc-quote-list-deals-closed-title-1017` = a) | Tier 2, reviewed at source by Tuesday | The list behind Home's Deals won tile is titled "Deals won" instead of "Deals closed". |
| #78 | f1d5641a | MPSCALC-140 (half) | B167 NO GO, then B168 GO WITH NOTES (round 2) | Care packs are imported from the distributor price book with the Care pack class. The hosted site shows them only after a new price book is imported there. Today's hosted store was written before this change, so it holds none (drafter's reading of `ReferenceData.cs:47-51`, not measured on the host). |
| #79 | 1e8a738f | MPSCALC-194 (partly) | Tier 2, reviewed at source by Tuesday | If only the feedback send is refused, the box says "Your feedback could not be sent. Try again." The message clears after a later send works. |
| #80 | b8ea9027 | MPSCALC-213 | Tier 2, reviewed at source by Tuesday | If every refused value is below 0, the headline reads "Some values are below 0.". Each entry names the line and the grid column instead of a raw field path. |
| #81 | cfe376d5 | MPSCALC-203 | B170 NO GO, then round 2 READY; Tuesday's completion check (tree 0f42ab5c = B170's probed tree) | Users see nothing. On the deploying machine, the copy of the hosted manual-items file is kept only when a deploy stops. It is removed after a clean check. |
| #82 | e6f92a5f | MPSCALC-214 | B170 NO GO, then round 2 READY; Tuesday's completion check (tree 81f604f8 = B170's probed tree) | The customer proposal of a deal-usage quote prints the deal's mono and colour rates, one pair per device class that holds a counted device line. They replace the section rates. The ink rate is not printed. |

## Part 2: words

### Already approved by you (shown for completeness, not asked again)
1. "Your feedback could not be sent. Try again." (#79, `web/src/feedback/words.ts:10`). Card `mpscalc-feedback-401-words-1017` = a, ruled 09:23:50.
2. "Deals won" as the quote-list title (#75, `web/src/screens/QuoteList.tsx:148`). Card `mpscalc-quote-list-deals-closed-title-1017` = a, ruled 10:34:04.
3. "Some values are below 0." as the error headline (#80, `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, the return line of the range check). Card `mpscalc-negative-input-headline-1017` = a, ruled 09:23:27.

### NEW: tapping a approves these
4. Error box, one line per below-0 value (#80, `web/src/components/ErrorBox.tsx:41`): "Line {n}, {column} is below 0; enter 0 or more."
   - {column} is the grid's existing column header (`ErrorBox.tsx:27-33`): "Qty", "Mono pages / device / month", "Colour pages / device / month", "Mono click override" or "Colour click override".
   - Any other entry is shown as it came. That is list W item 47's "{field} is below 0; enter 0 or more."
5. Item class labels, wherever a class shows (#76, `web/src/screens/inventory/InventoryScreen.tsx:23-24`): "Care pack" · "Staging".
   - Your K-05 and K-07 rulings made these two classes. Nobody has put the label text itself to you.
6. **Customer proposal, a new pairing of existing words (#82, gate B170-4, `B170_STATUS.md:109`).** On a deal-usage quote, the rate rows read "Monochrome office prints" and "Colour office prints" (`web/src/proposal/template/sections.ts:381-382`), each followed by the device class and "{rate} per page".
   - Those rows are printed against **Large format, Software, Services or Other**, not only Office MFP.
   - B170 found no new string; the new part is which words appear together.
7. API-only refusal (no screen sends it) (#76, `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs:45`): "class must be one of device, option, software, supply, service, other, carePack, staging."
8. Price-book import findings for care packs (#78, `src/MpsCalc.Import/PriceBookImporter.cs`, read at e6f92a5f):
   - "'BID Pricing' has no Core-block header (Group, Product Number, Sell) in columns B:F; care packs come from the model sheets only." (:561)
   - "Care pack {sku} has price cells that differ." (:606)
   - "Care pack {sku} has no numeric price; it is listed as unavailable." (:618)
   - "Care pack {sku}: the SKU cell carries a footnote mark, read as {sku}." (:643)
   - Plus the import rule text "CARE-PACKS" (:140).
   - **Which screen shows these findings: UNMEASURED.** They are staff-only and never reach a customer.
   - **Flag:** the rule text at :140 still ends "Item class: service (default K-05, until MPSCALC-142).", but since #78 imported care packs carry the Care pack class. Those words are out of date. Tuesday suggests a one-line ticket rather than approving them as they stand.

### For your information only, no yes needed
- Removed from the feedback box (#79): "Your session has ended. Sign in again." The app's own sign-in check now decides whether the session has ended.
- Deploy-machine lines no browser shows (#81, `scripts/deploy-from-ci.sh`):
  - "deploy-from-ci: PRE-1: could not create a new overlay copy (the name exists or the folder is not writable): {path}"
  - "deploy-from-ci: PRE-1: the overlay copy is kept: {path}"
  - "deploy-from-ci: PRE-1: the overlay copy could not be removed after a clean check: {path}"
- The import tool's summary line now ends "…, {n} care-pack rows (…)" (`tools/MpsCalc.ImportCli/Program.cs`).

## Part 3: what shipping this means for users (gate B170 and the carried items)

### From gate B170 (`1_Project_Definition/Briefs/2026-10-17_B170_STATUS.md`)
- **B170-3 (:108): an approved deal quote's proposal changes after the deploy.**
  - What happens: if a deal-usage quote was approved before this deploy, its approved proposal gains the rate rows afterwards. In the gate's synthetic quote that was 0 rows before and 4 after.
  - What does not change: the stored snapshot bytes.
  - A rollback hides the rows again.
  - Whether the hosted store holds any deal-usage quote: UNMEASURED (B170's own list). The hosted site held 6 quotes at B166 (`B166_STATUS.md`, step 5 start log).
- **B170-4 (:109): the office-prints labels are printed against other classes.** See Part 2 item 6.
- **B170-5 (:110): the one-pager prints at most 6 rates** (`OnePager.tsx:29`). A deal repeats the same pair of rates for every class, so a deal with 4 or more classes shows "and {n} more rates (see full proposal)" and hides rows. On the gate's 5-class quote, the Office MFP and Large format rows were the ones hidden. The full proposal shows all of them.
- **B170-8 (:113): a deploy that stops after the clean check leaves no copy.** If `az webapp deploy` or the live check fails after PRE-1 passed, no copy of the manual-items file is left. This follows your ruling on card `mpscalc-deploy-overlay-copy-retention-1017` (= b): the copy is removed before the deploy step. The copy B166 kept this morning stays where it is: each run removes only its own copy (`B166_STATUS.md:98`).
- **OBS-1 (:120), yes or no:** *"Print a colour rate only for device classes that have estimated colour pages?"*
  - Today, a class with 0 colour pages (a plotter, say) still shows "Colour office prints · Large format · {rate} per page", although its colour charge is 0.
  - Default if you do not answer: no change. The row stays, which is consistent with the engine rule X-25.
- **OBS-2 (:121), yes or no:** *"Block a deal-usage quote that has no counted device, instead of printing it with no rates?"*
  - Today, a deal quote whose only device is optional calculates, and its proposal prints with no rate rows.
  - Default if you do not answer: no change.

### Carried from earlier gates and rulings
- **Rollback doors: roll forward only, once a Care pack or Staging row exists** (B167, `B167_STATUS.md:15`, `:165`, `:345`; B168-1, `B168_STATUS.md:127`; #76 and #78 bodies). The way back (12f8e566) is older than the class change. Once a manual item, an overlay row or a quote holds a Care pack or Staging item:
  1. the old version refuses to start on such an overlay;
  2. it hides quotes that hold such items (the files stay on disk);
  3. it also hides every quote with an imported care pack that has been calculated on the new code.
  - Today none exists: B166 found no `overlay.json` and recorded 0 changed quote files at its end. So the way back stays open until someone adds the first such item.
- **PRE-1 still passes the class numbers 6 and 7** (B167-5, `B167_STATUS.md:297`): the app refuses them at start. #76 added only the two class names to PRE-1's list (`scripts/deploy-package.py`, a one-line change). The fix is MPSCALC-202.
- **deploy-from-ci.sh takes PRE-1 from its own checkout** (`deploy-from-ci.sh:24-26`, `B167_STATUS.md:165`):
  - Deploy e6f92a5 from a checkout at e6f92a5. An older checkout would stop on Care pack/Staging rows that are in fact valid.
  - A rollback to 12f8e566 run from a newer checkout would pass PRE-1 on an overlay holding Care pack rows, and then fail to start.
- **The Entra group step is still yours.** This range changes no Entra script (compare file list). Whether you have done it since this morning: UNMEASURED.
- **Your large-format items (C-35, card `mpscalc-large-format-manual-items-1017` = b) still wait.** They wait until both MPSCALC-202 and MPSCALC-203 are live.
  - MPSCALC-203 is merged (#81) and would go live with this deploy.
  - **MPSCALC-202 is not merged.** A GitHub search of the repo for "MPSCALC-202" returns 0 PRs; the same search for "MPSCALC-203" returns #81, which shows the search works.
  - So the large-format items still wait after this deploy.

## Part 4: the way back (rollback build)
- **Today's hosted build is the way back.** Main 12f8e566, from CI package run 38967822861.
  - `mpscalc.zip` sha256 `cdfe793e80248e866702e466d44c1489dbbb700d87293b5a4d8cabd065811d00`, 3,142,810 B, 50 files (`B166_STATUS.md:79`).
  - It is kept in `.tools/wt-B166-release/.local/deploy-packages/12f8e566…/`. At 17:20 AEDT the zip was there and its sha256 matched.
  - The GitHub copy of the artifact expires 2026-10-23 21:17Z (API read).
- **The older build B166 kept also stays.** 0f8ad97 (`7a5262fb…8570`, 48 files, `.tools/wt-B156-release`) is never deleted (`B166_STATUS.md:172`).
- **When a rollback needs Tuesday first** (B166's rule, `B166_STATUS.md:173-175`): once a real user saves a quote, takes a snapshot or sends feedback on the new build, a rollback becomes STOP: NEEDS TUESDAY. The roll-forward-only doors above apply on top of that.
- **What a rollback would undo:** the 9 changes above. The deal rates disappear from proposals again (B170-3).
- **Option b on the card** would deploy cfe376d5, main just before #82.
  - Its gated tree is 0f42ab5c (#81 body).
  - CI run 39008873514 succeeded, and its package `deploy-mpscalc-cfe376d5…` (3,150,560 B) is available until 2026-10-24 06:13Z.
  - That build carries everything except the proposal deal rates, so B170-3/-4/-5 and OBS-1/-2 would not apply.
