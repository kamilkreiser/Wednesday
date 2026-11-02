# READY — KS-1868-KS-1868-O72-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 11:35 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:35 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8aded39571d0d26dc5cd3632948803cd95c4680c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
166	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: admin.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts 166 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (7 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=7 of total=12; red cell(s): ["KS-1868 organization admin 'POST create' catch reads the thrown value safely RED ks1868 R1 POST create: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 organization admin 'POST create' catch reads the thrown value safely RED ks1868 R2 POST create: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 organization admin 'PUT update' catch reads the thrown value safely RED ks1868 R1 PUT update: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 organization admin 'PUT update' catch reads the thrown value safely RED ks1868 R2 PUT update: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 organization admin 'DELETE delete' catch reads the thrown value safely RED ks1868 R1 DELETE delete: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 organization admin 'DELETE delete' catch reads the thrown value safely RED ks1868 R2 DELETE delete: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", 'KS-1868 organization admin routes: what is written does not change RED ks1868 R3 POST create: with an unreadable failure the one INSERT was still issued once, and nothing else is written']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1387 failed=0 | after: total=1399 failed=0` · `NEW reds: []` [baseline_suite.json total=1387 failed=0; after_suite.json total=1399 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts` (+166/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8aded39571d0d26dc5cd3632948803cd95c4680c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p3_admin_organization_route_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1452,7 +1452,13 @@
       }
       res.status(201).json({ id, name, type: type || 'Organization', status: status || 'pending', userCount: 0, documentCount: 0, createdAt: new Date().toISOString() });
     } catch (err) {
-      log('error', '[Orgs] Create failed', { error: (err as Error).message });
+      let reason: string;
+      try {
+        reason = (err as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Orgs] Create failed', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create organization' } });
     }
   });
@@ -1472,7 +1478,13 @@
         res.json({ success: true });
       }
     } catch (err) {
-      log('error', '[Orgs] Update failed', { error: (err as Error).message });
+      let reason: string;
+      try {
+        reason = (err as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Orgs] Update failed', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update organization' } });
     }
   });
@@ -1511,7 +1523,13 @@
       }
       res.json({ success: true });
     } catch (err) {
-      log('error', '[Orgs] Delete failed', { error: (err as Error).message });
+      let reason: string;
+      try {
+        reason = (err as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('error', '[Orgs] Delete failed', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete organization' } });
     }
   });
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-organization-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,166 @@
+/**
+ * KS-1868: three organization-admin route catches in routes/admin.ts (POST /api/users/admin/organizations, PUT and DELETE
+ * /api/users/admin/organizations/:id) log `{ error: (err as Error).message }` before answering a constant 500. That read can itself
+ * throw (a revoked Proxy throws on any property read; an Error whose `message` getter throws throws on `.message`), and then the catch
+ * escapes: no log, no 500, the async handler rejects and Express 4 does not answer the request. Each read now sits in its own try and
+ * falls back to the constant `unreadable thrown value`.
+ *
+ * The handler under test is the LAST function of the route (the one after requireAdmin / the body parser), taken from the route table
+ * and called directly with a fake request and response, so the defect shows as an unchanged response and not as a hung request. The
+ * database stand-in is a plain function that rejects with the thrown value (a vi.fn() could inspect a revoked Proxy before the code
+ * under test does).
+ */
+import { describe, it, expect, beforeEach } from 'vitest';
+import type { Router } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+type Logged = { level: string; message: string; meta: { error?: unknown } | undefined };
+type ResOrg = { statusCode: number; body: unknown; status(c: number): ResOrg; json(b: unknown): ResOrg };
+
+const ks = {
+  thrown: undefined as { value: unknown } | undefined,
+  logs: [] as Logged[],
+  queries: [] as Array<{ text: string; params: unknown[] | undefined }>,
+};
+
+function mkRes(): ResOrg {
+  const r: ResOrg = {
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
+      return Promise.resolve({ rows: [{ id: 'o-1' }], rowCount: 1 });
+    },
+    isDbAvailable: () => true,
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
+const OID = 'd5800000-0000-4000-8000-000000000002';
+
+/** Run a route handler. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(method: string, path: string): Promise<ResOrg> {
+  const res = mkRes();
+  const req = {
+    params: { id: OID },
+    body: { name: 'Acme Org', type: 'Organization', status: 'active' },
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
+type CaseOrg = { name: string; method: string; path: string; failed: string; answer: string };
+
+const CASES: CaseOrg[] = [
+  { name: 'POST create', method: 'post', path: '/api/users/admin/organizations', failed: '[Orgs] Create failed', answer: 'Failed to create organization' },
+  { name: 'PUT update', method: 'put', path: '/api/users/admin/organizations/:id', failed: '[Orgs] Update failed', answer: 'Failed to update organization' },
+  { name: 'DELETE delete', method: 'delete', path: '/api/users/admin/organizations/:id', failed: '[Orgs] Delete failed', answer: 'Failed to delete organization' },
+];
+
+const expected500 = (c: CaseOrg) => ({ success: false, error: { code: 'INTERNAL_ERROR', message: c.answer } });
+const failedLog = (c: CaseOrg): Logged | undefined => ks.logs.find((l) => l.level === 'error' && l.message === c.failed);
+
+beforeEach(() => {
+  ks.thrown = undefined;
+  ks.logs.length = 0;
+  ks.queries.length = 0;
+});
+
+describe.each(CASES)('KS-1868 organization admin $name catch reads the thrown value safely', (c) => {
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
+});
+
+describe('KS-1868 organization admin routes: what is written does not change', () => {
+  it('RED ks1868 R3 POST create: with an unreadable failure the one INSERT was still issued once, and nothing else is written', async () => {
+    ks.thrown = { value: revoked() };
+    await invoke('post', '/api/users/admin/organizations');
+    expect(ks.queries.length).toBe(1);
+    expect(ks.queries[0].text).toContain('INSERT INTO organizations');
+    expect(failedLog(CASES[0])?.meta).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('control ks1868 C2 DELETE delete: a successful delete answers 200 and logs no error', async () => {
+    const res = await invoke('delete', '/api/users/admin/organizations/:id');
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true });
+    expect(ks.queries.length).toBe(1);
+    expect(ks.logs.filter((l) => l.level === 'error')).toEqual([]);
+  });
+
+  it('control ks1868 C3 POST create: a successful create answers 201 and logs no error', async () => {
+    const res = await invoke('post', '/api/users/admin/organizations');
+    expect(res.statusCode).toBe(201);
+    expect(ks.queries.length).toBe(1);
+    expect(ks.logs.filter((l) => l.level === 'error')).toEqual([]);
+  });
+});
```
