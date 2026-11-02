# READY — KS-1868-KS-1868-O80-G4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 18:38 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 18:38 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c234c2388a162385eae32b9d5dc31de781f13908`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
186	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: admin.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts 186 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=9 of total=12; red cell(s): ["KS-1868 admin 'POST integration test' catch coerces a non-string message safely RED ks1868 R1 POST integration test: a message that is a revoked Proxy is answered with a constant reason", "KS-1868 admin 'POST integration test' catch coerces a non-string message safely RED ks1868 R2 POST integration test: a message whose toString throws is answered with a constant reason", "KS-1868 admin 'POST integration test' catch coerces a non-string message safely RED ks1868 R3 POST integration test: a null-prototype message is answered with a constant reason", "KS-1868 admin 'PATCH user forward' catch coerces a non-string message safely RED ks1868 R1 PATCH user forward: a message that is a revoked Proxy is answered with a constant reason", "KS-1868 admin 'PATCH user forward' catch coerces a non-string message safely RED ks1868 R2 PATCH user forward: a message whose toString throws is answered with a constant reason", "KS-1868 admin 'PATCH user forward' catch coerces a non-string message safely RED ks1868 R3 PATCH user forward: a null-prototype message is answered with a constant reason", "KS-1868 admin 'GET audit export' catch coerces a non-string message safely RED ks1868 R1 GET audit export: a message that is a revoked Proxy is answered with a constant reason", "KS-1868 admin 'GET audit export' catch coerces a non-string message safely RED ks1868 R2 GET audit export: a message whose toString throws is answered with a constant reason", "KS-1868 admin 'GET audit export' catch coerces a non-string message safely RED ks1868 R3 GET audit export: a null-prototype message is answered with a constant reason"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=0 | after: total=1424 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=0; after_suite.json total=1424 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts` (+186/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c234c2388a162385eae32b9d5dc31de781f13908` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g4_apigateway_admin_integration_forward_export_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1017,7 +1017,7 @@
         } catch (err: any) {
           let reason: string;
           try {
-            reason = err.message;
+            reason = String(err.message);
           } catch {
             reason = 'unreadable thrown value';
           }
@@ -1524,7 +1524,7 @@
     } catch (err: any) {
       let reason: string;
       try {
-        reason = err.message;
+        reason = String(err.message);
       } catch {
         reason = 'unreadable thrown value';
       }
@@ -1643,7 +1643,7 @@
     } catch (err) {
       let reason: string;
       try {
-        reason = (err as Error).message;
+        reason = String((err as Error).message);
       } catch {
         reason = 'unreadable thrown value';
       }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-forward-export-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,186 @@
+/**
+ * KS-1868 (QA gate 110, G110-F1): three catches in routes/admin.ts (the Blockfrost connectivity test, the user-update forward and the
+ * audit-log export) read the thrown value's `message` inside a guard but never coerce it. When the `message` getter SUCCEEDS and returns a
+ * hostile NON-string (a revoked Proxy, an object whose `toString` throws, a null-prototype object), the hostile value is used in a template
+ * string, passed to `res.json` or passed to the logger OUTSIDE the guard, and the request is not answered with the constant reason. Each read
+ * is now wrapped in `String(...)` inside the same guard.
+ *
+ * The handler under test is the LAST function of the route, taken from the route table and called directly with a fake request and
+ * response. The stand-ins (`query`, the global `fetch`) are plain functions that reject with the thrown value (a vi.fn() could inspect a
+ * revoked Proxy before the code under test does). Only strings are compared, never a hostile value itself.
+ */
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+import type { Router } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+type Logged = { level: string; message: string; meta: { error?: unknown } | undefined };
+type ResX = { statusCode: number; body: unknown; status(c: number): ResX; json(b: unknown): ResX };
+
+const ks = {
+  thrown: undefined as { value: unknown } | undefined,
+  logs: [] as Logged[],
+};
+
+function mkRes(): ResX {
+  const r: ResX = {
+    statusCode: 200,
+    body: undefined,
+    status(c) {
+      r.statusCode = c;
+      return r;
+    },
+    json(b) {
+      r.body = b;
+      return r;
+    },
+  };
+  return r;
+}
+
+function buildRouter(): Router {
+  return createAdminRoutes({
+    authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+    query: () => (ks.thrown ? Promise.reject(ks.thrown.value) : Promise.resolve({ rows: [], rowCount: 0 })),
+    isDbAvailable: () => true,
+    redisService: {
+      getIntegration: () =>
+        Promise.resolve({ id: 'int-1', integrationType: 'blockchain', provider: 'blockfrost', config: { projectId: 'proj', network: 'preprod' } }),
+      setIntegration: () => Promise.resolve(undefined),
+    },
+    services: { auth: { url: 'http://auth.invalid' } },
+    log: (level: string, message: string, meta?: { error?: unknown }) => {
+      ks.logs.push({ level, message, meta });
+    },
+  } as unknown as AdminRouteDeps);
+}
+
+function handlerFor(rt: Router, method: string, path: string): (req: unknown, res: unknown) => Promise<void> {
+  const layers = (rt as unknown as { stack: Array<{ route?: { path: string; methods: Record<string, boolean>; stack: Array<{ handle: (req: unknown, res: unknown) => Promise<void> }> } }> }).stack;
+  const layer = layers.find((l) => l.route && l.route.path === path && l.route.methods[method]);
+  if (!layer || !layer.route) throw new Error('route not found: ' + method + ' ' + path);
+  const stack = layer.route.stack;
+  return stack[stack.length - 1].handle;
+}
+
+/** Run a route handler. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(method: string, path: string): Promise<ResX> {
+  const res = mkRes();
+  const req = {
+    params: { id: 'int-1' },
+    body: { role: 'USER' },
+    query: {},
+    headers: { authorization: 'Bearer ks1868' },
+    user: { userId: 'admin-72', role: 'SYSTEM_ADMIN', email: 'admin-72@test.io', verificationLevel: 'HIGH' },
+  };
+  await handlerFor(buildRouter(), method, path)(req, res).catch(() => undefined);
+  return res;
+}
+
+function revoked(): unknown {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+// An Error whose `message` getter succeeds but returns the given value.
+function withMessage(value: () => unknown): unknown {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        return value();
+      },
+    },
+  });
+}
+
+const toStringThrows = () => ({
+  toString() {
+    throw new Error('toString boom');
+  },
+});
+
+const plain = (v: unknown): unknown => (typeof v === 'string' ? v : '<non-string>');
+
+const fetchRejects = () => vi.stubGlobal('fetch', () => Promise.reject(ks.thrown?.value));
+
+type CaseX = { name: string; method: string; path: string; setup: () => void; read: (res: ResX) => unknown; expected: (reason: string) => unknown; httpCode: number };
+
+const bodyOf = (res: ResX) => (res.body ?? {}) as { message?: unknown; error?: { details?: { details?: unknown } } };
+
+const CASES: CaseX[] = [
+  {
+    name: 'POST integration test',
+    method: 'post',
+    path: '/api/admin/integrations/:id/test',
+    setup: fetchRejects,
+    read: (res) => plain(bodyOf(res).message),
+    expected: (reason) => `Network error: ${reason}`,
+    httpCode: 200,
+  },
+  {
+    name: 'PATCH user forward',
+    method: 'patch',
+    path: '/api/users/admin/:id',
+    setup: fetchRejects,
+    read: (res) => plain(bodyOf(res).error?.details?.details),
+    expected: (reason) => reason,
+    httpCode: 502,
+  },
+  {
+    name: 'GET audit export',
+    method: 'get',
+    path: '/api/security/audit/export',
+    setup: () => undefined,
+    read: () => {
+      const l = ks.logs.find((x) => x.message === '[AuditExport] Failed');
+      return l ? plain(l.meta?.error) : '<no log line>';
+    },
+    expected: (reason) => reason,
+    httpCode: 500,
+  },
+];
+
+const status = (c: CaseX) => c.httpCode;
+
+beforeEach(() => {
+  ks.thrown = undefined;
+  ks.logs.length = 0;
+});
+
+afterEach(() => {
+  vi.unstubAllGlobals();
+});
+
+describe.each(CASES)('KS-1868 admin $name catch coerces a non-string message safely', (c) => {
+  it(`RED ks1868 R1 ${c.name}: a message that is a revoked Proxy is answered with a constant reason`, async () => {
+    ks.thrown = { value: withMessage(revoked) };
+    c.setup();
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(status(c));
+    expect(c.read(res)).toBe(c.expected('unreadable thrown value'));
+  });
+
+  it(`RED ks1868 R2 ${c.name}: a message whose toString throws is answered with a constant reason`, async () => {
+    ks.thrown = { value: withMessage(toStringThrows) };
+    c.setup();
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(status(c));
+    expect(c.read(res)).toBe(c.expected('unreadable thrown value'));
+  });
+
+  it(`RED ks1868 R3 ${c.name}: a null-prototype message is answered with a constant reason`, async () => {
+    ks.thrown = { value: withMessage(() => Object.create(null)) };
+    c.setup();
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(status(c));
+    expect(c.read(res)).toBe(c.expected('unreadable thrown value'));
+  });
+
+  it(`control ks1868 C1 ${c.name}: an ordinary Error is answered with its own message, as before`, async () => {
+    ks.thrown = { value: new Error('boom 10.0.0.7') };
+    c.setup();
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(status(c));
+    expect(c.read(res)).toBe(c.expected('boom 10.0.0.7'));
+  });
+});
```
