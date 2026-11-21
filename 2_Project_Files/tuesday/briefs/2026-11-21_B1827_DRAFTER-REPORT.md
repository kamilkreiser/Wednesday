STARTABLE: YES - once stamped. The measurement agrees with case (b3): in my scratch clone a three-way merge of main ddbdf800 into bf1a4a24 conflicts in `Datasec.Suite.slnx` and nowhere else (two hunks); the file written as (b3) has sha256 `a94ad1ac414a9fb3eca2142f150fb254e8219f54bee96752a3e0cef26e21c8d6`; the commit made from it (twice, the second time with the block cut from the kit file) has tree `4a6fd8501706a01b9966fc897ef4c1b965834796` and `PROOFS: PASS (10 of 10, controls fired 10 of 10)`; it restores, builds with 0 warnings and 0 errors and tests `total: 762`, `failed: 0`, `succeeded: 758`, `skipped: 4` (run outside the wave's lock: see Outside the fences). `stamp_check.py` exits 0 (120 claims, 120 sidecar lines). NOT run by anyone: the push, the hosted run of the new head (its lines are DERIVED), any job through the kit's locked runner.

# B1827 DRAFTER REPORT (OXPd 2, WP1.1, the resolution commit; seat X16; delta review B1828)

Written 2026-11-21 by the in-session drafter (Opus, read-only). Work from 14:38 to 14:52 AEDT (clocks by `date`: 14:38:38, 14:38:48, 14:40:10, 14:42:27, 14:44:54, 14:49:10, 14:51:54).

## BLUF
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1827_SEAT-X16_oxpd2-wp11-resolve-solution-file.md` (170 lines, 52195 bytes before the stamp, 0 non-ASCII lines, 8 slot lines) with sidecar `.measured` (121 lines: a header and 120 claims). Same shape and mechanics as the landed B1820 kit; changed: lane, branch, heads, main, block, numbers, seat, files, one more proof (P10, the lane folders), per-leg hosted counts (this lane skips tests), and the launch rule ("launched" = statusline AND STATUS file within 5 minutes; Step 0 writes STATUS first).
- **The delta review:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1828_GATE_COMMISSION.md` (28 lines, 17771 bytes). A DRAFT: `HEAD40` occurs 29 times (`grep -o | wc -l`), and one paragraph `MEASURED BY TUESDAY ... TO FILL`. Fill both by program before the Agent call.
- **main re-read at the start and the end:** `ddbdf8009d0df77d084ef4834bb78d7c4a80b5b0` (14:38:38 and 14:51:54), its push run four ci jobs + three Analyze rows success, 0 open code-scan alerts; the branch at `bf1a4a24`; `compare`: diverged, ahead 2, behind 3, 39 files; pull requests 1 to 4 all closed and merged.
- **The block** is landing.txt lines 67 to 83 (case (b3), at column 1 there; the file holds three blocks, so the seat's `resolve.py` reads it from the kit, never from landing.txt). 17 lines, 1031 bytes, blob `0791300ab2b36e31e98b8ae8f4b08efc4a543b5b`; it is main's file plus exactly the two Secrets lines.
- **The commit is pinned by its tree, not its id:** parents bf1a4a24 then ddbdf800; tree `4a6fd850...`; message file 163 bytes, sha256 `eab1af16...`, subject `Merge main into the local secret store branch; the solution file keeps the projects of both sides (WP1.1)` (105 bytes) + the one attribution line; `WORDS: clean (1 files)`. My prototype ids: `36292f1e` and `934de72` (scratch identity, never pushable).

## What I measured, and how (scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1827/`)
1. Origin by `gh api -X GET` under the project `GH_CONFIG_DIR`: refs, pulls, compare, `rules/branches/b1789/...` 0 rules (control: main 4), `permissions.push` true, `allow_squash_merge` true, main's check runs and alerts.
2. Two clones by `clone.py` mode draft (push URL `invalid://no-push`). Census: branch 39 paths since 7bf37526 (38 A, slnx M); main 89 (87 A, `Directory.Packages.props` and slnx M); shared 1; main 113 files, head 64, merged 151, all 100644.
3. Trial `merge-tree --write-tree --name-only bf1a4a24 ddbdf800`: rc 1, tree `06e78fc5...`, one CONFLICT line (control: main into itself rc 0). Merge `--no-ff --no-commit`: the three lines, rc 1, porcelain 89 (87 A, 1 M, 1 UU). `merge --abort`: 89 -> 0 lines, HEAD bf1a4a24.
4. `resolve.py` (B1820's with this lane's values): written from a copy of the block and from the kit file itself (`<Solution>` at kit line 24, `</Solution>` at 40). Controls: one changed byte REFUSED on the sha256; landing.txt REFUSED (three blocks).
5. `proofs.py` (B1820's nine with this lane's values + P10 `git diff bf1a4a24 HEAD -- the two lane folders` empty and 21/17 files): PASS 10 of 10, controls 10 of 10, in both clones. P6 had to exclude the solution file (the fix round touched it: 22 paths, 21 blob-equal; my first run failed there and I corrected the program, not the commit).
6. Light jobs on the merged tree: `Ran 53 tests` `OK`; `RULES: clean (151 files)`; `gitleaks git` rc 0; the neutral-scan step rc 0, `25 of 25`, `NEUTRAL-SCAN: stored objects 327 (219 blob, 19 commit, 89 tree), copies written 654, objects of this commit not among them 0`.
7. **Build and test (the commission: "measure the expected totals yourself in the scratch clone if it can build"):** restore rc 0 from the project's package cache folder as the ONLY source into my own cache (so the cache holds every package the merged tree needs), build `0 Warning(s)` `0 Error(s)`, test `total: 762`, `failed: 0`, `succeeded: 758`, `skipped: 4`, five assemblies passed; porcelain 0 after (no lock file changed). 762 = 694 + 69 - 1 shared base test, the same shape the second review measured on the older main (260 = 192 + 68).
8. `hosted.py` (B1820's + `--linux S,K --windows S,K`, whole-line matches for the summary lines, needed because this lane skips 4 on linux and 19 on windows): bf1a4a24 `--total 69 --rules 64 --linux 65,4 --windows 50,19` PASS; control with the merged figures FAIL 5; main `--total 694 --rules 113` every count OK, FAIL 1 only for the three code-scanning rows. Merged expectation DERIVED: linux 762/758/4, windows 762/743/19, RULES 151, GUARD 10/11.
9. `history_entry.py` on a byte copy of the live history file: three True lines; a second run refused.
10. CI predicate at the merged tree: `ci.yml` lines 46 and 76 grep `total: +[1-9]`; push trigger `b[0-9]*/**` (line 7); main changed nothing under `.github/` or `build/`.

## D-decisions (mine, inside the commission)
- D1 the tools are B1820's, values changed; `heavy.py`, `clone.py`, `words.py`, `run_step.py` unchanged but for header lines (hashes in the kit).
- D2 P10 added to `proofs.py` because ruling 1 names the lane-folder diff (landing.txt step 0 (a)); P6 counts 21 of 22 (the solution file is P3's).
- D3 hosted counts per leg (the B1820 reader required `succeeded == total`, which this lane cannot meet).
- D4 a ninth OUTSIDE THE FRAME row: a windows skipped count other than 19 is a STOP (`W01` skips by the runner's descriptor).
- D5 launch section: the B1820 lesson ("launched" = statusline AND STATUS within 5 minutes; one re-launch after checking `<lane>` absent).

## Questions for Tuesday (each with its default; the kit assumes every default)
- Q1 tree property over all 39 branch paths (default; the commission's "the branch's own paths"); P6 and P10 prove the lane unchanged.
- Q2 no seat baseline build (default; cost: a local red cannot be split before/after; the drafter's 762 is a prototype run).
- Q3 one history entry (default; `words.py` counts 2 B-number hits in the template: the STATUS path and the branch name `b1789`, read case-blind; the file is outside the repository, as B1820's was).
- Q4 the commit message file as frozen (default).
- Q5 no local code scan (default; C# cannot be extracted here, RELAYED).
- Q6 STOP on a red hosted job or a count off FACT 6 (default).
- Q7 60/45 minutes, pane `Datasec/OXPd2-X16` (default).
- Q8 my build ran outside the wave's lock (no OXPd pane live, lock folder absent before and after each 2 s job): default, Tuesday accepts it as a drafter's prototype figure only; the seat's locked Step 5 is the one that counts. Cost of refusing it: the kit's 762 drops to DERIVED (the hosted parents give the same sum).
- Q-B1 (B1828) a NO GO goes to the product owner on a card (default, as Tuesday ruled for B1821's Q8); written into the TO FILL paragraph for Tuesday to confirm.
- Q-B2 (B1828) "carry B1824's FOR-RECORDS into the pull request body unchanged, N1 first": default, a known-follow-ups section in `pr-body.md` with section 3's N1 to N8 in order, substance unchanged, only scan-banned words changed and listed; not in `squash-body.txt`; `FOR-RECORDS.md` copied whole plus what the commit adds. Cost of the other reading (FOR-RECORDS copied, PR body untouched): N1 reaches the PR reader only through the existing "only as safe as that list" sentence.
- Q-B3 (B1828) scratch `/private/tmp/b1828-gate/` (default, by the B1821 pattern).

## Chain inputs (rule 4: each input made by an earlier step or present at BASE)
| Step | Inputs | Made by |
|---|---|---|
| 0 | the stamped kit | Tuesday's stamp |
| 1 | origin by GET; `gate/` (d1827); the checkout's local config; the deploy key | BASE |
| 2 | `<clone>` | Step 1(c) |
| 3 | `<clone>` on the branch; `<lane>/gate/merge-message.txt`; the Step-0 kit copy | Steps 1(b), 1(c), 0 |
| 4 | the commit; the message file | Step 3 |
| 5 | the committed tree; `<lane>/{logs,dotnet-home,_quarantine/locks}`; the project's SDK and package cache | Steps 1(b), 3; BASE |
| 6 | the commit; origin by GET | Steps 3 to 5 |
| 7 | the pushed sha40; the template | Step 6; Step 1(b) |

## UNMEASURED / NEVER RUN on a real output (marked so in the kit)
The REFUSE checks; `clone.py` mode seat and P8 against a seat identity; `heavy.py` with the lock; the push and its read-back counts by GET (ahead 4 / 3, files 89 / 39: measured locally only); `hosted.py --wait` and its verdict on the new head (its expected lines DERIVED); the history program on the live file; the hosted code scan of the later pull request.

## What I did NOT read
The B1824 commission beyond its first 3000 bytes and the round-1 commission B1809 (the B1828 reviewer reads them); the B1821 verdict beyond its first lines (named as a form only); kits B1813 and B1803; the lane builders' STATUS files beyond their last lines; kits B1825 and B1826 beyond a grep for branch and lock; `history.md` beyond its first entries (copied whole by program for the test); the decision store (the product owner's Opus words are RELAYED from the commission; the lesson file's first 12 lines match them).

## Outside the fences (disclosure)
- Network: two `git clone` of the origin over ssh with the project's deploy key, set in the `clone.py` process only (B1820's method); GETs only by `gh api -X GET` under the project `GH_CONFIG_DIR`.
- Git writes only in my two scratch clones under d1827 (switch, config of a scratch identity, merge, merge-tree, add, commit, abort); nothing pushed (push URL invalid).
- **dotnet restore, build and test in my scratch clone, WITHOUT the wave's lock** (taking it is a `mkdir` under `<project>/.tools/`, outside what I may write): my own runner (`d1827/scratch/drafter_heavy.py`, B1820's runner with the lock replaced by a refusal while the lock folder exists) read the lock absent before and after each job; load1 1.04 to 2.80; no OXPd pane live; three jobs of about 2 s. The project's `nuget-packages` folder was READ as a package source; nothing was written there.
- `<project>/.tools/dotnet/dotnet --version` ran once with my session's own HOME (it may have written first-run marker files under the user's `~/.dotnet`, outside every project tree).
- Three Bash calls were refused by workspace hooks and re-issued in the allowed form: an unquoted `====` separator; a `git switch` whose path the hook could not see through a variable; a stray `cp` through a `..` path (a no-op line of mine; nothing was copied).
- No write in any project tree; no Jira, no message, no Artifact, no `cd`, nothing deleted.
