# KS-1830 (gate 18 finding 1812-2, Spark operator 12, 2026-10-30): DID_PATTERN class widened by '+' or '/' survives all 135 cells. test_only, gen/mk_testonly.py.
# One spec, two briefs: CH=plus (tamper adds '+') or CH=slash (tamper adds '/'): the test_only tier plants ONE tamper per brief.
import os
CH = os.environ['CH']
assert CH in ('plus', 'slash')
CHAR, WORD, DIRN, ID = ('+', 'plus sign', 'plus', 'E1') if CH == 'plus' else ('/', 'slash', 'slash', 'E2')
PROD = 'Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TEST = 'Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts'
ROW_ANCHOR = "    ['a space inside the payload', REALISTIC_DID_JWK.slice(0, 40) + ' ' + REALISTIC_DID_JWK.slice(40)],\n"
ROW = f"    ['a {WORD} inside the payload (KS-1830: standard base64, not base64url)', REALISTIC_DID_JWK.slice(0, 40) + '{CHAR}' + REALISTIC_DID_JWK.slice(40)],\n"
CTL_ANCHOR = "      expectKept(field, REALISTIC_DID_JWK);\n    });\n"
CTL = f'''    it(`control KS-1830 ${{field}}: the {WORD} row is the realistic did:jwk with exactly one {WORD} inserted, nothing else`, () => {{
      const row = SHAPE_REFUSALS.find(([label]) => label.includes('{WORD}'));
      expect(row?.[1].replace('{CHAR}', '')).toBe(REALISTIC_DID_JWK);
      expect(row?.[1].split('{CHAR}')).toHaveLength(2);
    }});
'''
FROM = "export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged"
TO = FROM.replace('[A-Za-z0-9._:%-]', '[A-Za-z0-9._:%' + CHAR + '-]')
assert TO != FROM
T = dict(dir=f'ks_1830_p1_{DIRN}',
 ticket='KS-1830',
 title=f"anchoring did:jwk shape pins: adding `{CHAR}` to the DID_PATTERN character class still passes all 135 cells of ks1175-identity-anchoring (gate 18 finding 1812-2, mutant {ID}): add one refusal row for a payload containing `{CHAR}` (RUNG 3, TEST-ONLY: two in-place test hunks with a planted tamper; the product does not change)",
 intro=f"DRAFT by Spark operator 12 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 18 finding 1812-2 (info), filed as KS-1830: adding `+`, `/` or both to the class of `DID_PATTERN` leaves `ks1175-identity-anchoring.test.ts` at 135 of 135 (measured again by operator 12 at develop d7ddfa1f6433: E1 `+` 135/135, E2 `/` 135/135). This brief is the `{CHAR}` half; the other character is its own brief (one tamper per brief), both add one row at the same place in `SHAPE_REFUSALS`, so a raise seat combines them. Link the PR as Refs KS-1830 and KS-1175, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=124, tamper_from=FROM, tamper_to=TO,
 statement_ok=f"line 124 is the whole `export const DID_PATTERN = /.../;` statement with a trailing comment; the tamper adds `{CHAR}` to the character class and touches nothing else, which is KS-1830's mutant {ID} verbatim; the file still compiles",
 edit=[(ROW_ANCHOR, ROW_ANCHOR + ROW), (CTL_ANCHOR, CTL_ANCHOR + CTL)],
 nh_txt='2 hunks: one new row in `SHAPE_REFUSALS`, and one new control cell in the per-field loop',
 nh_word='TWO hunks (the new row, then the new control cell), in file order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 red=[f'RED KS-1805-1 actorDid: refuses a {WORD} inside the payload', f'RED KS-1805-1 orgDid: refuses a {WORD} inside the payload'],
 runner='vitest` (`npx vitest run src/__tests__/ks1175-identity-anchoring.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden the new cell; two hunks given byte-exact)',
 what_wrong=f"`anchorSchema.ts:124` is `DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/`. Its class holds the base64url alphabet plus `.` `:` `%`; `+` and `/` (the two non-url-safe characters of standard base64) are outside it. No cell of `ks1175-identity-anchoring.test.ts` uses a payload containing `{CHAR}`, so a class widened by `{CHAR}` passes 135 of 135 (the `\\s` widening IS caught, 8 cells red, because a space row exists). The product is right today; the gap is a missing pin. The runtime private-key guard also refuses a `{CHAR}` payload (it needs unpadded base64url), but with a different issue code: the pattern refuses it as `invalid_string`, the guard as `custom`. Each `SHAPE_REFUSALS` cell asserts the field's issues are EXACTLY `['invalid_string']`, so under the widened class the `{CHAR}` payload gets `['custom']` and the cell goes red by assertion. Add one row to `SHAPE_REFUSALS` whose payload is the realistic did:jwk with one `{CHAR}` inserted at offset 40 of the DID (the same offset the space row uses), and one control cell.",
 where="- `src/anchorSchema.ts:124` - (correct, STAYS) the `DID_PATTERN` line; the tamper corrupts it in the checker's clone.\n- Test file, hunk 1: `SHAPE_REFUSALS` is declared at :234 and its last row, `['a space inside the payload', ...]`, is :241 (closing `  ];` at :242). **The new row goes between :241 and :242.**\n- Test file, hunk 2: inside `for (const field of DID_JWK_FIELDS) {` of the same describe, the last `it` is `control KS-1805-1 ${field}: still accepts a did:key and the realistic did:jwk, kept verbatim` (:253-256, its closing `    });` is :256). **The new control goes between :256 and the loop's closing `  }` at :257.** `REALISTIC_DID_JWK`, `issuesFor`, `parseField`, `SHAPE_REFUSALS` and `DID_JWK_FIELDS` are all in scope.",
 cells=f"- RED under the tamper: `RED KS-1805-1 actorDid: refuses a {WORD} inside the payload (KS-1830: ...)` and the same cell for `orgDid` fail by assertion (the widened class lets the payload past the pattern, the guard then reports one `custom` issue, expected `['invalid_string']`).\n- GREEN at the untouched tip: both of those cells (the pattern refuses `{CHAR}`, exactly one `invalid_string` issue) and both control cells.\n- CONTROL `control KS-1830 <field>`: green on BOTH trees; it proves the row is the realistic did:jwk plus exactly one `{CHAR}` (so the red cell is red because of that character, not because the input was built wrong).\n- Every existing cell stays green on both trees except those the tamper itself reddens in the file (the `{CHAR}` rows only; the checker's A4 counts them).",
 unmeasured="- The drafter did NOT run vitest through the round machinery: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden. By hand the drafter measured only that the UNTOUCHED tip is 135 of 135 and that mutants E1 and E2 survive it.\n- The other character is the sibling brief. Mutant E3 (both characters) contains this brief's character, so this row also reddens E3; only the sibling row proves the other half independently.\n- Whether the `custom` issue is what the widened class yields is the drafter's reading of `didJwkRefusal` (BASE64URL_PAYLOAD refuses the `{CHAR}`); the checker's A4 is the measurement.\n- Open PRs touching either file: see the overlap count in the operator report (checked against every open PR on 2026-10-30).".replace('{CHAR}', CHAR),
 scope="**Closes finding 1812-2 (KS-1830), the `" + CHAR + "` half only.** Link the PR as Refs KS-1830 / KS-1175. No product file changes. Not in scope: KS-1813 (the published pattern vs the runtime), the Schemathesis hook.",
)
