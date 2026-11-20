STARTABLE: YES - the kit is whole, `stamp_check.py` exits 0 (130 claims, 130 measured), every pointer is checked by program (0 mismatches); but the drafter ran no build and no test, so the clone set-up, every `dotnet` result and all behaviour of the Data Protection library are UNMEASURED until the seat runs them, and three points need Tuesday at the stamp (the heavy lock's one path for all four kits, Q2 on "sealed", the base sha).

# B1789 drafter report | lane L4, seat X7, WP1.1 cut to the local secret store

Drafted 2026-11-20, 17:48 to 18:05 AEDT (clocks by `date` in each command). Files:
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1789_SEAT-X7_oxpd2-wp11-local-secret-store.md` (78,924 bytes, 285 lines, 0 non-ASCII bytes, 8 lines holding a slot).
- Sidecar: the same path plus `.measured` (130 claim lines, then the pointer rows, the scanner rows, the message row, the Jira row).
- This report.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1789/` (git-ignored there: `check-ignore` rc 0).

## BLUF
1. The kit has the seat build ONE library and ONE test project (`src/Datasec.Suite.Secrets`, `tests/Datasec.Suite.Secrets.Tests`): a secret store behind one interface, its local provider on ASP.NET Core Data Protection, key-ring protection by DPAPI-NG on Windows and by an owner-only key file on Linux, round trip, rotation, re-wrap, revocation. Fifteen controls K01 to K15, each red first by a named mutant.
2. Shared files: TWO lines in `Datasec.Suite.slnx`; NO line in `Directory.Packages.props` (a framework reference, not a package); NO line in `ci.yml`. The floor and both fingerprints do not move.
3. The kit says in its BLUF that `OXPD2-12` stays open and lists what is left of WP1.1.
4. The kit carries NO frozen code and no test filter: the drafter may not compile, so the contract is stated by property and every library behaviour is marked UNMEASURED. That is weaker than the form kit, whose texts were dry-run. It is the honest shape for a kit drafted without a build.

## Facts re-measured (instrument, result)
- Origin by `gh api -X GET`, 17:49:18, 17:55:50, 18:03:49: `main` = `7bf375268b9975ac9ece66579f7471ba7dbab11d`, one parent; open pull requests 0; pull requests of any state 1 (merged); tags 0; heads: `main` and the merged `b1764/wp03-ci-skeleton` at `6e2629bc...` (still on the origin). Check runs of `main`: 7 (the four `ci` jobs `success`, `Analyze (csharp)` and `Analyze (python)` `success`, `Adjust Configuration` `skipped`).
- Tree of `main`: 39 entries, 26 files; 20 files fetched into scratch `main/` and read.
- The floor: `FLOOR=53` counts indented `def test_` lines in `test_*.py` under `build/tests` only (`test_pipeline_controls.py:63-70`, `:86-88`; `ci.yml:192-196`). A dotnet test does not count. Read, not run.
- The hosted test step passes on any one `total: +[1-9]` line (`ci.yml:46`, `:76`): the existing project's `total: 1` would hide a new project that ran nothing. The kit makes the seat read its own assembly's summary from each log.
- Project checkout: on `b1764/wp03-ci-skeleton` at `6e2629bc`, local `main` `7e1a01cf` (stale), porcelain 0.
- Toolchain: `.tools/dotnet/dotnet --version` `10.0.404`; shared framework and reference pack `10.0.15`; package cache 62 entries with `xunit.v3` 4.0.3 and the 10.0.15 runtime packs; gitleaks 8.30.1.
- Library names: 17 Data Protection names, 3 runtime names, 3 test-framework names counted in the SDK's and the cache's `.xml` files, each at least 1, a made-up name 0.
- Scanner shapes: 12 sample lines (`gl_probe.out`): random hex or base64 beside a key word fires `generic-api-key`; a PEM header fires `private-key`; fake words, counted bytes and run-time random are quiet.
- Commit subject: 107 bytes; rc 0 as text shaped like an exported commit, rc 1 with a planted token (emulated headers, NOT through the workflow's function).
- Jira `OXPD2-12` by GET: Task, Backlog, parent `OXPD2-4`, 0 comments.
- Records files at 18:03:49: `BACKLOG.md` 215 lines, `SETUP_RUNBOOK.md` 101, `history.md` 44 (the form kit counted 131, 100, 22). Between 17:55:50 and 18:03:49 none of the three changed size. The three runbook fragments the kit cites each count 1. The runbook's Jira sentence now reads 24 issues.
- Load1 6.38, 5.16, 1.79 on 18 CPUs; 1023 GiB free; one live pane, `Datasec/OXPd2-R286`.

## Chain steps and their inputs (each input exists at the base or is made by an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit; `CLAUDE.md`; `CLARIFICATIONS.md`; the three design files | exist |
| 1 | `<repo>`'s three local settings; the deploy key; the origin; `run_step.py` of B1779 | exist (FACT 2, 11) |
| 2 | `<clone>`; `.tools/dotnet`; `.tools/nuget-packages` | Step 1; exist |
| 3 | the two frozen slnx lines | the Step-0 copy |
| 4 | the tests of Step 3 | Step 3 |
| 5 | the staged tree; the runner copy; `build/repo_rules.py`, `build/release_guard.py` in the clone; `Source_Documents/` (hash half) | Steps 1, 4; exist |
| 6 | the commit; the origin's `main` | Step 5; GET |
| 7 | the pushed head; job logs | Step 6 |
| 8 | `neutral_export` cut from the clone's `ci.yml` (lines 120 to 128 at `main`) | Step 1 |
| 9 | `history.md` | exists (being rewritten: read-compare-replace) |

## D-decisions the kit takes as defaults (all Tuesday's to confirm): D1 to D14 in the kit. The ones with weight
- D2 no package (framework reference). D5 the Linux key file is owner-only, AES-256-GCM over the key ring through the library's own extension point, and NOT sealed. D4 DPAPI-NG for the current account. D7 records are files behind an interface. D6 one key ring per partition. D9 a failed read throws, never an empty value.

## Q-questions for Tuesday (each with its default and the line that leaves it open)
- Q1 package or framework reference (`02:375`): framework reference.
- Q2 what the Linux "sealed key file" is (`02:375`, `02:560`, `02:926` say the words and nothing more): owner-only file now, sealing left and named as a limit. This is also item 1 of the kit's NOT DECIDED list: it is a design definition, possibly the Datasec team's.
- Q3 DPAPI-NG descriptor (`02:560`): the current account, an option.
- Q4 where ciphertext lives (`02:377` lists no secrets in the database): files.
- Q5 separate key for the most valuable store (`02:617`): partitions.
- Q6 keep the previous version (`02:131`, `02:616`): no.
- Q7 key lifetime: the library's 90 days (its `.xml` line 1541).
- Q8 algorithms: the library's defaults (UNMEASURED which).
- Q9 history entry by the seat: yes, read-compare-replace.
- Q10 the heavy lock: `<project>/.tools/wave1-heavy.lock`, a folder taken by `mkdir`. **It only works if all four wave-1 kits name the same path: Stamp slot S4.**
- Q11 rebase before the push only. Q12 240 and 180 minutes. Q13 pane `Datasec/OXPd2-X7`. Q14 gate G1 with a second reader of the D5 code.

## Where the lane plan's row no longer matches the documents as they stand
- The plan row is `03:152`, not `03:148`; the size scale is `03:131`, not `03:128`.
- C15 is `02:375`, not `02:344`; the readiness row is `05:226` (the table is `05:220-232`, not `05:155-166`).
- Flag 3 is stale: report A10 IS in the project folder (47,701 bytes).
- The C-43 flag is narrower, not closed: the corrected `02` section 8.7 (from line 848) keeps the probe result "in the server's device registry (C1)" (`02:877`) and sends each printer's password to the server's C15 (`02:880`, row 10 of that table); it does not say the utility's own entity projects share the registry. The cut still stands on it.
- The plan's "seeded" point on the Windows provider ("can only be tested on the Windows leg") holds; the kit builds on it.

## Corrections to the commission
1. "Start its seat from the origin's main in the seat's own clone or worktree, the way the three seats before it did": the three build seats worked in `<repo>` itself (B1764 kit line 343 `switch -c` in `<repo>`; B1779 STATUS "Trees left": `<repo>` on the lane branch). No seat has made a clone. The kit writes the clone procedure new (Step 1); it is UNMEASURED as a whole.
2. Consequence the commission does not name: in a clone under `.tools/`, `build/repo_rules.py` looks for the supplied source beside the clone and would print that the hash half was NOT RUN. The kit passes `--source-documents`.
3. "Its four `ci` check runs success": true, and three more check runs exist on that commit (two CodeQL, one skipped).
4. Item 8 asks that a `dotnet test --filter` be checked against names: the kit carries no filter at all. The runner is Microsoft.Testing.Platform (`global.json`), whose filter syntax the drafter could not run; a whole-solution run is the one command already measured by the earlier seats.
5. Item 4 (the lock): there is none (both earlier kits say so). Proposed in HEAVY.
6. The origin still holds the merged branch `b1764/wp03-ci-skeleton`: every lane's `secret-scan` reads it too.

## The exact lines the seat adds to the three shared files
- `Datasec.Suite.slnx`, after line 4: `    <Project Path="src/Datasec.Suite.Secrets/Datasec.Suite.Secrets.csproj" />` (78 bytes, sha256 `5938754381eb9dbaa8877eb9f3e4c5181da29f2ef0b8d03798b83e1a241e1a5a`).
- `Datasec.Suite.slnx`, after line 7: `    <Project Path="tests/Datasec.Suite.Secrets.Tests/Datasec.Suite.Secrets.Tests.csproj" />` (92 bytes, sha256 `07777311d3c63373702e316732f89676d3ff14a455afdd7e64821249cad56fbf`).
- `Directory.Packages.props`: none. `.github/workflows/ci.yml`: none.
All four lanes insert after the same two anchor lines, so every later lander meets a conflict of adjacent added lines: the kit's rebase rule covers exactly that shape.

## Reading load (bytes, by program)
READ WHOLE by the seat: the kit 78,924; `CLAUDE.md` 10,052; `ci.yml` 8,911; `test_pipeline_controls.py` 5,856; `Directory.Build.props` 834; `Directory.Packages.props` 319; `Datasec.Suite.slnx` 331; `global.json` 135; `.gitignore` 287; the three files of the existing projects 136, 342, 272. **Total 106,399 bytes.** By pointer only: 21 design lines, three clarification entries, one runbook section. No stamped kit of Tuesday's is on the list.

## UNMEASURED (the drafter ran no build and no test)
- The clone procedure; that the base builds and tests green inside a clone; that the restore fetches nothing.
- That a class library with a framework reference to `Microsoft.AspNetCore.App` builds, restores in locked mode and tests on both hosted jobs; what its lock file holds.
- Every behaviour of Data Protection the controls rest on: whether a new key is used at once by a running provider; whether a revoked key makes the plain unprotect throw; how a custom decryptor type is named and constructed; what happens at start when one key cannot be decrypted; the default algorithms of 10.0.15.
- DPAPI-NG on a GitHub `windows-latest` runner's account.
- The layout of the test summary for a solution with two test projects; the skip syntax of the test framework in use.
- Whether macOS git matches the `*keystore*` ignore pattern without regard to case.
- `MSBUILDDISABLENODEREUSE=1` and `-m:4` as the kit uses them.
- The commit subject through the workflow's own function (emulated only).
- How long the lane takes; how four seats behave on one package cache at once.
- Whether the other three kits name the same lock path (their files were not read).

## What the drafter did not read
- The other three lanes' kits, reports and scratch folders.
- `02`, `03`, `05` whole: only the lines found by program (printed into scratch `design_lines.txt`, `design_62.txt`) and the heading list of `02`.
- The first kit (B1764) beyond its lines 34 to 76, 312, 347 and 370; its sections THE CHECKS, THE FROZEN TEXTS, THE WORK, Stamp were not read. B1779's kit was read whole. B1779's STATUS: its heading list and lines 283 to 334 only.
- Reports A1, A5, A7, A10: the lines a grep returned, not the reports. A10 one line only.
- `CLARIFICATIONS.md` beyond lines 268 to 315. `BACKLOG.md` and `history.md` (sizes only). The B1785 kit (two grep hits and the head of its sidecar).
- Nothing under `Source_Documents/`, nothing in the library on the NAS, no keystore, nothing of the HPSM project or of another client.

## Outside the fences: disclosure
- Wrote only the kit, its sidecar, this report and the scratch folder. No git write, no Jira write, no GitHub write, nothing sent.
- Ran `gitleaks dir` on files the drafter's own programs made in scratch (12 sample lines, one message file, one planted control): an instrument read, not a build or a test of the project. Two scratch folders (`gl_probe_175340`, `msg_probe_180152`) hold random fake values and the workflow's planted token joined from its two halves; none is a credential; none was printed; the folder is git-ignored.
- Read `4_Credentials/.env` in-process for ONE Jira GET (`OXPD2-12`); read the three local git setting NAMES of `<repo>` with the values cut off before display. No value was printed or copied.
- One git verb outside the drafter rules' list: `check-ignore` in Tuesday's own tree (a read) and `config --local --get-regexp` in `<repo>` (a read).
- Read two files of other seats' lane folders: the first 25 lines of `.tools/b1779/scratch/run_step.py` and the first 1,500 bytes of the B1785 sidecar copy (for the form).
