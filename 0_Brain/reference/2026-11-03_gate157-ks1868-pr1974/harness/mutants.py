#!/usr/bin/env python3
# G157 mutants: each is ONE exact replace of the Nth occurrence (0 = pool listener, 1 = runDbReadyHook catch) in head db.ts.
# Runs the PR's new test file and the full billing vitest suite; restores db.ts by git checkout and asserts the blob sha.
import json, subprocess, pathlib
W = pathlib.Path('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974')
R = W / 'repo'; B = R / 'Blockchain/Dev/services/billing'; DB = B / 'src/db.ts'
V = str(R / 'Blockchain/Dev/node_modules/.bin/vitest')
T = 'src/__tests__/ks1868-billing-db-pool-error-and-ready-hook-unreadable-throw.test.ts'
HEAD_BLOB = '3f2d24d48a91f58710abd4915e6ac76dfd83f54d'
OPS = [
  ('1', 'optional chain dropped', 'const m = err?.message;', 'const m = (err as any).message;'),
  ('2', 'String() coercion dropped', 'reason = m === undefined || m === null ? m : String(m);', 'reason = m === undefined || m === null ? m : (m as any);'),
  ('3', 'constant changed', "reason = 'unreadable thrown value';", "reason = 'unreadable';"),
  ('4', 'null/undefined passthrough dropped', 'reason = m === undefined || m === null ? m : String(m);', 'reason = String(m);'),
  ('5', 'catch rethrows', "reason = 'unreadable thrown value';", "throw new Error('g157 m5');"),
  ('6', 'log line removed', None, None),
]
LOGS = {0: "logger.error('DB pool unexpected error', { error: reason });", 1: "logger.error('DB ready boot work failed', { error: reason });"}
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def blob(): return sh('git', '-C', str(R), 'hash-object', str(DB)).stdout.strip()
def vitest(name, *extra):
  out = W / f'logs/mut_{name}.json'
  p = sh(V, 'run', '--root', str(B), '--reporter=json', f'--outputFile={out}', *extra)
  try:
    j = json.loads(out.read_text()); return {'rc': p.returncode, 'pass': j['numPassedTests'], 'fail': j['numFailedTests'], 'total': j['numTotalTests'],
      'failed': [a['title'][:50] for s in j['testResults'] for a in s['assertionResults'] if a['status'] != 'passed']}
  except Exception as e: return {'rc': p.returncode, 'err': str(e)}
assert blob() == HEAD_BLOB, blob()
src0 = DB.read_text(); res = []
for site, tag in ((0, 'P'), (1, 'H')):
  for (n, desc, old, new) in OPS:
    if old is None: old, new = LOGS[site], 'void reason;'
    idxs = []; i = src0.find(old)
    while i != -1: idxs.append(i); i = src0.find(old, i + 1)
    pos = idxs[site] if len(idxs) == 2 else (idxs[0] if len(idxs) == 1 else None)
    assert pos is not None and len(idxs) in (1, 2), (tag + n, len(idxs))
    DB.write_text(src0[:pos] + new + src0[pos + len(old):])
    a = vitest(f'{tag}{n}_new', T); b = vitest(f'{tag}{n}_full')
    sh('git', '-C', str(R), 'checkout', '-q', '--', 'Blockchain/Dev/services/billing/src/db.ts'); assert blob() == HEAD_BLOB
    killed = a.get('fail', 0) > 0 or b.get('fail', 0) > 0 or a['rc'] != 0 or b['rc'] != 0
    r = {'id': tag + n, 'desc': desc, 'new': a, 'full': b, 'killed': killed}; res.append(r)
    print(r['id'], desc, 'KILLED' if killed else 'SURVIVED', 'new', a.get('pass'), '/', a.get('total'), 'full', b.get('pass'), '/', b.get('total'), a.get('failed'), flush=True)
(W / 'logs/mutants.json').write_text(json.dumps(res, indent=1))
print('killed', sum(r['killed'] for r in res), 'of', len(res), '; restored blob', blob())
