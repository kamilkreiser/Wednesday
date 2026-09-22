# READY — KS-974 PART B of two (security `requestSchemas.ts:63`: `scopeField()` gains `.trim()` BEFORE `.min(1)` — the house idiom (CLAUDE.md:173-181, KS-202) — so `tenantId` / `userId` on `/reset` are bounded and encoded on the value the runtime USES (`rateLimitScope.ts:88` trims); line 67's blank refine kept, harmless)
# Source read by me (Wednesday): the product hunk is the brief exactly (one line → `.trim() // KS-974 item 2 …` + `.min(1)`); the test imports only `resetRateLimitSchema` as `ks444-request-schemas.test.ts` does, no env, no boot; two 🔴 cells (a leading-space tenantId of 256 accepted with `data.tenantId` trimmed; a trailing-space userId likewise) + one control (257 refused / blank refused / key-only accepted). Checker: A4 RED-FIRST 2 failed / 3 at the tip, A5 3/3 after, suite 213 → 216 green, NEW reds []. First sample. Run: runs/2026-09-15_ks974-ornith35b-night3.
# PR NOTES: see Part A's — rename this test to `ks974-scope-field-bounds-the-trimmed-value.test.ts`; ONE PR with Part A; the openapi clause is the PR seat's.

```diff
--- a/Blockchain/Dev/services/security/src/requestSchemas.ts
+++ b/Blockchain/Dev/services/security/src/requestSchemas.ts
@@ -60,7 +60,8 @@ const boundedByCodePoints = (schema: z.ZodString) =>
 const scopeField = () =>
   z
     .string()
-    .min(1)
+    .trim() // KS-974 item 2: bound and encode the value the runtime USES (rateLimitScope.ts trims)
+    .min(1)
     .refine((value) => !hasLoneSurrogate(value), {
       message: 'must not contain an unpaired surrogate',
     })
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts
@@ -0,0 +1,32 @@
+/**
+ * KS-974 — published maxLength vs trimmed runtime bound on scope fields.
+ */
+
+import { describe, it, expect } from 'vitest';
+import { resetRateLimitSchema } from '../requestSchemas';
+
+describe('KS-974 — published bound vs runtime bound on rate-limit scope', () => {
+  it('🔴 KS-974 — a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one', () => {
+    const r = resetRateLimitSchema.safeParse({ key: 'login:1.2.3.4', tenantId: ' ' + 'a'.repeat(256) });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.tenantId).toBe('a'.repeat(256));
+    }
+  });
+
+  it('🔴 KS-974 — the same for userId, with trailing whitespace', () => {
+    const r = resetRateLimitSchema.safeParse({ key: 'login:1.2.3.4', userId: 'u'.repeat(256) + '  ' });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.userId).toBe('u'.repeat(256));
+    }
+  });
+
+  it('KS-974 control — 257 non-blank characters still refused; a blank scope field still refused; key alone accepted', () => {
+    expect(resetRateLimitSchema.safeParse({ key: 'login:1.2.3.4', tenantId: 'a'.repeat(257) }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: 'login:1.2.3.4', tenantId: '   ' }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: 'login:1.2.3.4' }).success).toBe(true);
+  });
+});
```

# SUPERSEDED-BY (feed10 drafter, 2026-09-22 11:37:36 AEST): re-briefed at develop 8c2f7b3fd as `night/briefs/KS-974-R16B-SCOPETRIM.md` (golden RESULT: PASS (7/7) through tasks/code_patch/checker.sh; the hunk re-cut as a pure insertion of `.trim()` above `.min(1)` - the READY re-added `.min(1)` as a `+` line, which the builder now refuses; the test rewritten ASCII). This READY is the 2026-09-15 pin; do not raise it.
