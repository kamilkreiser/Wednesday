## What this adds

A library, `src/Datasec.Suite.UniversalPrint` (one folder, `Ipp/`), and its tests, `tests/Datasec.Suite.UniversalPrint.Tests` (106 test methods, 216 test cells; the solution now runs 217 tests on both legs).

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
- A value tag the reader does not know is kept with its bytes and written back unchanged.
- **The reader takes four attribute groups only (operation, job, printer, unsupported). The public register lists five more group delimiters (0x06 to 0x0a). An answer that holds one is refused whole.** Whether the print service ever sends one has not been measured.
- An exception thrown by the stream the reader reads from passes through unchanged.
- The writer refuses a name or a value longer than 32767 bytes, an attribute with no value, and nesting deeper than 32.
- Measured in review: a hostile packet of 1 MiB made of group delimiters alone costs about 80 MiB of allocations before it is taken or refused. The cost is bounded by the bound; it is about eighty times the bound.

## The two requests and the lists

- Get-Jobs: the charset, the language, `printer-uri`, `output-device-uuid`, and for a named user `requesting-user-uri` and `my-jobs`. The address of the print service is a parameter. The library holds no default address.
- Acknowledge-Job: the charset, the language, three device addresses (`ipp`, `ipps`, `https`), `job-id`, `output-device-uuid`. The device host and port are parameters with no default.
- Ported as the Workpath app has it: Acknowledge-Job carries no `printer-uri`, and its charset value is spelt `UTF-8` where Get-Jobs has `utf-8`.
- **Not measured by anyone: the version (2.0), the request id (1) and the two leading attributes of Get-Jobs.** The Workpath app leaves them to its IPP library; here each is a setting with a provisional default.
- The lists: 14 job attributes copied into a print job; 30 device attributes never sent to the print service; five watch sets of 14, 19, 4, 8 and 3 names (48 in all); six success codes. In review each list was compared with the Workpath source by program and is equal as a set. One name, `printer-name`, is in both the blocked list and a watch set, as in the source.
- The tests fix the count of each list and a few names. They do not fix every name.

## The document stream

- It asks for the range from the bytes already yielded to the end of the document, requires status 206 and a `Content-Range` whose start is the offset asked for, reads and drops the IPP packet at the start of every answer, and yields document bytes only, never more than the total it was given.
- A read that fails with an I/O error, or an answer that ends early, is followed by a wait and a new fetch at the offset reached: at most three retries at one offset, and the count starts again whenever bytes arrived. The waits (1, 2 and 4 seconds, plus up to 299 ms) and the jitter are functions the caller hands in. Nothing in the library sleeps.
- Ported as the Workpath app has it:
  - a failure of the fetch itself, or of its answer, is not retried (a status other than 206, a missing or mismatched `Content-Range`, no body, a packet that does not parse);
  - the end and the total named by `Content-Range` are not checked;
  - the IPP status inside each answer is not checked (the caller can read the last dropped packet);
  - the stated ceiling of 10 seconds is never reached: the longest wait is 8 seconds plus the jitter.
- Where the port differs from the Workpath app (read in its source, not run):
  - the unit word of `Content-Range` is read in any letter case (by its source, the app reads lower case only);
  - numbers are ASCII digits only, with no sign;
  - status 416 is a typed error that names the offset (by its source, the app fails there with a missing-object error);
  - a packet that does not parse at the start of an answer leaves as the format exception, not as an I/O error;
  - reads are asynchronous only.
- **Measured in review at this head, and not right yet:**
  - **Closing the stream while a read is in flight does not stop it.** If the answer's body ends that read with an I/O error or with no bytes, the stream waits, fetches once more, hands bytes to the abandoned read and leaves the new answer open. By its source, the Workpath app stops at this point.
  - A second read started while one is in flight is not refused. With an answer that goes on beyond the range asked, the two reads together yielded more bytes than the document has.
  - An exception from the body that is not an I/O error is not retried and leaves as it is.
  - An answer that gives one byte and then fails makes progress each time, so the retry limit never applies: a document of N bytes can cost N fetches and N waits.

## What stays open

This is a part of the work package. Still to build, each needing a device, a tenant or a later change: the polling and its interval; the size probe; the other requests (Fetch-Job, Fetch-Document, Update-Job-Status, Update-Output-Device-Attributes, the print job to the device); the transport; the push to the device; PIN forwarding; status; the test with a document of 1 GB; registration and the device token.

## Shared files

- `Datasec.Suite.slnx`: two lines added. No package is added, and no line of `Directory.Packages.props`, of the workflow or of `build/` changes.
- The Layout and Reserved names lists of the root `README.md` are not updated here; one pass updates them after the related changes have landed.

## Who chose what

Every choice inside this change (what of the two Workpath files is ported and what is left out, the names, the two bounds, the provisional defaults, the strict readings, the differences from the app listed above) was made by the build's coordinator or by the builder. None is a product decision, and each can be changed.

## Not tested

- Nothing was compared with captured bytes. No printer, simulator, tenant or print service was reached.
- In review the three request fixtures were rebuilt by a second encoder written from the standard (equal byte for byte) and by the print library of the review machine's operating system (the two Get-Jobs requests equal; Acknowledge-Job equal but for the letter case of `UTF-8`). That shows two implementations agree on the framing. It does not show what the Workpath app sends.
- The repository's tests check totals beyond 2 GiB by arithmetic only. In review a made-up document of 4 GiB was streamed through the stream with failures planted around 2 and 4 GiB, with no wrong byte; no real document of that size was fetched.
- Code scanning has not read this code before this pull request; it could not be run for C# on the review machine.
- The Windows leg ran on the hosted runner only.

Nothing is deployed. Nothing was sent to anyone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
