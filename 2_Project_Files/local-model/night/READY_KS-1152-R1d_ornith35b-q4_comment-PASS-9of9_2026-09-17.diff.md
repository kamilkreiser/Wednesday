# READY — KS-1152 R1d (comment_patch: originate ks764 revoke route contract test :126-128 — the `jwt.ts:263` tenantId citation re-pointed at generateAccessToken)
# Source read by Wednesday 22:52: the model's +/- lines IDENTICAL to the brief's (python sequence compare, keyed on this input's own done row; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict. Tip = develop bb848b828. The new sentence verified by Wednesday at develop: generateAccessToken :187 copies tenantId :201; the conditional spread is the connector minter :295.
# PR NOTES: raise R1a+R1b+R1c+R1d as ONE PR — `Refs KS-1152 (R1, 4 of 5 sites)`, never Closes; the 5th site adminConfig.ts:1019 waits for READY_KS-730-B; the ks764 guard comment at :419-420 then describes old text (follow-up, not briefed). TIER: comment-only -> through-code. Run: runs/2026-09-17_ks1152-ornith35b-night4/out.md.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts
@@ -126,3 +126,4 @@
  * refusal this PR introduces on this route (`403 caller has no tenant`). The
- * auth service signs `tenantId` conditionally (jwt.ts:263), so this is a token
+ * auth service signs tenantId conditionally (generateAccessToken in jwt.ts),
+ * so this is a token
  * shape that exists, not a hypothetical.
```
