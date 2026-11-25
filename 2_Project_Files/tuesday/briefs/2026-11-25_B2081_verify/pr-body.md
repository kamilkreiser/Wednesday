## What this changes

`GET /api/data-sources` and `GET /api/data-sources/:id` answered every signed-in session 200 with every stored field of every data source (ids, workspace, endpoint, tenant and client ids, region and the rest; the client key masked as `***`), whatever the session's role. The permission table (`backend/services/capabilities.js`) puts both routes under `config.read` and gives that capability to neither `end_user` nor the two partner roles, but no server code read the table.

**The product owner's ruling (2026-11-25):** refuse the route to roles the permission table excludes, keep the fields as they are for allowed roles, review before merge, nothing deployed.

In `backend/server.js` (19 lines added, 0 removed), one helper, `refuseDataSourceReadForRole`, sits beside the two routes and is the first statement of both handlers, before the store is read. It reads `ROLE_CAPABILITIES` from the permission table and answers 403 `{"error":"Data source settings are not available to this role"}` unless the session's stored role is an own key of the table whose entry holds `config.read`.

- **Refused today:** `end_user`, `partner_manager`, `partner_technician`, and any stored role value the table does not name.
- **Answered exactly as before, field for field:** `admin`, `viewer` and the five proposed roles (`print_operations`, `finance`, `security`, `executive`, `department_manager`).
- **No session:** unchanged (401 with sign-in enforced; open mode answers as before).
- The role is the stored one, read again on every request, so a changed role takes effect on the next request. Each refusal writes the usual `REQUEST_DENIED` audit row.

## Choices that are the coordinator's, not the product owner's

- **A stored role the table does not name is refused too**, as the table's own `decide()` answers it: another case or spacing (`Admin`, `VIEWER`, `' viewer'`, `End_User`), a built-in property name (`constructor`, `__proto__`), a made-up word, or a non-string value. **This is a behaviour change:** before, any signed-in session was sent the list, so a user stored with such a role who reads the list today will be refused. Stored roles that are empty or missing, and a session with no stored user, still read as `viewer` and are answered.
- **The 403 body text** above (it names no role and no field).
- **The dashboard's region filter is left as it is.** For a refused role it keeps its one "All Regions" option and logs one console error; it throws nothing (checked by the new cells F1 and F2).
- **The sibling reads are not built here** (see "Not in this change").
- **The permission table's header and the committed role inventory are not touched** (see "Not in this change").

## The result (21 new cells in one file)

- **Before (main):** 8 of 21 fail, all on the property. The excluded roles and four role values the table does not name were answered 200 with the stored sources on both reads. A session whose stored role became `end_user` was still answered. HEAD, an upper-case path, a trailing slash and an unknown id were answered for `end_user`. No `REQUEST_DENIED` row was written, and the check was absent from the source.
- **After:** 21 of 21 pass. With only the product edit reverted, the same 8 fail.
- **Controls (green before and after):**
  - The administrator's answer: 2 sources, 17 keys, the client value `***`.
  - The six allowed non-administrator roles: an answer deep-equal to the administrator's.
  - No session: 401. Viewer-equivalent sessions: 200. Open mode: 200.
  - The region filter: refused and answered.
  - 0 connects and 0 stored-secret reads for a refused role.
- An unknown id is refused 403 for a refused role (not 404), so the status does not say which ids exist.
- The 59 suites that name the data-source routes, the permission table, the role inventory or the region filter: 834 of 834 pass. Among them are the viewer Data Sources list, the setup-list and debug-read administrator checks, the handler-span scan and the capability census.

## Files (3 files; two commits: the change, then the suite counts written by the project's own command)

- `backend/server.js`: 19 lines added, 0 removed.
- New: `__tests__/rd1040-data-source-reads-refuse-roles-without-config-read.test.js` (21 tests).
- `scripts/verify-expected-counts.json`: 6341 / 400 to **6362 / 401**, by `npm run verify -- --maxWorkers=2 --update-counts`.

## Verification

- Full verify, run by the author at both commits and again by review at the head (which already contains current main): `VERDICT: PASS`, 6362/6362 tests across 401 suites.
- Local CodeQL (javascript), main against head: NEW 0, KEPT 0, `rc 0 PASS`.
- gitleaks over the whole diff and the commit messages: no leaks found. The control fired.

## Not in this change (named)

- **Which fields an allowed role that is not an administrator receives.** The ruling keeps them as they are; this is a later question.
- **Other routes still send stored settings to every signed-in role, the excluded roles included:**
  - `GET /api/setup/status` (the primary Log Analytics workspace id and endpoint, and the sign-in tenant and client ids);
  - `GET /api/log-analytics/diagnostics`;
  - `GET /api/setup/validate-all`, `GET /api/models/active` and `GET /api/service-check` (each names an endpoint).
  - More widely, no other route reads the permission table yet, so the partner roles and `end_user` still read every other route a viewer reads.
- **The permission table's header** (`backend/services/capabilities.js` line 6) still reads "STATUS: DESIGN ONLY. Nothing in the product requires this file yet". It is now untrue: `backend/server.js` requires it.
- **The committed role inventory** still describes the two rows as "handler gate: none", because its scanner does not know this helper's name. The inventory's statuses for anonymous, viewer, administrator and open mode are unchanged.
- **Not tested:**
  - a hosted instance, a real identity provider, a real browser on the dashboard, Linux;
  - the sign-in-unproven state;
  - the first-run window with sign-in configured;
  - the hosted Build and CodeQL on the merge commit.

## Deploy

None. Merging starts a `Deploy demo` run, because `backend/**`, `__tests__/**` and `scripts/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'`, and the deploy job also needs approval from a required reviewer on the `demo` environment. The last 20 runs of the workflow all read skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
