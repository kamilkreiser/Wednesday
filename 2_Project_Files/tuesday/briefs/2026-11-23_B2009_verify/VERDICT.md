GATE B2009: GO WITH FINDINGS @ 25cb4cb on main b4b4ef6

Gate G1 (how the admin password and the pin reach output), round 1 of 2 of lane LH, one Opus reader (claude-opus-5-5),
in-session, read-only. OXPd 2, lane LH, kit B2006 (seat X58; S4 Q1 to Q8 the defaults, each the coordinator's, none the
product owner's). Head `25cb4cb2d2b8a82566e19fc6b1389753bbd4843b` on `b2006/lh-lab-hygiene`, ONE commit, one parent
`2e2feae8` (BASE = main after PR 40). **Main MOVED during the gate:** lane W1 landed as PR 41 at 22:20:48 AEDT, main =
`b4b4ef604c6381991dc224b92ebe5615dbab5bb4` (one parent 2e2feae8, tree = W1 head f039956d's tree `a1d181da`, six paths, all
OXPd 1.x client or its tests); its push run 45164375478 `HOSTED b4b4ef60: PASS` at 2020 / 645. The merge of this head
with that main is MEASURED below (MAIN MOVES (B) of landing.txt). Read and measured 2026-11-23 22:04 to 22:32 AEDT in my
scratch `fleet/state/s318/g2009/`: `clone` (clone.py draft at 22:06: push URL `invalid://no-push`, no identity), `clone2`
(the same at 22:30, main b4b4ef60), worktrees `red` (BASE + `1-red.diff`), `pat` (BASE + both patches, staged), `prb`
(the head + a gate probe file, now `_quarantine/G2009Probe.cs.txt`) and `w1m` (W1's head with this head merged, tree
`4af54a4b`). Every dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock,
one at a time (44 released lock folders, all mine, in `g2009/_quarantine/locks/`; lock absent at the end; gate B2008's
lock never touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira;
no push, no pull request, no re-run; the lab tool was driven only in-process by the test assembly against the tests' own
127.0.0.1 stubs (probe and oxpd1 first contacts to a CLOSED 127.0.0.1 port; print only as a dry run; no DNS name was ever
a run's host); no printer, no tenant; nothing deleted.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`pat` `write-tree` `0df641b1` = `25cb4cb2^{tree}`;
commit message = `commit-message.txt`); both patches and the ten tools equal THE TOOLS' sha256 in my copy and in the
seat's `.tools/b2006/gate` (20 of 20). 16 paths (2 A, 14 M), numstat equal to the kit's table, `checks_lh.py` 8 of 8 with
every control. Red first: Lab `Total: 129, Errors: 0, Failed: 28`, exactly the kit's 28 cases, every one an `Assert.`
line (15 `Assert.Null`, 9 `DoesNotContain`, 3 `StartsWith`, 1 `Equal`). Green 2041 / 0 / 2037 / 4. `MUTANTS: 16 of 16
MATCH, 16 of 16 undone equal` (my run of the frozen tool; `mFourthCommand` red on none). **The G1 question, MEASURED: 192
argument shapes over the four parsers (a 64-hex word and a password-shaped word; bare, `=` forms, `--x`, `-x`, em-dash,
U+2010, full-width and U+2212 lookalikes of `--`, `--PIN`, empty and space words, repeats, every insert position) put
neither word nor its first 16 characters in any output; 0 exceptions; all exit 2.** No refusal text carries a value (the
run-folder reason names only the type; 24 folder shapes: exit 5, no path marker printed). `probe --plain-discovery-tree`
without `--pin`: 120 of 120 argument orders and 9 more shapes exit 2 with 0 requests and 0 TLS connections at the stub
(control: with a pin, 2 requests). The merge with main b4b4ef60 builds 0/0 and tests 2054 / 0 / 2050 / 4, RULES 647.
Hosted push run of the head PASS on both legs. One Minor and six Info findings; none sends a byte or prints a value;
none blocks the landing.

## FOUND

1. **Minor (an exit-7 sentence that hangs instead).** Oxpd1 `README.md:23` to `:25` "A missing file, a file that cannot
   be read (...) ends the run with exit 7 before any connection". MEASURED (probe row `CRED fifo`): a credentials file
   that is a named pipe with no writer blocks `oxpd1 read` in `CredentialsFile.Read` (`LabFiles.cs:28`,
   `File.ReadLines` opening the pipe) with 0% CPU for about five and a half minutes (the probe ran 22:22:33 to about 22:29; the executable's Time 391.9 s), until I opened the pipe's write end from outside;
   then exit 7, 0 TLS connections, 0 requests, `nothing was sent`. The read is synchronous on the caller's thread before
   any await, so the command's cancellation token never reaches it (my probe's own 5-second watchdog could not run).
   Nothing is sent and nothing is printed; an agent driving the tool would hang. Fix for round 2: read only a regular
   file (refuse a pipe or a device before opening it) or name the shape in the README's Limits.
2. **Info (the argument number is relative).** `ParserWords.Unknown(index)` (`ParserWords.cs:16`) counts from the
   command's own arguments (the host is argument 1, after `probe`/`print`, after `oxpd1 read`/`lab-cert`), so the number
   printed is 1 (probe, print) or 2 (oxpd1 verbs) lower than the word's place on the whole command line. Not a leak; the
   READMEs say "by its position" without saying from where.
3. **Info (U+200B is not blank).** MEASURED: `--run` and `--credentials-file` refuse "", " ", tab, newline, NBSP and
   U+3000 in all four parsers (reasons name the option); a lone zero-width space U+200B is not white space to .NET
   (`string.IsNullOrWhiteSpace`), so it is taken as a folder or file name (a credentials file of that name: absent, exit 7).
   A valid file name, not a defect; a shape outside Y03/Y04.
4. **Info (the host and value limits, now measured).** Kit H5's DERIVED line is MEASURED: a 64-hex word, lower or upper,
   is `UriHostNameType.Unknown`, refused by all four parsers with a fixed text (no echo). A host-shaped password (letters
   and digits) IS taken as the host by all four parsers and printed with the run (the stated limit). An upper-case
   name-shaped word given as `--password-name` is taken as the name (the Oxpd1 README limit). Bad values of `--read`,
   `--addressing`, `--soap-port`, `--timeout-seconds`, `--pin` give fixed texts (value not in the reason).
5. **Info (the work-tree line, the seat's H24 (i)).** DERIVED (`LabFiles.cs` `RunFolderRule`): the exit-9 line prints the
   folder that holds `.git`, an ancestor of the full run path (the run path itself only when it already exists and holds
   a `.git`), not the `--run` value as typed; a typed word reaches it only as a path component above a `.git`. The seat's
   "like H4" is broader than the code.
6. **Info (masking edges, MEASURED).** Repeated names (password, nested `pwd`, untyped, `problem+json`, at depth 40) and
   a repeated XML attribute: not shown, marker absent, no exception. `Password` and `password` in one object (distinct
   to JsonObject): shown masked, marker absent. A type of "" or spaces is sniffed and shown (kit H21). An untyped JSON
   body led by a BOM or a space is NOT shown (`no type`): the first-byte rule errs toward hiding. `text/plain` JSON: not
   shown (SHOWN). The `ArgumentException` catch returns only the not-shown form: it can hide, never reveal.
7. **Info (Windows proof of exit 7).** On the hosted windows leg Y05's mode-000 and dangling-link rows return at once by
   design (Q6; windows `skipped: 21` = BASE's), so the `UnauthorizedAccessException` catch of `LabFiles.cs:30` has no
   Windows cell; the held-open and folder rows ran green there (Lab dll `passed` on both legs).

## THE KIT'S GATE LIST (FOR TUESDAY)

- `BASE..head` read whole: `ParserWords.cs`, the four parsers and `RunAsync` lines of `ProbeCommand.cs`,
  `PrintCommand.cs`, `Oxpd1Command.cs`, `LabCertificate.cs` (each whole at the head), `RunRecorder.cs`, `Masking.cs`,
  `LabFiles.cs`, `CommandRegistry.cs` (whole), `DeviceChannel.cs` hunk, the three README hunks, `HygieneTests.cs`
  whole, the P13 and R11 hunks; `Program.cs` (no catch-all: an exception would reach the runtime's handler).
- Patches and tools: 10 of 10 sha256 equal to THE TOOLS (my copy and the seat's). Head tree = BASE + both patches
  (`0df641b1`); `red` tree `1050bda8` = BASE + `1-red.diff`.
- Red first (`red`, my run): locked restore rc 0; Lab test project build 0/0; Lab executable `Total: 129, Errors: 0,
  Failed: 28`; the 28 `[FAIL]` names equal THE CONTROLS' list (Y01 x9, Y03 x5, Y04, Y05 x3, Y06 x4, Y07, Y08 x2, Y09
  x3); caught types in the `Assert.Null` lines `ArgumentException` 6, `DirectoryNotFoundException` 4, `IOException` 1,
  `UnauthorizedAccessException` 1, `FileNotFoundException` 1 (Y08 prints the exception object). Program
  `g2009/scratch/redcheck.py`, no value printed.
- Mutants (`pat`, `mutants_lh.py run`, rc 0): every row equal to the kit's MEASURED row (Failed 1, 1, 5, 4, 2, 1, 2,
  1, 4, 1, 2, 1, 1, 1, 1, 0); `pat` status after = the 16 staged rows, no unstaged change.
- ANY usage error repeating an argument: the 50 `error = ` lines (`git grep -n -i` at the head, 50 lines: 31 literals,
  4 `null`, 1 the `UsageError` constant, 11 `ParserWords` calls, 2 choices between fixed texts, 1 the enum's names) hold
  no argument; the `Usage` lines are constants; the run's first output line prints the host and the run folder (H4/H5,
  stated limits, FOUND 4); `LabCommands.RunAsync` and the `oxpd1` verb dispatcher print fixed texts. MEASURED: 192 of
  192 shapes clean (BLUF).
- The pin or password through a refusal text: `RunRecorder.cs:46` names `failed.GetType().Name` only; the exit-7 line
  names the password NAME (validated shape) only; MEASURED 24 folder shapes (below a file, an existing file and folder,
  a read-only parent, a 300-character name, below `/dev/null`) x 4 commands: exit 5, 0 exceptions, refusal kinds
  `exists`, `DirectoryNotFoundException`, `UnauthorizedAccessException`, `PathTooLongException`, path marker in no
  output. 10 credentials shapes: exit 7, 0 TLS, 0 requests, password in no output (FOUND 1 for the pipe).
- The masking catch: FOUND 6 (hides only).
- P13 and R11 against a fourth command: `mFourthCommand` (appended) red on none; DERIVED: a command inserted between
  probe and print reddens R11 by design ("print right after probe"); one inserted before probe reddens neither.
- README sentences (the kit's table) against the code: each holds at the head, but for FOUND 1 (pipe) and the scope of
  "position" (FOUND 2). `new DeviceChannel(` occurs at `ProbeCommand.cs:209` and `Oxpd1Command.cs:263` only under
  `src/` (the doc comment holds); `RunRecorder.Create` callers are the four commands (`:201`, `:192`, `:240`, `:121`);
  `CredentialsFile.Read`'s one caller is `Oxpd1Command.cs:298`, before the client is made.
- Hosted run on both legs (head): `hosted3.py 25cb4cb2 --total 2041 --rules 645 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`: run 45160807294 attempt 1, every step
  success; linux 2041 x2 / 2037 / 4, GUARD 14; windows 2041 x2 / 2020 / 21, GUARD 15; secret-scan both PLANTED-CONTROL
  lines, `no leaks found` x3, `wrong 0` x2, `not among ... 0`; rules `RULES: clean (645 files)`, floor 111; `HOSTED
  25cb4cb2...: PASS`; `failed Datasec.` 0 and 0, `Datasec.Suite.Lab.Tests.dll` 4 lines and `passed` on each leg.

## WIDER (G1 depth): a test-only probe (`_quarantine/G2009Probe.cs.txt`, never committed; results
`g2009/scratch/probe-results.txt`, booleans and counts only; Lab executable whole `Total: 130, Errors: 0, Failed: 0`)

- ECHO: 192 runs, 0 with the word or its first 16 characters in the output, 0 thrown, every one exit 2.
- PLAIN: 120 orders of `--run`, `--plain-discovery-tree`, `--https-port`, `--ipp-port`, `--timeout-seconds` without a
  pin: exit 2 x120, run folders 0, stub requests 0, TLS 0. Plus an invalid, empty, 63- and 65-hex pin, `--pin` last,
  `--pin=<hex>`, `--PIN`, the plain option twice, `--run --pin`: exit 2, 0 requests, 0 TLS. Control with a valid pin:
  exit 0, 2 requests.
- Blank values: FOUND 3. Credentials file: missing, a folder, empty, `NAME=`, `/dev/null`, a symbolic-link loop, mode
  000, a file inside a mode-000 folder, a dangling link: exit 7, 0 TLS, 0 requests; a pipe: FOUND 1.
- Exit codes against each README: 2 (usage, blank `--run`, blank `--credentials-file`), 5 (exists or cannot be made, all
  four commands), 7 (`oxpd1 read`, cannot read) as written; print's 7 ("any other failure of the send") not exercised
  (a dry run sends nothing).

## FRAME (stamp checklist item 11: three shapes outside the tested one per never / every / only sentence)

| Sentence | Shapes outside the tested one | Cell, probe or stated limit |
|---|---|---|
| a usage error never repeats a word the command does not know | `=` forms; unicode `--` lookalikes; empty/space words; `--PIN`; every insert position | probe: 0 of 192 |
| ... a pin or password typed where an option name belongs is not printed | as the host; as `--run`'s or `--password-name`'s value | 64-hex host refused (MEASURED); host-shaped and value shapes: stated limits (FOUND 4) |
| a run without a pin makes no plain call | every option order; malformed pins; `=` and case forms | probe: 0 requests (129 runs) |
| a file that cannot be read ends in exit 7 before any connection | link loop; file in a mode-000 folder; `/dev/null`; a pipe | probe: exit 7, 0 TLS; the pipe HANGS (FOUND 1) |
| a run folder that exists or cannot be made ends in exit 5 | read-only parent; 300-character name; below `/dev/null` | probe: exit 5 x4 commands, type-only reasons |
| a blank `--run` / `--credentials-file` is a usage error | tab; newline; NBSP; U+3000; U+200B | probe: refused but U+200B (FOUND 3) |
| only a body with no type is read by its first byte | "" and spaces as type; BOM- or space-led untyped JSON; `text/plain` JSON | probe: sniffed; not shown; not shown (FOUND 6) |
| a JSON object holding one name twice is not shown | deny-listed name; nested; untyped; problem+json; deep | probe: not shown, no exception |
| the registry cells need no line for a new command | appended; between probe and print; before probe | `mFourthCommand` NONE; DERIVED R11 red; DERIVED none |

## SCANS

- gitleaks 8.30.1: control FIRST (a token-shaped value built by a program from two halves and 36 random characters,
  never printed, alone in a new folder): rc 1, `leaks found: 1`, folder moved to `g2009/_quarantine/gl-control`. Then
  the head's 16 changed blobs, both patches, the commit message as committed and the 448 added lines under neutral names
  `1.txt` to `20.txt`: rc 0, `no leaks found`. Hosted secret-scan of the head: clean (above).
- words.py: `--control` `CONTROL FIRED: 13 of 13`; the 448 added lines + the commit message `WORDS: clean (2 files)`;
  the squash subject (with #42), squash body and PR title `WORDS: clean (3 files)`.
- squash_scan.py (main b4b4ef60's `build/`, equal to the head's: `build/**` is in neither diff): subject with #42 +
  `squash-body.txt`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`.

## THE CHAIN AND THE MERGE

- Head (`pat`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test`: `total: 2041`, `failed: 0`,
  `succeeded: 2037`, `skipped: 4`; `repo_rules.py` (no `--source-documents`) `RULES-NOTE: R5 hash half NOT RUN`,
  `RULES: clean (645 files)`; `unittest` `Ran 111 tests` OK; `checks_lh.py` 8 of 8.
- Merge with main of the gate's start (2e2feae8 = BASE): `git merge-tree --write-tree` = `0df641b1`, the head's tree.
- **Merge with main of the moment (b4b4ef60, W1's squash, PR 41):** `git merge-tree --write-tree b4b4ef60 25cb4cb2` rc
  0, tree `4af54a4bd6580ead93f629d705a728b0c487b17f` (the same tree as the merge with W1's head f039956d, whose tree main
  carries); `w1m`: locked restore rc 0 (no lock file in either diff); build 0 Warning(s) 0 Error(s); `total: 2054`,
  `failed: 0`, `succeeded: 2050`, `skipped: 4` (= main's 2020 + 34); `RULES: clean (647 files)` (= 645 + 2). W1's client
  diff (read whole) removes and re-signs no public member; it adds internal members to `Oxpd1Client`, internal
  `Oxpd1Soap` overloads and the public `Oxpd1Writer` with its types: the Lab's calls compile unchanged (MEASURED).
- New main's push run 45164375478: `HOSTED b4b4ef60...: PASS` at 2020 / 645 (linux 2016, windows 1999), Analyze rows
  success; code-scanning analyses at b4b4ef60 csharp/python/actions 0; open alerts 0; open PRs 0.

## NOT RUN

- The publish and release guard locally (the hosted legs' GUARD 14 / 15 on the head are the proof; the seat's local
  publish: 0 Lab files).
- The probe on Windows and Linux; CodeQL locally; the PR's merge-ref run (does not exist yet); the hosted legs of the
  merge 4af54a4b (the PR's own run is the first).
- An independent build of the mutants (my run is of the frozen tool, as the seat's).
- A rebuild and whole-solution test of `pat` after the mutants (undo proved equal by the tool and `git status`).
- Any device, simulator or tenant.

## DISCLOSURE

- My probe's credentials pipe row hung the probe (FOUND 1, by design of the row: I had expected the read to yield). The
  test process sat at 0% CPU holding the wave lock for about five and a half minutes until I opened the pipe's write end (my own
  scratch file `g2009/scratch/cred.fifo`) with a non-blocking open; the run then finished normally. Gate B2008 may have
  waited on the lock in that window; I never touched its lock or files.
- Lane W1 landed while I gated (not by me). I re-read main, cloned again, and measured the merge (above) rather than
  rely on the kit's BASE.

## LANDING

`landing.txt` (written for <M> = b4b4ef60, MAIN MOVES (B) measured), `pr-title.txt`, `pr-body.md`,
`squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md` in this folder. Who decides to land: the coordinator (Tuesday),
never the product owner. FOUND 1 to 7 are for round 2 of 2 of lane LH or the records lane, not a hold on this landing.
