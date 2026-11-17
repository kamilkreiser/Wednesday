## What this changes

Four developer-only lines still said that work was owed which the code already does. They now say what the code does. Comment and docs text only; no code line, identifier, assertion or test row changes.

- `docs/API.md:379`: the lead-in to the staff list columns now says the contract was written first and the values are filled now, and points to the next bullet, which lists the columns each quote carries.
- `tests/MpsCalc.Api.Tests/QuoteApiTests.V0Home.cs`: three comments (`:14`, `:38-39`, `:69`) now say that the server accepts `readyToExport` (it is listed in `QuoteFigures.ListFilter.Parameters`), and that a staff caller's row carries what `docs/API.md` says for its quote mode.

MPSCALC-411. Developer-only words, written from what the code does (the product owner's 2026-11-11 ruling for developer-only text).

## Verified

- With the comment lines dropped, the test file is byte-equal before and after (by program).
- No line of docs, src, tests or web/src still says a value the code supplies waits for later work.
- `dotnet build MpsCalc.slnx -c Release`: 0 warnings, 0 errors. Whole-solution tests passed before and after with equal counts (Engine 743, Import 196, Api 3663).
- The contract file and its generated copies are unchanged; no sync runs.

## Not deployed

Nothing is deployed. Hosted CI and CodeQL are the final check.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
