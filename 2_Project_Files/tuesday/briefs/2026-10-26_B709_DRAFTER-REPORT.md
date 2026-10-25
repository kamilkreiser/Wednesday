STARTABLE: YES

# B709 drafter report (SEAT-H29, HPSM-POC, lane H-TIMING, ticket HPSMPOC-354)
Drafted Mon 26 Oct 2026 from 07:52 AEDT (clock from `date`) by a Sonnet kit drafter. Kit: `2026-10-26_B709_SEAT-H29_hpsmpoc-354-timing-rows.md` (121 lines, 8 stamp-slot lines by `grep -c`, 0 at-sign placeholders, no person name by grep -i).

## BLUF
- One path, three small test-only edits: (A-1) `Assert.True(logged > held.Ms + Slack, ...)` after the row's `Assert.Throws`; (A-2) reword the `(finer: green at 1190, red at 1200)` parenthesis (the one existing line changed, numstat deleted = 1); (A-3) a read accessor on `StagedFactory`'s private statics and one rest-state assertion in the row after the try/finally.
- Done-when is mutant-driven and written as before/after: P3 (product, `UseEndpointStage` start read moved after `await next`) and Q (`Stage(m, "rest")`) are green on the base rows and must be red on the edited rows; s1-s3 (DisarmOnly resets removed) and regression r1/r2 (Slack 1500; literal 1100) add the rest.
- CI predicate written in: the class is in namespace `...Tests.Hosting`, so it runs in the `api-assessment` SQL Server shard (ci.yml filter lines 250-252); step "the tests ran on SQL Server, every one, and passed" (line 274, `bad` at 303, 100-database floor at 314) needs every outcome Passed. The seat cannot run SQL Server: UNMEASURED-ON-SQLSERVER, argued from the gate's 208-224 ms margin.
- Base `b069274cfc201bc451ab2c22dc6adc2a6e231bef` (main at 07:5x, compare `identical`), file blob `9ce335ce...` equals the gate's PR-head blob (file unmoved since #219). 0 open PRs, no `b7xx` branch. Model Sonnet, line 92, `claude-sonnet-5-5`. Ports 9760-9769 free (positive control fired); no PR or file overlap with B708 (`infra/tests/test_ci_workflow.py`) or B710 (`web/src/e2e-runner.test.ts`).

## Facts re-measured (instrument, control)
- main: `git ls-remote` = `b069274c...`; `gh api compare/b069274c...main` status `identical`. Open PRs: `length` 0; control `state=closed&per_page=3` = 3.
- Branch census: pages 100/100/34/0 (234 branches); prefix filter `b70x|b71x` found none; same line's `354|timing` alternative fired on 5 older branches (control). `b684/hpsmpoc-timing-floor-rows` and `b514/...` exist (merged heads), not yours.
- File: 653 lines, 39,257 bytes, `git hash-object` of the saved raw bytes = API `sha` = `9ce335ce34883ed12d8b1befaa69b294a364261d`; sha256 `ddcc2401...` equals the gate's recorded "before" hash; 17 Fact / 4 Theory by `grep -c`; non-ASCII 0; `NOSUCH` pattern 0. `finer` occurs twice (lines 182, 310): only 310 is stale.
- Jira (project helper, read whole, GET): HPSMPOC-354 Backlog, 0 comments, Done-when quoted. Gate B691 STATUS lines 1, 58-62, 140-142, 190-196, 216-220 read.
- ci.yml (679 lines) at the base: `on:` push main / pull_request / workflow_dispatch; shard matrix `part: [api-assessment, api-other-and-feedback]`; filters at 250-255.
- Ports: `lsof -nP -iTCP:9760-9769 -sTCP:LISTEN` rc 1 (empty); control: python listener on 9761 listed. Word-boundary scan of 102 non-`.pre-` SEAT kits of 10-25/10-26: 9 other kits hit, 15 lines (B626 x6, B630, B631, B633, B640, B646, B647, B648, B683 x2), all finished lanes or phrases; none live. Live panes: `tuesday`, `Datasec/NexusAI-M13`, `Datasec/Security-Composer-G133`, `fleet-monitor`. B708 takes 9750-9759.
- Landing: `rules/branches/main` types `deletion,non_fast_forward,code_scanning,required_status_checks`; squash head-pinned per CLARIFICATIONS line 138 and the gate's command. #219 = squash `ceb196495e...` merged 2026-10-25T12:08:16Z.
- Shared clone does NOT hold `b069274c` or `ceb19649` (`cat-file -t` fails): the kit tells the seat to fetch under its lock.

## D-decisions (drafter's)
- D-1: no new `[Fact]` for the DisarmOnly reset; the in-row assertion pins it in any run order (the ticket allows "one assertion, or one tiny test"). A new name is Tuesday's call.
- D-2: the `finally` block itself is not pinned (needs a planted throw, gate mutant L); the kit makes the seat record that in STATUS as the Done-when's "records why a line cannot be pinned" branch for that one line.
- D-3: the reworded parenthesis states no 1190 colour at all (the gate's three draws flip), and still says nothing about SQL Server; `SQL Server: not measured` stays.
- D-4: the comment line reword is the single permitted deletion in the diff (numstat deleted = 1, printed, with a control); the brief's other tests say "byte-equal".
- D-5: Part B drops P1, P2, P4 and the gate's other mutants (the gate ran them); only P3 and Q are Done-when.
- D-6: gate class named "NO GO 0 of 2 on this class" (assertions added to one row plus a comment parenthesis); B691's own verdict (GO WITH FINDINGS, round 1 of 2) said no round of its class was spent.

## Q-questions for Tuesday (each with a default)
- Q-1: Add one tiny `[Fact]` that `ArmOnly` then `DisarmOnly` returns the statics to rest? Default: NO (in-row assertion only; zero new test names).
- Q-2: Comment on HPSMPOC-354 and leave HPSMPOC-318 open after landing? Default: Tuesday comments after landing; 318 stays open for its SQL Server clause.
- Q-3: Launch order versus load: load averages were 8.15 7.37 6.54 at 07:54, above the 7 limit for heavy runs; default: launch when load1 is below 7 on two reads (the seat waits through `dn.sh` anyway).

## UNMEASURED
No dotnet, worktree, plant or mutant ran; P3 and Q reproduction on this machine; the new assertion on SQL Server; the whole of `UseEndpointStage` (lines 92-113 only seen through a filtered listing, the P3 anchor count is for the seat to print); accessor visibility under `TreatWarningsAsErrors`; the whole-project seconds today; `dn.sh`'s `B=` line being the only seat-number line.

## Outside-the-fences disclosure
I wrote only the two files named (this report and the kit). Reads: DRAFTER_RULES, the template kit, the sweep (HPSM-POC and LANES sections, via grep and a line range), the B691 STATUS and evidence patch log, ci.yml and the test file at the base via `gh api -X GET` into the session scratchpad (`.../scratchpad/b709/T.cs`, `ci.yml`), one Jira GET through `.tools/b653/jira.py`, the product file `RequestTimingLog.cs` through a filtered `gh api -X GET`, the sibling kits B708 and B710 (listing and a ports grep of B708). Git in the project clone: `cat-file -t` twice (both failed: commit absent), nothing else. One socket bound on 127.0.0.1:9761 for 6 s as the port positive control (freed). I read `.tools/b653/jira.py` and `.tools/b649/` (a directory listing only) in the project; both are read-only reads. No decision card, no `fleet/briefs_staged`, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no HTTP to a hosted host except the GitHub and Jira APIs, no mail or chat or publish tool.
