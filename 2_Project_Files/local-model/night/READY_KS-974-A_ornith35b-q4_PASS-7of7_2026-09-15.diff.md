# READY — KS-974 PART A of two (security `index.ts:600`: `/check`'s `key` bounded by CODE POINTS — the same predicate as `/reset`'s `boundedByCodePoints`, written inline because that helper is a non-exported `const` in `requestSchemas.ts`; the PR seat may hoist it — export + import — as polish)
# Source read by me (Wednesday): the product hunk is the brief byte-for-byte (comment + `.refine([...value].length <= RATE_LIMIT_KEY_MAX, { message })`); the test imports `checkRateLimitSchema` through the `SECURITY_DISABLE_BOOT` seam exactly as `ks698-rate-limit-poison.test.ts` does; two 🔴 cells (256 astral accepted; 257 astral refused with the `/reset` message) + one control (ASCII 256 / 257 / empty). Checker: A4 RED-FIRST 2 failed / 3 at the tip, A5 3/3 after, suite 213 → 216 green, NEW reds []. First sample, 48 s. Run: runs/2026-09-15_ks974-ornith35b-night2.
# PR NOTES: (1) the harness named the test file from the title — rename to `ks974-check-key-bound-code-points.test.ts` (Part B's file carries the SAME auto-name; the two must not collide — rename B to `ks974-scope-field-bounds-the-trimmed-value.test.ts`); (2) this hunk's paths lack the `Blockchain/Dev/` prefix — apply from `Blockchain/Dev/`; (3) item 2's openapi description clause (leading/trailing whitespace is stripped) is NOT in either part — the PR seat adds it to `security.openapi.ts` by hand; (4) bundle with Part B → ONE PR closing KS-974.

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -597,7 +597,12 @@ export {
 // behaviour — the schema was already module-level.
 export const checkRateLimitSchema = z.object({
   // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and
   // stored it. This bounds one entry; `sweepExpired` bounds the map.
-  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
+  // KS-974 item 1: the published `maxLength: 256` counts CODE POINTS; zod `.max()` counts UTF-16
+  // code units, so 256 astral characters were refused on the one route anyone can reach.
+  // Same predicate as `boundedByCodePoints` on /reset (requestSchemas.ts).
+  key: z.string().min(1).refine((value) => [...value].length <= RATE_LIMIT_KEY_MAX, {
+    message: `must not exceed ${RATE_LIMIT_KEY_MAX} characters`,
+  }),
   limit: z.number().int().min(1).default(100),
   // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.
   windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).default(60000),
--- /dev/null
+++ b/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts
@@ -0,0 +1,42 @@
+import { describe, it, expect, beforeAll } from 'vitest';
+
+let checkRateLimitSchema: { safeParse: (v: unknown) => any };
+
+beforeAll(async () => {
+  process.env.SECURITY_DISABLE_BOOT = '1';
+  const mod: any = await import('../index');
+  ({ checkRateLimitSchema } = mod);
+});
+
+describe('KS-974 — published vs runtime bound on rate-limit scope', () => {
+  it('\u{1F534} KS-974 \u2014 256 astral characters (256 code points, 512 code units) are inside the published bound', () => {
+    expect(checkRateLimitSchema.safeParse({ key: '\u{1F600}'.repeat(256) }).success).toBe(true);
+  });
+
+  it('\u{1F534} KS-974 \u2014 past the bound, the refusal names it in characters, like /reset', () => {
+    const r = checkRateLimitSchema.safeParse({ key: '\u{1F600}'.repeat(257) });
+    expect(r.success).toBe(false);
+    if (!r.success) {
+      expect(r.error.issues[0].message).toBe('must not exceed 256 characters');
+    }
+  });
+
+  it('KS-974 control \u2014 256 ASCII characters accepted; 257 refused; empty refused', () => {
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(256) }).success).toBe(true);
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(257) }).success).toBe(false);
+    expect(checkRateLimitSchema.safeParse({ key: '' }).success).toBe(false);
+  });
+});
```

# SUPERSEDED-BY (feed10 drafter, 2026-09-22 11:32:21 AEST): re-briefed at develop 8c2f7b3fd as `night/briefs/KS-974-R16B-CHECKKEYCP.md` (golden RESULT: PASS (7/7) through tasks/code_patch/checker.sh; paths normalised to Blockchain/Dev/; the template literal written as concatenation; the astral test character as String.fromCodePoint). This READY is the 2026-09-1x pin; do not raise it.
