PR 2242: GO WITH NOTES (at head 62ecc89eafdb4de83a4ca46cd999a856ed273776; tier 1)

# QA GATE 367, tier 1 (G1), PR 2242, KS-1703 analytics exports half. Findings only.

Gate seat: Opus (claude-opus-5-5), 2026-11-16 02:0x AEDT (15:0xZ). Nothing fixed, posted, mailed, pushed, merged or written to Linear/GitHub. No write under `!CODING`. All work in `scratch/`.

## Pins (gh api, GH_CONFIG_DIR = Blockchain's)
- Head re-pinned at start and at 15:07:55Z: `62ecc89eafdb4de83a4ca46cd999a856ed273776`. The PR is open with 1 commit, its parent is `dbb053b756ae`, and it changes 7 files (+580 -2). mergeable_state is unstable.
- develop at both reads: `6fdba4e013b384c7d1f60d36327491ff61e6476c`. PR 2188 is still open at `6e5c116d9b9d`.
- My own copy: `scratch/mirror.git` is a `--mirror --no-local` clone of the builder's worktree. It is read only there, and its remote is disabled. The commit objects are content-addressed, so the SHAs above prove the content. Worktrees are in `scratch/wt-head`, `wt-base` and `wt-dev`, plus `wt-merge` (develop + head). I ran `npm ci` in my own copy (rc 0, 22 s) and built `@secuura/shared`.

## Verdict basis, question by question

**(1) Every refusal is exactly the unknown-id answer.** The PR's cells hold. I also wrote my own 54 cells (`scratch/cells/g367-ks1703-exports-gate.test.ts`). They cover 22 refusal classes:
- OWNER, USER, ORG_ADMIN, ISSUER_ADMIN, `admin` and `platform_admin` callers of another company.
- The creator's own userId with another tenant.
- No tenant on a tenanted export.
- A tenant that is a substring of the creator's, an upper-cased tenant, and an array tenant.
- An array role, an object role, a number role, a dotless-i role and a role with a trailing space.
- No `req.user`.
- On a tenant-less creator's export: another tenant-less user, a tenanted user, and an empty userId.
- On an export with no owner: a same-tenant OWNER and an ORG_ADMIN.

For every one of them the by-id answer is 404, the **raw body equals the unknown id's raw body**, the **headers are equal** (ETag and content-length included, Date excluded), and the body has no `data:`, `downloadUrl` or type name. Every refused export is also **absent from that caller's list** (`?limit=1000`).
- 7 admitted cases read 200: the creator, a same-company USER, `SYSTEM_ADMIN` with no tenant, `Super_Admin` of another company, a tenant-less creator, the same creator who now carries a tenant, and an admin on an export with no owner.
- At head: 54 of 54 green. At base (the routes as of `dbb053b756ae` and no `exportAccess.ts`): 45 red, all by AssertionError (22 by id, 22 list, 1 list-after-202), 9 green. Runs are in `scratch/runs/gate_cells_{head,base}.json`.

**(2) The owner record.**
- `recordExportOwner` runs synchronously after `createExport` resolves and before `res.status(202)`. It keeps only string `tenantId`/`userId` from `req.user`.
- No owner field appears in the 202, by-id or list bodies. My leak cell checks this with marker ids.
- My mutant g16 records after the 202 (setTimeout 50 ms). It goes red in 9 cells, so "record before the 202" is pinned.
- `exportService.createExport` is called only by the route (grep at head). Exports can enter `memExports` without an owner by two paths: `loadFromDb` at boot and a direct service call. Both are admin-only (fail-closed), and cells prove it.
- One window exists and it fails closed. With the DB available, `dbSaveExport` sets the Map entry and then awaits the INSERT before the owner is recorded. During that await, only an admin can see the row. Nothing leaks.
- The owner map gains one small `{tenantId,userId}` per POST and never evicts. That is the same lifetime as `memExports`, which holds the whole `data:` file per row. It is not a leak relative to `memExports`; it is the same unbounded per-process growth, and the PR body states it.

**(3) The list.**
- A platform admin goes through `listExports(limit)` unchanged. The PR's cell compares the raw output to the service's own call. My g12 sends the admin through the filter path, and it reds that cell.
- For a non-admin, the code calls `listExports(Infinity)`, then filters, then slices. My g9 (filter after slice) reds the limit cell.
- An empty result is exactly `{"success":true,"data":[]}`.
- Pre-existing quirk, not a regression: `?limit=-1` gives `slice(0,-1)`, which drops one row on both paths.

**(4) Nothing widened, nothing inside a company removed.**
- `git diff --quiet dbb053b756ae..head` is 0 for `exportService.ts`, `analytics.openapi.ts`, `systemTest/`, `api-gateway`, `frontend`, `packages` and `database`. The control, `routes/analytics.ts`, is 1.
- My g10 narrows same-company reads to the creator: it reds 7 cells (the RULING cells). My g6 admits the org-bounded admin roles: it reds 7 cells.

**(5) The tests are honest.**
- Red first at `dbb053b756ae`, re-run by me: the by-id file has 13 red, all AssertionError, and 10 green. The list file has 7 red (AssertionError) and 4 green. The unit file fails to load (module missing), which matches the builder's account.
- Every RED-labelled cell is red and every control is green.
- **My own 16 mutants:** 15 killed, 1 survivor.

| Mutant | What it changes | Cells red |
|---|---|---|
| g1 | drops the by-id check | 13 |
| g2 | drops the list filter | 7 |
| g3 | skips the POST owner record | 14 (1 of them a TypeError, the R1-C2 key read on a 404 body) |
| g4 | tenant compare via case fold | 1 |
| g5 | tenant compare via `includes` | **0: SURVIVES** |
| g6 | admits the org-bounded roles | 7 |
| g7 | no-owner export readable by all | 4 |
| g8 | 403 for 404 | 13 |
| g9 | filters after the slice | 1 |
| g10 | same-company narrowed to the creator | 7 |
| g11 | `String(role)` fold | 3 |
| g12 | admin goes through the filter path | 1 |
| g13 | drops the non-empty guard on the tenant-less arm | 3 |
| g14 | record keeps non-string ids | 1 |
| g15 | tenant arm keyed on presence | 1 |
| g16 | records after the 202 | 9 |

- Every mutant was restored by content, and the sha256 values were checked: routes `82c346a3bcdec3ed`, exportAccess `7ee4e1f19bf76e94` (the same as the builder's).
- Whole analytics suite at head: 25 files, 211 tests, all green. The 22 pre-existing files at base: 129 green. Both match the READY.

**(6) Callers.**
- Re-searched at head (`analytics/exports` across the repo). Code callers: `frontend/issuer/.../ExportDialog.tsx:97` (list `?limit=10`), `:133` (POST), and `frontend/admin/src/services/api.ts:813` (`fetchReports`, which reads `res.data?.exports`). The rest are docs and specs.
- ExportDialog shows only the list and creation. The creator's own and same-company rows remain, and my cell shows the creator lists the new export straight after the 202. Nothing breaks.
- The admin `fetchReports` shape mismatch is pre-existing and the PR body names it.
- The body's "admits / REFUSES / does NOT change / NOT covered" sections match the code and the cells.

**(7) AC6.** The systemTest file is unchanged. The marker is correct to stay: `test_analytics_export_by_id` is `xfail(strict)` `_RULING_PENDING`, and its actors `owner`/`ownerPeer` are registered users. In auth, `userRepo.ts:685` defaults every tenant-less signup to `DEFAULT_TENANT_ID` `a0000000-0000-4000-8000-000000000001`, and `jwt.ts:201` signs `user.tenantId`. So both actors carry the same tenant, the peer still reads 200 under this PR, and the strict xfail holds. This was measured from code, not from a stack.

**Overlap, tsc, eslint, docs.**
- merge-tree (`scratch/mergetree.out`): head×develop and develop×head are rc 0; head×2188 and 2188×head are rc 0. A planted same-line edit on develop conflicts in both orders (rc 1, CONFLICT in routes/analytics.ts).
- develop `dbb053b756ae..6fdba4e013b3` touches 0 analytics, shared or lockfile paths.
- tsc with tests included (a temporary config): the only errors are the 2 pre-existing TS2835 (`db.retry.test.ts`, `ks1868-...-db-pool-...test.ts`) and 0 in the PR's files. A planted TS2322 in a ks1703 test fires. The service's own `tsc --noEmit` is rc 0.
- eslint (ESLint API, cwd `Blockchain/Dev`, the repo config) on the 5 changed code files: 0 errors and 0 warnings. A planted `no-debugger` fires.
- docs-fragments check: OK at head, with 2 ADVISORY lines that are pre-existing render lag. It is also OK on the develop+head merge probe. A planted literal section number in the flow fragment gives rc 1 and names the file. After restoring, OK again.
- Every test run was gated on load1. One batch was held at 8.47 and re-run after it dropped (5.8 to 7.8).

## Findings
- **N1, LOW (test gap):** mutant g5 (`owner.tenantId.includes(callerTenant)`) survives all 82 PR cells. No PR cell has a caller tenant that is a strict substring of the creator's. The code is correct (`===`), and my gate cell "tenant is a substring of the creator tenant" pins it at head. Suggested follow-up: one unit row. Not blocking.
- **N2, LOW (test strength):** only R1-X compares the raw 404 body. The other refusal cells compare parsed JSON. My 22-row cell closes this at head: raw body and headers are identical for every refusal class.
- **N3, NOTE for Kam (scope, not a defect):** the "company" boundary is `tenantId`, and auth puts every tenant-less signup (self-register, social, wallet) into the one DEFAULT tenant `a0000000-…-0001`. That is also the PR's own test tenant T1. So all default-tenant users stay one "company" and still read and list each other's exports. This PR separates distinct tenants only, and the PR body does not say so. In practice this falls under Kam's open card `secuura-ks1703-ac4-same-company-reads-1115`. Arm (iii), the tenant-less creator, is therefore probably rare for registered users.
- **N4, INFO:** under the fail-closed design, the PR's m3 (skip the record) cannot redden the cross-company cell. The builder declared this. Other cells kill it (g3 = 14), and g16 kills an after-the-202 record.
- **N5, INFO:** the owner map never evicts. It grows with `memExports` (one row per POST) and is far smaller, so it is not a relative leak. The PR body states it.

## NOT covered by this gate
- A stack, the gateway, a browser, the four platform suites, external clients, a live DB reload or an INSERT against a live DB, real JWTs and token types (refresh or service tokens with a tenantId), multiple processes or replicas (owner store is per-process), and the other KS-1703 routes.
- The open-PR census was not re-run; only PR 2188 was measured, as the commission named it.
- Kam's AC4 card was not re-read from the board.

## Evidence (all under scratch/)
`mergetree.out`, `runs/base_with_pr_tests.json`, `suite_head.json`, `runs/mut_g*.json`, `mutants.out`, `mutants2.out`, `cells/g367-ks1703-exports-gate.test.ts`, `runs/gate_cells_{head,base}.json`, `tsc_all.out`, `tsc_plant.out`, `docs_check.out`, `docs_plant.out`, `docs_check_merge.out`, `pr_body.md`, and the scripts `mt.sh`, `runsuite.sh`, `tobase.sh`, `mutants.py`, `eslint_g367.mjs`, `mergecheck.sh`. Restored originals and the moved temporary files are in `hold/`.
