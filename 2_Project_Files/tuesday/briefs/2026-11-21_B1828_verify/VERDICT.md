GATE B1828: GO WITH FINDINGS @ 9826559 on main ddbdf80

Delta review (G1 Tier 1, Opus 5.5, in-session) of ONE resolution commit of OXPd 2, WP1.1 (the local secret store): head
`9826559d7e00d473cd119da622a26dcaf48f922b` on the branch `b1789/wp11-local-secret-store`, a merge commit whose parents are
the reviewed head `bf1a4a24492f7849705e48cbc1d4938e15f30c56` and main `ddbdf8009d0df77d084ef4834bb78d7c4a80b5b0`. Read and
measured 2026-11-21 from 15:05 to 15:15 AEDT (clocks by `date`). Read clone `/private/tmp/b1828-gate/clone` (one clone of
the origin at 15:05:58, push URL `invalid://no-push`, no identity); the git verbs that write objects (`merge-tree
--write-tree`, `hash-object -w`, a temporary-index `write-tree`, a trial `merge --no-commit`, the scratch repositories of
the text scans) ran in a mirror of that clone and a clone of the mirror inside the session's scratchpad. Every number below
was printed by a program; programs under `/private/tmp/b1828-gate/scratch/`, logs under `/private/tmp/b1828-gate/logs/`.
The yardstick is the second verdict (`2026-11-21_B1824_verify/VERDICT.md`); this is not a third review of the lane.

**BLUF.** GO WITH FINDINGS: no Blocker, no Major. The commit is exactly the allowed change: one merge commit, parents
bf1a4a24 then main, pushed as a fast-forward; against a three-way merge of the two it differs in `Datasec.Suite.slnx` only,
and that file is byte-equal to block (b3) of the second verdict's `landing.txt` (sha256 `a94ad1ac...`) and is main's file
plus exactly the library's two lines; its tree is `4a6fd8501706a01b9966fc897ef4c1b965834796`, equal entry by entry to the
gate's own prediction. The 21 other fix-round paths, the 38 other branch paths and main's 88 other paths are blob-equal to
their side, and the diff of the two lane folders against bf1a4a24 is 0 bytes, so both earlier verdicts' measurements of the
code stand. The merged tree builds (0 warnings, 0 errors) and passes 762 of 762 run (758 passed, 4 skipped: 1 + 68 + 191 +
284 + 218) in the gate's own run; nothing the two sides share resolves differently. The hosted run's four jobs are success
with every proof line. Three sentences of the pull-request body were made untrue or inexact by the merge (two commits, 69
tests, "against this head"); re-worded and re-scanned here, with the second verdict's N1 to N8 carried in as known
follow-ups, N1 first. **In plain words: yes, the branch can now be landed by the squash line of this folder's
`landing.txt` (pinned to 9826559d), as long as main has not moved. The hosted code scan runs only on the pull request and
has not run on this code; it is the authority and must be green.**

## Item 1: the commit is exactly the allowed change (`scratch/item1.py`, `logs/item1.log`: ITEM1 PASS, every control fired)

| Check | Read | Control (must fail) |
|---|---|---|
| refs | the fresh clone (15:05:58) and GET at 15:05:49 and 15:14:17: branch `9826559d`, main `ddbdf800`; b1764, b1786, b1787, b1788 unchanged; pull requests 4, all closed | another branch's sha compared the same way: FIRED |
| parents | `rev-list --parents -n 1`: `9826559d bf1a4a24 ddbdf800`, in that order | bf1a4a24's own parents, and the swapped order: FIRED |
| one new commit, fast-forward | commits in `bf1a4a24..head` not in main: 1, `9826559d`; `bf1a4a24..head` is 4 (the merge and main's 3); commits beyond main `42f926d5`, `bf1a4a24`, `9826559d`; merges beyond main 1 (`9826559d`); `merge-base --is-ancestor bf1a4a24 head` rc 0 | the reverse rc 1: FIRED |
| (a) the merge | `merge-tree --write-tree bf1a4a24 ddbdf800`: rc 1, tree `06e78fc501dd22973dfeaa81611006ff5d6cef27`, ONE conflict `CONFLICT (content): Merge conflict in Datasec.Suite.slnx` (its conflicted file: 1243 bytes, 2 marker lines); `diff --name-only <that tree> head`: exactly `Datasec.Suite.slnx` | the same diff against bf1a4a24: 89 paths: FIRED; main merged with itself rc 0 |
| (b) the block | cut by program from the second verdict's `landing.txt`, the third `<Solution>`...`</Solution>` block at column 1 (lines 67 to 83): 17 lines, 1031 bytes, sha256 `a94ad1ac414a9fb3eca2142f150fb254e8219f54bee96752a3e0cef26e21c8d6`, blob `0791300ab2b36e31e98b8ae8f4b08efc4a543b5b`; the file at the head: 1031 bytes, byte-equal; CR or non-ASCII 0. Main's 15 lines plus exactly the branch's two Secrets lines, every other line in main's order, the Path values ordinal in both Folder blocks | the file at bf1a4a24 and block (b2): FIRED; the branch file and a copy with two lines swapped fail the second check: FIRED |
| (c) the tree | prediction from `ls-tree -r` of main (113 entries) with the branch's 39 paths since `7bf37526` laid over at bf1a4a24's blob (38 added) and the solution file as the block blob: 151 entries; head: 151; differing 0; the prediction written as a tree object: `4a6fd8501706a01b9966fc897ef4c1b965834796` = the head's tree = the kit's pinned tree | the prediction with the branch's solution file in place of the block: FIRED |
| (d) the 22 | paths of `42f926d5..bf1a4a24`: 22, the solution file among them; of the other 21, blob at head equal to bf1a4a24's: 21 | read at main: equal 0 (absent 21): FIRED |
| (d) the 39 | paths of the branch since the merge base: 39; of the 38 that are not the solution file, blob at head equal to bf1a4a24's: 38 | read at main: equal 0: FIRED |
| (d) lane folders | `git diff bf1a4a24 head -- src/Datasec.Suite.Secrets tests/Datasec.Suite.Secrets.Tests`: rc 0, 0 bytes; files 21 and 17 | the same diff against main: 211,554 bytes: FIRED |
| (d) main's 89 | paths of main since the merge base: 89 (87 added, `Directory.Packages.props`, the solution file); of the 88 that are not the solution file, blob at head equal to main's: 88; the sides share that one path only; the other 24 paths equal at all three commits | read at bf1a4a24: equal 0: FIRED |
| (d) modes | every one of 151 entries `100644` | a planted 100755 entry: FIRED |
| (e) message | 3 lines: the subject `Merge main into the local secret store branch; the solution file keeps the projects of both sides (WP1.1)` (105 bytes), an empty line, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; nothing else; 163 bytes, sha256 `eab1af16...` (the kit's message file); non-ASCII bytes in the commit object 0 | the same subject with one planted body line: FIRED |
| (e) words | over the message without the attribution line, underscore-aware: ban-list names (the verifier standard's list plus Tuesday, Wednesday, Friday), B-numbers, ticket keys, clarification ids, seat ids, card and decision ids, "product owner", "coordinator", "review", "gate", "ruling"/"ruled", decision words, "Tuesday", "Opus"/"Fable" outside the attribution: 0 hits | one planted line per class: 14 of 14 fired |
| (e) identity | author and committer name and e-mail equal the project checkout's own local `user.name` and `user.email` (compared in-process, not printed); the same identity as on bf1a4a24 | main's head (a squash made by the hosting service) compared the same way: unequal: FIRED |
| (e) secret scans | `gitleaks git` of the clone with the workflow's options (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`), scanner 8.30.1: rc 0, `17 commits scanned.`, `no leaks found`; `gitleaks dir` of the checked-out head: rc 0, `no leaks found` | the workflow's planted value in a folder: rc 1, `leaks found: 1` |

**So both verdicts' product measurements stand:** every path of the library, its tests and main is blob-equal at 9826559d
to the commit each verdict read, the solution file is the block the second verdict printed, and nothing else differs.

**The builder's `proofs.py` as an instrument** (copied with the other nine tools into `/private/tmp/b1828-gate/tools/`, ten
hashes equal to the kit's; run from the copy against the gate's mirror, `logs/proofs-copy.log`): P1 to P7, P9 and P10 read
what they claim, and each control is the same comparison on an input that fails (P3 builds its prediction from the two
parents, never from the commit; P4 diffs against git's own merge; P10 is the lane-folder diff). P1's control (bf1a4a24's
parents) is weak but can fail; P2 pins the drafter's prototype tree, which only P3 makes non-circular. **P8 (identity) is
not a true proof as written**: it compares the commit with the CLONE's local config, and its control compares a constant
with that config, so it can never fail on a commit with a wrong identity. In the gate's clone (no identity) it prints
`FAIL P8 identity` (`PROOFS: FAIL P8 identity (controls fired 10 of 10)`); in the seat's clone it read true only because
its clone program copied the checkout's values and printed "equals the checkout's: True". The gate's own check against
the checkout reads true. The same defect as the print lane's merge kit; records only (R1).

## Item 2: the merged tree builds and passes (`logs/restore.log`, `build.log`, `test.log`, `split-*.log`)

Every job through the gate's own runner (`scratch/runner.py`): load1 read first, the wave's lock by `mkdir` of exactly
`<project>/.tools/wave1-heavy.lock.d` with `owner.txt`, one command under 900 s, the lock moved into
`/private/tmp/b1828-gate/_quarantine/locks/`; the project's SDK 10.0.404, home `/private/tmp/b1828-gate/dotnet-home`, the
gate's own package cache (a copy of the project's, 585 MB, 64 packages), the closed local proxy, the three build settings.
- restore `dotnet restore Datasec.Suite.slnx --locked-mode -p:NuGetAudit=false`: rc 0, 11 projects restored, porcelain 0
  (audit off behind the closed proxy: NOT a full restore; known-vulnerability status NOT TESTED).
- build `-c Release --no-restore`: rc 0, `Build succeeded.`, `0 Warning(s)`, `0 Error(s)`, 11 assemblies.
- test `--solution Datasec.Suite.slnx -c Release --no-build`: `total: 762`, `failed: 0`, `succeeded: 758`, `skipped: 4`
  (K06, K07, W01, W02 of the store, each with the Windows-only reason). Split, one run per test project: Core.Tests 1,
  Secrets.Tests 68 (64 passed, 4 skipped), Logging.Tests 191, UniversalPrint.Tests 284, Cards.Tests 218, failed 0 each
  (1 + 68 + 191 + 284 + 218 = 762): the Core test both sides share once, the Logging, UniversalPrint and Cards tests of
  main, the Secrets tests of the branch.
- unit tests of the workflow: `Ran 53 tests`, `OK`; `build/repo_rules.py`: `RULES: clean (151 files)` rc 0 (= `ls-files`
  151; it says its R5 hash half is NOT RUN); control: a planted `oxpd2lib` in the solution file's bytes gives `RULES: R2
  Datasec.Suite.slnx:17`, rc 1 (bytes restored, porcelain 0).
- publishes of the server (linux-x64, win-x64, as the workflow, audit off) and the release guard: `GUARD: clean (10
  files)` and `GUARD: clean (11 files)`, each rc 0 with the owed warning `development CA deny-list holds 0 fingerprints`;
  no Secrets, Logging, UniversalPrint or Cards file in either folder.
- `status --porcelain` 0 lines after every job.

**Does anything the two sides share change behaviour when they meet? No.** `Directory.Packages.props` changed on main only
(+2 lines: `Serilog` [4.4.0], `Serilog.Sinks.File` [7.0.0]); neither store project references a package but `xunit.v3`
(the tests); the library has one `FrameworkReference` (ASP.NET Core) and no package. The locked-mode restore of 9826559d
passed, so every project resolved exactly its committed lock file. The two Secrets lock files are blob-equal at both
commits (item 1(d)); that proves the pins are the same, not what a restore resolves, so the gate also restored a `git
archive` of bf1a4a24 the same way and compared, for the five projects present at both (`scratch/resolve_cmp.py`,
`logs/resolve_cmp.log`): resolved entries (Secrets 0, Secrets.Tests 54, Core 0, Core.Tests 54, Server 9), library lists,
framework references and lock-file entries (0, 22, 0, 22, 5) equal at both trees, Serilog among them 0; control (one
version changed in a copy) unequal. `repo_rules.py` reads every project and solution file: clean over 151. The two GUARD
lines are unchanged (10 and 11 files) locally and hosted. The store's 4 Windows-only tests skip on macOS and Linux and its
18 Unix-only tests skip on Windows, by the same names as at bf1a4a24 (item 3).

## Item 3: the hosted run of 9826559d (`scratch/item3.py`, `logs/item3.log`, logs saved under `api/`)

Check runs by GET at 15:09:42: exactly 4, `linux`, `windows`, `secret-scan`, `rules`, each completed success, app
github-actions, head sha 9826559d, run 44863801046 attempt 1, every step success or skipped; beside them 0. The four job
logs by GET with `--allow-escape-sequences`, return code asserted (36,825, 35,734, 26,921 and 25,782 bytes; the runner's
echo of each script left out), counted by the gate's own program: linux and windows `total: 762` 2 each, `failed: 0` 1,
`0 Warning(s)` 1, `0 Error(s)` 1; linux `succeeded: 758` 1, `skipped: 4` 1 (K06, K07, W01, W02), `GUARD: clean (10 files)`
1; windows `succeeded: 743` 1, `skipped: 19` 1, `GUARD: clean (11 files)` 1; `total: 69` and `total: 694` 0 on both;
rules `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (151 files)` 1 (`(64 files)` 0); secret-scan
`PLANTED-CONTROL secret-scan: rc 1` 1, `PLANTED-CONTROL neutral-scan: ... found under a neutral name 25 of 25, rc 1` 1,
`17 commits scanned.`, `NEUTRAL-SCAN: stored objects 323 (217 blob, 19 commit, 87 tree), copies written 646, objects of
this commit not among them 0`, `no leaks found` 3. Control line `GATE-B1828-NOT-A-LINE` 0 in every log. **Windows skipped
by name: 19 = the store's 18 Unix-only tests (one reason: "Unix only: the key file protects the key ring there; Windows
uses DPAPI-NG.") and `W01`, with the reason "The default DPAPI-NG descriptor was refused on this machine.", the same 19
names and the same W01 reason as bf1a4a24's windows log read the same way.**

**NEUTRAL-SCAN, hosted beside the builder's local line:** hosted 323 (217 blob, 19 commit, 87 tree); the builder's local
327 (219 blob, 19 commit, 89 tree). The gate's fresh clone (15:05:58, the same refs) stores 323 objects (217 blob, 19
commit, 87 tree), all 323 reachable from a ref: equal to the hosted line. So the builder's 4 extra are local objects no
ref reaches, as it said: the trial `merge-tree` tree `06e78fc5...` with its conflicted blob `22616b47...` (the gate's own
`merge-tree` wrote the same pair), and tree `d0176fad...` with blob `67afeec8...`, which the builder attributed to its
`git merge --no-ff --no-commit` without proof: **measured here**, in a scratch clone of the mirror, both absent before
that merge and present after it (then `merge --abort`, porcelain 0). **No branch of the origin moved between** (refs by GET
at 15:03:43 by Tuesday, at 15:05:49 and 15:14:17 by the gate, and in the gate's clone, identical).

## Item 4: the landing texts re-pinned (`scratch/item4.py`, `logs/item4.log`; `scratch/texts.py`, `logs/texts2.log`)

| Sentence or number (text) | Instrument | Value at 9826559d | True? |
|---|---|---|---|
| 68 tests (pr-body, squash-body) | the test project's own run (gate) | 68 (64 passed, 4 skipped) | true |
| four run on Windows only (pr-body, squash-body) | skipped on macOS and hosted linux with the Windows-only reason | 4 | true |
| eighteen on Unix only (pr-body, squash-body) | hosted windows skipped lines with the Unix-only reason | 18 | true |
| "Two commits on the branch, folded by the squash: the library, then a second commit ..." (pr-body) | `rev-list main..head`, `--merges` | 3 commits, 1 a merge | **FALSE** |
| "(69 tests in the solution, 0 failed on each)" (pr-body) | whole-solution test, gate and both hosted legs | 762 | **FALSE** |
| "an independent review's attack program and its mutants against this head" (pr-body) | item 1(d) | they ran on bf1a4a24; the lane folders are byte-equal at 9826559d | **inexact** |
| "The server does not reference the library yet" (pr-body, squash-body, landing), "the server does not use it yet" (title, squash subject) | the server project's references | one, to Core | true |
| "The published folders of the server are unchanged" (pr-body, squash-body) | both gate publishes; GUARD lines against main's hosted 10 and 11 | 10 and 11 files; 0 Secrets files | true |
| "taken from the shared framework (no package)" (pr-body, squash-body) | the library project's references; resolve_cmp | FrameworkReference ASP.NET Core; 0 packages | true |
| "Code scanning had not run on this branch when it was reviewed: it runs on this pull request" | GET code-scanning analyses for the branch ref | 0 analyses | true |
| "Windows was run on a hosted build runner only"; "The default descriptor ... was refused on that runner: the store wrote nothing and the test skipped itself" | item 3 | hosted windows success; W01 skipped with that reason | true |
| "The solution file gains this library's two lines in the ordinal order of their paths" | `diff --numstat main head`, the added lines, item 1(b) | `2 0`, the Secrets library and test lines, ordinal | true |
| "No package, workflow or build line changes" | `diff --name-only main head` of `Directory.Packages.props`, `Directory.Build.props`, `.github`, `build`, `global.json`, `NuGet.config` | 0 each | true |
| "Nothing is deployed"; landing "the repository's one workflow (.github/workflows/ci.yml) ... has no deploy step" | workflow files at the head; the word deploy in ci.yml | one file; 0 | true |
| landing "src/Datasec.Suite.Secrets/ (21 files) and tests/Datasec.Suite.Secrets.Tests/ (17 files)" | `ls-tree` of the head | 21, 17 | true |
| landing "THIS HEAD CANNOT LAND AS IT IS" and step 0 | item 1 | the head now merges main | replaced (new landing.txt) |

25 rows read by program (the table groups them), 3 sentences of the pull-request body false or inexact, plus the old
landing's cannot-land paragraph. Every number and sentence about the library's own code (1 byte to 1 MiB, the nonce and
tag sizes, the 32-byte key file, the check rules, rotation, the Limits) stands by item 1(d): the 38 paths are blob-equal
to bf1a4a24, and the gate did not re-run them. **The three sentences are re-worded in this folder's `pr-body.md`**
(finding T1): "Three commits on the branch, folded by the squash: the library; a second commit that checks the key ring
at every use and closes the file checks; and a merge of main into the branch that changes no line of the library (the
solution file keeps the projects of both sides)." and "The suite on macOS and on the hosted Linux and Windows jobs (at the
branch head, which also holds main, 762 tests in the solution, 0 failed on each); an independent review's attack program
and its mutants against the library's code, which the merge leaves byte for byte unchanged; ...".

**The second verdict's FOR-RECORDS carried into the pull-request body:** a new section `## Known follow-ups (not fixed
here)` holds its section 3, N1 to N8 in order, N1 first (the DPAPI-NG key-folder item), byte for byte (checked by program)
but for ONE change the text scan required: N8's "the round-1 head" (a round number) became "the first commit of this
branch"; and one re-wrap of that line. Nothing of them went into `squash-body.txt`.

Texts in this folder: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` byte-equal copies of the second verdict's
(`cmp` rc 0 each); `pr-body.md` changed (the two paragraphs above and the new section; `logs/pr-body.diff`); `landing.txt`
NEW: pins 9826559d in `--match-head-commit`; names the three commits beyond main and that 9826559d is a merge whose second
parent is main ddbdf800; the cannot-land paragraph and step 0 are replaced by the record of the resolution (block sha256,
tree `4a6fd850...`, the delta check); the check wait and its reads are kept, re-measured on pull request 4 (12 rows),
pull request 3 (20 rows) and main ddbdf800 (7 rows); the after-merge reads give `total: 762`, `RULES: clean (151 files)`
and the lane folders 21 and 17 files. `FOR-RECORDS.md`: the second verdict's file carried whole (its first 7,232 bytes
`cmp` rc 0 against it) and a section 8 of only what this commit adds.

Each text exported through the workflow's own `neutral_export` (cut by program from `ci.yml` at 9826559d, lines 120 to
128) as the commit message of a scratch repository, then scanned with the workflow's options (scanner 8.30.1): title
alone; title and body; body alone; the squash message with a number; as written; the squash body alone; the repository's
default squash shape (the title and the three commit messages as a list); landing.txt: **each export rc 0, the message
stored whole, scan rc 0, "no leaks found". Control (the squash message with the workflow's planted value): rc 1, "leaks
found: 2".** Word counts over the four texts: ban-list names, B-numbers, ticket keys, clarification ids, seat ids,
"product owner", "gate", "ruling"/"ruled", "decided"/"approved", finding or round numbers, finding/round/gate words, card
ids, control numbers: 0 each (controls 16 of 16 fired); carried from the second verdict's texts and not re-graded:
"review" 2 and "coordinator" 1 in pr-body, "coordinator" 1 in squash-body (R3); host-shaped hits only the footer, the
attribution address and "ASP.NET"; non-ASCII 1, the pull-request footer only.

## Item 5: process

- Heavy jobs: 11, every one through the gate's runner, one at a time, load1 read first (2.18 to 3.68), the lock taken by
  `mkdir` of exactly `.tools/wave1-heavy.lock.d` with `owner.txt`, released by a move into
  `/private/tmp/b1828-gate/_quarantine/locks/` (11 folders there): restore, build, test, five test-project runs, two
  publishes, the restore of the bf1a4a24 archive. **The lock was never waited for** (`lock taken after 0 waits` 11 of 11,
  `logs/gate.log`). After the last job: no dotnet process alive; the lock folder absent; porcelain 0.
- Left in `/private/tmp/b1828-gate/`: `clone/` (detached at 9826559d, porcelain 0, build output ignored), `old/` (the
  bf1a4a24 archive, restored), `out/` (two publishes), `nuget/` (the package-cache copy), `tools/` (the drafter's ten files,
  copied, unedited), `scratch/` (clone, item1, runner, resolve_cmp, item3, item4, texts programs, `texts.py.bak`, the
  planted-control folder, section3.txt), `logs/`, `api/` (the job logs), `dotnet-home/`, `_quarantine/locks/`. In the
  scratchpad: `w.git` (a mirror of the clone, push URL invalid), `m2` (a clone of the mirror, push URL invalid; one trial
  merge, aborted), `texts/` and `texts2/` (scratch repositories and their exports), one used temporary index.
- Nothing pushed, opened, merged, deployed or sent; no ticket; no setting changed. Hosted calls: one clone of the origin,
  and `gh api -X GET` only (refs, pulls, check runs, job records and logs, code-scanning analyses and alerts).
- Slips, said plainly: two Bash calls refused by workspace hooks and re-issued in the allowed form (a `cp` the path guard
  read as a write into the project's package cache: nothing was copied, the copy was then made by a Python read; an
  unquoted command variable); one `sed -i.bak` on the gate's own scratch program `texts.py` (the original kept as
  `texts.py.bak`).

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| T1 | Text (re-worded, re-scanned) | No | Three sentences of the second verdict's `pr-body.md` are made false or inexact by the merge: "Two commits on the branch" (now three, the third a merge of main), "69 tests in the solution" (now 762 at the branch head), "its mutants against this head" (they ran on bf1a4a24; the library's files are byte-equal). | Use this folder's `pr-body.md` (re-worded, N1 to N8 carried, scanned rc 0). The other three texts are byte-equal and true. |
| R1 | Records | No | The builder's `proofs.py` P8 compares the commit's identity with the clone's own config, and its control compares a constant with that config, so it cannot fail on a wrong identity (FAIL in the gate's identity-less clone). The other nine proofs are true proofs. The commit's identity is right (the gate's own check against the checkout). The same defect the print lane's merge check recorded; the kit carried it unchanged. | For the next kit's proof program: compare against the checkout's config, and run the control on a commit with a planted identity. |
| R2 | Records | No | The builder's local NEUTRAL-SCAN line (327 objects) differs from the hosted one (323) by 4 unreachable local objects of the trial and the merge; the gate's fresh clone reads 323; no branch moved. The builder's unproven attribution of the second pair to `git merge --no-commit` is now measured true. | None for the code; a kit that lays the two lines side by side should expect the merge's by-products. |
| R3 | Records | No | The pull-request body says "review" twice and "coordinator" once, the squash body "coordinator" once, carried from the second verdict's texts (its scan did not ban them). The squash body becomes a commit message on main. | A records pass may change that one word of the squash body before the landing; then scan again. |

No Blocker. No Major. The second verdict's findings (N1 to N8) are not re-opened or re-graded; its landing condition (one
commit touching the solution file only, then a delta check) is met by this commit.

## FOUND / TESTED / NOT TESTED

- FOUND: 0 Blockers, 0 Majors, 1 text finding (re-worded), 3 records lines.
- TESTED: the rows above, in the gate's own clone, mirror and scratch, with the project's SDK, the gate's own home and
  package cache, every heavy job under the wave's lock.
- NOT TESTED / NOT RUN:
  - CodeQL for C# (cannot extract on arm64); the hosted code scan has not run on this branch (0 analyses for its ref); it
    runs on the pull request and is the authority.
  - A full restore with the vulnerability audit (the proxy was closed; known-vulnerability status not tested).
  - The 22 fix-round paths and the branch's other paths were NOT re-reviewed: they stand by blob-equality (item 1(d)).
  - Windows locally (the hosted leg is green); the release guard's hash half and `repo_rules.py`'s R5 hash half; the
    docker step of the linux job locally (hosted it is success).
  - Whether GitHub reads the future pull request as mergeable and clean (no pull request exists; expected, UNMEASURED).
  - The builder's `history.md` entry and its STATUS sections beyond those used here.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt.
