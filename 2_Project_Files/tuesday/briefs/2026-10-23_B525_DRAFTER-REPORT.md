# B525 drafter report (G58 batch gate kit, HPSM-POC PRs #197 and #198), 2026-10-23 13:18-13:30 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B525_SEAT-G58_hpsmpoc-b512-b513-batch-gate-tier2.md` (79 lines), byte-identical `.pre-stamp` beside it (`cmp` ok). Wrote only those two files and this report.

## Open slots
- Four-underscore lines in the kit: **9** = 8 Stamp slot lines (lines 34-41: STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, Heads/main/check-runs, Round rule, Model receipt) + the last line `READ-WHOLE-BY-TUESDAY: ____` (line 79). Measured with `/usr/bin/grep -c -E '_''_''_''_'` = 9 on the kit and on the `.pre-stamp`. The Stamp section states "The unstamped copy reads 9 lines".
- `@[A-Z_]+@` count 0; non-ASCII bytes 0; no person's name; no decision-card id (the only "card" hit is the standing rule text "no decision-card id"). Controls for those counts were not run by me beyond the zero results; the kit asks the gate for controls.

## What I read
Whole: the B523 template kit and its drafter report, the builders' briefs B513 and B512, the builders' STATUS files B513 and B512. Through GitHub GET: `pulls/197`, `pulls/198` (metadata, commits, files with full patches), `commits/<merge sha>` parents, check-runs of both heads, `code-scanning` alerts/analyses, `alerts/12`, main's required contexts, `contents` of `client.ts` (head, lines 296-360) and `revocations.race.test.ts` (head, lines 100-165). Local: `ls-remote`, `lsof`, `tmux list-panes`, `uptime`, `ls` of `.tools`, grep over the briefs folder.

## Facts and sources (13:18 AEDT, read-only)
- main `4db192b0`; `refs/pull/197/head` = branch b513 = `8e1b4688e5454b6bac4c4c76d310b6048ba69de8`; `refs/pull/198/head` = branch b512 = `43c4c25b44132c091a30ee87ad869382db8edf21`. Open PRs: #196, #197, #198.
- #197: 2 files, +99 -0, 1 commit (Sonnet trailer), mergeable true / clean, merge ref `7d8ad53e` (parents main + head); check-runs 20 of 20 completed success; alerts 0; four analyses at the head, 0 results each; new test file 27 rows by patch (10 + 17).
- #198: 3 files, +38 -11, 3 commits (trailer on each), mergeable true / blocked, merge ref `9ca318e7` (parents main + head); check-runs 13 listed: 4 completed (CodeQL neutral, gitleaks, dependency review, Analyze actions), 9 in progress; web e2e legs and `web (Next.js)` absent; alerts 0; one analysis (actions, 0).
- Main: open alerts 0; `alerts/12` instance `fixed`; required contexts five (listed in the kit). load1 15.54 / 12.73 / 11.24.
- Ports: `lsof` 8690-8699 empty (rc 1), and 8600-8699 empty; briefs allocate B510 8560-8569, B512-B516 8570-8619, B517-B522 within 8620-8669, B523 8670-8679, B524 8680-8689; no brief names an `869x` block. Block **8690-8699** chosen. The gate binds nothing (vitest/jsdom only).
- Panes at 13:18: tuesday, fleet-monitor, HPSM-POC-H3, -H4, -H5, MPS-M2, -M3, -M4; no G58 (also none for G56/G57). `.tools/b525`, `.tools/wt-b525-*` absent (control `ls -d .tools/b198` listed); no `refs/heads/b52*` on origin (control `b5*` printed 13 lines). The builders' `.tools/b512`, `.tools/b513`, `.tools/wt-b512-*`, `.tools/wt-b513-*` exist (named as not the gate's).

## Where the template did not fit (and what I did)
- One verdict per PR, not one: the first-line verdict and the last line carry two PR segments joined by `|`, each with `NOT GATED` as a fourth value for a moved head, and REFUSE-at-once split into batch-wide items (slots, pane, ports, auth, node) and per-PR items (head, state, main moved over that PR's paths).
- Escalation list is per PR (STOP that PR, the other continues). A census message that is internal is a Blocker (NO GO on #197), not a stop (the builder brief called it a STOP; the gate has no one to hand it to but Tuesday, so a finding is the right shape).
- No runner/CLI/outer-environment checks (the template's Check 4 and N-mutants for e2e.mjs do not apply); replaced by the census, the screens table, the 311 tolerance measurement (planted-pause cells, edge series, slack-0 repeat), the 316 titles-only and label proof, the 325 difference-set enumeration.
- Extra tree `-both` (#197 head with #198's diff applied by `git apply`, never committed) to run the whole suite once on the combination (expect 189 files, 2300 tests). That is a fifth `npm ci`; if the load will not allow it, the gate says NOT TESTED.
- 316 label proof needs the pre-#181 product (`a93b926a`) written over a tree; the kit makes it conditional (NOT TESTED if the revert is not clean).
- Repeats shortened from the builders' 1000 of the 311 row (about 7 minutes per pool) to 100 per pool plus 10 whole-file per pool plus 5 under contention; the 325 file is repeated 1000 per pool (seconds).
- CI of #198 is pending at drafting: the kit makes the verdict of each PR independent (#197 can reach GO on complete CI while #198 reads `CI pending`).
- Template Stamp had 8 slots; kept 8 (Round rule slot says default round 1 of 2 each).

## Leads I added from reading the patches (to measure, not findings)
- `describeResetFailure` ends in `describeFailure`, so a reset's 400 now shows the API's sentence.
- #197 title says "first error message", commit says `errors[0].message` (Note).
- 311: with `t0` read before the write the measured gap is negative on this machine, so the 20 ms protects nothing measured here; the comment "far below half the stale time" should be checked against the detection edge (k = 1..100 ms series).
- 325: `(?<![\w.-])` and `(?![\w-])` mean `-777`, `1.777`, `0.4321`, `777-999` were caught by the old regex and are not by the new one; the preview carries ranges such as "250-999".
- Sibling `b.waited >= 300` at `revocations.race.test.ts:122` is untouched and unmeasured by the builder.

## UNMEASURED
No npm, vitest, node, fetch, worktree or mutant was run. Not measured: that any new row is green or red anywhere (builder claims only), the exact row names as the JSON reporter prints them, the 27 / 2 / 8 row split beyond counting the patches, the census itself (read from the builder's table, not re-derived), whether either "contract" message names an internal type, the callers of `describeFailure` (taken from the builder's list), the 325 difference set, whether the preview emits any hyphen/dot-adjacent number, CI logs of either PR, the `.pre-stamp` of the builders' briefs, `web/AGENTS.md` and `web/CLAUDE.md` at the heads, PR #196's file list (taken from the B523 kit for the disjointness statement), whether the pre-#181 revert is clean, the panes' state after 13:18.
