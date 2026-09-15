# READY — KS-888 (dbSaveApiKey: structural INSERT failures re-raise; a mint that cannot persist no longer answers 201) — Ornith ornith:35b (Q4_K_M) first sample (`2026-09-15_ks888-ornith35b-night`, 48 s), re-checked by Wednesday 16:43 PASS 7/7 at develop M55 48e65c435. The runner's verdict was A2b PLACEHOLDER: the model wrote the test file's header once, a 1-line stub hunk, then the real 120-line body as a SECOND new-file hunk; the splitter had turned the body into a second, invented path. Fixed where it lives (checker splitter STUB HUNK DROPPED, backup `.pre-0915-stubmerge`) and re-checked on the same output: 2 🔴 red at the tip (201 → ≥500; key material gone) / control green / 3 green after / security suite Δ 0 / tsc 0. The first widened-pool ticket under Kam's 16:36/16:40 ruling (simple, not auth).
# Source read by Wednesday: the product hunk is the brief's exactly — the catch at :330-332 logs with the SQLSTATE code and re-raises classes 42/23/22 (structural), leaving 08/57 log-only (the decision stated from the ticket's own fix shape); the route's existing `next(error)` answers. The test mocks `../db` (isDbAvailable true; INSERT rejects with code 42703 on a flag), drives POST /api/keys with the ks742 RS256 platform token, and reads the response. Note for the raising seat: `dbSaveApiKey` is also called at :1261 and :1329 — a structural error now surfaces there too (the ticket names ALL key persistence as the blast radius). The diff below is the checker's merged section (the stub dropped) — apply this file.

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -327,7 +327,10 @@ async function dbSaveApiKey(k: ApiKey): Promise<void> {
        [k.id, k.organizationId, k.tenantId, k.name, k.keyHash, k.keyPrefix,
         JSON.stringify(k.scopes || []),
         k.rateLimit, k.rateLimitWindow, k.lastUsedAt || null, k.usageCount, k.isActive,
         k.expiresAt || null, k.createdAt, k.connectorId ?? null]
     ));
   } catch (err: any) {
-    logger.error('DB save API key failed', { error: err?.message });
+    logger.error('DB save API key failed', { error: err?.message, code: err?.code });
+    // KS-888: a mint that cannot persist must not answer 201 — a STRUCTURAL failure (SQLSTATE class 42 undefined
+    // object/syntax, 23 integrity, 22 data) re-raises to the caller's error path; transient classes (08, 57) stay
+    // log-only so an in-memory key still serves through a DB blip.
+    if (typeof err?.code === 'string' && /^(42|23|22)/.test(err.code)) throw err;
   }
 }
 
--- /dev/null
+++ b/services/security/src/__tests__/ks888-mint-does-not-201-when-persist-fails.test.ts
@@ -0,0 +1,120 @@
+/**
+ * KS-888: `dbSaveApiKey` swallows structural INSERT failures and answers 201 with live key material anyway.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import crypto from 'crypto';
+import type { Server } from 'http';
+import type { AddressInfo } from 'net';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+const TENANT_A = 'a0000000-0000-4000-8000-0000000000aa';
+const ORG_A = '11111111-1111-4111-8111-111111111111';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const b64url = (b: Buffer): string =>
+  b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
+
+function token(claims: Record<string, unknown>): string {
+  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) as Buffer);
+  const now = Math.floor(Date.now() / 1000);
+  const payload = b64url(
+    Buffer.from(JSON.stringify({ sub: 'test-user', iat: now, exp: now + 300, ...claims })),
+  );
+  const signature = b64url(
+    crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM) as Buffer,
+  );
+  return `${header}.${payload}.${signature}`;
+}
+
+const PLATFORM = () => token({ role: 'super_admin' });
+
+let server: Server | undefined;
+let base: string;
+
+const state = vi.hoisted(() => ({ failInsertWith: null as string | null }));
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: async (_sql: string, _params?: any[]) => {
+    if (/INSERT INTO svc_api_keys/i.test(_sql) && state.failInsertWith) {
+      throw Object.assign(new Error('column "connector_id" of relation "svc_api_keys" does not exist'), { code: state.failInsertWith });
+    }
+    return { rows: [] };
+  },
+}));
+
+async function mintRaw(): Promise<Response> {
+  return fetch(`${base}/api/keys`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${PLATFORM()}` },
+    body: JSON.stringify({ name: 'ks888', organizationId: ORG_A, tenantId: TENANT_A, scopes: ['documents:read'] }),
+  });
+}
+
+beforeAll(async () => {
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+
+  const app = (await import('../index')).default;
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', resolve);
+  });
+  base = `http://127.0.0.1:${(server!.address() as AddressInfo).port}`;
+});
+
+afterAll(async () => {
+  if (server) {
+    await new Promise<void>((resolve) => server.close(() => resolve()));
+  }
+});
+
+describe('KS-888 — dbSaveApiKey swallow on INSERT failure', () => {
+  it('🔴 KS-888 — a mint whose INSERT fails with SQLSTATE 42703 does NOT answer 201', async () => {
+    try {
+      state.failInsertWith = '42703';
+      const res = await mintRaw();
+      expect(res.status).not.toBe(201);
+      expect(res.status).toBeGreaterThanOrEqual(500);
+    } finally {
+      state.failInsertWith = null;
+    }
+  });
+
+  it('🔴 KS-888 — the failed mint hands out no key material', async () => {
+    try {
+      state.failInsertWith = '42703';
+      const res = await mintRaw();
+      const body: any = await res.json();
+      expect(body?.data?.key).toBeUndefined();
+    } finally {
+      state.failInsertWith = null;
+    }
+  });
+
+  it('KS-888 control — a mint whose INSERT succeeds answers 201 with an id', async () => {
+    try {
+      state.failInsertWith = null;
+      const res = await mintRaw();
+      expect(res.status).toBe(201);
+      const body: any = await res.json();
+      expect(typeof body.data.id).toBe('string');
+    } finally {
+      state.failInsertWith = null;
+    }
+  });
+});
```
