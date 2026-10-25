STARTABLE: YES

# B722 DRAFTER REPORT: MPS PR #119 gate kit (SEAT-G138, tier 1, Opus, row G1)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B722_SEAT-G138_mps-119-pkcs-pin-gate-tier1.md` (106 lines). Drafted 09:44 to about 10:0x AEDT 26 Oct from DRAFTER_RULES.md (read whole), the B715 template (read whole), the B720 builder STATUS (153 lines, whole) and the B720 builder kit (whole).

## BLUF
The kit is startable. It follows the B715 shape (STATUS-file channel, fact marks, REFUSE AT ONCE, STEP 1 and PINS, CHECKS, GRADING, VERDICT, LANDING, LOAD, HOLDS, NOT TESTED, SELF-CHECK) and settles your ten items as C1 to C10, plus C11 (secrets, provenance, process, Jira). Stamp: the unstamped copy reads 8 four-underscore lines (7 slots and the last line); nothing was filled. Ports 9970-9979 are free. The one thing that needs your eye before launch is the C10 finding below: a re-run of #117's and #118's `dotnet` check may not pick the fix up.

## Facts re-measured (instrument, control)
- Refs, `git --no-optional-locks ls-remote` (shared repo, read only): main `1ac8ab8a`; `refs/pull/119/head` = branch `b720/...` = `66f43cb6...`; `refs/pull/119/merge` = `8cab258d`; #117 head `6e34f07a`; #118 head `39e51272`. Control: `refs/heads/b720*` lists the builder branch.
- `gh api -X GET` under the project `GH_CONFIG_DIR`: PR #119 open, not draft, 1 commit, 1 file, +2 -1, `mergeable` true / `blocked`. `commits/8cab258d`: parents `1ac8ab8a`, `66f43cb6`, tree `58619d61...` = the head commit's tree (so the merge tree equals the head tree). `compare` ahead 1 behind 0, 1 file.
- Diff by raw GET of the csproj at base and head plus `diff`: exactly line 28 `10.0.13` to `10.0.14` and one added comment line (26). `grep -c -F` counts head/base for 7 strings (control `zzz-no-such-string-7f3a` 0/0); non-ASCII 0; sizes 2119 and 1982.
- Advisories, `gh api -X GET advisories/<id>`: both GHSA-2fmv-rv2c-59x7 (CVE-2026-70162, medium) and GHSA-846f-f764-76mx (CVE-2026-84008, high) vulnerable `>= 10.0.0, <= 10.0.12`, first patched 10.0.13. The package list returns 3 ids (the third is a 2023 7.x/6.x one). CVE numbers in the csproj comment match. 10.0.14 clears the floor by reading; the kit makes the gate prove it by program with a firing control (pin 10.0.12 must read IN RANGE).
- NuGet, `curl`: flat-container index lists `10.0.14` (24 x.y entries for 10.x, last one 10.0.14; 151 total); `HEAD` of the 10.0.14 `.nupkg` 200; control 10.0.99 `.nupkg` 404. `listed` and file-version equality left UNMEASURED (the kit's C6). My registration leaf guess returned 404, so I did not claim it.
- Check-runs at the head, `check-runs`: 8 listed, CodeQL umbrella neutral, Analyze python/actions success, dotnet/web/python/csharp/javascript-typescript in_progress. `code-scanning/analyses`: 2 of 4 so far (python, actions); main has 4 of 4. Alerts open: 0 at head, merge, main. **The alerts zero has no positive control**: the same GET on `refs/pull/999/head` also returned `[]`; the kit says so and uses 4 of 4 analyses as the control.
- Rules: `rules/branches/main` code_scanning thresholds `errors` and `high_or_higher`, required_status_checks empty.
- `ci.yml` at main (raw GET): dotnet job as the template; `global.json` 10.0.100 / latestFeature; `Directory.Build.props` TreatWarningsAsErrors true.
- Guard test at the head (raw GET): publish uses `DOTNET_HOST_PATH` and `--no-build`; the B160 row's four assertions at lines 75, 78, 83, 85.
- Ports: `lsof -nP -iTCP:9970-9979 -sTCP:LISTEN` empty rc 1; bind control (python on 9970) printed 2 lines while bound, rc 1 after free. Word-boundary scan of non-`.pre-` SEAT kits of 25 and 26 Oct: 8 hits, all 25 Oct, none live (B646, B647, B648, B650, B659, B695, B696, B698; their panes are not in the list); zero hits in B715 to B721; control pattern on "x 9975 y" reads 1. Hits are reported in the kit.
- Panes (`tmux list-panes -a`): no `Datasec/MPS-G138`, no `MPS-M30`; live MPS: `MPS-G135`, `MPS-M29`. Heavy slots: 1 held (B715), 2 held (B717), 3 absent. `.tools/b722` and `wt-b722-*` absent (control: `.tools/b715`, `.tools/b717` list).
- Model: `models_latest.json` line 17 `claude-opus-5-5`; routing rows G1 `:108`, G-cap `:111`, C2 `:92` (`grep -n -i`, control with a no-match pattern 0).
- Round-count frame: first lines of 248 `*_STATUS.md` matching `pkcs|B160`: 4 hits (B160, B98, B161 "GO WITH NOTES", B720); none NO GO; control B720's first line matches. The class NO GO 0 of 2 is the B720 stamp's own ruling.
- #118's red job log (`121294539543`): runtime 10.0.14, SDK 10.0.403, checked out merge `19759df` (parents `f5a27af0`, `39e51272`). #117's `dotnet` check: success 2026-10-25 11:59-12:05Z on merge `d644c083` (parents `110ebecd`, `6e34f07a`).

## D-decisions (mine; override at the stamp)
- D1. Tier 1, Opus, BRIEF_SEAT_LEVEL=opus inside the quotes, row G1 as you directed.
- D2. Two toolchains plus a control: (A) 10.0.403 seat-local, (B) the SDK the PR's own CI log shows if it differs, (C) the project's 10.0.401 as the old-SDK control. The kit does not assume 403 for the PR's CI; the SDK floats with `latestFeature`.
- D3. C4 gives the builder's P1 to P5 plus c0 to c3 and cw-weak, and my own Q1 to Q7 plus three seeded edits. Two of mine reach assertions the builder's mutants never reach: Q6 (pin 10.0.12, audit off, under 10.0.401) forces the line-78 `>= 10.0.13` assertion. Lines 83 and 85 are likely UNPINNED, graded Minor.
- D4. Advisory floor graded Major (as you directed) for a pin below a fixed version; vulnerable-at-head-only Major; 10.0.14 not published or file version below the framework's Blocker.
- D5. C10 names the re-runs by check-run id and states a predicate to check, not a command (see Q1).
- D6. Hard stop as the template: target verdict 150 minutes, hard stop 4 hours, both absolute at Step 0.
- D7. Added an XML-wellformedness and `--`-in-comment check on the added line (an XML comment may not contain `--`), with controls.
- D8. Landing line quotes CLARIFICATIONS:809; the PR body emoji line and the `B160` word are a Note (not in a one-commit squash with COMMIT_MESSAGES).

## Q-questions for Tuesday (each with my recommended answer)
- Q1. After this PR lands, will a plain re-run of #118's and #117's `dotnet` check carry the fix? Both PRs' merge refs are stale (`refs/pull/118/merge` first parent `f5a27af0`, `refs/pull/117/merge` first parent `110ebecd`, neither contains the new main). GitHub's documented behaviour (not measured by me) is that a re-run reuses the original run's commit, so it would be red again for #118 and, on today's runner, probably red for #117 too (its green is stale: old runner SDK, old pin). The kit names the checks (`dotnet (build Release, 0 warnings; test)` on both, ids in C10), states the log line to check (`HEAD is now at ... Merge <head> into <base>` with base a descendant of the squash) and says refreshing a merge ref is yours, with no push to either builder branch. Recommended: accept the kit as written; plan to obtain a recomputed merge ref on each (not a push) before relying on the re-run.
- Q2. Q-1 (scratch csproj variants and a scratch copy of the guard test in `.tools/wt-b722-mut`, never committed, each restored byte-equal). Recommended: YES (C4 needs it).
- Q3. Ports 9970-9979 are free now, but eight 25 Oct kits mention the block (the Composer lanes J13, J17, G109, G129, G110 and an MPS gate G127 among them), none live. Recommended: assign 9970-9979 as asked; the gate listens on nothing anyway.
- Q4. Heavy slots: 1 and 2 are held by B715 and B717, slot 3 is free, load1 was 9.5 to 10.4 at 09:45. Recommended: launch with `launch_when_cool` as usual; the gate waits on load itself.
- Q5. Should C10 include an optional gate-side proof of the stale-green on #117 (build its merge tree under 10.0.403, one narrow B160 run)? I wrote it as "if time allows". Recommended: leave optional.

## UNMEASURED
Everything runtime: file versions, red/green cells, mutants, suite counts and times, the `listed` flag and the signature of 10.0.14, whether `dotnet list package --vulnerable` reaches the feed, the SDK the PR's own CI installed (its job is in progress), and the re-run behaviour of GitHub Actions (documented behaviour only). I ran no build, test, mutant, clone, fetch or dotnet.

## Outside-the-fences disclosure
- Wrote only the two output files.
- Read-only outside them: `gh api -X GET` (project config dir, including `advisories/...` which is GitHub's public database), `git --no-optional-locks ls-remote` on the shared repo, two `curl` GETs of NuGet's public flat-container and a `HEAD` of two `.nupkg` URLs, one `curl` GET to a registration URL (404), `lsof` plus one transient loopback bind on 127.0.0.1:9970 as the control, `tmux list-panes`, `uptime`, `ls`, `sed`, `grep`. I read the B715 STATUS first lines and last lines and the B717 STATUS last line (the project's `Briefs/`, which kits allow) to see live-seat state, and listed `Briefs/` file names. I wrote three scratch files in the session scratchpad (the head and base csproj copies and one control text file). No Jira read, no decision-queue use, no Artifact, Docs, mail, chat or publish tool, no HTTP to any MPS host, no `cd`.
- One hook advisory fired (case-sensitive grep), and two of my greps were case-sensitive by accident (the port scan and a name check); each was paired with a positive control or was only a presence check on a file I wrote.
