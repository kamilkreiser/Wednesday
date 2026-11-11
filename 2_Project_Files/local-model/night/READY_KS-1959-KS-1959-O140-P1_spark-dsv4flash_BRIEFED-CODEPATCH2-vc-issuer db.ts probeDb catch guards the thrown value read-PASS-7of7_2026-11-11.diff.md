# READY — KS-1959-KS-1959-O140-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 16:47 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 16:47 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6911aa643db13ad1d09b37dd69c38df01cb029a4`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/vc-issuer/src/db.ts } + { Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/db.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/vc-issuer/src/db.ts
117	0	Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/vc-issuer/src/db.ts`; test(s): `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/vc-issuer/src/db.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts 117 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/db.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1959 the availability probe survives a hostile thrown value and logs text RED ks1959 R1: a probe failure that is a revoked Proxy leaves initDb resolving false and is logged as text, as for an ordinary Error', 'KS-1959 the availability probe survives a hostile thrown value and logs text RED ks1959 R2: a probe failure that is an Error whose message getter throws leaves initDb resolving false and is logged as text, as for an ordinary Error', 'KS-1959 the availability probe survives a hostile thrown value and logs text RED ks1959 R3: a probe failure that is an Error whose message is a Symbol leaves initDb resolving false and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=842 failed=0 | after: total=847 failed=0` · `NEW reds: []` [baseline_suite.json total=842 failed=0; after_suite.json total=847 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/db.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts` (+117/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/vc-issuer/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `6911aa643db13ad1d09b37dd69c38df01cb029a4` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1959): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/KS-1959.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1959_o140_p1_vc_issuer_db_probe_db_catch_guards_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/vc-issuer/src/db.ts b/Blockchain/Dev/services/vc-issuer/src/db.ts
--- a/Blockchain/Dev/services/vc-issuer/src/db.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/db.ts
@@ -99,6 +99,13 @@
     return { ok: dbAvailable };
   } catch (err: any) {
     dbAvailable = false;
-    return { ok: false, error: err?.message };
+    let error: string | undefined;
+    try {
+      const m = err?.message;
+      error = m === undefined || m === null ? undefined : String(m);
+    } catch {
+      error = 'unreadable thrown value';
+    }
+    return { ok: false, error };
   }
 }
diff --git a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1959-vc-issuer-db-probe-catch-unreadable-throw.test.ts
@@ -0,0 +1,117 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1959 (vc-issuer db module, probeDb): the probe's catch returns `{ ok: false, error: err?.message }` with an unguarded
+// read of the thrown value. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the
+// catch itself throw, so probeDb REJECTS: initDb rejects at boot instead of resolving false and arming the background retry,
+// and a rejecting probe inside the retry timer callback is an unhandled rejection that stops the retry for good. An Error whose
+// message is not a string (a Symbol) is handed to the log line uncoerced. The cells make the pool's query reject with such a
+// value and assert initDb resolves false and the 'Database unavailable' line carries text (the constant when the value cannot
+// be turned into text). Harness: the real module with pg replaced by a plain stand-in Pool whose query rejects with the armed
+// value (no database) and the logger replaced by a recording function.
+const h = vi.hoisted(() => ({
+  thrown: undefined as unknown,
+  calls: [] as { message: string; meta: unknown }[],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    error: () => undefined,
+    warn: (message: string, meta?: unknown) => {
+      h.calls.push({ message, meta });
+    },
+    info: () => undefined,
+    debug: () => undefined,
+  },
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: async () => {
+        throw h.thrown;
+      },
+      on: () => undefined,
+      end: async () => undefined,
+      connect: async () => undefined,
+    };
+  },
+}));
+
+type Db = typeof import('../db');
+const realUrl = process.env.DATABASE_URL;
+afterAll(() => {
+  if (realUrl === undefined) delete process.env.DATABASE_URL;
+  else process.env.DATABASE_URL = realUrl;
+});
+beforeEach(() => {
+  h.thrown = undefined;
+  h.calls.length = 0;
+  process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
+});
+
+async function freshDb(): Promise<Db> {
+  vi.resetModules();
+  return import('../db');
+}
+/** Arm the value, run initDb once, stop the background retry the failed probe arms, and say what came back. */
+async function probe(value: unknown): Promise<{ ok: boolean; value: boolean | undefined }> {
+  h.thrown = value;
+  const db = await freshDb();
+  try {
+    const result = await db.initDb();
+    return { ok: true, value: result };
+  } catch {
+    return { ok: false, value: undefined };
+  } finally {
+    await db.closeDb();
+  }
+}
+const UNAVAILABLE = 'Database unavailable';
+const LINE = (): Record<string, unknown>[] =>
+  h.calls.filter((c) => c.message.startsWith(UNAVAILABLE)).map((c) => c.meta as Record<string, unknown>);
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
+describe('KS-1959 the availability probe survives a hostile thrown value and logs text', () => {
+  it('control ks1959 C1: an ordinary Error from the probe leaves initDb resolving false and is logged with its message', async () => {
+    expect(await probe(new Error('connection refused'))).toEqual({ ok: true, value: false });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('connection refused');
+  });
+  it('control ks1959 C2: a plain string from the probe leaves initDb resolving false and is logged without a message', async () => {
+    expect(await probe('plain boom')).toEqual({ ok: true, value: false });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('<undefined>');
+  });
+  it('RED ks1959 R1: a probe failure that is a revoked Proxy leaves initDb resolving false and is logged as text, as for an ordinary Error', async () => {
+    expect(await probe(revokedProxy())).toEqual({ ok: true, value: false });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1959 R2: a probe failure that is an Error whose message getter throws leaves initDb resolving false and is logged as text, as for an ordinary Error', async () => {
+    expect(await probe(getterThrows())).toEqual({ ok: true, value: false });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1959 R3: a probe failure that is an Error whose message is a Symbol leaves initDb resolving false and is logged as text, as for an ordinary Error', async () => {
+    expect(await probe(withMessage(Symbol('ks1959')))).toEqual({ ok: true, value: false });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('Symbol(ks1959)');
+  });
+});
```

> NOTE (operator o140, 2026-11-11): db.ts only; credentialRepo.ts is NOT in this READY (o136 P4 / o137 P5). Status of KS-1959 not read by the operator (named by Seat S 55th). Read the + lines at source: error is typed string|undefined (a null message becomes undefined), not the credentialRepo null-preserving shape.
