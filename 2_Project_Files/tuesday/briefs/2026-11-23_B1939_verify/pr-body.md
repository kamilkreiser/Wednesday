Three follow-ups of the secret store, the state database and the OXPd 2 adapter: owed items 42 (2), 43 (1) and 45 of
the backlog. One commit, `b74f0f0c`, on `main` `c480a0c8` (ahead 1, behind 0). Seven existing files change, under
`src/Datasec.Suite.Secrets/`, `tests/Datasec.Suite.Secrets.Tests/`, `src/Datasec.Suite.Data/`,
`tests/Datasec.Suite.Data.Tests/` and `src/Datasec.Suite.Adapters.Oxpd2/README.md`. No file is added, and no public
member, error reason, migration, snapshot, package, project, lock, solution or workflow file changes.

## Why

- Item 42 (2): the removal guard probed the protection after judging the record, so a failure of the protection that
  ended between the judgement and the probe still removed a record that was good.
- Item 43 (1): a `SavingChanges` handler or a save interceptor that catches the audit refusal and goes on keeps its
  change, and the save writes it. The README's audit sentence and the watch's doc comment said the change is never
  written.
- Item 45: the adapter README said the inputs hold no map, which is true only of a declared map; 150 object schemas
  declare no properties at all, and are open by JSON Schema's default.

## What changed

- `LocalSecretStore.RemoveUnopened`: under a key of the verified ring that is not revoked, a failing probe is
  `StorageFailed` as before; after a passing probe the record is judged again under the same lock: still not read,
  removed; reads now (or is absent), kept and `false`; bytes not handed over, `StorageFailed` and kept. Records under a
  key the ring does not hold, or holds only as revoked, are removed without the probe, as before. Doc comment and the
  Secrets README say so; its Limits line keeps one residual: an older key that is not revoked and fails alone after the
  start.
- Data: no code line changes. The README's audit sentence gains "unless that handler or interceptor catches the
  refusal (see Limits)", a Limits line names the shape for a handler and for a save interceptor, and the watch's doc
  comment says the same.
- Adapter README: the map sentence names the census (206 `additionalProperties`, all `false`; no `patternProperties` or
  `propertyNames`; the generator reads none of them) and the 150 open object schemas: inline, a raw `JsonElement`
  (66 properties, for example `CapabilitiesImplInfoItem.Value`); a component, a model with no property (for example
  `BeepRequest`); a key a schema does not list is skipped when read.
- Cells: `U23` in `InventoryTests` with a test-only record store `DamagingRecordStore`, and one limit cell in
  `AuditTests` for a `SavingChanges` handler that catches. No existing cell, helper or assertion changes.

## What proves it

- Red first on macOS arm64: at `c480a0c8` with the cells alone the Secrets assembly reads 95, 1 failed, `U23` by its
  own assertion (`a record that reads when judged again after the probe was removed`); 95, 0 on the head. The Data
  limit cell is green at `c480a0c8` (it pins today's behaviour).
- Five mutants on the head, each red on exactly its cells: no second judgement (U23); the second judgement keeps a
  record that fails (U23, U04); a second read that hands over nothing returns false (U23); the probe's answer ignored
  (U22); the in-save `StateChanged` watch off (the limit cell and the six existing in-save cells).
- Public surface by reflection equal on the three assemblies (Secrets 160 lines, Data 107, Adapters.Oxpd2 22915),
  with a planted control that differs; the Data library's public lines and schema files equal.
- Census of the inputs and generated code equal to the README's numbers, with a planted control.
- C# totals 1664 on both legs at the head (1662 + 2), skipped 4 on linux and 21 on windows, RULES 530 files, 111 unit
  tests with floor 111 (push run 45029832759, four jobs success). With the sign-in and device token follow-up also
  applied: 1670 locally (1666 succeeded, 4 skipped).

## Still open

- The secret store: an older key of the ring that is not revoked and fails alone after the start still reads as a
  record that does not open, and that record is removed (named; not measured). Who may call `DeleteUnreadable` in the
  product is unchanged (item 42 (1)).
- The state database: a hook that catches the refusal keeps its change (named, asserted for the handler; the save
  interceptor's shape is named, not asserted). A library-owned refusal of the save's own commands is an owed design
  choice. A `SavedChanges` handler that catches the refusal: the change is not written by that save, and the next save
  on that context is refused; the README's `SavedChanges` line still says the caller sees the refusal, which such a
  handler hides from the caller of that save (unchanged here).
- An entry being added, `ExecuteUpdate`, `ExecuteDelete`, raw SQL and a command interceptor still bypass the refusal
  (each named in the README).

## Who decides

The coordinator chose, as coordinator, the three items and every choice inside them: the second judgement, the
tests' own record store for the cell, the catching hook as a named limit with one cell rather than a new refusal,
the `SavedChanges` line left as it stands, and the map sentence as built.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
