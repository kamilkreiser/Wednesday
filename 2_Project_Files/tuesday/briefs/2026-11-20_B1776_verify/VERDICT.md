GATE B1776: GO WITH FINDINGS @ 8af88ee on main b169b8a

Gate tier: G1 (security surface: who may make the server connect out with stored sign-in details, and what the audit trail records). Round 1 of 2. Reviewer: Opus 5.5, in session, independent of the builder.
Clocks (AEDT, 2026-11-20, from `date`): first 14:32:23. Lock acquired 14:45:34 and released 15:18:01, one acquisition. Last ref read 15:18:16.
Work folder: my own clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s297/g1776/clone`, push URL `invalid://no-push`. Worktrees:
- `head10`, `mut2` and `probe0` at the head
- `redT14` at T `0e2de94d4804`
- `base4` at the base

All five are on jest slot 9, band 25760-26399, printed by the project's own `worktreeSlot()` in each tree.

Blocker 0 | Major 0 | Minor 4 | Info 7

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Minor | F-1. A sibling route outside the four still lets a signed-in viewer make the server connect with stored sign-in details. `GET /api/setup/data-sources` (`backend/server.js:17162` at head) runs a live `testConnection` for every enabled source with `getDataSourceDecrypted` and `createLawClient` (`:17178`, `:17182`, `:17191`). Measured at head on the real server, as a seeded viewer: 200 with 1 connect and 1 decrypt for one source, and 2 and 2 for two sources. A request with no session gets 401 and 0. The committed inventory row reads viewer 200, handler gate none. The route is not in the three tickets, and it is not a regression (same answer at base). A Jira text search found no ticket for it. | Records line plus a follow-up ticket: the same setup-mode-aware check, or a status that does not dial for a viewer. The PR text must not say a viewer can no longer cause any stored-credential connect. pr-body.md says so. |
| Minor | F-2. `GET /api/debug/data-sources` (`server.js:18392`) answers a signed-in viewer 200 at head. For every non-primary source it decrypts the stored source, builds a client and queries 5 rows (`:18405`, `:18410`, `:18424`-`:18433`). The body carries `hasDecryptedSecret`, `workspaceId`, `authMode` and, when the query succeeds, a sample record (user name, printer host name). Measured with two sources: viewer 200 with 1 connect and 1 decrypt. With one source (the primary) it reads 0 and 0. The permission table gives it `config.read` on the same line as the two reads (`backend/services/capabilities.js:156`). So after this lane the table treats all three alike, but the wire refuses two. No ticket found (Jira text search `"api/debug"` and `"debug/data-sources"`: only RD-118, Done, another subject). | Records line plus a follow-up ticket: administrator only, or remove the route from production builds. Out of this lane. |
| Minor | F-3. The committed cells do not measure the stored-source read. My mutant M5 moved the check below `getDataSourceDecrypted` and its 404 in `POST /api/data-sources/:id/test`. V1 stayed GREEN (403 and 0 connects, because the check still sits before the dial). Only the text cell S1 went red. The behaviour itself is right at head: my fenced probe counted 0 decrypts for every refused caller on all four routes, via a counter wrapped around `getDataSourceDecrypted` in the spawned server, with the administrator control reading 1. The claim "before the server reads the stored source" is pinned by text only. | A follow-up cell that counts decrypts, like this gate's `progs/gate-preload.js`. Not a landing blocker: S1 catches the move. |
| Minor | F-4. The builder's heads census misreads one count: `b1480/nexusai-s-setup-column-mapping` is ahead 12 by compare, and the STATUS says 10. The four stale heads are not live work. None has ever had a pull request. Last commits: 2026-11-10 for the two `b1480/*` heads and 2026-09-14 for the two `*-s59` heads. They are behind main by 218 to 1116. | None for landing. Records may list the heads for clean-up. |
| Info | I-1. Cells test only the role `viewer`. My mutant M9 replaced the check in the setup test handler with a deny-list for `role === 'viewer'`. V4 stayed green; S4 and the call-count cells went red. My probe drove 9 non-administrator sessions on each route at head: `Admin`, `ADMIN`, empty, `['admin']`, `' admin'`, `administrator`, a missing role, a user not in the store, and viewer. Every one read 403 `Admin access required` with 0 connects and 0 decrypts (the matrix below). | None for landing. The helper compares `role === 'admin'` strictly (`backend/services/authEnforcement.js:647`). |
| Info | I-2. The setup window with sign-in configured but first run not complete is open by the helper's design (`adminGateRefuses`, `authEnforcement.js:645`). Measured on a real server in that state: a signed-in viewer reaches all four routes and connects. It can also create a data source (200) and call `POST /api/setup/complete-first-run` (200). A viewer cannot put a deployment into that state: on a completed deployment the only writer route answers the viewer 403, and a header or query parameter changes nothing (probe D). An administrator can, by resetting first run. Out of lane; same at base. | Records line: after an administrator resets first run, every signed-in viewer passes every `requireAdminFor` check until first run is completed again. |
| Info | I-3. Other audit and log sinks still record `req.path`, enumerated by program. Router-relative, the old form: `backend/services/scimProvisioning.js:120` (`scim_rate_limited`) and `:156` (`scim_auth_failed`), inside the router mounted at `/scim/v2` (`server.js:22385`). Full path, because they run at app or route level: `server.js:1627` (a CSRF log warning, not audit), `:2582` (`auth_state_unknown_denied`, called from app-level middleware), `:22518` (global error handler log), `backend/services/aiEnabled.js:299` (route-level middleware on four app routes). None is in RD-1012 or RD-1013. RD-1013 names `:1627`, `:2582` and `:22506` (at base) as not traced. | Records line for the two SCIM entries (the RD-1013 class). |
| Info | I-4. A very long path is recorded whole: a 6000-character segment was recorded in full in both rows, not truncated. Bounding is RD-1006's subject. A raw `#` now cuts the recorded path, while the router still matched the text after it as part of `:id`. That is RD-1012's pinned rule, and no route is mis-named. | None. |
| Info | I-5. The frozen headers of `rd1011` and `rd1012` contain "not the product owner's" (a negation; in rd1011 the phrase is split over two lines). It attributes nothing to the product owner, and every commit message is clean (`product owner` count 0 by program). Added comment lines carry existing ticket keys RD-793, RD-958, RD-964 and RD-968 in the style of the files they extend. | None for landing. |
| Info | I-6. A stale comment line sits above `pathnameOf` ("...full path as sent; the query string is never part of it."): `backend/services/accessAudit.js:48` at head. Cosmetic; the builder disclosed it. | Any later touch of the file. |
| Info | I-7. Gate's own process: one of my shell commands carried a no-op `cd` inside a `$( )` substitution, a leftover in a loop that did nothing. No file or tree changed. A rule breach disclosed, with no effect on any result. | None. |

No Blocker: no signed-in non-administrator could make the server connect, or read the stored source, through any of the four routes this lane closes. That holds for every session shape, path variant, method variant and target form I could send.

## THE FOUR ROUTES: route-by-caller MATRIX (measured, real server, both trees on Node v24.22.2)

How it was measured:
- The server was booted by the project's own harness (`bootServer`) with the project's own fence (`__tests__/helpers/route-table-preload.js`), plus my preload `progs/gate-preload.js`, which counts `getDataSourceDecrypted` calls in the spawned server.
- "c" is the fence's refused lookups plus refused connects, counted before and after one request. "d" is the decrypt count.
- Each request carried its own `X-Forwarded-For` (documentation IPv6 prefixes). `trust proxy` is 1 (`server.js:1143`), so the shared 5-per-10-minutes limiter never answered: 0 responses were 429.
- One stored source was created by the administrator (200).

Enforced shape (sign-in configured, first run complete, users exist):

| caller | each of the 4 routes at BASE | each of the 4 routes at HEAD |
|---|---|---|
| no session | 401 `Authentication required`, c0 d0 | 401, c0 d0 |
| viewer | 200, handler answer, c1 d1 (describe-table c3 d1) | **403 `Admin access required`, c0 d0** |
| role `Admin` / `ADMIN` / `''` / `['admin']` / `' admin'` / `administrator` / missing role / user not in store | 200, c1 d1 (describe-table c3 d1) | **403 `Admin access required`, c0 d0** (all 8, all 4 routes) |
| administrator (control) | 200, c1 d1 (describe-table c3 d1) | 200, c1 d1 (describe-table c3 d1): the counter counts |

Handler answers at base for the viewer:
- POST test: 200 with `Query execution failed: Authentication failed...`
- describe-table: 200 with `success:true`, the columns
- discover-tables: 200 with `success:false`, the authentication message
- setup test: 200 with `network_error`

Viewer variants at head, each route (base in brackets):

| variant | result at head [base] |
|---|---|
| trailing slash, upper-case path, mixed-case segment | 403, c0 d0 [200, c1] |
| `X-HTTP-Method-Override: GET` and `?_method=GET` on the POST routes | 403, c0 d0 [200, c1] (no override middleware: `method-override` 0 hits in server.js and package.json) |
| HEAD on the two GET routes | 403, c0 d0 [200, c1 or c3] |
| absolute-form target `http://evil.example/api/...` (raw socket) | 403 `{"error":"Admin access required"}`, c0 d0 [200, c1] |
| non-numeric id `abc` | 403, c0 d0 [404 `Data source not found`, c0 **d1**: base read the store first] |
| inner or leading doubled slash, encoded segment letter, encoded-dots id | 404, c0 d0, no handler [same] |
| encoded slash in id | 400 (the server's dot-segment/encoded-slash refusal), c0 d0 [same] |
| GET on a POST route, PUT, POST on a GET route | 404, c0 d0 [same] |
| OPTIONS | 200 empty (CORS), c0 d0 [same] |

Mounted once: each of the four registrations appears once (`server.js:15962`, `:15990`, `:16059`, `:17394` at head). The only `app.use` on these paths is the limiter at `:1404` and `:1405`. Every route that reaches the connect code, enumerated by program (`progs/callers.py`: every call of `getDataSourceDecrypted`, `createLawClient`, `testConnection`, `describeTable` and `discoverTables` under `backend/`, attributed to its enclosing registration):

| route | viewer at head (measured) |
|---|---|
| the four | 403, c0 d0 |
| `PUT /api/data-sources/:id` | 403 (gated) |
| `POST /api/setup/log-analytics` | 403 by the inventory row (gated) |
| `GET /api/setup/data-sources` | **200, c1 d1** (F-1) |
| `GET /api/debug/data-sources` | **200, c1 d1** with a non-primary source (F-2) |
| `GET /api/setup/discover-tables`, `GET /api/log-analytics/test`, `GET /api/log-analytics/status`, `GET /api/service-check`, `GET /api/setup/validate-all` | 200, c0 d0 in this boot (they use the primary workspace configuration, which the boot does not set: their dial with a configured primary is NOT measured; read at source they use the stored primary configuration) |
| query and report helpers (`initDataSource`, `getLawForSource`, `reportSource`, `queryAI`) | reached by the report and chat routes a viewer is meant to use; outside this class |

Open window (no sign-in configured, first run incomplete), anonymous: all four routes 200 and connect at base and at head (POST test c1 d1, describe c3 d1, discover c1 d1, setup test c1 d1). The wizard path is unchanged.

Sign-in configured and enforced, users exist, first run NOT complete:
- head: anonymous 401 c0 on all four; viewer and administrator 200 and connect on all four.
- base: the same.

That is I-2. It is the helper's design, at source: `adminGateRefuses` returns false while `!(firstRunComplete && hasUsers)` (`authEnforcement.js:645`).

## THE FIRST-RUN WINDOW (attack)

At source, the setup-mode inputs are all read per request from the store and the environment, never from the request:
- `getFirstRunStatus` reads the stored `firstRunComplete` setting (`server.js:4271`).
- `hasAnyAuthorizedUsers` and `resolveEntraConfig` read the store and the process environment.
- No header, query parameter or body field is read.

The writers of `firstRunComplete`, enumerated by grep over `backend/`:
- `server.js:4075` (`POST /api/auth/enforce`, writes true)
- `server.js:14842` (`setFirstRunComplete`, whose only caller is `POST /api/setup/complete-first-run` at `:16382`, administrator-gated, viewer 403 by inventory and by my probe D)

No other writer. A read error in `getFirstRunStatus` answers false, which means open. That is backstopped at source by the sign-in middleware's `denyAuthStateUnknown` (`server.js:2571`), which refuses every route when the store cannot establish the auth state. This was read, not measured.

Probe D (enforced, complete) measured:
- viewer `POST /api/setup/complete-first-run {completed:false}`: 403
- then a viewer request with headers `X-First-Run`/`X-Setup-Mode`: 403 c0
- then a viewer request with `?firstRunComplete=false&setup=1`: 403 c0
- then describe-table: 403 c0

A race with the setup-complete write, or a second process: not tested. The flag is per-request storage. A viewer has no writer to race with, but an administrator's reset could be (I-2).

## THE AUDIT PATH (RD-1012, RD-1013)

Unit level (`progs/rp_table.js`, plain node, base against head helper, a router mounted at `/api/feedback`):

| target form | base | head |
|---|---|---|
| plain, `?query`, trailing slash | same | same |
| absolute-form http, https with port, upper-case scheme | leaked scheme, host, port | `/api/feedback/6` |
| absolute-form with user-info | leaked `u:p@` | `/api/feedback/6` |
| absolute with `?` or `#` before the first slash, or no path | host text | `/` |
| raw `#`, `#` then `?` | fragment kept | cut |
| `%3F`, `%23`, `%2F`, `%00`, `%0D%0A`, `%e2%82%ac`, dot segments, encoded dots, backslash | as sent | as sent |
| `http:/x` (one slash), `//host/path`, no leading slash | as sent | as sent (no `://`, starts with `/`) |
| 9000-character path | whole | whole |

On the wire (real server, a viewer `PATCH /api/feedback/<target>`, refused 403 by the triage check, both rows read through the administrator's export):

| target | base row path | head row path (both rows equal) |
|---|---|---|
| absolute-form | `http://evil.example/api/feedback/zzq01` | `/api/feedback/zzq01` |
| absolute with user-info and port | `http://u:p@evil.example:8443/api/feedback/zzq02` | `/api/feedback/zzq02` |
| raw `#frag` | `/api/feedback/zzq03#frag` | `/api/feedback/zzq03` |
| `?a=1` | `/api/feedback/zzq04` | same |
| `%3F`, `%0D%0A`, `%e2%82%ac`, backslash, comma and quote | as sent | as sent |
| 6000 characters | whole | whole |
| `%2F`, dot segment, encoded dots, raw newline, raw control byte, raw tab, raw non-ASCII bytes | refused 400 before any router, no row | same |

Forging and splitting: rows are structured objects in the ring buffer and winston metadata (`server.js:305`-`:330`), so a path cannot add a row. The CSV export quotes and doubles quotes: the comma-and-quote path stays one cell, `"/api/feedback/zzq10,""x"""`. An encoded CRLF stays encoded. A path cannot record as a different route: the router matches the same pathname the helper keeps, and a target whose pathname does not start with the mount never reaches the router.

Entra refusal entry, measured on the real server through the export. Base wrote `/`, `/`, `/scim-token/revoke`, `/zzent` and `/zzent2`. Head writes:
- base path: `/api/setup/entra-provisioning`
- trailing slash: `/api/setup/entra-provisioning/`
- sub-path: `.../scim-token/revoke`
- absolute-form: `.../zzent`
- fragment: `.../zzent2`

Head keeps the two keys, `method` and `path`.

## NO NEW WORD
- The refusal is the helper's existing answer at `server.js:19110` (head).
- Sibling write refusal at base and at head: `POST /api/data-sources` as viewer gives 403 `Admin access required`.
- Each of the four routes at head gives 403 `Admin access required`, raw body `{"error":"Admin access required"}`.
- At base no route refused a viewer, and each returned its handler's answer (the matrix).
- The diff adds no other user-facing string. The product files add only comments, the gate statement, the helper and the import.

## CELLS AND MUTANTS (measured under the lock, Node v24.22.2, jest JSON judged: suites equal to paths passed)
- New files at head, twice, in `head10`: 47 of 47 green both times (rd1011 27, rd1012 11, rd1013 9).
- The four rewritten tests and the route callers at head, one run: 11 suites, 184 cells, 0 red. The suites: rd793 28, rd958 5, rd978 5, rd988 7, rd929 7, rd990 17, rd830 13, rd800 33, discover-tables-tenant-mask 12, scim-security-controls 54, rd932 3.
- Red-first, in `redT14` (the test-only commit T) with the base's four product files and two docs copied in, blobs proved equal to base: **27 RED and 20 GREEN**. The red cells are rd1011 V1-V4, S1-S4, P1, I1-I4; rd1012 U1, U2, U3, U7, H1, H2; rd1013 E1, E2, E3, E5, E6, E7, E8, H1. Equal to the kit table and the STATUS. The files were restored and blobs proved equal to T; porcelain empty.
- Base answers of V1-V4: 200, c1 / 200, c3 / 200, c1 / 200, c1.
- Rewrites: each is the narrowest that follows the new answer. Changes: 34->38, `['L1','RD-793']`->`['L1']` with `rd793: undefined`, kept 2->1, and the hand list plus 4. None removes an assertion or a cell (per-file counts as above).
- `rd929`'s pending cell computes, from the committed inventory, the routes a viewer reaches without holding their capability, and at head its computed set equals the pending list (only the L1 key's routes). It reads one direction only, so it cannot see the two reads, which are now refused while the table still says `config.read` (and F-2's route).
- Negative-asserting cells of the open-window callers (rd830, rd800, tenant-mask) still reach their checks. Paired mutation M10 makes the helper refuse everyone. It reddened their positive controls: tenant-mask CONTROL x6; rd830 CONTROL x4 and the PUT and POST cells; rd800 LIVE, C-BODY, C-PLAIN x2, CAP-500 and S-208/209/213/218/219; plus rd1011 A1-A4 and O1-O4, rd793 and rd988 cells. In total 54 red. So an early return would not pass silently.

| mutant (mine, asserted replace, reverted by `git show HEAD:` with blob proved) | RED cells (12- or 5-file set) |
|---|---|
| P0 none | 0 of 125 and 0 of 94 |
| M1-M4 the three added lines removed from each handler in turn | rd1011 V*n* S*n*, rd793 C2, rd978 probe, rd988 T7 (5 each) |
| M5 check moved below the stored-source read (POST test) | rd1011 S1 only (F-3) |
| M6 the helper's setup-mode test inverted (`authEnforcement.js`) | rd1011 V1-V4, G2, G3; rd793 V1-V4, E1-E4; rd988 T1, T4, T5, T6 (18) |
| M7 the audit helper returns the full target again | rd1012 U1, U2, U3, U7, H1, H2; rd1013 E6 (7) |
| M8 describe-table: 403 written, no return | rd1011 V2, S2 |
| M9 setup test: deny-list on `role === 'viewer'` | rd1011 S4, rd793 C2, rd978 probe, rd988 T7 (I-1) |
| M10 helper refuses everyone | 54 (paired mutation above) |
| M11 entry reads `req.path` again | rd1013 E1, E2, E3, E5, E6, E7, E8, H1 |
| M12 fragment cut dropped | rd1012 U2, U3, U7, H2; rd1013 E6 |

No asserted field is a constant written into both expected and received. The V/A/O/N cells read status, body and the ledger. The S cells read source text. The P cells read the module. The I cells read the committed file. The U and H cells read the helper and the export. E8 reads the router source.

## FULL VERIFY (head, Node 24)
`npm --prefix head10 run verify -- --maxWorkers=2` with Node v24.22.2 and its npm 11.19.1 first on PATH, `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES -u VERIFY_EXPECTED_FILE`.

| what | value |
|---|---|
| head and tree | 8af88ee and tree f5f7094e (equal to the builder's last verify tree) |
| porcelain before and after | empty |
| run | 14:54:44 to 15:17:08, rc 0 |
| verdict | `VERDICT: PASS - 6195 (the tool prints an em dash here)/6195 tests passed across 390 suites (jest exit 0)`, equal to the committed pair 6195/390 (6148 + 47, 387 + 3) |
| `EADDRINUSE` | 0 |
| band 25760-26399 listeners | 0 before and 0 after (control: all listeners 13) |
| load1 | 2.18 at start, 2.14 at end |

Node 24 result: no difference from the builder's v26 PASS. Every jest number above, the inventory drive and the verify came from v24.22.2. Native module `sqlite3` is N-API and loaded on 24.

Lock: one acquisition, under base `session-tools/locks-laptop-1017`. That is the builder's base (`.tools/b1762/lib.sh:18`). Tag `b1776-gate`, acquired after 0 s with the queue empty, no NexusAI pane live. Slot 9 was chosen because no 20 Nov brief names it: 0 files of 20 Nov, 4 of 18-19 Nov, none live. It is not 17.

Inventory: `scripts/role-capability-inventory.js --generate` from the head in `head10` (154 s, rc 0). Rows: equal to committed, 203 of 203. Meta: only `generatedAt` differs. The page differs only in line 4, the generated-at stamp. `--check` printed `runtime rows 203; committed rows 203` and `route set equal`, rc 0. The drive wrote 2 files under `backups/`, which were moved to `g1776/_quarantine/inv-backups/`. Porcelain empty after.

## CODEQL
`pr_codeql_check.sh --base b169b8a0... --head 8af88ee8... --lang javascript`, scratch clone as `--checkout`, CLI 2.27.4, fresh databases, 14:39:04 to 14:40:07, rc=0:
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
rc=0
```
Open alerts on main (gh api GET): 22. The alerts with any location in any of the four handlers were found by intersecting every primary, code-flow and related location of every result with the handler spans (`progs/overlap.py`). Three sources were read: the hosted analysis 2210775080 of main, the local base SARIF and the local head SARIF.
- `POST test`, `describe-table`, `discover-tables`: **0 results**.
- `POST /api/setup/data-sources/:id/test`: **alerts 67 and 68** only (`js/missing-token-validation`, high; primary `server.js:1469` and `:1487`). Each lists the handler as one of 33 related locations, "request handler".
  - At base the region is 17385:46-17571:2.
  - At head it is **17394:46-17583:2, and it contains the three ADDED lines 17395, 17396 and 17397**. Its start line, the registration, is not added.
  - Neither result has a code-flow step in the handler.
  - The local tool keys on start lines, so it does not keep them.

Precedent, re-measured. Pull request 231's base analysis 2201706323 (commit 295f989e) lists the same two alerts with related region 17565-17606. Pull request 231 inserted three lines just after base line 17565, inside that region, in `DELETE /api/setup/data-sources/:id`. Its head f06b080e read CodeQL, Analyze (javascript-typescript), Analyze (actions) and Analyze (python) all `success`, and it merged as 9373976e.

Answer: by the region the hosted check could see the added lines. By the local tool and the one identical precedent it does not block. Not a Major on this evidence; the hosted check on the head decides.

If it blocks, the fix shape is to take the check out of the handler's region without touching the registration line, which is the region's start. One way is a path-level `app.use('/api/setup/data-sources/:id/test', ...)` administrator check mounted after the sign-in middleware (not beside the limiter at `:1405`, which runs before `req.user` is set). Then rerun the local tool and the cells. Never a dismissal.

## SCOPE
- `git ls-remote`: branch at 8af88ee80b47a5f57c8f176690111047a8678e4e, main at b169b8a0eee8eaac594e98918c2ccaff91164dcf. Compare: ahead 7, behind 0, 14 files. Linear, no merge commit. Open PRs 0.
- Exactly the 14 paths, with numstat equal to the commission's list.
- `server.js`: 12 added and 0 removed, in four hunks. The new-side locations are `:15963-15965`, `:15991-15993`, `:16060-16062` and `:17395-17397`, each the three lines right after a registration line. All 12 added lines are the two comment lines plus `if (!(await requireAdminFor(req, res))) return;`, 4 times each. Every other line is byte-equal (0 removed).
- `git merge-tree --write-tree main head` = f5f7094e9981516890032a9e74785f7b3f4b3366 = the head tree (clean).
- Generated inventory files: equal to my drive at head (above).
- Blobs at head: server.js d5590beedf9b, capabilities.js f56e6e346d35, accessAudit.js 935e87edadc4, entraProvisioning.js 4674c7c44c1a. Equal to the kit's predicted blobs.

## TEXT
By program over the 620 added lines and the 7 commit messages (footer line dropped):
- Names (ban list plus the project's list, underscore-aware): 0. A planted control fired 2 and the longer-word control 0.
- B-number, seat id, card or decision ids: 0 (controls fired).
- `product owner`: 0 in messages, 1 in added lines (I-5).
- Ticket keys in messages: RD-1011, RD-1012 and RD-1013 only.
- Non-ASCII introduced net: 0 (0 added, 0 removed). Cf and bidi characters: 0 (control 1).
- Dotted quads: 4, all loopback, in test files.
- GUIDs: 3, the kit's made-up ones. Host names of real services: 0. Key shapes: 0.
- `new RegExp(`, timers, `.skip/.only/.each`, `innerHTML`, `child_process`, `eval`: 0.
- Sensitive names: `clientSecret` (a made-up value, in the cells), `nxToken` and token words of the harness.
- No message attributes any choice to the product owner. A1011 and A1012 say "defaults of the coordinator, not a ruling".
- The ticket's open question is stated in the ticket (RD-1011, last paragraph), in the A1011 message (the reversal sentence; the message does not mention the question itself), in the test header and in pr-body.md and merge-body.txt (stated open).
- Reversal size: one statement per read route, with its two comment lines (3 lines per handler, 6 lines). Regenerate the inventory: two rows. Rewrite rd793 C2 and rd988 T7 (38->36) and rd978's hand list. Cells V2, V3, S2, S3, I2 and I3 would invert.

## PROCESS (builder Corrections 1-9, judged by product effect)
1. A second lock acquisition after its own static row refused. The cause was its own tool. Nothing was committed between; T was made once. No product effect.
2. The frozen-text words "not the product owner's" and old ticket keys in added comments: I-5, no effect.
3. The four stale heads: not live (F-4); continuing was right. The "ahead 10" count is off by 2.
4. The stray `sed -i.bak 1d /dev/null` and a mangled refspec: no file changed. No effect.
5. Partial Step-0 reading (the B1739 kit, the CodeQL README and GATE_STEP.md not read): no product effect seen. The CodeQL step ran and its residual is stated correctly.
6. Run-list counts 79 against 78, union 101 equal: harmless.
7. `node_modules` symlinked: TRUE, and I did the same, to the builder clone's (package-lock sha256 prefix 37e5add354e5 equal). Tooling only.
8. The plants table taken from the drafter as data: true. My own 12 mutants are independent and agree where they overlap (P1-P4 <-> M1-M4; P8/P9 <-> M7/M12 subsets; P12 <-> M11). M5 (F-3) and M9 (I-1) are new.
9. Time: no effect.

Claims graded:
- TRUE: counts 6195/390; red-first 27/20; 47 green twice; inventory four rows and only three fields, `--check` lines; CodeQL rc 0 twice; 14 paths; blobs; push once with head = the verified tree; lock acquisitions 2.
- FALSE: the stale head's "ahead 10".
- NOT SHOWN by me: the builder's 101-file run-list results (I ran 11 of those files plus the full verify, which covers all).

## FOUND / TESTED / HOW
- FOUND: F-1 to F-4 and I-1 to I-7 above. No path by which a signed-in non-administrator reaches the connect code or the stored-source read through the four routes at head.
- TESTED:
  - the route-by-caller matrix over 11 callers x 4 routes, at base and head
  - 13 viewer variants per route
  - 10 sibling routes as viewer and administrator
  - the open window; the configured-but-unfinished window; the setup flip attempts
  - 17 audit targets on the wire and 33 at unit level
  - 6 Entra refusal targets
  - red-first; new files twice; 11 related files; 12 mutants plus P0
  - the inventory drive and `--check`; the full verify on Node 24
  - local CodeQL and the hosted SARIF intersection with the PR 231 precedent
  - text scans; the three tickets read whole by Jira GET (all To Do, 0 comments, updated equal to created)
- NOT TESTED:
  - the hosted Build and hosted CodeQL on the PR merge ref
  - Linux
  - a hosted instance
  - a real workspace or identity provider (connects are counted at the fence and refused)
  - the first-run wizard in a real browser
  - the five primary-workspace sibling routes with a primary workspace configured
  - the debug route's sample-record body on a successful query
  - a race of an administrator's first-run reset against viewer requests, or a second server process on one store
  - the 101-file run list as a separate step (the full verify covers it)
  - the Deploy demo run a landing starts (must read skipped)
- HOW:
  - Everything ran in my own clone and worktrees under `fleet/state/s297/g1776/`.
  - Every jest run and every server boot ran inside ONE acquisition of the NexusAI jest lock, held by a job runner (`progs/runner.sh`, jobs `jobs/j01`-`j07`). That covered the probes at head and base, new files, red-first, mutants, inventory, verify and the debug probe.
  - `NODE_OPTIONS` was unset on every run; `--maxWorkers=2`.
  - The probes were jest files of mine copied untracked into a tree and moved to `_quarantine/` after the run. Their temp folders are left in the OS temp area, not deleted. They booted loopback servers only, with made-up identities and values.
  - Jira: GET only, credentials read in-process by name, never printed. GitHub: `gh api -X GET` only.
  - No push, PR, Jira write, alert action, deploy or variable.
