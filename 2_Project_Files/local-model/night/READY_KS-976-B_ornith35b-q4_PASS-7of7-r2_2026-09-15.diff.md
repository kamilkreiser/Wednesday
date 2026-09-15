# READY — KS-976 PART B of two (security `index.ts:1379` (/check) and `:1489` (/reset): the 403 says "Caller scope claims are present but unusable (tenant, user or sub)" when any scope claim is present, "Caller has no tenant" only when none is — the two families `principalScope`/`explicitScope` collapse into one null)
# Source read by me (Wednesday): both product hunks are the brief's (the predicate INLINE at each site — r1's helper-function shape was placed inside a `/**` comment by the re-anchor, a harness defect since fixed; the PR seat may hoist the predicate into one `scopeRefusalMessage(user)` helper as polish); lines 752 and 803 untouched. Test: the real-HTTP harness with the regex-free `b64url`; two 🔴 cells (/check with a non-string userId; /reset with a blank tenant claim → both 'unusable') + one control (no scope claim at all → 'Caller has no tenant'; a good principal → 200). Checker: A3b 2/2, A4 RED-FIRST 2/3 at the tip, A5 3/3, suite 213 → 216 green, NEW reds []. Round 2. Run: runs/2026-09-15_ks976-ornith35b-night4.
# PR NOTES: ONE PR with Part A — the two auto-named test files collide (`ks976-rate-limit-refusals-name-the-wrong.test.ts` both): rename A → `ks976-reset-400-names-the-failing-field.test.ts`, B → `ks976-403-says-which-scope-claim-failed.test.ts`. KS-976 is COMPLETE in Ornith's hands.

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -1376,7 +1376,9 @@ app.post('/api/rate-limit/check', (req: Request, res: Response, next: NextFuncti
       return res.status(403).json({
         success: false,
-        error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
+        // KS-976 item 2: `scope` is null for three reasons — say whether a claim was present but unusable, or absent.
+        error: { code: 'FORBIDDEN', message: [(req as any).user?.tenantId, (req as any).user?.userId, (req as any).user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
       });
     }
     const bucketKey = scopedRateLimitKey(scope, data.key);
@@ -1486,7 +1488,9 @@ app.post('/api/rate-limit/reset', requirePlatformOperatorForRateLimit, (req: Requ
     return res.status(403).json({
       success: false,
-      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
+      error: { code: 'FORBIDDEN', message: [(req as any).user?.tenantId, (req as any).user?.userId, (req as any).user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
     });
   }
   rateLimits.delete(scopedRateLimitKey(scope, parsedBody.data.key));
--- /dev/null
+++ b/services/security/src/__tests__/ks976-rate-limit-refusals-name-the-wrong.test.ts
@@ -0,0 +1,107 @@
+/**
+ * =============================================================================
+ * KS-976 — Rate-limit refusals name the wrong field
+ * =============================================================================
+ */
+
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import crypto from 'node:crypto';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const b64url = (b: Buffer): string => b.toString('base64url');
+
+function token(claims: Record<string, unknown>): string {
+  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) as Buffer);
+  const now = Math.floor(Date.now() / 1000);
+  const payload = b64url(Buffer.from(JSON.stringify({
+    sub: 'ks952', iat: now, exp: now + 300, role: 'ISSUER_ADMIN', ...claims,
+  })) as Buffer);
+  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
+  return `${header}.${payload}.${sig}`;
+}
+
+const TENANT_A = 'a0000000-0000-4000-8000-00000000000a';
+let server: Server;
+let base: string;
+
+afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+
+async function post(path: string, claims: Record<string, unknown>, body: Record<string, unknown>) {
+  const res = await fetch(`${base}${path}`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token(claims)}` },
+    body: JSON.stringify(body),
+  });
+  const json: any = await res.json();
+  return { status: res.status, json };
+}
+
+beforeAll(async () => {
+  process.env.SECURITY_DISABLE_BOOT = '1';
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  const mod = await import('../index');
+  const app = mod.default;
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
+  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+
+describe('KS-976 — rate-limit refusals name the wrong field', () => {
+  it('\u{1F534} KS-976 \u2014 /check with a good tenant and a non-string userId is refused as UNUSABLE, not "no tenant"', async () => {
+    const r = await post('/api/rate-limit/check', { tenantId: TENANT_A, userId: 123 }, { key: 'login' });
+    expect(r.status).toBe(403);
+    expect(r.json.error.message).toContain('unusable');
+  });
+
+  it('\u{1F534} KS-976 \u2014 /reset by a platform operator whose tenant claim is blank is refused as UNUSABLE', async () => {
+    const r = await post('/api/rate-limit/reset', { role: 'SYSTEM_ADMIN', tenantId: '   ', userId: 'operator-1' }, { key: 'login' });
+    expect(r.status).toBe(403);
+    expect(r.json.error.message).toContain('unusable');
+  });
+
+  it('KS-976 control \u2014 a token with no scope claim at all still says "Caller has no tenant"; a good principal still passes', async () => {
+    const none = await post('/api/rate-limit/check', { sub: undefined }, { key: 'login' });
+    expect(none.status).toBe(403);
+    expect(none.json.error.message).toBe('Caller has no tenant');
+
+    const ok = await post('/api/rate-limit/check', { tenantId: TENANT_A, userId: 'u-1' }, { key: 'login' });
+    expect(ok.status).toBe(200);
+  });
+});
```
