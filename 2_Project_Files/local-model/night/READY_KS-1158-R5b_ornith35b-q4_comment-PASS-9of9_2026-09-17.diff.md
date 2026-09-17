# READY — KS-1158 R5 ks1058 half (comment_patch: re-point the ks1058 test header's `documentRepo.ts:480` at the shallow spread's current lines)
# Source read by Wednesday 22:13: the model's 2 +/- lines IDENTICAL to the brief's (python sequence compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict. Tip = develop 75ad0e55c.
# PR NOTES: `Refs KS-1158 (R5, ks1058 half)`, never Closes. A line reference in a comment moves when documentRepo.ts moves: re-read the cited lines at the raise tip. TIER: comment-only -> through-code. Run: runs/2026-09-17_ks1158-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts
@@ -4,3 +4,3 @@
  *
- * `updateDocument` shallow-spreads (`documentRepo.ts:480`, `{...doc, ...updates}`),
+ * `updateDocument` shallow-spreads (`documentRepo.ts:540-544`, `{...doc, ...updates}`),
  * so the object this writer builds does not merge into the prior blob — it
```
