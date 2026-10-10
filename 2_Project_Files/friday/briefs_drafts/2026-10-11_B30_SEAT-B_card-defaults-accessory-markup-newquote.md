From Friday (laptop seat), Datasec / MPS Commercial Calculator
# BRIEF B30 · SEAT-B — build the recommended defaults of three open cards: accessory fit warning (G-3 b), effective markup before calculating (G-4 b), New quote form (G-13 a)
**Written:** 06:50 AEDT 2026-10-11 . **Pane:** `Datasec/MPS-B`. Your commission is the newest file in `Briefs/` containing `_SEAT-B_`.
**Seat:** Seat B (Claude build seat), one branch, red-first.
**Report:** `1_Project_Definition/Briefs/2026-10-11_B30_STATUS.md`. No mail key in this project, so your STATUS file is the wrap.
Its last line is exactly one of:
- `READY FOR GATE`, with the head SHA of `b30/card-defaults` read back by `git ls-remote` in the same action as the push;
- `STOPPED: NEEDS FRIDAY` and one question.

**Kam RULED all three cards on 2026-10-11 (live board, Friday tab), each on the recommended option; see AUTHORITY.**

## AUTHORITY
Kam, live board (Friday tab), 2026-10-11, verbatim:
- 06:48:56 *"Decision mpscalc-new-quote-form-1010: a — A short form first (type, term, customer)"*
- 06:49:01 *"Decision mpscalc-markup-precedence-1010: b — Keep the order, show it before calculating"*
- 06:49:08 *"Decision mpscalc-accessory-fits-device-1010: b — Picker + a warning on the quote"*
Friday's reading of G-4 "before calculating": shown after the draft is SAVED and before Calculate is pressed, with a pending marker for unsaved edits (below). This is Friday's reading, told to Kam; his word corrects it.
Same morning, for context only (not this seat's work): 06:48:47 he approved the hosted deploy of main 4f27f55 (a separate deploy seat, MPS-C, runs it; it touches no code), and 06:49:56 ruled the restart check is covered by his Monday test quote.

The three cards (Friday's board, `decisions.json`), verbatim:
- `mpscalc-accessory-fits-device-1010`, recommended **b**: *"Picker + a warning on the quote"*: *"As (a), plus a review warning when a line's accessory fits no device in its section. Engine + contract change, gated like everything else."* (a) is *"The picker shows 'Fits <model>', lists each option once, and offers the section's device options first. A wrong pick can still print."* Default action: *"b: Friday's seat builds it and it goes through a QA gate; nothing is deployed until you have seen the new words and screens."*
- `mpscalc-markup-precedence-1010`, recommended **b**: *"Keep the order, show it before calculating"*: *"Each line shows its effective markup and where it comes from (catalogue or section) before you calculate."* Default action: *"b: Friday's seat builds it through a QA gate; no pricing rule changes; nothing deployed until you have seen it."*
- `mpscalc-new-quote-form-1010`, recommended **a**: *"A short form first (type, term, customer)"*: *"Web only; no record exists until you fill it in."* Default action: *"a: Friday's seat builds the form through a QA gate; nothing deployed until you have seen it."*

## READ WHOLE FIRST
- `Briefs/2026-10-10_B28_STATUS.md`: `## Options for Kam` (G-3, G-4, G-13: what Seat B measured), `## needs-Friday`, and the round-0 and round-1 NEW WORDS.
- `Briefs/2026-10-10_B28_SEAT-B_commercial-readiness-fixes.md` (STANDING LINES / HOLDS, red-proof and STATUS shape) and its ADDENDUM-1. Those lines apply here except where this brief changes them.
- The project `CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md`, and `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md` (I-2, C-12 and decision #6 bear on this work).

## Base and branch
- Base: origin main `4f27f55` (tree `a61a36dd`), per Friday's GitHub API read at 01:2x AEDT 2026-10-11. First action: `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main`. If it is not `4f27f55…`, **STOP: NEEDS FRIDAY**. Do not rebase on your own.
- **What the draft writer saw (read-only, no fetch):** the local `origin/main` was `42d6ecaf7805b746fbf28fe8b988fe76775650fc`, and `4f27f55` is **not in the local object store**. So every `file:line` below was read at `206b82f` (the B28 round-1 head) or at `42d6eca` (B25), **not at `4f27f55`**. B28 (`a168bad..206b82f`) and B25 (`a168bad..42d6eca`) touch disjoint file lists. If `4f27f55` is B28 merged onto `42d6eca` with nothing else, each cited line should hold there too. **Re-check every cite at `4f27f55` before you edit, and list any that moved in STATUS.**
- Branch `b30/card-defaults`, in a fresh worktree `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B30'` (`chmod 700`).
- **Ports:** 6590–6599 (Friday checked ~06:5x: 0 listeners, 0 earlier MPS briefs name them) (Friday names them at firing). Check that they are free before you bind. Never use 5080/5173, or any port named in the B22–B29 briefs or STATUS files (including 6280/6283 (B28) and 6470–6479 (B29)). Playwright and run-demo find your ports through env. Never edit a shared config default.
- **Push the branch only.** Friday opens the PR. He merges after CodeQL, the checks and a QA gate.

## Lanes and tiers
This brief **unfreezes, for B30 only**, three paths that B28 froze or gave to Seat A:
- `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs` (G-3 and G-4 only);
- `docs/API.md` and `docs/api/openapi.json`;
- `web/src/api/generated/**`, regenerated only by `web/scripts/sync-contract.mjs`, never by hand.

Still frozen: `infra/**`, `.github/**`, `scripts/**`, `src/MpsCalc.Import/**`, the root build files and every other engine file.
- If you need any other engine file, that is a **STOP: NEEDS FRIDAY**. A new engine test file under `tests/MpsCalc.Engine.Tests/` is fine.
- If origin carries another seat's open branch, newer than `4f27f55`, that touches any unfrozen path above: **STOP: NEEDS FRIDAY**.

**Tiers:**
- **Tier 1:** the G-3 Review issue (engine + contract) and the G-4 per-line effective markup in the contract (server + I-2 classification).
- **Tier 2:** the web-only parts: the G-3 picker, the G-4 display and the G-13 form.

Tier 1 means:
- red proof one conjunct at a time;
- the I-2 matrix is byte-for-byte unchanged and proved so;
- no internal value is ever derived in the browser;
- **no price, total or applied percent changes on any existing fixture.** Prove that with the engine replica/differential suites (`PurchaseReplicaDifferentialTests.cs`, `PurchaseRuleTests.cs`) green, unchanged.

## PRIOR-WORK CHECK
Before you replace or reword anything, record what existed and why (the ruling, brief or test behind it). At least:
- **The picker.** It lists every inventory row once per key. An option's key is per (device, option) (`PurchaseCatalogue.cs:28`, `CatalogueKeys.Option(deviceSku, optionSku)`). So, in B28's words, *"the picker's 'identical rows' are one option listed once per compatible device, told apart only by the hidden device."*
- **The markup order.** It is documented in `API.md:164-165` (B17). Why the catalogue default exists: the overlay's per-row default (B17 A-4).
- **New quote.** It creates the record at once. B08 task 3 is the Dashboard's origin (`Dashboard.tsx:1`).

## ITEMS (in this order; red test first for each; one commit per item)

### 1. G-3 (b): the accessory picker, plus a Review issue when a line's option fits no device in its section
**WHAT (picker, tier 2):**
- Each option row in the BOM picker shows `Fits <model>`. Take the model from the device row whose `sku` equals the option's `deviceSku`; `deviceSku` is not internal (openapi `InventoryRow.deviceSku`, *"For an option: the device it fits."*).
- An option SKU fitting several devices is listed **once**. When it is picked, the line gets the key for the device in the section; if more than one device fits, the user chooses which.
- Options that fit a device already in the section are offered first.
- Device rows and other classes are unchanged.

**WHAT (engine, tier 1):**
- In the purchase engine, add a `Review` issue to a catalogue option line when its `DeviceSku` matches no catalogue device line in the same section. That includes a section with no device line.
- The issue is not raised for manual lines (they carry no fit data).
- **Do not change the line's or the section's `Status`**: the warning must not move readiness, totals or approval. If you find it must, **STOP: NEEDS FRIDAY**.
- Say in STATUS which device lines count (optional? credit?) and which string comparer you used, and why. The catalogue keys use `StringComparer.Ordinal`; B25 fixed a case-sensitivity defect elsewhere, so state the choice.
- **Contract:** document the new issue `code` in `API.md` beside the purchase rules. `Issue.code` is a free string (openapi `Issue`: `"code": { "type": "string" }`), so no schema change is expected. If you make one, regenerate with `sync-contract.mjs`.

**WHERE:**
- The picker: `web/src/screens/bom/InventoryPicker.tsx:27-63` (`InventoryPicker`; the row button is at `:50-56`). It is called with no section context at `web/src/screens/bom/PurchaseBomEditor.tsx:281-289`. `picking` holds the section id (`:44`, `:269` `setPicking(s.id)`), so pass the section's lines in.
- **`listDeviceOptions`:** B28's option (a) names it. It is the **rental** catalogue call, `GET /catalogue/devices/{sku}/options` (`web/src/api/client.ts:69,141`). It is used today only by `web/src/screens/FleetGrid.tsx:251`, and it returns `CatalogueOption` (`optionSku`, `description`…), which has **no inventory `key`**.
  - A purchase line needs the inventory `key` (`addCatalogueLine(draft, picking, row.key)`, `PurchaseBomEditor.tsx:286`).
  - So the draft writer expects the ordering to come from the inventory rows' `deviceSku`, not from `listDeviceOptions`. Confirm or correct this at source, and say which you used.
- The Review issue: `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs`.
  - `PurchaseLineOf` is at `:228`.
  - Existing per-line Review issues are at `:300` (NO PRICE), `:304` (NO COST) and `:309` (SOURCE REVIEW).
  - The lines are resolved at `:64` and mapped at `:77`. `TierOf` already reads `item.DeviceSku` at `:71-72`.
  - Raise the fit check where all of a section's resolved lines are visible (after `:64`), not inside `PurchaseLineOf`, which sees one line.
- Issues are shown on the quote screen at `web/src/screens/bom/PurchaseResultView.tsx:160-164`. `CalculationDto.Issues` is classified `I` in `src/MpsCalc.Api/Quotes/Proposal.cs:68`, so it does not print on the proposal.

**PROVE (red-first):**
- An engine test with a SYN- option line whose device is not in its section gets exactly one Review issue with the new code. The same option, with its device in the section, gets none. A manual line gets none. Totals and statuses are byte-equal with and without the issue.
- Web: the picker shows `Fits <model>`, one row per option SKU, and the section's device options first.
- **Tampers (each must go RED):**
  - the fit check compares against every section, not the line's own;
  - the issue is suppressed;
  - the de-duplication is removed (rows listed per key again);
  - the ordering is reversed.

### 2. G-4 (b): keep the order; show each line's effective markup and its source before calculating
**WHAT:**
- The pricing order stays exactly as it is. Each BOM line shows, **for a caller with internal metrics only**, the percent that will apply and its source, before Calculate is pressed. The sources, in the documented order, are:
  1. sell override;
  2. catalogue sell price;
  3. catalogue default markup;
  4. section markup;
  5. server default;
  6. not set.
- Steps 1 and 2 carry no percent. Show the source and no number.
- The percent and source must come **from the server**: one server-side resolver that the engine itself uses. Extract the precedence from `PurchaseCalculator.cs:246` into one function that both call. The precedence must never be re-implemented in the browser. (The browser holds `InventoryRow.defaultMarkupPercent` and the section's `markupPercent`, but deriving the winner there is the derivation tier 1 forbids.)
- **Contract shape:** your choice, with your reasoning in STATUS. The draft writer's suggestion is an internal-only per-line field on the quote response (for example `lineNumber`, `effectiveMarkupPercent`, `markupSource`), recomputed on every GET and PATCH, and null or absent without internal metrics.
  - A new DTO property must be classified in `ProposalAllowList.Sources`. `tests/MpsCalc.Api.Tests/QuoteApiTests.Showcase.cs:488-492` fails on an unclassified one, and that is the intended guard.
  - The I-2 matrix must stay unchanged: a Seller-only body and response carry 0 internal fields (the B18 B3 check).
- **"Before calculating" means after the draft is saved.** If a line's source would change on an unsaved edit, the display must show that it is pending (for example "Save to see"). It must never show a stale percent as current.

**WHERE:**
- `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs:246`, `decimal? percent = item.OverlayMarkupPercent ?? section.MarkupPercent;`. The sell order is at `:249-292` (included → sell override → `OverlaySell` → percent). The applied percent is recorded at `:321`.
- `docs/API.md:164-165` (at `42d6eca`), verbatim: *"Unit sell, in order: the line's `unitSellOverride`; the catalogue row's overlay `unitSell`; else from cost with the row's overlay `defaultMarkupPercent`, or the section's percent, by the line's method."* Add the new field there. Do not reword the order.
- The server default for an absent section markup reaches the engine through `PurchaseMapping.ToEngineInput(..., defaults.PurchaseMarkup)` (`src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:220`; `PricingDefaults.cs:11`).
- Today's post-calculation display is `web/src/screens/bom/PurchaseResultView.tsx:53` (`internal('Applied %', 'appliedPercent', pct)`), mapped at `PurchaseMapping.cs:123` and nulled for non-internal callers at `:199`. Keep it.
- The editor's section markup field is at `web/src/screens/bom/PurchaseBomEditor.tsx:120-124`.

**PROVE (red-first):**
- With SYN- rows, cover all six sources: one line where the catalogue default (15 %) beats a section at 16 %, and one line each for the other five. Each shows the right source and percent before Calculate. After Calculate, `appliedPercent` equals the shown percent for every line (the server field and the engine agree by construction; prove it on the fixture).
- A Seller-only response carries none of the new fields.
- **Tampers (each must go RED):**
  - swap `??` to the section first in the shared resolver: every price test goes red too, which proves the engine and the display share one function;
  - make the field non-internal (unclassified, or `P`);
  - compute the source in the browser instead;
  - show the percent while an unsaved edit is pending.

### 3. G-13 (a): a short New quote form before any record exists (web only)
**WHAT:**
- "New quote" opens a short form: type (rental / purchase), term (from `TERMS`) and customer (optional, 0–200 characters, as the contract allows).
- No `createQuote` call is made until the user confirms. Cancel creates nothing.
- The form's defaults equal today's (rental, 60 months), so nothing changes silently.
- **No API or contract change.** `QuoteDraft` already carries `quoteMode` (`rental`/`purchase`), `customer` (string, max 200) and `assumptions.termMonths`.
- For purchase mode, `fleet`, `hardware` and `software` must be empty (openapi `quoteMode`: *"fleet, hardware and software must then be empty (400 otherwise)"*). `newDraft()` already sends them empty.

**WHERE:**
- `web/src/screens/Dashboard.tsx:44-55` (`create()`). At `:48`: `const q = await api.createQuote(newDraft());`. The button is at `:79-82` (Seller only).
- `web/src/app/defaults.ts:17-26` (`newDraft()`; `:21` is the assumptions line with `termMonths: 60`). `TERMS` is at `:4`.
- `quoteMode` and `customer`: `docs/api/openapi.json:546,551` (at `42d6eca`). Read only; no edit for this item.

**PROVE (red-first):**
- Clicking New quote makes 0 `createQuote` calls until the form is confirmed. Cancel makes 0. Confirm makes exactly 1, with the chosen mode, term and customer in the body.
- A purchase choice lands on the quote in purchase mode. A Seller-only identity sees the same form. A non-Seller identity still sees no button.
- **Tampers (each must go RED):**
  - call `createQuote` on open;
  - drop the chosen term;
  - default the type to purchase.

## Test Evidence (each run with `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (re-measure the base in your own base worktree at `4f27f55`; B28 reported 292/292 web and 826/826 .NET at its round-1 head, not at main, so do not trust those numbers):
  - web: `npm run lint`, `typecheck`, the full `test` suite, `build`;
  - .NET: the full suite, a Release build `--no-incremental` with 0 warnings, and 0 vulnerable packages.
- **Contract:** `sync-contract.mjs` run once after the doc change. `web/src/api/contract.test.ts` is green. The diff of `web/src/api/generated/**` is exactly the new field(s).
- **Red-proof table:** for each item, list the term, the tamper, `RED n/m` on the full suite, and the restore, checked by sha256. After every restore, touch the file and build `--no-incremental`.
- **Playwright** for the picker, the BOM line display and the New quote form, live and stub. Use SYNTHETIC data only (SYN- names, synthetic prices) and mask money cells in screenshots.
  - Evidence goes in `Briefs/2026-10-11_B30_evidence/` (folder 0700; files 0600).
  - `smoke.spec.ts:34` failing in stub mode is pre-existing (B28 Deferred). Report it; do not count it as yours.
- **B17 leak + secret scan** over `git diff origin/main...HEAD` and `git log --format=%B origin/main..HEAD`: counts only, with a planted control that fired. Never print the avoid list.
- **No infra change:** `git diff --numstat 4f27f55 -- infra scripts .github` is empty. `git diff --name-only 4f27f55 -- src/MpsCalc.Engine src/MpsCalc.Import` lists `PurchaseCalculator.cs` and nothing else.

## NEW WORDS (verbatim; Friday shows Kam before any deploy)
Every user-visible string you add or change goes in STATUS in this table: old → new, with `file:line` at your head. Expect at least:

| Where | Old | New |
|---|---|---|
| picker option row (G-3) | — | `Fits <model>` (yours, verbatim) |
| picker device choice when several fit (G-3) | — | yours |
| the Review issue message (G-3) | — | yours (it shows on the quote screen) |
| effective markup and source labels, plus the pending text (G-4) | — | yours, one row per source |
| the New quote form's title, labels, buttons and help (G-13) | — | yours |

Keep the words plain and short. Never copy wording from the example document.

## STATUS sections
- BLUF;
- PRIOR-WORK CHECK;
- Commits;
- Test Evidence;
- Red-proof table;
- Tier-1 conditions;
- Modified pre-existing tests (before → after, why);
- NEW WORDS;
- UNMEASURED;
- `## NOT DONE / NOT COVERED`, as prominent as the evidence;
- needs-Friday;
- Leak + secret scan;
- processes started / stopped;
- worktrees and files left.

## Time-box
**About 3 h.** If you run short, finish in this order: G-13 (smallest, web only), then G-3, then G-4. List what is left as **NOT DONE**, never half-merged. Each item is its own commit.

## UNMEASURED (by the draft writer)
- **`4f27f55` and tree `a61a36dd`:** not verified. Neither is in the local clone, and no fetch was allowed. Every cite was read at `206b82f` or `42d6eca` (see Base and branch).
- Whether `4f27f55` contains anything beyond B28 merged onto `42d6eca`.
- Whether any other seat holds an open branch on `PurchaseCalculator.cs`, `docs/API.md`, `openapi.json` or `web/src/api/generated/**` now. B28 STATUS needs-Friday 3 says *"The engine/contract options are Seat A's."* This brief gives them to Seat B. Friday confirms the lane at firing.
- Whether a Review issue changes submit or approval readiness anywhere. The draft writer saw the section status rule at `PurchaseCalculator.cs:340-343` (any non-Ok line status → REVIEW REQUIRED), which is why item 1 forbids touching `Status`.
- The test counts at `4f27f55` (the seat measures them).
- Ports for this run (`6590–6599 (Friday checked ~06:5x: 0 listeners, 0 earlier MPS briefs name them)`).

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- No deploy, no Azure, no setting change; nothing to any human.
- Never delete; quarantine.
  - Quarantine to `.tools/_quarantine/2026-10-11_B30_<what>/` (0700) and say so.
  - Never edit a running script.
- SITE HOLD: none of the four store path settings changes; ReferenceStorePath stays a regular file.
- No pricing rule changes. No price, total or applied percent moves on any fixture (G-4 is a display of the existing order).
- **No real client data anywhere.** The price books and the example quote are CONFIDENTIAL; report counts only. That covers code, tests, fixtures, screenshots, commit messages and STATUS. Price-book values never leave `.local/pricebooks/`.
- **Own worktree and own ports.**
  - Allowed: `fetch`, `worktree add`, commits and pushes on your own branch.
  - Never `checkout` or `switch` in `2_Project_Files`.
  - Never `gc`, `prune`, `worktree remove`, `branch -D` or force-push.
  - No merge, no Jira write.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate` and the shared `VBCSCompiler` are Friday's.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`. Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero has a positive control that fired.
- **Records:** write only your STATUS and your evidence folder. `CLAUDE.md`, `BACKLOG.md`, `history.md` and Jira are Friday's.

## End
The last line of `Briefs/2026-10-11_B30_STATUS.md` is one of these:
- `READY FOR GATE`, with the head SHA of `b30/card-defaults` read back by `git ls-remote` in the same action as the push;
- `STOPPED: NEEDS FRIDAY` and one question.
