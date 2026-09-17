# DRAFTER REPORT — #1034 (KS-1215) TIER 1 ROUND 1 gate @ fd81a75f0

Drafted 2026-09-17 23:02:36 → 23:50:41 AEST (clocks from `date`). `GS/` = this directory; every run output is under `GS/out/`.

- **The Secuura checkout:** only read verbs ran there (`ls-remote`, `status --porcelain`, `rev-parse`, `show`, `diff`, `grep`, `cat-file`, `for-each-ref`, `branch --show-current`).
- **The drafter clone:** every build, vitest run, tamper, harness, `merge-tree` and worktree ran in `/private/tmp/claude-501/drafter1034/gate1034_draft_xU29jl/` (worktrees `wt_head` fd81a75f0, `wt_dev` 27e53ec3a, `wt_pre` 0a2b1603f; side install `vitest41111b/`; everything moved aside is under `_quarantine/`).
- Nothing was pushed, filed, commented, merged or mailed. The launcher ran with `--check` only. Nothing was fetched (develop's new commits were already in the checkout's object store, read through the clone's alternates).

## BLUF

- **The HANG (Wednesday's lead) — MEASURED behaviour, PREDICTED reachability:**
  - **Process behaviour (MEASURED, a real tsx node process, not vitest; head AND develop × test AND production; `GS/out/hang_rows.json`):**
    - With `UNHANDLED_REJECTION_MODE` unset (the default, `exit`), a rejection injected into `connectorBearerCache.get` closes the socket with no response. The gateway then runs gracefulShutdown and **exits 0**. The next request and `/health` get ECONNREFUSED: **an availability kill.**
    - With `survive` (the value `docker-compose.yml:441` and `services.bicep:617` set; READ), that one request never answers and the process keeps serving (200, `/health` 200).
    - **Identical on all 8 arms, head = develop.**
  - **Reachability (PREDICTED: none):**
    - READ: both caches are `Map`s, and every fetch or parse in `getConnectorBearer` / `validateApiKey` sits inside a try.
    - MEASURED absence: 6,516 real-app cells over 5 exchange behaviours and 85 routes gave 0 unhandled-rejection lines.
    - #1034 only adds a synchronous `delete` before the await. **#1034 neither created nor widened it: it pre-exists, and a request cannot reach it.** Record, plus a hardening TICKET candidate (the async express-4 middleware has no catch).
  - **A different hang IS request-reachable (MEASURED, both trees):** an exchange that never answers leaves the gateway request hanging, because the fetch has no timeout. The process keeps serving. TICKET candidate.
- **Lead Q1 — the caller's Bearer on the connector branch (MEASURED, real `index.ts`, 3,258 cells per tree, planted control fires; `GS/out/drafter_table.out`):**
  - **develop:** 558 connector-branch cells forward the caller's Authorization.
  - **head:** **24**, **all on `POST /api/platform/organizations/register-connector`**. They go to `/api/tenants`, the security key mint `/api/keys` and `/api/audit`, on EVERY exchange outcome **including OK**, for LIVE and REVOKED callers, in all 3 legs, and every one answers 201.
  - **develop has the same 24.** The cause is `platform.ts:208-213` `authHeaders`, which prefers `rawAuthorization`; `index.ts:345-350` copies that header before any auth runs.
  - Everywhere else #1034 closes it: 534 cells change `user:<session>` → absent (or `''` on the 2 fetch routes). There are 0 status changes and 0 changes on non-connector keys or Bearer-less callers.
  - **The brief's rule makes those 24 head rows a Blocker.** Wednesday should rule before launch (the brief's last section).
- **Predicted verdict:** **NO GO** as drafted (the register-connector rows; round 1 of 2). The fix shape was measured: tamper X-PLATFORM-NO-RAW gives 0 suite reds and 0 forwards on the real app. **GO WITH FINDINGS** if Wednesday rules the forward pre-existing and out of #1034's scope. No other Blocker or Major is in sight on a path #1034 changed.
- **The builder's claims re-derive (MEASURED):**
  - The seat's tamper table: **8 / 8 exactly, 28 reds** (the forms were parsed from its `ROWS` literal; the runner was never executed).
  - Merge-in: tree `6339c404c` = `merge-tree 6c6fdc94e × 27e53ec3a`. The 44 brought files = develop's own delta, blob for blob. Patch-id is equal. `auth.ts` `6e1668362` at both develops.
  - Suites on vitest **4.1.11**: develop 57 / 556, head 58 / 572, 0 failed at default AND at 60 s.
  - tsc rc 0. The test-including program has 32 lines on both trees, 0 in ks1215; the plant adds +1. eslint: 1 pre-existing warning `:415` → `:424`; the control fires.
- **Launcher `--check` rc=0; 20 / 20 controls PASS** (`GS/out/check.out`). It guards by PATH BLOB (24 files) and by GUARDED paths on a develop move, never by develop's SHA.
- **Nothing blocks launching as drafted**, except that Wednesday should settle **RULE BEFORE LAUNCH** first, as with #1032's D1. develop moved twice during drafting (#1031, #1033), both disjoint.

## Outputs

- Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md` (33,926 b)
- Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt` (19,102 b; under 19,800)
- Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1215_1034.sh` (sha256 `8f5bf89bb77780c5`, 243 lines, mode 755)
  - Generated by `gen_launcher_1034.py` from `launch_qa_secuura_ks1194_1032.sh` (`out/gen_launcher.out`, 23:39:08).
  - 29 asserted substitutions, all count 1.
  - Pins re-read from the repo: 24 files at develop `27e53ec3a`; head = develop for the 22 untouched; the 2 PR blobs at head and at the fix.
  - Residual guard over the body (20 tokens), output controls, heredoc parity (PY 0 apostrophes, 8/8 parens; PYJ 0, 101/101), no git write verb, no control bytes, `bash -n` rc 0.
- Verdict subject the prompt carries (exit 23 guards it): `[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0 — <GO | GO WITH FINDINGS | NO GO>`, FROM coagent@ TO wednesday-agent@.
- Scripts: `api_read_1034.py` (GitHub GET, Linear query, AgentMail GET) · `drafter_setup_1034.py` · `drafter_vitest41111_1034.py` · `drafter_farm_1034.py` · `drafter_suites_1034.py` · `drafter_mounts_1034.py` · `drafter_probe_1034.py` + `src/qa1034-drafter-probe.template.ts` (sha256 `28c994357942c227`) · `drafter_table_1034.py` · `drafter_hang_1034.py` + `src/qa1034-hang-harness.template.cts` · `drafter_tamper_1034.py` · `drafter_consequence_1034.py` · `drafter_census_1034.py` · `guard_candidates_1034.py` · `devmove_read_1034.py` · `drafter_merged_1034.py` · `bounds_1034.py` · `make_fixtures_1034.py` (→ `fixtures/`) · `check_launcher_1034.sh`.

## Launcher `--check` (`out/check.out`)

- **rc=0.** The guards read: head on origin; compare `27e53ec3a ahead=2 files=2`; all 24 JUDGED blobs = develop; `origin develop MOVED 27e53ec3a -> 3961c2add: commits=2 files=8 — GUARDED hits 0`; the brief and prompt guards pass.
- **JUDGED by blob at the CURRENT develop (24):**
  - `middleware/auth.ts` `6e1668362` (LANDED `bf09d315a` → 19) and the ks1215 test ABSENT (LANDED `5b7431af0` → 19);
  - `index.ts`, `routes/{proxy,platform,batch,admin,verification}.ts`, `middleware/{rateLimitEnforce,scopes}.ts`, `services/redis.ts`, `utils/trustHeaders.ts`, `db.ts`;
  - the ks1207 and ks480 tests;
  - gateway `package.json` / `vitest.config.ts` / `vitest.setup.ts` / `tsconfig.json`;
  - shared `db/tenant-guc.ts`, `security/session-validation.ts`, `crypto/jwks.ts`, `utils/gracefulShutdown.ts`;
  - Dev `eslint.config.mjs`.
- **GUARDED on a develop move:** `services/api-gateway/src/`, the 4 gateway config files, `packages/shared/src/`, `eslint.config.mjs` → exit 18. `DEV_CONTENT_ALLOWED` is empty.
  - No lockfile is guarded. The gate reads develop's lock vitest version and says which one ran. The #1033 lock move changed mysql2 / seq-queue / sql-escaper / sqlstring only (MEASURED), and the vitest closure did not move.
- **Controls (`check_launcher_1034.sh`), want = got:**

| control | want = got |
|---|---|
| auth.ts fixture = develop bytes `6e1668362` | 0 |
| auth.ts fixture = #1034 bytes `bf09d315a` | 19 LANDED |
| auth.ts fixture = develop + 1 line (`b144eab2d`) | 18 |
| CUR_DEV = `27e53ec3a` (pinned arm) | 0 |
| **CUR_DEV = `732c13459` (a REAL develop move AHEAD, disjoint)** | **0** |
| CUR_DEV = `0a2b1603f` (behind → UNJUDGEABLE) | 18 |
| CUR_DEV = `d127dc7d4` (#923's head: JUDGED `auth.ts` `20311010d` unpinned) | 18 |
| CUR_DEV = `2cab54988` (#1033's head: diverged → UNJUDGEABLE) | 18 |
| CUR_DEV = `fd81a75f0` (#1034 itself) | 19 |
| CUR_DEV = `6c6fdc94e` (the fix commit) | 19 |
| HEAD = `6c6fdc94e` | 6 |
| prompt without the subject / per-ENTRY farm / PRIOR REPORT / NOT-TESTED-first / CLOSED-STILL OPEN-NEW | 23 / 22 / 24 / 24 / 25 |
| brief without MERGE ADDENDUM / full SHA; ROUND 2; TIER 2 | 25 / 20 / 15 / 7 |

- **NOT proven:** the GUARDED compare arm alone. No real commit AHEAD of `27e53ec3a` touches a GUARDED path outside the JUDGED set (`out/guard_candidates.out`: every open PR head is diverged). The launch path (exit 21) was not exercised, per the rule.
- The first full check (`out/check.run1-2339-…out`, 20 / 20, rc 0) ran before develop reached `3961c2add` and the brief was re-pinned. It was re-run on the edited brief with regenerated fixtures.

## Trees (MEASURED, `out/drafter_setup.out`, `out/drafter_merged_*.out`, `out/devmove_read_*.out`)

- **Head** `fd81a75f0`: parents `6c6fdc94e` + `27e53ec3a`; tree `6339c404c`.
  - `merge-tree --write-tree 6c6fdc94e × 27e53ec3a` = the head tree, 0 conflicts.
  - merge-base(fix, develop) = `0a2b1603f`.
  - The 44 brought files = develop's own delta. Every brought blob = develop's; control: not all equal `0a2b1603f`.
  - `27e53ec3a..head` = the 2 PR files (control `0a2b1603f..head` = 46).
  - patch-id `0a2b1603f..6c6fdc94e` = `27e53ec3a..fd81a75f0` = `975abd867785` (control `a8a9de00a26e`).
- **develop moved twice:**
  - `732c13459` (#1031, 3 originate files) → merged `ab870f0e6`;
  - **`3961c2add`** (#1033: the mysql2 override, Dev root and originate `package.json` + locks, `audit-baseline.json`; 8 files vs the pin) → **merged `92256f2dfa07370eba0590fcfcb954e4397824e9`**.
  - Both merges had 0 conflicts. Both have api-gateway `b97a330f3` and shared `dbd72dea0` subtrees = head, and the differing files = develop's own delta.
- **Checkout readings** (`out/bounds.out`, `out/drafter_setup.out`):
  - porcelain 0, 112 worktrees, `.git/config` `f9ef2cb7e4b9fa5a`, branch `feature/ks-597-b-caller-scoped-externalref`, `.vite` present — at 23:08:34, 23:08:41, 23:34:33 and 23:46:14.
  - refs 942 → 944 → 945 (other sessions).
- **Listeners:**
  - 23:34:33: 17 LISTEN rows, 0 node listeners, 0 stubs.
  - 23:46:14 (CLOSE): 19 rows, 2 node listeners with cwd under `gate1035_draft_3nsnlduk` (another drafter, not mine), 0 stubs, **0 under the drafter workdir**.
  - Every probe listener closed in `afterAll`. Every harness child exited 0 (`listen_rows_for_gateway_pid_after` 0 on all 8 arms). `ps` shows 0 leftover qa1034 processes.

## Predictions per lead question

### 1. The caller's Bearer on the connector branch (MEASURED, `out/drafter_table.out`, rows `out/rows_probe_{head,dev}.json`)

- **Harness:**
  - The REAL `index.ts` app, with `../db` mocked (SQL-aware: `INSERT INTO organizations` returns a row) and the session store stubbed.
  - ONE recorder stands in for every `*_SERVICE_URL` and `TENANT_PROVISIONING_URL`. Key validation returns scopes `['*']` (an instrument: maximal reach). The exchange behaves per key: OK, 401, socket destroyed, non-JSON, or never answers.
  - Routes: all 85 `authenticateToken` routes (`out/mounts_head.out`; the census has controls, and head = develop) plus `/api/batch/verify`.
  - Keys × callers: {NOKEY, JUNK, OK, REFUSED, DROPPED, NONJSON} × {NONE, LIVE, REVOKED}.
  - Legs: test `/api` (all), test `/api/v1` (6 routes), production `/api/v1` (all). Production 307 asserted.
- **Probe out of both collectors:** tsc 0 qa_probe (auth.ts listed); `vitest list` 58 files, 0 qa_probe (ks1215 listed). Head run 23:16:13 → 23:21:31; develop 23:21:38 → 23:26:48.
- **Grader control:** a develop N-1 row appended to head is flagged.

| tree | connector-branch cells forwarding the caller's Authorization | where |
|---|---|---|
| develop 27e53ec3a | 558 | every proxied / fetch / platform route (REFUSED / DROPPED / NONJSON) + register-connector on every outcome |
| head fd81a75f0 | **24** | **register-connector only**, OK / REFUSED / DROPPED / NONJSON × LIVE / REVOKED × 3 legs, 201; to `/api/tenants`, `/api/keys`, `/api/audit` |

- Head vs develop: 534 cells differ, and every one is a connector-branch forward `user:<session>` → `absent` (or `''` on `/api/signatories` and `/api/third-party-verifiers`, which send `req.headers.authorization || ''`). There are 0 status differences, and 0 differences on NOKEY / JUNK or on Bearer-less callers.
- Controls on both trees: key-only OK → `connector-jwt` on every hit (181 cells); live JWT alone → the caller's own Bearer on every hit; revoked JWT without a valid key → 0 forwards (401 / 403 / 405).
- **`/api/batch/verify`:** 401 on 54 / 54 cells per tree, live JWT included, 0 hits. The connector branch never runs there, and nothing sets `req.user`: the route family is dead (pre-existing).
- **`POST /api/v1/documents`:** NO-RESPONSE on 13 authenticated cells per leg, both trees (`/api/documents` 200). Pre-existing. The cause (READ, unconfirmed) is the body parser / `proxyPaths` prefix.
- **Prediction:** register-connector = a Blocker row under the brief's rule (pre-existing; RULE BEFORE LAUNCH). N-1 and the split principal are CLOSED on every other route. `/api/batch/*` and `POST /api/v1/documents` are TICKET candidates, not this PR's.

### 2. The HANG (MEASURED behaviour, `out/drafter_hang.out`, `out/hang/*.std{out,err}`, `out/hang_rows.json`)

- **Harness:** `src/qa1034-hang-harness.template.cts`, written as `harness.ts` under `<tree>/Blockchain/Dev/qa_hang_1034/` and run by tsx.
  - It provisions an RS256 keypair, points one recorder at every service, `require`s the real app, and serves it on `127.0.0.1:0`.
  - It patches `connectorBearerCache.get` to throw for `_cachethrow_` keys (an INSTRUMENT).
  - Same-instance control: the patched get printed `ok` on R1 and `cachethrow` on R2.

| arm (both trees identical) | R1 OK key | R2 cachethrow key | process after R2 | R3 OK key / `/health` | log |
|---|---|---|---|---|---|
| test, mode unset | 200 | socket closed, no response | **exited 0** | ECONNREFUSED / ECONNREFUSED | "Unhandled rejection … Received unhandledRejection. Starting graceful shutdown…" |
| test, survive | 200 | no response (5 s timeout) | alive | 200 / 200 | "UNHANDLED REJECTION #1 — mode: survive, process continues (KS-546)" |
| production `/api/v1`, mode unset | 200 | socket closed | **exited 0** | refused / refused | same as test |
| production `/api/v1`, survive | 200 | no response | alive | 200 / 200 | same as test |

- **Modes by deployment (READ):**
  - `survive`: `docker-compose.yml:441` and `deployment/azure/services.bicep:617`. `docker-compose.production.yml` and `deployments/staging/docker-compose.staging.yml` are overrides of the base compose.
  - Unset (= exit): `deploy/docker-swarm/docker-stack.yml` (BACKLOG calls it an unused legacy path), and any bare `node dist/index.js`.
- **Reachability (READ):**
  - `apiKeyCache` / `connectorBearerCache` are `Map`s.
  - In `getConnectorBearer`, the fetch, `resp.ok`, `resp.json()` and `.set` are all inside try. `validateApiKey` is the same.
  - `clientRateLimit`'s Redis calls sit inside try/catch with a second fallback catch.
  - In the connector branch, `createHash().update(apiKey)` takes a string and `runWithTenantId` guards `.length`.
  - A request controls the key string and the upstream response shapes. The probe tried 5 exchange behaviours × 85 routes × 2 trees and found 0 unhandled-rejection lines.
  - **Not tried:** `data: null` / a non-string token / a huge `expiresIn` from the exchange (READ-safe: optional chaining, template string, `Math.min`/`max`).
- **Prediction:** pre-existing; not created or widened by #1034; not request-reachable. **Record + TICKET candidate** (an async express-4 middleware with no catch: any future throw after an await becomes an unhandled rejection and, in exit mode, a process kill).
- **Separately: the exchange no-timeout hang** is request-reachable. Measured in-process: the NO-RESPONSE row, then the app keeps serving; both trees. TICKET candidate, severity for the gate.

### 3. Tampers (MEASURED 23:30–23:33, `out/drafter_tamper.out`, `out/tamper/tamper_table.json`)

- Every row: whole suite **58 / 572 / pending 0** on vitest 4.1.11; tsc 0; anchor 1 pre-asserted against HEAD; restored blob-equal; `git diff --quiet`; 0 non-assertion; load 5.7–13.2.
- **Seat rows** (`ROWS` parsed by a restricted AST evaluator; runner sha256 `8919c3d6b50e9ffd`, never executed):
  - T0 0 · T0-DEFAULT 0 · RP-DEV 9 · DELETE-REMOVED 9 · O1 2 (STRUCTURAL ×2) · AFTER-AWAIT 2 (STRUCTURAL ×2) · NOSET 6 (ks1215 ×4 + ks480 ×2) · TI 0.
  - **8 / 8 = the READY, 28 reds.**
- **Drafter rows:**

| row | form | reds | runtime consequence (`out/drafter_consequence.out`, real app, test `/api`) |
|---|---|---|---|
| X-DELETE-CASED | `delete headers['Authorization']` | 9 (control) | — |
| X-REQUIRED-ONLY | `if (required) delete …` | 5 (control: optional ×3, production, STRUCTURAL false) | — |
| X-EMPTY-NOT-DELETE | `authorization = ''` | 3 (STRUCTURAL ×2 + ks480 "fails closed … no bearer attached") | — |
| X-ONPROXYREQ-RAW | onProxyReq re-adds `rawAuthorization` | 9 (N-1 ×2, split ×2, unreachable ×2, production, key+live controls ×2) | — |
| **X-BEARER-PREFIX-ONLY** | strip only an exact `Bearer ` scheme | **0** | `bearer <live/revoked JWT>` forwarded on `/api/credentials` and `/api/signatories` (4 cells) |
| **X-FETCH-RAW** | `/api/signatories` reads `rawAuthorization` | **0** | the caller's Bearer on 8 / 8 signatories cells, **exchange OK included** |
| **X-PLATFORM-NO-RAW** | `authHeaders` without `rawAuthorization` (a FIX SHAPE) | **0** | register-connector forwards `connector-jwt` (OK) or nothing (refused); 0 caller forwards |

- The consequence BASE arm reproduced the head census on the 3 routes: 8 register-connector forwards, 0 elsewhere, and a lower-case `bearer` is dropped at head.
- **Prediction:** Minor test-coverage findings: no cell on hand-forwarded fetch routes, platform routes or a non-canonical scheme. No cell depends on `rawAuthorization`, so the fix is unconstrained.

### 4. Legitimate callers (READ, `out/census.out`)

- **Upstreams:**
  - 29 non-gateway, non-test lines read the inbound Authorization (control: shared `middleware/index.ts:92`).
  - originate re-forwards it to anchoring (`anchors.ts:277`, `:393`; `certifications.ts:229`, `:404`, `:1129`; `documents.ts:744`, `:806`, `:1044`, `:1332`, …).
  - tenant-provisioning forwards it to security (`index.ts:262`, `:295`).
  - originate reads `x-user-*` (7 lines).
- **Clients:**
  - The JS SDK (`sdk/javascript/src/client.ts:83-87`) and the Python SDK (`client.py:67-70`) send the Bearer **or** the key (else-if).
  - The issuer frontend sends the Bearer only.
  - **0 in-repo clients send both.**
- **Prediction:** a key + live-JWT caller changes only on an exchange FAILURE (served as the human at develop; no Bearer at head → a Bearer-only upstream 401). That is the intended O3 behaviour: Record, no legitimate in-repo flow breaks. Out-of-repo clients (Platform S) are unmeasured.

### 5. Merge-in: above, all MEASURED.

### 6. Checks (MEASURED 23:10:35 → 23:11:21, `out/drafter_suites.out`, `out/drafter_farm.out`, `out/drafter_vitest41111.out`)

- **vitest 4.1.11:**
  - develop 57 / 556 at default and at 60 s, 0 failed, 0 pending (load 9.3 / 8.6).
  - head 58 / 572 both ways, ks1215 16 / 16, 0 failed (load 8.1 / 8.0).
  - The side install's 38 hoisted closure packages match the lock. The farm points 8 entries at it: `vitest.mjs --version` reads 4.1.11, and the `.bin/vitest` control reads 4.1.10.
- **Project tsc:** rc 0 on both trees (491 files, 0 `__tests__`).
- **Test-including program** (`Blockchain/Dev/qa_tsc_1034/tsconfig.json`, outside `services/`, moved to `_quarantine` after):
  - develop: 623 files / 57 tests, rc 2, 32 error lines in 11 test files.
  - head: 624 / 58, ks1215 IN it (not in the project program), 32 lines with an identical map and 0 in ks1215.
  - The plant adds +1 (33 lines, ks1215 1). Restored sha-equal.
- **eslint:**
  - develop `auth.ts`: 0 errors / 1 warning (`@typescript-eslint/no-unused-vars` "'error' is defined but never used." `:415`).
  - head: the same at `:424`; the test 0 / 0.
  - The control (a planted unused const) fires 1 warning at `:304`. Restored.

### 7. Linking (MEASURED 23:04, `out/api_read.out`)

- `attachmentsForURL(pull/1034)` = [KS-1215 contributes In Progress]; controls `pull/1028` → KS-744, `pull/99999` → 0.
- Closing phrases 0 in the title, the body and both commits (regex controls 5 / 5).
- `Refs KS-1215` ×1. KS-1215 In Progress (history Backlog → In Progress 12:59:35Z).
- **Prediction:** KS-1215 stays In Progress (§5f).

## Disagreements with the READY / rulings / commission

1. **The O3 invariant is false on register-connector** (MEASURED): the caller's Bearer reaches the security key mint beside a connector principal, with and without an exchange failure. It is pre-existing, the READY does not list it, and no cell covers it.
2. **The READY's HANG record** ("the real app hangs … shutdown handling ran under vitest") is incomplete.
   - Outside vitest, in the default mode, the process EXITS.
   - In the deployed `survive` mode, only that request hangs.
   - Both are identical at develop.
3. **"/api/batch/* NOT covered":** true, and there is nothing to cover. The connector branch never runs there, and every caller gets 401.
4. **Commission slip:** "the #1028 gate report whose finding N-1 it fixes". KS-1215's source is the **#1023** report's N-1; #1028's N-1 is the illegal-header-character class. The brief names #1023 as the PRIOR REPORT.
5. Everything else re-derived exactly: 8 / 8 tampers, the 28 reds, the tree, the 44 files, `auth.ts` unchanged on develop, 58 / 572, tsc 0, the eslint warning at `:424`, `Refs` / contributes.

## What the drafter could NOT verify

1. A real security service's behaviour on a mint carrying a revoked user's Bearer (the recorder answers 201). Whether the mint authorises by that Bearer is unmeasured, and so is the blast radius.
2. A real auth exchange, real upstreams (whether they 401 a Bearer-less connector), the edge.
3. Exchange / validate response shapes beyond the 5 tried (READ only), and a real Redis limiter under failure.
4. `POST /api/v1/documents`'s cause (READ guess only).
5. The GUARDED compare arm of the launcher in isolation (no real ahead commit), and the exit 21 launch path.
6. Out-of-repo callers (Platform S) that might send a key and a Bearer together.
7. `development` mode, and routes outside the 85-route census (e.g. admin routes wired without `authenticateToken` in the 6-line window).
8. The seat's own tamper JSONs byte-for-byte (forms parsed; outputs not compared beyond counts and titles).

## Drafter slips (kept, not deleted)

1. **The vitest side install, run 1:** pinning `optionalDependencies` (aix / win32 esbuild binaries) failed EBADPLATFORM and installed nothing (`out/drafter_vitest41111.run1-EBADPLATFORM-…out`; dir `vitest41111/` kept). Run 2 left them to npm.
2. **The mount census, run 1** read a fixed 5-line window. It credited `/api/oauth` with `/api/webhooks`' `authenticateToken` and missed `platform.ts`'s multi-line routes (`out/mounts_head.run1-…out`). v2 stops at the next route statement and adds the next line: 72 → 85 routes.
3. **The HANG harness, three failed runs, each kept:**
   - Run 1: `.cts`; tsx did not transform the required `index.ts`; nothing booted.
   - Run 2: my patch appended a comment in the middle of the Python write line, commenting out `.write(...)`. It wrote an EMPTY harness; exit 0 with no output.
   - Run 3: the production arms used unversioned `/api/*` and measured 307s; also, the pid census read the tsx parent, not the gateway child.
   - Run 4 is the one reported. The brief and prompt carry the lessons.
4. **develop moved twice mid-draft.** The brief and prompt were re-pinned from `732c13459` / `ab870f0e6` to `3961c2add` / `92256f2df`, the fixtures were regenerated, and the full check was re-run. The first check is kept.
5. `grep -c` on a multi-line anchor counted lines, not the block. The tamper runner's Python anchor counts are the authority.

## Things Wednesday must read before launching

- **RULE BEFORE LAUNCH (the brief's last section) decides NO GO vs GO WITH FINDINGS.** The register-connector forward is pre-existing, in files #1034 did not touch, and needs a key with `organizations:register`. It breaks O3's stated invariant and matches the lead rule "a forwarded authorization equal to the caller's Bearer on the connector branch = Blocker". As drafted, the gate grades it a Blocker.
- **The HANG lead answers itself as a Record:** not request-reachable, and the same at develop. But the deployments' rejection mode matters (exit = a process kill), and the exchange's missing fetch timeout is a real per-request hang. Wednesday may want those two tickets regardless of the verdict.
- **develop is at `3961c2add` (disjoint).** `--check` passes through the MOVED arm. Re-run `check_launcher_1034.sh` immediately before launching. #575 / #649 / #923 / #995 / #922 trip exit 18 by design if they land first.
- **Run the launcher only in a cockpit pane** (stdin TTY). Never inside a Bash tool, and never without `--check` to prove exit 21.
