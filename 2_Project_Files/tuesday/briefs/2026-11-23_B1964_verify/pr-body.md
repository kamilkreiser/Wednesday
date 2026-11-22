## What this changes

The permission table in `backend/services/capabilities.js` (the design note the Roles UI work will wire, RD-929)
listed two data-source reads under `config.read`, a capability the viewer role holds, while the server refuses a
signed-in viewer on both with 403. This change moves the two rows so the table and the wire agree.

| route | before | after | the wire (unchanged) |
|---|---|---|---|
| `GET /api/data-sources/:id/describe-table` | `config.read` (viewer holds it) | `admin.read` (only the administrator role holds it) | administrator check first; viewer 403 once sign-in is set up and first run is complete |
| `GET /api/data-sources/:id/discover-tables` | `config.read` (viewer holds it) | `admin.read` (only the administrator role holds it) | the same |

- `backend/services/capabilities.js`: the two rows leave the `config.read` block and join the end of the `admin.read`
  block under a two-line comment. No other row, role or export changes. No backend, page or script code reads this
  table, so no response changes.
- `__tests__/rd1011-four-routes-administrator-only.test.js`: cell P2 now expects `admin.read` for both reads and that
  the viewer role does not hold `admin.read`.
- `__tests__/rd929-capability-design-census.test.js`: two cells. The first is the opposite case of the pending list:
  every route the committed inventory refuses a viewer on must map to a capability the viewer role does not hold. It
  fails before this change on exactly these two rows. The second runs the same comparison over a synthetic table with
  one row put back under `config.read` and proves the comparison can fail.
- `scripts/verify-expected-counts.json`: 6237 tests in 394 suites, written by the project's own `--update-counts`.

The route inventory (`docs/role-capabilities.json`) and its page are unchanged: they record the wire, which this
change does not touch. The rows of RD-1021 (`GET /api/debug/data-sources`) and RD-1022 (the setup reads) stay under
`config.read`.

## Who decided

The 2026-11-20 ruling on RD-1011 (C-311) keeps both reads administrator-only and says the permission table is to be
brought into line with it. Moving the rows to the existing `admin.read` (rather than a new capability) and placing
them at the end of that block are the coordinator's defaults.

## Independent check

- With the new test cells and the table unchanged, the two test files read 2 red of 36 (the new opposite-case cell,
  which received exactly the two routes, and P2, which received `config.read` twice); with the table change, 36 of 36.
- The 21 test files that read the table or the inventory: 284 of 284 green.
- Mutations of the table: either row put back, the sibling debug row moved, the viewer given `admin.read`, a row
  dropped: each turns the expected cells red. Putting the two rows under a different capability the viewer lacks reds
  P2 alone, and a drift of the committed inventory reds four cells.
- For every route, the table's decision for a viewer, an administrator, a caller with no session and the open setup
  window was compared with the committed inventory: the change removes exactly these two disagreements for the viewer
  and adds none in any mode.
- Local CodeQL comparison at this head: no new and no kept high-severity result.

## Not changed, listed

- The `about` text of `admin.read` does not name data-source reads.
- The RD-1011 test's header still calls refusing all four routes the coordinator's default; for these two reads it is
  now ruled.
- Only the viewer role is pinned not to hold `admin.read`; the proposed roles, which no user can hold yet, are not.

## Not tested

- The hosted Build and CodeQL on the merge commit; Linux.
- The later wiring of the table (RD-929).
- The Deploy demo run a merge starts, which must read skipped.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
