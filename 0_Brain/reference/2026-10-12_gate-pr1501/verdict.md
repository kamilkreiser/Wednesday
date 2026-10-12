# QA gate: Secuura Platform K PR #1501 (KS-1359)

- Head: `d69e11c6feac3b6fb9e71912ea702aea9b502b93` (confirmed exact, from the bundle; two commits aaf72e8ae, d69e11c6f over base 361537eed238)
- Base the PR was cut from: `361537eed238e9886f4cc22d8a91607a96fb1508`
- Gated against real current `origin/develop` = `06d33fb4b321c77270ff958f9db6accc5a622da8` (KS-1477, services/auth only). I merged the head into it (`gate-merge`, clean merge, no conflict) and ran everything on that merge tree. The author's choice not to merge #1498/KS-1477 in is harmless: it touches none of the same files.
- Gate seat: Sonnet tier, independent. Scratch clone only; nothing written to the project, GitHub or tickets.

## VERDICT: GO WITH NOTE

The one-line product change does what it claims: `limit` above 200 now answers 400 VALIDATION_ERROR with a message naming the bound, no input shape I could construct reaches a 200 over 200 or an overfetch above 5200, the removed 500 clamp is provably dead code, and the three departures from the brief are sound; the notes are follow-ups (a now-stale schemathesis baseline entry, a missing array/repeated-key cell, a pre-existing upstream truncation) and none blocks the merge.

## By my runs

All on `gate-merge` (develop 06d33fb4 + PR head), real `node_modules` of the project symlinked, `@secuura/shared` and `service-utils` rebuilt in my clone (the project's built `dist` was stale against develop and failed 47 files until rebuilt; that was my environment, not the PR).

| Check | Result |
|---|---|
| 16-cell file on head+develop | 16/16 passed, exit 0 (`file_merge.txt`) |
| 16-cell file against the BASE `platform.ts` (head's tests, base's product) | 9 green / 7 red: B5, B6, B7, B8, B9, B10 and the spec cell, each red for the right reason (`[200,null,201]`, `[200,null,500]`, `[200,null,5500]`, `expected 200 to be 400`). Matches the author exactly (`file_on_base_platform.txt`) |
| api-gateway full suite | 112 files / 1085 tests passed, exit 0 (author: 1085; the +9 over 1076 equals the 7 -> 16 cell change, consistent; I did not separately run the base suite) |
| `tsc --noEmit` (api-gateway) | exit 0, no output |
| eslint on both changed files | 0 errors, 1 warning at `platform.ts:990` (`'err' unused`), outside the diff, pre-existing |
| `npm run check:openapi` | CHECK PASS, on-disk YAML matches generated; spec-examples OK (413 blocks) |
| Spec | `secuura-api.yaml` `/api/platform/audit-log` `limit`: `exclusiveMinimum: 0`, `maximum: 200`; zod `.max(200)` in `tenant-provisioning.openapi.ts` |
| Input sweep (31 query shapes, real handler, `probe_inputs.txt`) | see below |

Input sweep, the ones that matter (status, overfetch the SQL LIMIT saw):
- no query: 200, 50 (default intact). `limit=1`: 200, 1. `limit=200`: 200, 200. `limit=201`: 400.
- `limit=0`, `-1`, `abc`, empty `limit=`, `00`, `1e2`, `0x10`, `200.0`, `+200`, `%2B200`, `%20200`, `200%20`, `200%00`, Arabic-Indic digits: all 400.
- `limit=5&limit=500`, `limit=500&limit=5`, `limit[]=500`, `limit[]=5&limit[]=500`, `limit[a]=500`, `offset=5&offset=7`: all 400 (Express 4 extended parser yields arrays/objects; the `typeof string` guard plus regex refuse them).
- `limit=000201`: 400. `limit=0200`: 200 with 200 (leading zeros accepted, value is 200, harmless).
- `limit=200&offset=5000` and `offset=999999999999`: 200, overfetch 5200 (KS-5 offset clamp intact, max overfetch 5200).
- `?LIMIT=500` (wrong case): 200 with default 50, the key is simply unknown, which is the ruled-tolerated behaviour.
- No shape reached 500 or any 200 above the maximum.

Tampers (`tampers.txt`; each applied to my clone, 16-cell file run, restored):

| # | Tamper | Outcome |
|---|---|---|
| neg. control | untouched head | 16/16 green |
| M1 | `MAX_AUDIT_LIMIT` 200 -> 201 | 4 red: B5, B6, B10, spec cell (as predicted) |
| M2 | -> 199 | 4 red: limit-200 edge, offset-clamp control, B10-adjacent, spec cell |
| M3 | `> max` -> `>= max` | 3 red: the limit-200 edge cells, spec cell |
| M4 | drop the `< min` check | 1 red: B3 (limit 0) |
| M5 | drop the max check (pre-PR behaviour with no clamp) | 7 red: B5-B10 and the spec cell |
| M6 | drop the `typeof v !== 'string'` guard | 16/16 GREEN, see Finding 2 |
| M7 | default `\|\| 50` -> `\|\| 500` | 1 red: the no-query default cell |
| M8 | re-add `Math.min(..., 500)` | 16/16 green, an equivalent mutant: proves the clamp removal is behaviour-neutral |
| M9 | YAML `maximum` 200 -> 250 (spec drifts up) | 1 red: the spec-reading cell |
| M9b | zod `.max(200)` -> `.max(250)` | `check:openapi` CHECK FAIL (generated differs from on-disk) |
| M10 | give `offset` a max of 10 | 1 red: the offset-clamp control |

Mine: M2/M3/M4/M6/M7/M8/M9/M10. The author's: B5-B10 + spec cell reds on base reproduced independently (above); M1, M5 and M9 mirror their drift/clamp tampers.

## Findings

Major: none.

Minor
1. Stale accepted-baseline entry for the very defect this PR fixes. `systemTest/schemathesis/config/schemathesis-baseline.json:488` still carries `accepted` -> `by_design_input_tolerance_guard::GET /api/platform/audit-log` (ticket KS-1359, expires 2026-12-31), and `systemTest/docs/known-issues-and-baseline.md:771` still documents DRIFT-AUDITLOG-QUERY-TOLERANCE as open (also line 908 mentions the six `limit=201` genuine failures). With limit now refused, an accepted entry on this operation silently absorbs a future regression of the same guard in the nightly sweep. Not in scope of the PR's two files and not a merge blocker, but it needs a follow-up (retire the entry once a post-merge sweep shows 0), ideally on the KS-1359 ticket. Evidence: the baseline line above.

Note
2. No cell for array or repeated-key limits. M6 (removing the `typeof === 'string'` guard) leaves the file 16/16 green, so the guard is untested. Behaviourally it is nearly redundant (an array of two strings fails the regex through string coercion, and `limit[]=500` coerces to "500" and fails the max), and my sweep shows every array shape is already 400, so there is no defect, only an untested line. That guard predates this PR (PR 1344's shape); a `?limit=5&limit=500` cell would close it.
3. Pre-existing, unchanged by this PR: the gateway forwards `limit + offset` (up to 5200) to tenant-provisioning `GET /api/audit-log`, which clamps at 200 (`services/tenant-provisioning/src/index.ts:555`). So the `platform_audit_log` half of the merge is silently truncated to 200 rows whenever `limit + offset` exceeds 200, and deep pages lose platform entries. The admin UI (25 rows a page) hits it from page 8. Worth its own ticket; this PR neither causes nor worsens it (for limit up to 200 and offset 0 the upstream now gets at most 200, which is satisfied).
4. Departures judged:
   - (1) Replacing the 'above the maximum still clamps' control: correct. It pinned the defect (limit=900 answering 200 / overfetch 5500). Its input is now B8 (refused) and its offset-clamp half survives as 'limit 200 + offset 999999 -> 200 / 5200', which M10 shows is live. Nothing meaningful lost.
   - (2) Spec-reading cell: good. M9 (spec drifts) reds it, M9b (zod drifts) reds `check:openapi`, and it throws when the entry is absent so it cannot pass on nothing. The number 200 still lives in two code places (zod and the handler constant), but a drift between spec and route is now caught by this cell, and zod-versus-yaml by `check:openapi`. Residual: the zod to handler link is only guarded transitively through the generated yaml.
   - (3) Removing the 500 clamp: correct. After validation it cannot fire; M8 shows restoring it changes no cell. Leaving it would have been a false-comfort second bound.
5. Leading zeros are accepted (`limit=0200` is 200) and `offset` stays unbounded above in validation (still clamped to 5000 by KS-5). Both consistent with the ruled behaviour; no action.
6. Lint warning `platform.ts:990` is pre-existing and outside the diff.
7. Unrelated: the YAML's other `maximum: 500` (line 31874) belongs to `/api/system-errors`, not this endpoint.

## Callers of the endpoint

Searched the whole tree (gateway, frontend, packages, services, tests, systemTest, scripts; there is no sdk dir and `mcp-server` src has no reference).

| Caller | Sends limit | Effect of this PR |
|---|---|---|
| `frontend/admin/src/pages/platform/PlatformAuditLog.tsx:29` via `services/api.ts:1031` `fetchPlatformAuditLog(limit=50, offset)` | `rowsPerPage = 25` (constant) | None. Default parameter 50 also under 200. |
| `tests/e2e-v2/tests/tier1-api/multi-tenancy.api.spec.ts:127` | no limit (default 50) | None |
| `tests/e2e-v2/.../admin-management.e2e.spec.ts:179` | UI navigation only | None |
| `ks1215` gateway test (connector key refused 403) | no limit | None; suite green |
| `systemTest/schemathesis` (guard, baseline, tripwire `test_by_design_permissive.py`) | fuzzes `limit=201` | Intended: now 400. Baseline entry is stale, see Finding 1. Not run here (needs a live stack). |
| tenant-provisioning `GET /api/audit-log` (internal upstream) | gateway sends `limit+offset` up to 5200 | Unchanged; see Finding 3. Has its own `Math.min(..., 200)`. |
| export job / sdk / mcp-server | none found | None |
| Sibling clamps | `notifications.ts:126` clamps at 200; a search for any `Math.min(...limit..., 500/1000)` clamp in `services/*/src` returned none (positive control: the 200 clamps were found by the same search) | No sibling accepts up to 500 |

## NOT tested

- Live gateway, real Postgres, a real `super_admin` JWT, nginx or any front proxy (query-string handling at the edge): Docker is down and live systems are out of bounds. The route was driven in-process with the real `createPlatformRoutes` and a fake query, the same harness as the PR's own cells.
- Peter's 2026-10-07 live measurement of 201..500 acceptance was not re-measured; I rely on the base-run reds (`overfetch 201`, `500`) as the equivalent evidence.
- A schemathesis sweep, so I cannot confirm the guard failures for `limit=201` drop to 0; Finding 1 is therefore a recommendation, not an observed failure.
- The base-branch full suite (author's 1076); inferred from 1085 minus the 9 added cells.
- Frontend behaviour beyond reading its call site (no browser run).
- The `systemTest` Python unit tests (`test_valid_as_sent.py` pins `limit=201` as a case fed to a predicate, not a live call; they do not depend on the route, but I did not run them).
- A literal NUL byte in the URL (fetch strips it before sending); the encoded `%00` form is refused.

Evidence files beside this one: `file_merge.txt`, `file_on_base_platform.txt`, `suite_merge.txt`, `tsc.txt`, `eslint.txt`, `check_openapi.txt`, `probe_inputs.txt`, `tampers.txt`, `siblings_clamp.txt` (empty by design; the positive control is in this report).
