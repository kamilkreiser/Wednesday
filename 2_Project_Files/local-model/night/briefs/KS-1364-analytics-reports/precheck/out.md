```diff
--- a/Blockchain/Dev/services/analytics/src/analytics.openapi.ts
+++ b/Blockchain/Dev/services/analytics/src/analytics.openapi.ts
@@ -923,7 +923,7 @@
   summary: 'Generate an analytics report',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: ReportRequestSchema } } },
+    body: { content: { 'application/json': { schema: ReportRequestSchema } }, required: true },
   },
   responses: {
     // KS-475 (§6): the runtime answers 200 synchronously — the spec's 202
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts
@@ -0,0 +1,40 @@
+// KS-1364 (sweep 4): the published contract for POST /api/analytics/reports did not mark the request body
+// required, so a spec-driven caller (Schemathesis) sent no body at all and the handler (routes/analytics.ts,
+// ReportRequestSchema.parse) answered 400. That zod object requires type and period, so it rejects an absent
+// body, and the spec now says the body is required. This file renders the document the generator publishes,
+// from the shared registry the analytics module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../analytics.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'analytics (ks1364 reports pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: POST /api/analytics/reports publishes a REQUIRED request body', () => {
+  it('RED KS-1364 AR1: POST /api/analytics/reports marks its request body required', () => {
+    expect(operation('/api/analytics/reports', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 AC1: the body keeps its request schema and the operation keeps bearerAuth', () => {
+    expect(bodyRef('/api/analytics/reports')).toBe('#/components/schemas/AnalyticsReportRequest');
+    expect(operation('/api/analytics/reports', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1364 AC2: the request component still requires type and period, which is why an absent body is refused', () => {
+    const r = doc.components?.schemas?.AnalyticsReportRequest?.required ?? [];
+    expect([...r].sort()).toEqual(['period', 'type']);
+  });
+
+  it('control KS-1364 AC3: the sibling POST /api/analytics/exports keeps its request body schema', () => {
+    expect(bodyRef('/api/analytics/exports')).toBe('#/components/schemas/AnalyticsExportRequest');
+  });
+});
```
