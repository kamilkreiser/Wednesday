#!/usr/bin/env python3
"""drafter_setup_1033.py — #1033 drafter (KS-763 PR-7, mysql2 override -> 3.23.1). READ-ONLY git on the Secuura checkout
(ls-remote, rev-list, rev-parse, show, diff, ls-tree, merge-base, status, for-each-ref); every WRITE verb (clone, worktree add,
merge-tree --write-tree) only inside the drafter's OWN clone under /private/tmp/claude-501/drafter1033/. Never cd.
Parts: A readings + shape; B merge proofs (2cab54988 brought only develop bb848b828; both-sides files by parse; head over CURRENT develop);
C blob table; D per-lock parse (root + originate) base vs head: moved entries, flag classes, --omit=dev set, declarer ranges both directions,
planted controls; E manifests by JSON parse; F baseline 31 -> 29 by parse + byte round-trip + planted control; G census of mysql2 in every
tracked lock at head (and base), with a positive control package."""
import datetime, hashlib, json, os, re, subprocess, sys, tempfile
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'; os.makedirs(OUT, exist_ok=True)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = '2cab54988b4e7b71d403576719f5fd80e470fa92'
CHANGE = '9fd3cb924e26a53a01d512462ce8b2c29f1ca6ee'
CPARENT = '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'
BASE = 'bb848b8283eb5ee6a6180067315b76f1321e7b6b'     # develop merged in by 2cab54988 = merge-base with current develop
D = 'Blockchain/Dev/'
ROOTLOCK, ORIGLOCK = D + 'package-lock.json', D + 'services/originate/package-lock.json'
BASEL = D + 'scripts/audit/audit-baseline.json'
TWO = ['GHSA-3f6p-5ww8-9rcr', 'GHSA-rgwj-5xj2-c3m3']
ROOT = '/private/tmp/claude-501/drafter1033'
os.makedirs(ROOT, exist_ok=True)
SCR = tempfile.mkdtemp(prefix='setup_', dir=ROOT)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(args, check=True, cwd=None, inp=None):
    p = subprocess.run(args, cwd=cwd or SCR, capture_output=True, text=True, input=inp)
    if check and p.returncode != 0: print('FAILED rc', p.returncode, args, p.stderr[-800:]); sys.exit(1)
    return p
def g(*a): return run(['git', '-C', REPO] + list(a)).stdout.strip()
def gq(*a):
    p = run(['git', '-C', REPO] + list(a), check=False); return p.stdout.strip() if p.returncode == 0 else None
def readings(tag):
    por = len([l for l in g('status', '--porcelain').splitlines() if l.strip()])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    refs = len(g('for-each-ref').splitlines()); wts = len(os.listdir(REPO + '/.git/worktrees'))
    print('CHECKOUT %s %s: porcelain %d | .git/config sha256 %s | refs %d | .git/worktrees %d | branch %s' % (tag, now(), por, cfg, refs, wts, g('rev-parse', '--abbrev-ref', 'HEAD')))
print('drafter_setup_1033 start', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| scratch', SCR, '| load %.1f/%.1f/%.1f' % os.getloadavg())
readings('start')
LSR = g('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1033/head', 'refs/heads/feature/ks-763-override-mysql2')
print(LSR)
CURDEV = [l.split()[0] for l in LSR.splitlines() if l.endswith('refs/heads/develop')][0]
PRH = [l.split()[0] for l in LSR.splitlines() if l.endswith('refs/pull/1033/head')][0]
if PRH != HEAD: print('STOP: refs/pull/1033/head moved to', PRH); sys.exit(2)
print('A head parents:', g('rev-list', '--parents', '-n1', HEAD))
print('A change parents:', g('rev-list', '--parents', '-n1', CHANGE))
print('A develop %s parents: %s | first-parent BASE..CURDEV: %s' % (CURDEV[:9], g('rev-list', '--parents', '-n1', CURDEV), g('log', '--oneline', '--first-parent', BASE + '..' + CURDEV).splitlines()))
print('A merge-base head curdev:', g('merge-base', HEAD, CURDEV), '| is BASE:', g('merge-base', HEAD, CURDEV) == BASE)
three = g('diff', '--name-only', CURDEV + '...' + HEAD).splitlines()
print('A three-dot curdev...head files %d: %s' % (len(three), three))
print('A numstat:', g('diff', '--numstat', CURDEV + '...' + HEAD).replace('\n', ' | '))
print('A change commit files:', g('diff', '--name-only', CPARENT, CHANGE).splitlines())
print('A develop delta BASE..CURDEV files:', g('diff', '--name-only', BASE, CURDEV).splitlines(), '| overlap with the PR paths:', sorted(set(g('diff', '--name-only', BASE, CURDEV).splitlines()) & set(three)))
print('A develop delta CPARENT..BASE first-parent:', g('log', '--oneline', '--first-parent', CPARENT + '..' + BASE).splitlines())
# B merge proofs in OWN clone
C = SCR + '/clone'
run(['git', 'clone', '--shared', '--no-checkout', '-q', REPO, C])
def tree(s): return run(['git', '-C', C, 'rev-parse', s + '^{tree}']).stdout.strip()
def mt(a, b):
    p = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b], check=False)
    lines = p.stdout.strip().split('\n'); return p.returncode, lines[0], lines[1:]
rc, t, conf = mt(CHANGE, BASE)
print('B merge-tree(9fd3cb924, bb848b828) rc %d tree %s conflicts %s | 2cab54988 tree %s | EQUAL %s' % (rc, t, conf, tree(HEAD), t == tree(HEAD)))
rc2, t2, _ = mt(CHANGE, CPARENT)
print('B control merge-tree(9fd3cb924, its own parent 75ad0e55c) = 9fd3cb924 tree?', t2 == tree(CHANGE))
mfiles = run(['git', '-C', C, 'diff', '--name-only', CHANGE, HEAD]).stdout.split()
dfiles = run(['git', '-C', C, 'diff', '--name-only', CPARENT, BASE]).stdout.split()
chg = run(['git', '-C', C, 'diff', '--name-only', CPARENT, CHANGE]).stdout.split()
both = sorted(set(dfiles) & set(chg))
print('B merge moved %d files | develop delta 75ad0e55c..bb848b828 %d files | merge-moved set == develop-delta set: %s | both-sides files %s' % (
    len(mfiles), len(dfiles), set(mfiles) == set(dfiles), both))
print('B merge-moved files not in develop delta:', sorted(set(mfiles) - set(dfiles)), '| develop delta files the merge did not move:', sorted(set(dfiles) - set(mfiles)))
def pid(a, b, paths):
    d = run(['git', '-C', C, 'diff', a, b, '--'] + paths).stdout
    p = subprocess.run(['git', '-C', C, 'patch-id', '--stable'], input=d, capture_output=True, text=True)
    return (p.stdout.split() or ['EMPTY'])[0]
only_dev = [f for f in dfiles if f not in chg]
print('B develop-only files (%d) patch-id merge %s == develop delta %s : %s | control (change commit on the both-sides files) %s' % (
    len(only_dev), pid(CHANGE, HEAD, only_dev)[:12], pid(CPARENT, BASE, only_dev)[:12], pid(CHANGE, HEAD, only_dev) == pid(CPARENT, BASE, only_dev), pid(CPARENT, CHANGE, both)[:12]))
def show(sha, p): return run(['git', '-C', C, 'show', sha + ':' + p]).stdout
def blob(sha, p): return run(['git', '-C', C, 'rev-parse', sha + ':' + p], check=False).stdout.strip()
mtree_blobs = {p: run(['git', '-C', C, 'rev-parse', t + ':' + p]).stdout.strip() for p in both}
for p in both: print('B both-sides %s: merge-tree blob %s == head blob %s : %s' % (p, mtree_blobs[p][:9], blob(HEAD, p)[:9], mtree_blobs[p] == blob(HEAD, p)))
def judge(a, d, c, m):
    bad, bth, nd, nc = [], [], 0, 0
    for k in sorted(set(a) | set(d) | set(c) | set(m)):
        dv, cv = d.get(k) != a.get(k), c.get(k) != a.get(k)
        if dv and cv:
            bth.append(k)
            continue
        want = d.get(k) if dv else (c.get(k) if cv else a.get(k))
        nd += dv; nc += cv
        if m.get(k) != want: bad.append(k)
    return bad, bth, nd, nc
a, dd, cc, mm = (json.loads(show(s, ROOTLOCK))['packages'] for s in (CPARENT, BASE, CHANGE, HEAD))
bad, bth, nd, nc = judge(a, dd, cc, mm)
print('B root lock per-entry: develop-side %d, change-side %d, BOTH-sides %s | merged entries != their changing side: %s' % (nd, nc, bth, bad))
m2 = json.loads(json.dumps(mm)); kx = next(x for x in dd if dd.get(x) != a.get(x)); m2[kx] = dict(m2[kx], version='0.0.0-planted')
print('B CONTROL planted version on develop-side root entry', kx, '-> reported', judge(a, dd, cc, m2)[0])
def blrows(sha): return json.loads(show(sha, BASEL))
ba, bd, bc, bm = (blrows(s) for s in (CPARENT, BASE, CHANGE, HEAD))
acc = lambda x: x['accepted']
bad, bth, nd, nc = judge(acc(ba), acc(bd), acc(bc), acc(bm))
print('B baseline per-row: develop-side %d, change-side %d, BOTH %s | merged rows != their changing side %s | develop removed %s | change removed %s' % (
    nd, nc, bth, bad, sorted(set(acc(ba)) - set(acc(bd))), sorted(set(acc(ba)) - set(acc(bc)))))
regen = json.loads(show(BASE, BASEL)); [regen['accepted'].pop(k) for k in TWO]
print('B baseline regeneration (develop bb848b828 minus the 2 rows, json.dumps indent=2 + newline) byte-equal to head blob:', json.dumps(regen, indent=2, ensure_ascii=False) + '\n' == show(HEAD, BASEL),
      '| control: develop blob itself equal to head:', show(BASE, BASEL) == show(HEAD, BASEL))
rc3, t3, conf3 = mt(CURDEV, HEAD)
dcur = run(['git', '-C', C, 'diff', '--name-only', HEAD, t3]).stdout.split()
print('B merged tree over CURRENT develop %s: rc %d tree %s conflicts %s | delta to head tree %s | develop delta BASE..CURDEV %s' % (CURDEV[:9], rc3, t3, conf3, dcur, run(['git', '-C', C, 'diff', '--name-only', BASE, CURDEV]).stdout.split()))
print('B merged tree vs CURDEV tree: %s' % run(['git', '-C', C, 'diff', '--name-only', CURDEV, t3]).stdout.split())
for name, sha in (('head', HEAD), ('base', BASE), ('change', CHANGE), ('cparent', CPARENT)):
    run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', SCR + '/wt_' + name, sha])
    print('worktree', name, run(['git', '-C', SCR + '/wt_' + name, 'rev-parse', 'HEAD']).stdout.strip()[:9])
json.dump({'SCR': SCR, 'C': C, 'HEAD': HEAD, 'BASE': BASE, 'CHANGE': CHANGE, 'CPARENT': CPARENT, 'CURDEV': CURDEV, 'merged_tree_curdev': t3, 'head_tree': tree(HEAD)}, open(OUT + '/drafter_paths.json', 'w'), indent=1)
# C blob table
audit = [x.split('\t')[1] for x in run(['git', '-C', C, 'ls-tree', BASE, D + 'scripts/audit/']).stdout.splitlines() if x.split()[1] == 'blob']
for f in sorted(three) + audit + [D + 'services/originate/Dockerfile', D + 'prisma/schema.prisma']:
    print('BLOB %s | cparent %s | base %s | change %s | head %s | curdev %s' % (f, (blob(CPARENT, f) or '-')[:9], (blob(BASE, f) or '-')[:9], (blob(CHANGE, f) or '-')[:9], (blob(HEAD, f) or '-')[:9], (blob(CURDEV, f) or '-')[:9]))
print('BLOB scripts/audit tree | base %s | head %s | curdev %s' % (blob(BASE, D + 'scripts/audit'), blob(HEAD, D + 'scripts/audit'), blob(CURDEV, D + 'scripts/audit')))
# D per-lock parse
def cls(v):
    if v is None: return 'ABSENT'
    return ','.join(f for f in ('dev', 'devOptional', 'optional', 'peer') if v.get(f)) or 'PROD'
def runtime(pk): return {k: (v.get('version'), v.get('integrity'), v.get('resolved'), v.get('link')) for k, v in pk.items() if k and not v.get('dev')}
SUB = re.compile(r'(^|/)node_modules/(mysql2|sql-escaper|seq-queue|sqlstring)(/|$)')
sys.path.insert(0, GS)
for p in (ROOTLOCK, ORIGLOCK):
    A, Bh = json.loads(show(BASE, p)), json.loads(show(HEAD, p))
    pa, pb = A['packages'], Bh['packages']
    changed = [k for k in sorted(set(pa) | set(pb)) if pa.get(k) != pb.get(k)]
    out_scope = [k for k in changed if not SUB.search(k) and k != '']
    drift = [(k, cls(pa.get(k)), cls(pb.get(k))) for k in changed if k in pa and k in pb and cls(pa[k]) != cls(pb[k])]
    ra, rb = runtime(pa), runtime(pb)
    rdiff = sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))
    top = sorted(x for x in set(A) | set(Bh) if x != 'packages' and A.get(x) != Bh.get(x))
    print('D %s entries %d->%d | changed %d: %s' % (p.replace(D, '') or 'root', len(pa), len(pb), len(changed), [(k, cls(pa.get(k)), (pa.get(k) or {}).get('version'), cls(pb.get(k)), (pb.get(k) or {}).get('version')) for k in changed]))
    print('D    out-of-mysql2-subtree changed (excluding packages[""]) %s | class drift %s | --omit=dev set diff %s | top-level key drift %s' % (out_scope, drift, rdiff, top))
    if '' in changed:
        x, y = pa[''], pb['']
        print('D    packages[""] fields moved:', sorted(f for f in set(x) | set(y) if x.get(f) != y.get(f)))
    for k in changed:
        if k and k in pa and k in pb:
            print('D    %s fields moved: %s' % (k, sorted(f for f in set(pa[k]) | set(pb[k]) if pa[k].get(f) != pb[k].get(f))))
    # declarer ranges, both directions, with npm's semver from the head worktree's scripts/audit (installed by drafter_audit) or a fallback
    edges = []
    moved = [k for k in changed if k and k in pb]
    names = {k.split('node_modules/')[-1]: k for k in moved}
    for dk, dv in pb.items():
        for sect in ('dependencies', 'optionalDependencies', 'peerDependencies'):
            for n, rng in (dv.get(sect) or {}).items():
                if n in names: edges.append(('declarer', dk or '<root>', sect, n, rng, pb[names[n]].get('version')))
    for mk in moved:
        for sect in ('dependencies', 'optionalDependencies', 'peerDependencies'):
            for n, rng in (pb[mk].get(sect) or {}).items():
                base_dir = mk
                cand = None
                while True:
                    k2 = (base_dir + '/node_modules/' + n) if base_dir else ('node_modules/' + n)
                    if k2 in pb: cand = k2; break
                    if 'node_modules/' not in base_dir: break
                    base_dir = base_dir.rsplit('/node_modules/', 1)[0] if '/node_modules/' in base_dir else ''
                edges.append(('own-dep', mk, sect, n, rng, (pb.get(cand) or {}).get('version') if cand else None))
    json.dump(edges, open(OUT + '/edges_%s.json' % ('root' if p == ROOTLOCK else 'originate'), 'w'), indent=1)
    print('D    edges to evaluate (declarer + own-dep): %d -> out/edges_%s.json' % (len(edges), 'root' if p == ROOTLOCK else 'originate'))
# planted controls on the parse instrument
A, Bh = json.loads(show(BASE, ORIGLOCK)), json.loads(show(HEAD, ORIGLOCK))
b2 = json.loads(json.dumps(Bh)); b2['packages']['node_modules/express']['version'] = '0.0.0-planted'
ch2 = [k for k in set(A['packages']) | set(b2['packages']) if A['packages'].get(k) != b2['packages'].get(k) and not SUB.search(k) and k]
print('D CONTROL planted out-of-scope version on originate node_modules/express -> out-of-subtree changed', ch2)
b3 = json.loads(json.dumps(Bh)); b3['packages']['node_modules/mysql2'].pop('devOptional'); b3['packages']['node_modules/mysql2']['dev'] = True
print('D CONTROL planted devOptional->dev on originate node_modules/mysql2 -> class', cls(A['packages']['node_modules/mysql2']), '->', cls(b3['packages']['node_modules/mysql2']),
      '| --omit=dev diff', sorted(k for k in set(runtime(A['packages'])) | set(runtime(b3['packages'])) if runtime(A['packages']).get(k) != runtime(b3['packages']).get(k)))
# E manifests
for m in (D + 'package.json', D + 'services/originate/package.json'):
    ja, jb = json.loads(show(BASE, m)), json.loads(show(HEAD, m))
    moved = []
    for k in sorted(set(ja) | set(jb)):
        if ja.get(k) == jb.get(k): continue
        if isinstance(ja.get(k), dict) and isinstance(jb.get(k), dict):
            for k2 in sorted(set(ja[k]) | set(jb[k])):
                if ja[k].get(k2) != jb[k].get(k2): moved.append((k, k2, ja[k].get(k2), jb[k].get(k2)))
        else: moved.append((k, ja.get(k), jb.get(k)))
    dl = run(['git', '-C', C, 'diff', '-U0', BASE, HEAD, '--', m]).stdout.splitlines()
    print('E %s parse moved %s | diff lines -%d +%d' % (m.replace(D, '') or 'root', moved, sum(1 for l in dl if l.startswith('-') and not l.startswith('---')), sum(1 for l in dl if l.startswith('+') and not l.startswith('+++'))))
# F baseline
ra, rb = acc(json.loads(show(BASE, BASEL))), acc(json.loads(show(HEAD, BASEL)))
def bdiff(x, y): return sorted(set(x) - set(y)), sorted(set(y) - set(x)), sorted(k for k in set(x) & set(y) if x[k] != y[k])
rem, add, alt = bdiff(ra, rb)
print('F baseline base %d -> head %d | removed %s | added %s | altered %s | order kept %s | non-row keys same %s | removed == the 2: %s' % (
    len(ra), len(rb), rem, add, alt, [k for k in ra if k in rb] == list(rb), {k: v for k, v in json.loads(show(BASE, BASEL)).items() if k != 'accepted'} == {k: v for k, v in json.loads(show(HEAD, BASEL)).items() if k != 'accepted'}, rem == sorted(TWO)))
for r in rem: print('F   removed row', r, 'package', ra[r].get('package'), 'ticket', ra[r].get('ticket'), 'expires', ra[r].get('expires'))
rb2 = json.loads(json.dumps(rb)); kk = next(iter(rb2)); rb2[kk] = dict(rb2[kk], expires='2099-01-01')
print('F CONTROL planted expiry on', kk, '-> altered', bdiff(ra, rb2)[2])
print('F baseline at current develop == base:', show(CURDEV, BASEL) == show(BASE, BASEL))
# G census mysql2 in every tracked lock at head and base
for tag, sha in (('head', HEAD), ('base', BASE), ('curdev', CURDEV)):
    all_locks = [x for x in run(['git', '-C', C, 'ls-tree', '-r', '--name-only', sha]).stdout.splitlines() if x.endswith('package-lock.json')]
    hits, ctl = [], 0
    for p in all_locks:
        try: pk = json.loads(show(sha, p)).get('packages', {})
        except Exception as e: print('G unparsable', p, type(e).__name__); continue
        h = sorted((k, v.get('version'), cls(v)) for k, v in pk.items() if re.search(r'(^|/)node_modules/mysql2$', k))
        if any(k.endswith('node_modules/express') for k in pk): ctl += 1
        if h: hits.append((p, h))
    print('G %s tracked locks %d | carrying mysql2 %d: %s | positive control: locks carrying express %d' % (tag, len(all_locks), len(hits), hits, ctl))
# Dockerfiles that could install either lock
dfs = [x for x in run(['git', '-C', C, 'ls-tree', '-r', '--name-only', HEAD]).stdout.splitlines() if re.search(r'(^|/)Dockerfile[^/]*$', x)]
print('G Dockerfiles tracked at head:', len(dfs))
for f in dfs:
    txt = show(HEAD, f)
    cp = [l.strip() for l in txt.splitlines() if re.match(r'\s*COPY\s', l) and 'package' in l]
    if any(('originate' in l) or re.search(r'COPY\s+(\./)?package(-lock)?\*?\.json', l) or 'Blockchain/Dev/package' in l for l in cp): print('G   %s copies: %s' % (f, cp))
readings('end')
print('done', now())
