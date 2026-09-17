# READY — KS-1179-F4 (comment_patch, comment lines only: ssrf-guard.ts :421-425 + :519-523 — 'blocked' also covers a host that does not resolve, or not within timeoutMs)
# Source read by Wednesday 21:10: the model's 14 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical; C5 inside the named lines; C6/C7 byte-exact). Tip = develop 75ad0e55c.
# PR NOTES: `Refs KS-1179 (F-4)`, never Closes (F-5's docblock half was refused by builder R9 on a merged READY — still open). PASSED ON RETRY-ONCE (first sample FAIL C2: diff did not apply strict); the retry is what is held. TIER: comment-only → through-code. Run: runs/2026-09-17_ks1179-ornith35b-night3/retry/out.md.

```diff
--- a/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
+++ b/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
@@ -421,5 +421,7 @@
  *  - `blocked`        — WE refused to send. The URL failed the literal check,
  *                       or its host resolved to an address the classifier
- *                       forbids. Nothing left this process.
+ *                       forbids, or its host did not resolve at all, or not
+ *                       within `timeoutMs` (a slow resolver lands here too).
+ *                       Nothing left this process.
  *  - `request_failed` — we sent, and the destination did not answer usefully:
  *                       connection refused, TLS failure, or the deadline below.
@@ -519,4 +521,5 @@
      * WHY `request_failed` AND NOT `blocked`: `blocked` means THIS GUARD refused
-     * for an SSRF reason, and an operator reads it as "we decided not to send".
+     * for an SSRF reason (or because the host did not resolve, or not within
+     * `timeoutMs`), and an operator reads it as "we decided not to send".
      * An unencodable header is not that decision — nothing about the destination
      * was refused. Mislabelling it would corrupt the one signal the discriminator
```
