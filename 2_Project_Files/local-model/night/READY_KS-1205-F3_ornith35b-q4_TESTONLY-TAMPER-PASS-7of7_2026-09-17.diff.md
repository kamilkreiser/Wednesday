# READY — KS-1205 F-3 G-BUCKET-HASH (NEW api-gateway test pinning that an API key's limiter bucket is never api_key: plus the bare sha256 of the key; tamper middleware/auth.ts:300; 1 red cell + control) — Ornith ornith:35b q4, first sample, PASS 7/7 at 16:52 2026-09-17 on tip f8c7aaa39 (READY written 16:58)
# Source read by Wednesday: the model's 77 `+` lines IDENTICAL to the brief's test fence (python compare; a mutated copy unequal); one new file, no product change; apply STRICT; A4: the ONE declared red (R1) is the failed name under the tamper (1 failed / 3 run).
# PR NOTES: `Refs KS-1205 (F-3 G-BUCKET-HASH)`, NEVER Closes. TIER 2. Wednesday ruled 16:49 the partition question: queue it — the diff is ONE new test file; the auth.ts:300 tamper exists only in the checker's clone. If KS-1207 (auth.ts :277-286, seat A local) merges before raise, re-run the cell at the new tip (tamper line moves to :304). The cell reads req.user.rateLimitBucket, not Redis keys: a tamper inside rateLimitEnforce.ts would not red it (stated in the brief).

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1205-api-gateway-per-key-limiter-follow.test.ts
@@ -0,0 +1,77 @@
+/**
+ * KS-1205 F-3 G-BUCKET-HASH: the per-key limiter counts an API key under
+ * api_key plus a DOMAINED sha256 of the key. Nothing pinned the domain, so a
+ * bucket built from the bare sha256 of the key, the same value the security
+ * service stores as key_hash, left the whole suite green. These cells read the
+ * bucket the real authenticateToken puts on req.user for two keys.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import express from 'express';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import { createHash } from 'crypto';
+import { configureAuth, authenticateToken } from '../middleware/auth';
+
+const EXPECTED_CELLS = 2;
+let CELLS_RUN = 0;
+const KEY_A = 'sk_ks1205_bucket_a_0001';
+const KEY_B = 'sk_ks1205_bucket_b_0002';
+const realFetch = globalThis.fetch;
+
+let bare: Server;
+let bareUrl = '';
+
+beforeAll(async () => {
+  configureAuth({ securityServiceUrl: 'http://127.0.0.1:9', authServiceUrl: 'http://127.0.0.1:9' });
+  globalThis.fetch = (async (url: string) => {
+    if (String(url).endsWith('/api/keys/validate')) {
+      return { ok: true, status: 200, json: async () => ({ data: { valid: true, tenantId: 't-ks1205', rateLimit: 50, rateLimitWindow: 60 } }) };
+    }
+    return { ok: false, status: 503, json: async () => ({}) };
+  }) as never;
+  vi.spyOn(console, 'error').mockImplementation(() => undefined);
+  const app = express();
+  app.get('/bucket', authenticateToken(true), (req, res) => {
+    res.status(200).json({ bucket: (req as any).user.rateLimitBucket });
+  });
+  bare = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => bare.once('listening', () => r()));
+  bareUrl = 'http://127.0.0.1:' + (bare.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  vi.restoreAllMocks();
+  await new Promise<void>((r) => bare.close(() => r()));
+});
+
+// the http status and the bucket the real middleware assigned to one key
+async function bucketFor(key: string): Promise<string> {
+  const r = await realFetch(bareUrl + '/bucket', { headers: { 'x-api-key': key } });
+  const body: any = await r.json();
+  return String(r.status) + ' ' + body.bucket;
+}
+
+// the bare sha256 of a key, the form the security service stores as key_hash
+function bareHash(key: string): string {
+  return createHash('sha256').update(key).digest('hex');
+}
+
+describe('KS-1205 G-BUCKET-HASH - a key bucket is never the stored key_hash', () => {
+  it('KS-1205 R1 - neither key is bucketed as api_key plus the bare sha256 of the key', async () => {
+    CELLS_RUN += 1;
+    const a = await bucketFor(KEY_A);
+    const b = await bucketFor(KEY_B);
+    expect(a).not.toBe('200 api_key:' + bareHash(KEY_A));
+    expect(b).not.toBe('200 api_key:' + bareHash(KEY_B));
+  });
+  it('KS-1205 CONTROL - each key gets its own api_key bucket of 64 hex that never carries the key', async () => {
+    CELLS_RUN += 1;
+    const a = await bucketFor(KEY_A);
+    const b = await bucketFor(KEY_B);
+    expect([a.startsWith('200 api_key:'), a.length, b.length, a === b, a.includes(KEY_A), b.includes(KEY_B)]).toEqual([true, 76, 76, false, false, false]);
+  });
+  it('KS-1205 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});```
