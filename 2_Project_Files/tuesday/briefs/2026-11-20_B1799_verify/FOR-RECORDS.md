# FOR RECORDS: gate B1799 (kit B1788, seat X6), OXPd 2, WP4.2 (part), head 9f4238a on main 7bf3752

For a records pass. Sources: the gate's VERDICT.md (measured rows), the builder's STATUS (sections RECORDS PROPOSED and
FOR TUESDAY; a claim where the gate did not re-measure it, marked RELAYED). Nothing below was filed, sent or decided by the gate.

## 1. State

- **Gate: NO GO at this head, one Major. A fix round follows (round 2 of 2).** No pull request exists for this branch.
- **WP4.2 and `OXPD2-18` stay OPEN after this lane lands**, whatever the fix round does. Left (RELAYED from the STATUS, FOR
  TUESDAY item 1; consistent with the kit's cut): the polling with its interval and stagger; the size probe (`Range: bytes=0-0`);
  the builders of Fetch-Job, Fetch-Document, Update-Job-Status, Update-Output-Device-Attributes and of the print job to the
  device; the transport; the push to the device; PIN forwarding; status; the 1 GB exit test (E4.11) and E4.6; the WP4.1 part
  (registration, device token). **The server does not reference the library.**
- **Every byte fixture is PROVISIONAL** until a capture exists. What would settle it: one captured Get-Jobs request and one
  captured Acknowledge-Job request from a Workpath printer or a test tenant, and one captured answer to Fetch-Document. No
  spike of the plan asks for that capture (RELAYED from the drafter's report, its correction 6): a line for the plan.

## 2. For the fix round (the kit of round 2)

1. **Finding 1 (Major): a close under a read.** Fix shape in VERDICT.md: the closed flag checked at the top of every turn of
   the read loop, after a failed read BEFORE the wait is asked for, and after the fetch returns (an answer that arrives after
   the close is disposed); the pending read ends in `ObjectDisposedException`. Test: a body that ends a pending read with an
   I/O error when it is disposed, and one that ends it with 0 bytes: after the close 0 fetches, 0 waits, every body disposed.
2. **Finding 2 (Minor, same commit): a second read while one is in flight** is refused with `InvalidOperationException`. One test.
3. **Finding 5 (Minor, same commit): three tests.** A length of 0x8000 followed by 32768 bytes; `bytes +0-9/10` in the table
   of unreadable values; each list compared with its whole expected list (the names are registered attribute names, not
   text of the source).
4. The comment of `ResumableDocumentStream` should then say what the stream does on a close, and that it serves one read at
   a time.
5. The texts of this folder (title, body, squash message, landing) are true at the reviewed head only. The gate of round 2
   writes them again; the body's section "Measured in review at this head, and not right yet" must not survive a fix.

## 3. Open rulings, DECIDED BY NOBODY (each is built one way today because the kit or the source has it so)

| # | Point | As built | The other reading | Whose |
|---|---|---|---|---|
| 1 | **A failed open is not retried** (kit Q6; STATUS 3b) | as the Workpath source has it: a status other than 206, a missing or mismatched `Content-Range`, no body, a fetch that throws, a packet that does not parse each end the document at once | retried like a failed read (a change of behaviour against the Workpath app) | product, with the Workpath team's answer |
| 2 | **Status 416** (kit Q7; STATUS 3c) | a typed error that names the offset, not retried | restart from offset 0, which the Secure path's own download does (RELAYED: report A3 line 239) | product |
| 3 | **The IPP status of a fetched part** (kit Q8; STATUS 3d) | not checked; the caller can read the last dropped packet. Measured by the gate: an answer whose packet carries an error status and a sound body is taken and its bytes yielded | an I/O error unless the status is one of the six success codes | product |
| 4 | **Group delimiters 0x06 to 0x0f** (kit row C13; STATUS item 4; VERDICT finding 3) | the whole packet is refused; in the stream that ends the document, not retried | taken as groups kept with their tag (one line; the public reference reader does so) | the coordinator's, before the first lane that reads a real answer; a question for the Workpath team in the meantime (list below, item 11) |
| 5 | **No ceiling on fetches per document** (VERDICT finding 6b) | an answer that gives one byte and then fails resets the retry count: N fetches and N waits for N bytes; as the source has it | a ceiling on fetches or on elapsed time per document | product |
| 6 | **The bound under which the stream reads the packet of each answer** (VERDICT finding 4) | the reader's default, 1 MiB; a hostile packet inside it costs about 80 MiB of allocations | a small bound for a fetched part and a cap on the count of groups | the transport lane's kit |
| 7 | **The canonical text of an attribute** for the capability sync (STATUS item 5) | not ported: the source builds it from its IPP library's printed form | a form of the server's own | design, WP4.6 |
| 8 | **The print service's base address and the device port** | parameters with no default | - | configuration, a later lane |

## 4. Questions for the Workpath team, as ONE list (none was sent to anyone; adding them to the master list `OXPD2-1` is the coordinator's)

Each is read in the source, not run (the builder's 3a to 3h, re-read at source by the gate; 9 to 11 are the gate's).

1. (3a) Acknowledge-Job is built with no `printer-uri`. Intended?
2. (3b) A failed open of a range is never retried; only a failed read is. Intended?
3. (3c) Status 416 returns from the open without a body and the next statement uses the missing body. What should a 416 do?
4. (3d) The IPP status inside each fetched part is read into a name that is never used. Should a part with an error status fail?
5. (3e) The unit word of `Content-Range` in upper or mixed case passes the first test and then reads as missing. Intended?
6. (3f) The 10 second ceiling of the back-off is never reached; the longest wait is 8 seconds plus the jitter. Intended?
7. (3g) `printer-name` is in both the list never sent to the print service and the watched defaults. Which wins?
8. (3h) Report A3 says "0.5 to 10 s back-off"; the source's waits are 1, 2 and 4 seconds plus 0 to 299 ms. (A correction for
   the report, not a question for the team.)
9. What does the app's IPP library put on the wire by itself: the version, the request id, and for Get-Jobs the charset, the
   language and their order? (kit Q4: 2.0, 1, `utf-8`, `en-us`, all provisional.)
10. Acknowledge-Job spells the charset `UTF-8`. Does the app's IPP library send it as written or in lower case? (The operating
    system's print library, used by the gate as a witness, writes `utf-8`.)
11. Does the print service ever answer with an attribute group other than operation, job, printer or unsupported (a document
    group in the answer to Fetch-Document, for one)?
12. Is a capture of the three exchanges available (section 1)?

## 5. The builder's RECORDS PROPOSED (not written by the seat; RELAYED, the gate agrees with each)

- `README.md`, `## Layout`: name `src/Datasec.Suite.UniversalPrint` (folder `Ipp/` built; `Registration/` later) and
  `tests/Datasec.Suite.UniversalPrint.Tests`; take the first out of `## Reserved names` (its line 47). One README pass after
  the wave.
- `SETUP_RUNBOOK.md`: (1) a local `dotnet test` of a solution with two test projects prints ONE summary (confirmed by the
  gate: one `total: 217`); (2) the wave's heavy lock path and form (worked for the gate as the kit's Stamp S4 writes it: 85
  takes); (3) analyzer rule CA2022 is an error here: a test must use the count a stream read returns.
- `BACKLOG.md`: the open points of section 3, and the three lines of section 6.

## 6. For the kits of the lanes that follow

1. **The transport lane (the first caller of the stream):** map every failure of its client's body to `IOException`, or the
   stream ends the document without a retry (VERDICT finding 6a); catch `IppFormatException` beside the I/O errors (deviation
   8); read the packet of a part under a small bound (ruling 6); close and cancel together until the fix of finding 1 is on
   `main`; its test against a real client must cover a close under a read (UNMEASURED by the gate: only fakes were used).
2. **Code scanning trap:** a call such as `Find("job-password")` is a sensitive source for the clear-text queries (a method
   call with an argument whose text holds `password`). Handing what it returns to a logger or a file write draws an alert at
   7.5, which blocks a merge to `main`. This lane has no such sink; the first lane that logs attributes will.
3. **The solution file:** by the ordering rule this lane's two lines are the last line of each Folder block whichever lanes
   land first (landing.txt, line 2, with the file as it must read after the logging lane). A branch brought onto a later
   `main` is a new head and needs its own hosted run and gate reading.
4. **For gate kits:** a restore with the network closed ends rc 1 here (`NU1900`, the restore's own audit, an error through
   warnings-as-errors): a gate's restore must reach the package source. A hook of the coordinator's workspace refuses
   `git merge-tree` outside the coordinator's folder even in the gate's own clone: the merge step of the verifier standard
   cannot be run as written; the gate used `rev-list --parents` and `merge-base`.
5. **A local witness exists for the wire encoding:** the operating system's print library builds and reads packets in-process
   on local files (no network call, no daemon call). The gate's program is `/private/tmp/b1799-gate/scratch/witness.py`
   (scratch: it may be cleared). A later lane that adds request builders can be checked the same way.

## 7. Ticket states

- `OXPD2-18` (Task, Backlog, under `OXPD2-6`; RELAYED from the kit): unchanged by the gate. It does not close on this lane's
  merge.
- No ticket was read or written by the gate.
