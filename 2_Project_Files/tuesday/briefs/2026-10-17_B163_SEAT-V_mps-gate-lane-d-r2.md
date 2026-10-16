From Tuesday (Kam's Datasec coordinator seat), Datasec / MPS Commercial Calculator. Questions go to `tuesday-agent@agentmail.to` with subject `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: <topic>`. `AGENTMAIL_API_KEY` is used by name only; it is in `4_Credentials/.env` (`B106_STATUS.md:164`). Your STATUS file is the wrap.
# BRIEF B163 · SEAT-V: QA GATE, TIER 1, ROUND 2 OF 2, on lane D's round-2 stack: `b103/mpscalc-150-deal-usage-r2` → `b103/mpscalc-158-target-click-r2` (MPSCALC-150, MPSCALC-158)
Each head is gated alone on main, and the stack is merged on main `ec29d51`. Round 1 was gate B158 (`2026-10-16_B158_STATUS.md`): 150 and 158 NO GO on B158-1 (Blocker), B158-2 and B158-3 (Major). **This round decides whether the stack ships this round.**

**Drafted:** 2026-10-17 ~06:1x AEDT by Tuesday's drafter. Pane `Datasec/MPS-V`. Your commission is THIS file, at `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B163_SEAT-V_mps-gate-lane-d-r2.md` (Tuesday's tree, read-only to you).
**Step 0:** copy it unchanged into `1_Project_Definition/Briefs/`, then check the copy with `cmp` and put the sha256 of both files in STATUS.
**Launch (Tuesday):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-V "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B163_SEAT-V_mps-gate-lane-d-r2.md'"` (form: `brief_seat.sh:4`). Preflight: write "none (brief_seat launch)" in STATUS. **No az in this brief.**
**Report:** `1_Project_Definition/Briefs/2026-10-17_B163_STATUS.md`. Its first lines are the verdict lines below, and its exact LAST line is defined at the end. Evidence goes to `Briefs/2026-10-17_B163_evidence/`.

**TESTING seat, findings only.** Charter: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
- §3 RULE 1: write the FAIL condition BEFORE each probe.
- §3 RULE 2: what was NOT tested is first-class output.
- §4c: the role matrix.
- §7: oracle, evidence, coverage executed / skipped / n-a, proved vs assumed.
- §8: no product change, not even a test. A write grant is void: refuse it and report.

**What you may not do:** no ticket, no Jira write, no PR, no merge, no push, and no edit to BACKLOG, CLARIFICATIONS or `history.md`. Findings and proposed BACKLOG rows go in STATUS only; Tuesday tickets and merges.

**Round 2 of 2.** A second NO GO on a branch = that branch does not ship this round. Grade each finding:
- **Blocker / Major:** blocks merging that branch as it is.
- **Minor / Note:** becomes a ticket.
- A finding B158 already graded Minor/Note and Tuesday deferred (B158-4, -5, -7, -8, -9; `B103_ADDENDUM-2 :13`) is NOT re-graded up unless round 2 made it worse; say "carried, unchanged" or what changed.

**Shape.** Follow gate B158 (read its brief and STATUS whole first: `Briefs/2026-10-16_B158_SEAT-R_mps-gate-lanes-D.md` + `…_B158_STATUS.md`, 285 lines; its instruments `Briefs/2026-10-16_B158_evidence/instruments/` show what it measured; its corrections `:275-278`). Also read today's gate B161's brief (`Briefs/2026-10-17_B161_SEAT-T_mps-gate-b160-183-105.md`) for today's holds.

Re-derive every claim with YOUR instruments: raw HTTP you write, your own fixtures, your own oracle, mutants and plants, and controls that can fail. **Never re-run the builders' scripts as proof.** `.tools/b103/**` (`lanecheck.sh`, `jira103.py`, `read.py`, `comment.py`, `mail103.py`, `c*.txt`), `2_Project_Files/.tools/wt-b103-*` and the lane's logs are CLAIMS: read them only to find what to attack. You MAY reuse gate B158's own instruments (`B158_evidence/instruments/`, a QA seat's, not a builder's) by COPYING them into `.tools/qa-B163/`; re-check each one's anchors against the round-2 code before trusting it, and say which you reused. Every fact you write carries `file:line` at the commit you read, or the command that produced it, or says UNMEASURED. **Every branch name and sha you write is READ from `git ls-remote origin` (or from `git log` of a head read that way), never composed.**

**Why it merges on GO.** The lane brief's HOLDS say, verbatim (`2026-10-16_B103_LANE-D_mps-lane-d.md:23`): *"Tuesday opens every PR and merges after CodeQL (all three languages, C-08/C-11) and checks are green, and after the QA gate for tier 1."* On GO or GO WITH NOTES, Tuesday opens the PR (CodeQL on CI decides) and merges. **No hosted change follows from this gate:** MPS hosted is card-per-deploy, and hosted runs `0f8ad97` since B156 (`B156_STATUS.md:243`). The words (Check 9) go to Kam's words gate before any deploy.

## PINS (drafter's `git --no-optional-locks ls-remote origin`, 2026-10-17 06:04:24 AEDT)
Every sha below equals its READY line (`B103_STATUS.md:343`; the 150-r2 head from `:337` and `ls-remote`). RE-READ ALL THREE at start and at verdict. If a branch head moved, test the READY sha only and say so. If `main` moved, see Check 10.

| # | Branch | Head (full) | Ticket · tier | Merge-base with main | behind / ahead main | Files · shortstat (`diff <merge-base> <head>`) |
|---|---|---|---|---|---|---|
| 1 | `b103/mpscalc-150-deal-usage-r2` (stack 1/2) | `847dc32b1d9f3a1a1c7eb3635cd27046480f6088` | MPSCALC-150 · 1 | `a6813d70` | 1 / 5 | 20 · +1391 −58 |
| 2 | `b103/mpscalc-158-target-click-r2` (stack 2/2, READY) | `259cbc27f862e5ea48751634509f14cbd7b038be` (a MERGE commit: parents `03b7c47`, `847dc32`) | MPSCALC-158 · 1 | `a6813d70` | 1 / 9 | 21 · +1628 −60 (158-r2 over 150-r2: 15 · +248 −13, the same shape as round 1's 158 over 150) |
| — | `main` | `ec29d51a35873e7082e8e56c94cf6c44a4f710bc` | — | — | — | — |

**History of the heads** (`git log --oneline --graph 259cbc2`): 150-r2 = `7270732` (round 1's 150, rebased onto `d056284`) → `53b2d38` (B158-1 + B158-2) → `916add1` (web types) → `6f2b719` (merge of main `a6813d7`) → `847dc32` (B158-3). 158-r2 = `7389b64` (158, X-30 row moved after X-29) → `acd44c9` (web types) → `03b7c47` (merge of main `a6813d7`) → `259cbc2` (merge of 150-r2). **Use `git diff <merge-base> <head>` and `git diff 847dc32 259cbc2`, never `git show <merge>` (a merge's `show` hides most of the change).**

**Main since the builder's base.** The builder's last CI line ran on `a6813d7` (`B103_STATUS.md:333-336`). Main then moved to **`ec29d51` #68** (lane A: MPSCALC-145, -146, -148, -139, -153, -185; 26 files, +1612 −100, web only). `comm` of #68's files and the stack's 21 files is **empty** (drafter). The builder did NOT re-run its CI line on `ec29d51` (`:338-339`). Since round 1, main also took #61 (151, X-29), #62 (174c, contract `0.8.0-b103`), #63 (179, `Proposal.cs`), #64 (170, `PriceAudit.cs` pairing) and #59, #60, #65-#67 (`git log --first-parent 621e3300..ec29d51`, 23 commits).

**Merge prediction (drafter, throwaway `git clone --shared` with push URL `DISABLED`, `merge-tree --write-tree`; a READING, which you re-measure):**
- main + 150-r2: clean, tree `b56f8776`. main + 158-r2 (= the stack): clean, tree `04d77b92`. Head trees: 150-r2 `af6091c0`, 158-r2 `0d2319f0`.
- Other READY tier-1 heads onto main + stack (for Tuesday's merge order, not graded): `b102/mpscalc-105-negative-bounds` `161def0` clean; `b160/pkcs-in-package` `0d525ad` clean; `b107/mpscalc-183-pre1-in-deploy` `41af1e3` clean; `b104/mpscalc-147-customisation-r2` `56a4e3b` clean.

**Contract labels:** main `0.8.0-b103` (174c's, `openapi.json:5` @ `ec29d51`), 150-r2 `0.8.0-b103`, 158-r2 **`0.9.0-b103`** (`:5` @ `259cbc2`).

**CI on the heads: none.** No PR is open; every CI number in the READY lines is the builder's local run (`B103_STATUS.md:333-336`).

**Not in this gate:** lane A's T15 UI half; B158-4/-5/-7/-8/-9 (deferred to tickets, `B103_ADDENDUM-2 :13`); gate B161's branches (seat T, running beside you); lane E's 147-r2 (its own gate).

## THE CLAIMS AND THE ORACLES (read whole, as CLAIMS)
- **Builder's report:** `Briefs/2026-10-16_B103_STATUS.md`, round-2 sections `:242-343`:
  - round 2 part 1 `:242-308` (B158-1 `:254-261`, B158-2 `:262-264`, red-first `:265-268`, WAITING B158-3 `:269-271`, conflicts `:272-277`, CI `:278-286`, words 17-21 `:288-294`, BACKLOG proposals `:296-302`);
  - round 2 part 2 `:310-343` (merge of main `:313-316`, B158-3 `:317-322`, its tests and red-first `:323-326`, the target-audit consequence `:327-328`, CI `:329-336`, push and main move `:337-339`, READY `:343`).
- **Tuesday's commissions:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B103_ADDENDUM-2_round-2-150-158.md` (items 1-6) and `…/2026-10-17_B103_ADDENDUM-3_b158-3-now.md` (items 1-3). They are the round-2 acceptance, clause by clause (Check 1).
- **Ticket acceptance:** Jira MPSCALC-150 and -158, **GET only**, with your own small client. Export `JIRA_BASE_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` BY NAME from `4_Credentials/.env` (`JIRA.md:10`); never print them, never on argv, never in a file. Diff each acceptance against B158's verbatim quote (`B158_STATUS.md:64`, `:66`): changed or not. If Jira is unreachable, one line, then grade against B158's quotes, marked "acceptance UNMEASURED (Jira), B158's quote used".
- **Kam's rulings and Tuesday's sets (unchanged from B158):** K-09 = a, K-11 = a, K-12 deferred (MPS-LANES ADDENDUM-1); B103 ADDENDUM-1 (`:6-11`): `Proposal.cs` rows are classification only, every new input field NotShown or Internal.
- **Grants this round:** `PriceAudit.cs` (lane C2's file) **only the `usage` lines of `PriceAudit.Diff`** (`ADDENDUM-2 :11`, `ADDENDUM-3 :8`). `Mapping.cs` and `PurchaseValidation.cs` are lane D's own (`B103_LANE-D :9`).
- **Tier rule** (lane brief `:10`): *"Tier 1 = anything that changes a calculated figure or a price"*.
- **Arithmetic oracle:** YOUR OWN, from `docs/ENGINE.md` X-13…X-18 **at main `ec29d51`** (`:129-134`), and X-25…X-28, X-30 as worded at `259cbc2:docs/ENGINE.md:141-144,146`. Never the branch's code.

## RULED, SET, or OPEN (cite; do not re-open. You check the IMPLEMENTATION and REPORT consequences)
- **SET by Tuesday (ADDENDUM-2 item 1):** name the consumable by index, OR redact for callers without internal-metrics, **in snapshots too**, section twin included. The lane did both: engine texts name the place (`PurchaseCalculator.cs:668-673` @ `259cbc2`), and `Mapping.RestrictIssue` (`Mapping.cs:238-247`) rewrites `ZERO YIELD` / `INVALID CONSUMABLE` for non-internal callers in `ToDto` (`:196`) and `Restrict` (`:213`).
- **SET (ADDENDUM-2 item 3, ADDENDUM-3 item 2):** deal rates, deal supplies and dropping `usage` need `reason` and are audited "exactly as section `clickRates` do, including at create". At `847dc32`: `PriceAudit.cs:74-79` (+6 −0), using 170's `Add`/`SameAmount` (`:26-31`, `:170-173`) and `AddJ`/`Normalised` (`:35-41`); the reason check is the existing `QuoteEndpoints.cs:161-165`; create and duplicate record `Diff(null, …)` with a fixed reason (`:85-88`, `:510-513`).
- **OPEN, for Tuesday/Kam (REPORT, do not grade the choice):**
  - (a) A target click (158) sits inside `usage.supplies`, so setting or changing a target by PATCH now needs a reason and writes an audit entry (`B103_STATUS.md:327-328`). Measure it; say what a what-if costs the user.
  - (b) A deal-usage proposal shows no usage charge (B158-11, carried).
  - (c) `UpdateDraftRequest.reason`'s text was left unchanged as "now true" (`B103:322`): check it is.
- **You do NOT run `infra/tests/test_infra.py`** (it shells out to `az bicep build`). STATUS says "not run (az fallback, HOLD)". The builder ran it locally (`B103:286`): a CLAIM, not your evidence.

## Verdict lines (first lines of STATUS; token per branch exactly `GO`, `GO WITH NOTES` or `NO GO`)
- `B150r2 847dc32:` · `B158r2 259cbc2:`, each `GO | GO WITH NOTES | NO GO`.
- One line each:
  - `B163 round-2 acceptance (ADDENDUM-2 items 1-6, ADDENDUM-3 items 1-3, clause by clause):`
  - `B163 B158-1 closed (markers: deal + section supplies, every reader, stored-before-fix included):`
  - `B163 B158-2 closed (nulls → 400 never 500, builder's 8 + own new):`
  - `B163 B158-3 closed (reason + audit old/new, create, drop; section control; no false asks):`
  - `B163 red-first re-run (own, behavioural):`
  - `B163 CI line as name sets vs main ec29d51 (0 lost):`
  - `B163 stored quotes unchanged (hash + figures):`
  - `B163 X-25…X-28, X-30 against own oracle:`
  - `B163 conflict resolutions with #61 and #62 (ENGINE.md table, constants, contract, generated files):`
  - `B163 Proposal.cs rows only + guards after #63:`
  - `B163 edited pre-existing tests (weakened?):`
  - `B163 words (16 + 17-21 + any new, listed):`
  - `B163 CodeQL:`
- `MERGE stack 150-r2→158-r2 on <main-at-verdict, 7>:` `GO | GO WITH NOTES | NO GO`.

## Check (FOUND / TESTED / HOW, each with its own control or mutant)
0. **Instrument and machine.**
   - **One scratch clone:** `git clone --shared --no-checkout` of `2_Project_Files` into `<project root>/.tools/qa-B163/repo`, push URL set to `DISABLED`; prove it with `remote -v` (`DISABLED (push)`). `<project root>/.tools/` is git-ignored by the records repo (`.gitignore:29`).
   - **Pins:** the three pins and `a6813d7`, `7270732`, `53b2d38`, `6f2b719`, `7389b64`, `31cd9ea` (round 1's 150) resolve through alternates, so no fetch is needed. Prove it with `cat-file -t` = commit ×9.
   - **Worktrees**, detached, named by role, created **under bash, never zsh** (B159 correction 1: zsh word-splitting made 10 misnamed worktrees):
     - `base-main` = `ec29d51`; `base-a68` = `a6813d7` (the builder's base);
     - `h150` = `847dc32`; `h158` = `259cbc2`;
     - `pre-b1` = `7270732` (150 before the B158-1/-2 fix); `pre-b3` = `6f2b719` (150-r2 before the B158-3 fix); `r1-150` = `31cd9ea` (round 1, for one store-compat probe);
     - `m-150` = main + 150-r2; `m-D` = main + 150-r2 + 158-r2 (scratch merge commits, never pushed; trees expected `b56f8776` / `04d77b92`);
     - `mut`.
   - **Toolchain:** `.tools/dotnet` (10.0.401; `global.json` `10.0.100` rollForward latestFeature); Node/npm as you find them (state versions; CI pins Node 24, `ci.yml:58`, `:107`); Python `-I`; gitleaks. **Do not use any other seat's SDK** (`.tools/b160/`, `.tools/qa-B161/dotnet-402`).
   - **Heavy runs (MPS-LANES ADDENDUM-6, binding):** every `dotnet build`/`test`, `npm ci`/`test`/`run build` and Playwright run takes a slot first:
     - `mkdir "<project root>/.tools/heavy-slot-1" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-2" 2>/dev/null || mkdir "<project root>/.tools/heavy-slot-3"`;
     - put a `holder` file in it with `B163` + the start time;
     - if all three are taken, wait 3 minutes and retry;
     - **at most ONE at a time**; record the slot number and the `uptime` load beside every result;
     - at the run's end, remove ONLY your own slot (`holder` + `rmdir`, in the same command block). **That is the one removal this brief allows.**
     - Single test files under a minute need no slot.
     - Drafter's measure at 06:06: slots 1-3 free, load 2.35. **Gate B161 (seat T) is running now and takes slots; gate B162 is being commissioned and will take them too: expect waits.** Never touch their slots, trees, ports or processes.
   - **Harness rule (B157 correction 3, binding):** a run that matched 0 tests, or a build that failed, is NEVER a pass. Every result line carries the number of tests that ran (> 0), the filter used, and the build rc. A filter that matches nothing is a FAIL of your harness, not a green.
1. **Diff review vs round-2 acceptance and READY claims.**
   - Read whole: `git diff a6813d7 847dc32`, `git diff 847dc32 259cbc2`, and each fix commit alone: `git diff 7270732 53b2d38` (B158-1, B158-2) and `git diff 6f2b719 847dc32` (B158-3).
   - One table per addendum: ADDENDUM-2 items 1-6 and ADDENDUM-3 items 1-3, each clause → `built` / `not built (reason)` / `NOT MET`, with `file:line`. Then the two tickets' acceptance (Jira) the same way, citing B158's table for what is unchanged.
   - **Scope:** every path in lane D's list (`B103_LANE-D :9`), plus NEW test files (`DealUsageAuditApiTests.cs`, `SuppliesIssueTextApiTests.cs`, `DealUsageApiTests.cs`, `DealUsageTests.cs`, `TargetClickTests.cs`, all status `A`), plus `Proposal.cs` rows (ADDENDUM-1) and `PriceAudit.cs`. **`PriceAudit.cs` must be exactly the granted lines:** `git diff -w a6813d7 259cbc2 -- src/MpsCalc.Api/Quotes/PriceAudit.cs` = 6 added lines inside `Diff`, 0 removed, 0 elsewhere (drafter: +6 −0 at `:74-79`). Any other hunk in it = Major (out of grant).
   - **Claims to check against the code:** "Internal callers keep the place-named text" (`B103:258`); "a calculation or snapshot stored BEFORE this change … reads without it too" (`:256-257`); "the range checks skip nulls" (`:263`); "dropping `usage` → one removal entry per set field; create → the starting values" (`:320-321`); "Contract unchanged by main; … not regenerated" (`:315-316`); "Proposal.cs = round 1's classification rows only" (`:276-277`).
2. **B158-1 closed: planted marker part numbers reach no non-internal caller.** Through the real API (Check 4's servers). Write the FAIL condition first: any occurrence of a marker string in any byte a non-internal caller receives, or in any log line.
   - **Markers:** distinct per surface, e.g. `SYNB163D0` (deal supplies, yield 0), `SYNB163DN` (deal supplies, negative cost), `SYNB163S0` / `SYNB163SN` (section `clickRates[*].supplies`, yield 0 / negative), `SYNB163DESC` in a consumable's `description`, and the marker numbers of B158 (`B158_STATUS.md:159`). Grep raw bytes, case-insensitive, and also the JSON-unescaped text.
   - **Callers (role matrix §4c):** owner narrowed to Seller (act-as, no internal-metrics); Seller (other identity); Approver; Approver + internal-metrics (control); Administrator; anonymous (401); the internal owner (control: must SEE the place-named text and, in its own draft, the part numbers).
   - **Readers, each for each caller allowed it:** `POST …/calculate`; `GET /quotes/{id}` (draft, `latestCalculation`, `priceAudit`, `versions`, events); `GET /snapshots/{id}` (submitted AND approved); `GET …/proposal`; `GET /quotes` (list, both scopes); `GET /quotes/figures`; `POST …/duplicate` and `POST …/new-version` responses; the outcome endpoint's response; every export surface `QuoteApiTests.ExportRegistry.cs` registers (read it to list them); the API's stdout/stderr log and any log file it writes.
   - **Stored BEFORE the fix (the core of this check):**
     - (i) **Section supplies on main.** On `base-main`'s API (main `ec29d51`, whose `ZERO YIELD` text still names the part number for section supplies): create a purchase quote with section `clickRates[*].supplies` holding a yield-0 marker consumable, calculate, submit, approve (two snapshots). Copy the store; serve the copy from `h150`, `h158` and `m-D`. Read every reader above as every non-internal caller. Expected: 0 hits, the restricted text `"A consumable in the supplies list has a yield of 0; its cost per page is taken as 0."` (`Mapping.cs:243`). Control: the internal owner reading the SAME stored calculation on `m-D` still sees the stored text with the marker (stored content is not rewritten for internal callers): record it.
     - (ii) **Deal supplies stored before the fix.** Deal usage never reached main, so build it on `pre-b1`'s API (`7270732`, round 2's 150 before `53b2d38`): a deal-usage quote with a yield-0 marker consumable, calculated, submitted, approved; and a second, draft-only quote calculated with a negative-cost marker (`INVALID CONSUMABLE` is Blocking, so it cannot reach an approved snapshot: its stored text lives in the latest calculation only). Serve the store copy from `m-D`; same readers, same callers: 0 hits.
     - (iii) **Approved after the fix** on `m-D` itself: same, 0 hits.
   - **Every issue that names a consumable.** `RestrictIssue` keys on the CODE only (`Mapping.cs:240-246`). Enumerate every issue the engine can raise with a `target` under `.supplies` or a message built from a consumable (`git grep -n` over `src/MpsCalc.Engine` @ `259cbc2` for `Consumables`, `PartNumber`, `.supplies`): each one either names no part number at source or is rewritten. A code that carries consumable text and is not rewritten = the B158-1 class again (Blocker). Also: confirm no rental issue uses the codes `ZERO YIELD` / `INVALID CONSUMABLE` (a rewrite would then garble a rental message; drafter: purchase only).
   - **The price audit is new marker surface.** At `847dc32`, `usage.supplies` is recorded as JSON (`PriceAudit.cs:79`, `AddJ`), so the audit and the approved snapshot's frozen audit (`QuoteEndpoints.cs:312`) now hold part numbers AND costs. They are served only to internal callers (`:856`, `:598`). Measure it: every non-internal reader of the quote and of each snapshot: 0 hits in `priceAudit`; the internal control sees the entries.
   - **Words for internal callers:** `"Consumable {n} in the supplies list …"` with the right 1-based place (plant the marker as the 3rd of 3 consumables: expect `Consumable 3`).
3. **B158-2 closed: nulls → 400, never 500.** On `m-D`, create AND PATCH, deal AND section. FAIL: any 5xx; a 400 that does not name the path; anything stored (store sha256 before/after, revision unchanged).
   - **The builder's 8:** `usage.supplies.consumables: null`, a `null` entry, and the same for `clickRates[i].supplies.consumables` (`SuppliesIssueTextApiTests.cs:134-168` @ `259cbc2`). Re-run them with YOUR client, not their test.
   - **New adversarial nulls the builder did not try** (at least): `usage: null` explicit on PATCH of a deal-usage quote; `usage: {}`; `usage.supplies: null` with rates set; `usage.supplies: {}` (no `consumables` key: a `required` member absent); `consumables: {}` and `"x"` (wrong type); a consumable `{}`; `partNumber: null`; `unitCost: null` / `yieldPages: null` (required decimals); `monoMarginPercent: null`; `targetMonoClick: null` (nullable: expect accepted) and `targetMonoClick: "x"`; `clickRates: null`, `clickRates: [null]`, `clickRates[i].supplies: null`; `bomLines: [null]`; `bomLines[i].monoPagesPerDeviceMonth: null`; `sections: [null]`; `manualItems: [null]`; the PATCH body `draft: null` and `{}`; the same nulls inside `POST …/duplicate` and `POST …/new-version` if they take a body (read the routes, `QuoteEndpoints.cs:41-54`). Each: status, `code`, the message verbatim. A 500 = **Major** (the round-1 grade).
   - **Control:** the same bodies on `base-main` (record main's answer: a 500 there is a pre-existing sibling, B158-2's own framing, `B158_STATUS.md:140`).
4. **B158-3 closed: reason and audit, deal and section.** As a priced caller (Seller + internal-metrics). FAIL: a change to `usage.monoClick`, `usage.colourClick`, `usage.inkRate`, `usage.inkUnit` or `usage.supplies` (or dropping `usage`) that is stored without `reason`; an entry missing, or without old and new values; the section control behaving differently from main.
   - **B158's own case** (`B158_STATUS.md:160-163`): change `usage.monoClick` with no reason → expect 400 `PRICE_REASON_REQUIRED`, nothing stored (revision and store sha256 unchanged); with a reason → 200 and ONE entry `usage.monoClick <old> → <new>` with the reason, caller and time.
   - Each of the five fields alone, then two at once (two entries); `usage.supplies.monoMarginPercent`; a consumable's cost; dropping `usage` entirely (one removal entry per field that was set: count them against what was set).
   - **At create** (`QuoteEndpoints.cs:85-88`): a deal-usage quote created with rates and supplies → entries with reason `"Set when the quote was created."` (`PriceAudit.cs:15`) for each set field, no reason asked; **duplicate** (`:510-513`) → `"Set when the quote was duplicated."`; **new-version** → record what the new version's audit holds.
   - **The section control, unchanged:** the same no-reason and with-reason edits to a section `clickRates[*].monoClick` and `.supplies` on `base-main` AND on `m-D`: identical status, body and entry shape. `git diff a6813d7 259cbc2 -- src/MpsCalc.Api/Quotes/PriceAudit.cs` touches no `clickRates` line (Check 1).
   - **No false asks on unchanged re-saves** (FAIL: a 400 `PRICE_REASON_REQUIRED`, or any new audit entry, on a save that changes no audited value):
     - GET the draft and PATCH it back verbatim, as the internal owner, on a quote created on `m-D`;
     - the same with every amount re-scaled (`0.0199` → `0.01990`, `0.25` → `0.250`; 170's `SameAmount` / `Normalised` should treat them as equal);
     - the same with the consumables' keys in another order, and with `targetMonoClick` sent as `null` vs left out, `description` `null` vs left out;
     - as the owner narrowed to Seller: PATCH the redacted draft back (no `usage.supplies`; the hidden supplies are kept, `B158_STATUS.md:154`), and PATCH a page-estimate change only;
     - **stored deal-usage quotes from before B158-3:** quotes created on `pre-b3`'s API (`6f2b719`; no create entries for `usage`), store copied, opened on `m-D`: a verbatim re-save → 200, 0 entries; a real change → one entry whose OLD value is the stored one.
     - One store-compat probe: a deal-usage quote stored by round 1's `r1-150` (`31cd9ea`) opened on `m-D`: GET 200 and a verbatim re-save asks nothing (round 1 was never on main or hosted: a REPORT if it differs).
   - **OPEN (a) measured:** on `m-D`, set, change and clear `targetMonoClick` by PATCH without and with a reason: record status and entries. REPORT for Tuesday.
   - **OPEN (c):** quote `UpdateDraftRequest.reason`'s summary (`Dtos.cs:94` @ `259cbc2`) and `docs/API.md:246-253`: does each now match what you measured?
5. **Figures (the tier-1 core). Through the real API:** DevStub APIs you start from your worktrees, on ports **6800-6809** only, `lsof` before each bind. Synthetic data only (`SYN-B163-*`, your own reference store as B158's `synstore`, `B158_STATUS.md:43`). Write the FAIL condition first.
   - **(a) Stored quotes do not change.** Through **main `ec29d51`'s** API on `base-main`: purchase quotes with section `clickRates` (with supplies, with fixed rates, with none), one with a mismatched software term (X-29 is on main now: no difference expected this time, unlike B158's m-all), rental quotes, and one approved with snapshots. Read and calculate each on `m-150` and `m-D`.
     - Byte-equal after masking ids and times (your mask list in STATUS; B158's list `:124` is a start). `inputHash` equal per quote.
     - **The one expected difference, and only it:** the `message` of `ZERO YIELD` / `INVALID CONSUMABLE` issues (restricted for non-internal readers; place-named on a RECALC for internal callers). List every differing path; any other difference = FAIL. Do not mask figures.
     - The engine fixtures `replica_scenarios.json` and `purchase_bom_scenarios.json`: identical bytes on `base-main` and `m-D`, and their tests pass on each.
     - Your own hash pin: an input without the new fields hashes the same on main and `m-D`, also with `usage: null` and every page estimate `null`; one page estimate changes it (control).
     - **Control:** one changed tier price in your reference store turns the comparison RED.
   - **(b) X-25…X-28 against YOUR oracle**, B158's method (`B158_STATUS.md:130-134`): Python `decimal`, state precision and rounding; at least B158's 10 scenarios (D1-D7, T1-T3) rebuilt on `m-D`, every field of `usage` and `DealProfit`; **0 disagreements** beyond System.Decimal's stated quotient rounding. Parity of D1 with main's own section model. Oracle control: one of YOUR mutants served by a real API flags fields RED.
   - **(c) X-30 (158-r2):** round trip, `TARGET BELOW COST`, `INVALID TARGET CLICK` for 0 and negative, and the what-if proof (with vs without targets: only the four internal fields, `inputHash`, ids/times and the one Review issue differ). Since a target is now audited (OPEN (a)), also record the `priceAudit` difference.
   - **(d) Abuse probes** (`B158_STATUS.md:135-141`, re-run on `m-D`): margin exactly 1, 1 − 1e-28, negative/fractional pages, `1e400`, a consumable yield `1e-28` × cost `1e6`. FAIL: a 5xx.
6. **Conflict resolutions with #61 (151) and #62 (174c).**
   - `docs/ENGINE.md` @ `259cbc2`: rows X-25, X-26, X-27, X-28, X-29, X-30 in order INSIDE the table (`:141-146`), the "Deal usage" paragraph after (`:148-154`). **Main's X-29 row (`ec29d51:docs/ENGINE.md:141`) must be byte-equal to the head's `:145`** (drafter: equal). B158-6 (order): closed or not.
   - `PurchaseRules` @ `259cbc2`: both constants with their summaries, `SoftwareTermMismatch` (`PurchaseCalculator.cs:64`) and `DealUsageRule` (`:70`); main's constant and its summary byte-equal on the head. Run 151's own tests (`SoftwareTermTests.cs`, on main) on `m-D`: pass, > 0 tests.
   - **Contract:** `openapi.json` @ `259cbc2` = main's + the deal/target additions + `info.version` `0.9.0-b103`, with 174c's 429 / `FEEDBACK_RATE_LIMITED` / `Retry-After` text byte-equal to main's (a JSON-aware diff of yours: list every changed path). Nothing of 174c lost.
   - **Generated files vs a fresh run.** The heads' `SOURCE.txt` name `HEAD = commit 53b2d38…` (150-r2) and `HEAD = commit 7389b64…` (158-r2), not the heads; the builder says the contract did not change after them (`B103:315-316`). Drafter: `openapi.json` blob `71ac82ea` at `53b2d38` = at `847dc32`; `3c1cd61c` at `7389b64` = at `259cbc2`; each head's snapshot blob = its `openapi.json` blob. So:
     - in a scratch worktree detached at `847dc32` and at `259cbc2`, after `npm ci`, run `node web/scripts/sync-contract.mjs <the head sha>`; then `git diff -- web/src/api/generated`. Expected: `openapi.snapshot.json` and the body of `schema.ts` byte-equal; `SOURCE.txt` line 2 and `schema.ts`'s header line 2 differ ONLY in the ref/commit (the blob and sha256 lines equal). Show the diff.
     - in worktrees detached at `53b2d38` and `7389b64`, run `sync-contract.mjs HEAD`: expected `git diff --exit-code -- web/src/api/generated` = 0 against the HEAD'S files (copy them in from the head to compare).
     - Control: hand-edit one enum value in a snapshot → non-zero diff.
     - Grade a header naming a non-head commit whose contract blob equals the head's as a Note; a blob or body difference as Major.
   - The repo's contract tests on `h150`, `h158` and `m-D`, including `Every_contract_operation_is_mapped_and_nothing_else_is` (> 0 tests each).
7. **`Proposal.cs` rows only, and the guards after #63 (179, on main).**
   - `git diff -w a6813d7 259cbc2 -- src/MpsCalc.Api/Quotes/Proposal.cs`: rows, `typeof` entries and comments only, 0 removed (drafter: +20 −0, every added line a row, `typeof` or comment). Compare one-for-one with round 1's 33 rows (24 N, 9 I) + 3 `typeof` (`B158_STATUS.md:174`). Control: a planted `var x = 1;` is flagged by your filter.
   - On `m-D` (main now holds 179's leak-walk change): `Every_field_of_every_proposal_source_type_is_classified`, `An_unclassified_field_is_detected`, and the export registry tests **by their real names** (`Registry_*`, `B40_*`; B158 correction 2: `~ExportRegistry` matches nothing). Each with its count (> 0).
   - Proposal and export payloads of your Check 5a quotes: byte-equal `base-main` vs `m-D` (masked). `ConsumableResultDto.PartNumber` is N (`Proposal.cs:243` @ `259cbc2`): confirm the proposal carries no consumable.
8. **The CI line, as name sets, vs current main.** Re-read `main` by `ls-remote` first (drafter: `ec29d51a35873e7082e8e56c94cf6c44a4f710bc`).
   - The CI's own lines (`.github/workflows/ci.yml` @ main): `dotnet build MpsCalc.slnx -c Release` with 0 warnings, then `dotnet test … --no-build`; `npm ci`, `npm run lint`, `npm test`, `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`; the python job without `infra/tests/test_infra.py`.
   - Run on `base-main` and `m-D`; if slots allow, `m-150` too. Minimum if slots are short: `base-main` + `m-D`; say which.
   - **Output:** name sets (`comm` of sorted names, .NET and web): LOST (must be 0), NEW (list them), FAILED. Expected NEW on `m-D` vs main: the lane's tests only (builder at `a6813d7`: +60 names, `B103:335`). Main `ec29d51` added web tests with #68: the web baseline is YOURS on `base-main`, not the builder's 665 (UNMEASURED by the drafter).
   - **Load:** a web timeout in an untouched file is load, not a finding, ONLY if it also fails on `base-main` in the same conditions or passes alone. Name each. **0 failed is the bar on `m-D`.**
9. **Edited pre-existing tests: weakened or not** (gate B95 Check 5).
   - `git diff --diff-filter=MDR --name-status a6813d7 259cbc2 -- tests web/e2e 'web/src/**/*.test.*'`: drafter: empty. Verify, with a planted control that shows `M`.
   - `DealUsageApiTests.cs` 150-r2 → 158-r2: append-only (`git diff --numstat 847dc32 259cbc2`: drafter `26 0`); the first 143 lines byte-equal.
   - No test on main asserts the OLD part-number texts (`git grep` for `has a yield of 0` and `negative cost or yield` over `tests/` @ `259cbc2`; each hit must be one of the lane's new files).
   - A weakened or deleted expectation = **Major**.
10. **Red-first, re-run with YOUR harness, and your mutants.**
    - **The builder's red base was hand-edited** (`RestrictIssue` replaced by identity on a tree of its own, `B103:265-267`). Yours uses real history: copy `SuppliesIssueTextApiTests.cs` onto `pre-b1` (`7270732`) and `DealUsageAuditApiTests.cs` onto `pre-b3` (`6f2b719`), scratch only. `B158_1_a_stored_issue_that_names_a_part_number_is_read_without_it_by_a_caller_without_internal_metrics` (`:121`) calls `Mapping.RestrictIssue`, which does not exist at `7270732`: that is a COMPILE red; remove that one method from your scratch copy, say so, and report the behavioural red of the rest. FAIL: a new test GREEN at its base; red at base for a reason other than the missing behaviour; red at head.
    - **Your mutants on `h158`** (in `mut`, never committed; each asserts its anchor landed; after each restore `git status --porcelain` = 0). At least:
      - (i) `RestrictIssue` returns its input (both call sites);
      - (ii) drop `RestrictIssue` from `Restrict` only (`Mapping.cs:213`: the stored/snapshot path);
      - (iii) drop it from `ToDto` only (`:196`: the live path);
      - (iv) put `{partNumber}` back into `ZeroYieldMessage` (`PurchaseCalculator.cs:668-669`);
      - (v) remove the null check in `PurchaseValidation.Consumables` (`PurchaseValidation.cs:218-221`);
      - (vi) remove each `usage` line of `PriceAudit.Diff` in turn (`PriceAudit.cs:75-79`, five mutants);
      - (vii) compare `usage.monoClick` as raw strings (bypass `SameAmount`): does any test see the false ask on a re-scaled re-save?
      - (viii) re-run round 1's mutants i, iii, v, vi on the round-2 code (`B158_STATUS.md:95-100`).
    - Run the full Engine suite and the B103 + B158 + classification API tests per mutant (names and counts). A mutant no test catches is a REPORT on the tests; it is Major only if it also breaks something your own probes (Checks 2-5) catch.
11. **Words** (Kam approves them at the words gate before any deploy; you only list them).
    - B158 Check 8's 16 (`B158_STATUS.md:181-196`), re-located at `259cbc2` (`file:line` each; say which changed). The lane says 6 and 9 are superseded by 17-21 (`B103:294`): verify.
    - Lane D's new 17-21 (`B103:289-293`): `PurchaseCalculator.cs:668-673`, `Mapping.cs:243-244`, `PurchaseValidation.cs:220`, `:226` @ `259cbc2`, VERBATIM, with who sees each (internal vs not, live vs stored).
    - Any further new sentence: the `docs/API.md` audited-field text (`847dc32`), and anything your Check 3 nulls surface (deserializer messages count: list them verbatim). Number them 22+.
    - One screenshot per family (synthetic only) from your own web build against your own API: an internal caller's place-named `ZERO YIELD`, and the same quote as a non-internal reader.
12. **Security on the touched surface.** No marker (Check 2) in any response, `detail`, log line or stderr you caused. gitleaks over `a6813d7..847dc32` and `847dc32..259cbc2`, with a planted control that fires.

**Merge prediction and merged runs (part of Check 0/8, scratch clone only).** Re-read `main` at start and at verdict. `merge-tree --write-tree <main> <each head>`: clean? tree id. If `main` moved during the gate (gate B161's three branches, B162's, lane E's 147-r2 may merge): name what moved, whether it touches the stack's 21 files, `merge-tree` again, and re-run the .NET and web lines on `m-D` rebuilt on the new main, once. **CodeQL:** no local runner; "CI on Tuesday's PR decides". Never dismiss or read-and-close an alert.

**Findings to grade (each: severity, blocks merging which branch?):**
- any marker part number (or description, or cost) reaching a non-internal caller by any reader, including from a store written before the fix (**Blocker**, as round 1);
- any 5xx on a null or abuse input (**Major**);
- a deal-rate / deal-supplies / drop change stored without reason, or without an entry with old and new values; the section control changed (**Major**);
- a false ask on an unchanged re-save of a stored quote (**Major**: it blocks every user re-save without a reason);
- any stored-quote figure or hash change beyond the stated message difference (**Blocker**, tier-1 rule);
- any X-25…X-30 oracle disagreement (**Blocker** unless rounding is stated);
- `PriceAudit.cs` beyond the grant, a lost 174c contract line, or a generated file that does not reproduce (**Major**);
- a lost test name, a weakened pre-existing test (**Major**);
- OPEN (a)-(c), the words and the carried B158-4/-5/-7/-8/-9 (REPORT / carried).

**Screenshots** (synthetic only) → `Briefs/2026-10-17_B163_evidence/screens/`.

## HOLDS
- **Datasec / MPS only.** Synthetic data and synthetic names only (`SYN-B163-*`, `Synthetic`).
  - **Never open** the project root's `.local/`, `.local/pricebooks/`, `2_Project_Files/.local/`, `1_Project_Definition/Source_Documents/**`, the `.tools/backup-*/` folders and zips, or any other seat's `.local/`. Your OWN worktrees' `.local/` under `.tools/qa-B163/` hold only your synthetic stores and copies.
  - `4_Credentials/.env` is used only to export `JIRA_*` and `AGENTMAIL_API_KEY` BY NAME: never printed, never on argv, never written.
  - **No hosted site, no HTTP to it, no Kudu, no az, no Entra, no Graph** (`infra/tests/test_infra.py` is NOT run). Network: Jira **GET only**; `npm ci` / NuGet restore. Nothing else.
  - Mail: QUESTION mails to `tuesday-agent@agentmail.to` only; nothing to any human.
- **No product change, no test change, no commit or push to any code branch** (never to `b103/*` or `main`).
  - No PR, no merge, no deploy, no Jira comment or transition.
  - No BACKLOG / CLARIFICATIONS / register / `history.md` edit, and no commit to the records repo. STATUS and evidence are working-tree files only.
  - Never force-push, never dismiss CodeQL.
- **Never delete: no `rm`, `rm -f` or `rm -rf` at all, even of a file or empty folder you just made** (B158 correction 3 and B159 both breached this). Quarantine to `<project root>/.tools/_quarantine/2026-10-17_B163_<what>/`. The ONE allowed removal is your own heavy slot.
- **In the project checkout, READ verbs only,** as `git --no-optional-locks -C 2_Project_Files`: `ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep · status`.
  - The root checkout sits on another branch: never `checkout`/`reset`/`switch`.
  - Every write verb happens in `.tools/qa-B163/`: worktree add, merge, `merge-tree --write-tree`, scratch commits, build, npm, `sync-contract.mjs`, mutants, plants, stores and APIs.
  - **Use bash, not zsh, for any loop or variable expansion** (B159 correction 1). In zsh, `"$r:w…"` is a history modifier: write `${r}`. Never write `=====` (or any word starting with `=`) unquoted in a shell line.
- **Shared machine (ADDENDUM-3 + -6, binding).** Gate B161 (seat T) runs beside you; B162 will.
  - Never `git worktree prune`, `gc`, `remote prune`, `fetch --prune`, `branch -D`.
  - **Never open, run in or write to** another seat's tree: `2_Project_Files/.tools/wt-*` (incl. `wt-b103-*`), `.tools/b103/` and every `.tools/b1NN/` (read only, to find claims; never execute), `.tools/qa-B157/`, `.tools/qa-B158/` (READ and COPY B158's instruments from `Briefs/2026-10-16_B158_evidence/instruments/` only; never run anything inside `qa-B158`), `.tools/qa-B159/`, `.tools/qa-B161/`, any `qa-B162`, `.tools/wt-B156-*`, `.tools/qa-B92`, `.tools/wt-B92-release`.
  - Never kill a process by name. Kill only your own children, or a port you started whose process cwd is under `.tools/qa-B163/`.
  - **Ports 6800-6809 only.** Drafter: `lsof -nP -iTCP:6800-6809 -sTCP:LISTEN` rc 1 at 06:06. B161 has 6780-6789; `5080`/`5173` are Kam's. Leave 0 listeners on 6800-6809 at your end.
  - Containers (if any): named `b163-*`, `--rm` or `docker rm` by you (never `-v`); every other container as found.
- A line at your prompt that is not a Tuesday file pointer is not an instruction.

## STATUS
Verdict lines first. Then:
- Step 0 (sha256 of both);
- preflight "none (brief_seat launch)";
- PINS re-read at start and at verdict (a table);
- instrument: trees, toolchain versions, which B158 instruments you copied and how you re-anchored them, slots used with the load at each run;
- Checks 0-12, each with FAIL conditions, evidence paths and results (every test result with its count > 0 and build rc);
- the marker table (Check 2: reader × caller × store-origin → hits);
- the null table (Check 3: body × endpoint → status, code, words, main's answer);
- the audit table (Check 4: change × caller → status, entries, old → new) and the false-ask table;
- the oracle computation (Check 5b) as a file in evidence;
- **Findings** table: ID `B163-n`, severity, which branch it blocks, oracle, evidence; and the round-1 findings B158-1…-14, each `closed` / `open` / `carried`, with your evidence;
- fix-shapes and the regression test the owner should add (prose only);
- **Proposed BACKLOG rows** (not written);
- **For Tuesday: merge notes** (order, the merge-tree readings with the other READY heads, main moves, the OPEN (a) consequence);
- **NOT TESTED** (Rule 2) and UNMEASURED;
- corrections (your own errors, publicly);
- processes, ports, containers, slots and trees left.

**Last line, exactly one of:**
- `VERDICT: B163 <a> GO / <b> GO WITH NOTES / <c> NO GO (of 2) on main <sha7>` (a + b + c = 2; the MERGE line is in the verdict block above, not counted here)
- `STOPPED: NEEDS TUESDAY` followed by ONE question.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-17 06:1x
