# KS-974 R16B-SCOPETRIM - Wednesday's task for Ornith, PART B of two (the `/reset` scope fields; Part A is the `/check` key): `scopeField()` gains `.trim()` BEFORE `.min(1)` so `tenantId` / `userId` are bounded and encoded on the value the runtime USES, plus a NEW test (code_patch, vitest, ONE pure-insertion hunk in `services/security/src/requestSchemas.ts`; re-brief of the STALE READY_KS-974-B at develop 8c2f7b3fd, written 11:36:56 AEST on 2026-09-22 by Wednesday's feed10 drafter from the file at the tip - `requestSchemas.ts` :54-:90 read whole; the reference test `ks444-request-schemas.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed10 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-974-B_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (Ornith PASS 7/7 first sample at develop 2026-09-15; the FEED 7 census typed it `unknown` - it is a code_patch: one product hunk + one NEW test).
- The product at the tip is UNCHANGED since the READY (offset 0): `:60` `const scopeField = () =>`, `:61` `  z`, `:62` `    .string()`, `:63` `    .min(1)`, `:64-:66` the lone-surrogate refine - byte-exact at 8c2f7b3fd (the file is 90 lines); the code-point bound sits at `:68-:70` and the blank-refine at `:67`, both untouched; `resetRateLimitSchema` is exported at `:78`. `rateLimitScope.ts` trims the scope value it uses, so the published bound must be measured on the TRIMMED value.
- The READY's hunk wrote `.min(1)` as a `-` line and again as a `+` line (the builder's CONTEXT-AS-ADDITION gate now refuses that shape), so this brief is a PURE INSERTION of the one `.trim()` line ABOVE `:63`, with `:63` as the first trailing context line. Its test carried the red glyph and em-dashes; this brief's test is ASCII, backslash-free, double-quote-free and `$`-free, the red cells declared under `## Red cells`. Same behaviour, same three cells.
- No file of this brief is on a live seat's list (security is neither Seat B's originate/anchoring/auth/shared nor Seat C's api-gateway; no round-18 PR and no held R15/R16 READY touches `requestSchemas.ts`). Ticket KS-974: Backlog, not archived, no PR attached (board read at drafting time). Part A (`index.ts:600`, brief `KS-974-R16B-CHECKKEYCP.md`) is a separate row on a different file and a different test file; the two ship as ONE PR.
- NOT in this task: `index.ts`, `rateLimitScope.ts`, the openapi description clause (the raising seat's polish).

## What is wrong (one paragraph)
`POST /api/rate-limit/reset` validates its `tenantId` / `userId` scope fields with `scopeField()` (`Blockchain/Dev/services/security/src/requestSchemas.ts:60-:70`): `.min(1)`, the lone-surrogate refine, a blank refine and the code-point bound `[...value].length <= RATE_LIMIT_KEY_MAX` - all measured on the RAW value, while the runtime (`rateLimitScope.ts`) trims the value before it uses it. So a tenantId of 256 characters with one leading space (257 raw code points) is REFUSED although the value the runtime keys on is 256 and inside the published bound, and the parsed `data.tenantId` still carries the whitespace. The fix (the house idiom, CLAUDE.md KS-202): E1 inserts `.trim()` before `.min(1)`, so every later refine and the bound see the trimmed value and the parsed data is the trimmed value; `:67`'s blank refine stays, harmless. Plus one NEW vitest file importing `resetRateLimitSchema` (as `ks444-request-schemas.test.ts` does, no env, no boot) that pins: a leading-space tenantId of 256 accepted and returned trimmed (RED at the tip), a trailing-space userId likewise (RED), and 257 non-blank refused / blank refused / key-only accepted (CONTROL).

## The exact change - ONE INSERTION in `Blockchain/Dev/services/security/src/requestSchemas.ts` (one hunk, header `@@ -60,6 +60,7 @@`)
E1 - a PURE INSERTION: NO `-` line; the one `+` line goes between `:62` (`    .string()`) and `:63` (`    .min(1)`); leading context `:60-:62`, trailing context `:63-:65`. Inside the hunk the lines run in exactly ONE sequence: three context lines, the one `+` line, three context lines. Four-space indent, as the chain uses.
```
@@ -60,6 +60,7 @@
 const scopeField = () =>
   z
     .string()
+    .trim() // KS-974 item 2: bound and encode the value the runtime USES (rateLimitScope.ts trims)
     .min(1)
     .refine((value) => !hasLoneSurrogate(value), {
       message: 'must not contain an unpaired surrogate',
```
Copy the `+` line byte for byte; every context line keeps its leading space (`:63` `    .min(1)` is CONTEXT - it survives the edit; never write it as a `-` or a `+`). No blank line anywhere in this hunk. Do not touch any other line of the product file.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest`: `describe/it/expect` imported from `'vitest'`. No `jest.*`. Import ONLY what the cells use (the names below are each used).

## The test - one NEW vitest file importing the exported schema directly (the `ks444-request-schemas.test.ts` shape: no env, no boot)
File: `Blockchain/Dev/services/security/src/__tests__/ks974-scope-field-bounds-the-trimmed-value.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-scope-field-bounds-the-trimmed-value.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 30), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, no `$`, ASCII only.
```
+// KS-974 Part B: the published maxLength is measured on the TRIMMED scope value, like the runtime.
+
+import { describe, it, expect } from 'vitest';
+import { resetRateLimitSchema } from '../requestSchemas';
+
+const KEY = 'login:1.2.3.4';
+
+describe('KS-974 Part B: published bound vs runtime bound on the rate-limit scope fields', () => {
+  it('RED KS-974 B: a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one', () => {
+    const r = resetRateLimitSchema.safeParse({ key: KEY, tenantId: ' ' + 'a'.repeat(256) });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.tenantId).toBe('a'.repeat(256));
+    }
+  });
+
+  it('RED KS-974 B: the same for userId, with trailing whitespace', () => {
+    const r = resetRateLimitSchema.safeParse({ key: KEY, userId: 'u'.repeat(256) + '  ' });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.userId).toBe('u'.repeat(256));
+    }
+  });
+
+  it('control: 257 non-blank characters still refused, a blank scope field still refused, key alone accepted', () => {
+    expect(resetRateLimitSchema.safeParse({ key: KEY, tenantId: 'a'.repeat(257) }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: KEY, tenantId: '   ' }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: KEY }).success).toBe(true);
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-974 B: a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one')` - at the untouched tip the raw value is 257 code points, so the bound refine refuses (`success` false: assertion red); after E1 the trimmed value is 256, accepted, and `data.tenantId` is the trimmed string.
- RED `it('RED KS-974 B: the same for userId, with trailing whitespace')` - the same on `userId` with two trailing spaces (258 raw); after E1 accepted and trimmed.
- CONTROL `it('control: 257 non-blank characters still refused, a blank scope field still refused, key alone accepted')` - the bound, the blank refine (`:67`; after E1 `.min(1)` on the trimmed empty string refuses first) and the optional scope fields behave the same on both trees.

## Red cells
- RED KS-974 B: a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one
- RED KS-974 B: the same for userId, with trailing whitespace

## Where (parsed into the checklist; this edit is a pure insertion - NO line changes, every named line stays and is context)
* `:60` - (correct) `const scopeField = () =>` - stays (E1's first leading context line)
* `:61` - (correct) `  z` - stays (leading context)
* `:62` - (correct) `    .string()` - stays (leading context; the `+` line goes directly under it)
* `:63` - (correct) `    .min(1)` - stays (E1's first trailing context line; the `+` line goes directly above it)
* `:64` - (correct) `    .refine((value) => !hasLoneSurrogate(value), {` - stays (trailing context)
* `:65` - (correct) `      message: 'must not contain an unpaired surrogate',` - stays (trailing context)
* `:67` - (correct) `    .refine((value) => value.trim().length > 0, { message: 'must not be blank' })` - stays (harmless after the trim)
* `:78` - (correct) `export const resetRateLimitSchema = z.object({` - stays (the schema the test imports)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/security/src/requestSchemas.ts` / `+++ b/Blockchain/Dev/services/security/src/requestSchemas.ts` (ONE hunk, header `@@ -60,6 +60,7 @@`, no `-` line, one `+` line), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-scope-field-bounds-the-trimmed-value.test.ts` (one `@@ -0,0 +1,30 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
