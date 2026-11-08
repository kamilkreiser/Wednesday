# READY - KS-2022-KS-2022-O102-P1 (spark-dsv4flash, briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2022_o102_p1_stale_gate_citation_two_comments/out.md.checker/patch.diff` (from `ls` at 22:58 2026-11-08; sha256[:16] 432ab7972f85a2ce, 1897 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 22:58 2026-11-08 by Spark operator 102 (Wednesday) after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2022_o102_p1_stale_gate_citation_two_comments/out.md.checker`; the expectations were RE-MEASURED here.** Tip `abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2022_o102_p1_stale_gate_citation_two_comments/KS-2022.md`
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/auth/src/auth.openapi.ts', 'Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts']; `+` lines 6 (2 NON-ASCII chars), `-` lines 4.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts, Blockchain/Dev/services/auth/src/auth.openapi.ts)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (10 comment line(s) changed in 2 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `passwordLoginGate.ts:55` in `Blockchain/Dev/services/auth/src/auth.openapi.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `passwordLoginGate.ts:55` in `Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `it now imports it from '@secuura/shared'` in `Blockchain/Dev/services/auth/src/auth.openapi.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `it now imports it from '@secuura/shared'` in `Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/auth/src/auth.openapi.ts
+++ b/Blockchain/Dev/services/auth/src/auth.openapi.ts
@@ -9,8 +9,9 @@
 //
 // `packages/shared/src/openapi/registry.ts:245` states the rule — a consumer MUST
 // import `z` from '@secuura/shared' so `extendZodWithOpenApi` lands on the same
-// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
-// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
+// prototype — and `services/passwordLoginGate.ts` imported `z` from 'zod'
+// directly (KS-810; it now imports it from '@secuura/shared'), so
+// `MFA_CODE_ACCEPTED` was built on an UNEXTENDED zod. The spec
 // generator's single CJS resolution happens to unify the two; a vitest run does
 // not. Filed separately; the fix is one import line with a blast radius across
 // every schema that file publishes, so it is not being slipped into a follow-up.
--- a/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts
@@ -115,8 +115,9 @@
 //
 // `packages/shared/src/openapi/registry.ts:245` states the rule — consumers MUST
 // import `z` from '@secuura/shared', so `extendZodWithOpenApi` lands on the same
-// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
-// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
+// prototype — and `services/passwordLoginGate.ts` imported `z` from 'zod'
+// directly (KS-810; it now imports it from '@secuura/shared'), so
+// `MFA_CODE_ACCEPTED` was built on an UNEXTENDED zod. The spec
 // generator's single CJS resolution happens to unify them; a vitest run does not.
 // That is a one-line change with a blast radius well past this PR, so it is FILED
 // rather than slipped in here — and it is the real reason `auth.openapi.ts` sits
```
