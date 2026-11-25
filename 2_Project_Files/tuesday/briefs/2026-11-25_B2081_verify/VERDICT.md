GATE B2081: GO WITH FINDINGS
@ 16a29d3 on main 40df849

Gate G1 (Opus, claude-opus-5-5), round 1 of 2, RD-1040 (kit B2076, seat N173). Read-only to the project, GitHub and Jira.

**Re-measured** by `gh api -X GET` at 10:43 and again at 11:11 AEDT, 25 Nov:

| Read | Value |
|---|---|
| main | `40df849310c9fd412ed7670d5c6647c3dcf096f1` (did not move) |
| branch `b2076/rd1040-data-source-reads-refuse-roles` | `16a29d3a65db7c72637a8810e6601be39673261e` |
| compare main...head | ahead 2, behind 0; files: the test file +337, `backend/server.js` +19/-0, the counts file +3/-3 |
| open pull requests | 0 |
| code scanning on main | 22 open, 13 at `server.js` |
| head's check runs | 1 (audit-production-deps, success) |

Parents: K^ = A `a41ed671`, A^ = BASE `40df8493`. BASE's parents are `4d8713e5` and `9d4ddb7f` (the merge of PR 253).

## Measured

All runs were in the gate's own dot-free trees under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/g2081/`, inside the NexusAI jest lock (2 acquisitions, `g2081-lane` and `g2081-verify`, each acquired after 0s and released, lock-wrapper rc 0), with `--maxWorkers=2`, `NODE_OPTIONS` unset and Node v24.22.2.

- **The diff was read whole:** both commit messages, `server.js` and the counts file, and all 337 lines of the new test file.
- **Red-first at BASE** (`rf`, plus the new file): 8 failed and 13 passed of 21. The failures are R1 end_user, R1 partner_manager, R1 partner_technician, X1, X3, X4, D1 and S1. `judge2076.py`: JUDGE rf PASS.
- **Green at head** (`work`): 21 of 21 on the new file. The 59-suite set (`suites2076.txt`) passed 834 of 834, with rd1036, rd1021, rd929 and rd978 among them; JUDGE green PASS.
- **Red-proof** (`rp`, the head with `backend/server.js` set back to BASE's blob `a7426b07`): 8 failed of 21. The names are identical to the red-first set, compared by program (equal: True); JUDGE redproof PASS.
- **Full verify at head** (`chk`, porcelain 0):
  - `VERDICT: PASS`, 6362/6362 tests across 401 suites (jest exit 0).
  - `^PASS` 401, `^FAIL` 0, EADDRINUSE 0; verify rc 0; 10:48:15 to 11:10:58.
  - This matches the expected 6362/401.
  - **Head IS the merge result** (behind 0: main `40df8493` is K's grandparent), so no separate merge build was needed. This verify is the merge verify.
- **gitleaks 8.30.1:**
  - Control first: a planted made-up AWS key pair in `_quarantine/plant`; `gitleaks dir` read rc 1, "leaks found: 2".
  - `BASE..head` (git mode, 2 commits): rc 0, no leaks.
  - The two commit messages: rc 0.
  - The five landing texts: rc 0.
- **Code scanning, for landing.**
  - Main's javascript-typescript analysis at `40df8493`: results_count 29, matching the seat's local CodeQL (29/29, NEW 0, KEPT 0).
  - Main's last `server.js` alert line 16873 is head line 16892 (the same text).
  - PR 253's PR-ref analyses read results_count 0.
- **Deploy demo, read only.**
  - Actions variables: total_count 0.
  - Last 20 of 267 runs: all skipped. The newest is 45495872057 at `40df8493`: build skipped, deploy skipped.

## Attack (G1: a real account whose stored role lacks config.read)

The probe is `probe-g2081.test.js.txt`. It ran on the real server at the head and at BASE, with results in `probe-head.json` and `probe-base.json`. It seeded 25 stored role shapes plus 2 data sources holding made-up markers, and sent every path verbatim with `http.request`.

- **Route spellings.**
  - For `end_user` at the head, 403 with no marker on 11 forms: a trailing slash; upper and mixed case on both routes; `?x=1`; `/:id/`; `%31` as the id; `/:id?a=b`; an unknown id; `%00`, `__proto__` and `constructor` as the id; and HEAD on both routes. At BASE every one of these answered 200 with all markers, or 404 for the unknown or odd ids.
  - These reach no handler at either sha and leak nothing: `//api/data-sources`, `/api//data-sources`, `/api/data-sources//`, `%2D`/`%2d`, `/%61pi/...`, `;x` and `.json` all answer 404; `%2F` and the dot-segment forms answer 400.
  - OPTIONS: 200 with an empty body at both shas.
  - TRACE: 403 at both shas.
  - The sub-routes `describe-table` and `discover-tables`: 403 at both shas (requireAdminFor).
- **Middleware and router order.** The only earlier `app.use` on this path is the `dataSourceTestLimiter` for `/:id/test`. `afterAuthGate` holds no data-source route. Express 5.2.1 matches without regard to case and without strict routing, so every spelling that matches lands in the two handlers, and the check is their first statement. Only `requireAuth` (server.js line 2782) sets `req.user`.
- **Role source.** The role is the STORED user's, read on every request (no cache: the probe's and X3's on-disk rewrite took effect on the next request).
  - A user who is deleted, set inactive, or has their role changed by PUT gets 401 on the next request (the sessions are deleted). Same at BASE.
  - A session with no stored user reads as viewer (the X2 control).
  - In open mode, with or without a stale cookie: 200, as at BASE (no `req.user`, as `decide()` answers open mode).
- **Prototype keys and non-string roles:** all refused 403, where BASE answered 200.
  - Strings: `__proto__`, `hasOwnProperty`, `toString`, `valueOf`, `constructor`.
  - Non-strings: `7`, `{}`, `["viewer"]`, `["config.read"]`, `true`.
  - `0` and `false` read as viewer through `|| 'viewer'` and are answered 200, as are `''` and `null` (X2).
- **Case and whitespace variants of an allowed role:** `' viewer'`, `'viewer '`, `'VIEWER'`, `'viewer\t'`, `'viewer\u0000'` and `'end_user '` are all refused 403 (Q-0, fail-closed). None gains access.
- **Existence and timing.** For a refused role, an existing id and a missing id each read 403; the median times are 18.23 and 18.16 ms (n 40). No oracle. BASE gave 200 against 404.
- **Audit row.**
  - The detail keys are exactly `method, path, reason, statusCode, userEmail (masked), userRole`; the row also holds `userId`.
  - No data-source marker is in any row.
  - `userRole` records the stored value verbatim, a non-string or a NUL included (pre-existing RD-932 shape).
- **The `require` at that point.** `capabilities.js` requires nothing and has no side effects; `ROLE_CAPABILITIES` is `Object.freeze`d. The identifiers `permissionTable` (3 uses) and `refuseDataSourceReadForRole` (1 definition, 2 calls) are unique. `node --check` and the full verify pass. The other importers are tests only (9 files), and their suites are green.
- **Existing tests and the inventory.**
  - rd978, rd929, rd1036 and rd1021 are green at the head.
  - `docs/role-capabilities.json` rows: the statuses (anonymous 401, viewer 200/404, admin 200/404, open 200/404) are unchanged and true. Its text "handler gate: none" is now stale (Finding 3).
  - No test asserts that the table is unused.
- **Sibling routes.** As `end_user` and `partner_manager`, `/api/setup/status`, `/log-analytics/diagnostics`, `/setup/validate-all`, `/models/active`, `/service-check` and also `/api/stats`, `/api/segments`, `/api/log-analytics/status` and `/api/ai/audit-log/summary` answer 200 at both shas. Not made worse.
  - The probe seeded no primary workspace, so the setup/status field content is the drafter's source read and not re-measured here.
  - `/api/setup/data-sources`, `/api/debug/data-sources` and `/api/admin/health` answer 403.

**Three shapes outside each tested property:**

1. **Outside the role cells:**
   - (a) A role from an identity provider's application roles or a restored store. Not read; the server reads only the stored role.
   - (b) The first-run window with sign-in configured but `authEnforced` false. Read: no `req.user`, everyone is answered, the same as BASE.
   - (c) `jsonStorage` null with sign-in enforced. Read: allow, then the handler fails with 500; no data (the seat's finding).
2. **Outside the spelling cells:** `//`-prefixed paths, `%2D`-encoded paths and `.json`/`;` suffixes. Probed: 404 at both shas, no leak.
3. **Outside the D1 audit cell:** row contents for non-string roles. Probed: verbatim, no source value.

## Findings

1. **MINOR. Does not block.** A behaviour change from Tuesday's Q-0 default: a stored role that differs from an allowed role by case or whitespace (`VIEWER`, `' viewer'`) is now refused, where it was answered before. Such a role can be stored only by an administrator through the create route's API, or by hand. Disclosed in the PR body; for the records.
2. **INFO. Does not block (records).** The sibling routes (`/api/setup/status` and the rest) still send stored ids and endpoints to the excluded roles, and no other route reads the table. Unchanged by this lane. The dup-check targets are in FOR-RECORDS (RD-929, RD-706 Done, RD-1022, RD-933); no open ticket was found for this exact item.
3. **INFO. Does not block (records).** `docs/role-capabilities.json` says "handler gate: none" for the two rows, and the scanner's `GATE_TOKENS` do not know the new helper, so rd978's gated count cannot see this gate. The statuses are still true.
4. **INFO. Does not block (records).** The header of `capabilities.js` (line 6, "DESIGN ONLY ... Nothing in the product requires this file") is now untrue. Fold it into RD-1034's stale-comment follow-up, or file it.
5. **INFO.** The `ROLE_CAPABILITIES` object is frozen but its role arrays are not. No product code mutates them; freeze them when the table becomes the enforcement source.
6. **INFO.** NOT RUN by anyone:
   - a hosted instance, a real identity provider, a real browser, Linux;
   - the sign-in-unproven state;
   - the hosted Build and CodeQL on the PR. Tuesday reads these at landing.
7. **INFO (gate's own instrument).** The probe's one create-route call with the role `' Viewer '` omitted the password and was answered 400. It is not counted; the store-seeded shapes cover the property.
8. **INFO.** The texts were checked:
   - PR title and body: no person's name, no card, seat or build id. The refusal is attributed to the product owner's ruling; the defaults are named as the coordinator's; the siblings that were not built are disclosed.
   - The commit messages carry the frozen "the product owner's 2026-11-25 ruling" sentence only.
   - FOR-RECORDS still holds the `<N>`, `<M>` and `<VERDICT line>` fill-ins, for the records pass.

## Before landing (Tuesday)

1. Open the PR from `landing.txt`. Re-measure main first: if it moved and touched `backend/**`, `__tests__/**`, `scripts/**` or `package*.json`, the lane goes back to a seat.
2. Wait for the hosted checks with `--min-checks 7`. Read the PR-ref code scanning against main's baseline.
3. Land with a merge commit pinned to `16a29d3a`.
4. Read the Deploy demo run: both jobs must read skipped. Never approve; the C-224 hold stands.

No Blocker, no Major.

Scratch left in place (nothing deleted): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/g2081/`, which holds:
- the clone and its four worktrees (rf, work, rp, chk), each with a `node_modules` symlink to the seat's `.tools/b2076/clone/node_modules`, used read-only;
- the logs and raw files;
- the gitleaks plant in `_quarantine/`;
- the probe's temporary server directories under the OS temp directory.

No project-side path was created. Bands 22560-23199, 28960-29599 and 21280-21919 had 0 listeners after the runs, and no process of the gate is running.
