The lab tool's first device-write verb and its end-of-session check. One commit, `67c24d18`, on `e39396f9` (main; ahead 1,
behind 0). One file is added (`tests/Datasec.Suite.Lab.Tests/Oxpd1/Oxpd1WriteTests.cs`) and five change, all under
`src/Datasec.Suite.Lab/` or `tests/Datasec.Suite.Lab.Tests/` (`Oxpd1Command.cs`, `LabFiles.cs`, the `oxpd1` README, the Lab
README, the tests' `Oxpd1Stub.cs`). No package, no `.csproj`, no lock file, no `Datasec.Suite.slnx` line, no workflow, no
`Directory.*` file, no path of the OXPd 1.x client or its tests, no `contracts/` path.

## Why

- `Oxpd1Writer` (the sign-in agent register and unregister, first-run step 5) landed with no caller. The lab needs ONE
  controlled way to send one of those writes to a test printer, refusing to overwrite an agent that is already there.
- A session that registers a test agent must be able to say, before it ends, which undos it still owes.

## What changed

- `oxpd1 write <host> --run <new folder> --credentials-file <file> --pin <sha256> --write RegisterSignInAgent|UnregisterSignInAgent --agent-id <uuid> [...] [--execute]`:
  - a dry run unless `--execute` (prints the address, action, envelope and the undo's command; opens no credentials file;
    connects to nothing);
  - an executed register first reads `GetAuthenticationAgentRecords` and writes nothing when a record holds the same id
    (compared as a UUID) or an unreadable id (exit 10), or when the read does not answer (exit 6 on 401/403, 4 on a refused
    pin, 8 otherwise);
  - the first 401 or 403 ends the run with the read verb's words (now one shared constant); at most two password-bearing
    requests per register, one per unregister, no retry;
  - every executed write is entered in the run folder's `undo-list.tsv` as `Pending` before it is sent and rewritten with
    its end after; the undo is printed whenever the write may have taken effect;
  - an address holding `@` and a name holding a control character are usage errors (exit 2) before any folder or
    connection.
- `oxpd1 undo-owed <session folder>`: reads every run folder's list directly inside the session, in time order; a
  register stays owed until an unregister of the same id on the same host has answered after it; an unreadable line is
  named by its place only; exit 11 when anything is owed or unreadable. It sends nothing.
- New exit codes 10 and 11.

## What proves it

- Red first on `main` + the patch's first shape: Lab 168 / 22 failed, exactly the 22 planted cases, each by an `Assert.`
  line. Green: 2093 / 0 / 2089 / 4. 14 mutants, each red on exactly its cells, no survivor.
- The branch's push run 45180555693: linux 2089 succeeded, windows 2072 succeeded, rules 648 files, secret scan clean.
- An independent read of the head with a test-only probe of 50 more shapes against a stub on 127.0.0.1 (VERDICT.md):
  no dry run connected; no read that did not answer, held the id or held an unreadable id was followed by a write; no
  refused password was followed by another request; the password was in no output and no run file.

## Still open

- `undo-owed` prints `nothing is owed` (exit 0) when it read no list: given the run folder itself, a folder one level
  above the session, or a list that is empty or holds only its header.
- The read before a register sees only records that are direct children of the result in HP's namespace; a record in
  another shape is not seen and the register is sent (HP's schema is the shape built).
- A name holding U+FFFE, U+FFFF or a lone surrogate passes the lab's check and fails in the envelope writer (an
  unhandled exception; for an executed register, after the read, with a `Pending` row left for a write never sent).
- The printed undo command does not carry `--addressing`, `--password-name` or `--timeout-seconds`.
- Equal recorded times are ordered by folder name; the order follows the recorded clock.
- Steps 2 to 4 and the rest of the end-of-session list are not built. Nothing compares the list with the device. No device
  has been reached.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (print-only `undo-owed`, the read verb's
guard structure and words, the list read compared as a UUID and failing closed, the dry-run form, `--pin` required, the
lab's stricter record rules, one list per run folder, exit codes 10 and 11, the two landed files). No choice in this change
is the product owner's.

Nothing is deployed; nothing was sent.
