# READY — KS-1118 F-3b (comment_patch, comment lines only in the ks1103 test)
# Source read by Wednesday 20:52: the model's 19 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical before/after; C5 inside the named lines; C6/C7 byte-exact). Tip 19f1e5475; develop is now 20ab16f9a (#1018 auth users.ts + test, #1027 locks) — the raising seat re-applies at the then-current develop.
# PR NOTES: `Refs KS-1118 (F-3)`, never Closes (F-3a and F-3b raise together as ONE PR — one logical path, the ticket's F-3). TIER: comment-only → through-code. Run: runs/2026-09-17_ks1118-ornith35b-night2 (first sample).

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1103-verify-hash-field.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1103-verify-hash-field.test.ts
@@ -13,7 +13,12 @@
  * These cells pin the fix:
  *   - `hash` alone answers exactly as `contentHash` alone does (H1/H2 vs C1/C2);
- *   - `hash` is read LAST in the alias chain, so every body that worked before
+ *   - `hash` is read LAST in the alias chain, so a body carrying a pre-existing alias
  *     keeps its answer — the lookup sees the pre-existing alias, never `hash`,
  *     when both are present (P1/P2);
+ *   - narrowed (KS-1118 F-3): every body carrying a pre-existing alias keeps its
+ *     lookup value; documentId-only, documentData-only and alias bodies are
+ *     unchanged; a body pairing `hash` with `documentId` or `documentData` now
+ *     takes the hash strategy, as v2 already does -- no caller in the repo sends
+ *     that pairing;
  *   - both 400 messages now name every field they accept (V1, E4);
  *   - a malformed `hash` value now reaches the lookup like any other alias and
@@ -201,5 +206,5 @@
 
   // ---------------------------------------------------------------------------
-  // GREEN on both sides — every body that worked before keeps its answer
+  // GREEN on both sides -- every body carrying a pre-existing alias keeps its answer
   // ---------------------------------------------------------------------------
   it('C1 {contentHash} with no rows answers 200 verified:false from one lookup', async () => {
```
