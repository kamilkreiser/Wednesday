# KS-629 R16B-LIVENESSSPEC - Wednesday's task for Ornith, PART B of two (the published OpenAPI selfie schema; Part A is the runtime schema): remove the `livenessVideo` property block and its comment mention from `services/kyc/src/kyc.openapi.ts` and pin the absence with a NEW source-read test (code_patch, vitest, TWO product hunks - numbered, ascending, non-adjacent - each a single context / minus / plus / context block; re-brief of the STALE READY_KS-629-B at develop 8c2f7b3fd, written 11:28:16 AEST on 2026-09-22 by Wednesday's feed10 drafter from the file at the tip - `kyc.openapi.ts` :178-:206 read; the reference test `ks386-no-image-payload-written.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed10 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-629-B_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md` (Ornith PASS 7/7 on the retry at develop 48e65c435; the FEED 7 census typed it `comment` - it is a code_patch: a product block replaced + one NEW test). KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a): "KS-629 - kyc livenessVideo is accepted by spec and runtime and silently discarded: REMOVE the field from schema and spec (nothing reads it)." That ruling is this brief's authority.
- The product at the tip is UNCHANGED since the old brief (offset 0): `:183-:200` byte-exact at 8c2f7b3fd (`KycSelfieUploadRequestSchema`, the KS-430 / KS-444 comment lines, `verificationId`, the `selfieImage` property and the six-line `livenessVideo` property); `grep -c livenessVideo kyc.openapi.ts` = 2 (`:184` the comment mention, `:195` the declaration; the file is 928 lines).
- The old READY's ONE 18-line hunk re-added nine unchanged lines as `+` lines (the builder's CONTEXT-AS-ADDITION gate now refuses that shape), so this brief re-cuts it as TWO minimal hunks: E1 the comment (`:184-:186`), E2 the property block (`:195-:200`). Two of the `-` lines carry an em-dash at the tip (`:186`, `:198`): they are declared `ascii_proxy U+2014=--` in the LINE-KEYED `## Where`, so you WRITE them with `--` where the tip has the em-dash and the checker restores the tip's bytes before applying (the KS-839 proof). Every `+` line is ASCII, backslash-free and double-quote-free; every context line is ASCII.
- The old READY's test file is ABSENT at the tip (no `ks629*` under `services/kyc/src/__tests__/`); no file of this brief is on a live seat's list (kyc is neither Seat B's originate/anchoring/auth/shared nor Seat C's api-gateway; no round-18 PR and no held R15/R16 READY touches `services/kyc/`). Ticket KS-629: Backlog, not archived, no PR attached (board read at drafting time).
- Part A (`index.ts:534`, brief `KS-629-R16B-LIVENESSRT.md`) is a separate row on a different file; the two ship as ONE PR with the REGENERATED `docs/openapi/secuura-api.yaml` (the raising seat runs the generator named in the yaml's header; never edit the YAML). NOT in this task.

## What is wrong (one paragraph)
The published OpenAPI schema `KycSelfieUploadRequest` (`Blockchain/Dev/services/kyc/src/kyc.openapi.ts:195-200`) declares `livenessVideo: z.string().optional().openapi({ description: 'Accepted by the schema but NOT stored or processed by any code path today - see KS-629 ...' })`, and the KS-430 comment above it (`:184`) says the runtime "accepts an optional livenessVideo" - while NO code path reads, stores or processes the field (Part A deletes the runtime declaration). A client reading the spec sees a working upload that does not exist. Kam ruled: remove the field from schema and spec. This task (Part B): E1 rewrites the KS-430 comment so it no longer mentions the field and records the KS-629 removal (the KS-444 line under it is re-written with a plain hyphen so the whole comment is ASCII), E2 deletes the six-line `livenessVideo` property; plus one NEW source-pin test proving `livenessVideo` is gone from the CODE of `kyc.openapi.ts` (comments stripped) while `KycSelfieUploadRequest`, `selfieImage` and `verificationId` stay declared. NOT in this task: `index.ts`, the example block (`:203-:210`, it never carried the field), the generated YAML.

## The exact change - TWO EDITS in `Blockchain/Dev/services/kyc/src/kyc.openapi.ts` (two hunks, NUMBERED, in ASCENDING line order; copy both headers)
THE ORDER IS THE TASK. Hunk 1 at `:183` comes BEFORE hunk 2 at `:193`; emit them in this order, each under its own `@@` header, never merged into one hunk. Inside EVERY hunk the lines run in exactly ONE sequence: context lines, then `-` lines, then `+` lines, then context lines.
E1 (hunk 1, header `@@ -183,5 +183,6 @@`) - the three comment lines `:184-:186` (the KS-430 sentence that names `livenessVideo` and the KS-444 line with the em-dash) become four ASCII comment lines; leading context `:183`, trailing context `:187`. The `-` line for `:186` is written with `--` where the tip has the em-dash (ascii_proxy, see `## Where`).
E2 (hunk 2, header `@@ -193,10 +194,4 @@`) - the six-line `livenessVideo` property `:195-:200` is DELETED (six `-` lines, NO `+` line); leading context `:193-:194`, trailing context `:201-:202`. The `-` line for `:198` is written with `--` where the tip has the em-dash (ascii_proxy). New-side start 194 = 193 + the 1 line E1 adds.
```
@@ -183,5 +183,6 @@
       // KS-430: runtime (submitSelfieSchema) also requires verificationId (the target
-      // session) and accepts an optional livenessVideo; the spec declared only
-      // selfieImage, so a spec-minimal body earned a 400. Reconciled to the live contract.
-      // KS-444: residual drift -- verificationId is a uuid at runtime (session ids
+      // session); the spec declared only selfieImage, so a spec-minimal body earned a
+      // 400. Reconciled to the live contract. KS-629: livenessVideo was declared here
+      // and read by nothing - removed from schema and spec (Kam, 2026-09-16).
+      // KS-444: residual drift - verificationId is a uuid at runtime (session ids
       // are uuids); published as documentation of reality.
@@ -193,10 +194,4 @@
           'Anything else is a 400 INVALID_IMAGE.',
       }),
-      livenessVideo: z.string().optional().openapi({
-        description:
-          'Accepted by the schema but NOT stored or processed by any code path ' +
-          'today -- see KS-629. Documented as inert rather than left to read as a ' +
-          'working upload.',
-      }),
     })
     .passthrough().openapi({
```
Copy every `+` line byte for byte (six-space indent, `//` comments); the `-` lines are the tip's `:184-:186` and `:195-:200` exactly EXCEPT the two proxied em-dashes written as `--`; every context line keeps its leading space. No blank line anywhere in these two hunks.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest`: `describe/it/expect` imported from `'vitest'`. No `jest.*`. `noUnusedLocals` is on: import ONLY what the cells use (the three imports below are each used).

## The test - one NEW vitest file, a SOURCE PIN in the ks386 shape (the file is READ as text, never imported, so a comment that merely mentions the field cannot red it)
File: `Blockchain/Dev/services/kyc/src/__tests__/ks629b-liveness-video-removed-from-openapi-schema.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629b-liveness-video-removed-from-openapi-schema.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 64), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only.
```
+// KS-629 Part B: livenessVideo is GONE from the published OpenAPI selfie schema.
+//
+// The field was declared in KycSelfieUploadRequest (kyc.openapi.ts) and by the
+// runtime schema (Part A) and read by nothing; Kam ruled 2026-09-16 that both
+// declarations go. This guard reads the file as TEXT with comments stripped (the
+// ks386 shape), so a comment that merely mentions the field cannot red it.
+// The stripper walks lines with indexOf: no regex, no escapes.
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const NL = String.fromCharCode(10);
+const SRC = readFileSync(join(__dirname, '..', 'kyc.openapi.ts'), 'utf8');
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
+describe('KS-629 Part B: the published selfie schema no longer declares livenessVideo', () => {
+  it('RED KS-629 B: livenessVideo is not declared anywhere in the code of kyc.openapi.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('control: KycSelfieUploadRequest, selfieImage and verificationId are still declared in the selfie schema', () => {
+    expect(CODE).toContain('KycSelfieUploadRequest');
+    expect(CODE).toContain('selfieImage: z.string().openapi({');
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
- RED `it('RED KS-629 B: livenessVideo is not declared anywhere in the code of kyc.openapi.ts')` - at the untouched tip `:195` declares `livenessVideo` in code (the `:184` comment mention is stripped, the declaration is not), so `not.toContain` fails by assertion; after E1+E2 no `livenessVideo` remains in the file (measured: `grep -c` = 2 at the tip, `:184` + `:195`, both removed).
- CONTROL `it('control: KycSelfieUploadRequest, selfieImage and verificationId are still declared in the selfie schema')` - `:180`, `:188`, `:189` are untouched on both trees.
- CONTROL `it('control: the comment stripper eats a line comment and a block comment and keeps a url')` - pure function of the stripper; green on both trees.

## Red cells
- RED KS-629 B: livenessVideo is not declared anywhere in the code of kyc.openapi.ts

## Where (line-keyed - every **must change** line must appear as a `-` line AT ITS NUMBER; the (correct) ones stay)
* `:184` - **must change**: `      // session) and accepts an optional livenessVideo; the spec declared only` - the first `-` line of E1
* `:185` - **must change**: `      // selfieImage, so a spec-minimal body earned a 400. Reconciled to the live contract.` - the second `-` line of E1
* `:186` - **must change**: `      // KS-444: residual drift -- verificationId is a uuid at runtime (session ids` - the third `-` line of E1, written with `--` for the tip's em-dash. ascii_proxy U+2014=--
* `:195` - **must change**: `      livenessVideo: z.string().optional().openapi({` - the first `-` line of E2
* `:196` - **must change**: `        description:` - E2
* `:197` - **must change**: `          'Accepted by the schema but NOT stored or processed by any code path ' +` - E2
* `:198` - **must change**: `          'today -- see KS-629. Documented as inert rather than left to read as a ' +` - E2, written with `--` for the tip's em-dash. ascii_proxy U+2014=--
* `:199` - **must change**: `          'working upload.',` - E2
* `:200` - **must change**: `      }),` - the last `-` line of E2 (the close of the livenessVideo property; the `}),` at `:194` that closes selfieImage STAYS)
* `:183` - (correct) `      // KS-430: runtime (submitSelfieSchema) also requires verificationId (the target` - stays (E1's leading context)
* `:187` - (correct) `      // are uuids); published as documentation of reality.` - stays (E1's trailing context)
* `:193` - (correct) `          'Anything else is a 400 INVALID_IMAGE.',` - stays (E2's leading context)
* `:194` - (correct) `      }),` - stays (E2's leading context; it closes selfieImage)
* `:201` - (correct) `    })` - stays (E2's trailing context)
* `:202` - (correct) `    .passthrough().openapi({` - stays (E2's trailing context)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/kyc/src/kyc.openapi.ts` / `+++ b/Blockchain/Dev/services/kyc/src/kyc.openapi.ts` with the E1 and E2 hunks IN THAT ORDER (headers `@@ -183,5 +183,6 @@`, `@@ -193,10 +194,4 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629b-liveness-video-removed-from-openapi-schema.test.ts` (one `@@ -0,0 +1,64 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; the two proxied `-` lines carry `--` exactly as printed; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
