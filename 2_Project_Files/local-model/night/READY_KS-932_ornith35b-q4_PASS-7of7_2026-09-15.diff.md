# READY — KS-932 — Ornith ornith:35b (Q4_K_M) PASS 7/7 on the first run, 2026-09-15 (q4 set of Kam's ten-ticket test) — tip develop M55 48e65c435
# Source read by Wednesday 11:41: the product hunk is byte-for-byte the brief's edits; the three cells are the brief's (2 red at the tip / control green; green after; suite delta 0; tsc rc 0).
# Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks932-ornith35b-night (checker.out = the verdict). HELD for a Secuura seat to raise as a PR under the normal gate — Wednesday holds no client identity.

```diff
--- a/packages/shared/src/security/ssrf-guard.ts
+++ b/packages/shared/src/security/ssrf-guard.ts
@@ -471,7 +471,19 @@ export async function safeOutboundRequest(
 
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
 
   const address = resolved.addresses[0];
@@ -481,7 +493,7 @@ export async function safeOutboundRequest(
     ? new https.Agent({ lookup: pinnedLookup(address) as any })
     : new http.Agent({ lookup: pinnedLookup(address) as any });
 
-  const timeoutMs = init.timeoutMs ?? 10_000;
+  const remainingMs = Math.max(1, timeoutMs - (Date.now() - startedAt));
 
   return new Promise((resolve) => {
     let settled = false;
@@ -564,7 +576,7 @@ export async function safeOutboundRequest(
         error: `request exceeded its ${timeoutMs}ms deadline (connect, transfer and drain)`,
       });
-    }, timeoutMs);
+    }, remainingMs);
 
     req.on('error', (err) => done({ ok: false, reason: 'request_failed', error: err.message }));
--- /dev/null
+++ b/packages/shared/src/__tests__/ks932-timeout-bounds-dns.test.ts
@@ -0,0 +1,107 @@
+/**
+ * KS-932 — verify that `timeoutMs` bounds DNS resolution end-to-end.
+ */
+
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+vi.mock('dns/promises', () => ({
+  lookup: vi.fn(),
+}));
+
+const { safeOutboundRequest } = await import('../security/ssrf-guard');
+const { lookup } = await import('dns/promises') as typeof import('dns/promises');
+
+function settledWithin<T>(promise: Promise<T>, ms: number): Promise<[true, T] | [false, undefined]> {
+  return new Promise((resolve) => {
+    const timer = setTimeout(() => resolve([false, undefined]), ms);
+    promise.then(
+      (v) => { clearTimeout(timer); resolve([true, v]); },
+      (e) => { clearTimeout(timer); resolve([true, e]); },
+    );
+  });
+}
+
+describe('KS-932 — timeoutMs bounds DNS resolution', () => {
+  beforeEach(() => {
+    vi.clearAllTimers();
+  });
+
+  it('🔴 KS-932 — a lookup that never calls back: the call settles within the declared bound', async () => {
+    (lookup as unknown as ReturnType<typeof vi.fn>).mockImplementation(() => new Promise(() => {}));
+
+    const resultPromise = safeOutboundRequest('https://hang.example/', { timeoutMs: 300 });
+    const [settledFirst, valueOrErr] = await settledWithin(resultPromise, 1500);
+
+    expect(settledFirst).toBe(true);
+    if (!valueOrErr || !(valueOrErr instanceof Error)) {
+      expect(valueOrErr).toBeDefined();
+      expect((valueOrErr as any).ok).toBe(false);
+      expect((valueOrErr as any).reason).toBe('blocked');
+      expect(String((valueOrErr as any).error)).toMatch(/300ms/);
+    } else {
+      throw new Error('expected SafeOutboundResult, got error');
+    }
+  });
+
+  it('🔴 KS-932 — the budget is shared: a slow lookup leaves less for the request', async () => {
+    (lookup as unknown as ReturnType<typeof vi.fn>).mockImplementationOnce((_host: string) =>
+      new Promise<{ address: string; family: number }>((resolve) => {
+        setTimeout(() => resolve([{ address: '203.0.113.7', family: 4 }]), 200);
+      }),
+    );
+
+    const started = Date.now();
+    const result = await safeOutboundRequest('https://slow.example/', { timeoutMs: 400 });
+    const elapsed = Date.now() - started;
+
+    expect(elapsed).toBeLessThan(550);
+    expect(result.ok).toBe(false);
+    if (!result.ok) {
+      expect(result.reason).toBe('request_failed');
+    }
+  }, 10_000);
+
+  it('KS-932 control — a lookup that answers promptly still reaches the request and the deadline', async () => {
+    (lookup as unknown as ReturnType<typeof vi.fn>).mockResolvedValue([{ address: '203.0.113.7', family: 4 }] as never);
+
+    const result = await safeOutboundRequest('https://fast.example/', { timeoutMs: 300 });
+
+    expect(result.ok).toBe(false);
+    if (!result.ok) {
+      expect(result.reason).toBe('request_failed');
+      expect(result.error).toMatch(/deadline/);
+    }
+  }, 10_000);
+});
```
