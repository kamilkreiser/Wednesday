# B553 drafter report (round-2 tier-2 gate kit for PR #103, pane Datasec/MPS-G69)

Written 2026-10-24 about 01:10 AEDT by the read-only drafter (Sonnet). Kit: `2026-10-24_B553_SEAT-G69_mps-103-round2-gate-tier2.md` (105 lines, 58167 bytes; B546's `.pre-stamp` is 112 lines, 65740 bytes), unstamped copy `.pre-stamp` beside it (`cmp` rc 0).

## Facts measured (command -> output, 01:04-01:07 AEDT)
- `ls-remote origin main, b527 branch, refs/pull/103/*, refs/heads/b5*` -> main `e3624f00...`; branch = `refs/pull/103/head` = `abb2c55fdc467e982ac2ba0eac79626e474f2580`; `refs/pull/103/merge` = `e13e24cd50f5832567bfc8c7f4b3177aa6a5182d`; b518 `27534990` (moved from `c7365aee`); no b553, b550 or b546 head.
- `gh api commits/e13e24cd...` parents -> `e3624f00  abb2c55f` (merge ref built on CURRENT main; `cat-file` of it in the local clone: "could not get object info").
- `pulls/103` -> open, draft false, mergeable true, clean, base `c4aa4cc7`, commits 12, changed_files 15, +1388 -25. `compare main...b527` -> diverged, ahead 12, behind 2, merge base `c4aa4cc7`. `rev-list --left-right --count`: `c4aa4cc7...abb2c55` `0 12`; `bf7ad7a...abb2c55` `0 6`; `e3624f00...abb2c55` `2 12`.
- `log --name-only bf7ad7a..abb2c55` -> per commit path counts 1,1,1,1,1,2 (fdccc5e, f9723bd, 04d383b, cabd7d0, ee89ea7, abb2c55); `diff --numstat bf7ad7a abb2c55` -> FleetGrid.tsx 20/3, FleetGridFocus 87/0, FleetGridKeys 83/0, BomClassColumn 21/6, BomEditorSecondSection 55/0, ConsolidatedBomPairingGuards 78/0 (344/9).
- `pulls/103/files` -> 15 paths, all under `web/` (count 15 of 15); round-1's 11 plus 4 new test files.
- `diff --name-only bf7ad7a abb2c55` over `FleetGrid.test.tsx`, `PurchaseBomEditor.tsx`, `consolidatedBomModel.ts`, `bomModel.ts`, `InventoryPicker.tsx` -> 0 lines (unchanged). Only src change: `FleetGrid.tsx` (focus: `:41`; `keys.push(next++)` at `:247`; `remove` at `:39`).
- Added lines `bf7ad7a..abb2c55`: non-ASCII 0; ticket/card/`B5nn` shape 0; skip/only/todo 0. Six new messages: non-ASCII 0, percent 0, trailer 6. FleetGrid.tsx added lines with a quote char: the `react` import, `className="danger"`, the aria-label template (existing text); removed lines 3.
- `show abb2c55:web/vite.config.ts | grep -c -i testTimeout` -> 0 (control `jsdom` 1). `it(` counts of the new files: 1, 4, 2, 3 = 10. `DEFAULT_REBATE_FRACTION` regex matches in `bomModel.ts` at the head: 1.
- Check-runs of `abb2c55`: 9, all completed success; open alerts on the PR ref 0; analyses at `abb2c55` 4 (results_count 0); `rules/branches/main` types: deletion, non_fast_forward, code_scanning, required_status_checks.
- Intersection of the 15 paths: b517 7/0, b518 21/0, b519 7/0, b520 14/0, b522 4/0, b53 5/0, b54 4/0, b58 5/0, PR #102 21/0 (0 under web/), self-compare 15 of 15. Open PRs: #102, #103.
- `tmux list-panes -a`: %0 tuesday, %352 Datasec/MPS-G68 (live), %351 HPSM-POC-H7, %349 MPS-M5R (idle), %348 MPS-M2R (idle), %1 fleet-monitor; no G69.
- `lsof -nP -iTCP:8890-8930 -sTCP:LISTEN` -> empty (rc 1); `8910-8930` -> empty (rc 1). `ls -d .tools/b553 .tools/qa-b553 .tools/wt-b553-diff .tools/heavy-slot-{1,2,3}` -> all absent (control `.tools/b484` lists); `ls .tools/ | grep heavy-slot` rc 1.
- `uptime` load averages 2.41 3.35 6.24 (01:04), 4.02 3.54 6.06 (01:05). `models_latest.json levels.sonnet.model_id` -> `claude-sonnet-5-5`. `node --version` v26.8.1, `npm --version` 11.19.0; `/opt/homebrew/opt` has node, node.js, node@26, nodejs (no node@24).
- Kit file checks: slot grep (split pattern) -> 9 lines (39-46 and 105), control 1; `@[A-Z_]+@` -> 0; non-ASCII lines 0 (control 1); person-name words 0; card-id shape 0.

## Judgement calls for Tuesday at the stamp
1. **Ports 8910-8919** (G68 holds 8900-8909, B550 8890-8899, all empty on lsof; no bind control run).
2. **Hard stop:** I suggest target 2.5 h, hard stop 3.5 h (round 1 overran its 3 h stop with a loaded machine; the machine is quiet now at load1 about 4, and G68 will take a heavy slot). Your call.
3. **E2E slot** in the Ports/slots line: `E2E: YES` allows one stub-mode run on loopback in the gate's block (the fix seat ran it once, RELAYED); default is NOT TESTED as behaviour (B546's rule). Port 8911 would be the natural one.
4. **Tier:** kept at tier 2 (Sonnet, G2): the delta is web only, one source file, no money. The kit escalates on any non-web byte.
5. **Scope of depth:** the six fix commits in depth, the whole PR for delta/words/CI/hygiene; the round-1 65-row red-first and 30-mutant matrix are NOT redone in full (lead 6: FleetGrid.tsx mutants A, B1, B2, N, F1, F3 mandatory, the rest as time allows, with the gap named). Widen if you want the full re-run.
6. **Gate-built mutants beyond the brief's list:** FO5 (focus only when the Remove button itself is active; tests the width of the stamp ruling "inside the removed row": the rows pin only the other-row case), GP1/GP2 (generator-coverage mutants of the property TEST, to check the walk does not leave `catalogue > 0`/`manual > 0` true by construction only). Q-1 must be YES for them. A survivor of FO5 is graded Note; strike it if you want no ruling-width question.
7. **Severity wording I chose:** a property row over 2500 ms in a properly started run is Major (it breaches your ruling); the `15_000` timeout is a Note while every run is within the ruling; a surviving mutant on a finding's code is an OPEN Major; the ten new rows are held to "no row without a killer" as Major, not Minor.
8. **Separability** is stated as a FACT (one fix commit per finding except finding 1, two commits on one file); the kit asks the gate to name independent commits, not to choose the squash plan.
9. gitleaks is required again (round 1 NOT RUN); a missing run makes the verdict conditional.

## UNMEASURED
- The assertions of `FleetGridKeys`, `BomEditorSecondSection` and `ConsolidatedBomPairingGuards` (not read; only `it(` counts); `FleetGridFocus.test.tsx` was read whole.
- The merge ref's object in the local clone; the `web` job log; any build, test, mutant or probe; the property row's duration at any seed; whether FO5 survives or GP1/GP2 die; ports by a bind control; Jira (not read); the fix STATUS's own sha for its copy of its brief is quoted from its text, not recomputed.
- The fix brief's current sha256 (not computed by the drafter).

## Files written
Only the three named: the brief, its `.pre-stamp` copy (the one allowed `cp`), and this report. One slip: before writing, I created two scratch listings (`mine.txt`, `l.txt`) in the session scratchpad for the intersection and removed them afterwards; nothing else, nothing in /tmp proper, nothing in the project.
