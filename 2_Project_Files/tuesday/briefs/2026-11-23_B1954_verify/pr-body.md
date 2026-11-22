## Why

Two limits lines in the library READMEs were not true of every shape they covered, and the change pins each with one
new test cell. No product code line changes.

## What changes

- `src/Datasec.Suite.Data/README.md`, Limits, the `SavedChanges` line: a handler that catches the audit refusal hides
  it from the caller of that save; the entry stays modified in the context's tracker, and the next save on that
  context refuses it before anything of that save is written. Asserted for the handler; a save interceptor's
  `SavedChanges` step that catches is read from the code and not asserted.
- `src/Datasec.Suite.UniversalPrint/Registration/README.md`: the late-answer bullet says the comparison is with the
  holder's state for the id as it was when the call was made (`Remove(id)` ends it, a later `GetAsync(id)` starts a
  new one); the Limits line names one valid token object answered to two calls for one id across a `Remove(id)`, in
  both orders of the two answers: held first, the id serves cleared bytes; disposed first, the later answer is refused
  `TokenAnswerRefused` and the issuer is asked again.
- `tests/Datasec.Suite.Data.Tests/AuditSavedChangesLimitTests.cs` (new): one cell, the catching handler's shape.
- `tests/Datasec.Suite.UniversalPrint.Tests/Registration/CloudDeviceTokenHolderLimitTests.cs` (new): one cell, L01,
  four forms: each order, in time and after the bound.

## What proves it

- Each cell is green on today's code (it pins the behaviour, it does not ask for it) and is turned red by product
  mutants run locally and never committed: two for the Data cell; five for L01, each red at its own form.
- `git diff --name-only <base> -- src` lists the two README files only.
- Totals 1783 to 1785 on both legs (no skip added); tracked files 551 to 553; unit tests 111, floor 111.

## Still open (named, not built)

- A latch that refuses a save's commit after a caught audit refusal; database-level append-only enforcement.
- A refusal of one token object across holder states or across a `Remove`.
- No cell reaches the holder's second disposed check, the one under the registration's lock (the cells reach the
  check on arrival).

## Who decides

The coordinator chose, as coordinator, the cut of this change and every choice inside it: name both limits as README
text with one pinning cell each, state both orders of the two answers and pin each in L01, and name the interceptor
form as read from the code. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
