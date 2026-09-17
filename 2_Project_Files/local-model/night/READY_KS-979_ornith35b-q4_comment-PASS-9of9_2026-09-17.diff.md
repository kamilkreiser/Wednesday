# READY — KS-979 (comment_patch, test file comment only: ks597-issuer-org-bind.test.ts :171 + :174 — cite provenance.ts:109 for its own reason and :136 for the 'different org' phrasing; migration 018 drops NOT NULL on the column outright, the admin endpoint is its reason)
# Source read by Wednesday 20:43: the model's 14 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict — C4 1343 code tokens identical before/after (no code change), C5 inside :171-174, C6/C7 byte-exact. Tip 19f1e5475; develop is now e02515f8f (#1018: services/auth only — this file untouched).
# PR NOTES: `Refs KS-979`, NEVER Closes unless the ticket's whole scope is this sweep (it is — the fix-shape names only these two claims; the raising seat re-reads the ticket). TIER: hygiene/comment-only → the gate tier for docs/comments (through-code only). Run: runs/2026-09-17_ks979-ornith35b-night (first sample, 19 s).

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts
@@ -169,8 +169,12 @@ describe('KS-597 — a mismatched organizationUuid is refused, not folded to NULL', () => {
   });
 
-  // provenance.ts:109: an org-less caller is not in a *different* org, so it is
+  // provenance.ts:109 gives the reason: an org-less caller "has no Organisation
+  // to validate against", so resolving "would attribute to ANY matching tenant
+  // user" (the "not in a *different* org" phrasing belongs to :136, the org-less
+  // SUBJECT, not the org-less caller). So the org-less caller is
   // not refused — but nothing can be bound to it either, so the claim is not
   // attributed. Reachable: migration 018 drops NOT NULL on
-  // svc_api_keys.organization_id for admin-issued keys.
+  // svc_api_keys.organization_id outright; the originate admin endpoint issuing
+  // org-less keys is the migration's stated reason, not a per-key condition.
   it('does NOT 403 an org-less caller, and does NOT attribute its claim either', async () => {
     currentUser = { userId: USER_ID, role: 'ISSUER_ADMIN' };
```
