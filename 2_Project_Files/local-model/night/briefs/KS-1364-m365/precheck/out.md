```diff
--- a/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
+++ b/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
@@ -598,7 +598,7 @@
   summary: 'Add a SharePoint site to a connection',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365AddSiteRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365AddSiteRequestSchema } }, required: true },
   },
   responses: {
     201: {
@@ -703,7 +703,7 @@
   summary: 'Sync a SharePoint drive item into the platform',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365SyncDocumentRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365SyncDocumentRequestSchema } }, required: true },
   },
   responses: {
     200: {
@@ -1016,7 +1016,7 @@
   tags: ['M365', 'Outlook'],
   summary: 'Verify a content hash via the Outlook add-in',
   request: {
-    body: { content: { 'application/json': { schema: M365VerifyHashRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365VerifyHashRequestSchema } }, required: true },
   },
   responses: {
     200: {
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts
@@ -0,0 +1,58 @@
+// KS-1364 (sweep 4): the published contracts for POST /api/m365/sites, POST /api/m365/documents/sync and
+// POST /api/m365/outlook/verify-hash did not mark the request body required, so a spec-driven caller
+// (Schemathesis) sent no body at all and all three handlers answered 400 (index.ts: addSiteSchema.parse,
+// syncDocumentSchema.parse, and an inline zod object for verify-hash). Each rejects an absent body, so the spec now
+// says the body is required. verify-hash stays public (KS-442). This file renders the document the generator
+// publishes, from the shared registry the m365-integration module populates on import. No server, no database,
+// no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../m365-integration.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'm365-integration (ks1364 pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: three m365 POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 MS1: POST /api/m365/sites marks its request body required', () => {
+    expect(operation('/api/m365/sites', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 MS2: POST /api/m365/documents/sync marks its request body required', () => {
+    expect(operation('/api/m365/documents/sync', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 MS3: POST /api/m365/outlook/verify-hash marks its request body required', () => {
+    expect(operation('/api/m365/outlook/verify-hash', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 MC1: the three bodies keep their request schemas', () => {
+    expect({
+      sites: bodyRef('/api/m365/sites'),
+      sync: bodyRef('/api/m365/documents/sync'),
+      hash: bodyRef('/api/m365/outlook/verify-hash'),
+    }).toEqual({
+      sites: '#/components/schemas/M365AddSiteRequest',
+      sync: '#/components/schemas/M365SyncDocumentRequest',
+      hash: '#/components/schemas/M365VerifyHashRequest',
+    });
+  });
+
+  it('control KS-1364 MC2: sites and sync keep bearerAuth, and verify-hash stays public', () => {
+    expect(operation('/api/m365/sites', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/m365/documents/sync', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/m365/outlook/verify-hash', 'post')?.security).toEqual([]);
+  });
+
+  it('control KS-1364 MC3: the sibling POST /api/teams/notify keeps its request body schema', () => {
+    expect(bodyRef('/api/teams/notify')).toBe('#/components/schemas/M365TeamsNotifyRequest');
+  });
+});
```
