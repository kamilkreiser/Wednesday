## What this adds

A library, `src/Datasec.Suite.UniversalPrint` (one folder, `Ipp/`), and its tests, `tests/Datasec.Suite.UniversalPrint.Tests` (137 test methods, 284 test cells; at the branch head, which also holds main, the solution runs 476 tests on both legs). Three commits: the first adds the library; the second makes the document stream stop at its close, refuses a second read while one is in flight, takes the attribute groups that the encoding keeps for later documents, and adds tests that compare every name list whole; the third merges main into the branch and changes no line of the library (the solution file keeps the projects of both sides).

**Nothing in this library talks to anything. It opens no connection and holds no address, token, key or certificate. The server does not reference it yet, so nothing of it runs in the product. It is unit code with unit tests.**

**Every byte fixture is PROVISIONAL.** Each was built by reading the public encoding standard and the source of the Workpath Universal Print app. None was compared with bytes captured from a printer or from the print service, because no capture exists.

It holds three things:

1. a reader and a writer of the IPP wire encoding;
2. the builders of two requests (Get-Jobs and Acknowledge-Job), three name lists, the list of success codes and the difference of two snapshots, re-expressed from the Workpath app's logic;
3. a stream that yields the bytes of one document, fetched in ranges through a function it is handed, and resumes after a failed read.

## The reader and the writer

- The reader takes one packet from a stream and stops at the end tag. It consumes no byte beyond it, so what follows (a document) stays with the caller.
- Anything that is not a well-formed packet ends in one exception type, `IppFormatException`: a packet cut short, a negative length, a value whose length does not fit its kind, a collection that breaks its framing, a name that is not UTF-8.
- Two bounds: a packet of more than 1 MiB is refused (the caller may give another bound), and collections nest at most 32 deep.
- Attribute groups: the delimiters 0x01, 0x02, 0x04 and 0x05, and every delimiter from 0x06 to 0x0f (which the encoding keeps for the groups of later documents), start a group. A group keeps its tag byte, so writing what was read gives the same bytes. A delimiter of 0x00 is refused. Whether the print service ever sends a group from 0x06 to 0x0f has not been measured.
- A value tag the reader does not know is kept with its bytes and written back unchanged.
- An exception thrown by the stream the reader reads from passes through unchanged.
- The writer refuses a name or a value longer than 32767 bytes, an attribute with no value, a group tag of 0x00 or 0x03 or a value tag, and nesting deeper than 32.
- Limits, as the reader's comment names them: within its bound the reader may allocate many times the bytes it reads (about eighty times for a megabyte of group delimiters, measured outside the repository and held by no test), so a caller that reads from a peer it does not trust passes a small bound; a source whose read never returns holds the reader; the count a source reports is trusted.

## The two requests and the lists

- Get-Jobs: the charset, the language, `printer-uri`, `output-device-uuid`, and for a named user `requesting-user-uri` and `my-jobs`. The address of the print service is a parameter. The library holds no default address.
- Acknowledge-Job: the charset, the language, three device addresses (`ipp`, `ipps`, `https`), `job-id`, `output-device-uuid`. The device host and port are parameters with no default.
- Ported as the Workpath app has it: Acknowledge-Job carries no `printer-uri`, and its charset value is spelt `UTF-8` where Get-Jobs has `utf-8`.
- **Not measured by anyone: the version (2.0), the request id (1) and the two leading attributes of Get-Jobs.** The Workpath app leaves them to its IPP library; here each is a setting with a provisional default.
- The lists: 14 job attributes copied into a print job; 30 device attributes never sent to the print service; five watch sets of 14, 19, 4, 8 and 3 names (48 in all); six success codes. Each list was compared with the Workpath source by program and is equal as a set. One name, `printer-name`, is in both the blocked list and a watch set, as in the source. The tests compare every list whole with an expected list kept in the test project, so a name exchanged, lost or added fails a test.

## The document stream

- It asks for the range from the bytes already yielded to the end of the document, requires status 206 and a `Content-Range` whose start is the offset asked for, reads and drops the IPP packet at the start of every answer, and yields document bytes only, never more than the total it was given.
- A read that fails with an I/O error, or an answer that ends early, is followed by a wait and a new fetch at the offset reached: at most three retries at one offset, and the count starts again whenever bytes arrived. The waits (1, 2 and 4 seconds, plus up to 299 ms) and the jitter are functions the caller hands in. Nothing in the library sleeps.
- **Closing.** Once the stream is closed (by `DisposeAsync`, `Dispose` or `Close`, from any thread), nothing is fetched, nothing is waited for, no read of a body is started, no read returns a count, and every answer the stream holds or receives is disposed. A read in flight at the close ends in `ObjectDisposedException` when the call it is waiting on returns, with the exception that ended that call inside it. The caller's own cancellation still leaves as the platform's cancellation exception.
- **One read at a time.** A second read while one is in flight is refused with `InvalidOperationException`. A body that reports more bytes than it was asked for, or more than remain, is a fetch error that is not retried. The stream may be closed from any thread; nothing else about it is safe to use from two threads at once.
- Limits, as the stream's comment names them: a fetch or a wait in flight at the close is not cut short (the read ends when that function returns); a read of a body that neither ends when the body is disposed nor honours its token never ends; bytes a body writes into the caller's buffer during a read that the close then ends are not reported and may be in that buffer; how the body of a real HTTP client ends a read in flight when it is disposed is not measured; the retry limit counts failures at one offset, so answers that each give at least one byte before they fail are not bounded by it (the caller's fetch function or its token is the bound). The fetch, delay and jitter functions and the start of a read of a body are called under a short lock that a close also takes: a close from another thread waits until such a call has handed back its task, and a function that, while called, waits for the thread that is closing never returns.
- Ported as the Workpath app has it:
  - a failure of the fetch itself, or of its answer, is not retried (a status other than 206, a missing or mismatched `Content-Range`, no body, a packet that does not parse);
  - an exception from a body that is not an I/O error is not retried and leaves as it is (with the stream open);
  - the end and the total named by `Content-Range` are not checked;
  - the IPP status inside each answer is not checked (the caller can read the last dropped packet);
  - the stated ceiling of 10 seconds is never reached: the longest wait is 8 seconds plus the jitter.
- Where the port differs from the Workpath app (read in its source, not run):
  - the unit word of `Content-Range` is read in any letter case (by its source, the app reads lower case only);
  - numbers are ASCII digits only, with no sign;
  - status 416 is a typed error that names the offset (by its source, the app fails there with a missing-object error);
  - a packet that does not parse at the start of an answer leaves as the format exception, not as an I/O error;
  - reads are asynchronous only;
  - the closed state is also looked at between a failed read and its wait (by its source, the app waits once more there).

## What stays open

This is a part of the work package. Still to build, each needing a device, a tenant or a later change: the polling and its interval; the size probe; the other requests (Fetch-Job, Fetch-Document, Update-Job-Status, Update-Output-Device-Attributes, the print job to the device); the transport; the push to the device; PIN forwarding; status; the test with a document of 1 GB; registration and the device token.

## Shared files

- `Datasec.Suite.slnx`: two lines added, one in each folder block. No package is added, and no line of `Directory.Packages.props`, of the workflow or of `build/` changes.
- The Layout and Reserved names lists of the root `README.md` are not updated here; one pass updates them after the related changes have landed.

## Who chose what

Every choice inside this change (what of the two Workpath files is ported and what is left out, the names, the two bounds, the provisional defaults, the strict readings, the exception types of a close and of a second read, taking the later group delimiters, the limits named above and the differences from the app) was made by the build's coordinator or by the builder. None is a product decision, and each can be changed.

## Not tested

- Nothing was compared with captured bytes. No printer, simulator, tenant or print service was reached.
- Every fetch and every body in the tests is a fake. No real HTTP client was put under the stream, so how such a client's body ends a read in flight at a close is not known.
- The three request fixtures were rebuilt by a second encoder written from the standard (equal byte for byte) and by the print library of the test machine's operating system (the two Get-Jobs requests equal; Acknowledge-Job equal but for the letter case of `UTF-8`). That shows two implementations agree on the framing. It does not show what the Workpath app sends.
- The repository's tests check totals beyond 2 GiB by arithmetic only. A made-up document of 4 GiB was streamed through the stream outside the repository with failures planted around 2 and 4 GiB, with no wrong byte; no real document of that size was fetched.
- Code scanning has not read this code before this pull request; it could not be run for C# on the machine the change was checked on.
- The Windows leg ran on the hosted runner only.

Nothing is deployed. Nothing was sent to anyone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
