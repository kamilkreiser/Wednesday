# READY — KS-1128-KS-1128 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 10:33 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:33 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/startup-migrations.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	1	Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
80	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/startup-migrations.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1128: a platform tenant seed that cannot seed says so at WARN RED KS-1128 - a refused platform seed is a WARN that names it FAILED on the platform DB', 'KS-1128: a platform tenant seed that cannot seed says so at WARN RED KS-1128 - the refused seed line carries the error text up to 200 characters, not cut at 80']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=750 failed=0 | after: total=754 failed=0` · `NEW reds: []` [baseline_suite.json total=750 failed=0; after_suite.json total=754 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +83/-1 test=src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (+3/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts` (+80/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1128-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
+++ b/Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
@@ -1145,6 +1145,8 @@ export async function runStartupMigrations(): Promise<void> {
         log('info', 'Platform tenant seed complete (Secuura Co. + 5 client tenants + config)');
       } catch (seedErr: any) {
-        log('debug', 'Platform tenant seed skipped', { error: seedErr?.message?.substring(0, 80) });
+        // KS-1128: warn, not debug, in the shape of the main-DB arm (KS-950): a seed that cannot seed
+        // reports at a level the demo reads, names itself a failure, and keeps 200 characters of the error.
+        log('warn', 'Platform tenant seed FAILED (platform DB)', { error: seedErr?.message?.substring(0, 200) });
       } finally {
         await pSeedPool.end();
       }
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts
@@ -0,0 +1,80 @@
+/**
+ * KS-1128: the platform tenant seed in runStartupMigrations() (startup-migrations.ts, the pSeedPool block)
+ * catches its own failure and logs it at DEBUG as skipped, with the error cut to 80 characters, so a seed
+ * that cannot seed reports into a level the demo does not read (the KS-962 class on the platform-DB path).
+ * runStartupMigrations() is called DIRECTLY with pg redirected, ONLY for the product file, to the fake Pool
+ * below (the ks1062 idiom); the control cell proves the redirect and the clean path before any cell is believed.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import * as fs from 'fs';
+import * as os from 'os';
+import * as path from 'path';
+import Module from 'module';
+const PRODUCT = path.join(__dirname, '..', 'startup-migrations.ts');
+const SCRATCH = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1128-'));
+const FAKE = path.join(SCRATCH, 'fake-pg.cjs');
+const EMPTY_MIGRATIONS_DIR = path.join(SCRATCH, 'migrations');
+const SEED_INSERT = 'INSERT INTO tenants (id, name, slug';
+const LONG_ERROR = 'ks1128 platform seed refused: ' + 'x'.repeat(120);
+let refuseSeed = false;
+let lines: string[] = [];
+let product: { runStartupMigrations: () => Promise<void> };
+const origResolve = (Module as any)._resolveFilename;
+/** No I/O. With refuseSeed set, the platform tenant seed INSERT throws LONG_ERROR; every other statement succeeds. */
+class FakePool {
+  async query(text: string): Promise<{ rows: unknown[]; rowCount: number }> {
+    if (refuseSeed && String(text).includes(SEED_INSERT)) throw new Error(LONG_ERROR);
+    return { rows: [], rowCount: 0 };
+  }
+  async end(): Promise<void> { /* nothing to close */ }
+}
+async function boot(refuse: boolean): Promise<void> {
+  refuseSeed = refuse;
+  lines = [];
+  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { lines.push(a.map(String).join(' ')); });
+  try { await product.runStartupMigrations(); } finally { spy.mockRestore(); }
+}
+const seedLine = () => lines.find((l) => l.includes('[startup-migrations] Platform tenant seed')) || '';
+const metaOf = (line: string) => JSON.parse(line.indexOf('{') < 0 ? '{}' : line.slice(line.indexOf('{')));
+beforeAll(async () => {
+  fs.mkdirSync(EMPTY_MIGRATIONS_DIR);
+  fs.writeFileSync(FAKE, 'module.exports = globalThis.__KS1128_FAKE_PG;');
+  (globalThis as any).__KS1128_FAKE_PG = { Pool: FakePool };
+  (Module as any)._resolveFilename = function (request: string, parent: any, ...rest: unknown[]) {
+    if (request === 'pg' && parent && parent.filename === PRODUCT) return FAKE;
+    return origResolve.call(this, request, parent, ...rest);
+  };
+  vi.stubEnv('DATABASE_URL', 'postgresql://qauser:qapass@qa-main.invalid:5432/qa_main');
+  vi.stubEnv('PLATFORM_DATABASE_URL', 'postgresql://qauser:qapass@qa-platform.invalid:5432/qa_platform');
+  vi.stubEnv('MULTI_TENANCY_ENABLED', 'false');
+  vi.stubEnv('MIGRATIONS_DIR', EMPTY_MIGRATIONS_DIR);
+  delete process.env.MIGRATION_DATABASE_URL;
+  delete process.env.MIGRATION_PLATFORM_DATABASE_URL;
+  delete process.env.APP_DB_PASSWORD;
+  product = await import('../startup-migrations');
+});
+afterAll(() => {
+  (Module as any)._resolveFilename = origResolve;
+  vi.unstubAllEnvs();
+  fs.rmSync(SCRATCH, { recursive: true, force: true });
+});
+describe('KS-1128: a platform tenant seed that cannot seed says so at WARN', () => {
+  it('CONTROL - pg resolves to the fake, and a clean run logs the platform seed at INFO as complete', async () => {
+    expect(Module.createRequire(PRODUCT).resolve('pg')).toBe(FAKE);
+    await boot(false);
+    expect(seedLine().startsWith('[INFO] [startup-migrations] Platform tenant seed complete')).toBe(true);
+  });
+  it('RED KS-1128 - a refused platform seed is a WARN that names it FAILED on the platform DB', async () => {
+    await boot(true);
+    expect(seedLine().split(' {')[0]).toBe('[WARN] [startup-migrations] Platform tenant seed FAILED (platform DB)');
+  });
+  it('RED KS-1128 - the refused seed line carries the error text up to 200 characters, not cut at 80', async () => {
+    await boot(true);
+    expect(metaOf(seedLine()).error).toBe(LONG_ERROR);
+  });
+  it('CONTROL - a refused seed does not escape: the platform migrations still read complete and nothing else fails', async () => {
+    await boot(true);
+    expect(lines.some((l) => l.startsWith('[INFO] [startup-migrations] Platform DB migrations complete'))).toBe(true);
+    expect(lines.filter((l) => l.includes('Platform DB migrations failed'))).toEqual([]);
+  });
+});
```
