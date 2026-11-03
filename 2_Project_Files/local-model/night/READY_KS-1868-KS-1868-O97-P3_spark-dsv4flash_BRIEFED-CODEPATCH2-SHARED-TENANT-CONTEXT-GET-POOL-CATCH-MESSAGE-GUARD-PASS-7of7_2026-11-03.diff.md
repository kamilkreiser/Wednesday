# READY — KS-1868-KS-1868-O97-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 17:24 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:24 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/db/tenant-context.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/db/tenant-context.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/packages/shared/src/db/tenant-context.ts
85	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: tenant-context.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/db/tenant-context.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/db/tenant-context.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts 85 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/db/tenant-context.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 extractTenantContext reads a thrown value safely RED ks1868 R1 a revoked Proxy answers 503 with a constant reason', 'KS-1868 extractTenantContext reads a thrown value safely RED ks1868 R2 an Error whose message getter throws answers 503 with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1447 failed=4 | after: total=1451 failed=1` · `NEW reds: []` [baseline_suite.json total=1447 failed=4; after_suite.json total=1451 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/db/tenant-context.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts` (+85/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/db/tenant-context.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p3_shared_tenant_context_get_pool_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/db/tenant-context.ts b/Blockchain/Dev/packages/shared/src/db/tenant-context.ts
--- a/Blockchain/Dev/packages/shared/src/db/tenant-context.ts
+++ b/Blockchain/Dev/packages/shared/src/db/tenant-context.ts
@@ -93,9 +93,15 @@
       req.tenantPool = manager.getPool(tenantId);
       next();
     } catch (err: any) {
+      let reason: string;
+      try {
+        reason = err.message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       res.status(503).json({
         error: 'Tenant database unavailable',
-        message: err.message,
+        message: reason,
       });
     }
   };
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts
@@ -0,0 +1,85 @@
+import { describe, it, expect } from 'vitest';
+import { extractTenantContext } from '../db/tenant-context';
+
+// KS-1868: the tenant-context middleware (src/db/tenant-context.ts) attaches a tenant pool to the request; when
+// manager.getPool throws, its catch answers 503 `{ error: 'Tenant database unavailable', message: err.message }`. The
+// `err.message` read is unguarded. When the value cannot be read (a revoked Proxy throws on any property read; an Error whose
+// `message` getter throws) the catch itself throws, so the middleware throws out of the request and no 503 is sent. The
+// manager is a plain stand-in whose getPool throws the cell's value (multi-tenancy off, so no status lookup); the response is
+// a plain recorder; no database.
+type Outcome = { threw: boolean; code: number | undefined; body: unknown; nextCalls: number };
+
+function run(value: unknown): Outcome {
+  const manager = {
+    isEnabled: () => false,
+    getPool: () => {
+      throw value;
+    },
+  };
+  const out: Outcome = { threw: false, code: undefined, body: undefined, nextCalls: 0 };
+  const res = {
+    status(c: number) {
+      out.code = c;
+      return res;
+    },
+    json(b: unknown) {
+      out.body = b;
+      return res;
+    },
+  };
+  const handler = extractTenantContext(manager as never);
+  try {
+    handler({ headers: { 'x-tenant-id': 'b1868000-0000-4000-8000-00000000000a' } } as never, res as never, () => {
+      out.nextCalls += 1;
+    });
+  } catch {
+    out.threw = true;
+  }
+  return out;
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 extractTenantContext reads a thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error answers 503 with its message', () => {
+    const out = run(new Error('pool gone'));
+    expect(out.threw).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body).toEqual({ error: 'Tenant database unavailable', message: 'pool gone' });
+    expect(out.nextCalls).toBe(0);
+  });
+
+  it('control ks1868 C2 a thrown plain string answers 503 without a message', () => {
+    const out = run('plain text failure');
+    expect(out.threw).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body).toEqual({ error: 'Tenant database unavailable', message: undefined });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy answers 503 with a constant reason', () => {
+    const out = run(revokedProxy());
+    expect(out.threw).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body).toEqual({ error: 'Tenant database unavailable', message: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws answers 503 with a constant reason', () => {
+    const out = run(getterThrows());
+    expect(out.threw).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body).toEqual({ error: 'Tenant database unavailable', message: 'unreadable thrown value' });
+  });
+});
```
