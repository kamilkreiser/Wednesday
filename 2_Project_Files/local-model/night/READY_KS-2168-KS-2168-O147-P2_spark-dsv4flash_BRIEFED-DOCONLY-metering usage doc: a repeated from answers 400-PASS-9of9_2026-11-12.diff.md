# READY - KS-2168-KS-2168-O147-P2 (spark-dsv4flash, briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2168_o147_p2_metering_usage_doc_repeated_from_answers_400-r2/out.md.checker/patch.diff` (from `ls` at 01:56 2026-11-12; sha256[:16] 3e68f77d6f7ee69b, 1350 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 01:56 2026-11-12 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2168_o147_p2_metering_usage_doc_repeated_from_answers_400-r2/out.md.checker`; the expectations were RE-MEASURED here.** Tip `4f85ca04c622f29099d184bc45de2faa61fb4af0`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2168_o147_p2_metering_usage_doc_repeated_from_answers_400/KS-2168.md`
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/docs/METERING-USAGE-API.md']; `+` lines 1 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/docs/METERING-USAGE-API.md)`
  - `PASS A4 RED AT BASE: all 2 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 2 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `is ignored and the call answers **200** with that bound open (KS-1875)` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `is refused: the call answers **400** `BAD_REQUEST` with "from and to may each be given once" (KS-1875 piece 2, PR 2167).` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/docs/METERING-USAGE-API.md
+++ b/Blockchain/Dev/docs/METERING-USAGE-API.md
@@ -23,7 +23,7 @@
 
 - `from`, `to` — **optional**, inclusive bounds on the event timestamp (`created_at`).
   ISO-8601 date (`2026-06-01`) or full timestamp (`2026-06-01T00:00:00Z`). Omit either
-  for an open bound. A string that does not match the date shape returns **400**. A value that fits the shape but is not a real date (`2026-02-30`, `2026-13-01`) passes that check and reaches the database cast, which fails, so the call answers **500** (known deviation, KS-1875: the check is a regular expression, not a date parse). A value that is not a single string, for example a repeated `from` parameter, is ignored and the call answers **200** with that bound open (KS-1875).
+  for an open bound. A string that does not match the date shape returns **400**. A value that fits the shape but is not a real date (`2026-02-30`, `2026-13-01`) passes that check and reaches the database cast, which fails, so the call answers **500** (known deviation, KS-1875: the check is a regular expression, not a date parse). A value that is not a single string, for example a repeated `from` parameter, is refused: the call answers **400** `BAD_REQUEST` with "from and to may each be given once" (KS-1875 piece 2, PR 2167).
 
 ## Authentication (tenant-scoped)
```

> NOTE (operator o145, 2026-11-12): round 1 failed on a brief defect (a third expectation that already held); this is round 2 of 2
