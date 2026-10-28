# READY — KS-1780-KS-1780-ks_1780_p2_admin (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
36	15	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
124	0	Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (34 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 36 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 15.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 34 line(s) byte-exact incl. leading whitespace (of 34; 36 line(s) added by the apply)` [a3i_indent.out: `OK 34 line(s) byte-exact incl. leading whitespace (of 34; 36 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=16, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts fails at the untouched tip (9 failed / 21 run; controls green; assertion reds)` [red_first.json: failed=9 of total=21; red cell(s): ['KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A1 GET /settings: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A1 GET /document-types: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A1 GET /workflows: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A1 GET /organizations: a revoked Proxy thrown by the query is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A2 GET /settings: an object whose message getter throws is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A2 GET /document-types: an object whose message getter throws is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A2 GET /workflows: an object whose message getter throws is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 A2 GET /organizations: an object whose message getter throws is answered with the constant 500', 'KS-1780: adminConfig catches answer a hostile thrown value RED KS-1780 S1: no catch condition in adminConfig.ts reads err?.message or err?.code directly']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts passes with the product hunk (21 passed / 21 run)` [green_after.json: failed=0 of total=21, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1690 failed=0 | after: total=1711 failed=0` · `NEW reds: []` [baseline_suite.json total=1690 failed=0; after_suite.json total=1711 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +160/-15 test=src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+36/-15 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (+124/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -128,3 +128,24 @@
+/**
+ * KS-1780: a catch that tests `err?.message?.includes(...)` or `err?.code` BEFORE it reaches fail500 reads the thrown value itself. A revoked Proxy, or an object whose `message` getter throws,
+ * makes THAT read throw from inside the catch, so the handler's promise rejects and the request gets no response at all (the KS-1772 shape, one step earlier). These two readers answer false
+ * when the value cannot be inspected: such a value is not a "table missing" or "unique constraint" error, so it falls through to fail500 and gets the constant 500.
+ */
+function errorMessageIncludes(err: any, needle: string): boolean {
+  try {
+    return err?.message?.includes(needle) === true;
+  } catch {
+    return false;
+  }
+}
+
+function isMissingTableError(err: any): boolean {
+  try {
+    return err?.message?.includes('does not exist') === true || err?.code === '42P01';
+  } catch {
+    return false;
+  }
+}
+
 adminConfigRouter.post('/refresh-tenants', async (_req: Request, res: Response) => {
   try {
     await refreshTenantConfigs();
@@ -188,7 +209,7 @@
     res.json({ success: true, documentTypes: rows.map(mapDocTypeRow) });
   } catch (err: any) {
     // Table may not exist yet — return empty list so frontend uses its defaults
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, documentTypes: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/document-types)', err);
@@ -224,7 +245,7 @@
     `;
     res.status(201).json({ success: true, documentType: mapDocTypeRow(rows[0]) });
   } catch (err: any) {
-    if (err?.message?.includes('unique constraint')) {
+    if (errorMessageIncludes(err, 'unique constraint')) {
       return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } });
     }
     fail500(res, 'Admin config request failed (POST /api/admin/document-types)', err);
@@ -288,7 +309,7 @@
     res.json({ success: true, workflows: rows.map(mapWorkflowRow) });
   } catch (err: any) {
     // Table may not exist yet — return empty list so frontend uses its defaults
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, workflows: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/workflows)', err);
@@ -376,7 +397,7 @@
     `;
     res.json({ success: true, items: rows.map(mapQueueRow) });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, items: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/verification-queue)', err);
@@ -431,7 +452,7 @@
     `;
     res.json({ success: true, integrations: rows.map(mapIntegrationRow) });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, integrations: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/integrations)', err);
@@ -520,6 +541,6 @@
     res.json({ success: true, settings });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, settings: {} });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/settings)', err);
@@ -700,7 +721,7 @@
       total: rows.length,
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, policies: [], total: 0 });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/verification-policies)', err);
@@ -816,7 +837,7 @@
       total: rows.length,
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, organizations: [], total: 0 });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/organizations)', err);
@@ -931,7 +952,7 @@
       })),
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, keys: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/api-keys)', err);
@@ -1224,7 +1245,7 @@
       total: countResult[0]?.total ?? rows.length,
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, logs: [], events: [], total: 0 });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/audit-logs)', err);
@@ -1387,7 +1408,7 @@
       total: rows.length,
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, rightsHolders: [], total: 0 });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/rights-holders)', err);
@@ -1565,7 +1586,7 @@
       })),
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist')) {
+    if (errorMessageIncludes(err, 'does not exist')) {
       return res.json({ success: true, documents: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/rights-holders/:id/documents)', err);
@@ -1656,7 +1677,7 @@
       },
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, data: { users: [], total: 0 } });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/users)', err);
@@ -1693,7 +1714,7 @@
       })),
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, users: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/identity/users)', err);
@@ -1721,7 +1742,7 @@
       })),
     });
   } catch (err: any) {
-    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
+    if (isMissingTableError(err)) {
       return res.json({ success: true, organizations: [] });
     }
     fail500(res, 'Admin config request failed (GET /api/admin/identity/organizations)', err);
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
@@ -0,0 +1,124 @@
+// KS-1780 (originate routes/adminConfig.ts): fifteen catch blocks tested `err?.message?.includes(...)` and/or `err?.code` BEFORE they reached fail500. That read touches the thrown value
+// itself, so a revoked Proxy, or an object whose `message` getter throws, made the read throw inside the catch: the handler's promise rejected and the request got NO answer. fail500
+// already survives such a value (KS-1772); this file pins that the catches' own reads do too. Four GET routes are driven over a real loopback listener by making their prisma.$queryRaw
+// reject, as the KS-1346 part C cells do; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+// S1 pins the source: no `if (err?.message` / `if (err?.code` condition may remain in the file.
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: jest.fn() },
+  refreshTenantConfigs: jest.fn(),
+  withTenant: (_t: unknown, fn: () => unknown) => fn(),
+  getTenantManager: () => null,
+}));
+
+jest.mock('../middleware/auth', () => {
+  const actual = jest.requireActual('../middleware/auth');
+  return {
+    ...actual,
+    authenticate: () => (req: any, _res: unknown, next: () => void) => {
+      const principal = { id: 'u-ks1780', role: 'SYSTEM_ADMIN', tenantId: 't-ks1780' };
+      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
+      next();
+    },
+    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  };
+});
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
+    runWithPlatformScope: (fn: () => unknown) => fn(),
+    queryWithTenantGuc: jest.fn(),
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import { readFileSync } from 'fs';
+import { join } from 'path';
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { adminConfigRouter } from '../routes/adminConfig';
+
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+const ROUTES = [
+  { label: 'GET /settings', path: '/settings', empty: { success: true, settings: {} } },
+  { label: 'GET /document-types', path: '/document-types', empty: { success: true, documentTypes: [] } },
+  { label: 'GET /workflows', path: '/workflows', empty: { success: true, workflows: [] } },
+  { label: 'GET /organizations', path: '/organizations', empty: { success: true, organizations: [], total: 0 } },
+] as const;
+
+const app = express();
+app.use('/api/admin', express.json(), adminConfigRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  (server as unknown as { closeAllConnections?: () => void })?.closeAllConnections?.();
+  server?.close();
+});
+beforeEach(() => mockQueryRaw.mockReset());
+
+async function callWithThrow(path: string, thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockQueryRaw.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/admin' + path, { signal: AbortSignal.timeout(1500) });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageGetter(): object {
+  return {
+    get message(): string {
+      throw new Error('ks1780 getter');
+    },
+  };
+}
+
+describe('KS-1780: adminConfig catches answer a hostile thrown value', () => {
+  it.each(ROUTES)('RED KS-1780 A1 $label: a revoked Proxy thrown by the query is answered with the constant 500', async (route) => {
+    expect(await callWithThrow(route.path, revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it.each(ROUTES)('RED KS-1780 A2 $label: an object whose message getter throws is answered with the constant 500', async (route) => {
+    expect(await callWithThrow(route.path, throwingMessageGetter())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it.each(ROUTES)('control KS-1780 C1 $label: an Error saying "does not exist" is still answered with the empty list', async (route) => {
+    expect(await callWithThrow(route.path, new Error('relation "x" does not exist'))).toEqual({ status: 200, body: route.empty });
+  });
+
+  it.each(ROUTES)('control KS-1780 C2 $label: a thrown object with code 42P01 is still answered with the empty list', async (route) => {
+    expect(await callWithThrow(route.path, { code: '42P01' })).toEqual({ status: 200, body: route.empty });
+  });
+
+  it.each(ROUTES)('control KS-1780 C3 $label: an ordinary Error is still answered with the constant 500', async (route) => {
+    expect(await callWithThrow(route.path, new Error('ks1780 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('RED KS-1780 S1: no catch condition in adminConfig.ts reads err?.message or err?.code directly', () => {
+    const source = readFileSync(join(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');
+    const direct = source.split('\n').filter((line) => /^\s*if \(err\?\.(message|code)/.test(line));
+    expect(direct).toEqual([]);
+  });
+});
```

## SOURCE-READ NOTE (Spark operator for Wednesday, 2026-10-28 PM) - HOLD
- Counted the replaced conditions in the patch: 15 (13 x `isMissingTableError` incl. the `'does not exist'`-only variant handled by `errorMessageIncludes` at rights-holders/:id/documents, 1 x `errorMessageIncludes(err,'unique constraint')`); the 2 helpers use `=== true`, so a non-boolean truthy `includes` result (not possible for string/array message) would read false. Cell S1 pins that no `err?.message`/`err?.code` read remains in a catch condition.
- SAME FILE as held `ks_1779_p1` (adminConfig.ts :2181/:2221 vs this patch :128-:1725): different hunks, but raise them in sequence (one rebases onto the other). Refs KS-1780 only: the systemErrors.ts (p1) and webhooks.ts/pgErrors.ts (p3) sites are the other two held READYs; the ticket lists 17 catches in total.
