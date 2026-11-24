GATE B2039: GO WITH FINDINGS @ 5c98e04 on main d96a83d

# G1 gate, NexusAI lane NX-S1 (RD-1021 + RD-1034), round 1 of 2

- **Reader:** G1 on Opus (claude-opus-5-5), one reader, in-session, read-only toward the project, Jira and GitHub.
- **Window:** 13:00:05 to about 13:10 AEDT, Tue 24 Nov 2026.
- **Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/g2039/` (program `g2039.py` and its output `g2039.out`, `probe.js` and `probe.out`, `rerun.sh` / `rerun.log` / `rerun.json`, `lane.patch`, the gitleaks outputs).

## The lane, re-measured (gh api -X GET, 13:00 and 13:06)
- **Main:** `d96a83d3ee6df25f74bcfe2f9ec0d0b42714e029`, unmoved.
- **Branch:** `b2032/rd1021-data-source-routes-admin` = `5c98e04daa23072c99276125a43b35dc245b4bf7` (the only `b2032` ref).
- **Compare main...branch:** ahead 2, behind 0, merge base = main, 10 files. Commits `14a0f2de` (A) and `5c98e04d` (K).
- **Open PRs:** 0.

## 1. The diff, read whole (`git diff d96a83d3 5c98e04d`, every hunk; the new test file read whole)
- **server.js:** 0 lines removed and 6 added (`diff` of the two whole blobs). Only the two three-line gates, after line 17163 and after line 18393 at BASE. Nothing else in server.js moved.
  - The `requireAdminFor(` count goes from 38 to 40.
  - The added form is identical, token for token, to the four RD-1011 siblings at 15966, 15994, 16063 and 17401: `if (!(await requireAdminFor(req, res))) return;`.
- **Order, by program over the handler bodies at K:**
  - Setup list (handler lines 17163-17245): the first statement is the gate (body line 2). The first data touch (`jsonStorage.` / `getActiveDataSources` / `getDataSourceDecrypted` / `createLawClient` / `testConnection`) is at body line 6.
  - Debug read (18396-18484): the gate is at body line 2; the first touch is at body line 7.
  - In both handlers the gate comes before every touch. The 403 is sent before the first read.
- **Single registration:** each path has exactly one GET registration, and no router mount covers `/api/setup` or `/api/debug`. `git grep -i` over `backend/` lists the path only in the handler, the audit rule of the POST, and capabilities.js.
- **capabilities.js:** the two rows move from `config.read` to the end of `admin.read`, with a two-line comment. The RD-1034 header count and the about text change. Checked by node: `ROUTE_CAPABILITY` has 203 keys and the inventory has 203 rows, the same set. `admin.read` is held by `admin` only.
- **Inventory, by program (BASE JSON against K JSON):**
  - 203 / 203 rows with the same key set. Exactly 2 rows changed: `GET /api/debug/data-sources` and `GET /api/setup/data-sources`.
  - Exactly two meta keys changed: `generatedAt` and `originMain` (= BASE).
  - No other top-level key changed.
  - The four page rows (`/first-run-setup`, `/login`, `/marketplace-landing`, `/status`) equal BASE, so ANSWER-1's dot-free regeneration held.
  - Control: a planted row change is detected.
  - The page diff is 5/5 lines: the stamp, the viewer column for 200 (71 to 69) and 403 (79 to 81), and the two route rows.
- **Counts file:** `_updated`, `tests` 6245 -> 6280 and `suites` 395 -> 396, nothing else.

## 2. Attack (assume a viewer wants that list)

**Role values.** `adminGateRefuses` (`backend/services/authEnforcement.js` line 647) ends `return !(user && user.role === 'admin')`, a strict string equality. The role is re-read on every request from the stored user record: `requireAuth` sets `req.user.role = user.role || 'viewer'`, and a user missing from the local store becomes `'viewer'`. So all of these are refused by construction:
- case variants (`Admin` is tested in R1/R2; `ADMIN` was not run)
- leading or trailing whitespace
- an array such as `['admin']`
- an empty or null role (becomes viewer)
- a role outside the table

**Request shapes, probed with the tree's own Express 5.2.1** (`probe.js` with `trust proxy` 1 as in server.js; loopback only, ephemeral port, no project code; closed itself). Results:

| Shape | Reaches the GET handler? |
|---|---|
| `GET /api/setup/data-sources` (positive control) | yes |
| `/API/SETUP/DATA-SOURCES`, `/Api/Setup/Data-Sources` | yes (Express routing ignores case) |
| HEAD | yes |
| GET with `X-HTTP-Method-Override: POST` | yes, as GET |
| `%2D` / `%2d` encoded paths | no (404) |
| `//api/...`, `/api//setup/...` | no (404) |
| `;x=1` | no (404) |
| OPTIONS | no (404) |
| POST with `X-HTTP-Method-Override: GET` | no; it reaches the POST handler, which RD-793 already gates |

- There is no method-override middleware: `method-override` / `methodOverride` count 0 in package.json and server.js. Control: `"express"` count 1 in package.json.
- The check sits inside the handler, so every shape that reaches the handler meets it, and shapes that do not reach the handler run no read. **Covered (by construction plus probe), not by cells.**
- Side note (no data): `requireAuth` tests `req.path.startsWith('/api/')` case-sensitively. With no session, an upper-case `/API/...` path is answered with a redirect to `/login` instead of 401 JSON. Reasoned, not measured on the real server.

**The open first-run window, after it closes.** Sessions hold no role. The role comes from the user record on each request (above). A session made during the window therefore carries whatever role its user has after the window closes. A non-administrator is refused. A user who made himself an administrator during the window is an administrator, which is the known open-window trust (C-01, RD-1011 open item 4): not a non-administrator bypass.

**API-key and service-token paths.**
- `X-API-Key` appears only in the CORS allow-list (line 1137) and is read nowhere.
- The coordinator secret exempts only the exact path `/api/coordinator-state` (line 2271).
- The SCIM bearer token applies only inside the `/scim/v2` router.
- None of these reaches the two routes.

**Other routes that return the same data-source fields** (`grep getDataSourceDecrypted|getActiveDataSources|getAllDataSources` over server.js, and over the backend by file):
- **F-1 (finding, frame; not a defect of this diff):**
  - `GET /api/data-sources` and `GET /api/data-sources/:id` (`config.read`, capabilities.js line 155; inventory viewer 200) return each source's `name`, `workspaceId`, `authMode`, `tenantId` and `clientId`, with `clientSecret` masked as `'***'` (server.js 15691-15712).
  - Neither route decrypts or connects, so neither is in RD-1021's class.
  - But the *list* the setup route returned stays readable to every `config.read` role. Q-5's refusal withholds the live connection test and its status, not the list.
  - Not filed. Named in FOR-RECORDS (candidate 2), CARD-Q5 and the PR body.
- **RD-1022 (named, not fixed):**
  - `GET /api/log-analytics/status` (viewer 200) returns the primary workspace's `workspaceId`, `authMode`, `tenantId`, `clientId` and `hasClientSecret` (`azureLogAnalytics.js` `getConfigurationStatus`, line 2432 on). It also runs `testConnection()` with the primary's stored credentials: the same fields, and more.
  - `GET /api/log-analytics/test`, `GET /api/setup/validate-all`, `GET /api/setup/discover-tables` and `GET /api/service-check` use the primary client's stored credentials (viewer 200). Their bodies were not read field by field; RD-1022 owns them.
- **By design, not a finding:** a viewer still causes stored-source reads and connects through the dashboard's data path (`getAllPrinterLogs`, server.js 5845-5866, e.g. `GET /api/database`) and through the assistant's `getLawForSource` (line 5246). These return log rows, not source fields. The ticket's "0 stored-source reads" is a per-route statement, and it holds per route.

**Does the counted "stored-source read" count every read?**
- The fence counts calls of `JsonStorage.prototype.getDataSourceDecrypted`. The preload `require`s the same absolute `backend/jsonStorage.js` that the server loads.
- That is the only path that decrypts a data source's secret: `_decryptCandidates` is called at jsonStorage.js 1516 (a settings health probe), 3425 and 3729 (settings), and 4281 (inside `getDataSourceDecrypted`). The server calls no data-source decrypt by any other name.
- The administrator controls A1/A2 count at least one read each, so the counter fires.
- An undecrypted `getAllDataSources` / `getActiveDataSources` read is NOT counted. For the refused requests it does not matter: the gate returns before any `jsonStorage.` call (order above), and `requireAdminFor` itself reads only settings and users (`authEnforcement.js` has 0 `datasource` mentions; control: 13 `signInConfigured`).
- **Verdict: the 0 / 0 for refused callers holds by order, independently of the counter.**

## 3. Frame (stamp checklist item 11): three things the gate is handed that are not the tested shapes
1. **Site states other than "first run complete, users present, sign-in configured" (the only enforced state the test seeds): a STATED LIMIT.**
   - `requireAdminFor` refuses nobody when first run is not complete (including after an administrator's reset) or sign-in is not configured, even where authentication is enforced. In those states a signed-in viewer passes on both routes, as on all 40 call sites.
   - It also returns true when `jsonStorage` is absent; `requireAuth` fails closed in that state.
   - `getFirstRunStatus` answers false on any throw, which opens the shared check. This is pre-existing, and `requireAuth`'s fail-closed read runs first.
   - The kit and the test header name "the open window after an administrator resets first run" and "the sign-in-unproven mode" (that mode refuses everyone) as limits. **"Every non-administrator role is refused" holds only in the configured enforced state.** It should be read that way in the records.
2. **Role values outside the tested ten: COVERED by construction** (strict `=== 'admin'`, role re-read per request; above). Not cells.
3. **Request shapes outside query, slash and HEAD: COVERED by construction plus probe.** STATUS listed upper-case paths and method-override headers as NOT TESTED. They are now reasoned and probed: upper case reaches the same handler and is checked; the override header changes nothing.
4. (Extra) **The same fields on other routes: FINDING F-1**, plus RD-1022's `log-analytics/status` (above).

## 4. Earlier-lane cells that changed meaning (by program over the test diff, `g2039.out` part 3)

| File | Tests BASE -> K | What changed |
|---|---|---|
| rd1011 | 27 -> 27 | 0 assertion lines; comment lines -2 +3 |
| rd793 | 28 -> 28 | two assertion changes: `N2` `toEqual(200)` -> `toEqual(403)` (title "a viewer still reads" -> "a viewer is refused"), and `C2` `toEqual(38)` -> `toEqual(40)` |
| rd988 | 7 -> 7 | one assertion change: `toBe(38)` -> `toBe(40)` (the `requireAdminFor(` count) |
| rd978 | 5 -> 5 | 0 assertion lines; one list line added (the two keys); the title changes twenty-five -> twenty-seven; the assertion is `43 + since` over the list's length, so its meaning is unchanged |

- The only HTTP-status expectation that changed is rd793 `N2` (200 to 403): intended under the Q-5 default. The other two number changes are counts of the gate token, the same pin one step on, as PR 236 did.
- **Confirmed: N2 is the only cell of an earlier lane whose meaning changed.**

## 5. Verify, CodeQL, and the gate's re-run
- **Seat logs** (`.tools/b2032/logs/`):
  - `verify-update.log` and `verify-plain.log` each read `Test Suites: 396 passed, 396 total`, `Tests: 6280 passed, 6280 total`, `VERDICT: PASS — 6280/6280 tests passed across 396 suites (jest exit 0)`. That is the VERDICT twice.
  - `EADDRINUSE`: 0 in each (`grep -i -c`). Control: the VERDICT line is present in each.
  - `v-update.out` / `v-plain.out`: `verify ... rc=0` and `lock-wrapper rc=0`. The plain run's head is `5c98e04d`.
- **CodeQL** (`cq/cq1/cq.out`, `cq.rc`, verdict json): base d96a83d3 against head 5c98e04d, CLI 2.27.4, javascript-security-extended.
  - `results head 29 base 29`; KEPT 0, NEW 0, GONE 0.
  - `RESULT rc 0 PASS`, `cq rc=0`, `cq.err` empty.
  - The verdict json reads `kept [] new [] gone [] kept_high 0 new_high 0`.
- **Gate re-run** (one jest-lock acquisition, tag `g2039-gate-rerun`, in `b2032-nodot/chk24` at K):
  - Before: no listener in band 30880-31519 (lsof rc 1); load 2.07.
  - The lock was acquired and released (`lock-wrapper rc=0`).
  - The new test file, rd1011 and rd793: **90 / 90 passed, 3 suites (35 + 27 + 28)**, 5.7 s.
  - After: chk24 porcelain empty, no `backups/`, no listener left. The gate started nothing that is still running.

## 6. gitleaks
- **Control:** an AWS key-id plus secret pair built by program (`mkctl.py`; not the AWS docs EXAMPLE keys), scanned alone: **rc 1, `leaks found: 2`**.
- **Lane:** `git log -p d96a83d3..5c98e04d` (41298 bytes) through `gitleaks stdin --no-banner --redact`: **rc 0, `no leaks found`**.

## 7. Landing texts (this folder)
`landing.txt`, `pr-title.txt`, `pr-body.md`, `FOR-RECORDS.md`, `CARD-Q5.md`. Key points:
- Merge commit pinned to `5c98e04d` (C-190, never squash).
- `--min-checks 7`, from PR 246's head: CodeQL, scan, build, audit-production-deps, Analyze (python / javascript-typescript / actions).
- A Deploy demo run will start; read its jobs by `head_sha=<M>`. Expect both skipped. If either runs, do not approve the `demo` review and card it under C-224.

## Findings (none blocks landing)
- **F-1 (frame, medium-informational):** the data-source list stays viewer-readable through `GET /api/data-sources` (ids and tenant/client ids, secret masked). RD-1021's fix is the stored-credential use, which it closes. The Q-5 card and the PR body say so; a follow-up candidate is filed in FOR-RECORDS.
- **F-2 (stated limit):** the shared check is open in not-yet-configured and first-run-reset states. "Every non-administrator role is refused" holds in the configured enforced state only. The candidate already exists (the open window after a reset).
- **F-3 (RD-1022, named):** `GET /api/log-analytics/status` returns the primary's tenant and client ids plus `hasClientSecret` to a viewer, and tests with the stored credentials. Add it to RD-1022's measurement.

## Corrections and disclosures (the gate's own)
1. I typed one Bash call containing `cd` (to the seat's `.tools/b2032`). The project hook `pretooluse_no_cd.sh` REFUSED it, nothing ran, and I took the refusal as a STOP for that action. All later calls used absolute paths.
2. `probe.js` is an Express-only loopback probe, not jest and not the project server. It ran outside the jest lock by that reading; it bound one ephemeral loopback port and closed it.
3. Nothing was written under `!CODING`. The jest run's JSON and log went to the gate's scratch folder.
