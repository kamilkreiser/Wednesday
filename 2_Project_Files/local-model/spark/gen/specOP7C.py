P='Blockchain/Dev/services/originate/src/routes/gdpr.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1029-gdpr-dsr-update-id-guard.test.ts'
E1=("    const updated = await gdpr.updateDSRStatus(req.params.dsrId, status, processedBy, notes);\n"
    "    res.json({ success: updated, message: updated ? 'DSR updated' : 'DSR not found' });\n",
    "    const updated = await gdpr.updateDSRStatus(req.params.dsrId, status, processedBy, notes);\n"
    "    // KS-1112: a canonical id that names no row answers the same 404 'DSR not found' as GET /dsr/:dsrId and as a non-canonical id above.\n"
    "    if (!updated) {\n"
    "      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'DSR not found' } });\n"
    "    }\n"
    "    res.json({ success: true, message: 'DSR updated' });\n")
H_OLD=" * as well (N1, N2). A canonical absent id is unchanged: 200 {success:false, 'DSR not found'}.\n"
H_NEW=" * as well (N1, N2). A canonical absent id answers the same 404 NOT_FOUND 'DSR not found' (KS-1112; it was 200 {success:false}).\n"
U1_OLD="""  it('U1 an uppercase canonical id passes the guard (the pattern is case-insensitive) and reaches the lookup', async () => {
    const res = await patchDsr(UPPERCASE_ABSENT_ID, VALID_BODY);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: false, message: 'DSR not found' });
"""
U1_NEW="""  it('RED KS-1112 U1 an uppercase canonical id passes the guard (the pattern is case-insensitive) and reaches the lookup, then answers 404', async () => {
    const res = await patchDsr(UPPERCASE_ABSENT_ID, VALID_BODY);
    expect(res.status).toBe(404);
    expect(await res.json()).toEqual({ success: false, error: { code: 'NOT_FOUND', message: 'DSR not found' } });
"""
A1_OLD="""  it('A1 a canonical absent id is unchanged: 200 {success:false}', async () => {
    const res = await patchDsr('aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', VALID_BODY);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: false, message: 'DSR not found' });
"""
A1_NEW="""  it('RED KS-1112 A1 a canonical absent id answers 404 NOT_FOUND, as GET does', async () => {
    const res = await patchDsr('aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', VALID_BODY);
    expect(res.status).toBe(404);
    expect(await res.json()).toEqual({ success: false, error: { code: 'NOT_FOUND', message: 'DSR not found' } });
"""
S=dict(dir='ks_1112_p1',ticket='KS-1112',
 title='originate PATCH /api/gdpr/dsr/{dsrId}: a canonical id that names no row answers 200 {success:false} where a non-canonical id and GET answer 404 - align PATCH with GET (RUNG 3, code_patch: one product hunk + three hunks in the existing ks1029 test; the DRAFTER chose option 1)',
 intro="DRAFT by Spark operator 7 for Wednesday, 2026-10-29 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. DECISION FLAG: the ticket offers two options (align PATCH to GET's 404, or document the split). This brief takes option 1. It is a CONTRACT change (a status code a caller sees), so the PR needs the owner's confirmation. NOT in this brief: the published spec's 200 description ('success=false if id not found') in originate.openapi.ts and its generated yaml, which the ticket also asks to update.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, 2 lines replaced by 6'],
 tests=[dict(path=TP,new=False,edits=[(H_OLD,H_NEW),(U1_OLD,U1_NEW),(A1_OLD,A1_NEW)])],
 testnote=['EXISTING (KS-1029 id-guard test, jest), modified in place: THREE hunks (a header comment line; the U1 cell; the A1 cell: title, status and body of two assertions each)'],
 runner='jest` (`npx jest src/__tests__/ks1029-gdpr-dsr-update-id-guard.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch', rung='3 (one product hunk, three test hunks, every line byte-exact)',
 pins='''# code_patch, ONE hunk in originate routes/gdpr.ts + the existing ks1029 test modified in place (3 hunks); test_file pinned; ref = the sibling ks444 gdpr test (shape only); line = the first changed product line.
tier=code_patch
test_file=Blockchain/Dev/services/originate/src/__tests__/ks1029-gdpr-dsr-update-id-guard.test.ts
ref=Blockchain/Dev/services/originate/src/__tests__/ks444-gdpr-dsr-update-withdraw-guards.test.ts
line=412
ctx=65536
''',
 wrong="After KS-1029, `PATCH /api/gdpr/dsr/:dsrId` answers \"DSR not found\" with two statuses depending on the spelling of the id: a non-canonical id is refused before the lookup with `404 NOT_FOUND 'DSR not found'` (`routes/gdpr.ts:408-410`), but a canonical id that names no row falls through to `res.json({ success: updated, message: updated ? 'DSR updated' : 'DSR not found' })` (`:413`) and answers `200 {success:false, message:'DSR not found'}`. `GET /dsr/:dsrId` answers 404 for both (`:366`). The change: when `updateDSRStatus` returns false, answer the same `404 {success:false, error:{code:'NOT_FOUND', message:'DSR not found'}}` the id guard sends, and send `{success:true, message:'DSR updated'}` otherwise. A database error still rethrows to the 500 handler (KS-754), the body checks still come first. The two KS-1029 control cells that pinned the old 200 (U1 and A1) are updated in place.",
 where="- `src/routes/gdpr.ts:412-413` - **must change**: line 412 (`const updated = await gdpr.updateDSRStatus(...)`) is context; line 413 (`res.json({ success: updated, message: updated ? 'DSR updated' : 'DSR not found' });`) is replaced by the comment line, the 3-line `if (!updated) {...}` block and `res.json({ success: true, message: 'DSR updated' });` under \"The exact change\".\n- `src/__tests__/ks1029-gdpr-dsr-update-id-guard.test.ts`: header line 19, the U1 cell (`:168-173`) and the A1 cell (`:175-180`) change as under \"The test\". Every other cell (M1-M4, N1, N2, R1, D1, O1 and the rest) is NOT touched.",
 exactnote="ONE hunk in the product file.\n",
 donot="**Do NOT touch** the id guard at `:408-410`, `updateDSRStatus`, the GET handlers, or any other line of either file.",
 testnote2="The `+` lines are byte-exact. Only the header comment line, the titles, the two `expect(res.status)` lines and the two `expect(await res.json())` lines of U1 and A1 change; `mockExecuteRaw` expectations stay.",
 red=['RED KS-1112 U1','RED KS-1112 A1'],
 cells="- RED `RED KS-1112 U1` and `RED KS-1112 A1` (titles start with `RED`, which is how the checker tells a red cell from a control): at the tip an absent canonical id answers 200 `{success:false, message}`, so `toBe(404)` fails by ASSERTION; after the product edit it answers 404 with the NOT_FOUND envelope.\n- CONTROL (existing, untouched): R1 (a real id still answers 200 `{success:true, message:'DSR updated'}`), D1 (a database error on a canonical id still answers 500), M1-M4/N1/N2 (non-canonical ids 404 with no DB call), O1 (body 400 first).",
 premises="- `routes/gdpr.ts:408-413` is as quoted (read at the tip). `UPPERCASE_ABSENT_ID`, `VALID_BODY`, `REAL_DSR_ID` and `DB_ERROR_DSR_ID` exist in the ks1029 test and are not touched.\n- No other test in `services/originate/src/__tests__` asserts the 200 `{success:false}` answer of PATCH (searched `DSR not found`: only ks1029 lines 162/171/178, comments in ks754).\n- The service's test runner is jest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether any consumer (the admin UI, a connector) reads the old 200 `{success:false}` answer: unmeasured.\n- The published spec description and yaml are not changed by this brief.\n- Open PRs touching these files: none by the git file lists of PRs 1782 and 1785-1799 read on 2026-10-29.",
 scope="**KS-1112 option 1 only.** DECISION FLAG above. Link the PR as Refs KS-1112 until the owner has confirmed the contract change.",
)
