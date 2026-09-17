# READY — KS-1152 R1a (comment_patch: packages/shared middleware/index.ts :32-35 — the `jwt.ts:263` tenantId citation re-pointed at generateAccessToken)
# Source read by Wednesday 22:52: the model's +/- lines IDENTICAL to the brief's (python sequence compare, keyed on this input's own done row; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict. Tip = develop bb848b828. The new sentence verified by Wednesday at develop: generateAccessToken :187 copies tenantId :201; the conditional spread is the connector minter :295.
# PR NOTES: raise R1a+R1b+R1c+R1d as ONE PR — `Refs KS-1152 (R1, 4 of 5 sites)`, never Closes; the 5th site adminConfig.ts:1019 waits for READY_KS-730-B; the ks764 guard comment at :419-420 then describes old text (follow-up, not briefed). TIER: comment-only -> through-code. Run: runs/2026-09-17_ks1152-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/packages/shared/src/middleware/index.ts
+++ b/Blockchain/Dev/packages/shared/src/middleware/index.ts
@@ -32,4 +32,5 @@
    * type declared the field: the revoke routes worked only because the auth
-   * service HAPPENS to sign it in, and `services/auth/src/services/jwt.ts:263`
-   * signs it CONDITIONALLY — `...(meta.tenantId ? { tenantId } : {})` — so a
+   * service HAPPENS to sign it in: generateAccessToken
+   * (services/auth/src/services/jwt.ts) copies user.tenantId as it is, and
+   * JSON serialisation drops an undefined value, so a
    * tenant-less user genuinely receives a token without the claim.
```
