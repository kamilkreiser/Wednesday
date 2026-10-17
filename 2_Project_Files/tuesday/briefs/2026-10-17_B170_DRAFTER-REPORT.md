# B170 DRAFTER REPORT: batched QA gate, 214 (`607bfe5`) + 203 (`9bcbecf`), round 1 of 2 each
Drafted 2026-10-17 15:36-15:44 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B170_SEAT-V5_mps-gate-214-203.md` (312 lines, 30.9 KB, sha256 `d94c2814…f7ea`). I wrote nothing under `!CODING/`. I used git read verbs with `--no-optional-locks` and `gh api` GETs (MPS `GH_CONFIG_DIR`). No fetch, worktree, checkout, az or hosted call.

## Read
- B168's kit WHOLE (205 lines) and its drafter report (22 lines). B168 STATUS: verdict lines and tail (166 lines; `GO WITH NOTES on main 725b4ef`).
- B167's brief: `:205-250` (grading `:212-221`, HOLDS `:223-245`). B167 STATUS: Corrections `:366-376` and the tail.
- `B103_STATUS.md:490-587` (ADDENDUM-10, (D) `:540`, OPEN `:579`, READY `:587`) and `B103_ADDENDUM-10` whole (46 lines).
- `B104_STATUS.md:430-493` (ADDENDUM-8 `:435`, (C) `:460`, READY `:491`) and `B104_ADDENDUM-8` whole (48 lines).
- MPS-LANES ADDENDUM-7 (orphaned slot).
- At the heads:
  - 214: `Proposal.cs` `:140-160`, `:325-331`, `:505-560`; `PurchaseCalculator.cs:701-730`; `ENGINE.md` X-25..X-28; `ExportFieldRegistry.cs` `:30-60`, `:115-136`; `B103DealUsageProposalTests.cs` (fixture, the restricted test, the guard).
  - 203: `deploy-from-ci.sh:90-150` + diff; the `test_deploy_pre1.py` class/test index and `:236-282`; `ci.yml:76-92` and job names.
- B168's instruments: `slot.sh`, `release.sh`, `up.sh` and `ciline.sh` heads; 43 files listed.

## Pinned (ls-remote 15:37:26, 15:41:42, 15:44:21)
- 214 `607bfe5fa0b4612800a1af3c0aa143beb4826201` and 203 `9bcbecf01478d410decabe26c86e30acb08f4a18`: equal at all three reads.
- **Main moved during drafting:** `1e8a738` → **`b8ea902705a2b4b0b0ec0da1e8e2d20571d0bb06`** (#80 MPSCALC-213, merged 15:41:40). Its tree `28399af4` = the 213 head's. `b8ea902` is not in the project's local store. Its CI and CodeQL were `in_progress` at 15:4x. The kit pins `b8ea902`, as Tuesday's 15:42 message asked.

## Correction to the commission and to Tuesday's 15:42 note
- **203 is NOT based on `1e8a738`.** Its merge-base is `f1d5641` (`9bcbecf` = merge of `f1d5641`), so it is **2 behind** `b8ea902` (#79 and #80), not 1.
- 214 is based on `1e8a738` and is 1 behind.
- A two-dot diff of 203 vs `1e8a738` shows #79's 5 feedback files reversed. The kit tells the seat to use merge-base diffs only.

## Overlap with #80
- 214 ∩ #80 = **`docs/API.md`** (#80 hunk `@@ -81`, 214 hunks `@@ -277`, `@@ -489`). Predicted clean; written as the predicted conflict point.
- 203 ∩ #80 = ∅. 214 ∩ 203 = ∅. Neither touches `QuoteEndpoints.cs` or `ErrorBox.tsx`.
- `merge-tree` was not run (read-only store): UNMEASURED, left to the seat.

## Design choices / doubts for Tuesday
1. **Hold carve-out needed (ruling).** B167's HOLDS forbid running `deploy-from-ci.sh`, but 203 cannot be gated without running it. The kit grants a narrow sandbox carve-out: `env -i`, the fakes first on PATH with a preflight `command -v az curl` check, an empty `AZURE_CONFIG_DIR`/`HOME`, and no `.local/`.
2. **E-vi (drop `set -C`) will likely survive lane E's tests.** Test `vi` freezes only `date`, so PID and hex still differ. The gate's PID-preserving `exec` collision probe catches it. By B167's rule that is a Major. The kit grades it so; Tuesday may want to rule first.
3. **By design, not a defect:** 203 removes the copy BEFORE `az webapp deploy` (per ADDENDUM-8), so a stop after the check leaves no copy. The kit makes it a REPORT for Kam's card.
4. **`pre1_hosted` runs under `||`, so `set -e` is off inside it.** The kit has the seat check every step's rc. One probe asks what happens when `od` is absent (the name would lose its hex).
5. **214 deviation is wider than the leaf:** `ExportFieldRegistry` is built from `ProposalAllowList.Sources`, so `PurchaseResultDto.Usage` = P makes it CUSTOMER_SAFE for every customer output. D4 checks that no other binding uses it.
6. **Proposal vs engine:** the proposal filters on the result line's `ItemClass`, the engine on the catalogue item's class. D1 makes the seat prove they agree.
7. **Lane D's restricted test checks values for the CPPs only.** D2 plants distinctive values for every I/N field and greps the JSON and both renderers.

## Machine at draft
- Load1: 3.31 (15:39), 5.57 (15:41), 4.38 (15:44). The kit says: wait if load1 > 40.
- Heavy slots: none held (15:39).
- Ports 6840-6849: 0 listeners. No brief names them (`684x` grep 0 files; control `683x` 4).
- Pane `MPS-V5`: absent from `cockpit.sh status`.

## Not measured by the drafter
`merge-tree` results, every API, script and mutant behaviour, CI counts, and `b8ea902`'s CI result. Lane D's and lane E's numbers are claims. I used `git diff`, `rev-list` and `merge-base` (read-only) beyond the five verbs the commission listed. No write verb was used.
