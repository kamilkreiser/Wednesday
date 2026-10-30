# READY (hand-written note: hold_ready.py REFUSES this run - it needs its own checker dir; graded by the operator's tsc + vitest checker) - O32-P1 (KS-1864, api-gateway test-file type fixes, group A: 3 files, 4 of 27 tsc errors)

Spark operator 32, 2026-10-30 AEDT. TEST-ONLY, type-level only. **A PASS is a candidate, never a merge.** Closes 4 of the 27 KS-1864 errors (ks1374 1, ks695-ask3-erase-connector-door 1, ks1464 2); refs KS-1864, does NOT close it.

- What: three one-line type fixes in api-gateway src/__tests__: ks1374 `const body = (await r.json()) as { error: { code: string } };`; ks695 `(c: unknown[])` on the warn.mock.calls filter callback; ks1464 `(c: unknown[])` and `(l: string)` on the noAllowanceLines callbacks. No product file; no assertion changed.
- Tip: develop a8c554659cb34c4406d0274daa5fed4aafec35ec (ls-remote 2026-10-30 16:3x; clone toplevel asserted before any fetch).
- Overlap: no OPEN PR (26 PRs, 135 file rows via GitHub API) touches any of the 7 KS-1864 files; planted control (api-gateway ks1240b test file, PR 1827; package.json, PRs 649/575) hit. Held READY elsewhere in night/ mention ks1374 and ks1165 files (older, already at the tip).
- Result: PASS on the ORIGINAL brief, first model round (no rebrief). Checker: patch applies strictly (git apply); tsc with types ["node"] AND types unset: api-gateway test-file errors 27 -> 23 exactly (the three files go to 0, every other file unchanged, no product-file error); vitest per file before/after identical (ks1374 7/7, ks695 6/6, ks1464 12/12). Added/removed lines equal the golden's (context width 2 vs golden's 3 only). Positive control (golden through the same checker) PASS; negative control (one annotation dropped) FAIL as it should.
- Not tested: eslint; other packages' tsconfigs; the production build (it excludes tests); CI's own type-check config (none known to include tests - that is the point of KS-1864).
- Brief: 2_Project_Files/local-model/night/briefs/ks_1864_a/KS-1864.md (+golden.diff)  Run dir: 0_Brain/reference/2026-10-30_spark-operator32/runs/a_r1 (checker tools in .../tools/run.py).

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts
@@ -92,5 +92,5 @@
   it('control KS-1374 B2: request 2001 in the same window is refused with 429 RATE_LIMIT_EXCEEDED', async () => {
     const r = await fetch(base + '/api/v1/documents');
-    const body = await r.json();
+    const body = (await r.json()) as { error: { code: string } };
     expect(r.status).toBe(429);
     expect(body.error.code).toBe('RATE_LIMIT_EXCEEDED');
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks695-ask3-erase-connector-door.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks695-ask3-erase-connector-door.test.ts
@@ -122,5 +122,5 @@
     expect(await drive(ROLE_ONLY, 'POST', POST_PATH)).toBe(200);
     expect(received).toHaveLength(1);
-    const graceLogs = warn.mock.calls.filter((c) => String(c[0]).includes('KS-843'));
+    const graceLogs = warn.mock.calls.filter((c: unknown[]) => String(c[0]).includes('KS-843'));
     expect(graceLogs).toHaveLength(1);
     expect(graceLogs[0][1]).toMatchObject({ requiredScope: 'subjects:erase', method: 'POST', route: POST_PATH, enforceFlag: FLAG });
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1464-limiter-key-hygiene.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1464-limiter-key-hygiene.test.ts
@@ -58,3 +58,3 @@
 let warn: ReturnType<typeof vi.spyOn>;
-const noAllowanceLines = (): string[] => warn.mock.calls.map((c) => String(c[0])).filter((l) => l.includes('has no rateLimit'));
+const noAllowanceLines = (): string[] => warn.mock.calls.map((c: unknown[]) => String(c[0])).filter((l: string) => l.includes('has no rateLimit'));
 beforeAll(() => { warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined); });
```
