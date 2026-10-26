STARTABLE: YES

# B801 drafter report (SEAT-H44, HPSM-POC, PR #222 / HPSMPOC-354, bring the branch up to main)
Drafted Tue 27 Oct 2026 from 09:35 AEDT (clock from `date`; 09:49:03 at the port scan) by a Sonnet kit drafter. Kit: `2026-10-27_B801_SEAT-H44_hpsmpoc-222-bring-up-to-main.md`; 8 stamp-slot lines by `grep -c` (7 slots plus the last line), 0 at-sign placeholders, 0 non-ASCII bytes.

## BLUF
- One merge commit of main `d415a3fe172e3fe1e392c51e8c883f1a3d759990` into the existing branch (head `7b3f3c76`), a plain fast-forward push of the same ref, no content change (test file blob stays `447c5b79`), local Hosting filter plus the Auth filter as control, a scratch mutant Q on the merged tree, then a GET-only read of the PR's CI on the new head. Ends READY FOR QA with the new sha, or STOPPED.
- Route is MERGE, not rebase. The project has no written rule for updating an open PR branch (CLAUDE.md and CLARIFICATIONS grep found nothing relevant). The fleet-wide kit line is "never rebase, never force-push, never amend", the main ruleset's `non_fast_forward` is on `main` only, and landing is a head-pinned squash, so a merge commit on the branch never reaches main. A found rule that REQUIRES a rebase makes the seat STOP.
- B719's ONE Blocker (CI red, Pkcs pin) is addressed by the merge; B719-2..-10 are Notes, all left unchanged (a content edit would re-open every first-gate mutant). The kit prints the in/out table.

## Facts re-measured (instrument, control)
- Main `d415a3fe...`: `gh api -X GET git/ref/heads/main`. PR #222: head `7b3f3c76`, base `b069274c`, open, `blocked`, 1 commit, 1 file (`pulls/222`). Branch ref `b709/hpsmpoc-timing-rows-354` = `7b3f3c76` (`git/matching-refs/heads/b709`). Open PRs: #232 and #222 only.
- `compare 7b3f3c76...main`: `diverged`, ahead 9, behind 1, merge base `b069274c`. `compare b069274c...d415a3fe`: 31 paths, 9 commits. The exact test file name counts 0 (control: `PkcsInPackageTests.cs` counts 1; made-up name 0). `ci.yml` counts 0 (so CI line numbers are the old base's; control for that same list is the Pkcs name firing). The drafter did not run a merge or `merge-tree` (fenced).
- ci.yml at `d415a3fe` (679 lines) read at lines 14-18, 32, 86, 165, 175, 248-256, 274, 303, 314, 353: `on:` includes `pull_request`, so the push starts the PR run; Hosting namespace runs in the `api-assessment` SQL Server shard, the Auth namespace in `api-other-and-feedback`. Required contexts (5) from `branches/main/protection/required_status_checks`; `rules/branches/main` = `deletion,non_fast_forward,code_scanning,required_status_checks`.
- Namespaces: `RequestTimingLogTests` is `namespace HpsmPoc.Api.Tests.Hosting;`, `Auth/UatOpenTests.cs` is `HpsmPoc.Api.Tests.Auth` (raw reads, each printed its line). 14 files under `Hosting/` in the tree.
- Model: routing rows L6 (line 85), C1 (line 91), G2 (109), G-cap (111) by `sed -n`; `claude-sonnet-5-5` at `models_latest.json` line 23. `brief_seat.sh` line 24 reads `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`; launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Ports 8880-8889: `lsof -nP -iTCP:8880-8889 -sTCP:LISTEN` rc 1 (empty). Word-boundary scan of 95 non-`.pre-` SEAT kits of 26-27 Oct: 0 hits for `888x`; control `886x` hit 1 file (B799). Live panes: `tuesday`, `Datasec/HPSM-POC-G168`, `Datasec/NexusAI-M19`, `Datasec/MPS-G167`, `fleet-monitor`. No hits to report.
- Gate verdict line (B719 line 165): NO GO round 1 of 2 on class "assertions added to one existing Api test row plus one comment parenthesis, tests only".

## D-decisions (drafter's)
- D-1: merge commit, not rebase (above).
- D-2: no Note is fixed in this lane; "address in-scope findings" is read as "list each and say in or out". Any wish to fix one goes under FOR TUESDAY.
- D-3: the seat reads CI on the new head by `gh api -X GET` only; a red check ends STOPPED with one question (re-run is Tuesday's: no POST by the seat). READY needs the five required contexts, both SQL Server shards, the aggregator and CodeQL green.
- D-4: one scratch mutant Q on the merged tree (a control that can fail), in a third detached worktree, never pushed.
- D-5: the sibling kit B800 (H43, 8870-8879) was not on disk when drafted; the partition names it from the lane text and says its ports are unmeasured.

## Q-questions for Tuesday (each with a default)
- Q-1: Does Tuesday accept a merge of main into the PR branch (one extra commit, squash lands it anyway)? Default: YES. Also note the #221 round-2 builder kit says "never merge" about a content round; this kit overrides that for this lane in writing.
- Q-2: If #232 lands before launch, merge that main too? Default: YES (the main-moved rule stops only if the new main touches the test file, `Timing/**`, `Identity/Caller.cs` or `ci.yml`).
- Q-3: Is the round-2 gate charged as round 2 of 2 on the class, or does Tuesday follow B719's own recommendation and not charge the external-cause NO GO? Default: kit says "NO GO 1 of 2"; the charge is Tuesday's call.
- Q-4: If a web e2e shard flakes on the new head (it failed once on a main push), should the seat wait or stop? Default: STOP with one question; re-run is Tuesday's.

## UNMEASURED
No clone, fetch, worktree, merge or dotnet ran; no `merge-tree`. That the merge is textually clean (inferred from disjoint file lists and B719's own read of GitHub's merge). The `lsof` positive control for 8880-8889 (the seat takes its own). B800's port block. Local green of the merged tree, runner behaviour with the raised pin, and the SQL Server rows (the seat cannot run SQL Server: every local row is UNMEASURED-ON-SQLSERVER). Whether `dn.sh`'s `B=` line is its only seat-number line.

## Outside-the-fences disclosure
I wrote only the two files named. Reads: DRAFTER_RULES, the sweep, B719 STATUS, the B709 kit and STATUS tail, B719 kit head, B799 kit (port and partition lines), B709 drafter report, `model-routing.md` lines 80-115, `models_latest.json` (grep), the project's CLAUDE.md and CLARIFICATIONS (grep). `gh api -X GET` only under the project's `GH_CONFIG_DIR` (ref, pulls, matching-refs, compare, contents, trees, protection, rules). Scratch copies of the compare file list and `ci.yml` in the session scratchpad. One slip: my first `git ls-remote git@github.com:...` used a guessed URL and failed with "Repository not found"; nothing was read or written. `lsof`, `tmux list-panes`, `uptime`, `date`, `ls` and `sed` were the other local commands. No bind, no az, ssh, docker, Jira, `decision_queue.sh`, Artifact or Docs call.
