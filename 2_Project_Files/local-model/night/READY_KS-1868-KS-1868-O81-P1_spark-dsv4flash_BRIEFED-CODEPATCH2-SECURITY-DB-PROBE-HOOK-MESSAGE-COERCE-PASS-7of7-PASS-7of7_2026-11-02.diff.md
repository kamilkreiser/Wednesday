# READY — KS-1868-KS-1868-O81-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 18:57 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 18:57 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `466a0d6c4c55b110bdb0384bf8c2d6c864b8a1d1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/db.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/db.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	2	Blockchain/Dev/services/security/src/db.ts
136	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: db.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/db.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/db.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts 136 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/db.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R1 probe: a message that is a revoked Proxy is logged as its safe text and initDb resolves false', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R2 probe: a message whose toString throws is logged as its safe text and initDb resolves false', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R3 probe: a null-prototype message is logged as its safe text and initDb resolves false', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R4 probe: a Symbol message is logged as its safe text and initDb resolves false', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R5 hook: a message that is a revoked Proxy is logged as its safe text and initDb resolves true', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R6 hook: a message whose toString throws is logged as its safe text and initDb resolves true', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R7 hook: a null-prototype message is logged as its safe text and initDb resolves true', 'KS-1868 the catches of the security db module coerce a non-string message safely RED ks1868 R8 hook: a Symbol message is logged as its safe text and initDb resolves true']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=424 failed=0 | after: total=436 failed=0` · `NEW reds: []` [baseline_suite.json total=424 failed=0; after_suite.json total=436 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/db.ts` (+4/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts` (+136/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/db.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `466a0d6c4c55b110bdb0384bf8c2d6c864b8a1d1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/db.ts b/Blockchain/Dev/services/security/src/db.ts
--- a/Blockchain/Dev/services/security/src/db.ts
+++ b/Blockchain/Dev/services/security/src/db.ts
@@ -100,7 +100,8 @@
   } catch (err: any) {
     let reason: string;
     try {
-      reason = err?.message;
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
     } catch {
       reason = 'unreadable thrown value';
     }
@@ -118,7 +119,8 @@
     dbAvailable = false;
     let reason: string;
     try {
-      reason = err?.message;
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
     } catch {
       reason = 'unreadable thrown value';
     }
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-db-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,136 @@
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+
+// KS-1868 (QA gate 112, G112-F1): the two catches of the security db module (src/db.ts), probeDb and runDbReadyHook,
+// read `err?.message` inside a guard and use the result outside it. The guard covers only the READ. When the message
+// getter SUCCEEDS and returns a hostile NON-string (a revoked Proxy, an object whose toString throws, a null-prototype
+// object, a Symbol) the value is passed on as it is: the boot hook's JSON log line then throws while it is built, so
+// `initDb` rejects, and the probe returns the value as its `error`. After the fix the read is coerced with String(...)
+// inside the same guard, so a value that cannot be turned into text lands in the existing catch and gives the constant
+// 'unreadable thrown value' (a Symbol gives its text). A message that is undefined or null is passed through unchanged,
+// so a thrown plain string is logged exactly as before.
+// The pg stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with. Hostile values are
+// compared by their type name so a revoked Proxy never reaches an equality matcher.
+const ctl = vi.hoisted(() => ({
+  probeBoom: undefined as unknown,
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: () => (ctl.probeBoom !== undefined ? Promise.reject(ctl.probeBoom) : Promise.resolve({ rows: [{ ok: 1 }] })),
+      on: () => undefined,
+      end: () => Promise.resolve(undefined),
+      connect: () => Promise.resolve(undefined),
+    };
+  },
+}));
+
+const lines: Array<{ level: string; message: string; error?: unknown }> = [];
+
+/** Fresh copy of the module per cell: db.ts holds module-level state. */
+async function importDb() {
+  vi.resetModules();
+  return import('../db');
+}
+
+const lineOf = (message: string) => lines.filter((l) => l.message.startsWith(message)).map((l) => ({ level: l.level, error: l.error }));
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+// An Error whose `message` getter succeeds but returns the given value.
+const withMessage = (value: () => unknown): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        return value();
+      },
+    },
+  });
+/** Settle a promise into a value so a rejection is an ordinary assertion failure, not a thrown error. */
+const settle = (p: Promise<boolean>): Promise<{ resolved: boolean; value?: boolean }> =>
+  p.then(
+    (value) => ({ resolved: true, value }),
+    () => ({ resolved: false }),
+  );
+const PROBE_FAILED = 'Database unavailable';
+const HOOK_FAILED = 'DB ready boot work failed';
+
+const hostile = (first: number): Array<[number, string, () => unknown, string]> => [
+  [first, 'a message that is a revoked Proxy', () => withMessage(revokedProxy), 'unreadable thrown value'],
+  [first + 1, 'a message whose toString throws', () => withMessage(() => ({ toString: () => { throw new Error('toString boom'); } })), 'unreadable thrown value'],
+  [first + 2, 'a null-prototype message', () => withMessage(() => Object.create(null)), 'unreadable thrown value'],
+  [first + 3, 'a Symbol message', () => withMessage(() => Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+
+describe('KS-1868 the catches of the security db module coerce a non-string message safely', () => {
+  let current: { closeDb: () => Promise<void> } | undefined;
+
+  beforeEach(() => {
+    ctl.probeBoom = undefined;
+    lines.length = 0;
+    process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
+    vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
+      try {
+        const o = JSON.parse(String(args[0]));
+        lines.push({ level: o.level, message: String(o.message), error: o.error });
+      } catch {
+        /* not a JSON line */
+      }
+    });
+  });
+
+  afterEach(async () => {
+    if (current) await current.closeDb();
+    current = undefined;
+    vi.restoreAllMocks();
+    delete process.env.DATABASE_URL;
+  });
+
+  it('control ks1868 C1 an ordinary Error from the probe is logged with its message and initDb resolves false', async () => {
+    ctl.probeBoom = new Error('db down');
+    const db = await importDb();
+    current = db;
+    expect(await settle(db.initDb())).toEqual({ resolved: true, value: false });
+    expect(lineOf(PROBE_FAILED)).toEqual([{ level: 'warn', error: 'db down' }]);
+  });
+
+  it('control ks1868 C2 an ordinary Error from the boot hook is logged with its message and initDb resolves true', async () => {
+    const db = await importDb();
+    current = db;
+    expect(await settle(db.initDb(() => Promise.reject(new Error('hook down'))))).toEqual({ resolved: true, value: true });
+    expect(lineOf(HOOK_FAILED)).toEqual([{ level: 'error', error: 'hook down' }]);
+  });
+
+  it('control ks1868 C3 a plain string thrown by the probe has no message and is logged with no error, as before', async () => {
+    ctl.probeBoom = 'plain string down';
+    const db = await importDb();
+    current = db;
+    expect(await settle(db.initDb())).toEqual({ resolved: true, value: false });
+    expect(lineOf(PROBE_FAILED)).toEqual([{ level: 'warn', error: undefined }]);
+  });
+
+  it('control ks1868 C4 a plain string thrown by the boot hook has no message and is logged with no error, as before', async () => {
+    const db = await importDb();
+    current = db;
+    expect(await settle(db.initDb(() => Promise.reject('plain string down')))).toEqual({ resolved: true, value: true });
+    expect(lineOf(HOOK_FAILED)).toEqual([{ level: 'error', error: undefined }]);
+  });
+
+  it.each(hostile(1))('RED ks1868 R%s probe: %s is logged as its safe text and initDb resolves false', async (_id, _what, make, text) => {
+    ctl.probeBoom = make();
+    const db = await importDb();
+    current = db;
+    expect(await settle(db.initDb())).toEqual({ resolved: true, value: false });
+    expect(lineOf(PROBE_FAILED)).toEqual([{ level: 'warn', error: text }]);
+  });
+
+  it.each(hostile(5))('RED ks1868 R%s hook: %s is logged as its safe text and initDb resolves true', async (_id, _what, make, text) => {
+    const db = await importDb();
+    current = db;
+    const boom = make();
+    expect(await settle(db.initDb(() => Promise.reject(boom)))).toEqual({ resolved: true, value: true });
+    expect(lineOf(HOOK_FAILED)).toEqual([{ level: 'error', error: text }]);
+  });
+});
```
