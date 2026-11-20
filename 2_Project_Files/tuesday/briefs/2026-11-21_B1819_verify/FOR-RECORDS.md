# FOR RECORDS: gate of the fix round of OXPd 2, WP4.2 (part), head ec75619 on main c56f3f3

For a records pass. Carries forward the first gate's list (`2026-11-20_B1799_verify/FOR-RECORDS.md`), marks what the fix
round closed, and adds what this gate found. Sources: this folder's VERDICT.md (measured), the builder's STATUS (a claim
where not re-measured: RELAYED). Nothing below was filed, sent or decided by the gate.

## 1. State

- **Gate: GO WITH FINDINGS at ec75619e (no Blocker, no Major).** The first gate's Major (a close under a read) and its
  Minors 2, 3 and 5 are closed by the gate's own run; its Minor 4 is now a named limit, as the fix kit put it in.
- **The head does not merge onto today's main as it is:** one conflict, in `Datasec.Suite.slnx`, with the logging change
  that landed as pull request 2. Resolving it needs ONE new commit (the file's bytes are in landing.txt, section 2), and that
  commit is a head no gate has read: it needs its own hosted run and a reading of that one commit before it lands. Whose
  seat makes it, and under which brief, is the coordinator's.
- **WP4.2 and `OXPD2-18` stay OPEN after this lane lands** (unchanged from the first list, section 1: the polling, the size
  probe, the other requests, the transport, the push to the device, PIN forwarding, status, the 1 GB exit test, the WP4.1
  part). **The server does not reference the library.**
- **Every byte fixture is PROVISIONAL** until a capture exists (unchanged).

## 2. The first gate's list for the fix round: what happened to each

| First gate's item | Now |
|---|---|
| 1. Finding 1 (Major), a close under a read | CLOSED (VERDICT.md item 1; the eight rows and ten more shapes of the gate's own, item 2) |
| 2. Finding 2, a second read | CLOSED (refused with `InvalidOperationException`) |
| 3. Finding 5, three tests | CLOSED (g4 and g17 killed; the lists compared whole) |
| 4. The stream's comment on the close and one read at a time | DONE, every sentence true at the head (VERDICT.md item 3) |
| 5. The texts rewritten for the fix | DONE in this folder; the section "not right yet" is gone |
| Open ruling 4, the delimiters 0x06 to 0x0f | BUILT as the fix kit's Stamp chose (taken, tag kept); still decided by nobody above the coordinator; the question for the Workpath team (first list, section 4, item 11) stays |

## 3. Open rulings, DECIDED BY NOBODY (carried; each built one way because the kit or the source has it so)

1. A failed open is not retried (as the Workpath source has it). 2. Status 416 is a typed error, not retried. 3. The IPP
status of a fetched part is not checked. 4. No ceiling on fetches per document: an answer that gives one byte and then
fails resets the retry count (now named in the stream's comment). 5. The bound under which the stream reads the packet of
each answer: the reader's default 1 MiB, with about 80 MiB of allocation for a hostile packet inside it (now named in the
reader's comment); a small bound for a fetched part and a cap on groups are the transport lane's choice. 6. The canonical
text of an attribute for the capability sync (design, WP4.6). 7. The print service's base address and the device port
(configuration, a later lane). 8. **New, from the fix: the exception types of a close (`ObjectDisposedException`, the
ending exception inside) and of a second read (`InvalidOperationException`)**, the coordinator's defaults of the fix kit.

## 4. Questions for the Workpath team (carried unchanged; none was sent; adding them to `OXPD2-1` is the coordinator's)

The first list's section 4, items 1 to 12, unchanged. Item 11 (does the print service ever send a group other than
operation, job, printer or unsupported) now decides only whether the tolerant reading is ever exercised, not whether a
document fails.

## 5. Found by this gate (none blocks the merge; by the round rule a Minor here is a records line, not a third round)

1. **Minor: one stated behaviour of the fix has no test that can fail.** The stream says the caller's own cancellation
   leaves as the cancellation exception, and everything else that reaches a read of a closed stream ends it as
   `ObjectDisposedException`. The gate's mutant o11 (a cancellation exception passes a closed read whatever the caller's
   token says) leaves all 285 tests green. The code is right: the gate's probe ended a held read after the close with a
   cancellation exception of a token not the caller's, and with a `TaskCanceledException`, and got
   `ObjectDisposedException` with that inside each time (VERDICT.md, item 2, row A8). The builder's list of statements no
   cell can fail named only the redundant half of the over-report comparison. Fix shape for any later change of the file:
   one cell, a body that ends its held read with a cancellation exception after the close while the caller's token is not
   cancelled; required `ObjectDisposedException`.
2. **Records: a close can now wait, and in one shape never return.** The fetch, delay and jitter functions and the start of
   a body's read are called under a short lock that a close takes. A close from another thread waits as long as such a call
   runs synchronously (measured: 401 ms behind a fetch that blocked for 400 ms), and a caller function that waits for the
   closing thread deadlocks both (measured). Named in the stream's comment. **For the transport lane's kit: its fetch
   function must return its task at once (an asynchronous send), never block on a result, and never wait for a thread that
   may be closing the stream.**
3. **Records: a close that arrives while the jitter function runs lets the wait start** (the second look runs under the
   lock the close is waiting for), so the pending read ends only after that wait: with the real back-off, up to about 8.3
   seconds after the close returned. True to the comment's "a wait in flight at the close is not cut short" and "none of
   them starts once a close has returned"; a caller that needs a prompt end cancels its token as well.
4. **Records: a body whose own `Dispose` throws makes the stream's close throw** that exception; the closed state is set and
   nothing starts after it, but a read held in that body never ends (the body never ended it). The transport lane's client
   body should not throw from its disposal.
5. **Records: the round-1 log lines `BOUND -1: accepted` and `BOUND -2147483648: accepted` do not reproduce** (see
   VERDICT.md item 1). The reader's guard refuses a bound of 0 or below at both heads.
6. **Records: `IppTag.IsKnownGroup` changed its public answer** (true for 0x06 to 0x0f). No caller outside the library on any
   ref of the origin; nothing publishes the library. Say it in the change log of the first release that ships the library.

## 6. Carried for the kits of the lanes that follow (the first list, section 6, with what changed)

1. **The transport lane (the first caller of the stream):** map every failure of its client's body to `IOException` (an
   exception of another type is not retried while the stream is open); catch `IppFormatException` beside the I/O errors;
   read the packet of a part under a small bound; **the fix is on this branch: a close now stops a read in flight, so
   "close and cancel together" is no longer needed for that, but the fetch function must not block (section 5, item 2)**;
   its test against a real client must cover a close under a read (UNMEASURED by both gates: only fakes were used).
2. **Code scanning trap** (unchanged): a call such as `Find("job-password")` is a sensitive source for the clear-text
   queries; this change adds none.
3. **The solution file:** the ordering rule holds; landing.txt, section 2, gives the merged file after the logging change.
   The card decoders and the secret store will meet the same file again; by ordinal order this lane's two lines stay the
   last of each block.
4. **For gate kits:** the workspace hook refuses `git merge-tree` (and every git write verb) in a clone under `/private/tmp`
   that is not the session's scratchpad; a clone made inside the session's scratchpad may run them (this gate did, for
   item 4). The round-1 mutant program applies only the second of two edits to one file; this gate's copy fixes that
   (`/private/tmp/b1819-gate/scratch/mutants.py`). A mutant that leaves held reads pending runs into the 30-second guards
   cell after cell (o10 ran over 6 minutes under the wave's lock): a gate stops such a run once the log shows a failure.
5. **The README pass after the wave** (unchanged: Layout does not name the two projects; Reserved names still holds the
   library's name).

## 7. Ticket states

- `OXPD2-18` (RELAYED): unchanged by the gate; it does not close on this lane's merge.
- No ticket was read or written by the gate.
