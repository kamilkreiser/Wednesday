STARTABLE: YES (all slots empty for Tuesday to stamp; heavy-slot-3 is free, slots 1 and 2 are held by B752 and B757 so the gate may wait or take 3; ports 9450-9459 clean; model Opus via BRIEF_SEAT_LEVEL=opus in the launch line)

# B763 DRAFTER-REPORT: round-2 (the cap) gate for `b745/mps-walk-caps` @ db571786

Drafted 2026-10-26 about 21:55-22:00 AEDT by the read-only kit drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B763_SEAT-G156_mps-walk-caps-round2-gate-tier1.md` (84 lines).

## BLUF
- Tier-1 gate, round 2 of 2 on class walk-cap (THE CAP), pane `Datasec/MPS-G156`, ports 9450-9459, Opus (row G1, `model-routing.md:108`, cap row `:111`). Shape copied from the B748 round-1 gate; checks cut to seven (C1-C7) around what round 2 can fail: the three fix-shapes met by the gate's OWN mutants, the 14 round-1 survivors killed (Pass A at the round-1 head reproduces them, Pass B at the head kills them), kills retained (seeded sample of 20 of the 94), the interruption audit, the CI line at the combined tree.
- The cap wording: a NO GO is NO GO 2 of 2, no round 3, the closed instances ship and the residue is ticketed per G-cap; the kit says that is a card for the product owner and the gate only says which instances are closed and which are residue.
- Drafter prediction in the kit: GO WITH FOLLOW-UPS (conditional: CodeQL NOT SCANNED). Live risks named: a same-family variant the gate did not name, the interrupted mutant pass (builder lost its pane about 21:03), weight.

## Facts re-measured (instrument + control)
1. Branch head `db57178676ee253479677fbcd723419fbc90ea9c`, main `1137f11962c9adbee84c119fe7dd2f545bd4a42a`: `git ls-remote` at 21:56:32; control: the same call lists the `b745` branch and `refs/pull/*` (it printed 100+ pull heads).
2. Delta: `gh api -X GET compare/d259ae1d...db571786` = ahead 1, behind 0, one file `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs +89 -0` (blob `d9655c54...`). Local `diff --numstat` `89 0`; `rev-list --left-right --count` `0 1`; `rev-parse db571786^` = `d259ae1d`; removed lines `grep -c -E '^-[^-]'` over `-U0` = 0 (control: added lines `^\+[^+]` = 81, plus 8 blank added lines = the 89 of numstat); one hunk `@@ -584,0 +585,89 @@`; non-ASCII in the diff 0 and in the commit message 0 (positive control not run for these two: UNMEASURED as a control, the count is an absence reading).
3. Product blob `681c9cc49a89...` identical at `d259ae1d` and `db571786` (`rev-parse "${h}:path"`; first attempt with `$h:path` was eaten by zsh `:t` modifier and printed garbage, then redone with `${h}:path`). Test file 585 lines / 35 `[Fact]` at the round-1 head, 674 lines / 38 at the head (`grep -c -F '[Fact]'`; control `zzz-no-such-string-7f3a` = 0).
4. Builder READY line is the last line of B754 STATUS (166 lines), quoted whole in the kit. B754 STATUS has a PRIOR WORK heading at line 38 (`grep -n -i 'prior work'` 4 lines; control 0).
5. Round count: B748 STATUS line 1 is `NO GO round 1 of 2 ... majors+: B748-1, B748-2, B748-3`; line 38 states "This gate: NO GO 1 of 2 on the class". So before this gate NO GO 1 of 2; the kit's re-measure of the frame is a gate task.
6. Main moved: `compare 2e7f9d8a...1137f119` ahead 2, files `src/MpsCalc.Import/Parity/ParityProof.cs`, `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs`, `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs` (commits #117, #122); none on the REFUSE guard list. `compare 1137f119...db571786` diverged 3/2 (the kit's `2 3` for `origin/main...branch` is the same fact the other way round). Round 1 measured Engine 435 / Import 193 / Api 3093 at a combined tree on this main; the kit predicts Api 3099 (UNMEASURED).
7. Open PRs: #120 and #121 only (`pulls?state=open`; dependabot, each `web/package-lock.json`: `pulls/<n>/files`). No PR for the branch (length 0). `commits/db571786/check-runs` total_count 0; `code-scanning/analyses?ref=refs/heads/b745/mps-walk-caps` length 0 (no positive control: an empty read, so "NOT SCANNED").
8. Live panes (`tmux list-panes -a`): `wednesday`, `Datasec/Security-Composer-R50`, `Datasec/MPS-M35` (B757), `Datasec/MPS-G153` (B752), `Datasec/HPSM-POC-H38`, `fleet-monitor`. No `MPS-G156`. Heavy slots: `heavy-slot-1` holder `B752 21:27:00 web`, `heavy-slot-2` holder `B757 21:54:22 m341`, `heavy-slot-3` absent. `.tools/b763` and `wt-b763-*` absent (glob "no matches"; no positive control run for this one: UNMEASURED control).
9. Ports 9450-9459: `lsof -nP -iTCP:9450-9459 -sTCP:LISTEN` empty (rc 1; no bind control run by me this time); word-boundary, letter-aware python scan over 153 non-`.pre-` SEAT kits of 10-25/10-26: 0 hits for `945x`, control `975x` 11 hits.
10. Model: `models_latest.json:17` `levels.opus.model_id` = `claude-opus-5-5`; `brief_seat.sh:24` defaults to Opus; row G1 text quoted in the kit from `model-routing.md:108` (header cells) and `:111`.
11. Landing rule lines: `CLARIFICATIONS.md:809` and `:854` both read "The landing rule, applied at the landing: squash with the head pinned (`--match-head-commit`, the MPS convention ..." (sed); project `CLAUDE.md:50-52` is the CodeQL ruleset paragraph (it names an earlier coordinator seat as the PR opener; the kit says Tuesday holds the project since the handoff).
12. Commit message of the head (gh api): one paragraph, one `Co-Authored-By: Claude Opus 5.5` line, no key, no id. Squash of three commits will carry three attribution lines.
13. Stamp check on the kit: four-underscore grep 8 lines (7 slots + last line); `@[A-Z_]+@` 0; name grep (`kam|kreiser|friday`) 0; non-ASCII 0.

## Decisions
- D1: Checks reduced from nine to seven; sibling census, docs-sentence census and the 100,000-line adversarial table were round 1's and the product bytes are unchanged, so they are not re-run (the kit says so under NOT TESTED). Default: keep.
- D2: The gate builds its OWN battery from the round-1 findings text (not the builder's scripts), including variants beyond the 14 (other counters seeded, half seeds, required entry suppressed, count error suppressed, budget inside the loop). Default: keep.
- D3: Pass A at a `-mut-r1` worktree (round-1 head) reproduces the 14 survivors as the control that the battery can fail. Default: keep.
- D4: Gate may read the round-1 gate's published evidence only after its own battery table is written (as round 1 did for B663/B678). Default: keep.
- D5: Verdict token best case remains GO WITH FOLLOW-UPS conditional (no PR, CodeQL unscanned), as round 1.
- D6: Seeds chosen: 763101 (kill sample), 763102 (seeded edits), 763103 (equivalence differential); the kit also excludes the prior seeds.

## Questions for Tuesday (each with a default)
- Q-1: Q-1 permission for scratch mutants in `wt-b763-mut`. Default YES.
- Q-2: The builder's pane was killed at about 21:03 mid-pass; the kit asks the gate to audit that the mutant results describe the committed blob (C4 f). Default: keep as written; stamp if you want it dropped.
- Q-3: Heavy slots: slot 3 is the only free one now. Default: the gate waits for or takes a free slot only, per the kit.
- Q-4: The B748 findings B748-4/-5 (Minor, pre-existing) are restated only. Default: no ticket action from this gate.
- Q-5: The project `CLAUDE.md` still names the earlier coordinator seat as PR opener. Default: kit says Tuesday; a records note is yours.

## UNMEASURED
- Everything runtime: 3048 / 3099 / the 14 of 14 red / 135 variants are the builder's claims or my arithmetic; no build or test was run.
- Whether the builder's recorded test-file sha256 for Pass B matches the committed blob (the gate's C4 f). I read the STATUS lines about it but did not compare shas.
- Positive controls for: `.tools/b763` absence, the 945x `lsof` read, non-ASCII counts, `code-scanning/analyses` empty read.
- Whether another live branch (`b744/mps-feedback-triage-my-feedback`, ahead 1, 18 files vs main) shares a path: overlap program is a gate task (C6 d).
- CodeQL on the branch (no PR): not scanned.

## Outside-the-fences disclosure
Wrote only the two files. Read: DRAFTER_RULES.md, the B748 kit and STATUS, B754 kit (head, grep) and STATUS, B740 kit (head), routing rows, models_latest.json, brief_seat.sh, B757/B758/B752 kits by grep for path overlap, CLARIFICATIONS lines 809/854, project CLAUDE.md lines 50-52, `.tools` holder files (cat). Git: read verbs only with `--no-optional-locks` in `2_Project_Files` (ls-remote, rev-parse, rev-list, show, diff, cat-file, grep not used). `gh api -X GET` under the project config dir only. No fetch, merge-tree, worktree, checkout, commit; no dotnet; no decision-queue, Artifact, Docs, mail, chat, Jira, or HTTP to a hosted site. Two minor slips: one zsh `$h:path` expansion error that printed git errors (harmless, redone), and the kit's first draft line about the PRIOR WORK heading said it was not found by eye (corrected in the kit after measuring).
