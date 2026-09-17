# READY — KS-1152 R1c (comment_patch: packages/shared ks764 revoke call-site guard test :390-393 — the `jwt.ts:263` tenantId citation re-pointed at generateAccessToken)
# Source read by Wednesday 22:52: the model's +/- lines IDENTICAL to the brief's (python sequence compare, keyed on this input's own done row; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict. Tip = develop bb848b828. The new sentence verified by Wednesday at develop: generateAccessToken :187 copies tenantId :201; the conditional spread is the connector minter :295.
# PR NOTES: raise R1a+R1b+R1c+R1d as ONE PR — `Refs KS-1152 (R1, 4 of 5 sites)`, never Closes; the 5th site adminConfig.ts:1019 waits for READY_KS-730-B; the ks764 guard comment at :419-420 then describes old text (follow-up, not briefed). TIER: comment-only -> through-code. Run: runs/2026-09-17_ks1152-ornith35b-night3/out.md.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
@@ -390,4 +390,5 @@
     // The routes worked anyway, because the auth service happens to sign it in
-    // — and `services/auth/src/services/jwt.ts:263` signs it CONDITIONALLY,
-    // `...(meta.tenantId ? { tenantId } : {})`, so a tenant-less user really
+    // -- generateAccessToken (services/auth/src/services/jwt.ts) copies
+    // user.tenantId as it is, and JSON serialisation drops an undefined value,
+    // so a tenant-less user really
     // does receive a token without the claim.
```
