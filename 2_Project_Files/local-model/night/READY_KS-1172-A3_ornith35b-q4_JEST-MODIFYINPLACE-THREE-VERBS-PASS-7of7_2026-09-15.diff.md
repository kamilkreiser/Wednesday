# READY — KS-1172 + KS-1173 PART A (originate `lifecycleActions.ts`: `note`, `certified`, `verified` added; the EXISTING pin `lifecycleEventRepo.test.ts` MODIFIED in place) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST RUN on the three-verb brief (run night9 20:30; supersedes the two-verb READY of 19:4x, kept beside as `_superseded_*`). Stuart's KS-1173 (18:51, blocks PS-836/837/862) is the ticket of record for `certified`.
# Source read by me (Wednesday): E1 three verbs + a two-line comment before `] as const;`; E2 the pin list (+3); E3 one 🔴 cell with `not.toContain('declare')` as the control (a verb WITH a dedicated route). **Sunday: ONE PR for KS-1172 + KS-1173 (A+B+D), close both; amend the pin-cell TITLES; regenerate the OpenAPI yaml; gateway image rebuilt on deploy; S adoption pinged on DEPLOY.**

```diff
--- a/Blockchain/Dev/services/originate/src/lifecycleActions.ts
+++ b/Blockchain/Dev/services/originate/src/lifecycleActions.ts
@@ -54,6 +54,11 @@ export const LIFECYCLE_EVENT_ACTIONS = [
   // delete/restore entries above; per PS-499 S stops omitting documentType
   // for these once this lands.
   'protect',
   'unprotect',
+  // KS-1172 (Stuart 2026-09-15): `note` (a user's short note on a document; payload = noteSha256/noteLength only)
+  // `certified` (the Certify FLOW completed) and `verified` (the Verify FLOW completed) — KS-1173. All non-mutating,
+  // KS-387 shape; paired in anchorSchema.ts.
+  'note',
+  'certified',
+  'verified',
 ] as const;
 
 --- a/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
@@ -57,6 +57,9 @@ describe('LIFECYCLE_EVENT_ACTIONS vocabulary pin', () => {
         'rename',
         'restore',
         'unprotect',
+        'note',
+        'certified',
+        'verified',
         'rights-unassign',
         'share-attach-consent',
         'share-expiry-change',
@@ -68,6 +71,15 @@ describe('LIFECYCLE_EVENT_ACTIONS vocabulary pin', () => {
         'share-revoke',
         'share-token-rotate',
       ].sort(),
     );
   });
+
+  it('🔴 KS-1172 / KS-1173 — accepts note, certified and verified (Stuart 2026-09-15); declare keeps its dedicated route', () => {
+    expect(LIFECYCLE_EVENT_ACTIONS).toContain('note');
+    expect(LIFECYCLE_EVENT_ACTIONS).toContain('certified');
+    expect(LIFECYCLE_EVENT_ACTIONS).toContain('verified');
+    // CONTROL — green on both trees: a verb WITH a dedicated K route is never accepted here.
+    expect(LIFECYCLE_EVENT_ACTIONS).not.toContain('declare');
+  });
 });
```
