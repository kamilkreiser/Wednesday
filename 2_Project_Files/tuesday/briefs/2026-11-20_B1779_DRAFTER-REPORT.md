STARTABLE: YES - once Stamp slot S0 reads `ruled a` (the kit refuses itself otherwise). The kit is whole, its four code blocks are byte-equal to the files the dry run used, `stamp_check.py` exits 0 (157 of 157 claims), and the candidate step ran green as a runner runs it on a committed copy of the head. Nothing of it has run on a GitHub runner.

# B1779 DRAFTER REPORT: OXPd 2, round 3 of the CI skeleton (SEAT-X3), a DRAFT

Drafted 2026-11-20, 15:39 to 16:04 AEDT (clocks by `date`), by a read-only drafter. Outputs:
- the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1779_SEAT-X3_oxpd2-wp03-round3-scan-every-object.md` (335 lines, sha256 `ef3fefcd347c6c46abea1cf9e05e00672180ba5af612a66226c873b089af4ee9` at 16:03:57, 9 unfilled stamp lines, ASCII, no tab);
- its sidecar `...md.measured` (157 claim lines and 12 fact-tag lines);
- this report.
Scratch (everything the kit quotes was copied or built here): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s297/d1779/` (799M).

## BLUF
- **The export chosen: every object of the object store, printed with `git cat-file -p`, written TWICE** under a neutral name: once behind one plain first line, once behind a plain block of 43008 bytes. One step, the same one as round 2, renamed; 61 lines replace 52. It starts from the gate's candidate and differs from it in three measured ways (below).
- **It closes the Major and more, with 0 rows lost.** Through the workflow's own function, on the gate's 108 probe repositories: 80 found before, 92 after, the gate's own two numbers; the 12 gained are G01 G02 G04 G05 G06 G08 G09 G12 G27 G28 G29 G30. On my own 17 token rows: 2 before, 15 after; the 2 that stay are named limits (a token in a branch name and in a lightweight tag name: ref names are not objects).
- **The planted control now fails unless a token is found in 11 places**, counted exactly: 25 findings. Dropping any one kind of object changes the count (files only 13, no commits 23, no tags 23, no folder listings 17, no second copy 12): each is rc 1 in the step.
- **Both conditional items are IN, each one small edit in the same step, each proven:** the read cut (the second copy; the plant holds a token across byte 125000 of the first copy, found only in the second) and the root ignore file (the step's first line fails when the checkout holds one; without that line the hole reproduces: rc 0, `no leaks found`).
- **Three things Tuesday should know before the stamp:** (1) the scanner cuts far more often than the verdict says (Corrections 2); (2) the second copy also closes the three byte marks of finding 3, which the commission put OUT: the kit writes nothing for it and the README claims nothing (Corrections 3, Q on it below); (3) from this commit on every commit MESSAGE and file NAME of every branch on the origin goes through the scanner with no ignore mechanism.
- The fingerprint of the `secret-scan` job changes to `7ef39469abc255a75ff51f9c5acf3a0134a505eb343d8181427dcb0022814544` (computed by the test file's own `job_sha256` on the candidate). The seat places it from a frozen one-line block and must recompute it and find it equal.

## The export, and the table that proves it
Instrument: `acc3.py --big` and `acc3b.py` in scratch; gitleaks 8.30.1 with the workflow's four options; each function cut out of its `ci.yml` by program (round 2's from the head, lines 119 to 127; round 3's from the candidate, lines 120 to 128); 1 = found. 508 captured outputs searched for the token pattern: 0 hits.

| Row | Plants | by name (tree, history) | round-2 function | round-3 function |
|---|---|---|---|---|
| D01 | commit subject | 0, 0 | 0 | 1 |
| D02 | commit body, third paragraph | 0, 0 | 0 | 1 |
| D03 | author name of a commit | 0, 0 | 0 | 1 |
| D04 | committer e-mail of a commit | 0, 0 | 0 | 1 |
| D05 | annotated tag message | 0, 0 | 0 | 1 |
| D06 | tagger name | 0, 0 | 0 | 1 |
| D07 | file name | 0, 0 | 0 | 1 |
| D08 | folder name, two levels down | 0, 0 | 0 | 1 |
| D09 | symbolic link target | 0, 1 | 1 | 1 |
| D10 | path of a submodule entry | 0, 0 | 0 | 1 |
| D11 | a file name a later commit renamed | 0, 0 | 0 | 1 |
| D12 | no blank line, token across byte 125000 of the first copy | 0, 0 | 0 | 1 |
| D13 | the same, across the first copy's second cut (153672) | 0, 0 | 0 | 1 |
| D14 | the same, across the first cut of the second copy | 0, 0 | 1 | 1 |
| D15 | commit message on another branch | 0, 0 | 0 | 1 |
| D16 | LIMIT: lightweight tag NAME | 0, 0 | 0 | 0 |
| D17 | LIMIT: branch NAME | 0, 0 | 0 | 0 |
| Q11 | quiet: names, a message, an author and a tag made of the scanner's key words | 0, 0 | 0 | 0 |
| D18 to D20 | `DICM`, `ustar`, `CD001` placed where ROUND 3's first copy is skipped, under skipped names | 0, 0 | 1 | 1 (first copy alone 0, second copy alone 1) |

The earlier tables through both functions: round 2's 63 rows: 59 and 59, the same rows, none differs (not found A60, A61; both quiet rows quiet). The gate's G01 to G44: 22 and 34. All 108 of the gate's rows: my by-name columns and round-2 column equal the gate's own log (0 rows differ). Seen by no pass after round 3: A60 A61 G17 to G23 G25 (compressed content, UTF-16 and UTF-32, a token split over two lines), G44 (a rule keyed on a file name, under a skipped folder), D16 D17.

Where it differs from the gate's candidate, and why:
1. **Block of 43008 bytes, not 35000.** The scanner's cuts in a file with no blank line are at byte 125000 and then about every 28672 bytes (measured: a 9000-line file, one token per line, loses lines at 124981, 153651, 182321 and so on). 43008 is one and a half of that step, so the two copies' cuts are about 14336 bytes apart (measured: 0 lines lost by both copies, nearest two losses 305 lines apart). With 35000 the nearest are 134 lines (6298 bytes) apart: also 0 lost by both, a smaller margin.
2. **The second copy is the first copy behind the block** (`cat`), not a second `git` call.
3. **The first line reads `stored object <id>`** (55 bytes; round 2's was 53).

## The files
In the repository, 3 paths, each as a frozen block: `.github/workflows/ci.yml` (T1: 61 lines replace lines 117 to 168; 199 lines after; numstat 22 and 13), `build/tests/test_pipeline_controls.py` (T2A: line 23, the fingerprint; T2B: lines 92 to 97, the fourth case's list, 9 lines; 119 lines after, still 4 cases, `FLOOR` stays 53; numstat 6 and 3), `README.md` (T3: lines 72 and 73; numstat 2 and 2). Outside it: `BACKLOG.md` (T4A owed line 9 ticked; T4B owed line 15; T4C owed line 16; 131 lines before and after), `SETUP_RUNBOOK.md` (T5A to T5E: lines 14, 50, 80, 86, 87; lines 21, 60, 66 by property), one prepended history entry. No dotnet, no lock file, no new file, no new test case, no new job.

Simulation of the seat (`sim_seat.py`): the blocks extracted from the KIT, applied at the line numbers the kit names, give three files BYTE-EQUAL to the committed candidate; the BACKLOG changes exactly lines 55, 57, 58, 93, 99, 100; the runbook exactly lines 14, 50, 80, 86, 87.

## Facts re-measured, with instruments
| Fact | Instrument | Reading |
|---|---|---|
| The heads | `gh api -X GET` under the OXPd_2 `GH_CONFIG_DIR` (account compared with `hosts.yml` in-process), 15:42:03 and 16:02:06 | `main` `7e1a01cf640f8abac89e7148322651be8e4bf15b`; the branch `e0ddd0dc8518f97ceba09759c5c0b9e987d872e9`; 2 refs; ahead 2, behind 0, 25 files; pull requests 0; tags 0; 4 check runs `completed` `success`. Equal to Tuesday's 15:11:12 read |
| The seat's checkout | git read verbs | at the head, branch `b1764/wp03-ci-skeleton`, porcelain 0, 26 tracked |
| The candidate step as a runner runs it | `run_step.py` (`/bin/bash --noprofile --norc -e -o pipefail`), on a fresh clone with the three files committed | `PLANTED-CONTROL neutral-scan: planted in 11 places, found by name 1, found under a neutral name 25 of 25, rc 1`; `NEUTRAL-SCAN: stored objects 71 (37 blob, 4 commit, 30 tree), copies written 142, objects of this commit not among them 0`; `no leaks found`; rc 0; planted value 0 times; porcelain equal |
| The plant, split | a JSON report (`--redact`) | files 6 and 7, commits 1 and 1, tags 1 and 1, folder listings 4 and 4: 25 |
| Suite, rules, scanner by name | python3, `repo_rules.py`, gitleaks | `Ran 53 tests`, `OK`; `RULES: clean (26 files)`; `gitleaks dir` rc 0; `gitleaks git` rc 0, `4 commits scanned.` |
| Mutants | `mutants.py`, 15 rows | in the kit's FACT 6 |
| The ignore file | `ignore_probe.py`, 4 cases | with the first line: rc 1 and the message; without it: rc 0, `no leaks found` (the hole) |
| The scanner's sources | `gh api -X GET` on `gitleaks/gitleaks` at `v8.30.1` and `h2non/filetype` at `v1.1.3` | `.gitleaksignore` is read from the start folder and from the scanned folder; 100000 bytes, then at most 25000 more; no type matcher reads a fixed byte beyond 32773 |
| Cost | a 3000-file scratch repository | export 18.8 s before, 31.6 s after; scan 1.0 s; the 96 MiB row 35.7 s for all four columns |
| Pointers | `awk NR==n`, `cat -n` | every `file:line` of the kit read as quoted at drafting |

Chain step inputs (each produced by an earlier step or present at the base):
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit | Tuesday |
| 1 | the Step-0 copy; the origin; `<repo>` at the head | Step 0; base |
| 2 | the head's `ci.yml` (round 2's function); gitleaks 8.30.1 | base |
| 3(a) | blocks T2A, T2B | Step 1 |
| 3(b) | block T1; the test file's helper | Step 1; Step 3(a) |
| 3(c) to 3(e) | the edited `ci.yml`; the Step-2 repositories; round 2's table (the round-2 kit copy and STATUS in `Briefs/`) | Steps 2, 3(b); base |
| 4 | block T3 | Step 1 |
| 5, 6 | the staged tree | Steps 3, 4 |
| 7 | blocks T4, T5; the pushed sha and the run id | Steps 1, 6 |

## Corrections to the commission
1. "Backlog lines 15 and 16" and "line 9" are OWED-line numbers. In the file they are lines 91 to 96, 97 to 102 and 55 to 60; the kit names the file lines.
2. **Finding 2 is wider than the verdict words it.** The verdict says the scanner reads "125 kB at a time". Measured, after the first cut at 125000 it cuts about every 28672 bytes (11 cuts in a 423 kB file, not 3). The closure still holds for a file with no blank line. `pr-body.md` line 20 of the second verdict folder carries the "125 kB at a time" wording.
3. **The gate's byte-mark rows do not by themselves prove the candidate closes finding 3.** They were placed for a 53-byte first line; with any other first-line length the first copy is read anyway. My rows D18 to D20 place the marks for round 3's 55-byte line: the first copy is then skipped and the SECOND copy finds all three. So finding 3 is closed as a side effect (measured on 3 rows, and derived from the type library's source). The commission lists it OUT: the kit asks the seat for nothing and T3 does not claim it. If Tuesday wants the README to claim it, that is a changed T3 (a new block and hash).
4. **Ref names.** The commission's property is "every object the repository stores". A branch name and a lightweight tag name are refs, not objects, and hold a token unseen (D16, D17). The kit names it as a limit (T3, T4C, T5E) and offers it as Q2. I did not add the one-line fix, because it is outside the commissioned scope.
5. **The read-cut closure is not total.** For a large file that has blank lines but none within 25 kB of a cut, the two copies are no longer a fixed distance apart; a shared cut is possible. Derived from the source, no row builds it. Named as a limit in T3. The total fix is Q1's alternative B.
6. The plant covers a commit MESSAGE and a tag MESSAGE, not an author or tagger line; those headers are in the same exported object and are proven by rows D03, D04 and D06 only.
7. The exact count 25 can be balanced by two faults at once: with the first copy's plain line removed, one finding is lost and one gained, and the step stays green (the fingerprint case is red). Q4 offers one planted repository per place.
8. For finding 5 I chose "the step fails", not "immune". The two by-name steps before it still read a root ignore file; the job is red at the last step either way.

## D-decisions (each Tuesday's as coordinator; the kit writes them so)
D1 every object twice; D2 the same one step, renamed; D3 the plant counts exactly 25; D4 an ignore file fails the step; D5 the fingerprint moves in the same commit, no new test case; D6 ref names are a named limit; D7 one commit, at most one fix-forward; D8 no dotnet, Jira, pull request or setting; D9 the gate probes through the function.

## Q-questions for Tuesday, each with its default
- Q1 the export's shape: default twice, 43008. (A: once. B: overlapping pieces.)
- Q2 ref names: default a named limit. (Alternative: one more exported file.)
- Q3 the ignore file: default the step fails.
- Q4 the planted count: default exactly 25.
- Q5 the OUT list: default the table.
- Q6 the gate: default G1.
- Q7 the pane: default `Datasec/OXPd2-X3`.
- Q8 the windows: default READY at Step 0 + 90 minutes, the push by Step 0 + 60 (round 2 took 33 minutes with a dotnet chain; this round has none).
A changed answer to Q1 to Q4 changes T1, so it is a new dry run, not a sentence at the stamp.

## Recommended slot answers (only what I measured, marked as mine; Tuesday writes its own reads)
- S0: Tuesday's alone, printed from the decision record at the stamp. The value must BEGIN with one of `open`, `ruled a`, `ruled b`, `ruled c`: the seat's refuse pattern is `\): ruled a(?![a-z])` on that line (checked: the unstamped line and `ruled b` do not match). I did not read the card.
- S1: `@NOW@` AEDT 2026-11-20, and what Tuesday read. The drafter read the kit's 12 blocks by program (FACT 8) and the 18-row table against the log.
- S2: the drafter read at 16:02:06: main `7e1a01cf640f8abac89e7148322651be8e4bf15b`; the branch `e0ddd0dc8518f97ceba09759c5c0b9e987d872e9`; 2 refs; pull requests 0; tags 0.
- S3: the drafter read at 16:02: the seat checkout at the head, porcelain 0; 0 panes holding `OXPd2`; `.tools` holds `b1764`, `b1774`, `dotnet`, `nuget-packages`, no `b1779`. **`<project>/1_Project_Definition/CLARIFICATIONS.md` carries the file time 15:42 of today: someone wrote it while I drafted. I did not open it. Whether another writer is under the project is Tuesday's to say.**
- S4: all eight defaults.
- S5, S7: Tuesday's (load1 at 16:03: 0.73).
- S6: no port; level fable; `BRIEF_SEAT_LEVEL=fable` inside the quotes.

## UNMEASURED
- Anything on a GitHub runner: T1 under bash 5 with GNU `head -c`, `tr`, `seq`, `cut`, `uniq -c`, `awk`, `sed -E`, the runner's `git cat-file -p` and `git tag -a`, the Linux binary of the scanner; that the count there is 25; the object counts 71 and 142 (derived for a fresh clone); `4 commits scanned.` (derived).
- A pull-request event (no pull request exists): which objects that checkout holds.
- A large file with blank lines whose two copies share a cut (derived only).
- A repository with thousands of objects on a runner (31.6 s for 3052 objects on this machine).
- Any type matcher behaviour beyond reading the source (the three marks are measured; "no other mark" is derived).
- The round-2 by-name steps with a root ignore file (not re-run; the gate measured them).
- Jira (no call). Line 29 of the runbook (19 issues) is left as it is.
- The state of the decision: not read.

## Outside the fences: disclosure
- Written: the kit, its sidecar, this report, and the scratch folder. Nothing else. An earlier sidecar skeleton was moved to scratch `_quarantine/measured.init1` (not deleted); three redacted scan reports of the sweep were renamed `.quarantine`.
- The project's checkout: git READ verbs, and it was the SOURCE of one `git clone` and one `git fetch` INTO my scratch (nothing written in it; its porcelain read 0 before and after). The scratch clones carry a push URL `invalid://no-push`. No build, no dotnet, nothing under the project's `.tools`.
- GitHub: `gh api -X GET` only: the project's repository (refs, pulls, compare, check runs) and two public repositories (`gitleaks/gitleaks`, `h2non/filetype`) for source files. No Jira call. No other HTTP.
- `/private/tmp/b1778-gate/`: read and copied (`scripts`, `logs`, `probes/scan`, `probes/big`); not written.
- Two of my shell calls were refused by machine hooks before running (a path given as a variable to a git write verb; a here-document whose text held the workflow's `git ... rm` line). Nothing ran in either; both were redone another way (a literal path; the Write tool). The kit warns the seat of the second.
- Tokens: every probe token was built by a program from a random source, lives only in scratch repositories and was never printed. The workflow's planted value stays in two halves in every file I wrote.
- Load: one heavy job (the 96 MiB row, 36 s) run alone; load1 between 0.73 and 3.04. No test of any project ran beside a lock.
- No text of the kit says the product owner decided anything: the kit says S0 states it, and refuses unless S0 begins `ruled a`.
