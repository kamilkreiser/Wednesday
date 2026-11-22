## Why

Two limits lines in the library READMEs were not true of every shape they covered, and the change pins each with one
new test cell. No product code line changes.

## What changes

- `src/Datasec.Suite.Data/README.md`, Limits, the `SavedChanges` line: a handler that catches the audit refusal hides
  it from the caller of that save; the entry stays modified in the context's tracker, and the next save on that
  context refuses it before anything of that save is written. Asserted for the handler; a save interceptor's
  `SavedChanges` step that catches is read from the code and not asserted.
- `src/Datasec.Suite.UniversalPrint/Registration/README.md`: the late-answer bullet says which state of the holder a
  call made before `Remove(id)` compares its answer with; the Limits line names one token object answered to two calls
  for one id across a `Remove(id)`, and in which order of the two answers the id then serves cleared bytes.
- `tests/Datasec.Suite.Data.Tests/AuditSavedChangesLimitTests.cs` (new): one cell, the catching handler's shape.
- `tests/Datasec.Suite.UniversalPrint.Tests/Registration/CloudDeviceTokenHolderLimitTests.cs` (new): one cell, L01,
  in time and after the bound.

## What proves it

- Each cell is green on today's code (it pins the behaviour, it does not ask for it) and is turned red by two
  product mutants each, run locally and never committed: the in-save state watch and the asynchronous pre-check for
  the Data cell; the in-time dispose of an answer for a removed entry and the late-answer dispose for L01.
- `git diff --name-only <base> -- src` lists the two README files only.
- Totals 1759 to 1761 on both legs (no skip added); tracked files 551 to 553; unit tests 111, floor 111.

## Still open (named, not built)

- A latch that refuses a save's commit after a caught audit refusal; database-level append-only enforcement.
- A refusal of one token object across holder states or across a `Remove`.

## Who decides

The coordinator chose, as coordinator, the cut of this change and every choice inside it: name both limits as README
text with one pinning cell each, keep "registration" in the late-answer bullet as the holder's own per-call state,
and name the interceptor form as read from the code. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
