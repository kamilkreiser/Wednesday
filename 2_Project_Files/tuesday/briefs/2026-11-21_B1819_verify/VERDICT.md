GATE B1819: GO WITH FINDINGS @ ec75619 on main c56f3f3

Gate G1 Tier 1, round 2 of 2 (the last) of OXPd 2, WP4.2 (part): the fix round (kit B1802, seat X9). Head
`ec75619ed6e97f1fc0bbacb87660eae3fdbe4dca` on the branch `b1788/wp42-ipp-encoder`, one commit on the round-1 head
`9f4238adbd465bf7924878982a7444341d9c7152`; `main` is `c56f3f3b015fae8d47288aa9d6c636ecd8fe2191`. Read and measured
2026-11-21 from 08:20 AEDT (clocks by `date`) on Opus 5.5, in the gate's own clone `/private/tmp/b1819-gate/clone` (push URL
`invalid://no-push`). Every number below was printed by a program; programs and logs are under `/private/tmp/b1819-gate/`
(`scratch/`, `logs/`, `probes/`). Every heavy job went through the wave's lock (`.tools/wave1-heavy.lock.d`, by `mkdir`,
`owner.txt`, released by moving it into `/private/tmp/b1819-gate/_quarantine/locks/`) with load1 under 7 before it.

**BLUF.** GO WITH FINDINGS: no Blocker, no Major. The round-1 Major is closed: the round-1 generator's own close rows now
read "ends with ObjectDisposedException; fetches after the close 0; waits after the close 0; bodies left open 0 of 1", and
ten more shapes of the gate's own around a close (in the wait, in the jitter, from inside each caller function, cancel and
close together 2,000 times, every exception type, the three ways of closing racing 5,000 times) end only in ODE or the
caller's OCE with nothing fetched, waited or left open. Findings 2, 3 and 5 are closed; 4 is a named limit. The builder's
short lock and private wrapper are kept: the lock is never held across an await, re-enters, and its one deadlock (a caller
function that waits for the closing thread) is real, measured, and said truly in the comment. One Minor for the records (a
stated cancellation behaviour without a failing cell; the code is right). **But this head does not merge onto today's main:
one conflict in the solution file, against the logging change; it needs one resolution commit, which is a head no gate has
read (landing.txt says exactly what it must hold). Nothing talks to anything and the server does not reference the library.**

## Item 1: the round-1 findings, closed or not, by the gate's own run

The round-1 generator, fake fetch functions and bodies (`probes/Fuzz`, copied from the kept folder
`fleet/state/s301/d1802/gate/`, 124 files, every sha256 equal to its `MANIFEST.sha256` row) were rebuilt against the library
built from the new head (the probe's copy of the dll has the same sha256 as the clone's build) and run in its three modes.
Every row was laid beside round 1's log by program with the times masked (`logs/fuzz-{stream,reader,worst}.log`).

| Round-1 finding | Round 1's row (old head) | The gate's run at `ec75619e` | Closed? |
|---|---|---|---|
| **1 (Major): a close under a read** | S8 rows 1 to 4 (DisposeAsync / Dispose; the body ends the held read with an I/O error / with 0 bytes): "the pending read RETURNS 4 byte(s) after the close; fetches made AFTER the close: 1; waits asked after the close: 1; bodies left open: 0 of 2 / 1 of 2" | the same four rows: "the pending read ends with ObjectDisposedException; fetches made AFTER the close: 0; waits asked after the close: 0; bodies left open: 0 of 1; a read after the close: ObjectDisposedException". Rows 5 and 6 (the body ends it with `ObjectDisposedException`) unchanged and right; rows 7 and 8 (a body that never ends its read) "NEVER ends; 0; 0; 0 of 1": unchanged, now a named limit in the type's comment. "closed twice and once more": unchanged (ODE, body disposed, `CanRead` false) | **CLOSED** |
| 2 (Minor): a second read in flight | S9: "no refusal: the second read got 10 bytes, the first 10; the stream yielded 20 bytes for a document of 10; Offset reads 20" | S9: "the second read is refused: InvalidOperationException" | **CLOSED** |
| 3 (Minor, decided by nobody): delimiters 0x06 to 0x0f refused | DELIMITERS: 0x06 to 0x0f `refused/refused`; S5 "group delimiter 0x06": `IppFormatException, yielded 0` | DELIMITERS: 0x00 `refused/refused`, 0x01 to 0x0f each `taken/taken`; S5 "group delimiter 0x06": `no exception, yielded 10` (the rig does not close the stream after a whole read, so its "body disposed False" is the held answer, as on every other taken row) | **CLOSED** as the kit's Stamp ruled (taken, tag kept) |
| 4 (Minor): ~80x allocation inside the bound | WORST rows: 80.0, 36.0, 21.6, 18.9, 12.0, 9.2, 1.0 MiB | every "allocated" figure equal (only the time columns move) | named in `IppReader`'s comment, as the kit put it IN (a named limit, no code): **CLOSED as a named limit** |
| 5 (Minor): three behaviours with no failing control | mutants g4 and g17 SURVIVED (217 of 217 green); the lists fixed by count and 2 or 3 names | g4 KILLED (2 red: `A_length_of_0x8000_ends_in_the_format_exception...` rows); g17 KILLED (4 red: the unreadable-Content-Range theory's two new rows and the parse cell's two); builder m7 KILLED (3 red, among them `Every_name_list_equals_it...`); the gate's own list mutants are the builder's mL1 to mL8 (not re-run by the gate: m7 stands in) | **CLOSED** |
| 6a to 6d, 7, 8, 9 (records) | - | OUT of the kit, unchanged (6b now a named limit in the stream's comment) | records only (FOR-RECORDS.md) |
| g19 (equivalent in round 1) | survived: `DisposeAsync` closed the body twice | text gone (one close routine): see the mutant table | carried by o13, o14, o26 |

Rows that changed against round 1, all of them, by program over the three logs (times masked): stream 6 lines (S5 delimiter
0x06; S8 rows 1 to 4; S9); reader: DELIMITERS, BOUND -1 and BOUND -2147483648, the accepted/format counts of five rows (single-byte
mutations, random bytes, the biased start, the gate's packets changed, the delimiter row) and TOTAL, the other differing
lines in time only; worst: time and memory-held columns only. Nothing else moved. **The reader's TOTAL at the new head:** `inputs 731132 |
accepted 355910 | format exception 370802 | OTHER exception types from bytes 0 | write(read(x)) differs 0 | consumed wrong
0 | one-byte-per-read differs 0 | largest single read 32767` (661 more inputs accepted than round 1: the mutations that now
hold a delimiter 0x06 to 0x0f; `write(read(x)) differs 0` still, so the tag is kept on every one). **The soak (S12)**: 0
runs with a wrong, repeated or lost byte or more than the total; 0 bodies left open after the close; unchanged.

**BOUND -1 and BOUND -2147483648** now read `ArgumentOutOfRangeException` where round 1's log reads `accepted`. The source line
`IppReader.cs:26` (`ThrowIfNegativeOrZero`) is byte-equal at both heads; the builder reports the same probe against the
first seat's build of the old head printing `ArgumentOutOfRangeException` too. The round-1 log line is the anomaly, not the
code (see item 1b below).

**The review's mutant table at the new head** (`scratch/mutants.py`: round 1's program with its paths changed and its one flaw
fixed, a two-edit entry now applies both edits; the mutant tree a plain copy of the clone without `.git`, `bin`, `obj`;
after the last undo 0 files differ; `logs/mutants.out`): of the 37 entries, **34 KILLED, 0 SURVIVED, g2 BUILD FAILED
`CS0649` as in round 1, g19 and g19b DO NOT APPLY AS WRITTEN** (their text `_disposed = true;` / `await CloseBodyAsync()` is
gone: both ways of closing now go through one routine). Every other entry's text applied exactly once. Counts of red tests
under each (of 285): m1 81, m2 8, m3 6, m4 10, m5 2, m6 2, m7 3, g1 2, g3 1, **g4 2**, g5 1, g6 1, g7 1, g8 1, g9 1, g10 7,
g11 19, g12 3, g13 13, g14 2, g15 16, g16 2, **g17 4**, g18 1, g20 25, g21 2, g22 1, g2b 2, g23 4, g25 3, g27 2, g28 3, g30 2,
g31 1.

## Item 2: what the fix changed that round 1 never saw

The stream's file was read whole at the head (432 lines). The gate wrote its own probe (`probes/Attack2/Program.cs`, its own
fake body, fetch, delay and jitter, calling only the built library; `logs/attack2-run.log`, 24 rows, every row AS REQUIRED,
8.8 s of wall clock) and 25 mutants of its own on the new code (`scratch/own_mutants.py`, run by the same driver).

**THE REQUIRED QUESTION: what can a caller or a body do around a close that is NOT one of the eight rows, and what does the
stream do with each?**

| # | Handed (the gate's own rig) | Runs | What the stream did |
|---|---|---|---|
| A1 | a close by `Dispose`, `DisposeAsync`, `Close`, on another thread, while the RETRY WAIT is held; then the wait returns | 1 each | the read stays pending until the wait returns (the named limit), then `ObjectDisposedException`; 0 fetches after the close; 1 wait in all; every body disposed exactly once |
| A2 | a close on another thread while the JITTER function runs (it returns 300 ms later) | 1 | the close returned only after the jitter returned (about 301 ms: it waited at the lock); the delay function WAS then called once (the second look runs under the same lock the close was waiting for), so the read ends after that wait, in `ObjectDisposedException`; 0 fetches after the close; 0 bodies open |
| A3 | a close from INSIDE the jitter function (same thread) | 1 | the lock is re-entered (no hang); 0 waits; `ObjectDisposedException` |
| A4 | a close from inside the fetch function; from inside the delay function; from inside a body's read before it hands back its task (each the same thread) | 1 each | no hang in any; `ObjectDisposedException` each; the answer of that fetch disposed exactly once; 0 fetches after the close |
| A5 | a fetch function that starts a close on another thread and WAITS for it (bounded at 1.5 s; unbounded) | 1 each | bounded: the close did not finish inside the wait and finished as soon as the fetch gave up; the read `ObjectDisposedException`. **Unbounded: DEADLOCK, neither the read nor the close returned in 3 s: the named limit, reached** |
| A6 | a fetch function that blocks synchronously for 400 ms; `Dispose` from another thread meanwhile | 1 | `Dispose` returned after about 401 ms (it waits for the call to hand back its task); the read `ObjectDisposedException`; 0 bodies open |
| A7 | the caller's token cancelled AND the stream closed while a read is held: cancel then close; close then cancel; both at once from two threads (alternating `Dispose` / `DisposeAsync`) | 50, 50, 2000 | cancel-then-close: `OperationCanceledException` 50; close-then-cancel: `ObjectDisposedException` 50; at once: OCE 337, ODE 1663, **any other type 0**; fetches and waits after the close 0; bodies open 0 |
| A8 | after the close the body ends the held read with `IOException`, `InvalidOperationException`, `OperationCanceledException` (not the caller's token), `TaskCanceledException`, `ObjectDisposedException`, `NullReferenceException`, `AggregateException` | 1 each | each: `ObjectDisposedException` with that exception inside it; 0 fetches, 0 waits after; 0 open |
| A8b | a body whose own `Dispose` throws, closed while a read is held | 1 | the stream's `Dispose` throws that exception; the closed state is set (`CanRead` false; a later read `ObjectDisposedException`; 0 fetches after); the held read never ends because the throwing body never ended it (the body's fault; the stream starts nothing) |
| A9 | `Dispose`, `DisposeAsync` and `Close` racing on three threads while a read is held | 5000 | a body disposed other than exactly once: 0 runs; a close that threw: 0; the held read other than ODE: 0 |
| A10 | a close at a random point of a read that resumes through many answers (3-byte bodies, waits that yield), three ways | 3000 | ODE 3000; a body disposed other than once: 0 runs; no wrong byte |

Answer in two lines: around a close a caller or a body can close from inside any of its own functions (handled: the lock is
re-entrant), close from another thread at any point (handled: no fetch, wait or body read starts after the close returns,
every answer disposed once, the read ends in ODE or, if the caller cancelled first, OCE, and nothing else), race the three
ways of closing (handled), or end the held read with any exception type (it becomes ODE with that inside). What it can
still do to itself: block a guarded function synchronously, which makes a close from another thread wait as long (A6), and
deadlock if that function waits for the closing thread (A5); and give a body whose read never ends or whose Dispose throws.

**DEVIATION 3, the short lock `_startLock`.** Read at the head: four `lock (_startLock)` statements: in the close (around the
one write `_disposed = true` only), in `StartFetch` (look, then call the fetch function), in `AfterFailureAsync` (look, limit,
jitter function, look, call the delay function) and in `AnswerBody.ReadAsync` (look, then call the body's read). Each body of
a `lock` returns the task the function handed back and holds no `await` (an `await` inside `lock` does not compile in C#).
So it is never held across an await: confirmed. Attacked: deadlock from a close inside a guarded function on the same
thread, none (A3, A4: `System.Threading.Lock` re-enters); a close from another thread while a fetch, delay or jitter
function runs, it waits for that call (A2, A6) and then the read ends right (0 fetches after, 0 open). **Is "a function that
waits there for the closing thread never returns" a limit a caller can meet? Yes, measured (A5), but only with a caller
function that BLOCKS synchronously on work that needs the closing thread: a fetch written as sync-over-async whose
continuation needs a single-threaded context that is the one calling `Dispose`, or a fetch that waits for a lock the closing
code holds around its `Dispose`. A fetch, delay or jitter function that returns its task at once (an `HttpClient` send, a
`Task.Delay`, a random number) cannot meet it.** The comment says it truly ("a close from another thread waits until such a
call has handed back its task, and a function that waits there for the closing thread never returns"). The cost the
builder did not list: a close that never blocked before now blocks for as long as a guarded function runs synchronously
(A6), and a close that arrives while the jitter function runs lets the wait start and the read end only after that wait
(A2: up to 8,299 ms with the real back-off); both fit the comment's words. Without the lock the gate's mutant o1 (the close
sets its state outside the lock) is red in the threaded cell and o24 (the take not atomic) too. **Ruling: KEEP.** For the
transport lane's kit: its fetch function must return its task without blocking (FOR-RECORDS).

**DEVIATION 4, the private wrapper `AnswerBody`.** A `private sealed` class nested in the stream: no public type or member is
added (the builder's member table, the gate's reading). Its effect: every read of a body, the packet reader's reads
included, looks at the closed state under the lock before it starts (the gate's o3, the look removed: 2 cells red, the
packet-read close cell and the threaded cell). It overrides the `Memory<byte>` read and the two disposals and forwards
each to the body; the array overload is not overridden, and both callers (the stream and `IppReader`) use the `Memory`
read (the suite and the generator read every packet through it: 285 green, 731,132 reader inputs). It adds one lock per
read of a body; the worst-case timings of the generator did not move beyond noise. **Ruling: KEEP.**

**`IppTag.IsKnownGroup` now answers true for 0x06 to 0x0f.** Callers, by `git grep -i` over every ref of the origin: at this
head 3 hits, the definition, `IppReader.cs:71` and `IppWriter.cs:30`, and no test calls it directly; on `main` and on the
branches of the card decoders, the logging change and the secret store: 0 hits; `main` references no project of this lane
at all, and nothing packs or publishes the library. So nothing outside this library relies on the old answer. The new
answer is pinned: o21 (back to four) reddens 23 cells, o22 (0x00 taken) 2, o23 (0x03 taken) 1. The name "known group"
still reads true (the groups the encoding reserves). **Ruling: a public behaviour change with no caller outside the
library; safe; say it in the pull request (pr-body.md does).**

**FOR TUESDAY item 6, bytes in the caller's buffer from a read the close ends: a NAMED LIMIT, not a fault.** The stream hands
the caller's buffer to the body (it did in round 1 too: a body that writes bytes and then fails with an I/O error left them
there before this change). The count is never reported and `Offset` does not move (the cell
`Named_limit_bytes_a_body_gives_to_a_held_read_while_it_is_disposed_are_not_reported_and_the_offset_does_not_move`, which the
gate's o4, the look after a body's read removed, turns red). The platform's stream contract promises nothing about a
buffer past the count returned, and nothing after an exception. The comment says exactly that ("Bytes that a body writes
into the buffer of a read which the close then ends are not reported and may be in that buffer"): true.

**The gate's own mutants on the new code** (of 285 tests; `logs/mutants.out`): o1 the close's state set outside the lock:
KILLED (the threaded cell); o2 no look before a fetch: KILLED (3); o3 no look before a body read: KILLED (2); o4 no look
after a body read: KILLED (1); o5 no look after an answer is published: KILLED (1); o6 / o7 no first / second look in the
failure path: KILLED (1 / 1); o8 an I/O error after the close counted as a failure: KILLED (3); o9 the refusal removed:
KILLED (5); o10 the read flag never released: KILLED (37; the run was stopped by the gate after 6 minutes of timed-out
cells, its log already holding 37 failures); **o11 any cancellation exception passes a closed read without the token being
looked at: SURVIVED**; o12 the ending exception not kept inside: KILLED (6); o13 the asynchronous close disposes
synchronously: KILLED (1); o14 the synchronous close leaves the answer open: KILLED (9); o15 a refused answer disposed by the
read even when a close took it: KILLED (4); **o16 `read > _totalBytes - _offset` removed: SURVIVED, as the builder states
(the second half of the comparison cannot fire while the refusal stands; with `wanted` capped to what remains the first half
implies it)**; o17 `read > wanted` removed: KILLED (1); o18 an over-reporting body not closed: KILLED (2); o19 the look before
the publish (the order reversed): KILLED (3); o20 `CanRead` always true: KILLED (4); o21 to o23: above; o24 the take of the
answer at the close not atomic: KILLED (the threaded cell); o26 the asynchronous close leaves the answer open: KILLED (12;
stopped by the gate after 4 minutes of timed-out cells). 25 own mutants: 23 killed, o16 survived as the builder named it,
o11 survived: finding 1.

## Item 3: scope and the texts (`scratch/scope_text.py`, `logs/scope_text.log`)

- **Scope:** `9f4238ad..ec75619e` is 11 rows, M 7 and A 4, every path under `src/Datasec.Suite.UniversalPrint/Ipp/` or
  `tests/Datasec.Suite.UniversalPrint.Tests/` and ending `.cs` (outside 0; control: a planted `M Datasec.Suite.slnx` row is
  flagged). `git diff --quiet` over the solution file, `Directory.Packages.props`, `README.md`, `.github`, `build`,
  `global.json`, `Directory.Build.props`, `NuGet.config`, `.gitignore`, `.editorconfig`, both project files and both lock
  files: rc 0 (control: the same over `IppTag.cs` rc 1). Modes 100644 only; binary rows 0; the head's one parent is
  `9f4238ad`. No package, project or lock file changed.
- **Text:** 1,890 added lines and the commit message: the ban list of the verifier standard (underscore-aware
  `(?<![A-Za-z])<name>(?![a-z])`), B-numbers, ticket keys, clarification ids, seat ids, "product owner", "coordinator",
  "review", "gate", "round n", "finding n", decision words, "Tuesday", and "Opus" or "Fable" outside the attribution line:
  0 hits (control: a planted `_by_<name>_` line and one line per pattern each fire). Non-ASCII bytes 0, tabs 0; hosts after
  a scheme 0; IPv4 0; identifiers 0; mail-like values 0. The subject is the kit's, 106 bytes.
- **Attribution and identity:** the message holds exactly one attribution line, `Co-Authored-By: Claude Opus 5.5
  <noreply@anthropic.com>`. Author and committer e-mail both equal the repository checkout's own local `user.email`, the
  author name equals its local `user.name` (compared in-process, not printed), and the identity is the same as on the
  round-1 commit. The STATUS says the work ran on Fable 5.2 until 22:21 on 2026-11-20 and on Opus 5.5 from 08:05 on
  2026-11-21 (its THE RESUME and DEVIATIONS 2): confirmed as written; Tuesday's answer quotes the product owner's word for
  Opus.
- **The comments, by property:** each new comment is ASCII and names no person, number or round. Every sentence of the
  stream's `<remarks>` was checked against the code and the gate's runs above: true as written (the Threads sentence, the
  four limits, the lock sentence). `IppReader`'s new limits paragraph says the 80x figure was "taken from a run outside
  this repository and held by no test here": true. Its sentence "the count a read of the source reports is trusted ... not
  refused (read from the code, UNMEASURED)": true by reading; not run by the gate either.

## Item 5: code scanning: NOT RUN

`CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof`. No analysis has run on this branch
(the default setup analyses a pull request and `main`). Facts by GET at 08:35: the default setup is `configured`, languages
`actions, csharp, python`, suite `extended`; every analysis on `main` and on pull request 2 reports 0 results; open alerts 0.

What the hosted check is likely to report for these 11 files, from a reading of the queries' needs, not a run: **0 alerts
at high or above.** The clear-text logging and storage queries need a sink: the 1,890 added lines hold no logger, file
write, trace, console write or cookie (each count 0); the one output call is the tests' `TestOutputHelper.WriteLine` of
the cells' own counts and exception type names, never an attribute value. Their sources: two added lines hold the word
`password`, both inside the frozen list of expected attribute names (`"job-password-encryption-supported"` and two more),
string elements of an array named for the watched security set, not a variable, field or call named for a credential, and
they reach no sink. No regular expression, deserialiser, process start, random number, path built from input, or
cryptography in the added code. The new synchronisation (`System.Threading.Lock`, `Interlocked`, a `volatile` field) is
outside the security suite's queries. The workflow language and Python: no such file changed (each byte-equal to the
round-1 head, whose pull request 2 neighbour on `main` reads 0 results). The trap round 1 named still stands for the
lanes that follow: a call such as `Find("job-password")` is a sensitive source; this change adds none.

## Item 4: the moved main

Measured in a clone made inside the session's scratchpad (the workspace hook refuses git write verbs in `/private/tmp/b1819-gate`;
it allows them in the scratchpad): `git merge-tree --write-tree --name-only main ec75619e` with main =
`c56f3f3b015fae8d47288aa9d6c636ecd8fe2191`: **rc 1, one conflict, `CONFLICT (content): Merge conflict in Datasec.Suite.slnx`,
and no other path.** The logging change added its two lines in the same places as this lane's two. `Directory.Packages.props`
changed on main only; every other path of this lane is new. **So this branch does NOT merge onto today's main without a new
commit, and a new commit is a head this gate did not read.** The gate made no commit on the branch.

The merged solution file by the wave's ordering rule (every added line kept, each Folder block ordered by the ordinal order
of the Path values), built by program from the two sides' own lines: 13 lines, 699 bytes, sha256
`df48c25f0a60cfd6fca65912d866b15b70ca0efdb701b00d23cba3fcc841179d`, byte-equal to the file the first gate predicted for this
case (`probes/out/slnx_after_logging.txt` of round 1). landing.txt, section 2, prints it. With that file written into the
scratch merge (main plus this head; nothing committed), the gate built and tested the resolved tree: restore rc 0, build 0
warnings and 0 errors, **test total 476, failed 0, succeeded 476** (main's hosted linux leg reads `total: 192` today, read by
GET with the return code asserted; this branch's 285 hold the one base test both share: 192 + 284 = 476). That tree is
not a commit on the origin: the resolution commit, when a seat makes it, needs its own hosted run and a gate reading of that
one commit (landing.txt says what to compare).

## Item 1b: the round-1 BOUND lines, settled

The gate built the OLD head's library (`git archive 9f4238ad`, its own restore and build) and the same round-1 generator
against it (`logs/fuzzold-reader.log`): `TOTAL inputs 731132 | accepted 355249 | format exception 371463`, equal to round
1's log row for row, and DELIMITERS 0x06 to 0x0f `refused`, as round 1 measured; but `BOUND -1` and `BOUND -2147483648` read
`ArgumentOutOfRangeException`. So round 1's two `accepted` lines do not reproduce from round 1's own program at round 1's own
head; the guard at `IppReader.cs:26` refuses every bound of 0 or below at both heads (and the builder's cell L03 says so).
Why round 1 printed `accepted` is UNMEASURED. Not a finding against either head; a correction of the first gate's log.

## The builder's hosted run, re-read

Run of `ec75619e` by GET (`--allow-escape-sequences`, return code asserted 0 for each of the four job logs; 30,244, 24,161,
25,711 and 26,869 bytes; the runner's echo of each script, the lines holding `$` variables, left out; control: a line that is
not there counts 0): linux and windows `0 Warning(s)` 1, `0 Error(s)` 1, `total: 285` 2 (one summary and the step's own
grep), `failed: 0` 1, `GUARD: clean (10 files)` and `(11 files)` 1 each; rules `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53,
floor 53` 1, `RULES: clean (56 files)` 1; secret-scan `PLANTED-CONTROL secret-scan: rc 1` 1, `PLANTED-CONTROL neutral-scan:
planted in 11 places, found by name 1, found under a neutral name 25 of 25, rc 1` 1, `NEUTRAL-SCAN: stored objects 248
(167 blob, 13 commit, 68 tree), copies written 496, objects of this commit not among them 0` 1, `no leaks found` 3. Every
line equals the STATUS. Locally at the head: restore rc 0, build 0 warnings and 0 errors, test `total: 285`, `failed: 0`,
`succeeded: 285`, `skipped: 0`, porcelain 0 lines after.

## Item 6: the landing texts

`pr-title.txt` (the first gate's title, still true), `pr-body.md` (written new for the whole branch: the reader's groups,
the close, one read at a time, every limit as the comments name it, the lock and its cost, what is not tested, who chose;
no sentence of the first gate's section "not right yet" survives), `squash-subject.txt` (ends `(#PRNUM)`),
`squash-body.txt` (ends with the one attribution line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; longest
line 70), `landing.txt` (opens with the merge stop of item 4; the head pinned 3 times and in `--match-head-commit` once; the
check wait of at least 8 ci rows plus the code-scanning rows; the squash line with both text files; the merged solution
file; what to read on main after; that a merge deploys nothing).

Each text, and the shapes a merge tool can build from them, exported through the workflow's own `neutral_export` (cut by
program from the head's `ci.yml`, lines 120 to 128; `ci.yml` is byte-equal on `main`) as a commit message of a scratch
repository and scanned with the workflow's four options, scanner 8.30.1 (`scratch/texts.py`, `logs/texts.out`): the title
alone; title and body; the body alone; the squash message with a number; as written; the squash body alone; the
repository's default squash shape (the title and the two commit messages as a list); landing.txt: **each rc 0, "no leaks
found", stored whole. Control (the squash message with the workflow's planted value joined in): rc 1, "leaks found: 2".
Texts flagged: 0.** In the four texts: ban-list names 0, B-numbers 0, clarification ids 0, ticket keys 0, seat ids 0,
"product owner" 0, "review" or "gate" 0, card ids 0, hosts and identifiers 0, non-ASCII bytes outside the footer 0. Two
pattern hits read by eye: "around 2 and 4 GiB" (a number after "round" inside "around") and "None is a product decision"
(a sentence that nobody decided), as in the first gate's texts.

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| L | **Landing condition** (not a fault of this head's code) | **This head cannot land as it is** | The branch meets the logging change on `main` in `Datasec.Suite.slnx`: one conflict, measured (item 4). The verifier standard's table would call an unclean merge a Major; the wave's kits barred every lane from that file's other lines, the ordering rule settles the bytes, and this commission asks the gate to say so and not to make the commit. The resolved tree builds and passes 476 of 476 in the gate's scratch. | One resolution commit whose only change against the merge is the solution file of landing.txt section 2 (byte-equal, sha256 df48c25f...), its own hosted run, a gate reading of that one commit, then the squash line with its sha. |
| 1 | Minor (records, by the round rule) | No | A stated behaviour of the fix has no test that can fail: a cancellation exception that reaches a read of a closed stream when the CALLER's token is not cancelled ends as `ObjectDisposedException` (the comment's "the caller's own cancellation ... leaves as the cancellation exception"). The gate's mutant o11 leaves all 285 green. The code is right (probe rows A8: OCE and `TaskCanceledException` each ended as ODE with it inside). The builder's "no other was found" missed it. | One cell in any later change of the file; FOR-RECORDS.md section 5 item 1. |
| 2 | Records | No | A close can now wait for a guarded function, and deadlocks if that function waits for the closing thread (A5, A6). Named truthfully in the comment; reachable only by a caller function that blocks synchronously. | The transport lane's kit: an asynchronous fetch that never blocks. |
| 3 | Records | No | A close during the jitter function lets the wait start; the read ends after it (up to about 8.3 s with the real back-off). True to the comment. | A caller that needs a prompt end cancels too. |
| 4 | Records | No | A body whose own `Dispose` throws makes the stream's close throw; a read held in it never ends. | The transport lane's body must not throw on disposal. |
| 5 | Records | No | The round-1 log's `BOUND -1: accepted` lines do not reproduce at the old head (item 1b). | None for the code. |

No Blocker. No Major. **Every round-1 finding the fix kit put IN is closed by the gate's own run** (1, 2, 3, 5; 4 as a
named limit). DEVIATION 3: keep. DEVIATION 4: keep. The `IsKnownGroup` change: safe, no caller outside the library.

## Graded claims of the STATUS

True as measured: the commit, its one parent, 11 paths, M 7 and A 4, nothing outside the two folders; 285 tests locally
and on both hosted legs; the eight X01 rows and R01 (by the gate's own generator, not its cells); the generator rows S8, S9,
S12, DELIMITERS, TOTAL; the BOUND lines at the old head; the review's 37 entries: 34 killed, g2 build failure, g19 and g19b
not applying; every hosted line; the author identity; the attribution line; the list block placed byte for byte (A01
passes; m7 is killed by it). Not shown by the gate: the builder's own mutants by its ids (the gate ran its own 25 in their
place), T01's counts under each mutant (the gate saw T01 red under o1, o2, o3, o19 and o24), the red-first run on the old
head, the scratch-probe member table (the gate read the class and agrees no member reaches a body without the guard), the
history entry. Contradicted: "Statements no cell can fail: ... No other was found" (finding 1).

## FOUND / TESTED / HOW, and what was NOT tested

- FOUND: 0 Blockers, 0 Majors, 1 Minor (a missing control of the fix), 4 records lines, and the landing condition.
- TESTED: everything in the rows above, in the gate's own clone with the project's SDK 10.0.404, the gate's own home,
  package cache and build output, every heavy job under the wave's lock.
- NOT TESTED / NOT RUN:
  - CodeQL for C# (cannot extract on this machine); the hosted analysis has not run on this branch.
  - Anything against a printer, a simulator, a tenant or the print service; every fixture stays PROVISIONAL.
  - A real HTTP client under the stream: every body and fetch was a fake (the builder's, the first gate's, this gate's).
  - Windows locally (the hosted leg ran green, read above).
  - The publishes and the release guard locally (no project changed; the hosted GUARD lines read 10 and 11 files).
  - The resolution commit (none exists); the resolved tree was built and tested only as an uncommitted scratch merge.
  - The builder's own mutant ids mC1 to mC17, mG1 to mG3, mB1 to mB3, mL1 to mL8 were not re-run by those ids; the gate's
    o1 to o26 cover the same looks, refusal, comparison, close routine and groups. The list mutants mL1 to mL8: only m7.
  - The gate's probes A1 to A10 ran once each at the counts shown; no soak of the lock beyond A7 (2,000), A9 (5,000) and
    A10 (3,000) runs.
  - The Workpath source was not opened by this gate; the pr-body's line that the source waits once more between a failed
    read and its wait is RELAYED from the fix kit's FACT 6 and the builder's DEVIATION 7.
  - Why the first gate's log read `BOUND -1: accepted`.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt,
landing.txt.
