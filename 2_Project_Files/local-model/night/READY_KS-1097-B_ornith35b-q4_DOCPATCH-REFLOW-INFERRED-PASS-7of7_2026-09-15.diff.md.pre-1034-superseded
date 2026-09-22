# READY — KS-1097 PART B of four (`CONTRIBUTING.md` §Pull Request Process: QA-957-5 line 458 gains "— superseded 2026-09-11 (KS-1092): the approval is Wednesday's GO on a TESTED PR."; QA-957-3 line 466 drops "— not the reviewer"; QA-957-3 line 550 "reads to the QA gate as a run")
# Source read by me (Wednesday): the DIFF BELOW IS THE APPLIED (re-anchored) PATCH, not the model's raw output. The model's r3 output (runs/2026-09-15_ks1097-ornith35b-night8) wrote hunk 1 as the whole paragraph joined on one CONTEXT line carrying the tail — three rounds of that one shape; the harness now splits it back (REFLOW) and, because the brief's must_remove names line 458, applies the tail to that line as -/+ (REFLOW INFERRED, D7/D5 judge it). Run's own verdict at the time: FAIL D2; Wednesday's re-check under the shipped checker on a scratch clone at M55: PASS 7/7 (D7: 3 must-remove lines present before, absent after). after.md verified at 458/466/550; 680 lines before and after.
# PR NOTES: ONE docs PR with A (READY), C and D (pending); NOT in the PR: CONTRIBUTING:531-532 (Kam's red-pen line), `.github/workflows/`.

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -455,7 +455,7 @@
 (v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56)). This section stays the contributor-facing copy,
 and the two agree on the adopted flow. **One item in that document differs and is
 flagged there as a proposal, not yet team-agreed** — *approval may come from any
-of the three who is not the author*.
+of the three who is not the author* — superseded 2026-09-11 (KS-1092): the approval is Wednesday's GO on a TESTED PR.
 
 1. Develop on a branch.
 2. **Test your own work before the PR goes up**, and put the results in the PR
@@ -463,7 +463,7 @@
 3. Commit → push → open the PR.
 4. Peter runs periodic formal test passes; demo (UAT) is updated after his nod.
 5. Findings from the QA gate are discussed with the PR issuer.
-6. **The author merges once the PR is TESTED — not the reviewer.** TESTED = a QA
+6. **The author merges once the PR is TESTED.** TESTED = a QA
    gate verdict (GO or GO WITH FINDINGS) at the PR's current head + a Test Evidence
    block + our own suites, and **Wednesday's GO, naming the head SHA, is the approval** (Kam, 2026-09-11):
    16:56:00 *"For the time being, I / you will approve our own elements"* ·
@@ -547,7 +547,7 @@
 A line must say what happened, not what applies. "Run and passing" means a run
 whose result you read. If a suite has no bearing on the change, write
 `not run — no spec change, no new route or method`; do not tick it as done.
-A box ticked on a not-applicable rationale reads to the reviewer as a run.
+A box ticked on a not-applicable rationale reads to the QA gate as a run.
 
 ### PR Description Template
 
```
