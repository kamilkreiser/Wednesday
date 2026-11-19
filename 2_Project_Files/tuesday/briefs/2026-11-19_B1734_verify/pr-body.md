## What changes

One sentence of one table cell (line 17) of `docs/IMPORTER.md` is corrected. The old words said the parity proof "counts them and compares the governed options only" about the colour panels. The new words say what the proof does: it does not compare the colour-panel records with the approved workbook, does not re-read the book, counts the section's SKUs per sheet against the store, and checks that the store holds exactly the owed (device, SKU) pairs, each once.

The file changes by 1 line added and 1 line removed. No code, test, contract or other document byte changes.

## Why it is safe

- Each word was read against `src/MpsCalc.Import/Parity/ParityProof.cs` (the `Run` method, `CheckPanels` and `CompareRecords`) and against `docs/IMPORTER.md` lines 86-95, which still read true.
- No program, test or CI step reads the words of this document (checked over the tracked files).
- This is a developer documentation correction under the agreed rule for developer-only documents (C-109).
- Nothing is deployed by this change.

## Landing

Squash merge, pinned to the head commit. Hosted CI and CodeQL must be green first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
