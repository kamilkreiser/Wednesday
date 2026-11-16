## What changed

One comment phrase on line 10 of `tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs`. The summary comment for the X-33 page-estimate tests said the description came from "docs/ENGINE.md row text in the seat's STATUS", which points at a status record that does not live in the repository. It now reads "the row of that id in docs/ENGINE.md", which points at the X-33 row that exists in `docs/ENGINE.md`.

## Why

MPSCALC-390 item 3. A comment in the repository should point at a document in the repository. The rest of the comment already agrees with the X-33 row (page estimates are checked on every purchase quote, and a refusal stops the calculation before any figure is formed), so the description is not reworded.

## Scope

- Comment only: one line, +1 -1. No code, identifier or test row changes.
- With comment lines removed, the file is identical before and after.
- The projects do not generate XML documentation files, so compilation is not affected.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
