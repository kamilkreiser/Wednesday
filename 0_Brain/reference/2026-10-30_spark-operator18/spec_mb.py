import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common18 import *
TEST = TDIR + 'ks1836-log-silent-on-an-ordinary-own-rows-call.test.ts'
HEAD = '''// KS-1836 (gate 23 finding F1, second half): GET /api/nft/certificates must write the 'NFT certificate list narrowed to the caller'
// warning ONLY when a row was withheld or a foreign ?userId was named. An ordinary call (the caller's own rows, an own-id selector, an
// empty set with no selector) must stay silent: the line is a signal, and a handler that logs on every call buries it. The PR's own
// cells assert the log when it should fire (R17) but never that it stays quiet, so changing `withheld > 0` to `withheld >= 0`
// stayed green.
// The router runs on a small express app over an ephemeral port with a test-only req.user middleware; the REAL minting service
// runs on a fake table, and the logger is spied. Harness copied from ks1836-nft-list-owner-bound.test.ts.
'''
CELLS = '''
describe('KS-1836 log contract: an ordinary call writes no narrowed-list warning', () => {
  it('RED KS-1836 Q1 a bare list for a caller with rows returns the own rows and logs no narrowed-list warning', async () => {
    const r = await get('/api/nft/certificates', CALLER_A);
    expect(r.status).toBe(200);
    expect(ids(r)).toEqual(['a2', 'a1']);
    expect(narrowedLogs()).toHaveLength(0);
  });

  it('RED KS-1836 Q2 a ?userId naming the caller itself returns the own rows and logs no narrowed-list warning', async () => {
    const r = await get('/api/nft/certificates?userId=user-A', CALLER_A);
    expect(r.status).toBe(200);
    expect(ids(r)).toEqual(['a2', 'a1']);
    expect(narrowedLogs()).toHaveLength(0);
  });

  it('RED KS-1836 Q3 a caller with no rows and no selector gets the empty 200 and logs no narrowed-list warning', async () => {
    const r = await get('/api/nft/certificates', CALLER_Z);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    expect(narrowedLogs()).toHaveLength(0);
  });

  it('CONTROL KS-1836 Q4 a foreign wallet selector still logs exactly one warning that counts the withheld row', async () => {
    const r = await get(`/api/nft/certificates?walletAddress=${W_B}`, CALLER_A);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    const logs = narrowedLogs();
    expect(logs).toHaveLength(1);
    expect(logs[0].meta).toMatchObject({ ownerId: 'user-A', walletAddress: W_B, returned: 0, withheld: 1 });
  });
});
'''
T = dict(dir='ks_1836_p2_log_silent_on_own_rows', ticket='KS-1836', test=TEST, product=ROUTE, ref=REF, runner=RUNNER,
 content=HEAD + HARNESS + CELLS, ncells='4 cells',
 title="nft-certificate GET /certificates: pin that an ordinary own-rows call writes no narrowed-list warning (gate 23 F1, mutant Mb; RUNG 3, TEST-ONLY: one NEW vitest file with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 18 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / nft-certificate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: " + GATE_NOTE + " The product is right at the tip; the gap is a missing pin. Surface: a read route's log line only (no response bytes depend on it). The new file is in the nft-certificate `__tests__` partition and adds a file; it edits neither of the two test files PR 1819 added.",
 scope="**Refs KS-1836, never a close-word.** Pins the other half of the brief A.3 log contract of PR 1819: the narrowed-list warning does NOT fire on an ordinary own-rows call. The first half (it fires for a foreign `?userId` when the fetched set is empty, mutant Ma) is the sibling brief `ks_1836_p1_log_foreign_selector_no_rows`. Out of scope and not done: F2, F3, F4 (decisions, not pins). No product line changes; one new test file, no existing file edited.",
 wrong="`GET /certificates` in `nft.routes.ts` logs `'NFT certificate list narrowed to the caller'` when `withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)`. PR 1819's cells assert the log when it must fire (R17) but none asserts it stays silent, so gate 23 mutant Mb (`withheld > 0` changed to `withheld >= 0`, so every call logs) survived 31 author cells and 55 gate cells. Add cells for the ordinary calls that must not log: a bare list for a caller with rows, a `?userId` naming the caller itself, and an empty set with no selector. One control keeps the firing case honest (a foreign wallet selector logs once with `withheld: 1`).",
 where="- `routes/nft.routes.ts:244` - (correct, STAYS) `if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {`; the line the tamper replaces in the checker's clone. The warn call is :245-247.\n- Harness copied from `__tests__/ks1836-nft-list-owner-bound.test.ts:11-131` (fake table, real minting service, spied logger, `x-ks1836-user` header middleware), minus the OpenAPI import and the spies on the two service readers. FIXTURE here is a1, a2 (user-A) and b1 (user-B); user-Z owns nothing.",
 tamper_line=244, tamper_from="    if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {",
 tamper_to="    if (withheld >= 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {",
 statement_ok="line 244 is the one-line `if` header (its block is :245-247); the replacement changes `>` to `>=` (gate mutant Mb), so the condition is always true; the file compiles and no response byte changes, only the number of warnings",
 red=['RED KS-1836 Q1 a bare list for a caller with rows returns the own rows and logs no narrowed-list warning',
      'RED KS-1836 Q2 a ?userId naming the caller itself returns the own rows and logs no narrowed-list warning',
      'RED KS-1836 Q3 a caller with no rows and no selector gets the empty 200 and logs no narrowed-list warning'],
 cells="- RED under the tamper: Q1, Q2 and Q3 fail by assertion (one warning logged where none is expected).\n- GREEN at the untouched tip: all four cells.\n- Control Q4 stays green under the tamper (a foreign wallet logs exactly once either way).",
 unmeasured="- The drafter did NOT run vitest for the brief; RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- Mutant Ma (the foreign-selector arm dropped) is not this tamper; the sibling brief covers it.\n- Open PRs touching nft-certificate: only 1360 and 649 (both `package*.json`), read 2026-10-30; none touches a `__tests__` path.",
)
