# KS-1830 follow-up (gate 21 finding 1817-2, Spark operator 14, 2026-10-30): DID_PATTERN class widened by ! * @ # , the A-z range, or a trailing \+? survives all 143 cells. test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TEST = 'Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts'
ROW_ANCHOR = "    ['a slash inside the payload (KS-1830: standard base64, not base64url)', REALISTIC_DID_JWK.slice(0, 40) + '/' + REALISTIC_DID_JWK.slice(40)],\n"
EXTRA = [('an exclamation mark', '!'), ('an asterisk', '*'), ('an at sign', '@'), ('a hash sign', '#'), ('a caret', '^')]
ROWS = ''.join(f"    ['{w} inside the payload (1817-2)', REALISTIC_DID_JWK.slice(0, 40) + '{c}' + REALISTIC_DID_JWK.slice(40)],\n" for w, c in EXTRA)
ROWS += "    ['a plus sign at the END of the payload (1817-2)', REALISTIC_DID_JWK + '+'],\n"
CTL_ANCHOR = "      expect(row?.[1].split('/')).toHaveLength(2);\n    });\n"
CTL = '''    it(`control 1817-2 ${field}: each added row is the realistic did:jwk with exactly one extra character, nothing else (the END row appends one plus sign)`, () => {
      for (const [word, ch] of [['exclamation mark', '!'], ['asterisk', '*'], ['at sign', '@'], ['hash sign', '#'], ['caret', '^']]) {
        const row = SHAPE_REFUSALS.find(([label]) => label.includes(word + ' inside the payload (1817-2)'));
        expect(row?.[1].replace(ch, '')).toBe(REALISTIC_DID_JWK);
        expect(row?.[1].split(ch)).toHaveLength(2);
      }
      const end = SHAPE_REFUSALS.find(([label]) => label.includes('plus sign at the END of the payload (1817-2)'));
      expect(end?.[1]).toBe(REALISTIC_DID_JWK + '+');
    });
'''
FROM = "export const DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/; // KS-1175 / PS-1324: + jwk (was key|web); cap unchanged"
TO = FROM.replace('[A-Za-z0-9._:%-]+$', '[A-z0-9._:%!*@#-]+\\+?$')
assert TO != FROM
WORDS = ['an exclamation mark', 'an asterisk', 'an at sign', 'a hash sign', 'a caret', 'a plus sign at the END']
red = []
for f in ('actorDid', 'orgDid'):
    for w in WORDS:
        red.append(f'RED KS-1805-1 {f}: refuses {w} ' + ('of the payload (1817-2)' if 'END' in w else 'inside the payload (1817-2)'))
T = dict(dir='ks_1830_p2_charclass_sweep',
 ticket='KS-1830',
 title="anchoring did:jwk shape pins: widening the DID_PATTERN class by `!` `*` `@` `#`, the `A-z` range, or a trailing `\\+?` still passes all 143 cells of ks1175-identity-anchoring (gate 21 finding 1817-2): add six refusal rows and one control (RUNG 3, TEST-ONLY: two in-place test hunks with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 14 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 21 (`0_Brain/reference/2026-10-30_gate21-1817/verdict.md`), info finding 1817-2, a follow-up to KS-1830 / PR #1817 (which pinned `+` and `/` at offset 40): the gate measured these widenings of `DID_PATTERN` as SURVIVORS at 143 of 143: `!`, `*`, `@`, `#`, the `A-z` range (adds `[ \\ ] ^` and the backtick), and a trailing optional `\\+?` at the END of the payload. This brief adds one refusal row per class and one control. The test_only tier plants ONE tamper, so the tamper combines them all in one line (the red cells name each row); the independent single-mutant results are in the operator report. Link the PR as Refs KS-1830 and KS-1175, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=124, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 124 is the whole `export const DID_PATTERN = /.../;` statement with a trailing comment; the tamper replaces `A-Za-z` by `A-z`, adds `!` `*` `@` `#` to the character class and `\\+?` before the `$`, and touches nothing else; the file still compiles",
 edit=[(ROW_ANCHOR, ROW_ANCHOR + ROWS), (CTL_ANCHOR, CTL_ANCHOR + CTL)],
 nh_txt='2 hunks: six new rows in `SHAPE_REFUSALS`, and one new control cell in the per-field loop',
 nh_word='TWO hunks (the six new rows, then the new control cell), in file order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 red=red,
 runner='vitest` (`npx vitest run src/__tests__/ks1175-identity-anchoring.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden the new cells; two hunks given byte-exact)',
 what_wrong="`anchorSchema.ts:124` is `DID_PATTERN = /^did:(key|web|jwk):[A-Za-z0-9._:%-]+$/`. No cell of `ks1175-identity-anchoring.test.ts` uses a payload containing `!`, `*`, `@`, `#` or `^` (the `A-z` range reaches `[ \\ ] ^` and the backtick), or ending in `+`, so a class widened by any of them, or a trailing `\\+?`, passes 143 of 143 (gate 21 measured each as a survivor). The product is right today; the gap is a missing pin. Each `SHAPE_REFUSALS` cell asserts the field's issues are EXACTLY `['invalid_string']`: under a widened pattern the value gets past the pattern, so the issues are a `custom` one (the private-key guard needs unpadded base64url) or none, and the cell goes red by assertion. Add five rows (the realistic did:jwk with one of `!` `*` `@` `#` `^` inserted at offset 40 of the DID, the same offset the space row uses), one row with a `+` appended at the END (the existing plus row inserts at offset 40 only), and one control cell.",
 where="- `src/anchorSchema.ts:124` - (correct, STAYS) the `DID_PATTERN` line; the tamper corrupts it in the checker's clone.\n- Test file, hunk 1: in `SHAPE_REFUSALS` the last row is `['a slash inside the payload (KS-1830: ...)', ...]` (:243), the closing `  ];` is :244. **The six new rows go between :243 and :244.**\n- Test file, hunk 2: inside `for (const field of DID_JWK_FIELDS) {` the last `it` is `control KS-1830 ${field}: the slash row is ...` (its closing `    });` is :268 and the loop's closing `  }` is :269). **The new control goes between :268 and :269.** `REALISTIC_DID_JWK`, `SHAPE_REFUSALS` and `DID_JWK_FIELDS` are in scope. The existing controls find their row by `label.includes('plus sign')` / `includes('slash')`; the first match is still the offset-40 row, because the new rows come after it.",
 cells="- RED under the tamper: for each of `actorDid` and `orgDid`, the six new `RED KS-1805-1 <field>: refuses ...(1817-2) with exactly one invalid_string issue on the field` cells fail by assertion (the widened pattern lets the value through, the issues are not exactly `['invalid_string']`).\n- GREEN at the untouched tip: all twelve of those cells and both control cells.\n- CONTROL `control 1817-2 <field>`: green on BOTH trees; it proves each of the five offset-40 rows is the realistic did:jwk plus exactly one extra character and the END row is the realistic did:jwk plus one `+`, so a red cell is red because of that character.\n- Every existing cell stays green on both trees (the tamper adds characters; the existing refusal rows use none of them).",
 unmeasured="- The drafter did NOT run vitest through the round machinery: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The tamper is the union of the six widenings; which single widening reddens which row is the operator's separate measurement, not the checker's.\n- Whether a character in the `A-z` range other than `^` is also refused is not tested (the row uses `^`).\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**Closes finding 1817-2 (info), the test half.** Link the PR as Refs KS-1830 / KS-1175. No product file changes. Not in scope: a class-wide ASCII sweep over every character, KS-1813 (the published pattern vs the runtime), the Schemathesis hook.",
)
