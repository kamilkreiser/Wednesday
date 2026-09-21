# READY — KS-975-ITEM1-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks975-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 22:22 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,34 @@ declared old=0 new=34 actual old=0 new=36 ); every line byte-exact`; golden not located — no byte-identity claim is made.

**Held 22:22 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks975-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/security/src/__tests__/ks975-malformed-sub-is-refused.test.ts` (new). `+` lines 36 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `ITEM1` → red exactly ['RED KS-975 - a BLANK sub with no userId is refused (null), n', 'RED KS-975 - a NUMERIC sub with no userId is refused (null),']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks975-ornith35b-night/input.json`. Brief: `night/briefs/KS-975-ITEM1-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks975-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks975-malformed-sub-is-refused.test.ts
@@ -0,0 +1,34 @@
+/**
+ * KS-975 item 1 - a MALFORMED `sub` (numeric, blank) with no `userId` is a REFUSAL.
+ *
+ * `principalScope` substitutes `sub` for an ABSENT `userId` (rateLimitScope.ts:118) and
+ * refuses on MALFORMED (:121). `claim(user?.sub)` can itself be MALFORMED, so a numeric or
+ * blank `sub` refuses - #894 shipped that; #893 had mapped it to the tenant-only bucket
+ * (200 on the ungated /check). Ruled deliberate (Kam, 2026-09-16); these cells pin it so
+ * a future change cannot silently map a MALFORMED `sub` back to ABSENT (the KS-949 gate
+ * measured that restoring #893's behaviour left all 179 cells green).
+ */
+
+import { describe, it, expect } from 'vitest';
+import { principalScope } from '../rateLimitScope';
+
+const TENANT_A = 'a0000000-0000-4000-8000-00000000000a';
+const USER_1 = 'user-1';
+
+describe('KS-975 item 1 - a MALFORMED `sub` is a refusal, not a silent downgrade to the tenant bucket', () => {
+  it('RED KS-975 - a NUMERIC sub with no userId is refused (null), not scoped to the tenant bucket', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: 123 })).toBeNull();
+  });
+
+  it('RED KS-975 - a BLANK sub with no userId is refused (null), not scoped to the tenant bucket', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: '   ' })).toBeNull();
+  });
+
+  it('KS-975 control - a good sub scopes exactly as the same userId would', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: USER_1 })).not.toBeNull();
+    expect(principalScope({ tenantId: TENANT_A, sub: USER_1 })).toBe(principalScope({ tenantId: TENANT_A, userId: USER_1 }));
+  });
+
+  it('KS-975 control - an ABSENT sub with a tenant is NOT a refusal: tenant-only scope', () => {
+    expect(principalScope({ tenantId: TENANT_A })).not.toBeNull();
+    expect(principalScope({ tenantId: TENANT_A, sub: undefined })).toBe(principalScope({ tenantId: TENANT_A }));
+  });
+});
```
