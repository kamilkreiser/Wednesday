# FOR-RECORDS: RD-1040 (records pass, after the landing)

Fill in `<N>` (the PR) and `<M>` (its merge commit) after the landing. Take the Deploy demo line from landing.txt step 4. Take the gate line from the first line of VERDICT.md.

**Jira GET at the gate** (10:4x AEDT, 25 Nov; credentials in-process, nothing printed):

| Ticket | Type | Status | Labels | Comments |
|---|---|---|---|---|
| RD-1040 | Bug | To Do | `records-pass-1125,security` | 0 (links 0) |
| RD-929 | Story | To Do | | 2 |
| RD-1036 | Task | Testing | | 1 |
| RD-1021 | Bug | Testing | | 1 |
| RD-1034 | | Testing | | |

## RD-1040: result comment

Landed by pull request <N>, merge commit <M>: a merge commit of the reviewed head `16a29d3a`. A is `a41ed671` (the change and the new test file); K is `16a29d3a` (the counts).

- **Change.** In `backend/server.js`, 19 lines were added and none removed:
  - A five-line RD-1040 comment.
  - `const permissionTable = require('./services/capabilities');`.
  - The nine-line helper `refuseDataSourceReadForRole(req, res)`.
  - One call line as the FIRST statement of `GET /api/data-sources` and of `GET /api/data-sources/:id`, before any store read.

  How the helper decides:
  - With no `req.user` (open mode) it allows.
  - It allows when the stored role is a string, is an OWN key of `ROLE_CAPABILITIES`, and that entry holds `config.read`.
  - Otherwise it answers 403 `{"error":"Data source settings are not available to this role"}`.
- **Whose call.**
  - The product owner ruled on 2026-11-25: refuse the route to roles the permission table excludes, keep the fields for allowed roles, review before merge, nothing deployed.
  - Tuesday's defaults, not the product owner's:
    - Q-0: a role the table does not name is refused.
    - Q-2: the region filter is unchanged.
    - Q-3: the sibling reads are not built.
    - Q-4: the table header is not touched.
    - Q-5: the inventory is not regenerated.
    - Q-6: the 403 body text.
- **Behaviour change to record (Q-0).** A stored role string the table does not name is now refused 403 on both reads; before, every signed-in session was sent the list. The gate measured these shapes on the real server, each 200 at BASE and 403 at the head:
  - Another case or spacing: `' viewer'`, `'viewer '`, `'VIEWER'`, `'viewer\t'`, `'viewer\u0000'`, `'end_user '`.
  - Built-in property names: `__proto__`, `hasOwnProperty`, `toString`, `valueOf`, `constructor`.
  - Non-string stored values: `7`, `{"role":"viewer"}`, `["viewer"]`, `["config.read"]`, `true`.

  Unchanged and answered 200: an empty or missing stored role, `0`, `false`, and a session whose email has no stored user. All of these read as `viewer` through `user.role || 'viewer'` (server.js line 2792).

  Who can hold an unnamed role: the create route `POST /api/auth/users` stores any role string of up to 32 characters that an administrator sends by API. The update route accepts only `admin` or `viewer`. A non-string role can only be written to the store by hand.
- **Measured (new file `rd1040-...`, 21 cells).**

  | Run | Where | Result |
  |---|---|---|
  | Red-first | BASE `40df8493` | 8 red: R1 x3, X1, X3, X4, D1, S1 |
  | Green | head | 21 of 21 |
  | Red-proof | head, `server.js` set back to BASE's blob `a7426b07` | the same 8 red (names compared by program) |
  | 59-suite set | head | 834 of 834 |

  The gate measured all of this in its own dot-free trees, and the seat measured it too.
- **Gate probes (real server, both trees):**
  - **Route spellings.** At the head, `end_user` is refused 403 on 11 forms: `/api/data-sources` with a trailing slash, in upper or mixed case, or with a query string; `/:id` with a trailing slash, an encoded id (`%31`) or upper case; an unknown id; `%00`, `__proto__` and `constructor` as the id; and HEAD on both routes.
  - **Spellings that reach no handler.** `//api/...`, `/api//...`, `/api/data-sources//`, `%2D`-encoded and `;x`/`.json` suffixes answer 404 at both BASE and head, with no stored field. Dot-segment forms answer 400, `rejectDotSegments`.
  - **OPTIONS** answers 200 with an empty body.
  - **TRACE** answers 403 at both BASE and head.
  - **Existence.** An existing and a missing id are each answered 403, and the median times are equal (18.2 and 18.2 ms, n 40), so a refused role cannot tell which ids exist.
  - **User changes end the session.** A deleted user, a user set inactive, and a user whose role was changed by PUT are each answered 401 on the next request.
  - **Audit row.** The `REQUEST_DENIED` row holds `method`, `path`, `statusCode` 403, `reason` `forbidden`, the masked `userEmail` and `userRole`, and no stored data-source value.
  - **Open mode** answers 200 with or without a cookie, as at BASE: by design, the table allows open mode.
- **Verification.**
  - Full verify `VERDICT: PASS`, 6362 tests in 401 suites: by the seat at A and K, and by the gate at the head (behind main 0, so the head is the merge tree).
  - Local CodeQL: NEW 0, KEPT 0, GONE 0 (29/29).
  - gitleaks: none.
  - Gate B2081: <VERDICT line>.
- **Not tested:**
  - A hosted instance, a real identity provider, a real browser on `index.html` and `admin.html`, Linux.
  - The sign-in-unproven state, read only: no session can exist there.
  - The first-run window with sign-in configured, read only: when `authEnforced` is false the global check sets no `req.user`, so everyone is answered, as `decide()` answers open mode and as at BASE.
  - The hosted Build and CodeQL on the merge commit.
- **Deploy.** None. Deploy demo run for <M>: <conclusions, from landing.txt step 4>.
- **Move.** To the column the records pass uses for a landed lane awaiting acceptance (RD-1036 and RD-1021 read Testing).

## Records items that are not this ticket's acceptance

1. **The `capabilities.js` header is now stale.** `backend/services/capabilities.js` line 6 reads `STATUS: DESIGN ONLY. Nothing in the product requires this file yet. No route reads it ...`, and `backend/server.js` now requires the file and reads it on two routes.
   - Dup-check: RD-1034 (Testing) already covers another stale comment in the same file (the about text of `admin.read`).
   - Either fold the header into RD-1034's follow-up or file one small ticket. Docs-only; no behaviour.
2. **The committed inventory under-describes the two rows.** `docs/role-capabilities.json` still reads "any signed-in session ... handler gate: none" for `GET /api/data-sources` and `GET /api/data-sources/:id`.
   - Its four measured modes (anonymous 401, viewer 200/404, administrator 200/404, open 200/404) are unchanged and true.
   - The scanner's `GATE_TOKENS` (`scripts/role-capability-inventory.js` lines 101 to 109) do not know `refuseDataSourceReadForRole`, so the inventory and rd978's gated-handler count do not see this gate.
   - Fold into RD-929 (the table-wide enforcement will need the scanner to know its check), or file it.
3. **Sibling routes still send stored settings to every signed-in role, the excluded roles included.** The gate re-ran them as `end_user` and `partner_manager`; each answered 200 at both BASE and head:
   - `GET /api/setup/status`: the primary workspace id and endpoint, and the sign-in tenant and client ids.
   - `GET /api/log-analytics/diagnostics`: an endpoint and a workspace display.
   - `GET /api/setup/validate-all`, `GET /api/models/active`, `GET /api/service-check`: each names an endpoint.

   The gate's probe seeded data sources only, not a primary workspace, so none of its markers appeared. The field content is the drafter's source read (kit finding 5), re-read by Tuesday at source, and not re-measured by the gate.

   More widely, no other route reads the table: `end_user` and the partner roles read every route a viewer reads (`/api/stats`, `/api/segments`, `/api/log-analytics/status`, `/api/ai/audit-log/summary` and more, each 200 in the probe).

   Dup-check before filing:
   - RD-929 (To Do): table-wide enforcement, the natural home for the "every route" item.
   - RD-706 (Done): the anonymous open-window read of `/api/setup/status` ids, a different caller.
   - RD-1022 (To Do): a viewer making the server USE stored sign-in details through five routes, a different property (use, not disclosure).
   - RD-933 (To Do): the partner and end-user roles, design.

   The JQL `text ~ "api/setup/status"` found no open ticket for a signed-in excluded role reading these ids. Propose one ticket for the `setup/status` fields (and diagnostics), under RD-929.
4. **Info, pre-existing, unchanged by this lane (the seat's finding).** If `jsonStorage` is null while sign-in is enforced, the global check skips the session block and leaves `req.user` unset. The helper then allows, and the handler fails 500 on its own store call. No data is sent.
5. **Info.** `ROLE_CAPABILITIES` is frozen, but its role arrays (`READS_TODAY` and the rest) are not. No product code mutates them. If the table becomes the enforcement source (RD-929), freeze the arrays too.
