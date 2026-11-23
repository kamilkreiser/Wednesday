# FOR RECORDS: lane W2 round 2 (kit B2021, seat X61), the fix build of the lab's `oxpd1 undo-owed` and `oxpd1 write`, head 28b25332 (gate B2026)

For the records lane only; nothing here is written into a project file by the gate. Who decided every choice of this
lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY: CLARIFICATIONS.md counts 0 on
every subject of the lane, RELAYED from the drafter and the seat's whole read of C-1 to C-79; S4's answers are the
defaults, Q1 "a" and Q2 "a" in words, each the coordinator's).

## From the kit's FOR RECORDS (RELAYED, copied)
- Lane W2's fix build closes gate B2016 FOUND 1 to 4 in the lab: `oxpd1 undo-owed` says `nothing is owed` (exit 0) only
  after reading at least one list with an entry line in every list and every line read; with no list read it prints `no
  undo list was read` and ends with exit 11; a list with no entry line is named unreadable; a folder that holds
  `undo-list.tsv` itself is refused before anything is read (exit 2). An executed register writes nothing (exit 10) when
  the read's result holds any element that is not a schema record or a record without exactly one id. An agent name XML
  cannot carry is a usage error (exit 2) before any folder or connection. The printed undo carries `--password-name`,
  the pins, `--soap-port`, `--addressing` and `--timeout-seconds`.
- Gate B2016 Info 5 has its cell (a device holding another agent only is written to); Infos 6, 7, 8 and 9 are README
  text (the recorded clock and ties; no undo printed after an exception or cancellation once sent, the `Pending` row
  stays owed; .NET's own re-send on a pooled connection UNMEASURED; the host compared as typed).
- Named limits: content outside the result element is not read (H9); a character XML cannot carry in `--agent-service`
  or `--prompt-page` UNMEASURED (H12: now MEASURED, below); the `undo-owed` hint line carries the host and id only (H15).
- The lab's write has still not run against a device; Tuesday's hold on `oxpd1 write --execute` lifts by Tuesday, after
  the landing.

## Changed or sharpened by the gate's measurements (MEASURED, gate probe of 74 cases, macOS arm64, .NET 10.0.404, stub on 127.0.0.1)
- **`undo-owed`, 30 folder and list shapes.** Never `nothing is owed` and never exit 0 when no entry was read: the run
  folder given (exit 2), also through a symbolic link to it (exit 2); the session one level below, a dangling link only,
  a list file that is a folder, only `undo-list.tsv.new`, a run folder closed by permission and alone (exit 11, `no undo
  list was read`); an empty list, a header-only list (also with a byte order mark), blank lines only, a list closed by
  permission, a list that is a dangling link (exit 11, named unreadable). Symbolic links to run folders, to the session
  and to a list ARE followed and read. A header-only or closed list BESIDE a clean pair is still exit 11.
- **The one silent pass left:** a run folder the command cannot open (mode 000) beside readable lists that are clean is
  counted as a folder without a list: exit 0, `nothing is owed`, `2 executed writes in 2 run folders`. A session folder
  it cannot list ends in an unhandled `UnauthorizedAccessException` (no `nothing is owed`).
- **The read before a register, 23 answer shapes.** Exit 10, one request, no write, no list: the same id (also
  pretty-printed, in parentheses, inside a child element of `id`, after 300 other records); an id with a `urn:uuid:`
  prefix or a comment only (unreadable). Exit 8: two result elements. The register IS sent (exit 0, one read, one write)
  when the same id sits only in: an attribute of the result; text or CDATA of the result (the records as a string); a
  comment or a processing instruction; text beside another agent's record; inside another agent's record as an `id` of
  another namespace, an unqualified `id`, another element (`agentId`) or an attribute of its `id`; a record beside the
  result inside the response; and for a result marked `xsi:nil`. HP's committed schema is element-only (no wildcard, not
  mixed), so a conforming device answers none of these; how the M577 answers is UNMEASURED.
- **Characters XML cannot carry.** The agent name: each of the 65536 single code units between two letters: 63421
  accepted, 2115 refused, 0 accepted that the XML writer refuses (36 refused that it would take: the control
  characters); a reversed pair, a lone half at either end: refused; 50 pairs (100 code units) accepted, 51 refused (the
  length rule counts code units). The two addresses, each of the 65536 code units in the path, the query and the
  fragment: all but `@` accepted and written percent-encoded (ASCII only; U+FFFE as `%EF%BF%BE`, a lone surrogate as
  `%EF%BF%BD`); in the HOST: 63395 accepted, 63317 of them written as typed (not ASCII), and ONE, U+FFFF, accepted and
  then refused by the envelope writer (a dry run throws after the run folder is made; an executed register throws after
  its read, leaving a `Pending` row for a write never sent).
- **The printed undo, run as printed** (placeholders filled; two pins, `--addressing 2004`, another password name, 7 s,
  and again with every default): exit 0, one request, the register's addressing namespace, the password under the same
  name, the stub's agent removed; `undo-owed` over the two run folders then prints `nothing is owed`, exit 0.

## Gate findings to carry (VERDICT.md FOUND; no Blocker, no Major, three Minor, three Info; none sends a byte or prints a value outside the stub)
- FOUND 1 (Minor): the read before a register reads child elements only: text, CDATA, comments, processing instructions
  and attributes of the result, a second `id` (of another namespace, or unqualified) or another element inside a record,
  and anything beside the result are not read, and the register is sent. The README's "an answer the run cannot read
  whole may hold that id" is wider than the code. Ticket: refuse (exit 10) a result with any non-whitespace text or any
  attribute but a namespace declaration, and a record with any child of the local name `id` beyond its one own; a README
  Limits line until then; a cell per shape.
- FOUND 2 (Minor): U+FFFF in the host of `--agent-service` or `--prompt-page` reaches the envelope writer (kit H12).
  Ticket: the name's `XmlText` check on each address's `AbsoluteUri`.
- FOUND 3 (Minor): a run folder that cannot be opened is counted as a folder without a list (`undo-owed` can print
  `nothing is owed` past it); a session folder that cannot be listed ends in an unhandled exception. Ticket: name the
  first unreadable (exit 11); catch the second as exit 11.
- FOUND 4 (Info): a non-ASCII host is written as typed and a lone surrogate in a path, query or fragment becomes U+FFFD
  percent-encoded: what the device is given is not always what was typed.
- FOUND 5 (Info): the name's length rule counts UTF-16 code units (51 emoji refused, 50 taken).
- FOUND 6 (Info): the probe's `undo-owed` shapes beyond the six of cell U05 have no cell (symbolic links, permission, a
  list that is a folder, a byte order mark, blank lines); each measured correct but for FOUND 3's.

## For the lanes after this one
- The hold on `oxpd1 write --execute`: the coordinator's. This gate's reading: gate B2016's FOUND 1 is closed; its FOUND 2
  is closed for every child element of the result; what is left of it (FOUND 1 above) can be carried by the first real
  run's own commission as one step before any executed register: an `oxpd1 read --read GetAuthenticationAgentRecords`
  run whose printed answer is looked at (records as elements directly inside the result, nothing else in it).
- RELAYED from the kit's FOR TUESDAY: a first real run commission (after the product owner's two morning actions); W1's
  round 2 (gate B2008 FOUND 1 and 3 in the adapter itself); LH's round 2 (gate B2009 FOUND 1, the pipe); steps 2 to 4
  writes on the contracts pull request 43 landed.
