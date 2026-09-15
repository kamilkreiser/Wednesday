# READY — KS-908 — Ornith ornith:35b (Q4_K_M) PASS 7/7 on the re-run (round 2, 12:16) under the REANCHORED accommodation (two insert-only hunks placed at :1150 and :1211 from the model's + lines) — tip develop M55 48e65c435
# Source read by Wednesday: the two inserted lines are the brief's (POST 201 data + GET list view, `|| null`); cells: 2 red at the tip / control green, green after, security suite Δ 0, tsc 0. Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks908-ornith35b-night2. HELD for a Secuura seat (tier 1 — the security service).

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -1147,6 +1147,7 @@
         scopes: apiKey.scopes,
         rateLimit: apiKey.rateLimit,
         createdAt: apiKey.createdAt,
+        connectorId: apiKey.connectorId || null, // KS-908: was persisted but invisible through POST response.
         // KS-577: reported, not assumed. `null` means the revoke was attempted
         // and FAILED, so the prior credential is still valid — a caller that
         // ignores this is back to the bug.
@@ -1208,6 +1208,7 @@
       usageCount: k.usageCount,
       isActive: k.isActive,
       createdAt: k.createdAt,
+      connectorId: k.connectorId || null, // KS-908: was persisted but invisible through GET list response.
     }));
   
   res.json({

--- /dev/null
+++ b/services/security/src/__tests__/ks908-connectorid-persists-but-is-invisible-through.test.ts
@@ -0,0 +1,107 @@
+/**
+ * KS-908 — wire test that `connectorId` survives the round-trip for both POST and GET.
+ */
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
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
+let server: Server | undefined;
+let base: string;
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
+  if (!server) return;
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+describe('KS-908 — connectorId persists but is invisible through the API', () => {
+  it('🔴 KS-908 — POST /api/keys returns the connectorId it was given', async () => {
+    const res = await fetch(`${base}/api/keys`, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
+      body: JSON.stringify({
+        name: 'probe',
+        organizationId: ORG_A,
+        tenantId: TENANT_A,
+        scopes: ['documents:read'],
+        connectorId: 'probe-connector-908',
+      }),
+    });
+    expect(res.status).toBe(201);
+    const body = (await res.json()) as { data?: Record<string, unknown> };
+    expect(body.data?.connectorId).toBe('probe-connector-908');
+  });
+
+  it('🔴 KS-908 — GET /api/keys lists the connectorId for that key', async () => {
+    const postRes = await fetch(`${base}/api/keys`, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
+      body: JSON.stringify({
+        name: 'probe-list',
+        organizationId: ORG_A,
+        tenantId: TENANT_A,
+        scopes: ['documents:read'],
+        connectorId: 'probe-connector-908',
+      }),
+    });
+    expect(postRes.status).toBe(201);
+    const created = (await postRes.json()) as { data?: { id: string } };
+
+    const listRes = await fetch(`${base}/api/keys?organizationId=${ORG_A}`, {
+      headers: { Authorization: `Bearer ${token({ role: 'super_admin' })}` },
+    });
+    expect(listRes.status).toBe(200);
+    const listBody = (await listRes.json()) as { data: Array<Record<string, unknown>> };
+    const row = listBody.data.find((k) => k.id === created.data!.id);
+    expect(row).toBeDefined();
+    expect(row!.connectorId).toBe('probe-connector-908');
+  });
+
+  it('KS-908 control — a key minted without a connectorId reads back connectorId: null, and the other fields are unchanged', async () => {
+    const postRes = await fetch(`${base}/api/keys`, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
+      body: JSON.stringify({
+        name: 'no-conn-control',
+        organizationId: ORG_A,
+        tenantId: TENANT_A,
+        scopes: ['documents:read'],
+      }),
+    });
+    expect(postRes.status).toBe(201);
+    const created = (await postRes.json()) as { data?: Record<string, unknown> };
+    expect(created.data?.connectorId ?? null).toBe(null);
+    expect(created.data?.id).toBeTruthy();
+    expect(created.data?.name).toBe('no-conn-control');
+    expect(created.data?.prefix).toBeTruthy();
+    expect(Array.isArray(created.data?.scopes)).toBe(true);
+
+    const listRes = await fetch(`${base}/api/keys?organizationId=${ORG_A}`, {
+      headers: { Authorization: `Bearer ${token({ role: 'super_admin' })}` },
+    });
+    expect(listRes.status).toBe(200);
+    const listBody = (await listRes.json()) as { data: Array<Record<string, unknown>> };
+    const row = listBody.data.find((k) => k.id === created.data!.id);
+    expect(row).toBeDefined();
+    expect(row!.connectorId ?? null).toBe(null);
+    expect(row!.name).toBe('no-conn-control');
+    expect(row!.prefix).toBeTruthy();
+    expect(Array.isArray(row!.scopes)).toBe(true);
+    expect(typeof row!.isActive).toBe('boolean');
+    expect(row!.createdAt).toBeTruthy();
+  });
+});
```
