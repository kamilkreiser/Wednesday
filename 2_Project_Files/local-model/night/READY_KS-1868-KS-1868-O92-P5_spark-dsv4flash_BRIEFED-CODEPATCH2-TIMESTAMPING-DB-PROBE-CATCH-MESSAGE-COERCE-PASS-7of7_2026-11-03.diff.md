# READY — KS-1868-KS-1868-O92-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:46 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:46 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b85b7b6786fa6329b6f781cebf2475147738004e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/db.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/db.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/timestamping/src/db.ts
107	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/db.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/db.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts 107 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/db.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the timestamping availability probe survives and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the probe query resolves initDb false and is logged as text, as for an ordinary Error', 'KS-1868 the timestamping availability probe survives and logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the probe query resolves initDb false and is logged as text, as for an ordinary Error', 'KS-1868 the timestamping availability probe survives and logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the probe query resolves initDb false and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=105 failed=0 | after: total=110 failed=0` · `NEW reds: []` [baseline_suite.json total=105 failed=0; after_suite.json total=110 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/db.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts` (+107/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b85b7b6786fa6329b6f781cebf2475147738004e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p5_timestamping_db_probe_db_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/db.ts b/Blockchain/Dev/services/timestamping/src/db.ts
--- a/Blockchain/Dev/services/timestamping/src/db.ts
+++ b/Blockchain/Dev/services/timestamping/src/db.ts
@@ -96,6 +96,13 @@
     return { ok: dbAvailable };
   } catch (err: any) {
     dbAvailable = false;
-    return { ok: false, error: err?.message };
+    let reason: string | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? undefined : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    return { ok: false, error: reason };
   }
 }
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts
@@ -0,0 +1,107 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 92 screen, timestamping db module): the catch of probeDb (line 99) of services/timestamping/src/db.ts returns `{ ok: false, error: err?.message }`, unguarded.
+// `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch throw, so
+// probeDb REJECTS: initDb rejects at boot instead of resolving false, and a failed background re-probe rejects inside the retry timer (an unhandled rejection
+// that also ends the retry chain, so the service stays degraded for good); an Error whose message is not a string (a Symbol) is handed to JSON.stringify
+// uncoerced and silently dropped from the line. The cells make the probe query reject with such a value and assert initDb resolves false and the unavailable
+// line carries text (the constant when the value cannot be turned into text). Harness: the real module with pg replaced by a plain stand-in Pool (its query
+// rejects with the value) and console.log replaced by a plain recording function (no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  lines: [] as string[],
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+      on: (_event: string, _fn: (e: unknown) => void) => undefined,
+      end: async () => undefined,
+      connect: async () => undefined,
+    };
+  },
+}));
+
+type Db = typeof import('../db');
+const realLog = console.log;
+const realUrl = process.env.DATABASE_URL;
+afterAll(() => {
+  console.log = realLog;
+  if (realUrl === undefined) delete process.env.DATABASE_URL;
+  else process.env.DATABASE_URL = realUrl;
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.lines.length = 0;
+  process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
+  console.log = (...args: unknown[]) => {
+    if (typeof args[0] === 'string') h.lines.push(args[0]);
+  };
+});
+
+async function freshDb(): Promise<Db> {
+  vi.resetModules();
+  return import('../db');
+}
+async function init(value: unknown): Promise<{ ok: boolean; value: boolean | undefined }> {
+  h.toThrow = value;
+  const db = await freshDb();
+  try {
+    const v = await db.initDb();
+    await db.closeDb();
+    return { ok: true, value: v };
+  } catch {
+    await db.closeDb();
+    return { ok: false, value: undefined };
+  }
+}
+const LINE = (message: string): Record<string, unknown>[] =>
+  h.lines.map((l) => JSON.parse(l) as Record<string, unknown>).filter((o) => o.message === message);
+const UNAVAILABLE = 'Database unavailable — using in-memory fallback until it comes up, retrying in background (KS-377)';
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
+describe('KS-1868 the timestamping availability probe survives and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the probe query resolves initDb false and is logged with its message', async () => {
+    expect(await init(new Error('probe boom'))).toEqual({ ok: true, value: false });
+    expect(LINE(UNAVAILABLE)).toHaveLength(1);
+    expect(reasonOf(LINE(UNAVAILABLE)[0])).toBe('probe boom');
+  });
+  it('control ks1868 C2: a plain string from the probe query resolves initDb false and is logged without a message', async () => {
+    expect(await init('plain boom')).toEqual({ ok: true, value: false });
+    expect(LINE(UNAVAILABLE)).toHaveLength(1);
+    expect(reasonOf(LINE(UNAVAILABLE)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the probe query resolves initDb false and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(revokedProxy())).toEqual({ ok: true, value: false });
+    expect(LINE(UNAVAILABLE)).toHaveLength(1);
+    expect(reasonOf(LINE(UNAVAILABLE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the probe query resolves initDb false and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(withMessage(Symbol('ks1868')))).toEqual({ ok: true, value: false });
+    expect(LINE(UNAVAILABLE)).toHaveLength(1);
+    expect(reasonOf(LINE(UNAVAILABLE)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the probe query resolves initDb false and is logged as text, as for an ordinary Error', async () => {
+    expect(await init(getterThrows())).toEqual({ ok: true, value: false });
+    expect(LINE(UNAVAILABLE)).toHaveLength(1);
+    expect(reasonOf(LINE(UNAVAILABLE)[0])).toBe('unreadable thrown value');
+  });
+});
```
