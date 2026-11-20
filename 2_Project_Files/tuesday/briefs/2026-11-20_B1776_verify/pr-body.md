## What changes

**RD-1011: four data-source routes now refuse a signed-in non-administrator**

These four routes make the server use a data source's stored sign-in details to connect to the Log Analytics workspace:

- `POST /api/data-sources/:id/test`
- `GET /api/data-sources/:id/describe-table`
- `GET /api/data-sources/:id/discover-tables`
- `POST /api/setup/data-sources/:id/test`

Before this change, once sign-in was enforced, any signed-in viewer could call all four. The server would then decrypt the stored source, try to sign in to the identity provider with the stored details, and return what came back. That was connection diagnostics on the two test routes, the table list on discover-tables, and the schema and sample rows on describe-table.

Now each handler runs the project's existing setup-mode-aware administrator check (`requireAdminFor`) as its first statement. A signed-in non-administrator gets `403 {"error":"Admin access required"}`. That text is the check's existing answer, so nothing new is shown to users. The refusal happens before the server reads the stored source and before any outbound connection.

What stays the same:

- An administrator gets the same answers as before.
- The first-run wizard keeps working. While setup is unfinished, or while no sign-in is configured (the open window), the check refuses nobody.
- A request with no session is still refused 401 by the sign-in check.

The two test routes come off the permission table's pending list. The role inventory and its page are regenerated with the project's own tool: four rows change, and in each one only the viewer status (now 403), the handler gate and the capability text differ.

**The two read routes: an open question.** Closing describe-table and discover-tables to a viewer is the coordinator's default, not a product decision. RD-1011 asks the product owner whether those two reads must stay open to a viewer, and that question is still open. Reversing it means removing the one check statement (and its two comment lines) from each of the two read handlers and regenerating the inventory. Until it is decided, the permission table still gives those two routes `config.read`, a capability a viewer holds, so the table and the wire disagree on those two rows.

**RD-1012: the audit path is the pathname only**

The refused-request row and the state-change row now record only the pathname of the request target. An absolute-form target (a full address in the request line) no longer puts its scheme, host, port or user-info into the path field, and a raw `#` cuts the path. Percent-encoded text is recorded as sent, never decoded, and dot segments are not resolved. That is also the coordinator's default. A plain path, a path with a query string, and a request handled outside any router are recorded as before.

**RD-1013: the provisioning refusal entry records the full path**

The sign-in provisioning router's own refusal entry (`entra_provisioning_forbidden`) used to record the path relative to the router, such as `/` or `/test`. It now records the full path and the method through the same helper as the shared rows.

## Tests

- Three new test files with 47 cells:
  - The first boots the real server with an outbound-connection fence. A viewer must get 403 with 0 connection attempts on each route. An administrator's call is the control and must count at least one attempt.
  - The second covers the audit path, including raw requests on the real server.
  - The third covers the provisioning entry.
- Four existing tests that counted check calls, read the pending list or kept a hand list of gated routes now expect the new answer. No cell was added or removed.
- Before merging, an independent review checked all of this:
  - It ran the full verify on Node 24.
  - It reproduced the red cells against the old code.
  - It planted mutants.
  - It drove the four routes with every non-administrator session shape it could seed (wrong-case and array roles, an empty or missing role, a user who is not in the store). The variants were trailing slash, upper case, method-override header and query, HEAD, absolute-form target and a non-numeric id. None of them reached the handler or made a connection.

## Not tested

- The hosted Build and CodeQL on the merge commit.
- The hosted CodeQL reading of two existing alerts whose region covers the setup test handler. The local comparison passed, and an earlier pull request with the same shape passed the hosted check.
- Linux.
- A hosted instance.
- The first-run wizard in a real browser.
- A real workspace or identity provider. The connection attempts are counted at a fence, not answered.
- Two sibling routes still let a signed-in viewer make the server use stored sign-in details. Neither is in these tickets, and both are follow-ups:
  - `GET /api/setup/data-sources` runs a live connection test for every enabled source.
  - `GET /api/debug/data-sources` decrypts every non-primary source and queries it for a sample.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
