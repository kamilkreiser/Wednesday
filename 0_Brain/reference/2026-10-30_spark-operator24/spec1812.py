# KS-1812 (anchoring anchorSchema.ts didJwkRefusal: the early return for a pattern-refused value is pinned by no cell). Spark operator 24. test_only, ONE existing test modified in place.
PROD='Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TEST='Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts'
REF='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts'
ANCHOR="""describe('buildFlatAnchorMetadataPayload — KS-721 exact anchored key set', () => {
"""
CELLS="""describe('anchorDocumentSchema - KS-1812 a did:jwk the shape checks already refuse is refused once, for its own reason', () => {
  // A public P-256 JWK (the RFC 7515 A.3 coordinates), unpadded base64url: the payload of an acceptable did:jwk.
  const PUBLIC_PAYLOAD = Buffer.from(
    JSON.stringify({ kty: 'EC', crv: 'P-256', x: 'f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU', y: 'x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0' }),
  ).toString('base64url');
  const PRIVATE_PAYLOAD = Buffer.from(JSON.stringify({ kty: 'EC', crv: 'P-256', d: 'jpsQnnGQmL-YBIffH1136cspYG6-0iY7X1fCE9-E9LI' })).toString('base64url');
  const FIELDS = ['actorDid', 'orgDid'] as const;

  /** The zod issue codes that belong to the field under test, so a refusal for some other reason cannot stand in for it. */
  const codesFor = (field: string, value: string): string[] => {
    const r = anchorDocumentSchema.safeParse({ ...BASE_BODY, identity: { [field]: value } });
    return r.success ? [] : r.error.issues.filter((i) => i.path.join('.') === `identity.${field}`).map((i) => i.code);
  };

  it.each(FIELDS)('RED KS-1812 R1 %s: a public did:jwk with base64 padding is refused once, as invalid_string only', (field) => {
    expect(codesFor(field, `did:jwk:${PUBLIC_PAYLOAD}==`)).toEqual(['invalid_string']);
  });

  it.each(FIELDS)('RED KS-1812 R2 %s: a did:jwk with a space inside the payload is refused once, as invalid_string only', (field) => {
    expect(codesFor(field, 'did:jwk:ab cd')).toEqual(['invalid_string']);
  });

  it.each(FIELDS)('control KS-1812 C1 %s: the public did:jwk is accepted and the private one is refused by the custom check alone', (field) => {
    expect(codesFor(field, `did:jwk:${PUBLIC_PAYLOAD}`)).toEqual([]);
    expect(codesFor(field, `did:jwk:${PRIVATE_PAYLOAD}`)).toEqual(['custom']);
  });
});

describe('buildFlatAnchorMetadataPayload — KS-721 exact anchored key set', () => {
"""
T=dict(dir='ks_1812_p1_didjwk_refused_once',ticket='KS-1812',test=TEST,product=PROD,ref=REF,
 runner='vitest` (`npx vitest run src/__tests__/anchorSchema.test.ts` from `Blockchain/Dev/services/anchoring`',
 rung='3-4 (test HARDENING: a mutant that survives all 183 cells gets a killing cell; the new describe is given byte-exact, the tamper is the mutant the ticket names)',
 title="anchoring: pin didJwkRefusal's early return for a pattern-refused did:jwk (KS-1812, gate 16 mutant X12; TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 24 for Wednesday, 2026-10-30 AEDT. Secuura (anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1812 (gate 16 finding 1807-1, a disclosed test gap). In `anchorSchema.ts` the first line of `didJwkRefusal` returns null for a value the shape checks (cap, alphabet pattern) already refuse, so a malformed did:jwk is refused once. Removing the `|| !DID_PATTERN.test(value)` clause leaves all 183 cells of the two DID test files green, because no cell asserts the issue COUNT for a pattern-refused value. This task adds the cells. The file anchorSchema.test.ts is used on purpose: ks1175-identity-anchoring.test.ts is touched by open PR 1825.",
 tamper_line=166,
 tamper_from="  if (!value.startsWith(DID_JWK_PREFIX) || value.length > DID_MAX_LENGTH || !DID_PATTERN.test(value)) return null;",
 tamper_to="  if (!value.startsWith(DID_JWK_PREFIX) || value.length > DID_MAX_LENGTH) return null;",
 statement_ok="line 166 is a one-statement `if (...) return null;`; the tamper removes only the `|| !DID_PATTERN.test(value)` clause (mutant X12), so the statement stays complete and the file still compiles (DID_PATTERN is still used by the regex below)",
 edit=(ANCHOR,CELLS),
 red=['RED KS-1812 R1','RED KS-1812 R2'],
 what_wrong="`didJwkRefusal` in `services/anchoring/src/anchorSchema.ts:166` begins `if (!value.startsWith(DID_JWK_PREFIX) || value.length > DID_MAX_LENGTH || !DID_PATTERN.test(value)) return null;`. The cap clause is pinned by an existing cell; the pattern clause is not: with it removed, `did:jwk:<public payload>==` and `did:jwk:ab cd` report TWO issues (`invalid_string` from the regex plus `custom` from the decode check) instead of ONE, and every existing cell stays green. It is still a 400, so only the error body differs. This task adds a describe at the end of `anchorSchema.test.ts`: R1 and R2 (each over both fields, `actorDid` and `orgDid`) assert the issue codes of a pattern-refused value equal exactly `['invalid_string']`; C1 is the positive/negative control (the public did:jwk gives no issue, the private one gives exactly `['custom']`).",
 where="- `services/anchoring/src/anchorSchema.ts:166` - (correct, STAYS) the early return; the line the tamper edits in the checker's clone (the tamper drops its pattern clause).\n- The test hunk is a NEW describe inserted between two describes of `anchorSchema.test.ts` (it sits directly before `describe('buildFlatAnchorMetadataPayload — KS-721 exact anchored key set'`). It uses `anchorDocumentSchema` and `BASE_BODY`, both already in the file.",
 cells="- RED under the tamper: `RED KS-1812 R1` and `R2` (4 test instances, 2 fields each) fail by assertion: the codes read `['invalid_string','custom']`, not `['invalid_string']`.\n- GREEN at the untouched tip: all cells, R1, R2 and C1 included.\n- C1 stays green under the tamper (a well-formed payload is not pattern-refused).",
 unmeasured="- The drafter did NOT run vitest for the brief: RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- The ticket proposed the same two values; the payload for R1 is built in the test from a public P-256 JWK, not copied from another test file.\n- The ks1175 describes already exercise the same schema via `identity`; whether the same cells would also belong there is not decided (PR 1825 changes that file).\n- Open PRs touching anchoring: 1821 (index.ts), 1825 (reconciler.ts, ks1175-identity-anchoring.test.ts, ks1816 test). None touches anchorSchema.ts or anchorSchema.test.ts (read 2026-10-30 from the PR heads).",
 scope="**Refs KS-1812, never a close-word.** Pins the pattern clause only; the rest of the ticket (whether the error-body count matters) is not decided here.",
)
