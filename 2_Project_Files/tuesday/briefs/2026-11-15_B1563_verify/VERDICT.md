GO WITH FINDINGS

GATE B1563: GO WITH FINDINGS @ a6eae4f on main 4ba2e03

Tier G1, round 1 of 2 (first gate on this branch). Gate clock 13:10 to 14:30 AEDT 2026-11-15 (`date` in the same programs; hard stop 15:30 not reached).
- Branch `b1563/nexusai-permission-core-audit`, head `a6eae4f17a3dcc77b1563c808fe895ad8cb1d2b7`: A `345cfa2a5b06ae1055a7b08e02959ffb08787709` (five code and test paths) plus K `a6eae4f1` (counts only).
- Main `4ba2e03cc88e928c2c6fdf6694ebed0e7cadf2e5`.
- Own clone by SSH (deploy key as clone-local `core.sshCommand`, push URL `invalid://no-push-gate`, never pushed) at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/g1563/clone`.
- Detached worktrees `head` (head, slot 9), `gbase` (main, slot 18) and `gmut` (head, slot 10). The slots were printed by the helper's own `worktreeSlot()` (`__tests__/helpers/test-server.js:89-94`); none is 1, 4 or 7.

**BLUF.** No Blocker, no Major. The change does what RD-932 row I-122 (part) asks:
- every 401 and 403 below the audit middleware writes ONE REQUEST_DENIED row, reads and HEAD included, with exactly six detail keys and a masked email;
- a refused write writes exactly its unchanged STATE_MUTATION row plus one REQUEST_DENIED row;
- an allowed read and the open window write none;
- a role change writes ONE ROLE_CHANGED row with `roleFrom`, `roleTo` and `changedBy`, only on a real change.

No status changes: the server.js diff only adds lines, and no gate token is added. The merge is clean. CodeQL `security-extended` (the suite the hosted default setup runs) gives 64 results at main and 64 at head, 0 new, and the 64 at main match the 64 open hosted alerts rule by rule.

My work: 15/15 new cells twice; red-first on main 10 red / 5 green; 18 related suites 288/288; eight mutants of my own, every required red received.

Three Minor findings:
- **F1:** a refusal answered inside a mounted router is recorded with the router-relative path. Measured: a viewer's refused `GET /api/setup/entra-provisioning` reads path `/`, and a refused `PATCH /api/feedback/6` reads `/6`.
- **F2:** the flood shape is somewhat worse than the stamp's Q4 states. A refused anonymous write now writes TWO rows (main: one). On a directly reachable server the limiter is keyed by `X-Forwarded-For`, so 600 rotated GETs gave 600 rows in 55 ms with no 429. Main already allowed the same rate of one row per refused POST, so the change is at most 2x and adds reads.
- **F3:** a disclosed out-of-fence write by the builder.

## Findings
| # | Sev | Finding | Evidence / how measured |
|---|---|---|---|
| F1 | Minor | The REQUEST_DENIED row records `path: req.path` (`backend/services/accessAudit.js:50`), as the kit's DESIGN 1 asks (the same field as STATE_MUTATION, `backend/server.js:540`). For a refusal answered inside a router mounted with `app.use('/api/...', ...)`, Express has stripped the mount prefix from `req.url` and does not restore it, because no `next()` follows the refusal. Affected: <br>- the Entra provisioning router's 403 for a viewer, any method (`backend/routes/entraProvisioning.js:165-167`, mounted `server.js:22146`); <br>- the feedback item write gate (`server.js:22108`); <br>- the sustainability config gate. <br>The audit then does not say which route was refused. Old for STATE_MUTATION; every new read row inherits it. Fix later, for both rows, with `req.baseUrl + req.path` (or the path part of `req.originalUrl`). Ticket proposed. | **Probe at head**, real server, enforced shape: <br>- viewer `GET /api/setup/entra-provisioning` 403: row `{"method":"GET","path":"/","statusCode":403,"reason":"forbidden","userEmail":"v***@roles-inventory.test","userRole":"viewer"}`; <br>- viewer `PATCH /api/feedback/6` 403: REQUEST_DENIED `path` `/6`, and its STATE_MUTATION `path` `/6`. <br>**Main:** the same STATE_MUTATION `/6`, no REQUEST_DENIED. <br>**Mechanism**, in-process, no socket (`tools/routerpath.js`, `router@2.2.0` under `express@5.2.1`): `req.url` is `/`, `/scim-token` and `/6` when the response ends (`router/index.js:200-203` restores only in `next()`). |
| F2 | Minor | **Flood shape (stamp Q4), measured.** One audit row is written per refused anonymous request; the only bound is `generalLimiter` (`server.js:1370`, above the audit mount at `:1605`). <br>- **Main:** an anonymous caller could already write rows. The CSRF check is double-submit and compares only header to cookie (`server.js:1556-1566`), so a POST passes it, gets the sign-in gate's 401 (`server.js:2676`) and leaves one STATE_MUTATION row. <br>- **Head:** that POST leaves TWO rows, and a plain GET or HEAD leaves one. <br>- **Production default:** 1000 per 15 min per address (`server.js:1193-1194`). Pushing the 10,000-row ring (`server.js:300`) out from one address takes about 150 min on main and about 75 min at head. <br>- **The bypass:** `trust proxy` is 1 (`server.js:1127`), so on a server reached directly, without an ingress that appends the client address, `X-Forwarded-For` picks the limiter key and the bound is gone, on main and at head alike. The repo's own inventory drive rotates it to get a fresh address per cell (`scripts/role-capability-inventory.js`, `xffFor`). <br>- **The durable store is also bounded:** winston `combined.log` rotates at 5 MB x 5 files (`backend/logger.js:176-179`), so "winston is the durable store" holds only as far as the platform's stdout capture goes. <br>Accepted for this slice by the stamp (Q4). Ticket proposed: coalesce anonymous REQUEST_DENIED per address and per window (one row with a count), and/or drop the second row of a refused write when its STATE_MUTATION row already carries the status. | **Probe** (`probe/zz-g1563-probe.test.js`, real server, `limiters: false` so the dev default 500 / 5 min applies), head vs main: <br>- 600 anonymous GETs from one forwarded address: 401 x500, 429 x100, REQUEST_DENIED rows +500 (main +0); <br>- 200 anonymous POSTs: 401 x200, STATE_MUTATION +200 (main +200) and REQUEST_DENIED +200 (main +0); <br>- 600 GETs, each from a new forwarded address: 401 x600, 0 x 429, rows +600 in 55 ms (main +0 rows; the POST path on main is equally unbounded). |
| F3 | Minor | **Process, builder side, disclosed by the builder:** <br>- its row-shape step (its own addition) created a folder and a machine-id file in the user's home, outside its fences, then moved them into its quarantine (builder STATUS, Corrections 8); <br>- it added cells D6 and D8 and plant P9 beyond the kit. These are additive and allowed. D6 is the cell that pins "a refused HEAD writes exactly one row" (my mutant G8 turns D6 alone red). | Builder STATUS `## Corrections` 8 and `## MUTATIONS`. |
| I1 | Info | **The audit envelope carries a header value.** `auditLog` adds `userAgent` and `ip` to EVERY row (`server.js:304-313`); this is old behaviour, not in the diff. The new `details` carry no header, cookie, query or body value (`accessAudit.js:46-56`, read whole). What changes is reach: a plain refused GET now puts an anonymous user agent into the ring and the log. **Measured, no injection:** <br>- a user agent with ESC/BEL and a path with ESC or TAB are refused 400 by Node's parser before routing (no row, nothing on stdout); <br>- a user agent with obs-text bytes is accepted and logged JSON-escaped; <br>- a user agent built to fake a second `[AUDIT] ROLE_CHANGED` record stays inside one JSON string (lines starting a forged record: 0). <br>An 8000-character path is recorded whole (row path length 8005), the same as STATE_MUTATION on main for writes. No credential reaches a row: `sessionId` reads `no-session`. | Probe C and D at head. |
| I2 | Info | **Two properties rest on source, not on a cell.** <br>(a) ROLE_CHANGED is written after `updateAuthorizedUser` resolves (`server.js:3555` then `:3588-3595`, same try), so a failed update writes none. That is correct at source, but my mutant G3 (the row moved BEFORE the update) survives all 15 cells, because no cell drives a failing update with a stored user. <br>(b) STATE_MUTATION byte-identity is proven by the diff (0 removed lines). D3 pins its keys, status and masked email, but not its values: my mutant G2b (`durationMs` constant) survives, while G2a (email unmasked) turns D3 red. <br>A later test change could add a cell for (a). | Mutation matrix below. |
| I3 | Info | **A client that closes before the answer is sent leaves no read row** (`finish` never fires). It also receives no answer, so it learns nothing. Also listening for `close` would cover it; the kit asked for `finish`. | `server.js:528-530`. |
| I4 | Info | **ROLE_CHANGED and CONFIG_CHANGE carry the full email** as typed in the URL, while REQUEST_DENIED and STATE_MUTATION mask it. This matches the existing role row. It cannot carry CR/LF, because it is written only when the lookup matched a stored user exactly (`jsonStorage.js:3934-3937`). The only role writer in the store is `updateAuthorizedUser` (writers of `authorizedUsersFile`: add, update, last-login, delete; `jsonStorage.js:3961-4005`), so no role-change path is missed. | Source. |
| I5 | Info | **CodeQL `js/user-controlled-bypass` risk is low.** The new condition `req.method === 'GET' \|\| req.method === 'HEAD'` (`server.js:528`) only decides whether a row-writing hook is attached; it guards no authorisation call. `security-extended` flags nothing new at head (user-controlled-bypass 10 = 10). | `cq/head-ext.sarif`. |
| I6 | Info | **Gate process, my own.** My first lock acquisition (14:22:22 to 14:22:32, about 10 s) ran no test: my chain passed relative test paths that jest resolved against the wrong folder ("No tests found"), so no server started. I fixed the path join and took a second, sequential acquisition (14:23:10 to 14:25:26), one waiter at a time, as the B1555 gate did. FIFO: behind b1567-chain (holder from 13:08) and b1568-chain, which left the queue at 14:22. | `logs/waiter.log`, `logs/waiter2.log`, `_quarantine/run1/chain.log`, `logs/chain.log`. |

## Check by check
1. **Refs and scope.**
   - `git ls-remote`: the branch = `a6eae4f17a3dcc77b1563c808fe895ad8cb1d2b7`, main = `4ba2e03c...`. `gh api -X GET .../commits/main` gives the same sha.
   - Open PRs: 0.
   - `gh api -X GET .../compare/4ba2e03c...a6eae4f1`: ahead 2, behind 0. Six paths, equal to OWNS-B1563 (6 of 6): the three tests and `backend/services/accessAudit.js` added; `backend/server.js` +60 -0 and `scripts/verify-expected-counts.json` +3 -3 modified. Commit A has the five; K has the counts file only.
   - Author and committer on both commits are the project's configured noreply identity, the same as every lane commit.
   - `gh api user` login contains "datasec": count 1.
2. **Merge.** `git merge-tree --write-tree main head` rc 0, tree `66dc47f21cbc81c26fe36b6a3548c0e9d35ca241`, which equals the head tree.
3. **Diff at source, read whole.**
   - `backend/server.js` has 0 removed lines; the STATE_MUTATION call and its masking expression are untouched.
   - `requireAdminFor(` 30 -> 30. `role (!==|===) 'admin'` 24 -> 24 in server.js and 0 in added lines (the inventory's gate tokens, `scripts/role-capability-inventory.js:107-108`), so the user PUT gains no gate token and the inventory cannot move.
   - `REQUEST_DENIED` sits only in `AUDIT_ACTIONS` and in `recordDenial`. `recordDenial` is called twice: the GET/HEAD `res.once('finish')` hook and the end of `finalize` (`done` flag, `server.js:554-560`, so `finalize` runs once).
   - No `res.json` or `res.send` is wrapped for reads, so streaming reads are untouched.
   - The masking expression `/^([^@])[^@]*(@.*)$/` is linear: one character, `[^@]*` which cannot cross `@`, then `@.*` once. It is the same expression as before.
   - The CSRF refusal (`app.use(csrfProtection)`, `server.js:1599`) is above the audit mount (`:1605`): no row, correctly out of scope.
4. **Tests in my clone** (all through `nexusai-lock.sh jest g1563-gate`, `NEXUSAI_LOCK_BASE` set, `env -u NODE_OPTIONS`, `--maxWorkers=2`; my bands empty before and after every step; EADDRINUSE 0 in every log):
   - **Red-first on main** (`gbase` with the three files copied untracked, 1 run): 10 red, D1 D2 D3 D6 D7 D8 R1, plus U1-U3 by suite-load failure ("Cannot find module '../backend/services/accessAudit'"). 5 green: D4 D5 R2 R3 R4. This equals the builder's table; the 5 green are the pins of today's answers.
   - **New cells at head:** 15 of 15, two runs.
   - **Related set at head:** 18 suites, 288 of 288 green. These are the four log-injection suites, rd436, rd452, rd497, rd966, rd525, rd615, rd627a, rd324, rd972, auth-gate-fail-closed, rd958, rd929, roles-foundation-route-census and rd978. Per-file counts equal the builder's.
   - **Mutants in `gmut`:** each anchor asserted at count 1, `node --check` passed on dry copies, one run each, then restored by blob (`hash-object` = HEAD blob, porcelain 0 after each).
   | mutant | change | red received | predicted |
   |---|---|---|---|
   | P0 | none | none (15/15) | none |
   | G1 | user-agent header copied into the row | U2, D1, D2, D3, D6, D8 | U2 (+ row-shape cells) |
   | G2a | STATE_MUTATION email unmasked | D3 | D3 |
   | G2b | STATE_MUTATION `durationMs` constant | none (survives; I2) | none |
   | G3 | ROLE_CHANGED written before the update | none (survives; I2) | none |
   | G4 | read hook attached for every method (a refused write gets two REQUEST_DENIED rows) | D3, D7 | D3 |
   | G5 | `changedBy` dropped | R1 | R1 |
   | G6 | `roleFrom` written as the new role | R1 | R1 |
   | G8 | HEAD not hooked | D6 | D6 |
   - **Probe** (`probe/zz-g1563-probe.test.js`, copied untracked into `head` and `gbase`, then moved to `_quarantine/untracked-copies/`): results in F1, F2 and I1. Raw: `raw/probe-head.json`, `raw/probe-base.json`.
5. **Scans** over the 515 added lines and both commit messages (`tools/scan.py`), each with a control that fires:
   - names (the standard ban list plus the commit login), underscore-aware: 0 (each `_by_<name>_` control fires 1; `kamera`/`kamikaze` 0);
   - B-number and seat ids: 0 (control 1);
   - card and decision ids: 0 (control 3);
   - ticket keys: only RD-929 to RD-932;
   - GUIDs: 0;
   - hosts: 0 in added lines (the 2 in the messages are the trailer's noreply address);
   - secret-shaped: 0;
   - non-ASCII: 0;
   - Cf characters: 0 (control 1).
   Hand CodeQL rows: `new RegExp(` 0 (control 1), `.replace(/[` 0, `innerHTML` 0, `eval`/`new Function` 0, `child_process`/`exec(`/`spawn(`/`shell: true` 0, `skip|only|todo|xit|setTimeout|setInterval` 0. **Sensitive-NAME row:** 0 added lines write (logger, console, `auditLog`, `writeFile`, stdout) a value whose name matches password, passwd, secret, token, credential, apikey, api_key, private_key or auth (control fires). The only such words among added identifiers are `getAuthorizedUser` (a store read), the string value `unauthenticated` and `/api/auth/` route strings. The new row keys are `method, path, statusCode, reason, userEmail, userRole` and `email, roleFrom, roleTo, changedBy`. Python paths 0; `.github/` paths 0.
6. **CodeQL pack** (CLI v2.27.4):
   - Setup: databases from `git archive` extracts of main and head, outside the clone (`cq/`), javascript-typescript. The suite is **`javascript-security-extended.qls`**, because the repo has no CodeQL workflow file and `code-scanning/default-setup` reads `query_suite: extended`.
   - Main: 64 results, the same per rule as the 64 open hosted alerts on main (polynomial-redos 11, user-controlled-bypass 10, file-access-to-http 10, missing-rate-limiting 7, remote-property-injection 5, incomplete-url-substring-sanitization 5, prototype-polluting-assignment 3, http-to-file-access 3, file-system-race 3, missing-token-validation 2, insecure-temporary-file 2, loop-bound-injection 1, incomplete-sanitization 1, identity-replacement 1).
   - Head: 64 results, every rule and every rule+file count unchanged, 0 results in the four added files and 0 in the server.js edit windows.
   - (The builder's `code-scanning.qls` run saw 31; this closes that gap.)
   - Hosted alert #237 (`js/http-to-file-access`, the audit flush at `server.js:389`) is an old sink that every audit row already reaches; it is not a new alert.
7. **Deploy demo.** `.github/` is unchanged. `deploy-demo.yml` has `on: push: branches [main]` with `paths-ignore` `**.md`, `docs/**`, `tests/**`. `backend/`, `__tests__/` and `scripts/` are not ignored, so **a merge WILL start Deploy demo**. Both jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'`. Repository variables: `total_count` 0, `CI_DEPLOY_ENABLED` 404. Organisation variables could not be read (403). The last three runs on main (4ba2e03c, ab5a16e9, 27c0b71e) concluded `skipped`, with jobs `build` and `deploy` skipped. A push of the branch starts nothing.

## Builder STATUS claims
| claim | grade |
|---|---|
| six paths, A five + K counts; parent main, unmoved | true (check 1) |
| STATE_MUTATION block byte-identical | true (0 removed lines in server.js; check 3) |
| no gate token added; requireAdminFor 30 -> 30 | true (check 3) |
| REQUEST_DENIED details exactly six keys, no header/cookie/query/body | true for `details` (U2, mutant G1); the envelope carries user agent and address, as before (I1) |
| ROLE_CHANGED only after success and only on a real change | true (R1-R3 green; G5/G6 red); "after success" holds at source but is unpinned (I2) |
| red-first 10 red / 5 green | true (my run, same cells) |
| new cells 15/15 x3 | true (my two runs) |
| related 18 suites, 288 cells green | true (my run, same per-file counts) |
| mutation matrix P0-P9 as predicted | not re-run; my eight mutants G1-G8 give the reds above |
| CodeQL 31 = 31, 0 new | true for its suite; on the hosted suite (security-extended) 64 = 64, 0 new |
| inventory INVDIFF PASS, `--check` 203/203 | not re-measured; consistent with source (no gate token, no status line changed) and the census suites green |
| full verify at K PASS 5651/352 | not re-measured; K's committed pair reads 5651/352; head tree = merge tree |
| merge starts Deploy demo, jobs skipped | true (check 7) |

## NOT RUN
- The full `npm run verify` (optional per the commission; the builder's PASS 5651/352 at this tree stands as its claim; no finding needed it).
- The inventory drive (`--generate` / `--check`).
- Hosted Build, hosted CodeQL on the PR head and the merge commit, gitleaks and npm-audit; Linux.
- The Deploy demo run a landing starts (expected skipped).
- A real ingress in front of the server (F2's bypass was measured on a directly reached server only).
- The builder's P1-P9 plants were not re-run.

## FOR TUESDAY
1. **Landing.** Open the PR from `b1563/nexusai-permission-core-audit` (head `a6eae4f17a3dcc77b1563c808fe895ad8cb1d2b7`, base main `4ba2e03cc88e928c2c6fdf6694ebed0e7cadf2e5`, 2 commits, 6 paths, merge tree = head tree) with `pr-title.txt` and `pr-body.txt`. Wait for hosted Build and CodeQL on that head, then run `landing.txt`: a merge commit pinned to the head; never squash, never rebase. The merge WILL start Deploy demo, and both jobs are expected to read skipped. If main moves first (N129 and N130 each carry a commit K of the counts file), the branch needs a merge of main and round 2 of 2.
2. **Tickets proposed (none blocks this landing):**
   - (a) record the full path (`baseUrl` + `path`) in REQUEST_DENIED and STATE_MUTATION (F1);
   - (b) coalesce or cap anonymous REQUEST_DENIED rows, and decide whether a refused write needs both rows. Note that `X-Forwarded-For` keys the limiter on a directly reachable deployment (F2), a property of `trust proxy 1` that predates this change;
   - (c) a cell for "no ROLE_CHANGED when the update fails" (I2a).
3. **Files written:** this folder, and my work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/g1563/` (clone, worktrees `head`/`gbase`/`gmut`, `cq/`, `raw/`, `logs/`, `tools/`, `probe/`, `_quarantine/` with my untracked copies and the run-1 log). Nothing was deleted. No project tree was written. No push, PR, Jira or message. Two lock acquisitions, one waiter at a time (I6). Every process I started has exited; porcelain is 0 in all three trees.
