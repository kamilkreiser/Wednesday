# Opus QA gate — PR #1460 (KS-1334 part C, fifth site)

**Head:** `dcb025b0f38b948f7271503b5ae6ac3fff616125` (one commit, parent `65d7722f83a61b7a18cf9dc0b4aeccd4fe1af6b9`, author kksecura)
**Verdict: GO WITH NOTE** (0 Major, 0 blocking Minor; 2 notes)
**Gate date:** 2026-10-12. Read-only: no pushes, merges, comments or board writes.

## Where the head came from
- `git ls-remote origin` (read): `refs/pull/1460/head` = `refs/heads/feature/ks-1334-migrate-tenant-data-200-body-error-code-j2-1` = `dcb025b0f…`. Develop tip on origin = `f5a24026…`.
- The head was not in the shared repo or under `Blockchain/worktrees` (only `s-b32-ks1334a`, `s-b33-ks1334b`). I found it in the seat's scratchpad clone `/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/09804d4e-…/scratchpad/clone` (its HEAD = dcb025b0). I made my own copy with `git clone --no-hardlinks` into my scratchpad `g1460`, checked out the SHA, and symlinked the seat clone's node_modules (I only read them).

## (1) Diff
`git diff --stat 65d7722..dcb025b`: 2 files, **+77 / -1**, and there is 1 commit between them. It matches the claim:
- `services/originate/src/routes/adminConfig.ts` +7/-1: in the per-tenant catch (`:2159-2167` on head), `results.push({tenant, error: err.message?.substring(0,60)})` becomes `logger.error('Admin config tenant step failed (POST /api/admin/migrate-tenant-data)', {tenant: tenant.slug, error: err instanceof Error ? err.message : String(err)})` followed by `results.push({tenant, error: 'TENANT_COPY_FAILED'})`.
- `src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` +70: 4 cells (C1, C2 RED; C0, C3 controls). The change touches nothing else.

## (2) RED and controls (my runs)
| Cell | base route + head test | head |
|---|---|---|
| C1 (stable code, no leak, all NODE_ENVs) | FAIL (leaked: true) | pass |
| C2 (logged once with route and tenant) | FAIL (calls = []) | pass |
| C0 control (clean tenant: no error field, no log) | pass | pass |
| C3 control (60-char prefix is inside the leak) | pass | pass |
File totals: base 2 failed / 25 passed / 27; head 27/27. This matches the seat's `ks1334c_red_before_fix.log`.

Planted reds on head, each changing one thing, each run against the 27-cell file:
- P1: put `err.message.substring(0,60)` back in the body. Only C1 fails.
- P2: change the code to `TENANT_FAILED`. Only C1 fails.
- P3: remove the logger call. Only C2 fails. Control for the zero-count grep: the head file has 1 hit at :2162.
- P4: rename the tenant key in the log payload. Only C2 fails.
- P5: add an error field on the success path. Only C0 fails.
I restored the file afterwards, and `git diff --quiet HEAD` confirms it matches head.

## (3) Suites on head
- ks730c file: 27/27.
- Full originate unit suite: **97/97 suites, 1103/1103 tests**, rc 0. No load timeouts, so nothing needed a file-by-file re-run.
- `tsc --noEmit`: rc 0. Control: a type error I planted in adminConfig.ts gave TS2339, so tsc does check this file.
- eslint on the 2 touched files: 0 errors and 2 warnings (prefer-const `copied` :2097, unused `e` :2137). Base has the same 2 warnings on lines this PR leaves alone.

## (4) Semantics
- **Leak paths in the handler (`:2044-2174`).** The 400 path sends static text. The outer catch goes to `fail500` (made safe in part B). The column-fix, docType and org loops have inner catches that swallow everything and push nothing. The only `results.push` sites are `:2158` (counts) and `:2166` (code), and the only `res.json` is `{success, results}`. Grepping the handler for `err.message` finds only the logger line. **The 200 body has no path left that leaks thrown text.**
- **Logger.** The only thing that can throw into this catch is `mgr.getPool()` (`packages/shared/src/db/tenant-pool-manager.ts:222`: "Tenant <id> is <status> — access denied"). Inner `pg` errors are swallowed. The log line gets tenant slug, route and message, with no credentials or connection string. It tells an operator which tenant failed, on which route, and why.
- **Consumers of the old `error` text.** `git grep -i 'migrate-tenant'` across the whole repo (frontend, mobile, docs, openapi, other services, scripts) finds only the route's own 3 lines, which also serve as the grep's positive control. A grep of the Extranet repo finds 0. Nothing parses the old text.
- **Code collision.** `TENANT_COPY_FAILED` appears only in the route and the test. It does not collide with any existing code.

## (5) Consistency with the four merged KS-1334 sites
Part A (#1294: refresh-tenants, backfill-certification-metadata) and part B (#1300: seed-demo-users, outer migrate-tenant-data) all route through `fail500`: the server log gets `logger.error(context, {error})` and the body gets a stable code. This site follows the same pattern for a 200 per-item entry: a context string naming the route, the message in the log, and a stable code in the body.

## Notes (non-blocking)
- N1 (Minor, `adminConfig.ts:2164`): for a non-Error throw the log uses `String(err)`, which turns an object into `[object Object]`. `fail500` (`:104`) logs the class name and field names in that case. It leaks nothing, but the log is less useful than the other four sites' logs. Only `getPool` can throw here and it throws Error, so in practice this never comes up.
- N2 (Minor, shape, `:2166`): the per-item `error` is a bare string code. The route's other errors use `{code, message}` objects. The field was already a string, so keeping it a string breaks no consumer, and I found none.

## Not checked
- Whether it merges cleanly onto develop tip `f5a24026`: that object is in no local clone and I did not fetch with Secuura credentials. GitHub does show a `refs/pull/1460/merge` (`12c5bf21`).
- I did not exercise the route against a live database.
