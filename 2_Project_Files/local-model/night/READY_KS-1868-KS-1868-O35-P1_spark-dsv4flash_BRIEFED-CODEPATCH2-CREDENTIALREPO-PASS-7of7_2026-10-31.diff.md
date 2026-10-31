# READY — KS-1868-KS-1868-O35-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:15 2026-10-31; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:15 2026-10-31 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cb2320368ae42fa793d81776fdd7fc8404ce312d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts } + { Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
61	0	Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: credentialRepo.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts`; test(s): `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts 61 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 credentialRepo.loadFromDb reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', 'KS-1868 credentialRepo.loadFromDb reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=413 failed=0 | after: total=416 failed=0` · `NEW reds: []` [baseline_suite.json total=413 failed=0; after_suite.json total=416 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts` (+61/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cb2320368ae42fa793d81776fdd7fc8404ce312d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
--- a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
@@ -430,5 +430,11 @@
   } catch (err) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.warn('credentialRepo.loadFromDb failed — starting with empty store', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
   }
diff --git a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts
@@ -0,0 +1,61 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: credentialRepo.loadFromDb must still log its WARN when the thrown value
+// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
+// `message` getter throws, throws on `.message`).
+// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it
+// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  warn: vi.fn(),
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (sql: string) =>
+    /ORDER BY created_at/i.test(sql) ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [] }),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: h.warn, error: vi.fn(), debug: vi.fn() },
+}));
+
+import * as repo from '../repositories/credentialRepo';
+
+const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('loadFromDb failed'));
+
+describe('KS-1868 credentialRepo.loadFromDb reads the thrown value safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.warn.mockReset();
+  });
+
+  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
+    h.toThrow = new Error('db down');
+    await repo.loadFromDb();
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    await repo.loadFromDb().catch(() => undefined);
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    await repo.loadFromDb().catch(() => undefined);
+    expect(WARNS()).toHaveLength(1);
+    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
