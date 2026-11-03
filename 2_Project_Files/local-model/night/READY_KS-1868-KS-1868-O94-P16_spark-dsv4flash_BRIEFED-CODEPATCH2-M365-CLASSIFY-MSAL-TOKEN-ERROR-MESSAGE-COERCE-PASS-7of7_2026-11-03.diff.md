# READY — KS-1868-KS-1868-O94-P16 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/out.md.checker/patch.diff`** (from `ls` at 13:51 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:51 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `27fe5476526c4200b752449e04be689724289e6d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts } + { Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	0	Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts
53	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: token-manager.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts`; test(s): `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts 53 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1868 classifyMsalTokenError reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value is unclassified (null)', 'KS-1868 classifyMsalTokenError reads the thrown value safely RED ks1868 R2 an Error whose message getter throws is unclassified (null)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=295 failed=0 | after: total=300 failed=0` · `NEW reds: []` [baseline_suite.json total=295 failed=0; after_suite.json total=300 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts` (+8/-0 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts` (+53/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `27fe5476526c4200b752449e04be689724289e6d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p16_m365_token_manager_classify_msal_token_error_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts b/Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts
--- a/Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts
+++ b/Blockchain/Dev/services/m365-integration/src/auth/token-manager.ts
@@ -208,6 +208,14 @@
  */
 export function classifyMsalTokenError(error: unknown): ClassifiedMsalError | null {
   const err = error as { name?: unknown; errorCode?: unknown; message?: unknown; code?: unknown };
+  try {
+    void err?.name;
+    void err?.errorCode;
+    void err?.code;
+    void (typeof err?.message === 'string' ? err.message : String(error));
+  } catch {
+    return null;
+  }
   const name = typeof err?.name === 'string' ? err.name : '';
   const errorCode = typeof err?.errorCode === 'string' ? err.errorCode : '';
   const nodeCode = typeof err?.code === 'string' ? err.code : '';
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts
@@ -0,0 +1,53 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1868: classifyMsalTokenError (src/auth/token-manager.ts) maps what an MSAL token call threw to an honest 400/401/503, or null when it is
+// unclassified (the route then keeps its 500). It reads `name`, `errorCode`, `code` and `message` of the thrown value unguarded. A revoked Proxy
+// throws on every read and an Error whose `message` getter throws throws on the last: the function THROWS from inside the route's catch, where an
+// ordinary error is classified. An unreadable value is an unclassified failure: null, the route's 500.
+import { classifyMsalTokenError } from '../auth/token-manager';
+
+/** The classification, or the string 'rejected' when the function throws (an assertion can then fail on it). */
+function classify(value: unknown): unknown {
+  try {
+    return classifyMsalTokenError(value);
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 classifyMsalTokenError reads the thrown value safely', () => {
+  it('control ks1868 C1 a network_error is still a 503', () => {
+    expect(classify(Object.assign(new Error('x'), { errorCode: 'network_error' }))).toEqual({
+      status: 503,
+      code: 'SERVICE_UNAVAILABLE',
+      message: 'Microsoft identity platform unreachable',
+    });
+  });
+
+  it('control ks1868 C2 an InteractionRequiredAuthError is still a 401', () => {
+    const e = new Error('consent required');
+    e.name = 'InteractionRequiredAuthError';
+    expect(classify(e)).toEqual({ status: 401, code: 'UNAUTHORIZED', message: 'SSO token was rejected by the identity platform' });
+  });
+
+  it('control ks1868 C3 an unclassified thrown plain string is still null', () => {
+    expect(classify('something odd happened')).toBeNull();
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value is unclassified (null)', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(classify(proxy)).toBeNull();
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is unclassified (null)', () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(classify(hostile)).toBeNull();
+  });
+});
```
