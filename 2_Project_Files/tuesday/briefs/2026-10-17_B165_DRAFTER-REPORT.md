# B165 drafter report · 2026-10-17 09:05 AEDT · for Tuesday
Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B165_SEAT-V2_mps-gate-whatif-and-carekey.md` (247 lines). It is NOT launched.

## BLUF
- **SHAs measured** (`git --no-optional-locks ls-remote origin`, 08:58:30 and again at 09:02:03, the same both times; `cat-file -t` = commit ×3):
  - `b103/mpscalc-158-target-whatif-noaudit` = `f1a4b21c90b8c57433bd768aec92bff60a8e8a62`
  - `b103/mpscalc-140-care-key-pattern` = `5d2d7ad3420e901046c08f8aea24efe8cc0cad41`
  - `main` = `12f8e566398bc83ea5c2be4d662f64ee9fbdbbfe` (#73)
  - Both heads equal their READY lines (`B103_STATUS.md:414-415`). Both branch from main itself (0 behind / 3 ahead), so each one alone is a fast-forward.
- **The pair conflicts, in either order, but only in the generated headers.** `web/src/api/generated/SOURCE.txt` and `schema.ts` header lines 2-3 conflict (each side names its own `b727644` / `187928e` and blob). `openapi.json`, `openapi.snapshot.json` (both blob `e240e49d`) and `API.md` (`de9d8beb`) auto-merge the same way in both orders. Whichever branch merges second needs lane D to merge main and re-run `sync-contract.mjs`, which gives a new head sha. By my reading that delta is header-only. The gate measures it.
- **My order reading (the gate decides): C (140) first, then T (what-if).** Lane E is told to merge `5d2d7ad` into its -140 (B104 ADDENDUM-4 item 2), and 142-155 conflicts with C inside `openapi.json`. Re-headering T has nobody downstream. Re-headering C after T would move a branch that lane E is stacking on.
- **No fix is needed before launch.** The launch line is at the end.

## Traps found (each is written into the brief)
1. **The core trap, Check 2(ii).** `Diff` drives both the reason check and the entries (`QuoteEndpoints.cs:161-171` @ `f1a4b21`). `WithoutTargets` (`PriceAudit.cs:79-82`) only nulls the two targets, so by reading it is correct. But the builder's only "real change" control is `monoMarginPercent`. The brief bundles a target with every other supplies field (both margins, cost, yield, part number, add/remove/reorder of consumables, description), with a deal rate and with a section supplies change, each without a reason (expect 400) and with one (expect one entry: real change in, targets out). Mutant T-iii (strip consumables too) is aimed at the gap the builder's tests may leave.
2. **Absent vs null.** Entries serialise with `ApiJson.Options` and `WhenWritingNull` (`ApiJson.cs:21`), so a stripped target should be absent from the entry JSON, not `null`. The builder's test only checks `New` for "target". The gate checks both Old and New.
3. **Audit-chain boundary.** Entries written by #73 hold targets, and the first post-fix entry's Old does not. So `entry[n].new != entry[n+1].old` once. I made this OPEN (a), a REPORT and not a grade, together with the not-rewritten check on stored entries and frozen snapshot audits (Blocker if rewritten).
4. **Non-internal callers.** Target-setting is gated by `PricingPolicy.cs:67-69`, which is independent of `Diff`, so T cannot open it up. The gate still proves 403 `INTERNAL_INPUT_FORBIDDEN` is identical to main, and that the narrowed owner's PATCH-back keeps the stored targets (`:139`).
5. **A target of 0 or below is now stored without a reason** (`INVALID TARGET CLICK` only fires at calculate, `PurchaseCalculator.cs:356`). This is OPEN (c), a REPORT.
6. **What a `care_` key does on main today.** Validation accepts it. At calculate, `catalogue.TryGet` misses, giving a Blocking `UNKNOWN ITEM` (`PurchaseCalculator.cs:420`, `:434-437`). The gate compares every reader against a control `dev_` key with an unknown hash, which should behave the same. `PATCH /inventory/care_…` is 404 both before and after (`InventoryEndpoints.cs:158` already returns 404 for a non-key).
7. **Regex `$` in .NET matches before a final `\n`.** The brief probes `care_<24hex>\n` and, if it is accepted, the same input for `dev_` on main. Pre-existing behaviour on main would be Minor and not C's.
8. **Census.** The only prefix lists are `PurchaseValidation.cs:25` and openapi's 3 patterns, plus the snapshot's 3. openapi-typescript emits no `pattern` (0 in `schema.ts`). The key builders are `CatalogueKeys` (5 prefixes on main; `CarePackPrefix` exists only on lane E's `a80c91d:PurchaseCatalogue.cs:27`) and `tools/replica/purchase_bom_replica.py:79-81`. The gate tabulates all of them.
9. **Not in this gate, but you need it for merge order:** `b103/mpscalc-142-155-item-classes` has moved `13295eb` → **`a4b7e92`** (ADDENDUM-6, a fast-forward). It conflicts with C in `openapi.json:1863-1869` (adjacent `key` / `itemClass` lines), not just the headers. Lane E's `a80c91d` does not yet contain `5d2d7ad`.
10. **Neither branch bumps `info.version`** (`0.9.0-b103` at all three). This is a REPORT only.
11. **Ported lessons:** from B163's Corrections, `mutants.sh` ran tests on stale binaries after a failed build, and the brief requires the copy to stop on build rc. Also: no `/tmp` or `.playwright-mcp` outside `.tools/qa-B165/`; bash, not zsh; a deploy-key `sshCommand` is read with `git config -f`.

## Choices you may want to overrule
- **The fetch of main is pre-granted** on B163 ANSWER-1's terms (one read-only fetch, own scratch clone). This saves a QUESTION round trip if main moves. Strike the "Main moves" paragraph's grant if you want it asked.
- **Pane `Datasec/MPS-V2`, seat V2.** B163's pane was `Datasec/MPS-V`. Check that it is closed or reusable in your pane list. If MPS-V is gone, V2 is still a distinct name.
- **Ports 6810-6819.** Today's briefs named 6780-89 (B161), 6790-99 (B162), 6800-09 (B163, released) and 6900-99 (HPSM). 6810-19 is unnamed and is not B163's block, so a stale B163 listener cannot be mistaken for this seat's. `lsof` rc 1 on 6810-6819 at 09:02:05, and on 6700-6999 at 09:00:12.
- **Grades:** a real supplies change stored without a reason = **Blocker**. A target-only change still refused or audited = **Major**. B163's mutant rule is kept: a survivor that the gate's own probe catches = Major.
- **The card id is not quoted.** Kam's pricing-review card handle contains a reviewer's first name, so the brief names it as "the pricing-review card ruled 2026-10-16 (K-09/K-11/K-12)" (ADDENDUM-6 item 4's direction). A case-insensitive grep for the name over the brief returns 0, against a positive control of 8 hits for "kam" in the same file.

## What Tuesday must check before launch
1. Re-read the three pins with `ls-remote`. Lane D is told not to move either branch (ADDENDUM-6 item 3), but main may have moved.
2. The pane list: `Datasec/MPS-V2` is free, and B163's `Datasec/MPS-V` is closed (B163 STATUS ends at 07:4x with its VERDICT line).
3. Heavy slots and load. At 09:00:32 slots 1-3 were free; load1 was 22.96 at 09:02. Lane D, lane E and B164 may be running.
4. Keep or strike the pre-granted fetch, then re-stamp the SELF-CHECK line.
5. Optional: tell lane D that the second branch to merge will need a header-only re-sync after the first lands, so it is not surprised.

## Instruments (read verbs only on the project checkout; write verbs only in my throwaway clone)
- `ls-remote`, `cat-file`, `log`, `diff`, `show`, `grep`, `merge-base` (`--is-ancestor`) on `2_Project_Files`, all with `--no-optional-locks`.
- Throwaway `git clone --shared --no-checkout` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1adf3692-9235-4f22-a389-4453cb048441/scratchpad/b165clone`, with push URL `DISABLED` (read back with `remote -v`). Only `merge-tree --write-tree` ran there. No commits, no fetch.
- Merge readings: main+T = `2d0ddfb0`; main+C = `77b40d86`; T→C conflict `ed0390e5`; C→T conflict `044d428f` (the two differ only in the two header files); T+`a4b7e92` = headers only (`f35cef80`); C+`a4b7e92` = `openapi.json`, snapshot and headers (`c2abcb28`). `161def0`, `0d525ad` and `41af1e3` are already in main.
- No `gh`, no HTTP, no Jira, no az, no build or test run, no mail, no pane.

## Exact launch line
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-V2 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B165_SEAT-V2_mps-gate-whatif-and-carekey.md'"
```
