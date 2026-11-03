# READY — KS-1868-KS-1868-O94-P8 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:34 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:34 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/services/authClient.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/services/authClient.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/demo-service/src/services/authClient.ts
58	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: authClient.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/services/authClient.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/services/authClient.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts 58 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/services/authClient.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 authenticatePersona reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value gives the failed result with a constant reason', 'KS-1868 authenticatePersona reads the thrown value safely RED ks1868 R2 an Error whose message getter throws gives the failed result with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=103 failed=0 | after: total=107 failed=0` · `NEW reds: []` [baseline_suite.json total=103 failed=0; after_suite.json total=107 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/services/authClient.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts` (+58/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/services/authClient.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p8_demo_service_auth_client_authenticate_persona_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/services/authClient.ts b/Blockchain/Dev/services/demo-service/src/services/authClient.ts
--- a/Blockchain/Dev/services/demo-service/src/services/authClient.ts
+++ b/Blockchain/Dev/services/demo-service/src/services/authClient.ts
@@ -59,7 +59,12 @@
       setCookieHeader,
     };
   } catch (err) {
-    const message = err instanceof Error ? err.message : 'Unknown error';
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : 'Unknown error';
+    } catch {
+      message = 'unreadable thrown value';
+    }
     logger.error('Auth service request failed', { error: message, email });
     return {
       success: false,
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts
@@ -0,0 +1,58 @@
+import { describe, it, expect, vi, afterEach } from 'vitest';
+
+// KS-1868: authenticatePersona (src/services/authClient.ts) is documented "does NOT throw on failure": a failed call is a
+// { success: false, error } result. Its catch reads `err instanceof Error ? err.message : 'Unknown error'` unguarded. When the value fetch
+// rejected with cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`) the catch
+// throws, so authenticatePersona REJECTS where an ordinary Error gives the failed result.
+// The fetch and logger stand-ins are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy first.
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: () => undefined,
+    error: () => undefined,
+  },
+}));
+
+import { authenticatePersona } from '../services/authClient';
+
+/** The result, or the string 'rejected' when authenticatePersona rejects (an assertion can then fail on it). */
+async function login(value: unknown): Promise<unknown> {
+  vi.stubGlobal('fetch', () => Promise.reject(value));
+  try {
+    return await authenticatePersona('demo@example.com', 'pw');
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 authenticatePersona reads the thrown value safely', () => {
+  afterEach(() => {
+    vi.unstubAllGlobals();
+  });
+
+  it('control ks1868 C1 an ordinary Error gives the failed result with its message', async () => {
+    expect(await login(new Error('connection refused'))).toEqual({ success: false, error: 'connection refused' });
+  });
+
+  it('control ks1868 C2 a thrown plain string gives the failed result with the default reason', async () => {
+    expect(await login('plain text failure')).toEqual({ success: false, error: 'Unknown error' });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value gives the failed result with a constant reason', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(await login(proxy)).toEqual({ success: false, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws gives the failed result with a constant reason', async () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(await login(hostile)).toEqual({ success: false, error: 'unreadable thrown value' });
+  });
+});
```
