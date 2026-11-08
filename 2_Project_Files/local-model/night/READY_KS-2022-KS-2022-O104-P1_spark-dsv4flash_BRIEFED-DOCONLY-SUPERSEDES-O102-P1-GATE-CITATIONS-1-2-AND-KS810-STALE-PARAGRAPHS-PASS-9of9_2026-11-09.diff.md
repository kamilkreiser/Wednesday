# READY - KS-2022-KS-2022-O104-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2022_o104_p1_stale_paragraphs_supersedes_o102_p1/out.md.checker/patch.diff` (from `ls` at 00:17 2026-11-09; sha256[:16] d0772439d0f28449, 4531 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 00:17 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2022_o104_p1_stale_paragraphs_supersedes_o102_p1/out.md.checker`; the expectations were RE-MEASURED here.** Tip `7eda23b34d3b7a413ca8f9c0945c7843708ce9f4`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/auth/src/auth.openapi.ts', 'Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts']; `+` lines 19 (1 NON-ASCII chars), `-` lines 28.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts, Blockchain/Dev/services/auth/src/auth.openapi.ts)`
  - `PASS A4 RED AT BASE: all 5 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (45 comment line(s) changed in 2 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 5 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 5/5 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `passwordLoginGate.ts:55` in `Blockchain/Dev/services/auth/src/auth.openapi.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `NOTHING IMPORTS THEM YET` in `Blockchain/Dev/services/auth/src/auth.openapi.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `passwordLoginGate.ts:55` in `Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `turns the auth suite red (KS-810)` in `Blockchain/Dev/services/auth/src/auth.openapi.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `KS-810 fixed that` in `Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/auth/src/auth.openapi.ts
+++ b/Blockchain/Dev/services/auth/src/auth.openapi.ts
@@ -2,23 +2,19 @@
 // OAuthAuthorizeRequestSchema are EXPORTED so the published wire contract can be
 // asserted rather than described.
 //
-// ⚠ NOTHING IMPORTS THEM YET, and the reason is a defect, not an oversight. This
-// module CANNOT be imported from a test today:
+// The module is loaded by `src/__tests__/s130-f6-openapi-module-in-the-import-graph.test.ts`,
+// so a module-scope throw in this file turns the auth suite red (KS-810).
 //
-//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function   (:152)
+// It was once un-importable from a test:
 //
-// `packages/shared/src/openapi/registry.ts:245` states the rule — a consumer MUST
-// import `z` from '@secuura/shared' so `extendZodWithOpenApi` lands on the same
-// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
-// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
-// generator's single CJS resolution happens to unify the two; a vitest run does
-// not. Filed separately; the fix is one import line with a blast radius across
-// every schema that file publishes, so it is not being slipped into a follow-up.
+//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function
 //
-// Until then the QA2-F4 guard asserts the GENERATED yaml instead — which is the
-// artefact a client generates from, so it is the thing that would ship wrong.
-// This also means the gate's canary still stands: a module-scope throw in this
-// file leaves the auth suite green, because it is in no test's import graph.
+// because `services/passwordLoginGate.ts` imported `z` from 'zod' directly. The
+// shared registry requires a consumer to import `z` from '@secuura/shared' so
+// `extendZodWithOpenApi` lands on the same prototype; the gate file now does.
+//
+// The QA2-F4 guard still asserts the GENERATED yaml, which is the artefact a
+// client generates from, so it is the thing that would ship wrong.
 /**
  * =============================================================================
  * AUTH SERVICE — OpenAPI registrations (Track 2 stage 3)
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts
--- a/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts
@@ -106,22 +106,17 @@
 // ---------------------------------------------------------------------------
 // KS-796 QA2-F4 — the same agreement, asserted at the PUBLISHED contract.
 //
-// ⚠ WHY THIS READS THE GENERATED YAML AND NOT THE SCHEMA OBJECTS. The obvious
-// version imports `LoginRequestSchema` etc. from `auth.openapi.ts` and compares
-// them to the runtime schema. It cannot load:
+// ⚠ WHY THIS READS THE GENERATED YAML AND NOT THE SCHEMA OBJECTS. The yaml is the
+// artefact a client generates from. This guard was written when `auth.openapi.ts`
+// could not be loaded from a test:
 //
 //   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function
-//     at src/auth.openapi.ts:152
-//
-// `packages/shared/src/openapi/registry.ts:245` states the rule — consumers MUST
-// import `z` from '@secuura/shared', so `extendZodWithOpenApi` lands on the same
-// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
-// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
-// generator's single CJS resolution happens to unify them; a vitest run does not.
-// That is a one-line change with a blast radius well past this PR, so it is FILED
-// rather than slipped in here — and it is the real reason `auth.openapi.ts` sits
-// in no test's import graph (the gate's canary: a module-scope throw there left
-// the suite 441/441 green).
+//
+// because `services/passwordLoginGate.ts` imported `z` from 'zod'; the shared
+// registry requires `z` from '@secuura/shared' so `extendZodWithOpenApi` lands on
+// the same prototype. KS-810 fixed that: the gate file now imports `z` from
+// '@secuura/shared', and `s130-f6-openapi-module-in-the-import-graph.test.ts`
+// imports `auth.openapi.ts`, so a module-scope throw there now turns the suite red.
 //
 // Reading the generated yaml is not a consolation prize: it is the artefact a
 // client actually generates from, and it is what would ship wrong.
```
