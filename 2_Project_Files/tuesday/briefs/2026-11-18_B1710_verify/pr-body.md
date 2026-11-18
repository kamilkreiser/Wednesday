## What

The price-book importer writes a short lineage note into each stored import that holds colour panels. Its last sentence said the parity proof counts the panels per sheet and does not compare them. Since the per-device pair check, the proof does more than that. This change corrects that one sentence to say what the proof does with the panel records:

- it counts the section's SKUs per sheet against the store;
- it checks that the store holds exactly the owed (device, SKU) pairs, each once;
- it does not compare the panel records with the approved workbook;
- it does not re-read the book.

Every word was read against the parity proof's own code. No other sentence of the note changes. The importer documentation already states the same rule and is not changed.

## Tests

One new test row pins the new sentence. It fails with the old sentence put back and passes with the new one. The import tests pass (198), and the build has 0 warnings.

## Authority and scope

A developer correction agreed by the product owner on 18 November, the sentence listed to the product owner after it lands. Two files change: the importer line holding the note and the test file. Nothing is deployed. Stores imported before this lands keep the old note text until their next import.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
