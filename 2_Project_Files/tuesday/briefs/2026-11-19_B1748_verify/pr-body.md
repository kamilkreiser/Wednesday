## What changes

When a draft is refused with 400 BAD_REQUEST because its quote reference is too long, the `errors` list used to say:

    quoteRef is at most 100 characters and customer at most 200.

It now says:

    quoteRef is at most 100 UTF-16 code units (an emoji counts as two) and customer at most 200.

That is the sentence the API document and the contract file already carry for the quote reference (the agreed sentence `at most 100 UTF-16 code units (an emoji counts as two)`). The old words told a caller 100 characters while a reference of 99 letters and one emoji (101 units) was refused.

Two lines change in two files:

- `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`: the one message string.
- `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs`: the one test line that pins that string (it runs for the three `invalid` cells of the refusal-order test).

## What does not change

- The limit is still 100 for the quote reference and 200 for the customer. The condition (`Length > 100 || Length > 200`) is not touched: the counting stays by UTF-16 code units, as the earlier ruling says.
- Every other message, the API document, the contract file and everything under `web/` are untouched.

## What stays open on the ticket

The two `maxLength: 100` entries for `quoteRef` in `docs/api/openapi.json` (the draft schema and the duplicate request) still carry no unit. They need words that no accepted text gives, and changing them also means regenerating the three generated contract files. That is a separate piece of work.

## Reading to note

The accepted wording covers this message by the coordinator's reading of the product owner's 2026-11-11 acceptance, recorded in the project's records: the comment on the ticket that lists the places still to change names this refusal sentence, and the earlier ruling's "no code change" is read as "the counting is unchanged". The sentence used is the earlier ruling's own form, not a shorter paraphrase.

## Not deployed

Nothing is deployed by this change. The hosted app is unchanged.

## Checks run before this pull request

Build in Release: 0 warnings, 0 errors. The whole API test project passes. The refusal-order tests fail on each of the three `invalid` cells when either the message or its pinned line is put back to the old words, and pass with both new.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
