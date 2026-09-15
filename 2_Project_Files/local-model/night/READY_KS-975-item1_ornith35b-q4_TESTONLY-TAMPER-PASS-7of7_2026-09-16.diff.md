# READY — KS-975 ITEM 1 (rateLimitScope tri-state: a MALFORMED `sub` — numeric or blank, with no `userId` — is a REFUSAL on the ungated `/api/rate-limit/check`; the behaviour #894 shipped, now PINNED so it cannot silently revert to #893's tenant-bucket mapping) — **KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a: "keep the 403 and pin it")** — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, TEST-ONLY MODE with a tamper on `rateLimitScope.ts:118`, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks975-ornith35b-night
# Source read by me (Wednesday): the new test file's imports, consts and four `it` cells are IDENTICAL to the brief's block (diff on non-comment lines: empty); under the tamper (a MALFORMED `sub` mapped back to ABSENT — #893's behaviour) the two 🔴 cells fail BY ASSERTION (2 failed / 4 run, controls green); at the untouched tip 4/4; A6 the whole security suite shows no new red. The product file is UNTOUCHED (test-only; A3 asserts it).
# PR NOTES for the Sunday raising seat: (1) ONE file: `Blockchain/Dev/services/security/src/__tests__/ks975-malformed-sub-is-refused.test.ts`; KS-975 stays OPEN for item 2 (below) — close item 1 with a comment citing Kam's 07:01 ruling. (2) The ticket's fix-shape also asked for the DECISION to be stated in the product comment at `rateLimitScope.ts:114-116` ("`sub` substitutes for an ABSENT `userId` only…") — add one sentence there in the PR: "A MALFORMED `sub` is itself a refusal (KS-975 item 1, ruled 2026-09-16) — pinned by ks975-malformed-sub-is-refused.test.ts." (a comment-only edit; no model round needed). (3) ITEM 2 (explicitScope treats JSON `null` as ABSENT and falls through to `principalScope(caller)` — :86 `claim()` / :232 the second line) is a SEPARATE product change, briefed next as its own pin.

```diff
--- /dev/null
+++ b/services/security/src/__tests__/ks975-malformed-sub-is-refused.test.ts
@@ -0,0 +1,49 @@
+/**
+ * KS-975 item 1 — a MALFORMED `sub` (numeric, blank) with no `userId` is a REFUSAL.
+ *
+ * `principalScope` substitutes `sub` for an ABSENT `userId` (rateLimitScope.ts:118) and
+ * refuses on MALFORMED (:121). `claim(user?.sub)` can itself be MALFORMED, so a numeric or
+ * blank `sub` refuses — #894 shipped that; #893 had mapped it to the tenant-only bucket
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
+describe('KS-975 item 1 — a MALFORMED `sub` is a refusal, not a silent downgrade to the tenant bucket', () => {
+  it('🔴 KS-975 — a NUMERIC sub with no userId is refused (null), not scoped to the tenant bucket', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: 123 })).toBeNull();
+  });
+
+  it('🔴 KS-975 — a BLANK sub with no userId is refused (null), not scoped to the tenant bucket', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: '   ' })).toBeNull();
+  });
+
+  it('KS-975 control — a good sub scopes exactly as the same userId would', () => {
+    expect(principalScope({ tenantId: TENANT_A, sub: USER_1 })).not.toBeNull();
+    expect(principalScope({ tenantId: TENANT_A, sub: USER_1 })).toBe(principalScope({ tenantId: TENANT_A, userId: USER_1 }));
+  });
+
+  it('KS-975 control — an ABSENT sub with a tenant is NOT a refusal: tenant-only scope', () => {
+    expect(principalScope({ tenantId: TENANT_A })).not.toBeNull();
+    expect(principalScope({ tenantId: TENANT_A, sub: undefined })).toBe(principalScope({ tenantId: TENANT_A }));
+  });
+});
```
