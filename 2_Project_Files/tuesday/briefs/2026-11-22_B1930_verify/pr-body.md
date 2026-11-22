The state database follow-up: owed item 43 (1) and (2) of the backlog. One commit on this branch (`69eeb1dc`), merge
base `7b0f4f55`. Six existing files change, all under `src/Datasec.Suite.Data/` and `tests/Datasec.Suite.Data.Tests/`.
No file is added, and no public member, `SuiteDataError` member, migration, snapshot, package, project, lock, solution
or workflow file changes.

## Why

- Owed item 43 (2): when `AddAsync` lost a race for its key (another writer inserted it between the registry's check
  and its save), it threw an untyped `DbUpdateException`, and the failed row stayed tracked, so the next audit append
  on the same context failed too and the audit row of that failure was never written.
- Owed item 43 (1): the README said `SaveChanges` refuses an audit entry that is modified or removed, but code holding
  the context could still change or remove saved entries inside the save, after the check, through a `SavingChanges`
  handler or a save interceptor in its options.

## What changed

- `EfDeviceRegistry.AddAsync`: the save is in a `try`. On `DbUpdateException` the tracker is cleared (as the stale
  update path already does) and the key is read again: held now, `DuplicateDevice`; not held, the original exception
  is rethrown (`throw;`). Clearing the tracker drops every tracked entry of the shared context, including any other
  unsaved change the caller had on it.
- `SuiteDbContext`: both constructors subscribe `ChangeTracker.StateChanged` and `ChangeTracker.Tracked`; a private
  flag is set around `base.SaveChanges` and `base.SaveChangesAsync` (the async override becomes `async`, its signature
  unchanged). While it is set, an `AuditEntry` that turns, or is tracked, `Modified` or `Deleted` throws
  `SuiteDataException(AuditEntryChanged)` out of the save.
- README: the registry line and the audit line say what the code now does; a new limit says a hook inside the save can
  still change an entry that is being added.
- Cells: three in `RegistryTests` (the lost race, the audit append after it, a failed add that is not the key) and three
  in `AuditTests` (a `SavingChanges` handler refused, a save interceptor refused, the entry-being-added limit), with
  test-only helpers `NewContextWith`, `RaceWinner` and `AuditRemover`. No existing cell, helper or assertion changes.

## What proves it

- Red first on macOS arm64 at `7b0f4f55`: with only the race cells applied the Data assembly reads 55, 3 failed (the
  three race cells, each by its own assertion); with the fix, 55, 0 failed. With the two refusal cells added and no
  guard, 58, 2 failed; with the guard, 58, 0 failed. The patched tree equals this head's tree.
- Mutants on the head (Data assembly, 58 cases): the race mapped away turns the lost-race cell red; the tracker not
  cleared turns the two after-the-failure cells red; every failure called a duplicate turns the not-a-duplicate cell
  red; the `StateChanged` watch removed turns both refusal cells red.
- C# totals 1587 on both legs at the head (1581 + 6), skipped 4 on linux and 19 on windows, RULES 500 files, 111 unit
  tests with floor 111 (push run 45017600055, four jobs success). Merged with the current `main` the totals are 1595.

## Still open

- A hook that runs a nested `SaveChanges` first and then changes or removes saved entries is not refused: the nested
  save clears the flag before the outer save detects the change (measured: all rows changed, or all rows removed).
  Restoring the flag's previous value instead of clearing it would close this; it is left for a later change.
- A `SavedChanges` handler runs after the commit: an entry it marks modified is refused, but the save's own rows are
  already written while the caller sees the refusal.
- The `Tracked` half of the watch and the synchronous `SaveChanges` path have no cell in this change (both were
  measured to refuse).
- An entry being added, `ExecuteUpdate`, `ExecuteDelete`, raw SQL and a command interceptor that rewrites SQL still
  bypass the refusal; the README names all but the command interceptor.
- The race is recognised by reading the key again; a unique violation on PostgreSQL or SQL Server is not measured (no
  real server runs in this project). A failure of that re-read (a cancellation, a lost connection) replaces the
  original exception.
- Items 43 (3) to (6) are unchanged.

## Who decides

The coordinator chose, as coordinator, to make items 43 (1) and (2) one change, and chose every choice inside it: the
in-save refusal over a named limit, reading the key again, rethrowing EF Core's exception, and clearing the whole
tracker.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
