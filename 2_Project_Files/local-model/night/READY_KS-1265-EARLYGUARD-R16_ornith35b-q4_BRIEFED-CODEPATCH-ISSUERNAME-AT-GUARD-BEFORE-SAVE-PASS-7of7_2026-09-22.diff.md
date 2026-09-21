# READY — KS-1265-EARLYGUARD-R16 (Ornith, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 03:50 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in documents.ts (run 14 vs golden 11 body lines — context, since the change lines are equal) (identical in ks549-documents-create-issuer-name-persist.test.ts); hunk headers differ (documents.ts: golden `@@ -614,3 +614,11 @@` vs run `@@ -611,6 +611,14 @@ documentsRouter.post(`; ks549-documents-create-issuer-name-persist.test.ts: golden `@@ -141,11 +141,8 @@` vs run `@@ -141,11 +141,8 @@ describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {`); APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks549-documents-create-issuer-name-persist.test.ts/documents.ts, sha256 equal).

**Held 03:50 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `64ab105132eada0621622acf4d6053bc59926780`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/documents.ts , Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/documents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	0	Blockchain/Dev/services/originate/src/routes/documents.ts
4	7	Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (8 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 8 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/documents.ts byte-exact incl. leading whitespace (apply mode strict): OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)` [a3i_indent.out: `OK 8 line(s) byte-exact incl. leading whitespace (of 8; 8 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/documents.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks549-documents-create-issuer-name-persist.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-549 POST /api/documents — top-level issuerName persists into data never persists an email-shaped issuerName (E-01 guard parity)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks549-documents-create-issuer-name-persist.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=809 failed=0 | after: total=809 failed=0` · `NEW reds: []` [baseline_suite.json total=809 failed=0; after_suite.json total=809 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +12/-7 test=src/__tests__/ks549-documents-create-issuer-name-persist.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+8/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts` (+4/-7); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `64ab105132eada0621622acf4d6053bc59926780` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1265-R16-EARLYGUARD.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1265-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -611,6 +611,14 @@ documentsRouter.post(
       // same condition here keeps an email out of the stored blob.
       const topLevelIssuerName =
         typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : '';
+      // KS-1265: refuse an "@"-carrying issuerName BEFORE the save below (it was refused at the anchoring
+      // step, AFTER saveDocument and the provenance row) - a refused create must write nothing.
+      if (topLevelIssuerName.includes('@')) {
+        return res.status(400).json({
+          success: false,
+          error: { code: 'BAD_REQUEST', message: 'issuerName must not contain "@" - it should be the organisation name, not a user email (audit E-01)' },
+        });
+      }
       if (topLevelIssuerName && !topLevelIssuerName.includes('@') && !data.issuerName) {
         data.issuerName = topLevelIssuerName;
       }
--- a/Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts
@@ -141,11 +141,8 @@ describe('KS-549 POST /api/documents — top-level issuerName persists into data', () => {
       issuerName: 'someone@example.com',
       data: { title: 'Doc' },
     });
-    // The route's existing E-01 guard rejects "@"-carrying issuerName in the
-    // anchor scope; whatever the status, the blob must not carry the email.
-    if (mockSaveDocument.mock.calls.length > 0) {
-      const saved = mockSaveDocument.mock.calls[0][0];
-      expect(saved.data.issuerName).toBeUndefined();
-    }
-    expect([201, 400]).toContain(res.status);
+    // KS-1265: the E-01 guard now refuses BEFORE the save. A refused create writes nothing:
+    // 400, and saveDocument is never called (at the old tip it was called once, then 400).
+    expect(res.status).toBe(400);
+    expect(mockSaveDocument).toHaveBeenCalledTimes(0);
   });
```
