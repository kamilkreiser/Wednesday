STARTABLE: YES - the kit is drafted, every frozen text was dry-run on a copy of the head, `stamp_check.py` exits 0 (155 claims, 155 measured); it needs Tuesday's stamp and answers to Q1 to Q4 (three of them change the owned-path list the commission expected).

# B1774 DRAFTER REPORT | OXPd 2, round 2 of 2 of the CI skeleton (WP0.3), SEAT-X2

Drafted 2026-11-20, 14:01 to 14:30 AEDT (every clock from `date`). Read-only drafter; the newest Fable.
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1774_SEAT-X2_oxpd2-wp03-round2-secret-scan.md` (545 lines, 85011 bytes, sha256 starting `90b3d631f1da7427` as printed at 14:29:18, ASCII, 9 slot lines).
Sidecar: the same path plus `.measured` (155 lines, 0 TODO).
Scratch (everything the numbers below came from): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s297/d1774/` (963M; git-ignored by Tuesday's own `.gitignore:44`).

## BLUF
1. **The fix chosen: a second scan of every STORED file under a neutral name behind one plain first line.** No configuration file, no refusal of names, no change to R1. One new last step in the `secret-scan` job (52 lines, frozen as T1) exports every blob of the object store as `<object id>.txt` and scans that folder; the same shell function serves a planted repository first (six files, five of them skipped by the scanner under their own names, one of them present only in an earlier commit) and the job fails unless the neutral scan finds exactly 6.
2. **The dry run found a second hole the gate did not report.** gitleaks 8.30.1 also skips a file by its FIRST BYTES, whatever its name: a token in clear text after `%PDF`, `MZ`, the ELF magic, `PK 03 04` or the gzip magic is not found (5 rows of 5). A neutral name alone does not close that; the one plain first line does. And the history form (`gitleaks git`) misses files git shows as binary changes (2 rows).
3. **The table that proves it** (63 scratch repositories, one committed file each, the workflow's own four options, the function cut out of the candidate `ci.yml` by program): 61 token rows; found by name in the working tree 14, in the history 13; **found under a neutral name 59**. The gate's 24 names: by name 10 found and 14 not (the gate's own reading reproduced), neutral 24 of 24. The 2 not found are the scanner's own limits (a gzip stream, UTF-16 text), named in the README text and in a backlog line, never claimed as fixed. Both quiet rows stay quiet. One repository with 60 token files committed and then all removed: by name the working tree finds 0 and the history 12; neutral finds 58 of 60.
4. **The cheap items are all in and measured:** floor = count (53) held by a test; `RuntimeIdentifiers` in the root props (both publish legs and the locked restore hold, fault 2 does not return, a later project inherits); one guard test that kills the gate's surviving mutant; README, runbook and backlog texts frozen.
5. **Round 2 of 2 is made provable before the push:** eight frozen blocks with sha256, two job fingerprints the seat's edit must reproduce, the 63-row table as the acceptance check red first and green after, three mutants on the workflow and one on the guard, a local run of both changed steps exactly as the runner runs them, a pre-push ancestor check and a measured refusal text.
6. **What is NOT measured and cannot be before the seat pushes:** the new step on a Linux runner (bash 5, GNU sed, the Linux binary). The kit says what the seat does if the hosted run is red on a shell difference (fix forward, recompute the fingerprint in the same commit, name every changed line).

## The acceptance table (the kit carries all 63 rows; totals here)
| Set | Rows | Working tree by name | History by name | Neutral name + first line |
|---|---|---|---|---|
| The gate's names | 24 | 10 found, 14 not | 10 found | 24 found |
| Drafter's names: 6 by directory (one from a per-rule list), 8 by extension, 11 by exact name | 25 | 0 found | 0 found | 25 found |
| Drafter's content rows: NUL bytes, five first-byte kinds, PNG magic, random bytes, 96 MiB | 9 | 4 found | 3 found | 9 found |
| A ZIP with a stored member | 1 | 0 | 0 | found |
| The scanner's limits: gzip stream, UTF-16LE | 2 | 0 | 0 | 0 (stay open, said so) |
| Quiet (no token; plain name and skipped name) | 2 | quiet | quiet | quiet |
Instrument: `dry2.py` in scratch, log `logs/acceptance.log`, 25.6 s. Control that can fail: the quiet rows (a scan that fired on everything would read 1 there) and the by-name column (it must reproduce the gate's 14).
The scanner has no size limit unless an option sets one (96 MiB row found by name; R1 already forbids `--max-target-megabytes`).

## Files
| File | State |
|---|---|
| the kit | written with the Write tool, corrected with the Edit tool (10 edits); blocks T1 to T6C byte-equal to the files the dry runs used (program compare: 8 of 8) |
| the kit's `.measured` | skeleton by `stamp_check.py --init`, filled by `sidecar_fill.py` (temp file, `os.replace`); `stamp_check.py <kit>` rc 0 |
| this report | Write tool |
Nothing else was written outside scratch. Nothing was written under the project folder, its `.tools`, or its checkout (porcelain 0 before and after; `.tools/` still lists `b1764`, `dotnet`, `nuget-packages`).

## Facts re-measured, with instruments
| Fact | Instrument | Reading |
|---|---|---|
| Heads and pull requests | `gh api -X GET` under the OXPd_2 `GH_CONFIG_DIR` (account verified first: one account, active), 14:01:41 and 14:25:36 | `main` `7e1a01cf640f8abac89e7148322651be8e4bf15b`; `b1764/wp03-ci-skeleton` `a0f9bdcc1fecd897d2dc7adbbc10adecb170fc89`; 2 refs; ahead 1, behind 0, 24 files; pull requests 0. Equal to Tuesday's 13:39:51 read |
| The seat's checkout | git read verbs, `--no-optional-locks` | `HEAD` at the lane head, branch `b1764/wp03-ci-skeleton`, porcelain 0, 25 tracked paths; 36 blobs in its object store (26 reachable, 10 unreachable from round 1's staged mutants) |
| Scanner | `/opt/homebrew/bin/gitleaks version` | `8.30.1` (installed, the pinned version) |
| Scanner's built-in list | default config at tag `v8.30.1` by `gh api -X GET` (the gitleaks repository) | 3209 lines, 222 rules, 25 global path patterns, 3 more path lists inside rules |
| Rule tests at the head | `/usr/bin/grep -c -E '^[[:space:]]+def test_'`, column-1 count beside it | 22 + 26 = 48 (column 1: 0 and 0); suite `Ran 48 tests`, `OK` |
| After the round | the same, on the candidate | 23 + 26 + 4 = 53; `Ran 53 tests`, `OK` |
| The new step, as the runner runs it | `run_step.py` (`/bin/bash --noprofile --norc -e -o pipefail`, macOS bash 3.2) | `PLANTED-CONTROL neutral-scan: planted 6, found by name 1, found under a neutral name 6, rc 1`; `NEUTRAL-SCAN: stored files 26, files of this commit not among them 0`; `no leaks found`; rc 0 |
| The real repository under the neutral scan | `neutral.sh` with `git cat-file` only, output in scratch | 36 stored files, rc 0, `no leaks found` |
| Rules on the candidate | the head's own `repo_rules.py` | `RULES: clean (26 files)` (R1's line checks accept the new step) |
| dotnet, the move of `RuntimeIdentifiers` | the project's SDK `10.0.404`, own home and cache, one job at a time, load1 2.6 to 2.7 | relock: ONE lock file changes (the test project's, +24 lines). With `CI=true`: restore, build (0 warnings, 0 errors), test (total 1), both publishes (10 and 11 files), both guards clean, locked restore again: all rc 0, lock files byte-equal. Without `CI`: both publishes leave all three lock files byte-equal (`cmp` rc 0 three times). A fourth project with no list of its own inherits and publishes under `CI=true` rc 0 |
| Mutants | `mutants.py`, 11 scratch copies | every one RED in the cell the kit names (FACT 7 of the kit); the gate's surviving mutant now dies on the new guard case, `failures=1` |
| Order of the edits | `order.py` | head 48 OK; + T3 49 OK; + T4 `Ran 53`, `FAILED (failures=6)`, exactly T4's four cases; + T1 + T2 53 OK |
| Base-image line | the gate's saved hosted `linux` log (copy in scratch), line 267 | the gate's quote holds, digest `sha256:12b1135f...03586` |
| Fast-forward and refusal texts | `nonff.py` on a scratch bare repository | fast-forward rc 0 `   79b69a3..6634109  HEAD -> b1/x`; non-fast-forward rc 1 ` ! [rejected]        HEAD -> b1/x (fetch first)` |
| Kit pointers | `kit_check2.py` | 52 `file:line` pointers, 52 held; 63 table rows equal to the log; 9 slot lines; 0 non-ASCII |
| The kit under the scanner | `gitleaks dir` on a copy of the kit and its sidecar | rc 0; the planted value appears whole 0 times |

## Chain-step inputs (each produced by an earlier step or present at BASE)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit | Tuesday |
| 1 | origin refs; the checkout at the lane head; the Step-0 copy (frozen blocks) | BASE; Step 0 |
| 2 | gitleaks 8.30.1; the head's scan options | BASE (`ci.yml:113`, `:116`) |
| 3(a) | block T3; `test_release_guard.py` | Step 1; BASE |
| 3(b) | block T4 | Step 1 |
| 3(c) | blocks T1, T2; T4 in place (its helper prints the fingerprints) | Step 1; 3(b) |
| 3(d) | `ci.yml` after 3(c); the staged T4 | 3(c), 3(b) |
| 3(e) | the 63 repositories; the function in `ci.yml` | Step 2; 3(c) |
| 3(f) | staged `ci.yml`; the runner of 3(d) | 3(c), 3(d) |
| 4 | block T5; the SDK at `.tools/dotnet`; the package cache | Step 1; BASE |
| 4(e) | block T6; `README.md` | Step 1; BASE |
| 5 | all eight paths staged | Steps 3, 4 |
| 6 | the staged tree; origin at the lane head | Step 5; BASE |
| 7 | the pushed head and the hosted lines; blocks T7, T8 | Step 6; Step 1 |
Step 4(e) was added on the drafter's last read (the first draft named T6 in the frozen texts and in the owned paths but gave it no numbered step); the sidecar and `stamp_check` were re-run after it.

## Corrections to the commission
1. **Owned paths differ from the expected list in three places.** (a) `build/repo_rules.py` and `build/tests/test_repo_rules.py` are NOT touched: R1 need not change. (b) ONE new file, `build/tests/test_pipeline_controls.py`: the mutants "the planted control removed" and "the floor lowered" need a cell that goes RED, and nothing at the head could; this file is that cell. (c) `tests/Datasec.Suite.Core.Tests/packages.lock.json` changes (+24 lines), because the root props are inherited by the test project too. Eight paths in the repository in all.
2. **"Closes the base-image line" would be untrue.** The digest is now known, but the `FROM` line still names the tag. Default: the digest is written into backlog line 7 and the line stays open. Q4 offers the one-line pin.
3. **The verdict's recommendation was not taken as written.** Its "smallest" (refuse the 14 names) covers neither the 24 further names measured here, nor the first-byte skip, nor the history; its alternative (copy tracked files under a neutral name) "covers the working tree, not the history". Exporting the object store covers both.
4. **The gate's re-run instruction needs one sentence.** "Re-run `rules_probes.py` rows S4 to S38" will read 14 GOT PAST again unchanged: those rows scan a folder by its own names. The round-2 gate must probe through the workflow's function (the kit's D10; first line of the seat's FOR TUESDAY).
5. **The design copies under the project were re-copied at 14:01 today** (file times). E0.4 now sits at `03:72`, not `:69`; `02:138` still holds. The kit prints the new line. Whether that writer returns while the seat runs is S3's to say.
6. **The pull-request texts beside the verdict go stale in two places** after this round: `pr-body.md` line 20 (says a rule refusing those names is not built) and the count 48 (lines 6 and 13). Tuesday's to re-word.

## D-decisions written into the kit (each Tuesday's as coordinator, none the product owner's)
D1 neutral-name second scan. D2 one step in `ci.yml`, one shared function. D3 one new test file; R1 unchanged. D4 `FLOOR=53`, equality held by a test, moves in the same commit as a control. D5 root `Directory.Build.props`. D6 backlog line 7 stays open with the digest. D7 a second commit, fast-forward. D8 the hosted planted repository is committed under a throwaway identity inside the workflow text. D9 no Jira, no pull request, no setting. D10 the gate probes through the function.

## Questions for Tuesday (each with its default)
- Q1 shape of the fix: default neutral-name scan. Alternatives: refuse names (weaker, measured); private config copy (3209 lines, breaks R1).
- Q2 where the text lives: default one workflow step plus one new test file (8 paths). Alternative: the cases inside `test_repo_rules.py` (7 paths).
- Q3 where `RuntimeIdentifiers` lives: default root props (measured). Alternative `src/Directory.Build.props` (UNMEASURED).
- Q4 base image: default line stays open. Alternative: pin the `FROM` line now (ninth path, UNMEASURED, no local `docker`).
- Q5 floor: default the job needs at least `FLOOR`, a test needs equality.
- Q6 planted repository identity: default two commits under `planted-control` in the workflow text. Alternative: no commit (index only).
- Q7 the OUT list: default as commissioned. One more item in means a new frozen text and a new dry run.
- Q8 gate: default G1, told to probe through the function.
- Q9 pane: default `Datasec/OXPd2-X2`.
- Q10 windows: default READY at Step 0 + 150 minutes, push by + 100 (the drafter's whole dry run took under 30 minutes; the seat also waits on load gates and one hosted run).

## Recommended slot answers (the drafter's own measurements only; Tuesday writes what Tuesday read)
- S0: the drafter read the commission whole (24 lines) and the verdict whole (110 lines): round 2 was named by Tuesday after NO GO 1 of 2; the drafter found no word of the product owner on this lane after his word to start in the files it read (the project `CLAUDE.md`, the verdict, FOR-RECORDS, the round-1 STATUS). Clock: `@NOW@`.
- S2: the drafter read by API at 14:25:36: two refs, the two shas of the kit's FACT 1, 0 pull requests.
- S3: the drafter read at 14:25 to 14:27: checkout at the lane head, porcelain 0; 0 panes named with `OXPd2`; `.tools/` lists three names, none `b1774`; the SDK prints `10.0.404`; the six design files under the project carry the file time 14:01.
- S4: all ten defaults; Q1 to Q4 are the ones that move the owned-path list.
- S5: load averages at 14:27: 3.41 3.05 3.17 (`LC_ALL=C uptime`); the drafter left no process (`pgrep` for the project's dotnet path: 0).
- S6: no port; level fable; `brief_seat.sh:31` and `:33` as quoted in the kit.
- S7: READY = Step 0 + 150 minutes; the push by Step 0 + 100.
S1 and the last line are Tuesday's alone.

## UNMEASURED (carried in the kit as such)
- The new step on a GitHub Linux runner; the hosted stored-file count (DERIVED 34) and `3 commits scanned.` (DERIVED).
- The Windows leg with the root props (hosted only). `docker build`. A pull request and its checks.
- Whether the scanner skips first-byte kinds beyond the five tried (the first line makes the question moot for every kind that is judged at byte 0: DERIVED, not proven for all).
- The cost of one `git cat-file` process per stored file at scale (measured: 61 files in 0.4 s, 36 real files in under 1 s; no reading beyond that).
- Whether an ignore file in the job's working folder can hide a neutral-scan finding: one probe was run and was NOT conclusive (the drafter's fingerprint lines may have had the wrong form); a tracked ignore file is refused by R1 either way.
- `src/Directory.Build.props` (Q3) and the digest pin (Q4). A token split over two lines (relayed from the gate, not re-run).
- The ruleset: not re-read by API by the drafter (relayed from the gate's file).

## Outside the fences: disclosure
- **What ran, where, at what load.** Everything in the scratch folder above. Heavy jobs: the dotnet chain three times (14:10:45 to 14:11:04) and one publish in a second copy, one at a time, load1 2.6 to 2.7; a 96 MiB file twice. No lane holds the OXPd_2 project (0 panes). The project's SDK was EXECUTED from `.tools/dotnet` with the drafter's own `HOME`, `DOTNET_CLI_HOME`, `NUGET_PACKAGES` and `TMPDIR` in scratch; nothing was written under the project's `.tools`. No process left.
- **The package cache** is a COPY of the gate's (`/private/tmp/b1772-gate/nuget`, 431M); the restores needed nothing more that the drafter saw, but the restore logs were not searched for registry calls: whether `api.nuget.org` was contacted is UNMEASURED.
- **Scratch git repositories** (more than 120 by a `find` for `.git` folders, all under the git-ignored scratch folder) were made and committed with a throwaway identity by `git -c`; none is the project's. On the project's checkout only read verbs ran, including `cat-file --batch-all-objects` and `ls-files`.
- **GitHub calls:** all `gh api -X GET` under the OXPd_2 login: the OXPd_2 repository (refs, pulls, compare) and ONE file of the public gitleaks repository (its default configuration at the pinned tag). No Jira call. No HTTP to any hosted host otherwise.
- **Three commands were refused by Tuesday's hooks and re-written, none ran in a refused form:** a separator word starting with `=`; `git init` through a shell variable; `git symbolic-ref` on the project checkout (the hook lists it as a write verb; `rev-parse --abbrev-ref` was used, and the kit names that form).
- **A script that would have edited the kit by program was written and NOT run** (the rule says Write and Edit only); it is in scratch `_quarantine/` under a name that says so. The sidecar WAS filled by program, as the tool that creates it does.
- **The planted value.** The workflow text T1 holds the two halves round 1 already committed, on two lines, joined at run time; the kit holds the tail half once and the whole value 0 times (counted). Every dry-run token was random, built in memory by a program, asserted absent from every captured output.
- **The gate's logs and scripts** were copied into scratch at 14:01 before anything was quoted from them.
- The first name the drafter gave T4's fingerprint constant made the scanner fire; it was renamed before the kit was written, and the kit warns the seat (FACT in THE FIX, MEASURED).
