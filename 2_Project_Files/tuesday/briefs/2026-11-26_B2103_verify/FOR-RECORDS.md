# FOR RECORDS: the row-4 write lane round 1 of 2 (kit B2100, seat X75), the OXPd 1.x top-level button writes, head 1c7cdbbb (gate B2103: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2100 THE AUTHORITY: `CLARIFICATIONS.md` counts `RegisterTopLevelButton` 0,
`UnregisterTopLevelButton` 0, `GetTopLevelButtonRecords` 0, `UIConfiguration` 0, `top-level button` 0, RELAYED; stamp
S4 states Q1, Q2 and Q7 "a" in words as Tuesday's, the rest the defaults). The DEVICE run of row 4 is the product
owner's to allow (below).

## What the lane gives (RELAYED from the kit's FOR RECORDS, CHECKED by the gate at 1c7cdbbb where marked)
- The OXPd 1.x client registers a top-level (home screen) button record on a device and unregisters it (HP's
  `RegisterTopLevelButton` and `UnregisterTopLevelButton`, admin), each a dry run unless executed; the record is an
  id, a title of 1 to 100 characters, a position of 1 to 65535 and an absolute https target page of at most 256
  characters, with no icon, no credentials and no post body (CHECKED: the register body's elements are exactly id,
  title, description, requestedPosition, browserTarget/webApplication/uri and binding; a target whose absolute form is
  256 characters taken, 257 refused; position 0 and 65536 refused; every taken body 0 schema errors against HP's
  committed schema); a register's undo is the unregister of the same id. It reads the button records
  (`GetTopLevelButtonRecords`, admin; CHECKED: `admin` on all 29 probe reads whose header the gate recorded, never `guest`) through the writer only,
  answered only when every record holds one id of HP's UUID form; the read catalogue is unchanged.
- The lab's `oxpd1 write --write RegisterTopLevelButton|UnregisterTopLevelButton --button-id <uuid> [--button-title
  --button-target [--button-position]]`: an executed register reads the records first and writes nothing (exit 10)
  when a record holds the id in any letter case (CHECKED both ways: held lower and typed upper, held upper and typed
  lower); an answered register or unregister reads the records after and says whether the id is listed; `undo-owed`
  owes the unregister of a register, and now matches every write only within its own family (sign-in agent, Test
  service, CA store, top-level button).
- Named limits: not run against a device; what the M577 shows for a button with no icon, where it places it, how long
  after an answered register it shows, how it writes an id, what it does when the target page cannot be reached, and
  its button limit are UNMEASURED; a fault's subcode is not read; a button added between the read and the register is
  not seen; a device that writes an id with braces or no hyphens stops every register at exit 8 with nothing written.

## Gate B2096 FOUND 1: CLOSED by D7 at this head (if this head lands)
- Gate B2096 FOUND 1 (`undo-owed` keyed a write by host and id without its kind) is fixed here: the key is (host,
  family, id), `LabFiles.cs:397`, with `Family` at `:414`. MEASURED by this gate through the real `oxpd1 undo-owed`
  (`fleet/state/s328/g2103/logs/probe-owed.tsv`): an owed import then an answered agent unregister of the certificate's
  id: still owed, exit 11 (B2096's E2, now closed); an owed import then an answered agent register of that id: BOTH
  owed (B2096's E4, now closed); an owed button register then an answered certificate remove of its id: still owed
  (B2096's E3 class, now closed for the button family too). Within one family the landed behaviour is unchanged
  (import then remove, agent register then unregister, enable then disable: "nothing is owed"; and every landed cell
  of `Oxpd1WriteTests`, `Oxpd1TestServiceTests` and `Oxpd1CaStoreTests` green in the gate's runs: the whole solution
  `total: 2338`, `failed: 0`, and the Lab test executable whole `Total: 301, Failed: 0` with the gate's probes). The records pass may mark B2096 FOUND 1's proposed owed item closed by this
  lane's squash, naming the squash commit.
- Gate B2096 FOUND 2 to 7 are NOT taken here (Q10's default); they stay as that gate's FOR-RECORDS.md proposed them.
  FOUND 4's class (`OnlyElements`, .NET white space) now also sits in the button records reader (this gate's FOUND 2):
  one fix for the three readers when next touched.

## The later device run of row 4 (NOT built; a SEPARATE kit after this lands; its word)
- **It needs the product owner's word first.** His option's detail of 2026-11-24 for the home-screen switch reads "We
  ask again before any home-screen app is added." (`CLARIFICATIONS.md:1088`, RELAYED from the kit), and the
  coordinator's own record of row 4 says its button goes on the home screen only after his word
  (`CLARIFICATIONS.md:1192`, RELAYED). The kit's drafter and the readiness note read a test button as on the home
  screen; the card is asked of him only when the run is near, never before. The readiness note's suggested card:
  "may a test button go on the M577's home screen, and will you press it?" (B2089, RELAYED).
- **Its shape** (DERIVED by the kit, for that kit to settle; RELAYED): on the M577 (`--addressing 2004`, as every M577
  run): (1) `oxpd1 write ... --write RegisterTopLevelButton --button-id <a NEW UUID, lower case> --button-title
  <a title> --button-target <a page>` as a dry run, then executed (the read before, the register, the read after);
  (2) the read after lists the id or not (a device that lists it late is a line, not a failure: HP warns a register
  "may return before the new button ... has become manifest"); (3) a PRESS on the panel is a physical act no agent can
  make, and the target page must be reachable from the printer's network (owed item 118: the route from 192.168.8 to
  this Mac is UNMEASURED); without a served page the press tests nothing of the callback; (4) the unregister, always,
  when the register may have taken effect (`undo owed`), then `oxpd1 undo-owed` on the session: "nothing is owed";
  (5) never a reset, a disk init or a firmware step (`CLARIFICATIONS.md:734`; HP clears button records only "by a disk
  init or restore factory settings").
- **Add from this gate:** (a) read the read-before line FIRST: if the M577 writes a record's id with braces, without
  hyphens, with white space around it, or carries `xml:lang` or another attribute on a record (all MEASURED
  `MalformedAnswer` here), the register stops at exit 8 with nothing written, and that line is the answer to record,
  not a pass or a fail of the button; (b) note how the M577 writes ids (case) in that read: the lab writes and sends
  every id in lower case, so it cannot unregister a record the device holds in upper case (gate FOUND 5); (c) a
  register is refused at exit 10 when the device holds the id in ANY case, so a fresh UUID per run is the form;
  (d) the run folder's `oxpd1-client.log` will hold the device's button records (other solutions' titles and target
  addresses, if any are installed): keep the run folder outside any shared or synced place, as any run folder.
- **The home-screen switch** (OXPD2-62, due 2026-12-08; `CLARIFICATIONS.md:1112`, RELAYED from the kit) is open beside
  the device run, not this lane.

## Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate)
- **NEW owed item proposed: `Family`'s default arm** (gate FOUND 1, Minor): `LabFiles.cs:419` `_ => "button"` puts
  any write kind without its own arm in the button family; today the eight kinds map to four families exactly
  (MEASURED), and `Parse` refuses a kind that is not one of the eight names, so nothing reaches it today. Fix when
  the next write kind is added: name the two button kinds in their own arm and make the default throw, with a cell
  that maps every `Oxpd1WriteKind` value to its family.
- **Gate B2096 FOUND 4's proposal widened** (this gate's FOUND 2, Minor): the button records reader takes a no-break
  space beside the records or beside the result (HP's schema refuses both); one fix of `OnlyElements` for the store
  reader, the button reader and B2070 FOUND 1's reader.

## Still open after this lane (none built; the coordinator's choices)
- The device run of first-run row 4 (above), after the product owner's word. The other UIConfiguration calls, the
  press, the device's call to the target page and the page itself are not built.
- The device run of first-run row 3 (owed item 103), as gate B2096's FOR-RECORDS.md routed it.

## Added by the gate (MEASURED; see VERDICT.md)
- FOUND 1 Minor: `Family`'s default arm puts any unnamed write kind in the button family (today exact for all eight).
- FOUND 2 Minor: the button records reader answers with a no-break space beside the records or the result (HP's
  schema refuses it; every record is still read whole).
- FOUND 3 Info: the button records reader does not check a record's parts beside its id (a foreign element after the
  id, text inside a record, the id after the other parts, a record of id alone: each read, each schema-refused); the
  id is still read whole, so the register's decision stands.
- FOUND 4 Info: the writer's `Oxpd1TopLevelButton` takes a title XML cannot carry (U+FFFE, U+0001, a lone surrogate)
  and a tab or line feed; building the request then throws `ArgumentException` before any connection (the lab refuses
  every one of them at the command line first).
- FOUND 5 Info: the lab writes and sends every id in lower case, so an unregister cannot remove a record the device
  holds in upper case; it answers with no effect and the read after reports the id as listed.
- FOUND 6 Info: the records reader refuses `xml:lang` on a record (schema-valid): the safe side; a device-run stopper
  only if the M577 writes it.
- FOUND 7 Info: a target with a non-ASCII host is written in its Unicode form (`AbsoluteUri`; MEASURED through the
  writer, DERIVED for the lab, whose `Address` makes the same `Uri`), schema-valid; what the M577 does with it is
  UNMEASURED.
