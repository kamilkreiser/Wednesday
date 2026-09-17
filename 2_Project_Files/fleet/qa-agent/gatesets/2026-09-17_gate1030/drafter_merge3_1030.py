#!/usr/bin/env python3
"""drafter_merge3_1030.py — the READY says 566107f01's merge of develop 20ab16f9a regenerated the issuer, referral and vc-issuer locks and the
result is byte-identical to git's merge. Re-derived by PARSE in the drafter's own clone: for each of the 3 locks, every packages entry at the
merge commit must equal the side that changed it relative to the common ancestor 19f1e5475 (develop side = #1027 js-yaml/bbm; change side =
17cbb1091 vitest family); an entry changed on BOTH sides is listed. Blob identity to merge-tree is proven in drafter_setup_parse_1030.out part B.
CONTROL: a planted version on one develop-side entry must be reported."""
import json, subprocess
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
C = json.load(open(G + '/drafter_paths.json'))['C']
ANC, DEVS, CHG, MRG, HEAD = '19f1e54750ce2b65312a687add2db4f5628edb7d', '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb', '17cbb10919854658a40a07fc3e5fdafdd1e82e08', '566107f019e6cc05b6b4b5a7d62122a3f9772c80', 'e43af493418a1f13cfb60c994380fb74d79ad07e'
def lk(sha, p): return json.loads(subprocess.run(['git', '-C', C, 'show', sha + ':' + p], capture_output=True, text=True, check=True).stdout)
def blob(sha, p): return subprocess.run(['git', '-C', C, 'rev-parse', sha + ':' + p], capture_output=True, text=True).stdout.strip()[:9]
def judge(a, d, c, m):
    bad, both, nd, nc = [], [], 0, 0
    for k in sorted(set(a) | set(d) | set(c) | set(m)):
        dv, cv = d.get(k) != a.get(k), c.get(k) != a.get(k)
        if dv and cv: both.append(k); continue
        want = d.get(k) if dv else (c.get(k) if cv else a.get(k))
        nd += dv; nc += cv
        if m.get(k) != want: bad.append(k)
    return bad, both, nd, nc
for sub in ('frontend/issuer', 'services/referral', 'services/vc-issuer'):
    p = 'Blockchain/Dev/%s/package-lock.json' % sub
    a, d, c, m = (lk(s, p)['packages'] for s in (ANC, DEVS, CHG, MRG))
    bad, both, nd, nc = judge(a, d, c, m)
    fam = {k: (a.get(k, {}).get('version'), m.get(k, {}).get('version')) for k in m if k.endswith(('node_modules/js-yaml', 'node_modules/baseline-browser-mapping'))}
    print('%-20s blobs anc %s dev %s chg %s merge %s head %s | develop-side entries %d, change-side %d, BOTH-sides %s | merge entries not equal to their changing side: %s | js-yaml/bbm anc->merge %s' % (
        sub, blob(ANC, p), blob(DEVS, p), blob(CHG, p), blob(MRG, p), blob(HEAD, p), nd, nc, both, bad, fam))
p = 'Blockchain/Dev/services/referral/package-lock.json'
a, d, c, m = (lk(s, p)['packages'] for s in (ANC, DEVS, CHG, MRG))
k = next(x for x in d if d.get(x) != a.get(x)); m[k] = dict(m[k], version='0.0.0-planted')
print('CONTROL planted version on develop-side entry', k, '-> reported', judge(a, d, c, m)[0])
