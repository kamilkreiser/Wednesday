# KS-629 R16B-LIVENESSRT - Wednesday's task for Ornith, PART A of two (the RUNTIME selfie schema; Part B is the OpenAPI schema): delete the ONE `livenessVideo` declaration line in `services/kyc/src/index.ts` and pin its absence with a NEW source-read test (code_patch, vitest; re-brief of the STALE READY_KS-629-A at develop 8c2f7b3fd, written 11:24:11 AEST on 2026-09-22 by Wednesday's feed10 drafter from the file at the tip - `index.ts` :525-:545 and :905-:935 read; the reference test `ks386-no-image-payload-written.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed10 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-629-A_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md` (Ornith PASS 7/7 at develop 48e65c435; the FEED 7 census typed it `comment` - it is a code_patch: one product `-` line + one NEW test). KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a): "KS-629 - kyc livenessVideo is accepted by spec and runtime and silently discarded: REMOVE the field from schema and spec (nothing reads it)." That ruling is this brief's authority.
- The product at the tip is UNCHANGED since the old brief (offset 0): `:533` `  selfieImage: z.string(), // Base64 encoded`, `:534` `  livenessVideo: z.string().optional(), // Base64 encoded video`, `:535` `});` - all three byte-exact at 8c2f7b3fd; `grep -c livenessVideo index.ts` = 1 (the declaration only; the file is 1261 lines). The handler `:909` `    const data = submitSelfieSchema.parse(req.body);` is untouched.
- The old READY's test file is ABSENT at the tip (no `ks629*` under `services/kyc/src/__tests__/`), and no file of this brief is on a live seat's list (kyc is neither Seat B's originate/anchoring/auth/shared nor Seat C's api-gateway; no round-18 PR and no held R15/R16 READY touches `services/kyc/`). Ticket KS-629: Backlog, not archived, no PR attached (board read at drafting time).
- The old test's `+` lines carried non-ASCII (em-dashes, the red glyph), backslashes (regex escapes) and a double-quoted string; this brief's test is REWRITTEN so every `+` line is ASCII, backslash-free and double-quote-free: the comment stripper walks lines with `indexOf` (no regex), the red cell is declared under `## Red cells` with an ASCII title, and the url control feeds a quote-free string. Same three cells, same meaning.
- Part B (`kyc.openapi.ts`, a separate brief) and the regenerated `docs/openapi/secuura-api.yaml` (the raising seat runs the generator; never edit the YAML) are NOT in this task.

## What is wrong (one paragraph)
`POST /api/kyc/{id}/selfie` accepts `livenessVideo` in its runtime Zod schema (`Blockchain/Dev/services/kyc/src/index.ts:534` `  livenessVideo: z.string().optional(), // Base64 encoded video`) and in the OpenAPI schema (`kyc.openapi.ts`, Part B), and NO code path reads, stores or processes it - the handler at `:909` parses the body and sets `livenessCompleted: true` in mock mode regardless. A caller who uploads liveness evidence gets `success: true` and the bytes are discarded: a contract advertising a capability the runtime does not have. Kam ruled: remove the field. This task (Part A): delete the ONE runtime declaration line, plus one NEW source-pin test proving `livenessVideo` is gone from the CODE of `index.ts` (comments stripped) while `selfieImage` and `verificationId` stay declared. `z.object` is non-strict, so a client still sending the field has it STRIPPED (as before, the bytes were discarded) - the contract no longer advertises it. NOT in this task: the handler (:905-:960), `kyc.openapi.ts`, any other schema.

## The exact change - ONE DELETION in `Blockchain/Dev/services/kyc/src/index.ts` (one hunk, header `@@ -533,3 +533,2 @@`)
E1 - line 534 DELETED: one `-` line, NO `+` line; leading context `:533`, trailing context `:535` - both copied from the file byte for byte, each with its leading space.
```
@@ -533,3 +533,2 @@
   selfieImage: z.string(), // Base64 encoded
-  livenessVideo: z.string().optional(), // Base64 encoded video
 });
```
Do not touch any other line of the product file. No `+` line in the product hunk. The hunk's old side is 3 lines (2 context + 1 minus), its new side 2.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest`: `describe/it/expect` imported from `'vitest'`. No `jest.*`. `noUnusedLocals` is on: import ONLY what the cells use (the three imports below are each used).

## The test - one NEW vitest file, a SOURCE PIN in the ks386 shape (`index.ts` boots a listener at module load, so it is READ as text, never imported)
File: `Blockchain/Dev/services/kyc/src/__tests__/ks629a-liveness-video-removed-from-runtime-schema.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629a-liveness-video-removed-from-runtime-schema.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 63), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only.
```
+// KS-629 Part A: livenessVideo is GONE from the runtime selfie schema.
+//
+// The field was accepted by submitSelfieSchema (index.ts) and by the OpenAPI
+// schema (Part B) and read by nothing; Kam ruled 2026-09-16 that both
+// declarations go. index.ts boots a listener at module load, so this guard
+// reads it as TEXT with comments stripped (the ks386 shape) rather than
+// importing it. The stripper walks lines with indexOf: no regex, no escapes.
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const NL = String.fromCharCode(10);
+const SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+
+/** Block comments and line comments removed, so the guard matches CODE, never prose (a url keeps its colon-slash-slash). */
+function codeOnly(source: string): string {
+  const kept: string[] = [];
+  let inBlock = false;
+  for (const line of source.split(NL)) {
+    let text = line;
+    if (inBlock) {
+      const close = text.indexOf('*/');
+      if (close < 0) continue;
+      inBlock = false;
+      text = text.slice(close + 2);
+    }
+    const open = text.indexOf('/*');
+    if (open >= 0) {
+      const close = text.indexOf('*/', open + 2);
+      if (close < 0) {
+        inBlock = true;
+        text = text.slice(0, open);
+      } else {
+        text = text.slice(0, open) + ' ' + text.slice(close + 2);
+      }
+    }
+    if (text.trimStart().startsWith('//')) text = '';
+    const slash = text.indexOf(' //');
+    if (slash >= 0) text = text.slice(0, slash);
+    kept.push(text);
+  }
+  return kept.join(NL);
+}
+
+const CODE = codeOnly(SRC);
+
+describe('KS-629 Part A: the runtime selfie schema no longer accepts livenessVideo', () => {
+  it('RED KS-629 A: livenessVideo is not declared anywhere in the code of index.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('control: selfieImage and verificationId are still declared in the selfie schema', () => {
+    expect(CODE).toContain('selfieImage: z.string()');
+    expect(CODE).toContain('verificationId: z.string().uuid()');
+  });
+
+  it('control: the comment stripper eats a line comment and a block comment and keeps a url', () => {
+    expect(codeOnly('const a = 1; // livenessVideo: z.string()')).not.toContain('livenessVideo');
+    expect(codeOnly('/* livenessVideo */ const b = 2;')).not.toContain('livenessVideo');
+    expect(codeOnly('const d = https://docs.secuura.io;')).toContain('https://docs.secuura.io');
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-629 A: livenessVideo is not declared anywhere in the code of index.ts')` - at the untouched tip `:534` declares `livenessVideo` in code (the trailing `// Base64 encoded video` comment is stripped, the declaration is not), so `not.toContain` fails by assertion; after E1 no `livenessVideo` remains in `index.ts` (measured: `grep -c` = 1 at the tip, the declaration only).
- CONTROL `it('control: selfieImage and verificationId are still declared in the selfie schema')` - `:532` and `:533` are untouched on both trees.
- CONTROL `it('control: the comment stripper eats a line comment and a block comment and keeps a url')` - pure function of the stripper; green on both trees.

## Red cells
- RED KS-629 A: livenessVideo is not declared anywhere in the code of index.ts

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:534` - **must change**: `  livenessVideo: z.string().optional(), // Base64 encoded video`
* `:533` - (correct) `  selfieImage: z.string(), // Base64 encoded` - stays (E1's leading context)
* `:535` - (correct) `});` - stays (E1's trailing context)
* `:909` - (correct) `    const data = submitSelfieSchema.parse(req.body);` - stays (the handler is untouched)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/kyc/src/index.ts` / `+++ b/Blockchain/Dev/services/kyc/src/index.ts` (ONE hunk, header `@@ -533,3 +533,2 @@`, one `-` line, no `+` line), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629a-liveness-video-removed-from-runtime-schema.test.ts` (one `@@ -0,0 +1,63 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
