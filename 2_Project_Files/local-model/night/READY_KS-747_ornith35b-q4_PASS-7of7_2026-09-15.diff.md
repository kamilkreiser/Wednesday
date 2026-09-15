# READY — KS-747 (spec drift: GET /api/security/keys now declares `organizationId` as a required uuid query parameter) — Ornith ornith:35b (Q4_K_M) FIRST SAMPLE (`2026-09-15_ks747-ornith35b-night`, 17 s, 541 tokens), re-checked by Wednesday 16:45 PASS 7/7 at develop M55 48e65c435. The runner refused it twice at A3b because Wednesday's v1 brief demanded a `-` line for an INSERT-ONLY edit; the model correctly emitted a pure insertion after :809 both times (the RETRY-ONCE fired and reproduced the same correct hunk). Brief amended (anchor, no must-change; backup `.v1-mustchange-2026-09-15`) and the first output re-checked: 2 🔴 red at the tip (no parameter declared) / control green (the DELETE's path param) / 3 green after / security suite Δ 0 / tsc 0.
# Source read by Wednesday: the product hunk inserts exactly `  request: { query: z.object({ organizationId: z.string().uuid() }) },` after `security:` inside the GET /api/security/keys registration (:801-824), the POST and DELETE registrations untouched; the test renders the document through the shared `generateOpenApiDocument` after importing the module and asserts the query parameter (required, string, uuid) and the sibling DELETE's path param as control. The handler is unchanged (the ticket's fix shape). The served contract (`/api/docs/openapi.json`) follows from the registry.

```diff
--- a/services/security/src/security.openapi.ts
+++ b/services/security/src/security.openapi.ts
@@ -806,6 +806,7 @@ sharedRegistry.registerPath({
     'Lists metadata only (no plaintext, no hash). Use /api/keys/validate ' +
     'to verify a specific key.',
   security: [{ bearerAuth: [] }],
+  request: { query: z.object({ organizationId: z.string().uuid() }) },
   responses: {
     400: commonErrorResponses[400],
     200: {
--- /dev/null
+++ b/services/security/src/__tests__/ks747-spec-drift-get-api-security-keys.test.ts
@@ -0,0 +1,25 @@
+import { describe, it, expect } from 'vitest';
+import '../security.openapi';
+import { generateOpenApiDocument } from '@secuura/shared';
+
+const doc = generateOpenApiDocument({ title: 'security (ks747 pin)', version: '0.0.0' });
+const getOp = doc.paths['/api/security/keys'].get;
+const params = getOp.parameters ?? [];
+const orgParam = params.find((p) => p.in === 'query' && p.name === 'organizationId');
+
+describe('KS-747 — GET /api/security/keys spec drift fix', () => {
+  it('🔴 KS-747 — GET /api/security/keys declares organizationId as a REQUIRED query parameter', () => {
+    expect(orgParam).toBeDefined();
+    expect(orgParam.required).toBe(true);
+  });
+
+  it('🔴 KS-747 — the declared organizationId is a uuid string', () => {
+    expect(orgParam?.schema?.type).toBe('string');
+    expect(orgParam?.schema?.format).toBe('uuid');
+  });
+
+  it('KS-747 control — the sibling DELETE /api/security/keys/{id} still declares its path parameter id', () => {
+    const del = doc.paths['/api/security/keys/{id}'].delete;
+    const idParam = (del.parameters ?? []).find((p) => p.in === 'path' && p.name === 'id');
+    expect(idParam).toBeDefined();
+  });
+});
```
