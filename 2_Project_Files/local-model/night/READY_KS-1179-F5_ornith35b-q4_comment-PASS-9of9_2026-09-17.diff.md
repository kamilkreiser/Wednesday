# READY — KS-1179 F-5 docblock half (comment_patch: `safeOutboundRequest`'s `timeoutMs` docblock stops saying 'DNS-free connect' — DNS now spends the same budget)
# Source read by Wednesday 22:18: the model's 2 +/- lines IDENTICAL to the brief's (python sequence compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict. Tip = develop 75ad0e55c (R9 builder: merged READYs skipped).
# PR NOTES: `Refs KS-1179 (F-5 docblock)`, never Closes. Raise with the other KS-1179 READYs (F-1, F-2/F-3, F-4) if still unraised. TIER: comment-only -> through-code. Run: runs/2026-09-17_ks1179-ornith35b-night4/out.md.

```diff
--- a/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
+++ b/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
@@ -459,3 +459,3 @@
  *
- * `timeoutMs` is a TOTAL deadline on the whole operation — DNS-free connect,
+ * `timeoutMs` is a TOTAL deadline on the whole operation -- DNS resolution, connect,
  * TLS, request, response and drain — not a socket-idle timer. That distinction
```
