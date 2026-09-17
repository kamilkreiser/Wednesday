#!/usr/bin/env python3
"""drafter_setup_parse.py — #1027 drafter (KS-1211 js-yaml + baseline-browser-mapping). READ-ONLY git on the Secuura checkout
(ls-remote, rev-parse, cat-file, diff, ls-tree, merge-base); every WRITE verb (clone, worktree add, merge-tree --write-tree) only inside
the drafter's OWN mktemp -d clone. Never cd; cwd for every subprocess is the scratch dir.
Parts: A readings + shape; B merge-commit proof; C blob table (for the launcher JUDGED list); D per-lock parse develop vs head with a
planted control; E js-yaml / bbm census in EVERY tracked lock at head (flags); F baseline diff with a planted control; G source importers."""
import datetime, hashlib, json, os, re, subprocess, sys, tempfile
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = 'd7fc6cc5582b918c0773ec6f25f86407de6f86ab'
CHANGE = 'b51ed77e18413301a0498d6845e77043b22530b1'
CPARENT = 'efaaa6034f036dd9538ee35b189217b1d08b90a9'
DEV = '19f1e54750ce2b65312a687add2db4f5628edb7d'
D = 'Blockchain/Dev/'
LOCKS = ['frontend/admin', 'frontend/issuer', 'frontend/outlook-addin', 'frontend/verifier', 'services/governance', 'services/originate',
         'services/referral', 'services/vc-issuer', '']
os.makedirs('/private/tmp/claude-501', exist_ok=True)
SCR = tempfile.mkdtemp(prefix='drafter1027.', dir='/private/tmp/claude-501')
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
print('scratch', SCR)
readings('start')
print(g('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1027/head', 'refs/heads/feature/ks-1211-bump-jsyaml-bbm'))
# A shape
print('A head parents:', g('rev-list', '--parents', '-n1', HEAD))
print('A change parents:', g('rev-list', '--parents', '-n1', CHANGE))
print('A merge-base head develop:', g('merge-base', HEAD, DEV), '| merge-base change develop:', g('merge-base', CHANGE, DEV))
print('A is efaaa6034 ancestor of develop:', run(['git', '-C', REPO, 'merge-base', '--is-ancestor', CPARENT, DEV], check=False).returncode == 0)
print('A three-dot develop...head numstat:'); print(g('diff', '--numstat', DEV + '...' + HEAD))
print('A -w numstat identical:', g('diff', '--numstat', DEV + '...' + HEAD) == g('diff', '-w', '--numstat', DEV + '...' + HEAD))
print('A change commit files (efaaa6034..b51ed77e1):'); print(g('diff', '--name-status', CPARENT, CHANGE))
print('A develop delta efaaa6034..19f1e5475 commits:'); print(g('log', '--oneline', '--first-parent', CPARENT + '..' + DEV))
# B merge commit brought only develop
os.makedirs(SCR, exist_ok=True)
C = SCR + '/repo'
run(['git', 'clone', '--shared', '--no-checkout', '-q', REPO, C])
for s in (HEAD, CHANGE, CPARENT, DEV): run(['git', '-C', C, 'cat-file', '-e', s + '^{commit}'])
def tree(s): return run(['git', '-C', C, 'rev-parse', s + '^{tree}']).stdout.strip()
def mt(a, b):
    p = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', a, b], check=False)
    return p.returncode, p.stdout.strip().replace('\n', ' || ')
rc, t = mt(DEV, CHANGE)
print('B merge-tree develop + b51ed77e1: rc %d tree %s | d7fc6cc55 tree %s | EQUAL (no hand edit in the merge) %s' % (rc, t, tree(HEAD), t.split(' ')[0] == tree(HEAD)))
rc2, t2 = mt(DEV, CPARENT)
print('B control: merge-tree develop + efaaa6034 (change parent) = develop tree?', t2.split(' ')[0] == tree(DEV), '| develop tree', tree(DEV))
m_files = set(run(['git', '-C', C, 'diff', '--name-only', CHANGE, HEAD]).stdout.split())
d_files = set(run(['git', '-C', C, 'diff', '--name-only', CPARENT, DEV]).stdout.split())
chg = set(run(['git', '-C', C, 'diff', '--name-only', CPARENT, CHANGE]).stdout.split())
print('B files moved by the merge (b51..d7f): %d | develop delta (efaaa..19f): %d | equal sets %s | overlap with change files %s' % (len(m_files), len(d_files), m_files == d_files, sorted(m_files & chg)))
bad = []
for f in sorted(m_files):
    bh = gq('rev-parse', HEAD + ':' + f); bd = gq('rev-parse', DEV + ':' + f)
    if bh != bd: bad.append(f)
print('B every merge-moved file at head == its develop blob:', not bad, bad[:5])
three = set(run(['git', '-C', C, 'diff', '--name-only', DEV + '...' + HEAD]).stdout.split())
print('B three-dot files == change-commit files:', three == chg, len(three))
for f in sorted(chg): print('B  change blob == head blob', f.replace(D, ''), gq('rev-parse', CHANGE + ':' + f) == gq('rev-parse', HEAD + ':' + f))
# worktrees for later probes
for name, sha in (('head', HEAD), ('develop', DEV)):
    run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', SCR + '/wt-' + name, sha])
    print('worktree', name, run(['git', '-C', SCR + '/wt-' + name, 'rev-parse', 'HEAD']).stdout.strip()[:9])
rc3, t3 = mt(DEV, HEAD)
print('B merged tree develop + head: rc %d %s | = head tree %s' % (rc3, t3, t3.split(' ')[0] == tree(HEAD)))
open('/private/tmp/claude-501/drafter1027.CLONE_PATH', 'w').write(SCR + '\n')
# C blob table
F = [D + 'scripts/audit/' + x for x in ('audit-baseline.json', 'audit-gate.mjs', 'audit-locks.mjs', 'lock-discovery.mjs', 'baseline-contract.mjs', 'package.json', 'package-lock.json')]
for l in LOCKS:
    F += [D + (l + '/' if l else '') + 'package-lock.json', D + (l + '/' if l else '') + 'package.json']
F += [D + 'scripts/preflight/preflight.sh', D + 'scripts/preflight/lockfile-cleanroom.sh', '.githooks/pre-push', D + 'packages/shared/package-lock.json']
mob = [x for x in g('ls-tree', '-r', '--name-only', HEAD).splitlines() if x.endswith('package-lock.json') and '/mobile/' in x]
F += mob
for f in F:
    print('BLOB', f, '| develop', gq('rev-parse', DEV + ':' + f), '| head', gq('rev-parse', HEAD + ':' + f), '| efaaa', (gq('rev-parse', CPARENT + ':' + f) or 'ABSENT')[:9])
# D parse
def lock_at(sha, path):
    return json.loads(run(['git', '-C', C, 'show', sha + ':' + path]).stdout)
def diff_lock(a, b):
    pa, pb = a['packages'], b['packages']
    ch = {}
    for k in sorted(set(pa) | set(pb)):
        if pa.get(k) != pb.get(k):
            fa, fb = pa.get(k) or {}, pb.get(k) or {}
            ch[k] = sorted(x for x in set(fa) | set(fb) if fa.get(x) != fb.get(x)) if k in pa and k in pb else ('ADDED' if k not in pa else 'REMOVED')
    top = sorted(x for x in set(a) | set(b) if x != 'packages' and a.get(x) != b.get(x))
    return ch, top, len(pa), len(pb)
FAM = re.compile(r'(^|/)node_modules/(js-yaml|baseline-browser-mapping)$')
total_other = 0
for l in LOCKS:
    p = D + (l + '/' if l else '') + 'package-lock.json'
    a, b = lock_at(DEV, p), lock_at(HEAD, p)
    ch, top, na, nb = diff_lock(a, b)
    other = [k for k in ch if not FAM.search(k)]
    total_other += len(other)
    print('D lock %-24s entries %d=%d | changed %d | family %s | OTHER %s | top-level drift %s | packages[""] same %s' % (l or 'ROOT', na, nb, len(ch),
          {k: (ch[k], (a['packages'].get(k) or {}).get('version'), (b['packages'].get(k) or {}).get('version'),
               {f: b['packages'].get(k, {}).get(f) for f in ('dev', 'devOptional', 'optional', 'peer') if f in b['packages'].get(k, {})}) for k in ch if FAM.search(k)},
          other[:6], top, a['packages'].get('') == b['packages'].get('')))
print('D OTHER total across 9 locks:', total_other)
# planted control on the root lock
a, b = lock_at(DEV, D + 'package-lock.json'), lock_at(HEAD, D + 'package-lock.json')
k = next(x for x in b['packages'] if x.endswith('node_modules/semver'))
b['packages'][k] = dict(b['packages'][k], version='0.0.0-planted')
ch, top, _, _ = diff_lock(a, b)
print('D CONTROL planted version on', k, '-> OTHER', [x for x in ch if not FAM.search(x)])
# E census in every tracked lock at head
all_locks = [x for x in g('ls-tree', '-r', '--name-only', HEAD).splitlines() if x.endswith('package-lock.json')]
cen = {'js-yaml': [], 'baseline-browser-mapping': [], 'express': []}
for p in all_locks:
    try: pk = lock_at(HEAD, p).get('packages', {})
    except Exception as e: print('E unparsable', p, type(e).__name__); continue
    for key, v in pk.items():
        for name in cen:
            if key.endswith('node_modules/' + name):
                cen[name].append((p.replace(D, ''), key, v.get('version'), ','.join(f for f in ('dev', 'devOptional', 'optional', 'peer') if v.get(f)) or 'PROD'))
print('E tracked locks at head:', len(all_locks), '| control express entries', len(cen['express']))
for name in ('js-yaml', 'baseline-browser-mapping'):
    print('E %s entries %d | non-dev (PROD/devOptional/optional) %d' % (name, len(cen[name]), sum(1 for x in cen[name] if x[3] != 'dev')))
    for x in cen[name]: print('E   ', name, x)
# declarers of js-yaml in the touched locks (who pulls it in)
for l in LOCKS:
    p = D + (l + '/' if l else '') + 'package-lock.json'
    pk = lock_at(HEAD, p)['packages']
    decl = sorted((k.split('node_modules/')[-1], (v.get('dependencies') or {}).get(n) or (v.get('devDependencies') or {}).get(n) or (v.get('peerDependencies') or {}).get(n), n)
                  for k, v in pk.items() for n in ('js-yaml', 'baseline-browser-mapping')
                  if n in (v.get('dependencies') or {}) or n in (v.get('devDependencies') or {}) or n in (v.get('peerDependencies') or {}))
    print('E declarers', l or 'ROOT', decl)
# F baseline
def bl(sha): return json.loads(run(['git', '-C', C, 'show', sha + ':' + D + 'scripts/audit/audit-baseline.json']).stdout)
ba, bb = bl(DEV), bl(HEAD)
def rows(x):
    acc = x.get('accepted')
    return acc if isinstance(acc, dict) else {r.get('id') or r.get('ghsa'): r for r in acc}
ra, rb = rows(ba), rows(bb)
def bdiff(ra, rb):
    return sorted(set(ra) - set(rb)), sorted(set(rb) - set(ra)), sorted(k for k in set(ra) & set(rb) if ra[k] != rb[k])
rem, add, alt = bdiff(ra, rb)
print('F baseline develop %d -> head %d | removed %s | added %s | altered %s | order kept %s | non-row keys same %s' % (len(ra), len(rb), rem, add, alt,
      [k for k in ra if k in rb] == list(rb), {k: v for k, v in ba.items() if k != 'accepted'} == {k: v for k, v in bb.items() if k != 'accepted'}))
for r in rem: print('F   removed row', r, json.dumps(ra[r])[:300])
rb2 = json.loads(json.dumps(rb)); kk = next(iter(rb2)); rb2[kk] = dict(rb2[kk], expires='2099-01-01') if isinstance(rb2[kk], dict) else rb2[kk]
print('F CONTROL planted alteration on', kk, '-> altered', bdiff(ra, rb2)[2])
raw = run(['git', '-C', C, 'show', HEAD + ':' + D + 'scripts/audit/audit-baseline.json']).stdout
print('F byte round-trip json.dumps(indent=2, ensure_ascii=False)+newline equal:', json.dumps(bb, indent=2, ensure_ascii=False) + '\n' == raw)
# G source importers of js-yaml / yaml in shipped source (git grep, read-only)
for pat in ("js-yaml", "from 'yaml'", 'require("yaml")', "require('yaml')", 'baseline-browser-mapping', 'express'):
    p = run(['git', '-C', REPO, 'grep', '-l', '-F', pat, HEAD, '--', D + 'services/governance/src', D + 'services/originate/src', D + 'services/referral/src',
             D + 'services/vc-issuer/src', D + 'packages/shared/src', D + 'frontend/admin/src', D + 'frontend/issuer/src', D + 'frontend/outlook-addin/src', D + 'frontend/verifier/src'], check=False)
    hits = [x.split(':', 1)[1] for x in p.stdout.splitlines()]
    print('G source files containing %r: %d %s' % (pat, len(hits), [h.replace(D, '') for h in hits[:6]]))
readings('close')
print('done', now())
