# KS-1828 (gate 18 survivor X8, Spark operator 11, 2026-10-30): the sign-only refinement is pinned for upload and no-verb only. test_only, gen/mk_testonly.py.
PROD='Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TEST='Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts'
IMP_OLD="import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';\n"
IMP_NEW="import { ACCEPTED_LIFECYCLE_VERBS, anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';\n"
ANCHOR="    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { signatureHash: SIG } });\n    expect(result.success).toBe(false);\n  });\n"
CELL = r'''
  // KS-1828 (gate 18 mutant X8): R2 and R3 pin the sign-only rule for `upload` and for no verb only, so a refinement that also admitted `declare` stayed 23 of 23. Every other accepted verb is driven here.
  const OTHER_VERBS = ACCEPTED_LIFECYCLE_VERBS.filter((verb) => verb !== 'sign');

  it.each(OTHER_VERBS)('RED KS-1828 R6: a signatureHash on the %s verb is refused, not anchored', (verb) => {
    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: verb, signatureHash: SIG } });
    expect(result.success).toBe(false);
  });

  it('control KS-1828 C5: the verbs driven by R6 include declare and upload and never sign', () => {
    expect(OTHER_VERBS).toContain('declare');
    expect(OTHER_VERBS).toContain('upload');
    expect(OTHER_VERBS).not.toContain('sign');
    expect(ACCEPTED_LIFECYCLE_VERBS).toContain('sign');
  });
'''
T=dict(dir='ks_1828_p1_signhash_other_verbs',ticket='KS-1828',
 title='ks1454 sign-verb cells pin the sign-only rule for upload and no verb only, so a refinement that also admits declare survives 23 of 23 (gate 18 mutant X8): add an it.each over every other accepted verb (RUNG 3, TEST-ONLY: two in-place test hunks with a planted tamper; the product does not change)',
 intro="DRAFT by Spark operator 11 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 18 (`0_Brain/reference/2026-10-30_gate18-1811-1812/verdict.md`), finding 1811-3, filed as KS-1828: mutant X8 (`!== 'sign'` becomes `!== 'sign' && data.metadata.documentType !== 'declare'`) leaves both KS-1454 test files 23/23 green. Link the PR as Refs KS-1828 and KS-1454, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=301, tamper_from="  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign') {",
 tamper_to="  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign' && data.metadata.documentType !== 'declare') {",
 statement_ok="line 301 is the whole `if (...) {` header of the KS-1454 refinement inside `anchorDocumentSchema.superRefine`; the tamper appends one more `&&` clause before the `{`, which is gate 18's mutant X8 verbatim; the block body is untouched and the file still compiles",
 edit=[(IMP_OLD, IMP_NEW), (ANCHOR, ANCHOR+CELL)],
 nh_txt="2 hunks: the import line, and the new cells added after cell R3",
 nh_word='TWO hunks (the import line, then the new cells), in file order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 red=['RED KS-1828 R6: a signatureHash on the declare verb'],
 runner='vitest` (`npx vitest run src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden the new cell; two hunks given byte-exact)',
 what_wrong="`anchorSchema.ts:301` refuses `metadata.signatureHash` on any verb but `sign`. The sign-verb test file pins that rule for `upload` (cell R2) and for no verb at all (R3) and for no other verb, so a refinement that ALSO lets `declare` through (`!== 'sign' && ... !== 'declare'`) passes 23 of 23: the rule 'sign only' is not itself pinned. The product is right today; the gap is a missing pin. This task imports `ACCEPTED_LIFECYCLE_VERBS` (exported from `../anchorSchema`, the same tuple that feeds the schema's `documentType` enum) and adds an `it.each` over every accepted verb except `sign`, each expecting `safeParse(...).success` to be false for a hash on that verb, plus a control C5 that the list really contains `declare` and `upload` and not `sign`.",
 where="- `src/anchorSchema.ts:301` - (correct, STAYS) `  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign') {` - the line the tamper corrupts in the checker's clone. `ACCEPTED_LIFECYCLE_VERBS` is exported at :96.\n- Test file: hunk 1 replaces the import at :6. Hunk 2 goes after cell R3: R3 is lines 33-36 (its closing `  });` is :36); :37 is blank; :38 starts the `it.each([` of R4. **The new cells go between :36 and :37.** `BASE_BODY` and `SIG` are in scope at module level (:9-:13).",
 cells="- RED under the tamper: the `declare` instance of `RED KS-1828 R6` fails by assertion (the mutant parses a `declare` body with a hash: `success` is `true`, expected `false`). Every other R6 instance stays green under the tamper.\n- GREEN at the untouched tip: all R6 instances (the refinement refuses a hash on every verb but sign) and C5.\n- CONTROL C5: green on BOTH trees.\n- Every existing cell stays green on both trees.",
 unmeasured="- The drafter did NOT run vitest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The set of verbs is read at run time from `ACCEPTED_LIFECYCLE_VERBS` (it includes the transitional `certify` alias); the instance count is whatever the tuple has at the tip. A verb added later is pinned automatically.\n- If a verb were refused by some OTHER rule of the schema (a verb-specific required field), its R6 instance would be green for the wrong reason; the checker's red-under-tamper proves only the `declare` instance can go red.\n- Open PRs touching either file: see the overlap count in the operator report (checked against every open PR on 2026-10-30).",
 scope="**Closes finding 1811-3 (KS-1828) only.** Link the PR as Refs KS-1828 / KS-1454. No product file changes.",
)
