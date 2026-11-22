# FOR RECORDS: job service lane (WP1.7 in part, lane G), gate round 3 (test-only delta), reader B1888

Not repository text. For Tuesday's records pass (backlog, design notes); nothing here was written into the project.

## What lands in this lane (three commits and two merges of main, squashed)

- JobSpool (encrypted per-job spool, AES-256-GCM chunks, key in memory only, wipes by job, session, lifetime, Sweep
  and start), ScanReceiver (scan secret shown once, SHA-256 kept, fixed-time compare, one JobNotFound for every
  refusal of secret or job, streaming multipart receive within caps and a bound, a failed upload wipes the job),
  PrintJobSender (Print-Job from the IPP library's public types, answer accepted only when it is the request's and
  valid, TrackAsync polling). 18 typed reasons; the host does not use the library.
- Round 2: own-cancellation of a transport or answer stream is TransportFailed; every bound armed before a caller's
  code (pool thread); a refused file stays refused.
- Round 3 (this delta): A03's reachability walk skips six types (TimeProvider, Task, CancellationTokenSource,
  CancellationToken, CancellationTokenRegistration, ExecutionContext, by IsAssignableFrom). Test-only, one file,
  +19 -2, byte-equal to the kit's 1-a03.diff.
- Totals (MEASURED by this reader): branch 1524 tests (main ca94ed96's 1404 RELAYED + 120), 476 files; with lane I
  at ff1defac also merged: 1524 tests, 478 files, build/tests Ran 108 (floor 108).

## Named limits

1. **The A03 walk does not see text kept as the state of ANY skipped object** (a clock, a task, a cancellation
   token, source or registration, an execution context), not only inside a Task. MEASURED here: mKeepTask (text in a
   completed Task field) survives; reader B1889's mKeepInGone (text as the state of a callback registered on a job's
   Gone source: `_ = _spool.GoneToken(job).Register(static _ => { }, text);` in OpenScan) also survives at the head,
   re-run by this reader (Jobs project total 120, failed 0, the mutant's library rebuilt after the edit; undone, cmp
   equal). That it is red at HEAD2 is RELAYED from B1889. The library holds no such text today: `git grep 'Register('`
   in src/Datasec.Suite.Jobs at edaa1b70 rc 1 (0 lines; control: `GoneToken` 2 lines, `CreateLinkedTokenSource` 3
   lines, whose callbacks' state is the linked source, not text, DERIVED from the runtime); 0 static fields
   (DERIVED by grep: every `static` declaration in the library's .cs files is a method or a class); 0 AsyncLocal,
   ThreadLocal or ThreadStatic (rc 1). Stated in pr-body.md and squash-body.txt.
2. Stamp S4's limits outside the frame (RELAYED; nothing read here contradicts them): a static field, an async-local
   or thread-local value, text held inside a host-supplied TimeProvider subclass.
3. mReasonDisposed remains a named survivor; the W02 body cell (2-w02-body.diff, drafted and measured by the kit's
   drafter) was left out this round by Stamp S4 (Q38 NO). A body whose read throws ObjectDisposedException ends
   JobNotFound (B1866 F2, RELAYED; stated in pr-body.md).
4. B1866 F3 (RELAYED): a good answer whose close never completes ends ResponseTimedOut at the send bound (30 minutes);
   the README's "An answer stream that fails to close changes nothing" holds for a close that throws, not one that
   hangs. Stated in pr-body.md; README unchanged.
5. B1866 F4 (RELAYED): the README's ObjectDisposedException list is exact for the named members; async and byte forms
   route through them. `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` is tracked as BACKLOG.md
   owed item 2 (RELAYED from B1866); seen again here on both publishes of the three-way merge and once in each hosted
   publish leg of the head.

## Text points (records, not in the shipped behaviour)

- The new comment above NotOwnState says these types are "Never the receiver's or its spool's storage". SpoolJob.Gone
  IS a CancellationTokenSource held by the spool's job; it holds only cancellation callbacks, no secret text (the
  census probe lists it). The sentence means "not where the receiver keeps data"; a later edit could say so.
- kit B1872's 3-mutants.txt header says mReasonDisposed runs "under the answer to Q39"; the kit body says Q38 (seat
  deviation 5). Kit text only.
- The A03 flake's rate at HEAD2 varies by machine state: drafter 0 of 145, round-2 reader 12 of 40, seat 5 of 40, this
  reader 1 of 40. The forcing probe (red 3 of 3 at HEAD2 here, 8 to 11 faults of 300) is the instrument that does not
  depend on timing.

## Not decided (unchanged)

- Round 2's NOT DECIDED items: where the host reads the scan secret; who calls Sweep and WipeSession; whether a
  blocking stream is refused rather than bounded.
- Whether a later round adds the W02 body cell (kit B1872's 2-w02-body.diff is ready in its tools folder).
