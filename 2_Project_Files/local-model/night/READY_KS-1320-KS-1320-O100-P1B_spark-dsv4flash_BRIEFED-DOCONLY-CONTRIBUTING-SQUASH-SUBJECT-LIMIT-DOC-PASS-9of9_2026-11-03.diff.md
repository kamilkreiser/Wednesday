# READY - KS-1320-KS-1320-O100-P1B (spark-dsv4flash, briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1320_o100_p1b_contributing_squash_subject_limit/out.md.checker/patch.diff` (from `ls` at 22:43 2026-11-03; sha256[:16] a78813334cf25ef8, 1166 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 22:43 2026-11-03 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1320_o100_p1b_contributing_squash_subject_limit/out.md.checker`; the expectations were RE-MEASURED here.** Tip `1cbf260548e7fd534603725f9fc6b05c5cdd9907`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1320_o100_p1b_contributing_squash_subject_limit/KS-1320.md`
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/CONTRIBUTING.md']; `+` lines 3 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/CONTRIBUTING.md)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `stay squash.` in `Blockchain/Dev/CONTRIBUTING.md` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `the squash` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `subject must be 92 characters or fewer and ASCII only` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -104,7 +104,9 @@
   `.github/**` file) gets twin-green without the real suite — same-name/latest-report semantics only
   self-correct where the real workflow exists. Hotfix review must eyeball the diff for this shape.
 - **Merge method:** `hotfix/*` and `release/*` PRs use **merge commits** (not squash) — the
-  fold-back/tombstone mechanics below depend on shared history. Feature PRs into `develop` stay squash.
+  fold-back/tombstone mechanics below depend on shared history. Feature PRs into `develop` stay squash, and the squash
+  subject must be 92 characters or fewer and ASCII only, so keep the PR title within that limit (KS-1320: nothing
+  rejects a longer title when the PR is opened; the merge gate finds it, and a replacement subject then has to be written).
 - **No force push (KS-1037):** `.githooks/pre-push` REFUSES any non-fast-forward push to a branch that
   already exists at origin — a rebase becomes a NEW branch. Why: a force push rewrites history another
   process may depend on — an open PR's head, or a gate running against the SHA being replaced.
```
