# READY — KS-1272 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1272-ornith35b-night/out.md.checker/patch.diff`** (from `ls` of that dir at 22:16 2026-09-20). Strict `git apply --numstat` → `1 1 …startup-migrations.ts` + `85 0 …ks1272-platform-dedup-uuid-tenant-id.test.ts`.

**Held 22:16 2026-09-20 by the 21:2x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. TWO files: ONE product line changed in `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` + ONE new test file. **`Refs KS-1272`, never a closing word** — the ticket's third item (which declaration of `tenant_id` is canonical, TEXT in the in-code CREATE vs UUID in `docker/init-platform/01-platform-schema.sql`) is a ruling, not briefed.

**What it fixes.** Every api-gateway boot against a platform DB whose `platform_document_registry.tenant_id` is `uuid` logs `Migration FAILED on platform {"error":"invalid input syntax for type uuid: \"\""}` because the KS-39 #4 de-dup DELETE compares `COALESCE(a.tenant_id, '')`. The fix is the ticket's own: `a.tenant_id IS NOT DISTINCT FROM b.tenant_id` — type-agnostic, NULL = NULL.

**Scope, narrowed on purpose and enforced by a control cell:** the SAME statement exists twice — `:473` (CORE_MIGRATIONS, the MAIN db, 5-space indent) and `:1077` (platformMigrations, 11-space indent). **Only `:1077` changes.** On the main DB the column is TEXT and `COALESCE(x,'')=COALESCE(y,'')` treats NULL and '' as equal where `IS NOT DISTINCT FROM` does not — changing 473 alters which rows a DELETE removes, outside this ticket's BLUF. CONTROL 2 in the test pins that CORE_MIGRATIONS still holds exactly one `COALESCE(a.tenant_id, '')`.

**Source read (Wednesday, in the same action as this file):** the patch's ONE product `-`/`+` pair sits in hunk `@@ -1074,7 +1074,7 @@` (line 1077) and the `+` line is byte-identical to the brief's; `grep -c` for a `+`/`-` on the 5-space form = 0 beside a positive 1 on the expected line in the same file. Test file 85 lines = the brief's verbatim design (ks1062/ks1125 FakePool idiom: pg redirected only for the product file; `qa_platform_uuid` fake throws the ticket's 22P02 text on any `COALESCE(a.tenant_id, '')`).

**Cells (full vitest titles in the run's `green_tip.cells.json`):** 🔴 the platform summary must read `complete {applied:7, failed:0}` (red at tip: `[false,{applied:6,failed:1}]`); CONTROL 1 a planted refusal of the `uq_pdr_hash_tenant` statement is counted `INCOMPLETE {6,1}` (proves the fake fires and the counter sees it); CONTROL 2 the main list still holds exactly one `COALESCE(a.tenant_id, '')` and its summary is `failed:0` (pins 473).

**Checker verdict (run 2026-09-20 22:1x):** `RESULT: PASS (7/7)`; A4 1/3 assertion red at tip; A6 suite 674 → 677, NEW reds `[]`; A7 tsc rc 0. **Drafter's pre-queue measurements (scratch clone at the tip, 22:00–22:10):** tip 1 failed/3, fix 3/3, suite 674/674 → 677/677, tsc rc 0 both; wrong variants refused by the REAL checker at named gates — `sqlcomment` A3c, `coalesce_text` A3c, `only473` A3i (indent shift 5 vs 11), `both` A5+A6 (control 2 red).

**For the raise seat:** apply the canonical patch STRICT (it is correctly counted); run the api-gateway vitest suite at the tip and after (677 expected); `Refs KS-1272`; PR body states the 473 narrowing and the unbriefed canonical-declaration item as NOT DONE. **Partition tonight:** this file is disjoint from Seat B 10th's two test files and its `enforcement.ts` tamper, and from Seat A 15th's `services/anchoring/**`.

**NOT TESTED:** a real Postgres (the fake reproduces 22P02 by matching the ticket's quoted text); the kintsugi log itself; `docker/init-platform/01-platform-schema.sql` is untouched.

---
--- a/Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
+++ b/Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
@@ -1074,7 +1074,7 @@ export async function runStartupMigrations(): Promise<void> {
         // UNIQUE index the verification.ts ON CONFLICT clause errors.
         `DELETE FROM platform_document_registry a USING platform_document_registry b
          WHERE a.id > b.id AND a.content_hash = b.content_hash
-           AND COALESCE(a.tenant_id, '') = COALESCE(b.tenant_id, '')`,
+           AND a.tenant_id IS NOT DISTINCT FROM b.tenant_id`,
         `CREATE UNIQUE INDEX IF NOT EXISTS uq_pdr_hash_tenant ON platform_document_registry(content_hash, tenant_id)`,
         `CREATE TABLE IF NOT EXISTS platform_document_type_templates (
           id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1272-platform-dedup-uuid-tenant-id.test.ts
@@ -0,0 +1,85 @@
+/**
+ * KS-1272 - the platform-DB de-dup DELETE in startup-migrations fails 22P02 on every boot where
+ * platform_document_registry.tenant_id is uuid (docker/init-platform/01-platform-schema.sql declares it so):
+ * the statement compares COALESCE(a.tenant_id, ''), and '' cannot be cast to uuid, so the gateway logs
+ * "Migration FAILED on platform" and "Platform DB migrations INCOMPLETE - 1 FAILED" at every boot.
+ * runStartupMigrations() is called DIRECTLY with pg redirected, ONLY for the product file, to the fake Pool
+ * below (the ks1062 / ks1125 idiom); the fake behaves like a uuid-typed platform database: it refuses any
+ * statement that coalesces tenant_id with ''. The controls prove the redirect, prove that ONE refused platform
+ * statement is exactly what the platform summary counts, and pin that the MAIN list is not touched.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import * as fs from 'fs';
+import * as os from 'os';
+import * as path from 'path';
+import Module from 'module';
+const PRODUCT = path.join(__dirname, '..', 'startup-migrations.ts');
+const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1272-'));
+const FAKE = path.join(SCRATCH, 'fake-pg.cjs');
+const EMPTY_MIGRATIONS_DIR = path.join(SCRATCH, 'migrations');
+const PLATFORM_URL_BASE = 'postgresql://qauser:qapass@qa-platform.invalid:5432/';
+/** What a uuid-typed tenant_id column refuses: the empty string cannot be cast to uuid. */
+const UUID_COALESCE = "COALESCE(a.tenant_id, '')";
+const UNIQUE_INDEX = 'CREATE UNIQUE INDEX IF NOT EXISTS uq_pdr_hash_tenant';
+let lines: string[] = [];
+let product: { runStartupMigrations: () => Promise<void>; CORE_MIGRATIONS: string[] };
+const origResolve = (Module as any)._resolveFilename;
+function dbOf(connStr: string): string {
+  try { return new URL(connStr).pathname.replace(/^\//, ''); } catch { return '?'; }
+}
+/** No I/O. qa_platform_uuid is a platform database whose tenant_id is uuid; qa_platform_index refuses one other statement. */
+class FakePool {
+  private db: string;
+  constructor(opts: { connectionString: string }) { this.db = dbOf(opts.connectionString); }
+  async query(text: string): Promise<{ rows: unknown[]; rowCount: number }> {
+    if (this.db === 'qa_platform_uuid' && String(text).includes(UUID_COALESCE)) throw new Error('invalid input syntax for type uuid: ""');
+    if (this.db === 'qa_platform_index' && String(text).includes(UNIQUE_INDEX)) throw new Error('qa planted refusal of the unique index');
+    return { rows: [], rowCount: 0 };
+  }
+  async end(): Promise<void> { /* nothing to close */ }
+}
+async function boot(platformDb: string): Promise<void> {
+  lines = [];
+  vi.stubEnv('PLATFORM_DATABASE_URL', PLATFORM_URL_BASE + platformDb);
+  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { lines.push(a.map(String).join(' ')); });
+  try { await product.runStartupMigrations(); } finally { spy.mockRestore(); }
+}
+const platformSummary = () => lines.find((l) => l.includes('[startup-migrations] Platform DB migrations')) || '';
+const mainSummary = () => lines.find((l) => l.includes('[startup-migrations] Main DB migrations')) || '';
+const metaOf = (line: string) => JSON.parse(line.replace(/^[^{]*/, '') || '{}');
+beforeAll(async () => {
+  fs.mkdirSync(EMPTY_MIGRATIONS_DIR);
+  fs.writeFileSync(FAKE, 'module.exports = globalThis.__KS1272_FAKE_PG;\n');
+  (globalThis as any).__KS1272_FAKE_PG = { Pool: FakePool };
+  (Module as any)._resolveFilename = function (request: string, parent: any, ...rest: unknown[]) {
+    if (request === 'pg' && parent && parent.filename === PRODUCT) return FAKE;
+    return origResolve.call(this, request, parent, ...rest);
+  };
+  vi.stubEnv('DATABASE_URL', 'postgresql://qauser:qapass@qa-main.invalid:5432/qa_main');
+  vi.stubEnv('MIGRATIONS_DIR', EMPTY_MIGRATIONS_DIR);
+  delete process.env.MIGRATION_DATABASE_URL;
+  delete process.env.MIGRATION_PLATFORM_DATABASE_URL;
+  delete process.env.MULTI_TENANCY_ENABLED;
+  delete process.env.APP_DB_PASSWORD;
+  product = await import('../startup-migrations');
+});
+afterAll(() => {
+  (Module as any)._resolveFilename = origResolve;
+  vi.unstubAllEnvs();
+  fs.rmSync(SCRATCH, { recursive: true, force: true });
+});
+describe('KS-1272: the platform de-dup DELETE on a uuid-typed tenant_id', () => {
+  it('control: pg resolves to the fake, and ONE refused platform statement (the unique index) is what the platform summary counts as 1 FAILED', async () => {
+    expect(Module.createRequire(PRODUCT).resolve('pg')).toBe(FAKE);
+    await boot('qa_platform_index');
+    expect([platformSummary().startsWith('[WARN] [startup-migrations] Platform DB migrations INCOMPLETE '), metaOf(platformSummary())]).toEqual([true, { applied: 6, failed: 1 }]);
+  });
+  it('control: the MAIN list keeps exactly one COALESCE de-dup on tenant_id (NULL and empty equal on its TEXT column) and the main summary is complete', async () => {
+    await boot('qa_platform_index');
+    expect([product.CORE_MIGRATIONS.filter((s) => s.includes(UUID_COALESCE)).length, mainSummary().startsWith('[INFO] [startup-migrations] Main DB migrations complete '), metaOf(mainSummary()).failed]).toEqual([1, true, 0]);
+  });
+  it('🔴 KS-1272: on a platform database whose tenant_id is uuid, the de-dup DELETE is accepted and the platform summary is complete with 0 FAILED', async () => {
+    await boot('qa_platform_uuid');
+    expect([platformSummary().startsWith('[INFO] [startup-migrations] Platform DB migrations complete '), metaOf(platformSummary())]).toEqual([true, { applied: 7, failed: 0 }]);
+  });
+});
