# FOR RECORDS: the logging lane (WP1.10), gate B1796, head 2c231b4 on main 7bf3752

What a records pass must file. The gate wrote none of it anywhere: no ticket, no backlog line, no runbook line, no README line.
State at the time of writing: **NO GO, a fix round follows; nothing below about the code is final until the fix round's gate.**
Sources: the builder's STATUS (section FOR RECORDS and FOR TUESDAY), the gate's VERDICT.md, CODEQL-FIRST-PR.md.

## 1. Ticket states (the master board; changing a ticket is the coordinator's)

- `OXPD2-15` ([WP1.10] Logging deny-list): NOT done. The unit form is built and under review; the gate reads NO GO at this head.
  After the merge it still stays open for "the scan of logs from a real sign-in" (exit test E1.8), which needs a printer.
- A new ticket for the fix round of this lane (the three blocking findings of VERDICT.md, and findings 4 to 6 in the same pass).
- A new ticket: wire the host to the logging library (section 3, line 1). Until it is done the list protects nothing.
- A new ticket: one README pass after the wave (section 2).

## 2. The repository's README (one pass after the four wave-1 lanes; nobody edits it inside a lane)

- Layout, under `src/`: add `src/Datasec.Suite.Logging/Datasec.Suite.Logging.csproj` (class library; the packages `Serilog` and
  `Serilog.Sinks.File`; references no project; the one way to build a logger, every sink behind the field deny-list) and its
  files as they stand after the fix round (at this head: `DenyListData.cs`, `DenyList.cs`, `DenyListClass.cs`, `DenyListSink.cs`,
  `SuiteLogOptions.cs`, `SuiteLoggerFactory.cs`, and under `Scanning/`: `LogScanner.cs`, `LogScanFinding.cs`, `LogScanResult.cs`,
  `KnownValueForms.cs`, `TokenShape.cs`).
- Layout, under `tests/`: add `tests/Datasec.Suite.Logging.Tests/` (`DenyListTests.cs` 30 cells, `LogScannerTests.cs` 12 cells,
  `LogHarness.cs`, `Synthetic.cs`; counts at this head).
- Reserved names: remove line 53, `src/Datasec.Suite.Logging`.
- Add one sentence: "The host does not log through `Datasec.Suite.Logging` yet."
- Add to Checks or beside it: the package restore's own audit is the only vulnerability check and it is an error (section 5).
- The gate read the README at this head line by line: stale in the two lists, no sentence untrue in a way that matters.

## 3. `BACKLOG.md` (each in the project's shape; discovered 2026-11-20 in the WP1.10 lane and its gate)

From the builder's STATUS, each confirmed by the gate unless marked:
1. The host is not wired to the logging library. Where: `src/Datasec.Suite.Server/Program.cs`. Symptom: the host builds its default logging; nothing it logs passes the deny-list. Needs: a project reference; the host's own logging calls routed into the library's logger (a THIRD package, a decision); the file path and retention as settings; the host's default providers cleared, with a test.
2. Nothing stops a second logger without the list. Rule shape for `build/repo_rules.py`: outside `src/Datasec.Suite.Logging/` and its test folder no tracked file holds `LoggerConfiguration`, `Serilog.Log.` or a `PackageReference` whose id starts `Serilog`; the seam `CreateWithoutDenyListForTests` and an `InternalsVisibleTo` of the library appear in the library and its test project only; no second project builds an assembly named `Datasec.Suite.Logging.Tests` (the library has no strong name, so the name alone opens its internals).
3. The file sink's size limit and rolling are the package's defaults; what happens at the limit is UNMEASURED by the builder and by the gate.
4. The limits of the list and of the scanner are named in the XML comments and are not closed (the full lists: section 4).
5. E1.8 on the logs of a real sign-in stays open.
6. The three extras of the design's weakness row (configuration, job packets, user e-mail addresses) are not on the list.
7. Code scanning had not read this code at the push; the pull request is its first read (CODEQL-FIRST-PR.md).

Added by the gate:
8. The scanner is a library call; nothing can point it at a folder of real logs from a shell or a pipeline step.
9. A second logger built on the same file while the first is open is built without an error and its events are lost (measured). One logger per file must be a rule of the wiring lane.
10. After a logger is disposed, callers that still log get no error; the file takes nothing more; an added sink still receives cleaned events (measured).
11. The scanner: a named pipe in the folder makes it wait without end; a link to a folder is followed, also out of the folder, and a link loop is read 33 levels deep (the same file counted 33 times); a hostile file can make the list of findings very large (5 MB gave 1146880 findings).
12. No audit step of the repository's own (section 5).
13. The mutants that leave the suite green (VERDICT.md, findings 2 and 5): 14 at this head; the fix round should leave 0 of them.

## 4. The limits, as measured at this head (for the runbook's five sentences and for the kits of the lanes that log)

The deny-list does NOT stop a value:
- in the text of a message template; in the message of an exception or of an inner exception; used as a dictionary key (named in the code);
- under a name that holds no stem (named in the code), which includes: an object logged as one string (a record, a class with its own text form, an anonymous object, a JSON element); a positional placeholder; a tuple; an exception logged as a property; a name in look-alike or full-width characters or in another script (none of these is named in the code: VERDICT.md, finding 4);
- **under a listed KEY of a key and value collection that the logging package does not capture as a dictionary (VERDICT.md, finding 1, the Blocker; to be closed or named by the fix round).**

Rules for the lanes that log, for their kits (the builder's item 8, extended by what the gate measured):
- never put a value into the template text; never log an exception of a call that carried a secret without wrapping it;
- never use a secret or a file name as a dictionary key;
- log a set of named values only as a plain generic dictionary with text keys, or as an object with `@`; never a concurrent, sorted or immutable dictionary, a hash table, a list of pairs or a headers object (until the fix round says otherwise);
- never log an object without `@` unless its text form is known to print no secret;
- always a named placeholder, never a positional one;
- HTTP: method and status only, no body, no headers;
- name every property from the list of names that ARE listed (30 of the 78 the gate tried; `logs/attack-deny.out` rows `N`); a harmless number must not carry a stem in its name (`TokenCount`, `Handler`, `BodyLength` lose their values);
- **CodeQL: never name a C# variable, parameter, field or method with `password` or `passwd` and pass it to a logger, a file write or a trace call, in test code too (an alert at 7.5 that blocks the merge).**

The scanner does NOT see: a value split over two lines; a compressed file (reported unreadable); base64 of a longer text unless the value starts at a multiple of 3 bytes and either ends the text or has a length that is a multiple of 3; hexadecimal, HTML, XML and other encodings; an escape that encodes more characters than the spellings searched; another letter case; a value shorter than 8 characters (refused); a value nobody listed unless token-shaped; a token-shaped string glued to letters; a known value in a file's NAME (and its report prints paths as they are: finding 3).

The runbook's sentences (the builder's five stand, with two corrections): (1) the wave's lock: used 37 times by the builder and 113 times by the gate, never contended, works as written; (2) a seat can work in its own clone made with the deploy key: confirmed, the gate cloned the same way; (3) the checks table after the merge: `total: 43`, `RULES: clean (45 files)`; (4) `--output Detailed` shows the output of passing tests; (5) the cache holds `serilog/4.2.0` beside `4.4.0` because `Serilog.Sinks.File` 7.0.0 declares 4.2.0 as its lowest `Serilog` (established from its nuspec); nothing can load it. Add: (6) the package restore asks the package source for vulnerability data and FAILS when it gets no answer (`NU1900` as an error); a restore with the network closed needs the audit switched off for that one command, and then proves nothing about vulnerabilities.

## 5. The packages (the first third-party packages of this repository)

- `Serilog` `[4.4.0]` and `Serilog.Sinks.File` `[7.0.0]`, pinned exactly in `Directory.Packages.props`, locked by content hash in two lock files; each `Apache-2.0` by its own nuspec; the library has no transitive package; the test project's 16 transitive packages are the test framework's, already on `main`.
- **Known-vulnerability status: NOT TESTED by the gate (no request to any package source or advisory service). Package signatures: not verified.** The repository has no audit step of its own: the instrument is the audit the restore runs by itself, turned into an error by `TreatWarningsAsErrors`. File as an owed line: say so in the README or the runbook, and decide whether an unreachable vulnerability feed should fail a build.
- A third package would be needed to route the host's own logging calls into the library (the bridge named in the kit's Question 4): a decision for the wiring lane's kit.

## 6. Open design points for the master list `OXPD2-1` (decided by nobody in this lane)

1. **The six replacement texts as possibly customer-facing words:** `[removed:token]`, `[removed:session handle]`, `[removed:card string]`, `[removed:mail content]`, `[removed:file name]`, `[removed:password]` (the class names with their spaces are the builder's reading of the kit's one example). An administrator may read them in a log or a support bundle.
2. **Whether a left-out value leaves a marker:** today a value of an unknown kind, or deeper than 32 levels, vanishes with its name and nothing says so. A marker would be a new word of the same kind as point 1.
3. **Whether a user's e-mail address may be logged** (and configuration and job packets: the three extras of the weakness row). An audit line may need to say who signed in.
4. **The third package** a host bridge would need.
5. **Which stems join the list** (VERDICT.md, finding 7: 38 ordinary names the gate tried are not listed, among them `ApiKey`, `Credential`, `Cookie`, `Bearer`, `Pin`, `CardNo`, `SessionId`, `Path`, `JobName`). The stems are the coordinator's; the other lanes' kits must use the same list.
6. **A deny-list or an allow-list** (the kit's Question 7): every limit of section 4 is a consequence of listing what to remove rather than what may pass. A design change, not a seat's.
7. Whether the scanner should search file names (file names are one of the six classes; finding 3).

## 7. For the next kits of the wave (the three lanes that rebase onto this change)

- The lines this change adds: `Datasec.Suite.slnx` line 4 and line 9; `Directory.Packages.props` lines 7 and 8.
- What meets them (measured with `git merge-file`): Cards: nothing. Secrets: 2 conflicts of added lines (Logging first, then Secrets, in each folder). UniversalPrint: 1 conflict, in `/tests/` (Logging.Tests first). A package id that sorts between `Microsoft...` and `xunit.v3` meets lines 7 and 8 the same way.
- Say in the kits whether the order is ordinal or case-insensitive (they part when an id starts with a lower-case letter).
- The load gate: say whether each job needs its own pair of reads or one earlier read may serve several.
- The Stamp's byte count is taken before the stamp is written (73275 against 76800): harmless, but a seat will report it.
- For gate commissions on this machine: a gate of the coordinator's tree cannot `cp` from the project folder in a shell (the path guard refuses it) and its shell `git` write verbs must name a literal path under the temporary folder; a runner program holds the lock.

## 8. What was not tested (carry forward)

CodeQL for C# (hosted only); known vulnerabilities and signatures of the two packages; the Windows leg, the container and the two publishes on a local machine; the hash half of rule R5; any log of a real sign-in; a pull-request run of this head; the scanner on Windows; peak memory of a scan.
