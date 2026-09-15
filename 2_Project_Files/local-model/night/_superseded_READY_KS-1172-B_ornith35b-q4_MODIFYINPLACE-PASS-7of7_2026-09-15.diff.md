# READY — KS-1172 PART B (anchoring: `note` + `verified` added to LIFECYCLE_VERBS; the EXISTING pin test `anchorSchema.test.ts` MODIFIED IN PLACE) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run night4 18:59, re-checked 19:4x under the red_cells arm; A2 strict)
# Source read by me (Wednesday): E1 exactly (two verbs + comment before `] as const;` at :63; TRANSITIONAL untouched; ACCEPTED derives); E2 the pin list; E3 one 🔴 cell (note/verified accepted by `anchorDocumentSchema`, `certified` rejected as the control); the `it.each` cell covers both new verbs automatically (65/65 after). **Bundle with Part A — see its header for the Sunday seat's docs/yaml/title/deploy items.**

```diff
--- a/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
@@ -60,6 +60,10 @@ export const LIFECYCLE_VERBS = [
   'protect',
   'unprotect',
   'restore',
+  // KS-1172 (Stuart 2026-09-15): `note` (a user's short note on a document; payload = noteSha256/noteLength only)
+  // and `verified` (the Verify FLOW's completion event). Both non-mutating; paired in originate's lifecycleActions.ts.
+  'note',
+  'verified',
 ] as const;
 
 // ─────────────────────────────────────────────────────────────────────────────
--- a/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
@@ -61,6 +61,8 @@ describe('anchorDocumentSchema — KS-388 lifecycle verb vocabulary', () => {
         'sign',
         'unprotect',
         'upload',
+        'note',
+        'verified',
         'view',
         'watermark',
       ].sort(),
@@ -79,6 +81,13 @@ describe('anchorDocumentSchema — KS-388 lifecycle verb vocabulary', () => {
     const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'obliterate' } });
     expect(result.success).toBe(false);
   });
+
+  it('🔴 KS-1172 — accepts note and verified on the flat path (Stuart 2026-09-15); certified was NOT requested and stays rejected', () => {
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'note' } }).success).toBe(true);
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'verified' } }).success).toBe(true);
+    // CONTROL — false on both trees: widening must not admit a verb nobody asked for.
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'certified' } }).success).toBe(false);
+  });
 
   it('rejects a document-type CODE on the flat path (codes belong to originate, not anchors)', () => {
     // SSD_DOCUMENT is valid on POST /api/documents (originate, catalogue-validated) —
```
