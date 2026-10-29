# "1805-1" (gate 15, Spark operator 10, 2026-10-29): pin the six DID_PATTERN weakenings that survived every cell. test_only, mk_testonly.py.
PROD='Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TEST='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts'
ANCHOR="  });\n});\n\n// KS-1175 (Kam's ruling, 2026-10-29 19:51:25 AEDT, card secuura-ks1175-private-jwk-guard-1029, option a, verbatim:"
BLOCK='''  });
});

// KS-1175 / gate 15 finding 1805-1 (Seat Q 2026-10-29): six weakenings of DID_PATTERN (anchorSchema.ts) survived every cell above: the `m` flag (a newline),
// `=` in the class (padding), `$` dropped (trailing junk), the `i` flag (case), `+` -> `*` (an empty payload) and `\\s` in the class (whitespace). The product refuses
// each input below today; nothing pinned it. Each cell asserts that the field's OWN issues are exactly one `invalid_string` (the shape pattern), so a weakened pattern
// goes red whether it then accepts the value (no issue) or lets the private-key guard refuse it for another reason (a `custom` issue).
describe('anchorDocumentSchema — KS-1175 did:jwk shape refusals pinned (gate 15, 1805-1: the six regex weakenings)', () => {
  const JWK_PAYLOAD = REALISTIC_DID_JWK.slice('did:jwk:'.length);
  const SHAPE_REFUSALS: Array<[string, string]> = [
    ['an empty payload (did:jwk:)', 'did:jwk:'],
    ['a trailing newline', REALISTIC_DID_JWK + '\\n'],
    ['a newline between two payloads', REALISTIC_DID_JWK + '\\n' + JWK_PAYLOAD],
    ['base64 padding (==)', REALISTIC_DID_JWK + '=='],
    ['a trailing space', REALISTIC_DID_JWK + ' '],
    ['an upper-case method (DID:JWK:)', 'DID:JWK:' + JWK_PAYLOAD],
    ['a space inside the payload', REALISTIC_DID_JWK.slice(0, 40) + ' ' + REALISTIC_DID_JWK.slice(40)],
  ];
  for (const field of DID_JWK_FIELDS) {
    for (const [label, bad] of SHAPE_REFUSALS) {
      it(`RED KS-1805-1 ${field}: refuses ${label} with exactly one invalid_string issue on the field`, () => {
        expect(parseField(field, bad).success).toBe(false);
        expect(issuesFor(field, bad).map((i) => i.code)).toEqual(['invalid_string']);
      });
    }
    it(`control KS-1805-1 ${field}: refuses a leading space (the pattern is anchored at the start), one invalid_string issue`, () => {
      expect(issuesFor(field, ' ' + REALISTIC_DID_JWK).map((i) => i.code)).toEqual(['invalid_string']);
    });
    it(`control KS-1805-1 ${field}: still accepts a did:key and the realistic did:jwk, kept verbatim`, () => {
      expectKept(field, 'did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK');
      expectKept(field, REALISTIC_DID_JWK);
    });
  }
});

// KS-1175 (Kam's ruling, 2026-10-29 19:51:25 AEDT, card secuura-ks1175-private-jwk-guard-1029, option a, verbatim:'''
FROM_LINE="export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged"
TO_LINE="export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%=\\s-]*/im; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged"
red=['RED KS-1805-1 actorDid:','RED KS-1805-1 orgDid:']
T=dict(dir='ks_1805_1_did_pattern_pins',ticket='KS-1175',
 title='the six DID_PATTERN weakenings gate 15 found surviving (finding 1805-1: m flag, =, dropped $, i flag, + to *, \\s) have no cell: pin the refusals (RUNG 3, TEST-ONLY: one in-place hunk with a planted tamper that applies all six weakenings; the product does not change)',
 intro="DRAFT by Spark operator 10 for Wednesday, 2026-10-29 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 15 (`0_Brain/reference/2026-10-29_gate15-1805-1806/verdict.md`), finding 1805-1 (minor) on PR 1805 (KS-1175 did:jwk, merged): \"Six regex weakenings survive every cell ... the product refuses each of these inputs today, but nothing pins it\", with the owner regression test named: refusal cells on both fields for `did:jwk:`, a trailing and an embedded newline, `==` padding, a leading and a trailing space, `DID:JWK:` and an embedded space. This brief writes those cells. The ticket is KS-1175 (the PR is on it): the Linear issue was not re-read for this brief.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=124, tamper_from=FROM_LINE, tamper_to=TO_LINE,
 statement_ok="line 124 is one complete statement (`export const DID_PATTERN = /.../;` plus a trailing line comment) and the tamper replaces only the regex literal: `$` dropped, `+` -> `*`, `=` and `\\s` added to the class, flags `i` and `m` added (all six weakenings of finding 1805-1 at once); it is still a valid RegExp literal, so the file compiles and the only behaviour change is that DID_PATTERN is looser",
 edit=(ANCHOR,BLOCK),
 red=red, nh_txt='1 hunk: a new describe inserted above the private-key guard comment block (after the first did:jwk describe, :226)', nh_word='ONE hunk', nh_head='ONE EDIT in the TEST file (one hunk)',
 runner='vitest` (`npx vitest run src/__tests__/ks1175-identity-anchoring.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden the cells; one hunk given byte-exact)',
 what_wrong="`ks1175-identity-anchoring.test.ts` pins the did:jwk widening of `DID_PATTERN` (`anchorSchema.ts:124`, `/^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/`) but QA gate 15 put six weakenings on that one regex and ran both DID test files (132 cells): all six passed every cell. They are the `m` flag (a newline), `=` in the class (padding), `$` dropped (trailing junk), the `i` flag (case), `+` -> `*` (an empty payload) and `\\s` in the class (whitespace). The product refuses all of these inputs today; the gap is a missing pin. This task adds a describe with 7 refusal inputs x 2 fields (`actorDid`, `orgDid`): for each, the field's own zod issues must be EXACTLY one `invalid_string` (the shape pattern's code). That form goes red on a weakened pattern whether the pattern then accepts the value (no issue at all) or hands it to the private-key guard `didJwkRefusal`, which refuses an undecodable payload with a `custom` issue. Two controls per field are green on both trees. The new cells reuse the file's own helpers `parseField`, `issuesFor`, `expectKept`, `REALISTIC_DID_JWK` and `DID_JWK_FIELDS` (module scope, defined at :138-:170, above the insertion point).",
 where="- `src/anchorSchema.ts:124` - (correct, STAYS) `export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged` - the line the tamper corrupts in the checker's clone. `didJwkRefusal` (:165-) returns null when `!DID_PATTERN.test(value)`, so a weakened pattern changes WHICH rule refuses.\n- Test file: the first did:jwk describe ends with `  });` and `});` at :225-226; :227 is blank; :228 starts the comment block `// KS-1175 (Kam's ruling, 2026-10-29 19:51:25 AEDT, card secuura-ks1175-private-jwk-guard-1029, option a, verbatim:` of the next describe. **The new describe goes between :226 and :228.**\n- Helpers in scope at module level (lines 138-170 of the test file): `DID_JWK_FIELDS`, `parseField`, `issuesFor`, `expectKept`, `PUBLIC_JWK`, `didJwkOf`, `REALISTIC_DID_JWK` (a 231-character did:jwk).",
 cells="- RED under the tamper (all 14, by assertion): each `RED KS-1805-1 <field>: refuses <label> ...` calls `expect(issuesFor(field, bad).map(code)).toEqual(['invalid_string'])`. Under the tampered pattern the empty payload, padding, a trailing space, a newline and an inner space all PASS the pattern, then `didJwkRefusal` refuses them with ONE `custom` issue (`['custom']`, not equal); `DID:JWK:...` passes the `i` pattern and the guard (`startsWith('did:jwk:')` is false) adds nothing (`[]`, not equal). The first assertion `success` is `false` in the tampered tree for all but the upper-case value, so that cell fails at the second assertion.\n- GREEN at the untouched tip: all 14 (each input fails the shape pattern, which is the only issue; the guard returns null on a pattern miss).\n- CONTROL (2 per field, 4 cells; green on BOTH trees): a LEADING space is refused with one `invalid_string` (the tamper keeps `^` and the `m` flag only matches after a newline, so it stays refused; this input is in the gate's list but none of the six weakenings changes it, so it is a control, not a red cell), and a `did:key` plus the realistic `did:jwk` are still accepted verbatim.",
 unmeasured="- The drafter did NOT run vitest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The checker plants ONE tamper, which applies all six weakenings together. It proves every new red cell goes red under the combined tamper; it does NOT prove each of the six weakenings is individually caught by a cell. The operator's by-hand six single-weakening check is recorded in the report.\n- Finding 1805-1 names the inputs on the pre-#1807 tree (`did:jwk:abc` style payloads). Here the payloads are the file's realistic decoding did:jwk so that a weakened pattern is not also masked by anything else; the guard that #1807 added is why a weakened pattern now produces a `custom` issue instead of an accepted value for most inputs.\n- Only `actorDid` and `orgDid` are driven (the two fields that use `DID_PATTERN`); the openapi YAML pattern is not tested here.\n- Open PRs touching this test file or anchorSchema.ts: see the operator's overlap run in the report (gen/overlap.py).",
 scope="**Closes finding 1805-1 only** (not 1805-2 comment wording, nor 1805-3, nor 1807-1, which is a different unpinned line). Link the PR as Refs KS-1175. No product file changes.",
)
