STARTABLE: YES - the kit stands on its defaults; one of them (Q1, which Workpath decoding family is the default per reader id) is a point Tuesday should read before the stamp, and it does not block the build because both families are built.

# B1786 DRAFTER REPORT | Datasec / OXPd_2, lane L1, seat X4, work package WP1.3 (card decoders)
Drafter: read-only, Fable, commissioned by Tuesday (seat s299). Drafted 2026-11-20 17:48 to 18:08 AEDT (clocks by `date`). No build and no test was run. Marks as in the kit.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1786_SEAT-X4_oxpd2-wp13-card-decoders.md` (86,504 bytes, 330 lines; 8 unfilled Stamp slots; `stamp_check.py` rc 0: 167 claims, 167 measured).
- Sidecar: the same path plus `.measured` (167 lines and a header; 53 of them say "nothing to run": names, paths and prose the kit defines, not expectations).
- This report.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1786/` (the model `model.py`, `vectors.py`, `cross.py`, `parity.py`, `pointers.py`, `assemble.py`, `sidecar.py`, `jira_get.py`; `main/` = the 26 files of the origin's `main` fetched by GET; `gl/` = the scanner probes; `kit_body.md`).

## BLUF
1. The lane is a pure C# library and its tests, in two new projects, plus two lines in the solution file. No package, no workflow change, no change of the unit-test floor or of a fingerprint.
2. **A finding the design does not state.** The Workpath app has TWO decoding families, chosen by firmware. The per-reader decoders that `02:368` and decision D9 (`02:907`) call "the Workpath decoders for the four reader ids" are the OLDER family (`PrinterAccessoryService.kt:258-401`). On Android 12 firmware the app skips them (`:173-177`) and decodes through `ReaderDataStore.kt`: the HP vendor as whole-buffer text, EVERY other vendor (RF IDeas and Elatec too) through the generic keyboard routine. The app version in the library has `minSdk = 31` (`app/build.gradle.kts:26`), so that version can only run where the newer family decodes. The two families do not give the same string for every input (kit block X: 13 inputs, 6 the same, 7 different; for example a byte 13 from the HP reader ends the card in the older routine and stays inside the string in the newer one). "UUID dashes removed" (F4, `02:67`) exists only in the newer family. Which family stored the cards of today's customers is not in any document I read. The kit builds both and keeps the design's sentence as the default; **the question belongs on the Datasec team's list** (C-45's first list), not with a seat.
3. Golden values are PROVISIONAL and say so in the golden file itself. They were computed by my own model of the five routines (41 vectors, block V). The model agrees with the three input and output pairs of the Workpath app's own unit test (newer family only; values never printed). The older family has no such pair: its vectors rest on reading alone.
4. The kit defines the reassembly rules (window, hole, unfinished read, cap) because the design gives one clause and the Workpath code has none beyond dropping a repeat. Each rule is a Question with a default and its source.

## Facts re-measured (instrument; clock)
- Origin: `main` `7bf375268b9975ac9ece66579f7471ba7dbab11d`, one other branch `b1764/wp03-ci-skeleton` `6e2629bc...`, open pull requests 0, any state 1 (`gh api -X GET`, 17:49:16 and again 18:07:43: unchanged). Tree of `main`: 26 files.
- Shared checkout `2_Project_Files`: branch `b1764/wp03-ci-skeleton`, local `main` `7e1a01cf...` (stale), porcelain 0 (git read verbs, 17:54).
- Design files: `02` 1126 lines, `03` 529, `05` 266, file time 14:01 on 2026-11-20. 90 pointers of the kit checked by program against their lines: 0 bad (control: a wrong line fails).
- `OXPD2-13` by GET at 17:52:14: Task, Backlog, 0 comments, parent `OXPD2-4`.
- Seven library source files: sizes and sha256 in the kit's table (`ls -l`, `shasum`, 17:50 to 17:52). The library was mounted throughout.
- Floor and fingerprints (read at `main`, `build/tests/test_pipeline_controls.py` 119 lines, `ci.yml` 199 lines): `FLOOR=53` is compared with the count of indented `def test_` lines of `build/tests/test_*.py` only; the fingerprints cover the `secret-scan` and `rules` jobs only. **The dotnet tests do not count toward the floor.** The `linux` and `windows` jobs run `dotnet test -c Release --no-build` over the solution and need `total: +[1-9]`.
- Scanner (gitleaks 8.30.1, the workflow's options, scratch probes, 17:53): lower-case hex test literals rc 0 in five shapes; flagged: a mixed-case 32-character literal under a name ending `Key` (1 of 1) and 32 upper-case hex characters after the word `token` (20 of 30). The proposed commit subject (90 bytes): rc 0. Planted control rc 1.
- Toolchain: project dotnet `10.0.404` (a version read only), gitleaks `8.30.1`, git `2.54.0`, `/usr/bin/lockf` present and measured on a scratch file (second holder rc 75).
- Machine: load averages 6.58 5.30 4.07 (17:52:55); 1023 GiB free.
- **The three records files moved while I drafted** (17:48 then 18:07): `SETUP_RUNBOOK.md` 100 lines 18,645 bytes then 101 lines 23,227 bytes (its Jira sentence now reads 24 issues, `OXPD2-20` to `OXPD2-24` filed); `BACKLOG.md` 131 lines 13,826 bytes then 215 lines 26,514 bytes (the row of `OXPD2-13` is now at a new line); `history.md` 33 lines 8,437 bytes then 44 lines 11,616 bytes. The kit cites them by fragment only (`One heavy dotnet job at a time` counts 1 at 18:07). The pane `Datasec/OXPd2-R286` was live at 17:54 and no pane holding `OXPd` was listed at 18:07.

## Decisions written into the kit (each a default; Tuesday's at the stamp)
D1 both families built, selection `DesignDefault` (Q1). D2 the two conditional ids are in the table and NOT enabled (the plan row: "only if S3's first step passes"). D3 own clone under `.tools/b1786/clone`, identity and ssh line copied from the shared checkout by program. D4 no test filter (the SDK runs the newer test platform; a filter literal could not be checked without running a test). D5 the seat writes no records file and no Jira (Q9). D6 rebase allowed only before the first push, only for side-by-side added lines in the solution file. D7 a machine lock by `lockf` (Q11). D8 the three Workpath test pairs are used in the seat's scratch only (Q7). D9 `CardValidator.kt` is not opened by the seat.

## Questions with defaults (source line beside each)
- Q1 which family per reader id: default the design's sentence (`02:368`, `02:907`); alternatives in the kit. Facts: `PrinterAccessoryService.kt:173-177`, `ReaderDataStore.kt:43-47`, `build.gradle.kts:26`.
- Q2 window 1000 ms (`02:368`; report C2 line 98). Q3 a hole or an unfinished read refuses the whole read, cap 256 (report A7 lines 217, 380).
- Q4 UUID step: canonical 36-character form only (`ReaderDataStore.kt:25-30`); what else Android's parser accepts is UNMEASURED.
- Q5 a 2-byte report for 3111:15354: refusal `MalformedReport` (`PrinterAccessoryService.kt:504-507`: the source reads past the end). Q6 bytes above 127: refusal `OutsideAscii` (`:384`, `ReaderDataStore.kt:44`).
- Q7 the Workpath unit-test pairs stay in scratch. Q8 names. Q9 no records file. Q10 README Layout untouched. Q11 the lock. Q12 180 and 140 minutes, pane `Datasec/OXPd2-X4`, gate G2.

## Not decided by the kit: for Tuesday (customer-facing, product or HP)
1. Q1 above: a question for the Datasec Workpath team (which app versions and firmware enrolled today's cards).
2. Whether the three card values in the Workpath unit test are test values or real cards (they sit in a source tree; the kit treats them as possibly real).
3. A string over 32 bytes, a hole or an unfinished read each give a refusal: what the user SEES is WP1.4's and a product wording, not this lane's.
4. The growth step of the sequence number on the newer printers is not stated in report B2 (line 210: "monotonically increasing"): a point for HP's list or for the first run on a printer. The kit makes gap detection an option for that reason.

## Where the lane plan's row no longer matches the corrected documents
- Its pointers moved: WP1.3 is `03:154` (plan: `03:150`); the golden-files sentence is `03:233` (plan: `03:228`); the logging sentence is `02:567` (plan: `02:536`); component C12 is `02:372` (plan: `02:341`).
- The corrected row adds "the two other ids only if S3's first step passes"; the plan's row does not carry it.
- "Scope about to change? no": the row is right about the pending correction pass, but point 2 of the BLUF is a scope question the plan could not see (the drafter of the plan did not open the library).
- "Needs NO key": confirmed. The key literal lives in `util/CardValidator.kt` lines 9 to 12, a file the decoders do not use.
- Difference 4 of the plan (goldens PROVISIONAL) stands and is carried.

## Corrections to the commission
1. "the way the three seats before it did": the three earlier build seats worked in the shared checkout itself; no seat has made a clone under `.tools/<brief>/`. The clone step is new and UNMEASURED.
2. "the lock the earlier seats used": there is none (both earlier build kits say "No lock file").
3. "A lane that adds tests changes the unit-test count": not the count the floor reads (measured above).
4. The decoder source is cited by reports A1 (section 4.11) and A7 (section 4.4), not by A3 or A8 (one passing mention each); A4 lines 173 and 281 name it.
5. `SETUP_RUNBOOK.md` is at the project root, not beside the STATUS in `Briefs/`.
6. "a `dotnet test --filter` is checked against the test names": this SDK runs the newer test platform (the first lane's fault 1); the kit carries no filter.

## The exact lines the seat adds to the three shared files
- `Datasec.Suite.slnx`: `    <Project Path="src/Datasec.Suite.Cards/Datasec.Suite.Cards.csproj" />` directly before the Core line (line 3 at `main`), and `    <Project Path="tests/Datasec.Suite.Cards.Tests/Datasec.Suite.Cards.Tests.csproj" />` directly before the Core tests line (line 7 at `main`). Rule offered to the other lanes: ascending order of path inside each folder.
- `Directory.Packages.props`: no line (`xunit.v3` `[4.0.3]` is already pinned at line 7).
- `.github/workflows/ci.yml`: no line.

## Reading load (by program, 18:07)
READ WHOLE list of the kit: 180,871 bytes in 16 files: the kit 86,504; `CLAUDE.md` 10,052; `CLARIFICATIONS.md` 33,300; `SETUP_RUNBOOK.md` 23,227 (growing); `ReaderDataStore.kt` 4,510; eleven small files of the clone 23,278 in all (`ci.yml` 8,911, `test_pipeline_controls.py` 5,856, `README.md` 5,847 the largest). Read in part only: six source files (about 230 lines), three report ranges, the quoted design lines.

## Chain steps and their inputs (each input exists at BASE or is made by an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit | Tuesday |
| 1 clone, extract | origin `main`; the shared checkout's local configuration (3 names); the Step-0 copy | BASE; exists (presence of the 3 names UNMEASURED by me: a REFUSE check); Step 0 |
| 2 reading | the seven library files | exist (sha256 in the kit) |
| 3(a) files | extracted T1, T2, T3, V, X; `Datasec.Suite.slnx` | Step 1; BASE |
| 3(b) restore, build, test | the two project files, stubs, tests; `.tools/dotnet`; `.tools/nuget-packages` | 3(a); exist |
| 3(c) port | the reading | Step 2 |
| 3(d) chain | lock files; `build/release_guard.py`, `build/repo_rules.py`, `build/tests` | 3(b); BASE |
| 4 checks | staged tree; `run_step.py` of the third seat; the ban list file | 3; exist (7,408-byte standard, the runner's sha256 in the sidecar) |
| 4(f) parity | the built assembly; `AccessoryReceiverTest.kt` | 3(c); exists |
| 5 commit, push, hosted | the checks; the deploy key through the clone's ssh line | 4; Step 1 |

## UNMEASURED (said plainly; the drafter ran no build)
Everything `dotnet` prints for the two new projects (restore fetch count, the lock files, warnings, the test summary with two test projects); T2 and T3 as a build; the clone procedure; the hosted run (Linux and Windows legs, `RULES: clean (<n> files)`); whether four seats restoring into one package cache collide; `ls-remote` over ssh; the older family's vectors against any Workpath-authored value; the Android UUID parser's leniency; the platform character set for bytes above 127; how the Workpath platform fills one event's buffer; the sequence step on the newer printers; which family today's fleets ran; whether the unit-test card values are real; the size of the lane in hours.

## What I did not read
The first kit (`B1764_SEAT-X1`): lines 49 to 98 (THE LAYOUT, THE CHECKS) and 306 to 376 read; lines 1 to 48, 99 to 305 and 377 to 407 NOT read. `02`, `03`, `05`: only the lines found by program for this package (about 30 lines), not whole. `CLARIFICATIONS.md`: C-41 to C-47 only. Reports: A1 lines 278 to 300, A7 195 to 224 and 376 to 382, grep hits of A4, A6, A10, B1, B2, C1, C2; none whole. `B1779_STATUS.md` and `B1764_STATUS.md`: grep hits only. The B1785 kit: not read. `FOR-RECORDS.md`, the lane plan, the form kit B1779, `DRAFTER_RULES.md`, the project `CLAUDE.md`, the runbook (as of 17:48): whole. Workpath source: the ranges in the kit; `ReaderOutputProcessor.kt` lines 1 to 100, 360 to 385 and 626 to 649 only; the Workpath test `ReaderOutputProcessorTest.kt` lines 1 to 100 (set-up only). The other three lanes' files: none.

## Outside the fences: disclosure
- I opened `util/CardValidator.kt` lines 1 to 100 while looking for the 32-byte limit, and its key literal was shown to me by the Read tool. I wrote it nowhere: not in the kit, the sidecar, this report or any scratch file (a scan of the kit for its first four characters counts 0). The kit tells the seat not to open that file.
- I ran, in my scratch folder only: the scanner on files of random values I built; `/usr/bin/lockf` on a scratch file; `dotnet --version` (a version read); my own Python model. I ran nothing from the library or from `Source_Documents/`, no build, no test, no git write, no Jira write (one GET), no GitHub write (GET only), and sent nothing to anyone.
- One command of mine was refused by a hook (an unquoted separator starting with `=`) and re-run with a different separator.
- The kit holds 5 non-ASCII characters (the section sign, inside three verbatim quotes of the design); the frozen blocks are ASCII.
