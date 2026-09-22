# READY — KS-1097-1097CLAUDEMD-R16B (Ornith, briefed, doc_patch, markdown) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night5/out.md.checker/patch.diff`** (from `ls` at 13:34 2026-09-22; sha256[:16] dc54e1f344372f81, 915 B — a BYTE count; byte-equal to the out.md fence (the model's as-written block)). Checker D2 (verbatim from checker.out): `PASS D2 diff applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night5/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed11-drafter-precheck/CLAUDEMD/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.md` (the document after its patch) `cmp` rc 0.

**Held 13:34 2026-09-22 by Wednesday after a source read (hold_ready.py, doc_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night5/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `doc_1097CLAUDEMD-R16B.json`).
- Subject [checker.out D0, verbatim]: `PASS D0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, CLAUDE.md present`
- Output shape [checker.out D1, verbatim]: `PASS D1 output is exactly one fenced ```diff block`
- Touched-file set [checker.out D3, verbatim]: `PASS D3 touched-file set == { CLAUDE.md }` — `patch.diff`'s own `+++` header names exactly `CLAUDE.md`; 1 hunk(s), `+` lines 1 (ASCII), `-` lines 3 (counted from patch.diff); before.md → after.md: 3 line(s) removed, 1 added (difflib on the checker's own files).
- Tip content [out.md.checker/before.md]: byte-equal to input.json['files'][product_file]; after.md is byte-equal to patch.diff re-applied to before.md (`git apply -p1 (strict)`, scratch tempdir, sha256 556803387ecbf749).
- Sections [checker.out D4/D5, verbatim, one pair per required section]:
  - `PASS D4 BEFORE: '## Branching' lacks ['the pending ruling is raise-to-1', 'Kam applies it himself'] at the tip (control: section found, 85 lines)`
  - `PASS D5 AFTER: '## Branching' carries ['the pending ruling is raise-to-1', 'Kam applies it himself']`
- section `## Branching` tokens ['the pending ruling is raise-to-1', 'Kam applies it himself'] — before.md: found at line 241, 85 lines, every token ABSENT; after.md: found at line 241, 83 lines, every token PRESENT (re-measured with the checker's section rule)
- D6 [verbatim]: `PASS D6 every changed region lies inside the required sections (1 section(s), measured on before/after)`
- D7 [verbatim]: `PASS D7 every must-remove line (3) present before and absent after (control: all found at the tip)` — re-measured: every one of the 3 must_remove line(s) in before.md and absent from after.md
- D8 [verbatim]: `PASS D8 every brief '+' line (1) is in the file AFTER, exactly` — re-measured: every one of the 1 brief '+' line(s) in after.md exactly (rstrip)
- D9 [verbatim]: `INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (8/8)` (total 8 = the checker's formula for must_remove=3, expected_plus=1, insert_after=None)

**PR NOTES for the raise seat:** DOC_PATCH — DOCUMENTATION ONLY, zero code bytes: `CLAUDE.md` (+1/-3 per patch.diff); one file. Apply `patch.diff` strictly (`git apply -p1`) at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Tier: tier 1 (documentation) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night5/input.json`. Brief (located by ticket + ROWID tokens ['1097', 'CLAUDEMD', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1097-R16B-CLAUDEMD.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1097-ornith35b-night5/checker.out`.

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -265,5 +265,3 @@
   so a missing box/ticket fails the check, then (2) add the check names to the develop AND
-  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): Kam has
-  ruled on the required-approvals setting and that ruling is not yet applied; turning required reviews on
-  while fleet PRs carry 0 GitHub reviews would block every fleet merge.]* The former
+  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): the pending ruling is raise-to-1 (Kam's card `secuura-required-approvals-zero-after-the-untick`; Kam applies it himself; not yet applied) - do not turn it on while fleet PRs carry 0 GitHub reviews: it would block every fleet merge.]* The former
   Environment-based sign-off jobs were removed in favour of this checkbox approach.
```
