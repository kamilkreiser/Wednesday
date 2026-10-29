# KS-1733 item 2 (gate on PR #1696, Minor 2): no cell pins upper case on the proposals list filters. Spark operator 15. test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/governance/src/types/governance.types.ts'
TEST = 'Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts'
OLD = "  it('R7 one bad filter refuses the request even beside good ones -> 400', async () => {\n    expectRefused(await list('?status=active&proposerId='));\n  });\n});\n"
CELLS = '''
  // KS-1733 item 2 (gate on #1696, Minor 2): no cell pinned upper case, so a case-insensitive status check stayed green on all 43 cells above. The policy pinned here is the one at the tip: lower case only.
  it.each([
    ['an upper-case status', '?status=ACTIVE'],
    ['a capitalised status', '?status=Active'],
    ['one capitalised part in a list', '?status=active%2CQueued'],
  ])('RED KS-1733 R8 %s -> 400, never reaches SQL', async (_label, q) => {
    expectRefused(await list(q));
  });

  it.each([
    ['an upper-case category', '?category=GENERAL'],
    ['a capitalised category', '?category=General'],
  ])('control KS-1733 R9 %s -> 400 (the category enum is exact-case)', async (_label, q) => {
    expectRefused(await list(q));
  });
'''
NEW = OLD[:-len("});\n")] + CELLS + "});\n"
FROM = "export const PROPOSAL_STATUS_LIST_PATTERN = new RegExp(`^(?:${STATUS_ALTERNATION})(?:,(?:${STATUS_ALTERNATION}))*$`);"
TO = "export const PROPOSAL_STATUS_LIST_PATTERN = new RegExp(`^(?:${STATUS_ALTERNATION})(?:,(?:${STATUS_ALTERNATION}))*$`, 'i');"
T = dict(dir='ks_1733_p1_status_case',
 ticket='KS-1733',
 title="governance ks1722 proposals-list cells: nothing pins that an upper-case or capitalised `?status=` is refused, so a case-insensitive status pattern stays green on all 43 cells (KS-1733 item 2, gate Minor 2 on #1696): add one `it.each` of three refusals and a two-row category control (RUNG 3, TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 15 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / governance) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1733 item 2 (QA gate on PR #1696, Minor 2; the ticket's fix shape: `pin the intended policy (lower case only, as today) with a cell: ?status=ACTIVE -> 400, and ?category=GENERAL -> 400`). ONLY item 2 of the ticket's four is in this brief; items 1, 3 and 4 change behaviour (strict unknown keys, control characters, a length limit) and are not test pins. The product is right today for the policy as written (`PROPOSAL_STATUS_LIST_PATTERN` has no `i` flag and the category is an exact-case `z.enum`). Wednesday decides whether lower case only is the policy she wants pinned: the cells fail if anyone later chooses case-insensitive on purpose. Link the PR as Refs KS-1733, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/governance/src/__tests__/ks594-business-refusals-are-not-500.test.ts',
 tamper_line=353, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 353 is a single complete `export const ... = new RegExp(...);` statement; the tamper adds the `'i'` flag as a second argument and nothing else, so the file compiles and the pattern accepts every case; the `status` rule at :368-371 uses this pattern and the published schema (governance.openapi.ts) reads the same export, so the runtime and the spec move together",
 edit=(OLD, NEW),
 nh_txt='1 hunk, three new `it.each` rows plus a two-row control added at the end of the `category and status` describe',
 red=['RED KS-1733 R8'],
 runner='jest` (`npx jest src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts` from `Blockchain/Dev/services/governance',
 rung='3 (test-only mode: a planted tamper must redden the new rows; the hunk is given byte-exact)',
 what_wrong="`ProposalListQuerySchema.status` (`types/governance.types.ts:368-371`) validates a comma list against `PROPOSAL_STATUS_LIST_PATTERN` (`:353`), a RegExp with no `i` flag, and `category` is a `z.enum` (exact-case). The KS-1722 test file has 43 cells but none sends an upper-case or capitalised value, so a change that makes the status pattern case-insensitive (`new RegExp(..., 'i')`) stays green on all of them, including S2 (published vs runtime agreement over a corpus with no upper-case value). The product is right today; the gap is a missing pin. Add one `it.each` of three refusals (`?status=ACTIVE`, `?status=Active`, `?status=active%2CQueued`), each expected to answer the router's BAD_REQUEST envelope through the file's own `expectRefused` (which also asserts that no query ran), and a two-row control for `?category=GENERAL` / `?category=General`.",
 where="- `src/types/governance.types.ts:353` - (correct, STAYS) `PROPOSAL_STATUS_LIST_PATTERN = new RegExp(...)`; the line the tamper replaces in the checker's clone (it appends `'i'`).\n- Test file: cell R7 is :254-256 (its closing `  });` is :256) and `});` at :257 closes the `category and status` describe. **The new block goes between :256 and :257**, after one blank line. `list` and `expectRefused` are in scope at module level.",
 cells="- RED under the tamper: the three `RED KS-1733 R8 ...` rows fail by assertion (the case-insensitive pattern accepts them, the route answers 200 and runs a select, so `expectRefused` fails on the status).\n- GREEN at the untouched tip: all five new rows and every existing cell.\n- CONTROL `control KS-1733 R9` (category rows): green on both trees; the category is an exact-case `z.enum`, which the status tamper does not touch.\n- Existing cells: the tamper makes no existing cell fail (every existing status value is lower case).",
 unmeasured="- The drafter did NOT run jest through the round machinery: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- Whether the router lower-cases anything before the schema (it does not at the tip by the source read: `status` goes straight into the regex).\n- The category rows are not red under the planted tamper; they pin the enum's exact-case behaviour only as controls (a `z.enum` made case-insensitive would be a different tamper).\n- Policy: whether lower case only is the policy Wednesday wants pinned (the ticket says `as today`).\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**KS-1733 item 2 only (gate Minor 2).** Link the PR as Refs KS-1733, never a close-word. No product file changes. Not in scope: unknown-key refusal, control characters, a proposerId length limit, the parameter cap.",
)
