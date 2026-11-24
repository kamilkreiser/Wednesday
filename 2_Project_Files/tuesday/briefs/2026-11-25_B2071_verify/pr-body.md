## What this changes

The admin page's Data Sources tab loads the setup list, `GET /api/setup/data-sources`. That route decrypts each enabled source's stored sign-in details and runs a connection test with them. Since RD-1021 it refuses a caller who is not an administrator with 403, so that caller saw an error box reading `HTTP 403` where the list should be.

The tab now handles that 403 by loading the plain list, `GET /api/data-sources`. The plain list reads the stored list only: it runs no connection test and decrypts nothing. The tab shows one card per source with three things only:
- the source name, through the page's own `escapeHtml`;
- the `primary` mark;
- the `disabled` mark.

There is no connection status, no identifier and no action button. An administrator's tab is unchanged in the configured, enforced state. Any other failure of the setup list (401, 404, 429, 5xx, a network error) still shows the error box and requests nothing else.

**The fields a card shows (name and the two marks, nothing else) were chosen by the coordinator**, within the product owner's 2026-11-24 ruling on RD-1021. That ruling chose "a viewer-safe list as a follow-up", served from the route that never connects. It did not choose the fields. Adding a field later means one line of `renderViewerSourceCard` and one test cell.

**Still open: what the plain route returns (not changed here).** This change narrows what the tab shows. It does not narrow what `GET /api/data-sources` (or `/:id`) returns. Every signed-in session still receives every stored field of every source except the secret, which reads `***`. That includes the workspace, tenant and client ids, the endpoint, the table, vendor, region and department. Narrowing the route is a separate decision. The dashboard's region filter also reads this route (`static/js/index.js`).

## The result for the ticket (from the test cells)

- **Before (main `e2911754`):** 7 of 23 new cells fail. These are T1 to T6 and S1. A non-administrator's tab requested only the setup list, showed the `HTTP 403` box and drew no cards. The page had no plain-list branch.
- **After:** all 23 pass.
- **With only the product edit reverted:** the same 7 fail (red-proof).
- **On the real server, at both commits:**
  - Each of the 9 non-administrator roles of the permission table reads `GET /api/data-sources` with 0 outbound connects and 0 stored-source reads, and the made-up secret appears 0 times in the body.
  - A viewer's setup list and debug read are still refused 403, with 0 connects and 0 reads.
  - With no session, the plain list answers 401.
  - The administrator's setup list counts at least one read and one connect. This is the control that shows the counters work.
- **On the tab (the shipped functions run against a jsdom document):**
  - A 403 loads the plain list and shows two cards: `rd1036 alpha primary` and `rd1036 beta disabled`.
  - None of 12 other stored values appears on a card, and the cards have no button, code or link.
  - A name holding markup shows as typed and creates no element.
  - An empty list and a refused plain list each show their own message.
  - The administrator's card is unchanged, and a 500 or a network failure still shows the error box.

## Files (3 files; two commits: the change, then the suite counts written by the project's own command)

- `static/js/admin.js`: 27 lines added, none removed. One branch in `loadDataSources` and two new functions, `loadViewerDataSources` and `renderViewerSourceCard`. All added text is ASCII.
- New: `__tests__/rd1036-viewer-data-sources-list.test.js` (23 tests).
- `scripts/verify-expected-counts.json`: changes from 6300 / 397 to **6323 / 398**, written by `npm run verify -- --maxWorkers=2 --update-counts`.

No server route, handler, permission-table row or inventory row changes, so the role inventory was not regenerated.

## Verification

- Full verify, run at both commits: `VERDICT: PASS`, 6323/6323 tests across 398 suites, `EADDRINUSE` 0. An independent re-run at the head read the same result.
- Local CodeQL (javascript-security-extended), main against head: results 29 / 29, NEW 0, KEPT 0, `rc 0 PASS`.
- gitleaks over the whole diff and the commit messages: no leaks found. The control fired.

## Not in this change (named)

- What `GET /api/data-sources` and `GET /api/data-sources/:id` return to a non-administrator (above).
- The sign-in-unproven state. There the setup list's check refuses everyone, administrators included, so an administrator's tab shows the plain cards instead of the `HTTP 403` box. Nothing more is shown than the route already returns to that caller.
- The setup list leaves out disabled sources, but the plain list includes them. So a non-administrator's tab lists disabled sources, with the `disabled` mark, that an administrator's tab does not show.
- RD-1022's routes and the open first-run window: their own tickets.
- Not tested: a real browser on the admin page, a hosted instance and its content security policy, the open first-run window, the sign-in-unproven state on a running server, Linux, and the hosted Build and CodeQL on the merge commit.

## Deploy

None. Merging starts a `Deploy demo` run, because `static/**`, `__tests__/**` and `scripts/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'`, and the deploy job also needs approval from a required reviewer on the `demo` environment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
