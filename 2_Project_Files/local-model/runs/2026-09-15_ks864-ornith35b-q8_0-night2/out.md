```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/system-status.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/system-status.ts
@@ -38,16 +38,14 @@ interface DependencyDefinition {
   required: boolean;
 }
 
-const getServiceUrl = (envVar: string, localPort: number, azureServiceName?: string): string => {
+// KS-864: rename to underscore-prefixed so noUnusedParameters accepts it.
+const getServiceUrl = (envVar: string, localPort: number, _azureServiceName?: string): string => {
   // Check for explicit environment variable first
   const envUrl = process.env[envVar];
   if (envUrl) return envUrl;
   
-  // In Azure staging, use internal URLs
-  if (process.env.NODE_ENV === 'staging' && azureServiceName) {
-    return `https://${azureServiceName}.internal.ashypond-b460d1a1.westeurope.azurecontainerapps.io`;
-  }
+  // KS-864: the Azure staging estate is decommissioned — URLs come from the env var above or the local default.
   
   // Default to localhost for development
   return `http://localhost:${localPort}`;
 };
@@ -229,8 +227,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'issuer-portal',
     description: 'Document issuer web application',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging' 
-      ? 'https://secuura-staging-issuer.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
+    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',
       : (process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80'),
     healthPath: '/',
     category: 'frontend',
@@ -240,8 +237,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'verifier-portal',
     description: 'Document verification web application',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging'
-      ? 'https://secuura-staging-verifier.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
+    url: process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80',
       : (process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80'),
     healthPath: '/verify/',
     category: 'frontend',
@@ -251,8 +247,7 @@ const SERVICES: ServiceDefinition[] = [
     name: 'admin-portal',
     description: 'Enterprise administration dashboard',
     port: 8882,
-    url: process.env.NODE_ENV === 'staging'
-      ? 'https://secuura-staging-admin.ashypond-b460d1a1.westeurope.azurecontainerapps.io'
+    url: process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80',
       : (process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80'),
     healthPath: '/admin/',
     category: 'frontend',

--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks864-dead-estate-pointers-in-runtime-source.test.ts
@@ -0,0 +1,95 @@
+/**
+ * KS-864 — no dead Azure estate pointers in runtime source outside deployment/.
+ */
+import { describe, it, expect, vi, afterAll } from 'vitest';
+import http from 'node:http';
+
+// Set env BEFORE import so the module's top-level table reads them once.
+const savedEnv = { ...process.env };
+process.env.NODE_ENV = 'staging';
+process.env.API_GATEWAY_URL = 'http://gw.example:1';
+delete process.env.ISSUER_PORTAL_URL;
+delete process.env.VERIFIER_PORTAL_URL;
+delete process.env.ADMIN_PORTAL_URL;
+
+vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
+vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('offline in test'); }));
+
+const router = (await import('../routes/system-status')).default;
+
+function mountAndGetPort(): Promise<number> & { close: () => void } {
+  return new Promise((resolve) => {
+    const app = require('express')();
+    app.use('/api/system', router);
+    const server = app.listen(0, '127.0.0.1', () => resolve(server.address().port as number));
+    // attach close to the resolved promise for convenience below
+    (server as any).closeSync = () => server.close();
+  });
+}
+
+describe('KS-864 — no dead Azure estate URLs served by GET /status', () => {
+  let port: number | null = null;
+  let closeServer: (() => void) | null = null;
+
+  beforeAll(async () => {
+    const p = await mountAndGetPort();
+    port = p;
+    closeServer = ((p as unknown) as { close: () => void }).close || (((s: any) => s && s.close()) as any)(null);
+  }, 10_000);
+
+  afterAll(() => {
+    if (closeServer) closeServer();
+    Object.keys(savedEnv).forEach((k) => {
+      if (!(k in process.env)) delete process.env[k]; else process.env[k] = savedEnv[k];
+    });
+    vi.unstubAllGlobals();
+  });
+
+  it('🔴 KS-864 — no served service URL names the dead estate', async () => {
+    expect(port).toBeGreaterThan(0);
+    const body = await httpGetJson(port!, '/api/system/status');
+    const allServices = Object.values(body.services).flat() as Array<{ name?: string; url?: string }>;
+    for (const svc of allServices) {
+      expect(svc.url ?? '').not.toContain('ashypond-b460d1a1');
+      expect(svc.url ?? '').not.toContain('westeurope');
+    }
+    const portals = allServices.filter((s) => /portal/i.test(s.name ?? ''));
+    for (const p of portals) {
+      expect(p.url ?? '').not.toContain('secuura-staging-');
+    }
+  });
+
+  it('🔴 KS-864 — the issuer portal falls back to its compose default when its env var is unset', async () => {
+    expect(port).toBeGreaterThan(0);
+    const body = await httpGetJson(port!, '/api/system/status');
+    const allServices = Object.values(body.services).flat() as Array<{ name?: string; url?: string }>;
+    const issuer = allServices.find((s) => s.name === 'issuer-portal');
+    expect(issuer?.url).toBe('http://issuer-frontend:80');
+  });
+
+  it('KS-864 control — an explicit env var still wins', async () => {
+    // passes both before and after the fix: API_GATEWAY_URL was set above.
+    expect(process.env.API_GATEWAY_URL).toBe('http://gw.example:1');
+    const body = await httpGetJson(port!, '/api/system/status');
+    const allServices = Object.values(body.services).flat() as Array<{ name?: string; url?: string }>;
+    const gw = allServices.find((s) => s.name === 'api-gateway');
+    expect(gw?.url).toBe('http://gw.example:1');
+  });
+});
+
+function httpGetJson(serverPort: number, path: string): Promise<any> {
+  return new Promise((resolve, reject) => {
+    http.get({ hostname: '127.0.0.1', port: serverPort, path }, (res) => {
+      let data = '';
+      res.on('data', (c) => (data += c));
+      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
+    }).on('error', reject);
+  });
+}
```
