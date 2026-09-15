# READY — KS-1172 PART A (originate: `note` + `verified` added to LIFECYCLE_EVENT_ACTIONS; the EXISTING pin test `lifecycleEventRepo.test.ts` MODIFIED IN PLACE — the first modify-in-place pin, via the new `test_file=` pin + `## Red cells`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run night5 19:01, re-checked 19:4x under the red_cells arm from a scratch clone; A2 --recount only)
# Source read by me (Wednesday): the product hunk is the brief's E1 exactly (two verbs + a two-line comment before `] as const;`); the test hunks are E2 (two list entries) + E3 (one 🔴 cell with the `certified` control) exactly. **Bundle with Part B into ONE PR for KS-1172; the Sunday seat also amends the pin cell's TITLE (left stale on purpose, a fourth edit), updates `docs/VOCABULARY.md` §2/§3, regenerates `docs/openapi/secuura-api.yaml`, and the deploy rebuilds the gateway image (it bakes the yaml). Stuart told on the ticket 19:47 (comment f427c34f): actioned Sunday. `certified` NOT included (not requested).**

```diff
--- a/Blockchain/Dev/services/originate/src/lifecycleActions.ts
+++ b/Blockchain/Dev/services/originate/src/lifecycleActions.ts
@@ -54,6 +54,10 @@ export const LIFECYCLE_EVENT_ACTIONS = [
   // (non-mutating, attach to the current doc). Pairs with the existing
   // delete/restore entries above; per PS-499 S stops omitting documentType
   // for these once this lands.
   'protect',
   'unprotect',
+  // KS-1172 (Stuart 2026-09-15): `note` (a user's short note on a document; payload = noteSha256/noteLength only)
+  // and `verified` (the Verify FLOW's completion event). Both non-mutating, KS-387 shape; paired in anchorSchema.ts.
+  'note',
+  'verified',
 ] as const;
 
 --- a/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
@@ -56,6 +56,8 @@ describe('LIFECYCLE_EVENT_ACTIONS vocabulary pin', () => {
         'rename',
         'restore',
         'unprotect',
+        'note',
+        'verified',
         'rights-unassign',
         'share-attach-consent',
         'share-expiry-change',
@@ -68,6 +70,14 @@ describe('LIFECYCLE_EVENT_ACTIONS vocabulary pin', () => {
       ].sort(),
     );
   });
+
+  it('🔴 KS-1172 — accepts note and verified (Stuart 2026-09-15); certified was NOT requested and stays out', () => {
+    expect(LIFECYCLE_EVENT_ACTIONS).toContain('note');
+    expect(LIFECYCLE_EVENT_ACTIONS).toContain('verified');
+    // CONTROL — green on both trees: widening must not admit a verb nobody asked for.
+    expect(LIFECYCLE_EVENT_ACTIONS).not.toContain('certified');
+  });
 });
 
```
