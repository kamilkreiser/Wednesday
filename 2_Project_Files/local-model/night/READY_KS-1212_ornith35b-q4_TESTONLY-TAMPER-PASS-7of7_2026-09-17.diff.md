# READY — KS-1212 (NEW api-gateway test: the erasure door reads its OWN router's caseSensitive option — R1/R2 router pair + CONTROL exactly two Router() calls; tamper = #1019r2 gate G-READOUTER at routes/proxy.ts:808) — Ornith ornith:35b q4, first sample, PASS 7/7 at 18:31 2026-09-17 on tip 81ee4b729 (READY written 18:32)
# Source read by Wednesday: the model's 134 `+` lines IDENTICAL to the brief's test fence (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A4: BOTH declared reds R1 + R2 in failed_names (2 failed / 4 run); A6 524 -> 528, NEW reds [].
# PR NOTES: `Refs KS-1212`, NEVER Closes. TIER 2. RENAME the test file at raise (e.g. ks1212-erasure-door-reads-its-own-router-case-option.test.ts). Brief night/briefs/KS-1212.md; report night/briefs/KS-1212_BRIEF_2026-09-17.REPORT.md.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1212-ks1187-tests-no-cell-pins-that.test.ts
@@ -0,0 +1,134 @@
+/**
+ * KS-1212: the gdpr erasure door compares the canonical path with the case
+ * rule of its OWN router, erasureDoor. The merged F-1019-2 cell makes every
+ * Router the factory builds case sensitive at once, so it cannot tell the door
+ * router from the factory router, and a read of the factory router option
+ * stays green. These cells build the REAL createProxyRoutes twice through a
+ * Router seam that makes exactly one of its two routers case sensitive: first
+ * the door router, then the factory router. The door must follow its own.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+import type { AddressInfo } from 'node:net';
+import type { NextFunction, Request, RequestHandler, Response } from 'express';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const seen: string[] = [];
+const servers: http.Server[] = [];
+const builtPerApp: boolean[][] = [];
+let built: boolean[] = [];
+let routerCalls = 0;
+let sensitiveCall = 0;
+let doorUrl = '';
+let factoryUrl = '';
+
+async function listen(server: http.Server): Promise<string> {
+  servers.push(server);
+  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
+  return 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+}
+
+// build the REAL factory with Router call number which case sensitive
+async function buildApp(which: number): Promise<string> {
+  const { createProxyRoutes } = await import('../routes/proxy');
+  const { services } = await import('../config/services');
+  sensitiveCall = which;
+  routerCalls = 0;
+  built = [];
+  const authenticateToken = (): RequestHandler => (req: Request, _res: Response, next: NextFunction) => {
+    (req as any).user = { userId: 'c-ks1212', email: 'connector@secuura.io', role: 'connector', authMethod: 'api_key', scopes: ['documents:read'], tenantId: 't-ks1212' };
+    req.headers['x-user-id'] = 'c-ks1212';
+    req.headers['x-user-email'] = 'connector@secuura.io';
+    req.headers['x-user-role'] = 'connector';
+    next();
+  };
+  const app = express();
+  app.use(createProxyRoutes({ services, authenticateToken, log: () => undefined }));
+  builtPerApp.push(built);
+  return listen(http.createServer(app));
+}
+
+beforeAll(async () => {
+  const recorder = http.createServer((req, res) => {
+    req.resume();
+    req.on('end', () => {
+      seen.push(req.method + ' ' + req.url);
+      res.writeHead(200, { 'content-type': 'application/json' });
+      res.end('{}');
+    });
+  });
+  const recorderUrl = await listen(recorder);
+  vi.stubEnv('NODE_ENV', 'test');
+  vi.stubEnv('ORIGINATE_SERVICE_URL', recorderUrl);
+  vi.stubEnv('SUBJECTS_ERASE_SCOPE_ENFORCED', 'true');
+  vi.resetModules();
+  vi.doMock('express', async (importOriginal) => {
+    const real = (await importOriginal()) as any;
+    const base = real.default ?? real;
+    const Router = (options?: Record<string, unknown>) => {
+      routerCalls += 1;
+      const r = base.Router({ ...(options ?? {}), caseSensitive: routerCalls === sensitiveCall });
+      built.push(Boolean(r.caseSensitive));
+      return r;
+    };
+    const wrapped = Object.assign((...args: unknown[]) => base(...args), base, { Router });
+    return { ...real, Router, default: wrapped };
+  });
+  doorUrl = await buildApp(2);
+  factoryUrl = await buildApp(1);
+}, 60000);
+
+afterAll(async () => {
+  for (const server of servers) {
+    server.closeAllConnections();
+    await new Promise<void>((r) => server.close(() => r()));
+  }
+  vi.doUnmock('express');
+  vi.resetModules();
+  vi.unstubAllEnvs();
+});
+
+// send the path verbatim so the dot segment reaches the gateway unresolved
+function send(base: string, path: string): Promise<unknown[]> {
+  return new Promise((resolve, reject) => {
+    const target = new URL(base);
+    const before = seen.length;
+    const req = http.request({ hostname: target.hostname, port: target.port, path, method: 'GET', agent: false }, (res) => {
+      const chunks: Buffer[] = [];
+      res.on('data', (d) => chunks.push(d));
+      res.on('end', () => {
+        let code: unknown = null;
+        try {
+          code = JSON.parse(Buffer.concat(chunks).toString()).error.code;
+        } catch {
+          code = null;
+        }
+        setTimeout(() => resolve([res.statusCode, code, seen.slice(before)]), 50);
+      });
+    });
+    req.on('error', reject);
+    req.end();
+  });
+}
+
+describe('KS-1212 - the erasure door follows its own router case rule, not the factory router', () => {
+  it('KS-1212 R1 - door router case sensitive, factory router default - GET /api/gdpr/ERASURES/.. is not the door and is forwarded', async () => {
+    CELLS_RUN += 1;
+    expect(await send(doorUrl, '/api/gdpr/ERASURES/..')).toEqual([200, null, ['GET /api/gdpr/ERASURES/..']]);
+  });
+  it('KS-1212 R2 - factory router case sensitive, door router default - GET /api/gdpr/ERASURES/.. is the door and is refused', async () => {
+    CELLS_RUN += 1;
+    expect(await send(factoryUrl, '/api/gdpr/ERASURES/..')).toEqual([400, 'NON_CANONICAL_PATH', []]);
+  });
+  it('KS-1212 CONTROL - each factory built two routers with only the intended one case sensitive, and erasures/.. is refused on both apps', async () => {
+    CELLS_RUN += 1;
+    const door = await send(doorUrl, '/api/gdpr/erasures/..');
+    const factory = await send(factoryUrl, '/api/gdpr/erasures/..');
+    expect([builtPerApp, door, factory]).toEqual([[[false, true], [true, false]], [400, 'NON_CANONICAL_PATH', []], [400, 'NON_CANONICAL_PATH', []]]);
+  });
+  it('KS-1212 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});```
