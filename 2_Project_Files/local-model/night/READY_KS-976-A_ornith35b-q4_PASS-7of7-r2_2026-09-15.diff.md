# READY — KS-976 PART A of two (security `index.ts:1470`: `/reset`'s 400 names the FIRST failing field — `tenantId: must not be blank` / `tenantId: must not exceed 256 characters` / `key: Required` — instead of the constant "Key required"; `details` unchanged)
# Source read by me (Wednesday): the product hunk is the brief byte-for-byte (comment + `first`/`field` + the templated message); the test is a real-HTTP harness (RSA pair + `token()` + `SECURITY_DISABLE_BOOT` + `listen(0)`) copied from ks952's route test with a regex-free `b64url` (`toString('base64url')`); two 🔴 cells (blank tenantId names tenantId; over-long tenantId names the bound) + one control (missing key → details name `key`; a good body → 200). Checker: A4 RED-FIRST 2/3 at the tip, A5 3/3 after, suite 213 → 216 green, NEW reds []. Round 2 — r1 and its RETRY-ONCE both loaded no test (the copied `b64url` regex lost a backslash twice; the brief now gives the helper regex-free). Run: runs/2026-09-15_ks976-ornith35b-night2.
# PR NOTES: ONE PR with Part B (the 403 split, running/queued); the harness auto-named the test from the title — rename to `ks976-reset-400-names-the-failing-field.test.ts`; Part B's test needs its own name too (`ks976-403-says-which-scope-claim-failed.test.ts`).

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -1467,7 +1467,11 @@ app.post('/api/rate-limit/reset', requirePlatformOperatorForRateLimit, (req: Req
 
   const parsedBody = resetRateLimitSchema.safeParse(req.body);
   if (!parsedBody.success) {
-    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Key required', details: parsedBody.error.errors } });
+    // KS-976 item 1: the top-level message names the FIRST failing field. A blank `tenantId`
+    // used to answer "Key required" with a perfectly good key; the truth was only in `details`.
+    const first = parsedBody.error.errors[0];
+    const field = first && first.path.length > 0 ? first.path.join('.') : 'body';
+    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `${field}: ${first ? first.message : 'invalid request body'}`, details: parsedBody.error.errors } });
   }
 
   // KS-952 (the folded-in KS-645 half): /check now stores under a
--- /dev/null
+++ b/services/security/src/__tests__/ks976-rate-limit-refusals-name-the-wrong.test.ts
@@ -0,0 +1,101 @@
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
+    sub: 'ks976', iat: now, exp: now + 300, role: 'SYSTEM_ADMIN', ...claims,
+  })) as Buffer);
+  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
+  return `${header}.${payload}.${sig}`;
+}
+
+const TENANT_A = 'a0000000-0000-4000-8000-00000000000a';
+
+let server: Server;
+let base: string;
+
+afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+
+async function reset(body: Record<string, unknown>) {
+  const res = await fetch(`${base}/api/rate-limit/reset`, {
+    method: 'POST',
+    headers: {
+      'Content-Type': 'application/json',
+      Authorization: `Bearer ${token({ role: 'SYSTEM_ADMIN', tenantId: TENANT_A, userId: 'operator-1' })}`,
+    },
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
+describe('KS-976 — the top-level error message names the failing field', () => {
+  it('\u{1F534} KS-976 \u2014 a blank tenantId is refused naming tenantId, not the key', async () => {
+    const r = await reset({ key: 'login', tenantId: '   ' });
+    expect(r.status).toBe(400);
+    expect(r.json.error.message).toContain('tenantId');
+    expect(r.json.error.message).not.toBe('Key required');
+  });
+
+  it('\u{1F534} KS-976 \u2014 an over-long tenantId is refused naming tenantId and the bound', async () => {
+    const r = await reset({ key: 'login', tenantId: 'a'.repeat(257) });
+    expect(r.status).toBe(400);
+    expect(r.json.error.message).toBe('tenantId: must not exceed 256 characters');
+  });
+
+  it('KS-976 control \u2014 a missing key is still a 400 whose details name key, and a good body still resets', async () => {
+    const r = await reset({});
+    expect(r.status).toBe(400);
+    expect(r.json.error.code).toBe('BAD_REQUEST');
+    expect(r.json.error.details[0].path).toEqual(['key']);
+
+    const ok = await reset({ key: 'login', tenantId: TENANT_A });
+    expect(ok.status).toBe(200);
+  });
+});
```
