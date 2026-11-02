# READY — KS-1868-KS-1868-O92-P11 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 09:10 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:10 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/index.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/index.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/timestamping/src/index.ts
130	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/index.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/index.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts 130 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the timestamping ensureTable catch logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the table creation is logged by ensureTable as text, as for an ordinary Error', 'KS-1868 the timestamping ensureTable catch logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the table creation is logged by ensureTable as text, as for an ordinary Error', 'KS-1868 the timestamping ensureTable catch logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the table creation is logged by ensureTable as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=105 failed=3 | after: total=110 failed=0` · `NEW reds: []` [baseline_suite.json total=105 failed=3; after_suite.json total=110 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/index.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts` (+130/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p11_timestamping_index_ensure_table_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/index.ts b/Blockchain/Dev/services/timestamping/src/index.ts
--- a/Blockchain/Dev/services/timestamping/src/index.ts
+++ b/Blockchain/Dev/services/timestamping/src/index.ts
@@ -117,6 +117,13 @@
     await query(`CREATE INDEX IF NOT EXISTS idx_ts_timestamps_hash ON ts_timestamps(hash)`);
     tableEnsured = true;
   } catch (err: any) {
-    log('warn', 'Failed to ensure ts_timestamps table', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    log('warn', 'Failed to ensure ts_timestamps table', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts
@@ -0,0 +1,130 @@
+import { describe, it, expect, afterAll, beforeEach, afterEach, vi } from 'vitest';
+import type { RequestHandler } from 'express';
+
+// KS-1868 (operator 92 screen, timestamping index): the catch of ensureTable (line 120) of services/timestamping/src/index.ts passes `err?.message` straight into
+// the log line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter
+// throws) makes the catch throw, so ensureTable REJECTS and the failure is attributed to its caller (the readiness check logs a TypeError as 'DB verification
+// failed' and the 'Failed to ensure ts_timestamps table' line is never written) where an ordinary Error is logged by ensureTable itself and the table creation
+// is retried on the next call; an Error whose message is readable but not a string (a Symbol) is handed to JSON.stringify uncoerced and silently dropped from the
+// line. The cells make the table-creation statement reject with such a value while the service boots (the boot readiness check calls ensureTable first) and
+// assert the line is logged by ensureTable with text (the constant when the value cannot be turned into text) and no unhandled rejection is raised. Harness: the
+// real index.ts (a fresh copy per cell; it listens on an ephemeral port at import); `./db` is a stand-in that is available, answers the schema-privilege probe yes and rejects the CREATE TABLE statement;
+// the shared JWT check is a pass-through; console.log is a plain recording function (no database, no network).
+const h = vi.hoisted(() => {
+  process.env.PORT = '0';
+  return {
+    toThrow: undefined as unknown,
+    lines: [] as string[],
+    unhandled: 0,
+  };
+});
+
+vi.mock('../db', () => ({
+  initDb: async () => true,
+  isDbAvailable: () => true,
+  closeDb: async () => undefined,
+  query: (sql: string, ..._args: unknown[]) =>
+    String(sql).includes('has_schema_privilege')
+      ? Promise.resolve({ rows: [{ ok: true }] })
+      : String(sql).includes('CREATE TABLE')
+        ? Promise.reject(h.toThrow)
+        : Promise.resolve({ rows: [{ count: '0' }] }),
+}));
+vi.mock('@secuura/shared', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  authenticate: () => ((_req, _res, next) => next()) as RequestHandler,
+}));
+
+const realLog = console.log;
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.lines.length = 0;
+  h.unhandled = 0;
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  console.log = (...args: unknown[]) => {
+    if (typeof args[0] === 'string') h.lines.push(args[0]);
+  };
+});
+afterEach(() => {
+  console.log = realLog;
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+afterAll(() => {
+  console.log = realLog;
+});
+
+const ENSURE = 'Failed to ensure ts_timestamps table';
+const LINE = (message: string): Record<string, unknown>[] =>
+  h.lines
+    .map((l) => {
+      try {
+        return JSON.parse(l) as Record<string, unknown>;
+      } catch {
+        return {} as Record<string, unknown>;
+      }
+    })
+    .filter((o) => o.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
+
+async function boot(value: unknown): Promise<{ unhandled: number }> {
+  h.toThrow = value;
+  vi.resetModules();
+  await import('../index');
+  for (let i = 0; i < 100 && !h.lines.some((l) => l.includes('Timestamping Service started')); i++) {
+    await new Promise<void>((resolve) => setTimeout(resolve, 20));
+  }
+  await new Promise<void>((resolve) => setTimeout(resolve, 25));
+  return { unhandled: h.unhandled };
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
+describe('KS-1868 the timestamping ensureTable catch logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the table creation is logged by ensureTable with its message', async () => {
+    expect(await boot(new Error('ddl boom'))).toEqual({ unhandled: 0 });
+    expect(LINE(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINE(ENSURE)[0])).toBe('ddl boom');
+  });
+  it('control ks1868 C2: a thrown plain string is logged by ensureTable without a message', async () => {
+    expect(await boot('plain boom')).toEqual({ unhandled: 0 });
+    expect(LINE(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINE(ENSURE)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the table creation is logged by ensureTable as text, as for an ordinary Error', async () => {
+    expect(await boot(revokedProxy())).toEqual({ unhandled: 0 });
+    expect(LINE(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINE(ENSURE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the table creation is logged by ensureTable as text, as for an ordinary Error', async () => {
+    expect(await boot(withMessage(Symbol('ks1868')))).toEqual({ unhandled: 0 });
+    expect(LINE(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINE(ENSURE)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the table creation is logged by ensureTable as text, as for an ordinary Error', async () => {
+    expect(await boot(getterThrows())).toEqual({ unhandled: 0 });
+    expect(LINE(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINE(ENSURE)[0])).toBe('unreadable thrown value');
+  });
+});
```
