## Summary
The dev-tooling dependency audit fails on a new high advisory, GHSA-fc5q-39xc-vjpf (picomatch `<=4.0.7`). No patched version exists. This change adds ONE dated exception for exactly that advisory, under the product owner's 2026-11-18 ruling (a narrow, dated exception for this advisory only, lapsing 18 Dec or on a fix). The last allowed day is 2026-12-18 (Australia/Sydney). The audit fails again from 19 Dec. The production audit step is unchanged. Nothing is deployed.

## What changed (three files)
- `web/scripts/audit-dev.mjs`: the header comment, plus one entry in the frozen exception list (id GHSA-fc5q-39xc-vjpf, package picomatch, range `<=4.0.7`, last day 2026-12-18). `evaluate()` and everything below the list are unchanged.
- `web/src/audit-dev.test.ts`:
  - The row that pinned the empty list now pins the one entry.
  - Five new rows test the shipped entry:
    - allowed to the end of 18 Dec in Sydney;
    - lapsed on 19 Dec in Sydney (still 18 Dec in UTC);
    - any other advisory still fails;
    - a different range or package stops the entry applying;
    - the old braces advisory is no longer allowed, and a note asks for the entry's removal once the advisory is no longer reported.
  - The zod row passes an empty list on purpose.
  - The synthetic test exception is cast to the list's element type so the file typechecks. This is type-only.
- `.github/workflows/ci.yml`: only the comment above the dev-tooling audit step changes. The step names and `run` lines are unchanged.

## Why
- npm's latest picomatch is 4.0.7, and the advisory has no first patched version. There is nothing to upgrade to.
- picomatch is reached only through dev tooling (vite, vitest and the eslint toolchain). The production audit finds 0 vulnerabilities.
- npm's suggested "fix" is a vitest downgrade. It was not taken. No dependency or lockfile changed.

## How it was verified
- Real audit step at main: exit 1 on this advisory alone (npm audit counts high 17, one advisory object).
- Real audit step with the entry: exit 0, with exactly one ALLOWED line.
- Copies of the script with a planted last day (2026-11-17), a wrong id, a wrong range or a wrong package each exit 1.
- Sydney boundary on the real report:
  - allowed through 2026-12-18T23:59:59+11:00;
  - failing from 2026-12-19T00:00+11:00;
  - failing from 2026-12-18T13:00Z, which is already 19 Dec in Sydney.
- A second high or critical advisory beside it, in another package or on picomatch itself, still fails.
- The new and replaced test rows fail without the entry (6 failed, 40 passed) and pass with it (46 passed).
- Unit tests: 304 files, 4340 passed at main; 304 files, 4345 passed, 0 failed, 0 skipped with this change (by title: 1 replaced, 5 added).
- Lint and typecheck pass.
- Infra checks pass: the hidden-characters scan (14 tests), the whole infra suite (325 tests) and the template validation.
- The production audit output is byte-identical before and after.
- A local CodeQL JavaScript scan of the two changed script files finds 0 results.
- Not run locally: the build and the end-to-end shards.

## Lapse
The exception lapses after 2026-12-18 (Australia/Sydney). It also stops applying if npm reports the advisory with a different range. It is not extended without a new ruling. If npm stops reporting the advisory, the audit prints a note to remove the entry. That note is not a failure.

Nothing deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
