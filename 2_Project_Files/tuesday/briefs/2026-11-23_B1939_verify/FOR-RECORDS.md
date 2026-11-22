# FOR RECORDS: OXPd 2 lane F2 follow-ups (kit B1936, seat X38), gate G1 round 1 of 2, reader B1939

Not repository text. For the next OXPd records pass (backlog owed items 42, 43 and 45); nothing here was written into
the project. No person is named. Who decided: the coordinator (Tuesday), as coordinator (Q1 = a and Q2 to Q6 the
defaults, each the coordinator's stamp S4 of kit B1936); nothing here says the product owner decided anything about
this lane.

## What lands

- One commit `b74f0f0c` (parent `c480a0c8`) squashed onto main; seven existing files (numstat 8/3, 6/2, 5/2, 19/3,
  14/6, 32/0, 97/0). C# totals +2 on both legs (1664 on main `c480a0c8`; 1670 with lane F1 also landed, measured
  locally); skipped 4 / 21; RULES 530 files; unit tests 111, floor 111. Public surface by reflection equal on the
  Secrets, Data and Adapters.Oxpd2 assemblies (160 / 107 / 22915 lines); Data PUBLIC 85 lines and SCHEMA 8 files equal.
- Owed item 42 (2) closes (gate B1927 FOUND 1): after a passing probe the removal judges the record again under the
  store's lock and removes it only while it still does not read; a record that reads now is kept (false); nothing
  handed over is `StorageFailed`. Cell U23, red first at `c480a0c8`. Gate B1927 Info 2 answered in the README: the
  older-active-key residual needs that one key to fail after the start. Item 42 (1) (who may call `DeleteUnreadable`)
  unchanged.
- Owed item 43 (1)'s residual (gate B1933 FOUND 1) is NAMED, not closed: a `SavingChanges` handler or a save
  interceptor that catches the refusal keeps its change and the save writes it; the README's audit sentence, a Limits
  line and the watch's doc comment say so; a limit cell asserts it for the handler. The latch (gate B1933's fix sketch
  (b)) stays an owed design choice.
- Owed item 45's open point (gate B1926 FOUND 1) closes: the adapter README's map sentence names the 150 open object
  schemas and how each kind is read.

## From this gate (for the backlog)

1. **Owed, Minor: the Data README's `SavedChanges` line is not true of a `SavedChanges` handler that catches.** The
   line reads "an audit entry it changes or removes is refused and the change is never written, but the save's own
   rows are already written, so the caller sees the refusal for a save whose rows are stored". MEASURED by the gate
   (scratch probe P8, macOS arm64, on the head): a `SavedChanges` handler that catches the refusal around a change to
   a saved entry: `caught 1; state Modified; first save exception none; after first rows 4; rows user-9 0; second save
   SuiteDataException AuditEntryChanged; after second rows 4; rows user-9 0`. So "never written" holds in this shape
   (kit B1936's D5, DERIVED there, now measured), but the caller of that save sees no refusal: the change stays
   tracked as modified and the NEXT save on that context is refused. Fix sketch for a records or later card: add to
   the line "; a handler that catches the refusal hides it from the caller of that save, and the next save on that
   context refuses the still-changed entry". Kit B1936 Q4 left the line unchanged by the coordinator's stamp; this
   is that point, measured.
2. **Info (measured, no change needed): the catching-hook limit is exactly scoped.** A hook that changes the entity
   object directly (no change-tracker call) inside a try/catch never receives the refusal: the save's own change
   detection after the hook raises it, out of the hook's reach (probe P7: `caught 0; exception SuiteDataException
   AuditEntryChanged; rows 3; rows user-9 0`, the append not written either). The interceptor shape the README names
   and the kit only RELAYED from gate B1933 is now re-measured (P5: `caught 3; states after catch
   Deleted,Deleted,Deleted; exception none; rows 1`), and the handler's "after the entry's state has changed" (P6:
   `states after catch Modified/user-9` x3, `rows 4; rows user-9 3`).
3. **Info (measured): the second judgement's other outcomes.** Kit B1936 H6 and H7 were DERIVED; probed on the head
   with a scripted record store of the gate's own: absent at the second read, `removed False; reads 2; deletes 0`
   (H6); replaced between the reads by another record that does not read under that id, `removed True; deletes 1`
   (H7: the second judgement does not re-check the payload's key id; covered by the README's one-process-per-partition
   limit); a fault of another kind at the second read, `StorageFailed; deletes 0; held True`; bytes that do not parse,
   read once and removed (no probe, as on main).

## Not measured (carried)

- An older active key failing alone after the start (needs a fault for one key inside the data protection library).
- What the hosted legs print for the merge with lane F1 (windows succeeded 1649 is PREDICTED).
- CodeQL on the pull request (no pull request exists yet).
