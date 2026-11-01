STARTABLE: YES

# B1049 drafter report (SEAT-H92, HPSM-POC builder for HPSMPOC-428: the API retries a connection open that timed out during a database wake)
Drafter: Agent-tool sub-agent for Tuesday, 2026-11-01 14:06 to about 14:40 AEDT. Kit: `briefs/2026-11-01_B1049_SEAT-H92_hpsmpoc-428-wake-retry.md` (155 lines). It has 9 stamp slots plus the last line, so **10** four-underscore lines. `@[A-Z_]+@` reads 0, non-ASCII 0, the card id 0, person names 0. Template: the B1034 kit (stamped, read whole). **No `.pre-stamp` was made:** DRAFTER_RULES allows two files only, so the copy is Tuesday's to make.

## BLUF
- **The cause in source: the 500 was a failure EF did not retry at all.** Making the retry schedule longer would not have helped. The API already uses `EnableRetryOnFailure()` (`AssessmentModule.cs:102`, EF defaults 6 / 30 s). With those defaults, a retried failure cannot end before the six waits add up to about 56 s. A 500 at 29.3 s therefore lands just under the API's `Connect Timeout=30` (`infra/modules/appservice.bicep:101`). Two connect-time failures end there, and EF 10.0.12 retries neither:
  - SqlException **-2**: the line is commented out at `SqlServerTransientExceptionDetector.cs:699`.
  - SqlClient's **pool wait**: a plain `InvalidOperationException`. The detector retries only SqlException numbers and `TimeoutException` (`:706`).
  The repository already says this in its own words: `HostedDemoStartup.cs:144` reads "neither of which EF Core's retrying strategy retries". Which of the two UAT actually threw is UNMEASURED (UAT keeps no API output).
- **The change.** A strategy class derived from `SqlServerRetryingExecutionStrategy`, with the same 6 / 30 s and the same error list, plus one marker interceptor. The class also retries those two forms, under two conditions:
  - Only when thrown while **opening** the connection, so no command was sent. A command-phase -2 is still not retried.
  - Only **outside** `HandledRace.ExpectAnyFailure()`. That keeps the hosted start-up read's designed single retry and its SQL Server tests unchanged.
  It covers the Assessment context only. The diff is three paths: the registration line, one new product file and one new test file. There is no setting, no `Connect Timeout` change and no package change.
- **Budget.** The BFF cuts each GET call at 30 s and the browser asks up to 3 times, only on a BFF 504 (`bff.ts:148`, `readRetry.ts:19`, `:29`). That gives 90 s. After the change the API gives up on an open timeout no sooner than 56.0 s, so the BFF always cuts first and the browser asks again. A wake of 46 to 65 s is served on call 2 or call 3. Two costs go to FOR TUESDAY:
  - A call the BFF abandons can keep the API busy for up to 266 to 268 s if the database is dead.
  - A dead database now shows its error at 90 s instead of about 30 s.
- **Prior work is used, not repeated.** B992's API commit (`a9025f2f`, 10 retries with a 15 s cap) was reverted by B995 because it pushed CI's SQL Server leg past a 300 s timeout (B994-1). The kit keeps EF's count and cap and has row T8 to guard them. `ImportFailPathTests` forges its failures on commands (1205, 547), not on opens, so its timing does not change.
- **HPSMPOC-207 does not share the fix (D-3).** Its socket reset during login happens in the start-up read, which this change deliberately leaves alone. That error is neither -2 nor on EF's list.
- **Seat and ports are free.** H92 appears in 0 kits. Ports 9150-9159 show 0 listeners and 0 word-bounded hits in the 80 non-`.pre-` SEAT kits dated 10-31 and 11-01. The sibling deploy lane B1048 (D44) is named in the PARTITION; no path is shared.

## Facts re-measured (instrument; control)
- **Main and branches.** Main is `a3a06b9a` (`gh api git/ref/heads/main`). `compare 77c3132e...a3a06b9a` reads ahead 2, behind 0, 31 files, all under `web/`. The `api` tree at main is `992581f7`, equal to `77c3132e:api` (`gh api git/trees` and `git rev-parse`). The `.github` tree is equal too. Open PRs 0. `matching-refs/heads/b1049` 0 (control `b1034` 1). The shared repo lacks `a3a06b9a` (`cat-file` fails) but holds `77c3132e`, so every `api/` file was read there.
- **The card.** Read with `decision_queue.sh show hpsmpoc-428-wake-500-fix-choice-1101` into a scratch file; the id count is 1. Status ruled, choice `a` "Fix it in code (retry during a wake)", detail "No cost; built and checked like any lane; proven on a real pause later". The card's `ruled_ts` is **2026-11-01T14:04:27+11:00**, while your brief says 14:03:43. The kit writes both, unreconciled, in the C-260 form.
- **Jira** (project helper `.tools/b1007/jira.py`, GET only, token never printed):
  - HPSMPOC-428 is Backlog. Its summary says "about 29.5 s". Its Done-when: "a database wake no longer loses a read to an API 500 in a measured visit on an environment that pauses, or the item is recorded as declined".
  - HPSMPOC-207 is Backlog with 8 comments. Its shapes are a login socket reset (error 35) and a pool-wait timeout at the start-up read; B192/B195 already retry the latter once. Comments by B179/B181 record `Connect Timeout=30` applied on the hosted demo.
- **B1031 STATUS** (318 lines). Lines 160-166 hold the wake test: 500 at 29.46 s; API Http5xx 1, max 29.338 s; 504 at 30.28 s; 200 at 55.62 s. Line 185 is NOT TESTED "Which SQL error". Lines 214 and 217 give the fix shapes.
- **C-260** (analysis main `e0c9bb87`, `CLARIFICATIONS.md:5054-5080`). It records the 500 as HPSMPOC-428 and leaves "which fix ... a scope call, not made here". The landing rule is a head-pinned squash: `CLARIFICATIONS.md:138` and C-256 to C-261.
- **EF 10.0.12 source** (`gh api -X GET repos/dotnet/efcore/contents/...?ref=v10.0.12`):
  - The detector has 176 `case` labels.
  - Present: 40613, 40197, 40501, 49918/49919/49920, 4060, 233, 10928/10929, 64, 20, 121, 10053/10054/10060, 11001, 1205.
  - Absent: -2 (commented out), 18456, 35, 0. Control: 40613 counts 1.
  - Throttling errors add 5 s to each wait.
  - The constructor taking `(ExecutionStrategyDependencies)` means defaults 6 / 30 s.
  - `RelationalConnection.OpenInternalAsync` puts the opening interceptor and the real open inside one `try` and calls `ConnectionErrorAsync` on any non-cancellation failure. That is the hook the marker interceptor relies on.
  - The builder re-measures the list from the loaded assembly in step 4.
- **Transactions.** 7 `BeginTransaction` sites, each inside `CreateExecutionStrategy().ExecuteAsync`, out of 8 strategy sites. This matches B994:143.
- **Existing tests.** `HostedDemoSlowFirstLoginTests` (`HostedDemoRobustnessTests.cs:522-700`) assert the start-up read's single retry on SQL Server. Without D-2's scope exclusion, two of its three rows would go red. A forge helper (`:862-871`) and an interceptor that throws on open (`:851-858`) already exist and are reused by the new rows.
- **CI** (`ci.yml` blob `0176b491`). It runs on push to main, `pull_request` and `workflow_dispatch`, so a branch push with no PR fires nothing. The SQL Server pass predicate: dotnet test rc 0 per part; every TRX outcome `Passed` (a skip fails); four named tests; database floors 100 and 110. The `Hosting.` namespace runs in part `api-assessment`. This machine has no SQL Server and no docker (relayed from B994 and B809), so the SQL Server leg is judged on the PR.
- **Ports.** `lsof -iTCP:9150-9159 -sTCP:LISTEN` 0 (all-listeners control 16). 0 hits in the 80 kits (control `974x` 10). Two hits in the project's 10-06 and 10-20 STATUS files are old and closed.
- **Panes** at 14:14: tuesday, MPS-M61, NexusAI-M62, NexusAI-M63, fleet-monitor. No HPSM-POC pane is live. load1 3.79.
- **Model.** `model-routing.md:92` C2 "1st"; `:93` C3; `:94` C4; `:108` G1; `:109` G2; `:111` G-cap. `models_latest.json:23` is `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- **B1048 kit** (120 lines, written 14:13; no drafter report seen yet). It deploys `a3a06b9a` to UAT. Its tree is `.tools/b1048/` and its ports 9740-9749. It does no fetch, worktree or ref write in `2_Project_Files` and pins S by sha (lines 53 and 91-93).

## D-decisions
- **D-1:** Add the two connect-timeout forms, retried at OPEN only. EF's count, cap and list stay the same. This rules out `errorNumbersToAdd` and any longer schedule.
- **D-2:** The change does not apply inside `HandledRace.ExpectAnyFailure()`.
- **D-3:** HPSMPOC-207 is not shared and not touched.
- **D-4:** Assessment context only.
- **D-5:** No setting and no app-setting write anywhere.
- **D-6:** One new test file, testing behaviour only, in `Hosting`. It compiles at main, which allows the red-first run. T10 runs only on SQL Server.
- **D-7:** Own clone, one commit, Sonnet; target READY 120 minutes, hard stop 180.

## Q-questions for Tuesday (each with a default)
- **Q-1, GATE-ROUND.** Default: **round 1 of 2 on a NEW class "API retry of a connection open that timed out during a database wake"**, commissioned by the product owner's 14:04 ruling. The earlier class "wake-tolerant reads: the BFF read budget and the API retry policy" ran B994 NO GO 1 of 2, B997 NO GO 2 of 2 and B1006 GO WITH FINDINGS round 3, the last; its API half was reverted. The alternative is to treat this as a 4th round of that class, which would need the product owner's word under G-cap.
- **Q-2, gate tier.** Default **tier 1 on Opus** (`model-routing.md:108`). The change touches the persistence path of every API request, and a wrong open-phase rule could retry a write. The same mechanism was gated at tier 1 in B994, B997 and B1006. The alternative is tier 2 on Opus (`:109`).
- **Q-3, D-4.** Leave the Feedback context on `EnableRetryOnFailure()`? Default **yes**. Adding it is one line, but the fix needs no Feedback read, and B992's both-context change is part of what was reverted.
- **Q-4, builder model.** Default **Sonnet** (C2, line 92). The kit spells out the design, including the open-phase rule and the scope rule. B992's Sonnet builder had the wrong mechanism (a longer schedule). If you want the extra margin on EF internals, launch with `BRIEF_SEAT_LEVEL=opus` and change the model line.
- **Q-5, timings.** Target READY 120 minutes, hard stop 180. Default yes.
- **Q-6, seat, ports and sibling.** H92 with ports 9150-9159, running alongside B1048 (D44). Default yes: no shared path, repository write or Jira write.
- **Q-7, budget lines 3 and 4.** A dead database shows its error after 90 s instead of about 30 s, and an abandoned call can keep server work going for up to 266 to 268 s. Accept both as consequences of the ruling? Default **yes**, recorded in the PR body by Tuesday. Neither adds cost, and both apply only while the database is unreachable.

## UNMEASURED
- No clone, build or test was run.
- Not measured: the red-first and plant outcomes; whether the suppressed open and suppressed read run on the SqlServer context with no server (the kit gives a fallback); exact compile details such as interceptor signatures and `ConditionalWeakTable.AddOrUpdate`; T10 and the whole SQL Server leg, which run only on a PR.
- Not measured: whether `RequestAborted` reaches EF's wait; which exception UAT's 500 carried; the live UAT connection string (only the template was read); whether the hosted demo still pauses.
- **The ticket's Done-when (a measured visit on a pausing environment) is NOT met by this lane.** The kit says so, and leaves the proof as a later step.

## Outside the fences (disclosure)
- I wrote only this report and the kit, with the Write tool.
- I read the card only with `decision_queue.sh show <exact id>` into a scratch file. I never ran `list`.
- Git in the shared repo used read verbs only (`--no-optional-locks`: `show`, `grep`, `cat-file`, `rev-parse`, `ls-tree`, `for-each-ref`). `gh` used `-X GET` only, under the project's `GH_CONFIG_DIR`.
- The EF Core source reads were `gh api -X GET` calls to the public `dotnet/efcore` repository on GitHub, not to any project host. I count them inside fence 4 (gh GET only); flagging them here in case you read the fence more narrowly.
- I made one Jira GET call through a scratch Python wrapper that imports the project helper `.tools/b1007/jira.py`. The token was read in-process and never printed.
- I sent no HTTP to any hosted, UAT or demo host and ran no `az`, docker or ssh.
- My first `git show` attempt failed on a zsh `$B:a` modifier, then succeeded with `${B}:`. It made no write.
