## What this changes

The published sentences about the four staff-only list columns (`oneOffGp`, `annualRecurringGp`, `tcv`, `totalGp`) said that no row carries them until later work fills them. The code already fills three of the four for a purchase quote and `tcv` alone for a rental quote (`QuoteFigures.Staff`). No quote carries `annualRecurringGp` today. The sentences now say what the code does.

- `docs/API.md`: the Home list paragraph for the four columns (MPSCALC-364; the open ticket for the missing per-year and whole-term figures is MPSCALC-315).
- `docs/api/openapi.json`: the four member descriptions of the staff figures.
- `src/MpsCalc.Api/Contracts/Dtos.cs`: one code comment above the staff figures. No code line, identifier, attribute or test row changes.
- `web/src/api/generated/`: the two generated copies and `SOURCE.txt`, written only by `web/scripts/sync-contract.mjs` from the first commit. The snapshot is byte-identical to the contract.

These are developer-only words (the API document, the contract file, its generated copies and a code comment). The description strings are copied into no screen, proposal or PDF text; the web code imports the generated types only.

## Commits

Two commits. The first holds the hand edits; the second is the generator's output for the first. `SOURCE.txt` names the first commit, which a squash merge does not carry (the same shape as the existing line for an earlier branch commit). The contract tests compare bytes and the hash line only.

## Verified

- Contract tests: red after the first commit (1 failed, 3 passed), green after the sync (4 passed).
- Web: lint clean, 146 test files, 1616 tests passed.
- `dotnet build MpsCalc.slnx -c Release`: 0 warnings, 0 errors.
- Re-running the sync on the first commit gives 0 diff against the second commit.

## Not deployed

Nothing is deployed and nothing needs deploying by this change: docs, a contract description, one code comment and generated copies. Hosted CI and CodeQL are the final check.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
