# READY — KS-1868-KS-1868-O89-P10 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 04:41 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:41 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/db.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/db.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/originate/src/db.ts
120	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/db.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/db.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts 120 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/db.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the initDb Prisma connection catch resolves and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error', 'KS-1868 the initDb Prisma connection catch resolves and logs text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error', 'KS-1868 the initDb Prisma connection catch resolves and logs text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2334 failed=0 | after: total=2339 failed=0` · `NEW reds: []` [baseline_suite.json total=2334 failed=0; after_suite.json total=2339 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/db.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts` (+120/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/db.ts b/Blockchain/Dev/services/originate/src/db.ts
--- a/Blockchain/Dev/services/originate/src/db.ts
+++ b/Blockchain/Dev/services/originate/src/db.ts
@@ -446,7 +446,14 @@
       await getPrismaClient().$queryRaw`SELECT 1`;
       console.log('[DB] Prisma connection verified (single-tenant mode)');
     } catch (err: any) {
-      console.error('[DB] Prisma connection failed:', err.message);
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      console.error('[DB] Prisma connection failed:', reason);
     }
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts
@@ -0,0 +1,120 @@
+// KS-1868 (operator 89 screen, originate db module): the catch around the Prisma connection check in initDb (line 449) of
+// services/originate/src/db.ts passes `err.message` straight into console.error's arguments, unguarded. A thrown value whose
+// read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw, so initDb REJECTS instead of
+// logging the failure and resolving (the single-tenant boot path carries on and fails per request); an Error whose message is
+// not a string (a Symbol) is handed to console.error uncoerced. The cells make the Prisma connection check reject with such a
+// value and assert initDb resolves and the logged value is text (the constant when the value cannot be turned into text).
+// Harness: the real module with the Prisma client, its adapter, the shared package and the config replaced by plain stand-ins
+// and console.error by a plain recording function (no database, no network).
+const mockH: { failure: { value: unknown } | undefined; errors: unknown[][] } = { failure: undefined, errors: [] };
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    TenantPoolManager: function TenantPoolManagerMock() {
+      return {};
+    },
+    currentTenantId: () => undefined,
+    isPlatformScope: () => false,
+    queryWithTenantGuc: async () => ({ rows: [] }),
+    applyTenantGuc: async () => undefined,
+  }),
+);
+jest.mock('../config', () => ({ config: { databaseUrl: 'postgresql://test:test@localhost:5432/test', nodeEnv: 'test' } }));
+jest.mock('@prisma/client', () => ({
+  PrismaClient: function PrismaClientMock() {
+    return {
+      $queryRaw: async () => {
+        if (mockH.failure) throw mockH.failure.value;
+        return [{ '?column?': 1 }];
+      },
+      $executeRaw: async () => 0,
+      $disconnect: async () => undefined,
+    };
+  },
+}));
+jest.mock('@prisma/adapter-pg', () => ({
+  PrismaPg: function PrismaPgMock() {
+    return {};
+  },
+}));
+
+type Db = typeof import('../db');
+const realError = console.error;
+const realTenancy = process.env.MULTI_TENANCY_ENABLED;
+afterAll(() => {
+  console.error = realError;
+  if (realTenancy === undefined) delete process.env.MULTI_TENANCY_ENABLED;
+  else process.env.MULTI_TENANCY_ENABLED = realTenancy;
+});
+beforeEach(() => {
+  mockH.failure = undefined;
+  mockH.errors.length = 0;
+  delete process.env.MULTI_TENANCY_ENABLED;
+  console.error = (...args: unknown[]) => {
+    mockH.errors.push(args);
+  };
+});
+
+function freshDb(): Db {
+  jest.resetModules();
+  // eslint-disable-next-line @typescript-eslint/no-require-imports
+  return require('../db') as Db;
+}
+async function init(value: unknown): Promise<{ ok: boolean }> {
+  mockH.failure = { value };
+  const db = freshDb();
+  try {
+    await db.initDb();
+    return { ok: true };
+  } catch {
+    return { ok: false };
+  }
+}
+const FAILED = '[DB] Prisma connection failed:';
+const LINES = (): unknown[][] => mockH.errors.filter((a) => a[0] === FAILED);
+/** The logged second argument as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (a: unknown[] | undefined): string => (typeof a?.[1] === 'string' ? (a[1] as string) : '<' + typeof a?.[1] + '>');
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
+describe('KS-1868 the initDb Prisma connection catch resolves and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the Prisma connection check leaves initDb resolving and is logged with its message', async () => {
+    expect(await init(new Error('prisma down'))).toEqual({ ok: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('prisma down');
+  });
+  it('control ks1868 C2: a thrown number from the Prisma connection check leaves initDb resolving and is logged without a message', async () => {
+    expect(await init(42)).toEqual({ ok: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(revokedProxy())).toEqual({ ok: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(getterThrows())).toEqual({ ok: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol from the Prisma connection check leaves initDb resolving and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(withMessage(Symbol('ks1868')))).toEqual({ ok: true });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+});
```
