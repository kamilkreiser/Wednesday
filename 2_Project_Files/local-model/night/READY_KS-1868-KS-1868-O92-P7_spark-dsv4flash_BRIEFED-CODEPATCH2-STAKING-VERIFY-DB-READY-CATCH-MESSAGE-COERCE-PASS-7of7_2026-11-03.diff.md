# READY — KS-1868-KS-1868-O92-P7 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:53 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:53 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/staking/src/routes/stake.ts } + { Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/staking/src/routes/stake.ts` (product) and `Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/staking/src/routes/stake.ts
94	0	Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: stake.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/staking/src/routes/stake.ts`; test(s): `Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/staking/src/routes/stake.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts 94 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/staking/src/routes/stake.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the staking verifyDbReady catch resolves and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the query is logged as text and verifyDbReady resolves, as for an ordinary Error', 'KS-1868 the staking verifyDbReady catch resolves and logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the query is logged as text and verifyDbReady resolves, as for an ordinary Error', 'KS-1868 the staking verifyDbReady catch resolves and logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the query is logged as text and verifyDbReady resolves, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=93 failed=0 | after: total=98 failed=0` · `NEW reds: []` [baseline_suite.json total=93 failed=0; after_suite.json total=98 failed=0]
- A6 [verbatim]: `PASS A6 whole services/staking suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/staking: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/staking/src/routes/stake.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts` (+94/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/staking/src/routes/stake.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p7_staking_verify_db_ready_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/staking/src/routes/stake.ts b/Blockchain/Dev/services/staking/src/routes/stake.ts
--- a/Blockchain/Dev/services/staking/src/routes/stake.ts
+++ b/Blockchain/Dev/services/staking/src/routes/stake.ts
@@ -145,6 +145,13 @@
     poolStats.totalStaked = Number(row.total);
     logger.info(`[Staking] DB ready — ${poolStats.stakerCount} stake positions (total staked: ${poolStats.totalStaked})`);
   } catch (err: any) {
-    logger.error('[Staking] Failed to verify DB readiness for stake positions', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('[Staking] Failed to verify DB readiness for stake positions', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts
@@ -0,0 +1,94 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 92 screen, staking): the catch of verifyDbReady (line 147) of services/staking/src/routes/stake.ts passes `err?.message` straight into the
+// logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter
+// throws) makes the catch throw, so verifyDbReady REJECTS where an ordinary Error is logged and the function resolves (the service boots with empty pool
+// statistics); an Error whose message is readable but not a string (a Symbol) is handed to the logger uncoerced. The cells make the pool-statistics query reject
+// with such a value and assert verifyDbReady resolves and the failure is logged as text (the constant when the value cannot be turned into text). Harness: the
+// real module with ../db and ../utils/logger replaced by plain stand-ins (the query is a plain function, not vi.fn(): a spy could inspect a revoked Proxy and fail
+// before the code under test saw it); no database, no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+import { verifyDbReady } from '../routes/stake';
+
+const FAILED = '[Staking] Failed to verify DB readiness for stake positions';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logs.length = 0;
+});
+
+const LINES = () => h.logs.filter((l) => l.message === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = l?.meta?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+async function run(value: unknown): Promise<{ threw: boolean }> {
+  h.toThrow = value;
+  try {
+    await verifyDbReady();
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
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
+describe('KS-1868 the staking verifyDbReady catch resolves and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the pool-statistics query is logged with its message and verifyDbReady resolves', async () => {
+    expect(await run(new Error('db boom'))).toEqual({ threw: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: a thrown plain string is logged without a message and verifyDbReady resolves', async () => {
+    expect(await run('plain boom')).toEqual({ threw: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the query is logged as text and verifyDbReady resolves, as for an ordinary Error', async () => {
+    expect(await run(revokedProxy())).toEqual({ threw: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the query is logged as text and verifyDbReady resolves, as for an ordinary Error', async () => {
+    expect(await run(withMessage(Symbol('ks1868')))).toEqual({ threw: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the query is logged as text and verifyDbReady resolves, as for an ordinary Error', async () => {
+    expect(await run(getterThrows())).toEqual({ threw: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+});
```
