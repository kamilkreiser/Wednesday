# READY — KS-629 PART B (kyc `livenessVideo` was declared in the published OpenAPI schema `KycSelfieUploadRequest` (`kyc.openapi.ts:195-200`) and mentioned in its KS-430 comment (`:184`), read by nothing — both gone; the KS-430 comment now records the KS-629 removal) — **KAM RULED 2026-09-16 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, option a: "REMOVE the field from schema and spec (nothing reads it)")** — Ornith ornith:35b (Q4_K_M) PASS 7/7 on the RETRY (r1 first sample changed only the property block and left the :184 comment mention — A3b partial; RETRY-ONCE carried the missed site), VITEST, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks629-ornith35b-night2/retry
# Source read by me (Wednesday): the applied block equals the brief's 13-line block (the model kept the unchanged `verificationId`/`selfieImage` lines as context and closed `selfieImage` with the `}),` that had closed `livenessVideo` — a net-identical file; tsc after 0 lines); the `-` lines are the four KS-430/KS-444 comment lines, `selfieImage`'s `}),`, and the six-line `livenessVideo` property. The new source-pin test (ks386 shape) is IDENTICAL to the brief's block (diff on non-comment lines: empty): at the tip 1 failed / 3 run by assertion (`:195` is code), after 3/3; A6 the whole kyc suite shows no new red.
# PR NOTES for the Sunday raising seat: (1) Ships with Part A (READY_KS-629-A_*) as ONE PR: `index.ts` (one line), `kyc.openapi.ts` (this block), the two source-pin tests, AND the REGENERATED `docs/openapi/secuura-api.yaml` (`:4427` `livenessVideo:` must disappear; the yaml's own header names the generator — "never edit this YAML"); `npm run check:openapi` (the KS-256 example guard) stays green — the example block never carried the field. KS-629 → Done, citing Kam's 07:01 ruling. (2) Contract change to state in the PR body: `livenessVideo` is REMOVED from the published selfie-upload schema (a spec-breaking change for any client that read it as a working upload; the runtime never processed it).

```diff
--- a/Blockchain/Dev/services/kyc/src/kyc.openapi.ts
+++ b/Blockchain/Dev/services/kyc/src/kyc.openapi.ts
@@ -182,19 +182,17 @@ const KycSelfieUploadRequestSchema = sharedRegistry.register(
     .object({
       // KS-430: runtime (submitSelfieSchema) also requires verificationId (the target
-      // session) and accepts an optional livenessVideo; the spec declared only
-      // selfieImage, so a spec-minimal body earned a 400. Reconciled to the live contract.
-      // KS-444: residual drift — verificationId is a uuid at runtime (session ids
-      // are uuids); published as documentation of reality.
+      // session); the spec declared only selfieImage, so a spec-minimal body earned a
+      // 400. Reconciled to the live contract. KS-629: `livenessVideo` was declared here
+      // and read by nothing — removed from schema and spec (Kam, 2026-09-16).
+      // KS-444: residual drift — verificationId is a uuid at runtime (session ids
+      // are uuids); published as documentation of reality.
       verificationId: z.string().uuid(),
       selfieImage: z.string().openapi({
         description:
           'Base64-encoded image bytes, optionally as a `data:<mime>;base64,` URI. ' +
           'Must be a real JPEG, PNG or WebP — verified from the bytes (KS-487 B-4). ' +
           'Anything else is a 400 INVALID_IMAGE.',
-      }),
-      livenessVideo: z.string().optional().openapi({
-        description:
-          'Accepted by the schema but NOT stored or processed by any code path ' +
-          'today — see KS-629. Documented as inert rather than left to read as a ' +
-          'working upload.',
       }),
     })
     .passthrough().openapi({
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks629b-liveness-video-removed-from-openapi-schema.test.ts
@@ -0,0 +1,47 @@
+/**
+ * KS-629 Part B — `livenessVideo` is GONE from the published OpenAPI selfie schema.
+ *
+ * The field was declared in `KycSelfieUploadRequest` (kyc.openapi.ts) and by the
+ * runtime schema (Part A) and read by nothing; Kam ruled 2026-09-16 that both
+ * declarations go. This guard reads the file as TEXT with comments stripped (the
+ * ks386 shape), so a comment that merely mentions the field cannot red it.
+ */
+
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const SRC = readFileSync(join(__dirname, '..', 'kyc.openapi.ts'), 'utf8');
+
+/** Block comments and `//` comments removed, so the guard matches CODE, never prose (a `https://` survives). */
+function stripComments(source: string): string {
+  return source.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/(^|[^:])\/\/[^\n]*/g, '$1 ');
+}
+
+const CODE = stripComments(SRC);
+
+describe('KS-629 Part B — the published selfie schema no longer declares livenessVideo', () => {
+  it('🔴 KS-629 — `livenessVideo` is not declared anywhere in the CODE of kyc.openapi.ts', () => {
+    expect(CODE).not.toContain('livenessVideo');
+  });
+
+  it('KS-629 control — `selfieImage` and `verificationId` are still declared in the selfie schema', () => {
+    expect(CODE).toContain("'KycSelfieUploadRequest'");
+    expect(CODE).toContain('selfieImage: z.string().openapi({');
+    expect(CODE).toContain('verificationId: z.string().uuid()');
+  });
+
+  it('KS-629 control — the comment stripper eats a comment and keeps a url', () => {
+    expect(stripComments('const a = 1; // livenessVideo: z.string()')).not.toContain('livenessVideo');
+    expect(stripComments("const d = 'https://docs.secuura.io';")).toContain('https://docs.secuura.io');
+  });
+});
```
