# MPS tier-2 READY branches: review at source · 2026-10-16 · for Tuesday
Reviewer: Tuesday's review assistant (read-only). Project `<P>` = `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`, repo `<P>/2_Project_Files`.
Inventory: `2026-10-16_MPS-READY-INVENTORY.md`. Lane file lists and tier rule: each lane brief `:9` / `:10`.

**Instruments:**
- `git --no-optional-locks -C <repo> ls-remote origin` (re-read this session): main = `621e3300aaae70b32a39edaed653beff7fe45b2d`, unchanged since 16:27.
- `merge-base`, `diff <base> <head>` (whole diffs saved under this session's scratchpad `t2/*.diff`), `diff --name-status --diff-filter=MD`, `log`, `grep <sha>`. All read verbs on the project checkout.
- One merge simulation (`merge-tree --write-tree`, for 171 only), run in a throwaway `git clone --shared` at `…/scratchpad/t2review` with push URL `DISABLED`.
- Nothing was built or run, and no HTTP call was made.

**Two facts that apply to every row:**
- **CI does not run Playwright.** `.github/workflows/ci.yml:61-66` runs only `npm ci`, `lint`, `npm test` (vitest) and `build`. Every e2e edit below (lanes A, B, G) is unverified by PR CI. Only the lanes' own local runs cover them: B101:47 33/33; B109:265 39/40; B100:87 "the three older BOM specs are edited but not run".
- **CodeQL has run on no head** (inventory `:35`).

## BLUF
- **9 OPEN PR, 3 HOLD.** Stacks count as one PR each; 171 is skipped as asked.
  - OPEN: 184, 180, 178→173, 111, 109, 157→156, 138→186, 143, 175-relay.
  - HOLD: 183, 105, lane A stack.
- **TIER-1-SUSPECT (3):**
  - `b107/183`: deploy path.
  - `b102/105`: validation of price inputs.
  - `b100/153` inside the lane A stack: customer price figures in code, shown as pricing guidance.
- **Lane A stack (top 185): HOLD**, for 4 reasons:
  1. 153 is tier-1-suspect (above).
  2. `smoke.spec.ts:42` is left with two matching buttons. CI cannot see it.
  3. `NewQuoteForm.tsx:48-49` still has the old K-20 words. **CONFIRMED.**
  4. The reviewer's first name appears in 4 code comments.
- **171 conflict is trivial:** keep both blocks.

| Branch | sha ok | tier ok | scope ok | tests ok | words | Recommendation |
|---|---|---|---|---|---|---|
| `b100/184` `3434b0e` | yes | yes | yes | yes (+1 test, no −) | 0 | **OPEN PR** |
| `b107/180` `735d400` | yes | yes (dev server only) | yes | yes (+2 tests, no −) | 0 new (403 text reused) | **OPEN PR** |
| `b107/183` `41af1e3` | yes | **NO: TIER-1-SUSPECT** (deploy path) | yes | yes (new 235-line test) | 8 operator lines | **HOLD** (re-tier: QA gate) |
| `b107/178`→`173` (top `6f41730`) | yes / yes | yes (note: hosted seeding with act-as, Kam-ruled MPS-2 = a) | yes | yes (one skip test rewritten, stronger) | 4 + 4 doc/tool lines | **OPEN PR** (one squash from 173) |
| `b109/111` `1781a4f` | yes | yes | yes | yes (e2e list extended) | 0 | **OPEN PR** |
| `b109/109` `528446f` | yes | yes | yes | yes (+27 cases) | 0 | **OPEN PR** |
| `b109/157`→`156` (top `a38f02b`) | yes / yes | yes (customer-document words only; no figure computed) | yes | yes (removed tests match removed blocks; one-page print test replaced by "cover = page 1, 2-4 pages") | ~45 new + removals (N1-N28, C1-C4, W1/W2) | **OPEN PR** (one squash from 156; reviewer name in branch name, see detail) |
| `b101/138`→`186` (top `3b97c65`) | yes / yes | yes (display of existing figures) | yes (`styles.css` `.kpi` rules only) | yes (order assertions re-pointed; won·lost line removed by design) | 4 | **OPEN PR** (one squash from 186) |
| `b104/143` `7a460ab` | yes | yes | yes | yes (new test) | 1 | **OPEN PR** |
| `b104/175-relay` `c9fb7f9` | yes | yes | yes | yes (new test) | 1 (same as main #43) | **OPEN PR** |
| `b102/105` `161def0` | yes | **NO: TIER-1-SUSPECT** (validation of price inputs; lane C2 brief `:10` says Tier 1) | yes | yes (+2 theories, no −) | 1 | **HOLD** (QA gate) |
| lane A `145`→`146`→`148`→`139`→`153`→`185` (top `7c7ff9f`) | yes ×6 | **153 TIER-1-SUSPECT**; rest yes | yes | unit yes; e2e edited, not run by CI or lane; smoke.spec break | ~30 | **HOLD** (4 reasons above) |
| `b102/171` | not reviewed (skipped) | — | — | — | — | conflict trivial: keep both |

The other heads all match ls-remote, as the inventory has them: `ecc1021`, `f37c6ab`, `d5fa999`, `95136a8`, `3729f37`, `e6a71fb`, `2e8608b`, `63d0630`.

**Stacks:** Tuesday merges each stack as ONE squash PR from the stack top. Each top was reviewed as the cumulative diff from merge base `0f8ad97d` (lane A, B, G, J). Base `7af91dec` applies to 184 and 105 (both 3 behind main). The inventory measured these tops as clean onto main.

---

## Per-branch detail

### 1. `b100/mpscalc-184-failed-read-guard` @ `3434b0e2431cc240185147d6d448e4c8aae7d61d` (base `7af91de`)
- **Diff:** one file, `web/src/screens/bom/EffectiveMarkup.test.tsx:266-288`, +24, an added test only.
- **Tier:** test only.
- **Scope:** the lane A bom test.
- **Tests:** a new guard test that the failed inventory read leaves every cell pending. No line removed.
- **Words:** none.
- **Wrong:** nothing.
- **OPEN PR.**

### 2. `b107/mpscalc-180-hmr-host-guard` @ `735d400…` (base `0f8ad97`)
- **Diff:** `web/vite.config.ts:41,60-77,84,88`. `guardUpgrades` moves Vite's `upgrade` listeners behind the loopback Host check. The 403 text becomes the constant `FORBIDDEN` (`:41`), with the same sentence as before.
- **Tier:** dev and preview server only. Not in the package or deploy path.
- **Tests:** `web/vite.hostguard.test.ts:42-73,131-149` adds a raw WebSocket handshake for `vite-hmr` and `vite-ping`. It expects 403 for foreign Hosts and 101 for loopback. Additions only.
- **Words:** the existing "Forbidden: this local server answers only to localhost, 127.0.0.1 or [::1]." is now also sent on a refused WebSocket upgrade (`vite.config.ts:41`).
- **Wrong:** nothing found. If HMR were ever configured on a separate `hmr.port` server, that server would not be guarded. That is not the case today.
- **OPEN PR.**

### 3. `b107/mpscalc-183-pre1-in-deploy` @ `41af1e3…` · **TIER-1-SUSPECT**
- **Tier: changes the deploy path.**
  - `scripts/deploy-from-ci.sh:88-123`: `scm_host`, `read_overlay`, `pre1_hosted`, and at `:121-123` a new gate before `az webapp deploy`.
  - It runs `az account get-access-token` plus `curl` against the live site's Kudu VFS (`:100-106`), then `python3 -I deploy-package.py pre1`.
  - `scripts/deploy-package.py:421-480` adds the PRE-1 rules (`PRE1_SHOWS_NOTHING`, `PRE1_ITEM_CLASSES`).
  - Every future `deploy` now reads production state and can stop the deploy. By the task's rule, this is the deploy/infra path.
- **Scope:** `scripts/deploy-*` (lane J) plus the new `scripts/tests/test_deploy_pre1.py`.
- **Tests:**
  - A new file, run by CI's python job (`ci.yml:86` globs `scripts/tests/test_*.py`).
  - It covers 13 refused shapes, absent and 404 overlays, a 500 that stops the deploy, probe/check never reading the overlay, and "never prints a value".
  - It also checks parity with the C# source (`ShowsNothingRanges`, `ItemClassDto`) and the bicep overlay path.
- **Words (operator output, not app UI):**
  - `deploy-from-ci.sh:113` "deploy-from-ci: PRE-1: the read of the hosted overlay failed (above)"
  - `:115` "deploy-from-ci: PRE-1 counted entries the new app would refuse at boot (above)"
  - `:116` "PRE-1: overlay.json absent → 0 entries (not run)"
  - `:117` "deploy-from-ci: PRE-1: the hosted overlay read answered HTTP $code, so the overlay cannot be checked"
  - `:122` "PRE-1 did not pass (above); nothing was deployed"
  - `deploy-package.py:473` "PRE-1: STOP: the overlay file could not be read as JSON"
  - `:476` "PRE-1: STOP: the overlay file is not a JSON object"
  - `:479` "PRE-1 count: …"
- **Wrong / notes:**
  1. Each deploy copies the hosted overlay, which holds manual rows with costs, into `.local/deploy-packages/<sha>.live/overlay-*.json`. The copy is 0600 and git-ignored. That puts confidential price data on the operator machine at every deploy. Say so to Kam.
  2. `pre1_count`: a `manualRows` element that is neither a dict nor null (for example a list) raises AttributeError. rc is then non-zero, so the deploy stops (fails closed), but with a traceback rather than a PRE-1 line. Minor.
  3. The new item classes that lane E is waiting on will turn this test red until `PRE1_ITEM_CLASSES` is updated. `B107:160` already records this.
- **HOLD**: re-tier to 1 (QA gate), or Tuesday rules it tier 2 explicitly.

### 4. `b107/mpscalc-178-docs-drift` → `b107/mpscalc-173-hosted-s4` (top `6f41730…`; ONE squash PR from 173)
- **Cumulative diff (5 files):** `docs/DEMO.md`, `tools/demo/seed.py`, `tools/demo/test/{stub_api,test_demo_doc,test_seed_purchase}.py`.
- **Tier:** no product code. `seed.py:558-571` (`hosted_purchaser`) reads `GET /api/v1/me` and posts S4 only when the token already holds Seller + PricingAnalyst. It sends act-as `Seller,PricingAnalyst` for S4 only (`:65-67`, `:694-710`). This uses existing roles through the existing act-as narrowing; no role or auth rule changes. Kam ruled C-23 MPS-2 = a.
  - Note: running it on hosted writes privileged price inputs (synthetic SYN- items) to the hosted showcase under a person's token. That run is approval-class (Kam's), not this PR.
- **Scope:** lane J (`docs/DEMO.md`, `tools/demo/**`).
- **Tests:**
  - `test_seed_purchase.py`: `test_hosted_mode_skips_s4` is rewritten for the new skip reason and is stronger (it now also asserts that no non-GET request is made). A new positive test checks act-as on every request and that no price is printed.
  - `test_demo_doc.py`: two classes added. Nothing weakened.
- **Words (docs and tool output):**
  - 178: `DEMO.md:13-14` "A proposal is printed here, never sent: an approved quote's footer says "Commercial in confidence" (C-13); any other quote's says "INTERNAL DRAFT — NOT FOR CUSTOMER RELEASE"."
  - 178: `DEMO.md:60` "Its footer follows the quote's state: **Commercial in confidence** once approved (C-13), **INTERNAL DRAFT — NOT FOR CUSTOMER RELEASE** in any other state (it is seeded as a draft)."
  - 178: `DEMO.md:75`, the talk track "Approved, its print footer says "Commercial in confidence"; any other quote's says "INTERNAL DRAFT — NOT FOR CUSTOMER RELEASE". Nothing is sent to anyone."
  - 178: `DEMO.md:129-130` "A proposal is printed, never sent from here. Its footer: "Commercial in confidence" once approved, "INTERNAL DRAFT — NOT FOR CUSTOMER RELEASE" in any other state."
  - 173: `DEMO.md:58-59` (line numbers at 173) "hosted, it is posted only with the token of a person who already holds Seller and Pricing analyst (see "Seeding the hosted quotes")."
  - 173: `DEMO.md:172-176`, the "DEMO-S4 hosted (MPSCALC-173, MPS-2: no new permissions)" paragraph.
  - 173: `seed.py:564` "the API did not say which roles the signed-in identity holds (…)"
  - 173: `seed.py:567-569` "the signed-in identity does not hold the Pricing analyst role (S4's manual items, section markups and fixed rates need Seller and Pricing analyst, B17 I-2). Run it with the token of a person who holds both (--token-fd); no role is added (MPS-2)"
- **Wrong:** nothing. "Datasec" in DEMO.md is the project owner (already on main), not a client name.
- **OPEN PR.**

### 5. `b109/mpscalc-111-narrow-screen` @ `1781a4f…`
- **Diff:** `web/src/proposal/proposal.css:95-99`. Inside `@media screen and (max-width:900px)`, `.pd .pd-table{display:block;overflow-x:auto}` and `.pd{overflow-x:clip}`. Screen only, so print is untouched.
- **Tests:** `web/e2e/proposal-buttons.spec.ts:370-371` adds the state 'purchase full, draft'. e2e only (not in CI); B109:272 reports 6/6 locally.
- **Words:** none.
- **OPEN PR.**

### 6. `b109/mpscalc-109-summary-cut-mock` @ `528446f…`
- **Diff:** `web/src/proposal/OnePager.tsx:43-67`. `cutSummary` now follows the mock's `condense_summary`: the text is trimmed and counted in code points, and a sentence end counts only as `". "`, `"! "` or `"? "`. `leadSummary` trims the first paragraph.
- **Tier:** text cutting of the summary only, no figure.
- **Tests:** new `summaryCut.test.ts` (27 cases) and new fixture `fixtures/summaryCutCases.ts` (SYNTHETIC "Sample Customer C"). Nothing removed.
- **Words:** none new. The lead text can differ on 4 edge inputs (by design, to match the mock).
- **Wrong:** nothing. It merges cleanly with 157, which also edits `OnePager.tsx` (inventory).
- **OPEN PR.**

### 7. `b109/mpscalc-157-proposals-paul-1013` → `b109/mpscalc-156-credit-callout` (top `a38f02b…`; ONE squash PR from 156)
- **Cumulative:** 22 files, +731 −345, all under `web/src/proposal/**` plus three e2e specs (`proposal-buttons`, `proposal-content`, `rental-book`). That is lane G's scope.
- **Tier:**
  - The customer document's structure and words change. Removed: Pricing interpretation (purchase), Not yet specified, Recommended next steps, the acknowledgement note and Proposal basis. Added: the concise short form and the credit callout.
  - No figure is computed. `CreditCallout.tsx:45-47` filters the server's `softwareReconciliation` rows by sign and prints the server's amounts.
  - `OnePager.tsx:180` sums `x.quantity` into a device count for the office capability intro. That is a count, not a price.
  - **Tier 2 holds**, but several new sentences make commercial and pricing-policy claims on a customer document. All go to Kam's words gate.
  - `CREDIT_CALLOUT_NOTE` ("already taken off the package price") agrees with `docs/API.md:419` ("credits in at their sign, as in every total").
- **Tests:**
  - Deleted: the `pricingCallout` unit tests, the next-steps / basis / not-specified assertions in `OnePager.test.tsx`, `ProposalDocument.test.tsx` and `RentalDocument.test.tsx`, and the e2e "short-form prints EXACTLY one A4 page". Each removal matches a block or function removed under K-15.
  - The one-page e2e is replaced by "cover sheet = page 1, room measured; 2-4 A4 pages; sections from page 2" (`proposal-buttons.spec.ts`).
  - `template.test.ts` adds `concise` to the proper-noun, price and banned-word scans, and to the call-coverage map.
  - New: `creditCallout.test.tsx`.
  - Nothing weakened beyond the ruled removal. e2e not in CI; B109:265 reports 39/40 locally (the 1 red is main's -111).
- **Words (new; line numbers at `a38f02b`):**
  - `template/concise.ts:11-13` "01 Proposed Solution" / "02 Commercial Schedule" / "03 Delivery, Service & Next Steps"
  - `concise.ts:16` "The proposition"
  - `concise.ts:17` "Proposed fleet and package price"
  - `concise.ts:19` "TOTAL UPFRONT ACQUISITION"
  - `concise.ts:20` "Pricing basis"
  - `concise.ts:25-26` "{edition} pricing. Upfront customer purchase, not a financed monthly rental. Support for the {n}-month term and any software listed are included in the package values; variable usage is additional." **(a pricing-policy claim)**
  - `concise.ts:31` "The proposed devices, coordinated through one service model."
  - `concise.ts:32` "Device stream" / "Solution and quoted inclusions"
  - `concise.ts:36` "{CLASS} · {n} DEVICE(S)"
  - `concise.ts:42` "{edition} price basis • {currency} excluding GST"
  - `concise.ts:45` "Variable usage charges"
  - `concise.ts:46` "No monthly total is stated because usage volumes are not yet confirmed."
  - `concise.ts:48` "Software bundle and credit"
  - `concise.ts:50` "Software element" / "{n}-month value · ex GST"
  - `concise.ts:53-54` "Separate customer Microsoft 365 / Universal Print subscriptions, extended analytics and bespoke integrations are not priced in the package unless expressly documented in the final agreement."
  - `concise.ts:56-57` "Commercial conditions" / "Item" / "Proposal treatment"
  - `concise.ts:62-76`, three condition rows: "Pricing validity" → "{n}-day {edition} pricing; commencement date to be confirmed"; "Invoicing / financing" → "Upfront purchase; separately metered usage charges. Finance terms and recurring fixed base charges are not quoted."; "Standard exclusions" → "Paper, large-format roll media, …"
  - `concise.ts:82` "A practical transition from technical discovery to operational handover."
  - `concise.ts:85-103`, the service heading and three service rows
  - `concise.ts:108-119`, "Implementation sequence" and its four stages
  - `template/cover.ts:20`, sub-line "{packages} | {n}-month managed support" (the edition is removed)
  - `template/rental.ts:51` "Pricing interpretation", kept on the rental book
  - `template/sections.ts:397` "Credit included in this proposal" (W1)
  - `sections.ts:398` "Each credit is already taken off the package price shown, ex GST." (W2)
  - Removed customer sentences: the `sections.ts` pricingCallout ×3, NOT_SPECIFIED ×2, defaultNextSteps ×5, ACKNOWLEDGEMENT_NOTE, defaultBasis ×2; `rental.ts` RENT_NOT_SPECIFIED.
  - Removed editor labels: `ContentEditor.tsx` drops "Proposal basis", "Still to be confirmed (one per line)" and "Next steps (one per line)". The stored values are kept on save.
- **Wrong / notes:**
  1. The branch name `b109/mpscalc-157-proposals-paul-1013` and the commit body of 156 ("Stacked on b109/mpscalc-157-proposals-paul-1013") carry the reviewer's first name. Main has 0 occurrences of "paul". The squash commit message is Tuesday's to write, so keep it out. A PR from 156's branch does not show 157's branch name as its head ref.
  2. `creditRows` treats any amount that starts with "-" as a credit, so a server "-0.00" would print a 0 credit. Edge case only.
  3. "Datasec Solutions Pty Ltd" in the tests is the project owner and is already on main (context lines).
- **OPEN PR.** Kam's words gate comes before any deploy.

### 8. `b101/mpscalc-138-deals-won-lost` → `b101/mpscalc-186-figures-one-read` (top `3b97c65…`; ONE squash PR from 186)
- **Diff:** `web/src/screens/Dashboard.tsx`, `Home.test.tsx`, `e2e/b46-home.spec.ts`, `styles.css:178-183`.
- **Tier:** display only.
  - Deals won shows `closedMonth`/`closedYtd` `count`/`valueExTax`. `docs/API.md:474-475` says those are the Won quotes'.
  - Deals lost shows `figure.lost` count only, with no value (`Dashboard.tsx:62-66`).
  - The period switch is local state and reads nothing new.
  - The tile order changes.
  - 186 adds a comment (`:407-410`) and a test.
- **Scope:** Dashboard plus its tests, home e2e and `.kpi` styles. `styles.css` touches only `.kpi .seg` rules and removes `.won-lost` / `.won`.
- **Tests:**
  - Modified assertions are re-pointed to the new order and labels.
  - The "n won · m lost" line assertions are removed with the line, and replaced by `expect(document.querySelector('.won-lost')).toBeNull()`, new per-tile count/value assertions, a click+keyboard switch test, a "lost missing → fails alone, never 0" test and the 186 one-read/Retry test.
  - Not weakened. Home e2e ran 33/33 locally (B101:47); not in CI.
- **Words:**
  - `Dashboard.tsx:97` "Deals won" / "Deals lost" (replaces "Deals closed")
  - `:101` "Quotes marked Lost in {Month YYYY}." / "Quotes marked Lost since 1 July {YYYY}." (the Won forms already existed)
  - `:163` group name "{Deals won|Deals lost} period" (was "Period")
  - The switch is now buttons (`aria-pressed`). The "n won · m lost" line is removed.
- **Wrong:** nothing.
- **OPEN PR.**

### 9. `b104/mpscalc-143-supplies-label` @ `7a460ab…`
- `InventoryScreen.tsx:20` changes 'Supply' to 'Supplies'. New `classLabels.test.ts`.
- **Words:** "Supplies" (`:20`), shown wherever `CLASS_LABELS` is used (inventory, the BOM picker, the manual form, the purchase result).
- **Note:** 147 (tier 1) stacks on 143. Merging 143 alone is clean; 147 later adds its own increment.
- **OPEN PR.**

### 10. `b104/mpscalc-175-inventory-sources-words` @ `c9fb7f9…`
- `InventoryEndpoints.cs:412-418`: the 503 detail becomes the constant `SourcesUnavailableWords`. New `B104InventorySourcesWordsTests.cs` (it uses `admin@example.test`, a synthetic identity).
- **Words:** `InventoryEndpoints.cs:417-418` "No active source versions are loaded. Import the price books into the reference store (mpscalc-import) and restart, or, with the source store on, an Administrator stages, validates and activates a version (/api/v1/admin/sources)." Byte-equal to main #43's quote-route constant.
- **Note:** this is a second copy of the constant (one in `QuoteEndpoints`, one here). A later edit could make them drift. The test pins this copy's words.
- **OPEN PR.**

### 11. `b102/mpscalc-105-negative-bounds` @ `161def0…` (base `7af91de`) · **TIER-1-SUSPECT**
- **Tier: validation of price inputs.** `QuoteEndpoints.cs:1111-1127` (`NotNegative`) refuses below 0 at create and edit for `fleet[].quantity`, the two page counts, and **`monoClickOverride` / `colourClickOverride` (price inputs, `:1126-1127`)**. Before, negatives reached the engine as Blocking issues.
  - It changes which priced inputs the API accepts. The lane's own brief grades C2 Tier 1 (`2026-10-16_B102_LANE-C2_mps-lane-c2.md:10`). The seat's tier-2 reading is at `B102:51`.
- **Tests:** `QuoteApiTests.InputRange.cs:76-123` adds 5 negative cases (create and PATCH, with "nothing stored") and 3 zero / "-0" accept cases. No removals.
- **Words:** `QuoteEndpoints.cs:1117` "{field} is below 0; enter 0 or more." The field is the JSON path, for example "fleet[1].monoClickOverride".
- **Note:** a stored draft that already holds a negative value can no longer be PATCHed until the value is fixed. That is the intended result. `baseChargeOverride` is not covered (the open question at `B102:62`).
- **HOLD** (QA gate as tier 1, or Tuesday rules the seat's reading).

### 12. Lane A stack `145`→`146`→`148`→`139`→`153`→`185` (top `b100/mpscalc-185-quote-390` @ `7c7ff9f…`; ONE squash PR from 185)
- **Cumulative:** 23 files, +1564 −97. Every file is in lane A's list: `QuoteScreen.tsx`, `bom/**`, `components/InfoHint.tsx`, `infoHintWords.ts`, and their tests and e2e specs.
- **Tier:**
  - 145, 146, 148, 139 and 185 are UI only. `bomModel.ts:71-76` `addCatalogueLines` adds lines with quantities and no pricing. The section-label `maxLength` goes from 132 to 100 (`PurchaseBomEditor.tsx:30`, matching the server limit).
  - **153: TIER-1-SUSPECT.** `components/infoHintWords.ts:24,61,67` hard-code "Typical: $0.0047 a page" / "$0.0470 a page" in code. They are the customer rates of the 16 Oct review quote, shown on the quote screen as pricing guidance.
    - The ticket's acceptance asked for a governed setting, not code (B100:236-238, "Reading, not a ruling").
    - It also puts a real customer quote's confidential sell rates into the repository (comment `:16-23` names the workbook cells).
    - No calculation reads it, so it is borderline. Tuesday to rule.
- **Tests:**
  - New unit tests: `SectionLabel.test.tsx`, `QuoteScreen.endActions.test.tsx`, `InventoryPickerMany.test.tsx`, `InfoHint.test.tsx`, `InfoHintTypical.test.tsx`, `InfoHintPlacement.test.tsx`, `QuoteScreen.narrow.test.tsx`.
  - New e2e: b100-section-label, actions-top-bottom, picker-many, info-hints, quote-390.
  - Pre-existing edits (`e2e/b28`, `b30`, `bom.spec.ts`, `PurchaseBomEditor.test.tsx`) only add `exact: true` and fill the now-blank section label. **No assertion is weakened or removed.**
  - **The break:** `web/e2e/smoke.spec.ts:42` `getByRole('button', { name: 'Save & calculate' })` will match the top button and the new "(end of page)" one, a Playwright strict-mode failure. CI does not run e2e, so CI will be green and the break silent. B100:375 asks Tuesday to add `exact: true`.
  - Testing-library unit tests are not affected (exact full-name match by default; checked: `QuoteScreen.test.tsx`, `callerCan.test.tsx`, `EntraBoot.test.tsx:255` use plain names that do not match the suffixed buttons).
  - B100:87: the three older BOM e2e specs were edited and not run.
- **K-20 check:** `NewQuoteForm.tsx:48-49` at `7c7ff9f` still reads "Rental (monthly)" / "Purchase (upfront BOM)". The file is not in the stack's diff. **CONFIRMED.** After merge, the New quote form and the quote screen (`QuoteScreen.tsx:42` "Finance (monthly)" / "Outright purchase") name one quote type two ways. `git grep` finds no other occurrence of the old words.
- **Words (at `7c7ff9f`):**
  - 145: `PurchaseBomEditor.tsx:27` "Package name, e.g. Devices and supplies" (placeholder)
  - 145: `:28` "Type a package name before saving."
  - 146: `QuoteScreen.tsx:31` screen-reader suffix " (end of page)" on Save draft / Calculate / Save & calculate
  - 146: `PurchaseBomEditor.tsx:32` " (end of BOM)" on "Add section" / "New section class" (`:127`)
  - 146: `:469` end-of-panel "{n} sections · {m} lines"
  - 148: `InventoryPicker.tsx:79` "Tick several items and set a quantity for each, then add them together."
  - 148: `:80` "Choose the device"
  - 148: `:81` "Choose the device for every ticked option."
  - 148: `:82` "Each quantity is a whole number from 1."
  - 148: `:83` "{n} selected"
  - 148: `:84` "Add 1 item" / "Add {n} items"
  - 148: `:164`/`:169` "Select" / "Select {sku}"
  - 148: `:174` "Qty"
  - 148: `:176` "Quantity of {sku}"
  - 148: `:184` "Device for {sku}"
  - 148: `:188` "For {device}"
  - 139: `QuoteScreen.tsx:42` K-20 "Finance (monthly)" / "Outright purchase"
  - 139: `infoHintWords.ts:89` button name "About {topic}"
  - 139: eleven hint texts at `infoHintWords.ts:30` (quote type), `:35` (optional), `:40` (included: "…its cost still counts against the margin."), `:45` (credit), `:50` (section markup), `:55` (section rebate: "…deducted from the margin. It does not change the customer's price."), `:60` (mono click), `:66` (colour click), `:72` (ink rate), `:77` (ink unit), `:82` (from supplies)
  - 153: `infoHintWords.ts:61` "Typical: $0.0047 a page (an A3 colour MFP fleet quoted at standard pricing, October 2026)."
  - 153: `:67` the same with "$0.0470"
  - 185: none
- **Wrong / notes:**
  1. The reviewer's first name appears in code comments, through card ids `mps-paul-review-…`: `infoHintWords.ts:1`, `:18`; `QuoteScreen.tsx:41`; `bom/InfoHintPlacement.test.tsx:1`. Main has 0 such occurrences. The brief's rule is about the client's company name, and this is a personal first name, so it is flagged, not a blocker. Tuesday decides whether the card ids need rewording.
  2. A client company name scan found none (B100:245 reports its own scan as 0). I could not name-check against the client's actual name, because it is only in `Source_Documents/`, which I may not open.
  3. Hints about margin and cost (the included, section markup and section rebate hints) also show to a Seller in the BOM header (included / optional / credit). They contain no figure.
- **HOLD.** Release when:
  - (a) Tuesday rules 153 (keep in code / move to a governed setting / drop the figures);
  - (b) `smoke.spec.ts:42` gets `exact: true`;
  - (c) `NewQuoteForm.tsx:48-49` gets the K-20 words (`QUOTE_TYPE_LABELS` is exported), or Kam accepts two names until it lands;
  - (d) optional: the card-id first name.
  Without 153, 145→139 has no tier issue. But the stack is linear and the squash comes from 185.

### 13. `b102/mpscalc-171-empty-quote` (skipped: conflict only)
- `merge-tree --write-tree 621e3300 1d340ae` (throwaway clone): one conflict in `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, merged-file lines 1167-1182.
  - Main's side: the `SourcesUnavailableWords` const (#43).
  - 171's side: `IsEmpty(...)` and `EmptyQuote(...)` ("Add at least one device.", 171 `:1174`).
  - Both are new class members inserted at the same point above `Stale(...)`, with no overlap in meaning.
- **Resolution is trivial: keep both blocks** (either order), drop the markers, and rebuild.
- Not reviewed for tier. Note for Tuesday: 171 stops calculation and the proposal for an empty quote. That is a rule on when a price is produced, so it deserves the same tier look as 105.

## What this review did not do
- No build, test or e2e run.
- The client's real company name was not checked: it lives only in `Source_Documents/`, which this review may not open.
- No CI or CodeQL was read beyond the inventory.
