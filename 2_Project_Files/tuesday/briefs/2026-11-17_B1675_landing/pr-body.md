## BLUF
One new test row pins what `startingOwner` already returns for a lone high surrogate that is the 100th unit. Tests only; the store file is byte-identical to main; nothing deployed; no integration with HP tools.

## What changes
- `web/src/components/customer/remediation-store.test.ts`: one `it(...)` row (10 added lines including one blank, 0 deleted) in the `startingOwner` block, before the row about a first character longer than the limit.
- Input: 99 letters, one lone high surrogate (U+D83D), then `b`. Result pinned: 100 units ending in the lone half; the `b` is not added; the register's own check (`checkEntry`) accepts it.

## The decision, and why it is a pin
The result is the one the code gave before and after the earlier grapheme change, so no behaviour moved. Of the two results the ticket offered (keep it, or end the result before a lone high surrogate that would be its last unit), the ticket's proposed default, approved for this change, was to keep it and pin it. The expected value is written in the row's title.

## Evidence
- Red first (row typed with one planted wrong expectation): expecting the 99 letters alone -> 1 failed, 136 passed of 137 (received: the 100 units ending in the lone half); expecting length 99 -> 1 failed, on that line; the true row -> 137 passed, 0 failed.
- The same Node (v24.21.0) measured the same input: length 100, last unit d83d, ends with b false, lone-half check true.
- Whole web suite, local: main 304 files, 4339 passed, 0 failed, 0 skipped; this change 304 files, 4340 passed, 0 failed, 0 skipped; by program, lost 0, added 1 (this row), changed 0.
- The store's test file alone: 136 tests at main, 137 here.
- `npm run lint` and `npm run typecheck`: exit 0. Infra: hidden-characters scan 14 OK, all infra tests 325 OK, `validate.sh` exit 0.
- Not run locally: build and the browser (e2e) shards. No e2e spec imports the store (0 files); a new row in a unit-test file changes no code the app or a browser loads.

Tests only, no product line changed. Nothing deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
