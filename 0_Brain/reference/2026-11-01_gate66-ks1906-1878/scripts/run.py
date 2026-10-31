#!/usr/bin/env python3
"""Gate 66 runner: run vitest files with JSON reporter, product swaps and mutants, sha256-asserted restores."""
import hashlib, json, os, subprocess, sys
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate66-ks1906-1878'
D = G + '/repo/Blockchain/Dev'
VC = D + '/services/vc-issuer'
BASE = 'eb9651392f4959ea509376d885242cf3e22512ed'
PROD = ['src/ownership.ts', 'src/repositories/credentialRepo.ts', 'src/routes/credentials.ts']
FILES = ['src/__tests__/ks1906-ownerless-credentials-read-by-platform-admins-of-their-tenant.test.ts',
         'src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts',
         'src/__tests__/ks1683-credential-list-and-by-hash-bound-to-the-creator.test.ts',
         'src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts']
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def vitest(files, tag):
    out = f'{G}/tmp/{tag}.json'
    env = dict(os.environ, TMPDIR=G+'/tmp')
    p = subprocess.run(['nice','-n','10', D+'/node_modules/.bin/vitest','run','--root',VC,'--maxWorkers=2',
                        '--reporter=json','--outputFile='+out] + files, cwd=VC, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    open(f'{G}/evidence/{tag}.log','w').write(p.stdout)
    res = {}
    j = json.load(open(out))
    for f in j['testResults']:
        if f.get('status') == 'failed' and not f['assertionResults']:
            res[os.path.basename(f['name'])+'::<COLLECT>'] = 'failed'
        for a in f['assertionResults']:
            res[os.path.basename(f['name'])+'::'+a['fullName']] = a['status']
    return p.returncode, res
def summary(res):
    c = {}
    for v in res.values(): c[v] = c.get(v,0)+1
    return c
def base_bytes(rel):
    return subprocess.run(['git','-C',G+'/repo','show',f'{BASE}:Blockchain/Dev/services/vc-issuer/{rel}'],stdout=subprocess.PIPE,check=True).stdout
def mode_base():
    orig = {r: (open(VC+'/'+r,'rb').read(), sha(VC+'/'+r)) for r in PROD}
    try:
        for r in PROD: open(VC+'/'+r,'wb').write(base_bytes(r))
        for r in PROD: assert sha(VC+'/'+r) != orig[r][1], f'base swap did not land {r}'
        rc, res = vitest(FILES, 'base_product')
    finally:
        for r in PROD: open(VC+'/'+r,'wb').write(orig[r][0])
        for r in PROD: assert sha(VC+'/'+r) == orig[r][1], f'restore failed {r}'
    return rc, res
def mutant(name, rel, old, new, files=FILES):
    p = VC+'/'+rel; b = open(p,'rb').read(); s0 = sha(p); t = b.decode()
    n = t.count(old); assert n == 1, f'{name}: anchor count {n}'
    try:
        open(p,'w').write(t.replace(old,new)); assert new in open(p).read() and sha(p)!=s0, f'{name}: mutant did not land'
        rc, res = vitest(files, 'mut_'+name)
    finally:
        open(p,'wb').write(b); assert sha(p)==s0, f'{name}: restore failed'
    return rc, res
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'head':
        rc, res = vitest(FILES, 'head_json'); json.dump(res, open(G+'/evidence/head_cells.json','w'), indent=1); print(rc, summary(res))
    elif mode == 'base':
        rc, res = mode_base(); json.dump(res, open(G+'/evidence/base_cells.json','w'), indent=1); print(rc, summary(res))

# ---- real-PG probe driver (appended) ----
import shutil, contextlib
PROBE_SRC = G + '/scripts/gate66-realpg.probe.test.ts'
PROBE_DST = VC + '/src/__tests__/gate66-realpg.probe.test.ts'
QUAR = G + '/tmp/_quarantine_2026-11-01'
_q = [0]
def probe(tag, db):
    out = f'{G}/evidence/realpg_{tag}_{db}.jsonl'
    open(out, 'w').close()
    shutil.copy(PROBE_SRC, PROBE_DST)
    try:
        env = dict(os.environ, TMPDIR=G+'/tmp', G66_DB=f'postgres://vcapp:vcapp@127.0.0.1:55466/{db}', G66_OUT=out)
        p = subprocess.run(['nice','-n','10', D+'/node_modules/.bin/vitest','run','--root',VC,'--maxWorkers=1',
                            '--reporter=json','--outputFile='+G+f'/tmp/realpg_{tag}_{db}.json', 'src/__tests__/gate66-realpg.probe.test.ts'],
                           cwd=VC, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        open(f'{G}/evidence/realpg_{tag}_{db}.log','w').write(p.stdout)
        j = json.load(open(G+f'/tmp/realpg_{tag}_{db}.json'))
        st = {}
        for f in j['testResults']:
            for a in f['assertionResults']: st[a['fullName']] = a['status']
        return p.returncode, st
    finally:
        os.makedirs(QUAR, exist_ok=True); _q[0] += 1
        shutil.move(PROBE_DST, f'{QUAR}/probe_{tag}_{db}_{_q[0]}.ts')
@contextlib.contextmanager
def swapped(edits):
    """edits: list of (rel, old, new) unique-anchor replacements, or (rel, None, bytes) whole-file."""
    saved = {}
    try:
        for rel, old, new in edits:
            p = VC+'/'+rel
            if p not in saved: saved[p] = (open(p,'rb').read(), sha(p))
            t = open(p,'rb').read()
            if old is None: open(p,'wb').write(new)
            else:
                s = t.decode(); n = s.count(old); assert n == 1, f'anchor count {n} in {rel}: {old[:60]}'
                open(p,'w').write(s.replace(old, new)); assert new in open(p).read()
            assert sha(p) != saved[p][1], f'edit did not land {rel}'
        yield
    finally:
        for p,(b,h) in saved.items():
            open(p,'wb').write(b); assert sha(p) == h, f'restore failed {p}'
