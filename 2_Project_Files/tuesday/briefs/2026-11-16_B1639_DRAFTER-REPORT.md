STARTABLE: YES (after Tuesday's stamp; five questions, each with a default that lets it start)

# B1639 drafter report: HPSM-POC lanes H-5 (HPSMPOC-505 test row) + H-6 (HPSMPOC-504 README counts dropped), seat H176

Drafted 2026-11-16 from 21:54 to about 22:04 AEDT (`date` printed 21:54:29, 21:54:38, 21:55:53, 21:56:41, 22:01:06, 22:02:09).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1639_SEAT-H176_hpsmpoc-lanes-h5-h6-owner-row-and-readme-counts.md` (296 lines).
- Sidecar: `...owner-row-and-readme-counts.md.measured` (130 lines: 86 stamp_check claims plus S01-S44). `stamp_check.py <kit>` exits 0 (run unpiped, `rc=0`; "86 claims, 86 measured, 0 not measured").
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s284/b1639/` (raw files at main, `jira.txt`, `probe_cont.mjs`, `out/`, `mk_sidecar.py`, `kit_body.md`).
- Template: B1620 (H-3, the same owner cut and the same test block) for shape, with its STATUS (Deviations: the red-first row 10 imprecision and the `bicep` PATH red are both carried into this kit); B1616 (H-4, the same README) for the docs-lane proofs and its STATUS item 4 (the stale counts).

## BLUF
- **H-5 is real and the row is measured.** At main `a816fd00` the loop is `startingOwner` `:67-71` and the line to pin is the `break` at `:68`. A copy of the loop run under the project's node `v24.21.0` gives, for `letters(99) + FAMILY + "b"` (108 units): `break` 99 units equal to `letters(99)`; `continue` 100 units ending U+62, not equal. The three existing rows with a joined emoji (92+family+b, 97+family, 95+family) give the SAME result under both, so none can kill the mutant (matches the ticket's derivation, now run). The row's three names (`letters`, `FAMILY`, `longer`) are already in scope in the block (`:487-493`), so the row is four lines, inserted after the exact-limit row (after `:534`).
- **H-6:** lines 85 and 88 of the Reporting README carry "208 tests", "(60)" and "(148)". Tuesday's answer to SWEEP question 1 is "drop the counts". The kit gives exact old and new lines (D2); the check is by program: `str.replace` of the three literals on each base line equals the head line, numstat `2 2`, every other line byte-identical.
- **No reader of the README** found: the Reporting csproj has 0 README items (control 8), 0 of 51 Reporting test files name README (control `namespace` 52), the one infra README reader reads `infra/README.md`. So H-6 runs no dotnet; the infra job's repo-wide hidden-character walk is the CI job that reads it (DRAFTER_RULES fence 8), and it runs in both parts. The seat re-checks by `git grep` (Step B2); a hit that reads this file is a STOP.
- **One seat, serial, two branches** each off BASE, one commit and one push each, so Tuesday can gate and land them independently (H-5 G2, H-6 G3 as commissioned; Q-1). Sonnet, row L6 (`model-routing.md:85`). No ports. A `PARTIAL B1639: A <sha40>` last line exists for a seat that must stop after part A.

## Facts re-measured with instruments
- **Main** `a816fd002892003913dd049c746141c200ca15a2` at 21:54 (`gh api -X GET branches/main`). **Open PRs: 0** (length 0; `pulls/99999` HTTP 404; `pulls?state=open` HTTP 200; closed list #328-#324 as control). `matching-refs/heads/b1639` length 0 (control `heads/b1599` length 1). Main's newest commit (#328, H-1) changes only two api files; the owned files' newest commits are `3e557e56` (test and product, #327) and `b9466911` (README, #326, the line-76 clause).
- **Tickets** (GET only, through my own copy of the sweep's `jdesc.py`; no token printed): HPSMPOC-504 and 505 both Backlog, updated 17:56 and 17:57 UTC; their texts are quoted in the kit. 505's own sentence "all 135 rows ... passed" matches the H-3 STATUS (135 of 135).
- **Pointers** printed by `awk NR==n` over raw files at `a816fd00`: store `:18`, `:58`, `:60`, `:61`, `:63-66`, `:67`, `:68`, `:69`, `:71`; test `:454`, `:487`, `:488`, `:490-493`, `:495`, `:532-534`, `:536`, `:563`; README `:84`, `:85`, `:88`, `:89`, `:90`; `ci.yml` `:384 :396 :409 :413 :478 :630`; `package.json` `:8 :10-12`; `vitest.config.mts:10-11`. All are in the sidecar (S01-S44). The ticket's `:68` and the sweep's "the function starts at `:58`" both hold.
- **Mechanism probe** `probe_cont.mjs` (node `v24.21.0`): see BLUF; the planted-wrong expected (`letters(98)`) is unequal under both modes (control that can fail).
- **README form:** lines 85 and 88 are ASCII with LF endings (0 carriage returns in the file); the file has 37 non-ASCII lines elsewhere, so the check is "introduced non-ASCII 0", not "none in the file".
- **Toolchains by path:** node `v24.21.0` (`.tools/node24/bin/node`), bicep `0.47.16` (`.tools/bicep/bicep`, read-and-run only), python `3.14.10`.

## D-decisions (the drafter's)
- **D1 Two branches, two commits, two pushes** (Q-4), because the paths are disjoint, the tiers differ (G2 and G3) and Tuesday lands by head-pinned squash per branch. Branch B is cut from BASE, never from branch A.
- **D2 Red-first for H-5 is by mutant, not by base** (a test-only pin is green at base by construction); the kit requires the new row red BY ASSERTION under `continue` in a scratch copy, plus a planted-wrong control at the unmutated code. A surviving mutant is a STOP that strengthens the row. This carries the B1620 STATUS lesson (a row whose assertions the base also satisfies is not red-first).
- **D3 One row, four lines, the block's own helpers**; existing rows byte-identical (0 removed lines); no product line changes.
- **D4 README edit as exact old/new lines**, "by group" as the only inserted phrase (Q-3), so the check is `str.replace` equality rather than a judgement.
- **D5 No `npm run build` at base for H-5** (a test file is not in the client bundle); build runs once at head. No dotnet for H-6 (measured above).
- **D6 BICEP and python version in the kit's TOOLCHAIN** (the B1616 and B1620 STATUS "FOR TUESDAY" item both asked for it).

## Q-questions for Tuesday (each with a default)
- **Q-1 Gate shape.** The commission says H-5 G2 and H-6 G3, "one G2 gate may carry both". **Default: one Sonnet G2 gate reads both branches** (both are path-disjoint and tiny; H-6's proofs are by program). Alternative: G2 on H-5 only, H-6 on the builder's own proofs plus Tuesday's check.
- **Q-2 The second Minor in 505's text** (a lone surrogate that is the 100th unit stays in the result). The ticket says it is named "so the row can be added with the first, not as a defect", and the sweep says out unless PRIOR WORK says otherwise. **Default: out** (kit Holds). Alternative: a second row pinning today's behaviour (adds a decision about what the result should be).
- **Q-3 README wording.** Default as written in D2: ", by group." after the project path, then "Readiness:" and "Executive report:" without counts. Alternative: delete the sentence ": 208 tests." entirely and let "`tests/...Tests`: Readiness: ..." read as is (a double colon).
- **Q-4 Two branches or one.** **Default: two** (D1). Alternative: one branch, two commits, one PR, one gate.
- **Q-5 Other imprecisions in the same README section** (named in the kit as Held, not fixed): line 89 "12 output mutants + 7 input mutations" (UNMEASURED whether still true) and a closing parenthesis at the end of line 90 with no opener on that line (it was already unmatched at base). **Default: leave both; the seat names them in FOR TUESDAY.**

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | stamped kit, deploy key, project git config, node 24 and bicep under `.tools/` | exists at BASE / Tuesday's stamp |
| A0, B0 | the clone `head` | Step 0 |
| A1, B1 | origin reads, the clone | Step 0 |
| A2 | `probe-continue.mjs` (written in A2), node 24 | Step 0 (node); A2 writes the script |
| A3 | clone with `npm ci`, BICEP | Step 0 |
| A4 | the clone, `base-unit.json` path | A3 (base runs); scratch copy made in A4 |
| A5 | the A4 diff, name lists | A4; project files at BASE |
| A6 | `base-unit.json`, `npm ci` | A3 and Step 0 |
| A7 | A2-A6 green | A2-A6 |
| B2 | the clone (README at BASE) | B0 |
| B3 | BICEP, python | Step 0; equal to A3's base results |
| B4 | the clone on branch B | B0 |
| B5, B6 | the B4 diff | B4 |
| B7 | B2-B6 green | B2-B6 |
| 8 | both diffs, mutant table, both pushed shas | A7 and B7 |

## UNMEASURED
- Whether `Tests` rows count beyond 135 today and whether the whole web suite is still 4337 (RELAYED from the H-3 STATUS; the seat prints both).
- Whether the row's literal text passes lint (`--max-warnings=0`) and typecheck (no run).
- Whether `continue` leaves ANY other row red (the ticket says none; the seat prints the red rows).
- Whether any reader of the README exists beyond the drafter's grep of the Reporting tests (51 files, 0 hits), the infra test sources (12 py files, 0 hits for "Reporting/README") and the csproj; GitHub code search returned two "unexpected end of JSON input" replies and was not used as evidence.
- Whether the numbers on line 89 and the group coverage sentences are still true.
- Whether `Intl.Segmenter` and node ICU in CI match the local node for the row (the row uses the block's existing FAMILY; the same sequence already passes in CI via the H-3 rows).

## Outside-the-fences disclosure
- **Reads outside my files.** `gh api -X GET` under the project's `GH_CONFIG_DIR` (branch, pulls, matching-refs, commits by path and for main, the recursive tree, raw contents of the owned files, `package.json`, `vitest.config.mts`, `ci.yml`, `RoadmapScreen.tsx`, the Reporting csproj, 51 Reporting test `.cs` files, 12 infra test `.py` files and `readiness.test.ts`, and three `search/code` queries of which two returned an unreadable reply); a GET-only Jira read of HPSMPOC-504 and 505 through my own copy of `jdesc.py` (copied from the sweep's scratch; no token printed); the commission, the SWEEP-2150 file, `DRAFTER_RULES.md`, the B1620 kit, its drafter report, its sidecar and its STATUS, the B1616 kit head and its STATUS, `model-routing.md`, `models_latest.json` and `brief_seat.sh` by `awk NR==n`.
- **Run.** One node probe (`probe_cont.mjs`) with the project's `.tools/node24` binary; `bicep --version` and `python3 --version`; `git -C <2_Project_Files> config user.email` and `user.name` (byte counts only printed here).
- **Not run.** No clone, fetch or ref write in any project repo; no build, lint, vitest, npm, dotnet, docker, `az`, mail, board or `decision_queue.sh`; no Artifact, no `_ledger.md`, no WEDNESDAY or FRIDAY tree, no `cd`, no Jira write. The B1624 gate file was not read.
- **Not written.** Only the kit, its sidecar, this report and my scratch folder. A hook refused one early command (a `tee` whose command line named the project folder); I re-ran it without `tee`; nothing was written there.

DRAFTED B1639: kit 296 lines, sidecar rc 0, questions 5
