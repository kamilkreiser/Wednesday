# FOR RECORDS: lane OX-B kit 1, round 1 of 2 (kit B2122, seat X78), the lab tool oxpd1 (LabFiles.cs and the Lab README), head cd2a3e13 (gate B2123: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2122 THE AUTHORITY; owed items 142 and 127 name "the coordinator's choice" in the owed list's own
words, 108 and 145 a reviewer's proposal, RELAYED; stamp S4 states Q1 and Q2 "a" in words as Tuesday's, Q3 to Q10 the
defaults). Nothing here ran against a device.

## What the lane gives (RELAYED from the kit's FOR RECORDS, CHECKED by the gate at cd2a3e13 where marked)
- Owed item 108 closed by the reviewer's proposal: `undo-owed` names a run folder whose entries cannot be listed as
  unreadable (`LabFiles.cs:411` to `:416`) and catches a session folder it cannot list (`:397` to `:404`), each exit 11,
  never `nothing is owed`; the verb's `none` (`:552`) is true only when nothing is unreadable either. CHECKED: U06's
  three rows red on BASE by assertion and green at the head (the gate's runs); modes 0000, 0100, 0300 on a run folder,
  a run folder that is a link to a mode-000 folder, and session modes 0100, 0300, 0400 each end exit 11 naming the
  folder (`g2123/logs/probe.tsv`). **A run folder that can be listed but not entered stays a named limit (H9), and the
  gate MEASURED its harm: modes 0400 and 0600 on a run folder holding an owed register, beside two clean lists, print
  `nothing is owed` and end 0 (gate FOUND 1).**
- Owed item 111 closed by cell U07 (six shapes pinned at BASE's behaviour; the permission shape is U06's). CHECKED: U07's
  six rows green on BASE plus the new cells (the gate's red run: the six reds are U06, U08, U09 and S16 only) and at the
  head. Row 6 (an undo list that is a dangling link) is re-pinned to BASE's MEASURED words
  `unreadable: r1/undo-list.tsv (FileNotFoundException)` under the kit's D8 (the seat's DEVIATION 2; the gate grades it
  the safe side and a better message: VERDICT.md, Tuesday's point a).
- Owed item 145 closed by the reviewer's proposal: the button kinds have their own arm (`:490`), the default throws
  `ArgumentOutOfRangeException` (`:491`), and U08 maps every write kind (and asserts exactly 8 kinds, so a ninth kind
  added later reddens it). CHECKED: `mFamilyDefault` reddens U08 row 2.
- Owed item 142 closed by its first option: the certificate file is read through ONE stream bounded at 64 KiB and one
  byte (`:272` to `:295`); a link is followed and bounded. CHECKED: a link chain of three, a hard link, `/dev/zero`, a
  link to it, a sparse file of 10 GiB and a pipe with an endless writer are each refused at once; a pipe with no writer
  blocks the run (MEASURED by the gate; the README's Limits clause says UNMEASURED and can now say MEASURED).
- Owed item 127 closed by its first option: `RealPath` (`:122` to `:163`) resolves one part at a time from a resolved
  prefix, each link by its own text (`LinkText`, `:172`). CHECKED: eighteen link shapes (`probe.tsv` G01: a relative
  link through another, an absolute link inside a relative one, `..` past the root, `.` and `//` in a text, a trailing
  slash, chains of 30 and 39 links, an absolute text with `..` through a link, the S16 shape) are refused inside a work
  tree and made where the system makes them outside one; loops (self, two links, three with a `..`) and chains of 41
  and 45 links end in 0 ms and the system refuses the folder (exit 5, nothing made).
- Owed item 150 closed: the Lab README's callback sentence names the sync echo's reader (`CallbackMessage`,
  `Oxpd1Echo.cs:215`) and the 400 answer (`Oxpd1EchoVerb.cs:518` to `:524`); the whole "Known, not changed here" bullet
  is removed (count 0 at the head, 1 at BASE; its first half by 127). CHECKED against the code at main.
- Kit 2 of lane OX-B (owed 110, 109, 107, 106, 135, 136) is still to be drafted.
- Nothing here ran against a device.

## Which owed items this squash closes, and which stay owed (the records seat reads and decides)
- **Close on this squash:** 108, 111, 145, 142, 127, 150.
- **Stay owed (kit 2 of lane OX-B):** 110, 109, 107, 106 (`Oxpd1Command.cs`), 135, 136 (`Oxpd1EchoVerb.cs`).
- **Candidates the kit left to Tuesday (NOT DECIDED BY THIS KIT, item 2), none filed by the gate:** H9 (a run folder
  readable but not searchable: now MEASURED as a false `nothing is owed`, gate FOUND 1: the gate proposes it be filed);
  H12 (the write section's `IsServiceEnabled` sentence, README `:103` to `:107` at BASE: true, not complete; a records
  note or a kit-2 line).

## Owed items, proposed for the records pass (none is ticked by the gate)
- **NEW owed item proposed (gate FOUND 1, Minor): `undo-owed` says `nothing is owed` and ends 0 beside a run folder it
  can list but not enter.** A run folder of mode 0400 or 0600 (read, no search permission) holding an executed
  register, beside two clean lists: `undo list: 2 executed writes in 2 run folders`, `nothing is owed`, exit 0
  (MEASURED, `g2123/logs/probe.tsv` G03). The listing succeeds, so C1's catch is not reached, and `File.Exists` of
  its list is false without search permission (`LabFiles.cs:421`), so the folder counts as one without a list. The
  README's sentence "It says `nothing is owed` only when it read at least one list, every list holds an entry line,
  every line was read" (README `:186` to `:187`) reads wider than this. Fix (the kit's Q3 alternative): when the
  folder's listing names `undo-list.tsv` but the list cannot be found or read, name it unreadable; or name the shape
  in the README Limits. The lab never makes such a folder itself (its folders get the system's default mode).
- **NEW owed item proposed (gate FOUND 2, Minor): the 40-link bound of the run folder rule is pinned by no cell.** The
  gate's mutant removing `links++;` (`LabFiles.cs:146`) survives every cell (`Total 314 Failed 0`); without the bound a
  link loop on the run folder's path would never end (DERIVED: each link puts its text's parts back in front of the
  walk). The code is right (MEASURED: three loop shapes end in 0 ms and the system refuses the folder). Fix: one
  S16-family row "a link loop on the run folder's path" (ends, exit 5, nothing made) in a later round.
- **Info, for the records:** a named pipe with no writer as the undo list blocks `undo-owed` (MEASURED: 5 s blocked,
  then exit 11 once a writer opened and closed it); not named in the README's `undo-owed` section (the credentials and
  certificate pipes are named). The read loop of the bounded certificate read is pinned by no cell (a regular file
  returns whole in one read; a pipe writing in 100-byte pieces is read whole through the loop: MEASURED); a cell
  cannot make a pipe without starting a program (the kit's H8).
- **Info:** entries of the session that are not folders (a dangling link, a link to itself) and an empty folder are
  passed silently (`nothing is owed` beside two clean lists, MEASURED); a run folder whose link target was moved away
  is one of these.
