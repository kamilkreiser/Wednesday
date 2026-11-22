The state database follow-up: owed item 43 (1) and (2) of the backlog. Two commits on this branch: `69eeb1dc` (the
race fix and the in-save refusal) and `07ae18eb` (the in-save flag restored, not cleared, at the end of a save; five
more cells; the README limits). Merge base `7b0f4f55`. Six existing files change, all under `src/Datasec.Suite.Data/`
and `tests/Datasec.Suite.Data.Tests/`. No file is added, and no public member, `SuiteDataError` member, migration,
snapshot, package, project, lock, solution or workflow file changes. The landing is one squash.

## Why

- Owed item 43 (2): when `AddAsync` lost a race for its key (another writer inserted it between the registry's check
  and its save), it threw an untyped `DbUpdateException`, and the failed row stayed tracked, so the next audit append
  on the same context failed too and the audit row of that failure was never written.
- Owed item 43 (1): the README said `SaveChanges` refuses an audit entry that is modified or removed, but code holding
  the context could still change or remove saved entries inside the save, after the check, through a `SavingChanges`
  handler or a save interceptor in its options, also after running a save of its own first.

## What changed

- `EfDeviceRegistry.AddAsync`: the save is in a `try`. On `DbUpdateException` the tracker is cleared (as the stale
  update path already does) and the key is read again: held now, `DuplicateDevice`; not held, the original exception
  is rethrown (`throw;`). Clearing the tracker drops every tracked entry of the shared context, including any other
  unsaved change the caller had on it.
- `SuiteDbContext`: both constructors subscribe `ChangeTracker.StateChanged` and `ChangeTracker.Tracked`; a private
  flag is set around `base.SaveChanges` and `base.SaveChangesAsync` (the async override becomes `async`, its signature
  unchanged) and given back in `finally` as the save found it (`var outer = saving; ... saving = outer;`), so a save
  run inside a save, or one that throws, leaves the watch on for the rest of the outer save. While it is set, an
  `AuditEntry` that turns, or is tracked, `Modified` or `Deleted` throws `SuiteDataException(AuditEntryChanged)`.
- README: the registry line and the audit line say what the code now does, including that what a hook's own save
  already wrote stays written; the Limits name an entry being added (asserted), a command interceptor (named, not
  asserted) and a `SavedChanges` handler or a save interceptor's `SavedChanges` step, which runs after the commit
  (asserted for the handler).
- Cells: three in `RegistryTests` (the lost race, the audit append after it, a failed add that is not the key) and
  eight in `AuditTests` (a `SavingChanges` handler, a save interceptor, each also after a save of its own, a detached
  entry tracked as modified, the synchronous save, the entry-being-added limit, the `SavedChanges` limit), with
  test-only helpers `NewContextWith`, `RaceWinner`, `AuditRemover` and `NestedSaveThenRemove`. No existing cell,
  helper or assertion changes.

## What proves it

- Red first on macOS arm64: at `7b0f4f55` the race cells read 55, 3 failed, then 55, 0 with the fix; the two refusal
  cells 58, 2 failed, then 58, 0 with the watch. At `69eeb1dc` the two nested-save cells read 63, 2 failed, each by its
  own assertion, then 63, 0 with the restore.
- Eight mutants on the head, Data assembly 63 cases, each red on exactly its cells: the race mapped away (1); the
  tracker not cleared (2); every failure called a duplicate (1); the `StateChanged` watch off (6); the `Tracked` watch
  off (1); no flag on the synchronous save (1); the synchronous save clearing, not restoring (1); the asynchronous save
  clearing, not restoring (1).
- Outside the cells, measured in scratch on the head: three levels of nested saves, a nested save that throws or is
  refused by the database, and every synchronous and asynchronous mix are refused with no saved entry changed (each
  of them was accepted at `69eeb1dc`); the flag is off again after a save that throws.
- C# totals 1592 on both legs at the head (1581 + 11), skipped 4 on linux and 19 on windows, RULES 500 files, 111 unit
  tests with floor 111 (push run 45021959952, four jobs success). Merged with main `40bfe5db`: 1662, measured locally
  (1658 succeeded, 4 skipped), RULES 530 files.

## Still open

- A hook that catches the refusal and goes on keeps its change, and the outer save writes it: the refusal is an
  exception thrown into the hook's own code after the entry's state has changed (measured: a handler that catches it
  changed all three saved rows; an interceptor that catches it removed all three). The README's audit line does not
  name this shape. It was the same at `69eeb1dc`, and `main` refuses nothing inside a save.
- A `SavedChanges` handler runs after the commit: an entry it marks modified is refused, but the save's own rows are
  already written while the caller sees the refusal (named and asserted).
- An entry being added, `ExecuteUpdate`, `ExecuteDelete`, raw SQL and a command interceptor that rewrites SQL still
  bypass the refusal (each named in the README; the command interceptor is not asserted by a test).
- The race is recognised by reading the key again; a unique violation on PostgreSQL or SQL Server is not measured (no
  real server runs in this project). A failure of that re-read (a cancellation, a lost connection) replaces the
  original exception.
- Items 43 (3) to (6) are unchanged.

## Who decides

The coordinator chose, as coordinator, to make items 43 (1) and (2) one change, to add a second commit before landing,
and every choice inside both: the in-save refusal over a named limit, reading the key again, rethrowing EF Core's
exception, clearing the whole tracker, restoring the flag rather than counting depth, and naming the `SavedChanges`
handler as a limit with its cell.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
