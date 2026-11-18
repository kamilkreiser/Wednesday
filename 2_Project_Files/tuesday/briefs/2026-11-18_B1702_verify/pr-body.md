## What changes

The validate paragraph of the developer API document, and the matching description of the validate operation in the API contract, said a source version id is unique "across every governed version that did not fail". The server counts a different set. A version blocks a copy in the state Validating, Active or Superseded, and also in a state word the server does not know (so an unrecognised word fails closed). A Draft, a Failed Validation and an Expired version do not count.

This change words the clause as the check is:

- `docs/API.md`: the one clause in the validate paragraph.
- `docs/api/openapi.json`: the same clause inside the validate operation description.
- `web/src/api/generated/*`: the three generated copies, written by `web/scripts/sync-contract.mjs` and by nothing else.

No code, test or other sentence changes. The rule itself is unchanged; only its description is corrected. The source of the new words is `SourceDocumentChecks.cs` (the duplicate check and `CountsAsDuplicate`) and the state rows in the source lifecycle tests.

Agreed by the product owner on 18 November: the contract description changes together with the document.

## Deployment

Nothing is deployed. This is documentation and a contract description; the hosted service is not touched.

## Checks run

- Re-running the generator at the first commit reproduces the generated files with no difference; the contract and the snapshot are byte-identical.
- Contract tests: 4 passed. Web tests: 1616 passed. Lint clean.
- `dotnet build MpsCalc.slnx -c Release`: 0 warnings, 0 errors.

The generated `SOURCE.txt` names the first commit of this branch as its source; a squash merge does not carry that commit, and the tests compare only bytes and the recorded hash, not the commit.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
