# B320 DRAFTER REPORT (2026-10-20, clock from `date`: 12:54-13:05 AEDT)

Brief: `2026-10-20_B320_SEAT-G16_composer-gate-pr82-tier2.md` (same folder, about 43 KB, a little over the ~40 KB target). Wrote only that file and this one. Ran only reads: `ls-remote`, `gh api` GETs (pulls/82 and its files, issues/326 and 327, check-runs, code-scanning analyses and alerts, pulls?state=open), `git show` / `diff` / `log` / `cat-file` in the Composer repos, `decision_queue.sh list` and `show`, `lsof`, `uptime`, `date`, and `BRIEF_SEAT_PRINT_MODEL=1 brief_seat.sh` (print-only, launches nothing).

## What I read
Whole: B290 gate brief, B297 round-2 gate brief, B290 drafter report, B301 builder brief, B301 ADDENDUM-1, B301 STATUS. Listed: B301 evidence `runs/` and `kit/`. Read at the lines the brief cites: BACKLOG rows 84, 320-322, 326, 327 at root `main`; the full PR diff; `brief_seat.sh`; the header of `decision_queue.sh`. NOT read: B290/B296/B297 STATUS files (the builder STATUS quotes the lines the gate needs), the evidence tables themselves, the charter.

## Measurements (all read-only)
- 12:54:46 `ls-remote`: main `d8d2a2c7…`, branch = `refs/pull/82/head` = `e62889831069135abc25e61b08f2f59f8196e4fd`. PR #82: open, draft, head branch `b301/ci-timing-test-truth-326-327`, base `main` at `d8d2a2c7`, 2 commits, 2 files, +68/-5 (b20 +2/-2, s47 +66/-3), mergeable clean. Only open PR is #82. `gh` identity `kamilDatasec`; the project's `4_Credentials/.gh-config` exists.
- **GitHub issues #326 and #327 do not exist (HTTP 404).** They are BACKLOG rows (root `main:BACKLOG.md:322-323`). The rows have no "Done when" field; the brief says so and grades against the rows' fix-shapes plus the builder brief's R-W10-2.
- 12:55: check-runs `CodeQL`, `Analyze (csharp)`, `Analyze (javascript-typescript)` completed / success on `e6288983`; both analyses for `e6288983`, `results_count` 0; open alerts on the PR ref 0. **The template's "main open list is non-empty" control does not fire** (open alerts on main = 0); I replaced it with `state=fixed` on main = 20, dismissed 0.
- Load: 8.09 (12:54:40), 7.22 (12:54:51). `lsof` on 7480-7499 rc 1; no file in Tuesday's `briefs/` names 748x/749x. Picked **7480-7489** (reserve, no stack runs).
- Decision queue: `list ruled --undelivered composer-` printed 18 ruled cards, none about timing tests or CI; the relevant ones are `composer-two-lanes-past-90pct-1011` = a and `datasec-80pct-band-build-lanes-1020` = c (the reason this gate launches). Section included.
- Diff read at head: the new test `overSingleSplit` (`s47…test.ts:257`), `SINGLE_SPLIT_BOUND = 3` (`:255`), comment `:246-254`, `it` title `:333`; `TIMEOUT_MS` 600,000, `GROWTH_*` 5 / 30 / 20,000 (MEASURED).
- Launch line: `cockpit.sh` exists; `BRIEF_SEAT_LEVEL=sonnet` prints `claude-sonnet-5-5`. Exact line is in the brief.

## My own traps (things I added beyond the commission)
1. **P3, the +150 ms LINEAR plant.** Whole and pieces cost alike, so the split cannot see it; only `BOUND_MS` 250 can, and the linear reading (~26 ms) + 150 stays under 250. Expected GREEN at head and at base: pre-existing, and not claimed (R-W10-2 rejected the tight absolute bound). Graded Note, not Blocker, unless the builder's text claims the class. This is the honest answer to "+150 ms regression".
2. **P4 shape probes:** fixed-cost-per-call plant (ratio < 1, passes by design), threshold-only plant above 100,000 characters, and a plant super-linear only in windows under 16,384 characters (ratio ~1). Only the threshold case is graded Major if GREEN.
3. **Piece-count assert** (64 pieces, concatenation equals whole; "cisco enable secret 5" is 1,048,575 characters) and a check that `Math.max(bestPieces, 0.05)` never binds with the 1 ms thread-clock granularity (it would turn the test into a false red).
4. **Base run as control for every mutant**, because the builder saw the OLD file red on D = 14000 in 3 of 6 runs while B290/B296 saw green: the gate measures the pre-existing blindness on its own machine state.
5. **Builder FOUND 4** (comment says "x6.51 or more", test runs printed down to x6.38) is graded in r6 with a threshold (Minor if the lowest test-printed D = 14000 ratio is under x3.75).
6. r7 checks only that the STATUS in `records/b301` matches the working copy up to the READY line; records text is not gated.
7. Per-issue verdict tokens (#326, #327, PR) in the verdict line.

## Decisions you may want to change
- Severity floors are mine (Blocker: new test passes D = 14000 / 10000 in all of >= 3 runs; Major: coin flip, or a flake in the 20-run hog loop; Minor: margin under 25%).
- Hog sample sizes: 20 two-file runs per arm, 5 quiet, 4 full `ci:node` under hog (builder did 8; the gate does not pool).
- Gate may copy the path-quoted harness from `.tools/b301/` (or the evidence `kit/`); B290/B296 copies are named as bad (unquoted `$L`).
- Slots left: MODEL, STAMP_TIME, B_NUMBER_CONFIRM, PORT_BLOCK. Defaults: `claude-sonnet-5-5`, your launch time `2026-10-20 HH:MM AEDT`, `B320`, `7480-7489`. The slot grep prints 2 (lines: the Drafted line and the SELF-CHECK line) on the file as written; the `.pre-stamp` copy is yours to make (I wrote no third file).
- `PC_E8_SOW_TEXT` is a PROPOSED confirmation for you to rule at stamp.

## UNMEASURED
- Whether the project's `Briefs/` folder already holds a `B320` file (I grepped Tuesday's `briefs/` only; the brief tells the gate to grep it at Step 0).
- Pane name `Datasec/Security-Composer-G16` collision with a live pane (not checked).
- Whether any Composer seat or heavy NexusAI / HPSM-POC seat is live at launch (load only).
- Whether the image `pc-b301-node:head` or a cached layer set still makes `docker build --pull=false` a cache hit for the gate.
- Whether the B301 evidence `kit/` equals `.tools/b301/` (I did not diff them).
- The B290/B296 STATUS lines the builder cites (`B290:92-101`, `:101`, `:192`; `B285:32`) other than B285 F7 (`:32`, which I saw says what the builder claims).
- `records/b301` content beyond its `--stat` header and the sha (`f18c6fff…`, rev-parse and `show` header read); the 86-file count.
- Whether the new test's runtime (14.7 s vs 10.3 s) is stable.
- Any other open card touching these files (I read two cards in full; the rest only by id).

## Open questions for Tuesday (each with a recommendation)
1. Rule `PC_E8_SOW_TEXT` for the full-step rows? Recommend yes (same as B281/B290/B297/B301).
2. Is Note the right grade for the linear +150 ms plant GREEN at base and head? Recommend yes: pre-existing and outside the row's fix-shape; carry the numbers to a card only if Kam wants an absolute-bound row.
3. Run the hog loops while another heavy seat is mid-build? Recommend launch only when no NexusAI / HPSM-POC build is mid-flight (R-W10-6).
4. Should the comment-vs-run ratio gap (x6.51 vs x6.38) be a third commit? Recommend no unless the gate grades it Minor.
5. Should `wt-b296-rec`'s uncommitted row 326 be quarantined (duplicate-#326 risk, builder FOR TUESDAY 4)? Recommend yes, by Tuesday, outside the gate.
