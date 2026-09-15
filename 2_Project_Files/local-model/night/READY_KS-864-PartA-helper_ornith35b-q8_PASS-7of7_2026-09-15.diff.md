# READY — KS-864 PART A of two (the `getServiceUrl` helper: E1 parameter rename + E2 the dead staging branch removed) — Ornith ornith:35b-q8_0 PASS 7/7 FIRST RUN on the split brief, 2026-09-15 15:32 — tip develop M55 48e65c435. Run `runs/2026-09-15_ks864-ornith35b-q8_0-night4` (25 s, 1,131 tokens). The five-edit brief failed four rounds on four different single slips (rows 44/58–60); the split landed both halves' first samples. Applied with --recount (one miscounted header). Part B (the three portal ternaries) is a SEPARATE READY file; a Secuura seat raises A + B as ONE PR (the ticket is one line of work).
# Source read by Wednesday: the two `-`/`+` edits are the brief's exactly; ONE deviation, harmless — the model added a one-line comment above the const (`// KS-864: renamed parameter so noUnusedParameters accepts it; body drops dead Azure staging.`) — the raising seat may keep or drop it. The test file kept the earlier name `ks864-dead-estate-pointers-in-runtime-source.test.ts` (the brief asked for `ks864a-…`); its three cells are the brief's (api-gateway → localhost:8080 under staging with the env var unset; no served URL contains `.internal.ashypond`; anchoring honours ANCHORING_SERVICE_URL as the control). After A alone the portals still carry `secuura-staging-*` — that is Part B.

```diff
--- a/services/api-gateway/src/routes/system-status.ts
+++ b/services/api-gateway/src/routes/system-status.ts
@@ -38,16 +38,15 @@ interface DependencyDefinition {
 
 // Helper to determine environment-appropriate URL
-const getServiceUrl = (envVar: string, localPort: number, azureServiceName?: string): string => {
+// KS-864: renamed parameter so noUnusedParameters accepts it; body drops dead Azure staging.
+const getServiceUrl = (envVar: string, localPort: number, _azureServiceName?: string): string => {
   // Check for explicit environment variable first
   const envUrl = process.env[envVar];
   if (envUrl) return envUrl;
   
-  // In Azure staging, use internal URLs
-  if (process.env.NODE_ENV === 'staging' && azureServiceName) {
-    return `https://${azureServiceName}.internal.ashypond-b460d1a1.westeurope.azurecontainerapps.io`;
-  }
+  // KS-864: the Azure staging estate is decommissioned — URLs come from the env var above or the localhost default.
   
   // Default to localhost for development
   return `http://localhost:${localPort}`;
 };
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks864-dead-estate-pointers-in-runtime-source.test.ts
@@ -0,0 +1,65 @@
+import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
+import http from 'node:http';
+import express from 'express';
+
+const savedEnv = { ...process.env };
+process.env.NODE_ENV = 'staging';
+process.env.ANCHORING_SERVICE_URL = 'http://anch.example:1';
+delete process.env.API_GATEWAY_URL;
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
+describe('KS-864 A — dead Azure estate pointers removed from runtime source', () => {
+  it('🔴 KS-864 A — api-gateway falls back to its localhost default under NODE_ENV=staging when its env var is unset', async () => {
+    const services = await flatServices();
+    const gw = services.find((s) => s.name === 'api-gateway')?.url;
+    expect(gw).toBe('http://localhost:8080');
+  });
+
+  it('🔴 KS-864 A — no served URL names the internal dead estate', async () => {
+    const services = await flatServices();
+    for (const s of services) {
+      expect(s.url ?? '').not.toContain('.internal.ashypond');
+    }
+  });
+
+  it('KS-864 A control — an explicit env var still wins', async () => {
+    const services = await flatServices();
+    const anchoring = services.find((s) => s.name === 'anchoring');
+    expect(anchoring?.url).toBe('http://anch.example:1');
+  });
+});
```
