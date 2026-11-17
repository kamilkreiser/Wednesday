**BLUF.** Moves the web app's `next` from 16.4.2 to 16.4.5, the first release outside the range of advisory GHSA-mfr8-8qww-v76h (16.3.0 to 16.4.4). The registry audit goes from 1 moderate vulnerability to 0. No code changed. Nothing deployed; no integration with HP tools.

## What changes
- `web/package.json` line 20: `"next": "16.4.5"` (was `16.4.2`; still an exact pin). One line.
- `web/package-lock.json`: exactly 11 entries move to 16.4.5, with their resolved URLs and integrity hashes: `next`, `@next/env`, the eight `@next/swc-*` binaries, and the root entry's `next` reference. Nothing is added or removed (80 changed lines).
- Not touched: `eslint-config-next` (stays 16.3.6), any code, config, test or workflow file.

## Why
The pinned 16.4.2 sat inside the advisory range (information disclosure when a `use cache` function is called through `unstable_cache`). The app does not use that cache feature (0 files match the cache family), but the release is in range and two dependency alerts are open; they close once this lock is on main.

## Measured, before and after (same machine, local builds)
| | main (16.4.2) | this change (16.4.5) |
|---|---|---|
| registry audit, whole | 1 moderate (next, GHSA-mfr8-8qww-v76h) | found 0 vulnerabilities |
| `npm audit --omit=dev --audit-level=high` / dev audit | exit 0 / exit 0 | exit 0 / exit 0 |
| vitest | 304 files, 4339 passed, 0 failed | 304 files, 4339 passed, 0 failed (no test lost, added or changed) |
| e2e, all 8 shards (CI settings) | 972 passed, 0 failed, 0 flaky, 48 skipped | 972 passed, 0 failed, 0 flaky, 48 skipped |
| lint, typecheck, build, shard plan | exit 0 | exit 0 |
| build notice | first build stopped once with the framework's security notice | first build passed, no notice |

A planted copy of the lock at 16.4.4 makes the same audit print the moderate finding again, so the instrument can see the range.

## Not done here
No deploy (the deployment of this version is a separate decision after the merge). The deploy-package script cannot complete on a Mac (it requires Linux x64 native modules; identical refusal at main), so that step is left to hosted CI.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
