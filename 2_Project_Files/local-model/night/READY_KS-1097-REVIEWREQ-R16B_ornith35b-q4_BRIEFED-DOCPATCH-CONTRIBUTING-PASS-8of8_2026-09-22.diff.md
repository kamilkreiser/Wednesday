# READY — KS-1097-REVIEWREQ-R16B (Ornith, briefed, doc_patch, markdown) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 11:24 2026-09-22; sha256[:16] 58b583ae7bd59f2f, 1110 B — a BYTE count; byte-equal to the out.md fence (the model's as-written block)). Checker D2 (verbatim from checker.out): `PASS D2 diff applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/REVIEWREQ/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0.

**Held 11:24 2026-09-22 by Wednesday after a source read (hold_ready.py, doc_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `doc_1097REVIEWREQ-R16B.json`).
- Subject [checker.out D0, verbatim]: `PASS D0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/CONTRIBUTING.md present`
- Output shape [checker.out D1, verbatim]: `PASS D1 output is exactly one fenced ```diff block`
- Touched-file set [checker.out D3, verbatim]: `PASS D3 touched-file set == { Blockchain/Dev/CONTRIBUTING.md }` — `patch.diff`'s own `+++` header names exactly `Blockchain/Dev/CONTRIBUTING.md`; 2 hunk(s), `+` lines 2 (ASCII), `-` lines 3 (counted from patch.diff); before.md → after.md: 3 line(s) removed, 2 added (difflib on the checker's own files).
- Tip content [out.md.checker/before.md]: byte-equal to input.json['files'][product_file]; after.md is byte-equal to patch.diff re-applied to before.md (`git apply -p1 (strict)`, scratch tempdir, sha256 3062451d0224713a).
- Sections [checker.out D4/D5, verbatim, one pair per required section]:
  - `PASS D4 BEFORE: '## Related Issues' lacks ["Wednesday's GO (Kam", 'a TESTED PR (see'] at the tip (control: section found, 22 lines)`
  - `PASS D5 AFTER: '## Related Issues' carries ["Wednesday's GO (Kam", 'a TESTED PR (see']`
- section `## Related Issues` tokens ["Wednesday's GO (Kam", 'a TESTED PR (see'] — before.md: found at line 601, 22 lines, every token ABSENT; after.md: found at line 601, 21 lines, every token PRESENT (re-measured with the checker's section rule)
- D6 [verbatim]: `PASS D6 every changed region lies inside the required sections (1 section(s), measured on before/after)`
- D7 [verbatim]: `PASS D7 every must-remove line (3) present before and absent after (control: all found at the tip)` — re-measured: every one of the 3 must_remove line(s) in before.md and absent from after.md
- D8 [verbatim]: `PASS D8 every brief '+' line (2) is in the file AFTER, exactly` — re-measured: every one of the 2 brief '+' line(s) in after.md exactly (rstrip)
- D9 [verbatim]: `INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (8/8)` (total 8 = the checker's formula for must_remove=3, expected_plus=2, insert_after=None)

**PR NOTES for the raise seat:** DOC_PATCH — DOCUMENTATION ONLY, zero code bytes: `Blockchain/Dev/CONTRIBUTING.md` (+2/-3 per patch.diff); one file. Apply `patch.diff` strictly (`git apply -p1`) at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Tier: tier 1 (documentation) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/input.json`. Brief (located by ticket + ROWID tokens ['REVIEWREQ', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1097-R16B-REVIEWREQ.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -608,5 +608,4 @@
 - TESTED before merge, as defined in step 6 of *Adopted merge flow* above, and
   Wednesday's GO naming the head SHA (Kam, 2026-09-11)
-- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO —
-  not the reviewer (Kam, 2026-09-11; see *Adopted merge flow* above)
+- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO (Kam, 2026-09-11; see *Adopted merge flow* above)
 - The ticket and the review must not sit with the same person
@@ -613,5 +612,5 @@
 - **GitHub Actions is retired** (Kam, 2026-08-27) — there are no CI checks to
-  pass. The gate is approval + a Test Evidence block filled from local runs
+  pass. The gate is a TESTED PR (see *Adopted merge flow*, step 6) + Wednesday's GO naming the head SHA, with the Test Evidence block filled from local runs
 - A filled-in **Test Evidence** block in the PR description, including the four
   platform-suite lines and the unit-suite line — the author's final check
 - No unresolved review comments
```
