## What changes

The price-book importer stores a PANEL-BLOCK lineage note when a store holds colour panels. The note said the panel rule reads "every row of a model sheet's" colour-panel section. It now says "every row of any mapped model sheet's" section, which is what docs/IMPORTER.md already says and what the importer does: the rule runs on every model sheet the catalogue map names, and on no other sheet.

One new test row, `The_panel_block_note_says_any_mapped_model_sheet`, pins the three added words. No other word of the note changes, and the later sentence about the parity proof is not touched.

## Authority

The words were agreed by the product owner on 18 November.

## Scope

Two files: `src/MpsCalc.Import/PriceBookImporter.cs` (one phrase on one line) and `tests/MpsCalc.Import.Tests/PanelSectionEndTests.cs` (one new test, 11 lines). No docs change.

## Checks

- Import tests: 196 pass before, 197 pass after. With the old phrase put back, exactly the new row fails ("Sub-string not found").
- Nothing reads the note's text: no screen, proposal, API response or stored file in the repository holds it. Stores that were already imported keep the old note text until their next import; nothing reads it.
- Hosted CI runs the whole-solution tests and CodeQL.

## Deployment

Nothing is deployed by this change, and it needs no deploy.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
