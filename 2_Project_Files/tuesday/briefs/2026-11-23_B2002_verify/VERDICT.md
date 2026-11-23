GATE B2002: GO WITH FINDINGS @ f0cd57a on main 57e9042

Gate G1 (an admin credential, TLS trust, key material), round 1 of 2 of lane L5, one Opus reader (claude-opus-5-5),
in-session, read-only. OXPd 2, lane L5, kit B1997 (seat X56; Q1 and Q10 "a" in words at stamp S4, Q2 to Q9 the
defaults; each the coordinator's, not the product owner's). Head `f0cd57a321678d7a95c2aaeaab9f7df4e8413a86` on
`b1997/l5-oxpd1-lab-read`, ONE commit, one parent `57e9042a` (BASE = main = L4's squash, PR 39). Main did NOT move
during the gate (57e9042a by clone at 19:40 and by gh api -X GET at about 19:45). Read and measured 2026-11-23 19:39 to
19:55 AEDT in my scratch `fleet/state/s317/g2002/`: `clone` (clone.py draft: push URL `invalid://no-push`, no
identity), worktrees `red` (BASE + `1-red.diff`) and `pat` (BASE + both patches, staged; later + a gate probe file, now
in `_quarantine/G2002Probe.cs.txt`). Every dotnet job and test executable through the kit's `heavy.py` (sha256
`31adedc8...`) and the wave lock, one at a time (lock waits 0 on every runner line printed; 43 released lock folders,
all mine, in `g2002/_quarantine/locks/`; the lock absent at the end; no other holder's lock touched). Origin by
`gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull request, no
re-run; the lab tool was never started (the command was driven in-process by the test assembly against the tests' own
and the probe's 127.0.0.1 stubs only); no printer, no tenant; the project's 4_Credentials not read (only the gh config
dir used by `gh`); nothing deleted.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`pat` `write-tree` `29be6357` = `f0cd57a3^{tree}`;
`red` = BASE + `1-red.diff`, tree `0e45cf1d`); both patches and the ten tools equal THE TOOLS' sha256 in my copy and in
the seat's `.tools/b1997/gate`; the commit message is the tool's 3 lines. 19 paths (8 A, 11 M), numstat equal to the
kit's table; `checks_l5.py` 7 of 7 with every control. Red first: Lab 95 / 15 failed, client 27 / 1 failed, the 16
planted cases exactly; 15 by an `Assert.` line, L01 by `InvalidOperationException: Sequence contains no elements` at
`LabCertTests.cs(51)`, the `.Single()` over the alternative-name extension: the planted missing SAN (the red shape also
omits the EKU, `:55`, never reached), nothing else (ANSWER-1's acceptance holds). Green 2007 / 0 / 2003 / 4.
`MUTANTS: 15 of 15 MATCH, 15 of 15 undone equal` (my run of the frozen tool; clone clean after). **The G1 question:
MEASURED, 18 of 18 shapes give exactly ONE password-bearing request** (401, 403, 401 with a Basic challenge, 307, SOAP
fault, time-out, connection dropped after the POST, dropped on the first POST, connection closed after the tree; each on
one shared port, where the POST reuses the tree's pooled connection, and on two ports) and in none is the password or its
Basic token in the output or the run folder. The environment, argument order and every other option give no password
source but the file. Hosted push run 45139381044 PASS on both legs (linux 2003, windows 1986, RULES 643). Two Minor
findings and five Info; none sends a byte, none blocks the landing.

## FOUND

1. **Minor (a "never printed" sentence false on three shapes).** Commands/Oxpd1 `README.md:24` "The password is not
   printed" and the kit's P2 ("never printed"). The parser echoes an unknown word: `"unknown option " + name`
   (`Oxpd1Command.cs:133`) and `"no value after " + name` (`:52`). MEASURED (probe SOURCE rows): `--password=<value>` as
   one token (both as last and as last-but-one argument) and a bare `<value>` at the end each exit 2, 0 TLS connections,
   0 requests, **the value in the output**. (`--password <value>`, R06's shape, consumes the value silently: not echoed;
   `-p <value>` and `--Password <value>` not echoed.) The value is already on the command line in these shapes, so this
   is an operator-error path, but agents drive this tool and its output lands in transcripts. Same class as B2000 FOUND 1
   (print). Fix (a later round): never echo an argument the parser did not recognise (print its position, or only a
   word that starts `--` and holds no `=`), or scope the sentence.
2. **Minor (exit codes 7 and 2 do not hold on four inputs).** README `:23` to `:24` "A missing file, name or value ends
   the run with exit 7 before any connection". MEASURED: a credentials file with mode 000 -> `UnauthorizedAccessException`
   out of `LabCommands.RunAsync` (unhandled in the tool), 0 TLS connections, the run folder created and left EMPTY; a
   dangling symbolic link as the credentials file -> `FileNotFoundException` from `CredentialsFile.Read`
   (`LabFiles.cs:18` `File.Exists` is true for it, `:24` `File.ReadLines` throws); a blank `--credentials-file " "`
   and a blank `--run " "` (both verbs) -> `ArgumentException` (`LabFiles.cs:17`, `:54`). Nothing sent in any; no
   exception text holds the password (MEASURED false in each). Same class as B2000 FOUND 2. Fix: catch
   `IOException`/`UnauthorizedAccessException` in the reader (exit 7), refuse blank values in `Parse` (exit 2).
3. **Info (the 2004 anonymous address).** `Oxpd1Soap.cs:21` `Anonymous2004 = ".../ws/2004/08/addressing/role/anonymous"`
   agrees with the W3C Member Submission "Web Services Addressing" of 10 August 2004 as this reader knows its text (the
   2004/08 namespace's anonymous URI is `.../role/anonymous`; WS-Addressing 1.0 dropped `/role`). NOT fetched in this
   session (no network but GitHub and 127.0.0.1) and no committed file holds it (`git grep` over the head: the
   2004/08 namespace appears only as the HP WSDLs' declared prefix); what an M577 accepts is UNMEASURED.
4. **Info (lab-cert's name rule).** MEASURED over 28 names: every IP form tried is refused (`127.1`, `2130706433`,
   `0x7f000001`, `0177.0.0.1`, `127.0.0.01`, `1.2.3`, `[::1]`, `::ffff:127.0.0.1`, `fe80::1%en0`, `::`, `0.0.0.0`,
   `255.255.255.255`, `1.2.3.4.`, `127.0.0.1:443`) with exit 2 and no run folder. Accepted, beyond the cells:
   `printer_lab.example` (an underscore: not a valid host name by RFC 1123 though `Uri.CheckHostName` says Dns),
   `localhost.localdomain`, a non-ASCII name, `1.2.3.4.nip.io`, and a single label `printer-lab`. None is an IP address;
   whether a device resolves or accepts them is UNMEASURED. `--days` 0, 398, -1 refused; 1 and 397 written.
5. **Info (Windows key file).** `LabCertificate.cs:184` to `:187`: off Windows `server.key` is created 0600 (MEASURED
   `UserRead, UserWrite` locally and L01 green on the linux leg); on Windows no mode is set, so the file takes the run
   folder's inherited ACL. The README says "on macOS and Linux readable by its owner only" and is silent on Windows; a
   line there would make the platform branch explicit. The CA key's lifetime: `RSA caKey` and the key-bearing `ca` are
   disposed at the end of the `using` block (`:155` to `:176`); only `caPublic` (loaded from `RawData`, no key) leaves
   `Make`; the only private-key export is `serverKey.ExportPkcs8PrivateKeyPem()` (`:126`). No failure path writes a CA
   key (none can: no CA key export exists; MEASURED: a run folder under a file -> `DirectoryNotFoundException`, nothing
   written; an existing folder -> exit 5, 0 files). Whether the platform persists the ephemeral key anywhere (a Windows
   key container, a macOS keychain) is DERIVED no, UNMEASURED.
6. **Info (parser leniencies, no new request).** `--read 'GetManufacturerInfo,GetSignInMethods'` parses (enum flag OR)
   to `GetSignInMethods`; `'GetSignInMethods '` (trailing space) parses; both are still ONE defined read (MEASURED).
   `--credentials-file` given twice: the last wins (MEASURED). The `Addressing` refusal names the parameter `value`.
7. **Info (records).** `DeviceChannel.cs:37` "The probe's ONE way to a device" (L4's) is untrue once this lands: the
   first contact uses the channel and the pinned read goes through the client (FOR-RECORDS.md). The seat's STATUS keeps
   a stale `PREDICTIONS ... (so far)` section ("P2 to P6: not reached") beside the final one, and its first line still
   reads `PROGRESS B1997: PENDING`; its last line is `READY B1997: f0cd57a3...`, which is what counts.

## THE KIT'S GATE LIST (FOR TUESDAY)

- `BASE..head` read whole: the 4 Oxpd1 command files, the 4 client diffs, the 3 test files and the stub, the registry,
  `.csproj`, README and lock-file hunks; the landed `DeviceChannel.cs`, `CertificatePin.cs` (`CertificateCheck`),
  `RunRecorder.cs`, `PlannedCall.cs`, `Program.cs`, `Oxpd1Client.cs` whole, `Oxpd1ReadResult.cs`.
- Patches and tools: 10 of 10 sha256 equal (both copies). Head tree = BASE + both patches (above).
- Red first: above (16 cases; L01's `.Single()` red is the planted missing SAN).
- Mutants: 15 rows, each red on exactly its listed cells, Totals 95 (Lab) and 122 (`mSeamIgnored`, both executables).
- A second password-bearing request: structurally ONE `ReadAsync` call (`Oxpd1Command.cs:312`), no loop, every
  `switch` arm returns (`:314` to `:330`); the tree GET carries no `Authorization` (`Oxpd1Client.cs:100` to `:108`: the
  header only with an envelope); the client's handler sets no `Credentials` (no challenge answered), `AllowAutoRedirect
  = false` (no redirect resend), and `HttpClient.Timeout` infinite with one linked token (no client-level retry). The
  HTTP layer's own retry on a reused connection was the open question (kit H4): MEASURED not to fire on a POST dropped
  after it was read, nor after the tree's connection was closed (one shared port), on macOS / .NET 10.0.404. On
  Windows and Linux only R02/R03 (hosted, green) measure it; the probe was not run there.
- The password's reach: output lines (`Oxpd1ReadResult.ToString` = outcome, status, scrubbed fault code), the summary
  (= the output lines), the client record (`Record` scrubs request and answer with the password and its Basic token;
  logs the URL), exception texts (MEASURED: none of the four exceptions above holds it). 18 READ shapes: 0 hits for the
  password or the Basic token in output and every run-folder file. The one leak path is FOUND 1 (operator-typed value).
- Run folder on a linked work tree: a `.git` FILE is refused (R07, and probe); a `.git` symlink (to a folder or
  dangling) is refused; a symlink INTO a work tree is not (H13, MEASURED); a relative path is resolved against the
  current folder (MEASURED: refused inside a work tree).
- lab-cert's key handling: FOUND 5. The Windows path: no mode set (D8), the hosted windows leg green with L01's mode
  assert skipped by the code's platform branch (`LabCertTests.cs:68`).
- The 2004 anonymous address: FOUND 3.
- Hosted run on both legs: `hosted3.py f0cd57a3 --total 2007 --rules 643 --skipped-linux 4 --skipped-windows 21 --unit
  111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`: run 45139381044, attempt 1, every step success;
  linux `total: 2007` x2, `succeeded: 2003`, `skipped: 4`, GUARD 14; windows `succeeded: 1986`, `skipped: 21`, GUARD 15;
  secret-scan both PLANTED-CONTROL lines, `no leaks found` x3, NEUTRAL lines `wrong 0`, `not among ... 0`; rules
  `RULES: clean (643 files)`, floor 111; `HOSTED f0cd57a3...: PASS`, rc 0; `failed Datasec.` 0 and 0, Lab test dll 4
  lines per leg. Check runs beside the four: 0 (no Analyze row on the branch push: the PR's run is the first analysis).
- words and gitleaks: below (SCANS).

## WIDER (G1 depth): measured by a test-only probe (`_quarantine/G2002Probe.cs.txt`, never committed; results
`g2002/scratch/probe-results.txt`, counts only, no value; Lab executable whole `Total: 96, Errors: 0, Failed: 0`)

- One password-bearing request: 18 of 18 (above). Exits: 401/403/challenge/close-after-tree 6; 307/500/time-out/drops 8.
- No other source: the environment variable of the default name set with a file lacking it -> exit 7, 0 connections; a
  `--password-name` that exists only in the environment -> exit 7; options before the host -> exit 2; the right file
  given last of two -> its value used (exit 6, 1 request); otherwise exit 2 or 7 with 0 connections. L03 counts
  `Environment.` 0 in the folder (green); `Process`, `X509Store` 0.
- Credentials reader: a symlink to a file is followed (the value read); a folder -> null (exit 7); mode 000 and a
  dangling link throw (FOUND 2).
- lab-cert: FOUND 4 and 5.
- `Oxpd1ClientOptions.Addressing`: default `Version200508`; -1, 2, 7 and `int.MaxValue` refused with
  `ArgumentOutOfRangeException`; the enum is `Version200508=0, Version200408=1` (A02 green).
- READMEs against the code: the command README's verb sentences hold but for FOUND 1 and 2 and the Windows silence of
  FOUND 5 ("Without --pin ... no password is read": `FirstContactAsync` never calls the reader, true; "exit 7 before any
  connection" is on the pinned path, the only path that reads it); the Lab README entry and the client README's switch
  paragraph hold.
- The two registry cells: `ProbeTests.cs:207` and `Print/PrintTests.cs:188`, numstat `1 1` each (check 6), the list
  `["probe", "print", "oxpd1"]` in both; R11's second line (`All[1]` is `PrintCommand`) unchanged.

## FRAME (stamp checklist item 11: three shapes outside the tested one per every/never/at-most-once sentence)

| Sentence | Shapes outside the tested one | Cell, probe or stated limit |
|---|---|---|
| P1 at most ONE password-bearing request per run | handler retry on a dropped reused connection; a 401 challenge; a 307; a time-out; a second run | probe 18/18 (MEASURED macOS); H6 limit (per run) |
| P2 never taken from the command line | env var; `--password-name` naming an env-only name; repeated `--credentials-file` | probe: none taken |
| P2 never printed | `--password=<v>`; a bare `<v>`; an exception text | FOUND 1 (echoed); exceptions MEASURED clean |
| P3 no run folder in a git work tree | `.git` symlink; symlink into a work tree; relative path; `GIT_DIR` only | probe: refused, NOT refused (H13), refused; H14 limit |
| P4 never writes to a device | `--read` combined flags; numeric; `Set*` | probe: still one defined `Get*` read; numeric refused; R09 |
| P5 never an IP address | octal/hex/short/decimal IPv4, bracketed/mapped/scoped IPv6, trailing dot, port | probe: all refused |
| P5 no CA key written | failure before Make; folder exists; folder under a file | probe: no file / 0 files; no CA-key export in the code |
| P6 the addressing asked for, 2005 by default | undefined values (-1, 2, max) | probe: refused |

## SCANS

- gitleaks 8.30.1: control FIRST (a GitHub-token-shaped value built by a program, never printed, alone in a new folder):
  rc 1, `leaks found: 1`, folder moved to `g2002/_quarantine/gl-control`. Then the added lines (1228, lock files out),
  the commit message as committed and the head's 19 changed blobs under neutral names `1.txt` to `21.txt`: rc 0, `no
  leaks found`.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; added lines + the commit message `WORDS: clean (2 files)`; the
  squash subject (with #40), squash body and PR title `WORDS: clean (3 files)`.
- squash_scan.py (the head's `build/`, equal to main's): subject with #40 + `squash-body.txt`: control rc 1 found 2,
  message rc 0 found 0, `SQUASH-SCAN: clean`.

## THE CHAIN AND THE MERGE

- Head (`clone`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test`: `total: 2007`, `failed: 0`,
  `succeeded: 2003`, `skipped: 4`. `pat`: `repo_rules.py` (no `--source-documents`) `RULES-NOTE: R5 hash half NOT RUN`,
  `RULES: clean (643 files)`; `unittest` `Ran 111 tests` OK; `checks_l5.py` 7 of 7.
- Merge with main of the moment (57e9042a = BASE): `git merge-tree --write-tree` rc 0, tree `29be6357` = the head's.
  The merge is the head; measured above. Open PRs 0; open code-scanning alerts 0; main's analyses results 0.

## NOT RUN

- The probe on Windows and Linux (the one-request result is MEASURED on macOS only; the hosted legs ran the cells).
- CodeQL locally; the PR's merge-ref run (does not exist yet).
- An independent build of the mutants (my run is of the frozen tool, same as the seat's).
- Any device, simulator or tenant; the 2004 submission's text fetched.

## DISCLOSURE

- One hook refusal: `pretooluse_recursive_scope.sh` refused an unscoped `grep -rn` over my clone's `src/.../Device/`
  (a path under fleet/state). I did not repeat it; I read the two named files by path and used `git grep` inside the
  clone (a git read verb), which is what that search needed.
- My first probe build failed on my own probe file (CA1416, Unix-only file-mode calls); fixed in the probe (marked not
  for Windows) and rebuilt. No lane file was touched.

## LANDING

`landing.txt`, `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md` in this folder.
Who decides to land: the coordinator (Tuesday), never the product owner. FOUND 1 and 2 are for a later round (round 2
of 2 of lane L5 or the shared device-trust lane), not a hold on this landing.
