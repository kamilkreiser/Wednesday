# READY - KS-902-O101-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-04_ks_902_o101_p1_no_tracked_credentials_comment_idiom/out.md.checker/patch.diff` (from `ls` at 02:14 2026-11-04; sha256[:16] 878aff7808fb8840, 883 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:14 2026-11-04 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-04_ks_902_o101_p1_no_tracked_credentials_comment_idiom/out.md.checker`; the expectations were RE-MEASURED here.** Tip `79145a312f0150ca9adaf5a36bb3dea93d108cff`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_902_o101_p1_no_tracked_credentials_comment_idiom/KS-902.md`
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh']; `+` lines 4 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (6 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `structurally immune` in `Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `that form is cwd-relative (KS-902)` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `not from the caller's` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh
+++ b/Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh
@@ -78,8 +78,10 @@
 # `git ls-files` output is index paths), which is why the output looked
 # identical until something was planted.
 #
-# `bare-path-scripts-executable.sh` and `action-pins-labelled.sh` already derive
-# their root this way and are structurally immune; this is the same idiom.
+# The root is derived from this script's own location, not from the caller's
+# working directory, so it does not depend on where the preflight runs. Do not
+# copy `REPO_ROOT="$(cd ../.. && pwd)"` from `bare-path-scripts-executable.sh`
+# or `action-pins-labelled.sh`: that form is cwd-relative (KS-902).
 DEV_DIR="$(cd "$(dirname "$0")/../.." && pwd)"   # Blockchain/Dev
 
 # Scrub the inherited git environment FIRST. Git exports GIT_DIR to a WORKTREE's
```
