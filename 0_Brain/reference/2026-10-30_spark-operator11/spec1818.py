# KS-1818 (Spark operator 11, 2026-10-30): wrap logger.error in the per-user catch of POST /seed-demo-users (the fail500 / migrate-tenant-data shape). code_patch rung 2, gen/mk2.py.
P='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts'
E1=("        logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });\n",
    "        // KS-1818: readableErrorMessage guards the message READ; the logger call after it sat directly in this catch, so a logger (or a serialiser) that throws left the catch, ended the loop\n"
    "        // at this user and reached the route's outer catch (the KS-1802 hang class). Log in a try of its own, as fail500 and migrate-tenant-data do; the loop goes on with the next user.\n"
    "        try { logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) }); } catch {\n"
    "          // Nothing more can be said if the logger itself fails; the failure is already counted and the next user is still attempted.\n"
    "        }\n")
ANCHOR="    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });\n  });\n"
CELLS=r'''
  // KS-1818: R1-R3 make the thrown VALUE hostile; these two make the LOGGER throw. The logger call after readableErrorMessage sat outside any guard.
  it('RED KS-1818 R4: a logger that throws on every failed insert is reported as 14 failed, not as the constant 500', async () => {
    mockLogError.mockImplementation(() => {
      throw new Error('ks1818 logger down');
    });
    mockExecuteRaw.mockRejectedValue(new Error('ks1818 insert'));
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
    expect(mockLogError).toHaveBeenCalledTimes(USERS);
  });

  it('RED KS-1818 R5: one failed insert whose log line throws does not stop the other 13 from being seeded', async () => {
    mockLogError.mockImplementation(() => {
      throw new Error('ks1818 logger down');
    });
    mockExecuteRaw.mockRejectedValueOnce(new Error('ks1818 insert')).mockResolvedValue(1);
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });
  });
'''
S=dict(dir='ks_1818_p1_logger_guard',ticket='KS-1818',
 title='originate POST /seed-demo-users: the logger.error after readableErrorMessage sits outside any guard, so a throwing logger ends the seed loop and answers the constant 500: log in a try of its own (RUNG 2, code_patch: one product hunk + one test hunk in the existing KS-1802 test)',
 intro="DRAFT by Spark operator 11 for Wednesday, 2026-10-30 AEDT. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: QA gate 17 minor 1809-2, filed as KS-1818 (reasoning only in the ticket: not measured with the real logger; the failing LOGGER is simulated here by the mock). The fix shape is the ticket's own: fail500 (:110-126) and migrate-tenant-data already log in a second try with the comment 'Nothing more can be said if the logger itself fails'. TWIN WARNING: the briefs ks_1817_p1_fallback_text and ks_1817_p1b_no_message edit the SAME test file at the SAME place (after cell R3); raise them together, applying each hunk with its context re-read. Link the PR as Refs KS-1818 and KS-1802, never a close-word.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, the logger.error call replaced by a comment and a one-line try around the same call with a commented, empty-bodied catch'],
 tests=[dict(path=TP,new=False,edits=[(ANCHOR,ANCHOR+CELLS)])],
 testnote=['EXISTING (the KS-1802 test), modified in place: ONE hunk, two RED cells added after cell R3'],
 runner='jest` (`npx jest src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch', rung='2 (one product hunk of 6 lines byte-exact; one test hunk)',
 pins='''# code_patch, ONE hunk in originate routes/adminConfig.ts + the existing ks1802 test modified in place (two RED cells added); ref = another originate test (shape only); test_file pinned (in-place test); line = the logger.error line.
tier=code_patch
test_file=Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
ref=Blockchain/Dev/services/originate/src/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts
line=2121
ctx=65536
''',
 wrong="In `POST /api/admin/seed-demo-users` (`routes/adminConfig.ts`), the per-user `catch (err: any)` counts the failure (`failed++`) and then calls `logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) })` at `:2121`. KS-1802 made the message READ safe (`readableErrorMessage`, `:150-156`) but the `logger.error(...)` call itself sits directly in the catch with no try of its own. A logger that throws (or a serialiser that throws on a value) therefore leaves the per-user catch, ends the `for` loop at that user (the later users are never attempted) and reaches the route's outer catch, which answers the constant 500: the hang class KS-1802 closed. `fail500` (`:110-126`) and migrate-tenant-data (`:2273-2292`) already log in a second `try` with an empty-bodied `catch`. The change: wrap that one call the same way. Nothing else changes: the count, the message text and the report are untouched.",
 where="- `src/routes/adminConfig.ts:2121` - **must change**: the single line `        logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });` (8 spaces) is replaced by 2 comment lines, then `try { <the same call> } catch {` on ONE line, one comment line, `}`, exactly as under \"The exact change\". It is the last statement of the `catch (err: any)` that begins at `:2116`.\n- `src/routes/adminConfig.ts:150-156` (`readableErrorMessage`) is NOT touched.\n- `src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts`: cell R3 is lines 107-110 (closing `  });` is :110), :111 blank, :112 starts `control KS-1802 C1`. **The two new cells go between :110 and :111.** `mockLogError`, `mockExecuteRaw`, `seed` and `USERS` are in scope at module level; the file's `beforeEach` resets every mock (including an installed implementation) before each cell.",
 exactnote="ONE hunk in the product file.\n",
 donot="**Do NOT touch** `readableErrorMessage`, `failed++`, the surrounding loop, or any other line of either file.",
 testnote2="The `+` lines are byte-exact. The two new cells install a throwing implementation on `mockLogError` (the file's own mock of `../utils/logger`) and drive the route with the file's own `seed()` helper.",
 red=['RED KS-1818 R4','RED KS-1818 R5'],
 cells="- RED `R4`: at the tip the first failed insert's log call throws out of the per-user catch into the outer catch, the route answers 500 and the report equality fails by ASSERTION (`seed()` returns status 500); after the product edit it is 200 with 14 failed and the mock was called 14 times.\n- RED `R5`: at the tip the first user's log call throws and the other 13 are never seeded; after the edit 13 created, 1 failed.\n- Every existing cell (R1-R3, C1-C3) stays green on both trees: none of them installs a throwing logger.",
 premises="- `routes/adminConfig.ts:2116-2122` is the per-user catch and `:2121` the logger line (read at the tip). The two sibling guards are at `:110-126` and `:2273-2292`.\n- The test file mocks `../utils/logger` with `error: mockLogError` (a `jest.fn()`), and `beforeEach` calls `mockLogError.mockReset()`.\n- The service's test runner is jest. The golden is generated by script, not typed.",
 unmeasured="- The drafter did NOT run jest by hand: the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- A throwing REAL logger or serialiser is not exercised (the ticket says reasoning only); the mock stands in for it.\n- Swallowing a logger failure silently is the file's existing convention (two sibling sites); if the owner wants a fallback sink, that is a separate decision.\n- Open PRs touching either file: see the overlap count in the operator report (checked against every open PR on 2026-10-30).",
 scope="**KS-1818 only.** Link the PR as Refs KS-1818 / KS-1802. The `/seed-demo-users` handler's other logger calls (outside the per-user catch) are NOT changed here.",
)
