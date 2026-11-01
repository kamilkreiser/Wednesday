# READY — KS-1868-KS-1868-O71-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:53 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:53 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bd8785796118a20b0220924523a543baf7f73340`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/kyc/src/index.ts } + { Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/index.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/kyc/src/index.ts
137	0	Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/kyc/src/index.ts`; test(s): `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/kyc/src/index.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts 137 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 verifyDbReady reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the boot probe ends without a rejection', 'KS-1868 verifyDbReady reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and the boot probe ends without a rejection']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=73 failed=0 | after: total=76 failed=0` · `NEW reds: []` [baseline_suite.json total=73 failed=0; after_suite.json total=76 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/index.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts` (+137/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/kyc/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `bd8785796118a20b0220924523a543baf7f73340` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/kyc/src/index.ts b/Blockchain/Dev/services/kyc/src/index.ts
--- a/Blockchain/Dev/services/kyc/src/index.ts
+++ b/Blockchain/Dev/services/kyc/src/index.ts
@@ -502,6 +502,12 @@
     );
     logger.info('KYC DB verified', { verifications: Number(result.rows[0]?.cnt ?? 0) });
   } catch (err: any) {
-    logger.warn('KYC DB verification query failed', { error: err?.message });
+    let reason: string;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('KYC DB verification query failed', { error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts b/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts
@@ -0,0 +1,137 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+process.env.KYC_PROVIDER = 'mock';
+process.env.NODE_ENV = 'test';
+
+// KS-1868: `verifyDbReady` (the boot-time table probe) must still log its warning and let the service start when
+// the thrown value itself cannot be read (a revoked Proxy throws on `instanceof`/property reads; an Error whose
+// `message` getter throws, throws on `.message`). Harness: the KS-1845 one (the app module imported with the db and
+// subject-DEK modules replaced), except that no listener is needed: the probe runs at import time.
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
+// itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  warned: [] as unknown[][],
+  probes: 0,
+}));
+
+vi.mock('../db', () => ({
+  initDb: async () => true,
+  isDbAvailable: () => true,
+  query: async (sql: string) => {
+    if (/COUNT\(\*\)/i.test(String(sql))) {
+      h.probes += 1;
+      throw h.toThrow;
+    }
+    return { rows: [] };
+  },
+}));
+
+vi.mock('../subjectDeks', () => ({
+  subjectDeks: {
+    getOrCreateDek: async () => Buffer.alloc(32, 7),
+    getDek: async () => Buffer.alloc(32, 7),
+    evict: () => undefined,
+  },
+}));
+
+vi.mock('../utils/logger', () => {
+  const logger = {
+    info: () => undefined,
+    debug: () => undefined,
+    error: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warned.push(args);
+    },
+  };
+  return { logger, createLogger: () => logger, validateEnv: () => undefined };
+});
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  };
+});
+
+vi.mock('express', async (importOriginal) => {
+  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
+  const factory: any = (...args: any[]) => {
+    const app = actual(...args);
+    app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } });
+    return app;
+  };
+  Object.assign(factory, actual);
+  return { ...actual, default: factory };
+});
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+let unhandled = 0;
+const countUnhandled = () => {
+  unhandled += 1;
+};
+
+const WARNINGS = () => h.warned.filter((c) => String(c[0]).includes('KYC DB verification query failed'));
+
+/** Imports the app fresh and waits (up to 2 s) for the boot probe to have run and its catch to have finished. */
+async function bootAndSettle() {
+  vi.resetModules();
+  await import('../index');
+  const deadline = Date.now() + 2000;
+  while (Date.now() < deadline && (h.probes === 0 || WARNINGS().length === 0)) {
+    await new Promise((resolve) => setTimeout(resolve, 25));
+  }
+  await new Promise((resolve) => setTimeout(resolve, 100));
+}
+
+describe('KS-1868 verifyDbReady reads the thrown value safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.warned.length = 0;
+    h.probes = 0;
+    unhandled = 0;
+    process.removeAllListeners('unhandledRejection');
+    process.on('unhandledRejection', countUnhandled);
+  });
+
+  afterEach(() => {
+    process.removeListener('unhandledRejection', countUnhandled);
+    for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+  });
+
+  it('control ks1868 C1 an ordinary Error still logs its message and the boot probe ends without a rejection', async () => {
+    h.toThrow = new Error('db down');
+    await bootAndSettle();
+    expect(h.probes).toBe(1);
+    expect(WARNINGS()).toHaveLength(1);
+    expect(WARNINGS()[0][1]).toEqual({ error: 'db down' });
+    expect(unhandled).toBe(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the boot probe ends without a rejection', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    await bootAndSettle();
+    expect(h.probes).toBe(1);
+    expect(WARNINGS()).toHaveLength(1);
+    expect(WARNINGS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(unhandled).toBe(0);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and the boot probe ends without a rejection', async () => {
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    await bootAndSettle();
+    expect(h.probes).toBe(1);
+    expect(WARNINGS()).toHaveLength(1);
+    expect(WARNINGS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(unhandled).toBe(0);
+  });
+});
```
