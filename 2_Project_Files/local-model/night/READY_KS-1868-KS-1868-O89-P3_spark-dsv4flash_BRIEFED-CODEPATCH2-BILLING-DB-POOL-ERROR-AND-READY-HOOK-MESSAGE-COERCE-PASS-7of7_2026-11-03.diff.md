# READY — KS-1868-KS-1868-O89-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 03:58 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 03:58 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/db.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/db.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/billing/src/db.ts
153	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/db.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/db.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts 153 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/db.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy reaching the pool listener does not throw and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol reaching the pool listener does not throw and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value RED ks1868 R3: an onReady hook failure that is a revoked Proxy leaves initDb resolving true and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value RED ks1868 R4: an onReady hook failure that is an Error whose message getter throws leaves initDb resolving true and is logged as text, as for an ordinary Error', 'KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value RED ks1868 R5: an onReady hook failure that is an Error whose message is a Symbol leaves initDb resolving true and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=365 failed=0 | after: total=374 failed=0` · `NEW reds: []` [baseline_suite.json total=365 failed=0; after_suite.json total=374 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/db.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts` (+153/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o89_q3_billing_db_pool_error_and_ready_hook_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/db.ts b/Blockchain/Dev/services/billing/src/db.ts
--- a/Blockchain/Dev/services/billing/src/db.ts
+++ b/Blockchain/Dev/services/billing/src/db.ts
@@ -32,5 +32,12 @@
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
@@ -77,6 +84,13 @@
     await onDbReady();
   } catch (err: any) {
     // Boot work failing must not un-flag an otherwise reachable DB.
-    logger.error('DB ready boot work failed', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB ready boot work failed', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts
@@ -0,0 +1,153 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 86 screen, billing db module): the pg pool 'error' listener (line 33) and the boot-work catch of
+// runDbReadyHook (line 80) of services/billing/src/db.ts pass `err.message` / `err?.message` straight into logger.error's meta
+// object, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the
+// listener / the catch itself throw: an exception thrown by a listener of the pool's 'error' event escapes the EventEmitter
+// and is an uncaught exception, and a throwing runDbReadyHook makes initDb REJECT instead of resolving with the availability
+// flag; an Error whose message is not a string (a Symbol) is handed to JSON.stringify uncoerced and silently dropped from the
+// line. The cells emit such a value to the captured listener / make the onReady hook reject with it and assert the listener
+// returns, initDb resolves and the line carries text (the constant when the value cannot be turned into text). Harness: the
+// real module with pg replaced by a plain stand-in Pool (it hands over the 'error' listener; its query answers the probe) and
+// console.log replaced by a plain recording function (no database).
+const h = vi.hoisted(() => ({
+  listener: undefined as undefined | ((e: unknown) => void),
+  lines: [] as string[],
+  calls: [] as { message: string; meta: unknown }[],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    error: (message: string, meta?: unknown) => {
+      h.calls.push({ message, meta });
+    },
+    warn: () => undefined,
+    info: () => undefined,
+    debug: () => undefined,
+  },
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: async () => ({ rows: [{ ok: 1 }] }),
+      on: (event: string, fn: (e: unknown) => void) => {
+        if (event === 'error') h.listener = fn;
+      },
+      end: async () => undefined,
+      connect: async () => undefined,
+    };
+  },
+}));
+
+vi.mock('@secuura/shared', () => ({ queryWithTenantGuc: async () => ({ rows: [{ ok: 1 }] }) }));
+
+type Db = typeof import('../db');
+const realUrl = process.env.DATABASE_URL;
+afterAll(() => {
+  if (realUrl === undefined) delete process.env.DATABASE_URL;
+  else process.env.DATABASE_URL = realUrl;
+});
+beforeEach(() => {
+  h.listener = undefined;
+  h.calls.length = 0;
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
+async function hook(value: unknown): Promise<{ ok: boolean; value: boolean | undefined }> {
+  const db = await freshDb();
+  try {
+    return {
+      ok: true,
+      value: await db.initDb(async () => {
+        throw value;
+      }),
+    };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINE = (message: string): Record<string, unknown>[] =>
+  h.calls.filter((c) => c.message === message).map((c) => c.meta as Record<string, unknown>);
+const POOL = 'DB pool unexpected error';
+const HOOK = 'DB ready boot work failed';
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
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
+describe('KS-1868 the pool error listener and the boot-work catch survive and log text for a hostile thrown value', () => {
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
+  it('control ks1868 C3: an ordinary Error from the onReady hook leaves initDb resolving true and is logged with its message', async () => {
+    expect(await hook(new Error('hydrate failed'))).toEqual({ ok: true, value: true });
+    expect(LINE(HOOK)).toHaveLength(1);
+    expect(reasonOf(LINE(HOOK)[0])).toBe('hydrate failed');
+  });
+  it('control ks1868 C4: a thrown number from the onReady hook leaves initDb resolving true and is logged without a message', async () => {
+    expect(await hook(42)).toEqual({ ok: true, value: true });
+    expect(LINE(HOOK)).toHaveLength(1);
+    expect(reasonOf(LINE(HOOK)[0])).toBe('<undefined>');
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
+  it('RED ks1868 R3: an onReady hook failure that is a revoked Proxy leaves initDb resolving true and is logged as text, as for an ordinary Error', async () => {
+    expect(await hook(revokedProxy())).toEqual({ ok: true, value: true });
+    expect(LINE(HOOK)).toHaveLength(1);
+    expect(reasonOf(LINE(HOOK)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an onReady hook failure that is an Error whose message getter throws leaves initDb resolving true and is logged as text, as for an ordinary Error', async () => {
+    expect(await hook(getterThrows())).toEqual({ ok: true, value: true });
+    expect(LINE(HOOK)).toHaveLength(1);
+    expect(reasonOf(LINE(HOOK)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an onReady hook failure that is an Error whose message is a Symbol leaves initDb resolving true and is logged as text, as for an ordinary Error', async () => {
+    expect(await hook(withMessage(Symbol('ks1868')))).toEqual({ ok: true, value: true });
+    expect(LINE(HOOK)).toHaveLength(1);
+    expect(reasonOf(LINE(HOOK)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
