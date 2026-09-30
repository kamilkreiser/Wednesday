#!/usr/bin/env python3
"""lockcensus_gate48b.py — the drafter's READ (git plumbing only: no build, no install, no bundle) behind ROOT-LOCK-CONSUMERS,
UNDICI-MAJOR-RUNTIME and the census half of ISSUER-IMAGE, at a NAMED tree (default the pinned END_TREE):
  C1 EVERY tracked package-lock.json (node_modules excluded): every `undici` / `js-yaml` / `@connectrpc/connect-node` entry with its version, `dev`
     flag (ABSENT in a v3 lock = PRODUCTION) and — for undici / js-yaml — VULNERABLE per GHSA-r53p / GHSA-r3ph ranges READ from the advisory API.
  C2 ROOT-LOCK-CONSUMERS: every Dockerfile's COPY/ADD line naming a package manifest or lock, resolved against the compose build context that
     uses that Dockerfile (compose `context:` + `dockerfile:` pairs); a line copies the WORKSPACE-ROOT lock when its source is a bare
     `package-lock.json` / `package*.json` (or `./…`) from a context that IS Blockchain/Dev. Control: the same matcher on the issuer Dockerfile
     finds its per-directory `frontend/issuer/package*.json` COPY (a matcher that finds nothing proves nothing).
  C3 UNDICI-MAJOR-RUNTIME (the READ half; the gate builds and measures): (a) every lock carrying @connectrpc/connect-node, its dev flag and its
     declared undici range; (b) every TRACKED source file (node_modules, locks and dist excluded) that names `@connectrpc/connect-node`,
     `@connectrpc/connect-web`, `@utxorpc/sdk`, `@meshsdk/provider`, `@meshsdk/core` or `undici` in an import / require / from string;
     (c) the issuer Dockerfile's final-stage COPY lines (what ships: /app/dist only?) and whether the issuer's vite config names a node-only
     resolution. Controls: the same import matcher finds `react` in frontend/issuer/src (fires) and a nonsense module 0 times.
The gate re-measures ALL of this against a BUILT image — this is a PREDICTION with its instruments named, never evidence.
rc 0 CENSUS DONE (controls hold) / rc 1. Writes lockcensus_gate48b.json (at END) or lockcensus_gate48b.<tree12>.json.
Usage: lockcensus_gate48b.py <scratchpad> [--tree <sha>] [--offline]"""
import json, os, re, subprocess, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48b_sp', 'clone'); T = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
def git(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, check=True).stdout
ADV = {'undici': 'GHSA-r53p-7pc4-xj5r', 'js-yaml': 'GHSA-r3ph-w7gj-g6xm'}
FALLBACK = {'undici': ['< 6.28.1', '>= 7.0.0, < 7.29.1', '>= 8.0.0, < 8.10.2'], 'js-yaml': ['>= 5.0.0, <= 5.4.0']}
def _tok():   # the Secuura GH_TOKEN, read by NAME and never printed: an authenticated GET of the PUBLIC advisory API (5000/h, not 60/h per IP)
    try:
        for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
            if l.startswith('GH_TOKEN='): return l.split('=', 1)[1].strip().strip('"').strip("'")
    except OSError: pass
    return ''
_T = _tok()
def ADVGET(g): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + g, headers=dict({'Accept': 'application/vnd.github+json'}, **({'Authorization': 'Bearer ' + _T} if _T else {}))), timeout=60))
RNG = {}
for pk, g in ADV.items():
    if '--offline' in A: RNG[pk] = FALLBACK[pk]; continue
    a = ADVGET(g)
    RNG[pk] = [v['vulnerable_version_range'] for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == pk]
def V(s): return tuple(int(x) for x in re.findall(r'\d+', s)[:3])
def inr(ver, rng):
    for c in rng.split(','):
        m = re.match(r'\s*(>=|<=|>|<|=)?\s*([\d.]+)', c); op, x = m.group(1) or '=', V(m.group(2)); v = V(ver)
        if not {'>=': v >= x, '<=': v <= x, '>': v > x, '<': v < x, '=': v == x}[op]: return False
    return True
files = git('ls-tree', '-r', '--name-only', T).splitlines()
nm = lambda f: '/node_modules/' in '/' + f
locks = sorted(f for f in files if f.endswith('package-lock.json') and not nm(f))
dfs = sorted(f for f in files if re.search(r'(^|/)Dockerfile[^/]*$', f) and not nm(f))
comp = sorted(f for f in files if re.search(r'(^|/)(docker-)?compose[^/]*\.ya?ml$', f) and not nm(f))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('lockcensus_gate48b %s | tree %s (%s) | %d tracked package-lock.json | %d Dockerfile(s) | %d compose file(s)' % (now, T, 'END_TREE' if T == P['end_tree'] else 'NOT END', len(locks), len(dfs), len(comp)))
print('    ranges READ %s: undici %s | js-yaml %s' % ('(OFFLINE fallback, not read)' if '--offline' in A else 'from the advisory API', RNG['undici'], RNG['js-yaml']))
# C1
rows = []; nent = 0; react = 0; nons = 0
for lk in locks:
    try: d = json.loads(git('show', '%s:%s' % (T, lk)))
    except Exception as e: print('    UNPARSED %s: %s' % (lk, e)); continue
    pk = d.get('packages') or {}; nent += len(pk)
    react += any(k.endswith('node_modules/react') for k in pk); nons += any(k.endswith('node_modules/zz-gate48b-no-such-pkg') for k in pk)
    for k, v in pk.items():
        for name in ('undici', 'js-yaml', '@connectrpc/connect-node'):
            if k.endswith('node_modules/' + name):
                ver = v.get('version', '?'); vul = any(inr(ver, r) for r in RNG[name]) if name in RNG else None
                rows.append(dict(lock=lk, key=k, pkg=name, version=ver, dev=v.get('dev', False), vulnerable=vul, undici_decl=(v.get('dependencies') or {}).get('undici')))
print('C1 undici / js-yaml / connect-node entries in every lock at this tree')
for r in rows:
    print('    %-4s %-25s %-8s dev=%-5s %-58s %s%s' % ({True: 'VUL', False: 'ok', None: '-'}[r['vulnerable']], r['pkg'], r['version'], r['dev'], r['lock'], r['key'][:70], (' | declares undici %s' % r['undici_decl']) if r['undici_decl'] else ''))
vul = [r for r in rows if r['vulnerable']]
print('    VULNERABLE entries: %d in %d lock(s): %s' % (len(vul), len(set(r['lock'] for r in vul)), sorted(set('%s %s %s%s' % (r['lock'], r['pkg'], r['version'], ' (dev)' if r['dev'] else ' (PRODUCTION entry)') for r in vul))))
# C2
ctxs = []
for c in comp:
    base = os.path.dirname(c); cur = None
    for l in git('show', '%s:%s' % (T, c)).splitlines():
        m = re.match(r'\s*context:\s*["\']?([^"\'#\s]+)', l)
        if m: cur = os.path.normpath(os.path.join(base, m.group(1))); ctxs.append([c, cur, None]); continue
        m = re.match(r'\s*dockerfile:\s*["\']?([^"\'#\s]+)', l)
        if m and ctxs and ctxs[-1][2] is None and ctxs[-1][0] == c: ctxs[-1][2] = os.path.normpath(os.path.join(ctxs[-1][1], m.group(1)))
for x in ctxs:
    if x[2] is None: x[2] = os.path.join(x[1], 'Dockerfile')
print('C2 ROOT-LOCK-CONSUMERS: %d compose build context(s); Dockerfile COPY/ADD lines naming a package manifest or lock' % len(ctxs))
ROOTCTX = 'Blockchain/Dev'; root_hits = []; iss_ctl = False; copies = 0
for d in dfs:
    uses = sorted(set(x[1] for x in ctxs if x[2] == d))
    for l in git('show', '%s:%s' % (T, d)).splitlines():
        if not re.match(r'\s*(COPY|ADD)\b', l, re.I) or not re.search(r'package(-lock)?[^ ]*\.json|package\*\.json', l): continue
        copies += 1; toks = [t for t in l.split()[1:] if not t.startswith('--')]; srcs = toks[:-1]
        bare = [s for s in srcs if re.fullmatch(r'(\./)?(package-lock\.json|package\*\.json|package\*\.json|package\.json)', s)]
        isroot = bool(bare) and ROOTCTX in uses and any('lock' in s or '*' in s for s in bare)
        if d == 'Blockchain/Dev/frontend/issuer/Dockerfile' and any(s.startswith('frontend/issuer/package') for s in srcs): iss_ctl = True
        if isroot or (bare and not uses): root_hits.append((d, l.strip(), uses))
        print('    %-4s %-62s ctx %-30s %s' % ('ROOT' if isroot else ('?' if bare and not uses else '-'), d[:62], ','.join(uses) or '(no compose context)', l.strip()[:120]))
print('    ROOT-LOCK copies (a bare lock / package*.json from a context that IS %s): %d %s | bare copies with NO compose context (context unknown — the gate resolves): %d' % (
    ROOTCTX, sum(1 for h in root_hits if ROOTCTX in h[2]), [h[0] for h in root_hits if ROOTCTX in h[2]], sum(1 for h in root_hits if not h[2])))
print('    CONTROL: the matcher finds the issuer Dockerfile\'s per-directory `frontend/issuer/package*.json` COPY: %s | %d manifest/lock COPY line(s) seen' % (iss_ctl, copies))
# C3
print('C3 UNDICI-MAJOR-RUNTIME (READ): where connect-node could run')
for r in rows:
    if r['pkg'] == '@connectrpc/connect-node': print('    (a) %s %s %s dev=%s declares undici %s' % (r['lock'], r['key'], r['version'], r['dev'], r['undici_decl']))
MODS = ['@connectrpc/connect-node', '@connectrpc/connect-web', '@utxorpc/sdk', '@meshsdk/provider', '@meshsdk/core', 'undici', 'react', 'zz-gate48b-no-such-mod']
src = [f for f in files if re.search(r'\.(m?[jt]sx?|cjs|mjs|vue)$', f) and not nm(f) and '/dist/' not in '/' + f and f.startswith('Blockchain/Dev/')]
hits = {m: [] for m in MODS}
for f in src:
    try: t = git('show', '%s:%s' % (T, f))
    except subprocess.CalledProcessError: continue
    for m in MODS:
        if re.search(r'''(from\s+|require\(\s*|import\(\s*|import\s+)['"]%s(/[^'"]*)?['"]''' % re.escape(m), t): hits[m].append(f)
for m in MODS:
    iss = [f for f in hits[m] if f.startswith('Blockchain/Dev/frontend/issuer/')]
    print('    (b) import of %-28s in %4d tracked source file(s) (%d under frontend/issuer): %s' % (m, len(hits[m]), len(iss), hits[m][:6]))
df = git('show', '%s:Blockchain/Dev/frontend/issuer/Dockerfile' % T).splitlines()
st = [i for i, l in enumerate(df) if re.match(r'\s*FROM\b', l, re.I)]
final = df[st[-1]:] if st else []
print('    (c) issuer Dockerfile final stage: %s' % ' || '.join(l.strip() for l in final if re.match(r'\s*(FROM|COPY|ADD)\b', l, re.I)))
vc = [f for f in files if re.fullmatch(r'Blockchain/Dev/frontend/issuer/vite\.config\.[mc]?[jt]s', f)]
for f in vc:
    t = git('show', '%s:%s' % (T, f)); print('    (c) %s: names connect-node %s | undici %s | ssr %s | resolve.conditions %s | nodePolyfills %s' % (
        f, 'connect-node' in t, 'undici' in t, bool(re.search(r'\bssr\b', t)), bool(re.search(r'conditions', t)), bool(re.search(r'nodePolyfills|node-polyfills', t))))
# C4 SUITES (READ): the root lock's workspace members (keys with no node_modules/) that declare vitest / jsdom / @meshsdk/core — the population
# behind the seat's "23 service suites reaching undici only via vitest -> jsdom" (the gate verifies and samples; the drafter runs none)
rl = json.loads(git('show', '%s:Blockchain/Dev/package-lock.json' % T))['packages']
mem = sorted(k for k in rl if k and 'node_modules/' not in k and not rl[k].get('link'))
def decl(k, d): e = rl[k]; return d in (e.get('dependencies') or {}) or d in (e.get('devDependencies') or {}) or d in (e.get('optionalDependencies') or {})
vit = [k for k in mem if decl(k, 'vitest')]; jsd = [k for k in mem if decl(k, 'jsdom')]; msh = [k for k in mem if decl(k, '@meshsdk/core')]
print('C4 SUITES (READ): root-lock workspace members %d | declare vitest %d (services/* %d) | declare jsdom %d %s | declare @meshsdk/core %d %s' % (
    len(mem), len(vit), sum(k.startswith('services/') for k in vit), len(jsd), jsd, len(msh), msh))
print('    vitest members: %s' % ' '.join(vit))
ok = nent > 0 and react >= 1 and nons == 0 and iss_ctl and len([f for f in hits['react'] if '/frontend/issuer/' in f]) > 0 and not hits['zz-gate48b-no-such-mod']
print('CT-PARSE %d entries across %d lock(s) | CT-POS react in %d lock(s), imported in %d issuer file(s) | CT-NEG nonsense package %d lock(s), nonsense import %d file(s) | CT-COPY issuer per-dir COPY found %s -> %s' % (
    nent, len(locks), react, len([f for f in hits['react'] if '/frontend/issuer/' in f]), nons, len(hits['zz-gate48b-no-such-mod']), iss_ctl, 'OK' if ok else 'FAIL'))
json.dump(dict(tree=T, locks=locks, rows=rows, ranges=RNG, contexts=ctxs, root_lock_copies=root_hits, imports={m: v for m, v in hits.items()}), open(os.path.join(G, 'lockcensus_gate48b.json' if T == P['end_tree'] else 'lockcensus_gate48b.%s.json' % T[:12]), 'w'), indent=1)
print('CENSUS %s: %d lock(s), %d undici/js-yaml/connect-node entr(y/ies), %d vulnerable | root-lock copies %d | connect-node imported in %d tracked source file(s)' % (
    'DONE' if ok else 'FAILED', len(locks), len(rows), len(vul), sum(1 for h in root_hits if ROOTCTX in h[2]), len(hits['@connectrpc/connect-node'])))
raise SystemExit(0 if ok else 1)
