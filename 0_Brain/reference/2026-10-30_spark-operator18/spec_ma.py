import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common18 import *
TEST = TDIR + 'ks1836-log-foreign-selector-with-no-rows.test.ts'
HEAD = '''// KS-1836 (gate 23 finding F1): GET /api/nft/certificates writes one warning, 'NFT certificate list narrowed to the caller', when
// `withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)`. The first disjunct (a row was withheld) is pinned
// by the PR's own R17. The SECOND disjunct only matters when the caller's fetched set is EMPTY and ?userId names someone else: nothing
// is withheld then, so only the foreign-selector arm can log it. No cell exercised that, so dropping the arm stayed green.
// The router runs on a small express app over an ephemeral port with a test-only req.user middleware; the REAL minting service
// runs on a fake table, and the logger is spied. Harness copied from ks1836-nft-list-owner-bound.test.ts.
'''
CELLS = '''
describe('KS-1836 log contract: the foreign-selector arm of the narrowed-list warning', () => {
  it('RED KS-1836 L1 a caller with no rows who names someone else in ?userId gets the empty 200 and exactly one narrowed-list warning naming the selector', async () => {
    const r = await get('/api/nft/certificates?userId=user-B', CALLER_Z);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    const logs = narrowedLogs();
    expect(logs).toHaveLength(1);
    expect(logs[0].meta).toMatchObject({ ownerId: 'user-Z', userIdSelector: 'user-B', returned: 0, withheld: 0 });
    const serialised = JSON.stringify(logCalls);
    expect(serialised.includes(B_KEY)).toBe(false);
    expect(serialised.includes('encryptedKey')).toBe(false);
  });

  it('CONTROL KS-1836 L2 a caller with no rows and no selector logs no narrowed-list warning', async () => {
    const r = await get('/api/nft/certificates', CALLER_Z);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    expect(narrowedLogs()).toHaveLength(0);
  });

  it('CONTROL KS-1836 L3 a caller with no rows whose ?userId names itself logs no narrowed-list warning', async () => {
    const r = await get('/api/nft/certificates?userId=user-Z', CALLER_Z);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    expect(narrowedLogs()).toHaveLength(0);
  });

  it('CONTROL KS-1836 L4 a caller with rows who names someone else in ?userId gets the empty 200 and one warning that counts the withheld rows', async () => {
    const r = await get('/api/nft/certificates?userId=user-B', CALLER_A);
    expect(r.status).toBe(200);
    expect(r.text).toBe(EMPTY_BODY);
    const logs = narrowedLogs();
    expect(logs).toHaveLength(1);
    expect(logs[0].meta).toMatchObject({ ownerId: 'user-A', userIdSelector: 'user-B', returned: 0, withheld: 2 });
  });
});
'''
T = dict(dir='ks_1836_p1_log_foreign_selector_no_rows', ticket='KS-1836', test=TEST, product=ROUTE, ref=REF, runner=RUNNER,
 content=HEAD + HARNESS + CELLS, ncells='4 cells',
 title="nft-certificate GET /certificates: pin the foreign-selector arm of the narrowed-list warning when the caller's fetched set is empty (gate 23 F1, mutant Ma; RUNG 3, TEST-ONLY: one NEW vitest file with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 18 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / nft-certificate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: " + GATE_NOTE + " The product is right at the tip; the gap is a missing pin. Surface: a read route's log line only (no response bytes depend on it). The new file is in the nft-certificate `__tests__` partition and adds a file; it edits neither of the two test files PR 1819 added.",
 scope="**Refs KS-1836, never a close-word.** Pins half of the brief A.3 log contract of PR 1819: the foreign-selector log fires when the fetched set is empty and `?userId` names someone else. The other half (the log does NOT fire on an ordinary own-rows call, mutant Mb) is the sibling brief `ks_1836_p2_log_silent_on_own_rows`. Out of scope and not done: F2 (row-owner trim asymmetry between the two read paths) and F3, F4: decisions, not pins. No product line changes; one new test file, no existing file edited.",
 wrong="`GET /certificates` in `nft.routes.ts` logs `'NFT certificate list narrowed to the caller'` when `withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)`. PR 1819's R17 reaches the log only through `withheld > 0` (a foreign wallet, one row withheld). When the caller's fetched set is empty (a caller with no rows, here user-Z) and `?userId=user-B` names someone else, `withheld` is 0, so ONLY the second disjunct can write the warning. Gate 23 mutant Ma (drop that disjunct) survived the author's 31 cells and the gate's own 55. Add the cell that fires the arm: caller user-Z, `?userId=user-B`, expect the empty 200 and exactly one warning carrying `{ ownerId: 'user-Z', userIdSelector: 'user-B', returned: 0, withheld: 0 }`. Three controls bracket it: no selector and own-id selector on an empty set log nothing; a foreign selector from a caller WITH rows logs once with `withheld: 2`.",
 where="- `routes/nft.routes.ts:244` - (correct, STAYS) `if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {`; the line the tamper replaces in the checker's clone. The warn call is :245-247.\n- Harness copied from `__tests__/ks1836-nft-list-owner-bound.test.ts:11-131` (fake table, real minting service, spied logger, `x-ks1836-user` header middleware), minus the OpenAPI import and the spies on the two service readers, which these cells do not use. FIXTURE here is a1, a2 (user-A) and b1 (user-B); user-Z owns nothing.",
 tamper_line=244, tamper_from="    if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {",
 tamper_to="    if (withheld > 0) {",
 statement_ok="line 244 is the one-line `if` header (its block is :245-247); the replacement keeps `withheld > 0` and drops the second disjunct (gate mutant Ma); `userIdSelector` stays used in the log call, so `noUnusedLocals` is not tripped and the file compiles; the withheld-row log (R17) and every response byte are unchanged",
 red=['RED KS-1836 L1 a caller with no rows who names someone else in ?userId gets the empty 200 and exactly one narrowed-list warning naming the selector'],
 cells="- RED under the tamper: L1 fails by assertion (`narrowedLogs()` has length 0 instead of 1).\n- GREEN at the untouched tip: all four cells.\n- Controls L2, L3, L4 stay green under this tamper (L2 and L3 expect NO log and the tamper only removes a log; L4 logs through `withheld > 0`).",
 unmeasured="- The drafter did NOT run vitest for the brief; RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- Mutant Mb (every call logs) is not this tamper; the sibling brief covers it.\n- The `__tests__` fake-table SQL strings were copied from the sibling file at the tip; a change to the minting service's four SQL shapes would break both files the same way.\n- Open PRs touching nft-certificate: only 1360 and 649 (both `package*.json`), read 2026-10-30; none touches a `__tests__` path.",
)
