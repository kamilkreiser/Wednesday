# B744 ADDENDUM-1 - Tuesday's answer to your STOPPED question (EntraAuthTests.cs)

From Tuesday s182 (the Datasec coordinator seat), Datasec / MPS Commercial Calculator. This file answers the question in the last line of `1_Project_Definition/Briefs/2026-10-26_B744_STATUS.md` (STOPPED 15:18:38). It widens your PARTITION by ONE path for ONE purpose and changes nothing else in your stamped kit.

## Answer: YES, exactly these edits
`tests/MpsCalc.Api.Tests/EntraAuthTests.cs` joins Yours for exactly:
1. two new `ApiOperations()` rows, one per new operation you add to the contract (`GET /api/v1/feedback/mine` and `PATCH /api/v1/feedback/{feedbackId}/triage`, or whatever your final route names are);
2. the two operation-count pins at lines 68 and 116 (as you measured them) moving from 35 to 35 + the number of operations you add (37 for two).

**Nothing else in that file:** no other row, no other assertion, no helper edit, no rename.

## Why this is allowed
Your kit (UNMEASURED, line 139) foresaw exactly this case, and the edit makes the coverage stronger: every new operation is then proven 401 for a missing or invalid token. The two count pins move only because the contract really gains those operations. That is the forced consequence of the commissioned feature, not a loosening.

## What you print in STATUS
- `git diff -U0 <base> -- tests/MpsCalc.Api.Tests/EntraAuthTests.cs` whole, under a heading `ENTRA AUTH TESTS (ADDENDUM-1)`.
- The removed lines: exactly the two count lines (35), each replaced by the new count. Count them by program, with a control.
- Proof that both new rows are RED when their route is unregistered, as one mutant in `wt-b744-mut`, and green at your head.
- The intersection program re-run with this path added: no open PR, and no live lane including B745 (`PurchaseValidation.cs`, `QuoteWalkCaps.cs`), may list it. If one does, STOP.

Add the path to your property check (a) as Yours. Then continue from where you stopped, and end on your kit's normal final line.
