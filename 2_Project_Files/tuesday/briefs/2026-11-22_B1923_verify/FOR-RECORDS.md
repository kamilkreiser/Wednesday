# FOR RECORDS: OXPd 2 held test cells (kit B1917, lane T, owed items 47 and 48), gate G2 round 1, reader B1923

Not repository text. For the next OXPd records pass (backlog owed items 47 and 48, item 46's note); nothing here was
written into the project. No person is named.

## What lands

- ONE commit `bb495b4a` on main `4a0a9717`, two test files: `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs`
  (64 added, 0 removed) and `tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs` (22 added, 0 removed). No
  file under `src/` or `contracts/`, no project, lock, solution or workflow file. C# totals 1581 on both legs (1579 +
  2: the theory's two rows; K8 stays one case); skipped 4 / 19; RULES 500 files; unit tests 111, floor 111.
- Owed item 47 closes: the W02 body theory and `ThrowingBody`, byte for byte the held diff (sha256 `ca79627a...`,
  equal in the seat's tools, the head's own diff and the third round's `.tools/b1872/gate/2-w02-body.diff`). It kills
  `mReasonDisposed`, which the base's tests leave green.
- Owed item 48 closes: a check inside K8 that every client model with an optional root property refuses its FIRST
  optional root property sent as null (`WrongType` at `$.<name>`), with a `> 0` count assertion. It kills
  `mNullStrictToo` (generated runtime and generator edited alike), which the base's tests leave green.
- Item 46's NOT DECIDED 1 (whether device answers should be read tolerantly at all) is untouched; the check pins
  today's strict reading and turns red by design if that is ever answered yes.

## From this gate

1. **Scope of the K8 check, stated for the records (Info):** one optional property per model (the first in schema
   order) and the root only. That is enough for the one shared rule at `Oxpd2Json.cs:431` (its `Tolerant` flag is per
   schema, not per property), and nested client schemas are held strict by K8's existing walk over every reachable
   schema's `Tolerant` flag. Not "every optional property of every model".
2. **The count the check sends as a diagnostic, now MEASURED:** the Contracts executable run whole with
   `-diagnostics` on the head prints `K8: client models refusing an optional root null 716`, equal to the 716 client
   models the tolerant-reading first reader's probe counted. The check walks the whole set, not a subset. The count is
   not pinned by the test (a new client model does not turn it red).
3. **The seat's `cp -p` undo (its DEVIATIONS 2):** re-done here with every mutant applied and undone by a full write
   (a fresh file time each time); the reds and greens reproduced exactly. The seat's results stand.
4. **The theory's `IOException` row is a contrast row** (no mutant of the kit turns it red, by design). The gate's own
   mutant `mIO` (`|| ex is IOException` added to the `JobNotFound` arm) turns it red, together with three `C01` rows
   and `L01` (Jobs 122, Failed 5): the row is not hollow, though landed cells already held that arm.
