STARTABLE: YES

# B820 drafter report (MPS MPSCALC-354, M-FEED, seat Datasec/MPS-M44)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B820_SEAT-M44_mps-354-feedback-case-and-warning-rows.md` (125 lines). Drafted 13:00-13:15 AEDT (clock = `date`; first `date` read 13:02:16).

## BLUF
- Startable once stamped, with one wait: load1 was 11.02 at 13:04 (`LC_ALL=C uptime`), the kit's heavy-run gate is below 7, so the seat polls.
- Two rows in one file: R-1 = one `InlineData("HIGH")` on the existing priority theory (kills K31c); R-2 = one new `[Fact]` asserting the whole hosted-store warning with a regex for the random probe name (kills S02d). Cap 3 names, expected 2. One commit, one path, no product byte.
- Model Sonnet (`claude-sonnet-5-5`, `models_latest.json` line 38), rows L6 line 85 / C2 line 92, gate G2 line 109, G-cap line 111; launch line carries `BRIEF_SEAT_LEVEL=sonnet`. Pane `Datasec/MPS-M44`, ports 7610-7619 (unused), branch `b820/mps-354-feedback-case-and-warning-rows`, gate round "1 of 2 on this new PR" (the coordinator's 13:0x ruling).
- Slot lines: 8 four-underscore lines (7 slots + last line), non-ASCII 0 (python, control not needed: count of bytes above 127 is 0 and the file holds plain ASCII), no person name (the one `Kam` hit is the scan instruction itself, as in the template).

## Facts re-measured (instrument, time)
- Main: `gh api git/matching-refs/heads/main` 13:0x = `32b09108a5c476249498d22229debe3e73c8a5d6`; check-runs on it `{"success":8}`. Open PRs 121, 120 (`pulls/<n>/files` piped to `/usr/bin/grep -c -x -F` for the feedback test path: 0; control: path piped to itself 1). The project's local `2_Project_Files` checkout is stale (`log origin/main` tip `b8ae901`), so everything was read from origin through `gh -X GET`.
- Jira: MPSCALC-354 read through the project `.env` in process (Backlog, labels lane-h / tier-2, 0 comments in the read; text quoted in the kit). Control: `MPSCALC-99999` answers HTTP 404.
- Files at main by raw contents: `FeedbackTriageTests.cs` 735 lines, 40,813 bytes, blob `b4736b8c` (sha1 of `blob <n>\0<bytes>`; control `abc` -> `f2ba8f84`), equals the ticket; `FeedbackStore.cs` 636 lines, blob `aac80cbd`, equals the ticket. Priority theory `:638-650`, `InlineData("urgent")` `:640`, `InlineData(null)` `:641`; existing hosted-warning row `:713-734`; nested `OpenModes` `:704`.
- Product reading: `TriagePriorities.All = [normal, high]` (`FeedbackStore.cs:76-79`); warning built at `FeedbackStore.cs:194-201`; findings from `QuoteFileStore.ProbeModes` (`:174-202`): dir findings then one `.mode-probe-{Guid:N}.tmp` finding, `"{name}: set 0700, read back 0777"` format (`CheckMode` `:205-220`, `Octal` `:223`); `FeedbackAttachments.Folder = "attachments"` (`:48`); `PlatformModesKey = "MpsCalc:QuoteStore:PlatformModes"` (`QuoteFileStore.cs:19`); `ResolveHosted` returns `GetFullPath(configuredPath)` so the `{dir}` in the warning is the path the existing row passes. Counts of anchors (`/usr/bin/grep -c -i -F`, control `zzz-no-such-string-7f3a` 0): `notes == notes.Trim()` 1, priority term 1, `runs WITHOUT private file modes` 1, `string.Join("; ", findings)` 1 (line 194), `.mode-probe-` in `QuoteFileStore.cs` 1, `"HIGH"` in the test file 0 (control `"urgent"` 1), `Regex` 0, `AcceptPlatformModes` 0.
- Build config (raw): `ImplicitUsings` enabled, `Nullable` enabled, `TreatWarningsAsErrors` true; `System.Text.RegularExpressions` is not implicit, so the kit says to fully qualify or add one `using` line.
- CI: `.github/workflows/ci.yml` lines 28-43 read raw; predicate written into the kit.
- SDK: `dotnet` not on PATH (the sweep says so); `'.tools/dotnet/dotnet' --version` printed `10.0.401` (kit names it; `global.json` says `10.0.100`).
- Seat name: python word-boundary scan of the 257 non-`.pre-` briefs of 26-27 Oct for `MPS-M44` and `SEAT-M44`: 0 (M40 to M50 all 0); control `MPS-M39` fires 11. Panes at 13:0x: `tuesday`, `Datasec/Security-Composer-R62` (%65), `Datasec/HPSM-POC-D38` (%63), `Datasec/NexusAI-M21` (%62), `fleet-monitor`.
- Ports: `lsof -nP -iTCP:7610-7619 -sTCP:LISTEN` empty, rc 1; scan `(?<![0-9])761[0-9](?![0-9])` over the same 257 files: 0 hits; control `960[0-9]` fires 9. The bind control of the lsof instrument was not repeated (the seat repeats it in its REFUSE step).
- Branch/tools: `heads/b820` 0 refs (control `heads/b7` lists ten refs, one of them the stale `b789/mps-residue-test-rows`); `.tools/b820` and `.tools/wt-b820-fix` absent (control `.tools/b789` lists). No heavy-slot or git-lock entry in `.tools`.

## D-decisions (override at the stamp)
- D1 Sonnet. D2 cap 3 names (expected 2). D3 R-2 is a NEW `[Fact]`, not an edit of the existing warning row (existing assertions never edited). D4 no product byte. D6 one commit. D8 pane M44. D9 one push.
- D10 (drafter, not in the kit as a number): hard stop 3 h and target READY 1.5 h after Step 0 (smaller than B789's 4 h / 2.5 h because the lane is 2 rows and one file); the template's "never later than 11:00" is replaced by the stamp's own limit (11:00 has already passed today).
- D11: the regex is built with `Regex.Escape` on the test's own temp path; the probe name is matched by `\.mode-probe-[0-9a-f]{32}\.tmp` and the final `\z` anchor pins the last full stop.

## Q-questions for Tuesday (each with a default)
- Q-1: seat name `Datasec/MPS-M44`; B819 and B821 drafters choose in parallel and may collide. Default: keep M44; re-run the pane and kit scan at the stamp.
- Q-2: round count: "round 1 of 2 on this new PR, tier 2" per the ruling; the findings' class read NO GO 0 at gate B794 anyway. Default: as written.
- Q-3: hard stop / target READY of 3 h / 1.5 h. Default: as written; the 11:00 cutoff of the template cannot apply today.
- Q-4: heavy slot while load1 is 11.02: the seat waits and polls at 20 s. Default: launch now anyway (the kit gates the heavy runs itself), or hold the launch until load1 is under 7.
- Q-5: an optional second `InlineData` (`"Normal"`) was left out; K31c is a single edit and one case kills it. Default: not added.

## UNMEASURED
- The expected warning text is a reading of the source (findings order `feedback`, `attachments`, probe file; `0700`/`0600`/`0777`), not a run. Nothing was built or run; `dotnet` was not used.
- Whether S02e (the join `"; "` -> `", "`) and S02f survive the base rows: the kit makes it a measure-first cell.
- Whether `Assert.Matches` with `\z` is accepted as written; the 247 Feedback-class name count at main (the gate's figure at head); the load at launch (11.02 at 13:04).
- Jira comment count and status were read once; not re-read after drafting.

## Outside-the-fences disclosure
- Read-only reads only: Jira GET through a scratchpad reader of this session (`w/jr.py`, loads the project's own `.env` in process, no token printed), `gh api -X GET` under the project's `GH_CONFIG_DIR` (matching-refs, pulls, pulls/<n>/files, contents raw for the feedback test file, `FeedbackStore.cs`, `QuoteFileStore.cs`, `FeedbackAttachments.cs`, `ci.yml`, `Directory.Build.props`, the csproj, git/trees, check-runs), `git --no-optional-locks ls-remote` and `log` (read verbs) on the project checkout, `lsof`, `tmux list-panes`, python scans of the briefs folder, local reads of the project's published `Briefs/2026-10-27_B794_STATUS.md` (a gate STATUS, claims), `model-routing.md`, `models_latest.json`.
- Scratch copies of the raw files live in the session scratchpad `b820/` (not committed). `.tools/dotnet/dotnet --version` was executed once (version query only; no build).
- Not touched: `decision_queue.sh`, `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, any WEDNESDAY / FRIDAY tree, any hosted host, az, ssh, docker, any Jira or GitHub write, mail, Artifact or Docs tools. Two Bash calls were refused by hooks (a zsh `=====` separator and a `cd`) and re-issued correctly; three greps drew the case-sensitivity advisory, and the counts that matter carry a positive control above.
