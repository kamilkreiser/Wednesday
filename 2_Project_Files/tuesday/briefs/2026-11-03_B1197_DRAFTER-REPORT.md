STARTABLE: YES (after the stamp; one launch precondition in Q-1)

# B1197 / SEAT-G312 drafter report (Composer, round 3 final QA gate, tier 1, Opus)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1197_SEAT-G312_composer-pcomp116-round3-gate-tier1.md` (118 lines, 9 lines with the four-underscore pattern = 8 slots + last line; control: the B1181 kit reads 0 after stamping and its `.pre-stamp` 9). Drafter read DRAFTER_RULES whole, the B1181 kit whole, the B1181 verdict and `residue.md`, the B1193 kit (skimmed for authority) and the B1193 STATUS whole.

## BLUF
- The kit is the B1181 shape re-aimed at the granted round 3: head `ce523783` (3 commits on old main `01bc16e4`), **main has moved to `f5f33e18` (PR #113 landed; two renderer paths, disjoint)**, so the kit tells the seat to judge the merge result, not the head tree. The seat re-proves the line independently on 3 engines over the full frame (expected 1,014 cells = 899 + 53 + 18 + 44 fixtures; the builder only ran 22 files), re-runs the gate's 50 mutants and **must write at least 25 new mutants of its own plus Y6 cells** (hashed before it reads the builder's Step 2-5), and closes B1181-1..-4 and K-1 by name.
- It says plainly that a NO GO here ends the class: no round 4, residue ticketed; and that `DEPLOY.md:255` is NOT touched and its replacement sentence is a separate later change (carried, never graded).

## Facts re-measured (instrument; times from `date` 09:47 to 09:50 AEDT)
- Pins: `git ls-remote` branch `ce523783bc2f9e2be99083a5bb34ef02becdf0db`, main `f5f33e189f34d36fa374c0ac1d6fa38d003df8ec`; `refs/heads/b1197*` and `*pcomp116*` absent (control: the `b1170*` pattern printed the branch). `gh api -X GET compare main...branch`: ahead 3, behind 1, base `01bc16e4`, files `DEPLOY.md` +1 -1, b778 +345 -4. `compare 01bc16e4...f5f33e18`: ahead 1, `packages/renderers/src/change-report.ts`, `packages/renderers/test/change-report.test.ts`. `commits/ce523783`: parent `643c389e`, tree `e3ca3300...`, one path +88 -0, one trailer.
- Raw files at `ce523783` via `gh api` raw into the scratchpad: b778 1786 lines, sha256 `1a2e549c...` (= the builder's STATUS prefix, RELAYED then MEASURED); `DEPLOY.md` 652 lines, sha256 `bf446a79...`, `cmp` equal to the file at `643c389e` (control: `shasum` of both printed equal; `awk NR==203 | wc -c` 256). Every b778 pointer in the kit (`:80`, `:149`, `:154`, `:165`, `:167`, `:443`, `:466`, `:491`, `:505`, `:603`, `:1186`-`:1194`, `:1219`, `:1254`, `:1272`-`:1276`, `:1292`, `:1319`-`:1333`, `:1377`-`:1395`, rows `:1501`, `:1513`, `:1523`, `:1529`, `:1545`, `:1754`, `:1758`) was printed by `/usr/bin/grep -n` or `awk NR==n` over that file. `it(` rows: 54 (`grep -c`; list printed). `PCOMP` 0; skip/only 0. The no-`!` row is given as "near `:1658`-`:1667`" because its exact line was not isolated (two `it` rows at `:1658`, `:1667`; the seat must print it).
- `DEPLOY.md` `:153`, `:198`, `:203`, `:204`, `:209`, `:255`, `:259`, `:263` printed by `awk NR==n`/`grep -n`. `scripts/ci.sh:76`, `:117`, `package.json:21` (`ci:node`) and `packages/db/vitest.config.ts:12` (`testTimeout: 30_000`) read at main `f5f33e18`.
- Routing: `model-routing.md:98` (C8), `:108` (G1), `:109` (G2), `:111` (G-cap); `models_latest.json:17` and `:37` `claude-opus-5-5`.
- Landing rule: `CLARIFICATIONS.md:2032` still the authority line pointing to `:1799`; `PR #88` control prints `:1797`, `:1799`, `:1802` and later lines.
- Round counts: `B1173_STATUS.md:1` NO GO ROUND 1 OF 2; `B1181_STATUS.md:1` NO GO ROUND 2 OF 2 (grep -n -i 'GATE VERDICT').
- Overlap/CodeQL: open PRs 91, 86, 85, each 0 hits on the two paths (counts printed; the #85 control was not re-run by me, the kit tells the seat to run it); check-runs total 0; open alerts on the branch 0; main alerts query returns rows (3); `gh auth status` Datasec-account pattern 1.
- Seats/load: panes `%0 tuesday`, `%142 MPS-R152`, `%141 NexusAI-N94`, `%140 MPS-M88`, `%138 MPS-M87`, `%135 HPSM-POC-H108`, `%1 fleet-monitor` (0 Composer panes); `P/.tools/composer-heavy.lock` absent, `P/.tools/b1197` absent (`ls -d` rc 1 each; `b1181`, `b1193`, `b1173` list); load1 2.90.
- Ports: python scan over the 123 non-`.pre-stamp` SEAT kits of 2026-11-02/03 (width <= 30, word-bounded): **9400-9409 hit 0 kits; `lsof -nP -iTCP:9400-9409 -sTCP:LISTEN` rc 1**; 9390-9399 hit 2 kits and 9380-9389 hit 5, so they were skipped; control 9980-9989 hit 9 kits.

## D-decisions
- D-1 Incorporated by reference the B1181 stamped kit (sha256 `32c8b1e1...`, equal to the project copy) for SEATS, INSTRUMENTS, LOAD, HOLDS; scripts copied from `.tools/b1181/scripts/` (the gate family's own), never from the builder's `.tools/b1193/`.
- D-2 Read order mirrors round 2: allowed builder STATUS `:1-44`, `:114-119`, `:137-144`; forbidden `:45-113` until Step 1 hashes (section starts printed by grep -n).
- D-3 Grading: any `mutant-accepts` survivor is Major; accept-side survivors graded by R2-G (the limit that made them Minor last round is gone, so (c) is reworded); `DEPLOY.md` unchanged since `643c389e` so no new false sentence can exist; REFUSE 9 added (`DEPLOY.md` not `cmp`-equal to `643c389e`).
- D-4 Verdict line uses `ROUND 3 (GRANTED, FINAL)` and requires the words "no round 4" on a NO GO.
- D-5 Landing files name the three-commit squash, the `:255` sentence as a separate later change, and `--match-head-commit ce523783...`.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block: no block was assigned to me; I chose 9400-9409 (measured free). Default: accept 9400-9409.
- Q-2 Main moved (PR #113): the kit judges `merge-tree` of `f5f33e18` + the branch, not the head tree. If you would rather have the builder rebase (it is forbidden to), say so; default: the gate judges the merge result as written.
- Q-3 The frame count 1,014 (44 fixtures) is derived, not counted; the seat prints its own. Default: leave as "expected, UNMEASURED".
- Q-4 Hard stop: I suggested +150 / +240 minutes in S6; set an absolute ceiling at the stamp. Default: same as B1181.
- Q-5 The B1193 builder's disclosure shows `rm -f` of three `/tmp/dummy_*` files and one scratch copy (a "never delete" breach, self-reported) and two dirty plant trees (`wt-b1177-mut`, `wt-b1170-mut`) left by earlier seats. Not graded by this gate; default: you decide whether to retire the trees. The kit forbids touching them.

## UNMEASURED
Engine behaviour of the unchanged line on any cell, the vitest route, plant outcomes, the 1,014 count, the `names.py` deltas (17, 8, 4 derived from 37/46/50/54), the builder's 22-file engine table (not read as a gate input; only claim-read for the drafter), gawk, the demo VM, hosted CI and CodeQL (no PR).

## Outside-the-fences disclosure
Read-only throughout; wrote only the two files above plus session-scratchpad copies (`b778.ts`, `DEPLOY.md`, `DEPLOY643.md`, `ci.sh.main`, `vitest.config.ts.main`) under the session scratchpad. `gh api -X GET` only, under the Composer `GH_CONFIG_DIR`; no git fetch/pull, no docker, no az, no HTTP to any hosted host. One slip: my first command held a `cd` and a hook refused it (no effect). Two hook advisories about case-sensitive phrase greps (pointers were all printed with positive hits; counts of 0 for `PCOMP` and `it.skip` have positive controls in the kit's instruction, and the drafter's own PCOMP count was a grep -c on a file where `Nothing else...` and other words matched, not a separate positive control for PCOMP). The mention of the earlier gates' scripts directory listing came from `ls` of `.tools/b1181/scripts` (read-only).
