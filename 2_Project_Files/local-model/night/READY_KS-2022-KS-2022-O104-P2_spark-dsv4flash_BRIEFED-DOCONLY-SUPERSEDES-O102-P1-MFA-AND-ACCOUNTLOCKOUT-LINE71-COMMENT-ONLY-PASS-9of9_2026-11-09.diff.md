# READY - KS-2022-KS-2022-O104-P2 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2022_o104_p2_mfa_lockout_citations/out.md.checker/patch.diff` (from `ls` at 00:17 2026-11-09; sha256[:16] 7f62133f721003cd, 1221 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 00:17 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2022_o104_p2_mfa_lockout_citations/out.md.checker`; the expectations were RE-MEASURED here.** Tip `7eda23b34d3b7a413ca8f9c0945c7843708ce9f4`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/auth/src/routes/mfa.ts', 'Blockchain/Dev/services/auth/src/services/accountLockout.ts']; `+` lines 2 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/auth/src/routes/mfa.ts, Blockchain/Dev/services/auth/src/services/accountLockout.ts)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (4 comment line(s) changed in 2 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `passwordLoginGate.ts:87` in `Blockchain/Dev/services/auth/src/routes/mfa.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `passwordLoginGate.ts:119` in `Blockchain/Dev/services/auth/src/services/accountLockout.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `MFA_CODE_PATTERN (passwordLoginGate.ts), not a second opinion` in `Blockchain/Dev/services/auth/src/routes/mfa.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `(by the gate's own normalisation)` in `Blockchain/Dev/services/auth/src/services/accountLockout.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/auth/src/routes/mfa.ts
+++ b/Blockchain/Dev/services/auth/src/routes/mfa.ts
@@ -127,7 +127,7 @@
   // change an existing field's accepted values; adding a field cannot make any
   // request that is valid today start failing.
   // The pattern is the 8-char alternative of the platform's own
-  // MFA_CODE_PATTERN (passwordLoginGate.ts:87), not a second opinion about what
+  // MFA_CODE_PATTERN (passwordLoginGate.ts), not a second opinion about what
   // a backup code looks like.
   backupCode: z.string().regex(/^[A-Za-z0-9]{8}$/).optional(),
 });
--- a/Blockchain/Dev/services/auth/src/services/accountLockout.ts
+++ b/Blockchain/Dev/services/auth/src/services/accountLockout.ts
@@ -68,7 +68,7 @@
  * (KS-795 / KS-796) add callers. Trimming in the derivation makes it structural.
  * Idempotent for both current callers, which already pass a trimmed address:
  * `routes/auth.ts:310` (via `loginSchema`'s `z.string().trim()`) and
- * `services/passwordLoginGate.ts:119` (via the gate's own normalisation).
+ * `services/passwordLoginGate.ts` (by the gate's own normalisation).
  */
 function normaliseEmailForKey(email: string): string {
   return String(email).toLowerCase().trim();
```
