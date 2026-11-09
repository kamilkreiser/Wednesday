# READY - KS-2089-KS-2089-O117-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2089_o117_p1_check_shared_relink_line_522_comment_names_a_refusal_that_is_gone/out.md.checker/patch.diff` (from `ls` at 17:59 2026-11-09; sha256[:16] b406b0ec5a246d39, 727 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 17:59 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2089_o117_p1_check_shared_relink_line_522_comment_names_a_refusal_that_is_gone/out.md.checker`; the expectations were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/scripts/check-shared-relink.sh']; `+` lines 1 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/check-shared-relink.sh)`
  - `PASS A4 RED AT BASE: all 2 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (2 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 2 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `refusal below. Bounded assumption, stated: the` in `Blockchain/Dev/scripts/check-shared-relink.sh` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `not found in NON_JS_BASES (see image_name_component above). Bounded assumption` in `Blockchain/Dev/scripts/check-shared-relink.sh` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/scripts/check-shared-relink.sh
+++ b/Blockchain/Dev/scripts/check-shared-relink.sh
@@ -519,7 +519,7 @@
       #
       # The strip is gated on the variable NAME (REGISTRY/REPO/MIRROR/PREFIX) so
       # that `$NODE_IMAGE`, where the variable IS the reference, is NOT stripped
-      # and falls to the `$` refusal below. Bounded assumption, stated: the
+      # and is refused later, when its name is not found in NON_JS_BASES (see image_name_component above). Bounded assumption, stated: the
       # prefix carries its own trailing separator or is empty, which is how this
       # repo uses it. A variable forming part of the NAME itself would defeat
       # this read; that shape does not occur here.
```
