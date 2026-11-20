STARTABLE: YES - once stamped; the kit is whole (323 lines, 83962 bytes before the stamp), `stamp_check.py` exits 0 (113 claims, 113 sidecar lines), and no fix in it has been built or run by anyone.

# B1798 DRAFTER REPORT (OXPd 2, WP1.10 round 2 of 2, seat X8)

Written 2026-11-20 by the read-only drafter (Fable, in-session). The session was stopped once by a usage limit after its reads and before any file was written; the kit was then written in two passes (a partial with a clear last line, then the rest) and that partial marker is gone (checked by program).

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1798_SEAT-X8_oxpd2-wp110-round2-denylist-fixes.md`, sidecar `.measured` beside it. 8 lines hold a stamp slot (S1 to S7 and the last line). 0 non-ASCII lines.
- **Nothing in the kit is proven by a run.** I ran no build and no test (the wave's lock was free, but the commission forbids both). Every "after" column, every "RED under mutant" cell and the whole mechanism are DERIVED from source reading. This is the main risk of a capped round: the seat's Step 2 reproduces the review's table before it changes product code, and Step 3 is where the design meets the compiler.
- Finding 1 is fixed by property, not by a list of types: a SIBLING rule (a member or element is replaced when a neighbour's VALUE is a listed name) plus a TEXT rule (a scalar holding a listed name, a separator and more text is replaced whole). Expected on the review's 58 `kvU` rows: 36 leak at the head, 6 after (three named limits in both forms), 30 rows change.
- One thing the kit cannot promise: telling a named pipe from a regular file without opening it. I know of no framework call that does it and could not test one. The kit makes the seat measure first (Step 5(c)) and, if there is none, name the pipe as a limit with links still closed (Q6), instead of stopping. The commission's rule 6 wanted the pipe closed; this is the one place the kit may fall short of it, said here and in the kit.

## What I measured, and how
1. Origin by `gh api -X GET` under the OXPd_2 `GH_CONFIG_DIR`, login checked first, 19:07:48 to 19:07:50: 3 branches (`main` 7bf37526, `b1787/wp110-logging-denylist` 2c231b44, `b1764/wp03-ci-skeleton` 6e2629bc), compare ahead 1 behind 0 files 21, 4 check runs success, pull requests 1 (closed, merged), tags 0.
2. The source at the head, in the review's clone (`rev-parse HEAD` = 2c231b44), by the Read tool: 8 product files and 3 test files whole, `LogScannerTests.cs` and `SuiteLoggerFactory.cs` in part. 25 `file:line` pointers re-printed by program at 19:26:54: 0 differ. The five mutant texts the kit quotes each occur exactly once in their file.
3. The logging package's converter, `serilog/serilog` tag `v4.4.0`, `PropertyValueConverter.cs` (528 lines) by GET: why every collection but the plain generic dictionary arrives as a sequence, and why a pair is a structure with `@` and one string without.
4. The review's logs, copied into scratch first: `attack-deny.out` 267 lines (78 name rows: 30 listed, 48 not; 58 `kvU` rows: 36 leak, 22 clean; 58 `kvL` rows clean; 12 other leaking rows), `attack-scan.out` 117 lines (24 `b64` rows, 10 found), `mutants.json` 52 entries (14 survive).
5. A Python model of `DenyList.Normalise` and `TryFindClass`. Control: it reproduces the review's listed-or-not verdict for all 75 name rows the log prints whole (0 differ). With it: each candidate stem's newly removed names among the 78, ten ordinary names per stem (each asserted to hold the stem and to be unlisted at the head), and the count after the proposed list (46 of 78 listed; 16 of the 38 plain names closed, 22 stay).
6. The kit's own tables recounted by program: table KV 29 makers, 36 / 6 / 30, 0 rows differ from the review's log; block DATA 6 lines, 587 bytes, sha256 `205ccd3c...c345f`, 34 stems.
7. The commit subject as a file under `gitleaks` 8.30.1 with the workflow's four options: rc 0.
8. Toolchain versions by path, the `.tools` listing, the lock folder (absent), the panes, load (2.16), free space, at 19:16:16.
9. The reading load by program: 333915 bytes (the kit 83962 plus 20 files: the first kit 76800, the verdict 33298, the first STATUS 46366, the review's `mutants.py` 13599, the project `CLAUDE.md` 10052, 15 `.cs` files).

## What I did NOT read
- The first STATUS whole (46366 bytes): I read its headings, lines 51, 158, 203, 205 and the heads of its FOR TUESDAY items. The verdict's `FOR-RECORDS.md`, `CODEQL-FIRST-PR.md` and landing texts. The review's commission.
- `DenyListClass.cs`, `SuiteLogOptions.cs`, most of `LogScannerTests.cs`, both lock files, the project files.
- The review's `Program.cs` beyond lines 21 to 24, 40 to 179 and the lines a search printed; its 104 mutant logs (only `mutants.json`).
- The form kit's `.pre-stamp` copy; the B1774 round-1 kit that the B1774 commission names as a form.
- `SETUP_RUNBOOK.md`, `BACKLOG.md`, `CLARIFICATIONS.md` beyond the two heading lines; the kits B1788 and B1789; Jira; anything under `Source_Documents/`; the NAS.
- No hosted job log was re-read: every hosted line in the kit is RELAYED from the verdict.

## Decisions I proposed (each the coordinator's to rule; alternatives are in the kit)
D1 sibling rule by the neighbour's value; D2 text rule for stringified forms; D3 the event's top-level properties are NOT siblings (a source-context property holding a class name with a stem would empty every event of that class: derived, not measured); D6 a path with a hit is withheld whole; D7 a path is searched like a line; D8 regular files only, no link followed; D9 empty list refused; D10 base64 without the last partial group; D11 the glued token a named limit.

## Questions, each with its default
- Q1 mechanism for structures and sequences: the sibling rule. Alternative: only members named `Key` or `Name`.
- Q2 stringified forms: the text rule. Alternative: a named limit (16 rows then stay open).
- Q3 top-level properties: not siblings, a named limit. Alternative: siblings too.
- Q4 the stems: the 13 of your leaning (`authorization` is already a stem, so `authorisation` is the new one). **The evidence argues against three of them as low-cost: `otp` sits inside `RootPath`, `SnapshotPath`, `Footprint`, `HotPlug`; `cardno` inside `CardNotPresent`, `CardNotFound`, `DiscardNotice`; `sessionid` inside `SessionIdleTimeout`.** The default keeps all 13 because the rule errs toward removing. A changed list means editing block DATA and FACT 6 at the stamp.
- Q5 a path with a hit: withheld whole. Alternative: only the hit replaced.
- Q6 the pipe when the framework gives no instrument: a named limit, links still closed. Alternative: STOP and you allow a native call.
- Q7 base64: the partial group dropped, offsets 1 and 2 named. Alternative: three alignments.
- Q8 the glued token: a named limit. Alternative: closed.
- Q9 the three new public names of `LogScanRule`: `KnownValueInPath`, `TokenShapeInPath`, `NotARegularFile`.
- Q10 the review after: G1 on Fable, round 2, its own table and 43 mutants.
- Q11 windows and pane: 180 and 150 minutes, `Datasec/OXPd2-X8`.

## Corrections to the commission
- "22 leaking rows of 116": the 58 `kvU` rows hold 36 leaking rows; the review's 22 are the key-and-value ones, and the other 14 are what your ruling 3 asks about. The kit's table carries all 58.
- "its 43 mutants": the result file holds 52 (2 reverts, the first seat's 7, the review's 43). The kit says so.
- Ruling 8 says "ONE or TWO new commits": the kit says one, and a second only for a red hosted run.
- The sidecar: 35 of its 113 lines say the literal is an instruction, not an expected output. They were matched to their text by substring, by program; spot-check a few.

## Inputs of each step (each exists at the head or is made by an earlier step)
Step 1: the origin branch, the checkout's local configuration, the first seat's `clone.py`. Step 2: the clone, table KV and the makers (in the kit). Step 3: block DATA (extracted in Step 1(e)), the red cells of Step 2. Step 4: the clone after Step 3. Step 5: the instrument program (made in 5(c)), the cells of Step 4. Step 6: everything built; the ban list file. Step 7: the staged tree; the first seat's `run_step.py`. Step 8: the pushed head.

## Outside the fences
- **Scratch is larger than it should be:** I copied the review's `logs`, `probes`, `scratch` and `mut` folders into `fleet/state/s300/d1798/gate/` (about 385 MB on disk; the probes hold a 3 GiB sparse file). Two entries with mode 000 could not be copied. The folder is ignored by git (`.gitignore:44`). Nothing was deleted; quarantine it when the round closes.
- The kit points the seat at three of those copies as readable claims (`mutants.py`, the two attack logs, `Program.cs`), because the review's folder under `/private/tmp` can vanish. That makes a file under `fleet/state` part of the seat's reading: your call whether to move `mutants.py` beside the verdict instead.
- One scan by `gitleaks` in scratch (a one-line file). No build, no test, no git write, no Jira, no GitHub write, no message. Two of my shell lines read `$?` after a pipeline (a hook warned); neither result is used in the kit.
- The partial kit ended with a clear PARTIAL line between 19:22 and 19:26; it was never stamped or copied.
