# READY — KS-794 (verify-file responses declare `fileSize` — the ticket author's option 1: an OPTIONAL int on the two BASE schemas `VerifyResponse` and `V2VerifyResponse`) — Ornith ornith:35b (Q4_K_M), round 2 (`2026-09-15_ks794-ornith35b-night2`; r1 was Wednesday's brief defect — a throw-red cell, IMPROVEMENTS row) — checker PASS 7/7 at develop M55 `48e65c435`
# Source read by Wednesday 22:30: both product hunks are the brief's line byte-for-byte (`originate.openapi.ts` after :461 and after :649); the jest test reads the shared registry exactly as `ks978` does — 3 🔴 cells red BY ASSERTION at the tip, 2 controls green both trees; suite 637 → 642 green, tsc rc 0.
# PR NOTES for the raising seat: (1) the two 200-response NOTE descriptions at `originate.openapi.ts:2067-2070` and `:2116-2119` still say the field is NOT declared in the schema and point at KS-794 — amend them to 'declared optional in the schema (KS-794)'; (2) regenerate the committed openapi yaml and run `check:openapi` (a second file, outside Ornith's contract); (3) the ticket's option 1 was taken on the author's stated preference — say so in the PR body; (4) the harness auto-named nothing — the test file name is the brief's; (5) paths in the diff lack the `Blockchain/Dev/` prefix (the checker applied with --directory).

```diff
--- a/services/originate/src/__tests__/ks794-verify-file-responses-declare-filesize.test.ts
+++ b/services/originate/src/__tests__/ks794-verify-file-responses-declare-filesize.test.ts
@@ -0,0 +1,62 @@
+/**
+ * KS-794 — verify-file responses declare fileSize
+ */
+import { sharedRegistry } from '@secuura/shared';
+// Importing for the side effect: it registers the paths and schemas on the
+// shared registry so we can read them back without mocking anything.
+import '../originate.openapi';
+
+type AnyDef = Record<string, any>;
+
+const V1 = '/api/verification/verify-file';
+const V2 = '/api/v2/verification/verify-file';
+
+function postRoute(path: string): AnyDef {
+  const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+  const route = defs.find((d) => d.type === 'route' && d.route?.method === 'post' && d.route?.path === path);
+  return route?.route as AnyDef;
+}
+
+function response200Shape(route: AnyDef): AnyDef {
+  const schema = route?.responses?.[200]?.content?.['application/json']?.schema;
+  // zod-to-openapi keeps the ZodObject; .shape (or _def.shape()) lists the declared fields.
+  return schema?._def?.shape?.() ?? schema?.shape ?? {};
+}
+
+describe('KS-794 — verify-file responses declare fileSize', () => {
+  it('KS-794 control — both verify-file routes are registered at all', () => {
+    expect(postRoute(V1)).toBeDefined();
+    expect(postRoute(V2)).toBeDefined();
+  });
+
+  it('🔴 KS-794 — VerifyResponse (v1 verify-file 200) declares fileSize', () => {
+    expect(Object.keys(response200Shape(postRoute(V1)))).toContain('fileSize');
+  });
+
+  it('🔴 KS-794 — V2VerifyResponse (v2 verify-file 200) declares fileSize', () => {
+    expect(Object.keys(response200Shape(postRoute(V2)))).toContain('fileSize');
+  });
+
+  it('🔴 KS-794 — fileSize is declared OPTIONAL on both, so /verify and /v2/verify stay honest', () => {
+    expect(response200Shape(postRoute(V1)).fileSize?.isOptional?.()).toBe(true);
+    expect(response200Shape(postRoute(V2)).fileSize?.isOptional?.()).toBe(true);
+  });
+
+  it('KS-794 control — the fields that were already declared are still there', () => {
+    expect(Object.keys(response200Shape(postRoute(V1)))).toContain('verified');
+    expect(Object.keys(response200Shape(postRoute(V2)))).toContain('count');
+  });
+});
--- a/services/originate/src/originate.openapi.ts
+++ b/services/originate/src/originate.openapi.ts
@@ -458,6 +458,7 @@
   'VerifyResponse',
   z
     .object({
       verified: z.boolean(),
+      fileSize: z.number().int().optional().openapi({ description: 'Bytes of the uploaded body (KS-794).' }),
       documentId: z.string().optional(),
       certificationId: z.string().optional(),
       status: z.string().optional(),
@@ -646,6 +647,7 @@
   'V2VerifyResponse',
   z
     .object({
       hash: z.string().nullable().openapi({ description: 'Canonical sha256:-prefixed hash the lookup ran on; null for documentId-only lookups.' }),
       count: z.number().int(),
+      fileSize: z.number().int().optional().openapi({ description: 'Bytes of the uploaded body (KS-794).' }),
       matches: z.array(V2VerifyMatchSchema),
       verifiedAt: z.string(),
     })
```
