# FOR RECORDS: lane OX-B kit 2, round 1 of 2 (kit B2128, seat X79), the lab tool oxpd1 (Oxpd1Command.cs, Oxpd1EchoVerb.cs and the Lab README), head 0ae90664 (gate B2130: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2128 THE AUTHORITY; owed items 135 and 136 name "the coordinator's choice" in the owed list's own
words, 106 and 107 a reviewer's proposal, 109 "a README line or an ASCII rule", 110 "a README line", RELAYED; stamp S4
states Q1 and Q3 "a" in words as Tuesday's, Q2 and Q4 to Q10 the defaults; ANSWER-1 (a) accepted one words.py hit, the
README's XML term "processing instruction"). Nothing here ran against a device.

## What the lane gives (RELAYED from the kit's FOR RECORDS, CHECKED by the gate at 0ae90664 where marked)
- **Owed item 106 closed** by the reviewer's proposal, widened to the record: an executed register writes nothing
  (exit 10) when the agent read's result or a record carries an attribute that is not a namespace declaration or text
  that is not XML white space, or a record holds a second element named `id` at any depth (`Oxpd1Command.cs:1053`,
  `:1060`, `:1085`, `:1092`; the line `:1020`). CHECKED: V17 rows 1 to 9 red on BASE by assertion and green at the head
  (the gate's runs); rows 10 to 12 taken on both; `mResultAttribute`, `mResultText`, `mRecordIds`, `mRecordNodes` each
  redden their rows and nothing else (the gate's run). The shapes the client never hands the lab (a comment, a
  processing instruction, anything beside the result) and the id as the text of a record's other elements are named in
  the README's Limits (`README.md:312` to `:314`). **The gate adds one shape the README does not name: a second `id`
  inside an element whose name the client's logging mask covers (HP's own `authenticationAgent/networkCredentials`, or
  any name holding a deny-list stem such as `secret`, `token`, `body`) is replaced by the mask before the lab reads it,
  so the register is written (MEASURED: gate FOUND 1).**
- **Owed items 107 and 109 closed** by one rule, the coordinator's choice and stricter than HP's `anyURI`: the three
  address options take printable ASCII only (`Oxpd1Command.cs:777`; error lines `:536`, `:555`; a host that is not ASCII
  in its `xn--` form). CHECKED: V18 rows 1 to 7 and 10 red on BASE (rows 1 and 2 by the writer's exception) and green at
  the head; `mAddressAscii` reddens all eight; the gate's extra mutants show both ends of the range pinned (U+0020 and
  U+00FF). 436 probe runs of every printable character in host, path and query of two options and 33 named shapes: no
  exception, no folder on a refusal, no connection (`g2130/logs/probe.tsv` G2).
- **Owed item 110 closed** by a README line and a pinning cell: the bound of 100 counts UTF-16 code units, as the
  client's record does (`README.md:80` to `:84`; V19 green on BASE and head). CHECKED: 100 units of each kind taken and
  101 or 102 refused (probe G5).
- **Owed item 135 closed** by its first option: the parser refuses a callback host whose callback address with port
  65535 would be over 256 characters (exit 2; `Oxpd1EchoVerb.cs:230`, the shared builder `:258`, used by the run at
  `:366`). CHECKED: E09 rows 232 and 200 and E10 red on BASE, green at the head; `mCallbackLength`, `mCallbackBound` and
  the gate's `xCallbackPort`, `xCallbackNoDigits` each redden E09 (and E10 for the first). No host the parser takes made
  the client's `Oxpd1EchoCall.Async` throw at ports 1, 80, 443, 8080 or 65535 (probe G3).
- **Owed item 136 closed** by its first option: a delay at least the callback wait (async) or the time-out (sync) is a
  usage error (`Oxpd1EchoVerb.cs:239`, `:246`). CHECKED: E11 six rows red on BASE, all eight green at the head; four
  mutants; twenty extra delay lines, every taken delay shorter than its wait or time-out (probe G4).
- Candidates for the adapter lane (not this lane's): the client could refuse an agent read whose response holds anything
  beside the result, a comment or a processing instruction, if a later round wants the lab to see them (H6); **and the
  mask's covered elements (FOUND 1).**
- Owed 152 and 153 (`LabFiles.cs`) stay for a later round of the lab tool (serial on the README).
- Nothing here ran against a device.

## What stays owed or becomes a candidate
- **H6** (adapter side): a comment, a processing instruction and anything beside the result are dropped by the client
  (MEASURED for the processing instruction by the gate: taken, register written, probe G1). Candidate owed item for the
  adapter lane, now with FOUND 1's masked element in the same class.
- **H9**: the device host (first word) and `--callback-host` stay outside the ASCII rule. MEASURED by the gate:
  `Uri.CheckHostName` takes as Dns a callback host holding U+00FC, U+00DF, U+0130, U+200B (zero-width space), an emoji,
  U+FFFD, U+FF0E, U+3002 and an invalid `xn--a` label; each is taken by the parser and written into the callback address
  as typed (Unicode, not its `xn--` form). A callback host holding a lone surrogate (`a\uD800b.example`) is taken by
  `CheckHostName` and now throws `UriFormatException` out of the parser (before any folder; at BASE the same host threw
  after the run folder was made): gate FOUND 2. The device host was NOT probed (UNMEASURED).
- **H14**: the write section's `IsServiceEnabled` sentence (README `:109` to `:113` at the head, `:103` to `:107` at BASE, printed by sed; the seat's STATUS said `:111` to `:115`)
  unchanged (owed 154).
- **152, 153** (`LabFiles.cs`): stay owed.

## Proposed owed items from this gate (graded in VERDICT.md; none blocks this landing)
1. **(FOUND 1, Minor)** The read before a register does not see a second `id` inside a record element the client's
   logging mask covers (any local name holding a deny-list stem: `networkCredentials` in HP's own record shape,
   `password`, `secret`, `token`, `body`, ...): the register is written. Fix: a README Limits clause now (the README's
   "a record holds a second element named `id` (in any namespace, at any depth)" reads wider than the code), and/or in
   the adapter lane a read that reports a masked element holding an element child.
2. **(FOUND 2, Minor)** `--callback-host` with a lone surrogate throws `UriFormatException` out of
   `Oxpd1EchoOptions.Parse` (unhandled; no folder). Fix: the address options' printable-ASCII rule (or `XmlConvert`'s
   character test) on `--callback-host` and the device host (closes H9 too), or catch the builder's exception as a usage
   error. A cell: E09-family row "a callback host holding a lone surrogate" -> exit 2, nothing thrown.
3. **(FOUND 3, Info)** The XML white-space test of C1 (space, tab, CR, LF only) is pinned by no cell: the gate's mutant
   `xXmlSpaceLoose` (`char.IsWhiteSpace`) reddens nothing, though it would take a result or record holding only a
   no-break space (MEASURED refused at the head, probe G1). A cell row "a no-break space as text of the result".
