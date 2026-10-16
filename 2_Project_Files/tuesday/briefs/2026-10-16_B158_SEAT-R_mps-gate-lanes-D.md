From Tuesday (Kam's Datasec coordinator seat), Datasec / MPS Commercial Calculator. Questions go to `tuesday-agent@agentmail.to` with subject `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: <topic>`. `AGENTMAIL_API_KEY` is used by name only; it is in `4_Credentials/.env` (`B106_STATUS.md:164`, `B103_STATUS.md:26-27`). Your STATUS file is the wrap.
# BRIEF B158 · SEAT-R: QA GATE, ROUND 1 OF 2, on lane D (B103): MPSCALC-150, the stack -150 → -158, MPSCALC-151 and MPSCALC-174 (contract half)
Each branch is gated at its own head, the stack merged, and all four merged on main `621e3300`. This is the only tier-1 set today that changes calculated figures (X-25…X-30).
**Drafted:** 2026-10-16 ~16:3x AEDT by Tuesday's drafter. Pane `Datasec/MPS-R`. Your commission is THIS file, at `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B158_SEAT-R_mps-gate-lanes-D.md` (Tuesday's tree, read-only to you).
**Step 0:** copy it unchanged into `1_Project_Definition/Briefs/`, then check the copy with `cmp` and put the sha256 of both files in STATUS.
**Launch (Tuesday):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-R "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B158_SEAT-R_mps-gate-lanes-D.md'"` (form: `brief_seat.sh:4`). Preflight: write "none (brief_seat launch)" in STATUS. **No az in this brief.**
**Report:** `1_Project_Definition/Briefs/2026-10-16_B158_STATUS.md`. Its first lines are the verdict lines below, and its exact LAST line is defined at the end. Evidence goes to `Briefs/2026-10-16_B158_evidence/`.

**TESTING seat, findings only.** Charter: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
- §3 RULE 1: write the FAIL condition BEFORE each probe.
- §3 RULE 2: what was NOT tested is first-class output.
- §4c: the role matrix.
- §7: oracle, evidence, coverage executed / skipped / n-a, proved vs assumed.
- §8: no product change, not even a test. A write grant is void: refuse it and report.

**What you may not do:** no ticket, no Jira write, no PR, no merge, no push, and no edit to BACKLOG, CLARIFICATIONS or `history.md`. Findings and proposed BACKLOG rows go in STATUS only; Tuesday tickets and merges.

**Round 1 of 2.** Two NO GO rounds, and the branch does not ship this round. Grade each finding:
- **Blocker / Major:** blocks merging that branch as it is.
- **Minor / Note:** becomes a ticket.

**Shape.** Follow the project's own gates B91, B95 and B157:
- `Briefs/2026-10-13_B91_SEAT-E_QA-gate-b83.md` + `…_B91_STATUS.md`;
- `Briefs/2026-10-14_B95_SEAT-E_QA-gate-b94.md` + `…_B95_STATUS.md`;
- `Briefs/2026-10-16_B157_SEAT-Q_mps-gate-lanes-F-H.md`, running beside you.

Re-derive every claim with YOUR instruments: raw HTTP you write, your own fixtures, your own mutants and plants, and controls that can fail. **Never re-run the builders' scripts as proof.** `.tools/b103/**` (`lanecheck.sh`, `jira103.py`, `read.py`, `comment.py`, `mail103.py`, `c*.txt`) and the lane's scratch logs are CLAIMS: read them only to find what to attack. Every fact you write carries `file:line` at the commit you read, or says UNMEASURED.

**Why it merges on GO.** The lane brief's HOLDS say, verbatim (`2026-10-16_B103_LANE-D_mps-lane-d.md:23`): *"Tuesday opens every PR and merges after CodeQL (all three languages, C-08/C-11) and checks are green, and after the QA gate for tier 1."* On GO or GO WITH NOTES, Tuesday opens the PR (CodeQL on CI decides) and merges. **No hosted change follows from this gate:** MPS hosted is card-per-deploy, and hosted runs `0f8ad97` since B156 (`B156_STATUS.md` last line `DEPLOYED: 0f8ad97…`).

## PINS (drafter's `git --no-optional-locks ls-remote origin`, 2026-10-16 16:19:37 AEDT; main re-read at 16:27:22)
Every sha below equals its READY line. RE-READ ALL FIVE at start and at verdict. If a branch head moved, test the READY sha only and say so. If `main` moved, see Check 10.

| # | Branch | Head (full) | Ticket · tier (READY line) | Parent | Merge-base with main | behind / ahead main | Files · shortstat (`diff <merge-base> <head>`) |
|---|---|---|---|---|---|---|---|
| 1 | `b103/mpscalc-150-deal-usage` (stack 1/2) | `31cd9ea7c9aef90ea447c79e6273b9df3da897d4` | MPSCALC-150 · 1 (`B103_STATUS.md:100`) | `7edf296` | `0f8ad97d` | 2 / 2 | 16 · +1058 −53 |
| 2 | `b103/mpscalc-158-target-click` (stack 2/2) | `c07aef2653c7324005f91de0cb5dff7d33c0c014` | MPSCALC-158 · 1 (`:213`) | `4ee8562` (on `31cd9ea`) | `0f8ad97d` | 2 / 4 | 17 · +1293 −53 (158 alone over 150: 15 · +248 −13) |
| 3 | `b103/mpscalc-151-software-term` | `e1a9a8214a32630efc60b5d6158b97757d2565f0` | MPSCALC-151 · 1 (`:203`) | `0f8ad97` | `0f8ad97d` | 2 / 1 | 4 · +103 −0 |
| 4 | `b103/mpscalc-174-feedback-429-contract` | `91040493d511ce1b17840521a2dc974ac5d0c855` | MPSCALC-174 (contract half) · 1 by label (`:208`; "no calculated figure changes", `:149`) | `a0af390` | `0f8ad97d` | 2 / 2 | 5 · +32 −12 (docs + `web/src/api/generated/**` only) |
| — | `main` | `621e3300aaae70b32a39edaed653beff7fe45b2d` (tree `c1b39c6c…`) | — | — | — | — | — |

**Main since the base**, from `git log --first-parent`:
- `5d7e481` #43: B102 MPSCALC-175, `QuoteEndpoints.cs` + tests.
- `621e330` #44: B106 MPSCALC-177, `web/src/feedback/**`.

None of the four branches touches those files.

**Merge prediction (measured by the drafter in a throwaway `git clone --shared` with `merge-tree --write-tree`; a READING, which you re-measure):**
- Each branch alone onto `621e3300`: clean. Trees: 150 `ed257eee`, 158 `fcc1211c`, 151 `7e1295a5`, 174c `ed384817`.
- 150 → 158: clean.
- **151 conflicts with 150 and with 158, in either order:**
  - `docs/ENGINE.md`: adjacent inserts, X-25…X-28 rows + paragraph vs the X-29 row, at `:141-156` of the merged file.
  - `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs`: `DealUsageRule` vs `SoftwareTermMismatch` constants, at `:60-71` of the merged file.
  - The lane's own HANDOVER says "in other hunks" (`B103_STATUS.md:221-224`). That is measured wrong.
- **174c conflicts with 150 and 158** on `web/src/api/generated/SOURCE.txt` and `schema.ts`, and after 158 also on `openapi.json` and `openapi.snapshot.json`. The lane predicted this (`:221-224`: regenerate with `node web/scripts/sync-contract.mjs <ref>`, never hand-merge).
- 151 → 174c: clean.
- `b102/mpscalc-179-leak-walk-classify` (`ee2fc09`, lane C2, gated by B159) also edits `Proposal.cs`. It merges clean before or after 150 → 158.

**Contract labels:** 150 = `0.8.0-b103` (`openapi.json:5` @ `31cd9ea`), 158 = `0.9.0-b103` (@ `c07aef2`), 174c = `0.8.0-b103` (@ `9104049`).

**CI on the branch heads: none.** `gh api …/commits/<sha>/check-runs` gives `total_count` **0** for all four, and no PR is open. Every CI number in the READY lines is the builder's local run (`B103_STATUS.md:188-197`).

**Not in this gate:**
- MPSCALC-160 (no lane-D branch; lane A's change, `:103-114`).
- MPSCALC-159 (skipped, K-12 deferred, `:116-117`).
- Lane A's T15 UI half (waits on this merge).
- Lane H's rate-limit server half `150441b`: local, waits on #4.
- Every other lane: B157 has lanes F/H, and B159 has lanes C2/E/C1 tier 1.

## THE CLAIMS AND THE ORACLES (read whole, as CLAIMS)
- **Builder's report:** `Briefs/2026-10-16_B103_STATUS.md` (240 lines). Sections:
  - readings `:10-20`;
  - 150 `:36-101`;
  - 160 `:103-114`;
  - 151 `:124-141` + `:200-203`;
  - 174c `:143-151` + `:205-208`;
  - 158 `:153-174` + `:210-213`;
  - CI table `:188-197`;
  - HANDOVER `:215-238`.

  There is no evidence folder; the lane's logs were in its session scratchpad (UNMEASURED by you unless you find them; never needed).
- **Ticket acceptance (the oracle):** Jira MPSCALC-150, -151, -158, -174, **GET only**.
  - Export `JIRA_BASE_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` BY NAME from `4_Credentials/.env` (`JIRA.md:10`). Never print them, never put them on argv, never write them to a file.
  - Write your own small GET client, not `.tools/b103/jira103.py`.
  - Quote each ticket's acceptance verbatim in STATUS.
  - If Jira is unreachable, say so in one line and grade against the register rows and Kam's cards below, marked "acceptance UNMEASURED (Jira)".
- **Rows and cards:**
  - `Registers/2026-10-16_paul-review-items.md`: T15, T16, T23, and BL-13 for 174.
  - Kam's rulings, MPS-LANES ADDENDUM-1 (`2026-10-16_MPS-LANES_ADDENDUM-1_kam-rulings-1303-1306.md:7`, `:14`, `:19`), verbatim: *"Build K-09 then K-11; defer K-12"*. K-10: *"offer ONLY the term SKU that matches the quote term, AND warn on a mismatch"*.
  - B103 ADDENDUM-1 (`2026-10-16_B103_ADDENDUM-1_proposal-rows-and-feedback-429.md:6-11`): lane D may add `Proposal.cs` classification rows for its own new DTO fields only. Every new input field is NotShown or Internal, and nothing becomes proposal-visible without Tuesday's word.
- **Tier rule** (lane brief `:10`), verbatim: *"Tier 1 = anything that changes a calculated figure or a price"*.
- **Calculation register:**
  - `1_Project_Definition/Architecture/2026-09-30_workbook-calculation-register.md` (rental ids; NOT edited by the lane, `B103:14-16`).
  - The purchase X-rows in `docs/ENGINE.md`: X-25, X-26, X-27, **X-30**, X-28 at `:141-145` @ `c07aef2` (note the order); X-29 at `:141` @ `e1a9a82`.
  - The lane's proposed register rows: `B103:60-67`, `:108-109`, `:133`, `:163-164`.
  - Your arithmetic oracle is the X-13…X-18 rows of `docs/ENGINE.md` **at `621e3300`**, never the branch's code.

## RULED, SET, or OPEN (cite; do not re-open what is ruled. You check the IMPLEMENTATION and REPORT consequences)
- **RULED by Kam:**
  - K-09 = a (T15 build).
  - K-11 = a (T23, after T15).
  - K-10 = a: BOTH the matching-term picker AND the warning.

    Branch 151 builds ONLY the warning; the picker half is a NEEDS LANE A (`B103:139-140`). Grade whether 151 alone meets MPSCALC-151's acceptance. If it does not, that is a REPORT of a split ticket, not a NO GO of the warning by itself, unless acceptance says otherwise.
  - K-12 deferred.
- **SET by Tuesday's ADDENDUM-1:** `Proposal.cs` rows are classification only. Check that every 150 and 158 hunk in `Proposal.cs` is rows or comments only (`git diff -w`). The lane lists N and I rows at `B103:52-56` and `:161-162`.
- **OPEN, NOT confirmed by Tuesday at drafting.** You check that each is built as stated and REPORT what follows for a user; you do not grade the choice:
  - (a) The deal's applied rates are NotShown, so a usage-model proposal shows no click rate (`B103:57-58`, `:227-228`).
  - (b) A quote uses ONE usage model: blocking `USAGE MODEL MIXED` (`PurchaseCalculator.cs:309` @ `31cd9ea`).
  - (c) Pages count only non-optional, non-credit device lines (`B103:40`).
  - (d) Shortfall is per line and per device (`B103:41-42`).
  - (e) The 174 contract documents a 429 that main's server does not send until lane H's half lands.
- **Known gap the lane declared, which you grade:** `B103:95-96`, verbatim: *"Until then a priced caller can change the deal rates without a reason or audit entry."* The section `clickRates` require `PRICE_REASON_REQUIRED` and are audited. Measure it (Check 5) and grade whether it blocks merging 150 as is.
- **You do NOT run `infra/tests/test_infra.py`** (it shells out to `az bicep build`). STATUS says "not run (az fallback, HOLD)".

## Verdict lines (first lines of STATUS; token per branch exactly `GO`, `GO WITH NOTES` or `NO GO`)
- `B150 31cd9ea:` · `B158 c07aef2:` · `B151 e1a9a82:` · `B174c 9104049:`, each `GO | GO WITH NOTES | NO GO`.
- One line each:
  - `B158 ticket acceptance (4 tickets, clause by clause):`
  - `B158 red-first re-run (own, behavioural):`
  - `B158 CI line as name sets (0 lost):`
  - `B158 stored quotes unchanged (hash + figures):`
  - `B158 X-25…X-30 against own oracle:`
  - `B158 pricing policy + privacy (role matrix, markers):`
  - `B158 deal-rate audit gap:`
  - `B158 contract + generated types:`
  - `B158 Proposal.cs rows only + guard tests:`
  - `B158 edited pre-existing tests (weakened?):`
  - `B158 words (issue texts on screen, listed):`
  - `B158 CodeQL:`
- `MERGE stack 150→158 on <main-at-verdict, 7>:` · `MERGE all four on <main-at-verdict, 7> (GATE-RESOLVED, order 150, 158, 151, 174c):`, each `GO | GO WITH NOTES | NO GO`.

## Check (FOUND / TESTED / HOW, each with its own control or mutant)
0. **Instrument and machine.**
   - **One scratch clone:** `git clone --shared` of `2_Project_Files` into `<project root>/.tools/qa-B158/repo`, with the push URL set to `DISABLED`. `<project root>/.tools/` is git-ignored by the records repo (`.gitignore:29`, as `B156_STATUS.md:62`).
   - **Pins:** the five pins and `ee2fc09` (lane C2's 179, for Check 7) already resolve through the clone's alternates, so no fetch is needed. Prove it with `cat-file -t` = commit ×6.
   - **Worktrees** go inside the clone, detached and named by role:
     - `base-main` = `621e3300`;
     - `base-0f8` = `0f8ad97`;
     - `h150`, `h158`, `h151`, `h174`;
     - `m-D` = main + 150 + 158;
     - `m-151` = main + 151;
     - `m-174` = main + 174c;
     - `m-all` (Check 10);
     - `mut`.
   - **Toolchain:** `.tools/dotnet` (10.0.401, B156 drafter), and Node/npm as the lanes ran them (state the versions).
   - **Heavy runs (MPS-LANES ADDENDUM-6, binding on you):** every `dotnet build`/`test`, `npm ci`/`test`/`run build` and Playwright run takes a slot first:
     - `mkdir "<project root>/.tools/heavy-slot-1" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-2" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-3"`;
     - put a `holder` file in it with `B158` + the start time;
     - if all three are taken, wait 3 minutes and retry.
   - **This gate takes slots like a lane: at most ONE at a time.**
     - Record the slot number and the `uptime` load beside every result.
     - At the run's end, remove ONLY your own slot (`holder` file + `rmdir`, in the same command block). **That is the one removal this brief allows.**
     - Single test files under a minute need no slot.
     - Drafter's measure at 16:25: slot 1 held by `B157` (16:23:54), slot 2 by `B160` (16:25:02), slot 3 free; load 4.84.
     - **B157 (seat Q), B160 (seat P) and B159 (seat S) share these three slots with you:** expect to wait.
1. **Diff review vs READY claims and ticket acceptance, per branch.**
   - Read whole: `git diff <merge-base> <head>`, and for 158 also `git diff 31cd9ea c07aef2`.
   - One table per ticket. Map every acceptance clause or row to `built` / `not built (reason)` / `NOT MET`, with `file:line`.
   - Check each READY claim against the code, e.g.:
     - "an input without them hashes exactly as at base" (`PurchaseInput.cs:65-66,111` `JsonIgnore(WhenWritingNull)` @ `31cd9ea`);
     - "Redact/Restrict strip them" (`B103:51`);
     - "a what-if: no rate, total or profit of the quote changes" (`B103:157`);
     - "Warning only: no price, status, total or approval changes" (`B103:126-127`);
     - "No server code" for 174c (`git diff --name-only 0f8ad97 9104049` = `docs/**` + `web/src/api/generated/**` only).
   - **Scope:** each branch's paths are inside lane D's file list (`2026-10-16_B103_LANE-D_mps-lane-d.md:9`), plus NEW test files (the lane's reading, `B103:11-13`), plus `Proposal.cs` rows (ADDENDUM-1). List any path outside.
2. **Red-first, re-run with YOUR harness.**
   - **The builder's red for 150 and 158 is a COMPILE red** (CS0246 / CS1061, `B103:69-71`, `:165-167`). That proves the inputs did not exist, not that the tests catch a wrong rule. So the red you report is **behavioural, by YOUR mutants** on the head (each mutant → which named tests go RED; restore → GREEN; `git status --porcelain` 0). At least these:
     - (i) X-27 on POOLED pages instead of per device;
     - (ii) count an optional or a credit device line's pages;
     - (iii) multiply the deal's supplies profit by the device count;
     - (iv) revenue at the CALCULATED rate when a fixed deal rate is set (W-B);
     - (v) drop one `JsonIgnore(WhenWritingNull)`, so the hash pin `A_quote_without_deal_usage_or_page_estimates_hashes_as_at_base` (`DealUsageTests.cs:64-71` @ `31cd9ea`, `ce2c8e03…4f65fc`) goes RED;
     - (vi) 158: margin = 1 − target / CPP (inverted);
     - (vii) 158: the target replaces the APPLIED rate;
     - (viii) 151: `SOFTWARE TERM MISMATCH` raised as Block, or on credit lines, or skipping optional lines (`PurchaseCalculator.cs:327-335` @ `e1a9a82`).

     A mutant that no test catches is a REPORT on the tests (name it). It is Major only if it also breaks a figure your own oracle (Check 4) catches.
   - **151's red as the builder framed it:** 4 tests at base `0f8ad97`, 3 red / 1 green (`B103:129-132`). The "warning only" test was NOT re-measured at base after the lane's fixture fix (`:132`, `:235-236`): measure it.
   - **174c:** no test was added (`B103:194-195`). Your control is Check 6.
3. **The CI line, as name sets.**
   - The CI's own lines:
     - `.github/workflows/ci.yml`: `dotnet build MpsCalc.slnx -c Release` with 0 warnings, then `dotnet test … --no-build`;
     - `npm ci`, `npm run lint`, `npm test`, `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`;
     - the python job, without `infra/tests/test_infra.py`.
   - Run on `base-main`, `m-D`, `m-151`, `m-174`, and `m-all` if Check 10 builds it. If slots are short, the minimum is `m-D` + `m-all` + each head's own new test files; say which.
   - The web line matters because 150, 158 and 174c regenerate `web/src/api/generated/**`.
   - **Output:** name sets (`comm` of sorted test names): lost (must be 0), new (list them), failed.
   - Builder's counts at base `0f8ad97` (72 / 310 / 1,440):
     - 150: 72 / 327 / 1,448 (`B103:73`);
     - 151: 72 / 314 / 1,440;
     - 174c: 72 / 310 / 1,440;
     - 158: 72 / 334 / 1,450 (`:191-193`);
     - web: 608/608 on each.
   - **Load:** a web timeout in an untouched file is load, not a finding, ONLY if the same test fails on `base-main` in the same conditions or passes alone. Name each. **0 failed is the bar on the merged trees.**
4. **Figures (the core of a tier-1 gate). Through the real API where reachable:** a DevStub API you start from your worktree, on ports **6760-6769** only, with `lsof` before each bind. Synthetic data only; Administrator / Seller / Approver via DevStub headers. Write the FAIL condition first for each.
   - **(a) Stored quotes do not change.**
     - Build synthetic purchase quotes WITH per-section `clickRates` (the old model) and without, plus rental quotes, through **main's** API on `base-main`. Then read and calculate each on `m-D` and on `m-all`.
     - Response bodies must be byte-equal after masking ids and timestamps (put your mask list in STATUS). `inputHash` must be equal per quote.
     - Also run the engine's own fixtures at `base-main` vs `m-D`: `tests/MpsCalc.Engine.Tests/Fixtures/replica_scenarios.json` and `purchase_bom_scenarios.json`.
     - Reproduce the hash pin `ce2c8e03…` with YOUR OWN input, not the test's.
     - Control: one changed tier price in your synthetic reference document must turn the comparison RED.
   - **(b) X-25…X-28 against YOUR oracle.**
     - Compute with Python `decimal` (state the precision and rounding) from `docs/ENGINE.md` X-13…X-18 **at `621e3300`** and X-25…X-28 as worded @ `31cd9ea:docs/ENGINE.md:141-145`. At least 6 deals:
       1. one device line (must equal the section model with the same AMPV and share: the lane's parity claim, `B103:67`);
       2. three device lines, mixed mono and colour, different quantities;
       3. a deal with an optional device line and a credit device line (both excluded from pages);
       4. a manual device line;
       5. a device line with no estimate (counts its devices and 0 pages, `B103:31-32`);
       6. a fixed deal rate that wins over the calculated one for revenue (W-B).
     - Compare every field of `PurchaseResult.usage` and `DealProfit` to the last digit.
     - FAIL: any difference you cannot attribute to a stated rounding rule.
     - Also probe: a book MONO device with colour pages (`COLOUR VOLUME ON MONO DEVICE`); pages on a non-device line; a negative or fractional mono estimate; and a margin of exactly 100% (X-15 divides by 1 − margin): block, never a division error or a 500.
   - **(c) X-30 (158).** Target margin = 1 − CPP / target, unrounded (`B103:155`).
     - Round trip: the margin fed back into X-15 gives the target (the lane claims within 1e-24).
     - `TARGET BELOW COST` when the margin is negative (`PurchaseCalculator.cs:765` @ `c07aef2`).
     - `INVALID TARGET CLICK` for 0 or a negative target (`:349`).
     - **What-if proof:** the same quote with and without targets is byte-equal except the four new internal fields (`DealUsageResultDto.{TargetMonoMargin,TargetColourMargin,SuppliesProfitAtTarget,DealProfitAtTarget}`).
     - A target on a quote with NO deal usage: state what happens.
   - **(d) X-29 (151).** The same purchase quote with a 12-month licence on a 36-month quote and with the matching licence:
     - every total, status and approval flag is equal; one Review issue appears per offending line;
     - credit lines and manual software (no term) raise nothing; optional lines DO raise one (`B103:125-127`).
5. **Pricing policy, privacy, and the audit gap (tier-1 abuse).** Use the role matrix, charter §4c.
   - **Callers:** Seller WITHOUT internal-metrics, Seller + PricingAnalyst, Approver, Administrator, anonymous (401), and a bad act-as (400). For each, send a purchase quote that:
     - sets `usage.supplies` → 403 `INTERNAL_INPUT_FORBIDDEN` for a caller without internal-metrics (`PricingPolicy.cs:69` @ `31cd9ea`);
     - sets or changes or DROPS a fixed deal rate without the price permission → 403 `PRICE_EDIT_FORBIDDEN` (`:128`);
     - omits `usage` on an edit, so the hidden deal supplies must be kept (`B103:50-51`);
     - for 158, sets target clicks as a non-internal caller.
   - **Markers:** plant marker values in `usage.supplies` (consumable cost, margins) and in the target clicks. Then grep the responses of every non-internal caller: GET, calculate, proposal, export, the quote list, and the API log. FAIL: any hit (`Redact` / `Restrict` claim, `B103:51`).
   - **The audit gap (`B103:95-96`):** as a priced caller, change `usage.monoClick` with no reason. Record:
     - the status code, and whether `PRICE_REASON_REQUIRED` fires;
     - whether an audit entry is written;
     - the same for a section `clickRates` change on `base-main` (the control that does ask).

     Grade it with its consequence: a price on a deal-usage quote changes without a reason or trail.
6. **Contract and generated types.**
   - For each of 150, 158 and 174c, in a scratch worktree: `node web/scripts/sync-contract.mjs <the head>`, then `git diff --exit-code -- web/src/api/generated`. It must be 0 (the generated files equal a fresh regeneration; `SOURCE.txt` names the ref, `B103:49`, `:147`, `:160`).
   - Control: hand-edit one enum value in the snapshot → the diff is non-zero.
   - The repo's own contract tests pass on each head and on `m-all`, including `QuoteApiTests.cs:97` (contract operations equal mapped routes, @ `621e3300`).
   - 174c: confirm the 429 / `FEEDBACK_RATE_LIMITED` / `Retry-After` text equals lane H's NEEDS LANE D text, which the lane says it applied verbatim (`B103:144`; `B106_STATUS.md` "NEEDS LANE D" items 1-5). Show the diff of the two texts.
   - Say what main's server sends on the 21st feedback post within an hour today (the documented default is 20; main has no 429 yet, `B106_STATUS.md:81-85`). Make NO feedback posts to anything but your own DevStub API.
   - The version labels: the merged tree should carry one label (say which).
7. **`Proposal.cs` rows, guard tests, proposal output.**
   - `git diff -w 0f8ad97 31cd9ea -- src/MpsCalc.Api/Quotes/Proposal.cs` and `31cd9ea c07aef2`: rows and comments only. List every row with its class against `B103:52-56`, `:161-162`.
   - On `m-D`, AND on main + `ee2fc09` (lane C2's 179) + 150 + 158 (`m-D179`; 179 makes the leak walk yield solution generics, `B102_STATUS.md:146-150`), run `Every_field_of_every_proposal_source_type_is_classified` (`QuoteApiTests.Showcase.cs`) and `QuoteApiTests.ExportRegistry.cs`. Both must be green (B103 ADDENDUM-1 item 3).
   - **Proposal output:** for your Check 4a quotes, the proposal and export payloads are byte-equal on `base-main` vs `m-D`.
   - For a deal-usage quote, record what the customer-facing proposal shows about usage charges. Expected per the lane: no applied click rate (`B103:57`). REPORT for Tuesday; do not grade the choice.
8. **Words.** Calculation issues DO reach a screen: `web/src/screens/bom/PurchaseResultView.tsx:204` and `PriceView.tsx:257` @ `621e3300` render `{i.message}`. The lane wrote "none on screen" (`B103:84`).
   - List every new or changed issue and problem sentence VERBATIM with `file:line` at the head: `B103:85-90`, `:137-138`, `:170-171`.
   - Prove which caller sees each, with one screenshot per family (synthetic only) from your own web build against your own API.
   - Kam approves these at the words gate before any deploy; you only list them.
9. **Edited pre-existing tests: weakened or not** (as gate B95 Check 5).
   - The lane says it modified no existing test file (`git diff --diff-filter=MDR` over tests: empty, `B103:82`). Verify on all four heads.
   - 158 appends to 150's own `DealUsageApiTests.cs` (+26/−0, `B103:168-169`): verify that it is append-only.
   - Any edit to a pre-existing assertion → count the assertions before and after, and run a mutant the OLD test caught. A weakened or deleted expectation = **Major**.
10. **Merge prediction and merged runs** (scratch clone only).
    - Re-read `main` by `ls-remote` at start and at verdict.
    - `git merge-tree --write-tree <main> <head>` for each of the four: clean? tree id.
    - The stack 150 → 158.
    - Then 151 and 174c onto `m-D`: expected CONFLICTS (see PINS). **Do not hide them:** report each hunk.
    - THEN build `m-all` as a **GATE-RESOLVED** tree, labelled so everywhere:
      - for `ENGINE.md` and `PurchaseCalculator.cs`, keep BOTH sides (the X-25…X-28 block and the X-29 row; both constants);
      - for the contract, regenerate `web/src/api/generated/**` with `sync-contract.mjs` from the merged `openapi.json`;
      - for `openapi.json` itself, keep both edits.
    - Run Check 3 on `m-all`. Its result tells Tuesday whether the obvious resolution compiles and passes; it is not the shipped resolution.
    - If `main` moved during the gate (B157's lanes F/H, B160's package change, or tier-2 PRs may merge): name what moved, whether it touches any of these files, and re-run the .NET and web lines on `m-D` and `m-all` rebuilt on the new main, once.
    - **CodeQL:** no local runner; "CI on Tuesday's PR decides". Never dismiss or read-and-close an alert.
11. **`docs/ENGINE.md` and the register rows.**
    - Each X-25…X-30 row's words against the code at its head: a row that says something the code does not do = Minor.
    - The row order at `c07aef2` is X-25, X-26, X-27, X-30, X-28 (`docs/ENGINE.md:141-145`): a Note.
    - The lane's proposed calculation-register rows (`B103:60-67`, `:133`, `:163-164`): say whether each matches the code. The register itself is Tuesday's records; do not edit it.
12. **Security and privacy on the touched surface.** No value from a synthetic quote's internal inputs appears in any response `detail`, log line or stderr you caused (planted markers, 0 hits). Run gitleaks over each range (`<mb>..<head>`), with a planted control that fires.

**Findings to grade (each: severity, blocks merging which branch?):**
- the deal-rate audit gap (Check 5);
- any marker leak (**Blocker**);
- any stored-quote figure or hash change (**Blocker**, tier-1 rule);
- any X-25…X-30 disagreement with your oracle (**Blocker** unless rounding is stated and agreed);
- a 500 on any abuse input (**Major**);
- 151's split acceptance (Check 1);
- the merge conflicts (a finding for Tuesday's merge, not a product NO GO by itself);
- the issue texts on screen (words list);
- a lost test name (**Major**).

**Screenshots** (synthetic only) → `Briefs/2026-10-16_B158_evidence/screens/`: the purchase result with a deal-usage issue, `SOFTWARE TERM MISMATCH`, `TARGET BELOW COST`, and a non-internal caller's view of a deal-usage quote.

## HOLDS
- **Datasec / MPS only.** Synthetic data and synthetic names only (`SYN-B158-*`, `Synthetic`).
  - **Never open** `.local/`, `.local/pricebooks/`, `1_Project_Definition/Source_Documents/**` (the client's review files), or the `.tools/backup-*/` zips and their contents.
  - `4_Credentials/.env` is used only to export `JIRA_*` and `AGENTMAIL_API_KEY` BY NAME: never printed, never on argv, never written.
  - **No hosted site, no HTTP to it, no Kudu, no az** (`infra/tests/test_infra.py` is NOT run). Jira **GET only**.
  - Mail: QUESTION mails to `tuesday-agent@agentmail.to` only; nothing to any human.
- **No product change, no test change, no commit or push to any code branch** (never to `b103/*` or `main`).
  - No PR, no merge, no deploy, no Jira comment or transition.
  - No BACKLOG / CLARIFICATIONS / register / `history.md` edit, and no commit to the records repo (the project root). Write STATUS and evidence as working-tree files only; Tuesday's records seat folds them.
  - Never force-push, never dismiss CodeQL.
- **Never delete:** quarantine to `<project root>/.tools/_quarantine/2026-10-16_B158_<what>/`. The ONE allowed removal is your own heavy slot (Check 0).
- **In the project checkout, READ verbs only,** as `git --no-optional-locks -C 2_Project_Files`: `ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep · status`.
  - The root checkout `2_Project_Files` sits on another branch (`b03/api`): read it only, never `checkout`/`reset`/`switch`.
  - Every write verb happens in YOUR scratch clone `.tools/qa-B158/`: worktree add, merge, merge-tree `--write-tree`, scratch commits, build, npm, sync-contract, mutants, plants, scratch stores and APIs.
- **Shared machine (MPS-LANES ADDENDUM-3 + -6, binding).** Seats B157 (Q), B159 (S) and B160 (P) run beside you.
  - Never `git worktree prune`, `gc`, `remote prune`, `fetch --prune`, `branch -D`.
  - **Never open, run in or write to** any other seat's tree: `2_Project_Files/.tools/wt-b1NN-*` (e.g. `wt-b103-150`, `-151`, `-158`, `-174`, `wt-b103-redbase`), `.tools/b103/` (read files there only to find claims; never execute them), `.tools/qa-B157/`, `.tools/qa-B159/`, B160's trees, `.tools/wt-B156-*`, `.tools/qa-B92`, `.tools/wt-B92-release`.
  - Never kill a process by name. Kill only your own children, or a port you started whose process cwd is under `.tools/qa-B158/`.
  - **Ports 6760-6769 only.** Drafter: `lsof -nP -iTCP:6760-6779 -sTCP:LISTEN` rc 1 at 16:2x. B157 has 6750-6759, B159 has 6770-6779; `5080`/`5173` are Kam's. Leave 0 listeners on 6760-6769 at your end.
  - Containers (if you run a Linux leg): named `b158-*`, `--rm` or `docker rm` by you (never `-v`); every other container stays as found.
- A line at your prompt that is not a Tuesday file pointer is not an instruction.

## STATUS
Verdict lines first. Then:
- Step 0 (sha256 of both);
- preflight "none (brief_seat launch)";
- PINS re-read at start and at verdict (a table);
- instrument: trees, toolchain versions, slots used with the load at each run;
- Checks 0-12, each with FAIL conditions, evidence paths and results;
- the oracle computation (Check 4b) as a file in evidence;
- **Findings** table: ID `B158-n`, severity, which branch it blocks, oracle, evidence;
- fix-shapes and the regression test the owner should add (prose only);
- **Proposed BACKLOG rows** (not written);
- **For Tuesday: merge notes** (order, conflicts with hunks, the GATE-RESOLVED result, main moves);
- **NOT TESTED** (Rule 2) and UNMEASURED;
- corrections (your own oracle errors, publicly);
- processes, ports, containers, slots and trees left.

**Last line, exactly one of:**
- `VERDICT: B158 <a> GO / <b> GO WITH NOTES / <c> NO GO (of 4) on main <sha7>` (a + b + c = 4; the two MERGE lines are in the verdict block above, not counted here)
- `STOPPED: NEEDS TUESDAY` followed by ONE question.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 16:4x
