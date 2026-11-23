GATE B2000: GO WITH FINDINGS @ 26f4b57 on main 86473f8

Gate G1 (the lab tool's first command that writes to a device; Tuesday's stamp S4 Q7), round 1 of 2 of lane L4, one
Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L4, kit B1992 (seat X53; Q1 = a in words at stamp
S4, Q2 to Q6 and Q8 the defaults, Q7 changed to G1; each the coordinator's, not the product owner's). Head
`26f4b57a619bb2c4b7009be5584e2e1580a1b127` on `b1992/l4-lab-print`, ONE commit, one parent `d804de5e` (BASE). Main
MOVED during the gate: FK (pull request 38) landed as `86473f8a91eb426a67a903b9c299b3b7f934ac80` (merged
07:43:35Z, read 18:50:45 AEDT); it shares no path with L4. Read and measured 2026-11-23 18:39 to 18:58 AEDT in my own
scratch `fleet/state/s317/g2000/`: `clone` and `clone2` (clone.py draft: push URL `invalid://no-push`, no identity);
worktrees `red` (BASE, then + `1-red.diff`, then + `2-fix.diff`), `l5chk` (the head + L5's patches, apply only) and
`mfk` (FK's head + L4's diff = the merge with main of the moment). Every dotnet job and test executable through the
kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (lock waits 0 in every runner line I printed;
the mutants tool does not print its 28 runner lines; no other holder's lock touched; 43 released lock folders, mine,
in `g2000/_quarantine/locks/`; the lock absent at the end). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull request, no re-run; the lab tool never run
(the command was driven in-process by the test assembly against the tests' own 127.0.0.1 stub only); nothing deleted
(probe file, a probe run folder and the scanner control moved to `g2000/_quarantine/`).

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`red` after both: `write-tree` `d60819db` = the
head's tree by gh api and by git; both patches and the ten tools equal THE TOOLS' sha256 in my copy and in the seat's
`.tools/b1992/gate`; the commit message equals `commit-message.txt`, 251 bytes). 13 paths (6 A, 7 M), the owned set;
`checks_l4.py` 6 of 6 with every control. Red first at BASE + `1-red.diff`: 1968 / 8 failed / 1956 / 4, the eight
R01, R04, R05, R06, R08 (`--pages` 0 and 601), R09 (`--port`), R10, each by its own assertion (6 `Assert.Equal()`, 2
`Assert.Contains()`), 0 `Exception` lines. Green 1968 / 0 / 1964 / 4. Mutants (my run of the frozen tool):
`MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`, every row `Total 63`. Nothing on the `--execute`-less path
constructs the transport, and the gate MEASURED the dry run under ten argument orders (0 TCP connections in each) and
ONE TCP connection, at most one request, on every send path (accepted, 600 pages, wrong pin, busy, silent). The
synthetic PDF opens unrepaired in two independent parsers (poppler 26.11, Apple PDFKit) at 1, 2 and 600 pages. The six
extra paths are each necessary (NOREF and P13 re-run). Hosted push run 45131837251 PASS on both legs (linux 1964,
windows 1947; R06 and R07 green on Windows). The merge with main of the moment (`86473f8a`, tree `9611a597`):
1971 / 0 / 1967 / 4, RULES 635, locally. Two Minor findings (repository text against two shapes; neither sends a byte,
neither blocks the landing).

## FOUND

1. **Minor (a "never" sentence false on one shape).** Print `README.md:24` to `:25`: "No document byte and no pin is
   written or printed". A pin typed where an option name belongs (`print 127.0.0.1 --run <r> <pin> --port <p>
   --execute`) is echoed by the parser's `"unknown option " + name` (`PrintCommand.cs:108`). MEASURED (gate probe B1,
   in-process against the stub on 127.0.0.1): exit 2, 0 TCP connections, 0 requests, the pin in the output (not
   reprinted here). `no value after <name>` (`:55`) has the same form. The kit's FRAME row 4 (c) names the echo of an
   option NAME but not this shape. A pin is the SHA-256 of a device's public certificate, not a secret; the run folder
   is not created (usage comes first), so nothing is written. Fix (a later round, the coordinator's order): do not
   echo a word that is 64 hex characters (or any value-like word), or scope the sentence to "of what it parsed".
2. **Minor (the exit-code list does not hold outside the send).** Print `README.md:27` to `:28` lists 0, 2, 4, 5, 6, 7
   ("7 any other failure"). A blank `--run` value (`--run " "`) passes the parser (`:71` to `:73` take any string) and
   `RunRecorder.Create` throws `ArgumentException` (`RunRecorder.cs:26`, landed with L1): MEASURED (probe B8:
   `System.ArgumentException` out of `LabCommands.RunAsync`, 0 TCP, 0 requests); in the tool that is an unhandled
   exception, not exit 2. A folder the tool cannot create (permissions) takes the same path (DERIVED from
   `RunRecorder.cs:33`, `Directory.CreateDirectory` uncaught). `probe` has the same shape (`ProbeCommand.cs:61` to
   `:63`, `:185`; DERIVED, L1's). Nothing is sent. Fix: refuse a blank `--run` in the parser (usage, 2) and name or
   catch the folder's I/O failure; records line (FOR-RECORDS.md item 2).

## INFO (each the gate's own reading; DERIVED marks source reading, not run)

1. **The dry-run branch at the head** (`awk`-checked by reading the file whole): `PrintCommand.cs:175` parse, `:176`
   to `:181` usage before anything; `:183` to `:188` the run folder (exit 5) before the document; `:190` the document
   in memory; `:198` `if (!options.Execute)` adds the dry-run line only; `:204` the ONE call of `SendAsync`; `:218`
   `new HttpIppTransport(` (the only construction in `src/Datasec.Suite.Lab`, `git grep` at the head: one hit) inside
   `SendAsync`. No other path reaches `SendAsync`. MEASURED: R01 0 TCP; gate probes below.
2. **Argument orders (gate probe `G2000Probe.cs`, one `[Fact]` recording facts, built into the Lab test executable in
   `red` only, `Total: 64, Failed: 0`, then moved to `_quarantine/G2000Probe-red.cs`; output
   `scratch/probe-out/shapes.txt`).** A2 `--run --execute` (no other `--execute`): exit 0, DRY, 0 TCP, a run folder
   literally named `--execute` in the test host's working folder (moved to `_quarantine/`); A3 `--execute` twice: 1
   TCP, 1 request; A4 `--execute` before the host, A5 `--Execute`, A6 `--execute=true`, A7 `--pages --execute`, A8
   `--path --execute`, A9 `-execute`, A10 `--pin --execute`: each exit 2, 0 TCP. So the dry-run sentence holds under
   every order tried: only the literal token in an option-NAME position sends.
3. **Exactly ONE Print-Job, never retried (MEASURED, TCP connections counted at the stub's Kestrel connection
   middleware).** A1 accepted 1 TCP / 1 request; C4 600 pages 1 / 1; C1 wrong pin 1 / 0 (exit 4); C2 busy 1 / 1 (exit
   6, `not sent again`); C3 silent at 2 s 1 / 1 (exit 7, `failed: ResponseTimedOut, transport none`). DERIVED: no loop
   in `SendAsync` (`:216` to `:250`); the sender's `SendAsync` calls `ExchangeAsync` once (`PrintJobSender.cs:76`);
   the transport sends `Connection: close` on a handler with `PooledConnectionLifetime = 0` (`HttpIppTransport.cs:40`,
   `:63`) and its body content refuses a second serialisation (`RequestReplayed`, `:200` to `:203`). A refused
   connection (R06) has no listener to count: DERIVED only.
4. **The pin and the port cannot be bypassed (MEASURED + DERIVED).** `PrintCommand.cs:113` refuses a missing pin,
   run or port (R09); `CertificatePin.Parse` (64 hex, either case, lower-cased) and `HttpIppTransport.ParsePin` both
   require 64 hex; the transport's only trust is the leaf hash (`HttpIppTransport.cs:44`, `:171` to `:180`, landed,
   gate B1983). B2 `--pin` last with no value: exit 2; B3 upper-case pin: sent (1 / 1); B4 wrong then right pin: the
   later wins, sent; B5 right then wrong: exit 4, 0 requests; B6 `--port 1 --port <stub>`: the later wins, ONE send;
   B7 `--port +631`: exit 2 (`NumberStyles.None`). A port of 0 cannot be given (`< 1` refused at `:75`); `port == 0`
   at `:113` means "not given".
5. **`ReasonKeepingTransport` changes no behaviour (DERIVED, `PrintCommand.cs:127` to `:144`).** It awaits the inner
   call, returns its stream unchanged, records `IppTransportException.Reason` and rethrows the same object (`throw;`);
   any other exception passes untouched. The sender sees the same exception it would have seen
   (`PrintJobSender.cs:311` to `:313`). `mReasonDropped` changes only the printed reason (R04, R06 red, nothing else).
6. **The synthetic PDF (MEASURED by two independent parsers on the probe's bytes of `SyntheticPdf.Make(1)`, `(2)`,
   `(600)`).** poppler 26.11.0 `pdfinfo`: Pages 1 / 2 / 600, A4 595 x 842, PDF 1.4, 600 / 878 / 174429 bytes, no
   `Syntax` or error line; `pdftotext`: 0 stderr lines for each, 600 lines "lab synthetic page", the first "1 of 600",
   the last "600 of 600"; `pdffonts`: Helvetica Type 1, not embedded (a standard font; a printer's rendering
   UNMEASURED). Apple PDFKit (`swift`, `scratch/pdfcheck.swift`): page counts 1 / 2 / 600, every MediaBox 595 x 842,
   first and last page text as above. The xref rows are 20 bytes ("nnnnnnnnnn 00000 n" + SP LF, a form the PDF
   standard allows), DERIVED from `SyntheticPdf.cs:59`.
7. **The READMEs against the code.** Print README: usage (`:3`) = `PrintOptions.Usage`; "connects to nothing" (I1,
   I2); "the same page count gives the same bytes" (D02; no clock, random or file in `SyntheticPdf.cs`, read); "No
   file is read" (true); "it carries no job attribute" (true: `JobAttributes` empty; `job-name` is an operation
   attribute); "TLS and HTTP/1.1 only; no proxy, no redirect, no retry; the body is streamed (chunked)" (the
   transport's, R03 `chunked`); "`--timeout-seconds` bounds the whole send ... and, up to 15 seconds, the connection"
   (`:221`, `:224`; true as an upper bound: INFO 9); "only the job id, the job state and the IPP status" (`:236`,
   `:241`, `:247`); exit codes (FOUND 2). Lab README: the `print` bullet, "`print` refuses a command line without
   `--pin`" (R09), "`print` writes only `summary.txt` there" (R01, R02; FOUND 2's shape writes nothing). The Trust
   paragraph's "every call has a time bound, and an answer is read to 1 MiB at most" holds for `print` (the sender
   reads at most 65536 bytes of an answer's packet, `PrintJobTypes.cs:29`). `DeviceChannel.cs:37` "The probe's ONE way
   to a device": `new DeviceChannel(` occurs once under `src/`, in `ProbeCommand.cs:193` (the other three in
   `ChannelTests.cs`).
8. **`CommandRegistry.cs:19`'s false comment is named for records**: the kit's FOR RECORDS item 3 and the seat's FOR
   RECORDS (RELAYED, copied); the line reads so at the head. Also in FOR-RECORDS.md.
9. **Bounds (DERIVED, the seat's H16 (1), confirmed).** `SendTimeout` = the option; `ResponseTimeout` stays at the
   sender's 60 s default (`PrintJobTypes.cs:26`), armed after the HTTP headers (`PrintJobSender.cs:326`): above 60 s,
   an answer stalled after its headers ends at 60 s. At 15 s or below the connect bound equals the send bound
   (`PrintCommand.cs:221`): a timed-out connection may read `ResponseTimedOut, transport none` (the bounds race;
   C3 printed `transport none`).
10. **Host shapes (MEASURED).** B9 `localhost`: sent (1 / 1); B10 `[::1]`: exit 2 (the seat's H16 (2)); B11
    `127.0.0.1/x`: exit 2; B12 `--path /ipp/%2e%2e/print`: sent (the transport sends the path it is given; the
    stub accepted it).
11. **Cosmetic.** The Lab README's re-flowed lines are 177 and 128 characters (`README.md:23`, `:29` at the head; the
    file wraps at 120, one line at BASE was 123).
12. **No CodeQL row on the branch head** (`check runs beside the four: 0`, my hosted3 read): the pull request's run is
    the first analysis of this code (landing.txt step 3 names what an analyst looks at).

## THE KIT'S GATE LIST (its FOR TUESDAY, verbatim items, each with the gate's result)

- **read `<BASE>..<head>` whole**: DONE (the 13 files whole at the head, the seven M files by their diff; also read
  whole: `PrintJobSender.cs`, `PrintJobTypes.cs` 1 to 80, `HttpIppTransport.cs`, `HttpIppTransportOptions.cs`,
  `CertificatePin.cs`, `RunRecorder.cs`, `Program.cs`, `CommandRegistry.cs`, `BoundaryTests.cs` 1 to 50,
  `ProbeTests.cs` 1 to 60).
- **the two patches against THE TOOLS' sha256**: `1-red.diff` `777b1674...`, `2-fix.diff` `83fe0d61...`, and the other
  eight files, equal in `d1992/seat-tools`, my `g2000/gate` and the seat's `.tools/b1992/gate` (10 of 10 each).
- **the red first of `1-red.diff` at BASE (`failed: 8`, the cells, by assertion)**: REPRODUCED (BLUF; log
  `g2000/logs/red-test.log`; restore `--locked-mode` `CI=true` rc 0, 10 status rows, 5 M + 5 ??; build 0 / 0, the
  transport built Release once). `2-fix.diff` alone refused at BASE (rc 1, control).
- **each of the 14 mutants red on exactly its cells**: REPRODUCED, all 14 rows MATCH, undone equal; after them the
  worktree equals the staged head (`git diff --quiet` rc 0). Independent of the seat's run, same frozen tool.
- **nothing on the `--execute`-less path constructs the transport**: CONFIRMED (INFO 1, 2).
- **no line printed or written holds the pin or a document byte**: holds on every tested and probed path but one
  (FOUND 1). R01, R02, R04 and every probe line but B1: the pin absent; the summary of R02 holds no page text; the
  dry-run folder of A2 holds only `summary.txt` (its four lines read: no pin; the document named by length and
  SHA-256 only).
- **the six paths beyond the commission (D1)**: each necessary: NOREF (the transport line out: build rc 1, CS0234
  and CS0246), P13 (the old list back: `Total: 63, Failed: 1`, only P13, `Collections differ`), both undone and proved
  (sha256 equal); the lock files are written by the restore (my locked restore with them rc 0 and no status change);
  `DeviceChannel.cs:37` and the Lab README sentences would be false without (INFO 7).
- **the hosted run on both legs**: my `hosted3.py 26f4b57a... --total 1968 --rules 634 --skipped-linux 4
  --skipped-windows 21 --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`: `HOSTED
  26f4b57a619bb2c4b7009be5584e2e1580a1b127: PASS` (run 45131837251, attempt 1; linux 1964, windows 1947, `GUARD`
  14 and 15, `RULES: clean (634 files)`, `Ran 111`, secret-scan every proof line; `failed Datasec.` 0 and 0 with
  `-i`, control `total: 1968` 2 and 2; `Datasec.Suite.Lab.Tests.dll` 4 and 4; `Datasec.Suite.Jobs.Transport -> ` 1
  and 1).
- **`words.py` and `gitleaks` over the added lines and the message**: SCANS below.

## WIDER (commission item 2)
Dry run under every argument order: INFO 2. Exactly one Print-Job, never retried: INFO 3. Pin and port: INFO 4. The
PDF's structure: INFO 6 (MEASURED, two parsers). `ReasonKeepingTransport`: INFO 5. The READMEs: INFO 7, FOUND 1, 2.
`CommandRegistry.cs:19`: INFO 8. The six paths: the gate list above (NOREF and P13 re-run).

## FRAME QUESTION (stamp item 11): each every / never / all sentence the lane adds, three shapes outside the tested one
| Sentence | Three shapes outside the tested one | Covered by |
|---|---|---|
| "Without `--execute` it is a dry run ... connects to nothing" (Print README `:6`, `PrintCommand.cs:149`) | `--execute` as `--run`'s value; as `--pages`' / `--path`'s / `--pin`'s value; misspelt or before the host | gate probes A2, A7, A8, A10, A4 to A6, A9 (MEASURED, no cell); R01 the tested one |
| "No document byte and no pin is written or printed" (`:24`) | the pin as a stray word; the pin given twice; an upper-case pin | B1 FALSE (FOUND 1); B4, B5, B3 hold (MEASURED); R01, R02, R04 cells |
| "only the job id, the job state and the IPP status are [printed]" (`:25`) | busy; silent; wrong pin | R05, C3, R04 (each prints status or reason names only) |
| "6 ... (it is not sent again)" (`:28`) | busy (TCP count); another refusal status; a second `--execute` token | C2 1 TCP (MEASURED); same branch `:239` (DERIVED, no cell, the kit's H5); A3 one send (MEASURED) |
| "The same page count gives the same bytes" (`:10`, `SyntheticPdf.cs:8`) | 1 and 600 compared at the stub; 3 vs 4; another culture | R02, R03; D02; `InvariantCulture` on every number (DERIVED, no cell) |
| "Only ASCII is written; nothing is read from any file or device" (`SyntheticPdf.cs:9`) | 1, 2, 600 pages; an independent parser; the page text | D01; poppler and PDFKit (MEASURED); source read |
| "`--pin` and `--port` are required: there is no first-contact mode" (`:16`) | `--pin` last with no value; a port of 0 or `+631`; a wrong then right pin | B2, R08, B7, B4 (MEASURED) |
| "One run sends one job to one port" (`:34`) | `--port` twice; `--execute` twice; a busy answer | B6, A3, C2 (MEASURED, one send each) |
| Lab README "`print` writes only `summary.txt` there" | a dry run; a send; a blank `--run` | R01, R02; B8 writes nothing (FOUND 2 is its exit code, not a write) |
| `DeviceChannel.cs:37` "The probe's ONE way to a device" | the print command; tests; later commands | 0 constructions in Print (git grep); ChannelTests only; L5 out of scope |

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by program from two halves and 36 random characters, never printed,
  outside any clone, scanned alone): rc 1, `leaks found: 1`, moved to `g2000/_quarantine/gl-control`. Then the 13
  head blobs, both patches, `commit-message.txt`, `mutants_l4.py`, `checks_l4.py` as `1.txt` to `18.txt`: rc 0, `no
  leaks found`; the added lines (783 and 796) and the head's message: rc 0; `gitleaks git` over
  `d804de5e..26f4b57a`: 1 commit, rc 0, `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over `added.txt` (783 lines, 36872 bytes, byte-equal to
  `checks_l4.py`'s own `added.txt`) and the head's message: `WORDS: clean (2 files)`; over the 796 lines with the lock
  files: `WORDS: clean (1 files)`. My landing texts `squash-subject.txt` (with #39), `squash-body.txt`, `pr-title.txt`:
  `WORDS: clean (3 files)`. `build/squash_scan.py` from main 86473f8a's build/ (`clone2`, TMPDIR in my scratch),
  subject with #39: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`. `pr-body.md` names the
  coordinator and the product owner on purpose (who decides) and is not a repository text.

## MAIN MOVES
- **Main moved during the gate**: `d804de5e` -> `86473f8a` (FK, pull request 38, one parent `d804de5e`, tree
  `2d6d5400` = FK's head tree). Its push run 45133195497: `HOSTED 86473f8a...: PASS` at `--total 1945 --rules 629`
  (linux 1941, windows 1924; three Analyze rows success; analyses csharp/python/actions results 0 at 86473f8a); open
  alerts 0; open pull requests 0 (18:50:45).
- **The merge with main of the moment**: `git merge-tree --write-tree 86473f8a 26f4b57a` rc 0, tree `9611a597`
  (= gate B1998's measured `merge-tree 26f4b57a 81ae47ed`). Worktree `mfk` = FK's head + L4's diff: index tree
  `9611a597`, 635 files; locked restore `CI=true` rc 0 (worktree equal to index after it); build 0 / 0; `total:
  1971`, `failed: 0`, `succeeded: 1967`, `skipped: 4`; `RULES: clean (635 files)`. Windows on that tree: 1950
  PREDICTED (1924 + 26). FK changed no Lab path (`git diff --quiet d804de5e 86473f8a -- src/Datasec.Suite.Lab
  tests/Datasec.Suite.Lab.Tests` rc 0).
- **L5 (kit B1997, not launched)**: nothing in L4's head makes L5's frozen patches fail to apply. In `l5chk` (L4's
  head): L5 `1-red.diff` `--check` rc 0, applied, then `2-fix.diff` `--check` rc 0 (control: `2-fix.diff` alone rc 1);
  on the FK + L4 merge tree `9611a597` (a temporary index only): the same, rc 0 and rc 0; at `d804de5e` L5's
  `1-red.diff` fails (`CommandRegistry.cs:24`), so L5 needs L4 first, as ordered. Not built or tested by this gate.

## HOOK REFUSAL
One command was refused by the harness's scope hook (`pretooluse_recursive_scope.sh`: a `grep -r` naming one file
under `fleet/state`); that action stopped there. The file it named (`CertificatePin.cs`) was then read with the Read
tool, as every other source file of this gate was.

## NOT RUN
CodeQL (none locally; none on the branch head); the hosted run of the merge ref (the pull request is not open); the
Windows leg of the merge tree (PREDICTED 1950); `repo_rules.py --source-documents` (forbidden); the container image;
the lab tool itself (never run), any printer, simulator or address but the tests' 127.0.0.1; a probe of a connect
time-out or of an HTTP 401 / 500 answer (DERIVED from the transport only); the `--force` lock-file chain (the seat's,
RELAYED: `LOCKS: 34 of 34 equal`).

## TREES LEFT (all in `fleet/state/s317/g2000/`)
`clone` (BASE checkout, push URL invalid), `clone2` (main 86473f8a, push URL invalid), worktrees `red` (the head tree
staged, `bin/` and `obj/` kept), `l5chk` (L4 head + L5 `1-red.diff` applied, never built), `mfk` (the merge tree
staged); `gate/` (the ten tools); `logs/`; `scratch/` (scripts, probe output, neutral copies, the mutants' keep
folder, `d1keep/`, `fkmerge.index`); `_quarantine/` (locks, `gl-control`, `G2000Probe-red.cs`,
`A2-run-folder-named--execute`). No process left running; the heavy lock not held by me.
