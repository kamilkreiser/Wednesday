# KS-1827 (gate 18 survivor X16, Spark operator 11, 2026-10-30): the by-id signatureHash spread is pinned by source text only. test_only, gen/mk_testonly.py.
PROD='Blockchain/Dev/services/anchoring/src/index.ts'
TEST='Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts'
LIVE_LINE = "...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),"
ANCHOR = "    expect(GET_BY_ID.includes('" + LIVE_LINE + "')).toBe(true);\n  });\n"
CELL = r'''
  // KS-1827 (gate 18 mutant X16): B5 matches the spread by source TEXT, and a commented-out spread keeps that text in the file, so the mutant passed 23 of 23 while the route stopped returning the hash.
  // B6 reads the handler slice with its comments removed (whole `//` lines and `/* */` blocks), so only live code can satisfy the match.
  it('RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out', () => {
    const live = GET_BY_ID.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').filter((line) => !line.trim().startsWith('//')).join('\n');
    expect(live.includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
  });

  it('control KS-1827 B7: the comment-stripping read still sees the live identity spread beside it and drops the KS-1454 comment line', () => {
    const live = GET_BY_ID.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').filter((line) => !line.trim().startsWith('//')).join('\n');
    expect(live.includes('...anchorIdentityView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
    expect(live.includes('KS-1454: the SHA-256 of the detached')).toBe(false);
    expect(GET_BY_ID.includes('KS-1454: the SHA-256 of the detached')).toBe(true);
  });
'''
T=dict(dir='ks_1827_p1_byid_spread_live',ticket='KS-1827',
 title='ks1454 read-back cell B5 matches the by-id signatureHash spread by source text, so a commented-out spread survives 23 of 23 (gate 18 mutant X16): add a comment-stripped live-code cell (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)',
 intro="DRAFT by Spark operator 11 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 18 (`0_Brain/reference/2026-10-30_gate18-1811-1812/verdict.md`), finding 1811-2, filed as KS-1827: mutant X16 (the spread line commented out) leaves both KS-1454 test files 23/23 green, while control X15 (the line removed outright) is killed by cell B5. Link the PR as Refs KS-1827 and KS-1454, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts',
 tamper_line=960, tamper_from="    "+LIVE_LINE, tamper_to="    // "+LIVE_LINE,
 statement_ok="line 960 is one complete object-literal entry (a spread) inside the `res.json({...})` of the `GET /api/anchors/:id` handler; the tamper only prefixes `// `, which is gate 18's mutant X16 verbatim; the entry stays between two other entries, so the file still compiles",
 edit=(ANCHOR, ANCHOR+CELL),
 red=['RED KS-1827 B6'],
 runner='vitest` (`npx vitest run src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` from `Blockchain/Dev/services/anchoring',
 rung='3 (test-only mode: a planted tamper must redden the new cell; the hunk is given byte-exact)',
 what_wrong="Cell B5 of `ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` pins the `GET /api/anchors/:id` signatureHash wiring by SOURCE TEXT: `GET_BY_ID` (line 31) is a slice of `index.ts`, and B5 asserts it `includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')`. A mutant that comments that line out (`    // ...anchorSignatureHashView(...)`) keeps the text in the file, so all 23 cells of the two KS-1454 test files stay green while the route silently stops returning `metadata.signatureHash`, the one field Platform S's 'signature anchored' check reads. The product is right today; the gap is a missing pin. This task adds cell B6, which strips whole-line `//` comments and `/* */` blocks from the handler slice before matching, plus a control B7 proving the stripper works (it drops the neighbouring KS-1454 comment line and keeps the live identity spread).",
 where="- `src/index.ts:960` - (correct, STAYS) `    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),` - the line the tamper corrupts in the checker's clone (preceded by the KS-1454 comment line at :959, followed by KS-535 comments).\n- Test file: cell B5 is lines 56-59 (its closing `  });` is :59); :60 is blank; :61 starts `control KS-1454 C1`. **The new cells go between :59 and :60.** `GET_BY_ID` (line 31) is in scope at module level.",
 cells="- RED under the tamper: `RED KS-1827 B6` fails by assertion (the comment-stripped slice no longer contains the spread; `false` is not `true`). B5 stays green under the tamper (that is the survivor); every other existing cell stays green.\n- GREEN at the untouched tip: B6 and B7 (the spread is live; the stripper drops the `KS-1454: the SHA-256 of the detached` comment line and keeps `...anchorIdentityView(...)`).\n- CONTROL B7: green on BOTH trees (the identity spread is untouched by the tamper, and the comment line is stripped from the live view but present in the raw slice).",
 unmeasured="- The drafter did NOT run vitest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- The route itself is never driven (it needs a database; the KS-1603 recipe returns before the SQL). Like B5, B6 is a source-text guard: it kills a COMMENTED-OUT spread, not a spread whose argument is broken (gate 18's X17, already caught by B5) and not a spread moved outside the `res.json` object.\n- The comment stripper handles whole-line `//` comments and `/* */` blocks; a trailing `// ...` after live code on the same line is deliberately left alone (it would not remove the spread).\n- Open PRs touching either file: see the overlap count in the operator report (checked against every open PR on 2026-10-30).",
 scope="**Closes finding 1811-2 (KS-1827) only.** Link the PR as Refs KS-1827 / KS-1454. No product file changes.",
)
