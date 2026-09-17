SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: Q3 vitest output consumer found for PR-3 (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Your Q3 condition for PR-3 (vitest / @vitest/mocker): run a grep for any harness or report that parses vitest output BEFORE writing the §6 line, and stop and ask if it finds a consumer. It found one.
- Grep (positive control: 134 lines match `vitest.*run` on the same instrument), 5 hits:
  git grep -n -i -E 'vitest.*(--reporter|outputFile|reporters)|(junit|json).*vitest|vitest-report|vitest\.results|test-results.*vitest' -- ':!*package-lock.json' ':!*CHANGELOG*'
  - 4 hits are prose or comments (a .planning doc, the baseline reason text, an analytics Dockerfile comment, a security test's header comment).
  - 1 is a real consumer: systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts:96-100.
- What it does:
  - spawnSync(VITEST_BIN, ['run', '--config', 'vitest.unit.config.ts', '--reporter=default', ...files]);
  - parses vitest's default-reporter summary with /Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)/;
  - throws "could not read the child vitest summary" when the line does not match.
  So a change in vitest's summary-line format would red that suite, loudly rather than silently.
- The move in that tree: systemTest/performance lock vitest 4.1.10 -> 4.1.11 (declared ^4.1.10), a patch. The same patch lands in 26 other locks + root. It is the vitest.unit.config.ts run of this one suite that reads the format.
- The harness is systemTest (Peter's area). My write scope stays locks only; no test file changes.

QUESTION
How should PR-3 treat this consumer?
(a) (recommended) Keep vitest in PR-3, and add to its evidence a run of that suite on the bumped lock: host `npm ci` in systemTest/performance (an install, not a lock write) plus `npx vitest run --config vitest.unit.config.ts tests/unit/utils/unitSuiteSlotIndependence.test.ts`. Record the child summary line it parsed, and write the §6 line as "1 consumer found (file:line); exercised on 4.1.11, parsed OK". If the parse fails, STOP and STATUS.
(b) Leave systemTest/performance's lock out of PR-3. That leaves GHSA-82fw present in that lock, so the row cannot be removed.
(c) Other.

MEANWHILE
PR-1 (hono) suites are running; its push follows. PR-3 does not start until PR-1 merges.

NEEDED-BY
Before PR-3 starts (after PR-1's merge).

Seat B
