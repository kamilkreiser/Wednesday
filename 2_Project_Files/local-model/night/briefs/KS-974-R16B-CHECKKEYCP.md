# KS-974 R16B-CHECKKEYCP - Wednesday's task for Ornith, PART A of two (the `/check` key bound; Part B is the scope field): `checkRateLimitSchema.key` bounded by CODE POINTS, the same predicate as `/reset`'s `boundedByCodePoints`, plus a NEW test (code_patch, vitest, ONE product hunk in `services/security/src/index.ts`; re-brief of the STALE READY_KS-974-A at develop 8c2f7b3fd, written 11:30:35 AEST on 2026-09-22 by Wednesday's feed10 drafter from the file at the tip - `index.ts` :594-:609 read, `RATE_LIMIT_KEY_MAX` imported at `:32` from `./rateLimitScope` (`rateLimitScope.ts:48` `export const RATE_LIMIT_KEY_MAX = 256;`); the reference test `ks698-rate-limit-poison.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed10 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-974-A_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (Ornith PASS 7/7 first sample at develop 2026-09-15; the FEED 7 census typed it `comment` - it is a code_patch: one product hunk + one NEW test; its paths lacked the `Blockchain/Dev/` prefix, normalised here).
- The product at the tip is UNCHANGED since the READY (offset 0 with the prefix): `:597` `export const checkRateLimitSchema = z.object({`, `:598-:599` the KS-952 comment, `:600` `  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),`, `:601-:603` the `limit` / KS-698 comment / `windowMs` lines - all byte-exact at 8c2f7b3fd (the file is 1598 lines). `RATE_LIMIT_KEY_MAX` is imported at `:32` (`  RATE_LIMIT_KEY_MAX,` inside the `from './rateLimitScope'` import) and defined as `export const RATE_LIMIT_KEY_MAX = 256;` at `rateLimitScope.ts:48`. The `SECURITY_DISABLE_BOOT` seam (`:1566`) is at the tip, as `ks698-rate-limit-poison.test.ts` uses it.
- The READY's `+` lines carried a template literal (`${RATE_LIMIT_KEY_MAX}`) and its test carried `\u{...}` escapes and em-dashes; this brief writes the message by string concatenation and the astral character as `String.fromCodePoint(128512)`, so every `+` line is ASCII, backslash-free, double-quote-free and `$`-free. Same behaviour, same three cells.
- No file of this brief is on a live seat's list (security is neither Seat B's originate/anchoring/auth/shared nor Seat C's api-gateway; no round-18 PR and no held R15/R16 READY touches `services/security/src/index.ts` - the held `READY_KS-975-ITEM1-R15` pins `rateLimitScope.ts`, a different file). Ticket KS-974: Backlog, not archived, no PR attached (board read at drafting time). The READY's `:596` context line carries an em-dash; this brief's hunk starts at `:597` so every context line is ASCII.
- Part B (the `scope` field, `rateLimitScope.ts`) is a separate row; item 2's openapi description clause is the raising seat's polish. NOT in this task.

## What is wrong (one paragraph)
`POST /api/rate-limit/check` validates its `key` with `z.string().min(1).max(RATE_LIMIT_KEY_MAX)` (`Blockchain/Dev/services/security/src/index.ts:600`); zod's `.max()` counts UTF-16 CODE UNITS while the published contract (`maxLength: 256`) and the sibling `/reset` route (`boundedByCodePoints` in `requestSchemas.ts`) count CODE POINTS - so a key of 256 astral characters (512 code units) is REFUSED on the one route any caller can reach, and the refusal carries zod's default wording instead of the `/reset` message. The fix: E1 replaces the `.max()` with a `.refine()` over `[...value].length` (code points) carrying the `/reset` message `must not exceed 256 characters`, with a three-line KS-974 comment above it; plus one NEW vitest file that imports the exported schema through the `SECURITY_DISABLE_BOOT` seam and pins: 256 astral characters accepted (RED at the tip), 257 refused with the characters message (RED at the tip - the tip refuses with zod's default text), and 256 / 257 / empty ASCII keys behave as before (CONTROL). NOT in this task: `/reset`, `requestSchemas.ts`, `rateLimitScope.ts`, the openapi description.

## The exact change - ONE EDIT in `Blockchain/Dev/services/security/src/index.ts` (one hunk, header `@@ -597,7 +597,12 @@`)
E1 - `:600` (the one `-` line) is REPLACED by six lines (three comment lines + the three-line `.refine()` property); leading context `:597-:599`, trailing context `:601-:603`. Inside the hunk the lines run in exactly ONE sequence: context, then the `-` line, then the six `+` lines, then context.
```
@@ -597,7 +597,12 @@
 export const checkRateLimitSchema = z.object({
   // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and
   // stored it. This bounds one entry; `sweepExpired` bounds the map.
-  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
+  // KS-974 item 1: the published maxLength 256 counts CODE POINTS; zod .max() counts UTF-16
+  // code units, so 256 astral characters were refused on the one route anyone can reach.
+  // Same predicate as boundedByCodePoints on /reset (requestSchemas.ts).
+  key: z.string().min(1).refine((value) => [...value].length <= RATE_LIMIT_KEY_MAX, {
+    message: 'must not exceed ' + RATE_LIMIT_KEY_MAX + ' characters',
+  }),
   limit: z.number().int().min(1).default(100),
   // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.
   windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).default(60000),
```
Copy every `+` line byte for byte (two-space indent on the comment and `key:` lines, four on `message:`); the `-` line is the tip's `:600` exactly; every context line keeps its leading space. No blank line anywhere in this hunk. Do not touch any other line of the product file.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest`: `describe/it/expect/beforeAll` imported from `'vitest'`. No `jest.*`. Import ONLY what the cells use (the four names below are each used).

## The test - one NEW vitest file, importing the exported schema through the `SECURITY_DISABLE_BOOT` seam (the `ks698-rate-limit-poison.test.ts` shape)
File: `Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 31), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, no `$`, ASCII only.
```
+import { describe, it, expect, beforeAll } from 'vitest';
+
+const ASTRAL = String.fromCodePoint(128512);
+
+let checkRateLimitSchema: { safeParse: (v: unknown) => any };
+
+beforeAll(async () => {
+  process.env.SECURITY_DISABLE_BOOT = '1';
+  const mod: any = await import('../index');
+  ({ checkRateLimitSchema } = mod);
+});
+
+describe('KS-974 Part A: published vs runtime bound on the rate-limit check key', () => {
+  it('RED KS-974 A: 256 astral characters (256 code points, 512 code units) are inside the published bound', () => {
+    expect(checkRateLimitSchema.safeParse({ key: ASTRAL.repeat(256) }).success).toBe(true);
+  });
+
+  it('RED KS-974 A: past the bound, the refusal names it in characters, like /reset', () => {
+    const r = checkRateLimitSchema.safeParse({ key: ASTRAL.repeat(257) });
+    expect(r.success).toBe(false);
+    if (!r.success) {
+      expect(r.error.issues[0].message).toBe('must not exceed 256 characters');
+    }
+  });
+
+  it('control: 256 ASCII characters accepted, 257 refused, empty refused', () => {
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(256) }).success).toBe(true);
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(257) }).success).toBe(false);
+    expect(checkRateLimitSchema.safeParse({ key: '' }).success).toBe(false);
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-974 A: 256 astral characters (256 code points, 512 code units) are inside the published bound')` - at the untouched tip `.max(256)` counts 512 code units and refuses (`success` false), so `toBe(true)` fails by assertion; after E1 the refine counts 256 code points and accepts.
- RED `it('RED KS-974 A: past the bound, the refusal names it in characters, like /reset')` - at the tip 257 astral characters are refused with zod's default `String must contain at most 256 character(s)`, so the message assertion fails; after E1 the refine's message is `must not exceed 256 characters`.
- CONTROL `it('control: 256 ASCII characters accepted, 257 refused, empty refused')` - for ASCII keys code units equal code points, and `min(1)` still refuses the empty string: green on both trees.

## Red cells
- RED KS-974 A: 256 astral characters (256 code points, 512 code units) are inside the published bound
- RED KS-974 A: past the bound, the refusal names it in characters, like /reset

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:600` - **must change**: `  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),`
* `:597` - (correct) `export const checkRateLimitSchema = z.object({` - stays (E1's first leading context line)
* `:598` - (correct) `  // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and` - stays (leading context)
* `:599` - (correct) `  // stored it. This bounds one entry; `sweepExpired` bounds the map.` - stays (leading context)
* `:601` - (correct) `  limit: z.number().int().min(1).default(100),` - stays (trailing context)
* `:602` - (correct) `  // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.` - stays (trailing context)
* `:603` - (correct) `  windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).default(60000),` - stays (trailing context)
* `:32` - (correct) `  RATE_LIMIT_KEY_MAX,` - stays (the import of the bound the refine reads; defined 256 in `rateLimitScope.ts:48`)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/security/src/index.ts` / `+++ b/Blockchain/Dev/services/security/src/index.ts` (ONE hunk, header `@@ -597,7 +597,12 @@`, one `-` line, six `+` lines), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts` (one `@@ -0,0 +1,31 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
