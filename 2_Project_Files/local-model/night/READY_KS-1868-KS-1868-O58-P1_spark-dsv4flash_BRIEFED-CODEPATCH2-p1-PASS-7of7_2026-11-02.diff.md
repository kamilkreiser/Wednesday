# READY — KS-1868-KS-1868-O58-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/out.md.checker/patch.diff`** (from `ls` at 08:05 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:05 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
167	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: admin.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts 167 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (7 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=7 of total=14; red cell(s): ["KS-1868 identity admin 'GET users' catch reads the thrown value safely RED ks1868 R1 GET users: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 identity admin 'GET users' catch reads the thrown value safely RED ks1868 R2 GET users: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 identity admin 'GET organizations' catch reads the thrown value safely RED ks1868 R1 GET organizations: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 identity admin 'GET organizations' catch reads the thrown value safely RED ks1868 R2 GET organizations: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 identity admin 'PATCH level' catch reads the thrown value safely RED ks1868 R1 PATCH level: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 identity admin 'PATCH level' catch reads the thrown value safely RED ks1868 R2 PATCH level: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", 'KS-1868 identity admin PATCH level: what is written does not change RED ks1868 R3 PATCH level: with an unreadable failure the one UPDATE was still issued with the same parameters, and nothing else is written']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1373 failed=0 | after: total=1387 failed=0` · `NEW reds: []` [baseline_suite.json total=1373 failed=0; after_suite.json total=1387 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts` (+167/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o58_p1_api_gateway_admin_identity_users_organizations_level_unreadable_throw-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1272,6 +1272,12 @@
       res.json({ success: true, users });
     } catch (err) {
-      log('error', '[Identity] Failed to fetch users', { error: err instanceof Error ? err.message : String(err) });
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Identity] Failed to fetch users', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch identity users' } });
     }
   });
@@ -1293,7 +1299,13 @@
       `));
       res.json({ success: true, organizations: result.rows });
     } catch (err) {
-      log('error', '[Identity] Failed to fetch organizations', { error: err instanceof Error ? err.message : String(err) });
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Identity] Failed to fetch organizations', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch identity organizations' } });
     }
   });
@@ -1317,7 +1329,13 @@
       }
       res.json({ success: true, userId: id, verificationLevel });
     } catch (err) {
-      log('error', '[Identity] Failed to update level', { error: err instanceof Error ? err.message : String(err) });
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Identity] Failed to update level', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update verification level' } });
     }
   });
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,167 @@
+/**
+ * KS-1868: three identity-admin route catches in routes/admin.ts (GET /api/admin/identity/users, GET /api/admin/identity/organizations,
+ * PATCH /api/admin/identity/users/:id/level) log `{ error: err instanceof Error ? err.message : String(err) }` before answering a constant 500.
+ * That read can itself throw (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws throws on `.message`), and then
+ * the catch escapes: no log, no 500, the async handler rejects and Express 4 does not answer the request. Each read now sits in its own try
+ * and falls back to the constant `unreadable thrown value`.
+ *
+ * The handler under test is the LAST function of the route (the one after requireAdmin / the body parser), taken from the route table and
+ * called directly with a fake request and response, so the defect shows as an unchanged response and not as a hung request. The database
+ * stand-in is a plain function that rejects with the thrown value (a vi.fn() could inspect a revoked Proxy before the code under test does).
+ */
+import { describe, it, expect, beforeEach } from 'vitest';
+import type { Router } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+type Logged = { level: string; message: string; meta: { error?: unknown } | undefined };
+type Res58 = { statusCode: number; body: unknown; status(c: number): Res58; json(b: unknown): Res58 };
+
+const ks = {
+  thrown: undefined as { value: unknown } | undefined,
+  logs: [] as Logged[],
+  queries: [] as Array<{ text: string; params: unknown[] | undefined }>,
+};
+
+function mkRes(): Res58 {
+  const r: Res58 = {
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
+    query: (text: string, params?: unknown[]) => {
+      ks.queries.push({ text, params });
+      if (ks.thrown) return Promise.reject(ks.thrown.value);
+      return Promise.resolve({ rows: [{ id: 'u-1' }], rowCount: 1 });
+    },
+    isDbAvailable: () => false,
+    redisService: {},
+    services: {},
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
+const TID = 'd5800000-0000-4000-8000-000000000001';
+
+/** Run a route handler. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(method: string, path: string): Promise<Res58> {
+  const res = mkRes();
+  const req = {
+    params: { id: TID },
+    body: { verificationLevel: 'HIGH' },
+    query: {},
+    headers: {},
+    user: { userId: 'admin-58', role: 'SYSTEM_ADMIN', email: 'admin-58@test.io', verificationLevel: 'HIGH' },
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
+function getterError(): unknown {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+}
+
+type Case58 = { name: string; method: string; path: string; failed: string; answer: string };
+
+const CASES58: Case58[] = [
+  { name: 'GET users', method: 'get', path: '/api/admin/identity/users', failed: '[Identity] Failed to fetch users', answer: 'Failed to fetch identity users' },
+  { name: 'GET organizations', method: 'get', path: '/api/admin/identity/organizations', failed: '[Identity] Failed to fetch organizations', answer: 'Failed to fetch identity organizations' },
+  { name: 'PATCH level', method: 'patch', path: '/api/admin/identity/users/:id/level', failed: '[Identity] Failed to update level', answer: 'Failed to update verification level' },
+];
+
+const expected500 = (c: Case58) => ({ success: false, error: { code: 'INTERNAL_ERROR', message: c.answer } });
+const failedLog = (c: Case58): Logged | undefined => ks.logs.find((l) => l.level === 'error' && l.message === c.failed);
+
+beforeEach(() => {
+  ks.thrown = undefined;
+  ks.logs.length = 0;
+  ks.queries.length = 0;
+});
+
+describe.each(CASES58)('KS-1868 identity admin $name catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.name}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {
+    ks.thrown = { value: revoked() };
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(expected500(c));
+    expect(failedLog(c)?.meta).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it(`RED ks1868 R2 ${c.name}: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500`, async () => {
+    ks.thrown = { value: getterError() };
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(expected500(c));
+    expect(failedLog(c)?.meta).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it(`control ks1868 C1 ${c.name}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {
+    ks.thrown = { value: new Error('db boom 10.0.0.7') };
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(expected500(c));
+    expect(JSON.stringify(res.body)).not.toContain('db boom');
+    expect(failedLog(c)?.meta).toEqual({ error: 'db boom 10.0.0.7' });
+  });
+
+  it(`control ks1868 C2 ${c.name}: a thrown string is logged as itself, as before`, async () => {
+    ks.thrown = { value: 'plain string failure' };
+    const res = await invoke(c.method, c.path);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(expected500(c));
+    expect(failedLog(c)?.meta).toEqual({ error: 'plain string failure' });
+  });
+});
+
+describe('KS-1868 identity admin PATCH level: what is written does not change', () => {
+  it('RED ks1868 R3 PATCH level: with an unreadable failure the one UPDATE was still issued with the same parameters, and nothing else is written', async () => {
+    ks.thrown = { value: revoked() };
+    await invoke('patch', '/api/admin/identity/users/:id/level');
+    expect(ks.queries.length).toBe(1);
+    expect(ks.queries[0].text).toContain('UPDATE users SET verification_level');
+    expect(ks.queries[0].params).toEqual(['HIGH', TID]);
+    expect(failedLog(CASES58[2])?.meta).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('control ks1868 C3 PATCH level: a successful update answers 200 with the new level and logs no error', async () => {
+    const res = await invoke('patch', '/api/admin/identity/users/:id/level');
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true, userId: TID, verificationLevel: 'HIGH' });
+    expect(ks.queries.length).toBe(1);
+    expect(ks.logs.filter((l) => l.level === 'error')).toEqual([]);
+  });
+});
```
