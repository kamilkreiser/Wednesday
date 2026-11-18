## What changed

The production dependency audit (workflow `npm-audit`, check `audit-production-deps`) has failed on every run since 2026-11-17 (UTC) because of one advisory, GHSA-fc5q-39xc-vjpf in `picomatch` (ReDoS, high). It reaches production only through the `sqlite3` install tooling (`sqlite3` -> `node-gyp` -> `tinyglobby` -> `picomatch`). No patched `picomatch` exists yet: 4.0.7 is the newest release and it is affected.

The product owner's 2026-11-18 ruling allows this one advisory, in this repository's production audit, until 18 Dec 2026 or until a fix ships, and nothing else. This pull request makes that ruling executable:

- `scripts/audit-prod.js` (new) reads the `audit.json` that the step already writes and decides. Every moderate, high or critical advisory fails the step, except one entry: advisory GHSA-fc5q-39xc-vjpf, on package `picomatch`, at the range text `<=4.0.7`, last allowed day 2026-12-18 (Australia/Sydney).
- `.github/workflows/npm-audit.yml`: the same `npm audit --omit=dev --audit-level=moderate --json` command still runs; its exit status is no longer the verdict, the script's is (`set -e`, then `node scripts/audit-prod.js audit.json` as the last line). The job id and the check name `audit-production-deps` are unchanged.
- `__tests__/audit-prod-dated-exception.test.js` (new): 11 cells covering the shipped entry, the real report, the Sydney day boundary, every other advisory failing, the range and package match, the fail-closed shapes, the exit codes and the workflow text.
- `scripts/verify-expected-counts.json`: 5870 tests in 377 suites -> 5881 in 378 (the 11 new cells and the one new suite).

## When it lapses

- On the date: allowed through the end of 18 Dec 2026 in Sydney; from 00:00 on 19 Dec (Sydney) the audit fails again by itself, with a message saying the exception lapsed.
- On a fix: if npm reports the advisory with a different range text or on another package, the entry no longer matches and the audit fails. If a patched `picomatch` is published while the advisory keeps the range text `<=4.0.7`, the entry keeps allowing it until 18 Dec, so the advisory and `npm view picomatch dist-tags` must be re-checked before then.
- When npm stops reporting the advisory, the audit passes and prints a NOTE asking for the entry to be removed.
- Extending past 18 Dec needs a new ruling; it is not an edit to make on its own.

## How it was verified

- Real `npm audit` on this branch: npm itself still exits 1 (the advisory is still reported); the step's command exits 0 with exactly one ALLOWED line for this advisory.
- On that real report, with planted changes: a second advisory on another package fails (moderate, high, critical; a low one does not block); a second advisory on `picomatch` itself fails; a different range text or another package fails; 23:59 on 18 Dec (Sydney) passes, 00:00 on 19 Dec (Sydney) fails, and a UTC instant that is still 18 Dec in UTC but 19 Dec in Sydney fails.
- Fail closed: an empty file, unparseable text, a missing file, an npm error object, a report version other than 2, and a missing or non-object `vulnerabilities` key all fail. The step body, run under the runner's shell flags with a stubbed npm that crashes before writing any JSON, exits 1.
- The new test file is red without the change (empty exception list: 8 of 11 cells red; the old workflow: the workflow cell red) and 11 of 11 green with it.
- Full suite: `npm run verify -- --maxWorkers=2` passes with 5881 tests in 378 suites, equal to the committed counts.
- CodeQL (JavaScript code-scanning suite) over the two new JavaScript files: 0 results.

## Not deployed

Nothing is deployed by this pull request. Merging to main starts the demo deploy workflow as every merge does; its jobs are gated off by the repository's deploy switch and have read skipped on recent merges.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
