#!/usr/bin/env python3
"""drafter_repin.py — #1022 RE-PIN to head ff49d0242 (merge of develop 81ee4b729 = #1021 into 58684e653).
READ-ONLY git on the Secuura checkout; worktrees + merge-tree only in the drafter's OWN clone. Re-derives what the move could affect:
 (1) shape: parents, tree, three-dot files vs the new develop, merge-tree over the new develop;
 (2) blob identity of every launcher-judged file between develop 581c9db0d and 81ee4b729, and of the 4 PR files between 58684e653 and ff49d0242;
 (3) parse: the 3 locks vs 58684e653 (identity) and vs develop 81ee4b729 (hono-only / 12 ruled flags), baseline 34 rows conservation;
 (4) the shipped gates at the new head: H1 real (34), H2 develop 81ee4b729 baseline (37), B0 develop real, B1 develop locks + head baseline;
 (5) GitHub compare + Linear attachments. Secrets by NAME, never printed."""
import copy, datetime, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
CLD = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip(); C = CLD + '/repo'
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out_repin'; os.makedirs(OUT, exist_ok=True)
NEW = 'ff49d0242a8ae764155d427232b15647c6bfa849'; OLD = '58684e6534b4d420c9fb9ea246d3a32c70c70828'
DEV2 = '81ee4b729e86a645fc9098aafa1aaf39035a9950'; DEV1 = '581c9db0db4201c42cbbf702f339b750989acdb1'; BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'
D = 'Blockchain/Dev/'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(args, cwd=CLD, check=True, env=None, timeout=400):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env, timeout=timeout)
    if check and p.returncode: print('FAILED', args, p.returncode, p.stderr[-600:]); sys.exit(1)
    return p
def g(*a): return run(['git', '-C', C] + list(a)).stdout.strip()
def gr(*a): return run(['git', '-C', REPO] + list(a)).stdout.strip()
print('start', now())
print(gr('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1022/head', 'refs/heads/feature/ks-1211-bump-hono'))
por = len([l for l in gr('status', '--porcelain').splitlines() if l.strip()])
print('CHECKOUT porcelain %d | .git/config sha256 %s | refs %d | worktrees %d' % (por, hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16], len(gr('for-each-ref').splitlines()), len(os.listdir(REPO + '/.git/worktrees'))))
for s in (NEW, DEV2): run(['git', '-C', C, 'cat-file', '-e', s + '^{commit}'])
print('(1) new head parents:', g('rev-list', '--parents', '-n1', NEW), '| tree', g('rev-parse', NEW + '^{tree}'))
print('    develop2 parents:', g('rev-list', '--parents', '-n1', DEV2), '| subject:', g('log', '-1', '--format=%s', DEV2))
print('    DEV1 ancestor of DEV2:', run(['git', '-C', C, 'merge-base', '--is-ancestor', DEV1, DEV2], check=False).returncode == 0,
      '| DEV2 ancestor of NEW:', run(['git', '-C', C, 'merge-base', '--is-ancestor', DEV2, NEW], check=False).returncode == 0)
print('    develop delta DEV1..DEV2:'); print('      ' + g('diff', '--numstat', DEV1, DEV2).replace('\n', '\n      '))
print('    three-dot DEV2...NEW:'); print('      ' + g('diff', '--numstat', DEV2 + '...' + NEW).replace('\n', '\n      '))
print('    OLD..NEW (what the merge commit brought):'); print('      ' + g('diff', '--name-only', OLD, NEW).replace('\n', '\n      '))
mt = run(['git', '-C', C, 'merge-tree', '--write-tree', DEV2, NEW], check=False)
print('    merge-tree DEV2 + NEW rc', mt.returncode, mt.stdout.strip(), '| == new head tree:', mt.stdout.strip() == g('rev-parse', NEW + '^{tree}'),
      '| == drafter prediction 1b03e6951:', mt.stdout.strip().startswith('1b03e6951'))
JUDGED = ['package-lock.json', 'scripts/audit/audit-baseline.json', 'services/mcp-server/package-lock.json', 'services/originate/package-lock.json',
          'package.json', 'services/mcp-server/package.json', 'services/originate/package.json', 'scripts/audit/audit-gate.mjs',
          'scripts/audit/audit-locks.mjs', 'scripts/audit/lock-discovery.mjs', 'scripts/audit/baseline-contract.mjs', 'scripts/audit/package.json',
          'scripts/preflight/preflight.sh', 'scripts/preflight/lockfile-cleanroom.sh', 'services/mcp-server/Dockerfile', 'services/originate/Dockerfile',
          'services/mcp-server/src/http-server.ts', 'services/mcp-server/src/index.ts']
print('(2) blobs  file | DEV1 | DEV2 | OLD head | NEW head')
for f in JUDGED:
    b = [g('rev-parse', r + ':' + D + f) for r in (DEV1, DEV2, OLD, NEW)]
    print('    %-44s %s %s %s %s%s' % (f, *[x[:9] for x in b], '' if b[0] == b[1] else '  <- develop moved'))
print('    FULL develop2 baseline blob', g('rev-parse', DEV2 + ':' + D + 'scripts/audit/audit-baseline.json'), '| FULL new-head baseline blob', g('rev-parse', NEW + ':' + D + 'scripts/audit/audit-baseline.json'))
def show(rev, path): return run(['git', '-C', C, 'show', rev + ':' + path]).stdout
def is_hono(k): return k.split('node_modules/')[-1] == 'hono'
def diffp(a, b):
    pa, pb = a['packages'], b['packages']; out = []
    for k in sorted(set(pa) | set(pb)):
        if k not in pa or k not in pb: out.append((k, 'ADDED' if k not in pa else 'REMOVED', None)); continue
        if pa[k] != pb[k]: out.append((k, 'CHANGED', {f: (pa[k].get(f), pb[k].get(f)) for f in sorted(set(pa[k]) | set(pb[k])) if pa[k].get(f) != pb[k].get(f)}))
    return out
RULED = {'lightningcss-' + x for x in ('android-arm64', 'darwin-arm64', 'darwin-x64', 'freebsd-x64', 'linux-arm-gnueabihf', 'linux-arm64-gnu', 'linux-arm64-musl', 'linux-x64-gnu', 'linux-x64-musl', 'win32-arm64-msvc', 'win32-x64-msvc')}
print('(3) parse vs develop 81ee4b729 (the new three-dot base)')
for lk in ('services/mcp-server/package-lock.json', 'services/originate/package-lock.json', 'package-lock.json'):
    a = json.loads(show(DEV2, D + lk)); b = json.loads(show(NEW, D + lk)); d = diffp(a, b)
    hono = [x for x in d if is_hono(x[0])]; other = [x for x in d if not is_hono(x[0])]
    ruled = [x for x in other if (x[0].split('node_modules/')[-1] in RULED and x[2] == {'dev': (True, None)}) or (x[0] == 'node_modules/magicast' and x[2] == {'dev': (True, None), 'devOptional': (None, True)})]
    unexpected = [x for x in other if x not in ruled]
    print('    %s: entries %d/%d | hono %s | non-hono %d (ruled %d, unexpected %d %s) | version fields among non-hono %d' % (
        lk, len(a['packages']), len(b['packages']), [(x[0], x[2].get('version')) for x in hono], len(other), len(ruled), len(unexpected), [u[0] for u in unexpected][:5],
        sum(1 for x in other if x[2] and 'version' in x[2])))
    bb = copy.deepcopy(b); k0 = sorted(k for k in bb['packages'] if k and not is_hono(k))[0]; bb['packages'][k0]['version'] = '9.9.9-planted'
    print('      CONTROL planted version on %s -> non-hono changes %d' % (k0, len([x for x in diffp(a, bb) if not is_hono(x[0])])))
def rows(rev): return json.loads(show(rev, D + 'scripts/audit/audit-baseline.json'))
rb = {r: rows(r) for r in (BASE, DEV2, OLD, NEW)}
for r, j in rb.items(): print('    baseline rows @%s = %d' % (r[:9], len(j['accepted'])))
n, o, dv = rb[NEW]['accepted'], rb[OLD]['accepted'], rb[DEV2]['accepted']
print('    NEW vs OLD: removed', sorted(set(o) - set(n)), '| added', sorted(set(n) - set(o)), '| altered', sorted(k for k in set(o) & set(n) if o[k] != n[k]))
print('    NEW vs DEV2: removed', sorted(set(dv) - set(n)), '| added', sorted(set(n) - set(dv)), '| altered', sorted(k for k in set(dv) & set(n) if dv[k] != n[k]), '| $comment equal', rb[NEW]['$comment'] == rb[DEV2]['$comment'])
dm = copy.deepcopy(rb[DEV2]); [dm['accepted'].pop(k) for k in ('GHSA-gqvv-2mrq-wpjv', 'GHSA-g6gw-c38x-mqfc', 'GHSA-crvj-82cr-hjcx')]
print('    NEW baseline == DEV2 baseline minus 3 hono rows (parsed, order kept):', list(dm['accepted'].items()) == list(n.items()), '| key order equal', list(dm['accepted']) == list(n))
ctrl = copy.deepcopy(n); k1 = next(iter(ctrl)); ctrl[k1] = dict(ctrl[k1], reason=ctrl[k1]['reason'] + 'x')
print('    CONTROL planted reason change -> altered vs DEV2', len([k for k in set(dv) & set(ctrl) if dv[k] != ctrl[k]]))
print('    body text: NEW baseline bytes == DEV2 bytes with the 3 hono objects removed?', end=' ')
tx = show(DEV2, D + 'scripts/audit/audit-baseline.json'); tn = show(NEW, D + 'scripts/audit/audit-baseline.json')
print(json.dumps(dm, indent=2, ensure_ascii=False) + '\n' == tn, '(json.dumps indent=2 round-trip of the parsed-minus-3 object)')
# (4) gates at the new head
scr = tempfile.mkdtemp(prefix='repin-', dir=CLD)
for name, sha in (('newhead', NEW), ('dev2', DEV2)):
    run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', scr + '/wt-' + name, sha])
    a = scr + '/wt-%s/Blockchain/Dev/scripts/audit' % name
    s0 = hashlib.sha256(open(a + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    p = run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=a)
    print('(4) worktree', name, g('-C', scr + '/wt-' + name, 'rev-parse', 'HEAD') if False else sha[:9], '| scripts/audit npm ci rc', p.returncode, '| lock sha', s0, '->', hashlib.sha256(open(a + '/package-lock.json', 'rb').read()).hexdigest()[:16])
cp = {}
for name in ('newhead', 'dev2'):
    cp[name] = scr + '/baseline_%s.json' % name
    open(cp[name], 'wb').write(open(scr + '/wt-%s/Blockchain/Dev/scripts/audit/audit-baseline.json' % name, 'rb').read())
RUNS = [('H1', 'newhead', None), ('H2', 'newhead', cp['dev2']), ('B0', 'dev2', None), ('B1', 'dev2', cp['newhead'])]
for tag, t, bl in RUNS:
    env = dict(os.environ); env.pop('AUDIT_BASELINE_PATH', None)
    if bl: env['AUDIT_BASELINE_PATH'] = bl
    for gate in ('audit-gate', 'audit-locks'):
        t0 = now(); p = run(['node', 'scripts/audit/%s.mjs' % gate], cwd=scr + '/wt-%s/Blockchain/Dev' % t, check=False, env=env)
        text = p.stdout + p.stderr; open(OUT + '/%s_%s.out' % (tag, gate), 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
        first = next((l for l in text.splitlines() if l.startswith(gate + ':')), '')
        cl = sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', text.split('CLEANUP', 1)[1].split('FAIL')[0]))) if 'CLEANUP' in text else []
        fl = sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', text.split('FAIL', 1)[1]))) if 'FAIL' in text else []
        print('    %s %s %s baseline=%s rc %d %s | %s | CLEANUP %s | FAIL %s' % (tag, t, gate, os.path.basename(bl) if bl else 'real', p.returncode, t0, first[:110], cl, fl))
print('    scratch', scr)
# (5) GitHub compare + Linear
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
vals = {k: l.split('=', 1)[1].strip().strip('"').strip("'") for l in open(ENV) for k in ('GH_TOKEN', 'LINEAR_API_KEY') if l.startswith(k + '=')}
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + vals['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
pr = get('/pulls/1022'); c = get('/compare/develop...' + NEW)
print('(5) PR API head', pr['head']['sha'], 'state', pr['state'], 'commits', pr['commits'], 'files', pr['changed_files'], '| compare develop...new: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd]|ing)?|resolve[sd]?|resolving|complete[sd]?|completing|implement(?:s|ed|ing)?)\s*:?\s+(?:#\d+|[A-Z]{2,}-\d+|https?://\S*(?:linear\.app|github\.com)\S*)')
assert CLOSE.findall('Fixes KS-1211') and not CLOSE.findall('Refs KS-1211')
for cm in get('/pulls/1022/commits'): print('    commit', cm['sha'][:9], [p['sha'][:9] for p in cm['parents']], '| closing', CLOSE.findall(cm['commit']['message']), '|', cm['commit']['message'].splitlines()[0][:80])
print('    body closing', CLOSE.findall(pr.get('body') or ''), '| title closing', CLOSE.findall(pr['title']))
q = {'query': 'query($u:String!){ attachmentsForURL(url:$u){ nodes{ metadata issue{ identifier state{name} completedAt } } } }', 'variables': {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1022'}}
d = json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps(q).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
for a in d['data']['attachmentsForURL']['nodes']: print('    attachmentsForURL(pull/1022):', a['issue']['identifier'], a['issue']['state']['name'], 'completedAt', a['issue']['completedAt'], 'linkKind', (a['metadata'] or {}).get('linkKind'))
por = len([l for l in gr('status', '--porcelain').splitlines() if l.strip()])
print('CHECKOUT close porcelain %d | .git/config sha256 %s | refs %d | worktrees %d' % (por, hashlib.sha256(open(REPO + '/.git/config', 'rb').read()).hexdigest()[:16], len(gr('for-each-ref').splitlines()), len(os.listdir(REPO + '/.git/worktrees'))))
print('done', now())
