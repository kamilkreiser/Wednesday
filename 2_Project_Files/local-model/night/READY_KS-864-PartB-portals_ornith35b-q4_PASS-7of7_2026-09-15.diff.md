# READY — KS-864 PART B of two (the three portal ternaries E3/E4/E5 → env-or-default) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST RUN on the split brief, 2026-09-15 15:35 — tip develop M55 48e65c435. Run `2026-09-15_ks864-ornith35b-night2` (27 s, 1,410 tokens). With Part A (helper, q8) held beside it, KS-864 is COMPLETE: a Secuura seat raises A + B as ONE PR; after both, `grep -c 'ashypond\|westeurope\|secuura-staging-' system-status.ts` = the 17 untouched call-site arguments only.
# Source read by Wednesday: the three `-`×3/`+`×1 edits are the brief's exactly (issuer/verifier/admin env-or-compose-default); the cells are the brief's (issuer-portal → http://issuer-frontend:80 under staging with the env var unset; no portal url contains secuura-staging-; api-gateway honours API_GATEWAY_URL as the control).

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/system-status.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/system-status.ts
@@ -228,9 +228,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'issuer-portal',
     description: 'Document issuer web application',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging' 
-      ? 'https://secuura-staging-issuer.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
-      : (process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80'),
+    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',
     healthPath: '/',
     category: 'frontend',
     required: false,
@@ -239,9 +237,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'verifier-portal',
     description: 'Document verification web application',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging'
-      ? 'https://secuura-staging-verifier.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
-      : (process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80'),
+    url: process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80',
     healthPath: '/verify/',
     category: 'frontend',
     required: false,
@@ -250,9 +246,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'admin-portal',
     description: 'Enterprise administration dashboard',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging'
-      ? 'https://secuura-staging-admin.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
-      : (process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80'),
+    url: process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80',
     healthPath: '/admin/',
     category: 'frontend',
     required: false,

--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks864-dead-estate-pointers-in-runtime-source.test.ts
@@ -0,0 +1,62 @@
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.NODE_ENV = 'staging';
+process.env.API_GATEWAY_URL = 'http://gw.example:1';
+delete process.env.ISSUER_PORTAL_URL; delete process.env.VERIFIER_PORTAL_URL; delete process.env.ADMIN_PORTAL_URL;
+
+vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
+vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('offline in test'); }));
+
+const router = (await import('../routes/system-status')).default;
+
+let server: http.Server; let port = 0;
+beforeAll(async () => {
+  const app = express(); app.use('/api/system', router);
+  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { port = (server.address() as any).port; r(); }); }, 10_000);
+}, 10_000);
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
+  Object.assign(process.env, savedEnv);
+  vi.unstubAllGlobals();
+});
+function getJson(path: string): Promise<any> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
+      let data = ''; res.on('data', (c) => (data += c));
+      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
+    }).on('error', reject);
+  });
+}
+async function flatServices(): Promise<Array<{ name?: string; url?: string }>> {
+  const body = await getJson('/api/system/status');
+  return Object.values(body.services).flat() as any;
+}
+
+describe('KS-864 — dead-estate portal URLs removed from runtime source', () => {
+  it('🔴 KS-864 B — the issuer portal falls back to its compose default under NODE_ENV=staging when its env var is unset', async () => {
+    expect((await flatServices()).find((s) => s.name === 'issuer-portal')?.url).toBe('http://issuer-frontend:80');
+  });
+
+  it('🔴 KS-864 B — no portal URL names the dead estate', async () => {
+    const portals = (await flatServices()).filter(s => ['issuer-portal', 'verifier-portal', 'admin-portal'].includes(s.name ?? ''));
+    for (const s of portals) {
+      expect(s.url ?? '').not.toContain('secuura-staging-');
+    }
+  });
+
+  it('KS-864 B control — an explicit env var still wins for a helper-built service', async () => {
+    const entry = (await flatServices()).find((s) => s.name === 'api-gateway');
+    expect(entry?.url).toBe('http://gw.example:1');
+  });
+});
```
