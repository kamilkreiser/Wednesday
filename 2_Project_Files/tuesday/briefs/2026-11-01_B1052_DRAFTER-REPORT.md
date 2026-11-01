STARTABLE: YES

# B1052 DRAFTER REPORT - SEAT-G261 tier-1 QA gate of B1049 (HPSMPOC-428 wake open retry, code half)

Drafted 2026-11-01 15:23-15:40 AEDT by a read-only drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1052_SEAT-G261_hpsmpoc-428-wake-retry-gate-tier1.md` (68 lines; 8 four-underscore lines = 7 stamp slots + the last line; 0 non-ASCII; 0 `@X@` tokens). Shape: the B1022 HPSM-POC tier-1 gate kit (claims, subject, round count, WHAT THE GATE JUDGES, checks, severity, verdict lines, STATUS-NOW, partition, standing lines, REFUSE, Stamp, launch).

## BLUF
- A tier-1 gate (G1, `model-routing.md:108`, Opus; G-cap `:111`) for `b1049/hpsmpoc-428-wake-open-retry` @ `35b343a483dfa773e21969c1089acf49f4db3acf` on main `a3a06b9ad334b16a16fd51f7fc23e138f8e58fa2`. Ahead 1, behind 0, 3 paths: `AssessmentModule.cs` +2 -1, `SqlServerWakeRetry.cs` +71 -0, `SqlServerWakeOpenRetryTests.cs` +334 -0. This matches Tuesday's 15:23 read.
- Round 1 of 2 on the NEW class "API retry of a connection open that timed out during a database wake". The census found 0 earlier gates on this class. The gate must re-run the census and write a paragraph answering "honest new class, or a renamed fourth round?".
- **The main new lead, from the drafter's read of EF source (not run).** EF calls `ConnectionError`, and so every interceptor's `ConnectionFailed`, on a failed CLOSE as well as a failed open. The places are `RelationalConnection.cs:907-909` (sync) and `:976-978` (async) at v10.0.12. The logger routes both to `ConnectionFailed`/`ConnectionFailedAsync` (`RelationalConnectionDiagnosticsLogger.cs:776-841`).
  - So `OpenFailureMarker` also marks a -2 thrown by a close. The comment "i.e. thrown while OPENING" (`SqlServerWakeRetry.cs:38-39`) and the commit sentence "so no command was sent" may be false.
  - If a close runs inside the strategy operation after a write (SaveChanges, a transaction site), a retry could repeat the write.
  - The kit makes this a never-cut scratch row, S1: a close throws a forged -2 after a counted non-query. It is run at head and at main.
  - The gate must then settle two questions from source: can SqlClient's `Close`/`CloseAsync` throw that form at all, and is a close inside the strategy operation for queries, SaveChanges and the transaction sites?
  - Grading is fixed in the SEVERITY table, in three steps:
    - Blocker if the retry is reachable after a write.
    - Major if the retry happens but reachability is unproven.
    - Minor (false text only) if SqlClient provably cannot throw it there.
- Also new beyond the builder kit:
  - (a) Nested scopes. `HandledRace.Active` is the INNERMOST scope, so an `Expect(key)` nested inside `ExpectAnyFailure()` re-enables the retry. The kit includes a census of the 6 keyed sites plus a reachability check.
  - (b) EF's `Exists` loop. It retries -2 itself (`SqlServerDatabaseCreator.cs:320`) and runs under the module strategy. A -2 it finally throws was raised by an open, so it is marked. Host start-up on SQL Server can now be retried whole.
  - (c) SqlClient's pool blocking period can rethrow the SAME exception instance. That means the weak table's per-instance marking needs its own row.
  - (d) Every retried open now logs EF's Error 20004, even when the request ends 200.
  - (e) The write window, a third trade-off that the commission did not name: a write whose open timed out can now land after the page showed its error. This is the same class as B994's N-1.
  - (f) `RequestAborted`. A probe tests whether cancellation reaches EF's wait.
- The budget is re-derived. Tuesday's "~56 s" earliest give-up holds for the pool-wait form only.
  - For a -2, EF adds 5 s to every wait. `-2` is the last label of `IsThrottlingError`, at `SqlServerRetryingExecutionStrategy.cs:262`. So the earliest give-up is about 86 s, and the abandoned-call cost is about 296 s rather than 266 s.
  - The builder found this (its first Correction), and the commit message already says "at least 86 s after a login timeout". The kit's PR body text carries both figures.

## Facts re-measured (instrument; control)
- Remote pins (`gh api -X GET`, project `GH_CONFIG_DIR`), 15:24:31:
  - main `a3a06b9a...`.
  - `matching-refs/heads/b1049` = 1 ref, `35b343a4...`. `heads/b1052` 0 (control `heads/b1034` 1).
  - compare: ahead 1, behind 0, 3 files, with blob ids `843dcdda` / `47fd3c8f` / `15926695`.
  - Open PRs 0. PRs for the branch 0.
  - check-runs on the head 0 (control: main's 19). `actions/runs?head_sha` 0.
  - Parent `a3a06b9a`. verified false. One Sonnet trailer.
  - Repo squash settings: COMMIT_OR_PR_TITLE / COMMIT_MESSAGES.
- `ci.yml` at the head: blob `0176b491...`, 679 lines. Predicate lines re-read:
  - `on:` 14-18.
  - api job `:32`, timeout 25. `dotnet test` `:87`. Azurite names `:89-123`.
  - Shard job `:165`, timeout 30 `:170`. Filters `:250-257`. Predicate `:274-316` (TRX all Passed, four named tests per part, databases >= 100 / >= 110). `api-sqlserver` `:353-365`.
  - Shard wall note `:162-163`.
- The diff of `AssessmentModule.cs` was read whole: one registration line replaced and one comment line added. `SqlServerWakeRetry.cs` was read whole. The test file was outlined: 11 rows, with the T10 SQLite branch at `:311-333`.
- The shared `2_Project_Files` lacks both `a3a06b9a` and `35b343a4` (`cat-file -t` fails). The `77c3132e:api` tree is `992581f7...`. The gate's own clone must fetch both.
- EF Core v10.0.12 source, fetched with `gh api -X GET` (6 files):
  - Detector: 708 lines. `//case -2:` `:699`, comment `:696`, `return ex is TimeoutException;` `:706`.
  - Strategy: 270 lines. `DefaultMinDelayThrottling` 5 s `:36`. Ctor `(ExecutionStrategyDependencies)` `:58-61`. `ShouldRetryOn` `:156`. `GetNextDelay` `:181`. `IsThrottlingError` `:217` with `case -2:` at `:262`.
  - Base: `DefaultMaxRetryCount = 6` `:32`, `DefaultMaxDelay` 30 s `:37`. `RetriesOnFailure` `:161-166`. Sync loop `:209-259` (`Thread.Sleep` `:258`). Async `:315-370` (`Task.Delay(delay, ct)` `:369`). Guard `:381-401`. Formula `:427-440`. `CallOnWrappedException` `:486-500`.
  - `EnableRetryOnFailure()`: `SqlServerDbContextOptionsBuilder.cs:41-42` = `new SqlServerRetryingExecutionStrategy(c)`, the same constructor the new factory uses.
  - `RelationalConnection.cs`: 1149 lines. Open `:757-797`, close catches `:907-909` / `:976-978`.
  - Logger: `ConnectionError` -> `ConnectionFailed` at `:776-802` / `:812-841`.
  - `SqlServerDatabaseCreator.cs`: 384 lines. `Exists` under the strategy `:175` / `:236`. Its own -2 retry `:320`.
- Builder STATUS: 210 lines, last line `READY FOR QA: B1049 ... @ 35b343a4...`. `## PRIOR WORK` is present (line 30). The BLUF (line 22) and MEASURED (line 148) are stale ("not pushed", "NOT READ"); the push read-back is at line 207. The evidence folder holds 31 names.
- Round census: 547 `*_STATUS.md` files and 132 `GATE VERDICT` first lines. The wake filter returned 6 hits (B994, B997, B1006 on the old class; B1003 and B1010 on keep-awake; B772 unrelated), and 0 on the new class. Control: `customer security preview` = 4. Last lines:
  - B994 `NO GO (round 1 of 2)`
  - B997 `NO GO (round 2 of 2)`
  - B1006 `GO WITH FINDINGS (round 3, the last)`
- Product source census at `77c3132e`, whose `api` tree equals main's:
  - `HandledRace.Expect(key)`: 6 sites.
  - `ExpectAnyFailure`: 2 flows (from the builder kit).
  - Product connection interceptors before this commit: 0.
- Landing source: records repo `datasecau/HPSM-POC-analysis` main `e0c9bb87`. `CLARIFICATIONS.md` is 5096 lines. Line 138 reads "squash-merged head-pinned". The PR #270 landing entry at line 5082 reads "a head-pinned squash". The local checkout of that file is 192 lines and stale, so it is not cited.
- Main's squash subjects carry the ticket key (`a3a06b9a` "HPSMPOC-388: ...", 1 trailer).
- Ports 9160-9169:
  - `lsof` LISTEN 0. With a `python3 -I -B` listener on 9169: 2. After: 0.
  - Word-boundary scan of the 83 non-`.pre-` SEAT kits dated 10-31 and 11-01: `916[0-9]` 0 hits. Control `915[0-9]` hits the B1049 kit.
  - Live panes: no claim on the block.
- Panes, 15:25:
  - `%0 tuesday`
  - `%165 Datasec/MPS-G260`
  - `%164 Datasec/NexusAI-G259`
  - `%163 Datasec/HPSM-POC-D44`
  - `%160 Datasec/NexusAI-M62`
  - `%1 fleet-monitor`
  - No G261 or H92 pane. G261 appears in 0 brief file names (control G260 also 0 by file name; the pane exists).
- Load: `uptime` load1 7.25 at 15:25.
- Model: `models_latest.json` line 17 `claude-opus-5-5`. `brief_seat.sh` line 24 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`. The launch line carries `BRIEF_SEAT_LEVEL=opus`.
- `.tools/b1052` and `.tools/wt-b1052-head`: absent. Helpers present: `b198/lock.sh` (`L=` line 4), `b267/waitload.sh` (threshold 6), `b649/jira.py`, `dotnet/dotnet`. `.tools/wt-b1049-*`: 2 names. `.tools/b1048`: present (forbidden to the gate).

## D-decisions (drafter's; Tuesday accepts or strikes at the stamp)
- D-1: tier 1 on Opus, per the B1049 stamp's GATE-ROUND slot.
- D-2: the close path is a never-cut check. Its grading is fixed in the table.
- D-3: the gate writes the four landing files. The PR body must state:
  - the code half only;
  - the two trade-offs (about 90 s dead-DB error; 266 s pool-wait or 296 s login-timeout abandoned cost);
  - the write window, if measured;
  - that the SQL Server leg is judged on the PR.
- D-4: the landing-file hygiene regex is `(^|[^A-Z])C-[0-9]`, not `C-[0-9]`. The template's pattern counts the `C-428` tail of `HPSMPOC-428`, which the title is allowed to carry.
- D-5: the gate's own mutants are g1-g13 plus the g15 equivalent control. g14 (Feedback context) is NOT RUN, because it is outside the 3 paths. At most 24 plant runs.
- D-6: real sockets (C6 (e)) are optional and the first thing cut under load.
- D-7: suggested target verdict 150 min, hard stop 210 min.

## Q-questions for Tuesday (each with a default)
- Q-1 Round count: honest new class, or a fourth round of the old one? Default: honest new class (the B1049 stamp's Q-1). Reasons: different mechanism, EF's count and cap kept, a new product owner ruling. The gate still writes its own paragraph, and STOPs before C9 if it disagrees.
- Q-2 Close-path grading: Blocker if reachable after a write, Major if unproven, Minor if provably unreachable. Default: as written.
- Q-3 Write window (C7 (c)): grade it a Note for the product owner, the same as B994 N-1. Major only if ONE user action writes twice. Default: as written.
- Q-4 Ports: 9160-9169. Tuesday assigned no block in the commission, so the drafter chose the next free block after H92's 9150-9159. Default: accept.
- Q-5 Should the gate read `dotnet/SqlClient` source by `gh api -X GET`? It is needed to settle close-path and blocking-period reachability. Default: yes, in S4 (Launch authority).
- Q-6 Does a NO GO mean a round-2 fix kit, with a second NO GO going to the product owner on a card? Default: yes.

## UNMEASURED by the drafter
- No clone, build, test, scratch row or plant was run.
- The close-path retry is a reading of EF source, not a runtime result. Whether SqlClient can throw -2 from `Close` is not read.
- Whether a close runs inside the strategy operation for queries and SaveChanges is not read.
- SqlClient's blocking-period rethrow is from memory of SqlClient's design; the gate must read the field and lines.
- Whether `RequestAborted` reaches EF's wait in `ListCustomers` is not read.
- The BFF write-limit rows were not re-read.
- Linux SqlClient's form for a refused port is not known.
- The SQL Server leg; T10 on SQL Server.
- Whether D44 is still live at launch.

## Outside-the-fences disclosure
- Read-only throughout. Files written: only the two named. Scratch copies of EF sources, head files and the census went to the session scratchpad.
- Project-repo git: read verbs only (`cat-file`, `rev-parse`, `show`, `grep`, `remote get-url`, `rev-parse --show-toplevel`), all with `--no-optional-locks`.
- `gh` calls: `-X GET` only, under the project `GH_CONFIG_DIR`, against `datasecau/HPSM-POC`, `datasecau/HPSM-POC-analysis` and `dotnet/efcore`.
- One `python3 -I -B` listener ran on 127.0.0.1:9169 for 6 s as the port control. It exited on its own.
- Not done: no Jira read, no `decision_queue.sh` in any form, no HTTP to any hosted host, no az/ssh/docker. No `fleet/briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY tree or non-Datasec project was read.
- `ls` of the project root listed a SOW `.docx` and `HP Reporting and Docs/` by name only. Neither was opened.
- One `echo` separator was refused by the zsh hook and re-run with `----`.
- No card id appears in the kit. The product owner is never named.
