# READY — KS-1097 PART C of four (`CONTRIBUTING.md` §Review Requirements bullets: QA-957-3 lines 600–601 collapse to one bullet without "— not the reviewer"; QA-957-2 line 604 "The gate is a TESTED PR (see *Adopted merge flow*, step 6) + Wednesday's GO naming the head SHA, with the Test Evidence block filled from local runs")
# Source read by me (Wednesday): the DIFF BELOW IS THE APPLIED (re-anchored, merged) PATCH. The model's r3 output (runs/2026-09-15_ks1097-ornith35b-night10) was right except one double marker on a continuation line (`--  not the reviewer`); the harness strips it (REFLOW double-marker repair) and merges the two hunks that share context (git apply refuses overlapping or asymmetric hunks). Run's own verdict at the time: FAIL D2; Wednesday's re-check under the shipped checker on a scratch clone at M55: PASS 7/7 (D7: 3 must-remove lines gone). after.md read at 599–603; 679 lines (680 − 1); byte-equal to a hand-built expected file except the E2 line, by design.
# PR NOTES: ONE docs PR with A + B (READY) and D (pending); NOT in the PR: CONTRIBUTING:531-532, `.github/workflows/`.

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -597,11 +597,10 @@
 
 - TESTED before merge, as defined in step 6 of *Adopted merge flow* above, and
   Wednesday's GO naming the head SHA (Kam, 2026-09-11)
-- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO —
-  not the reviewer (Kam, 2026-09-11; see *Adopted merge flow* above)
+- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO (Kam, 2026-09-11; see *Adopted merge flow* above)
 - The ticket and the review must not sit with the same person
 - **GitHub Actions is retired** (Kam, 2026-08-27) — there are no CI checks to
-  pass. The gate is approval + a Test Evidence block filled from local runs
+  pass. The gate is a TESTED PR (see *Adopted merge flow*, step 6) + Wednesday's GO naming the head SHA, with the Test Evidence block filled from local runs
 - A filled-in **Test Evidence** block in the PR description, including the four
   platform-suite lines and the unit-suite line — the author's final check
 - No unresolved review comments
```
