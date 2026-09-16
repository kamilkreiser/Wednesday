# READY — KS-1179 F-2 + F-3 (TEST-ONLY, MODIFY-IN-PLACE ks932-timeout-bounds-dns.test.ts: a never-answering https.request mock so the deadline cells stop depending on 203.0.113.7 hanging; cell 2 bounded below + one transport call + the deadline text; the line-48 type argument fixed) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (01:38). Held by Wednesday at 03:04 AEST (the 01:42–03:03 API outage delayed the hold, not the run). Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1179-ornith35b-night2
# Source read by me (Wednesday): the model's 16 `+` and 1 `-` lines are IDENTICAL to the brief's four hunks (python line compare); one file, product untouched. A2 applied with ONE accommodation: FUZZY -C1 (one context line reduced at the first hunk) — the brief's own golden applied strictly, so the model's hunk context differs by a line; content lines identical. A4: 1 red by assertion at the tip under the gate's T2 (controls green); A6 whole packages/shared no NEW red; A7 tsc rc 0.
# NOT MEASURED BY ME: the checker's standalone tsc on the test file printed rc=2 (3 lines) without the error names; the brief's premise P10 predicts exactly TS1378 x2 (pre-existing top-level await) and no TS2345. The raising seat runs an INCLUDING tsc and confirms TS2345 is gone before calling F-3 fixed.
# PR NOTES: "Refs KS-1179 (F-2, F-3)" — never Closes (F-4/F-5/F-6 are product edits to ssrf-guard.ts). Can ship in ONE PR with READY_KS-1179-F1 (different files). Residual stated by the brief writer: cells 2–3 no longer traverse the real agent/TLS (covered by ks914-shipped-path cell 1 + the F-1 file's cell 5). packages/shared = the Secuura raise seat's partition.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks932-timeout-bounds-dns.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks932-timeout-bounds-dns.test.ts
@@ -9,4 +9,14 @@
   });
 
+// KS-1179 (KS-932 gate F-2): https.request is a request that never answers, so no cell opens a socket
+// and the deadline cells no longer depend on 203.0.113.7 hanging.
+const { silentTransport } = vi.hoisted(() => ({
+  silentTransport: vi.fn((_options: unknown, _onResponse: unknown) => ({ on: vi.fn(), write: vi.fn(), end: vi.fn(), destroy: vi.fn() })),
+}));
+vi.mock('https', async (importOriginal) => {
+  const actual = await importOriginal<typeof import('https')>();
+  return { ...actual, default: actual, request: silentTransport };
+});
+
 const { safeOutboundRequest } = await import('../security/ssrf-guard');
 const { lookup } = await import('dns/promises') as typeof import('dns/promises');
@@ -25,4 +35,5 @@
     vi.clearAllTimers();
+    silentTransport.mockClear();
   });
 
@@ -46,17 +57,20 @@
   it('🔴 KS-932 — the budget is shared: a slow lookup leaves less for the request', async () => {
     (lookup as unknown as ReturnType<typeof vi.fn>).mockImplementationOnce((_host: string) =>
-      new Promise<{ address: string; family: number }>((resolve) => {
+      new Promise<Array<{ address: string; family: number }>>((resolve) => {
         setTimeout(() => resolve([{ address: '203.0.113.7', family: 4 }]), 200);
       }),
     );
 
     const started = Date.now();
     const result = await safeOutboundRequest('https://slow.example/', { timeoutMs: 400 });
     const elapsed = Date.now() - started;
 
     expect(elapsed).toBeLessThan(550);
+    expect(elapsed).toBeGreaterThanOrEqual(380);
+    expect(silentTransport).toHaveBeenCalledTimes(1);
     expect(result.ok).toBe(false);
     if (!result.ok) {
       expect(result.reason).toBe('request_failed');
+      expect(result.error).toContain('request exceeded its 400ms deadline');
     }
   }, 10_000);
@@ -72,4 +86,5 @@
       expect(result.error).toMatch(/deadline/);
     }
+    expect(silentTransport).toHaveBeenCalledTimes(1);
   }, 10_000);
 });
```
