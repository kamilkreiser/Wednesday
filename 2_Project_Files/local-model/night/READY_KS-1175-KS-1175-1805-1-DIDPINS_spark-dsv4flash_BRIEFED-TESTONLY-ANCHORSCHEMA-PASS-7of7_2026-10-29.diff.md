# READY — KS-1175-KS-1175-1805-1-DIDPINS (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins/out.md.checker/patch.diff`** (from `ls` at 21:18 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 21:18 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
32	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (31 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 32 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (1 NON-ASCII chars); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 31 line(s) byte-exact incl. leading whitespace (of 31; 32 line(s) added by the apply)` [a3i_indent.out: `OK 31 line(s) byte-exact incl. leading whitespace (of 31; 32 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `70886499dafd803b` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/anchorSchema.ts:124)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins_211347/clone/Blockchain/Dev/services/anchoring/src/anchorSchema.ts:124: 'export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged' -> 'export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%=\\s-]*/im; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/anchorSchema.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 124. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1175-identity-anchoring.test.ts fails at the untouched tip (14 failed / 135 run; controls green; assertion reds)` [red_first.json: failed=14 of total=135; red cell(s): ['anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses an empty payload (did:jwk:) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a trailing newline with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a newline between two payloads with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses base64 padding (==) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a trailing space with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses an upper-case method (DID:JWK:) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 actorDid: refuses a space inside the payload with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses an empty payload (did:jwk:) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a trailing newline with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a newline between two payloads with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses base64 padding (==) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a trailing space with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses an upper-case method (DID:JWK:) with exactly one invalid_string issue on the field', 'anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings) RED KS-1805-1 orgDid: refuses a space inside the payload with exactly one invalid_string issue on the field']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1175-identity-anchoring.test.ts passes with the product hunk (135 passed / 135 run)` [green_after.json: failed=0 of total=135, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=456 failed=1 | after: total=474 failed=1` · `NEW reds: []` [baseline_suite.json total=456 failed=1; after_suite.json total=474 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +32/-0 test=src/__tests__/ks1175-identity-anchoring.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` (+32/-0 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the tamper target and is byte-unchanged (sha256 70886499dafd803b, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1805_1_did_pattern_pins/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
@@ -228,3 +228,35 @@
+// KS-1175 / gate 15 finding 1805-1 (QA gate 15, 2026-10-29): six weakenings of DID_PATTERN (anchorSchema.ts) survived every cell above: the `m` flag (a newline),
+// `=` in the class (padding), `$` dropped (trailing junk), the `i` flag (case), `+` -> `*` (an empty payload) and `\s` in the class (whitespace). The product refuses
+// each input below today; nothing pinned it. Each cell asserts that the field's OWN issues are exactly one `invalid_string` (the shape pattern), so a weakened pattern
+// goes red whether it then accepts the value (no issue) or lets the private-key guard refuse it for another reason (a `custom` issue).
+describe('anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings)', () => {
+  const JWK_PAYLOAD = REALISTIC_DID_JWK.slice('did:jwk:'.length);
+  const SHAPE_REFUSALS: Array<[string, string]> = [
+    ['an empty payload (did:jwk:)', 'did:jwk:'],
+    ['a trailing newline', REALISTIC_DID_JWK + '\n'],
+    ['a newline between two payloads', REALISTIC_DID_JWK + '\n' + JWK_PAYLOAD],
+    ['base64 padding (==)', REALISTIC_DID_JWK + '=='],
+    ['a trailing space', REALISTIC_DID_JWK + ' '],
+    ['an upper-case method (DID:JWK:)', 'DID:JWK:' + JWK_PAYLOAD],
+    ['a space inside the payload', REALISTIC_DID_JWK.slice(0, 40) + ' ' + REALISTIC_DID_JWK.slice(40)],
+  ];
+  for (const field of DID_JWK_FIELDS) {
+    for (const [label, bad] of SHAPE_REFUSALS) {
+      it(`RED KS-1805-1 ${field}: refuses ${label} with exactly one invalid_string issue on the field`, () => {
+        expect(parseField(field, bad).success).toBe(false);
+        expect(issuesFor(field, bad).map((i) => i.code)).toEqual(['invalid_string']);
+      });
+    }
+    it(`control KS-1805-1 ${field}: refuses a leading space (the pattern is anchored at the start), one invalid_string issue`, () => {
+      expect(issuesFor(field, ' ' + REALISTIC_DID_JWK).map((i) => i.code)).toEqual(['invalid_string']);
+    });
+    it(`control KS-1805-1 ${field}: still accepts a did:key and the realistic did:jwk, kept verbatim`, () => {
+      expectKept(field, 'did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK');
+      expectKept(field, REALISTIC_DID_JWK);
+    });
+  }
+});
+
 // KS-1175 (Kam's ruling, 2026-10-29 19:51:25 AEDT, card secuura-ks1175-private-jwk-guard-1029, option a, verbatim: "Add a narrow
 // guard before deploying"): a did:jwk is decoded ONLY to refuse private-key members (d, p, q, dp, dq, qi, k), with a 400 and
 // a clear message; "Nothing else about the JWK is checked". Wednesday's reading of the ruling adds: a payload that does not
```
