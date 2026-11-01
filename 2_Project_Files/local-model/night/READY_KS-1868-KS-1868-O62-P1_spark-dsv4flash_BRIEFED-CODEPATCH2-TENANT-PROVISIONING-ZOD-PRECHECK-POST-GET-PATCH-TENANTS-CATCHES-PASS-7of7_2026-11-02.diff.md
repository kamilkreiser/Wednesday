# READY — KS-1868-KS-1868-O62-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 08:25 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:25 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tenant-provisioning/src/index.ts } + { Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
27	3	Blockchain/Dev/services/tenant-provisioning/src/index.ts
232	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (27 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tenant-provisioning/src/index.ts`; test(s): `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tenant-provisioning/src/index.ts 27 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts 232 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ["KS-1868 'POST /api/tenants' catch (ZodError check first) reads the thrown value safely RED ks1868 R1 POST /api/tenants: a revoked Proxy thrown value takes the ordinary Error path with a constant reason", "KS-1868 'POST /api/tenants' catch (ZodError check first) reads the thrown value safely RED ks1868 R2 POST /api/tenants: an Error whose message getter throws takes the ordinary Error path with a constant reason", "KS-1868 'GET /api/tenants' catch (ZodError check first) reads the thrown value safely RED ks1868 R1 GET /api/tenants: a revoked Proxy thrown value takes the ordinary Error path with a constant reason", "KS-1868 'GET /api/tenants' catch (ZodError check first) reads the thrown value safely RED ks1868 R2 GET /api/tenants: an Error whose message getter throws takes the ordinary Error path with a constant reason", "KS-1868 'PATCH /api/tenants/:id' catch (ZodError check first) reads the thrown value safely RED ks1868 R1 PATCH /api/tenants/:id: a revoked Proxy thrown value takes the ordinary Error path with a constant reason", "KS-1868 'PATCH /api/tenants/:id' catch (ZodError check first) reads the thrown value safely RED ks1868 R2 PATCH /api/tenants/:id: an Error whose message getter throws takes the ordinary Error path with a constant reason"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=84 failed=0 | after: total=96 failed=0` · `NEW reds: []` [baseline_suite.json total=84 failed=0; after_suite.json total=96 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (+27/-3 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts` (+232/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/tenant-provisioning/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -334,7 +334,15 @@
       keyPending,
       ...(keyPending ? { keyPendingMessage: KEY_PENDING_MESSAGE } : {}),
     });
-  } catch (err: unknown) {
+  } catch (thrown: unknown) {
+    let err: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      err = new Error('unreadable thrown value');
+    }
     if (err instanceof z.ZodError) {
       res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: err.errors } });
       return;
@@ -375,7 +383,15 @@
        ORDER BY t.created_at DESC`,
     );
     res.json({ success: true, tenants: result.rows, total: result.rowCount });
-  } catch (err: unknown) {
+  } catch (thrown: unknown) {
+    let err: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      err = new Error('unreadable thrown value');
+    }
     // Return 400 for validation errors, 500 for everything else
     if (err instanceof z.ZodError) {
       res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: err.errors } });
@@ -535,5 +551,13 @@
     res.json({ success: true });
-  } catch (err: unknown) {
+  } catch (thrown: unknown) {
+    let err: unknown = thrown;
+    try {
+      if (!(thrown instanceof z.ZodError)) {
+        String(thrown instanceof Error ? thrown.message : thrown);
+      }
+    } catch {
+      err = new Error('unreadable thrown value');
+    }
     // KS-497: a body failing updateTenantSchema threw a ZodError that fell
     // into the generic handler → raw 500. Map it to the declared 400, the
     // same shape the list route already uses.
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts
@@ -0,0 +1,232 @@
+/**
+ * KS-1868: the three catch blocks below (POST /api/tenants, GET /api/tenants, PATCH /api/tenants/:id) each begin with `err instanceof z.ZodError`
+ * and then read the caught value with `err instanceof Error ? err.message : String(err)`. Both reads can themselves throw (a revoked Proxy throws
+ * on `instanceof`; an Error whose `message` getter throws throws on `.message`), and inside an async Express 4 handler the rejection is not
+ * caught: the request gets no response and Node sees an unhandled rejection. Each catch now probes both reads inside its own try: an unreadable
+ * value is replaced by an ordinary Error('unreadable thrown value'), so the route takes the same path an ordinary Error takes. An ordinary
+ * ZodError still answers 400 with `details` equal to its `errors`, and an ordinary Error still takes its own path.
+ *
+ * POST /api/tenants creates a tenant: when the failure comes after the tenant row is inserted, an ordinary Error rolls the partial tenant back
+ * (three DELETE statements) and a ZodError does not (it answers 400 straight away). The cells pin both of those unchanged and show that an
+ * unreadable value now rolls back like an ordinary Error.
+ *
+ * The module binds a port and opens a database pool on import, so `express`, `pg` and `@secuura/shared` are replaced and the route handlers
+ * are captured and called directly with a fake request and response: no port is bound, no database is touched, and the key-service fetch is
+ * replaced by a rejection. The stand-ins that reject with the thrown value are plain functions, not vi.fn(): a spy inspects what it rejects
+ * with and could itself fail on a revoked Proxy before the code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
+import type { MockInstance } from 'vitest';
+import { z } from 'zod';
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
+type Res62 = {
+  statusCode: number;
+  body: unknown;
+  status(c: number): Res62;
+  json(b: unknown): Res62;
+};
+
+function mkRes(): Res62 {
+  const r: Res62 = {
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
+const TID = 'd6200000-0000-4000-8000-000000000001';
+
+let spy62: MockInstance<typeof console.error>;
+
+/** Everything passed to console.error, one line per call; a non-string argument shows as <<non-string:type>>. */
+function errLog(): string {
+  return spy62.mock.calls
+    .map((args) => args.map((x) => (typeof x === 'string' ? x : '<<non-string:' + typeof x + '>>')).join(' '))
+    .join('\n');
+}
+
+type Case62 = {
+  route: string;
+  req: unknown;
+  plan: (text: string, value: unknown) => Promise<unknown>;
+  /** POST echoes the caught message in its 500 (Kam's open card); the other two answer the constant 500. */
+  echoes: boolean;
+  /** POST rolls a partly-created tenant back with three DELETE statements when an Error (not a ZodError) is caught after the insert. */
+  rollsBack: boolean;
+};
+
+const reject = (_text: string, value: unknown) => Promise.reject(value);
+
+function planPost(text: string, value: unknown): Promise<unknown> {
+  const t = text.replace(/\s+/g, ' ').trim();
+  if (t.startsWith('SELECT id FROM tenants')) return Promise.resolve({ rows: [], rowCount: 0 });
+  if (t.startsWith('INSERT INTO tenants')) return Promise.resolve({ rows: [{ id: TID }], rowCount: 1 });
+  if (t.startsWith('DELETE')) return Promise.resolve({ rows: [], rowCount: 1 });
+  return Promise.reject(value);
+}
+
+const CASES62: Case62[] = [
+  {
+    route: 'POST /api/tenants',
+    req: { params: {}, body: { name: 'KS1868 Tenant', slug: 'ks1868-tenant' }, query: {}, headers: {} },
+    plan: planPost,
+    echoes: true,
+    rollsBack: true,
+  },
+  { route: 'GET /api/tenants', req: { params: {}, body: {}, query: {}, headers: {} }, plan: reject, echoes: false, rollsBack: false },
+  {
+    route: 'PATCH /api/tenants/:id',
+    req: { params: { id: TID }, body: { name: 'KS1868 renamed' }, query: {}, headers: {} },
+    plan: reject,
+    echoes: false,
+    rollsBack: false,
+  },
+];
+
+const body500 = (c: Case62, text: string) => (c.echoes ? { success: false, error: { code: 'INTERNAL_ERROR', message: text } } : CONST500);
+const deletes = () => ks.sql.filter((s) => s.startsWith('DELETE'));
+
+/** Run one route handler with the database rejecting its statements with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(c: Case62, value: unknown): Promise<Res62> {
+  ks.plan = (text) => c.plan(text, value);
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
+  spy62 = vi.spyOn(console, 'error').mockImplementation(() => undefined);
+  vi.spyOn(console, 'warn').mockImplementation(() => undefined);
+  vi.stubGlobal('fetch', () => Promise.reject(new Error('ks1868 no network')));
+});
+
+afterEach(() => {
+  vi.unstubAllGlobals();
+  vi.restoreAllMocks();
+});
+
+describe.each(CASES62)('KS-1868 $route catch (ZodError check first) reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown value takes the ordinary Error path with a constant reason`, async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const res = await invoke(c, proxy);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c, 'unreadable thrown value'));
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: unreadable thrown value');
+    expect(deletes()).toHaveLength(c.rollsBack ? 3 : 0);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws takes the ordinary Error path with a constant reason`, async () => {
+    const getterThrows = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const res = await invoke(c, getterThrows);
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c, 'unreadable thrown value'));
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: unreadable thrown value');
+    expect(deletes()).toHaveLength(c.rollsBack ? 3 : 0);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary ZodError answers 400 with details equal to its errors, logs nothing and rolls nothing back`, async () => {
+    const zerr = new z.ZodError([{ code: 'custom', path: ['name'], message: 'ks1868 control issue' }]);
+    const res = await invoke(c, zerr);
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual({
+      success: false,
+      error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zerr.errors },
+    });
+    expect(errLog()).toBe('');
+    expect(deletes()).toEqual([]);
+  });
+
+  it(`control ks1868 C2 ${c.route}: an ordinary Error logs its own message and answers the same 500 as before`, async () => {
+    const res = await invoke(c, new Error('ordinary boom 10.0.0.7'));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(body500(c, 'ordinary boom 10.0.0.7'));
+    if (!c.echoes) expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
+    expect(errLog()).toContain('[provisioning] ' + c.route + ' failed: ordinary boom 10.0.0.7');
+    expect(deletes()).toHaveLength(c.rollsBack ? 3 : 0);
+  });
+});
```
