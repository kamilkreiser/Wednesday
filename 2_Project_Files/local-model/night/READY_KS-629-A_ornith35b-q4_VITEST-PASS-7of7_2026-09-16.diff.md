# READY — KS-629 PART A (kyc `livenessVideo` was accepted by the RUNTIME selfie schema and read by nothing — the declaration at `services/kyc/src/index.ts:534` is deleted; Part B removes it from the OpenAPI schema) — **KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a: "REMOVE the field from schema and spec (nothing reads it)")** — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, VITEST, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks629-ornith35b-night
# Source read by me (Wednesday): the product hunk is exactly ONE `-` line (`  livenessVideo: z.string().optional(), // Base64 encoded video`), nothing else; tsc after 0 lines. The new source-pin test (the ks386 shape: `index.ts` boots a listener at module load, so it is read as TEXT with comments stripped) is IDENTICAL to the brief's block (diff on non-comment lines: empty): at the tip 1 failed / 3 run by assertion (the declaration is code), after 3/3; A6 the whole kyc suite shows no new red. ⚠ The model NAMED THE FILE `ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` (the ticket's title, misleading) instead of the brief's `ks629a-liveness-video-removed-from-runtime-schema.test.ts` — the raising seat `git mv`s it to the brief's name before the PR (a rename, no content change).
# PR NOTES for the Sunday raising seat: (1) Part A + Part B (READY_KS-629-B_*, when held) ship as ONE PR: `index.ts` (one line), `kyc.openapi.ts` (the property block), the two source-pin tests, AND the regenerated `docs/openapi/secuura-api.yaml` (`npm run` the generator named in the yaml's own header — "never edit this YAML"; its `livenessVideo` block at `:4427` must disappear in the regenerated file); KS-629 → Done, citing Kam's 07:01 ruling. (2) Behaviour: `z.object` is non-strict, so a client still sending `livenessVideo` has it stripped silently — exactly what happened before, minus the false promise in the contract; state in the PR body that the field is REMOVED from the published contract (a breaking change to the spec, not to the runtime's observable behaviour). (3) Rename the test file as in the ⚠ above.

```diff
--- a/Blockchain/Dev/services/kyc/src/index.ts
+++ b/Blockchain/Dev/services/kyc/src/index.ts
@@ -531,7 +531,6 @@ const submitSelfieSchema = z.object({
 const submitSelfieSchema = z.object({
   verificationId: z.string().uuid(),
   selfieImage: z.string(), // Base64 encoded
-  livenessVideo: z.string().optional(), // Base64 encoded video
 });
 
 const reviewVerificationSchema = z.object({
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts
@@ -0,0 +1,47 @@
+/**
+ * KS-629 Part A — `livenessVideo` is GONE from the runtime selfie schema.
+ *
+ * The field was accepted by `submitSelfieSchema` (index.ts) and by the OpenAPI
+ * schema (Part B) and read by nothing; Kam ruled 2026-09-16 that both
+ * declarations go. `index.ts` boots a listener at module load, so this guard
+ * reads it as TEXT with comments stripped (the ks386 shape) rather than
+ * importing it.
+ */
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+
+/** Block comments and `//` comments removed, so the guard matches CODE, never prose (a `https://` survives). */
+function stripComments(source: string): string {
+  return source.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/(^|[^:])\/\/[^\n]*/g, '$1 ');
+}
+
+const CODE = stripComments(SRC);
+
+describe('KS-629 Part A — the runtime selfie schema no longer accepts livenessVideo', () => {
+  it('🔴 KS-629 — `livenessVideo` is not declared anywhere in the CODE of index.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('KS-629 control — `selfieImage` is still declared in the selfie schema', () => {
+    expect(CODE).toContain('selfieImage: z.string()');
+    expect(CODE).toContain('verificationId: z.string().uuid()');
+  });
+
+  it('KS-629 control — the comment stripper eats a comment and keeps a url', () => {
+    expect(stripComments('const a = 1; // livenessVideo: z.string()')).not.toContain('livenessVideo');
+    expect(stripComments("const d = 'https://docs.secuura.io';")).toContain('https://docs.secuura.io');
+  });
+});
```

# SUPERSEDED-BY (feed10 drafter, 2026-09-22 11:32:21 AEST): re-briefed at develop 8c2f7b3fd as `night/briefs/KS-629-R16B-LIVENESSRT.md` (golden RESULT: PASS (7/7) through tasks/code_patch/checker.sh; same one-line deletion at :534; the test rewritten ASCII / backslash-free / double-quote-free with a Red cells declaration). This READY is the 2026-09-1x pin; do not raise it.
