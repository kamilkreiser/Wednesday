# For the records seat (after the PR lands; nothing here is filed by the gate)

Gate result: GO WITH FINDINGS at 8af88ee on main b169b8a (round 1 of 2). Not deployed.

## The three tickets (all To Do, 0 comments, read whole by Jira GET at the gate)
- **RD-1011**: move to Testing after landing.
  - Sentence: a signed-in non-administrator is refused 403 with the check's existing text on POST /api/data-sources/:id/test, GET .../describe-table, GET .../discover-tables and POST /api/setup/data-sources/:id/test, before the server reads the stored source or makes any outbound connection. An administrator, the first-run wizard and the open window are unchanged. The two test routes left the pending list, and the role inventory and its page were regenerated.
  - The gate measured 0 connects and 0 decrypts for 9 non-administrator session shapes and 13 path, method and target variants per route.
- **RD-1012**: move to Testing after landing.
  - Sentence: the refused-request row and the state-change row record the pathname only. An absolute-form target loses its scheme, host, port and user-info, and a raw # cuts the path. Percent-encoded text is recorded as sent and no dot segment is resolved (a default of the coordinator).
- **RD-1013**: move to Testing after landing.
  - Sentence: the provisioning router's refusal entry (entra_provisioning_forbidden) records the full path and the method through the same helper, on the router's base path and on sub-paths.

## The open question (keep it open on RD-1011)
- Must the two read routes (describe-table and discover-tables) stay open to a viewer? It is the ticket's question to the product owner, and it is unanswered. The landed behaviour (refused) is the coordinator's default, not a ruling.
- Reversal: remove the check statement and its two comment lines from each of the two read handlers (6 lines), regenerate the inventory (two rows) and adjust the counts in rd793 C2 and rd988 T7 and rd978's hand list.
- Until it is decided, the permission table (backend/services/capabilities.js:155-156) still gives both reads config.read, a capability a viewer holds, so the table and the wire disagree on those two rows. The RD-929 role design is where that is settled.

## Sibling routes found (not in these tickets; suggest new tickets)
1. **GET /api/setup/data-sources** (backend/server.js:17162 at the landed head) runs a live connection test with the stored sign-in details of every enabled source. With two sources, a signed-in viewer gets 200 and the server makes 2 connects and 2 decrypts. Same class as RD-1011, and the same answer before this change.
2. **GET /api/debug/data-sources** (server.js:18392) decrypts every non-primary source, builds a client and queries 5 rows. With a non-primary source, a signed-in viewer gets 200 with 1 connect and 1 decrypt. The body carries hasDecryptedSecret, workspaceId and authMode, plus a sample record (user name, printer host name) when the query succeeds. The permission table gives it config.read (capabilities.js:156), on the same line as the two reads.
3. Not measured with a primary workspace configured (they read 0 connects in a boot without one): GET /api/setup/discover-tables, GET /api/log-analytics/test, GET /api/log-analytics/status, GET /api/service-check and GET /api/setup/validate-all. All are viewer 200 in the inventory and use the stored primary-workspace configuration (read at source). This is a candidate for the same review.

## Audit sinks still recording the router-relative path (the RD-1013 class)
- backend/services/scimProvisioning.js:120 (scim_rate_limited) and :156 (scim_auth_failed), inside the router mounted at /scim/v2. Suggest one follow-up ticket.
- Not in the class (they run at app or route level, so req.path is already the full path): server.js:1627 (a log line), :2582 (auth_state_unknown_denied), :22518 (a log line) and backend/services/aiEnabled.js:299.

## Follow-ups
- A cell that counts the stored-source read (decrypts) for a refused caller. The committed cells count outbound connects only: a check moved below getDataSourceDecrypted is caught only by the source-text cell.
- A cell with a non-viewer, non-administrator role value (for example a wrong-case "Admin"): the committed cells test the role viewer only.
- A design note on the setup window: after an administrator resets first run (POST /api/setup/complete-first-run with completed false), every signed-in viewer passes every requireAdminFor check until first run is completed again. Measured on a real server in that state.
- The stale comment line above pathnameOf (backend/services/accessAudit.js:48).
- Four stale remote heads with no pull request ever (two b1480/* from 2026-11-10, two *-s59 from 2026-09-14): candidates for clean-up by whoever owns branch hygiene.
- Watch the hosted CodeQL result on the PR for alerts 67 and 68 (their region at the setup test handler holds the three added lines; one precedent passed).
