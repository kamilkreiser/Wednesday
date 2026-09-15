```diff
--- a/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
+++ b/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
@@ -471,7 +471,17 @@ export async function safeOutboundRequest(
 
   const url = new URL(literal.url);
-  const resolved = await resolvePublicAddresses(url.hostname);
+  const timeoutMs = init.timeoutMs ?? 10_000;
+  const startedAt = Date.now();
+  let dnsTimer: ReturnType<typeof setTimeout> | undefined;
+  const resolved = await Promise.race([
+    resolvePublicAddresses(url.hostname),
+    new Promise<{ ok: false; error: string }>((settle) => {
+      dnsTimer = setTimeout(() => settle({ ok: false, error: `host "${url.hostname}" did not resolve within the ${timeoutMs}ms deadline` }), timeoutMs);
+    }),
+  ]);
+  if (dnsTimer) clearTimeout(dnsTimer);
   if (!resolved.ok) return { ok: false, reason: 'blocked', error: resolved.error };
 
@@ -481,7 +491,7 @@ export async function safeOutboundRequest(
     : new http.Agent({ lookup: pinnedLookup(address) as any });
 
-  const timeoutMs = init.timeoutMs ?? 10_000;
+  const remainingMs = Math.max(1, timeoutMs - (Date.now() - startedAt));
 
   return new Promise((resolve) => {
 
@@ -564,7 +574,7 @@ export async function safeOutboundRequest(
         error: `request exceeded its ${timeoutMs}ms deadline (connect, transfer and drain)`,
       });
-    }, timeoutMs);
+    }, remainingMs);
 
     req.on('error', (err) => done({ ok: false, reason: 'request_failed', error: err.message }));
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks932-timeoutms-does-not-bound-dns-resolution.test.ts
@@ -0,0 +1,105 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+const SEED_USER_ID = 'seed-user-for-test';
+
+vi.mock('dns/promises', () => ({
+  lookup: vi.fn(),
+}));
+
+const { safeOutboundRequest } = await import('../security/ssrf-guard');
+
+function settledWithin<T>(promise: Promise<T>, ms: number): Promise<[true, T] | [false, null]> {
+  return new Promise((resolve) => {
+    let timer: ReturnType<typeof setTimeout>;
+    promise.then((value) => {
+      clearTimeout(timer);
+      resolve([true, value]);
+    }).catch((err) => {
+      clearTimeout(timer);
+      resolve([false, err]);
+    });
+    timer = setTimeout(() => resolve([null, null]), ms);
+  });
+}
+
+describe('KS-932 — DNS resolution must be bounded by the declared timeoutMs', () => {
+  beforeEach(() => {
+    vi.clearAllTimers();
+  });
+
+  it('🔴 KS-932 — a lookup that never calls back: the call settles within the declared bound', async () => {
+    // <KS-932>: hang forever so only the budget can end the operation.
+    vi.mocked(await import('dns/promises').then(m => m)).lookup.mockImplementation(() => new Promise(() => {}));
+
+    const started = Date.now();
+    const resultPromise = safeOutboundRequest('https://hang.example/', { timeoutMs: 300 });
+    const [settled, result] = await settledWithin(resultPromise, 1500);
+    const elapsed = Date.now() - started;
+
+    expect(settled).toBe(true);
+    if (!result || !result.ok) {
+      expect(result?.reason).toBe('blocked');
+      expect(result?.error).toMatch(/300ms/);
+    }
+    expect(elapsed).toBeLessThan(1500);
+  }, 5_000);
+
+  it('🔴 KS-932 — the budget is shared: a slow lookup leaves less for the request', async () => {
+    // <KS-932>: resolves after ~200 ms to an unroutable address (TEST-NET-3),
+    // then the remaining budget (~200 ms of the 400 ms total) bounds the connect attempt.
+    vi.mocked(await import('dns/promises').then(m => m)).lookup.mockImplementationOnce((_host: string) =>
+      new Promise<{ address: string; family: number }>((resolve) => {
+        setTimeout(() => resolve([{ address: '203.0.113.7', family: 4 }]), 200);
+      }),
+    );
+
+    const started = Date.now();
+    const result = await safeOutboundRequest('https://slow.example/', { timeoutMs: 400 });
+    const elapsed = Date.now() - started;
+
+    expect(result.ok).toBe(false);
+    if (!result.ok) {
+      expect(result.reason).toBe('request_failed');
+    }
+    expect(elapsed).toBeLessThan(550);
+  }, 5_000);
+
+  it('KS-932 control — a lookup that answers promptly still reaches the request and the deadline', async () => {
+    // <KS-932-control>: prompt resolution + unroutable destination → `request_failed` mentioning `deadline`.
+    vi.mocked(await import('dns/promises').then(m => m)).lookup.mockResolvedValueOnce([
+      { address: '203.0.113.7', family: 4 },
+    ]);
+
+    const result = await safeOutboundRequest('https://fast.example/', { timeoutMs: 300 });
+
+    expect(result.ok).toBe(false);
+    if (!result.ok) {
+      expect(result.reason).toBe('request_failed');
+      expect(result.error).toMatch(/deadline/);
+    }
+  }, 5_000);
+});
```
