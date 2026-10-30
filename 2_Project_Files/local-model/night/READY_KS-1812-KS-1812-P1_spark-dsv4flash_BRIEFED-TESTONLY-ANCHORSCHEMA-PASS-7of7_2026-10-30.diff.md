# READY — KS-1812-KS-1812-P1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once-control-r3/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (anchorSchema.test.ts, sha256 equal).

**Held 13:50 2026-10-30 by Spark operator 24 (Wednesday) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `40c06084919d5aff132e82693cd60d513cb40ba7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
28	0	Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (23 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 28 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 23 line(s) byte-exact incl. leading whitespace (of 23; 28 line(s) added by the apply)` [a3i_indent.out: `OK 23 line(s) byte-exact incl. leading whitespace (of 23; 28 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `ca46ef18214bd658` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/anchorSchema.ts:166)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once_134821/clone/Blockchain/Dev/services/anchoring/src/anchorSchema.ts:166: '  if (!value.startsWith(DID_JWK_PREFIX) || value.length > DID_MAX_LENGTH || !DID_PATTERN.test(value)) return null;' -> '  if (!value.startsWith(DID_JWK_PREFIX) || value.length > DID_MAX_LENGTH) return null;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/anchorSchema.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 166. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/anchorSchema.test.ts fails at the untouched tip (4 failed / 72 run; controls green; assertion reds)` [red_first.json: failed=4 of total=72; red cell(s): ['anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason RED KS-1812 R1 actorDid: a public did:jwk with base64 padding is refused once, as invalid_string only', 'anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason RED KS-1812 R1 orgDid: a public did:jwk with base64 padding is refused once, as invalid_string only', 'anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason RED KS-1812 R2 actorDid: a did:jwk with a space inside the payload is refused once, as invalid_string only', 'anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason RED KS-1812 R2 orgDid: a did:jwk with a space inside the payload is refused once, as invalid_string only']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/anchorSchema.test.ts passes with the product hunk (72 passed / 72 run)` [green_after.json: failed=0 of total=72, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=550 failed=1 | after: total=556 failed=1` · `NEW reds: []` [baseline_suite.json total=550 failed=1; after_suite.json total=556 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +28/-0 test=src/__tests__/anchorSchema.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts` (+28/-0 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the tamper target and is byte-unchanged (sha256 ca46ef18214bd658, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `40c06084919d5aff132e82693cd60d513cb40ba7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1812_p1_didjwk_refused_once/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts
@@ -260,3 +260,31 @@
+describe('anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason', () => {
+  // A public P-256 JWK (the RFC 7515 A.3 coordinates), unpadded base64url: the payload of an acceptable did:jwk.
+  const PUBLIC_PAYLOAD = Buffer.from(
+    JSON.stringify({ kty: 'EC', crv: 'P-256', x: 'f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU', y: 'x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0' }),
+  ).toString('base64url');
+  const PRIVATE_PAYLOAD = Buffer.from(JSON.stringify({ kty: 'EC', crv: 'P-256', d: 'jpsQnnGQmL-YBIffH1136cspYG6-0iY7X1fCE9-E9LI' })).toString('base64url');
+  const FIELDS = ['actorDid', 'orgDid'] as const;
+
+  /** The zod issue codes that belong to the field under test, so a refusal for some other reason cannot stand in for it. */
+  const codesFor = (field: string, value: string): string[] => {
+    const r = anchorDocumentSchema.safeParse({ ...BASE_BODY, identity: { [field]: value } });
+    return r.success ? [] : r.error.issues.filter((i) => i.path.join('.') === `identity.${field}`).map((i) => i.code);
+  };
+
+  it.each(FIELDS)('RED KS-1812 R1 %s: a public did:jwk with base64 padding is refused once, as invalid_string only', (field) => {
+    expect(codesFor(field, `did:jwk:${PUBLIC_PAYLOAD}==`)).toEqual(['invalid_string']);
+  });
+
+  it.each(FIELDS)('RED KS-1812 R2 %s: a did:jwk with a space inside the payload is refused once, as invalid_string only', (field) => {
+    expect(codesFor(field, 'did:jwk:ab cd')).toEqual(['invalid_string']);
+  });
+
+  it.each(FIELDS)('control KS-1812 C1 %s: the public did:jwk is accepted and the private one is refused by the custom check alone', (field) => {
+    expect(codesFor(field, `did:jwk:${PUBLIC_PAYLOAD}`)).toEqual([]);
+    expect(codesFor(field, `did:jwk:${PRIVATE_PAYLOAD}`)).toEqual(['custom']);
+  });
+});
+
 describe('buildFlatAnchorMetadataPayload — KS-721 exact anchored key set', () => {
   // The regression guard the KS-721 widening earns. buildFlatAnchorMetadataPayload
   // is the ONE path to the public ledger, and the ledger is immutable — a field
```

> OPERATOR 24 SCOPE NOTE: touches the anchoring service (not index.ts, not KS-1384, no open PR file overlaps at 2026-10-30). Operator 19 had treated the whole anchoring service as out; Wednesday to confirm before a raise.
