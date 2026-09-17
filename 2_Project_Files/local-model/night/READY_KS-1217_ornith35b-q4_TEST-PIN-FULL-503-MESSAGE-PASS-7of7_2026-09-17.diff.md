# READY — KS-1217 (test-only, auth ks1050 test :146 — pin the WHOLE 503 helper message, the dash built by code point, so an appended not-applied claim reds)
# Source read by Wednesday 22:13: the model's 3 +/- lines IDENTICAL to the brief's fence (python sequence compare; a mutated copy unequal); checker RESULT PASS (7/7) first sample, apply_mode=LENIENT (the model's hunk-header dialect: `@@ -143,9 +143,10 @@` vs the brief's `-143,7 +143,8`); A4 red by assertion under the :973 tamper; A5 4/4; A6 auth 762 -> 762 no new red; A7 tsc rc 0. Tip = develop 75ad0e55c.
# PR NOTES: `Closes KS-1217` is defensible once merged (the ticket's recommendation is exactly this edit; confirm at raise); KS-1050 stays In Progress (§5f). TIER 2 (coverage pin, in-process). Re-derive the hunk header at raise with `git diff` after applying (lenient apply). Develop has moved to 0a2b1603f since the brief: re-apply strict at raise. Run: runs/2026-09-17_ks1217-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts
@@ -143,9 +143,10 @@ describe('KS-1050 r2 — PATCH /me over a 0-row UPDATE refuses through updateUserO
     expect(res.status).toBe(503);
     expect(res.body.success).toBe(false);
     expect(res.body.error.code).toBe('SERVICE_UNAVAILABLE');
-    expect(res.body.error.message).toMatch(/^Profile update could not be confirmed\. Please retry/);
+    // KS-1217: the WHOLE message, so an appended not-applied claim in any words reds (the dash is U+2014, built by code point).
+    expect(res.body.error.message).toBe('Profile update could not be confirmed. Please retry ' + String.fromCharCode(0x2014) + ' if you already succeeded, you may not need to.');
     // The helper's docblock forbids asserting the change did not land: null has two causes.
     expect(res.text).not.toMatch(/not applied|matched no row|did not persist/i);
     // The null came from the 0-row arm: one UPDATE issued, and no read-back after it.
     expect(updates()).toHaveLength(1);
     expect(readBacksAfterUpdate()).toHaveLength(0);
   });
```
