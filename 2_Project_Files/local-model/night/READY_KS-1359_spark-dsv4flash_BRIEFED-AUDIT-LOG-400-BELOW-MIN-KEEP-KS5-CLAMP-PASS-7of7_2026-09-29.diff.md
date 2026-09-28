# READY — KS-1359 AUDIT-LOG-400-BELOW-MIN-KEEP-KS5-CLAMP (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1359-R1/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1359/KS-1359.golden.diff` (`cmp` rc 0; a control against a different ticket's golden rc 1), measured by Wednesday.

**Held BY HAND at 09:31 2026-09-29 by Wednesday morning seat 407373b1** (hold_ready.py's owed defect). Source develop **0de108577e61** (the round's source clone has a GitHub origin).

- **What:** api-gateway routes/platform.ts GET /api/platform/audit-log: 400 VALIDATION_ERROR on wrong-type or below-minimum limit/offset; the KS-5 upward clamp unchanged byte for byte.
- **Authority:** Kam ruled card `secuura-ks1359-platform-audit-log-bounds` = (a) on the live board 2026-09-29 09:05 AEST.
- **Brief + golden + README:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1359/` (the README states the red/green and suite counts and what the brief-writer could not measure; the raise seat reads it and carries its NOT COVERED into the PR body).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/platform.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts }`
  - `PASS A3c every '+' line the brief adds is in the product hunk (6 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts fails at the untouched tip (4 failed / 7 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts passes with the product hunk (7 passed / 7 run)`
  - `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=2 +89/-0 test=src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts red_first=yes apply_mode=strict`
  - `RESULT: PASS (7/7)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
@@ -360,5 +360,11 @@
     '/api/platform/audit-log',
     authenticateToken(),
     requireSuperAdmin,
     async (req: Request, res: Response) => {
+      // KS-1359: a present limit/offset must be a whole number (limit from 1, offset from 0), else 400. The KS-5 clamp below is unchanged.
+      const badInt = (v: unknown, min: number) => v !== undefined && (typeof v !== 'string' || !/^[0-9]+$/.test(v) || parseInt(v, 10) < min);
+      if (badInt(req.query.limit, 1) || badInt(req.query.offset, 0)) {
+        res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'limit must be an integer from 1 and offset an integer from 0' } });
+        return;
+      }
       // BACKLOG H1: the platform audit page used to read only from
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts
@@ -0,0 +1,83 @@
+/**
+ * KS-1359 - GET /api/platform/audit-log refuses a wrong-type or below-minimum
+ * limit/offset with 400, and keeps the KS-5 upward clamp (limit 500, offset
+ * PLATFORM_AUDIT_MAX_OFFSET) exactly as it was. Drives the REAL
+ * createPlatformRoutes on 127.0.0.1 with a fake query; the tenant-provisioning
+ * URL is a closed port, so that leg fails fast and the route degrades as it
+ * does in production. The overfetch (limit + offset) is read from the fake
+ * query's LIMIT parameter.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express, { type RequestHandler } from 'express';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import { createPlatformRoutes } from '../routes/platform';
+
+const limits: unknown[] = [];
+let base = '';
+let server: http.Server;
+
+beforeAll(async () => {
+  vi.stubEnv('PLATFORM_AUDIT_MAX_OFFSET', '5000');
+  const superAdmin = (() => ((req, _res, next) => {
+    (req as unknown as { user: object }).user = { userId: 'u-ks1359', email: 'a@b.c', role: 'super_admin', verificationLevel: 'none' };
+    next();
+  }) as RequestHandler) as (required?: boolean) => RequestHandler;
+  const app = express();
+  app.use(createPlatformRoutes({
+    authenticateToken: superAdmin,
+    tenantProvisioningUrl: 'http://127.0.0.1:1',
+    setTenantKey: () => {},
+    getTenantKey: () => undefined,
+    removeTenantKey: () => {},
+    query: async (_sql: string, params?: unknown[]) => {
+      if (params && params.length === 1) limits.push(params[0]);
+      return { rows: [] };
+    },
+  }));
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server?.close(() => resolve()));
+  vi.unstubAllEnvs();
+});
+
+async function auditLog(qs: string): Promise<[number, string | null, unknown]> {
+  limits.length = 0;
+  const r = await fetch(base + '/api/platform/audit-log' + qs);
+  const body = (await r.json()) as { error?: { code?: string } };
+  return [r.status, body.error?.code ?? null, limits[0] ?? null];
+}
+
+describe('KS-1359 audit-log limit/offset', () => {
+  it('RED KS-1359 B1: offset -1 is refused 400', async () => {
+    expect(await auditLog('?offset=-1')).toEqual([400, 'VALIDATION_ERROR', null]);
+  });
+
+  it('RED KS-1359 B2: a non-numeric limit is refused 400', async () => {
+    expect(await auditLog('?limit=abc')).toEqual([400, 'VALIDATION_ERROR', null]);
+  });
+
+  it('RED KS-1359 B3: limit 0 is refused 400', async () => {
+    expect(await auditLog('?limit=0')).toEqual([400, 'VALIDATION_ERROR', null]);
+  });
+
+  it('RED KS-1359 B4: a fractional offset is refused 400', async () => {
+    expect(await auditLog('?offset=1.5')).toEqual([400, 'VALIDATION_ERROR', null]);
+  });
+
+  it('control KS-1359: no query keeps the defaults, 200 and overfetch 50', async () => {
+    expect(await auditLog('')).toEqual([200, null, 50]);
+  });
+
+  it('control KS-1359: limit 10 offset 0 is admitted, 200 and overfetch 10', async () => {
+    expect(await auditLog('?limit=10&offset=0')).toEqual([200, null, 10]);
+  });
+
+  it('control KS-1359: above the maximum still clamps (KS-5), 200 and overfetch 500 + 5000', async () => {
+    expect(await auditLog('?limit=900&offset=999999')).toEqual([200, null, 5500]);
+  });
+});
```
