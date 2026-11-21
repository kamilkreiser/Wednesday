GATE B1859: NO GO @ 5dd0f85 on main 762e774

Gate G1, round 1 of 2, whole-lane reader. OXPd 2, lane G (WP1.7 in part): the job service `Datasec.Suite.Jobs` (encrypted
spool, streaming scan receiver, IPP Print-Job sender with tracking), head `5dd0f8595bc7f243c2ae97585e63fb32ad0d70bb` on
branch `b1841/wp17-scan-and-print-jobs`, one parent = main `762e774eeac2eb324704c7e5ebf0ace86e018f04`. Read and measured
2026-11-21, 19:54 to 20:15 AEDT (clocks by `date`), on Opus 5.5, in the gate's own clone (session scratchpad,
`b1859-clone`, cloned from the seat's clone, push URL `invalid://no-push`; branch and main re-read by `gh api -X GET` at
19:55:13: branch = 5dd0f859, main = 762e774e, open pull requests 0). Scratch and logs: `/private/tmp/b1859-gate/`. The probe
source, its output, the output of the fix sketch, the mutant program and its output and the hosted reading are copied
into `evidence/` beside this file. Every heavy job went through the kit's runner (`heavy.py`, sha256 `31adedc8...`; the
seven kit tools hashed seven of seven equal to the kit): load1 read first, the wave lock
`<project>/.tools/wave1-heavy.lock.d` taken by `mkdir` with `owner.txt`, released by a move into
`/private/tmp/b1859-gate/_quarantine/locks/` (51 releases; no lock folder left under `.tools/`); restores with
`-p:NuGetAudit=false`. `repo_rules.py` never got `--source-documents`; no key folder was opened; every document, secret,
user and session value is synthetic, made at run time, and none is printed here. No socket, no listener, no request to a
printer or host.

**BLUF.** Scope, the solution lines, the two frozen project files, the build (0 warnings), the suite (1081, failed 0), the
hosted run (PASS, `Ran 60`, floor 60, control FAIL 4), 16 of 17 gate mutants (all red, all undone) and 201 of the gate's
213 adversarial outcomes hold, and the raw spool scan finds no form of any document, secret, session, file name or key in
any of 29 encodings. **But the sender lets a raw `OperationCanceledException` out of `SendAsync` and `TrackAsync` when the
printer's answer stream throws one and the caller's token is NOT cancelled** (D17 allows that exception only for the
caller's own token). That is the commission's NO GO class "an exception outside the typed reasons": **one Major, a fix
round follows.** The fix is one filter, sketched and measured below (suite and probes green with it). Three Minors and
records lines besides.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | **Major** | **A raw `OperationCanceledException` leaves the sender.** Measured (evidence/probes.txt): an answer stream whose read throws `TaskCanceledException` (no token of the caller's cancelled) makes `SendAsync` throw `TaskCanceledException` (row G18 "answer stream throws its own OperationCanceledException"); the same answer on every poll makes `TrackAsync` throw it too (row G21). Mechanism: `RunAsync` maps the answer-read failures with `catch (Exception ex) when (ex is not OperationCanceledException and not JobServiceException)` (`PrintJobSender.cs:328`), so an OCE passes through; `ExchangeAsync` and `TrackAsync` re-throw OCE only `when (cancellationToken.IsCancellationRequested)` (`:281`, `:107`), so it is not caught there either, and `PollAsync` catches only `JobServiceException` (`:252`). The transport side handles the same case correctly (`:302`: `ex is not OperationCanceledException \|\| !token.IsCancellationRequested` gives `TransportFailed`; row G18 "transport throws its own OperationCanceledException" = `TransportFailed`), and the comment at `:330` says "never a raw exception to the caller". A real transport that bounds its own reads (the kit names Workpath's "read 15 s", `A3:199`, as the real transport's prior art) would throw exactly this. The suite's J09 throws `IOException` only, so no cell holds it. | One filter at `:328`: `catch (Exception ex) when (ex is not JobServiceException && (ex is not OperationCanceledException \|\| !token.IsCancellationRequested))`. **Measured as a sketch** (applied in the gate's clone, then undone, `git diff --quiet` rc 0): the lane's 108 tests and the gate's 17 probe tests: total 125, failed 0; G18 and G21 then read `TransportFailed` (evidence/probes-with-fix-sketch.txt). Add a J09 row: an answer stream that throws `TaskCanceledException`, for `SendAsync` and `TrackAsync`. |
| F2 | Minor | **A bound is armed only after the caller's code first yields.** `ReceiveAsync` starts `CopyAsync` (`ScanReceiver.cs:195`) and `SendAsync`/`TrackAsync` start `RunAsync` (`PrintJobSender.cs:270`) synchronously; the `WaitAsync` bound is attached to the returned task. A body whose `ReadAsync` blocks its thread, a transport whose `SendAsync` blocks before returning a task, and an answer stream whose `ReadAsync` blocks never return while blocked, whatever the clock does (rows G02 (b), G19 (c) and (d): HANG at the real-time guard with the test clock moved 20 and 31 minutes; each ends typed once freed). Not Major in my reading: a device or a printer cannot cause it (Kestrel's request body and an `HttpClient` transport are asynchronous); it needs a caller-supplied stream or transport that blocks inside an asynchronous method. The kit's property says "never a hang beyond its bound" for whatever "a caller" hands, so Tuesday may grade it up. | `await Task.Yield();` as the first statement of `CopyAsync` and `RunAsync` (or start them with `Task.Run`), so the bound always holds; or one README Limits line. |
| F3 | Minor (cells) | **The spool cap's exact boundary is held by no cell.** The gate's mutant mSpoolCap (`if (_reserved + count > _maxSpoolBytes)` made `if (_reserved > _maxSpoolBytes)`, so a write may pass the cap by one take) leaves all 108 lane tests green (evidence/mutants.out). The gate's own row G05 (spool 1500: job A 1000, job B exactly the 500 left = value, one byte more = `SpoolFull`; reserved back to 1000 then 0 after the wipes) holds on the head and goes RED under that mutant. The product is right; C04 tests the exact file, job and file-count caps but not the spool cap (H5 lists none), and C06's sizes pass the cap by far. | One C04 or C06 row: the spool cap taken exactly and refused at one byte more (G05's rows are ready-made). |
| F4 | Minor (text) | **`ObjectDisposedException` from a receiver and from `Dispose`.** Spool disposed under a running receive: `ReceiveAsync` throws `ObjectDisposedException` (row G13), from `Fail` calling `_spool.WipeJob` (`ScanReceiver.cs:272`) inside its catch; the receiver itself is not disposable, so D17's "on a disposed object" is stretched. A writer whose spool was disposed throws `ObjectDisposedException` from `Dispose` (a `using` block's end at host shutdown), and a writer whose job was wiped throws `JobNotFound` from `Dispose` (both typed or allowed; throwing from `Dispose` is the wording's consequence, D8). The README says "Every refusal is a `JobServiceException`". | Either catch `ObjectDisposedException` in `Fail` and end the receive with `JobNotFound`, or say in D17's README sentence that a disposed spool makes its receivers, writers and readers throw `ObjectDisposedException`, `Dispose` included. |
| F5 | Records | The host has no public way to turn a job id from a destination into a `SpoolJobId` (internal constructor only; the seat's own FOR TUESDAY point). A read after `SpoolCorrupt` keeps refusing (G17: seven further reads all `SpoolCorrupt`, nothing more handed out): good, and worth a cell. A root whose PARENT is a link is accepted (G15; only the root itself is checked, as the README says). `CloseScan` racing an upload that already passed the secret check lets that upload finish (read from source, not measured; consistent with T03, the window bounds the start). | Records; the first is host wiring (NOT DECIDED item 1's neighbour). |

No Blocker. No text names a person, a ticket, a brief or says anyone decided anything (words scan, section 6).

## 1. Scope (measured over `git diff 762e774e 5dd0f859` in the gate's clone)

- `--name-status`: 1 `M` (`Datasec.Suite.slnx`) and 31 `A`: 16 under `src/Datasec.Suite.Jobs/` (14 `.cs`, `README.md`,
  `packages.lock.json`, the `.csproj`) and 15 under `tests/Datasec.Suite.Jobs.Tests/`; 5138 lines added, 0 removed;
  `ls-files` 360 (= 329 + 31). No other path: `Directory.Packages.props`, `ci.yml`, `build/**`, the IPP library, the secret
  store and every existing lock file unchanged; two NEW lock files only.
- The solution file: exactly two added lines, `src/Datasec.Suite.Jobs/...` after `Core` and before `Logging`,
  `tests/Datasec.Suite.Jobs.Tests/...` after `Core.Tests` and before `Logging.Tests`: the ordinal rule against main
  762e774e (which holds `Sessions` lines since lane D landed).
- The two project files extracted from the stamped kit by program: T1 and T2 byte-equal to the head's files (sha256
  `81d9d98f...`, `c1eb2051...` = the sidecar's FROZEN line); T1 (not T1A), as Stamp S4 says.
- The library's lock file lists only the project reference; the test project's lock file holds `xunit.v3` 4.0.3 from
  the central pin (no `PackageReference` with a version, no new `PackageVersion`).
- Every added file ASCII, LF, no tab (0 lines per file; a planted U+200B counts 1). Boundary words (`System.Net.Http`,
  `HttpClient`, sockets, `Console.`, `Environment.`, `Thread.Sleep`, timers, wall clocks, `ILogger`, `Process.`,
  `unsafe`): 0 in the 14 library files (a planted copy fires); `File.`/`Directory.` only in `JobSpool.cs` and
  `SpoolFolders.cs`.
- One commit; author and committer address and name equal (address not printed); subject the kit's (171 bytes); body the
  one attribution line.

## 2. The contract and THE REQUIRED SECTION, with the gate's own inputs

Read whole: the 14 library files. Shape as built equals THE CONTRACT (types, members, the 18 reasons numbered from 1,
the fixed messages, the masks). The gate's probe file (evidence/GateProbeTests.cs.txt, 17 tests, run inside the lane's
test project, then moved out; `status --porcelain` 0 lines after) gave 213 recorded outcomes: 35 values, 166
`JobServiceException` (every one with its fixed message and no inner exception: 166 of 166), 9 other exceptions, 3 hangs.
The 12 that are not a value or a typed exception are F1 (2 rows), F2 (3 rows), F4 (5 rows), the caller's own token
cancelled (`TaskCanceledException`, allowed by D17) and one test-seam row (the delete hook made to throw a non-I/O
exception: the seam only, not reachable in product use).

| H | The gate's inputs | Result |
|---|---|---|
| H1 | 8 bodies ending early (mid-part, in headers, after the boundary line, boundary without line end, preamble only, empty, second part cut, closing boundary cut), each after an earlier good upload | `ScanRefused` x8, the whole job folder gone (earlier upload included), raw scan 0; the closing boundary alone = a value with 0 files |
| H2 | a body that ignores its token and never ends; a body whose `ReadAsync` blocks its thread | `ReceiveTimedOut` at 10 min on the test clock, job gone; blocking body: HANG (F2) |
| H3 | 12 refused content types (text/plain with boundary, empty, no boundary, `boundary=""`, 71 plain and quoted, two boundaries, two of differing case, control bytes, `/`, `multipart/`) and 4 accepted (quoted, upper case, multipart/mixed, 70 with inner spaces) | refused: `ScanRefused`, body read count 0 each; accepted: round trip byte-equal. A 1 MB extra parameter is accepted (the caller's header) |
| H4 | 17 headers, 16 headers, one header of 8200 bytes, 9000 bytes over 9 headers, a line with no colon, 100000 one-byte header lines | `ScanRefused` x5 with the job gone; 16 taken |
| H5 | own caps (chunk 64, file 1000, job 1500, 3 files): file 1000 / 1001; job 1500 / 1501 over two parts and over two uploads; 3 / 4 empty parts; 2 + 2 over two uploads; spool 1500 over two jobs exact / +1; file 64 / 65 at a chunk edge; a 16 MiB part over a 1000 cap | exact values taken; `FileTooLarge`, `JobTooLarge`, `TooManyFiles`, `SpoolFull` at one more; reserved bytes 0 after each failed job; the 16 MiB part read 4096 of 16777321 bytes |
| H6 | `Content-Length` 0, 1, 99999999999, -5, `abc` on 900 bytes; 10 on 1001 bytes | ignored: 900 counted and byte-equal; 1001 = `FileTooLarge` |
| H7 | (B1860's C06) | the exact spool boundary over two jobs held (H5 row); F3 |
| H8 | file names `../../x`, an absolute `/tmp/...` name, `..\..\x`, NUL, 300 characters, `con`, `.`, empty, each with `filename*=UTF-8''..%2F..%2Fy` and `Content-Type: application/pdf; name="../../z"` | one new path each, `spool/<job>/000001.part`; content type null; nothing created beside the test folder or at the absolute name |
| H9 | upper-cased, trailing space, trailing line feed, padded, standard-base64 form, 1 MB string, lone surrogate, another receiver's job and secret, its secret on this job, a job id of another spool, `default`, the right secret at exactly the window, after `Sweep` of an expired job, after `WipeJob`, after `WipeSession` | `JobNotFound` every time, one reason, body read count 0 each |
| H11 | (B1860's D2; the gate's own) a full chunk made last, the final chunk doubled and removed, chunk 1 dropped, chunk 0 in place of 1, format byte 2, header only, empty file, final tag cut by 1, last tag bit, 40 random single-bit flips | `SpoolCorrupt` every time; bytes handed out always a prefix of the document in whole verified chunks, never past the flipped chunk |
| H12 | (R01) a root holding a link to an outside folder and a link to an outside file | both links removed, the outside file kept; a root that is a dangling link, a link to a folder, or relative: `InvalidArgument` |
| H13 | `WipeSession` during a receive; read and write after `WipeJob`; writer `Dispose` after `WipeJob`; spool disposed under a receive, a reader and a writer | `JobNotFound`, folder gone; disposed spool: `ObjectDisposedException` (F4) |
| H14 | a REAL failing delete (no hook): the job folder made 0500 on this Mac | `WipeResult(jobs 1, failed deletes 1, pending deletes 1)`, the job gone from memory at once; mode restored, `Sweep` removes the folder |
| H16 | empty, 3 bytes, 8 header bytes, an HTML page, 1000 random bytes, a null stream | `ResponseRefused` x6 |
| H17 | another request id, request id 0, no job group, two job groups, `job-id` doubled, with two values, 0, -1, as enum, as text, integer tag with 8 bytes, `job-state` 2, 10, as integer, missing, `job-id` only in the operation group | `ResponseRefused` x16; `job-id` 2147483647 taken; a version 0.0 answer is taken (the version is not checked: D11 names no version rule) |
| H18 | a 70000-byte answer header | `ResponseRefused` |
| H19 | an answer that never ends; a transport that never returns and ignores its token; a transport and an answer stream that block their thread | `ResponseTimedOut` at 60 s and at 30 min, the transport's token cancelled; blocking: HANG (F2) |
| H20 | transport throws `IOException`, its own `TaskCanceledException`, synchronously; answer stream throws `IOException`, `ObjectDisposedException`, its own `TaskCanceledException`; reports more bytes than asked; document throws its own OCE | `TransportFailed` / `ResponseRefused`, except the answer stream's own OCE: raw (F1) |
| H21 | busy, not-possible, bad-request with a good job group, 0xFFFF, busy with another request id | `PrinterBusy` 1287, `PrinterRefused` 1028 / 1024 / 65535, `ResponseRefused` |
| H22 | `job-password`, `printer-uri` in the job group, a made-up name, `Copies`, `copies` with no value, with a 40000-byte value, a 40000-character job name, a relative URI, a null list, a null attribute, a collection 40 deep | `InvalidArgument` x11, transport calls 0 each |
| H23 | a busy poll answer; every poll answer stream throwing its own OCE; states 5, 3, 5, 9 | `PrinterBusy` at once; raw OCE (F1); progress 5, 3, 5, 9 (each change reported) |

**The raw spool scan (every encoding).** After a two-part receive (20000 random bytes and a text document) and a written
print job: every file under the root (3 files) searched for the document's first, middle and last 64 bytes, the text
document, the secret (text and its 32 raw bytes), the session id, the declared file name and BOTH jobs' keys, each in 29
forms (raw; lower and upper hex, base64 and base64url with and without padding, Latin-1, each in UTF-8, UTF-16 LE,
UTF-16 BE and UTF-32): **0 hits**. Controls: the kit's clear marker found; a UTF-16 marker planted beside the spool found by
these forms.

## 3. The second reader's points

D2, D6 and C06 are reader B1860's. From this reader's side: D2's tamper rows (H11 above) and D6's secret rows (H9 above)
behave as the kit says; the exact spool cap holds over two jobs (F3 is a missing cell, not a product fault).

## 4. Mutants (the gate's own texts, made by program on PRODUCT code; each = build and test of the lane's test project, 108 tests, through the lock; undone by restoring the original bytes and proved by `git diff --quiet` rc 0)

| Mutant | Text | RED (by assertion) |
|---|---|---|
| mFinal | final flag byte always 0 | S03 x2 |
| mNonce | chunk number in the nonce replaced by 0 | S04 (own nonce) |
| mJobAad | job-id bytes of the associated data cleared | S05 (same key) |
| mRelease | a failed tag hands the chunk out instead of `SpoolCorrupt` | S02, S03 x2, S04, S05 x2, L01 (10 failed) |
| mSecret | comparer `SequenceEqual` instead of `FixedTimeEquals` | A03 |
| mOracle | a wrong secret on a known scan refused as `ScanRefused` | A02, T03 |
| mBusy | the receive guard never true | A05, L01 |
| mTimeout | the receive's `WaitAsync` without its bound | T01 x2 (guards), L01 |
| mPartial | a failed upload no longer wipes its job | C01 and 16 more (17 failed) |
| mZero | the key not cleared when forgotten | K01, P02, W02, W03 |
| mWipeOrder | the key cleared only after the folder delete | W02, W03, P02 |
| mStart | the start removal skipped | R01, P02 |
| mAttr | the creatable-list check removed | J02 (3 rows) |
| mReqId | the request-id comparison never true | J06, Y03 |
| mState | the job-state range widened to all integers | J06, Y03 |
| mReadBound | the answer's `WaitAsync` without its bound | J08 (guard) |
| mSpoolCap (own form) | spool cap checked without the incoming count | **NONE: survived** (F3). With the gate's probe file present: G05 red |

16 of the kit's list re-made independently (more than the six required), each red and undone; one survivor named as F3.
After the last undo and the fix sketch's undo: `git diff --quiet` rc 0, whole suite rebuilt and run again (below).

## 5. Build, suite, hosted

- Through the lock at the head: `dotnet restore Datasec.Suite.slnx --locked-mode -p:NuGetAudit=false` with `CI=true`:
  rc 0, 0 lines naming `http` (closed proxy, nothing fetched); `status --porcelain` 0 lines (no lock file changed).
  `dotnet build Datasec.Suite.slnx -c Release --no-restore`: rc 0, `0 Warning(s)`, `0 Error(s)`. `dotnet test -c Release
  --no-build` (whole suite): `Passed!`, `total: 1081`, `failed: 0`, `succeeded: 1077`, `skipped: 4` (= 973 + 108). After
  all mutants: rebuilt 0/0, `total: 1081`, `failed: 0`, `skipped: 4`.
- Not heavy: `build/repo_rules.py <clone>` without `--source-documents`: `R5 hash half NOT RUN`, `RULES: clean (360
  files)`; `unittest discover -s build/tests`: `Ran 60 tests`, `OK`.
- Hosted run 44886542242 of `5dd0f859` by GET with the R5-aware reader (`fleet/state/s304/d1835/gate/hosted.py`, copied,
  sha256 `e73339f3...`; `--total 1081 --rules 360 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60`): four jobs
  success, attempt 1, 0 other runs; linux `total: 1081` x2, `succeeded: 1077`, `skipped: 4`, `GUARD: clean (10 files)`;
  windows `total: 1081` x2, `succeeded: 1062`, `skipped: 19`, `GUARD: clean (11 files)`; both `0 Warning(s)` `0 Error(s)`;
  secret-scan both PLANTED-CONTROL lines, `objects of this commit not among them 0`, `no leaks found` x3; rules `Ran 60
  tests in`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (360 files)`. **`HOSTED 5dd0f859...: PASS`** (rc 0).
  Control `--total 1082`: `FAIL 4`. Windows log: 20 lines with the word skipped, 0 naming a Jobs test (control: 9 name
  `KeyRing`). The guard counts 10 and 11 are main's: the host does not reach the library.
- CodeQL: no Analyze run on a branch push; C# extraction cannot run on this arm64 machine. NOT RUN; the pull request's
  analysis would be the only C# proof.

## 6. Texts

`words.py --control`: `CONTROL FIRED: 13 of 13`. Over the 4959 added lines without the two lock files and over the
commit message: `WORDS: clean (2 files)`. The README holds every limit the kit names (blocks not overwritten, key in
memory and swap or a crash dump, the cipher objects' own key copies, no timer, one process per root, Windows access
lists, the real transport out, HP's uploads and model acceptance UNMEASURED, the host does not use the library, no
converter). Untrue sentences: "Every refusal is a `JobServiceException`" (README) and the comment at
`PrintJobSender.cs:330` (F1, F4).

## 7. The seat's deviations (STATUS, DEVIATIONS 1 to 7)

1. L01 drives all 18 reasons inside its own test instead of collecting across cells: **accepted** (xUnit's order is not
   fixed; every cell also passes its exceptions through the leak helper, read in the test files).
2. L04 reads the test's own `deps.json` instead of the project file: **accepted** (the kit bars reads outside the test's
   folders; the project file was read by this gate: no `PackageReference` with a version).
3. Extra S04 and S05 tests (key-stream and same-key): **accepted**, and needed: the gate's mNonce and mJobAad are red ONLY
   on those two tests.
4. mNonce's undo proved through the next `diff -U0`: **accepted as records** (the head is what was pushed; the gate's
   clone is byte-equal to it).
5. A 1 GiB ceiling on `ChunkBytes`: **accepted** (fails closed with `InvalidArgument`; no behaviour beyond D4 otherwise).
6. The writer's file stream unbuffered (`BufferSize = 0`): **accepted** (whole chunks are written; makes C06's disk bound
   exact; no effect on the format).
7. The kit's `hosted.py` hard-codes `Ran 53`; R5 moved the floor to 60; read with the R5-aware reader per ANSWER-1:
   **accepted** and re-measured by this gate (PASS with `--unit 60 --floor 60`; control FAIL 4). Prediction P7 failed as
   written and is left unedited: correct.

## 8. Landing texts

NOT WRITTEN: item 7 is for GO or GO WITH FINDINGS only.

## 9. What was NOT tested

- Linux and Windows locally (macOS arm64 only); the hosted legs ran the lane's cells, not the gate's probes. F2 and F4 on
  Windows are DERIVED from source.
- D2 in depth, D6's timing and C06's races (reader B1860's): the gate ran no race harness.
- The two publishes and the release guard locally (the hosted GUARD lines were read instead); CodeQL (cannot extract C#
  here); the R5 hash half (`--source-documents`, never passed).
- A real transport, a device, what HP's devices send (UNMEASURED by design).
- `CloseScan` racing an upload that already passed its secret check (read from source only, F5).
