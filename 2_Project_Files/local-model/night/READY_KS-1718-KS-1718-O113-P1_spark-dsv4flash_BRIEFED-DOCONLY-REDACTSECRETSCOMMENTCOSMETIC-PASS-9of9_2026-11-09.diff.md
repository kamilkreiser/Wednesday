# READY - KS-1718-KS-1718-O113-P1 (spark-dsv4flash, briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1718_o113_p1_redact_secrets_comment_says_cosmetic/out.md.checker/patch.diff` (from `ls` at 10:25 2026-11-09; sha256[:16] 052a9bdc7019d1b8, 1184 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: BYTE-IDENTICAL.

**Held 10:25 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1718_o113_p1_redact_secrets_comment_says_cosmetic/out.md.checker`; the expectations were RE-MEASURED here.** Tip `4e529633d0a19a3efe626adfe05684fbd964e595`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['systemTest/fixtures/provision.ts']; `+` lines 7 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (systemTest/fixtures/provision.ts)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (8 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `regex metacharacters.` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `regex metacharacters, so they are matched only as exact substrings.` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `COSMETIC, NOT SECRECY (KS-1718)` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/systemTest/fixtures/provision.ts
+++ b/systemTest/fixtures/provision.ts
@@ -259,7 +259,13 @@
  * Where/when: applied to a server's error message before it is interpolated into a thrown Error
  * (KS-973 item 6), because that Error's message becomes the pre-suite DEGRADED banner every suite
  * prints. A plain split/join, not a regex: the secrets are generated passwords and may carry
- * regex metacharacters.
+ * regex metacharacters, so they are matched only as exact substrings.
+ *
+ * COSMETIC, NOT SECRECY (KS-1718): this scrub hides the literal password from the banner, but it does not keep the
+ * password private. `buildPassword` in actors.ts makes it `Ks256-<key>-<seed>-Pw!`, and the Error built from this
+ * reason names the actor's key and email (`ks256-<key>-<seed>@secuura-test.invalid`), so a reader of the banner can
+ * rebuild the password. A server echo that JSON-, URL- or HTML-escapes the password is not matched either. These are
+ * test accounts on undeliverable addresses.
  *
  * @param text - the message to scrub, e.g. a server's `error.message`.
  * @param secrets - the values that must not appear; an empty string is ignored, since it would
```
