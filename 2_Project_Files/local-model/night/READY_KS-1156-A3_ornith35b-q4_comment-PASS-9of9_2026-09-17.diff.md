# READY — KS-1156-A3 (comment_patch, comment lines only: ks835 test :59 — proxy.ts mounts the shape SEVEN times (measured at the tip), arrows ASCII)
# Source read by Wednesday 21:10: the model's 5 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical; C5 inside the named lines; C6/C7 byte-exact). Tip = develop 75ad0e55c.
# PR NOTES: `Refs KS-1156 (A.3)`; raises with A.2. TIER: comment-only → through-code. Run: runs/2026-09-17_ks1156-ornith35b-night3/out.md.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts
@@ -57,4 +57,4 @@
   configureAuth({ enableTestTokens: false, defaultTenantId: 'ten-1', securityServiceUrl: 'http://security.test' });
   const app = express();
-  // The shape proxy.ts mounts eight times: authenticate → attach → require.
+  // The shape proxy.ts mounts seven times: authenticate -> attach -> require.
   app.get('/gated', authenticateToken(true), attachScopes, requireScope('webhooks:manage'), (req, res) => {
```
