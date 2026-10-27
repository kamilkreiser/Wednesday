# QA gate: tier 1 (G1): Secuura/Blockchain #1763 (KS-1769)

- **Tier:** 1 (G1: auth-service request-path behaviour change)
- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), subagent of Wednesday. I did not author any of this work.
- **Window:** 2026-10-27 15:57:54Z → 16:03:14Z for the run, plus write-up (2026-10-28 02:57–03:05 AEDT)
- **Workspace:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-1763-1028/` (clone `repo/`, logs `out/`, gate scripts `gate-src/`, TMPDIR `/tmp/g63`)
- **Pushed / merged / commented / edited: nothing.** I ran no git command against `!CODING/Secuura/Blockchain/2_Project_Files` or its worktrees. I used no docker, no az, and no network beyond fetch and ls-remote. I started no long-lived processes, so I stopped none.
- **Gate clone tree at the end:** `git status --porcelain` is empty. My route driver was moved out to `out/_moved/`, and `userRepo.ts` was restored. Its sha256 is `6ea5c4715825adc91140e8f227178f0920f892b1608f13abf4daaad02532e111` before and after both swap runs.

## Pins

Start (`out/ls-start.txt`) and end (`out/ls-end.txt`) are equal to the brief's pins (`diff` is empty). I read them with ls-remote against `git@github.com:Secuura/Distributed_Secuura.git`.

| ref | sha |
|---|---|
| develop | 9b698b7aa1f8a578b2e54a279353dfd7d2d7b34d |
| refs/pull/1763/head | ed9a3147157953143e5c8090ca7949801442d519 |

develop is an ancestor of the head. Three commits: bf17b6513 (cells + docs), 88b9af645 (the catch), ed9a31471 (merge of develop). There are 4 files, +162/−2, matching the brief.

## BLUF

| PR | verdict | worst finding |
|---|---|---|
| #1763 KS-1769 | **GO WITH NOTES** | LOW: "the WHERE builder stays outside the try" is true by reading, but no test can see it. The mutant that moves the builder inside the try survives 0/43. It is an equivalent mutant: the builder cannot throw on the string arguments it receives, and the route runs the list's identical builder first. |

There is no MAJOR or MINOR finding. The claim holds at the route level, through the real router, error handler and **real** `userRepo` (only `db.query` is faked). Both routes answer 500 INTERNAL_ERROR at develop and 503 SERVICE_UNAVAILABLE at the head. A non-infrastructure count fault stays 500 on both sides, and the 200 control is intact.

## Findings

### F1: INFO: the count's catch matches the list's line for line
- Read at the head, `services/auth/src/repositories/userRepo.ts` (under `Blockchain/Dev/`):
  - list catch: `:1049-1055`
  - count catch: `:1098-1104`
- The two are the same except for one token: the log label, `'DB listUsers failed'` vs `'DB countUsers failed'`. That difference is intended.
  - Both log first, with the same payload `{ error: err?.message, code: err?.code }`.
  - Both classify with `isInfrastructureDbError` (imported once at `:26`).
  - Both throw `new ServiceUnavailableError('Authentication service temporarily unavailable, please retry')`. The class (`middleware/errorHandler.ts:77-80`) gives status 503 and code SERVICE_UNAVAILABLE.
  - Both end with `throw err;`.
- In both functions the WHERE builder sits outside the try (list `:1036`, count `:1091`). The list's try covers the query and `Promise.all(fromRow)`. The count's try covers the query and the `parseInt`.
- One divergence exists, but it predates this PR and is harmless:
  - The count's role branch (`:1084-1089`) omits `idx += roles.length`, which the list has at `:1033`.
  - Nothing is bound after it in the count, so the SQL is the same. The PR's FILTERS cells pin this SQL for 5 filter shapes.
- `countUsers` wraps the call in `runWithPlatformScope` (`packages/shared/src/db/tenant-guc.ts:102`, which is `scopeStorage.run`). It neither catches nor transforms errors.

### F2: LOW: the "WHERE builder outside the try" property is untestable (equivalent mutant)
- Mutant M4 moves `try {` above `const conditions`. It parses, and it survives: 0 of 43 cells fail (the ks1186 file's 35 plus my 8 route rows).
- The builder only does string work. `role.split` could throw only on a non-string. The routes pass `(req.query.role as string) || ''`, and an array `?role=a&role=b` would throw first in `listUsersInner`'s identical builder, which also sits outside its try. That gives 500 before the count runs.
- So there is no observable behaviour to pin. I am recording this so nobody reads the FILTERS controls as proving the try's position. They prove the SQL and the bound values, not where the try sits.

### F3: INFO: route level, before and after, through the real repo
- My driver is `gate-src/gate-ks1769-route.test.ts`. It differs from the author's shape in one way: I faked `../db` `query`, not `userRepo`, so `listUsersInner` and `countUsersInner` really run.
- The setup: the real `routes/users.ts` plus the real `errorHandler`, an authenticate stub that injects a SYSTEM_ADMIN, and an HTTP server on 127.0.0.1:0.
- Each mode:
  - **ok:** list `[]`, count `3`.
  - **infra:** the count rejects `ECONNRESET`.
  - **other:** the count rejects code `42601`.
  - **listinfra:** the list rejects `ECONNRESET`.
- For "before", I swapped in develop's `userRepo.ts` (sha256 `8e2be4b5…`) and restored the head's file afterwards. The sha was proven equal (see the header).
- Results (`out/route-rows-{head,develop}.txt`; the order of calls is recorded):

| route | mode | develop | head |
|---|---|---|---|
| GET / | ok (control) | 200 `{"success":true,"data":{"users":[],"total":3,…}}` | 200, same |
| GET / | infra at count | **500** `INTERNAL_ERROR` "An unexpected error occurred" | **503** `SERVICE_UNAVAILABLE` "Authentication service temporarily unavailable, please retry" |
| GET / | other at count | 500 `INTERNAL_ERROR` | 500 `INTERNAL_ERROR` (unchanged) |
| GET / | infra at list | 503 (count never called) | 503 (unchanged) |
| GET /admin/list | ok (control) | 200, total 3 | 200, same |
| GET /admin/list | infra at count | **500** `INTERNAL_ERROR` | **503** `SERVICE_UNAVAILABLE` |
| GET /admin/list | other at count | 500 | 500 (unchanged) |
| GET /admin/list | infra at list | 503 | 503 (unchanged) |

### F4: INFO: my own mutants, all on the gate clone, restored and proven
- Script: `gate-src/mutants.py`. Results: `out/mutants.json` and `out/mutants.txt`.
- Each mutant edits only the body of `countUsersInner`. Each passes an esbuild parse before it runs. Each runs the ks1186 file plus my route driver (43 cells).
- The file's sha256 was `6ea5c471…` before, and restore was proven at the end (`restore_ok: true`).

| mutant | killed? | killing cell(s) |
|---|---|---|
| M1 catch everything as 503 (`if (true)`) | yes, 1 | "control: a NON-infrastructure failure is rethrown as the very same error" |
| M2 swallow non-infra (`return 0`) | yes, 1 | same control |
| M3 log without `code` | yes, 1 | "🔴 the failure is logged once as 'DB countUsers failed' with the error and its code" |
| M4 WHERE builder inside the try | **no, 0** | equivalent (F2) |
| M5 different 503 message | yes, 1 | "🔴 countUsers and listUsers answer one database fault the same way" |
| M6 rethrow wrapped in a new Error | yes, 1 | "control: … rethrown as the very same error" (`toBe`) |
| M7 log only on the infra branch | yes, 1 | "🔴 … logged once …" (the non-infra half) |
| M8 log label `DB listUsers failed` | yes, 1 | "🔴 … logged once …" |
| M9 no catch at all (= the base shape) | yes, 4 | the four 🔴 cells, which matches the author's "4 red at base" |

- My route driver asserts only `status > 0`, so it kills nothing. It is a measuring instrument, not a guard. All kills come from the PR's cells. 8 of 9 mutants are killed. The survivor is the equivalent one.

### F5: INFO: suites at the head
- **ks1186 file:** 35/35, rc 0 (`out/ks1186-head.log`).
- **services/auth full suite (vitest 4.1.12, `--testTimeout=60000`, cwd = services/auth):** 105 files, **1185/1185**, rc 0, 34.6 s (`out/auth-suite-head-cwd.log`). This matches the author's figure.
- First attempt, run from cwd `/Volumes/DevMASTER/WEDNESDAY` with `--root`: 1177 passed and 1 file failed to load. `ks1009-wallet-status-reveals-only-existence.test.ts:172-180` `findDevRoot(process.cwd())` threw "could not locate the Dev root". This is cwd-dependent test setup that predates this PR. It is not a defect of the PR (`out/auth-suite-head.log`).
- **`check:test-types` for services/auth (leg 16):** rc 0. It examined 156 files (105 under `__tests__`), with 42 errors in the baseline, 0 new and 0 stale (`out/typecheck-tests.log`).
- Node v26.8.1 on this host is a Current release, not LTS. Mine and the author's runs share this, and the author discloses it. Nothing was run on Node 24.

### F6: INFO: published contract
- `docs/openapi/secuura-api.yaml`:
  - `/api/users/admin/list` starts at `:16849`. Its GET responses are 200, 400, 401, 403, 429, 500, 502 and **503 at `:16958`**: "Service unavailable — temporary outage or required dependency down", `ErrorResponse`. That matches the author's line number. The new 503 is already declared.
  - **Bare `/api/users` is not published.** 0 matches for `^  /api/users/?:`. Positive control: 10 paths beginning `/api/users` are found by the same search.
- No contract change is needed.

### F7: INFO: collateral
- `git grep -i countUsers` at the head finds the only production callers: `routes/users.ts:465` (GET /) and `:521` (GET /admin/list). Both call `listUsers` first and then `countUsers`. Both use `try { … } catch (error) { next(error); }`.
- No other service, script or systemTest file calls it.
- No test asserted a raw 500 for a failing count: 0 `countUsers` rejection mocks outside ks1186. Every other test file mocks `countUsers: vi.fn(async () => 0)`.
- systemTest schemathesis baseline: `known-issues-and-baseline.md:534/568` `not_a_server_error::GET /api/users/admin/list`, from the 500s at `offset=-1`. That 500 comes from a non-infrastructure Postgres error in the **list** query, which fails before the count runs. It is unaffected by this PR and stays 500, as ruled.

### F8: INFO: docs
- `systemTest/__tests__/support/html_docs_check.mjs` on both docs at the head: rc 0, no findings.
- `systemTest/__tests__/html_docs_matrix.test.sh`: **18 passed, 0 failed**.
- Append-only against develop, by difflib opcodes:
  - Flow Diagrams: one `insert` of 12 lines at line 4981 of 4983. Nothing was deleted or replaced.
  - Cheat Sheet: one `insert` of 22 lines at 5050 of 5052.
- The docs say the work was "measured at base ba9e8fad7f9d", not today's base 9b698b7. That still holds:
  - ba9e8fad is an ancestor of develop.
  - The only difference between the two is one line in the Flow Diagrams doc, with 0 changes under services/auth.
  - The doc's sha256/16 for userRepo.ts, `6ea5c4715825adc9`, equals the head file I tested.
  - So the measured code is the code under review.

## NOT TESTED
- A real `pg` fault against a live Postgres. Every DB call in my driver and in the author's cells is a mock, and classification was driven with a synthetic `ECONNRESET` and SQLSTATE `42601`.
- The gateway in front of auth: whether api-gateway passes the 503 body through unchanged. I made no stack or docker run.
- The four platform suites (Schemathesis, Akto, Playwright, k6). The pre-push hook legs other than leg 16.
- An LTS (Node 24) run.
- Logging content beyond what the mocked logger records. I did not check whether the `error` message could carry PII: it is the pg/socket message, the same as the list's existing log line.
- Deploy. The ticket stays open until auth is deployed, per the author.
