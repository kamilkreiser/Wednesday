```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts
@@ -92,7 +92,7 @@
 
   it('control KS-1374 B2: request 2001 in the same window is refused with 429 RATE_LIMIT_EXCEEDED', async () => {
     const r = await fetch(base + '/api/v1/documents');
-    const body = await r.json();
+    const body = (await r.json()) as { error: { code: string } };
     expect(r.status).toBe(429);
     expect(body.error.code).toBe('RATE_LIMIT_EXCEEDED');
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks695-ask3-erase-connector-door.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks695-ask3-erase-connector-door.test.ts
@@ -122,7 +122,7 @@
   it('🔴 GRACE (switch unset) - a role-only connector is admitted and logged, so Platform S\'s existing key keeps working', async () => {
     expect(await drive(ROLE_ONLY, 'POST', POST_PATH)).toBe(200);
     expect(received).toHaveLength(1);
-    const graceLogs = warn.mock.calls.filter((c) => String(c[0]).includes('KS-843'));
+    const graceLogs = warn.mock.calls.filter((c: unknown[]) => String(c[0]).includes('KS-843'));
     expect(graceLogs).toHaveLength(1);
     expect(graceLogs[0][1]).toMatchObject({ requiredScope: 'subjects:erase', method: 'POST', route: POST_PATH, enforceFlag: FLAG });
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1464-limiter-key-hygiene.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1464-limiter-key-hygiene.test.ts
@@ -57,7 +57,7 @@
 }
 
 let warn: ReturnType<typeof vi.spyOn>;
-const noAllowanceLines = (): string[] => warn.mock.calls.map((c) => String(c[0])).filter((l) => l.includes('has no rateLimit'));
+const noAllowanceLines = (): string[] => warn.mock.calls.map((c: unknown[]) => String(c[0])).filter((l) => l.includes('has no rateLimit'));
 beforeAll(() => { warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined); });
 afterAll(() => { warn.mockRestore(); vi.restoreAllMocks(); });
 
```
