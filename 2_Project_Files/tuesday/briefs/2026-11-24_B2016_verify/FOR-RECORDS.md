# FOR RECORDS: lane W2 (kit B2011, seat X59), the lab wiring of lane W1's writes and the end-of-session undo list, head 67c24d18 (gate B2016)

For the records lane only; nothing here is written into a project file by the gate. Who decided every choice of this
lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY: CLARIFICATIONS.md counts 0 on
every subject of the lane, RELAYED from the drafter; S4's answers are the defaults, Q1 "a" and Q2 "a" in words, each the
coordinator's).

## From the kit's FOR RECORDS (RELAYED, copied)
- The lab tool gained its first device-WRITE verb: `oxpd1 write`, ONE write of the OXPd 1.x writer per run (register or
  unregister a test sign-in agent, first-run step 5), a dry run unless `--execute`; an executed register reads the
  device's agent records first and refuses an id already there (gate B2008 FOUND 2's read-first); the run stops at the
  first refused password with the read's own words; every executed write is entered in the run folder's `undo-list.tsv`
  before it is sent and its end after; the undo is printed. Neither verb has run against a device.
- `oxpd1 undo-owed <session folder>`: the end-of-session check of the design review's F19 for step 5's pair, print-only
  (it sends nothing); a register stays owed until an unregister of the same id on the same host has answered after it.
- The lab refuses an address holding `@` and a name holding a control character (gate B2008 FOUND 1 and 3) for its own
  callers; the adapter's own record rules are unchanged (still owed to lane W1's round 2).
- Named limits: steps 2 to 4 and the rest of F19's list are not built (H24); nothing compares the undo list with the
  device (H17's neighbour, README); the read and the register are two requests, not atomic (H17); a write failure after
  the run folder is made is not caught (H20); a run folder outside the session folder is not counted (H21); the
  named-pipe credentials file and the blank-looking password are inherited (H23).
- Exit codes: `write` 10 when the id (or an unreadable id) is already on the device; `undo-owed` 11 when an undo is owed
  or a line cannot be read.

## Changed or sharpened by the gate's measurements (MEASURED, gate probe, macOS arm64, .NET 10.0.404, stub on 127.0.0.1)
- **Read before a register, 19 shapes:** 401 and 403 exit 6 (the lockout words), a 500 fault, a 404, a time-out, a
  dropped connection and malformed XML exit 8, the same id upper case, in braces, without hyphens or padded, an
  unreadable id text, an empty id element and an id given only as an attribute exit 10: each ONE request, one
  password-bearing, no write, no undo list. A device holding another agent only, or none: the write is sent (exit 0).
- **The fail-closed edge (FOUND 2):** a same-id record in another namespace, wrapped one level deeper, or unqualified is
  NOT seen and the register IS sent (exit 0). HP's committed schema (qualified, records directly under the result) is the
  shape the code reads; a device answering otherwise is UNMEASURED.
- **`undo-owed` "nothing is owed" with nothing read (FOUND 1):** the run folder itself given as the session, a folder one
  level above the session, an empty or header-only `undo-list.tsv`: exit 0, `nothing is owed`. Equal recorded times are
  ordered by folder name (one order clears, the other owes). A list truncated mid-line is named unreadable (exit 11),
  except a cut inside its last column (the undo text, not read), which is still counted.
- **An unregister of an id the device does not hold:** the stub's empty answer is `Answered`/`Yes`, exit 0, ONE request,
  no read (it clears that register in `undo-owed`); a fault is `Fault`/`Unknown`, exit 8 (clears nothing).
- **Names XML refuses (FOUND 3):** U+FFFE, U+FFFF and a lone surrogate pass the lab's check; the envelope writer throws
  (dry run: after the run folder is made, no summary; executed register: after the read, with a `Pending` row for a
  write never sent). U+0001, U+007F and U+0085 are refused (exit 2) before any folder or connection.
- **The printed undo (FOUND 4):** it carries the host, the pins and `--soap-port`, not `--addressing`, `--password-name` or
  `--timeout-seconds`.
- **The password:** a record name and a fault code holding the password, a refused read and a refused write: the password
  in no output and no file of the run folder (`summary.txt`, `undo-list.tsv`, `oxpd1-client.log`).

## Gate findings to carry (VERDICT.md FOUND; one Major, three Minor, five Info; none sends a byte or prints a value)
- FOUND 1 (Major): `undo-owed` says `nothing is owed` (exit 0) when it read no list. Round 2: no "nothing is owed" unless
  at least one list was read, an empty or header-only list is unreadable, and the given folder's own list is read or
  refused.
- FOUND 2 (Minor): the read before a register sees only schema-shaped records; any other child of the result should fail
  closed.
- FOUND 3 (Minor): the name check is narrower than XML's character rule (U+FFFE, U+FFFF, lone surrogates).
- FOUND 4 (Minor): the printed undo drops `--addressing`, `--password-name` and `--timeout-seconds`.
- FOUND 5 (Info): no cell for a register on a device that holds another agent (the probe measured it correct).
- FOUND 6 (Info): ties and the recorded clock (README states "by their time" only).
- FOUND 7 (Info): cancellation or an exception after the send prints no undo (the list keeps `Pending`, owed).
- FOUND 8 (Info): "nothing is retried" holds for the lab and the client's preemptive Basic header; .NET's own re-send of a
  request on a failed pooled connection is UNMEASURED.
- FOUND 9 (Info): the host is compared as typed (a name and its IP, or two cases, stay owed: the safe side).

## For the lanes after this one (RELAYED from the kit's FOR TUESDAY)
- A first real run commission (after the product owner's two morning actions); W1's round 2 (gate B2008 FOUND 1 and 3 in
  the adapter itself); LH's round 2 (gate B2009 FOUND 1, the pipe); steps 2 to 4 after a contracts lane (kit B2012's
  report). This lane's round 2: FOUND 1 to 4 above.
