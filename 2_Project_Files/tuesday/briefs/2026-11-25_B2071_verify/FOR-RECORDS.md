# FOR-RECORDS: RD-1036 (records pass, after the landing)

Fill in `<N>` (the PR) and `<M>` (its merge commit) after the landing. Take the Deploy demo line from landing.txt step 4.

RD-1036 at the gate (Jira GET, 02:3x AEDT 25 Nov):
- Status To Do, Task, labels `records-pass-1124,security`.
- Comments: 0.
- Description: 3541 characters, by the seat's GET-only reader.

## RD-1036: result comment

Landed by pull request <N>, merge commit <M>. It is a merge commit of the reviewed head `c1a99d4b`. A is `23b3a023`, the change. K is `c1a99d4b`, the counts.

- **Change.** The admin page's Data Sources tab now handles a 403 from the setup list (`GET /api/setup/data-sources`, administrator-only since RD-1021) by loading the plain list (`GET /api/data-sources`). It shows one card per source with three things only: the name (escaped), the `primary` mark and the `disabled` mark. There is no connection status, no identifier and no action. Only `static/js/admin.js` changed: 27 lines added, 0 removed. No server route, permission-table row or inventory row moved.
- **Measured (the new test file, 23 cells).**
  - At main `e2911754`, 7 cells were red: T1 to T6 and S1. A non-administrator's tab showed the `HTTP 403` box and no list.
  - At the head, 23 of 23 pass.
  - With only the product edit reverted, the same 7 are red.
  - The seat and the G1 gate each measured this, in separate trees.
- **On the real server.**
  - Each of the 9 non-administrator roles reads the plain list with 0 outbound connects and 0 stored-source reads, and the made-up secret 0 times in the body.
  - A viewer's setup list and debug read stay 403 with 0 and 0.
  - No session: 401.
  - The administrator's setup list counts at least 1 read and 1 connect. This is the control that shows the counters count.
- **Verification.**
  - Full verify `VERDICT: PASS`, 6323 tests in 398 suites. The seat ran it at both commits; the gate re-ran it at the head.
  - Local CodeQL: NEW 0, KEPT 0, rc 0.
  - gitleaks: no leaks found.
  - G1 gate B2071: GO WITH FINDINGS.
- **Whose choice.** The product owner's 2026-11-24 ruling on RD-1021 chose option b, a viewer-safe list as a follow-up, from the route that never connects. **The fields a card shows (name, primary, disabled) were chosen by the coordinator, within that ruling.** The ruling did not choose the fields (C-320, "What it does not decide").
- **Still open (Q-0).** This narrows what the TAB shows, not what the ROUTE returns. `GET /api/data-sources` and `/:id` still return 17 stored keys of every source to every signed-in session: `apiEndpoint, authMode, clientId, clientSecret ('***'), created_at, department, enabled, id, isPrimary, name, region, tableName, tables, tenantId, updated_at, vendor, workspaceId`. The gate measured this at the head for all 9 non-administrator roles. See the Q-0 ticket proposal below.
- **Deploy.** None. Deploy demo run for <M>: <build / deploy conclusions, from landing.txt step 4>.
- **Not tested.**
  - A real browser on `admin.html`, a hosted instance and its content security policy.
  - The open first-run window, the sign-in-unproven state on a running server, and Linux.
  - The gate probed hostile names and field values against jsdom. jsdom runs no script written by `innerHTML`, so "no element made" was measured, not "no handler runs".
- **Move.** RD-1036 goes from To Do to the column the records pass uses for a landed lane awaiting acceptance. RD-1021 sat in Testing after its landing; use the same column.

## C-entry proposal (for CLARIFICATIONS.md, after the landing)

> **C-<next>. RD-1036: the Data Sources tab for a non-administrator (landed PR <N>, merge <M>).** The product owner's 2026-11-24 ruling on RD-1021 (option b, C-320) chose a viewer-safe list served from the route that never connects (`GET /api/data-sources`). The coordinator chose the fields inside that ruling: a non-administrator's card shows the source name and the primary and disabled marks, nothing else. The tab takes this path only when the setup list answers 403. Every other failure still shows the error box.
>
> **What it does not decide:**
> - What the route itself returns. That is still every stored field but the secret, to every signed-in session; see the Q-0 ticket.
> - Whether a non-administrator should see disabled sources, which the administrator's own tab omits.
> - What an administrator sees in the sign-in-unproven state, where the shared check refuses everyone, so the administrator also gets the plain cards.

## Q-0: ticket proposal (a new ticket; the coordinator decides whether to file it and whether it goes to the product owner)

**Summary:** Narrow what `GET /api/data-sources` and `GET /api/data-sources/:id` return to a caller who is not an administrator.

**Why (measured by the G1 gate at `c1a99d4b`, the server unchanged since `e2911754`):**
- Both routes register with no handler gate (`backend/server.js` lines 15691 and 15703). `requireAuth` admits every signed-in session whatever its role.
- `backend/services/capabilities.js` puts both routes under `config.read`. But no backend file requires that table: `git grep services/capabilities -- backend` returns 0 files. The table describes access; it does not enforce it.
- Three roles the table says do NOT hold `config.read` (`end_user`, `partner_manager`, `partner_technician`) are answered **200** with the full list. The other six non-administrator roles are answered the same.
- Each source comes back with 17 keys: the workspace id, tenant id, client id, API endpoint, table name, tables, vendor, region, department, auth mode, created/updated times, id, name, the enabled and primary flags, and `clientSecret` as `***`.
- `PUT /api/data-sources/:id` merges the request body into the stored source (`jsonStorage.updateDataSource`). So any field an administrator ever writes on a source is also returned by these routes.
- Nothing is decrypted and nothing connects (0 / 0 for all 9 roles). The exposure is identifiers and settings, not the secret.

**Proposal:**
- Serve a non-administrator only the fields a consumer needs: the tab needs `id`, `name`, `isPrimary`, `enabled`; the dashboard's region filter (`static/js/index.js` line ~4288) needs `region`.
- Keep the full shape for the administrator.
- Add one cell per role, as RD-1021's and RD-1036's files do.
- Decide whether the permission table should be enforced, or the inventory corrected for the three roles above.

**Needs:** the product owner's answer on which fields a viewer may receive. C-320 left this open, and the coordinator chose only what the tab shows.

## Other follow-up candidates (for the records pass to file or fold in; none is decided here)

1. **Disabled sources: a non-administrator sees more than the administrator.**
   - The setup list reads `getActiveDataSources()` (`enabled !== false`, `backend/jsonStorage.js` line 4177), so a disabled source disappears from the administrator's tab. Its `Enable` button can then never be reached from the tab (pre-existing).
   - The plain list reads `getAllDataSources()`, so a non-administrator's tab lists disabled sources with the `disabled` mark. Cell T2 pins `rd1036 beta disabled`.
   - The gate measured it: after an administrator disabled source 2, the administrator's setup list made 1 read and 1 connect (one source), and every non-administrator role's plain list returned 2 sources.
   - Candidate: decide parity, which way is a product call, and fix the administrator's unreachable `Enable`.
2. **Sign-in-unproven state (RD-535).** `adminGateRefuses` returns true for everyone while sign-in is unproven, the administrator included. The gate measured this by calling the exported function: `admin, signInUnproven -> true`. So `requireAdminFor` answers an administrator 403 on the setup list, and the tab now shows the administrator the plain cards with the line "Connection status and source settings are shown to administrators." instead of the `HTTP 403` box.
   - No data beyond what the plain route already returns to that caller.
   - The kit's limit ("none is known") and commit A's "An administrator's tab is unchanged" do not cover this state.
   - Candidate: either accept and record it, or make the tab tell an administrator that the setup list is refused while sign-in is unproven.
3. **Test coverage note.** W1 asserts the 200 answer only for roles that hold `config.read`. For `end_user`, `partner_manager` and `partner_technician` it asserts 0 / 0 / 0 but not the status. The gate measured those three at 200 with both sources. Fold this into the Q-0 ticket's cells.
