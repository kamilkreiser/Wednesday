From Tuesday (Kam's Datasec coordinator seat), Datasec / MPS Commercial Calculator. Questions go to `tuesday-agent@agentmail.to` with subject `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: <topic>`. `AGENTMAIL_API_KEY` is used by name only; it is in `4_Credentials/.env` (`B106_STATUS.md:164`). Your STATUS file is the wrap.
# BRIEF B159 · SEAT-S: QA GATE, ROUND 1 OF 2, on six tier-1 branches
- **Lane C2 (B102):** MPSCALC-170 audit, -179 leak walk.
- **Lane E (B104):** MPSCALC-141 coverage docs, -147 "Customisation" + panel options (stacked on tier-2 -143), -182 Sydney date.
- **Lane C1 (B108):** MPSCALC-136 all roles.

Each branch is gated at its own head, and all six are merged on main `621e3300`.

**Drafted:** 2026-10-16 ~16:4x AEDT by Tuesday's drafter. Pane `Datasec/MPS-S`. Your commission is THIS file, at `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B159_SEAT-S_mps-gate-lanes-C1-C2-E.md` (Tuesday's tree, read-only to you).
**Step 0:** copy it unchanged into `1_Project_Definition/Briefs/`, then check the copy with `cmp` and put the sha256 of both files in STATUS.
**Launch (Tuesday):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-S "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B159_SEAT-S_mps-gate-lanes-C1-C2-E.md'"` (form: `brief_seat.sh:4`). Preflight: write "none (brief_seat launch)" in STATUS. **No az in this brief, and no Entra:** `scripts/entra_apps.py` runs ONLY against the repo's fake `az` (Check 4f).
**Report:** `1_Project_Definition/Briefs/2026-10-16_B159_STATUS.md`. Its first lines are the verdict lines below, and its exact LAST line is defined at the end. Evidence goes to `Briefs/2026-10-16_B159_evidence/`.

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

**Shape.** Follow gates B91, B95 and B157:
- `Briefs/2026-10-13_B91_SEAT-E_QA-gate-b83.md` + STATUS;
- `Briefs/2026-10-14_B95_SEAT-E_QA-gate-b94.md` + STATUS;
- `Briefs/2026-10-16_B157_SEAT-Q_mps-gate-lanes-F-H.md`.

Re-derive every claim with YOUR instruments: raw HTTP you write, your own fixtures, mutants and plants, and controls that can fail. **Never re-run the builders' scripts as proof.** These are CLAIMS: read them only to find what to attack.
- `.tools/b102/**` (`check.sh`, `scope.sh`, `namediff.py`, `trxnames.py`, `webnames.py`, `p1count.py`, `jira102.py`, `mail102.py`, `evidence/`);
- `.tools/b104/**` (`lanecheck.sh`, `ci.sh`, `ci-queue.sh`, `coverage/coverage.py`, …);
- `.tools/b108/**` and `2_Project_Files/.tools/b108-evidence/`.

Every fact you write carries `file:line` at the commit you read, or says UNMEASURED.

**Why it merges on GO.** The lane briefs' HOLDS say, verbatim (`2026-10-16_B102_LANE-C2_mps-lane-c2.md:23`, same text in `B104_LANE-E :23` and `B108_LANE-C1 :26`): *"Tuesday opens every PR and merges after CodeQL (all three languages, C-08/C-11) and checks are green, and after the QA gate for tier 1."* On GO or GO WITH NOTES, Tuesday opens the PR (CodeQL on CI decides) and merges.

**No hosted change follows from this gate.** MPS hosted is card-per-deploy, and hosted runs `0f8ad97` since B156. **The Entra change for 136 is FOR KAM** (`B108_STATUS.md:158-175`) and is never run by any seat.

## PINS (drafter's `git --no-optional-locks ls-remote origin`, 2026-10-16 16:19:37 AEDT; main re-read at 16:27:22)
Every sha below equals its READY line. RE-READ ALL EIGHT at start and at verdict. If a branch head moved, test the READY sha only and say so. If `main` moved, see Check 10.

| # | Branch | Head (full) | Ticket · tier (READY line) | Parent | Merge-base with main | behind / ahead main | Files · shortstat (`diff <merge-base> <head>`) |
|---|---|---|---|---|---|---|---|
| 1 | `b102/mpscalc-170-line-identity-audit` | `2a6dcdcdfba5b421c38d060e1298e1d9f9b63d4d` | MPSCALC-170 · 1 (`B102_STATUS.md:143`) | `cdd451d` | `7af91dec` | 3 / 2 | 6 · +390 −28 (`PriceAudit.cs`, `draftModel.ts`, `FleetGrid.tsx`, tests) |
| 2 | `b102/mpscalc-179-leak-walk-classify` | `ee2fc09d93c4bf0d3bc2b48be99fd0966de6a726` | MPSCALC-179 · 1 (`:169`) | `7af91de` | `7af91dec` | 3 / 1 | 2 · +79 −22 (`Proposal.cs`, `QuoteApiTests.GateB36.cs`) |
| 3 | `b104/mpscalc-141-coverage-audit` | `8b745389dd37a92bd2defd261436defb939cddb8` | MPSCALC-141 · 1, docs only (`B104_STATUS.md:33`) | `7af91de` | `7af91dec` | 3 / 1 | 1 · +34 (`docs/IMPORTER.md`) |
| — | `b104/mpscalc-143-supplies-label` (tier 2, the parent of #4; NOT graded here) | `7a460ab43baba6fac140726fcded3d5ae9ea59d6` | MPSCALC-143 · 2 (`:77`) | `0f8ad97` | `0f8ad97d` | 2 / 1 | 2 · +15 −1 |
| 4 | `b104/mpscalc-147-customisation` | `c61ccbc299c54ff91a593e8f87084decbce35a9a` | MPSCALC-147 · 1 (`:97`; stacked on 143) | `7a460ab` | `0f8ad97d` | 2 / 2 | 8 · +195 −6 (147 alone over 143: 8 · +180 −5) |
| 5 | `b104/mpscalc-182-sydney-date` | `66c0b8abfa086daf86c87daa4ed4d411523304e4` | MPSCALC-182 · 1 (`:117`) | `0f8ad97` | `0f8ad97d` | 2 / 1 | 3 · +62 −2 |
| 6 | `b108/mpscalc-136-all-roles` | `30e66e157526679ea1ff2861930a2cd9053899d7` | MPSCALC-136 · 1 (`B108_STATUS.md:222`) | `3e51565` | `0f8ad97d` | 2 / 2 | 9 · +370 −26 (no `.cs` file) |
| — | `main` | `621e3300aaae70b32a39edaed653beff7fe45b2d` (tree `c1b39c6c…`) | — | — | — | — | — |

**Main since the bases**, from `git log --first-parent`:
- `0f8ad97` #41: `web/src/proposal/**`.
- `5d7e481` #43: B102 MPSCALC-175, `QuoteEndpoints.cs` + tests.
- `621e330` #44: `web/src/feedback/**`.

None touches these branches' files (`B108_STATUS.md:214` measured the same for 136).

**Merge prediction (drafter, throwaway `git clone --shared`, `merge-tree --write-tree`; a READING, which you re-measure):**
- Each branch alone onto `621e3300`: clean. Trees: 170 `a27d13a3`, 179 `45c790a6`, 141 `95029725`, 147 `58860c1d`, 182 `ec3e6d3c`, 136 `2aa8bb49`.
- In sequence `143 → 147 → 141 → 182`: clean. They share `docs/IMPORTER.md`, and `PriceBookImporter.cs` between 147 and 182.
- **179 and lane D:** `179 → 150 → 158` and `150 → 158 → 179` are both clean. 179 and lane D's `31cd9ea`/`c07aef2` both edit `Proposal.cs`; lane D is gated by B158.
- **Squash trap:** if 143 is squash-merged and 147 merged as a second squash PR, it conflicts on `classLabels.test.ts` (measured). Merge the stack with merge commits, or 147 alone (it carries 143).

**CI on the branch heads: none.** `gh api …/check-runs` gives `total_count` **0** for all seven shas, and no PR is open. Every CI number in the READY lines is the builders' local run.

**Not in this gate:**
- tier-2 branches of these lanes: C2 105, 171 (171 conflicts with main #43); E 143, 175-relay;
- waiting items: C2 161/172/169/28; E 140/142/155/144; C1 T02 MPSCALC-137;
- BL-27 MPSCALC-188 (no code);
- lane D (B158) and lanes F/H (B157).

## THE CLAIMS AND THE ORACLES (read whole, as CLAIMS)
- **Builders' reports:**
  - `Briefs/2026-10-16_B102_STATUS.md` (218 lines): 170 `:107-143`, 179 `:145-169`, words `:177-185`, HANDOVER `:187-210`.
  - `Briefs/2026-10-16_B104_STATUS.md` (202 lines): 141 `:20-33`, 147 `:79-97`, 182 `:109-117`, words `:153-161`, HANDOVER `:171-181`, CI `:197-200`.
  - `Briefs/2026-10-16_B108_STATUS.md` (224 lines): 136 `:9-108` + `:204-222`, FOR KAM `:158-175`, C-33 paragraph `:140-156`.
- **Ticket acceptance (the oracle):** Jira MPSCALC-170, -179, -141, -147, -182, -136, **GET only**.
  - Export `JIRA_BASE_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` BY NAME from `4_Credentials/.env` (`JIRA.md:10`). Never print them, never put them on argv, never write them to a file.
  - Write your own GET client.
  - Quote each acceptance verbatim in STATUS.
  - If Jira is unreachable, use one line, then grade against the register rows + BACKLOG rows, marked "acceptance UNMEASURED (Jira)".
- **Rows each ticket covers:**
  - `Registers/2026-10-16_paul-review-items.md` and `BACKLOG.md`.
  - 170: `[B36-N4]` (not built: needs a contract id, `B102:114`), `[B36-N10]`, `[B38-L1]`, `[B38-L2]`, `[B38-L3]`, `[B38-N2]`, `[B36-K2-purchase]` (per-row table `B102:112-120`).
  - 179: `[B38-L4]`, `[B38-N5]`.
  - 141: T06.
  - 147: T12.
  - 182: BL-21.
  - 136: T01, `[B31-ENTRA5]`.

  Read each BACKLOG row whole.
- **Kam's rulings** (MPS-LANES ADDENDUM-1, verbatim):
  - roles card: *"All roles + owner self-approval, audited; accept cost-plus visibility"* (`:6`);
  - catalogue card: *"Approve all six as recommended"* (`:8`): K-06 = Option shown as "Customisation".
- **Tier rule** (lane briefs `:10`): *"Tier 1 = anything that changes a calculated figure or a price"*.
  - 170 is tier 1 because it changes when `PRICE_REASON_REQUIRED` fires and what the price audit records (`B102:124-125`).
  - 179 because it is a security test plus classification.
  - 147 because it adds PRICED catalogue rows.
  - 182 because it is the validity gate of the price books.
  - 141 by label (docs only).
  - 136 because it is access (`B108:48-49`).
- **Calculation register:** `1_Project_Definition/Architecture/2026-09-30_workbook-calculation-register.md`, and the X-rows in `docs/ENGINE.md` @ `621e3300` (X-23: Option → hardware, the class map 147 relies on, `B104:89-90`).

## RULED, SET, or OPEN (cite; do not re-open. You check the IMPLEMENTATION and REPORT consequences)
- **RULED (Kam):**
  - K-01 = a: all roles through an Entra group, never a code bypass (`B108:11-12`). 136 builds the web half plus an opt-in script; it changes no server file (verify).
  - K-06 = a: "Customisation".
  - K-18 = a: cost-plus visibility accepted (no code).
- **OPEN, NOT confirmed by Tuesday at drafting.** You check that each is built as stated and REPORT consequences:
  - (a) 170: `PriceAudit.Pairs` pairing within one line number: "an unchanged line first takes its identical old line, the rest pair in order" (`B102:119`).
  - (b) 170: amounts compared at their smallest scale, with recorded values kept as stored or sent (`B102:120`).
  - (c) 147: panel kits are imported as **options of every mapped device on that sheet**, with Core price, the same at every tier (`B104:82-85`), and the parity proof EXCLUDES them, printing "Not compared: n" (`B104:86-88`).
  - (d) 182: the import date is the Australia/Sydney date of the import time, whatever offset the time carries (`B104:110-111`).
  - (e) 136: a token missing ANY of the four roles keeps today's switch unchanged (`B108:17`).
- **Known consequences to REPORT, not to grade as missing:**
  - (i) With 136 merged and T02 (MPSCALC-137) NOT built, a four-role owner still meets `SELF_APPROVAL_FORBIDDEN` on their own quote (`B108:110-129`).
  - (ii) On the first deploy after 136, every token that ALREADY holds all four roles loses the act-as switch with no Entra change; `B108:164-166` counts "Kam's 4" assignments.
  - (iii) 182's Sydney date at IMPORT vs B157's 166 UTC date at API VALIDATE (`SourceLifecycle.cs:401` @ `7dfa241`): two rules for "expired" on one book.
- **You do NOT run `infra/tests/test_infra.py`** (it uses `az bicep`). STATUS says "not run (az fallback, HOLD)".

## Verdict lines (first lines of STATUS; token per branch exactly `GO`, `GO WITH NOTES` or `NO GO`)
- `B170 2a6dcdc:` · `B179 ee2fc09:` · `B141 8b74538:` · `B147 c61ccbc:` · `B182 66c0b8a:` · `B136 30e66e1:`, each `GO | GO WITH NOTES | NO GO`.
- One line each:
  - `B159 ticket acceptance (6 tickets, row by row):`
  - `B159 red-first re-run (own):`
  - `B159 CI line as name sets (0 lost):`
  - `B159 170 audit: no real change escapes, no false ask:`
  - `B159 179 guard catches a solution generic:`
  - `B159 147 imported options priced as stated, existing rows unchanged:`
  - `B159 182 Sydney date incl. DST edges:`
  - `B159 136 four-role token sends no act-as; fewer roles unchanged:`
  - `B159 entra_apps.py only against the fake az:`
  - `B159 no calculated figure of a stored quote changed:`
  - `B159 edited pre-existing tests (weakened?):`
  - `B159 words (listed):`
  - `B159 CodeQL:`
- `MERGE all six on <main-at-verdict, 7> (order 179, 170, 143→147, 141, 182, 136):`, `GO | GO WITH NOTES | NO GO`.

## Check (FOUND / TESTED / HOW, each with its own control or mutant)
0. **Instrument and machine.**
   - **One scratch clone:** `git clone --shared` of `2_Project_Files` into `<project root>/.tools/qa-B159/repo`, with the push URL set to `DISABLED` (`.tools/` is git-ignored, `.gitignore:29`).
   - **Pins:** all pins resolve through alternates, so no fetch is needed. Prove it with `cat-file -t` ×8, including lane D's `31cd9ea` and `c07aef2` for Check 9.
   - **Worktrees**, detached and named by role:
     - `base-main` = `621e3300`;
     - `base-7af` = `7af91de`;
     - `base-0f8` = `0f8ad97`;
     - `h170`, `h179`, `h141`, `h147`, `h182`, `h136`;
     - `m-all`;
     - `mut`.
   - **Toolchain:** `.tools/dotnet` (10.0.401), and Node/npm as the lanes ran them (state the versions).
   - **Heavy runs (ADDENDUM-6, binding):**
     - take one slot: `mkdir "<project root>/.tools/heavy-slot-1" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-2" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-3"`;
     - put a `holder` file in it with `B159` + the start time;
     - if all are taken, wait 3 minutes and retry;
     - **at most ONE at a time**;
     - record the slot and the `uptime` load beside every result;
     - at the end, remove ONLY your own slot (`holder` + `rmdir`, same block). **That is the one removal this brief allows.**
     - Drafter's measure at 16:25: slot 1 `B157`, slot 2 `B160`, slot 3 free; load 4.84. **B157, B158 and B160 share the three slots with you.**
1. **Diff review vs READY claims and ticket acceptance, per branch.**
   - Read whole: `git diff <merge-base> <head>`, and for 147 also `git diff 7a460ab c61ccbc`.
   - One table per ticket: each clause or row → `built` / `already on main (test name, run once on 621e3300)` / `not built (reason)` / `NOT MET`, with `file:line`.
   - **Scope:**
     - C2: brief `:9` + B102 ADDENDUM-1 (the web tests beside C2's screens).
     - E: brief `:9`; the lane's reading of its tests is at `B104:12-13`.
     - C1: brief `:9` + two declared NEW files, `scripts/tests/test_entra_all_roles.py` and `scripts/tests/fakes_groups/az` (`B108:83-86`).

     List any path outside.
   - **136:** `git diff --name-only 0f8ad97 30e66e1 -- '*.cs'` must be empty: "no server change" (`B108:40`).
2. **Red-first, re-run with YOUR harness.** For each branch, run the new and changed tests against the BASE source and against the head. FAIL:
   - a new test GREEN at base that the builder called red-first;
   - red at base for a reason other than the missing behaviour;
   - red at head.

   Builder's counts:
   - 170: per row (`B102:115-120`; e.g. `[B38-L2]` web red 6/6, `[B38-N2]` rental 1/1 + purchase API 2/2, `[B36-K2-purchase]` red 2/2).
   - 179: `B102_L4_…` red 2/2, `B102_N5_…` red 2/2 (`:149`, `:155`).
   - 147: compile red + label test 1 of 3 (`B104:91`).
   - 182: 2 of 3 red, control green (`B104:112-113`).
   - 136: web `src/auth` 9 red / 53 green, python 10 red / 1 green (`B108:42-46`).

   **Pins that pass at base by design** (170's `[B36-N10]`, `[B38-L1]`, `[B38-L3]`; 141 docs): use YOUR OWN mutants, not the builder's E-06 / K2-iii:
   - 170: pair removed lines by array index; compare amounts with `Math.Abs`; key the web grid by line number again → the named tests go RED; restore → GREEN.
   - 179: revert `HeldTypes` to yield only generic arguments (`QuoteApiTests.GateB36.cs:130-143` @ `ee2fc09`) → `B102_L4_…` RED.
   - 182: compare in UTC.
   - 136: make `holdsEveryRole` (`EntraBoot.tsx:76` @ `30e66e1`) true for three roles, then false for four.

   After each mutant, `git status --porcelain` must be 0.
3. **The CI line, as name sets.**
   - The CI's own lines (`.github/workflows/ci.yml`): dotnet build Release with 0 warnings, then test; `npm ci` / `lint` / `test` / `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`; and the python job (including `scripts/tests/test_entra_all_roles.py` and `test_scripts.py`, **with the repo's fake `az` only, Check 4f**; not `infra/tests/test_infra.py`).
   - Run on `base-main` and `m-all`. If slots are short, the minimum is `m-all` + each head's own new test files; say which.
   - **Output:** name sets (`comm`): lost (must be 0), new (list them), failed.
   - Builder's counts:
     - 170: 1,836 + web 612 (`B102:136`);
     - 179: 1,826 (`:162`);
     - 141: 72 / 310 / 1,440 (`B104:27`);
     - 147: 75 / 310 / 1,440 + web 611 (`:96`);
     - 182: 75 / 310 / 1,440 + web 608 (`:116`);
     - 136: 72 / 310 / 1,440 + web 615 + python 11 new (`B108:206-212`).
   - **Declared name changes:** 136 drops two names and changes `it.each` rows (`B108:71-80`). Check that each dropped name's behaviour is the one Kam's ruling removed, and that a successor name exists. Anything else lost = **Major**.
   - Load rule as B157 Check 3.
4. **Abuse cases, one or more per tier-1 behaviour, through the real API where the behaviour is reachable.** A DevStub API you start from your worktree, on ports **6770-6779** only, with `lsof` before each bind. Synthetic data only. Write the FAIL condition first for each.
   - **(a) 170, the price audit:**
     - Synthetic rental and purchase quotes. For purchase, BOM line numbers may repeat today (`B102:119`: live, not only legacy).
     - **For the legacy rental `[1,1]`:** write a quote file into YOUR scratch store (as the lane's `QuoteApiTestsEmptyQuoteLegacy` pattern did; your own file).
     - Cases, each run on `base-main` and `h170`, recording: `PRICE_REASON_REQUIRED` asked? audit entries written (exact)?
       1. remove one of two same-number lines;
       2. change one of two same-number lines in place;
       3. swap their order;
       4. re-send 6 amounts at another scale (`71.115` vs `71.11500`);
       5. a real change at another scale (`71.11500` → `72.0000`);
       6. a sign change and back;
       7. `0` vs `-0` vs `-0.00`;
       8. three lines `[3,5,5]` with an override removed from the middle.
     - **FAIL:** any REAL price change at head with no reason asked and no audit entry, or an audit entry naming the wrong line. **Equally FAIL:** an unchanged re-save at head that asks for a reason or writes an entry.
     - Put every case where head and main differ in one table: that table IS the behaviour change Tuesday merges.
     - **Web (`FleetGrid.tsx`, `draftModel.ts`):** a stored `[1,1]` draft through route interception (your own Playwright spec in the scratch tree, never committed). Test: Remove takes one row, an edit changes one row, and "Give each line its own number" renumbers losslessly (options and software stay with the first holder, `B102:117`). Screenshot it.
   - **(b) 179, the leak guard:**
     - Your own mutant in the `mut` tree, never committed: add a generic `SynBox<T>` defined in an `MpsCalc*` assembly, holding a cost-bearing type, onto a DTO the proposal reaches. The guard must be RED at head and GREEN at base `7af91de` (the gap, `B102:148-150`).
     - Then the 29 NotShown → Internal rows (`B102:151-155`): list them from `git diff 7af91de ee2fc09 -- src/MpsCalc.Api/Quotes/Proposal.cs`.
     - Prove "no output or export changes": the proposal and export payloads of your synthetic quotes are byte-equal on `base-main` vs `h179` (mask list in STATUS).
   - **(c) 147, panel options:**
     - From the importer's SYNTHETIC books only (`tests/MpsCalc.Import.Tests/Synthetic/SyntheticBooks.cs` @ `c61ccbc`, `SyntheticWorkbook.cs`; ids `SYN-B159-*`; never the real books).
     - Build a book with an "Optional Color Panel Accessories" section, including a heading row whose description cell holds a colour word, the trap at `B104:45-46`. Expect:
       - the rows import as options (class Option → label "Customisation") of every mapped device on the sheet, at Core, equal at every tier;
       - a SKU cell with a space ends the section;
       - the parity proof prints "Not compared: n" (`ParityProof.cs:49-51` @ `c61ccbc`) and compares the governed options only.
     - **Existing rows unchanged:** the importer output for a book WITHOUT a panel section is byte-equal on `base-main` vs `h147`.
     - **Price of a picked panel option:** a purchase quote picking one through your DevStub API prices under X-23 hardware. Compute the line independently from `docs/ENGINE.md` @ `621e3300`.
     - A stored quote holding a manual "Other" line stays unchanged (`B104:89`).
     - **Cross-gate (only if B157's 166 is on main when you reach this, else say "UNMEASURED: 166 not merged"):** a 147-imported synthetic document passes 166's content checks (orphan option, max quantity).
   - **(d) 182, the validity date:**
     - Drive the importer with your own import times and a book whose stated end date is D:
       - UTC 13:59 and 14:00 on D (around AEDT midnight);
       - `-07:00` 07:00 on D;
       - `+11:00` 23:59 on D (control: accepted);
       - **both DST edges:** the first Sunday of April and of October 2026, around 02:00/03:00 Sydney.

       FAIL: any case whose Sydney date is after D and imports.
     - Record what 166's API validate (UTC, B157) would answer for the same book and instant (REPORT (iii)).
   - **(e) 141, docs only:**
     - The table holds counts only: no price, no client or person name (grep, with a planted control).
     - Its rows sum consistently (state each sum).
     - The decisions point at the tickets the lane names (-140, -147, -74).
     - Counts against the real book: **UNMEASURED by rule** (the book is in `.local/`, which you never open). Say so.
   - **(f) 136, all roles:**
     - **Web, Entra mode with the test infrastructure's in-memory key, as gate B91 did** (`B91_STATUS.md:157`). Otherwise use the component tests and say so.
       - A token with Seller + Approver + Administrator + PricingAnalyst → no persona select, no "Roles held", no "No persona matches your roles".
       - **Log every request header of a full session** (Playwright route log): 0 `X-MpsCalc-Act-As`. FAIL on any.
       - Tokens with each 3-role subset and with 1 role → the switch is unchanged, and the server grants exactly what it grants on `base-main`. The role matrix is identical per route. Anonymous 401, every non-holder 403, bad act-as 400.
       - A four-role token WITHOUT the `internal-metrics` permission: record what the header and the internal columns do.
       - DevStub mode: the persona switch is unchanged.
     - **Script (`scripts/entra_apps.py`):** ONLY with `PATH` starting at the repo's fake directory (`scripts/tests/fakes_groups` → `scripts/tests/fakes`).
       - **Before EVERY invocation**, assert in the same command that `command -v az` resolves to a path under your worktree's `scripts/tests/`. Abort otherwise, and record the assertion output.
       - Cases: without the new flags (byte-equal behaviour to base, `B108:20`); `--all-roles-group`; `--approver-only-user` with Kam's own account (must STOP, `entra_apps.py:281` @ `30e66e1`); a group that exists but is not security-only (must STOP); the read-back with an extra assignment (must exit 1).
       - **Never run the shell wrapper `scripts/entra-app-registrations.sh` and never let any `az` but the fake run.** A real `az` call is a hold breach: STOP.
5. **Stored data still loads (170, 147, 182).** Build H0, the shipped hosted shape, as B157 Check 5 describes, under a synthetic root.
   - Its `data/quotes/` holds rental and purchase quotes WITH audit trails, written by main `621e3300`'s own API (edits with reasons, so `PriceAudit` entries exist).
   - **FAIL:** any quote that opens on `621e3300` and is refused, or reads differently, on `h170` or `m-all`; or an unchanged re-save at head that writes an audit entry.
   - **147:** a reference store imported by main's importer still opens at head. A store imported by head opens on main: rollback. Say what main shows for the new option rows.
6. **No calculated figure of a stored quote changed (expected: none; prove it).**
   - (a) Run `git diff --name-only <mb> <head> -- src/MpsCalc.Engine src/MpsCalc.Api/Quotes/Purchase* src/MpsCalc.Api/Quotes/Mapping.cs docs/api` per branch. Expected: empty for all six. 147 changes the importer (`src/MpsCalc.Import/**`), not the engine.
   - (b) Run the engine's fixtures (`replica_scenarios.json`, `purchase_bom_scenarios.json`) and 3+ synthetic quotes of YOUR OWN through `POST …/calculate` at `base-main` and `m-all`. Responses byte-equal after masking. Control: one changed tier price → RED.
   - (c) The calculation register: 0 rows touched by any branch (say so).
7. **136's ruling, implemented as stated.**
   - The grant is the Entra group only. No server bypass: no `.cs` change. `CallerResolver.cs` act-as narrowing is unchanged, so `git diff 0f8ad97 30e66e1 -- src` is empty.
   - The C-33 paragraph (`B108:140-156`) is for Tuesday's records. Check only that it matches what the code does.
8. **Edited pre-existing tests: weakened or not** (as gate B95 Check 5). For each file: `git diff` the file, count the assertions before and after, and run a mutant the OLD test caught against the NEW test.
   - 170: `web/src/app/draftModel.test.ts` (+31 −1), `web/src/screens/FleetGrid.test.tsx` (+43).
   - 179: `QuoteApiTests.GateB36.cs` (+55 −2).
   - 147: `classLabels.test.ts` (143's file, +22), `SyntheticBooks.cs` (+15).
   - 136: `EntraBoot.test.tsx`, `EntraInventory.test.tsx`, `EntraPricingOffer.test.tsx` (the declared replacements, `B108:71-80`).

   A weakened or deleted expectation outside the ruling = **Major**.
9. **Merge prediction and merged runs** (scratch clone only).
   - Re-read `main` by `ls-remote` at start and at verdict.
   - `git merge-tree --write-tree <main> <head>` for each of the six (clean? tree id).
   - Then all six in the order 179, 170, 143 → 147, 141, 182, 136, which gives `m-all` (any conflict: name the hunk; do not resolve it).
   - **The 179 × lane D question (B103 ADDENDUM-1 item 3):** on main + 179 + `31cd9ea` + `c07aef2`, run `Every_field_of_every_proposal_source_type_is_classified` (`QuoteApiTests.Showcase.cs`) and `QuoteApiTests.ExportRegistry.cs`. Both must be green. B158 runs the same on its side; say if your results differ.
   - If `main` moved during the gate: name what moved, whether it touches these files, and re-run Check 3 on `m-all` rebuilt on the new main, once.
   - **CodeQL:** "CI on Tuesday's PR decides"; never dismiss an alert.
10. **Words.** List every new or changed user-visible sentence VERBATIM with `file:line` at the head, and say which caller sees it:
    - 170: the repeated-number notice (singular and plural) and the button (`B102:129-131`; `FleetGrid.test.tsx:92-93` @ `2a6dcdc`).
    - 147: "Customisation" (`InventoryScreen.tsx:18` @ `c61ccbc`) and the `prove` line (`B104:160`, operator).
    - 136: the three header texts no longer shown (`B108:88-90`) and the operator script lines (`B108:90-94`).
    - 182: none on screen; the `IMPORTER.md:38` sentence.
    - 141, 179: none.

    Kam approves the words at the gate before any deploy; you only list them.
11. **Security and privacy on the touched surface.**
    - Role matrix (§4c) on `PATCH`/`POST` quote routes (170) and `GET …/proposal` / export (179) at `m-all` vs `base-main`: identical status per role.
    - No value from a synthetic quote's internal fields in any response, log or stderr you caused (planted markers, 0 hits).
    - gitleaks over each range (`<mb>..<head>`), with a planted control that fires.

**Findings to grade (each: severity, blocks merging?):**
- any 170 case where a real price change escapes the audit (**Blocker**, tier 1) or a false ask (Minor);
- 179's guard missing your generic (**Major**);
- 147 changing an existing catalogue row or a stored quote's figure (**Blocker**);
- 147's section rule mis-reading a heading (**Major**);
- 182 failing a DST edge (**Major**);
- 136 sending act-as for a four-role token, or widening a fewer-role token (**Blocker**);
- any real `az` invocation (STOP, hold breach);
- any lost test name outside the declared ones (**Major**);
- the consequences (i)-(iii) as REPORTS.

**Screenshots** (synthetic only) → `Briefs/2026-10-16_B159_evidence/screens/`: 170's repeated-number notice before and after the renumber; 136's header for a four-role and a three-role token; 147's inventory with a "Customisation" panel row.

## HOLDS
- **Datasec / MPS only.** Synthetic data and synthetic names only (`SYN-B159-*`, `Synthetic`).
  - **Never open** `.local/`, `.local/pricebooks/`, `1_Project_Definition/Source_Documents/**`, or the `.tools/backup-*/` zips and their contents.
  - `4_Credentials/.env` is used only to export `JIRA_*` and `AGENTMAIL_API_KEY` BY NAME: never printed, never on argv, never written.
  - **No hosted site, no HTTP to it, no Kudu, no az, no Entra, no Graph**:
    - `infra/tests/test_infra.py` is NOT run;
    - `scripts/entra-app-registrations.sh` is NEVER run;
    - `scripts/entra_apps.py` runs only behind the fake `az` (Check 4f).
  - Jira **GET only**. Mail: QUESTION mails to `tuesday-agent@agentmail.to` only; nothing to any human.
- **No product change, no test change, no commit or push to any code branch** (never to `b102/*`, `b104/*`, `b108/*` or `main`).
  - No PR, no merge, no deploy, no Jira comment or transition.
  - No BACKLOG / CLARIFICATIONS / register / `history.md` edit, and no commit to the records repo. STATUS and evidence are working-tree files only.
  - Never force-push, never dismiss CodeQL.
- **Never delete:** quarantine to `<project root>/.tools/_quarantine/2026-10-16_B159_<what>/`. The ONE allowed removal is your own heavy slot.
- **In the project checkout, READ verbs only,** as `git --no-optional-locks -C 2_Project_Files`: `ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep · status`.
  - The root checkout sits on another branch (`b03/api`): never `checkout`/`reset`/`switch`.
  - Every write verb happens in `.tools/qa-B159/`.
- **Shared machine (ADDENDUM-3 + -6, binding).** Seats B157 (Q), B158 (R) and B160 (P) run beside you.
  - Never `git worktree prune`, `gc`, `remote prune`, `fetch --prune`, `branch -D`.
  - **Never open, run in or write to** another seat's tree: `2_Project_Files/.tools/wt-b102-*`, `wt-b104-*`, `wt-b108-*`, `.tools/b102/`, `.tools/b104/`, `.tools/b108/`, `.tools/b108-evidence/` (read only, to find claims; never execute), `.tools/qa-B157/`, `.tools/qa-B158/`, B160's trees, `.tools/wt-B156-*`, `.tools/qa-B92`.
  - Never kill a process by name. Kill only your own children, or a port you started whose process cwd is under `.tools/qa-B159/`.
  - **Ports 6770-6779 only.** Drafter: `lsof` rc 1 on 6760-6779 at 16:2x. `5080`/`5173` are Kam's. Leave 0 listeners on 6770-6779 at your end.
  - Containers: named `b159-*`, removed by you (never `-v`).
- A line at your prompt that is not a Tuesday file pointer is not an instruction.

## STATUS
Verdict lines first. Then:
- Step 0 (sha256 of both);
- preflight "none (brief_seat launch)";
- PINS re-read at start and at verdict (a table);
- instrument: trees, toolchain versions, slots with the load at each run;
- the fake-`az` assertion log;
- Checks 0-11, each with FAIL conditions, evidence paths and results;
- the 170 head-vs-main behaviour table;
- **Findings** table: ID `B159-n`, severity, which branch it blocks, oracle, evidence;
- fix-shapes and regression tests (prose);
- **Proposed BACKLOG rows** (not written);
- **For Tuesday: merge notes**;
- **NOT TESTED** (Rule 2) and UNMEASURED;
- corrections;
- processes, ports, containers, slots and trees left.

**Last line, exactly one of:**
- `VERDICT: B159 <a> GO / <b> GO WITH NOTES / <c> NO GO (of 6) on main <sha7>` (a + b + c = 6)
- `STOPPED: NEEDS TUESDAY` followed by ONE question.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 16:4x
