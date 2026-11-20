GATE B1770: NO GO @ fa71fc8 on main 565ba14

Gate G1 Tier 1, round 1 of 2, independent reviewer for Tuesday. Clock by `date`: start 13:37:13, last read 13:59:38 AEDT 2026-11-20. Load1 never above 11.55 (uptime reads; under 24). Nothing pushed, no PR, no Jira read or write, no deploy, no `az`. Network: `gh api -X GET` (account kamilDatasec), one clone and one fetch with the project deploy key (push URL `invalid://no-push`), and `npm audit` (CI rule 9); `npm ci` came from the local cache (seeded by copying the first gate's cache). The project checkout was not written. Port block 9960-9969: 0 listeners before and after every browser run.

**Why NO GO:** one Major, by the commission's own rule ("a way the oracle can be made blind that the STATUS does not state is at least a Major"). The product change itself is clean: no figure reaches any unpriced render except what the server sent as a code, the priced documents are byte-identical, and every CI step is green on node 24. The Major is in the committed no-price check (oracle P), and the fix is a few lines in the test file. Its real exposure is low, and the Recommendation says why. Tuesday may weigh that, but the rule as written makes it a Major.

## Findings
| Severity | Finding | Recommendation |
|---|---|---|
| **Major** | **The position strip has no left boundary, so oracle P is blind to a figure whose tail equals a line's code, printed in that line's code slot.** `stripCodes` (unpriced.test.tsx:163-166) replaces every `<code> <description>` substring, wherever it starts. When a line's code is the tail of an amount (`0.50` of `1250.50`, `0` of `1234.50`, `0.00` of `57940.00`), a defect that prints the amount where the code goes reads `1250.50 Synthetic widget`. The strip eats the tail (`125Synthetic widget`) and `figuresIn` returns `[]`. Without the strip, `figuresInText` finds it. **Rendered proof:** a gate mutant in the optional-items site (`partCoded(o.unitSellExTax ?? o.code, o.description)`), with the item code `0.50` and the unit price `1250.50`, prints `1250.50` in the unpriced full proposal and oracle P reads `[]`. The control code `SYN-GATE-1` is found (`out/probe2.jsonl`). The STATUS, the commit body and the ADDENDUM state only "a code EQUAL to the amount". **What still catches it:** U10 flags the leftover leaf (`125Synthetic gate option`), so the committed suite goes red in leaf text. Attribute values are read by oracle P only, so there it stays blind. The committed fixtures carry `SYN-*` codes, which are never a figure's tail, so no committed cell is blind today. | In `stripCodes`, strip a code only when the character before it is not a digit, `.` or `,` (the rule `hasToken` already uses). Add a control cell for the tail case: code `0.50`, the amount `1250.50` in its slot, which must be found. Then the stated limit is true as written. Round 2: re-run this gate's probe (`zzprobe.test.tsx`, `zzprobe2.test.tsx`). |
| Minor | The stated limits are narrower than the oracle's real ones. (a) A code that CONTAINS an amount, printed in position (`PN57940.00X`), is also stripped whole and reads clean. The texts say "equal". (b) The whole-dollar rule only covers figures whose cents are zero. A figure with cents printed rounded (`57,941` for `57940.50`), grouped with a space (`57 940`) or abbreviated (`57.9k`) reads clean in oracle P. U10 would flag each as a new leaf. Measured in `out/head-probes.jsonl`. | Say it in the commit body, the PR body and the ADDENDUM's limits: "a code in its own slot is read as data whatever it holds", and "rounded or re-grouped forms of a figure with cents are not read". |
| Minor | **A long unbroken code shrinks the whole printed PDF.** In a seven-package proposal, an unbroken code of 20 characters or more in the first stream card (the narrow grid column) widens the card grid. Chrome then scales the whole document down. The heading height on page 3 reads 16.76 pt with no long code, then 16.61, 15.64, 14.78 and 13.30 pt at 20, 25, 30 and 40 characters, and 11.19 pt at 60 characters (scale about 0.67). The full proposal goes from 14 pages to 13 at 30 and 40 characters, and to 12 at 60. With the two-package `s4` layout, codes up to 40 characters change nothing (12 pages, 16.76 pt). No cell was clipped and no table crossed the page edge on the pages the gate looked at. The base prints no code, so the base is unaffected. The server accepts a manual code of 1 to 60 characters. How long real catalogue SKUs are is UNMEASURED. | Not fixable in this lane (CSS is outside it). Tell the product owner in the ADDENDUM (section 6), and file a follow-up to let a code break inside the stream cards (for example `overflow-wrap: anywhere` on the card items), with a PDF check. |
| Minor | The ADDENDUM does not tell the product owner that a code which LOOKS like a price prints as typed in the unpriced documents. Staff type a manual code as free text (1 to 60 characters), so `$1,234.56` or `4521.10` prints in the customer's unpriced PDF. Measured: the gate's hostile fixture PDFs hold 16 (full proposal) and 14 (short form) price-shaped strings. All of them are inside codes, and the count is 0 once the fixture's codes are removed. | Add one sentence to ADDENDUM section 3 or 6 before the word pack goes to the product owner. |
| Minor | STATUS check (b) says "added source lines: 24". `git diff --numstat` reads +21 (ProposalDocument.tsx) and +5 (OnePager.tsx), which is 26. All 26 are ASCII. | Correct the count in the records. |
| Info | U10's one exception applies to both documents, but only the short form needs it. Mutant M13 (an empty exception list) turns only the short form's U10 red, plus the two cells that test the function. | Optional: scope the exception to the short form. |
| Info | Mutant M3, a no-break space as the separator, leaves U10 green, because `squash` folds the no-break space into a space. 13 site and case cells catch it. | None. |
| Info | The office capability sentence names the software bundle's label without its code (`ProposalDocument.tsx:363`, `OnePager.tsx:297`). It is on the kit's not-sites list, and the reason holds: it is a template sentence. | None. |
| Info | At the head, plant P1 turns 8 cells red and P2 turns 12. The STATUS gives 3 and 4: it measured them at the end of Part 1, before the Part 2 cells existed. | None. |

## Measured rows (each printed by a program in this session)
- **Refs (rule 1):** main 565ba142d4d07b183099eee42c1b73f94242489b at 13:37:23 and again at 13:59:38 (unmoved). `matching-refs/heads/b1767` has 1 row, fa71fc87218120192aa0c68c2c85936978b997d9. Compare: ahead 1, behind 0, 1 commit. Open PRs: 0. Merge: the hook refuses `git merge-tree` outside the coordinator's folder, so it was NOT RUN. The merge base is 565ba142 = main and the branch is 0 behind, so the merge is the head tree 7ebcb8a652e1 (a fast-forward).
- **Scope (rule 1):** exactly 12 paths. `grep -c -v -x -F` over the allowed list reads 0; the control, a planted `web/src/styles.css`, reads 1. Blobs equal at base and head: `ProposalPage.tsx` ba3fe92c, `RentalDocument.tsx` 75d8b9ca, `package.json` b7ceb57f, lock 610a0767, `playwright.config.ts` a7ba5b0a, `ci.yml` 81a1a737, `rentalUnchanged.test.tsx` 2bde8a5a. No change under `*.css`, `template`, `api`, `e2e`, `src` or `docs`. The three words at the head: `ProposalPage.tsx:344` "Customer PDF option", `:346` "Show customer unit and extended prices", `:349` "Show SKUs and quantities only". Non-ASCII lines: ProposalDocument 9 and 9, OnePager 11 and 11, the same byte sequences. The lines holding the multiplication sign (2 and 1) are byte-identical. Added non-ASCII lines: 0 (control U+200B reads 1). CR: 0.
- **The leak (rule 2):** the gate's own detector walks the 40 `Decimal` members of the Proposal schemas, printed from `schema.ts`, less `taxRate` and the rental line `quantity`. It matches raw, `formatMoney`, `formatRate`, `money` and `moneyExGst` forms, integer parts, `$`, and anything money-shaped, over the text (style element included), every text node and every attribute value. Fixtures: the 4 builder fixtures and 4 gate fixtures, a distinctive figure on every price member, and 28 hostile detail codes plus 4 software and 4 optional codes. The hostile codes include `57,940`, `57940`, `57940.00`, `$57,940` (the package total is `57940.00`), `PN57940.00X`, another line's amount `8642.97`, `4521.10`, a padded code, empty, null, absent, blank, a code equal to its description, a 60-character code, `<b>bold</b>`, `A&B "q" 's`, a script tag, a line break, non-ASCII, `-24681.35`, `0.0137`, `(57,940)` and `$1,234.56`. Results:
  - **Unpriced, codes set to null: 0 hits in 16 of 16 renders.**
  - **Unpriced with codes:** every text node equals the codeless render once `<code> ` is removed in code position (unexplained 0 of 16). Attribute lists are identical in 16 of 16, so no code reaches an attribute. Elements `script`/`b`/`i`: 0 against 0. The script code prints escaped (`&lt;script&gt;`). Raw detector hits with codes (up to 53) all come from the amount-shaped codes.
  - **Priced:** with hostile codes, the markup equals the markup with every code null in 32 of 32 renders (default and `priced={true}`). Control: the priced renders have hits in 16 of 16.
  - **Search:** no other way found for the product path to put a figure into an unpriced render. The only blind spot is in the oracle (Major).
- **Plants and mutants (rule 3; the gate's own, each restored and checked by sha256, both trees re-hashed equal to the commits afterwards):**
  - P1 `data-total` on the KPI strip: 8 red (U1/U2 full, U8 radio, U7 full, the oracle-clean cell, 3 numeric-code cells, page cell full).
  - P2 `57,940` in the schedule cell: 12 red.
  - P3 `package price` in the Qty cell: 1 red (U10 full).
  - P4 22% to 23%: 4 red (the short-form goldens).
  - M1 code in the priced scope cards: 7 red (4 full goldens, U10 full, the priced-holds-none cell, the priced page cell).
  - M2 code after the description: 18 red.
  - M3 a no-break space as the separator: 13 red (site cells; U10 green, Info).
  - M4 helper arguments swapped at L2: 8 red.
  - M5 site L3 reverted: 4 red. M5b site L4 reverted: 5 red.
  - M6 the strip widened to remove every digit run: 14 red (U3 both documents, U10 both, the oracle controls).
  - M7 one character of a golden changed: 1 red.
  - M8 a second U10 exception: 2 red (the length cell and the phrase cell). M8 with P3: 3 red.
  - M9 arithmetic on a money value in the added line: 2 red in `noBrowserPricing.test.ts`.
  - M10 trim dropped: 5 red. M11 the short-form cap applied before the codes: 4 red. M12 P1 under M6: 14 red.
  - M13 an empty U10 exception list: 3 red (U10 short and 2 function cells). The exception is needed, by the short form only.
  - **No mutant stayed green.** Logs: `/private/tmp/b1770-gate/out/mut/`.
- **Priced unchanged, goldens true (rule 4), node v24.22.2:** the gate's own captures, default and `priced={true}`, equal the 8 committed files byte for byte, at the base (16 of 16) and at the head (16 of 16). Control: `cmp` of an altered copy gives rc 1. The builder captured on node 26 and the gate's node 24 captures are identical, so no node difference. `pricedUnchanged.test.tsx` and `rentalUnchanged.test.tsx` pass under `TZ=UTC` (14 of 14). The rental documents: `RentalDocument.tsx` blob unchanged; U9 green.
- **Sites (rule 5):** a grep of both files for `.description`, `.label`, `.product`, `.name`, `.sku` and `.code`. Every line-item print is L1 to L6 or a listed not-site: the package `x.label` reads (no code in the contract), the bundle label in a template sentence, the short form's optional-items sentence. Head unpriced text with the codes removed in position equals base unpriced text in **16 of 16** renders (the builder's 4 fixtures and the gate's 4, both documents; text nodes and attributes). Control: a planted character differs. `(included)` and `(credit)` stay last (case cells green; PDF shows `(included)` last). The caps of 4 and 3 and "+n more" are unchanged (M11 red; `detailCell` with a long code still 4 segments).
- **Words and ADDENDUM (rule 6):**
  - Added literals: none is a word (STATUS (c) list confirmed by reading the 26 added source lines: an import path, an existing class name, `''`, one template literal holding one space, the existing `'; '`). No JSX text added.
  - ADDENDUM's 7 before/after lines: each "before" is a text node of the base `s4` unpriced render and each "after" a text node of the head render (7 of 7). Its code counts are true: `s4` 30 and 8, `s4` approved 30 and 8, five 11 and 5, eight 164 and 17. Item rows 15, 15, 5, 68.
  - Its "where no code prints", its not-sites and its two limits are true as far as they go (see the Minor rows for what is missing).
- **No browser arithmetic (rule 7):** the added lines trim and compare strings only. `noBrowserPricing.test.ts`: 61 green. M9 red.
- **Real PDF (rule 8):** Chrome through Playwright `page.pdf`, stub off, read with `pdftotext` and `pdfinfo`, at the head and at the base.

  | Fixture | Full proposal, unpriced (base / head) | Short form, unpriced (base / head) | Full, priced | Short, priced |
  |---|---|---|---|---|
  | s4 | 12 / 12 | 3 / 3 | 13 | 3 |
  | eight packages | 13 / 13 | 3 / 3 | 14 | 3 |
  | gate hostile, 7 packages | 13 / 14 (longer cells) | 3 / 3 | 13 | 3 |

  - Unpriced: 0 figures by the detector for `s4` and `eight`. Hostile: every hit is inside a code; 0 once the fixture's codes are removed.
  - Codes: 15 of 15 in the `s4` full proposal and 8 in its short form; 12 of 12 for `eight`. 0 codes in every priced PDF.
  - Pages looked at (75 dpi PNG): hostile full proposal pages 3 and 7, short form pages 1 and 2, the narrow-card fixture page 3. No clipped cell, no table past the page edge, no orphaned heading seen. The whole-document shrink with long codes is the Minor above.
  - The first review's 13 and 3 were for its own seven-package fixture. This gate's base and head counts are the comparison.
- **Web checks (rule 9), node v24.22.2 / npm 11.19.1:**
  - `npm ci --prefer-offline` rc 0 at both trees (273 packages, from the cache). `npm audit --omit=dev --audit-level=high` rc 0, 0 vulnerabilities. `npm run lint` rc 0.
  - `npm test`: head 149 files and 1712 tests passed; base 148 and 1654.
  - Stub step (port 9961): 260 passed, 17 skipped, rc 0, 4.2 min. Stub-off step: 161 passed, rc 0, 2.5 min.
  - `VITE_MPSCALC_AUTH=entra npm run build` rc 0. `check-bundle.mjs dist` rc 0 (8 files, markers 0/57).
- **CodeQL (rule 10):** `pr_codeql_check.sh`, javascript-security-extended, CLI 2.27.4. Results head 0, base 0. KEPT high+ 0, NEW high+ 0. **rc 0 PASS.** This is a local approximation: the hosted `CodeQL` and `Analyze (javascript-typescript)` checks on the PR head remain the authority.
- **Text (rule 11):** underscore-aware name scan over 650 added lines and the commit message (each `_by_<name>_` control fires).
  - 0 hits for Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Waite, Friday, Tuesday and Wednesday.
  - **Inch: 7.** 6 are in the s4 goldens and 1 in `unpriced.test.tsx`; the only context is `ynthetic 24-inch large-forma`, the unit of the existing fixture description. Not a name.
  - B-numbers, seat or card ids: 0. ASCII in added source and test lines: 0 non-ASCII. Cf characters: 0 (goldens included; their non-ASCII is U+00B7, U+00D7, U+2013, U+2014, U+2022). No sentence of product-owner approval (the only `approv` hit is the fixture name `s4 approved`).
  - Hand rows: `new RegExp(` 0, hand-escape 0, `innerHTML =` 0, `dangerouslySetInnerHTML` 0, `child_process` 0, `eval` 0, `eslint-disable` 0, `waitForTimeout` 0, `.only(` 0, ts-ignore 0, storage 0, URLs or UUIDs 0. One `console.log` prints two counts. `token` appears only as a parameter name of `hasToken`, never written to a file or log.
  - Commit author and committer are the repo identity. Trailer: `Co-Authored-By: Claude Sonnet 5.5`.
- **The ticket (rule 12):** see FOR-RECORDS.

## Builder claims graded
- 12 paths, `ProposalPage.tsx` untouched, the multiplication-sign lines byte-identical: TRUE.
- Goldens captured from the base, `priced={true}` equals the default: TRUE, on node 24 too.
- P2 turned 4 red, not 3: TRUE in kind. U10 sees the planted text; at the head it is 12.
- The `scanText` per-node view was added because `textContent` runs the cells of a row together: TRUE. P2 is caught.
- The split cell (priced holds no code, and its control): TRUE, both present.
- The stated limits: TRUE but INCOMPLETE (Major and Minor above).
- U10 exact, with 1 exception: TRUE; the exception is needed (M13).
- About 600 test lines: TRUE (539 + 77 added).
- Node 26 only: the gate's node 24 numbers are equal (149/1712, 260+17, 161, goldens byte-equal).
- No real PDF: TRUE (the gate printed them).
- `Inch` 7, all `24-inch`: TRUE.
- Counts 30/8, 30/8, 11/5, 164/17: TRUE.
- Head minus codes equals main, for 8 renders: TRUE (the gate measured 16 of 16).
- "Added source lines: 24": FALSE, 26 (Minor).
- The mutants mC1 to mC8 were not re-run as the builder wrote them. The gate's own 18 runs cover the same shapes and all went red.

## TESTED / NOT TESTED / HOW
- **HOW:** a clone under `/private/tmp/b1770-gate/repo` (push URL invalid). Base and head trees were extracted with `git archive` to `/private/tmp/b1770-gate/{base,head}` and re-hashed equal to the commits at the end (734 and 725 blobs, 0 differing, no stray file). The gate's own files (`gatetests/zzgate.test.tsx`, `zzprobe.test.tsx`, `zzprobe2.test.tsx`, `zzoracle.ts` (a sed copy of the builder's oracle), `zzgate.spec.ts`) were copied into those trees only for their runs and parked in `/private/tmp/b1770-gate/quar/` before the CI checks. Mutants were applied by `scripts/mutants.py` with a sha256 restore check. Outputs are in `/private/tmp/b1770-gate/out/`.
- **NOT TESTED:**
  - Other browsers' print dialogs (only Chrome headless `page.pdf`).
  - Every page of every PDF by eye: the gate looked at the 7 pages that carry the codes; the rest were checked by text only.
  - The hosted CI and hosted CodeQL on a PR head (none exists).
  - The merge-tree command (refused by the hook; the fast-forward argument above stands in).
  - The project's heavy-lock files (outside the gate's write folders); heavy jobs ran one at a time instead.
  - Real Api data and real part codes, and the length of real catalogue SKUs (synthetic only).
  - The Jira text of the follow-up ticket for part codes: not read from Jira (no hosted request). Its acceptance check was read from the records seat's frozen kit text (`2026-11-20_B1766_SEAT-R283_mps-records-221.md:267`).
  - Dotnet, python and package jobs (no file of theirs changed).
  - Accessibility of the new text (screen-reader announcement of a code).
