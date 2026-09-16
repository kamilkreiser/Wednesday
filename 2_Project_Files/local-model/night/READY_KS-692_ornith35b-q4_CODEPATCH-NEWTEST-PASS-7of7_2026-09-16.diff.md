# READY — KS-692 (Security: `/api/status` revoke/unrevoke has no tenant ownership check — an ISSUER_ADMIN in ANY tenant could revoke ANY tenant's credential) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on its FIRST sample, CODE_PATCH (vitest), NEW test file, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks692-ornith35b-night
# ⚠ THE FIRST VERDICT ON THIS RUN WAS "FAIL — stopped at A4" AND IT WAS WEDNESDAY'S BRIEF, NOT THE MODEL. Retracted in done.md. The A4 gate counts a failing cell as a *declared red* only when its title carries 🔴 or when the brief names it under `## Red cells` (parsed into `defect_line.red_cells`). This brief's cells are titled `RED 1/2/3` with no glyph and the brief had no `## Red cells` section, so all three genuine assertion-reds were classified as CONTROL reds and a correct output failed. Section added to the brief, input rebuilt, the SAME `out.md` re-checked → PASS 7/7. No second model round was spent. Builder gate + arms: see `IMPROVEMENTS.md`.
# Source read by me (Wednesday), the applied artefacts, not the verdict: the product hunk is 4 `-` / 22 `+` in ONE hunk on `routes/status.ts` and does exactly one operative thing — drops `'ISSUER_ADMIN'` from `STATUS_WRITE_ROLES`; every other `+` line is comment. The test section is a NEW 6-cell file; at the untouched tip RED 1/2/3 fail by ASSERTION (not by throw) and GREEN CONTROL 4, GREEN CONTROL 5 and COMPLETENESS pass — so the harness demonstrably reaches the code before the fix as well as after. After the product hunk: 6/6 green, whole vc-issuer suite 113/113 (baseline 108/108, +5 tests, zero NEW reds), `tsc --noEmit` rc 0 against a green baseline.
# KAM'S RULING IS IN THE ARTEFACT, not only in a mail: the comment block quotes `secuura-ks692-status-revoke-interim-posture: a` — "Narrow now, bind-creator later" — verbatim, states plainly that this is INTERIM, and names `secuura-ks1116-presentation-credential-ownership-model` / `bind-creator` (Kam 2026-09-13) as what eventually replaces it. That is the whole point of the 2026-09-05 delivery rule and the model did it without being told twice.
# TWO TICKET-STATE CLAIMS THE MODEL WROTE INTO THE SOURCE, BOTH VERIFIED BY ME AT SOURCE (Linear read-only, 2026-09-16): KS-586 is **Done / completed** — so the tip's comment pointing a reviewer at KS-586 was indeed a stale pointer and removing it is correct; KS-1116 is **Backlog** — so "when the owner column lands" is an open future, not a finished one. Neither was taken on trust.
# PR NOTES for the Sunday raising seat:
#  (1) TWO files: `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (one hunk) + the NEW suite `Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts`.
#  (2) **This is a DELIBERATE, RULED narrowing with a user-visible cost, and the PR body must say so:** tenant-scoped admins (ISSUER_ADMIN) LOSE the ability to revoke/un-revoke until `credential_status_lists` carries an owner column. Kam chose that over leaving a cross-tenant write open. Anyone reading the diff cold will otherwise file it as a regression.
#  (3) The apply needs `--recount --ignore-whitespace` — the hunk header declares `new=34` where the actual is `new=31`. That is the model's known header-miscount dialect, not a content defect; the reanchored apply is byte-identical to the intended edit and the strict-mode rc 128 is the dialect, nothing else.
#  (4) Not in this diff and worth its own ticket: the `STATUS_WRITE_ROLES` gate is still role-class only. The per-list ownership comparison (`decideTenantAccess`) that brings ISSUER_ADMIN back is KS-1116 work.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
@@ -31,13 +31,34 @@ const router = Router();
 // route definitions — rather than per-endpoint, so a future POST added to this
 // file is covered by default instead of shipping open.
 //
-// Tenant scoping is NOT enforced here yet: status lists live in a
-// process-local Map with no tenant linkage, and the ownership model is the
-// KS-539/KS-547/KS-586 joint authorization decision — tracked on KS-586.
+// KS-692 (Kam 2026-09-16, `secuura-ks692-status-revoke-interim-posture: a`,
+// "Narrow now, bind-creator later"): tenant scoping still cannot be enforced
+// here - status lists live in a process-local Map and `credential_status_lists`
+// has no owner column, so there is no target tenant to compare a caller
+// against. An admin-class gate that included ISSUER_ADMIN therefore let an
+// ISSUER_ADMIN in ANY tenant revoke or un-revoke ANY tenant's credential
+// (reproduced live). Until a list carries an owner, "platform operator" is the
+// only authorisation that is TRUE of this surface - the same call KS-743 made
+// for the tenant-less security-event routes. So the gate narrows to the
+// platform roles: the hole closes now, at the cost of tenant admins not
+// writing status until the owner column lands.
+//
+// THIS IS INTERIM, NOT THE ANSWER. The ownership model is already ruled -
+// `secuura-ks1116-presentation-credential-ownership-model`, choice
+// `bind-creator` (Kam 2026-09-13): the owner is the authenticated principal
+// that created the resource, and pre-existing NULL-owner rows stay readable by
+// the tenant OWNER role alone. When `credential_status_lists` gains that owner
+// column, this gate reverts to an admin-class role PLUS a per-list ownership
+// comparison via `decideTenantAccess`, and ISSUER_ADMIN comes back. Tracked on
+// KS-692 - NOT on KS-586, which is Done and archived, and whose stale pointer
+// here sent a reviewer back to a defect that no longer existed.
 // 'SUPER_ADMIN'/'super_admin' are the legacy JWT variants the existing admin
 // gates already accept — the seeded platform admin carries 'super_admin'
 // (see services/auth/src/routes/users.ts:90 and issuerCerts.ts ADMIN_ROLES).
-export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin', 'ISSUER_ADMIN'] as const;
+export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'] as const;
 
 router.use((req: Request, res: Response, next: NextFunction) => {
   // Reads stay authenticated-only (status lists are verification data);
```

<!-- test section: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks692-ornith35b-night/out.md.checker/section_2.diff -->

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts
@@ -0,0 +1,105 @@
+/**
+ * KS-692 — /api/status WRITES are PLATFORM-ONLY (interim posture).
+ *
+ * Kam ruled `secuura-ks692-status-revoke-interim-posture: a` (2026-09-16),
+ * "narrow now, bind-creator later". A status list has no owning tenant to
+ * compare against, so platform-operator is the only authorisation TRUE of this
+ * surface today; ISSUER_ADMIN is off the write gate until a list has an owner.
+ */
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import express, { NextFunction, Request, Response } from 'express';
+import type { Server } from 'http';
+import { statusRoutes, STATUS_WRITE_ROLES } from '../routes/status';
+import { errorHandler } from '../middleware/errorHandler';
+
+const EXPECTED_CELLS = 5;
+let CELLS_RUN = 0;
+const PLATFORM_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'];
+const TENANT_SCOPED_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'ADMIN', 'OWNER'];
+let server: Server;
+let baseUrl = '';
+
+function buildApp(): express.Express {
+  const app = express();
+  app.use(express.json());
+  app.use((req: Request, _res: Response, next: NextFunction) => {
+    const role = req.header('x-test-role');
+    if (role) {
+      (req as Request & { user: unknown }).user = { userId: 'u-1', role, organizationId: 'org-1' };
+    }
+    next();
+  });
+  app.use('/api/status', statusRoutes);
+  app.use(errorHandler);
+  return app;
+}
+
+function writeRoutes(): string[] {
+  const stack = (statusRoutes as unknown as {
+    stack: Array<{ route?: { path: string; methods: Record<string, boolean> } }>
+  }).stack;
+  return stack
+    .filter((l) => l.route)
+    .filter((l) => Object.keys(l.route!.methods).some((m) => m !== 'get' && m !== 'head'))
+    .map((l) => l.route!.path);
+}
+
+async function probe(role: string | undefined): Promise<number> {
+  const headers: Record<string, string> = { 'content-type': 'application/json' };
+  if (role) headers['x-test-role'] = role;
+  const res = await fetch(`${baseUrl}/api/status/default/revoke`, {
+    method: 'POST',
+    headers,
+    body: '{}',
+  });
+  return res.status;
+}
+
+beforeAll(async () => {
+  const app = buildApp();
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  if (address === null || typeof address === 'string') throw new Error('no ephemeral port');
+  baseUrl = `http://127.0.0.1:${address.port}`;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+describe('KS-692 — status writes are platform-only (interim)', () => {
+  it('RED 1: ISSUER_ADMIN is not on the status write gate', () => {
+    CELLS_RUN += 1;
+    expect([...STATUS_WRITE_ROLES]).not.toContain('ISSUER_ADMIN');
+  });
+  it('RED 2: every role on the write gate is a platform role', () => {
+    CELLS_RUN += 1;
+    const tenantScoped = [...STATUS_WRITE_ROLES].filter((r) => !PLATFORM_ROLES.includes(r));
+    expect(tenantScoped).toEqual([]);
+  });
+  it('RED 3: every tenant-scoped admin is refused 403 on POST revoke', async () => {
+    CELLS_RUN += 1;
+    const seen: number[] = [];
+    for (const role of TENANT_SCOPED_ROLES) seen.push(await probe(role));
+    expect(seen).toEqual(TENANT_SCOPED_ROLES.map(() => 403));
+  });
+  it('GREEN CONTROL 4: every platform role still passes the gate', async () => {
+    CELLS_RUN += 1;
+    const blocked: string[] = [];
+    for (const role of PLATFORM_ROLES) {
+      const status = await probe(role);
+      if (status === 401 || status === 403) blocked.push(`${role}:${status}`);
+    }
+    expect(blocked).toEqual([]);
+  });
+  it('GREEN CONTROL 5: the write routes stay mounted and still 401 anonymous', async () => {
+    CELLS_RUN += 1;
+    expect(writeRoutes().length).toBeGreaterThanOrEqual(4);
+    expect(await probe(undefined)).toBe(401);
+  });
+  it('COMPLETENESS: every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
