## BLUF
This branch strengthens one test. The plant check of the Q-03/Q-04 scan test now exercises every alternative of its middle pattern, so dropping the generic Constraint or Compare alternative turns that test red (before, both left the file green). It changes one test file, no content release, no product code, and nothing deploys from it.

## What changes (one file, 17 lines added, 4 removed)
- `packages/content/test/b330-sm316-qgate.test.ts`: the pattern factory takes an optional fourth argument, `morePlants` (default empty, so every other pattern behaves as before); the middle pattern passes two extra plants (one per generic alternative, the existing plant stays for the distinctive one); the plant check loops over all plants, and the fragment check covers the new plants too. No new plant spells a scanned name whole (the file scans itself and passes).

## Limits
- Two other alternations in the same file, (True|False) and (png|svg|jpg), have the same shape and are left as they were; each is a follow-up of its own.
- A future alternative of the middle pattern needs its plant added by hand; the mutant that drops it shows the gap.

## Test results (CI image, no network; the withheld SOW text not mounted)
- The file: 10 passed (10), unchanged count and names.
- Mutants of the file, base then head: drop the Compare alternative green then RED; drop the Constraint alternative green then RED; drop the distinctive alternative RED both; a sibling alternation (True) green both.
- Renderers project 291 passed, 1 skipped; workspace project 3,041 passed, 2 failed: both equal to main, test names lost 0 added 0. The 2 failures are the same two rows in packages/content/src/citations.test.ts as on main (they read the withheld SOW text).
- Lint, format check, typecheck and build pass; content:check prints "is current" with the release-draft hash unchanged. Both CONTENT_HASH files, release-draft/bundle.json and content/sources/SOURCES.json are byte-identical to main.
- Hosted checks: read at landing.

## Status
Test-only. No release, no deploy.
