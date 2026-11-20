## BLUF
This branch builds and tests the L1 content catalogue: the SM 3.16 item and sub-setting ids, read from our own install. The new content release is built and hashed but NOT cut. Cutting it, deploying it and rebuilding the examples stay with the product owner's own decision, and no deploy of a Composer host may ship it without that decision, because a new release makes engagements pinned to the running release read-only. The branch carries a merge of the main branch (head `2a58dc5d`) and was reviewed independently at that head.

## What it changes
- release-draft: 55 -> 137 policy items, 55 -> 351 fields, 123 -> 132 controls (counts read from `bundle.json` at main and at this head). Content hash `5679855b...04f104`.
- release-demo: 55 items and 123 controls, as on main; each of its 55 items gains its SM ids; sources 5 -> 7. Content hash `05070f1d...` -> `5db37614...0d2c1d`. The counts are equal but the hash changes, so only the hash and the file bytes show that a release changed, not the counts.
- Two derived, sha-locked sources under `content/sources/`, with their provenance in `SOURCES.json`. Ids and names are SM's own English strings (no help text, no vendor marks).
- The secret scan of rendered document text has its own function (`renderedTextCredentialShapes`), and no product code calls it yet. The strict scanner that every input path uses (`credentialShapes`) is built from the same rule expressions as on main.
- Tests: 136 test titles are new compared with a run on main. 3 of them are existing tests renamed because their titles quote counts or a hash that the new release changes. Net: 133 more passing tests than on main.

## Test results on the merged tree (CI image, no network; the withheld SOW text not mounted)
- Renderers project: 33 files, 291 passed, 1 skipped (main: 32 files, 278 passed, 1 skipped). Workspace project: 290 files, 3,028 passed, 2 failed (main: 284 files, 2,908 passed, 2 failed). Passed in all: 3,319, against 3,186 on main.
- Red: the same two rows as on main, both in `packages/content/src/citations.test.ts`: every quoted phrase of every E8 SOW citation is in the SOW text, and its positive control. Both read the SOW text, which is withheld from this run, so both fail. Whether the new release's citations are green is not measured here.
- Database groups: 39 files / 674 tests and 83 files / 1,563 tests, all passed, the same counts as on main.
- Lint, format check, typecheck and build pass. `content:check` and the demo check print "is current" with the hashes above.
- Hosted checks on head `2a58dc5d`; open code-scanning alerts: 0 on this head, 0 on main.

| name | app | status | conclusion | started | completed |
|---|---|---|---|---|---|
| Analyze (csharp) | GitHub Actions | completed | success | 2026-11-20T10:41:20Z | 2026-11-20T10:42:58Z |
| Analyze (javascript-typescript) | GitHub Actions | completed | success | 2026-11-20T10:41:20Z | 2026-11-20T10:44:17Z |
| CodeQL | GitHub Advanced Security | completed | success | 2026-11-20T10:42:47Z | 2026-11-20T10:42:51Z |

## Status
The new content release is NOT cut and nothing is deployed. Two findings ride with the branch: the rendered-text scan can miss a directive that begins inside an exempt label run (no product code calls it yet), and the Q-03/Q-04 plant swap has a test-only gap. Landing is a squash pinned to the reviewed head.
