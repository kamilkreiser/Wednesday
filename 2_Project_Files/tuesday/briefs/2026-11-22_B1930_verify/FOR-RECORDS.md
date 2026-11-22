# FOR RECORDS: OXPd 2 state database follow-up (kit B1921, lane D, Q1 = b), gate G1 round 1, reader B1930

Not repository text. For the next OXPd records pass (backlog owed item 43); nothing here was written into the project.
No person is named. Who decided: the coordinator (Tuesday), as coordinator (Q1 = b is the coordinator's stamp S4);
nothing here says the product owner decided anything about this lane.

## What lands

- One commit `69eeb1dc` (parent `7b0f4f55`) squashed onto main: six existing files under `src/Datasec.Suite.Data/`
  and `tests/Datasec.Suite.Data.Tests/` (numstat 17/1, 10/2, 42/3, 72/0, 55/0, 27/0). C# totals +6 on both legs
  (1595 on main `83683af4`); skipped 4 / 19; RULES 500 files; unit tests 111, floor 111. PUBLIC 85 lines and SCHEMA
  8 files equal.
- Owed item 43 (2) closes: a lost duplicate race is `DuplicateDevice` (the key read again after `Clear()`), the next
  audit append on the same context is written; a failed add that is not the key keeps EF Core's `DbUpdateException`
  and clears the tracker. Three cells, red first.
- Owed item 43 (1) closes for the measured shapes (Q1 = b): a `SavingChanges` handler or a save interceptor that changes
  or removes a saved entry is refused `AuditEntryChanged` and nothing is written. The entry-being-added limit is named
  and asserted. Decision D15's text in the design documents: a records seat's update after the landing.
- Items 43 (3) to (6) stay owed.

## From this gate (for the backlog)

1. **Owed, Minor: the in-save flag is not re-entrant.** `SaveChanges`/`SaveChangesAsync` set `saving = true` and
   reset it to `false` in `finally`. A hook that runs a nested save and then changes entries finds the flag already
   cleared when the outer save detects the change. MEASURED (probes G03, G04, macOS arm64): a `SavingChanges` handler
   that calls `context.SaveChanges()` and then sets every entry's actor id: no exception, 4 of 4 rows changed; a save
   interceptor that awaits `SaveChangesAsync` and then marks every entry deleted: no exception, 0 rows left. The README's
   new audit sentence is false in this shape. Fix sketch: `var outer = saving; saving = true; try { ... } finally
   { saving = outer; }` (or a depth counter), plus a cell of the G03 or G04 shape. No main regression: main refused
   neither shape.
2. **Info: a `SavedChanges` handler is inside `base.SaveChanges`, after the commit.** One that marks a saved entry
   modified is refused `AuditEntryChanged`, but the append's row is already committed (G05: 4 rows after, 3 before),
   so the caller sees a failure for a written row; the change itself is never written.
3. **Info: coverage.** The `Tracked` half has no committed cell: probe G02 (a detached entry attached as modified inside
   the save) is refused at the head and accepted with the `Tracked` line removed (1 row changed). The sync path has no
   committed cell: G01 refused, table equal. The command interceptor is not named in the README (the kit's D2 and stamp
   S4 said it would be).
4. **Info: dropped changes at a failed add (H10).** G07: an unsaved audit entry pending on the shared context when an
   add loses its race is rolled back with the insert and then cleared: 0 audit rows, 0 tracked. The README says the
   tracker is cleared, not that other unsaved changes are dropped (the squash body says it).
5. **Info: a cancellation during the re-read (H9).** G06: `OperationCanceledException`, no inner exception (the
   original `DbUpdateException` is lost), tracker 0, and the next append on the same context is written.
6. **Measured, holds:** two contexts on one connection (G08: the other context's change not written, its own save
   refused); the flag after a failed save (G09: cleared, a later mark outside a save not refused).
7. **UNMEASURED:** a unique violation and an aborted transaction on PostgreSQL or SQL Server (the re-read after an
   error inside a caller's transaction on PostgreSQL could fail instead of mapping, DERIVED from that provider's
   aborted-transaction rule, never run).
