import difflib, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/gen/tip/'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TIP=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/tip_start.out').read().split()[0]
B='Blockchain/Dev/'
def rd(n): return open(G+n,encoding='utf-8').read()
def dd(p,old,new):
    assert old!=new
    return 'diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),'a/'+p,'b/'+p,n=3))
def rep(src,old,new):
    assert src.count(old)==1,(src.count(old),old)
    return src.replace(old,new)
def brief(tag,ks,title,origin,prod,tests,what,change,patch,red,redcells,unm,test_sec,pins,mode_extra=''):
    d=BR+tag+'/'; os.makedirs(d,exist_ok=False)
    open(d+'golden.diff','w',encoding='utf-8').write(patch)
    open(d+'golden_red.diff','w',encoding='utf-8').write(red)
    open(d+'spark.pins','w',encoding='utf-8').write(pins)
    tl=''.join('Test file: `%s`\n'%t for t in tests)
    rc=''.join('- `%s`\n'%c for c in redcells)
    md='''# %s

DRAFT by Spark operator 106 for Wednesday, 2026-11-09 AEDT. Secuura (Platform K) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: %s. Counter: this is round 1 of 2 (original).

Tier: `test_only_input`
Runner: vitest
Tip: `%s`
File: `%s`
%s
## The mode
test_only_input: the product is correct at the tip. The defect is a MISSING or WEAK assertion. The product file is READ-ONLY and never in the diff.%s

## What is wrong
%s

## The exact change
%s

The whole diff, to copy EXACTLY (hunk header counts are correct; 3 lines of unchanged context before and after each change; do not shorten the context, do not recompute the headers).

```diff
%s```

## The test
%s

## The red proof
The plant is `golden_red.diff` in the brief dir (applied only in the checker's clone, never to a real tree): %s

## Red cells
%s
## UNMEASURED
%s

## Scope
Exactly the Test file lines above. The product file is not in the diff.

## Output
ONE unified diff in a ```diff fence.
'''%(title,origin,TIP,prod,tl,mode_extra,what,change,patch,test_sec,'see below',rc,unm)
    open(d+'%s.md'%ks,'w',encoding='utf-8').write(md)
    print('wrote',d)
    return d

# ---- KS-2121 ----------------------------------------------------------------------------------------------------
TP=B+'services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts'
PI=B+'services/transfer/src/index.ts'
ot=rd('ks2081-transfer-doors-refuse-non-user-principals.test.ts')
tail="  });\n});\n"
assert ot.endswith("    expect(await statusOf(own)).toBe('pending_approval');\n  });\n});\n")
add='''
describe('KS-2121: the refusal is one answer across the six write doors', () => {
  it('RED KS-2121 F1: a key reads one and the same refusal, headers included, at all six write doors', async () => {
    const id = await open();
    const token = key(null, TENANT_A);
    const prints = new Set<string>();
    for (const d of DOORS) {
      const res = await call(token, 'POST', d.path(id), d.body());
      expect([d.name, res.status]).toEqual([d.name, 403]);
      prints.add(fingerprint(res));
    }
    expect(DOORS).toHaveLength(6);
    expect(prints.size).toBe(1);
  });
});
'''
nt=ot+add
pi=rd('transfer_index.ts')
npi=rep(pi,"  if (!isNonUserPrincipal((req as any).user)) return false;\n  res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'An API key cannot open or act on a transfer.' } });\n",
 "  if (!isNonUserPrincipal((req as any).user)) return false;\n  res.setHeader('x-ks2121-door', req.path); // TAMPER: a per-door response header\n  res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'An API key cannot open or act on a transfer.' } });\n")
brief('ks_2121_o106_p1_transfer_doors_one_refusal_fingerprint_across_six_doors','KS-2121',
 'KS-2121 (TEST-ONLY): no cell compares the 403 refusal across the six transfer write doors; a per-door header survives all 172 cells',
 'KS-2121 (seat S 38th filing, 2026-11-09; Backlog; Low; gate 240 note N5, tamper own3: a per-door response header left 0 of 172 cells red)',
 B+'services/transfer/src/index.ts',[TP],
 'PR 2077 (KS-2081) says a key reads one and the same 403 refusal at each of the six transfer write doors. In `services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts`, R1 (status and body) and R2 pin the BYTES at each door; R3 compares `fingerprint(r)` (status, body and every header but `date`) but only WITHIN one door (its own row, an unknown id, a malformed id). No cell compares that fingerprint ACROSS the doors, so a per-door response header on the refusal stays green. The refusal is built in one place, `refuseNonUserPrincipal` (`services/transfer/src/index.ts` line 522); today it is constant (gate 240 cell O2 measured one fingerprint across all six doors).',
 'Append ONE new `describe` with ONE `it` cell at the END of the test file, after the last existing `});`. Nothing else in the file changes. The cell opens one transfer, takes one key (`key(null, TENANT_A)`), calls each of the six doors in `DOORS` (open, open alias, approve, reject, execute, cancel) with the door\'s own path and body, requires status 403 at each, and expects ONE distinct `fingerprint` over the six replies. The whole diff, to copy EXACTLY:',
 dd(TP,ot,nt),
 dd(PI,pi,npi),
 ['reads one and the same refusal, headers included'],
 'That a per-door header is the only way the fingerprints can differ: the cell compares status, body and every header but `date`, so a different body or status would also fail it, which is intended. That the six doors are exactly `DOORS` (open, open alias, approve, reject, execute, cancel) is asserted by `toHaveLength(6)`. Not tried: a different key kind (a keyed connector id) at the six doors, since R1 already pins the bytes for all three key kinds.',
 'The cell is in the diff above; copy it verbatim. It reuses `open`, `key`, `call`, `fingerprint`, `DOORS` and `TENANT_A`, all already defined in the file. It passes on the correct code (the refusal is constant) and fails by an assertion when a per-door header is added.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n')

# ---- KS-2123 ----------------------------------------------------------------------------------------------------
TK=B+'services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts'
PN=B+'services/api-gateway/src/routes/notifications.ts'
ok=rd('ks1448-notification-create-own-id-only.test.ts')
nk=rep(ok,"  ['an org admin', { userId: 'ks1448-org', role: 'ORG_ADMIN' }],\n","  ['an org admin', { userId: 'ks1448-org', role: 'ORG_ADMIN' }],\n  ['an admin', { userId: 'ks1448-admin', role: 'ADMIN' }],\n")
nk=rep(nk,"""  it('RED KS-1448 R5: the answer does not depend on whether the target has rows, which is why 403 and not 404', async () => {""",
"""  it.each(['purchase', 'certification', 'verification', 'transfer'])('RED KS-1448 R6: a notification of type %s for another user gets 403 and no row is stored', async (type) => {
    const target = `ks1448-target-type-${type}`;
    const res = await post({ userId: 'ks1448-type-caller', role: 'user' }, { type, title: 'T', message: 'M', userId: target });
    expect(res._status).toBe(403);
    expect(res._json).toEqual(REFUSAL);
    expect(await rowsOf(target)).toEqual([]);
  });

  it('RED KS-1448 R5: the answer does not depend on whether the target has rows, which is why 403 and not 404', async () => {""")
pn=rd('gw_notifications.ts')
npn=rep(pn,"    if (userId !== getUserId(req)) {\n","    if (userId !== getUserId(req) && (type === 'security' || type === 'system') && (req as any).user?.role !== 'ADMIN') { // TAMPER: guard only two types, exempt ADMIN\n")
brief('ks_2123_o106_p1_notification_own_id_rule_pins_every_type_and_the_admin_role','KS-2123',
 'KS-2123 item 1 (TEST-ONLY): PR 2072\'s own-id rule has two surviving mutants, guarding only security and system, and exempting the role ADMIN',
 'KS-2123 (seat S 38th filing, 2026-11-09; Backlog; Medium; gate 246 finding 72-2 / G246-F2). Items: two of the three surviving mutants. NOT covered: the third (identity read from the x-user-id header, which needs the real middleware) and item 2 (the OpenAPI example)',
 B+'services/api-gateway/src/routes/notifications.ts',[TK],
 '`POST /api/notifications` (routes/notifications.ts line 321, `if (userId !== getUserId(req))`) refuses a userId other than the caller\'s, for every principal and every type (the ruling quoted at the top of the test file). Gate 246 measured that two plausible variants of it pass all 50 cells of `ks1448-notification-create-own-id-only.test.ts`: (a) guarding only the `security` and `system` types (no refusal cell uses `purchase`, `certification`, `verification` or `transfer`; `BODY` at line 89 uses `system` and the explicit bodies at lines 121 and 174 use `security`); (b) exempting the role `ADMIN`, a real spelling (`packages/shared/src/security/keyRevokePolicy.ts` line 94, `SCOPED_ADMIN_ROLES`), absent from the file\'s `PRINCIPALS` list (lines 93-105). The shipped code has neither variant.',
 'Two edit points in the one test file, nothing else. (1) In `PRINCIPALS`, add one row after the `an org admin` row: `[\'an admin\', { userId: \'ks1448-admin\', role: \'ADMIN\' }],` (the existing R1 `it.each` then covers it). (2) Add ONE new `it.each` cell, labelled R6, directly BEFORE the R5 cell inside the first describe: for each of `purchase`, `certification`, `verification`, `transfer`, a plain user posting that type for another user gets 403, the same REFUSAL object, and no row for the target. The whole diff, to copy EXACTLY:',
 dd(TK,ok,nk),
 dd(PN,pn,npn),
 ['R1: an admin posting for another user gets 403','R6: a notification of type'],
 'The third surviving mutant (identity read from the `x-user-id` request header instead of the verified token): the harness replaces `authenticateToken` with a pass-through and never sets that header, so a cell for it needs the real middleware and is NOT in this pass. The OpenAPI example at `api-gateway.openapi.ts` lines 241-246 (item 2 of the ticket) is not touched. That the plant below is the same two variants the gate planted is the brief author\'s reading of the ticket text (the gate\'s own plant files were not read).',
 'Both edits are in the diff above; copy them verbatim. The R6 cell reuses `post`, `rowsOf` and `REFUSAL`, already defined in the file. Both pass on the shipped code and fail by an assertion when the guard covers only `security` and `system` and exempts the role `ADMIN`.',
 'shared_pkg_dir=packages/shared\nshared_pkg_name=@secuura/shared\n')
