STARTABLE: YES, after Tuesday fills the slots (S2 = the head sha40, S3 = MAIN plus the base sha40 and the main sha40 read at the stamp, with PR 292's state). The builder has READY (its STATUS last line, read at drafting as claims) and the branch is at origin; the daemon looks up (8 `com.docker` processes) but no docker verb was run by the drafter.

# Drafter report: B1343 SEAT-G356, tier-2 gate of b1326/hpsmpoc-308-two-hosts-sqlserver (drafted 17:30-17:42 AEDT 2026-11-06)

## BLUF
Kit `2026-11-06_B1343_SEAT-G356_hpsmpoc-308-gate.md` (61 lines, ASCII, 8 lines carry a four-underscore run: seven slots and the last line) plus `2026-11-06_B1343_slots.json`. Sonnet, G2 (`model-routing.md:109`, cap `:111`), round 1 of 2, new class, one test file (+195 -0). Answers by step: Q1 plants G1 (retry removed), G2a/G2b (kill removed two ways), G3/G4 (lookup unrestricted with a bystander session), G5 (counter file), 30 cases each; Q2 the CI predicate written from `ci.yml:251-316` with the Azurite exclusion; Q3 added seconds per shard against `timeout-minutes: 30` (`ci.yml:170`) and the required `api` job's 25; Q4 kill reach and residue by snapshot of `sys.dm_exec_sessions`/`dm_tran_locks` with a live bystander; Q5 `sa` permissions by program plus a low-privilege control login; Q6 308 clause by clause and the 319 B469-5 line. Main-moved rule, landing rule, docker grant and the builder's container are in the kit.

## Facts re-measured (instrument; control)
1. Refs 17:30 (`gh api -X GET`): main `f422028651c415ef698a342120299170a1a29698` (= base); `matching-refs/heads/b1326` one row `f8adb612...` (control `b1295` 1 row); `commits/f8adb612`: one parent, one file +195 -0; `compare` ahead 1 behind 0 (reverse: behind 1). Blobs: test file base `7965f9cb...`, head `5364c3b5...`; `HostStartRetry.cs` `e402defe...`.
2. Message: subject 98 chars, one trailer, non-ASCII 0 (control planted U+200B counts 1); head file non-ASCII 0; removed lines 0, added 195 (`diff`), `Assert.` 62 -> 70, Theory 9 -> 10, Fact 8 -> 8; hygiene tokens 0 (control `Thread.Sleep` 1); one ticket key in added lines (`:636` retry-line prefix).
3. PR 292: open, **30 changed files** (the note said 29; `pulls/292` `.changed_files` and the `files` list both print 30), +124 -721, one `ci.yml` hunk (line 623, an `infra` step name), `Program.cs` comment line, `UatOpenAuthentication.cs` +6 -24. Intersection with the branch's path 0 (control: `ci.yml` counts 1), with `Hosting/`/`Support/` 0.
4. CI step (`ci.yml` raw at base, `awk NR==n`): shard job `:165`, `timeout-minutes: 30` `:170` (job level), parts `:175`, image `:184`, `sa` `:223`, test step `:251-252`, counter step `:263-270`, proof step `:274-316` (`:303` bad = any outcome not Passed), named tests `:281-286`, floor `:314`. The `api` job `:32`, `timeout-minutes: 25` `:35`, `dotnet test` `:87`. `api on SQL Server` not required (`:164`).
5. Hosted times (`actions/workflows/ci.yml/runs?...status=success`, 10 newest main push runs, `runs/<id>/jobs`): api-assessment job 954, 937, 888, 650, 929, 944, 1030, 888, 693, 744 s (median 908.5, max 1030 = 57 percent of 1800); test step median 771, max 882; api job max 1005 s (67 percent of 1500). Control: the same instrument reproduces the builder's 650 and 1030.
6. Ports 9400-9409: `lsof` listeners 0 (control all listeners 12); word-boundary scan of 53 non-`.pre-` SEAT kits of 5-6 Nov: 3 hits (B1314, B1338, B1341), all their own "printed 0" scan lines, none allots the block (control `939x` 3, `934x` 7); pane list has no HPSM-POC pane.
7. Docker: `ps -axo command | grep -c com.docker` 8; socket dated 6 Nov 14:55. No docker verb run.
8. Landing/ticket sources: records `CLARIFICATIONS.md` at `b4432413...` (5711 lines): `:3617` rule, `:5636` latest landing entry with the phrase, `:5114` C-263, `:5648` C-300 (all printed). Jira GET (`.tools/b60-jira.py`): 308 Done-when and clause (1), the 2 Nov comment, 319 B469-5 fix-shape and Done-when (printed).
9. Round count: loop over line 1 of 717 STATUS files, 166 `GATE VERDICT`; retry-related gates B469, B607 are GO WITH FINDINGS; no NO GO on this class; control B469 appears.
10. Feedback `HostStartRetry.cs` vs the Api copy (raw, `diff`): header line and namespace only; Feedback filter `:49`, `LockNotHeld` `:24`.
11. Mechanics read from the row (head `awk`): the kill is aimed by lock resource and `DB_ID(@database)`, requires exactly one holder, else records `Unexpected` and kills nothing; the row's database is never dropped (`SharedDatabase.cs:35-40`, `TestDatabase.cs:21-23`).

## D-decisions
- D-1 New class "real-session-loss row for the Api test-host start retry (one Api test file)", NO GO 0 of 2: B469/B607 judged forged-fault retry rows and were GO WITH FINDINGS.
- D-2 Tier 2 stays (tests only) but the kill step is written as a security-shaped item: any reach beyond the row's own session/database sends it to a tier-1 gate.
- D-3 Time predicate judges ADDED seconds (at most 90 on api-assessment, the builder's own budget) and the projection (at most 80 percent of the limit), not one hosted figure; hosted variance (650 to 1030 s) dwarfs the row.
- D-4 The shard is run whole once at the head (to apply the CI proof step's own python to a real trx), with the Azurite rows as the one stated exclusion (one container only).
- D-5 Gate's own plants split the kill removal in two (G2a no call, G2b call replaced by `SELECT 1`) to show the retry assertion is independent of the kill count; G4 (guard removed) is run only against the gate's own bystander.
- D-6 B469-5 is judged on the gate's own fresh local run, and the kit tells the gate to say the hosted log will NOT carry the 1223 line (the row keeps its retry lines out of the file and the log).
- D-7 HPSMPOC-308 clause (3) ("green on 3 consecutive main pushes") is stated as after-landing: the ticket cannot close on this branch.
- D-8 The builder's slot-leak (hv.sh copy without a `quarantine` folder) is written into the kit as a precaution.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block 9400-9409? Default: yes.
- Q-2 Tier 2 Sonnet? Default: yes.
- Q-3 Class name and "NO GO 0 of 2 before"? Default: yes.
- Q-4 Hard stop Step 0 + 150, target + 120 (emulated SQL Server, full shard once)? Default: yes.
- Q-5 Run the whole api-assessment filter once on the emulated server (long: Assessment sums 1108 s of test time in CI)? Default: yes; drop to the Hosting namespace only if load makes it exceed the hard stop.
- Q-6 Let the gate `DROP DATABASE` its own `hpsmpoc%` databases inside its own container between run sets? Default: yes (the builder did the same; no `docker rm`).
- Q-7 The builder's container `hpsm-h131-mssql`: the gate only lists it (`docker ps -a --filter`) before and after and never starts, execs, stops or removes it. Housekeeping (it holds about 213 databases) is Tuesday's later call. Default: left stopped.
- Q-8 If `docker info` shows no daemon, one `open -a Docker`, wait 3 minutes, else STOP. Default: yes (the product owner's 14:56 word).
- Q-9 Does a local forced-probe run (not a CI job) close HPSMPOC-319's B469-5 line, given the filter that saw the 1223 is the Api copy of `HostStartRetry.cs` (same code as the Feedback copy the ticket names) and the hosted log will never show it? Default: the gate reports it; Tuesday decides at the records step.
- Q-10 PR 292 will land first: the kit allows a moved main off its STOP list and adds a merged-tree build (Step 6) if main has moved. Default: yes.
- Q-11 Container name `hpsm-g356-mssql`, password file `4_Credentials/g356_sa.pw`: fine? Default: yes.

## UNMEASURED
No docker verb was run by the drafter: the daemon state (only inferred from 8 `com.docker` processes and the socket date), whether the image is present, `sa`'s permissions, every runtime figure of the builder (30 of 30, 16 existing rows red, 3.35 s median, 71 s namespace), whether the kill ever reaches another session, what remains on the server, the added seconds against the limit, the hosted job's own `sa` login and timing, whether the full shard runs inside the gate's window on an emulated server, whether Azurite-only rows are the only non-Passed ones locally. The builder's STATUS was read as claims (its last line, BLUF, PRIOR WORK, ROW, PLANTS, BUDGET, FOR TUESDAY); its trees and the container were not touched. The merge result of PR 292 with the branch was not built.

## Outside the fences
Read only: DRAFTER_RULES, the B1324 kit/report/slots (and `.pre-stamp`/`.pre-tuesday`), the B1326 builder kit (`.pre-stamp`) and STATUS in the project's `Briefs/`, 717 STATUS first lines, `model-routing.md`, `models_latest.json`, `gh api -X GET` (refs, matching-refs, commits, compare, pulls and pulls/292/files, raw contents of `ci.yml`, the test file, `HostStartRetry.cs` x2, `SharedDatabase.cs`, `TestDatabase.cs`, the analysis repo's `CLARIFICATIONS.md`, `git/trees`, `actions/workflows/ci.yml/runs` and `runs/<id>/jobs` for 10 runs), `lsof`, `tmux list-panes`, `ps`, `ls` of the socket. One Jira read: I loaded the project's `.tools/b60-jira.py` by `importlib` from a scratch script (GET `/rest/api/3/issue/HPSMPOC-308` and `-319`, token never printed): the project's own helper, as the kit's rules ask, but it is an older seat's script file. Wrote only the three B1343 files and scratch files in the session scratchpad. No decision_queue, no ledger, no briefs_staged, no Artifact/Docs, no mail, no az, no docker, no ssh, no HTTP to a hosted host.
