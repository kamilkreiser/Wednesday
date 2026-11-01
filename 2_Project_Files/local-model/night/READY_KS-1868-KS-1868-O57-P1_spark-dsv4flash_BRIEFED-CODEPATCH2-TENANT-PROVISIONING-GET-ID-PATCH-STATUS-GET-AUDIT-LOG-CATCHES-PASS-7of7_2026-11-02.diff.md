# READY — KS-1868-KS-1868-O57-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/out.md.checker/patch.diff`** (from `ls` at 07:47 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:47 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tenant-provisioning/src/index.ts } + { Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	3	Blockchain/Dev/services/tenant-provisioning/src/index.ts
186	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tenant-provisioning/src/index.ts`; test(s): `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tenant-provisioning/src/index.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts 186 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ["KS-1868 'GET /api/tenants/:id' catch reads the thrown value safely RED ks1868 R1 GET /api/tenants/:id: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /api/tenants/:id' catch reads the thrown value safely RED ks1868 R2 GET /api/tenants/:id: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 'PATCH /api/tenants/:id/status' catch reads the thrown value safely RED ks1868 R1 PATCH /api/tenants/:id/status: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'PATCH /api/tenants/:id/status' catch reads the thrown value safely RED ks1868 R2 PATCH /api/tenants/:id/status: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /api/audit-log' catch reads the thrown value safely RED ks1868 R1 GET /api/audit-log: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /api/audit-log' catch reads the thrown value safely RED ks1868 R2 GET /api/audit-log: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=84 failed=0 | after: total=96 failed=0` · `NEW reds: []` [baseline_suite.json total=84 failed=0; after_suite.json total=96 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (+18/-3 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts` (+186/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/tenant-provisioning/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -421,7 +421,12 @@
       contacts: contacts.rows,
     });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     console.error('[provisioning] GET /api/tenants/:id failed:', message);
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
@@ -480,6 +485,11 @@
     res.json({ success: true, status });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     console.error('[provisioning] PATCH /api/tenants/:id/status failed:', message);
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
@@ -648,7 +658,12 @@
     const countResult = await platformQuery(`SELECT COUNT(*) as total FROM platform_audit_log`);
     res.json({ success: true, entries: result.rows, total: parseInt(countResult.rows[0].total) });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     console.error('[provisioning] GET /api/audit-log failed:', message);
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,186 @@
+/**
+ * KS-1868: the three catch blocks below read the caught value with `err instanceof Error ? err.message : String(err)` only to put it in a
+ * `console.error` line. That read can itself throw (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws throws on
+ * `.message`), and inside an async Express 4 handler the rejection is not caught: the request gets no response and Node sees an unhandled
+ * rejection. Each catch now reads the value inside its own try and logs the constant `unreadable thrown value` when the read throws, and
+ * answers the same constant 500 as before.
+ *
+ * Routes covered here: GET /api/tenants/:id, PATCH /api/tenants/:id/status, GET /api/audit-log.
+ *
+ * The module binds a port and opens a database pool on import, so `express`, `pg` and `@secuura/shared` are replaced and the route handlers
+ * are captured and called directly with a fake request and response: no port is bound, no database is touched. The stand-ins that reject with
+ * the thrown value are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before the
+ * code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
+import type { MockInstance } from 'vitest';
+
+const ks = vi.hoisted(() => ({
+  routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
+  sql: [] as string[],
+  plan: (() => Promise.resolve({ rows: [], rowCount: 0 })) as (text: string) => Promise<unknown>,
+}));
+
+vi.mock('express', () => {
+  const app = {
+    use: () => app,
+    param: () => app,
+    get: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['GET ' + p] = f;
+    },
+    post: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['POST ' + p] = f;
+    },
+    patch: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['PATCH ' + p] = f;
+    },
+    delete: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['DELETE ' + p] = f;
+    },
+    listen: () => ({}),
+  };
+  const express = Object.assign(() => app, { json: () => () => undefined });
+  return { default: express };
+});
+vi.mock('pg', () => {
+  class Pool {
+    query(text: string) {
+      ks.sql.push(text.replace(/\s+/g, ' ').trim());
+      return ks.plan(text);
+    }
+    connect() {
+      return Promise.resolve({
+        query: (text: string) => {
+          ks.sql.push(text.replace(/\s+/g, ' ').trim());
+          return ks.plan(text);
+        },
+        release: () => undefined,
+      });
+    }
+    on() {
+      return this;
+    }
+    end() {
+      return Promise.resolve();
+    }
+  }
+  return { default: { Pool }, Pool };
+});
+vi.mock('@secuura/shared', () => ({
+  enforceProductionConfig: () => undefined,
+  authenticate: () => () => undefined,
+  errorHandler: () => undefined,
+  pgSslConfig: () => undefined,
+  rejectNulBytes: () => () => undefined,
+}));
+
+type Res57 = {
+  statusCode: number;
+  body: unknown;
+  status(c: number): Res57;
+  json(b: unknown): Res57;
+};
+
+function mkRes(): Res57 {
+  const r: Res57 = {
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
+const CONST500 = {
+  success: false,
+  error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
+};
+const TID = 'd5700000-0000-4000-8000-000000000001';
+
+let spy57: MockInstance<typeof console.error>;
+
+/** Everything passed to console.error, one line per call; a non-string argument shows as <<non-string:type>>. */
+function errLog(): string {
+  return spy57.mock.calls
+    .map((args) => args.map((x) => (typeof x === 'string' ? x : '<<non-string:' + typeof x + '>>')).join(' '))
+    .join('\n');
+}
+
+type Case57 = { route: string; req: unknown };
+
+const CASES57: Case57[] = [
+  { route: 'GET /api/tenants/:id', req: { params: { id: TID }, body: {}, query: {} } },
+  { route: 'PATCH /api/tenants/:id/status', req: { params: { id: TID }, body: { status: 'suspended' }, query: {} } },
+  { route: 'GET /api/audit-log', req: { params: {}, body: {}, query: {} } },
+];
+
+/** Run one route handler with the database rejecting every statement with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(c: Case57, value: unknown): Promise<Res57> {
+  ks.plan = () => Promise.reject(value);
+  const res = mkRes();
+  await ks.routes[c.route](c.req, res).catch(() => undefined);
+  return res;
+}
+
+beforeAll(async () => {
+  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
+  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
+  await import('../index.js');
+}, 30_000);
+
+beforeEach(() => {
+  ks.sql.length = 0;
+  spy57 = vi.spyOn(console, 'error').mockImplementation(() => undefined);
+});
+
+afterEach(() => {
+  spy57.mockRestore();
+});
+
+describe.each(CASES57)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const res = await invoke(c, proxy);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: unreadable thrown value');
+    expect(ks.sql.filter((s) => s.startsWith('INSERT'))).toEqual([]);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const getterThrows = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const res = await invoke(c, getterThrows);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: unreadable thrown value');
+    expect(ks.sql.filter((s) => s.startsWith('INSERT'))).toEqual([]);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {
+    const res = await invoke(c, new Error('ordinary boom 10.0.0.7'));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: ordinary boom 10.0.0.7');
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    const res = await invoke(c, 'plain-string-marker');
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: plain-string-marker');
+  });
+});
```
