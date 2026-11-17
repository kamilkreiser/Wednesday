## What changed

Test files and the expected test counts only. No product file, helper, script or workflow changed.

- **Tamper check (RD-998).** The harness check that decides whether the settings-store tamper landed inside the token exchange compared two clock readings with a strict less-than, the shape that failed one hosted run of its sister check (RD-991). It now orders the two events by the file's own counter, so a one-millisecond tie cannot fail a correct run. Four new cells (W1 to W4) hand the check results built by hand: a tie with the tamper first passes; a tie with the tamper second, a later tamper, and a missing answer stamp each throw the harness error.
- **Shared body check (RD-985).** One new cell (H8) sends the business-hours write with no content type and no body. That is the one request whose body stays undefined, so it is the one cell that can tell the shared body check apart from a check that always says yes. The comment above the two older body cells now says what they can and cannot tell apart.
- **Two cells that said more than they checked (RD-996).** The second host-match unit cell compared the test table's own columns and called no code; it now runs the helper on every row (and ends in a strict comparison, because the plain one ignores the `undefined` row). The department-keyword cell title now says what its expectations show.
- Expected test counts move from 5862 tests in 377 suites to 5867 in 377: five new cells, no new suite.

## Why

Each is a small gap an earlier review recorded: a check that could fail a good run on a clock tie, a cell that could not go red under the change it was meant to catch, and two cells whose names or bodies overstated what they checked.

## How verified

- Plain `npm run verify -- --maxWorkers=2` at this head in a fresh tree: `VERDICT: PASS`, 5867 of 5867 tests across 377 suites, equal to the committed pair.
- Red-first on copies, each reverted afterwards:
  - W1 goes red when the old strict clock comparison is put back.
  - The three server cells that call the tamper check go red when the tamper's order stamp is removed.
  - With the shared body check forced to return true, H8 goes red (status 500 instead of 400) while the two older body cells stay green.
  - The host-match cell goes red when the helper's answer is flipped, on every one of the 14 table rows, including the `undefined` row.
- The diff is exactly the four test files plus the counts file; no skipped, only or todo cells, no timers, no new regular-expression construction; gitleaks over the diff and history found nothing.

Not tested here: the hosted Build on Node 24 and Linux, and a real one-millisecond tie end to end.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
