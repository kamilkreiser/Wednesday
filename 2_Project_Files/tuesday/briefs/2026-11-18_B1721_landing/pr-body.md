## BLUF
Corrects one stale class comment in the colour panel option tests (MPSCALC-414). Comment lines only: no code, attribute, assertion or test row changes. Nothing is deployed.

## What changes
`tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs`, the class summary: it said the parity proof "counts them only". It now says what the proof does with the colour panels: it counts the panel section's SKUs per sheet against the store and checks that the store holds exactly the owed (device, SKU) pairs, each once, but does not compare them with the approved workbook and does not re-read the book. Each word was read against `src/MpsCalc.Import/Parity/ParityProof.cs`. This is a developer-only sentence, corrected from the code (entry C-109).

## Proof
- One file changed, 3 lines added, 1 removed; every changed line is a `///` comment line (checked by a program that compares the file with comment lines removed; its planted control fails as it should).
- `dotnet build MpsCalc.slnx -c Release`: 0 warnings, 0 errors, before and after.
- `dotnet test tests/MpsCalc.Import.Tests -c Release`: 198 passed, 0 failed, before and after.
- The old phrase no longer occurs in docs, src, tests or .github.

## Not in this change
`docs/IMPORTER.md` line 17 (narrower than the proof, not false) is left for a later ticket.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
