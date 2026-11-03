STARTABLE: YES

# B1203 drafter report (SEAT-M89, MPSCALC-373 round 2, tests only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1203_SEAT-M89_mps-373-round2-service-cost-row.md` (67 lines, 9 four-underscore lines, control: the same grep over the file's own Stamp reads them). Drafted 11:02 to 11:08 AEDT 2026-11-03 by `date`.

## BLUF
- A builder kit for ONE commit on the existing branch (head `66a11a45f5c1503bb647bef912d94dd70043ee37`), one path `tests/MpsCalc.Engine.Tests/VolumeBasisTests.cs`, two added rows: a two-line FleetTotal service-cost row (answers B1199-1) and a quantity-zero FleetTotal row (answers B1199-N2, kills GX4). Opus C3, as round 1. Round 2 of 2 = the cap.
- Hand figures are in the kit (revenue 1,518.19, cost 1,062.03; GX2 recomputed cost 981.48; GX3 354.45; quantity-zero 384.29 / 268.50). The seat must re-derive them by hand before running; none is read from Calculate()/Reconcile().
- STARTABLE YES: head unchanged, no overlapping live path, no port, no `.tools/b1203`, no `b1203*` ref.

## Facts re-measured (instrument; control)
- Origin branch head = `66a11a45f5c1503bb647bef912d94dd70043ee37` (`gh api -X GET git/ref/heads/...` --jq .object.sha); origin main `9bdf4548c24e1415bf07d8bcab40f171463f055b`; compare `314b53f6...9bdf4548` lists 3 files (TemplateIsolationTests.cs, contract.sync.test.ts, QuantityAudit.severalDevices.test.tsx), none ours; compare `314b53f6...66a11a45` ahead 2, 3 files (control: matches the round-1 STATUS). Open PRs 121, 120. `matching-refs/heads/b1203` length 0; control `heads/b1093` length 1.
- Every `file:line` in the kit printed by `awk NR` over `git show <head>:<path>`: RentalRecomputation.cs :77 :78 :84 :88 :92 :93 :97; QuoteCalculator.cs :102 :205 :208 :437 :474 :475; QuoteInput.cs :29 :31 :34 :37; Synthetic.cs :82; VolumeBasisTests.cs :6 (the `using`), :25, :155, :203 (row end), :205; ci.yml :42 :43; Directory.Build.props :6; CLARIFICATIONS.md :774 :2218; model-routing.md C3 :93 G1 :108; models_latest.json :17 (opus-5-5; control :11 is fable, :23 sonnet); brief_seat.sh :24 (LEVEL default opus).
- GX anchors: `finance + fixedService + other + softwareCost` occurs on 1 line of the head blob (`grep -c -F`, 1; the anchor with the following `+ line.MonoPagesPerDeviceMonth` also 1). Positive control for the method: the per-device cost line :98 differs (does not match), so the count is not vacuous.
- Arithmetic: python decimal, prec 40, over the kit's fixture (annuity factor 0.2586278037556596, line 1 revenue 1188.4837733, cost 831.4356413; line 2 revenue 329.7069924, cost 230.5948947; totals 1518.1907657 / 1062.0305360; GX2 drop 80.55; GX3 drop 707.58; quantity-zero 384.29 / 268.50). Rounding edges: 0.0042 and 0.0045 from the nearest half-cent. Control: the same script prints 634.29-class sums? NOT run as a control; the q-0 figures equal the round-1 pin table's per-term products (15.09, 369.20, 10.06, 258.44) which the head's committed rows assert.
- Tools: `.tools/b1192/` holds heavy.sh, hb.sh, env.sh, ci-dotnet.sh, engine-test.sh, plants.sh, jira_read.py (7 files) and `scratch/plant.py`, `scratch/trx.py` (`ls`; control: `.tools/b1203` absent, `ls -d` fails). `heavy.sh` light.lock count 1. The round-1 tree `wt-b1192-fix` has the branch checked out (`branch --show-current`), `for-each-ref` on the shared repo printed the branch as `+` in `branch -a`; hence the kit uses a DETACHED worktree and a fast-forward push.
- Panes: `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` showed `%0 tuesday` and `%140 Datasec/MPS-M88`; `Datasec/MPS-M89` count 0. No kit of today names M89 (`grep -l -w -i M89` over 2026-11-02/03 SEAT kits: none, before this one). B1194 kit mentions `VolumeBasisTests` on 2 lines, both in its own refuse/partition (it forbids itself that path and lists round 1's); `ComponentQuantityRuleTests` 14. No `.tools/*/heavy.lock` present at drafting (glob matched nothing). Load 2.67 at drafting; df 230 GiB free.
- Ports: Engine tests bind none (round-1 kit's census, not re-run); listeners at drafting `:49152 :5000 :59869 :7000 :8770 :9660-:9663 ...`, none assigned. No block assigned by Tuesday for this kit.
- Landing rule: quoted from CLARIFICATIONS.md :774; red-first :2218.

## D-decisions (drafter)
- D-1 ONE path, two Facts (not a Theory): the gate asked for one row; a second row for quantity 0 is separate because it cannot use `Priced()` (blocking issue by design) and its plant (GX4) differs.
- D-2 Quantity-zero row IN (the hand figures are clear: 384.29 / 268.50, the base and finance multiply by zero). Quantity -1 and 2.5 get NO row: GX4 dies at 0; the others add rows without a new plant. Recorded as a FOR TUESDAY item for the seat.
- D-3 Two lines (A3 Standalone q 3, A4 Colour q 4) so both fixed-service branches (`:77`) are killed, with NO base override so the reconciler's own base sell (:84, which holds the service costs) is exercised on the revenue side. Both quantities reuse the existing two-line row's, which reconciles at Core; the Core tier at quantity 4 is therefore RELAYED from that green row, not separately measured.
- D-4 Finance 6% a year (the gate said above 0%); GX3 is killed at 0% too (round-1 finding N6), the 6% adds the annuity path.
- D-5 Extra plants GX5 (drop only `other`) and GX6 (drop only `fixedService`) so a half-drop cannot survive; both predicted red on the service row (16.80 and 63.75 on cost).
- D-6 Detached worktree + fast-forward push (branch is checked out in the finished round-1 tree; no write to another seat's tools).
- D-7 Target READY 90 / HARD STOP 180 minutes (a one-row round; round 1 used 150 / 300).
- D-8 Round 1's plant predictions for the new rows (PA PB PC PE PH PI +2 each, PD PF +0) are labelled UNMEASURED guesses; a difference is reported, a round-1 row turning green is a STOP.

## Q-questions for Tuesday (each with a default)
- Q-1 Model: Opus C3 (`model-routing.md:93`) as the task says, although tests-only is arguably C2 (Sonnet first, `:92`). Default: Opus C3 (same seat model as the round that took the NO GO; the cap leaves no third round).
- Q-2 Should the seat also add a row for a fractional or negative quantity (2.5, -1)? Default: NO (GX4 is killed by quantity 0; the gate's note N2 asks only for a priced total below quantity 1).
- Q-3 The gate's reading ("a surviving plant is Major when no COMMITTED row kills it"; option C would count the gate's own probe) is superseded by option A here; confirm the product owner took option A (the kit assumes it, from the task). Default: A.
- Q-4 Hard stop: the Stamp slot carries the outer bound; the kit gives 90 / 180 minutes. Default: not after 16:30 AEDT as round 1.
- Q-5 Branch local tip: after the push, the shared repo's local `b1192/...` ref (checked out in `.tools/b1192/wt-b1192-fix`) stays at `66a11a45`; Tuesday's landing reads origin. Default: leave, no local ref write.

## UNMEASURED
- The two new rows' actual outputs at the head (not run; the drafter ran no dotnet). The Core tier of `A4Colour` at quantity 4 with 6% finance (precedent only). Engine count 712 after (710 + 2). The gate's claim that quantity 0 agrees at the head (RELAYED from the gate STATUS, not re-run). The round-1 plant count deltas.
- The control for the python arithmetic (see Facts): not run.

## Outside the fences, disclosed
- Read: the gate STATUS (a 36 KB read via the tool-result file) and `residue.md`, `card-input.txt` (head); NOT `.tools/b1199/**`. Read round 1's builder STATUS (grep only) and `.tools/b1192/*` script heads. Read the B1194 kit by grep (paths and lock only). No `decision_queue.sh`, no Jira, no HTTP beyond `gh api -X GET`. A first git call used a zsh `$S:path` substitution that failed (no effect); two hook refusals (a word-split variable, an unquoted `=====` echo) re-run in a safe form. One scratch file written: the head's VolumeBasisTests.cs copy in the session scratchpad. Only the two named files were written under the project tree.
