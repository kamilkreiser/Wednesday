STARTABLE: YES (stamp when you want it; read D2, D3 and Q1-Q3 first; the PR's CI is already complete and all-green on the head, so a GO is reachable, not capped)

# B809 drafter report (SEAT-G171, Datasec / HPSM-POC, QA gate tier 2 round 2 of 2 on PR #222) -- drafted Tue 27 Oct 2026 from 10:41 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B809_SEAT-G171_hpsmpoc-222-timing-rows-gate-round2.md` (101 lines). Checks on the file: four-underscore line count 8 (7 Stamp slots + last line; grep with the split pattern; the kit's own mention of the pattern is split); non-ASCII 0 (`LC_ALL=C grep -c '[^ -~]'`, no planted-byte control run); at-sign-capitals-at-sign tokens 0; owner-name tokens 0 (no positive control run); no decision-card id; no typed clock in a slot. The drafter ran no clone, fetch, worktree, dotnet or mutant.

## BLUF
- Head `595b0b59` = merge of main `d415a3fe` into `7b3f3c76`; the test file blob `447c5b79` is identical at both; `pulls/222` open, mergeable clean, 20 of 20 check-runs success (both SQL Server shards, aggregator, CodeQL, 4 Analyze, 5 e2e), runs `40419287463` and `40419282710` success; 4 of 4 code-scanning analyses at the head, results 0.
- **Main moved to `bf4a7bdd` (#232 squash).** compare main...head = ahead 2, behind 1, one file. #232's 5 paths: `UatOpenAuthentication.cs` (a `demo`-label branch in `Read`), `Program.cs` (comment-only hunk), two tests, two web auth files. Count of its paths matching `Timing|Caller|ci.yml|Hosting` = 0. I read both api patches: nothing touches the timing path or the test factory. The kit makes the gate prove it (read the patches, `git grep` the class for UatOpen use, run Hosting on head-merged-with-main).
- Round count: NO GO 1 of 2 on class "assertions added to one existing Api test row plus one comment parenthesis, tests only" (B719 verdict line; its single Blocker was external CI). Kit states a second NO GO is the cap.
- SQL Server: shard log (job `121909380542`) gives totals only (1261 passed, 287 databases, retried 0, 0 hits for the class name, control `Passed!` printed); the 28 rows by name come from artifact `api-sqlserver-test-results-api-assessment` (not expired). Kit has the recipe, controls, and margin test (B719 measured +296/+220/+203).
- The B801 builder did NOT read the artifact by name; the kit makes that the gate's first job (PRIORITY: Check 6 first).
- Ports 8950-8959 clear: `lsof` rc 1; word-boundary scan of non-`.pre-` SEAT kits of 10-26 and 10-27 printed no file (rc 1; control `888[0-9]` hit 10-27 kits, so the scan fires); `ls -d .tools/b809`, `.tools/wt-b809-base` absent (control `.tools/b514` lists). Pane `Datasec/HPSM-POC-G171` absent; live panes: G170, D37, R57, G169, tuesday, fleet-monitor.

## Facts re-measured (instrument; control)
- PR, head, mergeable, merge_commit_sha `1a7d1700`: `gh api -X GET pulls/222` 10:41. PR base sha reads `d415a3fe`; 2 commits; +10 -1; 1 file.
- Main `bf4a7bdd`: `git/ref/heads/main`; its push run `40420821396` had no conclusion yet; `d415a3fe` run `40383065653` success (baseline for log comparison).
- Blobs by `contents?ref=`: head `447c5b79`, `7b3f3c76` `447c5b79`, main `bf4a7bdd` `9ce335ce` (first attempt hit a zsh glob on unquoted `?`; re-ran quoted). `ci.yml` blob at head `0176b491`, 679 lines, equals the B719 base blob (no workflow hunk). CI step line numbers (165, 175, 252, 264, 274, 314, 348) read from the saved raw file by grep.
- Check-runs: 20 rows by `--jq`; no control beyond the count matching the builder's "20 of 20".
- Open PRs: #233 (`b800/...`) and #222.
- Model row: `model-routing.md` lines 109 (G2) and 111 (G-cap) by `grep -n`; `models_latest.json` line 23 `claude-sonnet-5-5`.
- Landing: `CLARIFICATIONS.md:138` printed ("PR #27 (B23) squash-merged head-pinned"), the only hit of `squash|match-head` over the project `CLAUDE.md` and `CLARIFICATIONS.md` (the hit is its own positive control).
- Dotnet: `.tools/dotnet` exists (`ls`); `dn.sh` header read: it sets PATH to `.tools/dotnet`, so a bare `dotnet` need not be on PATH; B719 and B801 STATUS record 10.0.402 via `dn.sh`. Not run by me.

## D-decisions (mine; override any)
- D1. Process is copied from the B719 kit by reference (the builder-gate precedent B719 did the same with B691), with explicit overrides: head, base = CURRENT main, ports, merge-commit properties (parents, 31 main paths, test file unchanged vs the old head), hygiene of BOTH commit messages, the #232 statement. The seat reads the B719 kit whole; it is not retyped here.
- D2. SQL Server by-name read from the trx artifact, the log for totals (same as B719's D2; here proven again: 0 hits).
- D3. Re-run scope: the first gate's class rows (Q, Q2, s1-s3, P3 at main and head, c0, cw-weak, c-fail), E, Wk3, s5, sweep; the B719 optional items (Wk1, Wk2, s4, L, H, H2, r1) are CUT by default because the test file is byte-identical to what B719 measured; L is re-run only if the gate wants to change Note B719-2. The whole Api project is run at main and at the head (two ~5-7 minute runs), because the base now differs (#232 tests).
- D4. B719 Notes 2-10 carry as Notes unless a gate measurement changes one. B719-1 is gone iff the three Pkcs-affected checks read success on this head (they do at 10:41; the gate re-reads).
- D5. Blocker "a path beyond the one" is judged on the branch's own delta, since the merge legitimately brings 31 main paths (auth, csproj among them); the tier-1 escalation list is likewise scoped to the branch's own delta. Without this the gate would STOP on main's own already-gated paths.
- D6. A Major is NO GO and, as round 2 of 2, the cap; the gate still writes fix-shapes in prose for Tuesday's ticket.

## Q-questions for Tuesday (each with a default)
- Q1. Stamp the kit now, or wait for main's push run `40420821396` (bf4a7bdd) to finish? Default: stamp now; the gate reads that run only if complete, and re-baselines if main moves again.
- Q2. Is the cut of B719's optional mutants (D3) acceptable for round 2? Default: yes (identical file bytes; the first gate measured them clean, 17 of 17 as predicted).
- Q3. Two HPSM-POC panes are live (G170 for B805/PR #233, D37 scope unknown to me). The kit names both as not-yours and relies on `dn.sh` waiting; confirm D37 is not a lane touching the test file or `Timing/`. Default: proceed; Check 8a lists open PR paths and would catch it only if D37 has a PR.
- Q4. Target verdict 2 h, hard stop 3 h after Step 0 (same as B719; B719 overran its target by 29 minutes on load). Default: accept, or lengthen to 2.5 h / 3.5 h if the machine is loaded at launch.

## UNMEASURED
- Whether `RequestTimingLogTests.cs` mentions UatOpen / Assessment:Environment (my one grep ran on an empty pipe after a glob error; the kit tells the gate to run it with a positive control).
- The trx contents (class rows by name, logged vs held ms) on this head: nobody has read the artifact.
- The 13 skipped names against main's log; whole-project SQLite totals at `bf4a7bdd` (main now includes #232's tests).
- Main's `bf4a7bdd` push-run result; the floor's green side on SQL Server; GitHub runner timing.
- The `Program.cs` hunk: I read the diff text (comment lines only); no build confirms it.
- No positive control for owner-name and non-ASCII greps on the kit.

## Outside-the-fences disclosure
- Read-only `gh api -X GET` calls under the project's `GH_CONFIG_DIR` (PR, compares, commit patches, contents, check-runs, runs, jobs, artifacts list, analyses, one shard job log saved to the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/5d4f3df6-7a7d-4042-a868-99d30aaa36b8/scratchpad/` with `ci.yml` raw copy), `lsof`, `tmux list-panes`, `ls`/`ls -d` of `!CODING/Datasec/HPSM-POC/.tools/` and `dotnet/` top level, reads of `dn.sh` header (first 30 lines), the three status files, the B719 kit and drafter report (head), `model-routing.md` grep, `models_latest.json` lines 20-26.
- I ran `ls` of the whole `.tools/` directory listing (names only) to check `b809` absence; I opened no file under any other seat's `.tools/**`. Two bash calls began with a stray `cd_unused=1` variable assignment (no `cd`). One hook advisory about case-sensitive grep was shown; the grep was a line-locator, not a count claim.
- Not touched: `decision_queue.sh`, `fleet/briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY trees, Jira (no JQL run), any hosted host, az/ssh/docker, mail/chat/Artifact/Docs tools.
