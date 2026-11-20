GATE B1799: NO GO @ 9f4238a on main 7bf3752

Gate G1 Tier 1, round 1 of 2, OXPd 2, WP4.2 (part) (kit B1788, seat X6). Head `9f4238adbd465bf7924878982a7444341d9c7152` on main
`7bf375268b9975ac9ece66579f7471ba7dbab11d`. Read and measured 2026-11-20, 19:39 to 20:07 AEDT (clocks by `date`), in the gate's
own clone `/private/tmp/b1799-gate/clone` (push URL `invalid://no-push`). Every number below was printed by a program; the
programs and their logs are under `/private/tmp/b1799-gate/` (`scratch/`, `logs/`, `probes/`).

**BLUF.** One Major, so NO GO and a fix round, by the round rule. The reader is clean: 731,132 inputs, no exception type but
the format exception, no hang, no read above 32767 bytes, a stop at the 1 MiB bound, exact consumption to the end tag and
write(read(x)) = x on all 352,240 accepted inputs that went through that check. The stream is clean under every answer a service can give when the caller
reads one read at a time: 0 wrong, repeated or lost bytes in 30,000 random runs, 924 cut runs and a made-up document of 4 GiB.
**The Major is on the caller's side of the stream: closing it while a read is in flight does not stop it; it waits, fetches
once more, hands bytes to the abandoned read and leaves the new answer open.** The Workpath source stops there; the builder's
deviation 4 says the difference needs nothing. Everything else the builder claims was reproduced: scope, the frozen blocks,
217 tests, the seven mutants, the hosted lines, the no-copy check. **Nothing talks to anything and the server does not
reference the library: no finding here can do harm today. They are about what the transport lane would build on.**

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Major** | **Yes (round rule)** | **Closing the stream while a read is in flight does not stop that read.** Measured with the gate's fake answers (`logs/fuzz-stream.log`, rows S8), `DisposeAsync` and `Dispose` alike: when the body ends the pending read with an I/O error or with 0 bytes (what a closed network body does), the stream then asks for the wait (1 wait after the close), makes 1 new fetch after the close, the abandoned read RETURNS 4 document bytes, and the new body is never closed (1 of 2 bodies left open). Only when the body throws `ObjectDisposedException` does the read end at once. Cause: the read loop looks at the token at every turn and never at the closed flag (`ResumableDocumentStream.cs` lines 89 to 126); `OpenAsync` does not look either. The source the lane ports looks at its closed flag at every turn of the loop and before every open (its lines 75, 132, 220 to 224), and its close sets that flag (line 126). The builder's deviation 4 names the difference and gives it no effect ("C# has the token of each read"): a caller that closes without cancelling gets a request to the print service after the close and a leaked answer. No test covers a close under a read. | In the fix round, one commit: refuse to go on once closed (the closed flag checked at the top of every turn of the loop, after a failed read BEFORE the wait is asked for, and after the fetch returns, disposing an answer that arrives after the close), ending the pending read in `ObjectDisposedException`. A test: a body that ends a pending read with an I/O error when it is disposed; after the close 0 fetches, 0 waits, every body disposed. |
| 2 | Minor | No, but fix in the same round (a few lines) | **A second read started while one is in flight is not refused.** Measured (row S9): with an answer that goes on beyond the range asked, the first read and the second each got 10 bytes: 20 bytes yielded for a document of 10, `Offset` 20, no error. Each read took its cap from the same offset before either finished. It needs two faults at once: a caller that breaks the platform's rule for a stream (one read at a time) AND an answer longer than asked. With one read at a time the cap holds (rows S4, S12: never more than the total in 30,000 runs). The gate does not read this as the Blocker of item 3: no answer of a service alone produces it. | A flag taken at the start of `ReadAsync` and released at its end; a second read while it is held throws `InvalidOperationException`. One test. |
| 3 | Minor (decided by nobody) | No | **The reader refuses a whole packet on any group delimiter but 0x01, 0x02, 0x04, 0x05** (kit row C13, the coordinator's choice). Measured: 0x00 and 0x06 to 0x0f refused as the first group and as a second group (`logs/fuzz-reader.log`, line DELIMITERS). The public register lists 0x06 to 0x0a (subscription, event notification, resource, document, system: `cups/ipp.h` lines 456 to 460 at the commit the kit names). The public reference reader takes every delimiter but 0x00 (`cups/ipp.c` lines 5479 to 5506 of the builder's copy, read by the gate). Effect in the stream: the packet at the start of every answer goes through this reader, a refusal there is not retried, so ONE such delimiter in the answers to a fetch would end every document (measured, row S5: format exception, 0 bytes, 0 waits, body disposed). Whether the print service sends one is UNMEASURED. | Before the first lane that reads a real answer: take 0x06 to 0x0f as groups kept with their tag (one line in `IppTag.IsKnownGroup`, used by reader and writer; the test rows of the refusal change). Cost of the tolerant reading, measured by reasoning on the code, not run: none in memory or time (the same bounds apply), the round trip holds because the tag is kept; the only loss is that a packet with a delimiter nobody registered is no longer refused. 0x00 stays refused. An open ruling: FOR-RECORDS.md. |
| 4 | Minor | No | **A hostile packet inside the bound costs about eighty times its size.** Measured (`logs/fuzz-worst.log`): 1 MiB of group delimiters is TAKEN after 80.0 MiB of allocations and about 100 ms; the endless variant is refused at the bound after the same 80.0 MiB. Other shapes: 36.0 MiB (attributes of six bytes), 21.6 MiB (members), 18.9 MiB (collections 32 deep), 12.0 MiB (further values). It is bounded: no single read above 32767 bytes was ever asked of the source, and the reader stops at 1,048,576 bytes. Under a caller's own bound of 64 MiB the same shape took 5,120 MiB of allocations and 5.6 s. The stream reads the packet of EVERY answer under the default bound. | Not for this round. For the transport lane: read the packet of a fetched part under a small bound (a few KiB: the dropped packet is tiny), and cap the count of groups. A backlog line. |
| 5 | Minor | No, but add in the same round | **Three stated behaviours have no test that can fail** (gate mutants that leave all 217 tests green; `logs/mutants.out`): g4, a length read unsigned (a negative length is no longer refused; the builder's five rows end in the same exception type because the stream ends first); g17, a signed number taken in `Content-Range` (the builder's deviation 1, "digits only", is pinned by no row); and the names of the lists: the tests fix each count and 2 or 3 names, so one name exchanged for another stays green (not run as a mutant; read in `UniversalPrintAttributeListsTests.cs`). The lists ARE right at this head: each equals the source as a set, compared by the gate's program against the compiled library. | A row with length 0x8000 followed by 32768 bytes (the format exception, and the source not read past the two length bytes); a row `bytes +0-9/10` in the unreadable table; a test per list against the whole expected list. |
| 6 | Minor (records) | No | **What the stream does with failures that are not I/O errors or that make progress, measured and not named in its comment.** (a) An exception from the body of another type is not retried and leaves as it is (row S6: `InvalidOperationException`, 1 fetch). The transport lane must map its client's failures to `IOException` or they end the document. (b) An answer that gives ONE byte and then fails makes progress every time, so the limit of three never applies: 50 fetches and 49 waits for 50 bytes (row S6). As coded in the source too. (c) After the limit is reached, each further read by the caller costs one more fetch (row S12: 5 fetches in a row at one offset). (d) The end and the total of `Content-Range` are not used: `bytes 0-0/10`, `bytes 0-9/5`, `bytes 0-9/-10`, `bytes 0-9/0` are each taken when the start is right (rows S2); as coded. | Records and the transport lane's kit. A ceiling on fetches per document is a product choice: FOR-RECORDS.md. |
| 7 | Minor (records) | No | **Acknowledge-Job differs from the system print library's encoding in the letter case of one value.** The library writes `UTF-8` (as the Workpath source spells it); the operating system's print library, building the same request, writes `utf-8` (3 bytes differ, positions 32 to 34; equal when case is ignored). The two Get-Jobs requests are equal byte for byte. What the Workpath app's own IPP library puts on the wire for that value is UNMEASURED. | A question for the Workpath team, with 3a to 3h. |
| 8 | Minor (records) | No | **The root README is stale**: Layout does not name the two projects and Reserved names still holds `src/Datasec.Suite.UniversalPrint` (its line 47). No sentence becomes untrue in a way that matters. | The one README pass after the wave. |
| 9 | Minor (records) | No | STATUS, HOSTED RUN: the hosted NEUTRAL-SCAN counts 133 stored objects and the builder's local run 134, "not looked into". The gate confirms the hosted line (133: 84 blob, 7 commit, 42 tree; objects of this commit not among them 0) and did not look into the local 134 either. | None needed for the merge. |

Not findings: the nesting bound of 32 (the public reference reader stops at 10: `cups/ipp.c` line 5410); the strict lengths
(each is a refusal of the public reference reader too: its lines 5690, 5692, 5714, 5776, 5791, 5811, 5831 to 5878, 5893, 5908,
5923); the exception of the source stream passing through the reader unchanged.

## Item 2, the required question: what is the reader handed that is NOT a well-formed packet, and what does it do with each?

`logs/fuzz-reader.log`, `logs/fuzz-worst.log`; harness `probes/Fuzz/Program.cs` (the gate's own generator and its own encoder;
it calls only the built library).

| Handed | Inputs | Taken | Format exception | Any other exception | write(read(x)) differs | Consumed past or short of the end tag |
|---|---|---|---|---|---|---|
| the five fixtures, each followed by 16 foreign bytes | 5 | 5 | 0 | 0 | 0 | 0 |
| every truncation of the five fixtures | 1,769 | 0 | 1,769 | 0 | - | - |
| every single-byte mutation of the five fixtures | 451,095 | 291,299 | 159,796 | 0 | 0 | 0 |
| every byte pair of the fixtures set to 0x0000, 0x0001, 0x7ffe, 0x7fff, 0x8000, 0xffff | 10,584 | 5,739 | 4,845 | 0 | 0 | 0 |
| random bytes, length 0 to 64 | 60,000 | 197 | 59,803 | 0 | 0 | 0 |
| a sound start, then bytes biased to tags and small lengths | 60,000 | 10,914 | 49,086 | 0 | 0 | 0 |
| the gate's own well-formed packets, each followed by foreign bytes | 20,000 | 20,000 | 0 | 0 | 0 | 0 |
| those with one byte changed, removed, added, or a slice repeated | 120,000 | 24,043 | 95,957 | 0 | 0 | 0 |
| collections nested 0 to 32 deep, balanced | 33 | 33 | 0 | 0 | 0 | 0 |
| nested 33 to 40, 100, 1,000, 10,000, 100,000, 200,000 deep | 13 | 0 | 13 | 0 | - | - |
| unbalanced collections at depth 1 to 40 and 100,000 | 164 | 0 | 164 | 0 | - | - |
| delimiter bytes 0x00 to 0x0f as first and as second group | 32 | 10 | 22 | 0 | 0 | 0 |
| the nine-byte packet under a caller's bound of 1 to 12 bytes | 12 | 4 | 8 | 0 | - | - |
| fixtures and own packets through a stream that completes asynchronously | 3,005 | 3,005 | 0 | 0 | - | 0 |
| streams that misbehave at each of 884 positions (five kinds) | 4,420 | - | 884 (zero bytes per read) | the source's own, unchanged | - | - |
| **all** | **731,132** | **355,249** | **371,463 + 884** | **0 from bytes** | **0** | **0** |

- **Exception types.** From bytes alone: `IppFormatException` and nothing else. A source stream that throws (I/O error,
  `InvalidOperationException`, `ObjectDisposedException`, planted at each of 884 positions) leaves the reader as that same
  exception, unchanged. A cancelled token leaves as `OperationCanceledException` (884 positions, and before the call with 0
  reads of the source). A source that gives zero bytes from a position on is the format exception after one more read (884
  positions): no loop. Arguments that are a programming error (a null source, a bound of 0 or below) are argument exceptions.
- **One byte per read.** Every input of the fixture, truncation, length-pair, own-packet and nesting rows, and one in five to
  seven of the rest, was read again one byte per read: the same outcome and the same packet in every case (0 differences).
- **Allocation.** The largest single read the reader ever asked of the source: 32,767 bytes. It never asks for a value before
  the bound allows it. Peak cost: finding 4.
- **Stack.** Depth 0 to 32 taken (33 of 33); 33 and every deeper one refused with "collections nest deeper than 32", up to
  200,000 deep with no stack fault (the refusal comes before the descent). Can a legitimate device answer nest deeper? Not by
  anything on this machine: the public reference reader refuses beyond depth 10, so a packet that reader takes is taken here.
  The deepest collections the standard's own attributes use are a few levels. UNMEASURED on a device.
- **A header that never ends.** Refused at the bound: 1,048,575 or 1,048,576 bytes taken, 25 to 39 ms, also at one byte per
  read. Endless values of 32,767 bytes: refused after 1,015,956 bytes, 1.0 MiB allocated.
- **Exact consumption (row C12).** For 352,240 accepted inputs (the other 3,009 of the 355,249 are the same packets read again
  through an asynchronous stream or under a caller's bound, compared with the first reading) the bytes written back equal the
  bytes consumed, the last
  consumed byte is the end tag, and the foreign bytes after it were not touched. Reading the written bytes again gives an
  equal packet. write(read(x)) differs: 0. Controls: a written packet with one bit flipped compares unequal; a foreign
  exception is seen as foreign.
- **A second witness.** The operating system's print library (`libcups`, loaded in-process through its public functions,
  writing to and reading from local files: no network call, no daemon call) reads each of the five fixtures whole (state
  "data", 243, 307, 326, 884 and 9 bytes taken; 4, 6, 5, 25 and 0 named attributes) and refuses a fixture cut at 100 bytes.

## Item 3, the stream attacked

`logs/fuzz-stream.log` (140 rows), `logs/fuzz-big.log`; harness `probes/Fuzz/StreamAttack.cs`. Every wait was the injected
one: the whole attack ran in 3.9 s of wall clock while asking for thousands of seconds of waits (one row alone: 7,990 s).

- **Content-Range (47 values at offset 0, 6 on a resume).** Refused, with 0 bytes yielded, 1 fetch, 0 waits and the body
  disposed: no header, empty, blank; a negative start; a start that is not the offset (1 for 0; on a resume at 4: 0, 3 and
  5); a start of 2^32, 2^63 - 1, 2^63, 2^64 (the overflow is a refusal, not a wrap); an end that overflows; `+0`, `0x0`, `0.0`;
  digits of another script and full-width digits; `bytes=`, `octets`, no slash, two slashes, `*` for the range, two ranges.
  Taken when the start is right: any letter case of the unit; spaces and tabs around each part, a no-break space too; no space
  after the unit; a total of `*`, of 0, 1, 5, 999, 3,000,000,000, 99999999999999999999, `-10`, `x` or nothing; an end of 0 or
  4. In each taken case the bytes yielded were the document's and exactly the stream's own total.
- **A total of 0:** no fetch. **A total of 1:** one fetch of 0 to 0. **Totals of 2^31, 2^31 + 1, 2^32, 5 GiB + 3 and
  2^63 - 1:** the ranges asked are 64-bit and right (for the last: `bytes=100-9223372036854775806` on the resume). A negative
  total is refused at construction. **Streamed, which no test of the repository does:** a made-up document of 4,311,744,515
  bytes (4.016 GiB) through the stream, each body cut at 2^31 - 5, 2^31 + 1, 2^32 - 1 and 2^32 + 7, ending or failing in turn:
  4,311,744,515 bytes yielded, 0 wrong, 5 fetches at exactly those offsets, 4 waits. Not streamed by anyone: a real document
  of that size, and anything through a real client.
- **A body shorter than asked:** cut at every position of the packet and of the document (924 runs, ending or failing with an
  I/O error, three buffer sizes): 0 runs with a wrong byte, more than the total, a short document without an error, a resume
  at a wrong offset or an earlier body left open. Cut inside the document: a wait, then a fetch at the offset reached. Cut
  inside the IPP packet: the format exception (an ending body) or the I/O error (a failing one), 1 fetch, not retried.
- **A body LONGER than asked:** exactly the total yielded, the next read gives the end, and the stream took no byte of the
  surplus from the body. **Bytes of the dropped packet:** never yielded (0 in every run). **A response whose start is wrong:**
  refused before its body is read.
- **The same failure for ever:** 1 fetch plus the retries allowed, never one more (0, 1, 3, 7: 1, 2, 4, 8 fetches), every
  retry at the offset reached, the waits 1007, 2007, 4007 and then 8007 ms with a jitter of 7, the last cause carried, the
  offset named, every body disposed, 0.0 ms of wall clock. A jitter function that gives `int.MaxValue` or `int.MinValue`:
  brought to 299 and 0.
- **Cancellation at every await** (before the read; in the fetch; at three positions of the packet; in the document; in the
  wait; in a wait that ignores the token): the platform's cancellation exception each time, no fetch after it, the body of a
  cancelled open disposed; reading on with a fresh token gives the rest of the document with no byte wrong, repeated or lost.
- **Dispose during a read:** finding 1. **A second read while one is pending:** finding 2.
- **Statuses:** only 206 is taken; 200, 201, 204, 207, 226, 299, 301, 304, 400, 401, 404, 429, 500, 503, 0, -1 and
  `int.MaxValue` are the fetch exception and 416 the typed one; each with 1 fetch, 0 waits, the body disposed.
- **Soak:** 30,000 random documents under random answers, reading on after an error up to three times: 28,553 read whole and
  right, 1,447 ended in errors, **0 with a wrong, repeated or lost byte or more than the total**; of 89,291 fetches, 0 asked at
  an offset other than the bytes yielded or with a last byte other than total - 1; 0 bodies left open after the close.
  Control: a body holding the bytes of offset 1 under a header that says 0 is seen as wrong by the checker.

**The builder's deviations, each by its effect**

| # | Deviation | Effect, measured | Keep? |
|---|---|---|---|
| 1 | the unit word in any letter case; digits only | `BYTES` and `Bytes` taken; `+0`, other scripts' digits refused. More lenient than the source on the unit (the standard's range units are case-insensitive), stricter on the number. Safe both ways. "Digits only" has no test that can fail (finding 5). | keep |
| 2 | the cap read as 8000 ms | waits 1007, 2007, 4007, 8007, 8007 ... as the source computes them (its lines 233 to 236); 10,000 is never reached. | keep |
| 3 | a read into an empty buffer gives 0 and fetches nothing | measured (0, 0 fetches); the platform's meaning of such a read. A test kills its mutant. | keep |
| 4 | closing does not set a flag | **finding 1** | fix |
| 5 | the jitter brought into 0 to 299 | measured; a test kills its mutant. | keep |
| 6 | nesting bound 32 | measured: 32 taken, 33 refused cleanly; the reference reader's bound is 10. | keep |
| 7 | strict lengths | each refusal is one the public reference reader makes too. A name that is not UTF-8 is refused as well; names are keywords of plain letters in the standard. | keep |
| 8 | a packet that fails to parse at the open is the format exception, not retried | measured (S3, S5). A caller that catches only I/O errors does not catch it: the transport lane must catch both. Not retried is the source's shape for every failure of the open. | keep; say it in the transport kit |
| 9 | two exemptions in the builder's own host pattern; the publish lines | no effect on the product. | - |

FOR TUESDAY 3a to 3h (the "as coded" list): each re-read at source by the gate in the stream's file (lines 90, 94, 145 to 148,
175, 233 to 236, 245 to 247) and in the request file (the Acknowledge-Job builder; `printer-name` in both lists: confirmed by
program). All eight stand as the builder wrote them. Item 4 (the delimiters): finding 3.

## Measured rows

| Item | Reading | How |
|---|---|---|
| Refs | `main` 7bf37526; the branch 9f4238ad; compare ahead 1, behind 0, 27 files (1 modified, 26 added); 4 check runs success; pull requests of any state 1 (number 1, merged), open 0; the origin holds 4 branches | `gh api -X GET`, 19:39:56 and 19:59:16 |
| Merge | the head's one parent IS main (merge-base = main, behind 0), so the merge is the head's tree | `rev-list --parents`, `merge-base`. `merge-tree` NOT RUN: a hook of this workspace refuses that verb outside the coordinator's folder |
| 1 Scope | 27 rows: A 26, M 1, other 0; outside the property 0 (control: 5 of 5 planted rows flagged); binary rows 0; +3910 -0; 26 files on main, 52 at the head; the one changed file of main is the solution file; modes all 100644; no path under `build/`, `.github/`, `packaging/`, no `README.md`, `Directory.Packages.props`, `global.json`; no key, certificate, capture or archive name | `scratch/scope.py` |
| 1 Frozen | F1 5/146, F2 12/362, F3 1/92, F4 1/106, each sha256 equal to the kit's FACT 5; F1 and F2 equal the two project files byte for byte; the solution file's added lines are exactly F3 and F4, 0 removed, 11 lines, 529 bytes, sha256 d0da6e47... equal to the kit (control: one more space is seen) | the same |
| 1 Packages | the library's lock names 0 packages; the test lock's 21 package rows are the base test lock's rows, 0 more, 0 fewer; `Directory.Packages.props` equal to main | the same |
| 1 No copy (5h) | lists: creatable 14 = 14 (same order), blocked 30 = 30, watch 14, 19, 4, 8, 3 each equal as sets, union 48 = 48, six success codes; compared against the COMPILED library, not its source text. Comment lines of the two source files 67 and 21, distinct texts of 20 characters or more 52: found in the 22 port files 0 (also with case and spacing ignored: 0). Source lines of 40 characters or more 351: port lines equal to one 0. Port lines sharing a run of six identifiers with a source line: 0. Names of the Java packages and classes of the source in the port: 0. Each with a control that fires | `scratch/port.py` |
| 4 Builders | Get-Jobs without and with a user: the library, the gate's encoder and the system print library write the same 243 and 307 bytes; equal to the builder's fixtures. Acknowledge-Job (port 631, job 42; and port 443, the largest job number): the library equals the gate's encoder (326 bytes) and the builder's fixture; the system print library differs in 3 bytes, the case of `UTF-8` (finding 7) | `scratch/witness.py`; the witness: `ippNew`, `ippAdd...`, `ippWriteFile`, `ippReadFile` on local files. `/usr/bin/ipptool` was not used (it needs an address to send to) |
| 5 Suite | locked restore rc 0 with no lock file changed; build 0 warnings, 0 errors; test `total: 217`, `failed: 0`, `succeeded: 217`, `skipped: 0`; porcelain 0 lines after | the project's SDK 10.0.404 with the gate's own home and package cache, each job under the wave's lock (85 lock folders moved into the gate's scratch; the lock is released) |
| 5 Mutants | the builder's seven: 7 of 7 killed (43, 8, 6, 9, 1, 2 and 2 red tests; the STATUS says 43, 8, 6, 9, 1, 2, 1: m7 reddens two tests here, the count test and the filter test). The gate's own 29: 26 killed, 2 survive (finding 5), 1 is equivalent (closing through `DisposeAsync` alone still closes the body through the base class; with both ways removed the test is red). After the undo the tree equals the clone (0 files differ) | `scratch/mutants.py`, `logs/mutants.out` |
| 5 Tests | 106 methods (28, 12, 22, 33, 11); no sleep, no delay, no clock, no stopwatch, no random, no skip, no operating-system condition in tests or library (each count 0); fixtures are hexadecimal constants compared with the writer's output, and the gate rebuilt three of them by two other encoders | counts by `grep -c -E`, with the positive rows `Fact` 84, `Theory` 23 from the same files |
| 5 Library | in `src/`: `.Result` 0, `.Wait(` 0, `GetResult(` 0, `HttpClient` 0, `Socket` 0, `File.` 0, `Environment.` 0, `NoWarn` 0, `pragma` 0, `SuppressMessage` 0 | the same |
| 6 Hosted run | run 44702478818: head = the reviewed head, event push, attempt 1, success. linux and windows: `0 Warning(s)` 1, `0 Error(s)` 1, `total: 217` 2, `succeeded: 217` 1, `failed: 0` 1, `GUARD: clean (10 files)` and `(11 files)` 1 each. rules: `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (52 files)` 1, the hash-half note 1, `OK` 2. secret-scan: both planted-control lines 1 each, the NEUTRAL-SCAN line (133: 84 blob, 7 commit, 42 tree; 266 copies; 0 not among them) 1, `no leaks found` 3. Every count equals the STATUS. Control line: 0 in each log | `scratch/hosted.py`: GET with `--allow-escape-sequences`, return code asserted, the runner's echo of each step left out |
| Repository controls | `RULES: clean (52 files)` with the hash half run (1657 files hashed); `Ran 53 tests`, `OK`; the scanner over `src`, `tests` and the history: `no leaks found` | in the clone |
| 8 Text | 3,910 added lines and the commit message: names of the ban list 0, B-numbers 0, clarification ids 0, ticket keys 0, "product owner" 0, "coordinator" 0, words of deciding 0, card ids 0, kit row ids 0 (control line: each fires); bytes outside printable ASCII 0; hosts after a scheme: three, all `.invalid`; IPv4 0; one identifier, the fake `00000000-0000-4000-8000-000000000001`; one mail-like value, `user@example.invalid`, beside the attribution line. The commit subject is the kit's, 94 bytes. "Workpath" in 5 comment lines (Datasec's own app). Seven hits of a seat-id pattern are the format text `x2` | `scratch/text.py` |
| 9 The texts through the function | `neutral_export` cut from the head's `ci.yml` (lines 120 to 128), scanner 8.30.1, the workflow's four options. Title alone; title and body; body alone; the squash message with a number; as written; the squash body alone; the repository's default squash shape; landing.txt: each rc 0, "no leaks found", stored whole. Control (the squash message with the workflow's planted value joined in): rc 1, "leaks found: 2". Texts flagged: 0. In the four texts: names 0, ids 0, non-ASCII bytes outside the footer 0. One hit of a round-number pattern in the body is the word "around" | `scratch/texts.py`, `logs/texts.out`. The scratch repositories of this step are under the session's own scratch folder, where this workspace allows git write verbs |

## Item 7, code scanning

The API facts against the table of the lane before this one (`2026-11-20_B1796_verify/CODEQL-FIRST-PR.md`), re-read 19:59:16:
**unchanged** in every row (the rules on `main`, the ruleset, the default setup with `csharp` and `python` and the extended
suite, 2 analyses on `main` with 0 results, 0 alerts of any state, 7 check runs on `main`, 2 workflows, the repository's
settings, the login's rights), but for the expected rows: 8 workflow runs (this lane's push is the eighth), 4 branches, still
1 pull request (merged) and 0 open.

**What the hosted check is likely to report for this code: 0 alerts.** A reading of the query sources on this machine
(`csharp-all` 7.4.2), not a run: `CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof`.
- The clear-text queries need a sink (a logger call, a trace call, a file write, a cookie). The lane has none: no logger, no
  file access, no trace (each count 0).
- Their sources: a variable or a method named with `password` (and the other words of that list), or a METHOD CALL with an
  argument whose constant text matches. The lane has five added lines with the word: two lines of a list (three registered
  attribute names), a comment of a fixture, a constructor call in a test (not a method call), and ONE method call in a test,
  `Find("job-password")`, whose result goes into an assertion only. No path to a sink.
- No remote source, no regular expression, no deserialiser, no process start, no random number in the library.
- Python: no Python file changes (each is byte-equal to `main`, where the analysis reads 0 results); not re-run.

**A trap for the lanes that follow:** a call such as `group.Find("job-password")` is a sensitive source by that query's own
reading. The first lane that hands what such a call returns to a logger or writes it to a file draws an alert at 7.5, and the
rule on `main` blocks at high or above. The fix there is not to log or store the value; never a dismissal.

## Graded claims of the STATUS

True as measured: the commit, its one parent and 27 paths; the frozen blocks; no package; 217 tests on this machine and on
both hosted legs; 106 methods; the seven mutants killed (one count differs by one, above); the checks (b) to (h) the gate
re-ran (ASCII, rules, scanner, names, hosts, the counts of (g), the three parts of (h) with the same numbers 67, 21, 52, 351);
the hosted lines; the push read-back; findings 3a to 3h. Not shown by the gate: the red-first build of Step 3 (58 errors),
the predictions file's time, the two publish folders locally (the hosted GUARD lines show 10 and 11), the history entry.
Contradicted by the gate's numbers: nothing stated as measured. Deviation 4's reason is the one judgement the gate does not
share (finding 1).

## FOUND / TESTED / HOW

- FOUND: 1 Major (close under a read), 4 Minors on the code and its tests (a second read; the delimiters; the memory factor;
  three behaviours without a test), 4 for the records.
- TESTED: everything in the tables above, in the gate's own clone, with the project's SDK and the gate's own home, package
  cache and build output.
- NOT TESTED / NOT RUN:
  - Nothing against a printer, a simulator, a tenant or the print service; no captured byte exists, so every fixture and both
    requests stay PROVISIONAL. What the two other encoders prove is that three implementations agree on the framing.
  - The stream against a real HTTP client: every body and fetch was a fake of the gate's. How a real client's body ends a
    pending read on dispose (finding 1 rests on two of the four ways a body can end it) is UNMEASURED.
  - Reads from several threads at once; only the one overlap of finding 2 was run.
  - CodeQL for C# (cannot extract on this machine). CodeQL for Python and for the workflow language: not re-run (no such file
    changed).
  - Windows locally (the hosted leg ran). The container build. The two publishes locally.
  - `git merge-tree` (refused by a hook); the merge with the logging lane's branch is described by rule in landing.txt, not run.
  - The Workpath source was read, never run. Of the request file the gate read lines 1 to 30, 158 to 284, 392 to 450 and
    492 to 602 by eye and the whole by program; the stream's file whole.
  - The kit's `.measured` sidecar, the design documents and report A3 were not opened; their lines in the kit are RELAYED.
  - Known-vulnerability status of the packages (none is new in this lane).
  - Why the builder's local scan counted 134 objects and the hosted one 133.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt
(landing.txt opens with DO NOT LAND THIS HEAD; the texts are true at this head and are written again by the gate of the fix
round).
