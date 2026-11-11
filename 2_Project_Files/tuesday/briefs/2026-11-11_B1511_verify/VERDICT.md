GATE B1511: GO WITH FINDINGS @ e93ef9a on main acd6aec

Tier G2 (independent QA gate), one round. Subject: branch b1511/mps-lane-l4-engine-docs @ e93ef9ac674a86409aa0a11128cc23fad0a5240a (2 commits on base 5cd6002f; docs/ENGINE.md only: row X-33 for MPSCALC-196, row X-46 for MPSCALC-147). Gate run 2026-11-11 19:00-19:20 AEDT. Own clone and worktrees: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s269/gate1502/ (clone push URL set INVALID-NO-PUSH; nothing pushed, no PR opened, nothing deployed). Logs: `logs/dotnet-1511.log`, `logs/dotnet2-1511.log`, `logs/dotnet3-1511.log` in that folder.

## Why GO WITH FINDINGS (one line)
Every sentence of both rows is true of the code at the head (checked line by line below); no test or script reads docs/ENGINE.md; with the described behaviour removed the tests that pin it go red for the right reason; the branch merges cleanly with current main. What is left is two Minors (each row leaves out one condition the code has) and Info.

## Refs read at source
- `git/ref/heads/b1511/mps-lane-l4-engine-docs` = e93ef9ac674a86409aa0a11128cc23fad0a5240a (matches the commission).
- `git/ref/heads/main` = acd6aec03e707a2c6fb30ac9adeccb4230b05764 (the builder's base 5cd6002f is its parent's parent; main moved by the L2 feedback/sources landing, 15 files under src/MpsCalc.Api/{Feedback,Sources} and tests/MpsCalc.Api.Tests, none a docs file and none a file either row cites).
- `git merge-tree --write-tree origin/main origin/b1511/...` rc 0, tree d74ced4c; the merged tree differs from main by exactly the two added table lines (`docs/ENGINE.md | 2 ++`).

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Minor | MPSCALC-147 | **X-46 says the importer reads a sheet's colour-panel section "as options of that sheet's devices", but it adds a panel only for a (device, panel) pair the importer's map does not already hold.** Pairs already mapped are skipped, so a panel the map already lists for a device is not added twice. The row's headline claim (a picked panel is class Option and counts in hardware) is true either way; the omitted condition only matters to someone reading the row to learn which panels become options. Suggested follow-up wording: "...for each of that sheet's devices that the option map does not already pair with it". Not a blocker; the row does not say anything false about class, subtotal or tier. | `src/MpsCalc.Import/PriceBookImporter.cs:656` (`var paired = mapped.Select(...)`), `:703` (`group.Where(d => !paired.Contains((d.Sku, bySku.Key)))`) |
| 2 | Minor | MPSCALC-196 | **X-33's INVALID MARGIN clause is stated without the order of precedence that decides whether it is reached.** The check runs only for a line that is not Included, has no sell override and no catalogue sell price (those branches set the sell first and never read the percent), and whose markup is set (MARKUP NOT SET answers first). The row says "a line on margin on price whose effective percent is 100% or more and whose cost is a number", which is true but reads as if every such line is refused. The row's other part (which member the issue names, X-37) is exact. | `PurchaseCalculator.cs:651` (Included), `:657` (SellOverride), `:662` (CatalogueSell), `:667` (MARKUP NOT SET), then `:673-681` the margin test |
| 3 | Info | MPSCALC-196 | A comment at `tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs:10` still says "X-33 (docs/ENGINE.md row text in the seat's STATUS)". The row now exists in the register, so the comment is stale. The builder disclosed it and left it (Engine tests are not this lane's). A comment-only follow-up. | builder STATUS RESIDUE; `PurchasePageEstimate.cs:10` |
| 4 | Info | MPSCALC-147 | The row's tier clause ("costed at its device's pool tier") is pinned by Engine tests, not by the Api test the builder named. With the Api test alone the clause would pass under a planted fault (MUT-D below: Api row stays green); six Engine rows go red. So the clause is pinned, but by `PurchaseRuleTests` and `PurchaseTierOverrideTests`, which the PR text should name instead of `B104PanelOptionApiTests`. | MUT-D rows below |
| 5 | Info | MPSCALC-147 | "Stored quotes do not move" is left out of the row, as the kit directs: no test pins it. Correct. | builder STATUS Part 2; searched, none |

No Blocker or Major: both rows are in the allowed path (docs/ENGINE.md only), ASCII, no person's name, no B-number, no K-/D- id, no finding or card id, no digit-dot-digit token, no secret.

## (1) Row X-33, every sentence against the code at the head (src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs)
| Sentence of the row | Code | Verdict |
|---|---|---|
| page estimates are checked on every purchase quote, with or without deal usage | `CheckPageEstimates(resolved, reference, issues)` is called unconditionally at `:209`; its summary says so at `:507` | TRUE |
| a page estimate (`monoPagesPerDeviceMonth`, `colourPagesPerDeviceMonth`; any stated value, 0 included) on a non-device line raises Blocking `PAGES ON NON-DEVICE LINE` on `bomLines[n]` | `:518-523`: `item.ItemClass != Device` and `MonoPagesPerDeviceMonth is not null \|\| ColourPagesPerDeviceMonth is not null` (a 0 is "not null"); target `$"bomLines[{l.LineNumber}]"` | TRUE |
| colour pages above 0 on a book device that is mono raise `COLOUR VOLUME ON MONO DEVICE` on `bomLines[n].colourPagesPerDeviceMonth` | `:525-530`: `Source == DistributorBook`, `PrintType == Mono`, `ColourPagesPerDeviceMonth > 0`; target `...colourPagesPerDeviceMonth` | TRUE |
| a line on margin on price, effective percent 100% or more, cost a number, raises `INVALID MARGIN` on `bomLines[n].pricingMethod` when the line's own method chose margin, or on `sections[<id>].pricingMethod` when the section's method chose it (X-37) | `:673` `cost is decimal c && percent is decimal pc`, `:675` `PurchaseMarkup.Method(...)`, `:678` `pc >= 1`, `:680` `field = method == l.PricingMethod ? "{t}.pricingMethod" : "sections[{id}].pricingMethod"`; `PurchaseMarkup.Method` at `:138-139` returns the section's stated method only when the source is Section and the line is MarkupOnCost. Both targets are pinned by `SectionPricingMethodTests.cs:108` and `:111` | TRUE (Minor 2: precedence not stated) |
| any of the three makes the calculation Blocked (`Priced` false, no `purchase` block, the issues listed), so no total, usage figure or deal profit counts a refused page or margin | `:212-218` early return `PurchaseResultOf(false, a, hash, sources, null, issues)` for the three codes; `:1040-1059` sets `Priced = priced`, `Purchase = purchase` (null), `Issues = issues`. The deal-usage and section figures are formed after it (`:219` onward) | TRUE |
| a line whose item is unknown is not checked (UNKNOWN ITEM names it) | `:514-516` `item is null -> continue`; `:636-640` the UNKNOWN ITEM issue returns before the margin | TRUE |
| a counted device, X-25, is unchanged | no Engine code changed (`git diff 5cd6002f e93ef9a -- src` empty); the tests named by the builder pass | TRUE |
| Code column: `CheckPageEstimates`, `PurchaseLineOf`, `CalculatePurchase` (the early return after the lines are priced) | all three exist; the early return follows the line pricing (`:206-218`) | TRUE |

## (2) Row X-46, every sentence against the code at the head
| Sentence of the row | Code | Verdict |
|---|---|---|
| the importer reads a model sheet's colour-panel section as options of that sheet's devices | `PriceBookImporter.cs:97` `deviceOptions.AddRange(ImportPanelOptions(...))`; `:651` the method; `:662` `book.PanelRows(layout, ...)` (`SynnexBook.cs:292`); `:703-706` one `StoredOption` per device of the sheet | TRUE for pairs not already mapped (Minor 1) |
| a panel picked from the catalogue is class `Option` (shown "Customisation") | `PurchaseCatalogue.cs:129` `ItemClass = ItemClass.Option` for every stored option; the word is existing (`web/src/screens/inventory/classLabels.test.ts:20`; `grep -i customis docs/ENGINE.md` hits only the new row, 1) | TRUE |
| counts in its section's hardware subtotal (device + option) by X-23 and X-24 | `PurchaseCalculator.cs:40-46` `ClassGroup`: `Device or Option => 0`; X-23 text in the same file already says "hardware (device + option)" (`docs/ENGINE.md:149`) | TRUE |
| costed at its device's pool tier (R-03: an option takes its device's pool) | `PurchaseCalculator.cs:192-194` `pool = item.ItemClass == Device ? item.TierPool : item.DeviceSku is {} d && reference.TryGetDevice(d, out dev) ? dev.TierPool : null`; R-03 text at `docs/ENGINE.md:151` says the same | TRUE |
| no rule changes: X-23 already groups options with devices | Engine byte-equal to base (`git diff 5cd6002f e93ef9a -- src tests` is empty) | TRUE |
| a manual line keeps the class it is given, so a panel typed in as class Other stays in other | `B104PanelOptionApiTests.A_picked_panel_option_lands_in_hardware_and_a_manual_other_line_stays_other` passes (1/1) and fails when options leave hardware (MUT-C) | TRUE |
| by X-23's cumulative rounding a picked panel can move one cent between the other class subtotals; the section's rounded total is formed as before | derived from X-23's rule (`docs/ENGINE.md:149`); worded "can"; no code claim | TRUE (derived) |
| Code column: `PurchaseRules.ClassGroup`, `PriceBookImporter.ImportPanelOptions`, `SynnexBook.PanelRows` | all three exist (`PurchaseCalculator.cs:40` in `PurchaseRules`; `PriceBookImporter.cs:651`; `SynnexBook.cs:292`) | TRUE |

## (3) Nothing reads docs/ENGINE.md
Search over the whole worktree (positive control: `tools/replica/purchase_bom_replica.py:5` and 11 Engine test files name the file in comments, so the search does hit):
- Every hit under `tests/`, `tools/`, `scripts/`, `web/src` and `src/` is a doc comment or a docstring; with comments filtered out, the only remaining line is a Python docstring (`tools/replica/purchase_bom_replica.py:16`). No test opens the file, no script parses its table.
- `docs/ENGINE.md` table integrity: the two added lines each carry exactly 3 cells (`| Id | Rule | Code |`), ASCII only; ids run X-32 .. X-46 with no gap or repeat; X-33 sits between X-32 and X-34, X-46 after X-45.

## (4) Red-first (a planted fault in a throw-away worktree, built and run with the project SDK; each fault restored byte for byte, `cmp` RESTORED)
| Fault planted | Tests run | At head | With the fault |
|---|---|---|---|
| MUT-A: delete the early-return block at `PurchaseCalculator.cs:212-218` (X-33's "stops before any figure") | Engine `PurchasePageEstimateTests` (6) | 6/6 pass | **5 of 6 red**, `Assert.False() Failure` at `PurchasePageEstimate.cs:63` (`AssertBlockedWithNoFigures`: Priced should be false) |
| same | Api page-estimate rows (4 rows x QuoteApiTests + Entra twin = 8) | 8/8 pass | **8 of 8 red** |
| MUT-B: a stated 0 no longer counts as a page estimate (X-33's "0 included") | Engine `PurchasePageEstimateTests` | 6/6 | 2 of 6 red (`Property_a_calculation_is_blocked_exactly_when_a_line_calls_for_a_page_refusal`, `Page_estimates_on_an_option_line_block_the_calculation_without_deal_usage`) |
| MUT-C: `ClassGroup` stops putting Option with Device (X-46's "counts in hardware") | Api `B104PanelOptionApiTests` | 1/1 | **1 of 1 red**, `Assert.Equal() Failure: Values differ` |
| MUT-D: an option is no longer costed at its device's pool tier (X-46's tier clause) | Api `B104PanelOptionApiTests` | 1/1 | stays green (Info 4) |
| same | Engine `Tier`/`Option` filter (41) | all pass | **6 of 41 red** (`PurchaseRuleTests.Device_and_option_cost_follow_the_pool_tier` x2, `PurchaseTierOverrideTests` x3, `DeviceGroupTests.The_tier_pool_counts_the_extended_devices`), `Values differ` / `Collections differ` |
| MUT-E (spot check of the builder's MPSCALC-158 mutant r2-ii): `Mapping.cs:213` `full.Issues.Select(RestrictIssue).ToList()` -> `full.Issues.ToList()` | Api `B163_1_a_calculation_and_snapshot_stored_with_the_old_part_numbered_text_reach_no_caller_without_internal_metrics` (Theory, 2 cases, x Entra twin) | passes | **4 of 4 red** (`Assert.Equal() Failure: Collections differ`); the builder's "5 of 5 runs" reproduced in kind on one run |

## What I ran (counts)
- Engine.Tests full at head: 743 passed, 0 failed (matches the builder). Import.Tests full at head: 196 passed, 0 failed. Release build of the Api tests project at head: 0 errors (the build is warnings-as-errors).
- Cited tests at head: `PurchasePageEstimateTests` 6/6; the 4 Api page-estimate rows x 2 (plain + Entra) 8/8; `B104PanelOptionApiTests` 1/1; 158 follow-up rows pass.
- Merge with current main: clean (above). gitleaks 8.x over `5cd6002f..e93ef9ac`: 2 commits, no leaks.
- Property scan of the added lines: non-ASCII 0; names (Kam, Kamil, Kreiser, Steve, Peter, Paul, ...) 0; B-number, K-/D- id, "card", "finding" 0; digit-dot-digit 0. Both commit messages carry one attribution line (the builder's own model line), author = committer = the project repo address.

## What I did NOT run
Hosted CI and CodeQL: NOT RUN. The full Api test suite (3466 rows) and the Python job: NOT RUN at the head or on the merged tree (the branch changes one docs file that no test reads; the builder ran both at base and head and reported equal results; I ran the filtered rows above and the whole Engine and Import suites). `scripts/package.sh`: NOT RUN (builder reports rc 0; no packaged file can change from a docs row, and the package script refuses nothing about docs).

## Corrections to the builder's record
1. STATUS Part 2 names `B104PanelOptionApiTests` as the test for the row's tier clause; it does not pin that clause (Info 4). `PurchaseRuleTests.Device_and_option_cost_follow_the_pool_tier` and `PurchaseTierOverrideTests` do.
2. STATUS Part 1 line references (`:209`, `:212-218`, `:518-523`, `:525-530`, `:647`, `:648`, `:673`, `:678`, `:680`, `:1040-1059`) all hold exactly at the head.
3. STATUS MPSCALC-158 note: the two mutants are the builder's own run and are now independently reproduced for r2-ii (MUT-E). r2-vii was not re-run by me (NOT RUN).
4. Nothing in STATUS contradicts the code. MPSCALC-160 clause 6 is not built, as the coordinator's answer rules; the branch touches no PricingPolicy.cs, QuoteEndpoints.cs or test (confirmed: the diff is docs/ENGINE.md alone).
