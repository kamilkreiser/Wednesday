# B573 DRAFTER REPORT (2026-10-24, Sonnet drafter, read-only; reads between 10:10 and 10:16 AEDT per `date`)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B573_SEAT-M11_mps-106-fix-round-2.md` (82 lines; sha256 `aa5e9bdd5d6229154303085379e8939a355bd2ecc89901d7ab7e4b33e3aa54dc`) and its `.pre-stamp` copy (`cmp` rc 0, same sha256). Unstamped copy reads **8** lines with the four-underscore pattern (`/usr/bin/grep -c -E '_''_''_''_'`; 7 slot lines at 67-73, all ending `  ____`, and the last line 82); control: a scratch file `a____b` reads 1. Non-ASCII bytes: 0 (`LC_ALL=C grep -c '[^ -~]'`; the first draft had two lines with a middle dot, replaced). Nothing launched, committed, pushed or posted; only the three files named were written.

## What I read (paths, shas)
- Gate STATUS `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/1_Project_Definition/Briefs/2026-10-24_B567_STATUS.md` (356 lines, whole): verdict line 1; C4 mutant table lines 99-129 (M11, M12, M18); findings B567-5 `:270-278`, B567-6 `:280-286`; Notes `:288-296`; FACTS `:300-309`; ROUND-CAP STATEMENT `:311-317`; UNMEASURED `:345-353`.
- Template `briefs/2026-10-24_B568_SEAT-M9_mps-102-fix-round-3.md` (80 lines, whole) and its `.pre-stamp` (slot lines 64-70 and 79; slot form `- LABEL:  ____` at line end).
- B565 brief `briefs/2026-10-24_B565_SEAT-M8_mps-readiness-reconciliation-hardening.md` (106 lines, whole): heavy-slot mechanism (STANDING LINE 7), NuGet home line, shell/word-split lines, PARTITION, intersection program. B565 STATUS (`Briefs/2026-10-24_B565_STATUS.md`, 227 lines): grep only (CI line `:144`, names `:146`, slot release `:222`).
- Project `CLAUDE.md` (82 lines): landing rule `:50-52` ("Seats push a branch only; Friday opens the PR and merges once CodeQL is green"); no squash-message line (the brief says so and points the seat at "serve as the squash line unedited").
- Code at `7809cd80db3039f6c8b89016b2f28e5dac1e9a13` via `git show` (read verbs only): `ReconciliationContractScale.cs` (220 lines, whole; blob `d4c057d397f58a33d7c14bf5785f9dc03d7027fc`), `ReconciliationReflectionGuard.cs` (265 lines, whole; blob `0bad5ee7792963a95a88b40daf8a48a1ccb782ab`), `PurchaseRecomputation.cs:60-215`, `QuoteReconciler.cs:25-100`, `ReconciliationScenarios.cs:1-175`, `OwnArithmetic.cs` (`CostPerPage`, `ClickAtMargin`), `DecimalMath.cs:31`, the test csproj. Tree `f30732aea0a4faeffac3c2ddf90f8583a0ee24ed`.
- Live reads: `git ls-remote origin` (branch, `refs/pull/106/head`, `refs/pull/106/merge`, main, `refs/heads/b5*`), `gh api -X GET` (`pulls/106`, `pulls?state=open`, `pulls/<n>/files --paginate` for 102/104/105/106, `compare/main...<branch>` for 11 branches, `pulls/98`), `tmux list-panes -a`, `lsof`, `uptime`, `ls .tools`. Not touched: `decision_queue.sh`, `fleet_ack.sh`, the scoreboard, `briefs_staged/`, Jira (not needed; the gate's Jira reads are relayed), `.tools/b5*` contents (only `ls` of names and `ls -d` of five paths), and no git write verb.

## Premises, each with the line read
1. Head/base/merge: `7809cd80db3039f6c8b89016b2f28e5dac1e9a13` on branch and `refs/pull/106/head`, merge ref `25f12e97352edf84021c11dda62e106d42e716b0`, main `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055` (10:10:13). `pulls/106`: `open false clean`, head sha equal, base sha equal, 5 commits, 8 files. `rev-list --left-right --count a5b4bbb5...7809cd8` = `0 5`.
2. The Major: `PurchaseRecomputation.cs:85` `decimal contractCostDifference = Math.Abs(monthly.Cost * term - reported.Cost);` (count 1 at head); `:86` passes it to `Figure.Compare`; `QuoteReconciler.cs:69` `(f.ContractDifference ?? difference) <= ReconciliationTolerance` (count of `<= ReconciliationTolerance` 1). The gate's M18 and why the rows miss it: `B567_STATUS.md:272-273`; fix-shape `:276`.
3. Why no existing row sees it: `ReconciliationContractScale.cs:214-219` `ExactDeal` (toners 50/10000 and 80/8000, monthly 41.25 = 6000 x 0.005 + 750 x 0.015, comment `:97`) - every contract amount 41.25 x term is on a whole cent.
4. Page counts of the deal: `ReconciliationScenarios.cs:111-113` (line 20: qty 3, 1000 mono, 250 colour; line 21: qty 2, 1500 mono; line 22 optional) with `PurchaseRecomputation.cs:177-183` (non-optional, non-credit, device class) = 6000 mono, 750 colour. Cost per page `OwnArithmetic.CostPerPage` = unit cost / yield (`:69`), no rounding.
5. Minor: forbidden set `ReconciliationReflectionGuard.cs:22`; token kinds `:116` (`InlineField` among them); row `:239-250`, fixture `Spellings` `:252-264` (only `Calculation.WorkbookRules.AllowedTerms`); `DecimalMath.IsWholeNumber` is `public static` (`DecimalMath.cs:31`, count 1), and `MpsCalc.Engine` has `InternalsVisibleTo MpsCalc.Engine.Tests` anyway.
6. New file name free: `ls-tree --name-only 7809cd8 tests/MpsCalc.Engine.Tests/` lists `ReconciliationContractRemainder` 0 times (control `ReconciliationContractScale` 1).
7. The `ContractDifference` row cannot compile at base (the member does not exist at `a5b4bbb5`): the brief makes the ten-line strip the gate used explicit, and keeps every value row free of the name so they compile at base unchanged.

## The fixture (drafter's arithmetic: Python `Decimal`, no C# run)
Search over mono toner unit cost p/100 (p 1100-1500) and colour toner q/100 (q 300-1200), yield 10000, pages 6000 mono / 750 colour; wanted: unmoved amount NOT on a cent at two terms, remainders of opposite sign (magnitude 0.002-0.004), no tie, Fail truth for +-0.011 and Pass truth for +-0.009/+-0.010, and every rounding mutant flipping at least one planted case. Chosen: K `11m`/`10000m` (both print types), C `5.07m`/`10000m` (colour): cost per page 0.0011 and 0.000507; monthly **7.80525**; term 12 -> **93.663** (rounds to 93.66, remainder +0.003); term 24 -> **187.326** (rounds to 187.33, remainder -0.004). Flips table (truth vs mutant), shifts +0.011 / -0.011 / +0.010 / -0.010 / +0.009 / -0.009:
- M18a/b (recomputed side rounded, half-even or away; no midpoint hit): term 12 flips -0.011, +0.010, +0.009; term 24 flips +0.011, -0.010, -0.009 (6 of 12; 2 are Fail cases).
- M18c (reported side rounded): term 12 flips +0.011, -0.010, -0.009; term 24 flips -0.011, +0.010, +0.009 (6 of 12; 2 Fail cases).
- M18d (both rounded) and M18e (difference rounded): the 4 Fail cases flip. R1 (monthly compare): the 4 Fail cases. R4 (`<`): the 4 +-0.010 cases. R2 (term - 1): the control row.
- Why not 60 months: for this fixture family the 60-month amount is 5 x the 12-month one, so its thousandths digit is 0 or 5; no pair with 60 gave opposite-sign remainders in the 0.002-0.004 band (0 hits in the search).
Expected at `a5b4bbb5` + new file (strip applied): 13 ran, 4 red by value (the Fail cases), 9 green, one Fact red by compile.

## Partition program (run by shell + `grep -x -F`, files in the session scratchpad; Yours = the two test paths)
```
lane                                  n paths  shared
PR #102 (b518)                             21       0
PR #104 (b560)                              7       0
PR #105 (b561)                             17       0
PR #106 (self, by design)                   8       2
branch b517/mps-contract-docs-wording       7       0
branch b518/mps-api-input-hardening        21       0
branch b519/mps-pricing-policy-leak-tests   7       0
branch b520/mps-source-lifecycle-hardening 14       0
branch b522/mps-deal-usage-colour-rate-row  4       0
branch b527/mps-bom-fleet-identity-class-labels 15  0
branch b53/source-store-hardening           5       0
branch b54/overlay-store-residue            4       0
branch b560/mps-importer-source-version-pins 7      0
branch b561/mps-proposal-combined-usage-rate 17     0
branch b58/gate-b57-overlay-fix-round       5       0
```
Controls: a planted copy of `ReconciliationContractScale.cs` appended to #104's list reads **1** (expect 1); the self-compare of #106 reads 2 (both Yours paths exist on the branch already). Glob check: paths starting `tests/MpsCalc.Engine.Tests/Reconciliation` in #102/#104/#105: 0/0/0. **Shared with every other open PR and live branch: 0.** Live seats named NOT yours from both sides (brief PARTITION; this report): G72 (gate on #104), G73 (gate on #105), M9 (round 3 on #102, Opus); also H10/G75 are HPSM-POC, not MPS. `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` at 10:10: `%0 tuesday`, `%370 Datasec/HPSM-POC-H10`, `%369 Datasec/HPSM-POC-G75`, `%367 Datasec/MPS-M9`, `%364 Datasec/MPS-G73`, `%361 Datasec/MPS-G72`, `%1 fleet-monitor`; no `Datasec/MPS-M11`, none for the old builder.

## Ports, slots, load
- `lsof -nP -iTCP:9230-9239 -sTCP:LISTEN` printed nothing, rc 1 (no bind control by the drafter; the brief gives the seat one). Word-boundary scan (`/usr/bin/grep -l -E '\b923[0-9]\b'`) over every `briefs/2026-10-2[34]_*` file, `.pre-stamp` and reports included: **no file**, rc 1; control, the same scan for `\b913[0-9]\b`: 9 files.
- Heavy slots at 10:10: `heavy-slot-1` `B568 09:36:55 mutants`, `heavy-slot-3` `B566 09:58:42 master`, `heavy-slot-2` free (read only; none touched). `.tools/b573` and `.tools/wt-b573-{base,fix,mut}` absent (4 `ls -d` errors; control `ls -d .tools/b567` lists).
- Load: `uptime` 7.68 at 10:10 and **15.48** at 10:16; the brief's load1 < 7 rule governs and tells the seat the heartbeat will show the wait. `gh auth status` under the project config: logged in, active account; `pulls/98` reads `closed` (control).

## UNMEASURED
No build, test, mutant or C# at all. Not measured: that the calculator reports exactly 93.663 / 187.326 for the fixture (the brief orders a STOP if not); the per-mutant red counts (Python predictions); that the nested Numerics fixture class resolves `DecimalMath` from the test project (expected: public); Jira since the gate's 09:21 read; whether `mergeable_state` stays `clean` to launch; any branch created after 10:16; the model-routing file and the learning file named in the model line were not re-read (the line is the commission's).

## Deviations from B568's shape
1. No decision-card authority: Tuesday's coordinator ruling (v1.3 technical scope) plus the gate's round-cap statement replace the product owner's card; the brief states round 2 of 2 is the cap and says so to the builder.
2. Sonnet, `BRIEF_SEAT_LEVEL=sonnet`, model line as commissioned (B568 was Opus).
3. A **tests-only** fence: no `src`/docs/web/`.github` change is a STOP, checked by an empty `git diff` over those paths; B568's allowed `QuoteEndpoints.cs` edit is absent.
4. New explicit rule against appending to `ReconciliationContractScale.cs` (rows go in a NEW `Reconciliation*.cs` so they compile at base); `ReconciliationReflectionGuard.cs` is append-only with a NEW fixture class and Fact (the B565 rule "existing rows never edited" kept).
5. A moving heartbeat file requirement (`.tools/b573/logs/heartbeat.txt`), the lock wrap on ref writes, `Datasec/MPS-M11` pane and ports 9230-9239, and the stray-file/word-split hazard line with a before/after `git status` of the project root.
6. Added a fixture STOP (calculator rounds its own contract cost), a small seeded differential (evidence for the delta gate, not committed), and mutants M18a-e/R1/R2/R4/M12/M11 instead of B568's M-A..M-C; no Words-literal tokenizer step (no `src` file is touched; stated and fenced instead).
7. The launch line uses the project clone path and the `sonnet` level; the `READY FOR QA` form names the tier-2 delta gate and counts mutants killed.
