# MPS READY inventory · lanes A, B, C1, C2, D, E, G, J (B100-B104, B107-B109) · for Tuesday
Drafted 2026-10-16 16:19-16:3x AEDT by Tuesday's drafter. Lanes F and H (B105, B106) are excluded: they are B157's gate.
Project: `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator` (written below as `<P>`). STATUS files: `<P>/1_Project_Definition/Briefs/2026-10-16_B1NN_STATUS.md` (cited as `B1NN:<line>`).

**Instruments (every fact below comes from one of these):**
- **Heads:** `git --no-optional-locks -C <P>/2_Project_Files ls-remote origin` at 16:19:37 AEDT; main re-read at 16:27:22 = `621e3300aaae70b32a39edaed653beff7fe45b2d` (unchanged).
- **History:** `merge-base`, `rev-list --left-right --count`, `diff --shortstat` / `--numstat` (read verbs, project checkout).
- **Merge prediction:** `git merge-tree --write-tree` and `commit-tree` in a THROWAWAY `git clone --shared` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/mps-clone`. Push URL is DISABLED, and no write verb ran in the project checkout. The scripts beside it are `sim.sh` and `mt.sh`.
- **CI:** `gh api repos/datasecau/MPS-Commercial-Calculator/commits/<sha>/check-runs` (GET only, project `GH_CONFIG_DIR`, 16:2x) and `gh api …/pulls?state=open` = 0 open PRs.

## BLUF
- **31 READY branches:** 21 tier 2 and 10 tier 1. A 32nd READY line is already merged: `b102/mpscalc-175` @ `d17051d` = main #43 `5d7e481`, because `merge-tree 621e3300 d17051d` gives main's own tree `c1b39c6c`.
- **16 items WAITING.**
- **Every READY sha equals ls-remote (32/32).** No branch moved after its READY line.
- **Main merges by squash.** `5d7e481` (#43), `621e330` (#44) and `0f8ad97` (#41) each have ONE parent (`git log --first-parent --format='%h %p'`).
- **Measured: squash breaks every stack.** Merged one PR per stack member by squash, these conflict:
  - lane A 146…185 on `PurchaseBomEditor.tsx` and 4 e2e specs;
  - lane G 156 on `OnePager.tsx`, `ProposalDocument.tsx` and `proposal-buttons.spec.ts`;
  - lane J 173 on `test_demo_doc.py`;
  - lane E 147 on `classLabels.test.ts`;
  - lane D 158 on 14 files;
  - **B157's own stack, 164 and 165, on `SourceLifecycle.cs`.**

  The same order merged with merge commits, or one PR per stack TOP, is clean. Read the merge-order section before you open the first PR.
- **Two conflicts no order avoids:**
  1. `b102/mpscalc-171` against main's #43 (`QuoteEndpoints.cs:1167-1182`, both insert above `Stale(…)`).
  2. `b103/mpscalc-151` and `b103/mpscalc-174` (contract) against `b103/mpscalc-150` / `-158`:
     - 151: `docs/ENGINE.md`, `PurchaseCalculator.cs`;
     - 174: `web/src/api/generated/SOURCE.txt`, `schema.ts` (plus `openapi.json` and the snapshot once 158 is in).

  Each needs an owner-lane `-r2` branch (no force-push) or a resolution in the PR.
- **One STATUS claim contradicted by measurement:** `B103:221-224` says 151 edits `PurchaseCalculator.cs` and `ENGINE.md` "in other hunks" than 150. `merge-tree` gives textual conflicts in both: the two inserts are adjacent (ENGINE.md `:141-156`, PurchaseCalculator.cs `:60-71` of the merged file).

## Table 1 · READY branches: identity
Head = ls-remote 16:19:37 = the sha on the STATUS's last READY line for that branch (EQUAL for all 31). Base = `merge-base 621e3300 <head>`. b/a = commits behind / ahead of main. CI = GitHub check-runs on the head (`gh api`): `4/4` = ci workflow (dotnet, web, python, package) dispatched by the lane, all success; `0` = none. **CodeQL has run on NO head** (0 CodeQL check-runs anywhere).

| # | Lane | Ticket | Branch | Head (ls-remote) | READY line (EQUAL) | Base (merge-base) | b/a | Parent(s) | Tier (STATUS line) | CI on head |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | MPSCALC-184 | `b100/mpscalc-184-failed-read-guard` | `3434b0e2431cc240185147d6d448e4c8aae7d61d` | `B100:43` | `7af91dec` | 3/1 | `7af91de` | 2 (`B100:43`) | 4/4 |
| 2 | A | MPSCALC-145 | `b100/mpscalc-145-blank-section-label` | `ecc1021168c03dea10e1b339196266a0a51c06a0` | `B100:337` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B100:337`) | 4/4 |
| 3 | A | MPSCALC-146 | `b100/mpscalc-146-actions-top-bottom` | `f37c6ab9994023db9e11f4384b858d15bae8818e` | `B100:342` | `0f8ad97d` | 2/3 | `beb8863` | 2 (`B100:342`) | 4/4 |
| 4 | A | MPSCALC-148 | `b100/mpscalc-148-picker-multi-add` | `d5fa999dee854255d5a6fbc31ec84dd18e382d68` | `B100:347` | `0f8ad97d` | 2/5 | `f0845a1` + `f37c6ab` (merge) | 2 (`B100:347`) | 4/4 |
| 5 | A | MPSCALC-139 (+K-20) | `b100/mpscalc-139-info-hints` | `95136a872177736e4f89f38a5da404d5abc5de06` | `B100:352` | `0f8ad97d` | 2/8 | `94737dd` | 2 (`B100:352`) | 4/4 |
| 6 | A | MPSCALC-153 | `b100/mpscalc-153-typical-rates` | `3729f3780cc3458f3cddf220f6035bcf8c9df4e9` | `B100:357` | `0f8ad97d` | 2/11 | `5f9ae67` + `95136a8` (merge) | 2 (`B100:357`) | 4/4 |
| 7 | A | MPSCALC-185 (quote half) | `b100/mpscalc-185-quote-390` | `7c7ff9fbeee532df69b2ec691e3dffe3477f4a15` | `B100:362` | `0f8ad97d` | 2/12 | `3729f37` | 2 (`B100:362`) | 4/4 |
| 8 | B | MPSCALC-138 | `b101/mpscalc-138-deals-won-lost` | `e6a71fb9cf559a4602d7402c902361b09812b0ce` | `B101:158` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B101:158`) | 0 |
| 9 | B | MPSCALC-186 | `b101/mpscalc-186-figures-one-read` | `3b97c6512351798612ce9eb5d3f7461b1bdbd661` | `B101:159` | `0f8ad97d` | 2/2 | `e6a71fb` | 2 (`B101:159`) | 0 |
| 10 | C2 | MPSCALC-105 (+MPS-5) | `b102/mpscalc-105-negative-bounds` | `161def050fc343bedab9c6ce1cecb02f555d5c7c` | `B102:73` | `7af91dec` | 3/1 | `7af91de` | 2 (`B102:73`) | 0 |
| 11 | C2 | MPSCALC-171 (MPS-6) | `b102/mpscalc-171-empty-quote` | `1d340ae078f6d7c283caab84625250eb309ed602` | `B102:105` | `7af91dec` | 3/1 | `7af91de` | 2 (`B102:105`) | 0 |
| 12 | C2 | MPSCALC-170 | `b102/mpscalc-170-line-identity-audit` | `2a6dcdcdfba5b421c38d060e1298e1d9f9b63d4d` | `B102:143` | `7af91dec` | 3/2 | `cdd451d` | **1** (`B102:143`) | 0 |
| 13 | C2 | MPSCALC-179 | `b102/mpscalc-179-leak-walk-classify` | `ee2fc09d93c4bf0d3bc2b48be99fd0966de6a726` | `B102:169` | `7af91dec` | 3/1 | `7af91de` | **1** (`B102:169`) | 0 |
| 14 | D | MPSCALC-150 (T15) | `b103/mpscalc-150-deal-usage` | `31cd9ea7c9aef90ea447c79e6273b9df3da897d4` | `B103:100` | `0f8ad97d` | 2/2 | `7edf296` | **1** (`B103:100`) | 0 |
| 15 | D | MPSCALC-151 (T16) | `b103/mpscalc-151-software-term` | `e1a9a8214a32630efc60b5d6158b97757d2565f0` | `B103:203` | `0f8ad97d` | 2/1 | `0f8ad97` | **1** (`B103:203`) | 0 |
| 16 | D | MPSCALC-174 (contract half) | `b103/mpscalc-174-feedback-429-contract` | `91040493d511ce1b17840521a2dc974ac5d0c855` | `B103:208` | `0f8ad97d` | 2/2 | `a0af390` | **1** (`B103:208`, label; contract only) | 0 |
| 17 | D | MPSCALC-158 (T23) | `b103/mpscalc-158-target-click` | `c07aef2653c7324005f91de0cb5dff7d33c0c014` | `B103:213` | `0f8ad97d` | 2/4 | `4ee8562` (on `31cd9ea`) | **1** (`B103:213`) | 0 |
| 18 | E | MPSCALC-141 (T06) | `b104/mpscalc-141-coverage-audit` | `8b745389dd37a92bd2defd261436defb939cddb8` | `B104:33` | `7af91dec` | 3/1 | `7af91de` | **1** (`B104:33`; docs only) | 0 |
| 19 | E | MPSCALC-143 (T08) | `b104/mpscalc-143-supplies-label` | `7a460ab43baba6fac140726fcded3d5ae9ea59d6` | `B104:77` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B104:77`) | 0 |
| 20 | E | MPSCALC-147 (T12, K-06) | `b104/mpscalc-147-customisation` | `c61ccbc299c54ff91a593e8f87084decbce35a9a` | `B104:97` | `0f8ad97d` | 2/2 | `7a460ab` | **1** (`B104:97`) | 0 |
| 21 | E | MPSCALC-182 (BL-21) | `b104/mpscalc-182-sydney-date` | `66c0b8abfa086daf86c87daa4ed4d411523304e4` | `B104:117` | `0f8ad97d` | 2/1 | `0f8ad97` | **1** (`B104:117`) | 0 |
| 22 | E | MPSCALC-175 relay | `b104/mpscalc-175-inventory-sources-words` | `c9fb7f9b6071c08d5da0ba5e0401f02d1dbe2548` | `B104:126` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B104:126`) | 0 |
| 23 | J | MPSCALC-180 (BL-19) | `b107/mpscalc-180-hmr-host-guard` | `735d400d2020dbfe8b35bcbe9aef8a558e0dd4ed` | `B107:73` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B107:73`) | 4/4 |
| 24 | J | MPSCALC-178 (DEMO.md part) | `b107/mpscalc-178-docs-drift` | `2e8608bae244052e0cbc84c2e58c6fd2fe855e96` | `B107:107` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B107:107`) | 4/4 |
| 25 | J | MPSCALC-173 (BL-12) | `b107/mpscalc-173-hosted-s4` | `6f41730df9f5ce125202d87aaa2bfcfad03c86c0` | `B107:139` | `0f8ad97d` | 2/2 | `2e8608b` | 2 (`B107:139`) | 4/4 |
| 26 | J | MPSCALC-183 (BL-22) | `b107/mpscalc-183-pre1-in-deploy` | `41af1e3af28ccc620efcd618d3d59050d46a129f` | `B107:168` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B107:168`) | 4/4 |
| 27 | C1 | MPSCALC-136 (T01, K-01) | `b108/mpscalc-136-all-roles` | `30e66e157526679ea1ff2861930a2cd9053899d7` | `B108:222` | `0f8ad97d` | 2/2 | `3e51565` | **1** (`B108:222`) | 0 |
| 28 | G | MPSCALC-157 (T22, K-15) | `b109/mpscalc-157-proposals-paul-1013` | `63d06305f4fd6e2558a7ee6bb35bd58f6412db6a` | `B109:266` | `0f8ad97d` | 2/3 | `7e4ab4b` (merge of main) | 2 (`B109:266`) | 0 |
| 29 | G | MPSCALC-156 (T21, K-14) | `b109/mpscalc-156-credit-callout` | `a38f02bfd5043e7ed1240f87a0a00d1ef902bf22` | `B109:270` | `0f8ad97d` | 2/7 | `4b84bc0` | 2 (`B109:270`) | 0 |
| 30 | G | MPSCALC-111 | `b109/mpscalc-111-narrow-screen` | `1781a4feb49411c68472fd12f77a21a2697b5771` | `B109:274` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B109:274`) | 0 |
| 31 | G | MPSCALC-109 | `b109/mpscalc-109-summary-cut-mock` | `528446f78342b454278327a23787b8b5c9518734` | `B109:278` | `0f8ad97d` | 2/1 | `0f8ad97` | 2 (`B109:278`) | 0 |
| — | C2 | MPSCALC-175 | `b102/mpscalc-175-sources-unavailable-words` | `d17051dfd48285c817adedd39935ade04a1e69bb` | `B102:49` | `7af91dec` | 3/1 | `7af91de` | 2 | **MERGED** as #43 `5d7e481` (same tree) |

Tier notes:
- **Lane C2's brief says "Tier: 1"** (`2026-10-16_B102_LANE-C2_mps-lane-c2.md:10`). The seat graded 105 and 171 as tier 2 itself (`B102:51`, `:78`: no accepted input prices differently). Treat them as tier 2 only if you accept that reading.
- **141 is tier 1 by its READY line, but changes `docs/IMPORTER.md` only** (+34). Its counts come from the real price books, which no gate may open (`B104:24`).

## Table 2 · READY branches: files, order, overlaps, words
Files = `git diff --stat <merge-base> <head>`. For a stack member, "own" = its increment over the stack parent. Overlap = another READY branch changes the same file, not counting its own stack. Conflict = measured with `merge-tree --write-tree` in the scratch clone; every branch alone onto main `621e3300` is CLEAN except #11.

| # | Branch (short) | Files · diffstat | Depends on / order | Overlaps with other READY branches (measured) | Kam words gate: new or changed user-visible sentences (where listed) |
|---|---|---|---|---|---|
| 1 | A 184 | 1 · +24 (`bom/EffectiveMarkup.test.tsx`) | none | none | none (test only, `B100:42`) |
| 2 | A 145 | 7 · +191 −6 (`bom/PurchaseBomEditor.tsx`, `SectionLabel.test.tsx`, e2e `b100-section-label`, `bom`, `b28`, `b30`) | stack 1/6 | none outside stack | 2 sentences, `B100:79-83` |
| 3 | A 146 | cumulative 10 · +483 −61; own 8 · +297 −60 (`QuoteScreen.tsx`, `PurchaseBomEditor.tsx`, e2e ×5) | stack 2/6, on 145 | none outside stack | 7 screen-reader names, `B100:115-120` |
| 4 | A 148 | cum 14 · +842 −65; own 5 · +359 −4 (`InventoryPicker.tsx`, `bomModel.ts`, …) | stack 3/6 | none outside stack | picker words, `B100:147-153` |
| 5 | A 139 | cum 20 · +1342 −97; own 8 · +500 −32 (new `components/InfoHint.tsx`, `infoHintWords.ts`, `UsageRates.tsx`) | stack 4/6 | none outside stack | 12 hint rows + **K-20 rename** "Finance (monthly)" / "Outright purchase", `B100:199-213` |
| 6 | A 153 | cum 21 · +1403 −97; own 3 · +63 −2 | stack 5/6 | none outside stack | 2 "Typical: $0.0047 / $0.0470 a page …" lines, `B100:252-256` (figures from the client's quote, in code: `B100:239-241`) |
| 7 | A 185 | cum 23 · +1564 −97; own 3 · +161 | stack 6/6 (top) | none outside stack | none (`B100:361`) |
| 8 | B 138 | 4 · +270 −134 (`Dashboard.tsx`, `Home.test.tsx`, `b46-home.spec.ts`, `styles.css` `.kpi` rules) | stack 1/2 | none outside stack | 8 rows + 4 look items, `B101:58-74` |
| 9 | B 186 | cum 4 · +287 −134; own 2 · +17 | stack 2/2 (top) | none outside stack | none (`B101:98`) |
| 10 | C2 105 | 2 · +65 −1 (`QuoteEndpoints.cs` `InRange`, `QuoteApiTests.InputRange.cs`) | none | `QuoteEndpoints.cs` with #11: merge clean in either order | "`<field>` is below 0; enter 0 or more.", `B102:66`, `:181` (from `QuoteEndpoints.cs:1117` @ `161def0`) |
| 11 | C2 171 | 2 · +183 (`QuoteEndpoints.cs`, `QuoteApiTests.EmptyQuote.cs`) | **CONFLICTS with main** (#43 `SourcesUnavailableWords` vs 171's `IsEmpty` / `EmptyQuote`, both above `Stale`, merged file `:1167-1182`); needs `-r2` or a PR resolution (keep both blocks) | see #10 | "Add at least one device." shown as "Conflict: Add at least one device.", `B102:98-99`, `:182` |
| 12 | C2 170 | 6 · +390 −28 (`PriceAudit.cs`, `draftModel.ts`, `FleetGrid.tsx`, tests) | none | none | "Line number 1 is used by more than one line. …" (+ plural) and button "Give each line its own number", `B102:129-131`, `:183-184` |
| 13 | C2 179 | 2 · +79 −22 (`Proposal.cs`, `QuoteApiTests.GateB36.cs`) | B103 ADDENDUM-1 item 3: whichever of 179 and lane D merges second re-runs the two guard tests | `Proposal.cs` with #14, #17: merge clean both orders (179→150→158 and 150→158→179) | none (`B102:160`) |
| 14 | D 150 | 16 · +1058 −53 (engine `PurchaseCalculator.cs` +212, `PurchaseInput.cs`, `PurchaseResult.cs`, `Dtos.cs`, `PricingPolicy.cs`, `PurchaseMapping.cs`, `PurchaseValidation.cs`, `Proposal.cs`, `openapi.json`, `API.md`, `ENGINE.md`, generated ×3, 2 new test files) | stack 1/2; contract `0.8.0-b103` | **CONFLICT** with #15 (`ENGINE.md`, `PurchaseCalculator.cs`) and #16 (`SOURCE.txt`, `schema.ts`) in either order; `Proposal.cs` with #13 clean | issue texts `B103:84-90`. **They DO reach a screen:** `PurchaseResultView.tsx:204` @ `621e3300` renders `{i.message}`. This contradicts "none on screen" (`B103:84`) |
| 15 | D 151 | 4 · +103 (`PurchaseCalculator.cs`, `ENGINE.md`, `API.md`, new `SoftwareTermTests.cs`) | none | **CONFLICT** with #14 / #17 (see #14); clean with #16 | 1 issue text, `B103:137-138` (renders as above) |
| 16 | D 174c | 5 · +32 −12 (`openapi.json`, `API.md`, generated ×3) | contract `0.8.0-b103` (same label as 150); lane H's rate-limit server half `150441b` (local, unpushed) waits on it | **CONFLICT** with #14 / #17 (generated files; regenerate with `node web/scripts/sync-contract.mjs <ref>`, `B103:221-224`); clean with #15 | none on screen (docs/API.md text, `B103:144-147`) |
| 17 | D 158 | cum 17 · +1293 −53; own 15 · +248 −13; contract `0.9.0-b103` | stack 2/2 on 150 | as #14 | 2 issue texts, `B103:170-171` (render as above) |
| 18 | E 141 | 1 · +34 (`docs/IMPORTER.md`) | none | `IMPORTER.md` with #20, #21: clean (sequence 143,147,141,182) | none (a docs table) |
| 19 | E 143 | 2 · +15 −1 (`inventory/InventoryScreen.tsx`, `classLabels.test.ts`) | stack 1/2 | none outside stack | "Supply" → "Supplies", `B104:156` |
| 20 | E 147 | cum 8 · +195 −6; own 8 · +180 −5 (`SynnexBook.cs`, `PriceBookImporter.cs`, `ParityProof.cs`, `SyntheticBooks.cs`, `IMPORTER.md`, …) | stack 2/2 on 143 | `PriceBookImporter.cs`, `IMPORTER.md` with #21: clean | "Option" → "Customisation" `B104:157`; `prove` line `B104:160` (operator) |
| 21 | E 182 | 3 · +62 −2 (`PriceBookImporter.cs`, `IMPORTER.md`, new test) | none | see #20 | none |
| 22 | E 175 relay | 2 · +35 −1 (`InventoryEndpoints.cs`, new test) | words copied from #43 (merged) | none | the 503 sentence on `/api/v1/inventory`, `B104:158` (same words Kam sees from #43) |
| 23 | J 180 | 2 · +79 −2 (`web/vite.config.ts`, `web/vite.hostguard.test.ts`) | none | none | none (`B107:71`) |
| 24 | J 178 | 2 · +26 −5 (`docs/DEMO.md`, `test_demo_doc.py`) | stack 1/2 | none outside stack | 4 doc sentences, `B107:86-94` (docs; listed for Kam anyway) |
| 25 | J 173 | cum 5 · +123 −19; own 5 · +97 −14 (`tools/demo/seed.py`, stub, tests, DEMO.md) | stack 2/2 on 178 | none outside stack | tool output + DEMO.md paragraph, `B107:128-132` |
| 26 | J 183 | 3 · +346 −5 (`scripts/deploy-from-ci.sh`, `deploy-package.py`, new `test_deploy_pre1.py`) | semantic link: its test parses `ShowsNothingRanges` in `CatalogueOverlayStore.cs` and `ItemClassDto` in `Dtos.cs`. Lane F's heads leave `ShowsNothingRanges` byte-equal (sha256 of the block `b936ca06…` at `621e3300`, `2d0a6e1`, `58ffb54`). No READY branch adds an item class | none | operator output (PRE-1 lines and STOP messages), `B107:143-145` |
| 27 | C1 136 | 9 · +370 −26 (`EntraBoot.tsx`, `Shell.tsx`, `session.ts`, `scripts/entra_apps.py`, tests, new fake `scripts/tests/fakes_groups/az`) | none (Entra change is FOR KAM, `B108:158-175`) | none | none new; 3 header texts no longer shown to a 4-role user, `B108:88-95`; operator script lines `B108:90-94` |
| 28 | G 157 | 18 · +606 −343 (`web/src/proposal/**`, new `template/concise.ts`, e2e ×3) | stack 1/2 | `OnePager.tsx` with #31, `proposal-buttons.spec.ts` with #30: clean (157,156,111,109 order) | N1-N28, C1-C4 and removals, `B109:52-100` |
| 29 | G 156 | cum 22 · +731 −345; own 8 · +125 −2 (new `CreditCallout.tsx`, `proposal.css`, `sections.ts`, …) | stack 2/2 on 157 | `proposal.css` with #30; `OnePager.tsx` with #31: clean | W1 "Credit included in this proposal", W2 note, `B109:157-158` |
| 30 | G 111 | 2 · +7 −1 (`proposal.css`, `proposal-buttons.spec.ts`) | none | see #28, #29 | none (`B109:272`) |
| 31 | G 109 | 3 · +172 −9 (`OnePager.tsx`, new fixture, test) | none | see #28, #29 | none (`B109:276`) |

**No READY branch here shares a file with B157's eight** (lane F/H): `comm -12` of the two file sets is empty (21 F/H files). Measured semantic links across gates:
- **182 vs 166:** 182 makes the IMPORTER compare validity in Australia/Sydney. B157's 166 validates at the API with the UTC date (`SourceLifecycle.cs:401` @ `7dfa241`, B157 brief Check 4). The two disagree for 10-11 hours a day.
- **140 vs 166:** lane E's waiting 140 needs lane F's `GateB41.cs` expectations changed, and lane F's 166 edits that file (`B104:55-57`; F file list).

## WAITING items (16 by the lanes' DONE lines; MPSCALC-160 appears under A and D as one ticket, and the J row holds two items)
| Lane | Item | Waits on | Where |
|---|---|---|---|
| A | T15 UI half (MPSCALC-150) | lane D 150 merged on main | `B100:370-373` |
| A (unassigned) | MPSCALC-160 (T25, 7% referral rebate start) | Tuesday to give it to lane A; `bomModel.addSection` + label words | `B103:110-114` (lane D WAITING; lane A's brief does not list -160) |
| B | BL-24 dashboard half (MPSCALC-185) | lane A's quote half merged (#7) | `B101:104-108`, `:161` |
| B | MPSCALC-28 Ready to Export UI | lane C2's API half merged + lane D contract | `B101:110-112` |
| C2 | T26 MPSCALC-161 (archive) | lane D contract merge | `B102:195-197` |
| C2 | BL-11 MPSCALC-172 (Won/Lost correction) | lane D contract merge | same |
| C2 | BL-08 MPSCALC-169 (lineMarkups source set) | lane D contract merge | same |
| C2 | MPSCALC-28 API half | lane D contract merge | same |
| C1 | T02 MPSCALC-137 (owner self-approval, audited) | lane C2 (`QuoteEndpoints.cs`, `QuoteEvents.cs`, `Lifecycle.tsx`) + lane D text | `B108:110-129` |
| D | MPSCALC-160 | lane A (see above) | `B103:114` |
| D | MPSCALC-159 (T24) | SKIPPED, K-12 deferred | `B103:116-117` |
| E | MPSCALC-140 care packs (`b104/mpscalc-140-care-packs` @ `a80c91d`, pushed, NOT ready) | lane D `care` key pattern + lane F `GateB41.cs:243,:255` expectations | `B104:59`, `:173-175` |
| E | MPSCALC-142 class "Care pack" | lane D new item class | `B104:61-68` |
| E | MPSCALC-155 class "Staging" | lane D new item class | `B104:99-107` |
| E | MPSCALC-144 large-format items | Tuesday's answer (question below) | `B104:137-141` |
| J | MPSCALC-178 rest (API.md part; IMPORTER.md part) and MPSCALC-187 (own hosted brief) | lane D T15 merge (API.md); lane E (IMPORTER.md); 187 skipped by brief | `B107:95-100`, `:170-171`, `:203` |

Also recorded, no code: BL-27 MPSCALC-188 (`B108:131-138`, a CLARIFICATIONS C-33 paragraph ready at `B108:140-156`). Lane G has 0 waiting, but lists "not built, needs a ruling or design rule": -112, -131, -132, -130, -115 (`B109:285-291`).

## PROPOSED MERGE ORDER (after B157 finishes)
**Headline:** do the tier 2 merges first, all independent, as merge commits or one PR per stack top. 171 waits for an `-r2`. The tier 1 set then goes in after B158/B159 GO: 179 → 150 → 158 → 170 → 151-r2 → 174c-r2 → 143/147 → 141 → 182 → 136.

**Squash or merge commit, decide first (measured, `sim.sh` in the scratch clone):**
- **Squash, one PR per stack member:** what the repo has done so far (single-parent commits on main). It conflicts at every second stack member: 146, 148, 139, 153, 185, 156, 173, 147, 158, and B157's 164 and 165. A squashed stack member keeps the old merge base, so the next member's edits to the same lines (and add/add of files created lower in the stack) conflict.
- **Merge commits** (B157's eight first, in B157's order, then the 31 below = 39 steps): 36 of 39 clean. The only conflicts are 171 (vs main) and 151 / 174c (vs lane D's stack).
- **Squash of stack TOPS only** (165, 173, 156, 186, 185, 147, 158 each as one PR): also clean up to lane D. One PR then carries several tickets, so its Jira and READY-line mapping is Tuesday's to write.

**Order (measured clean in this order with merge commits, on top of B157's eight in its order):**
1. **Tier 2, no dependencies** (Tuesday's review at source + PR CI incl. CodeQL):
   - `b100/184`, `b107/180`, `b107/183`;
   - `b107/178` → `b107/173`;
   - `b109/111`, `b109/109`, `b109/157` → `b109/156`;
   - `b101/138` → `b101/186`;
   - `b104/143`, `b104/175-relay`, `b102/105`.
2. **Lane A stack, tier 2:** `145 → 146 → 148 → 139 → 153 → 185`. Note that 139's K-20 rename leaves `NewQuoteForm.tsx:48-49` on the old words. Merge 139 only together with that fix, or accept two names for one quote type on screen until it lands (`B100:189-191`, `:376`).
3. **`b102/171`**: after an `-r2` branch from lane C2 (keep #43's constant AND 171's `IsEmpty`/`EmptyQuote`), or resolve in the PR. Conflict hunk: merged `QuoteEndpoints.cs:1167-1182`.
4. **Tier 1, after the gates' GO:**
   - `b102/179` → `b103/150` → `b103/158`, re-running `Every_field_of_every_proposal_source_type_is_classified` and `QuoteApiTests.ExportRegistry.cs` on the merged tree (B103 ADDENDUM-1 item 3);
   - then `b102/170`;
   - then `b103/151` as `-r2` rebased on 158 (union of the two adjacent inserts in `ENGINE.md` and `PurchaseCalculator.cs`);
   - then `b103/174c` as `-r2`, regenerated with `sync-contract.mjs` (never hand-merged, `B103:221-224`).

   Alternative: 174c BEFORE 150, which unblocks lane H's rate-limit half sooner. 150 and 158 would then both need regenerating instead of one branch.
5. **Lane E, tier 1:** `b104/147` (on 143, already in), `b104/141`, `b104/182`. Clean in that order.
6. **`b108/136` last.**
   - On the first deploy after it merges, every token holding all four roles loses the act-as switch: `B108:160-166` counts Kam's own account with 4 assignments. That needs no Entra change.
   - The Entra group step is FOR KAM.
   - Owner self-approval (T02) is NOT built, so a four-role owner still cannot approve their own quote until lane C2 builds it.

**Hosted:** none of this changes hosted. MPS hosted is card-per-deploy (lane HOLDS, e.g. `2026-10-16_B103_LANE-D_mps-lane-d.md:23`), and every sentence in Table 2's last column is Kam's at the words gate before any deploy.

## QUESTIONS / OPEN ITEMS FOR TUESDAY (verbatim, with file:line)
**Lane A (B100)**
- `B100:375` "- NEEDS TUESDAY: `web/e2e/smoke.spec.ts:42` add `exact: true` (T11's end-of-page copy makes the substring match two buttons)."
- `B100:376` "- NEEDS TUESDAY: `web/src/screens/NewQuoteForm.tsx:48-49` K-20 words ("Finance (monthly)" / "Outright purchase"); `QUOTE_TYPE_LABELS` is exported."
- `B100:377` "- NEEDS TUESDAY: `web/package.json`, an axe dev dependency, for T04's "axe 0 serious/critical"."
- `B100:378` "- NEEDS LANE B / C2 / E: site-wide hints use `<InfoHint hint=…>`; words go in `web/src/components/infoHintWords.ts` (lane A's file)."
- `B100:379` "- Reading to confirm: lane A counted `web/e2e/{bom,b28,b30}.spec.ts` as the BOM editor's own e2e specs (edited, not run here: they need the API and a store)."
- `B100:380` "- Reading to confirm: T18's figures sit in the words file (code), against the ticket's "governed setting" wording."
- `B100:381` "- QUESTION (T18): the ink rate, $0.70 or $0.90 per "mil", and which unit (in the T18 section)."
- `B100:382` "- BL-24's scoped style could move to `styles.css` or `PriceView.tsx` (not lane A's files)."
- `B100:383` "- BACKLOG `[B100-1]`: a C# feedback test timed out once on CI (re-run passed; lane H's files)."

**Lane B (B101)**
- `B101:125` "- **NEEDS (in the T03 section):** LANE D lost value on the closed figures (optional, Kam's call); LANE C2 `QuoteList.tsx` labels "Deals won"/"Deals lost"; LANE A / Tuesday the K-20 quote-type rename in `QuoteScreen.tsx` and `NewQuoteForm.tsx`."
- `B101:132` "- **Open (for Tuesday):** (1) the 4 T03 look items. (2) `NewQuoteForm.tsx` has no lane owner, and K-20 needs it. (3) Main's dotnet build was red at `e2990622` (NU1902/NU1903) until #42; any branch cut before `7af91de` fails CI's dotnet job until rebased."

**Lane C2 (B102)**
- `B102:15` "**NEEDS LANE A:** rename at `QuoteScreen.tsx:329,330,337`. **NEEDS TUESDAY (no lane owns it):** `NewQuoteForm.tsx:48-49` is in no lane's list."
- `B102:62` "Question for Tuesday, not blocking: should `baseChargeOverride` also refuse below 0 (same reasoning as MPS-5)?"
- `B102:83` "- **Reading (mine; Tuesday's word corrects it):** for purchase, "empty" = no BOM line at all."
- `B102:123` "NEEDS TUESDAY if an e2e on a seeded legacy file is required."
- `B102:207-208` "- **Deferred (BACKLOG.md):** `[B102-1]` stable line id ([B36-N4]); `[B102-2]` three contract sentences (lane D); `[B102-3]` inventory 503 sentence (lane E)."
- `B102:209` "- **Open (questions, `[B102-4]`):** (a) baseChargeOverride below 0; (b) MPS-6 purchase reading; (c) e2e on a seeded `[1,1]` file;"

**Lane D (B103)**
- `B103:57` "**For Tuesday:** the deal's applied rates are NotShown, so a proposal cannot show them yet (the section rates' equivalents are Proposal)."
- `B103:95` "- **NEEDS LANE C2 (`PriceAudit.cs`):** audit `usage.monoClick` / `colourClick` / `inkRate` / `inkUnit` / `usage.supplies` as `clickRates` are"
- `B103:227` "**NEEDS other lanes:** A: MPSCALC-150 UI half, MPSCALC-151 picker, MPSCALC-160, MPSCALC-158 UI. C2: `PriceAudit.cs` audit of `usage.*`. Tuesday:"
- `B103:228` "the deal's applied rates are NotShown (a proposal cannot show them until you say so). Lane H's proposed MPSCALC-176 contract (new routes) was not"
- `B103:229` "assigned to me and cannot land contract-first: `QuoteApiTests.cs:93` asserts the contract's operations equal the mapped routes."
- `B103:235` "Open: the Bicep compiler missing on this laptop (python CI line 7/8 locally); the T16 "warning only" test was not re-measured at base after the"

**Lane E (B104)**
- `B104:51` "- **NEEDS LANE D: add `care` to the catalogue-key pattern** `^(dev|opt|sw|sup|man)_[0-9a-f]{24}$` → `^(dev|opt|sw|sup|man|care)_[0-9a-f]{24}$` in"
- `B104:55` "- **NEEDS LANE F: `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GateB41.cs:243` (`B42-e07`) and `:255` (`B42-e08`) expect `F` (Failed Validation)**"
- `B104:62` "- **NEEDS LANE D:** a new item class `carePack` in `src/MpsCalc.Engine/Input/PurchaseInput.cs:14` (`ItemClass`), `src/MpsCalc.Api/Contracts/Dtos.cs:621`"
- `B104:100` "- **NEEDS LANE D:** a new item class `staging` (engine `ItemClass`, `ItemClassDto`, `PurchaseMapping`, openapi + generated). Also X-23 group `Staging → 3`"
- `B104:137` "- **QUESTION (one line):** where should the 3 large-format lines live: (a) as manual catalogue items an Administrator adds on the hosted inventory (no code;"
- `B104:138` "a data step under its own card), or (b) a new importer input that reads the review spreadsheet's `LFP_BOM` (code, a third source beside the two books, tier 1)?"
- `B104:139` "And do the review quote's E877 supply costs replace the book's for E877 CPP (yes/no)? Default if unanswered: (a), and the book stays the CPP source."
- `B104:179` "- **Merge note for Tuesday:** 140 and 147 both edit `SynnexBook.cs`, `PriceBookImporter.cs` and `SyntheticBooks.cs` in separate methods. Whichever merges"

**Lane J (B107)**
- `B107:194` "## FOR TUESDAY (none blocks lane J)"
- `B107:195` "1. PRE-1's scope (`[B107-2]`): keep B75's ruled subset, or widen PRE-1 to everything `WellFormed` refuses (manual-row fields, overrides, format,"
- `B107:197` "2. Merge order: `b107/mpscalc-178-docs-drift` before `b107/mpscalc-173-hosted-s4` (stacked). The other two are independent of each other and of these."
- `B107:198` "3. The two declared out-of-list test files (§ "How each ticket was checked"); your word corrects them."
- `B107:160` "- **NEEDS LANE E:** when T07/T12/T20 add item classes to `ItemClassDto`, `test_deploy_pre1.py` goes red until `PRE1_ITEM_CLASSES` in"
- `B107:162` "- **NEEDS LANE F:** a change to `WellFormed`/`IsMissingAuthor` (BL-01…BL-06) should name the PRE-1 line it changes; the ranges are guarded by test (b)."
- `B107:178` "and `web/src/screens/NewQuoteForm.tsx` (no lane lists it). **NEEDS LANE A** (and an owner for `NewQuoteForm.tsx`). DEMO.md names neither label."
- `B107:179` "- **K-01 (owner self-approval):** see §2: `DEMO.md:153` and `test_demo_doc.py:48` need a follow-up when lane C1 merges."

**Lane C1 (B108)**
- `B108:96` "**NEEDS (unowned files; not edited):** `web/README.md:36` describes the "Acting as" switch for every Entra user: add "(a user"
- `B108:129` "`WAITS: T02 (MPSCALC-137) on lane C2 (+ lane D contract text); no C1 file holds the rule.`"
- `B108:155` "**Not settled:** whether "self-approval" also frees reject (B108's reading: yes, C-12 bound both); the words any self-approval"
- `B108:158` "## FOR KAM (approval-class: nothing below has been run)" (the Entra group step, `:160-175`; licence P1 UNMEASURED, `:168-171`)
- `B108:201` "- **Not done by me (records are Tuesday's):** `BACKLOG.md` ([B31-ENTRA5] tick on merge, [B08A2-3] sub-bullet, the load row"

**Lane G (B109)**
- `B109:131` "and `web/src/screens/NewQuoteForm.tsx:48,49`. **NEEDS LANE A:** `QuoteScreen.tsx` (its file). **NEEDS TUESDAY (owner):** `NewQuoteForm.tsx` is in no"
- `B109:155` "out. **NEEDS LANE C2 (Proposal.cs) + LANE D (Dtos.cs/openapi.json):** a proposal field for every credit line (label, scope, amount),"
- `B109:200` "- **MPSCALC-115** (rental Devices table parts): `ProposalPage.tsx`, not my file. NEEDS the owner of `web/src/screens/ProposalPage.tsx` (no lane lists it)."
- `B109:285` "- **Waits on Kam (gate):** every word in the T22 words list (N1-N28, C1-C4, the removals) and T21's W1/W2 (cards K-15/K-14:"

**Drafter's own open items (measured above; not in any STATUS):**
1. Choose squash vs merge-commit vs stack-top PRs before the first PR. This also applies to B157's stack.
2. `b102/171` conflicts with main. An owner `-r2` branch is needed, or a PR-side resolution.
3. 151 and 174c conflict with lane D's stack. `-r2` after 158. `B103:221-224` said "other hunks": that is wrong for 151.
4. Lane D's issue texts render on the purchase result screen (`PurchaseResultView.tsx:204`), so they belong on Kam's words list.
5. `NewQuoteForm.tsx` has no owner. Three lanes ask, and K-20 is half-built without it.
6. `B102:59-60` and `:108-110`: lane C2 made Kudu VFS GETs against the HOSTED site (counts only) under `az account show` = tenant `ec01829b…`. Its brief asked for the P-1 count read-only (`2026-10-16_B102_LANE-C2_mps-lane-c2.md:8`), but the HOLDS line says "no Entra or Azure change". These were reads, not changes. Recorded as a fact for Tuesday, not graded.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 16:3x
