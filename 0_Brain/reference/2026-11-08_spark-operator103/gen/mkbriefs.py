import difflib, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator103/gen/'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TIP='abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82'
SV='Blockchain/Dev/services/'
def rd(n): return open(G+n,encoding='utf-8').read()
def dd(a,b,p):
    return 'diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),'a/'+p,'b/'+p,n=3))
def once(s,old,new):
    assert s.count(old)==1,(s.count(old),old[:60]); return s.replace(old,new)

def brief(tag,ks,title,origin,wrong,product,tests,cellnote,plantnote,reds,unmeasured,pins,golden,red):
    d=BR+tag+'/'; os.makedirs(d,exist_ok=True)
    open(d+'golden.diff','w',encoding='utf-8').write(golden)
    open(d+'golden_red.diff','w',encoding='utf-8').write(red)
    open(d+'spark.pins','w').write(pins)
    tf=''.join('Test file: `%s`\n'%t for t in tests)
    md='''# %s (TEST-ONLY: one new describe/cell appended to one existing test file)

DRAFT by Spark operator 103 for Wednesday, 2026-11-08 AEDT. Secuura (Platform K) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: %s

Tier: `test_only_input`
Runner: %s
Tip: `%s`
File: `%s`
%s
## The mode
test_only_input: the product is correct at the tip. The defect is a MISSING assertion. The product file is READ-ONLY and never in the diff.

## What is wrong
%s

## The exact change
%s

```diff
%s```

## The test
%s

## The red proof
%s

## Red cells
%s

## UNMEASURED
%s

## Scope
Exactly the one Test file; one cell added. The product file is not in the diff.

## Output
ONE unified diff in a ```diff fence.
'''%(title,origin,'vitest' if 'api-gateway' in tests[0] else 'jest',TIP,product,tf,wrong,
 'Append the lines below to the END of the existing test file, after its last line (nothing else changes). The whole diff, to copy EXACTLY (hunk header counts are correct: 3 lines of unchanged context before the change, git apply takes it with no fuzz; do not shorten the context, do not recompute the header).' if tag.endswith('p1') or tag.endswith('p2') else 'Insert ONE `it` cell into the existing describe, directly after the R5 cell and before the control C1 cell. Nothing else in the file changes. The whole diff, to copy EXACTLY (hunk header counts are correct; 3 lines of unchanged context before and after; do not shorten the context, do not recompute the header).',
 golden,cellnote,plantnote,reds,unmeasured)
    open(d+'KS-%d.md'%ks,'w',encoding='utf-8').write(md)

# ---- P1 KS-2016
tp1=SV+'api-gateway/src/__tests__/ks1645-the-audit-export-pages-its-rows-and-claims-no-type-filter.test.ts'
t=rd('ks1645.test.ts.tip')
add1='''
describe('KS-2016 - the caller\\'s Authorization header goes upstream on every page, not only the first', () => {
  it('RED KS-2016 A1: three upstream pages (2,300 rows) each carry the caller\\'s Authorization header', async () => {
    upstreamRows = manyRows(2300);
    const status = await new Promise<number>((resolve, reject) => {
      http.get({ hostname: '127.0.0.1', port, path: `/api/admin/audit/export?${RANGE}&format=json`, headers: { authorization: 'Bearer ks2016-caller' } }, (res) => {
        res.resume();
        res.on('end', () => resolve(res.statusCode ?? 0));
      }).on('error', reject);
    });
    const sent = fetchMock.mock.calls.map((call) => ((call as unknown[])[1] as { headers?: Record<string, string> } | undefined)?.headers?.Authorization);
    expect(status).toBe(200);
    expect(sent).toEqual(['Bearer ks2016-caller', 'Bearer ks2016-caller', 'Bearer ks2016-caller']);
  });
});
'''
assert t.endswith('});\n')
g1=dd(t,t+add1,tp1)
ae=rd('audit-export.ts.tip')
old="          { method: 'GET', headers, signal: AbortSignal.timeout(AUDIT_LIST_TIMEOUT_MS) },\n"
new="          { method: 'GET', headers: entries.length > 0 ? { 'Content-Type': 'application/json' } : headers, signal: AbortSignal.timeout(AUDIT_LIST_TIMEOUT_MS) },\n"
r1=dd(ae,once(ae,old,new),SV+'api-gateway/src/routes/audit-export.ts')
brief('ks_2016_o103_p1_audit_export_auth_every_page',2016,'KS-2016 api-gateway audit export: no cell asserts the caller\'s Authorization on every upstream page','KS-2016 (gate 202 note G202-N6: mutant M4, which drops Authorization on pages 2 and later, survives all 12 cells of PR 2012).',
 'The audit export pages the security service (limit 1000). `audit-export.ts` builds `headers` once (line 185, the caller\'s Authorization) and passes it to every page fetch (line 198). The KS-1645 test file never reads the headers a page fetch was given, so a change that sends the header on page 1 only stays green (gate 202 mutant M4; the real effect would be fail-closed, the cell is the missing guard).',
 SV+'api-gateway/src/routes/audit-export.ts',[tp1],
 'The cell is in the diff above; copy it verbatim. It reuses `http`, `port`, `RANGE`, `upstreamRows`, `manyRows` and `fetchMock` from the file. It sends a caller Authorization header, drives a 2,300-row export (three pages of 1000), and asserts every recorded upstream fetch carried that exact Authorization header.',
 'The plant is `golden_red.diff` in the brief dir (the checker applies it in its own clone, never to a real tree): it sends the page fetch\'s headers WITHOUT Authorization once any entries have been collected, i.e. on page 2 and later, which is gate 202\'s M4.',
 '- `three upstream pages (2,300 rows) each carry`',
 'Whether a missing Authorization is the only way page 2+ could lose the caller identity (only the Authorization header is pinned). Not run beyond the checker.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n',g1,r1)

# ---- P2 KS-2012
tp2=SV+'api-gateway/src/__tests__/ks1185-f2-f3-idle-bound-and-late-body-log.test.ts'
t=rd('ks1185.test.ts.tip')
add2='''
describe('KS-2012 - the late-body warn line carries the error text', () => {
  it('RED KS-2012 E1: a 201 whose body never ends logs the warn line with the status AND the idle-bound error text', { timeout: 15_000 }, async () => {
    behave = statusThenSilence(201);
    const log = vi.fn<Log>();
    await approve(await startGateway(freshStore(), log));
    await sleep(FORWARD_TIMEOUT_MS + 700);
    const late = calls(log, 'warn', (m) => m.includes('reply body did not finish'));
    expect(late).toHaveLength(1);
    expect(late[0][2]).toMatchObject({ status: 201, error: `originate did not answer within ${FORWARD_TIMEOUT_MS} ms` });
  });
});
'''
assert t.endswith('});\n')
g2=dd(t,t+add2,tp2)
v=rd('verification.ts.tip')
old="{ status: decidedByStatus, error: err.message });"
r2=dd(v,once(v,old,"{ status: decidedByStatus });"),SV+'api-gateway/src/routes/verification.ts')
brief('ks_2012_o103_p2_approve_forward_warn_error_key',2012,'KS-2012 api-gateway approve-forward warn line: no cell asserts the `error` key (TEST-ONLY)','KS-2012 (gate 201 note G201-N2: mutant own2 drops `error: err.message` from the warn meta and leaves all 7 cells of PR 2011 green).',
 'In `routes/verification.ts` (line 647) the late-body warn line logs `{ status: decidedByStatus, error: err.message }`. The F3 cells assert the warn line and its `status` (toMatchObject({ status: 201 })) but never the `error` key, so dropping it stays green.',
 SV+'api-gateway/src/routes/verification.ts',[tp2],
 'The cell is in the diff above; copy it verbatim. It reuses `statusThenSilence`, `startGateway`, `freshStore`, `approve`, `sleep`, `calls`, `FORWARD_TIMEOUT_MS` and `Log` already defined in the file. It asserts the single warn line\'s meta carries `status: 201` AND the idle-bound error text (the Error the route itself builds when the socket is silent for the bound).',
 'The plant is `golden_red.diff` in the brief dir (applied only in the checker\'s clone): it removes `error: err.message` from that warn meta, which is gate 201\'s mutant own2.',
 '- `logs the warn line with the status AND the idle-bound error text`',
 'That the exact error text is the right thing to pin rather than only that an `error` string is present; the text is the route\'s own (`originate did not answer within N ms`, built at verification.ts line 639), not a Node message.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n',g2,r2)

# ---- P3 KS-2005
tp3=SV+'originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts'
t=rd('ks1990.test.ts.tip')
anchor="  it('control KS-1990 C1:"
cell6='''  it('RED KS-1990 R6: ONE created and 13 failed answers 200 with success false (the boundary: any created row keeps the status at 200)', async () => {
    let calls = 0;
    mockExecuteRaw.mockImplementation(async () => {
      calls++;
      if (calls === 1) return 1;
      throw new Error('ks1990 insert failed');
    });
    expect(outcome(await seed())).toEqual({ status: 200, body: { success: false, seededUsers: 1, created: 1, alreadyPresent: 0, failed: 13 } });
  });

'''
g3=dd(t,once(t,anchor,cell6+anchor),tp3)
a=rd('adminConfig.ts.tip')
old="    const nothingCreatedAndSomethingFailed = created === 0 && failed > 0;\n"
r3=dd(a,once(a,old,"    const nothingCreatedAndSomethingFailed = created < 2 && failed > 0;\n"),SV+'originate/src/routes/adminConfig.ts')
brief('ks_2005_o103_p3_seed_demo_users_one_created',2005,'KS-2005 originate seed-demo-users: no cell pins created 1 with failed above 0 (TEST-ONLY: one cell, R6)','KS-2005 (gate 195 finding G195-F1: mutant g1, `created === 0` to `created < 2`, leaves all 20 cells of PR 2006 green).',
 'The 500 condition of POST /seed-demo-users is `created === 0 && failed > 0` (adminConfig.ts line 2163). None of the KS-1990 cells has created = 1 with failed above 0 (R2 has 13 created, R4 has 10), so changing `=== 0` to `< 2` keeps them green; the only effect is that 1 created and 13 failed would answer 500 instead of the ruled 200 with success false.',
 SV+'originate/src/routes/adminConfig.ts',[tp3],
 'The cell is in the diff above; copy it verbatim. It follows the shape of R3/R4/R5 in the same file: the first insert resolves 1 (created), every later insert rejects (13 failed), and the reply must be 200 with success false and the counts 1 / 0 / 13.',
 'The plant is `golden_red.diff` in the brief dir (applied only in the checker\'s clone): it changes `created === 0` to `created < 2` on that line, which is gate 195\'s mutant g1.',
 '- `R6: ONE created and 13 failed`',
 'Whether the sibling file ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts needs the same cell (the ticket names only the KS-1990 file). adminConfig.ts is listed by open PR 2087 (the admin mint route) and by held READYs; it is the read-only product here, not in the diff.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n',g3,r3)
print('ok')
