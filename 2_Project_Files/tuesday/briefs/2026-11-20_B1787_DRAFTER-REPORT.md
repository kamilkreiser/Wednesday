STARTABLE: YES - after the stamp; the kit is whole, `stamp_check.py` exits 0 (141 claims, 141 measured), and nothing in it waits on an answer. Two things Tuesday must do at the stamp or the seat stops early: write ONE lock path into all four wave-1 kits (slot S6), and accept or change the clone step (no earlier seat ever cloned).

# B1787 DRAFTER REPORT | Datasec / OXPd_2, lane L2, seat X5, WP1.10 logging deny-list

Drafted 2026-11-20, 17:48:40 to 18:03:32 AEDT (clocks by `date`). Read-only drafter. I ran no build and no test.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1787_SEAT-X5_oxpd2-wp110-logging-denylist.md` (73275 bytes, 255 lines, sha256 `33c31efe54ed8cb93a514e5e4b1d4d3563e2fbd56ff670c877f697b592db5ac2` at 18:03:32).
- Sidecar: the same path plus `.measured` (31036 bytes, 141 lines plus a header).
- This report.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1787/` (git-ignored there): `main/` (the 26 files of the origin's `main`, each checked against its blob id), `main_tree.txt`, `jira_OXPD2-15.txt`, `gl/` (the eight scanner rows; holds two synthetic values built by program, never printed), `verify_kit.py`, `sidecar.py`, `stamp_check.out`, two earlier sidecar files moved aside (`measured.skeleton.*`, `measured.filled.*`).

## BLUF
1. The kit cuts WP1.10 to what its plan row names: a logging library whose every sink sits behind a six-class field deny-list, a scanner of log files, and the tests of both with the planted marker of exit test E1.8. Two new folders, two lines in the solution file, two lines in the package file. No job step, no floor change, no fingerprint change.
2. **The dotnet tests do not count toward the unit-test floor.** Read at `main`: `FLOOR=53` (`ci.yml:192`) is compared with the count of the Python step, and the test that holds it counts indented `def test_` lines of `test_*.py` under `build/tests` only (`test_pipeline_controls.py:29`, `:63-70`, `:86-88`). The two fingerprints hold the `secret-scan` and `rules` jobs only. The `linux` and `windows` jobs build and test the whole solution, so a project named in the solution file runs in both legs with no new step.
3. **The repository's own secret scan is the main trap for this lane.** Measured in scratch with the pinned scanner: a token written as one literal in a test file is FOUND (rule `jwt`), and so is a random value under a token-like name (rule `generic-api-key`). There is no ignore mechanism and every run reads every branch, so one such literal reddens all four lanes. The kit makes the seat build real-looking values at run time and use obviously fake literals elsewhere, and scan before every push.
4. The design does not agree with itself on what is on the list (section 5.9 names six classes; weakness W9 adds config, job packets and user e-mails). The kit builds the six and hands the three to Tuesday.

## Facts re-measured (instrument in brackets)
- Origin [`gh api -X GET`, 17:49:26 and 18:02:58]: `main` = `7bf375268b9975ac9ece66579f7471ba7dbab11d`, one parent; one other branch `b1764/wp03-ci-skeleton` at `6e2629bca1762006917e5657c30e407034fdfb12`; open pull requests 0; pull request 1 closed and merged; tags 0. The four workflow check runs on `main` are success; three code-scanning runs are also there.
- Local checkout [git read verbs]: on the old lane branch, local `main` at `7e1a01cf...` (behind), porcelain 0.
- Design documents [sha256, `awk NR==n`]: 13 quotes compared byte for byte, 0 bad; 62 other pointers, 0 bad (`verify_kit.py`; control: a wrong quote reads False).
- Jira `OXPD2-15` [GET, 17:51:05]: Task, Backlog, parent `OXPD2-4`, 0 comments.
- Package source tags [`gh api -X GET` on the public repositories, 17:51:34]: `serilog/serilog` `v4.4.0`; `serilog/serilog-sinks-file` `v7.0.0`.
- Package cache [`ls`]: 62 folders, none for the two packages.
- Toolchain [`--version` by path]: project dotnet 10.0.404; gitleaks 8.30.1; git 2.54.0; python3 3.14.10.
- Prior work [grep with a positive control, files read and never run]: the deployment utility's 6 project files hold 8 package references, none a logging library; 0 of its 97 `.cs` files name the host's logger interface. The earlier OXPd 1 solution: 11 of 14 `.java` files print to standard output.
- Records files [line and byte counts]: at 17:48 the runbook read 100 lines and 18645 bytes; at 17:55 and again at 18:02:58 it read 101 lines and 23227 bytes; `BACKLOG.md` 215 lines (131 in the earlier kit); `history.md` 44 lines (22). So the records seat rewrote all three while I drafted. The kit cites them by fragment only; every fragment counted at 18:01 and 18:02:58.
- Neighbours: one `OXPd2` pane at 17:54 (`Datasec/OXPd2-R286`), none at 18:02:58; `.tools/` holds no `b1787` and no other wave-1 folder yet. Load1 between 2.83 and 5.38 on 18 CPUs.

## Where the lane plan's row no longer matches the documents
- The plan says `03:157`; the row is now `03:161` (the commission's own number is right).
- The plan says `02:536` for the logging sentence; it is now `02:567` (section 5.9, heading `02:565`).
- The plan cites the readiness table at `05:155-166`; the WP1.10 row is now `05:229`.
- The wording of the row and of the three sentences is unchanged. The plan's "no" in the column "scope about to change" still holds.
- Not in the plan and found by reading: the six-against-nine difference between `02:567` and `02:689`; requirement F77 (`02:165`) binds this package (the debug switch's output is under the list).

## Corrections to the commission
1. "the way the three seats before it did": **no earlier seat cloned.** All three worked in the project's checkout itself (their STATUS Step 0 reads `checkout | HEAD ...`). A clone made with the deploy key has never been done here. The kit has the seat clone and copy the three local git values by program (Question Q10); that step is UNMEASURED.
2. "Open pull requests: 0" is right, but the old lane branch still exists on the origin, and `main`'s commit now carries seven check runs, not four (code scanning added three). The kit tells the seat to require the four by name.
3. The commission names three shared files. **`README.md` is a fourth that this wave makes stale** (its Layout list and its Reserved names list, `README.md:53`). The kit leaves it alone (Q9); four lanes editing those lists would conflict four times.
4. `03` line 161 as the commission says: confirmed. The test strategy's rows are at `03:239` (security) and `03:241` (red-control).
5. The commission asks for a `dotnet test --filter` checked against test names. The repository's runner is `Microsoft.Testing.Platform` with `xunit.v3` (`global.json`), whose selector syntax I could not measure without running it. **The kit carries no selector at all** and makes the seat run the whole solution and stop on a total of 0 or a total equal to the base's.

## D-decisions written into the kit (each Tuesday's to confirm)
D1 two projects; D2 two packages pinned exact; D3 six classes and 21 name stems as data in one file; D4 "contains a stem" after normalising; D5 the value replaced by `[removed:<class>]`; D6 no way to switch the list off; D7 the scanner is value-first, five forms, one RFC 7519 shape, no vendor format; D8 a scan that read nothing is not clean; D9 the scanner never repeats a value; D10 no job step; D11 one commit; D12 one history entry, nothing else in the shared records.

## Questions for Tuesday, each with its default and the line that leaves it open
- Q1 the cut (`03:161`): default library, list, scanner, tests; host wiring, exporter, correlation id, support bundle OUT.
- Q2 the classes (`02:567` six, `02:689` three more): default six. **User e-mail addresses in logs is a product decision** (an audit line, `02:150`, may need to say who signed in).
- Q3 the stems (the design names no field): default the 21 in the kit. The other lanes' code must use these names, so Tuesday may want to fix the list across the four kits.
- Q4 the packages (`02:567` "Serilog to file"): default `Serilog` `[4.4.0]`, `Serilog.Sinks.File` `[7.0.0]`.
- Q5 the replacement text (no wording in the design): default `[removed:<class>]`. **A word a customer's administrator may read.**
- Q6 matching: default contains. Q7 deny-list or allow-list (`02:141`): default deny-list as written.
- Q8 scanner forms (`03:88` names none): default five forms and one shape.
- Q9 README: default untouched. Q10 the clone: default the seat makes it. Q11 a `main` that moves after the push: default report only.
- Q12 the lock: default a `mkdir` folder, path in slot S6. Q13 records: default one history entry. Q14 windows: 180 and 150 minutes.

## For Tuesday, not decided by the kit
- A possibly customer-facing word: the replacement text (Q5).
- A product decision: whether a user's e-mail address, a job packet or configuration may be logged (Q2).
- A design gap: a value under an unlisted name, or inside an exception's message, is stopped by nothing before the sink; only the scan sees it afterwards. The kit makes the seat prove that as a test (S08) and say it plainly. Whether the design wants more (an allow-list) is Q7.
- The list protects nothing until a later lane wires it into the host, which is not this lane's folder.
- Nothing here is a question for HP.

## The exact lines the seat adds to the shared files
`Datasec.Suite.slnx`, inside `/src/` after the Core line:
```
    <Project Path="src/Datasec.Suite.Logging/Datasec.Suite.Logging.csproj" />
```
and inside `/tests/` after the Core.Tests line:
```
    <Project Path="tests/Datasec.Suite.Logging.Tests/Datasec.Suite.Logging.Tests.csproj" />
```
`Directory.Packages.props`, between the two existing package lines:
```
    <PackageVersion Include="Serilog" Version="[4.4.0]" />
    <PackageVersion Include="Serilog.Sinks.File" Version="[7.0.0]" />
```
`.github/workflows/ci.yml`: nothing. Rule for the place of a line: alphabetical order of the path or package id. The other three drafters may have chosen another rule: Tuesday should make the four kits agree.

## Reading load of the seat (bytes, by program at 18:03)
Kit 73275 + `CLAUDE.md` 10052 + `CLARIFICATIONS.md` 33300 + `SETUP_RUNBOOK.md` 23227 + `ci.yml` 8911 + `test_pipeline_controls.py` 5856 + `README.md` 5847 = **160468 bytes**. The design documents are read by named lines only. The runbook's size is moving.

## Chain inputs (each input exists at the base or is made by an earlier step)
| Step | Inputs | Where each comes from |
|---|---|---|
| 0 | the stamped kit | Tuesday |
| 1 | the origin; the checkout's three local git values; the deploy key; project dotnet; the reports | exist now (measured), the clone itself is new |
| 2 | the clone and branch; the three frozen blocks | Step 1; the Step-0 copy |
| 3, 4 | the two projects restored and building | Step 2 |
| 5 | green tests; `run_step.py` of the earlier seat | Steps 3 and 4; exists (sha256 in FACT 10) |
| 6 | the staged tree; the commit | Step 5; Step 6(a) before 6(b) |
| 7 | the pushed head and its green run | Step 6 |

## UNMEASURED
- Everything `dotnet` prints for this lane: the restore of the two packages, their transitive packages, whether the core package holds a JSON formatter, the build, the tests, the test summary's shape with two test projects.
- That the package feed holds exactly versions 4.4.0 and 7.0.0 (derived from the source tags).
- A clone with the deploy key.
- The Windows leg for file-writing tests.
- Whether a lane-branch push gets code-scanning runs.
- Whether the SDK leaves a build server alive after a build.
- The lock: proposed, never used.
- The commit subject as a commit object under the neutral scan (as a file it is clean).
- What the other three drafters wrote (not read, by instruction).

## What I did not read
- The form kit B1779: read whole (335 lines). The first kit B1764: only its sections THE LAYOUT and THE CHECKS (lines 49 to 97) and its HEAVY section; not the rest.
- The B1779 STATUS: lines 1 to 40 and a heading list only. The B1764 and B1774 STATUS files: grep lines only.
- `02`, `03`, `05`: the lines that mention logs (found by program) and the sections around them; not whole.
- `CLARIFICATIONS.md`: C-42 to C-45 only.
- `BACKLOG.md`, `history.md`: sizes and one fragment; not read.
- `FOR-RECORDS.md`, `SETUP_RUNBOOK.md`, the project `CLAUDE.md`, `DRAFTER_RULES.md`, the lane plan: whole.
- The analysis reports: the cited lines only. Reports A6, A8, A9, A11, B1 to B3, C1, C2: not opened beyond a line-number grep.
- The NAS library: not opened (this lane ports nothing).
- The model-routing table: line 108 only. The gate-verifier standard: not opened (cited as the form kit cites it).

## Outside the fences
- I wrote only the kit, its sidecar, this report and my scratch folder. No git write, no Jira write, no GitHub write.
- GitHub GETs beyond the project's repository: the release lists of four public Serilog repositories (no project detail in the request).
- I read file NAMES and package names under `Source_Documents/` for the prior-work counts (grep with `-l` and `-o` on package ids); no secret value was displayed.
- One slip, harmless: my first shell loop used a variable named `path`, which broke the shell's command lookup for that one command; it created empty files only inside my scratch folder, later overwritten by the real copies.
- I ran `gitleaks` eight times on scratch files. That is a scan, not a build or a test.
