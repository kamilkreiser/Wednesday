#!/usr/bin/env python3
"""drafter_setup_parse_1030.py — #1030 drafter (KS-1211 PR-3b, vitest / @vitest/mocker -> 4.1.11). READ-ONLY git on the Secuura checkout
(ls-remote, rev-list, rev-parse, show, diff, ls-tree, merge-base, status, for-each-ref); every WRITE verb (clone, worktree add,
merge-tree --write-tree) only inside the drafter's OWN clone under gate1030/scratch/. Never cd; cwd for every subprocess is the scratch dir.
Parts: A readings + shape; B merge proofs (566107f01 brought only develop 20ab16f9a; the head over CURRENT develop); C blob table for the
launcher; D per-lock parse (27 locks) merge-base vs head, flag classes, runtime (--omit=dev) set equality, planted controls;
E manifests (exactly 2 range lines); F baseline 32 -> 31 with a planted control; G census of vitest/mocker in all tracked locks at head."""
import datetime, hashlib, json, os, re, subprocess, sys, tempfile
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = 'e43af493418a1f13cfb60c994380fb74d79ad07e'
MERGE = '566107f019e6cc05b6b4b5a7d62122a3f9772c80'
CHANGE = '17cbb10919854658a40a07fc3e5fdafdd1e82e08'
CPARENT = '19f1e54750ce2b65312a687add2db4f5628edb7d'
BASE = '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb'   # develop merged in = merge-base
D = 'Blockchain/Dev/'
os.makedirs(G + '/scratch', exist_ok=True)
SCR = tempfile.mkdtemp(prefix='gate1030_draft_', dir=G + '/scratch')
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(args, check=True, cwd=None):
    p = subprocess.run(args, cwd=cwd or SCR, capture_output=True, text=True)
    if check and p.returncode != 0: print('FAILED rc', p.returncode, args, p.stderr[-800:]); sys.exit(1)
    return p
def g(*a): return run(['git', '-C', REPO] + list(a)).stdout.strip()
def gq(*a):
    p = run(['git', '-C', REPO] + list(a), check=False); return p.stdout.strip() if p.returncode == 0 else None
def readings(tag):
    por = len([l for l in g('status', '--porcelain').splitlines() if l.strip()])
    cfg = hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16]
    refs = len(g('for-each-ref').splitlines()); wts = len(os.listdir(REPO + '/.git/worktrees'))
    print('CHECKOUT %s %s: porcelain %d | .git/config sha256 %s | refs %d | .git/worktrees %d' % (tag, now(), por, cfg, refs, wts))
print('drafter_setup_parse_1030 start', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| scratch', SCR)
readings('start')
LSR = g('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1030/head', 'refs/heads/feature/ks-1211-bump-vitest')
print(LSR)
CURDEV = [l.split()[0] for l in LSR.splitlines() if l.endswith('refs/heads/develop')][0]
print('A head parents:', g('rev-list', '--parents', '-n1', HEAD))
print('A merge parents:', g('rev-list', '--parents', '-n1', MERGE))
print('A change parents:', g('rev-list', '--parents', '-n1', CHANGE))
print('A develop %s parents: %s' % (CURDEV[:9], g('rev-list', '--parents', '-n1', CURDEV)))
print('A merge-base head curdev:', g('merge-base', HEAD, CURDEV), '| merge-base head BASE:', g('merge-base', HEAD, BASE))
three = g('diff', '--name-only', CURDEV + '...' + HEAD).splitlines()
print('A three-dot curdev...head files:', len(three), '| -w numstat identical:', g('diff', '--numstat', CURDEV + '...' + HEAD) == g('diff', '-w', '--numstat', CURDEV + '...' + HEAD))
locks = [f for f in three if f.endswith('package-lock.json')]; mans = [f for f in three if f.endswith('package.json')]; other = [f for f in three if f not in locks and f not in mans]
print('A locks %d | manifests %d | other %s' % (len(locks), len(mans), other))
print('A commit files: change %d | merge-vs-change %d | head-vs-merge %s' % (len(g('diff', '--name-only', CPARENT, CHANGE).splitlines()), len(g('diff', '--name-only', CHANGE, MERGE).splitlines()), g('diff', '--name-only', MERGE, HEAD).splitlines()))
print('A develop delta BASE..CURDEV files:', g('diff', '--name-only', BASE, CURDEV).splitlines(), '| overlap with the 43:', sorted(set(g('diff', '--name-only', BASE, CURDEV).splitlines()) & set(three)))
print('A develop delta 19f1e5475..BASE first-parent:'); print(g('log', '--oneline', '--first-parent', CPARENT + '..' + BASE))
# B merge proofs in OWN clone
C = SCR + '/clone'
run(['git', 'clone', '--shared', '--no-checkout', '-q', REPO, C])
def tree(s): return run(['git', '-C', C, 'rev-parse', s + '^{tree}']).stdout.strip()
def mt(a, b):
    p = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b], check=False)
    return p.returncode, p.stdout.strip().split('\n')[0], p.stdout.strip().split('\n')[1:]
rc, t, conf = mt(CHANGE, BASE)
print('B merge-tree(17cbb1091, 20ab16f9a) rc %d tree %s conflicts %s | 566107f01 tree %s | EQUAL %s' % (rc, t, conf, tree(MERGE), t == tree(MERGE)))
rc, t2, _ = mt(CHANGE, CPARENT)
print('B control merge-tree(17cbb1091, its own parent 19f1e5475) = 17cbb1091 tree?', t2 == tree(CHANGE))
mfiles = run(['git', '-C', C, 'diff', '--name-only', CHANGE, MERGE]).stdout.split()
dfiles = run(['git', '-C', C, 'diff', '--name-only', CPARENT, BASE]).stdout.split()
chg = run(['git', '-C', C, 'diff', '--name-only', CPARENT, CHANGE]).stdout.split()
print('B merge moved %d files | develop delta 19f1e5475..20ab16f9a %d files | equal sets %s | both-sides files %s' % (len(mfiles), len(dfiles), set(mfiles) == set(dfiles), sorted(set(mfiles) & set(chg))))
def pid(a, b, paths=None):
    d = run(['git', '-C', C, 'diff', a, b] + (['--'] + paths if paths else [])).stdout
    p = subprocess.run(['git', '-C', C, 'patch-id', '--stable'], input=d, capture_output=True, text=True)
    return (p.stdout.split() or ['EMPTY'])[0]
only_dev = [f for f in mfiles if f not in chg]
print('B merge moved (single-side files) patch-id %s == develop delta patch-id %s : %s' % (pid(CHANGE, MERGE, only_dev)[:12], pid(CPARENT, BASE, only_dev)[:12], pid(CHANGE, MERGE, only_dev) == pid(CPARENT, BASE, only_dev)))
print('B control patch-id of the change commit on those paths', pid(CPARENT, CHANGE, only_dev)[:12])
rc, t3, conf3 = mt(CURDEV, HEAD)
print('B merged tree over CURRENT develop %s: rc %d tree %s conflicts %s' % (CURDEV[:9], rc, t3, conf3))
dcur = run(['git', '-C', C, 'diff', '--name-only', HEAD, t3]).stdout.split()
print('B merged tree vs head tree: files %s (expect = develop delta BASE..CURDEV)' % dcur)
for name, sha in (('head', HEAD), ('base', BASE)):
    run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', SCR + '/wt_' + name, sha])
    print('worktree', name, run(['git', '-C', SCR + '/wt_' + name, 'rev-parse', 'HEAD']).stdout.strip()[:9])
json.dump({'SCR': SCR, 'C': C, 'wt_head': SCR + '/wt_head', 'wt_base': SCR + '/wt_base', 'HEAD': HEAD, 'BASE': BASE, 'CURDEV': CURDEV, 'merged_tree_curdev': t3}, open(G + '/drafter_paths.json', 'w'), indent=1)
# C blob table
AUD = [D + 'scripts/audit/' + x for x in ('audit-locks.mjs', 'audit-gate.mjs', 'lock-discovery.mjs', 'baseline-contract.mjs', 'package.json', 'package-lock.json')]
for f in sorted(three) + AUD:
    print('BLOB %s | base %s | head %s | curdev %s' % (f, gq('rev-parse', BASE + ':' + f), gq('rev-parse', HEAD + ':' + f), gq('rev-parse', CURDEV + ':' + f)))
print('BLOB scripts/audit tree | base %s | head %s | curdev %s' % (gq('rev-parse', BASE + ':' + D + 'scripts/audit'), gq('rev-parse', HEAD + ':' + D + 'scripts/audit'), gq('rev-parse', CURDEV + ':' + D + 'scripts/audit')))
# D per-lock parse
def lock_at(sha, path): return json.loads(run(['git', '-C', C, 'show', sha + ':' + path]).stdout)
def cls(v):
    if v is None: return 'ABSENT'
    return ','.join(f for f in ('dev', 'devOptional', 'optional', 'peer') if v.get(f)) or 'PROD'
def runtime(pk): return {k: (v.get('version'), v.get('integrity'), v.get('resolved'), v.get('link')) for k, v in pk.items() if k and not v.get('dev')}
FAM = re.compile(r'(^|/)node_modules/(vitest|@vitest/[^/]+)$')
union = {}
tot = {'bad': 0, 'other_nondev': 0, 'runtime_diff': 0}
for p in locks:
    a, b = lock_at(BASE, p), lock_at(HEAD, p)
    pa, pb = a['packages'], b['packages']
    changed = [k for k in sorted(set(pa) | set(pb)) if pa.get(k) != pb.get(k)]
    fam = [k for k in changed if FAM.search(k)]; oth = [k for k in changed if not FAM.search(k)]
    bad = [k for k in changed if k in pa and k in pb and cls(pa[k]) != cls(pb[k])]
    nondev = [(k, cls(pa.get(k)), cls(pb.get(k))) for k in changed if not ((pa.get(k) or {'dev': True}).get('dev') and (pb.get(k) or {'dev': True}).get('dev'))]
    oth_nd = [x for x in nondev if not FAM.search(x[0])]
    ra, rb = runtime(pa), runtime(pb)
    rdiff = sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))
    added = [k for k in changed if k not in pa]; removed = [k for k in changed if k not in pb]
    top = sorted(x for x in set(a) | set(b) if x != 'packages' and a.get(x) != b.get(x))
    tot['bad'] += len(bad); tot['other_nondev'] += len(oth_nd); tot['runtime_diff'] += len(rdiff)
    for k in changed:
        n = k.split('node_modules/')[-1]
        tr = '%s->%s' % ((pa.get(k) or {}).get('version', '-'), (pb.get(k) or {}).get('version', '-'))
        union.setdefault(n, {}).setdefault(tr, set()).add(p.replace(D, ''))
    famv = sorted({(k.split('node_modules/')[-1], (pa.get(k) or {}).get('version'), (pb.get(k) or {}).get('version'), cls(pb.get(k))) for k in fam})
    print('D %-44s entries %d->%d changed %d (added %d removed %d) | family %d | OTHER %d | class drift %d %s | nondev moved %s | RUNTIME(--omit=dev) set diff %d %s | top drift %s | packages[""] same %s' % (
        p.replace(D, ''), len(pa), len(pb), len(changed), len(added), len(removed), len(fam), len(oth), len(bad), bad[:3], nondev[:4], len(rdiff), rdiff[:4], top, pa.get('') == pb.get('')))
    print('D    family', famv)
print('D TOTAL class drift %d | OTHER non-dev moved %d | runtime-set diffs %d' % (tot['bad'], tot['other_nondev'], tot['runtime_diff']))
# planted controls
a, b = lock_at(BASE, D + 'services/auth/package-lock.json'), lock_at(HEAD, D + 'services/auth/package-lock.json')
k = next(x for x, v in b['packages'].items() if x and not v.get('dev') and x.endswith('node_modules/express'))
b2 = json.loads(json.dumps(b)); b2['packages'][k]['version'] = '0.0.0-planted'
print('D CONTROL planted prod version on auth', k, '-> runtime diff', sorted(x for x in set(runtime(a['packages'])) | set(runtime(b2['packages'])) if runtime(a['packages']).get(x) != runtime(b2['packages']).get(x)))
kd = next(x for x, v in b['packages'].items() if v.get('dev') and FAM.search(x))
b3 = json.loads(json.dumps(b)); b3['packages'][kd].pop('dev')
print('D CONTROL planted dev->PROD on auth', kd, '-> class', cls(a['packages'].get(kd)), '->', cls(b3['packages'][kd]), '| runtime diff', sorted(x for x in set(runtime(a['packages'])) | set(runtime(b3['packages'])) if runtime(a['packages']).get(x) != runtime(b3['packages']).get(x)))
print('D UNION of moves (name: transition -> lock count):')
for n in sorted(union):
    print('   %s: %s' % (n, {t: len(v) for t, v in sorted(union[n].items())}))
# vite / rolldown / lightningcss per lock, runtime flag
print('D vite/rolldown/lightningcss entries at head, by lock (key, base ver, head ver, head class):')
for p in locks:
    pa, pb = lock_at(BASE, p)['packages'], lock_at(HEAD, p)['packages']
    rows = [(k, (pa.get(k) or {}).get('version'), (pb.get(k) or {}).get('version'), cls(pb.get(k))) for k in sorted(set(pa) | set(pb)) if re.search(r'node_modules/(vite|rolldown|lightningcss)$', k)]
    if rows: print('   %-44s %s' % (p.replace(D, ''), rows))
# E manifests
for m in mans:
    d = run(['git', '-C', C, 'diff', '-U0', BASE, HEAD, '--', m]).stdout.splitlines()
    minus = [l for l in d if l.startswith('-') and not l.startswith('---')]; plus = [l for l in d if l.startswith('+') and not l.startswith('+++')]
    print('E %-48s -%d +%d | %s' % (m.replace(D, ''), len(minus), len(plus), [l.strip() for l in plus]))
ja, jb = lock_at(BASE, D + 'services/vc-issuer/package.json'), lock_at(HEAD, D + 'services/vc-issuer/package.json')
print('E vc-issuer manifest parse: keys moved', sorted((s, k) for s in set(ja) | set(jb) if isinstance(ja.get(s), dict) for k in set(ja.get(s, {})) | set(jb.get(s, {})) if ja.get(s, {}).get(k) != jb.get(s, {}).get(k)))
# F baseline
def bl(sha): return json.loads(run(['git', '-C', C, 'show', sha + ':' + D + 'scripts/audit/audit-baseline.json']).stdout)
ba, bb = bl(BASE), bl(HEAD)
def rows(x):
    acc = x.get('accepted'); return acc if isinstance(acc, dict) else {r.get('id') or r.get('ghsa'): r for r in acc}
ra, rb = rows(ba), rows(bb)
def bdiff(ra, rb): return sorted(set(ra) - set(rb)), sorted(set(rb) - set(ra)), sorted(k for k in set(ra) & set(rb) if ra[k] != rb[k])
rem, add, alt = bdiff(ra, rb)
print('F baseline base %d -> head %d | removed %s | added %s | altered %s | order kept %s | non-row keys same %s' % (len(ra), len(rb), rem, add, alt, [k for k in ra if k in rb] == list(rb), {k: v for k, v in ba.items() if k != 'accepted'} == {k: v for k, v in bb.items() if k != 'accepted'}))
for r in rem: print('F   removed row', r, json.dumps(ra[r])[:400])
rb2 = json.loads(json.dumps(rb)); kk = next(iter(rb2)); rb2[kk] = dict(rb2[kk], expires='2099-01-01')
print('F CONTROL planted expiry on', kk, '-> altered', bdiff(ra, rb2)[2])
cur = rows(bl(CURDEV)); print('F baseline at current develop == base:', cur == ra, len(cur))
raw = run(['git', '-C', C, 'show', HEAD + ':' + D + 'scripts/audit/audit-baseline.json']).stdout
print('F byte round-trip json.dumps(indent=2)+newline equal:', json.dumps(bb, indent=2, ensure_ascii=False) + '\n' == raw)
# G census vitest / @vitest/mocker in every tracked lock at head (semver compare done by the shipped semver in the audit script run)
all_locks = [x for x in g('ls-tree', '-r', '--name-only', HEAD).splitlines() if x.endswith('package-lock.json')]
cen = []
for p in all_locks:
    try: pk = lock_at(HEAD, p).get('packages', {})
    except Exception as e: print('G unparsable', p, type(e).__name__); continue
    hits = [(k, v.get('version'), cls(v)) for k, v in pk.items() if re.search(r'node_modules/(vitest|@vitest/mocker)$', k)]
    ctl = sum(1 for k in pk if k.endswith('node_modules/lodash'))
    cen.append((p, hits, ctl))
print('G tracked locks %d | with vitest/mocker %d | none %d | lodash control locks %d' % (len(all_locks), sum(1 for c in cen if c[1]), sum(1 for c in cen if not c[1]), sum(1 for c in cen if c[2])))
for p, hits, ctl in cen:
    if hits: print('G   %-52s %s' % (p, sorted(set((h[0].split('node_modules/')[-1], h[1], h[2]) for h in hits))))
print('G   none:', [p for p, h, c in cen if not h])
readings('end')
print('done', now())
