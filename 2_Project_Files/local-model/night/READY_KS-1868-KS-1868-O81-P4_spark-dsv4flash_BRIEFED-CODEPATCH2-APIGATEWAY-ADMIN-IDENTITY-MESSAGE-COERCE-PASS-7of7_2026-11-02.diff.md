# READY — KS-1868-KS-1868-O81-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 19:15 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 19:15 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bc8558db6b664967192dba55df844d73fcfe7cc6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
162	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: admin.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts 162 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (12 failed / 18 run; controls green; assertion reds)` [red_first.json: failed=12 of total=18; red cell(s): ['KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R1 users: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R2 users: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R3 users: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R4 users: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R5 organizations: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R6 organizations: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R7 organizations: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R8 organizations: get is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R9 level: patch is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R10 level: patch is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R11 level: patch is logged as its safe text and the route answers the constant 500', 'KS-1868 the identity route catches in admin.ts coerce a non-string message safely RED ks1868 R12 level: patch is logged as its safe text and the route answers the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (18 passed / 18 run)` [green_after.json: failed=0 of total=18, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=0 | after: total=1430 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=0; after_suite.json total=1430 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts` (+162/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `bc8558db6b664967192dba55df844d73fcfe7cc6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1285,7 +1285,7 @@
     } catch (err) {
       let reason: string;
       try {
-        reason = err instanceof Error ? err.message : String(err);
+        reason = String(err instanceof Error ? err.message : err);
       } catch {
         reason = 'unreadable thrown value';
       }
@@ -1313,7 +1313,7 @@
     } catch (err) {
       let reason: string;
       try {
-        reason = err instanceof Error ? err.message : String(err);
+        reason = String(err instanceof Error ? err.message : err);
       } catch {
         reason = 'unreadable thrown value';
       }
@@ -1343,7 +1343,7 @@
     } catch (err) {
       let reason: string;
       try {
-        reason = err instanceof Error ? err.message : String(err);
+        reason = String(err instanceof Error ? err.message : err);
       } catch {
         reason = 'unreadable thrown value';
       }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,162 @@
+/**
+ * KS-1868 (QA gate 110, G110-F1): three identity catches in routes/admin.ts (GET /api/admin/identity/users, GET
+ * /api/admin/identity/organizations and PATCH /api/admin/identity/users/:id/level) read the thrown value inside a guard
+ * (`reason = err instanceof Error ? err.message : String(err)`) and pass `reason` to `log(...)` outside it. The guard covers only
+ * the READ. When the message getter SUCCEEDS and returns a hostile NON-string (a revoked Proxy, an object whose `toString`
+ * throws, a null-prototype object, a Symbol) the value reaches the real winston formatter as it is, which throws on some of them.
+ * The read is now wrapped in `String(...)` inside the same guard, so a value that cannot be turned into text lands in the existing
+ * catch and is logged as the constant 'unreadable thrown value' (a Symbol as its text). The routes answer the same constant 500
+ * an ordinary Error gets.
+ *
+ * The handler under test is the LAST function of the route, taken from the route table and called directly with a fake request and
+ * response. The database stand-in is a plain function that rejects with the thrown value for one statement (a vi.fn() could inspect a
+ * revoked Proxy before the code under test does). Logged values are compared by their type name so a revoked Proxy never reaches a matcher.
+ */
+import { describe, it, expect, beforeEach } from 'vitest';
+import type { Router } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+type Logged = { level: string; message: string; meta: unknown };
+type ResSeed = { statusCode: number; body: unknown; status(c: number): ResSeed; json(b: unknown): ResSeed };
+
+const ks = {
+  thrown: undefined as { value: unknown } | undefined,
+  rejectOn: '' as string,
+  logs: [] as Logged[],
+  queries: [] as string[],
+};
+
+function mkRes(): ResSeed {
+  const r: ResSeed = {
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
+    query: (text: string) => {
+      ks.queries.push(text);
+      if (ks.thrown && ks.rejectOn !== '' && text.includes(ks.rejectOn)) return Promise.reject(ks.thrown.value);
+      if (text.includes('COUNT(*)')) return Promise.resolve({ rows: [{ cnt: '1' }], rowCount: 1 });
+      return Promise.resolve({ rows: [], rowCount: 1 });
+    },
+    isDbAvailable: () => true,
+    redisService: {},
+    services: {},
+    log: (level: string, message: string, meta?: unknown) => {
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
+/** Run the route handler. A handler that rejects leaves the response untouched at 200 with no body. */
+async function invoke(method: string, path: string, params: Record<string, string> = {}, body: unknown = {}): Promise<ResSeed> {
+  const res = mkRes();
+  const req = {
+    params,
+    body,
+    query: {},
+    headers: {},
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
+
+const logOf = (text: string) => ks.logs.filter((l) => l.level === 'error' && l.message === text).map((l) => (l.meta as { error?: unknown }).error).map((e) => (typeof e === 'string' ? e : typeof e));
+const ROUTES: Array<[string, string, string, Record<string, string>, unknown, string, string, string]> = [
+  ['users', 'get', '/api/admin/identity/users', {}, {}, 'FROM users u', '[Identity] Failed to fetch users', 'Failed to fetch identity users'],
+  ['organizations', 'get', '/api/admin/identity/organizations', {}, {}, "COALESCE(metadata->>'trust_level'", '[Identity] Failed to fetch organizations', 'Failed to fetch identity organizations'],
+  ['level', 'patch', '/api/admin/identity/users/:id/level', { id: '00000000-0000-4000-8000-000000001868' }, { verificationLevel: 'HIGH' }, 'UPDATE users SET verification_level', '[Identity] Failed to update level', 'Failed to update verification level'],
+];
+const hostile: Array<[string, () => unknown, string]> = [
+  ['a message that is a revoked Proxy', () => withMessage(revoked), 'unreadable thrown value'],
+  ['a message whose toString throws', () => withMessage(() => ({ toString() { throw new Error('toString boom'); } })), 'unreadable thrown value'],
+  ['a null-prototype message', () => withMessage(() => Object.create(null)), 'unreadable thrown value'],
+  ['a Symbol message', () => withMessage(() => Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+
+beforeEach(() => {
+  ks.thrown = undefined;
+  ks.rejectOn = '';
+  ks.logs.length = 0;
+  ks.queries.length = 0;
+});
+
+describe('KS-1868 the identity route catches in admin.ts coerce a non-string message safely', () => {
+  it.each(ROUTES)('control ks1868 C1 %s: an ordinary Error is logged with its message and the route answers the constant 500', async (_n, method, path, params, body, sql, logText, answer) => {
+    ks.thrown = { value: new Error('db boom 10.0.0.7') };
+    ks.rejectOn = sql;
+    const res = await invoke(method, path, params, body);
+    expect(logOf(logText)).toEqual(['db boom 10.0.0.7']);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: answer } });
+  });
+
+  it.each(ROUTES)('control ks1868 C2 %s: a thrown plain string is logged as itself and the route answers the constant 500', async (_n, method, path, params, body, sql, logText, answer) => {
+    ks.thrown = { value: 'plain string down' };
+    ks.rejectOn = sql;
+    const res = await invoke(method, path, params, body);
+    expect(logOf(logText)).toEqual(['plain string down']);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: answer } });
+  });
+
+  type Cell = [number, string, string, string, Record<string, string>, unknown, string, string, string, string, () => unknown, string];
+  const cells: Cell[] = [];
+  let n = 0;
+  for (const r of ROUTES) {
+    for (const h of hostile) {
+      n += 1;
+      cells.push([n, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], h[0], h[1], h[2]]);
+    }
+  }
+  it.each(cells)(
+    'RED ks1868 R%s %s: %s is logged as its safe text and the route answers the constant 500',
+    async (_i, _n, method, path, params, body, sql, logText, answer, _what, make, text) => {
+      ks.thrown = { value: make() };
+      ks.rejectOn = sql;
+      const res = await invoke(method, path, params, body);
+      expect(logOf(logText)).toEqual([text]);
+      expect(res.statusCode).toBe(500);
+      expect(res.body).toEqual({ success: false, error: { code: 'INTERNAL_ERROR', message: answer } });
+    },
+  );
+});
```
