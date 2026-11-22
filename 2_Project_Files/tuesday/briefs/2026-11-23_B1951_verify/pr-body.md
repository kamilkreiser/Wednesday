## BLUF
This branch adds a DRAFT data file of default values per template row, with a README and one test. It changes no content release and no product code, and nothing deploys from it. The file is derived from the records template and crosswalk (cited by path and sha256 inside the file) and the release-draft bundle at main, and it was independently re-derived at the pushed head.

## What it adds (three files, nothing else)
- `content/baselines/default-baseline.json` (format `pc-baselines/1`, status DRAFT): 132 rows (class, default severity, remediation, unsupported handling, item keys, flags, and for the 28 variable rows the control decision that sets them) and 350 field targets (one per bundle field a row takes, with the rule that gave the target).
- `content/baselines/README.md`: the keys, the rules, the flag and basis legends with counts, and the limits.
- `packages/content/test/b1948-cw2-baselines.test.ts`: 12 cells that pin the shape, the closed sets, the setters, the keys against the bundle, the targets, the absence of any sentence, and the counts.

## Limits (as built)
- Only 4 of the 34 boolean fields carry a value (2 true, 2 false). 16 sit on variable rows and read "variable"; 14 wait for a reading of the template, which this change does not do.
- 33 rows carry a remediation state the engine does not have yet, and 21 rows carry a plain-enable value with no mapping: both read null with a flag.
- No sentence of any source is carried. Every string but the title holds no whitespace.

## Test results (CI image, no network; the withheld SOW text not mounted)
- Renderers project: 33 files, 291 passed, 1 skipped, the same as main.
- Workspace project: 3,041 passed, 2 failed (main: 3,028 passed, 2 failed); the 13 added are the 12 new cells and one case the existing canonical-JSON test generates for the new file. The 2 failures are the same two rows in `packages/content/src/citations.test.ts` as on main (they read the withheld SOW text).
- The test alone on main is red on all 12 cells (the file is missing); at this head it is green. Seven of the kit's mutants of the data file, each swapped in and restored, turn named cells red.
- Lint, format check, typecheck and build pass. `content:check` prints "is current" with the release-draft hash unchanged.
- Both `CONTENT_HASH` files, `release-draft/bundle.json` and `content/sources/SOURCES.json` are byte-identical to main.
- Hosted checks: none yet on this head (no pull request until now); the CodeQL result is read at landing.

## Status
Draft data, read by no product code. Later lanes add their own files to the same directory.
