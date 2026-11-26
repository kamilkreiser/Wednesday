Six owed items of the lab tool `oxpd1`, built and tested against the file system of the system's temporary folder and
bodies held in the tests only. One commit, `cd2a3e13`, on `main` `c73cda4c` (behind 0, ahead 1). Five files, all
changed, none added: `LabFiles.cs` and the README under `src/Datasec.Suite.Lab/Commands/Oxpd1/`, and three test files
under `tests/Datasec.Suite.Lab.Tests/Oxpd1/`. No adapter file, no package, no lock file, no project file, no
`Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- `undo-owed` took a run folder it could not open as a folder without a list: beside two clean lists it printed
  `nothing is owed` and ended 0. A session folder it could not list threw an unhandled exception.
- The certificate file's 64 KiB bound read the size the path itself reports, so a symbolic link to a larger file was
  taken (the link's own size was read).
- The run folder rule collapsed a link's target text before walking on, so a run folder behind a relative link whose
  text walks `..` through another link was read at the wrong folder and could be accepted inside a git work tree.
- `UndoList.Family` put every write kind it did not name into the button family, so a kind added later would fall
  into another family silently.
- The lab README's callback sentence and its "Known, not changed here" bullet no longer matched the client after the
  last change to the OXPd 1.x client.

## What changed

- **`undo-owed`.** Each run folder's entries are listed once before its list is looked for; a listing that fails names
  the folder unreadable (`<folder> (the run folder cannot be opened)`). The session listing is caught and named
  unreadable (`the session folder cannot be listed`). The verb says `no undo list was read` only when nothing was
  unreadable either. Each ends with exit 11, never `nothing is owed`.
- **The certificate file.** Read through ONE stream (a link is followed) into a buffer of 64 KiB and one byte; more than
  64 KiB read is refused with the same words as before. A missing path keeps its refusal.
- **The run folder rule.** `RealPath` resolves one part at a time from a resolved prefix: a link is replaced by its
  own text (absolute from its root, relative from the folder that holds it) and each `..` is taken against the folder
  already resolved, as the system does. The 40-link bound and the read-as-written fallback for a link that cannot be
  read stay.
- **The undo family.** The two button kinds have their own arm; a kind with no arm throws
  `ArgumentOutOfRangeException`.
- **The lab README.** The callback sentence names the client's own reader (`CallbackMessage`) and the 400 answer to any
  other body; the unreadable folders, the bounded read and the link rule are named; the "Known, not changed here"
  bullet is removed (its first half is fixed here, its second half was fixed by the client change).

## What proves it

- Red first: on `main` with the new cells only, the lab's tests read `Total: 314, Failed: 6`, every failure an
  assertion of the new cells. Green: the lab `314 / 0`; the whole solution `total: 2384`, `failed: 0`,
  `succeeded: 2380`, `skipped: 4`; the branch's push run: linux `succeeded: 2380`, windows `succeeded: 2363`, rules
  679 files, `Ran 117 tests`, secret scan clean.
- Six mutants, each turning at least its cells red and nothing outside them: the run folder's listing removed; the
  session listing's catch made blind; the default family back to `button`; the bound back to the path's own size; the
  buffer one byte short; a link's text collapsed before the walk.
- 17 new cases: a run folder of mode 000 beside two clean lists and alone, a session folder of mode 000; six undo-list
  shapes (a list that is a folder, a byte order mark, a blank line, a run folder that is a link, a list that is a link,
  a list that is a dangling link) pinned as they are read today; every write kind's family and an unnamed kind; a
  certificate file of exactly 64 KiB, of 64 KiB and one byte, a link to the larger and a link to the CA; a run folder
  behind a relative link that walks `..` through another link, into a work tree and outside one.

## Still open

- Nothing here has run against a device.
- Not built: a run folder that can be listed but not entered (read permission without search permission) is still
  taken as a folder without a list, so beside clean lists `undo-owed` can say `nothing is owed` while that folder
  holds an owed write.
- A certificate file or an undo list that is a named pipe with no writer blocks the run.
- The write section's `IsServiceEnabled` sentence of the lab README does not name the response's own text and
  attributes (true, not complete).
- On Windows the permission and link rows return at once (no Unix file mode there, and a link needs a privilege).
- No test has a link loop on the run folder's path; the 40-link bound that ends such a walk is in the code.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the lab tool's items split in two
changes, this the first; the code written to a specification; the unreadable run folder and session folder only; the
bounded stream with links followed; the part-by-part walk by each link's own text; `ArgumentOutOfRangeException` for an
unnamed kind; the undo-list shapes pinned as read today; the two README sentences and the whole bullet; the Windows
early returns; no local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
