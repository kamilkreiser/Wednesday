# B168 DRAFTER REPORT: QA gate for CP round 2 of 2 (`b104/mpscalc-140-care-packs` @ `a3c9b9d`)
Drafted 2026-10-17 13:41-13:4x AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B168_SEAT-V4_mps-gate-cp-r2.md` (21.7 KB; B167's brief is 57.5 KB). I wrote nothing under `!CODING/`. I used git read verbs with `--no-optional-locks` and `gh api` GETs (MPS `GH_CONFIG_DIR`), and made no fetch, az or HTTP call to the hosted site.

## Measured (ls-remote at 13:41:35, re-read 13:44:36, equal)
- head `a3c9b9d7de1a37fcfa683b4b40c68c84167f6223` = READY line `B104_STATUS.md:433`. main `0217044e804afd4a457cbfd4ba4721f4f51071d1` = PR #76 (`merged=true`). Main's tree `50c52d2c` = `b50441f`'s (the tree B167 gated). main check-runs: 8/8 success. Open PRs: #75 only.
- Round 2 is three commits:
  - `070db90`: test + e07, 2 files, +21 −2.
  - `24143c3`: merge of main. Remerge-diff: 0 lines. Tree = `merge-tree 070db90 0217044`.
  - `a3c9b9d`: 4 files, +20 −11.
- **Product change beyond main's: `PurchaseCatalogue.cs` only, 2 lines (`:145` comment, `:148` Service → CarePack).** The other 10 of CP's 15 files have the same blob as at `d355620`. Main's 16 files have equal blobs at the head. The diff for `docs/api web scripts infra .github` is empty.
- **One file ADDENDUM-7 did not name: `docs/IMPORTER.md`** (`:16`, `:116`, class wording; it fixes B167-11). The brief grades it as docs (REPORT + words), not Major. Tuesday may want to rule on that before launch.
- head + `88c84cd` (T): conflict ONLY in the `SOURCE.txt` and `schema.ts` headers, the same conflict as main + T. T and CP share no file name. CP adds no conflict.
- Ports: 6830-6839 have 0 listeners and are named in no brief (grep 0, with a positive control). Slots: only `heavy-slot-1`, held by lane D since 13:35:55. Load1 47.79. Pane `Datasec/MPS-V4` is free (`cockpit.sh status`).

## Design choices in the brief
- **`prev` worktree** = scratch commit of tree `28608269` (d355620 + 0217044, = B167's CL+CP pair tree). It serves as the "only the class changed" oracle for subtotals, stored quotes and rollback door (c).
- The gate's own CP-i and CP-iii come from `mutateB.py`, re-anchored. The exhaustive 1,600-tuple check binds to the head's C# keys, not only to Python. New mutants: CP-ix (:148 → Service), CP-x (:148 → Other), and a CL-i re-run, which can now catch through the care test.
- Rollback door (3) gets a new question. An approved quote with an IMPORTED care line now stores `carePack`. Pre-CL code (the hosted line) may hide it, as in B167's door (2), where round 1 wrote `service`.
- Synthetic stores must reproduce B167's sha256 (v1 `152174ad…`, v2 `c2cec759…`, collide `4e6489ef…`) before B167's numbers count as a baseline (services 2,694.67).

## Not measured by the drafter
CP-iii and CP-i red runs, the CI counts and all API behaviour are left to the seat. Lane E's numbers are claims.
