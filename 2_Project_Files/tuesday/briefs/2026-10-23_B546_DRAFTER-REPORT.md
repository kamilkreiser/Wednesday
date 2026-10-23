# Drafter report: B546 (SEAT-G65), MPS Calculator tier-2 QA gate on PR #103 (B527 web BOM and fleet screens)

Drafted 2026-10-23 about 18:47-19:05 AEDT (clock `date`) by Tuesday's read-only gate-kit drafter (Sonnet 5.5, row C8). Wrote only: the kit, its `.pre-stamp` (made with `cp`, `cmp` identical) and this report. Nothing stamped, launched, sent, published, fetched, built or run in the project; no decision-queue tool, no scoreboard, nothing under `fleet/briefs_staged/`, no Artifact/Docs/mail/chat, no HTTP to any app or hosted host, no `az`, no docker, no Jira. The real price books were not opened.

## Number
**B546 was free** (`ls briefs | grep B546` empty before writing; highest existing was B545). Round 1 of 2.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B546_SEAT-G65_mps-103-web-bom-gate-tier2.md` (112 lines, 65,740 bytes, sha256 `7a38b8dcc72ecf7eb766d83c17e13fcc9a54b6eae269cf909fbe0d5127fbb230`; seat `Datasec/MPS-G65`, model `claude-sonnet-5-5` (read from `models_latest.json` by the launcher), tier 2, ports **8850-8859** reserved, none needed).
- `.pre-stamp`: same path plus `.pre-stamp`, byte-identical.

## Scans of the kit
Four-underscore line count (`/usr/bin/grep -c -E '_''_''_''_'`): **9** = 8 slot lines + the last line `READ-WHOLE-BY-TUESDAY: ____`; the kit's Stamp says "reads 9". Control: `printf 'x____\n'` through the same pattern reads 1. At-sign-capitals-at-sign 0; non-ASCII bytes 0 (`LC_ALL=C`); person-name list (the project owner and seat names) 0; `mps-...-10nn` shape 0.

## What I read
Templates: the B535 kit (whole, plus its `.pre-stamp` Stamp block and drafter report) and the B524 kit (whole). Subject: the builder brief B527 (whole), the builder STATUS B527 (whole, 373 lines), the compare diff `main...b527` (1290 lines; the five non-test source diffs whole, the FleetGrid, InventoryPickerFit and e2e test diffs whole, the other three new test files only scanned for seeds, strings and non-ASCII). Raw by `gh api -X GET`: `pulls`, `pulls/103`, `/files`, `/commits`, `check-runs`, `code-scanning` alerts and analyses, `rules/branches/main`, `ci.yml`, `package.json`, `SoftwareSection.tsx`, `ConsolidatedBom.tsx`, `InventoryScreen.tsx`, `QuantityAudit.tsx`, `compare main...<branch>` for every `b5*` branch and `pulls/<n>/files` for #99, #100, #102. Also `ls-remote`, `lsof` (8700-8899), `tmux list-panes`, `uptime`, `ls` of `.tools`, a briefs-folder scan for port tokens. Not opened: the builder's `.tools` trees, `.env`, Jira, the real books, the engine and DTO sources, the three new test files beyond scans.

## Facts re-derived (all MEASURED 18:47-18:50)
- Head `bf7ad7a1` = branch = `refs/pull/103/head`; merge ref `fc034a3c` has parents `c4aa4cc7` and `bf7ad7a1`; main `c4aa4cc7`; PR #103 open, not draft, 11 files, +1052 -24, 6 commits (one parent each), mergeable true, state blocked; open PRs #99, #100, #102, #103.
- Check-runs 18:47: 8 listed; CodeQL neutral; Analyze actions and python success; python, dotnet, web, Analyze csharp, Analyze javascript-typescript in progress; no `package` yet; alerts on the PR ref 0; 2 of 4 analyses.
- The 11 paths and their numstat match the builder's STATUS (1052 insertions, 24 deletions). `SoftwareSection.tsx`, `ConsolidatedBom.tsx` and `ConsolidatedBom.test.tsx` are NOT in the diff (the shared `consolidatedPurchase` serves both screens).
- Removed lines: 24 = FleetGrid 2, InventoryPicker 9, PurchaseBomEditor 9, consolidatedBomModel 4. Added-line scans: ticket keys / names / card-id shape 0 (control 1), non-ASCII 0, skip/only/todo 0. Existing test files gain only additions (one `react` import line in FleetGrid.test.tsx, new `describe` blocks).
- Intersection of the eleven paths with b518/b519/b520/b522/b53/b54 and PRs #99, #100, #102: 0 shared; self-compare 11 of 11.
- Heavy slots all absent at 18:48; load 9.99 / 7.96 / 9.75; panes: G64 (B545 gate), M4R, M5 (builder), HPSM-POC seats; no G65; `.tools/b546*` absent; ports 8700-8899 empty.

## Where I departed from the template, and why
- Web-only diff: NO .NET work (no build, no test, no `dotnet` heavy slot use); heavy work is `npm ci` x3, the baseline and red-first runs, the mutant matrix, the whole web CI line. The `dotnet`, `python` and `package` jobs are read statically.
- C3 is red-first at main's source (builder files copied into a main worktree); C4 is the gate's own mutants (the brief's M527-A..M re-proved at the HEAD, plus about 25 designed ones, per-input pairing mutants for -301, key-state mutants for -198, position mutants for -199, group-key mutants for -220) with a rows table (65 new names) and "rows no mutant turns red = 0"; C5 re-runs the three seeded property rows with fresh seeds and asks which mutants die on the property row alone; C9 holds gitleaks, hygiene, names and ids (moved out of C1 per the task).
- Kept the B535 refuse checks, Stamp (8 slots + last line), load rule (with an added "re-read load1 before EACH run inside the slot" line, because of the builder's disclosed lapse), scratch-clone rule, severity shape and verdict line shape.
- The builder's Playwright spec is NOT TESTED as behaviour (CI runs no e2e; no browser, no server): the kit asks for a static read of the spec and a jsdom scratch row with a REAL pointer click instead.

## Builder claims the gate should treat with suspicion (leads 1-10 in the kit)
1. **-198 "a product defect found".** The base-red rows (and the e2e) only reproduce when the click leaves the focus in a LATER row's input (`act(() => b.click())`, `dispatchEvent('click')`); the builder's own DESIGN 2 says a pointer click moves the focus to the Remove button of the row being removed. With controlled inputs the values read right under an index key, so the user-reachable loss is the DOM node, focus and any child-held local state. The kit makes the gate name a user-reachable symptom (a real `userEvent.click` scratch row, a read of which fleet-row children hold local state) or rate "defect" a Minor wording issue (a node-identity pin / hardening).
2. **"30 of 30 mutants killed" ran on `72c025a`, not on the head `bf7ad7a`** (commit 6 touches `InventoryPicker.tsx`, `ConsolidatedBomInPlace.test.tsx` and `InventoryPickerFit.test.tsx` by one line each). The builder says so in NOT RUN; the kit re-runs every mutant at the head and proves commit 6 is comment-and-escape only.
3. **Eleven pins are green at base** (FleetGrid 4, BomLineIdentity 2, ConsolidatedBomInPlace 3, InventoryPickerFit 2); the builder's mutants kill some by name but the STATUS never maps pin to killer. "Rows no mutant turns red = 0" is the check.
4. **-301 rests on the test's own BigInt stand-in for the server** (credit negated, included 0, override as typed, markup x1.5, margin x2) and on `r.unitSellExTax` / `r.unitCost` / `r.pricingMethod` shapes the builder never saw in a real response; the property row (c) is only as good as that stand-in. The kit has the gate read the cited engine lines (`PurchaseCalculator.cs:452,456,511-513`) and the result DTO. Section markup and rebate, the catalogue overlay and a manual item's class are not paired on (the builder says so; a FACT for Tuesday).
5. **-208's unknown class:** the cell is `itemClass === undefined ? CLASS_NOT_KNOWN : CLASS_LABELS[itemClass]`; an unknown TOKEN (not `undefined`) would print an empty cell. Probe and compare with `ConsolidatedBom.tsx:88`.
6. **-220 assumes a fitted care row carries `deviceSku`**; the builder admits nobody read a real inventory row. If the Api does not set it on care rows, the grouping never fires on real data (a Major for "ticket not met").
7. The builder's load-gate lapse (several runs inside its slot not re-gated) and the U+00B7 in the sixth commit's body are disclosed; results unaffected; the squash replaces the message.
8. Node: the builder used v26.8.1; CI uses 24. The gate records its own and says so.

## Stamp-time reminders for Tuesday
- Re-read head, main and PR #103's check-runs at launch (five legs were in progress at 18:47; `package` had not appeared).
- Q-1 must be YES (scratch vitest rows, scratch seed edits and scratch mutants in `qa-b546-*` worktrees) or C2-C5 become NOT TESTED as behaviour.
- Pane `Datasec/MPS-M5` (the builder) is live; `Datasec/MPS-G64` (a gate) is live; heavy slots were all free at 18:48 but load was 8-10 (expect waits). Three `npm ci` runs are needed (diff, head, mut worktrees).
- The kit says tier 2 per the builder brief (G2); the diff has no `.cs` and no money design, but `consolidatedBomModel.ts` decides which price figure a quote screen shows or withholds: the tier is Tuesday's stamped call.

## UNMEASURED
Nothing was built, run or fetched. Not measured by me: any CI leg result beyond the 18:47 in-progress snapshot; whether the new rows are red at main for the reasons the builder states; the mutant results; the three new test files beyond scans; the commit bodies and trailers; Jira; the engine and DTO sources; whether a real care row carries `deviceSku`; node 24 availability on the gate machine; load at launch.
