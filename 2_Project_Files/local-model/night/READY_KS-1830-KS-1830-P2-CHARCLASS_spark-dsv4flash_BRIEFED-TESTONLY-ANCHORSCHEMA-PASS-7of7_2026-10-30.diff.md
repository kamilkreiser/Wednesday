# READY — KS-1830-KS-1830-P2-CHARCLASS (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep/out.md.checker/patch.diff`** (from `ls` at 06:05 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 06:05 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7152ac669d2d6af08be5b9dcd35132818377155d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
15	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (15 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 15 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 15 line(s) byte-exact incl. leading whitespace (of 15; 15 line(s) added by the apply)` [a3i_indent.out: `OK 15 line(s) byte-exact incl. leading whitespace (of 15; 15 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `ca46ef18214bd658` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/anchorSchema.ts:124)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep_052731/clone/Blockchain/Dev/services/anchoring/src/anchorSchema.ts:124: 'export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged' -> 'export const DID_PATTERN = /^did:(key|web|jwk):[A-z0-9._:%!*@#-]+\\+?$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/anchorSchema.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 124. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1175-identity-anchoring.test.ts fails at the untouched tip (12 failed / 157 run; controls green; assertion reds)` [red_first.json: failed=12 of total=157; red cell(s): ['anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses an exclamation mark inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses an asterisk inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses an at sign inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a hash sign inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a caret inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a plus sign at the END of the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses an exclamation mark inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses an asterisk inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses an at sign inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a hash sign inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a caret inside the payload (1817-2) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a plus sign at the END of the payload (1817-2) with exactly one invalid_string issue on the field']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1175-identity-anchoring.test.ts passes with the product hunk (157 passed / 157 run)` [green_after.json: failed=0 of total=157, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=545 failed=1 | after: total=559 failed=1` · `NEW reds: []` [baseline_suite.json total=545 failed=1; after_suite.json total=559 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +15/-0 test=src/__tests__/ks1175-identity-anchoring.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (+15/-0 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the tamper target and is byte-unchanged (sha256 ca46ef18214bd658, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `7152ac669d2d6af08be5b9dcd35132818377155d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1830_p2_charclass_sweep/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
@@ -241,6 +241,12 @@
     ['a space inside the payload', REALISTIC_DID_JWK.slice(0, 40) + ' ' + REALISTIC_DID_JWK.slice(40)],
     ['a plus sign inside the payload (KS-1830: standard base64, not base64url)', REALISTIC_DID_JWK.slice(0, 40) + '+' + REALISTIC_DID_JWK.slice(40)],
     ['a slash inside the payload (KS-1830: standard base64, not base64url)', REALISTIC_DID_JWK.slice(0, 40) + '/' + REALISTIC_DID_JWK.slice(40)],
+    ['an exclamation mark inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '!' + REALISTIC_DID_JWK.slice(40)],
+    ['an asterisk inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '*' + REALISTIC_DID_JWK.slice(40)],
+    ['an at sign inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '@' + REALISTIC_DID_JWK.slice(40)],
+    ['a hash sign inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '#' + REALISTIC_DID_JWK.slice(40)],
+    ['a caret inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '^' + REALISTIC_DID_JWK.slice(40)],
+    ['a plus sign at the END of the payload (1817-2)', REALISTIC_DID_JWK + '+'],
   ];
   for (const field of DID_JWK_FIELDS) {
     for (const [label, bad] of SHAPE_REFUSALS) {
@@ -265,6 +271,15 @@
       const row = SHAPE_REFUSALS.find(([label]) => label.includes('slash'));
       expect(row?.[1].replace('/', '')).toBe(REALISTIC_DID_JWK);
       expect(row?.[1].split('/')).toHaveLength(2);
+    });
+    it(`control 1817-2 ${field}: each added row is the realistic did:jwk with exactly one extra character, nothing else (the END row appends one plus sign)`, () => {
+      for (const [word, ch] of [['exclamation mark', '!'], ['asterisk', '*'], ['at sign', '@'], ['hash sign', '#'], ['caret', '^']]) {
+        const row = SHAPE_REFUSALS.find(([label]) => label.includes(word + ' inside the payload (1817-2)'));
+        expect(row?.[1].replace(ch, '')).toBe(REALISTIC_DID_JWK);
+        expect(row?.[1].split(ch)).toHaveLength(2);
+      }
+      const end = SHAPE_REFUSALS.find(([label]) => label.includes('plus sign at the END of the payload (1817-2)'));
+      expect(end?.[1]).toBe(REALISTIC_DID_JWK + '+');
     });
   }
 });
```
