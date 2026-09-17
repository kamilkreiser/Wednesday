# READY — KS-1118 F-3a (comment_patch, comment lines only in the verification.ts)
# Source read by Wednesday 20:52: the model's 13 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical before/after; C5 inside the named lines; C6/C7 byte-exact). Tip 19f1e5475; develop is now 20ab16f9a (#1018 auth users.ts + test, #1027 locks) — the raising seat re-applies at the then-current develop.
# PR NOTES: `Refs KS-1118 (F-3)`, never Closes (F-3a and F-3b raise together as ONE PR — one logical path, the ticket's F-3). TIER: comment-only → through-code. Run: runs/2026-09-17_ks1118-ornith35b-night (first sample).

```diff
--- a/Blockchain/Dev/services/originate/src/routes/verification.ts
+++ b/Blockchain/Dev/services/originate/src/routes/verification.ts
@@ -737,7 +737,12 @@
 
       // Resolve the hash to verify against — accept multiple field names
-      // KS-1103: `hash` is read LAST so every body that worked before keeps its
+      // KS-1103: `hash` is read LAST so a body carrying a pre-existing alias keeps its
       // answer — when a pre-existing alias and `hash` are both present the lookup
       // still sees the alias. Before this change the chain stopped at documentHash.
+      // KS-1118 F-3, narrowed: every body carrying a pre-existing alias keeps its
+      // lookup value; documentId-only, documentData-only and alias bodies are
+      // unchanged; a body pairing `hash` with `documentId` or `documentData` now
+      // takes the hash strategy, as v2 already does -- no caller in the repo sends
+      // that pairing.
       const hashToVerify = providedHash || contentHash || documentHash || hash;
 
```
