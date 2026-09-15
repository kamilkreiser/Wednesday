# READY — KS-975 ITEM 2 (`explicitScope`'s second line treated an explicit JSON `null` as ABSENT and fell through to `principalScope(caller)` — item 1's exact hole, for `null`; now a guard refuses `null` in either field before `claim()`, matching the schema's first line) — **KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a — "closing item 2's backstop hole in the same pass")** — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, VITEST, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks975-ornith35b-night2
# Source read by me (Wednesday): the product hunk is the brief's block byte-for-byte (two comment lines + `if (target.tenantId === null || target.userId === null) return null;` + the original `const tenant = claim(target.tenantId);` re-emitted; A3c 4/4 `+` lines present; :227-236 untouched; `claim()` untouched — `principalScope` still reads a null TOKEN claim as absent, by design). tsc after: 0 lines. The new test file's imports, consts and four `it` cells are IDENTICAL to the brief's block (diff on non-comment lines: empty): at the tip `{ tenantId: null }` and `{ userId: null }` fell through to the caller's bucket (2 failed / 4 run, by assertion, controls green); after 4/4; A6 the whole security suite shows no new red.
# PR NOTES for the Sunday raising seat: (1) TWO files: `Blockchain/Dev/services/security/src/rateLimitScope.ts` (:226 → three lines inside `explicitScope`) + the NEW `src/__tests__/ks975-item2-explicit-null-is-refused.test.ts`; together with the item-1 pin (READY_KS-975-item1_*) this closes KS-975 → Done, citing Kam's 07:01 ruling. (2) Behaviour: unreachable at the wire today (`resetRateLimitSchema` refuses `null` first) — the backstop now agrees with the schema; state that in the PR body so nobody reads it as a live fix. (3) The ticket's 14-shape table: the second line now refuses 13 of 14 explicitly (`null` joins the 12) and treats only `undefined` as omitted. (4) Apply the section as held (A2 applied FUZZY at -C1 — the model's context drifted by a line; the `-`/`+` lines are exact).

```diff
--- a/Blockchain/Dev/services/security/src/rateLimitScope.ts
+++ b/Blockchain/Dev/services/security/src/rateLimitScope.ts
@@ -223,7 +223,10 @@ export function explicitScope(
   target: { tenantId?: unknown; userId?: unknown },
   caller: RateLimitPrincipal | undefined | null,
 ): string | null {
-  const tenant = claim(target.tenantId);
+  // KS-975 item 2: an explicit JSON null is PRESENT-and-unusable, not omitted — the schema refuses it
+  // first; this second line must too, or `{ tenantId: null }` retargets the caller's own bucket.
+  if (target.tenantId === null || target.userId === null) return null;
+  const tenant = claim(target.tenantId);
   const targetUser = claim(target.userId);
   // A body field that is present but unusable is refused rather than treated as
   // absent - otherwise naming a blank scope silently retargets the CALLER's own
 
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks975-item2-explicit-null-is-refused.test.ts
@@ -0,0 +1,49 @@
+/**
+ * KS-975 item 2 — `explicitScope` refuses an explicit JSON `null` in either field.
+ *
+ * The second line behind the request schema (rateLimitScope.ts:222-236) refused 12 of the
+ * 14 unusable shapes and treated `null` as ABSENT (claim() at :86 returns ABSENT for null),
+ * so `{ tenantId: null }` fell through to `principalScope(caller)` — KS-970 item 1's hole,
+ * for null. The schema refuses null first; these cells pin the backstop.
+ */
+
+import { describe, it, expect } from 'vitest';
+import { explicitScope, principalScope } from '../rateLimitScope';
+
+const TENANT_A = 'a0000000-0000-4000-8000-00000000000a';
+const USER_1 = 'user-1';
+const caller = { tenantId: TENANT_A, userId: USER_1 };
+
+describe('KS-975 item 2 — an explicit null scope field is refused by the second line, never treated as omitted', () => {
+  it('🔴 KS-975 — { tenantId: null } is refused (null), not retargeted to the caller bucket', () => {
+    expect(explicitScope({ tenantId: null }, caller)).toBeNull();
+  });
+
+  it('🔴 KS-975 — { userId: null } is refused (null), not retargeted to the caller bucket', () => {
+    expect(explicitScope({ userId: null }, caller)).toBeNull();
+  });
+
+  it('KS-975 control — omitting both fields still targets the caller own bucket', () => {
+    expect(explicitScope({}, caller)).toBe(principalScope(caller));
+    expect(explicitScope({ tenantId: undefined }, caller)).toBe(principalScope(caller));
+  });
+
+  it('KS-975 control — a blank field is still refused (KS-970 item 1) and a named tenant still scopes', () => {
+    expect(explicitScope({ tenantId: '   ' }, caller)).toBeNull();
+    expect(explicitScope({ tenantId: TENANT_A }, caller)).not.toBeNull();
+  });
+});
```
