# FOR RECORDS: OXPd 2 state database follow-up (kits B1921 and B1932, lane D), gate G1 round 2 of 2, reader B1933

Not repository text. For the next OXPd records pass (backlog owed item 43); nothing here was written into the project.
No person is named. Who decided: the coordinator (Tuesday), as coordinator (round 1 Q1 = b, round 2 Q1 = a and
Q2 = a, each the coordinator's stamp S4); nothing here says the product owner decided anything about this lane.

## What lands

- Two commits squashed onto main: `69eeb1dc` (parent `7b0f4f55`) and `07ae18eb` (parent `69eeb1dc`); six existing
  files under `src/Datasec.Suite.Data/` and `tests/Datasec.Suite.Data.Tests/` (numstat against the merge base 17/1,
  19/4, 45/3, 200/0, 55/0, 27/0). C# totals +11 on both legs (1662 on main `40bfe5db`); skipped 4 / 21; RULES 530
  files; unit tests 111, floor 111. PUBLIC 85 lines and SCHEMA 8 files equal against both `69eeb1dc` and `7b0f4f55`.
- Owed item 43 (2) closes: a lost duplicate race is `DuplicateDevice` (the key read again after `Clear()`), the next
  audit append on the same context is written; a failed add that is not the key keeps EF Core's `DbUpdateException`
  and clears the tracker. Three cells, red first.
- Owed item 43 (1) closes for the measured shapes: a `SavingChanges` handler or a save interceptor that changes or
  removes a saved entry is refused `AuditEntryChanged` and the change is not written, also after it has run a save of
  its own (the flag is restored, not cleared; two cells red first at `69eeb1dc`); the `Tracked` half and the
  synchronous path each have a cell; the README names an entry being added (asserted), a command interceptor (named,
  not asserted) and a `SavedChanges` handler or interceptor step, which runs after the commit (asserted for the
  handler), and says that what a hook's own save already wrote stays written.
- Decision D15's text in the design documents and the closing text of item 43 (1) and (2): a records seat's update
  after the landing. Items 43 (3) to (6) stay owed.

## From this gate (for the backlog)

1. **Owed, Minor: a hook that catches the refusal keeps its change.** The watch throws from inside the change tracker's
   `StateChanged` / `Tracked` event, after the entry's state has already changed, so the exception arrives in the
   hook's own code. A hook that catches it (a catch-all around its own work is enough) leaves the entry `Modified` or
   `Deleted`, and the outer save then writes it. MEASURED (scratch probes, macOS arm64, at `07ae18eb` and at
   `69eeb1dc` alike): N5a, a `SavingChanges` handler that catches around each change: `caught 3; exception none;
   rows 4; rows user-9 4`; N5b, a save interceptor that catches around each removal: `caught 3; exception none;
   rows 1`. The README's audit line ("the change is never written ... inside it when a handler ... or a save
   interceptor ... changes or removes it") is false in this shape, and its `SavedChanges` line by the same mechanism
   (DERIVED, not probed). Not a regression: main refuses nothing inside a save. Fix sketch, either: (a) name it in the
   README Limits with a limit cell of N5a's shape; or (b) a latch the watch sets when it refuses, which a library-owned
   command interceptor reads to refuse the save's own commands before they run (DERIVED, not built or measured; its
   ordering against a host's own interceptors is UNMEASURED).
2. **Info: a hook that saves first and then adds an entry.** N4a: the added entry is written (`rows 5`, one back-dated
   by 30 days through the test-only `AuditEntry.Create`). Host code cannot make an `AuditEntry` itself (private
   constructor `Audit.cs:103`, `internal` factory `:122`), so outside the library this is an append through
   `EfAuditLog` (clock-timed) or reflection. N4b: changing that added entry is the named entry-being-added limit
   (`rows user-9 1`).
3. **Measured, holds (each accepted at `69eeb1dc`, refused at `07ae18eb`):** three levels of nested saves with the
   change at level 2 or at level 1 (N1a, N1b: `AuditEntryChanged; rows 4; rows user-9 0`); a nested save that throws
   from a handler (N2a: `rows 3; rows user-9 0`; at `69eeb1dc` `outer none; rows 4; rows user-9 4`); synchronous outer
   with asynchronous nested in a handler (N3a) and in an interceptor (N3b), asynchronous outer with synchronous nested
   in an interceptor (N3c). A nested save refused by the database then a change (N2b) is refused at the head. After a
   nested throw ends the whole save, the flag is off (N6: marking outside a save `none`).
4. **The round-1 probes on the head:** G01 and G02 refused, table equal; G03 refused, `rows 4; rows user-9 0` (was
   `none; rows 4; rows user-9 4`); G04 refused, `rows 4` (was `none; rows 0`); G05 refused, `rows 4 (3 before the
   append)` (the named and asserted `SavedChanges` limit).
5. **UNMEASURED:** a unique violation and an aborted transaction on PostgreSQL or SQL Server; every probe on Linux and
   Windows; the drafter's command-interceptor probe P1 (RELAYED, not re-run here).
