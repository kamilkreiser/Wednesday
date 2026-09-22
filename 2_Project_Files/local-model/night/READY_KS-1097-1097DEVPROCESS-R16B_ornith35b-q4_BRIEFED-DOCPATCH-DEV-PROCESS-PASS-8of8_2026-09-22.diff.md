# READY — KS-1097-1097DEVPROCESS-R16B (Ornith, briefed, doc_patch, markdown) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` at 13:34 2026-09-22; sha256[:16] 4f36b0df0226ec09, 1918 B — a BYTE count; byte-equal to the out.md fence (the model's as-written block)). Checker D2 (verbatim from checker.out): `PASS D2 diff applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night4/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed11-drafter-precheck/DEVPROCESS/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0.

**Held 13:34 2026-09-22 by Wednesday after a source read (hold_ready.py, doc_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night4/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `doc_1097DEVPROCESS-R16B.json`).
- Subject [checker.out D0, verbatim]: `PASS D0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/docs/DEV-PROCESS.md present`
- Output shape [checker.out D1, verbatim]: `PASS D1 output is exactly one fenced ```diff block`
- Touched-file set [checker.out D3, verbatim]: `PASS D3 touched-file set == { Blockchain/Dev/docs/DEV-PROCESS.md }` — `patch.diff`'s own `+++` header names exactly `Blockchain/Dev/docs/DEV-PROCESS.md`; 2 hunk(s), `+` lines 2 (ASCII), `-` lines 2 (counted from patch.diff); before.md → after.md: 2 line(s) removed, 2 added (difflib on the checker's own files).
- Tip content [out.md.checker/before.md]: byte-equal to input.json['files'][product_file]; after.md is byte-equal to patch.diff re-applied to before.md (`git apply -p1 (strict)`, scratch tempdir, sha256 9e58247a19a941dd).
- Sections [checker.out D4/D5, verbatim, one pair per required section]:
  - `PASS D4 BEFORE: '## Why it's shaped this way' lacks ['a second seat signs it off', 'never the seat that built it'] at the tip (control: section found, 7 lines)`
  - `PASS D5 AFTER: '## Why it's shaped this way' carries ['a second seat signs it off', 'never the seat that built it']`
  - `PASS D4 BEFORE: '## Branch protection on ' lacks ['step 6 of Adopted merge flow', 'TESTED (as defined in'] at the tip (control: section found, 24 lines)`
  - `PASS D5 AFTER: '## Branch protection on ' carries ['step 6 of Adopted merge flow', 'TESTED (as defined in']`
- section `## Why it's shaped this way` tokens ['a second seat signs it off', 'never the seat that built it'] — before.md: found at line 62, 7 lines, every token ABSENT; after.md: found at line 62, 7 lines, every token PRESENT (re-measured with the checker's section rule)
- section `## Branch protection on ` tokens ['step 6 of Adopted merge flow', 'TESTED (as defined in'] — before.md: found at line 256, 24 lines, every token ABSENT; after.md: found at line 256, 24 lines, every token PRESENT (re-measured with the checker's section rule)
- D6 [verbatim]: `PASS D6 every changed region lies inside the required sections (2 section(s), measured on before/after)`
- D7 [verbatim]: `PASS D7 every must-remove line (2) present before and absent after (control: all found at the tip)` — re-measured: every one of the 2 must_remove line(s) in before.md and absent from after.md
- D8 [verbatim]: `PASS D8 every brief '+' line (2) is in the file AFTER, exactly` — re-measured: every one of the 2 brief '+' line(s) in after.md exactly (rstrip)
- D9 [verbatim]: `INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (8/8)` (total 8 = the checker's formula for must_remove=2, expected_plus=2, insert_after=None)

**PR NOTES for the raise seat:** DOC_PATCH — DOCUMENTATION ONLY, zero code bytes: `Blockchain/Dev/docs/DEV-PROCESS.md` (+2/-2 per patch.diff); one file. Apply `patch.diff` strictly (`git apply -p1`) at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Tier: tier 1 (documentation) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night4/input.json`. Brief (located by ticket + ROWID tokens ['1097', 'DEVPROCESS', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1097-R16B-DEVPROCESS.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night4/checker.out`.

```diff
--- a/Blockchain/Dev/docs/DEV-PROCESS.md
+++ b/Blockchain/Dev/docs/DEV-PROCESS.md
@@ -64,3 +64,3 @@
 - **Review isn't testing.** Untested PRs turn the reviewer into the bottleneck and stall the automation work Peter owns.
-- **Separate the ticket from the review.** The author tests, but a second pair of eyes signs it off — never the same person on both.
+- **Separate the ticket from the review.** The author tests, but a second seat signs it off - the QA gate verdict at head plus Wednesday's GO - never the seat that built it.
 - **Merging doesn't wait on the reviewer.** Approval is the gate, not availability. `develop` keeps moving when someone is off.
@@ -272,5 +272,5 @@
 ---
 
-*v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56): a PR merges once it is TESTED — a QA gate verdict at its current head, a Test Evidence block and our own suites — and Wednesday's GO is the approval. Peter runs periodic formal test passes, and demo (UAT) waits for his nod. Merge-signal sentences updated; the 2026-08-27 measurements kept, with dated superseded notes (KS-1092).*
+*v4 - 11 September 2026 - Kam ruled that we approve our own work (16:56): a PR merges once it is TESTED (as defined in `CONTRIBUTING.md`, step 6 of Adopted merge flow) and Wednesday's GO, naming the head SHA, is the approval. Peter runs periodic formal test passes, and demo (UAT) waits for his nod. Merge-signal sentences updated; the 2026-08-27 measurements kept, with dated superseded notes (KS-1092).*
 
 *v3 · 27 August 2026 — Kam ruled the four platform suites are the author's final check before handover, and that GitHub Actions will not be restored. Adds the four suite lines to the Test Evidence block, the manual CI-gate equivalents map KS-685 commissioned, and the branch-protection setting that now blocks every merge until it is unticked. Replaces v2's "suspended, not retired" framing throughout.*
```
