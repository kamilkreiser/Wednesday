# READY — KS-1868-KS-1868-O57-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 07:44 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:44 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tenant-provisioning/src/index.ts } + { Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	3	Blockchain/Dev/services/tenant-provisioning/src/index.ts
228	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (20 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tenant-provisioning/src/index.ts`; test(s): `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tenant-provisioning/src/index.ts 20 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts 228 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 DELETE /api/tenants/:id with R1 revoked Proxy RED ks1868 outer: the failed attempt is still audited, logged as a constant reason, and answered with the constant 500', 'KS-1868 DELETE /api/tenants/:id with R1 revoked Proxy RED ks1868 rollback: a rollback that fails with it is logged as a constant reason and the ORIGINAL error is still the one reported', 'KS-1868 DELETE /api/tenants/:id with R1 revoked Proxy RED ks1868 audit: an audit write that fails with it is logged as a constant reason and the route still answers the constant 500', 'KS-1868 DELETE /api/tenants/:id with R2 Error whose message getter throws RED ks1868 outer: the failed attempt is still audited, logged as a constant reason, and answered with the constant 500', 'KS-1868 DELETE /api/tenants/:id with R2 Error whose message getter throws RED ks1868 rollback: a rollback that fails with it is logged as a constant reason and the ORIGINAL error is still the one reported', 'KS-1868 DELETE /api/tenants/:id with R2 Error whose message getter throws RED ks1868 audit: an audit write that fails with it is logged as a constant reason and the route still answers the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=84 failed=0 | after: total=93 failed=0` · `NEW reds: []` [baseline_suite.json total=84 failed=0; after_suite.json total=93 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (+20/-3 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts` (+228/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/tenant-provisioning/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -600,7 +600,13 @@
       await client.query(archived ? 'COMMIT' : 'ROLLBACK');
     } catch (err) {
       await client.query('ROLLBACK').catch((rollbackErr: unknown) => {
-        console.error('[provisioning] DELETE /api/tenants/:id rollback failed:', rollbackErr instanceof Error ? rollbackErr.message : String(rollbackErr));
+        let reason: string;
+        try {
+          reason = rollbackErr instanceof Error ? rollbackErr.message : String(rollbackErr);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        console.error('[provisioning] DELETE /api/tenants/:id rollback failed:', reason);
       });
       throw err;
     } finally {
@@ -619,14 +625,25 @@
       message: 'Tenant archived. No data was removed: every row is kept and no database is dropped.',
     });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     // Ruling 1 (KS-1861): the audit log records a failed attempt too. Its own failure is logged, never silent.
     await platformQuery(
       `INSERT INTO platform_audit_log (action, target_type, target_id, details)
        VALUES ('tenant_archive_failed', 'tenant', $1, $2)`,
       [req.params.id, JSON.stringify({ erased: false })],
     ).catch((auditErr: unknown) => {
-      console.error('[provisioning] DELETE /api/tenants/:id could not audit the failure:', auditErr instanceof Error ? auditErr.message : String(auditErr));
+      let reason: string;
+      try {
+        reason = auditErr instanceof Error ? auditErr.message : String(auditErr);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      console.error('[provisioning] DELETE /api/tenants/:id could not audit the failure:', reason);
     });
     console.error('[provisioning] DELETE /api/tenants/:id failed:', message);
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts
@@ -0,0 +1,228 @@
+/**
+ * KS-1868: DELETE /api/tenants/:id (the archive route) has three catch-block reads of a caught value written as
+ * `x instanceof Error ? x.message : String(x)`: the rollback failure log inside the transaction block, the outer `message`, and the
+ * audit-write failure log in the outer catch. Each read can itself throw (a revoked Proxy throws on `instanceof`; an Error whose `message`
+ * getter throws throws on `.message`). A throw there escapes the catch: the outer catch loses the failed-attempt audit row and the 500,
+ * and a throw out of either `.catch` callback replaces the error being reported (rollback) or leaves the request without an answer (audit).
+ * Each read now sits in its own try and falls back to the constant `unreadable thrown value`.
+ *
+ * The module binds a port and opens a database pool on import, so `express`, `pg` and `@secuura/shared` are replaced and the route handler
+ * is captured and called directly with a fake request and response: no port is bound, no database is touched. The stand-ins that reject
+ * with the thrown value are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy
+ * before the code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
+import type { MockInstance } from 'vitest';
+
+const ks = vi.hoisted(() => ({
+  routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
+  sql: [] as string[],
+  updateThrow: undefined as { value: unknown } | undefined,
+  rollbackThrow: undefined as { value: unknown } | undefined,
+  auditThrow: undefined as { value: unknown } | undefined,
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
+  const run = (text: string): Promise<unknown> => {
+    const sql = text.replace(/\s+/g, ' ').trim();
+    ks.sql.push(sql);
+    if (sql.startsWith('SELECT slug, status FROM tenants')) return Promise.resolve({ rows: [{ slug: 'acme-co', status: 'active' }], rowCount: 1 });
+    if (sql.startsWith("UPDATE tenants SET status = 'archived'")) {
+      return ks.updateThrow ? Promise.reject(ks.updateThrow.value) : Promise.resolve({ rows: [], rowCount: 1 });
+    }
+    if (sql === 'ROLLBACK' && ks.rollbackThrow) return Promise.reject(ks.rollbackThrow.value);
+    if (sql.includes("'tenant_archive_failed'") && ks.auditThrow) return Promise.reject(ks.auditThrow.value);
+    return Promise.resolve({ rows: [], rowCount: 0 });
+  };
+  class Pool {
+    query(text: string) {
+      return run(text);
+    }
+    connect() {
+      return Promise.resolve({ query: (text: string) => run(text), release: () => undefined });
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
+const TID = 'd5700000-0000-4000-8000-000000000002';
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
+/** Run the DELETE handler. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(): Promise<Res57> {
+  const res = mkRes();
+  await ks.routes['DELETE /api/tenants/:id']({ params: { id: TID }, body: { confirm: true }, query: {} }, res).catch(() => undefined);
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
+const auditWritten = (): boolean => ks.sql.some((s) => s.includes("'tenant_archive_failed'"));
+
+beforeAll(async () => {
+  process.env.PLATFORM_DATABASE_URL = 'postgres://platform:pw@127.0.0.1:5432/platform';
+  process.env.DATABASE_URL = 'postgres://app:pw@127.0.0.1:5432/app';
+  await import('../index.js');
+}, 30_000);
+
+beforeEach(() => {
+  ks.sql.length = 0;
+  ks.updateThrow = undefined;
+  ks.rollbackThrow = undefined;
+  ks.auditThrow = undefined;
+  spy57 = vi.spyOn(console, 'error').mockImplementation(() => undefined);
+});
+
+afterEach(() => {
+  spy57.mockRestore();
+});
+
+const KINDS: Array<[string, () => unknown]> = [
+  ['R1 revoked Proxy', revoked],
+  ['R2 Error whose message getter throws', getterError],
+];
+
+describe.each(KINDS)('KS-1868 DELETE /api/tenants/:id with %s', (_name, make) => {
+  it('RED ks1868 outer: the failed attempt is still audited, logged as a constant reason, and answered with the constant 500', async () => {
+    ks.updateThrow = { value: make() };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id failed: unreadable thrown value');
+    expect(auditWritten()).toBe(true);
+  });
+
+  it('RED ks1868 rollback: a rollback that fails with it is logged as a constant reason and the ORIGINAL error is still the one reported', async () => {
+    ks.updateThrow = { value: new Error('update boom') };
+    ks.rollbackThrow = { value: make() };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id rollback failed: unreadable thrown value');
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id failed: update boom');
+    expect(auditWritten()).toBe(true);
+  });
+
+  it('RED ks1868 audit: an audit write that fails with it is logged as a constant reason and the route still answers the constant 500', async () => {
+    ks.updateThrow = { value: new Error('update boom') };
+    ks.auditThrow = { value: make() };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id could not audit the failure: unreadable thrown value');
+  });
+});
+
+describe('KS-1868 DELETE /api/tenants/:id with ordinary Errors (nothing changes)', () => {
+  it('control ks1868 C1 outer: an ordinary Error is logged with its message, audited, and answered with the constant 500', async () => {
+    ks.updateThrow = { value: new Error('update boom 10.0.0.7') };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(JSON.stringify(res.body)).not.toContain('update boom');
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id failed: update boom 10.0.0.7');
+    expect(auditWritten()).toBe(true);
+  });
+
+  it('control ks1868 C2 rollback: an ordinary rollback Error is logged with its message and the original error is still reported', async () => {
+    ks.updateThrow = { value: new Error('update boom') };
+    ks.rollbackThrow = { value: new Error('rollback boom') };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id rollback failed: rollback boom');
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id failed: update boom');
+  });
+
+  it('control ks1868 C3 audit: an ordinary audit Error is logged with its message and the route answers the constant 500', async () => {
+    ks.updateThrow = { value: new Error('update boom') };
+    ks.auditThrow = { value: new Error('audit boom') };
+    const res = await invoke();
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(CONST500);
+    expect(errLog()).toContain('[provisioning] DELETE /api/tenants/:id could not audit the failure: audit boom');
+  });
+});
```
