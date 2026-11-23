# FOR RECORDS: OXPd 1.x read-only SOAP client (lane X1, kit B1976, seat X49), gate G1 round 1 of 2 of lane X1, reader B1980

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this lane and every choice inside it (kit B1976 Q1 = a in words at
its stamp S4; Q2 to Q6 the defaults), the landing hold (Q3: after L1 and the slnx round) and this gate's commission.
Nothing here says the product owner decided, ruled or approved anything about this lane (kit B1976's counts over his
rulings and CLARIFICATIONS: 0 rulings on the lane, RELAYED).

## State at this gate

- Verdict NO GO at `1fca08cf` on main `da8d64a8` (round 1 of 2 of lane X1): a fix round is owed. The lane is HELD from
  landing in any case until L1 lands and a slnx round adds the two project lines (kit Q3); landing.txt is marked HELD.
- Measured and holding at the head: the head = BASE + the two frozen patches + the 14 HP files + two restore-written lock
  files (tree `32057fba`); the 14 HP files = the jar's `META-INF/wsdls/` entries (14 of 14); red first 18 / 13 by
  assertion, green 18 / 0; 14 of 14 mutants (an independent run); whole solution 1809 / 0, RULES 583, Ran 111; hosted PASS
  on the head and on main; the pin refuses a null certificate and a chain-only match; only one certificate callback.

## From this gate (for the backlog; each owed by the fix round of lane X1 unless the coordinator moves it)

1. **Owed, Major (VERDICT FOUND 1): a nested answer of about 35 kB ends the host process with a stack overflow.** The
   recursive copy that masks an answer (`Oxpd1Soap.Mask`) has no depth bound; MEASURED at 5000 levels on a SOAP read and
   on the unauthenticated discovery-tree GET; the framework's own `.Value` on a fault code overflowed at 60,000 levels
   (420 kB). Only a pinned device can send it. Fix direction: bound the depth while reading, before the document is
   built; a cell and a mutant.
2. **Owed, Minor (FOUND 2): the returned answer can hold the admin password** when the device's echo is split by a CDATA
   section or the password is an element or attribute name (MEASURED; the record stays clean). Fix: scrub joined text
   runs; refuse a secret in a name.
3. **Owed, a decision for the coordinator before the first device connection (FOUND 3): the WS-Addressing namespace.**
   The client sends August 2004 headers with mustUnderstand; HP's committed descriptions use WS-Addressing 1.0
   (2005/08, and the 2006/05 WSDL binding) in every addressing element and the 2004/08 namespace in none (MEASURED
   counts). Device behaviour UNMEASURED; a device that does not understand the headers would fault every read.
4. **Owed, Minor (FOUND 4): an infinite time-out is accepted** and turns every bound off (MEASURED); zero, negative and
   very long values throw from the handler, not from the options.
5. **Info: the README could state** that a caller's cancellation throws `TaskCanceledException`, and that misuse (an
   undefined read, a call after Dispose, a throwing setting reader) throws (MEASURED; the seat's H18, H20); and that a
   setting value of spaces is sent (`IsNullOrEmpty`).
6. **Info: the stub shares the library's assumptions** on the path prefix and the WS-Addressing namespace, so the cells
   cannot test either (kit D2: the path is DERIVED for three of the four services; the bindings' own address is
   `http://localhost/Service`). The response and record element names were checked against the committed schemas
   (declared); their namespace qualification was NOT RUN (a hook refused the search; not worked around).
7. **Info: CodeQL on this lane.** The branch push runs no Analyze job; whether the default setup's C# build compiles
   projects outside the solution is UNMEASURED, so a csharp count of 0 before the slnx round could be vacuous.
8. **Info: words.py reads `x64` (in `linux-x64`, `win-x64` of restore-written lock files) as a seat id**: 4 hits in this
   lane's two lock files, 56 in BASE's 28. A known false shape of the tool, not a finding.
9. **Carried (RELAYED from kit B1976):** the files in `contracts/oxpd1/` stand on the COORDINATOR'S reading of C-56
   message 5 with leave to correct (C-56's own entry reads "exactly the files" of `contracts/oxpd2/inputs.sha256`,
   `CLARIFICATIONS.md:414`; `<project>/CLAUDE.md:86` names only that list as the exception for Source_Documents, and
   these 14 came from the SDK jar, not from Source_Documents, per the drafter); R32 open; owed later rounds: the two
   slnx lines, one shared pin helper or the duplicates named for good, a lab command that calls this client, R5's
   exemption list covers only `contracts/oxpd2/` (a tracked copy of a Source_Documents file would fail R5's hash half,
   which no hosted job runs).
10. **UNMEASURED:** every probe shape on Linux and Windows (the stack depth at which FOUND 1 bites differs by thread
    stack); TLS session resumption; any device answer.

## SCANS (of this folder's texts)

- `words.py` over `pr-title.txt` (175 bytes, under 256), `squash-subject.txt` (184 bytes) and `squash-body.txt`: every
  count 0, `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #33> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from the gate clone's
  `build/`, the head's copy, which equals main's: no `build/**` path in this diff): control `rc 1, found 2`, message
  `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks `dir` over this folder (seven files, before this SCANS section was filled): rc 0, `no leaks found`.
- Lines outside printable ASCII in this folder: 0 in every file but `pr-body.md` line 52 (the attribution line).
