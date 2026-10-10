From Friday (laptop seat), Datasec / MPS Commercial Calculator
# BRIEF B28 · SEAT-B — fix the walkthrough's bugs and UX defects before Kam's own test quote (G-2 and G-5 first)
**Written:** 2026-10-10 ~22:40 AEDT (DRAFT for Friday). **Pane:** `*MPS*-B`. Your commission is the newest file in `Briefs/` containing `_SEAT-B_`.
**Report:** `1_Project_Definition/Briefs/2026-10-10_B28_STATUS.md`. No mail key in this project, so your STATUS file is the wrap.

## BLUF
Gate B26 walked a quote of the example's complexity end to end on `a168bad`. It priced correctly, but it found 19 gaps
(`Briefs/2026-10-10_B26_STATUS.md` §5, G-1…G-19). Fix the ones that are **bugs or clear UX defects** on ONE branch, red-first.
Leave the product decisions to Kam: for each one, write a 3-line options note with what you measured. End on `READY FOR GATE`.

## AUTHORITY (Kam, live board, verbatim)
- 2026-10-10 21:38:01: *"The test I will run is to do another quote (similar complexity to the one I provided )  please get the system so it's as close to commercially ready as possible"*
- 21:32:57: *"Don't stop. The hpsm poc and calculator are priorities…"*

**Friday's reading:** Kam will build a second quote by hand. Every defect he would trip over on the way to the proposal is in scope.
A change that alters what the product *does* (approval policy, pricing precedence, data model) is not in scope.

## READ WHOLE FIRST
- `Briefs/2026-10-10_B26_STATUS.md`: §4 walkthrough, §5 gap table (with `file:line` at `a168bad`), §6 known items.
  Friday re-read every `file:line` cited for G-1…G-17 at `a168bad` (2026-10-10 22:3x) and **all matched**. The gate's "fix shape"
  is a proposal, not an order: where you differ, say so and why.
- The project `CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md` and `Questions_and_Answers/00_QUESTIONS_FOR_KAM.md`
  (C-05, C-12, I-2, Q-12 bear on this work).
- Template for these standing lines: `Briefs/2026-10-10_B18_SEAT-B_web-inventory-bom.md` (STANDING LINES, HOLDS, STATUS
  shape). Those lines apply here except where this brief changes them.

## Base and branch
- Base: main `a168badaa4a88fcbbd91e7d1350cd45320969ce9`. First action: `git -C 2_Project_Files fetch origin` and
  `git ls-remote origin refs/heads/main`. If it is not that sha: **STOP: NEEDS FRIDAY**. (If B25 has merged meanwhile, main has moved. Stop and ask anyway; do not rebase on your own.)
- Branch `b28/commercial-readiness-fixes`, in a fresh worktree
  `'/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/wt-B28'` (`chmod 700`).
- **Ports: API 6280, web 6283** (Friday checked both free at 22:35). Check again before binding. Never use 5080/5173, or any
  port named in the B22–B27 briefs or STATUS files (5183, 5580, 5780–5783, 5880–5889, 5960–5969, 5990–5999, 10022–10082).
  Playwright and run-demo point at your ports through env, never by editing a shared config default.

## PARTITION (B25 · Seat A is open in parallel)
Seat A's branch `b25/overlay-gate-findings` (head `b0ff946…` at 22:3x) touches the paths below. **Seat B must touch NONE of them,
even for a one-line fix.** Write any such need as "needs Seat A / Friday" in STATUS and carry on.
- `docs/API.md`, `docs/api/openapi.json` (the contract; **so no contract change in B28**)
- `src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`, `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs`
- `tests/MpsCalc.Api.Tests/OverlayGateFindingsTests.cs`
- `web/src/api/generated/**` (and do **not** run `sync-contract.mjs`)

Everything else in `web/src/**`, `web/e2e/**` and `src/MpsCalc.Api/Quotes/**` is yours. Also yours: new test files under
`tests/MpsCalc.Api.Tests/` (new file names only). Before READY, the gate checks that
`git diff --name-only origin/main...HEAD` has no path in common with Seat A's list.
Frozen as before: `infra/**`, `.github/**`, `scripts/**`, `src/MpsCalc.Engine/**`, `src/MpsCalc.Import/**`, the root build files.
An engine or importer change is a **STOP: NEEDS FRIDAY**.

## Tiers
**Tier 2 (UI / text)** for everything except **G-2 and G-5, which are tier 1**: G-2 touches role-gated controls, and G-5 touches the
proposal data path. Tier 1 means:
- red proof one conjunct at a time;
- the I-2 matrix is unchanged and proved so (below);
- no internal value is ever derived in the browser.

## ITEMS (in this order; red test first for each)
1. **G-2 (Major, tier 1): Seller sees no markup / rebate / manual-line controls, and no reason why**
   (`web/src/screens/bom/PurchaseBomEditor.tsx:238`, the `pricing &&` gate).
   - Add a one-line hint in the Purchase BOM region when the caller lacks internal-metrics. It names the persona needed.
   - If the signed-in identity **holds** that persona, add a one-click switch. Use the existing act-as path in
     `web/src/auth/actAs.ts` (`offeredPersonas`) and the shell's switch; never add a new one.
   - **Do NOT widen permissions.** The I-2 matrix (`web/src/auth/pricePolicy.ts`, and the server's policy) stays byte-for-byte.
   - Red-proof: a Seller-only identity sees the hint and **no** switch. A Seller-only request body has 0 internal fields (the B18 B3
     check). After the switch, the controls appear only because the server's `/me` grants them.
   - Planted control: force-render the controls for a Seller; the test must go RED.
2. **G-5 (Major, tier 1): saving proposal content voids the calculation**, and the page shows 409 `PROPOSAL_NOT_AVAILABLE`.
   - Friday's reading of the cause (confirm or correct it at source):
     - `ContentEditor.tsx` (~`:116-134`) PATCHes the whole draft through `updateDraft`, which bumps the revision.
     - The proposal GET refuses when `calc.Revision != v.Revision` (`src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:530-532`).
     - On the error, `ProposalPage.tsx:164-166,173,186` sets `proposal` to null, so the editor and the document fall into the rental
       branch's ErrorBox.
   - Fix so that saving text keeps the document. Either content stops voiding the priced revision, or the page re-calculates
     transparently and says so. You choose, with your reasoning in STATUS.
   - Constraint: no contract change, because `docs/API.md:129,134` and `openapi.json` belong to Seat A. A server-side fix whose
     documented behaviour would then differ from `API.md` is a **STOP: NEEDS FRIDAY** with your proposed doc text.
   - If you re-calculate, a price that changed since the last calculation must be **visible** (a notice), never silent.
   - Red-first: save content → document and editor still present. Also red-prove that a draft whose *pricing* inputs changed
     still answers 409 (the guard must not be weakened).
3. **G-6 (device search)** (`InventoryPicker.tsx:10-11`):
   - AU/US spelling: "colour" matches "color".
   - Synonyms: "multifunction" and "MFP" match each other.
   - Show format, colour and speed on device rows **only if the data carries them**. Measure the count of rows that do, in
     `InventoryRowDto` and the stub. If 0, say so and skip; no new field.
4. **G-7 (customer-facing description):**
   - Make the description editable per catalogue line **on the quote**, not in the catalogue.
   - The proposal never prints a bare model code where a description exists.
   - At `a168bad` `PurchaseBomLineDto` has `Note` and no description field. **Do not repurpose `Note` and do not add a contract
     field.** If the editable description cannot be done without one, build only the "never a bare code" half (sections 3, 5, 11),
     and write the field proposal under needs-Friday.
5. **G-8:**
   - The default section label should not repeat the class (`PurchaseBomEditor.tsx:72`; the §3 heading shows "<class> – <class>").
   - Add a hint that labels are customer-facing.
6. **G-9:** clear the "Reason for price changes" box after a successful save, and only then.
7. **G-10:** the change log names the item. Render `InventoryAuditEntry.key` → item code (`AuditList.tsx:11`), with human labels
   and percentages (0.16 → 16 %). Same for the quote price audit (`web/src/screens/bom/PriceAudit.tsx`), where the data allows.
8. **G-11:** outcome cards accept `Title: bullet; bullet` (`ContentEditor` + `ProposalDocument.tsx:251`). A line with no colon prints
   as today (backward-compatible; red-prove that too).
9. **G-12:** group section 3 by element, each with its own treatment text. **Do this ONLY if it needs no template text Kam has not
   seen** (`template/sections.ts:433`, `IN_PACKAGE_TEXT`). Otherwise leave it and say why under NOT DONE.
10. **Polish:**
    - **G-14:** the GST tooltip is stale (`QuoteScreen.tsx:323`; also the comments `app/defaults.ts:6` and `saveDraft.ts:5`, since
      C-12 fixed F-13).
    - **G-15:** the markup placeholder says "server default" when none is set (`PurchaseBomEditor.tsx:90`).
    - **G-16:** "credit (credit)" is printed twice (`ProposalDocument.tsx:374`; `ProposalDocument.test.tsx:59` changes: list it).
    - **G-17:** "Manual" appears twice (`InventoryScreen.tsx:227`).
11. **G-18:** on the internal screens, show a "unit rounded for display" note. Do not change the Q-12 rounding.
12. **G-19: skip.** It needs a new input (a caption field). Say so under NOT DONE.

## OUT OF SCOPE: product decisions (Friday cards them for Kam)
For each one, add a **3-line options note** in STATUS (`## Options for Kam`): the options, what you measured, and your
recommendation. Build nothing.
- **G-1** (approver identity: Kam alone cannot approve his own quote). Options (a)–(d) are in B26 §5. Measure only from code and
  docs; nothing on Azure.
- **G-3** (accessory ↔ device compatibility). **Measure from the confidential price books by absolute path, counts only:**
  - does either book carry a compatibility field, and in which sheet or column (name it; no values)?
  - how many accessory rows map to ≥1 device;
  - how many map to none;
  - how many appear as duplicates (the same option on several rows).
- **G-4** (which markup wins: the catalogue default or the section). Today `PurchaseCalculator.cs:246` lets the catalogue default
  win, as documented in `API.md:164-165`.
- **G-13** (create-before-save: "New quote" creates a Rental / 60-month record at once).

## NEW WORDS (verbatim list)
Every user-visible string you add or change goes in STATUS under `## NEW WORDS (verbatim)`: old → new, with file:line. That covers:
- hints and notices;
- placeholders;
- tooltips;
- labels;
- the G-5 recalculation notice.

**Friday shows Kam the list before any deploy.** Keep the words plain and short. Never copy wording from the example document.

## Done means
- **Tests, at the head vs the base:** web `npm run lint`, `typecheck`, the full `test` suite (base **235/235**) and `build`; the
  .NET full suite (base **820/820** at `a168bad`, per B23/B24), Release build with 0 warnings, 0 vulnerable packages. Re-measure
  the base in your own base worktree; do not trust these numbers.
- **Red-proof table:** for each fix, the term, the tamper, `RED n/m`, and the restore checked by sha256. After every restore,
  touch the file and run `--no-incremental` (B22's stale-build incident).
- **Playwright** for every screen you change, with **SYNTHETIC data only** (SYN- names, synthetic prices) and money cells masked
  in screenshots. Evidence goes in `Briefs/2026-10-10_B28_evidence/` (0700; files 0600).
- **B17 leak + secret scan** over `git diff origin/main...HEAD` and `git log --format=%B origin/main..HEAD`. Report counts only,
  with a planted control that fired. Never print the avoid list.
- **No infra change:** `git diff --numstat a168bad -- infra scripts .github` is empty. The partition check (above) is empty.
- **STATUS sections:**
  - BLUF;
  - `## PRIOR-WORK CHECK`: what existed at each spot before you replaced it, and why it was so (B16/B18/B22 rulings);
  - Modified pre-existing tests (before → after, with why);
  - NEW WORDS;
  - Options for Kam;
  - UNMEASURED;
  - `## NOT DONE / NOT COVERED`, as prominent as the evidence;
  - needs-Friday;
  - processes started / stopped.

## Time-box
**About 3 h.** If you run short, finish G-2 and G-5 first, then the rest in rank order (G-6, G-7, G-8, G-9, G-10, G-11, G-12,
G-14…G-18). List what is left as **NOT DONE**, never half-merged. Each fix is its own commit.

## STANDING LINES / HOLDS
- Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green (the org ruleset requires CodeQL results; never push an unscanned commit to main).
- **PRIOR-WORK CHECK:** before you replace or reword anything, record what existed and why (ruling, brief, test).
- No merge, no deploy, no Azure / `az` / Kudu / app-setting change, no Jira write, no mail to any human.
- **No real client data anywhere.** The example quote is CONFIDENTIAL; report counts only. That covers code, tests, fixtures,
  screenshots, commit messages and STATUS. Price-book values never leave `.local/pricebooks/`.
- **Never delete, quarantine** to `.tools/_quarantine/2026-10-10_B28_<what>/` (0700) and say so. Never edit a running script.
- **Own worktree and own ports.** Only `fetch`, `worktree add`, commits and pushes on your own branch. Never `checkout` or
  `switch` in `2_Project_Files`, and never `gc`, `prune`, `worktree remove`, `branch -D` or force-push.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY. `caffeinate` and the shared
  `VBCSCompiler` are Friday's.
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`.
  Build with `UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** run `cmd > out 2>&1; rc=$?`, then read the file. Verdicts are ratios with denominators. Every scanner zero has
  a positive control that fired.
- **Records:** write only your STATUS and evidence folder. `CLAUDE.md`, `BACKLOG.md`, `history.md` and Jira are Friday's.

## End
The last line of `Briefs/2026-10-10_B28_STATUS.md` is one of these:
- `READY FOR GATE`, with the head SHA of `b28/commercial-readiness-fixes` read back by `git ls-remote` in the same action as the
  push;
- `STOPPED: NEEDS FRIDAY` and one question.
