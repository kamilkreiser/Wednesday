GATE B1821: GO WITH FINDINGS @ ce38c25 on main c56f3f3

Delta review (G1 Tier 1, Opus 5.5, in-session) of ONE resolution commit of OXPd 2, WP4.2 (part): head
`ce38c25e08a4c9f6f1cec55214e51a60f75a4f5f` on the branch `b1788/wp42-ipp-encoder`, a merge commit whose parents are the reviewed
head `ec75619ed6e97f1fc0bbacb87660eae3fdbe4dca` and main `c56f3f3b015fae8d47288aa9d6c636ecd8fe2191`. Read and measured 2026-11-21
from 09:50 to 09:58 AEDT (clocks by `date`). Read clone `/private/tmp/b1821-gate/clone` (one clone of the origin, push URL
`invalid://no-push`, no identity); the git verbs that write objects (`merge-tree --write-tree`, `hash-object -w`, a
temporary-index `write-tree`, the scratch repositories of the text scans) ran in a mirror of that clone inside the session's
scratchpad. Every number below was printed by a program; programs under `/private/tmp/b1821-gate/scratch/`, logs under
`/private/tmp/b1821-gate/logs/`. The yardstick is the second verdict (`2026-11-21_B1819_verify/VERDICT.md`); this is not a
third review of the lane.

**BLUF.** GO WITH FINDINGS: no Blocker, no Major. The commit is exactly the allowed change: one merge commit, parents
ec75619e then main, pushed as a fast-forward; against a three-way merge of the two it differs in `Datasec.Suite.slnx` only,
and that file is byte-equal to the block of the second gate's landing text (sha256 df48c25f...); its tree is
`6fc18eaa1e7356cf394c3fe2c47bfa1003fafb9c`, equal entry by entry to the gate's own prediction. All 31 paths of the branch
(the 11 of the fix round among them) and all 22 of main are blob-equal to their side, so both earlier verdicts' measurements
of the code stand. The merged tree builds (0 warnings, 0 errors) and passes 476 of 476 (1 + 284 + 191) in the gate's own run;
nothing the two sides share resolves differently. The hosted run's four jobs are success with every proof line. Two sentences
of the pull-request body were made untrue by the merge (285 tests, two commits); re-worded and re-scanned here.
**In plain words: yes, the branch can now be landed by the squash line of this folder's `landing.txt` (pinned to ce38c25e).
The hosted code scan runs only on the pull request and has not run on this code; it is the authority and must be green.**

## Item 1: the commit is exactly the allowed change (`scratch/item1.py`, `logs/item1.log`: ITEM1 PASS, every control fired)

| Check | Read | Control (must fail) |
|---|---|---|
| refs | the fresh clone (09:50) and GET at 09:57:33: branch `ce38c25e`, main `c56f3f3b`; other branches as Tuesday read them | another branch's sha compared the same way: FIRED |
| parents | `rev-list --parents -n 1`: `ce38c25e ec75619e c56f3f3b`, in that order | ec75619e's own parents, and the swapped order: FIRED |
| one new commit, fast-forward | commits in `ec75619e..ce38c25e` not in main: 1, `ce38c25e`; `ec75619e..ce38c25e` is 2 (the merge and main's commit); commits beyond main: `9f4238ad`, `ec75619e`, `ce38c25e`; merges beyond main: 1 (`ce38c25e`); `merge-base --is-ancestor ec75619e ce38c25e` rc 0 | the reverse rc 1: FIRED |
| (a) the merge | `merge-tree --write-tree --name-only ec75619e c56f3f3b`: rc 1, tree `637918b85232a72ce2ce08ef385c33465688cc74`, ONE conflict `CONFLICT (content): Merge conflict in Datasec.Suite.slnx`; `diff --name-only <that tree> ce38c25e`: exactly `Datasec.Suite.slnx` | the same diff against ec75619e: 22 paths: FIRED; main merged with itself rc 0 |
| (b) the block | cut by program from the second gate's `landing.txt` lines 43 to 55, three-space indent removed: 13 lines, 699 bytes, sha256 `df48c25f0a60cfd6fca65912d866b15b70ca0efdb701b00d23cba3fcc841179d` (equal to the stated one), blob `b659bf846a81faaf2838a5b72f8d744ea3f1cbc2`; the file at ce38c25e: 699 bytes, byte-equal; CR or non-ASCII 0 | the file at ec75619e compared the same way: FIRED |
| (c) the tree | prediction from `ls-tree -r` of main (46 entries) with the branch's 31 paths since `7bf37526` laid over at ec75619e's blob (30 added) and the solution file as the block blob: 76 entries; ce38c25e: 76 entries; differing 0; the prediction written as a tree object: `6fc18eaa1e7356cf394c3fe2c47bfa1003fafb9c` = the head's tree = the kit's pinned tree | the prediction with the branch's solution file in place of the block: FIRED |
| (d) the 11 | paths of `9f4238ad..ec75619e`: 11; blob at ce38c25e equal to ec75619e's: 11 | read at main: equal 0 (absent): FIRED |
| (d) the 31 | paths of the branch since the merge base: 31; blob at ce38c25e equal to ec75619e's: 30, the 31st the solution file (now the block) | read at main: equal 0: FIRED |
| (d) main's 22 | paths of main since the merge base: 22; blob at ce38c25e equal to main's: 21, the 22nd the solution file; the two sides share that one path only; the other 24 paths equal at all three commits | read at ec75619e: equal 0: FIRED |
| (d) modes | every entry at ce38c25e `100644` | a planted 100755 entry: FIRED |
| (e) message | 3 lines: the subject `Merge main into the IPP encoder branch; the solution file keeps the projects of both sides (WP4.2)` (98 bytes), an empty line, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; nothing else; sha256 `c29fbb82...` (the kit's message file); non-ASCII bytes in the commit object 0 | the same subject with one planted body line: FIRED |
| (e) words | over the message without the attribution line, underscore-aware: ban-list names (the verifier standard's list plus Tuesday, Wednesday, Friday), B-numbers, ticket keys, clarification ids, seat ids, card and decision ids, "product owner", "coordinator", "review", "gate", "ruling"/"ruled", decision words, "Tuesday", "Opus"/"Fable" outside the attribution: 0 hits | one planted line per class: 14 of 14 fired |
| (e) identity | author and committer name and e-mail equal the repository checkout's own local `user.name` and `user.email` (compared in-process, not printed); the same identity as on ec75619e | a planted identity compared the same way: FIRED |
| (e) secret scans | `gitleaks git` of the clone with the workflow's options (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`), scanner 8.30.1: rc 0, `15 commits scanned.`, `no leaks found`; `gitleaks dir` of the checked-out head: rc 0, `no leaks found` | the workflow's planted value in a folder: rc 1, `leaks found: 1` |

**So both verdicts' product measurements stand:** every path of the library, its tests and main is blob-equal at ce38c25e to
the commit each verdict read, the solution file is the block the second verdict printed, and nothing else differs.

**The builder's `proofs.py` as an instrument** (run from a copy against the gate's mirror, `logs/proofs-copy.log`): P1 to P7
and P9 read what they claim and each control is the same comparison on an input that fails (P3 builds its prediction from
the two parents, never from the commit; P4 diffs against git's own merge). P2 and P4 also pin the drafter's prototype ids
(`6fc18eaa`, `637918b8`), which only P3 makes non-circular. **P8 (identity) is not a true proof as written:** it compares the
commit with the CLONE's local config (in the gate's clone, which has no identity, it prints FAIL; in the seat's clone it is
true only because `clone.py` copied the checkout's values and printed "equals the checkout's: True"), and its control
compares a constant with that config, so it can never fail on a commit with a wrong identity. The gate's own check against
the checkout's config reads true. Records only (finding R1).

## Item 2: the merged tree builds and passes (`logs/restore.log`, `build.log`, `test.log`, `split-*.log`)

Every job through the gate's copy of the wave's runner (`tools/heavy.py`, sha256 equal to the kit's), the project's SDK
10.0.404, home `/private/tmp/b1821-gate/dotnet-home`, the gate's own package cache (a copy of the project's, 585 MB, 64
packages), the closed local proxy, the three build settings.
- restore `dotnet restore Datasec.Suite.slnx --locked-mode -p:NuGetAudit=false`: rc 0, 7 projects restored (audit off: NOT a
  full restore; known-vulnerability status NOT TESTED).
- build `-c Release --no-restore`: rc 0, `Build succeeded.`, `0 Warning(s)`, `0 Error(s)`, 7 assemblies.
- test `-c Release --no-build`, whole solution: `total: 476`, `failed: 0`, `succeeded: 476`, `skipped: 0`. The runner prints
  each test project "passed" without a count; each test project's own runner then printed: `Datasec.Suite.Core.Tests Total: 1`,
  `Datasec.Suite.UniversalPrint.Tests Total: 284`, `Datasec.Suite.Logging.Tests Total: 191` (1 + 284 + 191 = 476, failed 0 each).
- unit tests of the workflow: `Ran 53 tests`, `OK`; `build/repo_rules.py`: `RULES: clean (76 files)` rc 0 (it says its R5 hash
  half is NOT RUN); control: a planted `oxpd2lib` in a copy of the solution file's bytes gives `RULES: R2 Datasec.Suite.slnx:13`,
  rc 1 (bytes restored, porcelain 0).
- publishes of the server (linux-x64, win-x64, as the workflow) and the release guard: `GUARD: clean (10 files)` and
  `GUARD: clean (11 files)`, each rc 0 with the owed warning `development CA deny-list holds 0 fingerprints`; neither folder
  holds a UniversalPrint or Logging file. (The first two publish attempts failed `NU1900` because the gate's command left the
  publish's own restore audit on behind the closed proxy; re-run with `-p:NuGetAudit=false`. A fault of the gate's command,
  not of the commit.)
- `status --porcelain` 0 lines after every job.

**Does anything the two sides share change behaviour when they meet? No.** `Directory.Packages.props` changed on main only
(+2 lines: `Serilog` [4.4.0], `Serilog.Sinks.File` [7.0.0]); no project of the branch references either. The locked-mode
restore of ce38c25e passed, so every project resolved exactly its committed lock file. The gate also restored a `git archive`
of ec75619e the same way and compared, for the five projects present at both (`scratch/resolve_cmp.py`): resolved entries
(Server 9, Core.Tests 54, UniversalPrint.Tests 54, the two libraries 0), library lists and lock-file entries (5, 22, 22) equal
at both trees, Serilog among them 0; control (one entry planted in a copy) unequal. `repo_rules.py` (R2 reads `.slnx`,
`build/repo_rules.py:46`) is clean over the 76 files. The two GUARD lines are unchanged (10 and 11 files) locally and hosted.

## Item 3: the hosted run of ce38c25e (`logs/hosted.out` by the copied reader; `logs/item3.log` the gate's own recount)

Check runs by GET at 09:54:58: exactly 4, `linux`, `windows`, `secret-scan`, `rules`, each completed success, app
github-actions, head sha ce38c25e, run 44831455002 attempt 1; beside them 0. The four job logs by GET with
`--allow-escape-sequences`, return code asserted (31,789, 25,206, 26,877 and 25,713 bytes; the runner's echo of each script
left out), recounted by the gate's own program: linux and windows `total: 476` 2 each, `succeeded: 476` 1, `failed: 0` 1,
`0 Warning(s)` 1, `0 Error(s)` 1, `GUARD: clean (10 files)` (linux) 1 and `GUARD: clean (11 files)` (windows) 1, `total: 285` 0
and `total: 192` 0; rules `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (76 files)` 1 (`(56 files)` 0);
secret-scan `PLANTED-CONTROL secret-scan: rc 1` 1, `... found under a neutral name 25 of 25, rc 1` 1, `15 commits scanned.`,
`NEUTRAL-SCAN: stored objects 312 (215 blob, 16 commit, 81 tree), copies written 624, objects of this commit not among them 0`,
`no leaks found` 3. Control line counts 0 in every log.

**NEUTRAL-SCAN, hosted beside the builder's local line:** hosted 312 (215 blob, 16 commit, 81 tree); the builder's local
316 (217 blob, 16 commit, 83 tree). The gate's own fresh clone (09:50, the same refs) stores 312 objects (215 blob, 81 tree,
16 commit), all 312 reachable from a ref: equal to the hosted line. So the builder's 4 extra are local objects no ref
reaches (it named them: the trial's conflict tree and blob and the merge's conflict tree and blob). **No branch of the origin
moved between** (refs by GET at 09:49 by Tuesday, at the gate's clone at 09:50 and again at 09:57:33 are identical).

## Item 4: the landing texts re-pinned (`scratch/item4.py`, `logs/item4.log`; `scratch/texts.py`, `logs/texts.log`)

| Sentence or number (text) | Instrument | Value at ce38c25e | True? |
|---|---|---|---|
| 137 test methods (pr-body, squash-body) | `[Fact]`/`[Theory]` lines in the test project | 137 | true |
| 284 test cells (pr-body, squash-body) | the test project's own runner | 284 | true |
| "at the branch head the solution runs 285 tests on both legs" (pr-body) | whole-solution test, gate and both hosted legs | 476 | **FALSE** |
| "Two commits: the first adds the library; the second ..." (pr-body) | `rev-list main..head`, `--merges` | 3 commits, 1 a merge | **FALSE** |
| "The server does not reference it yet", "nothing of it runs in the product", title "nothing talks to anything yet" | the server project's references; both publishes | one reference, to Core; 0 library files published | true |
| "Nothing in this library talks to anything" | references of the library project | 0 | true |
| "`Datasec.Suite.slnx`: two lines added, one in each folder block" (pr-body), "Two lines added to Datasec.Suite.slnx" (squash-body) | `diff --numstat main ce38c25e` and the added lines | 2 0: the library line in `/src/`, the test line in `/tests/` | true |
| "No package is added, and no line of `Directory.Packages.props`, of the workflow or of `build/` changes" | `diff` against main | 0, 0, 0; the only lock files are the lane's own two | true |
| "The Layout and Reserved names lists of the root README.md are not updated here" | `diff` against main | README unchanged | true |
| "Code scanning has not read this code before this pull request" | GET code-scanning analyses for the branch ref | 0 analyses | true |
| "The Windows leg ran on the hosted runner only" | item 3 | hosted windows success; no local Windows run | true |

20 rows read by program, 2 false. Every number and sentence about the library's code (the bounds, the lists, the waits,
the stream's limits, the delimiters, the request builders) stands by item 1(d): the 31 paths are blob-equal to ec75619e,
and the gate did not re-run them. **The two false sentences are re-worded in this folder's `pr-body.md`** (finding T1):
"(137 test methods, 284 test cells; at the branch head, which also holds main, the solution runs 476 tests on both legs).
Three commits: the first adds the library; the second makes the document stream stop at its close, ... and adds tests that
compare every name list whole; the third merges main into the branch and changes no line of the library (the solution file
keeps the projects of both sides)." No other byte changed.

Texts in this folder: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` byte-equal copies of the second gate's (`cmp`
rc 0 each); `pr-body.md` changed (the one paragraph above); `landing.txt` NEW (pins ce38c25e in `--match-head-commit`; names
the three commits beyond main and that ce38c25e is a merge whose second parent is main; section 2 is now the record of the
resolution; the DO NOT LAND opening is dropped; the check wait and its reads are kept; the after-merge reads give
`total: 476` and `RULES: clean (76 files)` unless another lane lands first).

Each text exported through the workflow's own `neutral_export` (cut by program from `ci.yml` at ce38c25e, lines 120 to 128)
as the commit message of a scratch repository, then scanned with the workflow's options (scanner 8.30.1): title alone; title
and body; body alone; the squash message with a number; as written; the squash body alone; the repository's default squash
shape (the title and the three commit messages as a list); landing.txt: **each export rc 0, the message stored whole, scan
rc 0, "no leaks found". Control (the squash message with the workflow's planted value): rc 1, "leaks found: 2".** Word counts
over the four texts: ban-list names, B-numbers, ticket keys, clarification ids, seat ids, "product owner", "review", "gate",
"ruling"/"ruled", "decided"/"approved": 0 each (controls 10 of 10 fired); non-ASCII 1, the pull-request footer only.

## Item 5: process

- Heavy jobs: 11, every one through the runner, one at a time, load1 read first (0.51 to 0.73), lock taken by `mkdir` of
  exactly `.tools/wave1-heavy.lock.d` with `owner.txt`, released by moving it into `/private/tmp/b1821-gate/_quarantine/locks/`
  (11 folders there): restore, build, test, restore of the ec75619e archive, two failed and two good publishes, three
  test-project runs. **The lock was never waited for** (0 waits each, `logs/gate.log`). After the last job: no process of the
  gate alive (`ps eww` search for `b1821-gate/dotnet-home` matched only the search itself); the lock folder absent.
- Left in `/private/tmp/b1821-gate/`: `clone/` (detached at ce38c25e, porcelain 0, build output ignored), `old/` (the
  ec75619e archive, restored), `out/` (two publishes), `nuget/` (the package-cache copy), `tools/` (the drafter's ten files,
  copied, unedited), `scratch/` (item1, item3, item4, resolve_cmp, texts programs; a planted-control folder), `logs/`,
  `dotnet-home/`, `_quarantine/locks/`. In the scratchpad: `w.git` (a mirror of the clone, push URL invalid), `texts/` (nine
  scratch repositories and their exports), one used temporary index.
- Nothing pushed, opened, merged, deployed or sent; no ticket; no setting changed. Hosted calls: one clone of the origin, and
  `gh api -X GET` only (check runs, job records and logs, refs, pulls, code-scanning analyses).

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| T1 | Text (re-worded, re-scanned) | No | Two sentences of the second gate's `pr-body.md` are made false by the merge: "at the branch head the solution runs 285 tests" (now 476) and "Two commits" (now three, the third a merge of main). | Use this folder's `pr-body.md` (re-worded, scanned rc 0). The other three texts are byte-equal and true. |
| R1 | Records | No | The builder's `proofs.py` P8 compares the commit's identity with the clone's own config, and its control compares a constant with that config, so it cannot fail on a wrong identity. The other eight proofs are true proofs. The commit's identity is right (the gate's own check against the checkout). | For the next kit's proof program: compare against the checkout's config, and make the control run the comparison on a commit with a planted identity. |
| R2 | Records | No | The builder's local NEUTRAL-SCAN line (316 objects) differs from the hosted one (312) by 4 unreachable local objects of the merge; the gate's fresh clone reads 312. No branch moved. | None for the code; a kit that lays the two lines side by side should expect the merge's by-products. |

No Blocker. No Major. The second verdict's findings (its L, 1 to 5) are not re-opened; its finding L (the landing condition)
is met by this commit.

## FOUND / TESTED / NOT TESTED

- FOUND: 0 Blockers, 0 Majors, 1 text finding (re-worded), 2 records lines.
- TESTED: the rows above, in the gate's own clone and mirror, with the project's SDK, the gate's own home and package cache.
- NOT TESTED / NOT RUN:
  - CodeQL for C# (cannot extract on arm64); the hosted code scan has not run on this branch (0 analyses for its ref); it
    runs on the pull request and is the authority.
  - A full restore with the vulnerability audit (the proxy was closed; known-vulnerability status not tested).
  - The 11 fix-round paths and the branch's other paths were NOT re-reviewed: they stand by blob-equality (item 1(d)).
  - Windows locally (the hosted leg is green); the release guard's hash half and `repo_rules.py`'s R5 hash half.
  - Whether GitHub reads the future pull request as mergeable (no pull request exists; expected clean, UNMEASURED).
  - Anything against a printer, a tenant or the print service; every fixture stays PROVISIONAL.
  - The builder's `history.md` entry and its STATUS sections beyond those used here.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt.
