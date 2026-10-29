# KS-1815-1 (gate 20 finding 1815-1, Spark operator 14, 2026-10-30): B6's comment stripper misses a trailing // comment (mutant X16c). test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/anchoring/src/index.ts'
TEST = 'Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts'
A1 = "const GET_BY_ID = FROM < 0 ? '' : SRC.slice(FROM, SRC.indexOf(END_LINE, FROM) + END_LINE.length);\n"
H1 = '''// KS-1815-1 (gate 20 mutant X16c): the comment stripper behind B6 (B7 keeps its own whole-line read). It removes `/* */` blocks, then a whole-line OR trailing `//` comment on every line (a `//` at the start of a line or after whitespace).
// The handler slice holds `//` only in comment lines (no URL), so no live code is cut.
const liveCode = (src: string): string => src.replace(/\\/\\*[\\s\\S]*?\\*\\//g, '').split('\\n').map((line) => line.replace(/(^|\\s)\\/\\/.*$/, '')).join('\\n');
'''
OLD_LIVE = "    const live = GET_BY_ID.replace(/\\/\\*[\\s\\S]*?\\*\\//g, '').split('\\n').filter((line) => !line.trim().startsWith('//')).join('\\n');\n"
B6 = "  it('RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out', () => {\n"
B7 = "  it('control KS-1827 B7: the comment-stripping read still sees the live identity spread beside it and drops the KS-1454 comment line', () => {\n"
NEW_LIVE = "    const live = liveCode(GET_BY_ID);\n"
B6TAIL = "    expect(live.includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')).toBe(true);\n  });\n"
B8 = '''  // KS-1815-1 (gate 20 mutant X16c): B6 used to strip only `/* */` blocks and whole-line `//` comments, so a live line that kept the spread text in a TRAILING `//` comment passed it.
  it('control KS-1815-1 B8: liveCode drops a trailing // comment (the spread text left only in one is not live), keeps the code before it, and still drops whole-line and block comments', () => {
    const trailing = '    ...{}, // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),';
    expect(liveCode(trailing).includes('anchorSignatureHashView')).toBe(false);
    expect(liveCode(trailing).includes('...{},')).toBe(true);
    expect(liveCode('a // b\\n// c\\n/* d */ e').split('\\n').map((line) => line.trim())).toEqual(['a', '', 'e']);
  });

'''
FROM = "    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),"
TO = "    ...{}, // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),"
T = dict(dir='ks_1815_p3_trailing_comment',
 ticket='KS-1827',
 title="anchoring KS-1454 read-back test: B6's comment stripper handles `/* */` and whole-line `//` only, so a live line that keeps the spread in a trailing `//` comment still passes (gate 20 finding 1815-1, mutant X16c): strip trailing comments too and add a control (RUNG 3, TEST-ONLY: two in-place test hunks with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 14 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 20 (`0_Brain/reference/2026-10-30_gate20-1815-1816/verdict.md`), minor 1815-1, a follow-up to KS-1827 / PR #1815. Mutant X16c keeps the live line different but leaves the spread text in a trailing comment: `...{}, // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),`. B5 matches the text and B6 does not strip a trailing comment, so the file stays green. The gate's own check that the sliced handler region holds no URL on the lines of interest is repeated here: the `:id` handler slice has `//` only on comment lines. Link the PR as Refs KS-1827 and KS-1454, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=964, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 964 is the one-line spread inside the object literal of the `res.json({...})` in the `GET /api/anchors/:id` handler; the tamper replaces the spread with an empty spread and keeps the old text in a trailing `//` comment on the same line, so the object stays valid and the file compiles; it is mutant X16c verbatim",
 edit=[(A1, A1 + H1),
       (B6 + OLD_LIVE + B6TAIL, B6 + NEW_LIVE + B6TAIL + "\n" + B8.rstrip('\n') + "\n")],
 nh_txt='2 hunks: a `liveCode` helper after the `GET_BY_ID` constant; then B6 uses it and one new control cell B8 follows B6',
 nh_word='TWO hunks (the helper, then B6 + the new cell B8 after it), in file order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 red=['RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out'],
 runner='vitest` (`npx vitest run src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden an existing cell, B6, that this diff hardens; two hunks given byte-exact)',
 what_wrong="B6 (`RED KS-1827 B6`) and the control B7 each build the live handler text with the same inline expression: remove `/* */` blocks, then drop lines whose trimmed text starts with `//`. A trailing comment (code, then `// text`) survives, so mutant X16c (`...{}, // ...anchorSignatureHashView(...)`, the spread text only in a trailing comment) leaves B5 green (it matches text) and B6 green (the text is still there after stripping): 11 of 11. The product is right today; the gap is a weak instrument. Fix: one helper `liveCode` that removes `/* */` blocks and then, on every line, a `//` comment from a `//` at the start of the line or after whitespace to the end of the line; B6 calls it (B7 keeps its own inline read, unchanged: the brief builder refuses a hunk with a blank context line, and B6 and B7 are separated by one); one new control B8 feeds it a synthetic trailing-comment line. B6 then goes red under the X16c tamper while it stays green at the tip.",
 where="- `src/index.ts:964` - (correct, STAYS) the by-id spread line; the tamper corrupts it in the checker's clone. It lies inside the `GET_BY_ID` slice the test cuts (from `app.get('/api/anchors/:id',` to `retryCount: anchor.retryCount ?? 0,`), whose `//` occurrences are all on comment lines.\n- Test file, hunk 1: line 31 is the `const GET_BY_ID = ...` statement. **The helper (a two-line comment and one `const liveCode`) goes right after :31, before the blank line and `describe`.**\n- Test file, hunk 2: B6 is :63-66. **The line `    const live = GET_BY_ID.replace(...).join('\\n');` in B6 (:64) is replaced by `    const live = liveCode(GET_BY_ID);`, and the new cell B8 (with its comment, after one blank line) goes right after B6's closing `  });` (:66), before the blank line and `control KS-1827 B7` (:68).** B7 is not edited.",
 cells="- RED under the tamper: `RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out` fails by assertion (the live text no longer holds the spread, once the trailing comment is stripped). B5 stays green under this tamper (it matches the text, which is still in the file), so B6 is the only red.\n- GREEN at the untouched tip: B6, B7, B8 and every other cell of the file.\n- CONTROL `control KS-1815-1 B8`: green on BOTH trees; it feeds `liveCode` a synthetic trailing-comment line and a whole-line / block mix and proves the helper does what B6 relies on, independent of the product.\n- B7 is not edited and stays green under the tamper (it reads the identity spread and the KS-1454 comment, which the tamper does not touch).",
 unmeasured="- The drafter did NOT run vitest through the round machinery: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- A spread kept live but unreachable (after a `return`) is still invisible to B6, as the PR #1815 doc 113.3 states; not addressed here.\n- A string literal containing ` //` inside the sliced handler would be cut by the new helper; the drafter read the slice and found none (`//` occurs only on comment lines), and B6/B7 would go red, not silently green, if one appeared on a line they match.\n- B7 still uses its own inline whole-line stripper (not edited, see above); switching it to `liveCode` is a one-line follow-up.\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**Closes finding 1815-1 (minor), test half.** Link the PR as Refs KS-1827 / KS-1454. No product file changes. Not in scope: unreachable-but-live code, any other cell of the file.",
)
