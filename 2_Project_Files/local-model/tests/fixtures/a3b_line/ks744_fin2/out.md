```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
@@ -386,12 +386,13 @@
       if (!decoded.tenantId) decoded.tenantId = DEFAULT_TENANT_ID;
       req.user = decoded;
       req.headers['x-user-id'] = decoded.userId;
-      req.headers['x-user-email'] = decoded.email;
+      if (decoded.email) req.headers['x-user-email'] = decoded.email;
       req.headers['x-user-role'] = decoded.role;
       if (decoded.organizationId) {
         req.headers['x-organization-id'] = decoded.organizationId;
       }
-      req.headers['x-verification-level'] = decoded.verificationLevel;
+      if (decoded.verificationLevel) req.headers['x-verification-level'] = decoded.verificationLevel;
+      else delete req.headers['x-verification-level'];
 
       // Tenant context: super_admin can override via X-Tenant-Id header (admin portal tenant selector)
       const SUPER_ADMIN_ROLES = ['super_admin', 'SUPER_ADMIN', 'SYSTEM_ADMIN', 'platform_admin'];
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts
@@ -0,0 +1,93 @@
+/**
+ * KS-744: a verified token that lacks a claim must not 500 a proxied route.
+ *
+ * authenticateToken copied decoded.email and decoded.verificationLevel onto the
+ * x-user-email and x-verification-level headers unguarded. A missing claim put
+ * undefined in the header bag, the proxy's outbound setHeader threw
+ * ERR_HTTP_INVALID_HEADER_VALUE, and the route answered 500 with that message.
+ * x-verification-level is not in the edge strip pattern (utils/trustHeaders.ts),
+ * so a token without the claim must also drop a client-supplied value.
+ */
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import http from 'http';
+import express from 'express';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+import { createProxyMiddleware } from 'http-proxy-middleware';
+import { authenticateToken } from '../middleware/auth';
+
+const EXPECTED_CELLS = 4;
+let CELLS_RUN = 0;
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
+const FULL: Record<string, string> = { userId: 'u-ks744', email: 'ks744@example.test', role: 'user', verificationLevel: 'basic', tenantId: 't-ks744' };
+const upstreamSeen: http.IncomingHttpHeaders[] = [];
+let upstream: http.Server;
+let gateway: http.Server;
+let gatewayUrl = '';
+
+function tokenWithout(claim: string): string {
+  const payload: Record<string, string> = { ...FULL };
+  delete payload[claim];
+  return jwt.sign(payload, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+}
+
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
+
+// [HTTP status, upstream hits, the forwarded value of the header named by pick, or null]
+async function verdict(token: string, pick: string, extra: Record<string, string>): Promise<Array<number | string | null>> {
+  upstreamSeen.length = 0;
+  const res = await fetch(gatewayUrl + '/api/ks744/probe', { headers: { authorization: 'Bearer ' + token, ...extra } });
+  await res.text();
+  const forwarded = upstreamSeen.length > 0 ? upstreamSeen[0][pick] : undefined;
+  return [res.status, upstreamSeen.length, typeof forwarded === 'string' ? forwarded : null];
+}
+
+beforeAll(async () => {
+  expect(PRIV.length).toBeGreaterThan(100);
+  upstream = http.createServer((req, res) => {
+    upstreamSeen.push({ ...req.headers });
+    res.writeHead(200, { 'content-type': 'application/json' });
+    res.end('{"success":true}');
+  });
+  const upstreamUrl = await listen(upstream);
+  const app = express();
+  app.use('/api/ks744', authenticateToken(true), createProxyMiddleware({ target: upstreamUrl, changeOrigin: true, logLevel: 'silent' }));
+  app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+  });
+  gateway = http.createServer(app);
+  gatewayUrl = await listen(gateway);
+});
+
+afterAll(async () => {
+  for (const server of [gateway, upstream]) {
+    server.closeAllConnections();
+    await new Promise<void>((resolve) => server.close(() => resolve()));
+  }
+});
+
+describe('KS-744 - a verified token missing a claim is proxied, not answered 500', () => {
+  it('KS-744 R1 - no email claim: 200, one upstream hit, no x-user-email forwarded', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(tokenWithout('email'), 'x-user-email', {})).toEqual([200, 1, null]);
+  });
+  it('KS-744 R2 - no verificationLevel claim: 200, one upstream hit, no x-verification-level forwarded', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(tokenWithout('verificationLevel'), 'x-verification-level', {})).toEqual([200, 1, null]);
+  });
+  it('KS-744 R3 - no verificationLevel claim: a client-supplied x-verification-level is dropped', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(tokenWithout('verificationLevel'), 'x-verification-level', { 'x-verification-level': 'enhanced' })).toEqual([200, 1, null]);
+  });
+  it('KS-744 CONTROL - a token carrying every claim forwards the email and the level', async () => {
+    CELLS_RUN += 1;
+    expect(await verdict(tokenWithout('none'), 'x-user-email', {})).toEqual([200, 1, 'ks744@example.test']);
+    expect(await verdict(tokenWithout('none'), 'x-verification-level', { 'x-verification-level': 'enhanced' })).toEqual([200, 1, 'basic']);
+  });
+  it('KS-744 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
