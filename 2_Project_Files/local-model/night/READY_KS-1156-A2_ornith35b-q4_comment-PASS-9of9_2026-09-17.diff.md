# READY — KS-1156-A2 (comment_patch, comment lines only: api-gateway scopes.ts :125-126 — OAuth tokens carried 'email' before KS-835 (#984, verified 2c3315f37), now 'oauth')
# Source read by Wednesday 21:10: the model's 9 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical; C5 inside the named lines; C6/C7 byte-exact). Tip = develop 75ad0e55c.
# PR NOTES: `Refs KS-1156 (A.2)`; raise A.2 + A.3 as ONE PR (one ticket path). TIER: comment-only → through-code. Run: runs/2026-09-17_ks1156-ornith35b-night2/out.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts
@@ -123,6 +123,7 @@
  *
  * 1. **No `authMethod` short-circuit.** `requireScope` returns `next()` for
- *    any principal whose `authMethod` is `jwt` or `email`. KS-835 records that
- *    OAuth-minted tokens carry the `email` label too, so that branch is an
+ *    any principal whose `authMethod` is `jwt` or `email`. Before KS-835 (#984)
+ *    OAuth-minted tokens carried the `email` label too (they now carry 'oauth'
+ *    and are gated on their granted scopes), so that branch was an
  *    open door, not a convenience. A new auth door must not inherit it — this
  *    one grants on the scope or the role, and on nothing else.
```
