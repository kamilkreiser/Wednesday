# READY - KS-2146-KS-2146-O116-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2146_o116_p1_ks1536_header_says_g5_g5b_read_source_text/out.md.checker/patch.diff` (from `ls` at 17:47 2026-11-09; sha256[:16] 837c07f3b9bbe551, 1184 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 17:47 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2146_o116_p1_ks1536_header_says_g5_g5b_read_source_text/out.md.checker`; the expectations were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts']; `+` lines 3 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (4 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `It proves wiring, not behaviour: the` in `Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `It proves wiring in the source text, not behaviour: the` in `Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `not that the live routes are gated` in `Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts
@@ -13,8 +13,10 @@
  * admin, and platform or ORG_ADMIN. A new name, not a second list of platform roles.
  *
  * THE GUARD has the KS-764 call-site guard's shape: a source sweep over services, packages and frontends, with its own
- * planted-tree control, because a guard that cannot see a defect passes on anything. It proves wiring, not behaviour: the
+ * planted-tree control, because a guard that cannot see a defect passes on anything. It proves wiring in the source text, not behaviour: the
  * gateway's behaviour is services/api-gateway ks1536-gateway-role-checks-are-the-shared-predicates.test.ts.
+ * Cells G5 and G5b read the tokenisation source as text: they show that the two gated route lines exist, not that the live routes are gated
+ * (an earlier ungated registration of the same path leaves both green; KS-2146).
  */
 import { beforeAll, describe, it, expect } from 'vitest';
 import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
```
