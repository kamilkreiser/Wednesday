VERDICT: GO WITH NOTE at head 09e67d9ccd23... (tier 1, round 1 of 2; landing tree 34aebee73a39 on develop ad784e702ca2; 0 blockers, 4 notes)

# Gate AB1: PR #1616 (KS-1645 item 3), tier 1, Opus

Gate AB1, 2026-10-19 08:16Z to 08:25Z. All write verbs ran in my own clone at `scratchpad/ab1/repo` and its worktree `scratchpad/ab1/land`. Nothing was written under `!CODING`, nothing on GitHub or Linear. No `cd`, no `rm`, no Docker, no stderr to /dev/null.

## Heads (ls-remote on the project, read-only)

- At the start, 08:16Z: develop `80868551e679`, #1616 head `09e67d9ccd23f8200653001c94dc3bebe6f17fac`. Both match the brief.
- **Before the verdict, 08:22Z: develop had MOVED to `ad784e702ca205230e39d329abefa8a85fb5946c`** (#1615, KS-1603). #1615 touches 4 files, all under `services/anchoring`, so it does not overlap this PR. I re-ran everything that depends on the landing (see Q4). A last read at 08:24Z gave develop `ad784e702ca2` and the head `09e67d9ccd23`, both unchanged since 08:22Z.
- Merge-base of the head and develop: `722e07f19cee`.

## Q1: Does it refuse exactly the right set?

Instrument: a probe vitest file (`scratchpad/ab1/zz-ab1-probe.test.ts`) in the PR's own harness: the router on a bare express app behind a stub admin, with a recording `fetch` that counts calls. Its output is in `scratchpad/ab1/probe_out.txt`. The file was moved out of the tree after the run.

| Input | Status | Upstream fetches | Forwarded / meta.type | Defensible? |
|---|---|---|---|---|
| each of all, auth, document, admin, billing | 200 | 1 | the value as given (cell C1, and the probe for all and auth) | yes |
| absent | 200 | 1 | `all` / `all` (cell C2) | yes, unchanged behaviour |
| `type=` (empty string) | 200 | 1 | `all` / `all` | yes. `'' \|\| 'all'` treats empty the same as absent, which is what develop did. |
| `type=bogus` | 400 BAD_REQUEST | 0 | none | yes, this is the fix |
| `type=auth&type=admin` (repeated) | 400 | 0 | none | yes |
| `type=auth&type=auth` (identical repeat) | 400 | 0 | none | yes. Strict, and harmless. |
| `type[]=auth`, `type[x]=auth` (qs array or object) | 400 | 0 | none | yes, the `typeof` guard covers these |
| `type=AUTH` (case variant) | 400 | 0 | none | yes. The match is exact and nothing normalises case. |
| `type=%20auth`, `auth%20`, `%09auth` (whitespace) | 400 | 0 | none | yes. Nothing is trimmed, so the input is refused rather than reinterpreted. |
| `type=auth,admin` | 400 | 0 | none | yes |

**Zero-fetch positive control:** the same counter reads 1 on every 200 row.

**Does `AUDIT_TYPES` match what the security service accepts?** Instrument: I read `services/security/src/index.ts` at develop. GET `/api/audit` starts at `:834`, and `:835` destructures only `userId, organizationId, action, resourceType, from, to, limit, offset`. **The security service reads no `type` parameter at all.** Its entries carry no `type` field either: `createAuditLogSchema` (`:631-644`) has `action` and `resourceType`, but no `type`.
- So the list refuses nothing that security supports, because security supports no type filter. **That means this is not a regression.**
- Security also rejects nothing, so nothing is admitted that security would reject.
- What remains is **note N1**: the four non-`all` values are admitted, forwarded, and ignored.

## Q2: Response shape and auth order

Instrument: the probe, plus reading the route code.
- **Envelope:** the refusal body is `{"success":false,"error":{"code":"BAD_REQUEST","message":"Type must be one of: all, auth, document, admin, billing"}}`. This is byte-for-byte the same shape as:
  - the same file's `format` and date 400s (`audit-export.ts:125`, `:130`, `:141`);
  - the sibling route `routes/admin.ts:723`, `Invalid status. Must be one of: ...`.
- **CSV:** `format=csv&type=bogus` returns 400 with no `content-disposition` header (cell T3 and the probe). **Positive control:** `format=csv&type=auth` carries `attachment; filename="audit-logs_..._auth.csv"`.
- **Auth order:** the type check is at `audit-export.ts:117-121`. That is after the 401 check (`:101`) and the role check (`:106-110`), and the router is mounted behind `authenticateToken(true)` (`index.ts:811`).
  - Probe: no user with `type=bogus` returns **401**, 0 fetches. A VIEWER with `type=bogus` returns **403**, 0 fetches.
  - So auth and role still run first, and the refusal does not change who may call the route.
- **Order of the 400s:** the type 400 now comes before the format and date 400s. `format=xml&type=bogus` answers with the type message. This is harmless: it is a 400 either way, with the same envelope and no upstream call.

## Q3: Is red-first real?

Instrument: vitest on the new file, with the route bytes swapped in my worktree.
- **At develop's `audit-export.ts`, with the test file present:** 3 failed, 2 passed, 5 run.
  - T1, T2 and T3 fail on assertions: `expected [ 200, undefined, 1 ] to deeply equal [ 400, 'BAD_REQUEST', +0 ]`. T3 fails the same way with `[ 200, ... ]`.
  - C1 and C2 pass.
  - These are assertion failures, not a load failure.
- **At the head's route:** 5 of 5 pass, so the controls pass at both ends.
- **Mutations** (each one restored afterwards; `git status` was clean after each restore):
  - **M4** reads the first element of a repeated `type`: **T2 goes red** (`[200, undefined, 1]`). **The mutation is killed.**
  - **M5** moves the refusal to after the upstream fetch: **T1, T2 and T3 all go red** on the fetch count (`[400,'BAD_REQUEST',1]`). **Killed.** This is what proves that "never asked" is measured.
  - **M3** keeps the `typeof` guard and drops the membership check: **T1 and T3 go red**, T2 stays green. **Killed.**
  - **M1 and M2** drop the `typeof` guard (the brief's example): **all 5 stay green.**
    - This is an *equivalent* mutant for the inputs express can produce. `includes()` can never match an array or an object, so a repeated `type` is refused either way.
    - The guard exists for TypeScript narrowing and as defence in depth. It is not a gap in the cells, and I record it here only so that nobody reads it as a gap.

## Q4: Landing

Instrument: `git merge-tree --write-tree`, a scratch `commit-tree`, vitest, and tsc. Before every suite run I rebuilt `packages/shared` (`npm run build --workspace=packages/shared`, rc 0) after `npm ci`.

| Check | Original base: develop `80868551e679` | Live develop `ad784e702ca2` |
|---|---|---|
| Landing tree | `b8d59ffc73512d00439c8315410a9ecf28d0f077`, equal to the author's prediction | **`34aebee73a39575a7b88c51b19db3126e353ac72`**, merge-tree rc 0, no conflicts |
| api-gateway suite on the landing tree | **1158 passed of 1158, 118 files**, rc 0 | **1158 of 1158, 118 files**, rc 0. I confirmed blob by blob that the worktree equals tree `34aebee7` before running. |
| Develop baseline (develop's route, new test moved out) | **1153 of 1153, 117 files**, rc 0, which reconciles as +5 cells and +1 file | not run (see the NOT RUN list) |
| `tsc --noEmit -p services/api-gateway` | rc 0, 0 bytes | rc 0, 0 bytes |
| Three-dot diff develop...head | exactly the 2 files, +89/-2 | exactly the 2 files, +89/-2. The landing tree against `ad784e702ca2` is the same 2 files. |

- **tsc positive control:** I planted `const ab1Plant: number = "not a number"` in `audit-export.ts`. tsc returned rc 2 with TS2322 at `(230,7)`, then I restored the file.
- **Suite positive control:** the red-first runs and the M3, M4 and M5 runs above all went red.
- The author's figures (1153 to 1158, 117 to 118, tsc 0) reproduce. **The author's predicted landing tree `b8d59ffc7351` is now stale** because develop moved (note N3).

## Q5: OpenAPI

Instrument: I read `api-gateway.openapi.ts:610-647` and `docs/openapi/secuura-api.yaml:15569+`.
- The spec entry exists, but it declares only `format`, `from` and `to`. **It has no `type` parameter at all**, so there is no enum to compare with `AUDIT_TYPES`.
- This is a note (N2), not a blocker. The conformance and spec tests inside the api-gateway suite all pass (1158 of 1158), and KS-1645 item 4 ("the OpenAPI block disagrees with the route in four places") remains open by scope.

## Blockers

None.

## Notes

- **N1:** the security service ignores `type` entirely: GET `/api/audit` (`security/src/index.ts:834-835`) reads no `type`, and entries have no type field. So `auth`, `document`, `admin` and `billing` still return 200 with *unfiltered* rows, while the filename and `meta.type` name a filter. That is the same defect class, narrowed rather than closed. It is scoped out by the brief as item 3's second sentence ("pin that the filter actually filters"), so **KS-1645 must stay open (Refs, not Closes), and item 3 is not repaired for deploy purposes until that half lands.** The test file's title, "refuses a type it cannot filter on", overstates the fix: the gateway cannot filter on any type today.
- **N2:** the OpenAPI entry for `/api/admin/audit/export` declares no `type` parameter, so the new 400 contract and the five values are undocumented. This belongs to KS-1645 item 4. Conformance in the suite is green.
- **N3:** develop moved to `ad784e702ca2` (#1615, anchoring only, disjoint) during the gate. The live landing tree is `34aebee73a39`, not the author's `b8d59ffc7351`. The merger must re-predict on whatever develop is at merge time.
- **N4:** the api-gateway `tsconfig.json` excludes `src/__tests__`, so `tsc --noEmit` rc 0 says nothing about the new test file. Its type safety rests on the in-suite KS-1090 ratchet cell, which passed inside 1158 of 1158. I did not run that cell in isolation.

## NOT RUN

- the real security service, and any integration or end-to-end run against it (Docker is forbidden here, so the forward-and-ignore in N1 is established by reading code, not by execution);
- the real `authenticateToken(true)` mount with a real JWT (the auth order was probed with a stub user; the KS-1506 mount test passed only as part of the suite);
- schemathesis or any OpenAPI conformance outside the api-gateway vitest suite;
- the author's preflight legs (3, 4 and 8 need Docker), shell suites, and any other service's suite;
- GitHub CI and check-runs, PR body and file counts through the API (the 2 files were verified by git three-dot diff instead), and `mergeable_state`;
- the develop baseline suite on `ad784e702ca2` (run only on `80868551e679`; #1615 touches no api-gateway file);
- the KS-1090 ratchet cell in isolation;
- a real `git merge` (merge-tree plus commit-tree only).

sha256: 4a18100bec91de7581912d7790631c15c5c441a3999161f2ab0e438c96ca7868
