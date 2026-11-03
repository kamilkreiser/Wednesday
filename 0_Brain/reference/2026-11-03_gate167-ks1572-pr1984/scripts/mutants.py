"""Gate 167 mutants on the PR 1984 product hunk (services/referral/src/routes/referrals.ts, /apply only).
Each mutant: exact-string replacement on the HEAD blob (asserted to apply exactly once), written into the head clone,
then (1) the PR's 23-cell file and (2) the real-stack matrix g167.cjs (head tree, real PG) are run; the file is restored
from `git show HEAD:` after every mutant and its blob id re-checked. Results -> logs/mutants.json.
"""
import json, subprocess, os, hashlib
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate167-ks1572-pr1984'
R = W + '/repo'; REL = 'Blockchain/Dev/services/referral/src/routes/referrals.ts'; F = R + '/' + REL
ORIG = subprocess.run(['git', '-C', R, 'show', 'HEAD:' + REL], capture_output=True, text=True, check=True).stdout
OWNER = """    if (body.userId !== caller) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised' } });
    }
"""
APPLY_END = """      email: typeof authUser?.email === 'string' ? authUser.email : undefined,
    });
"""
M = {
  'M1 owner check removed': [(OWNER, '')],
  'M2 case-insensitive compare': [('if (body.userId !== caller) {', 'if (body.userId.toLowerCase() !== caller.toLowerCase()) {')],
  'M3 owner check moved after applyCode': [(OWNER, ''), (APPLY_END, APPLY_END + OWNER)],
  'M4 body ip/device passed through': [("      userId: caller,\n", "      userId: caller,\n      ipAddress: body.ipAddress || req.ip,\n      deviceId: body.deviceId,\n")],
  'M5 wallet read failure swallowed': [('      return next(err);\n    }\n\n    const referral', '      walletAddress = null;\n    }\n\n    const referral')],
  'M6 principal check removed': [("    if (typeof caller !== 'string' || caller === '') {\n      return res.status(403)", "    if (false) {\n      return res.status(403)")],
  'M7 empty-string principal allowed': [("typeof caller !== 'string' || caller === ''", "typeof caller !== 'string'")],
  'M8 platform-role bypass': [('if (body.userId !== caller) {', "if (body.userId !== caller && !isPlatformRole((authUser as any)?.role)) {")],
  'M9 applyCode gets body.userId': [('      userId: caller,\n', '      userId: body.userId,\n')],
  'M10 body walletAddress restored': [('      walletAddress: walletAddress ?? undefined,\n', '      walletAddress: body.walletAddress,\n')],
  'M11 body email restored': [("      email: typeof authUser?.email === 'string' ? authUser.email : undefined,\n", '      email: body.email,\n')],
  'M12 wallet failure rethrown to route catch': [('      return next(err);\n    }\n\n    const referral', '      throw err;\n    }\n\n    const referral')],
  'M13 wallet read uses body.userId': [('getLinkedWalletAddress(caller,', 'getLinkedWalletAddress(body.userId,')],
  'M14 403 becomes 401': [("    if (body.userId !== caller) {\n      return res.status(403)", "    if (body.userId !== caller) {\n      return res.status(401)")],
}
def blob():
    return subprocess.run(['git', '-C', R, 'hash-object', F], capture_output=True, text=True).stdout.strip()
HEADBLOB = subprocess.run(['git', '-C', R, 'rev-parse', 'HEAD:' + REL], capture_output=True, text=True).stdout.strip()
assert blob() == HEADBLOB
res = []
for name, reps in M.items():
    s = ORIG
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60], s.count(a)); s = s.replace(a, b, 1)
    assert s != ORIG
    open(F, 'w').write(s)
    tag = 'mut' + name.split()[0][1:]
    os.makedirs(W + '/logs/mut', exist_ok=True)
    t = subprocess.run(['node', W + '/scripts/vt.cjs', 'src/__tests__/ks1572-apply-referee-is-the-caller.test.ts'], capture_output=True, text=True)
    open(f'{W}/logs/mut/{tag}_prtest.log', 'w').write(t.stdout + t.stderr)
    import re
    clean = re.sub(r'\x1b\[[0-9;]*m', '', t.stdout + t.stderr)
    m = re.search(r'Tests\s+(.*)', clean); prline = m.group(1).strip() if m else 'NO SUMMARY (compile/collect error?)'
    g = subprocess.run(['node', W + '/scripts/g167.cjs', 'head'], capture_output=True, text=True, env={**os.environ, 'G167_TAG': tag})
    d = json.load(open(f'{W}/logs/probe/head_{tag}.json'))
    h = json.load(open(f'{W}/logs/probe/head.json'))
    diff = [r['label'] for r, r0 in zip(d['rows'], h['rows'])
            if (r['status'], r['writeRows'], json.dumps(r['referrals']), json.dumps(r['rewards']), json.dumps(r['fraudLog'])) !=
               (r0['status'], r0['writeRows'], json.dumps(r0['referrals']), json.dumps(r0['rewards']), json.dumps(r0['fraudLog']))]
    open(F, 'w').write(ORIG); assert blob() == HEADBLOB
    res.append({'mutant': name, 'prTest_rc': t.returncode, 'prTest': prline, 'matrix_rows': len(d['rows']), 'matrix_err': d.get('driverError'),
                'matrix_cells_differing_from_head': len(diff), 'differing': diff})
    print(name, '| PR file rc', t.returncode, prline, '| matrix diffs', len(diff), flush=True)
json.dump(res, open(W + '/logs/mutants.json', 'w'), indent=1)
print('restored blob', blob() == HEADBLOB)
