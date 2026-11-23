The second build of the lab tool's `oxpd1 write` and `oxpd1 undo-owed`: four corrections to what pull request 44 landed.
One commit, `28b25332`, on `b0b26b60` (main; ahead 1, behind 0). Five files change and none is added, all under
`src/Datasec.Suite.Lab/Commands/Oxpd1/` or `tests/Datasec.Suite.Lab.Tests/Oxpd1/` (`Oxpd1Command.cs`, `LabFiles.cs`, the
`oxpd1` README, the tests' `Oxpd1Stub.cs` and `Oxpd1WriteTests.cs`). No package, no `.csproj`, no lock file, no
`Datasec.Suite.slnx` line, no workflow, no `Directory.*` file, no path of the OXPd 1.x client or its tests, no
`contracts/` path.

## Why

The independent read of pull request 44 measured four places where the two verbs did less than their README said:

- `undo-owed` printed `nothing is owed` (exit 0) when it had read no list at all: the run folder given in place of the
  session, a folder one level above the session, an empty list, a list holding only its header.
- The read before a register saw only records directly inside the result in HP's namespace; a record with the same id in
  another shape was not seen and the register was sent.
- An agent name holding U+FFFE, U+FFFF or a lone surrogate passed the parser and failed in the envelope writer.
- The printed undo command left out `--addressing`, `--password-name` and `--timeout-seconds`.

## What changed

- `oxpd1 undo-owed`:
  - a folder that holds `undo-list.tsv` itself is a run folder: refused before anything is read (exit 2);
  - when no folder directly inside the folder given holds a list: `no undo list was read`, exit 11;
  - a list that is empty or holds only its header is named unreadable (exit 11);
  - `nothing is owed` and exit 0 only when at least one list was read, every list holds an entry line, every line was
    read and no undo is owed.
- `oxpd1 write`, the read before an executed register: every child element of the result is visited; an element that is
  not `AuthenticationAgentRecord` in the result's own namespace, or a record without exactly one `id` there, ends the
  run with exit 10 and nothing written. A device that holds other agents only is still written to.
- `--agent-name`: refused (exit 2, before any folder or connection) when it holds a character XML 1.0 cannot carry; a
  well-formed surrogate pair is taken.
- The printed undo carries `--password-name`, every pin, `--soap-port`, `--addressing` and `--timeout-seconds`, defaults
  included.
- README: the rules above, and four more limits (the recorded clock and ties, the owed line's host and id only, the host
  compared as typed, .NET's own re-send on a pooled connection unmeasured). No new exit code: 2, 10 and 11 widen.

## What proves it

- Red first on `main` itself with the new cells only: Lab 187 / 16 failed, exactly the 16 planted cases, each by an
  `Assert.Equal` line. Green: 2112 / 0 / 2108 / 4. 11 mutants, each red on exactly its cells, no survivor.
- The branch's push run 45279875689: linux 2108 succeeded, windows 2091 succeeded, rules 657 files, secret scan clean.
- A second independent read of the head with a test-only probe of 74 more cases against a stub on 127.0.0.1
  (VERDICT.md): 30 folder and list shapes of `undo-owed` (symbolic links, a list that is a folder, a list or a folder
  closed by permission among them): none that read no entry printed `nothing is owed` or ended 0; the agent name
  checked for every one of the 65536 single code units against the XML writer (none accepted that the writer refuses);
  the printed undo run as printed reached the stub with the register's addressing, password name, port, pins and
  time-out, and `undo-owed` then said `nothing is owed`.

## Still open (measured by that read; none changes what this pull request closes)

- The read before a register reads child ELEMENTS only. A result that holds its records as text or CDATA, or holds a
  comment, a processing instruction or an attribute, is read as "0 records" and the register is sent; inside a record,
  an `id` of another namespace (or unqualified) beside the record's own, another element, or an attribute is not read;
  an element beside the result inside the response is not read. HP's schema is element-only, so a conforming device is
  handled; how a real device answers is unmeasured.
- U+FFFF in the HOST of `--agent-service` or `--prompt-page` passes the parser and fails in the envelope writer (an
  unhandled exception; for an executed register, after the read, with a `Pending` row left for a write never sent).
  Every other single code unit, in the host, the path, the query or the fragment, is refused or written.
- A run folder `undo-owed` cannot open (no search permission) is counted as a folder without a list: beside readable
  lists that are clean it still prints `nothing is owed`. A session folder it cannot list ends in an unhandled
  exception.
- Steps 2 to 4 and the rest of the end-of-session list are not built. Nothing compares the list with the device. No
  device has been reached.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the run folder refused with exit 2, exit
11 when no list is read, an empty or header-only list unreadable, exit 10 on any element outside the record shape, XML's
character rule with pairs taken, every option in the undo, the notes as README text, the cells appended to the landed
class, no new exit code). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.
