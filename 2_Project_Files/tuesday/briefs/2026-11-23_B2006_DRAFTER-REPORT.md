STARTABLE: YES

# B2006 DRAFTER REPORT: lane LH, the lab tool's hygiene before the first printer run (ECHO, EXITS, PLAIN, DUP, LABTEXT, and SHOWN), seat Datasec/OXPd2-X58

Drafter B2006 (Opus, in-session, read-only toward the project, GitHub GET only), 2026-11-23 20:42 AEDT to the sidecar's write clock. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2006_SEAT-X58_oxpd2-lh.md` (size and sha256 in the sidecar's last line), sidecar `.measured` beside it. Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s318/d2006/` (below `<d>`); the seat's tools `<d>/seat-tools/` (ten files). Gate tier G1, round 1 of 2 of lane LH. BASE `2e2feae85d5fe3b8ee07cf618e3005b0630f4ca0` (main after pull request 40).

## BLUF
- ONE commit, 16 paths, all under `src/Datasec.Suite.Lab/` and `tests/Datasec.Suite.Lab.Tests/` (2 A, 14 M): no `.csproj`, no lock file, no package, no slnx, no path of lane W1's. Patches: `1-red.diff` (tests only: the new `HygieneTests.cs` with Y01 to Y09, 34 cases, and the P13 / R11 relaxations) and `2-fix.diff` (src only).
- (a) ECHO: a new `ParserWords` helper; no usage error of `probe`, `print`, `oxpd1 read` or `oxpd1 lab-cert` repeats a word its parser does not know (only its position); an option of the command given last is still named. Built for all FOUR parsers (the commission named two; `probe` and `lab-cert` carry the same two lines: Q1).
- (b) EXITS: blank `--run` (four commands) and blank `--credentials-file` are usage errors (2); a credentials file that cannot be read (held open, mode 000, dangling link) ends in 7; a run folder that cannot be made ends in 5 ("exists or cannot be made", Q2) through a new `RunRecorder.Create(folder, out refusal)` overload (the landed one-argument form kept for the landed channel cells). (c) PLAIN: `probe` refuses `--plain-discovery-tree` without `--pin`. (d) DUP: the masking catches `ArgumentException`. (e) LABTEXT: `CommandRegistry.cs:19`, `DeviceChannel.cs:37` corrected; P13 and R11 are contains-checks, red-proofed by three mutants, and a fourth command reddens neither (mutant `mFourthCommand`, expected NONE). (f) SHOWN: IN (it fit): only an untyped body is read by its first byte.
- MEASURED in a fresh `<d>/clone3` with the frozen patches: RED Lab `Total: 129, Errors: 0, Failed: 28` (all 28 by `Assert.`: the helper catches what a command throws); GREEN whole solution `total: 2041`, `failed: 0`, `succeeded: 2037`, `skipped: 4` (2007 + 34); mutants, chain and checks: see "Facts re-measured".
- One slip of my own, caught by my own tool: the first frozen run (`<d>/clone2`) used P13 with `Assert.Subset` (the wrong direction); `mFourthCommand` reddened P13 (`DIFFER`). Fixed to `Assert.Superset`, `1-red.diff` re-cut (`2-fix.diff` unchanged, `cmp` equal), the four registry mutants re-run on the prototype (4 of 4 MATCH, `mFourthCommand` NONE), and the WHOLE frozen run redone in a fresh `<d>/clone3`. `<d>/clone2` and `<d>/f/` are SUPERSEDED (left as they are).

## Facts re-measured (instrument)
- Origin `main` = `2e2feae85d5fe3b8ee07cf618e3005b0630f4ca0` (`clone.py draft` at 20:44, 20:58, 21:05); no `b2005` or `b2006` ref.
- BASE's push run 45143388653: `hosted3.py ... --total 2007 --rules 643 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15` -> `HOSTED 2e2feae8...: PASS`.
- Frozen run (`<d>/clone3`, logs `<d>/f2/logs/`): `apply --check` rc 0 for each patch alone; locked restore rc 0; build 0/0; RED Lab `Total: 129, Errors: 0, Failed: 28` (15 `Assert.Null`, 9 `Assert.DoesNotContain`, 3 `Assert.StartsWith`, 1 `Assert.Equal`); GREEN 2041 / 0 / 2037 / 4; `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal` (about 14 min under a shared lock); rebuild after mutants (dll newer than sources) and 2041 / 0 again; chain: `--force` restore `locks equal 34 of 34`, build 0/0, test 2041 / 0, both publishes rc 0, `GUARD: clean (14 files)` / `(15 files)` with 0 Lab files, `Ran 111 tests` OK, `RULES: clean (645 files)` (R5 hash half NOT RUN, no `--source-documents`); `checks_lh.py` `CHECKS: 8 of 8 PASS` (16 rows 2 A / 14 M; shared 60 paths rc 0; W1's folders rc 0; ASCII; 448 added lines; 10 public lines all in the test file; echo lines 0 and 1 vs BASE 4 and 4); staged tree `0df641b1`.
- Scans: `words.py --control` `CONTROL FIRED: 13 of 13`; over the 448 added lines and the message `WORDS: clean (2 files)`. gitleaks 8.30.1: control rc 1 (`leaks found: 1`, quarantined); `<d>/clone3` rc 0; 21 neutral copies (16 blobs, 2 patches, message, 2 tools) rc 0.
- Tools: `clone.py`, `heavy.py`, `hosted3.py`, `run_step.py`, `words.py` byte-equal to kit B1997's (`cmp`); `mutants_lh.py --list` -> `LIST: 16 mutants`.
- Owed items in `<project>/BACKLOG.md` (read live 20:58, records seat's write of 20:47): 80 PLAIN, 81 SHOWN, 82 DUP, 88 ECHO, 89 EXITS, 90 LABTEXT (cited in the kit's FOR RECORDS only, never in the commit message).
- `CLARIFICATIONS.md` 798 lines (C-1 to C-76) and today's rulings (16 lines): no ruling on any lane subject (counts in the kit's THE AUTHORITY; controls `OQ-6` 3, `C-63` 1, `printer` 4). The one `plain-discovery` hit records the coordinator's interim rule.
- Kit `stamp_check.py`: 217 claims, 217 measured, rc 0. Kit 92143 bytes before this report's write (exact size and sha256 in the sidecar's last line).
- Load up to 16.74 (load1) while drafter B2005 built; lock waits 0 to 14 per job.

## D-decisions (all the coordinator's)
D1 one never-echo rule for all four parsers via `ParserWords` · D2 an unmakeable run folder is exit 5 everywhere (the reason names the exception TYPE only) · D3 an unreadable credentials file is exit 7, one message · D4 blank checks in the parsers (the landed throws stay as guards, now unreachable from a command line) · D5 P13/R11 contains-checks, red-proofed (3 red mutants + 1 green) · D6 SHOWN in: sniff an untyped body only · D7 one commit, rebase before the first push only.

## Q-questions for Tuesday (each with its default; none STOP-CLASS, every default built)
- Q1 ECHO's parsers. Default: all four. Alternative: print and oxpd1 read only (re-cut; probe/lab-cert echo a named limit).
- Q2 unmakeable run folder. Default: exit 5 "exists or cannot be made". Alternative: a new code per command.
- Q3 unreadable credentials file. Default: exit 7, one message. Alternative: a distinct code.
- Q4 SHOWN. Default: IN. Alternative: OUT, the next lane (re-cut without the `KindOf` hunk, Y09, `mSniffTyped`).
- Q5 registry cells. Default: contains-checks, red-proofed. Alternative: keep exact lists (a limit; every later command edits both).
- Q6 Y05's mode-000 and dangling-link rows return at once on Windows (a designed branch written before any run, the shape of kit B1997's L01). Alternative: drop the rows (the `UnauthorizedAccessException` catch then has no cell).
- Q7 landing order with W1. Default: either order (disjoint paths; rebase rule; expectation = new main + 34 tests, + 2 rule files). Alternative: W1 first.
- Q8 Opus, X58, READY Step 0 + 120, push by Step 0 + 90, hard stop 02:30 AEDT Tue 2026-11-24, gate G1 round 1 of 2.

## Next lane (named, not built)
The lab wiring of lane W1's write calls and the end-of-session undo list (B1996 F19), after W1 and LH land (the commission). Nothing of (a) to (e) or SHOWN is left over.

## Chain table (every step's inputs exist earlier)
Step 0: the kit and the stamp → 1: `<src>` (ten files), the origin, BASE's push run → 2: the clone → 3: `1-red.diff` → 4: `2-fix.diff`, `mutants_lh.py`, the red tree built → 5: the green tree, mutants undone and rebuilt → 6: the staged tree, `checks_lh.py`, `words.py`, the message → 7: the commit, `origin/main`, `run_step.py`, `hosted3.py`.

## UNMEASURED / NEVER RUN
Every hosted leg of this lane's head (Linux and Windows: Y05's held-open row's file locking is DERIVED from .NET's Unix share emulation on Linux and the system's own on Windows); `clone.py seat`, the commit, `run_step.py`'s neutral scan of a commit, the push, the read-back, `hosted3.py` on a head of this lane, the rebase. Any device. The whole solution is not run red (not needed: the Lab executable is).

## Outside-the-fences disclosure
- Writes: only my kit, its sidecar, this report and files under `<d>/` (clones by `clone.py draft`, push URL `invalid://no-push`; `git add`/`write-tree` in my own scratch clones only). No write to the project, GitHub, Jira or any person. No push, no pull request.
- Reads: the project's `CLAUDE.md`, `CLARIFICATIONS.md`, `SETUP_RUNBOOK.md`, `BACKLOG.md` (read live for the owed-item numbers 80, 81, 82, 88, 89, 90), `kam_rulings_today.sh` output into scratch; GitHub by `gh api -X GET` (hosted3.py) under the project GH_CONFIG_DIR. Never `4_Credentials/.env`, `Source_Documents/`, a key folder or the NAS.
- The heavy lock: shared with drafter B2005 (its `owner.txt` read, never touched); every job of mine through `heavy.py`; released folders moved to my `_quarantine/locks/`.
- `sed -i` was used on my OWN prototype files in my scratch clones (never on a project file); nothing deleted (superseded folders moved to `<d>/_quarantine/` or left in place).
- Lane W1's files and scratch (`fleet/state/s318/d2005/`) were not opened.
