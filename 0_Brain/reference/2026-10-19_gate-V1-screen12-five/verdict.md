VERDICT: #1608 KS-1506 steps 1-2: GO WITH NOTE at head ce638c916fc7d550479ceb4e6f612998a1c14774. No legitimate caller loses access, because on develop no caller had any: the export answered 401 to everyone, admins included. This PR switches a dead admin export ON. It is not defence in depth. Read Q1 and Minor 1-2 before merging.
VERDICT: #1609 KS-1539 info-reader half: GO at head 8e68a262437a60bc4f44f770d530d3115881dde3. No reachable throw on that path has a class name that comes from data. Probe: 0 marker hits, and the control (a class named from data) hit.
VERDICT: #1610 KS-623: GO at head 940b84a9838d9c08a760d06278d214b0b904cfad. Its predicate is byte-for-byte the gateway's parseTestToken predicate. Every harness reaches auth through the gateway, which already refuses unset and staging, so nothing depends on the old behaviour.
VERDICT: #1611 KS-1637 Minor 1 (test only): GO at head 70bea5c98f0aa995744a9b1a8e0594f2b0d22952. I re-ran the mutant: it SURVIVES develop's 6 cells (6/6) and is KILLED on the branch (7/1 of 8, exactly G4).
VERDICT: #1612 KS-1503 Minor 1 (test only): GO at head f0b8fbbe663fd0d3e77d60e55167e799f4f2ea2e. I re-ran the mutant: it SURVIVES develop's 18 cells (18/18) and is KILLED on the branch (19/2 of 21, exactly M1 and M2). tsc gives rc 0 under the mutant.

# GATE V1: the SCREEN_12 five, batched, round 1 of 2

**Method.** Gate Q1's method and format (and through it gate O1's), as the brief says. R 52nd's READY mail is the claim I measured against. I ignored its §4-§5 (#1597), as the brief says.

**Live tip.**
- `git ls-remote` at 16:06 AEDT gave develop `7e2f8157cec243a6255aab2c4fc8678063da317b`, tree `5adb4e513696128baa072f371f8145997c88554d`. That equals the brief. It was re-read at 16:19 and had not moved.
- All five heads equal the brief at both reads.
- Each PR is ONE commit by `Kam Kreiser <kamil.kreiser@secuura.ai>`, so every author is a Secuura identity.
- **R's mail says all five are "on develop ce98606212e4". That is not quite right.** #1608 and #1609 have parent `9512cc70d8c4`. #1610, #1611 and #1612 have parent `ce98606212e4`. It is harmless, measured: `services/api-gateway`, `services/auth`, `packages/shared`, `package.json` and `package-lock.json` have identical tree/blob ids at 9512cc70, ce986062 and 7e2f8157. The two develop moves since (#1606, #1607) touch only `.githooks`, `scripts/` and anchoring. Each solo merge's service subtree equals its head's.
- **#1597 MOVED during the gate.** It was `8ec96bba` and is now `e48c0b821f48ae90c179855f8b77cec90c45013e`, a merge of develop 7e2f8157 into the KS-1634 branch (R's option 2). Its content is still 3 originate files. See Q5.

## Named questions

### Q1. #1608: who calls `/api/admin/audit`, does anyone lose access, and is 401 vs 403 right?

**The finding that matters: on develop the export was unreachable for EVERY caller. The PR does not move a 401; it turns the endpoint on.**
- On develop, nothing sets `req.user` before `index.ts:811`. Grep for `req.user =` / `(req as any).user =` across gateway `src` (tests excluded) finds 5 sites, and every one is inside `authenticateToken` (`middleware/auth.ts:412`, `:454`, `:504`) or admin.ts's own guard (`routes/admin.ts:599`, `:617`). The control: the router's own `req.user` read, `audit-export.ts:99`, is found by the same reader.
- I read every global `app.use` from `:236` to `:584`. None authenticates.
- **Measured:** red-first with develop's `index.ts` gives a SUPER_ADMIN JWT `[401, false]` where the branch gives `[200, true, 1, 'ks1506-entry-1']`. That is cell A1. The PR's own test header says the same ("answered 401 to every caller, an admin included").
- So R's "no caller loses access it should keep" is TRUE, trivially. R's framing "defence in depth; what moves is where the 401 is produced" is **WRONG**: the router's check never produced a 401 for an authenticated caller, because it never saw one.

**Who gains access after the merge**
- The roles in `audit-export.ts:105`: `super_admin`, `SUPER_ADMIN`, `platform_admin`, `SYSTEM_ADMIN`, `ORG_ADMIN`.
- The router forwards the caller's own `Authorization` to security `GET /api/audit` (`audit-export.ts:146-155`).
- That route is behind `jwtAuthenticate` (`security/src/index.ts:775`). It scopes to the JWT's `tenantId` for any non-platform role, and refuses a tenantless caller (`:850-858`, KS-28/KS-743).
- So an ORG_ADMIN gets only its own tenant's rows. This is no new cross-tenant reach, by reading. I did not drive it against a real security service.

**Callers of the mount.** I searched the whole repo with `git grep -i "admin/audit"`, excluding `audit-logs` (control: `admin/audit-logs` matches 21 files).
- **Admin UI, frontends, CI, e2e and scripts: 0 callers of `/api/admin/audit/*`.**
- The only callers are gateway unit tests: ks745, ks1346 and ks1410. Those mount the router bare, so they are unaffected, and all are green on the landing tree.
- Two docs cite a path that does not exist, `GET …/admin/audit?from=…` without `/export`: `docs/STAKEHOLDER-GUIDES.md:718` and `Projects Documents/Stakeholder-Guide-System-Administrator.md:407` (Nit 2).
- `USER_TESTING` probes `/api/admin/audit-log`. That is a different segment, so Express's mount boundary does not match it.
- `systemTest/schemathesis/tests/unit/report/test_verdict.py:66` uses the path only as fixture data.

**Fall-through paths.**
- Develop already sent `/api/admin/audit/<other>` on to `proxy.ts:1237-1241`, which is `authenticateToken(true)` + `enforceAdminProxy` (403). An anonymous caller gets 401 and a non-admin gets 403, before and after.
- **No access change.** The only difference is that `authenticateToken` now runs twice on those paths (Nit 3, unmeasured). No handler serves them.

**401 vs 403: it matches the router's own checks.**
- No credential, a bad JWT, a revoked session, or a connector JWT presented as a Bearer gets 401 from `authenticateToken`. Cells A4 and A5 cover the anonymous and connector cases.
- An authenticated non-admin gets the router's 403 FORBIDDEN (cell A3; develop gave 401).
- A valid `sk_` key becomes `role: 'connector'` and gets the router's 403. I read this; no cell covers it.
- This matches the spec, which declares 401 and 403 ("Admin role required") at `api-gateway.openapi.ts:638-639`.

**`middleware/audit.ts:85`: R's reading is CONFIRMED.**
- The entry is in `EXCLUDED_PREFIXES` (`:79-86`), which is consulted only at `:212` to skip writing an audit row. It plays no part in authentication, and the PR does not change it.
- Two side-effects, both pre-existing:
  - The skip is `startsWith`, so it also suppresses rows for `/api/admin/audit-logs`.
  - Once #1608 lands, the act of exporting the audit trail itself writes no audit row (Observation).

### Q2. #1609: can `errorClass` carry the stored allow-list bytes?

**No. No such throw is reachable on that path.**

**Inputs.** The only statements inside the `try` (`health.ts:63-77`) are:
- `redisService.getNotificationSettings('platform-settings')` (`services/redis.ts:671-678`): an ioredis `get`, then `JSON.parse`, or the in-memory map in fallback mode. Fallback mode is refused earlier at `:55`.
- Property reads, `Array.isArray` and `for…of` over JSON-parsed data. JSON data has no getters and no custom iterators.

**What can be thrown, and what it logs.**
- A parse failure logs `SyntaxError`.
- A client or driver failure logs a fixed library class: the ioredis error classes, or `TypeError` on a null client.
- A non-Error value logs `typeof`.

**Why a class name cannot come from data.** For a class name to come from data, the code on this path would have to construct a class or prototype from it. It does neither. `JSON.parse` makes `__proto__` and `constructor` OWN keys and never sets a prototype.

**Probe** (`v1/probe/errclass.cjs`, the PR's exact expression):

| case | errorClass |
|---|---|
| hostile bytes into `JSON.parse` | `SyntaxError` |
| a parsed `{"__proto__":{"constructor":{"name":"LEAK…"}},"constructor":{"name":"LEAK…"}}`, thrown as-is | `object` |
| iterating hostile `integrations` entries | no throw |
| null client | `TypeError` |
| **control: a class named from data** | **`LEAKMARK_ctrl`** |

**Marker hits outside the control: 0.** The control hits, so the probe can see a leak.

**Other fields and the logger.**
- `route` is a literal.
- `utils/logger.ts:15-19` stringifies only the meta object it is handed. Production uses `json()` (`:24`).
- R's honest boundary stands as stated. It is not reachable today. It would become reachable if a future change threw a value built from the settings.

### Q3. #1610: does anything rely on auth test tokens under an unset or other NODE_ENV?

**No. The predicate matches the gateway's exactly.**
- Auth after the PR (`authenticate.ts:21`): `!['development', 'test'].includes(process.env.NODE_ENV || '')`.
- The gateway (`api-gateway/src/middleware/auth.ts:123-124`): `const env = process.env.NODE_ENV || ''; if (!['development', 'test'].includes(env))`.
- These are the same predicate, so the PR comment's "as the gateway's parseTestToken does" is TRUE.
- The ENABLE_TEST_TOKENS opt-in differs only in WHEN it is read. The gateway reads it at configure time (`index.ts:214`, `auth.ts:92`); auth reads it on every call (`authenticate.ts:25`). This is not part of the claim, and I take no position on it.

**Every harness enters through the gateway.**
- Producers of `test_token_`, outside tests: `tests/e2e/tests/fixtures/api-helpers.ts:31`, the recruitment helpers, and `systemTest/playwright/fixtures/api.fixture.ts`. The schemathesis references are its unit tests.
- I counted references to a direct auth URL (`localhost:6003|4003`, `auth:4003`, `AUTH_SERVICE_URL`/`AUTH_URL`) in each producer and test file. The only hits are inside the gateway itself; the e2e, Playwright and schemathesis files have 0. Control: the same reader finds the gateway's own references.
- The gateway refuses unset and `staging` BEFORE auth is ever reached. So no harness could have been relying on auth accepting those.

**NODE_ENV settings in the repo.**

| file | NODE_ENV | ENABLE_TEST_TOKENS |
|---|---|---|
| `docker-compose.yml:739` (auth) | `development` (hard-coded) | `${ENABLE_TEST_TOKENS:-false}` (`:773`) |
| `docker-compose.yml:427` (gateway) | `${NODE_ENV:-development}` | `:521` |
| `deployments/staging/docker-compose.staging.yml:29-30` | auth AND gateway `staging` | not set |
| `docker-compose.production.yml` | `production` throughout | n/a |
| `docker-compose.e2e.override.yml` | no NODE_ENV | no ENABLE_TEST_TOKENS |
| the auth and gateway Dockerfiles | no NODE_ENV | n/a |

- The gateway also **FATAL-exits at boot** on `staging`, `demo` or `production` with `ENABLE_TEST_TOKENS=true` (`index.ts:79-90`). So a staging stack with test tokens on cannot even boot.
- `.github/workflows/*`: 0 files mention NODE_ENV or test_token. Control: `runs-on` matches 17 files.
- Scripts and systemTest: no NODE_ENV that feeds auth. `ks949_main_seed_idempotence.test.sh:240` sets `NODE_ENV=test` for the seed only.
- I did not re-measure the boxes, as the brief says. R's measurement (development / false) puts both inside the new allow-list either way.

**Observation.** Unlike the gateway, auth has no boot-time refusal for staging or demo with test tokens on. Shared `production-guard.ts:10` only enforces in `production`. After this PR the tokens are refused at parse time anyway.

### Q4. The mutants for #1611 and #1612, re-run by me (`v1/mutants.sh` + `mutate.py`, which asserts one match)

| mutant | develop's cells | branch cells | tsc under mutant |
|---|---|---|---|
| **M1611**: `app.post('/api/documents/:id/verify', …200…)` planted right after `app.use(rejectConnectorBearer());` (`index.ts:584`), so it sits ahead of every route and proxy; 1 marker | **6/6 pass: SURVIVES** | **7 pass / 1 fail of 8, the failure exactly G4**: `[200, null]` vs `[401,'UNAUTHORIZED']`. G-C4 passes | rc 0, 0 lines |
| **M1612**: the front door's `catch` (`middleware/auth.ts:293`) becomes `catch (e) { throw e; …` | **18/18 pass, cell J included: SURVIVES** | **19 pass / 2 fail of 21, exactly M1 and M2**: `[500, false, 0]` vs `[200, false, 1]`. M3 passes | rc 0, 0 lines, so this is a behavioural red and not a load failure |

After each run the blob was restored to develop's (`4817a72ac`, `6dfa84705`), the marker count was 0 and tracked porcelain was 0. **R's evidence is confirmed** for both mutants and both sides.

### Q5. Each PR

**Red-first, reproduced** (`v1/redfirst.sh`). For each PR I swapped develop's product blob into the head worktree, asserted the blob id equals develop's, ran the PR's file, then restored it and asserted the head blob.

| PR | head | with develop's blob | the failures | develop blob → restored |
|---|---|---|---|---|
| #1608 | 5/5 | 2 pass / 3 fail | A1, A2, A3, all assertions (401 where 200, 200, 403 expected) | 4817a72ac → 94d34512e |
| #1609 | 5/5 | 2 / 3 | L1, L2, L3, all assertions (0 warns) | 48aaf4dd3 → 8cbc352a8 |
| #1610 | 6/6 | 4 / 2 | T1 (unset), T2 (staging), both assertions (token accepted) | 9430831cd → 56a50f144 |
| #1611, #1612 | test only | the mutants in Q4 instead | n/a | n/a |

**Suite counts** (vitest, the service's own config, json reporter).
- At the landing parent, develop 7e2f8157: **api-gateway 1117/1117 in 114 files, auth 1078/1078 in 96 files.** Both equal R's baselines at ce98606.
- Each solo landing's service subtree equals its head's (tree ids asserted), so each head run IS the solo-landing run.

| tree | api-gateway | auth | R's figure |
|---|---|---|---|
| #1608 | 1122/1122, 115 files | n/a | 1122/115, match |
| #1609 | 1122/1122, 115 files | n/a | match |
| #1610 | n/a | 1084/1084, 97 files | match |
| #1611 | 1119/1119, 114 files | n/a | match |
| #1612 | 1120/1120, 114 files | n/a | match |
| **chained landing of all five** | **1132/1132, 116 files** | **1084/1084, 97 files** | predicted 1117+15 and 1078+6, match |

`auth.integration.test.ts` (in the unit run): 56/56 passed on both trees.

**`git apply --check` on live develop 7e2f8157** (`v1/applycheck.sh`, through a temporary index).
- All five give rc 0 solo.
- Applied sequentially, all five give rc 0 and **tree f8301c94deacd5621686413e9a51a70465f88a33**, which equals the merge-tree chain.
- Control: re-applying #1608 on top is refused, rc 1.
- Control: a corrupted #1608 is refused, rc 1.

**Chained landing tree** (`git merge-tree --write-tree`, in order 1608 → 1612, onto 7e2f8157; every step rc 0, no conflicts).

| step | tree after | solo onto 7e2f8157 |
|---|---|---|
| 0 develop | 5adb4e513696128baa072f371f8145997c88554d | n/a |
| #1608 | 7149aa0a887b2482a2d9c6b49c5ebd79d5e6800f | 7149aa0a |
| #1609 | 7a9d3cce1157bab87da85ca02d934c9f131f696a | b510ffbf |
| #1610 | 7452b25bb7994c7776f67fc62259f81808dec3a1 | 854b0912 |
| #1611 | 8b4ded4c0ae0b8497af78c08f33c7ac7fde885b2 | bab62da4 |
| #1612 | **f8301c94deacd5621686413e9a51a70465f88a33** | 0e69f152 |

**Files.**
- develop..final touches exactly **8 files**: 2 + 2 + 2 + 1 + 1.
- Intra-batch duplicates: 0.
- #1611 and #1612 edit two different existing test files (ks1628 and ks1470).

**Overlap with #1597: 0 shared files**, at both of its heads.
- At `8ec96bba`: 3 originate files; control self-overlap 3.
- At the new head `e48c0b82` (develop merged in): develop..e48c0b82 is the same 3 originate files.
- `merge-tree` of the five-chain with `e48c0b82` gives rc 0, tree 887273f6.

### Q6. Every touched service's suites

| service | suite | develop 7e2f8157 | landing f8301c94 |
|---|---|---|---|
| api-gateway | `vitest run` (unit; the ONLY config: `vitest.config.ts`, and there is no integration config in the service) | 1117/1117 | 1132/1132 |
| auth | `vitest run` (unit) | 1078/1078 | 1084/1084 |
| auth | **`test:auth-integration`** (`vitest.integration.config.ts`, real PostgreSQL 18.3, scratch cluster on 127.0.0.1:55433, `ks_full` built per `integration/README.md`: init 11/11, migrations 52/52) | **6/6** | **6/6** |

- The migrations directory is identical on both trees (tree id asserted). The cluster was stopped at the end (`pg_ctl stop` rc 0).
- tsc `--noEmit` on the landing tree: api-gateway rc 0 with 0 lines, auth rc 0 with 0 lines.
- **ESLint** (json) on all 8 landing files: 0 errors. The warnings are `index.ts:117` (no-namespace), `index.ts:929` (unused disable directive) and `authenticate.ts:100` (no-useless-assignment). **All three are proved pre-existing:** the same lines, rules and counts on develop's blobs.
- ESLint control: a stdin file with an unused variable reports `@typescript-eslint/no-unused-vars` (severity 1), so the reader sees input.
- R ran neither integration suite. auth's is green on both trees.

## Severities (file:line)

- **Minor 1, #1608 framing. Wednesday should decide knowing this:** the PR ENABLES the admin audit export, which has been dead since it was mounted. It does not harden it. After the merge, 5 roles (`audit-export.ts:105`, ORG_ADMIN included) can download audit rows. Downstream they are tenant-scoped by the forwarded JWT (`security/src/index.ts:850-858`). If KS-1506 was approved as "defence in depth", this is a capability change, and the approval should be read against it.
- **Minor 2, pre-existing and made LIVE by #1608** (want a follow-up ticket, Refs KS-1506/KS-745):
  - The export forwards no `limit` (`audit-export.ts:139-143`), and security defaults it to `'50'` (`security/src/index.ts:835`). So an "export" silently returns at most the 50 newest rows.
  - The `to=YYYY-MM-DD` is compared as midnight (`:866`), so the `to` day is excluded.
  - `type` is sent but never read (`:835`).
  - The spec (`api-gateway.openapi.ts:619-635`) says `from` and `to` are optional datetimes and the JSON is `{entries}`. The router requires both (`audit-export.ts:122`) and answers `{meta, data}`.
  - All of this is by reading, not measured against a real security service.
- **Nit 1, pre-existing:** the router's admin roles (`audit-export.ts:105`) omit `system_admin`, which `PROXY_ADMIN_ROLES` (`proxy.ts:1227`) includes.
- **Nit 2, docs:** `docs/STAKEHOLDER-GUIDES.md:718` and `Projects Documents/Stakeholder-Guide-System-Administrator.md:407` document `GET /api/admin/audit?from=…`, a path with no handler. The route is `/api/admin/audit/export`.
- **Nit 3, #1608, unmeasured:** on `/api/admin/audit/<anything but export>`, `authenticateToken` now runs at `index.ts:811` and again at `proxy.ts:1238`. That doubles the session check, and for an `sk_` key the exchange and the limiter pass too. No handler serves those paths.
- **Nit 4, R's mail:** "all on develop ce98606212e4". #1608 and #1609 are on `9512cc70d8c4`. It is harmless, as measured above.
- **Observation, #1608:** the export is in `EXCLUDED_PREFIXES` (`middleware/audit.ts:85`), so a bulk download of the audit trail leaves no audit row of its own.
- **Observation, #1610:** auth has no boot guard against `staging`/`demo` + `ENABLE_TEST_TOKENS=true`, as the gateway has at `index.ts:79-90`.

## HOW

- **Clone.** `git clone --shared --no-checkout` into `v1/repo`, with origin `git@github.com:Secuura/Distributed_Secuura.git` and the master checkout's `core.sshCommand` + `-o ServerAliveInterval=30`. Fetched through `v1/fetch.sh`.
- **Worktrees** (`v1/wt.sh`, `mkwt.sh`): `wt-dev`, `wt-land` (the chain commit `446190e8`, tree f8301c94) and `wt-1608` to `wt-1612`.
  - node_modules are per-entry symlinks into the master checkout, with the `@secuura/*` links re-created.
  - `packages/shared` was built by tsc (rc 0, 29 dist entries) in each.
- **Runs.** Suites ran by absolute path through `v1/incwd.py`: no `cd`.
- **Scripts:** `chain.sh`, `applycheck.sh`, `solo.sh`, `suites.sh`, `one.sh`, `redfirst.sh`, `mutants.sh`/`mutate.py`, `pg.sh`, `provision.sh`, `integ.sh`, `static.sh`, `f1597b.sh`, and `probe/errclass.cjs`.
- **Hooks.**
  - The no-cd hook refused my first `cd`-style call, an inline `git -C $R fetch`, and a `cp` through `$V/..`. Each was re-issued as a script file or with an absolute path; nothing was bypassed.
  - The zsh `=` hook refused a separator.
- **Clean-up.** Every worktree has tracked porcelain 0 at the end.
- **Writes.** None under !CODING, no GitHub or Linear writes, no Docker, no SSH, no `rm`, and no stderr sent to /dev/null by me.

## NOT tested

- **The PR bodies on GitHub**, including the preflight sentence R says each carries, and the `Refs`/`closes` census. As in gate Q1, I did not use the global gh account.
- **Linear** (KS-1506, KS-1539, KS-623, KS-1637, KS-1503, KS-1643).
- **R's 13/16 preflight legs, and R's 29-PR overlap census.** I checked overlap against #1597 only.
- **#1608 end to end against a real security service**: the tenant scoping, the 50-row cap and the `to` day. All by reading.
- **The `sk_` key → 403 arm of #1608**: by reading only, no cell.
- **The boxes' NODE_ENV for #1610**: not re-measured, per the brief.
- **Suites of services the PRs do not touch** (originate, anchoring, security). No PR here changes them.

MODEL: claude-opus-5-5
WALL-CLOCK: ~16 minutes (16:06 -> ~16:22 AEDT)
sha256: 25a256eafce0fde88baf8a2cde1711ec11c75406815c444f3c5428d4a5aa39f9 (this file with its first line and this last line deleted) | sha256-without-verdict-block: 441a16ce0cd32c0706c1e0d72b85b8417501ba9b3e6a811d6d7b0e9074d1cb46 (lines 1-5 and this last line deleted)
