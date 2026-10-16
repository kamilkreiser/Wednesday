# B158 + B159 drafter report · MPS QA gates for the tier-1 READY branches of lanes C1, C2, D, E (lanes F/H are B157)
Drafted 2026-10-16 ~16:19-16:4x AEDT. Nothing was launched or sent.

**Files written (Tuesday's briefs folder only):**
- `2026-10-16_MPS-READY-INVENTORY.md`
- `2026-10-16_B158_SEAT-R_mps-gate-lanes-D.md`
- `2026-10-16_B159_SEAT-S_mps-gate-lanes-C1-C2-E.md`
- this report

**How the drafter read:**
- `git --no-optional-locks` read verbs only in the project checkout. No fetch. Its `status --porcelain` was 0 lines before and after.
- Merges were predicted with `merge-tree --write-tree` + `commit-tree` in a THROWAWAY `git clone --shared` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/mps-clone`, with its push URL DISABLED. Objects were written only there.
- GitHub was read with `gh api` GETs under the project's `GH_CONFIG_DIR` (account `kamilDatasec`).
- `cockpit.sh status` was run once, read-only, to see the pane names.
- No az, no Jira, no HTTP to the hosted site.

## Why two seats, not one
- **There are 10 tier-1 READY branches** (inventory Table 1); B157 took 8.
- **B158 = lane D alone** (150, 158, 151, 174c):
  - the only set that changes calculated figures (X-25…X-30);
  - +2,486 lines over 4 heads;
  - a compile-only red-first, so the gate must write its own behavioural mutants and an independent arithmetic oracle;
  - the contract with three version labels.

  Mixing it with anything else would thin the figure proof.
- **B159 = the other six** (C2 170 and 179, E 141, 147 and 182, C1 136). Their oracles are smaller and cheaper (audit cases, a leak-guard mutant, synthetic books, a date function, a fake `az`).

## Launch commands (Tuesday; the same `brief_seat.sh` form as B157; pane names verified free)
- `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-R "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B158_SEAT-R_mps-gate-lanes-D.md'"`
- `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-S "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-16_B159_SEAT-S_mps-gate-lanes-C1-C2-E.md'"`

**Pane names in use at 16:2x** (`cockpit.sh status`): `Datasec/MPS-P`, `-Q`, `-LA`, `-LB`, `-LC1`, `-LC2`, `-LD`, `-LE`, `-LG`, `-LJ`. **`MPS-P` was not on your list:** it is B160 SEAT-P (`2026-10-16_B160_SEAT-P_mps-pkcs-in-package.md`, Pkcs in the CI package). Hence R and S. Brief numbers B158 and B159 were unused (only B160 exists past B157).

## Concurrency with B157 (and B160)
- **Shared checkout: no write sharing.** Each gate works in its own `git clone --shared` under `<project root>/.tools/qa-B15N/`:
  - B157 `qa-B157`, B158 `qa-B158`, B159 `qa-B159`;
  - the project's `.git` is read only, through alternates;
  - each brief forbids the others' trees.
- **Ports are disjoint:** B157 6750-6759, B158 6760-6769, B159 6770-6779. `lsof` rc 1 on 6760-6779 at 16:2x. Container prefixes `b157-` / `b158-` / `b159-`.
- **Heavy slots are the bottleneck.** At 16:25:
  - slot 1 held by `B157` (16:23:54, "dotnet-line m-7dfa241");
  - slot 2 by `B160` (16:25:02, "probe-builds");
  - slot 3 free;
  - load 4.84.

  Four seats then contend for three slots, each gate at most one at a time.
- **Recommendation:** launch both now. They do reading, Jira, diff review and scratch-clone setup before needing a slot, and the 3-minute retry serialises them. Or launch B158 first (deeper) and B159 when B157 or B160 releases a slot.
- **Can run concurrently with B157: YES.** No shared file between their branch sets: `comm -12` of the file lists is empty.

## Traps found
1. **Main merges by squash.** #41, #43 and #44 each have ONE parent. Simulated in the scratch clone, squash PRs per stack member conflict at every second member:
   - lane A 146-185;
   - lane G 156;
   - lane J 173;
   - lane E 147;
   - lane D 158;
   - **B157's own 164 and 165** on `SourceLifecycle.cs`, which also concerns B157's "MERGE stack" verdict.

   Merge commits, or one PR per stack TOP, are clean (36 of 39 steps on top of B157's eight). Decide before the first PR.
2. **`b102/mpscalc-171` conflicts with main** (#43's `SourcesUnavailableWords` vs 171's `IsEmpty`, both above `Stale`; merged `QuoteEndpoints.cs:1167-1182`). It is tier 2 and not in either gate, but it cannot merge without an `-r2` or a PR-side resolution.
3. **Lane D's own merge note is wrong for 151.** `B103_STATUS.md:221-224` says "other hunks", but 151 conflicts with 150/158 in `docs/ENGINE.md` and `PurchaseCalculator.cs` (adjacent inserts). 174c conflicts on the generated files, as the lane predicted. B158 builds a labelled GATE-RESOLVED `m-all` so that you learn whether the obvious union compiles.
4. **Lane D's red-first is compile-only** (CS0246/CS1061, `B103:69-71`, `:165-167`). B158 requires behavioural mutants and an independent decimal oracle from `docs/ENGINE.md` @ `621e3300`.
5. **Lane D says "none on screen" (`B103:84`), but its issue texts render** in `PurchaseResultView.tsx:204` and `PriceView.tsx:257` @ `621e3300`. They are Kam words-gate items. B158 Check 8 lists them.
6. **Deal-rate audit gap, declared by lane D** (`B103:95-96`): a priced caller can change `usage.*` rates with no reason or audit entry until lane C2 extends `PriceAudit.cs`. B158 measures it and grades whether it blocks 150.
7. **Contract labels:** 150 and 174c are both `0.8.0-b103`; 158 is `0.9.0-b103`. The merged label is unresolved.
8. **136 bites on deploy without any Entra step.** A token that already holds all four roles loses the act-as switch (`B108:164-166` counts Kam's own 4 assignments). With T02 unbuilt, a four-role owner still cannot approve their own quote. B159 reports both.
9. **136's script tests need the fake `az`.** B159 asserts `command -v az` resolves under `scripts/tests/` before every `entra_apps.py` call and forbids `entra-app-registrations.sh`. A real `az` call against the Datasec tenant would breach the HOLDS.
10. **182 vs B157's 166:** importer = Sydney date (182); API validate = UTC date (166, `SourceLifecycle.cs:401` @ `7dfa241`). Two "expired" rules on one book. Reported, not graded.
11. **141 and 147 cannot be proved on the real books** (`.local/`, forbidden), as with B157's 166. The gates use synthetic books, so 141's counts stay UNMEASURED by rule. You may want to downgrade 141 (docs only, +34) to your own review at source.
12. **179 × lane D:** whichever merges second must re-run the two guard tests (B103 ADDENDUM-1 item 3). Both gates run them on main + 179 + 150 + 158; the merge itself is clean in both orders.
13. **Your rulings are not recorded as confirmed in either brief.** B157 had "CONFIRMED by Tuesday 16:08" lines. Here every lane reading is marked OPEN and checked only as built (B158 RULED/OPEN section a-e; B159 a-e). If you confirm any, say so on the board or by ADDENDUM before the verdicts.
14. **Lane C2 read the HOSTED site** (Kudu VFS GETs, counts only, `B102:59-60`, `:108-110`), as its brief's P-1 asked. The facts are in the inventory; not graded.

## Could not verify (UNMEASURED by the drafter)
- Jira acceptance text for all 10 tickets.
- Whether any merged tree compiles and passes, including the GATE-RESOLVED lane-D union.
- Base test counts at `621e3300`. The lanes measured 1,822 at `7af91de` / `0f8ad97`, and main has since added #43's tests.
- Whether the calculation issues are shown to non-internal callers.
- The real-book counts behind 141 and 147.
- The Entra P1 licence (`B108:168-171`).
- The pane-name check covers only what `cockpit.sh status` printed at 16:2x.
