GATE B2071: GO WITH FINDINGS @ c1a99d4 on main e291175

# G1 gate, NexusAI RD-1036 (kit B2069, seat N171): the viewer-safe Data Sources tab, round 1 of 2

- **Reader:** G1 on Opus (claude-opus-5-5). One reader, in-session, read-only toward the project checkout, GitHub (`gh api -X GET` only) and Jira (GET only).
- **Window:** 02:31:34 to about 03:02 AEDT, Wed 25 Nov 2026.
- **Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s325/g2071/`. Everything is under one dot-free path, so I created no `!CODING/.../g2071-nodot/`.
  - My own clone, `clone/`: `--no-hardlinks` of the seat's clone, with the branch fetched from it. Its shas equal GitHub's.
  - Worktrees `rf/` (BASE plus the new test file), `work/` (the head, plus my two probe files) and `vk/` (the head, for the verify). Each `node_modules` is a symlink to the seat's `npm ci` (disclosed).
  - Scripts `gate2071.sh` and `gate2071b.sh`, with their outputs `gate.out` and `gate-wire.out`.
  - `logs/`, `raw/*.json`, `probe-tab.out.json` and `probe-wire.out.json`.
  - The gitleaks outputs, and `lane.patch`.
- **Lock:** two jest-lock acquisitions, `g2071-gate` (02:35:38 to 02:57:43) and `g2071-wire` (02:57:52 to 02:57:55). Each was acquired after 0 s with queue-jest at 0 tickets, and each was released with `lock-wrapper rc=0`. The `released/` folder lists both, beside the seat's three `b2069-*`.
- **Runs:** `--maxWorkers=2`, `NODE_OPTIONS` unset.
- **Slots:** rf 9, work 10, vk 0, by the project's `worktreeSlot` formula (control: `b2069-nodot/rf` reads 11, as the kit says). Every band had 0 listeners before and after.

## The lane, re-measured (gh api -X GET at 02:31 and 02:58)
- **Main:** `e29117548b9c41159d2e375fd3f889ec3d1b732d`, unmoved at both reads.
- **Branch:** `b2069/rd1036-viewer-data-sources-list` = `c1a99d4b47930b38813d5dedf55522954a07324d`, the only `b2069` ref.
- **Compare:** ahead 2, behind 0, merge base = main. Three files:
  - `__tests__/rd1036-viewer-data-sources-list.test.js` +322
  - `scripts/verify-expected-counts.json` +3 -3
  - `static/js/admin.js` +27 -0
- **Commits:** A `23b3a023` (parent BASE), then K `c1a99d4b` (parent A).
- **Open PRs:** 0.
- **Code scanning:** 22 open alerts, 0 of them at `static/js/admin.js` (control: 13 at `backend/server.js`).
- **Blobs at the head:**
  - `static/js/admin.js` is `62e1bcb52df4`; BASE's is `dabc44069fe7`.
  - The new file is `f083b8ef80ba`. Its sha256 `46c2dfd9...` equals the kit's frozen file.
  - `backend/**` diff BASE..head: none (`git diff --quiet` rc 0).

## 1. The diff, read whole
- **`admin.js`.** Exactly two insertions, no line removed. Both commit messages and the full patch are in `lane.patch`.
  - The first is in `loadDataSources`, after the setup-list fetch: `if (r.status === 403) { await loadViewerDataSources(list, loading); return; }`.
  - The second adds `loadViewerDataSources` and `renderViewerSourceCard`, before `window.setSourcePrimary`.
  - The administrator's path is byte-identical: `renderSourceCard`, `escapeHtml`, the error handling, and the `!r.ok` throw for every other status.
  - The new loader runs inside `loadDataSources`'s existing `try`. So its own `HTTP <status>` throw, a JSON parse error or a network error lands in the same error box, through `textContent`.
- **Callers.**
  - `loadDataSources` is called in three places: the tab's first opening (admin.js 584), and after a successful `setSourcePrimary` or `setSourceEnabled` (275, 289; administrator writes that refuse a viewer).
  - `first-run-setup.js` has its own `loadDataSources` (line 2336) and does not load admin.js. `git grep` over `static/` shows admin.js is loaded only by `admin.html:181`.
  - `escapeHtml` is unchanged; its seven other callers in admin.js are untouched.
  - **No other caller changes behaviour.**
- **Counts.** `_updated`, `tests` 6300 -> 6323 and `suites` 397 -> 398. Nothing else changes.
- **Messages.**
  - The scan reads: plain ASCII (0 non-ASCII; control 1); name scan 0 (control 3); B-number or seat id 0 (control 3); card or decision id 0 (control 1).
  - "product owner" appears once, in A, as the frozen sentence. It appears 0 times in the added lines.

## 2. Red-first, green, red-proof, full verify (the gate's own trees, one acquisition)
| run | tree | result |
|---|---|---|
| red-first | `rf` (BASE `e2911754`, admin blob `dabc44069fe7`, the new file only) | 23 total, **7 failed: T1, T2, T3, T4, T5, T6, S1**; 16 passed (the wire cells and the controls); 1 suite; no suite error |
| green | `work` (head, admin blob `62e1bcb52df4`) | **23 / 23 passed** |
| red-proof | `work` with ONLY `static/js/admin.js` replaced by BASE's blob `dabc44069fe7` | **7 failed, the same 7 names** (equal sets by program); then restored to `62e1bcb52df4` |
| full verify | `vk` (head, plain `npm --prefix vk run verify -- --maxWorkers=2`, 02:35:45 to 02:57:43, load 1.4 to 2.4) | `Test Suites: 398 passed, 398 total`, `Tests: 6323 passed, 6323 total`, `VERDICT: PASS — 6323/6323 tests passed across 398 suites (jest exit 0)`, `verify rc=0`, `EADDRINUSE` 0, `^FAIL ` 0 (control `^PASS ` 398), vk porcelain empty after |

The seat's logs say the same:
- `verify-update.log` and `verify-plain.log`: 6323 / 398, `VERDICT: PASS`.
- `cq/cq1/cq.out`: `--base e2911754... --head c1a99d4b...`, 3 files / 4 ranges, results 29 / 29, KEPT 0, NEW 0, GONE 0, `RESULT rc 0 PASS`. `cq.rc` reads `cq rc=0`, and `cq.err` is 0 bytes.
- `released/` lists exactly 3 `b2069-*` lock acquisitions.

## 3. Attack on the property (gate probes: `work/__tests__/g2071-probe-tab.test.js` 7/7 and `g2071-probe-wire.test.js` 1/1, observations in the two `.out.json` files)

**(a) Can a non-administrator path on the tab reach a decrypt or a connect?** No. Measured on the real server at the head, through the lane's own boot and counters, which I copied, for each of the 9 non-administrator roles. Each tuple is (status, connects, stored-source reads):

| Request | Result |
|---|---|
| The tab's sequence: setup list | 403 / 0 / 0 |
| The tab's sequence: then the plain list | 200 / 0 / 0, 2 sources |
| `GET /api/data-sources/1` | 200 / 0 / 0 |
| `HEAD /api/setup/data-sources` | 403 / 0 / 0 |
| `GET /API/SETUP/DATA-SOURCES` (upper case) | 403 / 0 / 0 |

- The made-up secret appeared 0 times in every body.
- Control: the administrator's setup list read 1 and connected 1 (one enabled source left after the probe disabled source 2), and its plain list read 0 / 0.
- By reading the code, the setup handler's first statement is `requireAdminFor` (server.js 17166). The plain handler calls only `getAllDataSources`, a file read: no `getDataSourceDecrypted`, no `createLawClient`.

**(b) Can a stored field other than the name and the two marks reach the DOM?** No (jsdom, the shipped functions lifted as the lane does).
- **P1.** I put a marked hostile value (`G2071MARK_<field><img src=x onerror=1>`) in each of 18 other fields: every field `GET /api/data-sources` returns, plus `status`, `error`, `lastTestedAt`, `freshnessThresholdDays` and an arbitrary admin-written field (PUT merges any body key into the stored source). Results:
  - 0 of 18 markers appear in the list's `innerHTML` or text, and the `tables` array does not appear either.
  - The elements made are only `div`, `h5` and `span`, and the only attribute is `class`.
- **P2.** Names of 14 shapes:
  - `42`, `0`, `null`, missing, `true`, `false`, `NaN`
  - an object (shows `[object Object]`) and an array holding `<img onerror>`
  - a 1,080,000-character `<script>` string
  - `</h5><script>`, `"><svg onload>`, a U+202E bidi name, and pre-escaped `&lt;`

  All 14 render as text in 14 cards. The elements made are only `div` and `h5`, and no attribute but `class` appears.
- **P5.** A 200 that is not an array (`{error}`, `null`, a string, an array-like object, a number) shows `No data sources configured.`. A 200 that is not JSON shows its parse error in the error box.

**(c) Can an administrator be shown the plain list instead of the error box or their own card?** Yes, in one known state; see F-1.
- The branch reads `r.status === 403` only (P7: a 403 whose body looks like a success still takes the plain path). So the question is which 403s an administrator can receive from the setup list.
- No global middleware sends 403 on a GET: the CSRF check skips GET, and the limiters send 429.
- `requireAdminFor` → `adminGateRefuses` returns true for EVERYONE while sign-in is unproven (authEnforcement.js, the RD-535 branch). Measured by calling the exported function: `admin, signInUnproven -> true`; control `admin, configured -> false`.
- In that state the administrator's tab now shows the plain cards and the line "Connection status and source settings are shown to administrators." instead of `HTTP 403`. **F-1.**
- The open first-run window: the setup list answers everyone 200. The tab shows the administrator's card to any caller. This is unchanged from BASE (C1 is the tested instance of a 200).

**(d) Does another caller of `loadDataSources` or `escapeHtml` change behaviour?** No (section 1).

**(e) Does the change add a request a viewer did not already make?** Yes, one, to a route the viewer was already granted:
- One `GET /api/data-sources`, on the tab's first opening only (`btn._loaded`), after the refused setup list.
- The same viewer already makes this request on the dashboard (`static/js/index.js` ~4288, every role).
- The request is a GET, so `auditMutationMiddleware` skips it. It counts against `generalLimiter` (`/api/`).
- No other request was added. Statuses 200, 401, 404, 405, 429, 500, 502 and 503 make exactly one request (P6).
- **Info.**

## 4. Stamp checklist item 11: three shapes per property beyond the tested ones
- **No decrypt or connect:**
  - (1) `GET /api/data-sources/:id`;
  - (2) HEAD on the setup list;
  - (3) an upper-case setup path.

  All three were measured at 0 / 0 for 9 roles: COVERED by the gate's probe.
- **No other field in the DOM:**
  - (1) hostile values in all 18 other fields;
  - (2) 14 non-string or hostile names, including 1.08 MB;
  - (3) non-array 200s and a non-JSON 200.

  COVERED by the probe. The limit is jsdom (it renders no layout and runs no script written by `innerHTML`). `escapeHtml` escapes `& < > " '` into an element text context, which is safe in a real browser by construction.
- **Administrator never shown the plain list:**
  - (1) a 403 whose body is a success: takes the plain path by design (P7);
  - (2) the sign-in-unproven state: **FINDING F-1**;
  - (3) setup-list statuses 401, 404, 405, 429, 502 and 503: COVERED by probe (error box, one request).
- **Marks:**
  - (1) `isPrimary: "false"` (a string) shows `primary`;
  - (2) `enabled: "false"` or `0` shows no `disabled` mark;
  - (3) a `null` array element turns the whole tab into the error box ("Cannot read properties of null (reading 'isPrimary')").

  (1) and (2) are the administrator card's own semantics, unchanged. The server writes booleans from its own UI, but `PUT` accepts any JSON: **Info F-5.** (3) cannot come from the server, which writes objects: **Info.**

## 5. Q-0, stated honestly (`backend/server.js` at the head, lines 15691-15712; the server is unchanged by this lane)
**The wire is unchanged by this lane.** What `GET /api/data-sources` and `/:id` return to each role today:
- **Anonymous (enforced):** 401, from `requireAuth`.
- **Every signed-in session, whatever its role:** 200. There is no handler gate. `capabilities.js`'s `config.read` row is descriptive only: no backend or scripts file requires the table (`git grep` returned 0; it returns 7 test files; control: `authEnforcement` has 2 backend requirers).
  - Measured 200 with both sources for all 9 non-administrator roles. That includes `end_user`, `partner_manager` and `partner_technician`, which the table says do NOT hold `config.read`.
  - Each source carries 17 keys: `apiEndpoint, authMode, clientId, clientSecret ('***'), created_at, department, enabled, id, isPrimary, name, region, tableName, tables, tenantId, updated_at, vendor, workspaceId`. It also carries any key an administrator's PUT ever merged in.
- **The administrator:** the same.
- **Open mode:** 200 to anyone.

Nothing is decrypted, nothing connects, and the secret is masked. The exposure is identifiers and settings. The tab now shows less than the wire carries; a viewer's browser still receives the full list in the network response. **F-Q0 (Major, pre-existing, NOT this lane's, does not block landing).** The product owner was told on the card. FOR-RECORDS proposes it as a separate ticket.

## 6. gitleaks and name scan
- **Control:** an AWS key-id plus secret pair built by program, not the docs' EXAMPLE keys, scanned alone: **rc 1, `leaks found: 2`**. The plant file was moved to `g2071/_quarantine/plant.txt`, not deleted.
- **Lane:** `git log -p BASE..head` (24252 bytes): **rc 0, `no leaks found`**.
- **Commit messages alone:** **rc 0, `no leaks found`**.
- **Name scan** (the four plain names of `scanlib1114.py` line 20, word-bounded) over the added lines and the messages: 0 (control 3).

## 7. Jira (GET only, the seat's GET-only reader; output to my scratch; 0 credential-shaped strings in it)
RD-1036 reads To Do, Task, labels `records-pass-1124,security`, 0 comments, description 3541 characters. This matches the seat's read.

## Findings
| id | grade | blocks landing? | what |
|---|---|---|---|
| F-Q0 | **Major (pre-existing)** | **No**: not this lane's (STAMP Q-0) | The plain route returns 17 stored keys (ids, endpoint, settings; secret masked) to EVERY signed-in role. That includes 3 roles the permission table says lack `config.read`, because the table is not enforced. The lane leaves the wire unchanged and says so. Ticket proposed in FOR-RECORDS. |
| F-1 | Minor | No | Sign-in-unproven state: `requireAdminFor` refuses the administrator too, so the administrator's tab now shows the plain cards ("...shown to administrators.") instead of `HTTP 403`. Nothing is shown beyond what the route already returns to that caller. Three texts misstate it and should be corrected in the records, not in the code: the kit's limit ("none is known"), STATUS, and commit A ("An administrator's tab is unchanged"). The PR body names it. |
| F-2 | Minor | No | Parity: the administrator's setup list omits disabled sources (`getActiveDataSources`), while the viewer's list includes them with the `disabled` mark. So a non-administrator sees source names the administrator's tab hides. T2 pins `rd1036 beta disabled`, a mark the administrator's tab cannot show. Pre-existing on the administrator's side (the `Enable` button is unreachable). It needs a product decision; it is named in the PR body and FOR-RECORDS. |
| F-3 | Info | No | W1 asserts the 200 only for roles that hold `config.read`. The three roles that do not are answered 200 too (measured by the gate, unasserted by the lane). Fold this into the Q-0 ticket. |
| F-4 | Info | No | One added request per first opening of the tab for a non-administrator (`GET /api/data-sources`). The route was already granted to that viewer and already called by the dashboard; GETs are not audited, and it counts against the general limiter. |
| F-5 | Info | No | The marks read truthiness and `=== false`, as the administrator's card does. Non-boolean stored values (`"false"`, `0`) mis-mark, which is cosmetic. A `null` element blanks the tab into the error box. Neither shape is written by the server's own UI. |

No Blocker. The property holds:
- A non-administrator's tab makes no decrypt and no connect.
- Only the name and the two marks reach the DOM.
- Every non-403 failure is unchanged.

It holds with F-1 as the one administrator exception, which shows less than the route already returns and adds no exposure.

## FOR TUESDAY
- Landing per `landing.txt`: merge commit pinned to `c1a99d4b`, `--min-checks 7` (distinct names; PR 250 and PR 248 heads carried 8 runs over 7 names), Deploy demo read skipped, C-224 hold.
- The PR title and body carry no person's name and no card id. The field choice is named as the coordinator's, within ruling b. Q-0 is named as open, and F-1 and F-2 are named.

## Corrections and disclosures (the gate's own)
1. **Hook refusals.** Two Bash calls were REFUSED by `pretooluse_no_cd.sh`, because the hook cannot resolve a shell variable in a `git -C` path and treated a clone or worktree into my scratch as a write outside TUESDAY. Nothing ran. I re-issued each with literal paths inside my scratch.
2. **Probe files.** My two probe files live only in my scratch `work/` tree, never in the project or on the branch.
   - The wire probe's server temp dirs (`/var/folders/.../T/nx-g2071-*`, `nexusai-g2071-wire-*`) were left in place rather than removed, under the never-delete rule. They are listed in `probe-wire.out.json`.
   - The full verify ran in `vk`, which held no probe file, so its 6323 / 398 is the lane's own count.
3. **Writes outside my folders.** Nothing was written under `!CODING` except the jest lock's own bookkeeping in `session-tools/locks-laptop-1017/` (two acquisitions, released).
4. **Not run.**
   - A real browser.
   - The sign-in-unproven state on a running server. F-1 is the exported gate function measured, plus code reading for `requireAuth`'s open-mode path.
   - The 27-suite set of the seat's lane. The full verify covers it.
