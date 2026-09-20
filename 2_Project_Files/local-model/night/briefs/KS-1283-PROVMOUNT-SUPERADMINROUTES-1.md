# KS-1283 PROVMOUNT-SUPERADMINROUTES-1 PIN THAT A TENANT-ADMIN BEARER IS REFUSED 403 ON THE register-connector MOUNT AND ON EVERY OTHER requireSuperAdmin MOUNT OF platform.ts — the real gateway over loopback with the file's own recording upstream and a tenant ADMIN JWT it already mints — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one helper + two cells added, no product file** (written 2026-09-21 after the #1112-#1118 batch gate; its NOT-PINNED rows PROVMOUNTUNPINNED and SUPERADMINROUTESWIDEN, both KS-1283, both measured 0 red of 684 at the head)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts`
Tip: `7be81d5c9b109959b559e03652fb092c12de58e8`
Runner: `vitest`

Written from develop `7be81d5c9b109959b559e03652fb092c12de58e8` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` on 2026-09-21, read verbs only; the tree that carries the seven #1112-#1118 squashes, #1113 = KS-1283 PROVADMIN-1 included). The test file at that tip is **529 lines** (blob `502989533359`), read whole; its full content is in `files[...]` of your input. The product the cells pin is `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (blob at the tip, **990 lines**): `const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];` at **`:64`**; `requireSuperAdmin` at `:66-:73` (403 `FORBIDDEN` / `Super-admin access required` unless `SUPER_ROLES.includes(user.role)`), mounted on THIRTEEN routes (`:222` GET `/api/platform/tenants`, `:239` POST `/api/platform/tenants`, `:284` GET `/api/platform/tenants/:id`, `:301` PATCH `/api/platform/tenants/:id`, `:320` PATCH `/api/platform/tenants/:id/status`, `:339` DELETE `/api/platform/tenants/:id`, `:362` GET `/api/platform/audit-log`, `:767` POST `/api/platform/tenant-key`, `:782` DELETE `/api/platform/tenant-key/:tenantId`, `:792` GET `/api/platform/tenant-key/:tenantId/status`, `:806` GET `/api/platform/templates/document-types`, `:832` GET `/api/platform/templates/workflows`, `:859` POST `/api/platform/templates/clone-to-tenant`); `export function requireOrgProvisioner` at `:91-:114` (admits `SUPER_ROLES` as `'admin'`, a connector with `organizations:register` as `'connector'`, else 403 `FORBIDDEN`), mounted ONCE, on `router.post('/api/platform/organizations/register-connector', authenticateToken(), requireOrgProvisioner, ...)` at `:486-:489` with **`    requireOrgProvisioner,` alone on `:489`**. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest.setup.ts` provisions `__TEST_JWT_PRIVATE_PEM`; no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `routes/platform.ts`, `middleware/auth.ts`, `index.ts` or any other product file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

#1113 (KS-1283 PROVADMIN-1) added a cell in `ks480-org-provisioner-gate.test.ts` that drives the REAL `requireOrgProvisioner` function with a fake req/res and pins its else-branch for `'ADMIN'` and `'admin'`. The #1112-#1118 gate then measured two seams at the head: (1) PROVMOUNTUNPINNED — with `    requireOrgProvisioner,` removed from the `:489` mount, **684/684 green**: no cell drives the MOUNT, so a mount that loses its guard is not noticed; (2) SUPERADMINROUTESWIDEN — with `SUPER_ROLES` widened by `'ADMIN', 'admin'`, only the ks1215 `GET /api/platform/tenants` cell (`:319`) and the new guard cell red: the other TWELVE `requireSuperAdmin` mounts have no cell that reds. This file is the one that already boots the real app over loopback with a recording upstream, mints a tenant-ADMIN JWT inline (`:321`, `role: 'ADMIN'`, `sessionId: 'ks1215-live'`, which the stubbed session store answers live) and drives `PATH = '/api/platform/organizations/register-connector'` (`:381`). This change adds, at the END of the third describe (`register-connector forwards no caller Bearer upstream`, `:374-:458`), ONE helper `tenantAdminJwt()` (the `:321` mint, as a function) and TWO cells: the first POSTs a full `registerBody()` to `PATH` with the tenant-ADMIN bearer alone and asserts `[403, 'FORBIDDEN', []]` — the mount's guard refuses a tenant admin and nothing reaches `/api/tenants`, `/api/keys` or `/api/audit`; the second is table-driven over the twelve OTHER `requireSuperAdmin` mounts (the thirteenth, GET `/api/platform/tenants`, is the existing `:319` cell) with the same bearer and asserts every row is `[method + ' ' + path, 403, 'FORBIDDEN', []]`. The two rows are ONE brief because they are COUPLED through `SUPER_ROLES`: `requireOrgProvisioner` admits `SUPER_ROLES` too (`:97`), so the widening tamper reds the register-connector cell as well as the table cell and `:319` — a red set only one brief can declare exactly (the checker's T6 is set EQUALITY, not superset). **Both cells pin TODAY's refusal**: if the owners ever decide a tenant ADMIN may provision or administer the platform, the cells go red on purpose and are rewritten with that decision.

## The exact change — ONE hunk in the test file

The helper and the two cells go at the END of the `describe('KS-1215 real app, NODE_ENV=test — register-connector forwards no caller Bearer upstream', ...)` block: after `:457` (`  });`, the close of the last cell, `control, register-connector: a key alone is unchanged, ...`) and before `:458` (`});`, the close of that describe). `});` at column 0 occurs FOUR times in the file (`:349`, `:372`, `:458`, `:500`) and `  });` many times, so the hunk carries THREE leading context lines — `:455` (`    const r = await post(gateway!.url, PATH, { 'x-api-key': OK_KEY }, registerBody());`, **unique in the file**), `:456` (`    expect(JSON.stringify([r.status, registerBearers(r)])).toBe(JSON.stringify([201, allThree('connector-jwt')]));`, which also occurs at `:395`, hence the line above it) and `:457` (`  });`) — and ONE trailing context line (`:458`). Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts`.**

```
@@ -455,4 +455,30 @@
     const r = await post(gateway!.url, PATH, { 'x-api-key': OK_KEY }, registerBody());
     expect(JSON.stringify([r.status, registerBearers(r)])).toBe(JSON.stringify([201, allThree('connector-jwt')]));
   });
+  function tenantAdminJwt(): string {
+    return 'Bearer ' + jwt.sign({ userId: 'u-ks1283-admin', email: 'ks1283-admin@secuura.io', role: 'ADMIN', verificationLevel: 'email', authMethod: 'email', tenantId: TENANT, sessionId: 'ks1215-live' }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
+  }
+  it('RED KS-1283: POST /api/platform/organizations/register-connector with a tenant ADMIN bearer answers 403 FORBIDDEN and forwards nothing', async () => {
+    const r = await post(gateway!.url, PATH, { authorization: tenantAdminJwt() }, registerBody());
+    expect([r.status, r.code, r.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED KS-1283: a tenant ADMIN JWT is refused 403 on every requireSuperAdmin mount and nothing is forwarded', async () => {
+    vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://ks1283:ks1283@127.0.0.1:1/ks1283');
+    const pairs: Array<[string, string]> = [
+      ['POST', '/api/platform/tenants'], ['GET', '/api/platform/tenants/ks1283-t1'], ['PATCH', '/api/platform/tenants/ks1283-t1'],
+      ['PATCH', '/api/platform/tenants/ks1283-t1/status'], ['DELETE', '/api/platform/tenants/ks1283-t1'], ['GET', '/api/platform/audit-log'],
+      ['POST', '/api/platform/tenant-key'], ['DELETE', '/api/platform/tenant-key/ks1283-t1'], ['GET', '/api/platform/tenant-key/ks1283-t1/status'],
+      ['GET', '/api/platform/templates/document-types'], ['GET', '/api/platform/templates/workflows'], ['POST', '/api/platform/templates/clone-to-tenant'],
+    ];
+    const outcomes: unknown[] = [];
+    for (const [method, path] of pairs) {
+      const n = hits.length;
+      const body = method === 'GET' || method === 'DELETE' ? undefined : JSON.stringify({ name: 'ks1283' });
+      const r = await fetch(gateway!.url + path, { method, headers: body ? { 'content-type': 'application/json', authorization: tenantAdminJwt() } : { authorization: tenantAdminJwt() }, body });
+      const code = ((await r.json().catch(() => ({}))) as any)?.error?.code ?? null;
+      await new Promise((w) => setTimeout(w, 50));
+      outcomes.push([method + ' ' + path, r.status, code, hits.slice(n).map((h) => h.url)]);
+    }
+    expect(outcomes).toEqual(pairs.map(([method, path]) => [method + ' ' + path, 403, 'FORBIDDEN', []]));
+  });
 });
```

`describe`, `it`, `expect` and `vi` are imported by the file at `:45`, `jwt` at `:47`; `PRIV` (`:75`), `TENANT` (`:76`), `hits` (`:83`), `post` (`:148-:167`, `[status, code, hits since the mark]` after a 250 ms settle), `registerBody()` (`:169-:172`) and the describe's own `gateway` (`:375`) and `PATH` (`:381`) are the file's — you add NO import and NO file-scope constant; `tenantAdminJwt` is a function declared INSIDE the describe callback, above the two cells that call it. The table cell drives PATCH and DELETE with `fetch` exactly as the file's `:296`, `:310`, `:338`, `:421` cells do (`hits.length` mark, `error.code` read, a 50 ms settle). The `vi.stubEnv('PLATFORM_DATABASE_URL', ...)` line copies `:432`/`:438`: the two templates handlers and clone-to-tenant open a `pg.Pool` on that URL when the guard ADMITS the caller (`platform.ts:810`, `:836`, `:874`), and an UNSET URL would make `pg` try `localhost:5432` — the stub points them at a closed loopback port instead, so under the widening tamper they answer 500 without leaving 127.0.0.1. **The new cells do NOT call `RAN.add`** on purpose: the file's `COMPLETENESS` cell (`:502-:528`) asserts the `RAN` set EQUALS a literal list, so registering would need a second hunk 60 lines away; the two cells are graded by their titles. The cells need no port of their own (`bootApp` listens on `127.0.0.1:0`, `:93`/`:219`), no database (`../db` is mocked at `:51-:61`) and no real upstream (the recorder at `:181-:207` answers every route; every `*_SERVICE_URL` and `TENANT_PROVISIONING_URL` point at it, `:213-:214`).

## Cells

- `provmount` = `RED KS-1283: POST /api/platform/organizations/register-connector with a tenant ADMIN bearer answers 403 FORBIDDEN and forwards nothing`
- `superroutes` = `RED KS-1283: a tenant ADMIN JWT is refused 403 on every requireSuperAdmin mount and nothing is forwarded`
- `tenantsadmin` = `RED: a tenant ADMIN JWT is refused 403 on GET /api/platform/tenants and nothing is forwarded`

## Red cells

The two cells below are GENUINE assertion-reds: each fails under the tamper(s) declared for it and passes at the tip. They are declared here rather than with a red glyph in their titles because every `+` line in this diff must be ASCII only.

- RED KS-1283: POST /api/platform/organizations/register-connector with a tenant ADMIN bearer answers 403 FORBIDDEN and forwards nothing
- RED KS-1283: a tenant ADMIN JWT is refused 403 on every requireSuperAdmin mount and nothing is forwarded

## Tampers

Two single-line tampers on `routes/platform.ts`, each the gate's own row byte for byte in its `From`. Each `From` is the tip's line at that number and occurs EXACTLY ONCE in the file (python whole-line scan: `    requireOrgProvisioner,` hits `[489]`; `const SUPER_ROLES = [...]` hits `[64]`; positive control `    requireSuperAdmin,`: 13 hits). Each `To` is valid TypeScript (measured: the file loads and the whole suite runs under each). The checker plants each and restores the file by bytes.

### PROVMOUNTUNGUARDED — the register-connector mount loses requireOrgProvisioner (the guard line becomes a comment)
File: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`
Line: 489
From:
```
    requireOrgProvisioner,
```
To:
```
    // requireOrgProvisioner, -- PROVMOUNTUNPINNED: the mount runs with no provisioner guard
```
Reds: `provmount`

### WIDENROLES — SUPER_ROLES admits the tenant-admin spellings
File: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`
Line: 64
From:
```
const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];
```
To:
```
const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN', 'ADMIN', 'admin'];
```
Reds: `tenantsadmin`, `provmount`, `superroutes`

## Controls

- `control, register-connector: a JWT-only platform admin still succeeds, and all three upstream calls carry the admin's own Bearer`
- `RED: a connector key is refused 403 on GET /api/platform/tenants and nothing is forwarded`
- `RED KS-1238 (iii): a connector key carrying organizations:register is refused 403 on POST /api/platform/tenants, and neither tenant-provisioning nor refresh-tenants is called`

*(All three are FULL `it(...)` titles copied from the file at the tip — `:447`, `:325`, `:403` — unchanged by this hunk (the insertion is below all of them). For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another. Under PROVMOUNTUNGUARDED the SYSTEM_ADMIN control still provisions (the guard it lost admitted it anyway) and the connector controls never reach the platform mounts' guards' admit branches; under WIDENROLES a CONNECTOR key is still no super role, so the two connector controls stay 403 and the SYSTEM_ADMIN control is unchanged — the controls prove the gateway, the session check and the recorder still run under each tamper. The file's other existing cells are also green under both tampers but are left undeclared, EXCEPT `:319`, which is a declared red under WIDENROLES — see Tampers.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip both new cells pass. `provmount`: `post` sends `registerBody()` to `PATH` with `authorization: Bearer <ADMIN JWT>` and no key; `authenticateToken()` verifies the RS256 JWT with the test public key, asks the stubbed session store about `ks1215-live` (live) and sets `req.user` with `role: 'ADMIN'`; `requireOrgProvisioner` finds `'ADMIN'` in neither `SUPER_ROLES` nor the connector branch and answers 403 `FORBIDDEN` before the handler runs, so nothing reaches `/api/tenants`, `/api/keys` or `/api/audit`: `[403, 'FORBIDDEN', []]` (measured). `superroutes`: each of the twelve requests passes `authenticateToken()` the same way and meets `requireSuperAdmin`, which answers 403 `FORBIDDEN` and forwards nothing: twelve rows of `[method + ' ' + path, 403, 'FORBIDDEN', []]` (measured).

Under **PROVMOUNTUNGUARDED** the mount is `authenticateToken(), <comment>, handler`: the ADMIN caller reaches the handler, which (as the `:447` SYSTEM_ADMIN control shows for a real super admin) looks the tenant up at `/api/tenants`, mints a key at `/api/keys` and writes `/api/audit` — the cell receives `[201, null, ['/api/tenants', '/api/keys', '/api/audit']]` (measured; the order of the three is the recorder's arrival order), an assertion red; `superroutes` is untouched (the twelve mounts keep `requireSuperAdmin`). Under **WIDENROLES** `'ADMIN'` is a super role: `requireOrgProvisioner` admits the caller as `'admin'` and `provmount` reds the same way; every one of the twelve mounts admits the caller and its handler answers whatever it answers with the upstream recorder and the closed-port `PLATFORM_DATABASE_URL` — none of the twelve is `[403, 'FORBIDDEN', []]` (measured, per-row outcomes in the MEASURED section), an assertion red on `superroutes`; and the file's existing `:319` cell (`tenantsadmin`) reds as the gate measured. Every other existing cell stays green under each tamper (measured: whole suite under each).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From lines.** `platform.ts` at `7be81d5c9`, line 489 is `    requireOrgProvisioner,` (4-space indent) and line 64 is `const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];` (column 0), byte for byte; each occurs **once** as a whole line. The checker plants and restores each (T8 by sha256 after).
- **Premise: the gate's claims, re-derived.** PROVMOUNTUNPINNED: `git grep -n 'register-connector' -- 'Blockchain/Dev/services/api-gateway/src/__tests__'` at the tip finds this file and `ks480-org-provisioner-gate.test.ts` — this file drives the mount only with a key, a key + user JWT, or a SYSTEM_ADMIN JWT (all admitted); ks480 drives the FUNCTION. No cell sends a tenant ADMIN to the mount: agreed. SUPERADMINROUTESWIDEN: the only tenant-ADMIN drive of any platform mount is `:319` (GET `/api/platform/tenants`); every other platform cell in this file uses a connector key: agreed.
- **Premise: the anchor.** The test file is **529** lines; `:455`-`:458` are non-blank, `:455` is unique, `:458` is the third describe's `});`. The hunk is a pure insertion with three leading and one trailing context line — no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** Two, unavoidable for new cells and added by this brief (so T4 accepts them): `  });` and `    }`. No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick — `method + ' ' + path` is string concatenation). Titles use `:` and `/`, no em dash.
- **Premise: the runner.** `services/api-gateway/package.json` at the tip has `"test": "vitest"`, no jest — the builder auto-detects vitest and the `Runner:` line agrees.
- **Premise: the surface.** The real gateway over loopback (`127.0.0.1:0`), `../db` mocked, the session store stubbed, every upstream the file's recorder; the pg URL for the templates handlers stubbed to a closed loopback port. No user store, no real session, no real key beyond the harness's test pair, no port of its own, nothing on :5432. GATEWAY platform-admin authorisation surface, test-only pin (allowed under Kam's scope rule; no product edit).

## Collision

**No held READY names this test file** (`/usr/bin/grep -il 'ks1215-the-connector-branch-never-carries-the-callers-bearer' night/READY_*.md`: counted in the MEASURED section, with the positive control) and no other brief of this round touches it (the other two of this round are `auth.test.ts` and the originate `ks978` file). Tamper file `routes/platform.ts` is planted by no held READY. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `7be81d5c9`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/PROVMOUNT-SUPERADMINROUTES/`)

- (filled in below after the measurement and golden runs)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts`, then the hunk above exactly as shown (`@@ -455,4 +455,30 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (gateway platform-admin authorisation, loopback with the file's recorder — allowed). Refs KS-1283** (and KS-1282 / KS-1215 for the cells' neighbours). **NEVER Closes** — KS-1283 is merged; these cells pin its mount and the twelve sibling mounts.
- **From the #1112-#1118 batch gate's NOT-PINNED table** (report `2026-09-21-batch1112-1118-tier1-r1/report.md`, rows PROVMOUNTUNPINNED and SUPERADMINROUTESWIDEN), written as ONE brief because the WIDENROLES tamper reds the register-connector cell too (`requireOrgProvisioner` reads `SUPER_ROLES`) — two briefs could each pass the checker alone but neither could declare WIDENROLES' true red set once both land.
- **Said plainly:** the new cells are not registered in the file's `RAN`/`COMPLETENESS` list (one hunk); the twelve rows send `{ name: 'ks1283' }` as the body of the three POST/PATCH-with-body routes, which under the widening reach their handlers' own 400s or the recorder — the assertion is only that NONE is the guard's 403.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1283 night/inputs/test_only_1283PROVMOUNT-SUPERADMINROUTES-1.json night/briefs/KS-1283-PROVMOUNT-SUPERADMINROUTES-1.md tip=7be81d5c9b109959b559e03652fb092c12de58e8 ctx=65536
```
