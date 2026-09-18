# READY — KS-1125 (Ornith, briefed, TEST-ONLY) — PASS 7/7 on the harness retry, HELD for QA

**Held 2026-09-18 11:0x by the 10:0x Wednesday seat, after a source read** (below). This isn't a bare checker pass.

| field | value |
|---|---|
| ticket | KS-1125: api-gateway startup-migrations tenant-failure guard `if (outcome.failed > 0)` has no cell |
| run | `runs/2026-09-18_ks1125-ornith35b-night` (**the pass is `retry/`**) |
| mode | **TEST-ONLY**: one new test file; the product file is **untouched** (A3 proves it) |
| tamper | `startup-migrations.ts:1189` `if (outcome.failed > 0) {` → `if (false) {` (the KS-1062 defect restored), reverted after |
| tip | develop `a105cd32b1ed9c6927ae6e797f8259224d8480c6` |
| size | 1 file, +104/-0 |
| verdict | **PASS (7/7)**, `red_first=yes`, `apply_mode=lenient` (the hunk count needed `--recount`, which is harmless for a new file) |

## ⚠ It passed on the RETRY, not the first attempt
The first attempt **FAILED at A2b (placeholder test file)**: the model produced a stub, not a test. The harness's
automatic retry produced this pass. **Record it as "passed on retry"**, because that is the honest
success rate.

## Why this one worked: the reachability rule held
The cell calls the exported `runStartupMigrations()` **directly**: no HTTP, no `index.ts`, no middleware. That's
the rule from KS-1222's failure (a red with a red control at the tip means the harness never reached the
code). **Briefed runs today: KS-1233 PASS · KS-1222 FAIL (unreachable) · KS-1125 PASS on retry. Brief-less runs this morning: 0 of 4.**

## My own source read
- **The test matches the brief.** The control runs FIRST and asserts two things: that the product resolves `pg` to the fake,
  so the redirect genuinely took and the file can't pass vacuously; and that two healthy tenants give
  `{migrated:2, failed:0, skipped:0, total:2}`. The red cell uses seven healthy tenants plus one missing database and asserts
  `[{migrated:7, failed:1, skipped:0, total:8}, 1]` (exactly one FAILED line naming the ghost).
- **The resolver patch is safe.** It overrides `Module._resolveFilename` but (a) redirects **only** when
  `request === 'pg'` AND the parent is the product file, and (b) restores the original in `afterAll`. So it can't
  leak into other test files running in the same worker. **I checked this specifically**, because an unrestored global patch
  is the classic way a passing new test reddens someone else's suite later. A6 (no new red across the whole suite) agrees.
- **Residual risk named in the brief, and it held:** the redirect was measured under vitest 4.1.10 and the tip has 4.1.11.
  The control would have gone red first if it had broken. It didn't.

## Status
**HELD.** Not raised, not gated, not merged. Under the TESTED grant, a merge needs a QA gate at head plus my signed GO.
**Closes KS-1125** is correct *for this ticket* (it asks for exactly this one cell), unlike PR-level closing
phrases on partially-measured work.

---
## The diff, verbatim (from `retry/out.md`)

```diff
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1125-api-gateway-startup-migrations-the-tenant.test.ts
@@ -0,0 +1,136 @@
+/**
+ * =============================================================================
+ * KS-1125 - the tenant-failure guard in startup-migrations has a cell
+ * =============================================================================
+ * KS-1062 (#932) counts a tenant as migrated only when migrateDatabase reports
+ * zero failed statements (startup-migrations.ts, if (outcome.failed > 0)).
+ * With that guard reverted the repository suite stayed green (#932 gate, T1).
+ *
+ * runStartupMigrations() is called DIRECTLY. Its bare require('pg') is not
+ * reached by vi.mock, so pg is redirected at Node's resolver, ONLY for the
+ * product file, to a fake Pool defined below. The CONTROL cell proves the
+ * redirect took effect before the red cell is believed.
+ * =============================================================================
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import * as fs from 'fs';
+import * as os from 'os';
+import * as path from 'path';
+import Module from 'module';
+
+const PRODUCT = path.join(__dirname, '..', 'startup-migrations.ts');
+const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1125-'));
+const FAKE = path.join(SCRATCH, 'fake-pg.cjs');
+const EMPTY_MIGRATIONS_DIR = path.join(SCRATCH, 'migrations');
+const TENANT_SCAN = 'FROM tenants t LEFT JOIN tenant_config tc';
+
+const REC = { pools: [] as string[] };
+let TENANTS: Array<Record<string, unknown>> = [];
+let MISSING = new Set<string>();
+let lines: string[] = [];
+let product: { runStartupMigrations: () => Promise<void> };
+const origResolve = (Module as any)._resolveFilename;
+
+function dbOf(connStr: string): string {
+  try { return new URL(connStr).pathname.replace(/^\//, ''); } catch { return '?'; }
+}
+
+/** The fake pg.Pool: no I/O. A database in MISSING rejects every statement; the tenant scan answers TENANTS. */
+class FakePool {
+  private db: string;
+  constructor(opts: { connectionString: string }) {
+    this.db = dbOf(opts.connectionString);
+    REC.pools.push(this.db);
+  }
+  async query(text: string): Promise<{ rows: unknown[]; rowCount: number }> {
+    if (MISSING.has(this.db)) throw new Error('database "' + this.db + '" does not exist');
+    if (String(text).includes(TENANT_SCAN)) return { rows: TENANTS, rowCount: TENANTS.length };
+    return { rows: [], rowCount: 0 };
+  }
+  async end(): Promise<void> { /* nothing to close */ }
+}
+
+const tenant = (n: number) => ({ id: 't-' + n, slug: 'tenant-' + n, db_name: 'qa_t' + n, db_host: null, db_port: null });
+const GHOST = { id: 't-ghost', slug: 'ks1125-ghost', db_name: 'tenant_does_not_exist', db_host: null, db_port: null };
+
+async function boot(tenants: Array<Record<string, unknown>>, missing: string[]): Promise<void> {
+  TENANTS = tenants;
+  MISSING = new Set(missing);
+  REC.pools.length = 0;
+  lines = [];
+  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { lines.push(a.map(String).join(' ')); });
+  try { await product.runStartupMigrations(); } finally { spy.mockRestore(); }
+}
+
+const tenantSummary = () => lines.find((l) => l.includes('[startup-migrations] Tenant DB migrations'));
+const summaryJson = () => JSON.parse((tenantSummary() || '{}').replace(/^[^{]*/, ''));
+const failedTenantLines = () => lines.filter((l) => l.includes('Tenant ks1125-ghost migrations FAILED'));
+
+beforeAll(async () => {
+  fs.mkdirSync(EMPTY_MIGRATIONS_DIR);
+  fs.writeFileSync(FAKE, 'module.exports = globalThis.__KS1125_FAKE_PG;\n');
+  (globalThis as any).__KS1125_FAKE_PG = { Pool: FakePool };
+  (Module as any)._resolveFilename = function (request: string, parent: any, ...rest: unknown[]) {
+    if (request === 'pg' && parent && parent.filename === PRODUCT) return FAKE;
+    return origResolve.call(this, request, parent, ...rest);
+  };
+  vi.stubEnv('DATABASE_URL', 'postgresql://qauser:qapass@qa-main.invalid:5432/qa_main');
+  vi.stubEnv('PLATFORM_DATABASE_URL', 'postgresql://qauser:qapass@qa-platform.invalid:5432/qa_platform');
+  vi.stubEnv('MULTI_TENANCY_ENABLED', 'true');
+  vi.stubEnv('MIGRATIONS_DIR', EMPTY_MIGRATIONS_DIR);
+  delete process.env.MIGRATION_DATABASE_URL;
+  delete process.env.MIGRATION_PLATFORM_DATABASE_URL;
+  delete process.env.APP_DB_PASSWORD;
+  product = await import('../startup-migrations');
+});
+
+afterAll(() => {
+  (Module as any)._resolveFilename = origResolve;
+  vi.unstubAllEnvs();
+  fs.rmSync(SCRATCH, { recursive: true, force: true });
+});
+
+describe('KS-1125: a tenant whose migrations fail is counted as FAILED, never as migrated', () => {
+  it('control: the product resolves pg to the fake, and two healthy tenants are both counted migrated', async () => {
+    expect(Module.createRequire(PRODUCT).resolve('pg')).toBe(FAKE);
+    await boot([tenant(1), tenant(2)], []);
+    expect([REC.pools.includes('qa_t1'), REC.pools.includes('qa_t2'), summaryJson()]).toEqual([true, true, { migrated: 2, failed: 0, skipped: 0, total: 2 }]);
+  });
+
+  it('\ud83d\udd34 seven healthy tenants and one ghost database: migrated 7, failed 1, and one FAILED line names the ghost', async () => {
+    await boot([tenant(1), tenant(2), tenant(3), GHOST, tenant(4), tenant(5), tenant(6), tenant(7)], ['tenant_does_not_exist']);
+    expect([summaryJson(), failedTenantLines().length]).toEqual([{ migrated: 7, failed: 1, skipped: 0, total: 8 }, 1]);
+  });
+});
```
