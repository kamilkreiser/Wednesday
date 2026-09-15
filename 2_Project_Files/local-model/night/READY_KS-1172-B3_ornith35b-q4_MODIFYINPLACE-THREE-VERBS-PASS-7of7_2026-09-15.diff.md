# READY — KS-1172 + KS-1173 PART B (anchoring `anchorSchema.ts`: three verbs; `anchorSchema.test.ts` modified in place) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST RUN (run night10 20:33; supersedes the two-verb READY). TRANSITIONAL `certify` untouched — `certified` is a different verb.
# Source read by me (Wednesday): E1 three verbs; E2 the pin list (+3); E3 one 🔴 cell (three accepted; `attested` rejected as the control); the `it.each` cell covers the three automatically.

```diff
--- a/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
@@ -60,6 +60,11 @@ export const LIFECYCLE_VERBS = [
   'protect',
   'unprotect',
   'restore',
+  // KS-1172 (Stuart 2026-09-15): `note` (a user's short note on a document; payload = noteSha256/noteLength only)
+  // `certified` (the Certify FLOW completed) and `verified` (the Verify FLOW completed) — KS-1173. All non-mutating;
+  // paired in originate's lifecycleActions.ts.
+  'note',
+  'certified',
+  'verified',
 ] as const;
 
 --- a/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
@@ -61,6 +61,9 @@ describe('anchorDocumentSchema — KS-388 lifecycle verb vocabulary', () => {
         'sign',
         'unprotect',
         'upload',
+        'note',
+        'certified',
+        'verified',
         'view',
         'watermark',
       ].sort(),
@@ -79,6 +82,14 @@ describe('anchorDocumentSchema — KS-388 lifecycle verb vocabulary', () => {
     expect(result.success).toBe(false);
   });
 
+  it('🔴 KS-1172 / KS-1173 — accepts note, certified and verified on the flat path (Stuart 2026-09-15); an invented verb stays rejected', () => {
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'note' } }).success).toBe(true);
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'certified' } }).success).toBe(true);
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'verified' } }).success).toBe(true);
+    // CONTROL — false on both trees: widening must not admit a verb nobody asked for.
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'attested' } }).success).toBe(false);
+  });
+
   it('rejects a document-type CODE on the flat path (codes belong to originate, not anchors)', () => {
```
