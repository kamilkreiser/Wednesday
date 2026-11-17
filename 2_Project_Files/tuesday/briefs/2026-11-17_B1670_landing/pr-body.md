## What changed

- **Role table row note.** The row for the internal feedback action route (`POST /api/feedback/:id/coordinator-action`) in `docs/ROLE-CAPABILITIES.md` and `docs/role-capabilities.json` now says why the route keeps its own caller check: the check is in the handler and is reached after the sign-in check; the route answers 403 unless the request comes from the loopback address or carries the shared coordinator header value; no page calls it; it was kept as it is by the product owner's 2026-11-16 ruling on RD-992.
- **Pending list.** The route is no longer on the list of routes owed an administrator check (`PENDING_GATE` in `backend/services/capabilities.js`). A new frozen export, `OWN_CALLER_CHECK`, names it. The route stays in `feedback.manage` in the table.
- **Generator.** `scripts/role-capability-inventory.js` writes the note from a closed map (`ROW_NOTES`). The two docs files were regenerated with the project's own command, `node scripts/role-capability-inventory.js --generate`. One row and the two generation clock lines changed; the other 202 rows are the same.
- **Tests.** The census in `__tests__/rd929-capability-design-census.test.js` excuses exactly the routes in `OWN_CALLER_CHECK`, and one new cell there pins the excused list, the pending state and the exact note. `__tests__/rd988-feedback-triage-admin-only.test.js` now pins that the route is NOT on the pending list.
- **Counts.** `scripts/verify-expected-counts.json` goes from 5867 to 5868 tests in 377 suites, one new cell.

No route, status, handler, middleware or workflow changed. Nothing in `backend/` reads the role table, so no request is answered differently.

## Why

RD-992 asked whether this route should take the administrator check or keep its own caller check. The product owner ruled on 2026-11-16 to keep its own check. RD-995 carries that ruling into the role table: the note says why, and the route leaves the pending list.

## How it was verified

- An independent review in a fresh clone checked the diff: exactly these seven files, ASCII only, no skipped or focused tests, no timers, `decide()` unchanged byte for byte.
- The 14 test files that read the role table or the pending list pass at the head (70 cells).
- Red-first. At the first commit with the new cell added and the docs not yet regenerated, the new cell is the only failure. With the route put back on the pending list, the census cell, the new cell and the triage test cell all fail. With the exception list emptied, the census cell and the new cell fail.
- Running the generator again into a scratch folder writes the same note.
- `npm run verify -- --maxWorkers=2` at the head printed `VERDICT: PASS` with 5868 tests in 377 suites, equal to the committed counts.
- Not covered yet: Node 24 and Linux (the hosted Build covers both) and CodeQL on this pull request.

## Known limit, not changed here

With sign-in enforced, the sign-in check answers 401 before the route's own check runs. The route is not in the machine-to-machine exemption, which names only `/api/coordinator-state`. A headless caller that holds only the shared value therefore cannot reach the route on such a deployment. A separate ticket for a decision follows this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
