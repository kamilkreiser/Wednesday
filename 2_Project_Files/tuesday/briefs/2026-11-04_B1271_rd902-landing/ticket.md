# Title (at most 100 ASCII chars)
RD-902 follow-up: add a test cell for the read-path sync when first run is not complete

# BLUF
The read-path sync on GET /api/risk-conditions (landed under RD-902) has one decision input that no committed test pins: whether the first run is complete. A test cell is missing. The fix is one test cell and no product change.

# Severity
Major, restrictive direction, as graded by the round-2 gate (the review cap). The product owner ruled on 2026-11-04 to land RD-902 with this gap ticketed.

# The failing cell (as the gate measured it)
Missing cell, in the gate's words: "MK1 - in the open window with users present and sign-in configured, the existing check still passes for everyone: an anonymous read syncs".

Mutant that survives: in the twin riskConditionAdminPasses (backend/server.js, the getFirstRunStatus input of the twin, at line 20993 at the gate's head bcdf835f) the line is changed to
`const firstRunComplete = (await getFirstRunStatus(), true);`
Evidence:
- Equivalence census: 24 of 1008 cells diverge, all restrictive, all on the row where first run is not complete, users exist, sign-in is configured and the reader is not an administrator.
- 219 of 219 tests pass with the mutant in the run set (the ten rd902 cells, the funnel guard, five route neighbours); 180 of 180 pass in ten more files that touch risk conditions or firstRunComplete. 399 tests in 17 files, none red.
- Over HTTP (harness servers on 127.0.0.1, temporary data directories; tenant and client set, an administrator and a viewer in the user list, firstRunComplete not set): an anonymous GET and a viewer GET sync at head and at main in open access, and a viewer GET syncs with enforcement on; with the mutant none of the three syncs. The writers' own POST /api/risk-conditions/sync admits the same readers (200, store changed). So the read would refuse a reader the writers admit.
At head and at main the new cell would be green; with the mutant it would be red at the store assertion.

# Fix shape (test only, no product change)
In __tests__/rd902-risk-conditions-get-sync-admin-only.test.js add one cell shaped like O1: boot open with the settings list, tenant and client set; add an administrator and a viewer; leave firstRunComplete unset; plant the store; read anonymously (and, if wanted, as the viewer) and assert the store gains the settings row. Assert the premise inside the cell: the anonymous POST /api/risk-conditions/sync answers 200, so the writers' check passes for this reader. Then run the mutant above and confirm the new cell, and only it, turns red. The expected-counts file moves by one test (regenerate it once, never edit it by hand).

# Not measured
Whether the real setup flow produces this state (users and sign-in saved before first run is marked complete). The gate planted it directly, as round 1 did for its restrictive survivor.

# Related notes from the same gate (not blocking)
- backend/server.js:462 still says "the eight admin gate sites" (stale comment; nine call sites now).
- The first commit message sentence "Any other reader gets the same answer" is true only once the store already holds the synced rows; the same message discloses the difference.
