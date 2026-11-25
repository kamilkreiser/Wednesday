The OXPd 1.x top-level button writes (first-run step 4), built and tested against stubs only, before any run against
a device. One commit, `1c7cdbbb`, on `main` `1ccf6d0c` (behind 0, ahead 1). Eleven files: two added, nine changed, all
under `src/Datasec.Suite.Adapters.Oxpd1/`, `src/Datasec.Suite.Lab/Commands/Oxpd1/` and the two matching test folders.
No package, no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/`.

## Why

- First-run step 4 needs a lab write for HP's UIConfiguration `RegisterTopLevelButton` and its undo
  (`UnregisterTopLevelButton`), with a dry run, a read of the button records before and an undo. HP's descriptions
  (committed under `contracts/oxpd1/hp/`) say a register whose id matches an existing record "overwrites the existing
  one", so an unregister sent as its undo would remove a button that was there before: the records are read first
  (`contracts/oxpd1/README.md`, "Read first: `GetTopLevelButtonRecords`").

## What changed

- **The client.** The closed write catalogue gains `RegisterTopLevelButton` and `UnregisterTopLevelButton` (two rows
  of the committed binding, HTTP Basic `admin`). `Oxpd1TopLevelButton` takes an id that is not empty, a title of 1 to
  100 characters (also its en-US description), a position of 1 to 65535 (HP's schema) and an absolute `https` target
  page with no user information and at most 256 characters; the record carries no icon, no credentials and no post
  body. A register's undo is the unregister of the same id. `ReadTopLevelButtonsAsync` makes
  `GetTopLevelButtonRecords` (admin) through the existing internal `SendAdminReadAsync` and answers only when the
  response, the result and every record (exactly one text-only `id` of HP's 8-4-4-4-12 form) are in HP's shape.
  `Holds` matches an id in any letter case. The read catalogue and its read-only rule are unchanged; `Oxpd1Client.cs`
  changes two comments only.
- **The lab.** `oxpd1 write --write RegisterTopLevelButton --button-id <uuid> --button-title <title> --button-target
  <https address> [--button-position <n>]` and `--write UnregisterTopLevelButton --button-id <uuid>`; any other
  combination is a usage error (exit 2) before any folder or connection. An executed register reads the records first:
  an id held in any letter case is exit 10 with nothing written and no undo; refused is exit 6; any other end, or a
  record it cannot read, is exit 8 with nothing written. An answered register or unregister reads the records after
  and prints whether the id is listed (the exit code does not change). The undo list's register line names
  `UnregisterTopLevelButton <id>`; `undo-owed` owes the unregister of a register until an answered unregister of the
  same id on the same host, and now matches every write only with a write of its own family (sign-in agent, Test
  service, CA store, top-level button), so an id typed for one family never clears or replaces what another owes.
- **Text.** Both READMEs: the three UIConfiguration rows, the record's rules, the records read's shape, the verb's
  options, order, exit codes and undo, the family rule of `undo-owed`, and the Limits.

## What proves it

- Red first: 27 cases fail by assertion on a permissive first shape (adapter `Total: 104, Failed: 14`; lab
  `Total: 297, Failed: 13`). Green: 2338 / 0 / 2334 / 4 locally; the branch's push run 45637707044: linux 2334
  succeeded, windows 2317 succeeded, rules 679 files, `Ran 117 tests`, secret scan clean.
- 17 mutants, each red on exactly its cells, none surviving (the position or the target unbounded; no undo for a
  register; the position left out of the body; an unreadable record skipped; an attribute or text taken in the
  records read; a loose id form; a case-sensitive match; the records read sent as `guest`; a held id ignored; no read
  before; no read after; an unregister taking a record; another write taking a button option; the register's undo not
  owed; the family dropped from `undo-owed`'s key).
- Against stubs on 127.0.0.1: a register of an id not on the device (read, register, read after: three requests,
  `admin` each); one already there in the same or another letter case (one request, nothing written); a records read
  refused, faulted or holding a record with no id (nothing written); a register that faults (owed) or is refused (not
  owed); an unregister; the ten option refusals (no folder, 0 connections); `undo-owed` across hosts, ids and
  families.

## Still open

- Nothing here has run against a device. What the M577 shows for a button with no icon, where it places it, how long
  after an answered register it shows, how it writes a record's id in its read, what it does when the target page
  cannot be reached, and its limit on buttons are not measured. The device run of step 4 is a separate step after
  this lands, and it needs the product owner's word first, because a test button goes on the device's home screen.
- Named limits: a device that writes a record's id in another form than 8-4-4-4-12 (braces, no hyphens) ends the
  read malformed and stops a register with nothing written; a button added by anyone else between the read before
  and the register is not seen; a fault's subcode is not read; a device that answers a register but does not list the
  button yet is reported, not acted on; the other UIConfiguration calls are not built; the press of the button, the
  device's call to the target page and the page itself are not built; the device run is not built here.
- Known, not changed here: the records reader takes a non-ASCII space beside the records or the result (HP's schema
  refuses it), and it reads a record's id without checking the record's other parts (a foreign element, text, or the
  id out of order), so a record outside HP's schema can still be read; the lab writes every id in lower case, so it
  cannot unregister a record the device holds in upper case (such an unregister answers with no effect, and the read
  after reports the id as listed); the writer's record type takes a title that XML cannot carry, and the request is
  then never built (the lab refuses such a title first); the write family of `undo-owed` puts any write kind without
  its own line in the button family (every one of today's eight kinds has its family).
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the order after the CA store writes;
the button records read as the writer's own, with the read catalogue unchanged; every record one id of HP's form or no
answer; an id already there in any letter case stopping the register; the read after reported only; no icon, no
credentials and no post body in the record; `undo-owed` matched within one family; the dry run's envelope printed
whole; no local CodeQL). No choice in this change is the product owner's. The run against a device needs the product
owner's word first.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
