# READY — KS-1868-KS-1868-O87-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 01:48 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:48 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/db.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/db.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/auth/src/db.ts
159	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/db.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/db.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts 159 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/db.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy reaching the pool listener does not throw and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol reaching the pool listener does not throw and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value RED ks1868 R3: a migration failure that is a revoked Proxy leaves initDb resolving true with every statement attempted and logged as text', 'KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value RED ks1868 R4: a migration failure that is an Error whose message getter throws leaves initDb resolving true with every statement attempted and logged as text', 'KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value RED ks1868 R5: a migration failure that is an Error whose message is a Symbol leaves initDb resolving true with every statement attempted and logged as text']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1536 failed=0 | after: total=1545 failed=0` · `NEW reds: []` [baseline_suite.json total=1536 failed=0; after_suite.json total=1545 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/db.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts` (+159/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p2_auth_db_pool_error_and_migration_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/db.ts b/Blockchain/Dev/services/auth/src/db.ts
--- a/Blockchain/Dev/services/auth/src/db.ts
+++ b/Blockchain/Dev/services/auth/src/db.ts
@@ -40,5 +40,12 @@
     pool.on('error', (err: Error) => {
-      logger.error('DB pool unexpected error', { error: err.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB pool unexpected error', { error: reason });
     });
   }
   return pool;
@@ -157,7 +164,14 @@
       await getPool().query(sql);
     } catch (err: any) {
       // Ignore errors (e.g., table doesn't exist yet, or constraint issues)
-      logger.debug('Column migration skipped', { sql: sql.substring(0, 60), error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.debug('Column migration skipped', { sql: sql.substring(0, 60), error: reason });
     }
   }
   logger.info('User column migrations applied');
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts
@@ -0,0 +1,159 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 87 screen, auth db module): the pg pool 'error' listener (line 41) and the best-effort column-migration
+// catch of ensureUserColumns (line 160) of services/auth/src/db.ts pass `err.message` / `err?.message` straight into the
+// logger's meta object, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws)
+// makes the listener / the catch itself throw: an exception thrown by a listener of the pool's 'error' event escapes the
+// EventEmitter and is an uncaught exception, and a throwing migration catch abandons the remaining migrations and makes
+// initDb REJECT; an Error whose message is not a string (a Symbol) is handed to the logger uncoerced. The cells emit such a
+// value to the captured listener / make every migration statement reject with it and assert the listener returns, initDb
+// resolves with the same statements attempted as for an ordinary Error, and the logged value is text (the constant when the
+// value cannot be turned into text). Harness: the real module with pg replaced by a plain stand-in Pool, @secuura/shared
+// replaced by plain pass-through stand-ins and the service logger replaced by a plain recording object (no database).
+const h = vi.hoisted(() => ({
+  listener: undefined as undefined | ((e: unknown) => void),
+  ddlFailure: undefined as undefined | { value: unknown },
+  ddlAttempts: 0,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: async (sql: string) => {
+        if (sql.indexOf('SELECT 1') === 0) return { rows: [{ ok: 1 }] };
+        if (sql.indexOf('SELECT has_schema_privilege') === 0) return { rows: [{ ok: true }] };
+        h.ddlAttempts += 1;
+        if (h.ddlFailure) throw h.ddlFailure.value;
+        return { rows: [] };
+      },
+      on: (event: string, fn: (e: unknown) => void) => {
+        if (event === 'error') h.listener = fn;
+      },
+      end: async () => undefined,
+      connect: async () => undefined,
+    };
+  },
+}));
+vi.mock('@secuura/shared', () => ({
+  applyTenantGuc: async () => undefined,
+  runWithTenantId: (_id: string, fn: () => unknown) => fn(),
+  queryWithTenantGuc: (pool: { query: (s: string, p?: unknown[]) => Promise<unknown> }, text: string, params?: unknown[]) =>
+    pool.query(text, params),
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Db = typeof import('../db');
+const realUrl = process.env.DATABASE_URL;
+afterAll(() => {
+  if (realUrl === undefined) delete process.env.DATABASE_URL;
+  else process.env.DATABASE_URL = realUrl;
+});
+beforeEach(() => {
+  h.listener = undefined;
+  h.ddlFailure = undefined;
+  h.ddlAttempts = 0;
+  h.logs.length = 0;
+  process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
+});
+
+async function freshDb(): Promise<Db> {
+  vi.resetModules();
+  return import('../db');
+}
+async function emit(value: unknown): Promise<{ threw: boolean }> {
+  const db = await freshDb();
+  db.getPool();
+  try {
+    (h.listener as (e: unknown) => void)(value);
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+async function migrate(value: unknown): Promise<{ ok: boolean; value: boolean | undefined }> {
+  h.ddlFailure = { value };
+  const db = await freshDb();
+  try {
+    return { ok: true, value: await db.initDb() };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINE = (message: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  h.logs.filter((l) => l.message === message);
+const POOL = 'DB pool unexpected error';
+const SKIPPED = 'Column migration skipped';
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string =>
+  typeof l?.meta?.error === 'string' ? (l.meta.error as string) : '<' + typeof l?.meta?.error + '>';
+/** Every migration statement was attempted and each failure was logged once, all with the same text. */
+function expectAllSkipped(expected: string): void {
+  expect(h.ddlAttempts).toBeGreaterThan(10);
+  expect(LINE(SKIPPED)).toHaveLength(h.ddlAttempts);
+  expect(new Set(LINE(SKIPPED).map((l) => reasonOf(l)))).toEqual(new Set([expected]));
+}
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the pool error listener and the migration catch survive and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error reaching the pool listener does not throw and is logged with its message', async () => {
+    expect(await emit(new Error('pool boom'))).toEqual({ threw: false });
+    expect(LINE(POOL)).toHaveLength(1);
+    expect(reasonOf(LINE(POOL)[0])).toBe('pool boom');
+  });
+  it('control ks1868 C2: a plain string reaching the pool listener does not throw and is logged without a message', async () => {
+    expect(await emit('plain boom')).toEqual({ threw: false });
+    expect(LINE(POOL)).toHaveLength(1);
+    expect(reasonOf(LINE(POOL)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an ordinary Error from every migration statement leaves initDb resolving true and each failure is logged with its message', async () => {
+    expect(await migrate(new Error('ddl boom'))).toEqual({ ok: true, value: true });
+    expectAllSkipped('ddl boom');
+  });
+  it('control ks1868 C4: a thrown number from every migration statement leaves initDb resolving true and each failure is logged without a message', async () => {
+    expect(await migrate(42)).toEqual({ ok: true, value: true });
+    expectAllSkipped('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy reaching the pool listener does not throw and is logged as text, as for an ordinary Error', async () => {
+    expect(await emit(revokedProxy())).toEqual({ threw: false });
+    expect(LINE(POOL)).toHaveLength(1);
+    expect(reasonOf(LINE(POOL)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol reaching the pool listener does not throw and is logged as text, as for an ordinary Error', async () => {
+    expect(await emit(withMessage(Symbol('ks1868')))).toEqual({ threw: false });
+    expect(LINE(POOL)).toHaveLength(1);
+    expect(reasonOf(LINE(POOL)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: a migration failure that is a revoked Proxy leaves initDb resolving true with every statement attempted and logged as text', async () => {
+    expect(await migrate(revokedProxy())).toEqual({ ok: true, value: true });
+    expectAllSkipped('unreadable thrown value');
+  });
+  it('RED ks1868 R4: a migration failure that is an Error whose message getter throws leaves initDb resolving true with every statement attempted and logged as text', async () => {
+    expect(await migrate(getterThrows())).toEqual({ ok: true, value: true });
+    expectAllSkipped('unreadable thrown value');
+  });
+  it('RED ks1868 R5: a migration failure that is an Error whose message is a Symbol leaves initDb resolving true with every statement attempted and logged as text', async () => {
+    expect(await migrate(withMessage(Symbol('ks1868')))).toEqual({ ok: true, value: true });
+    expectAllSkipped('Symbol(ks1868)');
+  });
+});
```
